# MiniMax-M2.7-nvidia (SGLang)

Run MiniMax-M2.7-NVFP4 via SGLang on 2x RTX PRO 6000 Blackwell GPUs.

## Hardware

- **GPUs:** 2x NVIDIA RTX PRO 6000 Blackwell (PCI slots 0 & 2)
- **Quantization:** NVFP4 (ModelOpt FP4)
- **Tensor parallelism:** 2-way

> **⚠️ Customize Before Running** — replace the following values with your own:
>
> | What to change | Current value | Where it appears |
> |----------------|-------------|------------------|
> | Model path base | `/media/mukul/data/models` | `-v` volume mounts |
> | Model subfolder | `nvidia/MiniMax-M2.7-NVFP4` | `--model-path` |
> | Model name | `jarvis-thinker` | `--served-model-name` |
> | Host port | `10002` | `-p` (varies by variant) |
> | GPU devices | `device=0,2` | `--gpus` |
> | Max context | `196608` | `--context-length` |
> | Shared memory | `32g` | `--shm-size` |

---

## Variant 1 — SGLang (Custom Build)


### Run

```bash
docker run --rm -it \
  --gpus '"device=0,2"' \
  --ipc=host \
  --shm-size 32g \
  -p 10002:10002 \
  -v /media/mukul/data/models:/models \
  -e OMP_NUM_THREADS=16 \
  -e SGLANG_ENABLE_SPEC_V2=True \
  voipmonitor/sglang:cu130 \
  python -m sglang.launch_server \
    --model-path /models/nvidia/MiniMax-M2.7-NVFP4 \
    --served-model-name jarvis-thinker \
    --reasoning-parser minimax \
    --tool-call-parser minimax-m2 \
    --tp 2 \
    --enable-torch-compile \
    --trust-remote-code \
    --quantization modelopt_fp4 \
    --moe-runner-backend b12x \
    --fp4-gemm-backend b12x \
    --attention-backend flashinfer \
    --enable-pcie-oneshot-allreduce \
    --mem-fraction-static 0.90 \
    --context-length 196608 \
    --max-running-requests 8 \
    --chunked-prefill-size 16384 \
    --sleep-on-idle \
    --host 0.0.0.0 \
    --port 10002
```

---

## Variant 2 — NVFP4, Latest (Stable)

Uses the official `lmsysorg/sglang:latest` image.

```bash
docker run --rm -it \
  --gpus '"device=0,2"' \
  --shm-size 32g \
  -p 10002:8000 \
  -v /media/mukul/data/models:/models \
  -e PYTORCH_ALLOC_CONF=expandable_segments:True \
  lmsysorg/sglang:latest \
  python -m sglang.launch_server \
    --model-path /models/nvidia/MiniMax-M2.7-NVFP4 \
    --served-model-name jarvis-thinker \
    --tp-size 2 \
    --quantization modelopt_fp4 \
    --tool-call-parser minimax-m2 \
    --reasoning-parser minimax \
    --host 0.0.0.0 \
    --port 8000 \
    --trust-remote-code \
    --dtype auto \
    --mem-fraction-static 0.90 \
    --context-length 196608 \
    --max-running-requests 16 \
    --chunked-prefill-size 16384 \
    --sleep-on-idle
```

---

## Variant 3 — NVFP4, dev-cu13

Uses `lmsysorg/sglang:dev-cu13` for cutting-edge development builds.

```bash
docker run --rm -it \
  --gpus '"device=0,2"' \
  --shm-size 32g \
  -p 10002:8000 \
  -v /media/mukul/data/models:/models \
  -e PYTORCH_ALLOC_CONF=expandable_segments:True \
  lmsysorg/sglang:dev-cu13 \
  python -m sglang.launch_server \
    --model-path /models/nvidia/MiniMax-M2.7-NVFP4 \
    --served-model-name jarvis-thinker \
    --tp-size 2 \
    --quantization modelopt_fp4 \
    --tool-call-parser minimax-m2 \
    --reasoning-parser minimax \
    --host 0.0.0.0 \
    --port 8000 \
    --trust-remote-code \
    --dtype auto \
    --mem-fraction-static 0.85 \
    --context-length 196608 \
    --max-running-requests 16 \
    --chunked-prefill-size 16384 \
    --sleep-on-idle
```

---

## Variant 4 — Native (No Docker)

Run directly in a conda environment without Docker.

### Activate environment

```bash
conda activate sglang
```

### Run

```bash
python -m sglang.launch_server \
  --model-path /media/mukul/data/models/lukealonso/MiniMax-M2.7-NVFP4 \
  --served-model-name jarvis-thinker \
  --tp-size 2 \
  --quantization modelopt_fp4 \
  --tool-call-parser minimax-m2 \
  --reasoning-parser minimax \
  --host 0.0.0.0 \
  --port 10002 \
  --trust-remote-code \
  --dtype auto \
  --mem-fraction-static 0.90 \
  --context-length 196608 \
  --max-running-requests 16 \
  --chunked-prefill-size 16384 \
  --sleep-on-idle
```

---

## Key Flags Explained

| Flag | Purpose |
> |------|---------|
> | `--context-length 196608` | 192K context window |
> | `--quantization modelopt_fp4` | ModelOpt FP4 quantization |
> | `--mem-fraction-static 0.90` | Reserve 90% GPU memory for KV cache |
> | `--sleep-on-idle` | Scale down when idle to save power |
> | `--enable-torch-compile` | Compile model with PyTorch compile (nightly only) |
> | `--enable-pcie-oneshot-allreduce` | Single-shot PCIe all-reduce for MoE (nightly only) |
> | `--moe-runner-backend b12x` | MoE expert routing backend (nightly only) |
> | `--attention-backend flashinfer` | FlashInfer attention kernel (nightly only) |
> | `--chunked-prefill-size 16384` | Split prefill into 16K-token chunks to bound latency |
