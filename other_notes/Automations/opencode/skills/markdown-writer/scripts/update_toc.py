#!/usr/bin/env python3
"""Insert or refresh a GFM table of contents between TOC markers.

Stdlib only. Matches VS Code Markdown All in One markers:

    <!-- TOC -->
    ...
    <!-- /TOC -->

Also refreshes doctoc markers if those are already present.

Usage:
    python3 update_toc.py path/to/file.md
    python3 update_toc.py --min-level 2 --max-level 3 file.md
    python3 update_toc.py --check file.md
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

TOC_START = "<!-- TOC -->"
TOC_END = "<!-- /TOC -->"
DOCTOC_START_RE = re.compile(r"^<!-- START doctoc.*-->$")
DOCTOC_END_RE = re.compile(r"^<!-- END doctoc.*-->$")
ATX_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
FRONTMATTER_RE = re.compile(r"^---\s*$")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
MD_EMPH_RE = re.compile(r"[*_`]+")
NON_SLUG_RE = re.compile(r"[^\w\-]", flags=re.UNICODE)


def strip_inline_md(text: str) -> str:
    text = MD_IMAGE_RE.sub(r"\1", text)
    text = MD_LINK_RE.sub(r"\1", text)
    return MD_EMPH_RE.sub("", text).strip()


def github_slug(text: str) -> str:
    """GitHub-style heading id (github-slugger order)."""
    value = strip_inline_md(text).lower().replace(" ", "-")
    value = NON_SLUG_RE.sub("", value).strip("-")
    return value or "section"


def unique_slug(base: str, seen: dict[str, int]) -> str:
    count = seen.get(base, 0)
    seen[base] = count + 1
    if count == 0:
        return base
    return f"{base}-{count}"


def iter_headings(lines: Sequence[str]) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False
    fence_marker: str | None = None
    i = 0
    if lines and FRONTMATTER_RE.match(lines[0]):
        i = 1
        while i < len(lines):
            if FRONTMATTER_RE.match(lines[i]):
                i += 1
                break
            i += 1
    while i < len(lines):
        line = lines[i]
        fence = FENCE_RE.match(line.strip())
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            i += 1
            continue
        if not in_fence:
            match = ATX_RE.match(line)
            if match:
                headings.append((len(match.group(1)), match.group(2).strip()))
        i += 1
    return headings


def find_marker_block(lines: Sequence[str]) -> tuple[int, int] | None:
    start = end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == TOC_START or DOCTOC_START_RE.match(stripped):
            start = i
        elif start is not None and (stripped == TOC_END or DOCTOC_END_RE.match(stripped)):
            end = i
            return start, end
    return None


def insert_index_after_title(lines: Sequence[str]) -> int:
    i = 0
    if lines and FRONTMATTER_RE.match(lines[0]):
        i = 1
        while i < len(lines) and not FRONTMATTER_RE.match(lines[i]):
            i += 1
        if i < len(lines):
            i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
    while i < len(lines) and not ATX_RE.match(lines[i]):
        i += 1
    if i < len(lines) and ATX_RE.match(lines[i]):
        i += 1
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "" or stripped.startswith("<!--") or stripped.startswith(">"):
            i += 1
            continue
        break
    return i


def render_toc(
    headings: Sequence[tuple[int, str]],
    *,
    min_level: int,
    max_level: int,
) -> list[str]:
    seen: dict[str, int] = {}
    slugs: list[str] = []
    for _level, text in headings:
        slugs.append(unique_slug(github_slug(text), seen))
    included = [
        (level, text, slug)
        for (level, text), slug in zip(headings, slugs, strict=True)
        if min_level <= level <= max_level
    ]
    if not included:
        return []
    base = min(level for level, _text, _slug in included)
    out: list[str] = []
    for level, text, slug in included:
        indent = "  " * (level - base)
        label = strip_inline_md(text)
        out.append(f"{indent}- [{label}](#{slug})")
    return out


def apply_toc(
    text: str,
    *,
    min_level: int,
    max_level: int,
) -> str:
    newline = "\n" if "\r\n" not in text else "\r\n"
    lines = text.splitlines()
    headings = iter_headings(lines)
    toc_items = render_toc(headings, min_level=min_level, max_level=max_level)
    block = [TOC_START, ""]
    if toc_items:
        block.extend(toc_items)
        block.append("")
    block.append(TOC_END)

    markers = find_marker_block(lines)
    if markers is None:
        idx = insert_index_after_title(lines)
        before = lines[:idx]
        after = lines[idx:]
        if before and before[-1].strip() != "":
            before.append("")
        new_lines = before + block + ([""] if after and after[0].strip() != "" else []) + after
    else:
        start, end = markers
        new_lines = lines[:start] + block + lines[end + 1 :]

    result = newline.join(new_lines)
    if text.endswith(("\n", "\r\n")):
        result += newline
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--min-level", type=int, default=2)
    parser.add_argument("--max-level", type=int, default=6)
    parser.add_argument(
        "--include-h1",
        action="store_true",
        help="Include the top-level heading (default: skip H1, like Markdown All in One)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if a file would change; do not write",
    )
    args = parser.parse_args(argv)
    min_level = 1 if args.include_h1 else args.min_level
    status = 0
    for path in args.files:
        original = path.read_text(encoding="utf-8")
        updated = apply_toc(original, min_level=min_level, max_level=args.max_level)
        if original == updated:
            print(f"unchanged {path}", file=sys.stderr)
            continue
        if args.check:
            print(f"stale {path}", file=sys.stderr)
            status = 1
            continue
        path.write_text(updated, encoding="utf-8")
        print(f"updated {path}", file=sys.stderr)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
