# Source Capture Packet Core — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Read-only adversarial implementation/code review of the Source Capture Packet
  core (models, writer, CLI runner), its unit and contract tests, and two local
  dry-run output packets. Advisory findings only; no patch queue, no validation
  claim, no readiness verdict.
review_question: >
  Is the Source Capture Packet core a stable enough common container for future
  Data Capture source-acquisition tools, before Orca builds Direct HTTP /
  browser / API / archive / media adapters?
authority_boundary: retrieval_only
```

---

## Source-Read Ledger

All 17 SHA256 pins verified exact match before review.

| File | SHA256 | Status |
|---|---|---|
| `orca-harness/source_capture/models.py` | `40224A7B…63FB76C` | ✓ pin match |
| `orca-harness/source_capture/writer.py` | `7C3E6F1D…E2FF8` | ✓ pin match |
| `orca-harness/runners/run_source_capture_packet.py` | `C4DF229D…343C59` | ✓ pin match |
| `orca-harness/tests/unit/test_source_capture_packet.py` | `524C6565…183F9` | ✓ pin match |
| `orca-harness/tests/contract/test_source_capture_packet_no_runtime_imports.py` | `462C4306…56CA` | ✓ pin match |
| `orca-harness/docs/source_capture_packet.md` | `0A9B75A9…6756F` | ✓ pin match |
| `orca-harness/README.md` | `58FA727B…0A49` | ✓ pin match |
| `orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run/manifest.json` | `B0C9D609…85BE8` | ✓ pin match |
| `orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run/receipt.md` | `AE8BFA54…7D64D` | ✓ pin match |
| `orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/manifest.json` | `32A64932…C1EC` | ✓ pin match |
| `orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/receipt.md` | `D1CA7CC0…C1476` | ✓ pin match |
| `docs/product/source_capture_toolbox/README.md` | `53DE41B2…CB1DF` | ✓ pin match |
| `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` | `FC4DB875…9E73D` | ✓ pin match |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `B06BD672…AC8C5` | ✓ pin match |
| `docs/product/data_capture_source_access_boundary_decision_v0.md` | `CBA3E118…9D532` | ✓ pin match |
| `docs/product/data_capture_source_access_method_plan_v0.md` | `119A37A4…6CB2` | ✓ pin match |
| `docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | `19982DDF…48E60` | ✓ pin match |

Additional source loaded for `StrictModel` verification (outside pin set):
- `orca-harness/schemas/case_models.py` — confirms `StrictModel = BaseModel(extra="forbid", populate_by_name=True)`.

---

## Preflight Status

```
SOURCE_CONTEXT_READY
review_lane: adversarial code review (advisory, no patch queue)
source_loading_mode: advisory findings-only (zero-config baseline + pinned source authority)
output_mode: filesystem-output
required_output_path: docs/review-outputs/source_capture_packet_core_adversarial_code_review_v0.md
hash_verification: all 17 pins match; no mismatch to report
dirty_state: confirmed; unrelated docs dirt ignored per commission
pycache: present at orca-harness/source_capture/__pycache__/; treated as hygiene note only
```

---

## Review Context Frame

Using `workflow-deep-thinking`.

The real question behind the commission is not "does the packet work for the
current local-file checkpoint" — that is evidenced by the two dry-runs. The
real question is: **will the packet model and writer hold their shape when
adapters (HTTP, archive, media, browser) arrive with different source-acquisition
behaviors, multiple locators, and per-slice divergence?**

Two sub-questions drive the failure-mode analysis:

1. **Container stability:** Does the model schema enforce enough structure to
   prevent vocabulary drift, boundary leakage, or incoherent payloads when
   future adapters produce packets?

2. **Writer API fit:** Does the current writer API expose enough of the packet
   model's structural capacity (multiple slices, per-slice timing/posture) to
   be usable by future adapters without replacement?

The following findings order these by impact on the container-stability question,
not by size of change required.

---

## Review Scope

**In scope:**
- `source_capture/models.py` — schema correctness, boundary compliance, vocabulary enforcement
- `source_capture/writer.py` — write behavior, file copy, defaults, non-claims
- `runners/run_source_capture_packet.py` — CLI flag correctness, conflict handling, failure mode visibility
- `tests/unit/test_source_capture_packet.py` — unit and integration test coverage
- `tests/contract/test_source_capture_packet_no_runtime_imports.py` — no-network contract boundary
- `orca-harness/docs/source_capture_packet.md` — documentation accuracy
- Dry-run outputs: both packets as review evidence for packet behavior
- Controlling sources: toolbox README, build authorization, obligation contract, boundary decision, method plan, Judgment toolkit specs

**Out of scope:**
- `schemas/case_models.py` — read for `StrictModel` definition only; not under review
- `harness_utils.py` — read-referenced; partially relevant as a boundary gap (see F-03)
- Unrelated dirty docs files
- Source Observability helper
- ECR, Cleaning, Judgment implementation

---

## Findings

### F-01 — MAJOR

**Criterion:** Metadata truthfulness; container stability  
**Location:** `orca-harness/source_capture/models.py:25–38` — `VisibleFact` model  
**Finding:** `VisibleFact.status` is declared as `str` with `min_length=1`, not as a constrained enum or `Literal` type. The `model_validator` only bifurcates on the literal string `"known"` vs. everything else. Any non-empty string is accepted as a valid status value, provided a `reason` is present.

**Evidence:**
```python
class VisibleFact(StrictModel):
    status: str = Field(min_length=1)   # free-form string
    value: str | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def validate_fact(self) -> "VisibleFact":
        if self.status == "known":
            if not self.value:
                raise ValueError("known facts require a value")
            return self
        if not self.reason:
            raise ValueError("non-known facts require a reason")
        return self
```

A caller can pass `VisibleFact(status="access_failed", reason="...")` or
`VisibleFact(status="partial", reason="...")` or any arbitrary string with a
reason, and the model accepts it without error.

**Authority basis:** The obligation contract (`core_spine_v0_data_capture_spine_obligation_contract_v0.md`) defines a formal discharge vocabulary: `met`, `partial`, `assessed_not_met`, `cannot_assess`, `access_failed`, `blocked`, `unavailable_by_source`, `not_applicable`, `not_attempted`. The packet's `VisibleFact` is not the obligation discharge state — it is a *fact availability* state. The toolbox README and the writer's factory functions imply four intended status values: `known`, `unknown_with_reason`, `not_attempted`, `not_applicable`. None of these are enforced at the schema layer.

**Impact:** At checkpoint 1, the writer exclusively uses the four factory functions (`known_fact`, `unknown_with_reason`, `not_attempted`, `not_applicable`) and the CLI is constructed exclusively from these factories. Vocabulary is correct in practice. However, when future adapters are built:
- An adapter could silently introduce non-standard status values (e.g., `"access_failed"`, `"unavailable"`, `"degraded"`) without a schema error.
- Downstream consumers (C1/C2 Judgment toolkit) that treat `VisibleFact.status` as an enumerated field would encounter values outside the implied vocabulary.
- The schema's tolerance would hide vocabulary drift across the adapter fleet.

**Minimum closure condition:** Either: (a) replace `status: str` with a `Literal` or `StrEnum` type enumerating the accepted packet-vocabulary values (`"known"`, `"unknown_with_reason"`, `"not_attempted"`, `"not_applicable"`), and verify existing callers pass; or (b) document the allowed status vocabulary explicitly in a comment or docstring on `VisibleFact`, and add a test that verifies a non-vocabulary status is either rejected or results in a known-good behavior. Option (a) is the stronger container guard.

**Next authorized action:** Design decision and, if accepted, bounded implementation change to `models.py` under the current first-tranche build authorization. Does not require new owner authorization.

---

### F-02 — MAJOR

**Criterion:** Multi-slice risk; container stability for future adapters  
**Location:** `orca-harness/source_capture/writer.py:109–152` — `write_local_source_capture_packet` — `source_slices` construction  
**Finding:** The writer hardcodes a single `SourceCaptureSlice` with `slice_id="slice_01"` and derives all slice metadata directly from packet-level parameters. There is no API path for passing per-slice metadata to the writer.

**Evidence:**
```python
packet = SourceCapturePacket(
    ...
    source_slices=[
        SourceCaptureSlice(
            slice_id="slice_01",          # hardcoded, no generation
            locator=source_locator,       # same as packet locator — no per-slice locator
            timing=timing,                # same timing as packet — no per-slice timing
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=packet_limitations,
            warning_notes=packet_warnings,
            preserved_file_ids=[item.file_id for item in preserved_files],
        )
    ],
    ...
)
```

All `preserved_files` are assigned to the single `slice_01`. If 5 files are passed,
they all go into one slice with the same locator, timing, access posture, and
archive posture.

**Authority basis:** The toolbox README (`docs/product/source_capture_toolbox/README.md`) states the cardinality rule explicitly:

> "a packet may cover one requested source or a bounded source set, but it must preserve per-source-slice state when archive posture, visibility, timing, locator, access, media, bundle, or re-capture relationship differs across slices. Capture-level rollups are allowed only when they do not hide slice-level divergence."

The Data Capture obligation contract (Ob10) requires per-slice archive posture when multiple states coexist. The model (`SourceCapturePacket.source_slices: list[SourceCaptureSlice] = Field(min_length=1)`) already supports multiple slices. The writer does not.

**Impact:** The packet *model* is multi-slice-capable. The *writer API* is not. When a Direct HTTP adapter or Archive.org adapter processes a URL that results in multiple locators (live URL + archive URL + fallback URL), each potentially with different timing, archive posture, or access failures, the current writer cannot represent per-locator divergence. An adapter would need to:
- Call a different, not-yet-existing writer function
- Post-process `PacketWriteResult.packet` and rewrite the manifest (unsupported)
- Build the slice list manually and bypass `write_local_source_capture_packet`

None of these paths exist yet. This means the first multi-locator adapter will hit this gap immediately.

The dry-run 2 limitation note acknowledges this: "slice-level divergence is represented only as one packet slice for this one-file dry-run." The question is whether the writer API needs to support multi-slice before adapters are built or whether it is acceptable to defer to the first adapter that needs it.

**Important distinction:** This is not a correctness defect at checkpoint 1. It is a design gap that creates adaptation cost at checkpoint 2+ (Direct HTTP adapter). The model can hold multi-slice payloads; the writer cannot produce them.

**Minimum closure condition:** Before the first multi-locator adapter begins implementation, document the slice API extension path: either (a) extend `write_local_source_capture_packet` with an optional `slices` parameter, (b) create a `write_source_capture_packet_from_slices` builder, or (c) publish a design note in `orca-harness/docs/` stating which writer API path will be used for multi-slice adapters. A code change is not required before accepting checkpoint 1, but the decision must be made before scoping the HTTP adapter.

**Next authorized action:** Design decision; does not require code change before checkpoint 1 acceptance. Requires design note or API extension before HTTP adapter scoping.

---

### F-03 — MINOR

**Criterion:** No-network boundary  
**Location:** `orca-harness/tests/contract/test_source_capture_packet_no_runtime_imports.py:24–32` — `target_paths` construction  
**Finding:** The no-network contract test scans `source_capture/*.py` and `runners/run_source_capture_packet.py`. It does not scan `harness_utils` (the module that provides `generate_ulid`, `hash_file`, `utc_now_z` to `writer.py`).

**Evidence:**
```python
target_paths = sorted((project_root / "source_capture").glob("*.py")) + [
    project_root / "runners" / "run_source_capture_packet.py"
]
```

`harness_utils` is outside this scan. `writer.py` imports `from harness_utils import generate_ulid, hash_file, utc_now_z` — these are clearly non-network utilities and the current `harness_utils` implementation is clean. However, if `harness_utils` were modified to add a network call (e.g., for version checking, telemetry, or an HTTP hash lookup), the contract test would not detect it.

**Authority basis:** The toolbox README states: "The packet core and first local-file CLI mode must perform no network access, browser automation, API calls, archive lookup, media fetch, scraper execution, or deferred-adapter behavior. Contract tests should guard this boundary."

**Impact:** The contract boundary guard is incomplete. A future change to `harness_utils` that introduces a network import would not be caught by the no-network test, creating a silent boundary violation. The risk is currently low because `harness_utils` exports only `generate_ulid`, `hash_file`, and `utc_now_z` — local deterministic utilities. The gap becomes more material if `harness_utils` grows to support shared adapter utilities that might include HTTP helpers.

**Minimum closure condition:** Add `harness_utils.py` (and any other non-schema, non-test module imported by `writer.py` or `run_source_capture_packet.py`) to the `target_paths` list in the contract test.

**Next authorized action:** Bounded implementation change to `tests/contract/test_source_capture_packet_no_runtime_imports.py` under current first-tranche build authorization.

---

### F-04 — MINOR

**Criterion:** Raw preservation and inspectability  
**Location:** `orca-harness/source_capture/models.py:57–67` — `SourceCaptureSlice.preserved_file_ids`; `models.py:84–107` — `SourceCapturePacket`  
**Finding:** There is no cross-validation between `SourceCaptureSlice.preserved_file_ids` and `SourceCapturePacket.preserved_files[*].file_id`. A packet could contain a slice referencing `file_id` values that do not exist in `preserved_files`, or `preserved_files` entries that are not referenced by any slice.

**Evidence:**
```python
class SourceCaptureSlice(StrictModel):
    ...
    preserved_file_ids: list[str] = Field(default_factory=list)

class SourceCapturePacket(StrictModel):
    ...
    source_slices: list[SourceCaptureSlice] = Field(min_length=1)
    preserved_files: list[PreservedFile] = Field(min_length=1)
    # No model_validator cross-checking these two
```

In the current writer, `preserved_file_ids` is always set to `[item.file_id for item in preserved_files]`, meaning the single slice always claims all files. In a multi-slice scenario, however, nothing would prevent a bug where a slice claims `file_03` but the packet only has `file_01` and `file_02`.

**Authority basis:** The toolbox README requires that preserved file metadata and slice state be coherent for downstream inspection. The obligation contract (Ob16, Categorical Handoff Readiness) requires that the captured signal be "inspectable." A dangling file_id reference would silently break inspectability.

**Impact:** Currently benign (single slice always gets all file IDs from the same pass). Becomes a correctness gap when multi-slice adapters build slices with partial file assignments.

**Minimum closure condition:** Add a `model_validator` to `SourceCapturePacket` that verifies: every `file_id` in every `slice.preserved_file_ids` exists in `preserved_files`. Optionally also check that every `preserved_files[*].file_id` is referenced by at least one slice.

**Next authorized action:** Bounded implementation change to `models.py`.

---

### F-05 — MINOR

**Criterion:** Raw preservation and inspectability; repo hygiene  
**Location:** `orca-harness/source_capture/writer.py:249–250` — `_copy_preserved_files` — `original_path` construction  
**Finding:** `original_path` in `PreservedFile` stores the absolute resolved OS path: `str(source_path)` where `source_path = path.resolve()`. Dry-run outputs confirm this: `"original_path": "C:\\Users\\vmon7\\Desktop\\projects\\orca\\docs\\product\\..."`.

**Evidence (dry-run 1 manifest):**
```json
"original_path": "C:\\Users\\vmon7\\Desktop\\projects\\orca\\docs\\product\\data_capture_spine_pressure_test_..."
```

**Impact:** Two concerns:

1. **Portability:** A committed packet with an absolute OS path embeds operator filesystem topology. A different reviewer opening the packet on a different machine would see a path that does not resolve on their system. This is an inspectability limitation rather than a correctness failure — the raw file is still present at `relative_packet_path`.

2. **Privacy/hygiene:** Username (`vmon7`) and full local path are baked into committed review artifacts. This is relevant if packets are eventually committed as fixtures.

**Authority basis:** The toolbox README requires that packets be "inspectable." An absolute path that is non-resolvable on reviewer machines reduces inspectability. The obligation contract (Ob16) requires inspection without recollection.

**Minimum closure condition (advisory):** Document in `orca-harness/docs/source_capture_packet.md` that `original_path` records the absolute path as-of-capture and is a provenance field (not a live locator). For committed fixtures, note that the value is for provenance traceability only. No code change required for checkpoint 1, but consider whether future committed packets should use a relative path from the repo root or a provenance comment instead.

**Next authorized action:** Documentation note or design choice deferred to fixture admission decision.

---

### F-06 — MINOR

**Criterion:** CLI correctness  
**Location:** `orca-harness/runners/run_source_capture_packet.py:37–53` — `build_optional_fact`  
**Finding:** The multi-supply conflict check uses Python truthiness (`if item`) rather than `is not None`. An empty-string argument passed as a positional value would not register as "supplied" in the count, bypassing the conflict check.

**Evidence:**
```python
supplied = [
    item
    for item in (value, unknown_reason, not_attempted_reason, not_applicable_reason)
    if item        # ← truthiness, not `is not None`
]
if len(supplied) > 1:
    raise ValueError(f"{label} accepts only one value/reason flag")
```

If a CLI caller somehow passes `--cutoff-posture ""` (empty string), the truthiness check would evaluate it as not supplied, while `--cutoff-posture-unknown-reason "some reason"` would count as one supplied item — no conflict raised even though two flags were passed. However, `known_fact("")` would then fail the `VisibleFact` model validator (`not self.value` is True for empty string), so the validation catch downstream would surface the error.

**Impact:** Low — the model validator catches the empty-string case downstream. The risk is primarily a readability and defense-in-depth issue. The outer conflict check should use `is not None` for accuracy and clarity.

**Minimum closure condition:** Change `if item` to `if item is not None` in the list comprehension. Verify the VisibleFact test for the known-empty-value case.

**Next authorized action:** Bounded implementation change to `runners/run_source_capture_packet.py`.

---

### F-07 — MINOR

**Criterion:** CLI correctness; access posture metadata truthfulness  
**Location:** `orca-harness/runners/run_source_capture_packet.py:199–201` — `access_posture` flag construction  
**Finding:** The CLI provides `--access-posture` (value) for `access_posture` but has no `--access-posture-unknown-reason` or `--access-posture-not-attempted-reason` flag. When `--access-posture` is not supplied, the writer defaults to `known_fact("local_file_only")`.

**Evidence (runner parser, lines 199–201):**
```python
access_posture=build_optional_fact(
    label="access posture",
    value=args.access_posture,
    # no unknown_reason, not_attempted_reason, or not_applicable_reason
),
```

Compare with `archive_history_posture` which also has `--archive-history-not-attempted-reason`, or `actor_audience_context` which has `--actor-audience-context-unknown-reason`. The `access_posture` field only accepts a value or inherits the default `known_fact("local_file_only")`.

**Impact:** For checkpoint 1 (local file only), access posture is always `local_file_only` and the default is correct. However, if a future use of the local-file CLI packages a file from a network share, a mounted volume, or a path whose access character is genuinely unknown, there is no CLI path to express that. An operator would be forced to accept the incorrect `known_fact("local_file_only")` or call the writer Python API directly.

**Minimum closure condition (advisory):** Add `--access-posture-unknown-reason` flag before any adapter mode uses the local-file CLI with non-local-file access postures. Not a blocker for checkpoint 1.

**Next authorized action:** Design note or deferred flag addition before first adapter that could produce non-`local_file_only` access posture.

---

### F-08 — MINOR

**Criterion:** Test coverage  
**Location:** `orca-harness/tests/unit/test_source_capture_packet.py`  
**Finding:** Several correctness-relevant edge cases are not covered by red-green tests:

1. **`VisibleFact` negative cases not tested directly:**
   - `VisibleFact(status="known")` with no `value` — should raise; not tested as a standalone case.
   - `VisibleFact(status="unknown_with_reason")` with no `reason` — should raise; not tested.
   - `VisibleFact(status="some_arbitrary_string", reason="x")` — passes silently (see F-01); not tested.

2. **Writer empty-input guard not tested:**
   - `write_local_source_capture_packet(..., input_files=[])` — raises `ValueError("at least one input file is required")`; no test for this.

3. **Non-file input path not tested:**
   - Passing a directory path as an input file raises `ValueError("input path is not a file: ...")` — no test.

4. **Multi-file packet not tested:**
   - The writer supports multiple input files (produces `file_01`, `file_02`, etc.) but no test exercises this path. Multi-file slice assignment behavior (all files go into `slice_01`) is not regression-tested.

5. **Full `NON_CLAIMS` set in receipt not verified:**
   - `test_writer_copies_files_records_sha256_and_writes_manifest_and_receipt` only checks `"not source acquisition" in receipt_text`. The full 10-item NON_CLAIMS list (defined in `writer.py:27–38`) is not compared against the receipt content.

**Authority basis:** AGENTS.md requires "define and run relevant verification or state why it was not run." The toolbox README states "no-network/no-deferred-adapter guard tests" as a required component (now present for the core, but the coverage gaps above could hide regressions in the core behaviors).

**Impact:** Items 1 and 2 could hide a regression in the `VisibleFact` validator if the model is refactored. Items 3–5 are lower risk but represent unchecked code paths.

**Minimum closure condition:** Add targeted tests for: `VisibleFact` known-without-value, `VisibleFact` non-known-without-reason, writer with empty input list, and full `NON_CLAIMS` comparison in the receipt test. Multi-file and non-file-path tests are advisory.

**Next authorized action:** Bounded test additions under current first-tranche build authorization.

---

### F-09 — OPTIONAL

**Criterion:** Repo hygiene — dry-run output commit status  
**Location:** `orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run/`, `slot3_reddit_batch1_packet_dry_run_2/`  
**Finding:** Both dry-run packet directories are in the `orca-harness/reports/source_capture/` path. The harness README states: "commit generated scores only under a separate fixture-admission decision." No equivalent rule is documented for `reports/source_capture/` outputs.

The dry-run packets contain:
- Absolute OS paths (operator username visible in `original_path`)
- A `raw/` subdirectory with the preserved source artifact (a pressure-test capture markdown)
- Timestamps from the capture session

These are appropriate as review evidence for this code review. Whether they should be committed as permanent fixtures (vs. left as review-evidence artifacts) is not determined by any current policy.

**Impact:** No correctness impact. The hygiene question is whether future maintainers would treat committed dry-run packets as canonical fixtures or as review scratch. The `original_path` field embeds operator-specific paths that would be misleading on other machines.

**Minimum closure condition:** No action required before checkpoint 1 acceptance. Before committing the dry-run packets permanently, establish a fixture admission policy for `reports/source_capture/` outputs analogous to the score fixture admission rule in the harness README.

**Next authorized action:** Documentation or overlay rule. Not a code fix.

---

### F-10 — OPTIONAL

**Criterion:** Dry-run evidence; metadata coherence  
**Location:** Both dry-run manifests — `source_locator.value` vs. `preserved_files[0].original_path`  
**Finding:** The `source_locator` in both dry-run packets is a relative path (`../docs/product/data_capture_spine_pressure_test_slot_3_...`), while `original_path` in `preserved_files` is an absolute path (`C:\Users\vmon7\Desktop\projects\orca\docs\product\...`). Both point to the same file but via different path conventions.

**Evidence (dry-run 1):**
```json
"source_locator": { "status": "known", "value": "../docs/product/data_capture_spine_pressure_test_..." },
"preserved_files": [{ "original_path": "C:\\Users\\vmon7\\Desktop\\projects\\orca\\docs\\product\\data_capture_spine_pressure_test_..." }]
```

**Impact:** This is an operator choice (the CLI received a relative path via `--source-locator`), not a model defect. However, a reviewer who follows the `source_locator` to reconstruct provenance would get a relative path that resolves only from the packet directory's parent, while the `original_path` resolves only on the original machine. Neither path is universally stable. This is a documentation/convention gap rather than a model error.

**Minimum closure condition (advisory):** Document in `orca-harness/docs/source_capture_packet.md` that `source_locator` is an operator-supplied provenance pointer (may be relative, absolute, or URL), while `original_path` is the resolved absolute path at capture time. No code change required.

**Next authorized action:** Documentation clarification.

---

### F-11 — OPTIONAL

**Criterion:** Multi-slice risk (secondary)  
**Location:** `orca-harness/source_capture/writer.py:130` — `slice_id="slice_01"`  
**Finding:** The slice ID is the literal string `"slice_01"`, not a ULID, ordinal, or generated value. No naming convention exists for slice IDs beyond this single hardcoded value.

**Impact:** Not a blocker for checkpoint 1. When multi-slice support is added (see F-02), adapters will need to choose a slice ID convention. If different adapter authors independently choose `"slice_01"`, `"slice_02"`, or `"{locator_hash}"`, packet consumers could see inconsistent slice ID schemas across adapter types. This is a naming convention gap.

**Minimum closure condition (advisory):** Decide slice ID convention (e.g., ordinal `"slice_01"`, `"slice_02"`; or ULID-based; or locator-derived) before the first multi-slice adapter implementation. Document the convention in `orca-harness/docs/source_capture_packet.md`.

**Next authorized action:** Design note before multi-slice adapter scoping.

---

## Review Summary — Criteria Assessment

| Criterion | Assessment | Blocking finding? |
|---|---|---|
| 1. Packet-boundary fit | Clean: no ECR, Cleaning, Judgment, scoring, or buyer-proof fields in model or writer. `StrictModel(extra="forbid")` prevents field additions without explicit schema change. | No |
| 2. No-network boundary | Core is clean. Contract test covers `source_capture/*.py` and `run_source_capture_packet.py`. Gap: `harness_utils` is outside the scan (F-03). | No (advisory) |
| 3. Raw preservation and inspectability | Files are copied verbatim with `shutil.copy2`, SHA256 recorded, manifest and receipt written. `original_path` records provenance. No lossy transformation. Minor gap: no cross-validation of slice file IDs (F-04). | No |
| 4. Metadata truthfulness | Defaults are honest non-known states, not fake success. All fields surfaced. Gap: `VisibleFact.status` vocabulary not schema-enforced (F-01). | Not for checkpoint 1; design gap for adapter fleet |
| 5. CLI correctness | Mutually exclusive source locator group works. Conflict handling in `build_optional_fact` works. Exit code 2 on all exception paths. Minor truthiness check issue (F-06). Access posture has no unknown flag (F-07). | No |
| 6. Dry-run evidence | Dry-run 1 is honest but metadata-thin. Dry-run 2 materially closes the thinness on actor, timing, posture, and mode-change dimensions. Progression is meaningful and demonstrates the CLI's optional metadata flag utility. | No |
| 7. Multi-slice risk | Model supports multiple slices. Writer API hardcodes single `slice_01` (F-02). Not a blocker for checkpoint 1. Is a design decision point before first multi-locator adapter. | Not now; before HTTP adapter |
| 8. Future-consumer boundary (Judgment C1/C2) | Clean: packet provides the posture data C1 would consume (timing, locator, hash, capture timestamp). No C3–C7 fields (participant safety, reveal quarantine, scoring, blind execution) are present or implied. | No |
| 9. Test coverage | Good coverage of happy path and primary error cases. Gaps in VisibleFact negative cases, empty input list, multi-file input, and full NON_CLAIMS set (F-08). | Advisory |
| 10. Repo hygiene | Dry-run outputs are review evidence. No existing fixture admission rule for `reports/source_capture/`. Absolute OS paths in `original_path` are provenance facts (F-09). | Advisory |

---

## Review Answer To The Commission Question

**Question:** Is the Source Capture Packet core a stable enough common container for future Data Capture source-acquisition tools, before Orca builds Direct HTTP/browser/API/archive/media adapters?

**Advisory assessment:**

The **packet model** (`models.py`) is stable as a container. It supports multiple slices, decomposed timing, all required posture fields, non-claims, and `StrictModel(extra="forbid")` prevents field additions without explicit schema changes. No ECR, Cleaning, or Judgment fields are present. The model can hold payloads from all planned first-tranche adapters.

The **writer API** (`write_local_source_capture_packet`) is single-slice-only and is not yet adapter-ready for multi-locator scenarios. This is a known limitation of the local-file checkpoint. It is not a blocker for accepting checkpoint 1 but creates a concrete design decision point before the Direct HTTP adapter is scoped. The decision (F-02) should be recorded before that scoping begins.

The **vocabulary enforcement gap** (F-01) is the most subtle container-stability risk. The `VisibleFact.status` field accepts arbitrary strings. Future adapters operating without the factory functions could silently drift the vocabulary. This should be closed (via a `Literal` or enum type) before the adapter fleet grows.

The **no-network contract test** is functional and correctly scans the source_capture package and runner. The gap (F-03) is the exclusion of `harness_utils` from the scan boundary — a bounded fix.

The **dry-run evidence** demonstrates meaningful packet behavior. Dry-run 2 closes the metadata thinness from dry-run 1 and demonstrates the CLI's optional metadata flags working end-to-end. The progression is acceptable review evidence for checkpoint 1.

**No findings are correctness blockers for checkpoint 1.** F-01 and F-02 are design decisions to be addressed before the adapter fleet begins.

---

## Non-Claims

This review is not: validation, readiness, approval, source-of-truth promotion, acceptance, mandatory remediation, patch authority, implementation scoping, or executor-ready handoff. Findings are decision input only. No patches are authorized by this review. No lifecycle claim is made about the dry-run outputs or the implementation as a checkpoint-admission artifact.

---

## Review Metadata

```yaml
review_id: source_capture_packet_core_adversarial_code_review_v0
review_date: 2026-06-02
reviewed_by: Claude Sonnet 4.6 (adversarial advisory review)
review_lane: advisory (zero-config + pinned source authority)
hash_verification: all 17 pins matched
findings_count: 11
blocking_or_major_findings: [F-01, F-02]
minor_findings: [F-03, F-04, F-05, F-06, F-07, F-08]
optional_findings: [F-09, F-10, F-11]
patch_queue: none authorized
next_action_required: owner or implementer decision on F-01 (VisibleFact vocabulary enforcement) and F-02 (multi-slice writer API path) before HTTP adapter scoping
```
