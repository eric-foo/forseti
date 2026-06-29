# Fragrance Purchase-Review Coverage Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output / read-only adversarial implementation-code review report
scope: >
  Read-only adversarial implementation/code review of PR #436 (fragrance
  purchase-review focused coverage docs + local no-network coverage
  runner/helper/tests) at target commit bf395583, branch
  codex/fragrance-purchase-review-probes.
use_when:
  - Adjudicating whether PR #436's focused review-coverage implementation is
    coherent with its MGT/contract docs before merge.
  - Checking which review-coverage behaviors are verified, untested, or
    inconsistent with the controlling docs.
authority_boundary: retrieval_only
```

## Review Provenance

```yaml
reviewed_by: claude-opus-4-8   # reviewer self-identified from runtime; operator may correct
authored_by: "Codex / GPT-5 family (commission-stated for bf395583); durable git committer: Eric"
de_correlation_bar: cross_vendor_discovery   # author vendor (OpenAI, per commission) != reviewer vendor (Anthropic)
de_correlation_note: >
  The cross_vendor_discovery bar rests on the commission-stated author vendor
  (Codex/GPT-5). The durable commit author is the human committer "Eric"; the
  model-authorship is asserted by the commission prompt and not independently
  verified by this review. If that author-vendor provenance is not accepted, the
  bar drops to `unrecorded`. Provenance/who-constraint only; not a runtime model
  recommendation, ranking, or routing.
same_vendor_rationale: not_applicable
review_mode: read_only_adversarial_code_review
methods_applied: [workflow-deep-thinking, workflow-code-review]
```

## Commission And Target

- Commission: read-only adversarial implementation/code review of PR #436, routed
  out of a `workflow-delegated-review-patch` request because the target is a
  multi-file implementation/code diff, not a single high-stakes authored artifact
  (per `.agents/workflow-overlay/delegated-review-patch.md` incomplete-commission
  route-out). No patching; findings-first; decision input only.
- Repo: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\fragrance-purchase-review-probes`
- Branch: `codex/fragrance-purchase-review-probes`; HEAD `f0789972` (prompt-add
  commit); review target `bf395583` (ancestor of HEAD; the prompt-on-later-commit
  matches the prompt's dirty-state allowance). Working tree clean.
- PR #436 diff scope (merge-base `190e1ef` -> `bf395583`): 16 files, +2299/-3.
  New code: `fragrance_review_coverage.py`, `run_fragrance_review_coverage.py`,
  `test_fragrance_review_coverage.py`. New docs (all six fragrance contract docs).
  Modified: `__init__.py`, `orca-harness/README.md`,
  `data_capture_spine_consolidation_map_v0.md`, `orca_repo_map_v0.md`, toolbox
  `README.md`, `capture_recon_index_v0.md`, retail_pdp `README.md`.

## Source Context Readiness

`SOURCE_CONTEXT_READY`. All required authority, target, support, and validation
sources were loaded; all 16 SHA256 target pins verified PASS (recomputed against
disk at review time). No `HASH_MISMATCH`. No required source missing.

Source-read ledger (decisive reads):

| Source | Why read | Status |
| --- | --- | --- |
| `orca-harness/source_capture/fragrance_review_coverage.py` | Core adapter under review | clean; pin PASS |
| `orca-harness/runners/run_fragrance_review_coverage.py` | CLI under review | clean; pin PASS |
| `orca-harness/tests/unit/test_fragrance_review_coverage.py` | Test coverage under review | clean; pin PASS |
| `orca-harness/source_capture/__init__.py` | Export surface | clean; pin PASS |
| `fragrance_purchase_review_focused_coverage_mgt_v0.md` | Controlling success-signal / selection policy | clean; pin PASS |
| `fragrance_purchase_review_row_contract_v0.md` | Row field / candidate-key / media / residual contract | clean; pin PASS |
| `fragrance_purchase_review_site_registry_v0.md` | Route/source expectations (incl. JSON route for Twisted Lily) | clean; pin PASS |
| `fragrance_purchase_review_widget_expansion_probe_v0.md` | Widget/route + media diagnosis evidence | clean; pin PASS |
| `retailer_recon` / `row_capture_pilot` / recon index / READMEs / maps | Overclaim + doc-sync checks (Q11/Q12) | clean; pins PASS |
| Overlay: source-of-truth, source-loading, delegated-review-patch, prompt-orchestration, review-lanes, validation-gates, template-registry, README | Lane authority / review boundaries | read in task context |

Independent verification performed (no-network, read-only w.r.t. target):

- Re-ran `tests/unit/test_fragrance_review_coverage.py` -> 4 passed (confirms the
  author's observed "25 passed" includes the 4 fragrance tests; env/imports work).
- Scratch-only probe importing the target module confirmed the F-01 behavior: an
  old, non-recent 5-star / 50-word row is SELECTED via `rating_5_recent_or_40_plus`.

## Deep-Thinking Framing (failure modes, decision criteria)

The lane's stated success signal (MGT `fitness_reference`) is metadata
sufficiency for downstream reading (rating balance, recency, length, media,
verified, native ids, aggregate, selected/skipped reasons, residuals) **while**
keeping skipped review bodies out of the reader set and refusing interpretation
labels. So the decision-relevant failure modes are:

1. **Selection-policy fidelity** — does the focused selector match the MGT policy,
   so the documented success signal (selected/skipped split) is the behavior?
2. **Containment** — are skipped/capped review bodies actually withheld, and is
   the receipt free of interpretation labels and of inferred (vs source-visible)
   facts?
3. **Honesty of diagnostics** — are media, aggregate, key-strength, and total-count
   disagreements surfaced rather than silently resolved?
4. **No fake success / no hidden network** — does the runner fail visibly and stay
   local-file-only?
5. **Verification adequacy** — are the highest-risk paths (the real production JSON
   route, malformed input, 1-star/candidate-key/dedup/aggregate-absence) actually
   covered by tests?
6. **Doc/code coherence** — do the PR's new docs and the modified maps describe the
   committed behavior without overclaiming?

Containment (2) and no-fake-success (4) are the highest-stakes (they map to the
`critical` bar). They hold. The material defects fall in fidelity (1/6) and
verification (5).

## Findings (severity-ordered)

Severity labels are finding-priority only; they are not a formal verdict,
approval, validation, or mandatory-remediation authority. No `patch_queue_entry`
is emitted (read-only review); remediation direction is advisory prose only.

### F-01 — `major` — Committed 5-star selection diverges from the MGT focused policy and its Observed Coverage Receipt; "bounded positives" is unimplemented

- Commissioned target/purpose: PR #436 review; selection-policy fidelity + doc/code sync (Q5, Q12).
- Reviewed target: `fragrance_review_coverage.py` selection logic vs `fragrance_purchase_review_focused_coverage_mgt_v0.md`.
- Location: `orca-harness/source_capture/fragrance_review_coverage.py:641-642`
  (`if row.rating_value == 5 and (recent or row.review_body_word_count >= 40): reasons.append("rating_5_recent_or_40_plus")`);
  MGT `...retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md:100-117`
  (Observed Coverage Receipt: selected 10 / skipped 4, with "one older 40-to-74-word 5-star row" among the skipped)
  and `:140-146` ("Usually skip ... older 5-star rows below the length threshold when the product already has enough positive coverage").
- Implementation evidence: empirically confirmed via a scratch probe importing the
  committed module — an old (2021), non-recent 5-star row with a 50-word body
  (`40_74` bucket) is **SELECTED**, sole reason `rating_5_recent_or_40_plus`. The
  MGT's worked receipt documents exactly such a row (older, 40-74 word, 5-star) as
  **skipped**. There is no "enough positive coverage" bound in the code; every
  5-star row that is recent **or** has >=40 words is selected. The only bound on
  positive volume is the optional `max_selected_rows` global cap (`:594-617`),
  which is `None` by default and not used in the MGT receipt's described run.
- Authority/evidence basis: MGT focused selection policy + Observed Coverage
  Receipt (both introduced by this PR); the prompt's `fitness_reference`
  (success signal); the prompt's own Implementation Summary claim of "bounded
  5-star positives."
- Impact: the PR's headline success-signal artifact (the MGT) documents a
  selected/skipped split the committed adapter does not reproduce on the MGT's own
  described fixture; a downstream reader/agent calibrating to the MGT will
  mis-predict adapter behavior, and the adapter passes more 5-star positive bodies
  into the reader set (more context, more positive skew) than documented. The
  "bounded 5-star positives" capability stated for the PR is effectively absent
  outside the optional cap. This materially misleads downstream consumers (the
  `major` bar) without losing data (skipped rows remain visible in the receipt).
- Uncertainty (named): the real 14-row Luckyscent fixture lives in ignored
  `_test_runs/` (contains review bodies; out of review scope and no-network), so
  the exact 10-vs-11 count on the real fixture is not re-observed here. The
  row-class divergence (40-74w 5-star selected, not skipped) is empirically proven
  on a synthetic fixture and is logically certain from the code. The MGT carries a
  `stale_if` for adapter-policy divergence, but that governs future drift; shipping
  the MGT and a contradicting adapter in the same PR leaves the doc's central
  example born-out-of-sync.
- minimum_closure_condition: the committed selection policy and the MGT
  (policy text + Observed Coverage Receipt) agree on the 5-star rule — either the
  code grows a positive-coverage bound for older mid-length 5-star rows and the
  receipt is regenerated, or the MGT's "Usually skip older 5-star" clause and
  Observed Coverage Receipt are corrected to the committed `recent OR >=40 words`
  rule. The owner decides which surface is canonical.
- next_authorized_action: owner adjudication of canonical surface; reconciliation
  performed in a separately authorized docs-write or implementation lane (not this
  read-only review).

### F-02 — `major` — High-risk code paths are untested (real JSON review route + malformed-input/error-visibility, plus several branches)

- Commissioned target/purpose: PR #436 review; test adequacy on highest-risk paths (Q9, Q10).
- Reviewed target: `tests/unit/test_fragrance_review_coverage.py` vs the adapter/runner surface.
- Location: `orca-harness/tests/unit/test_fragrance_review_coverage.py` (4 tests, all
  driving `{"html": ...}` happy-path responses). Untested code paths:
  `_parse_json_reviews` (`fragrance_review_coverage.py:464-487`, the
  `widget_json_review` route); `FragranceReviewCoverageInputError` on malformed JSON
  (`:391-394`) and the runner's visible-failure exit (`run_fragrance_review_coverage.py:106-110`);
  the 1-star + `has_one_star` branch (`:576`, `:629`, `:639`);
  the `candidate_key_only` path (`:523`); `_dedupe_rows` for actual duplicates (`:558-567`);
  aggregate absence (`pdp_html=None` / no `aggregateRating`, `:419-421`, `:690-714`);
  and the `media_filter_row_scan_mismatch` residual (`:433-434`, which the existing
  fixture actually triggers but no test asserts).
- Implementation evidence: the test fixture (`_widget_response`) emits only HTML
  responses, all rows with `data-review-id`, valid JSON, no 1-star, no duplicates,
  aggregate present. The site registry and widget-expansion probe document that
  **Twisted Lily** returns `{"reviews": [...]}` widget JSON (not HTML) — that route
  is exercised in production but has zero test coverage. The runner's
  fail-visibly-on-malformed-input behavior (a Q9 safety property) is unverified.
- Authority/evidence basis: prompt Q9/Q10; site registry
  (`fragrance_purchase_review_site_registry_v0.md:75`, Twisted Lily widget JSON);
  widget-expansion probe (`:38`).
- Impact: a real production route and a core safety property ship unverified. The
  JSON path looks correct on inspection, but a regression there (or in error
  handling) would not be caught — a high-risk test gap before merge (`major` bar).
- minimum_closure_condition: tests cover (a) the `widget_json_review` route with a
  `{"reviews": [...]}` response, (b) malformed/missing widget input asserting a
  non-zero runner exit / typed `FragranceReviewCoverageInputError`, (c) a 1-star
  fixture exercising `core_rating_1` and the `has_one_star` suppression of
  `recent_low_rating_without_1_star`, (d) a `candidate_key_only` (id-absent) row,
  (e) duplicate dedup by native id, (f) aggregate absence, and (g) the
  `media_filter_row_scan_mismatch` residual.
- next_authorized_action: author tests in a separately authorized lane; no patch from this review.

### F-03 — `minor` — Media diagnostic is one-directional; per-row media absence is asserted, not marked unknown

- Commissioned target/purpose: PR #436 review; honest media diagnosis (Q4).
- Location: `fragrance_review_coverage.py:432-436` (mismatch handled only for
  `source_media_filter_count == 0`); `media_attached_flag: bool = False` default
  (`:102`); row contract Mechanical Filter View
  (`fragrance_purchase_review_row_contract_v0.md:138`: "Absence is `unknown` unless
  the widget says the media-filter row count is zero").
- Implementation evidence: the only media mismatch surfaced is `filter == 0` but a
  row scan finds media (false-positive direction). The opposite direction —
  `source_media_filter_count > 0` (source says media exists) but the row scan finds
  zero (parser miss) — produces no residual. And every row defaults
  `media_attached_flag=False`, so when no source media-filter confirmation is
  supplied, a per-row "no media" fact is asserted rather than left unknown.
- Authority/evidence basis: row contract media rule; widget-expansion probe media
  diagnosis section; prompt Q4.
- Impact: a real-media source whose container markup the parser does not recognize
  would have its media silently dropped (and the `review_media_attached` selection
  reason missed) with no diagnostic, contrary to the contract's "absence is not
  proof of no media." Currently latent (all locked fixtures have media filter 0 and
  0 media), so no live misread today.
- minimum_closure_condition: a residual is emitted when `source_media_filter_count
  > 0` disagrees with a zero row-scan; and per-row media absence is represented as
  unknown (or carries a `media_indicator_absent`-style residual) when no source
  media-filter confirmation exists.
- next_authorized_action: owner/implementer decision; patch in an authorized lane.

### F-04 — `minor` — `candidate_key_basis` not carried; no weaker-key residual for `candidate_key_only` rows

- Commissioned target/purpose: PR #436 review; candidate-key stability + weaker-key visibility (Q7).
- Location: `_candidate_review_key` (`fragrance_review_coverage.py:742-763`, basis
  string computed then discarded — only the sha256 is stored as
  `candidate_review_key`); `_normalize_reviews` (`:552`, residual list omits any
  weaker-key/weak-anchor marker); row contract
  (`fragrance_purchase_review_row_contract_v0.md:73` "Must carry
  `candidate_key_basis`", `:67` "If only ordinal exists, mark `weak_raw_anchor`")
  and MGT drift contract (`...mgt_v0.md:198` "candidate keys can be generated with
  an explicit weaker-key residual").
- Implementation evidence: the row stores only the hash; the basis is recomputable
  from `receipt.product_url` + row fields but no named `candidate_key_basis` field
  exists, and no weaker-key/weak-anchor residual is emitted when
  `review_key_status == "candidate_key_only"`. The `review_key_status` enum gives
  partial visibility only.
- Authority/evidence basis: row contract candidate-key + raw-row-anchor rules; MGT
  drift contract; prompt Q7.
- Impact: a contract requirement is unmet and weaker-key usage is not visible in
  residuals. Latent today (all locked fixtures carry native Judge.me/Yotpo ids);
  triggers for id-less rows (e.g., a JSON review lacking `id`/`review_id`).
- minimum_closure_condition: the row carries `candidate_key_basis` (or its explicit
  component list) and emits a weaker-key/weak-anchor residual for
  `candidate_key_only` rows.
- next_authorized_action: implementer in an authorized lane.

### F-05 — `minor` — Skipped/capped rows retain verbatim review title text

- Commissioned target/purpose: PR #436 review; "skipped bodies out of the reader set" (Q1/Q6).
- Location: `_apply_selection_policy` (`fragrance_review_coverage.py:587`, `:608`):
  `review_body_verbatim` is set to `None` for non-selected/capped rows, but
  `review_title_verbatim` is not stripped.
- Implementation evidence: a skipped row keeps `review_title_verbatim` — verbatim
  reviewer-authored free text — while its body is stripped.
- Authority/evidence basis: `fitness_reference` observable success signal ("keeping
  skipped bodies out of the reader set"); MGT body-stripping intent. The row/MGT
  contracts class titles as preserved metadata, so this is a judgment call, not a
  clear contract breach.
- Impact: the often-most-salient line of a skipped review (its title) remains in the
  reader set, partially defeating the "skipped bodies out" goal if titles are
  treated as body-equivalent free text. Context cost is small (titles are short).
- minimum_closure_condition: owner decides whether review titles count as
  body-equivalent free text; if so, strip `review_title_verbatim` from
  skipped/capped rows (retaining a title hash/word-count if needed for readback).
- next_authorized_action: owner decision.

### F-06 — `minor` — Aggregate honesty gaps: aggregate-vs-widget count mismatch not surfaced; partial JSON-LD parse-error residual dropped on success

- Commissioned target/purpose: PR #436 review; honest aggregate semantics (Q8).
- Location: `build_fragrance_review_coverage` (`fragrance_review_coverage.py:419-436`,
  flags `widget_total_count != len(rows)` but never compares
  `aggregate_companion.review_count` against `widget_total_count`/row count);
  `_aggregate_from_pdp_html` (`:690-714`, the success return at `:705-712` hardcodes
  `residuals=[]`, discarding any `json_ld_parse_error` accumulated from earlier
  scripts; first `aggregateRating` in walk order wins with no `@type` filtering).
- Implementation evidence: PDP aggregate review_count and widget `total_count` can
  disagree with no residual; a malformed earlier `<script type="application/ld+json">`
  block's `json_ld_parse_error` is dropped when a later block yields an aggregate.
- Authority/evidence basis: MGT drift/fallback contract
  (`...mgt_v0.md:210`, `:224`: aggregate "conflicts with widget totals" is an
  upgrade trigger); prompt Q8.
- Impact: an aggregate-vs-widget disagreement (a documented drift trigger) is not
  surfaced, and a partial JSON-LD parse failure can be silently dropped. Bounded;
  the fixtures have agreeing counts and single clean JSON-LD blocks.
- minimum_closure_condition: emit a residual when `aggregate_companion.review_count`
  disagrees with `widget_total_count` (and/or row count); preserve accumulated
  `json_ld_parse_error` residuals on the success return path.
- next_authorized_action: implementer in an authorized lane.

### F-07 — `minor` — Over-broad forbidden-field substring matching can hard-fail on legitimate fragrance fields

- Commissioned target/purpose: PR #436 review; interpretation-field rejection correctness (Q2).
- Location: `_is_forbidden_field_name` (`fragrance_review_coverage.py:853-859`), the
  `token in normalized` substring clause; `_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES`
  includes `strength`, `discount`, `demand`, `weak`, `strong` (`:25-49`).
- Implementation evidence: the substring clause means a future `source_visible_fields`
  key such as `scent_strength` (a plausible source-visible fragrance attribute)
  matches `strength` -> the row validator raises -> the whole coverage build
  crashes (CLI exit 2). No current trigger: the six hardcoded keys
  (`source_widget`, `data_review_id`, `data_verified_buyer`, `data_product_title`,
  `data_product_url`, `data_badge_type`) contain no forbidden substring. There are
  also minor false negatives (concatenated forms like `buyerproof` evade the
  underscore-bearing token).
- Authority/evidence basis: row contract / MGT forbid interpretation labels
  (pain/pleasure/sentiment/integrity/etc.), not mechanical attributes; prompt Q2.
- Impact: latent fragility in the lane's own domain — the denylist conflates
  interpretation labels (its actual target) with mechanical substrings, so
  legitimate future source fields can hard-fail the build. Today the rejection
  works correctly for the contractually-named interpretation fields (the
  `integrity_label` test passes).
- minimum_closure_condition: match on exact token / word boundary (the existing
  `token == normalized` and `token in parts` clauses already do this) rather than
  raw substring; align the denylist with the contractually-forbidden interpretation
  set.
- next_authorized_action: implementer in an authorized lane.

### F-08 — `advisory` — Non-deterministic default `as_of_date`

- Location: `build_fragrance_review_coverage` (`fragrance_review_coverage.py:416`,
  `as_of_date or date.today()`); CLI `--as-of-date` is optional
  (`run_fragrance_review_coverage.py:68`).
- Evidence/impact: without `--as-of-date`, recency-derived selection
  (`recent_12m`, `rating_5_recent_or_40_plus`, control rules) varies by run date,
  so receipts are not reproducible across days. Tests pin `as_of_date`.
- Advisory direction: document (or require) `--as-of-date` for durable/comparable
  receipts.

### F-09 — `advisory` — Dead `_MutableReview.ordinal` / `start_ordinal`

- Location: `_MutableReview.ordinal` (`:177`), `_parse_json_reviews(start_ordinal=...)`
  (`:464`, called with `start_ordinal=len(raw_reviews)+1` at `:402`); `_normalize_reviews`
  re-enumerates ordinals from 1 (`:497`) and ignores the carried value.
- Evidence/impact: carried ordinal state is computed but never used for the final
  `row_ordinal` or candidate key — dead/misleading state. Maintainability only.
- Advisory direction: drop the unused ordinal carriage or make `_normalize_reviews`
  consume it.

### F-10 — `advisory` — CLI source defaults to Luckyscent; output-path discipline is documentation-only

- Location: `run_fragrance_review_coverage.py:59-60` (`--source-id` default
  `fragrance_retail_luckyscent`, `--source-site` default `Luckyscent / Scent Bar`);
  `--output` is required with no default (`:57`).
- Evidence/impact: running the runner against another registry source without
  `--source-id`/`--source-site` mislabels rows as Luckyscent. Separately, the runner
  writes selected-row verbatim bodies to whatever `--output` path is given; keeping
  outputs in ignored/local paths is enforced only by docs + `.gitignore` + operator
  discipline, not by the tool. (The required `--output`, the `_test_runs` example in
  the harness README, and the explicit non-claims make this acceptable, not a
  containment defect.)
- Advisory direction: consider requiring `--source-id` (or warning on default for a
  non-Luckyscent product URL); optionally nudge `--output` toward an ignored default.

## Non-Findings / Verified Strengths

These were checked adversarially and hold; they are noted so the owner can see the
lane's core safety properties are intact (no `critical` finding was found).

- **No-network / fail-visible (Q9):** the module and runner import no network
  libraries (only stdlib + pydantic + local `schemas`); malformed widget JSON
  raises `FragranceReviewCoverageInputError` -> the runner exits 2 with a message
  (`run_fragrance_review_coverage.py:106-110`); the success `print`/`return 0` is
  unreachable on error. No hidden success path found.
- **Body containment (Q6):** skipped and adaptive-cap-excluded rows have
  `review_body_verbatim` set to `None` while `review_body_sha256`,
  `review_body_word_count`, and `review_length_bucket` are retained (verified by
  `test_focused_review_coverage_extracts_source_visible_receipt` and
  `test_adaptive_cap_preserves_skipped_receipt`). (Title caveat: F-05.)
- **Interpretation-label refusal (Q2):** `source_visible_fields` keys are validated
  against the forbidden set; receipt `certification`
  (`source_visible_focused_coverage; not_cleaned; not_judgment_ready`) and
  `non_claims` are explicit; selection/skip reason vocabulary is mechanical
  (rating/length/recency/media), with no sentiment/quality/integrity values.
  (Over-breadth caveat: F-07.)
- **Verified flag honesty:** `verified_purchase_flag` is `None` (not `False`) when
  the source label is absent (`_bool_or_none`), so absence is not inferred as
  unverified — matching the row contract.
- **Media false-positive avoidance (Q3):** avatar/generic images are excluded from
  `media_attached_flag` (only `img/picture/source/video` inside a
  `jdgm-rev__pic(s)`/`jdgm-rev__vid(s)`/`jdgm-rev__video` container count);
  `test_..._receipt` confirms an `jdgm-rev__avatar` image yields
  `media_attached_flag is False` and a real picture container yields `True`. The
  parser handles void/self-closing tags, nested bodies, and native id / rating /
  timestamp / verified / helpful-count / badge data-attributes. (Direction caveat: F-03.)
- **Doc accuracy / non-overclaim (Q11):** the modified `orca-harness/README.md`
  ("Fragrance Review Coverage Runner"), `data_capture_spine_consolidation_map_v0.md`,
  and `orca_repo_map_v0.md` describe the runner accurately (saved widget/PDP files
  only; selected reader bodies + skipped metadata/hashes) and carry correct
  non-claims (no live capture, ECR, Cleaning, Judgment, integrity scoring). The MGT
  inconsistency is the exception (F-01).
- **Validation evidence:** re-ran the fragrance unit tests -> 4 passed, consistent
  with the author's observed "25 passed" for the two named test files.

## Review-Question Coverage Map

| Prompt question | Disposition |
| --- | --- |
| 1 MGT signals preserved, no scraping/interpretation drift | Metadata capture preserved; selection split diverges from MGT (F-01); skipped titles retained (F-05). |
| 2 receipt fields imply interpretation | No value-level leakage (strength); denylist over-broad (F-07). |
| 3 Judge.me HTML parsing robustness incl. media not from avatars | Solid (strength); media-miss direction unflagged (F-03). |
| 4 media diagnosis honest on disagreement | One-directional only (F-03). |
| 5 selection policy matches focused MGT contract | Diverges on 5-star / bounded positives (F-01). |
| 6 body stripping prevents blowup, keeps hashability | Bodies stripped + hash kept (strength); titles retained (F-05). |
| 7 candidate keys stable; weaker-key residuals visible | `candidate_key_basis` + weaker-key residual missing (F-04). |
| 8 aggregate semantics honest when split/mismatched | Mismatch not surfaced; parse-error residual dropped (F-06). |
| 9 runner no-network, fails visibly, no hidden success | Holds (strength); error path untested (F-02). |
| 10 tests strong on highest-risk paths | Major gaps incl. untested JSON route (F-02). |
| 11 docs accurate, no overclaim | Accurate except MGT (F-01). |
| 12 branch doc stale/contradictory vs code | MGT Observed Coverage Receipt out of sync (F-01). |

## Not-Proven Boundaries / Strict-Only Blockers

- This is zero-config-style adversarial review elevated only by the prompt's
  commission bindings (target, output path, severity-for-priority). It is **not** a
  formal lane verdict, validation pass/fail, approval, readiness, or fixture
  admission. The severity labels carry priority weight only.
- The real Luckyscent 14-row fixture (ignored `_test_runs/`, contains bodies) was
  not executed; F-01's exact selected-count effect on that specific fixture is
  reasoned + synthetically confirmed, not re-observed on the real data.
- No claim is made about runtime/production behavior beyond the offline paths
  exercised; ECR/Cleaning/Judgment/buyer-proof remain out of scope and unbuilt.

## Review-Use Boundary

Findings are decision input only. This review does not approve, validate, mandate
remediation, authorize patches, authorize commits, authorize source capture,
authorize commercial/runtime use, or create ECR, Cleaning, Judgment, buyer-proof,
fixture-admission, or readiness evidence. Remediation and severity adjudication
remain with the owner.

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/fragrance_purchase_review_coverage_adversarial_code_review_v0.md
  review_mode: read_only_adversarial_code_review
  recommendation: revise_before_merge
  findings_count:
    critical: 0
    major: 2
    minor: 5
    advisory: 3
  blocking_or_major_findings:
    - "F-01: committed 5-star selection (recent OR >=40 words) diverges from the MGT focused policy + Observed Coverage Receipt; bounded-positives unimplemented (empirically confirmed)."
    - "F-02: high-risk paths untested — the real widget_json_review route (Twisted Lily) and malformed-input/error-visibility, plus 1-star/candidate-key/dedup/aggregate-absence/media-mismatch branches."
  strict_only_blockers_or_not_proven_boundaries:
    - "Not a formal lane verdict/validation/approval/readiness/fixture-admission; severity labels are priority-only."
    - "Real ignored Luckyscent 14-row fixture not executed; F-01 count effect reasoned + synthetically confirmed, not re-observed on real data."
    - "de_correlation_bar cross_vendor_discovery rests on commission-stated author vendor (Codex/GPT-5); git committer is human (Eric)."
  next_action: "Owner adjudicates F-01 canonical surface (code vs MGT) and authorizes a separate lane to reconcile the doc/policy and add the F-02 tests; minor/advisory items batched into the same pass."
```
