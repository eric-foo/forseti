# Wind-Caller Calibration Carve-Out v0

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
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md   # wind-caller read type
  - docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md  # Tier 2 deferred items
  - docs/product/product_lead/orca_product_proof_lead_charter_v0.md  # external boundary unchanged
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
2. Record their **public outputs** — the "calls": posts, reviews, endorsements,
   trend participations — as dated calibration entries.
3. Record **public stats**: follower count, engagement rate, rank time-series,
   paid-promotion / sponsorship disclosure flags, trend-participation records.
4. Record **Orca's internal call-vs-outcome calibration**: how each wind-caller's
   public calls compared against observed market outcomes over time.

**Posture and constraints (non-negotiable within Tier 1):**

- Pre-commercial recon / bootstrap only.
- Small scale: **no more than 5 accounts** under this carve-out at any one time.
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

**Retention posture:** calibration records are **time-bounded**, not permanent. The
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
treat reclassification as authorization.

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
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md  # pointer only (line present)
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
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
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
        Superseded by docs/decisions/orca_product_thesis_consumer_demand_v0.md;
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
    docs/decisions/orca_product_thesis_consumer_demand_v0.md
  stale_language_search_result: >
    Executed on 2026-06-13 before edits; hits identified in:
    docs/product/product_lead/orca_demand_read_taxonomy_v0.md (lines 57-60 — amended with pointer),
    docs/product/product_lead/orca_product_proof_lead_charter_v0.md (line 130 — amended with pointer),
    docs/product/product_lead/orca_buyer_proof_packet_v0.md (line 131 — amended with pointer),
    docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md (line 133 — amended with pointer),
    docs/product/source_capture_toolbox/source_capture_playbook_v0.md (line 71 — amended with pointer),
    docs/decisions/orca_product_thesis_consumer_demand_v0.md (lines 152-153 — person-level language
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
