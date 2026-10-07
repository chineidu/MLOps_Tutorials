# fastmcp-docs-mcp

Local stdio MCP server that proxies the official FastMCP documentation MCP
at https://gofastmcp.com/mcp, with a small in-memory TTL cache so repeated
page reads do not re-hit upstream.

Unlike the other MCP servers in this repo, the source is NOT vendored
here. It lives in the MLOps_Tutorials repository at
`src/fastmcp_docs_server.py` and is installed per machine as a uv tool.
`/sync-opencode` deploys the config block only - the `fastmcp-docs-mcp`
binary must be installed manually on each machine.

Tools exposed over stdio:

| Tool | Purpose |
|---|---|
| `search_docs` | Search the FastMCP documentation by free-text query |
| `query_docs_filesystem` | Run read-only shell-like commands (ls, cat) against the docs filesystem |

Plus two resources: `fastmcp://pages` (page index) and
`fastmcp://page/{path*}` (page contents).

Requires outbound network access to `gofastmcp.com` at runtime (unlike the
offline docs servers).

---

## Prerequisites

| Requirement | Why | How to install |
|---|---|---|
| `uv` on `PATH` | Installs and runs the tool | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| MLOps_Tutorials checkout | `uv tool install` builds the tool from this source | `git clone <MLOps_Tutorials remote>` |
| Network access to gofastmcp.com | The server proxies the upstream docs MCP | - |

---

## Install (new machine)

1. **Install the tool from the MLOps_Tutorials checkout:**

   ```bash
   cd /path/to/MLOps_Tutorials
   uv tool install .
   ```

   This creates `~/.local/bin/fastmcp-docs-mcp` and a uv tool
   environment named `mlops-tutorials`. The install includes the repo's
   full dependency set and snapshots it - see **Updating** below.

2. **Run `/sync-opencode`** from any opencode session.

   This adds the `fastmcp-docs` block to
   `~/.config/opencode/opencode.jsonc` on machines that do not have it.

3. **Restart opencode.**

4. **Verify:**

   ```bash
   uv tool list          # shows mlops-tutorials and fastmcp-docs-mcp
   ```

   ```text
   opencode mcp list
   ```

   `fastmcp-docs` should show `✓ connected`.

---

## Updating

`uv tool install` snapshots the source and dependencies at install time.
After pulling changes to `src/fastmcp_docs_server.py` or `pyproject.toml`,
reinstall on each machine:

```bash
cd /path/to/MLOps_Tutorials
uv tool install --force .
```

Then restart opencode.

---

## Configuration

The entry in `configs/opencode.jsonc` (merged into each machine's global
config by `/sync-opencode`):

```jsonc
"fastmcp-docs": {
  "type": "local",
  "command": ["fastmcp-docs-mcp"],
  "disabled": false
},
```

No `cwd`, no `environment`. The command must be resolvable on the PATH
that opencode passes to MCP servers:

- Launched from a terminal: `~/.local/bin` is normally present; no
  override needed.
- Launched from the Dock / GUI: opencode may inherit a stripped PATH. Add
  an explicit `environment.PATH` that includes `~/.local/bin` (same
  workaround as `langgraph-docs-mcp`; see its README, Troubleshooting ->
  PATH issues).

---

## Files

| Path | Purpose |
|---|---|
| `README.md` | This file. Excluded from `/sync-opencode`. |

The server source is not stored in this repo - see
`MLOps_Tutorials/src/fastmcp_docs_server.py`.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `fastmcp-docs` not listed on a machine at all | Config block was never synced to that machine | Run `/sync-opencode`, restart opencode |
| `failed: ENOENT posix_spawn 'fastmcp-docs-mcp'` | Tool not installed, or `~/.local/bin` not on opencode's PATH | `uv tool install .` from the MLOps checkout; add `environment.PATH` if launched from the Dock |
| Tool calls fail while the server shows connected | No outbound access to `gofastmcp.com` | Check network or proxy; upstream is required at runtime |
| Behavior is stale after changing the source | `uv tool install` snapshotted the old code | `uv tool install --force .`, restart opencode |
| Upstream tool names changed | `gofastmcp.com/mcp` is owned by the FastMCP team and may rename tools | Update the upstream tool constants in `src/fastmcp_docs_server.py` and reinstall with `--force` |
