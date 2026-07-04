```yaml
retrieval_header_version: 1
artifact_role: proposed target architecture (non-authorizing) — creator-momentum pipeline
scope: >
  Target architecture for the Orca creator-momentum product: a 3-capability pipeline
  (discover -> deep-capture -> per-call curves) with a capture-satellite / derivation-core
  split. Defines the core/satellite boundary, the storage doctrine, the capture-shape
  contract (the one accepted lock-in + smallest next object), the ontology coupling, and
  placement. PROPOSED, pre-hardening: produced by a 3-perspective architecture pass
  (directional/adversarial/grounding), pending a de-correlated cross-vendor review + owner
  adoption. Not a build-go, validation, or readiness claim.
use_when:
  - Deciding how the IG capture satellite, the momentum-derivation core, and the ontology compose.
  - Scoping the capture-shape contract (the next build object) or any future platform satellite.
  - Checking what is core vs satellite, and what is deferred vs build-now.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_discovery_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - The ontology backbone is dispatched and Observation/TrendVector/SubNiche names/shapes land.
  - The capture-shape contract is specced + built (moves the next-object from proposed to built).
  - The carve-out is amended (the <=10 cap recorded) or the discovery-read posture is ruled.
  - A second platform satellite (TikTok/YouTube) is authorized (tests the agnostic seam).
status: PROPOSED — target architecture; cross-vendor review folded (AR-01..05 CA-adjudicated); capture-shape contract revised; owner adoption + gates pending
```

# Orca Creator-Momentum Pipeline — Target Architecture (PROPOSED, v0)

## Result

`TARGET_RECOMMENDED` — an **IG-specific capture-satellite → derivation-core** spine, with the
platform-agnostic generality **named but deferred**. The one decision worth making now is the
**capture-shape contract** (what each packet preserves), because history cannot be re-captured and
the current packet model has no typed home for the metrics. Everything else is rebuildable or
deferrable. This was reshaped away from a "platform-agnostic-now + hard-ontology-bound" proposal by
the adversarial and grounding perspectives (see *What reshaped it*).

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

## The capture-shape contract (smallest next object + the one accepted lock-in)

**This is the next thing to spec/build, and the only deliberate lock-in.** Each IG capture packet
must preserve, in a **stable parseable field** (not buried only in opaque hashed bytes), **per
metric: its value AND a typed availability posture** — `observed` / `unavailable_with_reason`
(private, blocked, rate-limited, metric-hidden) / `out_of_capture_window` / `not_attempted` (ride the
existing `VisibleFact` vocabulary). **A bare value is not enough** (AR-01, critical): absence, a
null, or a missing read must **never** be storable as if it were an observed `0`, or later momentum
curves cannot distinguish "no activity" from "not captured" — a fake-success path the kernel forbids,
and **irreversible** because history cannot be re-captured. The packet must also carry an explicit
**capture-coverage / window boundary** (which posts/period this capture claims to cover), so a gap is
visible as a gap. Field set: `numeric_id`, `follower_count`, `capture_time`, and per-post
`{shortcode, timestamp, view_count, like_count, comment_count}`, **each with its availability
posture**.

**These typed observation fields are the CANONICAL packet data** (AR-02): the rebuild path reads
them, **not** a future reparse. Raw bytes + the parser version are retained for **audit/provenance
only**, never as the primary rebuild dependency — so a drifting `og:description`/`web_profile_info`
shape can't threaten already-captured series. The current `SourceCaptureSlice`
(`orca-harness/source_capture/models.py`) carries `locator`, `timing`, postures, `limitations`,
`preserved_file_ids` — but **no typed metric field**; content lives inside the `PreservedFile` bytes.
So this typed observation field *is* the core/satellite contract and it does not exist yet.

## Ontology coupling — adapter, not hard-bind

The ontology (`AUTHORED_2026-06-13_AWAITING_DISPATCH`, declared HIGH lock-in) owns the vocabulary:
`Observation` (raw snapshot), `TrendVector` (derived trajectory), `SubNiche` (gating classifier).
**Core uses its own internal names and *maps* to the ontology through an adapter** — it does NOT
embed `Observation/TrendVector/SubNiche` as load-bearing types (they are *candidate* types that may
be renamed or folded into dimensions). The interim sub-niche keyword/cluster filter must **record
its raw drivers** (the keywords/graph edges that drove each assignment) so re-expression under the
ontology is deterministic, not a re-judgment.

## Placement

- IG capture satellite → `docs/product/source_capture_toolbox/` (clean; already holds the IG docs).
- Momentum-derivation **spec** → `docs/product/data_capture_spine/` — **NOT `core_spine/`** (naming
  collision: `core_spine/` is the decision-evidence Core Spine v0). `data_capture_spine/` already
  holds the LinkedIn influence-trajectory-watch analog (same shape).
- A new `creator_momentum/` lane would need a **recorded decision** (role-grammar change) — do not
  mint ad hoc.
- *(Placement claims are repo-verified against `.agents/workflow-overlay/artifact-folders.md` and the
  existing `data_capture_spine/` contents — not asserted; AR-05. The external reviewer could not check
  these, so they are cited here.)*

## Cross-cutting option decisions

- **Projection:** flat append file + on-demand pure derivations, written as a **spec** (defer the engine).
- **Sub-niche filter:** interim keyword/cluster + bridge-prune NOW (gating), recording raw drivers;
  forward-named to `SubNiche`. Stays in discovery/ontology, not absorbed into the momentum core.
- **Promotion:** pure-derivation; only an acted-on promotion becomes a durable ontology `DecisionEvent`.
- **Core scope:** IG-specific now; agnostic seams = band table + metric-availability + identity + content-unit + velocity-normalization, all **named but not built** (AR-04).

## Owner gates (preconditions, not architecture)

- **Discovery-read posture ruling** — hundreds of snowball reads vs the ≤10 capture cap (both source docs flag it OPEN).
- **Recorded ≤10 amendment** to `wind_caller_calibration_carveout_v0.md` (still reads ≤5; ≤10 is unrecorded intent).

## What reshaped it (the 4 decision-changing findings from the architecture pass)

1. The "thin interface" **does not exist** — `models.py` has no typed metric field; rebuildability is conditional on a frozen parser + versioned identity/conflict policy.
2. Forward-binding to the ontology → **downgrade to an adapter/mapping** (ontology is AWAITING_DISPATCH, HIGH lock-in, candidate types).
3. **"Platform-agnostic core" is premature** — the velocity layer is platform-shaped, and the carve-out forbids cross-platform now. IG-specific core with a named-deferred seam.
4. **Placement is not `core_spine/`** (naming collision) — derivation spec → `data_capture_spine/`.

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
