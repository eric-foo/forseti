# Direct HTTP No-Proxy Isolation Delegated Adversarial Code Review-And-Patch Prompt v0

## Commission

You are the de-correlated controller for a bounded adversarial code review-and-patch pass. The author/home model family is OpenAI/Codex. The controller must be a different vendor or family. This is a who-constraint, not a model recommendation.

Your task is to review and, only if needed, patch the direct HTTP ambient-proxy isolation change. Your output is decision input for CA adjudication; it is not approval, readiness, or auto-keep authority.

## Required Method Sequence

1. Read this prompt.
2. REFERENCE-LOAD `workflow-deep-thinking`.
3. REFERENCE-LOAD `workflow-code-review`.
4. Do not APPLY either method yet.
5. SOURCE-LOAD the target files and required context below.
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
7. APPLY `workflow-deep-thinking` to frame the highest-risk failure modes.
8. APPLY `workflow-code-review` to review the implementation.
9. If a bounded fix is needed, patch only the submitted scope.
10. Fresh-read the changed target files and rerun the required validation.
11. Return findings first, then patch summary, diff, validation evidence, residual risk, and verdict.

## Source Context

Required reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/review-lanes.md`
- `orca-harness/source_capture/adapters/direct_http.py`
- `orca-harness/tests/unit/test_source_capture_direct_http.py`
- `orca-harness/tests/contract/test_source_capture_direct_http_contract.py`
- `orca-harness/runners/run_source_capture_http_packet.py`
- `orca-harness/runners/run_reddit_old_http_batch.py`
- `orca-harness/runners/run_reddit_batch_quality_summary.py`

Optional context if needed:

- `orca-harness/tests/unit/test_reddit_old_http_batch.py`
- `orca-harness/tests/unit/test_reddit_batch_quality_summary.py`

## Observed Implementation Context

The live Reddit batch initially failed all 9 slots with `[WinError 10061]` because the shell environment had:

- `HTTP_PROXY=http://127.0.0.1:9`
- `HTTPS_PROXY=http://127.0.0.1:9`
- `ALL_PROXY=http://127.0.0.1:9`

That contradicted the direct HTTP lane's provenance/non-claim posture because the lane claimed no proxy use while urllib could still honor ambient proxy settings.

The current patch changes `direct_http.py` to use a no-proxy opener:

- imports `ProxyHandler`, `Request`, and `build_opener`;
- creates `_NO_PROXY_OPENER = build_opener(ProxyHandler({}))`;
- routes fetches through `_open_direct_http(...)`;
- leaves direct HTTP as stdlib urllib, no browser, no scraper framework, no session injection, and no explicit proxy support.

The current test patch:

- changes timeout/network monkeypatches to target `_open_direct_http`;
- adds `test_fetch_direct_http_capture_ignores_ambient_proxy_env`, which sets `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and empty `NO_PROXY`, then verifies local direct HTTP still succeeds.

Validation observed before this review commission:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q orca-harness\tests\unit\test_source_capture_direct_http.py orca-harness\tests\contract\test_source_capture_direct_http_contract.py orca-harness\tests\unit\test_reddit_old_http_batch.py orca-harness\tests\unit\test_reddit_batch_quality_summary.py
```

Observed output:

```text
............................                                             [100%]
```

## Review Target

Editable scope:

- `orca-harness/source_capture/adapters/direct_http.py`
- `orca-harness/tests/unit/test_source_capture_direct_http.py`

Read-only context:

- all other files.

Do not edit:

- batch proof outputs under `orca-harness/_test_runs/`;
- prompt artifacts;
- docs;
- proxy profile code;
- CloakBrowser code;
- Reddit parser/consolidation code;
- candidate intake, monitoring, crawler, archive, or commercial API code.

## Review Questions

Find material bugs, false-success paths, or provenance drift in the current patch. Focus especially on:

1. Whether `ProxyHandler({})` is sufficient to prevent urllib from honoring ambient proxy environment variables for the direct HTTP lane.
2. Whether the new `_open_direct_http` seam preserves timeout, HTTPError, URLError, redirect, size cap, and non-2xx body behavior.
3. Whether the test actually would fail under the old implementation and pass under the new one.
4. Whether the patch accidentally weakens non-claims, provenance, or packet metadata.
5. Whether any warning/metadata should record that ambient proxy env was ignored without storing secret-bearing values.
6. Whether review should flag a design-level issue instead of patching.

## Patch Boundary

If you patch, keep it to the editable scope. Patch only defects that materially affect the ambient-proxy isolation behavior, its tests, or directly adjacent failure classification. Do not refactor unrelated adapter structure.

If the correct fix requires changing packet schema, source-capture provenance doctrine, proxy profile policy, or Reddit batch runner behavior, return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding instead of patching those files.

## Required Validation

Run this exact focused slice after any patch, or state why it could not be run:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q orca-harness\tests\unit\test_source_capture_direct_http.py orca-harness\tests\contract\test_source_capture_direct_http_contract.py orca-harness\tests\unit\test_reddit_old_http_batch.py orca-harness\tests\unit\test_reddit_batch_quality_summary.py
```

Do not perform live Reddit network access.

## Output Path

Write the review result to:

`docs/review-outputs/direct_http_no_proxy_delegated_adversarial_code_review_patch_v0.md`

## Output Contract

Return:

1. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
2. Findings first, ordered by severity.
3. For each finding: affected file/line, evidence, risk, minimum closure condition, and whether you patched it.
4. Patch summary, if any.
5. Unified diff.
6. Validation command and observed output, or not-run reason.
7. Residual risk.
8. Verdict: `PATCHED_FOR_CA_ADJUDICATION`, `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, or `BLOCKED`.

Reminder: your diff and verdict are claims to adjudicate, not premises to inherit. CA/home model decides what is kept.
