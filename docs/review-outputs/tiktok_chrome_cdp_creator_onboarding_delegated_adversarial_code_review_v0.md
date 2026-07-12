# TikTok Chrome-CDP Creator Onboarding Delegated Adversarial Code Review-and-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial code review-and-patch result)
scope: >
  De-correlated cross-vendor controller review of PR #897's retained
  Chrome/CDP TikTok onboarding changes (commits ac0ff8a2, 3a9dbf60) on
  codex/tiktok-account-safety, bounded to the 15 named target files.
use_when:
  - Adjudicating whether the Chrome-CDP TikTok onboarding change is safe to land.
  - Checking whether the chrome_cdp browser backend fails loudly or silently
    substitutes a disposable browser when misconfigured.
authority_boundary: retrieval_only
reviewed_by: claude-sonnet-5
authored_by: openai-codex-gpt-5 (commission-declared author_vendor_family; exact
  version string not independently observable from repo evidence)
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
```

## 1. Commission, Preflight, De-Correlation, And Hash Evidence

- **Commission source (run-authoritative):**
  `C:\Users\vmon7\Desktop\projects\orca\docs\_inbox\tiktok_chrome_cdp_creator_onboarding_delegated_adversarial_code_review_patch_prompt_v0.md`.
- **Target worktree:** `C:\tmp\forseti-tiktok-account-safety`. **Branch:**
  `codex/tiktok-account-safety`. **HEAD (observed via `git rev-parse HEAD` /
  `git branch --show-current`):** `3a9dbf602bf99252fc6c6bfa8fffb1eeb59c99f2`,
  matching `review_target_commit`. **Dirty state:** clean at start
  (`git status --porcelain=v1 -uall` empty, confirmed by the calling session
  and re-observed by this reviewer before any edit).
- **Commit messages (observed via `git show -s`):**
  - `ac0ff8a2` "fix(tiktok): retain onboarding browser profile" —
    `review_routing_status: blocked -- different-vendor delegated review
    unavailable in this runtime`.
  - `3a9dbf60` "fix(tiktok): attach onboarding to persistent Chrome" — same
    `review_routing_status: blocked` line.
  - This commission and this review are the requested closure of that blocked
    disposition.
- **De-correlation bar.** Author vendor family per commission: OpenAI /
  Codex / GPT-5. Reviewing model (this actor): **Claude (Anthropic),
  claude-sonnet-5** — a different upstream model vendor/lineage than the
  author. `de_correlation_bar: cross_vendor_discovery` is satisfied; this is
  not a same-vendor sanity pass and not a self-review.
- **Hash evidence.** All 15 pinned SHA-256 values in the commission were
  independently recomputed by this reviewer (`sha256sum` over each pinned
  path in the checked-out worktree, before any edit) and matched the
  commission's pins byte-for-byte, e.g.:
  `d4bdb48a2ecf8f116609bc2c0b32f8beb42a6b20ace1cf06b34c9f32d0a2e2a4
  runners/run_source_capture_chrome_cdp_session.py` through
  `4730b184e78c15c9d32fab247d74984ce4090ac0faeae9fab329bde16f3a958e
  tests/unit/test_tiktok_live_batch_probe.py`. All 15/15 matched; no
  mismatch; the strict-review block condition does not apply. (Note: a
  same-path `git show <commit>:<path> | sha256sum` produces a *different*
  hash than the on-disk file for every one of these files — this is a
  CRLF/LF checkout-normalization artifact of this Windows worktree, not a
  content discrepancy; the pins were computed against on-disk CRLF bytes, and
  the direct on-disk `sha256sum` is the correct comparison, which is what was
  used.)
- **Loading sequence followed:** `AGENTS.md` read in full; overlay
  `README.md`, `source-loading.md`, `decision-routing.md`, `review-lanes.md`,
  `delegated-review-patch.md`, `prompt-orchestration.md`, `safety-rules.md`,
  `validation-gates.md` read in full. `workflow-deep-thinking` and
  `workflow-code-review` skills were `REFERENCE-LOAD`ed (invoked for their
  procedural instructions only) before any source-heavy reading or finding
  formation.

## 2. Source Context Status

**`SOURCE_CONTEXT_READY`.**

Source-read ledger:

- All 15 pinned files read in full (line counts 98–3120): both runners,
  `browser_snapshot.py`, `browser_user_data.py`, `session_profiles.py`,
  `source_access_provenance.py`, `blocker_triage.py`, `creator_onboarding.py`,
  `live_batch_probe.py`, and their six paired unit test files.
- Complete diff `origin/main...3a9dbf602bf99252fc6c6bfa8fffb1eeb59c99f2`
  (1383 lines) read in full via `git diff` from the target worktree; matches
  the 15-file stat in the commission.
- Commits `ac0ff8a2` and `3a9dbf60`: messages and stat read via `git show`.
- Installed `playwright` (1.60.0) and `cloakbrowser` (0.4.7) inspected
  directly from the Python environment (`site-packages`) to settle two
  lifecycle/input questions the diff cannot answer by itself:
  - `playwright.sync_api.Browser.close()` docstring: "In case this browser is
    connected to, clears all created contexts belonging to this browser and
    disconnects from the browser server" (does not terminate the underlying
    OS process for a `connect_over_cdp` handle).
  - `cloakbrowser.human.patch_context()` / `resolve_config("careful", None)`:
    `patch_context` monkeypatches the *real* context's `new_page` so any
    page later created through it is auto-humanized with the `careful`
    preset; `_careful_config()` is a concrete, slower/more-deliberate timing
    profile, applied once per context.
- Repo-wide grep (not diff-scoped) for `CloakBrowserPersistentPageObservationSessionEngine`
  and for `browser_backend="chrome_cdp"` call sites, to establish real
  production reachability rather than diff-local reasoning.
- Also read (context, not part of the 15-file patch scope, read-only):
  `runners/run_source_capture_tiktok_live_batch_probe.py` (existing runner,
  unchanged by this diff, but the caller that makes Finding F1 concretely
  reachable via `--session-profile` + `--allow-diagnostic-browser-backend`).

No source gap blocked a finding. No conflict found between the fitness
contract and the pinned files' behavior beyond what is reported below.

## 3. Findings (Ordered By Severity)

### F1 [blocker] [confidence: high] — `chrome_cdp` backend silently falls back to a disposable launched browser when no engine is supplied

- **target:** `[browser-snapshot-dispatch]`.
- **location:** `forseti-harness/source_capture/adapters/browser_snapshot.py`,
  `fetch_browser_page_observation_capture` dispatch (pre-patch: the
  `if engine is not None / elif cloakbrowser / else` chain immediately before
  the `try:` block, ~line 501–517 of the pinned file).
- **issue:** `chrome_cdp` was added to `ALLOWED_BROWSER_BACKENDS` (and
  therefore passes `_normalize_browser_backend`'s validation), but the engine
  **auto-construction dispatch** only had two branches: an explicit `engine`,
  or `cloakbrowser` (auto-constructs `_CloakBrowserPageObservationEngine`).
  Every other backend value — including the new `chrome_cdp` — fell into the
  final `else`, which auto-constructs a plain `_PlaywrightBrowserSnapshotEngine`
  (`playwright.chromium.launch(...)`, i.e. a fresh, disposable, non-CDP
  browser). So `fetch_browser_page_observation_capture(browser_backend="chrome_cdp",
  engine=None)` never attaches to the operator's Chrome at all: it silently
  launches and discards an ordinary throwaway Chromium instance instead.
- **evidence / reachability:** `run_tiktok_live_batch_probe` in
  `live_batch_probe.py` only self-constructs an engine for the `cloakbrowser`
  branch (`if engine is None and normalized_browser_backend ==
  TIKTOK_BROWSER_BACKEND_CLOAKBROWSER: ...`); for `chrome_cdp` with no
  `engine` it falls through to `fetch_browser_page_observation_capture(...,
  browser_backend="chrome_cdp", engine=None)` and hits the bug above. The
  onboarding path (`creator_onboarding.py`) always constructs and passes an
  explicit `engine=ChromeCdpPageObservationSessionEngine(...)`, so it is not
  itself exposed — but the pre-existing, unchanged runner
  `runners/run_source_capture_tiktok_live_batch_probe.py` calls
  `write_tiktok_live_batch_probe_outputs` without ever passing `engine=`, and
  its `--session-profile` path now legitimately resolves
  `browser_backend="chrome_cdp"` (this PR's own `session_profiles.py` change
  allows that value). That runner requires only
  `--allow-diagnostic-browser-backend` (already required for any non-cloakbrowser
  backend) to reach the silent-fallback path with a real, resolved
  `chrome_cdp` session profile.
- **impact:** directly violates fitness contract #1 ("no disposable relaunch
  per capture"), #4 (CDP loopback attach — bypassed, never attempted), and
  #12 ("fails loudly" — instead it fails silently by substituting the wrong
  backend with no error, warning, or receipt difference visible to the
  caller before capture starts).
- **minimum_closure_condition:** `browser_backend="chrome_cdp"` with no
  explicit `engine` must raise a clear, loud error instead of constructing
  any engine.
- **next_authorized_action:** patch (blocker; inside patch scope,
  `browser_snapshot.py` is a pinned file).
- **patched:** yes — see §5.

### F2 [major] [confidence: high] — unused duplicate persistent-Cloak engine surface (`CloakBrowserPersistentPageObservationSessionEngine`)

- **target:** `[browser-snapshot-engines]`.
- **location:** `forseti-harness/source_capture/adapters/browser_snapshot.py`
  (class, pre-patch ~122 lines) and its sole consumer,
  `tests/unit/test_source_capture_browser_snapshot.py::test_persistent_session_engine_reuses_retained_profile_and_existing_page`.
- **issue:** this class — added in the first commit (`ac0ff8a2`) as the
  original "retain the browser profile" approach — reuses one retained
  **CloakBrowser** profile via `cloakbrowser.launch_persistent_context(...)`.
  The second commit (`3a9dbf60`) superseded it with a materially different
  strategy: `ChromeCdpPageObservationSessionEngine`, which **attaches** to an
  operator-already-launched Chrome via `connect_over_cdp` instead of
  launching a CloakBrowser-managed persistent profile. Every production call
  site (`creator_onboarding.py`, both runners, `live_batch_probe.py`) was
  updated to require/construct `ChromeCdpPageObservationSessionEngine`
  (`TIKTOK_BROWSER_BACKEND_CHROME_CDP` checks). A repo-wide grep (not just
  the diff) confirms `CloakBrowserPersistentPageObservationSessionEngine` has
  **zero production callers** — its only reference anywhere in the repo was
  its own dedicated unit test.
- **impact:** exactly the adversarial angle the commission names by name
  ("unused duplicate persistent-Cloak engine surface"). Live, unreachable,
  untriggerable-from-any-CLI code that duplicates the "retained profile"
  concept via a different browser-attachment strategy is a drift and trust
  hazard: it still claims `"humanized_input_preset": "careful"` and
  `"persistent_profile_loaded"` in its own `lifecycle_receipt`, so a future
  reader (human or agent) could reasonably believe it is the shipped
  mechanism, wire it in, and get an untested, never-production-exercised
  code path for a TikTok-account-safety-relevant surface.
- **minimum_closure_condition:** either remove the dead class (and its
  test), or wire it into a real, tested call site with an explicit rationale
  for keeping two competing persistence strategies.
- **next_authorized_action:** patch (major; safe mechanical removal, zero
  callers confirmed by repo-wide grep, not just diff-local reasoning).
- **patched:** yes — see §5.

### F3 [major] [confidence: medium] — no binding between the resolved profile label and the Chrome process actually attached via CDP

- **target:** `[chrome-cdp-attach]`.
- **location:** `creator_onboarding.py:222-234` (checks `user_data_dir`
  exists and is non-empty) and
  `browser_snapshot.py::ChromeCdpPageObservationSessionEngine._launch_page_observation_browser`
  (connects to `cdp_endpoint`, default `http://127.0.0.1:9222`, and simply
  takes `browser.contexts[0]`).
- **issue:** the code verifies that the *labeled profile directory* exists
  and is non-empty, and separately connects to whatever Chrome is listening
  on the configured CDP port — but nothing binds the two together. Any
  Chrome (or other CDP-debuggable Chromium) currently listening on that port
  is accepted, regardless of which `--user-data-dir` it was actually
  launched with. If an operator has a stray debug Chrome on the same
  well-known port, or runs two profiles/aliases against the same default
  port, the harness would silently attach to the wrong browser/profile/account.
- **impact:** this is precisely the "wrong Chrome/profile/port attachment"
  risk named in the adversarial questions. It does not, by itself, produce a
  false success or violate the account-risk/CAPTCHA contracts (those still
  apply to whatever page is actually observed), but it means the *identity*
  of the attached session is unverified.
- **minimum_closure_condition:** the running Chrome's identity/profile is
  cross-checked against the expected label before capture begins (e.g. via a
  per-label distinct CDP port convention, or reading and comparing
  attach-time metadata), and a mismatch fails closed.
- **next_authorized_action:** owner decision / architecture-level — closing
  this well requires new capability (CDP/process-level profile
  introspection is not exposed by Playwright's `connect_over_cdp`), which is
  outside a bounded line-level patch. Not `NEEDS_ARCHITECTURE_PASS` for the
  whole review (the rest of the diff is soundly patchable), but this
  specific residual should route to an owner/architecture decision if closure
  is wanted.
- **patched:** no (architecture-level; not manufactured into a cosmetic
  patch).

### F4 [minor] [confidence: medium] — pre-action human-challenge-handoff gate is narrower than the post-capture account-risk/auth-wall triage

- **target:** `[tiktok-challenge-handoff]`.
- **location:** `live_batch_probe.py` `TIKTOK_CHALLENGE_TEXT_MARKERS` (`"drag
  the slider", "verify to continue", "captcha", "security check"`) versus
  `blocker_triage.py` `_CHALLENGE_MARKERS` (superset, adds `"your account
  might be at risk"`, `"account might be at risk"`, `"log in to comment"`
  in this PR).
- **issue:** the operator-handoff pause that suppresses scripted pointer
  actions (`maybe_run_handoff` in `browser_snapshot.py`) only triggers on the
  narrower marker set. A page showing the new account-risk/logged-out-wall
  text (but not one of the four original markers) will not pause for the
  operator before scripted retry/dismiss/open-comments pointer actions run.
- **impact:** does **not** allow a success, empty-capture, or
  cleared-CAPTCHA outcome for account-risk — `classify_tiktok_capture` runs
  again on the final captured text after pointer actions, using the full
  marker set, and forces a hard `break` + failure entry
  (`blocker_triage.action == TIKTOK_BLOCKER_ACTION_STOP`). So fitness
  contract #9 is satisfied at the **outcome** level. The residual is
  narrower: a handful of benign scripted UI actions (retry/dismiss/open
  comments) may fire against a page already showing an account-risk banner
  before the stop is registered.
- **minimum_closure_condition:** either accept this as within tolerance (the
  outcome contract already holds), or widen
  `human_challenge_handoff_markers` for the pre-action gate to match the
  full account-risk/auth-wall marker set (a behavior change with its own
  tradeoffs — e.g. "log in to comment" also appears on ordinary logged-out
  video pages, which would newly pause all such pages for operator handoff).
- **next_authorized_action:** advisory / owner decision; not required for
  this bounded patch pass.
- **patched:** no (outcome-level contract already holds; widening the gate
  is a behavior-shape decision, not a confirmed defect).

### F5 [minor] [confidence: high] — `run_tiktok_creator_onboarding`'s final `close_error` raise is unreachable when the try block already failed

- **target:** `[creator-onboarding-lifecycle]`.
- **location:** `creator_onboarding.py:370-421`.
- **issue:** when the `try` block itself raises (e.g. "one or more selected
  video deep captures did not complete") **and** `close()` in the `finally`
  block also raises, the combined text is written into the durable receipt's
  `error_or_none` field, but Python re-raises the **original** exception once
  `finally` completes — not a new exception mentioning the close failure.
  The explicit trailing `if close_error is not None: raise
  TikTokCreatorOnboardingError(f"browser session close failed: ...")` is
  therefore only reachable on the "onboarding succeeded, then close() failed"
  path.
- **impact:** no silent-success risk — an exception always propagates, and
  the close failure is always visible in the durable receipt either way —
  but the exception message a caller sees can omit a real close failure when
  both failures occur together, which is a minor observability gap, not a
  correctness or safety defect.
- **minimum_closure_condition:** if desired, chain/append the close-failure
  detail onto whatever exception is actually re-raised in every path (not
  only the success-then-close-fails path).
- **next_authorized_action:** optional hardening; not required.
- **patched:** no (receipt already records the truth; no silent success;
  optional hardening only).

## 4. Considered And Defended

- **Considered:** `Browser.close()` on a `connect_over_cdp` handle might
  close the operator's real Chrome process or its pre-existing tabs/contexts,
  defeating "operator Chrome resources stay open on success and failure"
  (contract #5). **Defended:** Playwright's own documentation for a
  connected (not launched) browser states `close()` "clears all created
  contexts belonging to this browser and disconnects from the browser
  server" — it does not terminate the underlying OS process. The code
  deliberately reuses the pre-existing `contexts[0]` (never a
  Playwright-created context) and never calls `.close()` on it directly
  (`_SessionContextProxy.close()` only detaches per-capture listeners/routes,
  matching `lifecycle_receipt["close_policy"] ==
  "detach_only_leave_browser_and_page_open"`). Not exercised against a real
  Chrome process in this review (no live browser operations were run, per
  commission boundary), so this remains source-read-verified, not
  empirically verified.
- **Considered:** `_capture_contract()`'s `"cookies_or_tokens_persisted":
  False` field might be a false truthful-receipt claim for `chrome_cdp` runs,
  since the whole point of a retained profile is persisted cookies.
  **Defended:** this field (and its siblings
  `raw_comment_response_bodies_persisted`, `raw_endpoint_urls_persisted`,
  etc.) describes what the probe's own JSON *staging output* embeds, not
  what the browser's on-disk profile retains — `assert_no_sensitive_tiktok_material`
  enforces exactly that narrower claim — and this logic predates this PR
  (untouched by the diff), so it is also out of the bounded patch scope
  regardless.
- **Considered:** the new `random_seed: int | None = None` default
  (`random.SystemRandom()` when unset) could regress prior deterministic
  behavior for callers that relied on an implicit fixed seed. **Defended:**
  every CLI entry point already exposed `--random-seed` as an optional,
  no-default argument before this PR; the change makes the "no silent fixed
  seed in normal runs" property explicit and test-covered rather than
  altering any previously-relied-upon default.
- **Considered:** the `browser_user_data.py` default-root change
  (`%LOCALAPPDATA%\Forseti\_browser_user_data` instead of a path relative to
  the harness source tree) could silently orphan or duplicate profiles
  across worktrees. **Defended:** this is the PR's explicit, tested fix for
  exactly that problem (`test_default_browser_user_data_root_is_stable_across_worktrees`),
  and `FORSETI_BROWSER_USER_DATA_ROOT` remains an explicit override; no
  defect found here.

## 5. Patch Scope And Diff

Patch authority used: 2 of the 15 pinned files, both closing a named finding
above (F1, F2). No other file touched; no doctrine, contract, profile, auth
state, or generated/hash-pinned artifact edited.

- `forseti-harness/source_capture/adapters/browser_snapshot.py` — F1 (added
  explicit fail-loud branch for `chrome_cdp` with no engine) + F2 (removed
  the unused `CloakBrowserPersistentPageObservationSessionEngine` class).
- `forseti-harness/tests/unit/test_source_capture_browser_snapshot.py` — F1
  (new regression test) + F2 (removed the dead class's now-orphaned test and
  import).

```diff
diff --git a/forseti-harness/source_capture/adapters/browser_snapshot.py b/forseti-harness/source_capture/adapters/browser_snapshot.py
index 3ac6a806..3035b521 100644
--- a/forseti-harness/source_capture/adapters/browser_snapshot.py
+++ b/forseti-harness/source_capture/adapters/browser_snapshot.py
@@ -500,6 +500,12 @@ def fetch_browser_page_observation_capture(

     if engine is not None:
         observation_engine = engine
+    elif normalized_browser_backend == BROWSER_BACKEND_CHROME_CDP:
+        raise ValueError(
+            "browser_backend='chrome_cdp' requires an explicit session engine; "
+            "it is never auto-constructed so a missing engine fails loudly "
+            "instead of silently launching a disposable browser"
+        )
     elif normalized_browser_backend == BROWSER_BACKEND_CLOAKBROWSER:
         observation_engine = _CloakBrowserPageObservationEngine(
             cloakbrowser_humanize=cloakbrowser_humanize,
@@ -1785,122 +1791,6 @@ class CloakBrowserPageObservationSessionEngine(_CloakBrowserPageObservationEngin
                 self._closed = True


-class CloakBrowserPersistentPageObservationSessionEngine(
-    CloakBrowserPageObservationSessionEngine
-):
-    """Reuse one retained CloakBrowser profile, context, and page per run."""
-
-    def __init__(self, *, user_data_dir: Path, **kwargs: object) -> None:
-        if not isinstance(user_data_dir, Path):
-            raise TypeError("user_data_dir must be a pathlib.Path")
-        super().__init__(**kwargs)
-        self.user_data_dir = user_data_dir
-
-    def _launch_page_observation_browser(
-        self,
-        *,
-        playwright: object,
-        proxy_profile: ProxyProfile | None,
-        headless: bool,
-        browser_channel: str | None,
-    ) -> object:
-        del playwright
-        if self._closed:
-            raise RuntimeError(
-                "CloakBrowser page-observation session is already closed"
-            )
-        if browser_channel is not None:
-            raise ValueError(
-                "browser_channel is not supported with a persistent CloakBrowser profile"
-            )
-        settings = (proxy_profile, headless, browser_channel)
-        if self._launch_settings is None:
-            self._launch_settings = settings
-        elif settings != self._launch_settings:
-            raise ValueError(
-                "CloakBrowser page-observation session launch settings changed mid-session"
-            )
-        return _SessionBrowserProxy(self)
-
-    def _new_scoped_context(self, context_kwargs: dict[str, object]) -> object:
-        normalized_context_kwargs = {
-            key: value
-            for key, value in context_kwargs.items()
-            if key != "storage_state"
-        }
-        if self._real_context is None:
-            try:
-                cloakbrowser = import_module("cloakbrowser")
-            except ModuleNotFoundError as exc:
-                raise _BrowserSnapshotDependencyUnavailable(
-                    "CloakBrowser is not installed. Install cloakbrowser before running CloakBrowser page observations."
-                ) from exc
-            proxy_profile, headless, _ = self._launch_settings or (None, False, None)
-            launch_kwargs: dict[str, object] = {
-                "headless": headless,
-                "stealth_args": True,
-                "humanize": self.cloakbrowser_humanize,
-                "human_preset": "careful",
-            }
-            viewport = normalized_context_kwargs.pop("viewport", None)
-            if viewport is not None:
-                launch_kwargs["viewport"] = viewport
-            timezone_id = normalized_context_kwargs.pop("timezone_id", None)
-            if timezone_id is not None:
-                launch_kwargs["timezone"] = timezone_id
-            locale = normalized_context_kwargs.pop("locale", None)
-            if locale is not None:
-                launch_kwargs["locale"] = locale
-            if proxy_profile is not None:
-                launch_kwargs["proxy"] = _playwright_proxy_settings(proxy_profile)
-            launch_kwargs.update(normalized_context_kwargs)
-            self._real_context = cloakbrowser.launch_persistent_context(
-                self.user_data_dir,
-                **launch_kwargs,
-            )
-            self._context_settings = {
-                key: value
-                for key, value in context_kwargs.items()
-                if key != "storage_state"
-            }
-        elif normalized_context_kwargs != self._context_settings:
-            raise ValueError(
-                "CloakBrowser page-observation context settings changed mid-session"
-            )
-        return _SessionContextProxy(self)
-
-    def _get_or_create_page(self) -> object:
-        if self._real_context is None:
-            raise RuntimeError("CloakBrowser page-observation context was not created")
-        if self._real_page is not None:
-            is_closed = getattr(self._real_page, "is_closed", None)
-            if callable(is_closed) and is_closed():
-                self._real_page = None
-        if self._real_page is None:
-            existing_pages = list(getattr(self._real_context, "pages", ()))
-            if existing_pages:
-                self._real_page = existing_pages[0]
-            else:
-                self._real_page = self._real_context.new_page()  # type: ignore[attr-defined]
-                self._page_creation_count += 1
-        return self._real_page
-
-    @property
-    def lifecycle_receipt(self) -> dict[str, object]:
-        receipt = dict(super().lifecycle_receipt)
-        receipt.update(
-            {
-                "browser_launch_count": 1 if self._real_context is not None else 0,
-                "profile_persistence": "retained_user_data_directory",
-                "persistent_profile_loaded": self._real_context is not None,
-                "humanized_input_preset": "careful",
-            }
-        )
-        return receipt
-
-
-
-
 class _SessionBrowserProxy:
     def __init__(self, owner: CloakBrowserPageObservationSessionEngine) -> None:
         self._owner = owner
diff --git a/forseti-harness/tests/unit/test_source_capture_browser_snapshot.py b/forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
index 26bff65c..91cb4ca0 100644
--- a/forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
+++ b/forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
@@ -24,7 +24,6 @@ from source_capture.adapters.browser_snapshot import (
     BrowserSnapshotFailureKind,
     BrowserSnapshotSuccess,
     CloakBrowserPageObservationSessionEngine,
-    CloakBrowserPersistentPageObservationSessionEngine,
     ChromeCdpPageObservationSessionEngine,
     fetch_browser_context_responses,
     fetch_browser_page_observation_capture,
@@ -946,6 +945,24 @@ def test_fetch_browser_page_observation_capture_rejects_unknown_browser_backend(
         )


+def test_fetch_browser_page_observation_capture_rejects_chrome_cdp_without_engine() -> None:
+    """chrome_cdp must never silently fall back to a disposable launched browser.
+
+    Without an explicit engine there is no operator-owned Chrome to attach to,
+    so this must fail loudly instead of defaulting to
+    ``_PlaywrightBrowserSnapshotEngine`` (which would launch and discard a
+    fresh browser per capture).
+    """
+    with pytest.raises(ValueError, match="browser_backend='chrome_cdp' requires an explicit session engine"):
+        fetch_browser_page_observation_capture(
+            url="https://example.com/source",
+            dom_extract_script="() => ({items: []})",
+            dom_extract_arg={},
+            response_url_predicate=lambda url: "widget" in url,
+            browser_backend="chrome_cdp",
+        )
+
+
 def test_fetch_browser_page_observation_capture_rejects_cloakbrowser_channel_mix() -> None:
     with pytest.raises(ValueError, match="browser_channel is not supported"):
         fetch_browser_page_observation_capture(
@@ -2969,75 +2986,6 @@ def test_cloakbrowser_page_observation_session_reuses_one_context_and_closes_onc
     assert event_log.count("browser_close") == 1


-def test_persistent_session_engine_reuses_retained_profile_and_existing_page(
-    tmp_path: Path,
-    monkeypatch: pytest.MonkeyPatch,
-) -> None:
-    page = object()
-
-    class FakeContext:
-        def __init__(self) -> None:
-            self.pages = [page]
-            self.close_count = 0
-
-        def new_page(self) -> object:
-            raise AssertionError("existing retained-profile page should be reused")
-
-        def close(self) -> None:
-            self.close_count += 1
-
-    context = FakeContext()
-    launch_calls: list[tuple[Path, dict[str, object]]] = []
-
-    class FakeCloakBrowser:
-        @staticmethod
-        def launch_persistent_context(
-            user_data_dir: Path, **kwargs: object
-        ) -> FakeContext:
-            launch_calls.append((user_data_dir, dict(kwargs)))
-            return context
-
-    original_import_module = browser_snapshot_module.import_module
-
-    def fake_import_module(name: str) -> object:
-        if name == "cloakbrowser":
-            return FakeCloakBrowser()
-        return original_import_module(name)
-
-    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)
-    engine = CloakBrowserPersistentPageObservationSessionEngine(
-        user_data_dir=tmp_path,
-        cloakbrowser_humanize=True,
-    )
-    browser = engine._launch_page_observation_browser(
-        playwright=object(),
-        proxy_profile=None,
-        headless=False,
-        browser_channel=None,
-    )
-    browser.new_context(
-        viewport={"width": 1280, "height": 720},
-        storage_state=str(tmp_path / "ignored-storage-state.json"),
-    )
-
-    assert engine._get_or_create_page() is page
-    assert launch_calls == [
-        (
-            tmp_path,
-            {
-                "headless": False,
-                "stealth_args": True,
-                "humanize": True,
-                "human_preset": "careful",
-                "viewport": {"width": 1280, "height": 720},
-            },
-        )
-    ]
-    assert engine.lifecycle_receipt["persistent_profile_loaded"] is True
-    engine.close()
-    assert context.close_count == 1
-
-
 def test_chrome_cdp_session_detaches_without_closing_context_or_page(
     monkeypatch: pytest.MonkeyPatch,
 ) -> None:
```

## 6. Red/Green Proof (F1)

Same-check proof for the new regression test
(`test_fetch_browser_page_observation_capture_rejects_chrome_cdp_without_engine`):

- **Red (pre-fix):** `git stash push -- forseti-harness/source_capture/adapters/browser_snapshot.py`
  (reverting only the source fix, keeping the new test), then:
  ```
  python -m pytest -q tests/unit/test_source_capture_browser_snapshot.py -k chrome_cdp_without_engine
  ```
  Result: **`F`** — `Failed: DID NOT RAISE <class 'ValueError'>` (the dispatch
  silently fell through to `_PlaywrightBrowserSnapshotEngine` as described in
  F1).
- **Green (post-fix):** `git stash pop` (restoring the fix), same command.
  Result: **`.`** (pass). Confirmed twice (once immediately after restoring,
  once again as part of the full pinned suite in §7).

F2's removal is a subtraction (dead class + its dedicated test deleted); its
proof is the full pinned suite in §7 passing with zero references to the
removed symbol remaining anywhere in the repository
(`grep -rn CloakBrowserPersistentPageObservationSessionEngine` returns no
hits post-patch).

## 7. Observed Validation

All commands run from the stated `cwd`; all exit codes and outputs observed
directly by this reviewer after the patch above was applied (not inherited).

| Command | cwd | Exit | Result |
| --- | --- | --- | --- |
| `python -m pytest -q tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_source_capture_chrome_cdp_session.py tests/unit/test_source_capture_session_profiles.py tests/unit/test_tiktok_blocker_triage.py tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py` | `forseti-harness/` | `0` | GATE PASS — 148 passed (counted via dot-character count; the pytest run in this environment does not print a final summary line under `-q` with this project's `addopts = "-q -p no:cacheprovider"`, but the run produced zero `F`/`E` markers and exit code 0 across all six files). |
| `python -m pytest -q tests/contract` | `forseti-harness/` | `0` | GATE PASS — 125 passed (same dot-count method; zero `F`/`E`; exit 0). |
| `git diff --check` | repo root | `0` | GATE PASS — no whitespace errors. |
| `python .agents/hooks/check_review_routing.py --strict` | repo root | `0` | GATE PASS — `check_review_routing --strict: OK (base: origin/main)`. |

No command was skipped and no command is recorded as not-run; all four
named validation commands in the commission exist and executed.

## 8. Verdict

**`accept_with_friction`.**

The confirmed blocker (F1 — silent disposable-browser fallback for
`chrome_cdp`) and the confirmed major dead-code hazard (F2 — unused
duplicate persistent-Cloak engine) are closed inside the named 15-file patch
scope, with same-check red/green proof for F1 and a clean repo-wide grep for
F2's removal. The remaining findings (F3 major/architecture-level, F4 and F5
minor) do not, on the evidence read, allow a false success, a silently
cleared CAPTCHA/account-risk state, a credentialed/proxied/extension-dependent
CDP path, or a masked primary error — they are residual hardening or
owner-decision items, not confirmed defects requiring a patch under this
commission's authority.

## 9. Residual Risks

- F3 (unverified profile/port binding for CDP attach) — real but
  architecture-level; not closed by this patch.
- F4 (narrower pre-action handoff marker set than post-capture triage) — the
  outcome contract holds; the narrower pre-action gate is a deliberate,
  bounded residual.
- F5 (incomplete exception message on double-failure in onboarding's
  `finally`) — observability-only; the durable receipt already records the
  truth.
- No live browser, TikTok, OAuth, or CAPTCHA operation was run to
  empirically confirm the Playwright `connect_over_cdp` disconnect semantics
  cited in §4; that conclusion rests on the installed library's own
  documentation, read directly, not on live observation.
- This review did not independently re-verify the two authored commits'
  claimed cross-references into files outside the 15-file scope (e.g. the
  Creator Registry preflight and batch-packet admission code the onboarding
  runner calls); those are out of the commissioned target and were treated as
  given.

## 10. Non-Claims

- No `PASS`, readiness, merge, deployment, or account-safety claim is made.
- Nothing was installed; no browser, TikTok, OAuth, CAPTCHA, or lake
  operation was run.
- No login, auth-state export, or credential material was produced, viewed
  in cleartext, or logged by this review.
- No bot-undetectability claim is made or endorsed; this review found no new
  bot-undetectability claim introduced by the diff, and one existing
  truthful-receipt field (`"cookies_or_tokens_persisted": false`) was
  checked and found to be about staging-output hygiene, not evasion.
- No registry/lake data was mutated.
- No scope was widened beyond the 15 pinned files; two files were touched,
  both named in this report's findings.

## 11. Review-Use Boundary

These findings, the diff, and the verdict above are decision input only. They
are not approval, validation, mandatory remediation, or executor-ready patch
authority, and not merge or deployment readiness, until the commissioning
Chief Architect separately adjudicates and accepts them, per
`.agents/workflow-overlay/communication-style.md` -> **Review Adjudication
Next Step**. Runtime model choice is not recommended, ranked, or implied
anywhere in this review.

## 12. Role Receipt

- **current_receiving_actor_role:** de-correlated controller / delegate
  (commissioned executor under `workflow-delegated-review-patch`,
  `delegated_code_review_and_patch` target kind).
- **author_home_model_family:** OpenAI / Codex / GPT-5 (commission-stated).
- **controller_model_family:** Anthropic / Claude (`claude-sonnet-5`,
  this actor).
- **de_correlation_status:** satisfied (`cross_vendor_discovery`); a
  different upstream vendor/model lineage than the author, as required by
  `controller_requirement: different upstream vendor/model lineage`.
- **dispatch_mode:** independent receiving lane / base-subagent controller,
  per commission.
- **delegate lifecycle hard stop honored:** no commit, push, PR
  creation/update, merge, stash (beyond the temporary, immediately-reverted
  red/green stash in §6), reset, worktree cleanup, or repository-hygiene
  action was performed. The report and the patch are left uncommitted in the
  working tree.

## 13. Courier Block

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/tiktok_chrome_cdp_creator_onboarding_delegated_adversarial_code_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: claude-sonnet-5
  authored_by: openai-codex-gpt-5
  summary: >
    Closed one blocker (chrome_cdp silently launched a disposable browser
    instead of failing loudly when no engine was supplied) and one major
    dead-code hazard (unused duplicate persistent-Cloak engine class) inside
    the 15 pinned files; one major (unverified CDP profile/port binding) and
    two minor findings remain as named, unpatched residuals/owner decisions.
  findings_count: 5
  blocking_findings:
    - F1: chrome_cdp silently falls back to a disposable launched browser
      when no engine is supplied (patched)
  advisory_findings:
    - F2: unused duplicate persistent-Cloak engine surface (patched)
    - F3: no binding between resolved profile label and CDP-attached Chrome
      (architecture-level, not patched)
    - F4: pre-action challenge-handoff marker set narrower than post-capture
      account-risk triage (outcome contract holds; not patched)
    - F5: onboarding finally-block close-error message incomplete on
      double-failure (observability-only; not patched)
  prior_findings_remediated: []
  next_action: Chief Architect adjudication
```

Please apply `.agents/workflow-overlay/communication-style.md` -> **Review
Adjudication Next Step**: adjudicate every claim above; self-close any
material issue that sits inside your own authority and this commissioned
scope in the same turn (e.g., accepting or vetoing the F1/F2 patch as
written); route only F3 (or any other genuinely non-self-closable item) to
another review round, lane, architecture pass, or owner decision; once clean,
batch admin/lifecycle follow-ups (commit, push, PR, merge) into exactly one
no-deep-thinking land step; then, if a visible active goal or
`thread_operating_target` exists, deep-think the 1-5 material next moves that
best advance it, or record `no_visible_active_goal` if none exists.
