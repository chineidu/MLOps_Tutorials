# Pre-Commit Hooks

- [Official Docs](https://pre-commit.com/)
- This contains pre-commit configurations

## Table of Content
<!-- TOC -->

- [Pre-Commit Hooks](#pre-commit-hooks)
  - [Table of Content](#table-of-content)
  - [Pre-Commit Setup](#pre-commit-setup)
    - [Installation Pre-Commit](#installation-pre-commit)
    - [Add a Pre-Commit Configuration Pre-Commit](#add-a-pre-commit-configuration-pre-commit)
    - [Install The Git Hook Scripts Pre-Commit](#install-the-git-hook-scripts-pre-commit)
    - [Optional Run Against All The Files Pre-Commit](#optional-run-against-all-the-files-pre-commit)
    - [Update Pre-commit hooks Pre-Commit](#update-pre-commit-hooks-pre-commit)
  - [Prek Setup](#prek-setup)
    - [Installation](#installation)
    - [Add a Pre-Commit Configuration](#add-a-pre-commit-configuration)
    - [Install The Git Hook Scripts](#install-the-git-hook-scripts)
    - [Optional Run Against All The Files](#optional-run-against-all-the-files)
    - [Update all hooks](#update-all-hooks)
    - [List all available hooks](#list-all-available-hooks)
    - [Clean unused cached repositories](#clean-unused-cached-repositories)
  - [Configs](#configs)
    - [Version 1](#version-1)
    - [Version 1.1](#version-11)

<!-- /TOC -->

## Pre-Commit Setup

### Installation (Pre-Commit)

```sh
pip install pre-commit

# Check version
pre-commit --version
```

### Add a Pre-Commit Configuration (Pre-Commit)

- Create a file named `.pre-commit-config.yaml`

### Install The Git Hook Scripts (Pre-Commit)

```sh
pre-commit install
```

### (Optional) Run Against All The Files (Pre-Commit)

```sh
pre-commit run --all-files
```

### Update Pre-commit hooks (Pre-Commit)

```sh
pre-commit autoupdate
```

## Prek Setup

- [Official Docs](https://prek.j178.dev/)

### Installation

```sh
# Using uv (recommended)
uv tool install prek
```

### Add a Pre-Commit Configuration

- Create a file named `.pre-commit-config.yaml` or `.pre-commit-config.yml`

### Install The Git Hook Scripts

```sh
prek install
```

### (Optional) Run Against All The Files

```sh
prek run --all-files
```

### Update all hooks

```sh
prek auto-update
```

### List all available hooks

```sh
prek list
```

### Clean unused cached repositories

```sh
prek gc
```

## Configs

### Version 1

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

### Version 1.1

```yaml
---
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-added-large-files
        args:
          - --maxkb=5000 # Allow files up to 5MB
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-docstring-first

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff-check
        args:
          - --fix
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        name: mypy
        entry: mypy
        language: python
        types_or:
          - python
          - pyi
        exclude: ^tests/
        args:
          - --ignore-missing-imports
          - --disallow-any-generics
          - --config-file
          - ./pyproject.toml

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks

```
