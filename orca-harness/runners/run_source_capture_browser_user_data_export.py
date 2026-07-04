from __future__ import annotations

import argparse
import sys
from importlib import import_module
from pathlib import Path
from typing import Protocol, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.auth_state import (
    AuthenticatedSessionMode,
    auth_state_metadata_path_for_label,
    auth_state_path_for_label,
    ensure_auth_state_directory,
    validate_auth_state_file,
    write_auth_state_metadata,
)
from source_capture.browser_user_data import browser_user_data_path_for_label

_EXPORT_OPEN_FAILURE_MESSAGE = (
    "CloakBrowser user-data export could not open the dedicated profile. "
    "Close any browser window using that user-data label, confirm the warmup terminal has finished, "
    "then retry the export."
)


class BrowserUserDataExportEngine(Protocol):
    def export_storage_state(
        self,
        *,
        user_data_dir: Path,
        state_path: Path,
    ) -> None:
        ...


def run_browser_user_data_export(
    *,
    user_data_label: str,
    state_label: str,
    session_mode: AuthenticatedSessionMode,
    auth_state_root: Path | None = None,
    browser_user_data_root: Path | None = None,
    engine: BrowserUserDataExportEngine | None = None,
) -> tuple[int, str]:
    auth_state_directory = ensure_auth_state_directory(auth_state_root=auth_state_root)
    state_path = auth_state_path_for_label(state_label, auth_state_root=auth_state_directory)
    metadata_path = auth_state_metadata_path_for_label(state_label, auth_state_root=auth_state_directory)
    if state_path.exists():
        raise ValueError(f"auth-state file already exists for label: {state_label}")
    if metadata_path.exists():
        raise ValueError(f"auth-state metadata already exists for label: {state_label}")

    user_data_dir = browser_user_data_path_for_label(
        user_data_label,
        user_data_root=browser_user_data_root,
    )
    if not user_data_dir.is_dir():
        raise ValueError(f"browser user-data directory does not exist for label: {user_data_label}")

    export_engine = engine or _CloakBrowserUserDataExportEngine()
    try:
        export_engine.export_storage_state(
            user_data_dir=user_data_dir,
            state_path=state_path,
        )
    except Exception:
        _discard_unbound_state(state_path, metadata_path)
        raise
    validate_auth_state_file(state_label, auth_state_root=auth_state_directory)
    write_auth_state_metadata(
        state_label,
        session_mode=session_mode,
        auth_state_root=auth_state_directory,
    )
    return (
        0,
        (
            f"auth-state saved for {session_mode.value} with label {state_label} "
            f"from browser user-data label {user_data_label}"
        ),
    )


class _CloakBrowserUserDataExportEngine:
    def export_storage_state(
        self,
        *,
        user_data_dir: Path,
        state_path: Path,
    ) -> None:
        try:
            cloakbrowser = import_module("cloakbrowser")
        except ModuleNotFoundError as exc:
            raise RuntimeError("CloakBrowser is not installed. Install cloakbrowser before exporting sessions.") from exc

        for headless in (True, False):
            context = None
            try:
                context = cloakbrowser.launch_persistent_context(
                    user_data_dir,
                    headless=headless,
                    stealth_args=True,
                )
                context.storage_state(path=str(state_path))
                return
            except Exception:
                _discard_unbound_state(state_path, None)
            finally:
                if context is not None:
                    context.close()
        raise RuntimeError(_EXPORT_OPEN_FAILURE_MESSAGE)


def _discard_unbound_state(state_path: Path, metadata_path: Path | None) -> None:
    if metadata_path is not None and metadata_path.exists():
        return
    try:
        state_path.unlink()
    except FileNotFoundError:
        return


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export storage-state JSON from a dedicated local CloakBrowser user-data label. "
            "This writes no Source Capture Packet."
        )
    )
    parser.add_argument("--user-data-label", required=True)
    parser.add_argument("--state-label", required=True)
    parser.add_argument(
        "--session-mode",
        choices=[item.value for item in AuthenticatedSessionMode],
        required=True,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, message = run_browser_user_data_export(
            user_data_label=args.user_data_label,
            state_label=args.state_label,
            session_mode=AuthenticatedSessionMode(args.session_mode),
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture browser user-data export failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"source capture browser user-data export failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"source capture browser user-data export failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
