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
    - [Get The Serve Status](#get-the-serve-status)
    - [Build Serve Config Files For Production Deployment](#build-serve-config-files-for-production-deployment)
    - [Run Serve Deployment Using Config File](#run-serve-deployment-using-config-file)
  - [Best Practices](#best-practices)

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

### Get The Serve Status

```sh
serve status
```

### Build Serve Config Files For Production Deployment

```sh
serve build <filename>:<deployment_name> -o <config_file_name>

# E.g.
serve build app:serve_app -o config.yaml
```

### Run Serve Deployment Using Config File

```sh
serve run <config_file_name>

# E.g.
serve run config.yaml
```

## [Best Practices](https://docs.ray.io/en/latest/serve/production-guide/best-practices.html)

- Use highly configurable serve `config files` for production deployments.

```sh
serve build ${filename}:${deployment_name} -o ${config_file_name}
```

- Use [serve deploy](https://docs.ray.io/en/latest/serve/advanced-guides/deploy-vm.html#deploy-on-vm) (especially for deployments on VMs) for production deployments.

```sh
# List all the files in the current directory
ls
text_ml.py
serve_config.yaml  # This is the config file

# Start Ray on the head node
ray start --head
...

# Deploy the Serve application on the head node using the config file
serve deploy ${config_file_name}
```

- You can also deploy to a remote VM by following the steps [here](https://docs.ray.io/en/latest/serve/advanced-guides/deploy-vm.html#using-a-remote-cluster)
- Add [sutoscaling](https://docs.ray.io/en/latest/serve/autoscaling-guide.html) to your Serve deployment.

```yaml
# Manual autoscaling
# Deploy with a single replica
deployments:
- name: Model
  num_replicas: 1

# Scale up to 10 replicas
deployments:
- name: Model
  num_replicas: 10


# Autoscaling Basic Configuration
- name: Model
  num_replicas: auto

# Equivalent to:
- name: Model
  max_ongoing_requests: 5
  autoscaling_config:
    target_ongoing_requests: 2
    min_replicas: 1
    max_replicas: 100
```
