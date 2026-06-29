```yaml
retrieval_header_version: 1
artifact_role: Future-exploration backlog (non-authorizing, capture-spine level)
scope: >
  Capture-spine residual backlog for gated capabilities surfaced during the
  LinkedIn Discovery & Planning Lane design and wind-caller calibration carve-out.
  Tier-2-B public-handle-to-public-handle stitching is now activated only through
  the dedicated linkage spec; Tier-2-A audience/follower-graph analytics,
  non-public-handle joins, and contact/outreach remain gated residuals.
use_when:
  - Someone proposes relationship-graph analytics or contact/outreach inside a discovery lane.
  - Scoping a future lane for audience-graph, non-public-handle joining, handle-stitching, or outreach.
  - Checking whether audience/follower-graph or cross-platform stitching is authorized.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
```

# Data Capture Spine — Future Exploration Lanes (v0)

## What This Is And Is Not

This is a capture-spine-level residual backlog. It was first written when Tier
2A audience/follower-graph analytics and Tier 2B cross-platform public-handle
stitching were sanctioned-but-deferred. Later amendments in
`docs/decisions/wind_caller_calibration_carveout_v0.md` supersede that historical
state for one narrow case: Tier-2-B public-handle-to-public-handle joins are now
activated and route through
`orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md`.

This file remains the warning surface for the residuals: audience/follower
analytics, non-public-handle joins, and contact/outreach. It is not legal
advice, not runtime authorization, not capture authorization, not a public
person-level product surface, and not a database or schema migration.

Nothing here changes the current discovery lane's Hard Stops or Non-Claims.
Discovery lanes still do not harvest contacts, build follower graphs, or turn
public account linkage into real-world identity proof.

## Future Exploration A — Audience / Follower-Graph Analytics Lane

**Classification:** Tier-2-A aggregate audience demographics are council-confirmed
under the current wind-caller carve-out only in the narrow aggregate/text-only
posture named there. Follower, connection, commenter, or audience graph
analytics remain gated and outside discovery lanes.

**Schema-home boundary.** The carve-out's remaining Tier-2-A activation gate is a
separate aggregate-audience-attribute schema home; that home is its own
architecture decision and is **not** the public-handle linkage ledger, whose
validator forbids demographic/audience fields. Do not add aggregate-audience or
ideal-audience attributes to the linkage ledger rows.

**The idea.** Apply data science to follower / connection / commenter relationship
graphs — network analysis, influence mapping, community detection — which is
genuinely useful analytically.

**Why it is OUT of every discovery lane.** Building or retaining these graphs is
the single highest-risk capability surfaced in the LinkedIn design:

- it is squarely against LinkedIn's Terms of Service;
- it is the behavior at the center of the major scraping disputes (e.g. hiQ v.
  LinkedIn, Clearview AI);
- under GDPR/PIPEDA-style regimes it is surveillance-grade processing of individuals
  who never consented and who are mostly not public actors;
- it flips the spine's posture from outside-in public-signal intelligence to
  social-graph harvesting.

**Boundary.** No discovery/planning lane ever emits, retains, or builds follower
/ connection / commenter / relationship / employment / org-chart / contact
graphs. Visible counts or coarse bands, when separately allowed by the owning
source-family contract, are not graph retention.

**Preconditions to revisit.** A separate, explicitly-authorized lane; legal
review where required; lawful basis and entitlement/consent model; data
minimization by design; and a clear statement of who the data subjects are and
on what basis they are processed. Never folded into discovery.

## Future Exploration B — Cross-Platform Public-Handle Stitching

**Classification update:** Reclassified from out-of-scope to
sanctioned-but-deferred on 2026-06-13, then activated for
public-handle-to-public-handle joins by the 2026-06-22 amendment in
`docs/decisions/wind_caller_calibration_carveout_v0.md`. The build route is the
dedicated linkage spec at
`orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md`.

**The idea.** Link the same wind-caller's public handles across IG, TikTok,
YouTube, and other platforms into a unified calibration record for
cross-platform call-accuracy grading.

**Active boundary.** Public-handle-to-public-handle joins only, at the
wind-caller/public-creator-account level. The linkage spec requires evidence
states, source pointers, human review for final links, and non-claims that the
cluster is not real-world identity proof.

**Residual boundary.** Any join beyond the public-handle layer remains gated:
private handles, contact data, legal or inferred real names, follower-level data,
cross-platform audience overlap, and person-level product surfaces are not
included in the Tier-2-B public-handle activation.

**Current build home.** Static table-shaped ledger plus validator first; SQLite
or another database is a later migration after the row model and evidence rules
survive synthetic/adversarial tests.

## Future Exploration C — Contact / Outreach Lane

**The idea.** B2B contact and outreach — including the question of whether
contact acquisition is acceptable "because it's B2B."

**The distinction that matters.** Harvesting mass personal contact data — emails,
phones, private contact routes — is not the same as contacting a business via
its published or consented channels. The first is the hard-stopped behavior; the
second is a separate outreach activity with its own legal basis.

**Why it is OUT of every discovery lane.**

- Discovery is planning, not outreach — different stage, different authority.
- Even B2B personal contact data is personal data under GDPR; harvesting also
  implicates CAN-SPAM / CASL / ePrivacy and platform ToS.
- Contact acquisition and outreach are explicitly named Non-Claims / Hard Stops
  of the discovery lane.

**Boundary.** No discovery/planning lane harvests contacts or performs outreach.
Outreach is a separate lane.

**Preconditions to revisit.** A separate Outreach Lane; legal review; a lawful
basis plus consent / published-channel model; no harvesting; and explicit
authorization.

## Cross-Cutting

- Tier-2-B public-handle-to-public-handle joins are active only through the
  dedicated linkage spec and its validator contract.
- Non-public-handle joins remain gated.
- Audience/follower graph analytics remain gated unless a separate owner/legal
  source says otherwise for a narrower aggregate-only slice.
- Contact/outreach remains a separate lane and is never implied by discovery or
  creator ledger work.

## Non-Claims

This document is not legal advice, not validation or readiness, not runtime
capture authorization, not SQLite adoption, not contact/outreach authorization,
not follower/audience graph authorization, not non-public-handle join
authorization, and not a public person-level product surface.