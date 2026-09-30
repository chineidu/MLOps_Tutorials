#!/usr/bin/env bash
# install.sh - idempotent installer for git shell aliases.
# Deploys scripts from <repo>/shell-aliases/bin/ to ~/.local/bin/.
#
# Update policy: diff-before-overwrite. Identical files are skipped silently.
# New files are written and made executable. Different files prompt before
# overwriting so local customizations are preserved by default.
#
# Usage:
#   bash /path/to/repo/shell-aliases/install.sh
#   bash /path/to/repo/shell-aliases/install.sh --yes   # overwrite diffs without prompting
#   bash /path/to/repo/shell-aliases/install.sh --dry-run

set -euo pipefail

# --- Resolve repo location ---------------------------------------------------

# Resolve the source bin/ directory next to this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_BIN="$SCRIPT_DIR/bin"

if [[ ! -d "$SOURCE_BIN" ]]; then
  echo "ERROR: cannot find bin/ next to this script ($SCRIPT_DIR)." >&2
  echo "The install script must live next to its bin/ directory." >&2
  exit 2
fi

# --- Parse flags -------------------------------------------------------------

ASSUME_YES=0
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --yes|-y)  ASSUME_YES=1 ;;
    --dry-run|-n) DRY_RUN=1 ;;
    --help|-h)
      sed -n '2,12p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

# --- Target ------------------------------------------------------------------

TARGET_DIR="${HOME}/.local/bin"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Creating $TARGET_DIR"
  [[ "$DRY_RUN" -eq 0 ]] && mkdir -p "$TARGET_DIR"
fi

# --- Confirm ~/.local/bin is on PATH ----------------------------------------

if [[ ":$PATH:" != *":$TARGET_DIR:"* ]]; then
  echo "WARNING: $TARGET_DIR is not on PATH. Scripts will be installed but not callable by name." >&2
  echo "Add this to your shell profile: export PATH=\"$TARGET_DIR:\$PATH\"" >&2
fi

# --- Walk every script in bin/ -----------------------------------------------

added=0
updated=0
skipped=0

shopt -s nullglob
for src in "$SOURCE_BIN"/*; do
  [[ -f "$src" ]] || continue
  name="$(basename "$src")"
  dst="$TARGET_DIR/$name"

  if [[ ! -e "$dst" ]]; then
    echo "ADD    $name"
    [[ "$DRY_RUN" -eq 0 ]] && cp "$src" "$dst" && chmod +x "$dst"
    added=$((added + 1))
    continue
  fi

  if cmp -s "$src" "$dst"; then
    skipped=$((skipped + 1))
    continue
  fi

  # Files differ - show diff and prompt unless --yes or --dry-run.
  echo "DIFF   $name"
  diff "$dst" "$src" || true

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  (dry-run: not overwriting)"
    skipped=$((skipped + 1))
  elif [[ "$ASSUME_YES" -eq 1 ]]; then
    echo "  (--yes: overwriting)"
    cp "$src" "$dst"
    chmod +x "$dst"
    updated=$((updated + 1))
  else
    printf "  Overwrite %s? [y/N] " "$dst"
    read -r ans
    case "$ans" in
      y|Y|yes|YES)
        cp "$src" "$dst"
        chmod +x "$dst"
        updated=$((updated + 1))
        ;;
      *)
        echo "  Skipped."
        skipped=$((skipped + 1))
        ;;
    esac
  fi
done

# --- Report ------------------------------------------------------------------

echo ""
echo "Summary: added=$added updated=$updated skipped=$skipped"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "(dry-run: no files were modified)"
fi

# --- Verify ------------------------------------------------------------------

fail=0
for src in "$SOURCE_BIN"/*; do
  [[ -f "$src" ]] || continue
  name="$(basename "$src")"
  dst="$TARGET_DIR/$name"
  if [[ ! -x "$dst" ]]; then
    echo "VERIFY FAIL: $dst is missing or not executable"
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "Verification failed." >&2
  exit 1
fi

echo "All scripts installed and executable."
