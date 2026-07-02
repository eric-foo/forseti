# IG Behavioral Residual Burn-Down Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial review prompt for PR #474's Instagram behavioral residual
  burn-down workflow docs, with special attention to source-backed completeness
  and Silver lineage claim discipline.
use_when:
  - Commissioning independent review of PR #474 before merge.
  - Checking whether the burn-down receipt over-trusts IG behavioral completeness or product-mention record membership.
  - Checking whether remaining residuals and non-goals stayed visible after the missing-input pass.
authority_boundary: retrieval_only
review_targets:
  - docs/workflows/ig_behavioral_residual_burndown_priority_v0.md
  - docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md
review_target_sha256:
  docs/workflows/ig_behavioral_residual_burndown_priority_v0.md: 152A3F8C279DB0BF0AB3513F62707DB79217A93B995DE0C0F4821C3158DB9B55
  docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md: B4E8C2B24BCEDDFEA129622FF64C1BDD94586280898A482C3C9B20FE19B13E0C
branch_or_commit: codex/ig-behavioral-residual-burndown @ 4602b7a5917d9a6ae67e5bf9cfa70403763d4bfe
intended_report_path: docs/review-outputs/adversarial-artifact-reviews/ig_behavioral_residual_burndown_adversarial_review_v0.md
stale_if:
  - Either review target hash differs from the hash above.
  - PR #474 changes in a way that modifies either review target.
  - A later F-lake inventory supersedes the receipt's final behavioral read.
  - IG behavioral lake/projection, Silver lineage, deep-capture, or operator extraction semantics change materially.
```

## Orca Prompt Preflight

- Output mode: `review-report`; write only `docs/review-outputs/adversarial-artifact-reviews/ig_behavioral_residual_burndown_adversarial_review_v0.md`.
- Template kind: `adversarial-artifact-review`; model-neutral prompt posture, not runtime model routing.
- Edit permission / targets / branch: read-only review of the two workflow target docs on branch `codex/ig-behavioral-residual-burndown`; no patches, no capture, no extraction, no PR edits.
- Reviews: findings-first adversarial artifact review; severity labels are `critical | major | minor` for finding priority only.
- Doctrine change: none authorized. If the review finds a doctrine change is needed, report it as a finding; do not patch.
- Destinations: this prompt is the input prompt; the durable report path is named above.
- Dirty-state allowance: target docs must match the hashes above. A prompt-only later commit or this prompt file may exist, but target hash mismatch blocks strict review claims.
- Thread target continuity: same IG behavioral residual workstream; review target is PR #474 documentation only, not a new capture or implementation lane.

## Commission

Review PR #474's IG behavioral residual burn-down docs before merge. The review must decide whether the docs accurately record what was done and what remains, without converting a successful run into a broader safety, completeness, validation, or readiness claim.

Plain success signal: a future reader can tell exactly what IG residuals were burned down, which claims depend on the live F-lake, which remaining gaps still block clean behavior, and which work was deliberately not done.

Treat that signal as an axis to attack, not as a pass bar.

## Required Source Loading

If you have repo/filesystem access, open the prompt from the repo and re-read every named load-bearing source before making strict or actionable claims. If you do not have repo/filesystem access, stop and request a pasted source capsule; do not review from memory.

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read these overlay authority files: `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/retrieval-metadata.md`, and `.agents/workflow-overlay/communication-style.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not APPLY it yet.
5. SOURCE-LOAD the two review target docs and verify their hashes against the retrieval header.
6. SOURCE-LOAD this bounded comparison pack:
   - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
   - `orca-harness/runners/run_source_capture_ig_reels_deep_capture.py`
   - `orca-harness/runners/run_ig_reels_operator_product_extract.py`
   - `orca-harness/source_capture/ig_reels_behavioral_lake.py`
   - `orca-harness/source_capture/ig_reels_behavioral_projection.py`
   - `orca-harness/data_lake/silver_lineage.py`
   - `docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md`
7. If `F:\orca-data-lake` is available, perform read-only verification of the receipt's final behavioral inventory and product-mention lineage claims using repo code. Do not run capture, extraction, imports, live network access, or media preservation. If `F:\orca-data-lake` is unavailable, declare `SOURCE_CONTEXT_INCOMPLETE` for lake verification and review only whether the docs make that dependency visible.
8. Declare `SOURCE_CONTEXT_READY` only after the target docs, comparison pack, and any available lake verification have been read. If a load-bearing source is missing, declare `SOURCE_CONTEXT_INCOMPLETE` and return a blocked or advisory-only report instead of strict findings.
9. After source readiness, APPLY `workflow-deep-thinking` to frame the failure modes, then APPLY `workflow-adversarial-artifact-review` to produce findings.

## Review Axes To Attack

Attack at least these failure modes:

1. The receipt overclaims behavioral completeness from record-set membership instead of source-backed Silver lineage, especially for `silver__cleaning__product_mentions` records and the `DaLBRQiMJhQ` default-pending explanation.
2. The docs state final counts, before/after counts, or residual prefixes without enough visible evidence, or fail to mark them stale when a later F-lake read would supersede them.
3. The operator extraction section claims conservative extraction, quote validation, or `rejected_count=0` without enough retained evidence for a reviewer to distinguish validated source-backed imports from temporary operator output.
4. Remaining non-complete items are framed too softly, hidden under aggregate success, or fail to distinguish grid/ranking absence, stale failed sources, no-speech/no-audio records, and render-unavailable sources.
5. The priority doc's old fresh-read counts could mislead a future agent despite the `superseded_by` pointer and short-answer update.
6. The run accidentally expands scope into shared IG/YT capture core, scheduler, durable media preservation, historical lake rewrite, gold/Judgment behavior, or full IG lane readiness.
7. The receipt treats a green parser/import result as validation, readiness, product proof, source promotion, or proof that all public IG Reels yield comments/audio/transcripts.
8. The docs understate live-source risk: public IG pages, transient media handles, ASR/no-speech posture, and missing local `F:\orca-data-lake` access.
9. The PR merge posture is overstated while `orca-harness-tests` or any later CI check is pending, failed, or not freshly checked.
10. Retrieval metadata is too weak to guide the next agent to the right files, stale conditions, and non-goals without broad searching.

## Output Contract

Write a durable report at:

`docs/review-outputs/adversarial-artifact-reviews/ig_behavioral_residual_burndown_adversarial_review_v0.md`

The report must include:

- retrieval header;
- target paths, branch/commit, and target hashes checked against the hashes above;
- `reviewed_by` and `authored_by`, using `unrecorded` only when the operator/tooling did not supply the value; do not fabricate either field;
- source-read ledger for load-bearing sources, including whether `F:\orca-data-lake` was available;
- compact `review_summary` YAML before detailed findings;
- findings first, ordered by `critical`, `major`, then `minor`;
- for every actionable finding: location, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, and advisory remediation direction;
- explicit non-findings only where they rule out plausible material failures;
- residual risk and review-use boundary.

Use this chat return shape only after the durable report is written:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/ig_behavioral_residual_burndown_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: unrecorded
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

If the durable report cannot be written, do not use `report_path`. Return a failed blocked `review_summary` with `review_location: chat_only_current_thread`, name the failed path, and explain the write failure.

Do not emit `patch_queue_entry`. Do not edit source files. Do not run live capture, product extraction, scheduler work, historical rewrite, media preservation, gold/Judgment work, or PR mutation. Do not claim approval, validation, readiness, implementation authorization, mandatory remediation, or runtime model recommendation.

After the review recommendation, the adjudicator should run the normal next-moves pass from `.agents/workflow-overlay/communication-style.md`: batch admin/lifecycle follow-ups separately from the few material next moves that require judgment.
