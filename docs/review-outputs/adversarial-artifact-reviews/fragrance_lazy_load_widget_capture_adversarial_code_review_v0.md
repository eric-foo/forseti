# Fragrance Lazy-Load Widget Capture Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output / read-only adversarial implementation-code review report
scope: >
  Read-only adversarial implementation/code review of commit 2c08ebb6
  (bounded lazy-load scroll support added to the rendered fragrance PDP +
  review-widget response companion capture route: browser page-observation
  adapter, companion helper, runner CLI, and synthetic tests). Findings are
  decision input only.
use_when:
  - Deciding whether one operator command can preserve no-scroll first-view PDP
    facts and passively retain review-widget responses fired by bounded
    lazy-load scrolls, without overclaiming row coverage, DOM scraping, or one
    literal HTTP request.
  - Recovering the material implementation risks in commit 2c08ebb6 before any
    merge or follow-up implementation decision.
authority_boundary: retrieval_only
review_mode: read_only_adversarial_code_review
```

## Provenance

```yaml
reviewed_by: claude-opus-4.8
authored_by: codex/gpt-5  # per the review prompt's operator-attributed provenance for 2c08ebb6; git committer is "Eric"; author lineage operator-supplied, not independently verified here
de_correlation_bar: cross_vendor_discovery  # Anthropic reviewer vs operator-attributed OpenAI author; cross-vendor. Author attribution is operator-supplied, not measured in this review.
same_vendor_rationale: not_applicable
```

This is a who-constraint / measurement record only. It does not select, rank, or
recommend any runtime model (`review-lanes.md` model-neutrality). The
de-correlation classification is at the same bar the sibling
`fragrance_rendered_widget_companion_adversarial_code_review_v0.md` recorded for
this workstream.

## Commission And Lane

- **Commission:** read-only adversarial implementation/code review of commit
  `2c08ebb6277eec4dbafba321f9787557a1e46dcb`, delta
  `047192d3..2c08ebb6`, in worktree
  `.codex/worktrees/fragrance-purchase-review-probes`.
- **Lane:** read-only implementation/code review. The prompt correctly routes a
  multi-file code diff *out* of the single-artifact `delegated-review-patch`
  convention (`delegated-review-patch.md` "Incomplete commission route-out" /
  non-eligible-target boundary); no patch authored, no patch queue emitted.
  `workflow-deep-thinking` then `workflow-code-review` were `REFERENCE-LOAD`ed
  before source loading and `APPLY`ed only after `SOURCE_CONTEXT_READY`.
- **Output:** this durable report (`review-report` / `filesystem-output` mode);
  chat returns a short summary plus the `review_summary` courier YAML.
- **Severity labels** (`critical` / `major` / `minor` / `advisory`) are finding
  priority only. Per `review-lanes.md` they create no approval, rejection,
  readiness, validation, or mandatory-remediation authority. No
  `patch_queue_entry` is emitted; remediation direction is advisory prose only.

## Source Context And Verification

- **Hash pins:** all 5 target + 2 support SHA256 pins verified **equal** to the
  pinned values via `Get-FileHash -Algorithm SHA256` on the working-tree files.
  No `HASH_MISMATCH`.
- **Git state:** branch `codex/fragrance-purchase-review-probes`. Worktree HEAD
  is `b89f1964` ("Add fragrance lazy-load capture review prompt"), exactly **one
  commit past** the review target `2c08ebb6`; `b89f1964^ == 2c08ebb6` and
  `b89f1964` adds only the 395-line review-prompt doc (single-file commit). So
  the 5 target files are byte-identical to their `2c08ebb6` state (confirmed by
  the hash match), consistent with the prompt's `dirty_state_allowance`. `git
  merge-base --is-ancestor 2c08ebb6 HEAD` → 0. `diff --stat 047192d3..2c08ebb6`
  matches the prompt's stated 5-file / 275-insertion / 1-deletion shape.
- **Required source basis:** all `blocked_if_missing` / Required-Source-Basis
  files PRESENT and loaded — `AGENTS.md`; overlay `README`, `source-of-truth`,
  `source-loading`, `delegated-review-patch`, `prompt-orchestration`,
  `review-lanes`, `validation-gates`, `template-registry`; preflight defaults;
  and the 3 spine contracts (`rendered_companion_probe`,
  `focused_coverage_mgt`, `row_contract`). → **`SOURCE_CONTEXT_READY`**.
- **Validation evidence (independently re-run):** `python -m pytest -q
  tests\unit\test_source_capture_browser_snapshot.py
  tests\unit\test_fragrance_rendered_widget_companion.py
  tests\unit\test_fragrance_review_coverage.py` → **exit 0, 50 passed** (50
  progress dots, `[100%]`, no `F`/`E`). Independently corroborates the author's
  "50 passed" evidence. No new live retailer smoke for the lazy-load scroll
  option exists; the prompt flagged that as a reviewable residual (see LZ-05/
  Not-Proven Boundaries).

### Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `adapters/browser_snapshot.py` (target) | Core lazy-load adapter logic, constants, ordering, `warning_notes` flow | clean (hash-pinned) |
| `fragrance_rendered_widget_companion.py` (target) | Companion receipt assembly, route-health, fallback gating, non-claims | clean (hash-pinned) |
| `runners/run_fragrance_rendered_widget_companion.py` (target) | CLI threading, return value, help text | clean (hash-pinned) |
| `tests/unit/test_source_capture_browser_snapshot.py` (target) | Adapter/scroll/cap/validation test coverage | clean (hash-pinned) |
| `tests/unit/test_fragrance_rendered_widget_companion.py` (target) | Companion + runner threading test coverage | clean (hash-pinned) |
| `fragrance_review_coverage.py` + test (support) | Confirm rows derive from widget bodies, mechanical-only | clean (hash-pinned) |
| 3 retail_pdp spine contracts | Domain authority: no-scroll baseline, row source = widget, no DOM-row parsing | clean |
| `fragrance_*_adversarial_code_review_v0.md` (2 prior outputs) | Prior workstream reviews | available, not read in full (not finding-material) |

## Failure-Mode Framing (applied `workflow-deep-thinking`)

The decisive question: does 2c08ebb6 broaden widget-response observation via
bounded scrolling **without** (a) mutating or losing the no-scroll above-fold
facts it promises to preserve, (b) manufacturing fake row-complete/coverage
success, or (c) crossing the row-contract hard line into DOM review-row
extraction or source-wide claims? Attacked, in consequence order: provenance
integrity of the `pre_lazy_load_scroll` ordering label; honest incompleteness
under cap / early-termination / silent-widget-miss; blast radius of the optional
stage onto the guaranteed baseline; boundary preservation (fallback-after-
passive, no DOM rows, no ECR/Judgment); and whether the load-bearing invariants
are actually exercised or only asserted by hardcoded strings and fakes.

## Findings (findings-first, ordered by severity)

No `critical` findings. The capture is bounded, fails loud, sources rows from
widget responses (not DOM), and carries honest non-claims. One `major` (a
test-coverage gap on the provenance invariant), three `minor`, four `advisory`.

---

### LZ-01 — Major — Patch's central ordering/provenance invariant has no test guard

- **Severity:** major (high-risk test gap before merge; provenance-integrity axis).
- **Commissioned target/purpose:** verify no-scroll first-view facts are
  preserved before any scroll can mutate page state (Review Q1, Q11).
- **Reviewed artifact:** `adapters/browser_snapshot.py`
  `capture_page_observation`; `tests/unit/test_source_capture_browser_snapshot.py`.
- **Location:** ordering at
  [browser_snapshot.py:725](orca-harness/source_capture/adapters/browser_snapshot.py)
  (`visible_text`), `:731` (`dom_observation`), `:732` (`_run_bounded_lazy_load_scrolls`),
  `:737` (`responses`); provenance label at `:760`
  (`"dom_observation_stage": "pre_lazy_load_scroll"`).
- **Implementation evidence:** in the *current* code the order is correct —
  `visible_text` (725) and `dom_observation` (731) are captured, *then* the
  scroll runs (732), *then* `responses` is read (737); the page-observation
  engine takes no screenshot, so there is no post-scroll screenshot mislabel.
  But the engine method `capture_page_observation` is **never executed by any
  test** — every test fakes it (`_FakePageObservationEngine`,
  `test_*_threads_lazy_load_scroll_controls_to_engine`) or fakes the fetcher
  (`fake_observation_fetcher`). `dom_observation_stage` is a hardcoded string
  literal, not a value derived from observed call order.
- **Authority/evidence basis:** the patch's own fitness signal (prompt
  `fitness_reference.observable_success_signal`: "preserve no-scroll first-view
  DOM/text facts **before** any lazy-load scroll") and the
  `rendered_companion_probe_v0` no-scroll baseline; `validation-gates.md`
  "Validation must be able to fail … never create fake success paths."
- **Impact:** a future refactor that moved `_run_bounded_lazy_load_scrolls`
  above the `dom_observation`/`visible_text` extraction (or re-read either after
  the scroll) would still pass all 50 tests while silently (i) mutating the
  preserved above-fold facts and (ii) turning the durable
  `dom_observation_stage: pre_lazy_load_scroll` provenance label into a false
  claim. The invariant the patch exists to protect is unguarded.
- **Minimum closure condition:** an executable test pins the ordering — e.g. a
  fake `page` that records the sequence of `inner_text` / `dom_extract` /
  `scrollTo` / response-read calls and asserts DOM+text precede the first
  scroll and responses are read after (the `_FakeLazyScrollPage` recording
  pattern already exists and can be extended), so a reordering regression fails
  a test.
- **Next authorized action:** owner/implementer decision — add the ordering
  regression test before merge, or accept with an explicit fast-follow. (Review
  is decision input only; no patch authored. No current correctness defect was
  found in the code itself — this is regression protection.)
- **`patch_queue_entry`:** not authorized (read-only lane).

---

### LZ-02 — Minor — `executed < requested` is not disambiguated in route_health (cap vs page-end vs short page)

- **Severity:** minor.
- **Commissioned target/purpose:** Review Q3/Q4/Q7 — can a reader compare a
  no-scroll baseline against an opt-in scroll capture, and is a capped/early-
  terminated pass count legible?
- **Reviewed artifact:** `fragrance_rendered_widget_companion.py`
  route-health; `adapters/browser_snapshot.py` cap warning.
- **Location:**
  [fragrance_rendered_widget_companion.py:274-278](orca-harness/source_capture/fragrance_rendered_widget_companion.py)
  (`lazy_load_scroll_passes_requested:N` / `..._executed:M` appended to
  `route_health`); cap warning at
  [browser_snapshot.py:712-716](orca-harness/source_capture/adapters/browser_snapshot.py);
  step early-break at `:996-997`.
- **Implementation evidence:** `route_health` carries only the raw `requested`
  and `executed` integers. `executed < requested` has three distinct causes:
  (a) the safety cap `_MAX_SCROLL_PASSES` (the *only* one with an explanatory
  signal, and that signal lives in `warning_notes`, a **different** receipt
  field — line 352 — not in `route_health`); (b) step-mode reached page end
  (`if position >= height: break`, a benign *complete* traversal); (c) a page
  shorter than the step budget. None of (b)/(c) emits any marker. The metadata
  stores the **raw** requested value (`:761`), so `requested:50 executed:40`
  surfaces honestly, but the *reason* is ambiguous.
- **Authority/evidence basis:** `validation-gates.md` failure-visibility intent;
  `focused_coverage_mgt_v0` route-health "proceed/rederive/fallback" legibility;
  prompt Q4 ("can requested pass caps be hidden … because the warning note
  remains in adapter warnings rather than route health").
- **Impact:** a downstream reader scanning `route_health` cannot distinguish
  "fully traversed the page" from "truncated by the hard cap" without
  cross-referencing `warning_notes`; the cap is **not hidden** from the receipt
  (it is in `warning_notes`), but the two scroll signals are split across two
  fields and the page-end case is unmarked.
- **Minimum closure condition:** the receipt makes the executed<requested cause
  legible from one place — e.g. a `route_health` (or residual) marker such as
  `lazy_load_scroll_capped` and/or `lazy_load_scroll_reached_page_end`, or the
  cap note mirrored into `route_health`.
- **Next authorized action:** owner/implementer decision; advisory only.
- **`patch_queue_entry`:** not authorized.

---

### LZ-03 — Minor — Test gaps on lazy-load branches (cap-warning emission, step early-break, zero-pass no-op)

- **Severity:** minor.
- **Commissioned target/purpose:** Review Q11 — tests strong enough for cap
  warnings, pass execution count, and default zero-pass backward compatibility?
- **Reviewed artifact:** `tests/unit/test_source_capture_browser_snapshot.py`.
- **Location:** `test_bounded_lazy_load_scrolls_stepwise_after_observation_extraction`,
  `test_bounded_lazy_load_scrolls_cap_pass_count`; cap-warning source at
  [browser_snapshot.py:712-716](orca-harness/source_capture/adapters/browser_snapshot.py);
  early-break source at `:996-997`.
- **Implementation evidence:** (a) the cap *warning_note* path (712-716) is
  never exercised — the cap is tested only through
  `_run_bounded_lazy_load_scrolls`, which caps **silently**; the warning lives
  in the faked engine method. (b) The step-mode early-break branch
  (`if position >= height: break`) is never triggered: the step test uses
  `height=2_000, step=500, passes=3` → executed 3, no break. (c) No test
  asserts that `lazy_load_scroll_passes=0` performs no scroll and adds no
  `route_health` lazy markers (zero-pass backward compat is only implicitly
  covered by pre-existing companion tests still passing).
- **Authority/evidence basis:** prompt Q11 enumerated coverage expectations;
  `validation-gates.md` failure-visibility.
- **Impact:** the cap-honesty signal (which LZ-02 shows is the only explainer of
  a capped count) and the early-termination branch can regress without any test
  failing.
- **Minimum closure condition:** tests that (a) assert a `> _MAX_SCROLL_PASSES`
  request produces the capped `warning_note` in the observation/receipt, (b)
  exercise the step early-break (executed < requested due to page end), and (c)
  assert zero-pass is a no-op with no lazy `route_health` markers.
- **Next authorized action:** owner/implementer decision; advisory only.
- **`patch_queue_entry`:** not authorized.

---

### LZ-04 — Minor — Optional scroll stage has no error containment; a recoverable scroll error discards the guaranteed no-scroll baseline

- **Severity:** minor (fails loud — no fake success — and matches the
  established house pattern; flagged for blast radius, not honesty).
- **Commissioned target/purpose:** Review Q5 robustness on long/virtualized/
  SPA pages.
- **Reviewed artifact:** `adapters/browser_snapshot.py`
  `_run_bounded_lazy_load_scrolls` and its call site.
- **Location:**
  [browser_snapshot.py:732](orca-harness/source_capture/adapters/browser_snapshot.py)
  (call site, not wrapped) and `:984-1013` (function body, no try/except).
- **Implementation evidence:** the scroll `page.evaluate(...)` calls are not
  wrapped. Because the no-scroll `visible_text` (725) and `dom_observation`
  (731) are already captured into locals **before** the scroll, an uncaught
  scroll exception (e.g. Playwright "Execution context was destroyed" if a
  scroll triggers a client-side/SPA navigation) propagates out of
  `capture_page_observation`, the success object is never built, and the
  companion raises `FragranceRenderedWidgetCompanionInputError` — discarding the
  already-captured baseline. This is consistent with the sibling `snapshot`
  method, which also lets its scroll evaluates propagate (`:591-603`), but there
  scrolling precedes capture, so nothing valuable is lost.
- **Authority/evidence basis:** the patch's stated goal of *preserving* no-scroll
  facts while *optionally* broadening; `AGENTS.md` "Preserve real failure
  visibility; never create fake success paths" (satisfied — failure is loud);
  Decision Priority "least compounded risk."
- **Impact:** an opt-in enhancement can now fail the entire capture, including
  the guaranteed no-scroll baseline, instead of preserving the baseline and
  recording a `lazy_load_scroll_failed` residual. Bounded (re-run without scroll
  recovers) and loud, so not a fake-success path.
- **Minimum closure condition:** either scroll-stage errors are contained
  (recorded as a residual/warning while the no-scroll baseline still returns),
  or an explicit, documented decision that a scroll failure should fail the
  whole capture.
- **Next authorized action:** owner/implementer decision; advisory only.
- **`patch_queue_entry`:** not authorized.

---

### LZ-05 — Advisory — Fixed `_SCROLL_PASS_SETTLE_MS`; no post-final-scroll settle/networkidle before responses are read

- **Severity:** advisory.
- **Location:**
  [browser_snapshot.py:22](orca-harness/source_capture/adapters/browser_snapshot.py)
  (`_SCROLL_PASS_SETTLE_MS = 2000`); response read at `:737` immediately after
  the scroll loop returns.
- **Evidence/impact:** the per-pass settle is a fixed 2000 ms, not operator-
  controllable, and there is no extra settle or `networkidle` wait after the
  final pass before `_read_observed_page_responses`. The `page.on("response")`
  listener is registered before `goto` (`:701`) and is never removed, so it
  captures responses fired during the scroll and the final settle — but a slow
  widget that fires after the last 2 s window is missed (Review Q8). This is
  bounded-probe-acceptable and is honestly covered by the receipt non-claim
  "not proof that below-fold widgets fired" (`fragrance_rendered_widget_companion.py:146`).
- **Minimum closure condition:** none required; optionally expose the settle or
  add a final networkidle wait if a slow widget is observed to be missed.
- **Next authorized action:** optional future hardening; non-blocking.

---

### LZ-06 — Advisory — Scroll targets window only; inner-scroll/virtualized containers untriggered; step×passes interaction and cap undocumented in CLI

- **Severity:** advisory.
- **Location:** `_run_bounded_lazy_load_scrolls`
  [browser_snapshot.py:984-1013](orca-harness/source_capture/adapters/browser_snapshot.py)
  (`window.scrollTo` / `document.body.scrollHeight`); runner help at
  [run_fragrance_rendered_widget_companion.py:109-123](orca-harness/runners/run_fragrance_rendered_widget_companion.py).
- **Evidence/impact:** both paths scroll the window and read
  `document.body.scrollHeight`; widgets inside an inner `overflow`/scroll
  container or a virtualized list will not be triggered and may not be reflected
  in `scrollHeight` (Review Q5/Q6). Bottom-scroll mode jumps straight to the
  page bottom (may skip mid-page intersection-triggered loads); step mode is the
  mitigation but, with a small `--lazy-load-scroll-step-px` and few passes, may
  not reach far down. The CLI help documents neither the passes×step interaction
  nor the `_MAX_SCROLL_PASSES = 40` cap.
- **Minimum closure condition:** none required; optionally a residual marker
  ("scroll target window-only") and a CLI help note on step/passes and the cap.
- **Next authorized action:** optional future hardening; non-blocking. See
  recommendation on Q14 below — this does **not** argue for post-scroll DOM
  row parsing.

---

### LZ-07 — Advisory — No single marker correlates "scrolled N" with "observed 0 new widget responses"

- **Severity:** advisory.
- **Location:** route-health/residual assembly
  [fragrance_rendered_widget_companion.py:274-293](orca-harness/source_capture/fragrance_rendered_widget_companion.py).
- **Evidence/impact:** a silent lazy-widget miss surfaces only as the
  *combination* of `lazy_load_scroll_passes_executed:N` +
  `passive_widget_response_count:0` + residual
  `passive_widget_not_observed_during_render` + `fallback_needed` (Review Q13).
  Reasonably visible, but the reader must correlate fields; there is no explicit
  "scrolled but no new widget response observed" marker.
- **Minimum closure condition:** none required; optional explicit correlation
  residual.
- **Next authorized action:** optional future hardening; non-blocking.

---

### LZ-08 — Advisory — Unrelated trailing-newline EOF change in the runner

- **Severity:** advisory (scope hygiene).
- **Location:** end of
  [run_fragrance_rendered_widget_companion.py:179](orca-harness/runners/run_fragrance_rendered_widget_companion.py)
  (`\ No newline at end of file` removed in the diff).
- **Evidence/impact:** the diff adds a trailing newline to the runner's final
  line — a whitespace-only EOF change unrelated to lazy-load, in a file already
  touched for the feature. De-minimis; noted only against `AGENTS.md` "Smallest"
  (avoid unrelated changes). No behavioral impact.
- **Next authorized action:** none required.

## What Held (adversarial non-findings)

- **Q1/Q2 — no-scroll facts preserved, no DOM-row implication:** `rendered_companion`
  is built from the **pre-scroll** `dom_observation`/`visible_text`
  (`_rendered_companion_from_observation`, lines 390-415); responses are read
  after the scroll; the above-fold flags are computed from the pre-scroll item
  text. No DOM review-row parsing — rows derive from widget **response bodies**
  (`review_response_bodies`, lines 295-299). Held.
- **Q5 — bounded, no infinite scroll:** both scroll paths terminate via
  `min(scroll_passes, _MAX_SCROLL_PASSES)` (`:994`); expanding body height /
  long pages cannot loop unbounded. Held (subject to LZ-06 container note).
- **Q9 — fallback only after passive cannot complete:** `_fallback_needed`
  (lines 577-587) gates the bounded fallback **after** the (now scroll-broadened)
  passive coverage is built (lines 217-238); lazy scroll reduces fallback need,
  it does not bypass the gate. Held.
- **Q10/Q14/Q15 — claim discipline:** receipt `non_claims` include "not one
  literal HTTP request", "not source-wide review coverage", "not proof that
  below-fold widgets fired", "not durable Attachment Records", "not ECR,
  Cleaning, Judgment, pain/pleasure labeling, or review-integrity scoring"
  (lines 142-150); certification is `...; not_judgment_ready`. No DOM-row,
  completeness, sentiment, or buyer-proof claim. Held.
- **Q12 — backward compatibility:** the two new params default to `0` (no-op);
  the `BrowserPageObservationEngine` Protocol (`:165`), the
  `_PlaywrightBrowserSnapshotEngine` implementation (`:629`), the
  `fetch_browser_page_observation_capture` call site (`:405`), and the test fake
  all expose/route `capture_page_observation` consistently; negative values are
  rejected (lines 393-394). No fake-success via permissive defaults. Held.
- **Q11 (covered portion):** threading (fetch→engine, capture→fetcher,
  runner→write), negative-value validation, step-position math, and cap-count
  are all tested; 50 tests pass. (Gaps captured in LZ-01/LZ-03.)

## Not-Proven Boundaries / Strict-Only Blockers

- **No live smoke for the scroll option.** No new live retailer capture
  exercises `lazy_load_scroll_passes > 0` against a real lazy-loading PDP;
  unit coverage uses fakes only. Whether bounded scrolling actually triggers a
  real below-fold review widget is **not proven** here (and is honestly
  non-claimed by the receipt). Reviewable residual, not a failure.
- **Author lineage** (`codex/gpt-5`) is operator-attributed, not independently
  verified; `de_correlation_bar: cross_vendor_discovery` rests on that
  attribution plus the reviewer's own Anthropic/Opus identity.
- This review is **not** validation, readiness, acceptance, merge authority, or
  a delegated-review-patch result. It authorizes no source capture, patch,
  commit, push, live probe, or product/runtime use.

## Lazy-Load Capture Recommendation (Review Q14)

**Keep the bounded lazy scroll; do not add post-scroll DOM row parsing.** Sourcing
rows from widget responses + bounded fallback is the safer MGT boundary: the
`row_contract_v0` "Extraction Hard Lines" forbid emitting rows from DOM/aggregate
substrate and `focused_coverage_mgt_v0` keeps the widget route as the row
substrate with rendered PDP as fallback. A future post-scroll DOM observation
should be added — if ever — only as a clearly separate, non-row companion origin,
never as a review-row source. The one genuine residual to close before relying on
this in production is a **live smoke** of the scroll option (see Not-Proven).

## Review-Use Boundary

These findings are decision input only. This review does not approve, validate,
mandate remediation, authorize patches, commits, source capture, live probes, or
commercial/runtime use, and creates no ECR, Cleaning, Judgment, buyer-proof,
fixture-admission, or readiness evidence.
