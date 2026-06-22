from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.models import known_fact
from source_capture.retail_pdp_projection import (
    PROJECTION_RETAIL_PDP_LANE,
    build_retail_pdp_projection_from_packet_directory,
    project_retail_pdp_into_lake,
)
from source_capture.writer import write_local_source_capture_packet


# A minimal but realistic rendered PDP: an ld+json Product plus visible text.
# The projection stays valid even for sparse pages; this exercises the seam, not
# the extraction depth.
_RETAIL_HTML = """<!doctype html>
<html><head><title>Widget</title>
<script type="application/ld+json">
{"@type":"Product","name":"Widget","sku":"500","offers":{"@type":"Offer","price":"32.00","priceCurrency":"USD","availability":"http://schema.org/InStock"}}
</script></head>
<body><h1>Widget</h1><p>Based on 12 Reviews</p></body></html>
"""


def _retail_capture(root: DataLakeRoot, tmp_path: Path):
    # The preserved file keeps its .html extension (writer names it raw/01_page.html),
    # which is what the retail projection looks for.
    src = tmp_path / "page.html"
    src.write_text(_RETAIL_HTML, encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="retail",
        source_surface="example_pdp",
        source_locator=known_fact("https://example.com/products/widget"),
        decision_question="demand pressure on widget?",
        capture_context="retail pdp lake pilot",
    )


def test_projects_committed_raw_into_a_derived_record(tmp_path: Path) -> None:
    # The anchor capability: capture -> committed raw -> read by key (verified)
    # -> Silver record appended beside the raw.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _retail_capture(root, tmp_path).packet.packet_id

    projection, derived_path = project_retail_pdp_into_lake(data_root=root, packet_id=pid)

    # the Silver record landed under derived/<pid>/projection_retail_pdp/<ulid>.json
    assert derived_path.parent == root.path / "derived" / pid / PROJECTION_RETAIL_PDP_LANE
    assert derived_path.suffix == ".json"
    assert derived_path.is_file()
    assert projection.packet_id == pid

    # the lake path is byte-identical to the canonical directory projection
    container = root.find_packet(pid)
    assert container is not None
    expected = build_retail_pdp_projection_from_packet_directory(packet_directory=container)
    expected_bytes = (
        f"{json.dumps(expected.model_dump(mode='json'), indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    assert derived_path.read_bytes() == expected_bytes

    # the raw is untouched: a fresh verified read still succeeds
    assert root.load_raw_packet(pid).manifest["packet_id"] == pid


def test_re_derive_appends_a_sibling_not_overwrite(tmp_path: Path) -> None:
    # Re-derive = new sibling record (append-only), per the derived contract.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _retail_capture(root, tmp_path).packet.packet_id

    _, first = project_retail_pdp_into_lake(data_root=root, packet_id=pid)
    _, second = project_retail_pdp_into_lake(data_root=root, packet_id=pid)

    lane_dir = root.path / "derived" / pid / PROJECTION_RETAIL_PDP_LANE
    assert first != second
    assert sorted(p.name for p in lane_dir.glob("*.json")) == sorted([first.name, second.name])
    assert len(list(lane_dir.glob("*.json"))) == 2


def test_explicit_record_id_is_create_only(tmp_path: Path) -> None:
    # A fixed record id makes the append-only/create-only guard observable.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _retail_capture(root, tmp_path).packet.packet_id

    project_retail_pdp_into_lake(data_root=root, packet_id=pid, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_retail_pdp_into_lake(data_root=root, packet_id=pid, record_id="rec1")
