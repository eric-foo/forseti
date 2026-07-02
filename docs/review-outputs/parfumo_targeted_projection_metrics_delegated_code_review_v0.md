# Parfumo Targeted Projection Metrics — Delegated Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated code review-and-patch, repo mode)
scope: Delegated cross-vendor code review of PR #532 — Parfumo targeted rendered projection / Cleaning / Silver MetricObservation changes.
commission: docs/prompts/reviews/parfumo_targeted_projection_metrics_delegated_code_review_prompt_v0.md
reviewed_by: claude-opus-4-8 (Claude Opus 4.8)
authored_by: OpenAI / GPT-family Codex (exact version unrecorded)
de_correlation_bar: cross_vendor_discovery
review_lane: delegated_code_review_and_patch (workflow-code-review method), access=repo
target_branch: codex/parfumo-targeted-projection-metrics
reviewed_commit: 3b6452cb6a6f4f906e1f21b3212970ce8745273a
worktree_head_at_review: af8223f87ce5aa7d562663d8ab5281ea6cc6c47d
expected_base: origin/main @ 65105faddeb73be50bf800c24f99e43c2df5c23e
patched_in_this_pass: false
escalation: NEEDS_ARCHITECTURE_PASS (coupled F1/F2/F3 — see Verdict)
authority_boundary: retrieval_only
```

## Actor / Model-Family Receipt

- `author_home_model_family`: OpenAI / GPT-family Codex
- `current_receiving_actor_role`: controller
- `controller_model_family`: Anthropic / Claude (Opus 4.8)
- `dispatch_mode`: external-controller-courier
- `de_correlation_status`: **satisfied** — controller vendor (Anthropic) ≠ author vendor (OpenAI). `de_correlation_bar = cross_vendor_discovery`.

## Worktree / Pin Reconciliation (non-blocking)

The prompt pins head `3b6452cb`; the worktree head is `af8223f8`. Verified
(`git merge-base --is-ancestor`, `git log 65105fad..HEAD`): `af8223f8` is exactly
`3b6452cb` **plus one commit** (`af8223f8 "Add Parfumo delegated review prompt"`)
that adds only this review's prompt doc — a read-only / out-of-scope file. The
implementation under review (the 6 target files = 710 insertions / 28 deletions)
is byte-identical to the pinned commit. Branch, base merge-base, and clean
dirty-state all match the prompt. Reviewed against the pinned implementation diff
`65105fad..3b6452cb`. Not treated as a blocker.

## Source Context

`SOURCE_CONTEXT_READY`.

### Source-read ledger (load-bearing reads)

| Source | Read | Used for |
|---|---|---|
| `orca-harness/source_capture/parfumo_projection.py` (full) | yes | slice filtering, bucket predicates, thresholds, row-id scoping, body guard |
| `orca-harness/cleaning/parfumo.py` (full) | yes | rating-carry transform per review card |
| `orca-harness/cleaning/parfumo_lake.py` (full) | yes | metric record emission, subject, coverage residual, front-door use |
| `orca-harness/runners/run_parfumo_mgt_capture.py` (full) | yes | slice/file assignment (all files → every slice), surface constant |
| `orca-harness/tests/*` (the 3 PR test files, via diff) | yes | what behavior the suite proves vs leaves unproven |
| `docs/workflows/parfumo_targeted_capture_contract_v0.md` | yes | bucket/source-visibility contract, no-Fragrantica-scale rule, batch scope |
| `orca-harness/data_lake/silver_record.py` (full) | yes | Silver front-door + MetricObservation posture coupling |
| `orca-harness/data_lake/lane_registry.py` (full) | yes | `cleaning_parfumo_silver` lane role |
| `orca-harness/cleaning/fragrantica_lake.py` (full) | yes | parity reference for metric emission |
| `.agents/workflow-overlay/review-lanes.md`, `delegated-review-patch.md` | yes | lane, verdict vocabulary, de-correlation, escalation |
| Skills: `workflow-deep-thinking`, `workflow-code-review`, `workflow-delegated-review-patch` | yes | method |

### Not individually opened (rationale; not load-bearing for findings)

`.agents/workflow-overlay/{README,decision-routing,source-loading,prompt-orchestration,safety-rules}.md`
(lane/safety bindings are reflected in the prompt commission and in
`delegated-review-patch.md`/`review-lanes.md`, which were read; no patch or
forbidden action was taken); `docs/research/orca_fragrance_native_database_live_probe_v0.md`
and the historical handoff packet (background); `fragrantica_projection.py`,
`cleaning/fragrantica.py`, the two Fragrantica tests, `data_lake/non_silver_record.py`,
`.agents/hooks/check_silver_lane_registry.py` (parity/guard context already
covered by `fragrantica_lake.py`, `silver_record.py`, and `lane_registry.py`).
No conflict was found in the sources that were read. None of the unread sources
is load-bearing for the findings below.

## Method

Per the Source-Gated Method Contract: REFERENCE-LOADED the three method skills,
SOURCE-LOADED the above, then APPLIED `workflow-deep-thinking` to frame failure
modes and `workflow-code-review` to produce findings. Findings were additionally
**empirically demonstrated** with a read-only probe (temp dir only; no repo file
touched) that drives the real runner → projection → cleaning path.

---

## Findings (ordered by materiality)

### F1 — Source-visible reviews that satisfy no targeted-slice predicate are silently dropped (no residual) — **HIGH**

- **Location:** `orca-harness/source_capture/parfumo_projection.py:456` (`_filter_targeted_projection`), `:527` (`_is_latest_or_recent_review`), `:549` (`_is_source_visible_high_rating_review`), `:562` (`_is_source_visible_low_rating_review`).
- **Implementation evidence:** For the targeted surface, each slice keeps only rows matching its own predicate (`:465-516`); a review row is emitted by a slice only if that slice's predicate matches. The predicates do **not** cover the review set:
  - `_is_latest_or_recent_review` (`:527-536`) requires either a `latest/recent/new` token **or** `tab_id ∈ {None, "reviews"}` *and* no `high/top/positive/low/critical/negative` token. A review whose `tab_id` carries a bucket-ish token (e.g. `"high_rating"`) is excluded here.
  - `_is_source_visible_high_rating_review` (`:549-559`): when a numeric `rating` is present it returns `rating >= 8.0` and **ignores the tab entirely**; the tab-token fallback runs only when `rating is None`.
  - So a review with `data-tab="high_rating"` and `rating = 7.5` matches the latest predicate (no — bucket token), the high predicate (no — 7.5 < 8.0), and the low predicate (no) → it appears in **no** slice and is dropped from projection, Cleaning, and Silver.
  - The bucket-absent residuals (`:486,495,504`) fire only when a slice is *entirely* empty; when the high slice is non-empty from some other review, the dropped review produces **no residual at all**.
- **Empirical proof (probe):** A DOM with `loss-1` (`data-tab="high_rating"`, rating 7.5) → `present in projection: False`; projection residuals contained `parfumo_low_rating_review_bucket_absent_or_unexposed` (incidental) but **nothing** signalling that `loss-1` was dropped.
- **Authority/evidence basis:** Contract `parfumo_targeted_capture_contract_v0.md:31` ("explicitly residualize uncaptured review and statement corpus depth") and the Agent Behavior Kernel ("Preserve real failure visibility; never create fake success paths"). Silent loss of a captured, source-visible review with text + rating is invisible data loss.
- **Impact:** Captured review text and ratings disappear from Silver with no audit trail. Reachable broadly: any review whose `tab_id` is not exactly `None`/`"reviews"` and lacks a `latest/recent/new` token, with a rating in the mid band (4 < r < 8), is dropped — i.e. exactly the kind of review a high/low-view capture is built to collect.
- **`minimum_closure_condition`:** Every source-visible review in a targeted packet either lands in ≥1 retained slice, or its omission is recorded as an explicit per-review/coverage residual (failure stays visible). No silent drop path remains.
- **`next_authorized_action`:** Home-model / owner decision on the slice-partitioning model (see F3), then a bounded follow-up patch + a regression test (see F4).
- **Patched in this pass:** No (design-level; see Verdict).

### F2 — The same review's single rating is emitted as multiple Silver MetricObservation (and TextObservation) facts when it satisfies more than one slice predicate — **HIGH**

- **Location:** `orca-harness/runners/run_parfumo_mgt_capture.py:400-414` (slice construction), `orca-harness/source_capture/parfumo_projection.py:745` (slice-scoped `row_id`) + `:456-524`, `orca-harness/cleaning/parfumo.py:165-185` (rating carry per review card), `orca-harness/cleaning/parfumo_lake.py:221-264` (`parfumo_post_cleaned_silver_metric_records`), `:411-419` (`_silver_subject`).
- **Implementation evidence:**
  - The runner builds **5 slices, each carrying *all* preserved file ids** (`_targeted_source_slices`, `preserved_file_ids=list(file_ids)` at `:411`). So every slice re-projects the *same* rendered DOM, and the per-slice predicate filter is the only thing deciding membership.
  - Predicates overlap: a review with `tab_id ∈ {None,"reviews"}` and `rating ≥ 8.0` satisfies **both** `_is_latest_or_recent_review` (clause 2) **and** `_is_source_visible_high_rating_review`. Each match yields a distinct projection row (row_id is slice-scoped: `f"{slice_id}:parfumo:{kind}:{tab_id}:{item_id}"`, `:745`), hence a distinct Cleaning handle, a distinct rating-carry ledger entry (`parfumo.py:165-185`), and a distinct MetricObservation (`parfumo_lake.py:221-264`) — plus a duplicate TextObservation for the body.
  - The two records are **not** dedupable downstream by subject: `_silver_subject` (`:411-419`) keys on the slice-scoped `projection_row_id`, which differs per slice; the stable review identity (`comment_id`/`review_id`) is only embedded inside `row_id`, not exposed as a dedup key. There is no cross-slice/cross-record dedup anywhere in the emit path.
- **Empirical proof (probe):** A DOM with `dup-1` (recent, no `data-tab` → default `tab_id="reviews"`, rating 9.0) projected into **both** `review_latest_recent` and `review_source_visible_high_rating`; rating-carry value counts were `{9.0: 2, 6.0: 1}` — two MetricObservations for one review's single intrinsic rating.
- **Authority/evidence basis:** Parity reference `cleaning/fragrantica_lake.py:476-484` — Fragrantica's metric emission is structurally identical but has **no** multi-slice-over-one-DOM design, so each review yields exactly one handle and one metric per vote field; the duplication is **new to Parfumo's targeted slicing**, not a parity-justified pattern. A MetricObservation is a Silver *fact*; a review's rating is one intrinsic value, so two `observed` records double-count it for any downstream rating aggregation.
- **Impact:** In the most common targeted capture (a "latest reviews" DOM whose cards carry no bucket tab → `tab_id="reviews"`), **every** review rated ≥ 8 or ≤ 4 is double-counted (latest + high/low). Silver facts are durable/high-lock-in, so the over-count propagates.
- **`minimum_closure_condition`:** Each source-visible review rating yields exactly one Silver MetricObservation regardless of how many slices the review appears in (or the per-slice multiplicity is made an explicit, documented, dedup-keyable design choice carrying the stable review identity). Duplicate TextObservations for one review body are likewise resolved.
- **`next_authorized_action`:** Home-model / owner decision on slice semantics + dedup key (see F3), then bounded follow-up patch + regression test (F4).
- **Patched in this pass:** No (design-level; see Verdict).

### F3 — High/low membership uses Orca-invented numeric cutoffs (8.0 / 4.0) that override the source-visible tab; the slice/metric names assert "source_visible" that the threshold does not establish — **MEDIUM** (shared root of F1/F2)

- **Location:** `orca-harness/source_capture/parfumo_projection.py:39-40` (`_PARFUMO_HIGH_RATING_MIN = 8.0`, `_PARFUMO_LOW_RATING_MAX = 4.0`), `:549-572`.
- **Implementation evidence:** When a numeric `rating` is present, high/low membership is decided purely by the hardcoded 8.0/4.0 cutoffs and the source-visible tab is ignored (`:551-553`, `:565-566`). The cutoffs are not derived from any Parfumo-exposed bucket/order/filter field and are not documented in the contract. Slice ids `parfumo_targeted:review_source_visible_high_rating` / `_low_rating` and metric posture `observed` assert source-visibility, but the *bucket boundary* is an Orca editorial choice, not source-visible.
- **Authority/evidence basis:** Contract `:29` — high/low buckets belong "only where Parfumo exposes the underlying rating/order/filter fields." The rating value is source-visible; the 8.0/4.0 partition is not. (Note: this is **not** a contract violation of `:48` "No Fragrantica rating-scale inheritance" — the thresholds are on Parfumo's 0–10 scale, not 1/4/5-star; the no-inheritance rule is respected.)
- **Impact:** This threshold-vs-tab mismatch is the mechanism behind F1 (a "high"-tab review below 8.0 falls through every predicate) and contributes to F2 (a recent review above 8.0 is pulled into two slices). On its own: the carried metric value is the real rating, so no *fact value* is fabricated — the defect is in *selection/coverage* and in the "source_visible" labelling overstating what the cutoff establishes.
- **`minimum_closure_condition`:** Bucket membership is either (a) derived from a source-visible Parfumo order/filter/tab field, or (b) the numeric cutoffs are documented as Orca selection thresholds and the predicate set is made total (no review falls through; see F1) — owner's choice recorded.
- **`next_authorized_action`:** Folded into the F1/F2 partitioning decision.
- **Patched in this pass:** No.

### F4 — Tests pass without exercising the duplication or loss paths; the "without_slice_duplication" test only covers a hand-disjoint fixture — **MEDIUM (review confidence)**

- **Location:** `orca-harness/tests/unit/test_parfumo_projection.py:869` (`test_builds_parfumo_projection_from_targeted_rendered_packet_without_slice_duplication`), `orca-harness/tests/test_parfumo_native_pipeline_lake.py:707-713` (asserts `metric_values == [3.0, 7.0, 9.0]`).
- **Implementation evidence:** Both targeted fixtures (`_TARGETED_HTML`) craft three reviews whose tabs (`latest` / `high_rating` / `low_rating`) and ratings (7.0 / 9.0 / 3.0) make each land in exactly one slice. No test covers (a) a review qualifying for two slices (F2), or (b) a review qualifying for none (F1). The test literally named `..._without_slice_duplication` proves only the disjoint case, giving false confidence on the core targeted-slice contract.
- **Authority/evidence basis:** Commission review axis — "leave tests that pass without proving the target surface, slice filtering, residualization, or MetricObservation front-door behavior."
- **Impact:** The suite is green while the two highest-materiality behaviors are unproven (confirmed: the probe reaches both defects against the same code the green suite covers).
- **`minimum_closure_condition`:** Regression tests assert the resolved F1 behavior (no silent drop / explicit residual) and F2 behavior (one MetricObservation per source-visible review rating), each red against current behavior before the fix.
- **`next_authorized_action`:** Add with the F1/F2 follow-up patch.
- **Patched in this pass:** No.

### F5 — `_field_mentions_any` uses unbounded substring token matching — **LOW (robustness)**

- **Location:** `orca-harness/source_capture/parfumo_projection.py:575-588`.
- **Implementation evidence:** Tokens such as `"low"`, `"new"`, `"top"`, `"high"` are matched as substrings of the joined `tab_id`+`tab_label` text. Real-world labels could collide (`"low"` ⊂ `"flower"`, `"new"` ⊂ `"renew"`, `"top"` ⊂ `"laptop"`). Review-tab labels make this unlikely, but the match is not word-bounded.
- **Impact:** Low; could mis-bucket a review if a tab label happens to contain a token as a substring. Surfaced for completeness.
- **`minimum_closure_condition`:** Token match is word/segment-bounded, or the risk is accepted and noted.
- **`next_authorized_action`:** Optional hardening (non-blocking).
- **Patched in this pass:** No.

---

## What the PR gets right (decision-sufficient context for adjudication)

- **Silver front-door is respected.** Metric records are written through `append_silver_record` (`parfumo_lake.py:103-122`), not the raw writer; no `cleaning_parfumo_silver` bypass. The lane is already declared `SILVER_ENVELOPE` (`lane_registry.py:57`) and `FRONT_DOOR_PENDING` is empty, so **no off-scope lane-registry change is required**.
- **MetricObservation posture coupling is correct.** `kind="observed"` with `metric_value` present and both reason fields null (`parfumo_lake.py:383-393`) satisfies `_validate_metric_posture` (`silver_record.py:114-156`). Absent metrics are **not** zero-filled or emitted as fake observations — absence is recorded as a coverage residual (`parfumo_lake.py:431-438`). This honors the commission's "do not emit MetricObservation records for absent metrics / zero-fill" axis.
- **Body-surface guard works.** `_looks_like_parfumo_body` (`parfumo_projection.py:953-976`) excludes `.json`/`.png`/`.jpg`/`.jpeg`/`.webp` and `http_response_metadata`, and content-gates on `<html`/`data-*`; the probe confirmed `route_receipt.json`, `viewport.png`, and `visible_text.txt` were not parsed (only the DOM's reviews/statement projected). This addresses the "accidentally parse route receipts/screenshots/plans" axis.
- **No Fragrantica rating-scale inheritance.** Unit is `parfumo_rating_0_10`; thresholds operate on the 0–10 scale, not 1/4/5-star (contract `:48` respected).
- **Surface constants are consistent.** Runner `TARGETED_RENDERED_SURFACE` == projection `PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE` == cleaning surface set; the targeted-rendered residual label and raw-pull trigger were added in lockstep across projection and cleaning.
- **Direct-HTTP behavior** is preserved structurally: targeted slice filtering runs only for the targeted surface (`parfumo_projection.py:451-453`); direct-HTTP now also emits a rating MetricObservation when a review card exposes `data-rating` (intentional, tested at `test_parfumo_native_pipeline_lake.py:660-669`). Direct-HTTP has no slice multiplication, so F1/F2 do not apply there. *(Minor adjudication note: confirm emitting metrics on the direct-HTTP/canary surface is intended, since the contract frames metric promotion around the targeted route.)*

## Off-scope flags

- **Root cause partly lives outside the 6-file patch scope.** `run_parfumo_mgt_capture.py` (`_targeted_source_slices`, `:400-414`) assigns *all* files to *every* slice and emits 5 slices over one DOM — a structural contributor to F1/F2. It is **read-only / flag-only** here (not in the bounded set). A complete fix may require either resolving F1/F2 entirely within projection/cleaning (in-scope) or a re-commission that includes the runner. Flagged, not patched.

## Validation evidence

- `python -m pytest -q tests/unit/test_parfumo_projection.py tests/unit/test_parfumo_cleaning_projection_integration.py tests/unit/test_parfumo_non_silver_record_roles.py tests/test_parfumo_native_pipeline_lake.py tests/unit/test_parfumo_mgt_capture_runner.py` → **22 passed** (green baseline confirmed; matches the authoring lane's reported result).
- Read-only probe (temp dir only; no repo file modified) reproduced F1 (`loss-1` dropped, no residual) and F2 (`{9.0: 2, 6.0: 1}` rating-carry counts) against the reviewed code.
- No patch was applied, so no post-patch re-run was required (`git diff --check` would remain clean except for this report). The 6 target files are unmodified by this review.

## Verdict (decision input only — not approval, validation, readiness, or merge authorization)

**Changes requested — `NEEDS_ARCHITECTURE_PASS` for the coupled F1/F2/F3.** The
targeted-slice design emits projection rows (and downstream Silver
TextObservation + MetricObservation facts) per slice membership, with predicates
that neither partition nor cover the review set. The result is, in realistic
captures, simultaneously **silent data loss** (F1) and **duplicate Silver facts**
(F2), both observed empirically and both unproven by the green suite (F4). The
correct fix turns on a design decision the controller should not bake in
unilaterally because it changes durable Silver-fact semantics (high lock-in):
**are the targeted slices overlapping *views* (→ keep overlap but dedup metrics to
one-per-review and guarantee coverage) or partitioning *buckets* (→ assign each
review to exactly one slice)?** Per the Decision-Priority lock-in tiebreaker, this
fork is surfaced to the owner / home model rather than auto-decided. No patch was
applied and no partial patch is left (escalation valve).

The non-slice machinery (front-door, posture coupling, lane registration, body
guard, surface-constant wiring, no-scale-inheritance) is sound.

**Residual risk:** If merged as-is, Parfumo targeted Silver MetricObservations
will under-represent (dropped reviews) and over-represent (double-counted
ratings) the source simultaneously, with no residual marking the loss — a
silently wrong durable Silver layer. The probe shows both are reachable on
ordinary captures, not just crafted edge cases. F5 is independent low-risk
hardening.

## Review-use boundary

These findings are decision input only. They are not approval, validation,
mandatory remediation, readiness, or executor-ready patch authority until
separately accepted or authorized by the commissioning Chief Architect. The
verdict and diff (none here) are claims to adjudicate, not premises to inherit.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: docs/prompts/reviews/parfumo_targeted_projection_metrics_delegated_code_review_prompt_v0.md (PR #532)
- implementation context / reviewed files (pinned 3b6452cb, diff 65105fad..3b6452cb):
  - orca-harness/source_capture/parfumo_projection.py
  - orca-harness/cleaning/parfumo.py
  - orca-harness/cleaning/parfumo_lake.py
  - orca-harness/tests/unit/test_parfumo_projection.py
  - orca-harness/tests/unit/test_parfumo_cleaning_projection_integration.py
  - orca-harness/tests/test_parfumo_native_pipeline_lake.py
- findings + implementation evidence: F1 silent review loss (no residual); F2 duplicate Silver MetricObservation/TextObservation per review across overlapping slices; F3 invented 8.0/4.0 cutoffs override source-visible tab (shared root); F4 tests pass without exercising dup/loss; F5 unbounded substring token match. Each carries file:line evidence above.
- proposed patch / diff: NONE — NEEDS_ARCHITECTURE_PASS on coupled F1/F2/F3 (slice = overlapping views vs partitioning buckets is an owner-level, Silver-fact-lock-in decision). No partial patch left.
- citations: inline above (neutral, file:line).
- reviewer verdict: changes_requested; NEEDS_ARCHITECTURE_PASS. Decision input only.
- validation evidence: 22 passed (green baseline); read-only probe reproduced F1 and F2; no patch applied.
- residual risk: targeted Silver simultaneously under- and over-represents source ratings with no loss residual; reachable on ordinary captures.
- blockers / off-scope: runner run_parfumo_mgt_capture.py (_targeted_source_slices) is a structural contributor but out of the bounded 6-file scope — flag-only; a complete fix may need a re-commission including the runner.
- not-proven boundaries: this review asserts no PASS/readiness/validation of the feature; verdict is advisory decision input.

Adjudicator next step (per .agents/workflow-overlay/communication-style.md -> Review Adjudication Next Step):
adjudicate findings/diff/verdict/residuals as claims first; if a material issue remains
(F1/F2), route the smallest complete closure step (decide slice semantics, then bounded
patch + red-green tests); only after a clean adjudication, batch any admin/lifecycle
follow-ups into one land step and deep-think only the 1-3 material next moves.
```
