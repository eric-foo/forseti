# No-Case Smoke Test Execution Artifacts Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the completed no-case smoke-test receipt, provenance, input, stdout, and stderr artifacts.
use_when:
  - Reviewing whether the completed no-case smoke-test artifacts are internally consistent and safe to retain as plumbing evidence.
  - Checking that the smoke receipt and provenance support only raw API execution plumbing, not real-case or judgment-quality claims.
  - Verifying that no secret value, real-case identifier, participant packet material, or gate-clearing overclaim leaked into smoke outputs.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml
  - docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_provenance_v0.yaml
  - docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
input_hashes:
  AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
  .agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
  .agents/workflow-overlay/source-of-truth.md: 57C9A6A457A80E0BB66771B3F1B67BD7994CEB9763F0D5D08076061A9921327A
  .agents/workflow-overlay/source-loading.md: 2FD6D8379FE6BF4542CF89BA9E15D6E4720129EE2273AFFD0295E46ACF401376
  .agents/workflow-overlay/prompt-orchestration.md: 5C6CFC60EFA408A492BF776259745AC25CB630D7B2339365243E68190728B5EA
  .agents/workflow-overlay/review-lanes.md: 2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199
  .agents/workflow-overlay/communication-style.md: B357B5B1E45200E3E05641B58F7E96108E173122DB702A687A494DCE941A8328
  .agents/workflow-overlay/artifact-folders.md: ADD8158798A1A300F81863A45004969CD8AF0EEC5D8A949D78FE46AEA79DD39B
  .agents/workflow-overlay/retrieval-metadata.md: 8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F
  docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md: 377D834A70F4B38ACD4A419290394DFD1B5C7A2F1957146DEBEE5B29867DB52B
  docs/prompts/handoffs/no_case_smoke_test_openai_gpt_5_4_mini_one_shot_operator_prompt_v0.md: DB0FFEF70AC3C7EB9A5E6B6E66936D9B09435B787070626286895B30E616498B
  docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_openai_gpt_5_4_mini_adversarial_artifact_review_v0.md: F883F0EB19B87F4369CE1704BA39D6D727AC27BABC9693ECC7B4042FA8715E7B
  docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 7A17255422C546858C54807161A265074FC0A5BD6739AFDE5592A51D94A8B26D
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: F46AA6A4003E200C41796826277A6D8074ED84F26E6B6A5DD9E15584BE5EB0F5
  orca-harness/runners/run_memorization_probe_raw_api.py: CD83FDE1960CA503AD0EE39188CB49EB4676426115A54A7A38A888AA2A99A021
  docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_probe_input_v0.yaml: A9DEA6EE2C249A6BB9F59F9DA8638F817648BB262D8304CE2746CF9D18B157F6
  docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml: DB2A90D8FF93CD58D6409AD0CD72AA44F69FF162050B656D4B297A88B48C7B61
  docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_provenance_v0.yaml: 8CA53EB85003ACBD75965C2A445AE083143A1E03FCE2FE4D3D6294A045273660
  docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_stdout_v0.txt: FC76EBA180D5C472FC850B22A75DDCCA00E03D4D3A2BB67FC58E0DD3E6655703
  docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_stderr_v0.txt: E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
branch_or_commit: main @ b9adaa26859e599dad17f052049b9065824d7165
stale_if:
  - Any input hash changes.
  - The target review report path already exists.
  - The smoke run is retried or any smoke artifact is overwritten.
  - The no-case authorization, checklist, execution contract, or runner changes.
```

## Commission

Perform a read-only adversarial artifact review of the completed no-case smoke-test execution artifacts under:

`docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/`

Primary review targets:

- `no_case_smoke_probe_input_v0.yaml`
- `no_case_smoke_receipt_v0.yaml`
- `no_case_smoke_provenance_v0.yaml`
- `no_case_smoke_stdout_v0.txt`
- `no_case_smoke_stderr_v0.txt`

Purpose: determine whether the run artifacts are internally consistent, safe to retain as no-case raw-API plumbing evidence, and bounded against secret leakage, real-case leakage, and gate-clearing overclaims.

This is not a request to rerun the smoke test.

## Required Output Mode

Use `review-report`.

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_execution_artifacts_adversarial_artifact_review_v0.md`

Before source loading, verify that the required output path does not already exist. If it exists, stop with:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Required report path already exists."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Choose a new report path or explicitly authorize overwrite; do not review in place."
```

After a successful report write, return only a short human summary plus compact `review_summary` YAML. The durable report is the review artifact; chat is courier output.

## Start Preflight

Use this workspace:

`C:\Users\vmon7\Desktop\projects\orca`

Expected branch and revision at prompt creation:

```yaml
expected_branch: main
expected_head: b9adaa26859e599dad17f052049b9065824d7165
```

Dirty-state allowance:

- Modified and untracked Orca docs, overlay files, harness files, prompt files, review outputs, and smoke artifacts are allowed because this lane reviews in-progress uncommitted plumbing.
- Do not require a clean worktree.
- Do require the pinned source hashes above to match before strict review claims.
- If any target smoke artifact hash does not match, stop with `SOURCE_CONTEXT_INCOMPLETE`.

Record this start state:

```yaml
orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: no_case_smoke_execution_artifact_review
  edit_permission: read-only
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/
    - docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_execution_artifacts_adversarial_artifact_review_v0.md
  dirty_state_checked: yes/no
  blocked_if_missing: required output path must be unused; target and controlling hashes must match
```

## Required Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `REFERENCE-LOAD` these method instructions, if available:
   - `C:\Users\vmon7\.codex\skills\workflow-deep-thinking\SKILL.md`
   - `C:\Users\vmon7\.codex\skills\workflow-adversarial-artifact-review\SKILL.md`
3. Do not APPLY either method yet.
4. SOURCE-LOAD the required local sources and verify all pinned hashes.
5. Declare `SOURCE_CONTEXT_READY` only after all local hashes match and output path preflight passes. If any local hash fails, declare `SOURCE_CONTEXT_INCOMPLETE`.
6. APPLY `workflow-deep-thinking` to frame failure modes and decision criteria.
7. APPLY `workflow-adversarial-artifact-review` to produce findings and the durable report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only result. Do not emit formal verdicts, severity authority, blocked/ready status, validation claims, readiness claims, mandatory remediation, patch queues, executor-ready handoffs, or alignment-complete claims.

## Required Local Sources

Load and hash-verify all files in `input_hashes`.

Do not use web search. Do not call OpenAI. Do not inspect, print, validate, hash, or test any API key.

## Review Target Boundary

Review only the completed no-case smoke-test execution artifacts and directly controlling authorization/contract sources listed above.

Do not:

- rerun the smoke test;
- make a model/provider call;
- read, print, validate, hash, or test `OPENAI_API_KEY`;
- create, modify, or delete smoke artifacts;
- inspect participant packets, facilitator ledgers, source packets, or real-case fixtures;
- run a real-case memorization probe;
- authorize blind-use, scoring, validation, fixture admission, product proof, or judgment-quality claims;
- emit patch queues or executor-ready implementation instructions.

## Decision Criteria

Check these surfaces adversarially:

1. Artifact existence and hash integrity: all target smoke artifacts exist and match pinned hashes.
2. Authorization alignment: receipt/provenance/provider/model/endpoint/input/output scope matches the patched authorization record and one-shot operator prompt.
3. Synthetic no-case boundary: probe input and artifacts contain no Daimler, Canoo, Unity, TR/Casetext, Milwaukee, real companies, real transactions, real votes, real disputes, real outcomes, participant packets, source packets, facilitator ledgers, or review packets.
4. Receipt consistency: `probe_result`, `isolation_result`, `gate_interpretation`, `prompt_hash`, `raw_response_hash`, provider/model metadata, and no-tools evidence fields are present and internally coherent.
5. Provenance consistency: provenance status, process exit status, receipt hash, prompt hash, raw response hash, input hash, runner hash, authorization hash, stdout/stderr capture, timestamps, and exact command are coherent with the actual artifacts.
6. Secret leakage: scan smoke artifacts for API-key-like or bearer-token-like patterns. If found, do not print the secret value. Report only path, field/context, and `SECRET_PATTERN_FOUND`.
7. Stdout/stderr capture: stdout/stderr files exist, are represented in provenance, and do not contradict receipt/provenance state.
8. Non-gate-clearing boundary: receipt `pass_valid` is clearly treated as no-case plumbing evidence only, not a real-case probe pass, blind-use authorization, validation, fixture admission, product proof, or judgment-quality evidence.
9. Artifact folder role: smoke artifacts are under the accepted no-case smoke folder and remain plumbing evidence only by folder rule.
10. Post-run next action: next step should be acceptance/retention of plumbing evidence or a bounded patch/recheck if findings require it, not real-case exposure by default.

## Findings Contract

Use severity labels only as finding-priority labels:

- `critical`: a defect that leaks a secret, exposes real-case/participant material, creates false gate-clearing evidence, or makes the run unsafe to retain without remediation.
- `major`: a defect that materially weakens auditability, makes receipt/provenance consistency ambiguous, or could mislead an operator about what the smoke run proves.
- `minor`: bounded hygiene, retrievability, or optional hardening that does not alter safe retention as plumbing evidence.

For each finding include:

- severity;
- location;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- advisory remediation direction.

Do not include `patch_queue_entry`.

Allowed recommendations:

- `accept`
- `accept_with_friction`
- `patch_before_acceptance`
- `reject`
- `blocked`

Interpretation:

- `accept`: no critical or major findings; artifacts can be retained as no-case plumbing evidence.
- `accept_with_friction`: no critical or major findings, but minor findings should travel before retention/use.
- `patch_before_acceptance`: at least one major finding should be resolved before treating the run as accepted plumbing evidence.
- `reject`: artifacts are unsafe or misleading in kind for the intended no-case smoke lane.
- `blocked`: required sources, output path, or method application failed.

## Required Report Shape

The durable report should include:

1. Commission.
2. Target artifact set.
3. Authority.
4. Source-read and hash-verification receipt.
5. Artifact consistency checks.
6. Secret/leakage scan result without printing secrets.
7. Findings ordered by severity.
8. Non-findings on key no-case/non-gate-clearing surfaces when clean.
9. Recommendation.
10. Next authorized action.
11. Review-use boundary.

After writing the report, fresh-read it, compute its SHA-256, and include that hash in the returned YAML.

Return this YAML shape in chat after the report is written:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_execution_artifacts_adversarial_artifact_review_v0.md
  report_hash: "<SHA256>"
  reviewed_target_root: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/
  reviewed_receipt_hash: DB2A90D8FF93CD58D6409AD0CD72AA44F69FF162050B656D4B297A88B48C7B61
  reviewed_provenance_hash: 8CA53EB85003ACBD75965C2A445AE083143A1E03FCE2FE4D3D6294A045273660
  recommendation: "accept | accept_with_friction | patch_before_acceptance | reject | blocked"
  summary: "<one sentence>"
  findings_count: <integer>
  blocking_findings: []
  advisory_findings: []
  next_action: "<one concrete next step>"
  non_claims:
    - no live provider call
    - no API key inspection
    - no smoke rerun
    - no real-case probe
    - no participant packet exposure
    - no blind judgment
    - no scoring
    - no ledger freeze
    - no schema/runtime implementation
    - no validation
    - no fixture admission
    - no product proof
    - no judgment-quality claim
```

Review-use boundary: review findings are decision input only; they are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized.

Required closeout boundary: plumbing works only; not judgment quality.
