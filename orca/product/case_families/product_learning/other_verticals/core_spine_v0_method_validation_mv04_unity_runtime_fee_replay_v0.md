# Core Spine v0 Method Validation Replay - MV-04 Unity Runtime Fee

## Status, Scope, Source Basis, And Non-Authority

- Case ID: `MV-04`.
- Case name: Unity Runtime Fee.
- Current status: `MV04_COMPLETE_USEFUL_AVOIDED_FALSE_COMMIT_DOWNGRADE_REFRAME`.
- Scope: Phase 3 only, MV-04 only.
- Source basis: public, non-deceptive sources visible before the 2023-09-11 cutoff, plus post-window outcome sources opened only after seal.
- Search/open budget used before seal: 4 searches; 11 pre-cutoff page opens attempted; 8 readable.
- Post-window source budget used after seal: 4 outcome page opens attempted; 3 readable.
- Non-authority: this is a method-validation replay artifact, not an accepted Unity recommendation, product-market proof, implementation plan, source map, automation plan, or validation of Core Spine v0.

## Repository State Checked

- Branch/status at preflight: `main...origin/main [ahead 11]`.
- Dirty state at preflight: existing modified overlay/docs files and untracked method-validation artifacts were present before this MV-04 artifact was written.
- Target path status at preflight: `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` was clear.
- Hash preflight: wrapper, base replay prompt, and accepted frame artifact matched the owner-supplied Phase 3 hashes.

## Accepted Decision Frame

- Decision question (DecisionEvent): As of 2023-09-11, should Unity watch, probe, test, hold, narrow, phase, grandfather, message, or commit a runtime-fee or install-based monetization change for Unity developers?
- Owner context: Unity pricing, developer-platform, engine strategy, and executive commercial leadership.
- Cutoff: 2023-09-11, before the public Runtime Fee announcement on 2023-09-12.
- Fair-cutoff rationale: the cutoff sits immediately before the announcement, so public ecosystem evidence can be tested without using backlash as at-cutoff evidence.
- First-order boundary: Unity pricing, plan, terms, product, investor, platform, ad-monetization, and official strategy material visible before cutoff.
- Second-order boundary: developer community posts, indie studio commentary, engine-switching discussions, asset-store or tooling ecosystem signals, education usage signals, consultant or publisher commentary, public trust complaints, and alternative-engine comparisons visible before cutoff.
- Post-window exclusion before seal: 2023-09-12 announcement, immediate backlash, clarification posts, revised terms, executive changes, later cancellation, and post-announcement migration claims.

## Verification Gate Result

- Cutoff visibility: verified for used sources by page date, PDF date, or visible forum/post date before 2023-09-12.
- First-order visibility: verified for Unity Q4 2022 shareholder letter, Q1 2023 shareholder letter, April 2023 Unity Industry release, and Q2 2023 shareholder-letter locator.
- Second-order visibility: verified for Unity forum pricing discussion, CG Channel pricing coverage, Motley Fool ironSource reputation analysis, PocketGamer industry coverage, and search-snippet-only Reddit pricing/ironSource signals, all before cutoff.
- Excluded visibility candidates: a Q2 2023 PDF fetch failed; two Reddit bodies were fetch-blocked; search results exposing post-announcement material were excluded.
- Blocking result: no case-level source-visibility blocker. The readable pre-cutoff sources are sufficient to judge the action ceiling conservatively.

## Compact Source-Read Ledger

| ID | Source family | Role | Locator | Date basis | Open status | Use | Leakage note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MV04-S01 | First-order official investor | Pre-cutoff evidence | Unity Q2 2023 Shareholder Letter locator, https://investors.unity.com/events-presentations/presentations/presentation-details/2023/Q2-2023-Shareholder-Letter/default.aspx | 2023-08-02 page date | opened/readable locator | used for visibility only | none |
| MV04-S02 | First-order official investor | Blocked source | Q2 2023 shareholder-letter PDF | 2023-08-02 locator | attempted/cache miss | excluded | none |
| MV04-S03 | First-order official investor | Pre-cutoff evidence | Unity Q4 2022 shareholder letter PDF, https://investors.unity.com/files/doc_financials/2022/q4/4Q-2022-Shareholder-Letter_FINAL.pdf | 2023-02-22 PDF date | opened/readable | used | none |
| MV04-S04 | First-order official product/investor | Pre-cutoff evidence | Unity Industry release, https://investors.unity.com/news/news-details/2023/Unity-Releases-Unity-Industry-An-Optimized-Offering-For-Enterprises-Building-Real-Time-3D-Experiences/default.aspx | 2023-04-03 page date | opened/readable | used | none |
| MV04-S05 | First-order official investor | Pre-cutoff evidence | Unity Q1 2023 shareholder letter PDF, https://investors.unity.com/files/doc_financials/2023/q1/2023_Q1-Shareholder-Letter_FINAL.pdf | 2023-05-10 PDF date | opened/readable | used | none |
| MV04-S06 | Second-order developer community/pricing | Pre-cutoff evidence | Unity Discussions, `New Unity Pro & Enterprise Pricing`, https://discussions.unity.com/t/new-unity-pro-enterprise-pricing/894157 | 2022-09-13 thread date | opened/readable | used | related-topic post-window noise excluded |
| MV04-S07 | Second-order public pricing coverage | Pre-cutoff evidence | CG Channel, `Unity to raise subscription prices next month`, https://www.cgchannel.com/2022/09/unity-to-raise-subscription-prices/ | 2022-09-14 page date | opened/readable | used | current sidebar noise excluded |
| MV04-S08 | Second-order public trust/monetization coverage | Pre-cutoff evidence | Motley Fool, `The Most Troubling Thing About Unity's ironSource Deal`, https://www.fool.com/investing/2022/07/24/most-troubling-thing-about-unitys-ironsource-deal/ | 2022-07-24 page date | opened/readable | used | current market/sidebar noise excluded |
| MV04-S09 | Second-order developer community/trust | Blocked source | Reddit Unity3D ironSource thread | 2022-07-13 search result | attempted/cache miss | excluded; snippet-only signal retained as locator | none |
| MV04-S10 | Second-order developer pricing friction | Blocked source | Reddit gamedev Personal-seat pricing thread | 2022-06-20 search result | attempted/cache miss | excluded; snippet-only signal retained as locator | none |
| MV04-S11 | Second-order industry coverage/trust | Pre-cutoff evidence | PocketGamer.biz, `Hot Five... Unity's John Riccitiello...`, https://www.pocketgamer.biz/hot-five-18-july-2022/ | 2022-07-18 page date | opened/readable | used | none |
| MV04-S12 | Post-window official announcement/community response | Post-window comparison | Unity Discussions, `Unity plan pricing and packaging updates`, https://discussions.unity.com/t/unity-plan-pricing-and-packaging-updates/927079 | 2023-09-12 post/update dates | opened/readable after seal | post-window-only | none |
| MV04-S13 | Post-window revision coverage | Post-window comparison | Axios, `Unity apologizes, makes controversial new game development fees optional`, https://www.axios.com/2023/09/22/unity-apologizes-runtime-fees | 2023-09-22 page date | opened/readable after seal | post-window-only | none |
| MV04-S14 | Post-window official cancellation | Post-window comparison | Unity Pricing Changes, https://unity.com/products/pricing-updates | 2024-09-12 cancellation basis on page | opened/readable after seal | post-window-only | none |
| MV04-S15 | Post-window executive change | Post-window comparison | CNBC CEO retirement result, https://www.cnbc.com/2023/10/09/unity-ceo-john-riccitiello-is-retiring-from-gaming-software-company-.html | 2023-10-09 search result | attempted/fetch failed after seal | excluded; locator noted | none |

## Compact Anti-Leakage Ledger

| Check | Result | Handling |
| --- | --- | --- |
| Search-result snippets | `snippet-noise: yes` | Post-announcement and later-cancellation snippets appeared in search output; not opened or used for at-cutoff reasoning. |
| Current-page chrome | `page-chrome-noise: yes` | Current pricing, sidebars, recent-news blocks, and related-topic links were excluded unless independently dated before cutoff. |
| Post-window outcome pages before seal | none intentionally opened | No known MV-04 outcome page was opened before the seal. |
| Post-window outcome pages after seal | opened after seal | Four MV-04 outcome pages were attempted only after the at-cutoff seal marker. |
| Archived bodies | none read | No archived replay bodies or contaminated artifacts were read. |
| Prior case evidence | none used | MV-01 and MV-03 receipts were not used as MV-04 evidence. |

## First-Order Evidence Units (EvidenceUnit) And Pass Result

### MV04-FO-1 - Unity had visible profitability and monetization pressure before cutoff

Unity's official investor materials before cutoff showed an explicit push toward sustainable growth, profitability, cost control, and revenue growth ahead of market. The Q4 2022 shareholder letter tied expected 2023 Create Solutions growth partly to pricing actions taken in 2022. The Q1 2023 shareholder letter showed continued profitability targets, restructuring, and a larger platform narrative around Create, Grow, ads, AI, data, and runtime reach.

- Signal integrity: high for Unity's commercial pressure; medium for a specific runtime-fee decision because investor material does not specify an install-based fee.
- Signal use classification: first-order monetization pressure and business-model signal.
- Decision implication: supports `probe`, `test`, `narrow`, and `phase`; does not justify broad `commit`.

### MV04-FO-2 - Unity had already segmented enterprise and industry monetization

Unity's April 2023 Unity Industry release showed an official move toward differentiated enterprise packaging for non-game industries, including enterprise support, long-term support, source-code access, onboarding, training, and dedicated services. This is a visible precedent for segmentation rather than a one-size-fits-all developer charge.

- Signal integrity: high for official segmentation; medium for games pricing because Unity Industry targets non-game enterprise use cases.
- Signal use classification: first-order packaging and segmentation signal.
- Decision implication: supports `narrow`, `phase`, `message`, and enterprise-only packaging before imposing broad install-linked terms.

### MV04-FO-3 - Unity's runtime and data position created strategic temptation but not enough downside proof

Unity's Q1 2023 investor material emphasized the Unity runtime's massive distribution and the value of Unity's data advantage. That makes an install-based or runtime-linked monetization logic legible from Unity's perspective, but it also increases the need to test whether developers would view runtime reach as a trusted infrastructure dependency or as a retroactive toll surface.

- Signal integrity: medium-high for strategic temptation; low for ecosystem acceptance.
- Signal use classification: first-order platform-leverage signal.
- Decision implication: supports `probe` and bounded pricing tests, not broad `commit`.

### First-Order Pass Result

- First-order Decision Strength: `MEDIUM`.
- First-order Action Ceiling: `PROBE_TEST_NARROW_PHASE`.
- First-order recommendation bound: explore segmented pricing changes around enterprise, industry, high-revenue support, or opt-in services; do not broadly commit to install-based monetization without ecosystem trust and downside testing.

## Second-Order Evidence Units And Pass Result

### MV04-SO-1 - Prior subscription price increases were tolerated but already carried trust and value objections

The September 2022 Unity Discussions thread and CG Channel coverage show a concrete pre-cutoff pricing precedent: Pro, Enterprise, and Industrial Collection price increases, while Personal and Plus were unaffected. Some developer responses accepted normal subscription increases, but the same discussion also surfaced concerns about value received, reliability, feature prioritization, recession timing, and Unity treating game developers as secondary to ads or investor narratives.

- Signal integrity: medium-high for pricing sensitivity among Unity developers; forum comments are not representative but are directly audience-relevant.
- Signal use classification: second-order pricing and trust-fragility signal.
- Decision implication: ordinary seat price increases may be acceptable when scoped and explainable; a broader or more ambiguous runtime/install fee would require much stronger messaging, grandfathering, and opt-in boundaries.

### MV04-SO-2 - The ironSource merger created a public trust penalty around monetization motives

The Motley Fool and PocketGamer sources show that Unity's 2022 ironSource move was publicly associated with ads, monetization, layoffs, reputation risk, and developer distrust. The reputational issue was not only "ads are bad"; it was that Unity's engine stewardship could be perceived as subordinated to monetization mechanics and investor strategy.

- Signal integrity: medium for public reputation risk; medium-low for predicting a specific Runtime Fee reaction.
- Signal use classification: second-order trust and monetization-framing signal.
- Decision implication: any install-based monetization proposal should be treated as high-risk unless narrowly scoped, grandfathered, and tested against developer trust loss.

### MV04-SO-3 - Fetch-blocked Reddit candidates reinforce but do not carry the case

Search-snippet-only Reddit candidates showed pre-cutoff developer concern around Unity/ironSource and smaller-team pricing friction, but their bodies were not readable and are therefore excluded from the evidence base beyond locator-level blocked signals.

- Signal integrity effect: residual risk remains around the depth of grassroots developer sentiment and credible migration intent.
- Decision implication: do not claim mass migration was proven before cutoff; do treat visible trust sensitivity as enough to cap a broad `commit`.

### Second-Order Pass Result

- Second-order Decision Strength: `MEDIUM_HIGH_FOR_DOWNSIDE_RISK`; `MEDIUM_LOW_FOR_MIGRATION_CERTAINTY`.
- Second-order Action Ceiling: `HOLD_NARROW_PHASE_GRANDFATHER_MESSAGE`; no broad `COMMIT`.
- Movement versus first-order: `Downgrade + Reframe`.
- Downgrade basis: second-order evidence shows trust fragility, pricing-value sensitivity, and monetization-frame risk.
- Reframe basis: the decision shifts from "can Unity monetize runtime reach?" to "how can Unity monetize without violating developer trust, retroactivity expectations, and small-team economics?"

## Action-Ceiling Movement

| Pass | Decision Strength | Action Ceiling | Movement |
| --- | --- | --- | --- |
| First-order only | `MEDIUM` | `PROBE_TEST_NARROW_PHASE` | Baseline |
| With second-order | `MEDIUM_HIGH_FOR_DOWNSIDE_RISK`; `MEDIUM_LOW_FOR_MIGRATION_CERTAINTY` | `HOLD_NARROW_PHASE_GRANDFATHER_MESSAGE`; no broad `COMMIT` | `Downgrade + Reframe` |

## At-Cutoff Decision Memo

As of 2023-09-11, Unity had a real commercial reason to revisit monetization. Official sources showed profitability pressure, prior Create pricing actions, enterprise packaging, runtime reach, and a strategic claim around Unity's data/runtime position. A first-order-only read could justify probing or testing new monetization models.

The second-order evidence should cap the decision. Developers had already reacted to scoped subscription price increases with value, reliability, and trust objections. Public coverage of ironSource and executive monetization framing created a known reputational penalty around Unity prioritizing ads, monetization, and investor logic over engine stewardship. These signals do not prove that developers would migrate en masse, but they are enough to make a broad install-based or runtime-linked `commit` unsafe before the announcement.

The valid at-cutoff recommendation is:

- `hold` any broad runtime-fee or install-based change until downside testing is complete;
- `narrow` monetization to enterprise, industry, high-revenue, support, cloud, services, or opt-in value-added packaging where cost exposure is predictable;
- `phase` changes through renewals, new versions, or new contracts rather than retroactive terms;
- `grandfather` existing shipped games, existing LTS/editor versions, and small-team economics;
- `message` the change around clear value received, predictable cost exposure, and developer control;
- run private and public developer-risk tests before committing to any install-count or runtime-linked fee.

Decision Strength is high enough to avoid false `commit`. It is not high enough to prove the exact best pricing model. The clean answer is not "never monetize runtime reach"; it is that broad runtime monetization needs segmentation, grandfathering, and trust repair before launch.

Counterevidence and limiting factors:

- Unity's developer lock-in, platform breadth, and business pressure are real.
- Prior 2022 subscription increases were not universally rejected and left Personal/Plus unaffected.
- Public sources do not prove private enterprise customer acceptance or rejection.
- Pre-cutoff evidence does not prove the scale of post-announcement migration or boycott risk.

Kill criteria:

- developers cannot estimate cost exposure before shipping;
- the charge applies retroactively or appears to alter prior implicit bargains;
- install counting is opaque, externally controlled, or hard to audit;
- small teams, subscription services, charity bundles, demos, or piracy create unbounded downside;
- messaging cannot credibly separate engine stewardship from ad/monetization extraction.

Update triggers:

- official announcement of runtime or install-based pricing;
- developer, publisher, platform-holder, or middleware-provider response;
- revisions, grandfathering, or cancellation;
- leadership changes or public trust-repair moves.

Boundary note: no post-window outcome source was used in this at-cutoff memo (Memo).

## AT-CUTOFF SEAL MARKER

`MV04_AT_CUTOFF_MEMO_SEALED_BEFORE_POST_WINDOW_OPEN`

## Post-Window Outcome Comparison

After the seal, the official Unity pricing/update thread showed the broad Runtime Fee announcement: a fee based on game installs, with cloud storage, DevOps tools, and runtime AI bundled into subscription plans. The same thread recorded immediate clarifications and community response around install counting, charity bundles, demos, subscription services, gross revenue thresholds, and whether existing titles or terms were effectively affected.

The post-window path then moved in the same direction the at-cutoff memo would have required before launch. Axios reported that Unity revised the plan after backlash, with apology language, reduced retroactivity, an easier path for smaller developers, and a choice between install-linked fees and revenue share for newer versions. Unity's later pricing page states that the Runtime Fee was canceled effective September 12, 2024, after analysis and consultation with game customers, and that no new or existing games would be subject to it because it was not implemented.

Outcome calibration:

- The at-cutoff `HOLD_NARROW_PHASE_GRANDFATHER_MESSAGE` ceiling was useful and materially safer than broad `COMMIT`.
- The second-order downgrade was correct: visible trust, pricing, and monetization-framing risks translated into immediate objection points around retroactivity, counting, auditability, small-team exposure, and platform trust.
- The reframe was correct: Unity eventually moved away from runtime/install charging and back toward subscription/pricing changes, aligning more closely with predictable packaging than runtime tolling.
- The method was conservative about migration certainty; it did not need to prove mass migration to flag the broad fee as an avoidable false commit.

## Calibration Label And Method Lesson

- Calibration label: `USEFUL_AVOIDED_FALSE_COMMIT_DOWNGRADE_REFRAME`.
- Method lesson: MV-04 is a strong reverse-case method signal. First-order business pressure made monetization tempting, but second-order ecosystem evidence should have capped the action ceiling before launch. For platform pricing changes, public trust-fragility and unclear cost-exposure signals are enough to require hold/narrow/phase/grandfather/message even when private monetization pressure is real.

## Blockers, Residual Risks, And Not-Proven Boundaries

- No case-level blocker after the pre-cutoff pass.
- Fetch-blocked Reddit candidates limit confidence in grassroots depth but do not block the case.
- The CEO-change post-window source was fetch-blocked; it was not needed for the calibration verdict.
- Private revenue segmentation, enterprise account tolerance, and actual install-fee economics are not proven.
- Public pre-cutoff evidence supports downside caution; it does not prove exact later backlash scale.

## Explicit Non-Claims

- Does not claim Unity should never change pricing.
- Does not claim developer migration was proven at cutoff.
- Does not claim broad `commit` was justified.
- Does not claim private Unity revenue, customer, publisher, or platform-holder data was available.
- Does not use post-window outcome evidence to raise the at-cutoff action ceiling.

## Current Verdict

`MV04_COMPLETE_USEFUL_AVOIDED_FALSE_COMMIT_DOWNGRADE_REFRAME`

## Packet Summary

- First-order: Unity had visible profitability, pricing-action, enterprise-packaging, runtime, and data-leverage pressure before cutoff.
- Second-order movement: `Downgrade + Reframe`; broad `Commit` was unsafe.
- At-cutoff ceiling: `HOLD_NARROW_PHASE_GRANDFATHER_MESSAGE`; monetize predictably through segmentation or opt-in packaging.
- Later outcome: Runtime Fee announcement triggered immediate clarification/backlash, revision, and eventual cancellation.
- Calibration: strong avoided-false-commit signal; method was useful without needing to prove mass migration.
- Leakage: post-window outcome sources opened only after seal; snippet and current-page noise excluded.
