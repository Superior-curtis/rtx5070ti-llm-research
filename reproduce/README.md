# Reproduce the experimental method

The reference Python harness is newly authored for this repository. It uses synthetic records and a local OpenAI-compatible streaming API. It is not the historical benchmark runner and does not guarantee identical tokenization, prompts, scores or engine throughput.

## Requirements

Python 3.10+, a running local model endpoint, and its exact model ID. Start with a small request and ensure adequate system/GPU memory. The script does not load models, install binaries, alter model settings, or send requests to public servers. Use the runtime's official documentation and trusted downloads for setup.

```bash
python reproduce/benchmark.py --self-test
python reproduce/benchmark.py --model YOUR_LOCAL_MODEL_ID --task recall --records 100 --max-tokens 256 --repeat 2
python reproduce/benchmark.py --model YOUR_LOCAL_MODEL_ID --task generation --records 100 --max-tokens 1024 --repeat 2
```

Use `--base-url` for a different loopback API. If authentication is required, set the `LOCAL_LLM_API_KEY` environment variable locally; never paste it into results or commits. The script appends JSONL. Some endpoints do not support streaming usage or reasoning deltas; missing usage stays null. An HTTP error is retained as an error, not a failed accuracy score.

## Measuring fairly

- Adjust record count gradually; actual tokens come from server usage, not record count.
- Keep sampling, model revision, context capacity, runtime version and output cap fixed.
- First request and repeated request are *intent labels*, not proof of cold/warm cache. Inspect the server's cache metrics or reset the session using its documented controls.
- TTFT means first received nonempty reasoning or text delta; first visible latency is separate.
- Client streaming throughput is an estimate, not engine-reported decode speed. Use engine metrics to compare against historical server decode values.
- Keep visible answer availability separate from generated-token throughput.
- Record failures, prompt and completion lengths, and all valid repetitions. Do not discard slower trials.
- Exact marker matching is only a narrow retrieval test; it is not a reasoning benchmark.

## Historical results

See [trial manifest](../data/trials/README.md) for metrics extracted directly from the recorded JSONL logs, and [runtime manifest](../docs/runtime-manifest.md) for known revisions. The original full prompts, responses and benchmark scripts are not redistributed. For exact replication of the external coding benchmark, consult its original repository and recorded revision in the project README.
