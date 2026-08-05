# Cycle 3 — Model Ladder and Grounding Validation

Target classification: CYCLE_3_EXTRACTION_MODELS_READY.

## Completed

- Versioned evidence-grounded packet schema.
- Deterministic numeric-comparison baseline with exact offsets.
- Pinned specialist-model identities.
- Pinned local Qwen tag and blob.
- Frozen deterministic Qwen settings: think:false, temperature 0, seed 20260719.
- Frozen ensemble fallback and abstention rule.
- Schema, evidence-offset, unsupported-field, and deterministic tests.

## Historical operational evidence

- FinBERT 100-article runtime: approximately 0.71 seconds and 0.73 GB.
- Financial-RoBERTa 100-article runtime: approximately 0.92 seconds and 1.8 GB.
- Historical Qwen 100-article runtime: approximately 1,264 seconds and roughly 26 GB VRAM.
- Repaired full Qwen run: 5,000/5,000 valid rows in 2,588.65 seconds after checkpoint reuse.

These are operational measurements, not extraction-accuracy scores.

## Performance status

- Rule baseline against human gold: PENDING_HUMAN_REVIEW.
- FinBERT against structured human gold: NOT_APPLICABLE.
- Financial-RoBERTa against structured human gold: NOT_APPLICABLE.
- Qwen v2 against human gold: PENDING_HUMAN_REVIEW.
- Ensemble against human gold: PENDING_HUMAN_REVIEW.

No precision, recall, F1, calibration, or human agreement is claimed.
