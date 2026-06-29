# Fragrance Auto Widget Parsing — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial implementation/code review output (read-only)
scope: >
  Read-only cross-vendor adversarial code review of PR #436 commit b6bbef42
  (auto Judge.me fallback derivation + Judge.me JSON and Yotpo v3 review-row
  parsing) across two source files and two test files in the fragrance
  purchase-review capture lane.
use_when:
  - Deciding whether the b6bbef42 auto-widget-parsing delta is mergeable or
    needs revision/hardening before merge.
  - Checking which provider-parser/fallback failure modes were attacked and
    which remain open.
authority_boundary: retrieval_only
review_mode: read_only_adversarial_code_review
output_mode: review-report
commission_prompt: docs/prompts/reviews/fragrance_auto_widget_parsing_delegated_adversarial_code_review_prompt_v0.md
branch_or_commit: codex/fragrance-purchase-review-probes @ b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
reviewed_delta: b8773277dd9858a60e72e8f512499fdfad4c4622..b6bbef420b88511cd7ea7008ec5a1eabd5ba5a9d
derived_from:
  orca-harness/source_capture/fragrance_rendered_widget_companion.py: 1D53A87197829CC8CB456C77761977D8242DB1722DADB3322A1578E83ECBB5D9
  orca-harness/source_capture/fragrance_review_coverage.py: AD8AAA0B2F371DA9F4E6DF4CDD60587A8326CD4C465020639A4E7A07A843CB93
  orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py: 194BB39091D3DE347A2E3FC094B9DF9CEC8D92CD4C64277ADE138468A9C26EEF
  orca-harness/tests/unit/test_fragrance_review_coverage.py: 6FFF1FC205AC6624AA618372C41F7727FF3D243E97F4532990BCC7363B3FA585
```

## Review Provenance

```yaml
reviewed_by: claude-opus-4-8
authored_by: codex / GPT-family lane (exact model/version unrecorded; per commission, b6bbef42 implementation authored via the Codex lane)
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable (cross-vendor: GPT-family author, Anthropic/Claude reviewer)
dispatch_mode: external-controller-courier (reviewer differs in vendor lineage from author)
no_model_recommendation: true   # provenance facts only; not a runtime-model recommendation, ranking, or selection
```

Cross-vendor discovery bar is satisfied: the patch and the commission prompt were authored by the GPT-family Codex lane; this review is performed by Claude (Anthropic). This is a who-constraint / measurement fact recorded as provenance, not runtime-model routing and not a model recommendation.

## Commission, Target, Authority

- **Commission:** filed delegated route-out for a read-only adversarial implementation/code review (not the single-file review-and-patch convention; this is a multi-file code diff, so no patch, no patch queue — per `.agents/workflow-overlay/delegated-review-patch.md`).
- **Target (delta only):** `b8773277..b6bbef42`, four files: `orca-harness/source_capture/fragrance_rendered_widget_companion.py`, `orca-harness/source_capture/fragrance_review_coverage.py`, and their two unit-test files. +464/-43.
- **Decision criteria / source authority:** the three behavior contracts —
  `fragrance_purchase_review_row_contract_v0.md`,
  `fragrance_purchase_review_focused_coverage_mgt_v0.md`,
  `fragrance_purchase_review_rendered_companion_probe_v0.md` — plus the
  fitness reference in the commission (preserve an adaptable rendered+widget
  capture route with explicit provider provenance and residuals; no
  overclaim of exhaustive scraping, integrity, sentiment, ECR/Cleaning/
  Judgment, validation, readiness, or buyer proof).
- **Authority boundary:** read-only review; findings are decision input only; severity labels are priority only and carry no formal verdict/validation/readiness/approval/remediation authority (`.agents/workflow-overlay/review-lanes.md`).

## Source Context

`SOURCE_CONTEXT_READY` — declared after loading all required authority, the three behavior contracts, the preflight defaults, all four target files, and the exact delta; verifying all four hash pins; clearing the staleness gate; and re-running the offline unit tests.

### Pre-review gates (observed)

- **Hash pins:** all four SHA256 pins match the worktree files (verified by `Get-FileHash`).
- **Staleness:** worktree HEAD is `3a17c548`, one commit ahead of the pinned `b6bbef42`; `b6bbef42` is a clean ancestor and the only later commit (`3a17c548`) adds **only** the review-prompt artifact (`docs/prompts/reviews/...`). No target file or source authority changed. `stale_if` not triggered.
- **Delta scope:** `git diff --name-status` confirms exactly the four pinned files changed in `b6bbef42`.
- **Tests (independently re-run by this reviewer):** `python -m pytest` on the two pinned offline test files at the worktree code → **26 passed, exit 0** (`..........................` — matches the author-reported result). These tests are network-free (capture tests inject fake fetchers; fallback-fetch tests monkeypatch `urlopen`).

### Source-read ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md`, overlay `README`, `source-of-truth`, `source-loading`, `delegated-review-patch`, `prompt-orchestration`, `review-lanes`, `validation-gates`, `template-registry` | Authority / claim boundaries / de-correlation rule | clean (matches origin/main doctrine state) |
| `fragrance_purchase_review_row_contract_v0.md`, `..._focused_coverage_mgt_v0.md`, `..._rendered_companion_probe_v0.md` | Behavior-contract authority (implementation fitness bar) | clean |
| `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` | Preflight constants | clean |
| 4 target files (source + tests) | Review object | clean; hashes verified |
| delta diff `b8773277..b6bbef42` | Attribute findings to this commit | clean |
| prior fragrance reviews under `docs/review-outputs/...` | available, **not read** — not decision-bearing for current code+contract | not loaded |
| `_test_runs/fragrance_live_widget_probe_after_patch_20260629/` | live-smoke receipts | available, **not read**; live-smoke summary in the commission is the author's reported observation (no live re-probe — forbidden by commission) |

### Method application

`workflow-deep-thinking` (failure-mode framing) and `workflow-code-review` (adversarial findings-first) were REFERENCE-LOADed before source loading and APPLIED only after `SOURCE_CONTEXT_READY`. Framing focused the attack on the three new capabilities: (1) auto Judge.me fallback derivation from rendered DOM, (2) Judge.me JSON review-list parsing, (3) Yotpo v3 row parsing — and on whether each preserves provenance/residual visibility without creating count-complete-but-substance-empty success.

---

## Findings (ordered by severity)

Severity labels are priority only (not verdict authority). No `patch_queue_entry` is emitted (read-only). Remediation directions are advisory prose.

### FAWP-01 — `major` — Auto fallback derives shop_domain/product_id by first-match over the whole page, unscoped to the Judge.me widget, and silently collapses multiple candidates

- **Location:** `fragrance_rendered_widget_companion.py` — `_DOM_EXTRACT_SCRIPT` provider-metadata block (`myshopify_domains`, `productIds`; ~lines 74–124) and `_derive_judgeme_fallback_from_dom_observation` (`_first_string`/`_first_numeric_string`; lines 632–673).
- **Implementation evidence:** `myshopify_domains: uniq(matchAll(/[A-Za-z0-9_-]+\.myshopify\.com/gi))` scans the entire `documentElement.outerHTML`; product ids are gathered from `.jdgm-widget`/`[data-widget-name="review_widget"]`, then **all** `[data-product-id]`, then six broad regexes including `gid://shopify/Product/(\d{6,14})` and `product_id["'\s:=]+["']?(\d{6,14})`. The Python side takes `_first_string(...)` and `_first_numeric_string(...)` — the first textual match — and records only the chosen `auto_judgeme_shop_domain`/`auto_judgeme_product_id`. The full candidate lists in `provider_metadata.judge_me` are discarded with no "multiple candidates observed" residual. `shop_domain` is never scoped to the Judge.me widget element's own config. When `judge_me.present` is true but domain/id are not derivable, the route is `{"auto_judgeme_detected": True}` with empty URLs and **no explicit "underivable" residual**.
- **Authority / evidence basis:** MGT drift contract — re-derive "`shop_domain`, product id, and Judge.me config from PDP scripts, Shopify product JSON, and widget params" (prefers widget-scoped derivation); row contract residual-visibility philosophy ("missing, weak, mismatched, or fallback fields stay visible"); `AGENTS.md` real-failure-visibility.
- **Impact:** On a noisy PDP (recommendations, related/recently-viewed products, embedded apps, multiple `myshopify` references, stale `gid`), the first textual match may be a non-canonical shop domain or a non-target product id. **Common case fails safe** — wrong params → empty Judge.me response → `fallback_needed` stays true → visible incomplete. **Worst case is silent provenance misattribution:** a wrong-but-valid `product_id` under the correct domain returns another product's rows, attributed to this `source_id`/`product_url`; the rows carry the other product's `product_url`/`product_title` while the receipt's `product_url` is the target, and nothing flags that mismatch. The multiple-candidate ambiguity and the detected-but-underivable case are also invisible.
- **minimum_closure_condition:** shop_domain derivation prefers the Judge.me widget element's own config over a whole-page regex; when more than one distinct shop_domain or product_id candidate is observed, the receipt records the candidate set plus a visible ambiguity residual; a "detected but domain/id underivable" residual is emitted; and a row-vs-receipt product mismatch (rows' `product_url`/id ≠ target) is surfaced as a residual rather than silently kept.
- **next_authorized_action:** owner/implementer decision on remediation scope; this lane is read-only (advisory only).
- **verification expectation (red-green):** add unit tests feeding `provider_metadata` with ≥2 `myshopify_domains` and ≥2 `product_ids` (including recommendation-style ids) — they should fail against current first-wins-silent behavior and pass once a deterministic widget-scoped pick and/or an ambiguity residual exists.

### FAWP-02 — `major` — Row "completeness" and the coverage summary ignore review-body presence (count-complete can mask body-empty)

- **Location:** `fragrance_rendered_widget_companion.py` `_fallback_needed` (lines 687–697); `fragrance_review_coverage.py` `_coverage_summary` (738–760) and `_normalize_reviews` body handling (586, 598–625).
- **Implementation evidence:** `_fallback_needed` returns `False` whenever `total_rows >= widget_total_count` (both present), regardless of how many rows actually carry `review_body_verbatim`. `_coverage_summary` reports `native_review_id_count`, `verified_true_count`, `media_true_count` — but **no body-present/body-absent count**. Body-less rows still count toward `total_rows`; the only signal that a row lacks text is the per-row `review_body_verbatim=None` plus the `review_body_absent` residual.
- **Authority / evidence basis:** row contract — `review_body_verbatim` "Required for usable row … If absent, do not emit usable row"; MGT decision — the focused corpus exists to give a reader pain/pleasure/integrity-readable **bodies**; `AGENTS.md` "never create fake success paths."
- **Impact:** rating-only reviews (common on Judge.me/Yotpo) yield body-less rows. A widget that returns count-matching but text-empty rows is marked `fallback_needed=False` ("complete") and may even select body-less rows for the reader, with no summary-level indication bodies are missing. A downstream agent reading the headline (`fallback_needed=False`, `selected_count`) can conclude bodies were captured when they were not. The truth is visible per row (so this is not fully hidden → `major`, not `critical`), but the success signal misrepresents body-level completeness.
- **minimum_closure_condition:** the coverage summary surfaces a body-present (and/or body-absent) count, and either `fallback_needed`/`route_health` or an explicit residual reflects when complete/selected rows lack bodies — so body-level completeness is visible at the summary layer, not only per row.
- **next_authorized_action:** owner/implementer decision; advisory only.
- **verification expectation (red-green):** a test with a review payload whose rows omit `body`/`content`/`body_html` should assert a body-absent count in the summary and that no unqualified "complete/green" signal is presented.

### FAWP-03 — `major` — Test gaps on the highest-risk new behaviors (auto-derivation edges + body-empty completeness)

- **Location:** `test_fragrance_rendered_widget_companion.py` (auto-derive coverage) and `test_fragrance_review_coverage.py` (body handling).
- **Implementation evidence:** `test_capture_auto_derives_judgeme_fallback_from_dom_metadata` exercises a single happy path: one `myshopify_domains` entry, one `product_ids` entry, `review_count=13` → 2 pages. There is **no** test for: (a) ≥2 candidate domains/ids and which is selected (or an ambiguity residual); (b) the `_AUTO_JUDGEME_FALLBACK_MAX_PAGES=5` cap and the `auto_judgeme_page_count_capped` field (needs `review_count > 50`); (c) `judge_me.present=true` with missing domain/id (`{auto_judgeme_detected: True}, []`); (d) body-empty rows (FAWP-02). Duplicate cross-page rows, PDP-vs-widget aggregate mismatch, widget aggregate fallback, and media false positives **are** covered.
- **Authority / evidence basis:** review-lanes / code-review red-green expectation; commission Review Question 11; `major` definition includes "high-risk test gap before merge."
- **Impact:** the riskiest new code (auto-derivation and body-empty completeness) is unverified at exactly its adversarial edges; wrong-selection or count-complete-but-empty regressions would not be caught.
- **minimum_closure_condition:** tests cover multi-candidate selection/ambiguity, the page cap plus its capped-count field, the detected-but-underivable path, and body-empty completeness.
- **next_authorized_action:** owner/implementer decision; advisory only.
- **verification expectation:** new tests fail against current behavior where FAWP-01/02 are unaddressed and pass once addressed.

### FAWP-04 — `minor` — `_html_to_text` does not skip `<script>`/`<style>`, and empty-but-present `body_html` overrides a non-empty `body`

- **Location:** `fragrance_review_coverage.py` `_TextOnlyHtmlParser` (312–322); `_parse_json_reviews` body precedence (522–524).
- **Implementation evidence:** `_TextOnlyHtmlParser.handle_data` appends every non-whitespace data run with no skip for `<script>`/`<style>` content. `body = item.get("body") or item.get("content") or item.get("body_html")`; then `if item.get("body_html") is not None: body = _html_to_text(...)` — `is not None` means a `body_html` of `""` overrides a non-empty `body` and yields an empty body.
- **Authority / evidence basis:** Review Question 5 ("without accidentally retaining … script text"); row contract `review_body_verbatim` = source body text (not markup/script).
- **Impact:** a `body_html` containing `<script>`/`<style>` would leak script/style text into `review_body_verbatim` (low likelihood; provider HTML is usually sanitized). Empty `body_html` + non-empty plain `body` yields an empty body (data loss, surfaces as `review_body_absent` — visible, not fake success). Both are low-likelihood edges.
- **minimum_closure_condition:** text extraction ignores script/style content; `body_html` is used only when non-empty (else fall back to `body`/`content`).
- **next_authorized_action:** advisory only.
- **verification expectation:** tests for `body_html` with embedded `<script>`/`<style>` and for `body_html=""` with a non-empty `body`.

### FAWP-05 — `minor` — Coverage-level residuals are not surfaced at the companion top level (the ZGO aggregate-mismatch case, Q13)

- **Location:** `fragrance_rendered_widget_companion.py` `build_fragrance_rendered_widget_companion_from_observation` residual assembly (407–420).
- **Implementation evidence:** the companion top-level `residuals` carries only companion-level signals (passive/fallback presence, parse failures, fallback-needed). `aggregate_review_count_widget_total_count_mismatch` and `media_filter_row_scan_mismatch` live **only** in `focused_review_coverage.residuals`. The commission's live-smoke summary reflects exactly this asymmetry — ZGO shows `coverage_residuals=aggregate_review_count_widget_total_count_mismatch` (nested) while the other four show `residuals=passive_widget_not_observed_during_render` (top level).
- **Authority / evidence basis:** Review Question 13; `AGENTS.md` real-failure-visibility; row-contract residual-visibility philosophy.
- **Impact:** a consumer scanning the companion top-level `residuals` for "is anything wrong" can miss material coverage-level residuals (aggregate mismatch, media mismatch) unless it also descends into the nested coverage receipt. Data is present but at an asymmetric layer.
- **minimum_closure_condition:** the companion makes coverage-level residuals discoverable at the top level (echo them, or add a compact pointer such as `focused_review_coverage_residuals_present`), or the receipt documents that readers must inspect the nested coverage residuals.
- **next_authorized_action:** advisory only.
- **verification expectation:** a test asserting that when the nested coverage carries a residual, the companion exposes it (or a pointer) at the top level.

### FAWP-06 — `minor` — Auto-fallback ignores operator-supplied `widget_route` shop_domain/product_id and always derives from DOM

- **Location:** `fragrance_rendered_widget_companion.py` `capture_fragrance_rendered_widget_companion` (262–301); `_derive_judgeme_fallback_from_dom_observation` (uses DOM only).
- **Implementation evidence:** the auto route/URLs are derived solely from `observation.dom_observation`; `widget_route` is merged for record-keeping (`effective_widget_route`) but its `shop_domain`/`product_id` are never used to build the fallback URLs. When `fallback_needed and not effective_fallback_widget_urls`, DOM-derived URLs are used even if the operator pinned an authoritative route. The operator must pass explicit `fallback_widget_urls` to control the fetch.
- **Authority / evidence basis:** MGT pinned-route doctrine (operator pins `shop_domain`/`product_id`); least-surprise.
- **Impact:** an operator who pins a correct route but relies on auto-fallback gets DOM-derived (possibly wrong, per FAWP-01) URLs instead of the pinned ones. Bounded — the operator can override via explicit fallback URLs, and the common (un-pinned) path is the intended one.
- **minimum_closure_condition:** auto-fallback prefers operator-supplied `widget_route` `shop_domain`/`product_id` when present, using DOM derivation only when they are absent.
- **next_authorized_action:** advisory only.
- **verification expectation:** a test asserting a pinned `widget_route` `shop_domain`/`product_id` is used to construct the auto-fallback URLs.

### FAWP-07 — `advisory` — Secondary observations (lower-risk; some pre-existing)

- **Row-level capture provenance (Q3, partly pre-existing):** `FragranceReviewCoverageRow` carries parser kind (`row_source`: judgeme_widget_html / widget_json_review / yotpo_v3_review) but **not** capture provenance (passive render vs bounded fallback) or `capture_route`. Per-response origin is preserved in `widget_responses[].response_origin`, and the coarse `passive_widget_not_observed_during_render` residual is present, but a reader cannot tell which response a given row came from. This matters if coverage rows are later promoted toward `candidate_fragrance_review_row_v0`, which the row contract requires to carry `capture_route` ("No row without route"). The coverage row does not yet claim to be that contract row (no `row_schema_version`), so this is advisory, not a contract violation.
- **Page-count from pre-fetch JSON-LD count can under-fetch:** `_derive_judgeme_fallback` sizes pages from the JSON-LD `review_count`. If that count is stale-low, fewer pages are fetched than the widget's true `total_count`; completeness is then judged against the widget's own `total_count`, so the receipt stays `fallback_needed=True` + mismatch residual (visible-incomplete, **not** false-green). Acceptable, but worth noting as a known bound.
- **Yotpo detection heuristic:** `_json_review_row_source` labels a JSON payload `yotpo_v3_review` only when it has both `bottomline` and `pagination` mappings — independent of the URL-derived `response_kind`. A Yotpo response whose body lacks one of those keys would be labeled `widget_json_review`. Low likelihood; the two provenance signals (URL kind vs body shape) could disagree.
- **JS `walk` keeps the last `aggregateRating`:** the in-page walk overwrites on each match, so the last-traversed aggregate wins. This only feeds the page-count sizing hint; the **authoritative** aggregate is re-parsed Python-side from `json_ld_texts` via `_aggregate_from_pdp_html`, so impact is limited to sizing.

---

## Verified-sound (adversarially checked, no finding)

- **No false-green on >50 reviews (Q2):** completeness is judged against the widget's own `total_count`, not the derived page count. A capped fetch (≤50 rows) against `total_count>50` keeps `fallback_needed=True` and adds `widget_total_count_deduped_row_count_mismatch`; the uncapped intent is recorded as `auto_judgeme_page_count_capped`. Stale-low/high JSON-LD counts also resolve correctly against the endpoint's own total.
- **Aggregate fallback rule correct (Q7):** PDP JSON-LD aggregate wins when present; the widget aggregate (`widget_json`) fills only when the PDP aggregate is absent; PDP-vs-widget count disagreement surfaces as `aggregate_review_count_widget_total_count_mismatch`. Test-confirmed.
- **Media detection (Q8):** JSON media keys are review-media-specific (`pictures`, `pictures_urls`, `videos`, `video_external_ids`, `imagesData`, `videosData`, `media_platform_hosted_video_infos`), counted only for non-empty lists; HTML media requires a `jdgm-rev__pics/pic/pic-link/vids/video` container ancestor, so avatars (`jdgm-rev__avatar`) and product-gallery images are excluded. Test-confirmed `media_true_count==1` against a fixture mixing real media + avatars.
- **Verified-purchase normalization (Q9):** `_bool_or_none` maps missing/unknown to `None` (not `False`); only `is True` is counted. Matches "never infer false from a missing verified label."
- **Native ids / candidate keys (Q10):** native id resolved from `id`/`review_id`/`uuid`/`sourceReviewId`; when absent, `review_key_status=candidate_key_only` + `candidate_key_only_weaker_than_native_id` residual + `candidate_key_basis`; dedupe by native id or candidate key. Within-capture stable; cross-capture instability is acknowledged by the contract ("only a replay handle").
- **Forbidden-label hygiene (Q12):** no ECR/Cleaning/Judgment/sentiment/integrity/buyer-proof output; the `_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES` validator rejects interpretation field names in `source_visible_fields`; certifications and `non_claims` are correctly scoped (`not_cleaned; not_judgment_ready`, etc.).
- **No arbitrary-fetch (SSRF) surface:** auto-derived fallback URLs always target the hardcoded host `https://api.judge.me/reviews/reviews_for_widget` (shop_domain/product_id are query params, not the host); fallback URLs are validated (`_validate_fallback_widget_url`) and cookie/set-cookie headers are stripped. A malicious DOM cannot redirect the fetch to an arbitrary host.

## Not-proven boundaries / strict-only blockers

- This review is **decision input only**. It is not approval, validation, readiness, acceptance, mandatory remediation, or patch authorization; severity labels are priority only.
- **Live retailer behavior not re-probed** (forbidden by the commission). The five-source live-smoke summary in the commission is the author's reported observation; this reviewer re-ran only the offline unit suite (26 passed). Whether the real Judge.me/Yotpo payloads of the five fixtures match the parsed shapes is not independently re-verified here.
- No runtime-model recommendation is made; the cross-vendor de-correlation is a who-constraint provenance fact.

## Review-use boundary

Findings are decision input only. This review does not approve, validate, mandate remediation, authorize patches, authorize commits, authorize source capture, authorize commercial/runtime use, or create ECR, Cleaning, Judgment, buyer-proof, fixture-admission, or readiness evidence. The Chief Architect/owner adjudicates what (if anything) is acted on.
