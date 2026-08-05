---
description: Sync the global opencode config from the repo mirror. One-way, adds missing/updated files, skips docs/python-skills/customize-opencode, merges opencode.jsonc mcp.
agent: build
---

Sync the global opencode configuration from the documentation repo mirror. The repo is the SOURCE OF TRUTH (it mirrors the intended setup for reuse across machines); the global config is the DESTINATION.

## Paths

```
SOURCE: /Users/mac/Desktop/Projects/MLOps_Tutorials/other_notes/Automations/opencode
DEST:   ~/.config/opencode
```

## Directory mapping (mirror subdir -> global subdir)

- `SOURCE/agents/*.md`            -> `DEST/agents/`
- `SOURCE/command/*.md`           -> `DEST/command/`
- `SOURCE/skills/<name>/SKILL.md` -> `DEST/skills/<name>/SKILL.md`
- `SOURCE/configs/config.json`    -> `DEST/config.json`
- `SOURCE/configs/opencode.jsonc` -> `DEST/opencode.jsonc`
- `SOURCE/AGENTS.md`              -> `DEST/AGENTS.md`

## Exclusions — never copy these

1. `SOURCE/docs/` (reference docs, not configs)
2. `SOURCE/README.md` (documentation)
3. `SOURCE/shift-enter-newline.md` (documentation)
4. `SOURCE/skills/python-skills/` (redundant with AGENTS.md)
5. `SOURCE/skills/customize-opencode/` (native/built-in opencode skill)
6. Any `node_modules`, `package.json`, `package-lock.json`, `tui.json`, or `.git` files

## Rules

1. DIRECTION IS ONE-WAY (SOURCE -> DEST). Do not modify the repo. Do not delete or rename anything already in DEST that is not in SOURCE (DEST may have extra files; leave them alone).
2. For plain markdown configs (`agents/`, `command/`, `skills/`, `AGENTS.md`, `config.json`): if SOURCE and DEST differ, overwrite DEST with SOURCE (SOURCE is newer/canonical). Report each overwrite.
3. For `opencode.jsonc`, MERGE — do not blindly overwrite:
   a. Add any top-level keys present in SOURCE but missing in DEST (e.g. `instructions`, `lsp`, `permission`).
   b. For the `mcp` block: preserve DEST's existing entries verbatim. DEST's `polars` uses the portable `uvx` invocation — keep it. Do NOT copy SOURCE's hardcoded machine-specific path (`/Users/neidu/.local/bin/polars-mcp`) or any other absolute path that does not exist on this machine.
   c. Do not remove any key that only exists in DEST.
4. Do not invent content. Copy bytes exactly. Use `cp`, not re-typing.
5. Never modify SOURCE. Never touch `DEST/tui.json` or any non-listed file.

## Steps

1. `find` SOURCE and DEST to enumerate files; skip the exclusions.
2. For each mapped file, compare with `diff -q` and classify: MISSING (in DEST only), DIFFERS, or same.
3. Copy MISSING and DIFFERS files (per Rules 2–3). Use exact byte copies.
4. After copying, re-run `diff -q` for every mapped file and confirm MISSING=0 and DIFFERS=0 (except `opencode.jsonc` mcp, which may legitimately differ in the preserved mcp block).
5. Validate `opencode.jsonc` parses (jsonc allows comments; use a tolerant parser or strip comments) and that no copied file references paths that do not exist on this machine (e.g. check `/Users/neidu/...` is absent from the final DEST configs).
6. Report a table: file | status (added/updated/skipped) | reason.

## Report format

```
Added: <list>
Updated: <list>
Skipped: <list with reasons>
Verified: <diff results + json validity>
```
