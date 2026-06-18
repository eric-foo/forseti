# JSG-01 Source-Side Receipt Translator — Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial artifact review of the PROPOSED JSG-01 source-side
  receipt translator, to inform owner ratification and the ECR-MVP
  independent-review bar before JSG-01 unfreezes.
use_when:
  - Dispatching the independent 2nd-opinion review of the translator.
  - Checking the review commission, target, decision criteria, and output contract.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/source_side_receipts/jsg01_source_side_receipt_translator_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
input_hashes:
  docs/product/jsg01_source_side_receipt_translator_v0.md: 2F6F3C4760AE554FF12D7A500882B43682E08B28D5F41718018B869A5EDFFA1B
branch_or_commit: main @ f9b05e6 (worktree dirty; controlling sources untracked)
```

## Commission

Adversarially review **one artifact**: the proposed JSG-01 source-side receipt
translator. Decide whether it is sound enough for the owner to **ratify** as the
official JSG-01 source-side first slice of the deferred ECR/EvidenceUnit
consolidation — and surface every material failure mode that should block or
qualify that ratification.

This is **read-only, findings-first, advisory** adversarial artifact review. It
does not approve, validate, ratify, or unfreeze the gate. It is decision input
for the owner.

## Target (commission-bound; do not retarget or widen)

- **Review object:** `docs/product/jsg01_source_side_receipt_translator_v0.md`
  (SHA256 `2F6F3C4760AE554FF12D7A500882B43682E08B28D5F41718018B869A5EDFFA1B`).
  Confirm the hash before reviewing; if it differs, stop and report drift.
- Adjacent sources are **context for judging the target**, not review objects.

## Operator precondition (owner-set, NOT prompt-routed)

The ECR-MVP bar wants an **independent** review. To satisfy it, the owner should
dispatch this to a reviewer **in a different model family from the artifact's
author (Claude)**, using a repo-access tool. This prompt is **model-neutral**: it
does not select, recommend, rank, or route a runtime model. Template posture, if
any, is `adversarial-artifact-review` (model-neutral) from the registry.

## Thread operating target continuity

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: >
    Anchor goal (orientation only): formalize a minimal source-side JSG-01
    receipt so a real post-cutoff case evaluates DETERMINATELY at the source-side
    subpredicates, shrinking the residual to one named owner decision
    (finalization authority). This review tests whether the proposed translator
    actually achieves that without forking the schema, leaking finalization, or
    over-claiming. Orientation only — not authority, readiness, or approval.
```

## Reviewer start state (orca_start_preflight)

```yaml
orca_start_preflight:
  agents_read: required_yes        # read AGENTS.md
  overlay_read: required_yes       # read .agents/workflow-overlay/README.md
  source_pack: custom              # see Read Pack below
  edit_permission: read-only       # reviewer thread is source-read-only
  target_scope:
    - docs/product/jsg01_source_side_receipt_translator_v0.md
  dirty_state_checked: required_yes
  blocked_if_missing: yes          # if the target or a controlling source is missing, return BLOCKED
controlling_source_state: untracked/dirty worktree; controlling Judgment-Spine and Core-Spine sources are untracked. This supports ADVISORY review only; strict PASS/readiness/acceptance claims remain blocked unless the owner accepts them.
doctrine_change: this review prompt does not change doctrine. The reviewed artifact is PROPOSED, not ratified; the review does not ratify it.
external_source_boundary: agent-workflow is read-only reusable mechanics; jb project policy is NOT Orca authority and must not be imported.
edit_permission: read-only
output_mode: review-report
```

## Source hierarchy and read pack (repo access assumed; read paths, do not paste)

Authority order: current instruction → `AGENTS.md` → `.agents/workflow-overlay/`
→ `docs/`.

Required reads:

- **Target:** `docs/product/jsg01_source_side_receipt_translator_v0.md`.
- **Canonical-home sources** (to verify SP-1/2/3 are grounded, not invented):
  - `docs/product/core_spine_v0_information_production_foundation_v0.md` (IPF Evidence Unit Standard)
  - `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Ob.7/8/9/12/16)
  - `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (Inclusion State Rule; cite-IPF-until-consolidation; deferred consolidation + open owner decisions)
- **Gate + ownership:** `docs/product/judgment_quality_promotion_operating_model_v0.md` (JSG-01 row + receipt-provenance sub-rule); `docs/product/judgment_spine_gate_ownership_map_v0.md` (JSG-01 owners).
- **Adapter target / pre_decision_status owner:** `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md` (AR-01/03/04/05); `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`; `orca-harness/schemas/case_models.py` (the `source_type`/`hash_basis` drift).
- **Validation discipline:** `.agents/workflow-overlay/validation-gates.md` (receipt-field provenance gate).
- **Replay fixtures:** `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md`; `.../unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md`.

## Method sequence (Source-Gated Method Contract — do not skip)

1. Read authority (`AGENTS.md`, overlay README, review-lanes, prompt-orchestration).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-adversarial-artifact-review`. **Do not APPLY yet.** Use them only to prepare neutral source-reading lenses.
3. `SOURCE-LOAD` the read pack above.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` (name missing sources, gaps, conflicts).
5. Only then `APPLY` `workflow-deep-thinking` to frame the boundary problem, failure modes, and decision criteria — then `APPLY` `workflow-adversarial-artifact-review` to produce findings.
6. Synthesize and verify each finding against the loaded sources (cite file/line).

If `workflow-adversarial-artifact-review` is unavailable or not applied, return a
**blocked or advisory-only** result and emit **no** formal verdict, readiness, or
validation claim.

## Decision criteria — attack these seams (be maximally adversarial on material ones)

Material (a failure here should block or qualify ratification):

1. **No-fork / canonical-home.** Is the target authored in IPF / Data-Capture
   canonical semantics with the harness as adapter-target only? Or does it pick
   the harness pydantic as the field-home (the withdrawn bind), invert layering,
   or create a parallel/final schema by stealth?
2. **Closed values are sourced, not invented.** For SP-1 (`source_identity_state`),
   SP-2 (`inspectability_state`), SP-3 (`cutoff_posture`): does each value and
   cleared-condition trace to a named owner field/clause (IPF, Ob.7/8/9/12,
   boundary Inclusion State Rule)? Flag any paraphrase or invented value
   (conductor Seam-1 forbids clearing on a paraphrase).
3. **Determinacy is real.** Independently replay Canoo/Walmart and Unity against
   the closed values. Does every unit resolve to exactly one of
   clears / does-not-clear / indeterminate? Reproduce or refute "Canoo clears
   source-side (residual = finalization)" and "Unity does-not-clear (TBD hashes +
   placeholder timestamps)." Find any unit whose value is ambiguous or outside the
   closed set.
4. **Provenance soundness.** Does any cleared-condition clear on a *self-asserted*
   value (receipt-field provenance gate)? Especially probe whether SP-1 `resolved`
   can clear on a bare operator-assigned `source_id` with no corroboration.
5. **The two contestable calls (attack BOTH directions):**
   - SP-1 clearing on `family_only` — is this **too loose** for a gate that
     gates downstream judgment-quality claims?
   - SP-2 requiring a byte-verifiable hash (so `inspectable_reference_only` does
     NOT clear) — is this **too strict**, wrongly failing legitimate archive-only
     sources (e.g., Unity EU-07's Wayback snapshot)?
6. **Finalization firewall (SP-5).** Does the target anywhere staff, name, define,
   or leak the finalization authority? Could SP-4's value-clear be misread as
   clearing the gate without SP-5? Is "necessary-not-sufficient" airtight?
7. **Adapter stability / three-representation drift.** Is "binds only invariant
   fields" actually true across `pydantic_schema_reference.md`, `case_models.py`,
   and the fixtures? Is there any case where `source_type`/`hash_basis` is
   load-bearing for SP-1/2/3, breaking the invariance claim? Does "fixtures only"
   hide a generalization the gate would need?
8. **Conductor reference.** Is the staged reference a pointer (not a copy, not a
   predicate edit), and does it leave the gate frozen / predicate unchanged until
   ratification?
9. **Scope honesty.** Does the target over-claim — implicitly perform the
   consolidation, or claim validation/ratification/gate-clearance? Are the
   non-claims accurate? Is "first slice ≠ consolidation" honored or violated by
   stealth?

Minor / hygiene:

10. Retrieval header correctness, `stale_if` accuracy, no forbidden authority
    fields, no `jb`/leakage imports.

## Output contract

- **Output mode:** `review-report`. Write the durable report to
  `docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md`.
- Start the report (and the chat closeout) with the compact `review_summary` YAML
  from `.agents/workflow-overlay/communication-style.md`
  (`recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked`),
  then detailed findings.
- **Findings-first.** Each finding: stable ID, `severity` (`critical` | `major` |
  `minor`, finding-priority only), the seam it attacks, cited evidence
  (file/line), `minimum_closure_condition` (required end state, not how-to), and
  `next_authorized_action` (owner decision / rerun / patch-authorization request /
  no action).
- Include **non-findings** (seams attacked that held) and **not-proven
  boundaries** (what this review cannot establish — e.g., that the slice is
  correct for cases beyond the two fixtures; that it satisfies any cross-family
  bar if the reviewer is same-family).
- **Advisory remediation only.** Do **not** emit `patch_queue_entry` or
  executor-ready how-to (this is read-only review). Optional hardening must be
  labeled optional and non-required.
- If a finding shows the byte-verifiability or family-only calls are wrong,
  state the required end state, not the patch.

## Validation gates (must be able to fail)

- Source readiness declared before any finding; otherwise `SOURCE_CONTEXT_INCOMPLETE`.
- `workflow-adversarial-artifact-review` applied after readiness, or strict
  claims blocked / advisory-only.
- Hash of the target confirmed; drift → `BLOCKED`.
- Untracked/dirty controlling sources support advisory findings only; no strict
  PASS/readiness/acceptance/validation claim.
- Durable report written before any YAML-only chat summary; on write failure use
  `status: failed`, `review_location: chat_only_current_thread`,
  `recommendation: blocked`, name the failed path.

## Review-use boundary

Findings are decision input for the owner only. They are not approval,
validation, ratification, mandatory remediation, gate-clearance, or
patch authority until the owner separately decides. This review does not unfreeze
JSG-01, does not ratify the field slice, and does not resolve the finalization
authority. `agent-workflow` is read-only reusable mechanics; `jb` is not Orca
authority.
```
