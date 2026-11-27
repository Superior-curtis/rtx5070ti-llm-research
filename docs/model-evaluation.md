# Model quality and agent evaluation

[← Research overview](../README.md)

## Fixed public subsets

The main overnight suite used GPQA Diamond (60), AIME 2026 (30), MMLU-Pro (70), MATH-500 (60 selected items) and an AA public exact-answer sample (72). GPQA/AIME requested high reasoning with 2,048 thinking budget, MMLU medium/1,024; MATH selected 12 from each difficulty level with Math-Verify final-answer checking. The benchmark stopped with partial coverage for some configurations. AA exact match is not the official Artificial Analysis Intelligence Index.

| Matched benchmark | N | Both correct | IQ2 only | IQ3_S only | Both wrong | Exact McNemar p |
|---|---:|---:|---:|---:|---:|---:|
| GPQA | 60 | 44 | 5 | 5 | 6 | 1.0000 |
| AIME | 30 | 17 | 1 | 5 | 7 | 0.2188 |
| MMLU-Pro | 70 | 58 | 0 | 8 | 4 | 0.0078 |

These exploratory single-run comparisons are not corrected for multiple comparisons and do not establish universal superiority. In a separate paired IQ3_S vs Swift 96K test, MMLU was 66/70 vs 59/70 (p=0.03906). Quality and runtime settings differed. Full denominator counts are in [benchmarks.csv](../benchmarks.csv).

## Swift reasoning level experiment

24 matched tasks (16 MMLU-Pro and 8 independently verified novel reasoning problems), four effort levels, temperature 0, no tools, output cap 2,048, default thinking budget 256.

| Effort | Correct | Final answer | Median tok/s | Median elapsed (s) | Median output tokens |
|---|---:|---:|---:|---:|---:|
| None | 17/24 | 19/24 | 173.71 | 5.26 | 830.5 |
| Low | 17/24 | 23/24 | 171.19 | 3.67 | 617.5 |
| Medium | 18/24 | 23/24 | 164.20 | 3.16 | 507.5 |
| High | 18/24 | 24/24 | 150.89 | 2.12 | 285 |

Higher effort was faster end-to-end in this subset because it generated fewer tokens, not because decode was faster.

Eight hard tasks under separate per-request budget overrides:

| Effort / budget | Correct | Median tok/s | Median elapsed (s) |
|---|---:|---:|---:|
| Low / 256 | 5/8 | 185.74 | 4.96 |
| Medium / 1,024 | 7/8 | 164.49 | 7.24 |
| High / 2,048 | 7/8 | 162.69 | 5.06 |

## Reproduction: coding agents

A same-task reproduction used a different engine and quantization than the original AI Pruner experiment (recorded revisions in the README).

| Test | Original reference (historical report) | Local result |
|---|---:|---:|
| QuixBugs | 27/29 | 28/29 |
| Wall time | 589 s | 206 s |
| Agent tool calls | 175 | 160 |
| Tool JSON errors | 0 | 0 |
| Test-file cheating | 0 | 0 |
| 2048 Python logic | 5/5 | 5/5, 95/95 assertions |
| Tetris syntax / feature checks | 3/3 | 3/3, 14/14 each |
| Math no tools | 4/8 | 3/8 |
| Math with Python | 8/8 | 8/8 |
| Math tool elapsed | 123 s | 61 s |
| Tool stress | — | 24/24 valid and semantically correct |

The QuixBugs result is from a corrected complete rerun after a Windows unittest environment issue. Tetris browser interaction found no JS page errors, but scoring and line clearing were not comprehensively verified. Different hardware/runtime settings and limited repetitions prevent a causal comparison to the reference.

## Speed across output types

The public reproduction harness recorded 177.1 tok/s on Python LRU cache (448 tokens), 193.5 on HTML/JS animation (600), 117.6 on English prose (600), and 106.4 on Traditional Chinese prose (600). Mean 148.7 tok/s; tasks differ in token counts and content. This illustrates workload dependence, not an average production guarantee.

## Basic multimodal and function tests

Two vision variants (Strata IQ3_S and Swift IQ3_XXS) reported a 128K capacity and correctly identified red on a simple image. The NInfer summary records 3/3 basic valid function-calling modes. Neither test establishes broad multimodal competence or reliable autonomous integration across arbitrary tools.

## Interpretation

The chosen general-purpose configuration was Strata IQ3_S. Its MMLU improvement over lower-precision variants and stronger AIME result justified the throughput trade-off in this local suite. Tool-assisted calculation was much more reliable than unassisted exact arithmetic on the eight-task sample. No GPT or Claude parity test was performed.
