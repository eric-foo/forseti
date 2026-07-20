"""Disposable SQLite source inventory for incremental lake-map generation.

The database is builder state, never lake authority and never a reader surface.
It stores bytes already read from append-only ``derived/`` and
``acknowledgements/`` records so an ordinary refresh can reconstruct the map
without reopening every unchanged small file. Deleting it causes a cold
inventory bootstrap on the next refresh.
"""
from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRootError

STATE_SCHEMA_VERSION = 1
STATE_PARTS = (
    "indexes",
    "derived_retrieval",
    "silver_vault",
    "core",
    "cache",
    "source_inventory.sqlite3",
)


@dataclass(frozen=True)
class StoredSourceRecord:
    subtree: str
    raw_anchor: str
    lane: str
    record_id: str
    relative_path: str
    ref_key: str
    body: bytes
    sha256: str
    classification_cache_key: str | None


class IncrementalSourceInventory:
    """One transaction over the disposable incremental source inventory."""

    def __init__(
        self,
        root,
        *,
        reset: bool = False,
        persistent: bool = True,
    ) -> None:
        self.root = root
        self.path = root._within(*STATE_PARTS)
        self.persistent = persistent
        self._connection: sqlite3.Connection | None = None
        self._reset = reset
        self._seen: set[str] = set()
        self._new = 0
        self._reused = 0
        self._metadata_refreshed = 0
        self._body_reads = 0

    def __enter__(self) -> "IncrementalSourceInventory":
        self.root._reverify()
        if self.persistent:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            database = str(self.path)
        else:
            database = ":memory:"
        try:
            connection = sqlite3.connect(
                database,
                timeout=0.0,
                isolation_level=None,
            )
            connection.execute("PRAGMA journal_mode=DELETE")
            connection.execute("PRAGMA synchronous=FULL")
            self._connection = connection
            if not self.persistent and self.path.is_file() and not self._reset:
                disk = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)
                try:
                    disk.backup(connection)
                finally:
                    disk.close()
            connection.execute("BEGIN IMMEDIATE")
            self._create_schema()
            if self._reset:
                self._reset_state()
        except DataLakeRootError:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
            raise
        except sqlite3.DatabaseError as exc:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
            raise DataLakeRootError(
                "lake-map source inventory is unavailable or another updater is "
                f"active: {exc}; retry later, or use --full-rebuild to recreate "
                "disposable updater state"
            ) from exc
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self._connection is None:
            return
        try:
            if exc_type is None and self.persistent:
                self._connection.execute("COMMIT")
            else:
                self._connection.execute("ROLLBACK")
        finally:
            self._connection.close()
            self._connection = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError("incremental source inventory is not open")
        return self._connection

    def _create_schema(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS source_records (
                relative_path TEXT PRIMARY KEY,
                subtree TEXT NOT NULL,
                raw_anchor TEXT NOT NULL,
                lane TEXT NOT NULL,
                record_id TEXT NOT NULL,
                ref_key TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                mtime_ns INTEGER NOT NULL,
                sha256 TEXT NOT NULL,
                body BLOB NOT NULL,
                classification_cache_key TEXT
            )
            """
        )
        self.connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS source_records_ref_key
                ON source_records(subtree, ref_key)
            """
        )
        row = self.connection.execute(
            "SELECT value FROM metadata WHERE key = 'state_schema_version'"
        ).fetchone()
        if row is None:
            self.connection.execute(
                "INSERT INTO metadata(key, value) VALUES(?, ?)",
                ("state_schema_version", str(STATE_SCHEMA_VERSION)),
            )
        elif row[0] != str(STATE_SCHEMA_VERSION):
            raise DataLakeRootError(
                "unsupported lake-map source inventory schema "
                f"{row[0]!r}; stop the updater, remove only the disposable "
                "source_inventory.sqlite3 file, then run a full rebuild"
            )

    def _reset_state(self) -> None:
        """Clear disposable state only while holding SQLite's writer lock."""
        self.connection.execute("DELETE FROM source_records")
        self.connection.execute(
            "DELETE FROM metadata WHERE key <> 'state_schema_version'"
        )

    def metadata(self, key: str) -> str | None:
        row = self.connection.execute(
            "SELECT value FROM metadata WHERE key = ?", (key,)
        ).fetchone()
        return str(row[0]) if row is not None else None

    def remember_metadata(self, key: str, value: str) -> None:
        self.connection.execute(
            """
            INSERT INTO metadata(key, value) VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )

    def refresh(
        self,
        *,
        derived_lanes: Iterable[str],
        include_acknowledgements: bool = True,
    ) -> None:
        for lane in sorted(set(derived_lanes)):
            pattern = f"*/*/{lane}/*"
            for path in sorted((self.root.path / "derived").glob(pattern)):
                if path.is_file():
                    self._observe(path, subtree="derived")
        if include_acknowledgements:
            ack_root = self.root.path / "acknowledgements"
            if ack_root.is_dir():
                for path in sorted(ack_root.glob("*/*/*/*")):
                    if path.is_file():
                        self._observe(path, subtree="acknowledgements")

        stored_paths = {
            str(row[0])
            for row in self.connection.execute(
                "SELECT relative_path FROM source_records"
            )
        }
        disappeared = sorted(stored_paths - self._seen)
        if disappeared:
            preview = ", ".join(disappeared[:3])
            raise DataLakeRootError(
                "append-only lake source disappeared after it was inventoried: "
                f"{preview}{' ...' if len(disappeared) > 3 else ''}; "
                "do not accept an incremental map until the lake is repaired or "
                "a deliberate cold rebuild is authorized"
            )

    def _observe(self, path: Path, *, subtree: str) -> None:
        relative_path = path.relative_to(self.root.path).as_posix()
        self._seen.add(relative_path)
        raw_anchor = path.parents[1].name
        lane = path.parent.name
        record_id = path.name
        ref_key = f"{raw_anchor}/{lane}/{record_id}"
        try:
            stat = path.stat()
        except OSError as exc:
            raise DataLakeRootError(
                f"cannot stat lake-map source {relative_path}: {exc}"
            ) from exc
        existing = self.connection.execute(
            """
            SELECT size_bytes, mtime_ns, sha256
            FROM source_records WHERE relative_path = ?
            """,
            (relative_path,),
        ).fetchone()
        if (
            existing is not None
            and int(existing[0]) == stat.st_size
            and int(existing[1]) == stat.st_mtime_ns
        ):
            self._reused += 1
            return
        try:
            body = path.read_bytes()
        except OSError as exc:
            raise DataLakeRootError(
                f"cannot read lake-map source {relative_path}: {exc}"
            ) from exc
        self._body_reads += 1
        sha256 = hashlib.sha256(body).hexdigest()
        if existing is not None and str(existing[2]) != sha256:
            raise DataLakeRootError(
                "append-only lake source changed after it was inventoried: "
                f"{relative_path}; run the source-integrity audit before any "
                "map refresh"
            )
        if existing is None:
            self.connection.execute(
                """
                INSERT INTO source_records(
                    relative_path, subtree, raw_anchor, lane, record_id, ref_key,
                    size_bytes, mtime_ns, sha256, body
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    relative_path,
                    subtree,
                    raw_anchor,
                    lane,
                    record_id,
                    ref_key,
                    stat.st_size,
                    stat.st_mtime_ns,
                    sha256,
                    body,
                ),
            )
            self._new += 1
        else:
            self.connection.execute(
                """
                UPDATE source_records
                SET size_bytes = ?, mtime_ns = ?
                WHERE relative_path = ?
                """,
                (stat.st_size, stat.st_mtime_ns, relative_path),
            )
            self._metadata_refreshed += 1

    def records(
        self,
        *,
        subtree: str,
        lanes: Iterable[str] | None = None,
    ) -> Iterator[StoredSourceRecord]:
        parameters: list[object] = [subtree]
        clause = ""
        lane_values = sorted(set(lanes or ()))
        if lane_values:
            placeholders = ",".join("?" for _ in lane_values)
            clause = f" AND lane IN ({placeholders})"
            parameters.extend(lane_values)
        rows = self.connection.execute(
            f"""
            SELECT subtree, raw_anchor, lane, record_id, relative_path, ref_key,
                   body, sha256, classification_cache_key
            FROM source_records
            WHERE subtree = ?{clause}
            ORDER BY lane, raw_anchor, record_id
            """,
            parameters,
        )
        for row in rows:
            yield StoredSourceRecord(
                subtree=str(row[0]),
                raw_anchor=str(row[1]),
                lane=str(row[2]),
                record_id=str(row[3]),
                relative_path=str(row[4]),
                ref_key=str(row[5]),
                body=bytes(row[6]),
                sha256=str(row[7]),
                classification_cache_key=(
                    str(row[8]) if row[8] is not None else None
                ),
            )

    def remember_classification_cache_key(
        self, relative_path: str, cache_key: str | None
    ) -> None:
        self.connection.execute(
            """
            UPDATE source_records
            SET classification_cache_key = ?
            WHERE relative_path = ?
            """,
            (cache_key, relative_path),
        )

    def inventory(self) -> dict[str, object]:
        rows = [
            {
                "relative_path": str(row[0]),
                "sha256": str(row[1]),
            }
            for row in self.connection.execute(
                """
                SELECT relative_path, sha256
                FROM source_records
                ORDER BY relative_path
                """
            )
        ]
        return {
            "source_count": len(rows),
            "source_inventory_sha256": hashlib.sha256(
                canonical_record_bytes(rows)
            ).hexdigest(),
        }

    def report(self) -> dict[str, object]:
        return {
            "state_schema_version": STATE_SCHEMA_VERSION,
            "new_sources": self._new,
            "reused_sources": self._reused,
            "metadata_refreshed": self._metadata_refreshed,
            "source_body_reads": self._body_reads,
            **self.inventory(),
        }


__all__ = [
    "IncrementalSourceInventory",
    "STATE_PARTS",
    "STATE_SCHEMA_VERSION",
    "StoredSourceRecord",
]
