# Cleaning Spine Real-Data Smoke Raw-To-Cleaned Efficacy Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for adversarial evidence-trace review of the
  2026-06-21 Cleaning spine real-data smoke run: captured raw/source packet
  material -> ECR source-side receipts -> CleaningPacket handles.
use_when:
  - Commissioning a de-correlated reviewer to test whether the raw captured
    material and cleaned handles support the same bounded smoke conclusion.
  - Checking whether the real-data smoke preserved raw/projection/ECR links
    without overclaiming product proof, Judgment readiness, or live E2E readiness.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/product-proof.md
branch_or_commit: codex/cleaning-spine-continuation at bc950cdfeeb3a02f33bf52217d71e049aa9093f2
stale_if:
  - The smoke output directory is deleted or overwritten.
  - The stitcher runner or Cleaning models change after this prompt is filed.
  - The worktree branch or HEAD differs from the pinned branch/head above.
  - The review-output destination already exists and the operator has not authorized a new version.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is review-report to `docs/review-outputs/adversarial-artifact-reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_v0.md`.
- Template kind: adversarial-artifact-review. Template targets are prompt-shaping only; no runtime model recommendation, ranking, or implication is made.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`, branch `codex/cleaning-spine-continuation`, HEAD `bc950cdfeeb3a02f33bf52217d71e049aa9093f2`, dirty state allowed exactly as listed below.
- Reviews: findings-first. Severity labels `blocker`, `major`, and `minor` are prioritization labels only. This review may state the bounded trace conclusion values named in this prompt, but must not emit Orca validation, approval, readiness, mandatory remediation, or patch authority.
- Doctrine change: none intended. This prompt routes an evidence-trace review and does not change Capture, ECR, Cleaning, Judgment, product-proof, review, prompt, or workflow doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/adversarial-artifact-reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_v0.md`.

## Commission

Run an adversarial review of the product efficacy of this smoke, where "efficacy" means only:

> Can an independent reviewer trace the raw captured material, projection/consolidation outputs, ECR source-side receipts, and CleaningPacket handles well enough to reproduce or reject the same bounded conclusion: the Cleaning spine can preserve source-visible real-data substrate through Source Capture-shaped packets into ECR refs and Cleaning handles without fabricating success?

Do not evaluate or claim buyer proof, demand proof, market conclusion truth, Judgment quality, product readiness, commercial readiness, or full live capture-to-Judgment E2E readiness. If the source material looks interesting or persuasive, that is not a proof claim.

## Delegated-Review-Patch Route-Out Boundary

This prompt was prepared after an explicit `workflow-delegated-review-patch` invocation. The requested target is not eligible for a patch executor because it is a multi-artifact smoke run plus ignored `_test_runs` outputs, not one Chief Architect-named authored target file. Therefore:

- no patching is authorized;
- no source edits are authorized;
- no commit, push, PR, live capture rerun, CAPTCHA/login, or network retry is authorized;
- this is a read-only adversarial evidence-trace review;
- patch-worthy issues must be reported as findings with minimum closure conditions, not as executor-ready patch queues.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the current authoring lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor/model lineage to claim cross-vendor discovery.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing or same-vendor, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- reviewed_by and authored_by must be recorded in the durable report. Use `unrecorded` only when the factual identity is not supplied; never fabricate it.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-adversarial-artifact-review` if available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and unavailable tools.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY adversarial artifact review to produce findings-first review.
5. If `workflow-adversarial-artifact-review` is unavailable, continue only as advisory critique and mark strict review claims `NOT_CLAIMED`.
6. If you do not have repository/filesystem access, stop and request a pasted source capsule or no-repo handoff. Do not infer from this prompt alone.

## Required Reads

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/product-proof.md`
- `docs/hygiene/cleaning_spine_lane_handoff_v0.md` if present; if absent, record the absence and continue from the current prompt plus actual in-repo sources.

Then read the Cleaning/Capture/ECR contracts needed to avoid treating the smoke as source truth or Judgment:

- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca-harness/cleaning/projection.py` for the current projection-to-handle implementation surface.
- `orca-harness/ecr/deriver.py` for the current ECR source-side posture implementation surface.

Then read the smoke implementation and model context:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`

## Target Smoke Outputs

Run root:

`orca-harness/_test_runs/cleaning_spine_real_data_smoke_20260621/`

Primary stitched outputs:

- `stitched/cleaning_packet.json`
  - SHA256: `583231825771BD6D1C57A04F5418D53A457AC2D5D7EB83B85F0C53F0E2A0F7F2`
- `stitched/ecr_source_side_receipts.json`
  - SHA256: `96857AD2AF44B370AEDD65BD109AE047B9FD8C0DF824061EF6BC4F6A3CB95567`
- `stitched/smoke_summary.json`
  - SHA256: `4990AC4104CFF1310F582142BEB9EE6FF1E8067BA3FB0F2FC0C003204EFFE82F`
- `capture_ecr_cleaning_smoke_manifest.json`
  - SHA256: `8D87F17C2B87FF90C4A33B47F073C84C0587DC004E777E5EFA0A275A3ECCFADD`

Capture summaries:

- `reddit_batch/batch_summary.json`
  - SHA256: `4DFEDB698651D5B086709EB5E9AD05594298E611BF938DE895D39855E97A413E`
- `retail/retail_capture_summary.json`
  - SHA256: `8410CE643E4D17DA27802D6DFDEB6CFFDD18DB3F6BBE1D1F5A354C59E16597FA`

Reddit target selection and capture artifacts:

- `reddit_candidates/fragrance_marketing/reddit_candidate_url_intake.json`
- `reddit_candidates/perfume_marketing/reddit_candidate_url_intake.json`
- `reddit_candidates/beauty_marketing/reddit_candidate_url_intake.json`
- `reddit_thread_urls.json`
- `reddit_batch/reddit_001_packet/`
- `reddit_batch/reddit_001_derived/reddit_thread_consolidation.json`
- `reddit_batch/reddit_002_packet/`
- `reddit_batch/reddit_002_derived/reddit_thread_consolidation.json`
- `reddit_batch/reddit_003_packet/`
- `reddit_batch/reddit_003_derived/reddit_thread_consolidation.json`

Retail target selection and capture artifacts:

- `retail/sephora/packet/`
- `retail/sephora/retail_pdp_projection.json`
- `retail/ulta/packet/`
- `retail/ulta/retail_pdp_projection.json`
- `retail/amazon/packet/`
- `retail/amazon/retail_pdp_projection.json`

For every packet directory, inspect `manifest.json` and the referenced raw/preserved files as needed. Do not rely on summary JSON alone for raw-to-cleaned trace claims.

## Dirty-State Allowance

The lane is intentionally dirty. Review only this smoke and its required context unless a dirty dependency directly affects trace correctness.

Observed status at prompt creation:

```text
## codex/cleaning-spine-continuation...origin/main [behind 6]
 M docs/workflows/orca_repo_map_v0.md
 M orca-harness/cleaning/models.py
 M orca-harness/tests/unit/test_cleaning_core.py
?? docs/prompts/reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_prompt_v0.md
?? docs/prompts/reviews/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_prompt_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_claude_cross_vendor_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md
?? docs/review-outputs/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md
?? docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
?? orca-harness/runners/run_capture_ecr_cleaning_smoke.py
?? orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
```

The `_test_runs/` directory is ignored by `.gitignore`; treating those files as observed smoke evidence is allowed for this review, but their presence is not source promotion or durable product proof.

## Independent Trace Passes

The controller should run two independent trace passes. If the review environment supports subagents, the controller may assign one pass to each subagent using this same source pack and require schema-bound returns. If no subagent capability exists, the controller must run both passes itself in separate notes. Do not ask subagents to skip the source-readiness contract.

Pass A, raw-first:

- Start from each of the six packet directories: 3 Reddit thread packets and 3 Retail/PDP packets.
- For each packet, read `manifest.json`, packet id, source family, preserved raw file ids, relative paths, and stored hashes.
- Follow raw files to the Reddit consolidation rows or Retail projection rows.
- Follow those rows into `cleaning_packet.json` handles.
- Check that the Cleaning handles preserve packet id, slice id where applicable, file id, relative packet path, hash basis, sha256, anchor kind, projection ref when applicable, and ECR ref packet-key coupling.
- At summary level, cover all 6 sources. At row/detail level, cover at least:
  - all 3 Reddit post handles;
  - at least 1 Reddit comment handle from each Reddit packet;
  - at least 2 Retail handles per retailer;
  - any row or handle tied to a reported residual.

Pass B, clean-first:

- Start from `stitched/cleaning_packet.json`.
- Group handles by `source_family` and `packet_id`.
- For each group, follow `raw_anchor` and `projection_ref` or consolidation refs back to the packet directory and raw/preserved file.
- Verify the `ecr_ref` points to a receipt for the same packet id in `stitched/ecr_source_side_receipts.json`.
- Look for Judgment vocabulary, demand/salience/credibility decisions, semantic transforms, or actionability claims. Any such material in Cleaning handles is a finding unless an authoritative Cleaning source permits it.

Reconciliation:

- Compare Pass A and Pass B conclusions. If they diverge, report the exact divergence and do not state the bounded smoke conclusion as supported.
- If both passes reproduce the same trace shape, the maximum allowed positive conclusion is: `bounded_raw_to_cleaned_trace_supported`.
- Do not use "production-ready", "validated", "buyer-proof", "Judgment-ready", or "full E2E ready".

## Review Questions To Answer

1. Raw to cleaned: Can the reviewer link source-visible raw material to the cleaned handles without trusting the home model's prose?
2. Cleaned to raw: Can the reviewer start from Cleaning handles and find the raw packet/projection/consolidation/ECR material they cite?
3. ECR coupling: Does every Cleaning handle's ECR ref point to the same packet id as the handle and raw anchor?
4. Limitation handling: Are residuals and limitations preserved honestly, especially `retail_structure_not_preserved` and `variant_offer_absent` for Sephora and Ulta?
5. Reddit capture: Distinguish the old-Reddit search candidate HTTP 200 events from actual thread packet capture. Did the run actually capture r/b2bmarketing thread data beyond candidate intake?
6. Overclaim risk: Does any prompt, report, runner output, summary, or home-model claim overstate the smoke as live capture-to-Judgment E2E readiness, buyer proof, product proof, validation, or production acceptance?
7. Product efficacy boundary: Does the smoke support only evidence-plumbing efficacy, or does it support a stronger product conclusion? Stronger product conclusions should be rejected unless independently proven by accepted Orca proof gates.

## Known Observed Facts To Confirm Or Refute

These are home-model observations, not review conclusions. Confirm them from files before relying on them:

- `stitched/smoke_summary.json` reported counts: `retail_sources=3`, `reddit_sources=3`, `ecr_receipts=6`, `cleaning_handles=27`.
- Retail/PDP summary reported:
  - Sephora: 4 handles, `structure_preserved=false`, residual `cloakbrowser_snapshot_01:sephora:variant_offer_absent`.
  - Ulta: 5 handles, `structure_preserved=false`, residual `cloakbrowser_snapshot_01:ulta:variant_offer_absent`.
  - Amazon: 3 handles, `structure_preserved=true`.
- Reddit summary reported:
  - reddit:1: 2 comments, 3 handles, packet id `01KVK3RHA2B0HDDKFT3MJ7328G`.
  - reddit:2: 3 comments, 4 handles, packet id `01KVK3RMGG75NXWM9F2ZRCG1VY`.
  - reddit:3: 7 comments, 8 handles, packet id `01KVK3RQMNDBH7785V9B7GEQ1Z`.
- `reddit_batch/batch_summary.json` reported `url_count=3`, `capture_success_count=3`, and `consolidation_success_count=3`.
- The Reddit candidate-intake searches returning HTTP 200 are not the same thing as thread body capture. The body capture claim depends on `reddit_batch/*_packet`, consolidation outputs, raw files, and stitched handles.

## Limitation Analysis Required

Explain each limitation as cause, impact, and closure condition:

- Sephora and Ulta `variant_offer_absent`: determine whether the raw capture lacks visible offer/variant substrate, the projection failed to extract visible substrate, or the stitcher mishandled projection residuals. State which is evidenced and which remains unknown.
- Amazon structure preserved: verify it is not only a parser artifact; inspect projection row kinds and raw anchors.
- Reddit search HTTP 200: verify whether candidate intake captured only URL candidates and whether thread body capture later wrote SourceCapturePacket directories.
- Ignored `_test_runs`: state that ignored run outputs are smoke evidence, not promoted durable source truth.
- Web search used for retail target selection: verify whether search was only candidate-freezing input and not treated as source truth.
- Cleaning scope: verify Cleaning did not decide credibility, demand, salience, independence, actionability, or Judgment semantics.

## Strict Claim Boundary

Allowed positive conclusion values:

- `bounded_raw_to_cleaned_trace_supported`
- `bounded_raw_to_cleaned_trace_partially_supported`
- `bounded_raw_to_cleaned_trace_not_supported`
- `SOURCE_CONTEXT_INCOMPLETE`

Allowed product-efficacy interpretation:

- "evidence-plumbing efficacy for this bounded smoke" only.

Forbidden claims:

- validation
- approval
- buyer proof
- demand proof
- product readiness
- production acceptance
- full live capture-to-cleaning E2E readiness
- capture-to-Judgment E2E readiness
- Judgment quality
- patch authority
- mandatory remediation

## Output Contract

Write the full review report to:

`docs/review-outputs/adversarial-artifact-reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- a compact `review_summary` YAML block with:
  - `trace_conclusion`
  - `product_efficacy_claim_cap`
  - `r_b2bmarketing_data_captured`
  - `limitation_handling`
  - `overclaim_risk`
  - `finding_ids`
- independent trace notes for Pass A and Pass B
- raw-to-cleaned sample trace table with file paths, packet ids, row ids or handle ids, and anchor/hash evidence
- limitation analysis
- explicit answer to: "r/b2bmarketing returned HTTP 200, but was any data captured?"
- validation evidence inspected and validation not-run gaps
- review-use boundary: findings are decision input only, not approval, validation, mandatory remediation, readiness, or executor-ready patch authority until separately accepted or authorized

For each finding, use:

- finding id
- severity as `blocker`, `major`, or `minor` for prioritization only
- source file/path and stable anchor
- evidence
- impact
- minimum closure condition
- next authorized action

After writing the report, return only a compact summary plus:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/adversarial-artifact-reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_v0.md
  commission: adversarial evidence-trace review of Cleaning spine real-data smoke raw-to-cleaned efficacy
  target_run_root: orca-harness/_test_runs/cleaning_spine_real_data_smoke_20260621/
  authority: advisory adversarial evidence-trace review; patch authority NOT_CLAIMED
  decision_criteria: raw/projection/consolidation/ECR/Cleaning traceability, limitation honesty, Reddit data-capture distinction, overclaim control
  trace_conclusion: <one allowed conclusion value>
  product_efficacy_claim_cap: evidence-plumbing efficacy only
  r_b2bmarketing_data_captured: yes | no | uncertain
  finding_ids: []
  next_authorized_action: home model adjudicates findings; no patch or readiness claim follows automatically
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not patch authority
    - not buyer proof
    - not judgment quality
    - not full live E2E proof
```
