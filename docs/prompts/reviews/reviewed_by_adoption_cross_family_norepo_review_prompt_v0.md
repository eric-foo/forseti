---
retrieval_header_version: 1
artifact_role: Review prompt (advisory no_repo cross-family adversarial artifact review commission)
scope: >
  Paste-ready, self-contained no_repo commission for a cross-family (non-Claude) ADVISORY adversarial
  review of the reviewed_by adoption draft v1. The reviewer has no repo/skills, follows the embedded
  portable method, and returns findings only (no patch); the commissioning home model (CA) adjudicates
  and applies, with a separate de-correlated post-patch re-review before keep.
use_when:
  - Running the cross-family de-correlated review of the reviewed_by adoption before keep.
  - Re-deriving / re-pinning this commission if the target or pinned sources change.
authority_boundary: retrieval_only
input_hashes:
  docs/_inbox/reviewed_by_adoption_draft_v1.md: 29e2b7bdb6c09b4e8daeba4daa24cde2008e41e92a6d21c0c073e4a20c8f88e5
  .agents/workflow-overlay/review-lanes.md: c3f37fb2e02b9ca6dee55e685c9913035a9cca050acff7954294e5e2a417df72
  docs/prompts/templates/review/adversarial_artifact_review_v0.md: 0cb80057795215b3311d00c3d0ad603fbef78fe92e5ae24d8042490b8b60c3fc
  docs/_inbox/reviewed_by_adoption_norepo_review_bundle_v0.zip: 8863377c97989d3c3fe3ea6e4adf26cd412804bf06e7a865fbff3311cc2a5dc1
branch_or_commit: ecr-sp3-timing-deriver-slice1
stale_if:
  - The target draft v1 changes (sha differs) — re-embed/re-point and re-pin.
  - Either portable-method derived_from pin changes — re-run the freshness gate before reuse.
---

# Cross-Family No_Repo Advisory Review Commission — `reviewed_by` adoption (draft v1)

**ADVISORY, non-bound commission.** Not a bound Orca review lane, not validation, not readiness, not a kept change. It produces advisory findings for the commissioning home model (CA) to adjudicate.

## How to run (operator)
1. Run on a model from a **different family than the author**. Author/home family = **Claude (Opus-class)**, so use a **non-Claude** family (e.g. a GPT- or Gemini-class model). This is a de-correlation **who-constraint**, not a claim that any model is "better."
2. **Attach/provide the source bundle** `docs/_inbox/reviewed_by_adoption_norepo_review_bundle_v0.zip` (sha256 `8863377c97989d3c3fe3ea6e4adf26cd412804bf06e7a865fbff3311cc2a5dc1`) to that model, or paste the files it contains. It holds the review TARGET (`reviewed_by_adoption_draft_v1.md`) **and** every source file the proposed edits touch or cite, plus `MANIFEST_sha256.txt` for byte-confirmation. The reviewer needs these to verify the edits, not just the target's prose.
3. Paste everything from `===== COMMISSION BEGIN =====` to `===== COMMISSION END =====` into that model, alongside the bundle.
4. Bring the model's findings back to the CA (home model) for adjudication. The reviewer does **not** patch; the CA applies, then a separate de-correlated post-patch re-review runs before anything is kept.

## Freshness gate (assembler-run; result recorded)
- `review-lanes.md`: live sha256 `c3f37fb2…df72` = pin → **MATCH**.
- `adversarial_artifact_review_v0.md`: live sha256 `0cb80057…c3fc` = pin → **MATCH**.
- → Portable method is **FRESH**; shipped as-is. No re-derivation.

## Source bundle (provide to the reviewer)
`docs/_inbox/reviewed_by_adoption_norepo_review_bundle_v0.zip` — sha256 `8863377c97989d3c3fe3ea6e4adf26cd412804bf06e7a865fbff3311cc2a5dc1`. Per its `MANIFEST_sha256.txt`, it contains:
- `reviewed_by_adoption_draft_v1.md` — the review TARGET.
- The 4 files the edits change: `review-lanes.md`, `prompt-orchestration.md`, `communication-style.md`, `validation-gates.md`.
- The files the "intentionally not changed" / template / pin claims cite: `retrieval-metadata.md`, `delegated-review-patch.md`, the review template, the portable method, and `AGENTS.md` (full kernel).
The reviewer must read these to verify the proposed edits (anchors exist and are worded as assumed, inserted text conforms, the 4-file binding is complete, the gate-duplication question). Without a needed file, label the check `unverifiable from provided sources`.

## Actor / model-family receipt
```yaml
actor_model_family_receipt:
  author_home_model_family: claude (opus-class)
  controller_model_family: <the non-Claude family you run this on — REQUIRED to differ from author>
  current_receiving_actor_role: controller
  access: no_repo            # no repo, no patch, findings only
  de_correlation_status: satisfied_when_run_on_non_claude_family   # else blocked
```

===== COMMISSION BEGIN =====

You are performing a READ-ONLY, ADVISORY adversarial artifact review. You have NO repository access and NO project skills — follow the PORTABLE METHOD below exactly. Be maximally adversarial about material, decision-relevant failure modes within the named target and purpose. Do NOT propose executor-ready patches; return findings only, as decision input for the commissioning owner.

## TARGET (review this)
The review target is `reviewed_by_adoption_draft_v1.md` in the attached bundle (sha256 `29e2b7bdb6c09b4e8daeba4daa24cde2008e41e92a6d21c0c073e4a20c8f88e5`). It proposes edits to live overlay files that are **included in the bundle**. **Verify those edits against the ACTUAL bundled files** — confirm each insertion anchor exists and is worded as the draft assumes, that the inserted text conforms to the authority rules, that the 4-file binding is complete and non-orphaning, and whether the Gate-11-vs-validation-gates duplication is a real hazard. Do not assess the target's self-description in isolation. If a file a claim depends on is absent from the bundle, label that check `unverifiable from provided sources`.

## AUTHORITY EXCERPTS (the binding rules the target must conform to)
The target proposes changes to a governance overlay. Conformance to the authoring environment's behavior kernel — **especially the Smallest Complete Intervention rule** — is part of your review.

--- AGENTS.md · Agent Behavior Kernel (verbatim) ---
Surface ambiguity or risky assumptions before acting.
Default to the smallest complete intervention: solve the actual request completely with the narrowest sufficient scope.
Every changed line must trace to the user request or required validation.
Preserve real failure visibility; never create fake success paths.
For non-trivial changes, define and run relevant verification or state why it was not run.
Before reporting work as committed, written, pushed, or otherwise persisted, verify the durable target with a fresh read and show the verifying read's actual output for that lifecycle claim. Report only observed facts: never state a SHA, count, status, write, or check you did not observe. If verification fails, report the mismatch and stop.

--- AGENTS.md · Smallest Complete Intervention (verbatim) ---
`Complete` is load-bearing. Do not underfix to minimize diff, ceremony, or visible change; a slightly larger fix is correct when required for durable, coherent, non-fragile completion.
`Smallest` is also load-bearing. Do not add unrelated cleanup, speculative abstractions, broad rewrites, extra workflow ceremony, or nice-to-have improvements.
When two candidate paths both satisfy the current request, prefer the one with materially lower downstream lock-in (the durable data, schema, interface, or workflow shape that would be irreversible or costly to roll back). Take the higher-lock-in path only when a benefit necessary to the current request outweighs that structural cost.

--- review-lanes.md · model-neutrality rule (verbatim) ---
Review lane routing must never recommend, prescribe, rank, or imply runtime model choice. Review lanes may bind review type, method/skill, target, authority, output mode, destination, and prompt-template target. Runtime model choice is outside Orca review-lane authority and remains an operator/tooling decision.

(The target's central claim is that `reviewed_by` is an observed RECORD of who reviewed, NOT model routing/selection/ranking. Test that claim hard against this rule everywhere the field appears — doctrine bullet, prompt default, validation gate, courier field.)

## PORTABLE METHOD — follow this exactly

### 1. Your stance
You are performing a read-only, advisory-only adversarial artifact review. The formal review tooling used inside the authoring environment is not available to you — state that explicitly in your output, because it bounds your result to advisory critique, not a formal verdict. Within the commission-bound target and purpose, be maximally adversarial about material, decision-relevant failure modes; do not soften a real failure mode because remediation would be hard. Do not retarget or widen beyond the named target.

### 2. Target & source-readiness
Review only the material provided to you. If the target carries a content hash, confirm the provided copy matches it and say so; if you cannot confirm, proceed advisory-only and say so. If any claim depends on a source not provided to you, label it `unverifiable from provided sources` rather than assuming. Treat any pasted authority excerpts as the binding rules the target must conform to.

### 3. Method (order matters)
First do a structured reasoning pass: enumerate the target's load-bearing claims, the boundary/decision criteria, and the likely failure modes — before listing any finding. Then produce findings. Reasoning-before-findings is required; it frames what to attack.

### 4. Review checks (be maximally adversarial)
- Authority / hierarchy conformance: does the target conflict with the provided authority rules, or violate their precedence?
- Internal consistency: self-contradiction; sections that undercut each other.
- Missing required inputs or unbound roles / intent.
- Output-mode / destination / interface correctness.
- Downstream executability: can the named next actor actually act on this from the stated sources?
- Fitness to goal: does it achieve its stated goal + success signal? Attack whether the goal and signal are themselves right — never treat the fitness reference as a pass-if-matches bar. If no checkable success bar is provided, name `no checkable success bar bound` as a finding rather than inventing one.
- Overclaims: readiness, validation, approval, or proof claims unsupported by evidence.
- Leakage of out-of-scope or unrelated-project policy into the target.
- Scope discipline: does the target do more than its stated purpose requires (scope inflation, speculative additions) — or less than required (underfix, symptom-only)? Flag both overreach and underfix against the target's actual purpose.

### 5. Severity meaning
Use `critical` / `major` / `minor` as finding-priority labels only. They carry no approval, rejection, readiness, validation, or mandatory-remediation authority.

### 6. Output contract
Lead with a compact `review_summary`, then findings:

    review_summary:
      status: review_complete | blocked
      recommendation: <one line; advisory>
      findings_count: <int>
      blocking_findings: []      # the critical/major ones, one line each
      advisory_findings: []      # minor / optional, one line each
      summary: <one line>

Then list findings, ordered `critical` → `major` → `minor`. For each include: `severity`, `location`, `issue`, `evidence` (cite the target section AND the conflicting authority excerpt), `impact`, `minimum_closure_condition` (the end state that resolves it — not how to implement), `next_authorized_action` (e.g. owner decision / rerun / re-allocate / no action), and an advisory remediation direction. Do NOT emit executor-ready patch steps. If you find no issues, say so and list residual risks / test gaps.

### 7. Review-use boundary
Your findings are decision input only for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## COMMISSION-SPECIFIC CHARGES (attack these especially — this is the goal-fitness / realism pass)
A prior same-family pass already cleared the objective layer (conformance wording, insertion anchors, vocabulary, scope). Spend your effort on judgment the prior pass deliberately did NOT touch:

1. **Realism of the measurement goal (headline).** The field is operator/tooling-supplied. If real tooling does not populate it, every output reads `unrecorded` and the stated purpose ("measurable rather than assumed") never materializes — pure ceremony. Is that risk acknowledged and acceptable? Should adoption be gated on a tooling-population commitment?
2. **Does the instrument actually enable the stated measurement?** The goal is *same-family vs cross-family coverage*. The target records the **reviewer** model (`reviewed_by`) but NOT the **author/artifact** model. Can same-vs-cross actually be computed from `reviewed_by` alone, or does the goal silently require author attribution too (which the target does not add)? If so, is the success signal honest?
3. **Is "model + version" the right grain** (vs family, vs a structured {family, role} record)? Consider downstream lock-in of the chosen grain under the Smallest Complete Intervention rule.
4. **Model-neutrality (re-attack):** does recording a concrete model id leak into prescription/ranking/selection anywhere it appears, despite the disclaimers?
5. **Single-source vs duplicate:** the draft adds the field to BOTH `prompt-orchestration` Gate 11 and the `validation-gates` Review-doctrine gate, while noting that gate already omits the fitness-reference item (a single-source precedent). Is the duplication a maintenance hazard, or is closing the enforcement gap worth it?
6. **Completeness / scope:** is the 4-file binding complete and non-orphaning, and does the draft add anything beyond the field + its non-fragile binding?

## OUTPUT CONTRACT (for this commission)
Return the portable method's `review_summary` then the ordered findings. Advisory only; no patch; no formal verdict. State explicitly that formal review tooling was unavailable to you. These findings are decision input for the CA, who will adjudicate, apply accepted changes, and run a separate de-correlated post-patch re-review before anything is kept.

===== COMMISSION END =====
