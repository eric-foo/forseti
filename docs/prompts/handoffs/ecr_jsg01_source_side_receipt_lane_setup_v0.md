# ECR Lane Setup — JSG-01 Source-Side Receipt Binding (fresh-agent handoff)

```yaml
retrieval_header_version: 1
artifact_role: Lane-setup handoff prompt
scope: Spins the JSG-01 source-side Evidence Candidate Record receipt binding work off as its own CA lane for a fresh agent.
use_when:
  - Starting the ECR (Evidence Candidate Record) lane from cold.
  - Authoring or reviewing the JSG-01 source-side receipt binding.
authority_boundary: retrieval_only
load_rule: confirm-don't-trust — re-read every named source before any strict or actionable claim. This prompt is orientation, not authority.
workspace: C:\Users\vmon7\Desktop\projects\orca
expected_branch: main
```

## Anchor goal

Unblock JSG-01 by formalizing the minimal source-side Evidence Candidate Record
receipt as a BINDING over the EXISTING `EvidenceUnit` schema (NOT a new/forked
schema), so a real post-cutoff case evaluates DETERMINATELY at JSG-01's
source-side subpredicates, shrinking the only residual to one named owner
decision (finalization authority). Path-not-proof.

## Success signals

1. A real post-cutoff case (Canoo/Walmart) evaluates determinately at JSG-01's
   source-side subpredicates — not `indeterminate_until_authored`.
2. The receipt BINDS to the existing `EvidenceUnit` + `PreDecisionStatus` enum —
   no forked/parallel schema.
3. Every source-side subpredicate names exact field(s) + CLOSED allowed-values +
   cleared-condition.
4. Inspectability binds to existing capture provenance/posture (0–1 new field).
5. Finalization-provenance is named but `indeterminate_until_authored`, bound to a
   SEPARATE owner decision — not self-staffed.
6. Conductor REFERENCES the binding (no copy, no predicate edit); minimal + closed
   + versioned; explicitly NOT the deferred ECR/EvidenceUnit consolidation.
7. Fresh-agent readable — loads cold from the anchors below.

## Locked decisions (verify against source, then build — do not relitigate)

- CALL 1 — bind-don't-fork. The `EvidenceUnit` schema + `PreDecisionStatus` enum
  already exist (`pydantic_schema_reference.md`). Authoring a new ECR schema would
  duplicate them. Write a minimal JSG-01 source-side receipt BINDING that
  references the existing schema and names which fields satisfy each subpredicate
  + the cleared-conditions. The boundary doc says cite the existing `EvidenceUnit`
  standard until the consolidation. The conductor references the binding.
- CALL 2 — source-side only; do NOT self-staff finalization. The
  finalization-provenance subpredicate is the gate's FIREWALL (`pre_decision_status`
  must be finalized by a named Judgment authority; an operator-set status is a
  block-state). Authoring that authority from this lane to clear the gate corrupts
  it. Name the `finalized_by` slot, mark `indeterminate_until_authored`, and
  surface finalization as a SEPARATE owner/Judgment decision. The lane MAY draft
  that decision-surface for owner ratification; it must NOT make the decision.

## Refined field diff (verify against the real schema)

| JSG-01 subpredicate | Resolution | New field? |
| --- | --- | --- |
| source-identity         | bind `source` + `source_id` (present, non-placeholder)            | no |
| timing/cutoff           | bind `timestamp` + `pre_decision_status` (cutoff relationship)    | no |
| pre_decision (value)    | bind `PreDecisionStatus`; `verified_pre_decision`=cleared, `uncertain_timestamp`/`excluded`=not | no |
| inspectability          | bind to `hash` + referenced source packet/posture                | 0 (lean) / 1 tiny optional |
| finalization-provenance | owner authority — `finalized_by` slot, `indeterminate_until_authored` | not ours to fill |

## Build steps

1. CANONICAL-HOME CHECK (do first): read
   `core_spine_v0_information_production_foundation_v0.md` (IPF `EvidenceUnit`,
   product-method) and compare to the v0.14 pydantic (harness). Bind to the
   canonical home; if they diverge, FLAG it and stop for an owner call rather than
   guessing.
2. AUTHOR the minimal binding (docs-level): fields → subpredicates → closed
   cleared-conditions; conductor-referenced; `schema_version`; explicit
   "superseded-by the ECR/EvidenceUnit consolidation"; finalization slot marked
   indeterminate. Resolve inspectability bind-vs-one-tiny-field (lean pure bind;
   add a field only if `hash` + packet cannot honestly carry inspectability).
3. VALIDATE: replay Canoo/Walmart (and Unity) drafts against the binding — confirm
   source-side determinate, finalization isolated. Show the evaluation.
4. ADVERSARIAL REVIEW the authored binding before it is treated as authoritative.
   Attack seams: (a) does it fork the schema? (b) does the real case truly evaluate
   determinately? (c) can finalization leak/contaminate (self-staffing by stealth)?
   (d) is it bound to the canonical field home? (e) is inspectability honestly
   bound or faked? (f) does the conductor reference (not copy/edit) it? Patch
   accepted findings, then proceed.
5. DCP RECEIPT (trigger: `architecture_doctrine`) — this creates JSG-01-facing
   receipt doctrine; record controlling source + downstream surfaces + stale-language
   sweep inline (no standalone receipt file).
6. (Optional, SEPARATE artifact) draft the finalization-authority decision-surface
   for owner ratification — options + the operator-set=block-state rule. Do NOT
   make the decision.

## Scope / non-claims (path-not-proof)

Minimal docs-level binding first; a harness/pydantic materialization is a LATER
authorized step. This is the source-side receipt contract only — NOT judgment
quality, NOT fixture admission, NOT the ECR/EvidenceUnit consolidation, NOT the
finalization authority, NOT validation/readiness. Packets/cases stay scratch.

## Owner-reserved decision

- Finalization authority (who may finalize `pre_decision_status`; the block-state rule).

## Source anchors (confirm-don't-trust — read before strict claims)

- `docs/product/judgment_quality_promotion_operating_model_v0.md` — JSG-01 clear-predicate row (~L205)
- `docs/product/judgment_spine_gate_ownership_map_v0.md` — JSG-01 row (~L125)
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` — ECR/Cleaning layer boundary
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` — Ob. 6/7/8/9/16 (16 explicitly does NOT define ECR fields)
- `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` — `EvidenceUnit` + `PreDecisionStatus`
- `docs/product/core_spine_v0_information_production_foundation_v0.md` — IPF `EvidenceUnit` semantic home (canonical-home cross-check)
- `docs/research/judgment-spine/harness/v0_14/fixtures/{canoo_walmart_2022,unity_runtime_fee_2023}_v0_14/evidence_registry_draft_v0.md` — validation cases
```
