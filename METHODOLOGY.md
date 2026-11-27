# Methodology and provenance

Data transcribed from local experiment summaries dated November 18–23, 2026. No new benchmark was run for this release. No credentials, private endpoints, device identifiers, or personal records are included.

## Source manifest (relative paths within original laboratory archive)

- `BenchmarkOvernight-20261118/REPORT.md` — aggregate speed and fixed public subsets; incomplete coverage; corrected model routing.
- `AdaptiveKV/RESULTS-2026-11-18.md`, `RESULTS-LONG-CONTEXT-20261118.md`, `RESULTS-MTP-SWEEP-20261118.md` — stock and adaptive inference experiments.
- `NInfer/FINAL-128K-RESULTS-20261118.md` — long-context Swift tests, cold and warm cache, 2,048-token runs.
- `StrataLab/STRATA-128K-256K-VS-SWIFT-20261118.md` — long-context retrieval and reasoning.
- `ArticleRepro/FINAL-AI-PRUNER-REPRO-20261118.md` — coding and math reproduction.
- `IntelligenceEval/REASONING-AND-STRATA-20261118.md` — reasoning budgets.
- `BenchmarkResults/Basalt-20261119/STATUS.json` — Basalt speed and quality.
- `OpenWebUI/swift-1m-output-retest.json`, `strata-1m-spec6-experiment-status.json`, `strata-1m-dflash-experiment-status.json`, `vision-test-results.json` — later integration experiments.

## Definitions

Decode tok/s is generated tokens per second, not full end-to-end speed. TTFT is time to first token. Cold and warm cache experiments must be reported separately. Configured context capacity is not the same as measured input length. Quality scores are fixed public subsets (GPQA 60, AIME 30, MMLU-Pro 70, MATH 60 where fully completed). Missing values are not zero. Different model architectures and quantizations are not controlled equivalents. No official Artificial Analysis Intelligence Index or proprietary-model parity claim is made.

For reproducibility, publish reviewed raw trial records and exact runtime versions in a later release. The initial release was an aggregate report. The expanded release includes six historical per-trial metric extracts and a reference harness, but remains short of a fully reproducible historical benchmark suite.


## Published files and measurement grain

| File | Grain | Notes |
|---|---|---|
| `benchmarks.csv` | One row per configuration | Aggregate quality numerators/denominators and synthetic decode speeds; mixed output lengths |
| `data/context-trials.csv` | One row per reported long-context trial | Input, cached and output tokens; decode, TTFT, wall time; blank means unrecorded in summary |
| `data/mtp-sweep.csv` | One row per draft-count/input-size experiment | 1,024 generated tokens per row; stock CUDA, IQ3_S, Q8 K/V |
| `docs/` | Narrative by experiment family | Runtime versions, model differences, failure cases, and interpretation |

All values were transcribed from the laboratory summaries rather than inferred from file names. The files are not raw logs; some row fields remain unreported. For comparisons that require equivalent tasks, replay the same prompt set, generation cap, sampling parameters, reasoning budget, cache condition and model revision. Separate speed, final-answer correctness, visible-answer availability, and request errors.

## Reproducibility status

This release publishes enough detail to understand the observed trade-offs and reproduce the analysis of the published aggregates, but not enough to independently rerun every experiment. Unfiltered raw logs and historical test harnesses still require review before redistribution. References are from local experiment records and have not been independently revalidated.

## Per-trial release and verification

[Trial manifest](data/trials/README.md): 155 rows from six historical JSONL files. Each source line is represented by an allowlisted record; numeric precision and null/boolean fields are preserved. Free text is omitted and only predefined categorical strings are allowed. Re-fetching all six published files confirmed their row counts and reproduced the NInfer long-output median (130.26307445610155 tok/s), Swift reasoning-level scores (17/24, 17/24, 18/24, 18/24), and thinking-budget scores (5/8, 7/8, 7/8).

[Runtime manifest](docs/runtime-manifest.md) records available historical revision identifiers. [Reference harness](reproduce/benchmark.py) is newly authored and passed its offline self-test on the original Windows experiment PC using portable Python 3.12. It has not been validated against a live model endpoint. These checks do not independently verify historical answer correctness or all benchmark trials.
