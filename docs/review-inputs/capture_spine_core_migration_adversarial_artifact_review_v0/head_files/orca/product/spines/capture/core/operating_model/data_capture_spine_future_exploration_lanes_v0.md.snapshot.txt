```yaml
retrieval_header_version: 1
artifact_role: Future-exploration backlog (non-authorizing, capture-spine level)
scope: >
  Deliberately-deferred, legally-gated capture-spine capabilities surfaced during the
  LinkedIn Discovery & Planning Lane design, plus two capabilities reclassified from
  out-of-scope to sanctioned-but-deferred by the wind-caller calibration carve-out
  (docs/decisions/wind_caller_calibration_carveout_v0.md, 2026-06-13):
  audience/follower-graph analytics (Tier 2A) and cross-platform public-handle
  stitching (Tier 2B). Records the idea, why it is deferred/gated, and preconditions.
use_when:
  - Someone proposes relationship-graph analytics or contact/outreach inside a discovery lane.
  - Scoping a future, separately-authorized lane for audience-graph, handle-stitching, or outreach.
  - Checking whether audience/follower-graph or cross-platform stitching is authorized.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/wind_caller_calibration_carveout_v0.md   # Tier 2 reclassification authority
```

# Data Capture Spine — Future Exploration Lanes (v0)

## What this is — and is not

This is a **capture-spine-level backlog of deferred capabilities**, surfaced while
designing the LinkedIn Discovery & Planning Lane, plus two items reclassified by the
2026-06-13 wind-caller calibration carve-out
(`docs/decisions/wind_caller_calibration_carveout_v0.md`) from out-of-scope to
**sanctioned-but-deferred** (Tier 2A audience/follower-graph analytics and Tier 2B
cross-platform public-handle stitching). It is **not authorized work, not a
build spec, and not legal advice.** Each item below remains deferred and may be
activated only under **its own** dated authorization + legal gate.

Nothing here changes the current discovery lane's Hard Stops or Non-Claims. The
discovery lane continues to forbid these capabilities; this doc only records *where
they would live if pursued* and *what would have to be true first*.

## Future Exploration A — Audience / Follower-Graph Analytics Lane

**Classification (2026-06-13):** Reclassified from out-of-scope →
**sanctioned-but-deferred** (Tier 2A) by `docs/decisions/wind_caller_calibration_carveout_v0.md`.
Requires own dated authorization + **hard legal gate** before any activation
(touches ordinary followers, not public figures).

**The idea.** Apply data science to follower / connection / commenter relationship
graphs — network analysis, influence mapping, community detection — which is
genuinely useful analytically.

**Why it is OUT of every discovery lane (and must not be activated without a legal gate).** Building or retaining these graphs is the
single highest-risk capability surfaced in the LinkedIn design:

- it is squarely against LinkedIn's Terms of Service;
- it is the behavior at the center of the major scraping disputes (e.g. hiQ v.
  LinkedIn, Clearview AI);
- under GDPR/PIPEDA-style regimes it is surveillance-grade processing of individuals
  who never consented and who are mostly **not** public actors;
- it flips the spine's posture from *outside-in public-signal intelligence* to
  *social-graph harvesting*.

**Boundary (hard line).** No discovery/planning lane ever emits, retains, or builds
follower / connection / commenter / relationship / employment / org-chart / contact
graphs. Visible *counts or coarse bands* (and their trend over time) remain allowed
context; the **graph itself** does not.

**Preconditions to revisit.** A separate, explicitly-authorized lane; legal review;
a lawful basis and entitlement/consent model; data-minimization by design; and a
clear statement of who the data subjects are and on what basis they are processed.
Never folded into discovery.

## Future Exploration B — Cross-Platform Public-Handle Stitching

**Classification (2026-06-13):** Reclassified from out-of-scope →
**sanctioned-but-deferred** (Tier 2B) by `docs/decisions/wind_caller_calibration_carveout_v0.md`.
Requires own dated authorization + legal review before any activation.

**The idea.** Link the same wind-caller's public handles across IG, TikTok, YouTube,
and other platforms into a unified calibration record — useful for cross-platform
call-accuracy grading.

**Why it is deferred.** At the public-handle level (linking @handle on IG to
@handle on TikTok) the risk is lower than audience-graph. However, any join beyond
the public-handle layer (private handles, follower-level data, cross-platform
audience overlap) raises the same legal concerns as Tier 2A and must be gated
separately.

**Boundary.** Public-handle stitching at the wind-caller level only; no audience
data, no cross-platform follower lists. Any broader cross-platform join requires its
own legal assessment.

**Preconditions to activate.** Separate dated authorization; legal review for any
non-public-handle joins; data-minimization design; explicit authorization.

---

## Future Exploration C — Contact / Outreach Lane

**The idea.** B2B contact and outreach — including the question of whether contact
acquisition is acceptable "because it's B2B."

**The distinction that matters.** *Harvesting* (mass extraction of personal contact
data — emails, phones, private contact routes) is **not** the same as *contacting a
business via its published or consented channels*. The first is the hard-stopped
behavior; the second is a legitimate outreach activity with its own legal basis.

**Why it is OUT of every discovery lane.**

- Discovery is **planning**, not outreach — different stage, different authority.
- Even **B2B** personal contact data is personal data under GDPR; harvesting also
  implicates CAN-SPAM / CASL / ePrivacy and LinkedIn ToS.
- Contact acquisition and outreach are explicitly named Non-Claims / Hard Stops of
  the discovery lane.

**Boundary (hard line).** No discovery/planning lane harvests contacts or performs
outreach. Outreach is a separate lane.

**Preconditions to revisit.** A separate **Outreach Lane**; legal review; a lawful
basis + consent / published-channel model; no harvesting; and explicit authorization.

## Cross-cutting

- All three items require **legal review** and a **separate explicit authorization**
  before any activation — none is implied by the discovery lane's existence or by
  the wind-caller Tier 1 carve-out.
- None changes the current discovery lane Hard Stops or Non-Claims.
- All three are **out of scope** for the LinkedIn Discovery & Planning Lane and for
  the capture spine's current build scope.
- Tier 2A (audience/follower-graph) and Tier 2B (cross-platform stitching) are
  reclassified to sanctioned-but-deferred by
  `docs/decisions/wind_caller_calibration_carveout_v0.md`; Tier 2C (contact/outreach)
  remains out-of-scope (no reclassification).

## Non-claims

This document is **not** an authorization, **not** a build spec, **not** legal advice,
**not** a validation or readiness claim, and confers **no** permission to build,
capture, harvest, or process. It is a forward-looking exploration record only.
