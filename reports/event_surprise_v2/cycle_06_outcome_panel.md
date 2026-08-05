# Cycle 6 — Outcome Panel Gate

Classification: `HOLD_TEST_UNLOCK`

Secondary blocker: `HOLD_OUTCOME_DATA`

## Decision

Lock B is not signed. The ten-cycle loop stops here under the stated hard-stop rule: test outcomes were inspected before a V2 predictive lock, and no genuinely later point-in-time corpus is currently available under authorized rights.

The 5,000-article historical corpus spans 2022-01-03 11:21:51 UTC through 2026-03-31 23:43:00 UTC. Its entry dates extend through 2026-04-01 and its 21-session exits through 2026-04-30. These outcomes were used in the earlier V1 retrospective and are historical evidence, not a new confirmatory test.

The earlier retrospective explicitly disclosed that holdout event-level IC had been viewed before its portfolio specification was frozen. It evaluated 517 holdout events, accepted 46 trades, produced five-session event IC +0.0349, gross Sharpe -0.2776, base-cost net Sharpe -0.7014, conservative net Sharpe -1.1471, and failed three of six promotion gates. Those negative results remain preserved.

## What was verified

- Historical article panel: 5,000 rows; 125 issuers.
- Historical price panel: 142,875 rows.
- Provider timestamps, entry dates, and exit dates exist for retrospective lineage.
- The V2 feature panel contains no outcome columns.
- The V2 preregistration requires a genuinely later period, provisionally beginning after 2026-03-31, frozen before outcome access.
- Current rights authorize neither a new paid provider pull nor redistribution of licensed rows.

## Why the old panel cannot be relocked

Renaming, repartitioning, or withholding a subset of already inspected outcomes would not restore confirmatory status. It would violate the two-lock protocol and the explicit hard-stop condition against test access before Lock B.

## Required unblock

Before Cycle 6 can be resumed:

1. Authorize a specific lawful post-2026-03-31 news and market-data source, including cost limits if paid.
2. Verify timestamp semantics, correction/update handling, historical identifiers, redistribution limits, and permitted derived outputs.
3. Acquire and hash the new article/metadata panel without reading its outcomes.
4. Freeze the exact chronological splits, features, preprocessing, missingness rules, tests, and economic rules.
5. Sign Lock B.
6. Only then load the locked test outcomes.

No provider call, paid API call, outcome unlock, inference run, deployment, or public-data exposure occurred.
