# Running DeepSeek-R1-0528 (FP8 Hybrid) with KTransformers

This guide provides instructions to run the DeepSeek-R1-0528 model locally using a hybrid FP8 (GPU) and Q4_K_M GGUF (CPU) approach with KTransformers, managed via Docker. This setup is optimized for high-end hardware (e.g., NVIDIA RTX 4090, high-core count CPU, significant RAM).

**Model Version:** DeepSeek-R1-0528
**KTransformers Version (Working):** `approachingai/ktransformers:v0.2.4post1-AVX512`

## Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Model Preparation](#model-preparation)
    *   [Step 2a: Download FP8 Base Model (Host)](#step-2a-download-fp8-base-model-host)
    *   [Step 2b: Download Q4\_K\_M GGUF Model (Host)](#step-2b-download-q4_k_m-gguf-model-host)
    *   [Step 2c: Merge Models (Inside Docker)](#step-2c-merge-models-inside-docker)
    *   [Step 2d: Set Ownership & Permissions (Host)](#step-2d-set-ownership--permissions-host)
3.  [Running the Model with KTransformers](#running-the-model-with-ktransformers)
    *   [Single GPU (e.g., 1x RTX 4090)](#single-gpu-eg-1x-rtx-4090)
    *   [Multi-GPU (e.g., 2x RTX 4090)](#multi-gpu-eg-2x-rtx-4090)
4.  [Testing the Server](#testing-the-server)
5.  [Key Server Parameters](#key-server-parameters)
6.  [Notes on KTransformers v0.3.1](#notes-on-ktransformers-v031)
7.  [Available Optimize Config YAMLs (for reference)](#available-optimize-config-yamls-for-reference)
8.  [Troubleshooting Tips](#troubleshooting-tips)

---

## 1. Prerequisites

*   **Hardware:**
    *   NVIDIA GPU with FP8 support (e.g., RTX 40-series, Hopper series).
    *   High core-count CPU (e.g., Intel Xeon, AMD Threadripper).
    *   Significant System RAM (ideally 512GB for larger GGUF experts and context). The Q4_K_M experts for a large model can consume 320GB+ alone.
    *   Fast SSD (NVMe recommended) for model storage.
*   **Software (on Host):**
    *   Linux OS (Ubuntu 24.04 LTS recommended).
    *   NVIDIA Drivers (ensure they are up-to-date and support your GPU and CUDA version).
    *   Docker Engine.
    *   NVIDIA Container Toolkit (for GPU access within Docker).
    *   Conda or a Python virtual environment manager.
    *   Python 3.9+
    *   `huggingface_hub` and `hf_transfer`
    *   Git (for cloning KTransformers if you need to inspect YAMLs or contribute).

---

## 2. Model Preparation

We assume your models will be downloaded and stored under `/home/mukul/dev-ai/models` on your host system. This path will be mounted into the Docker container as `/models`. Adjust paths if your setup differs.

### Step 2a: Download FP8 Base Model (Host)

Download the official DeepSeek-R1-0528 FP8 base model components.


```bash
# Ensure that correct packages are installed. Conda is recommended for environemnt management.
pip install -U huggingface_hub hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1 # For faster downloads

# Define your host model directory
HOST_MODEL_DIR="/home/mukul/dev-ai/models"
BASE_MODEL_HF_ID="deepseek-ai/DeepSeek-R1-0528"
LOCAL_BASE_MODEL_PATH="${HOST_MODEL_DIR}/${BASE_MODEL_HF_ID}"

mkdir -p "${LOCAL_BASE_MODEL_PATH}"

echo "Downloading base model to: ${LOCAL_BASE_MODEL_PATH}"
huggingface-cli download --resume-download "${BASE_MODEL_HF_ID}" \
  --local-dir "${LOCAL_BASE_MODEL_PATH}"```

### Step 2b: Download Q4\_K\_M GGUF Model (Host)

Download the Unsloth Q4\_K\_M GGUF version of DeepSeek-R1-0528 using the attached python script.
### Step 2c: Merge Models (Inside Docker)

This step uses the KTransformers Docker image to merge the FP8 base and Q4\_K\_M GGUF weights.

```bash
docker stop ktransformers
docker run --rm --gpus '"device=1"' \
  -v /home/mukul/dev-ai/models:/models \
  --name ktransformers \
  -itd approachingai/ktransformers:v0.2.4post1-AVX512

docker exec -it ktransformers /bin/bash
```

```bash
python merge_tensors/merge_safetensor_gguf.py \
  --safetensor_path /models/deepseek-ai/DeepSeek-R1-0528 \
  --gguf_path /models/unsloth/DeepSeek-R1-0528-GGUF/Q4_K_M \
  --output_path /models/mukul/DeepSeek-R1-0528-GGML-FP8-Hybrid/Q4_K_M_FP8
```


### Step 2d: Set Ownership & Permissions (Host)

After Docker creates the merged files, fix ownership and permissions on the host.

```bash
HOST_OUTPUT_DIR_QUANT="/home/mukul/dev-ai/models/mukul/DeepSeek-R1-0528-GGML-FP8-Hybrid/Q4_K_M_FP8" # As defined above

echo "Setting ownership for merged files in: ${HOST_OUTPUT_DIR_QUANT}"
sudo chown -R $USER:$USER "${HOST_OUTPUT_DIR_QUANT}"
sudo find "${HOST_OUTPUT_DIR_QUANT}" -type f -exec chmod 664 {} \;
sudo find "${HOST_OUTPUT_DIR_QUANT}" -type d -exec chmod 775 {} \;

echo "Ownership and permissions set. Verification:"
ls -la "${HOST_OUTPUT_DIR_QUANT}"
```

---

## 3. Running the Model with KTransformers

Ensure the Docker image `approachingai/ktransformers:v0.2.4post1-AVX512` is pulled.

### Single GPU (e.g., 1x RTX 4090)

**1. Start Docker Container:**

```bash
# Stop any previous instance
docker stop ktransformers || true # Allow if not running
docker rm ktransformers || true   # Allow if not existing

# Define your host model directory
HOST_MODEL_DIR="/home/mukul/dev-ai/models"
TARGET_GPU="1" # Specify GPU ID, e.g., "0", "1", or "all"

docker run --rm --gpus "\"device=${TARGET_GPU}\"" \
  -v "${HOST_MODEL_DIR}:/models" \
  -p 10002:10002 \
  --name ktransformers \
  -itd approachingai/ktransformers:v0.2.4post1-AVX512

docker exec -it ktransformers /bin/bash
```

**2. Inside the Docker container shell, launch the server:**

```bash
# Set environment variable for PyTorch CUDA memory allocation
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
CONTAINER_MERGED_MODEL_PATH="/models/mukul/DeepSeek-R1-0528-GGML-FP8-Hybrid/Q4_K_M_FP8"
CONTAINER_BASE_MODEL_CONFIG_PATH="/models/deepseek-ai/DeepSeek-R1-0528"

# Launch server
python3 ktransformers/server/main.py \
    --gguf_path "${CONTAINER_MERGED_MODEL_PATH}" \
    --model_path "${CONTAINER_BASE_MODEL_CONFIG_PATH}" \
    --model_name KVCache-ai/DeepSeek-R1-0528-q4km-fp8 \
    --cpu_infer 57 \
    --max_new_tokens 16384 \
    --cache_lens 24576 \
    --cache_q4 true \
    --temperature 0.6 \
    --top_p 0.95 \
    --optimize_config_path ktransformers/optimize/optimize_rules/DeepSeek-V3-Chat-fp8-linear-ggml-experts.yaml \
    --force_think \
    --use_cuda_graph \
    --host 0.0.0.0 \
    --port 10002
```
*Note: The `--optimize_config_path` still refers to a `DeepSeek-V3` YAML. This V3 config is compatible and recommended.

### Multi-GPU (e.g., 2x RTX 4090)

**1. Start Docker Container:**

```bash
# Stop any previous instance
docker stop ktransformers || true
docker rm ktransformers || true

# Define your host model directory
HOST_MODEL_DIR="/home/mukul/dev-ai/models"
TARGET_GPUS="0,1" # Specify GPU IDs

docker run --rm --gpus "\"device=${TARGET_GPUS}\"" \
  -v "${HOST_MODEL_DIR}:/models" \
  -p 10002:10002 \
  --name ktransformers \
  -itd approachingai/ktransformers:v0.2.4post1-AVX512

docker exec -it ktransformers /bin/bash
```

**2. Inside the Docker container shell, launch the server:**
```bash
# Set environment variable (optional for multi-GPU, but can be helpful)
# export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True 

# Define container paths
CONTAINER_MERGED_MODEL_PATH="/models/mukul/DeepSeek-R1-0528-GGML-FP8-Hybrid/Q4_K_M_FP8"
CONTAINER_BASE_MODEL_CONFIG_PATH="/models/deepseek-ai/DeepSeek-R1-0528"

# Launch server
python3 ktransformers/server/main.py \
    --gguf_path "${CONTAINER_MERGED_MODEL_PATH}" \
    --model_path "${CONTAINER_BASE_MODEL_CONFIG_PATH}" \
    --model_name KVCache-ai/DeepSeek-R1-0528-q4km-fp8 \
    --cpu_infer 57 \
    --max_new_tokens 24576 \
    --cache_lens 32768 \
    --cache_q4 true \
    --temperature 0.6 \
    --top_p 0.95 \
    --optimize_config_path ktransformers/optimize/optimize_rules/DeepSeek-V3-Chat-multi-gpu-fp8-linear-ggml-experts.yaml \
    --force_think \
    --use_cuda_graph \
    --host 0.0.0.0 \
    --port 10002
```
*Note: The `--optimize_config_path` still refers to a `DeepSeek-V3` YAML. Verify compatibility.*

---

## 4. Testing the Server

Once the server is running inside Docker (look for "Uvicorn running on http://0.0.0.0:10002"), open a **new terminal on your host machine** and test with `curl`:

```bash
curl http://localhost:10002/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "KVCache-ai/DeepSeek-R1-0528-q4km-fp8",
        "messages": [{"role": "user", "content": "Explain the concept of Mixture of Experts in large language models in a simple way."}],
        "max_tokens": 250,
        "temperature": 0.6,
        "top_p": 0.95
    }'
```
A JSON response containing the model's output indicates success.

---

## 5. Key Server Parameters

*   `--gguf_path`: Path inside the container to your **merged** hybrid model files.
*   `--model_path`: Path inside the container to the **original base model's** directory (containing `config.json`, `tokenizer.json`, etc.). KTransformers needs this for model configuration.
*   `--model_name`: Arbitrary name for the API endpoint. Used in client requests.
*   `--cpu_infer`: Number of CPU threads for GGUF expert inference. Tune based on your CPU cores (e.g., `57` for a 56-core/112-thread CPU might leave some cores for other tasks, or you could try higher).
*   `--max_new_tokens`: Maximum number of tokens the model can generate in a single response.
*   `--cache_lens`: Maximum KV cache size in tokens. Directly impacts context length capacity and VRAM usage.
*   `--cache_q4`: (Boolean) If `true`, quantizes the KV cache to 4-bit. **Crucial for saving VRAM**, especially with long contexts.
*   `--temperature`, `--top_p`: Control generation randomness.
*   `--optimize_config_path`: Path to the KTransformers YAML file defining the layer offloading strategy (FP8 on GPU, GGUF on CPU). **Essential for the hybrid setup.**
*   `--force_think`: (KTransformers specific) Potentially related to how the model processes or plans.
*   `--use_cuda_graph`: Enables CUDA graphs for potentially faster GPU execution by reducing kernel launch overhead.
*   `--host`, `--port`: Network interface and port for the server.
*   `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`: Environment variable to help PyTorch manage CUDA memory more flexibly and potentially avoid OOM errors.

---

## 6. Notes on KTransformers v0.3.1

As of 2025-06-02, the `approachingai/ktransformers:v0.3.1-AVX512` image was reported as **not working** with the provided single GPU or multi-GPU configuration.

**Attempted Docker Start Command (v0.3.1 - Non-Functional):**
```bash
# docker stop ktransformers # (if attempting to switch)
# docker run --rm --gpus '"device=0,1"' \
#   -v /home/mukul/dev-ai/models:/models \
#   -p 10002:10002 \
#   --name ktransformers \
#   -itd approachingai/ktransformers:v0.3.1-AVX512
#
# docker exec -it ktransformers /bin/bash
```

**Attempted Server Launch (v0.3.1 - Non-Functional):**
```bash
# # Inside the v0.3.1 Docker container shell
# PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True python3 ktransformers/server/main.py \
#     --gguf_path /models/mukul/DeepSeek-R1-0528-GGML-FP8-Hybrid/Q4_K_M_FP8 \
#     --model_path /models/deepseek-ai/DeepSeek-R1-0528 \
#     --model_name KVCache-ai/DeepSeek-R1-0528-q4km-fp8 \
#     --cpu_infer 57 \
#     --max_new_tokens 32768 \
#     --cache_lens 65536 \
#     --cache_q4 true \
#     --temperature 0.6 \
#     --top_p 0.95 \
#     --optimize_config_path ktransformers/optimize/optimize_rules/DeepSeek-V3-Chat-multi-gpu-fp8-linear-ggml-experts.yaml \
#     --force_think \
#     --use_cuda_graph \
#     --host 0.0.0.0 \
#     --port 10002
```
Stick to `approachingai/ktransformers:v0.2.4post1-AVX512` for the configurations described above until compatibility issues with newer versions are resolved for this specific model and setup.

---

## 7. Available Optimize Config YAMLs (for reference)

The KTransformers repository contains various optimization YAML files. The ones used in this guide are for `DeepSeek-V3` but are being applied to `DeepSeek-R1-0528`. Their direct compatibility or optimality for R1-0528 should be verified. If KTransformers releases specific YAMLs for DeepSeek-R1-0528, those should be preferred.

Reference list of some `DeepSeek-V3` YAMLs (path `ktransformers/optimize/optimize_rules/` inside the container):
```
DeepSeek-V3-Chat-amx.yaml
DeepSeek-V3-Chat-fp8-linear-ggml-experts-serve-amx.yaml
DeepSeek-V3-Chat-fp8-linear-ggml-experts-serve.yaml
DeepSeek-V3-Chat-fp8-linear-ggml-experts.yaml
DeepSeek-V3-Chat-multi-gpu-4.yaml
DeepSeek-V3-Chat-multi-gpu-8.yaml
DeepSeek-V3-Chat-multi-gpu-fp8-linear-ggml-experts.yaml
DeepSeek-V3-Chat-multi-gpu-marlin.yaml
DeepSeek-V3-Chat-multi-gpu.yaml
DeepSeek-V3-Chat-serve.yaml
DeepSeek-V3-Chat.yaml
```