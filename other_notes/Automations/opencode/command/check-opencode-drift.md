---
description: Detect drift between the global opencode configuration and the repository mirror.
agent: build
---

Compare the global opencode configuration against the repository mirror and report what has drifted.

The repository mirror (`REPO_MIRROR`) is the **canonical source of truth**. The global configuration (`GLOBAL_CONFIG`) is the machine-specific installation. Any edit should start in the repo and be pushed out via `/sync-opencode`.

This command is **read-only**. It detects drift but never modifies either side.

---

# Paths

```text
REPO_MIRROR: /Users/mac/Desktop/Projects/MLOps_Tutorials/other_notes/Automations/opencode
GLOBAL_CONFIG: ~/.config/opencode
```

---

# Directory mapping

| Global | Repository |
|--------|------------|
| `GLOBAL_CONFIG/agents/*.md` | `REPO_MIRROR/agents/*.md` |
| `GLOBAL_CONFIG/command/*.md` | `REPO_MIRROR/command/*.md` |
| `GLOBAL_CONFIG/skills/<name>/` (all contents) | `REPO_MIRROR/skills/<name>/` (all contents) |
| `GLOBAL_CONFIG/config.json` | `REPO_MIRROR/configs/config.json` |
| `GLOBAL_CONFIG/opencode.jsonc` | `REPO_MIRROR/configs/opencode.jsonc` |
| `GLOBAL_CONFIG/AGENTS.md` | `REPO_MIRROR/AGENTS.md` |
| `GLOBAL_CONFIG/plugins/*.ts` | `REPO_MIRROR/plugins/*.ts` |

`opencode.jsonc` lives in `REPO_MIRROR/configs/` (not repo root) because the repo root holds the mirror itself.

---

# Exclusions (skip these entirely)

- `GLOBAL_CONFIG/.gitignore`, `GLOBAL_CONFIG/node_modules/`, `GLOBAL_CONFIG/package.json`, `GLOBAL_CONFIG/package-lock.json`, `GLOBAL_CONFIG/tui.json`
- `REPO_MIRROR/docs/`, `REPO_MIRROR/README.md`, `REPO_MIRROR/shift-enter-newline.md`
- `REPO_MIRROR/skills/python-skills/`, `REPO_MIRROR/skills/customize-opencode/`
- `.git`

These are machine-specific, generated, documentation, or repo-only by design.

---

# Procedure

## 1. Enumerate

Build the list of mapped files from both sides, honoring exclusions.

For skills, include every file under `<name>/`, not just `SKILL.md` (the polars skill includes references and a `.claude-plugin/` directory).

## 2. Classify

For each mapped path, determine which side it exists on:

| Classification | Meaning |
|----------------|---------|
| `GLOBAL_ONLY` | Exists in `GLOBAL_CONFIG`, not in `REPO_MIRROR` |
| `REPO_ONLY` | Exists in `REPO_MIRROR`, not in `GLOBAL_CONFIG` |
| `DIFFER` | Exists on both sides, contents differ |
| `IDENTICAL` | Exists on both sides, byte-for-byte identical |

## 3. Report

Group results into a table with columns:

| Status | File | Detail |
|--------|------|--------|

Rules for the Detail column:

- `GLOBAL_ONLY`: file count
- `REPO_ONLY`: file count
- `DIFFER`: first meaningful difference (truncated). For JSONC, note specific top-level keys or MCP servers that differ, not raw diff.
- `IDENTICAL`: leave **Detail** blank

After the table, produce a summary section.

---

# Summary

```text
Drift detected:

GLOBAL_ONLY     N    Items in global but missing from repo
REPO_ONLY       N    Items in repo but missing from global
DIFFER          N    Items on both sides with different content
IDENTICAL       N    Items in sync

All other files excluded per mapping.
```

Interpretation guidance:

- `GLOBAL_ONLY` items were likely added directly to global. To bring them into the repo, copy each file from `GLOBAL_CONFIG` to the matching `REPO_MIRROR` path, then commit. After that, the repo is canonical again.
- `REPO_ONLY` items exist in the repo but not globally. If they should be deployed, run `/sync-opencode`. If they are stale, remove them from the repo.
- `DIFFER` items mean both sides were edited independently. This is a **conflict** — the repo is canonical by policy, but the global copy may contain intentional changes that need to be examined. Do not overwrite either side; flag for manual resolution.

Never suggest resolving conflicts automatically.

---

# Report format

```text
| Status | File | Detail |
|--------|------|--------|
| GLOBAL_ONLY | skills/critique/SKILL.md | 1 file under skills/critique/`
| REPO_ONLY | skills/python-skills/SKILL.md | 1 file under skills/python-skills/`
| DIFFER | AGENTS.md | line 98: "- **Line length:** 110 characters" vs "100 characters"
| IDENTICAL | agents/brainstorm.md | |

... (remaining identical files grouped as "[N] files")

Summary
...

Drift detected:
- GLOBAL_ONLY: [N]
- REPO_ONLY:   [N]
- DIFFER:      [N]
- IDENTICAL:   [N]
```

Collapse long lists of identical files: show the first 3 as individual rows, then `[N more] files` on a single `IDENTICAL` row.

For directories with multiple drifted files, show one row per directory with the count in Detail, not one row per file.

---

# Validation

After the report, check:

- No mapped file was excluded from the scan
- File counts match actual filesystem contents in both locations
- `REPO_MIRROR/configs/opencode.jsonc` parses successfully as JSONC (report if not; this is a repo-side problem)

Report any validation failures at the bottom.
