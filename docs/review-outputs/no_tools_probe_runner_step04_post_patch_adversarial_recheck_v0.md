---
artifact_id: no_tools_probe_runner_step04_post_patch_adversarial_recheck_v0
artifact_role: Bounded post-patch adversarial recheck — no-tools probe runner STEP-04
created_at: 2026-06-01
review_mode: bounded_post_patch_adversarial_recheck
output_mode: filesystem-output
status: completed
reviewed_by: claude-sonnet-4-6 via workflow-deep-thinking + workflow-code-review (bounded recheck mode)
commission: Did the patch close R-01 through R-06? Did the patch introduce any new critical or major regression inside the touched patch scope?
recommendation: accept
source_context_status: SOURCE_CONTEXT_READY
authority_hashes_verified: true
---

# Bounded Post-Patch Adversarial Recheck: No-Tools Probe Runner STEP-04


```yaml
retrieval_header_version: 1
artifact_role: Post-patch adversarial recheck report
scope: Post-patch adversarial recheck for no-tools probe runner STEP-04 findings R-01 through R-06.
use_when:
  - Checking closure of STEP-04 no-tools probe runner findings.
  - Auditing touched-scope regression scan after the STEP-04 patch.
authority_boundary: retrieval_only
```

## 1. Commission

**Central questions:**
1. Did the patch close prior findings R-01 through R-06 from `no_tools_probe_runner_step04_adversarial_code_review_v0.md`?
2. Did the patch introduce any new critical or major regression inside the touched patch scope?

**Review stance:** Adversarial recheck. Each claimed closure was traced against the contract and the actual code. Each touched code path was re-examined for regression against the gate-safety invariants.

**Out of scope:** Design questions, optional hardening, model execution, provider access, fixture quality, scoring, product proof, and findings unrelated to the patch scope.

**Output mode:** `filesystem-output`

---

## 2. Target

| File | Role | Changed by patch |
|---|---|---|
| `orca-harness/schemas/probe_models.py` | Probe schemas, enums, `derive_isolation_result`, `interpret_probe_gate`, `classify_probe_response` | Yes |
| `orca-harness/runners/run_memorization_probe.py` | Dry runner: receipt builder, CLI | No — hash unchanged |
| `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py` | Contract test suite | Yes |
| `orca-harness/tests/contract/test_no_llm_imports.py` | No-LLM-import guard | Yes |

---

## 3. Authority

| Source | Prior review pinned hash | Observed hash | Match |
|---|---|---|---|
| `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md` | `E8B5F2E26B5E6E6186440E43450490BE1B550B850BAADC5B4B333C7F50F5E29F` | `E8B5F2E26B5E6E6186440E43450490BE1B550B850BAADC5B4B333C7F50F5E29F` | ✓ |
| `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md` | `7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61` | `7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61` | ✓ |
| `docs/review-outputs/adversarial-artifact-reviews/contestant_no_tools_execution_contract_post_patch_closure_blast_radius_check_v0.md` | `7FF0E5F91FA219D4E864EE6575EFAC70E852E5A89223D464376B45664F478D72` | `7FF0E5F91FA219D4E864EE6575EFAC70E852E5A89223D464376B45664F478D72` | ✓ |

Authority sources are unchanged from the prior review. Contract semantics are identical to what the prior review assessed.

---

## 4. Source Context and Hash Verification

**Prior review:**

| File | Pinned hash | Observed hash | Match |
|---|---|---|---|
| `docs/review-outputs/no_tools_probe_runner_step04_adversarial_code_review_v0.md` | `9B7711806ED3A52592D928708AA8C531E91EA642CE0B789A53DFB6807B48B3BD` | `9B7711806ED3A52592D928708AA8C531E91EA642CE0B789A53DFB6807B48B3BD` | ✓ |

**Patched implementation targets:**

| File | Pinned hash | Observed hash | Match |
|---|---|---|---|
| `orca-harness/schemas/probe_models.py` | `A2277955037BFB43C2D2586226337AF44DEC4EAEEF594B10F7CFB5C10FBDA6F1` | `A2277955037BFB43C2D2586226337AF44DEC4EAEEF594B10F7CFB5C10FBDA6F1` | ✓ |
| `orca-harness/runners/run_memorization_probe.py` | `2AC939208D5D92F1E4A7D54B7AA2F96213D6EF65ED726DCA3674963D467A51BC` | `2AC939208D5D92F1E4A7D54B7AA2F96213D6EF65ED726DCA3674963D467A51BC` | ✓ |
| `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py` | `DB9E96C355A4D00B673510123D267E649696263E245C4E2ACE044ACE34DEA845` | `DB9E96C355A4D00B673510123D267E649696263E245C4E2ACE044ACE34DEA845` | ✓ |
| `orca-harness/tests/contract/test_no_llm_imports.py` | `1F2D74C020E8F5FD537F690242105EE41A8CC571A646CB4634D5EDA9ACD83A1C` | `1F2D74C020E8F5FD537F690242105EE41A8CC571A646CB4634D5EDA9ACD83A1C` | ✓ |

All eight required hashes verified. Workspace is dirty (untracked files, staged modifications), but all review targets and authority sources are at their pinned revisions.

`SOURCE_CONTEXT_READY`

---

## 5. Closure Table

| Finding | Prior severity | Patch claim | Closure verdict | Basis |
|---|---|---|---|---|
| R-01 | minor | Added `FAIL + NOT_PROVEN → FAIL_GATE_CLOSING_WITH_CAVEAT` test | **closed** | See §6.1 |
| R-02 | minor | Added `AMBIGUOUS + NOT_PROVEN → INVALID_FOR_CLEAN_PASS` test | **closed** | See §6.2 |
| R-03 | minor | Added `hidden_context_boundary` non-empty check to `derive_isolation_result` | **closed** | See §6.3 |
| R-04 | minor | Added validator rejecting `EMPTY_TOOL_TRACE` with non-`EMPTY_TRACE` status | **closed** | See §6.4 |
| R-05 | optional | Added `schemas/*.py` to `test_no_llm_imports` target paths | **closed** | See §6.5 |
| R-06 | optional | Made `AMBIGUOUS + PROVEN → AMBIGUOUS_QUARANTINE` explicit; replaced fallthrough with `ValueError` | **closed** | See §6.6 |

---

## 6. Finding-by-Finding Closure Analysis

### 6.1 R-01 — `FAIL + NOT_PROVEN → FAIL_GATE_CLOSING_WITH_CAVEAT`

**Prior minimum closure condition:** A test constructing `isolation_result = NOT_PROVEN` + `probe_result = FAIL` and asserting `gate_interpretation == FAIL_GATE_CLOSING_WITH_CAVEAT`.

**Patch:** Added `test_probe_fail_with_unproven_isolation_is_gate_closing_with_caveat` (lines 104–130, `test_memorization_probe_no_tools_contract.py`).

**Traced execution:**
- Isolation: `STRUCTURAL_CONFIG` + `UNAVAILABLE` trace. `UNAVAILABLE` is not in `trace_can_prove` (`{EMPTY_TRACE, NOT_APPLICABLE}`), so PROVEN branch is not reached. Result: `NOT_PROVEN`. ✓
- Response: `recognized`, confidence 0.9. `classify_probe_response`: recognition_status == "recognized" AND confidence >= 0.5 → `FAIL`. ✓
- Gate: `interpret_probe_gate(FAIL, NOT_PROVEN)` → fourth explicit branch → `FAIL_GATE_CLOSING_WITH_CAVEAT`. ✓

Test assertions pass. The closure condition is satisfied precisely.

**Verdict: closed.**

---

### 6.2 R-02 — `AMBIGUOUS + NOT_PROVEN → INVALID_FOR_CLEAN_PASS`

**Prior minimum closure condition:** A test constructing `probe_result = AMBIGUOUS` + `isolation_result = NOT_PROVEN` and asserting `gate_interpretation == INVALID_FOR_CLEAN_PASS`.

**Patch:** Added `test_probe_ambiguous_with_unproven_isolation_cannot_clear_gate` (lines 133–165, `test_memorization_probe_no_tools_contract.py`).

**Traced execution:**
- Isolation: same `STRUCTURAL_CONFIG` + `UNAVAILABLE` construction → `NOT_PROVEN`. ✓
- Response: `partial`, confidence 0.4. `classify_probe_response`: not "unknown", not `claimed_outcome is None`, not ("recognized" AND confidence ≥ 0.5) → `AMBIGUOUS`. ✓
- Gate: `interpret_probe_gate(AMBIGUOUS, NOT_PROVEN)` → fifth branch (`probe_result in {PASS, AMBIGUOUS}` AND `NOT_PROVEN`) → `INVALID_FOR_CLEAN_PASS`. ✓

This test specifically verifies the AMBIGUOUS member of the set, not duplicating the PASS-member test already present. The semantic distinction from R-02's finding (AMBIGUOUS + NOT_PROVEN → INVALID vs AMBIGUOUS_QUARANTINE) is correctly demonstrated.

**Verdict: closed.**

---

### 6.3 R-03 — `derive_isolation_result` not checking `hidden_context_boundary` as a PROVEN condition

**Prior minimum closure condition:** Either (a) `derive_isolation_result` adds an explicit check that `hidden_context_boundary` is non-empty before returning PROVEN, or (b) the function is made private and restricted to the Pydantic path.

**Patch:** Added `and bool(str(evidence.hidden_context_boundary).strip())` to the PROVEN branch condition (line 199, `probe_models.py`).

**Traced behavior:**
- Old code: a namespace with empty `hidden_context_boundary` satisfying all other PROVEN conditions returned `PROVEN`.
- New code: the same namespace returns `NOT_PROVEN`.

**Test:** `test_hidden_context_boundary_is_required_for_proven_isolation` (lines 283–294) constructs a plain Python class with `hidden_context_boundary = ""` and all other PROVEN conditions satisfied. Calls `derive_isolation_result` directly and asserts `NOT_PROVEN`. Test passes. ✓

**Pydantic path unchanged:** `ContestantExecutionIsolation.reject_blank_evidence` still rejects empty `hidden_context_boundary` at the field level before `validate_trace_status_and_result` fires. For well-formed Pydantic model instances, the new condition has no behavioral effect (boundary is always non-empty). The patch closes the raw-namespace call path, which is the R-03 exposure.

**Verdict: closed** (via option a).

---

### 6.4 R-04 — No cross-validator preventing `EMPTY_TOOL_TRACE` + `NOT_APPLICABLE`

**Prior minimum closure condition:** A model validator rejecting `tool_config_evidence_kind == EMPTY_TOOL_TRACE` when `tool_call_trace_status == NOT_APPLICABLE` (or vice versa).

**Patch:** Added a second check inside `validate_trace_status_and_result` (lines 121–125, `probe_models.py`):
```python
if (
    self.tool_config_evidence_kind == ToolConfigEvidenceKind.EMPTY_TOOL_TRACE
    and self.tool_call_trace_status != ToolCallTraceStatus.EMPTY_TRACE
):
    raise ValueError("empty tool-trace evidence requires tool_call_trace_status empty_trace")
```

**Scope of the new validator:** Rejects `EMPTY_TOOL_TRACE` evidence combined with any trace status other than `EMPTY_TRACE`. This covers:
- `EMPTY_TOOL_TRACE + NOT_APPLICABLE` — the R-04 case directly. ✓
- `EMPTY_TOOL_TRACE + UNAVAILABLE` — also blocked (claiming an empty trace as evidence while saying no trace was captured is equally contradictory). ✓
- `EMPTY_TOOL_TRACE + NON_EMPTY_TRACE` — also blocked (this would also be caught by the VIOLATED branch, but the earlier validator error is cleaner). ✓

**Test:** `test_empty_tool_trace_evidence_requires_empty_trace_status` (lines 240–254) constructs `EMPTY_TOOL_TRACE + NOT_APPLICABLE` on `RAW_API_NO_TOOLS` (the case not caught by the first NOT_APPLICABLE check) and asserts `ValidationError` with the correct message. Test passes. ✓

**Verdict: closed.**

---

### 6.5 R-05 — `schemas/` excluded from `test_no_llm_imports` scan

**Prior minimum closure condition:** Add `list((project_root / "schemas").glob("*.py"))` to `target_paths`.

**Patch:** Line 16 of `test_no_llm_imports.py` now reads:
```python
+ list((project_root / "schemas").glob("*.py"))
```

The test still passes, confirming `probe_models.py` (and any other `schemas/*.py` files) contain no forbidden imports. The scan is now materially broader.

**Verdict: closed.**

---

### 6.6 R-06 — `AMBIGUOUS_QUARANTINE` not in contract table; silent fallthrough

**Prior minimum closure condition:** Either (a) add `AMBIGUOUS + PROVEN → AMBIGUOUS_QUARANTINE` to the contract's gate interpretation table, or (b) add an explicit branch for `AMBIGUOUS + PROVEN` and make the fallthrough an `AssertionError` or similar guard.

**Patch:** Chose option (b). `interpret_probe_gate` now has:
```python
if probe_result == ProbeResult.AMBIGUOUS and isolation_result == IsolationResult.PROVEN:
    return GateInterpretation.AMBIGUOUS_QUARANTINE
raise ValueError(f"Unhandled probe gate combination: {probe_result.value}/{isolation_result.value}")
```

The six explicit branches now cover all 9 permutations of `(ProbeResult × IsolationResult)` (see §7.1 verification). The `ValueError` fires only for genuinely unhandled combinations — i.e., if a future enum value is added without updating this function.

**Test:** `test_ambiguous_with_proven_isolation_routes_to_quarantine_explicitly` (lines 297–301) calls `interpret_probe_gate(AMBIGUOUS, PROVEN)` directly and asserts `AMBIGUOUS_QUARANTINE`. Test passes. ✓

The prior finding noted the minimum closure condition included option (b). The patch satisfies it.

**Verdict: closed.**

---

## 7. Patch-Caused Critical/Major Regression Check

### 7.1 No-Fake-Clean-Pass Semantics

**Enumeration of all 9 `(ProbeResult × IsolationResult)` gate paths post-patch:**

| probe_result | isolation_result | Gate result | Contract-correct |
|---|---|---|---|
| PASS | PROVEN | PASS_VALID | ✓ |
| PASS | NOT_PROVEN | INVALID_FOR_CLEAN_PASS | ✓ |
| PASS | VIOLATED | EXECUTION_INVALID_TOOL_VIOLATION (first branch) | ✓ |
| FAIL | PROVEN | FAIL_GATE_CLOSING | ✓ |
| FAIL | NOT_PROVEN | FAIL_GATE_CLOSING_WITH_CAVEAT | ✓ |
| FAIL | VIOLATED | EXECUTION_INVALID_TOOL_VIOLATION (first branch) | ✓ |
| AMBIGUOUS | PROVEN | AMBIGUOUS_QUARANTINE (now explicit) | ✓ |
| AMBIGUOUS | NOT_PROVEN | INVALID_FOR_CLEAN_PASS | ✓ |
| AMBIGUOUS | VIOLATED | EXECUTION_INVALID_TOOL_VIOLATION (first branch) | ✓ |

The only path to `PASS_VALID` remains `PASS + PROVEN`. No new path to `PASS_VALID` was introduced by the patch. The `ValueError` terminates any combination not covered by the six explicit branches.

**No critical or major regression here.**

### 7.2 `not_applicable` / `unavailable` Tool Trace Semantics

The `NOT_APPLICABLE` restriction (`not_applicable is valid only for raw_api_no_tools`) is unchanged. The new `EMPTY_TOOL_TRACE` validator fires sequentially after the `NOT_APPLICABLE` check in the same model validator method. Execution order:

1. Check `NOT_APPLICABLE` + non-RAW_API surface → raise if true.
2. Check `EMPTY_TOOL_TRACE` + non-`EMPTY_TRACE` status → raise if true.
3. Compute and verify `isolation_result`.

Step 2 correctly catches the one case step 1 misses: `EMPTY_TOOL_TRACE + NOT_APPLICABLE` on `RAW_API_NO_TOOLS` surface (step 1 passes because it is RAW_API, but step 2 catches it because EMPTY_TOOL_TRACE evidence requires EMPTY_TRACE, not NOT_APPLICABLE).

**No critical or major regression here.**

### 7.3 `violated` Override Behavior

`derive_isolation_result` VIOLATED block is unchanged. The VIOLATED first-branch priority in `interpret_probe_gate` is unchanged. Any VIOLATED isolation result still routes to `EXECUTION_INVALID_TOOL_VIOLATION` regardless of `probe_result`.

**No critical or major regression here.**

### 7.4 Dry-Runner No-Provider/No-Network Boundary

`run_memorization_probe.py` hash is unchanged (`2AC939208D5D92F1E4A7D54B7AA2F96213D6EF65ED726DCA3674963D467A51BC`). The runner was not modified by the patch.

**No critical or major regression here.**

### 7.5 No-LLM-Import Guard Behavior

The guard now scans `schemas/*.py` in addition to the prior targets. The test passes, confirming `probe_models.py` is clean. The guard is more comprehensive, not weaker.

**No critical or major regression here.**

### 7.6 Pydantic Contradiction Prevention

The `hidden_context_boundary` tightening in `derive_isolation_result` cannot weaken any existing contract invariant. Within the Pydantic model path, `reject_blank_evidence` already ensures `hidden_context_boundary` is non-empty before `derive_isolation_result` is called. The change only affects direct calls on namespace-like objects (the R-03 scenario). All existing tests constructing PROVEN isolation use non-empty boundary strings and continue to produce PROVEN. ✓

The new `EMPTY_TOOL_TRACE` validator adds a contradiction check and cannot weaken any existing gate behavior.

**No critical or major regression here.**

### 7.7 Existing Harness Test Compatibility

Observed test results:

```
tests/contract/test_memorization_probe_no_tools_contract.py + tests/contract/test_no_llm_imports.py:
12 passed in 0.24s

Full suite:
50 passed in 3.33s
```

Commission-noted post-patch validation: 12 / 46. This recheck observes 12 / 50. The 4-test delta in the full suite is from other unrelated work in the dirty workspace (untracked test files). No tests were removed. The contract and no-llm-imports suites match the commission's count exactly.

**No critical or major regression here.**

---

## 8. Recommendation

**`accept`**

All six prior findings are closed. No critical or major regressions were introduced by the patch. The gate logic remains correct: `PASS_VALID` requires `PASS + PROVEN`, all other combinations route to non-pass states, and the `ValueError` fallthrough ensures any future unhandled enum combination is surfaced immediately rather than silently absorbed.

---

## 9. Non-Claims

- No live probe was run.
- No model or provider call was made.
- No participant packet was loaded or exposed.
- No scoring was performed.
- No ledger freeze was performed.
- No schema or runtime readiness claim is made.
- No validation, fixture admission, product proof, or judgment-quality proof is claimed.
- This recheck does not authorize probe execution, blind judgment runs, fixture admission, or gate clearing.
- This recheck does not prove that a real probe with these code paths will produce correct isolation under live execution conditions.

plumbing works only; not judgment quality.
