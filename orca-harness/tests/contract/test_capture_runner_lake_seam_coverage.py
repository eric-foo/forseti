"""Coverage flag: packet-producing capture runners must carry the Data Lake seam.

A runner that writes a SourceCapturePacket must either route into the lake
(``--data-root`` / ``data_root`` -> commit into the lake) or be explicitly
acknowledged as not-yet-synced. This is the enforced version of the manual
"which runners route into the lake?" survey.

The detector follows imported packet-writer names from ``source_capture.*`` so
new thin wrappers such as ``write_youtube_watch_packet`` cannot bypass the seam
contract just because they do not call ``stage_and_write_packet`` directly.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

_RUNNERS_DIR = Path(__file__).resolve().parents[2] / "runners"

_DIRECT_PACKET_WRITER_TOKENS = {"write_local_source_capture_packet", "stage_and_write_packet"}
_PACKET_WRITER_NAME_RE = re.compile(r"write_.*_packet$")
_ENV_OUTPUT_OMITTED_TOKENS = (
    'args.output is None and os.environ.get("ORCA_DATA_ROOT")',
    'output_directory is None and os.environ.get("ORCA_DATA_ROOT")',
)
_EXPLICIT_PAIR_REJECT_TOKENS = (
    "args.output is not None and args.data_root is not None",
    "output_directory is not None and args.data_root is not None",
    "add_mutually_exclusive_group",
)

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
    exposes_output_arg: bool
    exposes_data_root_arg: bool
    exposes_env_fallback: bool
    resolves_data_root: bool
    rejects_output_and_data_root: bool
    env_fallback_uses_output_omitted: bool
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

    @property
    def has_exclusive_output_mode(self) -> bool:
        if not self.exposes_output_arg:
            return True
        return self.rejects_output_and_data_root and self.env_fallback_uses_output_omitted

    def missing_seam_parts(self) -> list[str]:
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

    def missing_output_mode_parts(self) -> list[str]:
        if not self.exposes_output_arg:
            return []
        missing: list[str] = []
        if not self.rejects_output_and_data_root:
            missing.append("explicit --output + --data-root rejection")
        if not self.env_fallback_uses_output_omitted:
            missing.append("ORCA_DATA_ROOT gated on --output being omitted")
        return missing


def _has_any_token(src: str, tokens: tuple[str, ...]) -> bool:
    return any(token in src for token in tokens)


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _is_packet_writer_name(name: str | None) -> bool:
    return bool(name) and (name in _DIRECT_PACKET_WRITER_TOKENS or _PACKET_WRITER_NAME_RE.fullmatch(name))

def _cli_flags(tree: ast.AST) -> set[str]:
    flags: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or _call_name(node) != "add_argument":
            continue
        for arg in node.args:
            if (
                isinstance(arg, ast.Constant)
                and isinstance(arg.value, str)
                and arg.value.startswith("--")
            ):
                flags.add(arg.value)
    return flags


def _source_capture_imports(tree: ast.AST) -> tuple[set[str], set[str]]:
    writer_names = set(_DIRECT_PACKET_WRITER_TOKENS)
    module_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if not (node.module or "").startswith("source_capture"):
                continue
            for alias in node.names:
                if _is_packet_writer_name(alias.name):
                    writer_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("source_capture."):
                    module_aliases.add(alias.asname or alias.name.split(".")[-1])
    return writer_names, module_aliases


def _is_imported_module_writer_call(node: ast.Call, module_aliases: set[str]) -> bool:
    if not isinstance(node.func, ast.Attribute):
        return False
    if not _is_packet_writer_name(node.func.attr):
        return False
    return isinstance(node.func.value, ast.Name) and node.func.value.id in module_aliases


def _producer_calls(
    tree: ast.AST, writer_names: set[str], module_aliases: set[str]
) -> tuple[_ProducerCall, ...]:
    calls: list[_ProducerCall] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name not in writer_names and not _is_imported_module_writer_call(node, module_aliases):
            continue
        calls.append(
            _ProducerCall(
                name=name or "<unknown>",
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
        flags = _cli_flags(tree)
        writer_names, module_aliases = _source_capture_imports(tree)
        calls = _producer_calls(tree, writer_names, module_aliases)
        if calls:
            producers[path.name] = _RunnerSeam(
                exposes_output_arg="--output" in flags,
                exposes_data_root_arg="--data-root" in flags,
                exposes_env_fallback="ORCA_DATA_ROOT" in src,
                resolves_data_root="DataLakeRoot.resolve" in src,
                rejects_output_and_data_root=_has_any_token(src, _EXPLICIT_PAIR_REJECT_TOKENS),
                env_fallback_uses_output_omitted=_has_any_token(src, _ENV_OUTPUT_OMITTED_TOKENS),
                producer_calls=calls,
            )
    return producers


def test_detector_follows_source_capture_module_import_packet_writer_alias() -> None:
    tree = ast.parse(
        """
import source_capture.youtube_watch_packet as ywp

def main(root):
    return ywp.write_youtube_watch_packet(fetch, data_root=root)
"""
    )

    writer_names, module_aliases = _source_capture_imports(tree)
    calls = _producer_calls(tree, writer_names, module_aliases)

    assert len(calls) == 1
    assert calls[0].name == "write_youtube_watch_packet"
    assert calls[0].forwards_data_root is True

def test_detector_distinguishes_packet_output_from_summary_output_root() -> None:
    tree = ast.parse(
        """
def build_parser(parser):
    parser.add_argument("--output-root")
    parser.add_argument("--data-root")
"""
    )

    flags = _cli_flags(tree)

    assert "--output-root" in flags
    assert "--output" not in flags

def test_every_packet_runner_is_lake_wired_or_acknowledged() -> None:
    producers = _packet_producers()
    assert producers, "no packet-producing runners detected -- detection tokens are stale"

    unsynced = {name for name, seam in producers.items() if not seam.has_seam}

    new_unsynced = unsynced - set(KNOWN_UNSYNCED)
    assert not new_unsynced, (
        "Packet-producing runner(s) missing a real lake seam.\n"
        "Wire the seam (mirror run_source_capture_http_packet.py) OR add to KNOWN_UNSYNCED with a reason:\n"
        + "\n".join(
            f"  {name}: {', '.join(producers[name].missing_seam_parts())}"
            for name in sorted(new_unsynced)
        )
    )

    stale_ack = set(KNOWN_UNSYNCED) - unsynced
    assert not stale_ack, (
        "KNOWN_UNSYNCED lists runner(s) that now carry the seam (or are no longer packet producers).\n"
        "Remove them from KNOWN_UNSYNCED:\n"
        f"  {sorted(stale_ack)}"
    )


def test_packet_runner_output_modes_are_exclusive() -> None:
    producers = _packet_producers()
    ambiguous = {
        name: seam.missing_output_mode_parts()
        for name, seam in producers.items()
        if name not in KNOWN_UNSYNCED and not seam.has_exclusive_output_mode
    }

    assert not ambiguous, (
        "Packet-producing runner(s) with --output must keep local-output and lake-output modes exclusive: "
        f"{ambiguous}"
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
