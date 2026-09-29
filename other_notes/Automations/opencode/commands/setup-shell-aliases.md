---
description: Install or update git shell shortcuts (~/.local/bin/gst, gp, etc.) from this repo.
agent: build
---

Install or update the git shell shortcuts (`gst`, `gp`, `gco`, ...) into `~/.local/bin/` from the canonical copies in this repo.

These scripts make oh-my-zsh's git-plugin aliases work in **non-interactive** shell contexts (notably opencode's bash tool, which runs each command in a fresh non-interactive shell that does not source `~/.zshrc`).

---

# Paths

```text
REPO_MIRROR: $OPENCODE_REPO_MIRROR (default: ${HOME}/path/to/sync-opencode-repo)
INSTALL_SCRIPT: <REPO_MIRROR>/opencode/shell-aliases/install.sh
TARGET_DIR: ~/.local/bin
```

Resolve `REPO_MIRROR` in this order: (1) `$OPENCODE_REPO_MIRROR` when set and pointing at an existing directory; (2) the default below; (3) ask the user to paste the path to their checkout. The path differs per machine.

---

# Procedure

1. Resolve `REPO_MIRROR` (env var, default, or user-pasted).

2. Verify the install script exists:
   ```bash
   test -x "$INSTALL_SCRIPT" || { echo "Not found: $INSTALL_SCRIPT"; exit 1; }
   ```

3. Run the install script. Pass `--yes` to overwrite diffs without prompting (useful for clean re-syncs from the repo), or omit to be prompted per file:
   ```bash
   bash "$INSTALL_SCRIPT"
   ```

4. Surface the script's stdout and exit code to the user. The script itself reports added / updated / skipped counts.

5. Verify by listing the deployed scripts and calling one of them (for example `gst` from the project root). If any script is missing or not executable, the installer has already reported this in step 4.

---

# Behavior of the installer

- **Identical files**: skipped silently (idempotent re-runs are no-ops).
- **New files**: written and made executable.
- **Different files**: a `diff` is shown, then the user is prompted before overwriting. Local customizations are preserved by default.
- **`--yes` flag**: overwrite diffs without prompting.
- **`--dry-run` flag**: report what would change without writing anything.

---

# Adding or removing aliases

To add a new alias:

1. Drop a new file at `<REPO>/opencode/shell-aliases/bin/<name>` with the same 2-line format:
   ```bash
   #!/usr/bin/env bash
   exec git <subcommand> "$@"
   ```
2. Run `/setup-shell-aliases` (or `bash install.sh`).
3. Commit the new file to the repo.

To remove an alias, delete it from `bin/` and commit. The installer does **not** remove existing scripts on its own - run `rm ~/.local/bin/<name>` by hand.

---

# Why this is its own command (not part of `/sync-opencode`)

`/sync-opencode` is strictly `REPO → ~/.config/opencode/` and explicitly does not touch files outside its mapping table. Shell aliases deploy to `~/.local/bin/`, which is outside that scope by design. Keeping them separate preserves the boundary and means each command can evolve independently.
