from pathlib import Path
from typing import Annotated

import pandas as pd
import polars as pl
from omegaconf import DictConfig, OmegaConf
from typeguard import typechecked
from utils.prepare_data import prepare_data
from utils.prepare_features import prepare_features
from utils.train import train
from zenml import step

root: Path = Path(__file__).absolute().parent.parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")


@step
@typechecked
def load_train_test_data() -> (
    tuple[Annotated[pl.DataFrame, "X_train"], Annotated[pl.DataFrame, "X_test"]]
):
    X_train, X_test = prepare_data(config=config, return_data=True)
    return X_train, X_test


@step(enable_cache=False)
@typechecked
def prepare_model_features(
    X_train: pl.DataFrame, X_test: pl.DataFrame
) -> tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.DataFrame, "y_train"],
    Annotated[pd.DataFrame, "y_test"],
]:
    X_train_tr, X_test_tr, y_train, y_test = prepare_features(
        config=config, X_train=X_train, X_test=X_test, return_data=True
    )
    return X_train_tr, X_test_tr, y_train, y_test


@step
@typechecked
def train_model(X_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
    """This is used to train the model."""
    train(config=config, X_train=X_train, y_train=y_train, if_save_bento_model=False)
