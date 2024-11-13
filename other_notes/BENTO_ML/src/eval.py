from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from typeguard import typechecked

from .logger import logger
from .utils import load_model

root: Path = Path(__file__).absolute().parent.parent
config: DictConfig = OmegaConf.load("./params.yaml")
model_path: Any = config.train.trained_model_save_path
model = load_model(config=config)
metrics_save_path: Any = config.evaluate.metrics_save_path


@typechecked
def evaluate(config: DictConfig) -> dict[str, Any]:
    """This is used to evaluate the model performance."""
    X_test: pd.DataFrame = pd.read_parquet(path=config.features.test_features_save_path)
    y_test: pd.Series = pd.read_parquet(path=config.features.test_target_save_path)[
        config.data.target
    ]
    test_preds_proba: npt.NDArray[np.float_] = model.predict_proba(X_test)[:, 1]
    test_preds: npt.NDArray[np.float_] = model.predict(X_test)

    # The metrics of the test data
    _acc_score: float = np.round(accuracy_score(y_test, test_preds), 4)
    _auc_score: float = np.round(roc_auc_score(y_test, test_preds_proba), 4)
    _f1_score: float = np.round(f1_score(y_test, test_preds), 4)
    results: dict[str, Any] = {
        # Convert to regular float instead of np.float
        "accuracy_score": float(_acc_score),
        "auc_score": float(_auc_score),
        "f1_score": float(_f1_score),
    }

    logger.info(f" Evaluation results [Unseen]: {results}")

    # Save as yaml
    OmegaConf.save(config=results, f=metrics_save_path)

    return results
