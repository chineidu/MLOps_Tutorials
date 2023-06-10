"""This module contains utility functions."""
import json
import logging
import os
import re
from typing import Any, Optional

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


def _load_database(*, filename: str) -> dict[str, Any]:
    """This is used to load the database from a JSON file."""
    db_exists = os.path.exists(filename)

    if db_exists:
        with open(filename, "r", encoding="utf-8") as f:
            db = json.load(fp=f)
    else:
        db = {"data": []}

    return db


def _save_database(*, data: dict[str, list[str]]) -> None:
    """This is used to save the database as a JSON file."""
    fp = "./data/DB.json"

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info("Saving done ...\n")


def _check_role(*, role: str) -> bool:
    """This returns True if the role matches the pattern otherwise False."""
    THRESH = 0
    PATTERN = r"(eng|data|\bML\b|machine|dev)"

    matches = re.compile(pattern=PATTERN, flags=re.I).findall(string=role)
    result = len(matches) > THRESH
    return result


def _calculate_salary(*, scaler: float, role_weight: int) -> float:
    """This returns the estimated salary."""
    SIZE, LOW, HIGH = 10, 100_000, 300_000

    salaries = np.random.randint(low=LOW, high=HIGH, size=SIZE)
    salary_ = (np.random.choice(a=salaries, size=1, replace=False)[0] * scaler) + role_weight

    estimated_salary = np.round(salary_, 2)
    return estimated_salary


# pylint: disable=too-many-locals
def _make_prediction(*, name: str, role: str, experience: Optional[float]) -> dict[str, Any]:
    """This is used to make predictions."""
    MAX, CONSTANT = 5, 0.02

    experience = (
        CONSTANT
        if experience is None
        else (CONSTANT if experience == 0 else experience)  # type:ignore
    )
    # Weights
    is_developer = _check_role(role=role)
    role_weight = 80_000 if is_developer else 10_000
    experience_weight = np.random.random() * experience

    SCALER = MAX if experience_weight > MAX else experience_weight

    estimated_salary = _calculate_salary(scaler=SCALER, role_weight=role_weight)
    result = {
        "name": name,
        "role": role,
        "experience": float(experience),
        "predicted_salary": estimated_salary,
    }

    return result


# Load the DB
fp = "./data/DB.json"
DB = _load_database(filename=fp)
