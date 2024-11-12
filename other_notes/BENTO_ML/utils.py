from pathlib import Path
from typing import Any

import bentoml
import joblib
import pandas as pd
import polars as pl
from logger import logger
from omegaconf import DictConfig, OmegaConf
from sklearn.base import ClassifierMixin, TransformerMixin
from sklearn.pipeline import Pipeline
from typeguard import typechecked

pl.set_random_seed(42)

root: Path = Path(__file__).absolute().parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")
columns: list[str] = (
    config.features.num_vars + config.features.cat_vars + [config.features.unique_id]
)
uniq_id: str = config.features.unique_id


@typechecked
def _check_if_dataframe(
    data: pd.DataFrame | pl.DataFrame,
) -> pd.DataFrame | pl.DataFrame | TypeError:
    """This is used to validate the data."""
    if not isinstance(data, pd.DataFrame | pl.DataFrame):
        raise TypeError(f"{data} MUST be a `Pandas` or `Polars` DataFrame.")
    return data


@typechecked
def get_data_summary(data: pd.DataFrame | pl.DataFrame, features: list[str]) -> pd.DataFrame:
    """Get the summary statistics of the data using Pandas."""

    data = _check_if_dataframe(data)

    if isinstance(data, pl.DataFrame):
        data: pd.DataFrame = data.to_pandas()  # type:ignore

    df: pd.DataFrame = data[features].describe(include="all")  # type:ignore
    df_1: pd.DataFrame = data[features]  # type:ignore
    result: dict[str, Any] = {  # type:ignore
        var: data[var].value_counts(normalize=True).head(1).to_dict()  # type:ignore
        for var in features
    }
    res: dict[str, Any] = {key: v for key, val in result.items() for v in val.values()}
    df_1 = pd.DataFrame(res, index=["top_freq%"])
    df_2: pd.DataFrame = pd.DataFrame(
        data[features].isna().sum()  # type:ignore
    ).T.set_axis(  # type:ignore
        ["num_NaNs"], axis=0
    )

    df_res: pd.DataFrame = pd.concat([df, df_1, df_2], axis="index")
    return df_res


@typechecked
def get_value_counts(data: pd.DataFrame | pl.DataFrame, feature: str) -> pl.DataFrame:
    data = _check_if_dataframe(data=data)
    if isinstance(data, pd.DataFrame):
        data = pl.from_pandas(data)

    result_df: pl.DataFrame = (
        data.lazy()  # type:ignore
        .group_by(feature, maintain_order=True)
        .agg(pl.len().alias("count"))
        .with_columns((pl.col("count") / pl.col("count").sum()).alias("pct_count").round(3))
        .collect()
    )
    return result_df


@typechecked
def save_model(
    config: DictConfig, model: ClassifierMixin | Pipeline, is_preprocessor: bool = False
) -> None:
    """This is used to persist the trained model."""
    model_path: str = config.train.trained_model_save_path
    if is_preprocessor:
        model_path = config.train.preprocessor_save_path

    with open(model_path, "wb") as f:
        joblib.dump(model, filename=f)
    logger.info(f"Model: {model!s} saved successfully")


@typechecked
def save_bento_model(config: DictConfig, model: ClassifierMixin) -> None:
    bento_model = bentoml.sklearn.save_model(name=config.train.model_name, model=model)
    logger.info(f"Model: {bento_model!s} saved successfully")


@typechecked
def load_model(config: DictConfig, is_preprocessor: bool = False) -> ClassifierMixin | Pipeline:
    """This is used to load the trained model."""
    model_path: str = config.train.trained_model_save_path
    if is_preprocessor:
        model_path = config.train.preprocessor_save_path
    logger.info(f"Loading model: {model_path}")
    with open(model_path, "rb") as f:
        model: ClassifierMixin | Pipeline = joblib.load(filename=f)
        return model


class Preparedata(TransformerMixin):
    def __init__(self, variables: list[str]) -> None:
        self.variables = variables

    def fit(self, X: pd.DataFrame | pl.DataFrame, y=None) -> pd.DataFrame:
        """Reqired for sklearn pipeline."""
        return self

    def _to_lower(self, X: pd.DataFrame | pl.DataFrame) -> pl.DataFrame:
        """Convert the labels to lowercase."""
        if isinstance(X, pd.DataFrame):
            X = pl.from_pandas(X)

        for var in self.variables:
            X = X.with_columns(pl.col(var).str.to_lowercase().alias(var))

        return X

    @typechecked
    def transform(self, X: pd.DataFrame | pl.DataFrame, y=None) -> pd.DataFrame:
        """Apply the transformation."""
        X = self._to_lower(X)

        X = X.with_columns(
            ticket=pl.col("ticket").str.contains(r"^\D"),
        ).with_columns(
            ticket=(pl.when(pl.col("ticket").eq(False)).then(pl.lit(0)).otherwise(pl.lit(1)))
        )

        return X.sort(uniq_id).drop(uniq_id).to_pandas()


@typechecked
def select_features(data: pl.DataFrame | pd.DataFrame) -> pl.DataFrame:
    """Select the features from the data."""
    if isinstance(data, pd.DataFrame):
        data = pl.from_pandas(data)

    if uniq_id not in data.columns:
        data = data.with_columns(pl.int_range(0, len(data)).alias(uniq_id))
    return data.select(columns)
