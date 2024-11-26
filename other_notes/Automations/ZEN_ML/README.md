# [ZEN ML](https://docs.zenml.io/)

- ZenML is an extensible, open-source MLOps framework for creating portable, production-ready machine learning pipelines.
- By decoupling infrastructure from code, ZenML enables developers across your organization to collaborate more effectively as they develop to production.

## Table of Content

- [ZEN ML](#zen-ml)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
    - [Vanilla Installation With Pip](#vanilla-installation-with-pip)
    - [Installation With Dashboard](#installation-with-dashboard)
  - [ZenML Deployment](#zenml-deployment)
    - [Architecture](#architecture)
    - [Deploy With Docker](#deploy-with-docker)
    - [Deploy With Kubernetes](#deploy-with-kubernetes)
    - [Deploy With Hugging Face Spaces](#deploy-with-hugging-face-spaces)
  - [ZenML Concepts](#zenml-concepts)
    - [Add Retry To Steps](#add-retry-to-steps)
    - [Enforce Type Annotation](#enforce-type-annotation)
    - [Start ZenML Local Server](#start-zenml-local-server)

## Installation

### [Vanilla Installation With Pip](https://docs.zenml.io/getting-started/installation)

```sh
pip install zenml
```

### Installation With Dashboard

```sh
pip install "zenml[server]"
```

## ZenML Deployment

- ZenML Cloud (Managed)
- Docker
- Helm (Kubernetes)
- Hugging Face Spaces

### Architecture

[![image.png](https://i.postimg.cc/pT26D1n9/image.png)](https://postimg.cc/2qKGYGGm)

### Deploy With Docker

- Easy [setup](https://docs.zenml.io/getting-started/installation#running-with-docker)

```sh
docker run -it -d -p 8080:8080 zenmldocker/zenml-server
```

- Advanced setup guide can be found [here](https://docs.zenml.io/getting-started/deploying-zenml/deploy-with-docker#zenml-server-configuration-options).

### Deploy With Kubernetes

- The setup guide can be found [here](https://docs.zenml.io/getting-started/deploying-zenml/deploy-with-helm).

### Deploy With Hugging Face Spaces

- The setup guide can be found [here](https://docs.zenml.io/getting-started/deploying-zenml/deploy-using-huggingface-spaces).

## ZenML Concepts

1.) Development

- Steps: These are functions annotated with `@step` decorator. They perform a specific task.

```py
@step
def step_1() -> str:
    """Returns a string."""
    return "world"

@step(enable_cache=False)
def step_2(input_one: str, input_two: str) -> str:
    """Combines the two strings passed in."""
    combined_str = f"{input_one} {input_two}"
    return combined_str
```

### [Add Retry To Steps](https://docs.zenml.io/how-to/pipeline-development/build-pipelines/retry-steps#using-the-step-decorator)

```py
from zenml.config.retry_config import StepRetryConfig

@step(
    retry=StepRetryConfig(
        max_retries=3,
        delay=10,
        backoff=2
    )
)
def my_step() -> None:
    raise Exception("This is a test exception")
```

- Pipelines:  pipeline consists of a series of steps, organized in any order that makes sense for your use case.

```py
# filename: my_pipeline.py
@pipeline
def my_pipeline():
    output_step_one = step_1()
    step_2(input_one="hello", input_two=output_step_one)
```

[![image.png](https://i.postimg.cc/Kc3HtL1D/image.png)](https://postimg.cc/8sD4S7B7)

- Execute the pipeline:

```py
if __name__ == "__main__":
    my_pipeline()

# On the terminal, run:
python my_pipeline.py
```

### Enforce Type Annotation

- If you want to make sure you get all the benefits of type annotating your steps, you can set the environment variable `ZENML_ENFORCE_TYPE_ANNOTATIONS` to True.
- ZenML will then raise an exception in case one of the steps you're trying to run is missing a type annotation.

```sh
export ZENML_ENFORCE_TYPE_ANNOTATIONS=True
```

- Artifacts:
  - Artifacts represent the data that goes through your steps as `inputs` and `outputs` and they are automatically tracked and stored by ZenML in the artifact store.
  - They are produced by and circulated among steps whenever your step returns an object or a value.
- Models:
  - Models are used to represent the outputs of a training process along with all metadata associated with that output.
  - In other words: models in ZenML are more broadly defined as the weights as well as any associated information.
- Materializers:
  - Materializers define how artifacts live in between steps.
  - i.e., they define how data of a particular type can be serialized/deserialized, so that the steps are able to load the input data and store the output data.
- Parameters and Settings:
  - ZenML steps can receive both `artifacts` and `parameters` as input, and they produce artifacts as output. All these elements are stored and managed by ZenML.
- Model and Model versioning:
  - ZenML exposes the concept of a Model, which consists of multiple different model versions.
  - A model version represents a unified view of the ML models that are created, tracked, and managed as part of a ZenML project.
  - Model versions link all other entities to a centralized view.

2.) Execution

- Stacks and Components
- Orchestrators
- Artifact Stores
- Flavor
- Stack Switching

3.) Management

- ZenML Server
- Server Deployment
- Metadata Tracking
- Secrets
- Collaboration
- Dashboard

### Start ZenML Local Server

```sh
zenml login --local
```
