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
EXPECTED_BINDINGS = ("CapturePacket", "EvidenceUnit", "Case")
EXPECTED_REQUIRED_FIELDS = {
    "CapturePacket": ("manifest_version",),
    "EvidenceUnit": ("evidence_id", "pre_decision_status"),
    "Case": ("case_id",),
}
EXPECTED_FORBIDS_FIELDS = {
    "EvidenceUnit": ("claim_tier",),
}
EXPECTED_COMPOSED_WITH = {
    "Case": ("orca-harness/schemas/scoring_models.py:CaseReport",),
}


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
    """True if cls is defined in module `mod`."""
    actual = getattr(cls, "__module__", "") or ""
    return actual == mod


def _string_list(
    value: object,
    concept: str,
    key: str,
    findings: list[str],
    *,
    require_non_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or (require_non_empty and not value):
        findings.append("%s: `%s` missing or malformed (drift-check invariant vacuous)" % (concept, key))
        return []
    if not all(isinstance(item, str) and item.strip() for item in value):
        findings.append("%s: `%s` contains a non-string/empty value (drift-check invariant vacuous)" % (concept, key))
        return []
    return [item.strip() for item in value]


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
    except Exception as exc:
        return ["ontology.yaml: cannot parse `%s` (%s: %s)" % (YAML_REL, type(exc).__name__, exc)]
    if not isinstance(ss, dict):
        return ["ontology.yaml: malformed top-level document (expected mapping)"]
    bindings = ss.get("runtime_bindings")

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
    if not isinstance(bindings, dict):
        return ["runtime_bindings: missing or malformed (expected scoped bindings: %s)" % ", ".join(EXPECTED_BINDINGS)]
    for expected in EXPECTED_BINDINGS:
        if expected not in bindings:
            findings.append("%s: runtime binding MISSING (drift-check invariant vacuous)" % expected)

    for concept, b in bindings.items():
        if not isinstance(b, dict):
            findings.append("%s: binding malformed (expected mapping)" % concept)
            continue
        runtime = b.get("runtime")
        if not isinstance(runtime, str) or not runtime.strip():
            findings.append("%s: `runtime` missing or malformed (drift-check invariant vacuous)" % concept)
            continue
        cls, mod, err = load(runtime)
        if cls is None:
            findings.append("%s: binding dangles -- cannot import `%s` (%s)" % (concept, runtime, err))
            continue
        if not _defined_here(cls, mod):
            findings.append(
                "%s: `%s` is re-exported (defined in `%s`, bound to `%s`)"
                % (concept, cls.__name__, getattr(cls, "__module__", "?"), mod)
            )
        fields = set(getattr(cls, "model_fields", {}) or {})
        requires_fields = _string_list(
            b.get("requires_fields"), concept, "requires_fields", findings, require_non_empty=True
        )
        missing_required_guards = set(EXPECTED_REQUIRED_FIELDS.get(concept, ())) - set(requires_fields)
        if missing_required_guards:
            findings.append(
                "%s: `requires_fields` missing required guard(s): %s"
                % (concept, ", ".join(sorted(missing_required_guards)))
            )
        for f in requires_fields:
            if f not in fields:
                findings.append("%s: required field `%s` MISSING on `%s` (drift)" % (concept, f, cls.__name__))
        forbids_fields = _string_list(b.get("forbids_fields"), concept, "forbids_fields", findings)
        missing_forbid_guards = set(EXPECTED_FORBIDS_FIELDS.get(concept, ())) - set(forbids_fields)
        if missing_forbid_guards:
            findings.append(
                "%s: `forbids_fields` missing required guard(s): %s"
                % (concept, ", ".join(sorted(missing_forbid_guards)))
            )
        for f in forbids_fields:
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
        else:
            findings.append("%s: `not_payload_identifier` missing or false (drift-check invariant vacuous)" % concept)
        composed_with = _string_list(b.get("composed_with", []), concept, "composed_with", findings)
        missing_composed_guards = set(EXPECTED_COMPOSED_WITH.get(concept, ())) - set(composed_with)
        if missing_composed_guards:
            findings.append(
                "%s: `composed_with` missing required guard(s): %s"
                % (concept, ", ".join(sorted(missing_composed_guards)))
            )
        for cspec in composed_with:
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
    sys.exit(main(sys.argv[1:]))
