# Judgment Spine Pre-Sale Execution Evidence Tier Policy Patch Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the Judgment Spine pre-sale execution evidence-tier policy patch.
use_when:
  - Reviewing whether the pre-sale subscription/manual/chat default and API-optional routing patch is safe.
  - Checking that raw-API plumbing remains available without becoming default or mandatory.
  - Checking that advisory subscription/manual/chat use is not overpromoted into gate-clearing evidence.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
branch_or_commit: main @ 392f7935c029
downstream_review_output_path: docs/review-outputs/adversarial-artifact-reviews/judgment_spine_pre_sale_execution_evidence_tier_policy_patch_adversarial_artifact_review_v0.md
```

## Paste-Ready Review Commission

You are reviewing a docs-only policy patch in the Orca repository.

Workspace:

```text
C:\Users\vmon7\Desktop\projects\orca
```

Expected branch and HEAD:

```yaml
branch: main
head: 392f7935c029e96ae0f1342f37d37026ba66268b
```

Dirty-state allowance:

```yaml
dirty_state_allowed: yes
expected_dirty_or_untracked:
  - AGENTS.md may be modified
  - .agents/workflow-overlay/README.md may be modified
  - .agents/workflow-overlay/source-of-truth.md may be modified
  - .agents/workflow-overlay/validation-gates.md may be modified
  - .agents/workflow-overlay/prompt-orchestration.md may be modified
  - .agents/workflow-overlay/review-lanes.md may be modified
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md is untracked
  - docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md is untracked
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md is untracked
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md is untracked
review_boundary: >
  This review may assess the exact hash-pinned files below in the active
  workspace despite dirty/untracked status. Do not infer repo-wide cleanliness,
  source-of-truth promotion, validation, readiness, or acceptance from dirty
  state. If a required hash does not match, stop as hash_mismatch.
```

## Objective

Perform a bounded read-only adversarial artifact review of the pre-sale
execution evidence-tier policy patch.

The patch intent is:

- subscription/manual/chat execution is the default pre-sale path when adequate
  for advisory learning, demos, scouting, buyer conversation, or owner readback;
- raw API and harness execution remain in-bounds as optional gate-bearing
  plumbing when explicitly accepted for stricter provenance needs;
- no-case smoke tests remain optional plumbing and permanently
  non-gate-clearing;
- subscription/manual/chat output is not automatically gate-clearing;
- no runtime code, provider calls, model calls, scoring, validation, fixture
  admission, ledger freeze, product proof, or judgment-quality claim is made.

## Required Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD the following methods. Do not APPLY them yet:
   - `C:\Users\vmon7\.codex\skills\workflow-deep-thinking\SKILL.md`
   - `C:\Users\vmon7\.codex\skills\workflow-adversarial-artifact-review\SKILL.md`
3. Read the required authority sources and review targets below.
4. Verify every listed SHA-256 hash exactly. If any hash mismatches, stop with
   `status: blocked`, name the mismatched file, and do not review substitute
   content.
5. Declare `SOURCE_CONTEXT_READY` only after the required files are loaded and
   all hashes match.
6. APPLY `workflow-deep-thinking` to frame failure modes and review criteria.
7. APPLY `workflow-adversarial-artifact-review` to produce the review report.

If either workflow skill is missing or cannot be applied after source context
is ready, return only a blocked/advisory result. Do not emit strict review
claims.

## Required Sources And Hashes

Authority and overlay sources:

```yaml
AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
.agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
.agents/workflow-overlay/source-of-truth.md: 57C9A6A457A80E0BB66771B3F1B67BD7994CEB9763F0D5D08076061A9921327A
.agents/workflow-overlay/validation-gates.md: 2640638B8B8420B11951437A190B5578A8DACCB7B84583FC17A6808809628DE9
.agents/workflow-overlay/prompt-orchestration.md: 5C6CFC60EFA408A492BF776259745AC25CB630D7B2339365243E68190728B5EA
.agents/workflow-overlay/review-lanes.md: 2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199
.agents/workflow-overlay/retrieval-metadata.md: 8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F
```

Review targets:

```yaml
docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: 39A65D04D71A348C7E2C3075512F1BED335F922270ED1E0497A7F98FA48745ED
docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 0EA6D4C180CD36AF6611E42BFEAB92A576C9D0311EE98417CBB5CFFC33776BF5
docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md: 96C498C6583CF10BE9AA0F7A3DF4043CDB1B389A96A5DB723A21E69C11A536F8
```

Context source for source-access analogy only:

```yaml
docs/product/data_capture_source_access_method_plan_v0.md: 1C20DA685D57606F0AADFCD0829EBC7747623F3640E9D35F5DCA0616E584EABB
```

## Review Scope

Review only the policy patch and downstream wording in the listed target files.
This is not a full Judgment Harness review, product review, code review,
runtime review, or model-family recommendation.

Focus on these adversarial surfaces:

1. **Correct tier separation**
   - Advisory subscription/manual/chat use is allowed for pre-sale learning,
     demos, scouting, buyer conversation, or owner readback.
   - Advisory use is not converted into clean memorization-probe pass,
     blind-use authorization, fixture validation/admission, scoring readiness,
     product proof, or judgment-quality evidence.

2. **No API-default regression**
   - Raw API and harness execution remain in-bounds.
   - The patch does not make API mandatory for ordinary pre-sale work.
   - The patch does not imply every future probe, demo, scout, or owner
     readback must use API.

3. **No API-ban overcorrection**
   - The patch does not prohibit raw API.
   - The patch does not roll back, invalidate, or deprecate the raw-API runner
     and no-case smoke-test plumbing.
   - Gate-bearing execution evidence remains available when explicitly
     authorized and necessary.

4. **No-case smoke boundary**
   - No-case smoke remains optional plumbing only.
   - No-case smoke remains permanently non-gate-clearing.
   - The concrete OpenAI smoke authorization remains bounded to its exact
     one-shot scope and does not become a default operating instruction.

5. **Gate-bearing evidence integrity**
   - The contestant no-tools execution contract still requires structural
     no-tools isolation and provenance before gate consequences are trusted.
   - The patch does not weaken hidden-context, tool-isolation, endpoint,
     prompt-hash, response-hash, or provenance requirements.

6. **Doctrine propagation and retrieval hygiene**
   - The new decision record has an adequate `direction_change_propagation`
     receipt for a validation-philosophy/product-routing adjustment.
   - Downstream touched surfaces are plausible and sufficient for this narrow
     patch.
   - Retrieval metadata helps routing and does not create authority,
     validation, readiness, acceptance, lifecycle completion, deployment,
     resolver, or edit-permission claims.

7. **Claim discipline**
   - No file claims live provider calls, model calls, scoring, validation,
     fixture admission, product readiness, or judgment quality.
   - The closeout boundary remains: plumbing works only; not judgment quality.

## Out Of Scope

Do not:

- patch files;
- execute API calls, model calls, probes, smoke tests, blind judgments, scoring,
  validation, fixture admission, or ledger freeze;
- review runtime code except to notice if a docs claim incorrectly describes
  runtime behavior;
- recommend a runtime model for review or execution;
- broaden into a full repo hygiene review;
- create a patch queue or executor-ready remediation plan.

## Severity Contract

Use these finding severities:

- `critical`: patch creates a false gate-clearing path, live-call/model-run
  authorization, participant exposure authorization, fixture validation or
  admission claim, product-proof claim, or judgment-quality claim.
- `major`: patch materially misroutes future work by making API default,
  banning API, weakening gate-bearing evidence, or making advisory
  subscription/manual/chat output appear gate-clearing.
- `minor`: retrieval, wording, traceability, stale-field, or local consistency
  issue that should be fixed but does not materially misroute the next decision.
- `optional`: non-required hardening only.

For every actionable finding, include:

```yaml
minimum_closure_condition:
next_authorized_action:
```

Closure conditions must describe the required end state, not implementation
steps. Do not include `patch_queue_entry`.

## Required Output Mode

Output mode: `review-report`.

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/judgment_spine_pre_sale_execution_evidence_tier_policy_patch_adversarial_artifact_review_v0.md
```

Before writing, confirm the output path does not already exist. If it exists,
stop as `output_collision` and do not overwrite it.

After a successful write, fresh-read the report and compute its SHA-256. Return
a short human summary plus this courier YAML:

```yaml
review_summary:
  status:
  report_path:
  report_hash:
  reviewed_targets:
    - path:
      hash:
  recommendation:
  summary:
  findings_count:
  blocking_findings:
  advisory_findings:
  next_action:
  non_claims:
    - no file patching by reviewer
    - no live provider call
    - no model call
    - no probe or smoke test run
    - no participant packet exposure
    - no scoring
    - no ledger freeze
    - no schema/runtime implementation
    - no validation
    - no fixture admission
    - no product proof
    - no judgment-quality claim
```

If blocked before writing, return a human-readable blocker and YAML with
`status: blocked`, `recommendation: blocked`, no `report_path`, and the exact
blocking condition.

Review findings are decision input only; they are not approval, validation,
mandatory remediation, or executor-ready patch authority until separately
accepted or authorized.

Required closeout line: plumbing works only; not judgment quality.
