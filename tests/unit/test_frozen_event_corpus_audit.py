from __future__ import annotations

import polars as pl
import pytest

from sentiment_lab.event_surprise.corpus_v2 import audit_frozen_corpus


def fixture(rows: int = 5000) -> pl.DataFrame:
    return pl.DataFrame(
        {
            "article_id": [f"a-{index}" for index in range(rows)],
            "article_hash": [f"h-{index}" for index in range(rows)],
            "event_type": ["earnings"] * rows,
            "surprise_direction": [1.0] * rows,
            "confidence": [0.8] * rows,
            "materiality": [0.7] * rows,
            "abstain": [False] * (rows - 1) + [True],
            "abstain_reason": [None] * (rows - 1) + ["no reference"],
            "concise_evidence": ["supported"] * rows,
            "valid_json": [True] * rows,
        }
    )


def test_corpus_audit_reconciles_contract() -> None:
    result = audit_frozen_corpus(fixture())
    assert result["rows"] == 5000
    assert result["parse_failures"] == 0
    assert result["abstentions"] == 1
    assert result["surprise_available_rows"] == 4999
    assert result["concise_evidence_rows"] == 5000


def test_corpus_audit_rejects_incomplete_sample() -> None:
    with pytest.raises(ValueError, match="5,000"):
        audit_frozen_corpus(fixture(10))
