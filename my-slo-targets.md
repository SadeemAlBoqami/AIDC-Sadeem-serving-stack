# Service indicators and proposed targets

Team: 09
Use case: Baseline chat engine for AI Data Center Bootcamp lab.
Service measured: Qwen/Qwen2.5-1.5B-Instruct-AWQ model on vLLM, team namespace.
Workload: Lab traffic generator, up to 4 concurrent callers, 64 max output tokens.
Measurement period: 2026-09-13 11:33 to 11:37 AST.
Instrumentation gaps: Native vLLM metrics lack HTTP response status codes.

## SLI 1

Indicator: Time to First Token (TTFT) 95th percentile
Panel: TTFT p95 (5m)
Unit: ms
Target: < 100 ms
Window: 5 minutes
Observed: 38.899 ms
Evidence: Grafana dashboard panel snapshot at peak traffic.
Why it fits: Measures responsiveness, which is critical for a smooth user experience in chat applications.
Limitations: Histogram buckets provide estimates, and the sample size is small due to the short test duration.

## SLI 2

Indicator: Completed requests per minute
Panel: Completed requests / min (5m)
Unit: req/m
Target: > 15 req/m
Window: 5 minutes
Observed: 25.3 req/m
Evidence: Grafana dashboard panel snapshot at the end of the traffic script execution.
Why it fits: Shows the engine's throughput capacity and its ability to handle concurrent workloads.
Limitations: Only counts requests finished by stop or length limits; it does not verify output quality.