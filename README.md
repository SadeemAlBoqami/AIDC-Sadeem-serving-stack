# LLM Inference Benchmarking & Capacity Sizing (vLLM on NVIDIA T4)

## Objective
Benchmark the locked production model (`Qwen2.5-1.5B-Instruct-AWQ`) using a concurrency sweep (1 to 16) to locate the honest operational capacity point (**The Knee**) against an established latency budget (SLO: p95 latency ≤ 2.5s).

## Benchmark Results (Sweep Summary)

| Concurrency | Throughput (tok/s) | TTFT p95 (s) | E2E Latency p95 (s) | Errors |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 462.1 | 0.068 | 1.419 | 0 |
| 2 | 858.8 | 0.167 | 1.601 | 0 |
| 4 | 1527.1 | 0.187 | 1.737 | 0 |
| 8 | 2357.0 | 0.128 | 1.804 | 0 |
| **16 (Knee)** | **3142.4** | **0.162** | **2.267** | **0** |

* **Target SLO:** p95 ≤ 2.5s
* **Knee Concurrency:** 16 (Sweep-bounded)
* **Max Sustainable Request Rate:** ~7.06 req/s

## Key Takeaways & Infra Insights

* **The Knee vs. The Peak:** Peak throughput is an operational anti-pattern; it artificially inflates metrics by serving saturated requests past acceptable latency limits. Capacity must strictly be committed at the knee where the SLA/SLO holds.
* **Bottleneck Classification:** **Memory-bound**. Linear scaling begins to taper at higher concurrency as decode memory bandwidth and KV-cache block contention dictate scheduling overhead rather than raw tensor core compute.
* **Sizing Verdict:** The quantized AWQ build effectively frees KV-cache blocks, allowing the stack to comfortably sustain up to 16 concurrent streams on a single T4 GPU with zero request drops.
