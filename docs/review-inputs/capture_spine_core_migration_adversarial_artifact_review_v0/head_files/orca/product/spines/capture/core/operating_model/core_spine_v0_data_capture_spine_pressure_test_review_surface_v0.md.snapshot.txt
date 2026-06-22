# Core Spine v0 Data Capture Spine Review-Surface Pressure Test

```yaml
retrieval_header_version: 1
artifact_role: Product-method pressure-test fixture
scope: Review-surface pressure test for Data Capture Spine v0 obligations using public ClickUp review pages with recency and long-context tension.
use_when:
  - Continuing Data Capture Spine setup pressure tests after the review-surface fixture.
  - Checking whether review-surface findings require an obligation-contract patch before the docs/changelog fixture.
  - Preparing categorical downstream notes for future ECR or Cleaning work without designing those layers.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
  - orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
input_hashes:
  fixture_plan: D4BC5D2983F8EC490AD3154A3C748014A71B123364D73AFF8E8C2743297C0584
  contract: ED11CD3995E47A2DC1BF277966D59E66BE798128EBECCBFE3D4574AA82FC10CB
  context_note: DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D
  blueprint: 102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B
stale_if:
  - The Data Capture obligation contract is materially patched.
  - The review-surface fixture plan is superseded or reframed.
  - Trustpilot or G2 materially change the visible ClickUp review pages used here.
  - A later review-surface pressure-test artifact supersedes this fixture.
```

- Status: PRESSURE_TEST_FIXTURE_V0
- Artifact type: Data Capture Spine setup pressure test
- Captured: 2026-05-25
- External review surfaces refreshed: 2026-05-25
- Candidate: ClickUp public review surfaces on Trustpilot and G2
- Data Capture status claimed: setup / pressure-test mode only
- Implementation authorized: no
- Runtime/source-system design authorized: no
- ECR/Cleaning design authorized: no
- Source-of-truth promotion claimed: no

Non-claims: this artifact does not claim Data Capture closure, acceptance,
formal validation, source-of-truth promotion, ECR/Cleaning readiness,
runtime/tooling readiness, or implementation readiness.

## Source-Loading Surface

Purpose: test whether the draft Data Capture obligation contract handles review
surfaces with recency, long-context text, rating/text coupling, platform
posture, and fair-slice boundaries.

Use when: deciding whether the review-surface fixture produced a material
contract patch before the docs/changelog fixture.

Do not use for: credibility, review representativeness, ClickUp evaluation,
Trustpilot or G2 evaluation, ECR field design, Cleaning transformation design,
runtime review collection, source maps, dashboards, APIs, scrapers, or
readiness claims.

Authority boundary: current user instruction, `AGENTS.md`, and the Orca overlay
control this artifact. The local Data Capture docs are setup sources, not
acceptance or source-of-truth promotion evidence.

Recheck recipe: recompute the four local hashes above, re-open the Trustpilot
and G2 pages, and mark any changed external review surface as mutable rather
than silently reusing this fixture.

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 target deepening for Data Capture setup / pressure-test packet plus retrieval-header guidance and external review pages
  edit_permission: docs-write
  target_scope: review-surface pressure-test fixture artifact only
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README; source-loading; repo map; fixture plan; obligation contract; context note; architecture blueprint
```

Dirty state note: `git status --short --branch` showed many pre-existing
modified and untracked files. Relevant source statuses are recorded in the
ledger. This artifact treats untracked or modified local setup docs as
repo-visible task sources, not as proof of acceptance, validation, or
source-of-truth promotion.

## Candidate Selected And Admission

Selected candidate: ClickUp public review surfaces, bounded to:

- Trustpilot ClickUp reviews page 1:
  `https://www.trustpilot.com/review/clickup.com`
- Trustpilot ClickUp reviews page 2:
  `https://www.trustpilot.com/review/clickup.com?page=2`
- G2 ClickUp product reviews:
  `https://www.g2.com/products/clickup/reviews`
- G2 ClickUp seller/review surface:
  `https://www.g2.com/sellers/clickup`

Why it admits as a review-surface fixture:

- It exposes aggregate rating distribution and individual rating plus review
  text on public review surfaces.
- It exposes recent low-rating reviews describing operational pain, support
  failure, billing/pricing pain, product bugs, or vendor-trust concerns.
- It exposes long positive review text describing buyer context, adoption
  context, workflows, implementation conditions, and high-value use.
- It exposes visible recency posture and separate visible date lines.
- It exposes review-source posture: Trustpilot unprompted labels and incentive
  prohibition, plus G2 validated reviewer, current-user, incentivized, and
  seller-invite labels.
- It exposes sorting, filtering, score-inclusion, moderation, and vendor-reply
  posture enough to test whether Capture records platform constraints without
  deciding credibility or representativeness.

This is a fixture candidate, not a representative sample of ClickUp users and
not a claim about ClickUp quality.

## Source-Read Ledger

| Source | Why read | Scope read | Supports | Status |
| --- | --- | --- | --- | --- |
| Current user instruction | Controlling task and non-goals | Full current instruction | Output path, target fixture, required sections, forbidden ECR/Cleaning/runtime moves | user-stated |
| `AGENTS.md` | Workspace authority | Full file | Orca overlay requirement and default docs-write boundary | clean |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Full file | Orca authority boundary and missing-authority rule | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack and ledger rules | Full file | Preflight, bounded reads, Data Capture setup packet, not-proven boundaries | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source precedence | Full file | Conflict order and known-source status | modified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Durable artifact header | Full file | Retrieval header shape and forbidden header claims | clean |
| `docs/workflows/artifact_retrievability_guide.md` | Body-opening shape | Full file | Source-loading surface, stale/recheck pattern, non-claims | clean |
| `docs/workflows/orca_repo_map_v0.md` | Data Capture pressure-test navigation | Full file | Pressure-test packet and contract hash check | modified |
| `docs/product/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md` | Controlling fixture target | Full file | Review-surface test requirements and patch-before-next rule | untracked; hash recorded |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Obligation contract under test | Full file | Core obligations, discharge states, forbidden Capture outputs | untracked; hash recorded |
| `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md` | Review-surface context rules | Full file | Review-surface context categories and core/satellite boundary | modified; hash recorded |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Layer boundary | Full file | Commissioned capture, source-family satellites, rejected patterns | untracked; hash recorded |
| Trustpilot ClickUp page 1 | Current public review surface | Opened live page text | Aggregate rating, distribution, recent reviews, unprompted labels, filter/sort posture, vendor negative-reply posture | external mutable; not archived |
| Trustpilot ClickUp page 2 | Current public review surface | Opened live page text | Long recent one-star review with pricing/support/operational pain and nearby long positives | external mutable; not archived |
| G2 ClickUp product reviews | Current public B2B review surface | Opened live page text | Rating distribution, filters, validation/moderation statement, reviewer role/company-size posture, review prompts, response affordance | external mutable; not archived |
| G2 ClickUp seller page | Current public B2B review surface | Opened live page text | Sort options, star-rating counts, validated/current-user/incentivized/seller-invite labels | external mutable; not archived |

## Review-Surface Capture Slice: What Was Preserved And Why

The sampled slice stayed within one product family, ClickUp, and two public
review platforms. Trustpilot carried stronger recent low-rating and
long-context contrast. G2 carried stronger visible reviewer-status and
incentive/source-label posture.

Observed review-surface categories:

- Trustpilot exposed an overall TrustScore, total review count, star
  distribution, a claimed-company surface, a visible negative-review reply
  posture, "More filters", and "Most recent" sort posture.
- Trustpilot individual reviews exposed reviewer alias, country, reviewer-count
  context, relative recency or date, star rating, title, review body, and
  unprompted-review posture.
- Trustpilot page 1 included recent one-star reviews about vendor trust,
  product bugs/crashes, deceptive sales allegations, or UX pain, plus long
  five-star reviews about agency workflows, engineering/support/operations use,
  AI context, and multi-client operating structure.
- Trustpilot page 2 included a long one-star review about promised AI credits,
  billing charges, support delay, slowness, and bugs, plus nearby long positive
  reviews about migration, AI-powered summaries, organizational visibility, and
  workflow improvements.
- G2 exposed rating distribution, review totals, search and filter controls,
  filters by company size, role, category, industry, and region, plus
  validation/moderation language.
- G2 individual reviews exposed rating, date, reviewer role or company-size
  context where visible, prompt sections for likes/dislikes/problems solved,
  response affordances, and labels such as validated reviewer, current user,
  incentivized, seller invite, or G2 invite on behalf of seller.
- G2 also exposed score-inclusion constraints such as some guest/non-business
  or business-partner/competitor reviews not being included in G2 scores.

Preservation rationale:

- rating and text were kept together categorically because the fixture risk is
  star-rating flattening;
- recency, review date, and visible experience-date uncertainty were preserved
  because recent live regressions and older experience timing can diverge;
- long negative and long positive context were both preserved categorically
  because either side can carry buyer-context signal;
- review-source labels, moderation language, score-inclusion notes, response
  affordances, and sort/filter posture were preserved because they shape what
  the source surface visibly exposes without deciding credibility;
- the slice boundary was preserved as one product across two public review
  carriers because no single inspected carrier exposed all review-surface
  posture needed by the fixture.

This fixture did not reproduce full review bodies. It preserved source locators
and categorical observations, then tested whether the contract would require
full raw text or an explicit limitation in a real commissioned capture.

## Data Capture Obligations Tested

Tested obligations:

- Commissioning Gate.
- Boundary Compliance.
- Capture-Event Provenance.
- Capture Mode Disclosure.
- Mode-Change Rule.
- Raw Observable Preservation.
- Source Identity And Actor Context.
- Decomposed Timing.
- Cutoff Posture.
- Archive / Historical Posture.
- Source Visibility And Access Limits.
- Related Context Preservation, especially the review-surface branch.
- Capture Failure And Blocker Visibility.
- Re-Capture Semantics.
- Categorical Handoff Sufficiency.
- Forbidden Outputs From Capture.

Not materially tested:

- Bundled-Offer Structure Observables, because this review surface did not
  present a package, settlement, public-sector deal, or multi-term proposal.
- Multimodal capture sufficiency, because the text extraction carried enough
  to run this fixture. Rendered capture may still be needed in a future capture
  if exact badge labels, date labels, truncation state, screenshots, or layout
  placement become load-bearing.

## Obligations That Held

Commissioning Gate held for setup pressure testing. The current user supplied a
specific product-method decision: pressure-test whether the review-surface
obligations require patching before the docs/changelog fixture. This is enough
to start a pressure-test capture. It is not a buyer Decision Frame and does not
make the captured reviews ECR-ready.

Boundary Compliance held. The inspected material was public web review content
accessed without private credentials, deception, ordinary-person dossiers, or
intrusive collection.

Capture-Event Provenance held at product-method level. The artifact records
capture date, operator category, local source hashes, external source URLs, and
external mutability limits.

Capture Mode Disclosure held. The mode was agent-assisted public web and local
repo reading, with human-led obligation assessment in the artifact. No scraper,
API, runtime tool, automation, or source-system design was used.

Mode-Change Rule held. No material capture-mode change occurred after the
candidate was selected. Search/open behavior stayed inside the same
agent-assisted inspection mode.

Source Identity And Actor Context held. The contract was sufficient to force
separation of source carrier from source actor: Trustpilot and G2 are carriers;
reviewers are source actors with only visible aliases, countries, review counts,
roles, company-size categories, or status labels where exposed.

Related Context Preservation held. The review-surface branch in the contract
directly names rating, text, recency posture, visible experience timing,
moderation/incentive/sorting posture, and long-context positive or negative
detail. That was the right obligation surface for this candidate.

Source Visibility And Access Limits held. The contract handled visible
constraints such as public visibility, mutable review pages, platform
moderation, filters, sort posture, review-source labels, vendor-response
posture, score-inclusion notes, and extraction limits without converting those
constraints into credibility effects.

Capture Failure And Blocker Visibility held. The contract had enough discharge
states to mark unavailable-by-source, source-limited, not-attempted, and partial
items without hiding them.

Forbidden Outputs From Capture held. The fixture did not assign credibility,
discounting, representativeness, inclusion, Decision Strength, Action Ceiling,
Signal Use Classification, source-quality score, or Cleaning/ECR effects.

Categorical Handoff Sufficiency held as a contract boundary. The contract can
carry review-surface facts and limits categorically downstream without defining
ECR fields, keys, IDs, tables, schemas, storage, or Cleaning transformations.

## Partial, Blocked, Unavailable, Not Attempted, Or Source-Limited

Raw Observable Preservation: partial in this pressure-test artifact. The
contract requirement held, but this artifact did not reproduce the full raw
review text. A real commissioned capture would need to preserve full visible
review text, expanded text where available, rating, title, date labels, and
platform labels, or explicitly mark the limitation.

Decomposed Timing: partial/source-limited. Trustpilot exposed relative recency
and separate visible date lines, but the text extraction did not always expose
whether the date line was review date, experience date, or another platform
date label. G2 exposed review dates more plainly. A rendered capture would be
needed if exact label separation is load-bearing.

Cutoff Posture: partial/not applicable for this fixture. The fixture had a
capture date of 2026-05-25, but no buyer backtest or decision-window cutoff was
provided. The correct Capture posture is to mark external reviews as live-page
material captured on 2026-05-25, with decision cutoff unknown or not
applicable for this setup run.

Archive / Historical Posture: not attempted. No archive snapshot was created
or checked. The posture is visible as not_attempted for this fixture. If review
recency, deletion, edits, or prior-window visibility become load-bearing, the
next capture should use archive/history posture rather than silently relying on
live pages.

Vendor Response Posture: partial/source-limited. Trustpilot exposed a
company-level negative-review reply posture. G2 exposed response affordances.
The sampled public text did not expose a complete individual vendor-response
history across the corpus.

Verified / Unverified / Invited / Incentivized Posture: partial but adequate
for the fixture. Trustpilot exposed unprompted-review posture and platform
incentive constraints. G2 exposed validated, current-user, incentivized,
seller-invite, and G2-invite labels. The fixture did not try to prove whether
any label is true.

Sorting, Filtering, Removal, Or Moderation Constraints: partial/source-limited.
Trustpilot and G2 exposed filter/sort controls and moderation or label
language. The fixture did not enumerate every filter combination, every removed
review, or every moderation event. That is acceptable because Capture must
record visible constraints, not prove the unseen corpus.

Re-Capture Semantics: not triggered. The source pages are mutable, so the
contract appropriately requires re-capture semantics if later source state,
archive state, decision frame, cutoff posture, or mode confidence changes.

Bundled-Offer Structure Observables: not applicable.

## Slice Boundary Assessment

The slice was fair for the review-surface fixture.

It was not too thin because it included aggregate review surface, individual
rating/text examples, fresh low ratings, long positive reviews, source-status
labels, recency/date posture, sort/filter controls, moderation language,
vendor-response posture, and access limits.

It was not too broad because it stayed inside one product candidate and only
used two public review platforms to expose different review-surface constraints.
It did not attempt corpus-wide representativeness, source ranking, or evidence
weighting.

Fairness boundary: this is a target-risk slice, not a representative sample.
Capture should preserve enough contrasting review context for downstream
inspection, while refusing to decide whether the positive or negative reviews
are more credible, more representative, or more decision-useful.

## Patch Requirement Before Docs/Changelog Fixture

No material core obligation patch is required before the docs/changelog fixture.

Reason: the current obligation contract already names the key review-surface
requirements: rating and text together, recency posture, visible experience
timing, moderation/incentive/sorting posture, long-context positive and
negative detail, source visibility limits, decomposed timing, raw observable
preservation, and forbidden Capture outputs.

Carry forward as satellite guidance, not a core patch:

- For review surfaces, require a rendered or expanded-text capture when text
  extraction hides date labels, badge labels, "read more" state, response
  placement, or sort/filter state.
- Record platform-generated summaries as platform artifacts, not substitutes
  for individual review text.
- Record score-inclusion posture where visible, such as "not included in
  platform score" notices, without treating that as credibility or exclusion.

This is not a claim that the contract is accepted, validated, or hardened.

## Source-Family Satellite Guidance

Review-surface satellites should preserve:

- Aggregate surface context: overall score, total review count, visible star
  distribution, claimed/unclaimed profile posture, and current sort/filter
  state.
- Individual review context: rating, title, full visible text, reviewer-visible
  actor context, review date, experience date where labelled, relative recency,
  source label, invite/incentive/verification posture, and vendor response where
  visible.
- Platform constraint context: moderation language, removal/edit/delete posture
  where visible, score-inclusion notes, platform-generated summaries, and any
  visible explanation of how reviews are sourced, scored, filtered, or ordered.
- Slice-boundary context: why this set of reviews was enough for the
  commissioned question and which nearby review branches, platforms, pages, or
  filters were excluded.
- Long-context balance: recent low ratings about live regressions, support
  failure, quality break, pricing shock, or operational pain must not crowd out
  long five-star reviews that explain concrete fit, success conditions, buyer
  context, adoption context, or high-value use.
- Extraction-mode limits: if a text view drops labels or truncates review
  bodies, escalate to rendered capture or mark the limitation.

Satellite rules must not promote themselves into core unless they survive
comparison across at least two non-overlapping source families or the owner
accepts a specific invariant.

## Downstream ECR / Cleaning Notes, Categorical Only

ECR should receive review-surface context categorically: source carrier,
reviewer-visible actor context, rating, title/text relationship, date/recency
posture, source-label posture, platform constraint posture, capture mode,
visibility/access limits, archive posture, and explicit limitations.

Cleaning should not collapse review text into sentiment, average rating,
positive/negative bucket, or platform AI summary. It should preserve the
relationship among rating, text, title, date, review-source posture, and
platform constraints before any downstream reduction.

Cleaning should keep platform-generated summaries separate from individual
review observables. It should not infer credibility, independence,
representativeness, duplicate status, or admissibility from review labels,
incentive labels, vendor-response posture, or score-inclusion notes.

These are categorical carry-forward notes only. They do not define ECR fields,
keys, IDs, tables, schemas, storage, file formats, Cleaning transformations,
dedupe rules, clustering, dashboards, APIs, scrapers, or runtime tooling.

## Non-Claims And Not-Proven Boundaries

This fixture does not claim:

- Data Capture Spine is accepted, validated, complete, closed, hardened,
  source-of-truth promoted, implementation-ready, runtime-ready, ECR-ready, or
  Cleaning-ready.
- The selected review pages are representative of ClickUp users.
- Trustpilot, G2, ClickUp, or any reviewer is credible or not credible.
- Any review should be included, excluded, discounted, weighted, deduplicated,
  clustered, or treated as decision-useful.
- Any Decision Strength, Action Ceiling, Signal Use Classification, buyer proof,
  willingness to pay, product readiness, commercial readiness, or Core Spine
  validation result.
- Archive/history capture was performed.
- Full raw review bodies were captured into this artifact.
- Source pages will remain unchanged after 2026-05-25.
- Future ECR, Cleaning, Judgment, source maps, APIs, scrapers, storage,
  dashboards, automation, tests, or runtime systems are authorized.

## Next Routing Object

Next routing object: docs/changelog/versioned public page pressure-test thread.

Reason: no material core obligation defect appeared in the review-surface
fixture. The fixture sequence should continue, carrying only the satellite
review-surface guidance above. This does not claim Data Capture Spine closure,
acceptance, validation, source-of-truth promotion, ECR/Cleaning readiness,
runtime/tooling readiness, or implementation readiness.
