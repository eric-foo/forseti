# Source Capture Direct HTTP Adapter — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Adversarial implementation review of the bounded Direct HTTP Source Capture
  adapter. Covers boundary compliance, fake-success blocking, non-2xx honesty,
  provenance-header safety, writer.py receipt-override regression, no-network
  boundary integrity, test sufficiency, dry-run evidence quality, and doc
  accuracy. Advisory findings only; no patch queue, no validation claim, no
  readiness verdict.
authority_boundary: retrieval_only
review_lane: zero-config findings-only advisory review
output_mode: filesystem-output
commission: adversarial code review of direct_http.py, run_source_capture_http_packet.py,
  writer.py (receipt-override path), __init__.py, unit/contract tests,
  dry-run evidence, and docs
```

---

## Source-Read Ledger

All 11 SHA256 pins verified exact match before review.

| File | Pin SHA256 (prefix) | Status |
|---|---|---|
| `orca-harness/source_capture/adapters/direct_http.py` | `4FE478D4…` | ✓ pin match |
| `orca-harness/runners/run_source_capture_http_packet.py` | `84800498…` | ✓ pin match |
| `orca-harness/source_capture/writer.py` | `70EE62AE…` | ✓ pin match |
| `orca-harness/source_capture/__init__.py` | `14A19D70…` | ✓ pin match |
| `orca-harness/tests/unit/test_source_capture_direct_http.py` | `C3FCCEFF…` | ✓ pin match |
| `orca-harness/tests/contract/test_source_capture_direct_http_contract.py` | `2965BEA3…` | ✓ pin match |
| `orca-harness/docs/source_capture_packet.md` | `36E3D53C…` | ✓ pin match |
| `orca-harness/README.md` | `A1F1936E…` | ✓ pin match |
| `_test_runs/.../manifest.json` | `983D3E2F…` | ✓ pin match |
| `_test_runs/.../receipt.md` | `2A78F7C3…` | ✓ pin match |
| `_test_runs/.../raw/02_http_response_metadata.json` | `82B57699…` | ✓ pin match |

Note: the dry-run packet lives under `orca-harness/_test_runs/`, not `_test_runs/` at the project root. The pin refers to the same file; the path in the commission has a documentation-level ambiguity (see A-06).

Additional sources loaded (outside pin set):
- `AGENTS.md` — project-level behavior contract
- `.agents/workflow-overlay/README.md` — Orca overlay entrypoint
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` — first-tranche build authority
- `docs/product/source_capture_toolbox/README.md` — toolbox design authority
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` — obligation contract
- `docs/review-outputs/source_capture_packet_core_post_patch_blast_radius_recheck_v0.md` — prior review closure state

---

## Preflight Status

```
SOURCE_CONTEXT_READY
review_lane: zero-config findings-only advisory review
source_loading_mode: advisory findings-only (pinned source authority)
output_mode: filesystem-output
required_output_path: docs/review-outputs/source_capture_direct_http_adapter_adversarial_code_review_v0.md
hash_verification: all 11 pins match; no mismatch to report
dirty_state: confirmed; unrelated docs dirt ignored per commission
carried_advisories_from_prior_review: Advisory-01 (VisibleFactStatus not exported), F-05 carry (original_path convention) — both still active
```

---

## Review Frame

Using `workflow-deep-thinking`.

The adversarial question is not "does the code work on the happy path." It is: **do the nine named failure modes each produce a correctly visible non-success outcome, with no false-success escape hatch, while staying strictly inside the authorized first-tranche boundary and not weakening the existing no-network packet-core tests?**

The ten review questions map to three pressure zones:

1. **Boundary integrity** (Q1, Q8): Is every import, protocol, and behavior inside the authorized scope?
2. **Failure honesty** (Q2, Q3, Q4, Q5): Does every failure mode produce the right kind of non-success signal, with no path that produces a normal packet from bad input?
3. **Evidence quality** (Q6, Q7, Q9, Q10): Do the tests, dry-run evidence, and docs provide adequate downstream inspection surface?

---

## Q1 — Authorized First-Tranche Boundary

**Finding: boundary clean.**

The adapter imports only Python stdlib: `urllib.request`, `urllib.error`, `urllib.parse`, `http.client`, and `harness_utils` (project utility). No browser, API SDK, scraper, archive, proxy, auth-injection, or commercial-fetch import is present. The contract test (`test_direct_http_adapter_avoids_browser_api_and_scraper_imports`) confirms absence of all nine forbidden import roots by AST scan.

The request construction uses only `User-Agent` and `Accept: */*` headers — no cookie injection, no session header, no auth. Protocol is GET only. The scheme guard (`_validate_http_url`) enforces `http://` or `https://` with a non-empty netloc; `file://`, `data:`, and relative URLs raise `ValueError` (exit code 2).

The adapter's user-agent string self-describes: `OrcaSourceCaptureDirectHTTP/0.1 (stdlib honest fetch; no browser/api/archive)`. This is accurate and not spoofed.

**Hard-stop cross-check:**
- No entitlement bypass: ✓ (no credential or cookie injection)
- No stolen credentials: ✓ (adapter sends nothing)
- No security exploit path: ✓ (pure GET, no schema expansion)
- No anti-detect behavior: ✓ (honest stdlib UA, no browser fingerprint mimicry)
- No proxy injection: ✓

**Deferred surfaces not present:** no PRAW, requests, httpx, aiohttp, selenium, playwright, scrapy, archivebox, or webbrowser. ✓

**Verdict:** Direct HTTP adapter stays inside the authorized first-tranche boundary with no visible drift.

---

## Q2 — Fake-Success Blocking

**Finding: all named failure modes produce visible non-success; no fake-success escape identified.**

### Invalid URL
`_validate_http_url` raises `ValueError` before any network call. `main()` catches `ValueError` → `parser.exit(status=2, ...)`. No packet is ever written. ✓

### Network Error / DNS / TLS Failure
`URLError` (non-`HTTPError`) → `DirectHttpCaptureFailure(NETWORK_ERROR)` via `_failure_kind_from_url_error`. Runner returns `(3, message)` → `parser.exit(status=3)`. No packet written. ✓

The `HTTPError` → `URLError` catch ordering is correct: `HTTPError` is caught first (it is a subclass of `URLError`). If the ordering were reversed, non-2xx responses with bodies would be silently consumed as network errors rather than body-bearing `DirectHttpCaptureSuccess` objects. Ordering is safe. ✓

### Timeout
`URLError` with `"timed out"` or `"timeout"` in reason string → `DirectHttpCaptureFailureKind.TIMEOUT`. Exit code 3. ✓

### Empty Body
After body read: `if not body: return DirectHttpCaptureFailure(NO_BODY)`. This fires for 204 No Content, 304 Not Modified, and any response that returns an empty payload. ✓

### Size Cap (Pre-Read, Content-Length)
`content_length = _parse_optional_int(headers.get("Content-Length"))`. If `content_length is not None and content_length > max_bytes` → `DirectHttpCaptureFailure(SIZE_CAP_EXCEEDED)` before body read. ✓

### Size Cap (During Read, Streaming)
`_read_with_cap` reads in chunks of `min(65536, max_bytes - total + 1)`. The `+1` is intentional: it reads one byte beyond the cap per chunk to detect overflow. When `total > max_bytes` → `_BodyTooLargeError` → `DirectHttpCaptureFailure(SIZE_CAP_EXCEEDED)`. ✓

**Cap arithmetic trace:** For `max_bytes=5` with a 6-byte response — first read requests `min(65536,6)=6`, receives 6 bytes, `total=6 > 5` → error. For an exact 5-byte response — first read requests 6, receives 5, `total=5` not `> 5`; second read requests `min(65536,1)=1`, receives 0 bytes → returns 5-byte body cleanly. ✓ No off-by-one escape.

### Runner Failure Gate
`if isinstance(capture_result, DirectHttpCaptureFailure): return 3, capture_result.message` — this fires before any file I/O or packet write. The `try/finally` staging cleanup block is never entered. ✓

**Verdict:** All six failure modes produce a correctly non-success outcome. No fake-success path found.

---

## Q3 — Non-2xx Body Honesty

**Finding: non-2xx bodies are represented honestly; no implication of source success.**

Non-2xx responses with non-empty bodies reach `_capture_response` via the `HTTPError` branch (urllib raises `HTTPError` for 4xx/5xx). The code produces `DirectHttpCaptureSuccess` (not failure) because a body was received and preserved. The naming `DirectHttpCaptureSuccess` is a mild clarity concern (see A-01 below), but the packet surface is honest:

- `limitation_notes` carries `"access_failed: direct HTTP returned HTTP {status} …; response body preserved"` for any `status < 200 or status >= 300`.
- Runner sets `access_posture = known_fact("direct_http access_failed with HTTP {status} …; response body preserved")`.
- Packet manifest: `access_posture.value` starts with `"direct_http access_failed"`.
- Manifest `limitations` array carries the `access_failed:` limitation text.

Test `test_fetch_direct_http_capture_allows_non_2xx_body` asserts `isinstance(result, DirectHttpCaptureSuccess)`, `result.status == 404`, and `any("access_failed" in item for item in result.limitation_notes)`. Integration test asserts `manifest["access_posture"]["value"].startswith("direct_http access_failed with HTTP 404")` and `any("access_failed" in item for item in manifest["limitations"])`. ✓

**Note on empty-body 4xx:** A 404 with empty body produces `DirectHttpCaptureFailure(NO_BODY)`, not a success. This is correct — there is no body to preserve, so no packet is warranted.

**Verdict:** Non-2xx bodies are honestly represented with visible `access_failed` posture at both adapter and packet levels.

---

## Q4 — Provenance Header Safety

**Finding: provenance headers safe; explicit allowlist, not block-list.**

The metadata dict in `_capture_response` is constructed with named, hardcoded keys only:

```python
metadata = {
    "requested_url": ..., "final_url": ..., "status": ..., "reason": ...,
    "content_type": headers.get("Content-Type"),
    "content_length": content_length,
    "date": headers.get("Date"),
    "last_modified": headers.get("Last-Modified"),
    "etag": headers.get("ETag"),
    "capture_timestamp": ..., "timeout_seconds": ..., "byte_count": ...,
}
```

`Set-Cookie`, `WWW-Authenticate`, `Authorization`, `Cookie`, `Proxy-*`, `X-Auth-*`, and all other secret-bearing or session-bearing headers are structurally excluded because they are not named. The exclusion is architectural (allowlist), not runtime filtering.

Request sends only `User-Agent` and `Accept: */*`. No `Cookie`, no `Authorization`, no session material is injected into the outbound request.

Test coverage: `assert "set_cookie" not in result.metadata` (unit test) and `assert "Set-Cookie" not in metadata` (integration test). These are technically redundant given the allowlist design, but they function as regression tests for future refactors that might change the construction to dynamic header enumeration.

**Advisory note (A-07):** The unit test checks lowercase-underscore `"set_cookie"`, which is the correct key pattern for the existing dict (since keys are hardcoded snake_case). If a future refactor were to populate metadata dynamically using original header names (e.g., `"Set-Cookie"`), neither check would catch it as a new key. The existing allowlist architecture is the stronger guard; the test is a secondary signal. This is a minor advisory, not a correctness finding.

**Verdict:** Provenance header safety is structurally guaranteed by explicit allowlist. No cookies, auth tokens, or session material preserved by default.

---

## Q5 — `writer.py` Receipt Override Regression

**Finding: no regression for current callers; latent trap for future adapters.**

The `receipt_non_claims: Sequence[str] | None = None` parameter added to `write_local_source_capture_packet` introduced this expression at line 161:

```python
non_claims=list(receipt_non_claims or NON_CLAIMS),
```

**For current callers:**
- Local CLI runner (`run_source_capture_packet.py`): does not pass `receipt_non_claims` → `None or NON_CLAIMS` = `NON_CLAIMS`. Behavior unchanged. ✓
- Direct HTTP runner: passes `receipt_non_claims=DIRECT_HTTP_NON_CLAIMS` (11-element list, always truthy) → `DIRECT_HTTP_NON_CLAIMS or NON_CLAIMS` = `DIRECT_HTTP_NON_CLAIMS`. Correct. ✓

**Latent trap (A-02):** If a future adapter wants no non-claims and passes `receipt_non_claims=[]`, the expression `[] or NON_CLAIMS` evaluates to `NON_CLAIMS` (empty list is falsy). The caller's intent to produce an empty non-claims list is silently overridden. The correct expression is `receipt_non_claims if receipt_non_claims is not None else NON_CLAIMS`. This is the same truthiness-vs-`is not None` class of issue that F-06 closed in `build_optional_fact`. Current callers are not affected. This is a latent advisory finding.

**"not direct HTTP fetch" exclusion check:**
`DIRECT_HTTP_NON_CLAIMS` does not include `"not direct HTTP fetch"` (which is in the writer's own `NON_CLAIMS`). Unit test asserts `"not direct HTTP fetch" not in manifest["receipt_metadata"]["non_claims"]`. This correctly confirms that the HTTP adapter is not falsely claiming it doesn't do HTTP. ✓

**Local packet non-claims integrity:** The local CLI path still uses the writer's `NON_CLAIMS` list (which includes `"not direct HTTP fetch"`, `"not source acquisition"`, etc.) and these are loop-tested in the existing packet core tests. No regression observed. ✓

**Verdict:** No regression for local-packet or direct-HTTP callers. One latent truthiness trap for future adapters passing an explicit empty non-claims list.

---

## Q6 — Packet-Core No-Network Boundary

**Finding: no-network boundary intact; scope separation between two contract tests is correct.**

The direct HTTP adapter contract test (`test_source_capture_direct_http_contract.py`) scans:
- `source_capture/adapters/__init__.py`
- `source_capture/adapters/direct_http.py`
- `runners/run_source_capture_http_packet.py`

It checks for nine forbidden import roots: `aiohttp`, `archivebox`, `bs4`, `httpx`, `playwright`, `praw`, `requests`, `scrapy`, `selenium`, `webbrowser`.

The existing packet core contract test (from prior review, F-03 closure confirmed) scans `source_capture/*.py`, `harness_utils.py`, and `runners/run_source_capture_packet.py`. It covers `writer.py`, `models.py`, `__init__.py`, and `harness_utils.py`.

The two tests guard complementary surfaces. The direct HTTP adapter test permits `urllib` (the adapter's authorized tool) while blocking browser/API/scraper frameworks. The packet core test verifies that the writer and model layer remain network-free. Neither test is redundant; neither gap is critical.

**No weakening observed:** The direct HTTP adapter was added to a new sub-module (`source_capture/adapters/`) that the prior contract scan did not cover. The new adapter contract test correctly guards the new surface without relaxing the old scan.

**Verdict:** Packet-core no-network boundary is not weakened. The two-test architecture correctly separates "adapter boundary" from "packet-core boundary" concerns.

---

## Q7 — Test Sufficiency and External-Network Freedom

**Finding: tests are external-network-free; coverage is solid on critical paths with five advisory gaps on edge paths.**

### Network isolation
All unit tests use `ThreadingHTTPServer(("127.0.0.1", 0), Handler)` — in-process, OS-assigned port, loopback only. Zero external network calls. The contract test is pure AST analysis. ✓

### Critical path coverage (confirmed)
| Scenario | Test |
|---|---|
| 200 OK with body, metadata fields, cookie exclusion | `test_fetch_direct_http_capture_returns_selected_metadata_for_success` |
| Non-2xx (404) with body → success + `access_failed` limitation | `test_fetch_direct_http_capture_allows_non_2xx_body` |
| Empty body (204) → `NO_BODY` failure | `test_fetch_direct_http_capture_fails_for_empty_body` |
| Size cap exceeded → `SIZE_CAP_EXCEEDED` failure | `test_fetch_direct_http_capture_fails_for_size_cap` |
| Redirect followed → warning note, final_url updated | `test_fetch_direct_http_capture_follows_redirects` |
| Full runner integration, manifest structure, non-claims | `test_http_runner_writes_packet_with_metadata_and_body_files` |
| Runner exit code 3, no packet on empty body | `test_http_runner_returns_3_and_writes_no_packet_for_empty_body` |
| Runner exit code 0, non-2xx limitation in manifest | `test_http_runner_returns_0_and_marks_non_2xx_limitation` |
| No browser/scraper/API imports (AST) | `test_direct_http_adapter_avoids_browser_api_and_scraper_imports` |

All critical paths are covered. ✓

### Advisory gaps (A-03 through A-05)

**A-03 — No timeout failure path test.** `_failure_kind_from_url_error` contains timeout detection: `"timed out" in reason_text or "timeout" in reason_text`. This branch is not tested. A simulated `URLError("timed out")` or `URLError("timeout")` could verify the `TIMEOUT` kind is returned. Currently untested.

**A-04 — No network error failure path test.** The `NETWORK_ERROR` return from `_failure_kind_from_url_error` (the else branch) is not directly exercised by any test. A `URLError("connection refused")` simulation would cover this. Currently untested.

**A-05 — `DIRECT_HTTP_NON_CLAIMS` not fully loop-tested.** `test_http_runner_writes_packet_with_metadata_and_body_files` checks that `"not direct HTTP fetch"` is absent but does not assert all 11 expected non-claims are present. The packet core tests loop all `NON_CLAIMS` entries (F-08 closure), but the direct HTTP runner's 11-entry list has no equivalent loop check. A future refactor dropping one entry would not be caught.

**Minor gap — size cap during-read path not isolated.** The `/too-large` route sends `Content-Length: 6` with `max_bytes=5`. The pre-read Content-Length check (`content_length > max_bytes`) fires before body read. The `_BodyTooLargeError` path inside `_read_with_cap` (triggered when Content-Length is absent but streaming body exceeds the cap) is not directly exercised by a test. Not a correctness risk given the cap arithmetic is correct, but the streaming path is a separate code branch.

**Minor gap — `INVALID_URL` enum member is dead code (A-01).** `DirectHttpCaptureFailureKind.INVALID_URL = "invalid_url"` is defined but never instantiated. Invalid URLs raise `ValueError`, not `DirectHttpCaptureFailure(INVALID_URL)`. The enum member exists, is exported, and has no test. It is not reachable. No correctness impact; it could mislead future callers expecting to match on this failure kind.

**Verdict:** Tests are solid for all critical paths and are external-network-free. Five advisory gaps in edge-path coverage are non-critical.

---

## Q8 — Dry-Run Evidence Quality

**Finding: dry-run confirms end-to-end adapter path; loopback-only limitation is expected and correctly scoped.**

The manifest shows:
- `source_locator.value`: `"http://127.0.0.1:64694/ok"` — in-process test server, not an external URL
- `access_posture.value`: `"direct_http succeeded with HTTP 200 OK"` ✓
- `preserved_files[0]`: `raw/01_http_response_body.bin`, 27 bytes, sha256 matches body file ✓
- `preserved_files[1]`: `raw/02_http_response_metadata.json`, sha256 `82b5769…` matches pin ✓
- All 11 `DIRECT_HTTP_NON_CLAIMS` present in `receipt_metadata.non_claims` ✓
- `"not direct HTTP fetch"` absent from non-claims ✓
- No `Set-Cookie` or auth header in preserved metadata ✓
- `obligation_contract_version`: `"core_spine_v0_data_capture_spine_obligation_contract_v0"` ✓
- `limitations: []`, `warnings: []` — correct for 200 OK with no redirect ✓

The `02_http_response_metadata.json` (pinned separately) shows all 12 authorized metadata fields and no others. ✓

**What the dry-run proves:** That the full adapter → staging-file creation → `finally` cleanup → packet writer → manifest/receipt path operates correctly end-to-end. Posture vocabulary, non-claims, file preservation, hash computation, and receipt rendering are all confirmed by an actual run.

**What the dry-run does not prove:** The adapter against a real external URL with real-world behavior (chunked encoding, server-set cookies, compression, unusual redirect chains). The dry-run uses a controlled local server, consistent with the no-live-network-during-development constraint. This is appropriate for the current stage.

**Path ambiguity (A-06):** The commission specifies dry-run packet paths under `_test_runs/` (project root), but the actual packet is under `orca-harness/_test_runs/`. The file content and hashes are correct; only the path prefix in the commission is ambiguous.

**Verdict:** Dry-run evidence proves the end-to-end adapter path against a controlled local server. Loopback-only scope is appropriate and expected. External-URL behavior remains undemonstrated and is out of scope for this stage.

---

## Q9 — Documentation Accuracy

**Finding: docs are substantively accurate about boundary and failure semantics; two advisory staleness issues.**

`orca-harness/docs/source_capture_packet.md` correctly states:
- "uses stdlib `urllib`" ✓
- Exit codes 0/2/3 semantics ✓
- Exact list of 12 preserved metadata fields ✓
- "`set-cookie`, request cookies, authorization material" not preserved ✓
- Non-2xx with body → packet with `access_failed` limitation ✓
- Failure modes (timeout, DNS/TLS, empty body, byte-cap breach) → exit code 3 ✓

`orca-harness/README.md` is consistent with the above. ✓

**Advisory — staging file location undocumented (A-06):** The doc states the runner "writes two deterministic packet inputs before packet writing" but does not specify they are placed in `output_directory.parent`. For `--output _test_runs/my_packet`, staging files temporarily exist at `_test_runs/http_response_body.bin` and `_test_runs/http_response_metadata.json`. The `finally:` block cleans them up. An operator doing a manual run would not expect temporary files to appear in the parent of their output directory. This is minor but could surprise operators.

**Advisory — `docs/product/source_capture_toolbox/README.md` "Overall Gaps" is substantially stale:** The section still lists "no Direct HTTP adapter," "no packet writer," "no schema/model," "no CLI runner," "no unit/contract tests," and "no implementation review of source capture code" as current gaps. All of these are now implemented. The README was written before implementation began; its gap list was accurate at time of authoring but is now a stale snapshot. It should be updated when the toolbox product doc is next touched.

**Verdict:** Harness-level documentation is accurate. Product toolbox README "Overall Gaps" is stale but does not affect runtime behavior or downstream decision-making.

---

## Q10 — Blocking Before Commit

**Finding: no blockers.**

The adversarial review found no correctness bugs, no boundary violations, no fake-success paths, no provenance-header leaks, and no regression against the packet-core no-network tests.

---

## Summary

### Recommendation

`CLEAR_WITH_ADVISORY_FINDINGS`

No blockers. No major findings. Seven advisory findings, all non-critical for the current commit. The adapter is correctly bounded inside the authorized first-tranche, all named failure modes produce visible non-success outcomes, non-2xx bodies are honestly labeled, provenance headers are safe by explicit allowlist, and the existing no-network boundary is not weakened.

---

### Blocking Findings

None.

---

### Major Findings

None.

---

### Advisory Findings

| ID | Location | Finding |
|---|---|---|
| A-01 | `direct_http.py:21` | `DirectHttpCaptureFailureKind.INVALID_URL` is defined but never instantiated — dead code. Invalid URLs raise `ValueError` (exit code 2), not `DirectHttpCaptureFailure(INVALID_URL)`. Future callers matching on this enum member would never match. |
| A-02 | `writer.py:161` | `receipt_non_claims or NON_CLAIMS` uses truthiness, not `is not None`. An empty-list argument `[]` silently falls back to the writer's default `NON_CLAIMS`. Current callers are unaffected (direct HTTP runner always passes 11 items; local CLI never passes this param). Latent trap for a future adapter that wants an empty non-claims list. Correct expression: `receipt_non_claims if receipt_non_claims is not None else NON_CLAIMS`. |
| A-03 | `direct_http.py:213–217` | `_failure_kind_from_url_error` TIMEOUT branch (string match on `"timed out"` / `"timeout"`) is not covered by any test. |
| A-04 | `direct_http.py:215–217` | `_failure_kind_from_url_error` NETWORK_ERROR branch (else) is not covered by any test. |
| A-05 | `test_source_capture_direct_http.py:192` | `DIRECT_HTTP_NON_CLAIMS` 11-entry list is not loop-tested. Only the absence of `"not direct HTTP fetch"` is asserted; a future refactor dropping one of the other 10 entries would not be caught. |
| A-06 | `run_source_capture_http_packet.py:109–110`; `docs/source_capture_packet.md` | Staging files (`http_response_body.bin`, `http_response_metadata.json`) are placed in `output_directory.parent`, not in `output_directory`. This implicit staging-file location is not documented. Operators running the CLI at a path like `_test_runs/my_packet` would see temporary files appear in `_test_runs/`. The `finally` block cleans them up; risk is cosmetic (surprising output) not correctness. |
| A-07 | `test_source_capture_direct_http.py:127,202` | `Set-Cookie` exclusion tests check lowercase-underscore `"set_cookie"` (unit) and `"Set-Cookie"` (integration). Both are correct for existing code since the metadata dict uses hardcoded snake_case keys. The architectural allowlist is the stronger guard; tests are secondary signals. Not a correctness gap, but future dynamic-header enumeration would need a different guard. |

### Advisory Carries from Prior Review (Still Active)

| ID | Origin | Finding |
|---|---|---|
| F-05 carry | Post-patch blast-radius recheck | `original_path` absolute path provenance is documented as convention, not git-level or overlay-enforced. No fixture admission rule prevents future dry-run packets from being committed without a decision. |
| Advisory-01 | Post-patch blast-radius recheck | `VisibleFactStatus` is not exported from `source_capture/__init__.py`. Factory functions (`known_fact`, `unknown_with_reason`, etc.) are exported and are the primary API. Future adapter authors needing direct `VisibleFactStatus` access must import from `source_capture.models`. |

---

## Answers to Review Questions (Compact)

1. **Authorized boundary?** Yes. Stdlib-only GET, explicit allowlist headers, no browser/API/archive/proxy behavior. ✓
2. **Fake-success blocked?** Yes. All six failure modes (invalid URL, network error, timeout, no body, size-cap pre-read, size-cap during-read) produce visible `DirectHttpCaptureFailure` or `ValueError`; no packet is written. ✓
3. **Non-2xx bodies honest?** Yes. `access_failed` limitation appears in `limitation_notes`, `access_posture`, and manifest `limitations`. ✓
4. **Provenance headers safe?** Yes. Explicit allowlist in `_capture_response`; no cookies/auth/session preserved. Request sends only `User-Agent` + `Accept`. ✓
5. **`writer.py` receipt override regression?** No regression for current callers. One latent truthiness trap for future adapters passing an empty non-claims list (A-02). ✓ for current scope.
6. **No-network testing still strong?** Yes. Two-test architecture correctly separates adapter boundary from packet-core boundary; prior F-03 guard (`harness_utils.py` in core scan) confirmed still closed. ✓
7. **Tests sufficient, external-network-free?** Tests are network-free and cover all critical paths. Five edge-path gaps (A-03, A-04, A-05, size-cap streaming path, staging collision path) are advisory. ✓ for critical paths.
8. **Dry-run proves adapter path?** Yes, for end-to-end local-server run. External-URL behavior undemonstrated; appropriate for this stage. ✓
9. **Docs accurate?** Yes for harness-level docs. Product toolbox README "Overall Gaps" is substantially stale (A-06 note; does not affect runtime). ✓ for operational docs.
10. **Blocking before commit?** No. ✓

---

## Next Action

Commit is unblocked. The seven advisory findings are decision input for the next cleanup pass; none require resolution before the adapter commit.

Suggested order for advisory cleanup when convenient:

1. **A-02** (highest latent risk): Fix `receipt_non_claims or NON_CLAIMS` → `receipt_non_claims if receipt_non_claims is not None else NON_CLAIMS` in `writer.py`. Testable with an existing-pattern approach.
2. **A-03 / A-04**: Add two lightweight unit tests for `_failure_kind_from_url_error` using simulated `URLError` objects.
3. **A-05**: Add a `DIRECT_HTTP_NON_CLAIMS` loop assertion in `test_http_runner_writes_packet_with_metadata_and_body_files`.
4. **A-01**: Either use `INVALID_URL` in `_validate_http_url` (return a failure instead of raising) or remove the dead enum member. Choose whichever fits the desired CLI contract better.
5. **A-06**: Add one sentence to `source_capture_packet.md` explaining that staging files are placed in `output_directory.parent` and cleaned by the `finally` block.
6. **A-07**: No action required; existing allowlist architecture is the correct guard.
7. **Toolbox README staleness**: Update the "Overall Gaps" section when the product toolbox doc is next touched for any other reason.

---

## Non-Claims

This review is not: validation, readiness, approval, acceptance, source-of-truth
promotion, mandatory remediation, patch authority, implementation scoping,
executor-ready handoff, buyer proof, formal review verdict, or a claim that the
adapter works correctly against external live URLs. Findings are decision input
only. No patches are authorized by this review.

---

## Review Metadata

```yaml
review_id: source_capture_direct_http_adapter_adversarial_code_review_v0
review_date: 2026-06-02
reviewed_by: Claude Sonnet 4.6 (adversarial advisory review)
review_lane: zero-config findings-only advisory review
skills_used: workflow-deep-thinking, workflow-code-review
hash_verification: all 11 pins matched
blocking_findings: 0
major_findings: 0
advisory_findings: 7
advisory_carries_from_prior: 2 (F-05, Advisory-01)
patch_queue: none authorized
recommendation: CLEAR_WITH_ADVISORY_FINDINGS
commit_blocked: false
```
