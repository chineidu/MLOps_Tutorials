---
description: Gather commits/diff since the last release and draft the next CHANGELOG.md entry (uses the changelog skill for format/style)
agent: build
---

Use the `changelog` skill's rules for format, section order, bullet style, version-bump
logic, and cold-start behavior. Everything below is just the raw material — don't restate
or override the skill's conventions here.

Optional hint from the caller (version, range, or scope — may be empty): $ARGUMENTS

## Context

Today: !`date +%F`

Last tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "(no tags)"`

Declared version: !`grep -m1 -E '^\s*version\s*[:=]' pyproject.toml Cargo.toml config.yaml 2>/dev/null; grep -m1 '"version"' package.json 2>/dev/null; true`

Commits since last release:
!`git log --no-merges --pretty=format:'--- %h %s%n%b' $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD`

Files touched since last release:
!`git diff --stat $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD`

Existing changelog:
@CHANGELOG.md

## What to do

1. If the hint above names a different range, tag, or version, re-derive the context
   yourself for that range instead of trusting what's injected above.
2. Read the diff for the areas you plan to describe — not just commit subjects — before
   writing any bullet: `git diff <base>..HEAD -- <path>`.
3. Apply the `changelog` skill for everything else: version bump, section order, bullet
   format, cold-start handling, version-file sync.
4. Show the drafted entry for review before treating this as done.
