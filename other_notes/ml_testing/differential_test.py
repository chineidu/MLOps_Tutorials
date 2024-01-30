"""This module is used to compare the outputs from two versions/models of the same system."""

from typing import Optional

import click
import numpy as np
import numpy.typing as npt
import pandas as pd

from src.core import DATA_FILEPATH


def compare_differences(
    *,
    expected_predictions: npt.NDArray[np.float_],
    actual_predictions: npt.NDArray[np.float_],
    rel_tol: Optional[float] = None,
    abs_tol: Optional[float] = None,
) -> None:
    """This is used to compare the outputs from two models.

    Params:
        expected_predictions: The expected predictions.
        actual_predictions: The actual predictions.

    Returns:
        None

    Raises:
        ValueError is there's a significant difference between the two data.
    """

    diff_exp_actual = len(expected_predictions) - len(actual_predictions)
    diff_actual_exp = len(actual_predictions) - len(expected_predictions)

    if diff_exp_actual:
        raise ValueError(f"Missing {diff_exp_actual} predictions")

    if diff_actual_exp:
        raise ValueError(f"Found {diff_actual_exp} unexpected predictions")

    thresholds = {}

    if abs_tol is not None:
        thresholds["atol"] = abs_tol

    if rel_tol is not None:
        thresholds["rtol"] = rel_tol

    for idx, (actual_prediction, expected_prediction) in enumerate(
        zip(actual_predictions, expected_predictions)
    ):
        if not np.isclose(expected_prediction, actual_prediction, **thresholds):
            raise ValueError(
                f"Prediction at index: {idx} has changed"
                f"\nby more than the thresholds: {thresholds}"
                f"\n{expected_prediction} (expected) vs "
                f"{actual_prediction} (actual)"
            )


@click.command()
def compare_predictions() -> None:
    """This is used to compare the predictions."""
    ABS_TOL, REL_TOL = None, 0.05

    fp1, fp2 = f"{DATA_FILEPATH}/data_v1.csv", f"{DATA_FILEPATH}/data_v2.csv"
    actual_results, expected_results = pd.read_csv(fp1), pd.read_csv(fp2)

    click.echo(
        click.style("Comparing actual_results with expected_results ... ", fg="white", bold=True)
    )
    click.echo()
    try:
        compare_differences(
            expected_predictions=expected_results["predictions"],
            actual_predictions=actual_results["predictions"],
            rel_tol=REL_TOL,
            abs_tol=ABS_TOL,
        )

    except ValueError as err:
        click.echo(click.style(text="ERROR", fg="red", bold=True))
        click.echo(click.style(text=err, fg="red"))

    finally:
        click.echo()
        click.echo(click.style(text="DONE!", fg="green", bold=True))


if __name__ == "__main__":
    compare_predictions()
