# Git

## Table of Content

- [Git](#git)
  - [Table of Content](#table-of-content)
  - [Git Rebase](#git-rebase)
    - [Benefits of Git Rebase](#benefits-of-git-rebase)
    - [Common Git Rebase Use Cases](#common-git-rebase-use-cases)
      - [1. Squashing Multiple Commits](#1-squashing-multiple-commits)
      - [2. Reordering Commits](#2-reordering-commits)
      - [3. Fixing A Commit Message](#3-fixing-a-commit-message)
      - [4. Rebase Onto Upstream Branch (Automatic)](#4-rebase-onto-upstream-branch-automatic)

## Git Rebase

- Git rebase is a powerful tool in Git version control that allows you to rewrite your commit history.
- It re-applies your commits on top of a different base commit, giving you more flexibility in managing your project's history.

### Benefits of Git Rebase

- **Cleaner Commit History**: Rebase can create a cleaner and more linear commit history, especially if you made a series of small commits that you'd like to combine.
- **Collaboration Smoothness**: When collaborating with others, a linear commit history can make it easier to track changes and merge branches.
- **Upstream Branch Alignment**: Rebase helps you keep your branch in sync with the latest changes in the upstream repository.

### Common Git Rebase Use Cases

#### 1. Squashing Multiple Commits

- Imagine you made several small commits for a feature, but you'd like to present it as a single logical unit. You can squash them into one using:

```sh
git rebase -i HEAD~4  # Rewinds 4 commits
```

- In the opened editor, replace `"pick"` with "`squash"` for the commits you want to combine.
- Finally, edit the commit message for the resulting squashed commit.

#### 2. Reordering Commits

- If you made commits in the wrong order, rebase lets you rearrange them:

```sh
git rebase -i HEAD~3  # Rewinds 3 commits
```

- In the editor, rearrange the lines with "pick" to reflect the desired commit order.

#### 3. Fixing A Commit Message

- Made a typo or want to improve a commit message?

```sh
git rebase -i HEAD~1  # Rewinds 1 commit
```

#### 4. Rebase Onto Upstream Branch (Automatic)

- This keeps your local branch in sync with the latest upstream changes without prompting for edits

```sh
git fetch origin # Fetch latest changes from remote
git rebase origin/main  # Rewinds and replays on top of "main" branch
```

- For interactive edits, run:

```sh
git fetch origin # Fetch latest changes from remote
git rebase -i origin/main  # Rewinds and replays on top of "main" branch

# Optional: Edit commits here (squash, reword, drop)
```
