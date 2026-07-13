# TikTok Persistent Onboarding Navigation And Progress Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial code review (delegated_code_review_and_patch mode) of the
  combined TikTok persistent creator-onboarding navigation, progress-visibility,
  account-safety circuit-breaker, and Chrome CDP auth-root alignment diff on
  branch codex/review-tiktok-persistent-onboarding at head
  3cd83e63f6da22bc109d1f817a16802122cb4bbc, with the reviewer findings left for
  Chief Architect adjudication.
use_when:
  - Consuming the delegated review verdict for the persistent-onboarding diff.
  - Checking which navigation, progress, account-safety, lifecycle, and
    auth-root defect classes were investigated, confirmed, or defeated.
authority_boundary: retrieval_only
reviewed_by: Anthropic Claude (Opus 4.8)
authored_by: OpenAI Codex / GPT-5
de_correlation_bar: cross_vendor_discovery
commission: >
  docs/prompts/reviews/tiktok_persistent_onboarding_navigation_progress_delegated_adversarial_code_review_patch_prompt_v0.md
  (authoritative copy read from C:\tmp\forseti-chrome-cdp-auth-root-fix)
review_target: >
  branch codex/review-tiktok-persistent-onboarding, head
  3cd83e63f6da22bc109d1f817a16802122cb4bbc, base merge point
  dae46bbe8b98d6c3967648491da15244bd26fea5, range origin/main...HEAD
mode: delegated_code_review_and_patch
access: repo
source_context_ready: true
report_written: docs/review-outputs/tiktok_persistent_onboarding_navigation_progress_delegated_adversarial_code_review_v0.md
patch_status: no_patch_applied_no_confirmed_defect_reached_patch_threshold
superseded_review_note: >
  ccc77aaa is explicitly superseded and was not reviewed. Its accepted F1
  (auth-root alignment) is confirmed present at 3cd83e63 and not re-patched.
stale_if:
  - A later review round over the same scope replaces this report.
  - The reviewed branch is force-pushed to a different head.
non_claims:
  - not validation
  - not readiness
  - not acceptance
  - not runtime model routing
  - not a claim that any live TikTok, OAuth, CAPTCHA, or browser path was exercised
```

Use boundary: all findings, citations, and verdicts in this report are decision
input only — not approval, not validation, not readiness, not mandatory
remediation, and not patch authority. What is kept, escalated, or dismissed is
decided solely by the commissioning Chief Architect's adjudication under
`.agents/workflow-overlay/review-lanes.md` and the delegated-review-patch
convention in `.agents/workflow-overlay/delegated-review-patch.md`.

## De-correlation gate

- Author vendor: OpenAI Codex / GPT-5 (per commission).
- Reviewer/controller vendor: Anthropic Claude (Opus 4.8) — a different upstream
  vendor from the author. Cross-vendor discovery bar satisfied.
- `de_correlation_bar: cross_vendor_discovery`. This is a who-constraint only,
  not a runtime-model recommendation.

## Provenance and preflight verification

All preflight bindings were verified against the target worktree
`C:\tmp\forseti-persistent-onboarding-review` before review. Observed:

- `git rev-parse HEAD` = `3cd83e63f6da22bc109d1f817a16802122cb4bbc` (matches required head).
- `git rev-parse --abbrev-ref HEAD` = `codex/review-tiktok-persistent-onboarding` (matches).
- `git status --porcelain=v1` = empty (clean tree, required state).
- `git merge-base origin/main HEAD` = `dae46bbe8b98d6c3967648491da15244bd26fea5` (matches base merge point).
- `origin/main` = `15436f9a0d8f56e925d056f13ebbfe9de5282239` (ahead of the merge base; the three-dot range resolves to the merge base, so scope is unaffected).

All ten pinned committed Git blob IDs were verified with
`git rev-parse 3cd83e63f6da22bc109d1f817a16802122cb4bbc:<path>` and each matched
the commission exactly:

```text
ceaffa44e6a9d80d6007693f5f333aa3a5351af1  forseti-harness/docs/source_capture_agent_runbook.md
04d0f06b6608afb1538b11614c2a21a4f0f045e9  forseti-harness/runners/run_source_capture_chrome_cdp_session.py
b5e54d1d8d3f11954bfff82c4e6b824e0d35e31b  forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py
8ec87cc282f5cdc471cd2f55c9188d2f85d433b9  forseti-harness/source_capture/adapters/browser_snapshot.py
6fed79f8c65401260f534400d0e5d721593d7757  forseti-harness/source_capture/tiktok/creator_onboarding.py
e4596148ec1ee20f2cbafa938549ae724162e627  forseti-harness/source_capture/tiktok/live_batch_probe.py
405c55a16873bdf6574fc86f56d42d287f8fdfd7  forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
dc268bcea4581a1e39887c5e34134dca8d33ba47  forseti-harness/tests/unit/test_source_capture_chrome_cdp_session.py
7160f3c7a95ffc2bb8764b6a3a471b9ad710f0d4  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
6b727b771ced58554e12c807304e2aa7317d3ae4  forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
```

`git diff --name-status origin/main...HEAD` reports exactly these ten paths and
no others (597 insertions, 12 deletions), so the diff is inside the named patch
scope with no silent widening.

## Source-readiness (SOURCE_CONTEXT_READY)

Confirm-don't-trust source load complete. Read before any strict claim:

- Commission (authoritative copy, full).
- `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/delegated-review-patch.md`,
  `.agents/workflow-overlay/safety-rules.md`.
- Complete diff `origin/main...HEAD` (all ten files).
- All ten named files at working-tree state (byte-consistent with the verified
  blobs on a clean tree), plus the read-only collaborators the behavior depends
  on: `source_capture/tiktok/blocker_triage.py` (classification), the engine
  classes and `_pre_action_stop_marker_receipt` / `_page_text_marker_match_result`
  helpers in `browser_snapshot.py`, and `TikTokCreatorOnboardingError`.

Method applied: `workflow-deep-thinking` then `workflow-code-review`
(delegated_code_review_and_patch), strict mode. `SOURCE_CONTEXT_READY`.

## Fitness-contract adjudication (evidence)

Each accepted-behavior clause was checked against source; all hold.

1. One warm CLI invocation owns Registry preflight and alias resolution.
   `run_source_capture_tiktok_creator_onboarding.py:132-151` runs
   `_write_creator_registry_preflight` and `resolve_session_profile` internally;
   the runbook's direct-invocation note (`source_capture_agent_runbook.md`
   +18..+33) matches and preserves the failure gate ("unless it emits a
   blocker").
2. Retained operator Chrome stays the authority; one runner page reused;
   detach-without-close. `ChromeCdpPageObservationSessionEngine`
   (`browser_snapshot.py:1597`) attaches via `connect_over_cdp`
   (`:1673`), reuses one page in `_get_or_create_page` (`:1711-1721`), and
   `close()` (`:1739-1750`) calls `browser.close()` on a CDP-connected browser,
   which disconnects rather than terminating the operator process/tabs —
   matching `close_policy: detach_only_leave_browser_and_page_open`.
3. Direct selected-video URLs in selection order on one page, no grid return,
   final video visible after detach. The live-probe loop navigates
   `normalized_video_urls` in order (`live_batch_probe.py:450-491`); onboarding
   builds `selected_urls` from `selected_video_ids` in review-priority order
   (`creator_onboarding.py:325-332`); no grid navigation occurs between videos;
   `test_onboarding_writes_selection_before_same_engine_deep_capture` pins the
   selection-order URLs.
4. No address-bar typing, referrer spoofing, chrome pointer ceremony, fake
   clicks, OS pointer control, or CAPTCHA solving. `_capture_contract`
   (`live_batch_probe.py:2316-2340`) records `address_bar_simulation=False`,
   `referrer_spoofing=False`, `return_to_grid_between_videos=False`,
   `pointer_movement_policy=meaningful_page_actions_only`; no new pointer/typing
   code is introduced by the diff.
5. Flushed, machine-readable, non-secret progress distinguishing preflight,
   grid, selection, deep capture, close, admission, and blocker states.
   `_emit_progress`/`_emit_blocker` (`runner:271-284`) use
   `print(..., flush=True)` with sorted-key JSON; stage events fire in
   `creator_onboarding.py` via `_notify_progress`; fields are event names plus
   handle/alias/counts — no credentials or tokens.
6. Account-risk / logged-out-comment-auth wall / `/login` redirect suppresses
   scripted actions before the next pointer action, stops the batch, forbids
   auto-retry, leaves Chrome open, emits `ACCOUNT_SAFETY_STOP`; a cleared
   CAPTCHA may continue. Two independent, composing mechanisms:
   (a) pre-action suppression — `_pre_action_stop_marker_receipt`
   (`browser_snapshot.py:2654-2689`) checked via `maybe_stop_before_action`
   before every pointer action and before the handoff (`:943-983`,
   `:1401-1441`); markers `TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS`
   (`live_batch_probe.py:153-158`) are disjoint from the CAPTCHA handoff markers
   `TIKTOK_CHALLENGE_TEXT_MARKERS` (`:147-152`), so an account-risk warning can
   never be routed to the clearable-CAPTCHA handoff; (b) batch stop —
   `classify_tiktok_blocker` (`blocker_triage.py`) maps the three account-safety
   signals to `challenge_kind` account_risk / logged_out_or_auth_wall /
   login_or_auth_wall (account-risk checked first in `_challenge_kind_from_text`),
   `_challenge_reason_from_triage` returns non-None, the loop appends a failure
   and `break`s (`live_batch_probe.py:516-572`), and `_blocker_triage_receipt`
   (`:852-864`) stamps `account_safety_stop=True`,
   `automatic_retry_allowed=False`. `_has_account_safety_stop`
   (`creator_onboarding.py:750-761`) reads that triage; onboarding raises
   `TikTokCreatorOnboardingError("account_safety_stop")` (`:380`); the CLI maps
   `str(exc)=="account_safety_stop"` to blocker `ACCOUNT_SAFETY_STOP` phase
   `deep_capture`, exit 2 (`runner:168-179`). Chrome stays open because the
   owned CDP engine's `close()` only detaches. Tests
   `test_live_probe_account_risk_is_non_retriable_batch_stop`,
   `test_page_load_account_safety_stop_suppresses_actions_without_handoff`,
   `test_cloakbrowser_account_safety_stop_suppresses_actions_without_handoff`,
   and `test_onboarding_cli_emits_dedicated_account_safety_stop` pin these.
7. Engine-specific lifecycle/pre-action guarantees are emitted only when the
   selected engine supports them; fallbacks stay neutral. `_capture_contract`
   gates `video_page_reuse_policy` and `terminal_page_policy` on
   `session_engine_reused` and `account_safety_pre_action_circuit_breaker` on
   `bool(getattr(engine,"pre_action_stop_markers",()))`
   (`live_batch_probe.py:762-786`, `:2316-2340`), falling back to
   `capture_engine_defined` / `False`. `fetch_browser_page_observation_capture`
   has no pre-action-stop parameter (`browser_snapshot.py:419-453`), so the
   suppression is genuinely engine-borne and the fallback report is truthful.
   `test_capture_contract_reports_verified_session_engine_guarantees` and the
   subtitle-transcript test pin both the verified and neutral shapes.
8. Existing capture artifacts, selection order, challenge handoff, cadence,
   first-comment behavior, auth-state safety, and failure visibility remain
   intact. The cleared-CAPTCHA-continues path is unchanged: the handoff only
   fires on the disjoint CAPTCHA markers and returns not-suppressed on clear
   (`browser_snapshot.py:921-941`); pre-action stop returns None when no
   account-safety marker is present, so it does not interfere with a legitimate
   CAPTCHA handoff.
9. Chrome bootstrap default auth-state root aligns with logical
   session-profile resolution. `run_source_capture_chrome_cdp_session.py:53-56`
   now defaults `auth_state_root` to `default_session_profile_auth_state_root()`,
   the same default the onboarding runner uses (`runner:142`);
   `test_chrome_cdp_session_bootstrap_...` monkeypatches that resolver and drops
   the explicit arg, confirming alignment. This is the prior-review F1 closure
   and it composes with the new progress work (independent code paths).

## Findings ordered by severity

No blocker, major, or minor correctness finding was confirmed. Three
informational observations are recorded as decision input; none reaches the
commission's patch bar (confirmed defect with practical regression proof) and
none was patched.

### INFO-1 — mixed handoff-then-stop can over-attribute one suppression flag

- Reviewed target: `browser_snapshot.py:1083-1086`, `:1544-1547`
  (`pointer_actions_suppressed_by_human_challenge_handoff`).
- Evidence: the field is `pointer_actions_suppressed and bool(human_challenge_handoff_receipts)`.
  In the rare sequence where a CAPTCHA handoff clears on action N (receipt
  recorded, not suppressed) and a pre-action account-safety stop suppresses on
  action N+1, both `human_challenge_handoff_receipts` is non-empty and
  `pointer_actions_suppressed` is True, so this flag reads True although the
  final suppression was the pre-action stop.
- Impact: receipt-cosmetic only. The field is consumed only by tests (grep of
  `forseti-harness` shows no behavior consumer); the authoritative pre-action
  indicator `pointer_actions_suppressed_by_pre_action_stop` and
  `pre_action_stop_attempts` are separately True, and the batch account-safety
  determination is triage-driven, not flag-driven. Strictly better than the
  pre-diff behavior (which set the field True on any suppression). No false
  negative when a handoff genuinely suppresses.
- `minimum_closure_condition`: a durable receipt consumer would have to depend on
  this flag alone to distinguish stop-vs-handoff, which none does today.
- `next_authorized_action`: none required; note only.

### INFO-2 — account-safety propagation uses a magic-string sentinel

- Reviewed target: `creator_onboarding.py:380` raising
  `TikTokCreatorOnboardingError("account_safety_stop")` and `runner:169`
  matching `str(exc)=="account_safety_stop"`.
- Evidence: cross-module coupling by exact message string rather than a typed
  exception or attribute.
- Impact: works today and is identity-preserved on re-raise; a future edit to the
  message in one place only would silently downgrade the CLI blocker to
  `ONBOARDING_PRECHECK_OR_CAPTURE_FAILED`. This regression is guarded by
  `test_onboarding_cli_emits_dedicated_account_safety_stop`, which pins the exact
  string and the `ACCOUNT_SAFETY_STOP` output. Not a current defect.
- `minimum_closure_condition`: divergence between the two literals with the
  guarding test also changed.
- `next_authorized_action`: none required; optional future robustness (typed
  sentinel) is out of the confirmed-defect patch scope.

### INFO-3 — preflight-block and generic capture-failure share one blocker code/phase

- Reviewed target: `runner:171-174` emits
  `ONBOARDING_PRECHECK_OR_CAPTURE_FAILED` phase `onboarding` for both a Registry
  preflight block and a generic capture failure.
- Evidence: the fitness contract asks progress to distinguish preflight, grid,
  selection, deep capture, close, admission, and blocker states; the blocker
  phase does not separately name `preflight` for a preflight block.
- Impact: minor visibility granularity only; the code name is honest
  ("PRECHECK_OR_CAPTURE"), the dedicated account-safety and admission blockers
  are distinct, and the preflight-block message text names the blocker. No
  failure is hidden.
- `minimum_closure_condition`: an operator workflow would have to branch on
  blocker phase alone to separate preflight-block from capture-failure.
- `next_authorized_action`: none required; note only.

## Considered-and-defended hypotheses (probed, no defect)

- One-page/final-video claim is receipt prose only. Defeated: page reuse is real
  in `_get_or_create_page`; navigation is direct-URL sequence in the loop; the
  engine-conditional contract fields degrade to neutral off the session engine.
- Direct navigation could open new pages, return to grid, or reorder videos.
  Defeated: the loop only navigates the ordered `selected_urls`; no
  `new_page`/grid call between videos; selection order is pinned by test.
- Account-risk warning could be treated as a clearable CAPTCHA and continue.
  Defeated: account-safety and CAPTCHA marker sets are disjoint; pre-action stop
  is evaluated before the handoff; `_challenge_kind_from_text` classifies
  account_risk before slider/captcha.
- Account_safety_stop could be True yet status complete (skipping the raise).
  Defeated: an account-safety failure lands in `failures` and `break`s before
  completion, so `completed_count < len(selected)` forces `partial_failure`,
  which is the branch that raises.
- Close could kill the operator Chrome. Defeated: `connect_over_cdp`
  `browser.close()` disconnects; class docstring and lifecycle receipt affirm
  detach-only; owned-engine `finally` only detaches.
- A finally-block close error could mask/alter the account-safety exception.
  Defeated: `close()` errors are captured into `close_error` (not raised) while
  the original exception propagates; the post-finally `raise` for `close_error`
  is unreachable when the account-safety exception is in flight.
- Progress emission could raise and break capture. Considered: fields passed are
  ints/strings (JSON-serializable) and `_notify_progress` is a no-op when
  `progress_fn` is None; the CLI emitter is a flushed print. Wrapping it in
  try/except would risk hiding real stdout failure, so no change is warranted.
- Runbook direct-command could hide a necessary preflight or weaken a gate.
  Defeated: the runner owns the preflight and still fails loud on a blocker;
  the alias check is correctly demoted to a diagnostic, not removed.
- Auth-root correction and progress work could conflict. Defeated: independent
  code paths; both default to `default_session_profile_auth_state_root()`.
- API/test compatibility for custom engines / deep-capture functions. Defeated:
  new parameters (`progress_fn`, `pre_action_stop_markers`,
  `session_engine_reused`, `account_safety_pre_action_circuit_breaker`) all have
  safe defaults; engine introspection uses `getattr`/`isinstance` guards.

## Patch

No patch. No confirmed defect reached the patch threshold, so the working tree
is left clean and unchanged. `git diff --stat origin/main...HEAD` remains the
ten-file authored diff; `git status --porcelain` is empty.

## Validation evidence (observed)

Run from `C:\tmp\forseti-persistent-onboarding-review` with
`PYTHONDONTWRITEBYTECODE=1`.

```powershell
python -m pytest -p no:cacheprovider -q tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_source_capture_chrome_cdp_session.py tests/unit/test_tiktok_blocker_triage.py tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py tests/contract
```

- Result: exit code 0. 271 test items collected and all passed (progress reached
  100% with 271 passing dots; zero failures, zero errors). Includes the
  read-only `tests/unit/test_tiktok_blocker_triage.py` and `tests/contract`.

```powershell
python .agents/hooks/check_review_routing.py --strict
```

- Result: `check_review_routing --strict: OK (base: origin/main)`, exit code 0.

```powershell
git diff --check
```

- Result: no output, exit code 0 (no whitespace errors; tree clean).

`git status --porcelain=v1` after all steps: empty (no stray edits introduced by
the review).

## Verdict

Reviewer verdict: the combined persistent-onboarding navigation, progress,
account-safety circuit-breaker, engine-lifecycle-neutrality, and auth-root
alignment diff is correct and truthfully contracted against the commission
fitness contract, with no confirmed defect in the ten named files. All three
commissioned validation gates pass. Three informational observations are logged
as decision input; none is patch-eligible under the commission bar. This is a
delegated reviewer verdict for Chief Architect adjudication, not approval,
validation, readiness, or acceptance.

## Residual risks

- Behavior verified by source reasoning and the existing unit/contract suite
  only; no live TikTok, OAuth, CAPTCHA, browser, or data-lake path was exercised
  (out of scope by commission). The exact Playwright `connect_over_cdp` detach
  semantics are relied upon from documented behavior, not exercised here.
- INFO-1/INFO-2/INFO-3 are latent-fragility or granularity notes, not current
  faults; they are bounded and below the patch threshold.
- The read-only collaborator `blocker_triage.py` carries the account-safety
  classification; it is outside the patch scope and was confirmed, not modified.
  A future change to its `challenge_kind` vocabulary would need the
  `_blocker_triage_receipt` account-safety set kept in sync.

## Courier block

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: docs/prompts/reviews/tiktok_persistent_onboarding_navigation_progress_delegated_adversarial_code_review_patch_prompt_v0.md (authoritative copy), delegated_code_review_and_patch, access repo.
- target: branch codex/review-tiktok-persistent-onboarding, head 3cd83e63f6da22bc109d1f817a16802122cb4bbc, base dae46bbe, range origin/main...HEAD; ten named files; all ten pinned blob IDs verified; clean tree.
- reviewed files: source_capture_agent_runbook.md; run_source_capture_chrome_cdp_session.py; run_source_capture_tiktok_creator_onboarding.py; adapters/browser_snapshot.py; tiktok/creator_onboarding.py; tiktok/live_batch_probe.py; and the four paired unit test files.
- findings: no confirmed correctness defect. INFO-1 handoff-suppression flag over-attribution in a rare mixed sequence (receipt-cosmetic, test-only consumer). INFO-2 account-safety magic-string sentinel coupling (works, test-pinned). INFO-3 shared preflight/capture blocker code+phase (honest name, minor granularity).
- proposed patch: none; no finding reached the confirmed-defect patch bar; working tree left clean.
- citations: file:line anchors in the fitness-contract adjudication and findings sections above; classification in blocker_triage.py; disjoint marker sets in live_batch_probe.py:147-158; CDP detach in browser_snapshot.py:1739-1750.
- reviewer verdict: correct and truthfully contracted; delegated decision input only.
- validation: pytest exit 0 (271 passed, 0 failed) over the commissioned files; check_review_routing --strict OK exit 0; git diff --check exit 0; git status clean. Not run: any live browser/TikTok/OAuth/CAPTCHA/data-lake path (out of scope).
- residual risk: verified by source + existing tests only; Playwright detach relied on documented semantics; INFO items are bounded latent notes; blocker_triage.py is read-only and must stay in sync with the account-safety receipt set.
- blockers / off-scope / not-proven: no blockers. Off-scope: any source-changing edit outside the ten files, and all lifecycle actions (commit/push/merge/PR). Not proven: live runtime behavior.

Adjudicator next step: adjudicate these findings, the clean-tree no-patch
disposition, verdict, and residuals as claims under
.agents/workflow-overlay/communication-style.md -> Review Adjudication Next
Step; close any self-closable item in the same turn; then batch admin/lifecycle
follow-ups into one land step and deep-think only the material next moves.
```
