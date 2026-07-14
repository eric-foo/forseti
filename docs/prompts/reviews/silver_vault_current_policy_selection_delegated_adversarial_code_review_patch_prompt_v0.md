# Silver Vault Current-Policy Selection — Delegated Adversarial Code Review-and-Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code review-and-patch commission
scope: >
  Different-vendor review and bounded patch pass for Silver Vault product-mention
  policy identity, exact-policy current-record selection, consumer convergence,
  residual visibility, contracts, and focused tests.
use_when:
  - Reviewing branch codex/silver-current-policy-selection before merge.
authority_boundary: retrieval_only
```

## Forseti Prompt Preflight

```text
forseti_prompt_preflight:
  output_mode: review-report
  repository: C:\tmp\forseti-silver-current-policy-selection
  commissioned_branch: codex/silver-current-policy-selection
  commissioned_base_revision: 702df6188f5c72efe4b6f4ea45c0751ef5c496ba
  commissioned_target: the 18 named implementation, contract, workflow, and test files in the target manifest below
  author_model_family: OpenAI / Codex
  controller_identity: operator_to_fill
  reviewer_requirement: different vendor/model lineage from OpenAI; stop if this cannot be established
  operating_mode: repo-visible delegated_code_review_and_patch
  source_loading: confirm, do not trust; perform the receiving preflight and read current source before strict claims
  edit_permission: patch only confirmed defects inside the named target files; the required review report is the only additional write
  lifecycle_permission: do not commit, push, merge, open/update PRs, stash, reset, clean, delete files, or run production capture
  required_methods: workflow-deep-thinking, then workflow-code-review
  durable_output: docs/review-outputs/silver_vault_current_policy_selection_delegated_adversarial_code_review_v0.md
  stop_if: wrong worktree/branch, target-byte mismatch, concurrent writer, same-vendor reviewer, unavailable source, or scope expansion required
```

## Receiving Preflight — Required Before Source Loading

Report all of the following from fresh reads:

- `launch_checkout`, `effective_target_worktree`, current branch, observed HEAD, and clean/dirty state;
- direct-write proof that edits in the effective target worktree affect `codex/silver-current-policy-selection`;
- confirmation that no other writer is active in that worktree;
- confirmation that base revision `702df6188f5c72efe4b6f4ea45c0751ef5c496ba` is reachable;
- controller model/version/vendor as observed by the operator, and confirmation that its vendor is not OpenAI;
- a SHA-256 check of every commissioned target against the manifest below.

The prompt file itself may be present as review-routing infrastructure. It is not
part of the code-review target. Any other target mismatch or dirty overlap is a
hard stop: report `BLOCKED_TARGET_STATE_MISMATCH` and do not patch.

## Target Manifest

These hashes identify the commissioned working bytes observed after the focused
validation run. Hashes are lowercase SHA-256.

```text
233a3aafa9b5c16966f91e28d7f3b84d7e25f1d239f706a936b75d9c014064b8  docs/workflows/sov_extraction_quality_eval_report_v0.md
db3f2fe5bfde29a53f14cf33307e7891b63f99e6db0f2009630d07e760c4f9c5  forseti-harness/cleaning/transcript_product_lake.py
9c3509f76be43391892ce4cf3ccf2c4300084d2215dc366407aef5d9f771e0dd  forseti-harness/data_lake/derived_retrieval_views.py
781da9d67b1ed04ca75d8617ee7fb17c8030af5ee352111b97ce3def8f8b5c71  forseti-harness/data_lake/inventory.py
67071f2efc22dc63392c340b0459aa05b5e57241970eecd44d0431343713b1cf  forseti-harness/data_lake/product_mention_selection.py
4c1fb42407b62aac234375a836667ddbbe271502b7241f9ee7c8d259dff682d4  forseti-harness/data_lake/sov_readout.py
816b734b14da0791fccd0ab6c18400e92d11816774edd5b239deb7e5f2930491  forseti-harness/runners/run_data_lake_indexes_rebuild.py
22bb03e4e54f678cf9b6db11d5413a0d7544be52fef816f44a3b54b36e8930d4  forseti-harness/runners/run_data_lake_sov_readout.py
af4236794ec442f7104ee5587ddadca99eae6fb2fd29ca8804a8a0f4d1aac59f  forseti-harness/runners/run_sov_extraction_quality_eval.py
ceab8d57016eabdad949945e14a51b2296caf502f42666438576e65fd50134c6  forseti-harness/runners/run_transcript_product_extract.py
6097dafd33b0b08bd36b4cf9eac7a6ff094380379fc6ea3b2b0216b9b6f8f55b  forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
83e20e00938a9bb4346f7f6146c6488430e84f80b3dbfc88be2eba2266f384cb  forseti-harness/tests/test_data_lake_indexes_rebuild.py
f356dfdd88406fe6bf2c9edeb403df206ef2c83094e3f258844a223bcce01e9c  forseti-harness/tests/test_data_lake_rebuild_proof.py
c2e7305b60cba0a200370f6a822f5a20099940635fefbed26f3cc08f04bb6af0  forseti-harness/tests/test_data_lake_sov_readout.py
65d4adb35d1cde3173a89522f543482d1d5d5250a90fdc07eb130d356e38c020  forseti-harness/tests/test_sov_extraction_quality_eval.py
35455d95e998e2a531f6685c8d86faba27f934a860d95b7f7b9544b8bdb48ca2  forseti-harness/tests/unit/test_transcript_product_lake.py
faf32a609d749f6b5c8f1f2f8c93f6dd34933defe6327169084c9ef54544d8d8  forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
37536432ca9deb0bcba9af2d9caf60b6ed5e15a8c8a01013c8026dcf5a2fee73  forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
```

## Source Gate

Read completely before findings:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- every file in the target manifest
- the complete diff from the commissioned base revision to the current target bytes
- the nearest imported selector/identity helpers needed to judge the changed behavior

Declare `SOURCE_CONTEXT_READY` only after those reads. Then apply
`workflow-deep-thinking`, followed by `workflow-code-review`, with this project
overlay taking precedence over generic defaults.

## Review Target and Fitness Contract

Goal: prevent write-once Silver product-mention siblings from silently reusing
completion identity or being double-counted after policy changes, while making
selection exclusions visible rather than quietly dropping them.

The commissioned behavior is complete only if:

1. Product-mention policy version and the full SHA-256 policy fingerprint are part of durable record/completion identity; a policy change forces a distinct record and completion marker.
2. Exact policy version plus exact 64-hex fingerprint is required. No newest-file, version-only, fingerprint-prefix, or implicit fallback is accepted.
3. By-mention retrieval, Share of Voice readout, and extraction-quality evaluation all use the same selector and cannot independently walk the Silver lane.
4. Every lane file is either selected or represented by an explicit residual/status; wrong policy and malformed/unusable records remain lake-wide visible.
5. A subject has at most one selected record for the requested exact policy. Distinct same-policy siblings fail closed instead of being tie-broken or counted twice.
6. Subject identity preserves the raw/source/provenance anchors needed to prevent unrelated observations from collapsing together, without treating model choice as subject identity.
7. Rebuild/proof flows preserve and reuse the exact policy contract, and structured runner failures remain visible.
8. The contracts, inventory declarations, workflow report, and focused tests state the same behavior as the runtime.
9. Legacy lanes and live-population migration remain out of scope; this patch changes current product-mention identity and reads only.

Observed author-side validation before commission: 105 focused tests passed;
15 modified Python files compiled; `git diff --check` passed. Treat this as
reported evidence to reproduce, not as reviewer-observed proof.

## Adversarial Questions

At minimum, attack these seams:

- Can two different full policy fingerprints that share a readable prefix reuse a record/completion identity?
- Can a caller omit, partially specify, normalize inconsistently, or mismatch the policy pair and still receive apparently valid data?
- Do all three consumers truly delegate selection, or does any residual direct lane walk, manifest shortcut, or proof path bypass the selector?
- Can malformed envelopes, lineage states, wrong kinds, missing subjects, policy mismatches, or bypassed siblings disappear without an explicit residual?
- Can two distinct same-policy records for one subject be silently tie-broken because their refs, timestamps, provenance, or serialization differ?
- Can the subject key collapse distinct source observations, or split the same observation because of model/output metadata?
- Can a selector result become nondeterministic across filesystem order, path normalization, Windows case behavior, or duplicate refs?
- Can rebuild/proof manifests claim one policy while their stored by-mention rows or source refs came from another?
- Can SoV coverage or quality-eval denominators count selected records while hiding lake-wide exclusions?
- Can a corrupt file turn a hard ambiguity into a benign residual, or can a benign residual abort the entire consumer unexpectedly?
- Do CLI error envelopes preserve failure visibility and stable exit semantics?
- Do tests prove the production call paths and identity boundaries, or only injected/fake helper behavior?
- Does any changed line expand legacy migration, live population, schema authority, or maintenance surface beyond this bounded outcome?

## Patch Authority

Patch only confirmed defects inside the 18 target files. Keep the smallest
complete correction and preserve real failure visibility. Do not add unrelated
cleanup, migrate legacy data, change live population, redesign the wider lake,
or create a fallback success path.

For each patched defect, record the finding, evidence, changed files, and the
same-check red/green proof when practical. Leave all patches and the report
uncommitted. Do not push, open/update a PR, merge, stash, reset, or clean.

If a confirmed defect requires edits outside the target files or changes the
accepted architecture/contract, stop and return `NEEDS_ARCHITECTURE_PASS` with
the evidence and minimum closure condition. Do not widen scope yourself.

## Validation Route

From `forseti-harness/`, rerun:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest-silver-current-policy-review tests\unit\test_transcript_product_lake.py tests\unit\test_sibling_selection.py tests\test_data_lake_indexes_rebuild.py tests\test_data_lake_rebuild_proof.py tests\test_data_lake_sov_readout.py tests\test_sov_extraction_quality_eval.py tests\contract\test_silver_reader_selection_gate.py tests\contract\test_capture_runner_lake_seam_coverage.py tests\unit\test_silver_lane_registry_guard.py
```

From the repository root, also run:

```powershell
$py = @(git diff --name-only --diff-filter=ACMRT 702df6188f5c72efe4b6f4ea45c0751ef5c496ba -- '*.py')
python -m py_compile $py
git diff --check 702df6188f5c72efe4b6f4ea45c0751ef5c496ba
```

Report exact commands, exit codes, observed counts, warnings, and every not-run
check. Never convert a skipped or blocked check into success.

## Required Report and Return

Write:

`docs/review-outputs/silver_vault_current_policy_selection_delegated_adversarial_code_review_v0.md`

Include:

- receiving-preflight and different-vendor evidence;
- `reviewed_by` and `authored_by` (`unrecorded` only when genuinely unavailable);
- `de_correlation_bar: cross_vendor_discovery`;
- source-read ledger and `SOURCE_CONTEXT_READY` evidence;
- findings ordered by correctness impact, each with location/evidence, authority basis, confidence, minimum closure condition, next authorized action, and verification expectation;
- `considered_and_defended` candidates that survived the attack;
- exact patch summary and changed-file scope, or an explicit no-patch result;
- validation commands, exit codes, observed results, and not-run checks;
- reviewer verdict, residual risks, off-scope flags, and not-proven boundaries;
- a review-use boundary: findings and patches are decision input for home-model adjudication, not approval or merge authority;
- the following courier block, completed with the actual result.

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

Include:
- original commission and target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- applied patch or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

If no defect is confirmed, say so explicitly and do not manufacture a patch.
