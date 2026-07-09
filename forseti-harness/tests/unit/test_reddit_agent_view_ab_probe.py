from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from source_capture.reddit_agent_view_ab_probe import (
    RedditAgentViewABProbeFailure,
    build_reddit_agent_view_ab_probe,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_agent_view_ab_probe_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_builds_ab_probe_pack_for_agent_view_directory(scratch_dir: Path) -> None:
    view_dir = scratch_dir / "thread_view"
    _write_thread_view_pair(view_dir)

    result = build_reddit_agent_view_ab_probe(
        view_directories=[view_dir],
        output_directory=scratch_dir / "probe",
    )

    manifest = json.loads(Path(result["manifest_path"]).read_text(encoding="utf-8"))[
        "reddit_agent_view_ab_probe"
    ]
    case = manifest["cases"][0]

    assert manifest["probe_status"] == "needs_agent_or_owner_outputs"
    assert manifest["case_count"] == 1
    assert "not agent output" in manifest["non_claims"]
    assert case["case_label"] == "thread_view"
    assert case["artifact_type"] == "reddit_thread_consolidation"
    assert case["probe_status"] == "needs_agent_or_owner_outputs"

    full_prompt = Path(case["full_prompt_path"]).read_text(encoding="utf-8")
    stripped_prompt = Path(case["stripped_prompt_path"]).read_text(encoding="utf-8")
    worksheet = Path(case["comparison_worksheet_path"]).read_text(encoding="utf-8")
    receipt = Path(result["receipt_path"]).read_text(encoding="utf-8")

    assert "Input variant: `full`" in full_prompt
    assert "Input variant: `stripped`" in stripped_prompt
    assert "Substantive claim parity" in worksheet
    assert "this worksheet does not choose the default view by itself" in worksheet
    assert "Case count: 1" in receipt


def test_refuses_when_full_and_stripped_artifact_types_do_not_match(scratch_dir: Path) -> None:
    view_dir = scratch_dir / "bad_pair"
    _write_thread_view_pair(view_dir)
    full_path = view_dir / "reddit_agent_view_full.json"
    full_path.write_text(
        json.dumps({"reddit_candidate_url_intake": {"candidate_subreddits": []}}),
        encoding="utf-8",
    )

    with pytest.raises(RedditAgentViewABProbeFailure) as excinfo:
        build_reddit_agent_view_ab_probe(
            view_directories=[view_dir],
            output_directory=scratch_dir / "probe",
        )

    assert excinfo.value.code == "artifact_type_mismatch"


def test_refuses_missing_view_directory_pair(scratch_dir: Path) -> None:
    with pytest.raises(RedditAgentViewABProbeFailure) as excinfo:
        build_reddit_agent_view_ab_probe(
            view_directories=[scratch_dir / "missing"],
            output_directory=scratch_dir / "probe",
        )

    assert excinfo.value.code == "full_missing"


def _write_thread_view_pair(view_dir: Path) -> None:
    view_dir.mkdir(parents=True)
    full = {
        "reddit_thread_consolidation": {
            "thread": {"title": "React SEO issue"},
            "post": {"body_text": "Google sees <div id=\"root\"></div>"},
            "comments": [
                {
                    "body_text": "Use SSR.",
                    "comment_posture": "present",
                    "author_state": "helper",
                }
            ],
        }
    }
    stripped = {
        "reddit_agent_view": {
            "schema_version": "reddit_agent_view_v0",
            "source_artifact_type": "reddit_thread_consolidation",
            "view_mode": "stripped_agent_context",
            "stripped_profile": "agent_context_v0",
            "stripped": {
                "thread": {"title": "React SEO issue"},
                "post": {"body_text": "Google sees <div id=\"root\"></div>"},
                "comments": [{"body_text": "Use SSR.", "comment_posture": "present"}],
            },
            "non_claims": ["not canonical artifact replacement"],
        }
    }
    (view_dir / "reddit_agent_view_full.json").write_text(json.dumps(full), encoding="utf-8")
    (view_dir / "reddit_agent_view_stripped.json").write_text(
        json.dumps(stripped),
        encoding="utf-8",
    )
