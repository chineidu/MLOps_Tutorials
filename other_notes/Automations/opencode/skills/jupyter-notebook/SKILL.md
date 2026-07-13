---
name: jupyter-notebook
description: >
  Convert a Python script into a Jupyter notebook with jupytext and format its
  comments/notes into clean markdown cells. Use only when the user explicitly
  asks to turn a .py file into an .ipynb, to "promote comments to markdown", or
  to clean up / reformat the prose in a notebook. Not proactive — wait for an
  explicit request. Script -> notebook direction only.
compatibility: opencode
---

# Jupyter Notebook Conversion & Formatting

Use this skill when the user wants to turn a `.py` file into a `.ipynb`, or to
lift the explanatory comments in a script/notebook into proper markdown cells.
It covers the conversion step and the prose-formatting conventions that make a
notebook read well as a teaching/explainer document.

This skill is about **script -> notebook** conversion only. It does not cover
notebook -> script export or jupytext pairing/syncing.

## 1. Prerequisites

Check that the tooling is available before running anything:

```bash
uv run jupytext --version
```

If `jupytext` (and `nbformat`) are not installed, add them as dev dependencies:

```bash
uv add --dev jupytext nbformat nb-black-formatter
```

`nbformat` is needed for the validation step in section 5; `nb-black-formatter`
is the notebook-aware code formatter if the user also wants the code cells
auto-formatted (`uv run jupyter nbconvert --to notebook --inplace --stdout` with
the nb-black extension, or `uv run jupyter labextension` setup as the project
prefers).

## 2. Convert the script to a notebook

The default conversion uses jupytext's `notebook` format:

```bash
uv run jupytext --to notebook notebooks/module_name.py
```

This produces `notebooks/module_name.ipynb` alongside the script. To control
the destination explicitly:

```bash
uv run jupytext --to notebook --output notebooks/module_name.ipynb notebooks/module_name.py
```

### Percent-format markers

If the source script already uses jupytext percent markers, they are honored
automatically:

- `# %%` starts a new code cell.
- `# %% [markdown]` starts a new markdown cell (the following indented block
  becomes markdown prose, not code).

When the script has no markers, jupytext treats the whole file as a single code
cell. In that case, do the comment-to-markdown lifting described in section 3
after conversion so the notebook is not one giant cell.

## 3. Promote comments / notes to markdown

After conversion (or on an already-existing notebook), turn explanatory
comments into real markdown cells. The goal is a notebook that reads like a
document, with prose explaining each step and code doing the work.

### Module docstring -> title cell

If the script opens with a module-level docstring (`"""..."""`), convert it into
a top-of-notebook markdown cell.

- Use `# Title` when the docstring reads like a report/overview title.
- Use `## Section` when it reads like a section intro.
- Pick the level dynamically from the docstring's own structure (first line is a
  short phrase -> title; multi-line overview -> `##` intro).
- Render reST conventions as markdown: `::` code blocks become fenced
  ```...``` blocks, and double backticks `` `name` `` stay as inline code.

### Section banner comments -> `###` heading cells

A comment block of this shape is a section header:

```python
# ---------------------------------------------------------------------------
# 1. Load the raw orders
# ---------------------------------------------------------------------------
# One row per order. The target column ``High_Value_Order`` ("Yes"/"No") is
# separated out; we only engineer features from placement-time signals.
```

Convert it into a markdown cell placed immediately before the code it
describes:

```markdown
### 1. Load the raw orders

- One row per order. The target column `High_Value_Order` ("Yes"/"No") is
- separated out; we only engineer features from placement-time signals.
```

Rules:

- The banner separator lines (`# ----`) are dropped.
- The title line (`# N. ...`) becomes `### N. ...`.
- Each remaining comment line becomes a bullet: strip the leading `# ` and
  prefix `- `. Preserve the original indentation of nested bullets (e.g.
  `#   * item` -> `-   * item`).
- Use `###` for section banners. Promote to `##` or `#` only if the script's
  own heading hierarchy clearly calls for it (e.g. a "Part 1" wrapper around
  several `###` sections).
- Convert the whole leading comment block of a cell at once; do not split a
  section header across multiple markdown cells.

### Inline code annotations -> leave in place

Comments that sit directly above the single line they explain are part of the
code's teaching value. Leave them as `#` comments inside the code cell:

```python
# Saturday / Sunday
pl.col("Day_Of_Week").is_in(list(WEEKEND_DAYS)).cast(pl.Int64).alias("Is_Weekend"),
```

Only lift these to markdown when the user explicitly asks for "all comments"
converted, and acknowledge that doing so fragments the code.

### Markdown style

- No reStructuredText: write fenced code blocks (```), not `::` blocks.
- Use backticks for inline code, column names, and identifiers.
- One concept per cell; avoid giant run-on cells.
- Keep prose tight and skimmable; bullets over walls of text.

## 4. Notebook portability

Scripts often assume they are run as files. Notebooks do not define `__file__`,
so fix path logic during/after conversion:

- Replace `Path(__file__).resolve().parent` with a project-root anchor such as
  `Path.cwd()` (when run from the repo root) or an explicit configured root.
- Prefer running notebook steps via `uv run jupyter ...` so the managed
  environment is used.
- Confirm any data paths referenced by the script actually resolve from the
  notebook's execution context.

## 5. Notebook hygiene (recommended)

These steps are recommended good practice, not enforced automatically. Apply
them unless the user wants outputs/state preserved:

- Clear outputs and execution counts before committing:
  ```bash
  uv run jupyter nbconvert --clear-output --inplace notebooks/module_name.ipynb
  ```
- Remove empty or dead cells.
- Ensure every cell has a unique `id` (jupytext/nbformat normally assign these;
  regenerate if a manual edit collapsed them).
- Validate the notebook is well-formed:
  ```bash
  uv run python -m nbformat.validate notebooks/module_name.ipynb
  ```
- Optional execution check (only if the notebook is meant to run cleanly):
  ```bash
  uv run jupyter nbconvert --to notebook --execute --inplace notebooks/module_name.ipynb
  ```

## 6. Workflow summary

1. Confirm `jupytext`/`nbformat` are available (install with `uv add --dev` if not).
2. Convert: `uv run jupytext --to notebook <script>.py`.
3. Lift the module docstring to a title/intro markdown cell.
4. Lift each section banner comment block to a `###` markdown cell; keep inline
   code annotations in the code cells.
5. Fix `__file__` / path assumptions for notebook execution.
6. (Recommended) Clear outputs, ensure unique cell ids, and run
   `nbformat.validate`.
7. Show the user the resulting notebook (or a diff of the markdown cells) before
   considering the task done.
