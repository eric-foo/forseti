# no_repo Adversarial Artifact Review Bundle — Share-of-Voice Field Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review input artifact (Review prompt role binding, docs/review-inputs/)
scope: >
  Self-contained no_repo review package for the de-correlated cross-vendor
  adversarial artifact review of
  core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md.
  The repo-blind reviewer needs ONLY the files in this bundle.
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
| `core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md` | REVIEW TARGET (verbatim attachment) | `33C7F793AB049A9EE3655A7194FF39B8E3B83307D8B1C63E1A3D97FB24792F4B` |
| `README.md` (this file) | Method + authority + commission | (pinned in the courier wrapper) |

If you can compute SHA256, confirm the target matches its pin and say so; if you
cannot, proceed advisory-only and say so. If you cannot read the attached files
at all, reply only `BLOCKED_BUNDLE_UNREADABLE`.

**Freshness gate (assembler-run, 2026-07-02): PASS.** The portable method below
was re-derived earlier this same day (both `derived_from` pins verified against
live sources at re-derivation); no source change since.

## 2. Commission (no_repo Delegated Review, advisory-only)

```md
# Delegated Review Commission — no_repo access mode

## Lane Binding
- overlay_status: provisional_opt_in (single-use commission carried from the
  fused turn's Review Timing Advisory; not a bound review lane; no strict claims)
- operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md (no_repo mode)
- review_lane: artifact — executed via the PORTABLE METHOD in §4
  (registry id portable-adversarial-artifact-review-method); ADVISORY FINDINGS only
- mode: base-subagent shape, access: no_repo (external reviewer lane has no
  repository access; content identity travels by hash pin) — findings, not a diff
- actor_model_family_receipt:
  - author_home_model_family: Anthropic (Claude; authored by claude-fable-5)
  - controller_model_family: operator-dispatched; MUST be a different vendor /
    model lineage than Anthropic; unknown/undisclosed lineage cannot satisfy
    the cross-vendor discovery bar
  - current_receiving_actor_role: controller (you)
  - dispatch_mode: external-controller-courier
  - de_correlation_status: gated in the wrapper — self-check before reviewing
- de_correlation: who-constraint, never a model recommendation or ranking

## Target
- target: core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
  (single named artifact; whole file)
- what it is: the field-level contract every future share-of-voice computation
  or view over the data lake must conform to — readout identity, grouping,
  numerator/denominator/coverage fields, window basis, posture semantics, and
  forbidden fields. It gates the family's first buyer-facing view build.
- why_ordinary_same-family_review_is_insufficient: authored and adjudicated by
  the same model family that wrote the seam contract it binds under; the field
  semantics (zero handling, denominators, coverage) are exactly where an
  author's blind spot would produce a dishonest-but-plausible readout.
- bounded_patch_scope: NONE for you (no_repo). Accepted amendments are applied
  by the home CA after adjudication, then take the bounded same-vendor
  mechanical-tier post-patch recheck before keep.
- off_scope: everything beyond the attached files; label repo-settleable claims
  `unverifiable from provided sources`.

## Controller Output Contract
- PORTABLE METHOD (§4) exactly: reasoning pass first; findings ordered
  critical → major → minor with severity / location / issue / evidence /
  impact / minimum_closure_condition / next_authorized_action / advisory
  remediation direction; close with the one-line read-budget audit
- citations neutral in tone, decision-sufficient in substance (target sections
  + §3 authority excerpts)
- escalation: NEEDS_ARCHITECTURE_PASS for design-level problems; findings only
- no executor-ready steps; no validation/readiness/approval claims

## Adjudication Contract (for your awareness)
- findings are claims the home CA adjudicates (accept/modify/reject); CA-applied
  amendments take a bounded same-vendor recheck before keep; durable report
  written at ingestion under docs/review-outputs/adversarial-artifact-reviews/;
  state your model identity and version if known and permitted
```

## 3. Authority excerpts the target must conform to

**Silver Vault metric posture rules (binding):**
> metric_posture.kind must be one of ("observed", "unavailable_with_reason",
> "not_attempted"). An observed metric requires a metric_value and no posture
> reason; a non-observed metric must not carry a metric_value and requires a
> reason. metric_value = 0 is valid only as a real observed zero from the
> source. Never means missing.

**Consumption seam contract, On-Demand-First Metrics Policy (binding):**
> A metric family may be precomputed ONLY as a rebuildable, manifest-backed,
> non-authoritative view under indexes/derived_retrieval/. Metric views must
> expose posture and coverage fields so no reader can treat missing evidence
> as zero. Field-level gate: the owning decision for a named family must first
> bind that family's field-level posture, reason, and coverage contract.
> First families (owner-named 2026-07-02): source_backed_brand_line_share_of_voice
> (per platform, cohort, and coverage window, the share of captured
> product-line mentions per brand/line, derived from source-backed-complete
> silver__cleaning__product_mentions records; denominators are
> captured-evidence-only) and movement_threshold_crossings.

**Lake boundaries (binding):** the lake never cleans/normalizes (grouping
normalization is Cleaning's); per-platform only — no cross-platform person
identity; object-level, never person dossiers; what was not captured cannot be
derived — coverage limits travel with outputs.

**Committed evidence available to this family (facts):** mention records carry
brand (may be literal "unknown"), line, stance/confidence, source pointers, and
source-backed lineage refs; every packet records capture_time; publication time
exists only where the source surface captured it (e.g. YouTube publish date in
preserved metadata).

**Authoring environment's scope doctrine — AGENTS.md (Orca), verbatim:**
> Default to the smallest complete intervention: solve the actual request
> completely with the narrowest sufficient scope.
> Preserve real failure visibility; never create fake success paths.

**Fitness reference (attack it too):** a share-of-voice readout is honest only
if a brand-side buyer can see exactly which captured evidence stands behind
each share, missing evidence can never read as zero or shrink a denominator
silently, and nothing in the field schema can drift into market-total,
cross-platform, or ROI claims.

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

Close with a one-line read-budget audit over the provided materials: which provided files you read in full versus skipped or skimmed, and why. It records coverage of the provided bundle; it is not a validation, readiness, or coverage claim.

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

## 5. Return routing

Return your full output in the chat where you received the courier wrapper. The
commissioning CA couriers it back for review-return adjudication; durable
report destination (written at ingestion):
`docs/review-outputs/adversarial-artifact-reviews/sov_field_contract_adversarial_artifact_review_v0.md`.
Nothing you return is kept, applied, or treated as accepted until that
adjudication.
