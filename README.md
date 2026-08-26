# Week 2 Day 4: Portable GPU Serving Image with CPU Fallback

## Overview
Built a unified, portable container image (`aidc-serving:gpu-v1`) based on NVIDIA CUDA runtime (`nvidia/cuda:12.4.1-runtime-ubuntu22.04`). The serving stack dynamically selects CUDA when hardware acceleration is available and gracefully degrades to CPU fallback when executed on a GPU-less machine without container failure.

---

## Architectural Decisions & Portable Runtime
* **Base Image**: `nvidia/cuda:12.4.1-runtime-ubuntu22.04` to provide required CUDA userspace drivers.
* **Explicit Python 3.11 Toolchain**: Installed and symlinked `python3.11` to prevent version drift from Ubuntu 22.04 default (`3.10`).
* **Dynamic Device Discovery**: `app/generate_probe.py` and `app/main.py` resolve execution targets via `torch.cuda.is_available()` at runtime rather than baking device constraints into the image.

---

## Performance Benchmark & Evidence (128 Tokens Generated)

| Environment | Device | Precision | Throughput (Tokens/s) |
| :--- | :--- | :--- | :--- |
| **Colab Environment** | NVIDIA Tesla T4 | `torch.float16` | **31.4** |
| **Local Host** | CPU Fallback | `torch.float32` | Baseline |

---

## Verification Suite (Tier-0 Green Check)
Executed the local and remote verification script `verify.sh`:

* **Part 1**: Resolved and verified GPU image `sadeemalboqami/aidc-serving:gpu-v1`.
* **Part 2**: Confirmed `/health` returns HTTP 200 on CPU fallback mode (without passing `--gpus`).
* **Part 3**: Validated `gpu_evidence.json` generated on Colab T4 runtime (`cuda: true`, positive throughput).

```text
waiting for /health on CPU fallback (up to 420s) ...
OK:Tesla T4:31.4
part 1: GPU image resolved
part 2: /health 200 on CPU fallback
part 3: colab evidence shows cuda: true
GREEN CHECK: PASS
```

---
