---
description: Review changes, then stage and commit with a generated message.
agent: build
---

Stage all changes and run a code review before committing. Pass `--quick` or `-Q` to skip the review step.

## Step 1 — Stage everything

```
!`git add -A`
```
```
!`git status`
```

If nothing changed after staging, tell the user there are no changes to commit and stop.

## Step 2 — Quick or full?

Check `$ARGUMENTS` for `--quick` (or `-Q`).

- **If `$ARGUMENTS` contains `--quick` or `-Q`**: skip to step 5 (no review). When generating the commit message in step 5, strip both `--quick` and `-Q` from the extra context — do not let either bleed into the message.
- **Otherwise**: continue to step 3 for a full review.

## Step 3 — Review

Dispatch the review subagent first. Use the `task` tool with `subagent_type: review` and this exact prompt:

```
Review the staged changes in this repository. Run git diff --staged for the diff, git log --oneline -5 for context, and read the plan file if one exists (plan.md or notes/plan.md). Report gaps, scope creep, untested paths, convention violations, and edge cases. End with a verdict: ready to commit OR fix first.
```

Wait for the review to complete. If the `task` tool fails or the review returns no verdict (timeout, crash, tool unavailable), report the error to the user and STOP without committing.

## Step 4 — Act on findings

- **If the review verdict is "fix first"**: report the blocking items to the user verbatim, unstage the changes (`git restore --staged .`), and STOP. Do NOT commit.
- **If the review verdict is "ready to commit"**: proceed to step 5.

## Step 5 — Commit

Show the staged changes:
```
!`git diff --staged --stat`
```
```
!`git diff --staged`
```

Generate a commit message following the `git-commit` skill conventions — this exact format:

```
[type] short subject (≤60 chars, imperative, lowercase, no period)
- bullet 1
- bullet 2
...
```

- **Types:** `feat`, `fix`, `refactor`, `docs`, `chore`, `perf`
- **Subject:** max 60 chars, imperative mood, lowercase first letter, no trailing period
- **Bullets:** 1–6, one per atomic change, imperative mood, no trailing periods
- **No markdown fences** around the output

Extra context from the user (incorporate into the message, if non-empty): $ARGUMENTS

Show the proposed message to the user. Once they confirm, run `git commit -m "..."` using a single `-m` with embedded newlines (or multiple `-m` flags) with the generated message. Do NOT push. Do NOT amend. Do NOT skip hooks.

After committing, print the commit hash and a one-line summary of what was committed.
