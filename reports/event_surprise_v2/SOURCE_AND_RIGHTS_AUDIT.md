# Source and Rights Audit

## Current classifications

- Provider article bodies: `LICENSED_PRIVATE_RESEARCH`; redistribution is not established and is therefore prohibited.
- Provider article metadata: `PUBLIC_METADATA_ONLY` unless a provider contract permits more.
- Frozen price panel: `LICENSED_PRIVATE_RESEARCH`; aggregate statistics may be public, raw rows may not.
- I/B/E/S and CRSP pilot data in separate worktrees: `LICENSED_PRIVATE_RESEARCH`; excluded from this branch and from public artifacts.
- Model outputs derived from private text: `SYNTHETIC_DERIVED`; only aggregate metrics, nonreconstructive examples, hashes, and bounded evidence references may be public.
- Hand-authored synthetic fixtures: `PUBLIC_REDISTRIBUTABLE`.
- Open-source code, schemas, model cards, and methodology: `PUBLIC_REDISTRIBUTABLE` subject to their licenses.

## Timing semantics

The frozen corpus preserves provider timestamp, retrieval timestamp, entry timestamp, correction-independent content hashes, and future-return exit dates. It is sufficient for historical lineage checks.

A new predictive panel must separately prove publication availability, after-close/weekend/holiday handling, corrections, and identifier validity. Raw I/B/E/S time fields may not be labeled UTC without authoritative vendor documentation.

## Public boundary

Public artifacts must not contain article bodies, provider payloads, private paths, credentials, paid rows, reviewer identities, reconstructive excerpts, or raw caches. Human-review packets remain private unless every excerpt is independently redistributable.

## Open item

Provider contract terms for a new post-2026-03-31 article panel and market outcomes have not been re-authorized for this loop. Any paid or licensed acquisition is blocked pending explicit approval.
