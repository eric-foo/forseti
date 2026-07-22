"""Transactional SQLite authority for the operational Creator Registry.

The database is lane-specific lake state.  Raw packets, Frontier dispositions,
and Judgment outcomes remain file-backed evidence; this module stores only the
current Registry rows and their public allowlisted projections.
"""
from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import uuid
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRoot


SQLITE_SCHEMA = "creator_registry_sqlite_v1"
SQLITE_USER_VERSION = 1
SQLITE_POINTER_SCHEMA_VERSION = 4
SQLITE_ROOT_PARTS = ("derived", "creator_registry_sql_v1")
SQLITE_FILENAME = "creator_registry.sqlite3"


class CreatorRegistrySqliteError(ValueError):
    """Fail-closed SQLite Registry schema, integrity, or mutation error."""


def database_path(data_root: DataLakeRoot) -> Path:
    return data_root.path.joinpath(*SQLITE_ROOT_PARTS, SQLITE_FILENAME)


def database_ref() -> str:
    return Path(*SQLITE_ROOT_PARTS, SQLITE_FILENAME).as_posix()


def bootstrap_database(
    *,
    data_root: DataLakeRoot,
    internal_document: Mapping[str, Any],
    public_document: Mapping[str, Any],
    authority_refs: Sequence[Mapping[str, str]],
    authority_inventory_sha256: str,
    dry_run: bool,
) -> dict[str, Any]:
    """Build and parity-check one SQL Registry without switching CURRENT."""
    internal = deepcopy(dict(internal_document))
    public = deepcopy(dict(public_document))
    internal_rows = list(internal["creator_registry_index"]["platform_accounts"])
    public_rows = list(public["creator_profile_public"]["profiles"])
    generated_at = str(internal["creator_registry_index"]["generated_at_utc"])

    if dry_run:
        with tempfile.TemporaryDirectory(prefix="forseti-registry-sqlite-") as temp:
            target = Path(temp) / SQLITE_FILENAME
            _create_database(
                target=target,
                internal_document=internal,
                public_document=public,
                authority_refs=authority_refs,
                authority_inventory_sha256=authority_inventory_sha256,
            )
            parity = _parity(target, internal, public)
        return _bootstrap_result(
            target=database_path(data_root),
            internal_rows=internal_rows,
            public_rows=public_rows,
            generated_at=generated_at,
            authority_inventory_sha256=authority_inventory_sha256,
            parity=parity,
            would_write_database=not database_path(data_root).exists(),
        )

    data_root._require_writable("cut over Creator Registry to SQLite")
    data_root._reverify()
    target = database_path(data_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        metadata = inspect_database(target)
        if metadata["migration_authority_inventory_sha256"] != authority_inventory_sha256:
            raise CreatorRegistrySqliteError(
                "existing Creator Registry SQLite database has a different migration inventory"
            )
        parity = _parity(target, internal, public)
        would_write = False
    else:
        staging_root = data_root.path / ".staging"
        staging_root.mkdir(parents=True, exist_ok=True)
        staging = staging_root / f"creator-registry-{uuid.uuid4().hex}.sqlite3"
        try:
            _create_database(
                target=staging,
                internal_document=internal,
                public_document=public,
                authority_refs=authority_refs,
                authority_inventory_sha256=authority_inventory_sha256,
            )
            parity = _parity(staging, internal, public)
            os.replace(staging, target)
        finally:
            staging.unlink(missing_ok=True)
        would_write = True
    return _bootstrap_result(
        target=target,
        internal_rows=internal_rows,
        public_rows=public_rows,
        generated_at=generated_at,
        authority_inventory_sha256=authority_inventory_sha256,
        parity=parity,
        would_write_database=would_write,
    )


def load_documents(
    data_root: DataLakeRoot,
    *,
    expected_migration_authority_inventory_sha256: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    data_root._reverify()
    target = database_path(data_root)
    with _connect(target, readonly=True) as connection:
        metadata = _metadata(connection)
        if (
            expected_migration_authority_inventory_sha256 is not None
            and metadata["migration_authority_inventory_sha256"]
            != expected_migration_authority_inventory_sha256
        ):
            raise CreatorRegistrySqliteError(
                "Creator Registry SQLite CURRENT pointer does not match the database migration authority inventory"
            )
        index_template = _json_object(metadata["index_template_json"], "Registry index template")
        public_template = _json_object(metadata["public_template_json"], "public profile template")
        accounts = [
            _json_object(row[0], "Registry account row")
            for row in connection.execute(
                "SELECT account_json FROM registry_accounts ORDER BY platform, platform_account_id"
            )
        ]
        profiles = [
            _json_object(row[0], "public profile row")
            for row in connection.execute(
                "SELECT profile_json FROM registry_public_profiles ORDER BY profile_subject_id"
            )
        ]
        source_inputs = [
            {"record_ref": row[0], "sha256": row[1]}
            for row in connection.execute(
                "SELECT record_ref, sha256 FROM registry_migration_sources ORDER BY record_ref"
            )
        ]
    index = _render_internal_document(
        template=index_template,
        accounts=accounts,
        source_inputs=source_inputs,
        generated_at=metadata["generated_at_utc"],
    )
    public = _render_public_document(
        template=public_template,
        profiles=profiles,
        generated_at=metadata["generated_at_utc"],
    )
    return index, public


def inspect_database(target: Path) -> dict[str, Any]:
    with _connect(target, readonly=True) as connection:
        result = _metadata(connection)
        integrity = connection.execute("PRAGMA quick_check").fetchone()
        if integrity is None or integrity[0] != "ok":
            raise CreatorRegistrySqliteError("Creator Registry SQLite quick_check failed")
        result["platform_accounts_total"] = connection.execute(
            "SELECT COUNT(*) FROM registry_accounts"
        ).fetchone()[0]
        result["public_profiles_total"] = connection.execute(
            "SELECT COUNT(*) FROM registry_public_profiles"
        ).fetchone()[0]
        result["database_path"] = str(target)
        return result


def insert_candidate(
    *, data_root: DataLakeRoot, row: Mapping[str, Any], revision_id: str, generated_at: str
) -> str:
    account = deepcopy(dict(row))
    values = _account_columns(account)
    target = database_path(data_root)
    data_root._require_writable("admit Creator Registry candidate")
    data_root._reverify()
    try:
        with _write_transaction(target) as connection:
            matches = _identity_matches(connection, values)
            if matches:
                if (
                    len(matches) == 1
                    and matches[0]["platform_account_id"] == values["platform_account_id"]
                    and matches[0]["authority_kind"] == "candidate"
                    and matches[0]["source_revision_id"] == revision_id
                    and _json_object(matches[0]["account_json"], "stored candidate") == account
                ):
                    return "already_current"
                raise CreatorRegistrySqliteError(
                    "candidate identity conflicts with a current Registry account"
                )
            connection.execute(
                """
                INSERT INTO registry_accounts (
                    platform_account_id, platform, platform_public_account_id,
                    normalized_public_handle, onboarding_state, monitoring_eligible,
                    authority_kind, source_revision_id, account_json
                ) VALUES (?, ?, ?, ?, ?, ?, 'candidate', ?, ?)
                """,
                (
                    values["platform_account_id"],
                    values["platform"],
                    values["platform_public_account_id"],
                    values["normalized_public_handle"],
                    values["onboarding_state"],
                    values["monitoring_eligible"],
                    revision_id,
                    _json_text(account),
                ),
            )
            _advance_generated_at(connection, generated_at)
    except sqlite3.Error as exc:
        raise CreatorRegistrySqliteError(f"candidate Registry transaction failed: {exc}") from exc
    return "admitted"


def upgrade_validated_account(
    *,
    data_root: DataLakeRoot,
    account_row: Mapping[str, Any],
    public_profile: Mapping[str, Any],
    revision_id: str,
    generated_at: str,
) -> str:
    account = deepcopy(dict(account_row))
    profile = deepcopy(dict(public_profile))
    values = _account_columns(account)
    account_id = values["platform_account_id"]
    if profile.get("profile_subject_id") != account_id:
        raise CreatorRegistrySqliteError("public profile subject does not match Registry account")
    target = database_path(data_root)
    data_root._require_writable("complete Creator Registry onboarding")
    data_root._reverify()
    try:
        with _write_transaction(target) as connection:
            stored = connection.execute(
                "SELECT * FROM registry_accounts WHERE platform_account_id = ?", (account_id,)
            ).fetchone()
            if stored is None:
                raise CreatorRegistrySqliteError(
                    "validated onboarding requires one current Registry candidate"
                )
            existing_profile = connection.execute(
                "SELECT profile_json FROM registry_public_profiles WHERE profile_subject_id = ?",
                (account_id,),
            ).fetchone()
            if (
                stored["authority_kind"] == "validated"
                and stored["source_revision_id"] == revision_id
                and _json_object(stored["account_json"], "stored account") == account
                and existing_profile is not None
                and _json_object(existing_profile[0], "stored public profile") == profile
            ):
                return "already_current"
            if stored["authority_kind"] != "candidate" or stored["onboarding_state"] != "not_onboarded":
                raise CreatorRegistrySqliteError(
                    "validated onboarding requires one current Registry not_onboarded candidate"
                )
            connection.execute(
                """
                UPDATE registry_accounts
                SET platform = ?, platform_public_account_id = ?, normalized_public_handle = ?,
                    onboarding_state = ?, monitoring_eligible = ?, authority_kind = 'validated',
                    source_revision_id = ?, account_json = ?
                WHERE platform_account_id = ?
                """,
                (
                    values["platform"],
                    values["platform_public_account_id"],
                    values["normalized_public_handle"],
                    values["onboarding_state"],
                    values["monitoring_eligible"],
                    revision_id,
                    _json_text(account),
                    account_id,
                ),
            )
            connection.execute(
                "INSERT INTO registry_public_profiles (profile_subject_id, profile_json) VALUES (?, ?)",
                (account_id, _json_text(profile)),
            )
            _advance_generated_at(connection, generated_at)
    except sqlite3.Error as exc:
        raise CreatorRegistrySqliteError(f"validated Registry transaction failed: {exc}") from exc
    return "admitted"


def delete_candidate(
    *, data_root: DataLakeRoot, normalized_public_handle: str, generated_at: str
) -> dict[str, Any]:
    target = database_path(data_root)
    data_root._require_writable("remove Creator Registry candidate")
    data_root._reverify()
    try:
        with _write_transaction(target) as connection:
            rows = connection.execute(
                "SELECT * FROM registry_accounts WHERE platform = 'tiktok' AND normalized_public_handle = ?",
                (normalized_public_handle,),
            ).fetchall()
            if len(rows) != 1:
                raise CreatorRegistrySqliteError(
                    "candidate removal requires exactly one current Registry account"
                )
            stored = rows[0]
            if (
                stored["authority_kind"] != "candidate"
                or stored["onboarding_state"] != "not_onboarded"
                or stored["monitoring_eligible"] != 0
            ):
                raise CreatorRegistrySqliteError(
                    "validated, migrated, onboarded, or monitored Registry accounts cannot be candidate-removed"
                )
            public_count = connection.execute(
                "SELECT COUNT(*) FROM registry_public_profiles WHERE profile_subject_id = ?",
                (stored["platform_account_id"],),
            ).fetchone()[0]
            if public_count:
                raise CreatorRegistrySqliteError(
                    "a public Registry account cannot be candidate-removed"
                )
            account = _json_object(stored["account_json"], "stored candidate")
            connection.execute(
                "DELETE FROM registry_accounts WHERE platform_account_id = ?",
                (stored["platform_account_id"],),
            )
            _advance_generated_at(connection, generated_at)
            return {
                "platform_account_id": stored["platform_account_id"],
                "source_revision_id": stored["source_revision_id"],
                "account": account,
            }
    except sqlite3.Error as exc:
        raise CreatorRegistrySqliteError(f"candidate removal transaction failed: {exc}") from exc


def _create_database(
    *,
    target: Path,
    internal_document: Mapping[str, Any],
    public_document: Mapping[str, Any],
    authority_refs: Sequence[Mapping[str, str]],
    authority_inventory_sha256: str,
) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with _connect(target, readonly=False, creating=True) as connection:
        connection.executescript(
            """
            BEGIN IMMEDIATE;
            CREATE TABLE registry_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            ) WITHOUT ROWID;
            CREATE TABLE registry_migration_sources (
                record_ref TEXT PRIMARY KEY,
                sha256 TEXT NOT NULL CHECK(length(sha256) = 64)
            ) WITHOUT ROWID;
            CREATE TABLE registry_accounts (
                platform_account_id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                platform_public_account_id TEXT,
                normalized_public_handle TEXT NOT NULL,
                onboarding_state TEXT NOT NULL CHECK(onboarding_state IN ('not_onboarded', 'onboarded')),
                monitoring_eligible INTEGER NOT NULL CHECK(monitoring_eligible IN (0, 1)),
                authority_kind TEXT NOT NULL CHECK(authority_kind IN ('migrated', 'candidate', 'validated')),
                source_revision_id TEXT NOT NULL UNIQUE,
                account_json TEXT NOT NULL CHECK(json_valid(account_json)),
                CHECK((onboarding_state = 'onboarded' AND monitoring_eligible = 1)
                      OR (onboarding_state = 'not_onboarded' AND monitoring_eligible = 0))
            ) WITHOUT ROWID;
            CREATE UNIQUE INDEX registry_accounts_native_unique
                ON registry_accounts(platform, platform_public_account_id)
                WHERE platform_public_account_id IS NOT NULL;
            CREATE UNIQUE INDEX registry_accounts_handle_unique
                ON registry_accounts(platform, normalized_public_handle);
            CREATE TABLE registry_public_profiles (
                profile_subject_id TEXT PRIMARY KEY,
                profile_json TEXT NOT NULL CHECK(json_valid(profile_json))
            ) WITHOUT ROWID;
            """
        )
        index_template = deepcopy(dict(internal_document))
        public_template = deepcopy(dict(public_document))
        index_rows = index_template["creator_registry_index"].pop("platform_accounts")
        public_rows = public_template["creator_profile_public"].pop("profiles")
        metadata = {
            "schema_version": SQLITE_SCHEMA,
            "generated_at_utc": str(
                internal_document["creator_registry_index"]["generated_at_utc"]
            ),
            "migration_authority_inventory_sha256": authority_inventory_sha256,
            "index_template_json": _json_text(index_template),
            "public_template_json": _json_text(public_template),
        }
        connection.executemany(
            "INSERT INTO registry_meta (key, value) VALUES (?, ?)", metadata.items()
        )
        connection.executemany(
            "INSERT INTO registry_migration_sources (record_ref, sha256) VALUES (?, ?)",
            [(str(row["record_ref"]), str(row["sha256"])) for row in authority_refs],
        )
        for row in index_rows:
            values = _account_columns(row)
            connection.execute(
                """
                INSERT INTO registry_accounts (
                    platform_account_id, platform, platform_public_account_id,
                    normalized_public_handle, onboarding_state, monitoring_eligible,
                    authority_kind, source_revision_id, account_json
                ) VALUES (?, ?, ?, ?, ?, ?, 'migrated', ?, ?)
                """,
                (
                    values["platform_account_id"],
                    values["platform"],
                    values["platform_public_account_id"],
                    values["normalized_public_handle"],
                    values["onboarding_state"],
                    values["monitoring_eligible"],
                    f"migration:{values['platform_account_id']}",
                    _json_text(row),
                ),
            )
        connection.executemany(
            "INSERT INTO registry_public_profiles (profile_subject_id, profile_json) VALUES (?, ?)",
            [(str(row["profile_subject_id"]), _json_text(row)) for row in public_rows],
        )
        connection.execute(f"PRAGMA user_version = {SQLITE_USER_VERSION}")
        connection.commit()


def _parity(
    target: Path, internal_document: Mapping[str, Any], public_document: Mapping[str, Any]
) -> dict[str, bool]:
    with _connect(target, readonly=True) as connection:
        metadata = _metadata(connection)
        accounts = [
            _json_object(row[0], "Registry parity account")
            for row in connection.execute(
                "SELECT account_json FROM registry_accounts ORDER BY platform, platform_account_id"
            )
        ]
        profiles = [
            _json_object(row[0], "Registry parity profile")
            for row in connection.execute(
                "SELECT profile_json FROM registry_public_profiles ORDER BY profile_subject_id"
            )
        ]
    expected_accounts = sorted(
        deepcopy(list(internal_document["creator_registry_index"]["platform_accounts"])),
        key=lambda row: (str(row.get("platform")), str(row.get("platform_account_id"))),
    )
    expected_profiles = sorted(
        deepcopy(list(public_document["creator_profile_public"]["profiles"])),
        key=lambda row: str(row.get("profile_subject_id")),
    )
    parity = {
        "platform_accounts_equal": accounts == expected_accounts,
        "public_profiles_equal": profiles == expected_profiles,
        "generated_at_equal": metadata["generated_at_utc"]
        == internal_document["creator_registry_index"]["generated_at_utc"],
    }
    if not all(parity.values()):
        raise CreatorRegistrySqliteError(f"Creator Registry SQLite parity failed: {parity}")
    return parity


def _bootstrap_result(
    *,
    target: Path,
    internal_rows: Sequence[Mapping[str, Any]],
    public_rows: Sequence[Mapping[str, Any]],
    generated_at: str,
    authority_inventory_sha256: str,
    parity: Mapping[str, bool],
    would_write_database: bool,
) -> dict[str, Any]:
    return {
        "database_path": str(target),
        "database_ref": database_ref(),
        "database_schema_version": SQLITE_SCHEMA,
        "migration_authority_inventory_sha256": authority_inventory_sha256,
        "generated_at_utc": generated_at,
        "platform_accounts_total": len(internal_rows),
        "public_profiles_total": len(public_rows),
        "parity": dict(parity),
        "would_write_database": would_write_database,
    }


def _render_internal_document(
    *, template: Mapping[str, Any], accounts: Sequence[Mapping[str, Any]],
    source_inputs: Sequence[Mapping[str, str]], generated_at: str
) -> dict[str, Any]:
    document = deepcopy(dict(template))
    wrapper = document["creator_registry_index"]
    wrapper.update(
        {
            "schema_version": "creator_registry_index_v1",
            "index_id": "creator_registry_index_v1",
            "index_mode": "lake_sqlite_current_authority",
            "generated_at_utc": generated_at,
            "platform_accounts": deepcopy(list(accounts)),
            "source_inputs": deepcopy(list(source_inputs)),
            "source_policy_posture": (
                "Current operational Registry authority is the lake-resident SQLite database; "
                "source_inputs identify the verified v3 migration state and each account row "
                "retains its evidence pointers."
            ),
        }
    )
    wrapper["counts"] = _index_counts(accounts, wrapper.get("creator_records", []))
    return document


def _render_public_document(
    *, template: Mapping[str, Any], profiles: Sequence[Mapping[str, Any]], generated_at: str
) -> dict[str, Any]:
    document = deepcopy(dict(template))
    wrapper = document["creator_profile_public"]
    wrapper.update(
        {
            "schema_version": "creator_profile_public_v1",
            "view_id": "creator_profile_public_v1",
            "generated_at_utc": generated_at,
            "profiles": deepcopy(list(profiles)),
            "counts": {
                "profiles_total": len(profiles),
                "profiles_with_audience_triangulation": sum(
                    1 for row in profiles if row.get("audience_triangulation") is not None
                ),
                "profiles_with_metric_rollups": sum(
                    1 for row in profiles if row.get("current_metric_rollups")
                ),
            },
        }
    )
    return document


def _index_counts(rows: Sequence[Mapping[str, Any]], creator_records: Any) -> dict[str, Any]:
    platforms: dict[str, int] = {}
    onboarding: dict[str, int] = {}
    for row in rows:
        platform = str(row.get("platform"))
        state = str(row.get("onboarding", {}).get("onboarding_state"))
        platforms[platform] = platforms.get(platform, 0) + 1
        onboarding[state] = onboarding.get(state, 0) + 1
    return {
        "platform_accounts_total": len(rows),
        "creator_records_total": len(creator_records) if isinstance(creator_records, list) else 0,
        "known_account_rows_total": len(rows),
        "platform_accounts_by_platform": dict(sorted(platforms.items())),
        "platform_accounts_by_onboarding_state": dict(sorted(onboarding.items())),
        "monitoring_eligible_total": sum(
            1 for row in rows if row.get("monitoring_eligibility", {}).get("eligible") is True
        ),
    }


def _account_columns(row: Mapping[str, Any]) -> dict[str, Any]:
    onboarding = row.get("onboarding")
    monitoring = row.get("monitoring_eligibility")
    if not isinstance(onboarding, Mapping) or not isinstance(monitoring, Mapping):
        raise CreatorRegistrySqliteError("Registry account lacks onboarding or monitoring state")
    platform_account_id = _required_text(row.get("platform_account_id"), "platform account id")
    platform = _required_text(row.get("platform"), "platform").casefold()
    handle = _required_text(row.get("normalized_public_handle") or row.get("public_handle"), "public handle")
    native = row.get("platform_public_account_id_or_none")
    return {
        "platform_account_id": platform_account_id,
        "platform": platform,
        "platform_public_account_id": str(native) if native is not None else None,
        "normalized_public_handle": handle.lstrip("@").casefold(),
        "onboarding_state": _required_text(onboarding.get("onboarding_state"), "onboarding state"),
        "monitoring_eligible": 1 if monitoring.get("eligible") is True else 0,
    }


def _identity_matches(connection: sqlite3.Connection, values: Mapping[str, Any]) -> list[sqlite3.Row]:
    rows = connection.execute(
        """
        SELECT * FROM registry_accounts
        WHERE platform_account_id = ?
           OR (platform = ? AND platform_public_account_id IS NOT NULL AND platform_public_account_id = ?)
           OR (platform = ? AND normalized_public_handle = ?)
        """,
        (
            values["platform_account_id"],
            values["platform"],
            values["platform_public_account_id"],
            values["platform"],
            values["normalized_public_handle"],
        ),
    ).fetchall()
    by_id = {row["platform_account_id"]: row for row in rows}
    return list(by_id.values())


def _advance_generated_at(connection: sqlite3.Connection, candidate: str) -> None:
    current = connection.execute(
        "SELECT value FROM registry_meta WHERE key = 'generated_at_utc'"
    ).fetchone()[0]
    connection.execute(
        "UPDATE registry_meta SET value = ? WHERE key = 'generated_at_utc'",
        (max(str(current), str(candidate)),),
    )


def _metadata(connection: sqlite3.Connection) -> dict[str, str]:
    user_version = connection.execute("PRAGMA user_version").fetchone()[0]
    if user_version != SQLITE_USER_VERSION:
        raise CreatorRegistrySqliteError("Creator Registry SQLite user_version is unsupported")
    values = {str(row[0]): str(row[1]) for row in connection.execute("SELECT key, value FROM registry_meta")}
    required = {
        "schema_version",
        "generated_at_utc",
        "migration_authority_inventory_sha256",
        "index_template_json",
        "public_template_json",
    }
    if set(values) != required or values.get("schema_version") != SQLITE_SCHEMA:
        raise CreatorRegistrySqliteError("Creator Registry SQLite metadata is unsupported")
    return values


@contextmanager
def _write_transaction(target: Path) -> Iterator[sqlite3.Connection]:
    with _connect(target, readonly=False) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            yield connection
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()


@contextmanager
def _connect(
    target: Path, *, readonly: bool, creating: bool = False
) -> Iterator[sqlite3.Connection]:
    if readonly:
        if not target.is_file():
            raise CreatorRegistrySqliteError("Creator Registry SQLite database is missing")
        connection = sqlite3.connect(f"file:{target.as_posix()}?mode=ro", uri=True, timeout=5.0)
    else:
        if not creating and not target.is_file():
            raise CreatorRegistrySqliteError("Creator Registry SQLite database is missing")
        connection = sqlite3.connect(target, timeout=5.0)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        if not readonly:
            connection.execute("PRAGMA journal_mode = DELETE")
            connection.execute("PRAGMA synchronous = FULL")
        yield connection
    finally:
        connection.close()


def _json_text(value: Mapping[str, Any]) -> str:
    return canonical_record_bytes(value).decode("utf-8")


def _json_object(value: str, role: str) -> dict[str, Any]:
    try:
        decoded = json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc:
        raise CreatorRegistrySqliteError(f"{role} is not valid JSON") from exc
    if not isinstance(decoded, dict):
        raise CreatorRegistrySqliteError(f"{role} is not an object")
    return decoded


def _required_text(value: Any, role: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CreatorRegistrySqliteError(f"{role} must be nonblank text")
    return value.strip()


__all__ = [
    "CreatorRegistrySqliteError",
    "SQLITE_POINTER_SCHEMA_VERSION",
    "SQLITE_SCHEMA",
    "bootstrap_database",
    "database_path",
    "database_ref",
    "delete_candidate",
    "inspect_database",
    "insert_candidate",
    "load_documents",
    "upgrade_validated_account",
]
