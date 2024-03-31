# Hydra And OmegaConf

## Table of Content

- [Hydra And OmegaConf](#hydra-and-omegaconf)
  - [Table of Content](#table-of-content)
  - [Hydra](#hydra)
    - [Hydra Installation](#hydra-installation)
    - [Hydra With CLI](#hydra-with-cli)
    - [Hydra: Specify A Config File](#hydra-specify-a-config-file)
    - [Hydra: Update or Add Parameters From The CLI](#hydra-update-or-add-parameters-from-the-cli)
    - [Hydra: Grouping Config Files](#hydra-grouping-config-files)
    - [Hydra: Add Multiple Defaults To Multi Group Config](#hydra-add-multiple-defaults-to-multi-group-config)
  - [OmegaConf](#omegaconf)
    - [OmegaConf Installation](#omegaconf-installation)
    - [Benefits of OmegaConf](#benefits-of-omegaconf)
    - [Load A Config (YAML) File Using OmegaConf](#load-a-config-yaml-file-using-omegaconf)
    - [OmegaConf: Variable Interpolation](#omegaconf-variable-interpolation)
    - [Variable Interpolation With Env Variables](#variable-interpolation-with-env-variables)
    - [OmegaConf: Merge Config Files](#omegaconf-merge-config-files)

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
  - experiment: file1
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

```yaml
# ===================================== #
# config.yaml
# ===================================== #
# Specify the default (important!)
defaults:
  - experiment: file1
  - override experiment: file2
  - _self_ # Every object/key below it becaomes the defaulr

train:
  batch_size: 16
  epochs: 5
  optimizer:
    name: sgd
```

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
# params.yaml
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
# server.yaml
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
  description: Description of ${.address}
  # OR
  # description: Description of ${network2.address}
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
# config_1.yaml
training:
  batch_size: 126
  epochs: 30
  learning_rate: 5e-4

# config_2.yaml
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