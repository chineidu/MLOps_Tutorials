"""this module contains the Pytest fixtures."""
from typing import Any

import pytest


@pytest.fixture
def user_input_1() -> dict[str, Any]:
    """This is used to load the input for _make_predictions."""
    data = {
        "name": "Neidu",
        "role": "ML Engineer",
        "experience": 3,
    }
    yield data


@pytest.fixture
def role_1() -> str:
    """This returns the role."""
    yield "Research Engineer"


@pytest.fixture
def role_2() -> str:
    """This returns the role."""
    yield "Customer care associate"


@pytest.fixture
def payload_1() -> dict[str, Any]:
    """This is used to load the payload."""
    data = {
        "name": "Neidu",
        "role": "ML Engineer",
        "department": "Data",
        "experience": 3,
    }
    yield data


@pytest.fixture
def payload_2() -> dict[str, Any]:
    """This is used to load the payload."""
    data = {
        "name": "Jeremy",
        "role": "AI Researcher",
        "department": "AGI",
        "experience": 8,
    }
    yield data
