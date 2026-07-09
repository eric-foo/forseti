from __future__ import annotations

from pathlib import Path


FRONT_DOOR_READMES = (
    "forseti/product/README.md",
    "forseti/product/spines/creator_signal/README.md",
    "forseti/product/spines/foundation/ontology/README.md",
    "docs/research/answer_engine/README.md",
    "forseti/product/spines/capture/README.md",
    "forseti/product/spines/judgment/README.md",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _header_lines(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "```yaml")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "```")
    return lines[start + 1 : end]


def _header_value(header: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for line in header:
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return None


def _open_next_entries(header: list[str]) -> list[str]:
    entries: list[str] = []
    in_open_next = False
    for line in header:
        if line.startswith("open_next:"):
            in_open_next = True
            continue
        if not in_open_next:
            continue
        if line.startswith("  - "):
            entries.append(line[4:].strip())
            continue
        if line and not line.startswith(" "):
            break
    return entries


def _repo_path(entry: str) -> str | None:
    target = entry.split(" #", 1)[0].strip().strip("\"").strip("'")
    if target.startswith(("http://", "https://")):
        return None
    return target.split("#", 1)[0]


def test_forseti_front_door_readmes_have_retrieval_headers() -> None:
    for relpath in FRONT_DOOR_READMES:
        header = _header_lines(_repo_root() / relpath)

        assert _header_value(header, "retrieval_header_version") == "1", relpath
        assert _header_value(header, "authority_boundary") == "retrieval_only", relpath
        assert _open_next_entries(header), relpath


def test_forseti_front_door_open_next_targets_exist() -> None:
    missing: list[str] = []

    for relpath in FRONT_DOOR_READMES:
        header = _header_lines(_repo_root() / relpath)
        for entry in _open_next_entries(header):
            target = _repo_path(entry)
            if target is not None and not (_repo_root() / target).exists():
                missing.append(f"{relpath}: {entry}")

    assert not missing
