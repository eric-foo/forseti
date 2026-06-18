# Decision: JSG-01 UNFROZEN (owner dated act, 2026-06-12)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (the owner's dated JSG-01 unfreeze act)
scope: >
  Unfreezes the JSG-01 gate of the judgment-quality promotion conductor: the
  gate becomes evaluable over a bound case packet, with the conductor's JSG-01
  row amended inside this act. Records the D2-wording consumption (option b)
  and the judge-family correction-receipt caveat. Clears no case; authorizes no
  run; lifts no claim tier.
use_when:
  - Checking whether JSG-01 is frozen (it is NOT, as of this dated act) and what its unfreeze consumed.
  - Authorizing or preparing a run that would evaluate JSG-01 over a case packet (runs stay separately gated).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md  # the conductor; JSG-01 row amended by this act
  - docs/decisions/jsg01_unfreeze_decision_memo_v0.md                             # the slice-D memo this act consumed
  - orca-harness/cases/product_learning/jsg01_binding_assembly_proof_v0/README.md # the first carrying packet
stale_if:
  - D2 is built (the corroborated SP-6 tier activates; revisit the option-b record).
  - The conductor's JSG-01 row is restructured beyond this amendment.
```

**Status:** DECIDED (owner, 2026-06-12).

## Authorization basis (record, verbatim intent)

Owner, in-thread 2026-06-12: **"authorised"** — given in direct response to the
slice-D unfreeze decision memo (`docs/decisions/jsg01_unfreeze_decision_memo_v0.md`,
committed `1fb952c`) and its closing ask ("say the word (and pick a or b — or
just 'unfreeze, option b')"). The act therefore adopts the memo's recommended
**option (b)** as the authorized reading.

## The decision

1. **JSG-01 is UNFROZEN.** The conductor's JSG-01 row is amended inside this
   act from "JSG-01 stays FROZEN and clears no case" to its evaluable state:
   every subpredicate routes to built, ratified, owner-produced fields and
   evaluates determinately over a bound case packet.
2. **D2 wording consumed via option (b):** the frozen row's "+ D2" precondition
   is consumed as decision-C's determinate residual behavior being acceptable
   for this unfreeze boundary. D2 stays deferred and owner-reserved; the
   corroborated SP-6 tier stays unreachable; archive+current packets land on
   named residuals that **do not clear** (conservative — a residual never fakes
   a pass). Archive-only packets can clear SP-6 via `archive_only`.
3. **Judge-family caveat carried:** the first carrying packet's receipt records
   the explicit placeholder `judge_model_family: unassigned_pending_run_authorization`;
   the consumer clears only when the run's judge family matches the receipt,
   so the first authorized run must record a correction receipt
   (`--supersedes 01KTW48P5PW4JJQG7NBG6G6DBP`) carrying the real judge family
   before evaluation. This is a per-run input, not an unfreeze condition.

## Evidence basis (from the consumed memo; verified at authoring)

Schema ratified + SP-6 D-source amendment (boundary doc); derivers built
(`orca-harness/ecr/`); SP-5 model + validate-only consumer (`a37f896`) and
producer acting half (`aeedae9`), cross-vendor reviewed + adjudicated; the
JSG-01-scoped `EvidenceUnit` binding ratified (boundary doc amendment,
`15b2954`) and built (`orca-harness/evidence_binding/`, reviewed + adjudicated,
`231299a`); the first real case packet carrying all five reads
(`cases/product_learning/jsg01_binding_assembly_proof_v0`, `c3a44b9` +
`22fe279`; receipt `01KTW48P5PW4JJQG7NBG6G6DBP`); composition observed
2026-06-12 — all five subpredicates determinate, all clearing on that packet;
full harness suite `712 passed, 1 skipped`.

## What this act does NOT do

- Clears **no case** — evaluability is not clearance; no JSG-01 evaluation has
  been run under authorization.
- Authorizes **no run** — contestant runs, recognition probes, scoring, and
  batch-1 execution remain separately gated, outcome-clean, owner-authorized.
- Builds nothing — D2, the full ECR/Evidence Unit field architecture, the
  canonical object name, and materiality remain reserved exactly as before.
- Lifts no claim tier — machinery existence, never judgment-quality attainment;
  the evidence ladder + claim-defense doctrine cap every externally-shaped
  sentence (Row 1, product_learning).

## direction_change_propagation

```yaml
direction_change_propagation:
  doctrine_changed: "JSG-01 is UNFROZEN by the owner's dated act (2026-06-12): the conductor's JSG-01 row is amended inside this act from frozen/clears-no-case to evaluable-over-a-bound-case-packet, with the '+ D2' precondition consumed via option b (decision-C determinate residual behavior accepted for this unfreeze boundary; D2 itself stays deferred and reserved; residuals never clear). JSG-01 still clears no case until a separately authorized run evaluates one, and the first run must correction-receipt the placeholder judge family before evaluation."
  trigger: architecture_doctrine
  related_triggers: [lifecycle_boundary]
  controlling_sources_updated:
    - "docs/decisions/jsg01_unfreeze_decision_v0.md"  # this record (authoritative home of the act)
    - "docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md"  # JSG-01 row amended INSIDE this act (the only permitted edit context)
  design_basis:
    - path: "docs/decisions/jsg01_unfreeze_decision_memo_v0.md"
      status: "consumed by this act (its stale_if fires; this record supersedes it as live state)"
  downstream_surfaces_checked:
    - "docs/workflows/ecr_spine_submap_v0.md"  # UPDATED: downstream-consumer line, invariant 5, deferred list, stale_if
    - "docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md"  # UPDATED: SP-5 + binding rows, corrected-gap prose
    - "docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md"  # checked, NO edit: every 'JSG-01 stays FROZEN' there sits inside dated ratification records (history, not live state); the live reserved lists never carried the unfreeze
    - ".agents/workflow-overlay/safety-rules.md"  # checked, NO edit: no JSG-01 entry; run/ECR gates unchanged
  intentionally_not_updated:
    - path: "orca-harness/evidence_binding/ (module docstrings) + orca-harness/cases/product_learning/jsg01_binding_assembly_proof_v0/README.md + docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md"
      reason: "their 'JSG-01 stays FROZEN' lines are dated build-time/observation provenance, accurate when written; the conductor row + this record own the live gate state. Flag for refresh on next material touch of each file."
    - path: "docs/review-outputs/ (review records)"
      reason: "dated review provenance; never rewritten."
  stale_language_search: "rg -n 'stays FROZEN|JSG-01 is FROZEN|conductor \\(FROZEN' docs/workflows docs/research/judgment-spine — live navigation surfaces updated in this act; remaining hits are dated records/provenance per intentionally_not_updated."
  non_claims:
    - "no case cleared; no run, probe, scoring, or batch-1 execution authorized"
    - "not validation, readiness, or judgment-quality evidence (product-learning cap unchanged)"
    - "not D2, not the full ECR/Evidence Unit field architecture, not the canonical object name (all still reserved)"
```
