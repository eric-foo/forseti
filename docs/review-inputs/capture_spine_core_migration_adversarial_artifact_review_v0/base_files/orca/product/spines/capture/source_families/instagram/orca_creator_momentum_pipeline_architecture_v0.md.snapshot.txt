```yaml
retrieval_header_version: 1
artifact_role: proposed target architecture (non-authorizing) — creator-momentum pipeline
scope: >
  Target architecture for the Orca creator-momentum product: a 3-capability pipeline
  (discover -> deep-capture -> per-call curves) with a capture-satellite / derivation-core
  split. Defines the core/satellite boundary, the storage doctrine, the capture-shape
  contract (core typed metric substrate landed; IG satellite/coverage pieces still
  deferred), the ontology coupling, and placement. PROPOSED, pre-hardening: produced by a
  3-perspective architecture pass
  (directional/adversarial/grounding), pending a de-correlated cross-vendor review + owner
  adoption. Not a build-go, validation, or readiness claim.
use_when:
  - Deciding how the IG capture satellite, the momentum-derivation core, and the ontology compose.
  - Scoping the remaining IG satellite producer, packet-level coverage claim, or any future platform satellite.
  - Checking what is core vs satellite, and what is deferred vs build-now.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_capture_findings_consolidated_v0.md
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - The ontology backbone is dispatched and Observation/TrendVector/SubNiche names/shapes land.
  - The remaining IG satellite producer / packet-level coverage contract lands.
  - The carve-out is amended again or the discovery-read posture changes.
  - A second platform satellite (TikTok/YouTube) is authorized (tests the agnostic seam).
status: PROPOSED — target architecture; cross-vendor review folded (AR-01..05 CA-adjudicated); core typed metric substrate landed; remaining IG satellite/coverage work, owner adoption, and hardening pending
```

# Orca Creator-Momentum Pipeline — Target Architecture (PROPOSED, v0)

## Result

`TARGET_RECOMMENDED` — an **IG-specific capture-satellite → derivation-core** spine, with the
platform-agnostic generality **named but deferred**. The original critical decision was the
**capture-shape contract** (what each packet preserves), because history cannot be re-captured. The
core typed metric-observation substrate now exists in `SourceCaptureSlice.metric_observations`; the
remaining non-rebuildable work is the IG satellite producer plus packet-level coverage, identity, and
conflict metadata. Everything else is rebuildable or deferrable. This was reshaped away from a
"platform-agnostic-now + hard-ontology-bound" proposal by the adversarial and grounding perspectives
(see *What reshaped it*).

## The pipeline + core/satellite boundary

Pipeline: **discover** (roster by sub-niche + follower band) → **deep-capture** (each creator's
window over time) → **per-call (Call) curves** (momentum, follower trajectory, tier/promotion).

- **Satellite (per-platform; IG first; `source_capture_toolbox/`):** discovery (snowball + sub-niche
  filter), deep-capture, and the **obligation** to record, per capture, `numeric_id +
  follower_count + capture_time + per-post {shortcode, timestamp, view_count, like_count,
  comment_count}` in a stable, parseable packet field. **All platform knowledge lives here.**
- **Core (IG-specific now; derivation **spec** in `data_capture_spine/`):** the series (a flat
  append file at this scale), tier (pure function of `follower_count` × band config), promotion
  (band-jump OR within-band velocity — pure derivation). **Named-but-deferred agnostic seams**
  (designed-for, NOT built) (AR-04): the band table **plus** metric-availability semantics, identity
  semantics, content-unit definition, and velocity normalization — these differ across
  IG/TikTok/YouTube, so naming them keeps real future optionality instead of smuggling IG assumptions
  into "core." The velocity/momentum layer is platform-scoped now.
- **Interface (the entire coupling):** one-way satellite → packet → core. The **only** write-back to
  durable state is an **acted-on** promotion → an ontology `DecisionEvent`. Tier/promotion state is
  never written back.

## Storage doctrine

- **Packets are the SOLE system of record** (raw bytes, provenance, the carve-out's retention unit).
- The **time-series projection is a derived, rebuildable index — never a second source of truth.**
- **Tier and promotion are derived (recomputable), never stored as state.** Storing a tier is the
  canonical violation.
- **Band thresholds live in exactly one reference config** (inline at this scale, ~10 lines).
- **No projection engine, no warehouse infra** — a flat SQLite/Parquet file. **PROVISIONAL,
  conditioned on the owner gates** (AR-03): the choice holds at the *recorded* cap (≤5) and the
  floated ≤10 alike (both ≈ sub-million rows over 10yr), but it is **not** justified by the unrecorded
  ≤10 intent; if the discovery-read posture or the cap changes materially, re-evaluate. Write the
  derivation as a **spec, not a runtime**, until there is captured data to derive over.
- **Rebuildability rests on the typed observed fields, not on reparsing** (AR-02): the
  projection/tiers/promotions rebuild from the **canonical typed observation fields** in the packets
  (above) + a **versioned identity- + conflict-resolution policy** (username is mutable; the stable
  key is the numeric `id`; `re_capture_relationship: conflict` is a real packet value). Raw bytes and
  the parser version are audit/provenance, **not** the rebuild path. Untyped fields, or an unversioned
  identity/conflict policy, make "rebuildable" dishonest.

## The capture-shape contract (core substrate landed; remaining IG lock-in)

The contract is no longer entirely next-build: `MetricObservation`, `MetricPosture`,
`CoverageWindow`, and `SourceCaptureSlice.metric_observations` now provide the core packet substrate.
The remaining deliberate lock-in is the **IG satellite producer and packet-level coverage contract**.
Each IG capture packet must preserve, in a **stable parseable field** (not buried only in opaque
hashed bytes), **per metric: its value AND a typed availability posture** — `observed` /
`unavailable_with_reason` (private, blocked, rate-limited, metric-hidden) /
`out_of_capture_window` / `not_attempted` / `not_applicable`. **A bare value is not enough** (AR-01,
critical): absence, a null, or a missing read must **never** be storable as if it were an observed
`0`, or later momentum curves cannot distinguish "no activity" from "not captured" — a fake-success
path the kernel forbids, and **irreversible** because history cannot be re-captured. The IG producer
must also carry an explicit **capture-coverage / window boundary** (which posts/period this capture
claims to cover), so a gap is visible as a gap. Field set: `numeric_id`, `follower_count`,
`capture_time`, and per-post `{shortcode, timestamp, view_count, like_count, comment_count}`, **each
with its availability posture**.

**These typed observation fields are the CANONICAL packet data** (AR-02): the rebuild path reads
them, **not** a future reparse. Raw bytes + the parser version are retained for **audit/provenance
only**, never as the primary rebuild dependency — so a drifting `og:description`/`web_profile_info`
shape can't threaten already-captured series. The current `SourceCaptureSlice`
(`orca-harness/source_capture/models.py`) carries `locator`, `timing`, postures, `limitations`,
`preserved_file_ids`, and `metric_observations`. That lands the platform-agnostic core substrate, but
does **not** close the IG-specific contract: the satellite producer still has to emit the closed IG
metric vocabulary, enforce count semantics such as non-negative values, pin numeric-ID identity and
conflict-policy versions, and make the packet-level coverage claim explicit.

## Ontology coupling — adapter, not hard-bind

The ontology (`AUTHORED_2026-06-13_AWAITING_DISPATCH`, declared HIGH lock-in) owns the vocabulary:
`Observation` (raw snapshot), `TrendVector` (derived trajectory), `SubNiche` (gating classifier).
**Core uses its own internal names and *maps* to the ontology through an adapter** — it does NOT
embed `Observation/TrendVector/SubNiche` as load-bearing types (they are *candidate* types that may
be renamed or folded into dimensions). The interim sub-niche keyword/cluster filter must **record
its raw drivers** (the keywords/graph edges that drove each assignment) so re-expression under the
ontology is deterministic, not a re-judgment.

## Placement

- IG creator-momentum product docs now live under the spine-first product tree, with this family at
  `orca/product/spines/capture/source_families/instagram/`.
- Source Capture Armory / toolbox-level routing lives under
  `orca/product/spines/capture/source_capture_toolbox/`; implementation and projection helpers live
  in `orca-harness/source_capture/` and `orca-harness/runners/`.
- A new durable `creator_momentum/` lane would still need a **recorded decision** (role-grammar
  change) — do not mint ad hoc.
- Retired `docs/product/...` body references are historical after the spine-first migration; current
  placement resolves through `.agents/workflow-overlay/artifact-folders.md`, `docs/workflows/`, and
  the spine-first moved-paths index when provenance needs it.

## Cross-cutting option decisions

- **Projection:** flat append file + on-demand pure derivations, written as a **spec** (defer the engine).
- **Sub-niche filter:** interim keyword/cluster + bridge-prune NOW (gating), recording raw drivers;
  forward-named to `SubNiche`. Stays in discovery/ontology, not absorbed into the momentum core.
- **Promotion:** pure-derivation; only an acted-on promotion becomes a durable ontology `DecisionEvent`.
- **Core scope:** IG-specific now; agnostic seams = band table + metric-availability + identity + content-unit + velocity-normalization, all **named but not built** (AR-04).

## Owner gates and current boundaries (preconditions, not architecture)

- **Owner adoption / hardening of this proposed target architecture** remains pending.
- **Actual discovery or capture execution** still needs its own owner-gated run scope; this document
  is not live IG capture, a scheduler, standing crawler, production store, or commercial-scale
  collection authorization.
- The 2026-06-15 carve-out amendment resolved the old cap ambiguity: the ceiling counts Orca's own
  operating/capture accounts (≤10 ceiling; operations start ≤5), not subject creators; the subject
  roster is all-in-vertical/uncapped under the active-attended posture.

## What reshaped it (the 4 decision-changing findings from the architecture pass)

1. The "thin interface" **did not exist at architecture-pass time**; `models.py` now has the core typed metric field, so rebuildability is conditional on the IG satellite producer plus versioned identity/conflict and packet-level coverage policy.
2. Forward-binding to the ontology → **downgrade to an adapter/mapping** (ontology is AWAITING_DISPATCH, HIGH lock-in, candidate types).
3. **"Platform-agnostic core" is premature** — the velocity layer is platform-shaped, and the carve-out forbids cross-platform now. IG-specific core with a named-deferred seam.
4. **Placement is not `core_spine/`** (naming collision) — current product placement is the spine-first `orca/product/` capture tree, not retired `docs/product/...` homes.

## Cross-vendor review disposition (2026-06-15)

Hardened by a de-correlated **OpenAI-lineage** `no_repo` advisory review (cross-vendor discovery bar
satisfied), CA-adjudicated: **AR-01 (critical, coverage/availability) ACCEPTED** → typed availability
posture + coverage boundary now required; **AR-02 (major, rebuildability) ACCEPTED** → typed fields
canonical, parser = provenance; **AR-03 (major, scale-before-gates) ACCEPTED** → storage choice
marked provisional; **AR-04 (major, narrow seam) ACCEPTED** → deferred seams named; **AR-05 (minor,
placement) MODIFIED** → claims repo-verified + cited. The reviewer's `NEEDS_ARCHITECTURE_PASS` is
accepted **scoped to the capture-shape contract** (revised above); the overall spine is unchanged.

## Non-claims

PROPOSED target architecture only — not a build-go, validation, readiness, acceptance, or
commercial/legal authorization. It has had a 3-perspective same-vendor architecture pass + one
de-correlated cross-vendor advisory review (above), CA-adjudicated — **advisory input, not a formal
verdict or owner adoption.** Ontology names are forward references to a not-yet-dispatched ontology.
