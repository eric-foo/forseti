# Aphrodite Derived-Claim Provenance Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product contract (Creator Signal display/claim-language rule for derived claims)
scope: >
  The provenance contract every DERIVED creator claim must satisfy before it may
  be shown on any Creator Signal / Aphrodite surface. A derived claim is a fact
  about a creator produced by inference or extraction over captured content
  (transcripts, comments) — e.g. a fit label, an ad-reception read, an
  aggregate purchase-intent signal, a segment-share number — as distinct from a
  directly-observed metric (view count, follower count). This contract extends
  the existing per-number / claim-object provenance discipline from observed
  metrics to derived ones. It owns the claim-language and source-drill-back RULE
  (a Creator Signal-owned surface concern); it does not own, design, or
  authorize the extraction recipe, the capture, the model choice, or the
  physical storage schema.
use_when:
  - Designing or reviewing any Creator Signal surface that shows a derived creator claim.
  - Scoping the depth-layer build (the extractor must emit these fields).
  - Checking whether a derived label may be displayed, downgraded, or must be withheld.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
  - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
  - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
  - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - The charter's pre-build gate 1 (Section 7) is amended or superseded.
  - The product architecture's Signal claim layer contract changes.
  - A later accepted record moves derived-claim display ownership out of Creator Signal.
```

## Status

`CONTRACT_V0` — authored 2026-07-04 to discharge the *existence* requirement of
the Aphrodite carveout charter's pre-build gate 1
(`aphrodite_carveout_charter_v0.md`, Section 7). The charter (owner-ratified
direction) named this gate; this contract fixes the required **semantics** of
derived-claim provenance. It is a docs-first display/claim-language contract
inside Creator Signal's owned surface. It is **not** validation, build
authorization, capture authorization, a storage schema, or model routing, and
it authorizes no extractor build.

## Why this contract exists

The depth-now moat layer (charter Section 3) turns captured transcripts and
comments into *derived* claims — fit, ad-reception, purchase-intent, segment
share, momentum reads. Raw extraction is commodity; the moat is that our
derived claims carry receipts while a field-copying competitor's are unstamped
vibes (charter Section 3). The existing provenance discipline
(`creator_signal_product_architecture_v0.md`, "Signal claim layer";
per-number `sha256` + posture coupling) was written for *observed* metrics.
Without this contract, a derived label could reach a surface as a bare value —
exactly the "unstamped / LLM-only claim" the charter forbids. This contract
closes that gap by extending the same discipline to derived claims.

## The rule

A derived claim may be shown on any Creator Signal / Aphrodite surface **only
if it is expressed as a claim object carrying derivation provenance.** A
derived claim lacking any required field below resolves to `withhold` — it is
not shown, and it is **never** zero-filled or presented as absence-of-signal.

### Required derivation-provenance fields (per derived claim)

| Field | What it carries | Why |
| --- | --- | --- |
| `source_refs` | The captured unit(s) the claim was derived from (video/transcript id, comment-set id), each carrying its own capture provenance (source pointer + content hash) inherited from the capture record | Ties the derived claim back to real, addressable observed evidence |
| `extraction_model` | The model id + version that produced the label | A derived claim's producer is auditable, not anonymous |
| `extraction_recipe_version` | The versioned prompt/instruction/recipe that produced it | The derivation is reproducible and re-runnable; a recipe change is visible |
| `input_content_hash` | Hash of the exact input text the extraction ran over | The derivation can be re-checked against its true input, not a paraphrase |
| `extraction_timestamp` | When the derivation ran | Freshness of the *derivation*, distinct from capture freshness |
| `receipt` | The supporting quote(s) / timestamp(s) / comment link(s) the claim rests on | The buyer can "verify this claim" at the source, same as per-number drill-back |
| `confidence_or_abstention` | A confidence signal, or an explicit "insufficient evidence" abstention | A weak or unsupported derivation withholds rather than fabricating certainty |

### Composition with the existing claim layer

The derived claim is itself a claim object with
`provenance_state: show | downgrade | withhold`, structurally mirroring the
internal posture object (`value_or_none` / `posture` / `posture_reason`) exactly
as the product architecture requires for observed metrics. `missing != zero`
holds: an absent or unsupported derived claim is `withhold`, never `0`, never a
silent gap. Derivation provenance is *additive* to — never a replacement for —
the underlying capture provenance of the `source_refs`.

## Forbidden (extends the charter forbidden set to derived claims)

- No derived claim shown without the fields above (the unstamped/LLM-only claim
  the doctrine forbids).
- No derived claim presented as an observed metric — a derived value is
  labeled derived; the two are never blended into one number.
- No single "vanity" derived score collapsing multiple derived signals into one
  figure that hides its inputs' weakness (charter/product-architecture rule).
- No derived person-level identity or demographic inference (inherits the
  spine's forbidden set; person-level stays out regardless of provenance).
- No zero-filling a withheld derived claim.

## Boundary — what this contract does and does not own

- **Owns (Creator Signal surface concern):** the *rule* that a derived claim
  must carry the fields above to be displayed, downgraded, or withheld; the
  claim-language and source-drill-back expectation. Per the spine binding,
  Creator Signal owns "product-facing claim language" and "required
  freshness, limitation, and source-drill-back displays" — this is that,
  applied to derived claims.
- **Does NOT own or authorize:** the extraction recipe itself, the model
  choice, the capture of transcripts/comments, the runner, or the physical
  storage/field schema. Those are capture / computation-lane concerns
  (`does_not_own` in the spine binding) and are deferred to a separately
  authorized build. This contract fixes the required *semantics*, not the
  storage layout; the build lane physicalizes the fields under its own
  authorization and implementation scoping.

## Non-claims

- Not validation, readiness, buyer proof, or willingness-to-pay evidence.
- Not authorization to build the extractor, run capture, choose a model, or
  create a storage schema.
- Not a capture-boundary or ToS decision (see the depth-capture ToS sanity
  check and the capture-lane source-access boundary).
- Discharges only the *existence* of the charter's gate 1; the gate's
  operational satisfaction is checked when the depth-layer build binds to this
  contract.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Extends the Creator Signal provenance / claim-object discipline from
    observed metrics to DERIVED claims: any inferred creator claim (fit,
    ad-reception, purchase-intent, segment-share, momentum read) must carry
    derivation provenance (source_refs, extraction_model, recipe_version,
    input_content_hash, timestamp, receipt, confidence/abstention) to be shown,
    and resolves to withhold otherwise. Owns the display/claim-language rule
    only; the extractor, model, capture, and storage schema stay
    capture/computation-lane concerns deferred to a separately authorized
    build. Discharges the Aphrodite carveout charter's pre-build gate 1
    (existence).
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # Section 7 gate-status note
    - forseti/product/spines/creator_signal/README.md                          # index row
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md  # Signal claim layer is the parent concept this extends; consistent, not amended
    - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md              # claim-language ownership is Creator Signal's; this stays inside owns/does_not_own
    - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md # surface contract's claim-display rules are consistent; derived claims join the same discipline
  intentionally_not_updated:
    - path: forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
      reason: >
        Its Signal claim layer spec is the parent; this contract extends it to
        derived claims without changing the observed-metric rules. Routes to it.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Per spine-binding precedent, per-spine artifacts route via the spine
        front door (README), updated in this lane; no repo-map row added.
  stale_language_search: >
    rg -in "derived claim|extraction provenance|derivation provenance|unstamped" forseti/product/spines/creator_signal
  stale_language_search_result: >
    Executed 2026-07-04 in the lane worktree. Hits are this contract, the
    charter's pre-build gate 1 and moat-protector language it discharges, and
    the product architecture's forbidden "unstamped/LLM-only claims" rule this
    operationalizes. No conflicting surface: no existing artifact defined a
    competing derived-claim display rule.
  non_claims:
    - not validation
    - not readiness
    - not build or extractor authorization
    - not capture or ToS authorization
    - not a storage schema
    - not model routing
```
