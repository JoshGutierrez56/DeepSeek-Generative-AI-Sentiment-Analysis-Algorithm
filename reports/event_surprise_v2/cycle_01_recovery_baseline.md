# Cycle 1 — Recovery, Baseline Audit, and Pre-registration

Classification: `CYCLE_1_EVENT_SURPRISE_BASELINE_READY`

## Recovered authority

- Repository: `JoshGutierrez56/sentiment-lab-financial-news-research`
- Actual visibility: `PUBLIC` (the supplied historical prompt incorrectly described it as private)
- Recovered event-surprise branch: `agent/event-surprise-redesign`
- Validated event-surprise branch commit: `cc1c180be802d917e707bd90d3f9fac46ed0ff72`
- Latest validated release base: `main` at `0d6be1666811b853d954cf004b760f9595381f67`
- New branch: `feat/event-surprise-empirical-v2`
- Existing expectation-adjusted worktrees remain separate and untouched.

`git diff --check` passed. `git fsck --full` found only unreachable blobs and no corrupt object. The remote was fetched without history rewriting.

## Corpus and model reconciliation

The previously interrupted Qwen job was repaired before this cycle. It must not be restarted.

- Frozen articles: 5,000 rows, 125 issuers, 5,000 pre-existing story clusters, 2022-01-03 through 2026-03-31.
- Article SHA-256: `8ada422fcdefa894c55ae51400e073f97fa6d8e26272cde98d8926ce27b68385`.
- Price SHA-256: `4f030c49deea3dd536dcb4d06f3b41d8447492ebfae2370d3646bb615ce79615`.
- Canonical local classifications SHA-256: `a1bd6afa5d015b17c16412c1116342cb2203f64f1a4d14d102d8d9bae7180df7`.
- Final Qwen rows: 5,000/5,000 contract-valid and unique.
- Final Qwen SHA-256: `f696fd2795993ff6c2a64baee7dc314e8287e85d0b0dd79ee45e41bd98121391`.
- Derived signal SHA-256: `9388d59a609fcbef9e5b9cb91bfdfcdccd5fffa71ad424c9b76f9ebfd47efdf5`.
- Model tag: `qwen3.6:35b-a3b`.
- Ollama model ID: `07d35212591f`.
- Model blob SHA-256: `f5ee307a2982106a6eb82b62b2c00b575c9072145a759ae4660378acda8dcf2d`.
- Completed Qwen runtime: 2,588.65 seconds for 5,000 rows, 115.89 articles/minute, zero invalid final rows.
- No model is currently loaded in Ollama and no event-surprise inference worker is running.

The operational `classifier_predictions.parquet` is not the canonical classification artifact. Its distinct byte hash is expected because it retains execution telemetry. The scientific artifact is `data/results/hybrid_local_3c4cdaf2fd9d9a16/classifications.parquet`, whose hash matches the recorded reproducibility contract.

## Historical result reconciliation

The earlier generic-sentiment five-session gross Sharpe was 1.1396, base-cost net Sharpe 0.0082, and conservative net Sharpe -1.6210. The 21-session base-cost result was negative. It was not promoted.

The frozen event-surprise retrospective evaluated 517 holdout events and accepted 46 trades. Five-session event IC was +0.0349, gross Sharpe -0.2776, base-cost net Sharpe -0.7014, conservative net Sharpe -1.1471, base net return -0.2532%, and the block-bootstrap Sharpe interval was [-2.9615, 3.1299]. Three of six promotion gates failed. The strategy was not promoted.

## V2 study mode

The existing 2022–2026 outcomes were already accessed during the v1 retrospective. They are historical baseline evidence and cannot become a pristine confirmatory test merely by renaming a split.

V2 therefore has two distinct lanes:

1. Confirmatory extraction validation on an outcome-blinded human benchmark sampled from the frozen corpus.
2. A new predictive lock using a later, not-yet-ingested chronological period only if source rights, timestamps, identifiers, and outcomes can be acquired without an unauthorized paid call.

If the new outcome panel cannot be acquired lawfully and point-in-time, the correct final classification is `EXTRACTION_BENCHMARK_COMPLETE_OUTCOME_BLOCKED`. Existing negative results remain visible and are never discarded.

## Cycle decision

Recovery integrity: `COMPLETE`.

Rights for private research: `PARTIAL` pending source-by-source contract confirmation. Public redistribution of article bodies is prohibited.

Human gold: `PENDING_HUMAN_REVIEW`.

Predictive test unlock: `PARTIAL`; it requires a genuinely new chronological panel and a signed Lock B before outcome access.

No inference, provider call, paid API call, deployment, public-mirror mutation, or live-demo mutation occurred in Cycle 1.
