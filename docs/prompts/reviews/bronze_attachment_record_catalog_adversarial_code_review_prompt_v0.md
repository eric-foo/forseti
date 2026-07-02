# Bronze Attachment Record Catalog Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated adversarial implementation/code review
  of the Bronze Catalog AR-MGT-90 generated Attachment Record retrieval slice.
use_when:
  - Commissioning an independent reviewer to inspect the Bronze Catalog generated Attachment Record implementation.
  - Checking the prompt source, target revision, output binding, and de-correlation receipt for this review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: f36d7f62c6a8e932e26fcc94718d7eb91be6a981..b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179
prompt_carrier_note: >
  This prompt is committed after the implementation commit. The implementation
  target under review ends at b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179;
  prompt-only carrier commits do not change the implementation target unless
  they modify the named target files.
stale_if:
  - Any named implementation target file changes after b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179 and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor cannot inspect the named worktree or target commit in place.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is `review-report` to `docs/review-outputs/bronze_attachment_record_catalog_adversarial_code_review_v0.md`.
- Template kind: review. Orca-local `repo-code-review` template kind is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-ar-mgt-90`, branch `codex/bronze-ar-mgt-90`, implementation range `f36d7f62c6a8e932e26fcc94718d7eb91be6a981..b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179`. Dirty state allowed only for this prompt artifact or later prompt-carrier commits that do not touch target files.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended by this prompt. It routes a review of a prior implementation change; it does not alter Data Lake doctrine, AR physicalization authority, prompt doctrine, review doctrine, validation doctrine, Capture, Cleaning, ECR, Judgment, or product doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/bronze_attachment_record_catalog_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the Bronze Catalog generated Attachment Record retrieval slice. The implementation commit under review is `b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179` on branch `codex/bronze-ar-mgt-90`, with base `f36d7f62c6a8e932e26fcc94718d7eb91be6a981`.

This prompt was prepared after a fused implementation closeout where adversarial review was recommended. The target is a multi-file implementation/code diff plus repo-map update. No delegated patch authority is commissioned in this prompt: route it through read-only implementation/code review. The reviewer must not patch source files.

Review purpose:

1. Independently attack whether the generated `attachment_records/` catalog entries give downstream lanes durable, typed retrieval coordinates over preserved raw packet bodies without mutating raw packets or claiming final Attachment Record physicalization.
2. Verify whether body resolution is fail-closed against raw packet manifests, body sha/path drift, unsupported reference kind, and unsupported hash basis.
3. Inspect whether source-surface coordination now exposes useful `attachment_record_count` and `attachment_records_path` signals without implying source-family completeness, payload validation, currentness, or source-surface authority.
4. Check that the implementation remains source-family-agnostic across current and future lanes, especially fragrance review, Instagram creator, Reddit, binary/multi-file packet cases, and unknown source surfaces.
5. Scan only the touched implementation scope for patch-caused or newly visible blocker/major issues. Minor findings are allowed, but do not widen into unrelated Capture, Cleaning, ECR, Judgment, Silver, live lake operations, or final AR storage architecture review.

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

Then read the review target:

- `orca-harness/data_lake/catalog.py`
- `orca-harness/tests/test_data_lake_catalog.py`
- `docs/workflows/orca_repo_map_v0.md`

Read adjacent implementation and contract context as needed, but do not widen the review target:

- `orca-harness/data_lake/root.py`
- `orca-harness/runners/run_data_lake_catalog.py`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `orca-harness/source_capture/fragrance_review_lake.py`
- `orca-harness/tests/test_data_lake_root.py`

## Target Diff And Dirty-State Allowance

Implementation target range:

```text
f36d7f62c6a8e932e26fcc94718d7eb91be6a981..b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179
```

Observed target files in that range:

```text
M docs/workflows/orca_repo_map_v0.md
M orca-harness/data_lake/catalog.py
M orca-harness/tests/test_data_lake_catalog.py
```

Use this command shape as the reviewed implementation diff:

```powershell
git diff f36d7f62c6a8e932e26fcc94718d7eb91be6a981..b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179 -- docs/workflows/orca_repo_map_v0.md orca-harness/data_lake/catalog.py orca-harness/tests/test_data_lake_catalog.py
```

The author observed these Windows worktree SHA256 pins for the target files at the implementation commit:

```text
D66EB6A1E9939F3D6EEE520841F0669D68C64EB7D53282FE2CBEDF9FDB2A776A  orca-harness/data_lake/catalog.py
940AAFE2C77A2A8507B6AF7D91D522DB0580B95B8D29C186E34D877C7E3A5E98  orca-harness/tests/test_data_lake_catalog.py
A281D2241CFC9DEE94C957025503CE50E1286BF9B537A2B3D853E6F17B2BE306  docs/workflows/orca_repo_map_v0.md
```

If the branch contains a later prompt-only commit, verify whether the three target files above still match `b85e2a3d1d54cb8a50f441e44e9ed8a2a5917179`. If they changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The author observed these checks after the implementation commit:

```powershell
python -m py_compile orca-harness\data_lake\catalog.py orca-harness\tests\test_data_lake_catalog.py
python -m pytest -p no:cacheprovider tests\test_data_lake_catalog.py
python -m pytest -p no:cacheprovider tests\test_data_lake_root.py tests\test_data_lake_catalog.py
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\header_index.py --strict
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_repo_map_freshness.py --changed --strict --message "repo-map-ack: Bronze Catalog AR-MGT-90 generated Attachment Record retrieval coverage is reflected in docs/workflows/orca_repo_map_v0.md for data_lake and runner rows; worktrees/ is transient local worktree infrastructure, not a repository source area."
git diff --check
python .agents\hooks\check_retrieval_header.py --staged --strict
```

Observed validation notes:

- `py_compile` exited 0.
- Focused catalog pytest exited 0 with `14 passed, 1 skipped`.
- Broader data lake root + catalog pytest exited 0 with `46 passed, 2 skipped`.
- Retrieval-header, header-index, map-links, repo-map freshness, staged retrieval-header, and `git diff --check` exited 0. `git diff --check` printed only Windows CRLF warnings for touched Python files.
- The implementation commit readback was `b85e2a3d Add Bronze Attachment Record catalog coverage`, and `git show --stat --shortstat --oneline -1` reported 3 files changed, 542 insertions, 34 deletions.

Independently rerun the validation commands you judge necessary. If you do not rerun a command, report that command as author-supplied and not independently revalidated. Do not run live capture, public web research, live lake mutation, network source access, Cleaning/ECR/Judgment materialization, Silver/Gold migration, or final Attachment Record storage migration.

## Review Scope

Attack these questions:

- Do generated Attachment Record IDs avoid positional `file_id` inheritance as the record key while still remaining stable and collision-resistant enough for this generated index?
- Does every generated record point back to an existing raw packet body by `packet_id`, `file_id`, `relative_packet_path`, `body_sha256`, and manifest hash without copying bodies or creating a second authority source?
- Does `load_attachment_record_body` fail closed on unsupported `body_ref_kind`, unsupported `hash_basis`, packet/path/sha drift, missing preserved files, and raw load failures?
- Are `attachment_records/all_attachment_records.jsonl`, `by_attachment_record`, `by_packet`, `by_source_family`, `by_source_surface`, `by_payload_kind`, and `by_body_sha256` deterministic, stale-detectable, and safely named?
- Do `source_surfaces.json` and per-surface rows expose AR coordination paths/counts without implying completeness, source-family validation, projection coverage, downstream currentness, or final AR physicalization?
- Does `_packet_index_entry` prevent private implementation fields such as `_attachment_records` from leaking into public packet catalog files?
- Does `inspect_catalog` compare expected and actual generated files honestly for missing, stale, orphaned, and read-failure cases, including the new AR files?
- Does generic `payload_kind` classification stay source-family-agnostic, or does it create a hidden lake-core field that should belong to a future registry?
- Are empty, malformed, multi-file, binary, same-source-surface/different-family, and unknown future source-family cases handled honestly?
- Do tests assert the behavioral contracts that would catch safe-name mismatches, raw resolver overtrust, stale AR output, and multi-file packet regressions?
- Does the repo-map wording describe retrieval coverage only, without overclaiming validation, readiness, source-of-truth promotion, Manifest v2, a body-copy store, or final AR storage architecture?

## Intended Closure Check

Treat these MGT-90/95 goals as claims to verify, not accepted truth:

- AR-01 typed generated entries: preserved raw body files now have discoverable generated AR rows with stable IDs and explicit field semantics.
- AR-02 raw authority preserved: records resolve through verified raw packet manifests and do not copy or mutate raw bodies.
- AR-03 coordination: downstream lanes can coordinate from source surface or packet to body records without semantic folder names.
- AR-04 future-lane adaptability: no source-family-specific lake-core fields are introduced for fragrance, Instagram, Reddit, YouTube, or future lanes.
- AR-05 honesty: generated files and docs name residuals clearly: not Manifest v2, not final AR physicalization, not payload validation, not downstream currentness.
- AR-06 regression coverage: tests cover stale/missing generated files, resolver byte reads, bad body refs, multi-file packets, future surfaces, and source-surface summaries.

For each, report one of:

- `closed`: implementation and tests now cover the failure mode.
- `partially_closed`: some protection exists but a material variant remains.
- `not_closed`: the original failure mode remains.
- `not_assessed`: source or environment prevented assessment.

If `partially_closed` or `not_closed`, include evidence and a minimum closure condition.

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness, acceptance, validation, or pass/fail verdict unless Orca overlay authority is supplied separately. Use findings-only advisory review. Do not emit `patch_queue_entry`; do not edit source files; do not commit, push, PR, merge, or run live capture/lake operations.

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

`docs/review-outputs/bronze_attachment_record_catalog_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: openai-gpt-5-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- open questions and residual risk
- validation commands run, skipped, or blocked
- intended closure check for AR-01 through AR-06
- review-use boundary: findings are decision input only, not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

After writing the report, fresh-read the written report path and return compact courier YAML in chat:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/bronze_attachment_record_catalog_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_merge | needs_architecture_pass | blocked
  reviewed_by: operator_to_fill
  authored_by: openai-gpt-5-codex
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  summary: ""
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: ""
```

Review findings are decision input only; they are not approval, validation, mandatory remediation, readiness, or executor-ready patch authority until the Chief Architect separately accepts or authorizes them.