from __future__ import annotations

import hashlib

import pytest

from source_capture.sephora_browser_projection import (
    SEPHORA_BROWSER_SUBSTRATE_SCHEMA_VERSION,
    SephoraBrowserProjectionSubstrate,
)
from runners.run_sephora_pdp_browser_projection_probe import _apply_perturbation


def _payload(*, compact_dom: str = "<html>compact</html>") -> dict[str, object]:
    visible_text = "visible text"
    raw_dom = b"<html>raw</html>"
    return {
        "schemaVersion": SEPHORA_BROWSER_SUBSTRATE_SCHEMA_VERSION,
        "compactDom": compact_dom,
        "visibleText": visible_text,
        "renderedDomSha256": hashlib.sha256(raw_dom).hexdigest(),
        "renderedDomByteCount": len(raw_dom),
        "visibleTextSha256": hashlib.sha256(visible_text.encode()).hexdigest(),
        "visibleTextByteCount": len(visible_text.encode()),
        "compactDomSha256": hashlib.sha256(compact_dom.encode()).hexdigest(),
        "compactDomByteCount": len(compact_dom.encode()),
        "selectedSpanCount": 1,
        "lossCounts": {"hero|ProductHero|imageBlock|main-hero": 0},
    }


def test_browser_substrate_verifies_compact_and_raw_provenance() -> None:
    substrate = SephoraBrowserProjectionSubstrate.from_browser_payload(_payload())

    substrate.verify_raw_provenance(
        rendered_dom=b"<html>raw</html>",
        visible_text=b"visible text",
    )


def test_browser_substrate_rejects_compact_payload_hash_mismatch() -> None:
    payload = _payload()
    payload["compactDom"] = "<html>silently changed</html>"

    with pytest.raises(ValueError, match="compact DOM byte count"):
        SephoraBrowserProjectionSubstrate.from_browser_payload(payload)


def test_browser_substrate_rejects_wrong_raw_for_right_compact_payload() -> None:
    substrate = SephoraBrowserProjectionSubstrate.from_browser_payload(_payload())

    with pytest.raises(ValueError, match="raw rendered DOM byte count"):
        substrate.verify_raw_provenance(
            rendered_dom=b"<html>different raw</html>",
            visible_text=b"visible text",
        )


def test_drop_link_store_perturbation_keeps_internal_hashes_consistent() -> None:
    payload = _payload(
        compact_dom=(
            '<script id="linkStore">{"page":{"product":{"productId":"P1"}}}</script>'
            "<div>other retained evidence</div>"
        )
    )

    changed = _apply_perturbation(payload, "drop_link_store")
    substrate = SephoraBrowserProjectionSubstrate.from_browser_payload(changed)

    assert "linkStore" not in substrate.compact_dom
    assert "other retained evidence" in substrate.compact_dom
