# Orca AI-Exposed ICP Refinement Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Adversarial review prompt for testing whether the AI-exposed ICP refinement improves Orca's first proof wedge.
use_when:
  - Launching an adversarial review of the AI-exposed ICP / first-wedge refinement.
  - Checking whether AI market emphasis creates hype drift or improves market potential.
  - Preparing patch implications for the first ICP wedge decision artifact.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/product-proof.md
  - orca/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md
  - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
input_hashes:
  - path: docs/product/orca_product_lead_first_icp_wedge_decision_v0.md
    sha256: 67608F4E8DD0011E416C3F1619EEB4F2ACAAB1D062C46C0A4EA3527C756705A7
  - path: docs/product/orca_offer_hypothesis_v0.md
    sha256: AC3943A03864DF79918B9DC12B808E1AF39884F832592F5A71DC62FE03F76F64
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: B7B4B1699D6918422DCDDB243E6E33C2130AA619C750003DE12C0FE7041C1F18
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: BFA1685D21C318A65CE890D305B237366D7423D0BB9688B1634865813F800889
  - path: docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md
    sha256: 52A7F5E823A31562EAFDAE389AB51188BCAA021BF3E6B4478F8045435684FE28
  - path: docs/product/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md
    sha256: EA47275CEF6F98872BDE9A00F6488BEE5ED044C4A4BE4482532D2ADDB8CB74F3
  - path: .agents/workflow-overlay/product-proof.md
    sha256: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
downstream_consumers:
  - Orca AI-exposed ICP refinement adversarial review.
  - Future Product Lead decision artifact patch route.
stale_if:
  - The first ICP wedge decision artifact changes.
  - Product-proof trust or non-claim semantics change.
  - Owner accepts or rejects the AI-exposed ICP refinement before review.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Target reviewer: Claude Opus 4.7.

Template kind: `review`.

Output mode for downstream reviewer: `review-report`.

Downstream report destination:
`docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md`

Reviewer edit permission: read-only for source artifacts; write only the review
report named above.

Patch execution: not authorized.

## Paste-Ready Review Prompt

```markdown
# Orca Adversarial Review - AI-Exposed ICP Refinement

You are reviewing an Orca ICP / first-wedge refinement for Product Lead quality.

Target model: Claude Opus 4.7.

Do not rubber-stamp the current direction. Your job is to adversarially test
whether the proposed AI-exposed ICP refinement improves Orca's first proof
wedge or creates market-hype drift.

Begin with `workflow-deep-thinking`: briefly frame the real decision, strongest
failure modes, and criteria that should decide the review. Then produce an
adversarial artifact review. Deep thinking does not widen the scope, authorize
patching, or turn this into product planning.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected source state:
Dirty state is allowed. Review only the named Orca overlay and docs sources.
Do not treat unrelated dirty files as authority.

Expected prompt source:
`docs/prompts/reviews/orca_ai_exposed_icp_refinement_adversarial_review_prompt_v0.md`

Target report path:
`docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md`

Edit permission:
`review-report` write only for the target report path. Do not patch product
docs, prompt files, overlay files, skills, source systems, implementation
files, tests, commits, pushes, or PRs.

If the report cannot be written, return
`BLOCKED_AI_ICP_REVIEW_REPORT_WRITE` in chat with the intended path and the
best available review summary. Do not pretend a durable report exists.

## Source Hierarchy

Use this source hierarchy:

1. Explicit user instruction in this prompt.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with overlay.
5. Reusable workflow guidance only for generic mechanics, never Orca facts.

If reusable guidance conflicts with the Orca overlay for Orca facts, the
overlay wins. Do not import `jb` project rules, lifecycle mechanics,
validation habits, paths, product policy, or templates as Orca authority.

## Required Reads

Read these before reviewing:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/product-proof.md`
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/product/orca_product_proof_lead_charter_v0.md`
- `docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md`
- `docs/product/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md`

Optional if needed:

- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`

## Review Target

The current decision artifact selected this first proof wedge:

> Post-revenue developer-facing B2B SaaS, platform, API, or data-product
> companies with a live 30-90 day pricing, packaging, API, or monetization
> decision where public customer, developer, buyer, competitor, or ecosystem
> signals can change an executive decision deck and decision matrix.

A later second-pass discussion proposed sharpening the wedge to:

> Post-revenue, venture-backed AI-native or AI-adjacent B2B software,
> developer-platform, API, infrastructure, or data-product companies facing a
> live monetization, packaging, pricing, usage, trust, or competitive-positioning
> decision caused by AI adoption, AI cost structure, AI feature bundling, agent
> workflows, or AI-native competitors.

Core claim to review:

> This AI-exposed refinement may be a better first wedge because it preserves
> proofability while increasing long-term market potential, urgency, capital
> density, public-signal density, and strategic upside. But "anything with AI in
> the name" is explicitly rejected as hype drift.

Treat the AI market rationale as a hypothesis, not proof. Do not claim buyer
validation, willingness to pay, or repeatability from AI funding or VC interest.

## Review Questions

Answer these directly:

1. Does the AI-exposed refinement improve the first ICP / wedge, or does it
   weaken proof discipline?
2. Is "AI-exposed monetization and packaging decisions" a valid sharper wedge,
   or is it too trend-driven?
3. Does the refinement preserve the distinction between:
   - broad Orca offer boundary;
   - first proof wedge;
   - later expansion path?
4. Does it keep buyer proof grounded in live decision ownership,
   public-signal availability, paid-first behavior, and non-claims?
5. Does it accidentally create forbidden overconfidence because "VC money is
   flowing into AI"?
6. Should the existing decision artifact be patched now, patched with caveats,
   or left unchanged until more research / discovery?
7. If patched, what exact conceptual changes should be made without
   authorizing outreach, implementation, commercial readiness, or
   buyer-validation claims?

## Criteria

Evaluate against:

- market size and long-term market potential;
- urgency and decision pain;
- budget density and paid-first plausibility;
- clarity of decision owner;
- public/external signal density;
- ability to produce an executive decision deck and matrix;
- proofability without private data, dashboards, source systems, automation, or
  implementation;
- risk of hype chasing;
- risk of generic AI strategy consulting;
- risk of narrowing too far into only AI packaging;
- repeatability across similar buyers;
- alignment with Orca product-proof non-claims.

## Hard Boundaries

Do not run public web research unless you explicitly mark it as a separate
needed next step. This review should primarily inspect current Orca docs and
the proposed refinement.

Do not run outreach.
Do not produce buyer-facing copy.
Do not create or patch product docs.
Do not create, install, update, shadow, or promote skills.
Do not create software, automation, dashboards, source maps, data-spine
designs, source systems, packages, tests, commits, pushes, PRs, or feature
plans.

Do not claim buyer validation, willingness to pay, repeatability, ROI, product
readiness, feature readiness, implementation readiness, commercial readiness,
or Core Spine v0 validation.

Do not recommend "AI companies" as a generic ICP. If you support the AI
refinement, it must stay tied to a specific decision family and qualification
gates.

Initial buyer skepticism about public signal is not a disqualifier. Use the
Orca distinction:

- `trust_objection` is proof material;
- `trust_refusal` disqualifies.

## Required Report Artifact

Write:

`docs/review-outputs/adversarial-artifact-reviews/orca_ai_exposed_icp_refinement_adversarial_review_v0.md`

The report must include retrieval metadata and these sections:

1. `Verdict`
   - Use one of:
     - `ACCEPT_REFINEMENT`
     - `ACCEPT_WITH_CAVEATS`
     - `REJECT_REFINEMENT`
     - `BLOCKED_NEEDS_SOURCE`
   - One-sentence reason.

2. `Best Case For The Refinement`

3. `Strongest Objections`

4. `Failure Modes If Accepted`

5. `What Should Change In The Decision Artifact`
   - If no patch is recommended, say so.
   - If patching is recommended, describe conceptual patch units only.

6. `What Must Not Change`

7. `Evidence Gaps / Not Proven`

8. `Recommendation`
   - Give the exact next authorized step.

9. `Non-Claims`
   - Buyer validation.
   - Willingness to pay.
   - Repeatability.
   - ROI.
   - Product readiness.
   - Feature readiness.
   - Implementation readiness.
   - Commercial readiness.
   - Core Spine v0 validation.

## Chat Closeout

After writing the report, return compact YAML only:

```yaml
status:
report_path:
report_sha256:
verdict:
recommendation:
next_authorized_step:
```

Do not paste the full report into chat unless the write fails.
```

## Validation Notes

Prompt validation expectations before use:

- Overlay authority loaded.
- Artifact role is `Review prompt`.
- Review prompt triggers `workflow-deep-thinking`.
- Output mode is `review-report`.
- Downstream report path is under `docs/review-outputs/adversarial-artifact-reviews/`.
- Reviewer is read-only except for the report path.
- Product-proof non-claims are preserved.
- Skill creation, implementation, outreach, and product-doc patches are out of scope.
- `jb` project rules, paths, and templates are not imported.
