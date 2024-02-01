# GitHub Actions

## Table of Content

- [GitHub Actions](#github-actions)
  - [Table of Content](#table-of-content)
    - [Key Components](#key-components)
      - [Workflow](#workflow)
      - [Job](#job)
      - [Step](#step)
      - [A Simple Example](#a-simple-example)
      - [Filters](#filters)
      - [Pull Request Trigger](#pull-request-trigger)
      - [Multiple Triggers](#multiple-triggers)
      - [GitHub Actions Marketplace](#github-actions-marketplace)
      - [Adding Multiple Jobs](#adding-multiple-jobs)
      - [Sequential Vs Parallel](#sequential-vs-parallel)
      - [GitHub Actions Context](#github-actions-context)
    - [Using Activity Types](#using-activity-types)
      - [Label Issue](#label-issue)
      - [Pull Request](#pull-request)
      - [Event Filters](#event-filters)
      - [Cancel A Workflow](#cancel-a-workflow)
      - [Skip A Workflow](#skip-a-workflow)
    - [Artifacts](#artifacts)
      - [Upload Artiifacts](#upload-artiifacts)
      - [Download Artiifacts](#download-artiifacts)
      - [Job Outputs](#job-outputs)
      - [Dependency Caching](#dependency-caching)

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

#### A Simple Example

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

#### GitHub Actions Marketplace

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

#### Sequential Vs Parallel

- Sequential jobs can be triggered by adding the keyword: `needs`.

```yml
name: Parallel and Sequential Jobs

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Build Project
      run: |
        echo "Building project ..."

  test_parallel:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Run Parallel Tests
      run: |
        # Your test commands go here
        echo "Running parallel tests ..."

  deploy:
    runs-on: ubuntu-latest

    needs: [build, test_parallel]

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Deploy to Production
      run: |
        # Your deployment commands go here
        echo "Deploying to production"

  test_sequential:
    runs-on: ubuntu-latest

    needs: deploy

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Run Sequential Tests
      run: |
        # Your test commands go here
        echo "Running sequential tests after deployment"
```

#### GitHub Actions Context

- [Official docs](https://docs.github.com/en/actions/learn-github-actions/contexts)

[![image.png](https://i.postimg.cc/Px34sRgy/image.png)](https://postimg.cc/XG5F9Q7B)

- Contexts are a way to access information about workflow runs, variables, runner environments, jobs, and steps.
- Each context is an object that contains properties, which can be strings or other objects.

### Using Activity Types

- [Docs](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow)

#### Label Issue

- e.g, the following workflow uses a personal access token (stored as a secret called MY_TOKEN) to add a label to an issue via GitHub CLI. Any workflows that run when a label is added will run once this step is performed.

```yml
name: Example 1
on:
  issues:
    types:
      - opened

jobs:
  label_issue:
    runs-on: ubuntu-latest
    steps:
      - env:
          GH_TOKEN: ${{ secrets.MY_TOKEN }}
          ISSUE_URL: ${{ github.event.issue.html_url }}
        run: |
          gh issue edit $ISSUE_URL --add-label "triage"
```

#### Pull Request

```yml
name: Example 2
on:
  pull_request: # Event 1
    types:
      - opened
  workflow_dispatched: # Event 2

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Step
        run: |
          echo "Deploying ..."
```

#### Event Filters

- [Docs](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onevent_nametypes)

- `on.<pull_request|pull_request_target>.<branches|branches-ignore>`

```yml
on:
  pull_request:
    # Sequence of patterns matched against refs/heads
    branches:
      - main  # (refs/heads/main)
      - 'dev-*'  # dev-new, dev-this-is-new
      - 'mona/octocat'  # refs/heads/mona/octocat
      - 'releases/**'  # releases/, releases/10 (refs/heads/releases/10)
```

#### Cancel A Workflow

- By default:
  - workflows get cancelled if jobs fail.
  - a job fails if at least one step fails.
- Workflows an also be cancelled manually from the GUI.

#### Skip A Workflow

- [Docs](https://docs.github.com/en/actions/managing-workflow-runs/skipping-workflow-runs)

[![image.png](https://i.postimg.cc/QMfHxG02/image.png)](https://postimg.cc/gw6YN59s)

- e.g. skip a workflow by adding it in your commit message.

```sh
git add .

# Skip workflow
git commit -m "chore: Add comments [skip ci]"

# Push the commit
git push
```

### Artifacts

- [Docs](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)

- In GitHub Actions, artifacts are files or collections of files produced during a workflow run. They act as a way to preserve and share data generated by your workflow after it finishes.

#### Upload Artiifacts

```yml
build:
  runs-on: ubuntu-latest
  steps:
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist-files  # Name of the directory
        path: |
          dist/*.whl  # Upload all .whl files in the dist directory
          reports/*.txt  # Upload any text files in the reports directory
```

#### Download Artiifacts

- It `depends` on the job that uploaded the artifacts.

```yml
deploy:
  runs-on: ubuntu-latest
  needs: build
  steps:
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist-files  # Name of the directory MUST math the name used during upload
    - name: Deploy to server
      run: python deploy.py  # Example deployment script using the artifacts
```

#### Job Outputs

- [Docs](https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs)

- In GitHub Actions, job outputs allow you to share information between separate jobs within a workflow.

- This feature is useful for passing data or results from one job to another.

- **Defining Job Outputs:**
  - Use the jobs.<job_id>.outputs property in your workflow YAML file.
  - Specify key-value pairs, where the key is a string and the value is any supported data type (e.g., string, integer, boolean).
  - Values are evaluated at the end of the job, allowing expressions that utilize job context or outputs from other jobs.

- **Accessing Job Outputs:**
  - In subsequent jobs that depend on the output-producing job, use the `needs` context to access its outputs.
  - The `needs.<job_id>.outputs.<output_key>` syntax retrieves the corresponding value defined in the previous job.
  - Use this retrieved value within your subsequent job's steps for tasks like logging, decision-making, or further processing.

```yml
jobs:

  # Define the output
  job1:
    runs-on: ubuntu-latest
    # Map a step output to a job output
    outputs:
      output1: ${{ steps.step1.outputs.test }}
      output2: ${{ steps.step2.outputs.result }}
    steps:
      - id: step1
        run: echo "test=hello" >> "$GITHUB_OUTPUT"
      - id: step2
        run: echo "result=world" >> "$GITHUB_OUTPUT"

  # Access the output
  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - env:
          OUTPUT1: ${{ needs.job1.outputs.output1 }}
          OUTPUT2: ${{ needs.job1.outputs.output2 }}
        run: echo "$OUTPUT1 $OUTPUT2"
```

#### Dependency Caching

- [Docs: actions/setup-python@v5](https://github.com/actions/setup-python?tab=readme-ov-file#caching-packages-dependencies)

```yml
steps:
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: '3.9'
    cache: 'poetry' # caching poetry dependencies
- run: poetry install
```
