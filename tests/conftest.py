"""This module contains the Pytest fixtures."""
from typing import Any, Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from src.core import DATA_FILEPATH
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


@pytest.fixture
def data_v1() -> Generator:
    """This loads the predictions from v1."""
    data = pd.read_csv(f"{DATA_FILEPATH}/data_v1.csv")
    yield data


@pytest.fixture
def data_v2() -> Generator:
    """This loads the predictions from v2."""
    data = pd.read_csv(f"{DATA_FILEPATH}/data_v2.csv")
    yield data
