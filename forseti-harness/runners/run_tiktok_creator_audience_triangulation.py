"""Build one scratch Gold-ready assembly and one validated TikTok audience profile."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.audience_extractor import RawApiProvider, Transport
from evidence_binding.tiktok_audience_triangulation import build_gold_ready_audience_evidence
from runners.run_memorization_probe_raw_api import UrllibJsonTransport
from judgment.tiktok_audience_triangulation import build_triangulation_prompt, triangulate_audience


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _evidence_rows(paths: list[Path]) -> list[Mapping[str, Any]]:
    rows: list[Mapping[str, Any]] = []
    for path in paths:
        value: Any = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict):
            value = value.get("evidence")
        if not isinstance(value, list) or not all(isinstance(row, Mapping) for row in value):
            raise ValueError(f"transcript evidence must be a list or evidence wrapper: {path}")
        rows.extend(value)
    return rows


def _write_new_json(path: Path, value: Mapping[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to replace existing output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def run_triangulation(
    *,
    creator_id: str,
    batch_payloads: list[Mapping[str, Any]],
    transcript_evidence: list[Mapping[str, Any]],
    question: str,
    evidence_cutoff: str,
    semantic_labels: Mapping[str, Any] | None,
    assembly_out: Path,
    profile_out: Path,
    transport: Transport,
    provider: RawApiProvider,
    model: str,
    api_key: str,
    max_tokens: int = 4096,
) -> dict[str, Any]:
    if assembly_out.resolve() == profile_out.resolve():
        raise ValueError("assembly_out and profile_out must be different files")
    assembly = build_gold_ready_audience_evidence(
        creator_id=creator_id,
        batch_payloads=batch_payloads,
        transcript_evidence=transcript_evidence,
        question=question,
        evidence_cutoff=evidence_cutoff,
        semantic_labels=semantic_labels,
    )
    _write_new_json(assembly_out, assembly)
    profile = triangulate_audience(
        assembly=assembly,
        transport=transport,
        provider=provider,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
    )
    profile_document = {
        "profile": profile.model_dump(mode="json"),
        "run_receipt": {
            "creator_id": assembly["creator_id"],
            "model": model,
            "provider": provider.value,
            "gold_model_call_count": 1,
            "prompt_utf8_bytes": len(build_triangulation_prompt(assembly).encode("utf-8")),
            "assembly_utf8_bytes": assembly["assembly_receipt"]["serialized_utf8_bytes"],
        },
    }
    _write_new_json(profile_out, profile_document)
    return profile_document


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--creator-id", required=True)
    parser.add_argument("--batch", type=Path, action="append", required=True)
    parser.add_argument("--transcript-evidence", type=Path, action="append", default=[])
    parser.add_argument("--comment-labels", type=Path)
    parser.add_argument("--question", required=True)
    parser.add_argument("--evidence-cutoff", required=True)
    parser.add_argument("--assembly-out", type=Path, required=True)
    parser.add_argument("--profile-out", type=Path, required=True)
    parser.add_argument("--provider", choices=[item.value for item in RawApiProvider], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key-env", required=True)
    parser.add_argument("--max-tokens", type=int, default=4096)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        api_key = os.environ.get(args.api_key_env, "")
        if not api_key:
            raise ValueError(f"environment variable {args.api_key_env} is missing or blank")
        result = run_triangulation(
            creator_id=args.creator_id,
            batch_payloads=[_load_object(path) for path in args.batch],
            transcript_evidence=_evidence_rows(args.transcript_evidence),
            question=args.question,
            evidence_cutoff=args.evidence_cutoff,
            semantic_labels=_load_object(args.comment_labels) if args.comment_labels else None,
            assembly_out=args.assembly_out,
            profile_out=args.profile_out,
            transport=UrllibJsonTransport(),
            provider=RawApiProvider(args.provider),
            model=args.model,
            api_key=api_key,
            max_tokens=args.max_tokens,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps({"status": "written", **result["run_receipt"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
