# Serving Stack (Week 2): OpenAI-Compatible CPU Inference Service

A lightweight, production-structured inference microservice built with FastAPI and Hugging Face Transformers. It serves the `Qwen/Qwen2.5-0.5B-Instruct` model behind an OpenAI-compatible `/v1` HTTP API contract entirely on CPU.

---

## 📌 Features & API Contract

- **`GET /health`** — Liveness and readiness probe returning service and model status.
- **`GET /v1/models`** — Returns the served model metadata formatted as a standard OpenAI `ModelList`.
- **`POST /v1/chat/completions`** — Non-streaming completions endpoint supporting chat templates, token slicing, finish reason determination, and full usage metrics.

---

## 🛠️ Tech Stack & Dependencies

- **Framework:** FastAPI, Uvicorn
- **Model:** `Qwen/Qwen2.5-0.5B-Instruct`
- **Inference Engine:** Hugging Face `transformers` (v4.46.2), PyTorch CPU (v2.5.1)
- **Validation:** Pydantic v2

---

## 🚀 Setup & Execution

### 1. Environment Setup

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🧪 Verification & Testing

### 1. Server Execution & 200 OK Endpoints
Logs showing successful initialization of `Qwen/Qwen2.5-0.5B-Instruct` and healthy responses across `/health`, `/v1/models`, and `/v1/chat/completions`:

![FastAPI Uvicorn Server Logs & HTTP Status Checks](images/W2D2-1.png)

### 2. Client Test & Full Verification Pass
Successful inference via the official OpenAI client followed by the test suite pass:

![Client Verification & Test Suite Pass (GREEN CHECK)](images/W2D2-2.png)

---

### 3. Contract Fuzzing Suite (Extra Lab)

Run adversarial and malformed payload tests to verify schema resilience against invalid inputs:

```bash
python fuzz_client.py
```

#### Result & Server Interception:

1. Server-Side Request Interception
Uvicorn access logs demonstrating strict Pydantic validation intercepting invalid payloads with `422 Unprocessable Entity` before compute dispatch, while allowing valid requests with 200 OK:

![Server-side Validation](images/W2D2-3.png)

2. Test Suite Execution & Concurrency Probe
Full test run achieving a `12/12` pass rate (`GREEN CHECK: PASS`) and confirming expected serial execution for synchronous CPU inference:

![Test Suite Results](images/W2D2-4.png)

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

### Architectural Differences & Methodology
- **Core Lab (Inference Service)**: Used a single slim stage with a decoupled external cache volume (`hf-cache`) to handle massive dependencies (PyTorch/Transformers) dynamically without baking model weights into the image.
- **Extra Lab (Multi-Stage Golf)**: Applied a dual-stage build pattern (`builder` vs `runtime`) on a lightweight FastAPI registry service. Dependency wheels and build artifacts were isolated in `--prefix=/install/deps`, and only essential runtime binaries and explicit application files (`main.py`, `registry.json`) were copied across the boundary.

### Size Comparison Report

| Build Stage | Image Tag | Target | Final Image Size | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Build** | `registry:naive` | Baseline | **236 MB** | Baseline |
| **Multi-Stage Build** | `registry:multistage` | < 300 MB | **51.9 MB** | `GREEN CHECK: PASS` |


---

