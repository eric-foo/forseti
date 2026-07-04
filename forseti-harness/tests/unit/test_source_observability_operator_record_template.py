from __future__ import annotations

from pathlib import Path

from runners.run_source_observability_report import (
    build_source_observability_report,
    load_operator_records,
)


def test_operator_record_template_is_loadable_and_reports_limitations() -> None:
    project_root = Path(__file__).resolve().parents[2]
    template_path = project_root / "docs" / "source_observability_operator_records_template.yaml"

    records = load_operator_records(template_path)
    report = build_source_observability_report(records)

    assert [record.record_id for record in records] == [
        "EXAMPLE-FORUM-TEXT",
        "EXAMPLE-MEDIA-POINTER",
        "EXAMPLE-ACCESS-FAILURE",
    ]
    assert report["report_type"] == "source_observability_limitations_report"
    assert report["record_count"] == 3
    assert report["limitation_count"] >= 1
    assert "not source acquisition" in report["non_claims"]
