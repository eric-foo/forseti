from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.capture_request_lifecycle import (
    CaptureRequestLifecycleError,
    validate_capture_request_lifecycle,
)
from data_lake.root import DataLakeRoot, DataLakeRootError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one terminal scan-to-Capture lifecycle ledger and its packet evidence."
    )
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--require-p0", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.ledger.read_text(encoding="utf-8"))
        root = DataLakeRoot.resolve(explicit=args.data_root)
        validate_capture_request_lifecycle(
            payload,
            require_terminal=True,
            require_p0=args.require_p0,
            data_root=root,
            require_packet_verification=True,
        )
    except (OSError, ValueError, json.JSONDecodeError, DataLakeRootError, CaptureRequestLifecycleError) as exc:
        code = getattr(exc, "code", type(exc).__name__)
        parser.exit(status=2, message=f"capture-request lifecycle invalid [{code}]: {exc}\n")

    # A ledger whose requests all declined verifies no packets; say so rather than
    # reporting a verification that never happened.
    verified = sum(1 for event in payload["events"] if event["state"] == "handoff_ready")
    print(
        json.dumps(
            {
                "commission_id": payload["commission_id"],
                "packets_verified": verified,
                "requests": len(payload["requests"]),
                "status": "terminal_packet_verified" if verified else "terminal_no_packets_to_verify",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
