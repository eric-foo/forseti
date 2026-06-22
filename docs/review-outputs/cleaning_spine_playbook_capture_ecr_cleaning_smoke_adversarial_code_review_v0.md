# Cleaning Spine Playbook Capture → ECR → Cleaning Smoke: Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Read-only adversarial code/evidence review of the cleaning-spine-continuation
  branch smoke runner, related tests, ECR derivers, Cleaning models, and
  generated scratch evidence under
  orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/.
authority_boundary: retrieval_only
stale_if:
  - The branch is rebased, merged, or materially updated.
  - The smoke output directory is regenerated with different counts or findings.
  - The stitcher, Cleaning models, ECR derivers, Retail/PDP projection, or
    Reddit consolidation behavior changes.
```

## Review Summary

```yaml
review_summary:
  reviewed_by: claude-sonnet-4-6
  authored_by: gpt-5-codex
  de_correlation_bar: cross_vendor_discovery
  source_context: SOURCE_CONTEXT_READY
  source_context_qualifications:
    - "ulta/retail_pdp_projection.json: first 120 of 886KB lines loaded; structure
      confirmed from binding_map; smoke_summary confirms 9 handles, structure_preserved=true"
    - "4 capture-side doctrine sources not loaded (source_capture_playbook_v0,
      capture_recon_index_v0, source_capture_agent_runbook, retail_pdp_sidecar_operator_playbook);
      none listed in blocked_if_missing; review proceeds without them"
  verdict: findings_found
  validation_observed:
    - "not_run_with_reason: read-only review; the test-run output noted in the prompt
      (52 tests passing) is a prior-session observation and cannot be independently
      re-executed in this read-only pass; accepted as operator-stated pre-condition"
  strict_non_claims:
    - not validation
    - not readiness
    - not production e2e
    - not Judgment scoring
    - not playbook procedure verification (capture-side doctrine sources not loaded)
    - not independent test-run confirmation
```

---

## Source Loading Record

| Source | Status | Notes |
|--------|--------|-------|
| `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` | LOADED | Full file |
| `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` | LOADED | Full file |
| `orca-harness/cleaning/models.py` | LOADED | Full file |
| `orca-harness/cleaning/projection.py` | LOADED | Full file |
| `orca-harness/source_capture/retail_pdp_projection.py` | LOADED | Full file |
| `orca-harness/tests/unit/test_cleaning_core.py` | LOADED | Full file |
| `orca-harness/tests/unit/test_cleaning_projection_integration.py` | LOADED | Full file |
| `orca-harness/tests/unit/test_retail_pdp_projection.py` | LOADED | Full file |
| `capture_ecr_cleaning_smoke_manifest.json` | LOADED | Full file |
| `reddit_batch/batch_summary.json` | LOADED | Full file |
| `retail/sephora/retail_pdp_projection.json` | LOADED | Full file |
| `retail/ulta/retail_pdp_projection.json` | PARTIAL | First 120 lines; 886KB exceeds read limit |
| `retail/amazon/retail_pdp_projection.json` | LOADED | Full file (1 row) |
| `stitched_after_recaptcha_patch/smoke_summary.json` | LOADED | Full file |
| `stitched_after_recaptcha_patch/cleaning_packet.json` | LOADED | Full file (prior session) |
| `stitched_after_recaptcha_patch/ecr_source_side_receipts.json` | LOADED | Full file |
| `core_spine_v0_cleaning_spine_foundation_v0.md` | LOADED | Full file |
| `core_spine_v0_cleaning_spine_readme_v0.md` | LOADED | Full file |
| `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | LOADED | Full file |
| `core_spine_v0_projection_doctrine_v0.md` | LOADED | Full file |
| `source_capture_playbook_v0.md` | NOT LOADED | Not in blocked_if_missing; not in scope for this finding pass |
| `capture_recon_index_v0.md` | NOT LOADED | Not in blocked_if_missing |
| `source_capture_agent_runbook.md` | NOT LOADED | Not in blocked_if_missing |
| `retail_pdp_sidecar_operator_playbook_v0.md` | NOT LOADED | Not in blocked_if_missing |

---

## Deep-Thinking Failure Mode Frame

Using `workflow-deep-thinking`.

The core adversarial question: **can the stitcher create false success from bad capture substrate?**

Three distinct failure-mode families need framing before findings:

**FM-A — Structural false success (handle count masks content failure).** The runner creates CleaningInputHandles from all projection rows that exist, regardless of capture validity. For Amazon, 1 handle is produced from 1 product-context row, and the handle carries a valid sha256 anchor and ECR ref. The failure is correctly recorded in `smoke_summary.findings` but NOT on the handle itself. A downstream consumer of `cleaning_packet.json` in isolation cannot distinguish this handle from Sephora's 11 valid handles. This is the principal false-success vector the review must assess.

**FM-B — Semantic false success (smoke transform field picks metadata, not content).** `_retail_transform_candidates()` at line 682 iterates `row.source_visible_fields.items()` in dict key order. For `retail_pdp_product` rows, `_product_context_fields()` (retail_pdp_projection.py:906-919) builds source_visible_fields with both capture metadata (`capture_time`, `cutoff_posture`) and genuine source-locator facts (`retailer`, `source_family`, `source_locator`). When the projection JSON serializes with alphabetically ordered keys, `archive_history_posture` (None for live retail) precedes `capture_time` (non-null ISO timestamp) in iteration order. Result: the smoke transform picks capture_time = "2026-06-21T08:26:08Z" as the first source-visible string, not a product content field. The smoke proves the normalization pipeline runs but does so on a metadata timestamp — not product text. The non_claims list says `not_cleaning_semantic_transform`, which is an honest guard, but the underlying field placement (capture metadata in source_visible_fields) is a semantic boundary issue.

**FM-C — Raw-anchor integrity failure (tampered projection JSON passes hash checks).** The runner hash-verifies raw HTML files via `_verified_preserved_file()` (raises ValueError on sha256 mismatch) and verifies packet_id/slice_id/file_id inside projection rows via `_verify_retail_projection_anchors()`. But the projection JSON FILE ITSELF has no sha256 in the smoke manifest. A modified projection JSON — with rows removed, added, or failure indicators stripped — would pass all runner checks as long as the raw HTML sha256 matches. For the current single-operator local test scope this is theoretical, but the integrity chain is packet-anchored at the raw file level, not at the projection artifact level.

**FM-D — Heuristic boundary drift (captcha fix and remaining markers).** The captcha false-positive fix correctly removed captcha/recaptcha from `_RETAIL_ERROR_PAGE_MARKERS`. The remaining markers are: "page not found", "we couldn't find that page", "we can't load this page", "we can't load this page" (smart-quote), "robot check", "enter the characters you see below", "access denied". The marker "enter the characters you see below" is CAPTCHA challenge text and is correctly in the list for that purpose, but it could produce false positives on a legitimate PDP with instructional text matching this pattern. Low probability; documented as residual.

---

## Findings

### F-01 · MAJOR — Cleaning handles from failed retail captures are not distinguished at the handle level

- **File:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`; `orca-harness/cleaning/models.py`
- **Location:** `_process_retail_entry()`, `CleaningInputHandle` schema
- **Evidence:**
  - Amazon (packet_id `01KVMMN8T9F0Y2QPQS1F7RWKB8`) has `capture_validity_not_supported=True` and `structure_preserved=False`
  - smoke_summary.findings emits explicit `retail_capture_validity_not_supported` and `retail_structure_not_preserved` findings for Amazon
  - Amazon's handle count = 1 in smoke_summary.sources; 1 CleaningInputHandle is present in cleaning_packet.json with a valid `raw_anchor.sha256`, valid `ecr_ref`, and valid `projection_ref`
  - `CleaningInputHandle` schema (cleaning/models.py) has no `capture_validity` field or `findings` array
  - `CleaningEcrRef` and `CleaningProjectionRef` carry no capture-validity state; certification on `CleaningProjectionRef` = "view_only; not_cleaned; not_normalized; not_judgment_ready" (same for Amazon as for Sephora)
  - The ECR receipt for Amazon (`ecr:01KVMMN8T9F0Y2QPQS1F7RWKB8:source_side_postures`) shows `clears.identity=true` and `clears.inspectability=true` (same posture as valid captures)
- **Impact:** A downstream process that reads `cleaning_packet.json` without also reading `smoke_summary.json` findings cannot identify which handles derive from a failed capture. Amazon's 1 handle is structurally indistinguishable from Sephora's 11 valid handles within the packet. The failure signal lives in a separate artifact.
- **Boundary note:** The ECR source-side postures (identity, inspectability, timing, source_visibility) are scoped to provenance facts, not content validity. Amazon's HTML file IS hash-verifiable and identity-resolved — those postures are architecturally correct. The gap is at the CleaningInputHandle level, not the ECR receipt level.
- **Minimum closure condition:** One of: (a) add an optional `capture_validity_warnings: list[str]` field to `CleaningInputHandle` populated from the runner's `capture_validity_reasons`; or (b) add explicit documentation in the CleaningPacket schema that handles from failed captures are present and must be screened against companion `smoke_summary.findings`; or (c) owner accepts the separate-artifacts architecture and records the design decision. The current state leaves the coupling implicit.
- **Next authorized action:** Advisory only — owner routing on whether the handle level needs a propagated validity flag or documented read-together requirement.

---

### F-02 · MAJOR — Smoke transform picks `capture_time` (capture metadata) as the first source-visible string for pdp_product rows

- **File:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py:675-692`; `orca-harness/source_capture/retail_pdp_projection.py:901-919`
- **Location:** `_retail_transform_candidates()` line 682; `_product_context_fields()` lines 906-919
- **Evidence:**
  - `_product_context_fields()` returns a dict that includes capture metadata alongside source-locator facts:
    ```python
    {
        "retailer": retailer,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "source_locator": _fact_value(packet.source_locator),
        "slice_locator": _fact_value(source_slice.locator),
        "series_id": packet.series_id,
        "locale_pin": ...,
        "currency_pin": ...,
        "variant_pin": ...,
        "capture_time": _fact_value(source_slice.timing.capture_time),  # metadata
        "cutoff_posture": ...,
        "archive_history_posture": ...,
    }
    ```
  - When the projection JSON is serialized (Pydantic v2 / json.dumps), dict keys appear in alphabetical order. Alphabetically: `archive_history_posture` (None for live retail) → skip; `capture_time` (non-null ISO timestamp) → first non-null string → PICKED.
  - `_retail_transform_candidates()` at line 682 iterates `row.source_visible_fields.items()` and breaks on the first `isinstance(value, str) and value.strip()` match.
  - Observed in cleaning_packet.json transform ledger: `input_handle_id = "retail:sephora:01KVMMK0062R2A8GWY2V3GYZBW:cloakbrowser_snapshot_01:sephora:pdp"`, `original_value = "2026-06-21T08:26:08Z"`, `transformed_value = "2026-06-21T08:26:08Z"` (NFKC of a pure-ASCII ISO timestamp is identity).
- **Impact:** Two issues compounded:
  1. `capture_time` is capture harness metadata, not a value visible on the source page. Including it in `source_visible_fields` conflates capture provenance with source-visible content, violating the semantic contract of `source_visible_fields`.
  2. The smoke transform demonstrates the normalization pipeline runs, but exercises a timestamp that NFKC-normalizes identically (no transformation occurs). This provides zero evidence that the pipeline correctly handles source-page strings with unicode, whitespace, or normalization anomalies. The smoke's stated purpose — proving the pipeline runs — is met, but the field selection is misleading as an inspection artifact.
  - The `not_cleaning_semantic_transform` non_claim is honest about (2). There is no non_claim that covers (1).
- **Minimum closure condition:** (a) Move `capture_time`, `cutoff_posture`, and `archive_history_posture` out of `source_visible_fields` and into a separate `capture_context_fields` or `packet_metadata_fields` dict on the projection row, OR (b) have `_retail_transform_candidates()` explicitly skip known metadata fields by name; AND (c) add a non_claim or doc note about the metadata-in-source_visible_fields presence until the separation is done.
- **Next authorized action:** Advisory only — requires code changes in `retail_pdp_projection.py` and potentially `run_capture_ecr_cleaning_smoke.py`; no patch queue authorized by this review.

---

### F-03 · MINOR — `"enter the characters you see below"` remains in `_RETAIL_ERROR_PAGE_MARKERS` as a residual false-positive risk

- **File:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py:745-753`
- **Location:** `_RETAIL_ERROR_PAGE_MARKERS` tuple definition
- **Evidence:**
  ```python
  _RETAIL_ERROR_PAGE_MARKERS = (
      "page not found",
      "we couldn't find that page",
      "we can’t load this page",   # smart-quote variant
      "we can't load this page",
      "robot check",
      "enter the characters you see below",
      "access denied",
  )
  ```
  - The captcha fix correctly did NOT include "captcha" or "recaptcha" in this list (those terms were never present; the fix was removing them from a prior draft or preventing their addition).
  - "enter the characters you see below" is a human-CAPTCHA challenge phrase. It is correctly included for block-page detection.
  - However, this exact phrase could appear as legitimate product instructional text on a PDP (e.g., "Enter the characters you see below to submit your review"). The runner performs case-insensitive substring search on the full rendered DOM.
  - No test currently verifies a valid PDP that happens to include this phrase (only `test_retail_capture_validity_ignores_embedded_recaptcha_on_valid_pdp` covers the reCAPTCHA script false-positive case).
- **Impact:** Low probability false positive — a valid PDP with instructional text matching this pattern would be flagged as `capture_validity_not_supported`. The risk is residual, not a regression from the captcha fix.
- **Minimum closure condition:** Add a test case with a valid PDP HTML body that contains "Enter the characters you see below" as product/form instructional text (not a block-page marker), verifying `capture_validity_supported=True`; OR document explicit acceptance of the false-positive residual risk for this phrase.
- **Next authorized action:** Advisory only.

---

### F-04 · MINOR — `smoke_summary.json` uses absolute Windows paths in machine-specific fields

- **File:** `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/smoke_summary.json`
- **Location:** `output_paths`, `sources[*].packet_dir`, `sources[*].projection_json`, `sources[*].consolidation_json`
- **Evidence:**
  ```json
  "output_paths": {
    "cleaning_packet": "C:\\Users\\vmon7\\...\\cleaning_packet.json",
    ...
  },
  "sources": [
    {
      "packet_dir": "C:\\Users\\vmon7\\...\\retail\\sephora\\packet",
      ...
    }
  ]
  ```
  - All path fields are absolute Windows paths to the specific user's worktree.
- **Impact:** Moving or sharing the worktree invalidates all path references in the summary artifact. Any downstream process that consumes `smoke_summary.json` as a pointer to companion artifacts (packet_dir, projection_json, etc.) would fail. For the current local test scope, this is a portability limitation, not a correctness defect.
- **Minimum closure condition:** Use relative paths (relative to the smoke_summary.json or the manifest file) for the emitted path fields, OR add a doc note that path fields are machine-absolute and consumer must resolve against the local worktree root.
- **Next authorized action:** Advisory only.

---

### F-05 · MINOR — Amazon ECR receipt appears healthy in isolation without companion findings context

- **File:** `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/ecr_source_side_receipts.json`
- **Location:** Amazon receipt entry (`packet_id: "01KVMMN8T9F0Y2QPQS1F7RWKB8"`)
- **Evidence:**
  ```json
  {
    "packet_id": "01KVMMN8T9F0Y2QPQS1F7RWKB8",
    "source_label": "retail:amazon",
    "clears": {
      "identity": true,
      "inspectability": true,
      "source_visibility": false,
      "timing": false
    }
  }
  ```
  - Amazon's ECR receipt shows the same identity and inspectability posture as Sephora and Ulta (both clear).
  - This is architecturally correct: the block page HTML IS hash-verifiable and the packet_id IS resolved. ECR source-side postures are provenance facts, not content quality gates.
  - However, a reviewer reading `ecr_source_side_receipts.json` in isolation would see no indication that Amazon's capture yielded only a block page. The failure facts live in `smoke_summary.findings` only.
- **Impact:** No code defect. The separation between provenance postures (ECR receipt) and content validity (smoke_summary findings) is intentional. The interpretability gap is a documentation issue: two artifacts must be read together for the full picture, but neither explicitly says so.
- **Minimum closure condition:** Add a schema-level or artifact-level note that ECR source-side receipts are scoped to provenance postures only (not content validity or capture quality) and must be read alongside smoke_summary findings for the full picture. The current `non_claims` on the ECR receipts file does not include "not_capture_quality" or "not_content_validity" explicitly.
- **Next authorized action:** Advisory only; documentation note.

---

### F-06 · MINOR — No test explicitly verifies that a failed retail capture still produces an ECR receipt and Cleaning handle

- **File:** `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- **Location:** Test suite; no matching test found
- **Evidence:**
  - Existing tests cover: combined retail+reddit run, error page detection, reCAPTCHA false-positive fix, all-null rows, missing text pattern/selector anchor, cleaning transform smoke, transform smoke failure without source-visible string, old-Reddit anchor patterns, anchor downgrade to file-level, empty manifest, existing output refusal, projection slice/file mismatch, projection packet_id mismatch, hash mismatch, path escape.
  - None of these tests explicitly assert: "when retail entry has `capture_validity_not_supported`, the runner STILL emits one ECR receipt for that packet AND one CleaningInputHandle for its product-context row."
  - The combined run test (`test_retail_and_reddit_combined_run`) likely covers this implicitly, but the fixture HTML in that test may or may not trigger capture validity failure.
  - The `test_error_page_detection` family tests validity reasons but does not verify the downstream handle/receipt count.
- **Impact:** A future refactor that skips ECR receipt generation or handle creation for failed captures would not be caught by the existing test suite. The combined run provides weak implicit coverage but not assertion-level coverage for this specific behavior.
- **Minimum closure condition:** Add a test that sets up a retail entry whose HTML triggers `capture_validity_not_supported`, runs the stitcher, and asserts: (a) `smoke_summary.findings` contains `retail_capture_validity_not_supported`; (b) `ecr_source_side_receipts.json` contains exactly one receipt for that packet_id; (c) `cleaning_packet.handles` contains exactly one handle whose `raw_anchor.packet_id` matches.
- **Next authorized action:** Advisory only — test authorship is out of scope for this read-only review.

---

### F-07 · MINOR — Projection JSON and Reddit consolidation JSON files are not hash-verified; only the raw HTML files they reference are verified

- **File:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`; `capture_ecr_cleaning_smoke_manifest.json`
- **Location:** `_process_retail_entry()`, `_process_reddit_entry()`, manifest schema
- **Evidence:**
  - The manifest (`capture_ecr_cleaning_smoke_manifest.json`) has no `sha256` field for `projection_json` or `consolidation_json` paths.
  - The runner loads projection JSON at the manifest path without a hash check on the JSON file itself.
  - `_verify_retail_projection_anchors()` checks that the `packet_id`, `slice_id`, and `file_id` inside projection rows match the loaded packet — but these fields are INSIDE the JSON being loaded and could be consistent with a modified projection.
  - `_verified_preserved_file()` and `hash_file()` verify the raw HTML sha256 against the packet manifest and (for Reddit) the consolidation artifact — protecting the raw bytes.
  - For Reddit, consolidation JSON sha256 is not in the manifest; only the raw HTML sha256 (embedded inside the consolidation JSON) is hash-verified by the runner.
- **Impact:** Within the current scope (single-operator local test run, trusted workstation), the risk is theoretical. For any future use case involving shared manifests, multi-party hand-off, or CI-run artifact consumption, a modified projection or consolidation JSON with altered rows, stripped failure indicators, or injected fake anchors would pass runner integrity checks as long as the raw HTML sha256 matches. The integrity chain is strong at the raw file level but absent at the derived artifact level.
- **Minimum closure condition:** For production or shared-artifact use: add a `sha256` field for `projection_json` and `consolidation_json` in the manifest; have the runner verify these hashes before loading. For the current local test scope only: document the integrity chain limitation explicitly in the smoke runner's header or README.
- **Next authorized action:** Advisory only; out of scope for this local test run; flag for future production hardening.

---

## Review Question Answers

### Q1 — Does `run_capture_ecr_cleaning_smoke.py` refuse or visibly flag the right failures?

**Verdict: Substantially yes, with one architectural gap (F-01).**

The runner correctly:
- Raises `ValueError` → `exit(2)` on packet_id/slice_id/file_id mismatches (`_verify_retail_projection_anchors()`)
- Raises `ValueError` → `exit(2)` on raw file sha256 mismatch (`_verified_preserved_file()`)
- Raises `ValueError` → `exit(2)` on projection packet_id mismatch with loaded packet
- Raises `ValueError` → `exit(2)` on Reddit consolidation source_packet.packet_id mismatch
- Emits `retail_row_anchor_unverified` finding (not halt) when a projection anchor text or selector is absent in raw bytes — appropriate, since the hash confirms file integrity and only the anchor text location is uncertain
- Emits `reddit_row_anchor_downgrade_to_file` finding (not halt) when no old-Reddit pattern matches — appropriate downgrade behavior
- Emits `retail_capture_validity_not_supported` and `retail_structure_not_preserved` findings for Amazon — honest flagging

Gap (F-01): these findings live in `smoke_summary.findings` only. The produced `CleaningInputHandle` for the failed Amazon capture carries no validity warning. The runner correctly flags but doesn't propagate the flag to the downstream artifact.

### Q2 — Does the captcha heuristic patch correctly avoid treating reCAPTCHA on valid PDPs as block pages while still catching Amazon's failure?

**Verdict: Yes. The fix is correctly scoped. One residual noted (F-03).**

- `_RETAIL_ERROR_PAGE_MARKERS` contains no "captcha" or "recaptcha" strings. These were never in the list; the fix correctly excludes them going forward.
- `test_retail_capture_validity_ignores_embedded_recaptcha_on_valid_pdp` adds a reCAPTCHA `<script src>` and `<iframe src>` to a valid PDP HTML body and asserts `capture_validity_supported=True`. The test is correctly scoped to the false-positive scenario.
- Amazon's capture is caught by at least two independent markers: `rendered_dom_error_or_block_page_marker` (block-page text found) and `tiny_rendered_dom_with_error_marker` (the HTML body is under 5,000 bytes and has an error marker). The double-flag reduces false-negative risk.
- Residual (F-03): "enter the characters you see below" remains in the marker list. This is appropriate for CAPTCHA detection but could produce false positives on PDPs with matching instructional text.

### Q3 — Do Cleaning handles preserve `packet_id`, `slice_id`, `file_id`, `relative_packet_path`, `sha256`, `hash_basis`, projection refs for retail rows, and ECR ref packet-key coupling?

**Verdict: Yes. All required fields present and cross-key validated.**

- `CleaningRawAnchor` carries: `packet_id`, `slice_id`, `file_id`, `relative_packet_path`, `sha256`, `hash_basis`, `anchor_kind`, `anchor_value`. These come from the projection row's `raw_ref` and `raw_anchor` fields and are verified at anchor-validation time.
- `CleaningProjectionRef` is present on all retail handles and absent (null) on Reddit handles — correct, since Reddit has no projection artifact.
- `CleaningProjectionRef.validate_projection_is_not_cleaning_or_judgment` enforces `"not_cleaned"` AND `"not_judgment_ready"` both appear in the certification string. This is Pydantic-validated at construction.
- `CleaningEcrRef` is present on all 36 handles (confirmed in cleaning_packet.json). The ECR ref carries `packet_id` and `ref_id = f"ecr:{packet.packet_id}:source_side_postures"`.
- A Pydantic validator on `CleaningInputHandle` or `CleaningEcrRef` enforces that `ecr_ref.packet_id == raw_anchor.packet_id` (cross-key coupling). This prevents ECR refs from being attached to the wrong packet's handle.

### Q4 — Are ECR source-side receipts derived for every packet and correctly scoped as source-side postures, without becoming Judgment or sufficiency claims?

**Verdict: Yes, with an interpretability gap noted (F-05).**

- 6 ECR receipts for 6 packets — one per packet, no gaps.
- `ref_id = f"ecr:{packet_id}:source_side_postures"` — scoped label, not a sufficiency or Judgment claim.
- `posture_kind = "source_side_postures"` consistently.
- Non-claims on `ecr_source_side_receipts.json`: `not_capture_execution, not_crawler, not_production_acceptance, not_proof_run_readiness, not_judgment_scoring, not_cleaning_semantic_transform` — honest and sufficient.
- All 6 receipts have `timing.clears_pre_cutoff=false` with explicit residuals ("current live retail PDP capture; no historical cutoff asserted" / "direct HTTP runner did not receive cutoff posture metadata"). These are correctly named residuals, not invented values.
- All 6 receipts have `source_visibility.value="current_capture_only"` / `clears_source_visibility=false` — correct for current captures with no archive comparison.
- Gap (F-05): Amazon's receipt shows `identity=true, inspectability=true` — provenance-correct but reads as a "healthy" posture without the companion failure finding.

### Q5 — Does the stitched `CleaningPacket` remain a Cleaning working view, not raw evidence, ECR schema ratification, Judgment scoring, or production E2E proof?

**Verdict: Yes, with the F-02 semantic note.**

- `CleaningProjectionRef.validate_projection_is_not_cleaning_or_judgment` enforces `"not_cleaned"` AND `"not_judgment_ready"` in certification — Pydantic layer guard.
- `CleaningTransform.validate_method_or_rule` checks against `_JUDGMENT_TOKENS` frozenset — vocabulary guard at construction time.
- `CleaningPreservationCheck` requires all 6 booleans true — enforced per ledger entry.
- `REQUIRED_NON_CLAIMS = frozenset({"no_credibility_decision", "no_independence_effect", "no_signal_use_or_action_ceiling"})` — enforced on transform entries.
- The 1 transform ledger entry is for `unicode_nfkc_whitespace_collapse` on the Sephora pdp_product handle, with `rule_scope = SOURCE_INVARIANT_CORE`.
- Semantic note (F-02): the transform exercises a capture timestamp ("2026-06-21T08:26:08Z") that NFKC-normalizes identically, providing no evidence of normalization behavior on real source-page text. The smoke correctly non-claims `not_cleaning_semantic_transform`.

### Q6 — Does the run honestly report that Amazon did not yield usable PDP substrate?

**Verdict: Yes at the summary level. Not fully reinforced at the handle level (F-01).**

- `smoke_summary.sources[amazon]`: `capture_validity_supported=false`, `capture_validity_reasons=["rendered_dom_error_or_block_page_marker", "tiny_rendered_dom_with_error_marker"]`, `structure_preserved=false`, `handle_count=1`.
- `smoke_summary.findings`: `retail_capture_validity_not_supported` and `retail_structure_not_preserved` both emitted for Amazon's packet_id.
- The findings are explicit, named, and packet_id-linked — not smoothed into success.
- Limitation (F-01): `cleaning_packet.json` has no parallel honesty marker. The 1 Amazon handle inside the packet is indistinguishable from valid handles without reading `smoke_summary.findings`. This is not an omission in the summary; it is a gap in the packet artifact.

### Q7 — Are any tests missing that would allow this exact class of false-positive/false-success to regress?

**Verdict: One gap identified (F-06). Existing coverage is otherwise solid.**

Existing tests cover the critical regression paths:
- reCAPTCHA false-positive fix (direct test)
- Error page detection (dedicated test)
- Hash mismatch (ValueError + exit 2)
- packet_id / slice_id / file_id mismatch (ValueError + exit 2)
- Path escape (ValueError)
- All-null rows detection
- Reddit anchor patterns and anchor downgrade
- Empty manifest refusal
- Existing output refusal (idempotency guard)
- Transform smoke opt-in and no-source-visible-string failure

Gap (F-06): No test asserts that when a retail capture fails validity, the runner STILL emits an ECR receipt for that packet and a CleaningInputHandle for its extant rows. If a future refactor conditionally skips receipt/handle generation for invalid captures, the existing tests would not catch the regression.

Secondary gap: no test for what happens when ALL retail entries fail (no retail handles produced, only Reddit handles). The combined run test has Amazon failing but Sephora and Ulta succeeding. An all-fail retail scenario is untested.

### Q8 — Are any claims in this prompt or the run artifacts too strong relative to the loaded boundaries?

**Verdict: No overclaims found. Hedging is appropriate. One metadata semantic gap noted (F-02).**

- Prompt's "Known Real-Run Evidence To Verify" is explicitly labeled as hypotheses; this is correctly calibrated.
- `smoke_summary.json` non_claims: `not_capture_execution, not_crawler, not_production_acceptance, not_proof_run_readiness, not_judgment_scoring, not_cleaning_semantic_transform` — covers the major overclaim vectors.
- `ecr_source_side_receipts.json` carries identical non_claims.
- The test-run claim ("Focused tests passed") is scoped to 4 specific test files and labeled as a prior-session observation; not claimed as global validation.
- No claim of E2E production readiness, live capture execution, or Judgment scoring found in any reviewed artifact.
- Prompt's scope statement ("honest bounded real-data smoke") is accurately bounded.
- F-02 semantic note: `capture_time` in `source_visible_fields` makes a subtle overclaim that capture_time is source-visible content when it is capture harness metadata. This is not an overclaim in the reviewed artifacts' text, but in the code's field categorization.
- The cleaning spine foundation and boundary note are not overclaimed: the cleaning_packet.json correctly positions handles as non-destructive working material, not raw evidence or Judgment-ready output.

---

## Review-Use Boundary

Review findings are decision input only. They are not approval, validation, mandatory remediation, readiness, merge authority, fixture admission, production acceptance, or proof-run readiness until separately accepted and authorized.

This review:
- did not execute code
- did not modify any file
- did not verify test execution independently
- did not load 4 capture-side doctrine sources (source_capture_playbook_v0, capture_recon_index_v0, source_capture_agent_runbook, retail_pdp_sidecar_operator_playbook)
- did not read the full Ulta projection JSON (886KB partial read)
- is advisory only; findings require owner routing before any code or test changes

De-correlation bar: `cross_vendor_discovery` — code authored by GPT-5 Codex on branch `codex/cleaning-spine-continuation`; reviewed by Claude Sonnet 4.6.
