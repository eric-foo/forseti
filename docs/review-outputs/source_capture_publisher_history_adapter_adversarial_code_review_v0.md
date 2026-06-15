# Publisher-History Capture Adapter Adversarial Code Review

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated cross-vendor adversarial code review of the publisher-history
  capture adapter (PR #89): non-2xx / error-body honesty (PH-01/02/03), body
  and selection status gating, and re-capture / limitation visibility. Re-landed
  after #89 merged ahead of this review's patch. Advisory findings only; no
  validation claim and no readiness verdict.
authority_boundary: retrieval_only
review_type: delegated_adversarial_code_review
access_mode: no_repo_advisory
commission: PR #89 publisher-history capture adapter
authored_by: claude-opus-4.8
reviewed_by: gpt-5-codex
de_correlation_bar: cross_vendor_discovery
review_object:
  - orca-harness/source_capture/adapters/publisher_history.py
  - orca-harness/tests/unit/test_source_capture_publisher_history.py
  - orca-harness/tests/contract/test_source_capture_publisher_history_contract.py
  - orca-harness/source_capture/adapters/__init__.py
base: main
head: 64be253
worktree: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\capture-publisher-history-adapter
source_context_ready: true
```

## Findings

### PH-01 - major - Preserved HTTP error bodies can be treated as successful listing/body evidence

**Cites:** `orca-harness/source_capture/adapters/direct_http.py:150`, `orca-harness/source_capture/adapters/publisher_history.py:165`, `orca-harness/source_capture/adapters/publisher_history.py:186`, `orca-harness/source_capture/adapters/publisher_history.py:190`, `orca-harness/source_capture/adapters/publisher_history.py:360`, `orca-harness/source_capture/adapters/publisher_history.py:385`, `orca-harness/source_capture/adapters/publisher_history.py:389`, `orca-harness/tests/unit/test_source_capture_publisher_history.py:419`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:113`

`direct_http` intentionally returns `DirectHttpCaptureSuccess` for a non-empty non-2xx response, preserving the body and recording an `access_failed` limitation note. The publisher-history adapter then treats every `DirectHttpCaptureSuccess` listing as parseable availability input and every `DirectHttpCaptureSuccess` body as a retrieved body. There is no status/limitation gate before `parse_mediawiki_revisions` / `parse_github_commits`, no status gate before selection, and no status gate after fetching the selected revision body.

That means a non-2xx listing with a valid-looking revision JSON body can still select a revision, and a non-2xx body such as a raw GitHub 404/403 page can be returned as `body_result=DirectHttpCaptureSuccess` rather than a PARTIAL/non-usable body. The existing unit test at `test_source_capture_publisher_history.py:419` only covers a non-2xx listing with non-JSON text, so it fake-passes the desired split without proving the adapter refuses valid-shaped error bodies. The slice-F spec explicitly treats non-2xx as non-usable, not merely as a body-preserved success.

**Impact:** Fake-success path. Availability/body separation is present structurally, but a preserved error body can still be interpreted downstream as a usable publisher-history body. This violates the "availability != body" honesty boundary and can let a failed or blocked body retrieval look like a GO if downstream code checks only `isinstance(body_result, DirectHttpCaptureSuccess)`.

**Minimum closure condition:** Publisher-history must separate "body preserved for evidence" from "body usable": non-2xx listing responses must not produce selected revisions, and non-2xx body responses must be recorded as PARTIAL/non-usable even when the bytes are preserved. Add tests for non-2xx valid-shaped listing JSON and non-2xx body-with-bytes for both MediaWiki and GitHub.

**Next authorized action:** CA adjudication, then advisory remediation by the owning executor if accepted. No patch queue is emitted by this review.

### PH-02 - major - MediaWiki body retrieval is not verified against the selected revision identity/timestamp

**Cites:** `orca-harness/source_capture/adapters/publisher_history.py:237`, `orca-harness/source_capture/adapters/publisher_history.py:247`, `orca-harness/source_capture/adapters/publisher_history.py:190`, `orca-harness/source_capture/adapters/publisher_history.py:197`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:122`

The MediaWiki content URL requests `rvprop=content|timestamp|ids` for `rvstartid=<revid>`, but the adapter never parses the content response to confirm the returned `revid` and `timestamp` match `selected_revision.identity` and `selected_revision.served_timestamp`. It simply stores the direct HTTP result as the body result.

AR-02 requires publisher-history to bind the requested revision's timestamp and identity, not just carry an opaque revision ID. The listing selection does use parsed timestamp proof, but body retrieval remains unproofed: a 2xx response with a wrong revision, API warning payload, or other valid JSON wrapper can be preserved as the selected body without a body-level identity/timestamp verdict. GitHub is less exposed because the raw URL is pinned by commit SHA, but it still inherits PH-01's body-usability status gap.

**Impact:** The adapter can prove "a selected revision exists" without proving "the body returned belongs to that selected revision." That leaves the AR-02 served-time/identity proof incomplete for the actual preserved body.

**Minimum closure condition:** For MediaWiki, parse the content response enough to assert returned revision identity and normalized timestamp equal the selected revision before treating the body as usable. Missing, unparseable, mismatched, or non-2xx content responses must become a visible PARTIAL/verification failure, not a clean body result. Add mismatch and missing-proof tests.

**Next authorized action:** CA adjudication, then advisory remediation by the owning executor if accepted. No patch queue is emitted by this review.

### PH-03 - minor - One-item history queries can convert an unproofed top entry into an unproven NO-GO instead of continuing to older proofed entries

**Cites:** `orca-harness/source_capture/adapters/publisher_history.py:216`, `orca-harness/source_capture/adapters/publisher_history.py:229`, `orca-harness/source_capture/adapters/publisher_history.py:420`, `orca-harness/source_capture/adapters/publisher_history.py:425`, `orca-harness/source_capture/adapters/publisher_history.py:283`, `orca-harness/source_capture/adapters/publisher_history.py:287`, `orca-harness/source_capture/adapters/publisher_history.py:456`, `orca-harness/source_capture/adapters/publisher_history.py:459`, `orca-harness/source_capture/adapters/publisher_history.py:504`

Both rungs ask the publisher for a single result (`rvlimit=1`, `per_page=1`) and the parsers correctly skip entries missing a parseable timestamp or identity. But if the single returned top entry is unproofed, the adapter has no bounded cursor/page fetch to find the next older proofed entry. It returns `selected_revision=None` with a generic selection warning, which is indistinguishable from a true all-miss NO-GO at the result-shape level.

This is not a no-lookahead leak: the code still refuses post-cutoff or unproofed entries. The problem is availability honesty under the prompt's pagination/continuation edge case. "Skip the unproofed entry" is only complete if the adapter either continues through a bounded older-entry window or explicitly reports the rung as proof-blocked rather than as an ordinary no-pre-cutoff miss.

**Impact:** False NO-GO / under-capture risk on malformed, partial, or API-warning history pages. It is lower severity because normal MediaWiki and GitHub API entries should carry timestamps, but the adapter's edge-case behavior does not yet prove bounded exhaustion.

**Minimum closure condition:** Either fetch a bounded page/window and select the newest proofed entry `<= cutoff`, or expose a distinct proof-blocked/verification-failed outcome when the first entry cannot carry AR-02 proof. Add tests where the first returned/paged entry is unproofed and an older proofed entry exists.

**Next authorized action:** CA adjudication. This can be accepted as a known limitation only if the owner explicitly accepts the false-NO-GO risk.

## Verdict

`patch_before_acceptance`

The adapter is directionally sound on the core timestamp comparison: parsed timestamps are normalized to UTC, equality with cutoff is allowed, post-cutoff parsed revisions are excluded client-side, and missing/unparseable served timestamps are not trusted. The export surface is present, all adapter HTTP calls go through `fetch_direct_http_capture`, and the unit/contract tests are offline loopback/AST tests.

The review does not support accepting the adapter as-is because PH-01 creates a real fake-success path for preserved HTTP error bodies, and PH-02 leaves MediaWiki body identity/timestamp proof incomplete. These are adapter-level patchable issues; `NEEDS_ARCHITECTURE_PASS` is not warranted.

## Residual Risk

After PH-01 and PH-02 are fixed, residual risk remains around the real external API semantics for MediaWiki `rvstart/rvdir=older` and GitHub `until` ordering/inclusivity. The current tests simulate those semantics locally but do not prove the live API contracts. A narrow documentation/source-citation pass or live-probe fixture may be useful before stronger runtime claims, but it is outside this no-repo advisory review's acceptance authority.

## Source-Read Ledger

- `AGENTS.md` and `.agents/workflow-overlay/README.md`: project authority and overlay entrypoint.
- `.agents/workflow-overlay/decision-routing.md`: Cynefin routing requirement for delegated review work.
- `.agents/workflow-overlay/review-lanes.md` and `.agents/workflow-overlay/delegated-review-patch.md`: advisory no-repo review boundary, findings-first output, no patch queue, provenance/de-correlation fields.
- `workflow-deep-thinking` then `workflow-code-review` skill files: reference-loaded before applying source-gated review mechanics.
- `orca-harness/source_capture/adapters/publisher_history.py`: commissioned implementation target.
- `orca-harness/tests/unit/test_source_capture_publisher_history.py`: commissioned unit tests.
- `orca-harness/tests/contract/test_source_capture_publisher_history_contract.py`: commissioned import-discipline contract test.
- `orca-harness/source_capture/adapters/__init__.py`: commissioned export surface.
- `orca-harness/source_capture/adapters/archive_org.py` and `direct_http.py`: mirrored adapter/direct-fetch pattern evidence.
- `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md` lines 100-126 from the `capture-fallback-ladder-spec` worktree: slice E, slice F, and AR-02/G authority.

## Verification Run

```text
workdir: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\capture-publisher-history-adapter\orca-harness
command: python -m pytest -p no:cacheprovider -q tests/unit/test_source_capture_publisher_history.py tests/contract/test_source_capture_publisher_history_contract.py
observed: 16 passed
```

Passing tests are validation evidence only for the covered loopback and AST-import cases. They do not close PH-01 or PH-02 because the preserved-error-body and body identity/timestamp mismatch cases are not exercised.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized by the Chief Architect. Because this is `no_repo` advisory mode, the CA applies any accepted patch and a bounded same-vendor post-patch recheck closes the two-bar loop before a patch is final.
