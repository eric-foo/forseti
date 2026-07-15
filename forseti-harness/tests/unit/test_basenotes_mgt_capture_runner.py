from __future__ import annotations

import base64
import json
from pathlib import Path

import pytest

from cleaning.basenotes_lake import derive_basenotes_cleaning_into_lake
from data_lake.root import DataLakeRoot
from data_lake.silver_record import verify_silver_vault_record_sources
from runners import run_basenotes_mgt_capture as runner
from source_capture.adapters.browser_snapshot import BrowserPageObservationSuccess
from source_capture.basenotes_projection import project_basenotes_into_lake


_URL = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)
_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def test_preflight_names_real_dependencies(tmp_path: Path) -> None:
    bundle = _write_bundle(tmp_path)

    message = runner.preflight_basenotes_mgt_capture(
        url=_URL,
        bundle_directory=bundle,
        output_root=tmp_path / "output",
    )

    assert "user-visible persistent Chrome" in message
    assert "user-cleared access gate" in message
    assert "no cookie, credential, browser-profile, or proxy export" in message
    assert "no network capture attempted" in message


def test_runner_writes_packet_and_proves_projection_cleaning_silver_sources(
    tmp_path: Path,
) -> None:
    bundle = _write_bundle(tmp_path)
    root = DataLakeRoot.for_test(tmp_path / "lake")
    output_root = tmp_path / "output"

    exit_code, summary_message = runner.run_basenotes_mgt_capture(
        url=_URL,
        bundle_directory=bundle,
        output_root=output_root,
        data_root=root,
    )

    assert exit_code == 0
    summary = json.loads(Path(summary_message).read_text(encoding="utf-8"))
    role = summary["packet_roles"][runner.PERSISTENT_CHROME_SLOT]
    assert summary["capture_profile"] == runner.CAPTURE_PROFILE
    assert role["source_family"] == runner.SOURCE_FAMILY
    assert role["source_surface"] == runner.PERSISTENT_CHROME_SURFACE
    assert summary["capture_parameters"]["persistent_user_session"] is True
    assert summary["capture_parameters"]["cookies_or_credentials_exported"] is False

    packet_id = role["packet_id"]
    loaded = root.load_raw_packet(packet_id)
    assert loaded.manifest["source_surface"] == runner.PERSISTENT_CHROME_SURFACE
    assert len(loaded.manifest["preserved_files"]) == 4
    assert set(loaded.bodies) == {"file_01", "file_02", "file_03", "file_04"}

    projection, projection_path = project_basenotes_into_lake(
        data_root=root,
        packet_id=packet_id,
    )
    cleaning = derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id)

    assert projection_path.is_file()
    assert projection.loss_ledger.preserved_review_cards == 6
    assert cleaning.audit_path.is_file()
    assert len(cleaning.silver_paths) == 6
    for silver_path in cleaning.silver_paths:
        silver_record = json.loads(silver_path.read_text(encoding="utf-8"))
        verify_silver_vault_record_sources(root, silver_record, record_path=silver_path)


def test_direct_cdp_writes_packet_projection_cleaning_and_six_verified_silver(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    engine = _FakeCdpEngine()
    exit_code, summary_path = runner.run_basenotes_mgt_capture(
        url=_URL,
        bundle_directory=tmp_path / "cdp-bundle",
        output_root=tmp_path / "output",
        data_root=root,
        cdp_endpoint=runner.DEFAULT_CDP_ENDPOINT,
        cdp_engine=engine,
    )
    assert exit_code == 0
    assert engine.closed is True
    assert engine.capture_kwargs["proxy_profile"] is None
    assert engine.capture_kwargs["storage_state_path"] is None
    assert engine.capture_kwargs["headless"] is False
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    assert summary["capture_parameters"]["capture_transport"] == "existing_chrome_cdp_loopback"
    assert summary["capture_parameters"]["human_cleared_access_gate"] is False
    assert summary["capture_parameters"]["access_readiness_basis"] == (
        "observed_exact_url_challenge_free_sufficient_content"
    )
    packet_id = summary["packet_roles"][runner.PERSISTENT_CHROME_SLOT]["packet_id"]
    projection, projection_path = project_basenotes_into_lake(data_root=root, packet_id=packet_id)
    cleaning = derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id)
    assert projection_path.is_file()
    assert projection.loss_ledger.preserved_review_cards == 6
    assert cleaning.audit_path.is_file()
    assert len(cleaning.silver_paths) == 6
    for silver_path in cleaning.silver_paths:
        verify_silver_vault_record_sources(
            root,
            json.loads(silver_path.read_text(encoding="utf-8")),
            record_path=silver_path,
        )


def test_direct_cdp_observes_access_without_manual_readiness_confirmation(tmp_path: Path) -> None:
    engine = _FakeCdpEngine()
    bundle = runner.capture_basenotes_bundle_via_cdp(
        url=_URL,
        bundle_directory=tmp_path / "bundle",
        cdp_endpoint=runner.DEFAULT_CDP_ENDPOINT,
        engine=engine,
    )
    metadata = json.loads((bundle / "browser_snapshot_metadata.json").read_text(encoding="utf-8"))
    assert engine.capture_kwargs
    assert metadata["human_cleared_access_gate"] is False
    assert metadata["access_readiness_basis"] == (
        "observed_exact_url_challenge_free_sufficient_content"
    )
    assert "--human-access-ready" not in runner._build_parser().format_help()


@pytest.mark.parametrize("endpoint", ["https://example.com:9222", "http://user@127.0.0.1:9222"])
def test_direct_cdp_rejects_invalid_endpoint_before_capture(tmp_path: Path, endpoint: str) -> None:
    engine = _FakeCdpEngine()
    with pytest.raises(ValueError, match="credential-free loopback"):
        runner.capture_basenotes_bundle_via_cdp(
            url=_URL,
            bundle_directory=tmp_path / "bundle",
            cdp_endpoint=endpoint,
            engine=engine,
        )
    assert engine.capture_kwargs == {}
    assert not (tmp_path / "bundle").exists()


@pytest.mark.parametrize("visible_text", [
    "Performing security verification. This website verifies you are not a bot. " * 12,
    "too short",
])
def test_direct_cdp_rejects_challenge_or_insufficient_content_before_bytes(
    tmp_path: Path, visible_text: str
) -> None:
    engine = _FakeCdpEngine(visible_text=visible_text, screenshot_must_not_run=True)
    with pytest.raises(ValueError, match="source-detail sufficiency"):
        runner.capture_basenotes_bundle_via_cdp(
            url=_URL,
            bundle_directory=tmp_path / "bundle",
            cdp_endpoint=runner.DEFAULT_CDP_ENDPOINT,
            engine=engine,
        )
    assert engine.closed is True
    assert not (tmp_path / "bundle").exists()


@pytest.mark.parametrize(
    ("engine_kwargs", "message"),
    [
        ({"final_url": "https://basenotes.com/fragrances/other.1"}, "final_url"),
        ({"screenshot": b"\xff\xd8\xffnot-png"}, "genuine PNG"),
    ],
)
def test_direct_cdp_rejects_wrong_final_url_or_non_png_before_bytes(
    tmp_path: Path, engine_kwargs: dict[str, object], message: str
) -> None:
    engine = _FakeCdpEngine(**engine_kwargs)
    with pytest.raises(ValueError, match=message):
        runner.capture_basenotes_bundle_via_cdp(
            url=_URL,
            bundle_directory=tmp_path / "bundle",
            cdp_endpoint=runner.DEFAULT_CDP_ENDPOINT,
            engine=engine,
        )
    assert not (tmp_path / "bundle").exists()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("headless", True),
        ("persistent_user_session", False),
        ("human_cleared_access_gate", False),
        ("cookies_exported", True),
        ("credentials_exported", True),
        ("proxy_used", True),
    ],
)
def test_runner_rejects_wrong_route_metadata(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    bundle = _write_bundle(tmp_path, metadata_override={field: value})

    with pytest.raises(ValueError, match=field):
        runner.run_basenotes_mgt_capture(
            url=_URL,
            bundle_directory=bundle,
            output_root=tmp_path / "output",
        )

    assert not (tmp_path / "output").exists()


def test_runner_rejects_challenge_only_before_packet_publication(tmp_path: Path) -> None:
    challenge = (
        "Performing security verification. This website verifies you are not a bot. " * 12
    )
    bundle = _write_bundle(
        tmp_path,
        visible_text=challenge,
        metadata_override={"title": "Just a moment..."},
    )

    with pytest.raises(ValueError, match="access blocked"):
        runner.run_basenotes_mgt_capture(
            url=_URL,
            bundle_directory=bundle,
            output_root=tmp_path / "output",
        )

    assert not (tmp_path / "output").exists()


def test_runner_rejects_missing_or_unexpected_bundle_artifacts(tmp_path: Path) -> None:
    bundle = _write_bundle(tmp_path)
    (bundle / "browser_visible_text.txt").unlink()
    (bundle / "cookies.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="exactly the four public-page artifacts"):
        runner.preflight_basenotes_mgt_capture(
            url=_URL,
            bundle_directory=bundle,
            output_root=tmp_path / "output",
        )


def test_runner_rejects_missing_caller_bound_product_identity(tmp_path: Path) -> None:
    html = _FIXTURE.read_text(encoding="utf-8").replace(
        "fragrances/mojave-ghost-by-byredo.26143979",
        "fragrances/a-different-product.99999999",
    )
    bundle = _write_bundle(tmp_path, html=html)

    with pytest.raises(ValueError, match="missing rendered DOM regex"):
        runner.run_basenotes_mgt_capture(
            url=_URL,
            bundle_directory=bundle,
            output_root=tmp_path / "output",
        )


def _write_bundle(
    tmp_path: Path,
    *,
    html: str | None = None,
    visible_text: str | None = None,
    metadata_override: dict[str, object] | None = None,
) -> Path:
    bundle = tmp_path / "persistent-chrome-bundle"
    bundle.mkdir()
    rendered_dom = _FIXTURE.read_text(encoding="utf-8") if html is None else html
    text = (
        "Mojave Ghost by Byredo public product page with source-visible community reviews. " * 12
        if visible_text is None
        else visible_text
    )
    metadata: dict[str, object] = {
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
    }
    metadata.update(metadata_override or {})
    (bundle / "browser_rendered_dom.html").write_text(rendered_dom, encoding="utf-8")
    (bundle / "browser_visible_text.txt").write_text(text, encoding="utf-8")
    (bundle / "browser_viewport_screenshot.png").write_bytes(_PNG)
    (bundle / "browser_snapshot_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    return bundle


class _FakeCdpEngine:
    def __init__(
        self,
        *,
        visible_text: str | None = None,
        screenshot: bytes = _PNG,
        screenshot_must_not_run: bool = False,
        final_url: str = _URL,
    ) -> None:
        self.visible_text = visible_text or (
            "Mojave Ghost by Byredo public product page with source-visible community reviews. "
            * 12
        )
        self.screenshot = screenshot
        self.screenshot_must_not_run = screenshot_must_not_run
        self.final_url = final_url
        self.capture_kwargs: dict[str, object] = {}
        self.closed = False

    def capture_page_observation(self, **kwargs: object) -> BrowserPageObservationSuccess:
        self.capture_kwargs = dict(kwargs)
        return BrowserPageObservationSuccess(
            requested_url=_URL,
            final_url=self.final_url,
            title="Mojave Ghost by Byredo– Basenotes",
            visible_text=self.visible_text,
            dom_observation=_FIXTURE.read_text(encoding="utf-8"),
            responses=[],
            metadata={"capture_timestamp": "2026-07-15T17:50:00Z"},
            warning_notes=[],
            limitation_notes=[],
        )

    def capture_current_viewport_png(self, *, timeout_seconds: float) -> bytes:
        assert timeout_seconds > 0
        if self.screenshot_must_not_run:
            raise AssertionError("screenshot must not run for insufficient content")
        return self.screenshot

    def close(self) -> None:
        self.closed = True
