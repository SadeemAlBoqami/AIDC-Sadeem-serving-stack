# W3D3 Lab: vLLM

## Objective:

## Predictions card:

- At concurrency 8, I predict vLLM's throughput will be about 2.5x times Monday's static-batch-8 baseline.
- Based on my baselines.json, static batching scaled 2.88x from batch 1 to 8 (81.1 / 28.2).
- For vLLM running the identical queue, I predict it will scale 4x from concurrency 1 to 8.
- Because continuous batching eliminates slot efficiency collapse under mixed output lengths, I expect vLLM's scaling multiple to be larger than static batching's, and roughly 1.4x larger.

  ---
