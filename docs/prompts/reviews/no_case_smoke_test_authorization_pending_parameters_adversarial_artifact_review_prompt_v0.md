# No-Case Smoke Test Authorization Pending Parameters Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review of the pending-parameters no-case smoke-test authorization decision.
use_when:
  - Launching an adversarial review of the no-case smoke-test pending-parameters decision artifact.
  - Checking whether the decision artifact preserves the blocked/non-authorizing state before any live no-case smoke test.
  - Verifying the artifact cannot be mistaken for live-call, probe, validation, or gate-clearing authorization.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
```

## Paste-Ready Prompt

````text
You are performing a read-only adversarial artifact review for Orca.

Repository: C:\Users\vmon7\Desktop\projects\orca
Expected branch: main
Expected HEAD: 27cae7b4aec3f97656044ef82c4fea1a19ddc07f

Required output mode: filesystem-output.
Required output path:
docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_adversarial_artifact_review_v0.md

Review type: read-only adversarial artifact review.
Do not patch files. Do not produce a patch queue. Do not run live provider calls. Do not run models. Do not pass `--allow-live-provider-call`. Do not read API keys. Do not create a smoke receipt or provenance record. Do not expose participant packets. Do not run a real probe, blind judgment, scoring, validation, fixture admission, ledger freeze, product proof, or judgment-quality proof.

If the output path already exists, stop with:

```yaml
review_summary:
  status: blocked
  reason: BLOCKED_OUTPUT_COLLISION
```

## Source-Gated Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-adversarial-artifact-review`. Do not APPLY them yet. If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after source readiness, stop before formal review claims and return a blocked or advisory-only result naming the missing method.
3. SOURCE-LOAD the required source files below.
4. Verify all required source hashes exactly before declaring `SOURCE_CONTEXT_READY`.
5. If a file hash mismatches, stop before review and report the mismatch. If HEAD differs but all source hashes match, annotate the HEAD discrepancy and continue.
6. After `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame the authorization-boundary and fake-pass failure modes.
7. Then APPLY `workflow-adversarial-artifact-review` to write the durable report.
8. Fresh-read the report and compute its SHA-256 before returning chat closeout.

## Required Sources and Hashes

Authority and review rules:

```yaml
AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
.agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
.agents/workflow-overlay/source-loading.md: 9B4F8141D3B6FDB224642EF8E72A7DA681EB96AC8271870654C401E63B26C6B2
.agents/workflow-overlay/review-lanes.md: 2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199
.agents/workflow-overlay/artifact-folders.md: 4F109032585D1C4E3EC9C294CE38B16190B14ECFDE2FCAE5EBE0FD3ADB240505
.agents/workflow-overlay/artifact-roles.md: C8BD0DA4ACCECC2199E9FEED2A6C2BFBA617092E9A99A9D287AF86327C24DD7F
.agents/workflow-overlay/retrieval-metadata.md: 8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F
```

Review target:

```yaml
docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md: FE0C1E3D88E07215C9D6BBB4F30B49BCAC417509DD3D2E715D05646036F6AD93
```

Governing no-tools/no-case sources:

```yaml
docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 7A17255422C546858C54807161A265074FC0A5BD6739AFDE5592A51D94A8B26D
docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: F46AA6A4003E200C41796826277A6D8074ED84F26E6B6A5DD9E15584BE5EB0F5
docs/review-outputs/no_tools_execution_foundation_f01_f02_post_patch_adversarial_recheck_v0.md: 01129B39570F629AFF91BEB6631A70D6ABB5DB4F47885C07F083C153ABEAD016
orca-harness/runners/run_memorization_probe_raw_api.py: CD83FDE1960CA503AD0EE39188CB49EB4676426115A54A7A38A888AA2A99A021
```

Dirty-state allowance: broad dirty/untracked workspace is allowed for this review, including the untracked target artifact, as long as all required source hashes match and the required output path is unused. Do not treat unrelated dirty files as blockers. Do not mutate files.

## Review Commission

Review the target artifact:

`docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md`

The question is whether this pending-parameters decision artifact is safe, coherent, and sufficiently bounded as a non-authorizing precursor to a future one-shot no-case raw-API smoke-test authorization.

The review must determine:

- whether the artifact clearly preserves `blocked_pending_concrete_owner_parameters`;
- whether it avoids authorizing a live provider call or `--allow-live-provider-call`;
- whether all future authorization fields required by `no_case_smoke_test_authorization_checklist_v0.md` are present and visibly unset;
- whether the synthetic `SMOKE_NOCASE_` boundary is clear and cannot be mistaken for a real case probe;
- whether future receipt/provenance path patterns and required provenance fields are sufficient and placed under an accepted Orca folder boundary;
- whether blocked states are complete enough to prevent inference from environment state;
- whether the non-gate-clearing rule prevents `pass_valid`/`proven` smoke receipts from being laundered into memorization-probe, blind-use, validation, fixture-admission, product-proof, or judgment-quality claims;
- whether retrieval metadata and source hashes are consistent with the governing sources;
- whether the artifact introduces any blocker or major regression against the accepted F-01/F-02 closure.

## Failure Modes To Stress

Be adversarial about these surfaces:

1. **False authorization:** Any language that could be read as allowing a live call, `--allow-live-provider-call`, provider access inference, or smoke execution now.
2. **Fake pass laundering:** Any path by which a future smoke receipt with `pass_valid` or `isolation_result: proven` could be cited as a real case/probe gate.
3. **Parameter ambiguity:** Any required concrete field missing, ambiguous, owner-invisible, or inferable from local environment state.
4. **Synthetic boundary weakness:** Any real-case, company, source, vote, transaction, dispute, public identifier, or outcome residue.
5. **Path/role mismatch:** Any future receipt/provenance path pattern that conflicts with accepted Orca artifact folders or makes artifacts hard to discover.
6. **Provenance insufficiency:** Missing stdout, stderr, exit status, receipt hash, prompt hash, raw response hash, endpoint, model, credential-lane, or timestamp binding.
7. **Review/patch authority drift:** Any language that creates patch authority, validation approval, readiness, fixture admission, or mandatory remediation without binding.
8. **Source-staleness risk:** Any input hash, stale condition, or open-next field that would mislead a future operator after runner/checklist/contract changes.

## Severity And Recommendation Contract

Use these finding severities only as priority labels:

- `critical`: the artifact could authorize forbidden execution, expose real case/participant material, or create a fake gate-clearing path.
- `major`: the artifact preserves safety intent but has a material ambiguity, missing required field, path/role mismatch, or source-staleness problem that should be resolved before it is used as the basis for concrete smoke authorization.
- `minor`: hygiene, retrievability, clarity, or optional hardening that does not block the pending-parameters artifact from serving as decision input.

Allowed recommendations:

- `accept`
- `accept_with_friction`
- `patch_before_use`
- `blocked`

These recommendations are decision input only. They are not approval, validation, mandatory remediation, executor-ready patch authority, fixture admission, live-call authorization, or readiness proof.

For each actionable finding, include:

- `id`
- `severity`
- `summary`
- `evidence`
- `risk`
- `minimum_closure_condition`
- `next_authorized_action`

Do not include `patch_queue_entry`.

## Durable Report Requirements

Write the full report to:

`docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_adversarial_artifact_review_v0.md`

The report should include:

1. Commission.
2. Target.
3. Authority and sources.
4. Hash verification table.
5. Decision criteria.
6. Findings first, ordered by severity.
7. Non-findings / surfaces checked.
8. Recommendation.
9. Next authorized action.
10. Non-claims.

After writing, fresh-read the report and compute SHA-256.

## Chat Closeout

After the durable report is written and verified, return a short human summary plus this YAML:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_adversarial_artifact_review_v0.md
  report_hash: <SHA256>
  reviewed_target: docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
  reviewed_target_hash: FE0C1E3D88E07215C9D6BBB4F30B49BCAC417509DD3D2E715D05646036F6AD93
  recommendation: <accept | accept_with_friction | patch_before_use | blocked>
  findings_count: <integer>
  blocking_findings: []
  advisory_findings: []
  next_action: <one sentence>
  non_claims:
    - no live provider call
    - no model call
    - no smoke test run
    - no smoke receipt created
    - no provenance record created
    - no memorization probe
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

Required closeout line:

`plumbing works only; not judgment quality.`
````
