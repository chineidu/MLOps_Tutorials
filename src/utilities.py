"""This module contains utility functions."""
import json
import logging
import os
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


def _make_prediction(*, name: str, role: str, experience: Optional[float]) -> dict[str, Any]:
    """This is used to make predictions."""
    LOW, HIGH = 300_000, 800_000
    MAX, SIZE, CONSTANT = 5, 10, 0.02

    experience = (
        CONSTANT
        if experience is None
        else (CONSTANT if experience == 0 else experience)  # type:ignore
    )

    _res = np.random.random() * experience
    SCALER = MAX if _res > MAX else _res
    salaries = np.random.randint(low=LOW, high=HIGH, size=SIZE)

    estimated_salary = np.round(
        (np.random.choice(a=salaries, size=1, replace=False)[0] * SCALER), 2
    )
    result = {
        "name": name,
        "role": role,
        "experience": float(experience),
        "predicted_salary": float(estimated_salary),
    }

    return result


# Load the DB
fp = "./data/DB.json"
DB = _load_database(filename=fp)
