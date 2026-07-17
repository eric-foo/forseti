#!/usr/bin/env python3
"""Apply a bounded exact-replacement plan without hand-authoring a patch.

Changes may be passed as repeated ``--replace PATH OLD NEW`` triples. The OLD
and NEW values recognize ``\\n``, ``\\t``, and ``\\\\`` escapes, which keeps a
PowerShell invocation simple when every value is single-quoted. A versioned
UTF-8 JSON plan remains available directly or as base64:

    {
      "version": 1,
      "replacements": [
        {"path": "relative/file.txt", "old": "exact old text", "new": "new text"}
      ]
    }

All targets and replacement counts are checked before any write. Logical LF in
the plan is rendered using each target's existing LF or CRLF convention. The
helper rejects mixed-newline files, symlinks, path escapes, ambiguous matches,
and no-op replacements. ``--apply`` performs preflight and apply in one call.

The defensive preflight/rollback machinery here is deliberate, not bloat: the
AGENTS.md stalled-edit fallback route depends on it. Applies use a durable
root-local journal so an interrupted multi-file edit can be recovered before a
later edit begins, and a per-root OS lock outside the edited root so a
concurrent invocation fails loudly without leaving normal-use repository
residue. Each file is replaced atomically; the multi-file sequence is
recoverable, not atomic. Do not simplify this machinery away.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if os.name == "nt":
    import msvcrt
else:
    import fcntl


JOURNAL_NAME = ".atomic_exact_edit_journal_v1.json"
LOCK_DIRECTORY = "forseti-atomic-exact-edit-locks"
JOURNAL_VERSION = 1
TEST_FAULT_ENABLE = "ATOMIC_EXACT_EDIT_ENABLE_TEST_FAULTS"
TEST_CRASH_AFTER = "ATOMIC_EXACT_EDIT_TEST_CRASH_AFTER_REPLACES"


class EditError(Exception):
    """A visible plan, preflight, or apply failure."""


class RollbackError(EditError):
    """An apply failure whose rollback also failed."""


@dataclass(frozen=True)
class PreparedFile:
    path: Path
    display_path: str
    original: bytes
    updated: bytes
    mode: int


def _parse_plan_bytes(raw: bytes) -> tuple[dict[str, Any], bytes, str]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise EditError(f"plan is not UTF-8: {exc}") from exc
    try:
        plan = json.loads(text)
    except json.JSONDecodeError as exc:
        raise EditError(f"plan is not valid JSON: {exc}") from exc
    if not isinstance(plan, dict):
        raise EditError("plan root must be an object")
    return plan, raw, hashlib.sha256(raw).hexdigest().upper()


def _decode_plan_base64(encoded: str) -> tuple[dict[str, Any], bytes, str]:
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise EditError(f"plan is not valid base64: {exc}") from exc
    return _parse_plan_bytes(raw)


def _decode_plan_json(text: str) -> tuple[dict[str, Any], bytes, str]:
    return _parse_plan_bytes(text.encode("utf-8"))


def _decode_cli_text(value: str) -> str:
    output: list[str] = []
    index = 0
    escapes = {"n": "\n", "t": "\t", "\\": "\\"}
    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            marker = value[index + 1]
            if marker in escapes:
                output.append(escapes[marker])
                index += 2
                continue
        output.append(char)
        index += 1
    return "".join(output)


def _plan_from_replacements(values: list[list[str]]) -> tuple[dict[str, Any], bytes, str]:
    plan = {
        "version": 1,
        "replacements": [
            {
                "path": path,
                "old": _decode_cli_text(old),
                "new": _decode_cli_text(new),
            }
            for path, old, new in values
        ],
    }
    raw = json.dumps(plan, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return plan, raw, hashlib.sha256(raw).hexdigest().upper()


def _logical_text(value: Any, field: str, index: int) -> str:
    if not isinstance(value, str):
        raise EditError(f"replacement {index} field {field!r} must be a string")
    normalized = value.replace("\r\n", "\n")
    if "\r" in normalized:
        raise EditError(
            f"replacement {index} field {field!r} contains a bare carriage return"
        )
    return normalized


def _newline_for(data: bytes, display_path: str) -> bytes:
    without_crlf = data.replace(b"\r\n", b"")
    has_crlf = b"\r\n" in data
    has_bare_lf = b"\n" in without_crlf
    has_bare_cr = b"\r" in without_crlf
    if has_bare_cr or (has_crlf and has_bare_lf):
        raise EditError(f"{display_path}: mixed or bare-CR newlines are unsupported")
    return b"\r\n" if has_crlf else b"\n"


def _resolve_target(root: Path, raw_path: Any, index: int) -> tuple[Path, str]:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise EditError(f"replacement {index} path must be a non-empty string")
    rel = Path(raw_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise EditError(f"replacement {index} path must stay relative to the root")
    if rel.as_posix() == JOURNAL_NAME:
        raise EditError(f"replacement {index} cannot target the recovery journal")
    target = root / rel
    if target.is_symlink():
        raise EditError(f"{raw_path}: symlink targets are unsupported")
    try:
        resolved = target.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise EditError(f"{raw_path}: target is missing or escapes the root") from exc
    if not resolved.is_file():
        raise EditError(f"{raw_path}: target is not a regular file")
    return resolved, rel.as_posix()


def prepare(root: Path, plan: dict[str, Any]) -> list[PreparedFile]:
    if plan.get("version") != 1:
        raise EditError("plan version must be exactly 1")
    replacements = plan.get("replacements")
    if not isinstance(replacements, list) or not replacements:
        raise EditError("replacements must be a non-empty list")

    root = root.resolve(strict=True)
    originals: dict[Path, tuple[str, bytes, int, bytes]] = {}
    updated_payloads: dict[Path, bytes] = {}

    for index, item in enumerate(replacements, start=1):
        if not isinstance(item, dict):
            raise EditError(f"replacement {index} must be an object")
        unknown = set(item) - {"path", "old", "new", "expected"}
        if unknown:
            raise EditError(
                f"replacement {index} has unknown field(s): {', '.join(sorted(unknown))}"
            )
        target, display_path = _resolve_target(root, item.get("path"), index)
        if target not in originals:
            original = target.read_bytes()
            newline = _newline_for(original, display_path)
            originals[target] = (
                display_path,
                original,
                stat.S_IMODE(target.stat().st_mode),
                newline,
            )
            updated_payloads[target] = original

        display_path, original, mode, newline = originals[target]
        old = _logical_text(item.get("old"), "old", index)
        new = _logical_text(item.get("new"), "new", index)
        if not old:
            raise EditError(f"replacement {index} old text must not be empty")
        if old == new:
            raise EditError(f"replacement {index} is a no-op")
        expected = item.get("expected", 1)
        if isinstance(expected, bool) or not isinstance(expected, int) or expected < 1:
            raise EditError(f"replacement {index} expected must be a positive integer")

        old_bytes = old.encode("utf-8").replace(b"\n", newline)
        new_bytes = new.encode("utf-8").replace(b"\n", newline)
        current = updated_payloads[target]
        observed = current.count(old_bytes)
        if observed != expected:
            raise EditError(
                f"{display_path}: replacement {index} expected {expected} exact match(es), "
                f"observed {observed}"
            )
        updated_payloads[target] = current.replace(old_bytes, new_bytes, expected)

    prepared = []
    for target, (display_path, original, mode, _newline) in originals.items():
        updated = updated_payloads[target]
        if updated == original:
            raise EditError(f"{display_path}: combined replacements produce no byte change")
        prepared.append(PreparedFile(target, display_path, original, updated, mode))
    return prepared


def _write_temp(item: PreparedFile, payload: bytes) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{item.path.name}.atomic-exact-edit-", dir=item.path.parent
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, item.mode)
        return temporary
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _restore(item: PreparedFile) -> None:
    temporary = _write_temp(item, item.original)
    try:
        os.replace(temporary, item.path)
    finally:
        temporary.unlink(missing_ok=True)


def _journal_path(root: Path) -> Path:
    return root / JOURNAL_NAME


def _lock_path(root: Path) -> Path:
    owner_suffix = f"-{os.getuid()}" if hasattr(os, "getuid") else ""
    directory = Path(tempfile.gettempdir()) / f"{LOCK_DIRECTORY}{owner_suffix}"
    try:
        directory.mkdir(mode=0o700, exist_ok=True)
    except OSError as exc:
        raise EditError(
            f"cannot prepare transaction lock directory: {directory}: {exc}"
        ) from exc
    if directory.is_symlink() or not directory.is_dir():
        raise EditError(f"transaction lock directory is unsafe: {directory}")
    try:
        os.chmod(directory, 0o700)
    except OSError as exc:
        raise EditError(
            f"cannot secure transaction lock directory: {directory}: {exc}"
        ) from exc
    identity = os.path.normcase(str(root.resolve(strict=True)))
    digest = hashlib.sha256(os.fsencode(identity)).hexdigest()
    return directory / f"{digest}.lock"


def _acquire_lock(root: Path) -> int:
    """Take the root-local transaction lock, or fail loudly if it is held.

    The OS releases the lock when the holding process exits, including on a
    hard kill, so an interrupted apply never wedges later recovery. A live
    concurrent invocation must never silently join, roll back, or re-journal
    the same transaction.
    """
    path = _lock_path(root)
    if path.is_symlink():
        raise EditError(f"transaction lock must not be a symlink: {path}")
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
    except OSError as exc:
        raise EditError(f"cannot open the transaction lock: {path}: {exc}") from exc
    try:
        if os.name == "nt":
            msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        os.close(descriptor)
        raise EditError(
            f"another atomic_exact_edit invocation holds the transaction lock: {path}"
        ) from exc
    return descriptor


def _release_lock(descriptor: int) -> None:
    try:
        if os.name == "nt":
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
    except OSError:
        pass  # closing the descriptor below is the authoritative release
    finally:
        os.close(descriptor)


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def _journal_payload(root: Path, prepared: list[PreparedFile], state: str) -> dict[str, Any]:
    return {
        "version": JOURNAL_VERSION,
        "root": str(root),
        "state": state,
        "files": [
            {
                "path": item.path.relative_to(root).as_posix(),
                "mode": item.mode,
                "original_sha256": _sha256(item.original),
                "updated_sha256": _sha256(item.updated),
                "original_base64": base64.b64encode(item.original).decode("ascii"),
                "updated_base64": base64.b64encode(item.updated).decode("ascii"),
            }
            for item in prepared
        ],
    }


def _journal_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _create_journal(path: Path, payload: dict[str, Any]) -> None:
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise EditError(f"recovery journal already exists: {path}; run --recover") from exc
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_journal_bytes(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(path, 0o600)
    except Exception:
        path.unlink(missing_ok=True)
        raise


def _replace_journal(path: Path, payload: dict[str, Any]) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_journal_bytes(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _decode_journal_file(root: Path, raw: dict[str, Any], index: int) -> PreparedFile:
    if not isinstance(raw, dict):
        raise EditError(f"journal file {index} must be an object")
    expected = {"path", "mode", "original_sha256", "updated_sha256", "original_base64", "updated_base64"}
    if set(raw) != expected:
        raise EditError(f"journal file {index} has an invalid field set")
    target, display_path = _resolve_target(root, raw["path"], index)
    try:
        original = base64.b64decode(raw["original_base64"], validate=True)
        updated = base64.b64decode(raw["updated_base64"], validate=True)
    except (binascii.Error, ValueError, TypeError) as exc:
        raise EditError(f"journal file {index} has invalid base64 payloads") from exc
    if _sha256(original) != raw["original_sha256"]:
        raise EditError(f"{display_path}: journal original hash mismatch")
    if _sha256(updated) != raw["updated_sha256"]:
        raise EditError(f"{display_path}: journal updated hash mismatch")
    mode = raw["mode"]
    if isinstance(mode, bool) or not isinstance(mode, int) or mode < 0:
        raise EditError(f"{display_path}: journal mode is invalid")
    return PreparedFile(target, display_path, original, updated, mode)


def _load_journal(root: Path) -> tuple[Path, dict[str, Any], list[PreparedFile]]:
    path = _journal_path(root)
    if path.is_symlink():
        raise EditError(f"recovery journal must be a regular file, not a symlink: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EditError(f"recovery journal is unreadable: {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("version") != JOURNAL_VERSION:
        raise EditError(f"recovery journal has an unsupported shape: {path}")
    try:
        recorded_root = Path(payload["root"]).resolve(strict=True)
    except (KeyError, OSError, TypeError) as exc:
        raise EditError(f"recovery journal root is invalid: {path}") from exc
    if recorded_root != root:
        raise EditError(f"recovery journal root mismatch: {recorded_root} != {root}")
    state = payload.get("state")
    if state not in {"committing", "committed"}:
        raise EditError(f"recovery journal state is invalid: {state!r}")
    files = payload.get("files")
    if not isinstance(files, list) or not files:
        raise EditError("recovery journal must contain at least one file")
    prepared = [_decode_journal_file(root, raw, index) for index, raw in enumerate(files, 1)]
    seen: set[Path] = set()
    for item in prepared:
        if item.path in seen:
            raise EditError(
                f"{item.display_path}: recovery journal lists the same target more than once"
            )
        seen.add(item.path)
    return path, payload, prepared


def recover(root: Path) -> str:
    root = root.resolve(strict=True)
    journal = _journal_path(root)
    # exists() follows symlinks, so a dangling symlinked journal must still
    # reach _load_journal and fail closed instead of reporting NOT_NEEDED.
    if not journal.is_symlink() and not journal.exists():
        return "NOT_NEEDED"
    lock = _acquire_lock(root)
    try:
        return _recover_locked(root)
    finally:
        _release_lock(lock)


def _recover_locked(root: Path) -> str:
    path = _journal_path(root)
    if not path.is_symlink() and not path.exists():
        # The journal was finalized between the pre-lock check and lock
        # acquisition by whichever invocation held the lock first.
        return "NOT_NEEDED"
    path, payload, prepared = _load_journal(root)
    observed: list[bytes] = []
    for item in prepared:
        current = item.path.read_bytes()
        if current not in {item.original, item.updated}:
            raise EditError(
                f"{item.display_path}: recovery refused because current bytes match neither "
                "the journaled original nor updated payload"
            )
        observed.append(current)
    if payload["state"] == "committed":
        if any(current != item.updated for current, item in zip(observed, prepared)):
            raise EditError("committed recovery journal does not match every updated file")
        path.unlink()
        return "FINALIZED_COMMIT"
    for current, item in zip(observed, prepared):
        if current == item.updated:
            _restore(item)
    path.unlink()
    return "ROLLED_BACK_INTERRUPTED_APPLY"


def _test_crash_after() -> int | None:
    if os.environ.get(TEST_FAULT_ENABLE) != "1":
        return None
    raw = os.environ.get(TEST_CRASH_AFTER)
    if raw is None:
        return None
    try:
        value = int(raw)
    except ValueError as exc:
        raise EditError(f"{TEST_CRASH_AFTER} must be an integer") from exc
    if value < 1:
        raise EditError(f"{TEST_CRASH_AFTER} must be positive")
    return value


def apply(root: Path, prepared: list[PreparedFile]) -> None:
    root = root.resolve(strict=True)
    lock = _acquire_lock(root)
    try:
        _apply_locked(root, prepared)
    finally:
        _release_lock(lock)


def _apply_locked(root: Path, prepared: list[PreparedFile]) -> None:
    temporaries: dict[Path, Path] = {}
    replaced: list[PreparedFile] = []
    journal = _journal_path(root)
    journal_created = False
    crash_after = _test_crash_after()
    try:
        for item in prepared:
            if item.path.read_bytes() != item.original:
                raise EditError(f"{item.display_path}: changed after preflight")
            temporaries[item.path] = _write_temp(item, item.updated)
        for item in prepared:
            if item.path.read_bytes() != item.original:
                raise EditError(f"{item.display_path}: changed before atomic replace")
        payload = _journal_payload(root, prepared, "committing")
        _create_journal(journal, payload)
        journal_created = True
        for item in prepared:
            os.replace(temporaries.pop(item.path), item.path)
            replaced.append(item)
            if crash_after == len(replaced):
                os._exit(86)
        payload["state"] = "committed"
        _replace_journal(journal, payload)
        if crash_after == len(replaced) + 1:
            os._exit(86)
    except Exception as exc:
        rollback_failures = []
        for item in reversed(replaced):
            try:
                _restore(item)
            except Exception as rollback_exc:
                rollback_failures.append(f"{item.display_path}: {rollback_exc}")
        if rollback_failures:
            raise RollbackError(
                f"apply failed ({exc}); rollback also failed and the recovery journal was retained: "
                f"{'; '.join(rollback_failures)}"
            ) from exc
        if journal_created:
            try:
                journal.unlink(missing_ok=True)
            except OSError as cleanup_exc:
                raise EditError(
                    "apply failed and files were rolled back, but journal cleanup "
                    f"failed; run --recover: {cleanup_exc}"
                ) from exc
        if isinstance(exc, EditError):
            raise
        raise EditError(f"apply failed and completed files were rolled back: {exc}") from exc
    finally:
        for temporary in temporaries.values():
            temporary.unlink(missing_ok=True)
    try:
        journal.unlink()
    except OSError as exc:
        raise EditError(
            f"apply committed, but journal cleanup failed; run --recover to finalize: {exc}"
        ) from exc


def selftest() -> int:
    failures: list[str] = []

    def expect(label: str, condition: bool) -> None:
        print(("PASS " if condition else "FAIL ") + label)
        if not condition:
            failures.append(label)

    with tempfile.TemporaryDirectory() as directory:
        # Resolve so journal payloads built here relative_to() the same base
        # that prepare() resolves targets against (e.g. symlinked temp dirs).
        root = Path(directory).resolve()
        lf = root / "lf.txt"
        crlf = root / "crlf.txt"
        other = root / "other.txt"
        lf.write_bytes(b"alpha\nbeta\n")
        crlf.write_bytes(b"one\r\ntwo\r\n")
        other.write_bytes(b"keep\n")
        plan = {
            "version": 1,
            "replacements": [
                {"path": "lf.txt", "old": "beta\n", "new": "gamma\n"},
                {"path": "crlf.txt", "old": "two\n", "new": "three\n"},
            ],
        }
        prepared = prepare(root, plan)
        expect("preflight touches no files", lf.read_bytes() == b"alpha\nbeta\n")
        apply(root, prepared)
        expect("LF edit applied", lf.read_bytes() == b"alpha\ngamma\n")
        expect("CRLF preserved", crlf.read_bytes() == b"one\r\nthree\r\n")
        expect("unlisted file preserved", other.read_bytes() == b"keep\n")

        before_lf = lf.read_bytes()
        before_other = other.read_bytes()
        bad_plan = {
            "version": 1,
            "replacements": [
                {"path": "lf.txt", "old": "gamma", "new": "delta"},
                {"path": "other.txt", "old": "missing", "new": "changed"},
            ],
        }
        try:
            prepare(root, bad_plan)
            expect("mismatch fails preflight", False)
        except EditError:
            expect("mismatch fails preflight", True)
        expect("failed preflight changes nothing", lf.read_bytes() == before_lf)
        expect("later target also unchanged", other.read_bytes() == before_other)

        for label, bad in (
            (
                "path escape rejected",
                {"version": 1, "replacements": [{"path": "../x", "old": "a", "new": "b"}]},
            ),
            (
                "ambiguous count rejected",
                {"version": 1, "replacements": [{"path": "lf.txt", "old": "a", "new": "b"}]},
            ),
        ):
            try:
                prepare(root, bad)
                expect(label, False)
            except EditError:
                expect(label, True)

        mixed = root / "mixed.txt"
        mixed.write_bytes(b"a\r\nb\n")
        try:
            prepare(
                root,
                {"version": 1, "replacements": [{"path": "mixed.txt", "old": "a", "new": "z"}]},
            )
            expect("mixed newlines rejected", False)
        except EditError:
            expect("mixed newlines rejected", True)

        encoded = base64.b64encode(json.dumps(plan).encode("utf-8")).decode("ascii")
        decoded, _raw, digest = _decode_plan_base64(encoded)
        expect("base64 plan round trip", decoded == plan and len(digest) == 64)
        direct, _raw, direct_digest = _decode_plan_json(json.dumps(plan))
        expect("direct JSON plan round trip", direct == plan and len(direct_digest) == 64)
        cli_plan, _raw, cli_digest = _plan_from_replacements(
            [["lf.txt", r"gamma\n", r"delta\n"], ["other.txt", r"keep\n", r"kept\n"]]
        )
        expect(
            "repeated replacements decode escapes",
            cli_plan["replacements"][0]["old"] == "gamma\n" and len(cli_digest) == 64,
        )

        interrupted_plan = {
            "version": 1,
            "replacements": [
                {"path": "lf.txt", "old": "gamma", "new": "interrupted"},
                {"path": "other.txt", "old": "keep", "new": "changed"},
            ],
        }
        interrupted = prepare(root, interrupted_plan)
        interrupted_payload = _journal_payload(root, interrupted, "committing")
        _create_journal(_journal_path(root), interrupted_payload)
        first_temp = _write_temp(interrupted[0], interrupted[0].updated)
        os.replace(first_temp, interrupted[0].path)
        expect("interrupted apply leaves journal", _journal_path(root).exists())
        expect("recovery rolls back interrupted apply", recover(root) == "ROLLED_BACK_INTERRUPTED_APPLY")
        expect("recovery restores first file", lf.read_bytes() == interrupted[0].original)
        expect("recovery preserves untouched file", other.read_bytes() == interrupted[1].original)
        expect("recovery removes journal", not _journal_path(root).exists())

        committed = prepare(root, interrupted_plan)
        committed_payload = _journal_payload(root, committed, "committed")
        _create_journal(_journal_path(root), committed_payload)
        for item in committed:
            temporary = _write_temp(item, item.updated)
            os.replace(temporary, item.path)
        expect("committed recovery finalizes", recover(root) == "FINALIZED_COMMIT")
        expect("committed recovery keeps updated files", lf.read_bytes() == committed[0].updated)

        lock = _acquire_lock(root)
        try:
            _acquire_lock(root)
            expect("held transaction lock refuses reacquisition", False)
        except EditError:
            expect("held transaction lock refuses reacquisition", True)
        _release_lock(lock)
        _release_lock(_acquire_lock(root))
        expect("released transaction lock is reusable", True)
        lock_path = _lock_path(root)
        expect("transaction lock stays outside edited root", lock_path.parent != root)
        expect("transaction lock path is stable", lock_path == _lock_path(root))

        journal_path = _journal_path(root)
        tampered = _journal_payload(root, committed, "committing")
        tampered["files"][0]["updated_sha256"] = "0" * 64
        _create_journal(journal_path, tampered)
        try:
            recover(root)
            expect("tampered journal hash fails closed", False)
        except EditError:
            expect("tampered journal hash fails closed", True)
        expect("tampered journal is retained", journal_path.exists())
        escaping = _journal_payload(root, committed, "committing")
        escaping["files"][0]["path"] = "../escape.txt"
        _replace_journal(journal_path, escaping)
        try:
            recover(root)
            expect("escaping journal path fails closed", False)
        except EditError:
            expect("escaping journal path fails closed", True)
        journal_path.unlink()
        duplicated = _journal_payload(root, committed, "committing")
        duplicated["files"].append(duplicated["files"][0])
        _create_journal(journal_path, duplicated)
        try:
            recover(root)
            expect("duplicate journal target fails closed", False)
        except EditError:
            expect("duplicate journal target fails closed", True)
        expect("duplicate journal is retained", journal_path.exists())
        journal_path.unlink()

        try:
            journal_path.symlink_to(root / "missing-journal-target.json")
        except OSError:
            print("SKIP symlinked journal fails closed (symlink creation unavailable)")
        else:
            try:
                recover(root)
                expect("symlinked journal fails closed", False)
            except EditError:
                expect("symlinked journal fails closed", True)
            journal_path.unlink()

        expect("clean root needs no recovery", recover(root) == "NOT_NEEDED")
    print("SELFTEST", "OK" if not failures else "FAILED")
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", default=".", help="repository or snapshot root (default: .)"
    )
    plan_source = parser.add_mutually_exclusive_group()
    plan_source.add_argument("--plan-json", help="UTF-8 JSON plan as one argument")
    plan_source.add_argument("--plan-base64", help="base64-encoded UTF-8 JSON plan")
    plan_source.add_argument(
        "--replace", action="append", nargs=3, metavar=("PATH", "OLD", "NEW"),
        help="exact replacement triple; repeat as needed; single-quote values in PowerShell",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="preflight only; write nothing")
    action.add_argument(
        "--apply",
        action="store_true",
        help="preflight then apply (per-file atomic replaces plus a recovery journal)",
    )
    action.add_argument(
        "--recover", action="store_true", help="recover or finalize an interrupted apply"
    )
    parser.add_argument("--selftest", action="store_true", help="run built-in regression tests")
    args = parser.parse_args(argv)

    if args.selftest:
        if (
            args.plan_json
            or args.plan_base64
            or args.replace
            or args.check
            or args.apply
            or args.recover
        ):
            parser.error("--selftest cannot be combined with a plan or action")
        return selftest()
    if args.recover:
        if args.plan_json or args.plan_base64 or args.replace:
            parser.error("--recover cannot be combined with a plan")
        try:
            print(f"RECOVERY={recover(Path(args.root))}")
            return 0
        except EditError as exc:
            print(f"ATOMIC_EXACT_EDIT_ERROR={exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"ATOMIC_EXACT_EDIT_INTERNAL_ERROR={exc}", file=sys.stderr)
            return 2
    if not args.plan_json and not args.plan_base64 and not args.replace:
        parser.error("one of --replace, --plan-json, or --plan-base64 is required")
    if not args.check and not args.apply:
        parser.error("exactly one of --check or --apply is required")

    try:
        root = Path(args.root).resolve(strict=True)
        if args.apply:
            recovery = recover(root)
            if recovery != "NOT_NEEDED":
                print(f"RECOVERY={recovery}")
        elif _journal_path(root).exists():
            raise EditError("recovery journal exists; run --recover before --check")
        if args.plan_json:
            plan, _raw, digest = _decode_plan_json(args.plan_json)
        elif args.replace:
            plan, _raw, digest = _plan_from_replacements(args.replace)
        else:
            plan, _raw, digest = _decode_plan_base64(args.plan_base64)
        prepared = prepare(root, plan)
        print(f"PLAN_SHA256={digest}")
        print(f"PRECHECK=OK FILES={len(prepared)}")
        if args.apply:
            apply(root, prepared)
            print(f"APPLY=OK FILES={len(prepared)}")
        else:
            print("APPLY=NOT_RUN")
        return 0
    except RollbackError as exc:
        print(f"ATOMIC_EXACT_EDIT_ROLLBACK_ERROR={exc}", file=sys.stderr)
        return 3
    except EditError as exc:
        print(f"ATOMIC_EXACT_EDIT_ERROR={exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ATOMIC_EXACT_EDIT_INTERNAL_ERROR={exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
