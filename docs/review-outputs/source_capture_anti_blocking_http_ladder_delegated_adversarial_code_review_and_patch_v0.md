# Anti-Blocking HTTP Ladder (rung-1) — Delegated Review-and-Patch: CA Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review-output (delegated review-and-patch adjudication record)
scope: >
  Home-model (CA) adjudication of the de-correlated delegated review-and-patch
  pass on the rung-1 anti-blocking HTTP capture slice (honesty surface).
use_when:
  - Checking what the delegated review found and what the CA kept.
authority_boundary: retrieval_only
```

## Commission

- Prompt: `docs/prompts/reviews/source_capture_anti_blocking_http_ladder_delegated_adversarial_code_review_and_patch_prompt_v0.md`
  (sha256 `8665C79FD303FB175240A88D1AB150F8E8CB607ECE9979BFEB6994F2CFC89926`).
- Target: anti-block HTTP slice (honesty surface), worktree branch `feat/anti-block-http-ladder`, base HEAD `7be0866`.
- De-correlation: **satisfied** — delegate reported a non-Claude / non-Opus family; author/home is Claude, Opus-class. Who-constraint only; no runtime-model claim.
- Lane: provisional delegated review-and-patch convention (`.agents/workflow-overlay/delegated-review-patch.md`). **Decision-input only** — not validation, not readiness, not a formal review verdict.

## Delegate result (claims adjudicated, not inherited)

- Verdict: "bounded patch applied; decision input only." Three `major` findings: block_shell false-negative gaps; encoded-response laundering; empty/encoded slice+capture honesty.
- Bounded working-tree edits to `block_shell.py`, `anti_blocking_http.py`, `run_source_capture_antiblock_http_packet.py`, `test_block_shell.py`, `test_anti_blocking_http_adapter.py`. No off-scope edits.
- Residual (delegate): signature-based detection cannot certify source content or catch every novel shell; TLS/JA3, proxy, JS-challenge, decoded-body inspection remain outside rung-1.

## CA adjudication: ACCEPT IN FULL

Read the true on-disk state of every changed file and evaluated against the anchor (honest representation over "make the 403 disappear") and doctrine bounds.

- `block_shell.py` — **accept.** `latin-1` scan decode (stops `utf-8 errors=ignore` from silently dropping marker bytes); scan window `8192 -> 65536`; broadened high-confidence WAF/bot-wall body + header signatures; `encoded_body_uninspectable` short-circuit (compressed bodies flagged uninspectable rather than scanned as garbage). All changes are safe-direction (under-claim + preserve + flag); no positive `CONTENT` class introduced.
- `anti_blocking_http.py` — **accept.** `encoded_response_body` limitation when the server returns a non-identity `Content-Encoding`. **Contract note:** empty-body changed from a `NO_BODY` failure to a Success the runner records as an empty-body limited capture — diverges from `direct_http` parity, accepted on honest-artifact grounds. `NO_BODY` enum member now vestigial (left as-is; trivial).
- `run_source_capture_antiblock_http_packet.py` — **accept.** Added the `encoded_body_uninspectable` posture branch; honest mapping intact (a `200` is never recorded as captured content); limitations surfaced at both slice and capture level.
- tests — **accept.** New pins for WAF markers, scan depth past the old 8192 prefix, encoded-body limitation, and runner-level slice+capture propagation.

No hunks rejected or modified.

## Independent validation (CA-observed, not relayed)

- Full `tests/` suite (worktree, in isolation): **243 passed, 1 skipped, exit 0** — was 237 pre-patch (+6 delegate tests, zero regressions).
- Delegate-reported "197 passed" reconciled: `tests/unit`-only scope (CA reran `tests/unit` and observed 197).

## Residuals (accepted; live-run-observable)

- Broadest signature is `"reference #"` (Akamai-style) — small false-positive surface; safe-direction (misflag preserves body + records an auditable signal). Watch in live runs; tighten only if it misflags real content.
- Rung-1 honest limits unchanged: no TLS/JA3, no proxy, no JS-challenge, no decoded-body inspection. These are later rungs.

## Non-claims

- Not validation, not readiness, not a formal review verdict, not fixture admission.
- Does not certify any returned body as real source content.
- The arm has not yet met a live `403`; lowest-sufficient-rung determination remains the gated live run.
