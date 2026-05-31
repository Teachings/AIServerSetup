# Model Docker Runs

Docker Compose configurations for running local LLM inference servers.

## Prerequisites

- Docker + Docker Compose v2
- NVIDIA Container Toolkit (`nvidia-container-toolkit`)
- GPU drivers with CUDA support

## Usage

```bash
# Start all services
docker compose up -d

# Follow logs
docker compose logs -f jarvis-thinker

# Stop all services
docker compose down

# Restart a single service
docker compose restart jarvis-thinker
```

## Services

### jarvis-thinker

| Field | Value |
|-------|-------|
| Model | Step-3.7-Flash-NVFP4 |
| Image | `vllm/vllm-openai:stepfun37-cu129` |
| GPUs | 0, 2 (tensor-parallel-size 2) |
| Port | `10002` → container `8000` |
| Max context | 262,144 tokens |
| Max concurrent sequences | 16 |
| KV cache dtype | bfloat16 |
| GPU memory utilization | 0.75 |
| Quantization | modelopt (NVFP4) |

#### Endpoints

- OpenAI-compatible API: `http://localhost:10002/v1`
- Health check: `http://localhost:10002/health`
- Model name for API calls: `jarvis-thinker`

#### Example API call

```bash
curl http://localhost:10002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jarvis-thinker",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 256
  }'
```

### jarvis

| Field | Value |
|-------|-------|
| Model | Qwen3.6-35B-A3B-NVFP4 (NVIDIA) |
| Image | `vllm/vllm-openai:stepfun37-cu129` |
| GPUs | 0, 2 (tensor-parallel-size 2) |
| Port | `10006` → container `8000` |
| Max context | 262,144 tokens |
| Max concurrent sequences | 8 |
| KV cache dtype | bfloat16 |
| GPU memory utilization | 0.20 |
| Quantization | modelopt (NVFP4) |

#### Endpoints

- OpenAI-compatible API: `http://localhost:10006/v1`
- Health check: `http://localhost:10006/health`
- Model name for API calls: `jarvis`

#### Example API call

```bash
curl http://localhost:10006/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jarvis",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 256
  }'
```

## Configuration

Model weights are loaded from `/media/mukul/data/models`. Hugging Face cache is stored at `/media/mukul/data/models/.hf-cache` inside the container.

Both services share GPUs 0 and 2. `jarvis-thinker` uses 75% GPU memory, `jarvis` uses 20% — ensure both are running simultaneously for the split to work as intended.
