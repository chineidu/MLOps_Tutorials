---
description: Sparse-clone the LangGraph docs mirror into `~/docs-mirror/langchain`; idempotent setup, delegates refresh to `/opencode-refresh-docs`.
agent: build
---

Bootstrap (first-time only) the local LangGraph docs mirror used by the
`langgraph-docs-mcp` server. The mirror is a shallow, sparse clone of
`https://github.com/langchain-ai/docs` containing only the Python and
LangGraph sections (no JavaScript, no LangSmith).

For recurring refreshes, use `/opencode-refresh-docs` instead - this
command is for first-time setup only and is a no-op if the mirror already
exists.

---

# Paths

```text
DOCS_MIRROR: ~/docs-mirror/langchain
REPO_URL:    https://github.com/langchain-ai/docs.git
SPARSE_PATH: src/oss/python
```

The destination directory is fixed at `~/docs-mirror/langchain` so the
server's default `DOCS_PATH` (also `~/docs-mirror/langchain`) works
without per-machine configuration.

---

# Preconditions

Before doing anything, verify the prerequisites are present:

| Tool | How to check | Required because |
|---|---|---|
| `git` | `git --version` | Clones and refreshes the docs mirror |
| `uv` | `uv --version` | Spawned by opencode to run the MCP server (`uv run --isolated --with fastmcp`) |

If `git` is missing: install it (`brew install git` or `xcode-select --install`).
Do not proceed; abort with a clear error.

If `uv` is missing: stop with this exact message:

```text
uv is required but not on PATH.

Install with:
  curl -LsSf https://astral.sh/uv/install.sh | sh

This places uv at ~/.local/bin/uv. After installation, restart opencode
so the TUI inherits the updated PATH, then re-run this command.
```

Do not auto-install. Do not proceed.

If both are present, continue.

---

# What it does

1. Resolve `~/docs-mirror/langchain` to an absolute path.
2. If the directory exists, stop and tell the user to run
   `/opencode-refresh-docs` for the recurring case. Do nothing.
3. If the directory does not exist, run the initial sparse clone.

After the initial clone, this command is permanently a no-op. Future
updates go through `/opencode-refresh-docs`.

---

# Initial clone

```bash
mkdir -p ~/docs-mirror
git clone --depth 1 --filter=blob:none --sparse https://github.com/langchain-ai/docs.git ~/docs-mirror/langchain
cd ~/docs-mirror/langchain
git sparse-checkout set src/oss/python
git fetch --depth 1 origin
git reset --hard origin/main
```

`--filter=blob:none` lazy-fetches blobs; `sparse-checkout set
src/oss/python` keeps only the Python and LangGraph sections (drops JS,
LangSmith, and any future additions). Final working tree is roughly
100 MB.

---

# Refresh

This command does not refresh. Use `/opencode-refresh-docs` for that.

`/opencode-refresh-docs` runs:

```bash
cd ~/docs-mirror/langchain
git fetch origin --depth 1
git reset --hard origin/main
```

`git pull` fails on shallow mirrors when the upstream force-pushes
(because the local ref is no longer an ancestor of `origin/main`).
`fetch --depth 1 + reset --hard origin/main` always works.

---

# Idempotency rules

* If `~/docs-mirror/langchain` does not exist: run the initial clone.
* If it exists: stop, report, and recommend `/opencode-refresh-docs`.

---

# Validation

After the command completes:

* `test -d ~/docs-mirror/langchain/src/oss/python` exists.
* `find ~/docs-mirror/langchain -name "*.md*" | wc -l` returns more than
  zero. Expect several hundred for `src/oss/python` alone.
* `du -sh ~/docs-mirror/langchain` reports a reasonable size. Working
  tree under 200 MB; total repo under 600 MB before `git gc`.
* `git -C ~/docs-mirror/langchain log --oneline -1` returns one line
  (the shallow HEAD).

---

# What it does not do

* Does not edit `~/.config/opencode/opencode.jsonc`. That is the job of
  `/sync-opencode`. Run that first to deploy the vendored MCP server,
  then this command to bootstrap the docs mirror.
* Does not clone the JavaScript or LangSmith sections. If you need
  those, change `SPARSE_PATH` in this command's procedure.
* Does not push anywhere. The mirror is read-only from opencode's
  perspective.

---

# Report

```text
Preconditions:  git <version>, uv <version> OK | uv missing
Mirror path:    ~/docs-mirror/langchain
Action:         cloned | already-present | prerequisites-failed
HEAD:           <short SHA on first clone only>
Files indexed:  <count on first clone only>
Size on disk:   <du output on first clone only>
```

If the prerequisites failed (e.g. `uv` missing), end with the install
instructions from the **Preconditions** section. Do not proceed.

If the mirror already existed, end with:

```text
Nothing to do. Use /opencode-refresh-docs to pull new content.
```

If this was the initial clone, end with:

```text
Restart opencode so langgraph-docs-mcp indexes the new mirror.
```
