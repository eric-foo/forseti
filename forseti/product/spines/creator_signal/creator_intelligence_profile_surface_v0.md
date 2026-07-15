# Creator Intelligence Profile Surface v0

```yaml
retrieval_header_version: 1
artifact_role: product_signal_surface_contract
scope: >
  Product-facing surface contract for the one-stop creator intelligence profile:
  how Forseti operators or buyers may view observed public accounts or linked
  creator/account clusters, aggregate influence, audience triangulation,
  commercial creator fit, freshness, limitations, and source drill-back over
  the Capture-owned creator_profile_current view.
use_when:
  - Designing or reviewing the creator profile product surface.
  - Deciding what aggregate creator influence or ideal-audience fields may appear in a buyer/operator view.
  - Checking whether a proposed creator profile claim is allowed or must be withheld.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_creator_signal_spine_promotion_binding_v0.md
  - forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
stale_if:
  - The Capture creator_profile_current view contract is superseded.
  - The public-handle identity ledger, metric rollup, or ideal-audience schema home changes.
  - The audience-triangulation or commercial-projection contract changes.
  - A later accepted dashboard/product contract supersedes this surface.
```

## Status

`OWNER_ACCEPTED_PRODUCT_SURFACE_CONTRACT_V0`, amended by the owner-ratified
audience-triangulation and maximum-defensible-aggression direction on 2026-07-14.

This is the first promoted Creator Signal surface contract. It is docs/product
only. It does not create a dashboard, storage engine, live capture flow, real
creator rows, buyer proof, or runtime implementation.

## Product job

The surface gives a Forseti operator or buyer one current, source-backed profile
for an observed public account or creator/account cluster:

```text
Who is this observed account or creator/account cluster?
Where are the public accounts?
What aggregate influence is source-backed and fresh enough to show?
What does the creator say, what do captured participants reveal, and what does that make the creator commercially best suited to do?
What is missing, stale, gated, or not claimed?
Where can the operator drill back to the source rows?
```

This is a product interpretation over `creator_profile_current`, not a new source
of truth.

## Ownership split

Capture owns:

- `creator_public_handle_linkage_ledger_v0.json` and account-link evidence;
- metric observation rows for individual reels/videos/profile facts;
- metric rollup records for average views, engagement rate, cadence, velocity,
  and similar aggregate measures;
- validated audience-triangulation snapshots, source evidence, and current-view join mechanics;
- the derived `creator_profile_current` view and its join/denormalization
  mechanics.

Judgment owns:

- semantic interpretation of creator content and captured comments;
- agreement, contradiction, missingness, and engagement-salience effects;
- fused audience-triangulation and commercial creator-fit claim sets.

Creator Signal owns:

- first-screen information architecture and section ordering;
- operator/buyer decision language for creator fit and aggregate influence;
- claim-withhold rules for product presentation;
- required limitation, missingness, freshness, and source-drill-back display;
- maximum-defensible-aggression copy and the buyer-facing hire verdict;
- product-facing non-claims.

## Required surface sections

A conforming creator intelligence profile surface has these sections or their
functional equivalent:

| Section | Required contents | Source owner |
| --- | --- | --- |
| Identity and account cluster | `profile_subject_kind`, `profile_subject_id`, `identity_state` (`single_platform_observed` or the linkage-ledger `link_state` when present), `platform_account_id` when account-scoped, `creator_record_id_or_none` when linked, link/review state when present, public platform handles, linkage evidence summary | Capture identity linkage |
| Aggregate influence | Latest allowed rollups by platform/window: average views, engagement rate, median views, cadence, recent velocity when present | Capture metric rollups |
| Audience triangulation and commercial creator fit | Content-fit/intended-audience read; observed participating-audience read from captured comments; fused hire verdict, product meaning, mechanism, campaign jobs, briefing instructions, spend-protection boundary, and conditional robustness stamp; all with claim/evidence pointers | Capture/Silver evidence + Cleaning/ECR labels + Judgment claims + Creator Signal projection |
| Freshness | identity update timestamp, metric computation timestamp, audience computation timestamp, profile view computation timestamp, stale/partial/blocked state | Capture current view |
| Limitations and missingness | unavailable metrics, hidden counts, blocked access, thin evidence, stale windows, gated Tier-2-A demographics, abstentions | Source owner for each row |
| Non-claims | Explicit claim boundaries including no buyer proof, validation, readiness, contact/outreach authorization, public directory, lead-list authorization, or guaranteed performance | Creator Signal plus Capture record contract |
| Source drill-back | links/pointers to identity, metric observation, metric rollup, audience snapshot, and packet/data-lake records when available | Capture/Data Lake as applicable |

## Aggregate influence rules

Average views, engagement rate, and similar influence facts may appear only when
they come from `creator_metric_rollup` or a successor accepted rollup home.

The surface must show or make available:

- rollup window;
- platform scope;
- source observation set or drill-back pointer;
- calculation recipe/version;
- `computed_at`;
- freshness state;
- limitations and missing-data posture;
- sample support and representativeness posture;
- non-claims for any stronger interpretation the surface might otherwise imply.

The surface must withhold or downgrade an influence summary when source windows
are stale, input rows are blocked/hidden/absent, rollup recipe is missing, sample
support is thin, the rollup is admitted-pool-only without visible limitation, or
the claim would be unstamped, sourceless, or LLM-only.

## Ideal-audience rules

Use **ideal audience** as the buyer-facing label for the triangulated commercial
profile governed by
`creator_audience_triangulation_and_commercial_projection_v0.md`. Keep its
components distinct underneath: content-fit/pitched-at evidence is one input;
captured comments support an observed participating-audience read; Judgment
fuses them into commercial creator fit. Do not call captured participants a
platform-wide audience census.

The current claim axes are category knowledge, purchase/decision stage,
price/value posture, product/brand affinity, language/community norms,
objections, aspirations/identity, presentation-style resonance, and
engagement/memorability effect. They are claim lenses, not demographic labels
or a platform-wide audience census.

Tier-2-A demographic fields such as gender/age remain gated until an accepted
aggregate-audience-attribute schema home and sourced base-rate/data prerequisites
exist. Until then, show them as unavailable/gated or omit them. Never infer
actual audience demographics from this surface.

The commercial projection uses the maximum-defensible-aggression rule: state the
strongest useful sentence the evidence supports, bind it to claim IDs, and keep
the exact evidence and limitation one action away. Commercial rhetoric may be
causal and forceful without becoming a fabricated metric, guarantee, or census.

## Allowed product claims

Allowed claim shape:

- source-backed linked public accounts;
- source-backed observed single-platform public accounts labeled as account-scoped;
- source-backed aggregate influence for a named platform/window;
- current or stale posture for identity, metrics, and audience fields;
- ideal/content-fit audience profile with support band and evidence pointers;
- observed participating-audience claims labeled to their captured scope;
- evidence-backed hire verdict, product meaning, creative mechanism, campaign
  jobs, briefing instructions, and spend-protection boundary;
- aggressive commercial synthesis over stamped claims, including causal or
  outcome-oriented rhetoric allowed by the audience-projection contract;
- explicit limitations and non-claims;
- operator-facing summary that is derived from the visible fields and source
  stamps.

The surface may use a wind-calling or creator-fit summary as an operator or buyer
summary over stamped inputs. It may make the accountable brief-specific
recommendations and relative-performance judgments permitted by the Aphrodite
charter. It is not buyer proof, validation, or a performance guarantee.

## Forbidden product claims

The surface must not provide or imply:

- contact/outreach authorization;
- lead-list export;
- public person-level directory;
- legal-name or real-world identity proof;
- follower graph or individual audience-member retention;
- actual-audience demographics unless a later accepted schema and data gate
  authorize an aggregate slice;
- unstamped, sourceless, or LLM-only influence claims;
- hidden/blocked/not-applicable metrics as observed zeroes;
- candidate public-account links as final linked creator identities or
  cross-platform aggregate influence before human review promotes or rejects
  them;
- buyer proof, validation, readiness, guaranteed creator performance, or
  fabricated sales/conversion/ROI claims;
- live capture, source-access, dashboard, SQLite, or data-lake job readiness.

## First-screen guidance

A first screen should favor scanability over completeness:

1. Profile subject, identity state, and review/link state.
2. Commercial hire verdict and what the creator makes the product mean.
3. Platform accounts plus the available aggregate influence, sponsorship,
   momentum, adjacency, rate-context, and freshness panels owned elsewhere.
4. Audience mechanism, strongest campaign jobs, and briefing instructions.
5. Spend-protection boundary and robustness stamp when actually tested.
6. Material missingness cues and a clearly reachable claim-boundaries affordance.
7. Evidence drawer and source drill-back.

Detailed per-content reels/videos stay below the fold or in drill-back. They are
not copied into the identity ledger or into this surface contract as source truth.
Full limitations, non-claims, and source drill-back may be collapsed for
scanability, but material caveats must leave a visible cue on the first screen.
This guidance covers a single creator/account profile; multi-creator ranking,
shortlist, lead-list, or outreach surfaces need a separate accepted display
contract before implementation.

## Physicalization and testing sequence

The first static `creator_profile_current` export may test source-backed identity
rows, metric observations, and metric rollups against this surface before a
storage engine or dashboard exists. The durable target is a generated read model
over Silver Vault creator metric observations and derived rollups, as mapped in
`creator_profile_current_lake_native_record_mapping_v0.md`.

The correct next sequence remains:

1. Test source-backed real identity rows, metric observations, metric rollups, and
   populated audience-triangulation/commercial-projection claims against this surface.
2. Pressure-test missingness, blocked metrics, stale windows, cross-platform link
   ambiguity, and thin audience evidence.
3. Promote to SQLite, data-lake jobs, or a dashboard implementation only after
   the sibling record shapes survive those real rows and failure cases.

## Non-claims

This surface contract is not validation, readiness, buyer proof, product proof,
SQLite adoption, data-lake job authorization, dashboard implementation, live
capture authorization, source-access authorization, public directory, outreach,
contact enrichment, lead-list authorization, or a creator-performance guarantee.

## Direction Change Propagation — Audience Commercial Projection Amendment

The controlling receipt is inline in
`creator_audience_triangulation_and_commercial_projection_v0.md`. This surface
is a directly updated controlling consumer: it now renders content-fit evidence,
observed participating-audience evidence, and Judgment-owned commercial creator
fit as one maximally commercial but evidence-bound registry panel.
