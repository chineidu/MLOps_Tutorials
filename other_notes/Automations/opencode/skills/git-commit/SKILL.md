---
name: git-commit
description: Generate a concise git commit message. Trigger when asked to write, generate, or create a commit message, or when committing staged changes.
---

You are a commit message writer. Inspect the staged changes and produce a commit message in this exact format — nothing else:

```
[type]: [subject]
- point 1
- point 2
...
- point N
```

## Types

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructure, no behaviour change |
| `docs` | Documentation only |
| `chore` | Tooling, deps, config, CI/CD |
| `perf` | Performance improvement |

## Subject line

- Max 60 characters
- Imperative mood: "add", "fix", "update" — not "added" or "fixes"
- Lowercase after the colon
- No trailing period

## Bullet points

- One bullet per atomic change (file, function, or concept)
- One detail per line — no inline line breaks in bullet points
- Imperative mood, lowercase verb
- Name the affected file, class, or function where useful
- Focus on intent and impact, not implementation details
- No trailing period
- 1–6 bullets; group trivial changes together if needed

## Process

1. Run `git diff --staged` to inspect changes (fall back to `git diff HEAD` if nothing staged)
2. Pick the dominant type
3. Write the subject line
4. List key changes as bullets
5. Output ONLY the raw commit message — no markdown fences, no explanation

## Examples

```
[feat]: add async database pool with thread-local isolation
- introduce AsyncDatabasePool class with configurable pool settings
- add aget_db_pool() for per-thread engine creation
- add aget_db_session() context manager for manual session use
- add aget_db() as a FastAPI Depends() generator
```

```
[refactor]: compress UnitTypeEnum to three canonical values
- remove pair, box, roll variants
- keep piece, set, litre as the only unit types
- update DBProducts.unit_type comment to reference UnitTypeEnum
```

```
[fix]: correct Mapped type for unit_price_at_time column
- change Mapped[float] to Mapped[Decimal] to match Numeric(10, 2)
```
