# Bronze Catalog Coverage Census Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed delegated adversarial implementation/code review prompt for PR #505's
  Bronze Catalog coverage census slice: read-only real-lake census reporting,
  source-family/source-surface/Attachment Record counting, bounded issue samples,
  CLI exit behavior, and repo-map wording.
use_when:
  - Commissioning a de-correlated reviewer to inspect PR #505 before merge.
  - Checking the bounded review target, target revision, hash pins, and output contract for this review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: 64e7333b5e6743c68bf76440e6a2eace4fc6fc7d..2ecff496ce6fce0916f5680e3107102a66e034d6
prompt_carrier_note: >
  This prompt may be committed after the implementation commit on PR #505.
  The implementation target under review ends at
  2ecff496ce6fce0916f5680e3107102a66e034d6; later prompt-only carrier
  commits do not change the reviewed implementation unless they modify the
  named target files.
stale_if:
  - PR #505 is retargeted away from base 64e7333b5e6743c68bf76440e6a2eace4fc6fc7d.
  - Any named implementation target file changes after 2ecff496ce6fce0916f5680e3107102a66e034d6 and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor cannot inspect the PR, target commit, or named files.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is `review-report` to `docs/review-outputs/bronze_catalog_coverage_census_adversarial_code_review_v0.md`.
- Template kind: review. Orca-local `repo-code-review` template kind is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only by default. Target PR is `https://github.com/eric-foo/orca/pull/505`, branch `codex/bronze-real-lake-census`, base branch `codex/bronze-v41-clean-verify`, implementation range `64e7333b5e6743c68bf76440e6a2eace4fc6fc7d..2ecff496ce6fce0916f5680e3107102a66e034d6`. Dirty state allowed only for this prompt artifact or later prompt-carrier commits that do not touch target files.
- Patch boundary: this commission came from a `workflow-delegated-review-patch` request, but the target is a multi-file implementation/code diff. Under the Orca delegated-review-patch overlay, do not silently stretch the provisional one-artifact review-and-patch convention. No source edit is authorized by this prompt. If a later operator instruction explicitly grants patch execution, edits must be limited to the named PR #505 target files, reported as a diff, and must not be committed, pushed, merged, or treated as accepted without home-model adjudication.
- Reviews: findings-first. This is advisory implementation/code review. Do not emit formal PASS, readiness, mandatory remediation, approval, or validation verdict.
- Doctrine change: none intended by this prompt. It routes a review of a prior implementation change; it does not alter Data Lake doctrine, Attachment Record doctrine, prompt doctrine, review doctrine, validation doctrine, Capture, Cleaning, ECR, Judgment, Silver, or product doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/bronze_catalog_coverage_census_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of PR #505's Bronze Catalog coverage census slice. The implementation commit under review is `2ecff496ce6fce0916f5680e3107102a66e034d6`, with base `64e7333b5e6743c68bf76440e6a2eace4fc6fc7d`.

Review purpose:

1. Determine whether `--census` gives a high-signal, read-only real-lake coverage view over generated Bronze Catalog state without rebuilding, mutating, or overstating lake authority.
2. Attack whether the report can honestly guide the next Bronze material steps: stale/missing generated catalog closure, real coverage accounting across current capture lanes, and future-lane adaptability.
3. Verify that counts and issue samples for packets, Attachment Records, source families, and source surfaces remain bounded, deterministic, and useful even when generated files are missing or stale.
4. Inspect CLI and schema behavior so downstream/operator use gets a clear exit signal without breaking normal inspect/rebuild flows.
5. Check repo-map wording for retrieval/census scope only, with no "god tier", completeness, validation, source-of-truth, live-lake mutation, Silver readiness, or final AR physicalization claim.

This is not a request to rerun live capture, rebuild the live lake, migrate raw data, change Silver/Gold lanes, or finalize Attachment Record storage architecture.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor / model lineage from OpenAI to claim cross-vendor discovery.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing or same-vendor, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` if available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce findings-first implementation/code review.
5. If `workflow-code-review` is unavailable, use its zero-config findings-only advisory semantics from the prompt text below, but mark strict review claims `NOT_CLAIMED`.

## Required Reads

Read these authority and boundary files first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/source-of-truth.md`

Then read the review target at implementation commit `2ecff496ce6fce0916f5680e3107102a66e034d6`:

- `orca-harness/data_lake/catalog.py`
- `orca-harness/runners/run_data_lake_catalog.py`
- `orca-harness/tests/test_data_lake_catalog.py`
- `docs/workflows/orca_repo_map_v0.md`

Read adjacent implementation context as needed, but do not widen the review target:

- `orca-harness/data_lake/root.py`
- `orca-harness/source_capture/fragrance_review_lake.py`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `docs/prompts/reviews/bronze_catalog_source_surface_coverage_adversarial_code_review_prompt_v0.md`
- `docs/prompts/reviews/bronze_attachment_record_catalog_adversarial_code_review_prompt_v0.md`

## Target Diff And Dirty-State Allowance

Implementation target range:

```text
64e7333b5e6743c68bf76440e6a2eace4fc6fc7d..2ecff496ce6fce0916f5680e3107102a66e034d6
```

Observed target files in that range:

```text
M docs/workflows/orca_repo_map_v0.md
M orca-harness/data_lake/catalog.py
M orca-harness/runners/run_data_lake_catalog.py
M orca-harness/tests/test_data_lake_catalog.py
```

Use this command shape as the reviewed implementation diff:

```powershell
git diff 64e7333b5e6743c68bf76440e6a2eace4fc6fc7d..2ecff496ce6fce0916f5680e3107102a66e034d6 -- docs/workflows/orca_repo_map_v0.md orca-harness/data_lake/catalog.py orca-harness/runners/run_data_lake_catalog.py orca-harness/tests/test_data_lake_catalog.py
```

The author observed this diffstat:

```text
4 files changed, 223 insertions(+), 4 deletions(-)
```

The author observed these Windows worktree SHA256 pins for the target files at implementation commit `2ecff496ce6fce0916f5680e3107102a66e034d6`:

```text
31CFC8C22F28D12D233CF6DC94783F14A3AC700837690E34699AAEBFE799A738  docs/workflows/orca_repo_map_v0.md
0DFD08BDCE02DD8EFBA5F362558DFF5528C7B3201B41596CEE75558814148FEF  orca-harness/data_lake/catalog.py
735CA02349857A5CBF73BF103FB5C16BBA5B2631C7040C3DDFF8C78505CCB412  orca-harness/runners/run_data_lake_catalog.py
C574073DBD5B2418BBB0FC5D2F9189224935B8B8A15808602F3AC52EF9305035  orca-harness/tests/test_data_lake_catalog.py
```

If the branch contains a later prompt-only commit, verify whether the four target files above still match `2ecff496ce6fce0916f5680e3107102a66e034d6`. If they changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The author observed these checks after the implementation commit:

```powershell
python -m py_compile orca-harness\data_lake\catalog.py orca-harness\runners\run_data_lake_catalog.py
python -m pytest -q orca-harness\tests\test_data_lake_catalog.py
git diff --check
python .agents\hooks\check_retrieval_header.py docs\workflows\orca_repo_map_v0.md
python .agents\hooks\header_index.py --strict
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_repo_map_freshness.py docs\workflows\orca_repo_map_v0.md
python orca-harness\runners\run_data_lake_catalog.py --census --root F:\work\orca-lake
gh pr checks 505 --watch
```

Observed validation notes:

- `py_compile` exited 0.
- Focused catalog pytest exited 0 with `18 passed, 1 skipped`.
- Retrieval-header, header-index, map-links, repo-map freshness, and `git diff --check` exited 0.
- The read-only F-lake census command exited nonzero with `status=issues_found`, `expected_packet_count=99`, `attachment_record_count=216`, `source_family_count=6`, and `source_surface_count=7`; issue samples reported stale/missing generated catalog files. Treat that as an honest census result to inspect, not as a failure of the command.
- GitHub PR #505 checks passed for `orca-harness-tests`.

Independently rerun the validation commands you judge necessary. If you do not rerun a command, report that command as author-supplied and not independently revalidated. Do not run live capture, public web research, live lake rebuild, live lake mutation, network source access, Cleaning/ECR/Judgment materialization, Silver/Gold migration, or final Attachment Record storage migration.

## Review Scope

Attack these questions:

- Does `--census` stay read-only in all paths, including when generated catalog files are stale, missing, orphaned, unreadable, or internally inconsistent?
- Does the CLI exit nonzero for `issues_found` while preserving default inspect/rebuild behavior and clear `--rebuild` / `--census` mutual exclusion?
- Are `status`, issue counters, bounded issue samples, expected/generated packet counts, Attachment Record counts, source-family counts, and source-surface counts internally consistent with the existing generated catalog semantics?
- Does the census avoid implying that generated catalog files are authoritative over raw packets, that current source-family coverage is complete, or that stale generated files are acceptable?
- Does the report make the next operational move obvious when a real lake has stale/missing generated files: rebuild/catalog refresh rather than semantic folder inference, source-capture rerun, or Silver migration?
- Are source-family and source-surface names discovered generically enough for fragrance, Instagram, Reddit, YouTube, and unknown future lanes without adding lake-core fields for one family?
- Do Attachment Record counts in census mode coordinate correctly with the generated AR slice from the base branch without claiming final AR physicalization, payload validation, or downstream currentness?
- Are issue samples bounded and deterministic so a large lake cannot flood operator output while still leaving enough detail to find full artifacts through inspect or generated files?
- Do tests assert the real failure modes: stale/missing generated files, read-only behavior, bounded samples, command exit behavior, source-family/source-surface counts, and compatibility with existing inspect/rebuild?
- Does the repo-map wording describe retrieval/census coverage only, without "god tier", MGT readiness, validation, authority, or all-lane completeness leakage?

## Intended Closure Check

Treat these PR #505 goals as claims to verify, not accepted truth:

- CENSUS-01 read-only real-lake visibility: operators can run a no-rebuild census that reports generated catalog health and high-level coverage without mutating the lake.
- CENSUS-02 honest stale-index signal: missing/stale/orphaned generated files produce `issues_found` and actionable samples rather than silent success.
- CENSUS-03 coverage accounting: packet, Attachment Record, source-family, and source-surface counts line up with generated catalog expectations and remain useful across current lanes.
- CENSUS-04 future-lane adaptability: unknown or new source families stay visible through generic raw packet and generated catalog signals without source-family-specific lake-core schema.
- CENSUS-05 CLI/operator ergonomics: exit codes and output schema are clear enough for CI, scripts, and humans without breaking default inspect/rebuild use.
- CENSUS-06 regression coverage: tests protect the behavior above, not only the happy path.

For each, report one of:

- `closed`: implementation and tests now cover the failure mode.
- `partially_closed`: some protection exists but a material variant remains.
- `not_closed`: the original failure mode remains.
- `not_assessed`: source or environment prevented assessment.

If `partially_closed` or `not_closed`, include evidence and a minimum closure condition.

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness, acceptance, validation, or pass/fail verdict unless Orca overlay authority is supplied separately. Use findings-only advisory review. Do not emit `patch_queue_entry`; do not edit source files under this prompt; do not commit, push, PR, merge, run live capture, or run live lake mutation/rebuild operations.

If you find no blocker or major issue, say so and state residual risks or validation gaps. If you find an issue, findings lead the report and must include:

- finding id
- severity as `blocker`, `major`, or `minor` for prioritization only, not formal Orca verdict authority
- target file and stable line/anchor
- evidence from the implementation
- authority or evidence basis
- concrete impact
- minimum closure condition
- next authorized action
- validation expectation

## Output Contract

Write the full review report to:

`docs/review-outputs/bronze_catalog_coverage_census_adversarial_code_review_v0.md`

If that path already exists, do not overwrite it without operator authorization. Choose the next versioned path only if the operator permits that retarget, and record the retarget in the report.

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: openai-gpt-5-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- validation run ledger
- findings-first review body
- closure check against CENSUS-01 through CENSUS-06
- strict not-claimed boundaries

Close with this courier block so the home model can adjudicate later:

```yaml
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL:
  source_context: SOURCE_CONTEXT_READY_OR_INCOMPLETE
  reviewed_by: operator_to_fill
  authored_by: openai-gpt-5-codex
  de_correlation_bar: cross_vendor_discovery_OR_same_vendor_sanity_OR_self_fallback
  same_vendor_rationale: required_if_same_vendor_sanity
  target_pr: 505
  target_base: 64e7333b5e6743c68bf76440e6a2eace4fc6fc7d
  target_head: 2ecff496ce6fce0916f5680e3107102a66e034d6
  reviewed_files:
    - docs/workflows/orca_repo_map_v0.md
    - orca-harness/data_lake/catalog.py
    - orca-harness/runners/run_data_lake_catalog.py
    - orca-harness/tests/test_data_lake_catalog.py
  report_path: docs/review-outputs/bronze_catalog_coverage_census_adversarial_code_review_v0.md
  findings: []
  closure_check:
    CENSUS-01: closed_OR_partially_closed_OR_not_closed_OR_not_assessed
    CENSUS-02: closed_OR_partially_closed_OR_not_closed_OR_not_assessed
    CENSUS-03: closed_OR_partially_closed_OR_not_closed_OR_not_assessed
    CENSUS-04: closed_OR_partially_closed_OR_not_closed_OR_not_assessed
    CENSUS-05: closed_OR_partially_closed_OR_not_closed_OR_not_assessed
    CENSUS-06: closed_OR_partially_closed_OR_not_closed_OR_not_assessed
  proposed_patch_present: no_unless_separately_authorized
  needs_architecture_pass: yes_OR_no
  validation_run: []
  not_claimed:
    - formal_verdict
    - readiness
    - approval
    - validation_pass_fail_authority
    - patch_queue
    - runtime_model_recommendation
  ca_adjudication_required: true
```

For this prompt, proposed patch, diff, exact requested edits, formal verdict, severity authority, readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner instruction binds them.
