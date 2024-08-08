# Poetry Tutorial

- [Official Docs](https://python-poetry.org/docs/)
- [Video Tutorial](https://www.youtube.com/watch?v=0f3moPe_bhk&t=35s&ab_channel=ArjanCodes)

## Table of Content

- [Poetry Tutorial](#poetry-tutorial)
  - [Table of Content](#table-of-content)
  - [Create Virtual Env \[Poetry\]](#create-virtual-env-poetry)
    - [Configure Poetry](#configure-poetry)
      - [Create Virtual ENVs In The Project Directory](#create-virtual-envs-in-the-project-directory)
    - [Create New Project](#create-new-project)
    - [Create New Project \[From exisiting project\]](#create-new-project-from-exisiting-project)
  - [Install Packages](#install-packages)
    - [Default group](#default-group)
    - [Development group](#development-group)
    - [Test group](#test-group)
    - [Install The Packages](#install-the-packages)
  - [Uninstall Packages](#uninstall-packages)
  - [Manage ENVs](#manage-envs)
    - [Check Available ENVs](#check-available-envs)
    - [Check Active ENVs](#check-active-envs)
    - [Deactivate ENVs](#deactivate-envs)
  - [Run Program](#run-program)
    - [Run Program \[Without Shell\]](#run-program-without-shell)
    - [Run Program \[With Shell\]](#run-program-with-shell)
  - [Activate The Virtual Environment](#activate-the-virtual-environment)

## Create Virtual Env [Poetry]

### Configure Poetry

#### Create Virtual ENVs In The Project Directory

```sh
# Virtual ENVs are created in the project directory.
poetry config virtualenvs.in-project true
```

### Create New Project

- Create from scratch.

```sh
poetry new <project-name>

# e.g.
poetry new my-app
```

### Create New Project [From exisiting project]

- Create from exisiting project.

```sh
poetry init
```

## Install Packages

### Default group

```sh
poetry add "package-1==x.x.x" "package-2==x.x.x" "package-3==x.x.x"
```

### Development group

```sh
poetry add --group dev "package-1==x.x.x" "package-2==x.x.x" "package-3==x.x.x"

# e.g.
poetry add --group dev mypy ruff jupyter
```

### Test group

```sh
poetry add --group test "package-1==x.x.x" "package-2==x.x.x" "package-3==x.x.x"

# e.g.
poetry add --group test pytest pytest-cov
```

### Install The Packages

```sh
poetry install

# Fix descrepancies in the lockfile
poetry lock "--no-update" && poetry install
```

## Uninstall Packages

```sh
poetry remove "package-1==x.x.x" "package-2==x.x.x" "package-3==x.x.x"

# e.g.
poetry remove requests dask
```

## Manage ENVs

### Check Available ENVs

- Navigate to the directory where you have a `pyproject.toml` file.

```sh
poetry env info

# Get the path
poetry env info --path
```

### Check Active ENVs

```sh
poetry env list
```

### Deactivate ENVs

```sh
deactivate
```

## Run Program

### Run Program [Without Shell]

```sh
poetry run python filename.py
```

### Run Program [With Shell]

```sh
poetry shell
python filename.py
```

## Activate The Virtual Environment

```sh
# RECOMMENDED
source $(poetry env info --path)/bin/activate

# OR
poetry shell
```
