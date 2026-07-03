"""Source-backed brand/line share-of-voice readout builder (metric-family view).

Implements the field-level contract
``core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md``
under the consumption seam contract's on-demand-first metrics policy: the
readout is COMPUTED ON DEMAND from committed ``silver__cleaning__product_mentions``
records (never from another index), and may optionally be materialized as a
rebuildable, manifest-backed, non-authoritative cache under
``indexes/derived_retrieval/metric_family/<family>/<readout_id>/`` subject to
the same prove-rebuildability check as any index (regenerate under the stored
manifest's recorded spec + stamp and byte-compare; never self-comparing).

Contract invariants enforced here (each pinned by tests):

- Mention-LEVEL refs: every counted mention emits its own dereferenceable ref
  (raw_anchor/lane/record_id/sha256 + mention_id/source_pointer/start_ms/end_ms)
  and ``mention_count == len(mention_refs)`` holds exactly per row.
- Denominator is captured source-backed mentions only; ``share`` recomputes
  from the row's own numerator and the readout denominator.
- Read-side Silver lineage gate: only ``source_backed_complete`` records feed
  evidence; exclusions are counted, never silently dropped.
- Window basis: ``capture_time`` evaluates record ``captured_at`` falling back
  to the packet manifest's known ``timing.capture_time``;
  ``source_publication_time`` evaluates only records carrying publication/event
  timing evidence (record ``observed_at``, else the packet manifest's known
  ``timing.source_publication_or_event``). Records lacking the selected basis
  are excluded from numerator AND denominator and counted under
  ``coverage.window_basis_missing``.
- Cohorts are declared, never inferred: ``member_refs`` (source-object identity
  triples) reconcile to ``coverage.source_objects_in_scope`` by construction;
  a member whose namespace differs from the readout platform is a spec error.
- Zero rows exist only under a declared source-backed ``comparison_set``;
  an empty scope is ``readout_posture: unavailable_with_reason`` with no share
  rows and no denominator field — never a table of zeros.
- Exact-string grouping with a mandatory fragmentation note; the lake never
  normalizes brand/line strings.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from data_lake.canonical_json import canonical_record_bytes
from data_lake.derived_retrieval_views import MENTIONS_LANE, generation_stamp
from data_lake.root import DataLakeRootError
from data_lake.silver_lineage import (
    SOURCE_BACKED_COMPLETE_STATUS,
    silver_record_source_backed_status,
)

METRIC_FAMILY = "source_backed_brand_line_share_of_voice"
FAMILY_SCHEMA_VERSION = 1
SOV_MANIFEST_SCHEMA_VERSION = 1
GROUPING_BASIS = "exact_string_v0"
DENOMINATOR_BASIS = "captured_source_backed_mentions_only"
WINDOW_BASES = ("capture_time", "source_publication_time")
METRIC_FAMILY_PARTS = ("indexes", "derived_retrieval", "metric_family", METRIC_FAMILY)
FRAGMENTATION_NOTE = (
    "grouping is exact_string_v0: case/spelling variants of one real-world brand "
    "or line appear as separate rows until a Cleaning-owned canonicalization is "
    "adopted and cited in selection_policy_versions.brand_grouping"
)


class SovSpecError(DataLakeRootError):
    """A readout spec that cannot honestly parameterize this family (fail-closed)."""


def _require_non_empty_str(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SovSpecError(f"sov spec {field} must be a non-empty string: {value!r}")
    return value


def _parse_ts(value: object) -> datetime | None:
    """Parse an ISO-8601 timestamp; naive values are taken as UTC. None on failure
    (the caller counts the record under window_basis_missing, never drops it)."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _normalize_member_ref(entry: object, platform: str) -> dict[str, str]:
    if not isinstance(entry, dict):
        raise SovSpecError(f"cohort member_refs entries must be objects: {entry!r}")
    ref = {
        field: _require_non_empty_str(entry.get(field), f"cohort member_refs[].{field}")
        for field in ("namespace", "kind", "native_id")
    }
    if ref["namespace"] != platform:
        # Per-platform-only readout identity: a cross-platform cohort is
        # unrepresentable, not silently filtered.
        raise SovSpecError(
            f"cohort member {ref['native_id']!r} namespace {ref['namespace']!r} "
            f"does not match readout platform {platform!r}"
        )
    return ref


def _normalize_comparison_set(entry: object) -> dict:
    if not isinstance(entry, dict):
        raise SovSpecError(f"comparison_set must be an object: {entry!r}")
    keys: list[list[str]] = []
    raw_keys = entry.get("brand_line_keys")
    if not isinstance(raw_keys, list) or not raw_keys:
        raise SovSpecError("comparison_set.brand_line_keys must be a non-empty list")
    for raw in raw_keys:
        if not (isinstance(raw, (list, tuple)) and len(raw) == 2):
            raise SovSpecError(f"comparison_set key must be a [brand, line] pair: {raw!r}")
        brand = _require_non_empty_str(raw[0], "comparison_set brand")
        line = raw[1]
        if not isinstance(line, str):
            raise SovSpecError(f"comparison_set line must be a string: {line!r}")
        keys.append([brand, line])
    if len({tuple(k) for k in keys}) != len(keys):
        raise SovSpecError("comparison_set.brand_line_keys carries duplicate keys")
    return {
        "brand_line_keys": sorted(keys),
        "basis": _require_non_empty_str(entry.get("basis"), "comparison_set.basis"),
        "comparison_set_ref": _require_non_empty_str(
            entry.get("comparison_set_ref"), "comparison_set.comparison_set_ref"
        ),
        "version": _require_non_empty_str(entry.get("version"), "comparison_set.version"),
    }


def normalize_sov_spec(spec: object) -> dict:
    """Validate and canonicalize a readout spec (fail-closed). The normalized
    spec is the deterministic identity of the readout: ``readout_id`` derives
    from its canonical bytes and a materialized manifest stores it verbatim so
    prove-rebuildability can regenerate without any external input."""
    if not isinstance(spec, dict):
        raise SovSpecError(f"sov spec must be an object: {spec!r}")
    platform = _require_non_empty_str(spec.get("platform"), "platform")

    cohort = spec.get("cohort")
    if not isinstance(cohort, dict):
        raise SovSpecError("sov spec cohort must be an object")
    member_refs_raw = cohort.get("member_refs")
    if not isinstance(member_refs_raw, list) or not member_refs_raw:
        raise SovSpecError("cohort.member_refs must be a non-empty list (declared, never inferred)")
    member_refs = [_normalize_member_ref(entry, platform) for entry in member_refs_raw]
    member_keys = {(m["namespace"], m["kind"], m["native_id"]) for m in member_refs}
    if len(member_keys) != len(member_refs):
        raise SovSpecError("cohort.member_refs carries duplicate members")

    window = spec.get("coverage_window")
    if not isinstance(window, dict):
        raise SovSpecError("sov spec coverage_window must be an object")
    basis = window.get("window_basis")
    if basis not in WINDOW_BASES:
        raise SovSpecError(
            f"coverage_window.window_basis must be one of {WINDOW_BASES}: {basis!r}"
        )
    start_raw = _require_non_empty_str(window.get("start"), "coverage_window.start")
    end_raw = _require_non_empty_str(window.get("end"), "coverage_window.end")
    start_ts, end_ts = _parse_ts(start_raw), _parse_ts(end_raw)
    if start_ts is None or end_ts is None:
        raise SovSpecError("coverage_window start/end must be ISO-8601 timestamps")
    if start_ts > end_ts:
        raise SovSpecError("coverage_window.start must be <= coverage_window.end")

    normalized = {
        "metric_family": METRIC_FAMILY,
        "family_schema_version": FAMILY_SCHEMA_VERSION,
        "platform": platform,
        "cohort": {
            "cohort_id": _require_non_empty_str(cohort.get("cohort_id"), "cohort.cohort_id"),
            "definition": _require_non_empty_str(cohort.get("definition"), "cohort.definition"),
            "member_basis": "captured_set",
            "member_refs": sorted(
                member_refs, key=lambda m: (m["namespace"], m["kind"], m["native_id"])
            ),
        },
        "coverage_window": {"start": start_raw, "end": end_raw, "window_basis": basis},
        "cohort_selection": _require_non_empty_str(
            spec.get("cohort_selection"), "cohort_selection"
        ),
    }
    if spec.get("comparison_set") is not None:
        normalized["comparison_set"] = _normalize_comparison_set(spec["comparison_set"])
    return normalized


def sov_readout_id(normalized_spec: dict) -> str:
    """Deterministic readout identity from the normalized spec's canonical bytes."""
    return "sov_" + hashlib.sha256(canonical_record_bytes(normalized_spec)).hexdigest()[:24]


def _packet_timing(root, raw_anchor: str, cache: dict[str, dict]) -> dict:
    """The raw packet manifest's ``timing`` block (known facts only), read by key
    without loading preserved bodies; {} when unavailable (counted as missing
    basis downstream, never faked)."""
    if raw_anchor in cache:
        return cache[raw_anchor]
    timing: dict = {}
    try:
        container = root.find_packet(raw_anchor)
    except DataLakeRootError:
        container = None
    if container is not None:
        try:
            manifest = json.loads((container / "manifest.json").read_text(encoding="utf-8"))
            raw_timing = manifest.get("timing")
            timing = raw_timing if isinstance(raw_timing, dict) else {}
        except (OSError, ValueError):
            timing = {}
    cache[raw_anchor] = timing
    return timing


def _known_fact_value(fact: object) -> str | None:
    if isinstance(fact, dict) and fact.get("status") == "known":
        value = fact.get("value")
        if isinstance(value, str) and value.strip():
            return value
    return None


def _basis_timestamp(record: dict, timing: dict, basis: str) -> datetime | None:
    """The record's timestamp under the selected window basis, or None when the
    record does not carry that basis (counted, never silently dropped)."""
    if basis == "capture_time":
        ts = _parse_ts(record.get("captured_at"))
        if ts is not None:
            return ts
        return _parse_ts(_known_fact_value(timing.get("capture_time")))
    ts = _parse_ts(record.get("observed_at"))
    if ts is not None:
        return ts
    return _parse_ts(_known_fact_value(timing.get("source_publication_or_event")))


def _well_formed_mention(mention: object) -> dict | None:
    """A mention entry that can produce a contract-conforming mention-level ref,
    else None (the caller counts it under malformed_mention_entries)."""
    if not isinstance(mention, dict):
        return None
    mention_id = mention.get("mention_id")
    source_pointer = mention.get("source_pointer")
    start_ms, end_ms = mention.get("start_ms"), mention.get("end_ms")
    if not (isinstance(mention_id, str) and mention_id.strip()):
        return None
    if not (isinstance(source_pointer, str) and source_pointer.strip()):
        return None
    if not (isinstance(start_ms, int) and isinstance(end_ms, int)):
        return None
    brand = mention.get("brand")
    if not (isinstance(brand, str) and brand.strip()):
        brand = "unknown"
    line = mention.get("line")
    if not isinstance(line, str):
        line = ""
    return {
        "brand": brand,
        "line": line,
        "mention_id": mention_id,
        "source_pointer": source_pointer,
        "start_ms": start_ms,
        "end_ms": end_ms,
    }


def compute_sov_readout(root, spec: dict) -> tuple[dict, list[str]]:
    """The readout body plus the source refs a materialized manifest must cite.

    Reads ONLY committed availability + derived records + raw manifests by key —
    never another index — so the on-demand result and a materialized cache are
    the same computation and prove-rebuildability is meaningful.
    """
    normalized = normalize_sov_spec(spec)
    platform = normalized["platform"]
    basis = normalized["coverage_window"]["window_basis"]
    window_start = _parse_ts(normalized["coverage_window"]["start"])
    window_end = _parse_ts(normalized["coverage_window"]["end"])
    member_refs = normalized["cohort"]["member_refs"]
    member_keys = {(m["namespace"], m["kind"], m["native_id"]) for m in member_refs}

    timing_cache: dict[str, dict] = {}
    source_refs: list[str] = []
    counted: dict[tuple[str, str], list[dict]] = {}
    rubric_versions: set[str] = set()

    packets_in_scope: set[str] = set()
    packets_with_transcripts: set[str] = set()
    members_with_records: set[tuple[str, str, str]] = set()
    members_with_gated_records: set[tuple[str, str, str]] = set()
    mention_records_in_scope = 0
    excluded_not_source_backed = 0
    window_basis_missing = 0
    zero_mention_records = 0
    unreadable_lane_records = 0
    malformed_mention_entries = 0

    for raw_anchor in sorted(root.list_available()):
        lane_dir = root.lane_dir(subtree="derived", raw_anchor=raw_anchor, lane=MENTIONS_LANE)
        if not lane_dir.is_dir():
            continue
        for record_file in sorted(p for p in lane_dir.iterdir() if p.is_file()):
            body = record_file.read_bytes()
            source_refs.append(f"{raw_anchor}/{MENTIONS_LANE}/{record_file.name}")
            try:
                record = json.loads(body.decode("utf-8"))
            except ValueError:
                record = None
            if not isinstance(record, dict):
                # Unattributable to any cohort; disclosed lake-wide, never dropped silently.
                unreadable_lane_records += 1
                continue
            source_object = record.get("source_object")
            if not isinstance(source_object, dict):
                continue  # no source-local identity -> not claimable by any declared cohort
            member_key = (
                str(source_object.get("namespace") or ""),
                str(source_object.get("kind") or ""),
                str(source_object.get("native_id") or ""),
            )
            if member_key not in member_keys:
                continue  # out of the declared cohort scope
            mention_records_in_scope += 1
            packets_in_scope.add(raw_anchor)
            members_with_records.add(member_key)
            status = silver_record_source_backed_status(record)
            if status != SOURCE_BACKED_COMPLETE_STATUS:
                excluded_not_source_backed += 1
                continue
            members_with_gated_records.add(member_key)
            packets_with_transcripts.add(raw_anchor)
            ts = _basis_timestamp(record, _packet_timing(root, raw_anchor, timing_cache), basis)
            if ts is None:
                window_basis_missing += 1
                continue
            if not (window_start <= ts <= window_end):
                continue  # outside the declared window: excluded by definition, not a residual
            rubric_versions.add(str(record.get("rubric_version") or "unversioned"))
            sha256 = hashlib.sha256(body).hexdigest()
            mentions = record.get("mentions")
            if not isinstance(mentions, list):
                if mentions is not None:
                    malformed_mention_entries += 1
                mentions = []
            if not mentions:
                zero_mention_records += 1
                continue
            for mention in mentions:
                well_formed = _well_formed_mention(mention)
                if well_formed is None:
                    malformed_mention_entries += 1
                    continue
                counted.setdefault((well_formed["brand"], well_formed["line"]), []).append(
                    {
                        "raw_anchor": raw_anchor,
                        "lane": MENTIONS_LANE,
                        "record_id": record_file.name,
                        "sha256": sha256,
                        "mention_id": well_formed["mention_id"],
                        "source_pointer": well_formed["source_pointer"],
                        "start_ms": well_formed["start_ms"],
                        "end_ms": well_formed["end_ms"],
                    }
                )

    denominator = sum(len(refs) for refs in counted.values())
    coverage = {
        "packets_in_scope": len(packets_in_scope),
        "packets_with_transcripts": len(packets_with_transcripts),
        "mention_records_in_scope": mention_records_in_scope,
        "mention_records_excluded_not_source_backed": excluded_not_source_backed,
        "window_basis_missing": window_basis_missing,
        "source_objects_in_scope": len(member_refs),
        "source_objects_with_transcripts": len(members_with_gated_records),
        "source_backed_records_with_zero_mentions": zero_mention_records,
        "cohort_selection_residuals": {
            "members_without_committed_records": len(member_refs) - len(members_with_records)
        },
        "unreadable_mention_lane_records": unreadable_lane_records,
        "malformed_mention_entries": malformed_mention_entries,
    }
    selection_policy_versions = {
        "extractor_rubric_versions": sorted(rubric_versions),
        "silver_lineage_gate": SOURCE_BACKED_COMPLETE_STATUS,
        "family_schema_version": FAMILY_SCHEMA_VERSION,
        "brand_grouping": GROUPING_BASIS,
        "cohort_selection": normalized["cohort_selection"],
    }
    comparison_set = normalized.get("comparison_set")
    if comparison_set is not None:
        selection_policy_versions["comparison_set"] = comparison_set["version"]

    view = {
        "metric_family": METRIC_FAMILY,
        "family_schema_version": FAMILY_SCHEMA_VERSION,
        "platform": platform,
        "cohort": {
            **normalized["cohort"],
            "member_count": len(member_refs),
        },
        "coverage_window": dict(normalized["coverage_window"]),
        "selection_policy_versions": selection_policy_versions,
        "grouping_basis": GROUPING_BASIS,
        "fragmentation_note": FRAGMENTATION_NOTE,
        "coverage": coverage,
    }
    if comparison_set is not None:
        view["comparison_set"] = comparison_set

    if denominator == 0:
        # An empty scope is a posture, never a table of zeros: no share rows,
        # no denominator field, no comparison zero rows.
        gated_count = mention_records_in_scope - excluded_not_source_backed
        if gated_count == 0:
            reason = "no_source_backed_mention_records_in_scope"
        elif window_basis_missing == gated_count:
            reason = "window_basis_missing_for_all_source_backed_records_in_scope"
        else:
            reason = "no_source_backed_mentions_in_window"
        view["readout_posture"] = "unavailable_with_reason"
        view["readout_reason"] = reason
        view["rows"] = []
        return view, sorted(source_refs)

    row_keys = set(counted)
    if comparison_set is not None:
        row_keys.update((brand, line) for brand, line in comparison_set["brand_line_keys"])
    rows = []
    for brand, line in sorted(row_keys):
        refs = sorted(
            counted.get((brand, line), []),
            key=lambda r: (r["raw_anchor"], r["record_id"], r["start_ms"], r["mention_id"]),
        )
        rows.append(
            {
                "brand": brand,
                "line": line,
                "mention_count": len(refs),
                "mention_refs": refs,
                "share": len(refs) / denominator,
            }
        )
    view["readout_posture"] = "observed"
    view["rows"] = rows
    view["denominator"] = denominator
    view["denominator_basis"] = DENOMINATOR_BASIS
    return view, sorted(source_refs)


def _sov_manifest(
    normalized_spec: dict, readout_id: str, view_bytes: bytes, source_refs: list[str], stamp: dict
) -> dict:
    return {
        "manifest_schema_version": SOV_MANIFEST_SCHEMA_VERSION,
        "metric_family": METRIC_FAMILY,
        "family_schema_version": FAMILY_SCHEMA_VERSION,
        "readout_id": readout_id,
        "spec": normalized_spec,
        "generation_id": stamp["generation_id"],
        "generated_at": stamp["generated_at"],
        "source_record_ids": source_refs,
        "source_high_watermark": hashlib.sha256(
            canonical_record_bytes(source_refs)
        ).hexdigest(),
        "view_sha256": hashlib.sha256(view_bytes).hexdigest(),
        "stale_if": (
            "any committed availability/derived/raw-manifest change affecting the "
            "spec scope after source_high_watermark; verify with --prove-rebuildability"
        ),
    }


def _generate_sov_files(root, normalized_spec: dict, stamp: dict) -> dict[str, bytes]:
    """Both readout files as relpath -> bytes under the given stamp (pure)."""
    readout_id = sov_readout_id(normalized_spec)
    view, source_refs = compute_sov_readout(root, normalized_spec)
    view_bytes = canonical_record_bytes(view)
    manifest_bytes = canonical_record_bytes(
        _sov_manifest(normalized_spec, readout_id, view_bytes, source_refs, stamp)
    )
    return {"view.json": view_bytes, "manifest.json": manifest_bytes}


def _metric_family_root(root) -> Path:
    return root._within(*METRIC_FAMILY_PARTS)


def materialize_sov_readout(root, spec: dict, *, stamp: dict | None = None) -> dict:
    """Write one readout as a rebuildable cache (wipe-and-rewrite of that
    readout's directory only — the rebuildable-tier pattern). Never authoritative;
    the seam helper and pickup never read it."""
    root._reverify()
    normalized = normalize_sov_spec(spec)
    readout_id = sov_readout_id(normalized)
    stamp = stamp or generation_stamp()
    files = _generate_sov_files(root, normalized, stamp)
    target_dir = _metric_family_root(root) / readout_id
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    for relpath, data in files.items():
        (target_dir / relpath).write_bytes(data)
    view = json.loads(files["view.json"].decode("utf-8"))
    return {
        "status": "materialized",
        "readout_id": readout_id,
        "path": "/".join((*METRIC_FAMILY_PARTS, readout_id)),
        "readout_posture": view["readout_posture"],
        "row_count": len(view["rows"]),
        "generation_id": stamp["generation_id"],
        "file_count": len(files),
    }


def list_materialized_sov_readouts(root) -> list[str]:
    family_root = _metric_family_root(root)
    if not family_root.is_dir():
        return []
    return sorted(p.name for p in family_root.iterdir() if p.is_dir())


def prove_sov_rebuildability(root) -> dict:
    """Read-only verification for every materialized readout: regenerate under
    the stored manifest's recorded spec + stamp and byte-compare both files.
    Never compares a rebuild against itself; never writes."""
    root._reverify()
    family_root = _metric_family_root(root)
    results: dict[str, str] = {}
    failures: list[str] = []
    for readout_id in list_materialized_sov_readouts(root):
        view_path = family_root / readout_id / "view.json"
        manifest_path = family_root / readout_id / "manifest.json"
        if not view_path.is_file() or not manifest_path.is_file():
            results[readout_id] = "failed_partial_files"
            failures.append(readout_id)
            continue
        try:
            stored_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            spec = stored_manifest["spec"]
            stamp = {
                "generation_id": stored_manifest["generation_id"],
                "generated_at": stored_manifest["generated_at"],
            }
            regenerated = _generate_sov_files(root, normalize_sov_spec(spec), stamp)
        except (ValueError, KeyError, TypeError, SovSpecError):
            results[readout_id] = "failed_unreadable_manifest"
            failures.append(readout_id)
            continue
        if (
            regenerated["view.json"] == view_path.read_bytes()
            and regenerated["manifest.json"] == manifest_path.read_bytes()
        ):
            results[readout_id] = "rebuildable"
        else:
            results[readout_id] = "failed_drift_or_non_regenerable"
            failures.append(readout_id)
    return {
        "status": "proven" if not failures else "failed",
        "results": results,
        "failures": failures,
    }


__all__ = [
    "DENOMINATOR_BASIS",
    "FAMILY_SCHEMA_VERSION",
    "FRAGMENTATION_NOTE",
    "GROUPING_BASIS",
    "METRIC_FAMILY",
    "METRIC_FAMILY_PARTS",
    "SOV_MANIFEST_SCHEMA_VERSION",
    "SovSpecError",
    "WINDOW_BASES",
    "compute_sov_readout",
    "list_materialized_sov_readouts",
    "materialize_sov_readout",
    "normalize_sov_spec",
    "prove_sov_rebuildability",
    "sov_readout_id",
]
