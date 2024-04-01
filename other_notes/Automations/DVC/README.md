# DVC Tutorial

- [Official Docs](https://dvc.org/doc)

A tutorial on how to use **DVC (Data Version Control)** in your projects to version large data, models, etc.

## Table of Content

- [DVC Tutorial](#dvc-tutorial)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
  - [Initialize DVC](#initialize-dvc)
    - [Track Files](#track-files)
    - [Check Cached Files](#check-cached-files)
    - [Commit Files](#commit-files)
    - [Auto-stage Files](#auto-stage-files)
  - [Add Remote Storage](#add-remote-storage)
    - [Google Drive (Remote Storage)](#google-drive-remote-storage)
    - [Push To Remote](#push-to-remote)
    - [Pull Data From Remote](#pull-data-from-remote)
    - [Push Data To Remote After An Update](#push-data-to-remote-after-an-update)
    - [Remove / Modify Remote Storage](#remove--modify-remote-storage)
    - [Switching between versions](#switching-between-versions)
  - [Delete Files](#delete-files)
    - [Delete Locally](#delete-locally)
    - [Delete Remote File](#delete-remote-file)
  - [**Back To Top**](#back-to-top)
  - [Check Status](#check-status)
    - [Check Files Tracked By DVC In Any Remote Repo](#check-files-tracked-by-dvc-in-any-remote-repo)
    - [Check Files Tracked By DVC In Your Local Repo](#check-files-tracked-by-dvc-in-your-local-repo)
    - [Download Files Tracked By DVC In Your Remote Repo](#download-files-tracked-by-dvc-in-your-remote-repo)
  - [DVC Pipelines](#dvc-pipelines)
    - [Create Parameters (Config)](#create-parameters-config)
    - [Load Config File Using OmegaConf](#load-config-file-using-omegaconf)
    - [DVC Pipeline Setup](#dvc-pipeline-setup)
    - [DVC Dag](#dvc-dag)
    - [Run Pipeline](#run-pipeline)
    - [List The Stages In A Pipeline](#list-the-stages-in-a-pipeline)
  - [**Top**](#top)

## Installation

- Install dvd and other dependencies.

```sh
pip install dvc dvc_gdrive
```

## Initialize DVC

- To initialize dvc, run:

```sh
dvc init
git commit -m "Initialized dvc"
```

### Track Files

- To track the files (data and models) in the `src` directory, run:

```sh
dvc add <path_to_files>

# e.g.
dvc add src/data src/models
```

- Note:
  - It's better to add files individually than to track all files. i.e.

```sh
# Good
dvc add data/file_1.txt data/file_2.txt

# Bad
dvc add data/
```

### Check Cached Files

```sh
tree .dvc/cache
```

### Commit Files

- Git prompts you to add the changes made to the repo. Run:

```sh
git add src/data.dvc src/models.dvc
git commit -m "Add files to be tracked by dvc"
```

### Auto-stage Files

- To autostage changes (i.e git automatically adds files created by dvc), run:

```sh
dvc config core.autostage true
```

## Add Remote Storage

### Google Drive (Remote Storage)

- `-d` or `--default` is used to set the storage as the default storage.
- To add a remote storage, e.g Google Drive, run:

```sh
dvc remote add --default <storage_name> gdrive://<your_folder_id>

# e.g
dvc remote add -d myremote gdrive://0AIac4JZqHhKmUk9PDA
```

### Push To Remote

- Push to the remote storage. It prompts you for authentication

```sh
dvc push  # Assuming there's data to push

git commit -m "Add data"
```

### Pull Data From Remote

- If for some reason, you deleted your data or model files, run:

```sh
dvc pull
```

### Push Data To Remote After An Update

- Making changes to a file, run:

```sh
dvc add data/filename

git commit -m "Dataset updates"
dvc push
```

### Remove / Modify Remote Storage

- To delete or re-authenticate a remote storage, check [docs](https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive#configuration-parameters).
- `Step 1`: For `macOs`, navigate to this path:

```sh
cd ~/Library/Caches
```

- `Step 1`: For `linux`, navigate to this path:

```sh
cd ~/.cache
```

- `Step 2`: Delete the directory:

```sh
# Delete the directory containing the prev. auth
rm -rf pydrive2fs
```

### Switching between versions

- The regular workflow is to use git checkout first (to switch a branch or checkout a `.dvc file` version) and then run dvc checkout to sync data:

```bash
git checkout HEAD~1 data/filename.csv.dvc
dvc checkout
```

Commit it (no need to do `dvc push` this time since this original version of the dataset was already saved). Run:

```bash
git commit -m "Revert dataset updates"
```

## Delete Files

### Delete Locally

- Delete the dvc tracking file. i.e. `.dvc` extension.

```sh
dvc remove <filename>

# e.g.
dvc remove file_1.txt.dvc
```

### Delete Remote File

- This compares the locally tracked files with the remote and deletes the files that don't match.

```sh
# Check remote name
dvc remote list

dvc gc -w
```

---

## **[Back To Top](#table-of-content)**

## Check Status

```sh
dvc status
```

### Check Files Tracked By DVC In Any Remote Repo

- This assumes you're authorized to access the data.

```sh
dvc list <repo_url> <file_directory>

# e.g.
dvc list https://github.com/chineidu/MLOps_Tutorials.git ./data
```

### Check Files Tracked By DVC In Your Local Repo

- This command focuses specifically on DVC-tracked data and provides information about their status:

```sh
# (run this command in your DVC project directory)
dvc data status
```

### Download Files Tracked By DVC In Your Remote Repo

```sh
dvc get <repo_url> <file_directory>

# e.g.
dvc get https://github.com/chineidu/MLOps_Tutorials.git ./data
```

- To download the data and the dvc files for tracking the data

```sh
dvc import <repo_url> <file_directory>

# e.g.
dvc import https://github.com/chineidu/MLOps_Tutorials.git ./data
```

## DVC Pipelines

- A dvc `pipeline` in Data Version Control (`DVC`) refers to a series of automated data processing steps designed to be reproducible and manageable.
- It essentially allows you to define and execute workflows that transform your raw data into the final results you need for tasks like machine learning or data analysis.

### Create Parameters (Config)

- Create a `params.yaml` file for the configuration.

```yaml
# params.yaml
data:
  csv_file_path: ./data/titanic_data.csv
  test_size: 0.2
  random_state: 123
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
```

### Load Config File Using OmegaConf

```py
from omegaconf import DictConfig, OmegaConf

config: DictConfig = OmegaConf.load("./other_notes/Automations/DVC/params.yaml")


csv_file_path: str = config.data.csv_file_path
test_size: float = config.data.test_size
unique_id: str = config.features.unique_id
cat_vars: list[str] = list(config.features.cat_vars)

@typechecked
def prepare_data(config: DictConfig) -> None:
    """This is used to load and split the data."""
    data: pl.DataFrame = pl.read_csv(source=csv_file_path)
    # Add other logic
    ...
```

### DVC Pipeline Setup

- [Docs](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files#stages)
- Create a `dvd.yaml` file containing all required the steps/stages.

```yaml
stages:
  prepare:
    cmd: python3 src/prepare.py
    deps:
      - src/prepare.py
    params:
      - prepare.categories
    outs:
      - data/prepared

  featurize:
    cmd: python3 src/featurize.py data/prepared
    deps:
      - src/featurize.py
      - data/prepared
    outs:
      - data/features

  train_model:
    cmd: python3 src/train.py data/features
    deps:
      - src/train.py
      - data/features
    outs:
      - model.pkl
```

- In this template:
  - Each stage is defined with a unique name (e.g., prepare, featurize, train_model).
  - The `cmd` key specifies the command to be executed for the stage.
  - The `deps` key lists the files or directories that the command depends on.
  - The `params` key specifies any parameters needed for the stage.
  - The `outs` key lists the output files or directories generated by the stage.

### DVC Dag

- It's used to visualize the dependency graph of your data processing pipelines.

```sh
dvc dag
```

### Run Pipeline

- [Docs](https://dvc.org/doc/command-reference/repro#repro)
- Reproduce complete or partial pipelines by running their stages as needed in the correct order.
- It automatically hashes the outputs of each stage in the pipeline.

```sh
dvc repro
```

### List The Stages In A Pipeline

```sh
dvc stage list
```

---

## **[Top](#table-of-content)**
