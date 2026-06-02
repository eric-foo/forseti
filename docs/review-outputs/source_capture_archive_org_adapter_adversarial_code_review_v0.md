# Source Capture Archive.org Adapter — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Adversarial implementation review of the bounded Archive.org availability/body
  adapter. Covers archive-availability separation, no-snapshot-found behavior,
  availability-lookup-failure behavior, cutoff-bound snapshot selection, Direct HTTP
  reuse honesty, metadata-only and body-failed packet legibility, body-failed slice
  empty preserved_file_ids safety, non-2xx access_failed visibility, metadata and
  receipt safety, test sufficiency, dry-run evidence quality, and doc accuracy.
  Advisory and minor findings only; no patch queue, no validation claim, no
  readiness verdict.
authority_boundary: retrieval_only
review_lane: zero-config findings-only adversarial implementation review
output_mode: filesystem-output
commission: >
  adversarial code review of archive_org.py, run_source_capture_archive_packet.py,
  adapters/__init__.py, unit/contract tests, dry-run evidence, and docs;
  using Direct HTTP adapter, models.py, writer.py, cli_support.py, and prior
  media/direct-http/blast-radius reviews as supporting context
```

---

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Source Capture Archive.org adapter adversarial implementation review
  edit_permission: read-only review; filesystem-output report only
  target_scope:
    - orca-harness/source_capture/adapters/archive_org.py
    - orca-harness/runners/run_source_capture_archive_packet.py
    - archive adapter tests/docs/export surface
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md (read)
    - .agents/workflow-overlay/README.md (read)
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md (read)
    - docs/product/source_capture_toolbox/README.md (read)
```

---

## Source-Read Ledger

All 13 SHA256 pins verified exact match before review.

| File | Pin SHA256 (first 8 chars) | Status |
|---|---|---|
| `orca-harness/source_capture/adapters/__init__.py` | `4B8E5C2A…` | ✓ pin match |
| `orca-harness/source_capture/adapters/archive_org.py` | `F27F3F4D…` | ✓ pin match |
| `orca-harness/runners/run_source_capture_archive_packet.py` | `71AAD887…` | ✓ pin match |
| `orca-harness/tests/unit/test_source_capture_archive_org.py` | `9F23F6FE…` | ✓ pin match |
| `orca-harness/tests/contract/test_source_capture_archive_org_contract.py` | `0ABCB151…` | ✓ pin match |
| `orca-harness/docs/source_capture_packet.md` | `85BEA260…` | ✓ pin match |
| `orca-harness/README.md` | `BEE45261…` | ✓ pin match |
| `docs/product/source_capture_toolbox/README.md` | `EFCA46BA…` | ✓ pin match |
| `_test_runs/archive_org_manual_packet_.../manifest.json` | `132BFC93…` | ✓ pin match |
| `_test_runs/archive_org_manual_packet_.../receipt.md` | `BF7FD676…` | ✓ pin match |
| `_test_runs/.../raw/01_archive_availability_metadata.json` | `BC12B34C…` | ✓ pin match |
| `_test_runs/.../raw/02_archive_snapshot_body.bin` | `FB8A2E80…` | ✓ pin match |
| `_test_runs/.../raw/03_archive_snapshot_body_metadata.json` | `71914C57…` | ✓ pin match |

Additional sources loaded (outside pin set):

- `AGENTS.md` — project-level behavior contract
- `.agents/workflow-overlay/README.md` — Orca overlay entrypoint
- `.agents/workflow-overlay/source-loading.md` — source-loading rules
- `.agents/workflow-overlay/review-lanes.md` — review lane authority
- `.agents/workflow-overlay/prompt-orchestration.md` — prompt and output mode rules
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` — first-tranche build authority
- `docs/product/source_capture_toolbox/README.md` — toolbox design authority (dirty; advisory use)
- `docs/review-outputs/source_capture_media_asset_adapter_adversarial_code_review_v0.md` — prior media review; carried advisories and resolution state
- `docs/review-outputs/source_capture_direct_http_adapter_adversarial_code_review_v0.md` — prior direct HTTP review; partial read (authority and boundary findings)
- `docs/review-outputs/source_capture_packet_core_post_patch_blast_radius_recheck_v0.md` — prior blast-radius recheck; carried advisories
- `orca-harness/source_capture/models.py` — packet model and validator
- `orca-harness/source_capture/writer.py` — packet writer
- `orca-harness/source_capture/cli_support.py` — CLI support helper
- `orca-harness/source_capture/adapters/direct_http.py` — Direct HTTP adapter

---

## Preflight Status

```
SOURCE_CONTEXT_READY
review_lane: zero-config findings-only adversarial implementation review
source_loading_mode: advisory findings-only (pinned source authority; dirty controlling sources noted)
output_mode: filesystem-output
required_output_path: docs/review-outputs/source_capture_archive_org_adapter_adversarial_code_review_v0.md
hash_verification: all 13 pins match; no HASH_MISMATCH
dirty_state: confirmed; controlling overlay files and all implementation targets are modified/untracked; advisory use per commission allowance
carried_advisories_from_prior_reviews: F-05 (original_path fixture admission), Advisory-01 (VisibleFactStatus not exported), M-01/A-02 pattern class (staging cleanup gap); A-07 (toolbox README staleness) checked for resolution status below
```

---

## Review Frame

Using `workflow-deep-thinking`.

The adversarial question is not "does the adapter succeed on the happy path." It is: **do all eight distinct outcome paths each produce the correct visible non-success or partial-success signal with no fake-success escape hatch, while the adapter stays strictly inside the authorized first-tranche boundary and does not weaken existing no-network or no-discovery guards?**

Three pressure zones structure the review:

1. **Boundary integrity** (Q1, Q5, Q10, Q12): Are all imports, protocols, and behaviors strictly inside the no-browser/no-SDK/no-scraper boundary? Does the contract test guard it adequately?

2. **Failure honesty** (Q2, Q3, Q4, Q6, Q7, Q8): Does every failure mode at every layer produce a correctly visible non-success signal? Is there any escape hatch that collapses a partial or failed result into a normal packet?

3. **Evidence quality** (Q9, Q10, Q11): Do tests, dry-run evidence, and docs provide an adequate downstream inspection surface without leaking secrets?

Decisive failure modes inspected adversarially:

- **Availability-failure escape**: Can `DirectHttpCaptureFailure` for availability still trigger a packet write?
- **Parse-failure fake-success**: Does CDX JSON parse failure correctly record a limitation and avoid fake-success posture?
- **Post-cutoff all-filtered silent selection**: Can `select_snapshot` silently accept a post-cutoff snapshot?
- **Body-failed slice model incompatibility**: Does `validate_preserved_file_references` accept a body slice with `preserved_file_ids=[]`?
- **Non-2xx body without access_failed**: Any path where non-2xx body lands in the packet without visible `access_failed`?
- **Staging cleanup partial-write gap**: Is `body_metadata_path` tracked for cleanup before or only after its write?
- **Second HTTP stack**: Does `archive_org.py` bypass `fetch_direct_http_capture` for any network call?
- **Secret leakage**: Does availability or body metadata expose cookies, auth, or session headers?

---

## Q1 — Archive Availability / Snapshot Body Separation

**Finding: clean separation at adapter level, packet level, and slice level.**

**Adapter level** (`archive_org.py:53–111`):

`ArchiveOrgCaptureSuccess` carries `availability_result` (always a `DirectHttpCaptureSuccess` when present) and `body_result` (a `DirectHttpCaptureSuccess`, `DirectHttpCaptureFailure`, or `None`) as distinct fields. The two HTTP fetches are sequential, not merged:

```python
availability_result = fetch_direct_http_capture(url=availability_url, ...)
# → on failure: return ArchiveOrgCaptureFailure immediately

selected_snapshot = select_snapshot(snapshots, cutoff_timestamp=cutoff_timestamp)
body_result = None
if selected_snapshot is not None:
    body_result = fetch_direct_http_capture(url=selected_snapshot.snapshot_url, ...)
```

There is no path where the body result overwrites or merges with the availability result.

**Packet level** (`run_source_capture_archive_packet.py:96–148`):

`file_01` is always the availability metadata JSON (written when availability lookup succeeds). `file_02` and `file_03` are body and body-metadata (written only when `isinstance(capture.body_result, DirectHttpCaptureSuccess)`). The `staged_paths` list accumulates file references separately for each.

**Slice level**: Two slices have semantically distinct IDs and `preserved_file_ids`:

- `archive_availability` slice: `preserved_file_ids=["file_01"]` always.
- `archive_snapshot_body` slice: `preserved_file_ids=["file_02", "file_03"]` on success; `preserved_file_ids=[]` on body-fail.

The `archive_snapshot_body` slice is added only when `capture.selected_snapshot is not None` (line 169). When no snapshot exists, there is only one slice.

**Verdict: Q1 answered YES. Availability metadata and snapshot body are correctly separated at all layers.**

---

## Q2 — No-Snapshot-Found: Safe Metadata Packet

**Finding: correct; metadata-only packet with visible posture; no fake body absence or fake success.**

Control flow when all snapshots are filtered out (either empty CDX response or all-post-cutoff):

1. `parse_availability_snapshots` returns `[]` (empty CDX) or `_parse_cdx_list_payload` returns `[]` (all rows skipped if timestamps invalid) or `select_snapshot([...], cutoff_timestamp=...)` returns `None` (all post-cutoff).
2. `body_result = None` (body fetch never attempted).
3. Runner: `archive_history_posture = known_fact("archive_org availability metadata preserved; no eligible snapshot selected")`.
4. Only `archive_availability` slice is added (the body slice guard `if capture.selected_snapshot is not None:` is False).
5. `input_files = [availability_path]` → `write_local_source_capture_packet` receives one file → `preserved_files = [PreservedFile(file_id="file_01", ...)]`.
6. Packet model validator: `preserved_ids = {"file_01"}`, `archive_availability` slice references it, `unreferenced_ids = set()` → no validation error.
7. `receipt_summary = "Archive.org packet with availability metadata preserved and no eligible snapshot body."`.

This is not a fake-success result. The packet's `access_posture`, `archive_history_posture`, and receipt all state that no snapshot was selected. The absence of a body slice is unambiguous — no `archive_snapshot_body` slice appears in the manifest.

Test `test_archive_runner_writes_no_snapshot_metadata_packet`:
```python
assert len(manifest["preserved_files"]) == 1
assert [item["slice_id"] for item in manifest["source_slices"]] == ["archive_availability"]
assert "no eligible snapshot" in manifest["archive_history_posture"]["value"]
```
✓

**Verdict: Q2 answered YES. No-snapshot produces a safe, legible, non-fake metadata packet.**

---

## Q3 — Availability Lookup Failure: No Normal Packet

**Finding: correct; exit code 3, no staging files, no packet directory.**

Control flow when `fetch_direct_http_capture` for availability returns `DirectHttpCaptureFailure` (e.g., empty body from HTTP 204, network error, timeout):

1. `isinstance(capture, ArchiveOrgCaptureFailure)` is True (line 86 of runner).
2. `return 3, capture.availability_result.message` — exits `run_source_capture_archive_packet` before the `try` block.
3. The `staging_parent.mkdir()` call (line 89) HAS already run, but no files are written.
4. `main()`: `exit_code == 3`, so `parser.exit(status=3, ...)` → `sys.exit(3)`.
5. No `write_local_source_capture_packet` is ever called.
6. No output directory is created.

Test `test_archive_runner_fails_without_packet_when_availability_lookup_fails`:
```python
assert result.returncode == 3
assert "empty body" in result.stderr
assert not output_dir.exists()
```
✓

**Adversarial check — staging parent creation**: `staging_parent.mkdir(parents=True, exist_ok=True)` runs before the early return. If the output parent directory is newly created here and the process dies, an empty directory may remain. This is the same behavior as other adapters. Not a material concern: the empty directory contains no files, and the output_directory itself is never created on this path.

**Verdict: Q3 answered YES. Availability lookup failure correctly writes no normal packet and exits with code 3.**

---

## Q4 — Cutoff-Bound Snapshot Selection: No Silent Post-Cutoff Selection

**Finding: correct; lexicographic string comparison is safe for 14-digit timestamps; post-cutoff snapshots are correctly excluded.**

`select_snapshot` implementation (`archive_org.py:149–161`):

```python
if cutoff_timestamp is not None:
    eligible = [snapshot for snapshot in snapshots if snapshot.timestamp <= cutoff_timestamp]
    if not eligible:
        return None
    return max(eligible, key=lambda snapshot: snapshot.timestamp)
```

**Safety of string comparison**: Both `snapshot.timestamp` and `cutoff_timestamp` are validated by `_validate_wayback_timestamp` to be exactly 14 ASCII digits (`timestamp.isdigit() and len(timestamp) == 14`). Lexicographic comparison of equal-length digit strings is equivalent to numeric comparison. `"20240601000001" <= "20240601000000"` is `False`, correctly excluding a snapshot one second after cutoff.

**Validation chain**:
- `cutoff_timestamp` is validated by `_validate_wayback_timestamp` in `fetch_archive_org_capture` (line 63–64) before it reaches `select_snapshot`.
- Each CDX row's timestamp is validated by `_validate_wayback_timestamp` in `_parse_cdx_list_payload` (line 185) before the snapshot is appended to the list. A malformed CDX timestamp raises `ValueError`, which propagates to the `(JSONDecodeError, ValueError)` catch block, setting `snapshots=[]` and `parse_warning`.

**Boundary case**: A timestamp exactly equal to `cutoff_timestamp` is selected (`<=`, not `<`). This is the documented at-or-before behavior. ✓

Test `test_fetch_archive_org_capture_selects_cutoff_snapshot`:
```python
result = fetch_archive_org_capture(
    original_url="https://example.com/multi",
    cutoff_timestamp="20240601000000",
    ...
)
assert result.selected_snapshot.timestamp == "20240101000000"  # older of 20250101 and 20240101
```
✓ The post-cutoff snapshot (20250101) is not selected; the at-or-before snapshot (20240101) is selected.

**Verdict: Q4 answered YES. Cutoff-bound selection is safe and correct. Post-cutoff snapshots are structurally excluded.**

---

## Q5 — Snapshot Body Retrieval: Genuine Direct HTTP Reuse

**Finding: genuine reuse; no second HTTP stack.**

`archive_org.py` imports:

```python
from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)
```

This is the **only** HTTP acquisition path in `archive_org.py`. The module does not import `urllib.request`, `http.client`, `requests`, `httpx`, `aiohttp`, `waybackpy`, `internetarchive`, or any other HTTP library. Both the availability fetch and the snapshot body fetch go through `fetch_direct_http_capture`.

The runner (`run_source_capture_archive_packet.py`) imports `fetch_archive_org_capture` and uses no separate HTTP path. The runner adds no additional HTTP call; it only assembles the packet from results returned by the adapter.

Inheritance from `fetch_direct_http_capture`:
- URL scheme enforcement (`http://` or `https://` only)
- Request construction (GET only, `User-Agent` + `Accept: */*`, no cookie/auth injection)
- Size cap enforcement (pre-read Content-Length check + streaming `_read_with_cap`)
- Empty-body detection
- `Set-Cookie` exclusion from preserved metadata
- `access_failed` limitation notes for non-2xx responses

None of these are reimplemented in `archive_org.py`.

Contract test (`test_archive_org_adapter_avoids_browser_api_scraper_proxy_and_archive_package_imports`):
- AST-scans `__init__.py`, `archive_org.py`, and `run_source_capture_archive_packet.py`
- Checks 11 forbidden import roots: `aiohttp`, `archivebox`, `bs4`, `httpx`, `internetarchive`, `playwright`, `praw`, `requests`, `scrapy`, `selenium`, `waybackpy`, `webbrowser`
- Checks discovery imports: `"html" in node.module or "parser" in node.module`
- Includes `__init__.py` in the scanned set (improvement over media adapter's A-03, where `__init__.py` was omitted)

**Verdict: Q5 answered YES. Snapshot body retrieval genuinely reuses Direct HTTP; no second HTTP stack created.**

---

## Q6 — Metadata-Only and Body-Failed Packet Legibility

**Finding: both packet types are legible for downstream inspection.**

### Metadata-only packet (no eligible snapshot)

Manifest fields:
- `archive_history_posture.value`: `"archive_org availability metadata preserved; no eligible snapshot selected"` — unambiguous.
- `source_slices`: exactly one entry with `slice_id = "archive_availability"`.
- `preserved_files`: one entry (`file_01` = availability metadata JSON).
- `access_posture.value`: `"archive_org availability metadata preserved; no eligible snapshot body requested"`.
- `receipt.md` summary: `"Archive.org packet with availability metadata preserved and no eligible snapshot body."`.

Downstream inspection: the single-file packet with `no eligible snapshot` posture is sufficient for an inspector to know that the archive was queried, the CDX lookup returned either an empty result or one where all snapshots were post-cutoff, and no body retrieval was attempted.

### Body-failed packet

Manifest fields:
- `archive_history_posture.value`: `"archive_org availability metadata preserved; snapshot body not preserved for {timestamp}"`.
- `source_slices`: two entries — `archive_availability` (with `file_01`) and `archive_snapshot_body` (with `preserved_file_ids=[]`).
- `limitations`: carries `"archive_snapshot_body_not_preserved: {message}"`.
- `archive_snapshot_body` slice: `access_posture.value` starts with `"archive_org snapshot body access_failed:"`.
- `archive_snapshot_body` slice: `timing.capture_time.status = "unknown_with_reason"` with reason `"archive snapshot body was not preserved and did not produce response capture timing"`.
- `preserved_files`: one entry only (`file_01`).

Test `test_archive_runner_writes_metadata_packet_when_body_fails` confirms all key fields:
```python
assert len(manifest["preserved_files"]) == 1
assert body_slice["slice_id"] == "archive_snapshot_body"
assert body_slice["preserved_file_ids"] == []
assert body_slice["timing"]["capture_time"]["status"] == "unknown_with_reason"
assert any("archive_snapshot_body_not_preserved" in item for item in manifest["limitations"])
```
✓

**Verdict: Q6 answered YES. Both packet types are legible. Failure state is visible at posture, slice, and limitations level.**

---

## Q7 — Body-Failed Slices With Empty `preserved_file_ids`: Safe and Understandable

**Finding: safe and compatible with packet model validator; legible.**

`SourceCapturePacket.validate_preserved_file_references` (`models.py:116–134`) trace for body-failed case:

```
preserved_files = [PreservedFile(file_id="file_01", ...)]  # availability only
source_slices = [
  archive_availability: preserved_file_ids=["file_01"],
  archive_snapshot_body: preserved_file_ids=[],
]

preserved_ids = {"file_01"}

Slice archive_availability:
  unknown_ids = {"file_01"} - {"file_01"} = ∅  → ok
  referenced_ids = {"file_01"}

Slice archive_snapshot_body:
  unknown_ids = ∅ - {"file_01"} = ∅  → ok
  referenced_ids = {"file_01"}  (unchanged)

unreferenced_ids = {"file_01"} - {"file_01"} = ∅  → ok
```

The empty `preserved_file_ids` list on the body slice contributes nothing to `referenced_ids` but causes no validation error. ✓

The body slice's explicit `access_posture`, `limitations`, and `timing.capture_time` make the empty list understandable: the slice exists to record what was attempted and why it failed, not to reference preserved files.

**Verdict: Q7 answered YES. Body-failed slices with empty `preserved_file_ids` are safe and understandable.**

---

## Q8 — Non-2xx Snapshot Body Preservation: `access_failed` Visible

**Finding: `access_failed` is visible at slice posture, packet limitations, and receipt; no path produces a 2xx-success-equivalent for a non-2xx body.**

When `fetch_direct_http_capture` returns `DirectHttpCaptureSuccess` with non-2xx status (e.g., 404-with-body), the runner's `_access_posture_for_success` function:

```python
def _access_posture_for_success(*, prefix: str, result: DirectHttpCaptureSuccess):
    if 200 <= result.status < 300:
        return known_fact(f"{prefix} direct_http succeeded with HTTP {result.status} ...")
    return known_fact(
        f"{prefix} access_failed with HTTP {result.status} ...; response body preserved"
    )
```

For a 404-with-body body result:
- Body slice `access_posture.value` starts with `"archive_org snapshot body access_failed"`.
- `capture.body_result.limitation_notes` carries `"access_failed: direct HTTP returned HTTP 404..."` (from `direct_http.py`).
- Runner: `packet_limitations.extend(capture.body_result.limitation_notes)` → packet-level `limitations` carries the `access_failed` text.
- `archive_history_posture` for the packet uses `_archive_posture(capture)` which calls `_access_posture_for_success` separately and produces `"archive_org availability metadata preserved; snapshot body preserved for {timestamp}"` — this says "preserved" (accurately; the body IS in the packet), while the `access_failed` signal is carried in `access_posture` and `limitations`.

There is no path where a non-2xx-with-body result receives a `"direct_http succeeded"` access posture. The conditional `200 <= result.status < 300` is the only gate, and it is evaluated before building the posture string.

Test `test_archive_runner_preserves_non_2xx_body_with_access_failed_limitation`:
```python
assert body_slice["access_posture"]["value"].startswith("archive_org snapshot body access_failed")
assert body_slice["preserved_file_ids"] == ["file_02", "file_03"]
assert any("access_failed" in item for item in manifest["limitations"])
```
✓

**Verdict: Q8 answered YES. Non-2xx body preservation carries `access_failed` at slice posture and packet limitations. No fake-success path identified.**

---

## Q9 — Metadata and Receipt Safety

**Finding: safe; no cookies, auth, sessions, or secret-bearing headers in preserved metadata or receipts.**

Both availability metadata (`_availability_metadata`) and body metadata (`_body_metadata`) use `result.metadata` directly from `DirectHttpCaptureSuccess`. This metadata dict is constructed with an explicit allowlist in `direct_http.py:154–167`:

```python
metadata = {
    "requested_url": ..., "final_url": ..., "status": ..., "reason": ...,
    "content_type": ..., "content_length": ..., "date": ...,
    "last_modified": ..., "etag": ..., "capture_timestamp": ...,
    "timeout_seconds": ..., "byte_count": ...,
}
```

`Set-Cookie`, `Cookie`, `Authorization`, `WWW-Authenticate`, `Proxy-*`, and all other secret-bearing headers are structurally excluded: they are not named in this dict, and no path in `archive_org.py` or the runner adds header values from the HTTP response.

The CDX request sends only `User-Agent` and `Accept: */*` (inherited from `fetch_direct_http_capture`). No cookie, session, or auth material is sent with the availability request. The Wayback snapshot body request sends the same headers.

**Dry-run confirmation**: `raw/01_archive_availability_metadata.json` (pinned, read) contains `availability_http_metadata` with only the allowlist fields. No cookie-related keys present. ✓

**Verdict: Q9 answered YES. Metadata safety is architecturally guaranteed by Direct HTTP's explicit-allowlist construction; the archive adapter adds no new header exposure.**

---

## Q10 — Tests: External-Network-Free and Sufficient

**Finding: all tests are external-network-free; coverage is solid on all critical paths; five advisory gaps on edge paths.**

### Network isolation

All unit tests use `ThreadingHTTPServer(("127.0.0.1", 0), Handler)` — in-process, OS-assigned port, loopback only. Zero external network calls. The contract test is pure AST analysis. ✓

### Critical path coverage

| Scenario | Test |
|---|---|
| Cutoff snapshot selection (post-cutoff excluded) | `test_fetch_archive_org_capture_selects_cutoff_snapshot` |
| No-snapshot metadata-only packet | `test_archive_runner_writes_no_snapshot_metadata_packet` |
| Metadata + body packet: file count, slices, body content | `test_archive_runner_writes_metadata_and_body_packet` |
| Body-fail: exit 0, one preserved file, body slice present with empty file IDs | `test_archive_runner_writes_metadata_packet_when_body_fails` |
| Availability-fail: exit 3, no packet directory | `test_archive_runner_fails_without_packet_when_availability_lookup_fails` |
| Availability-fail at adapter level | `test_fetch_archive_org_capture_returns_failure_for_availability_lookup_failure` |
| Non-2xx body: access_failed posture + file IDs preserved | `test_archive_runner_preserves_non_2xx_body_with_access_failed_limitation` |
| Non-claims full-loop | `_assert_receipt_non_claims` called from no-snapshot test |
| Boundary: no browser/API/scraper/discovery imports (AST, including `__init__.py`) | `test_archive_org_adapter_avoids_browser_api_scraper_proxy_and_archive_package_imports` |

All primary outcome paths are covered. Non-claims loop asserts all 14 `ARCHIVE_ORG_NON_CLAIMS` items in `receipt.md`. ✓

### Advisory test gaps

**Advisory-test-01** — Parse-failure path not tested at runner level.

When `parse_availability_snapshots` raises `JSONDecodeError` or `ValueError` (e.g., malformed CDX JSON), `snapshots=[]` and `parse_warning` is set. The runner correctly adds `parse_warning` as a limitation and produces a metadata-only packet. However, no runner integration test exercises this path. The behavior is correct by code inspection but untested end-to-end at the runner level.

**Advisory-test-02** — All-post-cutoff filtering (snapshots exist but cutoff excludes all) not tested at runner level.

The no-snapshot runner test uses an empty CDX response (header row only). There is no test for the case where CDX returns data rows but all have timestamps after the cutoff. `select_snapshot` correctly returns `None` in this case, and the runner would produce a metadata-only packet with `"no eligible snapshot selected"` posture. The adapter-level selection is tested (`test_fetch_archive_org_capture_selects_cutoff_snapshot` implicitly covers the `max(eligible, ...)` path), but the runner-level behavior for an all-post-cutoff CDX response is not.

**Advisory-test-03** — Availability dict-payload format not tested.

`_parse_availability_dict_payload` handles the `{archived_snapshots: {closest: ...}}` format. The CDX endpoint always returns list format when `output=json` is requested, so this code path is never reached in the normal adapter flow. The function exists as defensive support for a different Archive.org API surface. Its correctness is visible by inspection but unverified by tests.

**Advisory-test-04** — Staging collision test absent.

No test for the staging collision detection guards (pre-existing `archive_availability_metadata.json` or `archive_snapshot_body.bin` / `archive_snapshot_body_metadata.json` in the output parent). Guards fire correctly and raise `ValueError` → exit 3 (via the `except Exception` catch in `main()`), but this path is untested.

**Advisory-test-05** — Non-claims loop not asserted in all runner tests.

`_assert_receipt_non_claims` (called from `test_archive_runner_writes_no_snapshot_metadata_packet`) checks all 14 `ARCHIVE_ORG_NON_CLAIMS` items. The metadata+body, body-fail, and non-2xx body tests do not repeat this loop. Low risk since the non-claims come from the same constant, but coverage is incomplete.

---

## Q11 — Manual Dry-Run Evidence Quality

**Finding: dry-run proves end-to-end adapter-to-packet path including staging cleanup; loopback-only limitation is appropriate.**

Dry-run evidence inspection (all files pinned and read):

| Field | Value | Expected |
|---|---|---|
| `access_posture.value` | `"archive_org availability metadata and selected snapshot body preserved"` | ✓ success posture |
| `archive_history_posture.value` | `"archive_org availability metadata preserved; snapshot body preserved for 20240101000000"` | ✓ body-preserved posture |
| `source_slices[0].slice_id` | `"archive_availability"` | ✓ |
| `source_slices[0].preserved_file_ids` | `["file_01"]` | ✓ availability file only |
| `source_slices[1].slice_id` | `"archive_snapshot_body"` | ✓ |
| `source_slices[1].preserved_file_ids` | `["file_02","file_03"]` | ✓ body + metadata |
| `preserved_files` count | 3 entries (file_01, file_02, file_03) | ✓ |
| `preserved_files[0].sha256` | `bc12b34c…` | ✓ matches pinned `01_archive_availability_metadata.json` |
| `preserved_files[1].sha256` | `fb8a2e80…` | ✓ matches pinned `02_archive_snapshot_body.bin` |
| `preserved_files[2].sha256` | `71914c57…` | ✓ matches pinned `03_archive_snapshot_body_metadata.json` |
| `receipt_metadata.non_claims` | 14 items matching `ARCHIVE_ORG_NON_CLAIMS` | ✓ |
| `obligation_contract_version` | `"core_spine_v0_data_capture_spine_obligation_contract_v0"` | ✓ |
| `warnings` | `[]` | ✓ no warnings |
| `limitations` | `[]` | ✓ no limitations (clean 200 OK run) |
| `capture_mode` | `"archive/history"` | ✓ |
| `source_family` | `"archive_org"` | ✓ |
| `source_surface` | `"archive_org_wayback"` | ✓ |
| `staging_cleanup_confirmed` | stated in commission evidence | ✓ |

The availability metadata JSON (`01_archive_availability_metadata.json`, pinned) confirms:
- `availability_http_metadata` contains only allowlist fields (no cookies). ✓
- `selected_snapshot.timestamp = "20240101000000"` (pre-cutoff). ✓
- `parse_warning: null` (clean CDX parse). ✓

**What the dry-run proves:** end-to-end path from `fetch_archive_org_capture` → staging → `write_local_source_capture_packet` → manifest/receipt with correct metadata-plus-body posture, two-slice structure, and staging cleanup. The loopback server used for the dry-run is consistent with the no-live-network-during-development constraint.

**What the dry-run does not prove:** behavior against real Archive.org CDX endpoints (redirect handling, CDX response variability, pagination behavior if CDX returns paginated results, availability API format response). Out of scope for current development stage.

**Verdict: Q11 answered YES. Dry-run evidence is sufficient for the current stage.**

---

## Q12 — Documentation and Non-Claim Accuracy

**Finding: harness-level docs are accurate; product toolbox README "Overall Gaps" prior advisory (A-07) is resolved; `collapse=digest` behavior is undocumented (advisory).**

### Harness-level docs

`orca-harness/docs/source_capture_packet.md` Archive.org Boundary section:
- "queries a CDX/Wayback-style availability endpoint" ✓
- "preserves the raw availability metadata whenever that lookup returns a body" ✓
- "selects a snapshot at or before `--cutoff-timestamp`... or the latest available snapshot when no cutoff is supplied" ✓
- Four outcome states (metadata-only, metadata+body, body-fail, availability-fail) all correctly documented ✓
- "Snapshot body retrieval reuses the Direct HTTP helper" ✓
- "Non-2xx snapshot responses with a body can be preserved, but the packet carries an `access_failed` limitation" ✓
- Non-claims enumeration is accurate ✓

`orca-harness/README.md` Archive.org runner section:
- "distinguishes archive availability from archive-body preservation" ✓
- "writes no normal packet" for availability lookup failure ✓
- All non-claims stated correctly ✓

### `ARCHIVE_ORG_NON_CLAIMS` list accuracy

The 14-item list in `run_source_capture_archive_packet.py` is accurate:
- "not browser automation" ✓ (no playwright, selenium, webbrowser)
- "not API SDK use" ✓ (no waybackpy, internetarchive, praw)
- "not Archive.org package use" ✓ (explicit; no `internetarchive`, `archivebox`, `waybackpy`)
- "not HTML meaning extraction" ✓ (no HTML parsing of archived body)
- "not OCR or image analysis" ✓
- "not scraper framework use" ✓
- "not proxy or session injection" ✓ (no cookies/auth sent)
- "not archive completeness proof" ✓ (important: see A-03 advisory)
- All ECR/Cleaning/Judgment/buyer-proof/commercial non-claims ✓

### Toolbox README: prior A-07 advisory carry (RESOLVED)

The prior media adapter review's A-07 advisory noted that `docs/product/source_capture_toolbox/README.md` "Overall Gaps" still listed unimplemented adapters as current gaps. In the current version (pinned hash `EFCA46BA…`):

- "Implemented first-tranche pieces" now lists "Archive.org availability/body adapter" and "Media / Asset Preservation adapter". ✓
- "Remaining current gaps" accurately reflects only: Honest Browser Snapshot adapter, Source Observability integration point, fixture policy, rights/retention rule. ✓

**A-07 carry from media review is RESOLVED in the current toolbox README version.**

### Advisory: `collapse=digest` undocumented

`build_cdx_availability_url` always adds `collapse=digest` to the CDX query. This deduplicates snapshots by content digest: multiple captures with identical content are collapsed to one result. The `snapshot_count` in availability metadata reflects unique-content snapshots, not total capture count. Neither the harness docs, the toolbox README, nor the receipt mention this behavior. The "not archive completeness proof" non-claim covers the general case but not this specific mechanism. An operator reviewing `snapshot_count=1` might incorrectly infer that the page was archived only once.

---

## Findings

### M-01 — Staging Cleanup Gap: `body_metadata_path` Could Be Orphaned After Partial Write Failure (Minor)

**Location:** `orca-harness/runners/run_source_capture_archive_packet.py`, lines ~157–164

```python
body_path.write_bytes(capture.body_result.body)
staged_paths.append(body_path)            # ← tracked immediately after write ✓
body_metadata_path.write_text(            # ← if this raises...
    ...,
    encoding="utf-8",
    newline="\n",
)
staged_paths.append(body_metadata_path)   # ← ... this line never runs → orphan
```

If `body_metadata_path.write_text()` fails after `body_path.write_bytes()` succeeds (disk full, permissions), `body_path` IS tracked in `staged_paths` (correctly cleaned up), but `body_metadata_path` is not yet tracked. The `finally` block will not include `body_metadata_path`, leaving it orphaned in the output parent.

This is in the same pattern class as M-01 from the media adapter review (`run_source_capture_media_packet.py:109–115`), but less severe: in the media adapter, both body and metadata paths could be orphaned (neither was tracked until after both writes); here only `body_metadata_path` can be orphaned.

The `availability_path` tracking is safe: `staged_paths.append(availability_path)` runs immediately after `availability_path.write_text()` completes, so the availability path is always tracked.

The collision guard prevents corruption on re-run:

```python
if body_path.exists() or body_metadata_path.exists():
    raise ValueError(
        "archive snapshot body staging files already exist in the output parent; clear them before rerunning"
    )
```

On the next run, this guard fires for the orphaned `body_metadata_path`, exits with code 3, and the operator must manually remove the file before rerunning.

**Impact:** Orphaned `archive_snapshot_body_metadata.json` in output parent after partial write failure (disk full, permissions). Collision guard prevents corruption on next run. Operator must manually clear before rerunning. Normal operation is unaffected.

**Minimum closure condition:** `body_metadata_path` is appended to `staged_paths` immediately after `body_metadata_path.write_text()` completes — OR both body staging paths are pre-declared in the `finally` cleanup target before either write (matching the safest pattern, where cleanup precedes I/O).

**Next authorized action:** Owner may accept as-is (collision guard is effective, risk is low), note it for the next cleanup pass alongside the media adapter M-01 fix, or patch independently. This review does not authorize patching.

---

### Advisory Findings

**A-01** — Parse-failure path (malformed CDX JSON) not tested at runner level

**Location:** `runners/run_source_capture_archive_packet.py`, `archive_org.py:84–92`

When `parse_availability_snapshots` raises `JSONDecodeError` or `ValueError`, `parse_warning` is set and `snapshots=[]`. The runner adds the `parse_warning` as both a packet limitation and a slice limitation. The resulting packet is a metadata-only packet with one slice. This path is not covered by any runner integration test. The behavior is correct by code inspection but is not explicitly verified end-to-end.

**Minimum closure condition:** A runner test that simulates a malformed CDX JSON body (e.g., a CDX endpoint returning `invalid json`) and asserts that: (1) exit code is 0, (2) packet has one slice (`archive_availability`), (3) `limitations` contains a string matching `parse_failed`, and (4) `archive_snapshot_body` slice is absent.

**Next authorized action:** Advisory carry for next test cleanup pass.

---

**A-02** — All-post-cutoff filtering path not tested at runner level

**Location:** `runners/run_source_capture_archive_packet.py`, `archive_org.py:149–161`

When CDX returns data rows but all have timestamps after `cutoff_timestamp`, `select_snapshot` returns `None`. The runner produces a metadata-only packet with `"no eligible snapshot selected"` posture. The no-snapshot runner test uses an empty CDX response; there is no test for the case where snapshots exist but are all post-cutoff. Adapter-level selection is tested by `test_fetch_archive_org_capture_selects_cutoff_snapshot` (implicitly, by confirming the correct one of two candidates is selected), but the runner's response to the all-excluded case is not directly covered.

**Minimum closure condition:** A runner test using a CDX fixture that returns data rows but with timestamps all after the supplied `cutoff_timestamp`, asserting: (1) exit 0, (2) one slice (`archive_availability`), (3) `archive_history_posture.value` contains `"no eligible snapshot"`.

**Next authorized action:** Advisory carry for next test cleanup pass.

---

**A-03** — `collapse=digest` CDX deduplication not documented in user-facing docs

**Location:** `archive_org.py:119–128` (`build_cdx_availability_url`), `orca-harness/docs/source_capture_packet.md`, `orca-harness/README.md`

The CDX query always includes `collapse=digest`, which deduplicates snapshots with identical content. The `snapshot_count` in availability metadata reflects unique-content snapshots, not total capture count. Neither the harness docs nor the toolbox README mentions this behavior. An operator reviewing `snapshot_count` may incorrectly infer total archive coverage. The "not archive completeness proof" non-claim covers the general limitation but not the specific mechanism that `collapse=digest` is applied.

**Minimum closure condition:** User-facing docs mention that `collapse=digest` is applied to the CDX query, and that `snapshot_count` reflects unique-content snapshots rather than total captures.

**Next authorized action:** Advisory carry for next doc cleanup pass.

---

**A-04** — Availability dict-payload format (`_parse_availability_dict_payload`) not tested

**Location:** `archive_org.py:203–229`

`_parse_availability_dict_payload` handles the `{archived_snapshots: {closest: {...}}}` response format (the `/wayback/available` API, distinct from CDX). `build_cdx_availability_url` always generates a CDX-format URL (`/cdx/search/cdx?output=json`), so this dict path is never reached in the normal adapter flow when using the default endpoint. The function's correctness is visible by inspection (it validates the timestamp, passes `snapshot_url` verbatim which is then validated by `fetch_direct_http_capture`), but no test exercises this branch.

**Minimum closure condition:** Either a unit test directly calling `parse_availability_snapshots` with a dict-format payload, or documentation noting that `_parse_availability_dict_payload` is a defensive fallback for the availability API format and is not reached by the default CDX endpoint.

**Next authorized action:** Advisory carry for next test cleanup pass; or document as a known untested defensive path.

---

**A-05** — Availability slice `source_edit_or_version` is the selected snapshot timestamp (provenance imprecision)

**Location:** `runners/run_source_capture_archive_packet.py:118–120`, `_source_version_from_snapshot`

The shared `packet_timing` object uses `source_edit_or_version = known_fact("Archive.org snapshot timestamp {timestamp}")` when a snapshot is selected. This object is reused for both the `archive_availability` and `archive_snapshot_body` slices. For the body slice, this is accurate: the body IS the content from that snapshot timestamp. For the availability slice, it is a mild provenance imprecision: the CDX lookup result covers all snapshots in the CDX index, not just the selected snapshot's version.

An operator inspecting the availability slice's `source_edit_or_version` would see the selected snapshot timestamp, which may suggest the CDX response itself is "of" that timestamp rather than describing the full snapshot history. The correct posture might be `unknown_with_reason("CDX availability metadata covers all archived snapshots; no single version applies")`.

This does not affect correctness or downstream data integrity. It is a documentation artifact only.

**Minimum closure condition:** Either document this as a known provenance approximation, or use a separate `source_edit_or_version` for the availability slice that does not reference a specific snapshot timestamp.

**Next authorized action:** Advisory for owner awareness. No action required before commit.

---

**A-06** — Non-claims loop not repeated in all runner tests

**Location:** `tests/unit/test_source_capture_archive_org.py:294–297`

`_assert_receipt_non_claims` is called only from `test_archive_runner_writes_no_snapshot_metadata_packet`. The metadata+body, body-fail, and non-2xx body runner tests do not invoke this helper. Low risk since all runner paths use the same constant `ARCHIVE_ORG_NON_CLAIMS`; a change to the constant would be caught by the existing test. However, coverage is incomplete across runner outcome variants.

**Minimum closure condition:** Optional; calling `_assert_receipt_non_claims` in at least one additional runner test (e.g., the metadata+body test) would complete the non-claims coverage sweep.

**Next authorized action:** Advisory for next test cleanup pass; optional.

---

### Advisory Carries from Prior Reviews

| ID | Origin | Finding | Current Status |
|---|---|---|---|
| F-05 carry | Blast-radius recheck | `original_path` in dry-run packet manifests carries absolute machine-specific paths. No git-level or overlay-enforced fixture admission rule prevents dry-run packets from being committed without a separate decision. `manifest.json` confirms: `original_path: "C:\\Users\\vmon7\\Desktop\\projects\\orca\\orca-harness\\_test_runs\\..."`. | Still active |
| Advisory-01 | Blast-radius recheck | `VisibleFactStatus` is not exported from `source_capture/__init__.py`. Factory functions (`known_fact`, `unknown_with_reason`, etc.) remain the primary public API and are exported. Future adapter authors needing direct `VisibleFactStatus` access must import from `source_capture.models`. | Still active |

---

### Prior Advisory Resolved

| ID | Origin | Status |
|---|---|---|
| A-07 (toolbox README staleness) | Media adapter review | RESOLVED. Current `docs/product/source_capture_toolbox/README.md` (pinned `EFCA46BA…`) correctly lists both the Media adapter and Archive.org adapter as "Implemented" in the first-tranche pieces. "Remaining current gaps" no longer lists these adapters. |

---

## Answers to Review Questions (Compact)

| # | Question | Verdict |
|---|---|---|
| Q1 | Does the adapter correctly separate archive availability metadata from snapshot body preservation? | ✓ Clean. Two separate HTTP fetches, two separate files, two separate slices with distinct `preserved_file_ids`. |
| Q2 | Does no-snapshot-found produce a safe metadata packet rather than fake body absence or fake body success? | ✓ Clean. Metadata-only packet with `"no eligible snapshot selected"` posture. No `archive_snapshot_body` slice. No fake body files. |
| Q3 | Does availability lookup failure correctly write no normal packet? | ✓ Clean. Early return with code 3 before any file writes or packet creation. Test confirms. |
| Q4 | Does cutoff-bound snapshot selection avoid silently selecting post-cutoff snapshots? | ✓ Clean. Lexicographic `<=` comparison is safe for equal-length 14-digit validated timestamps. Post-cutoff strictly excluded. |
| Q5 | Does snapshot body retrieval genuinely reuse Direct HTTP rather than creating a second body-fetch stack? | ✓ Clean. Only HTTP call is `fetch_direct_http_capture`. No `urllib`, `requests`, or other HTTP in `archive_org.py`. Contract test confirms. |
| Q6 | Are metadata-only and body-failed packets legible enough for downstream Data Capture inspection? | ✓ Clean. Posture, slice IDs, `preserved_file_ids`, limitations, and receipt all make the state unambiguous. Test assertions confirm fields. |
| Q7 | Are body-failed slices with empty `preserved_file_ids` safe and understandable? | ✓ Clean. Validator accepts empty list safely. Slice `access_posture` and `limitations` make failure reason visible. |
| Q8 | Does non-2xx snapshot body preservation carry `access_failed` visibly? | ✓ Clean. `_access_posture_for_success` applies `access_failed` label for all non-2xx statuses. Packet limitations carry the same text. Test confirms. |
| Q9 | Are preserved metadata and body receipts safe from cookies, auth, sessions, or secret-bearing headers? | ✓ Clean. Direct HTTP explicit-allowlist construction structurally excludes all secret-bearing headers. CDX and body requests send only `User-Agent` + `Accept`. |
| Q10 | Are tests external-network-free and sufficient? | ✓ Loopback server only. All primary outcome paths covered. Five advisory edge-path gaps (A-01 through A-05 test variants). |
| Q11 | Does the manual dry-run prove the actual adapter-to-packet path, including staging cleanup? | ✓ End-to-end path from CDX fetch → staging → packet write confirmed. Three preserved files with pinned SHAs. All non-claims present. Staging cleanup confirmed. |
| Q12 | Are docs and non-claims accurate, especially around no archive completeness proof, no browser/API/scraper/proxy behavior, and no ECR/Cleaning/Judgment? | ✓ for harness-level docs and non-claims. `collapse=digest` behavior undocumented (A-03 advisory). Toolbox README gap (A-07) resolved. |

---

## Summary

### Recommendation

`CLEAR_WITH_MINOR_AND_ADVISORY_FINDINGS`

No blocking or major findings. The adapter is safe to commit. One minor finding (M-01 staging cleanup gap for `body_metadata_path`) and six advisory findings are decision input for a future cleanup pass; none require resolution before the adapter commit.

The adapter is cleaner than the media adapter in two important respects: (1) `body_path` IS tracked immediately after its write (the staging gap is limited to `body_metadata_path` only, not both body files), and (2) the contract test includes `__init__.py` in its scan targets, addressing the media adapter's A-03.

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
| M-01 | `runners/run_source_capture_archive_packet.py:157–164` | `body_metadata_path` is appended to `staged_paths` only after its write. If `body_metadata_path.write_text()` fails after `body_path.write_bytes()` succeeds, `body_metadata_path` is written but not tracked for `finally` cleanup. Collision guard prevents corruption on next run, but operator must manually clear. Less severe than media-adapter M-01 (only one path can be orphaned vs. both). |

---

### Advisory Findings

| ID | Location | Finding |
|---|---|---|
| A-01 | `runners/run_source_capture_archive_packet.py`, `archive_org.py:84–92` | Parse-failure path (malformed CDX JSON → `parse_warning` set, `snapshots=[]`, metadata-only packet) not covered by runner integration test. Correct by inspection; untested end-to-end. |
| A-02 | `runners/run_source_capture_archive_packet.py`, `archive_org.py:149–161` | All-post-cutoff filtering path (snapshots exist but cutoff excludes all → `selected_snapshot=None`, metadata-only packet) not tested at runner level. |
| A-03 | `archive_org.py:119–128`, `docs/source_capture_packet.md`, `README.md` | `collapse=digest` CDX deduplication not mentioned in user-facing docs. `snapshot_count` reflects unique-content snapshots, not total captures. "Not archive completeness proof" non-claim covers the general case but not this specific mechanism. |
| A-04 | `archive_org.py:203–229` | `_parse_availability_dict_payload` (availability API format) is a defensive fallback never reached by the default CDX endpoint. No test exercises this path. Correct by inspection. |
| A-05 | `runners/run_source_capture_archive_packet.py:118–120` | `archive_availability` slice inherits `source_edit_or_version = "Archive.org snapshot timestamp {timestamp}"` from shared packet timing. CDX lookup covers all snapshots; pinning the selected snapshot timestamp as the "version" of the availability metadata is a mild provenance imprecision. |
| A-06 | `tests/unit/test_source_capture_archive_org.py:294–297` | `_assert_receipt_non_claims` is called from only one runner test. Non-claims loop not repeated in metadata+body, body-fail, or non-2xx body tests. Low risk; same constant in all paths. |

---

### Advisory Carries from Prior Reviews (Still Active)

| ID | Origin | Finding |
|---|---|---|
| F-05 carry | Blast-radius recheck | `original_path` absolute path in committed dry-run packets is documented as provenance convention, but no git-level or overlay-enforced fixture admission rule. |
| Advisory-01 | Blast-radius recheck | `VisibleFactStatus` not exported from `source_capture/__init__.py`. Factory functions are the primary public API. |

---

### Prior Advisories Resolved

| ID | Origin | Status |
|---|---|---|
| A-07 (toolbox README staleness) | Media adapter review | RESOLVED. Toolbox README now lists Archive.org adapter (and all other implemented first-tranche components) as implemented; "Remaining current gaps" is accurate. |

---

## Suggested Order for Advisory Cleanup When Convenient

1. **M-01**: Track `body_metadata_path` in `staged_paths` immediately after its write (append on the line after `body_metadata_path.write_text()`). Coordinate with media adapter M-01 fix for consistency.
2. **A-01**: Add a runner test exercising the parse-failure path (malformed CDX JSON → `parse_warning` in limitations, one slice, exit 0).
3. **A-02**: Add a runner test for all-post-cutoff filtering (CDX has rows, all post-cutoff → metadata-only packet, `"no eligible snapshot"` posture).
4. **A-03**: Add one sentence to `source_capture_packet.md` Archive.org Boundary section noting that `collapse=digest` is applied.
5. **A-04**: Add a unit test for `parse_availability_snapshots` with a dict-format payload, or document `_parse_availability_dict_payload` as an untested defensive path.
6. **A-06**: Call `_assert_receipt_non_claims` in the metadata+body runner test.
7. **A-05**: Document the availability slice `source_edit_or_version` approximation, or carry as-is.

---

## Non-Claims

This review is not: validation, readiness, approval, acceptance, source-of-truth promotion, mandatory remediation, patch authority, implementation scoping, executor-ready handoff, buyer proof, formal review verdict, or a claim that the adapter works correctly against real Archive.org endpoints. Findings are decision input only. No patches are authorized by this review.

---

## Review Metadata

```yaml
review_id: source_capture_archive_org_adapter_adversarial_code_review_v0
review_date: 2026-06-02
reviewed_by: Claude Sonnet 4.6 (adversarial advisory review)
review_lane: zero-config findings-only adversarial implementation review
skills_used: workflow-deep-thinking, workflow-code-review
hash_verification: all 13 pins matched
blocking_findings: 0
major_findings: 0
minor_findings: 1 (M-01)
advisory_findings: 6 (A-01 through A-06)
advisory_carries_from_prior: 2 (F-05, Advisory-01)
prior_advisory_resolved: 1 (A-07 toolbox README staleness)
patch_queue: none authorized
recommendation: CLEAR_WITH_MINOR_AND_ADVISORY_FINDINGS
commit_blocked: false
```
