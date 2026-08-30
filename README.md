# Week 3 Day 1: LLM Inference Profiling & Memory Leak Detection on NVIDIA T4

Empirical benchmarking of resident VRAM dynamics, throughput scaling, and leak detection algorithms using **Qwen2.5-1.5B-Instruct** on an NVIDIA Tesla T4 GPU (16GB).

---

## Core Findings & Benchmarks

* **Context Length vs. VRAM**: VRAM allocation scales with sequence length due to KV Cache expansion.
* **Quantization Footprint**: 8-bit precision halves baseline weight footprint from ~3.0 GB to ~1.5 GB.
* **The Utilisation Trap**: High reported `nvidia-smi` utilization on single streams reflects memory bandwidth bottlenecks rather than compute saturation.
* **Batching Efficiency**: Batch size 8 yields ~6x throughput improvement over batch size 1.
* **Memory Leak Hunter (Extra Lab)**: 
  * Unreleased Autograd computation graphs and retained output tensors induced a linear leak of **~90.4 MB/iter**.
  * Resolved via explicit `torch.no_grad()` inference scoping and tensor value extraction, flattening memory drift to **0.0 MB/iter**.

---

## Artifacts

* **Main Lab**:
  * `w3d1_profile_inference.ipynb`: Core profiling implementation.
  * `profile.json`: 6-point evaluation matrix across precisions and contexts.
  * `batch_check.json`: Batch 1 vs. Batch 8 throughput measurements.
* **Extra Lab**:
  * `w3d1_extra_memory_leak.ipynb`: Memory leak detector implementation.
  * `leak_report.json`: Baseline, leaky (~90.4 MB/iter), and fixed slope empirical records (`GREEN CHECK: PASS`).
