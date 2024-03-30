from typing import Any

import joblib
import pandas as pd
import polars as pl
from logger import logger
from omegaconf import DictConfig
from sklearn.base import TransformerMixin
from typeguard import typechecked


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
def save_model(config: DictConfig, model: Any) -> None:
    """This is used to persist the trained model."""
    with open(config.train.trained_model_save_path, "wb") as f:
        joblib.dump(model, filename=f)
    logger.info("Model saved successfully")


@typechecked
def load_model(config: DictConfig) -> Any:
    """This is used to load the trained model."""
    with open(config.train.trained_model_save_path, "rb") as f:
        model: Any = joblib.load(filename=f)
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

        return X.to_pandas().sort_values(by="name")
