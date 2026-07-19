---
description: Stage all changes and create a commit with a generated message.
agent: build
---

Stage everything and commit using the `git-commit` skill conventions.

If the user passed arguments after `/commit` (e.g. `/commit fix the login bug`), treat them as extra context for the commit message — incorporate them, but still derive the message from the actual diff.

Process:

1. Run `git status` to see the working tree state.
2. Run `git add -A` to stage all changes (new, modified, and deleted files). Do NOT skip this even if something is already staged — the user wants everything in this commit.
3. Run `git diff --staged --stat` and `git diff --staged` to inspect what's being committed. If nothing is staged after step 2, stop and tell the user there are no changes to commit.
4. Load the `git-commit` skill and follow its rules to produce the commit message (type tag, ≤60 char subject, 1–6 bullets, no trailing periods, no fences).
5. Show the proposed message to the user, then run `git commit -m "<message>"` using a single `-m` with embedded newlines (or multiple `-m` flags if your shell prefers that). Do NOT push.
6. Print the commit hash and a one-line summary of what was committed.

Do not amend, do not force-push, do not skip hooks. If a pre-commit hook fails, report the failure and stop — do not retry with `--no-verify`.
