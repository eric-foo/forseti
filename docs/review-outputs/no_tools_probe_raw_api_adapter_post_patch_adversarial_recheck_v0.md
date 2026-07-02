---
artifact_id: no_tools_probe_raw_api_adapter_post_patch_adversarial_recheck_v0
artifact_role: Post-patch adversarial recheck — raw-API no-tools adapter
created_at: 2026-06-01
review_mode: post_patch_adversarial_recheck
output_mode: filesystem-output
status: completed
reviewed_by: claude-sonnet-4-6 via workflow-deep-thinking + workflow-code-review
commission: >
  Closure-only recheck verifying M-01 and M-02 from prior adversarial review
  no_tools_probe_raw_api_adapter_adversarial_code_review_v0. Touched-scope
  blocker/major regression scan included.
recommendation: accept
prior_review: docs/review-outputs/no_tools_probe_raw_api_adapter_adversarial_code_review_v0.md
prior_review_hash: AEFDE9CDA1F71C793DF50DEF6894EADBEC480DD2BE481C6935F3BFD367B2D3D6
source_context_status: SOURCE_CONTEXT_READY
authority_hashes_verified: true
closed_findings: [M-01, M-02]
still_open_findings: []
patch_caused_regressions: none
---

# Post-Patch Adversarial Recheck: Raw-API No-Tools Adapter


```yaml
retrieval_header_version: 1
artifact_role: Post-patch adversarial recheck report
scope: Closure recheck for raw-API no-tools adapter M-01/M-02 patches.
use_when:
  - Checking closure of raw-API no-tools adapter major findings.
  - Auditing touched-scope blocker/major regression scan for the raw-API adapter patch.
authority_boundary: retrieval_only
```

## 1. Commission

Closure-only recheck of two prior major findings from
`no_tools_probe_raw_api_adapter_adversarial_code_review_v0`:

- **M-01:** `raw_response_hash` hashed only extracted model text, not the full provider
  response body.
- **M-02:** `NOT_APPLICABLE + PROVEN` isolation was validated against request-body shape
  but allowed arbitrary `--api-url` endpoints.

Scope: closure verification plus touched-scope blocker/major regression scan.
No full code review. Minor/nit findings reported only where the patch causes a blocker
or major downstream risk.

**Hard boundaries enforced.** No live provider call. No key exposure. No participant
packet access. No scoring. No fixture admission. No ledger freeze.

---

## 2. Source Context Verification

Branch: `main`  
HEAD: `84fa6d96714a3917919d94b0f45532564cee653f` — matches expected.  
Output path `docs/review-outputs/no_tools_probe_raw_api_adapter_post_patch_adversarial_recheck_v0.md` — did not exist before write; no collision.

All 16 required SHA-256 hashes computed and verified against on-disk files before review.

| File | Expected hash (prefix) | Match |
|---|---|---|
| `AGENTS.md` | `5800D6EC…` | ✓ |
| `.agents/workflow-overlay/README.md` | `40E28238…` | ✓ |
| `.agents/workflow-overlay/review-lanes.md` | `29778128…` | ✓ |
| `.agents/workflow-overlay/validation-gates.md` | `26406388…` | ✓ |
| `…/contestant_no_tools_execution_contract_v0.md` | `E8B5F2E2…` | ✓ |
| `…/memorization_probe_protocol.md` | `7862F03D…` | ✓ |
| `…/contestant_no_tools_execution_contract_post_patch_closure…` | `7FF0E5F9…` | ✓ |
| `…/no_tools_probe_runner_step04_post_patch_adversarial_recheck…` | `08BC5C7C…` | ✓ |
| `…/no_tools_probe_raw_api_adapter_adversarial_code_review_v0.md` | `AEFDE9CD…` | ✓ |
| `orca-harness/schemas/probe_models.py` | `A2277955…` | ✓ |
| `orca-harness/runners/run_memorization_probe.py` | `2AC93920…` | ✓ |
| `orca-harness/runners/run_memorization_probe_raw_api.py` | `CD83FDE1…` | ✓ |
| `orca-harness/tests/contract/test_memorization_probe_no_tools_contract.py` | `55F64BD0…` | ✓ |
| `orca-harness/tests/contract/test_no_llm_imports.py` | `1F2D74C0…` | ✓ |
| `orca-harness/README.md` | `3A05410B…` | ✓ |
| `orca-harness/docs/v0_14/README.md` | `DCD426F7…` | ✓ |

`SOURCE_CONTEXT_READY`

---

## 3. Test Results

Tests run offline only. No network, provider calls, or live probes.

**Focused suite** (`test_memorization_probe_no_tools_contract.py` + `test_no_llm_imports.py`):

```
22 passed in 1.75s
```

Commission reference baseline: `22 passed`. **Match.**

Delta from prior review baseline (19 passed): +3 new tests, all in the focused suite.
New tests identified:
- `test_raw_api_provider_rejects_non_standard_endpoint`
- `test_raw_api_provider_rejects_response_text_shortcut`
- `test_provider_http_error_redacts_header_secret`

**Full suite:**

```
66 passed in 5.84s
```

Commission reference baseline: `66 passed`. **Match.**

`git diff --check` on patched files: no whitespace errors. One LF/CRLF line-ending
notice on `orca-harness/README.md` (Windows working copy artifact, not a content defect).

---

## 4. Deep-Thinking Failure Mode Frame

Applied before listing findings.

**Gate invariant review:** `interpret_probe_gate` enumerates all 9 `(ProbeResult × IsolationResult)` combinations explicitly. The only path to `PASS_VALID` remains `PASS + PROVEN`. This invariant is unchanged by the patch and was confirmed clean in the prior step04 recheck.

**Adversarial frame for M-01 patch:** Full response hashing changes `raw_response_body` from the argument to `build_probe_artifact(..., raw_response_text=raw_response_body, ...)`. This does not affect `parsed_response` (still derived from extracted `model_text`) and does not affect gate logic. The semantic risk is whether the change correctly documents what the hash covers, and whether it creates any path for misleading downstream consumers. The documentation now explicitly states coverage. No gate path uses the hash value.

**Adversarial frame for M-02 patch:** The endpoint constraint is checked before transport and before any artifact write. The only question is whether the allowlist is sufficient and whether the check can be bypassed. The function `validate_standard_provider_endpoint` uses `urlparse` to independently parse the URL and checks scheme, hostname, path, params, query, and fragment separately. No bypass path was found.

---

## 5. M-01 Closure Verification

**Prior finding:** `build_probe_artifact(..., raw_response_text=model_text, ...)` — only extracted model text was hashed.

**Minimum closure conditions from prior review:**
- (a) `raw_response_hash` recomputed from `raw_response_body`, semantics updated in docs; OR
- (b) field renamed to `model_text_hash`; OR
- (c) owner accepts current scope with a clarifying note.

**Observed patch (option a):**

`run_memorization_probe_raw_api.py` line 286:
```python
artifact = build_probe_artifact(
    probe_input=probe_input,
    parsed_response=parsed_response,
    raw_response_text=raw_response_body,   # ← patched: full body, not model_text
    ...
)
```

`test_memorization_probe_no_tools_contract.py` line 517:
```python
assert receipt["raw_response_hash"] == hashlib.sha256(raw_response_body.encode("utf-8")).hexdigest()
```

The test uses `raw_response_body` — the full JSON response string — not `model_text`. This is a direct assertion that `raw_response_hash = sha256(full_provider_response_body)`.

`orca-harness/README.md` line 94:
> "the receipt `raw_response_hash` covers the full provider response body"

`orca-harness/docs/v0_14/README.md` line 25:
> "Its `raw_response_hash` covers the full provider response body."

**Dry-run behavior:** The dry runner (`run_memorization_probe.py`) still hashes the local raw response text file supplied via `--raw-response`. Test `test_cli_writes_dry_probe_receipt_with_hashes` at line 460:
```python
assert receipt["raw_response_hash"] == hashlib.sha256(raw_response_text.encode("utf-8")).hexdigest()
```
This is a local text file path, not a live provider response body. The dry runner never calls a provider; it normalizes pre-supplied local files. Dry-run behavior is unchanged and semantically correct for that execution surface.

**M-01: CLOSED.** All minimum closure conditions met under option (a).

---

## 6. M-02 Closure Verification

**Prior finding:** Arbitrary `--api-url` endpoints accepted; `NOT_APPLICABLE + PROVEN` isolation validated only against request-body shape, not provider endpoint identity.

**Minimum closure conditions from prior review:**
- (a) Isolation evidence made explicit about the assumption; OR
- (b) Provider validation added to verify known safe endpoint before `NOT_APPLICABLE + PROVEN`; OR
- (c) Owner accepts two-provider scope with documentation.

**Observed patch (option b):**

New constant (lines 96–99):
```python
STANDARD_PROVIDER_ENDPOINTS = {
    RawApiProvider.OPENAI_RESPONSES: ("api.openai.com", "/v1/responses"),
    RawApiProvider.ANTHROPIC_MESSAGES: ("api.anthropic.com", "/v1/messages"),
}
```

New function (lines 157–166):
```python
def validate_standard_provider_endpoint(provider: RawApiProvider, api_url: str) -> None:
    expected_host, expected_path = STANDARD_PROVIDER_ENDPOINTS[provider]
    parsed = urlparse(api_url)
    if parsed.scheme != "https" or parsed.hostname != expected_host or parsed.path != expected_path:
        raise ValueError(
            "Raw no-tools isolation is proven only for the standard "
            f"{provider.value} endpoint https://{expected_host}{expected_path}"
        )
    if parsed.params or parsed.query or parsed.fragment:
        raise ValueError("Raw no-tools provider endpoint must not include params, query, or fragment")
```

Called before transport (line 252):
```python
validate_standard_provider_endpoint(provider, api_url)
request_body = build_provider_request(...)
...
raw_response_body = transport.post_json(api_url, headers, request_body, timeout_seconds)
```

Execution order in `run_memorization_probe_raw_api`:
1. Load probe input
2. `validate_standard_provider_endpoint` — raises `ValueError` on non-standard URL
3. `build_provider_request` — raises if forbidden keys
4. `build_provider_headers` — raises if empty key
5. `transport.post_json` — network call
6. `extract_model_text`, `parse_provider_model_text`
7. `build_probe_artifact`, `write_yaml_file`

A non-standard endpoint raises at step 2. Transport is never called. No artifact is written.

Endpoint params/query/fragment are checked explicitly in `validate_standard_provider_endpoint`. A URL of `https://api.openai.com/v1/responses?injected=true` would be rejected.

**Test (lines 564–569):**
```python
def test_raw_api_provider_rejects_non_standard_endpoint() -> None:
    with pytest.raises(ValueError, match="standard openai_responses endpoint"):
        validate_standard_provider_endpoint(
            RawApiProvider.OPENAI_RESPONSES,
            "https://provider.invalid/v1/responses",
        )
```

**Request-body no-tools validation:** `validate_provider_request_shape` is called inside
`build_provider_request` at line 127, unchanged. The forbid-list and allow-list checks remain
intact.

**README documentation:**

`orca-harness/README.md` lines 90–92:
> "Clean no-tools isolation is limited to the standard OpenAI Responses endpoint and Anthropic
> Messages endpoint named by the runner; arbitrary proxy or provider URLs are rejected for clean
> isolation."

`orca-harness/docs/v0_14/README.md` lines 21–23:
> "limits clean isolation to standard OpenAI Responses and Anthropic Messages endpoints, rejects
> arbitrary proxy or provider URLs"

**M-02: CLOSED.** All minimum closure conditions met under option (b).

---

## 7. Patch-Caused Blocker/Major Regression Scan

Scope: touched patch scope only. Pre-existing issues excluded.

### 7.1 Can any path still produce fake `pass_valid`?

Gate invariant unchanged. `interpret_probe_gate` is not in the patched scope and was
confirmed clean in the prior recheck. No new path to fake `PASS_VALID` was introduced.
**No regression.**

### 7.2 Can a non-standard endpoint reach transport or write a valid artifact?

`validate_standard_provider_endpoint` is called at step 2, before transport and before
any artifact write. Non-standard endpoints raise `ValueError` immediately. The exception
propagates through `run_memorization_probe_raw_api` and is caught by `main()`, which exits
with status 2. No transport call occurs, no artifact is written.
**No regression.**

### 7.3 Can malformed provider JSON/YAML write a success artifact?

`extract_model_text` raises `ValueError` on JSON parse failure. `parse_provider_model_text`
raises `ValueError` on YAML parse failure or schema mismatch. Both occur before
`build_probe_artifact` and `write_yaml_file`. Test
`test_raw_api_provider_malformed_response_writes_no_artifact` confirms `output_path` does
not exist after a malformed response.
**No regression.**

### 7.4 Did full-response hashing create a mismatch between `parsed_response` and `raw_response_hash` semantics?

`parsed_response` remains derived from `model_text` (extracted text). `raw_response_hash`
now covers `raw_response_body` (full provider JSON). These are separate semantic layers
with different purposes:
- `parsed_response`: structured interpretation of model text for gate logic.
- `raw_response_hash`: integrity fingerprint of the full provider response body.

Both READMEs explicitly document what `raw_response_hash` covers. Downstream consumers
reading the receipt know the hash covers the full body, not just extracted text. No
misleading mismatch.
**No regression.**

### 7.5 Did endpoint allow-listing accidentally make mocked tests unrealistic or block standard providers?

All fake-transport tests explicitly supply the standard URL `https://api.openai.com/v1/responses`.
The CLI refusal test supplies `https://provider.invalid/v1/responses`, but the live-call
flag check at lines 389–390 fires before `run_memorization_probe_raw_api` is called, so
`validate_standard_provider_endpoint` is never reached in that test. Test realism is
preserved for both standard and non-standard URL paths.
**No regression.**

### 7.6 Did API-key redaction introduce secret leakage, over-redaction, or false sense of complete protection?

`_redact_header_secrets` (lines 343–353) targets only the specific header values used to
authenticate (`Authorization: Bearer <token>` and `x-api-key: <key>`). It does not
over-redact other evidence fields. It applies only to HTTP error response bodies reflected
in the error message (the m-03 minor finding from the prior review). The receipt still
asserts `"secret-token" not in str(receipt)`.

The function is narrow and correctly scoped. It does not claim to protect all possible
secret leakage paths (e.g., OS-level logging of stdout/stderr by external harnesses); this
limitation is unchanged from the prior review and is a known accepted risk.
**No regression introduced by the patch.**

### 7.7 Did removing the `response_text` shortcut break standard OpenAI or Anthropic extraction?

The `response_text` shortcut was a pre-dispatch path in the prior version of
`extract_model_text`. Its removal forces all extraction through the provider-specific
paths. Standard OpenAI responses use `output_text` (or `output[].content[].text`) handled
by `_extract_openai_response_text`. Standard Anthropic responses use `content[].text`
handled by `_extract_anthropic_response_text`. Neither provider returns a top-level
`response_text` key by standard API contract. New test
`test_raw_api_provider_rejects_response_text_shortcut` confirms the shortcut path is gone
and such payloads are rejected with an appropriate error.
**No regression. The shortcut removal was a security/clarity improvement.**

### 7.8 Did docs overclaim live-use readiness, validation, fixture admission, or judgment quality?

`orca-harness/README.md` lines 12–13:
> "opt-in raw-API no-tools memorization-probe execution plumbing only, not probe
> authorization"

Lines 95–97:
> "The runner is still only execution plumbing; using it for a real probe requires separate
> owner authorization for the exact model/case pair."

`orca-harness/docs/v0_14/README.md` lines 25–27:
> "It does not itself authorize a probe, expose participant packets, score outputs, freeze a
> ledger, admit a fixture, or prove judgment quality."

No overclaiming. Non-claim boundary is clearly stated in both READMEs.
**No regression.**

---

## 8. Prior Minor Findings (Touched Scope)

The following minor findings from the prior review were in the patched scope. No closure
claim is made; these are informational observations only.

| Prior finding | Status in patch |
|---|---|
| m-01: `response_text` shortcut untested and bypasses provider validation | Addressed: shortcut removed; new test `test_raw_api_provider_rejects_response_text_shortcut` confirms rejection |
| m-02: double `validate_provider_request_shape` call | Addressed: explicit second call removed; only the call inside `build_provider_request` remains |
| m-03: API key could appear in stderr via provider HTTP error body | Addressed: `_redact_header_secrets` called in `HTTPError` handler; new test `test_provider_http_error_redacts_header_secret` confirms redaction |
| O-01: `run_memorization_probe_raw_api` function carries no live-call guard | Unchanged; function docstring added: "CLI accidental-live-call guard is in main()". Matches declared intent. |

---

## 9. Recommendation

**`accept`**

Both M-01 and M-02 are closed. No patch-caused blocker or major regression was found.

M-01 is closed by passing `raw_response_body` (full provider JSON) instead of `model_text`
to `build_probe_artifact`, updating the test assertion, and documenting the coverage in
both READMEs. The dry-run path is unchanged and semantically correct.

M-02 is closed by `validate_standard_provider_endpoint`, which constrains clean `NOT_APPLICABLE + PROVEN`
isolation to the two named standard endpoints, rejects params/query/fragment, fires before
transport execution, and is tested. Both READMEs name the endpoint limitation.

All 22 focused tests and 66 full-suite tests pass. Three new tests cover the closure
implementations and the minor-finding fixes.

---

## 10. Non-Claims

- No live probe was run.
- No model call was made.
- No provider network access was performed.
- No participant packet was loaded or exposed.
- No probe pass or fail is claimed.
- No scoring was performed.
- No ledger freeze was performed.
- No schema or runtime readiness is claimed.
- No validation, fixture admission, product proof, or judgment-quality proof is claimed.
- This recheck does not authorize probe execution, blind judgment runs, fixture admission,
  or gate clearing.
- Recheck findings are decision input only; they are not approval, validation, mandatory
  remediation, or executor-ready patch authority until separately accepted or authorized.

plumbing works only; not judgment quality.
