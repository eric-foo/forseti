#!/usr/bin/env python3
"""PostToolUse hook — remind that docs/prompts/** is orchestrator-owned (advisory).

WHAT THIS DOES
  After a Write/Edit lands a file under docs/prompts/**, returns a one-line
  reminder that prompt, handoff, wrapper, rerun, and patch artifacts must be
  authored through workflow-prompt-orchestrator (or carry an applied-contract
  record). The observed failure mode is hand-drafted prompts caught only by
  the owner after the fact (>=4 sessions); this moves the nudge to the tool
  boundary at the moment of the write (ratified config proposal P5,
  2026-06-12).

WHY (enforcement placement)
  The routing rule is owned by .agents/workflow-overlay/prompt-orchestration.md
  ("Author Through The Prompt Orchestrator"). Whether the orchestrator ran is
  not mechanically checkable from one tool call, so the checkable part — a
  write into an orchestrator-owned folder — gets a deterministic reminder, per
  the Enforcement Placement principle in
  .agents/workflow-overlay/validation-gates.md.

HARD BOUNDARY — remind only, never block, never verdict.
  Exit 0 always; fails OPEN. It cannot verify the orchestrator was or was not
  used, so the reminder asserts no violation. It misses paste-ready-chat
  prompts that never touch disk (named, accepted limitation).

MODES
  check_prompt_provenance.py --hook      PostToolUse hook (stdin JSON, exit 0)
  check_prompt_provenance.py --selftest  pure-decision cases

REGISTRATION (.claude/settings.json, PostToolUse, matcher "Write|Edit")
  { "type": "command",
    "command": "python \"$CLAUDE_PROJECT_DIR/.agents/hooks/check_prompt_provenance.py\" --hook",
    "timeout": 10 }
  Hooks load at session start; restart the session after editing settings.
"""
from __future__ import annotations

import json
import sys

REMINDER = (
    "This write landed under docs/prompts/** (orchestrator-owned). Prompt, "
    "handoff, wrapper, rerun, and patch artifacts must be authored through "
    "workflow-prompt-orchestrator, or carry an applied-contract record per "
    ".agents/workflow-overlay/prompt-orchestration.md. If this artifact was "
    "orchestrator-authored, ignore this reminder. Advisory only -- not a "
    "verdict that the contract was skipped."
)


def is_prompt_path(path: str) -> bool:
    """True when the path is inside docs/prompts/ (pure function).

    Handles backslashes and absolute paths; requires a real path segment so
    e.g. docs/promptsx/ does not match."""
    if not path:
        return False
    p = path.replace("\\", "/")
    return p.startswith("docs/prompts/") or "/docs/prompts/" in p


def run_hook() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    tool_input = data.get("tool_input", {}) if isinstance(data, dict) else {}
    path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
    if is_prompt_path(str(path)):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": REMINDER}}))
    return 0


def selftest() -> int:
    cases = [
        ("docs/prompts/reviews/x_prompt_v0.md", True),
        ("docs\\prompts\\handoffs\\y_v0.md", True),
        ("C:\\Users\\u\\projects\\orca\\docs\\prompts\\z.md", True),
        ("/c/users/u/orca/docs/prompts/templates/t.md", True),
        ("docs/promptsx/a.md", False),
        ("docs/decisions/a_v0.md", False),
        ("", False),
    ]
    ok = True
    for i, (path, expect) in enumerate(cases, 1):
        got = is_prompt_path(path)
        status = "PASS" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print("%s case %02d  expect=%s got=%s  %s" % (status, i, expect, got, path))
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    return run_hook()  # default / --hook: PostToolUse hook mode


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: a reminder bug must never block a tool
        sys.stderr.write("check_prompt_provenance: internal error, allowing: %s\n" % exc)
        sys.exit(0)
