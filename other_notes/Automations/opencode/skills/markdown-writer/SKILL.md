---
name: markdown-writer
description: >
  Write and update markdown that passes markdownlint/pymarkdown and ASCII
  typography. Use when creating or editing README.md, docs, notes, architecture
  docs, SKILL.md, table of contents, TOC, Markdown All in One, or fixing
  MD013, MD022, MD028, MD031, MD032, MD040, MD041, MD047, MD056, em dashes,
  en dashes, curly quotes, or AI-slop punctuation.
compatibility: opencode
---

# Markdown Writer

Write lint-clean markdown. Follow these rules for every new `.md` file and
every edit. Do not wait for the linter to fail.

This skill is global. Discover the project's own linters and line length;
do not assume pymarkdown is installed.

## Default stance

1. Read the target file (or a sibling `.md`) before writing. Match heading
   style, list markers, and fence languages already in use.
2. Use ASCII punctuation only (see Typography). The skill file itself must
   follow this.
3. Prefer wrapping prose over disabling MD013. A file-level pragma is a last
   resort for tables and code that cannot wrap.
4. After writing, scan the file with whatever markdown linter the project
   actually has. Do not install a linter just to satisfy this skill. Do not
   run the Python test suite solely because a markdown file changed.
5. After adding, renaming, or removing headings, refresh the table of
   contents with `scripts/update_toc.py` (see Table of contents). Do not
   hand-edit TOC entries.

## Typography (no AI-slop)

Plain ASCII everywhere, including prose inside fenced blocks.

| Instead of | Use |
|---|---|
| em dash `U+2014` | `-` with spaces (` - `) |
| en dash `U+2013` | `-` (ranges like `1-3`) |
| ellipsis `U+2026` | `...` |
| curly quotes | `"` and `'` |
| decorative bullet | `-` or `*` |

Two exceptions only (from AGENTS.md Important Constraints): the user asked
for those characters, or you are quoting/editing text that already has them.
Do not rewrite the user's content just to enforce this.

Box-drawing and arrows inside fences (`|`, `v`, `->`) are fine. Do not
"ASCII-ify" diagrams.

## Structure

### Headings (MD022, MD041)

- First line is a single top-level `#` heading (MD041). YAML frontmatter is
  allowed; then the H1 follows the closing `---`.
- Blank line before and after every ATX heading.

```markdown
## 2. Scope

### In scope (v1)

- item
```

Not:

```markdown
### In scope (v1)
- item
```

### Lists (MD032)

Blank line before the first item and after the last item of a list block.

```markdown
Difficulty categories:

- `DIRECT_LOOKUP` (38) - answer exists in a single doc page
- `MULTI_HOP` (17) - answer requires synthesising across pages
```

Continuation lines indent to the text, not the `-`:

```markdown
- **Retrieval quality** - binary recall@k, per-category breakdown + delta
  from baseline
```

### Fences (MD040, MD031)

- Every opening fence has a language. Use `text` for diagrams, `python` /
  `json` / `sql` / `yaml` / `bash` / `markdown` when that is what it is.
- Blank line before and after the fence (MD031).

````markdown
```text
LABELING (one-time)                    EVAL (every run)
```
````

A bare ` ``` ` with no language is MD040.

When showing a fence inside a fence, use a longer outer run of backticks
(four or more) so the inner ` ``` ` does not close the block.

### Blockquotes (MD028)

No blank line inside a blockquote unless the blank line itself starts with
`>`.

```markdown
> Brainstorm session date: 2026-08-02
> Status: design phase (brainstorm complete, ready for plan mode)
```

Or keep the gap as a quoted blank:

```markdown
> Brainstorm session date: 2026-08-02
>
> Status: design phase
```

### Other hygiene

- MD047: file ends with exactly one newline
- MD009 / MD010 / MD012: no trailing spaces, no tabs, no stacked blank lines
- pre-commit `trailing-whitespace` and `end-of-file-fixer` catch the last two
  if the project uses them

## Table of contents

Do not write TOC links by hand. Do not rely on the VS Code command
`Markdown All in One: Create Table of Contents` (it is editor-only).

Use the stdlib script shipped with this skill. No npm, no extra Python
packages:

```bash
python3 ~/.config/opencode/skills/markdown-writer/scripts/update_toc.py FILE.md
```

If this skill was loaded from another path, run `scripts/update_toc.py`
next to `SKILL.md`.

What it does:

- Inserts or refreshes a GitHub-flavored TOC between Markdown All in One
  markers (`<!-- TOC -->` / `<!-- /TOC -->`)
- Also refreshes existing doctoc markers
- Places a missing TOC after the H1 and any following comments/blockquotes
- Skips H1 by default (the title is already on the page)
- Ignores headings inside fenced code
- Deduplicates slugs the GitHub way (`overview`, then `overview-1`)

```markdown
# Title

<!-- TOC -->

- [1. Purpose](#1-purpose)
  - [1.1 Mental Model](#11-mental-model)
- [2. Scope](#2-scope)

<!-- /TOC -->

## 1. Purpose
```

Useful flags:

```bash
python3 .../update_toc.py --include-h1 FILE.md     # keep H1 in the TOC
python3 .../update_toc.py --min-level 2 --max-level 3 FILE.md
python3 .../update_toc.py --check FILE.md          # exit 1 if TOC is stale
```

Run it after heading edits and on new long docs. Leave short notes (one
or two headings) without a TOC unless the user asks.

## Tables (MD056)

The header row sets the column count. Every body row must have the same
number of unescaped `|` cells.

Pipes that are content, not delimiters, must be escaped or wrapped in
inline code. This is the MD056 failure mode: `|Δ|` inside a 4-column row
parses as two extra cells (Expected 4, Actual 6).

```markdown
# wrong (6 cells)
| `--threshold-absolute` | no | `0.05` | Flag if |Δ| exceeds |

# right (4 cells)
| `--threshold-absolute` | no | `0.05` | Flag if \|Δ\| exceeds |
| `--threshold-relative` | no | `5` | Flag if \|Δ%\| exceeds (percent) |
```

Also valid: put the symbol in backticks (`` `|Δ|` ``) so the inner pipes
are not delimiters. Prefer `\|` when the cell is not otherwise code.

Do not wrap table rows to satisfy line length. That breaks the table.

## Line length (MD013)

- pymarkdown default is 80. Ruff in many Python repos is 110. Check
  `pyproject.toml`, `.pymarkdown.json`, `.markdownlint.json`, or
  `.markdownlint.yaml` before wrapping.
- Wrap prose and list items at the configured limit (or 80-110 if none).
  Break on spaces, not in the middle of `code` spans.
- Do not wrap tables or fenced code.
- If tables or code still trip MD013, prefer project config:

```toml
[tool.pymarkdown.plugins.md013]
line_length = 110
code_block_line_length = 120
table_line_length = 120
```

or `.pymarkdown.json`:

```json
{
  "plugins": {
    "md013": {
      "line_length": 110,
      "code_blocks": false,
      "tables": false
    }
  }
}
```

`code_blocks: false` is honoured. `tables: false` may still need a raised
`table_line_length` depending on pymarkdownlnt version.

- File-level `<!-- pyml disable md013 -->` (after the H1) only when config
  is out of scope and wrapping tables/code would destroy them. Do not put
  this pragma on every new file.

## Discovering linters

Run what exists. Skip what does not.

```bash
# pymarkdownlnt (PyPI name) if present
uv run pymarkdownlnt scan path/to/file.md

# markdownlint-cli if present
npx --yes markdownlint-cli path/to/file.md

# project hooks (trailing space, EOF newline)
uv run prek run --files path/to/file.md
```

`uv run pymarkdown` (the 0.1.x package) is a different, stale tool. Prefer
`pymarkdownlnt` if both exist. MD056 is a markdownlint rule; pymarkdownlnt
does not implement it. If only pymarkdownlnt is available, still escape
table pipes so markdownlint and GitHub rendering stay correct.

Do not `uv add` a markdown linter unless the user asks.

## Workflow

### New file

1. Start with `# Title`, then body. Add an MD013 pragma only if the file
   will contain wide tables or code you refuse to wrap.
2. Pad headings, lists, and fences with blank lines as you write.
3. Language on every fence. Count table columns; escape inner pipes.
4. Wrap prose. Leave tables and fences alone.
5. If the file has several headings, run `update_toc.py` on it.
6. Scan with the project's markdown linter if one exists.

### Existing file

1. Scan first; fix only reported issues plus typography in the lines you
   touch. Do not reformat the whole file unless asked.
2. Order: typography in edited regions, then MD028 / MD040 / MD022 /
   MD032 / MD056, then MD013 wrap, then pragma/config if tables/code remain.
3. If headings changed, run `update_toc.py` so the TOC matches.
4. Show `git diff` for the markdown file. Do not commit unless asked.

## Checklist

- No em dash, en dash, `U+2026` ellipsis, or curly quotes in new text
- Every fence has a language; fences and headings and lists have blank
  lines around them
- Table rows match the header column count; inner `|` is `\|` or in
  backticks
- Prose wrapped; tables and code not mangled
- File ends with one newline; no trailing spaces
- TOC markers (if present) match current headings; `update_toc.py --check`
  is clean
- Markdown linter (if present) is clean for the files you changed
