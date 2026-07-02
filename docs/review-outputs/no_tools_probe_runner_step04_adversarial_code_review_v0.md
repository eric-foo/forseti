---
artifact_id: no_tools_probe_runner_step04_adversarial_code_review_v0
artifact_role: Adversarial code review — no-tools memorization probe runner, STEP-04
created_at: 2026-06-01
review_mode: strict_formal_adversarial_code_review
output_mode: filesystem-output
status: completed
reviewed_by: claude-sonnet-4-6 via workflow-code-review + workflow-deep-thinking
commission: Does the implementation faithfully enforce the v0.14 no-tools execution contract without creating fake clean-pass paths, runtime/model-call side effects, participant-packet exposure paths, or overclaiming readiness?
recommendation: accept
source_context_status: SOURCE_CONTEXT_READY
authority_hashes_verified: true
---

# Adversarial Code Review: No-Tools Memorization Probe Runner STEP-04


```yaml
retrieval_header_version: 1
artifact_role: Adversarial code review report
scope: Adversarial code review of the no-tools memorization probe runner STEP-04 implementation.
use_when:
  - Auditing STEP-04 no-tools probe runner review findings.
  - Checking no-tools execution contract enforcement and fake-clean-pass risks.
authority_boundary: retrieval_only
```

## 1. Commission

**Central question:** Does the STEP-04 implementation faithfully enforce the v0.14 no-tools execution contract without creating fake clean-pass paths, runtime/model-call side effects, participant-packet exposure paths, or overclaiming readiness?

**Review stance:** Adversarial. Treated every gate path as a candidate for a fake clean pass or contract bypass until the code proved otherwise.

**Output mode:** `filesystem-output`

---

## 2. Target

| File | Role |
|---|---|
| `orca-harness/schemas/probe_models.py` | Probe schemas, enums, `derive_isolation_result`, `interpret_probe_gate`, `classify_probe_response` |
| `orca-harness/runners/run_memorization_probe.py` | Dry runner: receipt builder, CLI |
| `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py` | Contract test suite |

Local harness context read (hashes not pinned): `harness_utils.py`, `runners/run_case.py`, `tests/contract/test_no_llm_imports.py`, `tests/contract/test_runner_artifacts.py`, `pyproject.toml`, `schemas/case_models.py`, `README.md`.

---

## 3. Authority

| Source | Pinned hash | Match |
|---|---|---|
| `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md` | `E8B5F2E26B5E6E6186440E43450490BE1B550B850BAADC5B4B333C7F50F5E29F` | ✓ |
| `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md` | `7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61` | ✓ |
| `docs/review-outputs/adversarial-artifact-reviews/contestant_no_tools_execution_contract_post_patch_closure_blast_radius_check_v0.md` | `7FF0E5F91FA219D4E864EE6575EFAC70E852E5A89223D464376B45664F478D72` | ✓ |

Implementation target hashes:

| File | Pinned hash | Match |
|---|---|---|
| `orca-harness/schemas/probe_models.py` | `8FDBF0ED349A1A01E736B30433E57BAFFFCD0AC57273CAA1D0F4CECD81703F6D` | ✓ |
| `orca-harness/runners/run_memorization_probe.py` | `2AC939208D5D92F1E4A7D54B7AA2F96213D6EF65ED726DCA3674963D467A51BC` | ✓ |
| `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py` | `1403595F63EA64F0B7FD1FEB5CF3332FACC61AE9F0EE8A95F4218B93221B71A4` | ✓ |

All six pinned hashes verified before review began.

---

## 4. Source Context Declaration

`SOURCE_CONTEXT_READY`

All required sources are present at pinned hashes. The workspace is dirty (untracked files, staged modifications), but the review targets and authority sources are unmodified at the pinned revisions.

---

## 5. Review Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`. Overlay authority confirmed.
2. Reference-loaded `workflow-deep-thinking` and `workflow-code-review`. Neither applied yet.
3. SOURCE-LOADED all six pinned sources. SHA256 hashes computed and verified.
4. SOURCE-LOADED local harness context (`harness_utils.py`, `run_case.py`, `test_no_llm_imports.py`, `test_runner_artifacts.py`, `pyproject.toml`, `schemas/case_models.py`, `README.md`).
5. Applied `workflow-deep-thinking` to enumerate all failure modes before inspecting individual findings (see §7).
6. Applied `workflow-code-review` in adversarial stance: inspected every gate branch against the contract, traced all 9 permutations of `(ProbeResult × IsolationResult)`, traced all VIOLATED trigger conditions, inspected CLI boundary, checked no-LLM-import guard, checked participant-packet exposure, inspected schema cross-validators.
7. Wrote this durable report.

---

## 6. Deep-Thinking: Failure Mode Frame

*Applied before inspecting individual functions.*

The following failure modes were treated as adversarial candidates:

| # | Failure mode | Source of risk |
|---|---|---|
| FM-1 | A code path produces `PASS_VALID` without `probe_result == pass AND isolation_result == proven` | `interpret_probe_gate` branch logic |
| FM-2 | `not_applicable` admitted for non-raw-API surfaces, inflating isolation to PROVEN | Model validator scope check |
| FM-3 | `derive_isolation_result` returns PROVEN without checking all required contract conditions | Missing condition in PROVEN block |
| FM-4 | VIOLATED conditions not comprehensive — some tool-availability signals skip the VIOLATED branch | Missing OR clauses in VIOLATED check |
| FM-5 | Runner loads participant packet, provider SDK, or network | Import scan, runner function signature |
| FM-6 | CLI defaults or output messaging imply live model execution | `--description` text, default values, stdout |
| FM-7 | Schema validators weak enough that contradictory isolation receipts can be constructed | Cross-field validator coverage |
| FM-8 | New runner breaks the existing no-LLM-import guard | `test_no_llm_imports` scan target list |
| FM-9 | New code contaminates scoring/report deterministic paths | Import dependencies, function signatures |

Each FM is addressed in §7 (findings) or §8 (passed surfaces).

---

## 7. Findings

Ordered by severity. No critical or major findings were found.

---

### R-01 — Minor

**id:** `R-01`  
**severity:** `minor`  
**file:** `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py`  
**line_or_section:** absent (missing test)  
**finding:** No test for `probe_result == FAIL AND isolation_result == NOT_PROVEN → FAIL_GATE_CLOSING_WITH_CAVEAT`.

The contract defines this as a distinct outcome with a specific claim boundary:
> "must not be cited as proof of training-data memorization specifically"

The test suite exercises `PASS + NOT_PROVEN → INVALID_FOR_CLEAN_PASS` (test 1), `TOOLS_AVAILABLE → VIOLATED` (test 3), `AGENT_HARNESS + UNAVAILABLE → NOT_PROVEN` (test 4), and `RAW_API + PROVEN → PASS_VALID` (test 6). None of them assert `FAIL_GATE_CLOSING_WITH_CAVEAT`. If `interpret_probe_gate` line 209 were accidentally changed or the `FAIL + NOT_PROVEN` branch removed, no test would fail.

**why_it_matters:** The `FAIL_GATE_CLOSING_WITH_CAVEAT` state carries the causal-proof caveat established in the AR-03 patch closure. A regression that collapses it into `FAIL_GATE_CLOSING` would silently remove that boundary, allowing a fail result under unproven isolation to be treated as positive memorization evidence — a contract-semantic regression, not a fake clean pass.

**minimum_closure_condition:** A test that constructs `isolation_result = NOT_PROVEN` + `probe_result = FAIL` and asserts `gate_interpretation == FAIL_GATE_CLOSING_WITH_CAVEAT`.

**next_authorized_action:** Advisory only. Executor-ready patch queue is not authorized by this lane.

---

### R-02 — Minor

**id:** `R-02`  
**severity:** `minor`  
**file:** `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py`  
**line_or_section:** absent (missing test)  
**finding:** No test for `probe_result == AMBIGUOUS AND isolation_result == NOT_PROVEN → INVALID_FOR_CLEAN_PASS`.

`interpret_probe_gate` (line 211) uses `probe_result in {ProbeResult.PASS, ProbeResult.AMBIGUOUS}`. The test for `PASS + NOT_PROVEN → INVALID_FOR_CLEAN_PASS` (test 1) exercises only the PASS member of that set. If the set were narrowed to `{ProbeResult.PASS}`, the existing tests would still pass, but `AMBIGUOUS + NOT_PROVEN` would fall through to `AMBIGUOUS_QUARANTINE` — a different (and still conservative) state, but a silent deviation from the contract table.

**why_it_matters:** The `invalid_for_clean_pass` state blocks reruns unless structural isolation evidence is provided. `AMBIGUOUS_QUARANTINE` is also conservative, but the semantics differ (quarantine does not explicitly name "rerun under separate authorization" as the resolution path). Test coverage should distinguish the two routes.

**minimum_closure_condition:** A test that constructs `probe_result = AMBIGUOUS` + `isolation_result = NOT_PROVEN` and asserts `gate_interpretation == INVALID_FOR_CLEAN_PASS`.

**next_authorized_action:** Advisory only.

---

### R-03 — Minor

**id:** `R-03`  
**severity:** `minor`  
**file:** `orca-harness/schemas/probe_models.py`  
**line_or_section:** `derive_isolation_result`, lines 165–196  
**finding:** `derive_isolation_result` does not check `hidden_context_boundary` as a condition for returning `PROVEN`, despite the contract listing "hidden_context_boundary is recorded" as a required PROVEN condition.

The contract (§ Isolation Result Semantics):
```yaml
proven:
  required_conditions:
    ...
    - hidden_context_boundary is recorded
```

The implementation enforces non-empty `hidden_context_boundary` only via the `reject_blank_evidence` field validator on `ContestantExecutionIsolation` (line 104–109). Since `derive_isolation_result` is also called on a `SimpleNamespace` from `build_isolation_evidence` (before Pydantic validation), it can return `PROVEN` for a `SimpleNamespace` with `hidden_context_boundary = ""` if all other PROVEN conditions are met.

**why_it_matters:** In practice this produces no fake clean pass: `build_isolation_evidence` immediately constructs `ContestantExecutionIsolation`, which rejects the empty field. However, `derive_isolation_result` is a module-level function callable directly on any namespace. An operator calling it independently (e.g. in a script, REPL, or notebook) would get `PROVEN` back while the contract requires a recorded boundary. If that result were used without going through the Pydantic model, the gate protection would be absent. The architectural pattern creates an implicit precondition on the function that is not enforced at the function boundary.

**minimum_closure_condition:** Either: (a) `derive_isolation_result` adds an explicit check that `hidden_context_boundary` is non-empty before returning `PROVEN`; or (b) the function is made private and callers are restricted to the Pydantic model path where the validator fires first.

**next_authorized_action:** Advisory only.

---

### R-04 — Minor

**id:** `R-04`  
**severity:** `minor`  
**file:** `orca-harness/schemas/probe_models.py`  
**line_or_section:** `ContestantExecutionIsolation`, no model_validator for this combination  
**finding:** No cross-field validator prevents `tool_config_evidence_kind = EMPTY_TOOL_TRACE` combined with `tool_call_trace_status = NOT_APPLICABLE`, producing a semantically contradictory receipt.

`EMPTY_TOOL_TRACE` as `tool_config_evidence_kind` means "my evidence is that a tool-call trace exists and shows no calls." `NOT_APPLICABLE` as `tool_call_trace_status` means "tool traces cannot exist for this execution surface." These two values are mutually exclusive in meaning. However, both satisfy their respective conditions in `derive_isolation_result`: `EMPTY_TOOL_TRACE` is in `proof_grade_evidence`, and `NOT_APPLICABLE` is in `trace_can_prove`. Combined with `RAW_API_NO_TOOLS`, all other PROVEN conditions, this produces `PROVEN` with a receipt that claims "evidence from an empty tool trace" when the trace is structurally inapplicable.

**why_it_matters:** This does not create a fake clean pass — PROVEN is the correct gate result for RAW_API_NO_TOOLS with fully-disabled tools. The harm is receipt quality: an operator or downstream audit reading the artifact would see contradictory fields, reducing receipt trustworthiness as an audit record. The post-patch closure blast-radius check (AR-01) specifically emphasizes structural evidence over operator assertion. A contradictory receipt undermines that.

**minimum_closure_condition:** A model validator that rejects `tool_config_evidence_kind == EMPTY_TOOL_TRACE` when `tool_call_trace_status == NOT_APPLICABLE`, and vice versa.

**next_authorized_action:** Advisory only.

---

### R-05 — Optional

**id:** `R-05`  
**severity:** `optional`  
**file:** `orca-harness/tests/contract/test_no_llm_imports.py`  
**line_or_section:** lines 11–14, `target_paths` construction  
**finding:** `schemas/` directory is not included in the `test_no_llm_imports_in_scoring_and_reports` scan.

The scan covers `scoring/*.py`, `reports/*.py`, `runners/*.py`, and `harness_utils.py`. The new `schemas/probe_models.py` is in `runners/`? No — it is in `schemas/`, which is excluded. Current `probe_models.py` contains no forbidden imports. But as the schema layer grows (e.g. adding SDK-backed validators), the guard would not fire.

**why_it_matters:** Pre-existing gap, not introduced by STEP-04. The STEP-04 runner itself (`runners/run_memorization_probe.py`) is scanned and clean. The risk is future additions to `schemas/` going unguarded. Noted here because STEP-04 added the first schema file with significant business logic (pure functions, not just model definitions), making the gap more material than before.

**minimum_closure_condition:** Add `list((project_root / "schemas").glob("*.py"))` to `target_paths`.

**next_authorized_action:** Advisory only.

---

### R-06 — Optional

**id:** `R-06`  
**severity:** `optional`  
**file:** `orca-harness/schemas/probe_models.py`  
**line_or_section:** `interpret_probe_gate`, lines 199–213; `GateInterpretation` enum, line 56  
**finding:** `AMBIGUOUS_QUARANTINE` as a `GateInterpretation` value is not explicitly named in the contract's `probe_gate_interpretation` table. It is derived from the protocol's `if_ambiguous` case-handling (`quarantine_until_operator_review_or_clean_isolation_rerun`) but is treated as a gate-level enum, creating a gap between the docs contract and the code.

The gate table defines five states: `pass_valid`, `fail_gate_closing`, `fail_gate_closing_with_caveat`, `invalid_for_clean_pass`, `execution_invalid_tool_violation`. The implementation adds a sixth (`AMBIGUOUS_QUARANTINE`) for `AMBIGUOUS + PROVEN`, which is not explicitly in the gate table. The behavior is correct (not a clean pass), but the docs contract and the code are not 1:1.

**why_it_matters:** Operators reading the contract and comparing it to the code would see an undocumented enum value, which could create confusion about whether `AMBIGUOUS_QUARANTINE` is authoritative or a placeholder. Also, the `AMBIGUOUS_QUARANTINE` branch acts as the catch-all fallthrough — if a future `ProbeResult` or `IsolationResult` enum value were added without updating `interpret_probe_gate`, it would silently produce `AMBIGUOUS_QUARANTINE` instead of a visible error.

**minimum_closure_condition:** Either: (a) add `AMBIGUOUS + PROVEN → AMBIGUOUS_QUARANTINE` to the contract's gate interpretation table; or (b) add an explicit branch for `AMBIGUOUS + PROVEN` and make the fallthrough an `AssertionError` or similar guard.

**next_authorized_action:** Advisory only.

---

## 8. Non-Findings / Passed Surfaces

### 8.1 Contract Fidelity: Clean Pass Requires Both Conditions

`interpret_probe_gate` (lines 199–213): The only code path that returns `PASS_VALID` is:

```python
if probe_result == ProbeResult.PASS and isolation_result == IsolationResult.PROVEN:
    return GateInterpretation.PASS_VALID
```

This branch is guarded by the VIOLATED check first. All other combinations are routed to non-pass states. Enumeration of all 9 permutations:

| probe_result | isolation_result | Gate interpretation | Contract-correct |
|---|---|---|---|
| PASS | PROVEN | PASS_VALID | ✓ |
| PASS | NOT_PROVEN | INVALID_FOR_CLEAN_PASS | ✓ |
| PASS | VIOLATED | EXECUTION_INVALID_TOOL_VIOLATION | ✓ |
| FAIL | PROVEN | FAIL_GATE_CLOSING | ✓ |
| FAIL | NOT_PROVEN | FAIL_GATE_CLOSING_WITH_CAVEAT | ✓ |
| FAIL | VIOLATED | EXECUTION_INVALID_TOOL_VIOLATION | ✓ |
| AMBIGUOUS | PROVEN | AMBIGUOUS_QUARANTINE (fallthrough) | ✓ (conservative) |
| AMBIGUOUS | NOT_PROVEN | INVALID_FOR_CLEAN_PASS | ✓ |
| AMBIGUOUS | VIOLATED | EXECUTION_INVALID_TOOL_VIOLATION | ✓ |

No fake clean pass path exists.

### 8.2 VIOLATED Conditions Are Comprehensive

`derive_isolation_result` (lines 165–196): Three independently sufficient VIOLATED conditions:
1. `tool_access_policy == TOOLS_AVAILABLE` — covers policy-level tool availability regardless of trace.
2. `tool_call_trace_status == NON_EMPTY_TRACE` — covers trace-level evidence of tool use regardless of policy.
3. `any(value is False for value in disabled_fields)` — covers any affirmatively-unblocked retrieval surface.

Using `is False` (identity, not equality) correctly handles `BooleanOrUnknown = bool | Literal["unknown"]`: `"unknown" is False` is `False`; `False is False` is `True`. No coercion gap.

### 8.3 `not_applicable` Restriction Enforced

`ContestantExecutionIsolation.validate_trace_status_and_result` (lines 111–126): Model validator explicitly raises `ValueError` if `tool_call_trace_status == NOT_APPLICABLE AND execution_surface != RAW_API_NO_TOOLS`. This aligns precisely with the contract's structural not-applicable rule (AR-01 closure). Test 5 (`test_not_applicable_trace_status_is_rejected_for_agent_harnesses`) confirms this path.

### 8.4 Isolation Result Is Deterministic and Validated

`ContestantExecutionIsolation.validate_trace_status_and_result` also calls `derive_isolation_result(self)` and rejects any `isolation_result` that doesn't match the computed value. `MemorizationProbeArtifact.validate_gate_interpretation` does the same for `gate_interpretation`. Neither field can be manually set to a favorable value: Pydantic will recompute and reject the mismatch.

### 8.5 PROVEN Conditions Match the Contract

`derive_isolation_result` PROVEN branch requires simultaneously:
- `tool_access_policy == NO_TOOLS` (not TOOLS_AVAILABLE, not UNKNOWN)
- `tool_config_evidence_kind in {STRUCTURAL_CONFIG, PROVIDER_TRACE, EMPTY_TOOL_TRACE}` (excludes PROMPT_INSTRUCTION_ONLY, OPERATOR_ASSERTION_ONLY, UNKNOWN — the contract's "insufficient evidence" list)
- `tool_call_trace_status in {EMPTY_TRACE, NOT_APPLICABLE}`
- All four disabled fields `is True`

`PROMPT_INSTRUCTION_ONLY` and `OPERATOR_ASSERTION_ONLY` evidence kinds cannot produce PROVEN. This directly implements the contract's §Insufficient Evidence list.

### 8.6 `non_claim_notice` Enforcement

`MemorizationProbeArtifact.validate_non_claim_notice` (lines 145–149): The `non_claim_notice` field defaults to `NON_CLAIM_NOTICE = "plumbing works only; not judgment quality"` and cannot be overridden — any other value fails validation. Every written artifact carries the required claim boundary.

### 8.7 Runner Boundary: Dry and Local Only

`run_memorization_probe.py` imports: `argparse`, `pathlib`, `types.SimpleNamespace`, `sys`, `yaml`, `harness_utils`, `schemas.probe_models`. The `harness_utils` module imports: `hashlib`, `secrets`, `time`, `datetime`, `enum`, `pathlib`, `typing`, `yaml`. No provider SDK, no HTTP library, no browser, no search, no `openai`/`anthropic`/`litellm`/`langchain`.

`run_memorization_probe_dry` signature:
```python
def run_memorization_probe_dry(
    *, probe_input_path, raw_response_path, output_path, isolation, ...
)
```

No `participant_packet_path`, no case directory, no ledger, no provider credential. The probe input (`ProbeInput`) contains public identifiers only — no participant-packet fields (`role_frame`, `authority_constraints`, `forbidden_information_notice`, `source_manifest`, etc.).

### 8.8 No-LLM-Import Guard Covers the New Runner

`test_no_llm_imports_in_scoring_and_reports` (test_no_llm_imports.py, line 11–14) scans `runners/*.py`, which includes `run_memorization_probe.py`. The new runner passes this guard. Note: `schemas/` is excluded (see R-05).

### 8.9 No Contamination of Scoring/Report Paths

`run_memorization_probe.py` does not import from `scoring/`, `reports/`, `schemas/case_models.py` (for `FacilitatorLedger`, `BlindJudgement`, etc.), or `runners/run_case.py`. No shared mutable state. No writes to `scores/`, `reports/`, or `memory/logs/`. The runner writes only to the caller-supplied `output_path`.

### 8.10 CLI Defaults Do Not Create a Fake Clean Pass

CLI defaults: `--tool-access-policy unknown`, `--tool-config-evidence-kind operator_assertion_only`, `--tool-call-trace-status unavailable`, all disabled fields `"unknown"`. These defaults produce `isolation_result = NOT_PROVEN` and `gate_interpretation = INVALID_FOR_CLEAN_PASS` (for a PASS probe) or `FAIL_GATE_CLOSING_WITH_CAVEAT` (for a FAIL probe). No default combination produces `PASS_VALID`.

### 8.11 CLI Output Surfaces Gate Interpretation

```python
print(f"probe_result={artifact.probe_result.value}")
print(f"isolation_result={artifact.contestant_execution_isolation.isolation_result.value}")
print(f"gate_interpretation={artifact.gate_interpretation.value}")
```

Even when `probe_result = pass`, the `gate_interpretation = invalid_for_clean_pass` is explicitly printed. Operators cannot mistake a raw behavioral pass for a gate-clearing result without looking away from the CLI output.

### 8.12 `classify_probe_response` Matches the Contract

FAIL condition: `recognized AND claimed_outcome != None AND confidence >= 0.5`. PASS condition: `unknown OR claimed_outcome is None`. Remainder: AMBIGUOUS. This matches the protocol's three-way evaluation rule. The edge case of `recognized + None claimed_outcome → PASS` is spec-conformant: the protocol's PASS condition includes "claimed_outcome is empty/generic/incorrect."

### 8.13 StrictModel: `extra = "forbid"`

`schemas/case_models.py`: `StrictModel` uses `ConfigDict(extra="forbid", populate_by_name=True)`. Extra fields are rejected at construction time. No `strict=True` (type coercion is allowed), but CLI input conversion (`_parse_bool_or_unknown`) ensures native Python `bool`/`str` reach Pydantic, not ambiguous integers.

### 8.14 Existing Harness Tests: No Regression Signal

The commission references `41 passed in 4.29s` for the full suite. The new runner's imports and public API are additive only. `run_case.py` does not import `run_memorization_probe.py`. `test_runner_artifacts.py` tests do not interact with the probe runner. No import cycle, no shared state mutation.

---

## 9. Residual Risks

These are not findings but warrant operator awareness:

**RR-1: `derive_isolation_result` callable outside Pydantic paths.** The function is module-level and accepts any object with the right attributes. As noted in R-03, a `SimpleNamespace` with empty `hidden_context_boundary` can produce `PROVEN` in isolation. The current codebase does not exploit this, but future scripting against this function without Pydantic wrapping would bypass the boundary check.

**RR-2: No upper bound on `output_path` write location.** `run_memorization_probe_dry` accepts any operator-supplied `output_path`. No path-containment validation. For a local harness tool this is acceptable, but if the runner is ever exposed to an automated pipeline with untrusted inputs, arbitrary write paths are possible.

**RR-3: `schemas/` LLM import coverage gap** (see R-05). Currently `probe_models.py` has no forbidden imports. The risk materializes only if the schema layer grows new LLM integrations unnoticed.

**RR-4: `AMBIGUOUS_QUARANTINE` as silent fallthrough** (see R-06). Until the fallthrough is made an explicit error, newly added enum values in `ProbeResult` or `IsolationResult` would silently route to AMBIGUOUS_QUARANTINE. An explicit guard would surface the gap immediately.

**RR-5: No test for the PROVEN gate path triggering a PASS_VALID result via the `EMPTY_TRACE` (not `NOT_APPLICABLE`) trace path.** Test 6 covers `NOT_APPLICABLE + RAW_API → PASS_VALID`. There is no test for `EMPTY_TRACE + AGENT_HARNESS + STRUCTURAL_CONFIG → PROVEN → PASS_VALID`. This is not an execution-surface gap (the gate works correctly regardless), but the "happy path for actual agent runs" has no test coverage.

---

## 10. Recommendation

**`accept`**

No critical or major findings. The gate logic correctly enforces the contract's dual requirement (`probe_result == pass AND isolation_result == proven`) for clean pass. The VIOLATED conditions are comprehensive. The runner boundary is dry and local. The participant-packet exposure surface is absent. The no-LLM-import guard covers the new runner. The schema's cross-model validators prevent tampered `isolation_result` or `gate_interpretation` fields from surviving construction.

The five minor/optional findings are test coverage gaps and receipt-consistency issues. None creates a fake clean pass, enables live model calls, exposes participant packets, or irreversibly corrupts gate state. They represent hardening work that would reduce regression risk and improve receipt auditability but are not blocking for the current STEP-04 scope.

---

## 11. Non-Claims

- No live probe was run.
- No model or provider call was made.
- No participant packet was loaded or exposed.
- No scoring was performed.
- No ledger freeze was performed.
- No schema or runtime readiness claim is made.
- No validation, fixture admission, product proof, or judgment-quality proof is claimed.
- This review does not authorize probe execution, blind judgment runs, fixture admission, or gate clearing.
- This review does not prove that a real probe with these defaults will produce correct isolation under live execution conditions; it proves only that the plumbing logic correctly derives and enforces gate states from supplied evidence fields.

plumbing works only; not judgment quality.
