"""This module contains code for testing data preprocessing."""
from typing import Any
from unittest import mock

import pandas as pd
from pytest import fixture, mark

from ml_testing.differential_test import compare_differences
from src.utilities import _check_role, _make_prediction


# The path to the imported `complex` function
# Note: the mocked function must come before the fixture
@mock.patch("src.utilities._calculate_salary")
def test_pre_make_prediction(
    mock__calculate_salary: mock.Mock,
    user_input_1: dict[str, Any],
) -> None:
    """This is used to test the function `_calculate_salary`."""
    # Given
    expected = {
        'name': 'Neidu',
        'role': 'ML Engineer',
        'experience': 3.0,
        'predicted_salary': 294556.09,
    }
    mock__calculate_salary.return_value = 294556.09

    # When
    result = _make_prediction(**user_input_1)

    # Then
    assert result == expected


@mark.parametrize(
    ("input_, output_"),
    (["data engineer", True], ["ML Engineer", True], ["Product Manager", False]),
)
def test_check_role(input_: str, output_: bool) -> None:
    """This is used to test the function `_check_role`."""
    # Given

    # When
    result = _check_role(role=input_)

    # Then
    assert result == output_


# ==== Test using multiple fixtures and parametrize====
@mark.parametrize(
    ("input_", "output_"),
    (["role_1", True], ["role_2", False]),
)
def test_roles(input_: fixture, output_: fixture, request: fixture) -> None:
    """This test uses multiple fixtures with parametrize."""
    # Given
    print(type(input_))

    # Extract the fixture(s)
    input_ = request.getfixturevalue(input_)

    # When
    result = _check_role(role=input_)

    # Then
    assert result == output_


# ==== Test using multiple fixtures, parametrize and xfail====
@mark.xfail(reason="some bug")
@mark.parametrize(
    ("n", "expected"),
    [(1, 1), (1, 0)],
)
def test_increment(n: int, expected: int):
    """This is used to test an expected failed function."""
    # Then
    assert n + 1 == expected


@mark.xfail(reason="There are differences in the predictions")
@mark.differential
def test_model_prediction_differentials(data_v1: pd.DataFrame, data_v2: pd.DataFrame):
    """This is used to perform differential testing."""
    # Given
    N = 10  # Number of rows
    data_v1, data_v2 = data_v1.iloc[:N], data_v2.iloc[:N]

    # When
    pred_v1, pred_v2 = data_v1["predictions"], data_v2["predictions"]

    # Then
    compare_differences(
        expected_predictions=pred_v2,
        actual_predictions=pred_v1,
        # Tolerance
        rel_tol=0.08,
    )
