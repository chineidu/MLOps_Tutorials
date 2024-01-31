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
    - [GitHub Actions Marketplace](#github-actions-marketplace)
      - [Adding Multiple Jobs](#adding-multiple-jobs)

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
name: Example Workflow  # Name of the workflow

on:  # Trigger(s)
  push:
    branches: [ $default-branch ]  # repository's default branch
  pull_request:
    branches: [ $default-branch ]

jobs:
  build: # Name of the job. It can be any name
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4  # Action

      - name: Run a one-line script
        run: echo Hello World  # Script

      - name: Multi-line script
        run: |  # Script
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

### GitHub Actions Marketplace

- [Actions marketplace](https://github.com/marketplace?type=actions)

#### Adding Multiple Jobs

```yml
name: Workflow 1  # name of the workflow

on:  # trigger(s)
  push:
    branches: [ main ]

  pull_request:
    branches: [ main ]

jobs:
  build: # Job 1
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo content
        uses: actions/checkout@v4  # action

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |  # script
          echo ">>> Installing dependencies ... <<<"
          pip install rich typeguard

      - name: Example Code
        run: |
          echo ">>> Running ... <<<"
          python other_notes/Python_classes_notes/src/main.py

  deploy: # Job 2
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo content
        uses: actions/checkout@v4  # action

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |  # script
          echo ">>> Installing dependencies ... <<<"
          pip install rich typeguard

      - name: Deploy
        run: |
          echo ">>> Deploying code to production ... <<<"

```
