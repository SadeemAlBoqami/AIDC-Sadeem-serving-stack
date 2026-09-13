# Lab W5D1: Observability & Monitoring Summary

## Overview
Successfully deployed, integrated, and validated a Prometheus and Grafana observability stack to monitor a high-performance LLM serving instance.

## Key Deployments & Architecture
- **Model Monitored**: `Qwen/Qwen2.5-1.5B-Instruct-AWQ`.
- **Kubernetes Namespace**: `team`.
- **Monitoring Stack**: In-cluster Prometheus deployment (`http://prometheus:9090`) and Grafana Service mapped to `NodePort 30300`.
- **Telemetry**: vLLM engine exposed at `/metrics` and scraped at 15-second intervals.

## Validation & Testing Results
- **Automated Verification**: Passed all diagnostic queries, targets, and dashboard schema checks with `GREEN CHECK: PASS`.
- **Load Testing**: Generated continuous chat workloads via `traffic.py` (up to 4 concurrent callers, 64 max output tokens) to evaluate system stability.
- **Observed Service Level Indicators (SLIs)**:
  - *Time to First Token (TTFT) p95 (5m)*: ~38.899 ms (Established Target: < 100 ms).
  - *Completed requests / min (5m)*: ~25.3 req/m (Established Target: > 15 req/m).

## Deliverables
- **Dashboard JSON**: Configured and exported `my-dashboard.json`, containing integrated PromQL queries and time-series panels without external sharing metadata.
- **SLO Targets**: Finalized `my-slo-targets.md` defining measurement windows, observed metrics, and architectural justifications for the chosen SLIs.
