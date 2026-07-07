"""Runtime reconcile-failure surfacing for the YT/IG extract runners.

The F-SH-001 adjudication residual: the consumer seam-coverage contract gate
covers the failure-channel obligation STRUCTURALLY (AST), but no runtime test
drove a corrupt manifest through the YT/IG channels after their swallowed
``except: pass`` reconciles were replaced with the shared per-packet helper.
These tests are that runtime proof. A corrupt raw manifest must:

- surface as a visible ``availability_reconcile_failed`` status in both run
  loops (never a silent omission — the rebuild deletes index entries first,
  so a swallowed failure hides healthy packets);
- flow through the IG candidates channel as a ``(None, failure)`` entry;
- raise loud in the IG pending-count scheduler gate (a no-work count is a
  valid claim only over a fully reconciled availability surface).

No transport is exercised: with an empty-but-corrupt lake, pickup yields
nothing, so the transport/provider/api_key arguments are poisoned sentinels
that fail loudly if any code path ever touches them.
"""
from __future__ import annotations

import pytest

import runners.run_ig_reels_product_extract as ig_extract
import runners.run_transcript_product_extract as yt_extract
from data_lake.root import DataLakeRoot, raw_shard
from harness_utils import generate_ulid


class _PoisonTransport:
    def __getattr__(self, name: str):  # pragma: no cover - defensive sentinel
        raise AssertionError("transport must not be touched by a reconcile-only run")


def _lake_with_corrupt_packet(tmp_path) -> DataLakeRoot:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    corrupt_pid = generate_ulid()
    corrupt_dir = root.path / "raw" / raw_shard(corrupt_pid) / corrupt_pid
    corrupt_dir.mkdir(parents=True)
    (corrupt_dir / "manifest.json").write_text("{not json", encoding="utf-8")
    return root


def test_yt_run_loop_surfaces_reconcile_failures(tmp_path) -> None:
    root = _lake_with_corrupt_packet(tmp_path)

    results = yt_extract.run_extraction(
        data_root=root,
        transport=_PoisonTransport(),
        provider="poison",
        model="poison-model",
        api_key="poison",
    )

    statuses = {entry["status"] for entry in results}
    assert statuses == {"availability_reconcile_failed"}


def test_ig_run_loop_surfaces_reconcile_failures(tmp_path) -> None:
    root = _lake_with_corrupt_packet(tmp_path)

    results = ig_extract.run_extraction(
        data_root=root,
        transport=_PoisonTransport(),
        provider="poison",
        model="poison-model",
        api_key="poison",
    )

    assert "availability_reconcile_failed" in {entry["status"] for entry in results}


def test_ig_candidates_channel_carries_reconcile_failures(tmp_path) -> None:
    root = _lake_with_corrupt_packet(tmp_path)

    candidates = ig_extract.discover_transcript_candidates(root)

    failures = [failure for transcript, failure in candidates if failure is not None]
    assert any(entry["status"] == "availability_reconcile_failed" for entry in failures)
    assert all(transcript is None for transcript, failure in candidates if failure is not None)


def test_ig_pending_count_raises_loud_on_reconcile_failure(tmp_path) -> None:
    root = _lake_with_corrupt_packet(tmp_path)

    with pytest.raises(Exception, match="availability reconcile failed"):
        ig_extract.pending_extraction_counts(data_root=root)
