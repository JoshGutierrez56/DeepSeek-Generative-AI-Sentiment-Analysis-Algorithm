from __future__ import annotations

from sentiment_lab.event_surprise.gold import (
    benchmark_id,
    bucket_length,
    bucket_sentiment,
    bucket_unit,
    difficulty_bucket,
    public_manifest,
    select_stratified,
)


def candidate(index: int, family: str) -> dict[str, object]:
    return {
        "benchmark_id": benchmark_id(f"hash-{index}"),
        "event_family": family,
        "year": 2025 + (index % 2),
        "source": "fixture",
        "length_bucket": "SHORT" if index % 2 else "LONG",
        "sentiment_bucket": "POSITIVE" if index % 3 else "NEGATIVE",
        "confidence_bucket": "HIGH" if index % 2 else "LOW",
        "surprise_available": "YES" if index % 2 else "NO",
        "materiality_bucket": "HIGH" if index % 3 else "MEDIUM",
        "difficulty_bucket": "EASY" if index % 2 else "HARD",
        "private": {"article_id": f"private-{index}"},
    }


def test_buckets_and_review_identifier_are_stable() -> None:
    assert benchmark_id("abc") == benchmark_id("abc")
    assert benchmark_id("abc").startswith("ES2-")
    assert bucket_length(1499) == "SHORT"
    assert bucket_length(1500) == "MEDIUM"
    assert bucket_length(5000) == "LONG"
    assert bucket_unit(0.33) == "LOW"
    assert bucket_unit(0.5) == "MEDIUM"
    assert bucket_unit(0.9) == "HIGH"
    assert bucket_sentiment(-0.3) == "NEGATIVE"
    assert bucket_sentiment(0.0) == "NEUTRAL"
    assert bucket_sentiment(0.3) == "POSITIVE"
    assert difficulty_bucket(confidence=0.9, ambiguity=False, has_reference=True) == "EASY"
    assert difficulty_bucket(confidence=0.3, ambiguity=False, has_reference=True) == "HARD"


def test_stratified_sample_is_deterministic_and_public_safe() -> None:
    candidates = [candidate(index, "earnings" if index < 8 else "guidance") for index in range(12)]
    first = select_stratified(candidates, target=8, seed=7)
    second = select_stratified(candidates, target=8, seed=7)
    assert first == second
    assert {row["event_family"] for row in first} == {"earnings", "guidance"}
    manifest = public_manifest(first)
    assert manifest["sample_size"] == 8
    assert len(manifest["sample_digest"]) == 64
    assert all("private" not in row for row in manifest["records"])
