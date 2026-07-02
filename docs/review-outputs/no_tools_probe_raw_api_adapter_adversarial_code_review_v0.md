---
artifact_id: no_tools_probe_raw_api_adapter_adversarial_code_review_v0
artifact_role: Adversarial code review — raw-API no-tools memorization-probe adapter
created_at: 2026-06-01
review_mode: adversarial_code_review
output_mode: filesystem-output
status: completed
reviewed_by: claude-sonnet-4-6 via workflow-deep-thinking + workflow-code-review
commission: >
  Can the raw-API no-tools adapter accidentally turn an unclean provider execution
  into a clean pass_valid memorization-probe gate result?
recommendation: accept_with_friction
source_context_status: SOURCE_CONTEXT_READY
authority_hashes_verified: true
findings_count: 6
blocking_findings: 0
advisory_findings:
  major: 2
  minor: 3
  optional: 1
---

# Adversarial Code Review: Raw-API No-Tools Memorization-Probe Adapter


```yaml
retrieval_header_version: 1
artifact_role: Adversarial code review report
scope: Adversarial code review of the raw-API no-tools memorization-probe adapter.
use_when:
  - Auditing raw-API no-tools adapter review findings.
  - Checking fake-clean-pass risks in no-tools raw provider execution plumbing.
authority_boundary: retrieval_only
```

## 1. Commission

**Central question:** Can the raw-API no-tools adapter accidentally turn an unclean provider
execution into a clean `pass_valid` memorization-probe gate result?

**Review surfaces:** `run_memorization_probe_raw_api.py`, contract tests, no-LLM-imports guard,
READMEs, supporting schemas, dry runner.

**Hard boundaries enforced:** No live provider call. No key exposure. No participant packet access.
No scoring. No fixture admission. No ledger freeze.

**Required closeout:** `plumbing works only; not judgment quality`

---

## 2. Source Context

All 15 required SHA-256 hashes verified against on-disk files before review.

| File | Expected hash | Observed hash | Match |
|---|---|---|---|
| `AGENTS.md` | `5800D6EC…` | verified | ✓ |
| `.agents/workflow-overlay/README.md` | `40E28238…` | verified | ✓ |
| `.agents/workflow-overlay/review-lanes.md` | `29778128…` | verified | ✓ |
| `.agents/workflow-overlay/validation-gates.md` | `26406388…` | verified | ✓ |
| `…/contestant_no_tools_execution_contract_v0.md` | `E8B5F2E2…` | verified | ✓ |
| `…/memorization_probe_protocol.md` | `7862F03D…` | verified | ✓ |
| `…/contestant_no_tools_execution_contract_post_patch_closure…` | `7FF0E5F9…` | verified | ✓ |
| `…/no_tools_probe_runner_step04_post_patch_adversarial_recheck…` | `08BC5C7C…` | verified | ✓ |
| `orca-harness/schemas/probe_models.py` | `A2277955…` | verified | ✓ |
| `orca-harness/runners/run_memorization_probe.py` | `2AC93920…` | verified | ✓ |
| `orca-harness/runners/run_memorization_probe_raw_api.py` | `84B445ED…` | verified | ✓ |
| `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py` | `7F6F5A6B…` | verified | ✓ |
| `orca-harness/tests/contract/test_no_llm_imports.py` | `1F2D74C0…` | verified | ✓ |
| `orca-harness/README.md` | `F5A907A1…` | verified | ✓ |
| `orca-harness/docs/v0_14/README.md` | `ACF3753B…` | verified | ✓ |

`SOURCE_CONTEXT_READY`

---

## 3. Test Results

Tests run against pinned sources, offline only, no network, no provider calls.

**Focused suite (`test_memorization_probe_no_tools_contract.py` + `test_no_llm_imports.py`):**
```
19 passed in 1.80s
```

**Full suite:**
```
63 passed in 6.31s
```

Both counts match the commission reference baseline (focused: 19, full: 63).
No regressions against the prior review baseline.

---

## 4. Deep-Thinking Failure Mode Frame

Applied before listing findings.

**Gate invariant:** `pass_valid` requires `probe_result == PASS AND isolation_result == PROVEN`.
The gate logic in `interpret_probe_gate` enumerates all 9 `(ProbeResult × IsolationResult)`
combinations explicitly. The only path to `PASS_VALID` is `PASS + PROVEN`. This was confirmed
clean in the prior step04 recheck and is unchanged.

**Adversarial question 1: Can isolation be PROVEN without genuine no-tools execution?**

The adapter hardcodes `isolation_result = PROVEN` via `build_isolation_evidence` with fixed fields:
- `tool_access_policy = NO_TOOLS`
- `tool_config_evidence_kind = STRUCTURAL_CONFIG`
- `tool_call_trace_status = NOT_APPLICABLE`
- All four disabled fields = `True`
- `hidden_context_boundary` = non-empty string

PROVEN is then derived by `derive_isolation_result`, which runs the same logical path as all other
executions. The claim of PROVEN rests entirely on the request body having been validated to contain
no tool/search/retrieval/context fields. The validation is structural and programmatic
(`find_forbidden_request_keys` + provider-specific allow-lists + exact prompt equality checks).

**Finding:** PROVEN is not assumed — it is derived from request-body shape validation. If the
validation were bypassed, PROVEN would not be reached. The validation appears sound for the
intended providers (OpenAI Responses API, Anthropic Messages API).

**Adversarial question 2: Can probe_result be PASS from a contaminated response?**

`probe_result` is derived from `classify_probe_response(parsed_response)`. The parsed response
comes from `parse_provider_model_text(model_text)`, which YAML-parses the extracted model text
and validates against `ParsedProbeResponse`. PASS requires `recognition_status == "unknown"` OR
`claimed_outcome is None`. This is the contract's declared pass condition.

**Finding:** No code path allows PASS from a response that identifies the case outcome with
confidence ≥ 0.5 and non-null `claimed_outcome`. The classification is deterministic from the
YAML.

**Adversarial question 3: Can provider-side context leakage produce PASS without model knowledge
being probed cleanly?**

The adapter sends only provider control fields + probe prompt. The forbid-list check (`find_forbidden_request_keys`) runs recursively and the allow-list check catches unexpected top-level keys. The prompt equality check enforces that the `input` / `messages` field is exactly the generated probe prompt.

**Finding:** Request body leakage prevention is sound. The response-parsing path
(`extract_model_text`) strips provider JSON envelope and returns only model text. However,
provider-level tool-use blocks in the response are silently dropped (Anthropic-specific: only
`type == "text"` blocks are extracted). If a provider returned tool-use output alongside text,
the hash would not capture it.

**Adversarial question 4: What are the actual hash-coverage guarantees?**

- `prompt_hash` = SHA-256 of the generated probe prompt string. Covers exactly what was sent to
  the model. ✓
- `raw_response_hash` = SHA-256 of `model_text` (extracted model output YAML string), **not**
  of `raw_response_body` (the full provider JSON response). This is a material gap.

Verified computationally:
- `hash(model_text)` = `bfc01304ef47eac6d3349727f68f072abf23357c140b4bc2cf0c5c0760fa4650`
- `hash(full_provider_json)` = `ef4c0d6eb2fd5a3ab056bcbb62303817528c65e8eb631584479ba39b634c04d0`
- These differ.

The `raw_response_hash` field name implies raw-response coverage, but the implementation covers
only extracted model text. Provider-level envelope fields (system_fingerprint, usage tokens,
stop_reason, tool_use blocks) are not integrity-protected by this hash.

---

## 5. Findings

### M-01 (Major) — `raw_response_hash` hashes extracted model text, not full provider response body

**Location:** `run_memorization_probe_raw_api.py` line 274 (via `build_probe_artifact`
`raw_response_text=model_text`); `run_memorization_probe.py:121` (`raw_response_hash=sha256_text(raw_response_text)`)

**Evidence:**
```python
# run_memorization_probe_raw_api.py
model_text = extract_model_text(provider, raw_response_body)
...
artifact = build_probe_artifact(
    ...
    raw_response_text=model_text,   # ← extracted text only, not raw_response_body
    ...
)
```

The test explicitly confirms this:
```python
# test_memorization_probe_no_tools_contract.py line 515
assert receipt["raw_response_hash"] == hashlib.sha256(model_text.encode("utf-8")).hexdigest()
```

**Authority:** Protocol artifact schema names the field `raw_response_hash`.
Contract field purpose: integrity of what the model returned. Reviewer computation confirms the
hash values differ (`model_text` hash ≠ full provider JSON hash).

**Impact:** Provider-level envelope content (system_fingerprint, stop_reason, usage, any
tool_use blocks returned alongside text) is not covered by the receipt hash. If a provider
returns tool_use blocks that are stripped by `_extract_anthropic_response_text` (which filters
only `type == "text"` content), no evidence of those blocks appears in the hash. The field name
misleads downstream consumers expecting raw-response coverage.

This does not enable a fake `pass_valid` (the gate does not use the hash). It weakens audit
fidelity: a receipt cannot prove whether the full provider response contained anything beyond the
extracted text.

**Minimum closure condition:** Either (a) `raw_response_hash` is recomputed from `raw_response_body`
and the field semantics are updated in docs, or (b) the field name is changed to reflect that it
hashes extracted model text (`model_text_hash`) and documentation clarifies the scope, or (c) the
owner accepts the current scope and a note is added to the protocol schema and README clarifying
that the hash covers extracted model text, not the full provider response body.

**Next authorized action:** Owner decision on preferred scope; advisory finding only, no patch
authority here.

---

### M-02 (Major) — `NOT_APPLICABLE` isolation claim validated against request-body shape, not provider-level tool capability

**Location:** `run_memorization_probe_raw_api.py` lines 247–266 (hardcoded
`ToolCallTraceStatus.NOT_APPLICABLE`); `probe_models.py` line 171 (`not_applicable` contract rule)

**Evidence:**
The contract states:
> `not_applicable` is valid only when the execution environment structurally cannot invoke tools
> regardless of configuration, such as a raw API call where no tool schema or retrieval channel
> is supplied.

The adapter satisfies "no tool schema or retrieval channel supplied" via request-body validation.
However, the adapter accepts arbitrary `--api-url` at the CLI. For standard OpenAI Responses API
and Anthropic Messages API endpoints, the claim is sound (neither invokes tools without
client-supplied schemas). For non-standard endpoints (e.g., a provider with server-side function
calling or built-in search at the account level), the claim would be incorrect: the absence of
tool schemas in the request does not guarantee the provider cannot invoke tools.

The isolation evidence description says "no tool, search, retrieval, browser, file, attachment,
workspace, system, developer, or hidden-context fields were **supplied**." This is accurate for
the request, but `NOT_APPLICABLE` in the contract means the environment "**cannot** invoke tools
regardless of configuration." These are different claims. The evidence text matches the narrower
claim (what was sent) while the status value asserts the broader claim (what the environment
can do).

**Impact:** For the two supported providers (OpenAI, Anthropic) at standard REST endpoints, this
is correct in practice. For any future provider addition or non-standard endpoint, the isolation
claim would be incorrect without additional validation. A receipt produced against a
provider-with-server-side-tools would carry `isolation_result: proven` and `NOT_APPLICABLE`
despite a potentially unclean execution environment.

**Minimum closure condition:** Either (a) the isolation evidence string is made explicit about the
assumption ("for standard OpenAI/Anthropic REST API endpoints that do not invoke tools without
client-supplied schemas…"), or (b) provider validation is added to verify the endpoint is a
known safe provider before assigning NOT_APPLICABLE + PROVEN, or (c) the owner accepts the
two-provider scope constraint and adds documentation noting that arbitrary `--api-url` with
non-standard providers is not validated for server-side tool capability.

**Next authorized action:** Owner decision on scope claim or documentation; advisory finding only.

---

### m-01 (Minor) — `response_text` shortcut in `extract_model_text` is untested and bypasses provider-specific response format validation

**Location:** `run_memorization_probe_raw_api.py` lines 190–192

**Evidence:**
```python
def extract_model_text(provider: RawApiProvider, raw_response_body: str) -> str:
    ...
    if isinstance(response_data, dict) and isinstance(response_data.get("response_text"), str):
        return response_data["response_text"]      # ← shortcut before provider dispatch

    if provider == RawApiProvider.OPENAI_RESPONSES:
        text = _extract_openai_response_text(response_data)
    elif provider == RawApiProvider.ANTHROPIC_MESSAGES:
        text = _extract_anthropic_response_text(response_data)
```

Verified: any JSON with a top-level string `response_text` key is accepted as model text,
regardless of provider format or other keys present. This path fires before OpenAI/Anthropic
parsing. No test exercises this path (all tests use standard OpenAI/Anthropic-format JSON via
`_FakeTransport`).

**Impact:** The shortcut bypasses provider-specific response format validation. If a non-standard
provider or test fixture returns `{"response_text": "recognition_status: unknown..."}`, the
adapter accepts it silently. In production with real providers (OpenAI, Anthropic), neither
returns `response_text`, so this path does not trigger. However, it is an undocumented, untested
code path that could confuse future maintainers or trigger unexpectedly if a provider adds this
key to their response format.

**Minimum closure condition:** Either (a) the shortcut is removed and test transports use standard
provider-format JSON, or (b) the shortcut is retained but documented (comment explaining its
purpose) and a test is added that exercises it explicitly.

**Next authorized action:** Advisory suggestion; owner/implementer decision.

---

### m-02 (Minor) — Double `validate_provider_request_shape` call

**Location:** `run_memorization_probe_raw_api.py` lines 236–242

**Evidence:**
```python
request_body = build_provider_request(...)      # calls validate_provider_request_shape at line 122
validate_provider_request_shape(provider, request_body, probe_prompt)  # called again explicitly
```

`build_provider_request` already calls `validate_provider_request_shape` as its last line
(line 122). `run_memorization_probe_raw_api` then calls it again explicitly before transport
(line 242).

**Impact:** Harmless redundancy. Both calls use the same arguments and will produce identical
results. No gate-safety impact. Adds slight latency, could confuse readers about intent.

**Minimum closure condition:** Remove the redundant explicit call, or add a comment explaining
why both calls are intentional (defense-in-depth).

**Next authorized action:** Advisory cleanup suggestion; owner discretion.

---

### m-03 (Minor) — API key could appear in stderr via provider HTTP error response body reflection

**Location:** `run_memorization_probe_raw_api.py` lines 47–52 (`UrllibJsonTransport.post_json`),
lines 384–385 (`main` exception handler)

**Evidence:**
```python
# UrllibJsonTransport.post_json
except HTTPError as exc:
    detail = exc.read().decode("utf-8", errors="replace")
    raise ValueError(f"Provider HTTP error {exc.code}: {detail}") from exc
```

```python
# main()
except Exception as exc:
    parser.exit(status=2, message=f"{exc}\n")
```

If a provider returns a 401/403 HTTP error response that includes the submitted API key in its
body (e.g., `{"error": "Invalid API key: sk-abc123..."}`), the key value appears in the
`ValueError` message and then in stderr via `parser.exit`. Neither OpenAI nor Anthropic reflects
keys in error bodies by standard practice, but this is a non-zero path.

The test `test_raw_api_provider_runner_with_fake_transport_produces_proven_pass` verifies
`assert "secret-token" not in str(receipt)` — this covers the receipt file but not stderr.

**Impact:** Non-standard risk. No known provider reflects submitted keys in error responses.
However, if a test or debugging transcript captures stderr output, a reflected key could appear.

**Minimum closure condition:** Either (a) add a key-redaction step in the error message path, or
(b) document that the raw-API runner should not be used with debug-capturing harnesses that
retain stderr, or (c) owner accepts the risk given no known provider reflects keys.

**Next authorized action:** Advisory; owner decision.

---

### O-01 (Optional) — `run_memorization_probe_raw_api` function does not enforce live-call protection at function level

**Location:** `run_memorization_probe_raw_api.py` lines 344–392 (`main`), function signature
lines 221–276

**Evidence:**
The `--allow-live-provider-call` flag is checked only in `main()`:
```python
if not args.allow_live_provider_call:
    parser.exit(status=2, message="Refusing live provider call without --allow-live-provider-call\n")
```

The function `run_memorization_probe_raw_api` itself carries no equivalent guard. Callers
that import and call the function directly (e.g., tests) bypass this protection. The contract
test `test_raw_api_provider_runner_with_fake_transport_produces_proven_pass` exercises this
path directly without any flag.

This is deliberate design — the flag is CLI-level protection against accidental operator
invocation, not function-level protection. The test confirms the function works without the flag.

**Impact:** No gate-safety impact. Callers who understand they are making a live API call can do
so. The protection is against *accidental* CLI invocation, not all invocations. Documented
intent appears correct.

**Minimum closure condition (optional):** Document at the function level (docstring or inline
comment) that the live-call guard is CLI-only, so future callers are not confused by the
asymmetry.

---

## 6. Review Surfaces Summary

| Surface | Result |
|---|---|
| Fake clean pass via gate logic | No path found |
| `NOT_APPLICABLE` justification | Valid for standard providers; over-claims for arbitrary endpoints (M-02) |
| Tool/retrieval/context in request body | Prevented by forbid-list + allow-list + prompt equality checks |
| Hidden context boundary | Request body validated programmatically; description accurately reflects what was sent |
| `prompt_hash` fidelity | Correct: SHA-256 of generated probe prompt string |
| `raw_response_hash` fidelity | Covers only extracted model text, not full provider response body (M-01) |
| Model metadata | `model_snapshot_if_available` returns what provider supplies or None; no overclaiming |
| Blocked/error behavior | Malformed JSON, malformed YAML, missing fields, missing credentials, missing model ID, HTTP errors all raise `ValueError` before artifact is written |
| Secret handling | API key not in receipt (test-verified); theoretical stderr leak via provider error reflection (m-03) |
| No live-call safety (CLI) | CLI refuses without `--allow-live-provider-call`; test-verified |
| Dry-run regression | Dry runner hash unchanged; behavior unchanged |
| Test adequacy | 19 contract tests pass; covers clean mocked path, forbidden fields, malformed response, no output on failure, read boundary, no SDK imports, CLI live-call refusal |
| Documentation boundary | README correctly distinguishes dry normalization, raw-API execution plumbing, and probe authorization |

---

## 7. Recommendation

**`accept_with_friction`**

The adapter cannot produce a false `pass_valid` through its code paths. The gate invariant
(PASS + PROVEN → PASS_VALID) is preserved and all 9 `(ProbeResult × IsolationResult)`
combinations route correctly. The request body validation is sound for the two supported
providers. Test coverage of gate-boundary cases is adequate and all 63 tests pass.

The friction comes from two material audit-fidelity weaknesses (M-01, M-02) that do not threaten
gate safety but weaken the audit promise:

- `raw_response_hash` silently covers less than its name implies. Downstream consumers expecting
  full-response integrity are misled.
- The `NOT_APPLICABLE` + PROVEN claim asserts provider-level structural isolation but validates
  only request-body shape. For the two declared providers this is sound in practice; for future
  provider additions it may not be.

Neither weakness enables a fake gate pass. The adapter is safe to use for authorized probe
execution against OpenAI Responses API or Anthropic Messages API standard endpoints.

---

## 8. Non-Claims

- No live probe was run.
- No model call was made.
- No provider network access was performed.
- No participant packet was loaded or exposed.
- No probe pass or fail is claimed.
- No scoring was performed.
- No ledger freeze was performed.
- No schema or runtime readiness is claimed.
- No validation, fixture admission, product proof, or judgment-quality proof is claimed.
- This review does not authorize probe execution, blind judgment runs, fixture admission, or gate clearing.
- Review findings are decision input only; they are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized.

plumbing works only; not judgment quality.
