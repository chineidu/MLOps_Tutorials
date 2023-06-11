"""This module contains the test(s) for the endpoint(s)."""

from typing import Any

from fastapi.testclient import TestClient
from pytest import mark


# ==== `Mark` the test as an `integration test` ====
@mark.integration
def test_predict_income(client: TestClient, payload_1: dict[str, Any]) -> None:
    """This is used to test the predict_income enpoint."""
    # Given
    expected = {"status_code": 200}
    URL = "http://0.0.0.0:8000/predict"

    # When
    response = client.post(URL, json=payload_1)
    print(response.json())

    # Then
    assert response.status_code == expected.get("status_code")
    assert response.json().get("predicted_salary") != 0
