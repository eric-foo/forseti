# no_repo Adversarial Artifact Review Bundle — Demand-Projection F6+R6 Revised Design (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review input artifact (Review prompt role binding, docs/review-inputs/)
scope: >
  Self-contained no_repo review package: method, authority excerpts, commission, and
  attachment manifest for the de-correlated cross-vendor adversarial artifact review of
  demand_projection_f6_r6_revised_design_v0.md. The repo-blind reviewer needs ONLY the files
  in this bundle.
use_when:
  - You are the external, repo-blind, de-correlated reviewer commissioned for this target.
  - The home CA is adjudicating this commission's returned findings.
authority_boundary: retrieval_only
package_shape: self-contained bundle + thin-wrapper chat prompt
  (bound in .agents/workflow-overlay/delegated-review-patch.md, no_repo access mode)
```

## 1. Attachment manifest (confirm before reviewing)

| File | Role | SHA256 |
| --- | --- | --- |
| `demand_projection_f6_r6_revised_design_v0.md` | REVIEW TARGET (verbatim attachment) | `91ACE1B76852006A29A6AB4DF44D3DC108EDA3DF8B33F4C2373DF46D492B0C2F` |
| `README.md` (this file) | Method + authority + commission | (pinned in the courier wrapper) |

If you can compute SHA256, confirm the target matches its pin and say so in your output; if
you cannot, proceed advisory-only and say so. If you cannot read the attached files at all,
reply only `BLOCKED_BUNDLE_UNREADABLE`.

**Freshness gate (assembler-run, 2026-06-11): PASS.** Both `derived_from` pins of the portable
method below were hash-compared against the live Orca sources before bundling and matched
exactly (`adversarial_artifact_review_v0.md` @ `0CB80057…B60C3FC`; `review-lanes.md` @
`7FD702F5…F3C22`). The method ships un-re-derived.

## 2. Commission (no_repo Delegated Review, advisory-only)

```md
# Delegated Review Commission — no_repo access mode

## Lane Binding
- overlay_status: provisional_opt_in (explicit Chief Architect commission for this single use;
  not a bound review lane; creates no strict claims)
- operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md (no_repo mode)
- review_lane: artifact — executed via the PORTABLE METHOD block in §4 of this README
  (registry id portable-adversarial-artifact-review-method); the in-repo review skill is not
  available to you and your result is therefore ADVISORY FINDINGS, never a formal verdict
- mode: base-subagent shape, access: no_repo — you review and propose; you DO NOT patch and
  you return findings, not a diff
- actor_model_family_receipt:
  - author_home_model_family: Anthropic (Claude; authored by claude-fable-5)
  - controller_model_family: operator-dispatched; MUST be a different vendor / model lineage
    than Anthropic (vendor = upstream model developer, not host/reseller/wrapper); unknown or
    undisclosed lineage CANNOT satisfy this commission's cross-vendor discovery bar
  - current_receiving_actor_role: controller (you, on receipt of the courier wrapper)
  - dispatch_mode: external-controller-courier
  - de_correlation_status: gated in the wrapper — self-check before reviewing
- de_correlation: a who-constraint of the commission, NOT a model recommendation or ranking.
  Cross-vendor is the DISCOVERY bar and is required for this pass's
  survives-adversarial-review-with-no-new-seam standard.

## Target
- target: demand_projection_f6_r6_revised_design_v0.md (the single named artifact; whole file)
- why_ordinary_same-family_review_is_insufficient: the design was authored by the same model
  family that will adjudicate it; the author encoded the guardrails and can reintroduce the
  exact blind spots they exist to prevent. De-correlated discovery is required before the
  design gates a build.
- bounded_patch_scope: NONE for you (no_repo). Accepted amendments are applied by the home CA
  to the single target file after adjudication, followed by a bounded SAME-vendor
  mechanical-tier post-patch recheck (closure-of-findings + new blocker/major in the touched
  delta) before anything is kept.
- off_scope: everything beyond the attached files. You cannot and must not assess repository
  state; label repo-settleable claims `unverifiable from provided sources`.

## Roles (who-constraints, not recommendations)
- author / CA / home model (Anthropic family): authored the target; adjudicates every finding;
  owns what is kept; may veto any change at its discretion, even an individually defensible one
- controller (you, de-correlated): judgment, findings, citations into the provided material;
  advisory verdict + residual risk; final authority stays with the CA
- patch executor: not engaged in no_repo mode (CA applies accepted amendments)

## Controller Output Contract
- follow the PORTABLE METHOD (§4) exactly: reasoning pass first, then findings; output shape
  per its §6 (review_summary first, findings ordered critical → major → minor, each with
  severity, location, issue, evidence, impact, minimum_closure_condition,
  next_authorized_action, advisory remediation direction)
- citations: neutral in tone, decision-sufficient in substance — cite the target's own
  sections and the authority excerpts in this README; your argument lives in the verdict and
  residual-risk note, not in the citations
- escalation: if the target's problem is design-level rather than amendment-level, set
  recommendation: NEEDS_ARCHITECTURE_PASS and return findings only — do not propose
  amendment-level fixes for a broken design
- give specific attention to the target's §10 review questions, but do NOT stop there — §10 is
  non-exhaustive by declaration
- do not emit executor-ready patch steps, patch queues, or any claim of validation, readiness,
  approval, or formal verdict

## Adjudication Contract (home / CA model — recorded here for your awareness)
- your findings, citations, and verdict are claims to adjudicate, not premises to inherit
- the CA accepts / modifies / rejects per finding against your citations and the artifact's
  intent; CA-applied amendments then take the bounded same-vendor recheck before keep
- the durable review record (written by the CA at ingestion under
  docs/review-outputs/adversarial-artifact-reviews/) will carry reviewed_by and authored_by
  provenance plus de_correlation_bar: cross_vendor_discovery; state your model identity and
  version in your output if known and permitted — if you do not, the CA records `unrecorded`
  (a visible measurement gap, never fabricated)
```

## 3. Authority excerpts the target must conform to

**Decision criteria / fitness reference:** the target's own §1 (three-valued honesty contract
goal + I1–I7 success signal) and §2 (honesty doctrine + already-accepted set D1/D2/P1+/F4/M-8).
Attack the fitness reference itself as well as conformance to it.

**Authoring environment's foundational behavior + scope-discipline doctrine — AGENTS.md
(Orca), excerpted verbatim** (conformance to this is part of the review):

> Surface ambiguity or risky assumptions before acting.
> Default to the smallest complete intervention: solve the actual request completely with the
> narrowest sufficient scope.
> Every changed line must trace to the user request or required validation.
> Preserve real failure visibility; never create fake success paths.
> For non-trivial changes, define and run relevant verification or state why it was not run.

> **Smallest Complete Intervention.** `Complete` is load-bearing. Do not underfix to minimize
> diff, ceremony, or visible change; a slightly larger fix is correct when required for
> durable, coherent, non-fragile completion. `Smallest` is also load-bearing. Do not add
> unrelated cleanup, speculative abstractions, broad rewrites, extra workflow ceremony, or
> nice-to-have improvements. When two candidate paths both satisfy the current request under
> this rule, prefer the one with materially lower downstream lock-in -- the durable data,
> schema, interface, or workflow shape that would be irreversible, costly to roll back, or
> costly to maintain.

**Review-use boundary (Orca review doctrine, distilled):** your findings are decision input
only — not approval, validation, readiness, mandatory remediation, or executor-ready patch
authority until separately accepted by the commissioning CA.

## 4. PORTABLE METHOD — paste from here to the end marker

### 1. Your stance
You are performing a **read-only, advisory-only adversarial artifact review**. The formal review tooling used inside the authoring environment is **not available to you** — state that explicitly in your output, because it bounds your result to advisory critique, not a formal verdict. Within the commission-bound target and purpose, be **maximally adversarial** about material, decision-relevant failure modes; do not soften a real failure mode because remediation would be hard. Do not retarget or widen beyond the named target.

### 2. Target & source-readiness
Review only the material provided to you. If the target carries a content hash, confirm the provided copy matches it and say so; if you cannot confirm, proceed advisory-only and say so. If any claim depends on a source not provided to you, label it `unverifiable from provided sources` rather than assuming. Treat any pasted authority excerpts as the binding rules the target must conform to.

### 3. Method (order matters)
First do a structured reasoning pass: enumerate the target's load-bearing claims, the boundary/decision criteria, and the likely failure modes — **before** listing any finding. Then produce findings. Reasoning-before-findings is required; it frames what to attack.

### 4. Review checks (be maximally adversarial)
- **Authority / hierarchy conformance:** does the target conflict with the provided authority rules, or violate their precedence?
- **Internal consistency:** self-contradiction; sections that undercut each other.
- **Missing required inputs or unbound roles / intent.**
- **Output-mode / destination / interface correctness.**
- **Downstream executability:** can the named next actor actually act on this from the stated sources?
- **Fitness to goal** (intent-bearing targets): does it achieve its stated goal + success signal? **Attack whether the goal and signal are themselves right** — never treat the fitness reference as a pass-if-matches bar. If no checkable success bar is provided, name `no checkable success bar bound` as a finding rather than inventing one.
- **Overclaims:** readiness, validation, approval, or proof claims unsupported by evidence.
- **Leakage** of out-of-scope or unrelated-project policy into the target.
- **Scope discipline:** does the target do *more* than its stated purpose requires (scope inflation, speculative additions, unrequested scope) — or *less* than required (underfix, symptom-only)? Flag both overreach and underfix against the target's actual purpose.

### 5. Severity meaning
Use `critical` / `major` / `minor` as **finding-priority labels only**. They carry no approval, rejection, readiness, validation, or mandatory-remediation authority.

### 6. Output contract
Lead with a compact `review_summary`, then findings:

    review_summary:
      status: review_complete | blocked
      recommendation: <one line; advisory>
      findings_count: <int>
      blocking_findings: []      # the critical/major ones, one line each
      advisory_findings: []      # minor / optional, one line each
      summary: <one line>

Then list findings, ordered `critical` → `major` → `minor`. For each include: `severity`, `location`, `issue`, `evidence` (cite the target section **and** the conflicting authority excerpt), `impact`, `minimum_closure_condition` (the end state that resolves it — not how to implement), `next_authorized_action` (e.g. owner decision / rerun / re-allocate / no action), and an advisory remediation direction. Do **not** emit executor-ready patch steps. If you find no issues, say so and list residual risks / test gaps.

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

## 5. Return routing

Return your full output in the chat where you received the courier wrapper. The commissioning
CA will courier it back into the home lane for review-return adjudication; the durable report
is written there (destination pre-assigned:
`docs/review-outputs/adversarial-artifact-reviews/demand_projection_f6_r6_revised_design_adversarial_artifact_review_v0.md`).
Nothing you return is kept, applied, or treated as accepted until that adjudication.
