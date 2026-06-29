"""Driver: run Pass 1 over a transcript and persist the mentions into the Data Lake.

Mirrors `ecr/lake.py` (read/derive/append), adapted for the LLM extractor: take a
TranscriptInput, run `extract_transcript_products`, and append the validated mentions as a
silver derived record-set at
``derived/<transcript_anchor>/silver__cleaning__product_mentions/<record_id>`` with an
all-or-nothing completion marker (so the runner can skip already-extracted transcripts).

Lives in `cleaning/` because it invokes the LLM extractor. Also owns the source->cues
normalizers (ASR derived record / caption json3), so the runner stays a thin orchestrator.

Spec: youtube_transcript_product_extraction_spec_v0.md (medallion silver lane; daemon-ready).
"""

from __future__ import annotations

import hashlib
import json
import math
import re

from cleaning.transcript_product_extractor import (
    EXTRACTOR_RUBRIC_VERSION,
    TranscriptInput,
    extract_transcript_products,
)
from data_lake.silver_lineage import (
    SilverDerivedRef,
    SilverLineage,
    SilverLineageLimitation,
    SilverRawRef,
    SilverSourceObject,
    validate_silver_lineage,
)

# Silver lane (tiered medallion name) + its sibling completion-marker lane.
PRODUCT_MENTIONS_LANE = "silver__cleaning__product_mentions"
PRODUCT_MENTIONS_SET_LANE = "silver__cleaning__product_mentions__set"

# Producer identity stamped into the Silver lineage block of every product-mention
# record (the producer is this Pass-1 extractor; its schema version is the rubric).
PRODUCT_MENTIONS_PRODUCER_ID = "cleaning.transcript_product_extractor"


def build_transcript_source_lineage(
    *,
    namespace: str,
    source_surface: str,
    video_id: str,
    derived_ref: SilverDerivedRef | None = None,
    raw_ref: SilverRawRef | None = None,
    limitations: list[SilverLineageLimitation] | None = None,
    captured_at: str | None = None,
) -> SilverLineage:
    """Assemble the Silver lineage block for a product-mention record from the exact
    transcript source the runner discovered. Stamps this producer's identity and the
    transcript's source-local identity (``namespace + kind=transcript + native_id``);
    the caller supplies exactly one of a ``derived_ref`` (ASR -> the consumed
    ``transcript_asr`` derived record) or a ``raw_ref`` (caption -> the json3
    preserved file). Validated on construction (fail-closed)."""
    return SilverLineage(
        producer_id=PRODUCT_MENTIONS_PRODUCER_ID,
        producer_schema_version=EXTRACTOR_RUBRIC_VERSION,
        source_surface=source_surface,
        source_object=SilverSourceObject(namespace=namespace, kind="transcript", native_id=video_id),
        captured_at=captured_at,
        raw_refs=[raw_ref] if raw_ref is not None else [],
        derived_refs=[derived_ref] if derived_ref is not None else [],
        lineage_limitations=list(limitations or []),
    )


def cues_from_asr_record(record: dict) -> list[dict]:
    """Cues from a transcript_asr derived record (already {start_ms,end_ms,text})."""
    cues = record.get("cues")
    return cues if isinstance(cues, list) else []


def cues_from_json3(raw: bytes) -> list[dict]:
    """Parse caption json3 into ms-timed cues, PRESERVING timing.

    Unlike `flatten_json3` (which drops timing for a readable view), this keeps each event's
    start/end so caption-sourced mentions still get a timestamp anchor (CE5). Rolling
    duplicate lines are collapsed (consecutive identical text), matching the flattener.
    """
    # Fail-closed: an untrusted/corrupt json3 body yields [] (the runner then skips it),
    # never an exception that could abort the batch.
    try:
        data = json.loads(raw.decode("utf-8", "replace"))
    except ValueError:
        return []
    events = data.get("events", []) if isinstance(data, dict) else []
    cues: list[dict] = []
    prev: str | None = None
    for event in events:
        if not isinstance(event, dict):
            continue
        segs = event.get("segs") or []
        if not isinstance(segs, list) or not segs:
            continue
        text = "".join(s.get("utf8", "") for s in segs if isinstance(s, dict)).strip()
        if not text or text == prev:
            continue
        # finite-guard, not just type-guard: json.loads accepts bare NaN/Infinity, which ARE
        # floats (so isinstance passes) but raise on int() — guard them or the documented
        # fail-closed contract breaks. Negative duration is clamped so end_ms >= start_ms.
        raw_start = event.get("tStartMs", 0)
        start = int(raw_start) if isinstance(raw_start, (int, float)) and math.isfinite(raw_start) else 0
        duration = event.get("dDurationMs")
        end = (
            start + max(0, int(duration))
            if isinstance(duration, (int, float)) and math.isfinite(duration)
            else start
        )
        cues.append({"start_ms": start, "end_ms": end, "text": text})
        prev = text
    return cues


def mentions_record_id(transcript: TranscriptInput, model: str) -> str:
    """Deterministic per (transcript content, model) so re-runs check/skip the same record.

    The model token is bounded so the id stays within the lake's 128-char _SAFE_SEGMENT limit
    for any model string; the full model is still recorded in the record payload + provenance.
    """
    token = re.sub(r"[^A-Za-z0-9_-]", "-", str(model))[:48]
    digest = hashlib.sha256(transcript.joined_text.encode("utf-8")).hexdigest()
    return f"mentions_{token}__{digest[:16]}.json"


def extract_products_into_lake(
    *,
    data_root,
    transcript: TranscriptInput,
    transport,
    provider,
    model: str,
    api_key: str,
    record_id: str | None = None,
    max_tokens: int = 2048,
) -> dict[str, "object"]:
    """Run Pass 1 for one transcript and append the silver mentions record-set.

    Returns the written member paths. Re-appending the same record_id is refused by the lake
    (write-once); the runner avoids that by checking `is_record_set_complete` first.
    """
    rid = record_id or mentions_record_id(transcript, model)
    result = extract_transcript_products(
        transcript,
        transport=transport,
        provider=provider,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
    )
    payload = {
        "video_id": transcript.video_id,
        "transcript_anchor": transcript.transcript_anchor,
        "transcript_source": transcript.transcript_source,
        "model": model,
        "rubric_version": EXTRACTOR_RUBRIC_VERSION,
        "mention_count": len(result.mentions),
        "rejected_count": len(result.rejected),
        "mentions": [m.model_dump(mode="json") for m in result.mentions],
        "rejected": result.rejected,
    }
    # Silver lineage (additive): when the runner threaded the exact consumed source
    # (the transcript_asr derived record for ASR, or the json3 preserved file for
    # caption), populate the record's lineage fields IN PLACE so a downstream agent
    # can resolve the exact source consumed -- closing the same-shortcode ambiguity.
    # AR-01: these are top-level header-shaped fields, never a nested silver_lineage
    # block. Re-validated at this write boundary (fail-closed) before persistence.
    if transcript.source_lineage is not None:
        payload.update(validate_silver_lineage(transcript.source_lineage).to_record_fields())
    members = {
        # allow_nan=False: a non-finite float fails closed (the runner records `failed`) rather
        # than writing a literal NaN/Infinity token that is invalid RFC-8259 JSON.
        PRODUCT_MENTIONS_LANE: (
            json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        ).encode("utf-8")
    }
    return data_root.append_record_set(
        subtree="derived",
        raw_anchor=transcript.transcript_anchor,
        record_id=rid,
        members=members,
        completion_lane=PRODUCT_MENTIONS_SET_LANE,
    )
