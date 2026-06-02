# Source Capture Authenticated Browser Snapshot Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Adversarial code review of the Authenticated Browser Snapshot v0 implementation (auth_state.py, browser_snapshot.py extension, authenticated packet runner, bootstrap runner, tests, docs).
use_when:
  - Owner or implementer deciding whether to commit the Authenticated Browser Snapshot v0 implementation.
  - Routing findings to a patch or rerun.
authority_boundary: review_output_only
```

---

## Preflight Record

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Source Capture Toolbox authenticated browser snapshot implementation review
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: main
  expected_head_short: d868fc2
  dirty_state_checked: yes
  dirty_state_allowance: >
    Review target files are intentionally modified/untracked.
    Unrelated Orca dirty/untracked files are out of scope.
  edit_permission: read-only review; report-write only to required_output_path
  output_mode: review-report
  required_output_path: docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md
```

---

## Hash Pin Verification

All 13 target file hashes were verified against the pinned values in the prompt.

```text
RESULT: ALL 13 HASH PINS VERIFIED — NO MISMATCH
```

| File | Pin Matched |
|---|---|
| `.gitignore` | ✓ |
| `docs\product\source_capture_toolbox\README.md` | ✓ |
| `orca-harness\README.md` | ✓ |
| `orca-harness\docs\source_capture_agent_runbook.md` | ✓ |
| `orca-harness\docs\source_capture_packet.md` | ✓ |
| `orca-harness\source_capture\auth_state.py` | ✓ |
| `orca-harness\source_capture\__init__.py` | ✓ |
| `orca-harness\source_capture\adapters\browser_snapshot.py` | ✓ |
| `orca-harness\runners\run_source_capture_authenticated_browser_packet.py` | ✓ |
| `orca-harness\runners\run_source_capture_browser_session_bootstrap.py` | ✓ |
| `orca-harness\tests\unit\test_source_capture_browser_snapshot.py` | ✓ |
| `orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py` | ✓ |
| `orca-harness\tests\contract\test_source_capture_browser_snapshot_contract.py` | ✓ |

---

## Source Context Declaration

```text
SOURCE_CONTEXT_READY
```

All required authority files (`AGENTS.md`, overlay sections, source-access boundary decision, method plan, build authorization, obligation contract, toolbox README, runbook, packet docs) and all 13 target implementation files were loaded and read before this review began. No required source is missing or unreadable.

---

## Method Application Declarations

- `workflow-deep-thinking` APPLIED: failure-mode framing executed before findings.
- `workflow-code-review` APPLIED: adversarial posture over implementation, tests, and docs.

---

## Deep-Thinking: Failure Mode Framing

Before listing findings, this section captures the primary risk dimensions and the adversarial model that shaped the finding search.

### Risk Dimension 1 — Credential / Session-State Leakage

The highest-stakes failure mode: storage-state JSON, cookie values, tokens, or localStorage values appearing in `manifest.json`, `receipt.md`, raw packet files (`01_*.html`, `02_*.txt`, `03_*.png`, `04_*.json`), stdout, stderr, exception tracebacks, test output, or documentation.

Leakage vectors to trace:
- `validate_auth_state_file` reads and parses the JSON (cookie values are in memory)
- `context_kwargs["storage_state"] = str(storage_state_path)` passes the path to Playwright
- Exception messages from Playwright or `json.JSONDecodeError` could carry path or content fragments
- `BrowserSnapshotSuccess.metadata` is written as a raw packet file
- `capture_context`, `access_posture`, and `visible_mode_changes` strings go into `manifest.json`

### Risk Dimension 2 — Path Traversal and File Placement

Auth-state files must stay exclusively under the ignored `_auth_state/` directory. Bypass could allow:
- writing credentials to the packet output directory (leaking into the packet)
- writing credentials to a git-tracked location
- reading attacker-controlled state from outside the auth directory

Defense layers to check: label regex, explicit path-separator check, `Path(label).name != label`, `_assert_under_root` with `relative_to()`.

### Risk Dimension 3 — Bootstrap Runner Contract (No Packet, No Credential CLI)

The bootstrap runner must write only local ignored storage-state JSON and nothing else. No `manifest.json`, `receipt.md`, `raw/`. No password/username/token/cookie CLI arguments.

### Risk Dimension 4 — Authenticated Packet Runner Failure Visibility

Failures must surface cleanly:
- missing/invalid auth state → exit 2, no packet
- browser failure → exit 3, no packet, staging files cleaned
- login wall visible → limitation recorded
- staging file collision → ValueError before write
- packet writer failure → staging files cleaned even if packet not written

### Risk Dimension 5 — Anonymous Browser Snapshot Compatibility

The `storage_state_path=None` code path must preserve exactly the previous anonymous behavior: fresh context, no session loading, `storage_state_loaded: False` in metadata.

### Risk Dimension 6 — Session Mode Vocabulary and Boundary Accuracy

Four fixed modes must align with source-access boundary doctrine. The mode recorded in the packet must accurately represent the session used.

### Risk Dimension 7 — Docs Over-Authorization

Docs must not authorize: password-driven login automation, direct profile/cookie import, anti-detect, proxy, CAPTCHA solving, API SDKs, scraper frameworks, no-entitlement bypass.

### Risk Dimension 8 — Provenance Misrepresentation via Mode Mismatch

The session mode at capture time is a declaration by the operator, not a binding validated against the storage-state file. If the operator bootstraps with mode A and captures with mode B, the packet records mode B regardless of the actual session origin. This affects disclosability accuracy.

### Risk Dimension 9 — Staging File Safety Under Failure

If the authenticated packet runner writes staging files (containing visible text from an authenticated session) and then the packet writer fails, those files must be cleaned up by the `finally` block. Uncleaned staging files containing authenticated session content represent a material leak risk.

### Risk Dimension 10 — Fake Success and ECR/Cleaning/Judgment Leakage

No code path may claim login-wall absence, content sufficiency, or emit ECR/Cleaning/Judgment fields.

---

## Findings

Ordered by severity. No `patch_queue_entry` is emitted; this is read-only review.

---

### MAJOR Findings

---

#### M-01 — Session Mode Not Bound to Auth-State File; Provenance Misrepresentation Risk

```yaml
finding_id: M-01
severity: major
```

**Location:**
- `orca-harness/runners/run_source_capture_browser_session_bootstrap.py:33–64` (`run_browser_session_bootstrap`)
- `orca-harness/source_capture/auth_state.py` (entire file)
- `orca-harness/runners/run_source_capture_authenticated_browser_packet.py:155–163` (mode-change string and access posture)

**Implementation Evidence:**

`run_browser_session_bootstrap` receives a `session_mode: AuthenticatedSessionMode` parameter. The parameter is used only in the success message string (`f"auth-state saved for {session_mode.value} at ..."`) and is NOT embedded in the storage-state JSON file written to `state_path`.

`context.storage_state(path=str(state_path))` writes Playwright's native JSON format (cookies, origins). There is no sidecar metadata file binding the mode to the file.

`validate_auth_state_file` does not check for or verify a mode field. It checks only that the file is valid JSON with `cookies: list` and `origins: list`.

At capture time, `run_source_capture_authenticated_browser_packet` receives `session_mode` from the CLI and records it in:
```python
mode_changes = [
    *visible_mode_changes,
    f"authenticated_browser_storage_state_loaded:{session_mode.value}:{state_label}",
]
access_posture = known_fact(
    f"authenticated_browser_snapshot used {session_mode.value} via ignored local Playwright storage state; ..."
)
```

The packet records whatever `session_mode` the operator passes at capture time, not what was declared at bootstrap time. There is no cross-check between the two.

**Authority / Evidence Basis:**

`docs/product/data_capture_source_access_boundary_decision_v0.md` (the source-access boundary decision) requires that Orca would "fully disclose how it was obtained" for every capture. The allowed session modes carry different disclosure implications:
- `free_account_created_session` → "a free account we created"
- `consenting_coworker_session` → "a coworker's account with their consent"
- `client_provided_session` → "client-provided credentials"

If a session bootstrapped as `consenting_coworker_session` is captured as `free_account_created_session`, the packet misrepresents the source-access method. This violates the disclosability requirement.

The obligation contract (`core_spine_v0_data_capture_spine_obligation_contract_v0.md`) Obligation 3 (Capture-Event Provenance) requires that "the capture mode is disclosed" and "material mode changes inside the session are visible." An undetected mode mismatch is a material mode-disclosure failure.

**Impact:**

A packet's `access_posture` and `visible_mode_changes` fields can claim a lower-entitlement session mode while the actual session used a higher-entitlement or consent-dependent mode. Downstream agents reading packets for source-access auditing receive incorrect provenance. At evidence-grade usage, this constitutes false provenance disclosure.

**Minimum Closure Condition:**

Either:
(a) A mode-binding sidecar file (e.g., `{state_label}.meta.json`) is written by the bootstrap runner so the capture runner can validate that the declared mode at capture time matches the declared mode at bootstrap time; OR
(b) The `source_capture_agent_runbook.md` and `source_capture_packet.md` explicitly document this as a known limitation with a non-claim: "session mode is an operator declaration at capture time; it is not validated against the bootstrap declaration; the packet records the capture-time declaration only."

**Next Authorized Action:**

Owner decision on whether to implement (a) or (b) before commit. This review does not authorize patching.

---

#### M-02 — No Staging-File Cleanup Test for Authenticated Runner on Packet-Write Failure

```yaml
finding_id: M-02
severity: major
```

**Location:**
- `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py` (absent)
- `orca-harness/runners/run_source_capture_authenticated_browser_packet.py:120–219` (the `finally` cleanup block)

**Implementation Evidence:**

The anonymous browser runner (`run_source_capture_browser_packet.py`) has a test `test_browser_snapshot_runner_cleans_staged_files_when_metadata_write_fails` (in `test_source_capture_browser_snapshot.py` lines 357–409) that injects a non-serializable object into metadata, triggers a `TypeError` during `json.dumps`, and verifies that all 4 staged files are deleted.

The authenticated runner has the structurally identical `try`/`finally` cleanup pattern:

```python
finally:
    for staging_path in written_paths:
        try:
            staging_path.unlink()
        except FileNotFoundError:
            pass
```

But `test_source_capture_authenticated_browser_snapshot.py` contains no equivalent test for the authenticated runner. The test file has 7 tests, none of which inject a packet-write failure and verify cleanup.

**Authority / Evidence Basis:**

The anonymous runner test coverage establishes that this is a known risk dimension for this adapter family: staged files in the output parent directory contain raw browser artifacts. In the authenticated case, staged files contain rendered DOM and visible text extracted from an authenticated session. An uncleaned staging file could be:
- Picked up by a later run's collision check (and raise a confusing error)
- Left in the output parent directory containing authenticated session content
- Accidentally committed if an operator stages the parent directory

The `AGENTS.md` requirement "Preserve real failure visibility; never create fake success paths" implies that failure paths must be tested.

**Impact:**

If a regression in `write_local_source_capture_packet` causes an exception after staging files are written, the authenticated runner may leave up to 4 files containing authenticated session content (`authenticated_browser_rendered_dom.html`, `authenticated_browser_visible_text.txt`, `authenticated_browser_viewport_screenshot.png`, `authenticated_browser_snapshot_metadata.json`) in the output parent directory. These files are not in the ignored `_auth_state/` directory and could be committed.

**Minimum Closure Condition:**

A test exists in `test_source_capture_authenticated_browser_snapshot.py` that:
1. Monkeypatches `write_local_source_capture_packet` (or injects a non-serializable metadata value via the fake capture) to raise an exception;
2. Verifies that all 4 staging file names are absent from the output parent directory after the exception propagates;
3. Verifies no packet directory was created.

**Next Authorized Action:**

Owner decision on whether to add this test before commit.

---

### MINOR Findings

---

#### m-01 — Bootstrap Runner Prints Absolute Auth-State File Path to Stdout

```yaml
finding_id: m-01
severity: minor
```

**Location:**
`orca-harness/runners/run_source_capture_browser_session_bootstrap.py:59–63`

**Implementation Evidence:**

```python
return (
    0,
    (
        f"auth-state saved for {session_mode.value} at {state_path.resolve()} "
        f"after manual browser session ending at {final_url}"
    ),
)
```

`state_path.resolve()` expands to the absolute file system path, e.g., `C:\Users\vmon7\Desktop\projects\orca\orca-harness\_auth_state\example-label.json`. The `main()` function prints this message when `exit_code == 0`.

The path contains only the label (no credential values), and is printed to the operator's own terminal. This is intentional operator feedback about where the file was written.

**Authority / Evidence Basis:**

`source_capture_agent_runbook.md` says: "Do not paste, print, stage, commit, or copy storage-state JSON, cookies, credentials, or session values into a packet or report." The path is not the JSON or credentials, but it is an absolute system path that reveals directory structure.

**Impact:**

Bounded: the path reveals system directory structure and the label name, not credential values. An operator capturing stdout logs to a shared system would expose the file path, but not the session credentials. This is acceptable for v0 but worth noting.

**Minimum Closure Condition:**

No strict closure required. Optional hardening: print only the relative path from the harness root or the label only.

**Next Authorized Action:**

Owner decision; advisory only.

---

#### m-02 — `auth_state.py` Unnecessarily in Playwright-Allowed Set in Contract Test

```yaml
finding_id: m-02
severity: minor
```

**Location:**
`orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py:48–52`

**Implementation Evidence:**

```python
allowed = {
    project_root / "source_capture" / "auth_state.py",
    project_root / "source_capture" / "adapters" / "browser_snapshot.py",
    project_root / "runners" / "run_source_capture_authenticated_browser_packet.py",
    project_root / "runners" / "run_source_capture_browser_session_bootstrap.py",
}
```

The test `test_only_browser_snapshot_surfaces_name_playwright_dependency` checks that no files outside `allowed` reference "playwright". `auth_state.py` is in `allowed` but does not currently reference "playwright" anywhere. The test file content confirms: `auth_state.py` contains only stdlib imports (`json`, `re`, `pathlib`).

**Authority / Evidence Basis:**

Including `auth_state.py` in `allowed` means a future change accidentally adding a playwright import to `auth_state.py` would pass undetected. The contract test's purpose is to enforce that playwright is isolated to specific modules.

**Impact:**

Currently harmless. Forward-looking: silent bypass of the playwright-isolation contract for `auth_state.py`. Given that `auth_state.py` has no reason to ever import playwright, this appears to be an accidental over-inclusion.

**Minimum Closure Condition:**

Remove `auth_state.py` from the `allowed` set. The test still passes because `auth_state.py` doesn't reference playwright.

**Next Authorized Action:**

Owner decision; straightforward one-line fix.

---

#### m-03 — JSONDecodeError Exception Chain May Reveal Malformed Storage-State Fragments in Tracebacks

```yaml
finding_id: m-03
severity: minor
```

**Location:**
`orca-harness/source_capture/auth_state.py:52–54`

**Implementation Evidence:**

```python
try:
    payload = json.loads(path.read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    raise ValueError(f"auth-state file is not valid JSON for label: {state_label}") from exc
```

The `from exc` clause chains the original `JSONDecodeError` as `__cause__`. Python's `json.JSONDecodeError` includes a text snippet of the malformed input in its `doc` attribute and its string representation. If the storage-state JSON is malformed (e.g., truncated mid-write, partially corrupted), the traceback would show a fragment of the malformed file near the error position.

In practice, `json.JSONDecodeError` messages for typical corruption look like:
```
json.decoder.JSONDecodeError: Unterminated string starting at: line 3 column 22 (char 45)
```
The error message itself does not necessarily include the string value at that position; it includes the line/column. But the full `exc.doc` attribute (the entire malformed JSON text) is accessible on the exception object.

**Authority / Evidence Basis:**

The `source_capture_agent_runbook.md` and `source_capture_packet.md` both say: "Do not paste, print, stage, commit, or copy storage-state JSON, cookies, credentials, or session values."

**Impact:**

Bounded: a correctly written storage-state JSON (from a successful Playwright bootstrap) is valid JSON and would never trigger this path. Only if the file is malformed (e.g., partial write) would the chain be visible. The exception is raised before any capture attempt. Cookie values in a malformed truncated JSON might appear in the chained traceback, but this requires simultaneous file corruption and a logged traceback.

**Minimum Closure Condition:**

No strict closure required for v0. Optional hardening: use `raise ValueError(...) from None` to suppress the exception chain for the JSONDecodeError case.

**Next Authorized Action:**

Owner decision; advisory.

---

### ADVISORY Findings

---

#### a-01 — Login-Wall Heuristic Misses TOTP/OTP and "Verify Identity" Patterns

```yaml
finding_id: a-01
severity: advisory
```

**Location:**
`orca-harness/runners/run_source_capture_authenticated_browser_packet.py:227–237`

**Evidence:**
The `_possible_login_wall_limitation` heuristic requires both an auth-action word (`log in`, `login`, `sign in`, `sign-in`) AND a credential word (`password`, `captcha`, `two-factor`, `2fa`) to fire. TOTP/OTP prompts (e.g., "Enter your 6-digit code") do not contain "password". "Verify your identity" pages may not contain any of the auth-action words.

**Impact:** Some authentication challenges would not be flagged. The non-claims ("not login-wall absence proof") cover this limitation at the packet level. Not a security or boundary issue.

**Next Authorized Action:** Advisory; no action required for v0. Consider extending markers in a later revision.

---

#### a-02 — State Label Visible in `visible_mode_changes` and `capture_context`; Operators Should Use Non-Revealing Labels

```yaml
finding_id: a-02
severity: advisory
```

**Location:**
`orca-harness/runners/run_source_capture_authenticated_browser_packet.py:162–175`

**Evidence:**
```python
f"authenticated_browser_storage_state_loaded:{session_mode.value}:{state_label}"
```
and
```python
f"{capture_context}; session_mode={session_mode.value}; auth_state_label={state_label}; no password automation"
```
Both strings appear in `manifest.json` and `receipt.md`. If an operator chooses a label like `johnsmith-personal-reddit-session`, that label becomes visible in the packet.

**Impact:** Bounded. The label contains no credential values. Labels are operator-chosen. Not a credential leakage issue. However, operators should be aware that label names are packet-visible.

**Next Authorized Action:** Advisory; runbook could add a note that labels are visible in packets and should not contain PII.

---

#### a-03 — Symlink on Auth-State Directory Could Redirect File Placement (Theoretical)

```yaml
finding_id: a-03
severity: advisory
```

**Location:**
`orca-harness/source_capture/auth_state.py:78–84` (`_assert_under_root`)

**Evidence:**
`_assert_under_root` uses `path_resolved = path.resolve()` which follows symlinks. If the `_auth_state/` directory itself is a symlink to an arbitrary location controlled by an attacker, `resolve()` would follow it and the auth-state file would be written to the symlink target.

**Impact:** Theoretical on the target single-user developer machine. The `default_auth_state_root()` is computed from the package source path and is not user-supplied. Not exploitable in the expected operating environment.

**Next Authorized Action:** Advisory; not actionable for v0.

---

#### a-04 — Session Mode as Declaration-Only Not Documented as Non-Claim in Runbook

```yaml
finding_id: a-04
severity: advisory
```

**Location:**
`orca-harness/docs/source_capture_agent_runbook.md` (section "Required Inputs" and "Post-Run Inspection")

**Evidence:**
The runbook says agents must pass "an allowed session mode" and documents that the packet records session mode. It does not explicitly state that the session mode is an operator declaration at capture time and is NOT validated against what was declared at bootstrap time.

**Impact:** Future agents reading the runbook might assume session mode in the packet was verified against the bootstrap record. The M-01 finding above makes this a higher-priority documentation gap.

**Next Authorized Action:** Advisory; if M-01 is addressed by adding documentation (option b in M-01's closure condition), this finding is resolved simultaneously.

---

## Non-Findings

These scenarios were considered and found to be correctly handled:

**Credential values in packet artifacts**: `manifest.json`, `receipt.md`, and all four raw packet files (`01_authenticated_browser_rendered_dom.html`, `02_authenticated_browser_visible_text.txt`, `03_authenticated_browser_viewport_screenshot.png`, `04_authenticated_browser_snapshot_metadata.json`) do not contain storage-state JSON, cookie values, tokens, or localStorage values. The `BrowserSnapshotSuccess.metadata` records `storage_state_loaded: True` (a boolean) and no file path. The `access_posture` field records the session mode string only. Verified by code trace and by `test_authenticated_browser_runner_writes_packet_without_state_leakage`.

**Auth-state file path in packet artifacts**: `str(storage_state_path)` is passed only to Playwright's `new_context(storage_state=...)` and does not appear in `BrowserSnapshotSuccess`, `manifest.json`, `receipt.md`, or raw files. `test_authenticated_browser_runner_writes_packet_without_state_leakage` explicitly verifies `str(state_path) not in combined_text`.

**Path traversal via label**: The four-layer defense (label regex, explicit path-separator check, `Path(label).name != label`, `_assert_under_root` with `relative_to()`) correctly blocks `../outside` and `nested/state`. Covered by `test_auth_state_label_rejects_path_traversal`.

**Password/credential CLI flags**: Neither `run_source_capture_authenticated_browser_packet.py` nor `run_source_capture_browser_session_bootstrap.py` exposes `--password`, `--username`, `--token`, `--cookie`, `--profile`, `--profile-path`, or `--storage-state-path` arguments. Covered by `test_authenticated_browser_clis_expose_no_secret_or_password_flags`.

**Bootstrap writes no packet**: `run_browser_session_bootstrap` calls only `bootstrap_engine.save_storage_state(...)` and `validate_auth_state_file(...)`. No call to `write_local_source_capture_packet`. Covered by `test_session_bootstrap_writes_only_auth_state_file`.

**Anonymous browser snapshot compatibility**: The `storage_state_path=None` code path in `fetch_browser_snapshot_capture` preserves the pre-authenticated-extension behavior exactly: no context kwargs for storage state, `storage_state_loaded: False` in metadata. Covered by `test_fetch_browser_snapshot_capture_with_fake_engine_preserves_browser_artifacts` and `test_fetch_browser_snapshot_capture_passes_storage_state_without_recording_path`.

**Session mode vocabulary**: The four modes (`free_account_created_session`, `paid_entitled_session`, `client_provided_session`, `consenting_coworker_session`) are a `StrEnum` in `AuthenticatedSessionMode`. They align with the source-access boundary doctrine's enumerated access types. No forbidden access type (credential stuffing, no-entitlement bypass, stolen credentials) is present. Covered by `test_session_modes_are_fixed_vocabulary`.

**Scraper/API/proxy forbidden imports**: The contract test `test_browser_snapshot_adapter_avoids_scraper_api_proxy_and_webbrowser_imports` covers `browser_snapshot.py`, `run_source_capture_browser_packet.py`, `run_source_capture_authenticated_browser_packet.py`, and `run_source_capture_browser_session_bootstrap.py`. No forbidden import roots found.

**Docs over-authorization**: `source_capture_agent_runbook.md`, `source_capture_packet.md`, and the toolbox `README.md` all explicitly restrict to manual-login Playwright storage-state v0 and prohibit password automation, direct profile/cookie import, no-entitlement bypass, anti-detect, proxy, CAPTCHA solving, API SDKs, and scraper frameworks. No over-authorization found.

**Direction-change propagation receipt**: The DCP receipt in `docs/product/source_capture_toolbox/README.md` ("Authenticated Browser Snapshot v0") is complete: correct trigger (`lifecycle_boundary`), correct related trigger (`product_doctrine`), controlling sources listed, downstream surfaces checked including `AGENTS.md`, overlay, source-of-truth, safety-rules, boundary decision, method plan, build authorization, obligation contract, source-loading, and repo map. No missing surface found.

**ECR/Cleaning/Judgment leakage**: `AUTHENTICATED_BROWSER_SNAPSHOT_NON_CLAIMS` explicitly excludes ECR, Cleaning, Judgment, and buyer proof. No such fields appear in any call to `write_local_source_capture_packet`. Exit 0 returns the output directory path, not a validation or readiness claim.

**`_auth_state/` and `_test_runs/` ignored by git**: Verified in `.gitignore` lines 18–19.

---

## Review Question Dispositions

| Q# | Question | Disposition | Findings |
|---|---|---|---|
| Q1 | Can storage-state / credential data leak into packet artifacts, stdout, errors, tests, docs? | No critical leakage found. Minor: bootstrap prints absolute file path to stdout (m-01); JSONDecodeError chain could expose malformed JSON fragment in traceback (m-03). | m-01, m-03 |
| Q2 | Is auth-state path validation strong enough? | Yes. Four-layer defense is sound. Advisory: symlink on auth directory is theoretical risk (a-03). | a-03 |
| Q3 | Does bootstrap truly write no packet and avoid credential handling? | Yes. Confirmed by code and tests. | None |
| Q4 | Does authenticated runner preserve failure visibility? | Mostly yes. Login-wall heuristic has gaps (a-01). No cleanup test for auth runner packet-write failure (M-02). | M-02, a-01 |
| Q5 | Does the implementation preserve anonymous Browser Snapshot behavior? | Yes. Confirmed by code and tests. | None |
| Q6 | Are fixed session modes consistent with boundary doctrine? | Yes. All four modes are within the boundary. Session mode is not bound to the file at bootstrap time (M-01). | M-01 |
| Q7 | Do docs over-authorize anything? | No. Docs are correctly scoped to manual-login Playwright storage-state v0. | None |
| Q8 | Is the propagation receipt complete and accurate? | Yes. DCP receipt is complete. | None |
| Q9 | Are tests strong enough for highest-risk regressions? | Mostly yes. Two gaps: cleanup test for auth runner (M-02) and auth_state.py in allowed set (m-02). | M-02, m-02 |
| Q10 | Does any code path create fake success or ECR/Cleaning/Judgment leakage? | No. Non-claims are explicit and no forbidden fields appear. | None |

---

## Validation Evidence Disposition

The author reported:
- Focused test suite: `75 passed in 19.90s` — consistent with implementation scope
- Full harness: `143 passed in 29.27s` — no regressions to existing adapters
- Smoke run: `source_surface=authenticated_browser_snapshot`, `session_mode_seen=True`, `secret_found=False`, `auth_state_copied=False`
- Secret-flag scan: no hits for password, username, token, cookie, profile, storage-state-path, os.environ, getpass
- Ignore check: both `_auth_state` and `_test_runs` confirmed `!!` (ignored)

This reviewer finds the validation evidence consistent with the code as read. The smoke run exit `0` with `secret_found=False` and `auth_state_copied=False` are correctly non-claims (discovery-grade), not readiness claims.

---

## Review-Use Boundary

These findings are decision input only. This review does not approve, validate, require remediation, authorize patches, authorize commits, or authorize production or source-system runtime.

The implementation correctly achieves its core security properties: no credential values or storage-state JSON appear in packet artifacts; path traversal is blocked; the bootstrap runner writes no packet; anonymous behavior is preserved; session mode vocabulary is fixed; docs do not over-authorize.

M-01 and M-02 represent a provenance accuracy risk and a test coverage gap respectively. Neither constitutes credential leakage. The owner should acknowledge both before treating this implementation as authoritative for evidence-grade provenance.

---

## Summary

```yaml
review_completion:
  hash_pins_verified: all 13 matched
  source_context: SOURCE_CONTEXT_READY
  critical_findings: 0
  major_findings: 2
  minor_findings: 3
  advisory_findings: 4
  recommendation: accept_with_minor_findings
  blocking_concerns:
    - id: M-01
      summary: Session mode not bound to auth-state file; packet may record incorrect mode; provenance misrepresentation risk
    - id: M-02
      summary: No staging-file cleanup test for authenticated runner on packet-write failure; authenticated session content could be left on disk
  next_action: >
    Owner decides: (a) add session-mode sidecar binding or explicit runbook non-claim to address M-01; (b) add staged-file cleanup test for authenticated runner to address M-02. Neither finding constitutes credential leakage; all critical security properties are intact.
```
