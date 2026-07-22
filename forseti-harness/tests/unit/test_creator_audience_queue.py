from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from data_lake.creator_audience_queue import (
    CreatorAudienceQueueError,
    assert_creator_audience_capacity,
    claim_creator_audience_job,
    enqueue_creator_audience_job,
    load_creator_audience_queue,
    unfinished_profile_subject_ids,
    write_creator_audience_terminal,
)
from data_lake.root import DataLakeRoot


def _transport(tmp_path: Path, suffix: str = "a") -> tuple[Path, Path, dict]:
    core = {
        "schema_version": "creator_audience_evidence_bundle_v0",
        "raw_anchor": f"01QUEUE{suffix.upper()}PACKET",
        "creator_id": f"tiktok:@creator_{suffix}",
        "profile_subject_id": f"acct_tiktok_{suffix}",
        "question": "Who is the ideal audience?",
        "evidence_cutoff": "2026-07-22T00:00:00Z",
        "evidence": [{"id": suffix}],
    }
    compact = json.dumps(
        core, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    bundle_hash = "sha256:" + hashlib.sha256(compact).hexdigest()
    bundle = {
        **core,
        "bundle_hash": bundle_hash,
        "bundle_id": "caeb_" + hashlib.sha256(bundle_hash.encode()).hexdigest()[:20],
        "serialized_utf8_bytes": 0,
    }
    serialized_core = {
        key: value for key, value in bundle.items() if key != "serialized_utf8_bytes"
    }
    bundle["serialized_utf8_bytes"] = len(
        json.dumps(
            serialized_core,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    bundle_path = tmp_path / f"bundle-{suffix}.json"
    prompt_path = tmp_path / f"prompt-{suffix}.txt"
    bundle_path.write_text(json.dumps(bundle, sort_keys=True), encoding="utf-8")
    prompt_path.write_text(f"exact prompt {suffix}\n", encoding="utf-8")
    return bundle_path, prompt_path, bundle


def test_enqueue_is_bundle_hash_idempotent_and_preserves_exact_prompt(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle_path, prompt_path, _bundle = _transport(tmp_path)

    first = enqueue_creator_audience_job(
        data_root=root,
        bundle_path=bundle_path,
        prompt_path=prompt_path,
        enqueued_at="2026-07-22T00:00:00Z",
    )
    replay = enqueue_creator_audience_job(
        data_root=root,
        bundle_path=bundle_path,
        prompt_path=prompt_path,
        enqueued_at="2026-07-22T00:01:00Z",
    )
    assert first["status"] == "enqueued"
    assert replay["status"] == "already_current"
    assert replay["job_id"] == first["job_id"]

    claim = claim_creator_audience_job(
        data_root=root,
        worker_id="worker-one",
        prompt_out=tmp_path / "claimed.txt",
        now="2026-07-22T00:02:00Z",
    )
    assert claim["status"] == "claimed"
    assert (tmp_path / "claimed.txt").read_bytes() == prompt_path.read_bytes()

    prompt_path.write_text("changed prompt\n", encoding="utf-8")
    with pytest.raises(CreatorAudienceQueueError, match="different queue bytes"):
        enqueue_creator_audience_job(
            data_root=root,
            bundle_path=bundle_path,
            prompt_path=prompt_path,
        )


def test_concurrent_claim_has_one_winner_and_expired_lease_is_recoverable(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle_path, prompt_path, _bundle = _transport(tmp_path)
    enqueue_creator_audience_job(
        data_root=root,
        bundle_path=bundle_path,
        prompt_path=prompt_path,
        enqueued_at="2026-07-22T00:00:00Z",
    )

    def claim(worker: str) -> dict:
        return claim_creator_audience_job(
            data_root=root,
            worker_id=worker,
            prompt_out=tmp_path / f"{worker}.txt",
            now="2026-07-22T00:01:00Z",
            lease_seconds=60,
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(claim, ("worker-a", "worker-b")))
    assert sorted(row["status"] for row in results) == ["claimed", "empty"]

    projection = load_creator_audience_queue(root, now="2026-07-22T00:01:30Z")
    assert projection["counts"]["running"] == 1
    assert projection["counts"]["unfinished"] == 1

    reclaimed = claim_creator_audience_job(
        data_root=root,
        worker_id="worker-c",
        prompt_out=tmp_path / "worker-c.txt",
        now="2026-07-22T00:02:01Z",
        lease_seconds=60,
    )
    assert reclaimed["status"] == "claimed"
    assert reclaimed["claim_generation"] == 2

    terminal = write_creator_audience_terminal(
        data_root=root,
        job_id=reclaimed["job_id"],
        lease_id=reclaimed["lease_id"],
        status="blocked",
        details={"reason": "fixture stop"},
        completed_at="2026-07-22T00:02:30Z",
    )
    assert terminal["status"] == "blocked"
    projection = load_creator_audience_queue(root, now="2026-07-22T00:02:31Z")
    assert projection["counts"] == {
        "queued": 0,
        "running": 0,
        "succeeded": 0,
        "blocked": 1,
        "unfinished": 0,
    }


def test_capacity_counts_queued_and_running_and_pending_subjects(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    job_ids = []
    for index in range(10):
        bundle_path, prompt_path, _bundle = _transport(tmp_path, str(index))
        job = enqueue_creator_audience_job(
            data_root=root,
            bundle_path=bundle_path,
            prompt_path=prompt_path,
            enqueued_at=f"2026-07-22T00:00:{index:02d}Z",
        )
        job_ids.append(job["job_id"])
    claim = claim_creator_audience_job(
        data_root=root,
        worker_id="worker",
        prompt_out=tmp_path / "capacity-prompt.txt",
        now="2026-07-22T00:01:00Z",
    )
    assert claim["status"] == "claimed"
    with pytest.raises(CreatorAudienceQueueError, match="CAPACITY_REACHED"):
        assert_creator_audience_capacity(root, now="2026-07-22T00:01:01Z")
    pending = unfinished_profile_subject_ids(root, now="2026-07-22T00:01:01Z")
    assert pending == {f"acct_tiktok_{index}" for index in range(10)}


def test_malformed_noncontiguous_claim_chain_fails_closed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle_path, prompt_path, _bundle = _transport(tmp_path)
    job = enqueue_creator_audience_job(
        data_root=root, bundle_path=bundle_path, prompt_path=prompt_path
    )
    root.append_record(
        subtree="derived",
        raw_anchor=job["raw_anchor"],
        lane="creator_audience_onboarding_claim",
        record_id=f"{job['job_id']}_claim_0002",
        data=json.dumps(
            {
                "schema_version": "creator_audience_onboarding_claim_v1",
                "record_id": f"{job['job_id']}_claim_0002",
                "job_id": job["job_id"],
                "raw_anchor": job["raw_anchor"],
                "claim_generation": 2,
                "lease_id": "cajl_bad",
                "worker_id": "worker",
                "claimed_at": "2026-07-22T00:00:00Z",
                "lease_expires_at": "2026-07-22T00:30:00Z",
            },
            sort_keys=True,
        ).encode(),
    )
    with pytest.raises(CreatorAudienceQueueError, match="not contiguous"):
        load_creator_audience_queue(root, now="2026-07-22T00:01:00Z")


def test_corrupt_stored_transport_fails_closed_on_queue_read(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle_path, prompt_path, _bundle = _transport(tmp_path)
    job = enqueue_creator_audience_job(
        data_root=root, bundle_path=bundle_path, prompt_path=prompt_path
    )
    record_path = root.record_path(
        subtree="derived",
        raw_anchor=job["raw_anchor"],
        lane="creator_audience_onboarding_job",
        record_id=job["job_id"],
    )
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["prompt_sha256"] = "sha256:" + "0" * 64
    record_path.write_text(json.dumps(record), encoding="utf-8")

    with pytest.raises(CreatorAudienceQueueError, match="prompt_bytes_b64 does not match"):
        load_creator_audience_queue(root)
