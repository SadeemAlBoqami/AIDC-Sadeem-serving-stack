
  # Lab W3D3: LLM Inference Engine Swap (Static Batching vs. vLLM)

## Overview
Performance benchmark comparing traditional static batching against **vLLM** (`Qwen/Qwen2.5-1.5B-Instruct`) on an **NVIDIA T4 GPU**, evaluating the impact of **PagedAttention** and **Continuous Batching** under varying concurrency levels.

---

## Predictions card:

- At concurrency 8, I predict vLLM's throughput will be about 2.5x times Monday's static-batch-8 baseline.
- Based on my baselines.json, static batching scaled 2.88x from batch 1 to 8 (81.1 / 28.2).
- For vLLM running the identical queue, I predict it will scale 4x from concurrency 1 to 8.
- Because continuous batching eliminates slot efficiency collapse under mixed output lengths, I expect vLLM's scaling multiple to be larger than static batching's, and roughly 1.4x larger.

  ---

## Benchmark Results

| Concurrency | Static Baseline (tok/s) | vLLM Engine (tok/s) | Direct Speedup | Total Wall Time (vLLM) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 28.2 | 58.8 | **2.09x** | 23.64 s |
| **4** | 41.6 | 169.6 | **4.08x** | 8.19 s |
| **8** | 81.1 | 229.8 | **2.83x** | 6.05 s |

---

## Key Metrics & Scaling Analysis

* **Static Scaling (1 to 8):** `2.88x`
* **vLLM Scaling (1 to 8):** `3.91x` *(Target Prediction: ~4.0x)*
* **Continuous Batching Dividend:** `1.36x` extra scaling factor over static batching (`3.91 / 2.88`).

---

## Engineering Takeaways

* **Zero Batch-Door Delay:** Continuous batching dynamically schedules requests per token step, eliminating idle tails and head-of-line blocking caused by variable sequence lengths.
* **VRAM Efficiency via PagedAttention:** Eliminates internal KV cache fragmentation, allowing higher concurrent throughput without out-of-memory (OOM) faults.
* **Drop-in Optimization:** Replaced the backend serving layer with an OpenAI-compatible vLLM endpoint without altering the client-side API contract.
