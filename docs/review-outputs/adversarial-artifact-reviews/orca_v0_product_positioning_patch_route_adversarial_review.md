```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial review of the Orca v0 product-positioning patch route.
use_when:
  - Inspecting product-positioning patch-route findings and blockers.
  - Tracing later positioning patches to this review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

```yaml
review_summary:
  review_target: "Orca v0 product-positioning docs patch route"
  verdict: BLOCKED
  critical_findings: 0
  major_findings: 4
  minor_findings: 2
  report_path: "docs/review-outputs/adversarial-artifact-reviews/orca_v0_product_positioning_patch_route_adversarial_review.md"
  next_action: "revise_route"
```

## Findings

### Critical

None.

### Major

#### AR-01 - Downstream prompt and discovery artifacts are missing from stale-source handling

- severity: major
- location: Proposed touch set and PHASE-4 stale-term sweep.
- issue: The route updates `docs/product/orca_buyer_proof_packet_v0.md` and `docs/product/orca_product_proof_lead_charter_v0.md`, but omits the downstream operating prompt and discovery artifacts whose hashes, gates, and language depend on those product-proof sources.
- evidence: `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md` binds product-proof input hashes at lines 17-24 and states `stale_if` either accepted product-proof artifact hash changes at lines 25-26. The same prompt still asks whether the buyer would review a "short memo and evidence appendix" at line 227 and defines a `Memo Production Gate` at line 267. `docs/product/orca_discovery_batch_0_target_selection_brief_v0.md` has `input_hashes` at line 17 and memo-readback gates at lines 86, 99, 131, and 151.
- impact: A product-positioning patch can leave an accepted customer-discovery prompt and batch artifacts pointing at stale memo-centered product proof, or force a hash mismatch without a route for refreshing or quarantining the prompt. Future agents could run stale proof preparation while believing the premium artifact model has already shifted.
- recommended correction: Add explicit stale-source handling to the route. Either include the downstream customer-discovery prompt and affected Discovery Batch 0 artifacts in the write set, or add a clear deferral rule that they must not be used until refreshed against the updated proof packet and charter. This should be route-level scope control, not an implementation patch queue.

#### AR-02 - Raw-noise positioning must not weaken the clean-evidence boundary

- severity: major
- location: Proposed value proposition for `docs/decisions/turn_08_product_thesis_v0.md` and `docs/product/core_spine_v0_product_contract.md`.
- issue: "Messy, noisy, and contradictory public market signals" is accurate for raw input, but unsafe if it replaces the existing clean-evidence promise without explicitly preserving the cleanup and inspectability step.
- evidence: The current thesis says Orca "uses clean public market signals" at `docs/decisions/turn_08_product_thesis_v0.md:11` and names "clean public evidence plus signal-quality judgment plus decision accountability" as the durable wedge at line 29. Core Spine currently turns public signals into "inspectable allocation recommendations" in `docs/product/core_spine_v0_product_contract.md:11`. The information foundation requires every decision memo to include an evidence appendix and reconstruction path at `docs/product/core_spine_v0_information_production_foundation_v0.md:365`.
- impact: If the patch says Orca turns noisy signals into decks without saying those signals are cleaned, source-backed, and inspectable before they become final evidence, the positioning can drift into generic strategy consulting, market research, OSINT collection, or deck production.
- recommended correction: Keep the raw/final distinction explicit: raw public market signals are messy; Orca cleans, classifies, source-backs, and constrains them into inspectable decision artifacts. The executive deck can be premium buyer-facing packaging, but the evidence appendix and inference chain remain part of the rigor layer.

#### AR-03 - Paid sprint and bespoke language need tighter consulting-drift guardrails

- severity: major
- location: Proposed commercial path and bespoke model for the buyer proof packet and proof lead charter.
- issue: A paid decision sprint is a stronger commercial unit than hourly or generic retainer work, but it can still become unbounded consulting if the route relaxes the existing manual-session and bespoke-risk controls.
- evidence: Both `docs/product/orca_buyer_proof_packet_v0.md:105` and `docs/product/orca_product_proof_lead_charter_v0.md:105` say the proof memo should be producible in one focused manual session, indicatively 4-6 hours, and that materially exceeding this is consulting-risk evidence. The buyer proof packet treats "bespoke consulting with no repeatable pattern" as a weak or kill signal at lines 185 and 246. The charter says value depending on bespoke consulting labor with no repeatable decision pattern is a kill/reframe condition at line 152. `.agents/workflow-overlay/product-proof.md:134-141` preserves non-claims including no willingness-to-pay proof and no commercial readiness.
- impact: Reframing the offer as a paid decision sprint or allowing the last 10-20% bespoke work is safe only if bounded. If it becomes "more hours are fine because sprint" or "bespoke is the product," Orca drifts into custom consulting and may imply willingness-to-pay or commercial-readiness proof before evidence exists.
- recommended correction: Treat "paid decision sprint" as a fixed-scope offer hypothesis and proof step, not a validated commercial model. Preserve a scope ceiling, explicit deliverables, a core/satellite/bespoke split, and a rule that overages or repeated custom work are consulting-risk evidence unless tied to a repeatable decision family. Retainer language should remain conditional on recurring decision cadence and buyer pull.

#### AR-04 - Overlay update scope is mostly right, but validation-gate routing is under-specified

- severity: major
- location: Proposed PHASE-3 overlay patch route.
- issue: Touching overlay files is reasonable only where future routing would otherwise conflict, but the proposed overlay touch set misses or under-specifies the deck/readback gate conflict.
- evidence: `.agents/workflow-overlay/artifact-roles.md:30`, `.agents/workflow-overlay/artifact-folders.md:31`, `docs/STRUCTURE.md:22`, and `docs/product/README.md:3` still describe product artifacts as including "decision-memo shape drafts." `.agents/workflow-overlay/product-proof.md:74` says praise, curiosity, "interest in a deck," or generic research requests are not pull. `.agents/workflow-overlay/validation-gates.md:56` refers to "memo-readback artifacts" in product-proof gates.
- impact: If the executive-grade deck becomes the premium buyer-facing artifact, a generic request for a deck should still not count as pull, but a qualified decision owner asking for a deck for internal decision circulation after decision use may be meaningful. Leaving validation gates memo-only and product-proof deck language unqualified can create routing conflicts.
- recommended correction: Patch overlay only after the product docs define the memo/deck distinction. At minimum, update artifact role/folder descriptions where "decision-memo shape drafts" would misroute future deck artifacts, and clarify product-proof language so generic deck interest is not pull while decision-owner deck/internal-circulation behavior can be evaluated as pull. Either include `validation-gates.md` in the route or explicitly defer deck-readback gate changes with a no-use boundary.

### Minor

#### AR-05 - "Still v0" is acceptable only with freshness signals on hash-bound artifacts

- severity: minor
- location: Proposed "no historical continuity, still v0" assumption.
- issue: Keeping the artifacts as v0 is safe, but silently rewriting hash-bound v0 artifacts can confuse future source loading unless freshness is updated.
- evidence: `.agents/workflow-overlay/retrieval-metadata.md:19-24` applies retrieval headers to materially touched durable artifacts, while lines 99-107 describe stale and supersession fields when they prevent stale-source mistakes. The buyer proof packet and proof lead charter both carry input hashes at `docs/product/orca_buyer_proof_packet_v0.md:15` and `docs/product/orca_product_proof_lead_charter_v0.md:15`.
- impact: Future agents may treat older hash-bound prompt and proof artifacts as current even after a positioning rewrite, or may block on mismatched hashes without knowing whether the mismatch is expected.
- recommended correction: Do not add a heavy historical changelog by default. Do update material input hashes and add narrow `stale_if`, `supersedes`, or body freshness language where the artifact is used for routing, proof, or downstream prompt execution.

#### AR-06 - The stale-term sweep must not treat all memo language as stale

- severity: minor
- location: Proposed PHASE-4 stale-term consistency sweep.
- issue: "Decision memo" is not globally stale under the proposed model. The user-provided product model keeps the memo as the minimum viable artifact and reasoning substrate.
- evidence: `docs/product/core_spine_v0_product_contract.md:42` defines Decision Memo as the primitive that produces recommendation, evidence basis, alternatives, uncertainty, kill criteria, and what would change the answer. `docs/product/core_spine_v0_information_production_foundation_v0.md:365` defines required memo contents. The proposed model says the premium buyer-facing artifact is the executive-grade decision deck, not that the memo disappears.
- impact: A broad stale-term replacement can accidentally remove the substrate and proof gate that keep the deck from becoming presentation work.
- recommended correction: Split stale terms into three buckets: keep "decision memo" where it means reasoning substrate, proof gate, or minimum artifact; supplement with "executive decision deck" where it means buyer-facing premium artifact; replace only memo-as-sold-artifact language that contradicts the new model.

## Non-Findings

- The proposed value proposition preserves Orca's decision-intelligence boundary if the final artifact is explicitly tied to decision verbs such as accelerate, narrow, delay, defend, and reframe.
- "Messy, noisy, and contradictory public market signals" is directionally accurate for raw input; the issue is only whether the final evidence layer stays clean and inspectable.
- The memo/deck distinction is coherent: memo as reasoning substrate and minimum viable artifact; deck as premium buyer-facing artifact derived from the memo plus evidence appendix.
- The core/satellite/bespoke model is coherent if Core remains the repeatable decision spine, satellites carry decision-specific adaptation, and bespoke work is capped and treated as consulting-risk evidence when it stops repeating.
- Starting with a paid decision sprint is safer than leading with a generic retainer or hourly billing, provided it is not described as validated demand or commercial readiness.
- Touching `docs/STRUCTURE.md` and `docs/product/README.md` for directory language is not inherently overreach. They are directory guides, and `.agents/workflow-overlay/retrieval-metadata.md:42-46` excludes simple folder README files from mandatory retrieval headers.

## Not-Proven Boundaries

This advisory review does not prove or claim:

- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- Core Spine v0 validation;
- that the patch route is approved, validated, accepted, implementation-ready, or commercially ready.

The current working tree is dirty, including modified overlay authority files and untracked product-proof sources. This report uses current working-tree evidence for advisory review only; it does not claim clean revision-anchored formal validation.

## Recommended Next Action

Revise the route before source-changing documentation work begins. The revision should add downstream stale-source handling, preserve the raw-to-clean evidence boundary, bound paid-sprint and bespoke language, and either include or explicitly defer deck/readback overlay gate updates.

Findings are decision input for the authorized decision-maker, not mandatory remediation. Only a separately authorized patch or execution lane can make remediation executor-ready.
