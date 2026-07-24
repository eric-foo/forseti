from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

import source_capture.activity_journal as activity
from source_capture.activity_journal import (
    SourceCaptureActivityJournal,
    validate_source_capture_activity_jsonl,
)


def test_activity_journal_flushes_fsyncs_and_validates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fsync_calls: list[int] = []
    monotonic_values = iter((10.0, 10.1, 11.0, 12.0))
    monkeypatch.setattr(
        activity.os, "fsync", lambda file_descriptor: fsync_calls.append(file_descriptor)
    )
    path = tmp_path / activity.SOURCE_CAPTURE_ACTIVITY_JSONL_NAME
    journal = SourceCaptureActivityJournal(
        path,
        run_kind="creator_onboarding",
        platform="tiktok",
        monotonic_fn=lambda: next(monotonic_values),
        utc_now_fn=lambda: datetime(2026, 7, 24, tzinfo=UTC),
    )
    journal.record("phase", phase_name="select", details={"selected_count": 8})
    journal.close(
        status="complete",
        terminal_phase="close",
        error_type_or_none=None,
    )

    rows = validate_source_capture_activity_jsonl(path.read_bytes())
    assert [row["sequence"] for row in rows] == [0, 1, 2]
    assert [row["event_type"] for row in rows] == [
        "run_started",
        "phase",
        "terminal",
    ]
    assert len(fsync_calls) == 3


def test_interrupted_activity_journal_remains_line_valid_but_not_attachable(
    tmp_path: Path,
) -> None:
    path = tmp_path / activity.SOURCE_CAPTURE_ACTIVITY_JSONL_NAME
    journal = SourceCaptureActivityJournal(
        path,
        run_kind="creator_onboarding",
        platform="tiktok",
    )
    journal.record("phase", phase_name="deep_capture", details={})
    journal.close(
        status="complete",
        terminal_phase="close",
        error_type_or_none=None,
    )
    raw = b"\n".join(path.read_bytes().splitlines()[:-1]) + b"\n"
    assert all(isinstance(json.loads(line), dict) for line in raw.splitlines())
    with pytest.raises(ValueError, match="must end with terminal"):
        validate_source_capture_activity_jsonl(raw)


def test_activity_journal_rejects_raw_url_or_body_fields(tmp_path: Path) -> None:
    journal = SourceCaptureActivityJournal(
        tmp_path / activity.SOURCE_CAPTURE_ACTIVITY_JSONL_NAME,
        run_kind="creator_onboarding",
        platform="tiktok",
    )

    with pytest.raises(ValueError, match="field is forbidden"):
        journal.record(
            "phase",
            phase_name="unsafe",
            details={"raw_url": "redacted"},
        )
    journal.close(
        status="failed",
        terminal_phase="unsafe",
        error_type_or_none="ValueError",
    )
