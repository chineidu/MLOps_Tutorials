---
description: Read-only drift report for global opencode config vs repo mirror; `push [paths]` adopts global changes into the repo.
agent: build
---

Compare the global opencode configuration against the repository mirror and report what has drifted.

The repository mirror (`REPO_MIRROR`) is the **canonical source of truth**. The global configuration (`GLOBAL_CONFIG`) is the machine-specific installation. Any edit should start in the repo and be pushed out via `/sync-opencode`.

This command is **read-only by default**. It detects drift and never modifies either side. The `push` argument (see **Arguments**) is the sanctioned exception: it adopts global-side changes into `REPO_MIRROR` when the global files were edited directly.

---

# Arguments

Raw arguments: `$ARGUMENTS` (empty when the command was invoked bare).

| Arguments | Mode |
|-----------|------|
| (empty) | **Report mode** - read-only drift report. The default. |
| `push` | **Push mode** - render the report, then adopt global changes into `REPO_MIRROR` (see **Push mode**) |
| `push <path> ...` | **Scoped push mode** - push mode restricted to the named paths |
| `help` | Print the usage block below and stop. No report, no writes. |

`push` and `--push` are equivalent. Paths match the File column of the report (for example `AGENTS.md`, `agents/brainstorm.md`, `skills/critique/`).

Usage (print this block for `help` and for any invalid argument):

```text
/check-opencode-drift                  read-only drift report
/check-opencode-drift push             adopt global changes into the repo
/check-opencode-drift push <path>...   adopt only the named paths
```

Any other argument is an error: print the usage block and stop without modifying anything.

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

Interpretation guidance (report mode):

- `GLOBAL_ONLY` items were likely added directly to global. To adopt them into the repo, run `/check-opencode-drift push`, then commit in the repo. After that, the repo is canonical again.
- `REPO_ONLY` items exist in the repo but not globally. If they should be deployed, run `/sync-opencode`. If they are stale, remove them from the repo. Push mode never touches them.
- `DIFFER` items mean both sides were edited independently. Treat this as a conflict: examine both versions before acting. `/check-opencode-drift push` resolves it by overwriting the repo copy with the global one, so push only after confirming the global version is the one to keep.

In report mode, never suggest resolving conflicts automatically. Push mode is not automatic resolution: it runs only on explicit user request, behind a confirmation step.

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

In report mode, when the report contains `GLOBAL_ONLY` or `DIFFER` items, end with exactly this line:

```text
To adopt these into the repo: /check-opencode-drift push  (optionally add paths to scope)
```

Skip this line in push mode (the report there is a preview) and when there is nothing to push.

---

# Push mode

Runs only when the user passes `push`. Push mode adopts global-side changes into the repository mirror, for the workflow where global files were edited directly (live edits to agents, AGENTS.md, commands, skills) and the repo needs to catch up.

Direction:

```text
GLOBAL_CONFIG → REPO_MIRROR
```

## Rules

1. **Report first.** Always render the full report before touching anything. The report is the preview: it is the complete set of files push mode may act on.
2. **Confirm once.** Present the plan (files to add, files to overwrite, the scoped set if applicable) and ask for confirmation before writing. Abort on refusal. One confirmation covers the whole run; do not ask per file.
3. **Copy bytes exactly.** Use `cp`. Never retype, regenerate, normalize, or "improve" contents. Create parent directories where needed.
4. **Act on:**
   - `GLOBAL_ONLY`: copy from `GLOBAL_CONFIG` to the matching `REPO_MIRROR` path
   - `DIFFER`: overwrite the `REPO_MIRROR` copy with the global file
   - `IDENTICAL`: nothing to do
   - `REPO_ONLY`: never delete, never overwrite; report as untouched
5. **Never pushed, even when named explicitly:**
   - `configs/opencode.jsonc` and `configs/config.json`. The global copies contain machine-specific values (local MCP servers, absolute paths, OS-dependent settings) that must not leak into the canonical repo. If the user asks for them, show a key-level diff of the differing top-level keys and let them update the repo copy manually.
   - Anything on the Exclusions list.
6. **Scoped push.** With named paths, narrow only the copy step to those paths (matched against the report's File column). The report itself still covers everything.
7. **Nothing to push.** If no `GLOBAL_ONLY` or `DIFFER` item remains in scope, say so and stop. No confirmation, no writes.

## After pushing

- Re-classify every pushed path. Expected: all `IDENTICAL`.
- Remind the user that `REPO_MIRROR` now has uncommitted changes, and offer to commit following the repo's existing commit style (check `git log`). Commit only with explicit confirmation.
- Do not run `/sync-opencode` automatically; global and repo now agree on the pushed paths.

---

# Validation

After the report, check:

- No mapped file was excluded from the scan
- File counts match actual filesystem contents in both locations
- `REPO_MIRROR/configs/opencode.jsonc` parses successfully as JSONC (report if not; this is a repo-side problem)
- In push mode: every pushed path re-classifies as `IDENTICAL`, no `REPO_ONLY` item was deleted, and the only modifications were to mapped paths in `REPO_MIRROR`

Report any validation failures at the bottom.
