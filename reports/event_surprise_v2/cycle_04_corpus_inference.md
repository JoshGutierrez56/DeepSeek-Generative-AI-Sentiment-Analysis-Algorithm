# Cycle 4 — Frozen Event Corpus

Target classification: CYCLE_4_FROZEN_EVENT_CORPUS_READY.

The existing 5,000-row Qwen corpus was audited cache-first and accepted as the immutable v1 baseline. No model was loaded and no inference was restarted.

The corpus includes every frozen article, including abstentions and nontradable events. It is not filtered by market outcome.

The v1 corpus does not contain complete v2 field-to-evidence character offsets. That limitation is explicit in the manifest. V2 full-corpus re-extraction is deferred until human-gold results justify the compute and the extraction design survives review.

Required public outputs contain only aggregate counts and hashes. Licensed rows, article bodies, raw caches, and private packet mappings remain uncommitted.

## Audit result

- Rows and unique IDs/hashes: 5,000/5,000.
- Parse failures: 0.
- Abstentions: 1,476.
- Surprise-available rows: 3,524 (70.48%).
- Rows with nonempty concise evidence: 4,984 (99.68%).
- Event families: 17.
- Corpus SHA-256: f696fd2795993ff6c2a64baee7dc314e8287e85d0b0dd79ee45e41bd98121391.
- Inference restarted: no.
