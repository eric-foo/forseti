# Orca Backtest Specimen - Unity Runtime Fee Outcome Calibration v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact - outcome calibration
scope: Post-seal outcome calibration for the Unity runtime/install-based monetization backtest specimen.
use_when:
  - Comparing the sealed at-cutoff memo and owner blind-read decision against post-cutoff outcome evidence.
  - Assessing whether the specimen memo avoided false broad-commit risk without claiming validation.
  - Identifying improvements to future Orca decision memo specimens.
authority_boundary: retrieval_only
input_artifacts:
  - path: docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md
    sha256: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  - path: docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md
    sha256: 2DB46EEF3D6ED6F54451693DC33B5B789066EB1BF26946370B702601650A3C30
cutoff: 2023-09-11 23:59 Pacific Time
calibration_window: post-cutoff outcome sources opened after sealed memo and owner blind read
stale_if: Sealed memo hash changes, source packet hash changes, owner blind-read decision is materially restated, or materially better primary outcome sources are added.
```

## Calibration Boundary

This artifact is post-seal outcome calibration. It does not modify the sealed at-cutoff memo.

The sealed memo remains the at-cutoff specimen:

- path: `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- SHA256: `2DB46EEF3D6ED6F54451693DC33B5B789066EB1BF26946370B702601650A3C30`
- seal marker: `AT_CUTOFF_MEMO_SEALED_NO_OUTCOME_SOURCES_OPENED`

The outcome sources below were opened only after Phase 2 was sealed and after the owner completed a blind read in the current thread.

No prior Unity replay artifact, replay packet, or contaminated archive body was read for this calibration.

## Sealed Memo Baseline

Sealed memo recommended action ceiling:

> Do not proceed with a broad runtime/install-based fee model at cutoff. Proceed only with a narrowed, phased, and explicitly grandfathered monetization path, paired with segment exemptions, customer testing, and revised messaging before any broad launch.

Sealed memo's core rationale:

- Unity had public financial pressure and a plausible reason to explore monetization.
- Unity's own filings made customer confidence, renewal, cancellation, reduced use, in-house alternatives, competition, price, and customer economics relevant risks.
- High-value customer concentration made segmentation plausible.
- The source packet did not prove segment-level elasticity, contract rights, metering readiness, customer acceptance, legal enforceability, or launch communication readiness.
- Broad launch had asymmetric trust and ecosystem downside.

## Owner Blind-Read Decision

Owner-stated blind decision before outcome calibration:

`OPEN_MINIMAL_RUNTIME_WEDGE_PROTECT_ECOSYSTEM_TEST_ALTERNATIVES`

Human interpretation:

- Do not ship broad.
- If pursuing runtime monetization, start extremely small and minimal.
- The first move is partly psychological: open the category carefully so expansion remains possible later.
- Apply any first wedge only to high-value / high-switching-cost segments where ability to pay is clear.
- Exempt low-revenue or vulnerable developers by default.
- Use grandfathering or transition protection to avoid changing the bargain on existing projects.
- Messaging is mandatory but cannot fix a bad mechanism.
- Explore alternate monetization and cost reduction rather than consuming ecosystem trust for short-term earnings pressure.

This blind decision is a user-stated calibration input from the current thread, not an independent source artifact.

## Outcome Source Ledger

| ID | URL | Source type | Outcome role | Authority / limit |
| --- | --- | --- | --- | --- |
| O-01 | <https://discussions.unity.com/t/unity-plan-pricing-and-packaging-updates/927079> | Unity official discussion page | Initial runtime-fee announcement and subsequent Unity updates / clarifications | Official Unity-hosted thread; includes later edits and community replies, so use only as post-cutoff outcome material |
| O-02 | <https://www.axios.com/2023/09/13/unity-runtime-fee-policy-marc-whitten> | News report | Early backlash, install-fee mechanics, and Unity clarification pressure | Secondary source; useful for immediate market reaction, not official policy text |
| O-03 | <https://www.theguardian.com/games/2023/sep/12/unity-engine-fees-backlash-response> | News report | Announcement details, developer concerns, install/reinstall/subscription-service issues | Secondary source; useful for public reaction and framing |
| O-04 | <https://www.axios.com/2023/09/22/unity-apologizes-runtime-fees> | News report | September 22 revision: apology, reduced retroactivity, optionality, higher Personal threshold | Secondary source; summarizes revised terms |
| O-05 | <https://discussions.unity.com/t/update-to-the-unity-editor-software-terms-932808/932808> | Unity official discussion page | November 2023 terms update: ability to stay on terms for named editor version and runtime fee tied to next major release | Official Unity-hosted thread; later community replies show trust concerns |
| O-06 | <https://unity.com/products/pricing-updates> | Unity official pricing / FAQ page | Runtime Fee cancellation and replacement direction through plan/threshold/subscription pricing updates | Official current page; includes later 2024/2025/2026 updates, so use for cancellation and current policy state |
| O-07 | <https://discussions.unity.com/t/a-message-to-our-community-unity-is-canceling-the-runtime-fee/1517714> | Unity official discussion page | September 12, 2024 cancellation announcement and community replies | Official Unity-hosted thread; community replies are anecdotal |

## Outcome Timeline

### 2023-09-12: Runtime Fee announced

Unity announced a Runtime Fee based on game installs, effective January 1, 2024. The public announcement framed it as a change to the business model and subscription packaging. The official Unity thread stated that the Runtime Fee would be based on installs and paired with added cloud, DevOps, and AI-at-runtime benefits.

Outcome relevance:

- Confirms the broad category risk the memo was testing.
- Confirms install/runtime metering was central, not peripheral.
- Immediately moves the case from theoretical monetization pressure to live ecosystem pricing shock.

### 2023-09-13 to 2023-09-17: Backlash and clarification

Public reporting and Unity's own thread show that developers objected to install-based mechanics, retroactivity concerns, reinstall/fraud ambiguity, subscription-service scenarios, charity bundles, demos, platform distribution, and trust in Unity's metering.

Unity issued clarifications that included: more than 90% of customers would not be affected, fees would be on new installs after January 1, 2024, reinstall and fraudulent installs would not count, charity installs would be excluded, WebGL/streaming games would not count, and subscription-service creators would not be responsible for the fee.

Outcome relevance:

- Strongly supports the sealed memo's concern that metering, trust, communications, and customer-economics risks were launch-critical.
- Supports the owner's blind emphasis that the first move should be minimal and psychologically careful, not a shock.
- Shows that low-revenue / vulnerable-segment exemptions and operational dispute rules were not optional polish; they were core to acceptability.

### 2023-09-22: Policy revised after backlash

Unity apologized and revised the Runtime Fee policy. Reporting described the revised model as no longer imposing retroactive fees on existing games in the same way; smaller Personal users were exempted under a higher revenue threshold; paid users could avoid the fee by not switching to a newer Unity version; and qualifying developers could choose between runtime fees tied to new user installations or a 2.5% revenue share.

Outcome relevance:

- Revision moved toward the sealed memo's recommendations: grandfather/transition protection, low-segment protection, narrower conditions, and optionality.
- The revision also resembles the owner's blind "minimal wedge" intuition, but only after trust had already been damaged.
- The need for apology indicates messaging alone was insufficient once the mechanism and perceived bargain were wrong.

### 2023-11-06: Terms updated to reinforce version/terms protection

Unity updated Editor Software Terms to clarify that users could stay on terms applicable to the named Unity editor version they were using and that the Runtime Fee would not apply unless a game was created with or upgraded to the next major Unity release shipping in 2024 and beyond.

Outcome relevance:

- Confirms grandfathering / transition protection became central.
- Confirms legal/terms clarity and trust repair were material after the initial launch.
- Supports the sealed memo's legal/terms and enterprise-packaging caution.

### 2024-09-12: Runtime Fee canceled

Unity canceled the Runtime Fee for games customers effective immediately. Unity's official pricing page states that the Runtime Fee was intended for games generating significant revenue based on use of Unity Runtime, but was canceled after analysis and consultation with games customers to better align with developer ecosystem needs and expectations. Unity also states the fee was never implemented and no new or existing Unity games were, or will be, subject to it.

Outcome relevance:

- Strongly supports avoiding a broad immediate runtime fee.
- Suggests the category was more toxic, operationally costly, or ecosystem-misaligned than a narrow pre-cutoff memo could prove.
- Weakens even the "minimal runtime wedge" path unless customer consultation shows a clearly acceptable variant.

## Calibration Against Sealed Memo

| Sealed memo element | Outcome calibration | Assessment |
| --- | --- | --- |
| Hold broad runtime/install launch | Broad launch generated immediate backlash, revision, and eventual cancellation. | Strongly supported |
| Narrow / phase before any broad launch | Unity revised toward narrower applicability and future-version conditions. | Supported |
| Grandfather existing users/projects | Later terms update made version/terms protection central. | Strongly supported |
| Exempt low-revenue / vulnerable segments | Revision raised Personal threshold and protected smaller developers. | Supported |
| Messaging required but insufficient | Unity apologized and clarified, but later canceled the fee. | Strongly supported |
| Need metering/support/dispute readiness | Developer reaction centered on installs, fraud, reinstall, platform/subscription scenarios, and measurement trust. | Strongly supported |
| Segment-specific monetization review | Later replacement direction leaned toward subscription/threshold/pricing updates, not a broad runtime fee. | Partly supported; runtime category itself looked weaker than expected |
| Revenue pressure justified exploration | Unity did pursue monetization and later plan price/threshold changes. | Supported, but not specific to runtime fee |

## Calibration Against Owner Blind Decision

Owner blind decision was sharper than the sealed memo on the psychology of category introduction.

Calibrated result:

- "Do not broad ship" was strongly supported.
- "Start extremely small if introducing runtime monetization at all" was directionally supported by the need to reduce shock, but outcome suggests even a runtime-fee wedge needed extreme care or may have been strategically inferior to other monetization.
- "High-switching-cost/high-value segments first" remains commercially plausible, but outcome shows developers may punish the platform through future project choice, reputation, and migration intent even if current-project switching costs are high.
- "Low-revenue exemptions" was supported by later policy revision.
- "Grandfather / transition protection" was strongly supported by later terms update.
- "Explore alternate monetization and cut costs rather than spend trust for earnings pressure" was supported by later cancellation and plan/subscription pricing updates.

Best calibrated action ceiling:

`HOLD_BROAD_RUNTIME_FEE_TEST_ONLY_IF_CUSTOMER_ACCEPTED_MINIMAL_WEDGE_EXISTS_SHIFT_TO_SUBSCRIPTION_AND_SEGMENTED_PACKAGING`

Human version:

> Do not broadly launch runtime/install fees. Runtime monetization should proceed only if customer consultation proves a tiny, opt-in or future-version-only wedge is acceptable, operationally measurable, and legally clean. Otherwise, use less trust-damaging monetization such as subscription price/threshold changes, enterprise packaging, and cost control.

## What The Backtest Got Right

The specimen correctly identified the biggest failure mode: a broad runtime/install fee was not supported by the evidence and had asymmetric downside.

Specific hits:

- It treated customer confidence, renewal, cancellation, reduced use, in-house alternatives, competition, price, and customer economics as launch constraints.
- It warned that a broad fee required proof of segment-level revenue upside, elasticity, customer acceptance, metering, legal/contract enforceability, support readiness, and communications readiness.
- It recommended grandfathering and exemptions before broad rollout.
- It separated monetization exploration from broad launch approval.
- It correctly saw that public financial pressure could justify exploration but not this mechanism at broad scale.

## What The Backtest Missed Or Underweighted

1. Runtime-fee category psychology was underweighted.

The sealed memo said narrow/phase/grandfather; the owner blind read sharpened this into "open the category carefully." Outcome evidence shows category psychology was decisive: developers reacted not only to price level, but to the fact that Unity could meter runtime/installs after projects were built.

2. The cost of implementation should have been explicit.

The memo listed metering, billing, dispute, fraud, platform readiness, and support readiness as evidence gaps, but did not compare operational cost against expected revenue. Outcome reaction shows implementation cost and dispute handling were central, not secondary.

3. Switching cost needed segmentation.

The memo treated switching/substitution risk as medium-high, but should have split current projects, future projects, enterprise accounts, and indies:

- current shipped/in-development projects: high sunk cost, but high anger if terms change;
- future projects: more movable and reputation-sensitive;
- enterprise accounts: high switching cost and high negotiation power;
- indies/small studios: lower ability to pay, high public-signal amplification.

4. Alternative monetization should have been a primary option.

The sealed options table included hold, segment, phase, grandfather, exempt, and message, but did not elevate "use other monetization models first" as a main action path. Outcome cancellation and later pricing/threshold changes suggest alternative monetization was central.

5. Developer/community signal was absent pre-cutoff.

The source packet had zero pre-cutoff developer/community/customer signal pages. The memo correctly marked acceptance as unknown, but outcome shows this missing class was decisive. Future specimens should either load clean pre-cutoff community evidence or explicitly downgrade confidence further.

## Product-Proof Implications For Orca

Useful signal:

- The specimen produced a conservative action ceiling that avoided the false broad-commit path.
- Owner blind read improved the recommendation by adding market psychology, minimal wedge, switching-cost segmentation, and alternative monetization.
- Outcome evidence confirms those refinements were material.

Limits:

- This is a backtest, not buyer validation.
- The sealed memo used a thin pre-cutoff source packet and lacked developer/community signal.
- The memo was directionally right but not yet persuasive enough as a future executive deck.
- A buyer-facing version would need sharper economics, clearer segment math, operational cost comparison, and a more human recommendation.

Method improvement:

Future Orca backtest memos should include a required section:

`Mechanism Psychology And Implementation Cost`

It should force the memo to answer:

- Is the monetization mechanism itself trust-damaging, independent of price level?
- Does the first move open a category without causing shock?
- What is the cost to meter, bill, dispute, support, and enforce?
- Who is captive today, who can avoid the platform tomorrow, and who amplifies public reaction?
- Is an alternate monetization path less damaging for near-term revenue?

## Outcome Calibration Verdict

`CALIBRATION_USEFUL_AVOIDED_FALSE_BROAD_COMMIT_RECOMMENDATION_NEEDS_SHARPER_MINIMAL_WEDGE_AND_ALTERNATIVE_MONETIZATION_FRAME`

The sealed memo was directionally useful because it would have blocked a broad runtime/install-fee launch and forced segmentation, grandfathering, exemptions, testing, and messaging before scale.

The owner blind read improved the action ceiling. The best calibrated recommendation is not merely "narrow and phase"; it is:

> Hold broad launch. Do not introduce a meaningful runtime fee unless a tiny, customer-accepted, future-version-only or opt-in wedge proves the category can exist without ecosystem shock. Prefer less trust-damaging monetization and cost actions unless that proof exists.

## Anti-Leakage Ledger

- Phase 2 sealed memo opened public web pages: none.
- Outcome calibration public pages opened after seal: 7.
- Post-cutoff outcome sources opened after seal: yes.
- Prior Unity replay artifacts read: none.
- Prior replay packet read: none.
- Contaminated archive bodies read: none.
- Source packet leakage status carried forward: `snippet-noise: yes`; no leaked pre-seal facts preserved in source packet.
- Outcome facts introduced only in this post-seal calibration artifact.

## Strict Non-Claims

This calibration does not claim:

- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- Core Spine validation;
- the sealed memo is accepted as a buyer-facing artifact;
- a deck should now be built;
- a data spine should now be built;
- customer discovery should now proceed;
- runtime-fee strategy is proven generally correct or incorrect beyond this backtest.

