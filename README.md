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

---

# **EXTRA LAB**: LLM Serving Economics: Cost per Million Tokens & Scale-Out Analysis

## Objective
Convert empirical serving metrics (`tokens/s` and `p95 latency`) into financial infrastructure costs ($/M output tokens) and determine the exact scale-out breakeven point where deploying horizontal GPU replicas supersedes vertical concurrency overloading under a strict SLA/SLO contract.

## Unit Economics (On-Demand T4 @ $0.35/hr)

| Concurrency | Throughput (tok/s) | p95 Latency (s) | Cost per Million Tokens ($) | SLO Status (≤ 2.5s) |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 462.06 | 1.419 | $0.2104 | Compliant |
| 2 | 858.76 | 1.601 | $0.1132 | Compliant |
| 4 | 1527.08 | 1.737 | $0.0637 | Compliant |
| 8 | 2356.96 | 1.804 | $0.0412 | Compliant |
| **16 (Knee)** | **3142.41** | **2.267** | **$0.0309** | **Compliant (Optimal)** |

## Horizontal Scale-Out Plan (SLO-Preserving)

| Demand Multiple | Required Throughput (tok/s) | Replicas Needed | Total Cost ($/hr) | Effective p95 Latency (s) |
| :---: | :---: | :---: | :---: | :---: |
| **1.0x** | 3142.41 | 1 | $0.35 | 2.267 |
| **1.5x** | 4713.62 | 2 | $0.70 | 2.267 |
| **2.0x** | 6284.82 | 2 | $0.70 | 2.267 |
| **3.0x** | 9427.23 | 3 | $1.05 | 2.267 |

## Core Infrastructure Takeaways

* **The Unit Cost Paradox:** While higher concurrency mathematically suppresses the cost per million tokens, pushing past the knee breaches the SLO. Lower theoretical costs at degraded latency fail production viability.
* **Scale-Out Decision Model:** To absorb spikes exceeding knee capacity (3,142.41 tok/s), traffic must scale out across identical replicas running strictly at the safe knee concurrency. This preserves tail latency (`p95 = 2.267s`) across all replicas without risking queue saturation or thrashing.
