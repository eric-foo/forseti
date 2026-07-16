# Source Capture Browser Snapshot Playwright Path — Operational Blast-Radius Adversarial Review

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Post-smoke adversarial operational blast-radius review of the Browser Snapshot Playwright
  integration for the Orca Source Capture Toolbox. Reviews adapter code, CLI runner,
  pyproject.toml package discovery, docs/runbook, tests, prior review, and real install + smoke evidence.
use_when:
  - Inspecting Playwright-path operational blast-radius findings.
  - Tracing Browser Snapshot operational decisions to this review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
review_type: adversarial_operational_blast_radius_review
review_date: 2026-06-03
reviewer: Claude Sonnet 4.6 (automated adversarial review; read-only)
worktree: C:/Users/vmon7/Desktop/projects/orca
expected_branch: main
expected_head: a8c6a48
hash_verification: ALL_PASSED (15/15)
edit_permission: none — read-only review; no patches applied
prior_review: docs/review-outputs/source_capture_browser_snapshot_adapter_adversarial_code_review_v0.md
```

---

## Preflight: Hash Verification

All 15 target files verified before review commenced.

```text
VERIFIED SOURCE FILES (9/9):
  OK  orca-harness/pyproject.toml
  OK  orca-harness/source_capture/adapters/browser_snapshot.py
  OK  orca-harness/runners/run_source_capture_browser_packet.py
  OK  orca-harness/tests/unit/test_source_capture_browser_snapshot.py
  OK  orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py
  OK  orca-harness/docs/source_capture_agent_runbook.md
  OK  orca-harness/docs/source_capture_packet.md
  OK  docs/product/source_capture_toolbox/README.md
  OK  docs/review-outputs/source_capture_browser_snapshot_adapter_adversarial_code_review_v0.md

VERIFIED SMOKE PACKET FILES (6/6):
  OK  orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/manifest.json
  OK  orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/receipt.md
  OK  orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/raw/01_browser_rendered_dom.html
  OK  orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/raw/02_browser_visible_text.txt
  OK  orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/raw/03_browser_viewport_screenshot.png
  OK  orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/raw/04_browser_snapshot_metadata.json
```

No mismatches. Review proceeds.

## Preflight: Branch and HEAD

- Branch: `main` — matches spec.
- HEAD: `a8c6a48 fix: declare harness package discovery` — matches spec.
- Dirty state: non-target overlay/docs files only; all target source files are clean at HEAD.

---

## Prior Review Findings Status

The prior review (`source_capture_browser_snapshot_adapter_adversarial_code_review_v0.md`) ran against the same HEAD before install and smoke. It found two minors and six advisories. Their status at the current verified HEAD:

| ID | Prior Severity | Prior Finding | Status at HEAD |
|---|---|---|---|
| M-01 | Minor | `visible_text` extraction failure silently produced empty output with no warning note | **PATCHED** — `except` branch now appends `warning_notes` entry |
| M-02 | Minor | No tests for `EMPTY_RENDERED_DOM` or `EMPTY_SCREENSHOT` failure kinds | **PATCHED** — both tests now present in unit test file |
| A-01 | Advisory | `playwright install chromium` step absent from docs | **PATCHED** — both install steps present in runbook and packet.md |
| A-02 | Advisory | Runtime import isolation test does not enforce Playwright absence | **OPEN** — advisory only; static AST tests remain the reliable gate |
| A-03 | Advisory | Browser context not explicitly closed before `browser.close()` | **PATCHED** — `context.close()` now in dedicated `finally` block |
| A-04 | Advisory | Partial output directory possible if packet writer fails mid-write | **OPEN** — acknowledged inherent adapter contract, shared with all adapters |
| A-05 | Advisory | URL validator permitted `http://user:pass@host` form | **PATCHED** — `_validate_http_url` now explicitly rejects embedded credentials |
| A-06 | Advisory | `page.screenshot()` timeout not governed by `timeout_seconds` | **PATCHED** — `timeout=timeout_ms` now passed to `page.screenshot()` |

Six of eight prior findings have been addressed. The two remaining open items (A-02, A-04) are advisory-only and acknowledged inherent limitations.

---

## New Findings

### O-M01 — Minor: WinError 5 (Windows subprocess-launch denial) not documented in runbook or packet.md

**Evidence**: Operational smoke evidence from this review turn:
```yaml
first_local_smoke:
  result: failed
  exit_code: 3
  error: "WinError 5 Access is denied while Playwright tried to create its driver subprocess"
  packet_written: false
escalated_local_smoke:
  result: succeeded
  exit_code: 0
  packet_written: true
```

**Code behavior under WinError 5** (`browser_snapshot.py`):
1. `playwright.chromium.launch(headless=True)` raises an `OSError` / `PermissionError` with "WinError 5 Access is denied".
2. `_looks_like_missing_browser_binary` (lines 291–297) checks for: `"executable doesn't exist"`, `"browser has not been installed"`, `"playwright install"`. None match "WinError 5 Access is denied".
3. The exception falls through to the outer `except Exception as exc` in `fetch_browser_snapshot_capture` (line 108).
4. `_failure_kind_from_exception` returns `CAPTURE_FAILED` (no "timeout" in "WinError 5").
5. Runner returns `(3, "Browser snapshot capture failed: [WinError 5] Access is denied: ...")` — exit 3, no packet.

**Failure visibility**: Correct. Exit 3, no fake packet, error message is visible and contains the WinError 5 text. The failure KIND is `CAPTURE_FAILED` rather than `DEPENDENCY_UNAVAILABLE`, which is technically imprecise (Playwright and Chromium ARE installed; it's a process launch permission issue), but this does not create a fake success path or a hidden failure. The operator sees the error.

**Documentation gap**: Neither `source_capture_agent_runbook.md` nor `source_capture_packet.md` mentions this Windows-specific behavior. An agent hitting WinError 5 after successful `pip install` and `playwright install chromium` will see exit 3 with an unfamiliar error and will not know:
- That this is a Windows process isolation / sandbox permission issue, not an installation failure.
- That operator escalation or running in a higher-privilege context may resolve it.
- That AGENTS.md requires per-operation approval for sandbox escalation (not a standing rule).

**Impact**: Agents cannot self-diagnose. They will report `CAPTURE_FAILED` exit 3 without knowing the remediation. The caveat is operationally necessary to document before treating this path as agent-reusable on Windows.

**Recommendation**: Add a short note in the Browser Snapshot section of `source_capture_agent_runbook.md` (and optionally `source_capture_packet.md`) stating: on Windows, a `WinError 5 Access is denied` error means the browser subprocess launch was denied by the OS or sandbox; the operator must ensure the environment permits subprocess creation before retrying. Patch-queue handoff not authorized by this review lane; recommendation is advisory.

---

### O-A01 — Advisory: `visible_text_byte_count` and `rendered_dom_byte_count` in metadata are 1 byte less than corresponding file sizes

**Evidence from verified smoke packet**:
```text
manifest preserved_files[1].size_bytes = 77
metadata visible_text_byte_count      = 76  (diff: -1)

manifest preserved_files[0].size_bytes = 213
metadata rendered_dom_byte_count       = 212  (diff: -1)

manifest preserved_files[2].size_bytes = 11938
metadata screenshot_byte_count         = 11938  (diff: 0, consistent)
```

**Code path** (`run_source_capture_browser_packet.py`, lines 130–134):
```python
artifact_sizes = {
    "rendered_dom": len(engine_result.rendered_dom.encode("utf-8")),
    "visible_text": len(engine_result.visible_text.encode("utf-8")),
    "screenshot_png": len(engine_result.screenshot_png),
}
```

Then (`run_source_capture_browser_packet.py` line 190):
```python
def _write_text(path: Path, text: str) -> None:
    path.write_text(f"{text}\n", encoding="utf-8", newline="\n")
```

`artifact_sizes` is computed on the raw string before writing. `_write_text` appends a trailing `\n` to produce a clean-file-format text file. The resulting file is always 1 byte larger than the `rendered_dom_byte_count` / `visible_text_byte_count` fields in the metadata dict. The binary screenshot uses `write_bytes` directly, so its byte count is exact.

**Hashes are not affected**: the manifest's SHA256 hashes are computed on the actual written files, not the raw strings. The SHA256 values in manifest and receipt are consistent with actual file sizes.

**Impact**: An agent cross-referencing `visible_text_byte_count` from `raw/04_browser_snapshot_metadata.json` against `size_bytes` from `manifest.json` for file_02 will observe a 1-byte discrepancy. For most uses (empty-check, rough size check) this does not matter. A strict byte-count comparator would see a mismatch. The discrepancy is systematic, consistent, and reproducible from the code.

**Not a correctness issue**; packet integrity is verified by SHA256 hash. Advisory notation only.

---

### O-A02 — Advisory (inherited A-02): Runtime import isolation test name is misleading

**Status**: Open from prior review. Not patched. Advisory only. Static AST contract tests (`test_only_browser_snapshot_surfaces_name_playwright_dependency`, `test_browser_snapshot_adapter_avoids_scraper_api_proxy_and_webbrowser_imports`) remain the reliable boundary gate. The runtime test (`test_browser_snapshot_module_imports_without_playwright_installed`) passes regardless of whether Playwright is installed, because it only checks that the module is importable — not that Playwright is absent. The test name is misleading but the gap does not create a safety or correctness risk.

---

### O-A03 — Advisory (inherited A-04): Partial output directory possible if packet writer fails mid-write

**Status**: Open from prior review. Not patched. This is an acknowledged inherent limitation of the current packet-writer contract, shared by all four network adapters (Direct HTTP, Media/Asset, Archive.org, Browser Snapshot). No regression introduced by Browser Snapshot. Advisory only.

---

## Review Questions

### Q1 — Is the Browser Snapshot Playwright path safe enough for bounded agent use?

**Yes, with documented caveat.**

The path is safe for bounded agent use within its declared scope:

- Boundary: anonymous/headless only. `browser.new_context(viewport=...)` with no `storage_state`, `http_credentials`, `cookies`, `proxy`, or `user_agent` override. Fresh, isolated context. `headless=True` explicit. No anti-detect, no proxy, no CAPTCHA, no crawling, no OCR.
- No fake success packets. Exit 3 / no packet on all failure paths (confirmed by code + smoke).
- Failure visibility preserved. WinError 5 produces visible exit 3 with the actual OS error message.
- Non-claims list (14 items) is comprehensive and present in every packet.
- All prior review minor findings patched.

**Known requirement**: on Windows, real browser execution may require subprocess-launch permission or elevated context (WinError 5 behavior). This is not documented in the runbook or packet.md. Agents must be told that this error means process isolation is preventing subprocess launch, not an installation failure. Per AGENTS.md, sandbox escalation requires per-operation approval and must not become a standing rule.

**Verdict**: OPERATIONALLY SAFE with minor documentation patch needed.

---

### Q2 — Does `pyproject.toml` explicit package discovery correctly fix the editable install failure?

**Yes. Fix is correct and minimal.**

The fix adds:
```toml
[tool.setuptools]
py-modules = ["harness_utils"]

[tool.setuptools.packages.find]
include = [
  "runners",
  "schemas",
  "scoring",
  "source_capture",
  "source_capture.*",
  "source_observability",
]
```

Analysis:

- **Root cause of failure**: setuptools flat-layout auto-discovery found many top-level directories and refused to proceed with the editable build. The explicit `include` allowlist overrides auto-discovery.
- **Allowlist is narrow and correct**: only Python source packages are included. `_test_runs/`, `reports/`, `docs/`, and `tests/` are excluded.
- **`source_capture.*`** picks up `source_capture.adapters` and other subpackages correctly.
- **`harness_utils` as `py-modules`**: correctly handles the single-file utility module that is not a package directory.
- **`tests/` absent from include**: correct. Tests are not installed packages; they reference `source_capture` and `runners` via the editable install.
- **No accidental scratch/report inclusion**: `_test_runs/`, `reports/source_capture/`, and all `docs/` paths are outside the allowlist.
- **Smoke evidence confirms**: `pip install -e ".[browser]"` succeeded after this patch, and `python -m pytest` reached 67 passed.

**Verdict**: CORRECT and MINIMAL. No over-inclusion risk.

---

### Q3 — Do the docs/runbook accurately tell future agents what is required to install, run, stop, and report Browser Snapshot captures?

**Substantially yes, with one gap.**

**What is accurate:**

1. Both install steps are present in `source_capture_agent_runbook.md` and `source_capture_packet.md`:
   ```powershell
   python -m pip install -e .[browser]
   python -m playwright install chromium
   ```
   This addresses prior review A-01.

2. Runner command form is correct and operational (verified by successful smoke).

3. Exit codes are accurately documented:
   | Code | Meaning |
   |---|---|
   | 0 | packet written |
   | 2 | CLI/user/config error |
   | 3 | missing Playwright, missing Chromium binary, navigation failure, artifact failure; no packet |

4. Post-run inspection steps and agent report template are present and accurate.

5. Session/login stop instruction is clear: "stop with `visible_capture_limitation`" for login-visible or entitled content.

6. Non-claims and boundary are accurately stated: no stored sessions, no profiles, no cookies, no credentials, no storage-state, no anti-detect, no proxy, no CAPTCHA, no crawling, no OCR.

**Gap (O-M01)**: The `WinError 5 Access is denied` Windows subprocess-launch failure is not documented. An agent on Windows that has Playwright and Chromium correctly installed but hits this error will receive an unfamiliar exit-3 message without guidance. The remediation (subprocess-launch permission / elevated context, per-operation approval per AGENTS.md) is not described.

**Verdict**: ACCURATE with one minor gap (O-M01).

---

### Q4 — Does the adapter preserve failure visibility?

**Yes. No fake success paths.**

Complete failure path trace (all verified against code):

| Failure Mode | Handler | Exit Code | Packet Written |
|---|---|---|---|
| URL: non-http scheme or missing netloc | `ValueError` → `main()` exit 2 | 2 | none |
| URL: embedded credentials | `ValueError` → `main()` exit 2 | 2 | none |
| `wait_until` invalid | `ValueError` → `main()` exit 2 | 2 | none |
| Playwright module not installed | `DEPENDENCY_UNAVAILABLE` → runner (3, msg) | 3 | none |
| Chromium binary absent (standard error text) | `DEPENDENCY_UNAVAILABLE` → runner (3, msg) | 3 | none |
| WinError 5 subprocess-launch denied | `CAPTURE_FAILED` → runner (3, msg) | 3 | none |
| Navigation / browser exception | `CAPTURE_FAILED` or `TIMEOUT` → runner (3, msg) | 3 | none |
| Empty rendered DOM | `EMPTY_RENDERED_DOM` → runner (3, msg) | 3 | none |
| Empty screenshot | `EMPTY_SCREENSHOT` → runner (3, msg) | 3 | none |
| Size cap exceeded | `SIZE_CAP_EXCEEDED` → runner (3, msg) | 3 | none |
| Staging collision | `ValueError` → `main()` exit 2 | 2 | none |
| Packet writer mid-write exception | propagates → `main()` exit 3 | 3 | none (partial dir possible; see O-A03) |

**Visible_text extraction failure (M-01, now patched)**: When `page.locator("body").inner_text()` raises, the exception is caught, `visible_text` is set to `""`, and a warning note is appended to `warning_notes`: `"browser_snapshot visible_text extraction failed: {exc}"`. This warning travels through `BrowserSnapshotSuccess.warning_notes` into the packet manifest. The packet is not a fake success — the DOM and screenshot are still preserved, but the text extraction limitation is now disclosed.

**WinError 5 classification nuance**: The failure kind is `CAPTURE_FAILED` rather than `DEPENDENCY_UNAVAILABLE` because `_looks_like_missing_browser_binary` does not match "WinError 5" text. The failure is correctly captured at exit 3 with a visible message. The KIND classification is slightly imprecise but does not create a hidden or fake result.

**Verdict**: FAILURE VISIBILITY PRESERVED. No hidden downgrade, no fake packet, no exit-0 on failure.

---

### Q5 — Does the smoke packet demonstrate the intended path?

**Yes. Fully demonstrated.**

Smoke packet `browser_snapshot_smoke_packet_29c68de1` (verified against all 6 SHA256 hashes):

| Artifact | File | Size | Verified |
|---|---|---|---|
| Rendered DOM | `raw/01_browser_rendered_dom.html` | 213 bytes | SHA256 OK |
| Visible text | `raw/02_browser_visible_text.txt` | 77 bytes | SHA256 OK |
| Viewport screenshot | `raw/03_browser_viewport_screenshot.png` | 11,938 bytes | SHA256 OK |
| Browser metadata | `raw/04_browser_snapshot_metadata.json` | 437 bytes | SHA256 OK |
| Manifest | `manifest.json` | — | SHA256 OK |
| Receipt | `receipt.md` | — | SHA256 OK |

**Content verification**:
- `rendered_dom`: Full rendered HTML with `<html>`, `<head>`, `<body>`, `<main>`, `<h1>`, `<p id="marker">` — not an empty shell.
- `visible_text`: Contains `"source-visible loopback smoke marker 2026-06-03"` — the smoke page's date-stamped marker is correctly captured as visible text.
- `screenshot_png`: 11,938 bytes — non-trivial binary, non-empty image file.
- `metadata.json`: All expected fields present: `requested_url`, `final_url`, `title`, `capture_timestamp`, `timeout_seconds`, `wait_until`, `viewport_width`, `viewport_height`, `screenshot_mode: "viewport"`, `rendered_dom_byte_count`, `visible_text_byte_count`, `screenshot_byte_count`.
- `manifest.json`: 14 non-claims present, `source_surface: browser_snapshot`, `capture_mode: multimodal`, correct postures (access, archive, media, recapture), `source_slices[0].slice_id: browser_snapshot_01`, all four `preserved_file_ids` listed.
- `receipt.md`: All 14 non-claims present; timing, posture, and preserved file inventory correct.
- `warning_notes: []` in manifest — visible_text extraction succeeded cleanly on the loopback page.

**Verdict**: SMOKE DEMONSTRATES INTENDED PATH. All four artifacts present, correct structure, content verified.

---

### Q6 — Are non-claims and boundaries preserved?

**Yes. Clean.**

14 non-claims present in every verified packet:
```text
not content sufficiency proof
not login or session capture
not stored profile or cookie use
not anti-detect behavior
not proxy or session injection
not CAPTCHA solving
not crawler or source discovery
not API SDK use
not OCR or image analysis
not ECR design
not Cleaning implementation
not Judgment scoring
not buyer proof
not commercial-readiness logic
```

These match `BROWSER_SNAPSHOT_NON_CLAIMS` in the runner exactly, and are verified in the test `test_browser_snapshot_runner_writes_packet_with_four_artifacts`.

**Adapter code boundary**: `browser.new_context(viewport=...)` with no `storage_state`, `http_credentials`, `cookies`, `proxy`, `user_agent` override, or `bypass_csp`. Fresh anonymous context. No network interception, no JavaScript injection, no credential use. Boundary is clean.

**No ECR/Cleaning/Judgment references in code**: contract test `test_browser_snapshot_adapter_avoids_scraper_api_proxy_and_webbrowser_imports` verifies via AST walk that forbidden imports are absent. `test_only_browser_snapshot_surfaces_name_playwright_dependency` verifies Playwright reference is contained to `browser_snapshot.py` only.

**Logged-in/entitled extension**: consistently described as deferred across all docs (`"none yet"` in runner selection table; `"stop with visible_capture_limitation"` instruction; toolbox README build order shows deferred). No over-authorization.

**Verdict**: NON-CLAIMS AND BOUNDARIES PRESERVED.

---

### Q7 — Does the sandbox WinError 5 behavior need code or docs changes?

**Code: no change required. Docs: minor note needed.**

**Code analysis**:

The current behavior is acceptable:
- WinError 5 produces exit 3 (no packet) with a visible error message.
- The message contains the raw OS error text: `"[WinError 5] Access is denied: ..."` — which is actionable for an operator who understands Windows process isolation.
- Adding pattern-matching for "WinError 5" or "access is denied" to `_looks_like_missing_browser_binary` would change the failure kind from `CAPTURE_FAILED` to `DEPENDENCY_UNAVAILABLE`. This would be marginally more accurate semantically (it IS an environment issue, not a capture issue), but it risks false-positive reclassification of other legitimate "access denied" scenarios (e.g., network permission denied when fetching a URL — though that would be a navigation error, not a launch error). The current behavior does not create a fake success path, and the distinction between `CAPTURE_FAILED` and `DEPENDENCY_UNAVAILABLE` does not affect operator decision-making in this case (both mean "try again after fixing the environment"). No code change is the right call here.

**Docs gap**:
An agent following the runbook that installs Playwright and Chromium correctly will not understand WinError 5. The runbook currently says exit 3 means "missing Playwright package, missing Chromium binary, navigation failure, or artifact failure" — WinError 5 is none of these, so the runbook's exit-code table gives no guidance. The remediation (subprocess-launch permission or elevated context, per-operation approval per AGENTS.md) should be a visible note in the Browser Snapshot section of the runbook.

**Verdict**: CODE ACCEPTABLE AS-IS. DOCS NEED MINOR CAVEAT NOTE (O-M01).

---

### Q8 — Is there any reason to recommend a Puppeteer spike now?

**No.**

**Analysis**:

The friction observed during this install-and-smoke cycle:
1. `pyproject.toml` flat-layout auto-discovery failure → fixed with one-commit allowlist patch.
2. Separate `playwright install chromium` step → documented and working.
3. `WinError 5` subprocess-launch denial on first run → resolved with elevated context.

None of these friction points are Playwright-specific API problems. All three would occur identically with Puppeteer:
- Puppeteer is Node.js-based; adding a Node.js dependency to a Python project would increase operational surface substantially.
- Puppeteer also requires a separate browser binary installation step.
- Puppeteer also spawns browser subprocesses; WinError 5 (OS-level subprocess-launch denial) would affect any browser automation tool.
- A Puppeteer integration would require calling Node.js from Python or rewriting the adapter layer in JavaScript, neither of which is within the declared v0 scope.

The Playwright Python API is clean and well-supported for the anonymous/headless use case. The installed Playwright version (1.60.0, within the `>=1.44,<2` pin) is stable.

**Verdict**: NO REASON TO RECOMMEND PUPPETEER SPIKE. Observed friction is environment setup friction, not Playwright API friction.

---

### Q9 — Are there any blocker or major issues before calling Browser Snapshot operational for local agent use?

**No blockers. No majors.**

Evidence:
- 13/13 unit and contract tests pass.
- 67/67 full source-capture stack tests pass.
- Smoke packet produced, verified, and content-confirmed.
- All prior review minor findings patched.
- Boundary clean: anonymous/headless, no stored sessions, no fake success paths.
- Package discovery fix correct and minimal.
- Non-claims comprehensive and verified.

Remaining open items are advisory only:
- O-M01 (docs caveat for WinError 5): minor docs gap; does not break the path, does not hide failures.
- O-A01 (byte count off-by-one in metadata): systematic, non-blocking, SHA256 hashes are correct.
- O-A02 (inherited A-02): misleading test name; static AST tests are the reliable gate.
- O-A03 (inherited A-04): partial directory on mid-write failure; inherent adapter contract.

**Verdict**: NO BLOCKERS. NO MAJORS. PATH IS OPERATIONAL FOR LOCAL AGENT USE with minor docs patch (O-M01) recommended before agents operate autonomously on Windows.

---

## Summary Assessment

### What Was Reviewed

Browser Snapshot Playwright operational path end-to-end:
- `orca-harness/source_capture/adapters/browser_snapshot.py` — adapter core
- `orca-harness/runners/run_source_capture_browser_packet.py` — CLI runner
- `orca-harness/pyproject.toml` — optional dependency declaration, package discovery fix
- `orca-harness/docs/source_capture_agent_runbook.md` — agent-facing runbook
- `orca-harness/docs/source_capture_packet.md` — packet boundary docs
- `docs/product/source_capture_toolbox/README.md` — toolbox product docs
- `orca-harness/tests/unit/test_source_capture_browser_snapshot.py` — unit tests
- `orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py` — contract tests
- `docs/review-outputs/source_capture_browser_snapshot_adapter_adversarial_code_review_v0.md` — prior review
- `orca-harness/_test_runs/browser_snapshot_smoke_packet_29c68de1/` — real smoke packet (6 files)

### What Holds

- **Prior review minor findings patched**: M-01 (visible_text warning), M-02 (EMPTY_RENDERED_DOM / EMPTY_SCREENSHOT tests).
- **Prior review most advisory findings patched**: A-01 (install docs), A-03 (context.close()), A-05 (credential URL rejection), A-06 (screenshot timeout).
- **v0 boundary clean**: anonymous/headless only; no stored sessions, cookies, credentials, storage-state, anti-detect, proxy, CAPTCHA, crawling, OCR.
- **Dependency isolation correct**: Playwright lazy-imported inside engine; adapter stack importable without Playwright installed; AST contract tests guard the boundary.
- **Exit code mapping correct**: 0 = packet written; 2 = CLI/user/config error; 3 = browser/capture failure, no packet.
- **No fake success paths**: every failure path returns `BrowserSnapshotFailure` or raises; packet never written on failure.
- **Staging cleanup correct**: `finally` block cleans all written staging files on success and failure.
- **Package discovery fix correct**: explicit allowlist excludes `_test_runs/`, `reports/`, `docs/`, `tests/`.
- **Smoke demonstrates the full intended path**: all 4 artifacts present, SHA256-verified, content-confirmed including the date-stamped smoke marker.
- **Non-claims comprehensive**: 14 non-claims in receipt and manifest.
- **Docs install steps accurate**: both `pip install` and `playwright install chromium` present.

### Findings Table

| ID | Severity | Location | Summary |
|---|---|---|---|
| O-M01 | Minor | runbook, packet.md | WinError 5 Windows subprocess-launch caveat not documented; agents cannot self-diagnose or know remediation path |
| O-A01 | Advisory | browser_snapshot.py runner, metadata | `visible_text_byte_count` and `rendered_dom_byte_count` are 1 byte less than file sizes due to `_write_text` trailing-newline; SHA256 hashes are consistent with actual files |
| O-A02 | Advisory (inherited) | contract test | Runtime import isolation test does not enforce Playwright absence; static AST tests are the reliable gate |
| O-A03 | Advisory (inherited) | runner | Partial output directory possible if packet writer fails mid-write; inherent adapter contract, shared with all adapters |

### Prior Findings Closure

| Prior ID | Severity | Disposition |
|---|---|---|
| M-01 | Minor | CLOSED — patched |
| M-02 | Minor | CLOSED — patched |
| A-01 | Advisory | CLOSED — patched |
| A-02 | Advisory | CARRIED as O-A02 |
| A-03 | Advisory | CLOSED — patched |
| A-04 | Advisory | CARRIED as O-A03 |
| A-05 | Advisory | CLOSED — patched |
| A-06 | Advisory | CLOSED — patched |

### Recommendation

**`operational_accept_with_minor_patches`**

The Browser Snapshot Playwright path is correct, boundary-clean, failure-visible, and smoke-verified for local bounded agent use. The single new minor finding (O-M01) is a documentation gap only — the code handles WinError 5 correctly (exit 3, no fake packet, visible error message) but the runbook does not tell agents what the error means or how to escalate. This gap matters for Windows-hosted agents operating autonomously. The patch is a short prose note in the runbook's Browser Snapshot section; no code change is required.

All prior review minor findings have been addressed. No reason to recommend a Puppeteer spike. No reason to block agent use on the code or boundary plane.

---

## Non-Claims

This review does not patch, commit, install Playwright, run any live browser capture, approve source-access legality for any specific URL, validate capture quality, authorize logged-in or session browser reuse, grant ECR/Cleaning/Judgment readiness, or amend the source-access boundary, obligation contract, or build authorization. Findings are advisory to the owner/operator; acceptance or remediation decisions belong to the owner. This review was performed read-only against verified file hashes.
