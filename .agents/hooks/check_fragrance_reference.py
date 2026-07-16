#!/usr/bin/env python3
"""Fragrance sub-ontology reference-data integrity check.

Validates `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
against the four invariants the file's own header blocks declare but that no
other CI hook enforces (the three `check_ontology_*` gates only validate the
backbone `ontology.yaml`, never this reference-data file):

  - PROVENANCE (co-#1): every house/product/windcaller fact carries a
    non-empty `provenance` entry -- a source ref string, or the literal
    marker `operator_asserted_pending_source`. Never neither.
  - VOCABULARY CONFORMANCE: every house `tier`, plus every product
    `note_families`/`tier`/`occasions` value, exists in the file's own
    `vocabulary` block.
  - MAPPING-DERIVATION CONSISTENCY: a product's `note_families` must be a
    SUPERSET of the mechanical derivation of its `accords` through
    `vocabulary.accord_to_family_mapping.map` (unmapped accords contribute
    nothing). Superset, not equality: the file has a documented, provenanced
    case (`product:fragrance-one.office-for-men`) where an extra family is
    added from a non-accord source; the invariant that must hold is that
    derivation is never silently dropped, not that no other family may exist.
  - ENTITY RESOLUTION: every product `dupe_of` reference and every
    `dupe_relationships` edge resolves its `product:`-prefixed endpoint(s) to
    a product id defined in `products`. `dupe_relationships` is empty today;
    its check is schema-tolerant (it inspects edge values rather than
    assuming fixed key names) so it is ready the moment an edge is added.

This is a SHAPE / internal-consistency check on reference DATA -- it does not
assert fact-correctness, readiness, or that the reference data is complete
(see the file's own NON-CLAIMS block).

Usage:
  check_fragrance_reference.py --strict    CI gate: print findings; exit 1 if any, else 0.
  check_fragrance_reference.py --check     human-readable report; always exit 0.
  check_fragrance_reference.py --selftest  pure-function self-check; exit 0/1.

Fail-open: a missing file, unparseable YAML, or missing PyYAML exits 0
(advisory; never ghost-fail CI on infrastructure).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import repo_root  # noqa: E402  (sys.path pin must precede the import)

ONT_DIR = "forseti/product/spines/foundation/ontology"
YAML_REL = ONT_DIR + "/fragrance_reference_v0.yaml"

MARKER = "operator_asserted_pending_source"


def _has_provenance(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def check_bare_facts(doc: dict) -> list[str]:
    """co-#1: every product/house/windcaller fact has a provenance entry
    (source ref or the `operator_asserted_pending_source` marker)."""
    findings: list[str] = []

    for hid, h in (doc.get("houses") or {}).items():
        if not isinstance(h, dict):
            findings.append(f"{hid}: house entry is not a mapping")
            continue
        prov = h.get("provenance") if isinstance(h.get("provenance"), dict) else {}
        for key in ("existence", "tier"):
            if not _has_provenance(prov.get(key)):
                findings.append(f"{hid}: house field `{key}` has no provenance (bare fact)")

    for pid, p in (doc.get("products") or {}).items():
        if not isinstance(p, dict):
            findings.append(f"{pid}: product entry is not a mapping")
            continue
        prov = p.get("provenance") if isinstance(p.get("provenance"), dict) else {}
        required = {"existence"}
        for field in ("tier", "note_families", "accords", "notes", "occasions", "dupe_of"):
            if p.get(field):
                required.add(field)
        for key in sorted(required):
            if not _has_provenance(prov.get(key)):
                findings.append(f"{pid}: product field `{key}` has no provenance (bare fact)")

    for wid, w in (doc.get("windcallers") or {}).items():
        if not isinstance(w, dict):
            findings.append(f"{wid}: windcaller entry is not a mapping")
            continue
        prov = w.get("provenance") if isinstance(w.get("provenance"), dict) else {}
        if not _has_provenance(prov.get("existence")):
            findings.append(f"{wid}: windcaller field `existence` has no provenance (bare fact)")

    return findings


def check_vocabulary_conformance(doc: dict) -> list[str]:
    """Every house tier and product note_family/tier/occasion exists in `vocabulary`."""
    findings: list[str] = []
    vocab = doc.get("vocabulary") or {}
    nf_values = set((vocab.get("note_families") or {}).get("values") or [])
    tier_values = set((vocab.get("tiers") or {}).get("values") or [])
    occ_values = set((vocab.get("occasions") or {}).get("values") or [])

    for hid, h in (doc.get("houses") or {}).items():
        if not isinstance(h, dict):
            continue
        tier = h.get("tier")
        if tier is not None and tier not in tier_values:
            findings.append(f"{hid}: tier `{tier}` not in vocabulary.tiers")

    for pid, p in (doc.get("products") or {}).items():
        if not isinstance(p, dict):
            continue
        for nf in p.get("note_families") or []:
            if nf not in nf_values:
                findings.append(f"{pid}: note_family `{nf}` not in vocabulary.note_families")
        tier = p.get("tier")
        if tier is not None and tier not in tier_values:
            findings.append(f"{pid}: tier `{tier}` not in vocabulary.tiers")
        for occ in p.get("occasions") or []:
            if occ not in occ_values:
                findings.append(f"{pid}: occasion `{occ}` not in vocabulary.occasions")

    return findings


def _derive_families(accords: list, mapping: dict) -> set[str]:
    derived: set[str] = set()
    for accord in accords or []:
        derived |= set(mapping.get(accord) or [])
    return derived


def check_mapping_derivation(doc: dict) -> list[str]:
    """A product's note_families must be a superset of the mechanical
    derivation of its accords via vocabulary.accord_to_family_mapping."""
    findings: list[str] = []
    vocab = doc.get("vocabulary") or {}
    mapping = (vocab.get("accord_to_family_mapping") or {}).get("map") or {}

    for pid, p in (doc.get("products") or {}).items():
        if not isinstance(p, dict):
            continue
        accords = p.get("accords") or []
        note_families = set(p.get("note_families") or [])
        derived = _derive_families(accords, mapping)
        missing = derived - note_families
        if missing:
            findings.append(
                "%s: note_families missing derived family(ies) %s from accords %s"
                % (pid, sorted(missing), accords)
            )

    return findings


def check_dupe_relationships(doc: dict) -> list[str]:
    """Every product dupe_of reference and dupe_relationships edge resolves
    its product: endpoint(s). Schema-tolerant: inspects edge values rather
    than assuming fixed key names, since the list is currently empty and no
    shape is yet committed."""
    findings: list[str] = []
    products = doc.get("products") or {}

    for pid, p in products.items():
        if not isinstance(p, dict):
            continue
        dupe_of = p.get("dupe_of") or []
        if not dupe_of:
            continue
        if not isinstance(dupe_of, list):
            findings.append(f"{pid}: dupe_of expected a list")
            continue
        for ref in dupe_of:
            if not isinstance(ref, str) or not ref.startswith("product:"):
                findings.append(f"{pid}: dupe_of entry `{ref}` is not a `product:` reference")
            elif ref not in products:
                findings.append(
                    f"{pid}: dupe_of endpoint `{ref}` does not resolve to a defined product"
                )

    edges = doc.get("dupe_relationships")
    if edges is None:
        return findings
    if not isinstance(edges, list):
        return ["dupe_relationships: expected a list"]

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            findings.append(f"dupe_relationships[{i}]: expected a mapping (edge)")
            continue
        refs = [v for v in edge.values() if isinstance(v, str) and v.startswith("product:")]
        if not refs:
            findings.append(f"dupe_relationships[{i}]: no `product:` endpoint found")
            continue
        for ref in refs:
            if ref not in products:
                findings.append(
                    f"dupe_relationships[{i}]: endpoint `{ref}` does not resolve to a defined product"
                )

    return findings


def check_fragrance_reference(root: Path) -> list[str]:
    """Return all findings (empty == ok). Fail-open returns []."""
    try:
        import yaml
    except Exception:
        return []  # fail-open: PyYAML unavailable -> advisory skip
    yp = root / YAML_REL
    if not yp.is_file():
        return []
    try:
        doc = yaml.safe_load(yp.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(doc, dict):
        return ["fragrance_reference_v0.yaml: malformed top-level document (expected mapping)"]

    findings: list[str] = []
    findings.extend(check_bare_facts(doc))
    findings.extend(check_vocabulary_conformance(doc))
    findings.extend(check_mapping_derivation(doc))
    findings.extend(check_dupe_relationships(doc))
    return findings


def selftest() -> int:
    ok = True

    bare_doc = {
        "houses": {"brand:x": {"tier": "designer", "provenance": {"existence": "src", "tier": ""}}},
        "products": {
            "product:x.y": {
                "tier": "designer",
                "note_families": ["woody"],
                "provenance": {"existence": "src", "tier": MARKER},
            }
        },
        "windcallers": {"windcaller:creator.x": {"provenance": {}}},
    }
    bare_findings = check_bare_facts(bare_doc)
    cases = [
        ("bare fact: empty house tier provenance", any("brand:x" in f and "tier" in f for f in bare_findings), True),
        ("bare fact: missing product note_families provenance", any("product:x.y" in f and "note_families" in f for f in bare_findings), True),
        ("bare fact: windcaller marker-or-ref missing", any("windcaller:creator.x" in f for f in bare_findings), True),
        ("bare fact: marker counts as provenance", any("product:x.y" in f and f.endswith("`tier` has no provenance (bare fact)") for f in bare_findings), False),
    ]

    vocab_doc = {
        "vocabulary": {
            "note_families": {"values": ["woody"]},
            "tiers": {"values": ["designer"]},
            "occasions": {"values": ["daily"]},
        },
        "houses": {
            "brand:x": {"tier": "bogus"},
            "brand:y": {"tier": "designer"},
        },
        "products": {
            "product:x.y": {"note_families": ["woody", "bogus"], "tier": "designer", "occasions": ["nightlife"]}
        },
    }
    vocab_findings = check_vocabulary_conformance(vocab_doc)
    cases += [
        ("vocab: unknown house tier flagged", any("brand:x" in f and "`bogus`" in f for f in vocab_findings), True),
        ("vocab: known house tier not flagged", any("brand:y" in f for f in vocab_findings), False),
        ("vocab: unknown note_family flagged", any("`bogus`" in f for f in vocab_findings), True),
        ("vocab: unknown occasion flagged", any("`nightlife`" in f for f in vocab_findings), True),
        ("vocab: known tier not flagged", any("`designer`" in f for f in vocab_findings), False),
    ]

    map_doc = {
        "vocabulary": {"accord_to_family_mapping": {"map": {"woody": ["woody"], "citrus": ["citrus"]}}},
        "products": {
            "product:a": {"accords": ["woody", "citrus"], "note_families": ["woody"]},  # missing citrus
            "product:b": {"accords": ["woody"], "note_families": ["woody", "fresh"]},  # superset ok
            "product:c": {"accords": ["smoky"], "note_families": []},  # unmapped contributes nothing
        },
    }
    map_findings = check_mapping_derivation(map_doc)
    cases += [
        ("derivation: missing derived family flagged", any("product:a" in f for f in map_findings), True),
        ("derivation: superset (extra sourced family) allowed", any("product:b" in f for f in map_findings), False),
        ("derivation: unmapped accord contributes nothing", any("product:c" in f for f in map_findings), False),
    ]

    dupe_doc = {
        "products": {
            "product:real.one": {},
            "product:dupe.ok": {"dupe_of": ["product:real.one"]},
            "product:dupe.ghost": {"dupe_of": ["product:ghost.two"]},
        },
        "dupe_relationships": [
            {"dupe": "product:real.one", "original": "product:ghost.two"},
            {"from": "product:real.one", "to": "product:real.one"},
        ],
    }
    dupe_findings = check_dupe_relationships(dupe_doc)
    cases += [
        ("product dupe_of: dangling endpoint flagged", any("product:dupe.ghost" in f for f in dupe_findings), True),
        ("product dupe_of: resolving endpoint is clean", not any("product:dupe.ok" in f for f in dupe_findings), True),
        ("dupe edge: dangling endpoint flagged", any("product:ghost.two" in f for f in dupe_findings), True),
        ("dupe edge: both endpoints resolving is clean", not any("dupe_relationships[1]" in f for f in dupe_findings), True),
    ]

    for label, got, exp in cases:
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-55s got=%s" % (status, label, got))

    live = check_fragrance_reference(repo_root())
    status = "PASS" if not live else "FAIL"
    if live:
        ok = False
    print("%s  live fragrance_reference_v0.yaml clean (0 findings) -> %s" % (status, live))
    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (orca-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_fragrance_reference: cannot determine repo root: %s\n" % exc)
        return 0
    findings = check_fragrance_reference(root)
    if "--strict" in argv:
        if findings:
            print("check_fragrance_reference --strict: %d finding(s)" % len(findings))
            for f in findings:
                print("  " + f)
            return 1
        print("check_fragrance_reference --strict: OK (fragrance reference internally consistent)")
        return 0
    if "--check" in argv:
        if findings:
            print("fragrance reference findings (%d):" % len(findings))
            for f in findings:
                print("  " + f)
        else:
            print("fragrance reference: OK")
        return 0
    print("Usage: check_fragrance_reference.py --strict | --check | --selftest")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md; EP-35
        # delegated review FIND-02 class sweep): an internal checker bug must
        # not read as a green gate. Advisory modes fail open so a bug never
        # bricks the agent.
        sys.stderr.write("check_fragrance_reference: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
