# Lab W3D2: Inference Anatomy

## Objective
Measure the two distinct operational phases of LLM generation (Time to First Token vs. Time Per Output Token), empirically validate physical KV cache growth against the theoretical arithmetic formula, and benchmark hand-rolled static batching throughput under mixed-length workload queues to observe the ceiling imposed by straggler padding.

---

## Prediction Card (By Hand)

* **Time to First Token (TTFT)** is dominated by prefill (reading the whole prompt). A longer prompt makes TTFT go **UP** (scales with prompt sequence length due to parallel compute intensity).
* After the first token, decode emits one token at a time. The mean gap between tokens (TPOT) depends mostly on **model size and memory bandwidth** (memory-bound parameter movement per step).
* **KV Cache Math for Qwen2.5-1.5B** (28 layers, 2 KV heads, head_dim 128, fp16):
  * **Per Token**: `2 * 28 * 2 * 128 * 2 bytes = 28.0 KB per token`
  * **4096-token context**: `4096 * 28.0 KB ≈ 0.11 GB (0.115 GB)`
* **Static Batching Finish Condition**: If you pad 8 prompts of different lengths and run them as one batch, the batch finishes when the **slowest / longest** prompt finishes.

---

## Baseline Empirical Results (baselines.json)

* **Model & Precision**: `Qwen/Qwen2.5-1.5B-Instruct` (`fp16`) on NVIDIA Tesla T4 GPU.

### 1. Prefill vs. Decode Latency Dynamics
* **Time to First Token (TTFT)**:
  * `128` tokens: **`0.1080s`**
  * `512` tokens: **`0.1749s`**
  * `2048` tokens: **`0.7476s`** *(~7x increase proving sequence length dependency)*
* **Time Per Output Token (TPOT)**: **`0.0609s`** (~16.42 tokens/sec single-stream decode speed).

### 2. Static Batching Throughput & Straggler Ceiling
* **Batch 1**: **`28.2 tok/s`** (Slot efficiency: `1.000`)
* **Batch 4**: **`41.6 tok/s`** (Slot efficiency: `~0.333`)
* **Batch 8**: **`81.1 tok/s`** (Slot efficiency: `~0.333`)
* **Scaling Gain**: `2.87x` (Batch 1 to 8), capped well below linear ~5.6x due to locked-step padding waste across mixed lengths (32 vs 256 tokens).

### 3. KV Cache Footprint Verification (kv_check.json)
* **Formula Expected**: `28.0 KB/token`
* **Measured KV Cache**: `28.0 KB/token` (**Exact match**)
* **Status**: `GREEN CHECK: PASS`

  ---

  Empirical latency decomposition, theoretical KV cache arithmetic verification, static batching straggler measurements, and miniature PagedAttention block-pool simulation using **Qwen2.5-1.5B-Instruct** on NVIDIA Tesla T4 GPU.

---

## Prediction Card (By Hand)

* **Time to First Token (TTFT)**: Dominated by prefill and scales **UP** with sequence length.
* **Time Per Output Token (TPOT)**: Governed primarily by **model size and memory bandwidth** (memory-bound).
* **KV Cache Math for Qwen2.5-1.5B** (28 layers, 2 KV heads, head_dim 128, fp16):
  * **Per Token**: `2 * 28 * 2 * 128 * 2 bytes = 28.0 KB/token`
  * **4096 Context**: `4096 * 28.0 KB ≈ 0.11 GB (0.115 GB)`
* **Static Batching Finish Condition**: The batch finishes when the **slowest / longest** prompt finishes.

---

## 1. Inference Anatomy Baselines (`baselines.json` & `kv_check.json`)

* **TTFT Scaling (Prefill)**:
  * 128 tokens: `0.1080s`
  * 512 tokens: `0.1749s`
  * 2048 tokens: `0.7476s` (~7x growth across sequence length).
* **TPOT (Decode)**: `0.0609s/token` (~16.42 tokens/sec single stream).
* **Static Batching Straggler Tax**:
  * Batch 1: `28.2 tok/s` (Slot efficiency: `1.000`)
  * Batch 4: `41.6 tok/s` (Slot efficiency: `~0.333`)
  * Batch 8: `81.1 tok/s` (Slot efficiency: `~0.333`, throttled at 2.87x vs linear 5.6x due to padding).
* **KV Formula Validation**: Measured `28.0 KB/token` vs Theoretical `28.0 KB/token` (`PASS`).

---

# 2. Extra Lab: Paged KV Allocator Simulation (`kv_sim_report.json`)

Benchmarking a fixed 2 GB memory pool across a 60-sequence mixed-length workload (mean: 444.4 tokens, max: 3763 tokens):

| Allocator Strategy | Admitted Sequences | Rejected Sequences | Peak Concurrency |
| :--- | :--- | :--- | :--- |
| **Naive Slab (Max-length)** | 18 | 42 | 18 |
| **Block-Pool (Paged 16-tok)** | 60 | 0 | 60 |

* **Block-Pool Advantage**: **`3.33x` concurrency gain** over static slab allocation on identical memory budget.
* **Verification**: `GREEN CHECK: PASS`

---

## Artifacts

* `w3d2_inference_anatomy.ipynb`: Main profiling notebook.
* `paged_kv_sim.py`: Block-pool vs slab simulation script.
* `baselines.json`: Latency and throughput master record.
* `kv_check.json`: KV cache empirical footprint validation.
* `kv_sim_report.json`: Memory allocator simulation report.

  ---
