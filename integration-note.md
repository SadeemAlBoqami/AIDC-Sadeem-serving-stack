# Integration note: Team 08 (v1, go-live)

- **base_url**: http://localhost:8045/v1
- **service root**: http://localhost:8045
- **model id**: Qwen/Qwen2.5-0.5B-Instruct
- **auth**: bearer key, handed over in person
- **modalities**: text in, text out, tool calls per the OpenAI schema.
- **example call**: curl http://localhost:8045/v1/models -H "Authorization: Bearer REDACTED"
- **SLOs we publish**: availability 99% over the window · TTFT p95 150 ms · error rate 1%
- **limits, declared honestly**: max_tokens clamp 2048 · concurrency knee 10
- **on-call**: Sadeem · Slack channel
