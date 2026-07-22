from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.amazon_delivery_location import AmazonSearchGridPlugin
from source_capture.retail_capture_profiles import get_retail_capture_profile


_US_MARKER = "<script>ue_sn = 'www.amazon.com'</script>"


def _grid_dom(
    asins: list[str],
    *,
    start: int,
    end: int,
    total: int,
    terminal: bool = False,
) -> str:
    cards = "".join(
        f'<div data-asin="{asin}" data-component-type="s-search-result"></div>'
        for asin in asins
    )
    terminal_control = (
        '<span class="s-pagination-item s-pagination-next s-pagination-disabled">Next</span>'
        if terminal
        else '<a class="s-pagination-item s-pagination-next">Next</a>'
    )
    return (
        f"<html>{_US_MARKER}<body><span>{start}-{end} of {total} results for</span>"
        f"{cards}{terminal_control}</body></html>"
    )


class _NextLocator:
    def __init__(self, page: "_GridPage") -> None:
        self.page = page
        self.first = self

    def wait_for(self, **_kwargs: Any) -> None:
        if self.page.index + 1 >= len(self.page.pages):
            raise TimeoutError("next page absent")

    def scroll_into_view_if_needed(self, **_kwargs: Any) -> None:
        self.page.scroll_events.append(self.page.index)

    def click(self, **_kwargs: Any) -> None:
        self.page.index += 1


class _GridPage:
    def __init__(self, pages: list[tuple[list[str], int, int, int, bool]]) -> None:
        self.pages = pages
        self.index = 0
        self.url_override: str | None = None
        self.scroll_events: list[int] = []

    @property
    def url(self) -> str:
        if self.url_override is not None:
            return self.url_override
        suffix = "" if self.index == 0 else f"&page={self.index + 1}"
        return f"https://www.amazon.com/s?k=Tower+28+Beauty{suffix}"

    def content(self) -> str:
        asins, start, end, total, terminal = self.pages[self.index]
        return _grid_dom(
            asins,
            start=start,
            end=end,
            total=total,
            terminal=terminal,
        )

    def locator(self, _selector: str) -> _NextLocator:
        return _NextLocator(self)

    def evaluate(self, _expression: str) -> None:
        self.scroll_events.append(self.index)

    def wait_for_timeout(self, _milliseconds: float) -> None:
        return None


def test_amazon_grid_traverses_configurable_window_and_reconciles_duplicates() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=3,
    )
    page = _GridPage(
        [
            (["B000000001", "B000000002"], 1, 2, 200, False),
            (["B000000002", "B000000003"], 3, 4, 204, False),
            (["B000000004"], 5, 5, 201, False),
        ]
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert len(plugin.grid_page_doms) == 3
    assert plugin.grid_observation["amazon_grid_requested_page_count"] == 3
    assert plugin.grid_observation["amazon_grid_captured_page_count"] == 3
    assert plugin.grid_observation["amazon_grid_extracted_placement_count"] == 5
    assert plugin.grid_observation["amazon_grid_extracted_unique_parent_count"] == 4
    assert plugin.grid_observation["amazon_grid_duplicate_placement_count"] == 1
    assert (
        plugin.grid_observation["amazon_grid_termination"]
        == "requested_page_window_reconciled"
    )


def test_amazon_grid_waits_for_the_displayed_page_range_to_populate() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=2,
    )
    page = _GridPage(
        [
            (["B000000001", "B000000002"], 1, 2, 4, False),
            (["B000000003", "B000000004"], 3, 4, 4, True),
        ]
    )
    complete_content = page.content
    page_two_reads = 0

    def delayed_page_two_content() -> str:
        nonlocal page_two_reads
        if page.index == 1:
            page_two_reads += 1
            if page_two_reads < 3:
                return _grid_dom(
                    ["B000000003"], start=3, end=4, total=4, terminal=True
                )
        return complete_content()

    page.content = delayed_page_two_content  # type: ignore[method-assign]

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert page_two_reads >= 3
    assert plugin.grid_observation["amazon_grid_extracted_placement_count"] == 4


def test_amazon_grid_scrolls_to_pagination_then_accepts_stable_visible_cards() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
    )
    page = _GridPage(
        [(["B000000001", "B000000002"], 1, 48, 157, True)]
    )
    complete_content = page.content

    def lazy_content() -> str:
        if not page.scroll_events:
            return _grid_dom(
                ["B000000001"], start=1, end=48, total=157, terminal=True
            )
        return complete_content()

    page.content = lazy_content  # type: ignore[method-assign]

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert page.scroll_events
    assert plugin.grid_observation["amazon_grid_extracted_placement_count"] == 2
    assert plugin.grid_observation["amazon_grid_population_observations"] == [
        {
            "page": 1,
            "source_visible_placement_count": 2,
            "displayed_result_range_slot_count": 48,
            "stable_population_polls": 3,
            "population_stable": True,
            "pagination_control_reached": True,
            "observed_card_counts": [2, 2, 2],
            "observed_valid_asin_counts": [2, 2, 2],
        }
    ]


def test_amazon_grid_fails_when_pagination_region_cannot_be_reached() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
        traversal_timeout_seconds=0.01,
    )
    page = _GridPage([(["B000000001"], 1, 48, 157, True)])
    content = page.content
    page.content = lambda: content().replace(  # type: ignore[method-assign]
        "s-pagination-next", "pagination-unavailable"
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "page_population_unproven"


def test_amazon_grid_retries_pagination_while_page_hydrates() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
    )
    page = _GridPage([(["B000000001"], 1, 48, 157, True)])
    content = page.content

    def delayed_pagination() -> str:
        rendered = content()
        if len(page.scroll_events) < 3:
            return rendered.replace("s-pagination-next", "pagination-hydrating")
        return rendered

    page.content = delayed_pagination  # type: ignore[method-assign]

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert len(page.scroll_events) == 3


def test_amazon_grid_accepts_identity_rotation_when_valid_card_count_is_stable() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
    )
    page = _GridPage([(["B000000001"], 1, 48, 157, True)])
    content_reads = 0

    def rotating_sponsored_card() -> str:
        nonlocal content_reads
        content_reads += 1
        asin = "B000000001" if content_reads % 2 else "B000000002"
        return _grid_dom([asin], start=1, end=48, total=157, terminal=True)

    page.content = rotating_sponsored_card  # type: ignore[method-assign]

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert content_reads >= 3
    assert plugin.grid_observation["amazon_grid_extracted_placement_count"] == 1


def test_amazon_grid_reads_the_displayed_range_from_script_free_text() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
    )
    page = _GridPage([(["B000000001", "B000000002"], 1, 2, 99, True)])
    serialized_state = '<script>var s = "1-1 of 99 results for stale";</script>'
    page.content = lambda: _grid_dom(  # type: ignore[method-assign]
        ["B000000001", "B000000002"], start=1, end=2, total=99, terminal=True
    ).replace("<body>", f"<body>{serialized_state}")

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    # Serialized page state must not decide the retailer-displayed range; the
    # projection reads it from script-free text and the traversal gate must agree.
    assert plugin.grid_observation["amazon_grid_result_range_observations"] == [
        {"start": 1, "end": 2, "total": 99}
    ]


def test_amazon_grid_rejects_lowercase_product_identity() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
        traversal_timeout_seconds=0.01,
    )
    page = _GridPage([(["b000000001"], 1, 1, 1, True)])

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "product_identity_absent"


def test_amazon_grid_revalidates_binding_after_page_population_wait() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=1,
    )
    page = _GridPage([(["B000000001"], 1, 1, 1, True)])
    stable_content = page.content
    content_reads = 0

    def content_then_navigate() -> str:
        nonlocal content_reads
        content_reads += 1
        if content_reads >= 2:
            page.url_override = "https://www.amazon.com/s?k=Different+Query"
        return stable_content()

    page.content = content_then_navigate  # type: ignore[method-assign]

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "page_binding_changed_during_population_wait"


def test_amazon_grid_accepts_verified_early_terminal() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=4,
    )
    page = _GridPage([(["B000000001"], 1, 1, 1, True)])

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert plugin.grid_observation["amazon_grid_captured_page_count"] == 1
    assert (
        plugin.grid_observation["amazon_grid_termination"]
        == "retailer_terminal_reconciled"
    )


def test_amazon_grid_fails_when_continuation_disappears_without_terminal() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=2,
    )
    page = _GridPage([(["B000000001"], 1, 1, 10, False)])

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "next_page_control_unavailable"
    assert plugin.grid_observation["amazon_grid_termination"] == "unproven"


def test_amazon_grid_reports_the_retailer_error_shell_explicitly() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty",
        page_count=2,
    )
    page = _GridPage([(["B000000001"], 1, 1, 10, False)])
    page.content = lambda: (  # type: ignore[method-assign]
        "<html><title>Sorry! Something went wrong!</title>"
        '<a href="/ref=cs_503_link"><img src="500_503.png"></a></html>'
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "amazon_error_shell"
    assert "500/503 error shell" in plugin.grid_observation["amazon_grid_failure"]


def test_amazon_grid_marketplace_only_confirmation_does_not_claim_zip() -> None:
    plugin = AmazonSearchGridPlugin(
        target_url="https://www.amazon.com/s?k=Tower+28+Beauty"
    )

    confirmation = plugin.confirm(_US_MARKER)

    assert confirmation.confirmed is True
    assert plugin.describe()["delivery_zip_requested"] is None
    assert plugin.describe()["amazon_grid_location_binding"] == "us_marketplace_only"
    assert "delivery ZIP NOT REQUESTED" in plugin.note(
        plugin.before(object(), setup_timeout_ms=30_000), confirmation
    )


def _content_grid_dom(
    products: list[tuple[str, str]], *, start: int, end: int, total: int
) -> str:
    cards = "".join(
        f"""
        <div data-index="{position}" data-asin="{asin}"
             data-component-type="s-search-result">
          {'<span>Sponsored</span>' if position == 1 else ''}
          <a href="/{name.replace(' ', '-')}/dp/{asin}/ref=sr_1_{position}">
            <h2 aria-label="{name}"><span>{name}</span></h2>
          </a>
          <span aria-label="4.6 out of 5 stars, rating details"></span>
          <a aria-label="1,234 ratings"><span>(1,234)</span></a>
          <span class="a-price"><span class="a-offscreen">$16.00</span></span>
          <span>1K+ bought in past month</span>
          <div data-cy="delivery-block">FREE delivery Tomorrow</div>
        </div>
        """
        for position, (asin, name) in enumerate(products, start=1)
    )
    return (
        f"<html>{_US_MARKER}<body><span>{start}-{end} of {total} results for</span>"
        f'<span>"Tower 28 Beauty"</span>{cards}</body></html>'
    )


def _fake_amazon_grid_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    plugin = kwargs["pre_capture"]
    assert isinstance(plugin, AmazonSearchGridPlugin)
    pages = [
        _content_grid_dom(
            [("B000000001", "SOS Daily Rescue Spray"), ("B000000002", "ShineOn Lip Jelly")],
            start=1,
            end=2,
            total=214,
        ),
        _content_grid_dom(
            [("B000000002", "ShineOn Lip Jelly"), ("B000000003", "LipSoftie")],
            start=3,
            end=4,
            total=219,
        ),
    ]
    plugin._grid_page_doms = pages
    plugin._grid_page_urls = [
        "https://www.amazon.com/s?k=Tower+28+Beauty",
        "https://www.amazon.com/s?k=Tower+28+Beauty&page=2",
    ]
    plugin._grid_observation = {
        "amazon_grid_requested_page_count": 2,
        "amazon_grid_captured_page_count": 2,
        "amazon_grid_extracted_unique_parent_count": 3,
        "amazon_grid_extracted_placement_count": 4,
        "amazon_grid_duplicate_placement_count": 1,
        "amazon_grid_result_range_observations": [
            {"start": 1, "end": 2, "total": 214},
            {"start": 3, "end": 4, "total": 219},
        ],
        "amazon_grid_termination": "requested_page_window_reconciled",
        "amazon_grid_requested_query": "Tower 28 Beauty",
    }
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=plugin._grid_page_urls[-1],
        title='Amazon.com : Tower 28 Beauty',
        rendered_dom=pages[-1],
        visible_text=(
            '3-4 of 219 results for "Tower 28 Beauty" 4.6 out of 5 stars (1.2K) '
            '$16.00 1K+ bought in past month'
        ),
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-07-22T00:00:00Z",
            "pin_confirmed": True,
            "before_snapshot_attempted": True,
            "before_snapshot_steps_completed": True,
            "before_snapshot_reason": None,
            **plugin.describe(),
        },
        warning_notes=[],
        limitation_notes=[],
    )


def test_amazon_grid_runner_files_derived_only_observation_in_v41_lake(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_amazon_grid_capture
    )
    root = DataLakeRoot.for_test(tmp_path / "lake")

    exit_code, message = cloak_writer.run_source_capture_cloakbrowser_packet(
        url="https://www.amazon.com/s?k=Tower+28+Beauty",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Which products occupy the requested Amazon ranked window?",
        data_root=root,
        capture_context="offline Amazon grid test",
        operator_category="test",
        capture_mode=cloak_writer.CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=cloak_writer.unknown_with_reason("not needed"),
        visible_mode_changes=[],
        source_publication_or_event=cloak_writer.unknown_with_reason("not needed"),
        source_edit_or_version=cloak_writer.unknown_with_reason("not needed"),
        cutoff_posture=cloak_writer.unknown_with_reason("not needed"),
        recapture_time=cloak_writer.not_applicable("not needed"),
        re_capture_relationship=cloak_writer.not_applicable("not needed"),
        warnings=[],
        limitations=[],
        retail_capture_profile=get_retail_capture_profile("amazon_grid_aggregate"),
        timeout_seconds=30,
        wait_until="domcontentloaded",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=5_000_000,
        block_heavy_assets=False,
        amazon_grid_page_count=2,
    )

    assert exit_code == 0
    derived_path = Path(
        message.removeprefix(
            "raw sample not retained; derived observation preserved at "
        )
    )
    assert root.list_committed_packet_ids() == []
    projection = json.loads(derived_path.read_text(encoding="utf-8"))
    assert projection["projection_version"] == "v1"
    assert projection["packet_id"] is None
    assert projection["capture_event"]["raw_sample_packet_id"] is None
    assert projection["capture_event"]["capture_profile"] == "amazon_grid_aggregate"
    assert projection["rows"][0]["raw_ref"] is None
    assert projection["rows"][0]["raw_anchor"] is None
    assert projection["completeness"]["status"] == "complete"
    assert projection["completeness"]["termination"] == "requested_page_window_reconciled"
    assert projection["completeness"]["extracted_unique_parent_count"] == 3
    assert projection["completeness"]["extracted_placement_count"] == 4
    assert projection["completeness"]["duplicate_placement_count"] == 1


def test_amazon_grid_explicit_raw_sample_preserves_all_traversed_pages(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_amazon_grid_capture
    )
    root = DataLakeRoot.for_test(tmp_path / "lake")

    exit_code, message = cloak_writer.run_source_capture_cloakbrowser_packet(
        url="https://www.amazon.com/s?k=Tower+28+Beauty",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Which products occupy the requested Amazon ranked window?",
        data_root=root,
        capture_context="offline Amazon grid sample test",
        operator_category="test",
        capture_mode=cloak_writer.CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=cloak_writer.unknown_with_reason("not needed"),
        visible_mode_changes=[],
        source_publication_or_event=cloak_writer.unknown_with_reason("not needed"),
        source_edit_or_version=cloak_writer.unknown_with_reason("not needed"),
        cutoff_posture=cloak_writer.unknown_with_reason("not needed"),
        recapture_time=cloak_writer.not_applicable("not needed"),
        re_capture_relationship=cloak_writer.not_applicable("not needed"),
        warnings=[],
        limitations=[],
        retail_capture_profile=get_retail_capture_profile("amazon_grid_aggregate"),
        timeout_seconds=30,
        wait_until="domcontentloaded",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=5_000_000,
        block_heavy_assets=False,
        amazon_grid_page_count=2,
        retain_retail_grid_raw_sample=True,
    )

    assert exit_code == 0
    raw_text, derived_text = message.split(
        "; derived observation preserved at ", 1
    )
    raw_path = Path(raw_text.removeprefix("raw sample preserved at "))
    derived_path = Path(derived_text)
    loaded = root.load_raw_packet(raw_path.name)
    sample_file = next(
        item
        for item in loaded.manifest["preserved_files"]
        if item["original_path"].endswith("retail_grid_raw_sample_pages.json.gz")
    )
    sample = json.loads(gzip.decompress(loaded.bodies[sample_file["file_id"]]))
    assert len(sample["pages"]) == 2
    projection = json.loads(derived_path.read_text(encoding="utf-8"))
    assert projection["capture_event"]["raw_sample_packet_id"] == raw_path.name
    assert projection["rows"][0]["raw_ref"]["packet_id"] == raw_path.name


def test_amazon_grid_projection_failure_promotes_transient_packet_to_raw(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_amazon_grid_capture
    )
    monkeypatch.setattr(
        cloak_writer,
        "build_retail_grid_observation",
        lambda **_kwargs: (_ for _ in ()).throw(ValueError("fixture parser drift")),
    )
    root = DataLakeRoot.for_test(tmp_path / "lake")

    exit_code, message = cloak_writer.run_source_capture_cloakbrowser_packet(
        url="https://www.amazon.com/s?k=Tower+28+Beauty",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Which products occupy the requested Amazon ranked window?",
        data_root=root,
        capture_context="offline Amazon grid failure test",
        operator_category="test",
        capture_mode=cloak_writer.CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=cloak_writer.unknown_with_reason("not needed"),
        visible_mode_changes=[],
        source_publication_or_event=cloak_writer.unknown_with_reason("not needed"),
        source_edit_or_version=cloak_writer.unknown_with_reason("not needed"),
        cutoff_posture=cloak_writer.unknown_with_reason("not needed"),
        recapture_time=cloak_writer.not_applicable("not needed"),
        re_capture_relationship=cloak_writer.not_applicable("not needed"),
        warnings=[],
        limitations=[],
        retail_capture_profile=get_retail_capture_profile("amazon_grid_aggregate"),
        timeout_seconds=30,
        wait_until="domcontentloaded",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=5_000_000,
        block_heavy_assets=False,
        amazon_grid_page_count=2,
    )

    assert exit_code == cloak_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert "retail_grid_projection_failed: ValueError: fixture parser drift" in message
    packet_ids = root.list_committed_packet_ids()
    assert len(packet_ids) == 1
    assert str(root.find_packet(packet_ids[0])) in message
    assert list(root.path.rglob("projection_retail_grid/*.json")) == []
