# Lab W3D2: Inference Anatomy, By Hand

## Objective
Measure the two distinct operational phases of LLM generation (Time to First Token vs. Time Per Output Token), empirically validate physical KV cache growth against the theoretical arithmetic formula, and benchmark hand-rolled static batching throughput under mixed-length workload queues to observe the ceiling imposed by straggler padding.

---

## Prediction Card (By Hand)

* **Time to First Token (TTFT)** is dominated by prefill (reading the whole prompt). A longer prompt makes TTFT go **UP** (scales with prompt sequence length due to parallel compute intensity).
* After the first token, decode emits one token at a time. The mean gap between tokens (TPOT) depends mostly on **model size and memory bandwidth** (memory-bound parameter movement per step).
* **KV Cache Math for Qwen2.5-1.5B** ($28\text{ layers}, 2\text{ KV heads}, \text{head\_dim } 128, \text{fp16}$):
  $$\text{Per Token} = 2 \times 28 \times 2 \times 128 \times 2\text{ bytes} = \mathbf{28.0\text{ KB per token}}$$
  $$\text{A 4096-token context holds} = 4096 \times 28.0\text{ KB} \approx \mathbf{0.11\text{ GB (0.115 GB)}}$$
* **Static Batching Finish Condition**: If you pad 8 prompts of different lengths and run them as one batch, the batch finishes when the **slowest / longest** prompt finishes.

---

## Baseline Empirical Results (`baselines.json`)

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
* **Scaling Gain**: `2.87x` (Batch 1 to 8), capped well below linear ~5.6x due to locked-step padding waste across mixed lengths ($32$ vs $256$ tokens).

### 3. KV Cache Footprint Verification (`kv_check.json`)
* **Formula Expected**: `28.0 KB/token`
* **Measured KV Cache**: `28.0 KB/token` (**Exact match**)
* **Status**: `GREEN CHECK: PASS`
