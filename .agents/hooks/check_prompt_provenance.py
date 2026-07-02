#!/usr/bin/env python3
"""PostToolUse hook — inject the Orca Prompt Preflight on docs/prompts/** writes (advisory).

WHAT THIS DOES
  After a Write/Edit lands a file under docs/prompts/**, injects the Orca Prompt
  Preflight core (output mode · template kind · edit-permission+targets+branch ·
  reviews findings-first + no runtime-model routing · doctrine-change ->
  propagation receipt · destinations) so a routine prompt applies the prompt
  contract INLINE with no skill reload. Fused / delegated-review-patch / novel
  prompts still author through workflow-prompt-orchestrator.

  This is the real, agent-agnostic enforcement that replaces the invoke-ritual:
  the boundary nudge carries the checklist itself, not a bare "go reload the
  orchestrator" pointer. It evolved in place from the ratified config-proposal-P5
  provenance reminder (2026-06-12); the strong-mandate pointer it used to emit
  ("must be authored through workflow-prompt-orchestrator") went stale when the
  mandate was narrowed to routine -> preflight / novel -> full skill, so the
  payload now carries the narrowed two-depth routing.

WHY (enforcement placement)
  The prompt contract is owned by .agents/workflow-overlay/prompt-orchestration.md
  ("Orca Prompt Preflight" + "Author Through The Prompt Orchestrator"). Whether
  the contract was applied is not mechanically checkable from one tool call, so
  the checkable part -- a write into the canonical prompt surface -- gets a
  deterministic, always-fires injection of the checklist, per the Enforcement
  Placement principle in .agents/workflow-overlay/validation-gates.md.

HARD BOUNDARY -- remind only, never block, never verdict.
  Exit 0 always; fails OPEN. It cannot verify the contract was or was not
  applied, so the reminder asserts no violation. It does not fire for
  lane-scoped prompts carried in chat, a lane PR body/comment, or ignored
  docs/_inbox scratch; those are accepted only when prompt-orchestration.md
  classifies them as lane-scoped execution prompts and the author carries the
  preflight in the prompt body or PR comment. Canonical prompt artifacts still
  write under docs/prompts/** and fire this hook.

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
    "Prompt preflight (advisory, not blocking) -- this write landed under "
    "docs/prompts/**. Apply the Orca Prompt Preflight before treating the prompt "
    "as done; state, per prompt:\n"
    "  1. Output mode -- one of chat-only/file-write/review-report/"
    "paste-ready-chat/patch-queue, plus its write/report destination.\n"
    "  2. Template kind -- the bound template from template-registry.md, or none; "
    "template targets are prompt-shaping labels, never runtime-model routing.\n"
    "  3. Edit permission + targets + branch -- read-only/docs-write/patch-only/"
    "implementation-authorized; target files or dirs; workspace, branch, and "
    "dirty-state when repository state matters.\n"
    "  4. Reviews -- findings-first by default; bind any formal verdict, severity, "
    "or patch queue explicitly; no runtime-model recommendation, ranking, or "
    "implication.\n"
    "  5. Doctrine change -- product/architecture/workflow/validation/review/"
    "output doctrine or a lifecycle boundary carries a "
    "direction_change_propagation receipt or blocker (source-of-truth.md).\n"
    "  6. Destinations -- the input prompt-artifact path, and the exact "
    "output-artifact path written when the mode writes a durable artifact.\n"
    "Routine prompts apply this core inline -- no skill reload. Fused, "
    "delegated-review-patch, and novel/cross-lane prompts author through "
    "workflow-prompt-orchestrator. Rule owner: "
    ".agents/workflow-overlay/prompt-orchestration.md. Advisory only -- not a "
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
