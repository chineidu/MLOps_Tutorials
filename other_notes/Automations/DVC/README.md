# DVC Tutorial

- [Official Docs](https://dvc.org/doc)

A tutorial on how to use **DVC (Data Version Control)** in your projects to version large data, models, etc.

## Table of Content

- [DVC Tutorial](#dvc-tutorial)
  - [Table of Content](#table-of-content)
  - [Initialize DVC](#initialize-dvc)
    - [Track Files](#track-files)
    - [Commit Files](#commit-files)
    - [Auto-stage Files](#auto-stage-files)
  - [Add Remote Storage](#add-remote-storage)
    - [Google Drive (Remote Storage)](#google-drive-remote-storage)
    - [Pull Data From Remote](#pull-data-from-remote)
    - [Push Data To Remote After An Update](#push-data-to-remote-after-an-update)
    - [Switching between versions](#switching-between-versions)

## Initialize DVC

- To initialize dvc, run:

```bash
dvc init
git commit -m "Initialized dvc"
```

### Track Files

- To track the files (data and models) in the `src` directory, run:

```bash
dvc add <path_to_files>

# e.g.
dvc add src/data src/models
```

### Commit Files

- Git prompts you to add the changes made to the repo. Run:

```bash
git add src/data.dvc src/models.dvc
git commit -m "Add files to be tracked by dvc"
```

### Auto-stage Files

- To autostage changes (i.e git automatically adds files created by dvc), run:

```bash
dvc config core.autostage true
```

## Add Remote Storage

### Google Drive (Remote Storage)

- To add a remote storage, e.g Google Drive, run:

```bash
dvc remote add --default <storage_name> gdrive://<your_folder_id>

# e.g
dvc remote add -d myremote gdrive://0AIac4JZqHhKmUk9PDA

# Push to the remote storage
dvc push  # Assuming there's data to push

git commit -m "Add data"
```

### Pull Data From Remote

- If for some reason, you deleted your data or model files, run:

```bash
dvc pull
```

### Push Data To Remote After An Update

- Making changes to a file, run:

```bash
dvc add data/filename

git commit -m "Dataset updates"
dvc push
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
