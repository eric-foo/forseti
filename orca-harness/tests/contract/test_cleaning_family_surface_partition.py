"""Partition gate: the shared cleaning family's surfaces split exactly across lanes.

The ``fragrance_native_database`` family is shared by the fragrantica,
basenotes, and parfumo Cleaning lanes, split by ``source_surface``
(F-FRAG-002 adjudicated convention: allowlist known other-lane surfaces with
explicit out-of-scope acks; leave unknown surfaces visible and unacked). The
cross-vendor reviewers verified the partition BY HAND in the basenotes+parfumo
commission; this test is that check made mechanical:

- the three lanes' in-scope surface sets are pairwise disjoint (no packet has
  two owners);
- each lane's known-out-of-scope set is exactly the union of the OTHER lanes'
  in-scope sets (no gap: a surface someone owns is never "unknown" to a
  sibling; no overreach: a lane never acks-out-of-scope a surface nobody owns);
- all three lanes gate the same source family.

Adding a new surface to any lane (or a new lane to the family) fails this gate
until the family partition is deliberately re-declared — classification can no
longer happen by accident.
"""
from __future__ import annotations

import runners.run_basenotes_cleaning_catchup as basenotes
import runners.run_fragrantica_cleaning_catchup as fragrantica
import runners.run_parfumo_cleaning_catchup as parfumo

_LANES = {
    "fragrantica": (frozenset({fragrantica._FRAGRANTICA_SURFACE}), fragrantica._KNOWN_OUT_OF_SCOPE_SURFACES),
    "basenotes": (frozenset({basenotes._BASENOTES_SURFACE}), basenotes._KNOWN_OUT_OF_SCOPE_SURFACES),
    "parfumo": (parfumo._PARFUMO_SURFACES, parfumo._KNOWN_OUT_OF_SCOPE_SURFACES),
}


def test_family_lanes_gate_the_same_source_family() -> None:
    families = {
        "fragrantica": fragrantica._SOURCE_FAMILY,
        "basenotes": basenotes._SOURCE_FAMILY,
        "parfumo": parfumo._SOURCE_FAMILY,
    }
    assert set(families.values()) == {"fragrance_native_database"}, families


def test_in_scope_surfaces_are_pairwise_disjoint() -> None:
    overlaps = {}
    lanes = sorted(_LANES)
    for i, a in enumerate(lanes):
        for b in lanes[i + 1 :]:
            shared = _LANES[a][0] & _LANES[b][0]
            if shared:
                overlaps[(a, b)] = sorted(shared)
    assert not overlaps, f"surfaces claimed by two cleaning lanes: {overlaps}"


def test_each_lane_knows_exactly_the_other_lanes_surfaces_as_out_of_scope() -> None:
    problems = {}
    for lane, (in_scope, out_of_scope) in _LANES.items():
        others = frozenset().union(
            *(s for name, (s, _o) in _LANES.items() if name != lane)
        )
        if out_of_scope != others:
            problems[lane] = {
                "missing_from_out_of_scope (would surface as unsupported forever)": sorted(
                    others - out_of_scope
                ),
                "acked_out_of_scope_but_unowned (open-world ack risk)": sorted(
                    out_of_scope - others
                ),
            }
    assert not problems, (
        "The cleaning family's surface partition drifted. Each lane's known-out-of-scope "
        "set must be exactly the union of the other lanes' in-scope surfaces "
        f"(F-FRAG-002):\n{problems}"
    )
