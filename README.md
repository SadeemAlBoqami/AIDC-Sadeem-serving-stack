# AIDC-W2D1

Measurement results (from results.json for model Qwen/Qwen2.5-1.5B-Instruct).

| dtype | predicted GB | measured GB | observed bytes/param | tokens/s |
| :--- | :---: | :---: | :---: | :---: |
| fp16 | 3.00 | 3.29 | 2.19 bytes/param | 23.3 |
| int8 | 1.50 | 1.87 | 1.25 bytes/param | 5.3 |
| int4 | 0.75 | 1.24 | 0.83 bytes/param | 12.8 |