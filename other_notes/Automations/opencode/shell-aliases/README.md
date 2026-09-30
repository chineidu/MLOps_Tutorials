# shell-aliases

Idempotent installer for git shell shortcuts that work in **any shell context** - including opencode's bash tool, which runs commands non-interactively and so does not source `~/.zshrc` (and therefore does not see oh-my-zsh's git-plugin aliases).

## Why this exists

oh-my-zsh defines `gst`, `gp`, `gco`, etc. as zsh aliases. They resolve in interactive zsh (Terminal.app, Claude Code's terminal, an opencode interactive terminal) but **not** in the opencode bash tool, which uses a non-interactive shell per command.

This installer deploys equivalent scripts to `~/.local/bin/`, which is on `$PATH` in every shell context. Once installed, `gst`, `gp`, etc. work everywhere.

## When to run this

- On a fresh machine, after cloning this repo and running `/sync-opencode`.
- After pulling changes that added or modified any script under `bin/`.
- Any time you want to re-sync the shell aliases from the canonical repo copy.

## How to run

### Inside opencode (preferred)

Type `/setup-shell-aliases`. The command finds this repo, runs `install.sh`, and reports what changed.

### From any shell

```bash
bash /path/to/sync-opencode-repo/shell-aliases/install.sh
```

The installer locates `bin/` relative to its own path, so no repo path is passed explicitly.

## What gets installed

| Script | Wraps |
|--------|-------|
| `gst`  | `git status` |
| `gd`   | `git diff` |
| `gds`  | `git diff --staged` |
| `gl`   | `git log --oneline --decorate -20` |
| `glg`  | `git log --graph --oneline --decorate --all` |
| `gb`   | `git branch` |
| `gba`  | `git branch -a` |
| `gco`  | `git checkout` |
| `gp`   | `git push` |
| `gpl`  | `git pull` |
| `gf`   | `git fetch` |

All scripts:

- Live at `~/.local/bin/<name>`.
- Are `chmod +x`.
- Use `exec git ... "$@"` so they replace the shell process (faster startup, signals pass through cleanly).
- Forward any arguments, so `gst -s`, `gp origin main`, etc. work.

## Update policy

`install.sh` is **idempotent** and **diff-before-overwrite**:

- Identical files: skipped silently.
- New files: written and made executable.
- Different files: a diff is shown and the user is prompted before overwriting. Local customizations are preserved by default.

## Adding a new alias

1. Drop a new file at `shell-aliases/bin/<name>` with the same 2-line format as the existing ones.
2. Run `/setup-shell-aliases`.
3. Commit the new file to the repo.

## Removing an alias

1. Delete the file under `shell-aliases/bin/`.
2. The installer does **not** remove existing scripts on its own (preserves local customizations). To remove a stale alias, `rm ~/.local/bin/<name>` by hand.
3. Commit the deletion.
