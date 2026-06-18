#!/usr/bin/env python3
"""Ontology pull-trigger nudge -- reads the deferred-expansion backlog (rung 0) and
reports which adopted ontology types are now buildable but still un-carded (rung 1).

WHAT THIS DOES
  Reads orca/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json (the rung-0
  backlog).  For each auto-nudge trigger, the nudge FIRES when BOTH hold:
    (a) the trigger artifact has landed on disk (trigger_path exists), and
    (b) at least one owed card is still missing (no file matches its card_glob
        in the backlog's cards_dir).
  The owed type(s) are then "due": a dated trigger artifact made them buildable,
  but the card has not been written yet.  The owner is nudged at every session
  start (via the session-context capsule) so the expansion is not forgotten --
  no remembering required.

  This is the "agent nudges me" half of the pull-trigger wiring.  The backlog is
  the data; this hook is the check that reads it.  Pointers only: the adopted
  deliverable (orca_ontology_backbone_architecture_v0.md, §2.2/§3/§4/§9) is the
  authority for what each type is and why it is deferred.

MODES
  check_ontology_expansion.py --health            Full human-readable report. Exit 0.
  check_ontology_expansion.py --health --oneline  Single capsule line IFF >=1 type
                                                  is due (else prints nothing). Exit 0.
  check_ontology_expansion.py --selftest          Pure-function cases. Exit 0/1.

HARD BOUNDARY
  Read-only.  No writes.  Advisory only -- never blocks anything (always exit 0
  except --selftest).  Fails OPEN: a missing/unparseable backlog, a bad path, or
  any internal error yields NO nudge (omitted line), never a stall or a crash.

WHY THIS EXISTS (enforcement placement)
  A deferred-expansion list nobody actively watches still requires the owner to
  remember to check it.  Coupling the check to the session-start capsule turns
  the passive backlog into an automatic nudge that fires exactly when a type
  becomes buildable.  Enforcement-placement principle:
    .agents/workflow-overlay/validation-gates.md -> "Enforcement Placement"

REGISTRATION
  Capsule: session_context_capsule.py calls --health --oneline with a 5s timeout
  (same pattern as header_index.py's retrieval-health line).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BACKLOG_RELPATH = "orca/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json"


def repo_root() -> Path:
    """Repo root derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# I/O: load backlog (fail-open)
# ---------------------------------------------------------------------------

def load_backlog(root: Path) -> dict | None:
    """Load the rung-0 backlog JSON. Returns None on any problem (fail-open)."""
    path = root / BACKLOG_RELPATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


# ---------------------------------------------------------------------------
# Pure decision
# ---------------------------------------------------------------------------

def compute_due(backlog: dict,
                trigger_fired: dict[str, bool],
                card_present: dict[str, bool]) -> list[str]:
    """Return the ordered unique list of ontology type names that are DUE.

    A type is due when its trigger fired (trigger_fired[trigger_id] is True) and
    its card is absent (card_present[card_glob] is False).

    Pure function: callers inject trigger_fired (by trigger id) and card_present
    (by card_glob), so disk access is testable.
    """
    due: list[str] = []
    for trig in backlog.get("auto_nudge_triggers", []):
        if not trigger_fired.get(trig.get("id", ""), False):
            continue
        for owed in trig.get("cards_owed", []):
            typ = owed.get("type", "")
            glob = owed.get("card_glob", "")
            if typ and not card_present.get(glob, False) and typ not in due:
                due.append(typ)
    return due


def oneline(due_types: list[str]) -> str | None:
    """Capsule line IFF >=1 type is due, else None (omit the line). Pure."""
    if not due_types:
        return None
    return "ontology expansion: %d type%s due (%s)" % (
        len(due_types), "s" if len(due_types) != 1 else "", ", ".join(due_types))


# ---------------------------------------------------------------------------
# I/O wrappers
# ---------------------------------------------------------------------------

def _trigger_fired_map(backlog: dict, root: Path) -> dict[str, bool]:
    out: dict[str, bool] = {}
    for trig in backlog.get("auto_nudge_triggers", []):
        tpath = trig.get("trigger_path", "")
        out[trig.get("id", "")] = bool(tpath) and (root / tpath).exists()
    return out


def _card_present_map(backlog: dict, root: Path) -> dict[str, bool]:
    cards_dir = root / backlog.get("cards_dir", "")
    out: dict[str, bool] = {}
    for trig in backlog.get("auto_nudge_triggers", []):
        for owed in trig.get("cards_owed", []):
            glob = owed.get("card_glob", "")
            if not glob or glob in out:
                continue
            try:
                out[glob] = any(cards_dir.glob(glob))
            except OSError:
                out[glob] = False
    return out


def due_types(root: Path, backlog: dict) -> list[str]:
    return compute_due(backlog,
                       _trigger_fired_map(backlog, root),
                       _card_present_map(backlog, root))


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def run_health(root: Path, oneline_mode: bool, verbose: bool) -> int:
    backlog = load_backlog(root)
    if backlog is None:
        if not oneline_mode:
            print("ontology expansion: backlog absent or unreadable (%s) -- no nudge"
                  % BACKLOG_RELPATH)
        return 0  # fail-open: omit the capsule line
    due = due_types(root, backlog)
    if oneline_mode:
        line = oneline(due)
        if line:
            print(line)
        return 0
    # Full report
    if not due:
        print("ontology expansion: none due "
              "(no landed trigger has an un-carded owed type)")
    else:
        print("ontology expansion: %d type(s) due: %s" % (len(due), ", ".join(due)))
        if verbose:
            for trig in backlog.get("auto_nudge_triggers", []):
                print("  trigger %s (%s) -> %s"
                      % (trig.get("id"), trig.get("trigger_path"),
                         trig.get("action", "")))
    return 0


# ---------------------------------------------------------------------------
# Mode: --selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    backlog = {
        "cards_dir": "x",
        "auto_nudge_triggers": [
            {"id": "t1", "trigger_path": "p1", "cards_owed": [
                {"type": "Observation", "card_glob": "observation_*.md"},
                {"type": "TrendVector", "card_glob": "trend_*.md"},
            ]},
            {"id": "t2", "trigger_path": "p2", "cards_owed": [
                {"type": "Memo", "card_glob": "memo_*.md"},
            ]},
        ],
    }

    print("--- compute_due ---")
    due_cases = [
        ("none fired", {"t1": False, "t2": False},
         {"observation_*.md": False, "trend_*.md": False, "memo_*.md": False}, []),
        ("t1 fired, no cards", {"t1": True, "t2": False},
         {"observation_*.md": False, "trend_*.md": False, "memo_*.md": False},
         ["Observation", "TrendVector"]),
        ("t1 fired, obs carded", {"t1": True, "t2": False},
         {"observation_*.md": True, "trend_*.md": False, "memo_*.md": False},
         ["TrendVector"]),
        ("t1 fired, all carded", {"t1": True, "t2": False},
         {"observation_*.md": True, "trend_*.md": True, "memo_*.md": False}, []),
        ("both fired, memo missing", {"t1": True, "t2": True},
         {"observation_*.md": True, "trend_*.md": True, "memo_*.md": False}, ["Memo"]),
    ]
    for label, fired, present, expected in due_cases:
        got = compute_due(backlog, fired, present)
        passed = got == expected
        ok = ok and passed
        print("%s  %-26s expect=%s got=%s"
              % ("PASS" if passed else "FAIL", label, expected, got))

    print()
    print("--- oneline ---")
    ol_cases = [
        ("empty -> None", oneline([]) is None),
        ("one type", oneline(["Memo"]) == "ontology expansion: 1 type due (Memo)"),
        ("multi", oneline(["Observation", "TrendVector"])
         == "ontology expansion: 2 types due (Observation, TrendVector)"),
    ]
    for label, passed in ol_cases:
        ok = ok and passed
        print("%s  %s" % ("PASS" if passed else "FAIL", label))

    print()
    print("--- load_backlog (fail-open) ---")
    import tempfile
    fb_ok = True
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        # missing file -> None
        fb_ok = fb_ok and (load_backlog(tdp) is None)
        # malformed json -> None
        bad = tdp / BACKLOG_RELPATH
        bad.parent.mkdir(parents=True, exist_ok=True)
        bad.write_text("{not json", encoding="utf-8")
        fb_ok = fb_ok and (load_backlog(tdp) is None)
        # valid dict -> dict
        bad.write_text('{"cards_dir": "x"}', encoding="utf-8")
        fb_ok = fb_ok and (load_backlog(tdp) == {"cards_dir": "x"})
    ok = ok and fb_ok
    print("%s  load_backlog missing/malformed/valid" % ("PASS" if fb_ok else "FAIL"))

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        print("check_ontology_expansion: could not determine repo root: %s" % exc,
              file=sys.stderr)
        return 0  # fail open
    if "--health" in argv:
        return run_health(root, oneline_mode="--oneline" in argv,
                          verbose="--verbose" in argv)
    print("Usage: check_ontology_expansion.py --health [--oneline] [--verbose] | --selftest")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: an advisory bug must never stall a session
        sys.stderr.write(
            "check_ontology_expansion: internal error, failing open: %s\n" % exc)
        sys.exit(0)
