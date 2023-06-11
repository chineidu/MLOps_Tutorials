# ML Testing And Monitoring

## Table of Contents

- [ML Testing And Monitoring](#ml-testing-and-monitoring)
  - [Table of Contents](#table-of-contents)
  - [Building An ML System Key Phases](#building-an-ml-system-key-phases)
  - [Reasons For Running Tests](#reasons-for-running-tests)
  - [Key Testing Principals For ML (Before Deployment)](#key-testing-principals-for-ml-before-deployment)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
    - [Differential Tests](#differential-tests)

## Building An ML System Key Phases

```text
1. Research Environment
   - Testing different data and features.
   - Testing different algorithms.
   - Testing different hyperparameters.

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
  - Check for sudden degredation.
    * e.g. write tests to check the model's output and predictions using a validation dataset.
    * create lower and upper boundaries that can be used to test the predictions.
  - Check for gradual degredation.
- Apply integration test to the pipeline.
```

### Unit Tests

```text
-
A unit test in ML systems is a type of test that tests a single unit of code, such as a function or class.

- When writing unit tests for ML systems, it is important to keep in mind the following principles:
  - Isolation: Unit tests should test individual units of code in isolation. This means that they should not rely on any external dependencies, such as other functions or classes.
  - Determinism: Unit tests should be deterministic. This means that they should always produce the same results when run with the same input.
  - Repeatability: Unit tests should be repeatable. This means that they should be able to be run multiple times without any changes in results.
  - Fast: Unit tests should be fast. This means that they should be able to be run quickly, so that they can be used frequently during development.
```

### Integration Tests

```text
- An integration test in ML systems is a type of test that tests the interaction between different components of an ML system.

- Integration tests are typically performed after unit tests have been completed and before system tests are performed.

- Integration tests can be used to test a variety of things, such as:
  - The ability of different components to communicate with each other.
  - The accuracy of the results produced by the ML system.
  - The performance of the ML system.
  - The robustness of the ML system to changes in data or input.

- An example of integration test is testing an ML prediction endpoint.
```

```python
@pytest.mark.integration
def test_predict_income(client: TestClient, payload_1: dict[str, Any]) -> None:
    """This is used to test the predict_income enpoint."""
    # Given
    expected = {"status_code": 200}
    URL = "http://0.0.0.0:8000/predict"

    # When
    response = client.post(URL, json=payload_1)
    print(response.json())

    # Then
    assert response.status_code == expected.get("status_code")
    assert response.json().get("predicted_salary") != 0
```

```shell
# Remember to add the custome marker to the config file. (pytest.ini or pyproject.toml).
pytest -vv -m <marker_name>

# e.g
pytest -vv -m integration

# To view all the markers
pytest --markers

# To view all the fixtures
pytest --fixtures
```

### Differential Tests

```text
- Differential test is a type of testing that compares the outputs or behaviors of two different versions or configurations of the same system.

- Differential tests can be used to identify problems with an ML system, such as overfitting or bias.

Here are some examples of how differential tests can be used:
- A developer might use a differential test to compare the performance of two different versions of an ML image classification system. The developer might want to see if the new version of the system is more accurate or faster than the old version.

- A data scientist might use a differential test to compare the performance of an ML natural language processing system on two different sets of data. The data scientist might want to see if the system performs better on data from a particular source, such as social media or news articles.

- Differential testing is particularly useful in scenarios where you have made changes to an ML model or system, such as modifying the architecture, updating the training data, or adjusting hyperparameters. By comparing the outputs of the original version (baseline) and the modified version, you can assess the impact of the changes and determine if they have introduced any unexpected or undesired effects.
```
