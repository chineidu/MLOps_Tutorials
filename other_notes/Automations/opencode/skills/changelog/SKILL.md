---
name: changelog
description: Add, update, or draft entries in this project's CHANGELOG.md following Keep a Changelog conventions. Use whenever the user asks to update the changelog, log a change, write release notes, bump the version, or prepare a release — and proactively after finishing a feature or bug fix if it looks release-worthy, even if the user doesn't say "changelog" explicitly.
compatibility: opencode
---

# Changelog Maintenance

This repo's `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
with a house style layered on top. Match the existing style exactly — don't default to
generic Keep a Changelog phrasing if it drifts from what's already there.

## Before writing anything

1. Check whether `CHANGELOG.md` exists yet. If it doesn't, follow **Cold start** below first,
   then continue.
2. Read the full existing `CHANGELOG.md` — not just the latest entry — to confirm the current
   top version number and absorb the tone/format of recent entries.
3. Confirm what actually changed. Use `git log` / `git diff` against the last tagged release (or
   ask the user) rather than guessing at scope. Never invent or embellish a change.
4. Decide the version bump using semver, and confirm with the user if it's ambiguous:
   - **MAJOR** — breaking change to a public API, schema, or output contract.
   - **MINOR** — new capability, field, endpoint, or model behavior, backward compatible.
   - **PATCH** — bug fix, tuning, or internal correction with no new capability.

## Cold start (no CHANGELOG.md yet)

1. Look for a version signal already in the repo before inventing one: a version file
   (`config.yaml`, `package.json`, `pyproject.toml`, a git tag, etc.). If one exists, the first
   changelog entry should match it rather than starting the numbering over.
2. If there's truly no existing version anywhere, ask the user whether to start at `v0.1.0`
   (pre-1.0, still stabilizing) or `v1.0.0` (first stable release) — don't assume.
3. Scaffold the file with a short title block, then the first version entry:

   ```
   # Changelog

   All notable changes to <Project Name> are documented here.
   Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

   ---

   ## [vX.Y.Z] - YYYY-MM-DD

   Initial release.
   ```

   Only add `### Added` / `### Fixed` / `### Changed` subsections under that first entry if
   there's something specific worth calling out (notable initial capabilities, known
   limitations). If the project is genuinely brand new with nothing yet to itemize, "Initial
   release." on its own is enough — don't manufacture bullet points just to fill space.
4. Confirm the project name and starting version with the user before writing the file, since
   both are awkward to change gracefully later.
5. From this point on, every future update follows the normal workflow below.

## Entry format

Insert new versions at the very top of the file, directly under the title/intro block and above
the previous top entry, separated by a `---` rule. Never reorder or edit past entries.

```
## [vX.Y.Z] - YYYY-MM-DD

### Added

- **Short Title** (`file_one.py`, `file_two.py`) —
  Plain-English explanation of what changed and, more importantly, why: what problem existed
  before or what capability was missing. Name specific thresholds, function names, schema
  names, or counts when they matter (e.g. "hard cap of 10", "score >= 0.85").

### Fixed

- **Short Title** (`file.py`) —
  What was broken, the concrete symptom, and what the fix does about it.

### Changed

- `config.yaml` API version bumped from `vX.Y.Z` to `vX.Y.Z+1`.
```

Section order is always **Added → Fixed → Changed**, then `Removed` / `Deprecated` / `Security`
only if the release actually has one (Keep a Changelog's fuller set — this project hasn't needed
them yet, but don't force a change into the wrong bucket just to avoid adding a section).

### Rules for individual bullets

- Bold the short title first, like a mini headline.
- Follow it with the touched files in backticks, comma-separated, in parentheses — omit the
  parenthetical entirely for process-only lines (e.g. a version bump) that don't map to specific
  files.
- Use an em dash after the title/files, then the explanation.
- Wrap prose around ~95 characters per line to match existing entries; indent continuation lines
  to align under the bullet's text, not the `-` marker.
- Explain the *why*, not just the *what*. "Filters gambling payouts" is weaker than "gambling
  winnings were inflating formal-income scores, so transactions from betting platforms are now
  excluded before scoring."
- One tight paragraph per bullet — this is a changelog, not a design doc. If an entry needs more
  than ~4 sentences, it's probably two entries.
- Use present tense for what the code now does ("filters", "reinstates") and past tense for what
  was wrong before ("was inflating", "were being cut").

## Version file sync

Whenever a release changes API-facing behavior, the version file(s) in this repo (e.g.
`config.yaml`) must be bumped in the same change, and the changelog must record it under
`### Changed` as a one-liner: `` `config.yaml` API version bumped from `vX.Y.Z` to `vX.Y.Z+1`. ``
Check the repo for the actual version file each time rather than assuming the name — projects
using this skill may call it something other than `config.yaml`.

## Workflow

1. Gather the actual set of changes (git history, diff, or ask the user directly).
2. Agree on the version bump if it isn't obvious from the change alone.
3. Draft entries in the format above, grouped correctly by Added/Fixed/Changed.
4. Insert the new version block at the top of `CHANGELOG.md`, with a `---` separator before the
   previous top entry.
5. Bump the version file(s) if applicable, and add the corresponding `### Changed` line.
6. Show the user the diff/new entries before treating the task as done — don't silently commit
   changelog wording without a chance to review it, since tone and technical accuracy both matter
   here.
