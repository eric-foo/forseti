# Source Capture Browser Snapshot Adapter v0 — Adversarial Implementation / Code Review

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Adversarial implementation and code review of the Browser Snapshot Adapter v0 for the Source Capture Toolbox.
review_type: adversarial_implementation_code_review
review_date: 2026-06-03
reviewer: Claude Sonnet 4.6 (automated adversarial review; read-only)
worktree: C:/Users/vmon7/Desktop/projects/orca
expected_branch: main
hash_verification: ALL_PASSED (19/19)
edit_permission: none — read-only review; no patches applied
```

---

## Hash Verification Preflight

All 10 target files and 9 source-basis files verified before review commenced.

```text
VERIFIED TARGET FILES (10/10):
  OK  docs/product/source_capture_toolbox/README.md
  OK  orca-harness/README.md
  OK  orca-harness/docs/source_capture_agent_runbook.md
  OK  orca-harness/docs/source_capture_packet.md
  OK  orca-harness/pyproject.toml
  OK  orca-harness/source_capture/adapters/__init__.py
  OK  orca-harness/source_capture/adapters/browser_snapshot.py
  OK  orca-harness/runners/run_source_capture_browser_packet.py
  OK  orca-harness/tests/unit/test_source_capture_browser_snapshot.py
  OK  orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py

VERIFIED SOURCE-BASIS FILES (9/9):
  OK  AGENTS.md
  OK  .agents/workflow-overlay/README.md
  OK  docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  OK  docs/product/data_capture_source_access_boundary_decision_v0.md
  OK  docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  OK  orca-harness/source_capture/models.py
  OK  orca-harness/source_capture/writer.py
  OK  orca-harness/source_capture/cli_support.py
  OK  orca-harness/source_capture/adapters/direct_http.py
```

No mismatches. Review proceeds.

---

## Findings (Severity-First)

### M-01 — Minor: `visible_text` extraction failure silently produces empty output with no warning

**File**: `orca-harness/source_capture/adapters/browser_snapshot.py:215–218`

**Code**:
```python
try:
    visible_text = page.locator("body").inner_text(timeout=timeout_ms)
except Exception:
    visible_text = ""
```

When `page.locator("body").inner_text()` raises any exception (missing `<body>`, XML document, rendering error, Playwright internal error), the exception is swallowed silently, `visible_text` is set to `""`, and execution continues to return a `BrowserSnapshotSuccess`. No `warning_notes` entry is appended. The packet's `browser_visible_text.txt` in `raw/` will contain only a newline character (one byte), and the manifest will record `visible_text_byte_count: 0`.

**Risk**: An agent or operator reading the packet sees `visible_text_byte_count: 0` and cannot distinguish between (a) the page genuinely had no visible text, (b) the text extraction raised an error, or (c) the `<body>` element was absent. All three produce the same packet footprint. The metadata field gives no signal that an exception was suppressed. This weakens the packet's observable-fidelity posture against Obligation 6 (Raw Observable Fidelity) without making the limitation visible.

**This is not a fake-success path** — the DOM and screenshot are still preserved, the packet is real. But the observable gap is not disclosed within the packet.

**Recommendation**: When the `except` branch fires, append to `warning_notes`: `"visible_text extraction raised an exception; visible_text_byte_count is 0; rendered_dom is still preserved"` (or equivalent). This makes the limitation visible without changing any other behavior.

---

### M-02 — Minor: No unit tests for `EMPTY_RENDERED_DOM` or `EMPTY_SCREENSHOT` failure kinds

**Files**: `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`,
`orca-harness/source_capture/adapters/browser_snapshot.py:114–127`

**Code paths not covered**:
```python
# browser_snapshot.py lines 114–127
if not engine_result.rendered_dom:
    return BrowserSnapshotFailure(
        ...
        failure_kind=BrowserSnapshotFailureKind.EMPTY_RENDERED_DOM,
        message="Browser snapshot returned an empty rendered DOM",
    )
if not engine_result.screenshot_png:
    return BrowserSnapshotFailure(
        ...
        failure_kind=BrowserSnapshotFailureKind.EMPTY_SCREENSHOT,
        message="Browser snapshot returned an empty screenshot",
    )
```

These two failure kinds require the browser to have successfully launched, navigated, and returned — but the engine result contains empty content. This can be triggered by real pages: server-side rendering issues, content-gated app shells, cookie walls that return empty body, or pages where Playwright's screenshot API fails. Both paths already return `BrowserSnapshotFailure` with no packet written, which is the correct behavior.

**Risk**: If a regression were introduced (e.g., the checks were reordered, the conditions changed, or the early-return removed), no test would catch it. The `CAPTURE_FAILED` and `TIMEOUT` cases are tested; the empty-content cases are not.

**The fake-engine infrastructure already exists** in the test file — `_FakeBrowserEngine` and `_FakeEngineResult` can trivially produce `rendered_dom=""` or `screenshot_png=b""`. This is low-cost to add.

---

### A-01 — Advisory: `playwright install` browser binary step absent from all docs

**Files**: `orca-harness/README.md`, `orca-harness/docs/source_capture_agent_runbook.md`, `orca-harness/docs/source_capture_packet.md`

Installing `orca-harness[browser]` (or `playwright>=1.44,<2`) via pip installs the Playwright Python package but does not install the Chromium browser binary. The operator must separately run `playwright install chromium` (or `playwright install`). None of the three user-facing docs mention this step.

**Effect**: When Playwright is installed but Chromium binaries are absent, `chromium.launch(headless=True)` raises a Playwright `Error` (not `ModuleNotFoundError`). This exception is caught by the generic `except Exception` branch in `fetch_browser_snapshot_capture`, not by the `_BrowserSnapshotDependencyUnavailable` handler. The failure kind returned is `CAPTURE_FAILED`, not `DEPENDENCY_UNAVAILABLE`. The exit code is still 3 (no packet), which is correct — but the error message is a Playwright "Executable doesn't exist" message rather than "Playwright is not installed." An operator or agent following the docs would not know they need a second install step.

**No boundary or correctness impact.** Pure usability / operator-guidance gap.

---

### A-02 — Advisory: `test_browser_snapshot_module_imports_without_playwright_installed` does not enforce Playwright absence

**File**: `orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py:21–25`

```python
def test_browser_snapshot_module_imports_without_playwright_installed() -> None:
    module = importlib.import_module("source_capture.adapters.browser_snapshot")
    assert hasattr(module, "fetch_browser_snapshot_capture")
```

This test only verifies the module is importable; it does not verify that Playwright is absent from the environment. If Playwright is installed when the test suite runs, the test passes regardless of whether the import was truly lazy. If Playwright is later added as a main (non-optional) dependency by mistake, this test would not catch it.

**The static AST tests are more rigorous**: `test_only_browser_snapshot_surfaces_name_playwright_dependency` reads the source text of every adapter and runner file and asserts `"playwright"` does not appear in any file except `browser_snapshot.py`. This catches module-level or function-level static references. Combined with the `_forbidden_import_roots` AST walk, the import isolation contract is well-guarded statically.

**Advisory only**: the static tests are the reliable gate. The runtime test's name is misleading but it doesn't undermine safety.

---

### A-03 — Advisory: Browser context not explicitly closed before `browser.close()`

**File**: `orca-harness/source_capture/adapters/browser_snapshot.py:203–228`

```python
browser = playwright.chromium.launch(headless=True)
try:
    context = browser.new_context(...)
    page = context.new_page()
    page.goto(url, ...)
    rendered_dom = page.content()
    ...
finally:
    browser.close()
```

`context.close()` is never called explicitly. Playwright's `browser.close()` does cascade-close all contexts and pages in the sync API, so there is no resource leak in normal operation. However, explicit `context.close()` is Playwright's recommended pattern; the close order can matter if Playwright changes how it handles pending async operations, network drains, or cleanup hooks across versions.

**No current defect.** Purely a defensive hygiene gap.

---

### A-04 — Advisory: Partial output directory possible if `write_local_source_capture_packet` fails mid-write

**File**: `orca-harness/runners/run_source_capture_browser_packet.py:136–186`

If `write_local_source_capture_packet` raises after creating `raw/` and copying some files (e.g., Pydantic model validation rejects a field combination), a partial output directory may remain on disk. The `finally` block cleans staging files but does not roll back the output directory. The runner exits with code 3 (or the exception propagates to `main()` as code 3), which correctly signals no normal packet. An agent checking whether the output directory exists would find it exists — partially filled.

**This is the same behavior shared by direct_http, media_asset, and archive_org adapters** — not a regression introduced by browser snapshot. Noted for completeness as an acknowledged inherent limitation of the current packet-writer contract. No operator-visible fix is applied here without a broader writer contract change.

---

### A-05 — Advisory: URL validator permits userinfo (embedded credentials) in URL

**File**: `orca-harness/source_capture/adapters/browser_snapshot.py:244–248`

```python
def _validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Browser snapshot capture requires an absolute http:// or https:// URL")
    return parsed.geturl()
```

`http://user:pass@example.com` passes validation. If an operator supplies such a URL, Playwright will use those credentials for HTTP Basic Auth — a form of credential use that the v0 boundary explicitly excludes ("no credentials"). The requested_url and metadata in the packet would then contain the credential-bearing URL.

**Not a defect under the current operator-responsibility model**: the operator controls the URL and the adapter accepts what is supplied. This is consistent with `direct_http.py` (same validator shape). However, a conservative guard rejecting `parsed.username or parsed.password` would make the boundary explicit at the code level.

---

### A-06 — Advisory: `page.screenshot()` timeout is not governed by `timeout_seconds`

**File**: `orca-harness/source_capture/adapters/browser_snapshot.py:219`

```python
screenshot_png = page.screenshot(type="png", full_page=False)
```

`page.goto()` and `page.locator("body").inner_text()` are both called with `timeout=timeout_ms`. `page.screenshot()` is not. Playwright's default screenshot timeout is 30 seconds (independent of `timeout_ms`). This means the total execution time of `capture()` can exceed `timeout_seconds + 30s` if the screenshot hangs. In practice, screenshoting a loaded page is fast and this scenario is unlikely; it is a behavioral gap rather than a latent defect.

---

## Review Question Answers

**Q1 — Does `browser_snapshot.py` preserve the v0 boundary (anonymous/headless only)?**

Yes. `browser.new_context()` is called with only `viewport` — no `storage_state`, `http_credentials`, `cookies`, `proxy`, `user_agent` override, or `extra_http_headers`. This produces a fresh, isolated browser context with no persistent session data. `headless=True` is explicit. No anti-detect behavior, no proxy configuration, no CAPTCHA handling, no OCR, no crawling, no source discovery. The `_validate_http_url` validator restricts input to `http://` or `https://` scheme with a non-empty netloc. Boundary: **CLEAN**.

**Q2 — Is Playwright dependency handling actually lazy and isolated?**

Yes. `playwright.sync_api` is imported inside `_PlaywrightBrowserSnapshotEngine.capture()` via `importlib.import_module()`, not at module level. `browser_snapshot.py` can be imported without Playwright installed (verified by the contract test). Importing `source_capture.adapters` triggers the `browser_snapshot.py` module body, which has no Playwright import. The static AST test `test_only_browser_snapshot_surfaces_name_playwright_dependency` verifies that no other file in the adapter stack or runners mentions Playwright. Isolation: **CLEAN**.

One nuance (A-01): if Playwright is installed but Chromium binaries are absent, the lazy-import succeeds but `chromium.launch()` fails with a non-`ModuleNotFoundError` exception — reported as `CAPTURE_FAILED` rather than `DEPENDENCY_UNAVAILABLE`.

**Q3 — Does the runner write the four intended artifacts and clean staging files on both success and failure?**

Success path: All four staging files (`browser_rendered_dom.html`, `browser_visible_text.txt`, `browser_viewport_screenshot.png`, `browser_snapshot_metadata.json`) are written to `output_directory.parent/`, passed to `write_local_source_capture_packet` as `input_files`, copied into `raw/`, then cleaned in the `finally` block. The test `test_browser_snapshot_runner_writes_packet_with_four_artifacts` confirms all four appear in `raw/` and staging is gone.

Failure path: The `finally` block cleans only files in `written_paths` (those actually written before the failure). If failure occurs after writing files 1–3 but before file 4, files 1–3 are cleaned. Verified by `test_browser_snapshot_runner_cleans_staged_files_when_metadata_write_fails`.

**Q4 — Does any failure path create a fake packet, fake clean capture, or misleading exit code?**

No fake packets found. Each failure path traces correctly:

| Failure | Handler | Exit | Packet |
|---|---|---|---|
| URL scheme/netloc invalid | `ValueError` → `main()` exit 2 | 2 | none |
| `wait_until` invalid | `ValueError` → `main()` exit 2 | 2 | none |
| Playwright not installed | `DEPENDENCY_UNAVAILABLE` → runner returns (3, msg) | 3 | none |
| Navigation/browser exception | `CAPTURE_FAILED`/`TIMEOUT` → runner returns (3, msg) | 3 | none |
| Empty rendered DOM | `EMPTY_RENDERED_DOM` → runner returns (3, msg) | 3 | none |
| Empty screenshot | `EMPTY_SCREENSHOT` → runner returns (3, msg) | 3 | none |
| Size cap exceeded | `SIZE_CAP_EXCEEDED` → runner returns (3, msg) | 3 | none |
| Staging collision | `ValueError` → `main()` exit 2 | 2 | none |
| Packet writer exception | propagates → `main()` exit 3 | 3 | none (partial dir possible, see A-04) |

`limitation_notes` is always `[]` on `BrowserSnapshotSuccess`. The packet therefore carries no automatic limitation note for login walls, content walls, or bot-block pages — these are not detected by the adapter. The receipt non-claims and access_posture field (`"content sufficiency is not asserted"`) correctly disclose this. No fake clean capture.

**Q5 — Is the packet metadata sufficient without implying content sufficiency?**

Yes. The implementation uses:
- `access_posture = known_fact("browser_snapshot preserved rendered browser artifacts; content sufficiency is not asserted")` — explicit non-assertion.
- `media_posture = known_fact("browser_snapshot preserved a viewport screenshot; linked media files were not independently preserved")` — viewport-only scope explicit.
- `archive_posture = not_attempted(...)` — no archive claim.
- `screenshot_mode: "viewport"` in metadata dict — viewport scope machine-readable.
- `BROWSER_SNAPSHOT_NON_CLAIMS` list — 14 non-claims including "not content sufficiency proof", "not login or session capture", "not anti-detect behavior".
- Agent runbook explicitly instructs agents to report that the screenshot is viewport-only and does not prove content sufficiency or login-wall absence.

Metadata: **CLEAN**.

**Q6 — Are tests strong enough to catch regressions in the critical areas?**

Coverage map:

| Behavior | Test |
|---|---|
| Artifact writing (all 4 files in `raw/`) | `test_browser_snapshot_runner_writes_packet_with_four_artifacts` ✓ |
| Staging cleanup on success | same test ✓ |
| Staging cleanup on failure | `test_browser_snapshot_runner_cleans_staged_files_when_metadata_write_fails` ✓ |
| Exit 3 / no packet on capture failure | `test_browser_snapshot_runner_returns_3_without_packet_on_capture_failure` ✓ |
| Dependency absence (import isolation) | `test_browser_snapshot_module_imports_without_playwright_installed`, AST tests ✓ |
| Non-claims in receipt | `test_browser_snapshot_runner_writes_packet_with_four_artifacts` ✓ |
| Limitation travel to manifest | same test ✓ |
| Size cap failure | `test_fetch_browser_snapshot_capture_returns_size_cap_failure` ✓ |
| Timeout classification | `test_fetch_browser_snapshot_capture_classifies_timeout` ✓ |
| Redirect warning | `test_fetch_browser_snapshot_capture_with_fake_engine_preserves_browser_artifacts` ✓ |
| Metadata fields (viewport, wait_until, screenshot_mode) | same test ✓ |
| `EMPTY_RENDERED_DOM` failure | **MISSING** — see M-02 |
| `EMPTY_SCREENSHOT` failure | **MISSING** — see M-02 |
| `visible_text` silent empty fallback | **MISSING** — consequence of M-01 |
| URL validation error (non-HTTP scheme) | **MISSING** |
| `wait_until` validation error | **MISSING** |
| Staging collision error | **MISSING** |
| `screenshot_mode: viewport` in manifest | partial (metadata dict tested, not manifest field) |

The missing tests for `EMPTY_RENDERED_DOM` and `EMPTY_SCREENSHOT` are the highest-risk gap — these failure kinds have zero coverage despite being reachable with existing `_FakeBrowserEngine` infrastructure.

**Q7 — Do the docs correctly update runbook/toolbox status without over-authorizing session/login browser reuse?**

Yes. All three updated docs are consistent:

- `source_capture_toolbox/README.md`: "Logged-in or entitled browser session reuse remains a later extension that needs its own contract." Build order: "Done for anonymous/headless v0."
- `source_capture_agent_runbook.md`: Explicit stop instruction for login-visible content; runner selection table shows "none yet" for login-visible sessions; per-runner footer reiterates no stored sessions/profiles/cookies.
- `orca-harness/README.md`: "uses a fresh anonymous/headless browser context and does not accept stored sessions, browser profiles, cookies, credentials, storage-state files, anti-detect behavior, proxy behavior, CAPTCHA solving."
- `source_capture_packet.md`: "does not accept or load stored sessions, browser profiles, cookies, credentials, or storage-state files."

No over-authorization found. The logged-in/entitled extension is consistently described as deferred. **CLEAN**.

**Q8 — Is `playwright` as optional dependency in `pyproject.toml` the right shape?**

Yes. `[project.optional-dependencies] browser = ["playwright>=1.44,<2"]` is the standard Python packaging pattern. `pip install orca-harness[browser]` installs Playwright; bare `pip install orca-harness` does not. This matches the lazy-import design. The version bound `>=1.44,<2` is appropriate for a v0 checkpoint.

The missing `playwright install chromium` step (A-01) is a documentation gap, not a packaging shape error. The shape is correct.

**Q9 — Is viewport-only screenshot acceptable as v0 given the docs' wording?**

Yes, with the observed caveats documented. The behavior contract specifically says "viewport screenshot." Code: `page.screenshot(type="png", full_page=False)`. Metadata: `screenshot_mode: "viewport"`. Agent runbook and receipt non-claims both instruct that the screenshot does not prove content sufficiency. For pages with below-the-fold content, the rendered DOM (`page.content()`) and visible text (`inner_text()` on `body`) capture full content; only the screenshot is viewport-limited. The trade-off is acceptable for v0 given explicit disclosure.

Full-page screenshot was likely deferred intentionally (large pages would frequently hit the 5 MB size cap). No recommendation to change for v0.

**Q10 — Any blocker/major issue before commit?**

No blockers. No majors. The two minor findings (M-01 silent empty visible_text, M-02 missing EMPTY_RENDERED_DOM and EMPTY_SCREENSHOT tests) are fixable before or after commit at the team's discretion. Neither creates a fake success path, a boundary violation, or a missing-packet disguised as a packet.

---

## Summary Assessment

### What Was Reviewed

Browser Snapshot Adapter v0 for the Orca Source Capture Toolbox. Implementation adds:
- `orca-harness/source_capture/adapters/browser_snapshot.py` — adapter core with lazy Playwright engine
- `orca-harness/runners/run_source_capture_browser_packet.py` — CLI runner
- `orca-harness/tests/unit/test_source_capture_browser_snapshot.py` — unit tests
- `orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py` — import isolation and boundary contracts
- `orca-harness/source_capture/adapters/__init__.py` — updated to export browser adapter
- `orca-harness/pyproject.toml` — optional `browser` dependency group
- Documentation updates to toolbox README, runbook, packet doc, harness README

### What Holds

- **v0 boundary preserved**: anonymous/headless only; no stored sessions, cookies, credentials, storage-state, anti-detect, proxy, CAPTCHA, crawling, OCR.
- **Dependency isolation correct**: Playwright is lazy-imported; importing the adapters package or any non-browser runner does not require Playwright.
- **Exit code mapping correct**: exit 0 = packet written; exit 2 = CLI/user/config error; exit 3 = browser failure / no packet.
- **No fake success paths**: every failure path returns a `BrowserSnapshotFailure` or raises; the packet is never created on failure.
- **Staging cleanup correct on success and failure**: `finally` block cleans all written staging files.
- **Metadata non-claims correct**: content sufficiency not asserted; viewport-only screenshot disclosed; non-claims list comprehensive.
- **Docs consistent**: logged-in/entitled session reuse correctly described as deferred; runbook stop instructions clear.
- **Optional dependency shape correct**: `[browser]` extras group is the right packaging pattern.

### Findings Table

| ID | Severity | Location | Summary |
|---|---|---|---|
| M-01 | Minor | `browser_snapshot.py:215–218` | `visible_text` extraction failure silently produces empty output with no warning note |
| M-02 | Minor | `test_source_capture_browser_snapshot.py` | No unit tests for EMPTY_RENDERED_DOM or EMPTY_SCREENSHOT failure kinds |
| A-01 | Advisory | README, runbook, packet doc | `playwright install chromium` step missing from docs; absent binary gives CAPTURE_FAILED instead of DEPENDENCY_UNAVAILABLE |
| A-02 | Advisory | `test_source_capture_browser_snapshot_contract.py:21–25` | Runtime import isolation test does not enforce Playwright absence; static AST tests are more rigorous |
| A-03 | Advisory | `browser_snapshot.py:203–228` | Browser context not explicitly closed before `browser.close()` |
| A-04 | Advisory | `run_source_capture_browser_packet.py` | Partial output directory possible if packet writer fails mid-write (inherent adapter contract, shared with other adapters) |
| A-05 | Advisory | `browser_snapshot.py:244–248` | URL validator permits `http://user:pass@host` form; embedded credentials passed to browser silently |
| A-06 | Advisory | `browser_snapshot.py:219` | `page.screenshot()` timeout not governed by `timeout_seconds` parameter; Playwright's 30s default applies independently |

### Recommendation

**`accept_with_advisory_findings`**

The implementation is correct and boundary-clean for v0. The two minor findings (M-01, M-02) do not block commit — M-01 weakens observable fidelity for one edge case but does not create a fake success path; M-02 leaves two failure kinds untested but both already return the correct exit-3 / no-packet behavior. Advisory findings are polish items.

If the team wants to address findings before commit, M-02 is lowest effort (two fake-engine test cases using existing infrastructure) and highest value for regression resistance.

---

## Non-Claims

This review does not patch, commit, install Playwright, run a live browser capture, approve source-access legality for any specific URL, validate capture quality, authorize logged-in or session browser reuse, or establish ECR, Cleaning, or Judgment readiness. It does not amend the source-access boundary, obligation contract, or build authorization. Findings are advisory to the owner/operator; acceptance or remediation decisions belong to the owner.
