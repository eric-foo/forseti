# Demand-Durability Indicator Capture Profile — Review Velocity / Corpus v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (per-indicator capture profile; consumes the Capture Envelope durability delta)
scope: >
  Thin capture profile for the REVIEW VELOCITY / CORPUS demand-durability indicator.
  Names the per-review timestamp + text + reviewer-metadata facts (so downstream
  farm-detection is possible), the retroactive-timestamps + forward-integrity temporal
  regime, truncation handling, and the deletion-by-re-snapshot integrity signal —
  drawing the hard line against deleted-BODY retrieval (owner-dropped). Drops onto the
  Capture Envelope of record + durability delta. Design + spec only.
  TERMINOLOGY: "indicator" is the demand-side observable; "proxy" is reserved for the
  NETWORK sense (ProxyProfile). The keystone delta / taxonomy still say "proxy" for
  this concept — reconciliation pending (see deconfliction note).
use_when:
  - Specifying or reviewing capture of review arrival-cadence + corpus over time.
  - Checking how review observations sit on the Source Capture packet + durability delta + obligation Ob.12.
  - Drawing the line between detecting a deletion (allowed) and retrieving a deleted body (dropped).
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md  # Ob.12 review-surface related-context (cite, do not re-spec)
  - docs/decisions/data_capture_spine_deleted_comment_signal_retrieval_scoped_doctrine_decision_v0.md  # DROPPED — deleted-body retrieval is out
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md                          # review velocity & content shifts (Layer 3)
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md                            # reviews admissible (J-curve + FTC 16 CFR 465 flagged), never sole basis
stale_if:
  - The keystone durability delta changes the five elements.
  - The obligation contract changes Ob.12 (review-surface related-context) or the posture vocabularies.
  - The deleted-comment-retrieval decision is re-opened (it is currently DROPPED).
  - The demand-read taxonomy / Demand-Substrate Hard Gate changes the review-signal role.
  - An owner decision adopts, narrows, or rejects any review capture fact below.
```

- Status: `PROFILE_DRAFT_V0`
- Artifact type: Per-indicator capture profile (subordinate to the durability delta; not a new envelope)
- Implementation authorized: no · Feature planning authorized: no · Runtime/source-system design authorized: no · Contract hardening authorized: no (owner-gated, out of scope)

## What This Is (And Consumes)

A thin per-indicator profile on the **Capture Envelope of record** (`models.py` +
obligation contract, **including Ob.12 review-surface related-context**) and the
**durability delta** (`capture_envelope_durability_delta_spec_v0.md`; it calls these
observables "proxies" — same concept, renamed "indicator" here). It adds no provenance
field and re-specs neither Ob.12 nor any durability element; it supplies only the
review-velocity/corpus bindings. On conflict, the schema / obligation contract / delta
win.

Scope note (owner, 2026-06-15): demand-durability reading is **one decision Orca can
help with**, not Orca's whole job.

## The Demand Read This Indicator Serves (read-trace)

Review velocity & content shifts are **Layer 3 buy-side corroboration** in the
demand-read taxonomy. A review is comparatively costly (someone bought and wrote), so
**review arrival cadence is floor-eligible** as one fused venue — **but reviews are
manipulable (farms) and self-selected (J-curve), so the gate admits them flagged and
never as sole basis** (buyer-proof packet: "Reviews ARE admissible — as one fused venue,
flagged for J-curve self-selection bias and FTC 16 CFR 465 pollution — never as the sole
basis"). This indicator is **sentiment-grade unless farm-checked.**

| Captured review fact | Serves which read | Floor/ceiling role |
| --- | --- | --- |
| Review **arrival cadence** (from per-review timestamps) | Buy-side costly-behavior velocity; durable-vs-transient shape | **Floor-eligible** (one fused venue) — subject to farm-check; never sole basis |
| Review **text + content shift** over time | Pain-point convergence / content-shift read | Fused-venue input; flagged for incentive/J-curve |
| Reviewer **metadata** (for farm-detection) | Integrity layer (real-vs-manufactured axis) | Enables divergence/defeater; not an integrity verdict at capture |
| Review **deletion** (by disappearance across snapshots) | Integrity signal (suppression/cleanup) | Recorded as observed change; not classified at capture |

## Temporal Regime — per durability delta Element 5

Review velocity is **mixed**:

- **Retroactive-native (timestamps)** — each review carries its own posting timestamp, so
  **one scrape yields the full arrival-cadence history**. The series reaches backward past
  Orca's cold start because the **source** carries the timestamps;
  `pre_coverage_history_posture` (delta Element 2) is largely satisfied by this native
  history, bounded by what the surface exposes (and truncation, below), recorded with the
  source as basis.
- **Forward-only (integrity / deletion)** — *deletion* of a previously-present review is
  only observable by **forward re-snapshot** (present at snapshot N, absent at N+1). That
  integrity signal is forward-accumulated from cold start; pre-cold-start deletions are
  an inherent-limit cap (you cannot observe a deletion that happened before you started
  snapshotting).

So a velocity *shape* read is available immediately (retroactive timestamps), while the
*deletion-integrity* read requires a forward tracking window.

## Review-Specific Capture Facts

Each an observed `VisibleFact` / preserved item; none a score or judgment. These
**extend Ob.12's review-surface related-context** (rating, text, recency, visible
experience timing, moderation/incentive/sorting posture) for the durability series —
they do not replace Ob.12.

- **per-review `posted_timestamp`** — the source-visible posting/experience timestamp of
  each review (the basis of arrival cadence). Decomposed timing (Ob.8) keeps it distinct
  from `capture_time`.
- **per-review `review_text`** — the verbatim review body (Ob.6 raw observable + RQ-05
  source-language anchors). **Capture the text, do not just count** — farm- and
  content-shift detection downstream needs the corpus.
- **per-review `reviewer_metadata`** — source-visible reviewer attributes that enable
  downstream farm-detection: reviewer handle/id (as shown), review count,
  verified-purchase marker, badge/tenure, rating, helpful-votes — **captured as shown,
  never used to build a person dossier** (see boundary below).
- **`review_arrival_series`** — the ordered arrival cadence derived from the timestamps
  for one `series_id`.
- **`sort_moderation_posture`** — the source-visible sort order, filter, incentive
  disclosure, and moderation posture under which the corpus was observed (Ob.12), since it
  shapes which reviews are visible.
- **`truncation_posture`** — **whether the capture is truncated** by pagination caps, API
  page limits, or "most recent N only," recorded as a first-class limitation so a partial
  corpus is never read as complete.

These are source-visible facts. They are **not** a credibility/farm verdict, **not** ECR
fields, and **not** a sentiment score.

## Pinning (delta Element 1)

- **`variant_pin`** — record whether reviews are per-variant or aggregated across variants
  (surfaces differ); a series must hold this fixed or record the change.
- **`locale_pin`** — which regional store/locale's review set (regional review pools
  differ); record the effective rendered locale.
- **`session_visibility_pin`** — logged-out vs entitled (some surfaces gate full review
  sets or sort options behind login).
- `currency_pin` → `not_applicable` with reason.

Unknown/unexposed → `unknown_with_reason` / `unavailable_by_source`, never guessed.

## Capture Method & Boundary

Per the method plan (discoverable-or-entitled + disclosable; measured-ToS; industrial
scraping rejected):

1. **Structured access / API** — where the review surface offers a sanctioned API
   (Method 1); note API page caps as `truncation_posture`.
2. **Rendered/headless browser** — for render-time review lists / lazy-loaded pages
   (Methods 2/3/10); note pagination caps as `truncation_posture`.
3. **Archive (Wayback)** — for retroactive review-surface state (Method 6), recorded with
   `archive_snapshot_time`; useful for confirming a review's prior presence.
4. **Manual human-browser capture** — for high-value/bounded corpora (Method 8).

Capture mode disclosed (Ob.4); mode changes visible (Ob.5).

## Series Integrity (delta Element 3) — deletion detection, and the hard line

The **series-level recapture-diff** records observed review-corpus changes across the
ordered series — including a previously-present review that **disappears** (an integrity
signal: suppression, cleanup, or platform removal), anchored on the existing
`PreservedFile.sha256` of each snapshot and source-visible deletion markers, with a
`tamper_deletion_visibility` note.

**Hard line — deletion DETECTION vs deleted-BODY RETRIEVAL.** This profile authorizes
only **detecting that a review was deleted by its disappearance across Orca's own forward
snapshots** (the review was present in a snapshot Orca already captured; later it is
gone). It does **NOT** authorize **retrieving the deleted review body from a third-party
archive** (PullPush-style). That capability was **considered and `DROPPED` by owner
decision** (`docs/decisions/data_capture_spine_deleted_comment_signal_retrieval_scoped_doctrine_decision_v0.md`,
2026-06-08: stale coverage, low recovery, privacy/PDPA baggage, and it would amend the
capture-spine no-body hard stop). This profile re-specs none of that and stays inside the
existing hard stop: the deleted body is recorded as **present-then-absent with the text
Orca already captured before deletion**, never re-fetched from a deleted-content archive.

The diff **records** disappearance as an observed change; it **does not** classify it as
suppression, astroturf-cleanup, or distortion — that integrity classification is Judgment
Spine's (obligation contract forbidden output).

## Cadence (delta Element 4)

Cadence is the measurement-resolution + honesty knob, and it decides what each read can
claim: for the **forward deletion-integrity** read it sets how tightly a deletion can be
localized in time (a sparse cadence widens the deletion window and weakens "this review
was suppressed in week N"); for the **retroactive velocity** read a single capture
suffices, while re-snapshots refresh the corpus and detect deletions. **It must be
expressed on the indicator's sampling rhythm — hourly to daily (owner, 2026-06-15)**, not the seconds-scale `CadencePlan`
was built for; `CadencePlan` lends vocabulary only, and a real time-scale series cadence
is a confirmed need whose primitive is a build/hardening step (out of scope). Declare
intended cadence, record realized timings + gaps as visible limitations.

## Manipulability & Integrity Posture

Reviews are **manipulable (farms) and self-selected (J-curve)** — **sentiment-grade
unless farm-checked.** Under the manipulable-input rule (buyer-proof packet): reviews are
**admissible sentiment input**, review *velocity* is floor-eligible as **one fused venue**
(never sole basis), and **divergence can defeat the floor** when the divergence pattern
indicates the review burst is itself likely manufactured/coordinated (e.g. a velocity
spike whose corpus shows farm markers). Capture's job is to **preserve the corpus +
reviewer metadata + truncation + deletion signal** so farm-detection and the
floor/defeater decision are *possible* downstream — capture flags, it does not conclude.

## Deconfliction (per-indicator)

- **Already covered — do NOT re-spec:** envelope/provenance (schema + obligation
  contract); **Ob.12 review-surface related-context** (rating/text/recency/experience-
  timing/moderation-incentive-sorting posture) — this profile *cites and extends* it for
  the durability series, it does not restate it; RQ-05 source-language anchors and RQ-01
  verbatim/structure (source-observability boundary decision); durability elements
  (delta); the deletion-by-disappearance integrity facility (delta Element 3 series-diff).
- **Genuinely new here:** the **review arrival-cadence series** binding, **per-review
  reviewer-metadata for farm-detection-enablement** (corpus, not count), the
  **`truncation_posture`** first-class limitation, the **deletion-detection-vs-retrieval
  hard line**, and the read-trace tying review velocity to the costly-behavior floor with
  the J-curve/FTC/farm flags.
- **Explicitly OUT (dropped / deferred):** deleted-review **body retrieval** from
  third-party archives (`DROPPED` decision); person-level reviewer dossiers (forbidden —
  reviewer metadata is for farm-detection as fused signal, not a sold/external person
  surface; consistent with the wind-caller carve-out's internal-only boundary and the
  future-exploration-lanes hard stop); org-motion/distribution (EDGAR lane, deferred);
  repurchase indicators (deferred — they piggyback on review + price).

## INV-1 Preservation

Every element is a captured fact or a capture method/pin/regime — never a weight, score,
threshold, ranking, sentiment score, farm verdict, or durability verdict. Farm-detection,
J-curve/incentive adjustment, and durable-vs-transient reading are downstream (Cleaning
integrity labels + Judgment Signal Integrity), consumed from the taxonomy/gate, never
decided here. Capturing reviewer metadata enables farm-detection; it does not perform it
and does not build a person dossier.

## Boundaries, Non-Goals, Non-Claims

- No build/scrape/run/deploy; no scheduler/monitor; primitives referenced only.
- No edits to `models.py` or the obligation contract; field promotion (and any
  no-body-hard-stop change) is contract hardening (owner-gated, out of scope).
- No deleted-body retrieval; no person-level reviewer dossier; no ECR/Cleaning/Judgment
  design; no sentiment/farm scoring.
- **Commissioned capture only (Ob.1) today.** Continuous monitoring of this indicator is
  owner-confirmed as wanted (2026-06-15) but is gated on a standing-capture obligation
  home that does not yet exist (see deconfliction note); this profile does not authorize
  standing collection.
- Not validation, readiness, acceptance, source-of-truth promotion, buyer proof,
  implementation/runtime/tooling authorization, source-access boundary amendment,
  no-body-hard-stop amendment, or commercial-readiness evidence.
```
