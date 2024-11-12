from pathlib import Path
from typing import Literal

import polars as pl
from omegaconf import DictConfig, OmegaConf
from pydantic import BaseModel, Field

pl.Config.set_fmt_str_lengths(1_000)
pl.Config.set_tbl_cols(n=1_000)

from sklearn.pipeline import Pipeline
from utils import load_model

root: Path = Path(__file__).absolute().parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")
columns: list[str] = config.features.num_vars + config.features.cat_vars


class Request(BaseModel):
    age: int = Field(ge=0, le=100)
    fare: float = Field(ge=0, le=200)
    parch: int = Field(ge=0, le=8)
    pclass: int = Field(ge=1, le=3)
    sibsp: int = Field(ge=0, le=8)
    ticket: str
    embarked: Literal["C", "Q", "S"]
    sex: Literal["female", "male"]


fp: str = config.data.train_save_path
preprocessor: Pipeline = load_model(config=config, is_preprocessor=True)

request: Request = Request(
    age=22.0,
    fare=7.25,
    parch=0,
    pclass=1,
    sibsp=1,
    ticket="A/5 21171",
    embarked="S",
    sex="male",
    # cabin="unknown",
    # name="Braund, Mr. Owen Harris",
    # survived=None,
    # boat="?",
    # body=None,
    # home_dest="unknown",
)
# req = request.model_dump()
df: pl.DataFrame = pl.read_parquet(fp).head(100)
# df = select_features(df).to_pandas()
# print(df)
# print(df["embarked"].unique())
# df: pd.DataFrame = pd.DataFrame([req], index=[0])
# out: pd.DataFrame = preprocessor.transform(df)
# print(out)
