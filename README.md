# LLM Serving Stack: Compose, Authentication & Resource Guardrails (W2D5)

## 📌 Concept & Objective
Transitioning the LLM inference service from manual container executions to a production-ready, declarative orchestration stack managed via **Docker Compose**. The primary goals are:
- Encapsulating environment configuration and persistent weight caching.
- Implementing API security via Bearer Token authentication.
- Preventing Denial-of-Service / unbounded GPU compute consumption through request token clamping.
- Establishing zero-dependency container health probing suitable for orchestrators.

---

## 🛠️ Implementation Architecture

* **Orchestration (`compose.yaml`):** Configures single-command deployment, persistent model volume caching (`hf-cache`), auto-restart policies, and a Python-native healthcheck independent of external binaries like `curl`.
* **API Security & Routing:**
  - Enforced `Authorization: Bearer <API_KEY>` on inference endpoints (`/v1/*`) returning `401 Unauthorized` for invalid or missing credentials.
  - Kept `/health` unauthenticated (`200 OK`) to allow Kubernetes/Compose liveness and readiness probing.
* **Compute Guardrails:** Clamped `max_tokens` dynamically against a defined environment ceiling (`MAX_TOKENS`) to prevent resource exhaustion attacks.
* **Environment Separation:** Maintained configuration templates in `.env.example` while securing active credentials within git-ignored `.env` files.

---

## 📊 Verification & Results

The stack achieved full automated verification via `verify.sh`:
- **Liveness Probes:** `/health` responded with `200 OK` unauthenticated.
- **Access Control:** `/v1/models` successfully rejected unauthenticated requests (`401`) and allowed authenticated requests (`200`).
- **End-to-End Inference:** `/v1/chat/completions` generated validated OpenAI-compatible responses under token ceilings.
- **Shipped Checkpoint:** Passed with `GREEN CHECK: PASS`.

![W2D5 Verification Pass](images/W2D5%20lab.png)
