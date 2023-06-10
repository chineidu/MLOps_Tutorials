"""This module contains the Pytest fixtures."""
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from src.fast_api.main import app


@pytest.fixture()
def client() -> Generator:
    """This is used to setup the test client."""
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}


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
