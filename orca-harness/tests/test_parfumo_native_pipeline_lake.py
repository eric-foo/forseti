from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning import CleaningPacket
from cleaning.parfumo_lake import (
    CLEANING_AUDIT_PACK_SCHEMA_VERSION,
    DISCRIMINATOR_LOCALITY_NON_CLAIM,
    PARFUMO_CLEANING_AUDIT_LANE,
    PARFUMO_CLEANING_SILVER_LANE,
    derive_parfumo_cleaning_into_lake,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from runners.run_parfumo_mgt_capture import (
    TARGETED_RENDERED_SLOT,
    TARGETED_RENDERED_SURFACE,
    run_parfumo_targeted_rendered_capture,
)
from source_capture.models import known_fact
from source_capture.parfumo_projection import (
    PARFUMO_PROJECTION_CERTIFICATION,
    PROJECTION_PARFUMO_LANE,
    project_parfumo_into_lake,
)
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
_REVIEW_TEXT = "This perfume died young."
_STATEMENT_TEXT = "Airy amber trail."


def test_parfumo_projection_and_cleaning_persist_distinct_lake_layers(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    projection, projection_path = project_parfumo_into_lake(data_root=root, packet_id=packet_id)
    result = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)

    derived_root = root.path / "derived" / raw_shard(packet_id) / packet_id
    assert projection_path.parent == derived_root / PROJECTION_PARFUMO_LANE
    assert result.audit_path.parent == derived_root / PARFUMO_CLEANING_AUDIT_LANE
    assert result.silver_paths
    assert all(path.parent == derived_root / PARFUMO_CLEANING_SILVER_LANE for path in result.silver_paths)

    raw_html = _raw_html_body(root, packet_id)
    assert f"<p data-role=\"review-text\">{_REVIEW_TEXT}</p>" in raw_html
    assert f"<p data-role=\"statement-text\">{_STATEMENT_TEXT}</p>" in raw_html

    projection_record = json.loads(projection_path.read_text(encoding="utf-8"))
    assert projection_record["certification"] == PARFUMO_PROJECTION_CERTIFICATION
    assert projection.loss_ledger.preserved_review_cards == 1
    assert projection.loss_ledger.preserved_statements == 1

    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    assert audit["schema_version"] == CLEANING_AUDIT_PACK_SCHEMA_VERSION
    assert audit["record_family"] == "processing_audit"
    assert "record_kind" not in audit
    assert audit["raw_anchor"] == packet_id
    assert audit["lane_namespace"] == PARFUMO_CLEANING_AUDIT_LANE
    assert audit["content_hash"] == f"sha256:{_content_hash(audit)}"
    assert "not_silver_fact" in audit["non_claims"]
    assert DISCRIMINATOR_LOCALITY_NON_CLAIM in audit["non_claims"]
    assert "full_review_corpus_not_captured_ajax_pagination_present" in audit["coverage"]["residuals"]
    assert "parfumo_rating_metric_observations_deferred" not in audit["coverage"]["residuals"]
    assert "parfumo_review_rating_metric_absent_no_source_visible_numeric_rating" not in audit["coverage"]["residuals"]
    assert "not_metric_observation_promotion" not in audit["non_claims"]
    assert "inspect_raw_before_review_corpus_completeness_claim" in audit["coverage"]["raw_pull_triggers"]
    assert "cleaning_packet" in audit["payload"]

    round_tripped = CleaningPacket.model_validate(audit["payload"]["cleaning_packet"])
    assert len(round_tripped.transform_ledger) == len(result.cleaning_packet.transform_ledger)

    silver_records = [json.loads(path.read_text(encoding="utf-8")) for path in result.silver_paths]
    text_by_row_kind = {
        record["producer_row_kind"]: record
        for record in silver_records
        if record["payload_kind"] == "TextObservation"
    }
    metric_records = [record for record in silver_records if record["payload_kind"] == "MetricObservation"]
    assert set(text_by_row_kind) == {"parfumo_review_body_text", "parfumo_statement_body_text"}
    assert all(
        record["payload"]["observation"]["text_artifact_type"] == "review_body"
        for record in text_by_row_kind.values()
    )
    assert text_by_row_kind["parfumo_review_body_text"]["payload"]["observation"]["text_value"] == _REVIEW_TEXT
    assert text_by_row_kind["parfumo_statement_body_text"]["payload"]["observation"]["text_value"] == _STATEMENT_TEXT
    assert len(metric_records) == 1
    metric = metric_records[0]["payload"]["observation"]
    assert metric["metric_name"] == "review_rating"
    assert metric["metric_value"] == 8.0
    assert metric["unit"] == "parfumo_rating_0_10"
    assert metric["metric_posture"] == {
        "kind": "observed",
        "reason_code": None,
        "reason_detail": None,
    }
    for record in silver_records:
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["record_kind"] == "observation"
        assert record["payload_kind"] in {"TextObservation", "MetricObservation"}
        assert "cleaning_packet" not in record["payload"]
        assert "transform_ledger" not in json.dumps(record)
        refs = [ref for ref in record["derived_refs"] if ref["record_id"] == audit["record_id"]]
        assert len(refs) == 1
        assert refs[0]["lane_namespace"] == PARFUMO_CLEANING_AUDIT_LANE
        assert refs[0]["content_hash"] == audit["content_hash"]


def test_parfumo_targeted_rendered_packet_flows_to_projection_cleaning_and_metric_silver(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_targeted_packet(root, tmp_path)

    projection, _ = project_parfumo_into_lake(data_root=root, packet_id=packet_id)
    result = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)

    assert projection.loss_ledger.preserved_review_cards == 3
    assert projection.loss_ledger.preserved_statements == 1
    assert {row.raw_ref.slice_id for row in projection.rows} == {
        "parfumo_targeted:product_context",
        "parfumo_targeted:review_latest_recent",
        "parfumo_targeted:review_source_visible_high_rating",
        "parfumo_targeted:review_source_visible_low_rating",
        "parfumo_targeted:statement_latest_recent",
    }
    assert all(handle.source_surface == TARGETED_RENDERED_SURFACE for handle in result.cleaning_packet.handles)

    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    assert audit["source_surface"] == TARGETED_RENDERED_SURFACE
    assert "not_metric_observation_promotion" not in audit["non_claims"]

    records = [json.loads(path.read_text(encoding="utf-8")) for path in result.silver_paths]
    assert sum(1 for record in records if record["payload_kind"] == "TextObservation") == 4
    metric_values = sorted(
        record["payload"]["observation"]["metric_value"]
        for record in records
        if record["payload_kind"] == "MetricObservation"
    )
    assert metric_values == [3.0, 7.0, 9.0]
    for record in records:
        if record["payload_kind"] != "MetricObservation":
            continue
        observation = record["payload"]["observation"]
        assert observation["metric_name"] == "review_rating"
        assert observation["metric_posture"]["kind"] == "observed"
        assert observation["metric_posture"]["reason_code"] is None
        assert observation["source_surface"] == TARGETED_RENDERED_SURFACE


def test_parfumo_targeted_rendered_overlap_emits_one_metric_per_source_review(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_targeted_packet(root, tmp_path, html=_TARGETED_HTML_OVERLAP_AND_MID_BUCKET)

    projection, _ = project_parfumo_into_lake(data_root=root, packet_id=packet_id)
    result = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)

    projected_review_ids = [
        row.source_visible_fields["review_id"]
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
    ]
    assert sorted(projected_review_ids) == ["dup-001", "loss-001", "low-001"]
    assert len(projected_review_ids) == len(set(projected_review_ids))

    records = [json.loads(path.read_text(encoding="utf-8")) for path in result.silver_paths]
    metric_observations = [
        record["payload"]["observation"]
        for record in records
        if record["payload_kind"] == "MetricObservation"
    ]

    assert sorted(observation["metric_value"] for observation in metric_observations) == [
        3.0,
        7.5,
        9.0,
    ]
    metric_row_ids = [observation["subject"]["projection_row_id"] for observation in metric_observations]
    assert sum("dup-001" in row_id for row_id in metric_row_ids) == 1
    assert sum("loss-001" in row_id for row_id in metric_row_ids) == 1


def test_parfumo_projection_rederive_appends_sibling_and_explicit_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    _, first = project_parfumo_into_lake(data_root=root, packet_id=packet_id)
    _, second = project_parfumo_into_lake(data_root=root, packet_id=packet_id)

    lane_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / PROJECTION_PARFUMO_LANE
    assert first != second
    assert len(list(lane_dir.glob("*.json"))) == 2

    project_parfumo_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_parfumo_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def test_parfumo_cleaning_audit_rederive_appends_sibling_and_explicit_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    first = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)
    second = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)

    audit_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / PARFUMO_CLEANING_AUDIT_LANE
    assert first.audit_path != second.audit_path
    assert len(list(audit_dir.glob("*.json"))) == 2

    derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def _commit_targeted_packet(root: DataLakeRoot, tmp_path: Path, *, html: str | None = None) -> str:
    artifact_dir = tmp_path / "targeted_artifacts"
    artifact_dir.mkdir(parents=True)
    rendered_dom = artifact_dir / "rendered_dom.html"
    visible_text = artifact_dir / "visible_text.txt"
    route_receipt = artifact_dir / "route_receipt.json"
    screenshot = artifact_dir / "viewport.png"
    rendered_dom.write_text(html if html is not None else _TARGETED_HTML, encoding="utf-8")
    visible_text.write_text(
        "Baccarat Rouge 540 Eau de Parfum\nReviews 369\nStatements 1390\n",
        encoding="utf-8",
    )
    route_receipt.write_text(
        json.dumps(
            {
                "route": "chrome_extension_user_visible_rendered_session",
                "source_surface": TARGETED_RENDERED_SURFACE,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    screenshot.write_bytes(b"png fixture bytes")

    exit_code, message = run_parfumo_targeted_rendered_capture(
        url=_LOCATOR,
        output_root=tmp_path / "targeted_out",
        rendered_dom_path=rendered_dom,
        visible_text_path=visible_text,
        route_receipt_path=route_receipt,
        screenshot_path=screenshot,
        data_root=root,
    )
    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["packet_roles"][TARGETED_RENDERED_SLOT]["source_surface"] == (
        TARGETED_RENDERED_SURFACE
    )
    return summary["packet_roles"][TARGETED_RENDERED_SLOT]["packet_id"]


def _raw_html_body(root: DataLakeRoot, packet_id: str) -> str:
    loaded = root.load_raw_packet(packet_id)
    for body in loaded.bodies.values():
        decoded = body.decode("utf-8", errors="ignore")
        if "data-review-id" in decoded:
            return decoded
    raise AssertionError("raw packet body with Parfumo text markup not found")


def _commit_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML, encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="parfumo_product_page_direct_http",
        source_locator=known_fact(_LOCATOR),
        decision_question="test Parfumo native pipeline into lake",
        capture_context="parfumo native pipeline lake fixture",
    )
    return result.packet.packet_id


def _content_hash(record: dict[str, object]) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(
        json.dumps(
            canonical,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


_HTML = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <meta name="description" content="Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369"
        data-statement-count="1390" data-scent-rating="7.7" data-longevity-rating="8.7"
        data-sillage-rating="8.5">
    <button data-tab="reviews" data-active="true">Reviews <span>369</span></button>
    <button data-tab="statements">Statements <span>1390</span></button>
    <input type="hidden" name="h" value="7536fa6f9c01a6637a935e7717b53101">
    <script>const routes = {{reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720}};</script>
    <article data-review-id="900001" data-author="Rimazy" data-rating="8.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">{_REVIEW_TEXT}</p>
      <a href="/Users/rimazy">Read review</a>
    </article>
    <article data-statement-id="st7001" data-author="Lyra">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">{_STATEMENT_TEXT}</p>
    </article>
  </main>
</body></html>
"""


_TARGETED_HTML_OVERLAP_AND_MID_BUCKET = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-review-count="369" data-statement-count="1390">
    <script>const routes = {{reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720}};</script>
    <article data-review-id="dup-001" data-author="Rimazy" data-rating="9.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">High rating but latest source view.</p>
    </article>
    <article data-review-id="loss-001" data-author="Sol" data-rating="7.5" data-tab="high_rating">
      <time datetime="2026-06-23">06/23/26</time>
      <p data-role="review-text">Source-visible high bucket but mid numeric rating.</p>
    </article>
    <article data-review-id="low-001" data-author="Noir" data-rating="3.0" data-tab="low_rating">
      <time datetime="2026-06-20">06/20/26</time>
      <p data-role="review-text">Low source-visible bucket.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra" data-tab="statements">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""


_TARGETED_HTML = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <meta name="description" content="Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369"
        data-statement-count="1390" data-scent-rating="7.7" data-longevity-rating="8.7"
        data-sillage-rating="8.5">
    <script>const routes = {{reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720}};</script>
    <article data-review-id="latest-001" data-author="Rimazy" data-rating="7.0" data-tab="latest">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">This perfume died young.</p>
    </article>
    <article data-review-id="high-001" data-author="Sol" data-rating="9.0" data-tab="high_rating">
      <time datetime="2026-06-23">06/23/26</time>
      <p data-role="review-text">Glowing amber for hours.</p>
    </article>
    <article data-review-id="low-001" data-author="Noir" data-rating="3.0" data-tab="low_rating">
      <time datetime="2026-06-20">06/20/26</time>
      <p data-role="review-text">Too sharp on my skin.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra" data-tab="statements">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""
