"""Coverage flag: Bronze-writing capture runners must carry the Data Lake seam.

A runner that writes a SourceCapturePacket must either route into the lake
(``--data-root`` / ``data_root`` -> commit into the lake) or be explicitly
acknowledged as not-yet-synced. This is the enforced version of the manual
"which runners route into the lake?" survey.

The detector follows imported writer behavior from ``source_capture.*`` so new
thin wrappers such as ``write_asr_transcript`` or ``write_youtube_watch_packet``
cannot bypass the seam contract just because their name does not end in
``_packet`` or because they do not call ``stage_and_write_packet`` directly.
"""
from __future__ import annotations

import ast
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from functools import cache
from pathlib import Path

_HARNESS_ROOT = Path(__file__).resolve().parents[2]
_RUNNERS_DIR = _HARNESS_ROOT / "runners"
_SOURCE_CAPTURE_DIR = _HARNESS_ROOT / "source_capture"

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

# Current Bronze writer surface. This is the explicit audit answer for "which
# runners are supposed to write raw Bronze evidence?" Direct writers call a
# SourceCapturePacket writer. Orchestrators forward data_root into raw-packet
# sub-runners and are tested separately below.
EXPECTED_BRONZE_WRITER_RUNNERS = frozenset(
    {
        "run_fragrance_review_lake_packet.py",
        "run_fragrantica_mgt_capture.py",
        "run_ig_reels_lane_orchestrator.py",
        "run_parfumo_mgt_capture.py",
        "run_source_capture_antiblock_http_packet.py",
        "run_source_capture_archive_packet.py",
        "run_source_capture_authenticated_browser_packet.py",
        "run_source_capture_browser_packet.py",
        "run_source_capture_cloakbrowser_packet.py",
        "run_source_capture_historical_packet.py",
        "run_source_capture_http_packet.py",
        "run_source_capture_ig_calls_packet.py",
        "run_source_capture_ig_reels_audio_packet.py",
        "run_source_capture_ig_reels_grid_packet.py",
        "run_source_capture_media_packet.py",
        "run_source_capture_packet.py",
        "run_source_capture_price_payload_packet.py",
        "run_source_capture_tiktok_batch_packet.py",
        "run_source_capture_tiktok_video_packet.py",
        "run_source_capture_youtube_asr_packet.py",
        "run_source_capture_youtube_caption_packet.py",
        "run_source_capture_youtube_watch_packet.py",
    }
)

BRONZE_PACKET_ORCHESTRATORS: dict[str, tuple[str, ...]] = {
    "run_fragrantica_mgt_capture.py": ("http_runner", "cloakbrowser_runner"),
    "run_ig_reels_lane_orchestrator.py": ("grid_runner",),
}

FORBIDDEN_RUNNER_RAW_PUBLICATION_CALLS = {
    "allocate_raw_packet_dir",
    "publish_raw_packet",
    "record_availability",
}

NON_RAW_LAKE_TOUCHPOINT_CALLS = {
    "append_record",
    "append_record_set",
    "append_silver_record",
    "catalog_coverage_census",
    "inspect_catalog",
    "is_record_set_complete",
    "lane_dir",
    "load_attachment_record_body",
    "rebuild_catalog",
    "record_path",
    "source_surface_catalog_rows",
}

EXPECTED_NON_RAW_LAKE_TOUCHPOINTS = Counter(
    {
        ("capture_spine/creator_profile_current/silver_metric_producer.py", "append_silver_record"): 2,
        (
            "capture_spine/creator_profile_current/silver_metric_producer.py",
            "source_surface_catalog_rows",
        ): 1,
        ("capture_spine/creator_profile_current/silver_metric_reader.py", "lane_dir"): 3,
        (
            "capture_spine/creator_profile_current/youtube_silver_metric_producer.py",
            "append_silver_record",
        ): 2,
        (
            "capture_spine/creator_profile_current/youtube_silver_metric_producer.py",
            "source_surface_catalog_rows",
        ): 1,
        ("cleaning/basenotes_lake.py", "append_record"): 1,
        ("cleaning/basenotes_lake.py", "append_silver_record"): 1,
        ("cleaning/fragrantica_lake.py", "append_record"): 1,
        ("cleaning/fragrantica_lake.py", "append_silver_record"): 1,
        ("cleaning/parfumo_lake.py", "append_record"): 1,
        ("cleaning/parfumo_lake.py", "append_silver_record"): 1,
        ("cleaning/transcript_product_lake.py", "append_record_set"): 1,
        ("data_lake/catalog.py", "inspect_catalog"): 2,
        ("data_lake/consumption.py", "append_record"): 1,
        ("data_lake/consumption.py", "lane_dir"): 1,
        ("data_lake/derived_retrieval_views.py", "lane_dir"): 1,
        ("data_lake/silver_record.py", "append_record"): 1,
        ("ecr/lake.py", "append_record_set"): 1,
        ("runners/run_capture_ecr_cleaning_smoke.py", "lane_dir"): 1,
        ("runners/run_cleaning_spine_periodic_audit.py", "record_path"): 1,
        ("runners/run_data_lake_catalog.py", "catalog_coverage_census"): 1,
        ("runners/run_data_lake_catalog.py", "inspect_catalog"): 1,
        ("runners/run_data_lake_catalog.py", "rebuild_catalog"): 1,
        ("runners/run_ig_reels_lane_orchestrator.py", "is_record_set_complete"): 1,
        ("runners/run_ig_reels_product_extract.py", "is_record_set_complete"): 3,
        ("runners/run_source_capture_ig_reels_deep_capture.py", "is_record_set_complete"): 1,
        ("runners/run_transcript_product_extract.py", "is_record_set_complete"): 1,
        ("runners/run_transcript_product_extract.py", "lane_dir"): 1,
        ("runners/run_transcript_product_extract.py", "record_path"): 1,
        ("signal_content/lake.py", "append_record"): 1,
        ("source_capture/basenotes_projection.py", "append_record"): 1,
        ("source_capture/fragrance_review_lake.py", "append_record"): 1,
        ("source_capture/fragrantica_projection.py", "append_record"): 1,
        ("source_capture/ig_projection.py", "append_record"): 1,
        ("source_capture/ig_reels_behavioral_lake.py", "is_record_set_complete"): 2,
        ("source_capture/ig_reels_behavioral_lake.py", "lane_dir"): 1,
        ("source_capture/ig_reels_behavioral_lake.py", "record_path"): 1,
        ("source_capture/ig_reels_deep_capture_lake.py", "append_record_set"): 1,
        ("source_capture/ig_reels_grid_projection.py", "append_record"): 1,
        ("source_capture/ig_reels_grid_projection.py", "load_attachment_record_body"): 1,
        ("source_capture/ig_reels_grid_projection.py", "record_path"): 1,
        ("source_capture/ig_reels_grid_projection.py", "source_surface_catalog_rows"): 1,
        ("source_capture/parfumo_projection.py", "append_record"): 1,
        ("source_capture/retail_pdp_projection.py", "append_record"): 1,
        ("source_capture/transcript/asr_packet.py", "append_record_set"): 1,
        ("source_capture/transcript/ig_reels_audio_packet.py", "append_record"): 1,
        ("youtube_capture/behavioral_projection.py", "is_record_set_complete"): 1,
        ("youtube_capture/behavioral_projection.py", "lane_dir"): 1,
    }
)


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


def _called_names(node: ast.AST) -> set[str]:
    return {
        name
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
        for name in [_call_name(child)]
        if name is not None
    }


@cache
def _source_capture_packet_writer_names() -> frozenset[str]:
    """Function names in source_capture that eventually stage/write a raw packet."""
    function_calls: dict[str, set[str]] = {}
    for path in sorted(_SOURCE_CAPTURE_DIR.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_calls[node.name] = _called_names(node)

    writers = set(_DIRECT_PACKET_WRITER_TOKENS)
    changed = True
    while changed:
        changed = False
        for name, calls in function_calls.items():
            if name not in writers and calls.intersection(writers):
                writers.add(name)
                changed = True
    return frozenset(writers)


def _is_packet_writer_name(name: str | None, packet_writer_names: set[str] | frozenset[str]) -> bool:
    return bool(name) and (
        name in packet_writer_names or bool(_PACKET_WRITER_NAME_RE.fullmatch(name))
    )

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
    packet_writer_names = _source_capture_packet_writer_names()
    writer_names = set(_DIRECT_PACKET_WRITER_TOKENS)
    module_aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if not (node.module or "").startswith("source_capture"):
                continue
            for alias in node.names:
                if _is_packet_writer_name(alias.name, packet_writer_names):
                    writer_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("source_capture."):
                    module_aliases.add(alias.asname or alias.name.split(".")[-1])
    return writer_names, module_aliases


def _is_imported_module_writer_call(node: ast.Call, module_aliases: set[str]) -> bool:
    if not isinstance(node.func, ast.Attribute):
        return False
    if not _is_packet_writer_name(node.func.attr, _source_capture_packet_writer_names()):
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


def _bronze_writer_runners() -> frozenset[str]:
    return frozenset(_packet_producers()).union(BRONZE_PACKET_ORCHESTRATORS)


@cache
def _tracked_harness_python_files() -> tuple[Path, ...]:
    result = subprocess.run(
        ["git", "-C", str(_HARNESS_ROOT.parent), "ls-files", "--", "orca-harness"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = _HARNESS_ROOT.parent / line
        if path.suffix != ".py":
            continue
        relative_path = path.relative_to(_HARNESS_ROOT).as_posix()
        if relative_path.startswith("tests/"):
            continue
        paths.append(path)
    return tuple(sorted(paths))


def _non_raw_lake_touchpoints() -> Counter[tuple[str, str]]:
    """Current non-raw lake write/read touchpoints that must be classified before GT forks."""
    touchpoints: Counter[tuple[str, str]] = Counter()
    for path in _tracked_harness_python_files():
        relative_path = path.relative_to(_HARNESS_ROOT).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = _call_name(node)
            if name in NON_RAW_LAKE_TOUCHPOINT_CALLS:
                touchpoints[(relative_path, name)] += 1
    return touchpoints

def _calls_named(tree: ast.AST, names: tuple[str, ...]) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node) in names
    ]


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


def test_detector_discovers_indirect_source_capture_packet_writers() -> None:
    writers = _source_capture_packet_writer_names()

    assert "write_asr_transcript" in writers
    assert "write_ig_reels_asr_transcript" in writers
    assert "write_caption_packet" in writers
    assert "write_youtube_watch_packet" in writers


def test_current_bronze_writer_runner_surface_is_explicit() -> None:
    assert _bronze_writer_runners() == EXPECTED_BRONZE_WRITER_RUNNERS


def test_non_raw_lake_touchpoint_inventory_is_explicit() -> None:
    actual = _non_raw_lake_touchpoints()
    added = +(actual - EXPECTED_NON_RAW_LAKE_TOUCHPOINTS)
    removed = +(EXPECTED_NON_RAW_LAKE_TOUCHPOINTS - actual)

    assert actual == EXPECTED_NON_RAW_LAKE_TOUCHPOINTS, (
        "Non-raw Data Lake touchpoint inventory changed. Classify each new or removed "
        "touchpoint before selecting Manifest v2, a manifest-equivalent index, or a "
        "physicalization backend.\n"
        f"added={dict(sorted(added.items()))}\n"
        f"removed={dict(sorted(removed.items()))}"
    )

def test_non_raw_lake_touchpoint_inventory_reads_tracked_source_only() -> None:
    relative_paths = {
        path.relative_to(_HARNESS_ROOT).as_posix() for path in _tracked_harness_python_files()
    }

    assert "data_lake/root.py" in relative_paths
    assert not any(path.startswith("tests/") for path in relative_paths)
    assert not any(path.startswith("_test_runs/") for path in relative_paths)

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


def test_bronze_packet_orchestrators_forward_data_root_to_subrunners() -> None:
    missing: dict[str, list[str]] = {}
    for filename, callee_names in BRONZE_PACKET_ORCHESTRATORS.items():
        path = _RUNNERS_DIR / filename
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        calls = _calls_named(tree, callee_names)
        problems = [
            f"{_call_name(call)} line {call.lineno}"
            for call in calls
            if not any(keyword.arg == "data_root" for keyword in call.keywords)
        ]
        if not calls:
            problems.append(f"no calls found for {callee_names!r}")
        if problems:
            missing[filename] = problems

    assert not missing, (
        "Bronze packet orchestrator(s) must forward data_root= to raw-packet subrunners: "
        f"{missing}"
    )


def test_bronze_writers_do_not_directly_publish_raw_packets() -> None:
    offenders: dict[str, list[str]] = {}
    for filename in sorted(_bronze_writer_runners()):
        path = _RUNNERS_DIR / filename
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        hits = [
            f"{_call_name(node)} line {node.lineno}"
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and _call_name(node) in FORBIDDEN_RUNNER_RAW_PUBLICATION_CALLS
        ]
        if hits:
            offenders[filename] = hits

    assert not offenders, (
        "Bronze writer runner(s) must not publish/mark raw packets directly; "
        "route raw commits through source_capture.writer or packet_assembly: "
        f"{offenders}"
    )
