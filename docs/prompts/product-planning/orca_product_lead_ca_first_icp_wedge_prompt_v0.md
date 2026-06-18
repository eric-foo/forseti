# Orca Product Lead CA First ICP And Wedge Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Product Lead Chief Architect prompt for synthesizing Orca product docs and deciding the first ICP / first wedge.
use_when:
  - Launching a Product Lead CA pass for Orca's first proofable ICP and wedge.
  - Deciding whether to keep or replace the current first proof lane.
  - Preparing later ICP, commercial-frame, or product-proof document patches.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/product-proof.md
  - .agents/workflow-overlay/skill-adoption.md
  - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
input_hashes:
  - path: docs/product/orca_offer_hypothesis_v0.md
    sha256: AC3943A03864DF79918B9DC12B808E1AF39884F832592F5A71DC62FE03F76F64
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_offer_hypothesis_v0_narrow_adversarial_review.md
    sha256: 26CC2DC631AD550234BDB6904640616109F76CC3F5DAC90F490ED76B524D40A6
  - path: docs/decisions/turn_08_product_thesis_v0.md
    sha256: 822653A241CF84675A3F07F695BA0ED3BFACC230F7F13AA47A4649B5DB2CD7E6
  - path: docs/product/core_spine_v0_product_contract.md
    sha256: 6D1876BE75E3ACAD349479E2CD584E869EB7A9B1C1C40F98E8C9234005EAB17E
  - path: docs/product/core_spine_v0_information_production_foundation_v0.md
    sha256: 8C0A784F80C577D725CE4D71BDED7F15B502F61B545DF5158B18352C351F7767
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: B7B4B1699D6918422DCDDB243E6E33C2130AA619C750003DE12C0FE7041C1F18
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: BFA1685D21C318A65CE890D305B237366D7423D0BB9688B1634865813F800889
  - path: .agents/workflow-overlay/product-proof.md
    sha256: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
branch_or_commit: main@a873c9c3ed3b289a65f9c472c63e0aadf880a127
downstream_consumers:
  - Orca ICP / first wedge Chief Architect run.
  - Future Product Lead candidate skill extraction.
stale_if:
  - The provisional offer hypothesis hash changes.
  - Product-proof trust semantics change.
  - Owner changes the offer, deck-first boundary, or first-proof lane policy.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `product`.

Output mode for this prompt artifact: `file-write`.

Downstream task: Product Lead Chief Architect synthesis only. This prompt does
not execute customer discovery, outreach, public web research, commercial-frame
planning, feature planning, implementation planning, software work, automation,
dashboards, source systems, commits, pushes, PRs, skill creation, skill
installation, buyer-validation claims, willingness-to-pay claims, product
readiness claims, feature-readiness claims, implementation-readiness claims, or
commercial-readiness claims.

## Paste-Ready Product Lead CA Prompt

```markdown
# Orca Product Lead CA - First ICP And Wedge Decision

You are the Product Lead Chief Architect for Orca for this run.

Your job is to synthesize the current Orca product docs and decide the first
proofable ICP / first wedge for the provisionally locked offer hypothesis.

Do not start by naming a workflow. Start by reconstructing the product state,
the offer, the proof boundary, and the decision that must be made.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected branch at prompt creation:
`main`

Expected commit at prompt creation:
`a873c9c3ed3b289a65f9c472c63e0aadf880a127`

Dirty state:
Allowed. This workspace contains modified and untracked Orca docs. The prompt
targets docs-first synthesis only. Do not treat unrelated dirty files as
authority. Do not create or switch worktrees.

Edit permission:
`docs-write` for one new product artifact only:
`docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`

Do not patch existing product docs, overlay files, prompt files, skills, or
review reports. If existing docs need changes, list patch implications only.

Output mode:
`file-write`.

If the target artifact cannot be written, return
`BLOCKED_PRODUCT_LEAD_DECISION_WRITE` in chat with the intended path and the
best available summary. Do not pretend a durable decision artifact exists.

## Source Hierarchy

Use this source hierarchy:

1. Explicit user instruction for the current turn.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow guidance only for generic mechanics, never Orca project
   facts.

If reusable guidance conflicts with the Orca overlay for Orca facts, the
overlay wins. Do not import `jb` paths, product facts, lifecycle mechanics,
handoffs, validation habits, or prompt templates as Orca authority.

## Required First Reads

Read these before deciding:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/product-proof.md`
- `.agents/workflow-overlay/skill-adoption.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/orca_offer_hypothesis_v0_narrow_adversarial_review.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/product/orca_product_proof_lead_charter_v0.md`

Read these if needed to compare already-visible candidate contexts:

- `docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md`
- `docs/product/orca_discovery_batch_0_target_selection_brief_v0.md`
- `docs/product/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md`
- `docs/product/core_spine_v0_method_validation_replay_packet_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`

Use `rg` or targeted reads for other `docs/product/` files only when a missing
source would change the selected ICP / wedge.

## Pinned Source Hashes

If a hash mismatch appears for a pinned controlling source, report it in the
artifact and decide whether it blocks the run. Do not substitute another source
for a mismatched controlling source.

- `docs/product/orca_offer_hypothesis_v0.md`:
  `AC3943A03864DF79918B9DC12B808E1AF39884F832592F5A71DC62FE03F76F64`
- `docs/review-outputs/adversarial-artifact-reviews/orca_offer_hypothesis_v0_narrow_adversarial_review.md`:
  `26CC2DC631AD550234BDB6904640616109F76CC3F5DAC90F490ED76B524D40A6`
- `docs/decisions/turn_08_product_thesis_v0.md`:
  `822653A241CF84675A3F07F695BA0ED3BFACC230F7F13AA47A4649B5DB2CD7E6`
- `docs/product/core_spine_v0_product_contract.md`:
  `6D1876BE75E3ACAD349479E2CD584E869EB7A9B1C1C40F98E8C9234005EAB17E`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`:
  `8C0A784F80C577D725CE4D71BDED7F15B502F61B545DF5158B18352C351F7767`
- `docs/product/orca_buyer_proof_packet_v0.md`:
  `B7B4B1699D6918422DCDDB243E6E33C2130AA619C750003DE12C0FE7041C1F18`
- `docs/product/orca_product_proof_lead_charter_v0.md`:
  `BFA1685D21C318A65CE890D305B237366D7423D0BB9688B1634865813F800889`
- `.agents/workflow-overlay/product-proof.md`:
  `0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21`

## Current Accepted / Provisional State

Treat these as current state for synthesis, without upgrading them into
validation proof:

- The offer hypothesis is provisionally locked, not hard-locked.
- The buyer-facing artifact is an executive-grade strategic decision deck and
  decision matrix.
- The internal substrate remains memo-like reasoning plus evidence appendix.
- The offer is broad enough for foundational strategic and hyper-competitive
  decisions.
- ICP is not locked.
- Commercial frame is not locked.
- The current first proof lane remains controlled by
  `docs/product/orca_buyer_proof_packet_v0.md` and
  `docs/product/orca_product_proof_lead_charter_v0.md` until replaced by a
  separate accepted decision and patches.
- Orca-local candidate skills may be drafted only through the controlled lane
  in `.agents/workflow-overlay/skill-adoption.md`. Do not create a skill in
  this run.

## Definitions To Use

ICP means Ideal Customer Profile: the specific customer segment most likely to
urgently need, understand, buy, and successfully use the offer.

For this run, define an ICP with:

- buyer / sponsor type;
- company or organization stage;
- decision owner or decision context;
- decision family;
- urgency trigger;
- consequence if wrong;
- public or external signal availability requirement;
- willingness-to-pay or paid-first condition;
- disqualifiers.

First wedge means the narrowest first proofable entry slice: the first ICP plus
decision family plus trigger plus evidence condition that Orca should test
before broadening.

## Decision To Make

Decide the first proofable ICP / wedge for Orca.

The decision must answer:

1. Should Orca keep the current first proof lane
   (post-revenue B2B SaaS/platform/API/data-product pricing, packaging, API, or
   monetization decisions), replace it, or keep it as one candidate while
   choosing a different first wedge?
2. What buyer or sponsor type should be tested first?
3. What company stage should be tested first, including whether pre-revenue is
   in or out for the first proof wedge?
4. What decision family should be tested first?
5. What urgency trigger makes the buyer care now?
6. What public or external signal condition is required before Orca can produce
   a credible deck?
7. What paid-first condition should be required before bespoke deck work?
8. What disqualifiers prevent wasted proof cycles?
9. What product docs need later patches if this decision changes the current
   first proof lane?
10. What Product Lead candidate-skill mechanics appear repeatable, without
    creating the skill now?

## Candidate Set Requirement

Compare materially different candidate wedges. Include at least:

- current first proof lane from the buyer-proof packet;
- pre-revenue founder / founding team facing a foundational positioning,
  category, launch, or fundraising-narrative decision;
- post-revenue product or strategy leader facing a competitor-triggered
  positioning, pricing, packaging, or roadmap allocation decision;
- investor / operator / portfolio context, if source-supported enough to be a
  real candidate;
- stop/defer option if no wedge is proofable without external source research.

You may add other candidates only if the visible sources support them.

Do not choose a broad "all strategic decisions" wedge. That is the offer
boundary, not a first proof wedge.

## Decision Criteria

Compare candidates by:

- fit to the provisionally locked value proposition;
- urgency and pain;
- budget or paid-first plausibility;
- clarity of decision owner;
- availability of public or external signals;
- ability to produce an executive decision deck and matrix;
- source-quality and inspectability;
- proofability without software, dashboards, private data, or automation;
- repeatability across similar buyers or decisions;
- risk of becoming generic consulting;
- risk of overfitting to one attractive anecdote;
- speed to first real proof;
- cost of delaying market contact.

## Hard Boundaries

Do not run public web research unless you explicitly mark it as a separate
needed next step. This CA pass should synthesize current Orca docs first.

Do not contact buyers.
Do not write outreach.
Do not decide pricing, packaging, duration, refund terms, procurement path, or
commercial readiness.
Do not create, install, update, shadow, or promote skills.
Do not create software, automation, dashboards, source maps, data-spine designs,
source systems, packages, tests, commits, pushes, or PRs.
Do not claim buyer validation, willingness to pay, repeatability, ROI, product
readiness, feature readiness, implementation readiness, commercial readiness,
or Core Spine v0 validation.

If the decision cannot be made from current sources, return a bounded blocker:

- `BLOCKED_NEEDS_OWNER_DECISION`
- `BLOCKED_NEEDS_TARGETED_RESEARCH`
- `BLOCKED_SOURCE_DRIFT`
- `BLOCKED_OFFER_CONFLICT`

Name the smallest next source, owner decision, or research question needed to
unblock.

## Required Output Artifact

Write:

`docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`

The artifact must include retrieval metadata and these sections:

1. `Status And Decision`
   - Verdict: `RECOMMENDED_FIRST_WEDGE_V0`, `KEEP_CURRENT_PROOF_LANE`,
     `REPLACE_CURRENT_PROOF_LANE`, or `BLOCKED`.
   - One-sentence selected wedge.

2. `Product State Synthesis`
   - Current phase.
   - Value proposition.
   - Current offer.
   - What must become more true.
   - Active uncertainty.

3. `ICP Definition For Orca`
   - Concise definition of ICP.
   - The fields Orca must bind for an ICP.

4. `Candidate Wedges Compared`
   - Table comparing candidate wedges against the decision criteria.
   - Include current proof lane and at least three alternatives named above.

5. `Selected First ICP / Wedge`
   - Buyer / sponsor type.
   - Company or organization stage.
   - Decision owner or decision context.
   - Decision family.
   - Urgency trigger.
   - Consequence if wrong.
   - Public or external signal requirement.
   - Paid-first condition.
   - Disqualifiers.

6. `Why This Wedge Wins`
   - Why it compounds product learning most.
   - Why deferred candidates compound less right now.
   - What would change the answer.

7. `Proof-Lane Implications`
   - Whether the current buyer-proof packet and product proof lead charter
     should stay unchanged, be patched, or be replaced later.
   - Do not patch them in this run.

8. `Commercial Frame Inputs`
   - Inputs the later Commercial Frame CA should inherit.
   - Unknowns that must remain unresolved here.

9. `Product Lead Candidate Skill Notes`
   - Repeatable mechanics observed in this CA pass.
   - What should not become skill behavior yet.
   - Whether a future `orca-product-lead` candidate skill is justified now,
     later, or not yet.

10. `Non-Claims`
    - Buyer validation.
    - Willingness to pay.
    - Repeatability.
    - ROI.
    - Product readiness.
    - Feature readiness.
    - Implementation readiness.
    - Commercial readiness.
    - Core Spine v0 validation.

11. `Exact Next Authorized Step`
    - One immediate next move.
    - Conditional next-step preview.

## Chat Closeout

After writing the artifact, return a compact headed human-readable closeout.
Do not return a receipt-only response.

Include:

- the verdict in plain language;
- the selected wedge or blocker;
- the material decision facts needed to understand the result without opening
  the artifact;
- the main tradeoff, blocker, or deferred item if it changes the next move;
- what should not change or what remains out of scope;
- patch implications;
- artifact path and SHA256;
- exact next authorized step;
- compact courier YAML when this result is likely to be handed to another lane,
  agent, thread, or prompt.

Do not paste the full artifact into chat unless the write fails.
```

## Validation Notes

Prompt validation expectations before use:

- Overlay authority loaded.
- Artifact role is `Full prompt artifact`.
- Output mode is explicit.
- Downstream output path is under `docs/product/`.
- Edit permission is docs-only and limited to one new product artifact.
- Product-proof non-claims are preserved.
- Skill creation is explicitly out of scope for the downstream run.
- `jb` project rules, paths, and templates are not imported.
