"""Validate the completed v1 corpus without model or network access."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from sentiment_lab.event_surprise.corpus_v2 import audit_frozen_corpus


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict[str, object]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()
    corpus = pl.read_parquet(args.corpus)
    summary = audit_frozen_corpus(corpus)
    value = {
        "schema_version": "event_surprise_v2.frozen_corpus_manifest.v1",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "code_commit": args.code_commit,
        "config_sha256": args.config_sha256,
        "source_sha256": sha256(args.articles),
        "corpus_sha256": sha256(args.corpus),
        "corpus_schema": "event_surprise.v1",
        "v2_evidence_offset_status": "NOT_AVAILABLE",
        "human_gold_status": "PENDING_HUMAN_REVIEW",
        "inference_restarted": False,
        "network_model_calls": 0,
        **summary,
    }
    atomic_json(args.output, value)


if __name__ == "__main__":
    main()
