from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError, LoadedRawPacket, raw_shard
from harness_utils import generate_ulid
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _capture(root: DataLakeRoot, tmp_path: Path, body: bytes):
    # A committed raw packet in the lake. Any family works; the loader is
    # spine-agnostic. The capture path is the one already on main (data_root seam).
    src = tmp_path / "blob.bin"
    src.write_bytes(body)
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="s",
        source_locator=known_fact("https://example.com/x"),
        decision_question="q",
        capture_context="loader test",
    )


def _manifest_path(root: DataLakeRoot, packet_id: str) -> Path:
    container = root.find_packet(packet_id)
    assert container is not None
    return container / "manifest.json"


def _read_manifest(root: DataLakeRoot, packet_id: str) -> dict:
    return json.loads(_manifest_path(root, packet_id).read_text(encoding="utf-8"))


def _write_manifest(root: DataLakeRoot, packet_id: str, manifest: dict) -> None:
    _manifest_path(root, packet_id).write_text(
        f"{json.dumps(manifest, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )


def test_load_raw_packet_returns_verified_bodies(tmp_path: Path) -> None:
    # The read half: find raw by key, verify the seal, hand back bytes by file_id.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    body = b"AAAAAAAAAAAAAAAA"
    pid = _capture(root, tmp_path, body).packet.packet_id

    loaded = root.load_raw_packet(pid)
    assert isinstance(loaded, LoadedRawPacket)
    assert loaded.container == root.path / "raw" / raw_shard(pid) / pid
    assert loaded.manifest["packet_id"] == pid
    assert list(loaded.bodies.values()) == [body]
    # bodies are keyed exactly by the manifest's preserved-file ids
    assert set(loaded.bodies) == {pf["file_id"] for pf in loaded.manifest["preserved_files"]}


def test_load_raw_packet_detects_sha256_tampering(tmp_path: Path) -> None:
    # Same length, different content -> size check passes, sha256 check catches it.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture(root, tmp_path, b"AAAAAAAAAAAAAAAA").packet.packet_id

    container = root.find_packet(pid)
    assert container is not None
    next((container / "raw").iterdir()).write_bytes(b"AAAAAAAAAAAAAAAB")

    with pytest.raises(DataLakeRootError):
        root.load_raw_packet(pid)


def test_load_raw_packet_detects_missing_file(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture(root, tmp_path, b"some bytes").packet.packet_id

    container = root.find_packet(pid)
    assert container is not None
    next((container / "raw").iterdir()).unlink()

    with pytest.raises(DataLakeRootError):
        root.load_raw_packet(pid)


def test_load_raw_packet_unknown_key_fails_closed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    with pytest.raises(DataLakeRootError):
        root.load_raw_packet(generate_ulid())


def test_load_raw_packet_rejects_manifest_without_preserved_files(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture(root, tmp_path, b"some bytes").packet.packet_id
    manifest = _read_manifest(root, pid)
    del manifest["preserved_files"]
    _write_manifest(root, pid, manifest)

    with pytest.raises(DataLakeRootError, match="preserved_files"):
        root.load_raw_packet(pid)


@pytest.mark.parametrize("field", ["sha256", "size_bytes"])
def test_load_raw_packet_rejects_missing_integrity_fields(tmp_path: Path, field: str) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture(root, tmp_path, b"some bytes").packet.packet_id
    manifest = _read_manifest(root, pid)
    del manifest["preserved_files"][0][field]
    _write_manifest(root, pid, manifest)

    with pytest.raises(DataLakeRootError, match=field):
        root.load_raw_packet(pid)


@pytest.mark.parametrize(
    "unsafe_path",
    ["../escape.bin", "raw\\01_blob.bin", "C:raw/01_blob.bin", "/raw/01_blob.bin", ""],
)
def test_load_raw_packet_rejects_unsafe_preserved_paths(
    tmp_path: Path,
    unsafe_path: str,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture(root, tmp_path, b"some bytes").packet.packet_id
    manifest = _read_manifest(root, pid)
    manifest["preserved_files"][0]["relative_packet_path"] = unsafe_path
    _write_manifest(root, pid, manifest)

    with pytest.raises(DataLakeRootError):
        root.load_raw_packet(pid)


def test_load_raw_packet_blocks_preserved_path_escape_to_another_packet(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first_pid = _capture(root, tmp_path, b"first body").packet.packet_id
    second_pid = _capture(root, tmp_path, b"second body").packet.packet_id
    first_manifest = _read_manifest(root, first_pid)
    second_preserved = _read_manifest(root, second_pid)["preserved_files"][0]

    first_preserved = first_manifest["preserved_files"][0]
    first_preserved["relative_packet_path"] = f"../{second_pid}/{second_preserved['relative_packet_path']}"
    # Match the foreign bytes so only the packet-container boundary can catch this.
    first_preserved["size_bytes"] = second_preserved["size_bytes"]
    first_preserved["sha256"] = second_preserved["sha256"]
    _write_manifest(root, first_pid, first_manifest)

    with pytest.raises(DataLakeRootError):
        root.load_raw_packet(first_pid)


def test_load_raw_packet_corrupted_manifest_json_fails_closed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture(root, tmp_path, b"some bytes").packet.packet_id
    _manifest_path(root, pid).write_text("{", encoding="utf-8")

    with pytest.raises(DataLakeRootError, match="unreadable raw manifest"):
        root.load_raw_packet(pid)
