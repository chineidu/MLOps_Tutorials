.PHONY: setup_venv clean_pyc clean_test test code_quality lint checks
THRESHOLD:= 80

setup_venv: # Create virtual env. You have to run this first!
	python3 -m venv .venv && . .venv/bin/activate \
	&& pip install --upgrade pip \
	&& pip install -e ".[dev]"


clean_pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean_test:
	rm -f .coverage
	rm -f .coverage.*
	find . -name '.pytest_cache' -exec rm -fr {} +

clean: clean_pyc clean_test
	find . -name '.my_cache' -exec rm -fr {} +
	rm -rf logs/

test: clean # src is the source code
	. .venv/bin/activate && py.test tests -vv --cov=src \
	--cov-report=term-missing --cov-fail-under ${THRESHOLD}

code_quality:
	. .venv/bin/activate && pylint src && mypy src

lint:
	. .venv/bin/activate && black src && isort src

checks: test lint mypy code_quality
