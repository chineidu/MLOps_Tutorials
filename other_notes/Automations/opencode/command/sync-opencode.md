---
description: Sync the global opencode configuration from the repository mirror.
agent: build
---

Synchronize the global opencode configuration from the local repository mirror.

The repository mirror is a Git-tracked copy of my reusable opencode configuration.
It is the **canonical source of truth** that I maintain and version control.

The global configuration (`~/.config/opencode`) is the machine-specific installation.

This command performs a **one-way synchronization**:

```
REPO_MIRROR → GLOBAL_CONFIG
```

Never modify the repository mirror.
Never synchronize in the opposite direction.

The command must be **idempotent**. Running it multiple times without repository changes should produce no modifications.

---

# Paths

```text
REPO_MIRROR: /Users/mac/Desktop/Projects/MLOps_Tutorials/other_notes/Automations/opencode
GLOBAL_CONFIG: ~/.config/opencode
```

---

# Directory mapping

| Repository | Global |
|------------|--------|
| `REPO_MIRROR/agents/*.md` | `GLOBAL_CONFIG/agents/` |
| `REPO_MIRROR/command/*.md` | `GLOBAL_CONFIG/command/` |
| `REPO_MIRROR/skills/<name>/SKILL.md` | `GLOBAL_CONFIG/skills/<name>/SKILL.md` |
| `REPO_MIRROR/configs/config.json` | `GLOBAL_CONFIG/config.json` |
| `REPO_MIRROR/configs/opencode.jsonc` | `GLOBAL_CONFIG/opencode.jsonc` |
| `REPO_MIRROR/AGENTS.md` | `GLOBAL_CONFIG/AGENTS.md` |

Create parent directories if they do not already exist.

---

# Exclusions

Never copy:

- `REPO_MIRROR/docs/`
- `REPO_MIRROR/README.md`
- `REPO_MIRROR/shift-enter-newline.md`
- `REPO_MIRROR/skills/python-skills/`
- `REPO_MIRROR/skills/customize-opencode/`
- `.git`
- `node_modules`
- `package.json`
- `package-lock.json`
- `tui.json`

---

# Rules

## 1. Direction

Synchronization is strictly:

```
REPO_MIRROR → GLOBAL_CONFIG
```

Never:

- modify the repository
- delete files from `GLOBAL_CONFIG`
- rename files in `GLOBAL_CONFIG`

`GLOBAL_CONFIG` may contain additional files not present in the repository.

Leave them untouched.

---

## 2. Standard files

Applies to:

- `agents/`
- `command/`
- `skills/`
- `AGENTS.md`
- `config.json`

For every mapped file:

- If missing in `GLOBAL_CONFIG`, copy it.
- If contents differ, overwrite `GLOBAL_CONFIG` with an exact byte-for-byte copy.
- If identical, do nothing.

Do not recreate or rewrite file contents manually.

Use filesystem copy operations (`cp`) rather than retyping or regenerating files.

---

## 3. opencode.jsonc

Do **not** overwrite.

Merge instead.

`opencode.jsonc` contains machine-specific configuration (for example local MCP servers, portable executable paths, providers, and OS-dependent settings). Preserve those while importing reusable defaults.

### Top-level keys

For every top-level key:

- if it exists in the repository but not globally, add it
- if it already exists globally, preserve the global value
- never remove keys that exist only globally

Examples include:

- `instructions`
- `permission`
- `lsp`

### MCP

For each MCP server:

- preserve every existing server in `GLOBAL_CONFIG` unchanged
- add servers that exist only in the repository
- never replace an existing global server definition
- never remove existing global servers

Specifically:

- preserve the portable `uvx`-based `polars` configuration already in `GLOBAL_CONFIG`
- never copy machine-specific absolute paths from the repository (for example `/Users/neidu/...`)
- reject any copied configuration containing absolute paths that do not exist on this machine

---

## 4. Copy policy

Copy bytes exactly.

Do not:

- normalize formatting
- regenerate files
- reorder content
- "improve" configuration

The repository contents are authoritative.

---

## 5. Never touch

Do not modify:

- the repository mirror
- `GLOBAL_CONFIG/tui.json`
- any file outside the mappings above

---

# Procedure

1. Enumerate every mapped file while honoring the exclusions.

2. Classify each mapped file as one of:

- Missing in `GLOBAL_CONFIG`
- Different
- Identical

3. Synchronize according to the rules above.

4. Verify synchronization.

Re-check every mapped file.

Expected result:

- Missing = 0
- Different = 0

`opencode.jsonc` may legitimately differ where global machine-specific values are intentionally preserved.

5. Validate:

- `opencode.jsonc` parses successfully as JSONC.
- No copied configuration references nonexistent machine-specific paths (for example `/Users/neidu/...`).

Abort and report any validation failure.

---

# Report

Produce a summary table.

| File | Action | Reason |
|------|--------|--------|
| ... | Added / Updated / Skipped | ... |

Then report:

```text
Added:
...

Updated:
...

Skipped:
...

Verification

✓ Repository unchanged
✓ All mapped files synchronized
✓ JSONC valid
✓ No foreign machine-specific paths detected
✓ Synchronization complete
```