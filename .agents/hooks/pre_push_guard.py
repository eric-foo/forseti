#!/usr/bin/env python3
"""Orca local Git pre-push guard.

Reads Git pre-push updates from stdin:

    <local-ref> <local-sha> <remote-ref> <remote-sha>

Blocks pushes targeting main, branch deletions, non-fast-forward updates, and
updates whose fast-forward safety cannot be verified. This is a Git-bound local
adapter, not a Claude/Codex tool hook. It is bypassable with --no-verify and
does not see GitHub API actions such as `gh pr merge`.
"""

from __future__ import annotations

import subprocess
import sys

ZERO = "0" * 40
MAIN_REFS = {"main", "refs/heads/main"}


def _is_ancestor(remote_sha: str, local_sha: str) -> int:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", remote_sha, local_sha],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode


def decide_update(local_ref: str, local_sha: str, remote_ref: str, remote_sha: str) -> str | None:
    """Return a block reason, or None to allow the update."""
    if remote_ref in MAIN_REFS:
        return f"push targets main ({remote_ref})"
    if local_sha == ZERO:
        return f"branch deletion push ({remote_ref})"
    if remote_sha != ZERO:
        rc = _is_ancestor(remote_sha, local_sha)
        if rc == 1:
            return f"non-fast-forward push to {remote_ref}"
        if rc != 0:
            return f"could not verify fast-forward safety for {remote_ref}"
    return None


def iter_updates(stdin_text: str):
    for raw in stdin_text.splitlines():
        parts = raw.split()
        if not parts:
            continue
        if len(parts) != 4:
            yield None, f"malformed pre-push update line: {raw[:160]}"
            continue
        yield parts, None


def check_stdin(stdin_text: str) -> list[str]:
    reasons: list[str] = []
    for update, parse_error in iter_updates(stdin_text):
        if parse_error:
            reasons.append(parse_error)
            continue
        reason = decide_update(*update)
        if reason:
            reasons.append(reason)
    return reasons


def block(reasons: list[str]) -> int:
    print("BLOCKED by Orca local pre-push guard (.githooks/pre-push).", file=sys.stderr)
    for reason in reasons:
        print(f"Reason: {reason}", file=sys.stderr)
    print("Authority: .agents/workflow-overlay/safety-rules.md + dev-workflow doctrine.", file=sys.stderr)
    print("Boundary: local Git hook only; --no-verify can bypass it.", file=sys.stderr)
    return 1


def selftest() -> int:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    cases = [
        ("new lane branch", f"refs/heads/lane {head} refs/heads/lane {ZERO}\n", False),
        ("main target", f"refs/heads/lane {head} refs/heads/main {ZERO}\n", True),
        ("delete branch", f"refs/heads/lane {ZERO} refs/heads/lane {head}\n", True),
        ("already up to date", f"refs/heads/lane {head} refs/heads/lane {head}\n", False),
        ("malformed line", "not enough fields\n", True),
    ]
    ok = True
    for name, payload, expect_block in cases:
        got_block = bool(check_stdin(payload))
        status = "PASS" if got_block == expect_block else "FAIL"
        if got_block != expect_block:
            ok = False
        print(f"{status} {name} expect_block={expect_block} got_block={got_block}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    reasons = check_stdin(sys.stdin.read())
    if reasons:
        return block(reasons)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
