from pathlib import Path

import numpy as np
import polars as pl
from omegaconf import DictConfig, OmegaConf
from sklearn.model_selection import train_test_split
from typeguard import typechecked

from .logger import logger

root: Path = Path(__file__).absolute().parent.parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")
uniq_id: str = config.features.unique_id
random_state: int = config.data.random_state

np.random.seed(random_state)
pl.set_random_seed(42)


@typechecked
def prepare_data(
    config: DictConfig, return_data: bool = False
) -> None | tuple[pl.DataFrame, pl.DataFrame]:
    """This is used to load and split the data."""
    data: pl.DataFrame = pl.read_csv(source=config.data.csv_file_path).rename(
        {"home.dest": "home_dest"}
    )
    data = data.with_columns(pl.int_range(0, len(data)).alias(uniq_id))

    X_train: pl.DataFrame
    X_test: pl.DataFrame

    X_train, X_test = train_test_split(
        data,
        test_size=config.data.test_size,
        random_state=config.data.random_state,
        stratify=data.select(config.data.target),
    )

    try:
        if return_data:
            return X_train, X_test

        # Save data
        X_train.write_parquet(file=config.data.train_save_path)
        X_test.write_parquet(file=config.data.test_save_path)
        logger.info("`Train` and `Test` data saved!")
        return None

    except Exception as err:
        logger.error(f"{err}")
        return None


if __name__ == "__main__":
    prepare_data(config=config)
