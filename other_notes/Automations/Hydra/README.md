# OmegaConf And Hydra

- [Course](https://www.udemy.com/course/sustainable-and-scalable-machine-learning-project-development)

## Table of Content

- [OmegaConf And Hydra](#omegaconf-and-hydra)
  - [Table of Content](#table-of-content)
  - [OmegaConf](#omegaconf)
    - [OmegaConf Installation](#omegaconf-installation)
    - [Benefits of OmegaConf](#benefits-of-omegaconf)
    - [Load A Config (YAML) File Using OmegaConf](#load-a-config-yaml-file-using-omegaconf)
    - [OmegaConf: Variable Interpolation](#omegaconf-variable-interpolation)
    - [Variable Interpolation With Env Variables](#variable-interpolation-with-env-variables)
    - [OmegaConf: Merge Config Files](#omegaconf-merge-config-files)
  - [**Back To Top**](#back-to-top)
  - [Hydra](#hydra)
    - [Hydra Installation](#hydra-installation)
    - [Hydra With CLI](#hydra-with-cli)
    - [Hydra: Specify A Config File](#hydra-specify-a-config-file)
    - [Hydra: Update or Add Parameters From The CLI](#hydra-update-or-add-parameters-from-the-cli)
    - [Hydra: Grouping Config Files](#hydra-grouping-config-files)
    - [Hydra: Add Multiple Defaults To Multi Group Config](#hydra-add-multiple-defaults-to-multi-group-config)
    - [Hydra: Create Packages Using Default Lists](#hydra-create-packages-using-default-lists)
    - [Hydra: Multirun](#hydra-multirun)
      - [Using Glob Pattern](#using-glob-pattern)
    - [Hydra: Debugging](#hydra-debugging)
    - [View The Contents of A Package](#view-the-contents-of-a-package)
    - [Hydra: Instantiate Objects](#hydra-instantiate-objects)
    - [Hydra: Install Tab Completion](#hydra-install-tab-completion)
    - [Hydra: Create Configs Using Structured-Configs](#hydra-create-configs-using-structured-configs)
    - [Hydra: Validate Configs Using Schema](#hydra-validate-configs-using-schema)
  - [**Top**](#top)

## OmegaConf

### OmegaConf Installation

```sh
pip install omegaconf
```

- `OmegaConf` is a library for managing configurations in Python. It's designed to be flexible and handle configurations from various sources:
  - YAML files (a common configuration format)
  - Python dataclasses (structured data containers)
  - Regular Python objects
  - Command-line arguments

### Benefits of OmegaConf

- OmegaConf offers these key benefits:
  - **Hierarchical structure**: Configurations are organized in a tree-like manner, making them easy to navigate and understand.
  - **Merging capabilities**: It can combine configurations from different sources, allowing you to set defaults and override them with specific settings.
  - **Consistent API**: Regardless of the source, you interact with the configuration using the same methods and properties.

### Load A Config (YAML) File Using OmegaConf

```yaml
# ===================================== #
# params.yaml
# ===================================== #
data:
  csv_file_path: ./data/titanic_data.csv
  test_size: 0.25
  random_state: 20
  target: survived
  train_save_path: ./data/artifacts/train.parquet
  test_save_path: ./data/artifacts/test.parquet

features:
  unique_id: name
  cat_vars:
    - embarked
    - sex
  cols_to_drop:
    - boat
    - body
    - cabin
    - home.dest
  transform_output: pandas
  train_features_save_path: ./data/artifacts/train_features.parquet
  test_features_save_path: ./data/artifacts/test_features.parquet
  train_target_save_path: ./data/artifacts/train_target.parquet
  test_target_save_path: ./data/artifacts/test_target.parquet

evaluate:
  metrics_save_path: ./data/metrics/results.yaml
```

- From the Python file, set up the following:

```py
from omegaconf import DictConfig, OmegaConf

# Load config
config: DictConfig = OmegaConf.load("./params.yaml")

# Access the parameters
penalty: str = config.train.penalty
C: float = config.train.C
random_state: int = config.data.random_state
solver: str = config.train.solver

def train(config: DictConfig) -> None:
    """This is used to prepare the data."""
    X_train: pd.DataFrame = pd.read_parquet(path=config.features.train_features_save_path)
    X_test: pd.DataFrame = pd.read_parquet(path=config.features.test_features_save_path)
    # Other logic
    ...

if __name__ == "__main__":
    train(config=config)
```

### OmegaConf: Variable Interpolation

```yaml
# ===================================== #
# server.yaml
# ===================================== #
# Server general information
server:
  name: my_server  # Replace with your server name
  description: This is a basic server configuration.

# Network configuration
network:
  # Replace with your actual IP address
  address: 192.168.1.100
  port: 8080  # Common port for web servers, adjust as needed

network2:
  address: ${network.address}
  description: Description of ${.address} # relative path
  # OR
  # description: Description of ${network2.address} # abs path
```

```py
@hydra.main(config_path=".", config_name="server", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config, resolve=True))


if __name__ == "__main__":
    main()
```

- To display the variable interpolation, add `resolve=True`.
- On the CLI run:

```sh
python main.py

# Output:
server:
  name: my_server
  description: This is a basic server configuration.
network:
  address: 192.168.1.100
  port: 8080
network2:
  address: 192.168.1.100
  description: Description of 192.168.1.100
```

### Variable Interpolation With Env Variables

```yaml
auth:
  type: basic  # Choose authentication type (basic, token, etc.)
  username: ${oc.env:ENV_NAME}
  password: ${oc.env:ENV_PASSWORD,password123}
```

- Access the env vars using `oc.env:`
- Set default env values using: `${oc.env:ENV_PASSWORD,your_default_value}`. e.g. `${oc.env:ENV_PASSWORD,password123}`

```py
import os

@hydra.main(config_path=".", config_name="server", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    # Add env variables
    os.environ["ENV_NAME"] = "neidu"

    console.print(OmegaConf.to_yaml(config, resolve=True))


if __name__ == "__main__":
    main()
```

- Output:

```sh
python main.py

# Output
# auth:
#   type: basic
#   username: neidu
#   password: password123
```

### OmegaConf: Merge Config Files

```yaml
# ===================================== #
# config_1.yaml
# ===================================== #
training:
  batch_size: 126
  epochs: 30
  learning_rate: 5e-4

# ===================================== #
# config_2.yaml
# ===================================== #
server:
  name: my_server  # Replace with your server name
  description: This is a basic server configuration.
```

```py
def main() -> None:
    """Main function"""
    config_1: DictConfig = OmegaConf.load("config.yaml")
    config_2: DictConfig = OmegaConf.load("server.yaml")
    config: DictConfig = OmegaConf.merge(config_1, config_2)

    console.print(OmegaConf.to_yaml(config, resolve=True))


if __name__ == "__main__":
    config: DictConfig = OmegaConf.load("server.yaml")
    main()
```

- Output:

```sh
python main.py

# output:
# training:
#   batch_size: 126
#   epochs: 30
#   learning_rate: 5e-4
# server:
#   name: my_server  # Replace with your server name
#   description: This is a basic server configuration.
```

---

## **[Back To Top](#table-of-content)**

## Hydra

- Hydra (Python) simplifies complex app development. It excels at dynamically creating hierarchical configurations and overriding them via YAML files or command line.
- It is great for experiments or complex applications.
- It also integrates with OmegaConf for powerful configuration management.

### Hydra Installation

```sh
pip install hydra-core
```

### Hydra With CLI

```py
import hydra
from omegaconf import DictConfig, OmegaConf
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "#76FF7B",
        "warning": "#FBDDFE",
        "error": "#FF0000",
    }
)
console = Console(theme=custom_theme)


@hydra.main(config_path=None, version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config))


if __name__ == "__main__":
    main()
```

- Since no config file was specified, `config_path`=None
- To add parameters via the cli, type `+your_param=your_value`

```sh
python main.py +solver=lbfgs +penalty=l1

# output:
# solver: lbfgs
# penalty: l1
```

### Hydra: Specify A Config File

```py
@hydra.main(config_path=".", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config))


if __name__ == "__main__":
    main()
```

- Specify the `config_path`. If it's in the same directory, `config_path="."`
- Add the name of the config file without the extension. i.e. , `config_name='config'`

### Hydra: Update or Add Parameters From The CLI

```yaml
# config.yaml
training:
  batch_size: 126
  epochs: 30
  learning_rate: 5e-4
```

```sh
# No need to add `+` since the key already exists
python main.py training.batch_size=64

# Output:
# training:
#   batch_size: 64  # This changed!
#   epochs: 30
#   learning_rate: 5e-4
```

### Hydra: Grouping Config Files

- To group your config files, you need to create a directory with this file structure:

```text
mainDir               # it can be any name
├── config.yaml       # it can be any name
└── subDir            # it can be any name
    ├── file1.yaml
    └── file2.yaml
    └── ...
    └── fileN.yaml
```

- Create the files and the sub directories.

```yaml
# ===================================== #
# file1.yaml
# ===================================== #
model:
  name: resnet18
# Training configuration
train:
  batch_size: 32
  epochs: 80
  optimizer:
    name: adam
    learning_rate: 0.001

# ===================================== #
# file2.yaml
# ===================================== #
model:
  name: resnet50

# Training configuration
train:
  batch_size: 16
  epochs: 100
  optimizer:
    name: adam
    learning_rate: 0.001


# ===================================== #
# config.yaml
# ===================================== #
# Specify the default (important!)
defaults:
  - subDir: file1
```

```py
@hydra.main(config_path="mainDir", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config, resolve=True))

if __name__ == "__main__":
    main()
```

### Hydra: Add Multiple Defaults To Multi Group Config

- This can be done by using `override`
- Using `_self_` key, you can update the default key/object. i.e. Any key/object that comes after `_self_` becomes the default!
- You can also merge a config file by adding it as a default list.

```yaml
# ===================================== #
# another_config_file.yaml
# ===================================== #
some_values:
  n_estimators: 30
  model_name: "light gbm"


# ===================================== #
# config.yaml
# ===================================== #
# Specify the default (important!)
defaults:
  - subDir: file1
  # - override subDir: file2
  - subDir2: server2
  - another_config_file # This merges the file
  - _self_ # Every object/key below it becomes the default

train:
  batch_size: 16
  epochs: 5
  optimizer:
    name: sgd
```

### Hydra: Create Packages Using Default Lists

- Create a new package by copying the contents on an existing package.
- e.g. `experiment@neidu: exp-with-resnet50`
  - This creates a new object named `neidu` and populates the object with the contents of `exp-with-resnet50.yaml`

```yaml
# ===================================== #
# config.yaml
# ===================================== #
# Specify the default (important!)
defaults:
  - experiment: exp-with-resnet18
  - loss_function: mseLoss
  - experiment@neidu: exp-with-resnet50
  - _self_ # Every object/key below it becomes the default


experiment:
  optimizer:
    name: sgd
```

```sh
# Outputs:
# neidu:
#   model:
#     name: resnet50
#   train:
#     batch_size: 16
#     epochs: 100
#     optimizer:
#       name: adam
#       learning_rate: 0.001
#   data:
#     train_dir: /path/to/your/training/data
#     val_dir: /path/to/your/validation/data
```

### Hydra: Multirun

- You can run a script with multiple config files at the same time.
- This is done using the `-m` or `--multirun` flag.

```sh
python main.py -m subDir=file1,file2  subDir2=server2,server3,server5

# Another example
python main.py -m experiment=exp-with-resnet18,exp-with-resnet50 loss_function=mseLoss
```

#### Using Glob Pattern

```sh
python main.py -m experiment="glob(*)"

# Exclude some files
python main.py -m subDir="glob(*, exclude=file2)"
```

### Hydra: Debugging

- To view the `content` of the `config file` that was run, run:

```sh
python main.py --cfg job
```

- To view the `content` of the `Hydra` default config  that was run, enter the cmd:

```sh
python main.py --cfg hydra
```

### View The Contents of A Package

- This is used to view the content of the config file within a sub-directory/package.
- This is done with the `-p` or `--package` flag.

```sh
python main.py --cfg job --package subDir
```

### Hydra: Instantiate Objects

- This is used to instantiate objects using the definitions in the yaml/config files.
- This is done with the `instantiate` function and  `_target_` key.
- `_target_` points to the location of the `Python class` to be instantiated.
  - e.g.  _target_: main.Training means go to `main.py` and locate the class: `Taining`.
- `_partial_` key can be used to partially init an object that requires additional data during init. i.e. `_partial_=true`

```yaml
# ===================================== #
# config.yaml
# ===================================== #
training:
  _target_: main.Training
  _partial_=true
  batch_size: 126
  epochs: 30
  learning_rate: 5e-4

log_model:
  _target_: sklearn.linear_model.LogisticRegression
  _partial_: true
  C: 0.5
  penalty: "l2"
  solver: "liblinear"
```

```py
import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

class Training:
    def __init__(self, batch_size: int, epochs: int, learning_rate: float) -> None:
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(batch_size={self.batch_size}, "
            f"epochs={self.epochs}, learning_rate={self.learning_rate})"
        )


@hydra.main(config_path=".", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    training_hydra: DictConfig = instantiate(config.training)
    log_model: DictConfig = instantiate(config.log_model)

    console.print(training_hydra)
    console.print(log_model)


if __name__ == "__main__":
    main()
```

```sh
# Outpur
# Training(batch_size=126, epochs=30, learning_rate=0.0005)
# functools.partial(<class 'sklearn.linear_model._logistic.LogisticRegression'>, C=0.5, penalty='l2', solver='liblinear')
```

### Hydra: Install Tab Completion

- [official docs](https://hydra.cc/docs/1.2/tutorials/basic/running_your_app/tab_completion/#zsh-instructions)
- You can install tab completion by using `--hydra-help` and following the instructions.

```sh
python file_name.py --hydra-help

# Run: You may need to restart the shell
eval "$(python main.py -sc install=bash)"
```

### Hydra: Create Configs Using Structured-Configs

- The following line are used to init the ConfigStore

```text
cs = ConfigStore.instance()
cs.store(name="config", node=ExperimentConfig)
```

```py
from dataclasses import dataclass
import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class ExperimentConfig:
    model: str = "resnet18"
    epochs: int = 30
    learning_rate: float = 5e-3

# Setup the config store
cs = ConfigStore.instance()
cs.store(name="config", node=ExperimentConfig)

@hydra.main(config_path=None, config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config, resolve=True))

if __name__ == "__main__":
    main()
```

```sh
python main.py

# Outputs:
# model: resnet18
# epochs: 30
# learning_rate: 0.005
```

### Hydra: Validate Configs Using Schema

```yaml
# ===================================== #
# config.yaml
# ===================================== #
defaults:
  - _self_
  - main_config_schema # schema

training:
  _target_: main.Training
  batch_size: 126
  epochs: 30
  learning_rate: 5e-4

log_model:
  _target_: sklearn.linear_model.LogisticRegression
  _partial_: true
  C: 0.5
  penalty: "l2"
  solver: "liblinear"
```

- Add the schema to the default lists. i.e. `main_config_schema`

```py
from dataclasses import dataclass
# OR
from pydantic.dataclasses import dataclass # Better!
import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf

@dataclass
class TrainingSchema:
    _target_: str
    batch_size: int
    epochs: int
    learning_rate: float


@dataclass
class LogModelSchema:
    _target_: str
    _partial_: bool
    C: float
    penalty: str
    solver: str


@dataclass
class MainConfigSchema:
    training: TrainingSchema
    log_model: LogModelSchema


# Setup the config store
cs = ConfigStore.instance()
cs.store(name="main_config_schema", node=MainConfigSchema)
# Add groups
# cs.store(group="experiments", name="resnet18_schema, node=ResNet18)


@hydra.main(config_path=".", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function"""
    console.print(OmegaConf.to_yaml(config, resolve=True))


if __name__ == "__main__":
    main()

```

---

## **[Top](#table-of-content)**
