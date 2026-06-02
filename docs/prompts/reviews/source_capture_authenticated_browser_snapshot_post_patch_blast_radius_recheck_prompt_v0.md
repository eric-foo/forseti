# Source Capture Authenticated Browser Snapshot Post-Patch Blast-Radius Recheck Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Bounded adversarial code-review recheck for the Authenticated Browser Snapshot v0 post-patch changes.
use_when:
  - Verifying closure of M-01 and M-02 from the prior authenticated browser snapshot adversarial code review.
  - Deciding whether the patched Authenticated Browser Snapshot v0 implementation is safe to commit.
authority_boundary: prompt_only
```

## Objective

Run a read-only, bounded post-patch blast-radius recheck of the Authenticated
Browser Snapshot v0 implementation in the Orca workspace.

The review must answer only this closure question:

```text
Did the post-review patch close M-01 and M-02 from the prior adversarial code
review without introducing a blocker or major regression in credential/session
leakage, auth-state path containment, provenance accuracy, staging cleanup,
anonymous browser compatibility, source-access boundary compliance, or docs
over-authorization?
```

Do not perform a fresh full architecture review, do not broaden into unrelated
Source Capture Toolbox adapters, and do not patch files.

## Required Method Sequence

Follow this sequence exactly:

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking`.
3. REFERENCE-LOAD `workflow-code-review`.
4. Do not APPLY either method yet.
5. SOURCE-LOAD all required authority files, prior review output, and current
   target files listed below.
6. Verify all SHA256 pins listed below.
7. Declare `SOURCE_CONTEXT_READY` if all required files were loaded and all
   hashes matched, or `SOURCE_CONTEXT_INCOMPLETE` / `HASH_MISMATCH` with exact
   details and stop before review claims.
8. APPLY `workflow-deep-thinking` to frame the closure risks.
9. APPLY `workflow-code-review` in bounded recheck posture.
10. Write the durable review report to the required output path.
11. Return only a compact chat summary plus courier YAML after the report write
    succeeds.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: required
  overlay_read: required
  source_pack: custom Source Capture Toolbox authenticated browser post-patch recheck
  workspace: C:\Users\vmon7\Desktop\projects\orca
  expected_branch: main
  expected_head_short: d868fc2
  dirty_state_checked: required
  dirty_state_allowance: >
    Review target files are intentionally modified/untracked. The prior review
    output and this prompt may be untracked. Other Orca dirty/untracked files are
    out of scope unless they are listed below as required source basis.
  edit_permission: read-only review; report-write only to required_output_path
  output_mode: review-report
  required_output_path: docs/review-outputs/source_capture_authenticated_browser_snapshot_post_patch_blast_radius_recheck_v0.md
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md
    - orca-harness/source_capture/auth_state.py
    - orca-harness/runners/run_source_capture_authenticated_browser_packet.py
    - orca-harness/runners/run_source_capture_browser_session_bootstrap.py
    - orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py
```

## Source Hierarchy

Treat these as controlling for the review:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/prompt-orchestration.md`
6. `.agents/workflow-overlay/review-lanes.md`
7. `.agents/workflow-overlay/safety-rules.md`
8. `docs/product/data_capture_source_access_boundary_decision_v0.md`
9. `docs/product/data_capture_source_access_method_plan_v0.md`
10. `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
11. `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
12. `docs/product/source_capture_toolbox/README.md`
13. `orca-harness/docs/source_capture_agent_runbook.md`
14. `orca-harness/docs/source_capture_packet.md`
15. Prior review output:
    `docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md`

Reusable workflow skills are method guidance only, not Orca authority.

## Prior Findings To Recheck

Close only these prior major findings unless the patch introduces a new blocker
or major issue inside the touched scope:

### M-01

```text
Session mode not bound to auth-state file; packet can record wrong mode;
provenance misrepresentation risk.
```

Minimum closure from prior review:

```text
Either:
(a) A mode-binding sidecar file is written by the bootstrap runner so the
    capture runner can validate that the declared mode at capture time matches
    the declared mode at bootstrap time; OR
(b) Docs explicitly disclose that session mode is operator declaration only.
```

Expected patch direction observed from implementation notes:

```text
The implementation chose (a): bootstrap writes a small local ignored
`*.meta.json` sidecar under `_auth_state/` containing state file name and
session mode. Authenticated capture validates the sidecar and rejects mismatched
session-mode declarations before calling the browser capture path.
```

### M-02

```text
No staging-file cleanup test for authenticated runner on packet-write failure.
```

Minimum closure from prior review:

```text
A test exists that forces packet-write failure after staging files are written,
asserts all four authenticated staging files are absent afterward, and asserts
no packet directory was created.
```

Expected patch direction observed from implementation notes:

```text
`test_authenticated_browser_runner_cleans_staged_files_when_packet_write_fails`
was added to the authenticated browser test file.
```

## Current Target Files And SHA256 Pins

Verify these current target hashes before reviewing:

```text
BC1507835E9E5886516838705789D23865239D49812E4DBD0FF24272E23225B7  .gitignore
F1A84DFA383ECC59095B9C50DB72CA1F1FCFFAC69470D9797126067864D37627  docs\product\source_capture_toolbox\README.md
2EBA0524EC08FDE6BF8EB474F9A820F885E2472B139C56CFE8731AA6725C3908  orca-harness\README.md
611A82D9F7902089727783A43A09925C12F5F70BBABD4DD9DCA5A372D47C6765  orca-harness\docs\source_capture_agent_runbook.md
4FF2F20FEFA01D72E1933E30233A0FF74932C73246EFECA64B337D6CFDCA4586  orca-harness\docs\source_capture_packet.md
A0A6DC42AE621612015DB6F885B7ED75902E4FC0CF1F2CF4EA3B9D9D3E01EC75  orca-harness\source_capture\auth_state.py
EE77C5C60B0733F1B254EBA8E1FF37E453A6AB43931080278F55FF139C619045  orca-harness\source_capture\__init__.py
1BDB04730A9482CCAF793F506E4DD1D29D702928C0EB1444E782B35DEB2867FF  orca-harness\source_capture\adapters\browser_snapshot.py
8C4F959D96BEC4F5A5C15EE744749B78C494B15552F83F87C3AF675807D4B611  orca-harness\runners\run_source_capture_authenticated_browser_packet.py
83DDF7B74790768CBA85279DE34FE3DDB6EFA6D7F83E20F9E4807DB0D8E7BF62  orca-harness\runners\run_source_capture_browser_session_bootstrap.py
ADCFCB1DE5B10C83396C0D25AAB10096FA28F5ACC80E84F1348B67A394D24A4F  orca-harness\tests\unit\test_source_capture_browser_snapshot.py
7637D146CFF75170AD1D559A91834037D1E39BC6E518D493DD01F9E314D35487  orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py
E056B4847509BB495AE2CB43EF3AB20243020B0D7AC4F4D6B658FE4DD3C1B0AC  orca-harness\tests\contract\test_source_capture_browser_snapshot_contract.py
3EBD19D78253A280833F46DF16B3D3B6D6E841ABE3F21B9A39C084351CC41A18  docs\review-outputs\source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md
```

## Required Source-Basis Pins

Verify these source-basis hashes too:

```text
5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1  AGENTS.md
40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F  .agents\workflow-overlay\README.md
7DFBF052A098C0AD77A5598BB6EA4738DA9AD6943D391852DC2E032A173182EF  .agents\workflow-overlay\source-of-truth.md
D7495FA87447D56E8F02096C143796D6C349D35ACC8A2B3628A8157A0B3072B6  .agents\workflow-overlay\source-loading.md
5C6CFC60EFA408A492BF776259745AC25CB630D7B2339365243E68190728B5EA  .agents\workflow-overlay\prompt-orchestration.md
2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199  .agents\workflow-overlay\review-lanes.md
42F085F72F88FC797D470A6DC87CD4C76C8D163AD721C8DE67AF4CD6075AE68D  .agents\workflow-overlay\safety-rules.md
CBA3E118F2D6544DD833A76EC760F7B78E2BE795E259E6D5671B1FD110B9D532  docs\product\data_capture_source_access_boundary_decision_v0.md
119A37A461A6F49A1481282CF0B634FC69FC352F802D0B126D67547AB9006CB2  docs\product\data_capture_source_access_method_plan_v0.md
FC4DB875114C7D82D788E62B7978C390AB0AAF945448A1198116ADECF199E73D  docs\decisions\data_capture_spine_source_access_tooling_build_authorization_v0.md
B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5  docs\product\core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

## Patch Scope

Treat the patch scope as:

- session-mode sidecar path and validation in `auth_state.py`;
- bootstrap runner sidecar write and stdout behavior;
- authenticated packet runner sidecar validation and login-wall heuristic;
- authenticated browser unit tests and browser snapshot contract tests;
- docs describing authenticated browser behavior and non-claims;
- product README direction-change propagation text for authenticated browser v0.

Do not review unrelated Source Capture adapters except where a patch changes a
shared contract test or shared public API.

## Review Questions

Answer these directly in the report:

1. Does the sidecar close M-01 by mechanically binding bootstrap-time session
   mode to capture-time session mode?
2. Can a missing, malformed, mismatched, or path-traversed sidecar create fake
   success, packet write, auth-state leakage, or unclear failure?
3. Does the sidecar introduce sensitive data into packets, raw files, receipt,
   stdout, metadata, docs, test output, or review outputs?
4. Does the bootstrap runner still write no Source Capture Packet and avoid
   password, username, cookie, token, profile, or storage-state-path CLI flags?
5. Does the capture runner reject mode mismatches before browser capture?
6. Does the authenticated staging cleanup test close M-02 with real failure-path
   coverage?
7. Did the patch preserve anonymous Browser Snapshot behavior?
8. Did the patch preserve auth-state path containment under ignored
   `_auth_state/` and avoid printing absolute auth-state paths?
9. Did docs accurately describe sidecar binding without over-authorizing
   password automation, profile/cookie import, anti-detect, proxy behavior,
   CAPTCHA solving, no-entitlement bypass, API use, ECR, Cleaning, or Judgment?
10. Did the product README direction-change propagation remain accurate, or did
    the patch require additional propagation surfaces?
11. Do the validation results reported by the implementer correspond to tests
    that would actually catch the prior failures?
12. Are there any patch-caused blocker or major regressions inside the touched
    scope?

## Expected Validation Evidence To Inspect

The implementer reported these observed results after the patch. Treat them as
evidence to inspect against source, not as proof to accept blindly:

```text
Focused auth/browser tests:
python -m pytest -p no:cacheprovider --basetemp pytest_tmp_auth_browser_patch tests/unit/test_source_capture_authenticated_browser_snapshot.py tests/unit/test_source_capture_browser_snapshot.py tests/contract/test_source_capture_browser_snapshot_contract.py
observed: 23 passed in 0.41s

Source-capture/browser slice:
python -m pytest -p no:cacheprovider --basetemp pytest_tmp_auth_browser_patch_slice tests/unit/test_source_capture_packet.py tests/contract/test_source_capture_packet_no_runtime_imports.py tests/unit/test_source_capture_direct_http.py tests/contract/test_source_capture_direct_http_contract.py tests/unit/test_source_capture_media_asset.py tests/contract/test_source_capture_media_asset_contract.py tests/unit/test_source_capture_archive_org.py tests/contract/test_source_capture_archive_org_contract.py tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_source_capture_authenticated_browser_snapshot.py tests/contract/test_source_capture_browser_snapshot_contract.py
observed: 77 passed in 20.15s

Full harness:
python -m pytest -p no:cacheprovider --basetemp pytest_tmp_auth_browser_patch_full
observed: 145 passed in 27.68s

git diff --check over target files:
observed: exit 0, CRLF warnings only

Runtime secret-flag scan:
rg -n -- "--password|--username|--token|--cookie|--profile|--profile-path|--storage-state-path|os\.environ|getpass" orca-harness\runners\run_source_capture_authenticated_browser_packet.py orca-harness\runners\run_source_capture_browser_session_bootstrap.py orca-harness\source_capture\auth_state.py
observed: no hits

Playwright isolation scan:
rg -n "Playwright|playwright" orca-harness\source_capture\auth_state.py
observed: no hits

Ignored output check:
git status --ignored --short -- orca-harness\_auth_state orca-harness\_test_runs
observed: both ignored; existing permission warnings under _test_runs remain.
```

## Severity Contract

Use these finding severities:

- `critical`: credential/session values or storage-state JSON can leak into
  committed packet artifacts or normal stdout/stderr; no-entitlement bypass,
  password automation, raw profile/cookie import, anti-detect, proxy, CAPTCHA,
  ECR/Cleaning/Judgment leakage, or fake source-success path introduced.
- `major`: M-01 or M-02 not actually closed; sidecar mismatch can produce false
  provenance; staging cleanup can leave authenticated artifacts on normal
  failure; docs materially over-authorize; validation cannot catch the closure
  failure.
- `minor`: bounded correctness or documentation issue that does not reopen
  M-01/M-02 and does not create credential leakage or false provenance.
- `advisory`: optional hardening or future-maintenance issue only.

For this bounded recheck, list new `minor` and `advisory` findings only if they
are patch-caused or materially affect commit/use of this authenticated browser
surface. Do not inventory unrelated pre-existing issues.

## Required Report Shape

Write the durable report to:

```text
docs/review-outputs/source_capture_authenticated_browser_snapshot_post_patch_blast_radius_recheck_v0.md
```

The report must include:

1. Retrieval header.
2. Preflight record.
3. Hash verification table.
4. `SOURCE_CONTEXT_READY` / incomplete declaration.
5. Method application declarations.
6. Closure status for M-01 and M-02.
7. Any new blocker/major findings, findings-first.
8. Bounded minor/advisory findings only when patch-caused and decision-relevant.
9. Non-findings for credential leakage, path traversal, bootstrap no-packet,
   anonymous compatibility, source-access boundary, and docs over-authorization
   if cleared.
10. Recommendation using one of:
    - `closure_confirmed_commit_unblocked`
    - `closure_confirmed_with_minor_advisory_carry`
    - `revise_before_commit`
    - `blocked_hash_or_source_context`
11. Review-use boundary:

```text
Review findings are decision input only. This report does not approve,
validate, require remediation, authorize patches, authorize commits, or authorize
production/runtime source capture. Commit, patch, or runtime use requires
separate owner action.
```

## Chat Return Shape

After the durable report is written and verified, return this compact YAML in
chat:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/source_capture_authenticated_browser_snapshot_post_patch_blast_radius_recheck_v0.md
  recommendation: closure_confirmed_commit_unblocked | closure_confirmed_with_minor_advisory_carry | revise_before_commit | blocked_hash_or_source_context
  closure_status_by_finding:
    M-01: closed | open | not_assessable
    M-02: closed | open | not_assessable
  new_blocking_or_major_findings: []
  advisory_or_minor_carries: []
  next_action: "<one sentence>"
```

Do not patch files. Do not stage, commit, push, install, run browsers, use
network, or create packets. This is read-only review plus durable report write
only.
