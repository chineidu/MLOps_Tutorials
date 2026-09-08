#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["polars>=1.0"]
# ///
"""Fetch opencode Go docs and print the joined model table.

Reads https://opencode.ai/docs/go/, extracts three tables (Pricing,
Requests per period, Privacy), normalizes model names, joins them on the
model column with a left join from pricing (so models with no request
counts such as MiniMax M2.5 are kept), sorts by Usage (USD) descending
then requests per 5 hour descending, and prints a markdown table.

Null request counts and null data-retention values render as `N/A`.
"""

from __future__ import annotations

import re
import sys
import urllib.request
from html.parser import HTMLParser

import polars as pl

URL = "https://opencode.ai/docs/go/"

# Pricing tier suffixes to strip before joining on the model column.
TIER_SUFFIX_PATTERNS: tuple[str, ...] = (
    r"\s*\([≤<>]\s*\d+K\s*tokens\)",
    r"\s*\(Off-Peak\)",
    r"\s*\(Peak\)",
)

# MiMo name normalization. Pricing writes `MiMo V2.5` and `MiMo V2.5 Pro`;
# the other two tables write `MiMo-V2.5` and `MiMo-V2.5-Pro`. The Pro
# pattern must run before the bare pattern so both anchor correctly.
MIMO_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"^MiMo V(\d+\.\d+) Pro$", r"MiMo-\1-Pro"),
    (r"^MiMo V(\d+\.\d+)$", r"MiMo-\1"),
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


def find_table(
    tables: list[list[list[str]]], required_cols: set[str]
) -> list[list[str]] | None:
    """Return the first matching table.

    The header row must contain every required column (case-insensitive comparison).
    """
    required = {c.lower() for c in required_cols}
    for table in tables:
        if len(table) < 2:
            continue
        header = {cell.lower() for cell in table[0]}
        if required.issubset(header):
            return table
    return None


def rows_to_dataframe(rows: list[list[str]]) -> pl.DataFrame:
    """Build a Polars DataFrame from a parsed HTML table.

    rows[0] is the header; every row after it is data (HTML tables have no separator row).
    """
    if len(rows) < 2:
        return pl.DataFrame()
    header = rows[0]
    data = rows[1:]
    return pl.DataFrame(data, schema=header, orient="row")


def normalize_name(name: str | None) -> str | None:
    """Map a model name to its canonical form for joins.

    Strips pricing tier suffixes (`(≤ 200K tokens)`, `(Off-Peak)`, etc.)
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


def normalize_model_column() -> pl.Expr:
    """Expression that adds a normalized `model` column from `Model`."""
    return (
        pl.col("Model")
        .map_elements(normalize_name, return_dtype=pl.Utf8, skip_nulls=True)
        .alias("model")
    )


def parse_usage(value: str | None) -> int | None:
    """Parse '$60' to 60; blank, '-', or None to None."""
    if value is None:
        return None
    value = value.strip()
    if not value or value == "-":
        return None
    return int(value.lstrip("$"))


def render_markdown(df: pl.DataFrame) -> str:
    """Render a Polars DataFrame as a markdown pipe table with `N/A` for nulls."""
    columns = df.columns
    lines = ["| " + " | ".join(columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in df.iter_rows(named=True):
        cells = ["N/A" if row[c] is None else str(row[c]) for c in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_table() -> pl.DataFrame:
    """Fetch the page, parse tables, and return the joined DataFrame."""
    html = fetch_html(URL)
    tables = extract_tables(html)

    pricing_rows = find_table(tables, {"Input", "Output", "Usage"})
    requests_rows = find_table(
        tables,
        {
            "requests per 5 hour",
            "requests per week",
            "requests per month",
        },
    )
    privacy_rows = find_table(tables, {"Model training", "Data retention"})

    missing = [
        name
        for name, rows in (
            ("pricing", pricing_rows),
            ("requests", requests_rows),
            ("privacy", privacy_rows),
        )
        if rows is None
    ]
    if missing:
        raise RuntimeError("could not locate tables on the page: " + ", ".join(missing))

    pricing = rows_to_dataframe(pricing_rows).with_columns(normalize_model_column())
    requests = rows_to_dataframe(requests_rows).with_columns(normalize_model_column())
    privacy = rows_to_dataframe(privacy_rows).with_columns(normalize_model_column())

    # Collapse pricing tier duplicates to one row per model.
    pricing = pricing.unique(subset=["model"], keep="first")

    # Sort key: parsed Usage integer. None sorts last when descending.
    # Secondary key: requests per 5 hour, so models sharing a Usage tier
    # order by highest throughput first.
    pricing = pricing.with_columns(
        pl.col("Usage")
        .map_elements(parse_usage, return_dtype=pl.Int64, skip_nulls=False)
        .alias("_usage_int")
    )

    pricing_cols = pricing.select(["model", "Usage", "_usage_int"])
    # Request counts use thousand-separator commas (`2,150`); cast to int
    # only after stripping them. strict=False keeps unparseable cells as null
    # rather than raising.
    requests_cols = requests.select(
        [
            "model",
            pl.col("requests per 5 hour")
            .str.replace(",", "")
            .cast(pl.Int64, strict=False)
            .alias("req_5h"),
            pl.col("requests per week")
            .str.replace(",", "")
            .cast(pl.Int64, strict=False)
            .alias("req_week"),
            pl.col("requests per month")
            .str.replace(",", "")
            .cast(pl.Int64, strict=False)
            .alias("req_month"),
        ]
    )
    privacy_cols = privacy.select(
        ["model", pl.col("Data retention").alias("data_retention")]
    )

    return (
        pricing_cols.join(requests_cols, on="model", how="left")
        .join(privacy_cols, on="model", how="left")
        .sort(["_usage_int", "req_5h"], descending=[True, True], nulls_last=True)
        .rename({"Usage": "usage"})
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
