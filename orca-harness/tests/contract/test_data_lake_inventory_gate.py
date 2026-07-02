"""A1 deterministic inventory gate (Bronze full-GT proof scope, STEP-03).

Fails when the checked-in touchpoint inventory record drifts from fresh
source discovery in either direction, when an exclusion loses its reason, or
when an unknown lacks a resolved owner disposition. The record is a generated
inventory of code surfaces — never lake authority; updating it is a
deliberate, reviewed edit (regenerate via ``data_lake.inventory`` and commit
the diff).

Fail-capability is itself under test: the seeded-violation tests below prove
every failure class the gate claims to detect actually trips it.
"""
from __future__ import annotations

import copy
import json

from data_lake.inventory import (
    INVENTORY_PATH,
    build_inventory,
    inventory_violations,
    load_declared_inventory,
    serialize_inventory,
)


def test_inventory_record_matches_fresh_discovery_byte_identical() -> None:
    declared_text = INVENTORY_PATH.read_text(encoding="utf-8")
    discovered_text = serialize_inventory(build_inventory())

    if declared_text != discovered_text:
        violations = inventory_violations(json.loads(declared_text), build_inventory())
        raise AssertionError(
            "Checked-in lake touchpoint inventory drifted from fresh discovery. "
            "Classify each change (declare, exclude with a reason, or record an "
            "unknown for owner disposition), regenerate via data_lake.inventory, "
            "and commit the diff deliberately.\n" + "\n".join(violations or ["(formatting-only drift)"])
        )


def test_inventory_regeneration_is_deterministic() -> None:
    assert serialize_inventory(build_inventory()) == serialize_inventory(build_inventory())


def test_declared_inventory_has_no_gate_violations() -> None:
    declared = load_declared_inventory()
    assert inventory_violations(declared, build_inventory()) == []


def test_gate_fails_on_seeded_undeclared_writer() -> None:
    declared = load_declared_inventory()
    discovered = copy.deepcopy(declared)
    discovered["raw_packet_writers"]["runner_seams"].append(
        {
            "runner": "run_seeded_violation_packet.py",
            "kind": "direct_packet_writer",
            "a2_fork_impact": "manifest_shape",
        }
    )

    violations = inventory_violations(declared, discovered)

    assert any(
        "undeclared" in violation and "run_seeded_violation_packet.py" in violation
        for violation in violations
    ), violations


def test_gate_fails_on_seeded_stale_declared_entry() -> None:
    declared = copy.deepcopy(load_declared_inventory())
    declared["non_raw_touchpoints"].append(
        {
            "module": "data_lake/does_not_exist.py",
            "call": "append_record",
            "count": 1,
            "a2_fork_impact": "none",
        }
    )

    violations = inventory_violations(declared, build_inventory())

    assert any(
        "stale" in violation and "does_not_exist.py" in violation for violation in violations
    ), violations


def test_gate_fails_on_seeded_reasonless_exclusion() -> None:
    declared = copy.deepcopy(load_declared_inventory())
    declared["exclusions"].append({"target": "seeded/reasonless", "reason": "   "})

    violations = inventory_violations(declared, build_inventory())

    assert any(
        "exclusion without a reason" in violation and "seeded/reasonless" in violation
        for violation in violations
    ), violations


def test_gate_fails_on_seeded_reasoned_exclusion_drift() -> None:
    declared = copy.deepcopy(load_declared_inventory())
    declared["exclusions"].append(
        {"target": "seeded/reasoned_but_not_generated", "reason": "plausible but stale"}
    )

    violations = inventory_violations(declared, build_inventory())

    assert any(
        "stale exclusions entry" in violation
        and "seeded/reasoned_but_not_generated" in violation
        for violation in violations
    ), violations


def test_gate_fails_on_seeded_undispositioned_unknown() -> None:
    declared = copy.deepcopy(load_declared_inventory())
    declared["unknowns"].append(
        {
            "target": "seeded/unclassified_touchpoint",
            "question": "is this a lake touchpoint?",
            "owner_disposition": {"status": "pending"},
        }
    )

    violations = inventory_violations(declared, build_inventory())

    assert any(
        "unknown without a resolved owner disposition" in violation
        and "seeded/unclassified_touchpoint" in violation
        for violation in violations
    ), violations


def test_gate_fails_on_seeded_resolved_unknown_missing_disposition_detail() -> None:
    declared = copy.deepcopy(load_declared_inventory())
    declared["unknowns"].append(
        {
            "target": "seeded/thin_resolved_unknown",
            "question": "is this a lake touchpoint?",
            "owner_disposition": {"status": "resolved"},
        }
    )

    violations = inventory_violations(declared, build_inventory())

    assert any(
        "resolved unknown without a concrete disposition" in violation
        and "seeded/thin_resolved_unknown" in violation
        for violation in violations
    ), violations
    assert any(
        "resolved unknown without owner-attribution evidence" in violation
        and "seeded/thin_resolved_unknown" in violation
        for violation in violations
    ), violations


def test_resolved_unknown_clears_without_weakening_other_checks() -> None:
    declared = copy.deepcopy(load_declared_inventory())
    declared["unknowns"].append(
        {
            "target": "seeded/classified_touchpoint",
            "question": "is this a lake touchpoint?",
            "owner_disposition": {
                "status": "resolved",
                "disposition": "not a lake touchpoint; helper only",
                "recorded_by": "owner-gated PR merge",
            },
        }
    )

    violations = inventory_violations(declared, build_inventory())

    assert not any("seeded/classified_touchpoint" in violation for violation in violations), (
        violations
    )
