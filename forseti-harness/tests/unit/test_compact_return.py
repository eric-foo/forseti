import json

import pytest

from reports.compact_return import bounded_json, write_verified


def test_combined_unicode_output_is_bounded_without_slicing_evidence(tmp_path):
    report = {"status": "failed", "rows": [{"error": "失敗" * 300} for _ in range(20)]}
    path = write_verified(report, tmp_path / "report.json")
    text = bounded_json(report, record_path=path, facts={"status": "failed", "failed_rows": 20}, budget=1024)
    assert len(text.encode("utf-8")) <= 1024
    returned = json.loads(text)
    assert returned["return_view"] == "details_required"
    assert returned["facts"] == {"status": "failed", "failed_rows": 20}
    assert json.loads(path.read_text(encoding="utf-8")) == report


def test_fitting_return_is_complete_and_oversized_reference_fails(tmp_path):
    value = {"status": "unknown", "usage": None}
    path = write_verified(value, tmp_path / "record.json")
    assert json.loads(bounded_json(value, record_path=path, facts={})) == value
    with pytest.raises(ValueError, match="no partial return"):
        bounded_json({"large": "x" * 2000}, record_path=path, facts={"large": "x" * 2000}, budget=1024)
    with pytest.raises(FileExistsError):
        write_verified(value, path)
