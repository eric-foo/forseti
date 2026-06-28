"""Coverage flag: a packet-producing capture runner must either carry the Data
Lake seam (``--data-root`` / ``data_root`` -> commit into the lake) or be
explicitly acknowledged as not-yet-synced.

This is the enforced version of the manual "which runners route into the lake?"
survey. Adding a NEW packet runner without the seam -- and without an entry in
``KNOWN_UNSYNCED`` -- fails this test on purpose. That is the nudge: wire the
seam (mirror ``run_source_capture_http_packet.py``) or acknowledge the gap with a
reason. The test also fails if a runner gains the seam but is left in the
allowlist, so the allowlist cannot rot.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

_RUNNERS_DIR = Path(__file__).resolve().parents[2] / "runners"

# A runner is a raw-packet PRODUCER if it writes a SourceCapturePacket.
_PRODUCER_TOKENS = ("write_local_source_capture_packet", "stage_and_write_packet")

# Packet-producing runners that intentionally do NOT route into the lake yet.
# Each MUST carry a reason. Remove an entry when you wire its seam. Adding a new
# packet runner without the seam and without an entry here fails the test below.
KNOWN_UNSYNCED: dict[str, str] = {}


@dataclass(frozen=True)
class _ProducerCall:
    name: str
    line: int
    forwards_data_root: bool


@dataclass(frozen=True)
class _RunnerSeam:
    exposes_data_root_arg: bool
    exposes_env_fallback: bool
    resolves_data_root: bool
    producer_calls: tuple[_ProducerCall, ...]

    @property
    def forwards_data_root(self) -> bool:
        return any(call.forwards_data_root for call in self.producer_calls)

    @property
    def has_seam(self) -> bool:
        return (
            self.exposes_data_root_arg
            and self.exposes_env_fallback
            and self.resolves_data_root
            and self.forwards_data_root
        )

    def missing_parts(self) -> list[str]:
        missing: list[str] = []
        if not self.exposes_data_root_arg:
            missing.append("--data-root argument")
        if not self.exposes_env_fallback:
            missing.append("ORCA_DATA_ROOT fallback")
        if not self.resolves_data_root:
            missing.append("DataLakeRoot.resolve")
        if not self.forwards_data_root:
            missing.append("data_root= forwarded into packet writer")
        return missing


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _producer_calls(tree: ast.AST) -> tuple[_ProducerCall, ...]:
    calls: list[_ProducerCall] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name not in _PRODUCER_TOKENS:
            continue
        calls.append(
            _ProducerCall(
                name=name,
                line=node.lineno,
                forwards_data_root=any(keyword.arg == "data_root" for keyword in node.keywords),
            )
        )
    return tuple(calls)


def _packet_producers() -> dict[str, _RunnerSeam]:
    """Map each packet-producing runner filename to its lake seam shape."""
    producers: dict[str, _RunnerSeam] = {}
    for path in sorted(_RUNNERS_DIR.glob("run_*.py")):
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(path))
        calls = _producer_calls(tree)
        if calls:
            producers[path.name] = _RunnerSeam(
                exposes_data_root_arg="--data-root" in src,
                exposes_env_fallback="ORCA_DATA_ROOT" in src,
                resolves_data_root="DataLakeRoot.resolve" in src,
                producer_calls=calls,
            )
    return producers


def test_every_packet_runner_is_lake_wired_or_acknowledged() -> None:
    producers = _packet_producers()
    assert producers, "no packet-producing runners detected -- detection tokens are stale"

    unsynced = {name for name, seam in producers.items() if not seam.has_seam}

    new_unsynced = unsynced - set(KNOWN_UNSYNCED)
    assert not new_unsynced, (
        "Packet-producing runner(s) missing a real lake seam.\n"
        "Wire the seam (mirror run_source_capture_http_packet.py) OR add to KNOWN_UNSYNCED with a reason:\n"
        + "\n".join(
            f"  {name}: {', '.join(producers[name].missing_parts())}"
            for name in sorted(new_unsynced)
        )
    )

    stale_ack = set(KNOWN_UNSYNCED) - unsynced
    assert not stale_ack, (
        "KNOWN_UNSYNCED lists runner(s) that now carry the seam (or are no longer packet producers).\n"
        "Remove them from KNOWN_UNSYNCED:\n"
        f"  {sorted(stale_ack)}"
    )


def test_known_unsynced_entries_have_reasons() -> None:
    missing = [name for name, reason in KNOWN_UNSYNCED.items() if not reason.strip()]
    assert not missing, f"KNOWN_UNSYNCED entries need a reason: {missing}"


def test_packet_runner_lake_seams_reach_packet_writers() -> None:
    producers = _packet_producers()
    missing = {
        name: [
            f"{call.name} line {call.line}"
            for call in seam.producer_calls
            if not call.forwards_data_root
        ]
        for name, seam in producers.items()
        if name not in KNOWN_UNSYNCED
    }
    missing = {name: calls for name, calls in missing.items() if calls}

    assert not missing, (
        "Packet-producing runner(s) expose a lake seam but do not forward data_root= "
        f"into every packet writer call: {missing}"
    )
