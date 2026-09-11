#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["polars>=1.0"]
# ///
"""Fetch opencode Go docs and print the joined model table.

Reads https://opencode.ai/docs/go/, extracts three tables (Pricing,
Requests per period, Privacy), normalizes model names, joins them on
the model column with a left join from pricing (so models with no
request counts such as MiniMax M2.5 are kept), sorts by Usage (USD)
descending then requests per 5 hour descending, and prints a markdown
table.

Null request counts and null data-retention values render as `N/A`.

Each target column is resolved in two passes:

1. Header alias match against a list of known names. Handles past
   renames (e.g. "Usage" -> "Monthly limit") and lets a new alias be
   added without touching the lookup logic.
2. Value-pattern signature match against every non-empty cell in the
   column. Catches future renames the alias list has never seen. When
   the fallback fires, a stderr warning names the discovered column so
   it can be promoted into the alias list.

Gotchas the script handles:

- Pricing tier suffixes (`(<= 200K tokens)`, `(Off-Peak)`, `(Peak)`) are
  stripped before joining so the two duplicate rows per model collapse.
- MiMo name spacing differs across tables (`MiMo V2.5` vs `MiMo-V2.5`);
  normalized before joining or MiMo drops out on both sides.
"""

from __future__ import annotations

import re
import sys
import urllib.request
from html.parser import HTMLParser

import polars as pl

URL = "https://opencode.ai/docs/go/"

# Header hints that uniquely identify each table on the docs page.
PRICING_TABLE_HINTS = ("Input", "Output")
REQUESTS_TABLE_HINTS = ("requests per 5 hour", "requests per week", "requests per month")
PRIVACY_TABLE_HINTS = ("Model training", "Data retention")

# Column resolution: (header aliases, optional value-pattern signature).
# Pricing's monthly limit carries a pattern because the column has been
# renamed once already ("Usage" -> "Monthly limit") and we want the next
# rename to resolve automatically. The pattern matches whole-dollar
# amounts only ($15, $60) and explicitly excludes per-token rates
# ($0.15, $1.40) so the heuristic does not misfire on sibling columns.
COLUMN_LOOKUPS: dict[str, tuple[tuple[str, ...], re.Pattern[str] | None]] = {
    "pricing_limit": (
        ("Monthly limit", "Usage", "Usage limit", "Monthly cap"),
        re.compile(r"^\$\d+$"),
    ),
    "requests_5h": (("requests per 5 hour",), None),
    "requests_week": (("requests per week",), None),
    "requests_month": (("requests per month",), None),
    "privacy_retention": (("Data retention",), None),
}

# Pricing tier suffixes to strip before joining on the model column.
TIER_SUFFIX_PATTERNS: tuple[str, ...] = (
    r"\s*\([≤<>]\s*\d+K\s*tokens\)",
    r"\s*\(Off-Peak\)",
    r"\s*\(Peak\)",
)


class TableExtractor(HTMLParser):
    """Collect every `<table>` in the document as rows of cell strings."""

    def __init__(self) -> None:
        """Initialize the extractor with empty state."""
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self._current_table: list[list[str]] | None = None
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None

    def handle_starttag(self, tag: str, _attrs: list[tuple[str, str | None]]) -> None:
        """Record an opening table, row, or cell tag."""
        # _attrs unused - required by HTMLParser override.
        if tag == "table":
            self._current_table = []
        elif tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif tag in ("td", "th") and self._current_row is not None:
            self._current_cell = []

    def handle_endtag(self, tag: str) -> None:
        """Close the current cell, row, or table and store completed rows."""
        if tag == "table" and self._current_table is not None:
            self.tables.append(self._current_table)
            self._current_table = None
        elif (
            tag == "tr"
            and self._current_row is not None
            and self._current_table is not None
        ):
            self._current_table.append(self._current_row)
            self._current_row = None
        elif tag in ("td", "th") and self._current_cell is not None:
            if self._current_row is not None:
                self._current_row.append("".join(self._current_cell).strip())
            self._current_cell = None

    def handle_data(self, data: str) -> None:
        """Append character data to the current cell."""
        if self._current_cell is not None:
            self._current_cell.append(data)


def fetch_html(url: str) -> str:
    """Fetch the page and return its body as text."""
    request = urllib.request.Request(  # noqa: S310 - URL is the hardcoded Go docs page
        url, headers={"User-Agent": "opencode-go-pricing-skill"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 - URL is the hardcoded Go docs page
        return response.read().decode("utf-8")


def extract_tables(html: str) -> list[list[list[str]]]:
    """Parse `html` and return every table as rows of cell strings."""
    extractor = TableExtractor()
    extractor.feed(html)
    return extractor.tables


def find_table_by_hints(
    tables: list[list[list[str]]], hints: tuple[str, ...]
) -> list[list[str]] | None:
    """Return the first table whose header contains every hint (case-insensitive)."""
    required = {h.lower() for h in hints}
    for table in tables:
        if len(table) < 2:
            continue
        header = {cell.lower() for cell in table[0]}
        if required.issubset(header):
            return table
    return None


def find_column(
    table: list[list[str]],
    aliases: tuple[str, ...],
    pattern: re.Pattern[str] | None = None,
) -> tuple[int, str] | None:
    """Find a column by header alias (preferred) or value-pattern (fallback).

    Returns `(column_index, column_name)`, or `None` if neither resolves.
    Emits a stderr warning when the value-pattern fallback fires so the
    operator can promote the discovered name into the alias list.
    """
    if len(table) < 2:
        return None
    header = table[0]

    # Pass 1: header alias match.
    for alias in aliases:
        for col_idx, col_name in enumerate(header):
            if col_name.lower() == alias.lower():
                return (col_idx, col_name)

    # Pass 2: value-pattern signature. Matches only when every non-empty
    # cell in the column satisfies the regex.
    if pattern is not None:
        for col_idx in range(len(header)):
            values = [
                row[col_idx]
                for row in table[1:]
                if col_idx < len(row) and row[col_idx].strip()
            ]
            if values and all(pattern.match(v) for v in values):
                col_name = header[col_idx]
                print(
                    f"warning: column {col_name!r} matched by value pattern "
                    f"{pattern.pattern!r}; add it to the alias list "
                    f"(tried: {aliases}).",
                    file=sys.stderr,
                )
                return (col_idx, col_name)

    return None


def normalize_name(name: str | None) -> str | None:
    """Map a model name to its canonical form for joins.

    Strips pricing tier suffixes (`(<= 200K tokens)`, `(Off-Peak)`, etc.)
    and fixes the MiMo spacing mismatch (`MiMo V2.5 Pro` -> `MiMo-V2.5-Pro`)
    so all three tables share a single join key.
    """
    if name is None:
        return None
    for pattern in TIER_SUFFIX_PATTERNS:
        name = re.sub(pattern, "", name)
    name = re.sub(r"^MiMo V(\d+\.\d+) Pro$", r"MiMo-V\1-Pro", name)
    name = re.sub(r"^MiMo V(\d+\.\d+)$", r"MiMo-V\1", name)
    return name.strip()


def parse_usage(value: str | None) -> int | None:
    """Parse '$60' to 60; blank, '-', or None to None."""
    if value is None:
        return None
    value = value.strip()
    if not value or value == "-":
        return None
    return int(value.lstrip("$"))


def parse_int(value: str | None) -> int | None:
    """Parse '1,150' to 1150; blank, '-', or None to None."""
    if value is None:
        return None
    value = value.strip()
    if not value or value == "-":
        return None
    return int(value.replace(",", ""))


def render_markdown(df: pl.DataFrame) -> str:
    """Render a Polars DataFrame as a markdown pipe table with `N/A` for nulls."""
    columns = df.columns
    lines = ["| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in df.iter_rows(named=True):
        cells = ["N/A" if row[c] is None else str(row[c]) for c in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _resolve_column(
    table: list[list[str]],
    lookup: tuple[tuple[str, ...], re.Pattern[str] | None],
    label: str,
) -> int:
    """Resolve a column index; raise RuntimeError with diagnostic context on miss."""
    aliases, pattern = lookup
    result = find_column(table, aliases, pattern)
    if result is None:
        pattern_repr = pattern.pattern if pattern is not None else "none"
        raise RuntimeError(
            f"could not locate the {label} column; tried aliases {aliases} "
            f"and pattern {pattern_repr!r}"
        )
    return result[0]


def build_table() -> pl.DataFrame:
    """Fetch the page, parse tables, and return the joined DataFrame."""
    html = fetch_html(URL)
    tables = extract_tables(html)

    pricing_table = find_table_by_hints(tables, PRICING_TABLE_HINTS)
    if pricing_table is None:
        raise RuntimeError(
            "could not locate the pricing table (no table has Input + Output columns)"
        )
    requests_table = find_table_by_hints(tables, REQUESTS_TABLE_HINTS)
    if requests_table is None:
        raise RuntimeError("could not locate the requests table")
    privacy_table = find_table_by_hints(tables, PRIVACY_TABLE_HINTS)
    if privacy_table is None:
        raise RuntimeError("could not locate the privacy table")

    limit_idx = _resolve_column(
        pricing_table, COLUMN_LOOKUPS["pricing_limit"], "pricing monthly limit"
    )
    req_5h_idx = _resolve_column(
        requests_table, COLUMN_LOOKUPS["requests_5h"], "requests per 5 hour"
    )
    req_week_idx = _resolve_column(
        requests_table, COLUMN_LOOKUPS["requests_week"], "requests per week"
    )
    req_month_idx = _resolve_column(
        requests_table, COLUMN_LOOKUPS["requests_month"], "requests per month"
    )
    retention_idx = _resolve_column(
        privacy_table, COLUMN_LOOKUPS["privacy_retention"], "privacy data retention"
    )

    # Build per-table row lists as dicts so columns with missing cells
    # (e.g. Cached Write showing "-") do not shift the schema.
    pricing_rows: list[dict[str, object]] = []
    for row in pricing_table[1:]:
        if not row or not row[0].strip():
            continue
        pricing_rows.append(
            {
                "model": normalize_name(row[0]),
                "usage": parse_usage(row[limit_idx]) if limit_idx < len(row) else None,
            }
        )
    pricing = pl.DataFrame(pricing_rows).unique(subset=["model"], keep="first")

    requests_rows: list[dict[str, object]] = []
    for row in requests_table[1:]:
        if not row or not row[0].strip():
            continue
        requests_rows.append(
            {
                "model": normalize_name(row[0]),
                "req_5h": parse_int(row[req_5h_idx]) if req_5h_idx < len(row) else None,
                "req_week": parse_int(row[req_week_idx]) if req_week_idx < len(row) else None,
                "req_month": parse_int(row[req_month_idx]) if req_month_idx < len(row) else None,
            }
        )
    requests = pl.DataFrame(requests_rows)

    privacy_rows: list[dict[str, object]] = []
    for row in privacy_table[1:]:
        if not row or not row[0].strip():
            continue
        privacy_rows.append(
            {
                "model": normalize_name(row[0]),
                "data_retention": row[retention_idx] if retention_idx < len(row) else None,
            }
        )
    privacy = pl.DataFrame(privacy_rows)

    return (
        pricing
        .join(requests, on="model", how="left")
        .join(privacy, on="model", how="left")
        .sort(["usage", "req_5h"], descending=[True, True], nulls_last=True)
        .select(["model", "usage", "req_5h", "req_week", "req_month", "data_retention"])
    )


def main() -> int:
    """Fetch, join, and print the Go model table."""
    try:
        df = build_table()
    except Exception as exc:  # noqa: BLE001 - top-level CLI error boundary
        print(f"error: {exc}", file=sys.stderr)  # noqa: T201 - CLI error output
        return 1
    print(render_markdown(df))  # noqa: T201 - script output is the markdown table
    return 0


if __name__ == "__main__":
    sys.exit(main())
