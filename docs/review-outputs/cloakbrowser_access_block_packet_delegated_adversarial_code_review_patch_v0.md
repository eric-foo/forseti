# CloakBrowser Access-Block Packet Delegated Adversarial Code Review-And-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch output
scope: >
  Bounded adversarial review-and-patch of the CloakBrowser access-block packet
  preservation change. Findings and diff are decision input for CA adjudication.
  Not approval, readiness, or auto-keep authority.
use_when:
  - Inspecting access-block packet findings or the proposed bounded patch.
  - Tracing CA adjudication to this delegated review.
commission:
  author_family: OpenAI/Codex
  delegate_family: Anthropic/Claude
  de_correlation_satisfied: true
review_authority_boundary: ca_adjudication_input_only
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

---

## 1. SOURCE_CONTEXT_READY

All required files were read before analysis:

- `AGENTS.md` — loaded in session context
- `.agents/workflow-overlay/README.md` — read
- `.agents/workflow-overlay/decision-routing.md` — read
- `.agents/workflow-overlay/review-lanes.md` — read
- `.agents/workflow-overlay/delegated-review-patch.md` — read
- `docs/product/source_capture_toolbox/README.md` — read
- `orca-harness/docs/source_capture_agent_runbook.md` — read (first 80 lines sufficient)
- `orca-harness/source_capture/adapters/cloakbrowser_snapshot.py` — read in full
- `orca-harness/runners/run_source_capture_cloakbrowser_packet.py` — read in full
- `orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py` — read in full
- `orca-harness/tests/contract/test_source_capture_cloakbrowser_snapshot_contract.py` — read in full
- `orca-harness/source_capture/adapters/direct_http.py` — read (optional, for parallel-path comparison)

---

## 2. Findings (ordered by severity)

### F1 — MINOR: Non-claims list not adjusted for access-blocked captures

**File:** `orca-harness/runners/run_source_capture_cloakbrowser_packet.py`
**Lines:** `_cloakbrowser_snapshot_non_claims` function (original ~258–268) and its
call site (~194)

**Evidence:**

`_cloakbrowser_snapshot_non_claims(proxy_profile=proxy_profile)` — the function
accepted only `proxy_profile`. For both clean captures and blocked captures, the
receipt `non_claims` field was identical. A consumer reading only
`manifest["receipt_metadata"]["non_claims"]` would see a generic list
("not content sufficiency proof", etc.) with no blocked-specific signal, even
when the capture was an access-block interstitial.

The receipt _summary_ did say "source content was not captured" and `access_posture`
started with `access_failed`. But the non-claims section — which is the conventional
machine-readable list of what this packet cannot be used to claim — did not include
an entry specifically barring the blocked packet from being treated as a source-content
capture.

**Risk:** Downstream consolidation, quality, or ECR layers that scan `non_claims`
without also reading `access_posture` or `receipt_summary` would not see an
explicit "not source-content capture" signal. Low probability given the other
strong signals, but a defense-in-depth gap given the commission's mandate to be
hostile to any path that could make a block interstitial into a source-content claim.

**Minimum closure condition:** For access-blocked captures, `non_claims` must
include at least one entry that explicitly prohibits treating the packet as a
source-content capture.

**Patched:** Yes.

---

### F2 — MINOR: Normal-capture test does not assert `access_blocked=False`

**File:** `orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py`
**Test:** `test_fetch_cloakbrowser_snapshot_capture_with_fake_engine_records_method_provenance`

**Evidence:**

The normal-capture provenance test thoroughly checked method_category, proxy fields,
viewport, screenshot_mode, and byte counts — but did not assert:
- `result.metadata["access_blocked"] is False`
- `result.metadata["access_block_reason"] is None`
- `result.access_block_reason is None`
- `result.limitation_notes == []`

If a regression caused the access-block detection to fire on non-block pages (or
the field wiring to invert), this test would not catch it.

**Risk:** Regression in `_detect_access_blocked_page` producing false positives
on normal pages would be silent in the provenance test. Low probability given the
specific dual-phrase Reddit check, but the gap weakens the test coverage claimed.

**Minimum closure condition:** The provenance test must assert that a normal
(non-block) capture carries `access_blocked=False`, `access_block_reason=None`,
`access_block_reason` field `None`, and `limitation_notes=[]`.

**Patched:** Yes.

---

### F3 — ADVISORY (not patched): `CloakBrowserSnapshotFailureKind.ACCESS_BLOCKED` is now dead code

**File:** `orca-harness/source_capture/adapters/cloakbrowser_snapshot.py` line 48;
`orca-harness/runners/run_source_capture_cloakbrowser_packet.py` `_failure_report_token`

**Evidence:**

Before this patch, the adapter returned
`CloakBrowserSnapshotFailure(failure_kind=ACCESS_BLOCKED)` for detected block
pages. After the patch, detected block pages return `CloakBrowserSnapshotSuccess`
with `access_block_reason` set. `CloakBrowserSnapshotFailureKind.ACCESS_BLOCKED`
and its `_failure_report_token` branch are no longer reachable.

**Risk:** No safety risk. The dead code does not create a false-success path —
if it were ever reached again, it would produce an error exit, not a packet
write. The enum member could be useful if a future adapter variant needs to fail
hard on an unrenderable block. Retaining it as a semantic sentinel is acceptable.

**Decision:** Left in place. No patch.

---

## 3. Patch Summary

Two material findings patched, one advisory finding left unpatch-recommended.

**F1 patch — `run_source_capture_cloakbrowser_packet.py`:**

- `_cloakbrowser_snapshot_non_claims` signature extended with
  `access_block_reason: str | None`.
- When `access_block_reason is not None`, prepend
  `"not source-content capture; access-block page artifacts only"` before the
  base non-claims list.
- Call site updated to pass `capture_result.access_block_reason`.
- Existing non-blocked call sites (both with and without proxy) are unaffected:
  when `access_block_reason is None`, the base list is returned unchanged.

**F2 patch — `tests/unit/test_source_capture_cloakbrowser_snapshot.py`:**

- Added four assertions to the normal-capture provenance test:
  `access_blocked is False`, `access_block_reason is None` (metadata), field
  `access_block_reason is None`, `limitation_notes == []`.
- Added one assertion to `test_cloakbrowser_snapshot_runner_writes_access_blocked_packet`:
  the `non_claims` list must contain at least one item with "not source-content
  capture".

---

## 4. Unified Diff

```diff
diff --git a/orca-harness/runners/run_source_capture_cloakbrowser_packet.py b/orca-harness/runners/run_source_capture_cloakbrowser_packet.py
--- a/orca-harness/runners/run_source_capture_cloakbrowser_packet.py
+++ b/orca-harness/runners/run_source_capture_cloakbrowser_packet.py
@@ -191,7 +191,10 @@ def run_source_capture_cloakbrowser_packet(
             receipt_summary=_receipt_summary(
                 source_family=source_family,
                 access_block_reason=capture_result.access_block_reason,
             ),
-            receipt_non_claims=_cloakbrowser_snapshot_non_claims(proxy_profile=proxy_profile),
+            receipt_non_claims=_cloakbrowser_snapshot_non_claims(
+                proxy_profile=proxy_profile,
+                access_block_reason=capture_result.access_block_reason,
+            ),
         )
     finally:
         for staging_path in written_paths:
@@ -258,12 +261,19 @@ def _cloakbrowser_snapshot_non_claims(*, proxy_profile: ProxyProfile | None) -> list[str]:
-def _cloakbrowser_snapshot_non_claims(*, proxy_profile: ProxyProfile | None) -> list[str]:
-    if proxy_profile is None:
-        return CLOAKBROWSER_SNAPSHOT_NON_CLAIMS
-    return [
-        item
-        for item in CLOAKBROWSER_SNAPSHOT_NON_CLAIMS
-        if item != "not proxy use"
-    ] + [
-        "not proxy endpoint or credential disclosure",
-        "not proxy success or block-evasion proof",
-    ]
+def _cloakbrowser_snapshot_non_claims(
+    *, proxy_profile: ProxyProfile | None, access_block_reason: str | None
+) -> list[str]:
+    if proxy_profile is None:
+        base: list[str] = list(CLOAKBROWSER_SNAPSHOT_NON_CLAIMS)
+    else:
+        base = [
+            item
+            for item in CLOAKBROWSER_SNAPSHOT_NON_CLAIMS
+            if item != "not proxy use"
+        ] + [
+            "not proxy endpoint or credential disclosure",
+            "not proxy success or block-evasion proof",
+        ]
+    if access_block_reason is not None:
+        return ["not source-content capture; access-block page artifacts only"] + base
+    return base

diff --git a/orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py b/orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
--- a/orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
+++ b/orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
@@ -102,6 +102,10 @@ def test_fetch_cloakbrowser_snapshot_capture_with_fake_engine_records_method_pro
     assert result.metadata["rendered_dom_byte_count"] == len(result.rendered_dom.encode("utf-8"))
     assert result.metadata["visible_text_byte_count"] == len(result.visible_text.encode("utf-8"))
     assert result.metadata["screenshot_byte_count"] == len(result.screenshot_png)
+    assert result.metadata["access_blocked"] is False
+    assert result.metadata["access_block_reason"] is None
+    assert result.access_block_reason is None
+    assert result.limitation_notes == []
     assert engine.capture_kwargs == {

@@ -1170,6 +1170,8 @@ def test_cloakbrowser_snapshot_runner_writes_access_blocked_packet(
     visible_text = (output_dir / "raw" / "02_cloakbrowser_visible_text.txt").read_text(
         encoding="utf-8"
     )
     assert "You've been blocked by network security" in visible_text
+    non_claims = manifest["receipt_metadata"]["non_claims"]
+    assert any("not source-content capture" in item for item in non_claims)
```

---

## 5. Validation Command and Observed Output

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q --basetemp orca-harness\_pytest_tmp_cloakbrowser_review orca-harness\tests\unit\test_source_capture_cloakbrowser_snapshot.py orca-harness\tests\contract\test_source_capture_cloakbrowser_snapshot_contract.py
```

**Pre-patch observed output (32 tests):**
```
................................                                         [100%]
```

**Post-patch observed output (32 tests):**
```
................................                                         [100%]
```

All 32 tests pass after the patch.

---

## 6. Review Findings Supplement — Commission Questions Answered

**Q1. Does a rendered Reddit access-block page always write an inspectable packet without hiding that source content was not captured?**

Yes. The adapter's `_detect_access_blocked_page` function detects the known
Reddit network-security block via a dual-phrase probe against title, visible
text, and the first 5,000 characters of the DOM. When detected, the adapter
returns `CloakBrowserSnapshotSuccess` with `access_block_reason` set rather than
a failure. The runner then writes a packet with:
- `access_posture` beginning with `"cloakbrowser_snapshot access_failed with access block"`
- `limitations` containing `"access_failed: CloakBrowser rendered an access-block/interstitial page..."`
- `receipt_metadata["summary"]` saying "source content was not captured"
- `metadata["access_blocked"] = True` and `metadata["access_block_reason"]` set
- (Post-F1 patch) `non_claims` prepended with "not source-content capture; access-block page artifacts only"

No hiding path was found.

**Q2. Is exit code 0 for packet-written blocked captures consistent with runner semantics?**

Yes. Direct HTTP (`direct_http.py`) follows the same doctrine: HTTP 403 returns
`DirectHttpCaptureSuccess` with exit code 0 and `access_failed` in limitations.
The agent runbook explicitly states "exit code 0 proves only that bytes were
preserved into a packet." The pattern is consistent across the armory.

**Q3. Does the new `access_block_reason` field stay non-secret-bearing and avoid schema drift?**

Yes. `access_block_reason` holds one of a small set of named string tokens
(e.g., `"reddit_network_security_block"`) — never a credential, endpoint, or
user value. The metadata fields `access_blocked` (bool) and `access_block_reason`
(str | None) are additive; non-blocked captures receive `False`/`None`. The
contract test `test_cloakbrowser_snapshot_adapter_does_not_expose_secret_or_persistent_profile_terms`
still passes. Existing success-path JSON consumers ignore unknown fields.

**Q4. Are access-block artifacts size-capped before packet writing, and do staging files clean up on failure?**

Yes. The size-cap check (`oversized` dict, lines 173–193) runs before
`_detect_access_blocked_page` (line 203). An oversized block page returns
`CloakBrowserSnapshotFailure(SIZE_CAP_EXCEEDED)` — exit code 3, no packet.
Staging cleanup is unconditional in the `finally` block; tested by
`test_cloakbrowser_snapshot_runner_cleans_staged_files_when_metadata_write_fails`.

**Q5. Are receipt summary, access posture, limitations, and non-claims strong enough to prevent downstream claim misuse?**

Substantially yes, with the F1 patch closing the one identified gap. Before the
patch, the non-claims list was identical for blocked and clean captures. After
the patch, blocked-capture non-claims are prepended with
"not source-content capture; access-block page artifacts only", making the
non-claims section unambiguous.

**Q6. Would the tests fail under old behavior?**

Yes. `test_fetch_cloakbrowser_snapshot_capture_preserves_access_blocked_reddit_security_page`
asserts `isinstance(result, CloakBrowserSnapshotSuccess)` — old behavior returned
`CloakBrowserSnapshotFailure`. `test_cloakbrowser_snapshot_runner_writes_access_blocked_packet`
asserts exit code 0 and access_posture/limitations/summary signals — old behavior
returned exit code 3 with no packet. `CloakBrowserSnapshotSuccess.access_block_reason`
did not exist in old code, so fake-result construction would also fail.

**Q7. Any off-scope design issues requiring `NEEDS_ARCHITECTURE_PASS`?**

No. The patch is cleanly bounded to the access-block packet preservation behavior.
No packet schema doctrine, source-quality vocabulary, Reddit consolidation,
archive fallback, proxy profile, or commercial API routing was touched.

---

## 7. Residual Risk

- **Undetected block patterns:** `_detect_access_blocked_page` is heuristic and
  currently matches only the known Reddit network-security block. A new Reddit
  block page variant, a Cloudflare challenge, or a generic interstitial would not
  be detected — the packet would be written as if source content was captured.
  This is a pre-existing gap, not introduced by this patch. Future block-pattern
  expansion is outside the current commission scope.

- **Dead `ACCESS_BLOCKED` failure kind:** The enum member and its runner handler
  remain as dead code. No safety risk; left intact as a semantic sentinel for
  potential future use.

- **Non-claims for proxy + blocked combination:** The post-F1 patch correctly
  prepends the blocked non-claim for both proxy and non-proxy paths. The combined
  proxy + blocked case (not separately tested in the runner) was not separately
  tested but is mechanically covered by the function logic.

---

## 8. Verdict

**`PATCHED_FOR_CA_ADJUDICATION`**

Two MINOR findings patched. One ADVISORY finding (dead code) left in place with
rationale. All 32 pre-existing tests continue to pass post-patch. No off-scope
changes were made.

This diff and verdict are decision input for CA adjudication. They are not
approval, readiness, validation, or auto-keep authority. The CA reserves final
authority over what is kept.
