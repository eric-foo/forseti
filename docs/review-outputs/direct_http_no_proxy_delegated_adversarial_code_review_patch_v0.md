# Direct HTTP No-Proxy Delegated Adversarial Code Review-and-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: delegated review output
scope: Bounded adversarial code review of the direct HTTP ambient-proxy isolation patch.
reviewer_family: Anthropic/Claude (de-correlated from OpenAI/Codex author family)
commission: direct_http_no_proxy_delegated_adversarial_code_review_patch_prompt_v0.md
authority_boundary: findings_and_verdict_for_CA_adjudication_only
```

---

## Source Context Declaration

`SOURCE_CONTEXT_READY`

Files read:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/review-lanes.md`
- `orca-harness/source_capture/adapters/direct_http.py`
- `orca-harness/tests/unit/test_source_capture_direct_http.py`
- `orca-harness/tests/contract/test_source_capture_direct_http_contract.py`
- `orca-harness/runners/run_source_capture_http_packet.py`

`orca-harness/runners/run_reddit_old_http_batch.py` and
`orca-harness/runners/run_reddit_batch_quality_summary.py` confirmed to exist
(glob-located; not read in full — no review question required them).

---

## Deep-Thinking: Highest-Risk Failure Modes

Framed before listing findings per review-lane rules.

**F0 — ProxyHandler({}) does not actually suppress ambient env**
The entire isolation guarantee rests on whether `build_opener(ProxyHandler({}))` prevents urllib from reading `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY`. If it doesn't, every "direct HTTP" packet produced in a proxy-bearing shell is silently contaminated: the response comes from the proxy, not the origin, yet the packet records no proxy use and asserts the "not proxy or session injection" non-claim. This is the single highest-risk failure mode.

**F1 — `_open_direct_http` seam breaks a preserved behavior**
The old path went through `urllib.request.urlopen`. The new path goes through `_NO_PROXY_OPENER.open`. Any difference in how the two handle HTTPError, URLError, redirect, timeout, or size-capped reads could create a silent false-success or unexpected exception path not caught by the current call site.

**F2 — Test is vacuous or otherwise structurally incapable of falsifying the old code**
If `monkeypatch.setenv` runs after `_NO_PROXY_OPENER` is already built, and the old code was also module-level, the test might pass for the wrong reason. A test that passes under both old and new code does not validate the fix.

**F3 — Module-level singleton creates hidden shared-state hazard**
`_NO_PROXY_OPENER` is a single `OpenerDirector` instance shared across all calls and threads. Mutation of opener state by a handler (cookie jar, redirect tracking, connection pooling) could leak cross-call state.

**F4 — Provenance claim weakening: proxy bypass not recorded**
The lane asserts "not proxy or session injection" but does not record that an explicit bypass was enforced. A consumer comparing two packets — one from a proxy-bearing shell, one from a clean shell — sees no differentiating field.

---

## Findings

### Finding 1 — ProxyHandler({}) is sufficient (CONFIRMED CORRECT, no defect)

**Severity:** N/A (confirmatory)
**File:** `orca-harness/source_capture/adapters/direct_http.py` lines 9, 17

**Evidence:**
CPython `urllib/request.py` `ProxyHandler.__init__`:
```python
def __init__(self, proxies=None):
    if proxies is None:
        proxies = getproxies()   # reads env vars
    assert hasattr(proxies, 'keys')
    self.proxies = proxies
    for type, url in proxies.items():
        setattr(self, '%s_open' % type, ...)
```
Passing `{}` is not `None`, so `getproxies()` is never called. The loop over `{}.items()` sets no `http_open` or `https_open` attributes, making the handler a no-op interceptor.

`build_opener` logic: when passed a `ProxyHandler({})` *instance*, it adds `type(handler) = ProxyHandler` to the `skip` set. The default `ProxyHandler()` (which would have called `getproxies()`) is therefore omitted. The custom `ProxyHandler({})` replaces it.

`_NO_PROXY_OPENER` is evaluated at module import time. Because `{}` is a literal — not `None` — the opener never reads env vars at import time or call time. This is safe regardless of environment state at any lifecycle point.

**Risk:** None. The mechanism is correct.
**Closure condition:** Not applicable.
**Patched:** No.

---

### Finding 2 — `_open_direct_http` seam preserves all required behaviors (CONFIRMED CORRECT, no defect)

**Severity:** N/A (confirmatory)
**File:** `orca-harness/source_capture/adapters/direct_http.py` lines 182–184

**Evidence:**

| Behavior | How preserved |
|---|---|
| Timeout | `_NO_PROXY_OPENER.open(request, timeout=timeout_seconds)` — the `OpenerDirector.open` signature accepts `timeout`. Passed correctly. |
| HTTPError | `build_opener` includes `HTTPDefaultErrorHandler` (not skipped). Non-2xx responses raise `HTTPError`. Caught at call site in `fetch_direct_http_capture`. |
| URLError | Network/DNS failures raise `URLError` through the handler chain. Caught at call site. |
| Redirects | `HTTPRedirectHandler` is included in defaults (not skipped). |
| Size cap | Applied downstream in `_capture_response` / `_read_with_cap`, unaffected by opener change. |
| Non-2xx body | `HTTPError` is an `addinfourl` subclass with `getcode()`, `geturl()`, `headers`, and `read()`. `_capture_response` accepts `HTTPResponse | HTTPError` and uses only those methods. |
| Context manager | `addinfourl` (returned by `open()`) implements `__enter__`/`__exit__`. `with _open_direct_http(...) as response:` is valid. |

**Risk:** None.
**Closure condition:** Not applicable.
**Patched:** No.

---

### Finding 3 — Test correctly discriminates old vs. new implementation (CONFIRMED VALID, no defect)

**Severity:** N/A (confirmatory)
**File:** `orca-harness/tests/unit/test_source_capture_direct_http.py` lines 192–204

**Evidence:**

*Would the test fail under old implementation?*
If the old implementation used `urllib.request.urlopen(request, timeout=...)`, the default opener calls `getproxies()` at open-time (not import-time). `monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:9")` sets the env var before the call. `getproxies_environment()` would return `{'http': 'http://127.0.0.1:9'}`. The HTTP request to `http://127.0.0.1:PORT/ok` would be routed through the proxy at port 9. Port 9 (Discard) is unbound on Windows; the connection is refused with `[WinError 10061]`, matching the production failure described in the commission context. The test would return `DirectHttpCaptureFailure` and fail the `isinstance(result, DirectHttpCaptureSuccess)` assertion. ✓

*Does the test pass under new implementation?*
`_NO_PROXY_OPENER` was built with `ProxyHandler({})` at import time. Env vars set by `monkeypatch.setenv` post-import have no effect on the pre-built opener. The request goes directly to the local test server. Result is `DirectHttpCaptureSuccess`. ✓

*Is the `NO_PROXY=""` setting appropriate?*
Yes. An empty `NO_PROXY` means "bypass proxy for no hosts." Without it, some urllib implementations on Windows might auto-exempt `127.0.0.1` as a "local" host. Setting it empty closes that escape and ensures old code would genuinely route through the proxy.

**Risk:** None. The test is a valid discriminator.
**Closure condition:** Not applicable.
**Patched:** No.

---

### Finding 4 — Module-level singleton is safe under concurrent use (ADVISORY, minor)

**Severity:** minor (advisory, not a defect)
**File:** `orca-harness/source_capture/adapters/direct_http.py` line 17

**Evidence:**
`_NO_PROXY_OPENER` is a shared `OpenerDirector` instance. CPython's `OpenerDirector.open` does not hold a global lock across handler dispatch. Each call creates its own `Request` context and receives its own `HTTPResponse`. The handler chain is read-only after build. No cookie jar is attached (no `HTTPCookieProcessor`). No connection pool is shared across calls (urllib's HTTP handling uses ephemeral connections unless keep-alive is reused, but response state is per-call).

The pattern is identical to the implicit module-global used by `urllib.request.urlopen`, which is also a shared `OpenerDirector`. No new hazard is introduced.

**Risk:** Low. No cross-call state leakage identified for the current handler set.
**Minimum closure condition:** Not required; advisory only.
**Next authorized action:** CA discretion.
**Patched:** No.

---

### Finding 5 — Proxy bypass not recorded in packet metadata or warning_notes (ADVISORY, design-level flag)

**Severity:** minor (advisory, design-level; not a correctness defect)
**File:** `orca-harness/source_capture/adapters/direct_http.py` lines 145–168

**Evidence:**
`_capture_response` builds `warning_notes`, `limitation_notes`, and `metadata`. None of these record that ambient proxy env was explicitly bypassed. The runner's `DIRECT_HTTP_NON_CLAIMS` includes `"not proxy or session injection"`, which is correct and now more firmly guaranteed. However, a packet consumer inspecting two packets captured in different shell environments (one with `HTTP_PROXY` set, one without) would see identical metadata. There is no field stating "ambient proxy bypass enforced."

The prompt explicitly asks whether a note should record that ambient proxy env was ignored without storing secret-bearing values. A candidate note: adding `"proxy_isolation": "no_proxy_opener_enforced"` to the `metadata` dict in `_capture_response`, or adding a `warning_note` such as `"direct_http: ambient proxy environment variables are explicitly ignored by this adapter"`. This would not store proxy values, only the structural fact of bypass.

**Arguments for adding the note:**
- Provenance completeness: packet consumers can see that proxy bypass was in effect
- Distinguishes packets captured with this patch vs. pre-patch behavior
- Satisfies the provenance-transparency posture the rest of the packet upholds

**Arguments against patching now:**
- Not a defect; the existing non-claim posture is consistent
- Adding metadata fields expands the packet schema, which is doctrinal scope beyond the ambient-proxy isolation boundary
- The prompt's Patch Boundary clause states: "If the correct fix requires changing packet schema or source-capture provenance doctrine, return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding instead of patching those files."

**Risk:** Advisory. The non-claims posture is not weakened; this is an enhancement to provenance transparency.
**Minimum closure condition:** CA decision on whether adapter-layer isolation metadata belongs in the packet schema. If yes, a schema-scoped patch authorization is needed.
**Next authorized action:** CA discretion; off-scope for this patch boundary.
**Patched:** No — per Patch Boundary clause, this requires a schema or provenance doctrine decision.

---

### Finding 6 — Contract test does not verify proxy-bypass behavior (ADVISORY, minor gap)

**Severity:** minor (advisory, structural gap)
**File:** `orca-harness/tests/contract/test_source_capture_direct_http_contract.py` (read-only)

**Evidence:**
`test_direct_http_adapter_avoids_browser_api_and_scraper_imports` checks AST imports but does not verify that the adapter uses a no-proxy opener. A future change replacing `_open_direct_http` with `urllib.request.urlopen` would pass the contract test. The behavioral proxy-bypass guarantee lives only in the unit test.

**Risk:** Low — the unit test is the correct place for behavioral guarantees. Contract tests verify structural non-claims (no scraper framework imports), not behavioral non-claims. This is consistent with the existing contract test design philosophy.

The contract test's `FORBIDDEN_IMPORT_ROOTS` set correctly includes `playwright`, `requests`, `httpx`, `aiohttp`, `bs4`, etc. The `ProxyHandler` / `build_opener` / `Request` imports are stdlib and correctly pass.

**Minimum closure condition:** Advisory only. The existing unit test is sufficient coverage.
**Next authorized action:** CA discretion on whether a behavioral contract test is warranted.
**Patched:** No — read-only scope.

---

## Patch Summary

**No patch applied.**

All six review questions were investigated:

1. `ProxyHandler({})` is sufficient — confirmed correct.
2. `_open_direct_http` seam preserves all required behaviors — confirmed correct.
3. The proxy test would fail under old code, pass under new — confirmed valid.
4. Non-claims, provenance, and packet metadata are not weakened — confirmed.
5. Proxy bypass not recorded in metadata — advisory design flag, off-scope for this patch boundary per the commission's patch-boundary clause.
6. Contract test gap — advisory, read-only scope, no patch authority.

No material bugs, false-success paths, or provenance drift were found in the editable scope.

---

## Unified Diff

```diff
(no changes)
```

---

## Validation Command and Observed Output

Command run (from `orca-harness/` working directory):

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests\unit\test_source_capture_direct_http.py tests\contract\test_source_capture_direct_http_contract.py tests\unit\test_reddit_old_http_batch.py tests\unit\test_reddit_batch_quality_summary.py
```

Observed output:

```text
............................                                             [100%]
```

28 tests passed. Exit code 0. No patch applied; this is the baseline confirmation run.

---

## Residual Risk

1. **Proxy-bypass metadata transparency** (Finding 5): Packets produced by the direct HTTP adapter do not declare that proxy bypass was in effect. This is a provenance-transparency gap, not a functional defect. It requires a CA-level schema or doctrine decision to close. Risk is low for correctness but advisory for auditability.

2. **No behavioral contract test** (Finding 6): The proxy-bypass guarantee is carried only by the unit test, not by a contract test. A structural regression (replacing `_open_direct_http` with `urlopen`) would pass the contract suite and might not be caught at the contract layer. Risk is low given the current codebase, but the safety net has one fewer strand.

3. **Import-time singleton** (Finding 4): `_NO_PROXY_OPENER` is built at module import time. This is correct and safe for the current handler set. If a future maintainer adds a stateful handler (cookie jar, etc.), the shared-state property becomes a latent hazard. Current risk is low.

No residual risk is identified for the core proxy isolation guarantee itself.

---

## Verdict

`NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`

The ambient-proxy isolation implementation is mechanically correct. `ProxyHandler({})` reliably suppresses environment-variable proxy selection. All original adapter behaviors are preserved through the `_open_direct_http` seam. The new unit test correctly discriminates old from new behavior. No non-claims or provenance fields are weakened. Two advisory design considerations (proxy-bypass metadata recording, contract-test gap) are flagged for CA discretion but are not defects and are off-scope for this patch boundary.

---

*Review boundary: findings are decision input only. They are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized by CA adjudication.*
