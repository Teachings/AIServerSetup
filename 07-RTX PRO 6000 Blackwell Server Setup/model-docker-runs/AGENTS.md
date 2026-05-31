# Agents

This directory contains Docker Compose configurations for local LLM inference servers.

## Structure

- `docker-compose.yaml` — service definitions for model serving containers
- `README.md` — usage instructions and service documentation

## Conventions

- Each service in `docker-compose.yaml` corresponds to one model endpoint
- Services expose OpenAI-compatible APIs on host ports starting at `10000+`
- Model weights are stored at `/media/mukul/data/models` on the host, mounted at `/models` in containers
- GPU device assignments are pinned per service via `deploy.resources.reservations.devices`
- All services use `restart: unless-stopped` for crash recovery
- Health checks use the vLLM `/health` endpoint

## Services

| Service | Model | Port | GPU Mem | GPUs |
|---------|-------|------|---------|------|
| `jarvis-thinker` | Step-3.7-Flash-NVFP4 | 10002 | 0.75 | 0, 2 |
| `jarvis` | Qwen3.6-35B-A3B-NVFP4 | 10006 | 0.20 | 0, 2 |

Both services share GPUs 0 and 2. Total GPU memory allocation is 0.95 per GPU (0.75 + 0.20).

## Adding a new model service

1. Add a new service block to `docker-compose.yaml`
2. Assign a unique host port (check for conflicts with existing services)
3. Pin to specific GPU devices — if sharing GPUs with existing services, reduce `--gpu-memory-utilization` so total across services stays ≤ 0.95
4. Set `--served-model-name` to a recognizable alias
5. Choose the correct `--reasoning-parser` and `--tool-call-parser` for the model family
6. Run `docker compose up -d <service-name>` to start
