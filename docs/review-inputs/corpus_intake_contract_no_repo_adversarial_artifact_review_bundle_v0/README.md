# Corpus Intake (Standing-Capture) Obligation Contract — No-Repo Adversarial Artifact Review Bundle v0

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: No-repo delegated adversarial ARTIFACT review package for the PROPOSED standing-capture / Corpus Intake obligation contract (PR #112).
use_when:
  - Commissioning the repo-blind cross-vendor advisory artifact review of the corpus-intake contract proposal.
  - Rechecking the exact target attachment and hash supplied to the external controller.
authority_boundary: retrieval_only
branch_or_commit: standing-capture-corpus-intake-contract-v0 @ bf69d3bc
input_hashes:
  target/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md: 2e3d03bb4b6f964700c1a4439bcec752e7bef5676d906c0b117f9f02dfd30ee5
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom no_repo artifact-review pack (target + embedded authority excerpts + portable method)
  edit_permission: read-only for delegate (no_repo, advisory-only); CA patch-only within the single target file after adjudication
  target_scope: the single contract file attached under target/ (see Review Target)
  dirty_state_checked: yes
  blocked_if_missing: target attachment hash mismatch, wrong PR branch, missing portable method, missing authority excerpts
```

Workspace preflight observed by the package assembler (CA):

- assembler workspace: `C:\Users\vmon7\Desktop\projects\orca`
- assembler branch / HEAD: `ecr-sp3-timing-deriver-slice1` @ `0fc58cfe`
- target PR branch / HEAD: `standing-capture-corpus-intake-contract-v0` @ `bf69d3bc` (PR #112)
- base observed: `origin/main` @ `f883b68e`
- dirty-state allowance: unrelated dirty/untracked files exist in the assembler worktree; the review target is generated from the pinned git blob (LF), not from a dirty working copy.

### Portable-method freshness gate (run pre-bundle)

```yaml
freshness_gate:
  method: docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md
  pin1_adversarial_artifact_review_v0.md: MATCH (0cb80057… == live)
  pin2_review-lanes.md: MISMATCH (pinned 7fd702f5… ; live 231d2f6c…)
  pin2_disposition: >
    The only change to review-lanes.md since the pin (commit ff714c30, PR #42) is in its
    "Template Retrieval Binding" section (retiring _generic/ model-target template IDs). That
    section is NOT part of what the portable method distills (reviewer stance, checks, severity
    meaning, output contract, and de-correlation are unchanged). Verified by diff inspection:
    stale PIN, not stale METHOD — the embedded method body remains a faithful distillation.
  owed_followup: >
    A pin-only re-pin (7fd702f5 -> 231d2f6c) is owed to the portable method template by the
    template/prompt-orchestration lane. It is OUTSIDE this commission's bounded scope (the
    target is the corpus-intake contract, not the template) and is flagged, not performed here.
```

## Commission Binding

- overlay_status: `provisional_opt_in` — available only by explicit CA commission; not a bound formal review lane; not machine-routable.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: adversarial ARTIFACT review (non-code doctrine artifact), method `workflow-adversarial-artifact-review` if available in the receiving runtime; otherwise advisory-only via the embedded PORTABLE METHOD.
- access: `no_repo` — the delegate is **advisory-only and must not patch**; it returns findings. The CA (Anthropic/Claude) applies accepted findings within the single target file, and a **bounded same-vendor post-patch recheck is required before keep**.
- mode: base-subagent.
- author_home_model_family: **Anthropic / Claude** (`claude-opus-4.8`), which authored the target.
- controller_model_family: **non-Anthropic vendor** (operator/tooling supplied; the overlay binds no concrete model ID).
- current_receiving_actor_role: controller, once this bundle is handed off.
- dispatch_mode: external-controller-courier.
- de_correlation_status: satisfied (`cross_vendor_discovery`) **only if** the actual controller vendor differs from Anthropic; otherwise record `same_vendor_sanity` or `self_fallback` and do **not** claim cross-vendor discovery / no-new-seam.

No runtime model is recommended, ranked, or selected by this package. The family field is a **who-constraint only**.

## Review Target

- `target/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md`
  - SHA256 (git blob, LF): `2e3d03bb4b6f964700c1a4439bcec752e7bef5676d906c0b117f9f02dfd30ee5`
  - content: the full `PROPOSED_NOT_RATIFIED` standing-capture / Corpus Intake obligation contract (PR #112).

Confirm the attached copy matches this hash before reviewing. If it cannot be confirmed, proceed advisory-only and say so. If hashes cannot be computed, proceed only if the content is still readable, and state the limitation.

## Bounded Scope

Editable scope for any later CA-applied patch: **the single target file only.**

Off-scope, **flag-only** (read-only; do not propose edits to these — they are quoted below only as the authority the target must conform to):

- the v0 commissioned obligation contract (`core_spine_v0_data_capture_spine_obligation_contract_v0.md`);
- the Candidate URL Intake contract; the company-aggregate forward-signal capture-lane scope decision; the pre-capture discovery spine charter recommendation; the buyer-proof packet; the demand-durability indicator framing note (in sibling PR #106);
- all `.agents/workflow-overlay/` files, `AGENTS.md`/`CLAUDE.md`, and every path the Orca safety rules forbid editing.

## Fitness Reference (intent-bearing target — attack the goal too)

This target is intent-bearing: its correctness is fitness to an upstream goal, not internal consistency alone.

- **Goal:** be the standing-capture obligation home the v0 contract routes to (owner selection **D1 = general**, serving BOTH the demand-durability indicators and the company-aggregate org-motion lane; **D3 = scheduler deferred**), preserving the rebind rule + append-only + never-a-feed + manipulability flags + minimization, **without** re-spec'ing the lanes it serves and **without** becoming a sold feed or an owner-rejected "standing registry."
- **Success signals (pointers, quoted in Authority Excerpts):** the v0 contract's standing-capture carve-out + rebind rule; the buyer-proof never-a-feed invariant; the company-aggregate slice clarification + its `stale_if` (this contract supersedes it as obligation home); the pre-capture discovery charter's standing-registry / promote-on-reuse caution.
- **Required posture:** the fitness reference is an **added axis you must also attack** — ask whether the goal and these signals are themselves right. It is **never** a pass-if-matches bar. If you judge no checkable success bar is bound, name `no checkable success bar bound` as a finding.

## Highest-Value Checks (be maximally adversarial; not exhaustive)

1. **Sibling vs amendment.** Is "separate sibling contract, not a v0 amendment" (D2) actually coherent — or does the proposal smuggle in changes that effectively amend v0's obligations or its standing-capture carve-out?
2. **Rebind gate (S5).** Is the exit from standing-corpus to ECR evidence airtight, or is there a path where a standing row is treated as evidence without recapture/rebind under a Decision Frame?
3. **Never-a-feed lock (S7).** Does S7 genuinely prevent the corpus from becoming a sold feed/monitoring product, or is the line between "decision-substrate" and "feed" stated but not enforceable by the obligations?
4. **INV-1 / flag-don't-conclude (S6).** Does anything in S2–S7 (cadence, series identity, manipulability flags, append-only diff) introduce a weight, score, ranking, threshold, or judgment — i.e. violate INV-1 by stealth?
5. **Charter gate (S1) vs free-floating collection.** Does S1 actually replace v0's Ob.1 commissioning gate with a real anti-free-floating boundary, or is "Standing Capture Charter" an unbounded license?
6. **Standing-registry deconfliction.** Is the "promote-on-reuse, not ahead of reuse" / "obligation contract, not a data home" argument sound, or does this contract in fact charter the owner-rejected standing knowledge-home?
7. **Layer collision.** Does the contract stay strictly above Candidate URL Intake (locators) and below v0's rebind, or does it overlap/contradict either layer?
8. **Scope discipline.** Does the proposal do MORE than its purpose requires (scope inflation, speculative obligations) or LESS (underfix — a guardrail the goal needs but the contract omits)? Check both against the Smallest Complete Intervention rule.
9. **Inheritance honesty.** Is "inherits v0 obligations 2–16 unchanged" true, or does a standing delta silently relax an inherited obligation (e.g. minimization, boundary compliance, archive posture)?
10. **Proposal-status honesty.** Does the artifact correctly claim nothing beyond `PROPOSED_NOT_RATIFIED` (no validation/readiness/propagation/build), and is the `proposed_direction_change` block honest that nothing is propagated?

---

## Authority Excerpts (the rules the target must conform to — repo-blind reviewer, read these as binding)

### A. Orca Agent Behavior Kernel + Smallest Complete Intervention (`AGENTS.md`)

> Surface ambiguity or risky assumptions before acting. Default to the **smallest complete intervention**: solve the actual request completely with the narrowest sufficient scope. Every changed line must trace to the user request or required validation. Preserve real failure visibility; never create fake success paths. **Absence and build-state are claims, not defaults** — confirm load-bearing, cheaply-checkable claims against the primary source.
>
> `Complete` is load-bearing (do not underfix to minimize diff). `Smallest` is load-bearing (no unrelated cleanup, speculative abstractions, broad rewrites, or nice-to-haves). When two complete paths both satisfy the request, prefer **materially lower downstream lock-in**; take a higher-lock-in path only when a benefit necessary to the request outweighs it, and then **pause and surface the tradeoff** first.

### B. v0 commissioned obligation contract — standing-capture carve-out (the routing the target answers)

> Standing or opportunistic corpus capture is **out of scope** for Data Capture Spine v0. If Orca later collects public signals before a Decision Frame exists, that should be handled by **a separate Candidate Signal Intake or Corpus Intake contract**. Those items are **not ECR-ready evidence until rebound or recaptured under a Decision Frame**.

> (Ob.1 Commissioning Gate) standing or opportunistic capture is rejected or routed outside this contract. (Ob.15) re-observations supplement; re-capture does not erase prior capture history. (Rejected patterns) standing/opportunistic corpus capture inside this v0 contract; **paper contract hardening before real signal pressure tests**; runtime design as this contract. (Forbidden Capture outputs) credibility/integrity labels, exclusion, Signal-Use Classification, Decision Strength, Action Ceiling, source-quality scores, runtime plans.

### C. Buyer-proof never-a-feed invariant

> **Never-a-feed invariant:** every output is a calibrated decision with an action ceiling — **never a feed or stream**. This is the structural lock that keeps Orca off the "monitoring-only pull" kill and out of the social-listening category, including when a read is monitored over time: recurring engagement is sold as recurring **decisions**, never as a monitoring feed.

> (Kill signals) Buyer wants only generic research, source volume, dashboard access, **trend feeds, or a market-monitoring feed**; the strongest buyer ask is generic market monitoring, not allocation-risk reduction.

### D. INV-1 (Demand-Substrate no-scoring invariant)

Capture (commissioned or standing) introduces **no weight, score, ranking, threshold, or judgment**. It records visible facts and flags; whether a signal is decision-useful is a downstream Judgment call, never a capture call.

### E. Company-aggregate forward-signal slice clarification (the lane this supersedes as obligation home)

> The company-aggregate forward series is **standing / corpus capture**… It runs under the **existing v0 capture obligations** (minimization, boundary compliance, capture-event provenance, decomposed timing, archive/visibility posture, failure visibility). **Rebind rule:** a standing observation row is **not ECR-ready evidence** until rebound or re-captured under a Decision Frame. **Retention:** append-only; re-observations supplement, never overwrite. **Narrow to this slice.** It does **not** write the general Candidate Signal Intake / Corpus Intake contract the v0 contract points to (a future general contract may supersede this).

> Its `stale_if`: "A standing / corpus-capture obligation contract is accepted, giving this slice its obligation home."

### F. Candidate URL Intake contract — the layer BELOW (do not overlap)

> A candidate locator is **not** source material, a Source Capture Packet, a capture unit, Data Capture handoff input, or ECR-ready evidence. A candidate locator can become eligible for capture **only through a separate promotion gate**… recording that one locator has been selected **for a later authorized capture path**. Hard stop: if a lane must **fetch source bodies, preserve rendered pages, invoke a runner**, rank source quality, or hand off to Data Capture, it is **no longer Candidate URL Intake**.

### G. Pre-capture discovery spine charter recommendation — standing-registry caution

> Recommendation: `DO_NOT_BUILD` a new pre-capture discovery spine/lane now. A new product lane is "the same genus as the **owner-rejected standing registry** (a standing knowledge-home created ahead of proven reuse); it bypasses the **promote-on-reuse trigger** the owner adopted." (This is WHERE-side venue discovery; the target is capture-side standing capture of approved series — the reviewer should test whether the target's deconfliction of this is sound.)

---

## PORTABLE METHOD (component c) — paste from here to the end marker

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

---

## Output Contract (return to the commissioning CA)

Return findings in chat to the CA. Include:

- `reviewed_by`: your actual model and version if known; otherwise `unrecorded`.
- `authored_by`: `claude-opus-4.8` (Anthropic/Claude authored the target).
- `de_correlation_bar`: `cross_vendor_discovery` (if your vendor ≠ Anthropic), else `same_vendor_sanity` or `self_fallback`.
- `source_context_status`: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- `review_lane_status`: if your runtime can use `workflow-adversarial-artifact-review`, reference-load it first and say so; if not, state `workflow-adversarial-artifact-review unavailable; advisory_no_skill_fallback` and do not claim a formal lane ran.
- attachment hash confirmation status for the target.
- the `review_summary` YAML, then findings ordered `critical` → `major` → `minor`, each with location, evidence (target section + conflicting authority excerpt), impact, `minimum_closure_condition`, `next_authorized_action`, advisory remediation direction.
- explicit off-scope flags, if any.
- residual risk and not-proven boundaries.

Use `NEEDS_ARCHITECTURE_PASS` if the problem is design-level rather than patch-level; if you use it, stop at findings and propose no patch.

## Non-Claims

This package is not validation, readiness, formal `PASS`, proof that the review ran, a no-new-seam claim, patch authorization for the external controller, or a runtime model recommendation. In `no_repo` mode the controller returns **findings only**; the CA applies any accepted change within the single target file, and a **bounded same-vendor post-patch recheck is required before keep**. The contract under review is itself `PROPOSED_NOT_RATIFIED`; this review is one input to the owner's ratification decision, not the decision.
