# MLFlow Template

- [Official Docs](https://www.mlflow.org/docs/latest/index.html)

## Table of Contents

- [MLFlow Template](#mlflow-template)
  - [Table of Contents](#table-of-contents)
  - [Simple Setup](#simple-setup)
    - [Simple Tracking URI Setup](#simple-tracking-uri-setup)
  - [1. MLflow Tracking Quickstart](#1-mlflow-tracking-quickstart)
  - [2. MLFlow Tracking Server Overview](#2-mlflow-tracking-server-overview)
  - [3. Register a Model](#3-register-a-model)
  - [2. MLFlow Tracking Server Overview](#2-mlflow-tracking-server-overview-1)
  - [3. Load a Registered Model](#3-load-a-registered-model)
  - [4. Starting the MLflow Tracking Server](#4-starting-the-mlflow-tracking-server)
    - [4b. Setup MLflow Tracking Server For Self-managed MLflow](#4b-setup-mlflow-tracking-server-for-self-managed-mlflow)
    - [Clear All Experiment Runs In A DB](#clear-all-experiment-runs-in-a-db)

## Simple Setup

```py

# Standard imports
import numpy as np
import pandas as pd

# Sklearn
from sklearn import metrics
from sklearn.pipeline import Pipeline

from pydantic import BaseModel
import mlflow

# Built-in
from typing import Any, Union
import warnings


def eval_metrics(actual: np.ndarray, pred: np.ndarray) -> tuple:
    """This is used to evaluate the performance of the model."""
    rmse = metrics.mean_squared_error(actual, pred, squared=False)
    mse = metrics.mean_squared_error(actual, pred, squared=True)
    mae = metrics.mean_absolute_error(actual, pred)
    r2 = metrics.r2_score(actual, pred)

    return (rmse, mse, mae, r2)


Estimator = Union[Pipeline, Any]  # Alias for estimator


class Experiment(BaseModel):
    """This contains the experiment meta data"""

    experiment_name: str
    run_name: str
    model_name: str
    tracking_uri: str


class TrainingData(BaseModel):
    """This is the training data."""

    X_train: Union[pd.DataFrame, np.ndarray]
    X_validate: Union[pd.DataFrame, np.ndarray]
    y_train: Union[pd.Series, np.ndarray]
    y_validate: Union[pd.Series, np.ndarray]

    class Config:
        arbitrary_types_allowed = True


def run_experiment(
    *, experiment: Experiment, estimator: Estimator, training_data: TrainingData
) -> None:
    """This is used to track an MLFlow experiment.

    Params:
    -------
    experiment (Experiment): Experiment object which contains the experiment meta data.
    estimator (Estimator): Estimator object which contains the estimator meta data.
    training_data (TrainingData): Data used for training and validation.

    Returns:
    --------
    None
    """

    from urllib.parse import urlparse
    import warnings
    import logging

    warnings.filterwarnings("ignore")  # Required

    delim = "::"
    format_ = f"%(levelname)s {delim} %(asctime)s {delim} %(message)s"

    logging.basicConfig(level=logging.INFO, format=format_)

    logger = logging.getLogger(__name__)

    # Config
    mlflow.set_tracking_uri(experiment.tracking_uri)
    mlflow.set_experiment(experiment.experiment_name)

    with mlflow.start_run(run_name=experiment.run_name):
        # I'm using autolog
        mlflow.sklearn.autolog()
        logger.info(f"========= Training {experiment.model_name!r} =========")
        estimator.fit(training_data.X_train, training_data.y_train)

        # Make predictions
        y_pred = estimator.predict(training_data.X_validate)

        (rmse, mse, mae, r2) = eval_metrics(
            actual=training_data.y_validate, pred=y_pred
        )
        print(f" Model name: {experiment.model_name}")
        print(f"  RMSE: {rmse}")
        print(f"  MSE: {mse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        # Log params/metrics on MLFlow
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":

            # Register the model
            mlflow.sklearn.log_model(
                estimator, "model", registered_model_name=experiment.model_name
            )
        else:
            mlflow.sklearn.log_model(estimator, "model")
    logger.info(f"========= Training {experiment.model_name!r} Done! =========")

```

### Simple Tracking URI Setup

```py
TRACKING_SERVER_HOST: str = "http://127.0.0.1"  # localhost
PORT: int = 5000  # Default
TRACKING_URI: str = f"{TRACKING_SERVER_HOST}:{PORT}"

mlflow.set_tracking_uri(TRACKING_URI)
```

## 1. MLflow Tracking Quickstart

- Check [here](https://www.mlflow.org/docs/latest/getting-started/intro-quickstart/index.html) for quickstart.

## 2. MLFlow Tracking Server Overview

- Check [here](https://www.mlflow.org/docs/latest/getting-started/tracking-server-overview/index.html) for quickstart.

## 3. Register a Model

- Check [here](https://www.mlflow.org/docs/latest/getting-started/tracking-server-overview/index.html) for quickstart.

## 2. MLFlow Tracking Server Overview

- Check [here](https://www.mlflow.org/docs/latest/getting-started/tracking-server-overview/index.html) for quickstart.

## 3. Load a Registered Model

- Check [here](https://www.mlflow.org/docs/latest/getting-started/registering-first-model/step3-load-model.html) for quickstart.
Load a Registered Model

## 4. Starting the MLflow Tracking Server

- Check [here](https://www.mlflow.org/docs/latest/getting-started/logging-first-model/step1-tracking-server.html) for quickstart.

### 4b. Setup MLflow Tracking Server For Self-managed MLflow

- [Docs](https://www.mlflow.org/docs/latest/getting-started/logging-first-model/step1-tracking-server.html)

### Clear All Experiment Runs In A DB

```sh
mlflow gc --backend-store-uri sqlite:///mlflow.db
```
