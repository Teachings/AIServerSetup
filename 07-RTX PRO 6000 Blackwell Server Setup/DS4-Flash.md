# DeepSeek-V4-Flash (vLLM)

Run DeepSeek-V4-Flash with W4A16FP8 activation and MTP speculative decoding via vLLM on 2x RTX PRO 6000 Blackwell GPUs.

## Hardware

- **GPUs:** 2x NVIDIA RTX PRO 6000 Blackwell (PCI slots 0 & 2)
- **Quantization:** W4A16 + FP8 activation
- **Speculative decoding:** MTP (Multi-Token Prediction), 1 token lookahead
- **Tensor parallelism:** 2-way

> **⚠️ Customize Before Running** — replace the following values with your own:
>
> | What to change | Current value | Where it appears |
> |----------------|-------------|------------------|
> | Model path base | `/media/mukul/data/models` | `-v` volume mounts |
> | Model subfolder | `LordNeel/DeepSeek-V4-Flash-Acti-MTP-W4A16-FP8` | `-e MODEL_PATH` |
> | Model name | `jarvis-thinker` | `--served-model-name` |
> | Host port | `10002` | `-p 10002:8000` |
> | GPU devices | `device=0,2` | `--gpus` |
> | Max context | `262144` | `--max-model-len` |
> | Shared memory | `64g` | `--shm-size` |

## Running

```bash
docker run --rm -it \
  --gpus '"device=0,2"' \
  --ipc=host \
  --shm-size 64g \
  -p 10002:8000 \
  -v /media/mukul/data/models:/models \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e CUDA_DEVICE_ORDER=PCI_BUS_ID \
  -e MODEL_PATH=/models/LordNeel/DeepSeek-V4-Flash-Acti-MTP-W4A16-FP8 \
  -e NCCL_PROTO=LL \
  -e NCCL_ALGO=Ring \
  -e NCCL_MIN_NCHANNELS=8 \
  -e NCCL_NTHREADS=512 \
  dsv4-flash-acti-mtp:0.1.0 \
  --served-model-name jarvis-thinker \
  --trust-remote-code \
  --kv-cache-dtype fp8 \
  --block-size 256 \
  --tensor-parallel-size 2 \
  --disable-custom-all-reduce \
  --tokenizer-mode deepseek_v4 \
  --tool-call-parser deepseek_v4 \
  --enable-auto-tool-choice \
  --reasoning-parser deepseek_v4 \
  --max-model-len 262144 \
  --max-num-seqs 1 \
  --max-num-batched-tokens 8192 \
  --gpu-memory-utilization 0.93 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":1}' \
  --host 0.0.0.0 \
  --port 8000
```

## Key Flags Explained

| Flag | Purpose |
|------|--------|
| `--shm-size 64g` | 64 GB shared memory for large KV cache |
| `--kv-cache-dtype fp8` | FP8 KV cache for memory efficiency |
| `--tensor-parallel-size 2` | Split model across 2 GPUs |
| `--disable-custom-all-reduce` | Use NCCL instead of custom all-reduce |
| `--speculative-config` | Enable MTP speculative decoding (1 token lookahead) |
| `--max-model-len 262144` | 256K context window |
| `--gpu-memory-utilization 0.93` | Reserve 93% GPU memory for model + KV cache |
| `--max-num-batched-tokens 8192` | Max tokens per forward pass |

## Prerequisites

The Docker image must be built first (from the DSv4-Flash project):

```bash
docker build -t dsv4-flash-acti-mtp:0.1.0 .
```
