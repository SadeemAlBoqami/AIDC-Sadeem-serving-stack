# HPA Failure Analysis: CPU-Based Autoscaling on GPU-Bound LLM Serving

## 1. Where Today's Scaler Fails on the Real Engine
The Horizontal Pod Autoscaler (HPA) deployed today relies exclusively on CPU utilization metrics via the metrics-server. While this works effectively for CPU-bound applications like the echo backend (where processing requests consumes direct CPU cycles per token), it fails fundamentally when applied to GPU-accelerated LLM engines such as vLLM. 

In a GPU-bound architecture, the heavy computational lifting of matrix multiplications and token generation is offloaded entirely to the hardware accelerator (GPU). Consequently, the CPU idles at minimal levels (often under 5%) to coordinate I/O and batching, even when hundreds of concurrent requests flood the inference queue and the system experiences a severe performance bottleneck. Because the CPU metric remains flat, the HPA perceives no resource pressure, refuses to scale out, and holds the deployment at a single replica during a major traffic surge.

## 2. Recommended Alternative Signals
To accurately capture load and drive autoscaling for GPU-bound LLM serving, the control loop must monitor metrics that reflect actual inference pressure and queue congestion:
* **`vllm_num_requests_waiting` (Queue Depth):** Measures the number of incoming requests currently waiting in the scheduler's queue for available KV-cache blocks or compute slots. This is the most direct indicator of traffic saturation.
* **`vllm_gpu_cache_usage_pct` (KV-Cache Utilization):** Tracks how much of the GPU memory allocated for key-value caches is saturated, signaling impending memory limits before requests start failing or timing out.
* **In-Flight Requests:** Counts the active concurrent generations being processed by the engine.

For this specific workload, **Queue Depth (`vllm_num_requests_waiting`)** is the optimal primary signal because a backlog immediately indicates that consumer demand exceeds current inference capacity, directly justifying the deployment of additional replicas.

## 3. Initial Target Numbers and Tuning Strategy
* **Starting Target Threshold:** Configure the custom metrics scaler to trigger a scale-out event when the waiting request queue exceeds a threshold of **5 to 10 waiting requests** per replica.
* **Tuning Metrics:** 
  * Monitor **p95 and p99 request latencies (Time to First Token and Inter-Token Latency)** alongside throughput to verify if the scale-out action successfully drains the queue.
  * Adjust the `scaleUpStabilizationWindow` and `scaleDownStabilizationSeconds` to prevent thrashing (rapid scaling loops) caused by short-lived bursts in LLM generation lengths.
