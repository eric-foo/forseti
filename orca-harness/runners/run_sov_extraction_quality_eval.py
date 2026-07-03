"""Read-only extraction-quality eval for the SoV pipeline (measurement, not gate).

Measures, over EVERY committed ``silver__cleaning__product_mentions`` record in
the lake, the two things a share-of-voice reader cannot see from a readout
alone:

1. **Substrate snapshot** — how much extracted evidence actually exists:
   packets by family, mention records by read-side lineage-gate status,
   named-brand vs unknown-brand mention distribution, window-timing field
   presence, transcript-resolution dispositions.
2. **Brand knowledge-leak scan** — for every named-brand mention whose source
   transcript is resolvable via the record's OWN ``raw_refs`` (caption json3,
   hash-verified through ``load_raw_packet``), whether the brand string appears
   anywhere in the transcript text (casefold substring). A mention whose brand
   never appears in its transcript is a **leak**: the brand attribution came
   from model knowledge, not the creator's speech — exactly the un-source-backed
   step the extractor rubric forbids ("never invent a brand").

Honesty rules (mirrors the lake's counted-never-dropped posture):

- Every record and mention lands in exactly one counted disposition; nothing is
  silently skipped. Unreadable records, gate-failing records, records without a
  resolvable transcript ref, and failed packet loads are all counted classes.
- Read-only: no lake writes, no LLM calls (no-LLM runner zone), no new lake API.
- The output is measurement, not validation: it carries its own non-claims and
  a small-sample label; it asserts no extractor recall/precision (ground-truth
  labeling is a separate, deferred unit) and no readiness.

Leak-check limitation (named): matching is casefold substring over the joined
cue text — diacritic or spelling variants of a brand ("Hermes" spoken vs
"Hermès" emitted) count as leaks. Interpret per-brand results with that in
mind; the per-brand breakdown plus leaked-sample refs exist for exactly that
spot-check.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.transcript_product_lake import cues_from_json3
from data_lake.derived_retrieval_views import MENTIONS_LANE
from data_lake.root import DataLakeRoot, DataLakeRootError
from data_lake.silver_lineage import (
    SOURCE_BACKED_COMPLETE_STATUS,
    silver_record_source_backed_status,
)

EVAL_SCHEMA_VERSION = 1
LEAKED_SAMPLE_CAP = 20

NON_CLAIMS = [
    "not extractor recall or precision (ground-truth labeling is a separate deferred unit)",
    "not validation, readiness, acceptance, or a go-live claim",
    "leak matching is casefold substring; diacritic/spelling variants of a spoken brand count as leaks",
    "read-only measurement over committed records; writes nothing into the lake",
]


def _is_named_brand(value: object) -> bool:
    return isinstance(value, str) and value.strip().casefold() not in {"", "unknown"}


def _transcript_text_from_json3(raw: bytes) -> str:
    return " ".join(cue["text"] for cue in cues_from_json3(raw))


def _resolve_transcript(root: DataLakeRoot, record: dict) -> tuple[str | None, str]:
    """(transcript_text, disposition) for one gated mention record, using ONLY
    the record's own raw_refs. Every failure path is a named disposition."""
    json3_ref = None
    for ref in record.get("raw_refs") or []:
        if not isinstance(ref, dict):
            continue
        if str(ref.get("relative_packet_path") or "").endswith(".json3"):
            json3_ref = ref
            break
    if json3_ref is None:
        return None, "no_raw_transcript_ref"
    packet_id = str(json3_ref.get("packet_id") or "")
    try:
        loaded = root.load_raw_packet(packet_id)
    except DataLakeRootError:
        return None, "packet_load_failed"
    body = loaded.bodies.get(str(json3_ref.get("file_id") or ""))
    if body is None:
        # Fall back to path-suffix match within the SAME packet the ref names.
        for preserved in loaded.manifest.get("preserved_files") or []:
            if isinstance(preserved, dict) and str(
                preserved.get("relative_packet_path") or ""
            ).endswith(".json3"):
                body = loaded.bodies.get(str(preserved.get("file_id") or ""))
                break
    if body is None:
        return None, "transcript_file_missing_in_packet"
    text = _transcript_text_from_json3(body)
    if not text.strip():
        return None, "json3_empty_or_unparseable"
    return text, "resolved_caption_json3"


def run_eval(root: DataLakeRoot) -> dict:
    """The full eval report as a dict, computed purely from committed material."""
    packet_ids = sorted(root.list_available())
    packets_by_family: dict[str, int] = {}
    for packet_id in packet_ids:
        entry = root.read_availability(packet_id) or {}
        family = str(entry.get("source_family") or "unknown")
        packets_by_family[family] = packets_by_family.get(family, 0) + 1

    records_total = 0
    records_unreadable = 0
    records_by_gate_status: dict[str, int] = {}
    records_by_transcript_disposition: dict[str, int] = {}
    records_with_captured_at = 0
    records_with_observed_at = 0
    malformed_mention_entries = 0
    mentions_named = 0
    mentions_unknown_or_blank = 0
    named_scanned_present = 0
    named_scanned_leaked = 0
    named_unscannable = 0
    per_brand: dict[str, dict[str, int]] = {}
    leaked_samples: list[dict] = []

    for raw_anchor in packet_ids:
        lane_dir = root.lane_dir(subtree="derived", raw_anchor=raw_anchor, lane=MENTIONS_LANE)
        if not lane_dir.is_dir():
            continue
        for record_file in sorted(p for p in lane_dir.iterdir() if p.is_file()):
            records_total += 1
            try:
                record = json.loads(record_file.read_bytes().decode("utf-8"))
            except ValueError:
                record = None
            if not isinstance(record, dict):
                records_unreadable += 1
                continue
            status = silver_record_source_backed_status(record)
            records_by_gate_status[status] = records_by_gate_status.get(status, 0) + 1
            if record.get("captured_at"):
                records_with_captured_at += 1
            if record.get("observed_at"):
                records_with_observed_at += 1
            if status != SOURCE_BACKED_COMPLETE_STATUS:
                continue  # counted above; gate-failing records are never scanned

            mentions = record.get("mentions")
            if not isinstance(mentions, list):
                if mentions is not None:
                    malformed_mention_entries += 1
                mentions = []
            named_mentions: list[dict] = []
            for mention in mentions:
                if not isinstance(mention, dict):
                    malformed_mention_entries += 1
                    continue
                if _is_named_brand(mention.get("brand")):
                    mentions_named += 1
                    named_mentions.append(mention)
                else:
                    mentions_unknown_or_blank += 1

            transcript, disposition = (
                _resolve_transcript(root, record) if named_mentions else (None, None)
            )
            if disposition is not None:
                records_by_transcript_disposition[disposition] = (
                    records_by_transcript_disposition.get(disposition, 0) + 1
                )
            if not named_mentions:
                continue
            if transcript is None:
                named_unscannable += len(named_mentions)
                continue
            transcript_folded = transcript.casefold()
            for mention in named_mentions:
                brand = str(mention.get("brand")).strip()
                tally = per_brand.setdefault(brand, {"mentions": 0, "leaked": 0})
                tally["mentions"] += 1
                if brand.casefold() in transcript_folded:
                    named_scanned_present += 1
                else:
                    named_scanned_leaked += 1
                    tally["leaked"] += 1
                    if len(leaked_samples) < LEAKED_SAMPLE_CAP:
                        leaked_samples.append(
                            {
                                "raw_anchor": raw_anchor,
                                "record_id": record_file.name,
                                "mention_id": str(mention.get("mention_id") or ""),
                                "brand": brand,
                                "line": str(mention.get("line") or ""),
                            }
                        )

    scanned = named_scanned_present + named_scanned_leaked
    return {
        "eval": "sov_extraction_quality_eval",
        "eval_schema_version": EVAL_SCHEMA_VERSION,
        "substrate": {
            "packets_total": len(packet_ids),
            "packets_by_source_family": dict(sorted(packets_by_family.items())),
            "mention_records_total": records_total,
            "mention_records_unreadable": records_unreadable,
            "mention_records_by_gate_status": dict(sorted(records_by_gate_status.items())),
            "records_with_captured_at": records_with_captured_at,
            "records_with_observed_at": records_with_observed_at,
            "malformed_mention_entries": malformed_mention_entries,
            "mentions_named_brand": mentions_named,
            "mentions_unknown_or_blank_brand": mentions_unknown_or_blank,
        },
        "transcript_resolution": {
            "records_by_disposition": dict(sorted(records_by_transcript_disposition.items())),
            "named_mentions_unscannable": named_unscannable,
        },
        "knowledge_leak_scan": {
            "named_mentions_scanned": scanned,
            "brand_present_in_transcript": named_scanned_present,
            "brand_absent_from_transcript_leaked": named_scanned_leaked,
            "leak_rate": (named_scanned_leaked / scanned) if scanned else None,
            "per_brand": dict(sorted(per_brand.items())),
            "leaked_samples": leaked_samples,
            "leaked_samples_cap": LEAKED_SAMPLE_CAP,
        },
        "sample_size_note": (
            "measurement over the CURRENT committed substrate only; treat rates as "
            "small-sample estimates until the substrate grows"
        ),
        "non_claims": NON_CLAIMS,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only SoV extraction-quality eval: substrate snapshot + brand "
            "knowledge-leak scan over committed product-mention records."
        )
    )
    parser.add_argument(
        "--root",
        "--data-root",
        dest="data_root",
        help="Explicit Orca data root path (falls back to ORCA_DATA_ROOT).",
    )
    parser.add_argument(
        "--out",
        help="Optional file path (outside the data root) to also write the JSON report to.",
    )
    args = parser.parse_args(argv)

    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        if args.out:
            out_path = Path(args.out).resolve()
            try:
                out_path.relative_to(root.path.resolve())
            except ValueError:
                pass  # outside the lake: allowed
            else:
                raise DataLakeRootError(
                    f"--out must not write inside the data root (read-only eval): {out_path}"
                )
        report = run_eval(root)
    except DataLakeRootError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2

    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
