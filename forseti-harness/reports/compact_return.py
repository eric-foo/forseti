"""Bound a complete command return before emission; never slice JSON or evidence."""
import json
from pathlib import Path


def output_budget(value) -> int:
    budget = int(value)
    if not 1024 <= budget <= 32768:
        raise ValueError("max-output-bytes must be between 1024 and 32768")
    return budget


def write_verified(value: dict, path: Path) -> Path:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, allow_nan=False, indent=2)
    if json.loads(path.read_text(encoding="utf-8")) != value:
        raise ValueError("saved report differs from collected result")
    return path


def bounded_json(value: dict, *, record_path: Path, facts: dict, budget: int = 8192) -> str:
    """Facts must retain status/unknowns; overflow explicitly requires the full record."""
    budget = output_budget(budget)

    def encode(item):
        return json.dumps(item, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"

    text = encode(value)
    size = len(text.encode("utf-8"))
    if size <= budget:
        return text
    text = encode({"return_view": "details_required", "reason": "combined_return_exceeds_budget",
                   "full_return_bytes": size, "record_path": str(record_path.resolve()),
                   "facts": facts})
    if len(text.encode("utf-8")) > budget:
        raise ValueError("even the detail reference exceeds max-output-bytes; no partial return emitted")
    return text
