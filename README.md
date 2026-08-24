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

### Official OpenAI Client Test

Run the reference client test against the local server:

```bash
python app/client_test.py
```

### Full Verification Suite

Execute the lab test suite to confirm the contract integrity:

```bash
python verify.py
```

---

## 🧪 Verification & Testing

### Official OpenAI Client Test

Run the reference client test against the local server:

```bash
python app/client_test.py


---

## 📝 Design Considerations

- **CPU Execution:** Floating-point operations run entirely on the CPU (`torch.float32`).
- **Concurrency:** The current design executes inference synchronously per request; scalable queueing and async concurrency belong to the serving engine layer.
