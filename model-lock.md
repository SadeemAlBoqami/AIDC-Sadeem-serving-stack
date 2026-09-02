# Model lock (team record)

## The locked model

- Model id: Qwen/Qwen2.5-1.5B-Instruct-AWQ
- Quantisation: awq
- Why this one: Passed function-calling smoke test with full tool adherence and freed substantial KV cache block capacity.

## The launch flags
--model Qwen/Qwen2.5-1.5B-Instruct-AWQ --dtype half --max-model-len 4096 --gpu-memory-utilization 0.85 --quantization awq --enable-auto-tool-choice --tool-call-parser hermes
- Tool-call parser: hermes

## The smoke score

- Score (valid behaviours out of 10): 10
- Distractor stayed call-free in the majority: yes
- Passed the gate (>= 8/10 and distractor majority clean): yes
- Measured against: AWQ

## Quality spot check note

- The AWQ quantized build preserved reasoning coherence across all five prompts without hallucination or regression compared to fp16.
