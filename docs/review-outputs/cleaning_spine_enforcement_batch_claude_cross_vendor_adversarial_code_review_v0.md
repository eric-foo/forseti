# Cleaning Spine Enforcement Batch — Claude Cross-Vendor Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Cross-vendor advisory implementation/code review of the Cleaning spine enforcement batch.
use_when:
  - Adjudicating Claude's review findings for the Cleaning spine enforcement batch.
  - Checking closure evidence for projection refs, ambiguous anchors, and typed ECR receipts.
authority_boundary: retrieval_only
```

```yaml
artifact_role: Implementation/code review output (advisory, findings-first)
review_type: cross_vendor_adversarial_implementation_review
reviewed_by: claude-opus-4.8   # self-reported reviewing model; operator/CA may confirm on the durable record
authored_by: gpt-family-codex
de_correlation_bar: cross_vendor_discovery   # Anthropic/Claude reviewer vs OpenAI/GPT-family Codex author; author family != reviewer family
same_vendor_rationale: not_applicable   # only required when de_correlation_bar == same_vendor_sanity
dispatch_mode: external-controller-courier
current_receiving_actor_role: controller
implementation_under_review: 0ad2292c4d13e76597c5191d9157503c780a5145..db0bcdfb6d9279f53f49195fbbea2d9572bc564a
target_worktree: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation
target_branch: codex/cleaning-spine-continuation
review_authority: advisory_findings_only   # no formal PASS / readiness / acceptance / patch-queue authority
strict_review_claims: NOT_CLAIMED
overall_verdict: ADVISORY_CHANGES_RECOMMENDED   # no blocker; two majors (enforcement-coverage/fail-closed gaps); E-03 strong
```

## Actor And De-Correlation Receipt

- `author_home_model_family`: OpenAI / GPT-family Codex (recorded from the authoring lane; not independently verified by this reviewer beyond the prompt's recorded provenance).
- `controller_model_family`: Anthropic / Claude-family (this reviewer is Claude Opus 4.8).
- `de_correlation_status`: `cross_vendor_discovery` — author family (GPT) and reviewer family (Claude) differ. This is a who-constraint for de-correlation, **not** a runtime-model recommendation, rank, or selection rule.
- No runtime model recommendation is made by this review.

## Source-Gated Method Contract — Disposition

1. **Reference-load.** `workflow-code-review` and `workflow-deep-thinking` are available as skills in this environment. Their contracts (findings-first advisory; zero-config when no formal review lane is bound; frame material failure modes before listing findings) were in-context and applied inline per the Operating Economy ("load each skill once per thread … apply it"). No strict/formal review claims are emitted.
2. **Source reads.** Required Orca authority + boundary files and the review target were read (ledger below).
3. **Readiness.** `SOURCE_CONTEXT_READY` — declared below.
4. **Apply.** Deep-thinking failure-mode framing applied first; then findings-first advisory implementation review.
5. **Fallback.** `workflow-code-review` was available; zero-config findings-only advisory semantics used because no formal Orca implementation-review lane is bound to this commission. Strict review claims marked `NOT_CLAIMED`.

## Git / Target-State Verification (fresh reads)

- Target worktree HEAD: `df0dcf40` (`Add Cleaning enforcement batch review prompt`). This is the **only** commit after the target tip `db0bcdfb`; it is the prompt carrier and **does not touch** the six target files (`git diff --stat db0bcdfb..HEAD -- <6 targets>` returned empty). No target-file drift.
- Working tree: clean.
- Target range `0ad2292c..db0bcdfb` touches exactly the six named target files (verified via `git diff --stat`): `ecr/__init__.py`, `ecr/models.py`, `runners/run_capture_ecr_cleaning_smoke.py`, `runners/run_cleaning_spine_periodic_audit.py`, `tests/unit/test_capture_ecr_cleaning_smoke_runner.py`, `tests/unit/test_ecr_models.py`. No retarget needed.
- Output destination `docs/review-outputs/cleaning_spine_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md` did **not** exist at review start (collision check passed); this report is the first write.
- Optional orientation doc `docs/hygiene/cleaning_spine_lane_handoff_v0.md`: **ABSENT**. Reported and continued per prompt instruction; not blocking.

## Source-Read Ledger

**Read directly by the reviewing actor (claude-opus-4.8):**

- Reviewed diff (all six target files), full unified diff of `0ad2292c..db0bcdfb`.
- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` — main assembly loop (≈126–176), retail entry (≈238–320), reddit entry + comment enumeration (≈323–430), `_reddit_handle` (≈666–715), `_derive_ecr_receipt` (≈759–795), `_retail_anchor_unverified_reason` (≈865–886).
- `orca-harness/runners/run_cleaning_spine_periodic_audit.py` — status computation + `overall_status` (≈162–204), `_lane_status` / `BLOCKING_SEVERITIES` (≈1459–1465), Lane A hook into projection-ref + `_build_projection_row_index` (≈298–320, 587–665), `_verify_cleaning_projection_ref` (≈666–730), `_verify_cleaning_packet_traceability` hook (≈791–804), Lane B cleaning breakpoint (≈470–527), `_specific_anchor_issue` (≈982–1055), `_promote_smoke_summary_findings` (≈1060–1104), `_load_ecr_receipt_artifact` (≈1445–1449).
- `orca-harness/ecr/models.py` — new models `EcrSourceSidePostures` / `EcrSourceSideClears` / `EcrSourceSideReceipt` / `EcrSourceSideReceiptArtifact` (diff).
- `orca-harness/tests/unit/test_ecr_models.py`, `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` (diffs).
- `orca-harness/cleaning/models.py` — `CleaningProjectionRef` (141–164), `CleaningInputHandle.projection_ref` default None (181–216), `CleaningRawAnchor.validate_anchor_specificity` (101–138).
- `orca-harness/cleaning/projection.py` — `cleaning_input_handle_from_projection_row` projection_ref population (14–55), `cleaning_input_handles_from_projection_rows` (59–81).
- `orca-harness/source_capture/retail_pdp_projection.py` — row model + `validate_counts` (142–153), variant rows vs bindings (350–394).
- `orca-harness/source_capture/ig_projection.py` — row model + `validate_counts` (no row_id-uniqueness check) (≈118–140).
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` (full).
- `docs/workflows/ecr_spine_submap_v0.md` (full).
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (purpose + decision/ownership table, 1–120).
- `.agents/workflow-overlay/review-lanes.md` (full).

**Read via a de-correlation-preserving delegated reader (Claude-family worker subagent; constraint extraction folded in):**

- `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/validation-gates.md`, `.agents/workflow-overlay/safety-rules.md`, `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`, `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`.

**Absent / not read:** `docs/hygiene/cleaning_spine_lane_handoff_v0.md` (absent).

## SOURCE_CONTEXT_READY

`SOURCE_CONTEXT_READY` — required authority, boundary, and target sources were read; no unresolved conflicts block the review. Two qualifications, neither blocking:

- Authority/overlay/cleaning-contract files (9) were read via a delegated Claude-family reader and folded in as constraints, not re-attested line-by-line by the controller. De-correlation (author=GPT vs reviewer=Claude) is preserved.
- ECR posture deriver internals (`ecr/deriver.py`) and `source_capture/reddit_consolidation/consolidator.py` were treated as adjacent context: behavior was inferred from the smoke runner's call sites, the test fixtures, and the green test reruns rather than read in full. This bounds the confidence of F-05 (noted there).

---

## Findings (findings-first)

No **blocker** found. Two **major** findings concern enforcement *coverage* and *fail-closed* gaps (the prompt's explicit attack axes: false confidence, hidden source-family adapter gaps, fail-closed on ambiguity). Neither is a data-corruption or false-success path; the retail end-to-end path is correct and tests reproduce green.

### F-01 — Reddit projection-ref enforcement is unwired; the audit's Reddit row-index branch is unreachable in the live pipeline (major)

- **Target:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` `_reddit_handle` (≈700–715); `orca-harness/runners/run_cleaning_spine_periodic_audit.py` `_build_projection_row_index` reddit branch (≈624–657) + `needed_packet_ids` gate (≈302–311, 589–601) + `_verify_cleaning_projection_ref` early-return (≈672–673).
- **Evidence:**
  - `_reddit_handle` constructs `CleaningInputHandle(handle_id=…, source_family=…, source_surface=…, raw_anchor=…, ecr_ref=…)` with **no `projection_ref`**. `CleaningInputHandle.projection_ref` defaults to `None` (`cleaning/models.py:186`). Retail and IG handles, by contrast, get `projection_ref` from `cleaning_input_handle_from_projection_row` (`cleaning/projection.py:44–54`).
  - The audit derives `projection_ref_packet_ids` from `{handle.projection_ref.packet_id for handle … if handle.projection_ref is not None}` and passes it as `needed_packet_ids`. `_build_projection_row_index` skips any source entry whose packet_id is not in `needed_packet_ids` (`if packet_id not in needed_packet_ids: continue`). Because no Reddit handle carries a `projection_ref`, no Reddit packet_id ever enters `needed_packet_ids`, so the `elif entry["source_type"] == "reddit":` branch never executes in the normal flow.
  - `_verify_cleaning_projection_ref` returns immediately for `projection_ref is None`, so every Reddit handle is skipped by E-01.
- **Authority/basis:** Projection doctrine **OD-1** (`…projection_doctrine_v0.md` §11) makes `projection_ref` *optional* ("a single input handle keyed to raw that **may** attach projection and ECR references **when present**"), so Reddit-without-projection_ref is doctrinally permitted. The defect is the mismatch between **claimed/apparent coverage and delivered coverage**: the commission's E-01 scope question explicitly names "retail/PDP, IG, and **Reddit-shaped artifacts**," and the audit ships a full Reddit row-reconstruction branch (post + `comment_{i:04d}` rows, packet_id cross-check) that implies Reddit coverage it does not deliver. This is the prompt's named attack axis "hiding source-family-specific adapter gaps."
- **Impact:** Reddit cleaning handles receive **no** row-level projection-ref resolution. The Reddit branch of `_build_projection_row_index` is unreachable dead code under the live pipeline, is untested, and produces false confidence that Reddit row→raw resolution is enforced. (Reddit handles still get raw-anchor specificity checks via `_verify_cleaning_raw_anchor` / the old-reddit fullname pattern, so Reddit is not wholly untraced — but it is not traced by *this* mechanism.) Note the Reddit reconstruction logic is otherwise *consistent* with the producer (`enumerate(comments, start=1)`, explicit `row_id` else `comment_{i:04d}`, `reddit_thread_consolidation.comments` nesting) — so if it were wired, it would likely resolve; the gap is purely that nothing references it.
- **Minimum closure condition:** Either (a) Reddit cleaning handles carry a `projection_ref` (consolidation-as-projection) so the audit's Reddit branch actually resolves row_ids, **and** a Reddit-path projection-ref test (positive + row-miss) is added; **or** (b) if Reddit is intentionally projection-ref-free, the unreachable Reddit branch in `_build_projection_row_index` is removed or guarded, and the residual "Reddit row→raw resolution is anchor-based only, not projection-ref enforced" is recorded.
- **Next authorized action:** Owner / home-model decision on whether Reddit must carry a `projection_ref`. Reviewer is read-only; no source edit performed.
- **Validation expectation:** Closure (a) verified by a new failing-without-fix Reddit projection-ref unit test; closure (b) verified by removal of the dead branch + a no-coverage residual note and unchanged green suite.

### F-02 — Projection row index silently collapses duplicate/ambiguous `row_id`s; does not fail closed on structurally ambiguous projections (major)

- **Target:** `orca-harness/runners/run_cleaning_spine_periodic_audit.py` `_build_projection_row_index` (retail branch ≈608–615; IG branch ≈617–623): `row_index[packet_id] = {row.row_id: str(row.row_kind) for row in projection.rows}`.
- **Evidence:** The row index is a dict comprehension keyed by `row.row_id`. Two projection rows sharing a `row_id` collapse silently (last-wins) with no finding. Neither projection model enforces `row_id` uniqueness: `RetailPdpProjectionPacket.validate_counts` (`retail_pdp_projection.py:147–153`) checks only `preserved_evidence_rows == len(rows)` and binding counts; `IgCreatorMomentumProjectionPacket.validate_counts` (`ig_projection.py`) checks only `preserved_metric_rows == len(rows)` and empty bindings. So duplicate `row_id`s are admissible by the model and silently deduped by the verifier.
- **Authority/basis:** The commission's E-01 scope explicitly asks whether the check "fail[s] closed when the projection artifact … contains **duplicate or structurally ambiguous row ids**." Projection doctrine treats `row_id` as a back-reference anchor key (`…projection_doctrine_v0.md` §4 `rows[]` with `row_kind`), which implies a uniqueness invariant the audit relies on but does not enforce or assert.
- **Impact:** A structurally ambiguous projection (duplicate `row_id`s) is undetected; the `row_kind` cross-check in `_verify_cleaning_projection_ref` can be defeated by collapse (a handle pointing at a duplicated `row_id` resolves to whichever row survived, possibly masking a `row_kind` mismatch). **Exploitability is unconfirmed**: retail `row_id`s are constructed to be unique per slice in practice (`{slice}:{retailer}:pdp`, `…:review_substrate`, one variant row per slice), but module rows (`{slice}:{retailer}:module:{module_type}`) could collide if a slice carries two modules of the same `module_type`, and there is no model invariant preventing it. No duplicate-producing fixture was demonstrated in this pass.
- **Minimum closure condition:** When building the row index, detect duplicate `row_id`s and emit a finding (e.g., `projection_row_index_ambiguous`, major) instead of silently collapsing; **or** establish and rely on a model-enforced `row_id`-uniqueness invariant on the projection packets and assert it at index build.
- **Next authorized action:** Owner / home-model decision. Reviewer read-only; no edit.
- **Validation expectation:** A unit test that feeds a projection with two same-`row_id` rows and asserts a duplicate-ambiguity finding (or a model `ValidationError`), rather than a silent resolve.

### F-03 — IG (reachable) and Reddit (unreachable) projection-ref/row-index branches are untested; only retail is exercised (minor)

- **Target:** `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` (the only projection-ref tests — `test_periodic_audit_flags_cleaning_projection_ref_row_unresolved`, `test_periodic_audit_flags_cleaning_text_pattern_anchor_ambiguity` — use retail fixtures); `run_cleaning_spine_periodic_audit.py` `_build_projection_row_index` instagram branch (≈617–623).
- **Evidence:** No test exercises the `instagram` or `reddit` branches of `_build_projection_row_index`. IG handles **do** carry `projection_ref` (shared builder), so the IG branch is reachable but unverified; the Reddit branch is both unreachable (F-01) and untested.
- **Impact:** IG-specific index construction (`IgCreatorMomentumProjectionPacket.model_validate`, the `projection.packet_id != packet_id` mismatch path, row iteration) can regress undetected; the retail test does not cover it because the source-type branch differs.
- **Minimum closure condition:** Add an IG projection-ref resolution test (positive resolve + a row-miss negative producing `cleaning_projection_ref_row_unresolved`). Reddit coverage is decided under F-01.
- **Next authorized action:** Advisory; owner/home-model decision on added coverage. Reviewer read-only.
- **Validation expectation:** New IG test fails before the relevant code path is correct and passes after; suite stays green.

### F-04 — New ECR receipt model is strict-read; legacy/loose v0 receipt artifacts would be rejected with no lenient-read or migration path (minor / residual)

- **Target:** `orca-harness/ecr/models.py` `EcrSourceSideReceiptArtifact` (`schema_version: Literal["…v0"]`, `receipts: Field(min_length=1)`, `non_claims: Field(min_length=1)`) + per-receipt `validate_receipt_contract` (exact `ref_id` coupling, `clears` equality); `run_cleaning_spine_periodic_audit.py` `_load_ecr_receipt_artifact` (≈1445–1449) does full strict `model_validate`.
- **Evidence:** The audit now reads ECR receipts strictly: exact `schema_version` Literal, non-empty `receipts`/`non_claims`, exact `ecr:<packet_id>:source_side_postures` coupling, and `clears`-equals-recomputed-aggregate. The inherited ECR schema-evolution posture (`ecr_spine_submap_v0.md` invariant 4) is **"lenient-read / strict-admit"** (read-checked `_vN`, additive enum growth); this load path is strict-*read*.
- **Impact:** For an audit gate, strict-read is **defensible** — the gate's job is to fail closed on drift. But any committed/legacy `ecr_source_side_receipts.json` valid under the old loose dict (e.g., empty `receipts` from a zero-source manifest, empty `non_claims`, or a receipt lacking the exact `ref_id` coupling) would now hard-fail at load (`lane_a_ecr_receipts_invalid`), and a future `_v1` receipt schema would be rejected outright rather than lenient-read. Live risk is low because the smoke runner regenerates the artifact each run and the tests regenerate fresh.
- **Minimum closure condition:** Confirm no committed/legacy v0 receipt artifact relies on the old loose shape; record the strict-admit-on-read posture as an intentional audit-gate choice (and, if forward-compat reads of a future `_vN` are wanted, add a lenient-read path).
- **Next authorized action:** Advisory; owner/home-model confirmation. Reviewer read-only.
- **Validation expectation:** A grep/inventory of persisted `ecr_source_side_receipts.json` artifacts shows none with empty `receipts`/`non_claims` or non-coupled `ref_id`; otherwise a migration note is added.

### F-05 — Receipt packet-binding is enforced only for identity/source_visibility postures, not inspectability/timing (minor / residual)

- **Target:** `orca-harness/ecr/models.py` `EcrSourceSideReceipt.validate_receipt_contract` — packet_id cross-check loops over `self.postures.identity` and `self.postures.source_visibility` only.
- **Evidence:** Per the test fixture shapes, `identity` and `source_visibility` postures carry `packet_id`; `inspectability` and `timing` postures are keyed by `slice_id` and carry **no** `packet_id`. The receipt therefore cannot (and does not) bind inspectability/timing postures to its `packet_id`. A receipt could carry inspectability/timing postures whose slices belong to a different packet, undetected by the contract.
- **Impact:** Defense-in-depth gap on **tampered/hand-crafted** receipts only. In the live producer, all four posture lists are derived from the same `packet` in `_derive_ecr_receipt` (`run_capture_ecr_cleaning_smoke.py:759–795`), so the live flow is not affected. (Confidence bounded: `ecr/deriver.py` internals were inferred from call sites + fixtures + green reruns, not read in full.)
- **Minimum closure condition:** If stronger tamper-resistance is desired, bind inspectability/timing postures to the packet by validating their `slice_id`s against the packet's slice set; otherwise record the residual that those posture kinds are packet-bound only transitively via the producer.
- **Next authorized action:** Advisory; owner/home-model decision. Reviewer read-only.
- **Validation expectation:** Optional negative test: a receipt with a foreign-packet inspectability/timing slice is rejected (only if closure path (a) is chosen).

### Minor test-coverage note (not a separate numbered finding)

`test_source_side_receipt_rejects_clear_mismatch` exercises only the *aggregate-wrong-while-all-postures-clear* case. The model's `all(...)` recomputation also covers the *one-posture-false-while-aggregate-true* path, but that path is not directly tested. Low risk (the recompute is symmetric); a one-line fixture variant would close it.

---

## Intended Enforcement Closure Check

| ID | Enforcement claim | Status | Basis |
| --- | --- | --- | --- |
| **E-01** | Every Cleaning `projection_ref.row_id` resolves inside the named projection artifact (retail/PDP, IG, Reddit) | **partially_closed** | Closed + tested for **retail**; wired but **untested** for **IG** (F-03); **not delivered** for **Reddit** — handles carry no `projection_ref`, audit Reddit branch unreachable (F-01). Fail-closed on absent/malformed projection works (`projection_row_index_unavailable` → `cleaning_projection_ref_packet_unresolved`, both major). Fail-closed on **duplicate/ambiguous row_ids does not** (F-02). |
| **E-02** | Duplicate raw `text_pattern` anchors are flagged so cleaned text does not imply stronger traceability than raw supports | **closed** (with severity-calibration residual) | The "silently implies precise traceability" failure mode is closed: ambiguity is now a distinct signal (`text_pattern_ambiguous_in_raw` in the smoke summary; `cleaning_text_pattern_anchor_ambiguous` + `occurrence_count` in the audit). It is **not** advisory-only — a `minor` finding drives `_lane_status` → `warn` → `overall_status` `warn` → nonzero exit (`_lane_status`:1459–1465; status calc:168–174). Audit-level `_specific_anchor_issue` is anchor-kind-based, so it covers IG/Reddit `text_pattern` handles too. The empty-`anchor_value` `count(b"")` edge is neutralized by `CleaningRawAnchor.validate_anchor_specificity` requiring non-empty `anchor_value` for `text_pattern`. **Residuals:** ambiguity is `minor`/warn-level by design (not a fail-gate — confirm calibration is intended); smoke-*producer*-side ambiguity detection is retail-anchor-only (`_retail_anchor_unverified_reason`), so IG/Reddit ambiguity surfaces only at audit time. |
| **E-03** | ECR receipt artifacts are typed Pydantic models with required posture kinds, required clear aggregation, packet/ref coupling, duplicate-key rejection | **closed** (with residuals F-04, F-05) | `EcrSourceSidePostures` requires all four kinds non-empty (`min_length=1`); `EcrSourceSideReceipt` enforces exact `ecr:<packet_id>:source_side_postures` `ref_id`, recomputes and equality-checks `clears`, and rejects blank fields; `EcrSourceSideReceiptArtifact` requires non-empty `receipts`/`non_claims`, exact `schema_version` Literal, and unique `(packet_id, ref_id)` keys. Smoke runner constructs via the schema (no loose dict). Audit validates **both** Lane A and Lane B receipts via `_load_ecr_receipt_artifact`. Negative tests present: missing posture kind, clear mismatch, ref-packet mismatch, duplicate keys, audit invalid-shape. Residuals: strict-read posture (F-04); inspectability/timing not packet-bound (F-05). |

## Lane / Boundary Assessment

- **Cleaning stays in its lane.** The diff introduces no credibility, independence, salience, demand, exclusion, Decision Strength, Action Ceiling, or other Judgment vocabulary. The `clears` booleans (`clears_identity`/`clears_inspectable`/`clears_pre_cutoff`/`clears_source_visibility`) are mechanical posture aggregations, not Judgment labels — consistent with the data/cleaning boundary table (Cleaning owns "raw-to-cleaned traceability"; must not own credibility/discounting/integrity/strength/ceiling) and the cleaning foundation's forbidden-reason list.
- **No-network / bounded.** The reviewed code operates over existing packet/projection/consolidation/smoke artifacts; no live capture, network, crawler, scheduler, API/dashboard, storage/Data-Lake, product-proof, or Judgment-readiness paths are introduced or invoked.
- **Residual-visibility check (prompt attack axis "does any enforcement make a known residual invisible?").** No found instance of a failed/blocked capture handle being laundered into a clean Cleaning handle. The closest concern is the *inverse* — F-01's unreachable Reddit branch creates a false impression of coverage, which the closure condition addresses.

## Open Questions And Residual Risk

1. **Is Reddit intended to carry a `projection_ref`?** (F-01.) If yes → producer wiring + test is the fix. If no → the audit's Reddit branch is dead code that should be removed/guarded and the residual recorded. This is the single load-bearing owner/home-model decision.
2. **Should ambiguous anchors gate harder than `warn`?** (E-02 residual.) Current behavior: `minor` → `warn` → nonzero exit, but not `fail`. Confirm warn-level is the intended calibration for "traceability ambiguity" vs. "absence" (`major` → `fail`).
3. **Can any projection family emit duplicate `row_id`s?** (F-02.) No model invariant prevents it today; the audit silently collapses. Exploitability unconfirmed.
4. **Are there persisted legacy v0 receipt artifacts under the old loose shape?** (F-04.) If any exist with empty `receipts`/`non_claims` or non-coupled `ref_id`, the audit will now reject them.
5. **Confidence bound:** `ecr/deriver.py` and `reddit_consolidation/consolidator.py` were not read in full; F-05 and the Reddit-consistency claim in F-01 rest on call sites + fixtures + green reruns.

## Validation Rerun Status (independently revalidated)

Reran in the target worktree (`orca-harness/`), workspace-local write permission, no network:

- Targeted suite (author's command): `pytest … tests/unit/test_ecr_models.py tests/unit/test_capture_ecr_cleaning_smoke_runner.py -q` → **50 passed** (`..................................................`), matching the author's observed output.
- Broader no-network suite (16 files: ECR models/derivers, smoke runner, cleaning core, cleaning projection integration, IG/retail projection, reddit consolidation) → **210 passed** (`72/72/66` per the progress bars), matching the author's observed output.
- `python -B runners/run_capture_ecr_cleaning_smoke.py --help` → exit 0; `python -B runners/run_cleaning_spine_periodic_audit.py --help` → exit 0.
- The restricted-sandbox `_scratch` `PermissionError` the author noted was not reproduced here (runs used workspace-local writes; `tmp_path`-based tests). No code error independent of sandbox ACLs was observed.

Validation is therefore **independently reproduced green** for the committed batch. Note (validation-gate honesty): green tests confirm the *implemented* behavior; they do not exercise the gaps in F-01 (no Reddit projection-ref test), F-02 (no duplicate-row_id fixture), or F-03 (no IG/Reddit index test) — those are coverage gaps, not failures.

## Strict-Claim Boundary And Non-Claims

- This is **advisory, findings-first implementation/code review**. It claims **no** formal PASS, readiness, acceptance, validation verdict, severity authority, or mandatory remediation. Severity labels (`blocker`/`major`/`minor`) are **prioritization only**, not formal Orca verdict authority.
- No `patch_queue_entry` is emitted. No source file was edited, staged, committed, or pushed. No live capture / network / scheduler / Data-Lake / product-proof / Judgment action was taken.
- Review findings are **decision input only**; they are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized by the home model / owner.
- Strict review claims: `NOT_CLAIMED` (no formal Orca implementation-review lane bound to this commission).

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

original_commission_or_review_target:
  Cross-vendor (Claude reviewer vs GPT-family Codex author) adversarial implementation/code
  review of the Cleaning spine enforcement batch, range
  0ad2292c4d13e76597c5191d9157503c780a5145..db0bcdfb6d9279f53f49195fbbea2d9572bc564a,
  branch codex/cleaning-spine-continuation. Routed as multi-file CODE review (not the
  single-artifact delegated review-and-patch convention), reviewer read-only.

implementation_context_diff_and_reviewed_files:
  6 target files (verified matching db0bcdfb at review time; only later commit df0dcf40 is the
  prompt carrier and does not touch targets): ecr/__init__.py, ecr/models.py,
  runners/run_capture_ecr_cleaning_smoke.py, runners/run_cleaning_spine_periodic_audit.py,
  tests/unit/test_capture_ecr_cleaning_smoke_runner.py, tests/unit/test_ecr_models.py.
  Three commits: 3111c52f (projection refs), 9009151e (ambiguous anchors), db0bcdfb (typed ECR receipts).

findings_and_implementation_evidence:
  F-01 (major): Reddit projection-ref enforcement unwired — _reddit_handle sets no projection_ref;
    needed_packet_ids never includes Reddit packets; audit's reddit row-index branch unreachable;
    _verify_cleaning_projection_ref early-returns for all Reddit handles. OD-1 makes projection_ref
    optional, so not a doctrine violation, but E-01 scope names Reddit and the dead branch implies
    coverage not delivered (false-confidence / hidden adapter gap).
  F-02 (major): _build_projection_row_index builds {row.row_id: row.row_kind} dict — duplicate/ambiguous
    row_ids silently collapse; neither retail nor IG projection model enforces row_id uniqueness; does
    not fail closed on ambiguous row ids as E-01 requires. Live trigger unconfirmed.
  F-03 (minor): IG (reachable) and Reddit (unreachable) projection-ref/index branches untested; only
    retail exercised.
  F-04 (minor/residual): new ECR receipt model is strict-read (exact schema_version Literal, min_length
    receipts/non_claims); legacy/loose v0 artifacts would be rejected; diverges from inherited
    lenient-read/strict-admit posture. Defensible for an audit gate.
  F-05 (minor/residual): receipt packet-binding enforced only for identity/source_visibility postures;
    inspectability/timing (slice-keyed, no packet_id) bound only transitively via producer.
  Minor test note: clear-mismatch test covers aggregate-wrong-while-postures-clear only, not the
    one-posture-false path.

intended_enforcement_closure_statuses:
  E-01: partially_closed (retail closed+tested; IG wired+untested; Reddit not delivered; duplicate-row_id
        not fail-closed).
  E-02: closed (ambiguity is a distinct, non-silent finding driving warn/nonzero-exit in both smoke and
        audit; empty-anchor edge neutralized by model invariant). Residual: minor/warn-level by design;
        producer-side detection is retail-only (IG/Reddit ambiguity caught at audit).
  E-03: closed (typed models with required posture kinds, clears re-validation, exact ref coupling,
        unique keys, schema-constructed smoke artifact, both lanes validated; negative tests present).
        Residuals F-04, F-05.

proposed_patch_or_exact_requested_edits:
  None applied — reviewer is read-only; this is a multi-file code review, not a single-target patch
  commission. Closure conditions stated per finding (end-state, not how-to). The load-bearing decision
  is F-01: wire Reddit projection_ref + test, OR remove/guard the dead Reddit branch and record the
  residual.

citations:
  Code: run_capture_ecr_cleaning_smoke.py (_reddit_handle ~700-715; main loop 126-176; _derive_ecr_receipt
    759-795; _retail_anchor_unverified_reason 865-886). run_cleaning_spine_periodic_audit.py
    (_build_projection_row_index 587-665; _verify_cleaning_projection_ref 666-730; _lane_status 1459-1465;
    status calc 168-174; _promote_smoke_summary_findings 1060-1104; _load_ecr_receipt_artifact 1445-1449).
    ecr/models.py (new receipt models). cleaning/models.py (projection_ref default None 186;
    CleaningRawAnchor non-empty anchor_value 128-138). cleaning/projection.py (projection_ref population
    44-54). retail_pdp_projection.py (validate_counts 147-153). ig_projection.py (validate_counts, no
    uniqueness).
  Authority: projection_doctrine_v0 (OD-1 optional projection_ref); ecr_spine_submap_v0 (lenient-read/
    strict-admit invariant 4); data_and_cleaning_spine_boundary_v0 (Cleaning lane table); review-lanes.md
    (findings-first; code review excluded from fitness-reference; cross_vendor_discovery bar).

reviewer_verdict:
  ADVISORY_CHANGES_RECOMMENDED. No blocker. E-03 strong; E-02 effectively closed; E-01 partially closed
  with two majors (F-01 Reddit coverage/dead-branch, F-02 duplicate-row_id fail-open). No data-corruption
  or false-success path found. Advisory only; no formal PASS/readiness/acceptance claimed.

validation_evidence_and_not_run_checks:
  Independently reran: targeted suite 50 passed; broader no-network suite 210 passed; both runner --help
  exit 0 — all matching author-observed output. Not run / not exercised: any test for the F-01/F-02/F-03
  gaps (they are coverage gaps, not failures); live capture/network/scheduler/Data-Lake/product-proof/
  Judgment paths (out of scope, not run).

residual_risk:
  F-04 legacy-artifact rejection (low; regenerated each run). F-05 tamper-only (producer-safe). Confidence
  bound: ecr/deriver.py and reddit consolidator not read in full — F-05 and F-01 Reddit-consistency rest
  on call sites + fixtures + green reruns. Authority/overlay files (9) read via a Claude-family delegated
  reader; de-correlation (author=GPT vs reviewer=Claude) preserved.

blockers_offscope_flags_and_not_proven_boundaries:
  No blocker. Off-scope (not widened): Cleaning/Capture/Data-Lake/scheduler/product-proof/Judgment beyond
  the touched diff. Not proven: formal acceptance/readiness/validation (advisory only); F-02 live
  exploitability (no duplicate-producing fixture demonstrated).
```
