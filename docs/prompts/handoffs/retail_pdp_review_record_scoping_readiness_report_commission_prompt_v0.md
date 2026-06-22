# Retail PDP Review Record Scoping Readiness Report Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Capture-lane report commission prompt
scope: >
  Commissions the next retail PDP review_record report: decide whether the
  recon can move to implementation scoping by resolving or sharply routing the
  Attachment Record writer/storage blocker, Sephora native review ID mapping
  risk, and Ulta PowerReviews ID semantics risk.
use_when:
  - Commissioning a fresh Capture CA lane after the retail PDP review_record recon.
  - Turning the Amazon/Sephora/Ulta recon into a scoping-readiness decision.
  - Checking which blockers must be resolved before adapter implementation.
authority_boundary: retrieval_only
open_next:
  - docs/research/retail_pdp_review_record_capture_recon_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - orca-harness/source_capture/retail_pdp_projection.py
branch_or_commit: codex/retail-pdp-review-recon @ 3da8d9268af740780139b2683cebbf746010f396
stale_if:
  - The retail PDP review_record recon report is superseded.
  - Attachment Record writer/storage binding changes or is implemented.
  - Sephora or Ulta review DOM/API substrate is rerun or materially changes.
  - A later report resolves the scoping-readiness decision.
```

Paste the body below into a fresh Capture CA thread in this workspace.

---

You are the Capture Chief Architect for Orca.

## Objective

Produce the next report after the Retail PDP review_record recon: a
scoping-readiness report that decides whether a `retail_pdp` individual review
record adapter can move to implementation scoping, or exactly what remains
blocked.

This is a report commission, not an implementation commission.

The three concrete blockers to resolve or route are:

1. Attachment Record writer/storage binding.
2. Sephora native Bazaarvoice review ID mapping for non-image rows.
3. Ulta PowerReviews numeric DOM ID semantics.

The report must not pretend those blockers are resolved if evidence is missing.
It should make the next move boring: either implementation scoping is now
bounded enough, or one named upstream decision/probe is still required.

## ELI5 Starting Point

- We found that reviews are visible on the retailer pages.
- We have not yet proven exactly how to write one review as a durable Orca
  Attachment Record.
- Sephora shows review details, but we need to know which native ID belongs to
  each visible review row.
- Ulta shows review details, but we need to know whether the PowerReviews
  numeric IDs in the DOM are actual native review IDs or just UI element IDs.

## Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: owner request to commission the next report after retail PDP review_record recon.
objective: >
  Write one scoping-readiness report that resolves or sharply routes the three
  blockers before implementation scoping: Attachment Record binding, Sephora
  native ID mapping, and Ulta ID semantics.
intended_decision: >
  Decide whether the retail PDP review_record adapter is READY_FOR_IMPLEMENTATION_SCOPING,
  PARTIAL_READY_ATTACHMENT_BLOCKED, BLOCKED_SELECTOR_ID_VERIFICATION,
  BLOCKED_NEEDS_DATA_LAKE_BINDING_DECISION, or RUN_REQUIRED_NO_AUTHORITY.
target_files_or_dirs:
  - docs/research/retail_pdp_review_record_scoping_readiness_report_v0.md
  - docs/research/retail_pdp_review_record_capture_recon_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_v0.md
source_pack: bounded custom pack listed below.
output_mode: file-write
edit_permission: docs-write for the report only; no source code, runtime, packet, overlay, or product-authority edits.
dirty_state_allowance: use a clean worktree off the PR branch or current main; unrelated dirty files are out of scope.
controlling_source_state: reread required in receiver thread before strict claims.
branch_or_commit_reference: commission authored on codex/retail-pdp-review-recon @ 3da8d9268af740780139b2683cebbf746010f396.
doctrine_change_decision: >
  The report may recommend an upstream Data Lake or Attachment Record decision,
  but must not apply doctrine changes. If it needs a source-access, storage,
  manifest, or lifecycle change, name the propagation surfaces and stop at recommendation.
isolation_decision: new worktree off PR branch or current main; this is report-writing work adjacent to an active PR.
validation_gates: retrieval-header strict check, header-index strict check, report hash/readback, no readiness/validation claim unless source-bound.
thread_operating_target_continuity: not carried forward; this is a fresh commissioned report lane.
```

## Required Reads

Authority and workflow:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Retail PDP recon and review:

- `docs/research/retail_pdp_review_record_capture_recon_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_v0.md`
- `docs/prompts/reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_patch_prompt_v0.md`

Attachment Record and packet/storage sources:

- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
- `orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md`
- `orca/product/spines/capture/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/writer.py`

Retail PDP source and harness sources:

- `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md`
- `orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md`
- `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/runners/run_source_capture_cloakbrowser_packet.py`
- `orca-harness/runners/run_retail_pdp_projection.py`

Optional local evidence:

- Existing packet scratch may be present at
  `orca-harness/_test_runs/retail_pdp_review_recon_20260620/`.
- If present, you may inspect it as local reported evidence. State clearly that
  it is gitignored/untracked and not repo-reproducible.
- If absent or insufficient, do not invent selector certainty. Return a
  `RUN_REQUIRED_NO_AUTHORITY` or `BLOCKED_SELECTOR_ID_VERIFICATION` result with
  the exact smallest verification run needed.

Branch-only sources named by the recon:

- The commission prompt, review capture spec, and manufactured-demand design are
  reported as existing only in `.claude/worktrees/distracted-ishizaka-01eff5`.
  They are not tracked on this branch. Do not treat them as openable authority
  unless you independently verify they are present and state their status.

## Source-Gated Method

1. Run Orca Cynefin routing before planning. Include the allowed next move and
   the disallowed next move.
2. REFERENCE-LOAD `workflow-deep-thinking` and
   `workflow-architecture-planning` if available.
3. SOURCE-LOAD the required local sources above.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with material
   gaps.
5. Only after source readiness, APPLY the methods to the loaded context.
6. Do not use subagents unless the source context is ready and the assignments
   are narrow. If used, suggested roles are:
   - Attachment Record binding mapper.
   - Sephora selector/ID evidence checker.
   - Ulta selector/ID evidence checker.

## Hard Boundaries

Do not:

- Implement code.
- Modify source code, tests, packet artifacts, overlays, or product-authority contracts.
- Run live browser/network capture unless the owner separately authorizes an exact bounded run.
- Use auth, credentials, proxy, CAPTCHA solving, challenge clicking, stored browser profiles, or gate defeat.
- Claim validation, readiness, product acceptance, implementation completion, or production fixture status.
- Expand the scope to graph construction, reviewer identity, deduplication,
  fraud/integrity scoring, Cleaning, ECR, Judgment, or downstream routing.

You may recommend future implementation scoping or a bounded verification run,
but that recommendation is not execution authority.

## Questions The Report Must Answer

### 1. Attachment Record blocker

Answer:

- Does the current Attachment Record contract already bind enough to scope a
  `review_record` writer, or does exact packet-member/sidecar layout remain a
  blocker?
- What is the smallest acceptable Attachment Record shape for retail PDP
  `review_record` bodies, using only raw source-visible fields?
- Which keys are required in the compact manifest/index entry?
- What must be hash-checkable, immutable, and packet-relative?
- Which decisions belong to a Data Lake/Attachment Record lane rather than the
  retail PDP adapter lane?

Do not select a physical backend, storage engine, queue, scheduler, database,
warehouse, or production layout unless a current source already binds it.

### 2. Sephora ID mapping blocker

Answer:

- For visible Sephora review rows, where is the native Bazaarvoice review ID?
- Is the ID available for every row, only media rows, or only through an adjacent
  embedded/API substrate?
- What selector or source path should a future adapter use?
- What is still unverified?
- If evidence is insufficient, what exact smallest bounded rerun or packet
  inspection would verify it?

### 3. Ulta ID semantics blocker

Answer:

- Are numeric PowerReviews DOM IDs such as `pr-rd-review-headline-580013849`
  native review IDs, stable UI IDs, or unresolved candidate IDs?
- Does JSON-LD expose enough identity to avoid binding to the DOM ID?
- What selector/source path should a future adapter use?
- What remains unverified?
- If evidence is insufficient, what exact smallest bounded rerun or packet
  inspection would verify it?

### 4. Amazon scope boundary

Answer briefly:

- Does Amazon remain usable for PDP-embedded top reviews only?
- Does all-review pagination remain blocked under the no-gate-defeat route?
- Should Amazon be included in first implementation scoping, or held as a
  partial source while Sephora/Ulta carry the first full `review_record` path?

## Required Recommendation Labels

Choose one primary label:

- `READY_FOR_IMPLEMENTATION_SCOPING`
- `PARTIAL_READY_ATTACHMENT_BLOCKED`
- `BLOCKED_NEEDS_DATA_LAKE_BINDING_DECISION`
- `BLOCKED_SELECTOR_ID_VERIFICATION`
- `RUN_REQUIRED_NO_AUTHORITY`
- `NO_GO_RECON_STALE`

You may include secondary labels for mixed results, for example:
`SELECTORS_READY__ATTACHMENT_BLOCKED`.

## Required Output Artifact

Write exactly one durable report:

`docs/research/retail_pdp_review_record_scoping_readiness_report_v0.md`

Use a retrieval header and mark the report non-authorizing. The report must be
readable as a decision input without opening packet scratch.

## Output Structure

The report should include:

1. Title and retrieval header.
2. Status and non-authorizing boundary.
3. Source readiness and missing sources.
4. Cynefin routing result.
5. ELI5 summary of the three blockers.
6. Attachment Record binding analysis.
7. Sephora ID mapping analysis.
8. Ulta ID semantics analysis.
9. Amazon partial-scope note.
10. Recommendation label.
11. Minimal implementation-scoping surface if ready, or exact next blocker if not.
12. Evidence table with `repo-verifiable`, `local-scratch`, and `unverified` labels.
13. Owner decisions needed.
14. Required follow-up prompt/report/run, if any.
15. Non-claims.

## Success Bar

The report succeeds if the owner or next Capture CA can answer:

- Can we start implementation scoping now?
- If not, exactly which blocker remains and who owns it?
- Which retailer paths are first-scope candidates?
- Which selector or ID assumptions are verified, local-scratch-only, or unverified?
- What would the smallest legal/allowed verification run be if a run is needed?

The report fails if it:

- Treats a local scratch packet as committed evidence.
- Pretends Sephora/Ulta native ID semantics are solved without evidence.
- Hides that Attachment Record physical layout/writer seam may still be open.
- Uses `GO` language as build authorization.
- Runs live capture or edits code.

## Non-Claims

This commission is not implementation authorization, runtime authorization,
source-access boundary amendment, Attachment Record architecture acceptance,
validation, readiness, product proof, commercial authorization, fixture
admission, ECR, Cleaning, Judgment, production storage, scheduler work, or PR
merge authority.