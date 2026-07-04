from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

from harness_utils import hash_file
from source_capture.models import CaptureModeCategory, known_fact
from source_capture.reddit_consolidation import RedditConsolidationFailure, consolidate_reddit_packet
from source_capture.writer import write_local_source_capture_packet


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_consolidation_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_consolidates_old_reddit_thread_to_flat_comments_without_mutating_packet(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, NORMAL_THREAD_HTML)
    output_dir = scratch_dir / "derived"
    before = _packet_file_hashes(packet_dir)

    result = consolidate_reddit_packet(
        packet_or_manifest_path=packet_dir,
        output_directory=output_dir,
    )

    after = _packet_file_hashes(packet_dir)
    assert after == before
    assert Path(result["json_path"]).parent == output_dir
    assert Path(result["receipt_path"]).parent == output_dir

    artifact = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    data = artifact["reddit_thread_consolidation"]
    assert data["thread"]["title"] == "Durable Reddit packet spine"
    assert data["thread"]["subreddit"] == "orca_test"
    assert data["post"]["body_text"] == "Original post body"
    assert data["counts"]["observable_comment_nodes"] == 2
    assert data["counts"]["comments_parsed"] == 2
    assert data["comments"][0]["comment_id"] == "c1"
    assert data["comments"][1]["parent_id"] == "c1"
    assert data["comments"][1]["depth"] == 1
    assert data["comments"][0]["provenance"]["raw_html_file_id"] == "file_01"
    assert "not live Reddit capture" in data["non_claims"]

    receipt = Path(result["receipt_path"]).read_text(encoding="utf-8")
    assert "Comments parsed: 2" in receipt
    assert "Observable comment nodes: 2" in receipt


def test_deleted_removed_and_collapsed_postures_travel_as_closed_states(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, POSTURE_THREAD_HTML)
    result = consolidate_reddit_packet(
        packet_or_manifest_path=packet_dir,
        output_directory=scratch_dir / "derived",
    )

    artifact = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    comments = artifact["reddit_thread_consolidation"]["comments"]

    assert [comment["comment_posture"] for comment in comments] == ["deleted", "removed", "collapsed"]
    assert comments[2]["parser_warnings"] == ["comment body carried as collapsed"]
    assert artifact["reddit_thread_consolidation"]["counts"]["comment_postures"] == {
        "collapsed": 1,
        "deleted": 1,
        "removed": 1,
    }


def test_visible_comment_is_not_tainted_by_removed_or_deleted_child(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, VISIBLE_PARENT_WITH_REMOVED_CHILD_HTML)
    result = consolidate_reddit_packet(
        packet_or_manifest_path=packet_dir,
        output_directory=scratch_dir / "derived",
    )

    artifact = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    data = artifact["reddit_thread_consolidation"]
    comments = data["comments"]

    assert [comment["comment_id"] for comment in comments] == ["parent", "removed_child"]
    assert comments[0]["comment_posture"] == "present"
    assert comments[0]["body_text"] == "Visible parent body"
    assert comments[0]["parser_warnings"] == []
    assert comments[1]["comment_posture"] == "removed"
    assert data["counts"]["comment_postures"] == {
        "present": 1,
        "removed": 1,
    }


def test_media_only_comment_is_not_missing_dom(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, MEDIA_ONLY_COMMENT_THREAD_HTML)
    result = consolidate_reddit_packet(
        packet_or_manifest_path=packet_dir,
        output_directory=scratch_dir / "derived",
    )

    artifact = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    data = artifact["reddit_thread_consolidation"]

    assert data["counts"]["comment_postures"] == {"media_only": 1}
    assert data["comments"][0]["comment_id"] == "media"
    assert data["comments"][0]["body_text"] == ""
    assert data["comments"][0]["comment_posture"] == "media_only"
    assert data["comments"][0]["parser_warnings"] == [
        "observable comment body had no extractable text; non-text media may be present",
        "comment body carried as media_only",
    ]


def test_genuinely_empty_thread_is_reconciled_success(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, EMPTY_THREAD_HTML)
    result = consolidate_reddit_packet(
        packet_or_manifest_path=packet_dir,
        output_directory=scratch_dir / "derived",
    )

    artifact = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    data = artifact["reddit_thread_consolidation"]
    assert data["counts"]["observable_comment_nodes"] == 0
    assert data["counts"]["comments_parsed"] == 0
    assert data["comments"] == []


def test_observable_comment_node_without_body_travels_as_missing_dom(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, BROKEN_COMMENT_THREAD_HTML)

    result = consolidate_reddit_packet(
        packet_or_manifest_path=packet_dir,
        output_directory=scratch_dir / "derived",
    )

    artifact = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
    data = artifact["reddit_thread_consolidation"]
    assert data["counts"]["observable_comment_nodes"] == 1
    assert data["counts"]["comments_parsed"] == 1
    assert data["counts"]["comment_postures"] == {"missing_dom": 1}
    assert data["comments"][0]["comment_id"] == "unparsed"
    assert data["comments"][0]["body_text"] == ""
    assert data["comments"][0]["comment_posture"] == "missing_dom"
    assert data["comments"][0]["parser_warnings"] == [
        "observable comment node had no visible usertext body; body_text left empty",
        "comment body carried as missing_dom",
    ]


def test_contaminated_packet_refuses_before_derived_output(scratch_dir: Path) -> None:
    packet_dir = _write_packet(
        scratch_dir=scratch_dir,
        html=NORMAL_THREAD_HTML,
        source_family="reddit_thread",
        source_surface="old_reddit_html",
        source_locator="https://old.reddit.com/r/orca_test/comments/abc/durable_reddit_packet_spine/",
        capture_context="local reddit test packet leaking a session cookie: sid=abc123",
    )

    with pytest.raises(RedditConsolidationFailure) as exc_info:
        consolidate_reddit_packet(
            packet_or_manifest_path=packet_dir,
            output_directory=scratch_dir / "derived",
        )

    assert exc_info.value.code == "packet_contamination_suspected"
    assert not (scratch_dir / "derived").exists()


def test_non_reddit_packet_refuses_before_derived_output(scratch_dir: Path) -> None:
    packet_dir = _write_packet(
        scratch_dir=scratch_dir,
        html=NORMAL_THREAD_HTML,
        source_family="docs_page",
        source_surface="local_file_artifact",
        source_locator="https://example.com/docs",
    )

    with pytest.raises(RedditConsolidationFailure) as exc_info:
        consolidate_reddit_packet(
            packet_or_manifest_path=packet_dir,
            output_directory=scratch_dir / "derived",
        )

    assert exc_info.value.code == "ineligible_source_surface"
    assert not (scratch_dir / "derived").exists()


def test_hash_mismatch_refuses_before_parsing(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, NORMAL_THREAD_HTML)
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    raw_path = packet_dir / manifest["preserved_files"][0]["relative_packet_path"]
    raw_path.write_text("<html><body>tampered</body></html>", encoding="utf-8")

    with pytest.raises(RedditConsolidationFailure) as exc_info:
        consolidate_reddit_packet(
            packet_or_manifest_path=packet_dir,
            output_directory=scratch_dir / "derived",
        )

    assert exc_info.value.code == "raw_file_hash_mismatch"
    assert not (scratch_dir / "derived").exists()


def test_missing_thread_envelope_refuses_without_success_artifact(scratch_dir: Path) -> None:
    packet_dir = _write_reddit_packet(scratch_dir, "<html><body>No thread here</body></html>")

    with pytest.raises(RedditConsolidationFailure) as exc_info:
        consolidate_reddit_packet(
            packet_or_manifest_path=packet_dir,
            output_directory=scratch_dir / "derived",
        )

    assert exc_info.value.code == "required_thread_envelope_missing"
    assert not (scratch_dir / "derived").exists()


def test_runner_writes_derived_artifacts_for_existing_packet(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    packet_dir = _write_reddit_packet(scratch_dir, NORMAL_THREAD_HTML)
    output_dir = scratch_dir / "runner_derived"

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_reddit_consolidation.py",
            "--packet",
            str(packet_dir),
            "--output-dir",
            str(output_dir),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (output_dir / "reddit_thread_consolidation.json").exists()
    assert (output_dir / "reddit_thread_consolidation_receipt.md").exists()


def test_runner_writes_missing_dom_comment_for_bodyless_observable_node(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    packet_dir = _write_reddit_packet(scratch_dir, BROKEN_COMMENT_THREAD_HTML)

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_reddit_consolidation.py",
            "--packet",
            str(packet_dir),
            "--output-dir",
            str(scratch_dir / "runner_derived"),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (scratch_dir / "runner_derived" / "reddit_thread_consolidation.json").exists()
    artifact = json.loads(
        (scratch_dir / "runner_derived" / "reddit_thread_consolidation.json").read_text(
            encoding="utf-8"
        )
    )
    data = artifact["reddit_thread_consolidation"]
    assert data["counts"]["comments_parsed"] == 1
    assert data["comments"][0]["comment_posture"] == "missing_dom"


def _write_reddit_packet(scratch_dir: Path, html: str) -> Path:
    return _write_packet(
        scratch_dir=scratch_dir,
        html=html,
        source_family="reddit_thread",
        source_surface="old_reddit_html",
        source_locator="https://old.reddit.com/r/orca_test/comments/abc/durable_reddit_packet_spine/",
    )


def _write_packet(
    *,
    scratch_dir: Path,
    html: str,
    source_family: str,
    source_surface: str,
    source_locator: str,
    capture_context: str = "local test packet over already-preserved old-Reddit-like HTML",
) -> Path:
    input_path = scratch_dir / f"thread_{uuid.uuid4().hex}.html"
    input_path.write_text(html, encoding="utf-8")
    output_dir = scratch_dir / f"packet_{uuid.uuid4().hex}"
    result = write_local_source_capture_packet(
        output_directory=output_dir,
        input_files=[input_path],
        source_family=source_family,
        source_surface=source_surface,
        source_locator=known_fact(source_locator),
        decision_question="What visible Reddit thread content is preserved in this packet?",
        capture_context=capture_context,
        capture_mode=CaptureModeCategory.AGENT_ASSISTED,
        operator_category="reddit_consolidation_test_operator",
    )
    return Path(result.output_directory)


def _packet_file_hashes(packet_dir: Path) -> dict[str, str]:
    return {
        str(path.relative_to(packet_dir)): hash_file(path)
        for path in sorted(packet_dir.rglob("*"))
        if path.is_file()
    }


NORMAL_THREAD_HTML = """\
<!doctype html>
<html>
  <body class="old-reddit">
    <div id="siteTable">
      <div class="thing link" data-fullname="t3_abc" data-subreddit="orca_test"
           data-author="poster" data-score="42"
           data-permalink="/r/orca_test/comments/abc/durable_reddit_packet_spine/">
        <a class="title" href="/r/orca_test/comments/abc/durable_reddit_packet_spine/">Durable Reddit packet spine</a>
        <time datetime="2026-06-01T00:00:00Z">1 day ago</time>
        <div class="usertext-body"><div class="md"><p>Original post body</p></div></div>
      </div>
    </div>
    <div class="sitetable nestedlisting">
      <div class="thing comment" data-fullname="t1_c1" data-parent="t3_abc" data-depth="0"
           data-author="commenter_one" data-score="5">
        <time datetime="2026-06-01T01:00:00Z">1 hour ago</time>
        <div class="usertext-body"><div class="md"><p>First comment</p></div></div>
        <div class="child">
          <div class="sitetable">
            <div class="thing comment" data-fullname="t1_c2" data-parent="t1_c1" data-depth="1"
                 data-author="commenter_two">
              <span class="score unvoted">score hidden</span>
              <div class="usertext-body"><div class="md"><p>Nested reply</p></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""


POSTURE_THREAD_HTML = """\
<html><body>
  <div class="thing link" data-fullname="t3_abc" data-subreddit="orca_test" data-author="poster">
    <a class="title">Posture thread</a>
    <div class="usertext-body"><p>Body</p></div>
  </div>
  <div class="thing comment deleted" data-fullname="t1_deleted" data-parent="t3_abc" data-author="[deleted]">
    <div class="usertext-body"><p>[deleted]</p></div>
  </div>
  <div class="thing comment removed" data-fullname="t1_removed" data-parent="t3_abc">
    <div class="usertext-body"><p>[removed]</p></div>
  </div>
  <div class="thing comment collapsed" data-fullname="t1_collapsed" data-parent="t3_abc">
    <p>collapsed comment</p>
  </div>
</body></html>
"""


VISIBLE_PARENT_WITH_REMOVED_CHILD_HTML = """\
<html><body>
  <div class="thing link" data-fullname="t3_abc" data-subreddit="orca_test" data-author="poster">
    <a class="title">Visible parent thread</a>
    <div class="usertext-body"><p>Body</p></div>
  </div>
  <div class="thing comment" data-fullname="t1_parent" data-parent="t3_abc" data-author="visible_author">
    <div class="entry">
      <div class="usertext-body"><p>Visible parent body</p></div>
    </div>
    <div class="child">
      <div class="sitetable">
        <div class="thing comment removed" data-fullname="t1_removed_child" data-parent="t1_parent">
          <div class="usertext-body"><p>[removed]</p></div>
        </div>
      </div>
    </div>
  </div>
</body></html>
"""


MEDIA_ONLY_COMMENT_THREAD_HTML = """\
<html><body>
  <div class="thing link" data-fullname="t3_media" data-subreddit="orca_test" data-author="poster">
    <a class="title">Media thread</a>
    <div class="usertext-body"><p>Body</p></div>
  </div>
  <div class="thing comment" data-fullname="t1_media" data-parent="t3_media" data-author="media_author">
    <div class="usertext-body"><div class="md"><p><a href="https://example.com/gif"><img src="media.gif"></a></p></div></div>
  </div>
</body></html>
"""


EMPTY_THREAD_HTML = """\
<html><body>
  <div class="thing link" data-fullname="t3_empty" data-subreddit="orca_test" data-author="poster">
    <a class="title">Empty thread</a>
    <div class="usertext-body"><p>Body</p></div>
  </div>
</body></html>
"""


BROKEN_COMMENT_THREAD_HTML = """\
<html><body>
  <div class="thing link" data-fullname="t3_broken" data-subreddit="orca_test" data-author="poster">
    <a class="title">Broken thread</a>
    <div class="usertext-body"><p>Body</p></div>
  </div>
  <div class="thing comment" data-fullname="t1_unparsed" data-parent="t3_broken"></div>
</body></html>
"""
