# Bronze Full-GT Fused Batch — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review output
scope: >
  De-correlated adversarial code review of the Bronze full-GT fused batch
  implementation diff (inventory gate, ambiguous Attachment-Record branch pin,
  materially-different raw-body join-shape pin).
use_when:
  - Adjudicating the codex/bronze-full-gt-fused-batch test-hardening diff before
    keep/merge.
authority_boundary: retrieval_only
```

## Provenance

```yaml
reviewed_by: claude-opus-4-8            # observed controller identity, factual (not operator-backfilled)
authored_by: OpenAI GPT-family Codex    # per commission actor_model_family_receipt; exact model/version unrecorded
controller_model_family: Anthropic / Claude   # commission left controller_model_family: operator_to_fill; filled here with observed identity
de_correlation_bar: cross_vendor_discovery
de_correlation_status: satisfied         # controller vendor (Anthropic) != author vendor (OpenAI)
same_vendor_rationale: not_applicable    # required only for same_vendor_sanity
```

## Commission → Target → Authority → Decision Criteria

- **Commission.** `docs/prompts/reviews/bronze_full_gt_fused_batch_adversarial_code_review_prompt_v0.md` — de-correlated adversarial code review; `delegated_code_review_and_patch` mode; patch authority bounded to the three target test files only; review is decision input, home/CA adjudicates.
- **Target.** The implementation diff on `codex/bronze-full-gt-fused-batch` vs `origin/main`, across three test files:
  - `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - `orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`
  - `orca-harness/tests/unit/test_tiktok_batch_projection.py`
- **Authority (code fitness bar).** Spec/tests/ground-truth substrate: the changed tests must bind **real** implementation branches and trip on the specified regressions. Overlay authority: `review-lanes.md` (code fitness bar is spec/tests, not the artifact-review `fitness_reference`), `delegated-review-patch.md` (patch bound to named set; validation can fail; strict-claim boundary).
- **Decision criteria (from the commission's failure modes + fitness reference).** Future changes must **deterministically trip** a test when they (a) add/remove a non-raw lake touchpoint, (b) collapse the YouTube ambiguous Attachment-Record lineage into a winning record, or (c) weaken the materially-different raw-body join shape — **without** selecting storage architecture (Manifest v2 / manifest-equivalent index / physicalization backend / retention / erasure / backend lock-in), claiming a third Silver proof, or claiming Bronze full-GT readiness.

## Branch / Head / Dirty State

- Branch under review: `codex/bronze-full-gt-fused-batch`.
- Head SHA: `5b874b82891a49bf05c3e091511fc16088a905d3` (local == `origin/codex/bronze-full-gt-fused-batch`; verified equal).
- Base: `origin/main` = `3eb6ec5850bb95e6958795ccb610a066ead9c9c6`; merge-base == base, so the branch is exactly **one commit** ahead (`Harden Bronze full-GT inventory and AR threshold gates`).
- Diff contents (`origin/main...codex/bronze-full-gt-fused-batch`): the review prompt + the three target test files only (267 insertions, 2 deletions). No runtime/overlay/CI/product edits.
- Review-worktree dirty state: **clean** (`git status --porcelain` empty). Diff matches the commission's `dirty_state_allowance` exactly.
- `controlling_source_state`: no overlay, prompt-policy, review-lane, or validation-gate files are modified in the diff → **no strict-claim block** from that clause.

## Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` | Authority kernel (supplied in task context) | clean |
| `.agents/workflow-overlay/README.md` | Overlay binding rule | clean |
| `.agents/workflow-overlay/review-lanes.md` | Code vs artifact fitness bar, findings-first, two-bar de-correlation, provenance fields | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | `delegated_code_review_and_patch` mode, patch bound, strict-claim boundary | clean |
| `.agents/workflow-overlay/source-loading.md` | Source-pack + ledger discipline | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-gated method contract, review prompt defaults, adjudication tail | clean |
| `.agents/workflow-overlay/decision-routing.md` | Confirm review routing already fixed by commission | clean |
| Diff `origin/main...codex/bronze-full-gt-fused-batch` (3 test files) | Primary review target | clean |
| `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` (full) | Inventory test + `_call_name`/walk mechanics | clean |
| `orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py` (new + sibling "missing" test, helpers) | Ambiguous-AR pin | clean |
| `orca-harness/tests/unit/test_tiktok_batch_projection.py` (new + sibling anchor test, fixture) | Join-shape pin | clean |
| `orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py:490-624` | Ambiguous vs missing branch (`len(candidates) != 1`) is real | clean |
| `orca-harness/source_capture/tiktok/batch_projection.py` (full) | Row/raw_ref/raw_anchor/binding_map/non_claims shape | clean |
| `orca-harness/data_lake/{root,catalog,silver_record}.py` (API surface) | Completeness of the non-raw touchpoint token set | clean |
| Runtime callers of omitted API (`record_path`/`lane_dir`/`is_record_set_complete`/`inspect_catalog`/`catalog_coverage_census`) | Prove the coverage gap is live in non-test code | clean |

**SOURCE_CONTEXT_READY** — declared. No missing sources; no excluded decision-bearing sources; no conflicts.

---

## Findings (hard correctness / coverage first)

### F1 — MAJOR: Non-raw touchpoint inventory omits live, physicalization-coupled touchpoint classes; the gate under-covers its own stated purpose

- **Location.** `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:85-133` (`NON_RAW_LAKE_TOUCHPOINT_CALLS` + `EXPECTED_NON_RAW_LAKE_TOUCHPOINTS`) and the assertion message at `:390-396`.
- **Evidence.** The token set is exactly six names: `append_record`, `append_record_set`, `append_silver_record`, `load_attachment_record_body`, `rebuild_catalog`, `source_surface_catalog_rows`. The test's assertion message states these must be re-classified "before selecting Manifest v2, a manifest-equivalent index, or a physicalization backend." But the `data_lake` public API exposes further **non-raw** record-layer touchpoints that are **called in runtime (non-test) code** and are omitted from the set:
  - `record_path(subtree, raw_anchor, lane, record_id)` — constructs the **physical record path** (`data_lake/root.py:749`). Runtime callers: `source_capture/ig_reels_grid_projection.py:423`, `source_capture/ig_reels_behavioral_lake.py:352`, `runners/run_cleaning_spine_periodic_audit.py:1509`, `runners/run_transcript_product_extract.py:230`.
  - `lane_dir(subtree, raw_anchor, lane)` — constructs the **physical lane directory** (`data_lake/root.py:762`). Runtime callers: `youtube_capture/behavioral_projection.py:661`, `source_capture/ig_reels_behavioral_lake.py:333`, `runners/run_capture_ecr_cleaning_smoke.py:961`, `runners/run_transcript_product_extract.py:91`, `capture_spine/creator_profile_current/silver_metric_reader.py:57,352,361`.
  - `is_record_set_complete(...)` — reads **record-set completeness** (`data_lake/root.py:655`). Runtime callers: `youtube_capture/behavioral_projection.py:674`, `source_capture/ig_reels_behavioral_lake.py:196,247`, `runners/run_ig_reels_lane_orchestrator.py:252`, `runners/run_ig_reels_product_extract.py:246,397,515`, `runners/run_transcript_product_extract.py:220`, `runners/run_source_capture_ig_reels_deep_capture.py:288`.
  - Catalog reads `inspect_catalog` (`data_lake/catalog.py:209`) and `catalog_coverage_census` (`:284`) — runtime caller `runners/run_data_lake_catalog.py:39,41`. (`source_surface_catalog_rows` **is** covered but its sibling catalog reads are not.)
- **This is inside the non-raw class, not a raw/non-raw boundary question.** Raw writes (`allocate_raw_packet_dir`/`stage_raw_packet`/`publish_raw_packet`) are correctly excluded. `record_path`/`lane_dir` are the *most* physicalization-coupled functions in the whole API — they literally encode the on-disk layout a physicalization-backend decision would change — yet they are absent.
- **Impact.** The gate does not trip when a new `record_path`/`lane_dir`/`is_record_set_complete`/`inspect_catalog`/`catalog_coverage_census` call is added or removed. Against the commission's fitness reference ("future changes trip deterministic tests when they add/remove non-raw lake touchpoints") and named failure mode ("inventory misses a real writer/non-raw-touchpoint class"), the gate **under-covers its stated scope** and yields false confidence that "each new or removed touchpoint" is enumerated. The over-promise lives in the assertion-message prose; the code honestly enumerates only the six it names, so this is a coverage/scope gap, not a wrong-PASS on the six tokens — hence MAJOR, not critical.
- **`minimum_closure_condition`.** One of:
  - (a) the token set + `EXPECTED_NON_RAW_LAKE_TOUCHPOINTS` are expanded to the physicalization-coupled non-raw classes the message claims to gate (at minimum `record_path`, `lane_dir`, `is_record_set_complete`; and the catalog reads `inspect_catalog`, `catalog_coverage_census`), with accurate counts; **or**
  - (b) the docstring/assertion message is narrowed to state the gate covers only non-raw **writes** plus the two named reads, and is explicitly **not** the classification surface for record-path/lane-dir/completeness/catalog-read touchpoints — so stated scope equals actual coverage.
- **`next_authorized_action`.** Owner/CA decision on which non-raw touchpoint classes are in-scope for the pre-physicalization classification (the set boundary is genuinely fuzzy at the edges — e.g. raw-availability reads `list_available`/`read_availability` are arguably raw-side and out). Once the owner picks (a) or (b), the edit is mechanical and inside the patch-bounded target file.
- **Why not auto-patched.** Selecting the authoritative touchpoint set shapes the downstream GT-fork/physicalization gate (real lock-in), and the boundary is a modeling decision, not a clerical fix. Per the Decision Priority (least compounded risk; surface high-lock-in forks to the owner) I return this as decision input rather than baking a scope choice into a shared contract test. `patch_queue_entry`: not emitted (owner scope decision precedes any executor-ready edit).

### F2 — MINOR: Inventory walk includes ignored scratch and any stray `.py` outside `tests/` (latent non-determinism)

- **Location.** `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:330-344` (`_non_raw_lake_touchpoints`), specifically `_HARNESS_ROOT.rglob("*.py")` filtered only by `relative_path.startswith("tests/")`.
- **Evidence.** `orca-harness/_test_runs/` is git-ignored scratch (`git check-ignore _test_runs` and `_test_runs/probe.py` both match) purpose-built for run artifacts, and it is **not** excluded by the walk. Any `.py` deposited there (or any other untracked/ignored `.py` under the harness outside `tests/`, e.g. a developer probe or a `.venv` created under the harness) is `ast.parse`-d and, if it contains a token-named call, counted into `actual` — failing the `actual == EXPECTED` equality for reasons unrelated to real source. A malformed stray `.py` would raise inside `ast.parse` and error the test outright. Currently benign: `find _test_runs -name '*.py'` returns 0 files, so the gate passes today.
- **Impact.** Determinism of the gate depends on the working tree containing no stray/ignored `.py` outside `tests/` — a condition the repo's own ignore rules explicitly permit under `_test_runs/`. Instantiates the commission's "too brittle" / "treats generated scratch as runtime surface" failure modes, latently.
- **`minimum_closure_condition`.** The walk enumerates **source** deterministically — e.g. restrict to tracked files, or exclude ignored/scratch paths (`_test_runs/`, and defensively `.venv`/`venv`/`build`) — so the inventory is a function of source, not of transient working-tree contents.
- **`next_authorized_action`.** Patchable within the target file. Returned advisory (not shipped) because the complete fix is a design choice among tracked-files-only vs. explicit ignore-exclusion vs. source-dir allowlist (each with maintenance/`git`-dependency tradeoffs); a one-dir `_test_runs/` exclusion would be a fragile partial that leaves the general stray-`.py` gap and could read as "closed." Owner picks the approach; can be batched with F1.

---

## Cleared Checks (attacked, no finding)

- **Ambiguous Attachment-Record pin is real and trips on collapse.** `youtube_silver_metric_producer.py:530` branches on `len(candidates) != 1`, and `_fallback_raw_ref_fields` (`:572-583`) emits a **distinct** `raw_packet_fallback_ambiguous_attachment_record` / `typed_attachment_record_status: "ambiguous"` for `len>1`, vs `missing` for `len==0`, vs the winning `bronze_attachment_record` for `len==1` (`:542-568`). The new test (`test_youtube_...:308-337`) injects two candidates against a real committed packet's `(packet_id, sha256)` key and asserts the ambiguous kind/status/residual + the ambiguous `lineage_limitations` entry. If the producer collapsed to `candidates[0]` (e.g. `!= 1` → `< 1`), the `raw_ref_kind`/`typed_attachment_record_status` asserts would fail. Genuinely binds the branch and satisfies decision criterion (b).
- **TikTok test pins a materially-different raw-body join shape and does not claim a third Silver proof.** `batch_projection.py` builds a **projection (view over raw)**: per-row `raw_ref = {packet_id, slice_id="videos/{i}"}` and `raw_anchor.json_pointer="/videos/{i}"` into one shared packet path (`:281-291`). The new test (`test_tiktok_...:80-93`) pins `slice_id == ["videos/0","videos/1"]` and `json_pointer == ["/videos/0","/videos/1"]` over a 2-video fixture (the sibling test at `:42-43` confirms the fixture yields 2 rows), so a change to the slice/pointer scheme trips it. The lane is explicitly non-persisted: `binding_map` is empty (model validator rejects non-empty, `:142-143`), `preserved_bindings: Literal[0]` (`:107`), `write_tiktok_batch_projection` "does not append a data-lake record" (`:248`), and `non_claims` carries `not_ecr_record` + `not_persisted_derived_projection_lane` (`:33-34`) — so it neither duplicates the YouTube **Silver producer** (which appends silver records) nor claims a third Silver proof. Satisfies decision criterion (c).
- **No architecture selection / no readiness claims introduced.** The inventory message is a *pre-decision* gate ("before selecting Manifest v2…"), not a selection. The pre-existing `attachment_record_physicalization == "manifest_equivalent_entry_over_raw_packet_body_v0"` assertion (`test_youtube_...:265`) is **not in this diff** (it asserts an existing Bronze-AR record field). No retention/erasure/backend-lock-in, no Bronze full-GT readiness/validation/buyer-proof/runtime-proof claim appears in the diff. Non-claims preserved.

## Optional Hardening (non-required; not a blocker)

- In the TikTok test, `assert projection.binding_map == []` and `assert "not_persisted_derived_projection_lane" in projection.non_claims` are already **structurally guaranteed** by the `model_validator` and the `non_claims` default factory, so they add documentation value but little independent regression signal; the load-bearing asserts are the `slice_id`/`json_pointer` lists. Optional: assert the join *identity* (e.g. that `raw_anchor.relative_packet_path`/`sha256` equal the committed raw packet's, not merely that they are uniform across rows) to also pin the anchor to the real raw body. Non-required.

## Validation Evidence

```yaml
run:
  cwd: orca-harness
  command: python -m pytest -q tests/contract/test_capture_runner_lake_seam_coverage.py
           tests/unit/test_youtube_creator_metric_silver_producer.py
           tests/unit/test_tiktok_batch_projection.py
  result: passed            # 33 tests, 0 failed
  new_tests_focused_rerun: passed   # 3/3 (the three added tests)
not_run:
  - "from orca-harness, ORCA_DATA_ROOT unset: python -m pytest -q (full suite)"
  - ".agents/hooks/* --strict (map/header/csb/ontology/deletion/dcp/silver-lane) + git diff --check"
  not_run_rationale: >
    No patch was applied (both findings returned as owner-scope decision input),
    so per the commission's 'rerun only the focused tests you need for confidence'
    clause the focused files are sufficient. The diff touches only three test
    files (no runtime/overlay/ontology/prompt-provenance/CI surface), so the
    strict hooks and full suite are low-yield here; the CA/lane PR gate remains
    the authoritative full-suite run.
```

## Patch Status

- **No patch applied.** Working tree left clean (only this durable report is added under `docs/review-outputs/`). F1 is an owner scope decision (lock-in on the downstream physicalization gate); F2's complete fix is a design choice among enumeration strategies. Both are mechanically patchable within the bounded target file once the owner ratifies scope/approach — routed as decision input, not shipped, to avoid baking a scope/approach choice into a shared contract test. No `NEEDS_ARCHITECTURE_PASS`: the design is sound; the gaps are coverage/robustness within the existing test, not a broken design.

## Review-Use Boundary

These findings are **decision input only**. They are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until the CA separately accepts or authorizes them. This review makes no Bronze full-GT readiness, buyer-proof, runtime-proof, or production-safety claim, selects no storage architecture, and starts/claims no third Silver proof. The temporary material-decision packet remains slated for closeout/supersession.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: docs/prompts/reviews/bronze_full_gt_fused_batch_adversarial_code_review_prompt_v0.md
  (delegated_code_review_and_patch; patch bound to the 3 target test files; cross_vendor_discovery bar).
- implementation context / diff / reviewed files: codex/bronze-full-gt-fused-batch @ 5b874b82 (one commit
  over origin/main 3eb6ec58); files —
    orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py (inventory gate, +83)
    orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py (ambiguous-AR pin, +30)
    orca-harness/tests/unit/test_tiktok_batch_projection.py (join-shape pin, +14)
- findings and evidence:
    F1 (MAJOR): non-raw touchpoint inventory (test_capture_runner_lake_seam_coverage.py:85-133) omits live,
      physicalization-coupled non-raw touchpoints — record_path, lane_dir, is_record_set_complete (data_lake/root.py:749/762/655),
      inspect_catalog/catalog_coverage_census (data_lake/catalog.py:209/284) — all called in runtime code
      (cites in report). Gate under-covers its stated "classify before physicalization backend" scope → false confidence.
    F2 (MINOR): _non_raw_lake_touchpoints walk (:330-344) excludes only tests/, so git-ignored scratch _test_runs/
      (and any stray/ignored .py, e.g. a venv under the harness) is parsed/counted → latent non-determinism; benign today.
    Cleared: ambiguous-AR branch is real and trips on collapse; TikTok test pins a materially-different, non-persisted
      projection join shape and claims no third Silver proof; no architecture selection or readiness claim in the diff.
- proposed patch / exact edits: none applied (both are owner-scope decisions; see minimum_closure_conditions). Both are
  mechanically patchable within the bounded target file after the owner picks scope (F1) / enumeration approach (F2).
- citations: file:line cites inline in the report.
- reviewer verdict: findings-only advisory (code review lane). Diff is functionally correct and its three tests pass
  (33/33); the two findings are coverage-scope (F1) and robustness (F2) improvements, neither a blocker to the diff's
  stated behavior. No formal PASS/readiness asserted.
- validation evidence: focused pytest passed (33 tests, 0 failed); full suite + strict hooks not_run (no patch; test-only
  diff) — rationale in report.
- residual risk: if F1 is left open, the inventory canary silently ignores growth of the record-path/lane-dir/completeness
  touchpoint classes — the class most coupled to the physicalization decision the gate exists to protect.
- blockers / off-scope / not-proven: no off-scope edits attempted; no BLOCKED_CONTROLLER_NOT_DECORRELATED (cross-vendor
  satisfied); full-suite/hook PASS is not-proven here (not_run) and remains the lane PR gate's job.
```

### Adjudicator Next Step (for the commissioning CA)

1. Adjudicate F1/F2 and the verdict as **claims**, not premises.
2. If F1 is accepted as material, the smallest complete closure is the owner's **scope decision** (expand the token set to the physicalization-coupled classes, or narrow the message to match actual coverage) — resolve that one issue first; F2's approach can ride the same decision.
3. Only after a clean adjudication, batch admin/lifecycle (commit the report, push, PR, and any accepted test patch) into **one** land step with no deep-thinking; then deep-think only the 1–3 material next moves (e.g. whether the inventory should become the durable pre-physicalization classification surface, or stay a narrow write-side canary).
