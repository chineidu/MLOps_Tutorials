from pathlib import Path
from typing import Any, Literal

import bentoml
import numpy as np
import pandas as pd
from bentoml.models import BentoModel
from logger import logger
from omegaconf import DictConfig, OmegaConf
from pydantic import BaseModel, Field
from sklearn.pipeline import Pipeline
from utils import load_model, select_features  # type: ignore

root: Path = Path(__file__).absolute().parent
config: DictConfig = OmegaConf.load(f"{root}/params.yaml")


inference_vars: list[str] = config.features.inference_vars


class Request(BaseModel):
    age: int = Field(default=None, ge=0, le=100)
    fare: float = Field(default=None, ge=0, le=400)
    parch: int = Field(default=None, ge=0, le=8)
    pclass: int = Field(default=None, ge=1, le=3)
    sibsp: int = Field(default=None, ge=0, le=8)
    ticket: str
    embarked: Literal["C", "Q", "S", None] = None
    sex: Literal["female", "male", None] = None


@bentoml.service(
    name="titanic_prediction_service",
    resources={"cpu": 1, "memory": "500Mi"},
    traffic={"timeout": 10},
)
class PredictionService:
    bento_model = BentoModel(f"{config.train.model_name}:latest")

    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model(self.bento_model)
        self.preprocessor: Pipeline = load_model(config=config, is_preprocessor=True)

    @bentoml.api()
    def predict(self, body: Request) -> dict[str, Any]:
        input: pd.DataFrame = pd.DataFrame([body.model_dump()], index=[0])
        input = select_features(input)
        req_matrix: pd.DataFrame = pd.DataFrame(
            self.preprocessor.transform(input), columns=inference_vars
        )

        proba: np.ndarray = self.model.predict_proba(req_matrix).flatten()
        _pred: int = np.argmax(proba)
        pred: dict[str, Any] = {
            "survived": {0: "No", 1: "Yes"}.get(_pred),
            "probability": proba[_pred].round(2),
        }
        logger.info(f"Prediction: {pred}")

        return pred


if __name__ == "__main__":
    bentoml.serve(PredictionService, production=True, reload=False, port=3005)
    # 1``
    # To run: python service.py

    # OR  2.) without bentoml.serve(..)
    # run:
    # bentoml serve service:PredictionService
