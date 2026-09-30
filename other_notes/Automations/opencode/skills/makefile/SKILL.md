---
name: makefile
description: Create or update a Makefile for a Python project in the style of the Indicina ML/service repos (cdl-models, model_service, income-model). Use whenever the user asks to add a Makefile, scaffold a Makefile, create dev tooling targets, add a `make check` aggregator, add an `api-run` target, add port utilities, or standardize their dev workflow. Also use when the user wants to bring an existing Makefile into this pattern — even if they don't say "makefile" explicitly but mention `make test`, `make lint`, `make api-run`, or `make check`. Do not use for non-Python projects, GitHub Actions workflows, pre-commit configs, or shell scripts.
compatibility: opencode
---

# Makefile (Python project pattern)

Emit or update a `Makefile` for a Python project following the convention used
across Indicina's ML and service repos (`cdl-models`, `model_service`,
`income-model`, and friends). The shape is consistent: emoji-fenced `help`
target, dev workflow (`install`, `test`, `lint`, `format`, `type-check`,
`clean-cache`), `api-run` via gunicorn + uvicorn workers with port utilities,
and an optional Docker block. Adapt to what the repo actually has.

## Read the repo first

Before writing anything, detect what the project provides. Do not assume all
targets apply.

| Signal | Where to look | If present, emit |
| --- | --- | --- |
| `uv.lock` or `[tool.uv]` in `pyproject.toml` | repo root | `install` runs `uv sync`; everything else goes through `uv run ...` |
| `requirements.txt` only, no `uv` | repo root | `install` runs `pip install -r requirements.txt`; everything else goes through `python -m ...` or direct calls |
| `src/<pkg>/api/app.py` *or* `src/api/app.py` exposing `app: FastAPI` | `src/` | `api-run` via `gunicorn -k uvicorn.workers.UvicornWorker` — use the importable path that actually resolves (e.g. `src.api.app:app` if the package directory is `src/api/`, not `src/<pkg>/api/`). Verify with `python -c "from <dotted.path> import app"` or by reading the existing imports in `src/<pkg>/api/*.py` before emitting. |
| `app.py` at root (Flask-style, e.g. bsp-api) | repo root | `start_server` via the framework's own CLI (flask run, etc.) — not the FastAPI block |
| `docker-compose.yml` / `docker-compose.yaml` | repo root | `up`/`down`/`restart`/`logs`/`status`/`clean-all` targets |
| `docker/init-rabbitmq-vhost.sh` or similar one-off init | `docker/` | Append the init call to the `up` target only if the script exists. Skip otherwise. |
| `[tool.ruff]` in `pyproject.toml` | `pyproject.toml` | `lint` and `format` use `ruff` |
| `[tool.mypy]` or `mypy.ini` | repo root | `type-check` uses `mypy` |
| `.ty`-style type checker, or sibling repo uses `ty` | `pyproject.toml`/Makefile | `type-check` uses `uv run ty check` |
| `alembic/` or `alembic.ini` | repo root | `migration` (autogenerate) and `migrate` (apply) targets |
| `tests/` | repo root | `test`/`test-verbose`/`test-cov` |
| `pyproject.toml` `[tool.coverage.*]` or existing `--cov=` flag | `pyproject.toml`, Makefile | `test-cov` mirrors the existing flag, do not invent `--cov=src` if the repo says otherwise |

If a signal is missing, omit the corresponding target rather than emitting it
broken. An empty Docker block is worse than no Docker block.

## Aggregate target name

The three sibling repos use `make lint-format-all` as their aggregator. The
bnpl repo's `AGENTS.md` prescribes `make check` running `ruff format` →
`ruff check` → `ty check` → `pytest` in that order.

Decision rule:

1. If `AGENTS.md`, `README.md`, or `CONTRIBUTING.md` already names an
   aggregator target, use that name and that order.
2. Otherwise default to `make check` running the four steps in the order
   above. Format first because `ruff format` output is what `ruff check` and
   `ty check` then validate; pytest last because it is the slowest.
3. If the repo has no type checker at all, drop `type-check` from the
   aggregator rather than skipping it silently. Aggregator should still be
   a meaningful "everything is green" check. **Concretely: "no type
   checker" means** `pyproject.toml` has neither `[tool.mypy]`, nor any
   `[tool.ty]` section, nor a sibling Makefile using `mypy`/`ty`. If any
   of those signals exist, include `type-check`. Don't infer absence from
   a sparse pyproject alone — repos routinely add type-checker config
   later, and emitting `uv run ty check` is harmless if `ty` isn't yet a
   dev dependency (it just fails until installed).

## Scaffolding the file

A fresh Makefile should have this structure, in this order:

1. `.PHONY` declaration listing every target — keep two `.PHONY` lines if the
   list is long (cdl-models does this; the Makefile parser is fine with it).
2. `help:` — the only target that prints to stdout without a leading `@`-prefix
   isn't needed; prefix every `echo` with `@` to suppress the command line.
3. `install:` — minimal, one line of real work.
4. Service runner block (FastAPI runner or framework-specific, depending on
   detection).
5. Port utilities (`check-port`, `kill-port`) — these are referenced by the
   runner, so they come before it if you want clean forward references, but
   `make` resolves order at parse time so the actual placement is cosmetic.
6. Docker block — only if `docker-compose.*` is present.
7. Database migrations — only if `alembic/` or `alembic.ini` is present.
8. Dev workflow targets (`test`, `test-verbose`, `test-cov`, `type-check`,
   `lint`, `format`, aggregator, `gen-req`, `clean-cache`).
9. Aggregator target at the end of the dev-workflow section so it can depend
   on the others.

## Targets in detail

### help

Echo-only, no real work. Use the same emoji-fenced section headers as
cdl-models so muscle memory transfers:

```
📦 Development:
🚀 Running the Application:
🐳 Docker Services:   (omit if no docker-compose)
🛠 Utilities:
🗄  Database Migrations:   (omit if no alembic)
```

Each target line uses two spaces of left-padding inside the description,
followed by `- description`. **Alignment rule:** target names in the help
block are padded to the width of the longest name in that section, then a
single `-` separator, then the description. For the dev-workflow section
that means target names line up at column 16 (e.g. `  test-verbose  - `).
Don't pad with extra spaces for visual symmetry — fixed-width alignment
helps `grep` and copy-paste. Do not end descriptions with a period unless
they are full sentences; one-line target summaries read better without
trailing punctuation.

### install

```make
install:
	@echo "📦 Installing dependencies..."
	uv sync
```

If the repo uses pip instead of uv, swap to `pip install -r requirements.txt`.

### api-run (FastAPI repos)

The pattern is gunicorn forking uvicorn workers. `WORKERS` defaults to 2 and
is overridable. The target checks the port first via `check-port`, prompts
before killing, then launches:

```make
WORKERS ?= 2
api-run:
	@echo "🚀 Starting FastAPI server on http://localhost:$(PORT)"
	@PORT=$(PORT) $(MAKE) check-port || { \
		echo; \
		echo -n "❓ Port $(PORT) is in use. Kill and continue? (y/N) "; \
		read -r confirm; \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			PORT=$(PORT) $(MAKE) kill-port; \
			PORT=$(PORT) $(MAKE) check-port || { echo "🛑 Port $(PORT) still busy after kill attempt."; exit 1; }; \
		else \
			echo; \
			echo "🛑 Aborted. Free port $(PORT) manually or use a different port."; \
			exit 1; \
		fi; \
	}
	@echo "✅ Port $(PORT) is free. Launching FastAPI..."
	@uv run -m gunicorn --pythonpath . \
		-k uvicorn.workers.UvicornWorker \
		src.<pkg>.api.app:app \
		-w $(WORKERS) --bind "0.0.0.0:$(PORT)"
```

Replace `src.<pkg>.api.app:app` with the actual importable path. If the
service uses Flask, replace the whole block with `flask run --port $(PORT)`
or whatever the repo already does (see bsp-api).

On macOS, `gunicorn` workers can abort at startup due to Objective-C runtime
forking. The income-model Makefile guards this with:

```make
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
GUNICORN_ENV := OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
endif
```

…and prefixes the gunicorn command with `$(GUNICORN_ENV)`. Add this only if
the repo is macOS-targeted or if the user reports worker crashes during
startup. Don't add it by default — it's noise on Linux CI.

### api-stop

If the repo has `api-run`, add `api-stop` as a thin alias for
`PORT=$(PORT) make kill-port`. income-model and model_service have this; it
is a small ergonomic win.

### check-port / kill-port

```make
PORT ?= 8000

check-port:
	@echo "🔍 Checking if port $(PORT) is in use..."
	@if lsof -i :$(PORT) >/dev/null 2>&1; then \
		echo "⚠️  Port $(PORT) is in use"; \
		exit 1; \
	else \
		echo "✅ Port $(PORT) is free"; \
		exit 0; \
	fi

kill-port:
	@echo "💀 Killing process using port $(PORT)..."
	@if lsof -i :$(PORT) >/dev/null 2>&1; then \
		PID=$$(lsof -ti :$(PORT)); \
		echo "Killing process $$PID on port $(PORT)"; \
		kill -9 $$PID; \
		sleep 1; \
		if lsof -i :$(PORT) >/dev/null 2>&1; then \
			echo "⚠️  Port $(PORT) still in use after kill attempt."; \
			exit 1; \
		else \
			echo "✅ Port $(PORT) freed."; \
			exit 0; \
		fi; \
	else \
		echo "ℹ️  No process using port $(PORT)."; \
		exit 0; \
	fi
```

`lsof` is macOS/BSD-flavoured. On Linux it works the same way. Do not
substitute `fuser` or `ss` — consistency with the sibling repos is the
point. If the user is on Linux and `lsof` is missing, surface that as an
explicit error rather than silently switching tools.

### Docker block

Only emit if `docker-compose.yml` or `docker-compose.yaml` is present. The
six standard targets:

```make
up:
	docker-compose up -d && sleep 10

down:
	docker-compose down

restart: down up

clean-all:
	@echo "🧹 Warning: This will remove all containers, networks, images, and volumes!"
	docker-compose down -v --remove-orphans

logs:
	docker-compose logs -f

status:
	docker-compose ps

setup: clean-all up
	@echo "Setup complete! Services are running."
```

If `docker/init-rabbitmq-vhost.sh` (or any other one-off init script) is
present and the user wants it run on `up`, append `@docker/<script>` to the
`up` target with an `@` prefix to suppress command echo. Do not invent
init scripts.

If the repo has a `compose.yaml` (modern Docker Compose v2 syntax), use
`docker compose` (with a space) instead of `docker-compose`. Check the
file's first few lines — `-f` flag, `version:` key, etc. — for the
vintage.

### Migrations (Alembic)

```make
migration:
	@echo "🗄  Generating new Alembic migration..."
	uv run alembic revision --autogenerate -m "$(msg)"

migrate:
	@echo "🗄  Applying migrations to head..."
	uv run alembic upgrade head
```

The `msg` variable is required for `migration`. Make will treat `msg="..."`
as a make-variable assignment, so `make migration msg="add users.email"`
works. The repo's existing `alembic.ini` and `env.py` should already be set
up — the Makefile just wires the CLI.

### Dev workflow targets

```make
test:
	@echo "🧪 Running tests..."
	uv run -m pytest

test-verbose:
	@echo "🧪 Running tests..."
	uv run -m pytest -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	uv run -m pytest --cov=src

type-check:
	@echo "🔍 Running type checks..."
	uv run ty check

lint:
	@echo "🔍 Running linter..."
	uv run ruff check .

format:
	@echo "✨ Formatting code..."
	uv run ruff check --fix .
	uv run ruff format .

gen-req:
	@echo "📄 Generating requirements_test.txt..."
	uv pip compile -o requirements_test.txt pyproject.toml

clean-cache:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null
	find . -type f -name "*.pyc" -delete 2>/dev/null
	@echo "✅ Cleanup complete"
```

Notes:

- `test-cov` defaults to `--cov=src` (the cdl-models convention). If the
  repo's `pyproject.toml` has `[tool.coverage.*]` configured with a
  different source path, mirror it. If the repo has *no* coverage config
  at all, still emit `--cov=src` — that's the project's signal that they
  want coverage, and the user can refine it. Don't silently drop the flag.
- `type-check` uses `ty` because that's what bnpl and the cdl-models lineage
  standardized on. If the repo has `[tool.mypy]` configured, use `mypy`.
- `format` runs `ruff check --fix .` first, then `ruff format .`. The fix
  pass handles import sorting and unsafe autofixes; the format pass handles
  whitespace. This is the order the bnpl `AGENTS.md` prescribes.
- `clean-cache` deliberately does not have a trailing `|| true` on each
  line. Errors surface. If `find` returns no matches that's not an error
  (exit 0); only real failures (permissions, missing tool) should be loud.

### Aggregator target

Name and order per the **Aggregate target name** section above.

```make
# AGENTS.md name. Runs format first, then lint, type-check, pytest.
check: format lint type-check test
	@echo "✅ All checks complete"
```

If the repo uses the cdl-models name:

```make
lint-format-all: test test-cov type-check lint format
	@echo "✅ All checks complete"
```

The cdl-models variant runs tests inside the aggregator. That's a
deliberate choice there — it makes "did everything pass" one command — but
it conflates lint+format with test runs. Don't replicate that pattern
unless the repo already does. The `check` variant separates them by
running `lint`+`format` (format already does fix+format) and `test`
distinctly; coverage is its own optional target.

## When updating an existing Makefile

Do not rewrite a working Makefile from scratch. Detect what is already
there and:

1. If the new pattern fits the repo's existing structure, only add missing
   targets. Don't rename `lint-format-all` to `check` unless AGENTS.md asks
   for it.
2. If the existing Makefile uses different tooling (mypy vs ty, pip vs uv),
   keep what's working and add the new targets alongside.
3. If the user asks for a specific change, make the smallest change that
   satisfies it. Don't refactor `help` while adding `api-stop`.

The user almost always has a reason for what's already there. Ask if a
target seems wrong rather than silently replacing it.

## Hard rules

- Never use `print()` in the Makefile — `@echo` is the equivalent, prefixed
  to suppress command echo.
- Never use `|| true` to silence errors in `clean-cache` or anywhere else.
  Surface the failure.
- Never hardcode paths to the user's machine. Use `$(shell ...)` with
  portable tools (`uname -s`, `lsof`, `find`).
- Never run `docker system prune` or anything that destroys untagged
  resources outside the project's own compose stack.
- Never commit the generated Makefile without showing the user the diff
  first. Makefile changes can quietly break CI.
