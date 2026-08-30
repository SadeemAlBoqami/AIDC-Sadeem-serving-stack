# Week 3 Day 1: LLM Inference Profiling on NVIDIA T4

Empirical profiling of resident VRAM, GPU utilisation, and decoding throughput across multiple precisions and context lengths using **Qwen2.5-1.5B-Instruct** on an NVIDIA Tesla T4 GPU (16GB).

---

## Key Experimental Findings
* **Resident VRAM vs. Context Length**: Resident memory scales with context length due to KV Cache expansion.
* **FP16 vs. INT8 Memory Footprint**: 8-bit weight quantization reduces model memory allocation from ~3.0 GB to ~1.5 GB.
* **The Utilisation Trap (`nvidia-smi`)**: Single-request decoding exhibits high reported GPU utilisation despite low arithmetic saturation.
* **Batching & Throughput**: Increasing batch size from 1 to 8 achieves a ~6x increase in throughput (tokens/s).

---

## Verify (green check)
```
rows: 6, dtypes: ['fp16', 'int8'], contexts: [512, 2048, 4096]
batch-1 tokens/s: 28.8, batch-8 tokens/s: 175.3
GREEN CHECK: PASS
```
