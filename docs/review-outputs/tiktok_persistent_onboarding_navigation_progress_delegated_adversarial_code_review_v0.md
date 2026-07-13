# TikTok persistent onboarding navigation & progress — delegated adversarial code review

```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code review output (delegated_code_review_and_patch)
scope: >
  Cross-vendor adversarial review of the codex/review-tiktok-persistent-onboarding
  diff (origin/main...ccc77aaa): retained one-page Chrome CDP onboarding
  navigation, flushed progress/blocker events, capture-contract navigation keys,
  and Chrome auth-state-root alignment.
use_when:
  - Chief Architect adjudicates whether to keep/merge the reviewed diff.
authority_boundary: retrieval_only
```

## Provenance

```text
reviewed_by: Anthropic Claude (Opus) — cross-vendor discovery controller, repo access
authored_by: OpenAI Codex / GPT-5 lineage (branch codex/…, commit author Eric)
target_worktree: C:\tmp\forseti-persistent-onboarding-review
target_branch:   codex/review-tiktok-persistent-onboarding
target_revision: ccc77aaa28cb7a6494de45dc2f7dfa4773ceb61f  (HEAD, clean tree)
base_merge_point: dae46bbe8b98d6c3967648491da15244bd26fea5  (ancestor of HEAD: yes)
origin/main:     ff171a33bee8bb8c62800a2bea176db36a67faf8
source_range:    origin/main...HEAD  (8 files, +129 / -2)
access_mode:     repo
patch_authority: confirmed defects only, inside the eight named files, uncommitted
```

De-correlation: author vendor (OpenAI/Codex lineage) differs from reviewer vendor
(Anthropic), satisfying the cross-vendor discovery bar in
`.agents/workflow-overlay/delegated-review-patch.md`.

Committed Git blob IDs verified with `git rev-parse ccc77aaa:<path>` — all eight
match the commission manifest:

```text
3908ddc1f26c1535cceed886bb03532cd5246b10  forseti-harness/docs/source_capture_agent_runbook.md
04d0f06b6608afb1538b11614c2a21a4f0f045e9  forseti-harness/runners/run_source_capture_chrome_cdp_session.py
a7e66213f8d8d92b33c26bb7562bbcbce63fe416  forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py
5c223f8c71fde27bc49c63dc8544369e3fc0e4b4  forseti-harness/source_capture/tiktok/creator_onboarding.py
5f409f1b84441d50fd8bddada898805f3637fec2  forseti-harness/source_capture/tiktok/live_batch_probe.py
dc268bcea4581a1e39887c5e34134dca8d33ba47  forseti-harness/tests/unit/test_source_capture_chrome_cdp_session.py
683085b73fc371fefbabd531aa9c3d6bcb28ee9a  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
5f662e859ad7c75e0ef954f631274a2ef0d9ab84  forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
```

## Source-readiness

`SOURCE_CONTEXT_READY`. Read before strict claims: `AGENTS.md`,
`.agents/workflow-overlay/README.md`,
`.agents/workflow-overlay/delegated-review-patch.md`, the complete
`origin/main...HEAD` diff, and all eight named files, plus the out-of-patch-scope
substrate needed to verify the behavioral claims (`ChromeCdpPageObservationSessionEngine`
and `fetch_browser_page_observation_capture` in
`source_capture/adapters/browser_snapshot.py`). `workflow-deep-thinking` was
applied before `workflow-code-review`.

## Review-use boundary

These findings are decision input for Chief Architect adjudication only; they are
not approval, not validation, not mandatory remediation, and not executor-ready
patch authority. The verdict and severities below are claims to adjudicate, not a
formal review-lane status.

## Findings (ordered by severity)

### F1 — LOW / advisory. Two capture-contract navigation keys are backend-agnostic constants that are only strictly accurate for the Chrome-CDP session-engine path.

`live_batch_probe.py::_capture_contract` now emits, unconditionally:

```text
video_navigation_mode:          direct_selected_url_sequence
video_page_reuse_policy:        one_page_sequential_navigation
terminal_page_policy:           leave_last_selected_video_open
pointer_movement_policy:        meaningful_page_actions_only
address_bar_simulation:         false
referrer_spoofing:              false
return_to_grid_between_videos:  false
```

For the enforced onboarding path these are all truthful (see verification below).
Two of the seven, however, are stated as policy constants while the behavior they
name is backend-dependent:

- `video_page_reuse_policy: one_page_sequential_navigation` is true only when a
  session engine is used (Chrome-CDP or the CloakBrowser session engine, both of
  which reuse one runner page). For the default Playwright backend with
  `engine=None`, `fetch_browser_page_observation_capture` builds a fresh
  `_PlaywrightBrowserSnapshotEngine` per call (`browser_snapshot.py:517-523`), so
  each video gets its own browser/page — no page reuse.
- `terminal_page_policy: leave_last_selected_video_open` is true only for
  Chrome-CDP, whose `close()` disconnects a `connect_over_cdp` session and leaves
  the operator browser and last page open (`browser_snapshot.py:1665-1676`,
  `close_policy: detach_only_leave_browser_and_page_open`). The CloakBrowser
  session engine's `close()` closes context and browser
  (`browser_snapshot.py:1780-1789`), and the default backend closes per-video, so
  neither leaves the last video open.

Failure scenario: a direct caller of `run_tiktok_live_batch_probe` on the
`cloakbrowser` or default backend receives a `capture_contract` asserting
`leave_last_selected_video_open` / `one_page_sequential_navigation` that does not
describe that run.

Why not patched: the onboarding feature — the bound outcome — enforces
`chrome_cdp` (`creator_onboarding.py:192-193`) and requires an explicit session
engine (`browser_snapshot.py:503-508`), so every key is accurate on the path this
diff exists to serve. Making the two keys backend-conditional would require
threading engine/close-policy state into `_capture_contract` (which today receives
neither), plus updating the asserting test — i.e. broadening the contract shape
and touching live-capture-policy surface, which the commission explicitly scopes
out ("Do not broaden the architecture or alter live-capture policy"). Recommended
disposition: keep as-is, or (owner's call) tighten the two keys' wording to name
the session-engine precondition in a follow-up. Adjudicator decision, not a
blocker.

## Considered-and-defended hypotheses (probed, not defects)

- **One-page / final-video policy vs. real engine semantics (focus #1) — MATCHES
  for the enforced path.** The CDP engine reuses `self._real_page` across
  observations (`_get_or_create_page`, `browser_snapshot.py:1637-1647`;
  `page_reuse_policy: reuse_one_runner_page_until_detached`). The onboarding shares
  one engine across suggested → grid → each video, so the whole run is one tab.
  `close()` calls `browser.close()` on a `connect_over_cdp` connection, which
  detaches without terminating operator Chrome and without navigating away. The
  runbook's "operator Chrome remains open on the final selected video" is backed by
  engine code, not receipt prose alone.
- **Direct navigation opening new pages / returning to grid / reordering (focus
  #2) — no.** Each selected video is fetched by its own validated URL in selection
  order (`live_batch_probe.py:442-483`); between videos there is only a cadence
  sleep, and nothing navigates back to grid in or after the loop
  (`live_batch_probe.py:752-775`). Selection order is preserved
  (`creator_onboarding.py:322-336`). URLs are handle/id-validated
  (`_normalize_video_url`, `_is_creator_video_url`).
- **Progress events mislabeled / late / buffered / secret-bearing / capable of
  breaking capture (focus #3).** Events are `print(..., flush=True)` with sorted
  JSON under distinct prefixes (`PROGRESS_`/`BLOCKER_`/`SUMMARY_`), so they are
  flushed, machine-readable, and unbuffered. Payload fields (creator_handle,
  session_profile alias, window/selection/completed counts, status) are public,
  not secrets. They CAN raise (no guard in `_notify_progress`), but a raise
  propagates as a loud stage failure → the runner emits a blocker and exits
  non-zero; it never fabricates success. Guarding emission would risk swallowing a
  genuine `BrokenPipeError`, so leaving it loud is consistent with the
  failure-visibility rule. Not a defect.
- **Runbook direct-command hides a preflight or weakens a gate (focus #4) — no.**
  The runner genuinely owns the Creator Registry preflight
  (`run_source_capture_tiktok_creator_onboarding.py:132-141`, blocks on
  non-`allowed`) and session-alias resolution (`:144-151`) before any capture, and
  emits a blocker on failure. The runbook keeps the standalone alias check as a
  blocker-diagnostic, not a required preamble — an accurate description; the gate
  moved into the runner (fail-loud), it was not removed.
- **Blocker codes preserve failure visibility (focus #5) — yes.** Codes are coarse
  (`ONBOARDING_PRECHECK_OR_CAPTURE_FAILED`, `ONBOARDING_UNEXPECTED_FAILURE`,
  `ADMISSION_FAILED`) but the detailed exception text still reaches stderr via
  `parser.exit(message=...)`, and the failure receipt records `terminal_stage` and
  `error_or_none`. No success summary is printed on any failure path.
- **Auth-root correction composes with the progress work (focus #6) — yes.** The
  CDP-bootstrap runner now defaults `auth_state_root or
  default_session_profile_auth_state_root()`
  (`run_source_capture_chrome_cdp_session.py:53-55`), matching the default the
  onboarding runner already used (`:142`) and the root threaded into
  `validate_auth_state_provenance_requirement` and the deep-capture call. The two
  entry points resolve the same logical root; the changes are independent and do
  not interfere.
- **API/test compatibility for custom engines or deep-capture functions (focus
  #7) — preserved.** `progress_fn` is a new keyword-only parameter defaulting to
  `None` on `run_tiktok_creator_onboarding`; it is not forwarded to
  `deep_capture_fn`, so custom deep-capture callables and custom-engine callers are
  unaffected. `deep_capture_fn`'s call signature is unchanged.
- **`_emit_progress` before the `try` block (runner:124-130).** If `print` raised
  there it would be uncaught, but that is before any capture side effect and
  `print` to an operator TTY does not realistically raise; negligible.
- **Dead `return 2` / `return 3` after `parser.exit(...)`.** Unreachable
  (`parser.exit` raises `SystemExit`), but pre-existing and untouched in substance
  by this diff; out of scope.

## Patch

None. No confirmed defect met the "patch only confirmed defects with practical
regression proof" bar. The single finding (F1) is a low-severity truthfulness
precision on a non-enforced code path whose fix would broaden the contract shape
the commission scoped out. The target worktree carries no review edits.

## Validation evidence (observed)

Run in `C:\tmp\forseti-persistent-onboarding-review` with `PYTHONDONTWRITEBYTECODE=1`:

```text
python -m pytest -p no:cacheprovider -q \
  tests/unit/test_source_capture_chrome_cdp_session.py \
  tests/unit/test_tiktok_creator_onboarding.py \
  tests/unit/test_tiktok_live_batch_probe.py \
  tests/contract
  -> 191 passed, exit 0

python .agents/hooks/check_review_routing.py --strict
  -> check_review_routing --strict: OK (base: origin/main), exit 0

git diff --check
  -> no output, exit 0   (working tree clean; no patch applied)
```

## Verdict

No confirmed defect requiring a patch. The reviewed diff is correct and its
navigation/close contract is truthful for the enforced Chrome-CDP persistent
onboarding path: one reused runner page, direct selected-URL sequence in selection
order, no grid return, CDP detach leaving the operator browser and final video
open, flushed non-secret progress/blocker events, preserved failure visibility, an
auth-root default aligned with session-profile resolution, and backward-compatible
public signatures. All bound tests and gates pass. One low-severity advisory (F1)
is offered for the Chief Architect to keep or refine. This is decision input, not a
formal `PASS`, readiness, or acceptance.

## Residual risks

- F1 leaves two `capture_contract` keys generous for non-CDP direct callers; bounded
  and below the onboarding feature's assurance need, but a latent
  truthful-contract snag if those keys are later relied on off the CDP path.
- Review scope is the eight named files at `ccc77aaa`; the browser adapter and the
  broader capture stack were read for verification but not audited.
- Progress emission is deliberately allowed to fail loud; a consumer that closes
  stdout mid-run will surface an emission error rather than a clean blocker line —
  acceptable under failure-visibility, noted for completeness.

## Courier block

```text
COMMISSION: TikTok persistent onboarding navigation & progress — delegated adversarial code review-and-patch
CONTROLLER: Anthropic Claude Opus (cross-vendor vs OpenAI/Codex author; repo mode)
TARGET: C:\tmp\forseti-persistent-onboarding-review | codex/review-tiktok-persistent-onboarding | ccc77aaa (clean; 8/8 blob IDs verified; ancestor of base dae46bbe)
RESULT: PASS (advisory). No confirmed defect; no patch applied; tree left clean.
CORE CLAIMS VERIFIED (Chrome-CDP path): one reused runner page; direct selected-URL sequence in order; no grid return; CDP detach leaves operator Chrome + final video open; flushed non-secret progress/blocker events; failure visibility intact; auth-root default aligned; public signatures backward-compatible.
FINDING F1 (LOW): capture_contract emits video_page_reuse_policy / terminal_page_policy as constants; strictly accurate only for the CDP session-engine path (default & cloakbrowser backends close). Not patched — enforced path is truthful; fix would broaden contract shape the commission scoped out. Keep-or-refine is CA's call.
VALIDATION: pytest 191 passed (exit 0); check_review_routing --strict OK (exit 0); git diff --check clean (exit 0).
ARTIFACT: docs/review-outputs/tiktok_persistent_onboarding_navigation_progress_delegated_adversarial_code_review_v0.md (uncommitted, in target worktree).
ADJUDICATION: run communication-style.md -> Review Adjudication Next Step. F1 is self-closable (keep as-is, or a bounded 2-key wording tighten in live_batch_probe.py + its asserting test). Then batch any lifecycle follow-ups into one land step; deep-think material next moves only if a visible active goal exists, else record no_visible_active_goal.
```
