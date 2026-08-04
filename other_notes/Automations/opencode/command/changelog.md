---
description: Add or update a changelog entry following Keep a Changelog conventions.
agent: build
---

Load the `changelog` skill and follow its workflow to produce or update `CHANGELOG.md`.

If the user passed arguments after `/changelog` (e.g. `/changelog added dark mode toggle`), treat them as the scope of changes for the entry.

Process:

1. Check whether `CHANGELOG.md` exists. If not, follow the skill's **Cold start** section to scaffold it before continuing.
2. Read the full `CHANGELOG.md` to confirm the current top version and absorb the existing tone/format.
3. Gather the actual set of changes — run `git log` / `git diff` against the last tagged release (or ask the user) rather than guessing. Never invent or embellish.
4. Agree on the version bump (MAJOR / MINOR / PATCH) if it isn't obvious from the change alone. Ask the user when ambiguous.
5. Draft entries using the skill's format: bold short title, file list in backticks, em dash, plain-English explanation of *why*. Group under `### Added`, `### Fixed`, `### Changed` as appropriate.
6. Insert the new version block at the top of `CHANGELOG.md`, separated from the previous entry by `---`.
7. Bump version file(s) if applicable, and record it under `### Changed`.
8. Show the user the diff/new entries. Do not treat the task as done until the user confirms — changelog tone and technical accuracy matter.
