from pathlib import Path

import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm
from typeguard import typechecked

from .eval import evaluate
from .logger import logger
from .utils import save_bento_model, save_model  # type: ignore

root: Path = Path(__file__).absolute().parent.parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")

penalty: str = config.train.penalty
C: float = config.train.C
random_state: int = config.data.random_state
solver: str = config.train.solver
n_estimators: int = config.train.n_estimators
max_depth: int = config.train.max_depth
use_log_model: bool = config.train.use_log_model
n_splits: int = config.train.n_splits

# Initialize StratifiedKFold
folds = StratifiedKFold(n_splits=n_splits, random_state=random_state, shuffle=True)
log_model: LogisticRegression = LogisticRegression(
    penalty=penalty, C=C, random_state=random_state, solver=solver
)
rf_model: RandomForestClassifier = RandomForestClassifier(
    n_estimators=n_estimators, max_depth=max_depth
)
model: LogisticRegression | RandomForestClassifier = log_model if use_log_model else rf_model


@typechecked
def train(
    config: DictConfig,
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    if_save_bento_model: bool = False,
) -> None:
    """This is used to prepare the data."""
    y_train: pd.Series = y_train[config.data.target]  # type: ignore

    auc_vals: list[float] | list = []  # type: ignore

    # Loop through folds
    for _, (train_idx, valid_idx) in tqdm(enumerate(folds.split(X_train, y_train), start=1)):
        """In each iteration of the cross-validation loop, the model is trained on a specific
        subset of the data (training set) and validated on a different subset (validation set),
        facilitating the evaluation of the model's performance across diverse portions of the
        dataset."""
        try:
            # Train model
            X_train_fold, y_train_fold = (
                X_train.iloc[train_idx],
                y_train.iloc[train_idx],
            )
            X_test_fold, y_test_fold = X_train.iloc[valid_idx], y_train.iloc[valid_idx]

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
    if if_save_bento_model:
        save_bento_model(config=config, model=model)
    save_model(config=config, model=model)

    # Evaluate the model
    evaluate(config=config)

    return None


if __name__ == "__main__":
    train(config=config)
