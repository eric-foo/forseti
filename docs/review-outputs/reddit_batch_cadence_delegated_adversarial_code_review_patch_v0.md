---
retrieval_header_version: 1
artifact_role: Orca review output
scope: Delegated adversarial code review-and-patch output for the Reddit old-HTTP batch cadence patch.
use_when:
  - Inspecting Reddit batch-cadence findings or the proposed patch.
  - Tracing CA adjudication to this delegated review.
review_authority_boundary: decision_input_only
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
---

# Reddit Batch Cadence Delegated Adversarial Code Review-and-Patch v0

## Source Context Status

`SOURCE_CONTEXT_READY`

Files read before review:

- `AGENTS.md` (loaded via system context)
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `orca-harness/source_capture/cadence.py`
- `orca-harness/runners/run_reddit_old_http_batch.py`
- `orca-harness/tests/unit/test_reddit_old_http_batch.py`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md` (first 200 lines)
- `orca-harness/tests/unit/test_reddit_batch_quality_summary.py` (read-only context)

De-correlation: author/CA model family is GPT-5/Codex; receiving actor is Claude (claude-sonnet-4-6, Anthropic). Different vendor and model family. De-correlation satisfied.

Branch verified: `ecr-sp3-timing-deriver-slice1`. Short HEAD at read time: `db519f0` (consistent with prompt authoring receipt).

---

## Findings

Findings are ordered by severity. No blockers or major issues were identified.

---

### F1 — MINOR: Bounded-jitter test does not assert `cadence["delay_seconds"] is None`

**File:** `orca-harness/tests/unit/test_reddit_old_http_batch.py`
**Lines:** ~197–206 (`test_batch_runner_bounded_jitter_records_budgeted_cadence`)

The test asserts `summary["delay_seconds"] is None` (the top-level summary key) but does not assert `cadence["delay_seconds"] is None` (the field inside the cadence sub-dict returned by `CadencePlan.to_dict()`). Both fields are present in `batch_summary.json`.

`CadencePlan.to_dict()` always emits `delay_seconds`. Under `bounded_jitter`, `_build_bounded_jitter_plan` does not set it, so the default `None` applies. The production code is correct; the test gap means a future change that accidentally populated `delay_seconds` in the bounded-jitter plan would not be caught.

This is a receipts-contract gap: the test does not fully pin the `bounded_jitter` receipt shape. A reader checking the test as the receipts specification would conclude that `cadence["delay_seconds"]` is unspecified for `bounded_jitter`.

**Risk:** False-success risk is low (production code is correct), but the test omission allows receipt drift to go undetected.

**Patch:** Add `assert cadence["delay_seconds"] is None` to the bounded-jitter test immediately after the other `cadence[...]` assertions.

---

### F2 — INFORMATIONAL (no patch): Float rounding can push `sum(planned_waits_seconds)` above `window_seconds` by at most ~0.5 ms

**File:** `orca-harness/source_capture/cadence.py`
**Lines:** 108–121 (`_build_bounded_jitter_plan` wait loop)

`wait = round(rng.uniform(min_gap_seconds, upper), 3)` is applied after computing `upper = min(max_gap_seconds, max_allowed_now)`. Because `max_allowed_now` is derived from floating-point subtraction and `upper` may not be exactly representable with 3 decimal places, `round(x, 3)` can produce a value that is at most `~0.0005` above `upper`. At the last loop iteration (where `max_allowed_now = window_seconds - elapsed`), this means `sum(waits)` could exceed `window_seconds` by at most ~0.0005 seconds (0.5 ms).

`elapsed` correctly tracks the sum of rounded waits so the loop self-corrects over all but the final step. The exposure is bounded to the rounding error of a single wait value. The test `assert sum(waits) <= 9` would pass in normal arithmetic; it could fail only in the rare case where float subtraction produces `max_allowed_now` with more than 3 decimal places and rounding pushes the last wait over the window by 0.5 ms.

**Assessment:** Negligible impact for a cadence tool operating in tens-to-hundreds of seconds. The `batch_summary.json` receipt would in extreme cases record `sum(planned_waits_seconds)` marginally above `window_seconds`, but the discrepancy is instrument-noise level and does not affect hard-ceiling (URL count) correctness. Not patching: the fix (clamping after rounding) adds complexity for a sub-millisecond edge case.

---

### F3 — INFORMATIONAL (no patch): `delay_seconds` is silently ignored when `cadence_mode="bounded_jitter"` — no validation error or warning

**Files:** `orca-harness/runners/run_reddit_old_http_batch.py` (lines 39–48), `orca-harness/source_capture/cadence.py` (lines 51–58)

`run_reddit_old_http_batch` accepts `delay_seconds` (default `DEFAULT_DELAY_SECONDS = 30.0`) regardless of `cadence_mode`. For `bounded_jitter`, `build_cadence_plan` routes to `_build_bounded_jitter_plan`, which does not consume `delay_seconds`. The argument is silently dropped.

The summary correctly records `delay_seconds: null` at both the top level and inside the `cadence` dict, so a reader of `batch_summary.json` can see that the fixed delay was not used. The test `test_batch_runner_bounded_jitter_records_budgeted_cadence` explicitly passes `delay_seconds=999` and asserts `summary["delay_seconds"] is None`, demonstrating and pinning this behavior.

**Assessment:** The receipt is clear; the test pins the behavior. An operator who passes `--delay-seconds 30 --cadence-mode bounded_jitter` receives no warning, but the `batch_summary.json` makes the actual mode unambiguous. Not patching: a `ValueError` for this combination would break callers that rely on the default `delay_seconds` when invoking with `bounded_jitter`, and the current behavior is already tested and visible. If the operator intent is important, a warning-level message (not a `ValueError`) could be added later.

---

### Q1–Q7 Answers (no additional findings)

**Q1 (Hard ceilings):** `_validate_batch_inputs` enforces `max_urls`, `len(slots)` is never exceeded by the cadence plan, and the loop iterates exactly over `slots`. No retries, source discovery, proxy, browser, or live expansion anywhere in the cadence path. Hard ceilings preserved.

**Q2 (Schedule bounds):** Window invariant: the per-step `max_allowed_now` construction guarantees `sum(waits) <= window_seconds` modulo the ~0.5 ms rounding edge case noted in F2. Min-gap: each `wait >= min_gap_seconds` (enforced by `rng.uniform(min_gap_seconds, upper)` with `upper >= min_gap_seconds` guarded). Max-gap: each `wait <= upper <= max_gap_seconds`. Hidden deterministic bias: none. The seed is recorded verbatim; when `random_seed=None`, `random.SystemRandom().randrange(1, 2**31)` is used and the generated seed is captured in the plan.

**Q3 (Invalid cadence fails before output):** `_validate_batch_inputs` and `build_cadence_plan` are both called before `output_root.mkdir(...)`. Any ValueError from invalid cadence (e.g., window too tight) fires before any directory or `batch_summary.json` is created. Test `test_batch_runner_rejects_impossible_bounded_jitter_before_output` verifies `assert not output_root.exists()`. Clean.

**Q4 (`delay_seconds: null` clarity):** Under `bounded_jitter`, `cadence_plan.delay_seconds` is `None`, so `summary["delay_seconds"]` and `summary["cadence"]["delay_seconds"]` are both `null` in the JSON. Test `test_batch_runner_bounded_jitter_records_budgeted_cadence` asserts the top-level field. The per-row `limitations` list includes `batch runner cadence_mode=bounded_jitter`, making the mode visible in each packet's metadata. Clean after the F1 patch.

**Q5 (Tests prove both modes, no real network):** Ten tests cover: URL parsing and rejection, fixed-mode capture/consolidate/sleep sequence, bounded-jitter cadence receipt, failure-without-retry, max_urls enforcement, pre-output error for impossible cadence, direct-built-slot host bound, direct-built-slot path traversal, and forbidden-import AST scan. No real network calls; all capture/consolidate/sleep are monkeypatched.

**Q6 (Docs — no stealth/human-impersonation/bypass language):** The runbook (line ~175) states "This is a bounded low-load schedule, not a stealth or human-impersonation claim." The Armory README (line ~495) states "This cadence is for low-load bounded operation and provenance, not a claim to mimic a human or bypass access controls." Both documents explicitly disclaim the forbidden frames. No material doc drift found.

**Q7 (No broadened authority):** `cadence.py` and `run_reddit_old_http_batch.py` contain no references to ECR, Cleaning, Judgment, warm JSON, CloakBrowser, archive fallback, or source discovery. The `capture_context` field in the runner explicitly states "exact supplied URL only; no proxy, browser, crawler, retry, or link following." The cadence patch is strictly scoped to the Direct HTTP batch runner.

---

## Patch Applied

**File:** `orca-harness/tests/unit/test_reddit_old_http_batch.py`

**Changed function:** `test_batch_runner_bounded_jitter_records_budgeted_cadence`

**Change summary:** Added one assertion after the existing `cadence["random_seed"]` check to pin the `cadence["delay_seconds"]` receipts field as `None` under `bounded_jitter`.

**Diff:**

```diff
--- a/orca-harness/tests/unit/test_reddit_old_http_batch.py
+++ b/orca-harness/tests/unit/test_reddit_old_http_batch.py
@@ test_batch_runner_bounded_jitter_records_budgeted_cadence
     assert cadence["random_seed"] == 1234
+    assert cadence["delay_seconds"] is None
     waits = cadence["planned_waits_seconds"]
```

No other files were modified. No changes were made to `cadence.py`, the runner, the docs, or any other file in the target or read-only scope.

---

## Validation

**Pre-patch baseline:**

```powershell
python -m pytest -p no:cacheprovider -q --basetemp orca-harness\_pytest_tmp_reddit_cadence orca-harness\tests\unit\test_reddit_old_http_batch.py
```

Output: `..........  [100%]`

```powershell
python -m pytest -p no:cacheprovider -q --basetemp orca-harness\_pytest_tmp_reddit_cadence_quality orca-harness\tests\unit\test_reddit_batch_quality_summary.py
```

Output: `........  [100%]`

**Post-patch:**

```powershell
python -m pytest -p no:cacheprovider -q --basetemp orca-harness\_pytest_tmp_reddit_cadence orca-harness\tests\unit\test_reddit_old_http_batch.py
```

Output: `..........  [100%]`

Both validation suites observed passing. The patch did not break existing tests and the new assertion passes, confirming the production code already satisfies the `cadence["delay_seconds"] is None` contract under `bounded_jitter`.

No live Reddit/network commands were run. No live capture, archive, warm-JSON, browser, proxy, CloakBrowser, or install operations were performed.

---

## Residual Risk

1. **Float rounding at window boundary (F2):** `sum(planned_waits_seconds)` can technically exceed `window_seconds` by at most ~0.5 ms due to float rounding in the last wait. This is instrument-noise level and does not affect hard ceilings on URL count, retries, or source scope. Risk: negligible.

2. **`delay_seconds` silently ignored for `bounded_jitter` (F3):** No validation error or warning is emitted when `--delay-seconds` is passed with `--cadence-mode bounded_jitter`. The `batch_summary.json` correctly shows `delay_seconds: null`, so a reader of the receipt is not misled, but an operator may be surprised. Risk: low (receipt is clear; test documents the behavior).

3. **Single rounding path in `_build_bounded_jitter_plan` not covered by a dedicated property-based test:** The test uses a fixed seed (`1234`) and a single parameter set. Adversarial seeds or extreme parameter combinations (e.g., `slot_count=2`, `window=min_gap=max_gap`) are not covered. Risk: low (the logic is simple and the structural analysis above shows the invariants hold for all valid inputs).

---

## Verdict

`PATCHED_FOR_CA_ADJUDICATION`

One minor receipts-contract patch was applied (F1 — `test_reddit_old_http_batch.py`). No production-code bugs were found. No blocker or major issues identified.

---

## Non-Claims

- Not deployment, not staging or commit, not live Reddit or network use.
- Not source-capture readiness claim.
- Not validation or formal PASS authority.
- Not fixture admission.
- Not auto-kept: this diff and verdict are decision input for CA adjudication only; nothing is kept without explicit CA acceptance.
- The patch does not affect runtime behavior — `cadence.py` and `run_reddit_old_http_batch.py` were not modified.
