# Lab W4D4: Package It and Let It Breathe

## Overview
This laboratory focuses on packaging a Kubernetes serving deployment into a Helm chart, configuring and verifying Horizontal Pod Autoscaling (HPA) using CPU metrics, and analyzing the limitations of CPU-based autoscaling in GPU-bound LLM serving architectures.

## Completed Objectives
1. **Helm Chart Packaging:** Converted raw Kubernetes manifests (Deployment, Service) into a parameterized Helm chart (`serving-chart`) utilizing custom `values.yaml` configurations for resources, probes, and HPA parameters.
2. **Dynamic Autoscaling & Load Testing:** 
   - Enabled HPA targeting 50% CPU utilization with a maximum of 3 replicas.
   - Deployed an in-cluster `loadgen` workload generating concurrent requests.
   - Successfully observed the control loop scaling replicas from 1 to 3 dynamically as CPU utilization peaked above 150%.
3. **Verification:** Passed all automated checks via `verify.sh` resulting in `GREEN CHECK: PASS`.
4. **Failure Analysis:** Documented the limitations of CPU metrics for GPU-bound engines (`vllm`) and proposed queue-depth-based scaling strategies (`hpa-failure-analysis.md`).
5. **Pre-staged Go-Live Endpoint:** Verified the namespace tunnel and external health probe (`/health`), ensuring readiness for Thursday's deployment.

---

## Troubleshooting & Incident Notes
* **Symptoms Observed:**
  - Repeated `OOMKilled` (Exit Code 137) errors causing the serving container to enter a `CrashLoopBackOff` state.
  - Intermittent `Readiness` and `Liveness` probe connection failures (`dial tcp :8000: connect: connection refused`) due to insufficient initialization time and memory starvation during startup.
  - HPA metric targets remained in an `<unknown>/50%` state because metrics-server could not scrape unready/crashing pods.
* **Root Cause:**
  - Initial memory limits (`512Mi` and `1Gi`) were insufficient to accommodate runtime allocations, model initialization, and concurrent request overhead within the container image.
* **Resolution:**
  - Increased pod resources to **`limits.memory=4Gi`** and **`requests.memory=1Gi`** (alongside extending probe initial delays).
  - Cleaned up dangling terminating pods and re-deployed the Helm release cleanly.
  - Immediately resolved container crashes, stabilized pod readiness (`1/1 Running`), and enabled metrics-server to report steady CPU utilization to the HPA.
