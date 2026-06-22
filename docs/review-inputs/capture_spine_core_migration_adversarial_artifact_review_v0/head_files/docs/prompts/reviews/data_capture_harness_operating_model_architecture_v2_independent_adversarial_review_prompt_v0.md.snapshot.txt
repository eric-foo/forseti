# Data Capture Harness Operating Model Architecture v2 Independent Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Independent read-only adversarial artifact review prompt for the proposed Data Capture Harness operating-model architecture v2, explicitly excluding the prior narrow self-review as evidence.
use_when:
  - Commissioning an independent adversarial review of `docs/product/data_capture_harness_operating_model_architecture_v2.md`.
  - Checking whether v2 should be accepted, patched, rejected, or sent back to architecture before owner acceptance.
  - Avoiding tester-examiner bias from the local narrow review of the same v2 artifact.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md
stale_if:
  - `docs/product/data_capture_harness_operating_model_architecture_v2.md` changes.
  - The Data Capture obligation baseline or obligation contract changes.
  - Owner accepts, rejects, patches, or supersedes v2.
  - A later independent adversarial review prompt supersedes this one.
```

## Paste-Ready Prompt

You are performing an **independent read-only adversarial artifact review** for Orca.

This is not a patch lane, not an acceptance lane, not a validation lane, and not a self-review. Your job is to attack the proposed Data Capture Harness operating-model architecture v2 hard enough that the owner can decide whether to accept it, patch it, reject it, or reopen architecture.

## Independence Gate

Before reading the target artifact, answer this gate:

```yaml
reviewer_independence_preflight:
  did_you_author_v2: yes | no | unknown
  did_you_author_the_v2_narrow_review: yes | no | unknown
  are_you_in_the_same_local_thread_that_authored_v2_or_the_narrow_review: yes | no | unknown
  have_you_read_the_v2_narrow_self_review_before_this_prompt: yes | no | unknown
  independence_result: INDEPENDENT | BLOCKED_REVIEWER_NOT_INDEPENDENT | CONTAMINATED_BUT_DISCLOSED
```

Rules:

- If you authored `docs/product/data_capture_harness_operating_model_architecture_v2.md`, return `BLOCKED_REVIEWER_NOT_INDEPENDENT`.
- If you authored `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md`, return `BLOCKED_REVIEWER_NOT_INDEPENDENT`.
- If you are running in the same local thread/session that authored v2 or the narrow self-review, return `BLOCKED_REVIEWER_NOT_INDEPENDENT`.
- If you have already read the narrow self-review but did not author it, disclose `CONTAMINATED_BUT_DISCLOSED`, do not use it as evidence, and proceed only if you can ground every finding in the allowed sources below.
- Do not read the narrow self-review during this run. Treat it as excluded contaminated evidence.

Excluded contaminated evidence:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md
```

Do not cite it, summarize it, use its recommendation, or use its non-findings.

## Workspace And Preflight

Worktree:

```text
C:\Users\vmon7\Desktop\projects\orca
```

Expected branch and revision:

```text
branch: main
HEAD: b7627d3
```

Output mode:

```text
review-report
```

Required output path:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
```

Edit permission:

```text
read-only review; write only the required review report path above
```

Dirty-state allowance:

- Modified overlay files and untracked product/prompt/review artifacts are allowed for advisory review.
- Dirty or untracked source state does not support validation, readiness, source-of-truth promotion, buyer proof, implementation authority, or owner acceptance claims.
- If any target hash below mismatches, report `BLOCKED_SOURCE_HASH_MISMATCH` unless the current owner instruction explicitly authorizes reviewing the changed artifact.

Target hashes:

| Source | SHA256 |
| --- | --- |
| `docs/product/data_capture_harness_operating_model_architecture_v2.md` | `4DE2F89A7B6B48192F9F734516BA3723D20BBB0550EF80BEBB23A6467EBEBB46` |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md` | `A7E0E9FA7E5DED92C3A37914E6871AC251AECF8D8ABF8B2066614755ABFF775E` |
| `docs/product/data_capture_harness_operating_model_architecture_v0.md` | `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2` |
| `docs/product/data_capture_harness_operating_model_architecture_v1.md` | `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF` |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | `51D74EF534117744C5B4506393D0BA43927E636B4DA821E9A7BDE35A33728387` |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF` |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | `0FCC5DD4048EB3B03B96F644B3EF545D82C6F5EEC212301B4C0F28E34F04B166` |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | `1C3370C714BEF951FB3B424BC651251C63CE48AA88E680A4D1CB6CBD77775D94` |

If you cannot access the repo/worktree files, return `BLOCKED_REPO_ACCESS_UNAVAILABLE`. Do not review from summaries, chat memory, or this prompt alone.

## Required Method Sequence

REFERENCE-LOAD these method instructions first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Before `SOURCE_CONTEXT_READY`, you may prepare only neutral source-reading lenses. Do not produce findings, verdicts, rankings, recommendations, or architecture conclusions before source readiness.

Then SOURCE-LOAD the required Orca sources below.

After declaring `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the boundary problem, likely failure modes, and decision criteria.

Then APPLY `workflow-adversarial-artifact-review` to produce the findings-first review report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, readiness claims, validation claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Sources

Authority and review-lane sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`

Target and controlling product-method sources:

- `docs/product/data_capture_harness_operating_model_architecture_v2.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md`
- `docs/product/data_capture_obligation_baseline_decision_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`

Targeted comparison sources:

- `docs/product/data_capture_harness_operating_model_architecture_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v1.md`

Use targeted reads for v0 and v1 unless a finding requires full-file expansion. Search keys:

- `second operator`
- `reviewer`
- `approve`
- `refuse`
- `CPOE`
- `locked now`
- `control surface`
- `Next Authorized Step`
- `Bloat-Cut Queue`
- `Non-Claims`

Excluded by default:

- `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md`
- broad `docs/review-outputs/`
- broad `docs/prompts/`
- broad `docs/product/`
- `docs/_inbox/`
- method-validation replays
- proof-run packets
- research corpus
- implementation/runtime folders

Expand only if a missing source could materially change a finding. If expansion would exceed a bounded review source pack, report `SOURCE_CONTEXT_INCOMPLETE` with the exact missing source and why it matters.

## Review Target

Primary target:

```text
docs/product/data_capture_harness_operating_model_architecture_v2.md
```

Review purpose:

```text
Determine whether v2 is actually safe to accept as the Data Capture Harness operating-model architecture for later bounded pressure-test commissioning planning, or whether it should be patched, rejected, or sent back to architecture before owner acceptance.
```

The v0/v1 review report is allowed as source evidence for the prior findings and criteria. It is not binding authority. Do not assume v2 closed those findings merely because v2 says it did.

## Adversarial Review Questions

Attack v2 against these questions:

1. Does v2 truly eliminate hidden reviewer approval/refusal authority, or does `capture_closure_blocker` recreate pass/fail authority under a softer name?
2. Does v2 preserve enough counterparty pressure to catch silent omission, per-slice flattening, raw-observable loss, agent-assistance creep, hidden mode changes, and forbidden Capture outputs?
3. Did v2 cut v1's operating-model weight appropriately, or did it become too thin to pressure-test?
4. Does v2 distinguish accepted baseline obligations from pressure-test candidate controls without implying validation, hardening, source-of-truth promotion, readiness, or owner acceptance?
5. Does v2 keep Capture separate from ECR, Cleaning, Judgment, source maps, runtime/source systems, proof execution, operator scoring, and implementation?
6. Does v2 preserve source-family satellite discipline and the Source-Family Promotion Rule?
7. Does v2 preserve buyer-trustable capture output without turning the harness into review theater, source theater, or defensive audit armor?
8. Does v2's next step authorize only bounded planning, or does it silently authorize pressure-test execution, operator-roster execution, templates, forms, implementation, or runtime work?
9. Did v2 overfit to the prior AR-01/AR-02/AR-03 findings and miss a new architecture failure mode introduced by the hybridization?
10. Is v2 better than v0 and v1 for owner acceptance, or should the owner prefer v0, v1-with-patch, another hybrid, or a reopened architecture lane?

## Required Finding Severity

Use these priority labels only:

- `critical`: owner acceptance would likely break a controlling Orca boundary or create a false authorization/validation/readiness claim.
- `major`: owner acceptance would likely create material architecture risk, hidden role authority, downstream leakage, or pressure-test distortion.
- `minor`: wording, routing, or friction issue that should be patched but does not block owner acceptance if explicitly carried.

These labels are finding priority only. They do not create approval, rejection, validation, readiness, or mandatory remediation authority.

## Recommendation Vocabulary

Use exactly one:

- `accept_v2_as_proposed_architecture`
- `accept_v2_with_watch_items`
- `patch_v2_before_acceptance`
- `reject_v2_prefer_v0`
- `reject_v2_prefer_v1_with_patch`
- `reject_v2_reopen_architecture`
- `blocked_reviewer_not_independent`
- `blocked_source_context`

Do not use a generic `pass` or `fail`.

## Output Report Requirements

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
```

The report must include:

- retrieval header;
- `review_summary` YAML at the top;
- reviewer independence preflight result;
- source readiness declaration;
- source-read ledger with dirty/untracked notes;
- review boundary and excluded scope;
- decision criteria;
- findings first, ordered by severity;
- non-findings that matter;
- comparison to v0 and v1 where decision-relevant;
- not-proven boundaries;
- final recommendation;
- review-use boundary.

For each finding include:

- finding id;
- severity;
- phase: `correctness` or `friction`;
- target location or stable search key;
- issue;
- source evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- advisory remediation direction, not a patch queue.

Do not emit `patch_queue_entry`. This is read-only review.

## Chat Closeout

After successfully writing the durable report, return only a compact human sentence plus this courier YAML:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
  recommendation: <one recommendation from the allowed vocabulary>
  summary: "<one sentence>"
  findings_count: <number>
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated:
    - AR-01: closed | not_closed | partially_closed | not_reviewed
    - AR-02: closed | not_closed | partially_closed | not_reviewed
    - AR-03: closed | not_closed | partially_closed | not_reviewed
  next_action: "<one concrete next step>"
```

If report writing fails after `review-report` is selected, do not use `report_path`. Return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve report write failure, then rerun the review-report prompt."
```

## Hard Boundaries

Do not:

- patch v2;
- patch v0 or v1;
- patch the obligation contract;
- read or rely on the v2 narrow self-review;
- accept or reject the architecture on behalf of the owner;
- design ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- design operator rosters, pressure-test cases, templates, forms, or execution plans;
- claim validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness.

Review findings are decision input only. Owner acceptance, patch authorization, pressure-test commissioning, and any implementation/runtime work require separate explicit authorization.
