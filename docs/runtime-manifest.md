# Runtime and model revision manifest

These identities come from the historical local reports, not a fresh installation or verification of remote download URLs. Unknown hashes are explicitly left unknown.

| Configuration | Engine / runtime | Model / quantization | Context tested or configured | Recorded identity |
|---|---|---|---|---|
| Stock CUDA | LM Studio llama-server CUDA13 2.73.0 | GSQ-RCO IQ3_S | 32K, 64K; stock 128K aborted | Engine version known; weight revision/hash unavailable |
| AdaptiveKV | Adaptive KV Streaming V2 | IQ3_S / UD-IQ4_XS | 262,144 configured, ~125K measured | Exact engine and weight revision unverified |
| NInfer / Swift | Windows CUDA 13.4, SM120a, release 2026-11-16.2+a317194 | Swift 1.5 27B GSQ-RCO IQ3_S | 131,072; ~125K input | Engine and weight identity below |
| Strata | v0.2.15 / engine 0.1.60 | Flash-Next IQ2_XS, IQ3_XXS, IQ3_S; UD-IQ4_XS v3.1 | 32K / 128K / 256K; later 1M experiments | Exact weight hashes unavailable |
| Basalt | 0.4.1 | IQ3_XXS (Unsloth) | 128K configured | Exact model revision/hash unavailable |
| Lobo | SM120 Windows v0.1.1 artifact | 27B IQ3_S | Not verified in summary | Exact model hash unavailable |
| LM Studio | llama.cpp CUDA 2.73 | 27B Q4_K_M / Q3_K_XL | 262,144 configured in baseline | Exact weight revisions unavailable |

## Recorded NInfer artifact identity

- Model repository: `fyb1214/Swift-1.5-Qwen3.8-27B-GSQ-RCO-NInfer`
- Model revision: `7da3e38b9ee7a6c8888cf2112d3c5a48a952a2a8`
- Model bytes: 12,790,639,360
- Model SHA-256: `0e1771e4df425a7e05b0ffce8662cb500dc2546f3759767fe6ac2699d64c0816`
- Engine repository: `iamwavecut/ninfer-all`
- Engine release: `2026-11-16.2`
- Engine source commit: `a3171940a3574cda4d4f3bc3000df7c0944e8ad8`

The earlier report recorded matching archive and extracted-file checksums, but the executable lacked an Authenticode signature. Hash matching is not proof of trust or safety. No executable or model weights are distributed in this repository.

## Historical runtime settings

See [inference optimization](inference-optimization.md) for the recorded CUDA, KV, context and draft-count settings. Different architectures and settings are not controlled equivalents. Do not substitute unknown revisions without labeling the change.
