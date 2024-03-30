import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from logger import logger
from omegaconf import DictConfig, OmegaConf
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm
from typeguard import typechecked
from utils import save_model

config: DictConfig = OmegaConf.load("./other_notes/Automations/DVC/params.yaml")
penalty: str = config.train.penalty
C: float = config.train.C
random_state: int = config.train.random_state
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
def train(config: DictConfig) -> None:
    """This is used to prepare the data."""
    X_train: pd.DataFrame = pd.read_parquet(path=config.features.train_features_save_path)
    X_test: pd.DataFrame = pd.read_parquet(path=config.features.test_features_save_path)
    y_train: pd.Series = pd.read_parquet(path=config.features.train_target_save_path)[
        config.data.target
    ]

    # Implementing oversampling for handling the imbalanced class
    smt = SMOTETomek(random_state=random_state)

    X_t_sampled, y_t_sampled = smt.fit_resample(X_train, y_train)
    logger.info(f"Data shape after SMOTE: {X_t_sampled.shape, y_t_sampled.shape}")

    from sklearn.metrics import roc_auc_score

    test_preds = np.empty((n_splits, X_test.shape[0]))
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
    save_model(config=config, model=model)

    return None


if __name__ == "__main__":
    train(config=config)
