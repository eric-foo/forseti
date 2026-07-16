# Adversarial Code Review: Source Quality State Assembler v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Adversarial implementation review of the Source Quality State Assembler over source-quality queue rows and existing Source Capture Packet manifests.
use_when:
  - Inspecting Source Quality State Assembler findings before patching or reuse.
  - Tracing assembler changes to this review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_lane: adversarial_implementation_review
output_mode: filesystem-output
required_output_path: docs/review-outputs/source_quality_state_assembler_adversarial_code_review_v0.md
review_date: 2026-06-03
reviewer: Claude Sonnet 4.6 (workflow-deep-thinking + workflow-code-review)
```

---

## Source-Read Ledger

### Primary Target Files

| File | SHA256 | Status |
| --- | --- | --- |
| `orca-harness/source_capture/source_quality.py` | `ACB9D8DCA14AA957C58BB81C7B81F9606574D7F2B96D2960C0FC7198E685F83B` | Read |
| `orca-harness/runners/run_source_quality_state_assembler.py` | `FF0874EB1D07E7E312080820C8ED5E819E4A4C34213A6792A46595E5DD3838C3` | Read |
| `orca-harness/source_capture/__init__.py` | `293F59AE0A296DC4A1B8592F9C82D56637967450300A4139D1DC71CDE2E6A715` | Read |
| `orca-harness/tests/unit/test_source_quality_state_assembler.py` | `8662DD3864AEAA7102F59C1F96127663DC0DF95BA07284CC1A4D7E196C99F7D1` | Read |
| `orca-harness/tests/contract/test_source_quality_report_skeleton_contract.py` | `40FA6B5B69708E90AFCB27A4430C668CB0E9A20969A4026042983A77195A947B` | Read |
| `orca-harness/docs/source_capture_agent_runbook.md` | `504BD76C0316464906E7C7BF071EB23A0ECBEC301E42531D04AA5F26BF1C1DD8` | Read |
| `orca-harness/README.md` | `F42E1B1048275E710603633F9BD37BCBADEE85E5470C22D9E4FDCA149BE2A53F` | Read |
| `docs/product/source_capture_toolbox/README.md` | `AD83B8EB80EB5ECDB7B19AECEDCF9CB264724FC1D35DCA273B6F382DB17D936D` | Read |

### Source-Basis Files

| File | SHA256 | Status |
| --- | --- | --- |
| `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` | `39CB2E59F1827CAE9B5CF0806D3236222DAC5800FB128254B1AD54479F97694E` | Read |
| `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | `048CC8065CC57683C8A783B471E19D60DBB7F4768DDFE81ABFCAE604CCBAEA09` | Read |
| `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` | `50222211694DB2AD335DBAFAD98B5163A631EB288BE3CBCB5EBDDCE87F2ECC01` | Read |
| `orca-harness/source_capture/models.py` | `09C032C768A58FC7562F0E0D1CB34CBC4ACD2D1211723AC0ACDC1F97ECEB46B3` | Read |
| `orca-harness/source_capture/writer.py` | `F6BC4BDB8CA0B9EC50406D782CB97CD12FF704D42684117F82D931B3F44B50CD` | Read |
| `orca-harness/runners/run_source_quality_report_skeleton.py` | `1616479E71DA67821CAF96FC5F8D1999949A157D55191BD3D4EF071E3FB55897` | Read |
| `orca-harness/tests/unit/test_source_quality_report_skeleton.py` | `D91A58BAD446A74A90493A8690B650B2EF75D5D76209C74DA9B75357DDED6247` | Read |
| `.agents/workflow-overlay/source-of-truth.md` | `7DFBF052A098C0AD77A5598BB6EA4738DA9AD6943D391852DC2E032A173182EF` | Read |
| `.agents/workflow-overlay/review-lanes.md` | `2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199` | Read |
| `.agents/workflow-overlay/validation-gates.md` | `FD7AE96F481733ED7FA5F1DDE252B7CF6A7C5A9053DAC7317795353F003F520F` | Read |

All 18 required files are present and readable. No missing files. No blocked result.

---

## Validation Rerun Results

**Focused test suite:**

```
python -m pytest -p no:cacheprovider tests/unit/test_source_quality_state_assembler.py tests/unit/test_source_quality_report_skeleton.py tests/contract/test_source_quality_report_skeleton_contract.py -v
```

Observed: **19 passed** in 1.57s. Matches implementer's claim.

**Full harness:**

```
python -m pytest -p no:cacheprovider
```

Observed: **164 passed** in 31.61s. Matches implementer's claim.

**Vocabulary verification:** Python import check confirmed:
- `RESULT_TOKENS` (7 tokens) exactly matches `source_quality_mini_god_tier_profile_v0.md`
- `ROW_STATUSES` (5 tokens) exactly matches `source_quality_source_unit_queue_template_v0.md`
- `LIFECYCLE_STATES` (4 tokens) exactly matches the Mini God-Tier profile

**Forbidden import scan:** Static AST analysis of `source_quality.py` and `run_source_quality_state_assembler.py` found zero imports from: `aiohttp`, `bs4`, `httpx`, `playwright`, `requests`, `scrapy`, `selenium`, `socket`, `urllib`.

**Overclaim scan:** All matches in target files for `mini_god_tier_met`, `not fixture admission`, `not Judgment scoring`, etc. are located in constant definitions, the `RESULT_TOKENS` set membership, non-claims lists, or explanatory string literals that explicitly deny the claim. No live assertion of `mini_god_tier_met` or equivalent batch verdict found.

**Whitespace/CRLF check:** Not rerun directly; the implementer noted LF-to-CRLF warnings only. These are OS-level line-ending artefacts and do not affect correctness on the target Windows platform.

---

## Findings

### MAJOR — M-01: Toolbox README "Overall Gaps" has stale "not implemented" claim for the State Assembler

**Finding ID:** M-01
**Target:** `docs/product/source_capture_toolbox/README.md` — `## Overall Gaps` section
**Evidence:** The "Overall Gaps" section lists the State Assembler under *"Recorded architecture boundaries that are not implemented tooling"*:

```
Recorded architecture boundaries that are not implemented tooling:
- Source Quality State Assembler architecture boundary for a read-only
  multi-row state census over existing packets.
```

This contradicts the same document's `### Source Quality State Assembler` component subsection, which correctly states:

```
The helper is implemented in
`orca-harness/runners/run_source_quality_state_assembler.py`.
```

The implementation is confirmed present (`source_quality.py:136`, `run_source_quality_state_assembler.py`, tests). The DCP receipt in the runbook lists `docs/product/source_capture_toolbox/README.md` as a `controlling_sources_updated` entry for the State Assembler helper, but the "Overall Gaps" section was not updated during that propagation.

**Authority basis:** `source_quality_state_assembler_v0.md` DCP `controlling_sources_updated` includes this README; AGENTS.md requires that completion claims not be made when required source updates are incomplete.

**Impact:** The toolbox README is the primary product-facing entrypoint for the Source Capture Toolbox. An operator or agent reading the status summary in "Overall Gaps" will conclude the State Assembler is not yet available, even though it is implemented and tested. The contradiction between sections creates unreliability in the document.

**Minimum closure condition:** Remove "Source Quality State Assembler architecture boundary for a read-only multi-row state census over existing packets." from the "Recorded architecture boundaries that are not implemented tooling" list and add the State Assembler to the "Implemented first-tranche pieces" list, consistent with the already-updated component subsection.

**Next authorized action:** Owner decision to apply a doc patch to the "Overall Gaps" section. This is an advisory-level patch to documentation consistency; it does not require a new DCP receipt if no doctrine is changed.

**Patch queue:** Not emitted — this is adversarial artifact review, read-only output.

---

### MINOR — m-01: No test for invalid `packet_lifecycle` on a row with an otherwise valid packet path

**Finding ID:** m-01
**Target:** `orca-harness/tests/unit/test_source_quality_state_assembler.py`
**Evidence:** `_validate_row_state` (`source_quality.py:519`) correctly adds a visible stop for invalid lifecycle states. When the row also carries a valid packet path, `build_source_quality_report_skeleton` subsequently raises `ValueError` (lifecycle validation fails at line 87–89) which is caught at line 499–506, producing a second visible stop and `helper_state: helper_failed`. This combined path is untested. Existing tests cover manifestly broken/missing packets or valid lifecycle states only.

**Impact:** A regression that suppressed the lifecycle validation stop on the combined path would not be caught by the test suite. The implementation is currently correct; the gap is discriminating coverage.

**Minimum closure condition:** A unit test that supplies a row with a valid packet path AND an invalid `packet_lifecycle` value (e.g., `"production"`) and asserts both a lifecycle visible stop and `helper_state: "helper_failed"`.

**Next authorized action:** Advisory — owner may add the test in a later implementation turn.

---

### MINOR — m-02: No test for `operator_reported_result_token_valid: False` when an invalid token is supplied

**Finding ID:** m-02
**Target:** `orca-harness/tests/unit/test_source_quality_state_assembler.py`
**Evidence:** `_validate_row_state` (`source_quality.py:527–529`) adds a visible stop and the assembled dict sets `operator_reported_result_token_valid: False` when a non-profile token appears. The test suite has no case for this path.

**Impact:** A regression removing or misrouting the token validation would not be caught.

**Minimum closure condition:** A unit test supplying `result_token: "invalid_token"` in a row and asserting `operator_reported_result_token_valid: False` and the corresponding visible stop.

**Next authorized action:** Advisory — owner may add the test in a later implementation turn.

---

### MINOR — m-03: All unit tests are single-row; multi-row census aggregation is not covered

**Finding ID:** m-03
**Target:** `orca-harness/tests/unit/test_source_quality_state_assembler.py`
**Evidence:** Every unit test passes exactly one row to `build_source_quality_state_census`. The CLI integration test also uses a single-row queue. `_build_state_census` aggregates counts across all rows (`source_quality.py:535–551`) but this path is not exercised with mixed states (e.g., one `manifest_inspectable` + one `manifest_missing` row).

**Impact:** A regression that broke cross-row aggregation in `_build_state_census` (e.g., wrong Counter key, off-by-one in `visible_stop_count`) would not be caught.

**Minimum closure condition:** A unit test with at least two rows in different states and assertions on the aggregate `census` counts.

**Next authorized action:** Advisory — owner may add the test in a later implementation turn.

---

### ADVISORY — a-01: Valid-packet test does not assert `visible_stop_count == 0`

**Finding ID:** a-01
**Target:** `test_source_quality_state_assembler.py:28` (`test_state_assembler_surfaces_existing_packet_skeleton_without_finalizing`)
**Evidence:** The test verifies the "happy path" skeleton state but does not assert `census["census"]["visible_stop_count"] == 0`. A regression that spuriously added stops to clean rows would not be caught here.

**Next authorized action:** Optional hardening — add `assert census["census"]["visible_stop_count"] == 0` to the existing test.

---

### ADVISORY — a-02: No multi-row CLI integration test

**Finding ID:** a-02
**Target:** `test_source_quality_state_assembler.py:134` (`test_cli_writes_state_census_yaml`)
**Evidence:** The subprocess integration test uses a single-row queue. A multi-row CLI path with mixed outcomes is not tested end-to-end.

**Next authorized action:** Optional hardening.

---

### ADVISORY — a-03: Undocumented `lifecycle_state` alias in row assembly

**Finding ID:** a-03
**Target:** `source_quality.py:445`
**Evidence:**
```python
lifecycle_state = _row_text(row, "packet_lifecycle",
    default=_row_text(row, "lifecycle_state", default="scratch"))
```
The fallback from `packet_lifecycle` to `lifecycle_state` enables the queue template's canonical field name (`packet_lifecycle`) while also accepting the skeleton helper's internal field name (`lifecycle_state`) as an alias. This alias is not documented in the runbook or architecture spec. If an operator inadvertently supplies `lifecycle_state` in a queue (thinking they're setting the lifecycle), they will get the expected behavior — but for unintended reasons.

The `"scratch"` default when neither field is present is reasonable but also undocumented.

**Next authorized action:** Optional documentation clarification in the runbook. Low priority; the behavior is safe.

---

## Answers to the 10 Review Questions

**Q1. Does `build_source_quality_state_census` preserve the architecture boundary from `source_quality_state_assembler_v0.md`?**

Yes. The function reads explicit rows, reads existing packet directories or manifests, invokes `build_source_quality_report_skeleton` (the authorized read-only helper), surfaces visible stops per row, and emits a state census. No network calls, no source acquisition, no runner dispatch, no scoring, no finalization. The architecture's "only allowed flow" from the spec (`queue row → packet path → exists check → inspectability check → read-only skeleton → operator-finalization requirement → state census`) is implemented faithfully.

**Q2. Does the CLI stay a thin read-only wrapper, or does it create runner-dispatch / workflow-authority ambiguity?**

The CLI stays a thin read-only wrapper. It reads a YAML queue file, calls `build_source_quality_state_census`, and writes YAML output. It does not dispatch, chain, or select runners. The `--output` existence check prevents silent overwrites. No runner-dispatch or workflow-authority ambiguity was found.

**Q3. Are missing packet paths, missing manifests, invalid manifests, invalid row status, invalid result token, and invalid lifecycle state preserved as visible row-level stops rather than hidden failures or fake success?**

Yes, with all primary paths confirmed:

| Failure mode | Handler location | Disposition |
| --- | --- | --- |
| No `packet_path`/`manifest_path` in row | `source_quality.py:477–481` | `visible_stops` entry; `packet_state: not_cited` |
| Manifest path does not exist | `source_quality.py:485–488` | `packet_state: manifest_missing`; visible stop |
| Manifest exists but is invalid JSON or fails model validation | `source_quality.py:499–506` (exception catch) | `packet_state: manifest_uninspectable`; `helper_state: helper_failed`; visible stop |
| Invalid `row_status` | `source_quality.py:526–528` | visible stop; `row_status_valid: False` |
| Invalid `result_token` | `source_quality.py:528–530` | visible stop; `operator_reported_result_token_valid: False` |
| Invalid `lifecycle_state` | `source_quality.py:530–532` | visible stop; `packet_lifecycle_valid: False`; also triggers helper failure when a valid packet exists (double stop — correct) |

**Q4. Does the aggregate `census` shape avoid pass/fail or verdict semantics?**

Yes. The `census` dict contains only: `row_status_counts`, `packet_state_counts`, `helper_state_counts`, `suggested_result_token_counts`, `operator_finalization_required_count`, `visible_stop_count`, and `rows_with_visible_limitations_count`. No `verdict`, `pass`, `fail`, `all_rows_passed`, `ladder_complete`, or equivalent key is present. The output is counts only.

`operator_finalization_required_count` is always equal to `row_count` because every code path sets `result_token_finalization: "operator_review_required"`. This is intentional and correct — it cannot be read as "some rows are finalized."

**Q5. Does the implementation preserve `result_token_finalization: operator_review_required` and avoid automated `mini_god_tier_met`?**

Yes. `result_token_finalization: "operator_review_required"` is hardcoded in three places:
1. The assembled row default (`source_quality.py:470`)
2. Passed through from the skeleton helper for inspectable packets (`source_quality.py:512` → `skeleton["result_token_finalization"]` which is always `"operator_review_required"` per `source_quality.py:116`)
3. `_suggest_result_token` (`source_quality.py:286–300`) never returns `MINI_GOD_TIER_MET`. The strongest suggestion is `MINI_GOD_TIER_WITH_VISIBLE_LIMITATIONS`.

`MINI_GOD_TIER_MET` appears in `RESULT_TOKENS` (line 44) — this is correct, as it allows operator-supplied queue rows that already carry that token to pass validation without error. The assembler echoes operator-supplied tokens but never generates them.

**Q6. Are result-token, lifecycle, and row-status vocabularies correctly sourced from existing profile/template vocabulary?**

Confirmed by direct comparison:
- `RESULT_TOKENS` (7 items) matches `source_quality_mini_god_tier_profile_v0.md` exactly.
- `LIFECYCLE_STATES` (4 items) matches the profile exactly.
- `ROW_STATUSES` (5 items) matches `source_quality_source_unit_queue_template_v0.md` exactly.

No new tokens are minted by the assembler.

**Q7. Does the no-acquisition import contract cover the new assembler and CLI sufficiently?**

Yes. The contract test `test_source_quality_report_skeleton_contract.py` was updated to include `run_source_quality_state_assembler.py` in its `target_paths` list (line 25). The contract checks cover: `aiohttp`, `bs4`, `httpx`, `playwright`, `requests`, `scrapy`, `selenium`, `socket`, `urllib`. A static AST scan on both files confirmed zero forbidden imports.

**Q8. Are the tests discriminating enough to catch fake-success regressions?**

The primary fake-success paths are covered:
- Asserts `suggested_result_token != "mini_god_tier_met"` on a valid packet path
- Asserts `result_token_finalization == "operator_review_required"` for every case
- Asserts `packet_state: manifest_missing` + visible stop for missing manifest
- Asserts `helper_state: helper_failed` for invalid manifest
- Asserts visible stop for no-packet-path row

Gaps (see m-01, m-02, m-03): invalid lifecycle/status/token combinations on valid packets are not tested; multi-row aggregation is not tested. These are discriminating-coverage gaps, not implementation bugs.

**Q9. Do docs and DCP wording overclaim implementation status, validation, readiness, fixture admission, source discovery, runner dispatch, or Judgment authority?**

The runbook (`source_capture_agent_runbook.md`) and harness README wording are within bounds. The State Assembler description in both correctly states it is a read-only state census helper and does not overclaim.

**Exception — M-01:** `docs/product/source_capture_toolbox/README.md` "Overall Gaps" section retains the claim that the State Assembler is "not implemented tooling." This is a stale underclaim (the opposite direction) that creates internal contradiction with the component subsection. It does not overclaim, but it is an accuracy defect that could mislead.

No validation, readiness, fixture admission, source discovery, runner dispatch, or Judgment authority language was found in any target doc.

**Q10. Any blast-radius issue from adding assembler exports to `source_capture.__init__`?**

Bounded. The additions are:
- `build_source_quality_state_census` — the assembler function
- `SOURCE_QUALITY_STATE_ASSEMBLER_VERSION` — a version string constant

Neither introduces network calls, writes, or acquisition behavior. The assembler is now accessible via `from source_capture import build_source_quality_state_census`, which is intentional. Internal helpers (`_validate_row_state`, `_assemble_source_quality_row`, `_build_state_census`, etc.) remain private (not in `__all__`). `resolve_manifest_path` is correctly not exported (confirmed by existing test `test_package_public_api_does_not_export_manifest_path_helper`).

One prior test explicitly validates the non-export of `resolve_manifest_path` — this guard remains in place and still passes.

---

## Recommendation

**Proceed with minor remediation.**

The State Assembler implementation is architecturally sound. The architecture boundary from `source_quality_state_assembler_v0.md` is correctly honored: read-only, no network, no acquisition, no runner dispatch, no scoring, no finalization, no batch verdict. The vocabulary is correctly sourced, failure modes surface as visible stops, and the no-acquisition contract test explicitly covers the new CLI.

One major finding (M-01) requires a documentation accuracy fix before the toolbox README can be used as a reliable status entrypoint: the "Overall Gaps" section must be updated to reflect that the State Assembler is now implemented. This fix is a bounded doc patch (no DCP receipt required if no doctrine changes). The three minor test gaps (m-01, m-02, m-03) are advisory and do not block usage.

No critical or blocking findings.

---

## Non-Claims

- This review is not validation, readiness, fixture admission, source completeness proof, or Judgment authority.
- Review findings are decision input only. They are not approval, mandatory remediation, or executor-ready patch authority until separately accepted or authorized.
- This review does not authorize any patch to the reviewed files.
- This review does not constitute a `PASS` or `ADEQUATE_NOW` claim.
- Confirmed test passage (19 focused, 164 full) is rerun evidence only; it does not prove all possible failure modes are covered.
- Vocabulary match confirmation is not a source-of-truth promotion for the vocabulary tables in `source_quality.py`.
