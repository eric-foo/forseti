# Instagram Reels Grid Parser — Advisory Code Review (v0)

```yaml
retrieval_header_version: 1
artifact_role: Advisory code review output (findings-only, read-only)
scope: >
  Read-only adversarial code review of the IG public /reels/ grid parser slice:
  orca-harness/source_capture/ig_reels_grid.py and tests/unit/test_ig_reels_grid.py.
  DOM row normalization, passive JSON media-candidate extraction, shortcode-keyed
  source-surface-preserving joins.
commissioned_by: docs/prompts/reviews/instagram_reels_grid_parser_adversarial_code_review_prompt_v0.md
source_loading_mode: zero-config findings-only advisory review (workflow-code-review)
authority_boundary: retrieval_only
controlling_source_state: mixed_dirty_worktree; strict readiness / formal pass NOT authorized
result_class: ADVISORY_FINDINGS_ONLY  # not a formal verdict, approval, or readiness claim
```

## Provenance

```yaml
reviewed_by: unrecorded
authored_by: unrecorded
de_correlation_bar: operator_to_fill_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Model identity is not fabricated. No runtime model is recommended, ranked, or implied.

## Method Declaration

- REFERENCE-LOADED `workflow-deep-thinking` and `workflow-code-review` before applying them.
- SOURCE-LOADED the target slice and all context-only files named in preflight.
- Declared `SOURCE_CONTEXT_READY` (see ledger) before applying review.
- Applied `workflow-deep-thinking` to frame failure modes, then `workflow-code-review` (zero-config
  findings-only advisory mode) for findings-first review.
- This is a **read-only** review. No patch, patch queue, formal verdict, severity authority, readiness,
  or runtime-model recommendation is claimed. `patch_queue_entry` is `no` for every finding.

`SOURCE_CONTEXT_READY` — all named target and context-only files were readable in this worktree; no
material source gap blocks the review. The dirty/untracked state of the parser slice is expected and
acknowledged; strict pass/readiness claims are withheld accordingly.

## Source-Read Ledger

| File | Role | Read |
|---|---|---|
| `orca-harness/source_capture/ig_reels_grid.py` | review target (impl) | full (1-409) |
| `orca-harness/tests/unit/test_ig_reels_grid.py` | review target (tests) | full (1-154) |
| `.../instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md` | context: capture-path spec / evidence basis | full |
| `docs/prompts/architecture/instagram_reels_profile_metadata_capture_architecture_prompt_v0.md` | context: architecture intent | full |
| `orca-harness/source_capture/ig_momentum_harvest.py` | context: sibling parser conventions | full |
| `orca-harness/tests/unit/test_ig_momentum_harvest.py` | context: sibling test conventions | full |
| `orca-harness/tests/unit/test_source_capture_ig_calls_packet.py` | context: downstream runner surface | full |

Evidence labels: "spec" = `ig_profile_grid_dom_engagement_recon_and_spec_v0.md`; "arch" =
architecture prompt; "impl" = `ig_reels_grid.py`; "repro" = reproduced live in this worktree's
interpreter (Windows / CPython) during review.

## Validation Run Status

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\orca-harness
python -m pytest -q tests/unit/test_ig_reels_grid.py tests/unit/test_ig_momentum_harvest.py tests/unit/test_source_capture_ig_calls_packet.py
```

Observed this turn: **23 passed** (consistent with the dispatcher's `23 passed`). Treated as evidence
inspected, not a formal validation claim. In addition, four ad-hoc probes were run against the live
module to reproduce F-01, F-02, and F-03 (results inline below). The probes were throwaway and wrote
nothing to the repo.

A green suite here is **not** counter-evidence to the findings: the failing behaviors below are simply
not exercised by the four existing reels-grid tests (see F-08).

---

## Findings (ordered by materiality)

### F-01 — Ambiguity is never emitted; positional likes/comments are silently trusted (HIGH)

- **Commissioned target / purpose:** parser must not silently corrupt grid engagement metadata before
  runner wiring.
- **Reviewed target / role:** `ig_reels_grid.py` DOM normalization (impl).
- **Location:** `AMBIGUOUS_HIDDEN_NUMERIC` constant defined at `ig_reels_grid.py:26`; never referenced
  again. `_dom_parse_status` at `ig_reels_grid.py:336-343`. Value-based subtraction
  `_subtract_visible_numbers` at `:323-333`. Positional assignment at `:134-137`.
- **Implementation evidence:** `_dom_parse_status` returns only `PARSED_NO_HOVER_GRID_ENGAGEMENT`,
  `VIEWS_ONLY_NO_HIDDEN_ENGAGEMENT`, `HIDDEN_ENGAGEMENT_ONLY_NO_VISIBLE_VIEWS`, or
  `ROUTE_NOT_VERIFIED`. There is no branch that ever returns `AMBIGUOUS_HIDDEN_NUMERIC`. `likes_text`
  and `comments_text` are taken positionally as `hidden_candidates[0]`/`[1]` whenever ≥2 hidden
  candidates exist. `_subtract_visible_numbers` removes visible values **by value**, so when a
  like/comment value equals the views value, the wrong leaf is consumed.
  - **repro:** `visibleNumericTexts=['30']`, `leafNumericTexts=[30,4,30]` (true likes=30, comments=4)
    →  `likes_text='4'`, `comments_text='30'`, `parse_status='parsed_no_hover_grid_engagement'`. Both
    engagement fields are wrong and the row is reported as a *confident* clean parse.
- **Authority / evidence basis:** spec §"Current Finding": "Code must still preserve the raw leaf list
  **and mark ambiguous rows instead of silently trusting the order** when the shape changes." Spec
  §"Parse Statuses" lists `ambiguous_hidden_numeric` as required. Spec §"Code-Enforceable Capture
  Rules": "Parse likes/comments only when the clean observed shape is present; otherwise emit
  `ambiguous_hidden_numeric` or another partial status."
- **Impact (correctness):** The central safety invariant of the slice is unimplemented. Rows with a
  views/likes/comments value collision, an unexpected hidden-leaf count (e.g. 3+ candidates), or any
  shape change are emitted as `parsed_no_hover_grid_engagement` with positionally-assigned — and
  potentially swapped — likes/comments. This is exactly the "silent corruption" the commission exists
  to prevent.
- **minimum_closure_condition:** `_dom_parse_status` (or the assignment path) emits
  `AMBIGUOUS_HIDDEN_NUMERIC` when the clean shape is not unambiguously present (e.g. value collision
  between views and a hidden candidate, hidden-candidate count outside the expected 2, or
  subtraction that did not remove exactly the visible views), and likes/comments are withheld (left
  null) on ambiguous rows; a test pins each case.
- **next_authorized_action:** Read-only advisory only. Route to a separately-authorized patch lane /
  home-model adjudication. No edit performed.
- **verification expectation:** Same-check red-green: a new test asserting `AMBIGUOUS_HIDDEN_NUMERIC`
  on the collision/3-leaf fixtures fails against current code and passes after the fix. Not run (read-only).
- **patch_queue_entry:** no.

### F-02 — `device_timestamp` fallback + unguarded `fromtimestamp` → wrong dates and a crash that drops the whole payload (HIGH)

- **Reviewed target / role:** JSON candidate extraction (impl).
- **Location:** `_candidate_from_node` timestamp resolution at `ig_reels_grid.py:208`
  (`_first_int(node, ("taken_at_timestamp", "taken_at", "device_timestamp"))`); `_timestamp_to_utc`
  at `:385-388` (no range guard); call site has no try/except in `iter_json_media_candidates` `:162-168`.
- **Implementation evidence:** `device_timestamp` is accepted as a publish-time fallback. IG
  `device_timestamp` is a client-upload value, commonly in **epoch microseconds**, and is not publish
  time. `_timestamp_to_utc` calls `datetime.fromtimestamp(value, timezone.utc)` with no bounds check.
  - **repro:** a node `{'code':'ABC','device_timestamp':1782112975123456}` (no `taken_at*`) →
    `iter_json_media_candidates(...)` raises `OSError [Errno 22] Invalid argument` on this platform.
    Because the loop has no guard, the exception aborts the **entire** call and every candidate from
    that payload is lost.
- **Authority / evidence basis:** Review-axis explicitly: "over-trusting `device_timestamp` as publish
  time." Spec sanctions only `taken_at_timestamp` (timeline media) and `taken_at` (clips); neither spec
  nor architecture endorses `device_timestamp`. Kernel: "Preserve real failure visibility" — a single
  malformed node should degrade to a limitation, not silently crash the join.
- **Impact (correctness + runtime/availability):** (a) When only `device_timestamp` is present, the
  derived `taken_at_utc` is either wrong (micro/seconds confusion) or the call crashes; (b) one bad
  node takes down all candidates for the payload, which downstream reads as "no JSON metadata"
  rather than a visible per-node limitation.
- **minimum_closure_condition:** `device_timestamp` is dropped from the publish-time precedence (or
  parsed with an explicit unit normalization and labeled non-publish), **and** `_timestamp_to_utc`
  guards out-of-range epochs (returns null + a limitation rather than raising); a fixture pins both the
  micro-seconds value and an out-of-range value.
- **next_authorized_action:** Read-only advisory; route to authorized patch lane.
- **verification expectation:** Same-check red-green: a test feeding a microsecond `device_timestamp`
  fails (raises) against current code and passes (null/limitation) after the fix. Not run (read-only).
- **patch_queue_entry:** no.

### F-03 — Recursive discovery double-yields nested `code`/`shortcode` nodes and coerces integer `code` (MED-HIGH)

- **Reviewed target / role:** `_iter_media_nodes` / `_node_shortcode` (impl).
- **Location:** `_iter_media_nodes` at `ig_reels_grid.py:192-201`; `_node_shortcode` at `:234-235`;
  int→str coercion in `_string_or_none` at `:391-397`.
- **Implementation evidence:** `_iter_media_nodes` yields a node when it has a shortcode **and then
  still recurses into that node's values**, so any nested object carrying its own `code`/`shortcode`
  is yielded as a second candidate. `_node_shortcode` falls back to `code`, and `_string_or_none`
  coerces ints to strings, so a non-media `{"code": <int>}` becomes a candidate.
  - **repro 1 (nesting):** `{'items':[{'media':{'code':'PARENT','like_count':5,'nested':{'code':'CHILD','like_count':99}}}]}`
    → two candidates `[('PARENT',5),('CHILD',99)]`. A nested object's counts surface as if they were a
    distinct reel; if `CHILD` collides with a real DOM shortcode it attaches wrong-layer counts.
  - **repro 2 (int code):** `{'error':{'code':400,'message':'x'}}` → a candidate with
    `shortcode='400'`.
  - Duplicates/junk are retained: `candidates_by_shortcode` (`:171-175`) groups but does not dedup, and
    the join (`:178-189`) keeps every grouped candidate.
- **Authority / evidence basis:** Review-axis: "recursive JSON candidate discovery can misclassify
  non-media nodes with `shortcode` or `code`, duplicate nested media, or attach counts/captions from
  the wrong payload layer." Real IG payloads nest code-bearing nodes (carousel children, reshares /
  collab / cross-post media), and `web_profile_info` timelines include non-reel media types.
- **Impact (correctness / review-confidence):** spurious and duplicate candidates pollute
  `iter_json_media_candidates` output and the by-shortcode index. Most junk (`'400'`) is dropped at the
  DOM join because DOM shortcodes are alphanumeric, but nested **real** shortcodes can join to the
  wrong row, and duplicate same-shortcode candidates inflate the conflict set the runner must later
  reconcile.
- **minimum_closure_condition:** discovery stops descending into a matched media node's known
  child-media containers (or dedups by a stable node identity), and `code` is accepted only as a
  string (no int coercion for the shortcode key); fixtures pin a carousel/nested payload and an int
  `code` payload.
- **next_authorized_action:** Read-only advisory; route to authorized patch lane.
- **verification expectation:** Same-check red-green on a nesting fixture and an int-`code` fixture.
  Not run (read-only).
- **patch_queue_entry:** no.

### F-04 — Intra-node count precedence collapses multiple count keys and drops which key won (MED)

- **Reviewed target / role:** count extraction in `_candidate_from_node` (impl).
- **Location:** `ig_reels_grid.py:221`
  (`_first_count(node, ("video_view_count", "play_count", "view_count", "ig_play_count"))`); `_first_count`
  at `:346-354`.
- **Implementation evidence:** when a single node carries several of these keys with **different**
  values (common in real IG clip media: `play_count`/`ig_play_count`/`view_count` can differ),
  precedence silently returns the first present key and records `video_or_play_count` only — the
  selected key is not preserved. The spec's validated DOM-matching field for `/clips/user` was
  `ig_play_count` (spec evidence: `DZ4Stb5MVPB` → `ig_play_count` 2984 == DOM 2984), which is **last**
  in precedence; if `play_count` or `view_count` is also present and differs, the chosen value may not
  be the DOM-matching one.
- **Authority / evidence basis:** spec §"Code-Enforceable Capture Rules": "Record `source_surface` for
  every numeric/count candidate. Do not collapse DOM views, `/clips/user` play/view counts, and
  `web_profile_info` video/play counts into one unqualified value." arch Q6 (clips vs web_profile_info
  count semantics). Source-surface is preserved at candidate level, but the **intra-node** key identity
  is not.
- **Impact (review-confidence / correctness):** the captured count is deliberately ambiguous-named
  (`video_or_play_count`) and provenance to the *surface* is kept, so this is not a false-canonical-count
  bug at the surface level. But which raw key produced it is unrecoverable, weakening the later
  selection/reconciliation policy the spec defers, and the precedence can disagree with the spec's
  DOM-validated `ig_play_count` semantics.
- **minimum_closure_condition:** record the selected count key alongside the value (or preserve all
  present count candidates per node), and reconcile precedence with the spec's DOM-matching evidence;
  a test pins a multi-count-key node.
- **next_authorized_action:** Read-only advisory; route to authorized patch lane or confirm "selected
  key need not be preserved" as an explicit owner decision.
- **verification expectation:** test asserting recorded key / all-candidates on a multi-key node. Not
  run (read-only).
- **patch_queue_entry:** no.

### F-05 — DOM-row dedup is path-exact, not shortcode-keyed (MED)

- **Reviewed target / role:** `normalize_dom_grid_rows` dedup (impl).
- **Location:** `ig_reels_grid.py:118` (`seen: set[str]`), `:120` (path source), `:125-127`
  (`if path in seen: continue`).
- **Implementation evidence:** dedup keys on the exact `path` string. The same reel rendered as both a
  relative `path` and an absolute `href`, or with/without a trailing slash, or with a query string on
  one occurrence, yields different strings → duplicate rows for one shortcode (IG commonly renders the
  same permalink twice per cell). Note also `raw.get("path")` is used verbatim while `href` is run
  through `urlparse` (`_path_from_href` `:285-291`), so a `path` carrying a query is not normalized,
  widening the variance.
- **Authority / evidence basis:** spec §"Code-Enforceable Capture Rules": "Use shortcode or permalink
  path as identity; never use grid index as identity." A path-exact key admits multiple identities for
  one shortcode.
- **Impact (correctness):** duplicate joined rows for one reel; the join attaches the same candidate
  tuple to each, double-counting reels downstream.
- **minimum_closure_condition:** dedup prefers `shortcode` when present (fall back to a
  `urlparse`-normalized path); a test pins absolute-vs-relative and trailing-slash variants of one reel
  collapsing to a single row.
- **next_authorized_action:** Read-only advisory; route to authorized patch lane.
- **verification expectation:** same-check red-green on a duplicate-variant fixture. Not run (read-only).
- **patch_queue_entry:** no.

### F-06 — Handle filter cannot exclude bare cross-profile permalinks (LOW-MED)

- **Reviewed target / role:** `_path_matches_handle` (impl).
- **Location:** `ig_reels_grid.py:294-300`.
- **Implementation evidence:** any path whose first segment is `p` or `reel` (the common IG bare
  permalink shape `/reel/X/`) returns `True` regardless of `profile_handle`. The handle filter only
  rejects handle-*prefixed* paths for other handles (`/{otherhandle}/reel/X/`). Injected "suggested" /
  "related" reels rendered as bare `/reel/X/` from other creators pass the filter.
- **Authority / evidence basis:** review-axis: "wrong-profile rows." Accurate limitation: bare
  permalinks carry no handle, so value-based handle filtering structurally cannot exclude them.
- **Impact (review-confidence):** cross-profile rows can leak into the grid result when IG injects
  bare permalinks; the parser cannot self-detect this from path alone.
- **minimum_closure_condition:** document the limitation in the row/limitations output, or cross-check
  emitted shortcodes against the page-owner JSON when available; a test pins that an injected
  other-creator bare `/reel/` either is excluded or is marked as unverified-owner.
- **next_authorized_action:** Read-only advisory; owner decision on whether ownership verification is
  in-scope for this slice.
- **verification expectation:** test on a mixed-owner row set. Not run (read-only).
- **patch_queue_entry:** no.

### F-07 — Ad-term regex matches bare words anywhere in caption (LOW)

- **Reviewed target / role:** `_AD_TERM_RE` ad-term candidate extraction (impl).
- **Location:** `ig_reels_grid.py:30`; applied at `:210`.
- **Implementation evidence:** the alternation `partner(?:ship)?|gifted|affiliate` has no `#` anchor and
  no boundary intent beyond the word itself, so benign caption words ("my partner", "a gifted child")
  produce ad-term candidates. (`#ad\b` / `#sponsored\b` are appropriately anchored.)
- **Authority / evidence basis:** review-axis: "ad-term parsing preserve evidence without overclaiming
  that a reel is or is not an ad." Spec: treat ad-related fields as candidate signals only.
- **Impact (review-confidence):** over-inclusive `ad_term_candidates`. **Mitigated** because the field
  is explicitly a candidate list, the parser asserts no `is_ad`, and the spec defers ad classification —
  so this is over-collection of *evidence*, not an ad overclaim.
- **minimum_closure_condition:** tighten the bare-word terms (e.g. require `#` or a sponsorship phrase)
  or document that bare-word matches are intentional broad candidates; a test pins a benign-"partner"
  caption.
- **next_authorized_action:** Read-only advisory; owner decision on candidate breadth.
- **verification expectation:** test on benign-word captions. Not run (read-only).
- **patch_queue_entry:** no.

### F-08 — Tests do not exercise the spec's hardest invariants (review-confidence; LOW-MED)

- **Reviewed target / role:** `test_ig_reels_grid.py`.
- **Location:** whole file (4 tests + 1 surface-label test).
- **Implementation evidence:** tests cover the clean no-hover happy path, the clips/web_profile_info
  shapes, one conflicting join, and surface labels. There is **no** test for: ambiguity/value-collision
  (F-01), `device_timestamp`/timestamp overflow (F-02), nested/duplicate or int-`code` candidates
  (F-03), multi-count-key precedence (F-04), duplicate path variants (F-05), or cross-profile leak
  (F-06). The join test asserts conflict preservation only for two cleanly-distinct candidates.
- **Authority / evidence basis:** review-axis: "whether tests cover the real intended invariants,
  including no-hover parsing, source conflict preservation, timestamp conversion, and known IG
  source-surface labels." The spec's load-bearing rule ("mark ambiguous rows") is untested precisely
  because it is unimplemented (F-01).
- **Impact (review-confidence):** the green suite (23 passed) does not constrain the failure modes
  above; it cannot be read as evidence that engagement metadata is not silently corrupted.
- **minimum_closure_condition:** each of F-01..F-05 lands with a same-check red-green test as part of
  its closure.
- **next_authorized_action:** Read-only advisory; tests added under the authorized patch lane.
- **verification expectation:** as per F-01..F-05. Not run (read-only).
- **patch_queue_entry:** no.

---

## Nits (LOW; grouped, non-blocking)

- **N-1:** When `hidden_leaf_numeric_texts` is supplied explicitly, `_leaf_numeric_texts` (`:303-306`)
  returns it via `_text_tuple` **without** the `_NUMERIC_RE` filter applied to the `leafNumericTexts`
  branch (`:308-319`). Inconsistent cleaning between the two input shapes; non-numeric junk in the
  explicit list flows into hidden candidates.
- **N-2:** `UNKNOWN_SOURCE_SURFACE` (`:21`) and `ITEM_PAGE_METADATA` (`:20`) are defined but never
  returned; `source_surface_from_url_or_path` (`:90-98`) collapses every unmatched path to
  `passive_page_json_metadata`, so a genuinely unknown surface is mislabeled "passive page JSON"
  rather than `unknown`. Low impact (label only, caller-supplied), but it removes the `unknown`
  distinction the spec defines.
- **N-3:** `raw_node_keys_sample` (`:230`) is `sorted(...)[:80]` — the alphabetically-first 80 keys,
  not a representative "sample"; cosmetic naming only.

## Positive Affirmations (axes checked, no finding)

- **Zero-value preservation:** `_first_count`/`_int_or_none` (`:346-382`) gate on `is not None`, so a
  genuine `0` like/comment/view count is preserved (e.g. `comment_count == 0` in the
  web_profile_info test). The "drop valid zero" hazard is **not** present on the count path.
- **No false canonical count at the surface level:** the join (`:178-189`) preserves all per-surface
  candidates without selecting a winner; `test_join_preserves_conflicting_source_surface_candidates_without_selection`
  confirms DOM views and the two JSON counts are kept side-by-side. (Intra-node key collapse is the
  residual gap — F-04.)
- **Scope containment:** the module is pure (no network, browser, proxy, stealth, token-cost, runner,
  storage, projection, or ad-classification behavior). `permalink_url = urljoin(final_url, path)`
  (`:143`) is a derived string, not a navigation claim, matching the spec. `is_paid_partnership`/
  `is_affiliate` are trusted only when explicitly boolean (`:224-227`), avoiding an ad overclaim.

## Strict-Only Blockers / `not proven` boundaries

- No bound implementation-review lane, verdict vocabulary, severity taxonomy, validation gate, or
  patch-queue authority was supplied; therefore **no** formal verdict, severity, blocked/ready status,
  pass/fail, readiness, or executor-ready patch is claimed. All such claims are `NOT_CLAIMED` /
  `not proven` for this prompt.
- `controlling_source_state: mixed_dirty_worktree` — strict readiness and formal pass claims are not
  authorized; the `23 passed` run is inspected evidence only.
- Real IG payload shapes (carousel/reshare nesting, multi-count-key clip nodes, microsecond
  `device_timestamp`) are asserted from documented IG behavior and reproduced with synthetic fixtures;
  exact production payloads were **not** captured here (no live probe in scope). The failure
  *mechanisms* are reproduced; their *production frequency* is `not proven`.

## Open Questions (for the owner / next lane)

1. Is ambiguity-marking (F-01) in-scope for this slice, or deferred to the runner? The spec puts it on
   the parser; confirm before patch.
2. Should `device_timestamp` be dropped entirely (F-02) or normalized + labeled non-publish?
3. For multi-count-key nodes (F-04), does the owner want the selected key recorded, all candidates
   preserved, or precedence-only (accepting lost key identity)?
4. Is owner-verification of bare cross-profile permalinks (F-06) in-scope, or an accepted documented
   limitation?

## Residual Risk

Even with F-01..F-05 closed, the parser depends on the live runner supplying a faithful leaf-numeric
shape and source-surface labels; DOM/JSON shape drift on IG's side remains outside code's control (spec
"Not enforceable by code alone"). The advisory does not establish production stability, endpoint
stability, or that the four existing tests plus any added tests are exhaustive.

## Review-Use Boundary

These findings are **decision input only**. They are not approval, validation, readiness, a formal
verdict, a severity ruling, mandatory remediation, or executor-ready patch authority until separately
accepted or authorized. No source file was edited by this review.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- original commission / review target:
  Read-only adversarial code review of the IG public /reels/ grid parser slice
  (orca-harness/source_capture/ig_reels_grid.py + tests/unit/test_ig_reels_grid.py),
  commissioned by docs/prompts/reviews/instagram_reels_grid_parser_adversarial_code_review_prompt_v0.md.
  Read-only workflow-code-review with adversarial posture; multi-file impl diff is NOT
  delegated-patch-eligible, so no patch execution was authorized.

- implementation context, diff, and reviewed files:
  New pure-parser slice (no network/browser). Reviewed ig_reels_grid.py (1-409) and
  test_ig_reels_grid.py (1-154); context: ig_profile_grid_dom_engagement_recon_and_spec_v0.md,
  the architecture prompt, ig_momentum_harvest.py and its tests, and
  test_source_capture_ig_calls_packet.py. Worktree dirty/untracked for the named slice (expected).

- findings and implementation evidence:
  F-01 (HIGH) AMBIGUOUS_HIDDEN_NUMERIC defined (:26) but never emitted; _dom_parse_status (:336-343)
    always trusts positional hidden_candidates[0]/[1] (:134-137); value-based _subtract_visible_numbers
    (:323-333) misassigns on views/likes/comments value collisions. Repro: leaves [30,4,30] with
    views 30 -> likes='4', comments='30', status 'parsed_no_hover_grid_engagement' (both wrong, no flag).
  F-02 (HIGH) device_timestamp accepted as publish-time fallback (:208) + unguarded _timestamp_to_utc
    (:385-388). Repro: microsecond device_timestamp -> OSError [Errno 22], aborting the entire
    iter_json_media_candidates call and dropping all candidates.
  F-03 (MED-HIGH) _iter_media_nodes (:192-201) yields a matched node then recurses into it, double-yielding
    nested code/shortcode nodes; _string_or_none coerces int code (:391-397). Repro: nested code 'CHILD'
    -> 2 candidates; {'code':400} -> shortcode '400'. candidates_by_shortcode does not dedup.
  F-04 (MED) count precedence (:221) collapses multiple count keys and drops which key won; precedence
    may disagree with spec-validated ig_play_count DOM match.
  F-05 (MED) dedup is path-exact (:118,:125-127); abs/rel + trailing-slash/query variants of one reel
    duplicate rows; spec wants shortcode/permalink identity.
  F-06 (LOW-MED) _path_matches_handle (:294-300) cannot exclude bare cross-profile /reel/ permalinks.
  F-07 (LOW) _AD_TERM_RE (:30) matches bare words (partner/gifted/affiliate); mitigated by candidate-only labeling.
  F-08 (LOW-MED) tests miss F-01..F-06 invariants; 23 passed does not constrain them.
  Nits N-1..N-3 and positive affirmations (zero preserved, no surface-level canonical count, scope clean) recorded.

- proposed patch, diff, or exact requested edits, if authorized: NOT_CLAIMED (read-only; no patch authorized).

- citations: spec ig_profile_grid_dom_engagement_recon_and_spec_v0.md (Current Finding, Parse Statuses,
  Code-Enforceable Capture Rules); architecture prompt Q5/Q6; impl line anchors above; live repros this turn.

- reviewer verdict: NOT_CLAIMED (advisory findings only; no formal verdict / severity / readiness authority).

- validation evidence and not-run checks: focused pytest reran -> 23 passed (inspected, not a pass claim).
  Four ad-hoc repros confirmed F-01/F-02/F-03. Same-check red-green for each finding: NOT RUN (read-only).

- residual risk: IG payload-shape drift outside code control; production frequency of the reproduced
  mechanisms not proven; test exhaustiveness not established.

- blockers, off-scope flags, and not-proven boundaries: no bound review lane/verdict/severity/validation-gate/
  patch authority supplied -> formal verdict, severity, readiness, pass/fail, patch queue all NOT_CLAIMED.
  Live IG probe, runner wiring, projection, and ad classification are off-scope for this parser slice.
```
