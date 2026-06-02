# Source Capture Authenticated Browser Snapshot Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial code review prompt for Authenticated Browser Snapshot v0.
use_when:
  - Reviewing the uncommitted Authenticated Browser Snapshot v0 implementation before commit.
authority_boundary: prompt_only
output_mode: review-report
required_output_path: docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md
```

## Commission

Perform a read-only adversarial implementation/code review of the uncommitted
Authenticated Browser Snapshot v0 implementation in:

`C:\Users\vmon7\Desktop\projects\orca`

This review is decision input only. Do not patch files, commit, clean generated
outputs, launch real external logins, install packages, run browsers against
remote sites, or broaden into product planning. The review target is the
existing worktree implementation, not a substitute checkout.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: required
  overlay_read: required
  source_pack: custom Source Capture Toolbox authenticated browser snapshot implementation review
  edit_permission: read-only review; report-write only to required_output_path
  target_scope:
    - .gitignore
    - docs/product/source_capture_toolbox/README.md
    - orca-harness/README.md
    - orca-harness/docs/source_capture_agent_runbook.md
    - orca-harness/docs/source_capture_packet.md
    - orca-harness/source_capture/auth_state.py
    - orca-harness/source_capture/__init__.py
    - orca-harness/source_capture/adapters/browser_snapshot.py
    - orca-harness/runners/run_source_capture_authenticated_browser_packet.py
    - orca-harness/runners/run_source_capture_browser_session_bootstrap.py
    - orca-harness/tests/unit/test_source_capture_browser_snapshot.py
    - orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py
    - orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py
  dirty_state_checked: required
  expected_branch: main
  expected_head_short: d868fc2
  dirty_state_allowance: >
    The review target files above are intentionally modified/untracked.
    Existing unrelated Orca dirty/untracked files are out of scope and must not
    be treated as review targets unless they affect source authority.
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/product/source_capture_toolbox/README.md
    - docs/product/data_capture_source_access_boundary_decision_v0.md
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
```

## Required Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking`.
3. REFERENCE-LOAD `workflow-code-review`.
4. Do not APPLY either method yet.
5. SOURCE-LOAD all required authority, target, support, and validation evidence
   listed below.
6. Verify every pinned target hash below. If any hash mismatches, stop with
   `HASH_MISMATCH` and list the mismatched path, expected hash, actual hash,
   and nearest allowed next step.
7. Declare `SOURCE_CONTEXT_READY` only after the required sources and hashes are
   loaded. If any required source is missing, declare `SOURCE_CONTEXT_INCOMPLETE`.
8. Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame
   failure modes and APPLY `workflow-code-review` in adversarial posture.
9. Write the full durable review report to:
   `docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md`
10. After the report is written, return only a compact human summary plus a
    fenced `review_summary` YAML block in chat.

## Target Hash Pins

Verify these SHA256 pins before review:

```text
BC1507835E9E5886516838705789D23865239D49812E4DBD0FF24272E23225B7  .gitignore
014721D7D66E2C79AA8FB94DA66A3E90B83407A5B3AD4C08EF8285727384AEF9  docs\product\source_capture_toolbox\README.md
0307977A69814AC9E411DC62A09D9681B7DAEABC0D5F1752C51F89645FC6805C  orca-harness\README.md
899DEC76DD0B03B2FE8EA5D79D433A676A5CFB572E02CBFF65C9336B8AB96BD0  orca-harness\docs\source_capture_agent_runbook.md
80E8E4F1023E778B308F1760B3D854FDD7A1C8CA252A9869BC26216C0354A847  orca-harness\docs\source_capture_packet.md
C3313D11215C094131CE45CA328EB80A7D0984F1662AFCA46FBF2AFA7D178E11  orca-harness\source_capture\auth_state.py
EE77C5C60B0733F1B254EBA8E1FF37E453A6AB43931080278F55FF139C619045  orca-harness\source_capture\__init__.py
1BDB04730A9482CCAF793F506E4DD1D29D702928C0EB1444E782B35DEB2867FF  orca-harness\source_capture\adapters\browser_snapshot.py
1D89350B90AC5BCF79CF265BF4AC25E123D811F7BD96365B43190C523D1CF3AC  orca-harness\runners\run_source_capture_authenticated_browser_packet.py
9B599C8C71ADE90A8CEFBED5AEB6D33581B1971359ED6364D0DCA6DFA31F42A0  orca-harness\runners\run_source_capture_browser_session_bootstrap.py
ADCFCB1DE5B10C83396C0D25AAB10096FA28F5ACC80E84F1348B67A394D24A4F  orca-harness\tests\unit\test_source_capture_browser_snapshot.py
C22FF0928E95109BE91F25F8B8F1F5A9A1CFEBE3C55B64D7CB1BA90D15A73023  orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py
EED2144BCDF6B7F752940FE325B333BC6EE6F0E8273F299DEAC67B46A01E3316  orca-harness\tests\contract\test_source_capture_browser_snapshot_contract.py
```

## Required Source Basis

SOURCE-LOAD these authority and support files:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- all target files listed under Target Hash Pins.

## Implementation Summary To Verify

The implementation is intended to add Authenticated Browser Snapshot v0:

- `auth_state.py` defines fixed session modes:
  - `free_account_created_session`
  - `paid_entitled_session`
  - `client_provided_session`
  - `consenting_coworker_session`
- auth-state files must live under ignored `orca-harness/_auth_state/`;
- bootstrap runner opens headed Playwright for manual login and writes local
  ignored storage-state JSON only;
- bootstrap writes no Source Capture Packet;
- authenticated packet runner loads an existing state label and writes a normal
  Source Capture Packet with rendered DOM, visible text, viewport screenshot,
  and metadata;
- packets may record session mode and state label, but must not copy, hash,
  print, or preserve storage-state JSON, cookies, tokens, or credentials;
- no username/password/token/cookie/profile CLI flags are allowed;
- no password-driven login automation, direct profile/cookie import,
  no-entitlement bypass, anti-detect, proxy, CAPTCHA solving, API SDK,
  scraper framework, ECR, Cleaning, Judgment, buyer proof, or production runtime
  is authorized;
- anonymous Browser Snapshot behavior should remain compatible.

## Validation Evidence To Inspect

The implementation author observed:

```text
python -m pytest -p no:cacheprovider --basetemp pytest_tmp_auth_browser tests/unit/test_source_capture_packet.py tests/contract/test_source_capture_packet_no_runtime_imports.py tests/unit/test_source_capture_direct_http.py tests/contract/test_source_capture_direct_http_contract.py tests/unit/test_source_capture_media_asset.py tests/contract/test_source_capture_media_asset_contract.py tests/unit/test_source_capture_archive_org.py tests/contract/test_source_capture_archive_org_contract.py tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_source_capture_authenticated_browser_snapshot.py tests/contract/test_source_capture_browser_snapshot_contract.py
```

Observed result:

```text
75 passed in 19.90s
```

Full harness:

```text
python -m pytest -p no:cacheprovider --basetemp pytest_tmp_full_auth_browser
```

Observed result:

```text
143 passed in 29.27s
```

Local authenticated browser smoke:

- sandbox run failed visibly with `WinError 5 Access is denied`, exit `3`, no
  packet;
- escalated local loopback run exited `0`;
- observed packet existed;
- `source_surface=authenticated_browser_snapshot`;
- `session_mode_seen=True`;
- raw files were:
  - `01_authenticated_browser_rendered_dom.html`
  - `02_authenticated_browser_visible_text.txt`
  - `03_authenticated_browser_viewport_screenshot.png`
  - `04_authenticated_browser_snapshot_metadata.json`
- `secret_found=False`;
- `auth_state_copied=False`.

Other checks:

- `git diff --check` on target files produced only LF/CRLF warnings and no
  whitespace errors.
- stale session-support scan hit only the literal search string inside the new
  propagation receipt.
- secret-flag scan over implementation files returned no hits for password,
  username, token, cookie, profile, storage-state-path CLI flags, `os.environ`,
  or `getpass`.
- `git status --ignored --short -- orca-harness\_auth_state orca-harness\_test_runs`
  showed both generated areas ignored (`!!`), with unrelated pre-existing
  permission warnings under `_test_runs`.

## Review Questions

Be adversarial about material implementation risks:

1. Can storage-state JSON, cookies, tokens, localStorage values, or auth-state
   file paths leak into `manifest.json`, `receipt.md`, raw packet files, stdout,
   errors, tests, or docs?
2. Is auth-state path validation strong enough to prevent path traversal,
   packet-output placement, fixture/report placement, or accidental commit of
   session state?
3. Does the bootstrap runner truly write no packet and avoid credential
   handling/password automation?
4. Does the authenticated packet runner preserve failure visibility, especially
   missing/invalid state, browser failures, login wall/challenge visibility,
   output collisions, and packet writer failures?
5. Does the implementation preserve anonymous Browser Snapshot behavior and
   non-claims?
6. Are the fixed session modes consistent with Orca source-access boundary
   doctrine and hard stops?
7. Do the docs over-authorize anything beyond manual-login Playwright
   storage-state v0?
8. Is the direction-change propagation receipt complete and accurate for this
   toolbox status change?
9. Are tests strong enough to catch the highest-risk regressions: state leakage,
   path traversal, forbidden flags, no-packet bootstrap, state-loaded metadata,
   and login-wall limitation behavior?
10. Does any code path create fake success, validation/readiness claims, or
    ECR/Cleaning/Judgment leakage?

## Findings Standard

Report findings first, ordered by severity. Use:

- `critical`: defect can leak credentials/session state, silently bypass hard
  stops, create fake source-capture success, or materially corrupt packet
  evidence.
- `major`: defect can mislead agents, weaken access/session safety, break
  authenticated capture semantics, or leave a material test gap before commit.
- `minor`: bounded correctness, documentation, test, or maintainability issue
  that should be considered but does not block commit by itself.
- `advisory`: optional hardening or future-work note.

Every actionable finding must include:

- finding id;
- severity;
- location;
- implementation evidence;
- authority/evidence basis;
- impact;
- minimum closure condition;
- next authorized action.

Do not emit `patch_queue_entry`; this is read-only review.

## Output Contract

Write the full durable report to:

`docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md`

After successful write, return a concise chat summary plus:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md
  recommendation: accept | accept_with_minor_findings | revise_before_commit | blocked
  findings_count:
    critical: <n>
    major: <n>
    minor: <n>
    advisory: <n>
  blocking_or_major_findings:
    - <id and one-line summary, or none>
  next_action: <owner/implementer next action>
```

Review-use boundary: findings are decision input only. This review does not
approve, validate, require remediation, authorize patches, authorize commits,
or authorize production/source-system runtime.
