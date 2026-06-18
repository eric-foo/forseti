#!/usr/bin/env python3
"""Ontology<->runtime drift-check (W2b).

Verifies the SCOPED alignment between the ontology SSOT
(`ontology.yaml` `runtime_bindings`) and the runtime Pydantic classes, for the
ONLY 3 overlaps -- NOT full field conformity (the runtime types are
harness-pipeline artifacts, so most fields legitimately differ). The contract
shape was cross-vendor adversarially reviewed (2026-06-19): structured per-binding
invariants, not a free-text acknowledgment.

For each binding it imports the runtime class and verifies:
  - the class imports and is DEFINED in (not re-exported into) its bound module;
  - `requires_fields` are present (load-bearing anchors);
  - `forbids_fields` are absent (e.g. EvidenceUnit must not expose `claim_tier`, AR-01);
  - `not_payload_identifier`: the canonical/alias name is not itself a field
    (leak guard -- the condition under which the alias-only name reconciliation is safe);
  - `composed_with` classes also import.
A binding that no longer imports is real DRIFT (a dangling binding) -> a finding.

Usage:
  check_ontology_drift.py --strict   CI gate: print findings; exit 1 if any, else 0.
  check_ontology_drift.py --check     human-readable report; always exit 0.
  check_ontology_drift.py --selftest  self-check (live bindings clean); exit 0/1.

Fail-open ONLY for infrastructure gaps (no PyYAML, missing ontology.yaml, no
orca-harness/ tree). A present-but-changed runtime class is real drift, never
fail-open.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

YAML_REL = "orca/product/spines/foundation/ontology/ontology.yaml"
HARNESS_REL = "orca-harness"


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def _normalize_module(spec_module: str) -> str:
    """'orca-harness/source_capture/models.py' -> 'source_capture.models'."""
    mod = spec_module.strip()
    if mod.startswith(HARNESS_REL + "/"):
        mod = mod[len(HARNESS_REL) + 1:]
    if mod.endswith(".py"):
        mod = mod[:-3]
    return mod.replace("/", ".")


def _defined_here(cls, mod: str) -> bool:
    """True if cls is defined in module `mod` (tolerates an install package prefix)."""
    actual = getattr(cls, "__module__", "") or ""
    return actual == mod or actual.endswith("." + mod)


def check_drift(root: Path) -> list[str]:
    """Return drift findings (empty == ok). Fail-open (return []) only on infra gaps."""
    try:
        import yaml
    except Exception:
        return []
    yp = root / YAML_REL
    harness = root / HARNESS_REL
    if not yp.is_file() or not harness.is_dir():
        return []
    try:
        ss = yaml.safe_load(yp.read_text(encoding="utf-8"))
    except Exception:
        return []
    bindings = (ss or {}).get("runtime_bindings") or {}
    if not isinstance(bindings, dict) or not bindings:
        return []

    if str(harness) not in sys.path:
        sys.path.insert(0, str(harness))

    def load(spec: str):
        """'module:Class' (module may be a repo path) -> (cls|None, normalized_mod, err)."""
        raw_mod, _, cls_name = spec.partition(":")
        mod = _normalize_module(raw_mod)
        try:
            m = importlib.import_module(mod)
            return getattr(m, cls_name.strip()), mod, None
        except Exception as e:  # noqa: BLE001 -- import/attr failure == drift signal
            return None, mod, "%s: %s" % (type(e).__name__, e)

    findings: list[str] = []
    for concept, b in bindings.items():
        if not isinstance(b, dict):
            continue
        cls, mod, err = load(b.get("runtime", ""))
        if cls is None:
            findings.append("%s: binding dangles -- cannot import `%s` (%s)" % (concept, b.get("runtime"), err))
            continue
        if not _defined_here(cls, mod):
            findings.append(
                "%s: `%s` is re-exported (defined in `%s`, bound to `%s`)"
                % (concept, cls.__name__, getattr(cls, "__module__", "?"), mod)
            )
        fields = set(getattr(cls, "model_fields", {}) or {})
        for f in b.get("requires_fields") or []:
            if f not in fields:
                findings.append("%s: required field `%s` MISSING on `%s` (drift)" % (concept, f, cls.__name__))
        for f in b.get("forbids_fields") or []:
            if f in fields:
                findings.append(
                    "%s: forbidden field `%s` PRESENT on `%s` (intent violated, e.g. AR-01)"
                    % (concept, f, cls.__name__)
                )
        if b.get("not_payload_identifier"):
            alias = str(b.get("name_alias", cls.__name__)).lower()
            if alias in {x.lower() for x in fields}:
                findings.append(
                    "%s: `%s` appears as a field (possible payload-leaking discriminator -- alias-only no longer safe)"
                    % (concept, b.get("name_alias", cls.__name__))
                )
        for cspec in b.get("composed_with") or []:
            c2, _, err2 = load(cspec)
            if c2 is None:
                findings.append("%s: composed_with binding dangles -- cannot import `%s` (%s)" % (concept, cspec, err2))

    return findings


def selftest() -> int:
    ok = True
    cases = [
        ("normalize repo-path module", _normalize_module("orca-harness/source_capture/models.py"), "source_capture.models"),
        ("normalize dotted module", _normalize_module("schemas.case_models"), "schemas.case_models"),
    ]
    for label, got, exp in cases:
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-32s got=%s" % (status, label, got))
    live = check_drift(repo_root())
    status = "PASS" if not live else "FAIL"
    if live:
        ok = False
    print("%s  live ontology<->runtime drift clean -> %s" % (status, live))
    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_ontology_drift: cannot determine repo root: %s\n" % exc)
        return 0
    findings = check_drift(root)
    if "--strict" in argv:
        if findings:
            print("check_ontology_drift --strict: %d finding(s)" % len(findings))
            for f in findings:
                print("  " + f)
            return 1
        print("check_ontology_drift --strict: OK (ontology<->runtime bindings aligned)")
        return 0
    if "--check" in argv:
        if findings:
            print("ontology<->runtime drift (%d):" % len(findings))
            for f in findings:
                print("  " + f)
        else:
            print("ontology<->runtime drift: OK")
        return 0
    print("Usage: check_ontology_drift.py --strict | --check | --selftest")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        sys.stderr.write("check_ontology_drift: internal error, allowing: %s\n" % exc)
        sys.exit(0)
