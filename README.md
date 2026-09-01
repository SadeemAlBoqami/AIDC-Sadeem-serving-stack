# AI Data Center Operations & Serving Stack

This repository contains daily labs, benchmarks, and production deployments for the AI Data Center Operations Bootcamp. Each branch represents an isolated standalone layer of the overall serving stack.

---

## Repository Structure & Daily Branches

### Week 2: Microservices, Containerisation & Orchestration
* **`w2d1`**: Microservices architecture & API contract definitions.
* **`w2d2`**: OpenAI-compatible serving stack implementation.
* **`w2d3`**: CPU-based containerisation & Docker runtime deployment.
* **`w2d4`**: Portable GPU image configuration with CPU fallback.
* **`w2d5`**: Multi-container Docker Compose stack with auth & token clipping.

---

### Week 3: High-Performance GPU Serving Engines & Profiling
* **`w3d1`**: Inference profiling on NVIDIA T4 GPU (VRAM scaling, arithmetic intensity, and batching dynamics).
* **`w3d2`**: LLM inference anatomy, KV-cache memory arithmetic & PagedAttention block-pool allocation.
* **`w3d3`**: vLLM engine swap via Continuous Batching & PagedAttention, client-side load shedding.

---

## Navigation
Switch to any specific branch using the branch selector above or via Git CLI:
```bash
git checkout <branch-name>

