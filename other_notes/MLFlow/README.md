# MLFlow Template

- [Official Docs](https://www.mlflow.org/docs/latest/index.html)

## Table of Contents

- [MLFlow Template](#mlflow-template)
  - [Table of Contents](#table-of-contents)
  - [Simple Setup](#simple-setup)
    - [Simple Tracking URI Setup](#simple-tracking-uri-setup)
    - [Creating Experiments With Meaningful Tags](#creating-experiments-with-meaningful-tags)
  - [MLFlow Guide](#mlflow-guide)
    - [1. MLflow Tracking Quickstart](#1-mlflow-tracking-quickstart)
    - [2. MLFlow Tracking Server Overview](#2-mlflow-tracking-server-overview)
    - [3. Register a Model](#3-register-a-model)
    - [4. Load a Registered Model](#4-load-a-registered-model)
    - [5. Starting the MLflow Tracking Server](#5-starting-the-mlflow-tracking-server)
      - [5b. Setup MLflow Tracking Server For Self-managed MLflow](#5b-setup-mlflow-tracking-server-for-self-managed-mlflow)
    - [6. Configure Backend Store](#6-configure-backend-store)
    - [7. Configure Artifact Store](#7-configure-artifact-store)
    - [8. Searching based On Tags](#8-searching-based-on-tags)
  - [MLFlow Setups](#mlflow-setups)
    - [1. Local MLFlow Setup](#1-local-mlflow-setup)

## Simple Setup

```py
# Standard imports
import logging
import warnings
from typing import Any, Literal, TypeAlias
from urllib.parse import urlparse

import mlflow
from mlflow.models import infer_signature
import numpy as np
import numpy.typing as npt
import pandas as pd
from pydantic import BaseModel
from rich.console import Console
from rich.theme import Theme
from sklearn import metrics
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from typeguard import typechecked

custom_theme = Theme(
    {
        "info": "#76FF7B",
        "warning": "#FBDDFE",
        "error": "#FF0000",
    }
)
console = Console(theme=custom_theme)
NPTensor: TypeAlias = npt.NDArray[np.float_]


@typechecked
def eval_metrics(
    actual: NPTensor | pd.Series,
    pred: NPTensor | pd.Series,
    type: Literal["classification", "regression"],
) -> dict[str, Any]:
    """This is used to evaluate the performance of the model."""

    if type == "classification":
        acc = metrics.accuracy_score(actual, pred)
        f1 = metrics.f1_score(actual, pred)
        auc = metrics.roc_auc_score(actual, pred)
        result: dict[str, Any] = {"accuracy": acc, "f1": f1, "auc": auc}

    else:
        rmse = metrics.mean_squared_error(actual, pred, squared=False)
        mse = metrics.mean_squared_error(actual, pred, squared=True)
        mae = metrics.mean_absolute_error(actual, pred)
        r2 = metrics.r2_score(actual, pred)
        result = {"rmse": rmse, "mse": mse, "mae": mae, "r2": r2}

    return result


SklearnPipe: TypeAlias = Pipeline | Any


class Experiment(BaseModel):
    """This contains the experiment meta data"""

    experiment_name: str
    experiment_type: Literal["classification", "regression"]
    run_name: str
    model_name: str
    tracking_uri: str = "http://127.0.0.1:5252"


class TrainingData(BaseModel):
    """This is the training data."""

    X_train: pd.DataFrame | NPTensor
    X_validate: pd.DataFrame | NPTensor
    y_train: pd.Series | NPTensor
    y_validate: pd.Series | NPTensor

    class Config:
        arbitrary_types_allowed = True


class Estimator(BaseModel):
    """This is used to model the estimator."""

    preprocessor: SklearnPipe
    model: BaseEstimator

    class Config:
        arbitrary_types_allowed = True


def run_experiment(
    *,
    experiment: Experiment,
    estimator: Estimator,
    training_data: TrainingData,
) -> None:
    """This is used to track an MLFlow experiment.

    Params:
    -------
    experiment (Experiment): Experiment object which contains the experiment meta data.
    estimator (Estimator): Estimator object which contains the estimator meta data.
    training_data (TrainingData): Data used for training and validation.
    validation_tag (Literal["pending", "passed"]): Tag used to identify the model validation.

    Returns:
    --------
    None
    """

    warnings.filterwarnings("ignore")  # Required

    delim = "::"
    format_ = f"%(levelname)s {delim} %(asctime)s {delim} %(message)s"

    logging.basicConfig(level=logging.INFO, format=format_)
    logger = logging.getLogger(__name__)

    model = estimator.model
    preprocessor = estimator.preprocessor

    # Config
    mlflow.set_tracking_uri(experiment.tracking_uri)
    mlflow.set_experiment(experiment.experiment_name)

    with mlflow.start_run(run_name=experiment.run_name):
        mlflow.set_tag("model.type", experiment.experiment_type)
        # I'm using autolog
        mlflow.sklearn.autolog()
        logger.info(f"========= Training {experiment.model_name!r} =========")
        model.fit(training_data.X_train, training_data.y_train)

        # Make predictions
        y_pred = model.predict(training_data.X_validate)

        experiment_results = eval_metrics(
            actual=training_data.y_validate,
            pred=y_pred,
            type=experiment.experiment_type,
        )
        console.print(f" Model name: {experiment.model_name}")
        console.print(f"  Experiment Results: {experiment_results}", style="info")

        # Log params/metrics on MLFlow
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":

            # Infer the model signature
            signature = infer_signature(
                model_input=training_data.X_train,
                model_output=model.predict(training_data.X_train),
            )
            # Log the pipeline using sk_log_model
            mlflow.sklearn.log_model(
                sk_model=preprocessor,
                artifact_path="preprocessor",
                registered_model_name="preprocessor-model",
            )
            # Register the model
            mlflow.sklearn.log_model(
                sk_model=estimator,
                artifact_path="model",
                registered_model_name=experiment.model_name,
                signature=signature,
                input_example=training_data.X_train,
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

### [Creating Experiments With Meaningful Tags](https://mlflow.org/docs/latest/getting-started/logging-first-model/step3-create-experiment.html)

```py
# Provide an Experiment description that will appear in the UI
experiment_description = (
    "This is the grocery forecasting project. "
    "This experiment contains the produce models for apples."
)

# Provide searchable tags that define characteristics of the Runs that
# will be in this Experiment
experiment_tags = {
    "project_name": "grocery-forecasting",
    "store_dept": "produce",
    "team": "stores-ml",
    "project_quarter": "Q3-2023",
    "mlflow.note.content": experiment_description,
}

# Create the Experiment, providing a unique name
produce_apples_experiment = client.create_experiment(
    name="Apple_Models", tags=experiment_tags
)

```

## MLFlow Guide

### 1. MLflow Tracking Quickstart

- Check [here](https://www.mlflow.org/docs/latest/getting-started/intro-quickstart/index.html) for quickstart.

### 2. MLFlow Tracking Server Overview

- Check [here](https://www.mlflow.org/docs/latest/getting-started/tracking-server-overview/index.html) for quickstart.

### 3. Register a Model

- Check [here](https://www.mlflow.org/docs/latest/getting-started/registering-first-model/step1-register-model.html) for quickstart.

### 4. Load a Registered Model

- Check [here](https://www.mlflow.org/docs/latest/getting-started/registering-first-model/step3-load-model.html) for quickstart.
Load a Registered Model
- Example:

```py
model_name: str = "your_model_name"
model_version: int = "your_model_version" # e.g. 1

model = mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
print(model)
```

### 5. Starting the MLflow Tracking Server

- Check [here](https://www.mlflow.org/docs/latest/getting-started/logging-first-model/step1-tracking-server.html) for quickstart.

#### 5b. Setup MLflow Tracking Server For Self-managed MLflow

- [Docs](https://www.mlflow.org/docs/latest/getting-started/logging-first-model/step1-tracking-server.html)

### 6. Configure Backend Store

- [Docs](https://mlflow.org/docs/latest/tracking/backend-stores.html)

### 7. Configure Artifact Store

- [Docs](https://mlflow.org/docs/latest/tracking/artifacts-stores.html)

### 8. Searching based On Tags

- [Docs](https://mlflow.org/docs/latest/getting-started/logging-first-model/step4-experiment-search.html)


## MLFlow Setups

### 1. Local MLFlow Setup

- Click [here](./other_notes/MLFlow/LOCAL_MLFLOW_SETUP.md)
