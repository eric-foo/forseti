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


def apply(prepared: list[PreparedFile]) -> None:
    temporaries: dict[Path, Path] = {}
    replaced: list[PreparedFile] = []
    try:
        for item in prepared:
            if item.path.read_bytes() != item.original:
                raise EditError(f"{item.display_path}: changed after preflight")
            temporaries[item.path] = _write_temp(item, item.updated)
        for item in prepared:
            if item.path.read_bytes() != item.original:
                raise EditError(f"{item.display_path}: changed before atomic replace")
        for item in prepared:
            os.replace(temporaries.pop(item.path), item.path)
            replaced.append(item)
    except Exception as exc:
        rollback_failures = []
        for item in reversed(replaced):
            try:
                _restore(item)
            except Exception as rollback_exc:  # preserve the more severe state
                rollback_failures.append(f"{item.display_path}: {rollback_exc}")
        if rollback_failures:
            raise RollbackError(
                f"apply failed ({exc}); rollback also failed: {'; '.join(rollback_failures)}"
            ) from exc
        if isinstance(exc, EditError):
            raise
        raise EditError(f"apply failed and completed files were rolled back: {exc}") from exc
    finally:
        for temporary in temporaries.values():
            temporary.unlink(missing_ok=True)


def selftest() -> int:
    failures: list[str] = []

    def expect(label: str, condition: bool) -> None:
        print(("PASS " if condition else "FAIL ") + label)
        if not condition:
            failures.append(label)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
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
        apply(prepared)
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

    print("SELFTEST", "OK" if not failures else "FAILED")
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository or snapshot root (default: .)")
    plan_source = parser.add_mutually_exclusive_group()
    plan_source.add_argument(
        "--plan-json",
        help="UTF-8 JSON plan as one argument (PowerShell: wrap it in single quotes)",
    )
    plan_source.add_argument("--plan-base64", help="base64-encoded UTF-8 JSON plan")
    plan_source.add_argument(
        "--replace",
        action="append",
        nargs=3,
        metavar=("PATH", "OLD", "NEW"),
        help=(
            "exact replacement triple; repeat as needed. PowerShell: single-quote "
            "each value. OLD/NEW recognize \\n, \\t, and \\\\"
        ),
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="preflight only; write nothing")
    action.add_argument("--apply", action="store_true", help="preflight then atomically apply")
    parser.add_argument("--selftest", action="store_true", help="run built-in regression tests")
    args = parser.parse_args(argv)

    if args.selftest:
        if args.plan_json or args.plan_base64 or args.replace or args.check or args.apply:
            parser.error("--selftest cannot be combined with a plan or action")
        return selftest()
    if not args.plan_json and not args.plan_base64 and not args.replace:
        parser.error("one of --replace, --plan-json, or --plan-base64 is required")
    if not args.check and not args.apply:
        parser.error("exactly one of --check or --apply is required")

    try:
        if args.plan_json:
            plan, _raw, digest = _decode_plan_json(args.plan_json)
        elif args.replace:
            plan, _raw, digest = _plan_from_replacements(args.replace)
        else:
            plan, _raw, digest = _decode_plan_base64(args.plan_base64)
        prepared = prepare(Path(args.root), plan)
        print(f"PLAN_SHA256={digest}")
        print(f"PRECHECK=OK FILES={len(prepared)}")
        if args.apply:
            apply(prepared)
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
