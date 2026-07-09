# Pipe: Block-Wall Escalation

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Source Capture Armory pipe (cross-cutting access route) — the cheap-ladder + less-walled-surface options used when a capture returns a block signature.
use_when:
  - A capture returns a block signature and you need the routing options before declaring "blocked".
  - Checking what the block-wall escalation pipe targets and its honest limits.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/armory_weapon_and_pipe_readme_templates_v0.md
stale_if:
  - The rung set or the less-walled-surface examples change.
  - The post-block-handling cell or its node id changes.
```

- Principle: provide the cheap escalation path + less-walled-surface options used when the block-handling guard fires.
- Wall-signature it targets: observed UA/header-keyed blocks where request identity changes the response (generic "Python-urllib" UA → 403; browser-like UA → HTTP 200, still uncertified). Also where a JS-heavy front surface has a server-rendered / less-walled sibling (old.reddit.com vs www.reddit.com; developers.openai.com vs openai.com).
- Pairs with: rung-1 for UA/header walls; rung-3 for JS-rendered content; rung-0/1 against the less-walled sibling.
- Applies / doesn't: applies when the wall is UA/header-keyed or a less-walled surface exists. Does NOT beat JS-challenge / Turnstile bot-detection (→ rung-3, then gated cloakbrowser/proxy), IP/rate blocks, or login/entitlement gates — never *bypass* an unentitled gate (hard line); entitled access via our own account is a separate authenticated path, not this pipe.
- Honest limits: verified on one site at one moment (the OpenAI UA-gate); Cloudflare can still challenge on IP/rate/edge even with a browser UA; container-level retrieval ≠ content authenticity.
- fires_via: node:source-fetch-block-handling (post-block routing) — proposed cell, pending the data-capture binding's home.

## Non-claims

Descriptive armory page only — not validation, readiness, a general anti-block guarantee, or a firing cell. The "what to do on a block" rule lives in the post-block-handling cell, not here.
