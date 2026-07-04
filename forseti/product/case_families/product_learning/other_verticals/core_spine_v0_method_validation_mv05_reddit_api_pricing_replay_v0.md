# Core Spine v0 Method Validation MV-05 Reddit API Pricing Replay v0

## Status, Scope, Source Basis, And Non-Authority

- Status: `COMPLETE`
- Case: `MV-05` - Reddit API and data pricing.
- Scope: Clean Phase 4B rerun for MV-05 only.
- Source basis: bounded public source loading under the accepted case-frame lock, wrapper, and base replay prompt.
- Non-authority: This artifact is a method-validation replay artifact only. It does not authorize implementation, source maps, data spine work, dashboards, scoring systems, automations, packages, tests, commits, pushes, PRs, feature planning, or product-readiness claims.
- Contamination boundary: The archived failed MV-05 artifact was not read. Prior accepted case bodies were not read. Prior case receipt summaries were not used as MV-05 evidence.

## Repository State Checked

`git status --short --branch` was checked during this run. The workspace was on `main...origin/main [ahead 11]` with existing modified overlay/docs files and untracked accepted method-validation inputs/case artifacts. The MV-05 target path did not exist before this run.

`git log --oneline -6` was checked during this run:

```text
3bf5c45 docs: add first proof run packet
8cdfe8f docs: reconcile proof lock review gate
b7d3395 docs: lock SH-01 shadow case
7492093 docs: lock Shutterstock backtest case
f596149 docs: add AI-era proof case discovery refresh
c43cfc6 docs: add proof case discovery results
```

## Accepted Decision Frame

- Decision question: As of the cutoff, should Reddit watch, probe, test, hold, narrow, phase, exempt, or commit API/data pricing changes across AI-training, third-party app, moderator, developer, and platform-governance use cases?
- Decision owner or context: Reddit platform, API, developer-relations, data-licensing, moderator-tooling, and executive monetization leadership.
- Cutoff used: `2023-05-30`.
- Fair-cutoff rationale: Reddit's intent to charge for API/data access was publicly visible in April 2023, while concrete third-party-app pricing fallout and shutdown waves were not used before the seal.
- Allowed verbs: watch, probe, test, hold, narrow, phase, exempt, segment, price, license, commit.
- Reliable-bet threshold: A broad pricing `Commit` requires segmentation between high-value AI/data extraction and ecosystem-critical apps or moderation workflows, with credible evidence that trust costs and operational disruption are bounded.

## Compact Source-Read Ledger

| source_id | source_family | authority_role | title_or_locator | url_or_path | publication_or_snapshot_date | searched_or_opened | visibility_basis | used_status | reason | leakage_note | excerpt_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MV05-S01 | Reddit official API/data monetization | pre-cutoff evidence | RedditInc API ecosystem update | https://www.redditinc.com/blog/2023apiupdates | 2023-04-18 | opened | Page dated before 2023-05-30 | used | Shows official intent to change commercial API/data access while preserving some access categories. | none | Short title/date/claim only |
| MV05-S02 | Reddit official API/developer policy | pre-cutoff evidence | r/reddit API update | https://www.reddit.com/r/reddit/comments/12qwagm/an_update_regarding_reddits_api/ | 2023-04-18 thread, verified by linked pre-cutoff reporting | opened | Thread existed before cutoff and is linked from pre-cutoff reporting | used | Shows official terms direction, rate-limit framing, and developer/moderator assurances. | none | Short title/date/claim only |
| MV05-S03 | Reddit official data-access/moderator tooling | pre-cutoff evidence | Reddit Data API Update: Changes to Pushshift Access | https://www.reddit.com/r/Devvit/comments/135wpr9/reddit_data_api_update_changes_to_pushshift_access/ | 2023-05-01 | opened | Page dated before 2023-05-30 | used | Shows enforcement around data access and acknowledges moderator/tooling disruption risk. | none | Short title/date/claim only |
| MV05-S04 | Process / visibility cross-check | process source | Search Engine Journal Reddit paid API report | https://www.searchenginejournal.com/reddit-paid-api/485172/ | 2023-04-21 | opened | Article dated before cutoff | used | Cross-checks pre-cutoff visibility of API terms and AI/LLM access framing. | none | Short title/date/claim only |
| MV05-S05 | AI-training/data-use commentary and third-party-app concern | pre-cutoff evidence | Fortune Reddit API report | https://fortune.com/2023/04/19/reddit-charge-api-access-usage-openai-chatgpt-google-bard-ai/ | 2023-04-19 | opened | Article dated before cutoff | used | Captures public reporting on data-value rationale and third-party reader concern before pricing fallout. | none | Short title/date/claim only |
| MV05-S06 | Third-party app developer statement | pre-cutoff evidence | Apollo developer post after Reddit calls | https://www.reddit.com/r/apolloapp/comments/12ram0f/had_a_few_calls_with_reddit_today_about_the/ | 2023-04-18/2023-04-19 update, corroborated by pre-cutoff reporting | opened | Thread and update predate cutoff | used | Shows app-developer visibility into paid API direction and unresolved pricing uncertainty. | none | Short title/date/claim only |
| MV05-B01 | Blocked / unused | blocked source | NYT direct URL attempt | https://www.nytimes.com/2023/04/18/technology/reddit-ai-openai-google.html | 2023-04-18 | opened attempt | Fetch returned no usable extract in this run | blocked | Not used as evidence. | none | Locator only |
| MV05-B02 | Blocked / unused | blocked source | Additional Reddit result opens from pre-cutoff search results | search-result refs only | 2023-04/2023-05 visible titles | opened attempts | Fetch returned no usable extract in this run | blocked | Not used as evidence. | none | Locator only |
| MV05-P01 | Post-window app-pricing outcome (Outcome) | post-window comparison | TechCrunch Apollo API-pricing report | https://techcrunch.com/2023/05/31/popular-reddit-app-apollo-may-go-out-of-business-over-reddits-new-unaffordable-api-pricing/ | 2023-05-31 | opened after seal | Post-window by date | post-window-only | Used only to compare pricing exposure after the at-cutoff memo (Memo). | none | Short title/date/claim only |
| MV05-P02 | Post-window third-party-app outcome | post-window comparison | Apollo shutdown announcement | https://www.reddit.com/r/apolloapp/comments/144f6xm/apollo_will_close_down_on_june_30th_reddits/ | 2023-06-08 visible thread age | opened after seal | Post-window by event timing and thread age | post-window-only | Used only to compare app shutdown after the at-cutoff memo. | none | Short title/date/claim only |
| MV05-P03 | Post-window platform-governance outcome | post-window comparison | The Verge subreddit blackout/crash report | https://www.theverge.com/2023/6/12/23758002/reddit-crashing-api-protest-subreddit-private-going-dark | 2023-06-12 | opened after seal | Post-window by date | post-window-only | Used only to compare governance/protest fallout after the at-cutoff memo. | none | Title/date only |
| MV05-P04 | Blocked post-window long-window calibration | blocked source | Reddit/OpenAI partnership direct URL attempt | https://www.redditinc.com/blog/reddit-and-openai-build-partnership | post-window | opened after seal | Fetch returned no usable extract in this run | blocked | Not used as evidence. | none | Locator only |

## Compact Anti-Leakage Ledger

| check | result |
| --- | --- |
| Archived failed MV-05 artifact body read | `no` |
| Prior accepted case artifact bodies read | `no` |
| Launch context contained prior failed-run source evidence, URLs, notes, or outcome observations | `no` |
| Pre-cutoff search count | `4` |
| Pre-cutoff page-open count, including failed fetches and line-window opens | `12` |
| Opened post-window outcome sources before seal | `no` |
| Post-window page-open count after seal | `4` |
| Opened post-window outcome sources after seal | `yes` |
| Search snippets contained outcome noise | `snippet-noise: yes`; the leaked fact was not preserved or used |
| Outcome material used in at-cutoff memo | `no` |

## Verification Gate Result

- Cutoff verified usable: `2023-05-30` is usable for this replay because Reddit API/data pricing intent, terms direction, and ecosystem concern were visible before cutoff, while concrete third-party-app pricing fallout was not used before the seal.
- First-order source-family visibility: `verified enough for replay`.
- Second-order source-family visibility: `verified enough for bounded replay`, but exact pricing and shutdown behavior are not pre-cutoff.
- Post-window exclusions before seal: third-party app shutdown announcements, June 2023 blackout/protest activity, post-cutoff moderator escalation, later API concessions, later corporate data-licensing developments, and later AI-data deals.
- Blocked-source status: Some direct source fetches failed, but they were not needed to establish the action ceiling.

## First-Order Evidence Units (EvidenceUnit)

### FO-1 - Reddit had a legitimate data-value and monetization rationale before cutoff

Reddit had publicly framed its corpus and API access as valuable to commercial users, including large AI/model-training use cases. This supports pricing or licensing commercial data extraction and confirms that "do nothing" was not the only defensible first-order posture.

- Signal Integrity: medium. The source is official or near-official, but it is still actor strategy and monetization framing.
- Signal Use Classification: strategic monetization signal, not buyer-pull proof.
- Decision Strength effect: supports `price` or `license` for high-value commercial data users.

### FO-2 - Official terms direction already separated some use categories

Pre-cutoff official material indicated that Reddit expected API access to remain available for many uses while higher limits, broader rights, and commercial use would move toward contract, approval, or premium access. Moderator tooling and accessibility-related assurances were present before cutoff.

- Signal Integrity: medium. Official terms direction is probative, but exact prices and enforcement details were not visible before cutoff.
- Signal Use Classification: segmentation design signal.
- Decision Strength effect: supports `segment`, `narrow`, `phase`, and `exempt`.

### FO-3 - Pushshift enforcement showed ecosystem-critical data access was already operationally sensitive

The May 2023 Pushshift access change was pre-cutoff and involved moderator/research/tooling dependencies. Reddit's own framing acknowledged operational disruption risk and the need to preserve moderator-approved access paths.

- Signal Integrity: medium-high for dependency visibility; medium for scale.
- Signal Use Classification: ecosystem-risk signal.
- Decision Strength effect: caps broad `commit` unless exemptions and migration paths are proven.

### First-Order Pass Result

- First-order Decision Strength: `MODERATE_FOR_SEGMENTED_DATA_PRICING_LOW_FOR_BROAD_API_COMMIT`.
- First-order Action Ceiling: `SEGMENT_PRICE_LICENSE_WITH_PHASED_EXEMPTIONS`.
- First-order boundary: no pre-cutoff first-order source proved that broad pricing across third-party apps, moderation tooling, accessibility tooling, and AI/data extraction had bounded trust or operational cost.

## Second-Order Evidence Units

### SO-1 - Third-party app developers were visibly affected before cutoff, but concrete prices were not yet known

The Apollo developer's pre-cutoff post described Reddit's direction toward paid API access for third-party apps and emphasized that actual pricing remained the decisive unknown. This is a visible dependency signal, not yet a shutdown-outcome signal.

- Signal Integrity: medium. Direct developer statement, but pre-price and app-specific.
- Signal Use Classification: dependency and uncertainty signal.
- Decision Strength effect: supports `phase`, `exempt`, and `hold` on broad app pricing until price exposure is testable.

### SO-2 - Public reporting showed user and developer concern before cutoff

Pre-cutoff reporting captured public concern that Reddit's API changes could affect third-party readers and other app ecosystems. This was enough to reveal stakeholder sensitivity before cutoff, but not enough to quantify the full later backlash.

- Signal Integrity: medium-low. Public reporting is timely but not a measured demand or churn signal.
- Signal Use Classification: governance/trust risk signal.
- Decision Strength effect: downgrades broad `commit` and raises the need for stakeholder-specific design.

### SO-3 - Moderator/tooling dependence was visible through Pushshift and developer-tool discussions

Pushshift-related material made moderator, tooling, and data-access dependencies visible before cutoff. Even without later protest evidence, the dependency pattern was enough to warn that API pricing could damage platform governance if treated as a single undifferentiated monetization surface.

- Signal Integrity: medium. Source visibility is clear; exact operational scale remains not proven.
- Signal Use Classification: operational-risk and ecosystem-dependence signal.
- Decision Strength effect: reframes the problem from "charge for API" to "license extractive commercial use while protecting governance-critical usage."

### Second-Order Pass Result

- Second-order Decision Strength: `MODERATE_FOR_REFRAME_LOW_FOR_BROAD_COMMIT`.
- Second-order movement: `Downgrade + Reframe`.
- Second-order Action Ceiling: `SEGMENT_PRICE_LICENSE_PHASE_EXEMPT`.
- What changed: second-order evidence did not reject monetization; it narrowed the safe path away from broad API pricing and toward distinct treatment for AI/data extraction, third-party apps, moderator tooling, accessibility, and developer ecosystem use cases.

## Action-Ceiling Movement

- First-order ceiling: `SEGMENT_PRICE_LICENSE_WITH_PHASED_EXEMPTIONS`.
- Second-order ceiling: `SEGMENT_PRICE_LICENSE_PHASE_EXEMPT`.
- Movement: `Downgrade + Reframe`, not `Upgrade` and not broad `Commit`.
- Reason: official data-value evidence supports monetization, but ecosystem dependence and unresolved pricing exposure block a reliable broad commit.

## At-Cutoff Decision Memo

As of 2023-05-30, Reddit should not broadly commit API pricing across AI-training, third-party app, moderator, developer, and governance use cases as one surface.

The strongest evidence supports a segmented path: `price` or `license` high-value AI/data extraction and large commercial use; `phase` any developer pricing; `exempt` or protect moderator, accessibility, and governance-critical tools; and `hold` broad third-party-app enforcement until prices, usage tiers, migration windows, and exemption rules are publicly testable.

Signal Integrity is mixed. Reddit's first-order material is strong enough to prove strategic monetization intent and legitimate data-value pressure. It is not strong enough to prove ecosystem safety. Second-order material is strong enough to reveal dependency, sensitivity, and uncertainty, but not enough to quantify later backlash or prove a complete alternative pricing model.

Signal Use Classification is therefore: monetization signal for AI/data access; segmentation signal for official terms; dependency-risk signal for third-party apps and moderator tooling; not reliable-bet proof for broad API pricing.

Decision Strength: `MODERATE` for segmented monetization and `LOW` for broad commit.

Action Ceiling: `SEGMENT_PRICE_LICENSE_PHASE_EXEMPT`.

Recommendation using allowed verbs: `segment` API/data use cases; `price` and `license` commercial AI/data extraction; `phase` developer pricing; `exempt` moderator, accessibility, and governance-critical tooling; `hold` broad third-party-app enforcement until concrete price exposure and migration risks are tested.

Counterevidence: Reddit had legitimate incentives to monetize data access, reduce uncompensated commercial extraction, and impose clearer terms on large API users. Some app developers pre-cutoff acknowledged that reasonable paid API access could be acceptable.

Alternative explanations: Public concern could have reflected early stakeholder anxiety rather than durable platform risk. Reddit might also have had private cost, abuse, or usage data that made tighter API economics more urgent than public evidence could show.

Uncertainty: exact app economics, API cost allocation, private usage distribution, moderator-tool dependence scale, accessibility-tool exposure, and enterprise data-license willingness to pay were not publicly proven before cutoff.

Kill criteria: broad pricing should be killed or narrowed if concrete prices imply third-party-app shutdown, moderator-tool breakage, accessibility loss, large subreddit governance disruption, or inability to distinguish commercial data extraction from ecosystem-critical usage.

Update triggers: publishable price tiers, exemption lists, moderator-tool eligibility, accessibility-tool treatment, developer migration windows, commercial data-license terms, and early developer/moderator response.

Boundary note: no post-window shutdown, protest, concession, executive, or data-deal evidence was used in this memo.

## Seal Marker

`AT_CUTOFF_MEMO_SEALED_2026-05-21_PHASE_4B_MV05`

## Post-Window Outcome Comparison

Post-window outcome evidence supported the at-cutoff cap. The May 31 TechCrunch source reported concrete Apollo pricing exposure that made the earlier "reasonable paid API might work" uncertainty resolve in the dangerous direction. The June Apollo announcement then showed at least one major third-party app shutting down. The Verge outcome source showed that subreddit governance backlash became a platform-level event.

The at-cutoff recommendation would not have perfectly predicted the speed or scale of the fallout, because exact price exposure was not visible before 2023-05-30. It would, however, have avoided the false broad `commit`: it would have forced Reddit to separate commercial AI/data extraction from ecosystem-critical apps, moderator tooling, accessibility tooling, and governance dependencies before enforcement.

The later outcome does not retroactively prove that Reddit should have abandoned monetization. It strengthens the method lesson that data-value capture and ecosystem-preservation needed to be designed as different decisions.

## Calibration Label And Method Lesson

- Calibration label: `USEFUL_AVOIDED_FALSE_BROAD_COMMIT_CONSERVATIVE_ON_SPEED`.
- Method lesson: second-order ecosystem evidence was useful because it did not need to forecast the exact later protest to cap the action ceiling. The correct method move was to downgrade broad commitment and reframe toward segmentation, exemptions, phased pricing, and governance protection.
- Error boundary: the replay did not prove exact app-level economics, later protest scale, or private Reddit cost/revenue constraints before cutoff.

## Blockers / Not-Proven Boundaries

- Not proven before cutoff: exact API prices, third-party app shutdown decisions, moderator protest scale, accessibility impact scale, later data-license terms, private API costs, private revenue exposure, or private platform-governance risk.
- Blocked source note: Direct NYT and some Reddit result fetches were not usable, but visibility was sufficient through official Reddit pages and other pre-cutoff public sources.
- Source-visibility blocker status: `none blocking case completion`; remaining gaps cap confidence rather than block replay.

## Explicit Non-Claims

- This artifact does not claim Reddit should have abandoned data monetization.
- This artifact does not claim public evidence proved private willingness to pay.
- This artifact does not claim app shutdowns, protests, or later data deals were visible before cutoff.
- This artifact does not claim a broad pricing commit was validated.
- This artifact does not authorize product changes, implementation, source systems, data spine work, dashboards, scoring systems, automation, packages, tests, commits, pushes, or PRs.

## Current Verdict

Current verdict: `MV05_COMPLETE_USEFUL_AVOIDED_FALSE_BROAD_COMMIT_DOWNGRADE_REFRAME`.

## Packet Summary

- First-order: Reddit had visible pre-cutoff data/API monetization rationale and official terms direction, including category separation signals.
- Second-order movement: `Downgrade + Reframe`, not `Upgrade`.
- At-cutoff ceiling: `SEGMENT_PRICE_LICENSE_PHASE_EXEMPT`.
- Calibration: useful avoided-false-broad-commit signal; conservative on speed and scale because exact prices were not visible before cutoff.
- Leakage: post-window sources opened only after seal; snippet noise was recorded and not used.
