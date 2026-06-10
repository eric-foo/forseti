# Daimler v0.14 Participant Packet Conversion Plan Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Daimler participant packet conversion plan before any participant packet draft is authored.
use_when:
  - Reviewing participant_packet_conversion_plan_v0.md for zero-spoiler source-manifest safety and v0.14 frontmatter fit.
  - Checking whether the conversion plan is safe to use as the basis for a later participant_packet_draft_v0.md authoring pass.
  - Preserving the boundary that review findings are decision input only, not fixture admission or blind-use readiness.
authority_boundary: retrieval_only
input_hashes:
  participant_packet_conversion_plan_v0.md: A9C230419DF8D952A810FD9EEBB1AC303481E3C8494CB778014BB14E0D0016C1
  fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  evidence_registry_draft_v0.md: 2E9FC02E7D19AA21DC9C66E9DF740D53A6798365D70EB76A2D3F213F2DD2FBA5
  source_acquisition_receipt_v0.md: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
  post_patch_adversarial_recheck_v0.md: 5E43E7E26BD37AA7270A019A60BD5F600ED53C75367611EA7F44B886AE605F34
  docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  pydantic_schema_reference.md: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  canoo_source_manifest_adapter_decision_reference.md: 39E92DB6C9D86C1BB18857069CF0507065C4460A15B3293359611875B3DB2E32
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_conversion_plan_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/evidence_registry_draft_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
stale_if:
  - Any input hash above does not match current filesystem state.
  - participant_packet_conversion_plan_v0.md changes before the review runs.
  - The review is run on a target contestant family for the Daimler blind run.
  - The review scope expands into drafting participant_packet_draft_v0.md, running a probe, scoring, validation, ledger freeze, fixture admission, or judgment-quality assessment.
```

You are performing a read-only adversarial artifact review for Orca.

## Commission

Review `participant_packet_conversion_plan_v0.md` for whether it is safe and complete enough to serve as the docs-only basis for a later Daimler `participant_packet_draft_v0.md` authoring pass.

Focus on:

- zero-spoiler participant-facing source-manifest safety;
- v0.14 frontmatter fit against the Pydantic schema reference;
- correct use of withheld placeholders for participant-facing `retrieval_timestamp` and `hash`;
- prevention of facilitator-only provenance leakage;
- preservation of the parent packet's pre-cutoff and no-outcome boundary;
- explicit blocking of readiness, validation, fixture admission, blind-use, model-run, scoring, ledger-freeze, and judgment-quality claims.

This is not a request to draft the participant packet.

## Non-Contestant Gate

The Daimler fixture plan names GPT-5.5 primary and Claude Opus backup as later target contestant families. This review exposes participant-packet conversion material. If this prompt is being run on GPT-5.5, Claude Opus, or another runtime intentionally selected as the target contestant family for this Daimler blind run, stop and return:

```yaml
review_summary:
  status: blocked
  recommendation: blocked_target_contestant_exposure_risk
  summary: "Review would expose Daimler participant-packet material to a target contestant family before memorization probe/pass and blind-use authorization."
  next_action: "Rerun this review on a non-contestant review lane."
```

Do not continue source loading after this gate fails.

## Workspace And Preflight

Repository: `C:\Users\vmon7\Desktop\projects\orca`

Expected branch and revision at prompt authoring:

```yaml
branch: main
head_prefix: 0a5e1d9ea04c
dirty_state_allowance:
  allowed:
    - untracked Daimler parent case artifacts under docs/research/judgment-spine/cases/daimler-carve-out/
    - untracked Daimler v0.14 fixture artifacts under docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/
    - untracked Daimler source/evidence post-patch adversarial recheck report named in this prompt
  disallowed:
    - reviewing a substitute checkout
    - switching branches or creating worktrees
    - patching any target file
    - creating participant_packet_draft_v0.md
```

Run this start receipt before review work:

```yaml
orca_start_preflight:
  agents_read: yes_required
  overlay_read: yes_required
  source_pack: custom_daimler_packet_conversion_plan_review
  edit_permission: read-only
  target_scope: Daimler v0.14 participant packet conversion plan adversarial artifact review
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
- `.agents/workflow-overlay/retrieval-metadata.md`

Orca-specific authority must come from Orca overlay files and the target artifacts named here. Do not import `jb` policy, paths, lifecycle mechanics, validation habits, handoffs, or prompt conventions.

## Required Method Sequence

REFERENCE-LOAD these methods before source loading. Do not APPLY them yet.

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

After the required task sources are loaded and hashes verified, declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. Only after that declaration, APPLY `workflow-deep-thinking` to frame the leakage, frontmatter, and downstream-conversion failure modes, then APPLY `workflow-adversarial-artifact-review` to produce the review report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, blocked/ready status, validation claims, readiness claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Task Sources

Read and hash-verify these exact sources:

```yaml
review_target:
  path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_conversion_plan_v0.md
  expected_sha256: A9C230419DF8D952A810FD9EEBB1AC303481E3C8494CB778014BB14E0D0016C1
context_sources:
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
    expected_sha256: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/evidence_registry_draft_v0.md
    expected_sha256: 2E9FC02E7D19AA21DC9C66E9DF740D53A6798365D70EB76A2D3F213F2DD2FBA5
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_receipt_v0.md
    expected_sha256: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
  - path: docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_source_receipt_evidence_registry_post_patch_adversarial_recheck_v0.md
    expected_sha256: 5E43E7E26BD37AA7270A019A60BD5F600ED53C75367611EA7F44B886AE605F34
  - path: docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
    expected_sha256: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  - path: docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
    expected_sha256: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  - path: docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
    expected_sha256: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  - path: docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_manifest_participant_safe_adapter_decision_v0.md
    expected_sha256: 39E92DB6C9D86C1BB18857069CF0507065C4460A15B3293359611875B3DB2E32
```

If any hash mismatches, stop and return `SOURCE_CONTEXT_INCOMPLETE` with the mismatched path and observed hash. Do not continue the review on stale or substituted inputs.

## Decision Criteria

Use `critical`, `major`, and `minor` as finding-priority labels only. They are not approval, rejection, readiness, validation, or mandatory-remediation authority.

Treat a finding as critical if the plan would cause participant-facing leakage, post-cutoff contamination, outcome leakage, source-identity leakage, or a false readiness/admission claim.

Treat a finding as major if the plan leaves a conversion actor likely to invent frontmatter intent, source-manifest values, placeholder policy, no-spoiler policy, or downstream gate status before packet drafting.

Treat a finding as minor if it creates ambiguity, stale-source risk, retrieval-metadata weakness, or local consistency risk that does not block use as a conversion-plan basis.

For actionable findings, include:

- `minimum_closure_condition`;
- `next_authorized_action`;
- advisory remediation direction, not a patch queue.

Do not include `patch_queue_entry`.

## Review Checks

Check at least these surfaces:

1. **Source-manifest safety:** Participant-facing `source_manifest.source` values must be source-class labels only; no raw locators, filenames, source titles, domains, outlet names, byte sizes, true source hashes, true retrieval timestamps, optional-residue notes, or 403 details.
2. **Placeholder discipline:** Participant-facing `retrieval_timestamp` and `hash` values must be `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL`, not real audit provenance.
3. **S1-S7 mapping completeness:** `DCSV-S1` through `DCSV-S7` must map exactly once in a way consistent with the evidence registry labels. `DCSV-S4A` and `DCSV-S4B` may share the S4 label only if the plan explains why.
4. **S3 alternate handling:** `DCSV-S3-ALT` must not leak or become participant-facing unless separately authorized; the plan must preserve DCSV-S3 as the current registry source.
5. **S7 independent-press handling:** S7 may be participant-facing only as the safe source-class label, without title, outlet cue, URL, original-wire residue, or valuation-pressure source identity leakage.
6. **Pydantic frontmatter fit:** Required v0.14 participant frontmatter fields must be present in the plan's conversion intent: `case_id`, `decision_question`, `decision_date_or_cutoff`, `role_frame`, `authority_constraints`, `capability_constraints`, `permitted_assumptions`, `forbidden_information_notice`, and `source_manifest`.
7. **Parent packet preservation:** The plan must preserve the existing clean pre-cutoff packet body and must not authorize adding new substantive facts from facilitator-only summaries unless already in the parent packet.
8. **No-spoiler boundary:** The plan must continue excluding final vote result, later implementation, later corporate actions, later outcomes, consulting narrative, source titles, source URLs, and result-quality labels.
9. **Non-claim discipline:** The plan must not claim participant-packet readiness, blind-use readiness, probe pass, model-run authorization, scoring readiness, validation, fixture admission, product proof, or judgment quality.
10. **Downstream boundary:** The plan may authorize a later docs-only packet draft after owner acceptance; it must not itself create the draft, run review, execute a probe, freeze a ledger, validate a fixture, or score anything.
11. **Retrieval metadata:** The retrieval header should help future agents open the right sources and should not create authority, validation proof, approval, readiness, lifecycle completion, deployment/install/resolver status, or edit permission.

## Output Mode

Output mode: `review-report`.

Required output path:

```text
docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_participant_packet_conversion_plan_adversarial_artifact_review_v0.md
```

Write the full durable review report to that path. If the report cannot be written, return a failed blocked `review_summary` in chat with `review_location: chat_only_current_thread`; do not use `report_path`.

After a successful report write, return a short human summary plus a fenced YAML `review_summary` block with:

- `status`
- `report_path`
- `report_hash`
- `reviewed_target`
- `reviewed_target_hash`
- `recommendation`
- `findings_count`
- `blocking_findings`
- `advisory_findings`
- `next_action`
- `non_claims`

## Recommendation Vocabulary

Use one of:

- `accept`
- `accept_with_friction`
- `patch_before_packet_draft`
- `blocked`

`accept` or `accept_with_friction` means the conversion plan may be used as decision input for a later separately authorized `participant_packet_draft_v0.md` authoring pass. It does not mean the packet draft exists, is accepted, is blind-use-ready, is probe-safe, is validated, or is fixture-admitted.

## Forbidden Work And Non-Claims

Do not patch files. Do not create `participant_packet_draft_v0.md`. Do not retrieve external sources. Do not execute memorization probes. Do not run contestant models. Do not score. Do not freeze the ledger. Do not implement schema/runtime code. Do not validate fixture admission. Do not claim participant-packet readiness, blind-use readiness, product proof, or judgment quality.

Required review-use boundary: findings are decision input only; they are not approval, validation, mandatory remediation, executor-ready patch authority, fixture admission, or readiness.

Close with: `plumbing works only; not judgment quality.`
