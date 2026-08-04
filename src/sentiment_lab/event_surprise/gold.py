"""Outcome-blind stratified sampling for human event-surprise review."""

from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

PUBLIC_SAMPLE_FIELDS = (
    "benchmark_id",
    "event_family",
    "year",
    "source",
    "length_bucket",
    "sentiment_bucket",
    "confidence_bucket",
    "surprise_available",
    "materiality_bucket",
    "difficulty_bucket",
)


def benchmark_id(article_hash: str) -> str:
    """Create a stable nonreconstructive review identifier."""
    return "ES2-" + hashlib.sha256(f"event-surprise-v2\n{article_hash}".encode()).hexdigest()[:16]


def bucket_length(characters: int) -> str:
    if characters < 1_500:
        return "SHORT"
    if characters < 5_000:
        return "MEDIUM"
    return "LONG"


def bucket_unit(value: float) -> str:
    if value < 0.34:
        return "LOW"
    if value < 0.67:
        return "MEDIUM"
    return "HIGH"


def bucket_sentiment(score: float) -> str:
    if score < -0.2:
        return "NEGATIVE"
    if score > 0.2:
        return "POSITIVE"
    return "NEUTRAL"


def difficulty_bucket(*, confidence: float, ambiguity: bool, has_reference: bool) -> str:
    if ambiguity or confidence < 0.45:
        return "HARD"
    if confidence < 0.75 or not has_reference:
        return "MEDIUM"
    return "EASY"


def stratum(candidate: Mapping[str, Any]) -> tuple[object, ...]:
    return tuple(candidate[field] for field in PUBLIC_SAMPLE_FIELDS[1:])


def select_stratified(
    candidates: Sequence[Mapping[str, Any]], *, target: int, seed: int
) -> list[dict[str, Any]]:
    """Round-robin across outcome-blind strata with stable within-stratum ranking."""
    if target <= 0:
        raise ValueError("target must be positive")
    if len(candidates) < target:
        raise ValueError(f"target {target} exceeds candidate count {len(candidates)}")
    groups: dict[tuple[object, ...], list[dict[str, Any]]] = {}
    seen: set[str] = set()
    for raw in candidates:
        candidate = dict(raw)
        identifier = str(candidate["benchmark_id"])
        if identifier in seen:
            raise ValueError(f"duplicate benchmark_id: {identifier}")
        seen.add(identifier)
        groups.setdefault(stratum(candidate), []).append(candidate)
    for rows in groups.values():
        rows.sort(
            key=lambda row: hashlib.sha256(f"{seed}\n{row['benchmark_id']}".encode()).hexdigest()
        )
    family_queues: dict[str, list[dict[str, Any]]] = {}
    for family in sorted({str(key[0]) for key in groups}):
        family_groups = [key for key in sorted(groups, key=repr) if str(key[0]) == family]
        queue: list[dict[str, Any]] = []
        while any(groups[key] for key in family_groups):
            for key in family_groups:
                if groups[key]:
                    queue.append(groups[key].pop(0))
        family_queues[family] = queue
    selected: list[dict[str, Any]] = []
    ordered_families = sorted(family_queues)
    while len(selected) < target:
        progressed = False
        for family in ordered_families:
            if family_queues[family]:
                selected.append(family_queues[family].pop(0))
                progressed = True
                if len(selected) == target:
                    break
        if not progressed:
            raise RuntimeError("stratified selection exhausted unexpectedly")
    return selected


def counts(rows: Iterable[Mapping[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[field]) for row in rows).items()))


def public_manifest(rows: Sequence[Mapping[str, Any]]) -> dict[str, object]:
    public_rows = [{field: row[field] for field in PUBLIC_SAMPLE_FIELDS} for row in rows]
    digest = hashlib.sha256(
        "\n".join(sorted(str(row["benchmark_id"]) for row in public_rows)).encode()
    ).hexdigest()
    return {
        "sample_size": len(rows),
        "sample_digest": digest,
        "event_family_counts": counts(rows, "event_family"),
        "year_counts": counts(rows, "year"),
        "source_counts": counts(rows, "source"),
        "length_counts": counts(rows, "length_bucket"),
        "sentiment_counts": counts(rows, "sentiment_bucket"),
        "confidence_counts": counts(rows, "confidence_bucket"),
        "surprise_available_counts": counts(rows, "surprise_available"),
        "materiality_counts": counts(rows, "materiality_bucket"),
        "difficulty_counts": counts(rows, "difficulty_bucket"),
        "records": public_rows,
    }
