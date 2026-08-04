"""Prepare private review packets and a public-safe stratification manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from sentiment_lab.event_surprise.gold import (
    benchmark_id,
    bucket_length,
    bucket_sentiment,
    bucket_unit,
    difficulty_bucket,
    public_manifest,
    select_stratified,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def candidates(
    articles_path: Path, qwen_path: Path, classifiers_path: Path
) -> list[dict[str, object]]:
    articles = pl.read_parquet(
        articles_path,
        columns=[
            "article_id",
            "article_content_hash",
            "provider",
            "provider_timestamp",
            "title",
            "content",
            "ticker",
            "story_cluster_id",
        ],
    )
    qwen = pl.read_parquet(
        qwen_path,
        columns=[
            "article_id",
            "article_hash",
            "event_type",
            "actual_information",
            "expected_or_prior_information",
            "surprise_direction",
            "confidence",
            "materiality",
            "abstain",
            "abstain_reason",
            "concise_evidence",
        ],
    )
    classifiers = (
        pl.read_parquet(classifiers_path)
        .filter(pl.col("model") == "finbert")
        .select("article_id", "finbert_score")
    )
    joined = articles.join(qwen, on="article_id", how="inner", validate="1:1").join(
        classifiers, on="article_id", how="inner", validate="1:1"
    )
    if joined.height != articles.height:
        raise ValueError("outcome-blind source joins must retain every article")
    output: list[dict[str, object]] = []
    for row in joined.to_dicts():
        content = str(row["content"])
        reference = row["expected_or_prior_information"]
        confidence = float(row["confidence"])
        abstain_reason = row["abstain_reason"]
        output.append(
            {
                "benchmark_id": benchmark_id(str(row["article_hash"])),
                "event_family": str(row["event_type"]),
                "year": row["provider_timestamp"].year,
                "source": str(row["provider"]),
                "length_bucket": bucket_length(len(content)),
                "sentiment_bucket": bucket_sentiment(float(row["finbert_score"])),
                "confidence_bucket": bucket_unit(confidence),
                "surprise_available": "NO" if bool(row["abstain"]) else "YES",
                "materiality_bucket": bucket_unit(float(row["materiality"])),
                "difficulty_bucket": difficulty_bucket(
                    confidence=confidence,
                    ambiguity=bool(abstain_reason),
                    has_reference=bool(reference),
                ),
                "private": {
                    "article_id": row["article_id"],
                    "article_hash": row["article_hash"],
                    "article_content_hash": row["article_content_hash"],
                    "story_cluster_id": row["story_cluster_id"],
                    "provider_timestamp": row["provider_timestamp"].isoformat(),
                    "ticker": row["ticker"],
                    "title": row["title"],
                    "content": content,
                    "model_packet": {
                        "event_family": row["event_type"],
                        "actual_information": row["actual_information"],
                        "expected_or_prior_information": reference,
                        "surprise_direction": row["surprise_direction"],
                        "confidence": confidence,
                        "materiality": row["materiality"],
                        "abstain": row["abstain"],
                        "abstain_reason": abstain_reason,
                        "concise_evidence": row["concise_evidence"],
                    },
                },
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--qwen", type=Path, required=True)
    parser.add_argument("--classifiers", type=Path, required=True)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--public-output", type=Path, required=True)
    parser.add_argument("--target", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20260804)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()

    source = candidates(args.articles, args.qwen, args.classifiers)
    selected = select_stratified(source, target=args.target, seed=args.seed)
    private_rows = [
        {"benchmark_id": row["benchmark_id"], **dict(row["private"])} for row in selected
    ]
    atomic_text(
        args.private_output,
        "".join(json.dumps(row, ensure_ascii=False, default=str) + "\n" for row in private_rows),
    )
    manifest = {
        "schema_version": "event_surprise_v2.gold_sample_manifest.v1",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "code_commit": args.code_commit,
        "config_sha256": args.config_sha256.lower(),
        "source_sha256": sha256(args.articles),
        "qwen_sha256": sha256(args.qwen),
        "target": args.target,
        "seed": args.seed,
        "human_gold_status": "PENDING_HUMAN_REVIEW",
        "ai_review_status": "NOT_RUN",
        "private_mapping_committed": False,
        **public_manifest(selected),
    }
    atomic_text(args.public_output, json.dumps(manifest, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
