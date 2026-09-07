# Week 4 Day 1: First Cluster — Multi-Tenancy & Pod Diagnostics

Operational log for configuring isolated Kubernetes namespaces on a shared `k3s` cluster, diagnosing scheduling and runtime failures, and deploying a functional LLM serving microservice.

---

## Environment

* **Cluster:** `k3s` on `aidc-t09` (NVIDIA RTX A6000)
* **Namespace:** `sadeem`
* **Base Image:** `sadeemalboqami/aidc-serving:cpu-v1`

* **Target Model:** `Qwen/Qwen2.5-0.5B-Instruct`


---

## Triage: The Three Refusals

| Pod | Observed Status | Component Responsible | Root Cause |
| --- | --- | --- | --- |
| `pod-a` | `ImagePullBackOff` | `kubelet` | Non-existent image tag on remote registry (`busybox:this-tag-does-not-exist`). |
| `pod-b` | `Pending` | `default-scheduler` | Insufficient compute capacity; requested 64 CPU cores on a 28-core physical node. |
| `pod-c` | `CrashLoopBackOff` | Container Runtime | Application crash on launch exiting with internal failure (`Exit Code: 3`). |

---

## Deployment & Verification

1. **Deploy Workload**

```bash
kubectl apply -f pod.yaml
kubectl get pods -w

```


2. **Port-Forward & Probe Endpoints**
```bash
kubectl port-forward pod/serving 8001:8000

```


* Readiness check (`/health`): Returns HTTP `200` (`{"status":"ok"}`).
* Model listing (`/v1/models`): Confirms `Qwen/Qwen2.5-0.5B-Instruct` is registered.
* Inference test (`/v1/chat/completions`): Validates request routing and JSON payload completion.


3. **Automated Cluster Validation**

```bash
bash verify.sh

```


* Output: `GREEN CHECK: PASS`

* Evidence: Saved cluster state to `w4d1_evidence.json`.





---

## Hardware Contention Note (Stretch)

* Requesting exclusive GPU resources via `[nvidia.com/gpu](https://nvidia.com/gpu): 1` places concurrent pods into `Pending` state (`Insufficient [nvidia.com/gpu](https://nvidia.com/gpu)`) due to indivisible device locking.
* CPU workloads run unaffected during GPU allocation bottlenecks.
