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
  - Commissioning an explicit no_repo adversarial review of a non-code artifact because the reviewer cannot inspect the repository/worktree or invoke Forseti skills/overlay.
  - Any reviewer lacking repository, Forseti skill, or overlay access must follow the embedded method instead of "invoking" a skill.
  - Cross-family, external, couriered, paste-ready, or portable delivery by itself does not select this method; use repo-bound review when repository access exists.
authority_boundary: retrieval_only
derived_from:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md@b6ab8b234dce59473790af8a56cc2f2d4c50fa809d01e905b63b82fc49e40d6c   # re-derived 2026-07-16: deep-thinking single-owner + review-internalized framing -- the template now defines the framing pass in-lane (no separate workflow-deep-thinking load for review commissions); non-material to the PORTABLE METHOD body, whose section 3 already embeds reasoning-before-findings with no skill reference. Also absorbs the shared-contract path rename (#784). (Prior pin afc441cf…c2ba9f, 2026-07-04: coverage-first find stage.)
  - .agents/workflow-overlay/review-lanes.md@23518fe43d5fee0118f199ed8f475f226788ea4aabaa1ec710f75a9921b20e0a   # re-pinned 2026-07-16 (second pass, post-PR-984): the deep-thinking trigger bullet became a pointer to prompt-orchestration.md's Review Prompt Defaults with review-internalized framing -- prompt-side sequencing, non-material to the distilled no_repo method body (same class as the prior re-pin's "deep-thinking trigger wording" delta). (Prior pins: 2030e3f2…7a59 earlier 2026-07-16; 99b9e071…f9315, 2026-07-04: coverage-first Review Doctrine.)
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

> **How to use:** deliver the delimited PORTABLE METHOD block only to an explicit no_repo reviewer -- **pasted in chat, or shipped as the bundle `README`** (the no_repo package shape is bound in `.agents/workflow-overlay/delegated-review-patch.md`) -- together with the review target and the authority excerpts it must conform to -- **always including the authoring environment's foundational behavior + scope-discipline doctrine** (for Forseti: the `AGENTS.md` kernel, which carries the *Smallest Complete Intervention* rule), since conformance to it is part of the review. If the reviewer can inspect the repository or worktree, route to the repo-bound review path instead of this portable method.

---

## PORTABLE METHOD — paste from here to the end marker

### 1. Your stance
You are performing a **read-only, advisory-only adversarial artifact review**. The formal review tooling used inside the authoring environment is **not available to you** — state that explicitly in your output, because it bounds your result to advisory critique, not a formal verdict. Within the commission-bound target and purpose, be **maximally adversarial and coverage-first**: report every issue you find, including uncertain and low-severity ones. Do not filter for importance or confidence at this stage — the commissioning owner's adjudication ranks and filters. Materiality, severity, and confidence are labels you attach, never thresholds for reporting; do not soften or drop a real failure mode because remediation would be hard, confidence is low, or the finding seems minor. Do not retarget or widen beyond the named target.

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

### 5. Severity and confidence meaning
Use `critical` / `major` / `minor` as **finding-priority labels only**. Also label each finding with `confidence` (`high` / `medium` / `low`) — your own certainty the finding is real. Neither label carries approval, rejection, readiness, validation, or mandatory-remediation authority, and neither is a threshold for reporting.

### 6. Output contract
Lead with a compact `review_summary`, then findings:

    review_summary:
      status: review_complete | blocked
      recommendation: <one line; advisory>
      findings_count: <int>
      blocking_findings: []      # the critical/major ones, one line each
      advisory_findings: []      # minor / optional, one line each
      summary: <one line>

Then list findings, ordered `critical` → `major` → `minor`. For each include: `severity`, `confidence` (high / medium / low), `location`, `issue`, `evidence` (cite the target section **and** the conflicting authority excerpt), `impact`, `minimum_closure_condition` (the end state that resolves it — not how to implement), `next_authorized_action` (e.g. owner decision / rerun / re-allocate / no action), and an advisory remediation direction. Low-confidence or minor findings may use a compact one-line form: `severity | confidence | location | issue | advisory direction` — compactness lowers reporting cost, not the finding's standing as decision input. Do **not** emit executor-ready patch steps.

After the findings, add a `considered_and_defended` section: one line per candidate finding you defeated with a steelman defense (candidate plus the defense that held). These are not findings and carry no severity, closure, or action fields; they make your discard pile visible to the commissioning owner. If none, write `considered_and_defended: none`. If you find no issues, say so and list residual risks / test gaps.

Close with a one-line read-budget audit over the provided materials: which provided files you read in full versus skipped or skimmed, and why. It records coverage of the provided bundle; it is not a validation, readiness, or coverage claim.

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

---

*Provenance: this method is a faithful, flattened distillation of the `derived_from` sources (the Forseti adversarial-artifact-review template + the Review Doctrine in `review-lanes.md`), made self-contained for reviewers without skill/overlay/repo access. The repository header and this footer are repository metadata; only the delimited PORTABLE METHOD block is shipped to the reviewer. Re-derive when a `derived_from` hash changes.*
