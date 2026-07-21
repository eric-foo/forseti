from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.retail_portfolio_onboarding import (
    write_retail_portfolio_onboarding,
)


def run_retail_portfolio_onboarding(
    *, commission_path: Path, output_path: Path
) -> Path:
    write_retail_portfolio_onboarding(
        commission_path=commission_path, output_path=output_path
    )
    return output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compose an owned census, verified retail-grid outcomes, deterministic "
            "parent/listing reconciliation, and verified raw PDP baselines."
        )
    )
    parser.add_argument("--commission", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        output_path = run_retail_portfolio_onboarding(
            commission_path=args.commission, output_path=args.output
        )
    except Exception as exc:
        parser.exit(status=2, message=f"retail portfolio onboarding failed: {exc}\n")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
