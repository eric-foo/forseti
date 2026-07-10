from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_creator_profile_current_materialize import _enforce_new_account_preflight


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _ledger(path: Path, account_ids: list[str]) -> Path:
    return _write_json(
        path,
        {"platform_accounts": [{"platform_account_id": account_id} for account_id in account_ids]},
    )


def _view(path: Path, account_ids: list[str]) -> Path:
    return _write_json(
        path,
        {
            "creator_profile_current_view": {
                "creators": [
                    {"platform_accounts": [{"platform_account_id": account_id}]}
                    for account_id in account_ids
                ]
            }
        },
    )


def _preflight_receipt(path: Path, *, blocked_actions: int) -> Path:
    return _write_json(
        path,
        {
            "creator_registry_match_preflight_receipt": {
                "summary": {"blocked_actions": blocked_actions}
            }
        },
    )


def test_no_new_accounts_needs_no_receipt(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path / "ledger.json", ["acct_a"])
    view = _view(tmp_path / "view.json", ["acct_a"])
    _enforce_new_account_preflight(
        account_ledger_path=ledger, output_path=view, preflight_receipt_path=None
    )


def test_new_account_without_receipt_is_rejected(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path / "ledger.json", ["acct_a", "acct_new"])
    view = _view(tmp_path / "view.json", ["acct_a"])
    with pytest.raises(ValueError, match="acct_new"):
        _enforce_new_account_preflight(
            account_ledger_path=ledger, output_path=view, preflight_receipt_path=None
        )


def test_missing_view_treats_every_account_as_new(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path / "ledger.json", ["acct_a"])
    with pytest.raises(ValueError, match="preflight-receipt"):
        _enforce_new_account_preflight(
            account_ledger_path=ledger,
            output_path=tmp_path / "absent_view.json",
            preflight_receipt_path=None,
        )


def test_new_account_with_clean_receipt_passes(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path / "ledger.json", ["acct_a", "acct_new"])
    view = _view(tmp_path / "view.json", ["acct_a"])
    receipt = _preflight_receipt(tmp_path / "receipt.json", blocked_actions=0)
    _enforce_new_account_preflight(
        account_ledger_path=ledger, output_path=view, preflight_receipt_path=receipt
    )


def test_new_account_with_blocking_receipt_is_rejected(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path / "ledger.json", ["acct_a", "acct_new"])
    view = _view(tmp_path / "view.json", ["acct_a"])
    receipt = _preflight_receipt(tmp_path / "receipt.json", blocked_actions=2)
    with pytest.raises(ValueError, match="blocking"):
        _enforce_new_account_preflight(
            account_ledger_path=ledger, output_path=view, preflight_receipt_path=receipt
        )
