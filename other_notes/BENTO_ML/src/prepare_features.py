from pathlib import Path

import pandas as pd
import polars as pl
from feature_engine.imputation import CategoricalImputer, MeanMedianImputer
from imblearn.combine import SMOTETomek
from omegaconf import DictConfig, OmegaConf
from sklearn import set_config
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from typeguard import typechecked

from .logger import logger
from .utils import Preparedata, save_model, select_features  # type: ignore

pl.set_random_seed(42)

root: Path = Path(__file__).absolute().parent.parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")

# Set global scikit-learn configuration.
set_config(transform_output=config.features.transform_output)

cat_vars: list[str] = list(config.features.cat_vars)
cols_to_drop: list[str] = list(config.features.cols_to_drop)
preprocess_vars: list[str] = list(config.features.preprocess_vars)
uniq_id: str = config.features.unique_id
random_state: int = config.data.random_state
num_vars: list[str] = list(config.features.num_vars)

col_transf: ColumnTransformer = ColumnTransformer(
    transformers=[
        ("num_vars", MinMaxScaler(clip=True), num_vars),
        (
            "cat_vars",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            cat_vars,
        ),
    ],
    remainder="drop",
)
processor: Pipeline = Pipeline(
    steps=[
        ("preprocess", Preparedata(variables=preprocess_vars)),
        ("median_imputer", MeanMedianImputer(variables=num_vars)),
        (
            "cat_imputer",
            CategoricalImputer(
                imputation_method="frequent", variables=cat_vars, ignore_format=True
            ),
        ),
        ("col_transf", col_transf),
    ]
)


@typechecked
def prepare_features(config: DictConfig) -> None:
    """This is used to prepare the data."""
    X_train: pl.DataFrame = pl.read_parquet(source=config.data.train_save_path)
    X_test: pl.DataFrame = pl.read_parquet(source=config.data.test_save_path)

    # The uniq_id is the Unique_id (Polars does NOT maintain order)
    y_train: pd.DataFrame = (
        X_train.select([uniq_id, config.data.target]).sort(uniq_id).drop([uniq_id]).to_pandas()
    )
    y_test: pd.DataFrame = (
        X_test.select([uniq_id, config.data.target]).sort(uniq_id).drop([uniq_id]).to_pandas()
    )

    X_train = select_features(X_train)
    X_test = select_features(X_test)

    X_train_tr: pd.DataFrame = processor.fit_transform(X=X_train.to_pandas())
    X_test_tr: pd.DataFrame = processor.transform(X=X_test.to_pandas())

    # Save the preprocessor
    save_model(config=config, model=processor, is_preprocessor=True)

    # Implementing oversampling for handling the imbalanced class
    smt = SMOTETomek(random_state=random_state)

    X_t_sampled, y_t_sampled = smt.fit_resample(X_train_tr, y_train)
    logger.info(f"Data shape after SMOTE: {X_t_sampled.shape, y_t_sampled.shape}")

    try:
        # Save data
        X_t_sampled.to_parquet(path=config.features.train_features_save_path, index=False)
        X_test_tr.to_parquet(path=config.features.test_features_save_path, index=False)
        y_t_sampled.to_parquet(path=config.features.train_target_save_path, index=False)
        y_test.to_parquet(path=config.features.test_target_save_path, index=False)
        logger.info("`Train` and `Test` features saved!")

    except Exception as err:
        logger.error(f"{err}")

    finally:
        return None


if __name__ == "__main__":
    prepare_features(config=config)
