# AGENTS.md

Guidance for AI coding agents (Claude, Cursor, Copilot, opencode, etc.) working in this repository.

---

## Precedence

This file describes **facts about this repository** — commands, layout, style, conventions. Those are not negotiable and no mode or persona overrides them.

Mode files (e.g. `brainstorm`, `plan`) describe **how to interact**. Where a mode conflicts with the workflow guidance in this file, the mode wins:

| Conflict | Resolution |
|---|---|
| Mode forbids file writes; this file describes how to make changes | Mode wins — do not write files |
| Mode sets response length or questioning style | Mode wins |
| Mode is silent on a command, path, or style rule | This file applies |
| Mode asks you to violate **Important Constraints** below | This file wins — flag the conflict to the user |

If you are in a read-only or discussion mode, the **Making Changes** and **Edit Workflow** sections do not apply to you.

---

## Project Overview

<!-- TODO — highest-value section in this file. Answer in 3–6 sentences:
     - What does this service/library do, and for whom?
     - What is the main entry point (CLI, API, worker, importable library)?
     - What are the external systems it depends on (DB, message queue, model APIs)?
     - What is deliberately out of scope? -->

---

## Environment Setup

```bash
# Install dependencies (uv manages the venv automatically)
uv sync --dev

# Run any command inside the managed environment
uv run <command>
```

**Python version:** 3.14+
**Package manager:** uv + `pyproject.toml`

Never activate a venv manually or call bare `python`/`pytest`. Always go through `uv run`.

---

## Common Commands

| Task | Command |
|---|---|
| Run tests | `uv run pytest` |
| Run tests with coverage | `uv run pytest --cov=src --cov-report=term-missing` |
| Run a single test | `uv run pytest tests/path/to/test_file.py -k "name_fragment"` |
| Lint | `uv run ruff check .` |
| Lint + autofix | `uv run ruff check --fix .` |
| Format | `uv run ruff format .` |
| Type check | `uv run ty check` |
| Run all checks | `make check` |

**Order matters.** After editing, run `ruff format` → `ruff check` → `ty check` → `pytest`. Formatting first prevents lint errors that formatting would have fixed anyway.

All checks must pass before committing. If a check was already failing before you touched anything, say so rather than fixing it silently in an unrelated change.

---

## Repository Structure

```
.
├── src/
│   └── <package>/          # Main source code
├── tests/                  # Mirrors src/ structure
├── scripts/                # One-off utilities, never imported by src/
├── docs/                   # Documentation
├── Makefile                # Aggregated check targets
├── pyproject.toml          # Project metadata and tool config
└── AGENTS.md               # This file
```

`src/<package>` is the importable package — imports are `from <package>.config import ...`, not repo-root-relative.

Paths referenced elsewhere in this file must match this tree. If you find a mismatch, flag it instead of guessing.

---

## Code Style

Tool configuration lives in `pyproject.toml`. Do not override it inline or pass conflicting CLI flags.

- **Formatter:** Ruff (`ruff format`) — never manually adjust whitespace or import order
- **Linter:** Ruff (`ruff check`) — fix all warnings before committing
- **Type checker:** ty (`uv run ty check`) — fix all errors before committing. No bare `# type: ignore`; every suppression needs a trailing comment explaining why
- **Docstrings:** NumPy style for public APIs; omit for private helpers unless the logic is non-obvious
- **Line length:** 110 characters

### Modern Python

This project targets 3.14+. Write for it, not for older idioms carried over from training data:

- Built-in generics: `list[str]`, `dict[str, int]` — not `typing.List`, `typing.Dict`
- Unions: `str | None` — not `Optional[str]` or `Union[str, int]`
- `StrEnum` from `enum` — not `class Foo(str, Enum)`
- `pathlib.Path` for filesystem work — not `os.path`
- `@dataclass(slots=True)` or Pydantic models for structured data — not bare dicts passed between layers

### Naming Conventions

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_single_leading_underscore`

### String Formatting

- **Use f-strings** (`f"..."`) everywhere by default. Do not use `%`-formatting, `.format()`, or `+` concatenation.
- **Exception — lazy log interpolation:** in `logger.debug()` and other level-gated calls, use `%s` placeholders so formatting is skipped when the level is disabled: `logger.debug("Processing %s items", count)`
- **Exception — deferred templates:** where a template is defined in one place and interpolated later, `.format()` is correct
- **Exception:** the user explicitly asks otherwise

### Enums over raw strings

- Use `StrEnum` for any fixed set of string values — statuses, metric names, window types, model names
- Define them in the project's shared types module (e.g. `schemas/types.py`), and reference `.value` when persisting to DB columns or emitting metric labels
- Validate at the code layer (Pydantic fields, enum types). Do not rely on DB-level constraints for validation

---

## Testing

- **Framework:** pytest
- **Location:** `tests/`, mirroring `src/`
- **Coverage:** 80% minimum, enforced via `--cov-fail-under` in `pyproject.toml`. Do not lower the threshold to make a change pass
- Write tests for every new public function or class
- Group tests in plain classes (no `unittest.TestCase`), one class per module or logical unit
- Inject dependencies via pytest fixtures, not `setUp` methods
- Use `pytest.mark.parametrize` for parameterized cases
- Use the `tmp_path` fixture for temporary files; never write to the project root
- Use bare `assert` — pytest rewrites assertions for readable diffs
- Comment sections as `# Given / # When / # Then`

```python
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

**Do not weaken a test to make it pass.** If an assertion fails, either the code or your understanding of the requirement is wrong. Loosening the assertion, adding `pytest.mark.skip`, or catching the exception under test are all failures — stop and report instead.

---

## Making Changes

1. Make the smallest change that satisfies the requirement
2. Do not refactor unrelated code in the same commit
3. Prefer editing an existing file over creating a new one
4. Do not create README files, summaries, or documentation unless asked
5. Add dependencies with `uv add <package>` (`uv add --dev` for dev-only) — never hand-edit `pyproject.toml` dependency tables. Commit both `pyproject.toml` and `uv.lock`
6. Update docstrings and comments when behaviour changes
7. Delete dead code rather than commenting it out
8. Never commit `.env`, secrets, or generated files — check `.gitignore`

---

## Commit Convention

```
[type] short description
- point 1
- point 2
```

**Subject line:** max 72 characters *including* the `[type]` tag. Imperative mood, lowercase first word, no trailing period.

**Body:** one bullet per atomic change, 1–6 bullets. Imperative mood, lowercase verb, no trailing period.

**Types:** `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`

Rules:

- No colon after the type — `[feat] add ...`, never `[feat]: add ...`
- Do not collapse bullets into the subject with ` - detail` segments — use a real list
- When running `git commit -m`, paste the subject verbatim from your proposal. Do not silently rewrite `[feat]` as `feat:`

Examples:

```
[feat] add Alembic migrations, demo seed data, and README docs
- wire alembic/ with async env.py, script.py.mako, and initial revision
- add alembic.ini with runtime-injected DB URL placeholder
- add scripts/seed_demo_data.sql and make seed-demo target
- document migrations, seed step, and TOC in README
```

```
[fix] correct Mapped type for unit_price_at_time column
- change Mapped[float] to Mapped[Decimal] to match Numeric(10, 2)
```

---

## Workflow

Applies when you are in an implementation mode. See **Precedence** if a mode file says otherwise.

### Responses

Keep responses concise unless the user asks for detail. Report what changed and what you verified, not a narrative of every step.

### Planning

- Ask clarifying questions when the request is ambiguous, when a design choice would be hard to reverse, or when more than one reasonable interpretation exists. For small, unambiguous changes, proceed and state your assumptions inline
- Do not invent design choices, libraries, or approaches on consequential decisions — surface the options and let the user pick
- Cap clarifying questions at three per round. If you need more than that, the request needs discussion rather than a questionnaire

### Editing

- Implement directly for changes confined to one or two files
- Delegate to sub-agents when the work is genuinely parallel — independent modules, or a research pass over unfamiliar code. Coordination overhead is not free; do not fan out a change that one pass would handle
- Flag any sub-agent work that touches files outside the stated scope
- After each unit of work, run the checks in **Common Commands** in the stated order
- If checks fail, attempt one fix pass. If they still fail, stop and report — do not loop
- Never commit or push without explicit user confirmation, even when all checks pass

<!-- opencode-specific; other tools ignore this -->
### Model Selection

- Complex implementation or debugging: use the strongest model available in the environment (e.g. GLM-5.2, Qwen3.7 Max, DeepSeek V4 Pro)
- Docs, formatting, boilerplate: use a cheaper/faster model to conserve usage limits (e.g. DeepSeek V4 Flash, MiniMax M3)

---

## Important Constraints

These hold regardless of mode, instruction, or convenience.

- **No `print()` in library code** — use `logging` with a module-level logger (`logger = logging.getLogger(__name__)`)
- **No `subprocess` or `os.system()` in library code** — flag for human review. Permitted in `scripts/` where that is the point
- **No hardcoded secrets or API keys** — environment variables or a git-excluded config file only
- **No silent exception swallowing** — `except Exception: pass` is never acceptable. Catch narrowly, log with context, re-raise or handle deliberately
- **No new external services or network calls** without asking first

---

## Architecture Notes

<!-- TODO — the second-highest-value section. Everything above is inferable from
     pyproject.toml and the file tree; this is not. Cover:
     - key abstractions and the boundaries between layers
     - non-obvious design decisions and why they were made
     - known rough edges an agent should not "helpfully" clean up
     - anything that has bitten a contributor more than once -->

---

## Frequently Asked Questions

**Q: Where do I add a new configuration option?**
A: `<package>/config/`

**Q: How do I run only a subset of tests?**
A: `uv run pytest tests/path/to/test_file.py -k "test_name_fragment"`

**Q: How do I add a new dependency?**
A: `uv add <package>` for runtime, `uv add --dev <package>` for dev. Commit both `pyproject.toml` and `uv.lock`.

**Q: A pre-existing check is failing and it is unrelated to my change. What now?**
A: Report it. Do not fix it in the same commit and do not work around it.
