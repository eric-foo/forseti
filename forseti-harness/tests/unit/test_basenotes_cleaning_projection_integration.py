from __future__ import annotations

import json
from pathlib import Path

from cleaning.basenotes import build_basenotes_cleaning_packet
from runners.run_basenotes_mgt_capture import (
    PERSISTENT_CHROME_SLOT,
    run_basenotes_mgt_capture,
)
from source_capture.basenotes_projection import (
    build_basenotes_projection_from_packet_directory,
)


_URL = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)


def test_basenotes_content_and_raw_packets_are_projection_and_cleaning_equivalent(
    tmp_path: Path,
) -> None:
    bundle = _write_bundle(tmp_path)
    packet_dirs: dict[str, Path] = {}
    for mode in ("raw", "content"):
        exit_code, message = run_basenotes_mgt_capture(
            url=_URL,
            bundle_directory=bundle,
            output_root=tmp_path / mode,
            capture_artifact_mode=mode,
        )
        assert exit_code == 0
        summary = json.loads(Path(message).read_text(encoding="utf-8"))
        packet_dirs[mode] = Path(
            summary["packet_roles"][PERSISTENT_CHROME_SLOT]["packet_path"]
        )

    projections = {
        mode: build_basenotes_projection_from_packet_directory(
            packet_or_manifest_path=packet_dir
        )
        for mode, packet_dir in packet_dirs.items()
    }
    semantic_rows = {
        mode: [
            row.model_dump(mode="json", exclude={"raw_ref", "raw_anchor"})
            for row in projection.rows
        ]
        for mode, projection in projections.items()
    }
    assert semantic_rows["content"] == semantic_rows["raw"]
    assert all(
        row.raw_ref.packet_id == projections["content"].packet_id
        and row.raw_anchor.anchor_kind == "json_pointer"
        and row.raw_anchor.json_pointer == f"/rows/{index}"
        for index, row in enumerate(projections["content"].rows)
    )
    assert all(
        binding.raw_ref.packet_id == projections["content"].packet_id
        and binding.raw_anchor.anchor_kind == "json_pointer"
        and binding.raw_anchor.json_pointer == f"/binding_map/{index}"
        for index, binding in enumerate(projections["content"].binding_map)
    )

    cleaning_packets = {
        mode: build_basenotes_cleaning_packet(projection)
        for mode, projection in projections.items()
    }
    assert (
        cleaning_packets["content"].transform_ledger
        == cleaning_packets["raw"].transform_ledger
    )


def _write_bundle(tmp_path: Path) -> Path:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "browser_rendered_dom.html").write_text(
        _FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (bundle / "browser_visible_text.txt").write_text(
        "Mojave Ghost by Byredo public product page with source-visible reviews. " * 12,
        encoding="utf-8",
    )
    (bundle / "browser_snapshot_metadata.json").write_text(
        json.dumps(
            {
                "capture_timestamp": "2026-07-15T17:50:00Z",
                "requested_url": _URL,
                "final_url": _URL,
                "title": "Mojave Ghost by Byredo– Basenotes",
                "browser_channel": "user_chrome_extension",
                "headless": False,
                "persistent_user_session": True,
                "human_cleared_access_gate": True,
                "cookies_exported": False,
                "credentials_exported": False,
                "proxy_used": False,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return bundle
