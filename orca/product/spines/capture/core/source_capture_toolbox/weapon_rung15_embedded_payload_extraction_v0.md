# Weapon: Rung-1.5 Embedded-Payload Extraction (browser-free)

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Source Capture Armory weapon — rung-1.5 browser-free recovery of a structured data payload a JS-hydrated SPA embeds, over the rung-1 anti-block HTTP path. Source-agnostic spine PRIMITIVES; OpenAI price = the only live adapter.
use_when:
  - A source renders the data you want client-side, so a plain rung-1 body shows an empty shell, but the payload is actually EMBEDDED (in the page hydration stream and/or a linked JS-module chunk), not behind an XHR/auth wall.
  - You need that payload WITHOUT a headless browser (rung-3), and without hand-parsing rendered HTML.
  - Checking what this rung does, its reusable surface, and its honest limits before reaching for it.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/pipe_block_wall_escalation_v0.md
stale_if:
  - The spine surface (extract_object_at_anchor / certify_payload / PayloadBody) changes signature or guarantees.
  - The certification invariants (a 200 is never certified content; internal-consistency, not truth; encoded body refuses) change.
  - A second adapter lands and the general/per-source seam moves.
```

- Purpose: recover a structured data payload that a JS-hydrated page embeds, browser-free, over rung-1 — escalate to rung-3 (browser) only if the payload is genuinely render-time-only. It sits BETWEEN rung-1 (anti-block HTTP, no JS) and rung-3 (browser_snapshot).
- Rung / cost: rung-0 direct_http → rung-1 anti_blocking_http → **rung-1.5 embedded-payload extraction (this)** → rung-3 browser_snapshot. Same fetch + `block_shell` as rung-1; the added work is structured-payload PARSING, not heavier access.
- Input → Output: a URL (or page text already captured at rung-1) → the embedded object(s), plus a certification verdict over the recorded provenance. Output is the payload, NOT a rendered DOM.
- **The extracted spine primitives are source-agnostic; OpenAI pricing is still the only live adapter.** OpenAI ChatGPT pricing (`run_source_capture_price_payload_packet.py`) is adapter #1: it reads the React Router v7 hydration turbo-stream (tier structure) and a static `prices:{"chatgpt.` object in a linked JS-module chunk (amounts), joined by priceToken. "It shouldn't always just be a price checker" — the reusable primitive layer isn't, but OpenAI pricing is still the only live adapter built on it (source-agnosticism is demonstrated at the primitive/unit-test level, not yet on a second live source).

## Reusable surface (what another agent calls)

In `source_capture/price_payload_extraction.py`:

- `extract_object_at_anchor(text, anchor) -> dict` — recover a brace-delimited JS object literal that begins at a caller-supplied content anchor (regex/pattern); JS unquoted keys quoted, parsed as JSON; **raises on an absent/unparseable object (loud miss, never a silent empty)**.
- `certify_payload(*, bodies, payload_parsed, domain_checks, discriminator, discriminator_note=None, payload_check_name=…, payload_check_detail=…) -> CertificationVerdict` — the certification scaffold. `certified` ⇔ at least one `PayloadBody` is present and every one is 2xx + not a block/empty shell + INSPECTABLE (not an undecoded/encoded body), the payload parsed, and at least one caller-supplied `domain_checks` entry is present and all passed (no vacuous pass on empty bodies/checks). Carries NO price/vendor semantics.
- `PayloadBody(label, block_class, status, block_signal, detail_label=None)` — one fetched body; `label` namespaces its checks; `detail_label` preserves a legacy serialized detail label.
- `decode_react_router_stream(html) -> object graph` — a framework decoder (React Router v7), reusable by any RRv7 source. (A Next.js `self.__next_f` decoder exists alongside it for the announcement path — proof the framework-decode layer is plural/swappable, not a universal core.)

## What is general vs what a new source must supply

- **General (the spine, reuse as-is):** rung-1 fetch + `block_shell`; locate the object at a content anchor (`extract_object_at_anchor`); the certification scaffold (`certify_payload`) and its honesty invariants; loud-failure + per-attempt evidence; retry-only-transient discipline.
- **Per-framework (an adapter, reusable across that framework):** the hydration-stream decoder (RRv7 / Next.js / …).
- **Per-source (a thin adapter):** the schema parse — which objects/typenames in the decoded graph carry the data (e.g. OpenAI's `chatGPTPricingCard`).
- **Per-domain (a predicate):** the `domain_checks` that make the payload internally consistent for its meaning (e.g. price token-coherence + amount plausibility).

To use this rung on a new source: pick the anchor, write the schema parse, write the domain checks, pass them to the spine. No framework/registry is required (deliberately deferred — see Non-claims).

## Invariants (carry into any adapter)

- A 200 is never certified as content on its own; `block_shell` is never weakened.
- "Certified" asserts INTERNAL CONSISTENCY of the payload as served at capture-time — NOT freshness, NOT completeness, NOT truth. Freshness headers are recorded as provenance, not gated.
- A miss fails loud (no fake-empty). Retry only TRANSIENT misses (a degraded/thin page that heals on re-fetch); a full page genuinely missing the payload is a likely vendor change → fail loud immediately, do not retry-mask it.

- Build status + ref: implemented on lane `capture-rung15-openai-payload` (the post-`2d8e19e` "isolate, don't abstract" pass — generic spine separated from the OpenAI price adapter). **NOT merged to main.** Reuse is demonstrated by a unit test on a non-price toy payload (`tests/unit/test_embedded_payload_spine.py`), **not yet on a second live source.** The OpenAI price path is behaviour-preserved (certification artifact byte-stable; runner untouched).
- fires_via: same anti-block path as the rung ladder; runner selection is the operator's (no firing-cell binding claimed here).

## Non-claims

Descriptive armory page only — not validation, readiness, source-content certification, or a firing cell. This rung proves fetch + parse + certify-internal-consistency on real data only; it does not prove freshness, completeness, feed quality, product-fit, or unattended reliability. The source-agnostic claim is demonstrated on the spine primitives (one non-price test), NOT on a second live source — a multi-source decoder registry / source-config framework is deliberately DEFERRED until a real second target justifies the seam.
