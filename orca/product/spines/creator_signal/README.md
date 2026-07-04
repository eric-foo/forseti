# Creator Signal Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door (Creator Signal product/signal spine)
scope: >
  Front-door for the Creator Signal spine: the product-facing interpretation and
  presentation layer for creator intelligence, including creator profile surface
  contracts, operator/buyer information architecture, claim language, freshness,
  limitation display, and source drill-back over Capture-owned creator records.
use_when:
  - Entering the Creator Signal spine or deciding whether a creator-intelligence surface is Creator Signal-owned.
  - Checking how a current creator profile may be shown to an Orca operator or buyer.
  - Distinguishing product interpretation from Capture identity, metrics, audience inference, storage, and runtime work.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
stale_if:
  - The Creator Signal spine identity or product_signal kind is amended.
  - The creator intelligence profile surface is superseded.
  - Capture current-view, identity, metric rollup, or ideal-audience ownership changes.
```

## What this spine is

Creator Signal is the high-level product/signal spine for the **creator
intelligence product surface**. It answers: when Orca opens a creator, what should
an operator or buyer see, what can the surface claim, and what limits must stay
visible?

It consumes the low-level Capture current view; it does not replace it.

- **Consumes:** public-handle identity linkage, platform account links, metric
  observations, metric rollups, ideal-audience snapshots, freshness fields, and
  source pointers.
- **Owns:** product-facing layout, grouping, claim language, limitation display,
  freshness display, and source drill-back expectations.
- **Does not own:** identity ledger rows, metric computation, audience inference
  schemas, SQLite/data-lake storage, live capture, source access, outreach,
  contact enrichment, lead lists, public directories, or dashboard runtime code.

Binding authority:
`docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md`.

## Current artifacts

| Path | Role |
| --- | --- |
| `creator_intelligence_profile_surface_v0.md` | First product surface contract for the one-stop creator intelligence profile. |
| `creator_signal_product_architecture_v0.md` | Pre-ratification product architecture plan for the Creator Signal carve-out and Vetting v0 first increment. |
| `creator_signal_market_sizing_v0.md` | Internal rough TAM/SAM/SOM market-sizing estimate for the Creator Signal carve-out (not demand validation or buyer proof). |
| `creator_signal_multi_creator_library_surface_v0.md` | Product-facing display contract for the multi-creator Creator Signal Library surface. |
| `creator_signal_multi_creator_library_static_projection_v0.md` | Static, source-backed Markdown projection of the Creator Signal Library over committed creator_profile_current rows. |
| `creator_signal_multi_creator_library_client_projection_v0.md` | Client-readable static projection of the Creator Signal Library with audit detail one click away. |

No subfolders are bound yet. Add folders only when a concrete artifact needs one
and update the binding/route surfaces at the same time.

## Boundary summary

Capture owns the current view and record mechanics. Creator Signal owns how that
view becomes a product experience.

The spine must inherit the Capture `Dashboard Boundary`: no contact/outreach, no
lead-list export, no public person-level directory, no legal-name/person-identity
proof, no follower graph, no actual-audience demographics without a later schema
and data gate, and no unstamped/sourceless/LLM-only influence claims.

## Non-claims

This spine front-door is not validation, readiness, buyer proof, runtime
implementation, SQLite adoption, a data-lake job, live capture authorization, a
dashboard build, outreach authorization, or a public creator directory.
