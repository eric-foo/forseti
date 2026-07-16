#!/usr/bin/env python3
"""PostToolUse hook — inject the Forseti Prompt Preflight on docs/prompts/** writes (advisory).

WHAT THIS DOES
  After a Write/Edit lands a file under docs/prompts/**, injects the Forseti Prompt
  Preflight core in its elided form (always: output mode + destination ·
  edit-permission+targets+branch · destinations when couriered/durable; omit
  fields at their named default; cite repo constants from the shared preflight
  defaults instead of restating them) so a routine prompt applies the prompt
  contract INLINE with no skill reload. An eligible lane-scoped delegated patch
  prompt uses the compact pointer-first default; prompts matching the project
  owner's Full orchestration predicate use the full orchestrator.

  This is the real, agent-agnostic enforcement that replaces the invoke-ritual:
  the boundary nudge carries the checklist itself, not a bare "go reload the
  orchestrator" pointer. It evolved in place from the ratified config-proposal-P5
  provenance reminder (2026-06-12); the strong-mandate pointer it used to emit
  ("must be authored through workflow-prompt-orchestrator") went stale when the
  mandate was narrowed to routine -> preflight / novel -> full skill, so the
  payload now carries the narrowed two-depth routing.

WHY (enforcement placement)
  The prompt contract is owned by .agents/workflow-overlay/prompt-orchestration.md
  ("Forseti Prompt Preflight" + "Author Through The Prompt Orchestrator"). Whether
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

CONTEXT-TOKEN THROTTLE (once-per-session full checklist)
  The full checklist (~380 tokens) is injected on the FIRST in-scope prompt
  write of a session; later prompt writes in the same session get a one-line
  pointer back to it instead (~40 tokens). State is a tempdir marker keyed by
  the hook payload's session_id (_hooklib.mark_session_once). Fails OPEN to
  the full checklist: no session_id or any state error -> full reminder, so a
  throttle bug can only cost tokens, never the nudge.

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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import mark_session_once  # noqa: E402  (sys.path pin first)

REMINDER = (
    "Prompt preflight (advisory, not blocking) -- this write landed under "
    "docs/prompts/**. Apply the Forseti Prompt Preflight (elided form) before "
    "treating the prompt as done. Always state:\n"
    "  1. Output mode -- exactly one of chat-only/file-write/review-report/"
    "paste-ready-chat/patch-queue, plus its write/report destination.\n"
    "  2. Edit permission + targets + branch -- read-only/docs-write/patch-only/"
    "implementation-authorized; target files or dirs; workspace, branch, and "
    "dirty-state when repository state matters.\n"
    "  3. Destinations -- run-authoritative input source and exact "
    "output-artifact path -- when the prompt is couriered to another "
    "model/agent/thread/worktree or writes a durable artifact.\n"
    "Omit fields at their named default (an omitted field asserts it): "
    "template kind none; reviews findings-first with no formal verdict, "
    "severity, or patch queue bound and no runtime-model routing; doctrine "
    "change none -- a doctrine-changing prompt carries a "
    "direction_change_propagation receipt or blocker (source-of-truth.md).\n"
    "Cite repo constants (intake reads, external-source boundary, environment "
    "baseline, lifecycle hard stop, de-correlation constants) from "
    "docs/prompts/templates/shared/forseti_preflight_defaults_v0.md; do not "
    "restate them.\n"
    "Before using a durable or cross-recipient implementation-authorized "
    "codex_managed_worktree commission or an operator-courier "
    "delegated_code_review_and_patch prompt, gate its rendered body with "
    "`python .agents/hooks/check_prompt_output_mode.py --validate-stdin`; a "
    "green shape check never replaces receiver preflight.\n"
    "Routine prompts apply this core inline -- no skill reload. An eligible "
    "lane-scoped delegated review-and-patch prompt uses the compact "
    "pointer-first default. Prompts matching the Full orchestration predicate "
    "use workflow-prompt-orchestrator. Rule owner: "
    ".agents/workflow-overlay/prompt-orchestration.md. Advisory only -- not a "
    "verdict that the contract was skipped."
)

# Injected on later in-scope prompt writes of the same session, once the full
# checklist above has already been injected (context-token throttle).
SHORT_REMINDER = (
    "Prompt preflight (advisory) -- this write landed under docs/prompts/**. "
    "Re-apply the elided Forseti Prompt Preflight injected earlier this session "
    "(output mode+destination; edit permission+targets+branch; destinations "
    "when couriered/durable; defaulted fields omitted; constants cited from "
    "forseti_preflight_defaults_v0.md). Rule owner: "
    ".agents/workflow-overlay/prompt-orchestration.md."
)


def reminder_for(path: str, first_time: bool) -> str | None:
    """Pure decision: the reminder text for this write, or None when out of scope.

    First in-scope prompt write of a session -> the full checklist; later ones
    -> the one-line pointer."""
    if not is_prompt_path(str(path)):
        return None
    return REMINDER if first_time else SHORT_REMINDER


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
    if not is_prompt_path(str(path)):
        return 0
    session_id = data.get("session_id", "") if isinstance(data, dict) else ""
    # Fail OPEN to the full checklist: without a session_id there is no safe
    # session bucket (the shared "nosession" bucket would mute every future
    # session on this machine), so throttle only when the id is present.
    first_time = (not session_id) or mark_session_once(
        "prompt_preflight", str(session_id))
    msg = reminder_for(str(path), first_time)
    if msg:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": msg}}))
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

    # once-per-session throttle decision (pure)
    throttle_cases = [
        ("first write -> full checklist",
         reminder_for("docs/prompts/reviews/x_v0.md", True) == REMINDER),
        ("later write -> short pointer",
         reminder_for("docs/prompts/reviews/x_v0.md", False) == SHORT_REMINDER),
        ("out of scope -> silent either way",
         reminder_for("docs/decisions/a_v0.md", True) is None
         and reminder_for("docs/decisions/a_v0.md", False) is None),
        ("short pointer stays short",
         len(SHORT_REMINDER) < len(REMINDER) // 3),
        ("full reminder carries receiver and delegated-patch authoring gate",
         "--validate-stdin" in REMINDER
         and "codex_managed_worktree" in REMINDER
         and "delegated_code_review_and_patch" in REMINDER),
    ]
    for label, passed in throttle_cases:
        if not passed:
            ok = False
        print("%s throttle  %s" % ("PASS" if passed else "FAIL", label))

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
