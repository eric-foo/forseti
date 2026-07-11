"""CLI: select a reach-proven top quarter from complete TikTok grid metrics."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.tiktok.grid_video_selection import (
    TikTokGridVideoSelectionError,
    build_tiktok_grid_video_selection,
)


def run_tiktok_grid_video_selection(
    *,
    input_path: Path,
    expected_item_count: int,
    output_path: Path,
) -> dict[str, Any]:
    if input_path.resolve() == output_path.resolve():
        raise TikTokGridVideoSelectionError("input and output paths must differ")
    raw = input_path.read_bytes()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TikTokGridVideoSelectionError("input is not valid JSON") from exc
    items = _extract_items(payload)
    selection = build_tiktok_grid_video_selection(
        items,
        expected_item_count=expected_item_count,
    )
    selection["input_receipt"] = {
        "file_name": input_path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(selection, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return selection


def _extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        items = None
        for key in ("public_item_stats", "response_items", "videos", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                items = value
                break
        if items is None:
            raise TikTokGridVideoSelectionError(
                "input must be a list or contain public_item_stats, response_items, videos, or items"
            )
    else:
        raise TikTokGridVideoSelectionError("input JSON must be an array or object")
    if not all(isinstance(item, dict) for item in items):
        raise TikTokGridVideoSelectionError("every input item must be an object")
    return items


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Select the reach-first top quarter from complete TikTok creator-grid "
            "playCount/diggCount metrics."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--expected-item-count", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        selection = run_tiktok_grid_video_selection(
            input_path=args.input,
            expected_item_count=args.expected_item_count,
            output_path=args.output,
        )
    except (OSError, TikTokGridVideoSelectionError) as exc:
        parser.exit(status=2, message=f"TikTok grid video selection failed: {exc}\n")
    print(
        json.dumps(
            {
                "status": "selected",
                "selection_count": selection["selection_summary"]["selection_count"],
                "output": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
