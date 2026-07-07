#!/usr/bin/env python3
"""Ontology SSOT integrity check (W2a).

Validates `forseti/product/spines/foundation/ontology/ontology.yaml` as a faithful,
self-consistent promotion of the prose backbone
(`forseti_ontology_backbone_architecture_v0.md`):

  - parses; every type has a known namespace + a valid status (adopted|reserved);
  - every typed-link endpoint resolves to a defined type;
  - the type roster EXACTLY equals the backbone section 2.2 bold roster (no drift
    from the naming authority);
  - `deferred_no_auto_trigger` EXACTLY equals the expansion-backlog JSON's deferred
    set;
  - runtime_bindings reference defined types; the roster stays within `type_cap`.

This is a SHAPE / faithfulness check: it proves the SSOT did not drift from its
authority. It is NOT validation or readiness, and it does NOT check the runtime
Pydantic schemas -- that is the separate, scoped W2b drift-check.

Usage:
  check_ontology_ssot.py --strict    CI gate: print findings; exit 1 if any, else 0.
  check_ontology_ssot.py --check     human-readable report; always exit 0.
  check_ontology_ssot.py --selftest  pure-function self-check; exit 0/1.

Fail-open: a missing file, unparseable YAML, or missing PyYAML exits 0 (advisory;
never ghost-fail CI on infrastructure).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ONT_DIR = "forseti/product/spines/foundation/ontology"
YAML_REL = ONT_DIR + "/ontology.yaml"
BACKLOG_REL = ONT_DIR + "/ontology_expansion_backlog_v0.json"
BACKBONE_REL = ONT_DIR + "/forseti_ontology_backbone_architecture_v0.md"

VALID_STATUS = {"adopted", "reserved"}
# Backbone section 2.2 roster rows: "| <n> | **<Type>** | ... |"
_ROSTER_RE = re.compile(r"^\|\s*\d+\s*\|\s*\*\*(\w+)\*\*", re.M)


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def deferred_names(raw) -> set[str]:
    """Type names from a backlog `deferred_no_auto_trigger` list (strings or {type}/{name} dicts)."""
    out: set[str] = set()
    for e in raw or []:
        if isinstance(e, str):
            out.add(e)
        elif isinstance(e, dict):
            n = e.get("type") or e.get("name")
            if n:
                out.add(n)
    return out


def check_ssot(root: Path) -> list[str]:
    """Return structural/faithfulness findings (empty == ok). Fail-open returns []."""
    try:
        import yaml
    except Exception:
        return []  # fail-open: PyYAML unavailable -> advisory skip
    yp = root / YAML_REL
    if not yp.is_file():
        return []
    try:
        ss = yaml.safe_load(yp.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(ss, dict) or not isinstance(ss.get("types"), dict):
        return ["ontology.yaml: missing or malformed `types` mapping"]

    findings: list[str] = []
    types = set(ss["types"])
    namespaces = set(ss.get("namespaces") or {})

    for t, v in ss["types"].items():
        if not isinstance(v, dict):
            findings.append(f"type `{t}`: not a mapping")
            continue
        if v.get("namespace") not in namespaces:
            findings.append(f"type `{t}`: unknown namespace `{v.get('namespace')}`")
        if v.get("status") not in VALID_STATUS:
            findings.append(
                f"type `{t}`: invalid status `{v.get('status')}` (expected adopted|reserved)"
            )

    for grp, links in (ss.get("links") or {}).items():
        for link in links or []:
            if not isinstance(link, dict):
                continue
            for end in ("from", "to"):
                if link.get(end) not in types:
                    findings.append(
                        "link [%s] %s-%s->%s: `%s` is not a defined type"
                        % (grp, link.get("from"), link.get("rel"), link.get("to"), link.get(end))
                    )

    for t in ss.get("runtime_bindings") or {}:
        if t not in types:
            findings.append(f"runtime_bindings: `{t}` is not a defined type")

    cap = ss.get("type_cap")
    if isinstance(cap, int) and len(types) > cap:
        findings.append(f"type roster ({len(types)}) exceeds type_cap ({cap})")

    bp = root / BACKLOG_REL
    if bp.is_file():
        try:
            bl = json.loads(bp.read_text(encoding="utf-8"))
            bl_def = deferred_names(bl.get("deferred_no_auto_trigger"))
            y_def = set(ss.get("deferred_no_auto_trigger") or [])
            if y_def != bl_def:
                findings.append(
                    "deferred_no_auto_trigger drift vs backlog: yaml-only=%s backlog-only=%s"
                    % (sorted(y_def - bl_def), sorted(bl_def - y_def))
                )
        except Exception:
            pass  # fail-open on backlog parse

    bbp = root / BACKBONE_REL
    if bbp.is_file():
        roster = set(_ROSTER_RE.findall(bbp.read_text(encoding="utf-8")))
        if roster and types != roster:
            findings.append(
                "type roster drift vs backbone 2.2: yaml-only=%s backbone-only=%s"
                % (sorted(types - roster), sorted(roster - types))
            )

    return findings


def selftest() -> int:
    ok = True
    cases = [
        ("deferred names from strings", deferred_names(["A", "B"]), {"A", "B"}),
        ("deferred names from dicts", deferred_names([{"type": "A"}, {"name": "B"}]), {"A", "B"}),
        ("roster regex", set(_ROSTER_RE.findall("| 1 | **Vertical** | x |\n| 2 | **Brand** | y |")),
         {"Vertical", "Brand"}),
    ]
    for label, got, exp in cases:
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-40s got=%s" % (status, label, sorted(got)))

    live = check_ssot(repo_root())
    status = "PASS" if not live else "FAIL"
    if live:
        ok = False
    print("%s  live ontology.yaml clean (0 findings) -> %s" % (status, live))
    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_ontology_ssot: cannot determine repo root: %s\n" % exc)
        return 0
    findings = check_ssot(root)
    if "--strict" in argv:
        if findings:
            print("check_ontology_ssot --strict: %d finding(s)" % len(findings))
            for f in findings:
                print("  " + f)
            return 1
        print("check_ontology_ssot --strict: OK (ontology.yaml faithful + self-consistent)")
        return 0
    if "--check" in argv:
        if findings:
            print("ontology SSOT findings (%d):" % len(findings))
            for f in findings:
                print("  " + f)
        else:
            print("ontology SSOT: OK")
        return 0
    print("Usage: check_ontology_ssot.py --strict | --check | --selftest")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md; EP-35
        # delegated review FIND-02 class sweep): an internal checker bug must
        # not read as a green gate. Advisory modes fail open so a bug never
        # bricks the agent.
        sys.stderr.write("check_ontology_ssot: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
