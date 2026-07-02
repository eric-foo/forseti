"""End-to-end lake-free proof of the TikTok capture->registry metric loop.

Mirrors the YouTube live-recapture loop test: TWO full cycles against
``DataLakeRoot.for_test`` (CI never resolves the real lake) -- batch packets ->
metric document -> Silver producer -> committed snapshot (run-order chain
advance) -- with the longitudinal rollup history accruing append-only and the
formula revalidator recomputing the whole history clean. Also pins the
registry wiring this lane adds: the snapshot runner's ``tiktok`` platform entry
(committed artifact paths under social_media/tiktok/), the loud-and-clear
failure when a tiktok snapshot is requested against a lake with no rollup
records, and the fail-closed operator account-map resolution (no TikTok ledger
identity exists yet; identity additions are a separate owner-gated lane).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.rollup_formula_revalidation import (
    revalidate_creator_metric_rollups,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    CreatorRollupDiscoveryError,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import SNAPSHOT_WRAPPER_KEY
from data_lake.root import DataLakeRoot
from runners.run_creator_metric_rollup_snapshot import (
    _PLATFORM_OUTPUTS,
    main as snapshot_main,
    run_snapshot,
)
from runners.run_tiktok_batch_metric_rollup_producer import (
    main as producer_main,
    resolve_account_map,
    run_tiktok_batch_producer,
)
from test_tiktok_creator_metric_seed import _commit_batch_packet, _stats, _video

CAPTURE_T1 = "2026-07-01T10:00:00Z"
CAPTURE_T2 = "2026-07-02T09:00:00Z"
RUN_T1 = "2026-07-01T11:00:00Z"
RUN_T2 = "2026-07-02T10:00:00Z"
ACCOUNT_MAP = {"funmimonet": "acct_tt_funmimonet", "scentwithbee": "acct_tt_scentwithbee"}


def _account_ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_tt_funmimonet",
                "platform": "tiktok",
                "public_handle": "funmimonet",
            },
            {
                "platform_account_id": "acct_tt_scentwithbee",
                "platform": "tiktok",
                "public_handle": "scentwithbee",
            },
        ]
    }


def _commit_capture_cycle(data_root: DataLakeRoot, *, captured_at: str, base_views: int) -> None:
    _commit_batch_packet(
        data_root,
        handle="funmimonet",
        capture_timestamp=captured_at,
        videos=[
            _video("7655000000000000001", stats=_stats(base_views, 10, 5)),
            _video("7655000000000000002", stats=_stats(base_views * 2, 20, 8)),
        ],
    )
    _commit_batch_packet(
        data_root,
        handle="scentwithbee",
        capture_timestamp=captured_at,
        videos=[_video("7655000000000000003", stats=_stats(base_views // 2, 5, 2))],
    )


def _snapshot_paths(tmp_path: Path) -> tuple[Path, Path, Path]:
    committed = tmp_path / "committed"
    return (
        committed / "tiktok_profile_grid_creator_metric_rollup_snapshot_v0.json",
        committed / "tiktok_profile_grid_creator_metric_rollup_selection_manifest_v0.json",
        committed / "tiktok_profile_grid_creator_metric_rollup_freshness_receipt_v0.json",
    )


def test_two_cycle_producer_snapshot_and_revalidation_loop(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    account_ledger = _account_ledger()
    snapshot_path, manifest_path, receipt_path = _snapshot_paths(tmp_path)

    # -- cycle 1: admit batches, produce, mint snapshot run 1 -----------------
    _commit_capture_cycle(data_root, captured_at=CAPTURE_T1, base_views=1000)
    result_1 = run_tiktok_batch_producer(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=RUN_T1
    )
    assert len(result_1.rollup_records) == 2
    assert len(result_1.observation_records) == 15  # (2 + 1) videos x 5 named metrics

    summary_1 = run_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform="tiktok",
        snapshot_generated_at=RUN_T1,
        reconciled_at=RUN_T1,
        snapshot_path=snapshot_path,
        manifest_path=manifest_path,
        receipt_path=receipt_path,
        write=True,
    )
    assert summary_1["selection_run_id"] == 1
    assert summary_1["accounts"] == 2

    snapshot_1 = json.loads(snapshot_path.read_text(encoding="utf-8"))
    rollups_1 = {
        rollup["profile_subject_id"]: rollup
        for rollup in snapshot_1[SNAPSHOT_WRAPPER_KEY]["metric_rollups"]
    }
    funmi_1 = rollups_1["acct_tt_funmimonet"]
    assert funmi_1["computed_at"] == RUN_T1
    assert funmi_1["metric_rollups"]["average_views"]["value_or_none"] == 1500.0
    # (10 + 20 + 5 + 8) / (1000 + 2000) = 43 / 3000
    assert funmi_1["metric_rollups"]["engagement_rate"]["value_or_none"] == 0.014333

    # -- cycle 2: recapture with moved numbers, fresh computed_at -------------
    _commit_capture_cycle(data_root, captured_at=CAPTURE_T2, base_views=1500)
    result_2 = run_tiktok_batch_producer(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=RUN_T2
    )
    assert len(result_2.rollup_records) == 2

    summary_2 = run_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform="tiktok",
        snapshot_generated_at=RUN_T2,
        reconciled_at=RUN_T2,
        snapshot_path=snapshot_path,
        manifest_path=manifest_path,
        receipt_path=receipt_path,
        write=True,
    )
    assert summary_2["selection_run_id"] == 2

    snapshot_2 = json.loads(snapshot_path.read_text(encoding="utf-8"))
    rollups_2 = {
        rollup["profile_subject_id"]: rollup
        for rollup in snapshot_2[SNAPSHOT_WRAPPER_KEY]["metric_rollups"]
    }
    funmi_2 = rollups_2["acct_tt_funmimonet"]
    assert funmi_2["computed_at"] == RUN_T2
    assert funmi_2["metric_rollups"]["average_views"]["value_or_none"] == 2250.0  # (1500+3000)/2
    # (10 + 20 + 5 + 8) / (1500 + 3000) = 43 / 4500
    assert funmi_2["metric_rollups"]["engagement_rate"]["value_or_none"] == 0.009556

    # -- the formula revalidator recomputes the WHOLE history (both cycles) ---
    report = revalidate_creator_metric_rollups(data_root)
    assert report.rollups_checked == 4  # 2 accounts x 2 cycles
    assert report.failures_total == 0, [f.failures for f in report.findings if not f.ok]


def test_snapshot_platform_choices_include_tiktok_with_mirrored_paths() -> None:
    assert "tiktok" in _PLATFORM_OUTPUTS
    outputs = _PLATFORM_OUTPUTS["tiktok"]
    for path, token in (
        (outputs.snapshot, "tiktok_profile_grid_creator_metric_rollup_snapshot_v0.json"),
        (outputs.manifest, "tiktok_profile_grid_creator_metric_rollup_selection_manifest_v0.json"),
        (outputs.receipt, "tiktok_profile_grid_creator_metric_rollup_freshness_receipt_v0.json"),
    ):
        assert path.name == token
        assert path.parent.name == "tiktok"
        assert path.parent.parent.name == "social_media"


def test_snapshot_fails_loud_when_lake_has_no_tiktok_rollups(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    snapshot_path, manifest_path, receipt_path = _snapshot_paths(tmp_path)

    # Ledger names tiktok accounts, lake holds no rollup records: discovery
    # fails closed on the expected account set.
    with pytest.raises(CreatorRollupDiscoveryError, match="missing_account_rollup"):
        run_snapshot(
            data_root,
            account_ledger=_account_ledger(),
            platform="tiktok",
            snapshot_generated_at=RUN_T1,
            reconciled_at=RUN_T1,
            snapshot_path=snapshot_path,
            manifest_path=manifest_path,
            receipt_path=receipt_path,
            write=False,
        )

    # Ledger has NO tiktok accounts at all (today's real state): still a loud
    # ValueError, never a silent empty snapshot.
    with pytest.raises(ValueError, match="no platform_accounts"):
        run_snapshot(
            data_root,
            account_ledger={
                "platform_accounts": [
                    {"platform_account_id": "acct_ig_001", "platform": "instagram"}
                ]
            },
            platform="tiktok",
            snapshot_generated_at=RUN_T1,
            reconciled_at=RUN_T1,
            snapshot_path=snapshot_path,
            manifest_path=manifest_path,
            receipt_path=receipt_path,
            write=False,
        )


def test_snapshot_main_exits_clean_on_empty_tiktok_lake(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(lambda cls, **kwargs: data_root))
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(
        json.dumps({"creator_public_handle_linkage_ledger": _account_ledger()}),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit) as excinfo:
        snapshot_main(["--platform", "tiktok", "--account-ledger", str(ledger_path)])
    assert excinfo.value.code == 2
    assert "creator metric rollup snapshot failed" in capsys.readouterr().err


def test_resolve_account_map_merges_ledger_and_cli_fail_closed() -> None:
    ledger = {
        "platform_accounts": [
            {
                "platform_account_id": "acct_tt_funmimonet",
                "platform": "tiktok",
                "public_handle": "@FunmiMonet",
            },
            {
                "platform_account_id": "acct_ig_001",
                "platform": "instagram",
                "public_handle": "someoneelse",
            },
        ]
    }
    # Ledger rows are casefolded and de-@-prefixed; non-tiktok rows are ignored.
    assert resolve_account_map(None, ledger) == {"funmimonet": "acct_tt_funmimonet"}
    # CLI entries merge; a repeat agreeing with the ledger is fine.
    merged = resolve_account_map(
        ["scentwithbee=acct_tt_scentwithbee", "@funmimonet=acct_tt_funmimonet"], ledger
    )
    assert merged == {
        "funmimonet": "acct_tt_funmimonet",
        "scentwithbee": "acct_tt_scentwithbee",
    }
    # A CLI entry contradicting the resolved mapping fails closed.
    with pytest.raises(ValueError, match="conflicts with the mapping"):
        resolve_account_map(["funmimonet=acct_tt_other"], ledger)
    # Malformed entries fail closed.
    with pytest.raises(ValueError, match="handle=account_id"):
        resolve_account_map(["nonsense"], ledger)
    with pytest.raises(ValueError, match="handle=account_id"):
        resolve_account_map(["=acct_tt_x"], ledger)
    # No tiktok identity anywhere: fail with the actionable message.
    with pytest.raises(ValueError, match="no TikTok account mappings available"):
        resolve_account_map(None, {"platform_accounts": []})


def test_producer_main_rejects_malformed_account_map() -> None:
    with pytest.raises(SystemExit) as excinfo:
        producer_main(["--account-map", "nonsense"])
    assert excinfo.value.code == 2


def test_producer_fails_closed_on_unmapped_captured_handle(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(
        data_root,
        handle="funmimonet",
        capture_timestamp=CAPTURE_T1,
        videos=[_video("7655000000000000001", stats=_stats(1000, 10, 5))],
    )
    with pytest.raises(ValueError, match="missing_account_mapping"):
        run_tiktok_batch_producer(
            data_root,
            account_id_by_handle={"scentwithbee": "acct_tt_scentwithbee"},
            generated_at_utc=RUN_T1,
        )
