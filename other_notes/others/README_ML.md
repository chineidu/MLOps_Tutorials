# ML CI/CD Pipeline

- [MLOps Roadmap](https://roadmap.sh/mlops)
- This README will contain the best practices for ML CI/CD workflows and pipeline.

## Table of Content

- [ML CI/CD Pipeline](#ml-cicd-pipeline)
  - [Table of Content](#table-of-content)
  - [Template 1](#template-1)
  - [Template 2](#template-2)
    - [1. ML development](#1-ml-development)
    - [2. Training Operationalization](#2-training-operationalization)
    - [3. Continuous Training](#3-continuous-training)
    - [4. Model Deployment](#4-model-deployment)
    - [5. Prediction Serving](#5-prediction-serving)
    - [6. Continuous Monitoring](#6-continuous-monitoring)
    - [7. Data \& Model Management](#7-data--model-management)

## Template 1

[![Screenshot-2024-02-16-at-5-07-22-PM.png](https://i.postimg.cc/vBkDdZR4/Screenshot-2024-02-16-at-5-07-22-PM.png)](https://postimg.cc/5Y5fB12J)

---

## [Template 2](https://webcache.googleusercontent.com/search?q=cache:https://pauliusztin.medium.com/this-is-what-you-need-to-know-to-build-an-mlops-end-to-end-architecture-c0be1deaa3ce)

- [Source](https://webcache.googleusercontent.com/search?q=cache:https://pauliusztin.medium.com/this-is-what-you-need-to-know-to-build-an-mlops-end-to-end-architecture-c0be1deaa3ce)

[![image.png](https://i.postimg.cc/zv43bLLW/image.png)](https://postimg.cc/ZvFJX5xK)

- ML development
- Training operationalization
- Continuous training
- Model deployment
- Prediction serving
- Continuous monitoring
- Data & model management

### 1. ML development

- **Summary**:
  - Extract, transform, Validate and Load (store the preprocessed features) (`ETvL`) the data.
  - Experimenting and developing a robust and reproducible model training procedure (training pipeline code).

- **Main outputs**:
  - The `source code` (versioned by Git or other similar tools).
  - `Data and Model validation`.
  - `Metadata and artifacts` of the experiments (e.g., model weights, data schemas, metrics, samples, predictions, visualizations, etc.)
  - The `configuration files` (hyperparameters, information about the training, validation & testing split, evaluation metrics, and the validation procedure that was used).

### 2. Training Operationalization

- **Summary**:
  - Automating the process of packaging, testing, and deploying repeatable and reliable training pipelines.

- **Main outputs**:
  - `Training-pipeline executable components` (for example, container images stored in a container registry)
  - `CI/CD scripts` that automate the whole process.

### 3. Continuous Training

- **Summary**:
  - Repeatedly executing the training pipeline in response to new data or code changes, or on a schedule.
- **Main outputs**:
  - A `trained and validated model` stored in the model registry.
  - `Training metadata and artifacts` stored in the ML metadata and artifacts repository (pipeline execution parameters, data statistics, data validation results, transformed data files, evaluation metrics, model validation results, and training checkpoints and logs).

### 4. Model Deployment

- **Summary**:
  - Packaging, testing, and deploying a model to a serving environment for online experimentation and production serving.

- **Main outputs**:
  - `Model serving executable application` (for example, a container image
stored in a container registry)
  - `Online experimentation evaluation metrics` stored in ML metadata and
artifact repository.

### 5. Prediction Serving

- **Summary**:
  - After the model is deployed to its target environment, the model service starts to accept prediction requests (serving data) and serve responses with the computed predictions.

- **Main outputs**:
  - `Online inference` in near real-time for high-frequency
requests using interfaces like REST or gRPC;
  - `Streaming inference` in near real-time through an event-processing pipeline;
  - `Offline batch inference` for high volume data processing;
  - `Embedded inference` as part of embedded systems or edge devices.

### 6. Continuous Monitoring

- **Summary**:
  - The process of monitoring the effectiveness and efficiency of a model in production.

- **Main outputs**:
  - `Data` / `Concept drift` detection.
  - `Continuous evaluation & validation` (if GT is available).
  - A `dashboard` where you can visualize/monitor the state of the production system. (`Resource utilization` such as CPUs, GPUs, memory, etc.)
  - An `alarm system` will send various signals based on a set of thresholds.

### 7. Data & Model Management

- **Summary**:
  - It is a central function for governing ML artifacts to
support traceability, shareability, reusability and , discoverability.

- **Main outputs**:
  - `Dataset` repository.
  - `Feature` repository.
  - `ML metadata` & artifact repository.
  - `Model` registry.
