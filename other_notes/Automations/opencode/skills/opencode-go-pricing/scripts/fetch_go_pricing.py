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

Each target column is resolved in passes, first success wins:

1. Header alias match against a list of known names. Handles past
   renames (e.g. "Usage" -> "Monthly limit") and lets a new alias be
   added without touching the lookup logic.
2. Value-pattern signature match: every data cell (ignoring `-`/`N/A`
   placeholders) must contain the pattern. Catches renames the alias
   list has never seen.
3. Structural fallback for the request windows: the unique column triple
   in table order satisfying 5h <= week <= month on every complete row.
   Request headers are indistinguishable by value pattern alone, but the
   20%/50%/100% sizing relationship identifies them.

Tables are located by header hints first, then by column signature (the
first table whose columns resolve). Every fallback prints a stderr
warning naming what it found so the name can be promoted into the alias
or hint lists. Total failure still raises, never guesses.

Gotchas the script handles:

- Pricing tier suffixes (`(<= 200K tokens)`, `(Off-Peak)`, `(Peak)`) are
  stripped before joining so the two duplicate rows per model collapse.
- MiMo name spacing differs across tables (`MiMo V2.5` vs `MiMo-V2.5`);
  normalized before joining or MiMo drops out on both sides.
- Promo markup (`<del>$15</del> <strong>$60</strong>`, `4x - Ends Sep 20`)
  is parsed to the current (bold) value; inline tag boundaries emit a
  space so struck-through and current values never concatenate.
- Digit parsing is fully regex-driven and never assumes a clean cell:
  usage takes the last `$` amount (handles commas, decimals, reworded
  promo notes) and counts take the last number (handles commas, k/M/B
  suffixes, `~`/`+` decorations). Cells with no parseable digits yield
  None (rendered `N/A`) instead of raising.
"""

from __future__ import annotations

import itertools
import re
import sys
import urllib.request
from collections.abc import Callable
from html.parser import HTMLParser
from typing import NamedTuple

import polars as pl

URL = "https://opencode.ai/docs/go/"

# Header hints that uniquely identify each table on the docs page.
PRICING_TABLE_HINTS = ("Input", "Output")
REQUESTS_TABLE_HINTS = ("requests per 5 hour", "requests per week", "requests per month")
PRIVACY_TABLE_HINTS = ("Model training", "Data retention")

# Column resolution: header aliases, value-pattern signature, excluded headers.
# Pricing's monthly limit carries a pattern because the column has been
# renamed once already ("Usage" -> "Monthly limit") and we want the next
# rename to resolve automatically. The pattern matches a whole-dollar
# amount anywhere in the cell ($15, $60, "$15 $60 4x ...") and explicitly
# excludes per-token rates ($0.15, $1.40) via the trailing negative
# lookahead. Known per-token price columns are excluded outright, and if
# several columns still match, the lowest-cardinality one wins (tiered
# limits repeat; per-model prices vary) - so a hypothetical whole-dollar
# Input price can never shadow the limit column.
class ColumnLookup(NamedTuple):
    """How to locate one target column."""

    aliases: tuple[str, ...]
    pattern: re.Pattern[str] | None
    exclude: tuple[str, ...] = ()


# Per-token price columns: never the monthly limit, even if whole-dollar.
PRICE_COLUMN_ALIASES: tuple[str, ...] = ("Input", "Output", "Cached Read", "Cached Write")

COLUMN_LOOKUPS: dict[str, ColumnLookup] = {
    "pricing_limit": ColumnLookup(
        ("Monthly limit", "Usage", "Usage limit", "Monthly cap"),
        re.compile(r"\$\d+(?![\d.])"),
        PRICE_COLUMN_ALIASES,
    ),
    "requests_5h": ColumnLookup(("requests per 5 hour", "requests per 5 hours"), None),
    "requests_week": ColumnLookup(("requests per week",), None),
    "requests_month": ColumnLookup(("requests per month",), None),
    "privacy_retention": ColumnLookup(
        ("Data retention", "Retention", "Data storage"),
        re.compile(r"(?i)\b(?:\d+\s*days?\*?|ZDR)\b"),
    ),
}

# Cell markers treated as missing data and skipped by signature matching.
_MISSING_MARKERS: frozenset[str] = frozenset({"-", "N/A", "n/a", "NA"})

# A request-count cell: plain or comma-grouped ints, decimals, k/M/B
# suffixes, promo pairs ("6,500 26,000"), "~"/"+" decorations.
INT_CELL_RE: re.Pattern[str] = re.compile(
    r"^\s*[\d,]+(?:\.\d+)?\s*[kKmMbB]?"
    r"(?:\s+[\d,]+(?:\.\d+)?\s*[kKmMbB]?)*\s*[+~]?\s*$"
)

# Pricing tier suffixes to strip before joining on the model column.
TIER_SUFFIX_PATTERNS: tuple[str, ...] = (
    r"\s*\([≤<>]\s*\d+K\s*tokens\)",
    r"\s*\(Off-Peak\)",
    r"\s*\(Peak\)",
)

# Promo suffixes to strip before joining on the model column. Kept generic
# (multiplier + separator + note, bullet + keyword + note, or bare
# Ends/Until/Through + date) so reworded promos still strip. All patterns
# are ASCII-escaped; \u00b7 is middle dot, \u2022 is bullet.
PROMO_SUFFIX_PATTERNS: tuple[str, ...] = (
    r"\s*\d+\s*x\s*[\u00b7\u2022\-\u2013\u2014].*$",
    r"\s*\d+\s*x\s+(?i:ends|until|through|limited|promo|sale|offer|new|only|now)\b.*$",
    r"\s*[\u00b7\u2022]\s*(?i:ends|until|through|limited|promo|sale|offer|new).*$",
    r"\s*(?i:ends|until|through)\s+\w+\s+\d+.*$",
    r"\s*\(\s*(?i:limited|promo|sales?|offers?|special).*?\)\s*$",
    r"\s*(?i:limited time|on sale)\s*$",
)

# Inline tags whose boundaries separate values inside a cell. Without a
# separator, `<del>$15</del> <strong>$60</strong>` followed by
# `<small>4x ...</small>` (or `<del>6,500</del><br><strong>26,000</strong>`)
# concatenates into "$15 $604x ..." / "6,50026,000", which no parser can
# split reliably. Emitting a space on these boundaries keeps the
# struck-through (old) and bold (current) values distinct. `span` is
# included because promo values are often span-wrapped; the residual risk
# (a mid-word styled fragment inside a model name gaining a space and
# missing its join) is accepted because the docs tables style values,
# not partial names.
_CELL_SEPARATOR_TAGS: tuple[str, ...] = (
    "del",
    "s",
    "strike",
    "strong",
    "b",
    "small",
    "span",
    "sup",
    "sub",
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
        elif tag == "br" and self._current_cell is not None:
            self._current_cell.append(" ")
        elif tag in _CELL_SEPARATOR_TAGS and self._current_cell is not None:
            self._current_cell.append(" ")

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
                raw = "".join(self._current_cell)
                self._current_row.append(re.sub(r"\s+", " ", raw).strip())
            self._current_cell = None
        elif tag in _CELL_SEPARATOR_TAGS and self._current_cell is not None:
            self._current_cell.append(" ")

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
    exclude_aliases: tuple[str, ...] = (),
) -> tuple[int, str] | None:
    """Find a column by header alias (preferred) or value-pattern (fallback).

    Returns `(column_index, column_name)`, or `None` if neither resolves.
    Emits a stderr warning when the value-pattern fallback fires so the
    operator can promote the discovered name into the alias list.
    Placeholder cells (`-`, `N/A`) are ignored by signature matching. When
    several columns match, excluded headers drop out first, then the
    lowest-cardinality column wins (tiered limits repeat; prices vary).
    """
    if len(table) < 2:
        return None
    header = table[0]

    # Pass 1: header alias match.
    for alias in aliases:
        for col_idx, col_name in enumerate(header):
            if col_name.lower() == alias.lower():
                return (col_idx, col_name)

    # Pass 2: value-pattern signature. A column matches only when every
    # data cell contains the pattern (search, not full match, so promo
    # cells like "$15 $60 4x ..." still resolve).
    if pattern is not None:
        excluded = {e.lower() for e in exclude_aliases}
        matches: list[int] = []
        for col_idx in range(len(header)):
            if header[col_idx].lower() in excluded:
                continue
            values = [
                row[col_idx]
                for row in table[1:]
                if col_idx < len(row)
                and row[col_idx].strip()
                and row[col_idx].strip() not in _MISSING_MARKERS
            ]
            if values and all(pattern.search(v) for v in values):
                matches.append(col_idx)
        if not matches:
            return None
        matches.sort(
            key=lambda i: (len({row[i] for row in table[1:] if i < len(row)}), i)
        )
        col_idx = matches[0]
        col_name = header[col_idx]
        extra = f"; also matched {[header[i] for i in matches[1:]]}" if len(matches) > 1 else ""
        print(
            f"warning: column {col_name!r} matched by value pattern "
            f"{pattern.pattern!r}{extra}; add it to the alias list "
            f"(tried: {aliases}).",
            file=sys.stderr,
        )
        return (col_idx, col_name)

    return None


def _int_like_columns(table: list[list[str]]) -> list[int]:
    """Return indices of non-model columns whose data cells all look like counts.

    Column 0 holds model names everywhere in this script, so it is never a
    candidate (a future `405B`-style name must not read as a count).
    """
    if len(table) < 2:
        return []
    header = table[0]
    candidates: list[int] = []
    for col_idx in range(1, len(header)):
        values = [
            row[col_idx]
            for row in table[1:]
            if col_idx < len(row)
            and row[col_idx].strip()
            and row[col_idx].strip() not in _MISSING_MARKERS
        ]
        if values and all(INT_CELL_RE.match(v) for v in values):
            candidates.append(col_idx)
    return candidates


def _resolve_request_triplet(table: list[list[str]]) -> tuple[int, int, int]:
    """Resolve (5h, week, month) indices by magnitude order.

    Structural fallback for renamed request headers: the three windows are
    20%/50%/100% of one monthly base, so in every complete row the 5-hour
    count <= weekly count <= monthly count. The unique column assignment
    satisfying that across rows wins, whatever the column order. Raises
    RuntimeError when zero or several assignments qualify - ambiguity must
    stay loud.
    """
    valid: list[tuple[int, int, int]] = []
    for trio in itertools.permutations(_int_like_columns(table), 3):
        checked = 0
        ok = True
        for row in table[1:]:
            if any(i >= len(row) for i in trio):
                continue
            va, vb, vc = (parse_int(row[i]) for i in trio)
            if va is None or vb is None or vc is None:
                continue
            checked += 1
            if not (va <= vb <= vc):
                ok = False
                break
        if ok and checked > 0:
            valid.append(trio)
    if len(valid) != 1:
        raise RuntimeError(
            "could not resolve the request window columns by magnitude order; "
            f"qualifying triples {valid} in header {table[0] if table else []}"
        )
    result = valid[0]
    print(
        "warning: request window columns resolved by magnitude order as "
        f"{[table[0][i] for i in result]}; add them to the alias lists.",
        file=sys.stderr,
    )
    return result


def _resolve_request_columns(table: list[list[str]]) -> tuple[int, int, int]:
    """Resolve the 5h/week/month indices via aliases, else magnitude order."""
    lookups = COLUMN_LOOKUPS
    try:
        return (
            _resolve_column(table, lookups["requests_5h"], "requests per 5 hour"),
            _resolve_column(table, lookups["requests_week"], "requests per week"),
            _resolve_column(table, lookups["requests_month"], "requests per month"),
        )
    except RuntimeError:
        return _resolve_request_triplet(table)


def _search_tables(
    tables: list[list[list[str]]],
    label: str,
    resolve: Callable[[list[list[str]]], object],
) -> list[list[str]] | None:
    """Return the first table `resolve` succeeds on; None when none qualify.

    Structural fallback for renamed table headers: a table counts as the
    target when its columns resolve. Warns, since a new hint alias is
    cheaper than a scan.
    """
    for table in tables:
        try:
            resolve(table)
        except RuntimeError:
            continue
        print(
            f"warning: located the {label} table by column signature "
            f"(header {table[0] if table else []}); add its headers to the hint lists.",
            file=sys.stderr,
        )
        return table
    return None


def normalize_name(name: str | None) -> str | None:
    """Map a model name to its canonical form for joins.

    Strips pricing tier suffixes (`(<= 200K tokens)`, `(Off-Peak)`, etc.),
    promo suffixes (`4x · Ends Sep 20`), and fixes the MiMo spacing
    mismatch (`MiMo V2.5 Pro` -> `MiMo-V2.5-Pro`) so all three tables
    share a single join key.
    """
    if name is None:
        return None
    for pattern in PROMO_SUFFIX_PATTERNS:
        name = re.sub(pattern, "", name)
    for pattern in TIER_SUFFIX_PATTERNS:
        name = re.sub(pattern, "", name)
    name = re.sub(r"^MiMo V(\d+\.\d+) Pro$", r"MiMo-V\1-Pro", name)
    name = re.sub(r"^MiMo V(\d+\.\d+)$", r"MiMo-V\1", name)
    return name.strip()


def parse_usage(value: str | None) -> int | float | None:
    """Parse a monthly-limit cell to dollars; blank, '-', or None to None.

    Extracts every `$`-prefixed amount via regex and returns the last one,
    so promo cells (`$15 $60 4x ...`) resolve to the current (bold) price.
    Handles thousands separators (`$1,200`) and decimals (`$59.99`,
    returned as float); per-token rates (`$0.15`) parse without crashing
    if a column is ever misresolved. Returns None when no amount is found
    instead of raising.
    """
    if value is None:
        return None
    value = value.strip()
    if not value or value == "-":
        return None
    amounts = re.findall(r"\$\s*([\d,]+(?:\.\d+)?)", value)
    amounts = [a for a in amounts if re.search(r"\d", a)]
    if not amounts:
        return None
    last = amounts[-1].replace(",", "")
    return float(last) if "." in last else int(last)


def parse_int(value: str | None) -> int | None:
    """Parse a request-count cell to int; blank, '-', or None to None.

    Extracts every number via regex and returns the last one, so promo
    cells (`6,500 26,000`) resolve to the current (bold) count. Handles
    thousands separators, compact suffixes (`26k`, `1.2M`, `2.5B`), and
    stray decorations (`~26,000`, `26,000+`). Returns None when no number
    is found (e.g. `N/A`, `unlimited`) instead of raising.
    """
    if value is None:
        return None
    value = value.strip()
    if not value or value == "-":
        return None
    candidates = re.findall(r"[\d,]+(?:\.\d+)?\s*[kKmMbB]?", value)
    candidates = [c for c in candidates if re.search(r"\d", c)]
    if not candidates:
        return None
    last = candidates[-1].strip()
    multiplier = 1
    if last[-1] in "kK":
        multiplier = 1_000
    elif last[-1] in "mM":
        multiplier = 1_000_000
    elif last[-1] in "bB":
        multiplier = 1_000_000_000
    number = last[:-1] if multiplier != 1 else last
    number = number.replace(",", "").strip()
    try:
        return int(float(number) * multiplier)
    except ValueError:
        return None


def render_markdown(df: pl.DataFrame) -> str:
    """Render a Polars DataFrame as a markdown pipe table with `N/A` for nulls."""
    columns = df.columns
    lines = ["| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in df.iter_rows(named=True):
        cells = [_format_cell(row[c]) for c in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _resolve_column(table: list[list[str]], lookup: ColumnLookup, label: str) -> int:
    """Resolve a column index; raise RuntimeError with diagnostic context on miss."""
    result = find_column(table, lookup.aliases, lookup.pattern, lookup.exclude)
    if result is None:
        pattern_repr = lookup.pattern.pattern if lookup.pattern is not None else "none"
        raise RuntimeError(
            f"could not locate the {label} column; tried aliases {lookup.aliases} "
            f"and pattern {pattern_repr!r}"
        )
    return result[0]


def _format_cell(value: object) -> str:
    """Format one cell: None as `N/A`, integral floats without decimals."""
    if value is None:
        return "N/A"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def build_table() -> pl.DataFrame:
    """Fetch the page, parse tables, and return the joined DataFrame."""
    html = fetch_html(URL)
    tables = extract_tables(html)

    pricing_table = find_table_by_hints(tables, PRICING_TABLE_HINTS)
    if pricing_table is None:
        pricing_table = _search_tables(
            tables,
            "pricing",
            lambda t: _resolve_column(
                t, COLUMN_LOOKUPS["pricing_limit"], "pricing monthly limit"
            ),
        )
    if pricing_table is None:
        raise RuntimeError(
            "could not locate the pricing table (no table has Input + Output columns)"
        )
    requests_table = find_table_by_hints(tables, REQUESTS_TABLE_HINTS)
    if requests_table is None:
        requests_table = _search_tables(tables, "requests", _resolve_request_columns)
    if requests_table is None:
        raise RuntimeError("could not locate the requests table")
    privacy_table = find_table_by_hints(tables, PRIVACY_TABLE_HINTS)
    if privacy_table is None:
        privacy_table = _search_tables(
            tables,
            "privacy",
            lambda t: _resolve_column(
                t, COLUMN_LOOKUPS["privacy_retention"], "privacy data retention"
            ),
        )
    if privacy_table is None:
        raise RuntimeError("could not locate the privacy table")

    limit_idx = _resolve_column(
        pricing_table, COLUMN_LOOKUPS["pricing_limit"], "pricing monthly limit"
    )
    req_5h_idx, req_week_idx, req_month_idx = _resolve_request_columns(requests_table)
    retention_idx = _resolve_column(
        privacy_table, COLUMN_LOOKUPS["privacy_retention"], "privacy data retention"
    )

    # Tripwire: alias-resolved windows must still satisfy 5h <= week <= month
    # on complete rows; a violation means the docs changed semantics, not
    # just names, so warn instead of printing suspect numbers silently.
    for row in requests_table[1:]:
        if not row or not row[0].strip():
            continue
        if max(req_5h_idx, req_week_idx, req_month_idx) >= len(row):
            continue
        va, vb, vc = (parse_int(row[i]) for i in (req_5h_idx, req_week_idx, req_month_idx))
        if va is None or vb is None or vc is None:
            continue
        if not (va <= vb <= vc):
            print(
                f"warning: request windows violate 5h <= week <= month in row "
                f"{row[0]!r}; check whether the docs changed semantics.",
                file=sys.stderr,
            )
            break

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
