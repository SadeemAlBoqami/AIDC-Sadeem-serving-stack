# Serving Stack (Week 2): OpenAI-Compatible CPU Inference Service

A lightweight, production-structured inference microservice built with FastAPI and Hugging Face Transformers. It serves the `Qwen/Qwen2.5-0.5B-Instruct` model behind an OpenAI-compatible `/v1` HTTP API contract entirely on CPU.

---

## Container Size Report (W2D3)

| Stage | Image Tag / Build | Compressed (Pull) Size | Disk (Uncompressed) Size |
| :--- | :--- | :--- | :--- |
| **Naive Build** | `aidc-serving:naive` | ~6.88 GB | ~17.9 GB |
| **Slim Build** | `sadeemalboqami/aidc-serving:cpu-v1` | ~625 MB | ~3.03 GB |

### Verification
- Image: `sadeemalboqami/aidc-serving:cpu-v1`
- Status: `GREEN CHECK: PASS`

![Image Validation](images/W2D3-Step5.png)

---
---

## Extra Lab: Multi-Stage Build Golf (Model Registry Service)

### Architecture & Optimization Methodology
- **Dual-Stage Separation**: Built dependencies in an isolated `builder` stage (`--prefix=/install/deps`) and copied only clean binaries into the runtime image to strip build tools, pip caches, and unnecessary artifacts.
- **Selective Copying**: Whitelisted application runtime files (`main.py`, `registry.json`) instead of copying the whole repository context.

### Size Comparison Report

| Build Stage | Image Tag | Target | Final Image Size | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Build** | `registry:naive` | Baseline | **278 MB** | Baseline |
| **Intermediate Multi-Stage** | `registry:multistage` | < 300 MB | **227 MB** (18.3% savings) | Fits Target |
| **Optimised Multi-Stage** | `registry:multistage` | < 300 MB | **51.9 MB** | `GREEN CHECK: PASS` |

### Verification Artifacts

**1. Multi-Stage Size Report Execution:**
![Size Report Output](images/W2D3-Extra-lab2.png)

**2. Automated Verifier Green Check:**
![Verification Pass](images/W2D3-Extra-lab1.png)

