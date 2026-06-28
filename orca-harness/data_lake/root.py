"""Data Lake physical root: resolver, per-root identity marker, directory
skeleton, and the deterministic write-boundary guard.

Implements the foundation slice of the adopted decision contracts:

- physicality location: one operator-configured external data root
  (``ORCA_DATA_ROOT``) that resolves OUTSIDE the repo working tree; fail-closed.
- write-boundary enforcement: a single deterministic writer; write-once raw;
  append-only derived/ack; per-root UUID marker; atomic no-overwrite create.
- raw admission + key grammar: ``packet_id`` is an opaque Crockford-26 handle;
  raw container is ``raw/<packet_shard>/<packet_id>/`` -- an opaque deterministic
  shard prefix (``sha256(packet_id)[:3]``, 4096 buckets) physically fans the
  write-once packets out so no single directory grows unbounded; by-key reads
  recompute the shard, never look it up.
- derived layout: ``derived/<anchor_shard>/<raw-anchor>/<lane>/<record-id>``
  (acknowledgements likewise) -- the same opaque fanout -- and the split
  ``indexes/availability`` (content-free) vs ``indexes/derived_retrieval``
  (rebuildable, non-authoritative; created empty, population build-deferred).

This module is the current filesystem-incumbent foundation. It is not the
engine/backend selection record; that choice belongs to the Data Lake Storage
Contract physicalization boundary.

Threat model / accepted residual (DL-003): the write guard re-verifies the
root marker identity and rejects symlinked components immediately before each
write session, which catches a swapped/remounted root and static symlink
escapes. It does NOT fully exclude an *active* adversary racing same-host
symlink/reparse swaps between the check and the syscall; full exclusion needs
OS-level no-follow / directory-handle primitives and is out of scope for the v0
local single-operator deployment.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from harness_utils import generate_ulid, hash_file, utc_now_z

ROOT_MARKER_FILENAME = ".orca-data-root"
ROOT_MARKER_CONTRACT_VERSION = "v0"
_STAGING_DIRNAME = ".staging"

# v0 logical directory grammar. ``indexes/`` is split into a content-free
# availability subslot and a rebuildable, non-authoritative derived_retrieval
# subslot (created empty here; population is governance-gated/build-deferred).
LAKE_SUBDIRECTORIES: tuple[str, ...] = (
    "raw",
    "attachments",
    "derived",
    "acknowledgements",
    "indexes/availability",
    "indexes/derived_retrieval",
)

# packet_id grammar: incumbent Crockford base32, 26 chars (harness generate_ulid).
# Patterns are applied with fullmatch (not ^...$, which also accepts a trailing
# newline — DL-004).
_CROCKFORD_26 = re.compile(r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}")
# Conservative, collision-safe, traversal-proof path segments for raw anchors,
# lane namespaces, and record ids.
_SAFE_SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")

_APPENDABLE_SUBTREES = ("derived", "acknowledgements")


# Raw container physical fanout (decided 2026-06-25): raw packets live under a
# deterministic opaque shard prefix — raw/<packet_shard>/<packet_id>/ — so no
# single directory accumulates an unbounded packet count at scale. The shard is
# the first RAW_SHARD_HEX_WIDTH lowercase hex chars of sha256(packet_id): even
# spread, physical fanout ONLY (no family/date/identity/content meaning), and
# by-key lookup RECOMPUTES it from packet_id (never via an index).
RAW_SHARD_HEX_WIDTH = 3  # 4096 buckets


def raw_shard(packet_id: str) -> str:
    """Deterministic opaque shard segment for ``packet_id`` (physical fanout
    only; never stored as authority — every by-key read recomputes it)."""
    return hashlib.sha256(packet_id.encode("ascii")).hexdigest()[:RAW_SHARD_HEX_WIDTH]


class DataLakeRootError(Exception):
    """Fail-closed error. Raised instead of writing to an unsafe or unverified
    location; the caller must surface it, never silently fall back."""


def _detect_repo_root(start: Path) -> Path | None:
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


# The Orca repo working tree, detected from this module's location. The data
# root must resolve OUTSIDE it.
_ORCA_REPO_ROOT = _detect_repo_root(Path(__file__))


def _is_inside_repo(path: Path, repo_root: Path | None) -> bool:
    if repo_root is None:
        return False
    try:
        path.resolve().relative_to(repo_root.resolve())
        return True
    except ValueError:
        return False


def _validate_packet_id(packet_id: str) -> str:
    if not _CROCKFORD_26.fullmatch(packet_id):
        raise DataLakeRootError(
            f"invalid packet_id (expected Crockford base32, 26 chars): {packet_id!r}"
        )
    return packet_id


def _validate_segment(name: str, *, role: str) -> str:
    if name in {".", ".."} or not _SAFE_SEGMENT.fullmatch(name):
        raise DataLakeRootError(f"invalid {role} path segment: {name!r}")
    return name


def _read_marker(root: Path) -> dict:
    marker = root / ROOT_MARKER_FILENAME
    if not marker.is_file():
        raise DataLakeRootError(
            f"missing root marker {ROOT_MARKER_FILENAME!r}; not an initialized Orca data root: {root}"
        )
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DataLakeRootError(f"unreadable root marker at {marker}: {exc}") from exc
    if not isinstance(data, dict) or "root_uuid" not in data or "contract_version" not in data:
        raise DataLakeRootError(f"malformed root marker at {marker}")
    return data


def _write_marker(root: Path, *, root_uuid: str, label: str | None) -> None:
    payload = {
        "root_uuid": root_uuid,
        "contract_version": ROOT_MARKER_CONTRACT_VERSION,
        "label": label,
        "created_at": utc_now_z(),
    }
    (root / ROOT_MARKER_FILENAME).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _atomic_create(target: Path, data: bytes) -> None:
    """Create-only, no-overwrite, crash-tolerant publish of a single record.

    Writes a sibling temp file (fully written + fsync'd), then publishes it with
    an atomic *no-overwrite* primitive: ``os.link`` (POSIX + NTFS) which fails
    with ``FileExistsError`` if the target exists. On filesystems that cannot
    hardlink (e.g. exFAT/FAT on removable media), falls back to an exclusive
    ``O_EXCL`` create-write, which still guarantees no-overwrite (DL-001). Never
    uses ``os.replace`` (overwrite semantics).
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.parent / f".{target.name}.{generate_ulid()}.tmp"
    try:
        with open(tmp, "xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(tmp, target)  # atomic no-overwrite publish
        except FileExistsError as exc:
            raise DataLakeRootError(
                f"refusing to overwrite existing record (create-only): {target}"
            ) from exc
        except OSError:
            # Filesystem without hardlink support: exclusive create-write still
            # guarantees no-overwrite (crash-atomicity is reduced to a partial
            # record residual on such filesystems only).
            try:
                with open(target, "xb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            except FileExistsError as exc:
                raise DataLakeRootError(
                    f"refusing to overwrite existing record (create-only): {target}"
                ) from exc
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def _atomic_replace(target: Path, data: bytes) -> None:
    """Create-or-replace atomic write for a rebuildable index entry. Replace is
    acceptable here (unlike records) because indexes/ is disposable and is
    regenerated from committed raw."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.parent / f".{target.name}.{generate_ulid()}.tmp"
    with open(tmp, "xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, target)


def _availability_entry_from_raw(packet_id: str, container: Path) -> dict:
    """A content-free availability entry derived purely from committed raw, so
    the whole index is rebuildable from raw + hashes."""
    manifest = container / "manifest.json"
    if not manifest.is_file():
        raise DataLakeRootError(f"committed raw packet missing manifest.json: {packet_id}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    shard = raw_shard(packet_id)
    return {
        "packet_id": packet_id,
        "source_family": data.get("source_family"),
        "source_surface": data.get("source_surface"),
        "raw_path": f"raw/{shard}/{packet_id}",
        "manifest_relpath": f"raw/{shard}/{packet_id}/manifest.json",
        "manifest_sha256": hash_file(manifest),
    }


def _production_candidate(
    *, explicit: str | os.PathLike[str] | None, env: dict[str, str], config_path: Path | None
) -> str | None:
    """Production precedence only: explicit/per-run -> ORCA_DATA_ROOT env ->
    optional config file. A test root is never part of this chain."""
    if explicit is not None:
        return str(explicit)
    env_value = env.get("ORCA_DATA_ROOT")
    if env_value:
        return env_value
    if config_path is not None and config_path.is_file():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        value = config.get("data_root") if isinstance(config, dict) else None
        if value:
            return str(value)
    return None


def _preserved_path_parts(relative_packet_path: str, *, file_id: str) -> tuple[str, ...]:
    """Return canonical packet-relative POSIX path parts, or fail closed."""
    windows_path = PureWindowsPath(relative_packet_path)
    posix_path = PurePosixPath(relative_packet_path)
    if (
        "\\" in relative_packet_path
        or windows_path.drive
        or windows_path.root
        or posix_path.is_absolute()
        or relative_packet_path in {"", "."}
    ):
        raise DataLakeRootError(
            f"preserved path for {file_id!r} must be packet-relative POSIX: {relative_packet_path!r}"
        )
    parts = tuple(relative_packet_path.split("/"))
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise DataLakeRootError(
            f"preserved path for {file_id!r} has an unsafe segment: {relative_packet_path!r}"
        )
    return parts


@dataclass(frozen=True)
class LoadedRawPacket:
    """Result of a verified by-key raw read. ``manifest`` is the raw manifest as
    a plain dict -- the lake selects no spine schema, so the caller interprets
    it. ``bodies`` maps each preserved ``file_id`` to its bytes, re-hashed
    against the manifest sha256 on read (fail-closed on mismatch)."""

    container: Path
    manifest: dict[str, Any]
    bodies: dict[str, bytes]


class DataLakeRoot:
    """A resolved, verified Orca data-lake root. Construct via ``resolve``,
    ``initialize``, or ``for_test`` — never trust a bare path."""

    def __init__(self, path: Path, *, _verified: bool) -> None:
        if not _verified:
            raise DataLakeRootError("construct DataLakeRoot via resolve()/initialize()/for_test()")
        self._path = path
        # Identity captured at construction; re-checked before every write (DL-003).
        self._root_uuid = _read_marker(path)["root_uuid"]

    @property
    def path(self) -> Path:
        return self._path

    @property
    def root_uuid(self) -> str:
        return self._root_uuid

    # -- construction -------------------------------------------------------

    @classmethod
    def resolve(
        cls,
        *,
        explicit: str | os.PathLike[str] | None = None,
        env: dict[str, str] | None = None,
        config_path: Path | None = None,
        expected_uuid: str | None = None,
        repo_root: Path | None = _ORCA_REPO_ROOT,
    ) -> "DataLakeRoot":
        """Resolve the production data root, fail-closed. A test root is NEVER
        part of this chain (use ``for_test``). Refuses to write when the root is
        unset, relative, inside the repo, absent/unmounted, not a directory,
        missing/mismatched its marker, or not writable."""
        env = os.environ if env is None else env
        candidate = _production_candidate(explicit=explicit, env=env, config_path=config_path)
        if candidate is None:
            raise DataLakeRootError(
                "ORCA_DATA_ROOT is unset/unresolvable (no explicit root, env var, or config); "
                "refusing to write (fail-closed)."
            )
        path = Path(candidate)
        if not path.is_absolute():
            raise DataLakeRootError(f"data root must be an absolute path: {path}")
        if _is_inside_repo(path, repo_root):
            raise DataLakeRootError(f"data root must resolve OUTSIDE the repo working tree: {path}")
        if not path.exists():
            raise DataLakeRootError(
                f"data root does not exist / not mounted (removable media absent?): {path}"
            )
        if not path.is_dir():
            raise DataLakeRootError(f"data root is not a directory: {path}")
        marker = _read_marker(path)  # raises if missing/malformed
        if expected_uuid is not None and marker["root_uuid"] != expected_uuid:
            raise DataLakeRootError(
                "root marker identity mismatch (drive letter may have been reassigned): "
                f"expected {expected_uuid}, found {marker['root_uuid']}"
            )
        if not os.access(path, os.W_OK):
            raise DataLakeRootError(f"data root is not writable: {path}")
        return cls(path, _verified=True)

    @classmethod
    def initialize(
        cls,
        path: str | os.PathLike[str],
        *,
        label: str | None = None,
        root_uuid: str | None = None,
        repo_root: Path | None = _ORCA_REPO_ROOT,
    ) -> "DataLakeRoot":
        """Create (or verify) the root: marker + directory skeleton. Idempotent
        when a well-formed marker already exists; refuses to claim a non-empty
        directory that lacks a marker."""
        path = Path(path)
        if not path.is_absolute():
            raise DataLakeRootError(f"data root must be an absolute path: {path}")
        if _is_inside_repo(path, repo_root):
            raise DataLakeRootError(f"data root must be OUTSIDE the repo working tree: {path}")
        return cls._init_at(path, label=label, root_uuid=root_uuid)

    @classmethod
    def for_test(cls, path: str | os.PathLike[str], *, label: str = "test") -> "DataLakeRoot":
        """TEST-MODE ONLY. Initializes a root at ``path`` bypassing the
        outside-repo guard (tests use temp dirs that live inside the repo). The
        path must still be absolute (DL-005). Never reachable from production
        ``resolve``."""
        path = Path(path)
        if not path.is_absolute():
            raise DataLakeRootError(f"for_test path must be absolute: {path}")
        return cls._init_at(path, label=label, root_uuid=None)

    @classmethod
    def _init_at(cls, path: Path, *, label: str | None, root_uuid: str | None) -> "DataLakeRoot":
        marker = path / ROOT_MARKER_FILENAME
        if path.exists():
            if not path.is_dir():
                raise DataLakeRootError(f"data root path is not a directory: {path}")
            if marker.is_file():
                _read_marker(path)  # verify the existing marker is well-formed
            elif any(path.iterdir()):
                raise DataLakeRootError(
                    f"refusing to initialize a non-empty directory that lacks a root marker: {path}"
                )
            else:
                _write_marker(path, root_uuid=root_uuid or generate_ulid(), label=label)
        else:
            path.mkdir(parents=True, exist_ok=False)
            _write_marker(path, root_uuid=root_uuid or generate_ulid(), label=label)
        for sub in LAKE_SUBDIRECTORIES:
            (path / sub).mkdir(parents=True, exist_ok=True)
        return cls(path, _verified=True)

    # -- write-session guards ----------------------------------------------

    def _reverify(self) -> None:
        """Re-check root identity immediately before a write session: the path is
        still a directory carrying the same marker root_uuid. Catches a
        swapped/remounted root (e.g. drive-letter reassignment to a different
        volume). See the module-level accepted residual for active syscall races."""
        if not self._path.is_dir():
            raise DataLakeRootError(f"data root is no longer a directory: {self._path}")
        if _read_marker(self._path).get("root_uuid") != self._root_uuid:
            raise DataLakeRootError(f"data root identity changed since resolution: {self._path}")

    def _within(self, *parts: str) -> Path:
        """Resolve a lake-owned path and assert containment, rejecting symlinked
        components along the way (pre-resolution)."""
        probe = self._path
        for part in parts:
            probe = probe / part
            if probe.is_symlink():
                raise DataLakeRootError(f"refusing symlinked component under the data root: {probe}")
        target = self._path.joinpath(*parts).resolve()
        try:
            target.relative_to(self._path.resolve())
        except ValueError as exc:
            raise DataLakeRootError(f"refusing path escape outside the data root: {target}") from exc
        return target

    # -- guarded writes -----------------------------------------------------

    def allocate_raw_packet_dir(self, packet_id: str) -> Path:
        """Create the write-once raw packet container
        ``raw/<packet_shard>/<packet_id>/`` and return it. Create-only: fails if it
        already exists. For atomic packet
        publication (a partial packet never appears under ``raw/``), prefer
        ``stage_raw_packet`` + ``publish_raw_packet`` instead."""
        self._reverify()
        _validate_packet_id(packet_id)
        container = self._within("raw", raw_shard(packet_id), packet_id)
        container.parent.mkdir(parents=True, exist_ok=True)
        try:
            container.mkdir(parents=False, exist_ok=False)
        except FileExistsError as exc:
            raise DataLakeRootError(
                f"raw packet container already exists (write-once): {container}"
            ) from exc
        return container

    def stage_raw_packet(self, packet_id: str) -> Path:
        """Reserve a non-authoritative staging directory for an incumbent packet.
        The completed staging dir is published atomically to
        ``raw/<packet_shard>/<packet_id>`` by ``publish_raw_packet``, so a partial
        packet never appears under ``raw/`` (DL-002)."""
        self._reverify()
        _validate_packet_id(packet_id)
        final = self._within("raw", raw_shard(packet_id), packet_id)
        if final.exists():
            raise DataLakeRootError(f"raw packet container already exists (write-once): {final}")
        staging_parent = self._path / _STAGING_DIRNAME
        staging_parent.mkdir(parents=True, exist_ok=True)
        staging = staging_parent / generate_ulid()
        staging.mkdir(parents=False, exist_ok=False)
        return staging

    def publish_raw_packet(self, staging_dir: Path, packet_id: str) -> Path:
        """Atomically publish a completed staging directory to
        ``raw/<packet_shard>/<packet_id>`` (write-once)."""
        self._reverify()
        _validate_packet_id(packet_id)
        final = self._within("raw", raw_shard(packet_id), packet_id)
        final.parent.mkdir(parents=True, exist_ok=True)
        if final.exists():
            raise DataLakeRootError(f"raw packet container already exists (write-once): {final}")
        try:
            os.rename(staging_dir, final)  # atomic same-filesystem directory publish
        except OSError as exc:
            raise DataLakeRootError(f"failed to publish raw packet to {final}: {exc}") from exc
        return final

    def append_record(
        self, *, subtree: str, raw_anchor: str, lane: str, record_id: str, data: bytes
    ) -> Path:
        """Append-only create of a derived or acknowledgement record at
        ``<subtree>/<anchor_shard>/<raw_anchor>/<lane>/<record_id>`` (the anchor
        shard is recomputed from ``raw_anchor``). Refuses overwrite."""
        if subtree not in _APPENDABLE_SUBTREES:
            raise DataLakeRootError(
                f"append_record subtree must be one of {_APPENDABLE_SUBTREES}: {subtree!r}"
            )
        self._reverify()
        _validate_segment(raw_anchor, role="raw_anchor")
        _validate_segment(lane, role="lane")
        _validate_segment(record_id, role="record_id")
        target = self._within(subtree, raw_shard(raw_anchor), raw_anchor, lane, record_id)
        _atomic_create(target, data)
        return target

    def append_record_set(
        self,
        *,
        subtree: str,
        raw_anchor: str,
        record_id: str,
        members: dict[str, bytes],
        completion_lane: str,
    ) -> dict[str, Path]:
        """Append a set of sibling records as one derivation with all-or-nothing
        completion semantics. Writes every member record, then a completion marker
        (in ``completion_lane``) listing the member lanes -- the marker is the last
        create in process order. A crash before the marker leaves no marker; a
        filesystem crash around final publish may still leave any subset of
        directory entries durable, so consumers must use
        ``is_record_set_complete`` to reject marker-present/member-missing sets.
        Fail-closed preflight: none of the member targets nor the
        marker may already exist, so a colliding ``record_id`` never produces a new
        partial. Returns ``{member_lane: path}`` (the marker path is not returned).

        This gives DETECTABLE completeness, not crash-atomic publication: each
        member file is individually create-only and a consumer must consult the
        marker (or ``is_record_set_complete``) to trust the set; true cross-file
        atomic publish is not available for siblings in distinct lane dirs."""
        if subtree not in _APPENDABLE_SUBTREES:
            raise DataLakeRootError(
                f"append_record_set subtree must be one of {_APPENDABLE_SUBTREES}: {subtree!r}"
            )
        if not members:
            raise DataLakeRootError("append_record_set requires at least one member record")
        if completion_lane in members:
            raise DataLakeRootError(
                f"completion_lane {completion_lane!r} must not collide with a member lane"
            )
        self._reverify()
        _validate_segment(raw_anchor, role="raw_anchor")
        _validate_segment(record_id, role="record_id")
        _validate_segment(completion_lane, role="completion_lane")
        for lane in members:
            _validate_segment(lane, role="lane")

        anchor_shard = raw_shard(raw_anchor)
        member_targets = {
            lane: self._within(subtree, anchor_shard, raw_anchor, lane, record_id)
            for lane in members
        }
        marker_target = self._within(subtree, anchor_shard, raw_anchor, completion_lane, record_id)
        existing = [t for t in (*member_targets.values(), marker_target) if t.exists()]
        if existing:
            raise DataLakeRootError(
                "refusing partial record set; a member or marker already exists for "
                f"record_id {record_id!r}: {', '.join(str(p) for p in existing)}"
            )

        written: dict[str, Path] = {}
        member_sha256: dict[str, str] = {}
        for lane, data in members.items():
            _atomic_create(member_targets[lane], data)
            written[lane] = member_targets[lane]
            # The lake computes each member's content sha256 from the bytes IT writes (never
            # caller-supplied): the marker becomes a derivation-time content-integrity manifest,
            # trustworthy by construction.
            member_sha256[lane] = hashlib.sha256(data).hexdigest()
        marker_body = (
            json.dumps(
                {
                    "record_id": record_id,
                    "member_lanes": sorted(members),
                    "member_sha256": member_sha256,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        _atomic_create(marker_target, marker_body.encode("utf-8"))
        return written

    def is_record_set_complete(
        self, *, subtree: str, raw_anchor: str, record_id: str, completion_lane: str
    ) -> bool:
        """True iff the completion marker for this set exists AND every member lane
        it names has its record present. Lets a consumer reject a partial
        (crash-interrupted or in-flight) derivation; fail-closed on any anomaly."""
        if subtree not in _APPENDABLE_SUBTREES:
            raise DataLakeRootError(
                f"is_record_set_complete subtree must be one of {_APPENDABLE_SUBTREES}: {subtree!r}"
            )
        self._reverify()
        _validate_segment(raw_anchor, role="raw_anchor")
        _validate_segment(record_id, role="record_id")
        _validate_segment(completion_lane, role="completion_lane")
        anchor_shard = raw_shard(raw_anchor)
        marker = self._within(subtree, anchor_shard, raw_anchor, completion_lane, record_id)
        if not marker.is_file():
            return False
        try:
            body = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        if not isinstance(body, dict) or body.get("record_id") != record_id:
            return False
        member_lanes = body.get("member_lanes")
        if not isinstance(member_lanes, list) or not member_lanes:
            return False
        for lane in member_lanes:
            if not isinstance(lane, str):
                return False
            try:
                _validate_segment(lane, role="lane")
            except DataLakeRootError:
                return False
            if not self._within(subtree, anchor_shard, raw_anchor, lane, record_id).is_file():
                return False
        return True

    def read_record_set_member_sha256(
        self,
        *,
        subtree: str,
        raw_anchor: str,
        record_id: str,
        completion_lane: str,
        member_lane: str,
    ) -> str | None:
        """Return a record-set member's derivation-time content sha256 committed in the completion
        marker, or ``None`` ONLY when the marker file is ABSENT (a legitimate legacy
        ``append_record`` record that never wrote a marker -- the caller's stitch-time fallback).

        Fail-closed on corruption -- this is the integrity crux (never collapse a damaged marker
        into the "old record" None): a marker that is PRESENT but malformed (unreadable / not a JSON
        object / wrong ``record_id``), or present but whose ``member_sha256`` is missing, not a
        mapping, lacks ``member_lane``, or carries a non-string sha, RAISES ``DataLakeRootError``.
        Every record written via ``append_record_set`` has a well-formed marker, so a new record
        whose marker cannot yield its sha must surface, never silently downgrade. Validates segments
        like the sibling marker methods."""
        if subtree not in _APPENDABLE_SUBTREES:
            raise DataLakeRootError(
                f"read_record_set_member_sha256 subtree must be one of {_APPENDABLE_SUBTREES}: {subtree!r}"
            )
        self._reverify()
        _validate_segment(raw_anchor, role="raw_anchor")
        _validate_segment(record_id, role="record_id")
        _validate_segment(completion_lane, role="completion_lane")
        _validate_segment(member_lane, role="member_lane")
        anchor_shard = raw_shard(raw_anchor)
        marker = self._within(subtree, anchor_shard, raw_anchor, completion_lane, record_id)
        if not marker.is_file():
            # Marker ABSENT: the only legitimate None (legacy markerless record).
            return None
        try:
            body = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DataLakeRootError(
                f"record-set marker present but unreadable/malformed: {marker}: {exc}"
            ) from exc
        if not isinstance(body, dict) or body.get("record_id") != record_id:
            raise DataLakeRootError(
                f"record-set marker present but malformed (record_id mismatch or non-object): {marker}"
            )
        member_sha256 = body.get("member_sha256")
        if not isinstance(member_sha256, dict):
            raise DataLakeRootError(
                f"record-set marker present but missing a member_sha256 mapping: {marker}"
            )
        sha = member_sha256.get(member_lane)
        if not isinstance(sha, str) or not sha:
            raise DataLakeRootError(
                f"record-set marker present but missing member_sha256 for lane {member_lane!r}: {marker}"
            )
        return sha

    def record_path(self, *, subtree: str, raw_anchor: str, lane: str, record_id: str) -> Path:
        """Resolve a derived/ack record's on-disk path BY KEY (sharded), without
        writing. The anchor shard is recomputed from ``raw_anchor`` (never looked
        up); the returned path may or may not exist, so callers must check it."""
        if subtree not in _APPENDABLE_SUBTREES:
            raise DataLakeRootError(
                f"record_path subtree must be one of {_APPENDABLE_SUBTREES}: {subtree!r}"
            )
        _validate_segment(raw_anchor, role="raw_anchor")
        _validate_segment(lane, role="lane")
        _validate_segment(record_id, role="record_id")
        return self._within(subtree, raw_shard(raw_anchor), raw_anchor, lane, record_id)

    def lane_dir(self, *, subtree: str, raw_anchor: str, lane: str) -> Path:
        """Resolve a derived/ack lane DIRECTORY by key (sharded), without writing.
        Callers iterate it to read the lane's records; it may not exist."""
        if subtree not in _APPENDABLE_SUBTREES:
            raise DataLakeRootError(
                f"lane_dir subtree must be one of {_APPENDABLE_SUBTREES}: {subtree!r}"
            )
        _validate_segment(raw_anchor, role="raw_anchor")
        _validate_segment(lane, role="lane")
        return self._within(subtree, raw_shard(raw_anchor), raw_anchor, lane)

    # -- availability index (content-free, rebuildable) ---------------------

    def record_availability(self, packet_id: str) -> Path:
        """Record the content-free committed-by-key availability fact for a
        committed raw packet, derived solely from raw/<packet_id>/manifest.json
        (so the whole index is rebuildable). Index entry: create-or-replace."""
        self._reverify()
        _validate_packet_id(packet_id)
        container = self._within("raw", raw_shard(packet_id), packet_id)
        if not container.is_dir():
            raise DataLakeRootError(
                f"cannot record availability; raw packet not committed: {packet_id}"
            )
        entry = _availability_entry_from_raw(packet_id, container)
        target = self._within("indexes", "availability", f"{packet_id}.json")
        _atomic_replace(target, (json.dumps(entry, indent=2, sort_keys=True) + "\n").encode("utf-8"))
        return target

    def find_packet(self, packet_id: str) -> Path | None:
        """Return the committed raw packet container by key, or None."""
        _validate_packet_id(packet_id)
        container = self._within("raw", raw_shard(packet_id), packet_id)
        return container if container.is_dir() else None

    def load_raw_packet(self, packet_id: str) -> LoadedRawPacket:
        """Verified by-key raw read -- the read half, symmetric to the write
        guard. Resolve ``raw/<packet_id>/``, read the manifest, and return each
        preserved file's bytes re-hashed against the manifest sha256. Fail-closed
        on a missing packet/manifest/file, a size or sha256 mismatch, or a
        preserved path that is absolute or escapes the container. The lake selects
        no spine schema: the manifest is returned as a plain dict for the caller
        to interpret."""
        self._reverify()
        container = self.find_packet(packet_id)
        if container is None:
            raise DataLakeRootError(f"raw packet not committed: {packet_id}")
        manifest_path = container / "manifest.json"
        if not manifest_path.is_file():
            raise DataLakeRootError(f"committed raw packet missing manifest.json: {packet_id}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DataLakeRootError(f"unreadable raw manifest for packet {packet_id}: {exc}") from exc
        if not isinstance(manifest, dict):
            raise DataLakeRootError(f"raw manifest is not a JSON object: {manifest_path}")
        preserved_files = manifest.get("preserved_files")
        if not isinstance(preserved_files, list) or not preserved_files:
            raise DataLakeRootError(
                f"raw manifest preserved_files must be a non-empty list: {packet_id}"
            )
        bodies: dict[str, bytes] = {}
        container_root = container.resolve()
        for index, preserved in enumerate(preserved_files):
            if not isinstance(preserved, dict):
                raise DataLakeRootError(
                    f"raw manifest preserved_files[{index}] must be a JSON object: {packet_id}"
                )
            file_id = preserved.get("file_id")
            if not isinstance(file_id, str) or not file_id:
                raise DataLakeRootError(
                    f"raw manifest preserved_files[{index}].file_id is missing or invalid: {packet_id}"
                )
            if file_id in bodies:
                raise DataLakeRootError(f"duplicate preserved file_id {file_id!r}: {packet_id}")
            relative_packet_path = preserved.get("relative_packet_path")
            if not isinstance(relative_packet_path, str):
                raise DataLakeRootError(
                    f"raw manifest preserved file {file_id!r} missing relative_packet_path: {packet_id}"
                )
            parts = _preserved_path_parts(relative_packet_path, file_id=file_id)
            file_path = self._within("raw", raw_shard(packet_id), packet_id, *parts)
            try:
                file_path.relative_to(container_root)
            except ValueError as exc:
                raise DataLakeRootError(
                    f"preserved path escapes raw packet container for {file_id!r}: "
                    f"{relative_packet_path!r}"
                ) from exc
            if not file_path.is_file():
                raise DataLakeRootError(
                    f"preserved file {file_id!r} missing at {relative_packet_path!r}: {packet_id}"
                )
            try:
                body = file_path.read_bytes()
            except OSError as exc:
                raise DataLakeRootError(
                    f"unreadable preserved file {file_id!r} at {relative_packet_path!r}: {packet_id}: {exc}"
                ) from exc
            expected_size = preserved.get("size_bytes")
            if type(expected_size) is not int or expected_size < 0:
                raise DataLakeRootError(
                    f"raw manifest preserved file {file_id!r} missing valid size_bytes: {packet_id}"
                )
            if len(body) != expected_size:
                raise DataLakeRootError(
                    f"preserved file size mismatch for {file_id!r} "
                    f"(read {len(body)}, manifest {expected_size}): {packet_id}"
                )
            expected_sha = preserved.get("sha256")
            if not isinstance(expected_sha, str) or not expected_sha:
                raise DataLakeRootError(
                    f"raw manifest preserved file {file_id!r} missing sha256: {packet_id}"
                )
            actual_sha = hashlib.sha256(body).hexdigest()
            if actual_sha != expected_sha:
                raise DataLakeRootError(
                    f"preserved file sha256 mismatch for {file_id!r} "
                    f"(recomputed {actual_sha}, manifest {expected_sha}): {packet_id}"
                )
            bodies[file_id] = body
        return LoadedRawPacket(container=container, manifest=manifest, bodies=bodies)

    def read_availability(self, packet_id: str) -> dict | None:
        """Return the availability entry for a packet by key, or None."""
        _validate_packet_id(packet_id)
        target = self._within("indexes", "availability", f"{packet_id}.json")
        if not target.is_file():
            return None
        return json.loads(target.read_text(encoding="utf-8"))

    def list_available(self, *, source_family: str | None = None) -> list[str]:
        """List committed packet ids by key, optionally filtered by source family."""
        avail = self._path / "indexes" / "availability"
        if not avail.is_dir():
            return []
        out: list[str] = []
        for entry_file in sorted(avail.glob("*.json")):
            entry = json.loads(entry_file.read_text(encoding="utf-8"))
            if source_family is None or entry.get("source_family") == source_family:
                out.append(entry["packet_id"])
        return out

    def rebuild_availability(self) -> int:
        """Rebuild indexes/availability entirely from committed raw packets
        (delete + regenerate), proving the index is non-authoritative and
        rebuildable. Returns the number of packets indexed."""
        self._reverify()
        avail = self._path / "indexes" / "availability"
        if avail.is_dir():
            for entry_file in avail.glob("*.json"):
                entry_file.unlink()
        avail.mkdir(parents=True, exist_ok=True)
        raw_dir = self._path / "raw"
        count = 0
        if raw_dir.is_dir():
            for shard_dir in sorted(raw_dir.iterdir()):
                if not shard_dir.is_dir():
                    continue
                for container in sorted(shard_dir.iterdir()):
                    if (
                        container.is_dir()
                        and _CROCKFORD_26.fullmatch(container.name)
                        # A packet sitting in the wrong shard dir is corruption/
                        # misplacement: skip it rather than record a wrong-path
                        # availability entry (failure stays visible as absence).
                        and shard_dir.name == raw_shard(container.name)
                        and (container / "manifest.json").is_file()
                    ):
                        self.record_availability(container.name)
                        count += 1
        return count

    def relocate_to_sharded(self) -> int:
        """One-time migration to the sharded layout: move any legacy flat
        ``<subtree>/<key>/`` container -- a raw packet under ``raw/``, or a
        raw-anchor-first ``derived/``/``acknowledgements/`` subtree -- to
        ``<subtree>/<shard>/<key>/``. Idempotent and re-runnable: already-sharded
        entries are not direct children, so they are skipped. A flat entry whose
        sharded target ALSO exists is a collision and FAILS CLOSED (write-once
        material is never overwritten and a hidden duplicate is never tolerated).
        Returns the total relocated. Run ``rebuild_availability`` afterwards so the
        index points at the new paths."""
        self._reverify()
        return sum(
            self._relocate_subtree_to_sharded(subtree)
            for subtree in ("raw", *_APPENDABLE_SUBTREES)
        )

    def _relocate_subtree_to_sharded(self, subtree: str) -> int:
        base = self._path / subtree
        if not base.is_dir():
            return 0
        moved = 0
        for child in sorted(base.iterdir()):
            # A legacy flat entry is a direct child whose name is a full key
            # (Crockford-26 packet_id / raw-anchor). Shard dirs are short hex,
            # so they are not Crockford-26 and are skipped.
            if not (child.is_dir() and _CROCKFORD_26.fullmatch(child.name)):
                continue
            key = child.name
            target = self._within(subtree, raw_shard(key), key)
            if target.exists():
                raise DataLakeRootError(
                    f"relocate collision under {subtree}/: both flat {subtree}/{key}/ "
                    f"and sharded {target} exist; resolve the duplicate before "
                    f"migrating (write-once material is never overwritten)"
                )
            target.parent.mkdir(parents=True, exist_ok=True)
            os.rename(child, target)  # atomic same-fs move; bytes/hashes unchanged
            moved += 1
        return moved
