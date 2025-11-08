# GLiNER ONNX Export

Convert GLiNER model to ONNX format and quantize for efficient inference.

## Requirements

- Python 3.13+
- torch, gliner, onnxruntime, onnxruntime-quantization

## Usage

Run `0-lab.ipynb` to export model to ONNX and quantize.

Load ONNX model: `GLiNER.from_pretrained("./gliner_small_v_2_p_1_local_onnx", load_onnx_model=True)`

## Files

- `0-lab.ipynb`: Export and test notebook
- `gliner_small_v_2_p_1_local/`: PyTorch model
- `gliner_small_v_2_p_1_local_onnx/`: ONNX model + config
