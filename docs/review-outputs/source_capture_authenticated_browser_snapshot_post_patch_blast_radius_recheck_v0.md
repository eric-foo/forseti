# Source Capture Authenticated Browser Snapshot Post-Patch Blast-Radius Recheck v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Bounded adversarial recheck of the Authenticated Browser Snapshot v0 post-patch
  implementation. Closure verification for M-01 (session-mode sidecar binding) and
  M-02 (authenticated staging-file cleanup test). Blast-radius check for patch-caused
  regressions within the touched scope.
use_when:
  - Owner deciding whether the patched Authenticated Browser Snapshot v0 is safe to commit.
review_authority_boundary: review_output_only
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

---

## Preflight Record

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Source Capture Toolbox authenticated browser post-patch recheck
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: main
  expected_head_short: d868fc2
  dirty_state_checked: yes
  dirty_state_allowance: >
    Review target files are intentionally modified/untracked. Prior review output
    and this prompt are untracked. All other dirty/untracked Orca files are out of scope.
  edit_permission: read-only review; report-write only to required_output_path
  output_mode: review-report
  required_output_path: docs/review-outputs/source_capture_authenticated_browser_snapshot_post_patch_blast_radius_recheck_v0.md
```

---

## Hash Verification

### Target File Pins

All 14 target file hashes match the prompt pins exactly.

| File | Expected | Match |
|---|---|---|
| `.gitignore` | `BC150783...` | ✓ |
| `docs\product\source_capture_toolbox\README.md` | `F1A84DFA...` | ✓ |
| `orca-harness\README.md` | `2EBA0524...` | ✓ |
| `orca-harness\docs\source_capture_agent_runbook.md` | `611A82D9...` | ✓ |
| `orca-harness\docs\source_capture_packet.md` | `4FF2F20F...` | ✓ |
| `orca-harness\source_capture\auth_state.py` | `A0A6DC42...` | ✓ |
| `orca-harness\source_capture\__init__.py` | `EE77C5C6...` | ✓ |
| `orca-harness\source_capture\adapters\browser_snapshot.py` | `1BDB0473...` | ✓ |
| `orca-harness\runners\run_source_capture_authenticated_browser_packet.py` | `8C4F959D...` | ✓ |
| `orca-harness\runners\run_source_capture_browser_session_bootstrap.py` | `83DDF7B7...` | ✓ |
| `orca-harness\tests\unit\test_source_capture_browser_snapshot.py` | `ADCFCB1D...` | ✓ |
| `orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py` | `7637D146...` | ✓ |
| `orca-harness\tests\contract\test_source_capture_browser_snapshot_contract.py` | `E056B484...` | ✓ |
| `docs\review-outputs\..._adversarial_code_review_v0.md` | `3EBD19D7...` | ✓ |

### Source-Basis Pins

All 11 source-basis file hashes match the prompt pins exactly.

| File | Match |
|---|---|
| `AGENTS.md` | ✓ |
| `.agents\workflow-overlay\README.md` | ✓ |
| `.agents\workflow-overlay\source-of-truth.md` | ✓ |
| `.agents\workflow-overlay\source-loading.md` | ✓ |
| `.agents\workflow-overlay\prompt-orchestration.md` | ✓ |
| `.agents\workflow-overlay\review-lanes.md` | ✓ |
| `.agents\workflow-overlay\safety-rules.md` | ✓ |
| `docs\product\data_capture_source_access_boundary_decision_v0.md` | ✓ |
| `docs\product\data_capture_source_access_method_plan_v0.md` | ✓ |
| `docs\decisions\data_capture_spine_source_access_tooling_build_authorization_v0.md` | ✓ |
| `docs\product\core_spine_v0_data_capture_spine_obligation_contract_v0.md` | ✓ |

**RESULT: ALL 25 HASHES VERIFIED — NO MISMATCH.**

---

## Source Context Declaration

```text
SOURCE_CONTEXT_READY
```

All required authority files, the prior adversarial review output, and all 13 current target implementation files were loaded and read before this review began.

---

## Method Application Declarations

- `workflow-deep-thinking` APPLIED: closure risk framing completed before findings.
- `workflow-code-review` APPLIED: bounded adversarial recheck over patch-touched scope.

---

## Deep-Thinking: Closure Risk Framing

Before closure verdicts, this section captures the adversarial questions that shaped the recheck.

### Risk Dimension 1 — Does the Sidecar Actually Bind Mode, or Can It Be Bypassed?

The sidecar must (a) be written atomically enough that a half-bootstrap doesn't produce fake success, and (b) be validated before any browser activity runs, not after. Key questions: Is `validate_auth_state_session_mode` called before `fetch_browser_snapshot_capture`? Does a missing sidecar exit cleanly? Does a mismatched mode exit before browser activity?

### Risk Dimension 2 — Does the Sidecar Introduce Credential Leakage?

The sidecar is a new file artifact. Its contents must not include cookies, tokens, localStorage values, or storage-state JSON. Its path must not appear in packet artifacts or error messages that route to committed files.

### Risk Dimension 3 — Bootstrap Non-Atomicity Between State File and Sidecar

The bootstrap writes the state file (via Playwright) first, then validates it, then writes the sidecar. If the sidecar write fails after the state file is written, the `_auth_state/` directory has a half-bootstrapped artifact. Does this create a silent success path, an unrecoverable state, or a misleading error?

### Risk Dimension 4 — M-02 Test Coverage Adequacy

The new cleanup test must exercise the actual failure path: staging files are written, then the packet writer fails, then the `finally` block runs. The test must inject failure after staging (not before), assert files are gone, and assert no packet directory exists. A test that injects failure before staging would not prove cleanup works.

### Risk Dimension 5 — Prior Minor Findings Carried Through

Minor findings m-01 (absolute path in stdout), m-02 (auth_state.py in playwright allowed set), and m-03 (JSONDecodeError chain) from the prior review are also within the patch scope. Each has a visible patch change.

### Risk Dimension 6 — Blast Radius: Does the Patch Introduce Any Regression in Anonymous Behavior, Path Containment, or Contract Tests?

`browser_snapshot.py` and `test_source_capture_browser_snapshot.py` are unchanged (verified by hash match). The contract test's playwright-allowed set was reduced. The path containment logic (`_assert_under_root`) is unchanged. The sidecar path is derived via `with_suffix` and also validated by `_assert_under_root`. Regression risk is bounded to the new functions.

---

## Findings: Closure Status

### M-01 — Session Mode Not Bound to Auth-State File

**Closure Verdict: CLOSED**

**Evidence of Closure:**

The patch adds three new functions to `auth_state.py`:

1. `auth_state_metadata_path_for_label()` — derives sidecar path from state path via `state_path.with_suffix(".meta.json")`. The sidecar lives in the same `_auth_state/` directory as the state file. `_assert_under_root` is called explicitly, preventing path escape.

2. `write_auth_state_metadata()` — validates the state file exists (calls `validate_auth_state_file`), checks sidecar does not already exist, writes:
   ```json
   {
     "auth_state_file": "<filename-only>",
     "session_mode": "<mode-value>"
   }
   ```
   The sidecar contains only the filename (not the full path) and the mode string. No credential values. The `json.JSONDecodeError` guard uses `from None` (no exception chain).

3. `validate_auth_state_session_mode()` — validates state file (via `validate_auth_state_file`), checks sidecar exists, checks sidecar is valid JSON (with `from None`), checks `auth_state_file` binding matches `state_path.name`, checks `session_mode` matches `session_mode.value`. Returns `state_path` on success, raises `ValueError` on any failure.

The bootstrap runner (`run_source_capture_browser_session_bootstrap.py`) now:
- Checks both `state_path.exists()` AND `metadata_path.exists()` before Playwright runs (prevents half-state overwrites)
- Calls `validate_auth_state_file` and `write_auth_state_metadata` after Playwright writes the state

The capture runner (`run_source_capture_authenticated_browser_packet.py`) now:
- Calls `validate_auth_state_session_mode(state_label, session_mode=session_mode, ...)` as the FIRST operation
- This replaces the prior `validate_auth_state_file` call
- If validation raises, it propagates as `ValueError` → exit 2, no browser activity, no staging files, no packet

**Test Coverage:**

`test_authenticated_browser_runner_rejects_session_mode_mismatch`:
- Creates state pair with `CONSENTING_COWORKER`
- Injects `fake_capture` that raises `AssertionError` if invoked
- Calls capture runner with `FREE_ACCOUNT_CREATED` (mismatch)
- Asserts `ValueError` with "session mode mismatch" is raised — not `AssertionError` — proving `fake_capture` was never called
- Asserts `not (scratch_dir / "packet").exists()` — no packet directory created

`test_session_bootstrap_writes_auth_state_and_sidecar_without_packet`:
- Verifies sidecar exists after bootstrap
- Verifies sidecar JSON content exactly: `{"auth_state_file": "free-example.json", "session_mode": "free_account_created_session"}`
- Verifies `str(state_path) not in message` (no absolute path in stdout)
- Verifies no manifest/receipt written

**Provenance accuracy is now mechanical:** a packet cannot be written with session mode X unless the sidecar records mode X from bootstrap time. Misrepresentation requires the operator to independently bootstrap and capture with matching wrong modes — which is operator-controlled identity fraud, not a system-level leakage.

---

### M-02 — No Staging-File Cleanup Test for Authenticated Runner on Packet-Write Failure

**Closure Verdict: CLOSED**

**Evidence of Closure:**

`test_authenticated_browser_runner_cleans_staged_files_when_packet_write_fails` (test file lines 367–446):

1. Creates valid auth state pair with `CLIENT_PROVIDED` (session validation passes)
2. Injects `fake_capture` returning valid `BrowserSnapshotSuccess` — staging files get written before packet write is attempted
3. Injects `fake_packet_writer` that raises `RuntimeError("packet writer failed")` — injected at `auth_runner.write_local_source_capture_packet`
4. Calls the runner — RuntimeError propagates from the `try` block in `run_source_capture_authenticated_browser_packet`
5. The `finally` block runs: `written_paths` contains all 4 staged file paths, each is unlinked
6. Asserts propagated `RuntimeError` (not swallowed)
7. Asserts `not output_dir.exists()` — no packet directory
8. Asserts all 4 staging file names absent from `output_dir.parent`:
   - `authenticated_browser_rendered_dom.html`
   - `authenticated_browser_visible_text.txt`
   - `authenticated_browser_viewport_screenshot.png`
   - `authenticated_browser_snapshot_metadata.json`

The monkeypatch targets `auth_runner.write_local_source_capture_packet` (the name in the runner module's namespace, bound via `from source_capture import write_local_source_capture_packet`). This is correct Python module-level monkeypatching — the patch affects the binding in `auth_runner`'s namespace, which is what the runner calls.

The test failure path correctly exercises: staging files written → packet write fails → `finally` cleanup → confirmed absent.

---

## Review Question Dispositions

**Q1 — Does the sidecar mechanically bind bootstrap-time to capture-time session mode?**
Yes. `validate_auth_state_session_mode` enforces mode match via sidecar before any browser activity. Mismatch → exit 2, no packet. Tested directly. ✓

**Q2 — Can a missing/malformed/mismatched/path-traversed sidecar create fake success or leakage?**

| Sidecar state | Result | Safe? |
|---|---|---|
| Missing | `ValueError` "sidecar does not exist; re-bootstrap" → exit 2, no packet | ✓ |
| Malformed JSON | `ValueError` "not valid JSON" (from None, no chain) → exit 2, no packet | ✓ |
| Not a dict | `ValueError` "must be a JSON object" → exit 2, no packet | ✓ |
| Filename binding mismatch | `ValueError` "file binding mismatch" → exit 2, no packet | ✓ |
| Mode mismatch | `ValueError` "session mode mismatch; bootstrapped as X, declared Y" → exit 2, no packet | ✓ |
| Missing `session_mode` key | `payload.get("session_mode")` → `None`; `None != mode.value` → mismatch error → exit 2 | ✓ |
| Path traversal via label | Blocked by label regex + explicit separator check + `_assert_under_root` on both state and sidecar paths | ✓ |

No fake-success path exists. All failure modes exit cleanly with a visible error message before browser activity.

**Q3 — Does the sidecar introduce sensitive data into packets, raw files, receipt, stdout, metadata, docs, test output?**

Sidecar content: `{"auth_state_file": "<filename-only>", "session_mode": "<mode-value>"}`. No cookies, tokens, or credential values.

The sidecar file is NOT copied into any packet artifact. `validate_auth_state_session_mode` reads the sidecar internally and returns only `state_path`. The capture context, access posture, and visible_mode_changes fields in `manifest.json` record `session_mode.value` and `state_label` — same as the pre-patch implementation. The sidecar's `auth_state_file` field (just a filename) does not appear in any packet output.

Mismatch error message: `f"...bootstrapped as {bootstrapped_mode!r} but capture declared {session_mode.value!r}"` — contains the mode strings only (not credentials). ✓

Bootstrap success message: `f"auth-state saved for {session_mode.value} with label {state_label} after manual browser session ending at {final_url}"` — no absolute file path. Prior m-01 finding closed. ✓

**Q4 — Does the bootstrap runner still write no packet and avoid credential CLI flags?**
No `write_local_source_capture_packet` call. Parser unchanged: `--login-url`, `--state-label`, `--session-mode`, `--timeout-seconds` only. `test_authenticated_browser_clis_expose_no_secret_or_password_flags` passes. `test_session_bootstrap_writes_auth_state_and_sidecar_without_packet` explicitly checks no manifest/receipt written. ✓

**Q5 — Does the capture runner reject mode mismatches before browser capture?**
Yes. `validate_auth_state_session_mode` is line 86–90 of the capture runner, before `fetch_browser_snapshot_capture` at line 91. The test proves fake_capture is never called when mismatch occurs. ✓

**Q6 — Does the authenticated staging cleanup test close M-02 with real failure-path coverage?**
Yes. The test injects failure after staging files are written (via fake_capture success then fake_packet_writer failure). All 4 files are verified absent. Output dir is absent. RuntimeError propagates. ✓

**Q7 — Did the patch preserve anonymous Browser Snapshot behavior?**
`browser_snapshot.py` hash unchanged (1BDB0473...). Anonymous code path untouched. ✓

**Q8 — Did the patch preserve auth-state path containment under `_auth_state/` and avoid printing absolute paths?**
`_assert_under_root` unchanged. Sidecar path explicitly checked via `_assert_under_root`. Bootstrap message now uses label string (not `state_path.resolve()`). Test verifies `str(state_path) not in message`. `.gitignore` unchanged — `orca-harness/_auth_state/` remains ignored, covering both `.json` state files and `.meta.json` sidecars. ✓

**Q9 — Did docs accurately describe sidecar binding without over-authorizing?**

`source_capture_agent_runbook.md`: "stores only local ignored Playwright storage-state JSON under `orca-harness/_auth_state/`, plus a small local ignored metadata sidecar binding the saved state file to the declared session mode." And: "it refuses to run if the capture-time session mode does not match the bootstrap sidecar. It does not copy, hash, print, or preserve the storage-state file, metadata sidecar, or cookie/session values." Explicit non-preserve statement covers the sidecar. "Choose a non-sensitive state label; the label is later recorded in packet metadata." (addresses prior a-02). ✓

`source_capture_packet.md`: "writes only a Playwright storage-state JSON file plus a session-mode metadata sidecar under `orca-harness/_auth_state/`... It does not copy, hash, print, or preserve the storage-state JSON, metadata sidecar, or cookie/session values." ✓

Both docs correctly describe forbidden methods (password automation, profile/cookie import, no-entitlement bypass, anti-detect, proxy, CAPTCHA, API SDK, ECR, Cleaning, Judgment) without relaxing any restriction. No over-authorization found. ✓

**Q10 — Did the product README DCP remain accurate?**

The DCP receipt in `docs/product/source_capture_toolbox/README.md` was updated to include "with local ignored session-mode sidecar binding" in `doctrine_changed`. The controlling sources updated include toolbox README, runbook, packet doc, and harness README. The stale-language search is unchanged (checking for pre-implementation language about "no logged-in/entitled browser session"). No new stale-language sweep is needed because the sidecar is an additive feature with no pre-existing stale references. The DCP accurately reflects the post-patch implementation. ✓

**Q11 — Do reported validation results correspond to tests that would catch the prior failures?**

| Evidence | Arithmetic Check | Assessment |
|---|---|---|
| 23 focused tests | 9 (auth) + 11 (browser snapshot) + 3 (contract) = 23 ✓ | Consistent with +2 new auth tests |
| 77 source-capture slice | 75 (prior) + 2 = 77 ✓ | Consistent |
| 145 full harness | 143 (prior) + 2 = 145 ✓ | Consistent |
| Secret-flag scan: no hits | auth_state.py, both runners scanned; no password/token/cookie/os.environ/getpass | ✓ |
| Playwright isolation on auth_state.py: no hits | auth_state.py has no playwright reference (confirmed by read) | ✓ |
| Both dirs ignored | .gitignore lines 18–19 unchanged; `_auth_state/` covers both `.json` and `.meta.json` | ✓ |

The new tests (`test_authenticated_browser_runner_rejects_session_mode_mismatch` and `test_authenticated_browser_runner_cleans_staged_files_when_packet_write_fails`) are the tests that would have caught the M-01 and M-02 prior failures. Both exist in the read file and their assertions match the minimum closure conditions from the prior review. ✓

**Q12 — Any patch-caused blocker or major regressions inside the touched scope?**

None found. See advisory finding below.

---

## Advisory Finding (Patch-Caused, Decision-Relevant)

### a-new-01 — Bootstrap Non-Atomicity: State File Written but Sidecar Write Can Fail

```yaml
finding_id: a-new-01
severity: advisory
```

**Location:** `orca-harness/runners/run_source_capture_browser_session_bootstrap.py:62–67`

**Evidence:**

```python
validate_auth_state_file(state_label, auth_state_root=auth_state_directory)
write_auth_state_metadata(
    state_label,
    session_mode=session_mode,
    auth_state_root=auth_state_directory,
)
```

The sequence is: (a) Playwright writes state file, (b) validate state file, (c) write sidecar. If `write_auth_state_metadata` raises (e.g., permission error, disk full), the bootstrap exits with exception → exit 3. The state file remains on disk without a sidecar.

Subsequent bootstrap attempt → `ValueError` "auth-state file already exists" (exit 2). Capture attempt → `ValueError` "sidecar does not exist; re-bootstrap" (exit 2). The operator must manually delete `<label>.json` to re-bootstrap cleanly.

**Impact:** Bounded. Both failure messages are visible and informative. The recovery path is clear: delete the state file and re-bootstrap. No credentials leak; no fake-success path. Disk-full or permission failures during sidecar write are uncommon in practice.

**Next Authorized Action:** Advisory; no action required for v0.

---

## Prior Minor Findings — Closure Status

| Finding | Status | Evidence |
|---|---|---|
| m-01: Bootstrap prints absolute auth-state file path to stdout | **CLOSED** | Message now uses label (`state_label`) not `state_path.resolve()`. Test verifies `str(state_path) not in message`. |
| m-02: `auth_state.py` in playwright-allowed set unnecessarily | **CLOSED** | `auth_state.py` removed from `allowed` set in contract test (contract test hash changed: E056B4...). `auth_state.py` has no playwright reference (confirmed by Playwright isolation scan: no hits). |
| m-03: JSONDecodeError exception chain could reveal malformed storage-state fragments | **CLOSED** | `validate_auth_state_file` now uses `except json.JSONDecodeError: raise ValueError(...) from None`. Same pattern applied to `validate_auth_state_session_mode` for sidecar parsing. |

## Prior Advisory Findings — Status

| Finding | Status |
|---|---|
| a-01: Login-wall heuristic misses TOTP/OTP patterns | **PARTIALLY ADDRESSED** — heuristic extended with "verify your identity", "authentication", "otp", "totp", "verification code". Coverage improved; edge cases remain possible. Non-claims still cover this. |
| a-02: State label visible in packet metadata | **DOCUMENTED** — runbook and packet doc now include: "Choose a non-sensitive state label; the label is later recorded in packet metadata." |
| a-03: Symlink attack on auth-state directory | **UNCHANGED** — advisory only; not actionable for v0. |
| a-04: Mode as declaration-only not documented as non-claim | **RESOLVED** — docs now explicitly state the runner "refuses to run if the capture-time session mode does not match the bootstrap sidecar"; the sidecar mechanism is the non-claim substitute. |

---

## Non-Findings

**Credential/session leakage into packet artifacts:** Sidecar contains only `auth_state_file` (filename) and `session_mode` (mode string). Neither flows into packet artifacts. Cookie values remain isolated inside the Playwright storage-state JSON file under `_auth_state/`. Verified by code trace and `test_authenticated_browser_runner_writes_packet_without_state_leakage` (cookie value `SECRET_COOKIE_VALUE` not in combined packet text). ✓

**Path traversal via sidecar:** Sidecar path derived from validated state path via `with_suffix` (no user input accepted). `_assert_under_root` applied explicitly. No label can escape the `_auth_state/` root. ✓

**Bootstrap writes no packet:** Confirmed by code (no `write_local_source_capture_packet` call) and by test (no manifest/receipt asserted absent). ✓

**Anonymous browser snapshot compatibility:** `browser_snapshot.py` hash unchanged. ✓

**Source-access boundary compliance:** All four session modes remain within the boundary doctrine. No new modes added. No API SDK, anti-detect, proxy, CAPTCHA, or password-automation code introduced. ✓

**Docs over-authorization:** Runbook and packet doc explicitly list forbidden methods unchanged. Sidecar description adds no new authorization. ✓

**ECR/Cleaning/Judgment leakage:** `AUTHENTICATED_BROWSER_SNAPSHOT_NON_CLAIMS` unchanged. No ECR/Cleaning/Judgment fields in any packet writer call. ✓

**Contract test blast radius:** Playwright-allowed set correctly reduced (auth_state.py removed). Auth_state.py confirmed to have no playwright reference. FORBIDDEN_IMPORT_ROOTS check still covers both runners and adapters. ✓

---

## Recommendation

```text
closure_confirmed_with_minor_advisory_carry
```

M-01 and M-02 are mechanically closed. The sidecar binding correctly enforces bootstrap-time ↔ capture-time mode consistency, and the authenticated staging cleanup test exercises the actual failure-path with correct assertions. No new blocker or major findings were introduced by the patch. Three prior minor findings (m-01, m-02, m-03) are also closed. One new advisory finding (bootstrap non-atomicity) carries forward. The implementation is sound for commit.

---

## Review-Use Boundary

Review findings are decision input only. This report does not approve, validate, require remediation, authorize patches, authorize commits, or authorize production/runtime source capture. Commit, patch, or runtime use requires separate owner action.
