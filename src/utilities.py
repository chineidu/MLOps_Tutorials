"""This module contains utility functions."""
import json
import logging
from typing import Any

import numpy as np


def _set_up_logger(delim: str = "::") -> Any:
    """This is used to create a basic logger."""

    format_ = f"[%(levelname)s]{delim} %(asctime)s{delim} %(message)s"
    logging.basicConfig(level=logging.INFO, format=format_)
    logger = logging.getLogger(__name__)
    return logger


logger = _set_up_logger()


def _save_json_data(*, data: dict[str, Any]) -> None:
    """This is used to save the data as a JSON file."""
    IDX = np.random.randint(low=0, high=5, size=1)[0]
    fp = f"./data/sample_data_{IDX}.json"

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info("Saving done ...\n")


def _make_prediction(*, name: str, role: str) -> dict[str, Any]:
    """This is used to make predictions."""
    LOW, HIGH, SIZE = 300_000, 1_200_000, 10
    SCALER = np.random.random()
    salaries = np.random.randint(low=LOW, high=HIGH, size=SIZE)
    estimated_salary = np.round(
        (np.random.choice(a=salaries, size=1, replace=False)[0] * SCALER), 2
    )
    result = {"name": name, "role": role, "predicted_salary": estimated_salary}

    return result


# Create the DB
DB: dict[str, Any] = {"data": []}
