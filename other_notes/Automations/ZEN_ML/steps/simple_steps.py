from pathlib import Path

import polars as pl
from omegaconf import DictConfig, OmegaConf
from utils.prepare_data import prepare_data
from zenml import step

root: Path = Path(__file__).absolute().parent.parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")


@step
def load_train_test_data() -> dict[str, pl.DataFrame]:
    train_data, test_data = prepare_data(config=config, return_data=True)
    return {"train_data": train_data, "test_data": test_data}
