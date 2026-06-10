# Daimler v0.14 Fixture Entry Source Manifest Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Daimler v0.14 fixture-entry and source acquisition/manifest planning artifacts.
use_when:
  - Commissioning a non-contestant reviewer to adversarially review Daimler fixture-entry plumbing before source acquisition.
  - Checking whether the Daimler pre-retrieval source-manifest plan preserves zero-spoiler and v0.14 fixture-entry boundaries.
  - Producing a durable adversarial review report under the bound review-output path.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md: A77216FADDA09E0965386853CCA90E836B51D4060E7B17005903798225251892
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md: 7472397A750964BAE40C8CCCE4DB56086D50826971B0BF12BE8216D9D0D759D9
  docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md: E60B496101E154401EA9D6E0E5C2EC58701A7EF1E1FBEC4C01A9C5E392D0347F
  docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
downstream_consumers:
  - docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md
stale_if:
  - either target artifact changes before review.
  - source acquisition, source-byte capture, memorization probe, model run, scoring, ledger freeze, schema/runtime work, or fixture admission starts before review.
  - GPT-5.5, Claude Opus, or another later target contestant family is used as the reviewer.
```

## Prompt Authoring Receipt

```yaml
orca_start_preflight:
  agents_read: true
  overlay_read: true
  source_pack: custom_prompt_review_authority_plus_daimler_targets
  template_kind: review
  template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md
  output_mode: review-report
  prompt_path: docs/prompts/reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_prompt_v0.md
  required_report_path: docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md
  edit_permission: docs-write_for_prompt_only
  reviewer_edit_permission: read-only
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
    - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md
  dirty_state_checked: true
  dirty_state_allowance: target artifacts and related docs may be untracked or modified in the current worktree; reviewer must read this worktree in place and must not substitute another checkout.
  blocked_if_missing: target artifacts, AGENTS.md, overlay README, review lane binding, prompt output path, report output path, or required review skills.
```

## Paste-Ready Review Prompt

````markdown
# Daimler v0.14 Fixture Entry Source Manifest Adversarial Artifact Review

You are performing a read-only adversarial artifact review for Orca.

## Non-Contestant Safety Gate

Before reading any Daimler participant packet material, source-manifest detail, or target artifact body, confirm that this review is not being run on GPT-5.5, Claude Opus, or any other model family reserved for later blind contestant use on this Daimler case.

If you are GPT-5.5, Claude Opus, cannot determine whether you are a target contestant family, or cannot enforce this non-contestant boundary, stop immediately and return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Blocked before reading Daimler target materials because reviewer execution could contaminate a later target contestant family."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Rerun this review with a non-contestant reviewer before exposing Daimler packet or source-manifest details."
```

Do not recommend, rank, or select a runtime model. The gate above is a contamination boundary only.

## Workspace Preflight

Repository: `C:\Users\vmon7\Desktop\projects\orca`

Expected branch: `main`

Expected HEAD: `a2aebdd8e04c627c5102e79eb324b24b3de35226`

Read the existing worktree in place. Do not create, clone, request, or switch to a different worktree. The target artifacts may be untracked in this worktree; that is in scope. If the required files are missing or the repository cannot be accessed, return a blocked review result.

## Required Method Sequence

REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.

REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not APPLY it yet.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, blocked/ready status, validation claims, readiness claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

After task sources are loaded, declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. Only after that declaration, APPLY deep-thinking to frame boundary risks and APPLY adversarial artifact review to produce findings.

## Required Source Pack

Read these first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md`
4. `.agents/workflow-overlay/artifact-roles.md`
5. `.agents/workflow-overlay/prompt-orchestration.md`
6. `.agents/workflow-overlay/review-lanes.md`
7. `.agents/workflow-overlay/validation-gates.md`
8. `.agents/workflow-overlay/communication-style.md`
9. `.agents/workflow-overlay/template-registry.md`
10. `.agents/workflow-overlay/retrieval-metadata.md`

Review targets:

1. `docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md`
2. `docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md`

Case context sources:

1. `docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md`
2. `docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md`
3. `docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md`

Open adjacent v0.14 harness sources only if a finding depends on them or they materially change the review result. Good candidates if needed:

- `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_daimler_pressure_test_v0.md`
- `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
- `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
- `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
- `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`

Do not load Canoo/Walmart, Unity, Milwaukee, TR/Casetext, or `jb` rules, prompts, review outputs, or lifecycle mechanics as authority. Do not broaden into general case discovery.

## Input Hash Pins

Check these target/context hashes if feasible. If a hash differs, continue only if you can label the source as changed and the difference does not invalidate the commission; otherwise return blocked.

```yaml
input_hashes:
  fixture_entry_plan_v0: A77216FADDA09E0965386853CCA90E836B51D4060E7B17005903798225251892
  source_acquisition_and_manifest_plan_v0: 7472397A750964BAE40C8CCCE4DB56086D50826971B0BF12BE8216D9D0D759D9
  case_02_preflight_v0: E60B496101E154401EA9D6E0E5C2EC58701A7EF1E1FBEC4C01A9C5E392D0347F
  participant_packet_v0: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  safety_receipt_v0: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
```

## Review Commission

Adversarially review whether the Daimler fixture-entry and source acquisition/manifest planning artifacts are safe and sufficient as pre-retrieval plumbing for a v0.14 draft fixture pack.

The review must answer whether the artifacts:

- preserve the zero-spoiler boundary;
- keep participant-facing source labels separate from facilitator-only provenance;
- require source-byte hashes and retrieval timestamps without pretending they already exist;
- keep S1-S7 complete enough for the next authorized source acquisition step;
- block contestant exposure, memorization probes, model runs, scoring, ledger freeze, schema/runtime implementation, validation, product proof, fixture admission, and judgment-quality claims;
- avoid importing Canoo/Walmart, Unity, Milwaukee, TR/Casetext, or `jb` authority;
- avoid overclaiming Daimler's readiness beyond `accepted_for_draft_fixture_entry_only` / `not_admitted`;
- leave owner/source-retrieval decisions explicit rather than silently decided;
- give the next source-retrieval or evidence-registry actor enough contract to proceed without inventing intent.

## Out Of Scope

Do not retrieve sources.

Do not open public web pages, source URLs, search result pages, consulting case pages, post-cutoff company records, or later business press.

Do not run a memorization probe.

Do not expose Daimler packet text to GPT-5.5, Claude Opus, or any other target contestant family.

Do not run any contestant model.

Do not score, freeze a ledger, implement schema/runtime/code, create validation or product-proof claims, or claim judgment quality.

Do not write patches, patch queues, or executor-ready instructions.

## Finding Severity

Use `critical`, `major`, and `minor` only as finding-priority labels.

Critical: a flaw that could contaminate blind use, authorize forbidden work, claim readiness/validation/judgment quality, or make the next source-acquisition lane unsafe.

Major: a flaw that would likely cause source-retrieval, evidence-registry, packet-conversion, or review rework before v0.14 fixture entry can proceed.

Minor: a clarity, retrievability, or hygiene issue that does not change the safe next step.

These labels do not create approval, rejection, readiness, validation, or mandatory remediation authority.

## Required Report Output

Output mode: `review-report`.

Write the full review report to:

`docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md`

If the durable report cannot be written, do not use `report_path`. Return a failed blocked YAML summary with `review_location: chat_only_current_thread` and name the failed path in `summary` or `next_action`.

After a successful report write, return only this compact YAML summary in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

Do not add extra YAML keys.

## Full Report Shape

The durable report should include:

1. Commission, target, authority, and decision criteria.
2. Source-read ledger with status for each required source.
3. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Findings first, ordered by severity.
5. For each finding:
   - severity;
   - location;
   - issue;
   - evidence;
   - impact;
   - minimum_closure_condition;
   - next_authorized_action;
   - recommended correction or advisory remediation direction.
6. Non-findings that matter, especially where the artifacts correctly block overclaim or leakage.
7. Not-proven boundaries.
8. Review-use boundary.

If no issues are found, say so clearly and list residual risks or test gaps.

Do not include `patch_queue_entry`.

## Review-Use Boundary

This is a read-only adversarial artifact review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, fixture admission, blind-use readiness, judgment-quality proof, or executor-ready patch authority until separately accepted or authorized.
````

## Prompt Validation Notes

- Template kind: `review`.
- Template source: Orca-registered `adversarial-artifact-review`.
- Output mode: `review-report`.
- Downstream report path is bound.
- Prompt is read-only for the reviewer.
- Runtime model choice is intentionally unbound and not recommended.
- The prompt includes a non-contestant safety gate before reading Daimler packet or target material.

## Closeout

plumbing works only; not judgment quality.
