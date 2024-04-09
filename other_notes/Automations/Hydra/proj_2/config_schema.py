from pydantic.dataclasses import dataclass


@dataclass
class Files:
    train_data: str
    test_data: str


@dataclass
class Paths:
    log: str
    data: str


@dataclass
class Params:
    epochs: int
    lr: float
    batch_size: int


@dataclass
class MNISTConfig:
    files: Files
    paths: Paths
    params: Params
