# Lab W3D4: Quantise and Lock the Model

## Overview
Serving an AWQ 4-bit quantized model (`Qwen/Qwen2.5-1.5B-Instruct-AWQ`) using **vLLM** on an NVIDIA T4 GPU. The lab validates memory pool allocation, evaluates generation quality, and gates the model via a function-calling smoke test before locking it for production serving.

---

## 1. VRAM Dynamics: Pool vs. Weights
* **Resident VRAM (`nvidia-smi`):** Read **$12,843\text{ MiB}$** ($\approx 12.8\text{ GB}$).
* **The Mechanism:** Quantizing weights from FP16 ($\approx 2.5\text{ GB}$) to INT4 ($\approx 0.9\text{ GB}$) did not shrink the total reported VRAM. Because `--gpu-memory-utilization 0.85` pre-allocates a static pool, vLLM repurposed the freed memory directly into additional **KV-cache blocks**, expanding concurrency headroom rather than lowering card-level allocation.

---

## 2. Quality Spot Check (5 Prompts)
A comparative check confirmed zero semantic degradation between FP16 and AWQ:
* **System Summary:** Concisely captured inference server responsibilities.
* **Tool Identification:** Correctly targeted weather and timezone capabilities without prompt drift.
* **Technical Refactoring:** Accurately consolidated the memory-bound decode constraint.
* **Operational Reasoning:** Produced a logical step-by-step rollback sequence.
* **Intuition / Analogy:** Clearly abstracted precision loss and quantization trade-offs.

---

## 3. Function-Calling Smoke Test Gate
* **Model Tested:** `Qwen/Qwen2.5-1.5B-Instruct-AWQ`
* **Tool Parser:** `hermes`
* **Final Score:** **$10 / 10$ (100% Pass)**

| Test Scenario | Attempts ($k$) | Valid Executions | Restraint (Call-Free) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Dual Tool (`two_tool`)** | 4 | 4 / 4 | 0 (Calls made) | Passed |
| **Single Tool (`single`)** | 4 | 4 / 4 | 0 (Calls made) | Passed |
| **Distractor (`distractor`)** | 2 | 0 (Restrained) | 2 / 2 Clean | Passed |

*The model demonstrated both tool adherence on demand and restraint on distractors, clearing the $\ge 8/10$ acceptance threshold.*

---

## 4. Locked Configuration (`model-lock.md`)
* **Model ID:** `Qwen/Qwen2.5-1.5B-Instruct-AWQ`
* **Quantization:** `awq`
* **Runtime Flags:**
  ```bash
  python3 -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-1.5B-Instruct-AWQ \
    --dtype half \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.85 \
    --quantization awq \
    --enable-auto-tool-choice \
    --tool-call-parser hermes
