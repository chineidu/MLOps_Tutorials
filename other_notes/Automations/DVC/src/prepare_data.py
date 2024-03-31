import polars as pl
from logger import logger
from omegaconf import DictConfig, OmegaConf
from sklearn.model_selection import train_test_split
from typeguard import typechecked

config: DictConfig = OmegaConf.load("./params.yaml")


@typechecked
def prepare_data(config: DictConfig) -> None:
    """This is used to load and split the data."""
    data: pl.DataFrame = pl.read_csv(source=config.data.csv_file_path)

    X_train: pl.DataFrame
    X_test: pl.DataFrame

    X_train, X_test = train_test_split(
        data,
        test_size=config.data.test_size,
        random_state=config.data.random_state,
        stratify=data.select(config.data.target),
    )

    try:
        # Save data
        X_train.write_parquet(file=config.data.train_save_path, use_pyarrow=True)
        X_test.write_parquet(file=config.data.test_save_path, use_pyarrow=True)
        logger.info("`Train` and `Test` data saved!")

    except Exception as err:
        logger.error(f"{err}")

    finally:
        return None


if __name__ == "__main__":
    prepare_data(config=config)
