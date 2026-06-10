# Gate & Conductor Excerpts (review bundle payload)

```yaml
retrieval_header_version: 1
artifact_role: Review courier excerpt (disposable; no_repo bundle payload)
scope: Verbatim excerpts of the gate-ownership map JSG-04 row and the conductor's Isolation Topology + by-hand isolation cap, bundled so a no-repo reviewer can check the spec's grounding claims without repo access.
use_when:
  - Reviewing the blind-judgment execution-receipt spec without repo access.
authority_boundary: retrieval_only
open_next:
  - blind_judgement_execution_receipt_spec_v0.md
stale_if:
  - The review completes, or the conductor / gate-ownership map changes the excerpted text.
```

> These are verbatim excerpts copied for the no_repo review. The owning sources
> (the conductor `judgment_quality_promotion_operating_model_v0.md` and the
> `judgment_spine_gate_ownership_map_v0.md`) win on any conflict.

## Gate-ownership map — JSG-04 row

```
| JSG-04 | No-tools isolation | owned | contestant_no_tools_execution_contract_v0.md | No-tools execution receipt complete per the contestant no-tools execution contract, including its owner-required isolation result and auditable execution-provenance boundary | Clean blind-use readiness, scoring, validation, fixture admission, judgment-quality evidence | Execution surface or runner receipt proves isolation; prompt text alone is insufficient | none for ownership |
```

## Conductor — Isolation Topology

```yaml
isolation_topology:
  orchestrator_thread:
    role: reads sources, evaluates predicates, sequences gates, records run state
    authority: none
  isolated_child_runs:
    - gate: JSG-05 memorization probe
      isolation_owner: memorization_probe_protocol + contestant_no_tools_execution_contract
    - gate: JSG-06 contestant blind judgment
      isolation_owner: contestant_no_tools_execution_contract
    rule: child runs must be isolated from orchestrator context; the orchestrator must not leak packet, ledger, or outcome material into them
  deterministic_scorer:
    gate: JSG-07
```

## Conductor — by-hand isolation cap

```yaml
by_hand_isolation_cap:
  affected_gates: [JSG-04, JSG-05, JSG-06]
  mechanism: >
    By-hand execution cannot bind the authorized, auditable live-execution
    provenance the no-tools contract requires; a hand-typed
    isolation_result == "proven" or gate_interpretation == "pass_valid" field is
    not self-certifying and is not gate-clearing (receipt-provenance sub-rule and
    the no-tools contract Receipt Provenance Boundary). JSG-04 therefore does not
    clear, JSG-05 cannot clear on a by-hand probe receipt, and JSG-06 (which
    inherits JSG-04 provenance) cannot clear by-hand.
```

## Conductor — JSG-06 predicate note (Round-3 / Round-13 patches)

```
JSG-06's predicate is re-bound to its own owner field (isolation_result proven)
with the sealed-output subpredicate marked indeterminate_until_authored ... and
JSG-06's inherited-provenance dependency on JSG-04 is stated explicitly.

(Round-13) blind judgment hash named by the gate map and evidence ladder ... so
`sealed` is reachable for a clean isolated run while still gated behind JSG-04
provenance (by-hand still cannot reach it).
```
