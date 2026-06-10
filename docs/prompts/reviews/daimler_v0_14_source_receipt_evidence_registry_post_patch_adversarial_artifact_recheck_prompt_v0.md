# Daimler v0.14 Source Receipt Evidence Registry Post-Patch Adversarial Artifact Recheck Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Bounded post-patch adversarial artifact recheck for Daimler v0.14 source receipt and evidence registry plumbing.
use_when:
  - Rechecking whether the patched Daimler evidence registry closes the prior source receipt/evidence registry review findings.
  - Checking only patch-scope blocker or major regressions before participant packet conversion.
authority_boundary: retrieval_only
input_hashes:
  evidence_registry_draft_v0.md: 2E9FC02E7D19AA21DC9C66E9DF740D53A6798365D70EB76A2D3F213F2DD2FBA5
  source_acquisition_receipt_v0.md: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
  source_acquisition_and_manifest_plan_v0.md: D85D69F16308138AFB639DA3BD2229A43A13EE96653D9CF8B62E69122B8C5BDD
  fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  prior_adversarial_review_report_v0.md: 55F1AA090240EF31C37040A3B64504E09C99635D7546639E9B6E3BACFD54757B
  prior_adversarial_review_prompt_v0.md: 866CEB8083A3A663B2B08882B78F8C9DFD12DEA10C6E2AD2F26E9E843D78118D
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_source_receipt_evidence_registry_adversarial_artifact_review_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/evidence_registry_draft_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_receipt_v0.md
stale_if:
  - Any input hash above does not match current filesystem state.
  - The review target is staged, committed, or patched again before this recheck runs.
  - The commission expands beyond post-patch closure/regression checking for MAJ-01 and MIN-01 through MIN-04.
```

You are performing a read-only adversarial artifact recheck for Orca.

## Commission

Determine whether the patched Daimler evidence registry closes the prior adversarial review findings `MAJ-01` and `MIN-01` through `MIN-04`, without reopening the full source-acquisition review or authorizing any downstream fixture work.

This is a bounded patch recheck. First verify whether the patch closes each prior finding. Then scan only the touched patch scope for patch-caused or newly visible blocker/major regressions. Exclude unrelated structural review, new minor/nit findings, source acquisition adequacy beyond the current source set, participant packet drafting, probe readiness, model readiness, scoring readiness, ledger freeze, and judgment-quality claims.

## Workspace And Preflight

Repository: `C:\Users\vmon7\Desktop\projects\orca`

Expected branch and revision at prompt authoring:

```yaml
branch: main
head_prefix: 4d1887c0e230
dirty_state_allowance:
  allowed:
    - untracked Daimler v0.14 fixture artifacts under docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/
    - untracked prior adversarial review report named in this prompt
  disallowed:
    - reviewing a substitute checkout
    - switching branches or creating worktrees
    - patching any target file
```

Run this start receipt before review work:

```yaml
orca_start_preflight:
  agents_read: yes_required
  overlay_read: yes_required
  source_pack: custom_bounded_post_patch_recheck
  edit_permission: read-only
  target_scope: Daimler v0.14 source receipt/evidence registry post-patch closure recheck
  dirty_state_checked: yes_required
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - required workflow skills
    - any pinned input file
    - required output path write access
```

If launched outside the pinned workspace, change directory to the pinned workspace if accessible. If the pinned workspace is not accessible, return a blocked result. Do not create, clone, request, or switch to a different worktree.

## Required Authority Reads

Read these before source analysis:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/template-registry.md`

Orca-specific authority must come from Orca overlay files and the target artifacts named here. Do not import `jb` policy, paths, lifecycle mechanics, validation habits, or handoffs.

## Required Method Sequence

REFERENCE-LOAD these methods before source loading. Do not APPLY them yet.

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

After the required task sources are loaded and hashes verified, declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. Only after that declaration, APPLY `workflow-deep-thinking` to frame closure and regression risks, then APPLY `workflow-adversarial-artifact-review` to produce the recheck report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, blocked/ready status, validation claims, readiness claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Task Sources

Read and hash-verify these exact sources:

```yaml
review_target:
  path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/evidence_registry_draft_v0.md
  expected_sha256: 2E9FC02E7D19AA21DC9C66E9DF740D53A6798365D70EB76A2D3F213F2DD2FBA5
context_sources:
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_receipt_v0.md
    expected_sha256: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md
    expected_sha256: D85D69F16308138AFB639DA3BD2229A43A13EE96653D9CF8B62E69122B8C5BDD
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
    expected_sha256: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  - path: docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_source_receipt_evidence_registry_adversarial_artifact_review_v0.md
    expected_sha256: 55F1AA090240EF31C37040A3B64504E09C99635D7546639E9B6E3BACFD54757B
  - path: docs/prompts/reviews/daimler_v0_14_source_receipt_evidence_registry_adversarial_artifact_review_prompt_v0.md
    expected_sha256: 866CEB8083A3A663B2B08882B78F8C9DFD12DEA10C6E2AD2F26E9E843D78118D
```

If any hash mismatches, stop and return `SOURCE_CONTEXT_INCOMPLETE` with the mismatched path and observed hash. Do not continue the recheck on stale or substituted inputs.

## Prior Findings To Recheck

The prior review recommendation was `accept_with_friction`. It found no blockers, but identified one major finding that must be resolved before participant packet conversion and four minor findings.

Recheck only these:

- `MAJ-01`: EvidenceUnit `source` field alias-placeholder design plus unresolved packet-conversion source-manifest mapping.
- `MIN-01`: `DCSV-S3-ALT` captured in receipt but absent from evidence registry excluded/unresolved sources.
- `MIN-02`: `DCSV-E06` `pre_decision_basis` defers to safety receipt instead of stating explicit date-based reason.
- `MIN-03`: Extra EvidenceUnit fields are not explicitly noted as facilitator-only must-strip before schema validation.
- `MIN-04`: Evidence registry `input_hashes` uses alias key for the Canoo shape reference instead of repository-resolvable path.

## Closure Checks

For `MAJ-01`, verify all of the following:

- Facilitator-owned `EvidenceUnit.source` carries real source locators or local file paths for the current source set.
- The registry explicitly says participant packet conversion must not copy `EvidenceUnit.source`.
- The registry explicitly says participant-facing `source_manifest.source` values must be derived only from `participant_safe_label` and source-class labels.
- The patch does not leak URLs, titles, filenames, outlet names, byte sizes, hashes, retrieval timestamps, optional residue, or 403 details into any participant-facing artifact, and does not claim the registry itself is participant-facing.

For `MIN-01`, verify `DCSV-S3-ALT` appears in excluded or unresolved source material with status equivalent to optional alternate distribution not used.

For `MIN-02`, verify `DCSV-E06` now states an explicit date-based pre-decision basis tied to the 2019 annual-meeting agenda and the May 21, 2019 cutoff.

For `MIN-03`, verify the registry explicitly marks `bytes_available`, `leakage_check_status`, `participant_safe_label`, and `leakage_notes` as facilitator-only tracking fields outside the v0.14 EvidenceUnit schema and says they must be stripped before schema-validated or participant-facing use.

For `MIN-04`, verify the Canoo evidence-registry shape reference is keyed by the repository-resolvable path:

```text
docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md
```

## Regression Checks

Check only touched patch scope for blocker or major regressions:

- Did real locators in facilitator-only `EvidenceUnit.source` create a participant leakage route?
- Did the source mapping note accidentally authorize participant packet conversion, blind use, source retrieval, probe execution, model runs, scoring, ledger freeze, schema/runtime implementation, validation, fixture admission, readiness, or judgment-quality claims?
- Did the S3 alternate residue create ambiguity about the current S3 source of record?
- Did the schema must-strip note overclaim schema implementation or schema validation?
- Did the source-hash/timestamp gate wording overclaim historical archive proof, canonical source proof, fixture readiness, or accepted source finality?

Do not produce new minor findings unless a minor issue directly prevents closure of one of the five prior findings. Optional hardening may be named only as explicitly non-required.

## Output Mode

Output mode: `review-report`.

Required output path:

```text
docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_source_receipt_evidence_registry_post_patch_adversarial_recheck_v0.md
```

Write the full durable review report to that path. If the report cannot be written, return a failed blocked `review_summary` in chat with `review_location: chat_only_current_thread`; do not use `report_path`.

After a successful report write, return only:

- a short human summary; and
- a fenced YAML `review_summary` block with:
  - `status`
  - `report_path`
  - `report_hash`
  - `reviewed_target`
  - `reviewed_target_hash`
  - `prior_review_hash`
  - `recommendation`
  - `closed_findings`
  - `still_open_findings`
  - `patch_caused_regressions`
  - `next_authorized_action`
  - `non_claims`

## Forbidden Work And Non-Claims

Do not patch files. Do not retrieve external sources. Do not execute memorization probes. Do not run contestant models. Do not score. Do not freeze the ledger. Do not implement schema/runtime code. Do not validate fixture admission. Do not claim participant-packet readiness, blind-use readiness, product proof, or judgment quality.

Required review-use boundary: findings are decision input only; they are not approval, validation, mandatory remediation, executor-ready patch authority, fixture admission, or readiness.

Close with: `plumbing works only; not judgment quality.`
