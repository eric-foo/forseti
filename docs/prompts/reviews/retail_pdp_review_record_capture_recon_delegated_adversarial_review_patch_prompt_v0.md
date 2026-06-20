# Retail PDP Review Record Capture Recon Delegated Adversarial Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Route-out prompt for a de-correlated delegated adversarial review-and-patch pass on the retail PDP review_record capture recon report.
use_when:
  - Commissioning an independent controller to harden the retail PDP review_record capture recon report before downstream adapter scoping.
  - Checking whether the recon report overclaims Amazon, Sephora, Ulta, Attachment Record, or implementation-readiness evidence.
  - Producing a bounded diff and report for Chief Architect adjudication.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/research/retail_pdp_review_record_capture_recon_v0.md
input_hashes:
  docs/research/retail_pdp_review_record_capture_recon_v0.md: 30D3F9D6F1152483800969CC9E539317B3120C3AF52F82671A8F560DAAAF342C
branch_or_commit: codex/retail-pdp-review-recon @ 0dd2f355552b8c91d31aa67b20c0d0922e1126da
stale_if:
  - docs/research/retail_pdp_review_record_capture_recon_v0.md changes.
  - PR 312 is rebased, amended, closed, or superseded.
  - Amazon, Sephora, or Ulta recon packet evidence is rerun or replaced.
  - Attachment Record writer/storage binding changes.
```

## Orca Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom delegated-review-patch route-out prompt pack
  edit_permission: patch-only when all commission receipt fields are filled and de-correlation is satisfied; otherwise read-only blocked return
  target_scope: single research recon report only
  dirty_state_checked: yes
  blocked_if_missing:
    - de-correlation receipt
    - controller access mode
    - repo access to the pinned worktree or an explicit no_repo package
    - output report destination write permission
```

- Output mode for this prompt artifact: `file-write` under `docs/prompts/reviews/`, with paste-ready-chat copy allowed for dispatch.
- Downstream controller output mode: `review-report` plus bounded working-tree diff only when `access_mode: repo`; advisory findings only when `access_mode: no_repo`.
- Template kind: `review`, using the registered `adversarial-artifact-review` template plus the provisional delegated-review-patch convention.
- Target file: `docs/research/retail_pdp_review_record_capture_recon_v0.md`.
- Target hash at prompt creation: `30D3F9D6F1152483800969CC9E539317B3120C3AF52F82671A8F560DAAAF342C`.
- Expected branch / revision: `codex/retail-pdp-review-recon` at `0dd2f355552b8c91d31aa67b20c0d0922e1126da`.
- Dirty-state allowance for controller: target file may be modified only by the delegated patch pass after preflight; unrelated dirty/untracked files are out of scope and must be flagged, not touched.
- Report destination: `docs/review-outputs/adversarial-artifact-reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_v0.md`.
- Doctrine change decision: this prompt does not change doctrine. It routes a provisional review-and-patch convention already bound in the overlay.
- Isolation decision: use the existing lane branch/worktree or a fresh worktree off PR 312 branch; never review a substitute checkout.
- Validation gates: target hash/HEAD check, report write verification, final `git diff` scope check, and no committed changes unless a later CA explicitly authorizes commit.
- Thread operating target continuity: no visible active `thread_operating_target`; omitted for `no_visible_active_target`.

## Delegated Review-And-Patch Commission Receipt

This is an incomplete-commission route-out. Before starting review or patch work, the operator or receiving lane must replace every `operator_to_fill` value below or return the nearest blocker.

```yaml
lane_binding:
  overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lane: artifact via workflow-adversarial-artifact-review after SOURCE_CONTEXT_READY
  mode: base-subagent
  access_mode: operator_to_fill(repo | no_repo)
  actor_model_family_receipt:
    author_home_model_family: OpenAI/GPT-family Codex lane authored the target report; exact model/version operator_to_fill or unrecorded
    controller_model_family: operator_to_fill_must_differ_from_author_home_family_for_cross_vendor_discovery
    current_receiving_actor_role: controller
    dispatch_mode: external-controller-courier
    de_correlation_status: operator_to_fill(satisfied | blocked)
  de_correlation_bar: operator_to_fill(cross_vendor_discovery | same_vendor_sanity | self_fallback)
  no_model_recommendation: true
```

Hard block rules:

- If the controller model family is missing, undisclosed, or the same vendor/model lineage as the author/home family, do not claim delegated cross-vendor discovery. Return `BLOCKED_DECORRELATION_RECEIPT_MISSING` or `BLOCKED_CONTROLLER_NOT_DECORRELATED`.
- If `access_mode: repo` is selected but the controller cannot access the pinned worktree/revision, return a worktree/source blocker.
- If `access_mode: no_repo` is selected, do not patch. Return advisory findings only; the CA must apply any accepted patch and then run the required bounded post-patch re-review before keeping changes.
- Do not include a `Recommended model` block or any runtime model recommendation.

## Objective

Harden the recon report so a downstream Capture CA can safely decide whether to scope a `retail_pdp` `review_record` adapter. The report must make the source-access verdicts, field-shape risks, Attachment Record blocker, and non-claims impossible to misread.

Fitness reference:

- Goal: the recon report should be a reliable decision input for the next capture-lane scoping move.
- Observable success signal: a fresh CA can tell, from the report alone plus named sources, which retailer paths are GO, PARTIAL, or BLOCKED; which fields remain unverified; why adapter implementation is still blocked; and what is forbidden, without inferring readiness or authority that is not present.

Why read-only review is insufficient:

- The report is intended to route downstream scoping. If it overclaims or under-specifies a blocker, a review-only loop would likely return a patch request to the authoring lane. A bounded patch to the single report file is the smallest complete way to correct factual, boundary, or source-loading defects while the reviewer has the issue in context.

Bounded patch scope:

- Patch only `docs/research/retail_pdp_review_record_capture_recon_v0.md`.
- Patch only claim-boundary, source-citation, retrieval metadata, output-boundary, access-verdict, field-risk, or next-scope wording defects.
- Do not edit source code, packet artifacts, prompt artifacts, overlay files, branch-only source docs, PR metadata, tests, or any other file.
- If the correct fix requires another file, a source rerun, a doctrine change, an Attachment Record design decision, or adapter implementation, flag it and return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding. Do not patch around it.

## Required Source Sequence

REFERENCE-LOAD these method instructions first. Do not APPLY them before source readiness:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`
- `workflow-delegated-review-patch` mechanics as carried by this prompt and `.agents/workflow-overlay/delegated-review-patch.md`

SOURCE-LOAD these Orca sources:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/prompt-orchestration.md`
6. `.agents/workflow-overlay/review-lanes.md`
7. `.agents/workflow-overlay/delegated-review-patch.md`
8. `.agents/workflow-overlay/validation-gates.md`
9. `.agents/workflow-overlay/retrieval-metadata.md`
10. `docs/research/retail_pdp_review_record_capture_recon_v0.md`

Then read target `open_next` sources only when material and accessible. At minimum, check whether the following are available and state gaps explicitly:

- `docs/prompts/handoffs/retail_pdp_review_capture_commission_prompt_v0.md`
- `orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `orca-harness/source_capture/retail_pdp_projection.py`

Packet scratch note: the report points at local scratch under `orca-harness/_test_runs/retail_pdp_review_recon_20260620/`. If those packet artifacts are absent in the receiving worktree, say so and review the report as a claim-bearing artifact with unverified scratch evidence rather than pretending packet verification happened.

Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before APPLYING the methods. If incomplete, name the missing sources and which claims they affect.

## Review Axes To Attack

Attack material failure modes, not style nits:

- Amazon classification: Does the report correctly separate blocked all-reviews pagination from PDP-embedded top-review availability, without implying full Amazon corpus access?
- Sephora classification: Does it clearly distinguish source-visible fields from the unresolved native-review-ID mapping for non-image rows?
- Ulta classification: Does it clearly distinguish JSON-LD/PowerReviews per-review fields from unresolved native-ID semantics?
- Attachment Record blocker: Does it prevent a downstream adapter build from claiming durable `review_record` Attachment Records before writer/storage binding exists?
- Evidence durability: Does it make clear that `_test_runs` packet artifacts are local scratch and not production fixtures or committed evidence?
- Source authority: Does it avoid treating branch-only docs, local scratch, or the report's own assertions as source-of-truth authority?
- Prompt/report hygiene: Does the retrieval header stay retrieval-only and avoid approval, validation, readiness, or implementation authority?
- Forbidden work: Does it preserve no auth, no proxy, no CAPTCHA solving, no challenge clicking, no source discovery, no graph/dedup/identity/integrity, no volume capture, and no downstream Judgment/Cleaning claims?

## Controller Output Contract

If the commission receipt is complete and the source context is ready:

1. APPLY `workflow-deep-thinking` to frame the boundary problem and likely failure modes.
2. APPLY `workflow-adversarial-artifact-review` to produce findings-first adversarial artifact review findings.
3. If `access_mode: repo`, patch only the target file for accepted material findings inside the bounded patch scope. Leave changes uncommitted.
4. Write the durable report to `docs/review-outputs/adversarial-artifact-reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_v0.md`.
5. Return a compact chat courier with the `review_summary` YAML shape from `.agents/workflow-overlay/communication-style.md`.

The durable report must include:

- `reviewed_by` and `authored_by` fields, using operator-supplied exact model/version values or `unrecorded`; never fabricate.
- The de-correlation receipt and `de_correlation_bar`.
- Source-read ledger with material gaps.
- Findings ordered by `critical`, `major`, then `minor`.
- For each finding: severity, location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and correction direction.
- Unified diff or exact changed hunks when repo-mode patching occurred.
- Residual-risk note.
- Review-use boundary: findings and patched diff are decision input only, not approval, validation, readiness, mandatory remediation, source-of-truth promotion, or executor-ready authority until CA adjudicates.

Do not emit `patch_queue_entry` unless a separate patch-queue review is explicitly commissioned. Do not commit, push, merge, or open/modify a PR.

If a design-level issue prevents safe bounded patching, return `NEEDS_ARCHITECTURE_PASS`, revert any partial target-file diff, and provide findings only.

## CA Adjudication Contract

The returned diff, citations, verdict, and residual risk are claims to adjudicate, not premises to inherit. The CA may accept, reject, or modify each change. No delegated change is kept until the CA fresh-reads the target diff and report, verifies cited evidence, and decides what remains.

## Paste-Ready Launch Wrapper

Operator: before sending this prompt to the controller, fill the `operator_to_fill` fields in the commission receipt or explicitly instruct the controller to block on them. Do not add runtime model recommendations.