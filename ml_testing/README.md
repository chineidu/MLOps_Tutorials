# ML Testing And Monitoring

## Table of Contents

- [ML Testing And Monitoring](#ml-testing-and-monitoring)
  - [Table of Contents](#table-of-contents)
  - [Building An ML System Key Phases](#building-an-ml-system-key-phases)
  - [Reasons For Running Tests](#reasons-for-running-tests)
  - [Key Testing Principals For ML (Before Deployment)](#key-testing-principals-for-ml-before-deployment)

## Building An ML System Key Phases

```text
1. Research Environment
   - Testing different algorithms.
   - Testing different hyperparameters.
   - Testing different data and features.

2. Development Environment
   - Unit tests.
   - Integration tests.
   - Acceptance tests.
     - Reproducible predictions.
     - Validate model quality using differential tests.
   - Benchmark tests. i.e. computational performance
   - Load tests.

3. Production Environment
   - Shadow mode test.
   - Canary releases.
   - Observability and monitoring.
   - Logging and tracing
   - Alerting.
```

## Reasons For Running Tests

```text
Testing code and ML systems is crucial for several reasons:

- Identifying and preventing bugs.

- Ensuring correctness and accuracy.

- Maintaining software quality.

- Promoting collaboration and documentation: Tests act as living documentation for the codebase. They describe the intended behavior of various components, making it easier for developers to understand and collaborate on the project.

- Building confidence and reducing risks: Testing builds confidence in the codebase and reduces the risk of deploying faulty or unreliable software.
```

## Key Testing Principals For ML (Before Deployment)

```text
- Use a schema for the input features (tabular data).
- Test the feature engineering code.
- Test the model config/hyperparams.
- Ensure that the model training is reproducible.
- Validate model quality.
- Apply integration test to the pipeline.
```
