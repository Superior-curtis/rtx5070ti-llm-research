# Beyond 16GB: High-Speed Local LLM Inference on a Single RTX 5070 Ti

An independent experimental study of local language-model inference, quantization, long-context memory management, coding agents, and single-GPU serving. Experiments conducted in November 2026. This is a research report, not a new model release or an official leaderboard.

[繁體中文](README.zh-TW.md) · [Benchmark data](benchmarks.csv) · [Methodology](METHODOLOGY.md)

## Highlights

- **130.26 tokens/s median decode** across three 2,048-token generations at approximately 125K input tokens using Swift IQ3_S and NInfer (one cold and two cached requests).
- **134.3 tokens/s** at 241,231 input tokens using Strata IQ2_XS, with 1,732 generated tokens and a reused prefix.
- **985,092 input tokens** in a successful warm-cache retrieval test; this is not a cold 1M-context throughput result.
- **66/70 MMLU-Pro** and **22/30 AIME** on fixed public subsets using Strata IQ3_S.
- **28/29 QuixBugs repairs** using Swift/NInfer in a reproduction of a published coding experiment.

## Hardware

| Component | Configuration |
|---|---|
| GPU | Single NVIDIA RTX 5070 Ti, 16 GB VRAM |
| CPU | AMD Ryzen 7 9700X |
| RAM | 64 GB DDR5 |
| OS | Windows 11 |

## 1. Quantization and engine comparison

| Configuration | Synthetic decode (tokens/s) | GPQA | AIME | MMLU-Pro | MATH |
|---|---:|---:|---:|---:|---:|
| Strata IQ2_XS | 138.8 | 49/60 | 18/30 | 58/70 | 60/60 |
| Strata IQ3_XXS | 115.4 | 49/60 | 19/30 | 62/70 | 60/60 |
| Strata IQ3_S | 105.4 | 49/60 | 22/30 | 66/70 | 59/60 |
| Basalt IQ3_XXS | 94.4 | 49/60 | 22/30 | 62/70 | — |
| Swift IQ3_S (96K) | 94.2 | 43/60 | 17/30 | 59/70 | 57/60 |
| Strata UD-IQ4_XS | 47.6 | 21/25 | 7/12 | 22/24 | 20/20 |
| Lobo IQ3_S | 53.8 | 13/30 | 4/16 | 25/37 | 29/30 |
| LM Studio Q4_K_M | 10.8 | 2/5 | 1/3 | 8/9 | 4/6 |
| LM Studio 27B Q3_K_XL | 10.6 | 1/4 | 1/3 | 6/9 | 3/5 |
| AdaptiveKV UD-IQ4_XS | 10.5 | 1/3 | 1/3 | 6/9 | 5/6 |

These results combine different architectures, context settings, and output lengths (512 or 2,048 tokens); Basalt is the median of four 2,048-token trials. Incomplete subsets are not comparable to completed subsets as official scores. The full-coverage Strata IQ3_S configuration was selected for its measured speed/quality trade-off rather than maximum raw throughput. On the same 70 MMLU-Pro questions, IQ3_S answered eight more correctly than IQ2_XS (paired exact McNemar p=0.0078, exploratory single-run comparison).

## 2. Long-context experiments

| Configuration | Actual input tokens | Output tokens | Decode tok/s | TTFT (s) | Cache |
|---|---:|---:|---:|---:|---|
| Stock IQ3_S 64K | 62,950 | 1,024 | 78.14 | 0.51 | Warm |
| AdaptiveKV IQ4 128K | 125,765 | 203 | 30.44 | 293.28 | Cold |
| Swift/NInfer 128K | 125,783 | 2,048 | 123.81 | 85.46 | Cold |
| Swift/NInfer 128K | 125,778 | 2,048 | 130.26 | 3.57 | Warm |
| Swift/NInfer 128K | 125,779 | 2,048 | 164.45 | 3.52 | Warm |
| Strata IQ2_XS 128K | 120,706 | 2,048 | 134.8 | 8.18 | Partial reuse |
| Strata IQ2_XS 256K | 241,231 | 1,732 | 134.3 | 9.20 | Warm |
| Strata IQ3_S 256K | 230,596 | Not recorded in summary | 99.1 | 5.99 | Warm |

The original stock 128K configuration was aborted during prefill under severe memory pressure. Strata IQ2_XS cold retrieval at 241,232 tokens required 78.72 seconds to first token and correctly retrieved all three markers. A separate near-1M Swift warm-cache test reported 985,092 input tokens, 985,087 cached tokens, 111 output tokens and a correct marker in 2 seconds. No claim of full 1M cold-input validation or comprehensive 1M reasoning is made.

## 3. Coding and reasoning

A same-task reproduction of the AI Pruner experiment used Swift/NInfer rather than the author's original engine and weights.

| Test | Published reference (as recorded in local report) | Local result |
|---|---:|---:|
| QuixBugs repair | 27/29 | 28/29 |
| QuixBugs elapsed | 589 s | 206 s |
| 2048 game logic | 5/5 | 5/5 (95/95 assertions) |
| Tetris syntax/features | 3/3 | 3/3 |
| Math without tools | 4/8 | 3/8 |
| Math with Python tools | 8/8 | 8/8 |

Tetris feature checks do not establish complete game correctness. Tool-assisted mathematics was substantially more reliable than unaided answers in this small sample. Increasing the reasoning budget from 256 to 1,024 improved Swift's hard-task subset from 5/8 to 7/8; 2,048 produced no further gain in that subset.

## 4. What did not work

- Stock 128K prefill was too slow and was aborted.
- NInfer's initial higher-precision KV configuration did not fit the 16 GB GPU; a more compact KV representation was required.
- A later Strata 1M speculative-decoding experiment reduced median throughput from 56.8 to 43.8 tokens/s and failed its quality smoke test. An additional draft configuration failed to start because of memory pressure. Neither experimental preset was retained.
- Some early LM Studio runs selected the wrong model ID. Those results were invalidated; corrected results are shown above.
- The overnight benchmark ended with partial coverage, not a complete evaluation of all configurations.

## 5. Serving architecture

The project evolved toward a single-GPU service with an OpenAI-compatible API, model routing, queueing, streaming, idle model scheduling, and a dashboard for GPU and game-mode control. OpenWebUI and OpenCode were integration targets; image and video pipelines were explored through ComfyUI. Basic vision tests passed on two variants, but full end-to-end OpenCode reliability, concurrent workloads and media generation through every frontend were not established.

## 6. Conclusions

A single 16 GB consumer GPU can achieve sustained generation above 100 tokens/s at 128K-class inputs under selected workloads, and some configurations support substantially longer contexts. Decode throughput alone does not describe perceived latency: cold prefill can take over a minute. Lower precision, model architecture, runtime and cache behavior all affect the result. The chosen general-purpose configuration was Strata IQ3_S, not necessarily the fastest configuration.

No equivalence to GPT or Claude is claimed. These are local experimental results, not official benchmark scores. Raw logs and third-party weights are not included in this initial publication; the aggregate data is transcribed from historical experiment summaries.

## References

- [AI Pruner reproduction source](https://github.com/aipruner/qwen3.8-3bit-test-in-16GB-GPU) — recorded commit `17a3ea44f094c2d9d0e7c09b198ae0397b494679`.
- [QuixBugs](https://github.com/jkoppel/QuixBugs) — recorded commit `4257f44b0ff1181dedaedee6a447e133219fcebf`.
- [Strata](https://github.com/Niko1221/Strata).
- [NInfer](https://github.com/iamwavecut/ninfer-all).

Reference URLs and revisions are taken from the historical experiment records and have not been revalidated for this publication.
