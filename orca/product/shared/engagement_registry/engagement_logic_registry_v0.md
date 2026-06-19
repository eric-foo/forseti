# Engagement Logic Registry v0

- Status: PROPOSED_FREEZE
- Artifact type: Product artifact
- Scope: Core Spine engagement interpretation skeleton
- Source basis: current owner direction, `docs/decisions/turn_08_product_thesis_v0.md`, `orca/product/README.md`
- Implementation authorized: no

## Purpose

This registry defines how Orca interprets public engagement signals without
collapsing them into a single demand score.

Core rule:

> For every engagement signal, ask what decision the signal can validly inform.

Do not ask only whether the signal is real demand. No engagement pattern is
automatically demand, and no noisy pattern is automatically worthless.

## Product Boundary

The registry is a judgment artifact, not an implementation design. It does not
authorize scrapers, bot detection systems, data pipelines, dashboards, scoring
engines, or automation.

Use it to classify and reason about evidence in decision memos (Memo), backtests (Case),
competitive intelligence, source-quality review, and satellite proof plans.

## Core Spine Relationship

This registry is a rubric for Core Spine primitives, not a separate product
surface.

| Registry concern | Core Spine primitive |
| --- | --- |
| Pattern, source, and timestamp | Evidence Unit (EvidenceUnit) |
| Incentives, copied language, bot-like activity, and manipulation risk | Signal Integrity |
| Strong for, weak for, and decision use | Signal Use Classification |
| Corroboration, discount factors, audience fit, costly behavior, and action implication | Decision Strength |
| Backtest interpretation and later outcome (Outcome) | Backtesting and Outcome Memory |

## Engagement Pattern Schema

Each engagement pattern should be captured with these fields:

| Field | Meaning |
| --- | --- |
| Pattern | What was observed. |
| Strong for | What the signal can support. |
| Weak for | What the signal should not prove by itself. |
| Possible meanings | Competing interpretations. |
| Corroboration needed | What would upgrade confidence. |
| Discount factors | What reduces weight. |
| Decision use | Recommendation verbs this signal may affect. |

## Initial Pattern Registry

| Pattern | Strong for | Weak for | Corroboration needed | Discount factors | Decision use |
| --- | --- | --- | --- | --- | --- |
| Reward-driven comments | Campaign mechanics, incentive design, competitor channel testing, audience responsiveness | Organic demand, willingness to pay | Non-incentivized repeats, downstream clicks, search lift, detailed discussion, costly behavior | Giveaway prompt, low-detail comments, same wording, low-history accounts | Monitor, test channel, discount demand claim |
| Affiliate push | Distribution strategy, creator economics, acquisition motion, competitor priorities | Unbiased advocacy, product-market pull | Non-affiliate mentions, buyer-side discussion, conversion hints, persistent independent demand | Disclosure gaps, commission incentives, copied talking points | Monitor competitor, test channel, discount advocacy |
| Like or comment spike | Attention, timing, reach, content resonance | Purchase intent, durable demand | Detailed comments, search lift, follow-on discussion, repeat exposure, costly behavior | Paid boost, creator prompt, trend timing, low audience fit | Monitor, test message, investigate |
| Burst after creator or brand prompt | Mobilization capacity, audience responsiveness, campaign mechanics | Independent market pull | Persistence after burst, independent reposts, cross-channel discussion, buyer-visible repeats | Prompt dependency, short half-life, reward framing | Monitor, test campaign, discount demand |
| Praise comments | Positioning resonance, emotional language, perceived benefit, social proof | Deep pain, willingness to pay, switching intent | Specific reasons, comparisons, repeat use, objections, costly behavior | Generic praise, parasocial dynamics, fan community, incentive context | Test message, harvest language, investigate |
| High comments with low detail | Attention, social proof, curiosity, controversy | Strong demand, precise buyer pain | Detailed objections, questions, use cases, external repeats, behavior after attention | Meme dynamics, low-effort replies, prompt farming | Monitor, investigate, discount demand |
| Copied phrase | Message propagation, meme spread, campaign coordination, narrative pollution | Independent demand | Original source mapping, varied phrasing, unrelated-source repeats, target-audience use | Syndication, templated comments, affiliate scripts, SEO copying | Monitor narrative, discount independence |
| Bot-like activity | Manipulation risk, artificial amplification, competitor tactics, evidence pollution | Customer pull, buyer belief by itself | Account history, timing clusters, cross-source comparison, downstream organic discussion | Thin accounts, identical timing, unnatural ratios, irrelevant audience | Discount signal, flag risk, investigate competitor |
| Negative complaint cluster | Objection evidence, unmet need, switching risk, product gap | Market size, WTP by itself | Repeated independent complaints, detailed stakes, workarounds, churn or switching evidence | Review bombing, competitor seeding, single incident, copied complaint | Test, reposition, fix, monitor |
| Question-heavy discussion | Curiosity, confusion, onboarding friction, latent demand | Purchase readiness by itself | Repeat questions from target audience, follow-up action, comparison behavior | Low-intent audience, novelty, unclear source context | Clarify positioning, test offer, monitor |
| Workaround sharing | Costly behavior, unmet need, workflow pull | Broad market demand by itself | Multiple independent workarounds, repeated pain, adoption of workaround, buyer fit | Hobbyist-only context, edge cases, stale examples | Test, invest, reposition |
| Competitor campaign repetition | Competitor intent, positioning test, distribution focus, narrative strategy | Customer demand by itself | Landing page changes, ad copy, creator mix, audience response, independent pickup | Coordinated paid push, low engagement quality, affiliate distortion | Competitive response, monitor, defend |

## Engagement Quality Ladder

Engagement is not a single linear score. These levels describe what an observed
signal may support. The ladder is a judgment rubric, not a core primitive and
not a scoring engine.

| Level | Name | Question |
| --- | --- | --- |
| 1 | Visibility | Did the signal exist and become visible to a relevant audience or analyst before the decision date? |
| 2 | Attention | Did people notice, click, like, comment, watch, share, or discuss it? |
| 3 | Reaction | Did people respond emotionally through praise, anger, curiosity, ridicule, skepticism, or surprise? |
| 4 | Interpretive detail | Did people explain why they care, what they compare it to, or what problem it touches? |
| 5 | Independent repetition | Does similar meaning appear across unrelated sources rather than copied phrasing? |
| 6 | Audience fit | Do the reacting sources match the buyer, user, influencer, competitor, or market observer relevant to the decision? |
| 7 | Persistence | Does the signal survive beyond a burst, launch, giveaway, paid push, or trend cycle? |
| 8 | Costly behavior | Do people spend money, switch, apply, build workarounds, complain with stakes, churn, waitlist, create content, or commit time? |
| 9 | Decision pressure | Is the signal strong enough to justify monitor, test, delay, kill, reposition, defend, or invest? |

## Signal Use Classification

Every engagement signal should be classified by decision use:

- demand evidence;
- attention evidence;
- resonance evidence;
- positioning evidence;
- objection evidence;
- competitor-strategy evidence;
- distribution evidence;
- manipulation-risk evidence;
- social-proof evidence;
- buyer-belief evidence;
- weak or noisy evidence;
- exclusion evidence.

The same signal may support several uses with different confidence levels.

## Required Splits

Orca must keep these distinctions visible:

- attention versus demand;
- repeated language versus independent demand;
- artificial amplification versus useless evidence;
- competitor intent versus buyer pull;
- buyer-visible belief versus analyst-discoverable intelligence;
- praise versus willingness to pay;
- campaign success versus product truth;
- marketing demo value versus internal product evidence.

## Backtesting Use

Backtests should use this registry to ask whether the engagement interpretation
would have helped before the outcome was known.

Internal backtests must freeze the evidence window before the outcome date and
separate pre-window evidence from post-window knowledge. Marketing demos may
use cherry-picked cases, but those cases must not train the internal evidence
standard unless they pass leakage controls.

## Open Questions

- Exact confidence vocabulary: UNKNOWN - requires owner input.
- Exact numeric or qualitative weighting method: UNKNOWN - requires owner input.
- Exact backtest case-selection policy: UNKNOWN - requires owner input.
- Exact satellite-specific engagement patterns: UNKNOWN - requires owner input.
