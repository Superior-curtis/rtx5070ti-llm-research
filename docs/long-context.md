# Long-context experiments

[← Research overview](../README.md) · [Trial data](../data/context-trials.csv)

Configured context is not measured input length. Decode throughput excludes prompt prefill. The reported 128K, 256K and near-1M results must not be conflated.

## Swift / NInfer near 128K

| Task | Input | Cached | Output | Decode tok/s | TTFT (s) | Wall (s) |
|---|---:|---:|---:|---:|---:|---:|
| Marker recall, default | 125,813 | 0 | 270 | 120.79 | 85.30 | 87.54 |
| Generation, default | 125,833 | 121,856 | 1,024 | 110.48 | 3.66 | 12.93 |
| Marker recall, budget 256 | 125,771 | 0 | 206 | 147.29 | 85.62 | 87.03 |
| Refactor, budget 256 | 125,791 | 121,856 | 1,024 | 136.95 | 3.57 | 11.05 |
| Refactor plan | 125,783 | 0 | 2,048 | 123.81 | 85.46 | 102.01 |
| Code review | 125,778 | 121,856 | 2,048 | 130.26 | 3.57 | 19.30 |
| Regression tests | 125,779 | 121,856 | 2,048 | 164.45 | 3.52 | 15.98 |

The default 1,024-token generation exhausted its budget on reasoning with no visible final answer. The budget-256 follow-up and all three 2,048-token trials produced visible answer text. Synthetic Python input used three dispersed markers; all three were recalled. The median of the three long generations is 130.26 tok/s, not the cold-prefill speed.

## Strata 128K / 256K

| Quantization | Task | Input | Output | Decode tok/s | TTFT (s) | Result |
|---|---|---:|---:|---:|---:|---|
| IQ2_XS | 128K cold recall | 120,707 | 45 | 137.3 | 37.07 | 3/3 |
| IQ2_XS | 128K long generation | 120,706 | 2,048 | 134.8 | 8.18 | Completed |
| IQ2_XS | 256K cold recall | 241,232 | 45 | 130.2 | 78.72 | 3/3 |
| IQ2_XS | 256K long generation | 241,231 | 1,732 | 134.3 | 9.20 | Completed |
| IQ3_S | 128K recall | 120,707 | Not recorded | 82.6 | 36.27 | 3/3 |
| IQ3_S | 256K recall | 230,597 | Not recorded | 84.6 | 73.24 | 3/3 |
| IQ3_S | 256K long generation | 230,596 | Not recorded | 99.1 | 5.99 | Unscored quality |

The IQ2_XS 256K multihop test retrieved all three values in all settings, but only high reasoning / 2,048 budget computed the correct checksum. No reasoning and medium/1,024 returned wrong answers. This distinction between retrieval and computation is critical.

## Near 1M

A separate later Swift retest returned HTTP 200: 985,092 input tokens, 985,087 cached, 111 output tokens, 2.0 s elapsed and exact marker match. This establishes a warm-cache request at this token count, not cold prefill speed, full-context comprehension or model parity. Free system RAM was recorded as 2.4 GB.

## Limits

Long context can consume most available memory. Cache-matched tasks are not identical to uncached tasks; warm and cold results are labeled separately. A three-marker test is a narrow capacity check and does not demonstrate robust arbitrary document reasoning.
