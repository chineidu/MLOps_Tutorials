# GitHub Actions

## Table of Content

- [GitHub Actions](#github-actions)
  - [Table of Content](#table-of-content)
    - [Key Components](#key-components)
      - [Workflow](#workflow)
      - [Job](#job)
      - [Step](#step)
    - [A Simple Example](#a-simple-example)

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

### A Simple Example

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
        run: echo Hello from Octo Organization  # script

```
