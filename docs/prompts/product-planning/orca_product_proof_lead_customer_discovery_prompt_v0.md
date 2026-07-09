# Orca Product Proof Lead Customer Discovery Prompt v0

> **RETIRED / OFF-TARGET (2026-06-12)**
> This operating prompt remains hard-gated to the superseded pricing wedge
> (pricing-first propagation AR-01 flagged it; the consumer-demand
> ratification of 2026-06-12 made it doubly stale). Do not use it to drive
> discovery preparation. The live qualification instruments are
> `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`
> and the buyer-proof packet's Demand-Substrate Hard Gate. A consumer-demand
> discovery operating prompt is deliberately deferred — authored just-in-time
> when a discovery prep run is actually commissioned (owner-routed); none
> exists yet. Retained as history. (Closes the live-misroute half of
> ORCA-HYGIENE-018.)

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact (retired 2026-06-12 — historical)
scope: Operating prompt for bounded Orca Product Proof Lead customer-discovery preparation.
use_when:
  - Preparing Product Proof Lead customer discovery for Orca buyer proof.
  - Qualifying target buyers before first memo or executive-deck production.
  - Grading discovery, decision-artifact readback, and pull results without claiming validation.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/product-proof.md
  - forseti/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md
  - forseti/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
  - forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
input_hashes:
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: B570672CD7F31B2D78F9DC5E851C3AEDA7030A56ECF2CDC6733E0191ED3DDC23
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: 731E4349AA931613D393DFC64B05F410E098D40F86D1C26A11BD31A1E2852322
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: ECDCD4BFC626295D486189F063CA8429EA2F324BD71151C9D28A52683927A224
branch_or_commit: main @ a873c9c3ed3b289a65f9c472c63e0aadf880a127
downstream_consumers:
  - Orca Product Proof Lead customer-discovery prep runs.
stale_if:
  - Any accepted product-proof or ICP artifact hash changes.
  - `.agents/workflow-overlay/product-proof.md` changes trust-objection semantics.
  - Owner changes target buyer segment, decision family, proof shape, or non-claim boundary.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `product`.

Output mode for this prompt artifact: `file-write`.

Downstream operating mode: customer-discovery preparation only. This prompt does not authorize customer outreach, public web research, buyer contact, memo production, executive deck production, product-bet planning, feature planning, implementation planning, software, automation, dashboards, source systems, source maps, data-spine designs, CRM workflows, commits, pushes, PRs, buyer-validation claims, willingness-to-pay claims, product-readiness claims, feature-readiness claims, implementation-readiness claims, commercial-readiness claims, or Core Spine v0 validation claims.

## Pricing-First Refinement (2026-06-08)

This prompt's first-proof framing is REFINED by the owner-locked pricing-first
direction. Controlling wedge authority:
`docs/decisions/orca_icp_wedge_pricing_first_v0.md` (the accepted-source hashes
embedded below are superseded by it — reread-required; the embedded
hash-mismatch / `BLOCKED_ROLE_DRIFT` stop does NOT fire for this intentional
refinement). Deltas:

- Engine/spine = outside-in COMPETITIVE & market intelligence; pricing is its
  first application.
- First-proof BEACHHEAD re-scoped: from "developer-facing SaaS" (a stale,
  convenience-derived inheritance) to the AI-MONETIZATION SLICE — B2B SaaS making
  a first-time AI-monetization or competitor-triggered repricing/repackaging
  decision, where the competitor-pricing substrate is publicly rich and the firm
  is flying blind. Dev-facing SaaS is a strong sub-instance, not the defining
  qualifier; the wedge frame is cross-sector-open. Decision family
  (pricing/packaging/API/billing/usage/add-on/monetization) is UNCHANGED.
- Beachhead RATIONALE (test instrument, not arbitrary filter): the
  first-time/flying-blind qualifiers exist because that is where public signal can
  plausibly DECIDE the repricing move rather than merely CONFIRM it — no internal
  AI-pricing history. Caveat the proof must test: in a first-time wave the
  competitor-price substrate is itself new/sparse, so "publicly rich" is not yet
  "clean/decision-grade."
- Servability HARD GATE: the differentiated read must sit on a CLEAN,
  decision-grade public substrate — competitor PRICE/packaging signal (pricing
  pages, changelogs, filings, earnings), NOT user reviews (biased / FTC-polluted /
  interview-gated). Read the rubric's "public-signal surface" requirement as that
  clean substrate; reviews are confirmatory-only.

```yaml
direction_change_propagation:
  doctrine_changed: First-proof framing refined to pricing-first / AI-monetization beachhead / competitive-intelligence engine / clean-substrate hard gate.
  trigger: product_doctrine
  controlling_sources_updated:
    - this artifact
  controlling_decision: docs/decisions/orca_icp_wedge_pricing_first_v0.md
  non_claims:
    - not validation
    - not willingness-to-pay
    - not readiness
    - not ICP proven
```

The paste-ready operating prompt below is SURGICALLY ALIGNED to this refinement
(company-type rubric + servability gate); the discovery script, intake form, pull
rubric, stop/continue rules, non-claims, and no-outreach/docs-first boundaries are
unchanged.

## Paste-Ready Operating Prompt

```markdown
# Orca Product Proof Lead Customer Discovery Prep

You are running Orca Product Proof Lead customer-discovery preparation.

Use `workflow-deep-thinking`.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

## Authority And Source Boundary

Source hierarchy:
1. Explicit user instruction for the current turn.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow guidance only for generic mechanics, never Orca project facts.

Required first read:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/product-proof.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/decisions/orca_icp_wedge_pricing_first_v0.md` (CURRENT ICP wedge authority — pricing-first / AI-monetization beachhead / competitive-intelligence engine)
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` (SUPERSEDED — reread-required; current authority is `docs/decisions/orca_icp_wedge_pricing_first_v0.md`)
- `docs/product/orca_product_proof_lead_charter_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`

Accepted product-proof and ICP source hashes:
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`: `B570672CD7F31B2D78F9DC5E851C3AEDA7030A56ECF2CDC6733E0191ED3DDC23`
- `docs/product/orca_product_proof_lead_charter_v0.md`: `731E4349AA931613D393DFC64B05F410E098D40F86D1C26A11BD31A1E2852322`
- `docs/product/orca_buyer_proof_packet_v0.md`: `ECDCD4BFC626295D486189F063CA8429EA2F324BD71151C9D28A52683927A224`

If any accepted source hash mismatches, stop as `BLOCKED_ROLE_DRIFT` and report the mismatch. Do not substitute another product-proof boundary.

## Worktree Preflight

Expected workspace: `C:\Users\vmon7\Desktop\projects\orca`.

Expected branch at prompt creation: `main`.

Expected commit at prompt creation: `a873c9c3ed3b289a65f9c472c63e0aadf880a127`.

Dirty state: allowed. Existing modified and untracked docs may be present. Do not read archived contaminated replay outputs. Do not treat unrelated dirty files as authority.

Target scope: customer-discovery preparation for the accepted Orca buyer proof boundary only.

Edit permission: `docs-write` only if the current user explicitly asks to write a discovery-prep artifact or batch note under an accepted docs folder. Otherwise use `chat-only`.

Default output mode: `chat-only`.

## Hard Boundaries

Do not contact buyers.
Do not perform outreach.
Do not run public web research in this customer-discovery preparation or operating prompt. Any later memo or executive-deck production research requires a separate explicitly authorized production prompt.
Do not create software, automation, packages, tests, dashboards, source maps, data-spine designs, source systems, CRM workflows, commits, pushes, or PRs.
Do not perform product-bet planning, feature planning, implementation planning, or commercial-readiness planning.
Do not claim buyer validation, willingness to pay, repeatability, product readiness, feature readiness, implementation readiness, commercial readiness, or Core Spine v0 validation.

Return `BLOCKED_BY_AUTHORIZATION` if the requested work would require outreach, implementation, automation, source systems, dashboards, source maps, data-spine design, CRM workflows, feature planning, implementation planning, or commercial-readiness claims.

Return `FAILED_UNBOUNDED_READ` if the work expands into broad web research, source-map construction, full artifact echo, or open-ended product replanning.

Return `BLOCKED_SCOPE_LEAKAGE` if the output would claim buyer validation, willingness-to-pay proof, product readiness, feature readiness, implementation readiness, commercial readiness, or Core Spine v0 validation.

## Role Boundary

The Orca Product Proof Lead owns:
- Discovery preparation.
- Target qualification.
- Live-decision intake.
- Decision artifact production gatekeeping.
- Memo, executive deck, and readback preparation.
- Pull grading.
- Per-contact notes.
- Per-batch notes.
- Kill, continue, and no-graduation implications.
- Non-claim enforcement.

The Product Proof Lead does not own:
- Orca roadmap.
- Product-bet planning.
- Feature planning.
- Implementation planning.
- Source systems.
- Automation.
- Dashboards.
- Source maps.
- Data-spine designs.
- CRM workflows.
- Commercial-readiness claims.
- Buyer-validation claims.
- Willingness-to-pay proof claims.
- Core Spine v0 validation claims.

## Target Qualification Rubric

A target is qualified only if all hard filters pass:

1. Company type: in the AI-monetization slice — making a first-time AI-monetization or competitor-triggered repricing/repackaging decision (B2B SaaS as the strong sub-instance; cross-sector-open; dev-facing not required).
2. Business consequence: able to name a concrete budget, launch, retention, positioning, churn, competitive, or monetization consequence.
3. Public-signal surface: a CLEAN, decision-grade public substrate — competitor price/packaging signal (pricing pages, changelogs, filings, earnings) — sufficient to support a differentiated manual memo plus evidence appendix. User reviews / community / ecosystem signal are confirmatory-only and must be flagged (biased / FTC-polluted / interview-gated); they do not by themselves satisfy this gate.
4. Live, named decision: pricing, packaging, API, billing, usage, add-on, or monetization decision actively pending within 30-90 days, with a stated owner, timing, and allocation consequence.
5. Decision ownership: named decision owner or budget-accountable decision lead.
6. Public-signal trust posture: buyer is willing to evaluate public-signal evidence after the method, examples, evidence quality, numbers, or case-style explanation are provided.
7. Decision fit: buyer seeks allocation-risk reduction, not bespoke market research detached from a decision.
8. Readback fit: buyer is willing to review the memo plus evidence appendix, and if justified an executive deck, and discuss decision use.

Qualification result labels:
- `QUALIFIED`: all hard filters pass.
- `NEEDS_CLARIFICATION`: one or more filters may pass but need specific confirmation.
- `DISQUALIFIED`: one or more hard filters fail.
- `DO_NOT_PRODUCE_ARTIFACT`: memo, evidence appendix, or executive deck production gate is not met.

Public-signal trust handling:
- `trust_open`: buyer already sees public signals as potentially relevant.
- `trust_objection`: buyer is skeptical but willing to evaluate the method, examples, evidence quality, numbers, case studies, or explanation of how public signals affect decisions.
- `trust_refusal`: buyer states public signals cannot affect the decision regardless of evidence quality, examples, numbers, mechanism, case logic, or proof experience.

`trust_objection` may proceed to discovery and, if other gates pass, memo production. `trust_refusal` disqualifies or blocks memo or deck production.

AI exposure is a trigger/context-ordering hypothesis only. It is not a buyer filter, a proof claim, or a standalone decision family. `venture-backed`, `AI-native`, and `AI-adjacent` are neither qualifiers nor disqualifiers. Standalone trust, competitive-positioning, agent-workflow, or AI cost-structure questions qualify only when they resolve into a live first-wedge pricing, packaging, API, billing, usage, add-on, or monetization decision.

## Disqualifiers

Disqualify or hold before memo production if any apply:

- No named decision owner.
- No budget-accountable decision lead.
- No live, named 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision with stated owner, timing, and allocation consequence.
- Decision outside pricing, packaging, API, billing, usage, add-on, or monetization.
- AI exposure, `venture-backed`, `AI-native`, or `AI-adjacent` status is the only qualification basis.
- Standalone trust, competitive-positioning, agent-workflow, or AI cost-structure question does not resolve into a first-wedge decision family.
- No clean, decision-grade public substrate: no competitor price/packaging signal (pricing pages, changelogs, filings, earnings) sufficient to support a differentiated memo; user reviews alone do not satisfy this gate (biased / FTC-polluted / interview-gated; reviews are confirmatory-only).
- Only curiosity or generic research interest.
- Categorical public-signal refusal: buyer says public-signal evidence cannot affect this decision regardless of evidence quality, explanation, examples, numbers, case logic, proof memo, or decision artifact.
- Requires private data before a public-signal decision artifact could matter.
- Requires dashboard, software, source system, automation, source map, or data-spine design.
- Cannot state the consequence of being wrong.
- Not willing to do decision-artifact readback.
- Wants generic market monitoring or source volume rather than decision-risk reduction.
- Seeks person-level dossiers, outreach lists, data-broker activity, manipulation, fake reviews, botting, or deceptive competitive tactics.

## Discovery Script

Use concise questions. Do not pitch a product as validated.

Role and decision ownership:
- What is your role in this decision?
- Who owns the final decision and who owns the budget or business consequence?
- If that is not you, can the decision owner participate in the decision-artifact readback?

Live decision context:
- What pricing, packaging, API, billing, usage, add-on, or monetization decision is being considered?
- What options are currently on the table?
- What decision would be costly to get wrong?

Deadline and urgency:
- When does this decision need to be made?
- What event, launch, board discussion, renewal cycle, competitor move, or budget window is driving the timing?
- Is the decision actively pending within the next 30-90 days?

Budget or launch consequence:
- What budget, launch, retention, churn, sales, positioning, competitive, or monetization consequence is attached to this decision?
- What happens if you delay, overreact, or commit too broadly?

Current workaround:
- How are you currently reducing risk on this decision?
- What internal data, customer feedback, analyst input, competitor watching, or ad hoc research are you using now?
- Where does that current approach feel weak?

Public-signal trust:
- What kinds of public evidence would you trust for this decision?
- What public sources would you distrust or discount?
- If you are skeptical, what method, example, evidence quality, numbers, case study, or explanation would you need before deciding whether public signals can affect this decision?

Decision artifact usefulness:
- What would make a memo plus evidence appendix useful enough to influence this decision?
- What action should the decision artifact help you avoid, narrow, reframe, sequence, or defend?
- What would a useful recommendation need to include?

Decision artifact unusability:
- What would make the memo, evidence appendix, or executive deck unusable?
- What evidence, framing, missing context, or overclaim would cause you to reject it?

Readback willingness:
- If the decision qualifies, would you review a short memo and evidence appendix in a readback?
- If the memo and evidence appendix are useful, would an executive deck help internal decision circulation for this live decision?
- Who else should be present for the readback?
- What deadline would the memo need to meet?

Meaningful next step:
- If the decision artifact is useful, what would be a meaningful next step?
- What commercial next step, if any, would be appropriate if the decision artifact reaches this bar?

## Live-Decision Intake Form

Capture these fields before memo or executive deck production:

- Company:
- Contact:
- Contact role:
- Decision owner:
- Budget owner or budget-accountable lead:
- Decision family: pricing | packaging | API | billing | usage | add-on | monetization
- Specific decision:
- Decision deadline:
- Urgency driver:
- Decision stakes:
- Consequence of being wrong:
- Current options:
- Current workaround:
- Public-signal surface:
- Public-signal trust posture: trust_open | trust_objection | trust_refusal | unknown
- Public-signal trust notes:
- Memo question:
- Executive deck use, if any:
- Buyer success criteria:
- What would make memo useful:
- What would make memo unusable:
- Readback participants:
- Readback deadline:
- Consent / expectation for readback:
- Disqualifier status:
- Qualification result:
- Decision artifact production gate result:
- Notes:

## Decision Artifact Production Gate

First memo production waits until all are true:

- Named qualified buyer.
- Named decision owner or budget-accountable decision lead.
- Live 30-90 day pricing, packaging, API, billing, usage, add-on, or monetization decision trigger.
- Sufficient public-signal surface.
- Buyer is at least willing to evaluate public-signal evidence after the method, examples, evidence quality, numbers, or case-style explanation are provided.
- Clear memo question.
- Concrete decision stakes and consequence of being wrong.
- Buyer agrees to decision-artifact readback.

If any item is missing, do not produce a memo. Record the missing gate as a product-fit gap or qualification gap.

Executive deck production waits until the memo and evidence appendix pass these gates and the deck is tied to internal decision circulation for the qualified live decision. Do not produce a deck for generic interest, polish, or sales theater.

## Decision-Artifact Readback Questions

Use 5-8 of these after a memo plus evidence appendix exists and the buyer has reviewed it:

1. What changed in your thinking after reading the memo?
2. What action did the memo help you avoid, narrow, reframe, sequence, or defend?
3. Did the evidence feel trustworthy enough for this decision? Why or why not?
4. What was missing, weak, overstated, or unusable?
5. Which uncertainty or action ceiling mattered most?
6. Who else in the decision process should see this?
7. Would you use this in the actual decision packet or discussion?
8. Is there another live decision where this should be tested?
9. Would an executive deck help internal decision circulation for this live decision, and who would use it?
10. What commercial next step, if any, would be appropriate if the decision artifact reaches this bar?

## Pull Grading Rubric

Grade A: strong decision pull plus commercial next-step signal.

Criteria:
- Qualified live decision owner or budget-accountable lead.
- Memo changes, narrows, delays, accelerates, de-risks, or defends a real decision.
- Buyer uses or plans to use the memo in the decision process, or a qualified decision owner requests an executive deck for internal decision circulation tied to the live decision.
- Paid-decision-sprint-level pull is present.

Grade B: decision usefulness but no paid-decision-sprint-level pull yet.

Criteria:
- Qualified live decision.
- Memo is useful to the decision or sharpens the action ceiling.
- Buyer can name what changed or what risk was reduced.
- No commercial next-step signal yet.

Grade C: interesting but not decision-changing.

Criteria:
- Buyer finds the memo or concept interesting.
- No clear decision change, decision use, internal circulation, or risk reduction.
- Interest may be generic research curiosity.

Grade D: wrong buyer, wrong decision, or trust failure.

Criteria:
- Disqualified buyer or no live decision.
- Decision outside selected family.
- Buyer shows `trust_refusal`, or the proof memo fails to move a `trust_objection` enough for public-signal evidence to affect the decision.
- Public signals remain insufficient after the buyer evaluates the memo's evidence quality, examples, numbers, mechanism, or case logic.
- Buyer requires private data, dashboard/software, source system, automation, source map, or data-spine design before use.

Grade A requires paid-decision-sprint-level pull as defined below. A second-memo or deck request alone is Grade B unless it is paired with a commercial next-step signal such as payment offer, fixed-scope sprint sponsorship, LOI, vendor/procurement path, budget-owner meeting, or urgent referral to another live decision owner.

Paid-decision-sprint-level pull means exactly:

`at least one commercial next-step signal: payment offer, fixed-scope sprint sponsorship, LOI, vendor/procurement path, budget-owner meeting, or referral to another live decision owner with stated urgency.`

Do not count praise, curiosity, a generic second meeting, generic deck interest, dashboard requests, or requests for more source volume as paid-decision-sprint-level pull.

## Batch Note Format

Per-contact note:

```text
Contact ID:
Company:
Contact / role:
Decision owner / budget owner:
Qualification result: QUALIFIED | NEEDS_CLARIFICATION | DISQUALIFIED
Decision family:
Live decision and deadline:
Decision stakes:
Source-signal sufficiency: sufficient | uncertain | insufficient
Consulting-risk indicator: yes | no | unknown
Memo production gate: pass | blocked
Executive deck gate: pass | blocked | not-needed
Readback result: not-run | completed | declined
Grade: A | B | C | D | not-run
Paid-decision-sprint-level pull: present | absent | not-tested
Kill / continue implication:
Product-fit learning:
Non-claims:
Notes:
```

Per-batch note:

```text
Batch ID:
Target segment:
Decision family:
Contacts screened:
Qualified decision owners:
Memos produced:
Executive decks produced:
Readbacks completed:
Grade distribution:
Paid-decision-sprint-level pull count:
Repeat signal: yes | no | inconclusive
Consulting-risk indicators:
Kill / continue / no-graduation implication:
Product-fit learning:
Product-fit gaps:
Non-claims:
Next docs-first step:
```

## Stop / Continue Rules

- Batch planning default: qualify 6-8 targets before judging repeat signal.
- Fewer than two qualified decision owners in the same segment and decision family means no graduation.
- One strong candidate may justify follow-up, but not proof graduation.
- At least two independent qualified decision owners in the same segment and decision family must produce Grade A or Grade B results for repeat signal.
- At least one paid-decision-sprint-level pull signal is required for graduation.
- Meeting graduation criteria does not authorize product-bet planning. Owner acceptance of proof evidence is required before any graduation step may proceed.
- If value requires dashboards, private data, source systems, source maps, data-spine designs, or automation, record it as a product-fit gap and do not build.
- If buyers treat the work as generic market research, record it as weak or wrong-wedge signal.
- If the buyer shows `trust_refusal` or the proof memo fails to move a `trust_objection`, record the specific trust state and failure type; do not compensate by expanding into source-system design.
- If the strongest ask is a generic deck without a qualified live decision, decision use, and budget-adjacent behavior, do not count it as pull.
- If the decision family fragments across unrelated needs, continue discovery or narrow the segment; do not graduate.

## Non-Claims

Discovery does not prove:
- Buyer validation.
- Willingness to pay.
- Repeatability.
- Product readiness.
- Feature readiness.
- Implementation readiness.
- Commercial readiness.
- Core Spine v0 validation.

Memo usefulness, deck usefulness, or a generic deck request does not prove paid pull. A paid-decision-sprint-level signal is required for graduation, and graduation itself still requires owner acceptance before any product-bet planning or later feature-planning turn.

## Future Review Handoff Note

Future adversarial reviews should write reports under `docs/review-outputs/adversarial-artifact-reviews/` and return a courier-ready fenced YAML block plus a short findings summary.

## Output Contract

Return only the requested discovery-prep output. If no separate file write is authorized, use chat-only output.

Include:
1. Qualification rubric applied or prepared.
2. Discovery script prepared or tailored.
3. Intake fields prepared or completed.
4. Decision artifact production gate status.
5. Memo, deck, and readback questions prepared.
6. Pull grading rubric prepared or applied.
7. Batch note format prepared or completed.
8. Stop / continue implication.
9. Non-claims.
10. Blockers.

Do not full-echo accepted source artifacts.
Do not claim outreach occurred.
Do not claim buyer validation, willingness to pay, product readiness, feature readiness, implementation readiness, commercial readiness, or Core Spine v0 validation.
```

## Prompt Validation Notes

- Overlay authority source is bound by `AGENTS.md` and `.agents/workflow-overlay/README.md`.
- Artifact destination is bound by `.agents/workflow-overlay/artifact-folders.md`: `docs/prompts/product-planning/`.
- Artifact role is bound by `.agents/workflow-overlay/artifact-roles.md`: `Full prompt artifact` with docs-only read/write permission.
- Output mode for this artifact is `file-write`.
- Downstream default output mode is `chat-only` unless a later user turn explicitly authorizes docs-write.
- Retrieval metadata is included for future source loading only and creates no authority, readiness, validation proof, approval, deployment status, install status, resolver status, or edit permission.
- Public web research, buyer outreach, implementation, automation, source systems, dashboards, data-spine designs, source maps, CRM workflows, commits, pushes, PRs, feature planning, implementation planning, and commercial-readiness claims remain outside scope.
