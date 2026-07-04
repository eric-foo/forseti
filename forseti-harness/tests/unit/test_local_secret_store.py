from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from source_capture.local_secret_store import (
    assert_under_root,
    label_to_filename,
    read_store_payload,
    write_sidecar,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"local_secret_store_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_label_to_filename_appends_suffix_and_accepts_clean_labels() -> None:
    assert label_to_filename("free-example", kind="auth-state") == "free-example.json"
    assert label_to_filename("already.json", kind="auth-state") == "already.json"


def test_label_to_filename_rejects_traversal_and_separators() -> None:
    for bad in ("../outside", "nested/cred", "..\\win", "has space", ".hidden"):
        with pytest.raises(ValueError, match="reddit-credential label"):
            label_to_filename(bad, kind="reddit-credential")


def test_label_to_filename_rejects_reserved_sidecar_suffix() -> None:
    # A data filename ending in the sidecar suffix could shadow another label's sidecar.
    for bad in ("script-app.meta", "foo.meta.json"):
        with pytest.raises(ValueError, match="reserved"):
            label_to_filename(bad, kind="reddit-credential")


def test_assert_under_root_rejects_escape_and_allows_inside(scratch_dir: Path) -> None:
    root = scratch_dir / "store"
    root.mkdir()
    with pytest.raises(ValueError, match="reddit-credential path"):
        assert_under_root(root.parent / "outside.json", root, kind="reddit-credential")
    # A path under the root must not raise.
    assert_under_root(root / "inside.json", root, kind="reddit-credential")


def test_assert_under_root_rejects_symlinked_root(scratch_dir: Path) -> None:
    real = scratch_dir / "real_store"
    real.mkdir()
    link = scratch_dir / "linked_store"
    try:
        link.symlink_to(real, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation not permitted on this host")
    with pytest.raises(ValueError, match="must not be a symlink"):
        assert_under_root(link / "x.json", link, kind="reddit-credential")


def test_read_store_payload_enforces_existence_size_and_shape(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        read_store_payload(scratch_dir / "missing.json", max_bytes=100, kind="reddit-credential", label="missing")

    empty = scratch_dir / "empty.json"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="is empty"):
        read_store_payload(empty, max_bytes=100, kind="reddit-credential", label="empty")

    big = scratch_dir / "big.json"
    big.write_text(json.dumps({"k": "v" * 200}), encoding="utf-8")
    with pytest.raises(ValueError, match="byte cap"):
        read_store_payload(big, max_bytes=10, kind="reddit-credential", label="big")

    not_json = scratch_dir / "notjson.json"
    not_json.write_text("not json at all", encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        read_store_payload(not_json, max_bytes=1000, kind="reddit-credential", label="notjson")

    not_object = scratch_dir / "list.json"
    not_object.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    with pytest.raises(ValueError, match="must be a JSON object"):
        read_store_payload(not_object, max_bytes=1000, kind="reddit-credential", label="list")

    ok = scratch_dir / "ok.json"
    ok.write_text(json.dumps({"client_id": "x"}), encoding="utf-8")
    assert read_store_payload(ok, max_bytes=1000, kind="reddit-credential", label="ok") == {"client_id": "x"}


def test_write_sidecar_refuses_overwrite(scratch_dir: Path) -> None:
    sidecar = scratch_dir / "x.meta.json"
    write_sidecar(sidecar, payload={"a": 1}, kind="reddit-credential", label="x")
    assert json.loads(sidecar.read_text(encoding="utf-8")) == {"a": 1}
    with pytest.raises(ValueError, match="already exists"):
        write_sidecar(sidecar, payload={"a": 2}, kind="reddit-credential", label="x")
