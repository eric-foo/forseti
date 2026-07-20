from __future__ import annotations

import json
from pathlib import Path

import pytest

from source_capture.content_qualification import (
    ContentQualificationError,
    qualify_rendered_content,
)


def _extract(dom: bytes, text: bytes, source_url: str) -> dict:
    return {
        "schema_version": "fixture_v1",
        "source_url": source_url,
        "dom": dom.decode("utf-8"),
        "text": text.decode("utf-8"),
    }


def _inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    dom = tmp_path / "rendered_dom.html"
    text = tmp_path / "visible_text.txt"
    expected = tmp_path.parent / f"{tmp_path.name}_expected.json"
    dom.write_bytes(b"<main>valuable</main>")
    text.write_bytes(b"valuable")
    expected.write_text(
        json.dumps(_extract(dom.read_bytes(), text.read_bytes(), "https://example.test/p")),
        encoding="utf-8",
    )
    return dom, text, expected


def test_match_writes_report_and_releases_only_disposable_inputs(tmp_path: Path) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    dom, text, expected = _inputs(scratch)
    report_path = scratch / "qualification_report.json"

    code, report = qualify_rendered_content(
        scratch_root=scratch,
        rendered_dom_path=dom,
        visible_text_path=text,
        expected_content_record_path=expected,
        report_path=report_path,
        extractor_version="fixture_parser_v1",
        source_url="https://example.test/p",
        extractor=_extract,
    )

    assert code == 0
    assert report["status"] == "match"
    assert not dom.exists()
    assert not text.exists()
    assert expected.exists()
    assert json.loads(report_path.read_text(encoding="utf-8")) == report


def test_drift_preserves_scratch_for_diagnosis(tmp_path: Path) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    dom, text, expected = _inputs(scratch)
    expected.write_text('{"schema_version":"different"}', encoding="utf-8")

    code, report = qualify_rendered_content(
        scratch_root=scratch,
        rendered_dom_path=dom,
        visible_text_path=text,
        expected_content_record_path=expected,
        report_path=scratch / "qualification_report.json",
        extractor_version="fixture_parser_v1",
        source_url="https://example.test/p",
        extractor=_extract,
    )

    assert code == 1
    assert report["status"] == "drift"
    assert dom.exists()
    assert text.exists()
    assert report["changed_top_level_keys"]


def test_failure_preserves_scratch_and_records_failure(tmp_path: Path) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    dom, text, expected = _inputs(scratch)

    def fail(*_args) -> dict:
        raise ValueError("fixture failure")

    code, report = qualify_rendered_content(
        scratch_root=scratch,
        rendered_dom_path=dom,
        visible_text_path=text,
        expected_content_record_path=expected,
        report_path=scratch / "qualification_report.json",
        extractor_version="fixture_parser_v1",
        source_url="https://example.test/p",
        extractor=fail,
    )

    assert code == 1
    assert report["status"] == "failure"
    assert dom.exists()
    assert text.exists()


def test_scratch_boundary_is_fail_closed(tmp_path: Path) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    outside = tmp_path / "outside.html"
    outside.write_bytes(b"x")
    text = scratch / "visible.txt"
    text.write_bytes(b"x")
    expected = tmp_path / "expected.json"
    expected.write_text("{}", encoding="utf-8")

    with pytest.raises(ContentQualificationError, match="below scratch_root"):
        qualify_rendered_content(
            scratch_root=scratch,
            rendered_dom_path=outside,
            visible_text_path=text,
            expected_content_record_path=expected,
            report_path=scratch / "report.json",
            extractor_version="fixture_parser_v1",
            source_url="https://example.test/p",
            extractor=_extract,
        )
