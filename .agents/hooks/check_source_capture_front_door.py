#!/usr/bin/env python3
"""Online source-capture front-door reminder (advisory, never blocks).

WHAT THIS DOES
  When an agent reaches for a generic online tool (`WebSearch`, `WebFetch`) it
  injects a one-shot, non-blocking reminder: if the intent is to *capture or
  preserve a source as evidence* for an Orca decision, the sanctioned path is the
  Source Capture Armory runbook, not a free-form fetch/crawl. The *rule* — what
  the front door covers, the evidence-only scope, and the runner discipline — is
  owned by:

      .agents/workflow-overlay/source-loading.md   (-> "Online Source-Capture Front Door")
      orca-harness/docs/source_capture_agent_runbook.md   (the runner manual)

  This script does NOT restate that rule. It is a thin boundary nudge that
  references the authority above. If the rule and this checker ever disagree, the
  rule wins and this checker is the stale party.

WHY THIS EXISTS (enforcement placement)
  The runbook was reachable only if an agent already knew to open it; nothing
  caught the moment an agent decided to go online. Per the Enforcement Placement
  principle in
      .agents/workflow-overlay/validation-gates.md  (-> "Enforcement Placement")
  a load-bearing routing rule that is checkable at a tool boundary is enforced at
  that boundary, not left to actor memory. The owner chose ADVISORY (reminder,
  never deny): a free-form lookup of, e.g., library docs is legitimate and must
  not be blocked; only *source/evidence capture* belongs in the runbook, and the
  agent — not this hook — makes that judgment.

SCOPE (low-noise by design)
  - Fires ONLY for the generic online tools `WebSearch` and `WebFetch`. It does
    not touch dedicated MCP tools (docs lookups, browser, computer-use), which are
    frequently legitimate non-evidence use. The doctrine applies to any online
    source capture regardless of tool; the hook is the precise, low-false-positive
    arm of it.
  - Never blocks. PreToolUse returns exit 0 with an `additionalContext` note and
    no permission decision.
  - Fails OPEN on any error, so a bug here can never stop a tool call.

MODES
  check_source_capture_front_door.py --hook       PreToolUse hook (stdin JSON, exit 0)
  check_source_capture_front_door.py --selftest    decision-logic self-check

This is advisory tooling, not validation, readiness, source-access authorization,
or a source-access-boundary amendment. It reminds; it never grants permission to
run any capture.
"""

from __future__ import annotations

import argparse
import json
import sys

# Authorities this hook references (it does not restate the rule).
RULE_AUTHORITY = ".agents/workflow-overlay/source-loading.md (Online Source-Capture Front Door)"
RUNBOOK = "orca-harness/docs/source_capture_agent_runbook.md"
PRINCIPLE = ".agents/workflow-overlay/validation-gates.md (Enforcement Placement)"

# The generic online tools this hook nudges on. Dedicated MCP tools are out of
# scope on purpose (see SCOPE in the module docstring).
WATCHED_TOOLS = ("WebSearch", "WebFetch")


def note_for(tool_name: str) -> str:
    """The advisory reminder injected before a watched online tool runs."""
    return (
        "Source-capture front door (advisory, not blocking): you are about to use "
        f"`{tool_name}`. If the intent is to CAPTURE OR PRESERVE a source as "
        "evidence for an Orca decision, the sanctioned path is the Source Capture "
        f"Armory runbook ({RUNBOOK}): a bounded runner over an explicitly supplied "
        "input, preserving a provenance packet, with no broad search/crawl and no "
        "source-meaning inference. Ordinary non-evidence lookups (library/API docs, "
        "a quick fact check) need no packet and may proceed. Rule authority: "
        f"{RULE_AUTHORITY}; enforced at the tool boundary per {PRINCIPLE}."
    )


def emit(note: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "additionalContext": note}}))


def run_hook() -> int:
    """PreToolUse hook: read tool_name from stdin JSON, nudge for watched tools,
    never block, exit 0."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
        tool_name = data.get("tool_name")
    except (ValueError, AttributeError):
        return 0  # malformed payload -> stay silent, never block a call
    if not tool_name or tool_name not in WATCHED_TOOLS:
        return 0
    emit(note_for(tool_name))
    return 0


def selftest() -> int:
    ok = True
    # watched tools build a note that names the runbook and stays advisory
    for tool in WATCHED_TOOLS:
        n = note_for(tool)
        if RUNBOOK not in n or "not blocking" not in n or tool not in n:
            print("FAIL note-content", tool)
            ok = False
        else:
            print("PASS note-content", tool)
    # an unwatched tool name is silently skipped by the hook decision
    skip_ok = ("Bash" not in WATCHED_TOOLS) and ("mcp__docs__query" not in WATCHED_TOOLS)
    print(("PASS" if skip_ok else "FAIL"), "unwatched-skipped")
    ok = ok and skip_ok
    # emitted payload is valid hookSpecificOutput JSON
    import io
    buf, real = io.StringIO(), sys.stdout
    try:
        sys.stdout = buf
        emit(note_for("WebFetch"))
    finally:
        sys.stdout = real
    try:
        payload = json.loads(buf.getvalue())
        shape_ok = payload["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    except (ValueError, KeyError):
        shape_ok = False
    print(("PASS" if shape_ok else "FAIL"), "payload-shape")
    ok = ok and shape_ok
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Advisory online source-capture front-door reminder. "
        f"Rule authority: {RULE_AUTHORITY}")
    parser.add_argument("--hook", action="store_true",
                        help="PreToolUse hook mode (stdin JSON, exit 0)")
    parser.add_argument("--selftest", action="store_true",
                        help="run decision-logic self-check")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.hook:
        return run_hook()
    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: a hook bug must never block a tool call
        sys.stderr.write("source-capture-front-door: internal error, allowing: %s\n" % exc)
        sys.exit(0)
