# Demand-Durability Multi-Retailer Rendered Capture — Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Product spec (commission input to the capture-spine lane; what-must-be-true, not a build)
scope: >
  Stabilizes what the capture-spine lane must settle so the demand-durability cadence runner can
  capture the SAME SKU across multiple retailers (Ulta, Amazon, Sephora, …) — which the current
  direct_http-only path cannot reach. Specifies the required behavior, the per-retailer source-access
  posture (rendered capture + measured-ToS, NOT paid entitlement), the comparability shape, and the
  non-goals. It is the resolution of the assumption-gate block, not the build.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/README.md                                   # the Armory (rendered adapters)
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md                   # Sephora/Ulta recon (worktree, pending-merge); no Amazon recon
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md               # the capture PLAYBOOK (probe-then-pin, recon procedure) — USE IT to assess each retailer
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md   # anti-block ladder (direct_http -> anti_blocking_http -> visible browser -> cloakbrowser+proxy)
  - orca/product/spines/capture/core/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md
  - orca/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md   # Ob.6 fidelity, Ob.17 durability facts
  - orca-harness/runners/run_source_capture_durability_series.py                    # the step-3 cadence runner (the consumer)
stale_if:
  - The source-access boundary decision changes hard stops or the measured-ToS posture.
  - The cadence runner's writer-invocation seam changes.
  - A retailer's recon verdict (GO/PARTIAL/NO-GO) lands or changes.
  - The Armory rendered (CloakBrowser) adapter set changes.
```

## Status

- Status: `SPEC_V0` — commissioned to the **capture-spine lane to settle**. This is a what-must-be-true spec, not an architecture, route, or build. The capture-spine lane owns the architecture + build under its own scoping.
- Trigger: the assumption gate (`BLOCKED_ASSUMPTION_UNVERIFIABLE`) found the multi-retailer live run bakes in a rendered-capture capability the built `direct_http` machinery does not have. Owner authorized settling it (2026-06-15).
- Owner authorization (2026-06-15): settle the multi-retailer rendered retail capture for the demand-durability series. Implementation by the capture-spine lane is authorized within the boundary + no-gate-defeat; **landing to `main` stays owner-gated.**

## Why (the gap this closes)

The step-3 cadence runner invokes the step-2 `direct_http` writer (stdlib urllib) per slot. Retail PDPs serve the price/review substrate via JS / embedded-JSON, so `direct_http` cannot read them: recon shows **Sephora** = progressive-scroll + the **Bazaarvoice** API, **Ulta** = `__APOLLO_STATE__` embedded-JSON (both rendered, via CloakBrowser), with that recon **worktree-resident (unmerged)**, and **Amazon has no recon at all**. The series can only span retailers once a rendered capture path exists, is wired to the runner, and each retailer's posture is settled.

## Required behavior (what must be true when this is settled)

1. **Same packet shape, per retailer.** Each authorized retailer is captured into the **same `SourceCapturePacket` (CapturePacket)** the `direct_http` path produces — the Ob.6 fidelity dimensions and the Ob.17 durability fields (Element 1 pins, Element 2 series origin, Element 4 cadence) are populated as first-class schema fields, so the cadence runner treats a rendered observation identically to a `direct_http` one.
2. **Wired to the cadence runner's existing seam.** The runner already accepts an injectable `writer_main` (it defaults to the `direct_http` writer). The rendered path must be a writer with the **same interface** so the runner can invoke it per slot per retailer — no re-architecture of the runner, no schema change, no `SOURCE_CAPTURE_MANIFEST_VERSION` bump.
3. **Substrate-first, per retailer** (recon pattern 2 — locate the signal substrate, then pick the tool): Sephora → Bazaarvoice + progressive scroll; Ulta → `__APOLLO_STATE__` embedded-JSON; Amazon → recon-then-decide. Capture must preserve the source bytes/structure (verbatim-vs-paraphrase axis), not a paraphrase.
4. **Source-access posture recorded per retailer — public + measured-ToS, NOT entitlement.** These are public pages (no paid account); the gate is the **measured-ToS / honest-anti-blocking** posture (real browser context, low-volume, posture-tagged) under the source-access boundary. **No-gate-defeat: STOP at any auth / CAPTCHA / Cloudflare *challenge*** and record the limitation. Per recon pattern 1, a first "blocked" is a hypothesis — escalate the interaction (real browser → user-action → progressive scroll → proxy/geo) and re-probe before recording NO-GO. Amazon's ToS posture is the most restrictive on automation and must be recorded explicitly (measured pre-commercial; commercial scale routes through a provider, not Orca's own path).
5. **Comparability = one series PER retailer** (resolves the gate's A3). Each retailer is its own `series_id` with its own pins (locale/currency/variant for that storefront); the same SKU across retailers is a **set of parallel per-retailer series compared downstream**, never one `series_id` spanning retailers (which would conflate distinct price/availability/review semantics).
6. **Per-retailer recon settled — via the existing capture playbook, not invented.** The capture **playbook** + anti-block **ladder** + recon **index** are the assessment tools; use them. Sephora (`GO` via scroll + Bazaarvoice) and Ulta (`__APOLLO_STATE__` embedded-JSON) are **already recon'd** (worktree-resident, pending-merge) — consume + merge them, do not re-probe. **Amazon** is the only un-assessed retailer — run the playbook's ladder (probe-then-pin; escalate-and-re-probe before NO-GO) and author an honest **GO / PARTIAL / NO-GO** verdict (NO-GO is a first-class, successful diagnosis — recon pattern 5).

## Non-goals (explicit)

- **Not** the single-source SdJ `direct_http` series — that runs now, in parallel, unchanged.
- **Not** series-diff (Element 3) — still deferred.
- **Not** industrial / unbounded scraping — bounded, measured, commissioned-series volume only.
- **Not** commercial-scale capture — at scale, ToS-risky access routes through a commercial data provider (the existing posture), not Orca's own browser path.
- **Not** ECR / Cleaning / Judgment, source-quality scoring, or any demand verdict (INV-1 — capture records observed facts + limits only).
- **Not** a new schema, manifest bump, or change to the cadence runner's state model.

## Acceptance signal (how "settled" is recognized)

Each **authorized** retailer produces a valid durability-series observation packet (Ob.17 fields set) via the rendered path, invoked by the cadence runner through the existing writer seam, with the per-retailer ToS posture + recon verdict recorded; gap≠no-change honored; no gate defeated; one-series-per-retailer shape. A retailer that recons NO-GO/PARTIAL is recorded as such (an honest outcome), not forced.

## Open questions for the capture-spine lane (to settle)

- **Amazon GO/PARTIAL/NO-GO** — needs recon under the boundary (the hardest anti-bot + ToS case). NO-GO is acceptable.
- **Adapter shape** — per-retailer adapters vs one generic rendered+embedded-JSON extractor behind the writer interface (smallest-complete call).
- **Source-access tooling authorization tranche** — whether a retail rendered adapter sits in the existing CloakBrowser tranche or needs a named addition (owner-gated).
- **Storefront/locale** — which storefront per retailer (US vs UK) fixes the currency/locale pins and cross-series comparability.
```
