"""TikTok creator-audience onboarding work queue over append-only lake records.

The queue is intentionally specific: it transports the already-prepared
creator-audience bundle/prompt, leases that work to one cold subscription
context, and records only terminal success or an explicit terminal block.  It
is not a generic event framework or a model executor.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping

from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRoot, DataLakeRootError


JOB_LANE = "creator_audience_onboarding_job"
CLAIM_LANE = "creator_audience_onboarding_claim"
TERMINAL_LANE = "creator_audience_onboarding_terminal"
JOB_SCHEMA_VERSION = "creator_audience_onboarding_job_v1"
CLAIM_SCHEMA_VERSION = "creator_audience_onboarding_claim_v1"
TERMINAL_SCHEMA_VERSION = "creator_audience_onboarding_terminal_v1"
DEFAULT_LEASE_SECONDS = 30 * 60
DEFAULT_CAPACITY = 10
_BUNDLE_DERIVED_KEYS = frozenset({"bundle_hash", "bundle_id", "serialized_utf8_bytes"})


class CreatorAudienceQueueError(ValueError):
    """Fail-closed queue state, identity, or lease error."""


def enqueue_creator_audience_job(
    *,
    data_root: DataLakeRoot,
    bundle_path: Path,
    prompt_path: Path,
    enqueued_at: str | None = None,
) -> dict[str, Any]:
    """Persist the exact prepared transport, idempotently by bundle hash."""

    bundle_bytes = bundle_path.read_bytes()
    prompt_bytes = prompt_path.read_bytes()
    try:
        bundle = json.loads(bundle_bytes.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CreatorAudienceQueueError(f"audience bundle is not UTF-8 JSON: {exc}") from exc
    if not isinstance(bundle, Mapping):
        raise CreatorAudienceQueueError("audience bundle must be a JSON object")
    try:
        prompt_text = prompt_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CreatorAudienceQueueError("audience prompt must be UTF-8") from exc
    if not prompt_text.strip():
        raise CreatorAudienceQueueError("audience prompt must be nonblank")
    _verify_bundle_content_hash(bundle)

    bundle_hash = _text(bundle.get("bundle_hash"), "bundle_hash")
    raw_anchor = _text(bundle.get("raw_anchor"), "raw_anchor")
    job_id = "cajq_" + hashlib.sha256(bundle_hash.encode("utf-8")).hexdigest()[:24]
    semantic = {
        "schema_version": JOB_SCHEMA_VERSION,
        "record_id": job_id,
        "job_id": job_id,
        "raw_anchor": raw_anchor,
        "platform": "tiktok",
        "creator_id": _text(bundle.get("creator_id"), "creator_id"),
        "profile_subject_id": _text(
            bundle.get("profile_subject_id"), "profile_subject_id"
        ),
        "bundle_id": _text(bundle.get("bundle_id"), "bundle_id"),
        "bundle_hash": bundle_hash,
        "bundle_sha256": _sha256(bundle_bytes),
        "prompt_sha256": _sha256(prompt_bytes),
        "bundle_bytes_b64": base64.b64encode(bundle_bytes).decode("ascii"),
        "prompt_bytes_b64": base64.b64encode(prompt_bytes).decode("ascii"),
    }
    record = {**semantic, "enqueued_at": _timestamp(enqueued_at)}
    target = data_root.record_path(
        subtree="derived", raw_anchor=raw_anchor, lane=JOB_LANE, record_id=job_id
    )
    if target.exists():
        existing = _load_object(target)
        _verify_enqueue_replay(existing, semantic)
        return _enqueue_result(existing, "already_current")
    try:
        data_root.append_record(
            subtree="derived",
            raw_anchor=raw_anchor,
            lane=JOB_LANE,
            record_id=job_id,
            data=canonical_record_bytes(record),
        )
    except DataLakeRootError:
        if not target.is_file():
            raise
        existing = _load_object(target)
        _verify_enqueue_replay(existing, semantic)
        return _enqueue_result(existing, "already_current")
    return _enqueue_result(record, "enqueued")


def load_creator_audience_queue(
    data_root: DataLakeRoot, *, now: str | None = None
) -> dict[str, Any]:
    """Fold all creator-audience job records into fail-closed current state."""

    observed_at = _timestamp(now)
    observed_dt = _parse_timestamp(observed_at, "now")
    jobs = _unique_records(data_root, JOB_LANE, JOB_SCHEMA_VERSION, "job_id")
    claims = _records(data_root, CLAIM_LANE, CLAIM_SCHEMA_VERSION)
    terminals = _unique_records(
        data_root, TERMINAL_LANE, TERMINAL_SCHEMA_VERSION, "job_id"
    )
    for job_id, job in jobs.items():
        _validate_job(job_id, job)
    claims_by_job: dict[str, list[dict[str, Any]]] = {job_id: [] for job_id in jobs}
    for claim in claims:
        job_id = _text(claim.get("job_id"), "claim job_id")
        if job_id not in jobs:
            raise CreatorAudienceQueueError(f"claim references unknown job: {job_id}")
        _validate_claim(claim, jobs[job_id])
        claims_by_job[job_id].append(claim)
    for job_id, terminal in terminals.items():
        if job_id not in jobs:
            raise CreatorAudienceQueueError(f"terminal references unknown job: {job_id}")
        _validate_terminal(terminal, jobs[job_id], claims_by_job[job_id])

    rows: list[dict[str, Any]] = []
    for job_id, job in jobs.items():
        ordered = sorted(
            claims_by_job[job_id], key=lambda row: int(row["claim_generation"])
        )
        _validate_claim_chain(job_id, ordered)
        terminal = terminals.get(job_id)
        if terminal is not None:
            state = str(terminal["status"])
            active_claim = None
        elif ordered:
            latest = ordered[-1]
            expires = _parse_timestamp(str(latest["lease_expires_at"]), "lease expiry")
            state = "running" if observed_dt < expires else "queued"
            active_claim = latest if state == "running" else None
        else:
            state = "queued"
            active_claim = None
        rows.append(
            {
                "job_id": job_id,
                "raw_anchor": job["raw_anchor"],
                "platform": job["platform"],
                "creator_id": job["creator_id"],
                "profile_subject_id": job["profile_subject_id"],
                "bundle_id": job["bundle_id"],
                "bundle_hash": job["bundle_hash"],
                "enqueued_at": job["enqueued_at"],
                "state": state,
                "claim_generation": (
                    int(ordered[-1]["claim_generation"]) if ordered else 0
                ),
                "active_lease": (
                    {
                        "lease_id": active_claim["lease_id"],
                        "worker_id": active_claim["worker_id"],
                        "claimed_at": active_claim["claimed_at"],
                        "lease_expires_at": active_claim["lease_expires_at"],
                    }
                    if active_claim is not None
                    else None
                ),
                "terminal": terminal,
                "_job_record": job,
            }
        )
    rows.sort(key=lambda row: (str(row["enqueued_at"]), str(row["job_id"])))
    counts = {state: sum(row["state"] == state for row in rows) for state in (
        "queued", "running", "succeeded", "blocked"
    )}
    return {
        "schema_version": "creator_audience_onboarding_queue_view_v1",
        "observed_at": observed_at,
        "counts": {**counts, "unfinished": counts["queued"] + counts["running"]},
        "jobs": rows,
    }


def public_queue_view(data_root: DataLakeRoot, *, now: str | None = None) -> dict[str, Any]:
    projection = load_creator_audience_queue(data_root, now=now)
    return {
        **projection,
        "jobs": [
            {key: value for key, value in row.items() if not key.startswith("_")}
            for row in projection["jobs"]
        ],
    }


def unfinished_profile_subject_ids(
    data_root: DataLakeRoot, *, now: str | None = None
) -> set[str]:
    return {
        str(row["profile_subject_id"])
        for row in load_creator_audience_queue(data_root, now=now)["jobs"]
        if row["state"] in {"queued", "running"}
    }


def assert_creator_audience_capacity(
    data_root: DataLakeRoot,
    *,
    capacity: int = DEFAULT_CAPACITY,
    now: str | None = None,
) -> dict[str, Any]:
    projection = load_creator_audience_queue(data_root, now=now)
    unfinished = int(projection["counts"]["unfinished"])
    if unfinished >= capacity:
        raise CreatorAudienceQueueError(
            "AUDIENCE_QUEUE_CAPACITY_REACHED: "
            f"queued={projection['counts']['queued']} running={projection['counts']['running']} "
            f"capacity={capacity}"
        )
    return projection["counts"]


def claim_creator_audience_job(
    *,
    data_root: DataLakeRoot,
    worker_id: str,
    prompt_out: Path,
    now: str | None = None,
    lease_seconds: int = DEFAULT_LEASE_SECONDS,
) -> dict[str, Any]:
    """Atomically claim the oldest effective queued job and emit its exact prompt."""

    worker = _text(worker_id, "worker_id")
    if lease_seconds <= 0:
        raise CreatorAudienceQueueError("lease_seconds must be positive")
    claimed_at = _timestamp(now)
    claimed_dt = _parse_timestamp(claimed_at, "claimed_at")
    prompt_out.parent.mkdir(parents=True, exist_ok=True)
    if prompt_out.exists():
        raise CreatorAudienceQueueError(f"prompt output already exists: {prompt_out}")

    for _attempt in range(32):
        projection = load_creator_audience_queue(data_root, now=claimed_at)
        queued = [row for row in projection["jobs"] if row["state"] == "queued"]
        if not queued:
            return {"status": "empty", "counts": projection["counts"]}
        row = queued[0]
        generation = int(row["claim_generation"]) + 1
        job_id = str(row["job_id"])
        raw_anchor = str(row["raw_anchor"])
        lease_key = f"{job_id}\0{generation}\0{worker}\0{claimed_at}".encode("utf-8")
        lease_id = "cajl_" + hashlib.sha256(lease_key).hexdigest()[:24]
        record_id = f"{job_id}_claim_{generation:04d}"
        claim = {
            "schema_version": CLAIM_SCHEMA_VERSION,
            "record_id": record_id,
            "job_id": job_id,
            "raw_anchor": raw_anchor,
            "claim_generation": generation,
            "lease_id": lease_id,
            "worker_id": worker,
            "claimed_at": claimed_at,
            "lease_expires_at": _render_timestamp(
                claimed_dt + timedelta(seconds=lease_seconds)
            ),
        }
        try:
            data_root.append_record(
                subtree="derived",
                raw_anchor=raw_anchor,
                lane=CLAIM_LANE,
                record_id=record_id,
                data=canonical_record_bytes(claim),
            )
        except DataLakeRootError:
            continue
        prompt_bytes = _decoded_bytes(
            row["_job_record"], "prompt_bytes_b64", "prompt_sha256"
        )
        prompt_out.write_bytes(prompt_bytes)
        return {
            "status": "claimed",
            "job_id": job_id,
            "lease_id": lease_id,
            "worker_id": worker,
            "claim_generation": generation,
            "lease_expires_at": claim["lease_expires_at"],
            "prompt_out": str(prompt_out),
            "prompt_sha256": row["_job_record"]["prompt_sha256"],
            "bundle_hash": row["bundle_hash"],
            "raw_anchor": raw_anchor,
            "profile_subject_id": row["profile_subject_id"],
        }
    raise CreatorAudienceQueueError("could not acquire a queue claim after concurrent writers")


def require_active_claim(
    *,
    data_root: DataLakeRoot,
    job_id: str,
    lease_id: str,
    now: str | None = None,
) -> dict[str, Any]:
    projection = load_creator_audience_queue(data_root, now=now)
    matches = [row for row in projection["jobs"] if row["job_id"] == job_id]
    if len(matches) != 1:
        raise CreatorAudienceQueueError(f"unknown queue job: {job_id}")
    row = matches[0]
    active = row.get("active_lease")
    if row["state"] != "running" or not isinstance(active, Mapping):
        raise CreatorAudienceQueueError(f"queue job is not actively leased: {job_id}")
    if active.get("lease_id") != lease_id:
        raise CreatorAudienceQueueError("queue lease does not own the job")
    return row


def materialize_claim_bundle(job: Mapping[str, Any], target: Path) -> Path:
    record = job.get("_job_record")
    if not isinstance(record, Mapping):
        raise CreatorAudienceQueueError("queue projection omits its internal job record")
    payload = _decoded_bytes(record, "bundle_bytes_b64", "bundle_sha256")
    if target.exists():
        if target.read_bytes() != payload:
            raise CreatorAudienceQueueError(f"bundle output differs: {target}")
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    return target


def write_creator_audience_terminal(
    *,
    data_root: DataLakeRoot,
    job_id: str,
    lease_id: str,
    status: str,
    details: Mapping[str, Any],
    completed_at: str | None = None,
) -> dict[str, Any]:
    if status not in {"succeeded", "blocked"}:
        raise CreatorAudienceQueueError("terminal status must be succeeded or blocked")
    at = _timestamp(completed_at)
    job = require_active_claim(
        data_root=data_root, job_id=job_id, lease_id=lease_id, now=at
    )
    semantic = {
        "schema_version": TERMINAL_SCHEMA_VERSION,
        "record_id": job_id,
        "job_id": job_id,
        "raw_anchor": job["raw_anchor"],
        "lease_id": lease_id,
        "status": status,
        "details": dict(details),
    }
    record = {**semantic, "completed_at": at}
    target = data_root.record_path(
        subtree="derived",
        raw_anchor=str(job["raw_anchor"]),
        lane=TERMINAL_LANE,
        record_id=job_id,
    )
    if target.exists():
        existing = _load_object(target)
        if {key: value for key, value in existing.items() if key != "completed_at"} != semantic:
            raise CreatorAudienceQueueError("queue job already has a different terminal record")
        return existing
    data_root.append_record(
        subtree="derived",
        raw_anchor=str(job["raw_anchor"]),
        lane=TERMINAL_LANE,
        record_id=job_id,
        data=canonical_record_bytes(record),
    )
    return record


def _verify_bundle_content_hash(bundle: Mapping[str, Any]) -> None:
    core = {key: value for key, value in bundle.items() if key not in _BUNDLE_DERIVED_KEYS}
    expected = "sha256:" + hashlib.sha256(_compact_json(core)).hexdigest()
    if bundle.get("bundle_hash") != expected:
        raise CreatorAudienceQueueError("bundle_hash does not close over bundle content")


def _compact_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _records(data_root: DataLakeRoot, lane: str, schema: str) -> list[dict[str, Any]]:
    root = data_root.path / "derived"
    paths = sorted(root.glob(f"*/*/{lane}/*")) if root.is_dir() else []
    rows: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            continue
        row = _load_object(path)
        if row.get("schema_version") != schema:
            raise CreatorAudienceQueueError(f"unsupported queue record schema: {path}")
        if path.name != row.get("record_id"):
            raise CreatorAudienceQueueError(f"queue record id/path mismatch: {path}")
        if path.parent.parent.name != row.get("raw_anchor"):
            raise CreatorAudienceQueueError(f"queue raw_anchor/path mismatch: {path}")
        rows.append(row)
    return rows


def _unique_records(
    data_root: DataLakeRoot, lane: str, schema: str, key: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in _records(data_root, lane, schema):
        identity = _text(row.get(key), f"{lane} {key}")
        if identity in result:
            raise CreatorAudienceQueueError(f"multiple {lane} records for {identity}")
        result[identity] = row
    return result


def _validate_claim(claim: Mapping[str, Any], job: Mapping[str, Any]) -> None:
    generation = claim.get("claim_generation")
    if type(generation) is not int or generation < 1:
        raise CreatorAudienceQueueError("claim_generation must be a positive integer")
    expected_id = f"{job['job_id']}_claim_{generation:04d}"
    if claim.get("record_id") != expected_id or claim.get("raw_anchor") != job.get("raw_anchor"):
        raise CreatorAudienceQueueError("claim identity does not match its job")
    _text(claim.get("lease_id"), "lease_id")
    _text(claim.get("worker_id"), "worker_id")
    claimed = _parse_timestamp(str(claim.get("claimed_at")), "claimed_at")
    expires = _parse_timestamp(str(claim.get("lease_expires_at")), "lease_expires_at")
    if expires <= claimed:
        raise CreatorAudienceQueueError("claim lease must expire after it is acquired")


def _validate_job(job_id: str, job: Mapping[str, Any]) -> None:
    bundle_hash = _text(job.get("bundle_hash"), "bundle_hash")
    expected_id = "cajq_" + hashlib.sha256(bundle_hash.encode("utf-8")).hexdigest()[:24]
    if job_id != expected_id or job.get("record_id") != expected_id:
        raise CreatorAudienceQueueError("queue job id does not match its bundle hash")
    if job.get("platform") != "tiktok":
        raise CreatorAudienceQueueError("queue job platform must be tiktok")
    _parse_timestamp(str(job.get("enqueued_at")), "enqueued_at")
    bundle_bytes = _decoded_bytes(job, "bundle_bytes_b64", "bundle_sha256")
    prompt_bytes = _decoded_bytes(job, "prompt_bytes_b64", "prompt_sha256")
    try:
        bundle = json.loads(bundle_bytes.decode("utf-8-sig"))
        prompt = prompt_bytes.decode("utf-8")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CreatorAudienceQueueError("queue job transport is not valid UTF-8") from exc
    if not isinstance(bundle, Mapping) or not prompt.strip():
        raise CreatorAudienceQueueError("queue job transport is incomplete")
    _verify_bundle_content_hash(bundle)
    for field in ("raw_anchor", "creator_id", "profile_subject_id", "bundle_id", "bundle_hash"):
        if job.get(field) != bundle.get(field):
            raise CreatorAudienceQueueError(
                f"queue job {field} does not match its stored bundle"
            )


def _validate_claim_chain(job_id: str, claims: list[dict[str, Any]]) -> None:
    for index, claim in enumerate(claims, start=1):
        if claim["claim_generation"] != index:
            raise CreatorAudienceQueueError(f"claim generations are not contiguous: {job_id}")
        if index > 1:
            prior = claims[index - 2]
            if _parse_timestamp(str(claim["claimed_at"]), "claimed_at") < _parse_timestamp(
                str(prior["lease_expires_at"]), "prior lease expiry"
            ):
                raise CreatorAudienceQueueError(
                    f"job was reclaimed before its prior lease expired: {job_id}"
                )


def _validate_terminal(
    terminal: Mapping[str, Any],
    job: Mapping[str, Any],
    claims: list[dict[str, Any]],
) -> None:
    if terminal.get("record_id") != job.get("job_id") or terminal.get("raw_anchor") != job.get("raw_anchor"):
        raise CreatorAudienceQueueError("terminal identity does not match its job")
    if terminal.get("status") not in {"succeeded", "blocked"}:
        raise CreatorAudienceQueueError("unsupported queue terminal status")
    if not isinstance(terminal.get("details"), Mapping):
        raise CreatorAudienceQueueError("queue terminal details must be an object")
    completed = _parse_timestamp(str(terminal.get("completed_at")), "completed_at")
    matching = [claim for claim in claims if claim.get("lease_id") == terminal.get("lease_id")]
    if len(matching) != 1:
        raise CreatorAudienceQueueError("queue terminal does not name exactly one claim")
    claim = matching[0]
    if completed < _parse_timestamp(str(claim["claimed_at"]), "claimed_at") or completed >= _parse_timestamp(
        str(claim["lease_expires_at"]), "lease_expires_at"
    ):
        raise CreatorAudienceQueueError("queue terminal was not written during its lease")


def _verify_enqueue_replay(existing: Mapping[str, Any], semantic: Mapping[str, Any]) -> None:
    if {key: value for key, value in existing.items() if key != "enqueued_at"} != semantic:
        raise CreatorAudienceQueueError("bundle_hash already identifies different queue bytes")
    _parse_timestamp(str(existing.get("enqueued_at")), "enqueued_at")


def _enqueue_result(record: Mapping[str, Any], status: str) -> dict[str, Any]:
    return {
        "status": status,
        "job_id": record["job_id"],
        "raw_anchor": record["raw_anchor"],
        "profile_subject_id": record["profile_subject_id"],
        "bundle_id": record["bundle_id"],
        "bundle_hash": record["bundle_hash"],
        "prompt_sha256": record["prompt_sha256"],
        "queue_state": "queued",
    }


def _decoded_bytes(record: Mapping[str, Any], body_key: str, hash_key: str) -> bytes:
    try:
        payload = base64.b64decode(_text(record.get(body_key), body_key), validate=True)
    except (ValueError, binascii.Error) as exc:
        raise CreatorAudienceQueueError(f"invalid {body_key}") from exc
    if _sha256(payload) != record.get(hash_key):
        raise CreatorAudienceQueueError(f"{body_key} does not match {hash_key}")
    return payload


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CreatorAudienceQueueError(f"queue record is unreadable: {path}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise CreatorAudienceQueueError(f"queue record must be an object: {path}")
    return dict(value)


def _text(value: Any, role: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CreatorAudienceQueueError(f"{role} must be nonblank text")
    return value.strip()


def _sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _timestamp(value: str | None) -> str:
    if value is None:
        return _render_timestamp(datetime.now(UTC))
    parsed = _parse_timestamp(value, "timestamp")
    return _render_timestamp(parsed)


def _parse_timestamp(value: str, role: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CreatorAudienceQueueError(f"{role} must be an RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise CreatorAudienceQueueError(f"{role} must include a timezone")
    return parsed.astimezone(UTC)


def _render_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


__all__ = [
    "CLAIM_LANE",
    "DEFAULT_CAPACITY",
    "DEFAULT_LEASE_SECONDS",
    "JOB_LANE",
    "TERMINAL_LANE",
    "CreatorAudienceQueueError",
    "assert_creator_audience_capacity",
    "claim_creator_audience_job",
    "enqueue_creator_audience_job",
    "load_creator_audience_queue",
    "materialize_claim_bundle",
    "public_queue_view",
    "require_active_claim",
    "unfinished_profile_subject_ids",
    "write_creator_audience_terminal",
]
