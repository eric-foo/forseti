# Orca Discovery Candidate Scan - Beauty Sub-Niche ChatGPT Pro Intake v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  Advisory intake of a ChatGPT Pro web-research response on Orca's first
  beauty/personal-care sub-niche, preserving its source gap, recommendation,
  candidate contexts, and no-contact next scan.
use_when:
  - Reviewing the external ChatGPT Pro sub-niche recommendation before deciding
    whether to run a formal no-contact candidate scan.
  - Checking why indie fragrance/scent-layering is the current first bet to test.
  - Separating candidate contexts from buyers, leads, proof, or outreach.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/chatgptpro_beauty_subniche_research_prompt_v0.md
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - orca/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md
stale_if:
  - A verified no-contact candidate scan supersedes this external intake.
  - The buyer-proof gate, first commercial target, or demand-read taxonomy changes.
  - The source gap below is rerun cleanly and changes the recommendation.
```

## Status

Status: `ADVISORY_EXTERNAL_RESEARCH_INTAKE`.

This artifact preserves an external ChatGPT Pro response supplied by the owner
from:

`C:\Users\vmon7\.codex\attachments\b7f28ea5-f47c-4148-b5b3-db7545bbcfd0\pasted-text.txt`

It is not a verified Orca candidate scan, not buyer proof, not outreach
authorization, not capture authorization, not product readiness, not commercial
readiness, and not a filled target-slot instrument.

## Visible Source Gap From The External Response

The external response declared `SOURCE_CONTEXT_READY`, but also reported this
source gap:

- it could not read separate uploaded copies of
  `orca_product_proof_lead_charter_v0.md`,
  `orca_demand_read_taxonomy_v0.md`, or
  `ig_creator_roster_frontier_ledger_spec_v0.md`;
- it saw prompt duplicates plus thesis/wedge/buyer-proof/taxonomy-adjudication
  material under partly mismatched filenames;
- it continued using the available controlling gates.

Treat the recommendation as directional until either:

- a cleaner rerun reads the full source pack; or
- a no-contact scan verifies candidate contexts directly against current Orca
  gates.

This gap does not by itself overturn the result, because the received answer did
read the central buyer-proof gates. It does prevent treating the output as a
complete source-loaded Orca research artifact.

## External Recommendation Captured

The response recommends:

- best first sub-niche: indie fragrance / scent-layering /
  fragrance-adjacent hair and body mists;
- runner-up: scalp and haircare, scoped to scalp-as-skincare and hair-wellness,
  excluding medicalized hair-growth or treatment claims in the first pass;
- avoid first: SPF / sun-makeup / sunscreen-adjacent beauty, because US
  sunscreen regulation and claims substantiation add first-pass complexity.

The recommendation is narrow. It does not say "fragrance broadly." It says to
test founder-led indie/DTC fragrance brands already showing Sephora/Ulta/DTC
traction and making visible decisions about scent-family extension, hair/body
mist versus EDP conversion, discovery/travel/mini formats, inventory depth, and
retail-door expansion.

## Candidate Contexts To Verify

Fragrance contexts surfaced:

| Context | External status | Why it may fit | Verification need |
| --- | --- | --- | --- |
| PHLUR - Vanilla Skin / Missing Person / mist-to-EDP extensions | strong | Founder-visible, waitlist/sellout claims, Sephora/PDP and founder/trade surfaces. | Verify current 30-90 day decision window and independent origins beyond brand/founder narrative. |
| Dedcool - Milk / Mochi Milk / layering franchise | strong | Founder-visible, Sephora inventory sell-through claim, taste-shift and franchise-extension decision surface. | Verify current live decision and separate demand origins from seeded launch/social amplification. |
| Snif - Secret Menu / Ulta expansion / Notewrks | strong | Founder-visible, Ulta expansion, subbrand launch, retail/DTC mix, repeat-purchase claim. | Verify not all decision evidence comes from one trade interview; inspect retailer/PDP and community/review origins. |
| NOYZ - Mylk de Parfum / Ulta-exclusive formats | tentative | Founder-visible and Ulta review surfaces, but less proven as a decision context. | Verify review provenance and live decision window. |
| Ellis Brooklyn - body mists | tentative | Useful body-mist precedent and founder-visible operator surface. | Refresh to a current live 2026 trigger before using as a slot. |

Scalp/haircare contexts surfaced:

| Context | External status | Why it may fit | Verification need |
| --- | --- | --- | --- |
| Divi - scalp serum / Ulta and Ulta-at-Target expansion | strong with claims guard | Founder-visible, retail expansion, high public review surface. | Keep away from medicalized hair-loss claims; verify public-signal usefulness before internal repeat-purchase data. |
| Act+Acre - scalp wellness / Sephora distribution | strong if non-medical | Founder-visible, Sephora presence, inventory financing and review surfaces. | Bound to scalp-wellness and buildup/routine decisions, not clinical claims. |
| Ceremonia - scalp rituals / Sephora scale | tentative | Founder-visible, Sephora distribution, scalp/routine surface. | May be broader haircare, not a clean scalp-first test. |
| Crown Affair - prestige haircare scaling | tentative | Founder/CEO-visible and Sephora scaling context. | Weaker scalp specificity; better as a haircare benchmark than first slot. |

## Spot-Check Notes

A lightweight source spot-check in the Codex lane found the response's core
direction plausible:

- Circana's August 19, 2025 H1 2025 beauty report supports fragrance and scalp
  care as active categories: prestige fragrance up 6% to $3.9B, mini/travel
  fragrance units up 15%, mass fragrance up 17%, and scalp care up 19%.
  Source: `https://www.circana.com/post/us-beauty-industry-grows-in-the-first-half-of-2025-circana-reports`
- FDA's sunscreen Q&A supports treating SPF as a regulated substrate under OTC
  sunscreen requirements rather than a simple beauty trend surface.
  Source: `https://www.fda.gov/drugs/understanding-over-counter-medicines/questions-and-answers-fda-posts-deemed-final-order-and-proposed-order-over-counter-sunscreen`
- Glossy's Dedcool article supports the Mochi Milk sell-through claim and the
  milk/layering franchise surface.
  Source: `https://www.glossy.co/beauty/milk-remains-hot-in-fragrance-dedcool-aims-to-own-the-trend/`
- Beauty Independent's Snif article supports Snif as a live retail/subbrand
  decision context.
  Source: `https://www.beautyindependent.com/snif-talks-new-subbrand-notewrks-fragrances-toys-category-future/`

This spot-check is not a full source verification pass. The remaining candidate
claims still need direct source review before any target slot is filled.

## Working Interpretation

Adopt as the working first bet to test:

**Founder-led indie fragrance / scent-layering / fragrance-adjacent hair and
body mists with visible Sephora/Ulta/DTC traction and discrete format,
inventory, or retail-depth decisions.**

Do not adopt:

- broad fragrance as a category;
- celebrity or licensed fragrance without a visible operator;
- home-only scent;
- pure TikTok virality;
- PR-only launch narratives;
- international-only contexts without substantial US-market evidence.

## Recommended Next Step

Run a no-contact candidate scan before any outreach or capture:

1. Build a 20-brand fragrance list and a 12-brand scalp/haircare comparison
   list.
2. Verify named operators and public role visibility.
3. Map independent venue origins for each candidate context.
4. Grade costly-behavior evidence: waitlists, sellouts, reviews, restocks,
   retailer door count, purchase-depth signals, switching/dupe language, or
   repeat franchise extensions.
5. Assign decision family and action ceiling.
6. Promote only candidates with enough public evidence for a manual memo and
   no need for proprietary/internal data.

Pass signal:

- at least three strong fragrance slots survive with named operators,
  gradeable costly behavior, and at least two non-derived public origins.

Downgrade signal:

- fragrance examples collapse into one-origin PR/social hype, or only
  engagement volume appears.

Fallback:

- if fragrance downgrades, rerun the same scan discipline on scalp/haircare,
  excluding medicalized hair-growth and clinical-treatment claims.
