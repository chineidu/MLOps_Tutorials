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

## Install (existing machine with `/sync-opencode`)

1. Run `/sync-opencode` to copy this server into
   `~/.config/opencode/mcp-servers/langgraph-docs/` and merge the
   matching `mcp` block into `~/.config/opencode/opencode.jsonc`.
2. Run `/opencode-bootstrap-docs` to clone the docs mirror into
   `~/docs-mirror/langchain` (first-time only).
3. Restart opencode. `opencode mcp list` should show
   `langgraph-docs-mcp ✓ connected`.

## Refresh the mirror

Run `/opencode-refresh-docs` whenever you want updated LangGraph/LangChain
docs. It pulls from upstream without recloning:

```bash
# the command does this:
cd ~/docs-mirror/langchain
git fetch origin --depth 1
git reset --hard origin/main
```

Restart opencode after refresh so `langgraph-docs-mcp` reindexes.

(`git pull` fails on shallow mirrors when the upstream force-pushes;
the fetch + reset pattern always works.)

## Install (fresh machine)

1. Clone or pull the MLOps repo that vendors this folder.
2. Run `/sync-opencode` (deploys commands, agents, configs, MCP servers).
3. Run `/opencode-bootstrap-docs` (clones the docs mirror).
4. Restart opencode.

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

## Files

| Path | Purpose |
|---|---|
| `langgraph_docs_mcp.py` | Server source. Copied verbatim by `/sync-opencode`. |
| `README.md` | This file. Excluded from sync. |

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `DOCS_PATH is not a directory: ...` | Mirror missing - run `/opencode-bootstrap-docs`. |
| `connected` but `list_doc_sources` returns 0 files | Mirror is sparse-checked to an empty set. Re-run `/opencode-bootstrap-docs` or widen sparse-checkout manually. |
| Stale content after `git pull` | Shallow mirror + force-push. Use `git fetch origin --depth 1 && git reset --hard origin/main` instead. |
