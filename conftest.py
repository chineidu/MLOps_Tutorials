"""Repo-root pytest conftest.

Adds `src/` to `sys.path` so tests can `from src.<module> import ...`
without requiring an editable install. This is the canonical pattern for
projects that aren't packaged as an installable distribution.
"""
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
