from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_source_capture_realchrome_cdp_packet import (
    RealChromeCDPCaptureResult,
    run_source_capture_realchrome_cdp_packet,
)
from source_capture.source_detail_sufficiency import (
    SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE,
    SourceDetailSufficiencyRequirements,
)

PDP_URL = "https://www.kohls.com/product/prd-6715879/tower-28-beauty-lipsoftie.jsp"

_CONTENT_DOM = (
    '<html><head><title>Tower 28 LipSoftie</title></head><body>'
    'Tower 28 Beauty LipSoftie $16.00 '
    '<div itemscope itemtype="http://schema.org/Offer">'
    '<meta itemprop="price" content="16"><meta itemprop="priceCurrency" content="USD"></div>'
    '</body></html>'
)
_CONTENT_TEXT = "Tower 28 Beauty LipSoftie Hydrating Tinted Lip Treatment Balm $16.00 " + ("x" * 1200)
_BLOCK_DOM = "<html><head><title>Access Denied</title></head><body>Access Denied Reference #1 errors.edgesuite.net</body></html>"
_BLOCK_TEXT = "Access Denied\nYou don't have permission to access this server.\nerrors.edgesuite.net"


class _FakeEngine:
    def __init__(self, *, dom: str, text: str, status: int, title: str) -> None:
        self._dom, self._text, self._status, self._title = dom, text, status, title
        self.calls: list[dict] = []

    def capture(self, **kwargs) -> RealChromeCDPCaptureResult:
        self.calls.append(kwargs)
        return RealChromeCDPCaptureResult(
            requested_url=kwargs["url"],
            final_url=kwargs["url"],
            title=self._title,
            rendered_dom=self._dom,
            visible_text=self._text,
            screenshot_png=b"\x89PNG\r\n\x1a\n_fake_png_bytes",
            http_status=self._status,
            warm_hop_url=kwargs.get("warm_hop_url"),
            warm_hop_blocked=True if kwargs.get("warm_hop_url") else None,
            warning_notes=[],
        )


def _read_manifest(out: Path) -> dict:
    return json.loads((out / "manifest.json").read_text(encoding="utf-8"))


def test_content_capture_writes_packet_and_passes(tmp_path: Path) -> None:
    engine = _FakeEngine(dom=_CONTENT_DOM, text=_CONTENT_TEXT, status=200, title="Tower 28 LipSoftie")
    out = tmp_path / "pkt"
    code, path = run_source_capture_realchrome_cdp_packet(
        url=PDP_URL,
        source_family="retail_pdp",
        source_surface="realchrome_cdp_snapshot",
        decision_question="q",
        output_directory=out,
        warm_hop_url="https://www.kohls.com/",
        source_detail_sufficiency_requirements=SourceDetailSufficiencyRequirements(
            require_not_access_blocked=True,
            visible_text_contains=("LipSoftie",),
            rendered_dom_regexes=(r'priceCurrency"\s+content="USD"',),
        ),
        engine=engine,
    )
    assert code == 0
    assert Path(path).resolve() == out.resolve()
    m = _read_manifest(out)
    assert m["source_surface"] == "realchrome_cdp_snapshot"
    assert m["source_family"] == "retail_pdp"
    # honest method provenance + no proxy/secret leakage
    meta_file = next(out.glob("raw/*metadata.json"))
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    assert meta["browser_engine"] == "chrome_real_via_cdp"
    assert meta["proxy_used"] is False
    assert meta["access_blocked"] is False
    assert meta["http_response_status"] == 200
    assert meta["warm_hop_url"] == "https://www.kohls.com/"
    # engine received the warm hop
    assert engine.calls[0]["warm_hop_url"] == "https://www.kohls.com/"


def test_block_is_preserved_and_fails_closed(tmp_path: Path) -> None:
    engine = _FakeEngine(dom=_BLOCK_DOM, text=_BLOCK_TEXT, status=403, title="Access Denied")
    out = tmp_path / "pkt"
    code, path = run_source_capture_realchrome_cdp_packet(
        url=PDP_URL,
        source_family="retail_pdp",
        source_surface="realchrome_cdp_snapshot",
        decision_question="q",
        output_directory=out,
        source_detail_sufficiency_requirements=SourceDetailSufficiencyRequirements(
            require_not_access_blocked=True
        ),
        engine=engine,
    )
    # packet still written to the output dir, but command fails closed on the access block
    assert code == SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert "source_detail_sufficiency_failed" in path
    m = _read_manifest(out)
    assert m["source_surface"] == "realchrome_cdp_snapshot"
    meta_file = next(out.glob("raw/*metadata.json"))
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    assert meta["access_blocked"] is True
    assert meta["access_block_reason"]


def test_requires_exactly_one_output_target(tmp_path: Path) -> None:
    engine = _FakeEngine(dom=_CONTENT_DOM, text=_CONTENT_TEXT, status=200, title="t")
    with pytest.raises(ValueError):
        run_source_capture_realchrome_cdp_packet(
            url=PDP_URL,
            source_family="retail_pdp",
            source_surface="realchrome_cdp_snapshot",
            decision_question="q",
            output_directory=None,
            data_root=None,
            engine=engine,
        )
