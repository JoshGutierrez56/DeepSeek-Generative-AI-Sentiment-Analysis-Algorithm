"""Outcome-blind event clustering and feature construction for event-surprise v2."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from statistics import fmean, pstdev
from typing import Any

import polars as pl

FORBIDDEN_OUTCOME_PREFIXES = ("future_return_", "exit_date_", "benchmark_return_")
FORBIDDEN_OUTCOME_COLUMNS = {
    "entry_adjusted_open",
    "realized_volatility",
    "abnormal_return",
    "abnormal_volume",
}


def _reject_outcomes(frame: pl.DataFrame) -> None:
    forbidden = {
        column
        for column in frame.columns
        if column in FORBIDDEN_OUTCOME_COLUMNS
        or any(column.startswith(prefix) for prefix in FORBIDDEN_OUTCOME_PREFIXES)
    }
    if forbidden:
        raise ValueError(f"outcome-aware columns are prohibited: {sorted(forbidden)}")


def _present(value: object) -> bool:
    return value is not None and bool(str(value).strip())


def build_event_feature_panel(
    articles: pl.DataFrame,
    extractions: pl.DataFrame,
    classifiers: pl.DataFrame,
) -> pl.DataFrame:
    """Create one deterministic row per precomputed, outcome-blind story cluster.

    The earliest article is the primary observation. Duplicate/update articles contribute
    source-count, disagreement, update-count, and evidence-completeness features only.
    """

    for frame in (articles, extractions, classifiers):
        _reject_outcomes(frame)
    article_fields = {
        "article_id",
        "provider",
        "provider_timestamp",
        "retrieved_at",
        "ticker",
        "story_cluster_id",
    }
    extraction_fields = {
        "article_id",
        "event_type",
        "expected_or_prior_information",
        "surprise_direction",
        "surprise_magnitude",
        "confidence",
        "materiality",
        "novelty",
        "abstain",
        "abstain_reason",
        "concise_evidence",
    }
    classifier_fields = {"article_id", "model", "finbert_score"}
    for name, required, frame in (
        ("articles", article_fields, articles),
        ("extractions", extraction_fields, extractions),
        ("classifiers", classifier_fields, classifiers),
    ):
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"missing {name} columns: {sorted(missing)}")

    finbert = classifiers.filter(pl.col("model") == "finbert").select("article_id", "finbert_score")
    joined = articles.join(extractions, on="article_id", how="inner", validate="1:1").join(
        finbert, on="article_id", how="inner", validate="1:1"
    )
    if joined.height != articles.height:
        raise ValueError("outcome-blind joins must retain every article")

    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in joined.to_dicts():
        grouped[str(row["story_cluster_id"])].append(row)

    output: list[dict[str, Any]] = []
    for cluster_id, members in grouped.items():
        members.sort(key=lambda row: (row["provider_timestamp"], str(row["article_id"])))
        primary = members[0]
        sentiment_values = [float(row["finbert_score"]) for row in members]
        evidence_values = [_present(row["concise_evidence"]) for row in members]
        provider_time = primary["provider_timestamp"]
        retrieved_at = primary["retrieved_at"]
        if not isinstance(provider_time, datetime) or not isinstance(retrieved_at, datetime):
            raise ValueError("timestamps must be datetimes")
        abstain = bool(primary["abstain"])
        direction = float(primary["surprise_direction"])
        magnitude = float(primary["surprise_magnitude"])
        output.append(
            {
                "event_cluster_id": cluster_id,
                "primary_article_id": str(primary["article_id"]),
                "issuer_id": str(primary["ticker"]),
                "availability_timestamp": provider_time,
                "event_family": str(primary["event_type"]),
                "signed_surprise": None if abstain else direction * magnitude,
                "absolute_surprise": None if abstain else magnitude,
                "surprise_available": not abstain,
                "materiality": float(primary["materiality"]),
                "certainty": float(primary["confidence"]),
                "ambiguity": abstain or _present(primary["abstain_reason"]),
                "novelty": float(primary["novelty"]),
                "sentiment": float(primary["finbert_score"]),
                "reference_available": _present(primary["expected_or_prior_information"]),
                "source_count": len({str(row["provider"]) for row in members}),
                "source_disagreement": pstdev(sentiment_values)
                if len(sentiment_values) > 1
                else 0.0,
                "update_count": len(members) - 1,
                "evidence_completeness": fmean(float(value) for value in evidence_values),
                "article_latency_seconds": max(0.0, (retrieved_at - provider_time).total_seconds()),
                "residual_textual_novelty": None,
            }
        )

    output.sort(key=lambda row: (row["availability_timestamp"], row["primary_article_id"]))
    issuer_history: defaultdict[str, list[float]] = defaultdict(list)
    for row in output:
        history = issuer_history[str(row["issuer_id"])]
        novelty = float(row["novelty"])
        row["residual_textual_novelty"] = None if not history else novelty - fmean(history)
        history.append(novelty)
    return pl.DataFrame(output)


def feature_panel_summary(panel: pl.DataFrame) -> dict[str, object]:
    required = {
        "event_cluster_id",
        "issuer_id",
        "event_family",
        "surprise_available",
        "evidence_completeness",
        "source_count",
        "update_count",
    }
    missing = required - set(panel.columns)
    if missing:
        raise ValueError(f"missing feature-panel columns: {sorted(missing)}")
    return {
        "rows": panel.height,
        "unique_event_clusters": panel["event_cluster_id"].n_unique(),
        "unique_issuers": panel["issuer_id"].n_unique(),
        "event_families": panel["event_family"].n_unique(),
        "surprise_available": panel.filter(pl.col("surprise_available")).height,
        "multi_article_clusters": panel.filter(pl.col("update_count") > 0).height,
        "multi_source_clusters": panel.filter(pl.col("source_count") > 1).height,
        "mean_evidence_completeness": panel["evidence_completeness"].mean(),
        "outcome_columns": [],
    }
