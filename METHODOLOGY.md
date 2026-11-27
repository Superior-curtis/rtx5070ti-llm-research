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

For reproducibility, publish reviewed raw trial records and exact runtime versions in a later release. The initial release is an aggregate report, not a fully reproducible benchmark suite.
