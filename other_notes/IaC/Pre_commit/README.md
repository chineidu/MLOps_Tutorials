# Pre-Commit Hooks

- [Official Docs](https://pre-commit.com/)
- This contains pre-commit configurations

## Table of Content

- [Pre-Commit Hooks](#pre-commit-hooks)
  - [Table of Content](#table-of-content)
  - [Setup](#setup)
    - [1. Installation](#1-installation)
    - [2. Add a Pre-Commit Configuration](#2-add-a-pre-commit-configuration)
    - [3. Install The Git Hook Scripts](#3-install-the-git-hook-scripts)
    - [4. (Optional) Run Against All The Files](#4-optional-run-against-all-the-files)
  - [Version 1](#version-1)
  - [Version 1.1](#version-11)

## Setup

### 1. Installation

```sh
pip install pre-commit

# Check version
pre-commit --version
```

### 2. Add a Pre-Commit Configuration

- Create a file named `.pre-commit-config.yaml`

### 3. Install The Git Hook Scripts

```sh
pre-commit install
```

### 4. (Optional) Run Against All The Files

```sh
pre-commit run --all-files
```

## Version 1

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.2.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ["--maxkb=2000"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.1.1
    hooks:
      - id: mypy
        name: mypy
        entry: mypy
        language: python
        "types_or": [python, pyi]
        exclude: ^tests/
        args:
          [
            "--ignore-missing-imports",
            "--disallow-any-generics",
            "--config-file",
            "./pyproject.toml",
          ]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.1.4
    hooks:
      # Run the linter.
      - id: ruff
        args: [--fix]
      # Run the formatter.
      - id: ruff-format

```

## Version 1.1

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-docstring-first
        args: ["--maxkb=2000"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.3.4
    hooks:
      # Run the linter.
      - id: ruff
        args: [--fix]
      # Run the formatter.
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        name: mypy
        entry: mypy
        language: python
        "types_or": [python, pyi]
        exclude: ^tests/
        args:
          [
            "--ignore-missing-imports",
            "--disallow-any-generics",
            "--config-file",
            "./pyproject.toml",
          ]
```
