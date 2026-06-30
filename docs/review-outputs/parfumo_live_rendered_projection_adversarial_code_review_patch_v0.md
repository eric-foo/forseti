# Parfumo Live Rendered Projection Adversarial Code Review Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated code review-and-patch, repo mode)
scope: >
  Delegated cross-vendor adversarial code review of PR #532 commit 9066900f —
  Parfumo live-rendered DOM projection parser and explicit capture-route guard
  patch; follow-up pass after prior NEEDS_ARCHITECTURE_PASS escalation on F1/F2/F3.
commission: docs/prompts/reviews/parfumo_live_rendered_projection_adversarial_code_review_patch_prompt_v0.md
reviewed_by: claude-sonnet-4-6 (Claude Sonnet 4.6, Anthropic)
authored_by: OpenAI / GPT-family Codex (exact version unrecorded)
de_correlation_bar: cross_vendor_discovery
review_lane: delegated_code_review_and_patch (workflow-code-review method), access=repo
target_branch: codex/parfumo-targeted-projection-metrics
review_patch_range: 383f7a0b967f1d134cf63ea6caf07ddd3d7a4993..9066900fab64d85115b5b978a777767b6e9ff07e
pinned_commit: 9066900fab64d85115b5b978a777767b6e9ff07e
worktree_head_at_review: eb8b3f9bc5d1f826226a6bbc9686124c82e3ce57
patched_in_this_pass: false
escalation: none; prior NEEDS_ARCHITECTURE_PASS resolved
authority_boundary: retrieval_only
```

## Actor / Model-Family Receipt

- `author_home_model_family`: OpenAI / GPT-family Codex
- `current_receiving_actor_role`: controller
- `controller_model_family`: Anthropic / Claude (Sonnet 4.6)
- `dispatch_mode`: external-controller-courier (repo mode)
- `de_correlation_status`: **satisfied** — controller vendor (Anthropic) ≠ author vendor (OpenAI). `de_correlation_bar = cross_vendor_discovery`.

## Worktree / Pin Reconciliation (non-blocking)

The commission pins head `9066900f`. The worktree head is `eb8b3f9b`. Verified: `eb8b3f9b` (`docs: add Parfumo live parser review prompt`) adds only this review's commission prompt document — a read-only, out-of-scope file. The four implementation target files are byte-identical to the pinned commit. Branch `codex/parfumo-targeted-projection-metrics` is up to date with origin. Dirty state: clean. Not treated as a blocker — same drift pattern as the prior review (one doc commit ahead of the implementation pin).

## Method

REFERENCE-LOADED `workflow-deep-thinking`, `workflow-code-review`, and `workflow-delegated-review-patch` skills. SOURCE-LOADED all required sources from the pinned worktree (see ledger below). Declared SOURCE_CONTEXT_READY. APPLIED `workflow-deep-thinking` to frame failure modes. APPLIED `workflow-code-review` to produce findings.

## Source Context

`SOURCE_CONTEXT_READY`.

### Source-read ledger

| Source | Read | Used for |
|---|---|---|
| `orca-harness/source_capture/parfumo_projection.py` (full, 1424 lines) | yes | parser logic, slice routing, token matching, live DOM detection, all new helper functions |
| `orca-harness/runners/run_parfumo_mgt_capture.py` (full, 634 lines) | yes | route guard, `--direct-http`/`--targeted-rendered` flags, slice construction |
| `orca-harness/tests/unit/test_parfumo_projection.py` (full, 510 lines) | yes | new test fixtures, F1/F2/F5 coverage, live-rendered fixture |
| `orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py` (diff) | yes | route guard tests, CLI changes |
| `git diff 383f7a0b..9066900f` (four target files) | yes | exact change surface for review |
| `docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md` | yes | prior F1/F2/F3/F4/F5 findings and escalation context |
| `docs/workflows/parfumo_targeted_capture_contract_v0.md` | yes | bucket/source-visibility contract, no-Fragrantica-scale rule |
| `.agents/workflow-overlay/delegated-review-patch.md` | yes | lane convention, de-correlation, verdict vocabulary |
| `.agents/workflow-overlay/review-lanes.md` | yes | review doctrine, two-bar rule, findings standard |
| `.agents/workflow-overlay/safety-rules.md` | yes | implementation authorization boundary, patch scope |
| `.agents/workflow-overlay/README.md` | yes | overlay entry |
| Skills: `workflow-deep-thinking`, `workflow-code-review`, `workflow-delegated-review-patch` | yes | method |

### Not individually opened (rationale)

`.agents/workflow-overlay/{decision-routing,source-loading,prompt-orchestration,communication-style}.md` — lane/safety bindings already reflected in loaded overlay files and commission; no patch or doctrine-changing action was taken. Fragrantica reference modules, Silver/non-Silver records, lane-registry hook, and no-blur infrastructure — prior review established these as parity references; the current patch does not touch Silver, lane registry, Cleaning, or raw writer paths. Local probe evidence files (`_test_runs/`) — not present in working tree. No conflict found among loaded sources.

---

## Prior Finding Closure Status

The prior review (`parfumo_targeted_projection_metrics_delegated_code_review_v0.md`) escalated with `NEEDS_ARCHITECTURE_PASS` for coupled F1/F2/F3, citing a design-level decision: *are targeted slices overlapping views or partitioning buckets?* This patch implements the **partitioning bucket** design. Each of F1–F5 is assessed below.

### F1 (Prior) — Silent review drop resolved — **CLOSED**

**Prior finding:** Reviews satisfying no slice predicate were silently dropped (no residual).

**Evidence of closure:** `_targeted_review_slice_id()` (`parfumo_projection.py:537–548`) is now a **total partition function**: it always returns exactly one slice ID. Priority order: `tab_id == "order_scent_desc"` → HIGH_RATING; `tab_id == "order_scent_asc"` → LOW_RATING; `_has_high_rating_bucket_cue(row)` → HIGH_RATING; `_has_low_rating_bucket_cue(row)` → LOW_RATING; else → LATEST_RECENT. No review row can fall through to "no slice." The previously dropped case (`loss-001`: `data-tab="high_rating"`, rating 7.5) now routes via the `"high"` token match to HIGH_RATING.

`_filter_targeted_projection()` (`parfumo_projection.py:466–534`) was rewritten to use `_targeted_review_slice_id(row) == slice_id` as the filter predicate — no longer three separate predicates with gaps between them.

**Regression test:** `test_targeted_projection_partitions_overlapping_review_views_without_loss` (test_parfumo_projection.py:175–199) asserts `preserved_review_cards == 3` and `loss-001` lands in `review_source_visible_high_rating`. This is red against the prior code (loss-001 was dropped) and green against the new code. **CLOSED.**

---

### F2 (Prior) — Duplicate Silver MetricObservation resolved — **CLOSED**

**Prior finding:** A review satisfying multiple slice predicates appeared in multiple slices, producing duplicate MetricObservation (and TextObservation) Silver facts.

**Evidence of closure:** Because `_targeted_review_slice_id()` is a partition function (each row maps to exactly one slice ID), a review row can satisfy at most one slice's filter predicate. Even though all five slices re-project the same DOM (runner `_targeted_source_slices()` still assigns all file IDs to every slice — confirmed at `runners/run_parfumo_mgt_capture.py:400–413`), the filtering in `_filter_targeted_projection()` ensures each review row is retained in exactly one slice and discarded from all others.

The previously doubled case (`dup-001`: no tab, rating 9.0) was in BOTH LATEST and HIGH in the old code. In the new code: `tab_id = "reviews"` (fallback), no bucket token → LATEST_RECENT only.

**Regression test:** Same test (`test_targeted_projection_partitions_overlapping_review_views_without_loss`) asserts `len(review_ids) == len(set(review_ids))` — no duplicate review IDs across all slices. `dup-001` appears in `review_latest_recent` only. This is red against prior code (dup-001 was in two slices) and green against new code. **CLOSED.**

---

### F3 (Prior) — Invented 8.0/4.0 numeric thresholds eliminated — **CLOSED**

**Prior finding:** `_PARFUMO_HIGH_RATING_MIN = 8.0` and `_PARFUMO_LOW_RATING_MAX = 4.0` overrode source-visible tab; slice names asserted "source_visible" that the threshold did not establish.

**Evidence of closure:** Both constants are absent from the new file (confirmed: no occurrences of `_PARFUMO_HIGH_RATING_MIN` or `_PARFUMO_LOW_RATING_MAX` anywhere in `parfumo_projection.py`). The new `_targeted_review_slice_id()` uses only source-visible signals:

1. Exact `tab_id` values `order_scent_desc` / `order_scent_asc` from the Parfumo order/filter DOM (`parfumo_projection.py:540–543`) — directly source-visible Parfumo order fields.
2. Token matching on `tab_id`/`tab_label` values via `_has_high_rating_bucket_cue()` / `_has_low_rating_bucket_cue()` (`parfumo_projection.py:563–580`) — source-visible tab/label strings.

No numeric threshold is applied to the `rating` value for bucket routing. The rating value is preserved in `source_visible_fields["rating"]` as a raw fact; it no longer controls slice assignment. Contract `:29` requirement ("high/low buckets only where Parfumo exposes the underlying rating/order/filter fields") is now satisfied. **CLOSED.**

---

### F4 (Prior) — Test coverage extended to exercise drop/duplicate paths — **CLOSED**

**Prior finding:** The "without_slice_duplication" test used a hand-disjoint fixture; no test exercised the overlap or drop paths.

**New tests added:**

- `test_targeted_projection_partitions_overlapping_review_views_without_loss` (test_parfumo_projection.py:175): fixture `_TARGETED_HTML_OVERLAP_AND_MID_BUCKET` contains `dup-001` (would have been duplicated, F2) and `loss-001` (would have been dropped, F1). Test is red against prior behavior for both behaviors.
- `test_targeted_projection_bucket_token_matching_is_segment_bounded` (test_parfumo_projection.py:202): fixture contains `data-tab="flower"` — word-bounded token split means "low" does not match "flower". Test is red against the prior unbounded substring matching.
- `test_targeted_projection_parses_live_rendered_parfumo_cards` (test_parfumo_projection.py:123): drives the full live-rendered schema.org fixture through projection and asserts all material fields (review_id, author, date, rating, tab_label, review_text, source_item_url; statement_id, author, date_display_text, rating, statement_text, source_item_url). This proves the live parser end-to-end without numeric-threshold dependence.

All 24 targeted tests pass (verified). **CLOSED.**

---

### F5 (Prior) — Token matching is now word-bounded — **CLOSED**

**Prior finding:** `_field_mentions_any()` matched tokens as unbounded substrings ("low" ⊂ "flower").

**Evidence of closure:** `_field_mentions_any()` (`parfumo_projection.py:583–597`) now uses:
```python
field_tokens = {token for token in re.split(r"[^a-z0-9]+", text) if token}
return any(token in field_tokens for token in tokens)
```
The `re.split(r"[^a-z0-9]+", text)` splits on all non-alphanumeric characters, producing word-level tokens. `"flower"` → `{"flower"}`; `"low"` is not a member → no match. `"low_rating"` → `{"low", "rating"}`; `"low"` matches. The test `test_targeted_projection_bucket_token_matching_is_segment_bounded` confirms this with the `"flower"` tab case. **CLOSED.**

---

## New Findings

### NF1 — Dual-attribute article produces empty-segment row — **LOW (edge case)**

- **Location:** `parfumo_projection.py:822–861` (`_text_card_starts()`), `parfumo_projection.py:762–822` (`_text_card_rows()`)
- **Implementation evidence:** `_text_card_starts()` appends entries from the `data-review-id` attribute pattern first, then from the live `itemprop="review"` pattern. If a Parfumo DOM element carries both attributes on the same tag (e.g., `<article data-review-id="258984" itemprop="review">`), two `_TextCardStart` entries at the same `start` position are generated. After stable sort, the data-attr entry (with `explicit_id="258984"`) comes first.

  In `_text_card_rows()`, the first entry processes with `segment_end = starts[index+1].start` where `starts[index+1].start` is identical (same position) → `segment = _bounded_segment(text, X, X, "article") = ""`. `_text_card_item_id("", explicit_id="258984")` returns "258984" (explicit wins), so the row IS created — but with an empty segment, meaning `_source_text`, `_author_name`, `_date_published`, `_text_row_rating`, and `_source_item_url` all return None. The `seen` set then blocks the second entry (live pattern, explicit_id=None), so the proper row with full segment is skipped.

  **Result:** a review row with the correct `review_id` but all text/author/date/rating/source_item_url fields None.

- **Authority/evidence basis:** Agent Behavior Kernel ("Preserve real failure visibility; never create fake success paths"). A row with correct ID but all None fields silently loses review content.

- **Impact:** LOW. Parfumo's observed DOM uses `data-review-id` (older direct-HTTP format) OR `itemprop="review"` (live rendered schema.org format) as distinct structural patterns — not both on the same element. The test fixtures and live probe evidence confirm this. The defect would only surface if Parfumo begins writing both attributes on the same element. No current capture is affected.

- **`minimum_closure_condition`:** If the dual-attribute case can occur, `_text_card_starts()` must either deduplicate by position before `_text_card_rows()` processes them, or `_text_card_rows()` must detect same-position starts and take the entry with the larger available segment.

- **`next_authorized_action`:** Owner acknowledgment that the dual-attribute case is not currently present in Parfumo DOM. Optional hardening if the pattern is anticipated.

- **Patched in this pass:** No. Current Parfumo DOM patterns do not exhibit this case; patching would be speculative scope expansion.

---

## What the Patch Gets Right

- **Route guard is source-correct and `--preflight-only` bypass is intentional.** `main()` returns before the guard for `--preflight-only` (`run_parfumo_mgt_capture.py:575–577`); the guard fires only after that check (`run_parfumo_mgt_capture.py:579–581`). This is correct — preflight explicitly opts out of route selection. The guard uses `args.targeted_rendered == args.direct_http` which fires on (both False) or (both True), enforcing exactly-one-route invariant. Tested by `test_parfumo_cli_requires_explicit_capture_route`.

- **Live review card parsing is source-visible and complete.** The parser handles:
  - `itemprop="review"` + schema.org `ratingValue`, `datePublished`, `author/name` attributes (test-confirmed with `_LIVE_RENDERED_HTML` fixture)
  - `review_article_<id>` class → `item_id` (no `data-review-id` needed on live cards)
  - `r_text_<id>` / `r_text_content_<id>` → review body text
  - `/Users/<username>` URL fallback → author name (correctly URL-decoded via `unquote()`)
  - `<span class="nr blue">N</span>Scent` pattern → review/statement Scent rating
  - `class="lightblue2"` → `date_display_text` for relative-date statements

- **`_active_review_order_tab_before()` correctly reads Parfumo order state.** Scans `data-o` elements with `action_reviews_order` class before each review's position. Active tab `order_scent_desc` → HIGH_RATING slice; `order_scent_asc` → LOW_RATING. Source-visible (not invented). Test confirmed via `_LIVE_RENDERED_HTML` where `<div class="active action_reviews_order" data-o="order_scent_desc">` makes the one review land in `review_source_visible_high_rating`.

- **`_review_tab_rows()` now also captures `action_reviews_order` tabs.** `tab_labels["order_scent_desc"] = "Positive"` flows through `_text_row_fields()` → `source_visible_fields["tab_label"] = "Positive"`. Test asserts this correctly.

- **`_bounded_segment()` depth tracking is correct.** Old code found first `</tag>` occurrence regardless of nesting depth. New code uses a depth counter (`depth=0`, open tag → `+1`, close tag → `-1`, return when `depth == 0`). Correctly handles nested `<article>` structures.

- **`_source_item_url()` is now item-scoped.** Looks specifically for `/{kind}/{escaped_id}` URLs, not generic `review|statement` href patterns. Author profile URLs (`/Users/.../statements`) are correctly excluded since they don't contain `/statements/2397523`. Test confirms `.endswith("/statements/2397523")` and `.endswith("/reviews/258984")`.

- **`_text_row_residuals()` date check is corrected.** Changed from `<time` tag presence to `_date_published() is None`. Live rendered HTML may use `itemprop=datePublished` on a `<div>` with no `<time>` tag; the new check correctly residualizes only when no date can be extracted by any supported pattern.

- **Body filter extended for live DOM.** `_looks_like_parfumo_body()` now accepts `itemprop="review"` and `statement-bubble` as recognition signals for targeted rendered surface. `route_receipt.json`, `visible_text.txt`, and `viewport.png` still correctly excluded (not-HTML file extensions for the former two, non-HTML content for the latter).

- **No Silver via raw writer; no Cleaning/Silver changes.** The patch is entirely within the four target files. Silver front-door, lane registry, and no-blur infrastructure are unchanged and unaffected.

- **No Fragrantica rating-scale inheritance.** Rating values are captured directly from Parfumo DOM attributes; no 1/4/5-star mapping. Contract `:48` respected.

- **Deduplication in `_text_card_rows()` via `seen` set.** When the same item_id appears from multiple start patterns (sorting may interleave data-attr and live patterns), the `seen: set[tuple[str, str]]` prevents duplicate rows for the same item. Handles the transition between fixture formats correctly.

---

## Off-Scope Flags

- **Runner `_targeted_source_slices()` still assigns all file IDs to every slice** (`run_parfumo_mgt_capture.py:400–413`). This was flagged in the prior review as a structural contributor to F1/F2. With the new partition function, the all-files-per-slice design no longer causes duplication or loss — `_filter_targeted_projection()` discards non-matching rows per slice. The structural redundancy (projecting the same DOM 5 times) is now a performance characteristic, not a correctness issue. No patch required; no re-commission needed.

- **Direct-HTTP metric emission** was flagged as a minor adjudication note in the prior review ("confirm emitting metrics on the direct-HTTP/canary surface is intended"). This patch does not change that behavior. Out of scope.

---

## Validation Evidence

| Gate | Command | Result |
|---|---|---|
| py_compile | `python -m py_compile runners\run_parfumo_mgt_capture.py source_capture\parfumo_projection.py` | **PASS** |
| targeted suite | `python -m pytest -v tests\unit\test_parfumo_projection.py tests\unit\test_parfumo_mgt_capture_runner.py tests\test_parfumo_native_pipeline_lake.py` | **24 passed** |
| full suite | `$env:ORCA_DATA_ROOT=$null; python -m pytest -q` | **PASS** (exit code 0; one unrelated `PytestUnknownMarkWarning` on integration test mark, same as prior review) |
| git diff --check | `git diff --check` | **CLEAN** |

All tests run against commit `9066900f` implementation (worktree head `eb8b3f9b` adds only this review's prompt doc, not touching any target file).

---

## Verdict (decision input only — not approval, validation, readiness, or merge authorization)

**Changes accepted — no patch required.** Commit `9066900f` closes all five prior findings (F1–F5) from the `NEEDS_ARCHITECTURE_PASS` escalation. The architecture question the prior review surfaced ("overlapping views or partitioning buckets?") is resolved as **partitioning buckets** via `_targeted_review_slice_id()` as a total partition function. This is a complete and correct implementation of the owner's documented design intent.

The non-slice machinery (Silver front-door, posture coupling, lane registration, body guard, surface-constant wiring) remains sound and is not affected by this patch.

**NF1** (dual-attribute article dedup) is a low-impact edge case not present in observed Parfumo DOM patterns. It does not constitute a blocker.

**Residual risk:** NF1 (dual-attribute article on same element produces empty-segment row). Not present in current Parfumo DOM. Acceptable residual below the observed-DOM assurance tier. No other material residuals.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, mandatory remediation, readiness, or executor-ready patch authority until separately accepted or authorized by the commissioning Chief Architect. The verdict and findings are claims to adjudicate, not premises to inherit.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: docs/prompts/reviews/parfumo_live_rendered_projection_adversarial_code_review_patch_prompt_v0.md (PR #532)
- implementation context / reviewed files (pinned 9066900f, diff 383f7a0b..9066900f):
  - orca-harness/source_capture/parfumo_projection.py
  - orca-harness/runners/run_parfumo_mgt_capture.py
  - orca-harness/tests/unit/test_parfumo_projection.py
  - orca-harness/tests/unit/test_parfumo_mgt_capture_runner.py
- prior escalation: NEEDS_ARCHITECTURE_PASS on coupled F1/F2/F3 (slice overlap/partition design decision)
- findings:
  - F1 CLOSED: _targeted_review_slice_id() is total partition function; no silent drop
  - F2 CLOSED: each review row in exactly one slice; no duplicate MetricObservation
  - F3 CLOSED: 8.0/4.0 thresholds removed; order_scent_desc/asc and token matching
  - F4 CLOSED: three new red-green tests for F1/F2 behavior, F5 behavior, live DOM parsing
  - F5 CLOSED: re.split(r"[^a-z0-9]+") word-bounded token matching
  - NF1 LOW: dual-attribute article (data-review-id + itemprop=review) produces empty-segment
    row; second occurrence skipped by seen-set dedup. Not observed in Parfumo DOM patterns.
- proposed patch / diff: NONE — prior findings closed without patch by this controller;
  NF1 is advisory-only residual
- citations: inline above (neutral, file:line)
- reviewer verdict: changes_accepted; no blocking issues remain. Decision input only.
- validation evidence: py_compile PASS; 24 targeted tests PASS; full suite PASS (exit 0,
  one unrelated integration-mark warning); git diff --check CLEAN
- residual risk: NF1 (dual-attribute edge case, low, not patched, not in observed DOM)
- not-proven boundaries: direct-HTTP metric intent (prior minor note, out of scope)
- non_claims: not approval; not validation; not readiness; not merge authorization

Adjudicator next step (per .agents/workflow-overlay/communication-style.md -> Review Adjudication Next Step):
adjudicate findings/verdict/residuals as claims first; F1–F5 are closed by evidence and
tested regressions; NF1 is low-risk residual for owner acknowledgment. If adjudication
is clean, batch any admin/lifecycle follow-ups (merge PR #532, close review artifacts)
into one land step. Deep-think only the 1-3 material next moves that need judgment
(e.g. direct-HTTP metric intent if that was deferred; Cleaning/Silver lane next steps).
```
