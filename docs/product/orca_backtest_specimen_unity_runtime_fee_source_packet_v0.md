# Orca Backtest Specimen - Unity Runtime Fee Source Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact - pre-cutoff source packet
scope: Phase 0 case frame and Phase 1 pre-cutoff public source packet for the Unity runtime/install-based monetization backtest specimen.
use_when:
  - Preparing a sealed at-cutoff Phase 2 memo for this Unity monetization case.
  - Checking which public sources were loaded before cutoff without opening outcome material.
  - Verifying anti-leakage, source-family caps, and evidence gaps for this specimen.
authority_boundary: retrieval_only
cutoff: 2023-09-11 23:59 Pacific Time
source_caps_used:
  search_queries: 6/6
  unique_public_pages_opened: 8/12
  per_source_family_pages_opened:
    unity_official_investor_filings_and_materials: 3/3
    unity_official_pricing_packaging_terms_or_policy_visibility: 2/3
    pre_cutoff_market_or_industry_context: 3/3
    pre_cutoff_developer_community_customer_signal: 0/3
stale_if: Cutoff changes, Phase 2 needs post-cutoff calibration, any outcome fact is introduced, or a later clean run loads materially better pre-cutoff Unity pricing/terms evidence.
```

## Retrieval Header

- artifact role: Product artifact - pre-cutoff source packet.
- scope: Phase 0 case frame and Phase 1 pre-cutoff public source packet only.
- use_when: Use for later sealed Phase 2 at-cutoff memo preparation, source verification, and leakage review.
- authority boundary: `retrieval_only`; this packet is evidence-routing material, not a recommendation or approval.
- cutoff: `2023-09-11 23:59 Pacific Time`.
- source caps used: 6 search queries; 8 unique public URLs opened; 3/3 Unity investor/materials URLs; 2/3 Unity pricing/terms/archive-visibility URLs; 3/3 market-context URLs; 0/3 developer/community/customer signal URLs.
- stale_if: cutoff changes; any post-cutoff or outcome evidence is added; exact pre-cutoff Unity pricing/terms pages become available in a clean run; or Phase 2 asks for outcome calibration.

## Phase 0 Case Frame

- case name: Unity potential runtime/install-based monetization change.
- decision family: pricing / packaging / monetization.
- cutoff: `2023-09-11 23:59 Pacific Time`.
- later Phase 2 decision question: Should Unity proceed with a broad runtime/install-based fee model, narrow or phase the change, grandfather existing users, change messaging, or hold pending further evidence?
- assumed decision-owner role type: executive or senior monetization/package decision owner accountable for product packaging, developer trust, revenue, customer retention, and launch risk.
- allowed source families: pre-cutoff Unity official investor filings/materials; Unity official pricing, packaging, terms, documentation, or policy pages with clear pre-cutoff visibility; pre-cutoff developer/community/customer signal pages where date and snippet do not reveal outcome; pre-cutoff market or industry context directly relevant to pricing/package/monetization risk.
- forbidden source families: retrospective explainers; Wikipedia or summary pages; post-cutoff news; post-cutoff Unity announcements; sources with snippets or titles revealing backlash, revision, cancellation, apology, resignation, leadership change, or any later outcome; any query designed to find "what happened"; prior Unity replay artifacts or prior-thread source lists; contaminated archive bodies.
- blocker conditions: `BLOCKED_BY_PRIOR_REPLAY_CONTAMINATION`, `BLOCKED_OUTPUT_DESTINATION_COLLISION`, `BLOCKED_SOURCE_VISIBILITY`, `FAILED_UNBOUNDED_SCAN`, `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL`.
- no-outcome/no-memo boundary: This packet does not write the at-cutoff decision memo, does not recommend an action, does not define an action ceiling, and does not preserve any later outcome fact.

## Source-Loading Plan

Search strategy used:

- Prefer first-order, official, pre-cutoff sources.
- Use search only to locate official filings/materials and dated visibility candidates.
- Stop at 6 search queries.
- Avoid outcome-oriented terms and avoid opening results whose visible title/snippet leaks post-window facts.
- Use direct archive lookups for pre-cutoff pricing/licensing visibility where search snippets were noisy.
- Stop early once there is enough source coverage to let Phase 2 write a sealed at-cutoff memo with explicit unknowns.

Search queries used:

1. `Unity Q2 2023 shareholder letter August 2023 investor relations`
2. `Unity Software Inc 2022 Form 10-K annual report 2023 SEC 1810806`
3. `Unity pricing plans Personal Plus Pro Enterprise August 2023 Unity`
4. `site:web.archive.org/web unity.com/products/compare-plans 202309`
5. `site:web.archive.org/web unity.com/legal/editor-terms-of-service/software 202308`
6. `Unity Editor Software Terms of Service August 2023 Unity legal`

Target source families:

- Unity official investor filings and materials.
- Unity official pricing, packaging, terms, or policy pages with clear pre-cutoff visibility.
- Pre-cutoff developer/community/customer signal pages.
- Pre-cutoff market or industry context directly relevant to pricing/package/monetization risk.

Caps:

- query count cap: 6.
- unique public URL open cap: 12.
- source-family open cap: 3 URLs per family.

Leakage avoidance rules used:

- Do not search for later outcomes.
- Do not open result pages whose title/snippet discloses post-cutoff outcome material.
- If a result snippet leaks post-window information, record only `snippet-noise: yes`.
- Do not quote or preserve leaked facts.
- Do not open prior replay artifacts or contaminated archive bodies.

Page-open counting note: counts below are unique public URLs accessed for source loading. Same-URL line views or bounded text extraction on an already opened URL are not counted as additional source pages.

## Source Ledger

| ID | URL | Source family | Source type | Publication / visibility date basis | Why opened | Status | Evidence role | Authority limit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-01 | <https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/0001810806-23-000016-index.htm> | Unity official investor filings and materials | SEC filing index for Unity 2022 Form 10-K | SEC accession page for 2022 Form 10-K filed before cutoff | Confirm filing identity and pre-cutoff visibility | readable | first-order filing locator | Index proves filing visibility, not substantive facts by itself |
| S-02 | <https://www.sec.gov/ix?doc=%2FArchives%2Fedgar%2Fdata%2F1810806%2F000181080623000016%2Funity-20221231.htm> | Unity official investor filings and materials | SEC Inline XBRL viewer | Same accession as S-01, before cutoff | Attempted SEC viewer open | blocked / not used | none | Viewer was not used for evidence extraction |
| S-03 | <https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm> | Unity official investor filings and materials | Unity 2022 Form 10-K filing body | 2022 Form 10-K filed before cutoff for fiscal year ended 2022-12-31 | Load first-order company evidence on business model, revenue pressure, customers, competition, and risk factors | readable | primary first-order evidence source | Annual filing does not prove September 2023 private plans, exact pricing terms, launch readiness, or customer elasticity |
| S-04 | <https://web.archive.org/cdx?url=unity.com/products/compare-plans&from=20230901&to=20230911&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest> | Unity official pricing, packaging, terms, or policy visibility | Internet Archive CDX lookup for Unity compare-plans URL | Query constrained to 2023-09-01 through 2023-09-11; returned no matching 200 snapshot | Try to prove pre-cutoff pricing-page visibility without opening current/post-window pages | readable / excluded | source-visibility gap | Negative result does not prove no page existed; it only failed this URL/window lookup |
| S-05 | <https://web.archive.org/cdx?url=unity.com/products/*pricing*&from=20230101&to=20230911&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest&limit=20> | Unity official pricing, packaging, terms, or policy visibility | Internet Archive CDX lookup for Unity pricing URL variants | Query constrained to 2023-01-01 through 2023-09-11; returned no matching 200 snapshot | Attempt bounded alternative Unity pricing URL discovery without broader search | readable / excluded | source-visibility gap | Negative result does not prove no Unity pricing evidence existed; exact plan/pricing evidence remains a gap |
| S-06 | <https://web.archive.org/cdx?url=unrealengine.com/en-US/license&from=20230101&to=20230911&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest&limit=5> | Pre-cutoff market or industry context | Internet Archive CDX lookup for Unreal Engine license page | Returned 200 snapshots beginning 2023-01-03, before cutoff | Establish dated visibility for competitor licensing context | readable | contextual source locator | Archive lookup only; substantive licensing facts require snapshot page |
| S-07 | <https://web.archive.org/web/20230103153058/https://www.unrealengine.com/en-US/license> | Pre-cutoff market or industry context | Archived official Unreal Engine license page | Internet Archive snapshot timestamp 2023-01-03 15:30:58 UTC, before cutoff | Load pre-cutoff public market context for alternative engine licensing/package expectations | readable | contextual evidence | Competitor context only; does not prove Unity customer behavior, Unity pricing feasibility, or legal risk |
| S-08 | <https://web.archive.org/web/20230103153058/https://www.unrealengine.com/faq> | Pre-cutoff market or industry context | Archived official Unreal FAQ page | Internet Archive snapshot timestamp 2023-01-03, before cutoff | Attempt to load linked royalty FAQ context | excluded / not evidentiary | none | Snapshot wrapper loaded, but relevant licensing text was not extractable enough for evidence use |

## Pre-Cutoff Evidence Units

### EU-01 - Unity platform has distinct create and grow monetization surfaces

- source(s): S-03.
- pre-cutoff visibility basis: Unity 2022 Form 10-K filing body available before 2023-09-11 cutoff.
- fact or signal: Unity publicly described its platform as a combined set of Create Solutions and Grow Solutions: tools for creating, running, and monetizing interactive content, alongside user acquisition, engagement, and monetization services.
- decision relevance: A runtime/install-based monetization change would sit near the boundary between creation tooling, distribution/runtime use, and monetization economics. Phase 2 can use this to frame whether a broad fee changes the implied bargain across Unity's product surfaces.
- authority level: first-order.
- limits / not proven: Does not identify any planned pricing change, expected fee structure, private rationale, or customer willingness.

### EU-02 - Unity had visible financial pressure before cutoff

- source(s): S-03.
- pre-cutoff visibility basis: Unity 2022 Form 10-K filing body available before cutoff.
- fact or signal: Unity reported 2022 revenue of about $1.39 billion, a 25% year-over-year increase, while also reporting a substantial net loss and operating expenses exceeding annual revenue.
- decision relevance: Phase 2 can treat monetization expansion pressure as public and visible before the cutoff, without inferring private urgency or endorsing any specific fee model.
- authority level: first-order.
- limits / not proven: Does not prove cash need, board pressure, target revenue, acceptable pricing mechanism, or timing.

### EU-03 - Unity revenue depended on both Create and Grow businesses

- source(s): S-03.
- pre-cutoff visibility basis: Unity 2022 Form 10-K filing body available before cutoff.
- fact or signal: Unity disclosed material revenue from both Create Solutions and Grow Solutions in 2022, with Grow tied to advertising, user acquisition, and monetization services and Create tied to subscriptions and platform services.
- decision relevance: Phase 2 can test whether a broad runtime/install-based model risks changing Create customer expectations while potentially addressing monetization capture not covered by traditional subscriptions.
- authority level: first-order.
- limits / not proven: Does not show revenue by customer cohort, game size, install count, platform, plan, or developer economics.

### EU-04 - High-value customer base was material, but distribution details were missing

- source(s): S-03.
- pre-cutoff visibility basis: Unity 2022 Form 10-K filing body available before cutoff.
- fact or signal: Unity disclosed a large number of customers contributing more than $100,000 of trailing-12-month revenue, and described these high-value customers as contributing a substantial majority of revenue.
- decision relevance: Phase 2 can consider segmentation and enterprise exposure as public evidence, while treating exact targetability and grandfathering economics as unknown.
- authority level: first-order.
- limits / not proven: Does not prove which customers would face a runtime/install fee, how contracts constrain pricing changes, or how much revenue is exposed to churn.

### EU-05 - Unity publicly disclosed renewal, retention, and customer-confidence risks

- source(s): S-03.
- pre-cutoff visibility basis: Unity 2022 Form 10-K filing body available before cutoff.
- fact or signal: Unity identified risks around customer expansion, renewal, cancellations, reductions in use, customers developing in-house alternatives, and customer confidence in Unity's monetization products.
- decision relevance: Phase 2 can use this as first-order evidence that customer trust, retention, and substitution risk were known risk categories before cutoff.
- authority level: first-order.
- limits / not proven: Does not quantify churn probability, elasticity, switching costs, or the effect of a specific pricing mechanism.

### EU-06 - Price and customer economics were public competitive factors

- source(s): S-03.
- pre-cutoff visibility basis: Unity 2022 Form 10-K filing body available before cutoff.
- fact or signal: Unity described competition from alternative platforms, in-house tools, and other providers, and listed factors including features, functionality, price, and customer economics.
- decision relevance: Phase 2 can analyze a broad fee as a pricing/package decision where the perceived economics versus alternatives matter.
- authority level: first-order.
- limits / not proven: Does not establish competitor adoption likelihood, the buyer's threshold for switching, or the acceptable communications package.

### EU-07 - A major alternative engine publicly presented a different licensing frame

- source(s): S-06, S-07.
- pre-cutoff visibility basis: Internet Archive CDX lookup and archived official Unreal Engine license page dated 2023-01-03, before cutoff.
- fact or signal: The archived Unreal license page presented Unreal as free to download and use in many cases, with custom licensing for some professional/studio needs and FAQ-based royalty applicability.
- decision relevance: Phase 2 can use this only as context that public alternatives could shape developer expectations around engine pricing and monetization mechanics.
- authority level: contextual.
- limits / not proven: Does not prove the exact operative Unreal EULA terms, does not prove Unity customers would switch, and does not establish Unity's legal or commercial constraints.

### EU-08 - Exact pre-cutoff Unity pricing/terms visibility was not established in this run

- source(s): S-04, S-05.
- pre-cutoff visibility basis: bounded Internet Archive CDX lookups constrained to pre-cutoff windows.
- fact or signal: Two bounded archive lookups for Unity pricing/compare-plan URLs did not return usable 200 snapshots.
- decision relevance: Phase 2 should not assume exact Unity plan prices, plan thresholds, legal terms, or pre-cutoff pricing copy unless a later clean source-loading unit proves them without leakage.
- authority level: second-order.
- limits / not proven: Negative archive lookup results do not prove that pre-cutoff pricing or terms pages were unavailable; they only mark this run's bounded visibility failure.

## Evidence Gaps

Phase 2 should treat the following as unknown unless separately loaded from clean, pre-cutoff sources:

- private revenue model and target economics for any runtime/install-based model.
- internal customer data, cohort economics, plan mix, and usage/install distribution.
- enterprise contract constraints, amendment rights, notice obligations, and grandfathering cost.
- developer churn, switching, substitution, and in-house engine data.
- exact elasticity and willingness to pay by customer segment.
- exact Unity pre-cutoff public pricing, package thresholds, and legal terms.
- legal/terms risk, including enforceability and measurement disputes.
- launch readiness, metering reliability, dispute handling, support readiness, and billing operations.
- buyer willingness to accept packaging changes.
- communications readiness and trust impact.
- platform-holder, publisher, and downstream customer constraints.
- pre-cutoff developer/community signal specific to install-based engine monetization.

## Phase 2 Memo-Readiness Check

Value: `ENOUGH_FOR_PHASE_2_MEMO`.

Basis: There is enough first-order pre-cutoff evidence to frame a sealed at-cutoff memo around visible financial pressure, Unity's Create/Grow business model, customer retention risks, competitive economics, and the absence of exact public pricing/terms visibility in this run. The Phase 2 memo must preserve the gaps above as unknown and must not import post-cutoff or outcome evidence.

No action ceiling or recommendation is made here.

## Anti-Leakage Ledger

- search query count: 6.
- unique public page-open count: 8.
- per-source-family page-open count:
  - Unity official investor filings and materials: 3.
  - Unity official pricing, packaging, terms, or policy visibility: 2.
  - pre-cutoff market or industry context: 3.
  - pre-cutoff developer/community/customer signal: 0.
- snippet-noise: yes.
- snippet-noise handling: noisy result snippets were not used as evidence, quoted, or preserved.
- post-cutoff/outcome pages opened: none.
- prior replay artifacts read: none.
- contaminated archive bodies read: none.
- output destination collision: none.
- broad scan status: no broad repo scan and no unbounded market scan performed.
- context compaction before artifact seal: no.

## Strict Non-Claims

- no memo written.
- no recommendation made.
- no action ceiling made.
- no outcome calibration.
- no buyer validation.
- no WTP proof.
- no repeatability proof.
- no product readiness.
- no feature readiness.
- no implementation readiness.
- no commercial readiness.
- no Core Spine validation.
