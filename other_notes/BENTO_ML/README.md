# BentoML

## Table of Contents

- [BentoML](#bentoml)
  - [Table of Contents](#table-of-contents)
  - [BentoML](#bentoml-1)
    - [BentoML Service](#bentoml-service)
    - [Service APIs](#service-apis)
  - [Model Loading And Management](#model-loading-and-management)
    - [Save A Sckit Learn Model](#save-a-sckit-learn-model)
    - [Load A Model](#load-a-model)
  - [BentoML Cloud](#bentoml-cloud)

## [BentoML](https://docs.bentoml.com/en/latest/get-started/index.html)

- BentoML is a Python library for building online serving systems optimized for AI applications and model inference.

### BentoML Service

- BentoML Services are defined using class-based definitions.
- Each class represents a distinct Service that can perform certain tasks, such as preprocessing data or making predictions with an ML model.
- Service configurations can be found [here](https://docs.bentoml.org/en/latest/guides/configurations.html).

```py
from __future__ import annotations
import bentoml
from transformers import pipeline

@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class Summarization:
    def __init__(self) -> None:
        # Load model into pipeline
        self.pipeline = pipeline('summarization')

    @bentoml.api
    def summarize(self, text: str) -> str:
        result = self.pipeline(text)
        return result[0]['summary_text']
```

- To serve the service, you need to be in the same directory as the service file and run:

```sh
bentoml serve service:<service_name>

# E.g.
bentoml serve service:Summarization
```

### [Service APIs](https://docs.bentoml.org/en/latest/guides/services.html#service-apis)

- The `@bentoml.api` decorator in BentoML is a key component for defining API endpoints for a BentoML Service.
- This decorator transforms a regular Python function into an API endpoint by providing it with additional capabilities needed to function as a web API endpoint:

```py
@bentoml.api
def summarize(self, text: str) -> str:
    result = self.pipeline(text)
    return result[0]['summary_text']
```

## [Model Loading And Management](https://docs.bentoml.org/en/latest/guides/model-loading-and-management.html)

### Save A Sckit Learn Model

```py
import bentoml
from sklearn.base import BaseEstimator

model: BaseEstimator = ... # Any sklearn model
bentoml.sklearn.save_model(name="your_model_name", model=model)
```

- The same applies to other models. e.g. xgboost, lightgbm, etc.

### Load A Model

```py
import bentoml

model_name: str = "your_model_name"

@bentoml.service(
    name="name_of_service"
)
class MyService:
    bento_model = BentoModel(f"{model_name}:latest")

    def __init__(self) -> None:
        # Load model into pipeline
        self.model = bentoml.sklearn.load_model(self.bento_model)

    @bentoml.api()
    def predict(self, body: Request) -> dict[str, Any]:
        ...
```

## [BentoML Cloud](https://www.bentoml.com/pricing)

- This is necessary to deploy your models to the cloud.
- You also need a cloud account before you can build or dockerize your applications.
- You can create a free account [here](https://www.bentoml.com/pricing).
