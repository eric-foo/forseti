# Fragrance Rendered Widget Companion Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output / read-only adversarial implementation-code review report
scope: >
  Read-only adversarial implementation/code review of PR #436 commit 7201e6c5
  (rendered fragrance PDP + widget response companion capture helper, runner,
  tests, package exports, and repo-map route). Findings are decision input only.
use_when:
  - Deciding whether the rendered+widget companion capture route honestly
    preserves above-fold rendered facts, same-load widget provenance, and
    bounded fallback row completion without overclaiming completeness.
  - Recovering the material implementation risks found in commit 7201e6c5 before
    any merge or follow-up implementation decision.
authority_boundary: retrieval_only
review_mode: read_only_adversarial_code_review
```

## Provenance

```yaml
reviewed_by: claude-opus-4.8
authored_by: codex/gpt-5  # per the review prompt's operator-attributed provenance note for 7201e6c5; not independently verified in this review
de_correlation_bar: cross_vendor_discovery  # Anthropic reviewer vs operator-attributed OpenAI author; cross-vendor. Author attribution is operator-supplied, not measured here.
same_vendor_rationale: not_applicable
```

This is a who-constraint / measurement record only; it does not select, rank, or
recommend any runtime model (review-lanes.md model-neutrality).

## Commission And Lane

- **Commission:** read-only adversarial implementation/code review of commit
  `7201e6c5e8902c0a2432906bbe50d388214a5179`, delta
  `6c730b31..7201e6c5`, in worktree
  `.codex/worktrees/fragrance-purchase-review-probes`.
- **Lane:** read-only implementation/code review (the prompt correctly routes a
  multi-file code diff *out* of the single-artifact `delegated-review-patch`
  convention; no patch authored). `workflow-deep-thinking` then
  `workflow-code-review` applied after source readiness.
- **Output:** this durable report (review-report mode); chat returns a summary
  plus the `review_summary` courier YAML.
- **Severity labels** (`critical`/`major`/`minor`/`advisory`) are finding
  priority only. Per `review-lanes.md` they create no approval, rejection,
  readiness, validation, or mandatory-remediation authority. No
  `patch_queue_entry` is emitted; remediation direction is advisory prose only.

## Source Context And Verification

- **Hash pins:** all 5 target and 3 support SHA256 pins verified equal to the
  pinned values (`Get-FileHash -Algorithm SHA256`). No `HASH_MISMATCH`.
- **Required source basis:** all 13 `blocked_if_missing` / Required-Source-Basis
  files PRESENT and loaded (AGENTS.md, the 7 named overlays, preflight defaults,
  3 spine contracts). → **`SOURCE_CONTEXT_READY`**.
- **Git state:** branch `codex/fragrance-purchase-review-probes`; base
  `6c730b31` and target `7201e6c5` both resolve; `diff --stat` confirms the
  5-file delta (991 insertions, 3 deletions). Worktree HEAD is at a *later*
  commit `43e7f4a4` ("Add fragrance rendered companion review prompt"), but the
  pinned target files still hash-match the pins, so the working tree faithfully
  reflects the reviewed state. Overlays/spines were read at the worktree
  checkout; their clean-vs-origin state is not asserted (support context, not
  the review target).
- **Boundaries honored:** no edits to source, no patch queue, no live retailer
  probes, no network fetches, no review bodies moved into tracked docs.

## Findings (ordered by severity)

No `critical` findings. Three `major`, four `minor`, six `advisory`.

---

### F1 — `major` — `fallback_needed` goes silently green when `widget_total_count` is absent

- **Reviewed target/role:** `fragrance_rendered_widget_companion.py` (companion helper) + `fragrance_review_coverage.py` (delegated coverage builder).
- **Location:** [`_fallback_needed`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (lines 546–554); coverage `widget_total_count` derivation [`fragrance_review_coverage.py:386`](orca-harness/source_capture/fragrance_review_coverage.py) and lines 395–396, 422–425.
- **Evidence:** `_fallback_needed` returns `True` only when `coverage is None`, `total_rows == 0`, or (`widget_total_count is not None` and `total_rows < widget_total_count`). When a review body yields rows (`total_rows > 0`) but **no** response body carried `total_count`, `widget_total_count` stays `None`, the third clause is skipped, and the function returns `False`. The coverage builder emits **no** residual for an absent `total_count` (it only adds `widget_total_count_present` / `..._mismatch` when the value *is* present), and the companion emits no residual either. So the receipt headline `fallback_needed: false` and an empty completeness-residual set can both appear while true row-completeness is unknown.
- **Authority/evidence basis:** focused-coverage MGT spine "Drift And Fallback Contract" — "The route is healthy when ... response is parseable JSON with an `html` field and `total_count`": `total_count` is a stated health precondition; its absence is an unhealthy/uncertain state, not a complete one. Prompt `fitness_reference` (receipt "must not imply ... source-wide review scraping" and must stay "honest about which data was observed ... versus completed by bounded fallback").
- **Impact:** the core success signal of the route — "are review rows complete, or is fallback needed?" — can read complete/not-needed when completeness is actually unverifiable. A downstream reader treating `fallback_needed=false` as "rows complete" is misled, with no residual to warn them.
- **Minimum closure condition:** when `widget_total_count is None` and `total_rows > 0`, the route must not present an unqualified not-needed/complete state — at minimum emit an explicit completeness-unverified residual (e.g. `widget_total_count_absent_completeness_unverified`) and/or treat completeness as unknown rather than satisfied.
- **Next authorized action:** owner/implementer decision; revise before merge; re-review the changed gating logic. **Escalates to `critical`** if any production review endpoint in scope returns rows without a `total_count` the builder reads (see F2).
- **Verification expectation:** add a unit test that builds coverage from a rows-present / `total_count`-absent body and asserts the receipt does not present silent completeness (red-green on the new residual/semantics). No `patch_queue_entry` (read-only lane).

---

### F2 — `major` — coverage completeness/parse assumes Judge.me-shaped bodies; Yotpo v3 review bodies are admitted but unverified

- **Reviewed target/role:** companion → coverage integration seam.
- **Location:** companion review-body handoff [`fragrance_rendered_widget_companion.py:282`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (lines 282–309); `_REVIEW_RESPONSE_KINDS` line 77 (admits `yotpo_v3_reviews`); coverage parse [`fragrance_review_coverage.py:388`](orca-harness/source_capture/fragrance_review_coverage.py) (lines 388–404) and `_parse_json_reviews` lines 473–496.
- **Evidence:** the URL classifier admits `yotpo_v3_reviews` as a review kind, and the companion feeds those bodies into `build_fragrance_review_coverage`, which derives completeness from `parsed.get("total_count")` and rows from `parsed.get("html")` or `parsed.get("reviews")` with row fields `rating|score` / `body|content` / `created_at|date`. The builder is Judge.me-shaped; `_parse_json_reviews` has partial Yotpo tolerance (`score`, `content`) but `total_count` and the rows-container key are Judge.me names. No Yotpo v3 fixture or test exists (tests use only Judge.me-shaped JSON).
- **Authority/evidence basis:** row-contract spine assigns ZGO Perfumery to the **Yotpo v3** storefront route; repo-map delta claims the helper "emits the focused coverage subreceipt." **Not-proven element:** the actual Yotpo v3 storefront reviews JSON shape (e.g. whether its total lives under `total_count` vs a `pagination` field, and its row field names) was not inspected in this read-only review.
- **Impact:** for the Yotpo-backed source (ZGO), the focused-coverage subreceipt may parse zero/incomplete rows (→ `widget_response_N:review_rows_absent`) and/or leave `widget_total_count` `None` (→ compounds the F1 silent green), while the receipt still reports a coverage subreceipt as if it succeeded.
- **Minimum closure condition:** verify the coverage builder against a real Yotpo v3 storefront reviews body (fixture) for total-count and row-field extraction; either confirm parity or explicitly scope the companion's coverage to Judge.me and residualize Yotpo bodies as preserved-but-not-parsed.
- **Next authorized action:** owner/implementer verification with a Yotpo fixture; revise or scope. No `patch_queue_entry`.

---

### F3 — `major` — test coverage omits the safety-bearing, failure-visibility, and false-green paths

- **Reviewed target/role:** `test_fragrance_rendered_widget_companion.py`.
- **Location:** [`test_fragrance_rendered_widget_companion.py`](orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py) (4 tests). Test 3 injects a fake `fallback_fetcher`, so the real fetch + URL validation never execute.
- **Evidence:** present tests cover passive success, incomplete-rows→fallback_needed, fallback-fires-when-passive-absent, and the URL filter. **Untested:** `_validate_fallback_widget_url` rejection (unsupported host, embedded credentials, non-http scheme); the real `_fetch_fallback_widget_response` path (HTTP error → `status=0, ok=False`; cookie/Set-Cookie stripping; over-cap body → empty + note; network exception → status-0); malformed fallback JSON (`widget_review_coverage_parse_failed` residual); duplicate-only / partial / non-200 fallback bodies; fallback-needed-but-no-URLs (the `not fallback_widget_urls` early return); mixed passive+fallback both present; the F1 `widget_total_count`-absent false-green; any Yotpo v3 body (F2).
- **Authority/evidence basis:** `validation-gates.md` — "Validation must be able to fail. Missing evidence is not a pass." Prompt review question 11 enumerates exactly these gaps.
- **Impact:** the SSRF-containment validation, the failure-visibility fetch path, and the core completeness signal are all unproven; regressions in any would pass CI silently.
- **Minimum closure condition:** add unit tests for URL-validation rejection, the real fetch error/status-0/cookie-strip/over-cap behavior, malformed/duplicate/partial/non-200 fallback bodies, the fallback-disabled branch, mixed passive+fallback, the `widget_total_count`-absent false-green, and a Yotpo v3 body fixture.
- **Next authorized action:** owner/implementer; revise before merge. No `patch_queue_entry`.

---

### F4 — `minor` — separate per-origin dedup can double-count id-less reviews captured by both render and fallback

- **Location:** companion [`_widget_response_captures`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) called twice with independent `seen` sets (lines 267–273, 393–402); coverage dedup [`_dedupe_rows`](orca-harness/source_capture/fragrance_review_coverage.py) (585) and the ordinal-bearing `_candidate_review_key` (767–788), with global ordinals assigned at `fragrance_review_coverage.py:402`.
- **Evidence:** passive and fallback captures dedup `(requested_url, status)` separately, so a URL+status fetched both passively and via fallback is preserved once per origin. Both bodies feed coverage. Rows **with** native ids dedup correctly; rows **without** native ids fall back to `candidate_review_key`, which includes `row_ordinal`, and ordinals increase globally across response bodies — so the same id-less review in two bodies gets two keys and is **not** deduped → inflated `total_rows`/`rating_counts`, which can also mask completeness vs F1.
- **Authority/evidence basis:** row-contract spine — the candidate key "is only a replay handle, not dedupe." Within-origin `(url,status)` collapse of genuinely different bodies (e.g. SSR re-hydration of the same URL) is a related but low-likelihood concern (vendors paginate via distinct query URLs).
- **Impact:** low in practice (Judge.me/Yotpo rows carry native ids), real for id-less rows captured by both origins.
- **Minimum closure condition:** dedup widget responses across origins by `(url,status)` (preserving an origin annotation), or document why per-origin preservation is intended and make coverage dedup origin-stable for id-less rows.
- **Next authorized action:** advisory; owner decision.

---

### F5 — `minor` — a bad `--fallback-widget-url` discards an otherwise successful render

- **Location:** [`capture_fragrance_rendered_widget_companion`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (fallback runs after render, 209–219); validation only inside the fetcher [`_validate_fallback_widget_url`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (494–507); runner abort [`run_fragrance_rendered_widget_companion.py:150`](orca-harness/runners/run_fragrance_rendered_widget_companion.py).
- **Evidence:** `_validate_fallback_widget_url` is reached only inside `fetch_fragrance_widget_fallback_responses`, which runs **after** the (expensive) Playwright render and only when `fallback_needed`. A rejected URL raises `FragranceRenderedWidgetCompanionInputError`, which propagates up through `write_…` and is caught by the runner as `exit 2` — no receipt is written, so the successful render is lost.
- **Authority/evidence basis:** AGENTS kernel — preserve real failure visibility / smallest-complete robustness; operating-economy (avoid no-value rework).
- **Impact:** an operator typo in an optional arg throws away the primary capture; recoverable only by re-running the full render.
- **Minimum closure condition:** validate fallback URLs before the render (fail fast), or record the rejection as a residual and still write the passive receipt.
- **Next authorized action:** advisory.

---

### F6 — `minor` — above-fold visibility heuristics use unbounded substring matching (false positives)

- **Location:** [`_rendered_companion_from_observation`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (377–382) and [`_contains_any`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (775–777).
- **Evidence:** `_contains_any` does casefold substring matching with no word boundary. `"review"` matches `"preview"`/`"reviewer"` (→ `rating_or_review_count_visible`, `review_section_visible`); `"ml"` matches `"html"`/`"xml"` (→ `size_or_variant_visible`); `"ready in"` matches `"already in"` (→ `stock_or_pickup_visible`).
- **Authority/evidence basis:** rendered-companion probe — these fields mean a signal "actually visible before scroll"; `fitness_reference` (honest above-fold facts).
- **Impact:** presentation-salience booleans can read `True` spuriously. Bounded — these are salience signals, not row-integrity; raw item text is still preserved.
- **Minimum closure condition:** use word-boundary / token matching for short or substring-prone tokens (`"ml"`, `"review"`, `"ready in"`).
- **Next authorized action:** advisory.

---

### F7 — `minor` — rendered companion omits the `rendered_locale_residuals` the probe contract requires

- **Location:** [`_rendered_companion_from_observation`](orca-harness/source_capture/fragrance_rendered_widget_companion.py) (no locale residual; 476–499) and `_price_pattern` line 779–780.
- **Evidence:** `FragranceAboveFoldCompanion` carries `price_visible` as a bare boolean and emits no currency/locale residual; `_price_pattern` even matches `s$`/`sgd`, yet an SGD price still yields `price_visible=True` with no locale caveat.
- **Authority/evidence basis:** rendered-companion probe explicitly enumerates `rendered_locale_residuals` as one of the six companion fields and devotes a residual to it ("price/currency is not yet US-storefront-pinned ... price should be treated as display-context evidence"; Twisted Lily rendered as SGD).
- **Impact:** locale/currency-sensitive prices are presented as plain visible facts with no structured residual. Understated, not hidden (raw currency text remains in `items`), but a named-contract field is absent.
- **Minimum closure condition:** emit a locale/currency residual (e.g. when non-USD currency markers are present) before any buyer-facing pricing use.
- **Next authorized action:** advisory.

---

### Advisories (optional hardening; non-blocking)

- **A1 — fallback fetch trust boundary.** `_validate_fallback_widget_url` validates only the *requested* URL; `urllib.request.urlopen` follows redirects to arbitrary hosts, so the body can be fetched from an unvalidated final host (recorded in `final_url`). Allowlisted hosts (`api.judge.me`, `api-cdn.yotpo.com`) keep this low-risk, and `http://` is also permitted (cleartext). Consider rejecting redirects to non-allowlisted hosts and requiring `https`. (`:429`–451, 494–507)
- **A2 — "bounded" fallback is operator-bounded only.** `--fallback-widget-url` is repeatable with no count cap; "bounded" relies on the operator. Consider a count cap or disclosing the fallback request count in `route_health`. (runner `:83`–91)
- **A3 — oversize detection via single read (low confidence).** `_read_response_body_with_cap` reads `max_response_bytes + 1` in one `.read()`; a short read on a chunked/streamed response could under-detect oversize. Usually safe for `HTTPResponse`; flag only. (`:478`–483)
- **A4 — above-fold item cap without residual.** `_DOM_EXTRACT_SCRIPT` caps `items` at 160 and dedups by `(top,left,text)`; nested `innerText` duplication can consume slots and silently drop distinct items, with no truncation residual. (`_DOM_EXTRACT_SCRIPT` line 71; `_normalize_items` 563–583)
- **A5 — row-level origin not preserved.** Provenance is response-level (`response_origin`), but `focused_review_coverage` rows do not carry which origin (render vs fallback) produced them. Acceptable per spine; note as a limitation if row-level provenance later matters.
- **A6 — companion `non_claims` is a subset of the spine non-claims.** It omits sentiment / demand / buyer-proof / credibility / validation / readiness / fixture-admission. Risk is low (the coverage row field-name validator structurally blocks interpretation field names, and `certification` says `not_judgment_ready`); consider mirroring the fuller spine list. (`:141`–149)

## Design Recommendations (review questions 8–9; assess only, not patched)

- **Q8 — bounded DOM/interaction stage for lazy widgets → `add_bounded_dom_trigger`.** `capture_page_observation` currently does **not** scroll (only the unused `capture` path exposes `scroll_passes`/`scroll_step_px`), so widgets that fire only on scroll never appear in passive capture and depend wholly on operator-supplied fallback URLs. Minimum design constraints: extract above-fold geometry **before** any scroll (preserve true first-viewport facts); bound passes (reuse `_MAX_SCROLL_PASSES`); settle between passes; rely on the existing `page.on("response")` listener to preserve newly-fired widget traffic; then optionally extract review-section DOM. Failure modes to guard: layout shift altering above-fold facts (mitigated by extract-first), infinite scroll (cap), cost/over-capture, and click-only (non-scroll) lazy widgets.
- **Q9 — parse rendered DOM rows as a third origin → keep widget fallback as the only row source for now.** Note Judge.me HTML-in-JSON is *already* handled (coverage parses `parsed["html"]`); the genuine gap is SSR/DOM-only reviews with no API response. A `rendered_dom_review_rows` origin would carry real risk: no stable cross-site DOM contract (unlike widget JSON), harder dedup against API rows, and conflation of rendered-DOM provenance with source-API provenance. Recommend adding it only as a clearly-labeled third `row_source` with its own weaker-key residuals, and only when widget API rows are truly absent.

## Review Question Disposition

| # | Question | Disposition |
| --- | --- | --- |
| 1 | Preserves rendered / passive / fallback distinction? | **Yes (strength).** `response_origin`, `route_health` counts, and origin residuals make provenance explicit. Limitation: A5 (no row-level origin in coverage). |
| 2 | `fallback_needed` falsely green on empty/malformed/dup/partial bodies? | **Yes — F1** (rows present + `total_count` absent → silent green), compounded by **F2**. Empty/parse-fail/dup-only cases otherwise stay red correctly. |
| 3 | Dedup by `(requested_url, status)` risks? | **F4** — cross-origin double-count for id-less rows; within-origin masking low-risk (vendors paginate via distinct query URLs). |
| 4 | Fallback bounded enough (validation, caps, timeout, headers, failure)? | **Mostly.** Cookie-strip, timeout>0, byte cap, and failure-as-status-0 are sound; gaps: A1 (redirect/https), A2 (count cap), A3 (oversize read), F5 (validate-after-render). |
| 5 | Overclaims one command = one HTTP request? | **No (strength).** `non_claims` includes "not one literal HTTP request"; runner help says "in the same operator command"; certification `passive_first_bounded_fallback`. |
| 6 | Back-compat risk from `passive_widget_responses` → `widget_responses`? | **No durable risk.** Grep finds `passive_widget_responses` only in the review prompt itself — no prior shipped field/consumer exists; this is a new model. Exports (`__init__.py`) and tests cover the new shape. |
| 7 | Render observation sufficient / false positives? | **F6** (substring heuristics), **A4** (160-cap + nested-text duplication). `block_heavy_assets` defaults `False`, so default capture does not shift layout. |
| 8 | Add bounded DOM/interaction stage? | **`add_bounded_dom_trigger`** — see Design Recommendations. |
| 9 | DOM rows as third origin? | **Keep widget fallback primary**; DOM rows only as a labeled third origin — see Design Recommendations. |
| 10 | Avoids ECR/Cleaning/Judgment/sentiment/etc.? | **Yes (strength).** `not_judgment_ready` certification, `non_claims`, and the coverage row field-name validator (`_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES`). Minor: A6. Selection-policy curation lives in the prior-commit support file (out of target scope) and is disclosed as focused coverage. |
| 11 | Tests strong enough? | **No — F3** (major test gaps on validation, fetch, false-green, Yotpo). |
| 12 | Repo-map wording accurate? | **Yes (strength).** Accurately describes the helper/runner, says "not ECR, Cleaning, or Judgment," and does not overclaim completeness or review readiness. |

## Strict-Only Blockers / Not-Proven Boundaries

- **Yotpo v3 body shape not verified** (F2): the actual ZGO/Yotpo storefront reviews JSON was not inspected; the integration concern is evidenced but its exact failure is `not proven`.
- **Live fetch path not executed** (read-only commission; no live probes): runtime behavior of `_fetch_fallback_widget_response` against real endpoints is `not proven` here; the author's reported smoke (`fallback_count: 2`, `total_rows: 14 == widget_total`) is recorded as author-supplied evidence, not independently reproduced.
- **No formal verdict / validation / readiness / approval** is created by this review; the recommendation below is decision input only (review-lanes.md). Severity labels are priority-only.
- **Reviewed state fidelity:** worktree HEAD `43e7f4a4` is later than target `7201e6c5`, but pinned target files hash-match, so the reviewed bytes are faithful; overlay/spine clean-vs-`origin/main` state is not asserted.

## Strengths (brief)

Provenance design is the artifact's strongest aspect: explicit per-response `response_origin`, origin-counted `route_health`, honest `non_claims`/`certification`, a structural interpretation-field-name guard in the coverage row model, and accurate non-overclaiming repo-map text. The passive-first / bounded-fallback split is a clean, honest shape.

## Review-Use Boundary

These findings are decision input only. This review does not approve, validate,
mandate remediation, authorize patches, authorize commits, authorize source
capture, authorize commercial/runtime use, or create ECR, Cleaning, Judgment,
buyer-proof, fixture-admission, or readiness evidence.

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_rendered_widget_companion_adversarial_code_review_v0.md
  review_mode: read_only_adversarial_code_review
  recommendation: revise_before_merge
  findings_count:
    critical: 0
    major: 3
    minor: 4
    advisory: 6
  blocking_or_major_findings:
    - "F1: fallback_needed goes silently green when widget_total_count is absent but rows exist (no completeness residual)"
    - "F2: coverage completeness/parse assumes Judge.me-shaped bodies; admitted Yotpo v3 bodies (ZGO) unverified, compounds F1"
    - "F3: tests omit URL-validation, real fetch/error path, false-green, and Yotpo body coverage"
  strict_only_blockers_or_not_proven_boundaries:
    - "Yotpo v3 reviews JSON shape not inspected (read-only): F2 failure is evidenced but not proven"
    - "Live fallback fetch not executed; author smoke recorded as author-supplied, not reproduced"
    - "No formal verdict/validation/readiness created; severity labels are priority-only; recommendation is decision input"
  dom_lazyload_recommendation: add_bounded_dom_trigger
  next_action: "Owner/implementer: close F1 (honest completeness when total_count absent) + F3 (test the safety/fetch/false-green paths), verify F2 against a real Yotpo v3 body, then re-review the changed gating + tests."
```
