# Wind-Caller (WindCaller) Calibration Carve-Out v0

```yaml
retrieval_header_version: 1
artifact_role: owner-signed decision record
scope: >
  Bounded carve-out to the "wind callers = channels not persons" boundary,
  scoped to creator/influencer wind-callers only, for internal calibration.
  Owner-signed 2026-06-13.
use_when:
  - Deciding whether internal wind-caller calibration data collection is permitted.
  - Checking the tier classification (allowed / deferred / excluded) for person-adjacent capture.
  - Checking whether audience-graph or cross-platform handle stitching is authorized.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md   # wind-caller read type
  - orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md  # Tier 2 deferred items
  - forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md  # external boundary unchanged
stale_if:
  - The owner amends this record (dated amendments only; no silent rewrites).
  - Commercial scale begins — triggers mandatory licensed/bought-data posture for wind-caller stats.
  - EU/UK creator inclusion is assessed — requires legitimate-interest/retention check before activation.
```

## Status

`OWNER_SIGNED_DIRECTION_LOCK` — signed by owner 2026-06-13.

This record is a bounded carve-out to one prior boundary, scoped exclusively to
internal wind-caller calibration for creator/influencer wind-callers. It is not
validation, readiness, buyer proof, or commercial authorization.

## Amendment — 2026-06-14 (owner): attended-automated, human-mimicking pace

Tier-1's pace constraint is amended (dated; original preserved here, not silently
rewritten).

- **Original (2026-06-13):** "Human pace: human-scrolling rate only — no automated
  crawling, no scheduled scraping, no mass extraction."
- **Amended (2026-06-14, owner):** attended **automated** capture is permitted, but
  paced to imitate a human — a variable, irregular, human-speed scroll/fetch cadence
  (an ADHD-like rhythm), explicitly **not** uniform machine-rate, high-throughput
  blasting, or continuous/24-7 operation.

Unchanged: the anti-mass-extraction, no-standing/scheduled-crawler, attended,
≤5-account, pre-commercial, internal-only, US-first, and buy-at-commercial
constraints. Only the manual-vs-automated method is relaxed, and only to a
human-mimicking cadence. "Human pace" elsewhere in this record now reads as this
human-mimicking automated cadence.

## Amendment — 2026-06-14 (owner): scope of the ≤5-account / attended-capture cap

Owner-adjudicated in the demand-read-taxonomy lane (Q3; dated, original preserved).
The Tier-1 small-scale **capture** constraints — **≤5 accounts, attended
human-mimicking pace, IG-first sequencing, Social Blade discipline** — are scoped
to **social-platform creator capture (Instagram / TikTok / equivalent)**, the
ToS-risky scraping context they were written for. **Named public-figure
wind-caller calibration from other public outputs** (public web, detector venues,
public statements — not platform scraping) **is allowed more broadly**, subject to
**non-permanence**: records are time-bounded (retention/purge horizon per this
record), never permanent person dossiers. The "≤5 accounts" wording elsewhere in
this record now reads as this platform-capture-scoped cap.

Unchanged: internal judgment/calibration **use** only; and the **external/product
boundary** — Orca never sells or externally publishes a person-level surface
(Tier 3, permanent). This amendment relaxes only the *capture* cap for
non-platform named-public-figure calibration; it does **not** loosen the
external/product boundary. Selling or publishing any person-level surface remains
a separate charter-level decision, not granted here. Propagated surface: the
demand-read taxonomy's wind-caller boundary (Layer 2 / calibration read-type /
non-claims), updated the same day.

## Amendment — 2026-06-14 (owner): retention horizon set to 10 years, with takedown-on-request

The signed posture leaves the specific retention/purge horizon for the owner to set before
the first session. The owner sets it (dated):

- **Horizon: 10 years from capture, then purge** — longer than the proof-phase-duration
  default, to support a durable call-vs-outcome calibration time-series. (Rationale: most
  wind-callers won't persist near that long anyway, so 10 years is a generous-but-bounded
  ceiling, not indefinite accumulation.)
- **Standing commitment:** immediate takedown / purge on request — any subject, platform, or
  legal removal request is honored promptly.
- This **stays within** the signed "time-bounded, not permanent" posture (10 years is
  bounded); it simply fills in the owner-set horizon, longer than the default. **Not a
  reversal.** (Consistent with the ≤5-account-scope amendment above, which requires
  non-permanence — this sets the bounded horizon that amendment refers to.)

**Unchanged:** every other Tier-1 constraint (≤5 accounts at any one time, attended +
human-mimicking cadence, no standing/scheduled crawler, no mass extraction, pre-commercial,
internal-only, US-first, buy-at-commercial) and all Tier-3 exclusions.

## Amendment — 2026-06-15 (owner): the cap counts OUR operating accounts (not subjects), ≤10; active/passive method

Owner-adjudicated 2026-06-15 (creator-momentum lane). This **supersedes the count and the
referent** of the small-scale cap in the prior records above — which read "≤5 accounts" and, in
context, as ≤5 subject creators. Those prior dated lines are preserved as history; this amendment
governs going forward.

- **What the cap counts:** a ceiling on **Orca's own operating/capture accounts** (the
  accounts/sessions WE use to capture), **NOT** the number of subject creators. **Ceiling: ≤10**
  (operations start at ≤5; ≤10 is written now to avoid a future re-propagation).
- **Subject-creator roster: uncapped.** The calibration roster target is **all creators within the
  vertical** (e.g. all of a beauty sub-niche); the "small scale" framing no longer applies to the
  subject side.
- **Method — active / passive:**
  - **Active** (discovery + capture-target decisions) stays **attended** (human-initiated/supervised).
  - **Passive** (time-series monitoring of **already-flagged** creators) may run **human-initiated,
    time-bounded, and self-terminating** — it runs, captures over a defined period, then turns off;
    **no discovery during it.** This is **not** a perpetual/scheduled standing crawler, which remains
    forbidden.
  - Pace: **faster than human, but not takedown-risking.**
- **ToS risk:** owner-accepted at this scope.
- **Deliberately relaxed:** the small-scale subject cap (now all-in-vertical) and the strict
  "attended"/"human-mimicking pace" requirement for the bounded passive-monitoring phase.
- **UNCHANGED:** the external/product person-level boundary (Orca never sells/publishes a
  person-level surface); non-permanence + 10-year retention + takedown-on-request; commercial scale →
  licensed/bought data.

This is a doctrine change; its downstream surfaces are propagated under the
`direction_change_propagation` receipt at the foot of this record (creator-momentum
cap-redefinition, 2026-06-15).

## Amendment — 2026-06-22 (owner; council-cleared except Tier-2-A): logged-in capture for IG/TikTok; Tier-2-B activated; Tier-2-A authorized-pending-legal

Owner-adjudicated 2026-06-22 with legal-counsel input (creator-momentum / fragrance lane). Dated; prior
lines preserved as history.

- **Access mode — logged-in own-account capture for IG + TikTok (council-cleared).** IG and TikTok capture
  will run **logged in with our own operating accounts**, not logged-out-only. This is **within** the
  already-permitted scope of this carve-out ("Orca's own operating/capture **accounts/sessions**", 2026-06-15
  amendment) — **not a new grant**. It supersedes the *operational* "logged-out-first" recommendation in the
  IG findings/recon docs (which chose logged-out for lower account-risk); that recommendation is **superseded
  for IG/TikTok** (see those docs' pointers). Council-cleared 2026-06-22 as acceptable/low-risk **at internal
  pre-commercial scope** (not sold; no public person-level surface). **UNCHANGED:** the ≤10 / start-≤5
  operating-account ceiling, human-mimicking cadence, no standing/scheduled crawler. **YouTube is
  unaffected** — it stays anonymous logged-out (its public data needs no login).
- **Tier-2-B — cross-platform PUBLIC-handle stitching: ACTIVATED (council-cleared).** The Tier-2-B
  pre-conditions (separate dated authorization + legal review) are met for **public-handle↔public-handle**
  joins by this dated authorization + council clearance 2026-06-22. Build routes through a dedicated
  **linkage spec** (the link-confidence model). **Residuals:** **non-public-handle joins remain gated**
  (still need separate legal); linkage is probabilistic — some links wrong, bounded by the link-score, not
  eliminated. **Tier-3** real-person de-anonymization / contact stays excluded.
- **Tier-2-A — aggregate audience demographics (the audience-graph slice): AUTHORIZED, ACTIVATION
  LEGAL-PENDING.** Owner-authorized 2026-06-22; **activation gated on council confirmation** of the Tier-2-A
  lawful-basis + data-minimization pre-conditions. Binding posture on activation: **aggregate-only**
  distribution (age-band / gender / geo / language), from **TEXT signals only** (name/bio/location/language —
  **no facial/biometric inference**), **legitimate-interests** lawful basis, **transient processing with NO
  retention of individual follower data**, and **NO special-category attributes** (ethnicity/health/politics/
  religion/sexuality). Remains **deferred** until council confirms; this activates only the demographics
  slice, not the full follower-network analysis.
- **Tier-3 — permanent exclusions: UNCHANGED.** Special-category data (health, biometrics, political views,
  etc.), contact/outreach/lead-lists, genuinely private data, and resale/sold person-level product remain
  absolute. The header `stale_if` EU/UK legitimate-interest/retention assessment still applies — the
  Tier-2-A legal-pending gate covers exactly this for the audience layer.

Downstream surfaces propagated under the `direction_change_propagation` receipt at the foot of this record
(2026-06-22, logged-in + Tier-2 activation).

## Amendment — 2026-06-23 (owner; council-confirmed): Tier-2-A council confirmation received

Owner reported council confirmation 2026-06-23 (creator-momentum / fragrance lane). Dated; the
2026-06-22 lines preserved as history.

- **Tier-2-A — aggregate audience demographics: COUNCIL-CONFIRMED; activation no longer legal-gated.**
  Council confirmed the lawful-basis (legitimate interests) + data-minimization safeguards for the
  Tier-2-A slice. The binding posture is **UNCHANGED and now confirmed acceptable**: aggregate-only
  (age-band / gender / geo / language), **TEXT signals only** (no facial/biometric inference),
  legitimate-interests basis, **transient processing with NO retention of individual follower data**,
  **NO special-category attributes**. The 2026-06-22 "activation-legal-pending" gate is **cleared**.
- **Remaining activation gates are now BUILD/DATA, not legal:** (1) a roster-ledger
  aggregate-audience-attribute **schema home** (the ledger currently forbids demographic fields); (2) for
  the category→gender component specifically, the owner-adopted (2026-06-23) **defeasible documented
  base-rate prior** is **data-first** — it needs a sourced, versioned per-category base-rate table before
  it produces gender/age output. A general base rate is obtainable to start, refined over time.
- **Category→gender treatment (adjudicated 2026-06-23):** a **defeasible documented base-rate prior** — a
  Bayesian distribution that creator-specific evidence updates and overrides, with prior-dominated vs
  evidence-dominated transparency, base rates **sourced + versioned (not model-gut)**. It is **confined to
  the Tier-2-A slice** and never used as a hard category→gender map; the Tier-1 slice never votes gender.
- **Tier-3 — permanent exclusions: UNCHANGED** (absolute). Person special-category data, contact/outreach/
  lead-lists, private data, and resale/person-level product remain excluded.

direction_change_propagation (2026-06-23; product_doctrine + lifecycle_boundary):
- trigger: product_doctrine (Tier-2-A legal gate cleared) + lifecycle_boundary (gate type shifts legal → build/data).
- downstream surfaces updated by this change:
    — Tier-2-A pointers bumped "pending council" → "council-confirmed 2026-06-23; remaining gate = ledger-schema home (+ base-rate data)".
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
    — privacy-invariant note bumped Tier-2-A "AUTHORIZED-pending council" → "council-confirmed; gated on a ledger-schema home".
- unchanged: Tier-2-B (already active), Tier-3 (forbidden), the ≤10/start-≤5 operating-account ceiling, logged-in posture.

## The Prior Boundary (baseline)

All Orca product and capture doctrine to date has held:

> "Wind callers are channels, not persons — tracked only through their public
> output and call record; person-level dossiers remain forbidden."

This carve-out amends that boundary in one bounded direction only. Every other
person-level exclusion is unchanged (see Tier 3 — Permanent Exclusions below).

## Tier 1 — Allowed Now (this carve-out)

For **internal wind-caller calibration only**, Orca may:

1. Identify an individual **public-figure** creator/influencer wind-caller by their
   **public handle and public name** as the calibration subject.
2. Record their **public outputs** — the "calls" (Call): posts, reviews, endorsements,
   trend participations — as dated calibration entries.
3. Record **public stats**: follower count, engagement rate, rank time-series,
   paid-promotion / sponsorship disclosure flags, trend-participation records.
4. Record **Orca's internal call-vs-outcome calibration**: how each wind-caller's
   public calls compared against observed market outcomes (Outcome) over time.

**Posture and constraints (non-negotiable within Tier 1):**

- Pre-commercial recon / bootstrap only.
- Small scale: **no more than 5 accounts** under this carve-out at any one time. *(Amended
  2026-06-15 — see amendment above: "accounts" = Orca's own operating/capture accounts, ceiling ≤10 /
  start ≤5; the subject-creator roster is uncapped / all-in-vertical; active=attended,
  passive=bounded self-terminating monitoring.)*
- Human-mimicking pace (amended 2026-06-14, see above): attended **automated**
  capture is permitted, but it must imitate human behaviour — a variable,
  irregular, human-speed scroll/fetch cadence (an ADHD-like rhythm), explicitly
  **not** a uniform machine rate, high-throughput blast, or continuous/24-7
  operation. No standing or scheduled crawler; no mass extraction.
- ToS risk: accepted by the owner at this scale, consistent with the project's
  measured-ToS-risk posture. At commercial scale, this becomes non-negotiable:
  licensed or bought data only.
- Platform sequencing: **Instagram (IG) first**; TikTok and other platforms later,
  under the same discipline.
- **Social Blade** may be read under the same discipline (free tier, human pace,
  pre-commercial). Social Blade data is second-hand (aggregated from platform
  feeds); it is suitable for stats (follower/rank time-series) but verbatim
  first-party call text must come from the public profile directly, not Social
  Blade. At commercial scale, Social Blade data also migrates to a licensed
  arrangement — non-negotiable.

**Use boundary:** internal judgment and calibration **only**. The compounding
asset is the calibration ledger ("who actually calls beauty winds, with receipts"),
not a public or sold data product. See Tier 3 for the permanent external exclusion.

**Retention posture: [Horizon SET 2026-06-14 — see "Amendment — 2026-06-14 (owner):
retention horizon set to 10 years, with takedown-on-request" above. The time-bounded
posture below STANDS; the amendment fills in the owner-set horizon (10 years) and adds
takedown-on-request.]** calibration records are
**time-bounded**, not permanent. The
owner will set a specific retention/purge horizon before the first calibration
session begins; records past their retention date are purged, not accumulated
indefinitely. Default posture: retain for the active proof-phase duration; review
for purge on any commercial-scale trigger or annual review, whichever comes first.

**Geography:** US-first creators (relying on CCPA publicly-available-information
exemption for public figures). Any EU or UK creator must be flagged and assessed for
a legitimate-interest basis and retention compliance **before** inclusion in the
calibration set.

## Tier 2 — Allowed-But-Deferred (sanctioned future capability, gated)

These capabilities are **not collected or activated now**. They are reclassified
from out-of-scope → **sanctioned-but-deferred**: each requires its own dated
authorization and a legal-gate check before any activation.

**A. Audience / follower-graph analytics.**
Network analysis of follower, commenter, or connection graphs for a wind-caller's
audience. The idea is analytically useful. It is deferred because it touches
ordinary followers who are not public figures — a **hard legal gate** applies
(GDPR/PIPEDA-style regimes; CCPA ordinary-consumer provisions; not covered by the
public-figure carve-out). Pre-conditions: separate dated authorization + legal
review + lawful-basis/consent model + data-minimization design.
Home: `docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md`
(reclassified from out-of-scope → sanctioned-but-deferred; see propagation below).

**B. Cross-platform public-handle stitching.**
Linking the same wind-caller's public handles across IG, TikTok, YouTube, etc. into
a unified calibration record. Pre-conditions: separate dated authorization + legal
review for any non-public-handle joins.
Home: `docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md`
(reclassified from out-of-scope → sanctioned-but-deferred; see propagation below).

Neither Tier 2 item is activated by this record. Each needs its own gate. Do not
treat reclassification as authorization. *(Update — 2026-06-22 + 2026-06-23 amendments above:
**Tier-2-B is now ACTIVATED** for public-handle↔public-handle joins (council-cleared);
**Tier-2-A is now COUNCIL-CONFIRMED** (2026-06-23) — the legal gate is cleared; activation gated only on a
ledger-schema home (+ base-rate data for the category→gender prior). See the 2026-06-22 / 2026-06-23
amendments for the exact scope, binding posture, and residuals.)*

## Tier 3 — Permanent Exclusions (unchanged; no carve-out)

These exclusions are **absolute** and are not touched by any tier of this record:

- Contact information, outreach, or lead lists derived from wind-callers.
- Special-category data (health, biometrics, political views, etc.).
- Genuinely private or non-public data (behind auth gates, DMs, private accounts).
- Resale, data-broker activity, or any sold person-level data product.
- Selling or externally publishing a person-level surface of any kind (unchanged;
  this carve-out is internal-only).

**LinkedIn / org-motion boundary:** the LinkedIn org-level person boundary is a
**separate context** and is **completely unchanged** by this record.
LinkedIn routes stay org-level only (hiring composition, headcount — never
person-level dossiers). Do not read this carve-out as touching LinkedIn doctrine.

## What This Record Is Not

- Not validation, readiness, or buyer-proof.
- Not authorization for commercial-scale wind-caller data collection.
- Not Tier-2 activation (neither audience-graph nor cross-platform stitching).
- Not outreach or contact acquisition.
- Not a change to the external/product boundary (Orca never sells or externally
  publishes a person-level surface; claim-defense doctrine governs any external
  sentence).
- Not a change to LinkedIn org-motion doctrine.

---

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has a bounded owner-signed carve-out permitting internal
    creator/influencer wind-caller calibration (public handle + public name +
    public calls + public stats + call-vs-outcome calibration) at small scale
    (≤5 accounts), human pace, pre-commercial only; commercial scale triggers
    licensed/bought-data posture (non-negotiable). The "wind callers = channels
    not persons" boundary is amended only to this extent; all other person-level
    exclusions and the external/product boundary are unchanged. Two previously
    out-of-scope capabilities (audience/follower-graph analytics and
    cross-platform public-handle stitching) are reclassified to
    sanctioned-but-deferred with their own legal gates.
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/wind_caller_calibration_carveout_v0.md   # this record (new)
    - docs/product/product_lead/orca_demand_read_taxonomy_v0.md
    - docs/product/product_lead/orca_product_proof_lead_charter_v0.md
    - docs/product/product_lead/orca_buyer_proof_packet_v0.md
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
    - docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md  # pointer only (line present)
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/product/product_lead/orca_product_proof_lead_charter_v0.md
    - docs/product/product_lead/orca_demand_read_taxonomy_v0.md
    - docs/product/product_lead/orca_buyer_proof_packet_v0.md
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
    - docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md
    - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
  intentionally_not_updated:
    - path: docs/product/product_lead/orca_demand_read_taxonomy_v0.md
      note: "wind-caller section (lines 57-60) amended with pointer; external/product boundary unchanged"
    - path: AGENTS.md
      reason: >
        AGENTS.md routes doctrine to the overlay; this carve-out is a
        product-doctrine change that lives in docs/decisions/ and is pointed
        to from the product surfaces. No root-instruction change needed.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay entrypoint already names source-of-truth.md as the
        propagation owner; no new overlay section was added.
    - path: docs/decisions/turn_08_product_thesis_v0.md
      reason: >
        Superseded by docs/decisions/forseti_product_thesis_consumer_demand_v0.md;
        retained as history per existing doctrine. Must not be edited.
    - path: docs/product/product_lead/orca_product_proof_lead_charter_v0.md
      reason_detail: >
        LinkedIn / org-motion docs are a separate context;
        this carve-out does not touch them.
    - path: "LinkedIn docs (any)"
      reason: >
        LinkedIn org-motion person boundary is a completely separate context
        and is not changed by this carve-out. LinkedIn docs must not be edited.
  stale_language_search: >
    rg -n "wind callers are channels, not persons|person-level dossiers remain forbidden|channels not persons"
    docs/product/product_lead/orca_demand_read_taxonomy_v0.md
    docs/product/product_lead/orca_product_proof_lead_charter_v0.md
    docs/product/product_lead/orca_buyer_proof_packet_v0.md
    docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    docs/product/source_capture_toolbox/source_capture_playbook_v0.md
    docs/decisions/forseti_product_thesis_consumer_demand_v0.md
  stale_language_search_result: >
    Executed on 2026-06-13 before edits; hits identified in:
    docs/product/product_lead/orca_demand_read_taxonomy_v0.md (lines 57-60 — amended with pointer),
    docs/product/product_lead/orca_product_proof_lead_charter_v0.md (line 130 — amended with pointer),
    docs/product/product_lead/orca_buyer_proof_packet_v0.md (line 131 — amended with pointer),
    docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md (line 133 — amended with pointer),
    docs/product/source_capture_toolbox/source_capture_playbook_v0.md (line 71 — amended with pointer),
    docs/decisions/forseti_product_thesis_consumer_demand_v0.md (lines 152-153 — person-level language
    present; pointer added).
    After edits each retained surface carries a pointer to this carve-out and explicitly preserves the
    external/product boundary. No surface retains an unqualified blanket prohibition that would
    contradict the bounded internal carve-out.
  non_claims:
    - not validation
    - not readiness
    - not buyer-proof
    - not commercial scale authorization
    - not Tier-2 activation
    - not outreach authorization
    - not a change to LinkedIn org-motion doctrine
    - not merged; owner adjudicates
```

```yaml
# Retention horizon set 2026-06-14 (owner): bounded 10-year horizon + takedown-on-request (within the time-bounded posture; not a reversal).
direction_change_propagation:
  doctrine_changed: >
    The owner set the Tier-1 retention horizon (which the signed posture delegates to the owner)
    to a bounded 10-years-from-capture-then-purge horizon, longer than the proof-phase default,
    plus a standing immediate-takedown / purge-on-request commitment. This stays WITHIN the signed
    "time-bounded, not permanent" posture (10 years is bounded; not a reversal). All other Tier-1
    bounds and Tier-3 exclusions are unchanged.
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/wind_caller_calibration_carveout_v0.md   # this record (horizon set)
  downstream_surfaces_checked:
    - path: docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md
      note: Delta 3 retention reference set to 10-year horizon + takedown-on-request (recon lane).
  non_claims:
    - not validation
    - not readiness
    - not commercial-scale authorization
    - not a change to the scale / attended / no-standing-crawler bounds
    - not a change to Tier-3 exclusions
    - not legal sufficiency
    - owner-instructed 2026-06-14; owner merge = sign-off
```

```yaml
# Cap re-definition set 2026-06-15 (owner): the ≤N cap counts Orca's OWN operating/capture
# accounts (ceiling ≤10, ops start ≤5), NOT subject creators; subject roster uncapped
# (all-in-vertical); active/passive method posture defined. See the 2026-06-15 amendment above.
direction_change_propagation:
  doctrine_changed: >
    The wind-caller capture cap is re-defined: the ≤N ceiling counts Orca's OWN
    operating/capture accounts (≤10 ceiling; operations start at ≤5), NOT the number of
    subject creators. The subject-creator roster is uncapped (target = all creators within
    the vertical). Method posture is defined in two modes: ACTIVE (discovery + capture-target
    decisions) stays attended/human-initiated; PASSIVE (time-series monitoring of
    already-flagged creators) may run human-initiated, time-bounded, and self-terminating
    with no discovery during it — a perpetual/scheduled standing crawler remains forbidden.
    Pace is faster-than-human but not takedown-risking; ToS risk owner-accepted at this scope.
    This supersedes the prior "≤5 accounts" count and its subject-creator referent. UNCHANGED:
    the external/product person-level boundary, non-permanence + 10-year retention +
    takedown-on-request, and commercial-scale → licensed/bought-data posture.
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/wind_caller_calibration_carveout_v0.md   # this record (2026-06-15 amendment + Tier-1 pointer)
  downstream_surfaces_checked:
    - path: docs/decisions/forseti_product_thesis_consumer_demand_v0.md
      note: Product Boundary wind-caller parenthetical re-framed; external/product boundary preserved verbatim; DCP note added.
    - path: docs/product/product_lead/orca_demand_read_taxonomy_v0.md
      note: Three live sites (Layer-2 boundary, calibration read-type, Non-Claims) re-framed; external boundary preserved verbatim; DCP note added.
    - path: docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md
      note: Three live boundary sites re-framed; dated-historical Q3 sites (Status, Q3-decided, Q3 lane-reasoning) received forward-pointing notes only; PLAN block got a dated 2026-06-15 sub-note.
    - path: docs/product/product_lead/orca_product_proof_lead_charter_v0.md
      note: The "What Remains Outside The Role" exception re-framed; external/product person-level boundary preserved verbatim; external activity scope NOT expanded; DCP note added.
    - path: docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md
      note: Residuals (H5) + Posture/carve-out re-framed; retention + commercial clauses preserved verbatim; DCP note added.
    - path: docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md
      note: stale_if + Posture/carve-out re-framed; discovery-read open question marked RESOLVED by the active/passive posture; DCP note added.
    - path: docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md
      note: YAML scope header, Authorization-map Covered cell, and Cadence governor ceiling re-framed; dated 2026-06-14 owner-confirmation receipts forward-noted (not retro-edited); DCP note added.
    - path: docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md
      note: Posture/bounds + method-posture re-framed; dated 2026-06-14 PR #73 receipt and probe n=2 facts left untouched; DCP note added.
    - path: docs/product/source_capture_toolbox/source_capture_playbook_v0.md
      note: Risk-posture dossier-carve-out exception re-framed; "does not change the general dossier prohibition" preserved verbatim; DCP note added.
    - path: docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md
      note: H5 residual + non-claims carve-out-posture reference re-framed; n=1 @hyram probe facts left untouched; DCP note added. (Caught in this lane's stale-language sweep; not in the original propagation set.)
  intentionally_not_updated:
    - path: docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
      reason: >
        Owned and landed by the parallel ontology-backbone lane (committed aed85c4d on the
        primary repo). This worktree's working tree also carries the new framing for this file,
        but it is intentionally NOT included in this lane's cap-propagation commit to avoid a
        competing version; the ontology lane owns it.
    - path: docs/decisions/wind_caller_calibration_carveout_v0.md (the 2026-06-13 carve-out receipt and the 2026-06-14 retention receipt above)
      reason: Dated-historical receipts; preserved verbatim. The 2026-06-15 amendment supersedes the prior count/referent in-doc via a forward note; the historical receipts are not retro-edited.
    - path: docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
      reason: Carries no live ≤5 capture-cap framing (confirmed by sweep); the carve-out pointer it holds resolves to the now-amended record.
    - path: docs/product/product_lead/orca_buyer_proof_packet_v0.md
      reason: Carries no live ≤5 capture-cap framing (confirmed by sweep).
    - path: docs/product/source_capture_toolbox/ig_creator_discovery_suggested_accounts_recon_v0.md
      reason: Recon finding; carries no live ≤5 capture-cap framing (confirmed by sweep).
    - path: docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md
      reason: Carries no live ≤5 capture-cap framing (confirmed by sweep).
    - path: "ontology-review artifacts (docs/review-outputs/.../ontology_commission_refresh_delegated_review_v0.md and siblings)"
      reason: Dated review records that legitimately quote both old and new cap wording as a review diff; not live doctrine surfaces.
  stale_language_search: >
    git grep -n -iE "(≤5|<=5|five|[^0-9]5)[ -]?(account|public-figure|creator)" -- docs/
  stale_language_search_result: >
    Ran 2026-06-15 after the propagation edits. The only residual LIVE ≤5 capture-cap surface
    was docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md
    (H5 residual + non-claims) — now re-framed and listed above. All other ≤5 occurrences are
    either this record's own baseline lines (which the 2026-06-15 amendment explicitly supersedes
    in-doc) or dated-historical receipts/decision records already carrying forward-pointing notes.
    No live surface retains the superseded "≤5 subject-creator" reading.
  non_claims:
    - not validation
    - not readiness
    - not buyer-proof
    - not commercial-scale authorization
    - not Tier-2 activation
    - not a change to the external/product person-level boundary
    - not a change to non-permanence / 10-year retention / takedown-on-request
    - not a change to LinkedIn org-motion doctrine
    - not merged; owner adjudicates (lane PR flow; landing to main is human-gated)
```

```yaml
# Logged-in capture + Tier-2 activation set 2026-06-22 (owner; council-cleared except Tier-2-A pending). See the 2026-06-22 amendment above.
direction_change_propagation:
  doctrine_changed: >
    IG/TikTok capture will run logged-in with our own operating accounts (WITHIN the already-permitted
    operating-account/session scope; supersedes the IG findings' OPERATIONAL "logged-out-first"
    recommendation; YouTube unaffected, stays anonymous logged-out). Tier-2-B cross-platform PUBLIC-handle
    stitching is ACTIVATED for public-handle joins (dated authorization + council clearance 2026-06-22;
    non-public-handle joins remain gated; build via a dedicated linkage spec). Tier-2-A aggregate audience
    demographics is AUTHORIZED but ACTIVATION-LEGAL-PENDING council confirmation of the lawful-basis +
    data-minimization design (binding on activation: aggregate-only, text-only / no-biometric,
    legitimate-interests, transient / no individual retention, no special-category). UNCHANGED: Tier-3
    permanent exclusions, the external/product person-level boundary, the ≤10/start-≤5 operating-account
    ceiling, non-permanence + 10-year retention + takedown-on-request.
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - docs/decisions/wind_caller_calibration_carveout_v0.md   # this record (2026-06-22 amendment + Tier-2 annotation)
  downstream_surfaces_checked:
    - path: orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
      note: Privacy/Forbidden-in-v0 section got a pointer note — cross-platform public-handle stitching now activated (Tier-2-B); aggregate audience demographics authorized-pending (Tier-2-A); person special-category still forbidden (Tier-3).
    - path: orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md
      note: Auth/route-posture "logged-out-first" recommendation pointer-superseded for IG/TikTok by this amendment.
  intentionally_not_updated:
    - path: ig_at_scale_operating_envelope_v0.md ; ig_r_probe_results_v0.md ; ig_logged_out_sustainability_probe_plan_v0.md
      reason: >
        Record logged-out PROBE EVIDENCE / a logged-out probe PLAN — still accurate as measurements/plan;
        the logged-in posture is a forward operational choice, not a retro-correction of past probes. The
        carve-out is the authority and the consolidated findings doc carries the forward pointer.
    - path: ig_wind_caller_capture_feasibility_recon_v0.md ; orca_creator_monitoring_policy_architecture_v0.md
      reason: >
        Recon finding / restatement-by-reference of "Tier-2 not activated" + the ledger's cross-platform rule;
        the carve-out (authority) + the ledger pointer cover the forward routing (point-don't-duplicate).
    - path: youtube tooling + docs
      reason: anonymous logged-out posture unchanged; this change is IG/TikTok-scoped.
  stale_language_search: >
    git grep -niE "logged-out-first|session.*(fallback|default)|cross-platform identity stitch|stitch" --
    orca/product/spines/capture/core/source_families/social_media/instagram/
  stale_language_search_result: >
    Run 2026-06-22 on this branch (off origin/main 666c4f14). Live surfaces found: ig_capture_findings_consolidated
    (logged-out-first conclusion — POINTER added), ig_creator_roster_frontier_ledger (cross-platform "Forbidden in v0"
    + "must not be cross-platform stitched without a separate owner-approved spec" — POINTER added; the carve-out
    is that separate owner approval), ig_at_scale_operating_envelope / ig_r_probe_results / ig_logged_out_sustainability_probe_plan
    (logged-out as evidence/plan, not a forward rule — intentionally_not_updated), ig_wind_caller_capture_feasibility_recon /
    orca_creator_monitoring_policy ("Tier-2 not activated" / cross-platform restatement — intentionally_not_updated, covered
    by the carve-out + ledger pointer). After the two pointers, no LIVE forward-routing surface contradicts this amendment.
  non_claims:
    - not validation
    - not readiness
    - not commercial-scale authorization
    - not Tier-2-A activation (legal-pending council confirmation)
    - not a change to Tier-3 exclusions or the external/product person-level boundary
    - not merged; owner adjudicates (lane PR flow; landing to main is human-gated)
```
