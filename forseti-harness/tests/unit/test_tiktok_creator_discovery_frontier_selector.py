from __future__ import annotations

from capture_spine.tiktok_creator_discovery_frontier import (
    RefreshOutcome,
    ScanReceipt,
    SuggestedAccountObservation,
    build_tiktok_creator_discovery_frontier_register,
)
from capture_spine.tiktok_creator_discovery_frontier.frontier_selector import (
    rank_tiktok_creator_discovery_targets,
    summarize_tiktok_creator_discovery_overlap,
)


def _scan_receipt(root_handle: str) -> dict:
    safe_root = root_handle.replace(".", "_")
    return ScanReceipt(
        receipt_id=f"receipt_{safe_root}",
        run_id=f"run_{safe_root}",
        register_id=f"register_{safe_root}",
        root_seed={
            "platform": "tiktok",
            "handle": root_handle,
            "url": f"https://www.tiktok.com/@{root_handle}",
        },
        source_surface="tiktok_profile_suggested_accounts_existing_cloakbrowser_cdp",
        captured_at_utc="2026-07-09T10:00:00Z",
        method_mode="existing_cloakbrowser_cdp_dom_extraction",
        access_mode="owner_authorized_existing_session_screen_light_dom_read",
        extraction_method="dom_visible_suggested_account_cards",
        browser_session_label_or_none="cloakbrowser_existing_chowdakr",
        parent_grid_packet_id_or_none="01KXROOTGRIDPACKET",
        parent_grid_packet_path_or_none="F:/orca-data-lake/raw/root/01KXROOTGRIDPACKET",
        source_packet_id_or_none="01KXSUGGESTEDPACKET",
        source_packet_path_or_none="F:/orca-data-lake/raw/suggested/01KXSUGGESTEDPACKET",
        parent_profile_capture_status="tiktok_parent_profile_grid_packet_available",
        suggested_accounts_capture_status="tiktok_suggested_accounts_packet_available",
        browser_closed_by_runner=False,
        refresh_attempt_count=0,
        refresh_outcome=RefreshOutcome.NOT_NEEDED,
        pagination_bound=1,
        suggested_accounts_observed=3,
        candidate_profiles_opened=0,
        follow_unfollow_actions_taken=0,
        screenshots_emitted_to_chat=0,
        caps_applied={
            "root_profiles": 1,
            "suggested_accounts_observed": 3,
            "candidate_profiles_opened": 0,
            "screenshots_emitted_to_chat": 0,
        },
        stop_reason="bounded_suggested_accounts_observation_complete",
        exclusions=(
            "no_candidate_profile_open",
            "no_follow_unfollow_action",
            "no_metric_rollup",
            "no_registry_mutation",
            "no_screenshot_chat_output",
        ),
    ).to_dict()


def _register(root_handle: str, *suggested_accounts: SuggestedAccountObservation) -> dict:
    return build_tiktok_creator_discovery_frontier_register(
        scan_receipt=_scan_receipt(root_handle),
        suggested_accounts=suggested_accounts,
        prior_register_pointer=f"docs/review-inputs/{root_handle}.json#/tiktok_creator_discovery_frontier_register",
        accepted_residuals=("selector test register",),
    )


def _suggested(
    handle: str,
    display_name: str | None = None,
    observed_sections: tuple[str, ...] = ("suggested_accounts",),
) -> SuggestedAccountObservation:
    return SuggestedAccountObservation(
        handle=handle,
        display_name_or_none=display_name,
        observed_sections=observed_sections,
    )


def test_target_ranker_prioritizes_once_only_expanded_fragrance_over_repeated_hub() -> None:
    registers = [
        _register(
            "rootone",
            _suggested(
                "smallfrag",
                "Small Fragrance Reviews",
                ("profile_suggested_view_all",),
            ),
            _suggested("hugehub", "Huge Scent Hub"),
        ),
        _register("roottwo", _suggested("hugehub", "Huge Scent Hub")),
        _register("rootthree", _suggested("hugehub", "Huge Scent Hub")),
    ]

    ranked = rank_tiktok_creator_discovery_targets(registers)

    assert ranked[0]["handle"] == "smallfrag"
    assert ranked[0]["recommendation_tier"] == "prioritize"
    assert ranked[0]["prior_suggested_frequency"] == 1
    assert ranked[0]["is_expanded_tail_observed"] is True
    assert ranked[-1]["handle"] == "hugehub"
    assert ranked[-1]["recommendation_tier"] == "deprioritize_repeated_hub"
    assert ranked[-1]["prior_suggested_frequency"] == 3


def test_target_ranker_excludes_already_scanned_roots_by_default() -> None:
    registers = [
        _register("alreadyroot", _suggested("freshfrag", "Fresh Frag")),
        _register("otherroot", _suggested("alreadyroot", "Already Root")),
    ]

    handles = [item["handle"] for item in rank_tiktok_creator_discovery_targets(registers)]

    assert "freshfrag" in handles
    assert "alreadyroot" not in handles


def test_target_ranker_excludes_caller_supplied_already_scanned_handles() -> None:
    registers = [
        _register("rootone", _suggested("freshfrag", "Fresh Frag"), _suggested("seenalready")),
    ]

    handles = [
        item["handle"]
        for item in rank_tiktok_creator_discovery_targets(
            registers, already_scanned_handles=("SeenAlready",)
        )
    ]

    assert "freshfrag" in handles
    assert "seenalready" not in handles


def test_overlap_summary_splits_repeated_once_and_new_tail_candidates() -> None:
    prior_registers = [
        _register("rootone", _suggested("repeat2"), _suggested("once_now"), _suggested("oldonly")),
        _register("roottwo", _suggested("repeat2"), _suggested("oldtwo")),
    ]
    current_register = _register(
        "currentroot",
        _suggested("repeat2"),
        _suggested("once_now"),
        _suggested("brandnew", observed_sections=("profile_suggested_view_all",)),
    )

    summary = summarize_tiktok_creator_discovery_overlap(
        prior_registers=prior_registers,
        current_register=current_register,
    )

    assert summary["current_root_handle"] == "currentroot"
    assert summary["current_candidate_count"] == 3
    assert summary["seen_before_count"] == 2
    assert summary["not_seen_before_count"] == 1
    assert summary["repeated_prior_2plus"] == ["repeat2"]
    assert summary["prior_once_now_repeated"] == ["once_now"]
    assert summary["brand_new_tail"] == ["brandnew"]
    assert "overlap summary is not capture authorization" in summary["non_claims"]
