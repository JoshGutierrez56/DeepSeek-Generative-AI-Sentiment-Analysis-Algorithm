# Event Surprise V2 Model Card

Status: EXTRACTION_MODELS_READY; human-gold performance is PENDING_HUMAN_REVIEW.

## Ladder

1. Deterministic rules extract only explicit numeric comparisons and exact evidence offsets.
2. Pinned FinBERT and Financial-RoBERTa provide sentiment/certainty baselines, not event-surprise truth.
3. Pinned local Qwen emits strict structured packets with think:false, temperature 0, and a fixed seed.
4. The frozen ensemble accepts an LLM packet only when schema and evidence offsets validate; otherwise it preserves supported rule fields and abstains.

No cloud adjudicator is authorized.

## Intended use

Private research extraction, human review triage, and empirical feature construction. The model does not provide investment advice, establish facts without evidence, or predict employability.

## Known limitations

- Existing Qwen v1 outputs do not contain complete v2 field-to-evidence offsets.
- The 400-packet benchmark has no human labels yet.
- Specialist sentiment models do not measure expectation-adjusted surprise.
- Historical v1 return outcomes cannot validate v2 extraction quality.
- Model confidence is not calibrated probability until human gold exists.
