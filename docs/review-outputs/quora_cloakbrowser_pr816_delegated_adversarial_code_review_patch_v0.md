# Quora CloakBrowser PR 816 Delegated Adversarial Code Review-And-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch output
scope: >
  Bounded delegated_code_review_and_patch pass over PR #816 (profile-backed
  CloakBrowser capture plus the source-detail sufficiency gate). Findings and
  diff are decision input for CA adjudication. Not approval, readiness, or
  auto-keep authority.
commission:
  author_family: OpenAI/Codex
  delegate_family: Anthropic/Claude
  de_correlation_satisfied: true
authority_boundary: retrieval_only
```

```yaml
reviewed_by: claude-sonnet-5
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery
patch_applied: yes
```

---

## 1. Commission and Gate

- Repository: `eric-foo/forseti`, PR #816, branch `codex/quora-cloakbrowser-patch`.
- Target worktree: `C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\quora-cloakbrowser-patch`.
- Start-gate check (`git status --short --branch`, `git rev-parse HEAD`, `git rev-parse main`,
  `git diff --name-only main...HEAD`): branch matched `codex/quora-cloakbrowser-patch`;
  HEAD matched the expected `11fe885c5574ed4c51038a7dea26233dc51f3ff3`; dirty state was
  clean except untracked `_test_runs/`. Local `main` observed as `9b8edc7c89ec6578d6eba19df7abe45fee4bf848`,
  newer than the commission's recorded `8dfec4c39295ff41dfe18f4e69b454bf8d361cf9` — per the
  commission's explicit allowance, the newer main SHA is recorded here and the PR branch is
  still reviewed with `main...HEAD`.
- Review method: `workflow-code-review` under the code-diff sibling mode of
  `.agents/workflow-overlay/delegated-review-patch.md`, not artifact review.

**SOURCE_CONTEXT_READY.** Sources read in full before analysis:

- `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/decision-routing.md`,
  `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`,
  `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/source-loading.md`
- Full PR diff (`git diff main...HEAD`, 9 files, +936/-43)
- `forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py` (full file)
- `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py` (full file)
- `forseti-harness/runners/run_source_capture_browser_packet.py` (diff + surrounding context)
- `forseti-harness/runners/run_source_capture_authenticated_browser_packet.py` (diff + surrounding context)
- `forseti-harness/source_capture/source_detail_sufficiency.py` (full new file)
- `forseti-harness/source_capture/browser_user_data.py` (full file — pre-existing, unmodified,
  read to confirm the label→path resolution used by the new CLI flag is traversal-safe)
- `forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py`,
  `test_source_capture_browser_snapshot.py`, `test_source_capture_authenticated_browser_snapshot.py`,
  `test_source_detail_sufficiency.py` (new/changed sections in full)
- Local live-run evidence: both referenced `_test_runs/` packets exist and were inspected
  (manifests + metadata JSON), see §6.

No source gaps materially affected the findings below.

---

## 2. Findings (ordered by severity)

### F1 — MAJOR: Profile-backed persistent-context capture silently drops the proxy while packet metadata still claims it was used

**File:** `forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py`
**Lines (pre-patch):** `_CloakBrowserSnapshotEngine.capture`, the `user_data_dir is not None` branch
(`launch_persistent_context(user_data_dir, headless=True, stealth_args=True, humanize=humanize)`),
and the unconditional `proxy_used`/`proxy_category`/`geoip_used`/`proxy_timezone`/`proxy_locale`
metadata fields in `fetch_cloakbrowser_snapshot_capture`.

**Evidence:**

`run_source_capture_cloakbrowser_packet` accepts `proxy_profile` and `browser_user_data_dir` as two
fully independent optional parameters — nothing in the runner, the CLI (`--proxy-profile-category` /
`--browser-user-data-label`), or the adapter rejects supplying both. When both are supplied, the
persistent-context branch runs:

```python
context = launch_persistent_context(
    user_data_dir,
    headless=True,
    stealth_args=True,
    humanize=humanize,
)
```

— `proxy_profile.proxy_endpoint`, `.timezone`, `.locale`, `.geoip_enabled` are never passed, unlike the
anonymous-launch branch immediately below it which does pass all of them to `launch()`. Meanwhile
`fetch_cloakbrowser_snapshot_capture`'s metadata block sets `"proxy_used": proxy_profile is not None`,
`"proxy_category": proxy_profile.proxy_category.value if proxy_profile is not None else None`, etc.,
**unconditionally** — derived from whether `proxy_profile` was passed in, not from which launch path
actually ran. The runner's own receipt-text builders (`_default_capture_context`, `_access_posture_value`)
independently confirm the combination was an intended narrative, not an overlooked edge case: both
functions construct sentences describing "profile-backed ... and label-indirected {proxy_category} proxy
profile" together when both parameters are set. So the code was written expecting the combination to be
meaningful, but the actual capture silently ignores the proxy in that case while the packet's provenance
fields, receipt text, and non-claims all still assert proxy protection was applied.

**Risk:** A caller combining `--browser-user-data-label` with a proxy profile gets a packet whose
`manifest["receipt_metadata"]` and `04_*_snapshot_metadata.json` both claim `proxy_used: true` and a
specific `proxy_category`/timezone/locale, when the browser in fact launched with no proxy at all —
a false provenance claim on exactly the axis (proxy disclosure, IP/geo posture) this adapter's non-claims
list exists to be honest about. Not exercised by any unit test (the new persistent-context test explicitly
uses `proxy_profile=None`) or by either live Quora probe inspected in §6 (both show `proxy_used: false`
in the profile-backed run).

**Minimum closure condition:** Either (a) the persistent-context launch actually applies the proxy/timezone/
locale/geoip settings when both are supplied, with metadata reflecting the real launch path, or (b) the
combination is rejected before any capture attempt so the packet is never written with proxy-claim metadata
that doesn't match what the browser did.

**Next authorized action:** Patch (applied — see §3/§4). I chose (b): reject the combination with a clear
`ValueError` rather than guess the external `cloakbrowser` package's `launch_persistent_context` keyword
surface (unverifiable from this repo — no vendored source, no network access in this session). Guessing
wrong kwargs risks a worse failure mode (a runtime `TypeError` on every profile-backed capture) for an
external API this review cannot confirm. If the CA/owner can confirm `launch_persistent_context` accepts
`proxy`/`timezone`/`locale`/`geoip`, option (a) is the more complete fix and should replace this patch.

**Confidence:** high (the code-level asymmetry between the two launch branches, the unconditional metadata
block, and the receipt-text builders' explicit "profile + proxy" narrative are all directly readable in the
diff; the only uncertainty is the unverifiable external library surface, which is exactly why (b) was chosen
over (a)).

**Patched:** Yes.

---

### F2 — MINOR: `run_source_capture_cloakbrowser_packet` accepted `browser_user_data_dir` without requiring the matching label/session-mode that drive provenance disclosure

**File:** `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`
**Lines (pre-patch):** `run_source_capture_cloakbrowser_packet` signature and body;
`_visible_mode_changes` and `_cloakbrowser_snapshot_non_claims`.

**Evidence:** `browser_user_data_label`, `browser_user_data_session_mode`, and `browser_user_data_dir`
are three independent optional parameters on the runner function. Only the CLI's `main()` enforces
label/session-mode pairing (`(args.browser_user_data_label is None) != (browser_user_data_session_mode
is None)` → `ValueError`), and `main()` always derives `browser_user_data_dir` from the label, so the
three are only kept in sync by CLI-side discipline, not by the runner itself. `_visible_mode_changes`
only appends the `cloakbrowser_persistent_profile_loaded:...` disclosure label when **both**
`browser_user_data_label` and `browser_user_data_session_mode` are non-`None`; `_cloakbrowser_snapshot_
non_claims` only swaps in the profile-aware non-claims (dropping "not login or session capture" / "not
stored profile or cookie use") when `browser_user_data_session_mode` is non-`None`. A caller that invokes
the runner directly with `browser_user_data_dir` set but `browser_user_data_label`/`browser_user_data_
session_mode` left `None` would load a real persistent profile while the packet's visible-mode-changes and
non-claims still read as if no stored profile/cookie use occurred — the inverse of F1's failure mode
(silent under-disclosure instead of silent over-claim), on the same provenance surface.

**Risk:** Not reachable through the shipped CLI today (no other caller in this diff or the rest of the repo
passes `browser_user_data_dir` to this runner). It is reachable through the public function directly, as
the unit tests already do, so it is a real latent gap in the function's own contract rather than a
theoretical one — a future batch/cadence caller that reuses this runner would inherit the gap silently.

**Minimum closure condition:** `run_source_capture_cloakbrowser_packet` rejects `browser_user_data_dir`
being supplied without both `browser_user_data_label` and `browser_user_data_session_mode`, independent of
CLI-side discipline.

**Next authorized action:** Patch (applied — see §3/§4).

**Confidence:** medium (real gap in the function contract; currently unreachable via the shipped CLI, so
practical exposure today is low).

**Patched:** Yes.

---

### Considered and defended

- **Keyword-only parameter ordering in `run_source_capture_cloakbrowser_packet`:** the new
  `browser_user_data_label`/`_session_mode`/`_dir` parameters (each with a default) are inserted before
  several parameters without defaults (`actor_audience_context`, `visible_mode_changes`, ...), which would
  be a `SyntaxError` for positional-or-keyword parameters. Defeated: the function signature opens with a
  bare `*,` (line 82), making every parameter keyword-only, where Python does not require default-before-
  non-default ordering. Confirmed by `python -m py_compile` succeeding and by reading the full signature
  directly (not just the diff hunk).
- **`test_cloakbrowser_snapshot_runner_fail_closes_source_detail_sufficiency_after_packet_write` passes
  `browser_user_data_label="quora-client"` with `browser_user_data_session_mode=None` and
  `browser_user_data_dir=None`:** looks like the same mismatched-pairing shape as F2. Defeated as a
  distinct bug: since `browser_user_data_dir` is `None`, no persistent context is attempted regardless of
  the label value, so this is inert test looseness (the label is simply irrelevant to that test's actual
  assertions), not a reachable defect. Confirmed it does not trip the new F2 guard, which only fires when
  `browser_user_data_dir is not None` (test suite re-run post-patch, all 156 pass).
- **Removing `backend=CLOAKBROWSER_BACKEND` from the anonymous `launch()` call could silently change
  which browser engine launches:** cannot be fully confirmed from this repo (the `cloakbrowser` package
  is an external dependency, not vendored). Defeated to the extent checkable: `CLOAKBROWSER_BACKEND` is
  still used unchanged for descriptive metadata elsewhere, only the launch-call kwarg was removed; the
  updated unit test for the anonymous path (`test_live_engine_uses_anonymous_non_persistent_launch`) still
  asserts every other launch kwarg unchanged; and the author's own live-run evidence (§6) shows a 0-exit,
  12,374-byte-visible-text capture through this exact code path against the real Quora Cloudflare gate,
  which would not succeed if the launch call were broken. Residual uncertainty about the library's default
  backend selection remains (see §7) but is not, on the evidence available, a blocking finding.
- **Persistent-context branch never passes `viewport_width`/`viewport_height` to `launch_persistent_context`
  (unlike the anonymous branch's `browser.new_context(viewport={...})`):** both branches now also call
  `page.set_viewport_size(...)` as a fallback after page creation, and the new persistent-context test
  asserts `viewport_size == {"width": 1024, "height": 768}` is actually achieved via that fallback. Not a
  functional gap, just a structural asymmetry; not blocking.

---

## 3. Patch Summary

Two findings patched, both by rejecting an unsafe input combination rather than guessing at the external
`cloakbrowser` package's undocumented API surface — consistent with `NEEDS_ARCHITECTURE_PASS` guidance to
avoid patching past what this review can actually verify. No packet schema, sufficiency-gate semantics, or
proxy-profile/auth-state doctrine was touched.

**F1 patch — `forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py`:**
Added an early validation in `fetch_cloakbrowser_snapshot_capture` that raises `ValueError` when both
`user_data_dir` and `proxy_profile` are supplied, before any capture is attempted.

**F2 patch — `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`:**
Added an early validation in `run_source_capture_cloakbrowser_packet` that raises `ValueError` when
`browser_user_data_dir` is supplied without both `browser_user_data_label` and
`browser_user_data_session_mode`.

**Tests — `forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py`:**
Added `test_fetch_cloakbrowser_snapshot_capture_rejects_combining_user_data_dir_and_proxy_profile` (F1) and
`test_cloakbrowser_runner_rejects_user_data_dir_without_label_and_session_mode` (F2).

Both new `ValueError`s propagate through the existing `main()` `except ValueError as exc: parser.exit(status=2, ...)`
handler unchanged (verified by reading `main()`; not separately CLI-invoked in this pass since the fixtures
needed for a full CLI subprocess run were out of the bounded validation slice).

---

## 4. Unified Diff

```diff
diff --git a/forseti-harness/runners/run_source_capture_cloakbrowser_packet.py b/forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
index 7f586a7a..276981a3 100644
--- a/forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
+++ b/forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
@@ -128,6 +128,14 @@ def run_source_capture_cloakbrowser_packet(
 ) -> tuple[int, str]:
     if (output_directory is None) == (data_root is None):
         raise ValueError("exactly one of output_directory or data_root is required")
+    if browser_user_data_dir is not None and (
+        browser_user_data_label is None or browser_user_data_session_mode is None
+    ):
+        raise ValueError(
+            "browser_user_data_dir requires browser_user_data_label and browser_user_data_session_mode "
+            "so the packet's visible-mode-change and non-claims provenance reflects the persistent "
+            "profile load; a caller must not load a stored profile without disclosing it in the packet"
+        )

     # The US-storefront pin is an Amazon-specific pre-capture plugin (FIX #6): the generic
     # adapter knows nothing about Amazon or its delivery-location widget. The plugin carries
diff --git a/forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py b/forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py
index c6509fc1..7ea143c6 100644
--- a/forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py
+++ b/forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py
@@ -219,6 +219,13 @@ def fetch_cloakbrowser_snapshot_capture(
         raise ValueError("load_more_clicks must be zero or greater")
     if load_more_clicks > 0 and not load_more_selector:
         raise ValueError("load_more_selector is required when load_more_clicks is greater than zero")
+    if user_data_dir is not None and proxy_profile is not None:
+        raise ValueError(
+            "CloakBrowser persistent-context capture (user_data_dir) does not apply proxy_profile; "
+            "the persistent-context launch path never receives the proxy, so combining them would "
+            "record proxy_used/proxy_category in packet metadata while no proxy was actually used. "
+            "Supply only one of user_data_dir or proxy_profile."
+        )
     if wait_until not in ALLOWED_WAIT_UNTIL:
         allowed = ", ".join(sorted(ALLOWED_WAIT_UNTIL))
         raise ValueError(f"wait_until must be one of: {allowed}")
diff --git a/forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py b/forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
index 3fe18cba..c2fcc1db 100644
--- a/forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
+++ b/forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
@@ -2590,4 +2590,61 @@ def test_cloakbrowser_snapshot_runner_fail_closes_source_detail_sufficiency_afte
     manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
     assert "source_detail_sufficiency_failed" in manifest["visible_mode_changes"]
     assert any("source_detail_sufficiency_failed" in item for item in manifest["limitations"])
-    assert any("not source-content capture" in item for item in manifest["receipt_metadata"]["non_claims"])
+    assert any("not source-content capture" in item for item in manifest["receipt_metadata"]["non_claims"])
+
+
+def test_fetch_cloakbrowser_snapshot_capture_rejects_combining_user_data_dir_and_proxy_profile(
+    scratch_dir: Path,
+) -> None:
+    profile = ProxyProfile(
+        proxy_endpoint="http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080",
+        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
+        geoip_enabled=False,
+    )
+
+    with pytest.raises(ValueError, match="does not apply proxy_profile"):
+        fetch_cloakbrowser_snapshot_capture(
+            url="https://example.com/source",
+            proxy_profile=profile,
+            user_data_dir=scratch_dir,
+        )
+
+
+def test_cloakbrowser_runner_rejects_user_data_dir_without_label_and_session_mode(
+    scratch_dir: Path,
+) -> None:
+    output_dir = scratch_dir / "packet"
+
+    with pytest.raises(
+        ValueError, match="browser_user_data_dir requires browser_user_data_label"
+    ):
+        cloakbrowser_runner.run_source_capture_cloakbrowser_packet(
+            url="https://www.quora.com/search?q=B2B%20questions",
+            source_family="web_page",
+            source_surface="cloakbrowser_snapshot",
+            decision_question="Can Quora search provide B2B question candidates?",
+            output_directory=output_dir,
+            capture_context="test provenance guard",
+            operator_category="cloakbrowser_snapshot_cli_operator",
+            capture_mode=CaptureModeCategory.MULTIMODAL,
+            session_id=None,
+            proxy_profile=None,
+            browser_user_data_label=None,
+            browser_user_data_session_mode=None,
+            browser_user_data_dir=scratch_dir,
+            actor_audience_context=None,
+            visible_mode_changes=[],
+            source_publication_or_event=None,
+            source_edit_or_version=None,
+            cutoff_posture=None,
+            recapture_time=None,
+            re_capture_relationship=None,
+            warnings=[],
+            limitations=[],
+            timeout_seconds=20,
+            wait_until="load",
+            viewport_width=1280,
+            viewport_height=720,
+            max_artifact_bytes=50_000,
+            block_heavy_assets=False,
+        )
```

---

## 5. Validation Commands and Observed Output

```powershell
git status --short --branch
git diff --check
Push-Location forseti-harness
python -m py_compile source_capture\source_detail_sufficiency.py source_capture\adapters\cloakbrowser_snapshot.py runners\run_source_capture_browser_packet.py runners\run_source_capture_authenticated_browser_packet.py runners\run_source_capture_cloakbrowser_packet.py
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests\unit\test_source_detail_sufficiency.py tests\unit\test_source_capture_browser_snapshot.py tests\unit\test_source_capture_authenticated_browser_snapshot.py tests\unit\test_source_capture_cloakbrowser_snapshot.py
Pop-Location
```

**Observed (bash equivalent actually run, same commands/semantics):**

- `git status --short --branch`: `## codex/quora-cloakbrowser-patch...origin/codex/quora-cloakbrowser-patch`,
  three modified files (the patch) plus untracked `_test_runs/`. No other dirty state.
- `git diff --check`: clean, no output.
- `python -m py_compile ...` (all five touched/adjacent source files): succeeded, no output.
- `python -m pytest -p no:cacheprovider -q tests/unit/test_source_detail_sufficiency.py
  tests/unit/test_source_capture_browser_snapshot.py
  tests/unit/test_source_capture_authenticated_browser_snapshot.py
  tests/unit/test_source_capture_cloakbrowser_snapshot.py`:

  ```
  ........................................................................ [ 46%]
  ........................................................................ [ 92%]
  ............                                                             [100%]
  156 passed in 1.73s
  ```

  156 = the author's pre-patch baseline plus the 2 new tests added by this patch. The first attempt at
  the F1 test failed with `TypeError: ProxyProfile.__init__() missing 1 required positional argument:
  'geoip_enabled'` (a test-authoring mistake on my side, not a product defect); fixed by adding
  `geoip_enabled=False` to the fixture, then re-run to the clean 156-pass result above.

No test failed after the fix; no gate returned `not-run`.

---

## 6. Live Evidence Interpretation

Both referenced `_test_runs/` packets exist and were inspected directly (not trusted from the commission's
prose):

- `source_capture_quora_b2b_search_auth_browser_sufficiency_fail_probe_20260709/manifest.json`:
  `limitations` includes `"access_failed: ... cloudflare_interstitial ..."` and
  `"source_detail_sufficiency_failed: access blocked: cloudflare_interstitial; visible text too small: 0
  bytes < required 1000; missing visible text literal: 'Results for B2B questions'; ..."`. Matches the
  commission's claim of a lower-rung authenticated-browser Quora probe failing sufficiency with 0 visible
  text.
- `source_capture_quora_b2b_search_cloak_profile_sufficiency_success_20260709/manifest.json`:
  `visible_mode_changes` includes `source_detail_sufficiency_passed` and
  `cloakbrowser_persistent_profile_loaded:client_provided_session:quora_client_provided_20260709`;
  `limitations` is empty. The corresponding `04_cloakbrowser_snapshot_metadata.json` shows
  `visible_text_byte_count: 12374`, `access_blocked: false`, `persistent_profile_loaded: true`, and —
  load-bearing for F1 — `proxy_used: false`, `proxy_category: None`. This run never combined a proxy
  profile with the persistent profile, so it corroborates rather than refutes F1: the specific failure mode
  (proxy silently dropped, metadata still claiming proxy use) was not exercised by either the author's own
  live probes or the new unit tests.

The claim these two packets support is exactly what the commission states, no wider: the sufficiency gate
distinguishes a useless lower-rung packet (0 visible text, Cloudflare-blocked) from a useful profile-backed
capture for this one Quora B2B search query. It is not evidence that the sufficiency gate, the proxy path,
or the profile path are correct in general, or that the proxy+profile combination (F1) works.

---

## 7. Residual Risk

- **External `cloakbrowser` library API surface is unverifiable from this repo.** Both the removed
  `backend=` kwarg (compatibility fix) and `launch_persistent_context`'s actual accepted parameters are
  facts about a dependency not vendored here. The live-run evidence in §6 corroborates the compatibility fix
  works against the real library for the anonymous path; the persistent-context path's viewport/proxy
  parameter surface remains unconfirmed beyond what F1's patch defensively closes off.
- **`_detect_access_blocked_page`/`classify_rendered_access` heuristic coverage is unchanged by this PR**
  and was not re-audited in this pass (out of the named editable scope); a novel access-block page shape
  it does not recognize would still pass the sufficiency gate if it happened to contain the required
  literals/regexes. Pre-existing risk, not introduced or worsened here.
- **F2's guard is currently dead code on the only shipped call path** (the CLI always keeps label/session-
  mode/dir in sync); its value is defense-in-depth for future direct callers of the runner, not a fix to an
  actively reachable defect today.
- **Literal/regex sufficiency predicates use plain substring/`re.search` matching** with no Unicode
  normalization; a source that renders the required text with different Unicode composition would fail
  sufficiency even though a human would consider the content present. Not evaluated as blocking — this is
  a reasonable default and no evidence suggests it affects the Quora case — but it is a real edge case the
  predicate design does not address.

---

## 8. Verdict

**`PATCHED_FOR_CA_ADJUDICATION`**

One MAJOR finding (F1: silent proxy drop + false proxy provenance in profile-backed persistent-context
capture) and one MINOR finding (F2: runner-level provenance gap for direct callers) were patched, both by
rejecting the unsafe input combination rather than guessing unverifiable external-library behavior. Four
additional candidate concerns were considered and defeated (see "Considered and defended") rather than
silently dropped. All 156 tests in the required validation slice pass post-patch, including 2 new tests
covering the patched guards. No off-scope files were touched; no packet schema, sufficiency-gate semantics,
or auth-state doctrine was changed.

## 9. CA Adjudication Addendum

CA adjudication by OpenAI/Codex GPT-5 on 2026-07-10 accepted F1 and F2, with one modification before keep:

- F1 accepted as MAJOR. The adapter-level `user_data_dir` + `proxy_profile` rejection is kept.
- F2 accepted as MINOR. The runner-level `browser_user_data_dir` provenance guard is kept.
- CA modification: added a matching CLI validation before `--preflight-only` can print `preflight passed`, because the delegate patch still allowed a profile+proxy preflight to report success before reaching the runner or adapter guards.
- CA test addition: `test_cloakbrowser_snapshot_cli_preflight_rejects_proxy_with_browser_profile` verifies that preflight rejects the impossible profile+proxy combination without printing `preflight passed`, without writing a packet, and without leaking proxy credentials or host details.

Post-adjudication validation observed by CA:

```powershell
git diff --check
Push-Location forseti-harness; python -m py_compile source_capture\source_detail_sufficiency.py source_capture\adapters\cloakbrowser_snapshot.py runners\run_source_capture_browser_packet.py runners\run_source_capture_authenticated_browser_packet.py runners\run_source_capture_cloakbrowser_packet.py; Pop-Location
Push-Location forseti-harness; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider tests\unit\test_source_detail_sufficiency.py tests\unit\test_source_capture_browser_snapshot.py tests\unit\test_source_capture_authenticated_browser_snapshot.py tests\unit\test_source_capture_cloakbrowser_snapshot.py; Pop-Location
```

- `git diff --check`: exit 0, no output.
- `py_compile`: exit 0, no output.
- Focused pytest slice: `157 passed in 1.64s`.

Final CA disposition before commit: keep the delegated patch as modified. The final kept diff contains three guards (adapter profile+proxy rejection, runner profile-provenance rejection, CLI preflight profile+proxy rejection) and three regression tests.

This addendum is an adjudication record, not a second delegated review and not a formal readiness or approval claim.


## Review-Use Boundary

These findings, the diff, the validation output, and the verdict above are decision input for CA
adjudication only. They are not approval, not validation, not mandatory remediation, and not
executor-ready patch authority — the CA reserves final authority over what, if anything, is kept.
