# Core Spine v0 Method Validation Rubric

- Status: PROPOSED_RUBRIC
- Artifact type: Product-method validation rubric
- Scope: Five-case historical method validation for competitive and category-response decisions under evidence pollution
- Date context: 2026-05-21, Asia/Singapore
- Source basis: current owner direction, `docs/product/core_spine_v0_product_contract.md`, `docs/product/core_spine_v0_information_production_foundation_v0.md`, `docs/product/core_spine_v0_proof_protocol_v0.md`, `docs/product/core_spine_v0_first_proof_run_packet_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- Evidence collection authorized by this artifact: no
- Source maps, source systems, data spine, automation, dashboards, scoring engines, and generated artifacts authorized: no

## 1. Purpose

This rubric defines the next method-validation shape for Forseti after the first
bounded Core Spine v0 proof packet.

The validation question is:

> Can Forseti repeatedly improve high-stakes competitive or category-response
> decisions before the outcome is obvious, and does cleaned second-order public
> evidence change or sharpen the correct action ceiling?

This rubric is not a new proof run. It is a validation design for selecting and
judging future historical cases (Case).

## 2. Commercial Thesis Under Test

The promising product wedge is competitive response under evidence pollution.

The buyer problem is not generic data cleaning or broad competitor monitoring.
The buyer problem is:

> A competitor or category narrative is spreading through noisy public evidence.
> The company must decide whether to watch, probe, test, hold, move, or commit,
> but the evidence is polluted by vendor claims, campaign language, benchmarks,
> review-platform bias, bots, social proof, and weak second-order signals.

Forseti's value hierarchy for this wedge is:

1. Judgment: what action can this evidence validly support?
2. Cleaning: what evidence is polluted, duplicated, incentive-shaped, bot-shaped, or misclassified?
3. Data farming: where should evidence be collected, and how much coverage is enough?

Cleaning is the trust engine. Data farming is the supply chain. The sold
outcome is decision judgment.

## 3. Five-Case Validation Design

Use five preselected historical cases (Case). Do not select cases after interpreting
the evidence.

Each case must have:

- a real company, product, category, or competitor-response decision;
- a plausible decision date or cutoff before the later outcome (Outcome) was obvious;
- public pre-cutoff evidence that can be inspected without private access;
- later post-window outcome evidence for calibration;
- enough evidence pollution to stress Core Spine rather than reward simple hindsight;
- plausible second-order public evidence beyond official company or vendor claims.

The five-case set should include:

- at least one SH-01-like competitor narrative pressure case;
- at least one AI or technology-disruption case where a company had to decide whether to respond before demand was clean;
- at least one pricing, packaging, or business-model disruption case;
- at least one positive-action case where Forseti should be tested on whether it would have justified a reliable `Test`, bounded `Move`, acquisition, partnership, or build path before the later outcome (Outcome) was obvious;
- at least one reverse case where a company made a visible move that later performed badly, and Forseti should be tested on whether it would have advised `Hold`, `Probe`, `Test`, or a narrower move;
- at least one case where second-order data is likely to matter more than first-order official claims.

Do not use five near-identical cases. The point is to test method portability,
not to overfit one category.

## 4. Case-Hunting Criteria

Strong candidate cases have most of these traits:

- high-stakes decision consequence;
- loud competitor, category, or technology narrative;
- polluted public evidence environment;
- meaningful uncertainty at cutoff;
- visible later outcome;
- enough public source availability before cutoff;
- plausible buyer, operator, partner, reviewer, community, or workflow evidence;
- realistic alternative actions at cutoff, not one obvious path;
- credible chance that Forseti could have been early, useful, cautious, wrong, overconfident, or underconfident.

Weak candidate cases have one or more of these problems:

- the correct action was obvious by the cutoff;
- the case is famous mainly because of hindsight;
- pre-cutoff public evidence is too thin or unavailable;
- the decision depends mostly on private internal data;
- the later outcome cannot be tied to the decision frame;
- the public evidence lacks second-order source families;
- the case rewards generic trend prediction rather than action-ceiling judgment.

## 5. Two-Pass Evidence Test

Each selected case should be replayed in two passes.

### Pass A - First-Order Evidence

Use only first-order sources such as:

- company pages;
- competitor pages;
- official blogs;
- pricing pages;
- product pages;
- press releases;
- public filings;
- official launch material;
- official help or terms pages;
- official benchmark or customer-story claims.

Pass A asks:

> What action ceiling would Forseti assign from official and near-official public
> evidence alone?

### Pass B - Second-Order Evidence

Add second-order public sources such as:

- end-customer complaints;
- buyer or operator community posts;
- implementation partner commentary;
- consultant or agency guidance;
- review-platform language;
- procurement-adjacent discussion;
- sales or support objection proxies;
- job postings or workflow-change signals;
- public migration guides;
- third-party comparisons;
- creator, developer, admin, or practitioner backlash;
- repeated objections across independent channels.

Pass B asks:

> Does cleaned second-order evidence change the action ceiling, sharpen the
> response angle, expose a false move, or reveal stronger convergence?

## 6. Source-Use Ladder

Classify source families by what they can usually support. Do not treat this as
a fixed scoring system.

| Source family | Typical valid use | Typical invalid use |
| --- | --- | --- |
| Vendor or company claims | Actor strategy, claimed positioning, public narrative | Independent demand, buyer pull |
| Competitor response | Actor strategy, category pressure, defensive posture | Proof that buyers are switching |
| End-customer complaints | Downstream risk, objection hypotheses | B2B buyer demand by itself |
| Operator or admin posts | Implementation friction, workflow pain, adoption blockers | Market size by itself |
| Consultants or partners | Field pattern, repeated implementation issues | Representative demand without discounting |
| Review or comparison platforms | Buyer-visible evaluation frame, social proof infrastructure | Clean truth or segment-matched buyer behavior by default |
| Buyer, procurement, or leader statements | Buyer belief, costly behavior proxy, shortlist pressure | Broad market proof from isolated examples |
| Job, workflow, or organizational signals | Capability buildout, process change, adoption pressure | Direct product demand without corroboration |

## 7. Action-Ceiling Movement

The key test is not whether more data is more interesting. The key test is
whether cleaned evidence changes the valid action.

Record one of these outcomes for each case:

- No change: second-order evidence adds color but does not change the ceiling.
- Upgrade: the ceiling moves upward, such as `Watch` to `Test` or `Test` to bounded `Move`.
- Downgrade: second-order evidence exposes that first-order claims were overstrong.
- Reframe: the ceiling stays similar, but the correct response angle changes.
- Blocked: timing, source visibility, or decision frame cannot be established.

For high-stakes and less reversible moves, Forseti should not require certainty.
It should require a reliable bet:

- evidence convergence across independent source families;
- audience fit;
- persistence over time;
- costly behavior or credible proxies;
- alternative explanations handled;
- downside of waiting compared against downside of moving;
- explicit kill criteria and update triggers.

## 8. Strong Method Signal

The five-case method validation is strong if most of these are true:

- Forseti improves the at-cutoff decision in at least three of five cases.
- Second-order evidence changes or materially sharpens the action ceiling in at least two cases.
- At least one positive-action case identifies a reliable `Test`, bounded `Move`, acquisition, partnership, or build path before the later outcome is obvious.
- At least one reverse case shows that Forseti would have advised against, delayed, narrowed, or downgraded a move that later performed badly.
- Forseti avoids at least one false `Move` caused by vendor, campaign, social-proof, or benchmark pollution.
- Forseti preserves misses, underconfidence, overconfidence, and inconclusive results as calibration input.
- The final comparison explains why the method was useful, wrong, early, late, overconfident, or underconfident.

The reverse-case criterion matters. A method that only finds promising moves is
not enough. Forseti must also show that it can block or downgrade bad moves before
they become obvious failures.

## 9. Weak Method Signal

The validation is weak if most of these are true:

- every case collapses into generic `Test`;
- second-order evidence adds color but no decision movement;
- the method only works on famous hindsight cases;
- Forseti cannot distinguish campaign pressure from buyer behavior;
- official claims dominate the conclusion after cleaning;
- reverse cases are rationalized after the fact instead of judged from pre-cutoff evidence;
- memos feel like research summaries rather than action-ceiling decisions.

## 10. Failure Or Blocked States

Fail the method validation if:

- post-window evidence leaks into the at-cutoff recommendation;
- cases are chosen because the later outcome is already persuasive;
- evidence pollution is counted as independent demand;
- second-order data is treated as inherently stronger without source-use classification;
- `Move` or `Commit` is justified without action-ceiling rationale;
- misses are removed from calibration;
- the process turns into a data-spine, dashboard, scraper, monitoring, or feature plan.

Block a case if:

- cutoff timing cannot be established;
- source visibility before cutoff cannot be established;
- the decision frame is missing;
- public evidence is not inspectable enough;
- the case requires private or intrusive evidence;
- the action ceiling cannot be judged without owner input.

## 11. Output Expected From A Future Validation Run

A future five-case validation run should produce:

- five locked case frames;
- cutoff dates and fair-cutoff rationales;
- first-order pass result for each case;
- second-order pass result for each case;
- action-ceiling movement for each case;
- post-window outcome comparison for each case;
- calibration labels: useful, wrong, early, late, overconfident, underconfident, inconclusive, or blocked;
- cross-case method conclusion;
- explicit non-claims about external willingness to pay, feature readiness, implementation readiness, source systems, and data-spine buildout.

## 12. Current Verdict

Current verdict: `READY_FOR_CASE_HUNTING_PROMPT`.

This rubric is sufficient to guide a case-hunting prompt. It does not authorize
the case-hunting run, source collection, evidence interpretation, feature
planning, implementation planning, or runtime work.
