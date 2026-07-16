# Adversarial Code Review: Source Quality Report-Skeleton Helper

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Read-only adversarial implementation/code review of the Source Quality report-skeleton helper.
use_when:
  - Deciding whether the helper is safe for agent-reuse.
  - Inspecting fake-pass, boundary leakage, result-token semantics, lifecycle claims, and test sufficiency.
review_authority_boundary: advisory_review_output
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

## Review Identity

| Field | Value |
| --- | --- |
| Review type | Adversarial code review — read-only, no patches |
| Worktree | `C:\Users\vmon7\Desktop\projects\orca` |
| Expected branch | `main` |
| Expected HEAD | `6cd8a95` |
| Review date | 2026-06-03 |
| SHA256 pin verification | All 18 pins OK (see §PIN VERIFICATION) |
| Skills loaded | `workflow-deep-thinking`, `workflow-code-review` |

---

## Pin Verification

All target and source-basis files verified before review. No `HASH_MISMATCH`.

| File | Result |
| --- | --- |
| `orca-harness/source_capture/source_quality.py` | OK |
| `orca-harness/runners/run_source_quality_report_skeleton.py` | OK |
| `orca-harness/source_capture/__init__.py` | OK |
| `orca-harness/tests/unit/test_source_quality_report_skeleton.py` | OK |
| `orca-harness/tests/contract/test_source_quality_report_skeleton_contract.py` | OK |
| `orca-harness/docs/source_capture_agent_runbook.md` | OK |
| `orca-harness/README.md` | OK |
| `docs/product/source_capture_toolbox/README.md` | OK |
| `docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md` | OK |
| `docs/prompts/hygiene-queue/precompact_source_quality_report_skeleton_helper.md` | OK |
| `AGENTS.md` | OK |
| `.agents/workflow-overlay/README.md` | OK |
| `.agents/workflow-overlay/source-of-truth.md` | OK |
| `.agents/workflow-overlay/source-loading.md` | OK |
| `orca-harness/source_capture/models.py` | OK |
| `orca-harness/pyproject.toml` | OK |
| `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | OK |
| `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` | OK |

---

## Source-Read Ledger

| Source | Status | Purpose |
| --- | --- | --- |
| `AGENTS.md` | clean (in git, modified) | Agent behavior kernel and Orca overlay instructions |
| `.agents/workflow-overlay/README.md` | clean (in git, modified) | Overlay entrypoint and binding rule |
| `.agents/workflow-overlay/source-of-truth.md` | clean (in git, modified) | Source hierarchy, conflict rules, DCP contract |
| `.agents/workflow-overlay/source-loading.md` | clean (in git, modified) | Source-loading budgets and read packs |
| `orca-harness/source_capture/source_quality.py` | clean (in git, modified) | Primary review target: skeleton helper logic |
| `orca-harness/runners/run_source_quality_report_skeleton.py` | clean (in git, modified) | Primary review target: CLI wrapper |
| `orca-harness/source_capture/__init__.py` | clean (in git, modified) | Primary review target: package export surface |
| `orca-harness/tests/unit/test_source_quality_report_skeleton.py` | clean (in git, modified) | Primary review target: unit tests |
| `orca-harness/tests/contract/test_source_quality_report_skeleton_contract.py` | clean (in git, modified) | Primary review target: contract tests |
| `orca-harness/docs/source_capture_agent_runbook.md` | clean (in git, modified) | Primary review target: doc coverage and DCP receipt |
| `orca-harness/README.md` | clean (in git, modified) | Primary review target: doc coverage |
| `docs/product/source_capture_toolbox/README.md` | clean (in git, modified) | Primary review target: doc coverage |
| `docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md` | clean (in git, modified) | Primary review target: helper-input context |
| `docs/prompts/hygiene-queue/precompact_source_quality_report_skeleton_helper.md` | clean (in git, modified) | Primary review target: pre-compact checkpoint |
| `orca-harness/source_capture/models.py` | clean (in git, modified) | Source basis: manifest model |
| `orca-harness/pyproject.toml` | clean (in git, modified) | Source basis: dependency and package scope |
| `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | clean (in git, modified) | Source basis: result token and lifecycle vocabulary authority |
| `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` | clean (in git, modified) | Source basis: queue template and row-status vocabulary |
| `orca-harness/_test_runs/source_quality_skeleton_cw_p1_20260603/cw_p1_skeleton.yaml` | untracked scratch | Optional dry-run evidence |
| `docs/workflows/orca_repo_map_v0.md` | available, not read | DCP receipt claims it was checked and intentionally not updated; unverified independently in this review |

Dirty-state note: multiple files in scope are modified in the working tree. Reviewing files as found. No source-authority diminishment for advisory findings; strict claims are not proved by reading modified source alone.

---

## Validation Run

Reviewer ran tests from `orca-harness/`:

```
python -m pytest -p no:cacheprovider tests/unit/test_source_quality_report_skeleton.py tests/contract/test_source_quality_report_skeleton_contract.py -v
```

**Result: 6 passed in 0.64s** — matches implementer's reported count.

Reviewers did not re-run the full 151-test suite or the 83-test source-capture stack. Those counts are taken as stated by the implementer and not independently verified.

---

## Findings

Ordered by severity. No critical or major findings.

---

### MINOR-01 — `separately_admitted` guard bypassed by string `"none"`

**Location:** `source_quality.py:54-55`; `run_source_quality_report_skeleton.py:29`

**Evidence:**

```python
if lifecycle_state == "separately_admitted" and not lifecycle_decision_reference:
    raise ValueError("separately_admitted requires lifecycle_decision_reference")
```

The guard fires when `lifecycle_decision_reference` is `None` (default) or empty string `""`. It does NOT fire when `lifecycle_decision_reference` is the string `"none"`, because `not "none"` evaluates to `False`. A CLI caller can pass `--lifecycle-decision-reference none` and reach `separately_admitted` output with a reference value that looks like a null sentinel:

```yaml
lifecycle_state: separately_admitted
lifecycle_decision_reference: none
```

This is visually indistinguishable from a valid separately-admitted row with no actual decision reference. An agent consuming the skeleton could misread this as having an acknowledged non-reference rather than a missing enforcement.

**Authority basis:** Implementation intent ("require `lifecycle_decision_reference` if `lifecycle_state=separately_admitted`"); `source_quality_mini_god_tier_profile_v0.md` lifecycle vocabulary ("If the report cannot cite the separate admission decision, do not use `separately_admitted`").

**Impact:** An agent or operator could mark a skeleton `separately_admitted` without providing a real reference, inflating lifecycle state beyond `scratch`. The conservative safety of the skeleton is not broken (non-claims remain; `result_token_finalization` is still `operator_review_required`), but the lifecycle guard can be silently defeated via CLI.

**Minimum closure condition:** Either add a check that `lifecycle_decision_reference not in (None, "", "none")`, or document in CLI help that `"none"` is a sentinel value that bypasses enforcement with equivalent effect.

**Next authorized action:** Advisory — operator may choose to patch before CLI-facing agent deployment, or accept as-is if the CLI is only used under direct operator supervision.

**Test coverage:** No test for this bypass path. `test_separately_admitted_requires_lifecycle_decision_reference` only tests the `None` case.

---

### ADVISORY-01 — `visible_limitations` fallback `["none_observed_in_manifest"]` may be misread without context

**Location:** `source_quality.py:90`

**Evidence:**

```python
"visible_limitations": visible_limitations or ["none_observed_in_manifest"],
```

`_build_visible_limitations()` returns an empty list when: all of `packet.limitations`, `packet.warnings`, per-slice limitations and warning notes are empty; the body is not metadata-only; the source surface is not `archive_org_wayback`; and both `archive_history_posture` and `media_modality_posture` have status `KNOWN` or `NOT_APPLICABLE`. In that scenario the output says `["none_observed_in_manifest"]`, which reads as "no limitations were observed in the manifest."

This is technically accurate, but an agent reading `none_observed_in_manifest` without also reading `suggested_result_token`, `result_token_finalization`, and `operator_completion_required` might infer this is closer to `mini_god_tier_met` than it is. The mitigating fields are all present and mandatory in the output:

- `result_token_finalization: operator_review_required` — hardcoded, cannot be overridden
- `suggested_result_token: mini_god_tier_with_visible_limitations` — best case for a preserved body
- `operator_completion_required` — always has at least one entry

These mitigants are robust. The advisory is that the `none_observed_in_manifest` sentinel could stand alone in documentation excerpts or partial reads.

**Impact:** Claim inflation risk if the skeleton is read out of context. Not a code defect.

**Minimum closure condition:** None required. If desired, the string could be changed to `"none_observed_in_manifest: operator review still required"` to be self-contained. Optional documentation note in the runbook or README.

**Next authorized action:** Advisory — operator may improve phrasing or accept as mitigated by surrounding required fields.

---

### ADVISORY-02 — `resolve_manifest_path` exported from `__init__.py` widens public API surface

**Location:** `source_capture/__init__.py:18-22`, `__all__:43`

**Evidence:**

```python
from source_capture.source_quality import (
    SOURCE_QUALITY_REPORT_SKELETON_VERSION,
    build_source_quality_report_skeleton,
    resolve_manifest_path,
)
```

`resolve_manifest_path` is an internal path-resolution helper: if the supplied path is a directory, it appends `manifest.json`. Exporting it from the package public API (`__all__`) makes it a stable API surface that callers may depend on independently of `build_source_quality_report_skeleton`. A caller using `resolve_manifest_path` directly for other purposes could introduce behavior that bypasses the main function's lifecycle and limitation checks.

No import cycle risk. `source_quality.py` imports only `source_capture.models`, which imports `schemas.case_models`. The dependency graph is a DAG.

**Impact:** Minor API surface growth. Not a correctness defect.

**Minimum closure condition:** Remove `resolve_manifest_path` from `__all__` if there is no known agent or user need to call it independently. Keeping it if CLI or other callers need it is acceptable; the function itself is harmless.

**Next authorized action:** Advisory — operator may narrow `__all__` or accept as-is.

---

### ADVISORY-03 — `body_possession_not_proven` result token path has no dedicated test

**Location:** `tests/unit/test_source_quality_report_skeleton.py`

**Evidence:**

`_suggest_result_token()` has three code paths:

1. `body["kind"] == "metadata_only"` → `archive_body_not_preserved` (tested by `test_archive_metadata_only_suggests_archive_body_not_preserved`)
2. `body["kind"] != "preserved"` (i.e., `not_preserved`) → `body_possession_not_proven` (no test)
3. `body["kind"] == "preserved"` → `mini_god_tier_with_visible_limitations` (tested by `test_archive_snapshot_body_is_preserved_but_not_auto_met` and `test_direct_http_body_carries_archive_not_attempted_limitation`)

The `not_preserved` path is reached when: no `archive_snapshot_body` slice with a non-metadata file exists, no non-metadata file is found in any slice, and the packet is not `archive_org_wayback` with availability metadata. An example: a packet that has no preserved files or whose preserved files are all metadata files and source is not archive.org.

The `body_possession_not_proven` path is exercised in principle by the `SourceCapturePacket` pydantic model requiring `preserved_files: list[PreservedFile] = Field(min_length=1)`, so every real packet has at least one file. However, if all preserved files are metadata files and the packet is `direct_http` (not `archive_org_wayback`), the `not_preserved` path would be reached. This path is not tested.

**Impact:** Low — the three commissioned paths (`archive_body_not_preserved`, `archive snapshot body`, `Direct HTTP body`) are all covered. The untested path exists in logic but is harder to reach in practice. Not a fake-pass path (the token `body_possession_not_proven` is correctly conservative).

**Minimum closure condition:** Add one test for a packet where all preserved files are metadata files and source surface is `direct_http`, verifying `suggested_result_token == "body_possession_not_proven"`.

**Next authorized action:** Advisory — add test in a future maintenance pass; does not block agent reuse.

---

### ADVISORY-04 — Broad `except Exception` in CLI maps all errors to exit code 2

**Location:** `run_source_quality_report_skeleton.py:50-51`

**Evidence:**

```python
except Exception as exc:
    parser.exit(status=2, message=f"source-quality skeleton failed: {exc}\n")
```

Exit code 2 in other harness runners means CLI/config/user-input error. Here, a pydantic `ValidationError` on a malformed manifest file would also produce exit 2. From the agent runbook exit-code table, exit 2 means "report the exact missing or invalid input." A malformed manifest is not a user-input error — it is a data integrity issue. An agent following the runbook's exit-code guidance might incorrectly diagnose a broken manifest as an operator flag error.

**Impact:** Misclassified exit code for manifest validation failures. Agent diagnostics may be misleading. No fake-pass path.

**Minimum closure condition:** Distinguish `ValueError` (user-input, CLI misconfiguration, lifecycle rules) from `pydantic.ValidationError` (malformed manifest data) in the exception handler, or document that exit 2 means "helper failed" broadly.

**Next authorized action:** Advisory — acceptable for current agent-reuse scope; operator may patch for better diagnostics before broader deployment.

---

### ADVISORY-05 — `docs/workflows/orca_repo_map_v0.md` update claim unverified in this review

**Location:** DCP receipt in `orca-harness/docs/source_capture_agent_runbook.md:665-688`

**Evidence:**

The DCP receipt lists `docs/workflows/orca_repo_map_v0.md` in `downstream_surfaces_checked` and `intentionally_not_updated` with reason "Repo map already indexes the toolbox and runbook entrypoints; detailed helper command routing belongs in the README/runbook." This file is not in the pinned target set and was not read by this reviewer.

**Impact:** Cannot independently confirm the claim. The DCP receipt is correctly formed per `source-of-truth.md` contract. The risk is low: `source-loading.md` routes through the toolbox README (confirmed read), and the toolbox README explicitly indexes the helper. An agent following `source-loading.md → toolbox README → runbook` would reach the helper. An agent following the repo map directly without reading the toolbox README would depend on the unverified claim.

**Minimum closure condition:** None blocking agent reuse. If independent verification is needed, read `docs/workflows/orca_repo_map_v0.md` and confirm it references the toolbox README or runbook path.

**Next authorized action:** Advisory — operator may verify independently in a follow-on pass.

---

## Adversarial Question Answers

**Q1. Does `source_quality.py` avoid all source acquisition, source discovery, browser/API/network behavior, and source-body meaning inference?**

Yes. Imports are `__future__`, `json`, `pathlib`, `typing`, and `source_capture.models`. No network, browser, archive, API, or scraper imports. File reads in `_read_metadata_files()` are bounded to already-local packet-side metadata JSON files. No HTTP calls. No body meaning inference: `_is_metadata_path()` classifies files by suffix only; `_best_http_metadata()`, `_selected_snapshot_field()`, and `_availability_field()` read structured JSON fields from already-local metadata, not from parsed source bodies. The contract test confirms no forbidden import roots.

**Q2. Can any code path silently convert packet-write success or empty `limitations` into clean source-quality success?**

No. Three defense layers prevent it:

1. `_suggest_result_token()` has three branches returning `archive_body_not_preserved`, `body_possession_not_proven`, or `mini_god_tier_with_visible_limitations`. `mini_god_tier_met` is not a constant in the module and cannot be returned.
2. `result_token_finalization` is hardcoded to `"operator_review_required"` at line 80 with no conditional path.
3. `operator_completion_required` always includes at least `"review suggested_result_token against the Mini God-Tier profile"`.

The most favorable output for a fully preserved body with empty manifest limitations would be: `suggested_result_token: mini_god_tier_with_visible_limitations`, `result_token_finalization: operator_review_required`, `visible_limitations: ["none_observed_in_manifest"]`. This is not clean success — it explicitly requires operator review. See ADVISORY-01 for a wording note on the `none_observed_in_manifest` sentinel.

**Q3. Does Archive.org metadata-only behavior correctly produce `archive_body_not_preserved` rather than body-preserved or clean success?**

Yes, confirmed. `_detect_best_body()` evaluation order:

1. Looks for `archive_snapshot_body` slice with a non-metadata file → not found for CW-P1 (no such slice)
2. Iterates all slices for any non-metadata file → `archive_availability` slice has only `01_archive_availability_metadata.json`, which `_is_metadata_path()` correctly identifies as metadata → no body file found
3. Checks `source_surface == "archive_org_wayback"` AND `_has_archive_availability_metadata()` → both True → returns `metadata_only` body
4. `_suggest_result_token()` → `archive_body_not_preserved`

The dry-run evidence (`cw_p1_skeleton.yaml`) confirms: `suggested_result_token: archive_body_not_preserved`, `best_in_bound_body.posture: metadata_only`. Test `test_archive_metadata_only_suggests_archive_body_not_preserved` passes and asserts this behavior.

**Q4. Does the helper avoid auto-suggesting or finalizing `mini_god_tier_met`?**

Yes. The token `mini_god_tier_met` does not appear anywhere in `source_quality.py` as a return value, constant, or string. The three possible `suggested_result_token` values are `MINI_GOD_TIER_WITH_VISIBLE_LIMITATIONS`, `ARCHIVE_BODY_NOT_PRESERVED`, and `BODY_POSSESSION_NOT_PROVEN`. The `result_token_finalization` field is always `"operator_review_required"` with no conditional override.

Test `test_archive_snapshot_body_is_preserved_but_not_auto_met` asserts `skeleton["suggested_result_token"] != "mini_god_tier_met"` explicitly.

**Q5. Does `separately_admitted` correctly require a lifecycle decision reference?**

Mostly yes, with a bypass gap. The Python function guard at `source_quality.py:54-55` fires when `lifecycle_decision_reference` is `None` or `""`. It does NOT fire when `lifecycle_decision_reference` is the string `"none"`, which is also the default output value (line 93). A CLI caller can pass `--lifecycle-decision-reference none` to bypass enforcement. See MINOR-01. The Python API used directly with `lifecycle_decision_reference=None` (default) correctly raises.

**Q6. Are docs clear that this is a skeleton helper, not validation, fixture admission, source completeness proof, or Judgment scoring?**

Yes. Multiple surfaces carry explicit non-claims:

- `SKELETON_NON_CLAIMS` in output YAML: `["not validation", "not source completeness proof", "not fixture admission unless separately decided", "not Judgment scoring"]`
- `orca-harness/README.md` skeleton helper section: "does not fetch sources, parse source bodies for meaning, score source quality, admit fixtures, or run Judgment logic"
- `docs/product/source_capture_toolbox/README.md` source quality helper component description: matches implementation boundaries
- `orca-harness/docs/source_capture_agent_runbook.md` helper section: "does not fetch sources, parse source bodies for meaning, infer source-language anchors, discover sources, admit fixtures, score source quality, or finalize `mini_god_tier_met`"
- DCP receipt for the helper includes `non_claims` block covering all these dimensions

Non-claims coverage is well-distributed and redundant across operator-facing, agent-facing, and machine-readable surfaces.

**Q7. Are tests sufficient for the known false-success paths?**

The six commissioned paths are covered:

| Path | Test | Status |
| --- | --- | --- |
| metadata-only archive → `archive_body_not_preserved` | `test_archive_metadata_only_suggests_archive_body_not_preserved` | ✓ |
| archive snapshot body → `mini_god_tier_with_visible_limitations`, not `mini_god_tier_met` | `test_archive_snapshot_body_is_preserved_but_not_auto_met` | ✓ |
| Direct HTTP body → preserved, archive not-attempted limitation | `test_direct_http_body_carries_archive_not_attempted_limitation` | ✓ |
| `separately_admitted` requires lifecycle reference | `test_separately_admitted_requires_lifecycle_decision_reference` | ✓ |
| CLI YAML output | `test_cli_writes_yaml_report_skeleton` | ✓ |
| No forbidden runtime imports | `test_source_quality_report_skeleton_has_no_runtime_acquisition_imports` | ✓ |

Two gaps not in the commissioned list but noted:
- No test for `body_possession_not_proven` (ADVISORY-03)
- No test for the `separately_admitted + "none" string` bypass (MINOR-01)

**Q8. Does exporting the helper from `source_capture/__init__.py` introduce import cycles, dependency leakage, or widened public API risk?**

No import cycles. Dependency graph: `source_quality.py → source_capture.models → schemas.case_models`. This is a DAG with no cycle. `pyproject.toml` already includes `source_capture.*` in found packages, so the file is automatically in scope. The only concern is widened public API (ADVISORY-02): `resolve_manifest_path` is exported from `__all__` and could be depended on independently. No dependency leakage from external network or browser libraries.

**Q9. Does the direction-change propagation receipt in the runbook sufficiently cover output/lifecycle doctrine, or is there a downstream source-loading/repo-map gap?**

The DCP receipt is correctly formed per `source-of-truth.md` contract. `controlling_sources_updated` covers the runbook, harness README, and toolbox README. `downstream_surfaces_checked` covers all required surfaces including `source-loading.md` and `docs/workflows/orca_repo_map_v0.md`. Both are listed in `intentionally_not_updated` with stated reasons.

The `source-loading.md` justification ("already routes Data Capture source-access tooling through the toolbox README and runbook") is confirmed: `source-loading.md` Data Capture Intake Surface pack lists `docs/product/source_capture_toolbox/README.md`, which now indexes the helper. The routing chain `source-loading → toolbox README → runbook` is intact for an agent following source-loading guidance.

The `docs/workflows/orca_repo_map_v0.md` claim was not independently verified in this review (ADVISORY-05). The justification is plausible given the repo map commit history.

**Q10. Are there any blocker/major issues that should be patched before treating the helper as agent-reusable?**

No. There are no critical or major findings. MINOR-01 (`separately_admitted` lifecycle guard bypass via string `"none"`) is the highest-severity finding. It does not break the conservative skeleton output: `result_token_finalization: operator_review_required` and non-claims remain in force even for a bypass case. The bypass requires deliberate CLI misuse, not an accident or latent code path. Agent reuse under supervised operation is not blocked.

---

## Summary by Severity

| Severity | Count | Finding IDs |
| --- | --- | --- |
| Critical | 0 | — |
| Major | 0 | — |
| Minor | 1 | MINOR-01 |
| Advisory | 5 | ADVISORY-01, ADVISORY-02, ADVISORY-03, ADVISORY-04, ADVISORY-05 |

---

## Final Recommendation

**`accept_with_advisory_findings`**

The implementation correctly satisfies all ten implementation intent requirements. No fake-pass paths exist. The result-token semantics are sound. No code path can produce `mini_god_tier_met` or override `operator_review_required`. Archive.org metadata-only detection is correct and tested. The `separately_admitted` guard works for the primary Python API (`None` default) and has one minor CLI bypass path via string `"none"`. Docs coverage of non-claims is thorough and redundant. Import graph is acyclic. The direction-change propagation receipt is correctly formed with verified routing paths.

MINOR-01 is real and should be patched before wide-scale agent deployment where agents are expected to use the `separately_admitted` lifecycle state autonomously, but it does not block supervised agent-assisted use.

---

## Validation Commands Run by Reviewer

```powershell
# From orca-harness/ — SHA256 pin verification
python -c "[compute_hashes script]"
# Result: all 18 pins OK

# From orca-harness/ — focused test suite
python -m pytest -p no:cacheprovider tests/unit/test_source_quality_report_skeleton.py tests/contract/test_source_quality_report_skeleton_contract.py -v
# Result: 6 passed in 0.64s
```

The full 83-test source-capture stack and 151-test full suite were NOT re-run by this reviewer. Implementer-reported counts are taken as stated.

---

## Non-Claims

This review is not validation, not source completeness proof, not fixture admission, not Judgment scoring, not ECR or Cleaning output, not readiness certification, not acceptance, not deployment authorization, not source-access boundary amendment, and not a patch queue. Findings are advisory; the operator decides whether and when to close them. This review does not modify any source file.
