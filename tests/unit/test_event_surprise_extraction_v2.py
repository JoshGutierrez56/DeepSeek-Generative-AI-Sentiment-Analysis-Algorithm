from __future__ import annotations

import pytest

from sentiment_lab.event_surprise.extraction_v2 import (
    Direction,
    EventFamily,
    EventPacket,
    Interpretation,
    ReferenceType,
    Surprise,
    extract_explicit_comparison,
    validate_offsets,
)


def packet(text: str, *, unsupported: tuple[str, ...] = ()) -> EventPacket:
    extracted = extract_explicit_comparison(text)
    assert extracted is not None
    fact, evidence = extracted
    return EventPacket(
        event_id="event-1",
        article_id="article-1",
        source="fixture",
        source_timestamp="2026-01-01T12:00:00Z",
        ingestion_timestamp="2026-01-01T12:00:01Z",
        availability_timestamp="2026-01-01T12:00:01Z",
        article_version="v1",
        duplicate_cluster_id="cluster-1",
        event_family=EventFamily.earnings,
        fact=fact,
        reference_type=ReferenceType.analyst_consensus,
        surprise=Surprise(
            available=True,
            direction=Direction.positive,
            magnitude=0.2,
            materiality=0.8,
            novelty=0.6,
            confidence=0.9,
        ),
        evidence=evidence,
        field_evidence={"fact.actual_value": (0,), "fact.comparison_value": (0,)},
        unsupported_fields=unsupported,
        interpretation=Interpretation(),
        abstain=bool(unsupported),
        abstain_reason="unsupported field" if unsupported else None,
    )


def test_rule_model_extracts_exact_comparison_and_offsets() -> None:
    text = "Revenue was 120 million versus 100 million expected."
    result = packet(text)
    assert result.fact.actual_value == 120
    assert result.fact.comparison_value == 100
    assert validate_offsets(text, result)
    assert not validate_offsets(text.replace("120", "121"), result)


def test_rule_model_abstains_when_no_explicit_comparison() -> None:
    assert extract_explicit_comparison("Revenue improved materially.") is None


def test_packet_requires_abstention_for_unsupported_fields() -> None:
    text = "Revenue was 120 million versus 100 million expected."
    valid = packet(text, unsupported=("fact.period",))
    assert valid.abstain
    with pytest.raises(ValueError, match="unsupported"):
        EventPacket(**{**valid.model_dump(), "abstain": False, "abstain_reason": None})


def test_unavailable_surprise_rejects_signed_direction() -> None:
    with pytest.raises(ValueError, match="unavailable"):
        Surprise(
            available=False,
            direction=Direction.positive,
            materiality=0.5,
            novelty=0.5,
            confidence=0.5,
        )
