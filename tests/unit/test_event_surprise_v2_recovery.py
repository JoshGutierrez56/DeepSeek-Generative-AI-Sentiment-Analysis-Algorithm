from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts" / "event_surprise_v2"
EXPECTED_ARTICLES = "8ada422fcdefa894c55ae51400e073f97fa6d8e26272cde98d8926ce27b68385"
EXPECTED_QWEN = "f696fd2795993ff6c2a64baee7dc314e8287e85d0b0dd79ee45e41bd98121391"


def load(name: str) -> dict[str, object]:
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def test_recovery_receipt_preserves_frozen_lineage() -> None:
    receipt = load("recovery_receipt.json")
    source_hashes = receipt["source_hashes"]
    corpus = receipt["corpus"]
    assert isinstance(source_hashes, dict)
    assert isinstance(corpus, dict)
    assert source_hashes["articles"] == EXPECTED_ARTICLES
    assert source_hashes["qwen_final"] == EXPECTED_QWEN
    assert corpus["articles"] == 5000
    assert corpus["qwen_valid_rows"] == 5000
    assert corpus["qwen_invalid_rows"] == 0
    assert receipt["inference_restart_required"] is False


def test_cycle_one_artifacts_are_public_safe_and_lineaged() -> None:
    forbidden = ("C:\\Users\\", "provider_payload", 'article_content"')
    for path in ARTIFACTS.rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        document = json.loads(text)
        assert "schema_version" in document
        assert not any(token in text for token in forbidden)


def test_cycle_one_receipt_is_immutable_as_checkpoint_advances() -> None:
    receipt = load("cycle_01_validation_receipt.json")
    checkpoint = load("checkpoint.json")
    assert receipt["cycle"] == 1
    assert receipt["classification"] == "CYCLE_1_EVENT_SURPRISE_BASELINE_READY"
    assert checkpoint["cycle"] >= 1
    assert checkpoint["critical_hold"] is None
