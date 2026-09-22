# langgraph-docs-mcp

Offline LangGraph / LangChain / LangSmith docs MCP server.

Reads `.md` and `.mdx` files from a local Git mirror of the
[langchain-ai/docs](https://github.com/langchain-ai/docs) repository and
exposes three tools over stdio:

| Tool | Purpose |
|---|---|
| `list_doc_sources` | Return the corpus location, label, and file count |
| `search_docs` | Rank files by a query over title and body terms |
| `get_doc` | Return the body of a single file by relative path |

No outbound network required at runtime. The corpus is read from disk.

---

## Prerequisites

| Requirement | Why | How to install |
|---|---|---|
| `uv` 0.4+ on `PATH` | Spawns the server via `uv run --isolated --with fastmcp` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `git` | Clones and refreshes the docs mirror | Pre-installed on macOS; `brew install git` otherwise |
| Python 3.10+ | The MCP runtime requires it; `uv` will fetch one if missing | Installed automatically by `uv run` |

Verify prerequisites before first sync:

```bash
uv --version
git --version
```

If `uv --version` prints nothing, the opencode TUI may inherit a stripped
`PATH` and fail with `ENOENT posix_spawn 'uv'`. See **Troubleshooting ->
PATH issues** below.

---

## Install (fresh machine, no global config yet)

The fastest path. Assumes you have cloned the MLOps repo somewhere on disk.

1. **Install `uv` if missing:**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   This places `uv` at `~/.local/bin/uv`. Confirm with `uv --version`.

2. **Run `/sync-opencode`** from any opencode session:

   This copies the vendored server source into
   `~/.config/opencode/mcp-servers/langgraph-docs/` and merges the
   `langgraph-docs-mcp` block into `~/.config/opencode/opencode.jsonc`.

3. **Bootstrap the docs mirror (first-time only):**

   ```bash
   mkdir -p ~/docs-mirror
   git clone --depth 1 --filter=blob:none --sparse https://github.com/langchain-ai/docs.git ~/docs-mirror/langchain
   cd ~/docs-mirror/langchain
   git sparse-checkout set src/oss/python
   git fetch --depth 1 origin
   git reset --hard origin/main
   ```

   This sparse-clones `~/docs-mirror/langchain` (Python and LangGraph sections
   only, no JavaScript, no LangSmith). Skip if the directory already exists.

4. **Restart opencode**.

5. **Verify:**

   ```text
   opencode mcp list
   ```

   `langgraph-docs-mcp` should show `✓ connected`. If it shows `failed`,
   jump to **Troubleshooting**.

6. **Smoke test from the command line (optional but recommended):**

   ```bash
   DOCS_PATH=~/docs-mirror/langchain \
     uv run --isolated --with fastmcp python client.py list_doc_sources '{}'
   ```

   Should print `LangChain`, a `file://` URL, and the first 50 indexed
   files. `client.py` is a vendored fastmcp client that mirrors this
   README's opencode config.

---

## Install (existing machine with `/sync-opencode` already wired)

If `/sync-opencode` is already in your `~/.config/opencode/command/`:

1. `/sync-opencode` - updates the server source and config block.
2. Ensure `~/docs-mirror/langchain` exists; bootstrap it with the sparse-clone commands above if missing.
3. Restart opencode.

---

## Daily use

Once installed, the server is silent. Just ask LangGraph / LangChain
questions in any opencode session; the model will call
`list_doc_sources`, `search_docs`, or `get_doc` automatically.

---

## Refresh the mirror

To update the LangGraph / LangChain docs without recloning, run:

```bash
cd ~/docs-mirror/langchain
git fetch origin --depth 1
git reset --hard origin/main
```

Restart opencode after refresh so `langgraph-docs-mcp` reindexes.

(`git pull` fails on shallow mirrors when the upstream force-pushes;
the fetch + reset pattern always works.)

Optional disk reclaim after several refreshes:

```bash
cd ~/docs-mirror/langchain
git reflog expire --expire=now --all
git gc --prune=now
```

---

## Configuration

The vendored `configs/opencode.jsonc` registers the server with no
`DOCS_PATH` set in `environment`, so the server falls back to its built-in
default of `~/docs-mirror/langchain`. To point at a different mirror:

```jsonc
"langgraph-docs-mcp": {
  ...
  "environment": {
    "DOCS_PATH": "~/docs-mirror/fastapi"
  },
  ...
}
```

`DOCS_PATH` accepts any directory containing `.md` / `.mdx` files - it
does not have to be the LangChain docs repo. The corpus label reported to
clients is derived from the directory basename (e.g. `langchain` ->
`LangChain`, `fastapi` -> `FastAPI`).

---

## Files

| Path | Purpose |
|---|---|
| `langgraph_docs_mcp.py` | Server source. Copied verbatim by `/sync-opencode`. |
| `client.py` | FastMCP test client mirroring this README's opencode config. |
| `README.md` | This file. Excluded from sync. |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `failed: MCP error -32000: Connection closed` | `~/docs-mirror/langchain` missing | Bootstrap the mirror with the sparse-clone commands in Install step 3. |
| `failed: ENOENT posix_spawn 'uv'` | `uv` not on PATH inside opencode TUI | See **PATH issues** below. |
| `failed: DOCS_PATH is not a directory: ...` | Mirror path wrong | Set `environment.DOCS_PATH` or fix the symlink. |
| `connected` but `list_doc_sources` returns 0 files | Sparse-checkout misconfigured | `cd ~/docs-mirror/langchain && git sparse-checkout set src/oss/python` |
| Stale content after `git pull` | Shallow mirror + force-push | `git fetch origin --depth 1 && git reset --hard origin/main` |
| Server shows old content after refresh | opencode did not restart | Restart opencode so the server reindexes from disk. |

### PATH issues

The opencode TUI on macOS inherits a minimal `PATH`
(`/usr/bin:/bin:/usr/sbin:/sbin`) and ignores shell `PATH` modifications
from `~/.zshrc` / `~/.bashrc`. This is a known opencode bug; see
[anomalyco/opencode#26356](https://github.com/anomalyco/opencode/issues/26356).

Workaround: add an explicit `environment.PATH` to your local
`~/.config/opencode/opencode.jsonc` that includes `~/.local/bin`:

```jsonc
"langgraph-docs-mcp": {
  "type": "local",
  "command": ["uv", "run", "--isolated", "--with", "fastmcp", "python", "langgraph_docs_mcp.py"],
  "cwd": "~/.config/opencode/mcp-servers/langgraph-docs",
  "environment": {
    "PATH": "/Users/mac/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
  },
  "timeout": 30000,
  "enabled": true
}
```

Replace `/Users/mac/.local/bin` with wherever `uv` is installed on this
machine (`which uv`). The vendored repo config does not include this
override because it bakes the user-specific `uv` path into the canonical
source - each machine adds its own `environment.PATH` after the first
sync if needed.
