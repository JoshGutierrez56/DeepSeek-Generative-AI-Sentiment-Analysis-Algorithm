# Predictive Analysis Plan — Draft Blocked Before Lock B

Status: `BLOCKED_NOT_FROZEN`

## Confirmatory sample

A future point-in-time event corpus beginning after the historical provider cutoff of 2026-03-31. Exact end date and sample size must be recorded before outcome access. The historical 2022–2026 panel is contextual baseline evidence only.

## Timing

- Use provider availability timestamp plus verified correction/update history.
- Map same-session, after-close, weekend, and holiday releases to the first defensibly tradable session.
- Use historically valid security identifiers.
- Never use an article update arriving after the decision timestamp.

## Targets

- Primary: five-session signed abnormal return.
- Secondary: one- and 21-session abnormal return, five-session absolute abnormal return, realized volatility, and abnormal volume.
- Missing outcomes remain missing; missing surprise is never zero.

## Feature ladder

1. Metadata and lagged price/volume controls.
2. FinBERT sentiment.
3. Event-family taxonomy.
4. Point-in-time residual textual novelty.
5. Structured event surprise.
6. Surprise plus novelty.

## Model and inference plan

- Chronological training, validation, and locked test only.
- Preprocessing fitted on training data only.
- Primary models: transparent regularized linear/logistic baselines appropriate to each target; no opaque outcome-scoring model.
- Report Pearson IC, Spearman IC, rank IC by date where defined, coefficients, confidence intervals, calibration, coverage, and decay.
- Use issuer-clustered inference, calendar-time aggregation, and block bootstrap for dependence and overlapping horizons.

## Negative controls

Shuffled dates, shuffled issuers, future-incompatible placebo, article length, random direction, non-material events, and source-only features.

## Multiplicity

The H2 five-session coefficient and rank IC are co-primary and must agree in sign. Benjamini-Hochberg false-discovery control at 10% applies to secondary tests. All preregistered horizons and families are reported, not only favorable ones.

## Economic gate

No directional portfolio is allowed unless H2 survives the locked test with stable coverage and no leakage finding. No test-period tuning of threshold, feature, family, horizon, cost, or model is permitted.

## Lock status

This plan is not Lock B. Dates, source rights, sample size, identifiers, and outcome availability remain unresolved. The predictive receipt records a refused lock rather than a fabricated signature.
