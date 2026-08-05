"""Contract validation for the frozen event-surprise corpus."""

from __future__ import annotations

from collections import Counter

import polars as pl


def audit_frozen_corpus(frame: pl.DataFrame) -> dict[str, object]:
    required = {
        "article_id",
        "article_hash",
        "event_type",
        "surprise_direction",
        "confidence",
        "materiality",
        "abstain",
        "abstain_reason",
        "concise_evidence",
        "valid_json",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"missing corpus columns: {sorted(missing)}")
    if frame.height != 5000 or frame["article_id"].n_unique() != 5000:
        raise ValueError("frozen corpus must contain 5,000 unique articles")
    invalid = frame.filter(~pl.col("valid_json")).height
    evidence_missing = frame.filter(
        pl.col("concise_evidence").is_null() | (pl.col("concise_evidence").str.len_chars() == 0)
    ).height
    event_counts = Counter(str(value) for value in frame["event_type"].to_list())
    abstentions = frame.filter(pl.col("abstain")).height
    return {
        "rows": frame.height,
        "unique_article_ids": frame["article_id"].n_unique(),
        "unique_article_hashes": frame["article_hash"].n_unique(),
        "valid_json_rows": frame.height - invalid,
        "parse_failures": invalid,
        "abstentions": abstentions,
        "surprise_available_rows": frame.height - abstentions,
        "concise_evidence_rows": frame.height - evidence_missing,
        "event_family_counts": dict(sorted(event_counts.items())),
        "confidence": {
            "minimum": frame["confidence"].min(),
            "median": frame["confidence"].median(),
            "maximum": frame["confidence"].max(),
        },
        "materiality": {
            "minimum": frame["materiality"].min(),
            "median": frame["materiality"].median(),
            "maximum": frame["materiality"].max(),
        },
    }
