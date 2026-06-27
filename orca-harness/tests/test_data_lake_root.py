from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import (
    DataLakeRoot,
    DataLakeRootError,
    EPOCH_MARKER_FILENAME,
    LAKE_EPOCH,
    LAKE_EPOCH_POLICY,
    LAKE_SUBDIRECTORIES,
    ROOT_MARKER_CONTRACT_VERSION,
    ROOT_MARKER_DEFAULT_LABEL,
    ROOT_MARKER_FILENAME,
    raw_shard,
)
from harness_utils import generate_ulid
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _init(tmp_path: Path, name: str = "orca-data") -> DataLakeRoot:
    # tmp_path lives inside the repo working tree; for_test bypasses the
    # outside-repo production guard (which is exercised separately below).
    return DataLakeRoot.for_test(tmp_path / name)


# -- resolver / fail-closed -------------------------------------------------

def test_resolve_unset_is_fail_closed(tmp_path: Path) -> None:
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.resolve(env={}, repo_root=None)


def test_resolve_relative_path_rejected(tmp_path: Path) -> None:
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.resolve(explicit="relative/dir", env={}, repo_root=None)


def test_resolve_inside_repo_rejected(tmp_path: Path) -> None:
    root = _init(tmp_path)
    # Treat the root's own path as the repo root -> it resolves "inside the repo".
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.resolve(explicit=root.path, env={}, repo_root=root.path)


def test_resolve_missing_marker_rejected(tmp_path: Path) -> None:
    bare = tmp_path / "bare"
    bare.mkdir()
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.resolve(explicit=bare, env={}, repo_root=None)


def test_resolve_marker_uuid_mismatch_rejected(tmp_path: Path) -> None:
    root = _init(tmp_path)
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.resolve(
            explicit=root.path, env={}, expected_uuid="WRONGUUID", repo_root=None
        )


def test_resolve_success_with_env(tmp_path: Path) -> None:
    root = _init(tmp_path)
    resolved = DataLakeRoot.resolve(env={"ORCA_DATA_ROOT": str(root.path)}, repo_root=None)
    assert resolved.path == root.path
    assert resolved.root_uuid == root.root_uuid


def test_resolve_precedence_explicit_over_env(tmp_path: Path) -> None:
    a = _init(tmp_path, "a")
    b = _init(tmp_path, "b")
    resolved = DataLakeRoot.resolve(
        explicit=a.path, env={"ORCA_DATA_ROOT": str(b.path)}, repo_root=None
    )
    assert resolved.path == a.path


def test_test_root_is_never_a_production_fallback(tmp_path: Path) -> None:
    # for_test builds a usable root, but it does not register itself in the
    # production precedence chain: resolve() with an empty env still fails closed.
    _init(tmp_path)
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.resolve(env={}, repo_root=None)


# -- init / marker / skeleton ----------------------------------------------

def test_initialize_creates_skeleton_and_marker(tmp_path: Path) -> None:
    root = _init(tmp_path)
    for sub in LAKE_SUBDIRECTORIES:
        assert (root.path / sub).is_dir(), sub
    marker = json.loads((root.path / ROOT_MARKER_FILENAME).read_text(encoding="utf-8"))
    assert marker["root_uuid"]
    assert marker["contract_version"] == ROOT_MARKER_CONTRACT_VERSION
    epoch = json.loads((root.path / EPOCH_MARKER_FILENAME).read_text(encoding="utf-8"))
    assert epoch["lake_epoch"] == LAKE_EPOCH
    assert epoch["epoch_policy"] == LAKE_EPOCH_POLICY
    assert epoch["compatibility_migration"] is False
    assert epoch["legacy_roots"] == []


def test_initialize_creates_default_v4_1_label_and_legacy_roots(tmp_path: Path) -> None:
    legacy = "F:\\orca-data-lake"
    root = DataLakeRoot.initialize(tmp_path / "forward", repo_root=None, legacy_roots=[legacy])
    marker = json.loads((root.path / ROOT_MARKER_FILENAME).read_text(encoding="utf-8"))
    assert marker["label"] == ROOT_MARKER_DEFAULT_LABEL
    epoch = json.loads((root.path / EPOCH_MARKER_FILENAME).read_text(encoding="utf-8"))
    assert epoch["legacy_roots"] == [legacy]


def test_resolve_missing_epoch_marker_rejected(tmp_path: Path) -> None:
    root = _init(tmp_path)
    (root.path / EPOCH_MARKER_FILENAME).unlink()
    with pytest.raises(DataLakeRootError, match="epoch marker"):
        DataLakeRoot.resolve(explicit=root.path, env={}, repo_root=None)


def test_resolve_legacy_v0_marker_rejected(tmp_path: Path) -> None:
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    (legacy / ROOT_MARKER_FILENAME).write_text(
        json.dumps({"root_uuid": "LEGACYROOT", "contract_version": "v0"}),
        encoding="utf-8",
    )
    with pytest.raises(DataLakeRootError, match="contract_version"):
        DataLakeRoot.resolve(explicit=legacy, env={}, repo_root=None)


def test_initialize_refuses_nonempty_foreign_dir(tmp_path: Path) -> None:
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    (foreign / "stray.txt").write_text("x", encoding="utf-8")
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.initialize(foreign, repo_root=None)


# -- write-once raw ---------------------------------------------------------

def test_allocate_raw_packet_dir_is_create_only(tmp_path: Path) -> None:
    root = _init(tmp_path)
    pid = generate_ulid()
    container = root.allocate_raw_packet_dir(pid)
    assert container.is_dir()
    assert container == root.path / "raw" / raw_shard(pid) / pid
    with pytest.raises(DataLakeRootError):
        root.allocate_raw_packet_dir(pid)  # write-once: second allocation fails


def test_allocate_rejects_bad_packet_id(tmp_path: Path) -> None:
    root = _init(tmp_path)
    for bad in ["../evil", "short", "lower-case-not-crockford", "x" * 26, "AAAA"]:
        with pytest.raises(DataLakeRootError):
            root.allocate_raw_packet_dir(bad)


# -- append-only derived/ack + path escape ---------------------------------

def test_append_record_is_append_only(tmp_path: Path) -> None:
    root = _init(tmp_path)
    pid = generate_ulid()
    target = root.append_record(
        subtree="derived", raw_anchor=pid, lane="projection", record_id="rec_01", data=b"{}"
    )
    assert target.read_bytes() == b"{}"
    assert target == root.path / "derived" / raw_shard(pid) / pid / "projection" / "rec_01"
    with pytest.raises(DataLakeRootError):
        root.append_record(
            subtree="derived", raw_anchor=pid, lane="projection", record_id="rec_01", data=b"{}"
        )


def test_append_record_rejects_path_escape(tmp_path: Path) -> None:
    root = _init(tmp_path)
    with pytest.raises(DataLakeRootError):
        root.append_record(
            subtree="derived", raw_anchor="../../etc", lane="x", record_id="y", data=b""
        )


def test_append_record_rejects_non_appendable_subtree(tmp_path: Path) -> None:
    root = _init(tmp_path)
    with pytest.raises(DataLakeRootError):
        root.append_record(
            subtree="raw", raw_anchor=generate_ulid(), lane="x", record_id="y", data=b""
        )


# -- test-mode bypass -------------------------------------------------------

def test_for_test_bypasses_outside_repo_guard(tmp_path: Path) -> None:
    # tmp_path lives inside the repo working tree; for_test must still succeed.
    root = DataLakeRoot.for_test(tmp_path / "lake")
    assert (root.path / "raw").is_dir()
    assert (root.path / "indexes" / "derived_retrieval").is_dir()


# -- capture writer routing -------------------------------------------------

def _writer_common(src: Path) -> dict:
    return dict(
        input_files=[src],
        source_family="reddit",
        source_surface="r/test",
        source_locator=known_fact("https://example/test"),
        decision_question="q",
        capture_context="ctx",
    )


def test_writer_routes_go_forward_writes_through_root(tmp_path: Path) -> None:
    root = _init(tmp_path)
    src = tmp_path / "input.txt"
    src.write_text("hello", encoding="utf-8")
    result = write_local_source_capture_packet(data_root=root, **_writer_common(src))
    out = Path(result.output_directory)
    assert out == root.path / "raw" / raw_shard(result.packet.packet_id) / result.packet.packet_id
    assert (out / "manifest.json").is_file()


def test_writer_requires_exactly_one_target(tmp_path: Path) -> None:
    root = _init(tmp_path)
    src = tmp_path / "input.txt"
    src.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError):
        write_local_source_capture_packet(**_writer_common(src))  # neither
    with pytest.raises(ValueError):
        write_local_source_capture_packet(
            output_directory=tmp_path / "out", data_root=root, **_writer_common(src)
        )  # both


def test_writer_incumbent_output_directory_still_works(tmp_path: Path) -> None:
    # Backward compatibility: the legacy output_directory path is unchanged.
    src = tmp_path / "input.txt"
    src.write_text("hello", encoding="utf-8")
    out = tmp_path / "legacy_packet"
    result = write_local_source_capture_packet(output_directory=out, **_writer_common(src))
    assert Path(result.output_directory) == out.resolve()
    assert (out / "manifest.json").is_file()


# -- review hardening (DL-001..DL-005) -------------------------------------

def test_data_root_write_publishes_atomically_no_staging_leftover(tmp_path: Path) -> None:
    # DL-002: a successful data_root write publishes to raw/<packet_id> and
    # leaves no partial staging directory behind.
    root = _init(tmp_path)
    src = tmp_path / "input.txt"
    src.write_text("hello", encoding="utf-8")
    result = write_local_source_capture_packet(data_root=root, **_writer_common(src))
    out = Path(result.output_directory)
    assert out == root.path / "raw" / raw_shard(result.packet.packet_id) / result.packet.packet_id
    assert (out / "manifest.json").is_file()
    staging = root.path / ".staging"
    assert not staging.exists() or not any(staging.iterdir())


def test_publish_raw_packet_is_write_once(tmp_path: Path) -> None:
    # DL-002: the same packet_id cannot be published twice.
    root = _init(tmp_path)
    pid = generate_ulid()
    staging = root.stage_raw_packet(pid)
    (staging / "x").write_text("1", encoding="utf-8")
    published = root.publish_raw_packet(staging, pid)
    assert published == root.path / "raw" / raw_shard(pid) / pid
    with pytest.raises(DataLakeRootError):
        root.stage_raw_packet(pid)  # final already exists -> write-once


def test_packet_id_rejects_trailing_newline(tmp_path: Path) -> None:
    # DL-004: fullmatch, not ^...$ (which would accept a trailing newline).
    root = _init(tmp_path)
    with pytest.raises(DataLakeRootError):
        root.allocate_raw_packet_dir("A" * 26 + "\n")


def test_segment_rejects_trailing_newline(tmp_path: Path) -> None:
    # DL-004.
    root = _init(tmp_path)
    with pytest.raises(DataLakeRootError):
        root.append_record(
            subtree="derived", raw_anchor=generate_ulid(), lane="l", record_id="rec_01\n", data=b""
        )


def test_for_test_requires_absolute_path() -> None:
    # DL-005: test-mode bypasses the outside-repo guard but not the absolute-path guard.
    with pytest.raises(DataLakeRootError):
        DataLakeRoot.for_test("relative-lake")


def test_reverify_catches_root_identity_change(tmp_path: Path) -> None:
    # DL-003: a swapped/remounted root (same path, different marker identity) is
    # caught before any write.
    root = _init(tmp_path)
    marker = json.loads((root.path / ROOT_MARKER_FILENAME).read_text(encoding="utf-8"))
    marker["root_uuid"] = "DIFFERENTIDENTITY"
    (root.path / ROOT_MARKER_FILENAME).write_text(
        json.dumps(marker),
        encoding="utf-8",
    )
    with pytest.raises(DataLakeRootError):
        root.allocate_raw_packet_dir(generate_ulid())
    with pytest.raises(DataLakeRootError):
        root.append_record(
            subtree="derived", raw_anchor=generate_ulid(), lane="l", record_id="r", data=b""
        )


def test_within_rejects_symlinked_component(tmp_path: Path) -> None:
    # DL-003: a symlinked component under a lake-owned subtree is rejected.
    root = _init(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    # append_record now resolves to derived/<shard>/linked/l/r, so symlink the
    # shard component the traversal actually crosses (DL-003 rejects any symlinked
    # lake-owned component along the path).
    link = root.path / "derived" / raw_shard("linked")
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not supported in this environment")
    with pytest.raises(DataLakeRootError):
        root.append_record(
            subtree="derived", raw_anchor="linked", lane="l", record_id="r", data=b""
        )
