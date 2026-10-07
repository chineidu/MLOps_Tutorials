# polars-mcp

Polars API documentation MCP server, launched on demand with `uvx`.

There is no vendored source and no docs mirror: the server introspects the
`polars` package installed in its own uvx environment and builds its API
index from it at runtime. Four tools over stdio:

| Tool | Purpose |
|---|---|
| `polars_search_api` | Search functions, methods, and classes by keyword |
| `polars_browse` | Browse all methods in a class or namespace |
| `polars_get_docstring` | Full docs, signature, and related methods for one API element |
| `polars_get_guide` | Conceptual guides (expressions, lazy API, pandas-to-polars) |

The first launch downloads wheels from PyPI into the uv cache; later
launches normally run from cache in about a second.

---

## Prerequisites

| Requirement | Why | How to install |
|---|---|---|
| `uv` on `PATH` | `uvx` builds and launches the server | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Network access to PyPI (first run, and after any pin bump) | Downloads `polars` (about 3MB) plus the `polars-runtime-32` wheel (about 50MB) | - |

---

## Install (fresh machine)

1. **Install `uv` if missing:**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Run `/sync-opencode`** from any opencode session.

   This merges the `polars-mcp` block into
   `~/.config/opencode/opencode.jsonc`. Nothing is vendored - the server
   itself lives in the uv cache.

3. **Warm the uv cache once (recommended):**

   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"warmup","version":"0"}}}' \
     | uvx --with "polars==1.44.2" --with "mcp<1.30" polars-mcp
   ```

   The command prints a JSON handshake response and exits. The first run
   downloads the wheels and can take minutes on a slow connection; later
   runs take about a second.

   Why this step matters: opencode gives each MCP server a short startup
   window (the default catalog timeout, about 30s). A cold 50MB download
   can exceed it, and a launch that is cut off restarts the download on
   the next attempt - so the server can never bootstrap on its own. See
   **Version pinning** below.

4. **Restart opencode.**

5. **Verify:**

   ```text
   opencode mcp list
   ```

   `polars-mcp` should show `✓ connected`. Quick in-session check: ask for
   the docs of `DataFrame.filter`; the model calls `polars_get_docstring`
   and returns the signature.

---

## Daily use

Once installed the server is silent. Ask Polars API questions in any
opencode session and the model calls `polars_search_api`,
`polars_browse`, `polars_get_docstring`, or `polars_get_guide` on its own.

---

## Version pinning

`uvx` re-resolves `--with polars` on every launch. When a new polars
release appears, the next launch rebuilds the server environment and must
download the matching `polars-runtime-32` wheel (about 50MB).

If that download cannot finish inside opencode's startup window, the
server never starts, and each retry starts the download again, so it never
recovers on its own. This happened on 2026-10-07 with polars 2.0.0: every
launch failed with `failed: Request timed out` because the 2.0.0 runtime
wheel never finished downloading.

Mitigations, in order of preference:

1. **Keep the version pinned** (what `configs/opencode.jsonc` does):
   `--with "polars==1.44.2"`. Startup is deterministic; the docs cover the
   pinned version only.
2. **Warm before you switch versions.** To move to a newer polars, warm
   the new version first (see **Migrating to a new polars version**), then
   update the pin. Raising `timeout.catalog` for this server also gives a
   cold build more headroom, but warming is the deterministic fix.

To check whether a runtime wheel finished downloading:

```bash
ls ~/.cache/uv/wheels-*/pypi/polars-runtime-32/
```

A completed version has a wheel entry (for example
`1.44.2-cp310-abi3-macosx_10_12_x86_64`) next to its `.http` file. A
version with only a `.msgpack` file never finished downloading.

Keep the `mcp<1.30` pin as-is. polars-mcp 0.2.1 predates the current
`mcp` releases and is only verified against older ones; do not bump this
pin without testing that the server still starts and answers.

---

## Migrating to a new polars version

Worked example: 1.44.2 -> 2.0.0. The same steps apply to any pin bump.

**Order matters: warm first, pin second.** Bumping the pin and restarting
opencode without warming reproduces the 2026-10-07 failure described in
**Version pinning** - the launch is cut off mid-download and the server
stays failed.

1. **Warm the new version from a terminal** (outside opencode, so no
   startup window applies). Expect minutes on a slow connection; the shell
   prints nothing until the wheels finish downloading. Do not Ctrl-C.

   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"warmup","version":"0"}}}' \
     | uvx --with "polars==2.0.0" --with "mcp<1.30" polars-mcp
   ```

   If it is interrupted before printing the JSON response, nothing is
   cached - run it again.

2. **Confirm the runtime wheel finished downloading:**

   ```bash
   ls ~/.cache/uv/wheels-*/pypi/polars-runtime-32/
   ```

   You want a wheel entry and an `.http` file for the new version, not just
   a `.msgpack` file.

3. **Update the pin in both config files:**

   - `configs/opencode.jsonc` (canonical, repo)
   - `~/.config/opencode/opencode.jsonc` (this machine)

   `/sync-opencode` preserves existing server definitions, so it will not
   update the global entry for you - edit it directly.

4. **Restart opencode and verify:**

   ```text
   opencode mcp list
   ```

   Then run one Polars lookup in a session (for example, docs for
   `DataFrame.filter`) to confirm the API index builds.

5. **Caveats for 2.x:** polars-mcp 0.2.1 predates polars 2.0. The index is
   built by introspection, so if 2.x changed internals some namespaces may
   be incomplete - that is a polars-mcp limitation, not a config problem.
   If a newer polars-mcp release adds 2.x support it is picked up
   automatically the next time the environment rebuilds.

Notes:

- Prefer exact pins (`polars==X.Y.Z`). A range like `polars>=2,<3`
  reintroduces the release-day risk: every new release needs its runtime
  wheel downloaded before the server can start.
- If a cold rebuild ever lands in the startup window again, optional
  hardening is to add `"timeout": { "catalog": 180000 }` to the
  `polars-mcp` entry, but warming remains the reliable fix.

---

## Configuration

The entry in `configs/opencode.jsonc` (merged into each machine's global
config by `/sync-opencode`):

```jsonc
"polars-mcp": {
  "type": "local",
  "command": ["uvx", "--with", "polars==1.44.2", "--with", "mcp<1.30", "polars-mcp"],
  "disabled": false
},
```

No `cwd`, no `environment`, no docs mirror - the entry is self-contained.
The server documents the polars version in its own uvx environment, not
the version installed in your projects. If a project uses a different
polars, either accept the mismatch or re-pin this server to match.

---

## Files

| Path | Purpose |
|---|---|
| `README.md` | This file. Excluded from `/sync-opencode`. |

There is no server source to vendor; `uvx` fetches and caches the package
on first launch.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `failed: Request timed out` on every launch | Cold uvx build stuck downloading the `polars-runtime-32` wheel; the startup window expired and each retry restarts the download | Warm the cache once (Install step 3), or pin an already-warmed version |
| `failed` right after a polars release | Unpinned `--with polars` pulled the new release; its runtime wheel is not cached | Same as above, then keep or bump the pin |
| `failed: ENOENT posix_spawn 'uvx'` | opencode TUI inherited a stripped `PATH` | Same PATH workaround as `langgraph-docs-mcp`; see its README, Troubleshooting -> PATH issues |
| Docs describe a different polars version than your project uses | The server documents its uvx environment's polars, not the project's | Re-pin the server to the version you want documented |
| Resolution error mentioning `mcp` | `mcp<1.30` pin removed or overridden | Restore `--with "mcp<1.30"` |
