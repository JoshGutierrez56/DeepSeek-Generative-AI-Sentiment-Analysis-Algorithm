# Decision Log

## D-001 — Base branch

Branch from validated release `main` at `0d6be1666811b853d954cf004b760f9595381f67`, which contains the event-surprise negative-result lineage and public evidence page. Do not branch from the unrelated expectation-adjusted pilots.

## D-002 — No Qwen restart

The final 5,000-row Qwen artifact is complete and hash-valid. Re-running it would waste compute and violate cache-first controls.

## D-003 — Existing outcomes are historical

The frozen 2022–2026 outcomes were already inspected. V2 may use them for reproducibility and exploratory comparison but not as a pristine confirmatory test.

## D-004 — Rights-first public boundary

The GitHub repository is already public. Every pushed artifact must therefore be public-safe by construction; no raw licensed text or private path may be committed.

## D-005 — Negative results remain canonical

Generic sentiment and v1 event surprise were not promoted. Those results stay visible regardless of V2 outcomes.
