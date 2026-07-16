# Company Surface Vertical Slice Delegated Adversarial Code Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch prompt
scope: >
  Revision-bound, findings-first review and bounded patch commission for the
  owner-authorized Company Surface vertical slice at implementation revision
  bc2f7cfecf2f4b6e9d20e534625bf754c90e9c47.
use_when:
  - Couriering the completed Company Surface implementation to an independent, different-vendor controller.
  - Adjudicating whether that implementation can proceed beyond its fused review checkpoint.
authority_boundary: retrieval_only
stale_if:
  - The implementation target revision changes.
  - Any named target file changes after the implementation revision without a new review commission.
  - The owner changes the frozen Company Surface purpose, logical semantics, or review scope.
```

## Forseti Prompt Preflight

- output_mode: `file-write` for this filed prompt at
  `docs/prompts/reviews/company_surface_vertical_slice_delegated_adversarial_code_review_patch_prompt_v0.md`;
  the controller returns findings, diff, citations, validation, verdict, and
  residual risk in the couriering task or lane PR/comment, not a durable review report.
- template_kind: `repo-code-review`, enabled by the explicit owner-authorized
  implementation and review-and-patch commission in the run-authoritative task prompt.
- edit_permission: `patch-only` within the exact named target set below.
- reviews: findings-first delegated adversarial code review-and-patch through
  `workflow-code-review`; severity is finding priority only (`critical | major | minor`).
- doctrine_change: the implementation includes an `architecture_doctrine`
  change; its direction-change receipts are review targets, not review authority.
- destinations: this filed prompt is run-authoritative for the receiving
  controller; controller edits stay in the commissioned worktree and its return
  stays in chat or the lane PR/comment for Chief Architect adjudication.

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_company_surface_review_capsule
  edit_permission: patch-only
  target_scope: exact named files in the implementation diff 3bb7e6f531758df93d8f88c8c6c0bf332e91493c..bc2f7cfecf2f4b6e9d20e534625bf754c90e9c47
  dirty_state_checked: receiver_to_observe
  blocked_if_missing: target revision, exact target bytes, write capability, no-concurrent-writer state, review skill, or controlling sources
workspace_or_repo: C:\Users\vmon7\Desktop\projects\forseti-worktrees\9958\orca
authorization_basis: owner-authorized /fused implementation prompt and explicit delegated review-and-patch checkpoint
objective: find and patch material defects without changing the three accepted Company Surface outcomes or their signed semantics
intended_decision: whether the implementation diff is acceptable for home-model adjudication, not whether it is merged or ready
branch_or_commit_reference:
  branch: codex/company-surface-vertical-slice-9958
  implementation_revision_exact: bc2f7cfecf2f4b6e9d20e534625bf754c90e9c47
  base_revision_exact: 3bb7e6f531758df93d8f88c8c6c0bf332e91493c
  head_semantics: current branch HEAD may be a clean descendant containing only this filed review prompt after the implementation revision
dirty_state_allowance: clean at intake; controller-created edits may touch only the named target set
controlling_source_state: clean and committed at the implementation revision; receiver must verify
doctrine_change_decision: architecture doctrine changed by narrow Org adoption; review the inline receipts and downstream propagation
isolation_decision: existing isolated worktree off main; do not create or select another worktree
repo_map_decision: not_needed
repo_map_reason: exact revision, named file set, and controlling-source pointers are already bound
thread_operating_target_continuity: omitted; no separate active thread_operating_target was supplied
external_source_boundary: no web or live capture; inspect repository sources and frozen local evidence only
```

## Receiver Binding And De-Correlation Receipt

```yaml
receiver_binding:
  receiver_class: external_direct_write
  receiver_mechanism: operator-couriered independent controller with repo access
  launch_checkout: operator_to_fill
  effective_target_worktree: C:\Users\vmon7\Desktop\projects\forseti-worktrees\9958\orca
  resolution_method: two-root preflight when launch checkout differs; exact-root check when it does not
  direct_write_capability: receiver_to_observe_before_source_loading
  no_concurrent_writer: receiver_to_observe_before_source_loading
  dispatch_status: preparation_only_until_verified
actor_model_family_receipt:
  author_home_model_family: OpenAI GPT-5 family
  controller_model_family: operator_to_fill_different_vendor_or_lineage_from_OpenAI
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: receiver_must_verify_before_review
access: repo
review_lane: code (workflow-code-review)
mode: base-subagent
```

The controller-family field is a who-constraint, not a model recommendation.
Unknown, undisclosed, or OpenAI lineage does not satisfy the cross-vendor
discovery bar. If the receipt cannot be completed with a different vendor or
lineage, return `BLOCKED_CONTROLLER_NOT_DECORRELATED`; do not substitute a
self-review or directly launch another reviewer. The receiving actor is already
the controller and must not dispatch a replacement controller.

Before source loading, verify:

1. the effective target is the exact worktree above and the branch contains the
   exact implementation revision;
2. `git diff bc2f7cfecf2f4b6e9d20e534625bf754c90e9c47..HEAD -- <named-targets>`
   is empty, so any later prompt-only commit did not change target bytes;
3. the working tree is clean, the controller can write and stage/unstage a
   harmless probe in this worktree, and no concurrent writer is active; and
4. the target diff is exactly
   `3bb7e6f531758df93d8f88c8c6c0bf332e91493c..bc2f7cfecf2f4b6e9d20e534625bf754c90e9c47`.

Return `BLOCKED_RECEIVER_REROOT_REQUIRED`, `BLOCKED_TARGET_DRIFT_DURING_REVIEW`,
or the nearest exact blocker if any check fails. Do not review a context pack,
summary, alternate checkout, recreated copy, or different revision instead.

## Goal And Success Signal

Goal: adversarially test and, where justified, patch the complete Company
Surface vertical slice while preserving the owner-signed purpose contract,
logical contract, Brand/Org distinction, temporal meanings, Silver authority,
and offline product-learning claim tier.

Done means the controller returns findings-first review evidence and a bounded
working-tree diff (or no diff), with each finding traceable to repository source;
the producer schema remains fail-closed, Org adoption stays narrow, the four
logical families survive Silver mapping without changing the generic envelope,
restated and as-known history diverge correctly after corrections, identical
inputs rebuild identical views/manifests, and the frozen Topicals case traverses
the same public path without an inflated claim. The nine success signals in
`forseti/product/information/company_surface/purpose_contract_v0.md` are the
fitness reference and an axis to attack, not an automatic pass bar.

Ordinary source-read-only review is insufficient because material findings in
validation, temporal selection, deterministic serialization, provenance
projection, or Silver integration may require tightly coupled corrections and
tests. Patch authority is therefore explicit but remains subordinate to the
frozen architecture and exact file set.

## Exact Named Target Set

Only these files are patchable; label every finding, citation, and diff hunk
with the corresponding short tag:

- `[capture-api]` `forseti-harness/capture_spine/company_aggregate_forward_signal/__init__.py`
- `[capture-model]` `forseti-harness/capture_spine/company_aggregate_forward_signal/models.py`
- `[capture-validation]` `forseti-harness/capture_spine/company_aggregate_forward_signal/validation.py`
- `[company-runtime]` `forseti-harness/data_lake/company_surface.py`
- `[lake-inventory]` `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json`
- `[lane-registry]` `forseti-harness/data_lake/lane_registry.py`
- `[silver-census]` `forseti-harness/data_lake/silver_census.py`
- `[touchpoint-contract]` `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- `[capture-tests]` `forseti-harness/tests/unit/test_company_aggregate_forward_signal.py`
- `[company-tests]` `forseti-harness/tests/unit/test_company_surface.py`
- `[company-router]` `forseti/product/information/company_surface/README.md`
- `[identity-contract]` `forseti/product/information/company_surface/company_identity_boundary_v0.md`
- `[logical-contract]` `forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md`
- `[mapping-contract]` `forseti/product/information/company_surface/company_surface_silver_mapping_contract_v0.md`
- `[purpose-contract]` `forseti/product/information/company_surface/purpose_contract_v0.md`
- `[ontology-architecture]` `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md`
- `[ontology-ssot]` `forseti/product/spines/foundation/ontology/ontology.yaml`
- `[brand-card]` `forseti/product/spines/foundation/ontology/ontology_cards/brand_beautypie_v0.md`
- `[venue-card]` `forseti/product/spines/foundation/ontology/ontology_cards/venue_basenotes_v0.md`
- `[ontology-backlog]` `forseti/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json`

Everything else is read-only and flag-only, including this prompt, other tests,
canonical/frozen/hash-pinned artifacts, generated or provenance ledgers,
`AGENTS.md`, `.agents/workflow-overlay/`, installed skills, external workflow
sources, and `jb`. A correct fix outside the named set requires
re-commissioning; do not silently widen scope. Do not modify frozen Topicals
evidence.

## Required Reads And Method Order

`REFERENCE-LOAD` before inspecting target sources:

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`;
2. `.agents/workflow-overlay/delegated-review-patch.md` sections **When it
   applies**, **The loop**, **Access selection rule**, **De-correlation**,
   **Code-diff target kind**, and **Overlay Interface**;
3. `.agents/workflow-overlay/prompt-orchestration.md` sections **Review Prompt
   Defaults** and **Repo-Bound Review Target Resolution**;
4. the available `workflow-code-review` skill in the controller runtime; and
5. `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` for the
   environment baseline.

`SOURCE-LOAD` a bounded custom capsule from the exact diff plus:

- `forseti/product/information/company_surface/purpose_contract_v0.md`;
- `forseti/product/information/company_surface/company_identity_boundary_v0.md`;
- `forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md`;
- `forseti/product/information/company_surface/company_surface_silver_mapping_contract_v0.md`;
- `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md` targeted to Org adoption and its direction-change receipt;
- `forseti/product/spines/foundation/ontology/ontology.yaml` targeted to Brand/Org and active relationships;
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` targeted to the common envelope, closed record kinds, correction edges, and generated views; and
- the frozen Topicals packet files referenced by the tests, only as needed to
  verify the copied facts and product-learning non-claims.

Exclude prior review outputs, unrelated prompts, broad product/capture files,
web sources, and the stale `codex/fused-cold-dogfood` worktree/branch. Declare
`SOURCE_CONTEXT_READY` with the bounded files/sections actually read, or return
`SOURCE_CONTEXT_INCOMPLETE` with the precise gap. Only then `APPLY`
`workflow-code-review`; if that lane is unavailable, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Frozen Decisions And Stop Conditions

Do not reinterpret or reopen:

- the owner-signed Company Surface purpose and nine success signals;
- the four logical families, Brand/Org distinction, assertion states, dual
  effective/knowledge time, append-only history, and unsupported-relation behavior;
- narrow Org adoption limited to `org:<slug>`, `Brand -owned_by-> Org`, and
  `Org -subsidiary_of-> Org`;
- Silver as physical authority with its unchanged common envelope and closed
  `entity | relationship | observation` kinds;
- generated views as rebuildable, non-authoritative read models; and
- Topicals as offline `product_learning` only.

Return `NEEDS_ARCHITECTURE_PASS`, revert any partial controller diff, and stop
with findings only if a credible fix requires new vocabulary, material generic
Silver contract/header/path changes, live capture or source access, a matcher or
registry, a second store, a UI/API/feed, or another design-level choice.

## Adversarial Review Focus

Be coverage-first and report every issue found, including minor and
low-confidence issues. At minimum attack:

1. fail-closed validation of required provenance, explicit capture/measurement
   posture, all decomposed time postures, absence-vs-zero, and append-only
   re-observation;
2. whether Org graduated only after a real producer schema and whether every
   live ontology/router surface now agrees without inventing an Org card;
3. exact preservation of the four logical families, subject identity,
   assertion state, evidence, capture/effective/recorded time, coarse precision,
   limitations/alternatives, correction/supersession/conflict, and visible failure;
4. correction edge direction and cutoff semantics, especially whether a later
   correction changes restated history while earlier as-known history stays intact;
5. deterministic ordering and canonical bytes for views and manifests,
   including generation stamps, source sets, high-watermarks, selection-policy
   evidence, repeated builds, and drift proof;
6. write-front-door use, lane binding, census posture, inventory coupling,
   record ID/path safety, and any accidental weakening of generic Silver;
7. Brand/Org separation and unsupported relationship behavior in the frozen
   Topicals path, including exact source locator/hash, unknown/coarse time,
   traceable provenance, and all three query modes; and
8. false product/readiness/buyer/source-completeness/GTM claims, forbidden
   decision fields, or hidden capture/runtime expansion.

For each actionable finding include: label, severity (`critical | major |
minor`), confidence (`high | medium | low`), file and line, evidence/citation,
impact, `minimum_closure_condition` as an end state, and
`next_authorized_action`. Put steelman-defeated candidates in
`considered_and_defended` rather than silently dropping them.

## Patch And Validation Contract

Patch only findings inside the exact target set. The controller owns judgment,
citations, and the bounded patch; citations must be neutral in tone and
decision-sufficient in substance. Do not commit the patch.

Run and report real `GATE PASS`, `GATE FAIL`, `INFO`, and `OUT OF SCOPE`
distinctions for:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
$env:PYTHONPATH='forseti-harness'
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest-company-review-focused forseti-harness/tests/unit/test_company_aggregate_forward_signal.py forseti-harness/tests/unit/test_company_surface.py forseti-harness/tests/unit/test_silver_record.py forseti-harness/tests/unit/test_silver_census_behavior.py forseti-harness/tests/unit/test_silver_lane_registry_guard.py forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py forseti-harness/tests/contract/test_data_lake_inventory_gate.py
python .agents/hooks/check_ontology_ssot.py --strict
python .agents/hooks/check_ontology_expansion.py --health --verbose
python .agents/hooks/check_ontology_drift.py --strict
python .agents/hooks/check_ontology_tag_validity.py --strict --base 3bb7e6f531758df93d8f88c8c6c0bf332e91493c
python .agents/hooks/check_dcp_receipt.py --strict --base 3bb7e6f531758df93d8f88c8c6c0bf332e91493c
python .agents/hooks/check_silver_lane_registry.py --strict
python .agents/hooks/check_harness_coupling.py --strict --base 3bb7e6f531758df93d8f88c8c6c0bf332e91493c
```

If the controller changes code, also run the full harness suite when feasible:

```powershell
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest-company-review-full forseti-harness/tests
```

Never hide or route around failure. Report exact blocked/not-run reasons.

## Controller Return And Lifecycle Hard Stop

Return in this order:

1. findings first, including `considered_and_defended`;
2. bounded working-tree diff summary, with each hunk attributable to its target label;
3. neutral per-change citations;
4. validation evidence with pass/fail/info/out-of-scope distinctions;
5. one overall verdict plus per-target sub-verdicts where materially different; and
6. residual risks, off-scope flags, and any `NEEDS_ARCHITECTURE_PASS` result.

Record provenance facts as `reviewed_by` and `authored_by`; use `unrecorded`
when tooling does not supply a value and never fabricate them.

The returned findings, diff, citations, verdict, and residuals are claims for
the Chief Architect to adjudicate, not premises to inherit. Nothing is kept
until the home/CA model accepts, modifies, or rejects each material change
against the cited sources. After adjudication, the CA must follow
`.agents/workflow-overlay/communication-style.md` -> **Review Adjudication Next
Step**, including closure of self-closable issues, exactly one later land step
when clean, and the goal-conditioned material-next-move check.

Hard stop: the controller must not commit, push, open or update a PR, merge,
stash, reset, clean the worktree, run repository hygiene, or otherwise advance
lifecycle state. Do not edit outside the commissioned file set. Stop after the
return; the Chief Architect owns adjudication and every keep/land action.

## Prompt Validation Receipt

```yaml
prompt_validation:
  prompt_contract_depth: full_orchestration
  overlay_and_template_sources:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/template-registry.md
    - docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
    - workflow-delegated-review-patch SKILL.md
    - workflow-prompt-orchestrator SKILL.md
  template_source: authorized project-local repo-code-review shape plus run-authoritative commission
  workflow_sequence_status: bound
  output_destination_status: bound
  model_lane: unbound_by_design
  output_frame: bound_to_controller_return_contract_above
  prompt_verdict: PASS
  non_claims:
    - review not yet run
    - controller identity and cross-vendor de-correlation not yet observed
    - no finding, patch, adjudication, acceptance, readiness, or merge claim
```
