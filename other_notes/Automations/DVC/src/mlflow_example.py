# Standard imports
import warnings
from typing import Any, Literal, TypeAlias
from urllib.parse import urlparse

import mlflow
import numpy as np
import numpy.typing as npt
import pandas as pd
from logger import logger
from mlflow.models import infer_signature
from pydantic import BaseModel
from rich.console import Console
from rich.theme import Theme
from sklearn import metrics
from sklearn.base import BaseEstimator
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from tqdm import tqdm
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


def train_categorical_model(
    *,
    model: Estimator,
    training_data: TrainingData,
) -> None:
    """This is used to prepare the data."""
    random_state: int = 123
    n_splits: int = 5
    # Initialize StratifiedKFold
    folds = StratifiedKFold(n_splits=n_splits, random_state=random_state, shuffle=True)

    auc_vals: list[float] | list = []  # type: ignore

    # Loop through folds
    for _, (train_idx, valid_idx) in tqdm(
        enumerate(folds.split(training_data.X_train, training_data.y_train), start=1)
    ):
        """In each iteration of the cross-validation loop, the model is trained on a specific
        subset of the data (training set) and validated on a different subset (validation set),
        facilitating the evaluation of the model's performance across diverse portions of the
        dataset."""
        try:
            # Train model
            X_train_fold, y_train_fold = (
                training_data.X_train.iloc[train_idx],
                training_data.y_train.iloc[train_idx],
            )
            X_test_fold, y_test_fold = (
                training_data.X_train.iloc[valid_idx],
                training_data.y_train.iloc[valid_idx],
            )

            # Fitting the model
            model.fit(
                X_train_fold,
                y_train_fold,
            )

            # Predicting on validation set and Printing Results.
            y_pred_val = model.predict_proba(X_test_fold)[:, 1]
            auc_val = roc_auc_score(y_test_fold, y_pred_val)
            auc_vals.append(auc_val)

        except Exception as err:
            logger.error(f"{err}")
    # The mean AUC value across all folds
    mean_auc_validation = np.mean(auc_vals)
    logger.info(
        f"Mean AUC [Validation]: {mean_auc_validation:.4f}",
    )

    logger.info("Training finished successfully")

    return None


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

    model = estimator.model
    preprocessor = estimator.preprocessor

    # Config
    mlflow.set_tracking_uri(experiment.tracking_uri)
    mlflow.set_experiment(experiment.experiment_name)

    with mlflow.start_run(run_name=experiment.run_name):
        mlflow.set_tag("model.type", experiment.experiment_type)
        # I'm using autolog
        mlflow.sklearn.autolog()
        logger.info(f" Training {experiment.model_name!r} ")
        train_categorical_model(
            model=model,
            training_data=training_data,
        )

        # Log params/metrics on MLFlow
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            # Infer the model signature
            signature = infer_signature(
                model_input=training_data.X_train,
                model_output=model.predict(training_data.X_train),
            )
            # Log the pipeline
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

    logger.info(f" Training {experiment.model_name!r} Done! ")
