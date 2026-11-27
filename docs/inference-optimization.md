# Inference optimization experiments

[← Research overview](../README.md)

## Stage 1 — baseline and AdaptiveKV

The initial objective was 90–100 decode tokens/s at 128K or more on one 16 GB GPU, without unverified quality degradation. LM Studio Q4_K_M was the initial baseline. In the overnight synthetic comparison, Q4 achieved 10.8 tok/s; earlier long-prompt observations were approximately 7.5 tok/s at 62,865 input tokens. These are different workloads.

| Input tokens | Configuration | Cached tokens | Prefill tok/s | Decode tok/s | TTFT (s) |
|---:|---|---:|---:|---:|---:|
| 37,732 | Adaptive IQ3_S + MTP3 | 0 | 1,345.22 | 61.38 | 29.05 |
| 37,732 | Adaptive IQ4_XS target only | 0 | 1,214.69 | 39.46 | 31.09 |
| 62,865 | Adaptive IQ3_S + MTP3 | 37,476 | 955.31 | 63.68 | 26.61 |
| 62,865 | Adaptive IQ4_XS target only | 37,600 | 845.79 | 31.72 | 29.91 |

Each row generated 256 tokens; some prior observations were taken from earlier runs. At 37K, IQ4 allocated approximately 15.4 GB GPU memory. A corrected small coding test gave Q4 10/10, Adaptive IQ3 10/10 and Adaptive IQ4 9/10 with medium thinking. This is not evidence of general equivalence.

## Stage 2 — stock CUDA speculative decoding

Engine: stock LM Studio CUDA13 llama-server 2.73.0, GSQ-RCO IQ3_S, 32,768 maximum context, flash attention, Q8_0 K/V, one request at a time. All rows below generated 1,024 tokens.

| Draft count | Input | Decode tok/s | Cold prefill tok/s | TTFT (s) | Accepted / attempted drafts |
|---:|---:|---:|---:|---:|---:|
| 4 | 7,579 | 124.56 | 1,774.15 | 4.28 | 768/1016 |
| 5 | 7,579 | 129.84 | 1,795.19 | 4.23 | 808/1071 |
| 6 | 7,579 | 131.78 | 1,796.21 | 4.23 | 829/1164 |
| 4 | 22,664 | 115.67 | 1,684.53 | 9.28 | 776/986 |
| 5 | 22,664 | 112.66 | 1,672.86 | 9.34 | 797/1124 |
| 6 | 22,664 | 112.78 | 1,670.86 | 9.35 | 815/1239 |

The highest draft count won at 7.6K, not at 22.7K. Identical repeated 22.7K requests had TTFT around 0.09–0.10 seconds with cached prefixes. Draft count is workload-dependent, not a universally increasing speed lever.

## Stage 3 — memory pressure and context

Stock 64K switched to Q4 K/V. A 62,926-input, 39-output marker test reached 101.64 tok/s and retrieved three markers; the longer 1,024-output follow-up reached 78.14 tok/s. At a configured 128K, stock prefill fell to about 65.9 tok/s after processing 2,560 tokens and the run was aborted. GPU memory was about 15,890/15,996 MiB. This was not a completed 128K benchmark.

Adaptive KV streaming completed 125,765 input tokens with 203 output tokens at 30.44 tok/s and 293.28 s TTFT.

## Stage 4 — NInfer

NInfer Windows CUDA 13.4, release 2026-11-16.2+a317194, Swift 1.5 27B IQ3_S. Initial higher-precision KV allocation failed. The successful 128K experiment used RK4V4 KV, prefill chunk 256, MTP4, FP16 GDN state and one concurrent request; approximately 15,393 MiB GPU memory was in use. Median decode of three 2,048-token long-output trials was 130.26 tok/s. See [context experiments](long-context.md).

## Stage 5 — Strata and Basalt

Strata v0.2.15 / engine 0.1.60 Flash-Next MoE used Q4_0 KV and reported 32,768 resident cells per QSA layer with remaining KV in pinned host RAM in the IQ2_XS 256K experiment. This architecture is not the same model as dense Swift 27B. Selected IQ3_S balanced throughput (105.4 tok/s on the synthetic suite) and matched quality. Basalt 0.4.1 IQ3_XXS recorded four 2,048-output trials: 94.2, 93.3, 99.1, and 94.6 tok/s; median 94.4. Basalt was not retained as the primary engine.

## Stage 6 — 1M experiments and regression

A later 1M Strata experiment recorded baseline median 56.8 tok/s. Speculative configuration spec6 yielded 43.8 tok/s (0.771x) and failed its quality smoke test; it was not retained. A DFlash2 experiment could not start because of memory pressure. Both experiment records indicate baseline restoration. The 1M configurations are separate from the earlier 128K speed records.

## Takeaways

GPU residency, KV precision, model architecture, prefix reuse and speculation are intertwined. Results are selected local measurements, not controlled estimates of independent causal effects. Higher precision or larger draft counts were not consistently better on the tested workloads. No complete raw logs are distributed with this release.
