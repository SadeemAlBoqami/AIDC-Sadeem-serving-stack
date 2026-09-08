# Lab W4D3: GPU Scheduling, Resource Accounting, and vLLM Deployment

## Overview
This lab covers Kubernetes resource management, QoS classes, CPU/GPU scheduling constraints, and deploying a shared vLLM inference engine on a GPU-accelerated node.

---

## Key Tasks & Achievements

### 1. Resource Requests & Limits
* Configured CPU and Memory `requests` and `limits` in deployment manifests to establish proper QoS classes.
* Verified resource accounting via `kubectl describe node` under the `Allocated resources` ledger.

### 2. Overcommitment & Scheduler Enforcement
* Tested resource overdraw by requesting impossible allocations (e.g., `cpu: "64"`).
* Confirmed the scheduler rejects over-allocated pods into `Pending` state with the `Insufficient cpu` event.

### 3. GPU Scheduling & Team Namespaces
* Verified GPU hardware ledger tracking via `nvidia.com/gpu` requests.
* Resolved resource contention and scheduling conflicts in shared environments using strict namespace isolation (`team` vs. individual `$ME` namespaces).

### 4. Noisy Neighbour Mitigation
* Measured latency impact ($p95$) under unconstrained CPU load (`while True: pass`).
* Demonstrated how setting explicit CPU `limits` protects inference service latencies from rogue workloads.

### 5. vLLM Engine Deployment & Verification
* Deployed the production vLLM inference engine to the shared `team` namespace utilizing the physical GPU node.
* Executed automated verification scripts (`verify.sh`) resulting in **`GREEN CHECK: PASS`**.
