# Capacity note (team, one page)

## The numbers

- Locked model: Qwen/Qwen2.5-1.5B-Instruct-AWQ
- Target p95 end-to-end latency (your SLO today): 2.5 seconds
- Knee concurrency (highest concurrency whose p95 is still under target): 16
- Tokens per second at the knee: 3142.4
- Max sustainable request rate at the target p95: 7.06 req/s

## The limiting family

One sentence, using this morning's triage lens (compute vs memory vs overhead):
which family limits this stack at the knee, and the tell that points to it.

- Memory-bound: token throughput begins tapering off its linear scaling slope while decode memory bandwidth and KV cache management dominate execution time rather than raw compute.

## Why the knee, not the peak

One sentence in your own words on why you report the knee at the SLO rather than
the peak throughput.

- Reporting the knee reflects the honest usable serving capacity under our latency contract, whereas peak throughput includes saturated requests that fail acceptable latency limits.