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
  - `not_payload_identifier`: none of the binding's interchangeable names
    {ontology concept, runtime __name__, name_alias} is a self-identifier on the
    runtime class's (or any `composed_with` class's) TOP-LEVEL serialized surface --
    a field/computed-field name, a `Literal`/`Enum` discriminator value, or a
    serialized alias (`alias`/`serialization_alias`; not `validation_alias`). SCOPE:
    top-level class-local only; values nested inside member models are out of scope
    (documented limitation). A discriminated-union field yields a readiness finding
    (its nested tag value is unseeable top-level -- extend with recursion). See
    docs/decisions/ontology_runtime_drift_check_contract_v0.md;
  - `composed_with` classes import AND get the same top-level leak + readiness scan.
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

import enum
import importlib
import sys
import typing
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


def _annotation_strings(annotation: object) -> set[str]:
    """Every string a field with this annotation can SERIALIZE as a discriminator:
    `Literal` string values and `Enum` member `.value`s, recursing through
    Optional/Union/Annotated. Covers `f: SomeEnum`, `Literal["x"]`,
    `Literal[SomeEnum.X]`, and nesting thereof. Bounded: a leaf (str, NoneType, a
    non-Enum class) has empty `get_args`, so recursion terminates; nested BaseModel
    fields are NOT descended (top-level scope -- see the module docstring)."""
    out: set[str] = set()
    if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
        return {m.value for m in annotation if isinstance(m.value, str)}
    for arg in typing.get_args(annotation):
        if isinstance(arg, enum.Enum):            # Literal[SomeEnum.MEMBER]
            if isinstance(arg.value, str):
                out.add(arg.value)
        elif isinstance(arg, str):                # Literal["x"]
            out.add(arg)
        else:                                     # Union/Optional/Annotated/Enum-type -> recurse
            out |= _annotation_strings(arg)
    return out


def _payload_identifier_surfaces(cls) -> set[str]:
    """Lowercased names on `cls`'s TOP-LEVEL serialized surface that could carry a
    type discriminator: each field's and computed-field's name, the discriminator
    strings reachable in its annotation (`Literal` values + `Enum` member values),
    and any string alias (`alias` / `serialization_alias` -- NOT `validation_alias`,
    which is input-side). Nested member models are out of scope (see module
    docstring + the drift-check contract)."""
    surfaces: set[str] = set()
    for fname, finfo in (getattr(cls, "model_fields", {}) or {}).items():
        surfaces.add(fname.lower())
        surfaces |= {s.lower() for s in _annotation_strings(getattr(finfo, "annotation", None))}
        for attr in ("alias", "serialization_alias"):
            val = getattr(finfo, attr, None)
            if isinstance(val, str) and val.strip():
                surfaces.add(val.lower())
    for cname, cinfo in (getattr(cls, "model_computed_fields", {}) or {}).items():
        surfaces.add(cname.lower())
        surfaces |= {s.lower() for s in _annotation_strings(getattr(cinfo, "return_type", None))}
        alias = getattr(cinfo, "alias", None)
        if isinstance(alias, str) and alias.strip():
            surfaces.add(alias.lower())
    return surfaces


def _interchangeable_names(concept: str, cls, b: dict) -> set[str]:
    """The names a binding's alias-only reconciliation treats as the-same-thing:
    the ontology concept, the runtime class `__name__`, and the explicit
    `name_alias` if present. None may be a leak surface (R2)."""
    names = {str(concept), getattr(cls, "__name__", "") or str(concept)}
    na = b.get("name_alias")
    if isinstance(na, str) and na.strip():
        names.add(na.strip())
    names.discard("")
    return names


def _discriminator_fields(cls) -> list[str]:
    """Field names on `cls` that declare a Pydantic discriminated union -- the one
    nested shape whose serialized tag value the top-level scan cannot see (A4
    readiness)."""
    return [
        n for n, f in (getattr(cls, "model_fields", {}) or {}).items()
        if getattr(f, "discriminator", None)
    ]


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
        composed_with = _string_list(b.get("composed_with", []), concept, "composed_with", findings)
        missing_composed_guards = set(EXPECTED_COMPOSED_WITH.get(concept, ())) - set(composed_with)
        if missing_composed_guards:
            findings.append(
                "%s: `composed_with` missing required guard(s): %s"
                % (concept, ", ".join(sorted(missing_composed_guards)))
            )
        composed_classes = []
        for cspec in composed_with:
            c2, _, err2 = load(cspec)
            if c2 is None:
                findings.append("%s: composed_with binding dangles -- cannot import `%s` (%s)" % (concept, cspec, err2))
            else:
                composed_classes.append(c2)

        if b.get("not_payload_identifier"):
            names = _interchangeable_names(concept, cls, b)        # R2: {concept, __name__, name_alias?}
            for who in (cls, *composed_classes):                   # R3: composed classes share the concept set
                surfaces = _payload_identifier_surfaces(who)
                leaked = sorted(n for n in names if n.lower() in surfaces)
                if leaked:
                    findings.append(
                        "%s: interchangeable name(s) %s appear on `%s`'s top-level serialized surface "
                        "(field/computed name, Literal/Enum value, or serialized alias) -- payload-leaking; "
                        "alias-only reconciliation no longer safe"
                        % (concept, ", ".join("`%s`" % n for n in leaked), who.__name__)
                    )
                disc = _discriminator_fields(who)                  # A4 readiness: nested tag unseeable top-level
                if disc:
                    findings.append(
                        "%s: `%s` has discriminated-union field(s) %s -- the top-level leak-scan cannot see "
                        "nested member discriminator values; extend the guard with nested recursion "
                        "(see docs/decisions/ontology_runtime_drift_check_contract_v0.md)"
                        % (concept, who.__name__, ", ".join("`%s`" % d for d in sorted(disc)))
                    )
        else:
            findings.append("%s: `not_payload_identifier` missing or false (drift-check invariant vacuous)" % concept)

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

    # Non-vacuity probe: the leak guard MUST catch a self-naming `Literal`
    # discriminator AND a self-naming serialized alias, and MUST NOT trip on a
    # clean model. Skips only if pydantic is unavailable (infra gap), never on a
    # guard defect.
    try:
        from pydantic import BaseModel, Field
    except Exception:
        print("INFO  leak-guard probe skipped (pydantic unavailable)")
    else:
        class _LeakProbe(BaseModel):
            kind: typing.Literal["SourceCapturePacket"] = "SourceCapturePacket"
            tag: str = Field(default="x", serialization_alias="EvidenceUnit")

        class _Mode(enum.Enum):          # plain (non-str) Enum -> the A2 gap the review found
            LEAK = "EvidenceUnit"

        class _EnumProbe(BaseModel):
            mode: _Mode = _Mode.LEAK

        class _A(BaseModel):
            kind: typing.Literal["a"] = "a"

        class _B(BaseModel):
            kind: typing.Literal["b"] = "b"

        class _DiscProbe(BaseModel):
            pet: typing.Union[_A, _B] = Field(discriminator="kind")

        class _CleanProbe(BaseModel):
            manifest_version: str = "1"

        leak = _payload_identifier_surfaces(_LeakProbe)
        probes = [
            ("leak-guard: Literal + serialized alias",
             "sourcecapturepacket" in leak and "evidenceunit" in leak),
            ("leak-guard: enum member value (A2)",
             "evidenceunit" in _payload_identifier_surfaces(_EnumProbe)),
            ("clean model: no false positive",
             "sourcecapturepacket" not in _payload_identifier_surfaces(_CleanProbe)),
            ("readiness: discriminated union detected (A4)",
             _discriminator_fields(_DiscProbe) == ["pet"]),
            ("readiness: clean model has no discriminated union",
             _discriminator_fields(_CleanProbe) == []),
        ]
        for label, passed in probes:
            if not passed:
                ok = False
            print("%s  %-46s" % ("PASS" if passed else "FAIL", label))

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
