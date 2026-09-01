
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

---
# Extra Lab W3D3: Client-Side Load Shedding Under Overload

## Overview
Demonstration of a client-side admission control pattern (Load Shedding) in front of a **vLLM** inference server (`Qwen/Qwen2.5-1.5B-Instruct` on NVIDIA T4). The experiment evaluates latency resilience under sudden traffic bursts by comparing unmanaged queueing against a strict concurrency cap.

---

## Experimental Results

### 1. Unbounded Baseline vs. Load Shedding (Burst = 50)
| Strategy | Requests Sent | Accepted | Shed (Rejected) | p95 Latency (Accepted) | Mean Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Naive (Unbounded)** | 50 | 50 | 0 | **1.001 s** | 0.996 s |
| **Shedded (`cap=8`)** | 50 | 8 | 42 | **0.444 s** | 0.438 s |

### 2. Load Shedding Sweep Across Burst Sizes (`cap=8`)
| Burst Size ($N$) | Accepted | Shed | Accepted p95 Latency | Invariant Status |
| :--- | :--- | :--- | :--- | :--- |
| **8** | 8 | 0 | **0.435 s** | In-flight within safe bounds |
| **16** | 8 | 8 | **0.401 s** | Overflow rejected fast |
| **32** | 8 | 24 | **0.400 s** | Overflow rejected fast |
| **50** | 8 | 42 | **0.444 s** | Overflow rejected fast |

---

## Verified Invariants

* **`shedding happened`**: Overflow requests beyond the concurrency limit were dropped immediately with minimal overhead.
* **`accepted p95 protected`**: Accepted request latency remained strictly bounded within **$0.400\text{ s} - 0.444\text{ s}$**, avoiding the $>2.3\times$ latency degradation seen in the unbounded baseline.
* **`cap flat`**: Active in-flight concurrency never exceeded the safe threshold of 8, preventing KV cache contention and GPU VRAM saturation.

---

## Engineering Takeaways

* **Unbounded Degradation:** Admitting all 50 requests without admission control caused server-side queue buildup, degrading $p95$ latency by over $2.3\times$ ($1.001\text{ s}$ vs. $0.435\text{ s}$) across all traffic.
* **Controlled Load Shedding:** Enforcing a strict concurrency ceiling (cap=8) with fast rejections prevented KV cache contention and VRAM saturation in vLLM. This kept accepted $p95$ latency strictly protected within a stable $0.400\text{ s} - 0.444\text{ s}$ window across all burst levels (8, 16, 32, and 50).
* **Fail-Fast over Queue Starvation:** Immediate rejection of excess requests protects SLAs for admitted traffic far better than allowing unbounded queues to degrade latency for 100% of users.
* **Hardware Protection:** Hard-capping in-flight requests ensures predictable memory allocation and prevents out-of-memory (OOM) failures on memory-constrained GPUs (e.g., NVIDIA T4).
