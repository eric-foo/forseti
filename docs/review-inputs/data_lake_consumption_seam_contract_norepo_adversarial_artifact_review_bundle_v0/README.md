# no_repo Adversarial Artifact Review Bundle — Data Lake Consumption Seam Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review input artifact (Review prompt role binding, docs/review-inputs/)
scope: >
  Self-contained no_repo review package: method, authority excerpts, commission, and
  attachment manifest for the de-correlated cross-vendor adversarial artifact review of
  core_spine_v0_data_lake_consumption_seam_contract_v0.md. The repo-blind reviewer needs
  ONLY the files in this bundle.
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
| `core_spine_v0_data_lake_consumption_seam_contract_v0.md` | REVIEW TARGET (verbatim attachment) | `C3D5A74B74273982C7E0192BB52504B0754E4F92DBF641DD39332B2B18D6C159` |
| `README.md` (this file) | Method + authority + commission | (pinned in the courier wrapper) |

If you can compute SHA256, confirm the target matches its pin and say so in your output; if
you cannot, proceed advisory-only and say so. If you cannot read the attached files at all,
reply only `BLOCKED_BUNDLE_UNREADABLE`.

**Freshness gate (assembler-run, 2026-07-02): PASS after re-derivation.** The portable
method's two `derived_from` pins had drifted since 2026-06-14; the assembler re-derived
before bundling: the review-template change (source-read budget + closing read-budget audit)
was material and is folded into method §6 below; the review-lanes changes were lane-index
wording only (pin-only re-pin). Both pins now match the live sources.

## 2. Commission (no_repo Delegated Review, advisory-only)

```md
# Delegated Review Commission — no_repo access mode

## Lane Binding
- overlay_status: provisional_opt_in (explicit commission for this single use, carried from
  the implementing lane's scoping Review Timing Advisory; not a bound review lane; creates
  no strict claims)
- operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md (no_repo mode)
- review_lane: artifact — executed via the PORTABLE METHOD block in §4 of this README
  (registry id portable-adversarial-artifact-review-method); the in-repo review skill is not
  available to you and your result is therefore ADVISORY FINDINGS, never a formal verdict
- mode: base-subagent shape, access: no_repo (reason: the commissioned external reviewer lane
  has no repository or worktree access; content identity travels by hash pin) — you review
  and propose; you DO NOT patch and you return findings, not a diff
- actor_model_family_receipt:
  - author_home_model_family: Anthropic (Claude; authored by claude-fable-5)
  - controller_model_family: operator-dispatched; MUST be a different vendor / model lineage
    than Anthropic (vendor = upstream model developer, not host/reseller/wrapper); unknown
    or undisclosed lineage CANNOT satisfy this commission's cross-vendor discovery bar
  - current_receiving_actor_role: controller (you, on receipt of the courier wrapper)
  - dispatch_mode: external-controller-courier
  - de_correlation_status: gated in the wrapper — self-check before reviewing
- de_correlation: a who-constraint of the commission, NOT a model recommendation or ranking.
  Cross-vendor is the DISCOVERY bar and is required for this pass's
  survives-adversarial-review-with-no-new-seam standard.

## Target
- target: core_spine_v0_data_lake_consumption_seam_contract_v0.md (the single named
  artifact; whole file)
- what it is: the consumption seam contract binding how EVERY derived lane (Silver, ECR,
  cleaning, projection) discovers committed raw work and acknowledges completion, plus the
  index rebuild-command binding and the on-demand-first metrics policy. A defect here
  propagates into every lane migration that adopts the seam.
- timing context (be adversarial about it): the contract's first implementation already
  landed on the authoring branch (shared helper, rebuild runner, one migrated consumer,
  tests green). This review is the commissioned post-implementation hardening pass carried
  from the route's Review Timing Advisory; nothing is ratified, accepted, or validated by
  that landing, and your findings may attack the contract even where the implementation
  already conforms to it.
- why_ordinary_same-family_review_is_insufficient: the contract was authored, implemented,
  and will be adjudicated by the same model family; the author encoded the guardrails
  (ack grammar, no-queue-as-truth, posture invariants) and can reintroduce the exact blind
  spots they exist to prevent.
- bounded_patch_scope: NONE for you (no_repo). Accepted amendments are applied by the home
  CA to the single target file after adjudication, followed by a bounded SAME-vendor
  mechanical-tier post-patch recheck (closure-of-findings + new blocker/major in the touched
  delta) before anything is kept.
- off_scope: everything beyond the attached files. You cannot and must not assess repository
  state, the landed implementation code, or test results; label repo-settleable claims
  `unverifiable from provided sources`.

## Roles (who-constraints, not recommendations)
- author / CA / home model (Anthropic family): authored the target; adjudicates every
  finding; owns what is kept; may veto any change at its discretion
- controller (you, de-correlated): judgment, findings, citations into the provided material;
  advisory verdict + residual risk; final authority stays with the CA
- patch executor: not engaged in no_repo mode (CA applies accepted amendments)

## Controller Output Contract
- follow the PORTABLE METHOD (§4) exactly: reasoning pass first, then findings; output shape
  per its §6 (review_summary first; findings ordered critical → major → minor with severity,
  location, issue, evidence, impact, minimum_closure_condition, next_authorized_action,
  advisory remediation direction; close with the one-line read-budget audit)
- citations: neutral in tone, decision-sufficient in substance — cite the target's own
  sections and the authority excerpts in §3; your argument lives in the verdict and
  residual-risk note, not the citations
- escalation: if the target's problem is design-level rather than amendment-level, set
  recommendation: NEEDS_ARCHITECTURE_PASS and return findings only
- do not emit executor-ready patch steps, patch queues, or any claim of validation,
  readiness, approval, or formal verdict

## Adjudication Contract (home / CA model — recorded here for your awareness)
- your findings, citations, and verdict are claims to adjudicate, not premises to inherit
- the CA accepts / modifies / rejects per finding; CA-applied amendments take the bounded
  same-vendor recheck before keep; the adjudication closes with the overlay's Review
  Adjudication Next Step tail (adjudicate → self-close closable issues → one land step →
  deep-think 1-5 material moves)
- the durable review record (written by the CA at ingestion under
  docs/review-outputs/adversarial-artifact-reviews/) will carry reviewed_by / authored_by
  provenance plus de_correlation_bar: cross_vendor_discovery; state your model identity and
  version in your output if known and permitted — otherwise the CA records `unrecorded`
```

## 3. Authority excerpts the target must conform to

The target binds itself to four ratified Data Lake contracts. These are the decisive
excerpts (paraphrase-minimal); the target must not fork, weaken, or contradict them. Attack
both conformance AND whether the target's own additions (obligation fingerprint, namespace
rule, conformance suite, view semantics) are sound.

**Storage contract (by-key authority; ack slot):**
> Downstream lanes scan or query by committed packet/slice/file keys. A queue may later
> optimize notification, but it is not the source of truth.
> Acknowledgement Log: append-only lane-owned completion or acknowledgement facts keyed to
> raw. Must not become: lake-consumed control flow for scheduling, gating, retrying, or
> calling another lane.

**Derived-layout + index-rebuild contract:**
> acknowledgements/<anchor_shard>/<raw-anchor>/<ack-namespace>/<ack-record-id> —
> acknowledgements are lane-owned facts keyed to raw, one create-only record per fact;
> correction is a new ack record.
> All of indexes/ is rebuildable from committed material, or it is not an index.
> derived_retrieval rebuilds only from committed derived/ + raw refs and remains
> non-authoritative. [Gate opened 2026-06-25 for exactly three object-level views:
> by_creator (per-platform), by_mention, undone; no engine selected; SQL query-lens stays
> scan/query-latency-gated.]
> Command shape: lake indexes rebuild --root <ORCA_DATA_ROOT> --target
> availability|derived_retrieval|all --prove-rebuildability

**Write-boundary enforcement contract:**
> derived/ and acknowledgements/: append-only create; no replace, delete, or in-place
> rewrite. Enforcement is mechanical at the write/byte boundary, not reliant on reviewer
> discipline. By-key discovery stays authority; a queue may optimize notification but is
> never the source of truth.

**Silver Vault record contract (read models + metric posture):**
> Generated read models are not authority. Query tables must be rebuildable from committed
> raw + derived records. Every generated query table and envelope must have a manifest row
> [with] generation id, source record ids, source high-watermark, selection policy versions
> used, generated_at, and stale/drift detection fields.
> metric_value = 0 is valid only as a real observed zero from the source. Never means
> missing. Missing, hidden, blocked, not attempted, not applicable, outside window must be
> represented by posture + reason, not by numeric value.

**Authoring environment's foundational behavior + scope-discipline doctrine — AGENTS.md
(Orca), excerpted verbatim** (conformance to this is part of the review):

> Default to the smallest complete intervention: solve the actual request completely with
> the narrowest sufficient scope.
> Every changed line must trace to the user request or required validation.
> Preserve real failure visibility; never create fake success paths.

> **Smallest Complete Intervention.** `Complete` is load-bearing. Do not underfix to
> minimize diff, ceremony, or visible change; a slightly larger fix is correct when required
> for durable, coherent, non-fragile completion. `Smallest` is also load-bearing. Do not add
> unrelated cleanup, speculative abstractions, broad rewrites, extra workflow ceremony, or
> nice-to-have improvements.

**Fitness reference (attack it too):** the seam's success signal, from the accepted scoping
route — "every derived lane (Silver, ECR, cleaning, projection) would pick up committed
Bronze work the same tested way, with metrics views rebuildable and never authoritative";
drift cues — a queue/event system becoming pickup truth, pickup logic entering the lake
core, a view becoming load-bearing, a backend being selected, a metric family being named
without owner input.

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

Close with a one-line read-budget audit over the provided materials: which provided files you read in full versus skipped or skimmed, and why. It records coverage of the provided bundle; it is not a validation, readiness, or coverage claim.

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

## 5. Return routing

Return your full output in the chat where you received the courier wrapper. The
commissioning CA will courier it back into the home lane for review-return adjudication;
the durable report is written there (destination pre-assigned:
`docs/review-outputs/adversarial-artifact-reviews/data_lake_consumption_seam_contract_adversarial_artifact_review_v0.md`).
Nothing you return is kept, applied, or treated as accepted until that adjudication.
