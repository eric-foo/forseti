# Capture Session Fast Path Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated code review (delegated_code_review_and_patch mode) of the
  capture-session fast-path diff (browser/context/page reuse across a TikTok
  live-batch session, per-capture listener/route detachment, measured 10s
  cadence default, post-click challenge-handoff coverage expansion,
  first-comment-only semantics, and safe subtitle-host diagnostics), plus
  adversarial artifact review of the paired playbook prose, with the
  reviewer's findings adjudicated by the commissioning Chief Architect.
use_when:
  - Consuming the delegated review findings for the capture-session fast-path diff.
  - Checking which lifecycle/challenge-handling/receipt defect classes were
    investigated, confirmed, defeated, or left open for CA adjudication.
authority_boundary: retrieval_only
reviewed_by: Anthropic Claude (Sonnet 5)
authored_by: OpenAI Codex / GPT-5
de_correlation_bar: cross_vendor_discovery
commission: chat_thread_current_session
review_target: >
  branch codex/capture-session-fast-path, head
  7f496e7cd4ad7b30cf47d423c9a9a891bb2d18ce, diff base
  a98f056c9d5d3e325f38abece3619552115698a7
mode: delegated_code_review_and_patch
access: repo
source_context_ready: true
report_written: docs/review-outputs/capture_session_fast_path_delegated_adversarial_code_review_v0.md
patch_status: no_patch_applied_no_confirmed_defect_reached_patch_threshold
stale_if:
  - A later review round over the same scope replaces this report.
  - The reviewed branch is force-pushed to a different head.
non_claims:
  - not validation
  - not readiness
  - not acceptance
  - not runtime model routing
  - not a claim that every theoretically-possible Playwright fault path was exhaustively tested
```

Use boundary: all findings, citations, and verdicts in this report are decision
input only — not approval, not validation, not readiness, not mandatory
remediation, and not patch authority. What is kept, escalated, or dismissed is
decided solely by the commissioning Chief Architect's adjudication under
`.agents/workflow-overlay/review-lanes.md`.

## De-correlation gate

- Author: OpenAI Codex / GPT-5 (per commission).
- Controller (this review): Claude Sonnet 5 (Anthropic) — a different upstream
  vendor from the author. Cross-vendor discovery bar satisfied.
- `de_correlation_bar: cross_vendor_discovery`.

## Preflight

- `AGENTS.md` and `.agents/workflow-overlay/README.md`: read (see Source
  Context Ready below).
- Commissioned worktree: `C:\tmp\forseti-capture-session-fast-path`, branch
  `codex/capture-session-fast-path`, HEAD
  `7f496e7cd4ad7b30cf47d423c9a9a891bb2d18ce` — matched exactly via
  `git worktree list --porcelain`; confirmed clean with
  `git status --porcelain=2 --branch` (no untracked files, `+0 -0` ahead/behind
  its own upstream).
- Diff range verified: `git log --oneline` over
  `a98f056c9d5d3e325f38abece3619552115698a7..7f496e7cd4ad7b30cf47d423c9a9a891bb2d18ce`
  shows exactly two commits (`efc28fec`, `7f496e7c`); `git diff --stat` over the
  same range touches exactly the nine commissioned files, no more, no fewer.

### Target file SHA-256 pin verification

All nine pins matched exactly (`Get-FileHash -Algorithm SHA256` against the
commissioned worktree, before any read or edit):

| # | File | Match |
| - | ---- | ----- |
| 1 | `forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py` | MATCH |
| 2 | `forseti-harness/runners/run_source_capture_tiktok_live_batch_probe.py` | MATCH |
| 3 | `forseti-harness/source_capture/adapters/browser_snapshot.py` | MATCH |
| 4 | `forseti-harness/source_capture/tiktok/creator_onboarding.py` | MATCH |
| 5 | `forseti-harness/source_capture/tiktok/live_batch_probe.py` | MATCH |
| 6 | `forseti-harness/tests/unit/test_source_capture_browser_snapshot.py` | MATCH |
| 7 | `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py` | MATCH |
| 8 | `forseti-harness/tests/unit/test_tiktok_live_batch_probe.py` | MATCH |
| 9 | `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | MATCH |

## `SOURCE_CONTEXT_READY`

Read in full: `AGENTS.md`, `.agents/workflow-overlay/README.md`,
`.agents/workflow-overlay/delegated-review-patch.md`,
`.agents/workflow-overlay/review-lanes.md`,
`.agents/workflow-overlay/source-loading.md`,
`.agents/workflow-overlay/validation-gates.md`,
`.agents/workflow-overlay/communication-style.md`, the complete diff for both
commits, and all nine target files (including adjacent called code:
`_capture_page_observation` call sites in both `_PlaywrightBrowserSnapshotEngine`
and `_CloakBrowserPageObservationEngine`, `_SessionBrowserProxy`/
`_SessionContextProxy`/`_SessionPageProxy`, `_should_run_human_challenge_handoff_after_action`,
`_run_human_challenge_handoff`, `_page_owned_comment_list_responses`,
`_subtitle_capture_from_item_struct`, `assert_no_sensitive_tiktok_material`/
`find_sensitive_tiktok_material` in `source_capture/tiktok/admission.py`, the
`post_load_pointer_action`/`post_load_pointer_actions` mutual-exclusivity guard
in `browser_snapshot.py`, the TikTok batch-loop challenge `break` logic and
`_validate_staging_contracts` allowlist in `batch_packet.py`). No source gap
was identified that would change a claim in this report.

`SOURCE_CONTEXT_READY: true`.

Required upstream skills (`workflow-deep-thinking`, `workflow-code-review`,
`workflow-adversarial-artifact-review`) were reference-loaded per the
commission's method order; `workflow-code-review` mechanics (failure-mode
decomposition, evidence-before-claim, coverage-first find stage) were applied
to the Python diff and tests; `workflow-adversarial-artifact-review` mechanics
(steelman-then-defend, considered_and_defended discard pile) were applied to
the playbook prose and its code/receipt consistency.

## Executive summary

The diff delivers exactly what the fitness reference asks for and every
required-validation command passes clean. I found no confirmed critical or
major defect. Two low-confidence/minor findings survive adversarial pressure
(an unlikely double-fault gap in per-capture binding detachment, and an
incomplete — not wrong — receipt-field description in the new playbook prose);
one candidate finding that looked real on first pass (a "singular pointer
action can leave a challenge suppression unchecked before the loop runs")
is defeated by an existing mutual-exclusivity guard and is recorded under
`considered_and_defended`. No patch was applied: nothing reached a confirmed
defect that a smallest-complete code correction would fix, and the commission
requires patching only confirmed findings.

## Findings

### FF-01 — minor — [browser_snapshot.py] `_SessionPageProxy.detach_capture_bindings` has no partial-failure recovery

Evidence: `forseti-harness/source_capture/adapters/browser_snapshot.py`
(`_SessionPageProxy.detach_capture_bindings`, lines ~1672-1690 in the reviewed
head). The method iterates `self._listeners` calling `remove_listener(event,
callback)` for each, then only after that loop completes does it iterate
`self._routes` calling `unroute(pattern, handler)`. If a real
`remove_listener`/`off` call raises partway through the listener loop (for
example because a listener was recorded in `_SessionPageProxy.on` before the
underlying `self._page.on(...)` call actually completed, or because of a
transport-level fault), the method raises out of `_SessionContextProxy.close()`,
which is itself invoked from the outer `finally: context.close()` in
`_CloakBrowserPageObservationEngine.capture_page_observation`. Two
consequences: (a) `self._routes` is never cleared and `unroute` is never
attempted for this capture, so a route registered on the real
(session-persistent) page can remain bound into the next capture even though
the owning `_SessionPageProxy` instance is discarded; (b) a successful capture
result already computed inside the `try` block is discarded because the
`finally` raised, converting what should read as a completed capture into an
unhandled exception.

Impact: this is exactly the "double-fault" class the commission asked to be
checked for, but it requires a real Playwright API call (`remove_listener`/
`unroute`) to itself fail — something that essentially never happens against a
real `Page` object (both are standard, always-available methods on Playwright
sync pages) and is not exercised by the fixture/test double in this diff. I
could not construct a realistic trigger in the reviewed code paths; I list it
because the review explicitly asked for double-fault coverage and because the
gap is real on the code as written, not because I have a reproduction.

minimum_closure_condition: either (a) an inline comment/owner decision
recording this as an accepted residual (matches the fitness reference's
"bounded and acceptable" posture for genuinely rare double-faults), or (b) if
the CA wants it hardened, `detach_capture_bindings` attempts every
listener/route detachment (e.g., via a best-effort loop that collects
exceptions and re-raises only after attempting all removals) so a single
failed detach cannot suppress the rest.

next_authorized_action: Chief Architect adjudicates; no patch applied (low
confidence, no observed trigger, would require judgment about how much
Playwright-internal defensiveness this session-reuse layer should carry).

### FF-02 — minor — [source_capture_playbook_v0.md] New "Launch and session economy" prose under-describes the actual receipt shape

Evidence: `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`,
new "Launch and session economy" section: "Multi-page receipts record
browser-launch count, context-creation count, capture attempt/success counts,
and close state." The actual `CloakBrowserPageObservationSessionEngine.lifecycle_receipt`
(browser_snapshot.py) also carries `page_creation_count` and
`page_reuse_policy`, which the prose does not mention.

Impact: not a contradiction — every field the prose names is present — but a
future reader relying on the playbook's prose alone would not know the receipt
also proves one-page reuse (`page_creation_count == 1` across a multi-item
batch), which is one of the two concrete lifecycle facts this whole change
exists to make checkable. This is a documentation completeness gap, not a code
defect.

minimum_closure_condition: the playbook sentence names `page_creation_count`
and `page_reuse_policy` alongside the fields already listed, or explicitly
says the list is illustrative rather than exhaustive.

next_authorized_action: Chief Architect adjudicates; optional prose tightening,
non-blocking.

## `considered_and_defended`

- **Candidate**: In both `_PlaywrightBrowserSnapshotEngine.capture_page_observation`
  and `_CloakBrowserPageObservationEngine.capture_page_observation`, the
  singular `post_load_pointer_action` runs and sets
  `pointer_actions_suppressed = maybe_run_handoff(post_load_pointer_action.action_name)`,
  and execution then unconditionally enters `for pointer_action in
  post_load_pointer_actions: ...` without checking `pointer_actions_suppressed`
  first — looking like a gap where one more scripted pointer action could run
  after an uncleared challenge. **Defense**: `fetch_browser_page_observation_capture`
  (the public entry point, lines ~482-487) enforces
  `post_load_pointer_action` and `post_load_pointer_actions` as mutually
  exclusive before either engine is ever constructed — if the singular form is
  set, the normalized plural tuple is always empty, so the `for` loop always
  iterates zero times whenever the singular branch could have set
  `pointer_actions_suppressed = True`. Confirmed the only production caller,
  `source_capture/tiktok/live_batch_probe.py`, exclusively uses the plural
  `post_load_pointer_actions=` form (grep-verified: no call site anywhere in
  the reviewed tree passes both). Defeated; not a real code path.
- **Candidate**: the playbook's "reuse the measured recipe-card value instead
  of inheriting a slower discovery/probe default" could read as an unverified
  empirical claim that 10.0s specifically was measured for TikTok. **Defense**:
  the commission's own fitness reference explicitly authorizes "approximately
  ten seconds" as the intended new default; the playbook sentence is generic
  forward-looking method guidance for any source with a recipe card, not a
  specific evidentiary claim tied to the TikTok literal. No overclaim against
  the bound fitness reference.
- **Candidate**: cosmetic soft-wrap in the playbook diff ("Per-item\nbrowser
  isolation is allowed only when...") looked like a stray line break.
  **Defense**: Markdown renders soft-wrapped lines within one paragraph
  identically to a single line; no rendered-meaning change. Not worth a
  finding entry.

## Fitness-reference check (owner-requested outcome)

Each bullet below is the outcome named in the commission, with the evidence
that it holds in the reviewed diff:

- **Retains one browser and context across a batch**: `CloakBrowserPageObservationSessionEngine`
  launches the real browser/context exactly once (`_launch_settings`/
  `_context_settings` guards raise if a caller tries to change them mid-session);
  `run_tiktok_live_batch_probe` now auto-constructs and owns this session
  engine whenever `engine is None and browser_backend == "cloakbrowser"`, and
  closes it in a `finally` after the whole batch. Verified by
  `test_default_cloakbrowser_batch_reuses_one_owned_session` (one engine
  instance reused across two videos, closed exactly once) and
  `test_cloakbrowser_page_observation_session_reuses_one_context_and_closes_once`
  (`browser_launch_count == 1`, `context_creation_count == 1` across two
  captures).
- **Reuses one tab by navigating between deep captures**: `_get_or_create_page`
  returns the same real page unless it was closed; `page_creation_count == 1`
  across two captures in the same test.
- **Does not accumulate response listeners, routes, or per-capture bindings**:
  `_SessionPageProxy` tracks only the current capture's own `.on()`/`.route()`
  calls and `detach_capture_bindings()` removes exactly those in
  `_SessionContextProxy.close()`, called from the existing per-capture
  `finally: context.close()`. Verified: `remove_listener` count == 2 and
  `unroute` count == 2 for 2 captures with `route` count == 2 (one blocked
  resource-type route per capture, added then removed each time).
- **Defaults TikTok pacing to ~10s while preserving explicit overrides and
  challenge stops**: `TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS = 10.0` now
  backs every min/max cadence default across the library functions and both
  CLI runners; overrides remain ordinary keyword/CLI arguments, unaffected.
  Verified by `test_onboarding_cli_defaults_to_measured_ten_second_gap` and
  `test_live_probe_cli_defaults_to_measured_ten_second_gap`. Challenge-stop
  logic (the batch-loop `break` on a detected challenge/auth-wall marker in
  `run_tiktok_live_batch_probe`) is untouched by this diff.
- **Visibly hands off when a challenge appears before or after a pointer
  action**: `_tiktok_human_challenge_handoff_after_action_names()` now also
  checks after `TIKTOK_RETRY_VISIBLE_ERROR_POINTER_ACTION_NAME`,
  `TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME`,
  `TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME`,
  `TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME`, and
  `TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME` (previously only after page
  load), all of which are real pre-existing action-name constants (grep
  confirmed, no typos).
- **Suppresses subsequent actions while an uncleared challenge remains**: the
  `for pointer_action in post_load_pointer_actions:` loop now captures
  `maybe_run_handoff`'s return value and `break`s when it is `True` (previously
  the return value was discarded and the loop ran to completion regardless).
  Verified by the new
  `test_post_action_handoff_stops_remaining_actions_when_challenge_persists`
  (asserts exactly one `mouse_click` and one handoff attempt across two
  configured actions).
- **Captures only the first platform-default comment response, no pagination
  or "top comments" ranking claim**: `TIKTOK_COMMENT_LIST_RESPONSE_CAP = 1`;
  `_page_owned_comment_list_responses` iterates `capture_result.responses` in
  arrival order and stops at the cap — first-seen, not ranked. New
  `capture_contract` keys `comment_selection_policy:
  "platform_default_first_response_only"` and `comment_pagination: false` make
  the semantics explicit and are additive to the existing
  `_validate_staging_contracts` allowlist check in `batch_packet.py` (a subset
  check, not an exact-key check, so the new keys don't break admission).
  Verified by
  `test_live_probe_keeps_only_platform_default_first_comment_response`.
- **Diagnoses unsupported subtitle hosts using safe hostname metadata only /
  never persists raw or signed subtitle URLs**: `_subtitle_capture_from_item_struct`
  now records `subtitle_url_host` (bare, lower-cased, trailing-dot-stripped
  `urlparse(...).hostname`) and `subtitle_url_host_supported`, alongside the
  pre-existing `subtitle_url_sha256`/`subtitle_url_length`. The full URL is
  never placed in the returned dict on any path, and every return path still
  calls `assert_no_sensitive_tiktok_material(base/result)`. Verified by
  `test_live_probe_rejects_unanchored_subtitle_host_without_fetch`, which
  asserts the raw attacker URL is absent from the serialized cadence JSON
  while the hostname is present. The allowlist itself
  (`TIKTOK_SUBTITLE_ALLOWED_HOST_SUFFIXES`) is untouched by this diff — no
  broadening without evidence.
- **Preserves visible failure when subtitle acquisition is unsupported**:
  unchanged control flow — `base["reason"]` is still set and returned on the
  unsupported-host path; only new hostname metadata was added alongside it.
- **Does not silently mutate creator-registry or data-lake state during
  probe-only capture**: no file touched by this diff is in the
  registry/admission/data-lake write path (`source_capture/tiktok/admission.py`,
  `batch_packet.py`'s writer, or lake modules were read for context only, never
  modified).
- **Keeps runtime receipts, runners, tests, and the playbook mutually
  truthful**: see FF-02 for the one incomplete-but-not-false description found;
  otherwise the new receipt fields, contract keys, and CLI defaults are
  consistent across the library, both runners, and their tests.

## Validation

| # | Command | Result |
| - | ------- | ------ |
| 1 | `python -m pytest forseti-harness/tests/unit/test_source_capture_browser_snapshot.py forseti-harness/tests/unit/test_tiktok_live_batch_probe.py forseti-harness/tests/unit/test_tiktok_creator_onboarding.py -q` | GATE PASS — exit 0, 118 passed, 0 failed, 0 errors (dot/`F`/`E` count verified programmatically since this pytest configuration does not print the usual summary line). Matches commissioning baseline of 118 passed. |
| 2 | `python -m pytest forseti-harness/tests/contract/test_source_capture_browser_snapshot_contract.py forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py -q` | GATE PASS — exit 0, 21 passed, 0 failed, 0 errors. Matches commissioning baseline of 21 passed. |
| 3 | `python .agents/hooks/check_retrieval_header.py --strict forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | GATE PASS — exit 0. |
| 4 | `python .agents/hooks/check_doc_terms.py --check` | INFO / non-gating — exit 0; report-mode ontology-term scan, 4 new-term candidates listed (unrelated to the reviewed files; none of the nine target files appear in the candidate list). |
| 5 | `git diff --check` (over the commissioned range) | GATE PASS — exit 0, no whitespace errors. |
| 6 | `python .agents/hooks/check_review_routing.py --strict` | GATE PASS — exit 0 (`check_review_routing --strict: OK (base: origin/main)`). |

A green check above is shape/mechanical evidence only, per
`.agents/workflow-overlay/validation-gates.md`; it is not validation,
readiness, or approval of this report's findings or verdict.

## Verdict and residual risks

No confirmed critical or major defect. Recommendation:
`accept_with_friction` — the diff is correct against the bound fitness
reference and every named validation command passes, but two minor,
low-confidence findings (FF-01, FF-02) remain open for the Chief Architect to
adjudicate before treating this as fully closed. No patch was applied because
neither finding reached a confirmed-defect threshold that a smallest-complete
code change would fix without speculative hardening; `patch: none`.

Residual risks (named, not scored): (1) FF-01's double-fault gap is bounded to
an essentially-never-observed Playwright API failure mode and is acceptable
below a buyer-proof-tier bar; (2) no load/soak test of the session-reuse path
across a large batch (e.g., dozens of videos) was run as part of this review —
only the existing unit/contract fixtures — so long-run page/context stability
under real CloakBrowser conditions remains unverified by this pass.

## `NEEDS_ARCHITECTURE_PASS`

Not invoked. Nothing found requires architecture, product-policy,
security-policy, or cross-lane authority to close; both open findings are
ordinary code/doc adjudication items within the commissioning Chief
Architect's own authority.

## Courier — Chief Architect adjudication instructions

Per `.agents/workflow-overlay/delegated-review-patch.md` (Adjudication
closeout) and `.agents/workflow-overlay/communication-style.md` (Review
Adjudication Next Step): adjudicate FF-01 and FF-02 and the
`considered_and_defended` entries as claims, not premises. Both findings are
self-closable within the commissioned scope (docs/prose tightening for FF-02;
an optional code hardening for FF-01) if the CA chooses to act on them, or may
be recorded as accepted residuals with no code change. Once adjudicated, batch
any resulting admin/lifecycle steps (commit, push, PR) into one land step with
no deep-thinking; if a visible active goal or accepted next objective exists,
name the 1-5 next material moves that best advance it in the same turn,
otherwise record `no_visible_active_goal`.

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/capture_session_fast_path_delegated_adversarial_code_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: claude-sonnet-5
  authored_by: gpt-5 (OpenAI Codex)
  summary: "Capture-session fast-path diff correctly delivers session/page/route reuse, expanded challenge-handoff coverage with real action suppression, 10s cadence defaults, first-comment-only semantics, and safe subtitle-host diagnostics; no confirmed critical/major defect; two minor open findings for CA adjudication; no patch applied."
  findings_count: 2
  blocking_findings: []
  advisory_findings:
    - FF-01: Double-fault gap in per-capture listener/route detachment (unlikely, no reproduction)
    - FF-02: Playbook receipt-field description omits page_creation_count/page_reuse_policy
  prior_findings_remediated: []
  next_action: "Chief Architect adjudicates FF-01 and FF-02, then runs the one-batch land step plus goal-conditioned material-moves check."
```

## Chief Architect adjudication — 2026-07-12

- **FF-01 — accepted residual; no code change.** The candidate failure requires
  Playwright listener/route detachment itself to raise. Preserving the raised
  failure is correct because a capture whose cleanup failed is not safely
  complete. The review did not establish a realistic open-page trigger or a
  safe recovery contract; adding exception swallowing, page quarantine, or
  retry behavior would therefore be speculative lifecycle policy. Upgrade this
  residual only if a real detach failure is observed or a focused test exposes
  stale bindings crossing into a later capture.
- **FF-02 — accepted and closed.** The playbook now names
  `page_creation_count` and `page_reuse_policy` alongside the other lifecycle
  receipt fields, making the one-tab reuse proof discoverable without reading
  the implementation.
- **`considered_and_defended` — accepted.** The singular/plural action forms are
  mutually exclusive at the public boundary, the cadence prose is authorized
  by the bound fitness reference, and the Markdown soft wrap has no semantic
  effect.

**Adjudicated verdict:** accept. No unresolved material issue remains. The
remaining named risks are the unobserved Playwright detach double-fault and the
absence of a long real-browser soak run; neither blocks this bounded change.
