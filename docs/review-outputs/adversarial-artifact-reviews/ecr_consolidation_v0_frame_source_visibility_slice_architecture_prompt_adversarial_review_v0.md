# Adversarial Artifact Review — ECR Consolidation v0 Frame + Source-Visibility Slice Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review artifact (adversarial artifact review report)
scope: >
  Read-only adversarial artifact review of the architecture-planning PROMPT that
  commissioned ECR consolidation v0 (thin frame + source-visibility slice). Target
  is the prompt artifact, not the plan it produced and not code.
use_when:
  - Deciding whether to reuse / rerun the ECR-consolidation-v0 architecture prompt.
  - Patching the prompt before it is treated as a clean reusable artifact.
authority_boundary: retrieval_only
reviewed_target: docs/prompts/architecture/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_v0.md
branch_or_commit: main @ d69aeee (worktree dirty; target prompt + producer code untracked/modified -> advisory only)
```

## Review summary (courier YAML)

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_adversarial_review_v0.md
  recommendation: patch_before_acceptance
  summary: "Sound, well-bounded prompt that drove a successful run, but it embeds a false producer-state fact and leaves the central owner-open authority unprovenanced; patch before reuse/rerun."
  findings_count: 4
  blocking_findings: []
  advisory_findings:
    - PR-01: Source pack embeds a now-false producer fact and under-pins the most volatile source (major)
    - PR-02: The load-bearing "owner OPENED the consolidation" decision has no cited provenance (major)
    - PR-03: Commissioning "SP-6 as the first authored ECR field" presupposes the owner-reserved ECR-object decision (minor)
    - PR-04: Output contract under-bound — two modes offered, no exact destination path (minor)
  optional_hardening:
    - OH-1: Inline restatement of SP-6-plan content is a maintenance-drift surface (mitigated by hash-pin)
  prior_findings_remediated: []
  next_action: "Owner decides whether to patch PR-01/PR-02 before any rerun; no plan rework needed (the prior-session plan already absorbs all four)."
```

## Commission

User (owner) instruction: "prompt — adv review." Adversarially review the prompt at `docs/prompts/architecture/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_v0.md` — the prompt this session read-and-executed. Maximally adversarial about material, decision-relevant failure modes in the prompt; not a re-review of the plan it produced and not a code review.

## Target

`docs/prompts/architecture/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_v0.md` (full prompt artifact, 132 lines). Read directly this session; untracked working-tree artifact -> advisory.

## Authority / decision criteria

- Lane: **adversarial artifact review** (`.agents/workflow-overlay/review-lanes.md`) — read-only; report under `docs/review-outputs/adversarial-artifact-reviews/`; `critical`/`major`/`minor` for priority only; recommendation vocabulary `accept | accept_with_friction | patch_before_acceptance | reject | blocked`; findings-first; `minimum_closure_condition` (required end state) + `next_authorized_action`; no `patch_queue_entry`.
- Prompt-quality criteria: the 13 prompt validation gates in `.agents/workflow-overlay/prompt-orchestration.md`; preflight + source-loading rules in `.agents/workflow-overlay/source-loading.md`; doctrine-propagation rules in `.agents/workflow-overlay/source-of-truth.md`; retrieval-metadata contract.
- Method: `workflow-deep-thinking` + `workflow-adversarial-artifact-review` REFERENCE-LOADED before source readiness, APPLIED after `SOURCE_CONTEXT_READY` (source `agent-workflow` cache `0.1.50`; resolver behavior not proven in-thread — advisory mechanics only).

## Scope / excluded scope

- **In scope:** the prompt's source support, internal consistency, authority/provenance, boundary control, output binding, and downstream executability.
- **Excluded:** re-reviewing the synthesized plan at `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` (written by the prior session that first ran this prompt; current at d69aeee; untracked); reviewing harness code correctness; JSG-01 unfreeze; any product-proof claim checking (the prompt is not a product-proof artifact).

## Source-read ledger + dirty-source names

- Target prompt — read directly; untracked (advisory).
- `.agents/workflow-overlay/prompt-orchestration.md`, `review-lanes.md`, `source-loading.md`, `source-of-truth.md`, `AGENTS.md` — read directly; the prompt-quality authority.
- `orca-harness/source_capture/models.py` — read directly; **modified (dirty)**. Decisive for PR-01: `PreservedFile.hash_basis` exists (`:102`), closed to `{raw_stored_bytes}` (`:66`, AR-04 validator `:105-114`).
- `docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` — read directly; untracked; hash-pin matched. Decisive for PR-02/PR-03 (says opening the consolidation is owner-reserved and was NOT done; SP-2 section assumes "no hash_basis").
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` — read directly; **modified (dirty)**; still `PROPOSED_FREEZE` with the consolidation reserved (`:281-309`). Decisive for PR-02/PR-03.
- `docs/product/jsg01_source_side_receipt_translator_v0.md`, `data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` — read directly; untracked; hash-pins matched.

**Dirty-source caveat:** producer code and boundary doc are modified; the three planning docs and the target prompt are untracked. All findings are **advisory**; no strict readiness/acceptance claim is made about the prompt or the work it produced.

## Preflight results

- Deep-thinking discipline: applied (failure modes, hidden assumptions, authority leaks, source gaps framed before findings).
- Trigger gate: PASS — explicit adversarial artifact review request on a repo-visible non-code artifact (a prompt).
- Lane-collision: resolved — prompt artifact -> adversarial artifact review lane (the prompt-review lane overlaps, but the user named "adv review"; `review-lanes.md` routes adversarial review of prompts here). No `BLOCKED_LANE_COLLISION`.
- Artifact-role / output binding: `filesystem-output` with `required_output_path` = this report (overlay default destination, derivation convention bound by `prompt-orchestration.md`). PASS.
- Validation-gate semantics: findings-first advisory; recommendation bound by overlay vocabulary; no patch-queue emitted.

---

## Phase 1 — Correctness findings

### PR-01 — Source pack embeds a now-false producer fact and under-pins the most volatile source · `major`

- **Phase:** correctness (source support).
- **Location:** prompt "Source pack / required reads" line: *"Implemented producer (READ — the blind-spot fix): `orca-harness/source_capture/models.py` (`SourceCapturePacket`, `VisibleFact`, `PreservedFile` — no `hash_basis`)"*; and `branch_or_commit` / locked-decision line *"R2 (posture-vocabulary closure, in flight)."*
- **Source authority:** `orca-harness/source_capture/models.py:102` (`PreservedFile.hash_basis: str`), `:66` (`HASH_BASIS_VALUES = {"raw_stored_bytes"}`), `:105-114` (AR-04 validator); `:48-55,90-94,129-143,185-199` (Ob.9/10/15 closed vocabularies enforced at write-time).
- **Defect:** the prompt asserts a specific producer-state fact — "PreservedFile — no `hash_basis`" — that is **contradicted by the producer** in the working tree (and was already being landed by the capture lane the prompt itself names). It also describes R2 as merely "in flight" when R2 is in fact *enforced-but-uncommitted* in the working tree. Compounding this: the prompt **pins three stable docs by SHA256 in `input_hashes` but does not pin the producer code** — i.e., the most decision-volatile, concurrently-changing source (the one it labels "the blind-spot fix") is the one left unpinned and described with a stale inline claim. This is a pinning-priority inversion.
- **Impact:** the false "no `hash_basis`" claim is decision-bearing for D3 / the SP-2 verifiability basis. An executor who trusts it (as the upstream SP-6 plan did) designs the slice's recomputation basis around an acquisition-receipt fallback instead of the upstream closed `PreservedFile.hash_basis` — a wrong primary basis. The "in flight" vagueness creates a strict-claim hazard (is R2 available or not?).
- **Mitigation present:** the `branch_or_commit` note does say *"recheck source_capture/* if HEAD advanced,"* which is why this run caught it. The defect is the embedded false fact + unpinned volatile source, not the absence of any warning.
- **Blocked state:** not a blocker; advisory.
- **`minimum_closure_condition`:** the prompt's producer description states only what is verifiable at its pin (or carries no producer-state assertion beyond "read and verify against HEAD"), and the volatile producer source is either pinned or explicitly flagged as recheck-required-because-changing; "R2" is characterized as present-but-uncommitted rather than "in flight."
- **`next_authorized_action`:** owner decision to patch the prompt before any rerun (cheap: correct the parenthetical + flag the producer as verify-against-tree). No plan rework is implied — the existing prior-session plan already verified the producer and carried the correction.
- **`patch_queue_entry`:** not authorized (read-only lane).
- **`not proven`:** that R2/`hash_basis` is committed/ratified (it is uncommitted working-tree state).

### PR-02 — The load-bearing "owner OPENED the consolidation" decision has no cited provenance · `major`

- **Phase:** correctness (source support + authority).
- **Location:** prompt "Locked decisions": *"The ECR consolidation is OPENED by the owner, scoped to the source-visibility slice."* (echoed in Commission, Authorization, and `thread_operating_target_continuity`).
- **Source authority:** `docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md:35,42,115,286` (opening the consolidation / Option B is **owner-reserved** and was **not** selected/entered); `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md:19,281-309,367` (consolidation still reserved; status `PROPOSED_FREEZE` / `NEEDS_FOUNDATION_ACCEPTANCE`).
- **Defect:** the single most load-bearing premise of the whole task — that the owner has opened the previously-reserved consolidation — is **asserted in the prompt with no cited owner decision record**. It directly reverses the controlling sources, which say opening is owner-reserved and not done. No `docs/decisions/...` artifact, owner-acceptance receipt, or current-turn-owner-instruction marker is cited.
- **Impact:** on rerun by a fresh agent (or audit by a later lane), the authorization for the entire consolidation is unverifiable. This is exactly the receipt/predicate provenance trap the overlay guards against (validation gate 1: modified/untracked controlling sources block strict claims unless owner acceptance is explicit). The work proceeded this turn only because the user-owner issued the instruction in-thread (source hierarchy #1) — but that provenance is not captured in the durable prompt.
- **Blocked state:** not a blocker for advisory work; it *would* block a strict readiness/ratification claim (correctly, the prompt does not make one).
- **`minimum_closure_condition`:** the owner-open authorization is traceable — either a cited owner decision artifact, or an explicit "current-turn owner instruction; record a decision artifact at ratification" marker — so a fresh reader can verify the open without the owner present.
- **`next_authorized_action`:** owner decision to (a) confirm the open and (b) have the prompt cite/anchor it before reuse; at ratification this becomes the boundary-doc edit + DCP the plan already routes to.
- **`patch_queue_entry`:** not authorized.
- **`not proven`:** that the consolidation is formally opened in any controlling source (it is opened by in-thread owner instruction only).

### PR-03 — Commissioning "SP-6 as the first authored ECR field" presupposes the owner-reserved ECR-object decision · `minor`

- **Phase:** correctness (internal consistency / boundary control).
- **Location:** prompt Commission part 2 (*"SP-6 ... as the first authored ECR field"*) and the Output bullet (*"SP-6 as an ECR field"*).
- **Source authority:** `core_spine_v0_data_and_cleaning_spine_boundary_v0.md:283-284,298-299,309` (whether ECR is the canonical object name and the final field architecture are owner-reserved); `jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md:115` (Option B gating act #2 = "accept an ECR object exists as the field home").
- **Defect:** authoring a *field* presupposes accepting that the *ECR object exists* as the field home — itself one of the gating owner-reserved acts. The prompt does not surface the strictly-smaller alternative (author only the derivation contract / seed, deferring the field declaration) as an owner sub-choice.
- **Impact:** risk that the executor freezes "ECR is the object + a field is declared" when the owner may have wanted only the derivation contract scoped. Material to *what the owner ratifies*.
- **Mitigation present (why minor, not major):** the prompt explicitly says "a canonical (**at least provisional**) ECR object name," keeps the lane **non-executing/design-only**, and lists siblings "named-but-deferred." Those guards bound the freeze risk to "an unsurfaced owner sub-choice," not an actual commitment; everything is reversible advisory design.
- **Blocked state:** none.
- **`minimum_closure_condition`:** the prompt names "author-the-field vs author-only-the-derivation-contract" as an owner choice at ratification, and flags that hosting a field provisionally assumes the (owner-reserved) ECR-object-exists question.
- **`next_authorized_action`:** carry the choice into the ratification request (the existing prior-session plan already surfaced this as AF-7); no prompt rerun required.
- **`patch_queue_entry`:** not authorized.

### PR-04 — Output contract under-bound: two modes offered, no exact destination path · `minor`

- **Phase:** correctness (downstream executability / output binding; prompt validation gate 5).
- **Location:** prompt Output: *"Output mode: `file-write` the plan to `docs/` (or `chat-only`)."*; preflight `target_scope: [the ECR-consolidation-v0 architecture plan artifact under docs/]`.
- **Source authority:** `prompt-orchestration.md` gate 5 ("exactly one output mode is named, with write destination"); Default Path Assignment ("a repo-aware prompt handed to another agent must state ... the exact output artifact path"); `source-loading.md` preflight fields.
- **Defect:** the prompt offers **two** output modes (`file-write` *or* `chat-only`) with no decision rule, and names a destination **tree** (`docs/`) rather than an exact path/child folder. Gate 5 wants exactly one mode + a write destination.
- **Impact:** the executor must choose the mode and derive the path; the prior run derived `docs/product/..._architecture_plan_v0.md`. Low impact for a single careful run; higher drift risk across reruns or different executors (inconsistent destinations / a substantial routing object landing in chat-only).
- **Blocked state:** none.
- **`minimum_closure_condition`:** the prompt names exactly one output mode and an exact destination path (or a bound derivation convention), e.g. `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`.
- **`next_authorized_action`:** optional prompt patch before reuse; no plan rework (the existing prior-session plan is at the conventional path).
- **`patch_queue_entry`:** not authorized.

---

## Phase 2 — Friction findings

No required friction findings. The prompt's density is mostly load-bearing (locked decisions, guards, source pack, subagent contract); it is not avoidable process bloat.

### OH-1 (optional hardening, non-required) — Inline restatement of SP-6-plan content is a maintenance-drift surface

- The prompt restates D1–D4, the residual concept, and the input vocabulary inline rather than referencing the SP-6 plan for them. If the SP-6 plan changes, the inline copies can drift. **Mitigated** because the prompt hash-pins the SP-6 plan (`input_hashes`) and lists it as the slice spec, so drift is detectable. Optional: thin the inline restatement to references where the pinned plan is authoritative. **Not a blocker, not mandatory.**

---

## Non-findings (checked, sound)

- Source-Gated Method Contract sequencing is correctly specified (REFERENCE-LOAD -> SOURCE-LOAD -> declare -> APPLY); gate 8 satisfied.
- Subagent contract satisfies the same-contract rule (source pack + own readiness gate + advisory-only, non-verdict); 3 general-purpose subagents explicitly authorized.
- `thread_operating_target_continuity` block present and correctly shaped (gate 9).
- Doctrine propagation correctly **deferred**: the prompt's `doctrine_note` states the boundary-doc edit + DCP is a later owner-gated step, not this lane — and correctly does **not** demand a DCP this turn (gate 12 satisfied; consistent with `source-of-truth.md`).
- Boundary control is strong: overbuild guard, premature-freeze guard, JSG-01-frozen, owner-reserved list, no `jb` import, `agent-workflow` as mechanics only.
- Retrieval header present and bounded (gate 10) — though `input_hashes` omits the producer code (see PR-01).

## Recommendation (advisory decision input)

`patch_before_acceptance`. The prompt is fundamentally sound and drove a successful, well-bounded run — but two `major` correctness/authority defects (PR-01 false/under-pinned producer state; PR-02 unprovenanced owner-open) would mislead a fresh rerun or fail an audit, and should be patched before the prompt is treated as a clean reusable artifact. Decisive criterion: a durable prompt must be verifiable by a fresh reader without the owner present, and must not embed a source fact its own named source contradicts. The two `minor` findings (PR-03, PR-04) and OH-1 are cheap to fold into the same patch.

**Important:** this recommendation is about *prompt reuse/rerun*, not about reworking the existing plan. Provenance: the synthesized plan at `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` was written by the **prior session** that first ran this prompt (current at d69aeee, untracked); it already absorbs all four findings — it corrects the `hash_basis` premise, fences R2 as uncommitted / `not_proven`, surfaces the field-vs-contract owner sub-choice (its AF-7), and routes correctly. **This session's** re-run reached `SOURCE_CONTEXT_READY` + the 3-subagent fan-out (which independently reproduced that design) and was then redirected to this review; it did **not** re-synthesize the plan. So no plan rework is implied by these findings.

## Review-use boundary

These findings are decision input for the owner / Chief Architect. They are not approval, validation, mandatory remediation, or executor-ready patch authority. Only a separately authorized patch or owner decision can make any remediation mandatory or executor-ready. This review is advisory (target prompt and several controlling sources are untracked/modified). It does not unfreeze JSG-01, ratify the consolidation, or accept the produced plan.
