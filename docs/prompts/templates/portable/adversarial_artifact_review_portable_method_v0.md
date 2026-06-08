# Portable Adversarial Artifact Review Method v0 (model-agnostic, self-contained)

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: >
  Self-contained, model-agnostic adversarial artifact review METHOD for repo-agnostic /
  cross-family reviewers that cannot invoke Orca review skills or read the overlay. Bundle the
  PORTABLE METHOD block below as component (c) of any no-repo cross-family review package,
  alongside the review target and the authority excerpts it must conform to.
use_when:
  - Commissioning a cross-family / external / no-repo adversarial review of a non-code artifact.
  - Any reviewer lacking Orca skill/overlay access must follow the embedded method instead of "invoking" a skill.
authority_boundary: retrieval_only
derived_from:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md@0cb80057795215b3311d00c3d0ad603fbef78fe92e5ae24d8042490b8b60c3fc
  - .agents/workflow-overlay/review-lanes.md@b8569fb5edd62d5cc85e265658317e8e30fd8fd04ed244872912a5d7057f6884   # re-pinned 2026-06-09: reviewed_by/authored_by provenance bullets added to Review Doctrine; those fields are CA-recorded on ingest (not part of this reviewer method), so the distilled stance/checks are unchanged and this is pin-only
method_version: v0
stale_if:
  - Either derived_from source hash changes. Freshness gate = hash-compare these pins against the live files before assembling any package; on mismatch, re-derive this method rather than shipping it.
model_neutrality: Method/posture only. It never names, recommends, ranks, or routes a runtime model. The cross-family property is satisfied by the operator's model choice, not by this file.
```

> **How to use:** paste the delimited PORTABLE METHOD block below to the reviewer, together with the review target and the authority excerpts it must conform to — **always including the authoring environment's foundational behavior + scope-discipline doctrine** (for Orca: the `AGENTS.md` kernel, which carries the *Smallest Complete Intervention* rule), since conformance to it is part of the review. The reviewer needs nothing else — no repo, no skills, no overlay.

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

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

---

*Provenance: this method is a faithful, flattened distillation of the `derived_from` sources (the Orca adversarial-artifact-review template + the Review Doctrine in `review-lanes.md`), made self-contained for reviewers without skill/overlay/repo access. The orca header and this footer are repository metadata; only the delimited PORTABLE METHOD block is shipped to the reviewer. Re-derive when a `derived_from` hash changes.*
