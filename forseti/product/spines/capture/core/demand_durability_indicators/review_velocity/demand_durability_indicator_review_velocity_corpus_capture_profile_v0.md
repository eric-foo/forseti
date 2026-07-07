# Demand-Durability Indicator — Review Velocity / Corpus Capture Profile v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (demand-indicator capture profile)
scope: >
  Capture profile for the review velocity / corpus demand-durability indicator.
  Specifies what the capture lane must record and what limits must be made
  visible when review surfaces are commissioned for a Decision Frame. Design+spec
  only. Does not authorize sourcing, implementation, contract hardening, or
  runtime. Conditional on sourcing (see below).
use_when:
  - Specifying or reviewing review-surface capture obligations for a commissioned Decision Frame.
  - Checking the temporal regime, arrival-cadence history, farm-detection observables, and deletion-detection approach for a review series.
  - Deciding whether a review corpus capture is ready for handoff to ECR.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md  # Lane 1 envelope-delta (temporal regimes, cold-start doctrine, five new elements)
  - orca-harness/source_capture/models.py                                          # Capture Envelope of record (schema)
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md  # Obligation contract §12 (review surfaces rule)
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md                        # INV-1, Demand-Substrate Hard Gate, costly-behavior, integrity labels
  - forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md  # AR-04 sourcing-gap status
  - docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md  # RQ-05 source-language-anchor status
stale_if:
  - The Lane 1 envelope-delta spec (capture_envelope_durability_delta_spec_v0.md) is amended or superseded.
  - The capture envelope of record (models.py or the obligation contract) is amended in a way that covers these facts, especially §12 (review surfaces).
  - An owner decision adopts, narrows, or rejects the review-surface unsourced-gap classification (AR-04).
  - A sourcing authorization for review surfaces is accepted (at which point this profile becomes binding, not conditional).
  - The RQ-05 carry-forward classification is amended or superseded.
```

- Status: `CAPTURE_PROFILE_DRAFT_V0`
- Artifact type: Product-method spec (demand-indicator capture profile)
- Implementation authorized: no
- Feature planning authorized: no
- Runtime / source-system design authorized: no
- Contract hardening authorized: no (owner-gated, out of scope)
- Sourcing authorized: **no** — see Conditional-On-Sourcing statement below

## Retrieval Header And Deconfliction Note

**What this is.** This capture profile is a delta-on-the-envelope spec that
names the review-surface-specific capture obligations, temporal regime, and
observability constraints a commissioned review corpus must satisfy. It CITES
AND EXTENDS — it does not re-derive, replace, or fork — the following
authoritative sources:

- **Lane 1 envelope-delta spec:** `forseti/product/spines/capture/core/demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md`
  (status `DELTA_SPEC_DRAFT_V0`). Consumed: the three temporal regimes + cold-start
  inherent-limit cap (Element 5), the five new elements, and the INV-1
  preservation rule. This profile's temporal regime ("retroactive timestamps +
  forward integrity") is derived from Regime 1 (retroactive-native) for the
  arrival-cadence dimension and from the series-diff (Element 3) for
  forward re-snapshot deletion detection.
- **Capture Envelope of record:** `orca-harness/source_capture/models.py` (schema)
  and `forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  (obligations). Controlling authority. If this profile conflicts with either,
  the envelope of record wins.
- **Obligation contract §12 — Related Context Preservation, review surfaces rule:**
  The contract's §12 already states: "For review surfaces, preserve rating, text,
  recency posture, visible experience timing, moderation/incentive/sorting posture
  where available, and long-context positive or negative detail when it carries
  signal." This profile **CITE-AND-EXTENDS** §12 — it does not restate it as new
  authority. The §12 rule is the floor; this profile adds the velocity/corpus
  capture facts (arrival cadence, reviewer metadata, farm-detection observables,
  deletion detection, truncation disclosure) that §12 does not specify.
- **RQ-05 (source-language anchors):** Per
  `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md`,
  RQ-05 is `carry_forward` for forum, review, and text-heavy discourse captures:
  capture artifacts should include bounded source-language anchors from the start.
  This profile **cite-and-extends** RQ-05: review text capture under this profile
  must include source-language anchors from the start per the RQ-05 carry-forward
  classification.
- **INV-1 and the Demand-Substrate Hard Gate:** `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md`.
  Consumed as-is; not redefined here. Integrity labels (artificial-amplification
  risk, incentive distortion, copied/coordinated) are a pre-requisite for review
  evidence entering a fused read.
- **Demand-Read Taxonomy:** `forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md`
  (PROPOSED, pending adjudication). Review velocity and content shifts are named
  as buy-side corroboration (costly behavior layer); review surfaces are also
  flagged for J-curve self-selection bias and FTC 16 CFR 465 pollution risk.

**Deconfliction — §12 and RQ-05.** This profile extends, not replaces, §12 and
RQ-05. The §12 rule governs what is preserved per review observation (rating,
text, recency, moderation/incentive, experience timing). This profile adds the
*series-level* obligations (arrival-cadence history, reviewer metadata for
farm-detection, deletion-detection via forward re-snapshots, truncation
disclosure) that a velocity/corpus read requires but that §12 does not name.
Any future amendment to §12 that covers these facts supersedes this profile's
corresponding sections; this profile then becomes stale for those sections and
§12 controls.

**AR-04 deconfliction:** Review surfaces are classified in
`forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md`
(AR-04) as **G1 unsourced demand-family gap** — owner-owned, not yet sourced.
This profile is CONDITIONAL ON SOURCING; see below.

---

## Conditional-On-Sourcing Statement

**Review-surface (Venue) sourcing is an UNSOURCED GAP (AR-04).** Per
`forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md`,
review surfaces are a G1 demand-family card that is currently unsourced — the
sourcing route, vendor, API, or access method has not been authorized by the
owner for Orca capture use.

**This capture profile describes obligations that apply ONLY AFTER a
review-surface source is sourced and the sourcing is authorized by the owner.**
Reading this document does not authorize sourcing, implementation, contract
hardening, vendor selection, API access, or any runtime. Those decisions are
owner-gated and out of scope for this profile.

---

## What This Profile Adds (Cited Extension, Not New Authority)

This profile names the review-surface-specific facts that sit on top of the
Lane 1 envelope-delta's five new elements and the obligation contract's §12
floor. It does not invent new capture facts; it applies the envelope-delta
doctrine and extends §12 to the velocity/corpus surface.

### Temporal Regime: Retroactive Timestamps + Forward Integrity

The review surface has a **dual temporal character** that the Lane 1 envelope-
delta's regime vocabulary captures as follows:

1. **Retroactive-native dimension (arrival-cadence history):** Each review
   carries a timestamp (review date, posting date, or visible submission date).
   A single scrape of the review corpus therefore yields a timestamped sequence
   of arrivals — an arrival-cadence history back to the source's own retention
   window. This is **retroactive-native** (Lane 1 §Element 5 Regime 1): the
   source carries its own history; Orca need not have been observing since day
   one to recover velocity and arrival patterns.

   Capture obligation: record the timestamp per review as a first-class capture
   fact. The `source_publication_or_event` timestamp in `PacketTiming` (from the
   envelope of record `models.py`) is the capture anchor. When the source exposes
   multiple date fields (posting date, edit date, verified-purchase date,
   experience date), capture all that are visible per review, as `VisibleFact`s,
   and record which is the authoritative arrival timestamp for velocity
   computation.

2. **Forward integrity dimension (deletion and edit detection):** Review corpora
   are dynamic: individual reviews may be deleted by the platform, removed for
   moderation, edited, or flagged as incentivized/unverified after the initial
   scrape. A single snapshot cannot detect these changes. Forward re-snapshots
   of the same corpus surface are required to detect deletions and edits as
   integrity observables.

   Capture obligation: forward re-snapshots of the same corpus must be treated
   as a series (Lane 1 §Element 2 cold-start marker applies; §Element 3
   series-diff applies). Differences between snapshots — reviews present in
   snapshot N but absent in snapshot N+1 — are recorded as **observed deletions**
   via the series-diff, using content-hash comparison (`PreservedFile.sha256`
   from the envelope of record) and source-visible deletion/moderation markers
   where available.

Cold-start as inherent-limit cap (consumed from Lane 1 §Element 5): reviews
that existed before the first Orca scrape but are no longer visible in a later
scrape cannot be recovered for forward-only or event-based surfaces. The
retroactive-native dimension applies to the timestamps of reviews still visible
at scrape time; deleted reviews that were never scrapped are irrecoverable
(inherent-limit cap, not a clearable risk).

### Review Text and Reviewer Metadata (Cite-And-Extend of §12)

Building on obligation contract §12 ("for review surfaces, preserve rating,
text, recency posture, visible experience timing, moderation/incentive/sorting
posture where available"):

This profile extends §12 for velocity/corpus use by adding:

- **Review text** — full review body (or the longest excerpt the source exposes
  without API caps; see Truncation below), not just rating and summary. Source-
  language anchors from the start (RQ-05 carry-forward) apply: the capture must
  include bounded verbatim text from the review, not only an operator paraphrase.
- **Reviewer metadata (observables only):** capture the reviewer identifier or
  pseudonym, account age or tenure visibility, review history count (if visible),
  verified-purchase or verified-experience flag, and any platform-visible
  reviewer tier or badge. These are **capture observables** that downstream
  farm-detection can use. They are NOT a credibility or integrity verdict
  (see INV-1 / flag-don't-conclude below).
- **Incentive and moderation visibility:** per §12, capture whether the
  review is visibly marked as incentivized, compensated, solicited, or
  moderated. Capture the platform's own label; do not infer incentive from the
  review text.
- **Sort order and surface positioning:** when reviews are scraped in a
  particular platform-determined sort order (most recent, highest rated,
  featured), record that sort order as a visible capture condition — it affects
  which reviews are captured when pagination limits apply (see Truncation).
- **Experience timing vs posting timing:** when both are visible (e.g., "used
  for 6 months before posting"), capture both timestamps. Experience timing is
  a demand-timing observable distinct from posting velocity.

### Farm-Detection Observables: Flag-Don't-Conclude (INV-1)

Downstream signal-integrity processing (Judgment Spine, Signal Integrity) may
use reviewer metadata and corpus patterns to detect review farms, coordinated
astroturf, or artificially amplified sentiment. Capture's role is to record
the **observables that make farm detection possible**, not to render a
farm-detection verdict.

Capture must record the **raw, source-visible observables** that make farm
detection possible downstream (not derived pattern features, not verdicts):

- reviewer account age and review history depth, when visible;
- **raw per-review arrival timestamps** — the substrate from which downstream
  Cleaning/Judgment computes posting-velocity / burst features. Capture records
  the timestamps; it does **not** compute or record "bursts" (a derived
  pattern);
- **review text verbatim** — the substrate from which downstream computes
  language-pattern / clustering features. Capture records the text; it does
  **not** compute or record clustering, per the obligation contract's *Forbidden
  Outputs From Capture* (no "semantic dedupe or clustering effects", no
  "Cleaning transformations");
- verified-purchase / verified-experience flag per review, or the absence of
  such flags;
- any platform-visible moderation or flagging on individual reviews.

Burst, clustering, and farm-pattern **derivation** is downstream (Cleaning /
Judgment Signal Integrity). Capture preserves the raw timestamps, text, and
visible labels that make that derivation possible and emits no derived pattern
feature (INV-1).

**Flag-don't-conclude rule (INV-1 application):** capture records each of these
as a `VisibleFact` or `warning_note` per the envelope of record's mechanism. It
does NOT classify a reviewer as a bot, a review as fake, a corpus as astroturfed,
or a brand's reviews as farm-generated. Those credibility and integrity verdicts
are downstream Judgment / Signal Integrity calls, not capture outputs. Capture's
observable anchors the Judgment call; it never substitutes for it.

This is consistent with the Lane 1 envelope-delta §Element 3 hard boundary:
"the series-diff records observed differences and their evidentiary basis. It
does not decide whether a change is malicious, manufactured, astroturfed, or
distortion — that integrity judgment is Judgment Spine's."

### Truncation Disclosure

Review platforms commonly expose only a paginated or API-capped subset of the
full corpus. Capture must record:

- **Total visible review count** as reported by the source surface (e.g., "4,382
  reviews"), if visible. This is the denominator the capture is drawn from.
- **Captured review count** — how many reviews were actually captured in this
  session.
- **Truncation reason** — whether truncation is due to pagination limits, API
  rate caps, session time limits, operator scope decisions, or source-side
  filtering. Record as a visible limitation per the obligation contract's
  `not_attempted` / `access_failed` / `partial` vocabulary, as applicable.
- **Sort order and coverage bias** — when the captured subset is a non-random
  sample (e.g., only the most-recent 50 reviews), the arrival-cadence history
  derived from that subset is biased toward that stratum; record this as a
  visible series-level limitation.

Silent truncation — capturing only the first page without recording that more
exists — is a silent failure. Per obligation contract §14, failure must be made
visible.

### Deletion Detection via Forward Re-Snapshots

Forward re-snapshots are the capture mechanism for detecting review deletions.
The capture lane should:

- treat each re-snapshot of the same review surface as a new observation in the
  series (series-id via Lane 1 §Element 2 cold-start marker);
- compute content-hash differences between snapshots (`PreservedFile.sha256`
  from the envelope of record) to identify reviews present in snapshot N but
  absent in snapshot N+1;
- record the `tamper_deletion_visibility` field (Lane 1 §Element 3): whether the
  deletion was source-visibly marked (moderation, platform removal notice) or
  inferred from hash/value divergence only, or `cannot_assess`.

**Deletion is an integrity OBSERVABLE, not a verdict.** A deleted review is
recorded as an observed disappearance. Capture does not decide why it was
deleted (legitimate moderation, legal takedown, review-farm cleanup,
self-removal). That determination is downstream Judgment / Signal Integrity.

### Pinning Facts for Comparability (Lane 1 §Element 1)

For a review corpus series to remain comparable across snapshots:

- `locale_pin` — the locale and language the review surface was accessed in,
  when the platform serves locale-filtered reviews.
- `variant_pin` — the specific product variant (SKU, size, edition) the reviews
  are attached to, when a platform splits reviews by variant. A series mixing
  reviews from different variants is not comparable without this pin.
- `session_visibility_pin` — whether the capture was performed logged-out,
  logged-in without purchase history, or entitled/verified-purchase account,
  when platform visibility differs by session type.

Each carried as a `VisibleFact` (Lane 1 §Element 1). When a pin is unknown or
the source does not expose it, record `unknown_with_reason` / `unavailable_by_source`.

### Cadence Disclosure (Lane 1 §Element 4)

A review corpus series should declare its intended re-snapshot cadence using
the existing `CadencePlan` shape (Lane 1 §Element 4), record realized cadence
per snapshot via `capture_time`, and record cadence deviations and gaps as
visible limitations. Cadence gaps affect the arrival-cadence history's ability
to detect deletion events: a review deleted between two widely-spaced snapshots
cannot be dated to a specific window.

---

## INV-1 Preservation

This profile is bound by INV-1 (no scoring, weighting, ranking, or judgment),
per `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md` and the
demand-read taxonomy. Concretely in this profile:

- reviewer metadata and corpus-pattern observables are **capture inputs**, not
  credibility scores or astroturf verdicts;
- arrival-cadence history records **observed review posting velocity** as a
  timestamped series — it does not classify that velocity as organic vs
  manufactured;
- deletion detection records **observed disappearances** — it does not classify
  them as suppression, moderation, or fraud;
- the farm-detection flag rule (above) is a hard INV-1 boundary: capture
  flags the observable; it never renders the integrity verdict;
- the sentiment/costly-behavior separation is downstream Judgment's job:
  capture records the review text and rating; whether that text evidences
  costly behavior (switching, workarounds, durable buyer pressure) vs
  engagement-only sentiment is a Judgment call, not a capture output.

---

## Boundaries And Non-Goals

- **No sourcing authorization.** This profile is conditional on sourcing (see
  above). Reading it does not authorize any review-platform access, vendor
  selection, API subscription, or web scraping.
- **No credibility or integrity verdicts.** Farm detection, astroturf
  classification, review credibility scoring, and sentiment-to-costly-behavior
  translation are downstream Judgment / Signal Integrity outputs, not capture
  outputs.
- **No second envelope.** The envelope of record is the controlling authority;
  this profile extends it and does not fork it.
- **No contract hardening.** Owner-gated, out of scope.
- **No ECR / Cleaning / Judgment design.** No ECR fields, Cleaning
  transformations, normalization rules, or Judgment/scoring logic.
- **No runtime, scraper, API, or scheduler design.** `CadencePlan` is referenced
  as an existing planning primitive only.
- **§12 is the floor, not replaced.** This profile adds to §12 for velocity/
  corpus use; if §12 is amended to cover these facts, the amended §12 controls
  and the corresponding sections of this profile become stale.
- **No implementation of any kind.** Design+spec only.

---

## Non-Claims

This profile is not validation, readiness, acceptance, contract hardening,
source-of-truth promotion, buyer proof, judgment-quality evidence, sourcing
authorization, implementation authorization, runtime authorization, tooling
authorization, scheduler/monitor authorization, source-access boundary
amendment, obligation-contract amendment, schema change, ECR design, Cleaning
implementation, Judgment design, or commercial-readiness evidence. It is a
design+spec profile that cites the existing Capture Envelope of record, the
Lane 1 envelope-delta spec, obligation contract §12 (cite-and-extend), and
RQ-05 carry-forward (cite-and-extend), and names the review-surface-specific
capture obligations and observability constraints a commissioned review corpus
must satisfy when a source is authorized.

---

## Lifecycle Verification

```yaml
lifecycle_verification:
  authored_by: Claude Sonnet 4.6 (claude-sonnet-4-6)
  authored_date: 2026-06-14
  worktree: .claude/worktrees/capture-indicator-search-review
  branch: capture-indicator-search-review
  base: origin/main
  pr_target: main
  sources_cited:
    - forseti/product/spines/capture/core/demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md  # Lane 1 envelope-delta (consumed, not re-derived)
    - orca-harness/source_capture/models.py                                          # Capture Envelope of record (schema, cited)
    - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md  # Obligation contract §12 (cite-and-extend)
    - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md                        # INV-1, Hard Gate, integrity labels (consumed)
    - forseti/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md  # AR-04 (cited)
    - docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md  # RQ-05 carry_forward (cite-and-extend)
    - forseti/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md                      # Signal layer orientation (consumed)
  inv1_preserved: yes — observables+flag only; no credibility/integrity verdict; farm-detection is downstream Judgment
  conditional_on_sourcing: yes — AR-04 unsourced gap; sourcing not authorized by this profile
  deconfliction_section12: cite-and-extend — §12 is the floor; this profile adds velocity/corpus facts §12 does not name
  deconfliction_rq05: cite-and-extend — RQ-05 carry_forward applies; source-language anchors from the start for review text
  contract_hardening_authorized: no
  implementation_authorized: no
  non_claims_stated: yes
```
