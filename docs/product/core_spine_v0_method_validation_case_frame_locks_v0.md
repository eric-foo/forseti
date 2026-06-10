# Core Spine v0 Method Validation Case-Frame Locks

## 1. Status, Scope, Source Basis, And Non-Authority

- Status: `CASE_FRAME_LOCKS_ACCEPTED_WITH_VERIFICATION_NEEDS`
- Artifact type: Product-method validation case-frame lock record
- Scope: Safe pre-replay frame locks for the five locked Core Spine v0 method-validation cases
- Date context: 2026-05-21, Asia/Singapore
- Source basis: current prompt, Orca overlay, `docs/decisions/turn_08_product_thesis_v0.md`, Core Spine v0 product and proof artifacts, the method-validation rubric, the case identity lock, and the case-frame lock contract
- Shallow verification basis: public source checks were used only to verify plausible cutoff timing, broad outcome windows, and likely source-family availability
- Implementation authorized: no
- Feature planning authorized: no
- Evidence replay authorized: no
- Source maps, source systems, data spine, automation, dashboards, scoring engines, generated artifacts, staging, commits, pushes, and PRs authorized: no
- Acceptance state: Chief Architect accepted this frame-lock record in chat on 2026-05-21 after the `FF-01` source-boundary patch; evidence replay still requires a separate launch authorization.

This artifact locks case frames only. It does not collect evidence pools,
produce at-cutoff recommendations, write case studies, build source maps, or
claim that any case will pass, fail, upgrade, downgrade, or validate Orca.

Where exact cutoff visibility, source-publication timing, or second-order
source availability remains unresolved, the field is marked
`NEEDS_VERIFICATION`. That marker means the later replay must verify timing
before using the source family for at-cutoff reasoning.

## 2. Repository State Checked

`git status --short --branch`:

```text
## main...origin/main [ahead 11]
?? docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md
?? docs/product/core_spine_v0_method_validation_case_locks_v0.md
?? docs/product/core_spine_v0_method_validation_rubric_v0.md
?? docs/prompts/deep-thinking/
?? docs/prompts/hygiene-queue/
?? docs/prompts/product-planning/
```

`git log --oneline -6`:

```text
3bf5c45 docs: add first proof run packet
8cdfe8f docs: reconcile proof lock review gate
b7d3395 docs: lock SH-01 shadow case
7492093 docs: lock Shutterstock backtest case
f596149 docs: add AI-era proof case discovery refresh
c43cfc6 docs: add proof case discovery results
```

## 3. Frame-Locking Rules

- Use exactly the five locked cases: `MV-01`, `MV-03`, `MV-04`, `MV-05`, and `MV-09`.
- Lock the decision frame before evidence interpretation.
- Treat cutoff dates as replay gates, not evidence conclusions.
- Separate first-order official or near-official source families from second-order public source families.
- Exclude every post-window source from at-cutoff reasoning, even when it later looks explanatory.
- Use result labels to compare method behavior, not to produce marketing claims.
- Preserve `NEEDS_VERIFICATION` rather than pretending a source was visible before cutoff.

## 4. Portfolio-Level Balance Check

The five-case set preserves the intended method-validation balance.

| Case | Portfolio role | Primary action-ceiling tension |
| --- | --- | --- |
| `MV-01` | SH-01-like competitor narrative pressure | Whether cleaned second-order buyer, admin, operator, or implementation-friction evidence raises, reframes, or caps the response ceiling. |
| `MV-03` | AI disruption and developer workflow | Whether developer behavior, community pressure, content-quality concerns, traffic pressure, or data-value signals justify a sharper response than official policy/product claims alone. |
| `MV-04` | Reverse pricing and ecosystem trust | Whether pre-announcement ecosystem evidence should have capped a broad pricing `Commit`. |
| `MV-05` | Business-model, platform, and data monetization | Whether API/data pricing should have been narrowed, phased, or held because of ecosystem dependence and governance backlash. |
| `MV-09` | Positive-action legal AI | Whether public legal-tech and practitioner/workflow evidence could justify stronger action such as acquire, partner, build, or bounded move before the outcome was obvious. |

The set is balanced because it includes competitor pressure, AI disruption,
pricing backlash, platform/data monetization, and positive-action acquisition
judgment. It should not be simplified into five generic AI-response stories or
five caution-only cases.

## 5. `MV-01` Case Frame

- Case ID and name: `MV-01` - Intercom Fin pressure on Zendesk.
- Frame status: `LOCKED_WITH_NEEDS_VERIFICATION`.
- Validation role: SH-01-like competitor narrative pressure case.
- Decision question: As of the cutoff, should the Zendesk customer service product, positioning, or competitive-response context watch, probe, test, hold, defend, or reposition in response to Intercom Fin's buyer-visible AI-agent narrative?
- Decision owner or context: Zendesk customer service suite product, positioning, pricing, and competitive-response context.
- Cutoff date or cutoff window: Provisional cutoff window of 2024-09-30 to 2024-10-08, before Zendesk's October 2024 AI Summit or equivalent response-expansion surface; April 2024 Zendesk AI-agent material is pre-cutoff first-order evidence. Exact cutoff remains `NEEDS_VERIFICATION`.
- Fair-cutoff rationale: Intercom Fin had been publicly launched and repeatedly positioned by this point, while a major Zendesk AI-agent response surface had not yet entered the outcome window. This creates a fair decision moment after competitive pressure is visible but before later Zendesk response material can be used as evidence.
- Why later outcome was not obvious at cutoff: Intercom's vendor narrative could reflect actor strategy, category messaging, or campaign pressure rather than durable Zendesk buyer behavior; Zendesk may also have had broader AI-agent incentives unrelated to Fin.
- Allowed action verbs: watch, probe, test, hold, defend, reposition, narrow, move.
- First-order source-family boundary: Intercom/Fin launch, product, pricing, help, comparison, integration, and customer-story material; Zendesk AI, product, pricing, help, terms, comparison, and official announcement material visible before cutoff.
- Second-order source-family boundary: Buyer-visible comparison platforms, public admin/operator discussions, implementation partner or consultant commentary, support-operations practitioner posts, pricing/measurement objections, migration or evaluation statements, and public community friction visible before cutoff.
- Post-window exclusion rule: Exclude post-cutoff Zendesk AI-agent, resolution-product, platform-restructuring, acquisition, packaging, comparison, or response-positioning material; post-cutoff Intercom/Fin repositioning, pricing, or integration changes; refreshed comparison pages; and forum/review material published or materially changed after cutoff from the at-cutoff recommendation.
- Expected outcome-comparison window: 2024-10-09 through 2026-05-21 for broad response calibration; exact source timing remains `NEEDS_VERIFICATION`.
- Reliable-bet, costly-behavior, or action-threshold standard: Upgrade above `Test` requires independent buyer-visible evidence of real evaluation, switching consideration, renewal or sales-cycle pressure, support-workflow changes, budget movement, or repeated objections with stakes. Vendor claims alone cannot prove buyer pull.
- Upgrade conditions: Independent second-order sources show persistent Zendesk-versus-Fin evaluation pressure, costly workflow or budget stakes, and audience fit beyond vendor campaign material.
- Downgrade conditions: Second-order sources show weak buyer salience, low enterprise fit, campaign-shaped comparison traffic, or broad AI-agent pressure not specific enough to Fin.
- Reframe conditions: Evidence shifts the competitive response angle away from direct feature matching toward a different buyer-facing claim or response basis.
- Blocked conditions: Pre-cutoff visibility for key source families cannot be established; second-order evidence is only post-window; the frame depends on private Zendesk win/loss, churn, or sales data.
- Result labels that matter: useful, inconclusive, upgraded, downgraded, reframed, early, late, overconfident, underconfident, blocked.

## 6. `MV-03` Case Frame

- Case ID and name: `MV-03` - Stack Overflow response to ChatGPT.
- Frame status: `LOCKED_WITH_NEEDS_VERIFICATION`.
- Validation role: AI disruption and developer workflow case.
- Decision question: As of the cutoff, should Stack Overflow watch, probe, test, hold, partner, license, build, or reposition its public platform and Teams product response to ChatGPT-driven developer behavior?
- Decision owner or context: Stack Overflow product, community, data/licensing, and enterprise knowledge-product leadership.
- Cutoff date or cutoff window: 2023-07-26, immediately before the public OverflowAI announcement on 2023-07-27; source-level visibility for second-order materials remains `NEEDS_VERIFICATION`.
- Fair-cutoff rationale: ChatGPT had been public since late 2022, Stack Overflow's generative-AI posting policy and developer AI-sentiment material were visible, and the cutoff sits just before Stack Overflow's public AI product-roadmap announcement.
- Why later outcome was not obvious at cutoff: Developer AI adoption, accuracy distrust, traffic effects, content-quality concerns, community governance, and data-value pressure could support several incompatible responses: ban, license, integrate, partner, narrow to Teams, or defend community quality.
- Allowed action verbs: watch, probe, test, hold, govern, license, partner, build, reposition, move.
- First-order source-family boundary: Stack Overflow policy posts, official blog posts, Developer Survey AI material, public product pages, Stack Overflow for Teams material, community-policy announcements, and official data/licensing or AI-product statements visible before cutoff.
- Second-order source-family boundary: Developer community discussions, public traffic analyses visible before cutoff, practitioner workflow posts, third-party developer surveys, publicly available academic or preprint studies of developer AI behavior, Stack Overflow usage patterns, or knowledge-platform adoption visible before cutoff, customer or enterprise knowledge-management commentary, and public reactions to Stack Overflow's AI policy.
- Post-window exclusion rule: Exclude the OverflowAI announcement itself, later traffic retrospectives, post-announcement community reaction, later partnership/licensing announcements, and later product-roadmap details from at-cutoff reasoning.
- Expected outcome-comparison window: 2023-07-27 through 2025-12-31 for product, traffic, community, data/licensing, and enterprise response calibration.
- Reliable-bet, costly-behavior, or action-threshold standard: Upgrade requires evidence that developer behavior, enterprise knowledge workflows, or data/licensing pressure had enough persistence, audience fit, and consequence to justify more than policy enforcement or exploratory AI features. Traffic anecdotes or AI hype alone cannot justify `Move`.
- Upgrade conditions: Independent sources show persistent developer workflow substitution, material enterprise search/knowledge pressure, or data-value leverage that supports a bounded AI product, licensing, or partnership response.
- Downgrade conditions: Evidence shows usage curiosity without durable workflow shift, weak trust in AI answers, low willingness to pay, or community harm that caps response below product `Move`.
- Reframe conditions: The frame shifts from direct AI competition response toward knowledge quality, data-value capture, community governance, or workflow-positioning strategy.
- Blocked conditions: Public pre-cutoff traffic and developer-behavior evidence cannot be verified; the decision depends on private Teams customer data; second-order material is only post-announcement.
- Result labels that matter: useful, wrong, inconclusive, upgraded, downgraded, reframed, early, late, overconfident, underconfident, blocked.

## 7. `MV-04` Case Frame

- Case ID and name: `MV-04` - Unity Runtime Fee.
- Frame status: `LOCKED_WITH_NEEDS_VERIFICATION`.
- Validation role: Reverse pricing and ecosystem-trust case.
- Decision question: As of the cutoff, should Unity watch, probe, test, hold, narrow, phase, or commit a runtime-fee or install-based monetization change for Unity developers?
- Decision owner or context: Unity pricing, developer-platform, engine strategy, and executive commercial leadership.
- Cutoff date or cutoff window: 2023-09-11, before the public Runtime Fee announcement on 2023-09-12; exact source visibility remains `NEEDS_VERIFICATION`.
- Fair-cutoff rationale: The cutoff sits immediately before the fee announcement, so public developer ecosystem evidence can be tested without using the backlash as at-cutoff evidence.
- Why later outcome was not obvious at cutoff: Unity had real monetization pressure and high developer lock-in, while it was uncertain before announcement whether developer ecosystem trust was fragile enough for a pricing change to trigger significant disruption or migration.
- Allowed action verbs: watch, probe, test, hold, narrow, phase, grandfather, message, commit.
- First-order source-family boundary: Unity pricing, plan, terms, product, investor, platform, ad-monetization, and official strategy material visible before cutoff.
- Second-order source-family boundary: Developer community posts, indie studio commentary, engine-switching discussions, asset-store or tooling ecosystem signals, game-jam or education usage signals, consultant or publisher commentary, public trust complaints, and public alternative-engine comparisons visible before cutoff.
- Post-window exclusion rule: Exclude the 2023-09-12 announcement, immediate backlash, clarification posts, revised Runtime Fee terms, executive changes, later cancellation, and all post-announcement migration claims from at-cutoff reasoning.
- Expected outcome-comparison window: 2023-09-12 through 2024-09-12, covering immediate backlash, revisions, trust effects, and eventual policy reversal.
- Reliable-bet, costly-behavior, or action-threshold standard: A broad `Commit` requires evidence that ecosystem trust cost, switching risk, revenue consequence, and downside cases are bounded. Developer dependence alone is not enough if public trust and switching-cost evidence indicate fragile goodwill.
- Upgrade conditions: Pre-cutoff evidence shows developers accept similar pricing logic, switching risk is low, cost exposure is clear, and migration threats are weak or unserious.
- Downgrade conditions: Pre-cutoff second-order evidence shows high trust sensitivity, fear of retroactive terms, pricing-formula complexity, unclear or retroactive cost-exposure risk, thin margins, credible alternatives, or strong developer identity/community backlash risk.
- Reframe conditions: The correct move shifts from runtime fee to transparent revenue-share, grandfathered pricing, usage-tier packaging, enterprise-only monetization, or opt-in services.
- Blocked conditions: Developer ecosystem evidence visible before 2023-09-12 is too thin; pricing terms cannot be separated from post-announcement reaction; the replay requires private revenue or customer segmentation data.
- Result labels that matter: useful, wrong, avoided false move, downgraded, reframed, early, late, overconfident, underconfident, blocked.

## 8. `MV-05` Case Frame

- Case ID and name: `MV-05` - Reddit API and data pricing.
- Frame status: `LOCKED_WITH_NEEDS_VERIFICATION`.
- Validation role: Business-model, platform, and data-monetization case.
- Decision question: As of the cutoff, should Reddit watch, probe, test, hold, narrow, phase, exempt, or commit API/data pricing changes across AI-training, third-party app, moderator, developer, and platform-governance use cases?
- Decision owner or context: Reddit platform, API, developer-relations, data-licensing, moderator-tooling, and executive monetization leadership.
- Cutoff date or cutoff window: Provisional cutoff of 2023-05-30, before concrete third-party-app pricing fallout and shutdown waves became broadly visible; exact cutoff remains `NEEDS_VERIFICATION`.
- Fair-cutoff rationale: Reddit's intent to charge for API/data access was public in April 2023, and the potential for ecosystem disruption was visible, but the full scale of app-developer and moderator response had not yet materialized. The cutoff creates a decision moment after pricing direction was known but before consequences dominated the evidence record.
- Why later outcome was not obvious at cutoff: Reddit had legitimate data-monetization incentives, especially around AI training and commercial data use, but third-party app dependence, moderator workflow reliance, community governance, and trust costs could imply a narrower response.
- Allowed action verbs: watch, probe, test, hold, narrow, phase, exempt, segment, price, license, commit.
- First-order source-family boundary: Reddit official API, developer, policy, terms, moderator-tooling, data-access, executive, and monetization statements visible before cutoff.
- Second-order source-family boundary: Third-party app developer statements, moderator community posts, subreddit governance discussions, accessibility/tooling concerns, user backlash, developer API discussions, AI-training/data-use commentary, and public app-dependence signals visible before cutoff.
- Post-window exclusion rule: Exclude third-party app shutdown announcements, June 2023 blackout/protest activity, post-cutoff moderator escalation, later API concessions, later corporate or data-licensing developments, and later AI-data deals from at-cutoff reasoning.
- Expected outcome-comparison window: `NEEDS_VERIFICATION`; provisional window is 2023-06-01 through 2023-08-31 for immediate ecosystem response, with later corporate and data-licensing context allowed only as separate long-window calibration if the cutoff is verified before broad third-party-app fallout.
- Reliable-bet, costly-behavior, or action-threshold standard: A pricing `Commit` requires segmentation between high-value AI/data extraction and ecosystem-critical apps or moderation workflows, with credible evidence that platform trust costs and operational disruption are bounded.
- Upgrade conditions: Pre-cutoff evidence supports clear commercial data-value capture, low ecosystem dependence, viable exemptions, and limited moderator or accessibility harm.
- Downgrade conditions: Second-order evidence shows high app/moderator dependence, credible shutdown threats, accessibility or moderation damage, community governance backlash, or inability to distinguish AI-data users from ecosystem users.
- Reframe conditions: The response shifts from broad API pricing toward segmented monetization, ecosystem protection, governance design, or staged rollout.
- Blocked conditions: Pricing details cannot be verified as visible before cutoff; app-developer and moderator evidence only appears post-cutoff; the cutoff cannot be pinned before broad third-party-app or moderator fallout; the decision requires private usage, revenue, or API-cost data.
- Result labels that matter: useful, wrong, upgraded, downgraded, reframed, avoided false move, early, late, overconfident, underconfident, blocked.

## 9. `MV-09` Case Frame

- Case ID and name: `MV-09` - Thomson Reuters / Casetext legal AI response.
- Frame status: `LOCKED_WITH_NEEDS_VERIFICATION`.
- Validation role: Positive-action legal AI case.
- Decision question: As of the cutoff, should Thomson Reuters watch, probe, test, partner, license, build, acquire, or move around legal AI assistants such as Casetext CoCounsel?
- Decision owner or context: Thomson Reuters legal products, Westlaw, Practical Law, legal workflow, partnerships, and corporate development leadership.
- Cutoff date or cutoff window: 2023-06-25, before Thomson Reuters' public definitive-agreement announcement to acquire Casetext; exact source visibility remains `NEEDS_VERIFICATION`.
- Fair-cutoff rationale: CoCounsel and generative legal AI were publicly visible before the acquisition announcement, while the later acquisition and integration path were not yet public outcome evidence.
- Why later outcome was not obvious at cutoff: Legal AI had strong promise and plausible action-side pressure from incumbent content assets, practitioner workflow pain, visible AI capability, strategic timing, and legal-workflow distribution. It also carried unresolved accuracy, confidentiality, professional-duty, hallucination, workflow-fit, adoption, procurement, and integration risks. An incumbent could plausibly build, partner, acquire, wait, or limit exposure.
- Allowed action verbs: watch, probe, test, hold, partner, license, build, acquire, move.
- First-order source-family boundary: Thomson Reuters official product, investor, AI, partnership, Westlaw, Practical Law, and legal-workflow statements; Casetext/CoCounsel official launch, product, customer, and positioning material visible before cutoff.
- Second-order source-family boundary: Law-firm, legal-operations, practitioner, bar/professional responsibility, legal-tech analyst, buyer/procurement, court or legal-workflow commentary, public product reviews, and law-practice AI-risk discussions visible before cutoff.
- Post-window exclusion rule: Exclude the acquisition announcement, closing announcement, later CoCounsel integration, customer/adoption claims, post-acquisition analyst commentary, and later legal AI product updates from at-cutoff reasoning.
- Expected outcome-comparison window: 2023-06-26 through 2025-12-31 for acquisition, integration, product adoption, and incumbent legal-AI strategy calibration.
- Reliable-bet, costly-behavior, or action-threshold standard: Upgrade to decisive capability capture or bounded `Move` requires convergence across practitioner workflow pain, credible AI capability, incumbent content advantage, buyer urgency, and manageable professional-risk controls. AI hype or vendor claims alone cannot justify acquire, partner, build, license, or move.
- Upgrade conditions: Independent pre-cutoff evidence shows legal workflow urgency, credible practitioner use, defensible content/workflow fit, high strategic consequence for incumbents, and timing advantage for decisive capability capture over a wait-and-see or build-only path.
- Downgrade conditions: Evidence shows unresolved professional-risk barriers, weak practitioner trust, unclear willingness to adopt, poor integration fit, or vendor claims without costly behavior.
- Reframe conditions: The move shifts from a single outcome path toward partner, license, build, acquire, test inside existing legal-workflow products, or target narrower legal workflows.
- Blocked conditions: Pre-cutoff legal practitioner evidence is unavailable; CoCounsel timing cannot be verified; acquisition logic depends on private diligence, customer pipeline, or valuation data.
- Result labels that matter: useful, wrong, upgraded, downgraded, reframed, early, late, overconfident, underconfident, blocked.

## 10. Blockers And Verification Needs

No case is blocked at the frame-lock stage.

Verification needs before evidence replay:

- `MV-01`: Confirm exact cutoff date and which Intercom/Fin and Zendesk source families were publicly visible before that cutoff.
- `MV-03`: Confirm which traffic, developer-behavior, and community-reaction sources were public before 2023-07-27.
- `MV-04`: Confirm the pre-2023-09-12 visibility of developer trust, pricing, switching, and ecosystem-risk source families.
- `MV-05`: Confirm the cleanest cutoff around 2023-05-30 and separate pre-cutoff API-dependence evidence from June 2023 protest evidence. If the cutoff cannot be pinned before broad third-party-app or moderator fallout, mark the case blocked or reframe the cutoff before replay.
- `MV-09`: Confirm CoCounsel launch timing, pre-announcement legal-practitioner source visibility, and what Thomson Reuters official AI material was public before 2023-06-26.

If any verification step fails, the replacement must preserve the blocked
case's role: competitor narrative pressure, AI/developer workflow disruption,
reverse pricing mistake avoidance, platform/data monetization, or positive
legal-AI action.

Completing these verification steps does not itself authorize evidence replay;
replay requires a separate later owner launch authorization.

## 11. Explicit Non-Claims

This artifact does not claim:

- Orca has replayed any case;
- any at-cutoff recommendation is known;
- any case will pass, fail, upgrade, downgrade, or validate Orca;
- second-order evidence will change an action ceiling;
- the later outcome was obvious at the cutoff;
- public source families are sufficient until timing is verified;
- external buyers will pay for Orca;
- feature planning is ready;
- implementation planning is ready;
- a source map, data spine, source system, scraper, dashboard, scoring engine,
  API, automation, or software implementation should be built.

## 12. Current Verdict

Current verdict: `CASE_FRAMES_ACCEPTED_REPLAY_AUTHORIZATION_NOT_GRANTED`.

All five locked cases now have a usable decision frame, provisional or exact
cutoff logic, source-family boundaries, post-window exclusion rule,
case-specific action-threshold standard, and result semantics. Several timing
and source-visibility fields remain marked `NEEDS_VERIFICATION`; those markers
must be resolved before any source is used for at-cutoff reasoning. Evidence
replay remains unauthorized until a separate owner launch turn grants it.
