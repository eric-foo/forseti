# Weapon: Anti-Block HTTP Ladder (rung-0 / rung-1 / rung-3)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Source Capture Armory weapon — the cost-ordered anti-block HTTP capture ladder (rung-0 / rung-1 / rung-3).
use_when:
  - Capturing a public source body that may be behind a header/UA or JS-render block.
  - Checking what the anti-block ladder does, its rungs, and its honest limits.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/pipe_block_wall_escalation_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/armory_weapon_and_pipe_readme_templates_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md
stale_if:
  - A rung is added/removed or its build state changes.
  - The block_shell honesty classification or the rung-1 header profile changes.
```

- Purpose: retrieve a public source body, escalating cost-ordered only as far as a block forces.
- Rung / cost: rung-0 direct_http (honest baseline/control) → rung-1 anti_blocking_http (Chrome-like HTTP header profile; not browser-equivalent) → rung-3 browser_snapshot (rendered DOM, no raw bytes). [rung-2 curl_cffi gated/unbuilt; proxy/cloakbrowser are separate higher rungs.]
- Input → Output: one URL → SourceCapturePacket (CapturePacket) (response bytes + metadata; block_shell classification; honest access_posture).
- Built-in behavior (code-pole): rung-1 sends a Chrome-like HTTP header set by construction (UA Chrome/126 · Sec-CH-UA · Sec-Fetch-* · Accept-Encoding: identity). block_shell classifies every body (BLOCK_SHELL / EMPTY / encoded / uncertified); HTTP 200 is not recorded as certified source content.
- Boundaries / non-claims: same Python TLS; no JA3/browser-TLS impersonation; not proxy/session; not anti-detect; does not certify a body as real source content; rung-3 has no raw-body path (can't capture file bytes).
- Build status + ref: CA-verified 2026-06 — implemented + merged on `main` (source_capture/block_shell.py, source_capture/adapters/anti_blocking_http.py, the rung-0/1/3 runners, 2 unit tests); rung-3 browser_snapshot present on main + branch; Playwright 1.60 + Chromium installed.
- fires_via: node:source-fetch-access-mode (pre-fetch runner selection) · node:source-fetch-block-handling (post-block routing) — proposed cells, pending the data-capture binding's home.

## Non-claims

Descriptive armory page only — not validation, readiness, source-content certification, or a firing cell. Anti-block capability is bounded (see Boundaries) and demonstrated on limited evidence (see the pipe page and the anti-block ladder usage guide).
