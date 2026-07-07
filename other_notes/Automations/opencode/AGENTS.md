# AGENTS.md

This file provides guidance for AI coding agents (Claude, Cursor, Copilot, etc.) working in this repository.

---

## Project Overview

<!-- TODO: Briefly describe what this project does and its primary purpose. -->

---

## Environment Setup

```bash
# Install dependencies (uv manages the venv automatically)
uv sync --dev

# Run any command inside the managed environment
uv run <command>
```

**Python version:** 3.14+
**Package manager:** uv + pyproject.toml

---

## Common Commands

| Task | Command |
|---|---|
| Run tests | `uv run pytest` |
| Run tests with coverage | `uv run pytest --cov=src --cov-report=term-missing` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run ty check` |
| Run all checks | `make check` (or see CI script) |

Run these before committing. All checks must pass.

---

## Repository Structure

```
.
├── src/
│   └── <package>/          # Main source code
├── tests/                  # Mirrors src/ structure
├── scripts/                # One-off utilities, not imported
├── docs/                   # Documentation
├── pyproject.toml          # Project metadata and tool config
└── AGENTS.md               # This file
```

---

## Code Style

- **Formatter:** Ruff (`ruff format`) — do not manually adjust whitespace or imports
- **Linter:** Ruff (`ruff check`) — fix all warnings before committing
- **Type checker:** ty (`uv run ty check`) — fix all errors before committing; do not use `# type: ignore` without a comment explaining why
- **Docstrings:** NumPy style for public APIs; omit for private helpers unless complex
- **Line length:** 100 characters

### Naming Conventions

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_single_leading_underscore`

---

## Testing

- **Framework:** pytest
- **Location:** `tests/` — mirror the `src/` directory structure
- **Coverage target:** 80% minimum; do not reduce existing coverage
- Write tests for every new public function or class
- Group tests in plain classes (no `unittest.TestCase`), one class per module or logical unit
- Inject dependencies via pytest fixtures, not `setUp` methods
- Use `pytest.mark.parametrize` for parameterized cases
- Use `tmp_path` fixture for temporary files; never write to the project root in tests
- Use bare `assert` (not `self.assert*`) — pytest rewrites assertions for clear diffs
- Comment sections as `# Given / # When / # Then`

```python
# Good test structure
class TestFunctionName:
    def test_<scenario>(self, some_fixture: SomeType) -> None:
        """One-line description of what this test verifies."""
        # Given
        expected = ...
        # When
        result = function_under_test(...)
        # Then
        assert result == expected
```

---

## Commit Convention

Use this format:

```
[type] Short description
- point 1
- point 2
...
- point N
```

The title line is a short summary (max 60 characters, imperative mood, lowercase first letter, no trailing period). Follow it with one bullet per atomic change — one detail per line, imperative mood, lowercase verb, no trailing period. Keep it to 1–6 bullets.

**Types:** `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`

Rules:
- Do **not** add a colon after the type — use `[feat] add ...`, never `[feat]: add ...`
- Do **not** collapse bullets into the title line with ` - detail` segments — use a real bulleted list

Examples:

```
[feat] add Alembic migrations, demo seed data, and README docs
- wire alembic/ with async env.py, script.py.mako, and initial revision
- add alembic.ini with runtime-injected DB URL placeholder
- add scripts/seed_demo_data.sql and make seed-demo target
- document migrations, seed step, and TOC in README
- comment stock calculation in transactions route
```

```
[fix] correct Mapped type for unit_price_at_time column
- change Mapped[float] to Mapped[Decimal] to match Numeric(10, 2)
```

---

## Making Changes

1. Make the smallest change that satisfies the requirement
2. Do not refactor unrelated code in the same PR
3. If adding a dependency, use `uv add <package>` (or `uv add --dev <package>` for dev-only); do not edit `pyproject.toml` by hand for deps
4. Update docstrings and inline comments when changing behavior
5. Do not commit `.env`, secrets, or generated files — check `.gitignore`

---

## Workflow Modes

### Responses
- Keep responses concise unless the user asks for more detail

### Planning Mode
- Always ask clarifying questions before proposing a plan
- Never assume design choices, libraries, or approach — confirm with the user
- Use sub-agents for research/deep-dives on unfamiliar parts of the codebase before presenting a plan
- Use sub-agents to review different aspects of the plan (e.g. test coverage, type safety, architecture fit) before presenting it to the user

### Edit Mode
- Prefer sub-agents for implementation; act as coordinator rather than implementing directly, except for trivial single-file changes
- Identify independent parts of the plan and dispatch them to sub-agents in parallel where safe to do so
- Flag any sub-agent work that touches files outside the plan's stated scope
- After each sub-agent completes, run the relevant checks from Common Commands (`uv run ruff check .`, `uv run ty check`, `uv run pytest`) before considering the task done
- If checks fail, attempt one fix pass; if still failing, stop and report to the user rather than looping
- Never commit or push without explicit user confirmation, even after all checks pass

### Model Selection
- For complex implementation tasks, use a stronger model available in this environment (e.g. GLM-5.2, Qwen3.7 Max, DeepSeek V4 Pro)
- For simple tasks (docs, formatting, boilerplate), use a cheaper/faster model (e.g. DeepSeek V4 Flash, MiniMax M3) to conserve usage limits

---

## Important Constraints

- **No `print()` in library code** — use `logging` with the module-level logger (`logger = create_logger(name=__name__)`)
- **No `os.system()` or `subprocess` without review** — flag these for human review
- **No hardcoded secrets or API keys** — use environment variables or a config file excluded from git
- **No silent exception swallowing** — `except Exception: pass` is never acceptable

---

## Architecture Notes

<!-- TODO: Add any domain-specific context, key abstractions, or non-obvious design decisions here. -->

---

## Frequently Asked Questions

**Q: Where do I add a new configuration option?**
A: src/config/

**Q: How do I run only a subset of tests?**
A: `uv run pytest tests/path/to/test_file.py -k "test_name_fragment"`

**Q: How do I add a new dependency?**
A: `uv add <package>` for runtime deps, `uv add --dev <package>` for dev deps. Commit both `pyproject.toml` and `uv.lock`.
