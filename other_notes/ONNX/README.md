# ONNX (Open Neural Network Exchange)

## Table of Content

- [ONNX (Open Neural Network Exchange)](#onnx-open-neural-network-exchange)
  - [Table of Content](#table-of-content)
  - [Introduction](#introduction)
    - [installation](#installation)
    - [Convert A Pytorch Model to ONNX](#convert-a-pytorch-model-to-onnx)
    - [Inference Using Onnxruntime](#inference-using-onnxruntime)

## Introduction

ONNX (Open Neural Network Exchange) is an open-source AI ecosystem that standardizes the representation of machine learning models. This standardization allows developers to:

- Move models between different frameworks, tools, and hardware.
- Facilitate easier integration and optimization of AI models.
- Train models in one framework and deploy them on others.

ONNX achieves this by providing:

- An extensible computation graph model.
- Built-in operators.
- Standard data types.

### installation

```sh
pip install onnx

# ONNX Runtime
pip install onnxruntime
pip install onnxruntime-gpu
```

### Convert A Pytorch Model to ONNX

```python
import onnx
import torch


model.eval()

# Create dummy inputs with the correct dimensions
# This is based on the model's input requirements
batch_size = 1
seq_length = 300
vocab_size: int = 40_000
num_tokens: int = 20
num_heads: int = 6

# For dates and amounts, use float tensors
dummy_dates = torch.randn(batch_size, seq_length, num_heads, dtype=torch.float32)
dummy_amounts = torch.randn(batch_size, seq_length, dtype=torch.float32)

# For input_ids, use long (integer) tensor with values in range [0, vocab_size-1]
# This is critical as embedding layers require integer indices
dummy_input_ids = torch.randint(
    0, vocab_size, (batch_size, seq_length, num_tokens), dtype=torch.long
)

# Create a tuple of the dummy inputs
dummy_inputs = (dummy_dates, dummy_input_ids, dummy_amounts)

# Export the model
torch.onnx.export(
    model,
    dummy_inputs,
    "model.onnx",
    export_params=True,
    opset_version=13,
    do_constant_folding=True,
    input_names=["dates", "input_ids", "amounts"],
    output_names=["output"],
    dynamic_axes={
        "dates": {0: "batch_size", 1: "seq_length"},
        "input_ids": {0: "batch_size", 1: "seq_length"},
        "amounts": {0: "batch_size", 1: "seq_length"},
        "output": {0: "batch_size"},
    },
)

# Verify the exported model
onnx_model = onnx.load("model.onnx")
onnx.checker.check_model(onnx_model)
```

### Inference Using Onnxruntime

```python
import numpy as np
import onnxruntime as ort
import scipy
from torch.utils.data import DataLoader

# Create ONNX Runtime session
session = ort.InferenceSession(
                              "model.onnx",
                              providers=["CPUExecutionProvider", "CUDAExecutionProvider"]
)

# Original data needs to be converted to the right types
# Dates and amounts as float32
dates_data = np.random.randn(300, 6).astype(np.float32)
amounts_data = np.random.randn(300).astype(np.float32)

# Input_ids as int64 (long) with proper vocabulary range
input_ids_data = np.random.randint(0, 40_000, (300, 20), dtype=np.int64)

# Reshape to add batch dimension
dates_data = dates_data.reshape(1, 300, 6)
input_ids_data = input_ids_data.reshape(1, 300, 20)
amounts_data = amounts_data.reshape(1, 300)


# Run inference with properly typed inputs
outputs = session.run(
    None, {"dates": dates_data, "input_ids": input_ids_data, "amounts": amounts_data}
)

# Making predictions using a dataloader
dataloader: DataLoader = DataLoader(
        dataset, batch_size=max(1, batch_size), shuffle=False
    )

all_probas: list[np.ndarray] = []

# Iterate through batches
for batch in dataloader:
    # Prepare input data for ONNX Runtime
    # shape: (batch_size, max_transactions * n_date_features)
    dates: np.ndarray = (batch["dates"].numpy().astype(np.float32))
    # shape: (batch_size, max_transactions * max_length)
    input_ids: np.ndarray = (batch["input_ids"].numpy().astype(np.int64))
    # shape: (batch_size, max_transactions)
    amounts: np.ndarray = (batch["amounts"].numpy().astype(np.float32))

    # Reshape inputs to match ONNX model expectations
    # shape: (batch_size, max_transactions, n_date_features)
    dates = dates.reshape(dates.shape[0], max_transactions, dates.shape[-1])
    # shape: (batch_size, max_transactions, max_length)
    input_ids = input_ids.reshape(
        input_ids.shape[0], max_transactions, input_ids.shape[-1]
    )
    # shape: (batch_size, max_transactions)
    amounts = amounts.reshape(amounts.shape[0], max_transactions)

    # Run inference
    # First output is logits
    # shape: (batch_size, n_classes)
    logits: np.ndarray = session.run(
        None, {"dates": dates, "input_ids": input_ids, "amounts": amounts}
    )[0]

    # Calculate probabilities
    # shape: (batch_size, n_classes)
    proba: np.ndarray = (
        scipy.special.expit(logits) * 100
    )

    # Store the results
    all_probas.append(proba)

# Combine results
# shape: (n_samples, n_classes)
all_probas_array: np.ndarray = np.concatenate(all_probas, axis=0)
avg_probability: np.ndarray =  np.mean(all_probas_array, axis=0, dtype=np.float16).round(2)
```
