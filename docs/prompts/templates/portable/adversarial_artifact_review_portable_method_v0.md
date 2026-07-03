# Portable Adversarial Artifact Review Method v0 (model-agnostic, self-contained)

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: >
  Self-contained, model-agnostic adversarial artifact review METHOD only for no_repo
  reviewers without repository, skill, or overlay access. Bundle the PORTABLE METHOD
  block below as component (c) of an explicit no_repo adversarial review package,
  alongside the review target and the authority excerpts it must conform to.
use_when:
  - Commissioning an explicit no_repo adversarial review of a non-code artifact because the reviewer cannot inspect the repository/worktree or invoke Orca skills/overlay.
  - Any reviewer lacking repository, Orca skill, or overlay access must follow the embedded method instead of "invoking" a skill.
  - Cross-family, external, couriered, paste-ready, or portable delivery by itself does not select this method; use repo-bound review when repository access exists.
authority_boundary: retrieval_only
derived_from:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md@c5c4e7d3913b59d60c592c86255abbafd82336910b90656e6bafcac57a33e9c4   # re-derived 2026-07-02: 1b0d60b5 added the source-read budget + closing read-budget audit to the template's output contract -- material; PORTABLE METHOD section 6 gains the provided-materials read-budget audit line. (Prior pin 0cb80057…b60c3fc.)
  - .agents/workflow-overlay/review-lanes.md@ddc3e03b9ea995783e1d29100d502b025119460ae158bbb9e79f960e4729750d   # re-pinned 2026-07-02: 73f41506 (delegated_code_review_and_patch lane-index wording) + 82613874 (routine-read-shape head note) -- both confined to lane bindings/read-shape guidance, NOT the distilled reviewer stance/checks, so pin-only. (2026-06-14: #42 Template Retrieval Binding, pin-only; 2026-06-10: two-bar de-correlation / provenance machinery, pin-only; 2026-06-09: reviewed_by/authored_by bullets, pin-only. Prior pin 231d2f6c…abef51.)
# Hash convention (recorded 2026-06-13 after an observed false-stale on a CRLF checkout): the
# derived_from pins are SHA256 over git BLOB bytes (LF as stored; e.g. `git cat-file blob <rev>:<path>`),
# NOT over CRLF working-tree bytes. Run the freshness gate like-for-like: a Get-FileHash mismatch on a
# CRLF working tree is not staleness by itself. Verified 2026-06-14: both pins match origin/main @ 4947b2c
# blob bytes (pin 1 unchanged; pin 2 re-pinned this date for #42, above).
method_version: v0
stale_if:
  - Either derived_from source hash changes. Freshness gate = hash-compare these pins against the live files before assembling any package; on mismatch, re-derive this method rather than shipping it.
model_neutrality: Method/posture only. It never names, recommends, ranks, or routes a runtime model. The cross-family property is satisfied by the operator's model choice, not by this file.
```

> **How to use:** deliver the delimited PORTABLE METHOD block only to an explicit no_repo reviewer -- **pasted in chat, or shipped as the bundle `README`** (the no_repo package shape is bound in `.agents/workflow-overlay/delegated-review-patch.md`) -- together with the review target and the authority excerpts it must conform to -- **always including the authoring environment's foundational behavior + scope-discipline doctrine** (for Orca: the `AGENTS.md` kernel, which carries the *Smallest Complete Intervention* rule), since conformance to it is part of the review. If the reviewer can inspect the repository or worktree, route to the repo-bound review path instead of this portable method.

---

## PORTABLE METHOD — paste from here to the end marker

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

Close with a one-line read-budget audit over the provided materials: which provided files you read in full versus skipped or skimmed, and why. It records coverage of the provided bundle; it is not a validation, readiness, or coverage claim.

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

---

*Provenance: this method is a faithful, flattened distillation of the `derived_from` sources (the Orca adversarial-artifact-review template + the Review Doctrine in `review-lanes.md`), made self-contained for reviewers without skill/overlay/repo access. The orca header and this footer are repository metadata; only the delimited PORTABLE METHOD block is shipped to the reviewer. Re-derive when a `derived_from` hash changes.*
