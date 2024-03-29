# GitHub Actions

- The course can be found on [Udemy](https://www.udemy.com/course/github-actions-the-complete-guide).

## Table of Content

- [GitHub Actions](#github-actions)
  - [Table of Content](#table-of-content)
    - [Expressions](#expressions)
      - [Operators](#operators)
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
      - [Putting It Together (Job Output)](#putting-it-together-job-output)
      - [Dependency Caching](#dependency-caching)
        - [Poetry Caching](#poetry-caching)
    - [Environment Variables](#environment-variables)
      - [Access The Environment Variable(s)](#access-the-environment-variables)
      - [Workflow Level](#workflow-level)
      - [Job Level](#job-level)
      - [Steps Level](#steps-level)
    - [Repository Secrets](#repository-secrets)
      - [Create Repository Secrets](#create-repository-secrets)
      - [Access Repository Secrets](#access-repository-secrets)
    - [Repository Environments](#repository-environments)
      - [Create Repository Environments](#create-repository-environments)
      - [Access Repository Environments](#access-repository-environments)
    - [Controlling Workflow And Job Execution](#controlling-workflow-and-job-execution)
      - [If \[Steps Level\]](#if-steps-level)
      - [Conditional Jobs](#conditional-jobs)
      - [More If Examples](#more-if-examples)
      - [Ignore Errors (Continue-on-error)](#ignore-errors-continue-on-error)
      - [Matrix Strategies](#matrix-strategies)
        - [Include](#include)
        - [Exclude](#exclude)
      - [Reusable Workflow](#reusable-workflow)
        - [Limitations](#limitations)
        - [Create Reusable Workflow](#create-reusable-workflow)
        - [Call The Resuable Workflow](#call-the-resuable-workflow)
        - [Add Inputs To Resusable Workflow](#add-inputs-to-resusable-workflow)
        - [Add Inputs To Workflow Calling The Resusable Workflow](#add-inputs-to-workflow-calling-the-resusable-workflow)
        - [Add Secrets To Resusable Workflow](#add-secrets-to-resusable-workflow)
        - [Add Secrets To Workflow Calling The Resusable Workflow](#add-secrets-to-workflow-calling-the-resusable-workflow)
        - [Add Outputs To Resusable Workflow](#add-outputs-to-resusable-workflow)
        - [Use The Outputs In The Workflow Calling The Resusable Workflow](#use-the-outputs-in-the-workflow-calling-the-resusable-workflow)
        - [Using A Matrix Strategy With A Reusable Workflow](#using-a-matrix-strategy-with-a-reusable-workflow)

### Expressions

- [Docs](https://docs.github.com/en/actions/learn-github-actions/expressions)

#### Operators

- [Docs](https://docs.github.com/en/actions/learn-github-actions/expressions#operators)

[![image.png](https://i.postimg.cc/597FzDKv/image.png)](https://postimg.cc/4ncdk2gN)

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
  - Use the `jobs.<job_id>.outputs` property in your workflow YAML file.
  - Specify key-value pairs, where the key is a string and the value is any supported data type (e.g., string, integer, boolean). i.e. `echo "key=value" >> "$GITHUB_OUTPUT"`
  - e.g. `echo "result1=hello" >> "$GITHUB_OUTPUT"`

```yml
# Define the output
job1:
  runs-on: ubuntu-latest

  # Map a step output to a job output
  outputs:
    output1: ${{ steps.step1.outputs.result1 }}
    output2: ${{ steps.step2.outputs.result2 }}

  steps:
    - id: step1
      run: echo "result1=hello" >> "$GITHUB_OUTPUT"

    - id: step2
      run: echo "result2=world" >> "$GITHUB_OUTPUT"
```

- **Accessing Job Outputs:**
  - In subsequent jobs that depend on the output-producing job, use the `needs` context to access its outputs.
  - The `needs.<job_id>.outputs.<output_key>` syntax retrieves the corresponding value defined in the previous job.
  - Use this retrieved value within your subsequent job's steps for tasks like logging, decision-making, or further processing.

```yml
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

#### Putting It Together (Job Output)

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

##### Poetry Caching

- [Poetry caching](https://github.com/Gr1N/setup-poetry)

```yml
steps:
  - name: Repo Checkout
    uses: actions/checkout@v4

  - name: Python Setup
    uses: actions/setup-python@v5
    with:
      python-version: "3.11"

  - name: Poetry Setup
    uses: Gr1N/setup-poetry@v8

  - name: Poetry Cache Setup
    uses: actions/cache@v4
    with:
      path: ~/.cache/pypoetry/virtualenvs
      key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
```

### Environment Variables

#### Access The Environment Variable(s)

- Linux syntax: `${MY_ENV}`
- GitHub Actions: `${{ env.MY_ENV }}`

#### Workflow Level

```yml
name: Workflow 1  # name of the workflow

on:  # trigger(s)
  push:
    branches: [ dev ]

env: # Workflow env var
  HOST_NAME: localhost

jobs:
  build: # Job 1
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repo Content
        uses: actions/checkout@v4
      ...
```

#### Job Level

```yml
name: Workflow 1  # name of the workflow

on:  # trigger(s)
  push:
    branches: [ dev ]

jobs:
  build: # Job 1

    env: # Job level env var
      HOST_NAME: localhost

    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repo Content
        uses: actions/checkout@v4
      - name: Access Env Var
        run:
          echo ${HOST_NAME}
      ...
```

#### Steps Level

```yml
name: Workflow 1  # name of the workflow

on:  # trigger(s)
  push:
    branches: [ dev ]

jobs:
  build: # Job 1
    runs-on: ubuntu-latest

    steps:
      - name: Use Env Var
        env: # Steps Level env var
          HOST_NAME: localhost
        run:
          echo ${HOST_NAME}

      - name: Checkout Repo Content
        uses: actions/checkout@v4
      ...
```

### Repository Secrets

- [Docs](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-development-environment-secrets-for-your-repository-or-organization)

#### Create Repository Secrets

- Follow the instructions shown below:

[![image.png](https://i.postimg.cc/8CZFwDYG/image.png)](https://postimg.cc/gw6k29dt)

- I created a `secret` with:
  - `key`: **DB_PATH**
  - `value`: **test.db**

#### Access Repository Secrets

```yml
name: Setup Poetry

on:  # trigger(s)
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
env: # Access the secret
  DB_PATH: ${{ secrets.DB_PATH }}
```

### Repository Environments

- [Docs](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)

- Environments are used to **`describe a general deployment target`** like `production`, `staging`, or `development`.
- These environments can include `settings`, `secrets`, and `variables` specific to each environment, enabling you to tailor your deployment process to different stages such as `development`, `staging`, and `production`.
- I can `only` be set within a `job`.

#### Create Repository Environments

[![image.png](https://i.postimg.cc/t47147Cx/image.png)](https://postimg.cc/5Xd9P4z4)

- I created an environment named: `testing` wtih a `secret` variable shown below:
  - `key`: **DB_PATH**
  - `value`: **test.db**

#### Access Repository Environments

```yml
jobs:
  build:  # Job 1
    # Set the environment
    environment: testing
    env:  # Job level
      MY_NAME: ${{ secrets.MY_NAME}}
    runs-on: ubuntu-latest
```

### Controlling Workflow And Job Execution

- For `jobs`, the execution can be controlled using an `if` statement.
- For `steps`, the execution can be controlled using an `if`  or `continue-on-error` statement.

#### If [Steps Level]

- [Steps context docs](https://docs.github.com/en/actions/learn-github-actions/contexts#steps-context)

[![Screenshot-2024-02-02-at-5-50-04-PM.png](https://i.postimg.cc/3NyVnPXN/Screenshot-2024-02-02-at-5-50-04-PM.png)](https://postimg.cc/9whLfgNH)

- Check if the previous step(s) failed:
  - `if: failure() && steps.step_id.outcome == "failure"`

```yml
jobs:
  build:
    steps:
      - name: Repo Checkout
        uses: actions/checkout@v4
      - name: Python Setup
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: Gr1N/setup-poetry@v8
      - name: Poetry Cache Setup
        uses: actions/cache@v4
        with:
          path: ~/.cache/pypoetry/virtualenvs
          key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
      - name: Install Dependencies
        id: install-dependencies
        run: |
          cd my-app && poetry install
          # intentional typo to cause an error!
          lss
      - name: Lint Code
        # Run the step if the prev. step fails.
        if: ${{ failure() }} && steps.install-dependencies.outcome == "failure"
        run: |
          cd my-app
          poetry run mypy . && poetry run ruff . --fix
      - name: Run Code
        run: |
          cd my-app && ls
          poetry run python main.py
          echo DB_PATH: ${{ env.DB_PATH }}
```

#### Conditional Jobs

- For `job2` to run if `job1` failed, `job2` MUST **`depend`** on `job1`.
- It also requires the special `failure()` function.
- i.e. use:
  - `needs`
  - `${{ failure() }}`

```yml
jobs:
  build: # Job 1
    steps:
      - name: Repo Checkout
        uses: actions/checkout@v4
      - name: Python Setup
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

  deploy: # Job 2
    runs-on: ubuntu-latest

    needs: build

    # Run the `deploy` job if the `build` job fails.
    if: ${{ failure() }}

    steps:
      - uses: actions/checkout@v4
      - name: Pytbon Setup
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Deploy Code
        env:  # Step level
          TEXT: Done
        run: |
          echo "Deploying ${TEXT} ... "
```

#### More If Examples

- `actions/cache/vx` docs is shown below:

[![image.png](https://i.postimg.cc/tJpJHBJY/image.png)](https://postimg.cc/sQHsY9pr)

- Configure a step to run if cache was found/used. This is shown below:

```yml
jobs:
  build:  # Job 1
    # Set the environment
    environment: testing
    env: # Workflow level
      DB_PATH: ${{ secrets.DB_PATH }}
    runs-on: ubuntu-latest
    outputs:
      result1: ${{ steps.step1.outputs.result1 }}

    steps:
      - name: Repo Checkout
        uses: actions/checkout@v4
      - name: Python Setup
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: Gr1N/setup-poetry@v8
      - name: Poetry Cache Setup
        id: cache-id
        uses: actions/cache@v4
        with:
          path: ~/.cache/pypoetry/virtualenvs
          key: ${{ runner.os }}-poetry-${{ hashFiles('poetry.lock') }}
      - name: Install Dependencies
        # If the cache was not used. The output of this action is a bool.
        # It ONLY runs this step if the cached file has changed.
        if: steps.cache-id.outputs.cache-hit != "true"
        run: |
          cd my-app && poetry install
          pip list
          echo "dependencies installed by ${MY_NAME}"
      - name: Lint Code
        run: |
          cd my-app
          poetry run mypy . && poetry run ruff . --fix
      - name: Run Code
        run: |
          cd my-app && ls
          poetry run python main.py
          echo DB_PATH: ${{ env.DB_PATH }}
```

#### Ignore Errors (Continue-on-error)

- `continue-on-error` is a property that controls a job's behavior in the face of errors within its steps.
- By default, a job stops execution as soon as any step fails. This is aimed at preventing further errors or unexpected outcomes.
- With `continue-on-error: true`, a job will continue running even if a step fails, allowing subsequent steps to execute.

```yml
jobs:
  build:  # Job 1
    # Set the environment
    environment: testing
    env: # Workflow level
      DB_PATH: ${{ secrets.DB_PATH }}
    runs-on: ubuntu-latest
    outputs:
      result1: ${{ steps.step1.outputs.result1 }}

    steps:
      # A step that might fail!
      - name: Step 1
        runs: |
          echo "Do something interesting"

      - name: Step 2
        # This step runs and the entire workflow does NOT fail!
        continue-on-error: true
        runs: |
          echo "Do something cool"
          echo "Do something super cool"
```

#### Matrix Strategies

- [Docs](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#specifying-a-python-version).
- The `matrix strategy` in GitHub Actions allows you to use variables in a single job definition to automatically create multiple job runs based on the combinations of the variables.
- This is particularly useful when you want to run the `same job` with `different configurations`, such as different versions of software, different operating systems, or other parameters.

```yml
jobs:
  example_matrix:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-20.04]
        python-version: ['3.9', '3.10', '3.11']
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.version }}
```

##### Include

- [Docs](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#expanding-or-adding-matrix-configurations).
- The `include` key is used to expand existing matrix configurations or to add new ones.
- It allows you to dynamically adjust the matrix based on the workflow context.
- The `value` of include is a `list of objects`, and for each object in the include list, a new job run is created with the specified matrix configuration.

```yml
jobs:
  example_matrix:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-20.04]
        python-version: ['3.9', '3.10', '3.11']
        include:
          - python-version: '3.12'
            os: 'windows-latest'
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.version }}
```

##### Exclude

- The `exclude` key is used to exclude specific matrix configurations from the job runs.
- It allows you to specify which matrix configurations should `not` be included in the job runs.
- The exclude key is particularly useful when you want to `exclude certain combinations of matrix variables` from being executed as part of the workflow.

```yml
jobs:
  example_matrix:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-20.04]
        python-version: ['3.9', '3.10', '3.11']
        exclude:
          - python-version: '3.9'
            os: 'ubuntu-22.04'
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.version }}
```

#### Reusable Workflow

- Instead of copying and pasting from one workflow to another, you can make workflows reusable. You and anyone with access to the reusable workflow can then call the reusable workflow from another workflow.
- Reusing workflows avoids duplication.
- Workflow reuse also promotes best practice by helping you to use workflows that are well designed, have already been tested, and have been proven to be effective.

##### Limitations

- [Docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows#limitations)

##### Create Reusable Workflow

- [Docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows#creating-a-reusable-workflow).
- For a workflow to be reusable, the values for on `must` include **`workflow_call`**.

```yml
name: Reusable Workflow
on:
  workflow_call:

jobs:
  deploy:
      runs-on: ubuntu-latest
      steps:
          - name: Output Information
            run: |
              echo "Deploying to prod ..."
```

##### Call The Resuable Workflow

```yml
name: Workflow 2

on:  # trigger(s)
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:  # Job 1
    runs-on: ubuntu-latest
    steps:
      - name: Repo Checkout
        uses: actions/checkout@v4
      - name: Python Setup
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install Dependencies
        run: |
          cd my-app && poetry install
          pip list
          echo "dependencies installed by ${MY_NAME}"

  deploy: # Reusable workflow!
    needs: build
    uses: ./.github/workflows/deploy.yml
```

##### Add Inputs To Resusable Workflow

- [Docs](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onworkflow_callinputs)
- Access Input Variable(s): inputs.key. e.g.
  - `${{ inputs.username }}`

```yml
on:
  workflow_call:
    inputs:
      username:
        description: 'A username passed from the caller workflow'
        default: 'john-doe'
        required: false
        type: string

jobs:
  print-username:
    runs-on: ubuntu-latest

    steps:
      - name: Print the input name to STDOUT
        # Print the username passed from the caller workflow
        run: echo The username is ${{ inputs.username }}
```

##### Add Inputs To Workflow Calling The Resusable Workflow

- Using `with` context.

```yml
deploy: # Reusable workflow!
  needs: build

  uses: ./.github/workflows/deploy.yml
  with: # Add additional params!
    username: Neidu
```

##### Add Secrets To Resusable Workflow

```yml
on:
  workflow_call:
    secrets:
      some-secret:
        required: false

jobs:
  print-username:
    runs-on: ubuntu-latest

    steps:
      - name: Print the input name to STDOUT
        # Print the username passed from the caller workflow
        run: echo The username is ${{ inputs.username }}
```

##### Add Secrets To Workflow Calling The Resusable Workflow

- [Docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-inputs-and-secrets-in-a-reusable-workflow)

- Using `secrets` keyword.

```yml
deploy: # Reusable workflow!
  needs: build

  uses: ./.github/workflows/deploy.yml
  secrets: # Add secrets!
    some-secret: ${{ secrets.SOME_SECRETS}}
```

##### Add Outputs To Resusable Workflow

- [Docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-outputs-from-a-reusable-workflow)

```yml
name: Reusable workflow

on:
  workflow_call:
    # Map the workflow outputs to job outputs
    outputs:
      result1:
        description: "The first output string"
        value: ${{ jobs.deploy.outputs.output1 }}
      result2:
        description: "The second output string"
        value: ${{ jobs.deploy.outputs.output2 }}

jobs:
  deploy:
    name: Generate output
    runs-on: ubuntu-latest
    # Map the job outputs to step outputs
    outputs:
      output1: ${{ steps.step1.outputs.result1 }}
      output2: ${{ steps.step2.outputs.result2 }}
    steps:
      - id: step1
        run: echo "result1=hello" >> $GITHUB_OUTPUT
      - id: step2
        run: echo "result2=world" >> $GITHUB_OUTPUT

```

##### Use The Outputs In The Workflow Calling The Resusable Workflow

- Using `needs` keyword.

```yml
print-result: # Reusable workflow!
  needs: deploy

  uses: ./.github/workflows/deploy.yml
  steps:
    - name: Print Deploy output
      run: echo "${{ needs.deploy.outputs.result1 }}"
```

##### Using A Matrix Strategy With A Reusable Workflow

- [Docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-a-matrix-strategy-with-a-reusable-workflow)

```yml
jobs:
  ReuseableMatrixJobForDeployment:
    strategy:
      matrix:
        target: [dev, stage, prod]
    uses: octocat/octo-repo/.github/workflows/deployment.yml@main
    with:
      target: ${{ matrix.target }}

```
