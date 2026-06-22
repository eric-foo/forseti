# Demand-Read Projection Semantics Propagation — Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Adversarial review prompt for the multi-file demand-read projection-semantics
  propagation patch at commit eca296145ac395e33b6b9c9928e4c96b29566f9d.
use_when:
  - Commissioning an adversarial review of the demand-read transient/durable semantics propagation patch.
  - Checking whether the 15-file doctrine propagation stayed coherent across taxonomy, CSB, capture, projection, buyer-proof, and Judgment surfaces.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
branch_or_commit: codex/demand-read-machinery-settlement-prompt @ eca296145ac395e33b6b9c9928e4c96b29566f9d
stale_if:
  - Commit eca296145ac395e33b6b9c9928e4c96b29566f9d is amended or superseded.
  - The demand-read projection-semantics patch is materially changed after this prompt.
  - The delegated-review-patch, review-lanes, or prompt-orchestration overlay contract changes.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 — constants bound; deltas stated below.

## Prompt Preflight

- authorization_basis: owner invoked `workflow-delegated-review-patch` after commit `eca29614` as a "just in case" hardening pass.
- output_mode: `file-write` for this prompt artifact; receiving review output mode is `review-report`.
- template_kind: `adversarial-artifact-review` via `docs/prompts/templates/review/adversarial_artifact_review_v0.md`.
- edit_permission: authoring lane is docs-write for this prompt only; receiving reviewer is read-only unless a later CA commission explicitly assigns patch execution.
- target_files_or_dirs: the 15 files changed by `eca29614` listed below.
- source_pack: custom S3 change-packet review pack; read the patch, the changed files, and the overlay authority named below.
- dirty_state_allowance: receiving reviewer should expect a clean checkout of branch `codex/demand-read-machinery-settlement-prompt` at `eca29614`; any extra dirt is a blocker unless explicitly supplied by the operator.
- branch_or_commit_reference: review `eca296145ac395e33b6b9c9928e4c96b29566f9d` against parent `c4655c976a3e7bc8a01ed415efbc20f5108908b8`.
- doctrine_change_decision: review only; this prompt changes no doctrine. The reviewed patch is doctrine-changing and carries its own propagation receipts/validation evidence.
- isolation_decision: existing lane worktree/branch; no new worktree required for this prompt artifact.
- validation_gates: reviewer checks source coherence and reports findings; no validation, readiness, approval, or keep decision is created by the review.
- thread_operating_target_continuity: omitted; no active durable thread operating target is bound.

## Copy-Paste Review Prompt

You are performing an adversarial artifact review for Orca.

### Commission Boundary

Review target:

- Commit: `eca296145ac395e33b6b9c9928e4c96b29566f9d`
- Parent/base: `c4655c976a3e7bc8a01ed415efbc20f5108908b8`
- Branch: `codex/demand-read-machinery-settlement-prompt`
- PR: `https://github.com/eric-foo/orca/pull/352`
- Review purpose: determine whether the demand-read projection-semantics propagation is coherent, sufficiently propagated, and free of stale or contradictory transient/durable proof language.

This prompt was produced after an owner invoked `workflow-delegated-review-patch`, but Orca's delegated-review-patch overlay is single-target for repo-mode patching. This target is a 15-file doctrine-change packet, so this commission is a read-only adversarial artifact review, not a repo-mode delegated patch commission and not executable patch authority. Patch suggestions are advisory findings only unless a later CA decision assigns patch execution.

### De-Correlation Receipt

- authored_by: OpenAI / GPT-family Codex lane, exact model/version `operator_to_fill` if needed.
- reviewed_by: `operator_to_fill`; record the actual reviewing model/version in the report.
- de_correlation_bar: `operator_to_fill`.
- If the reviewer is non-OpenAI upstream model lineage, label the pass `cross_vendor_discovery`.
- If the reviewer is OpenAI/GPT-family, unknown, or undisclosed lineage, do not claim cross-vendor discovery; label it `same_vendor_sanity` or `self_fallback` as appropriate.
- This is a who-constraint, not a model recommendation. Do not recommend, rank, or route runtime models.

### Required Authority Sources

Read these before review work:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

Use `workflow-deep-thinking` first. Then use `workflow-adversarial-artifact-review`. If either skill is unavailable or cannot be applied after source context is ready, return a blocked or advisory-only result and do not emit strict review claims.

### Source-Load The Change Packet

Review the diff:

```text
git diff c4655c976a3e7bc8a01ed415efbc20f5108908b8..eca296145ac395e33b6b9c9928e4c96b29566f9d
```

Review these changed files:

- `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
- `orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `orca/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md`
- `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
- `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_adjudication_v0.md`
- `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md`
- `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md`
- `orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
- `orca/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md`
- `orca/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md`
- `orca/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md`
- `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`

Declare `SOURCE_CONTEXT_READY` only after reading the authority sources, the diff, and the changed sections needed to support each finding. Otherwise declare `SOURCE_CONTEXT_INCOMPLETE` and list the gaps.

### Intended Semantic Standard To Attack

The owner-intended semantics are:

- Durable demand means strong real demand with an evidence-supported projection that it will stay strong over the relevant decision horizon.
- Durable is not merely a retrospective observation that demand already stayed strong.
- Observed persistence can support a durability projection, but it is not the definition.
- Transient demand is strong real current-window demand whose durability is not called, or whose evidence supports decay.
- Weak demand, attention-only engagement, fake/manufactured hype, or dedupe-contaminated signals are not transient demand.
- CSB, capture, and projection surfaces may preserve or pass evidence/gaps for durability, decay, and manufactured-hype dedupe, but they must not themselves call durable/transient/manufactured demand unless their lane owns that judgment.

### Review Checks

Find material issues in priority order. At minimum, attack:

1. Stale semantics: any active language still defines durable as "already stayed strong," "observed only," "earned only by monitoring," or treats transient as weak/default/fallback rather than strong current-window demand.
2. Over-propagation: any CSB, capture, projection, scan, or substrate-gate surface now makes a demand-state judgment it should only preserve or pass through.
3. Under-propagation: any Judgment, taxonomy, buyer-proof, scan, CSB, capture, or projection surface still lacks the owner-intended projection basis / transient-is-strong distinction where it makes or routes the call.
4. Proof confusion: any surface implies Orca can prove demand in a strict sense from these docs, rather than call demand with evidence, uncertainty, and named basis.
5. Grading confusion: any backtest or grading surface uses hindsight outcome-label matching instead of information-set evidence-basis grading.
6. Manufactured-hype dedupe gap: any surface calls transient demand without first separating fake/manufactured or engagement-only hype.
7. Structural damage from the patch: broken bullets, duplicated lines, malformed YAML, stale DCP receipts, contradictory heading dates, or line-range edit artifacts.
8. Prompt/overlay leakage: any imported `jb` mechanics, model recommendation, readiness/validation/proof overclaim, or forbidden runtime-model routing.
9. Propagation completeness: whether the changed surfaces are the right smallest-complete set, or whether a clearly owning surface remains stale and materially affects future work.

### Output Contract

Use findings-first output. Severity labels are finding-priority only: `critical`, `major`, `minor`.

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/demand_read_projection_semantics_propagation_adversarial_review_v0.md`

If you cannot write that report, return the failed `review_summary` shape with `review_location: chat_only_current_thread` and no `report_path`.

Each finding must include:

- severity;
- location;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- recommended correction or advisory remediation direction.

Do not include `patch_queue_entry` and do not apply patches unless a later CA prompt explicitly assigns patch or integration execution authority.

If no issues are found, say so and name residual risks or test gaps.

Review-use boundary: this review is decision input only. It is not approval, validation, readiness, proof, buyer-proof, mandatory remediation, source promotion, merge authorization, or executor-ready instruction.
