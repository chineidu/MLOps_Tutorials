# GitHub Actions

## Table of Content

- [GitHub Actions](#github-actions)
  - [Table of Content](#table-of-content)
    - [Key Components](#key-components)
      - [Workflow](#workflow)
      - [Job](#job)
      - [Step](#step)
    - [1. A Simple Example](#1-a-simple-example)
      - [Filters](#filters)
      - [Pull Request Trigger](#pull-request-trigger)
      - [Multiple Triggers](#multiple-triggers)

### Key Components

#### Workflow

- It defines what happens when something triggers it, like a push to a specific branch or a tag release.
- A workflow can have one or more jobs.

#### Job

- A job is a unit of work within a workflow.
- It's a series of steps that are executed together on the same runner (a virtual machine provided by GitHub or self-hosted).
- Jobs can run in parallel or sequentially, depending on how you configure them.

#### Step

- A single, specific task within a job.
- It can be:
  - A **shell script**: You write the script directly in your workflow file.
  - **An action:** A reusable piece of code written by someone else (like yourself or the GitHub community) that performs a specific task, like building your code, running tests, or deploying your application.

### 1. A Simple Example

- [Triggers](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#push)

```yaml
name: Example Workflow  # name of the workflow

on:  # trigger(s)
  push:
    branches: [ $default-branch ]  # repository's default branch
  pull_request:
    branches: [ $default-branch ]

jobs:
  build: # name of the job
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4  # action

      - name: Run a one-line script
        run: echo Hello World  # script

      - name: Multi-line script
        run: |  # script
            echo Hello World
            echo something else

```

#### Filters

- If you use both the `branches` filter and the `paths` filter, the workflow will only run when `both` filters are satisfied.
- For example, the following workflow will only run when a push that includes a change to a Python (.py) file is made to a branch whose name starts with releases/:

```yml
on:
  push:
    branches:
      - 'releases/**'
    paths:
      - '**.py'
```

#### Pull Request Trigger

- This workflow is run when a pull request has been `opened` or `reopened`.

```yml
on:
  pull_request:
    types: [opened, reopened]
```

#### Multiple Triggers

```yml
on:
  push:  # trigger 1
    branches:
      - 'dev'
      - 'prod'

  pull_request:  # trigger 2
    branches:
      - 'dev'
      - 'prod'
```

```yml
name: run main.py

on:
  schedule:
    - cron: '0 0 * * 1' # At 00:00 on Monday

jobs:
  build:
    runs-on: ubuntu-latest
    steps:

      - name: checkout repo content
        uses: actions/checkout@v2 # checkout the repository content to github runner

      - name: setup python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9' # install the python version needed

      - name: install python packages
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: execute py script # run main.py
        env:
          SOME_SECRET: ${{ secrets.SOME_SECRET }}
        run: python main.py

      - name: commit files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff-index --quiet HEAD || (git commit -a -m "updated logs" --allow-empty)

      - name: push changes
        uses: ad-m/github-push-action@v0.6.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: main
```
