---
description: Review uncommitted changes with the review subagent. Read-only, no fixes.
agent: build
---

Dispatch the `review` subagent to review the uncommitted changes in this repository. This command is validate-only — do NOT build, edit, fix, or commit anything.

## Step 1 — Check for changes

Run `git status`. If there are no uncommitted changes (no staged, unstaged, or untracked files), tell the user the working tree is clean and STOP — do not dispatch a review.

## Step 2 — Dispatch the review subagent

Use the `task` tool with `subagent_type: review` and this exact prompt:

```
Review the uncommitted changes in this repository. Run git status to see what changed, then git diff HEAD to review all changes to tracked files (staged and unstaged together), reading untracked files directly from disk. Read git log --oneline -5 for context, and read the plan file if one exists (plan.md or notes/plan.md). Report gaps, scope creep, untested paths, convention violations, and edge cases. End with a verdict: ready to commit OR fix first.
```

If `$ARGUMENTS` is non-empty, append this to the prompt:

```
Focus the review on: $ARGUMENTS
```

## Step 3 — Report

Wait for the review to complete.

- **If the `task` tool fails or the review returns no verdict** (timeout, crash, tool unavailable): report the error to the user and STOP.
- **Otherwise**: present the review's report to the user verbatim.

Do NOT commit, edit files, or attempt fixes based on the findings — the user will decide what to do next.
