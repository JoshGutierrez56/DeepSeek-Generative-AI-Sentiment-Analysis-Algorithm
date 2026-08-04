# Event Surprise V2 Pre-registration

Status: `FROZEN_FOR_CYCLE_1`; extraction lock is planned for Cycle 3 and predictive lock for Cycle 6.

## Research questions

1. Can an evidence-grounded local model produce structured event packets that agree with blinded human labels?
2. Does structured signed surprise add chronological out-of-sample information for five-session abnormal return beyond sentiment, metadata, event family, recent market controls, issuer history, and residual novelty?
3. Does absolute surprise add information for absolute abnormal return or realized volatility?
4. Does surprise plus residual novelty outperform either representation alone?
5. Does any surviving signal retain value after conservative timing, turnover, slippage, and transaction costs?

Extraction quality, prediction, economic value, and reviewer usefulness are separate claims.

## Confirmatory hypotheses

- H1: structured extraction reaches the field-specific thresholds below on blinded human gold.
- H2: valid signed surprise has a positive association with five-session abnormal return in the locked future test period.
- H3: absolute surprise has a positive association with five-session absolute abnormal return and/or realized volatility.
- H4: surprise adds information beyond sentiment, metadata, controls, and residual novelty.
- H5: economic evaluation is permitted only if H2 survives the locked test and stability gates.

Failure of H2 does not invalidate H1, H3, H4, or the evidence-review product.

## H1 thresholds frozen before human labeling

- Issuer identity exact agreement: at least 0.98.
- Event-family macro F1: at least 0.80.
- Direction accuracy on adjudicated directional events: at least 0.80.
- Reference-type macro F1: at least 0.75.
- Surprise-availability F1: at least 0.85.
- Materiality weighted kappa: at least 0.60.
- Certainty weighted kappa: at least 0.60.
- Evidence-offset validity: at least 0.95.
- Field-to-evidence support precision: at least 0.95.
- Normalized numeric actual/reference exact agreement where both are present: at least 0.95.

Metrics will include confidence intervals and coverage. Abstentions are scored, not silently removed.

## Extraction benchmark

- Target sample: 400 unique event clusters.
- Sampling dimensions: event family, year, source, length, sentiment, confidence, surprise availability, expected materiality, and easy/hard strata.
- At least 20% double-reviewed by humans when reviewers are available.
- AI review may prioritize cases but is labeled `AI REVIEW — NOT HUMAN GOLD`.
- Market-outcome columns are excluded from annotation packets and model inputs.

## Predictive design

The 2022-01-03 through 2026-03-31 frozen corpus is historical baseline evidence because its outcomes were previously accessed. A confirmatory Lock B requires a later point-in-time corpus, provisionally beginning 2026-04-01, acquired and frozen before outcomes are loaded.

Primary horizon: five sessions. Secondary horizons: one and 21 sessions.

Primary targets: signed abnormal return, absolute abnormal return, realized volatility, and abnormal volume.

Primary comparison ladder:

1. metadata and market controls;
2. sentiment;
3. event family;
4. residual textual novelty;
5. event surprise;
6. surprise plus novelty.

Primary validation is chronological. Random cross-validation is prohibited. Issuer dependence, date dependence, duplicate clusters, overlapping horizons, and market-wide shocks must be handled explicitly.

## Multiple testing and negative controls

The primary H2 coefficient and five-session rank IC are co-primary and must agree in sign. Family/year/horizon breakdowns are secondary. Benjamini-Hochberg false-discovery control at 10% applies across secondary predictive tests.

Negative controls: shuffled event dates, shuffled issuers, future-incompatible placebo, article length, random direction, non-material events, and source-only features.

## Economic gate

No directional portfolio is permitted unless H2 survives the locked test with stable coverage and no leakage finding. No test-set threshold, family, horizon, feature, or cost assumption may be optimized.

## Null handling

Null, mixed, rejected, and blocked conclusions are valid outcomes. No adverse result may be excluded to create a positive claim.
