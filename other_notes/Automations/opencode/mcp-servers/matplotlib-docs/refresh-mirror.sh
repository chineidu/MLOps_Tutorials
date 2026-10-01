#!/bin/zsh
# Refresh the local matplotlib docs mirror used by matplotlib-docs-mcp.
#
# The mirror is a shallow, sparse clone of matplotlib/matplotlib. This
# script re-applies the sparse scope and the post-materialize cleanup;
# run it whenever the upstream docs need a refresh. Read-only mirror:
# fetch + reset is safe, no local commits exist.
#
# Usage:
#   ./refresh-mirror.sh              refresh an existing mirror
#   ./refresh-mirror.sh --bootstrap  clone the mirror first, then refresh
#
# Location precedence: $MATPLOTLIB_MIRROR, then $DOCS_PATH (as set in
# opencode.jsonc for the server), then ~/docs-mirror/matplotlib.
set -euo pipefail

REPO_URL="https://github.com/matplotlib/matplotlib.git"
MIRROR="${MATPLOTLIB_MIRROR:-${DOCS_PATH:-$HOME/docs-mirror/matplotlib}}"
# Expand a leading ~ so env values like ~/docs-mirror/matplotlib work.
MIRROR="${MIRROR/#\~/$HOME}"

if [[ ! -d "$MIRROR/.git" ]]; then
  if [[ "${1:-}" == "--bootstrap" ]]; then
    echo "Cloning matplotlib docs mirror into $MIRROR"
    mkdir -p "$MIRROR"
    git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$MIRROR"
  else
    echo "No git mirror at $MIRROR" >&2
    echo "Run with --bootstrap to clone it, or set MATPLOTLIB_MIRROR / DOCS_PATH." >&2
    exit 1
  fi
fi

echo "Refreshing mirror at $MIRROR"
cd "$MIRROR"
git fetch origin --depth 1
git reset --hard origin/main
git sparse-checkout set doc galleries lib/matplotlib

# Indexer hygiene: strip what the offline docs corpus should never carry.
# Cone-mode sparse checkout cannot express exclusions, so cleanup is
# re-applied on every refresh.
rm -rf lib/matplotlib/tests \
       lib/matplotlib/testing \
       lib/matplotlib/sphinxext \
       lib/matplotlib/mpl-data \
       doc/_static \
       doc/_embedded_plots

echo "refresh done: $(find doc galleries lib/matplotlib -type f 2>/dev/null | wc -l | tr -d ' ') files"
