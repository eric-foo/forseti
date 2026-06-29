# Silver Lineage Kit Enforcement Codex Cross-Vendor Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for an OpenAI/GPT-family (Codex) cross-vendor adversarial
  implementation/code review of the Silver lineage kit ENFORCEMENT implementation
  (PR #459): the generic Silver lineage helper/validator and its first adopter
  (transcript product mentions referencing the exact consumed transcript record).
use_when:
  - Commissioning a non-Anthropic reviewer to attack the Silver lineage enforcement code before it lands.
  - Checking whether the code faithfully and safely enforces the adjudicated genericity-check design (AR-01/AR-02) under adversarial attack.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: 48f3e3b43d6de4d73bc2609bb10737b6967c5860..558e8de506eb0f2f8706bcee5231cf055631c4d9
input_hashes:
  # git-blob (LF-normalized) sha256 of the design authority the code must honor.
  # Verify with `git show <commit>:<path> | sha256sum`, NOT raw Get-FileHash:
  # this worktree is autocrlf=true, so the working-tree file is CRLF and its raw
  # hash differs from the blob hash below.
  - docs/workflows/silver_lineage_kit_genericity_check_v0.md: sha256:57c2a67b9c4a9f2a34e130a253ee2459c8416c84aae82eca96af9acd42b5ba5f
  - docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md: sha256:1bd07a9027f77c6535fb4644fd04b5643034794eb0c759239987469e1cb477ef
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md: sha256:6891bc540ad9f9347f8a6569d45425657df47bbdc8f99813b123be73dcdf215f
prompt_carrier_note: >
  This prompt may be committed after the implementation commit. The implementation
  target under review ends at 558e8de506eb0f2f8706bcee5231cf055631c4d9; prompt-only
  carrier commits do not change the target unless they modify the named target files.
stale_if:
  - Any named target file changes after 558e8de506eb0f2f8706bcee5231cf055631c4d9 and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor is Anthropic/Claude-family but still claims cross_vendor_discovery (author is Anthropic/Claude here).
  - delegated-review-patch, review-lanes, prompt-orchestration, or the genericity-check design source changes.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 — constants bound; deltas stated below.

## Orca Prompt Preflight

- **authorization_basis**: current owner instruction to commission a delegated cross-vendor review of the Silver lineage enforcement code before landing PR #459.
- **objective / intended_decision**: decide whether PR #459's code is a faithful, safe, fail-closed enforcement of the adjudicated genericity-check design (especially AR-01 one-home and AR-02 row-locator), with no false-success path, no silent scope creep, and the IG deferral made a NAMED residual — i.e. whether it is safe to land.
- **output_mode**: `file-write` review prompt; the receiver's output mode is `review-report` filesystem-output to `docs/review-outputs/silver_lineage_kit_enforcement_codex_cross_vendor_adversarial_code_review_v0.md`.
- **template kind**: review; Orca-local implementation/code-review template is unbound, so this uses the prompt-orchestrator review frame plus Orca overlay bindings and the `cleaning_spine_enforcement_batch_claude_cross_vendor_adversarial_code_review_prompt_v0.md` precedent.
- **edit_permission / targets / branch**: reviewer is **read-only** on all source. Target worktree `C:\Users\vmon7\Desktop\projects\orca\worktrees\silver-lineage-enforcement`, branch `claude/silver-lineage-enforcement`, range `48f3e3b43d6de4d73bc2609bb10737b6967c5860..558e8de506eb0f2f8706bcee5231cf055631c4d9`. Dirty state allowed only for this prompt artifact or later prompt-carrier commits that do not touch the target files.
- **reviews**: findings-first. Advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or a patch queue.
- **doctrine_change_decision**: none. This prompt routes a review; it does not alter review, prompt, implementation, Cleaning, Capture, Data Lake, or Judgment doctrine.
- **isolation_decision**: neither (read-only review); reviewer inspects the named worktree in place.
- **destinations**: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/silver_lineage_kit_enforcement_codex_cross_vendor_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the Silver lineage **enforcement** change ending at commit `558e8de506eb0f2f8706bcee5231cf055631c4d9` (PR #459). This is a cross-vendor controller prompt intended for an **OpenAI / GPT-family (Codex)** reviewer. That family label is a who-constraint for de-correlation from the Anthropic/Claude-family author, not a runtime-model recommendation, rank, or selection rule.

This commission follows `workflow-delegated-review-patch` route-out, but the target is a **multi-file implementation/code diff**. Per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do **not** force this into the single-artifact delegated review-and-patch convention. Route it through implementation/code review instead: **the reviewer is read-only and must not patch source files.** Any fix is adjudicated and applied by the home model (Anthropic/Claude), not by the delegate. (This is why the commission is a "code review," not a "review-and-patch," despite the lane's design-doc precedent having granted single-artifact patch authority.)

Review purpose:

1. Independently attack the enforcement change for blocker/major correctness, scope, validation, source-boundary, or false-confidence issues.
2. Verify whether the intended enforcement is actually enforced by code and tests (see Intended Enforcement Closure Check).
3. Scan only the touched implementation scope for newly visible blocker/major issues. Minor findings are allowed; do not widen into unrelated Cleaning, Capture, Data Lake, scheduler, product-proof, or Judgment review.

## Actor And De-Correlation Receipt

- `author_home_model_family`: Anthropic / Claude-family (Opus), recorded from the authoring lane. The code under review was authored by Claude; the home/adjudicating model is also Claude.
- `controller_model_family`: OpenAI / GPT-family (Codex), if and only if the receiving reviewer is actually GPT-family.
- `current_receiving_actor_role`: controller.
- `dispatch_mode`: external-controller-courier.
- `de_correlation_status`: `cross_vendor_discovery` only if the reviewer is OpenAI/GPT-family and the author family remains Anthropic/Claude; otherwise set `same_vendor_sanity` or `self_fallback` and do not claim cross-vendor discovery.
- No runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-code-review` and `workflow-deep-thinking` if available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce a findings-first implementation/code review.
5. If `workflow-code-review` is unavailable, use its zero-config findings-only advisory semantics from this prompt, and mark strict review claims `NOT_CLAIMED`.

## Required Reads

Authority and boundary first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`

Design authority the code must honor (verify blob hashes per `input_hashes`):

- `docs/workflows/silver_lineage_kit_genericity_check_v0.md` — the adjudicated design (Required v0 Grammar, Relationship to the Common Record Header, Agent Use Contract, Accepted Residuals).
- `docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md` — AR-01..AR-06 rationale.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` — Common Record Header (the single persisted home for `raw_refs`/`derived_refs`).

Review target (the change under review):

- `orca-harness/data_lake/silver_lineage.py` (NEW)
- `orca-harness/cleaning/transcript_product_lake.py`
- `orca-harness/cleaning/transcript_product_extractor.py`
- `orca-harness/runners/run_transcript_product_extract.py`
- `orca-harness/tests/unit/test_silver_lineage.py` (NEW)
- `orca-harness/tests/unit/test_transcript_product_lake.py`

Adjacent implementation context as needed (do not widen the review target):

- `orca-harness/data_lake/root.py` — `append_record_set` writes a completion marker committing each member's `member_sha256`; `read_record_set_member_sha256` reads it back fail-closed.
- `orca-harness/cleaning/models.py` — `CleaningProjectionRef.row_id`/`row_kind` (the row-locator precedent), `CleaningRawAnchor` dual preserved-file/derived-record anchor precedent.
- `orca-harness/source_capture/transcript/asr_packet.py` — writes the `transcript_asr` derived record via `append_record_set` (record_id grammar, provenance).
- `orca-harness/schemas/case_models.py` — `StrictModel` (`extra="forbid"`).
- `orca-harness/runners/run_ig_reels_product_extract.py` — the OTHER caller of the shared driver, deliberately left unadopted (Patch 3); confirm it is genuinely unaffected.

## Target Diff And Dirty-State Allowance

Implementation target range:

```text
48f3e3b43d6de4d73bc2609bb10737b6967c5860..558e8de506eb0f2f8706bcee5231cf055631c4d9
```

Reviewed diff: `git diff 48f3e3b43d6de4d73bc2609bb10737b6967c5860..558e8de506eb0f2f8706bcee5231cf055631c4d9 -- <the six target files>` (the single commit `558e8de5`, +684/-11). The base `48f3e3b4` is `codex/silver-lineage-kit` (PR #454 head); the genericity-check design source is present at that base.

Verify before review:

```text
git -C <worktree> rev-parse HEAD                # expect 558e8de506eb0f2f8706bcee5231cf055631c4d9
git -C <worktree> status --short --branch
git show 48f3e3b4:docs/workflows/silver_lineage_kit_genericity_check_v0.md | sha256sum   # expect 57c2a67b...
```

Hash note (load contract): this worktree is `core.autocrlf=true`, so design-source files are CRLF on disk and a raw `Get-FileHash` will NOT match `input_hashes`. Compare the **git-blob** hash via `git show <commit>:<path> | sha256sum` (or compare blob OIDs with `git rev-parse <commit>:<path>`). If a target file changed after `558e8de5`, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only on explicit operator authorization.

## Validation Evidence To Inspect

The author observed, from `orca-harness/`, with `ORCA_DATA_ROOT` unset:

```bash
env -u ORCA_DATA_ROOT python -m pytest tests/unit tests/contract -q
```

Result: process exit code `0` (no failures); progress reached 100% with one skip (the live-lake YouTube-creator-observation ledger test, which self-skips when `ORCA_DATA_ROOT` is unset). The exact pass count was not captured (terminal truncation); exit 0 is the pass signal. The 40 tests in `test_silver_lineage.py` + `test_transcript_product_lake.py` passed explicitly.

Environment caveat: with `ORCA_DATA_ROOT` **set** to a live lake, two unrelated tests fail — `test_run_source_capture_packet_lake.py::test_cli_requires_exactly_one_target` and `test_youtube_creator_observation_ledger.py::...live_lake_refs_when_available` (`live_lake_root_uuid_mismatch`). Both are environmental (a bound live `F:` lake) in `source_capture`/`capture_spine`, untouched by this change; they vanish when `ORCA_DATA_ROOT` is unset. Do not treat them as implementation failures.

Reviewer rerun guidance:

```bash
# bash:
env -u ORCA_DATA_ROOT python -m pytest tests/unit/test_silver_lineage.py tests/unit/test_transcript_product_lake.py -q
# PowerShell:
# Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; python -m pytest tests\unit\test_silver_lineage.py tests\unit\test_transcript_product_lake.py -q
```

If you do not rerun, report validation as author-supplied and not independently revalidated. Do not run live capture, network, scheduler, storage/Data-Lake, or Judgment code.

## Review Scope

Attack these questions:

- **AR-01 (one home).** Does `SilverLineage.to_record_fields()` emit only TOP-LEVEL header-shaped fields and never a nested `silver_lineage` object? When the driver merges it into the product-mention payload, is there exactly one home for `raw_refs`/`derived_refs` (no nested duplicate, no second persisted store)? Does it avoid emitting a record-level `schema_version` that would falsely claim the product-mention record is a full `silver_vault_record_v0` Common Record Header record? Is `lineage_schema_version` an honest, non-clobbering marker?
- **Exact identity (the gap closure).** Does the runner capture the REAL consumed `transcript_asr` `record_id` (the actual file name) and the actual record-bytes sha256 — not a guess or a reconstructed id? Is the caption `raw_ref` built from the actual json3 preserved file's `file_id` + manifest sha256 + `relative_packet_path`? Could a same-shortcode / same-anchor collision still produce an ambiguous reference?
- **Hash basis correctness.** Is `derived_record_bytes` sha256 (hash of the record file the runner read) equal to the lake's committed `member_sha256` for that record? Is `raw_stored_bytes` sha256 the manifest's preserved-file hash? Any path where the persisted sha256 would not actually verify against the referenced bytes?
- **Fail-closed (no fake success).** Can an invalid/empty lineage be constructed or persisted? Are the model validators correct (ref-or-limitation; rawless requires a limitation; derived_ref exact lane+record_id; raw_ref hash-checkability; row_locator both-or-neither; `other` limitation requires detail)? Does the write-boundary re-validation (`validate_silver_lineage`) actually run before persist, and would a mutation between build and persist be caught?
- **AR-02 (row locator).** Is `row_locator` structurally expressible on `derived_refs` and consistency-enforced? Is it correctly OPTIONAL for the transcript adopter (a `transcript_asr` record is not a multi-row projection), while remaining available for a future projection adopter? Is the deferral of "require row_locator for projection-sourced multi-row facts" a named residual rather than a silent gap?
- **Additive / no-regression.** Is `TranscriptInput.source_lineage` genuinely optional (default `None`), so the IG runner and existing callers are unaffected? Does a no-lineage record write cleanly with NO lineage fields (no empty/fake lineage block)? Is the IG (Patch 3) deferral a NAMED residual, and does the shared driver still behave correctly for the unadopted caller?
- **Scope boundary.** Does the change avoid historical lake rewrite, a universal record-wrapper migration, global `DataLakeRoot.append_record` gating, a Silver Vault schema redesign, and any live F-drive write? Is everything additive?
- **Layering / imports.** Is `data_lake/silver_lineage.py` free of cycles (imports only `schemas`/`pydantic`; no `cleaning`/`data_lake.root` back-edge)? Does threading lineage through `runners/` introduce any LLM-SDK import into the no-LLM zone (the `test_no_llm_imports` contract)?
- **Test adequacy.** Do tests prove the end-to-end exact-reference resolution (the persisted record's `derived_ref` resolves to a real committed record AND its sha256 verifies), not just construct-and-assert? Are the validator's negative paths covered? Is backward-compat (no-lineage) covered? Any assertion that would pass even if the enforcement were broken (a weak/tautological test)?
- **Pydantic edge cases.** `StrictModel` `extra="forbid"` behavior; `model_dump(mode="json")` null handling; `SilverAnchor` file-vs-specific-kind rules; Literal/enum rejection of unknown values; any field that should be rejected but is silently accepted (or vice versa).

## Intended Enforcement Closure Check

Treat these as claims to verify, not accepted truth. For each, report `closed` | `partially_closed` | `not_closed` | `not_assessed`, with evidence and (if not closed) a minimum closure condition.

- **C-01 (AR-01 one home):** lineage is persisted as top-level header-shaped fields with exactly one home for `raw_refs`/`derived_refs`; no nested `silver_lineage` block; no false full-header claim.
- **C-02 (exact identity):** the product-mention record references the EXACT consumed transcript record (ASR `transcript_asr` lane + real `record_id` + verifiable sha256) or the exact caption raw file — closing same-shortcode ambiguity.
- **C-03 (AR-02 row locator):** the grammar can express `row_id`/`row_kind`, consistency-enforced, correctly optional for the transcript case.
- **C-04 (fail-closed):** invalid lineage cannot construct or persist; write-boundary re-validation runs; no fake-success path.
- **C-05 (additive / no-regression):** `source_lineage` optional; IG runner unaffected; no-lineage path writes with no lineage fields; deferral is a named residual.
- **C-06 (scope):** no historical migration, no universal wrapper, no global `append_record` gating, no schema redesign, no live writes.

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness, acceptance, validation, or pass/fail verdict unless Orca overlay authority is supplied separately. Use findings-only advisory review. Do not emit `patch_queue_entry`; do not edit source files; do not stage, commit, push, open/update PRs, merge, or run live capture. Flag off-scope issues as findings only.

If you find no blocker or major issue, say so and state residual risks or validation gaps. If you find an issue, findings lead the report and each must include:

- finding id
- severity `blocker` | `major` | `minor` (prioritization only, not formal Orca verdict authority)
- target file and stable line/anchor
- evidence from the implementation
- authority or evidence basis (design source / contract / overlay)
- concrete impact
- minimum closure condition
- next authorized action
- validation expectation

Escalation valve: if the change is design-level wrong rather than patchably rough, say so in findings and recommend the home model return to design, leaving no patch.

## Output Contract

Write the full review report to:

`docs/review-outputs/silver_lineage_kit_enforcement_codex_cross_vendor_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill_codex_identity`
- `authored_by: anthropic-claude-opus`
- `de_correlation_bar: cross_vendor_discovery` only if the reviewer is OpenAI/GPT-family; otherwise `same_vendor_sanity` or `self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- the C-01..C-06 intended enforcement closure table
- open questions and residual risk
- validation rerun status
- strict-only blockers and non-claims
- the `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block

Do not write outside that report path. If the report path already exists, stop and report `BLOCKED_OUTPUT_DESTINATION_COLLISION` unless the operator explicitly provides a new output path.

## Delegated Code Review Return Courier

Append this block at the end of the report:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission / review target (PR #459, range 48f3e3b4..558e8de5)
- implementation context, diff, and reviewed files
- findings and implementation evidence (file:line anchors)
- C-01..C-06 intended enforcement closure statuses
- citations (design source / contract / overlay)
- reviewer verdict (no formal Orca PASS/readiness claimed)
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
- explicit note: reviewer is read-only; the home model (Claude) adjudicates and applies any fix
```
