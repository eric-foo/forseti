# Source Capture Media / Asset Adapter — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Adversarial implementation review of the bounded Media / Asset Preservation
  adapter. Covers explicit-URL-only boundary, Direct HTTP reuse honesty,
  mixed success/failure semantics, failed-slice packet-model compatibility,
  all-failed exit behavior, non-2xx body preservation honesty, metadata and
  receipt safety, test sufficiency, dry-run evidence quality, and doc accuracy.
  Advisory and minor findings only; no patch queue, no validation claim, no
  readiness verdict.
authority_boundary: retrieval_only
review_lane: zero-config findings-only adversarial implementation review
output_mode: filesystem-output
commission: >
  adversarial code review of media_asset.py, run_source_capture_media_packet.py,
  adapters/__init__.py, unit/contract tests, dry-run evidence, and docs;
  using Direct HTTP adapter and prior reviews as supporting context
```

---

## Source-Read Ledger

All 11 SHA256 pins verified exact match before review.

| File | Pin SHA256 (first 8 / last 4 chars) | Status |
|---|---|---|
| `orca-harness/source_capture/adapters/__init__.py` | `DF7530C3…15B4` | ✓ pin match |
| `orca-harness/source_capture/adapters/media_asset.py` | `4DBD8C59…779D` | ✓ pin match |
| `orca-harness/runners/run_source_capture_media_packet.py` | `7569C76C…BC1` | ✓ pin match |
| `orca-harness/tests/unit/test_source_capture_media_asset.py` | `94A20B46…E0F3` | ✓ pin match |
| `orca-harness/tests/contract/test_source_capture_media_asset_contract.py` | `D347426C…01F` | ✓ pin match |
| `orca-harness/docs/source_capture_packet.md` | `B87AE1CC…65A3` | ✓ pin match |
| `orca-harness/README.md` | `324904FF…446` | ✓ pin match |
| `_test_runs/media_asset_manual_packet_92f4d.../manifest.json` | `D930C22F…E16` | ✓ pin match |
| `_test_runs/media_asset_manual_packet_92f4d.../receipt.md` | `34C2734E…606` | ✓ pin match |
| `_test_runs/.../raw/01_asset_01_body.bin` | `DB789374…677` | ✓ pin match |
| `_test_runs/.../raw/02_asset_01_metadata.json` | `85F98D38…A8` | ✓ pin match |

Additional sources loaded (outside pin set):

- `AGENTS.md` — project-level behavior contract
- `.agents/workflow-overlay/README.md` — Orca overlay entrypoint
- `.agents/workflow-overlay/source-loading.md` — source-loading rules
- `.agents/workflow-overlay/review-lanes.md` — review lane authority
- `.agents/workflow-overlay/prompt-orchestration.md` — prompt and output mode rules
- `.agents/workflow-overlay/safety-rules.md` — project safety rules
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` — first-tranche build authority
- `docs/product/source_capture_toolbox/README.md` — toolbox design authority
- `docs/review-outputs/source_capture_direct_http_adapter_adversarial_code_review_v0.md` — prior Direct HTTP review; carried advisories
- `docs/review-outputs/source_capture_packet_core_post_patch_blast_radius_recheck_v0.md` — prior blast-radius recheck; carried advisories
- `orca-harness/source_capture/models.py` — packet model and validator
- `orca-harness/source_capture/writer.py` — packet writer
- `orca-harness/source_capture/adapters/direct_http.py` — Direct HTTP adapter
- `orca-harness/runners/run_source_capture_http_packet.py` — HTTP runner (imports `build_optional_fact`)

---

## Preflight Status

```
SOURCE_CONTEXT_READY
review_lane: zero-config findings-only adversarial implementation review
source_loading_mode: advisory findings-only (pinned source authority)
output_mode: filesystem-output
required_output_path: docs/review-outputs/source_capture_media_asset_adapter_adversarial_code_review_v0.md
hash_verification: all 11 pins match; no HASH_MISMATCH
dirty_state: confirmed; unrelated docs and overlay dirt exists; ignored per commission allowance
carried_advisories: A-02 carry (writer.py receipt_non_claims truthiness trap — RESOLVED in current code), F-05 carry (original_path fixture admission), Advisory-01 carry (VisibleFactStatus not exported from package __init__)
```

---

## Review Frame

Using `workflow-deep-thinking`.

The adversarial question is not "does the media adapter succeed on the happy path." It is: **does every named failure mode produce a correctly visible non-success outcome at both the adapter level and the packet level, with no fake-success escape hatch, while the adapter stays strictly inside the authorized first-tranche boundary and does not weaken the existing no-network and no-discovery guards?**

The ten review questions compress to three pressure zones:

1. **Boundary integrity** (Q1, Q2, Q10): Is every import, protocol, and behavior strictly inside the authorized explicit-URL-only, Direct-HTTP-reuse scope? Does the contract test guard it?

2. **Failure honesty** (Q3, Q4, Q5, Q6): Does every failure mode produce the right kind of non-success signal — at the batch level, the slice level, and the packet level? Can a mixed-success run lie about its aggregate success? Is an all-failed run blocked from writing a packet?

3. **Evidence quality** (Q7, Q8, Q9): Are metadata and receipts free of leaked secrets? Do the tests cover the critical paths without live network? Does the dry-run prove the end-to-end adapter-to-packet path?

The decisive failure modes to probe adversarially:

- **Mixed-success fake-success path**: Could a 1-success-3-failure batch still emit a packet that looks like full success?
- **All-failed packet-write escape**: Is there any path through `run_source_capture_media_packet` where `batch.successes` is empty but `write_local_source_capture_packet` is still called?
- **Non-2xx body pretending success**: Does a 404-with-body asset end up in a success slice without an `access_failed` signal?
- **Failed-slice packet-model compatibility**: Does `SourceCapturePacket.validate_preserved_file_references` accept slices with empty `preserved_file_ids`?
- **Metadata secret leakage**: Does the metadata JSON stored in `raw/` carry `Set-Cookie`, auth tokens, or session headers?
- **Second HTTP stack creation**: Does the media adapter reinvent HTTP, or does it strictly call `fetch_direct_http_capture`?

---

## Q1 — Explicit-Asset-URL-Only; No Discovery Drift

**Finding: boundary clean; no discovery path visible.**

`media_asset.py` line 34: `fetch_media_assets(*, asset_urls: list[str], ...)` — receives a caller-supplied list of URLs, iterates, calls `fetch_direct_http_capture(url=asset_url, ...)` for each. Nothing in the loop inspects response bodies for linked assets, parses HTML, inspects CSS, or recurses.

`run_source_capture_media_packet.py` parser: `--asset-url` uses `action="append"` (explicit multi-value flag). Only URLs the operator explicitly passes are processed. No response body is parsed for additional URLs.

Contract test (`test_media_asset_adapter_avoids_discovery_browser_api_and_scraper_imports`):
- Scans both `media_asset.py` and `run_source_capture_media_packet.py` via AST
- Checks for 9 forbidden import roots (aiohttp, archivebox, bs4, httpx, playwright, praw, requests, scrapy, selenium, webbrowser)
- Checks for HTML parser / gallery discovery imports: `"html" in node.module or "parser" in node.module`
- `source_capture.adapters.direct_http` is explicitly allowed; all other HTTP-related patterns are blocked

No `bs4`, `lxml`, `html.parser`, `html5lib`, `re.findall`, or response-body inspection for asset discovery is present in either file.

**Hard-stop cross-check:**
- No entitlement bypass: ✓ (no credential or cookie injection; delegates entirely to Direct HTTP adapter)
- No browser automation: ✓ (no playwright, selenium, webbrowser)
- No scraper frameworks: ✓ (no scrapy, requests, httpx)
- No discovery/gallery parsing: ✓ (no HTML/CSS parser imports)
- No archive services: ✓ (not_attempted posture; no archivebox, no Wayback API call)

**Verdict: explicit-URL-only boundary holds with no visible drift to discovery, parsing, or gallery behavior.**

---

## Q2 — Direct HTTP Boundary Reuse; No Second HTTP Stack

**Finding: genuine reuse; no second HTTP stack created.**

`media_asset.py` imports:
```python
from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)
```

This is the only acquisition path in `media_asset.py`. The module imports nothing from `urllib`, `urllib.request`, `http.client`, `requests`, `httpx`, or any other HTTP library. `fetch_direct_http_capture` handles URL validation, scheme enforcement, header construction, body reading with size cap, redirect tracking, `Set-Cookie` exclusion, and failure classification. The media adapter inherits all of these without reimplementing them.

`run_source_capture_media_packet.py` imports `MediaAssetCaptureFailure` and `fetch_media_assets` from `source_capture.adapters`. No second HTTP call path is present in the runner.

The contract test's `ALLOWED_DIRECT_HTTP_IMPORTS = {"source_capture.adapters.direct_http"}` confirms that the one allowed import root for HTTP behavior is the existing adapter.

**Verdict: the media adapter genuinely reuses the Direct HTTP boundary; no second acquisition stack created.**

---

## Q3 — Mixed Success/Failure Semantics

**Finding: semantics are honest; no fake "all captured" success path identified.**

Trace through the mixed-success path (1 success, 1 failure):

1. `fetch_media_assets` returns `MediaAssetCaptureBatch(successes=[asset_01], failures=[asset_02])`.
2. `if not batch.successes:` — False; continues to packet build.
3. Success loop (lines 102–142): stages body and metadata for `asset_01`, creates slice `asset_01` with `preserved_file_ids=["file_01","file_02"]`.
4. Failure loop (lines 144–162): no staging files; creates slice `asset_02` with `preserved_file_ids=[]`, `access_posture = known_fact("media_asset access_failed: ...")`, `media_modality_posture = known_fact("media_asset asset 02 not preserved")`, and `limitations=["asset 02 ... no_body: ..."]`.
5. `packet_limitations` accumulates `"asset_02_not_preserved: ..."`.
6. `write_local_source_capture_packet` is called with:
   - `access_posture = known_fact("media_asset preserved 1 of 2 explicit asset URL(s)")` — not "all captured"
   - `media_modality_posture = known_fact("media_asset preserved 1 asset body/bodies; 1 asset(s) not preserved")`
   - `limitations = ["asset_02_not_preserved: ..."]`
   - `source_slices = [asset_01 slice, asset_02 slice]`

Packet-level posture and limitations correctly reflect the partial capture. The failure slice is visible with `preserved_file_ids=[]`, an explicit `access_failed` access posture, and a limitation note. There is no rollup path that collapses failures into a silent omission.

The `SourceCapturePacket` model's `validate_preserved_file_references` validator passes correctly for this pattern: failure slice's empty `preserved_file_ids` contributes nothing to `referenced_ids`; since all `preserved_files` entries (file_01, file_02) are referenced by the success slice, the uniqueness/completeness invariants are satisfied.

Dry-run manifest confirms:
- `access_posture.value`: `"media_asset preserved 1 of 2 explicit asset URL(s)"` ✓
- `limitations`: `["asset_02_not_preserved: ..."]` ✓
- `source_slices[1].preserved_file_ids`: `[]` ✓
- `source_slices[1].access_posture.value` starts with `"media_asset access_failed:"` ✓

**Verdict: mixed success/failure semantics are honest; no fake "all captured" success escape identified.**

---

## Q4 — Failed Asset Slices With Empty `preserved_file_ids`

**Finding: safe and compatible with the packet model.**

`SourceCapturePacket.validate_preserved_file_references` (models.py:116–134):

```python
referenced_ids: set[str] = set()
for source_slice in self.source_slices:
    unknown_ids = set(source_slice.preserved_file_ids) - preserved_ids
    if unknown_ids:
        raise ValueError(...)       # slice references nonexistent file
    referenced_ids.update(source_slice.preserved_file_ids)
unreferenced_ids = preserved_ids - referenced_ids
if unreferenced_ids:
    raise ValueError(...)           # preserved file not referenced by any slice
```

For a failure slice with `preserved_file_ids=[]`:
- `set([]) - preserved_ids` = empty set — no unknown IDs → no error. ✓
- `referenced_ids.update([])` → adds nothing. ✓

The validator's completeness check is `preserved_ids - referenced_ids`: if the success slices reference all entries in `preserved_files`, the unreferenced set is empty regardless of how many failure slices have empty lists. ✓

The model also has `preserved_files: Field(min_length=1)` and `source_slices: Field(min_length=1)`. Both are satisfied because:
- `preserved_files` is populated from `staged_paths` (success assets only), always ≥2 when `batch.successes` is non-empty.
- `source_slices` always contains at least the success slices (and possibly failure slices).

**Verdict: failed-slice empty `preserved_file_ids` is safe and compatible with the packet model validator. Failure slices are legible with explicit `access_failed` posture and limitation notes.**

---

## Q5 — All-Failed Exit Behavior

**Finding: correct; exit code 3, no normal packet, failure clearly visible.**

Control flow trace for all-failed batch:

```python
# media_asset.py fetch_media_assets:
# all asset URLs return DirectHttpCaptureFailure (e.g., empty body)
# → batch.successes = [], batch.failures = [...]

# run_source_capture_media_packet.py:73
if not batch.successes:
    failure_summary = "; ".join(_format_failure(f) for f in batch.failures)
    return 3, f"no media assets were preserved; {failure_summary}"

# main():
# exit_code=3, message=failure_summary
# → if exit_code == 0: False
# → parser.exit(status=3, message=...)  → sys.exit(3)
```

No packet directory is created, no staging files are written (the `try` block is never entered), no `write_local_source_capture_packet` is called.

Test `test_media_runner_fails_without_packet_when_all_assets_fail`:
- Two failing assets: `/empty` (204, no body) + `/too-large` (Content-Length 6, max_bytes 5)
- `result.returncode == 3` ✓
- `"no media assets were preserved" in result.stderr` ✓
- `not output_dir.exists()` ✓

The failure summary in the exit message names each failed asset's index, HTTP status, failure kind, and message — fully inspectable.

**Verdict: all-failed behavior is correct; exit nonzero, no normal packet, failure summary visible.**

---

## Q6 — Non-2xx-With-Body Preservation Visibility

**Finding: non-2xx bodies are honestly labeled as `access_failed` at both adapter and packet levels.**

When `fetch_direct_http_capture` receives a 4xx/5xx response with a non-empty body, it returns `DirectHttpCaptureSuccess` (body preserved) with `limitation_notes = ["access_failed: direct HTTP returned HTTP {status}...; response body preserved"]`.

The media adapter's success-loop handling:

`_access_posture_for_success` (runner:210–214):
```python
if 200 <= result.status < 300:
    return known_fact("media_asset direct_http succeeded with HTTP ...")
return known_fact("media_asset access_failed with HTTP ...; asset body preserved")
```

So for a 404-with-body result, the slice `access_posture` starts with `"media_asset access_failed"`. The slice `limitations` carries the HTTP adapter's `limitation_notes` (which contains `"access_failed: direct HTTP returned HTTP 404..."`). The packet-level `limitations` aggregates the same text through `packet_limitations.extend(success.http_result.limitation_notes)`.

Test `test_media_runner_preserves_non_2xx_body_with_access_failed_limitation`:
```python
assert manifest["source_slices"][0]["access_posture"]["value"].startswith(
    "media_asset access_failed with HTTP 404"
)
assert any("access_failed" in item for item in manifest["limitations"])
```
Both assertions pass. ✓

There is no path where a non-2xx-with-body result is recorded as a "succeeded" access posture. The `_access_posture_for_success` function applies the correct conditional regardless of whether the HTTP adapter flagged it in `limitation_notes`.

**Verdict: non-2xx body preservation is honestly labeled as `access_failed` at slice, access_posture, and packet limitations levels.**

---

## Q7 — Metadata and Receipt Safety

**Finding: safe; no cookies, auth, session, or secret headers preserved.**

The media adapter's `_asset_metadata` function (runner:218–223):
```python
{
    "asset_index": asset_index,
    "asset_url": asset_url,
    "direct_http_metadata": result.metadata,
}
```

`result.metadata` is the Direct HTTP adapter's metadata dict, which uses an explicit allowlist construction:
```python
metadata = {
    "requested_url": ..., "final_url": ..., "status": ..., "reason": ...,
    "content_type": ..., "content_length": ..., "date": ...,
    "last_modified": ..., "etag": ..., "capture_timestamp": ...,
    "timeout_seconds": ..., "byte_count": ...,
}
```

`Set-Cookie`, `WWW-Authenticate`, `Authorization`, `Cookie`, `Proxy-*`, `X-Auth-*`, and all other secret-bearing headers are structurally excluded because they are not named in this dict. The media adapter adds no additional headers — `asset_index` and `asset_url` are safe provenance fields.

The outbound request uses only `User-Agent` and `Accept: */*` (inherited from Direct HTTP adapter). No cookie injection, no auth material.

Test `test_media_runner_writes_single_asset_packet` (line 157):
```python
assert "Set-Cookie" not in metadata["direct_http_metadata"]
```
Confirms that `Set-Cookie` is absent in the preserved metadata JSON even though the test server sends it in the response header. ✓

**Verdict: metadata and receipt safety is architecturally guaranteed by the Direct HTTP adapter's explicit-allowlist construction; the media adapter adds no new header exposure.**

---

## Q8 — Test External-Network Freedom and Boundary Sufficiency

**Finding: tests are external-network-free; coverage is solid on all critical paths; four advisory gaps on edge paths.**

### Network isolation

All unit tests use `ThreadingHTTPServer(("127.0.0.1", 0), Handler)` — in-process, OS-assigned port, loopback only. Zero external network calls. The contract test is pure AST analysis. ✓

### Critical path coverage

| Scenario | Test |
|---|---|
| Mixed batch (1 success, 1 failure) at fetch level | `test_fetch_media_assets_collects_successes_and_failures` |
| Single-asset packet: manifest structure, non-claims loop, receipt, staging cleanup | `test_media_runner_writes_single_asset_packet` |
| Multi-asset packet: file numbering, slice IDs, preserved file count | `test_media_runner_writes_multi_asset_packet` |
| Mixed failure visibility: access_posture, empty preserved_file_ids, limitation text | `test_media_runner_keeps_mixed_failure_visible` |
| All-failed: exit 3, no packet directory, error message | `test_media_runner_fails_without_packet_when_all_assets_fail` |
| Non-2xx body: access_failed in slice + packet limitations | `test_media_runner_preserves_non_2xx_body_with_access_failed_limitation` |
| Boundary: no browser/API/scraper/discovery imports (AST) | `test_media_asset_adapter_avoids_discovery_browser_api_and_scraper_imports` |

All critical paths are covered. The non-claims loop in `test_media_runner_writes_single_asset_packet` asserts all 13 `MEDIA_ASSET_NON_CLAIMS` entries in both the manifest and receipt. ✓

### Advisory gaps

**Advisory-test-01**: No test for invalid asset URL (e.g., `"file:///etc/passwd"` or a relative path) passed via `--asset-url`. Invalid URLs cause `fetch_direct_http_capture` → `_validate_http_url` to raise `ValueError`, which propagates through `fetch_media_assets` (not caught there) to `main()` → exit 2. This is correct behavior (arg/config error), but it means a single invalid URL among a list of valid ones terminates the entire batch rather than recording that one asset as a per-asset failure. The behavior is consistent with the Direct HTTP adapter's design but could surprise operators.

**Advisory-test-02**: No test for the staging collision detection path (what happens when `asset_01_body.bin` already exists in the output parent before the run).

**Advisory-test-03**: `MEDIA_ASSET_NON_CLAIMS` loop assertion is in the single-asset test only. The multi-asset and mixed-success tests do not repeat it. Low risk since the non-claims source is the same constant in all paths.

**Advisory-test-04**: The contract test does not scan `source_capture/adapters/__init__.py`. The `__init__.py` is currently a pure re-export module (no network or discovery behavior), but a future change adding a forbidden import would not be caught by the contract test. The prior Direct HTTP review established a precedent for explicitly guarding `harness_utils.py` (F-03 fix); `__init__.py` is a similar surface.

---

## Q9 — Manual Dry-Run Evidence Quality

**Finding: dry-run proves end-to-end adapter-to-packet path; loopback-only limitation is appropriate.**

Manifest confirms (against pinned `manifest.json`):

| Field | Value | Expected |
|---|---|---|
| `access_posture.value` | `"media_asset preserved 1 of 2 explicit asset URL(s)"` | ✓ mixed-success posture |
| `media_modality_posture.value` | `"media_asset preserved 1 asset body/bodies; 1 asset(s) not preserved"` | ✓ honest partial count |
| `source_slices[0].slice_id` | `"asset_01"` | ✓ ordinal pattern |
| `source_slices[0].preserved_file_ids` | `["file_01","file_02"]` | ✓ correct file IDs |
| `source_slices[1].slice_id` | `"asset_02"` | ✓ failure slice present |
| `source_slices[1].preserved_file_ids` | `[]` | ✓ empty for failure |
| `source_slices[1].access_posture.value` | starts `"media_asset access_failed:"` | ✓ visible failure |
| `limitations[0]` | `"asset_02_not_preserved: asset 02 HTTP 204..."` | ✓ human-readable |
| `preserved_files` count | 2 entries (file_01 body, file_02 metadata) | ✓ success asset only |
| `preserved_files[0].sha256` | `db789374…` matches pinned body.bin | ✓ |
| `preserved_files[1].sha256` | `85f98d38…` matches pinned metadata.json | ✓ |
| `receipt_metadata.non_claims` | all 13 MEDIA_ASSET_NON_CLAIMS | ✓ |
| `obligation_contract_version` | `"core_spine_v0_data_capture_spine_obligation_contract_v0"` | ✓ |
| `archive_history_posture.reason` | `"media asset adapter does not query archive or history services"` | ✓ not_attempted |
| `staging_cleanup_confirmed` | Confirmed per commission evidence | ✓ |

Receipt confirms: all 13 non-claims present, failure limitation visible, mixed posture accurate.

The dry-run used loopback (127.0.0.1) assets. This is appropriate and consistent with the no-live-network-during-development constraint. External-URL behavior (chunked encoding, real image bodies, CDN-style redirects) remains undemonstrated; this is out of scope for the current stage.

**What the dry-run proves:** end-to-end path from `fetch_media_assets` → staging → `write_local_source_capture_packet` → manifest/receipt with correct mixed-success semantics, failure slice legibility, and staging cleanup.

**Verdict: dry-run evidence is sufficient for the current development stage.**

---

## Q10 — Documentation and Non-Claim Accuracy

**Finding: harness-level docs are accurate; product toolbox README "Overall Gaps" remains stale (now also missing the media adapter).**

`orca-harness/docs/source_capture_packet.md` Media / Asset Boundary section states:
- "preserves only operator-supplied explicit asset URLs" ✓
- "does not discover assets, parse galleries, parse HTML, inspect CSS, recurse through linked assets, run OCR, analyze images, query archives, or automate a browser" ✓
- "reuses the Direct HTTP helper for ordinary HTTP access" ✓
- "If at least one asset body is preserved... records failed or unavailable assets as visible per-slice limitations" ✓
- "If no asset body is preserved, it fails visibly and writes no normal packet" ✓
- "Non-2xx responses with bodies can be preserved, but the corresponding slice carries an `access_failed` limitation" ✓
- Staging files documented: "stages explicit asset files as `asset_01_body.bin`, `asset_01_metadata.json`... in the output directory's parent while building the packet, then removes those staging files after the packet writer copies preserved assets into `raw/`" ✓

`orca-harness/README.md` media runner section:
- "explicit-URL-only"; "reuses the Direct HTTP helper"; all non-claims stated correctly ✓
- "writes mixed-success packets when at least one asset is preserved"; "carries failed assets as visible limitations" ✓

`MEDIA_ASSET_NON_CLAIMS` list in the runner is substantively accurate:
- Includes "not asset discovery", "not gallery parsing", "not OCR or image analysis" — correct, adapter does none of these
- Does NOT include "not media preservation" — correct, this adapter IS doing media preservation
- Does NOT include "not direct HTTP fetch" — correct, adapter uses Direct HTTP under the hood (would be dishonest to disclaim)

**Stale doc note:** `docs/product/source_capture_toolbox/README.md` "Overall Gaps" still lists "no Media / Asset Preservation adapter" (and "no Direct HTTP adapter", "no packet writer", etc.) as current gaps. These are all now implemented. This was noted in the prior Direct HTTP review (A-06 advisory carry) and remains stale after the media adapter addition. Not a correctness issue; it can be updated when the toolbox product doc is next touched.

**Verdict: harness-level documentation is accurate and matches implementation behavior. Product toolbox README "Overall Gaps" is stale but does not affect runtime behavior.**

---

## Findings

### M-01 — Staging File Cleanup Gap on Partial Write Failure (Minor)

**Location:** `orca-harness/runners/run_source_capture_media_packet.py:109–115`

```python
body_path.write_bytes(success.http_result.body)       # line 109
metadata_path.write_text(                              # line 110–115
    json.dumps(...),
    encoding="utf-8",
    newline="\n",
)
staged_paths.extend([body_path, metadata_path])        # line 115 — AFTER both writes
```

If `body_path.write_bytes()` succeeds but `metadata_path.write_text()` raises (e.g., disk full, permissions), `body_path` has been written to the output parent but is NOT yet in `staged_paths`. The `finally` block (`for staging_path in staged_paths: staging_path.unlink()`) will not include it, leaving an orphaned file.

On the next run, the collision guard at line 105–107:
```python
if body_path.exists() or metadata_path.exists():
    raise ValueError("media asset staging files already exist in the output parent...")
```
catches the residual file and prevents silent corruption, but the operator must manually remove the orphaned file before rerunning.

By contrast, the Direct HTTP runner pre-declares both staging paths (`body_path`, `metadata_path`) in the `finally` cleanup before any writes occur, so partial write failures always trigger cleanup.

This is a real defect. In normal operation, `write_bytes()` and `write_text()` with standard Python JSON should not fail. The practical risk is low but the cleanup gap is a design inconsistency relative to the Direct HTTP adapter pattern.

**Impact:** Orphaned staging file in output parent after partial write failure; collision guard prevents corruption on next run; operator must manually clear before rerunning.

**Minimum closure condition:** The body staging path is added to `staged_paths` immediately after `body_path.write_bytes()` succeeds, not after both writes — OR both paths are pre-declared in the `finally` cleanup target before either write (matching the Direct HTTP runner pattern).

**Next authorized action:** Owner may accept as-is (collision guard is effective), note it for the next cleanup pass, or patch independently. This review does not authorize patching.

---

### Advisory Findings

**A-01** — `build_source_locator` uses truthiness rather than `is not None`

**Location:** `runners/run_source_capture_media_packet.py:341–346`

```python
def build_source_locator(*, source_locator: str | None, unknown_reason: str | None):
    if source_locator:           # truthiness, not `is not None`
        return known_fact(source_locator)
    if unknown_reason:           # truthiness, not `is not None`
        return unknown_with_reason(unknown_reason)
    return None
```

An empty-string `--source-locator ""` falls through both conditions and returns `None`, which triggers the fallback `known_fact("explicit media asset URL set")` at line 170. This is the same truthiness-vs-`is not None` issue that was identified as a pattern concern in the codebase (F-06 and A-02 in prior reviews), where the established fix uses `is not None`. Current callers passing meaningful strings or `None` are unaffected. The inconsistency with `build_optional_fact` (which correctly uses `is not None`) is worth noting.

**Minimum closure condition:** Either apply `is not None` consistently with `build_optional_fact`, or document that empty-string inputs are treated as absent.

**Next authorized action:** Advisory carry for next cleanup pass.

---

**A-02** — Staging `extend` after both writes (root-cause location for M-01)

**Location:** `runners/run_source_capture_media_packet.py:115`

Stated as a separate advisory to surface the root-cause location and safer pattern. The Direct HTTP runner pre-registers both staging paths in a `finally` cleanup target before any I/O. The media runner accumulates paths post-write. Moving the `extend` (or equivalently, appending each path immediately after its write) would close the M-01 gap. Alternatively, pre-registering all staging paths before the first write would match the Direct HTTP pattern exactly.

**Minimum closure condition:** Staging path tracking covers each written file from the moment of write, not after both writes complete.

**Next authorized action:** Informational; see M-01 minimum closure condition.

---

**A-03** — Contract test omits `source_capture/adapters/__init__.py`

**Location:** `tests/contract/test_source_capture_media_asset_contract.py:27–30`

```python
target_paths = [
    project_root / "source_capture" / "adapters" / "media_asset.py",
    project_root / "runners" / "run_source_capture_media_packet.py",
]
```

`source_capture/adapters/__init__.py` is not scanned. It is currently a pure re-export module (no network or discovery behavior), so there is no current risk. However, a future addition of a forbidden import to `__init__.py` would not be caught. The Direct HTTP review established precedent for guarding `harness_utils.py` explicitly (F-03 closure). Adding `__init__.py` to the scanned set would extend that pattern.

**Minimum closure condition:** `source_capture/adapters/__init__.py` is added to `target_paths` in the contract test.

**Next authorized action:** Advisory for next cleanup pass.

---

**A-04** — Shared timing object uses first-success asset's capture timestamp for failure slices

**Location:** `runners/run_source_capture_media_packet.py:91`

```python
timing = PacketTiming(
    ...
    capture_time=known_fact(str(batch.successes[0].http_result.metadata["capture_timestamp"])),
    ...
)
```

This `timing` object is shared by all slices — both success and failure. In a batch where early assets fail and a later asset succeeds (e.g., asset_01 fails, asset_02 succeeds), failure slices inherit `capture_time` from the successful asset's fetch timestamp, not from when the failure was attempted. The times are likely within seconds of each other in practice, but the provenance is technically inaccurate for failure slices.

The obligation contract's Ob8 (Decomposed Timing) requires carrying timing categories separately, which is done. This is a mild provenance imprecision, not a contract violation.

**Minimum closure condition:** Either document this as a known approximation, or per-asset `capture_time` recording requires storing failure timestamps in `DirectHttpCaptureFailure`.

**Next authorized action:** Advisory for owner awareness; no action required before commit.

---

**A-05** — Cross-import of `build_optional_fact` from HTTP runner module creates coupling

**Location:** `runners/run_source_capture_media_packet.py:24`

```python
from runners.run_source_capture_http_packet import build_optional_fact
```

The media runner depends on a function defined in the HTTP runner's module. If the HTTP runner is renamed, moved, or refactored, the media runner breaks. The function is small and standalone. A local definition or a shared `harness_utils`-style location would decouple them. Low practical risk given the stable codebase, but the coupling is worth noting.

**Minimum closure condition:** `build_optional_fact` is defined in a location that does not create a cross-runner dependency (e.g., a shared helper or local copy).

**Next authorized action:** Advisory for next cleanup pass.

---

**A-06** — Advisory test coverage gaps (invalid URL, staging collision, multi-test non-claims loop)

Three advisory test gaps, restated compactly:

1. No test for invalid asset URL (e.g., `"file:///etc/passwd"`). An invalid URL causes `ValueError` from `_validate_http_url`, which propagates through `fetch_media_assets` (not caught there) to `main()` → exit 2. This is correct (arg/config error), but it means a single invalid URL terminates the batch rather than recording a per-asset failure — a behavioral difference from network-level failures. Untested.

2. No test for staging collision detection (pre-existing `asset_01_body.bin` in output parent). The guard fires correctly and raises `ValueError` → exit 2, but this path is untested.

3. The `MEDIA_ASSET_NON_CLAIMS` full-loop assertion (`test_media_runner_writes_single_asset_packet:149–151`) covers the single-asset case only. The multi-asset and mixed-success tests do not repeat the loop. Low risk since the non-claims come from the same constant.

**Minimum closure condition:** (1) test verifying exit 2 for an invalid asset URL; (2) test verifying exit 2 for staging collision; (3) as-is (single-test loop coverage is adequate).

**Next authorized action:** Advisory for next cleanup pass.

---

**A-07** — Product toolbox README "Overall Gaps" stale (now missing media adapter)

**Location:** `docs/product/source_capture_toolbox/README.md` (Overall Gaps section)

The "Overall Gaps" section still lists "no Direct HTTP adapter", "no packet writer", "no schema/model", "no CLI runner", "no unit/contract tests", and "no implementation review of source capture code" as current gaps. All of these are now implemented. "No Media / Asset Preservation adapter" also remains listed. The gap list was accurate at time of authoring but is now a stale snapshot. Does not affect runtime behavior.

**This finding was previously identified (as advisory carry from the Direct HTTP review). It is restated here because the media adapter has now also been implemented without updating the gap list.**

**Minimum closure condition:** "Overall Gaps" section updated when the product toolbox doc is next touched for any other reason.

**Next authorized action:** Advisory carry; update when the product doc is next edited.

---

### Advisory Carries from Prior Reviews (Still Active)

| ID | Origin | Finding |
|---|---|---|
| F-05 carry | Post-patch blast-radius recheck | `original_path` absolute path provenance is documented, but no git-level or overlay-enforced fixture admission rule prevents dry-run packets from being committed without a decision. Manifest shows `original_path: "C:\\Users\\vmon7\\Desktop\\projects\\orca\\orca-harness\\_test_runs\\..."`. |
| Advisory-01 | Post-patch blast-radius recheck | `VisibleFactStatus` is not exported from `source_capture/__init__.py`. Factory functions (`known_fact`, `unknown_with_reason`, etc.) remain the primary public API and are exported. Future adapter authors needing direct `VisibleFactStatus` access must import from `source_capture.models`. |

---

### Carry Resolution: Prior A-02 (writer.py receipt_non_claims truthiness trap)

**Status: RESOLVED in current code.**

The prior Direct HTTP review (A-02) identified that `receipt_non_claims or NON_CLAIMS` in `writer.py` used truthiness rather than `is not None`. The current `writer.py` at line 161 reads:

```python
non_claims=list(receipt_non_claims if receipt_non_claims is not None else NON_CLAIMS),
```

This is the correct `is not None` form. The A-02 latent trap is closed. `MEDIA_ASSET_NON_CLAIMS` (13-entry list, always truthy) passes correctly. ✓

---

## Answers to Review Questions (Compact)

| # | Question | Verdict |
|---|---|---|
| Q1 | Explicit-asset-URL-only, no discovery drift? | ✓ Clean. No HTML parsing, no gallery recursion, no discovery imports. Contract test confirms AST-level. |
| Q2 | Genuine Direct HTTP reuse, no second stack? | ✓ Clean. Only HTTP call is `fetch_direct_http_capture`. No `urllib` or other HTTP in media_asset.py. |
| Q3 | Mixed success/failure semantics honest? | ✓ Packet posture, slice posture, limitations, and `preserved_file_ids` all correctly reflect partial capture. |
| Q4 | Failed-slice empty `preserved_file_ids` safe? | ✓ Validator handles empty lists correctly. No structural incompatibility. |
| Q5 | All-failed: exit 3, no packet? | ✓ `if not batch.successes: return 3, ...` fires before any staging or packet write. Test confirms. |
| Q6 | Non-2xx with body visible as `access_failed`? | ✓ Slice `access_posture`, slice `limitations`, and packet `limitations` all carry `access_failed` text. |
| Q7 | Metadata and receipts safe? | ✓ Explicit allowlist from Direct HTTP adapter. No cookies, auth, or session headers. Test confirms. |
| Q8 | Tests external-network-free, sufficient? | ✓ Loopback server only. All critical paths covered. Four advisory edge-path gaps (A-06). |
| Q9 | Dry-run proves adapter-to-packet path? | ✓ Mixed-success path, failure slice legibility, staging cleanup, and all non-claims confirmed by actual run. |
| Q10 | Docs and non-claims accurate? | ✓ for harness-level docs. Product toolbox "Overall Gaps" remains stale (A-07). |

---

## Summary

### Recommendation

`CLEAR_WITH_MINOR_AND_ADVISORY_FINDINGS`

No blocking or major findings. The adapter is safe to commit. One minor finding (M-01 staging cleanup gap) and seven advisory findings are decision input for a future cleanup pass; none require resolution before the adapter commit.

---

### Blocking Findings

None.

---

### Major Findings

None.

---

### Minor Findings

| ID | Location | Finding |
|---|---|---|
| M-01 | `runners/run_source_capture_media_packet.py:109–115` | Staging `extend` happens after both writes. If `body_path.write_bytes()` succeeds but `metadata_path.write_text()` fails, `body_path` is written but not tracked in `staged_paths`, leaving an orphaned file in the output parent. Collision guard prevents corruption on next run, but operator must manually clear. Pattern is safer in Direct HTTP runner (pre-declared cleanup targets). |

---

### Advisory Findings

| ID | Location | Finding |
|---|---|---|
| A-01 | `run_source_capture_media_packet.py:341–346` | `build_source_locator` uses truthiness (`if source_locator:`) not `is not None`. Empty-string input falls through to `None`. Inconsistency with the established `build_optional_fact` `is not None` pattern. |
| A-02 | `run_source_capture_media_packet.py:115` | Root-cause location for M-01: staging `extend` after both writes. Safer pattern: append immediately after each write, or pre-declare all targets. |
| A-03 | `tests/contract/test_source_capture_media_asset_contract.py:27–30` | Contract test omits `source_capture/adapters/__init__.py` from the AST scan. Currently a pure re-export module; future additions would not be caught. |
| A-04 | `run_source_capture_media_packet.py:91` | Shared timing object uses first-success asset's `capture_timestamp` for all slices including failures. Failure slices' `capture_time` is an approximation of when those failures were attempted. |
| A-05 | `run_source_capture_media_packet.py:24` | `build_optional_fact` is imported from the HTTP runner module, creating a cross-runner coupling. Could be decoupled by a local definition or shared helper location. |
| A-06 | `tests/unit/test_source_capture_media_asset.py` | Three advisory test gaps: (1) no invalid-asset-URL test (exit 2 behavior differs from network failures); (2) no staging-collision test; (3) MEDIA_ASSET_NON_CLAIMS loop not repeated in multi-asset or mixed-success tests. |
| A-07 | `docs/product/source_capture_toolbox/README.md` | "Overall Gaps" still lists media adapter (and other now-implemented components) as unbuilt. Stale snapshot; does not affect runtime. (Carry from prior review; still active after media adapter addition.) |

---

### Advisory Carries from Prior Reviews (Still Active)

| ID | Origin | Finding |
|---|---|---|
| F-05 carry | Blast-radius recheck | `original_path` absolute path in committed dry-run artifacts is documented as provenance convention, but no git-level or overlay-enforced fixture admission rule. |
| Advisory-01 | Blast-radius recheck | `VisibleFactStatus` not exported from `source_capture/__init__.py`. Factory functions are the primary public API. |

---

### Prior Advisory Resolved

| ID | Origin | Status |
|---|---|---|
| A-02 | Direct HTTP adversarial review | RESOLVED. `writer.py` now uses `is not None` form correctly. |

---

## Suggested Order for Advisory Cleanup When Convenient

1. **M-01 / A-02** (highest practical risk): Move staging path tracking so each file is appended to `staged_paths` immediately after its write, or pre-declare targets before the loop (Direct HTTP pattern). Testable with an existing `finally`-focused integration scenario.
2. **A-03**: Add `source_capture/adapters/__init__.py` to the contract test's `target_paths`.
3. **A-01**: Apply `is not None` in `build_source_locator` consistent with `build_optional_fact`.
4. **A-06-1**: Add a test that passes an invalid URL (e.g., `"file:///etc/passwd"`) as `--asset-url` and asserts exit 2.
5. **A-05**: Move `build_optional_fact` to a shared location (e.g., `harness_utils` or a shared runner helper) to remove cross-runner import dependency.
6. **A-04**: Either document the timing approximation explicitly in docs or accept as-is.
7. **A-07 / toolbox README staleness**: Update "Overall Gaps" when the product toolbox doc is next edited.

---

## Non-Claims

This review is not: validation, readiness, approval, acceptance, source-of-truth promotion, mandatory remediation, patch authority, implementation scoping, executor-ready handoff, buyer proof, formal review verdict, or a claim that the adapter works correctly against external live URLs. Findings are decision input only. No patches are authorized by this review.

---

## Review Metadata

```yaml
review_id: source_capture_media_asset_adapter_adversarial_code_review_v0
review_date: 2026-06-02
reviewed_by: Claude Sonnet 4.6 (adversarial advisory review)
review_lane: zero-config findings-only adversarial implementation review
skills_used: workflow-deep-thinking, workflow-code-review
hash_verification: all 11 pins matched
blocking_findings: 0
major_findings: 0
minor_findings: 1 (M-01)
advisory_findings: 7 (A-01 through A-07)
advisory_carries_from_prior: 2 (F-05, Advisory-01)
prior_advisory_resolved: 1 (A-02 writer.py truthiness trap)
patch_queue: none authorized
recommendation: CLEAR_WITH_MINOR_AND_ADVISORY_FINDINGS
commit_blocked: false
```
