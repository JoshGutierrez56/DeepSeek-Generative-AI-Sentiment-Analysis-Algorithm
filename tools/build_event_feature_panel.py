"""Build a private outcome-blind feature panel and public-safe manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from sentiment_lab.event_surprise.features_v2 import (
    build_event_feature_panel,
    feature_panel_summary,
)


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
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--extractions", type=Path, required=True)
    parser.add_argument("--classifiers", type=Path, required=True)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--public-output", type=Path, required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()

    articles = pl.read_parquet(
        args.articles,
        columns=[
            "article_id",
            "provider",
            "provider_timestamp",
            "retrieved_at",
            "ticker",
            "story_cluster_id",
        ],
    )
    extractions = pl.read_parquet(args.extractions)
    classifiers = pl.read_parquet(args.classifiers)
    panel = build_event_feature_panel(articles, extractions, classifiers)
    if args.private_output.exists():
        raise FileExistsError(f"refusing to overwrite {args.private_output}")
    args.private_output.parent.mkdir(parents=True, exist_ok=True)
    panel.write_parquet(args.private_output)
    manifest = {
        "schema_version": "event_surprise_v2.event_feature_manifest.v1",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "code_commit": args.code_commit,
        "config_sha256": args.config_sha256,
        "source_hashes": {
            "articles": sha256(args.articles),
            "extractions": sha256(args.extractions),
            "classifiers": sha256(args.classifiers),
        },
        "private_panel_sha256": sha256(args.private_output),
        "private_panel_committed": False,
        "clustering_uses_market_outcomes": False,
        "feature_selection_uses_market_outcomes": False,
        "residual_novelty_method": "issuer expanding prior mean; first observation null",
        **feature_panel_summary(panel),
    }
    atomic_json(args.public_output, manifest)


if __name__ == "__main__":
    main()
