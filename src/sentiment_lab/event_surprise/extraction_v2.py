"""Frozen evidence-grounded event-surprise v2 extraction contract."""

from __future__ import annotations

import hashlib
import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventFamily(StrEnum):
    earnings = "earnings"
    guidance = "guidance"
    capital_allocation = "capital_allocation"
    financing_liquidity = "financing_liquidity"
    debt_refinancing = "debt_refinancing"
    merger_acquisition = "merger_acquisition"
    asset_sale = "asset_sale"
    legal_regulatory = "legal_regulatory"
    operations = "operations"
    product_commercial = "product_commercial"
    management_governance = "management_governance"
    restructuring = "restructuring"
    impairment = "impairment"
    cyber_technology = "cyber_technology"
    supply_chain = "supply_chain"
    macro_sector = "macro_sector"
    other = "other"
    no_material_event = "no_material_event"


class ReferenceType(StrEnum):
    analyst_consensus = "analyst_consensus"
    company_guidance = "company_guidance"
    prior_period = "prior_period"
    prior_disclosure = "prior_disclosure"
    market_implied = "market_implied"
    contractual_threshold = "contractual_threshold"
    management_target = "management_target"
    article_stated = "article_stated"
    none = "none"
    unclear = "unclear"


class Direction(StrEnum):
    positive = "positive"
    negative = "negative"
    none = "none"
    unclear = "unclear"


class EvidenceRole(StrEnum):
    fact = "fact"
    reference = "reference"
    timing = "timing"
    uncertainty = "uncertainty"


class EvidenceSpan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    start: int = Field(ge=0)
    end: int = Field(gt=0)
    role: EvidenceRole
    text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def end_follows_start(self) -> EvidenceSpan:
        if self.end <= self.start:
            raise ValueError("evidence end must follow start")
        return self


class EventFact(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    subject: str | None = None
    action: str | None = None
    object: str | None = None
    actual_value: float | None = None
    unit: str | None = None
    comparison_value: float | None = None
    comparison_unit: str | None = None
    period: str | None = None
    geography: str | None = None
    counterparty: str | None = None
    status: str | None = None
    certainty: float = Field(ge=0, le=1)
    expected_timing: str | None = None


class Surprise(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    available: bool
    direction: Direction
    magnitude: float | None = Field(default=None, ge=0)
    standardized: float | None = None
    materiality: float = Field(ge=0, le=1)
    novelty: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    ambiguity: str | None = None
    missing_information: tuple[str, ...] = ()
    contradiction: bool = False

    @model_validator(mode="after")
    def unavailable_has_no_signed_claim(self) -> Surprise:
        if not self.available and self.direction not in {Direction.none, Direction.unclear}:
            raise ValueError("unavailable surprise cannot carry a signed direction")
        if self.available and self.direction in {Direction.none, Direction.unclear}:
            raise ValueError("available surprise requires a signed direction")
        return self


class Interpretation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    possible_mechanism: str | None = None
    expected_horizon: str | None = None
    alternative_explanation: str | None = None
    falsification_condition: str | None = None
    analyst_question: str | None = None
    no_trade_reason: str | None = None


class EventPacket(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str = "event_surprise.v2"
    event_id: str
    article_id: str
    issuer_id: str | None = None
    ticker: str | None = None
    source: str
    source_timestamp: str
    ingestion_timestamp: str
    availability_timestamp: str
    article_version: str
    duplicate_cluster_id: str
    correction_of: str | None = None
    event_family: EventFamily
    event_subtype: str | None = None
    fact: EventFact
    reference_type: ReferenceType
    surprise: Surprise
    evidence: tuple[EvidenceSpan, ...]
    field_evidence: dict[str, tuple[int, ...]]
    unsupported_fields: tuple[str, ...] = ()
    conflicting_evidence: tuple[str, ...] = ()
    interpretation: Interpretation
    abstain: bool
    abstain_reason: str | None = None

    @model_validator(mode="after")
    def validate_evidence_mapping_and_abstention(self) -> EventPacket:
        for field, indices in self.field_evidence.items():
            if not field or any(index < 0 or index >= len(self.evidence) for index in indices):
                raise ValueError("field evidence index is invalid")
        if self.abstain and not self.abstain_reason:
            raise ValueError("abstention requires a reason")
        if not self.abstain and self.abstain_reason:
            raise ValueError("non-abstention cannot carry an abstain reason")
        if self.unsupported_fields and not self.abstain:
            raise ValueError("unsupported factual fields require abstention")
        return self


def evidence_span(text: str, start: int, end: int, role: EvidenceRole) -> EvidenceSpan:
    return EvidenceSpan(
        start=start,
        end=end,
        role=role,
        text_sha256=hashlib.sha256(text[start:end].encode()).hexdigest(),
    )


def validate_offsets(text: str, packet: EventPacket) -> bool:
    return all(
        span.end <= len(text)
        and hashlib.sha256(text[span.start : span.end].encode()).hexdigest() == span.text_sha256
        for span in packet.evidence
    )


COMPARISON_PATTERN = re.compile(
    r"(?P<actual>-?\d+(?:\.\d+)?)\s*(?P<unit>%|million|billion|m|bn)?"
    r"\s+(?:versus|vs\.?|compared with|from)\s+"
    r"(?P<reference>-?\d+(?:\.\d+)?)\s*(?P<reference_unit>%|million|billion|m|bn)?",
    re.IGNORECASE,
)


def extract_explicit_comparison(text: str) -> tuple[EventFact, tuple[EvidenceSpan, ...]] | None:
    """Model 0: extract only explicit numeric comparisons and their exact evidence."""
    match = COMPARISON_PATTERN.search(text)
    if match is None:
        return None
    fact = EventFact(
        actual_value=float(match.group("actual")),
        unit=match.group("unit"),
        comparison_value=float(match.group("reference")),
        comparison_unit=match.group("reference_unit"),
        certainty=1.0,
    )
    return fact, (evidence_span(text, match.start(), match.end(), EvidenceRole.fact),)


FROZEN_MODEL_LADDER = {
    "model_0": "deterministic_explicit_comparison_rules.v1",
    "model_1": {
        "finbert": "ProsusAI/finbert@4556d13015211d73dccd3fdd39d39232506f3e43",
        "financial_roberta": (
            "soleimanian/financial-roberta-large-sentiment@f8804d31111d7c3569e88abaad6969918e858fbd"
        ),
    },
    "model_2": {
        "tag": "qwen3.6:35b-a3b",
        "blob_sha256": "f5ee307a2982106a6eb82b62b2c00b575c9072145a759ae4660378acda8dcf2d",
        "think": False,
        "temperature": 0,
        "seed": 20260719,
    },
    "model_3": (
        "accept_llm_only_when_schema_and_offsets_validate;"
        "otherwise_retain_supported_rule_fields_and_abstain"
    ),
}
