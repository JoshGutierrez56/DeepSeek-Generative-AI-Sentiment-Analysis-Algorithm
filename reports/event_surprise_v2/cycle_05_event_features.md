# Cycle 5 — Outcome-Blind Event Features

Classification: `CYCLE_5_EVENT_FEATURE_PANEL_READY`

## Method

The panel uses the previously computed `story_cluster_id`, which was created from article text and timing without market outcomes. Each cluster retains its earliest article as the primary observation. Later or duplicate members may affect only source count, source disagreement, update count, and evidence completeness.

The production builder rejects forward-return, exit-date, adjusted-open, abnormal-return, abnormal-volume, benchmark-return, and realized-volatility columns. No market outcome is read by the Cycle 5 tool.

Features include signed and absolute surprise, materiality, certainty, ambiguity, novelty, FinBERT sentiment, event family, reference availability, source count, source disagreement, update count, evidence completeness, article latency, and point-in-time residual textual novelty. Residual novelty subtracts only the issuer's prior mean; it does not use future articles.

## Current corpus result

The recovered 5,000-article corpus contains 5,000 unique precomputed story clusters, so this historical sample has no multi-article clusters to aggregate. That is a property of the upstream frozen sample, which retained one primary article per cluster. Synthetic integration tests verify multi-source/update aggregation without changing the historical corpus.

The private panel is excluded from Git. The public manifest contains only aggregate counts and hashes.

## Limitations

- The current panel remains schema version 1 extraction data; V2 evidence offsets require a future frozen inference corpus.
- Source disagreement and update-count features are structurally zero in this one-primary-per-cluster sample.
- Human gold remains `PENDING_HUMAN_REVIEW`.
- No predictive or economic claim is made in this cycle.
