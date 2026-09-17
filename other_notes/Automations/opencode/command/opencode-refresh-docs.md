---
description: Refresh the offline LangGraph docs mirror (`fetch --depth 1` + `reset --hard origin/main`); no-op if missing.
agent: build
---

Refresh the local LangGraph docs mirror used by the
`langgraph-docs-mcp` server. Pulls new content from upstream without
recloning.

For first-time setup, use `/opencode-bootstrap-docs` instead - this
command fails fast if the mirror does not exist.

---

# Paths

```text
DOCS_MIRROR: ~/docs-mirror/langchain
REPO_URL:    https://github.com/langchain-ai/docs.git
```

---

# What it does

1. Resolve `~/docs-mirror/langchain` to an absolute path.
2. If the directory does not exist, stop with a clear "run
   `/opencode-bootstrap-docs` first" message. Do nothing.
3. If `.git` is missing, stop with a "looks like a partial clone" warning.
   Do not delete or repair.
4. If the working tree is misconfigured (no `src/oss/python` materialized),
   warn the user and offer to re-run `git sparse-checkout set src/oss/python`
   after confirmation. Do not auto-repair.
5. Otherwise: fetch + reset + optional gc.

---

# Refresh

```bash
cd ~/docs-mirror/langchain
git fetch origin --depth 1
git reset --hard origin/main
```

`git pull` fails on shallow mirrors when the upstream force-pushes
(because the local ref is no longer an ancestor of `origin/main`).
`fetch --depth 1 + reset --hard origin/main` always works.

---

# Optional: reclaim disk

Skip by default. The mirror rarely grows large because of `--filter=blob:none`
plus sparse-checkout, but offer this on demand:

```bash
cd ~/docs-mirror/langchain
git reflog expire --expire=now --all
git gc --prune=now
```

Ask the user before running. `git gc --prune=now` rewrites pack files
and can be slow on very large mirrors.

---

# Validation

After the command completes:

* `git -C ~/docs-mirror/langchain log --oneline -1` returns one line
  matching the new upstream HEAD.
* `find ~/docs-mirror/langchain -name "*.md*" | wc -l` returns a positive
  count. Compare to the previous refresh's count to spot large drops
  (which would mean upstream changed the file layout).
* `du -sh ~/docs-mirror/langchain` is within the expected size band
  (working tree under 200 MB; total under 600 MB before `git gc`).

---

# What it does not do

* Does not clone. Use `/opencode-bootstrap-docs` for that.
* Does not edit `~/.config/opencode/opencode.jsonc`.
* Does not restart opencode. After refresh, the user must restart
  opencode so `langgraph-docs-mcp` reindexes from the updated mirror.
* Does not push anywhere.

---

# Report

```text
Mirror path:    ~/docs-mirror/langchain
Previous HEAD:  <short SHA before refresh>
New HEAD:       <short SHA after refresh>
Files indexed:  <count>
Size on disk:   <du output>
Disk reclaimed: <yes / no / skipped>
```

End with:

```text
Restart opencode so langgraph-docs-mcp reindexes from the updated mirror.
```
