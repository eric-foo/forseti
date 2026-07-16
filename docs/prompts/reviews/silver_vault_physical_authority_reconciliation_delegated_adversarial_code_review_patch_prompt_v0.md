# Silver Vault Physical-Authority Reconciliation Delegated Adversarial Code Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch commission prompt
scope: >
  Independent, different-vendor review of the rebased Silver Vault
  physical-authority reconciliation and hash-basis correction, with bounded
  patch authority over the explicitly named implementation files and a
  replacement durable review report.
use_when:
  - Reviewing the corrected codex/silver-vault-mgt-reconciliation implementation diff before fused closeout.
  - Checking closed raw, Bronze Attachment Record, and independent derived hash-basis semantics against physical verification.
stale_if:
  - The exact implementation range no longer resolves on the target branch.
  - The target file set or owner-bound behavior changes after this prompt is filed.
  - A later commission supersedes this review route.
authority_boundary: retrieval_only
```

## Commission

You are the independent controller for a delegated adversarial code
review-and-patch pass. This is a `delegated_code_review_and_patch` target under
`.agents/workflow-overlay/delegated-review-patch.md`. Use the code-review lane
only; do not merge it with artifact review merely because the diff contains
supporting contracts and tests.

The implementation was authored in an OpenAI/GPT-family Codex lane. Before
reviewing, record your actual model/provider lineage. You may act as controller
only if your model vendor/family is different from OpenAI/GPT. This is a
who-constraint, not a recommendation or ranking. If you cannot establish that
de-correlation, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` without reviewing
or patching.

```yaml
commission_binding:
  overlay_status: provisional_opt_in
  authorization_basis: owner explicitly invoked fused implementation and the fused review checkpoint recommends delegated adversarial review of the completed repository diff
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lane: workflow-code-review
  target_kind: delegated_code_review_and_patch
  access: repo
  mode: base-subagent
  terminal_return: durable review report plus uncommitted bounded patch when findings are safely closable in scope
  author_home_model_family: OpenAI/GPT family (Codex implementation lane)
  controller_model_family: operator_to_fill; must be a different vendor/family from OpenAI/GPT
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_fill before source loading
  reviewed_by: operator_to_fill in the durable review report
  authored_by: OpenAI GPT-5 Codex
  review_routing_status: routed_pending_fresh_different_vendor_return
```

No tester/testee shortcut is permitted. You are already the receiving
controller; do not launch a replacement controller or recursive review agent.
If `workflow-code-review` is unavailable, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not emulate it or patch.

## What This Is For

Goal: make Silver authority impossible to obtain from a malformed envelope or
an unresolved/tampered claimed source, while preserving historical audit bytes
and keeping the existing retrieval and census contracts truthful.

Done looks like: the accepted physical-authority reconciliation remains intact;
raw-packet and Bronze body hashes mean exact saved bytes with
`raw_stored_bytes`; derived saved-byte hashes and canonical content hashes use
independent closed pairs with no alias or fallback; wrong basis, wrong bytes, or
wrong hash fails before persistence or authority; and no unsupported recovery,
migration, Mini God Tier, or production-readiness claim is introduced.

Smallest Complete Intervention success means the shared write/read/census gate,
closed hash pairs, current packet-first IG deep-capture route, truthful fixtures,
and retrieval-home reconciliation are coherent together without reviving the
superseded retirement/stub route or widening the product surface. Mini God Tier
remains an owner-invoked capability-target lens only: the implementation must
preserve the contract's named residuals and nonclaims and must not convert green
repository tests into a capability, recovery, or readiness claim.

Treat that goal and success signal as the implementation target and an axis to
attack, not as a pass-if-matches review bar.

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: null
```

## Forseti Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: patch-only
  target_scope: the exact implementation file set listed below, reviewed only as 8cfdbc1e7807e2d9c01e8f8dc81ce1c142830e0e..7671d5cfc97ce1a891cb5a751952378d70ca7e60; any later prompt-only commit is administrative and excluded
  dirty_state_checked: receiver_must_verify
  blocked_if_missing: stop before source loading if the branch/base relationship, target worktree, clean start, de-correlation receipt, exact file set, or direct write capability cannot be verified
```

`preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.`

```yaml
escalated_deltas:
  workspace_or_repo: C:\Users\vmon7\Desktop\projects\forseti-worktrees\1b40\orca
  expected_branch: codex/silver-vault-mgt-reconciliation
  review_base_exact: 8cfdbc1e7807e2d9c01e8f8dc81ce1c142830e0e
  review_implementation_head_exact: 7671d5cfc97ce1a891cb5a751952378d70ca7e60
  review_range_exact: 8cfdbc1e7807e2d9c01e8f8dc81ce1c142830e0e..7671d5cfc97ce1a891cb5a751952378d70ca7e60
  review_head_semantics: review_implementation_head_exact is the only review head; record the later dispatch HEAD separately and exclude its administrative prompt-only delta
  isolation_decision: existing dedicated worktree and branch; do not create or switch isolation
  receiver_mechanism: operator-couriered external controller with repo access
  launch_checkout: operator_to_fill
  effective_target_worktree: C:\Users\vmon7\Desktop\projects\forseti-worktrees\1b40\orca
  target_resolution_method: verify registered worktrees and resolve the unique worktree for the expected branch
  direct_write_capability_proof: operator_to_fill by the doctrine-required target-rooted file write and git-index probe before source loading
  no_concurrent_writer_status: operator_to_fill; must be confirmed before source loading and rechecked before the first edit
  dirty_state_allowance: clean start required; only controller-created edits to the named target set and report path are allowed afterward
  untracked_files_in_scope: none at start; controller-created test scratch must be removed before return
  controlling_source_state: AGENTS.md and overlay sources are expected clean; the changed Silver contract and convergence decision are commissioned targets, not readiness evidence
  doctrine_change_decision: this is a bounded clarification of the accepted physical-authority rule; the inline DCP receipts are review targets, and the controller must not reopen the Silver v0 envelope or invent a new doctrine change
  output_mode: review-report
  report_destination: docs/review-outputs/silver_vault_physical_authority_reconciliation_delegated_adversarial_code_review_patch_v0.md; replace the tracked prior-head report with the fresh corrected-head report
  prompt_source: docs/prompts/reviews/silver_vault_physical_authority_reconciliation_delegated_adversarial_code_review_patch_prompt_v0.md
  external_source_boundary: external workflow source is read-only from Forseti work; jb is not Forseti authority
```

Before source loading:

1. Record `launch_checkout` and its write scope.
2. Run `git worktree list --porcelain`; resolve the unique worktree for
   `codex/silver-vault-mgt-reconciliation`.
3. In the effective target worktree, verify the branch, clean state, exact
   implementation commits, and ancestry for
   `8cfdbc1e7807e2d9c01e8f8dc81ce1c142830e0e..7671d5cfc97ce1a891cb5a751952378d70ca7e60`.
   Record the later dispatch HEAD separately.
4. Verify that the exact review range's changed paths equal the named target set
   below plus the tracked prior-head review report. Verify
   separately that
   `7671d5cfc97ce1a891cb5a751952378d70ca7e60..dispatch_HEAD` changes only this
   prompt. The prompt and prior report are read-only review inputs; the report
   path becomes writable only for the fresh replacement report.
5. Run the target-rooted lane-start file-write and git-index probe. Confirm no
   concurrent writer. A readable path is not write proof.
6. Stop with the nearest target-resolution blocker if any identity, byte-set,
   cleanliness, write-capability, or concurrency fact fails. Do not review an
   alternate checkout, summary, recreated copy, or context pack.
7. Recheck target identity immediately before the first edit; stop as
   `BLOCKED_TARGET_DRIFT_DURING_REVIEW` if it changed.

## Exact Review And Patch Scope

The patch may touch only these labeled targets. Everything else is read-only and
flag-only. Do not silently widen this set.

### `[authority-gate]`

- `forseti-harness/data_lake/silver_record.py`
- `forseti-harness/data_lake/silver_lineage.py`
- `forseti-harness/data_lake/product_mention_selection.py`
- `forseti-harness/data_lake/silver_census.py`
- `forseti-harness/source_capture/ig_reels_behavioral_lake.py`
- `forseti-harness/source_capture/ig_reels_behavioral_projection.py`
- `forseti-harness/data_lake/inventory.py`
- `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json`

### `[producer-refs]`

- `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
- `forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`
- `forseti-harness/cleaning/basenotes_lake.py`
- `forseti-harness/cleaning/fragrantica_lake.py`
- `forseti-harness/cleaning/parfumo_lake.py`

### `[packet-first-integration]`

- `forseti-harness/source_capture/ig_reels_deep_capture_lake.py`
- `docs/decisions/silver_vault_legacy_record_convergence_v0.md`

### `[retrieval-home]`

- `forseti-harness/data_lake/derived_retrieval_views.py`
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`

### `[proof-tests]`

- `forseti-harness/tests/test_data_lake_consumption.py`
- `forseti-harness/tests/test_data_lake_indexes_rebuild.py`
- `forseti-harness/tests/test_data_lake_rebuild_proof.py`
- `forseti-harness/tests/test_data_lake_sov_readout.py`
- `forseti-harness/tests/test_sov_extraction_quality_eval.py`
- `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- `forseti-harness/tests/contract/test_policy_module_version_pins.py`
- `forseti-harness/tests/unit/_creator_metric_silver_fixtures.py`
- `forseti-harness/tests/unit/test_creator_metric_lineage.py`
- `forseti-harness/tests/unit/test_creator_metric_silver_discovery.py`
- `forseti-harness/tests/unit/test_creator_metric_silver_producer.py`
- `forseti-harness/tests/unit/test_creator_metric_silver_reader.py`
- `forseti-harness/tests/unit/test_creator_metric_silver_snapshot.py`
- `forseti-harness/tests/unit/test_ig_reels_behavioral_lake.py`
- `forseti-harness/tests/unit/test_ig_reels_deep_capture_lake.py`
- `forseti-harness/tests/unit/test_rollup_formula_revalidation.py`
- `forseti-harness/tests/unit/test_silver_census_behavior.py`
- `forseti-harness/tests/unit/test_silver_lineage.py`
- `forseti-harness/tests/unit/test_silver_record.py`
- `forseti-harness/tests/unit/test_transcript_product_lake.py`
- `forseti-harness/tests/unit/test_youtube_creator_metric_rollup_producer_runner.py`
- `forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`

### `[owning-contracts]`

- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

The report destination is separately authorized replacement output, not
implementation patch scope. The tracked prior-head report is evidence only until
the replacement write. This prompt, `AGENTS.md`, overlay sources, all other
contracts/decisions, generated artifacts, installed skills, and all other tests
are read-only. Flag an off-scope fix; do not apply it.

Why read-only review is insufficient: the fused checkpoint explicitly
commissions a bounded review-and-patch pass so safely closable defects in this
exact implementation can be corrected before home-model adjudication. Patch
authority is subordinate to the named scope and does not extend to architecture
changes.

## Required Reads And Method Sequence

Use a bounded custom source pack. Pointer over copy.

### REFERENCE-LOAD

Read these as operating instructions only. Do not apply the review method yet:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md` — When It Applies, The
  Loop, Access Selection Rule, De-correlation, code-diff target kind, and Overlay
  Interface
- `.agents/workflow-overlay/prompt-orchestration.md` — Review Prompt Defaults,
  Repo-Bound Review Target Resolution, and Output Modes
- `.agents/workflow-overlay/review-lanes.md` — Current Lanes, Review Doctrine,
  and Rules
- `workflow-code-review` skill instructions

Do not apply `workflow-code-review` before source readiness.

### SOURCE-LOAD

Read:

- the exact
  `8cfdbc1e7807e2d9c01e8f8dc81ce1c142830e0e..7671d5cfc97ce1a891cb5a751952378d70ca7e60`
  diff and all named target files;
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`;
- `docs/decisions/silver_vault_legacy_record_convergence_v0.md`;
- the tracked prior-head report only as adjudicated historical review input, not
  as approval or a substitute for reviewing the corrected diff;
- only adjacent source directly imported or invoked by a questioned target when
  needed to prove a finding.

Do not load prior Silver review prompts or review outputs as a substitute for
the current diff. Do not inspect a private or live data lake.

Declare `SOURCE_CONTEXT_READY` with loaded, missing, excluded, and conflicting
sources, or `SOURCE_CONTEXT_INCOMPLETE` and the resulting blocker. Only after
`SOURCE_CONTEXT_READY` may you apply the review method.

### APPLY

Invoke and apply `workflow-code-review` to the completed repository diff. Be
maximally adversarial and coverage-first inside the commissioned scope. Findings
come first. Report every issue found, including minor or low-confidence issues;
severity and confidence are labels, not filters. List steelman-defeated
candidates compactly under `considered_and_defended`.

## Owner-Bound Behavior To Attack

- A Silver record is authoritative only when the `silver_vault_record_v0`
  envelope is valid and every claimed source physically resolves and verifies.
- Both Silver write front doors must fail before any bytes are persisted when a
  source is unresolved or tampered. Record-set validation must be all-before-any.
- Authority-making readers and the existing Silver census must use the same
  root-aware physical gate.
- Raw refs must explicitly identify `raw_packet` or
  `bronze_attachment_record`; Bronze resolution may use only public
  `source_surface_catalog_rows` and `load_attachment_record_body` surfaces.
- Raw-packet and Bronze Attachment Record `sha256` always means exact preserved
  body bytes and pairs only with `hash_basis: raw_stored_bytes`. Source type
  remains in existing provenance fields.
- Derived refs require exact `raw_anchor + lane + record_id`. A claimed
  `sha256` hashes exact saved derived-record bytes and pairs only with
  `hash_basis: derived_record_bytes`. A claimed `content_hash` pairs separately
  with `content_hash_basis: canonical_json_excluding_content_hash`; either pair
  may appear, both may coexist, and neither aliases or falls back to the other.
- Preserve main's packet-first IG deep-capture producer, registry, runner, and
  supported-leg behavior. Its current Silver records may be authoritative only
  through the same physical verifier used by readers and census; historical
  grammar-B records remain audit-only. Do not replay the superseded
  retirement/stub route or invent another producer.
- The existing `data_lake/silver_census.py` must be extended, not replaced or
  duplicated. Physically unresolved records are named non-authority errors and
  cannot inflate observation headlines.
- The exact-policy product-mention selector remains the selection policy; do not
  redesign it.
- Only `by_mention` and `undone` move to the Silver Vault contract-owned
  `indexes/derived_retrieval/silver_vault/core/query_tables` and paired
  `manifests` home. `by_creator` remains deferred. Do not add `by_video` or
  `by_metric_time`.
- `lineage_schema_version` is not required by the official envelope.
- No live `F:\forseti-data-lake` writes, migration, recapture, reprocessing, or
  private-lake-layout guesses.
- Do not claim that 226 unavailable records were recovered. Repository tests do
  not establish Mini God Tier or production readiness.

Only the YouTube metric-observation producer's emitted ref meaning changed; its
producer schema is therefore expected to move from v1 to v2. Its rollup producer
and unrelated producers remain unbumped unless direct evidence proves their
emitted semantics changed. The 196-observation fixture is synthetic structural
proof only, not proof that private-lake seed sources resolve.

Actively attack closed-basis validation, raw-ref/manifest disagreement,
raw-packet manifest ambiguity, Bronze ref/catalog/body mismatch, altered saved
bytes, derived pair aliasing or fallback, derived-ref path/hash substitution,
mixed valid/invalid record sets, and tests that accidentally present synthetic
fixtures as private-lake recovery proof. Also check that the accepted shared
write/read/census/selector gate and all-before-any persistence behavior were not
regressed by the correction.

## Patch And Escalation Contract

Patch only a finding that is safely closable within the exact named target set.
Keep each change traceable to a finding and preserve real failure visibility.
Do not weaken tests, add a success fallback, infer private lake layout, or expand
the requested capability.

If the correct fix requires an off-scope file, doctrine change, new producer,
live-lake action, or redesign, return `NEEDS_ARCHITECTURE_PASS`, revert any
partial patch for that design-level issue, and report findings only. Off-scope is
flag-only.

The returned diff, citations, and verdict are claims for the home/Chief
Architect to adjudicate, not premises to inherit. Nothing is kept until that
adjudication accepts, modifies, or rejects each material change against its
citations and the owner-bound intent.

## Validation

Inspect the already-recorded validation evidence, then run validation relevant
to any controller patch. Every command must report `pass`, `fail`, `blocked`, or
`not_run`; never turn a missing run into success.

At minimum after any behavioral patch, run the focused tests for the touched
authority/producer/reader/retrieval surface and the relevant cross-surface
subset. If the patch could affect the integrated behavior, rerun this combined
suite from `forseti-harness`:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q tests/unit/test_silver_record.py tests/unit/test_silver_lineage.py tests/unit/test_youtube_creator_metric_silver_producer.py tests/unit/test_youtube_creator_metric_rollup_producer_runner.py tests/unit/test_creator_metric_silver_producer.py tests/unit/test_creator_metric_silver_discovery.py tests/unit/test_creator_metric_silver_reader.py tests/unit/test_creator_metric_silver_snapshot.py tests/unit/test_rollup_formula_revalidation.py tests/unit/test_silver_census_behavior.py tests/contract/test_silver_reader_selection_gate.py tests/contract/test_policy_module_version_pins.py tests/contract/test_data_lake_inventory_gate.py tests/contract/test_capture_runner_lake_seam_coverage.py tests/test_data_lake_indexes_rebuild.py tests/test_data_lake_sov_readout.py
```

Also run `git diff --check`. Run the diff-scoped retrieval-header and DCP gates
when a controller patch touches either changed Markdown contract. Do not write to
or inspect a live data lake.

## Durable Review Report

Write the review to:

`docs/review-outputs/silver_vault_physical_authority_reconciliation_delegated_adversarial_code_review_patch_v0.md`

The report must include:

- retrieval metadata appropriate to a review output;
- `reviewed_by` with the actual reviewer model/version, or `unrecorded` only when
  tooling truly does not supply it;
- `authored_by: OpenAI GPT-5 Codex`;
- exact review base and implementation head reviewed, the separately recorded
  administrative dispatch HEAD, branch, worktree, initial/final dirty state,
  and de-correlation receipt;
- findings first, each with target label, location, evidence, impact, severity
  (`critical`, `major`, or `minor`), confidence (`high`, `medium`, or `low`),
  `minimum_closure_condition` stated as an end state, and
  `next_authorized_action`;
- `considered_and_defended` for candidates the evidence defeated;
- a unified working-tree diff summary for controller patches, with every change
  attributed to its target label;
- neutral, decision-sufficient per-change source citations;
- validation evidence with exact commands and observed results;
- overall verdict plus materially different per-label sub-verdicts, without a
  production-readiness or Mini God Tier claim;
- residual risk and explicit not-proven boundaries;
- an adjudicator next-moves tail that points the commissioning Chief Architect
  to `.agents/workflow-overlay/communication-style.md` -> Review Adjudication
  Next Step.

Do not return a `patch_queue_entry`; you have direct bounded patch authority.
Optional hardening must be labeled optional and non-required.

## Hard Stop

Do not commit, push, create or update a PR, merge, stash, reset, clean up a
worktree, run repository hygiene, or perform any other lifecycle action. Leave
the bounded patch and review report uncommitted for Chief Architect
adjudication. Report the final changed-file set and any controller-created
scratch that could not be removed.
