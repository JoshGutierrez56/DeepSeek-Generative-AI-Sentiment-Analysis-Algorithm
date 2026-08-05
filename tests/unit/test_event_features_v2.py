from datetime import UTC, datetime, timedelta

import polars as pl
import pytest

from sentiment_lab.event_surprise.features_v2 import (
    build_event_feature_panel,
    feature_panel_summary,
)


def _frames() -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    timestamp = datetime(2026, 1, 1, 14, tzinfo=UTC)
    articles = pl.DataFrame(
        {
            "article_id": ["a", "b", "c"],
            "provider": ["one", "two", "one"],
            "provider_timestamp": [timestamp, timestamp + timedelta(minutes=1), timestamp],
            "retrieved_at": [
                timestamp + timedelta(seconds=5),
                timestamp + timedelta(minutes=1, seconds=8),
                timestamp + timedelta(seconds=10),
            ],
            "ticker": ["AAA", "AAA", "AAA"],
            "story_cluster_id": ["cluster-1", "cluster-1", "cluster-2"],
        }
    )
    extractions = pl.DataFrame(
        {
            "article_id": ["a", "b", "c"],
            "event_type": ["earnings", "earnings", "guidance"],
            "expected_or_prior_information": ["consensus 2", "consensus 2", ""],
            "surprise_direction": [1.0, 1.0, 0.0],
            "surprise_magnitude": [0.5, 0.5, 0.0],
            "confidence": [0.9, 0.8, 0.2],
            "materiality": [0.8, 0.7, 0.1],
            "novelty": [0.7, 0.6, 0.5],
            "abstain": [False, False, True],
            "abstain_reason": [None, None, "no expectation"],
            "concise_evidence": ["actual 3", "actual 3", ""],
        }
    )
    classifiers = pl.DataFrame(
        {
            "article_id": ["a", "b", "c"],
            "model": ["finbert", "finbert", "finbert"],
            "finbert_score": [0.4, 0.2, -0.1],
        }
    )
    return articles, extractions, classifiers


def test_cluster_features_are_outcome_blind_and_point_in_time() -> None:
    panel = build_event_feature_panel(*_frames())
    assert panel.height == 2
    first = panel.row(0, named=True)
    second = panel.row(1, named=True)
    assert first["source_count"] == 2
    assert first["update_count"] == 1
    assert first["signed_surprise"] == 0.5
    assert first["residual_textual_novelty"] is None
    assert second["signed_surprise"] is None
    assert second["residual_textual_novelty"] == pytest.approx(-0.2)
    assert feature_panel_summary(panel)["outcome_columns"] == []


def test_outcome_columns_are_rejected() -> None:
    articles, extractions, classifiers = _frames()
    articles = articles.with_columns(pl.lit(0.1).alias("future_return_5d"))
    with pytest.raises(ValueError, match="outcome-aware"):
        build_event_feature_panel(articles, extractions, classifiers)
