# Ray Serve

## Table of Contents

- [Ray Serve](#ray-serve)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Creating Deployments](#creating-deployments)
    - [Via HTTP](#via-http)
    - [Via FastAPI HTTP Deployment](#via-fastapi-http-deployment)
      - [1.)](#1)
      - [2.) Using An Existing FastAPI App](#2-using-an-existing-fastapi-app)
  - [Serve Deployment Using CLI](#serve-deployment-using-cli)

## [Installation](https://docs.ray.io/en/latest/ray-overview/installation.html)

```sh
pip install -U "ray[data,train,tune,serve]"

# For reinforcement learning support, install RLlib instead.
# pip install -U "ray[rllib]"
```

## Creating Deployments

### Via HTTP

```py
import ray
import requests
from fastapi import FastAPI
from ray import serve


app = FastAPI()


@serve.deployment
@serve.ingress(app)
class FirstDeployment:
    @app.get("/")
    def root(self):
        return {"message": "Hello World!"}

serve.run(FirstDeployment.bind())
response = requests.get("http://localhost:8000/")
print(response.json())

# Output:
# {'message': 'Hello World!'}
```

### Via FastAPI HTTP Deployment

#### 1.)

```py
from typing import Any
import requests
from fastapi import FastAPI
from ray import serve
from pprint import pprint


# Create a FastAPI app
app = FastAPI()

@serve.deployment(num_replicas=2)
@serve.ingress(app)
class FirstDeployment:
    @app.get("/")
    def root(self):
        return {"message": "Hello World!"}

    @app.post("/predict")
    def do_something(self, body: dict[str, Any]):
        return f"Hello {body['name']}"



serve.run(FirstDeployment.bind())

# Make a request to the deployment
headers: dict[str, str] = {"Content-Type": "application/json"}
body: dict[str, Any] = {"name": "Neidu!"}
response = requests.post("http://localhost:8000/predict", headers=headers, json=body)
print(response.json())

# Output:
# Hello Neidu!
```

#### 2.) Using An Existing FastAPI App

```py
import ray
import requests
from fastapi import FastAPI
from ray import serve

# Create a FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}

# Create a Serve deployment
@serve.deployment
@serve.ingress(app)
class FastAPIWrapper:
    pass

# Deploy the FastAPI app as a Serve deployment
serve.run(FastAPIWrapper.bind(), route_prefix="/")

# Make a request to the deployment
response = requests.get("http://localhost:8000/")
print(response.json())

# Output:
# {'message': 'Hello World!'}
```

## Serve Deployment Using CLI

```py
# filename: app.py

from typing import Any
import requests
from fastapi import FastAPI
from ray import serve
from pprint import pprint


# Create a FastAPI app
app = FastAPI()

@serve.deployment(num_replicas=2)
@serve.ingress(app)
class FirstDeployment:
    @app.get("/")
    def root(self):
        return {"message": "Hello World!"}

    @app.post("/predict")
    def do_something(self, body: dict[str, Any]):
        return f"Hello {body['name']}"


serve_app = FastAPIWrapper.bind()
```

- To run a Serve deployment, you can use the `serve run` command.

```sh
serve run <filename>:<deployment_name>

# E.g.
serve run app:serve_app
```
