# Cycle 2 — Human Gold Benchmark

Target classification: `CYCLE_2_GOLD_BENCHMARK_READY`.

The engineering package prepares a deterministic, outcome-blind, 400-cluster review sample. Private packets contain licensed article text and remain ignored local data. The public manifest contains only nonreconstructive benchmark IDs and stratification attributes.

Stratification covers event family, source, year, article length, FinBERT sentiment, Qwen confidence, surprise availability, materiality, and easy/medium/hard cases. Human review requires at least 20% double review before inter-reviewer agreement is reported.

Human gold status: `PENDING_HUMAN_REVIEW`.

AI review status: `NOT_RUN`.

No human rating, adjudication, agreement statistic, or extraction accuracy is claimed.

## Prepared sample

- Records: 400.
- Event families represented: 17/17 present in the frozen model taxonomy.
- Years represented: 2022–2026.
- Surprise available: 347 yes, 53 no.
- Difficulty: 297 easy, 50 medium, 53 hard.
- Length: 62 short, 182 medium, 156 long.
- Private packet size: approximately 2.2 MB, ignored and not committed.
- Public records contain only benchmark ID and stratification fields.

Validation: 115 tests passed at 85.38% coverage; Ruff formatting/lint, strict mypy across 57 modules, package build, and Git diff checks passed.
