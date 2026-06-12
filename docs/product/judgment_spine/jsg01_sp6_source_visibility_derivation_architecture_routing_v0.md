# JSG-01 SP-6 Source-Visibility Derivation Architecture Routing v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Non-executing architecture routing object for the JSG-01 SP-6
  source_visibility_posture derivation: ownership boundary, mechanical rule
  shape, residuals, and SP-2 hash_basis verifiability interaction.
use_when:
  - Deciding whether SP-6 should be a JSG-01 interim reader rule or future ECR-owned rule.
  - Preparing the owner decision on SP-6 derivation ownership and comparison/materiality residuals.
  - Rechecking SP-6 after the capture-build lane re-couriers capture-context or hash_basis deltas.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/architecture/jsg01_sp6_source_visibility_derivation_architecture_prompt_v0.md
  - docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/product/data_capture_spine/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md
input_hashes:
  docs/product/jsg01_source_side_receipt_translator_v0.md: E8944D13FF8B3FAF62AC24209EC50FDA7C03CC9D4F906687246B2E15C01592B2
branch_or_commit: main @ e4e854e (worktree dirty; controlling prompt/product/review sources include untracked or modified files)
stale_if:
  - The owner selects Option A or explicitly authorizes Option B / ECR consolidation entry.
  - The capture-build lane re-couriers the dedicated capture-context field, acquisition-scope contract, or hash_basis contract.
  - docs/product/jsg01_source_side_receipt_translator_v0.md changes SP-6 values, residuals, or owner-reserved status.
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md changes Ob.9, Ob.10, Ob.11, Ob.15, or Ob.16.
  - The full ECR/EvidenceUnit consolidation supersedes this interim routing object.
```

- Status: `ADVISORY_ARCHITECTURE_ROUTING_OBJECT_OWNER_DECISION_REQUIRED`
- Output mode: `file-write`
- Edit permission used: docs-write for this architecture routing artifact only.
- Authorizes: nothing. Not implementation, not schema work, not ECR consolidation, not JSG-01 unfreeze, not source capture, not validation.
- Doctrine-change assessment: this artifact is owner decision input and does not amend a controlling source. No direction-change propagation receipt is emitted because no product/architecture doctrine is ratified or changed here.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope:
    - docs/product/jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md
  dirty_state_checked: yes
  blocked_if_missing: yes for strict readiness/acceptance claims; no for advisory architecture routing
workspace_state:
  branch: main
  observed_head: e4e854e
  dirty_state: dirty
  target_source_state:
    docs/prompts/architecture/jsg01_sp6_source_visibility_derivation_architecture_prompt_v0.md: untracked
    docs/product/jsg01_source_side_receipt_translator_v0.md: untracked; hash matched prompt pin
    docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md: untracked
    docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md: tracked clean in targeted status
    docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md: modified
    docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md: untracked
strict_claim_boundary: >
  Dirty and untracked controlling sources allow advisory planning only. They do
  not support strict PASS, readiness, acceptance, ratification, source-of-truth,
  validation, gate-clearance, fixture-admission, implementation, or
  judgment-quality claims.
```

## Method And Evidence Status

```yaml
source_context_status: SOURCE_CONTEXT_READY_ADVISORY
method_sequence:
  workflow-deep-thinking:
    reference_loaded_before_source_loading: yes
    applied_after_source_context_ready: yes
  workflow-architecture-planning:
    reference_loaded_before_source_loading: yes
    applied_after_source_context_ready: yes
subagents:
  launched: 3
  completed: 3
  runtime: inherited/default agent type and model
  evidence_mode: delegated advisory lanes plus local synthesis
  lanes:
    - SA-1 Option A architect
    - SA-2 Option B architect
    - SA-3 adversary / integrator
  boundary: advisory input only; not verdicts, not proof, not implementation authority
```

Source-read ledger:

| Source | Why read | Observed state |
| --- | --- | --- |
| `AGENTS.md` | Workspace rules, overlay requirement, durable-claim verification boundary | modified in worktree |
| `.agents/workflow-overlay/README.md` | Orca overlay entrypoint | modified in worktree |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and doctrine-change contract | read |
| `.agents/workflow-overlay/prompt-orchestration.md` | Output mode, source-gated method contract, prompt gates | modified in worktree |
| `.agents/workflow-overlay/source-loading.md` | Start preflight, source pack, dirty-state strict-claim boundary | modified in worktree |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted folder for output artifact | modified in worktree |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact role and write permission | modified in worktree |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | read |
| `docs/prompts/architecture/jsg01_sp6_source_visibility_derivation_architecture_prompt_v0.md` | Commission, frozen contract, output contract | untracked |
| `docs/product/jsg01_source_side_receipt_translator_v0.md` | SP-6 definition, SP-2 hash_basis requirement, owner residuals | untracked; SHA256 matched prompt pin |
| `docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md` | AR-01 source and hash_basis review history | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Ob.9/10/11/15/16 capture obligations | tracked clean in targeted status |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Data Capture / ECR / Cleaning / Judgment boundary and owner-reserved ECR field architecture | modified |
| `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` | Relevant expanded source for capture posture closure, access_posture free-text, SP-6 still-needs-derivation residual | untracked |
| `orca-harness/source_capture/models.py` | Read-only orientation on current implemented VisibleFact posture shapes | modified; not used as Orca authority |

## Human Summary

Recommendation: **route SP-6 through Option A now, as a JSG-01-side interim reader rule, only if the owner approves it as bounded interim logic.** Preserve Option B as the eventual cleaner home, but do not select it in this lane because it enters the owner-reserved ECR consolidation.

The key pushback: a value-only "complete closed table" is not honest under the frozen contract. The table can be exhaustive only because named residuals are allowed. Any rule that emits `archive_diverged` merely from `re_capture_relationship: conflict`, or parses `access_posture` free text into a closed value, is smuggling a Judgment/ECR decision into this lane.

## Architecture Frame

The real architecture decision is not "which field name should exist." It is where the SP-6 composite derivation may live without violating three boundaries:

1. JSG-01 remains frozen and cannot be made determinate by this plan.
2. ECR field architecture and consolidation remain owner-reserved.
3. Capture records value posture and limitations; downstream owner/Judgment authority owns sufficiency, materiality, and finalization.

The frozen contract gives SP-6 these inputs:

- `archive_history_posture`: `known/archived`, `known/attempt_failed`, `not_attempted/<reason>`, or `not_applicable/<reason>`;
- `re_capture_relationship`: `supersede`, `supplement`, `conflict`, or `mixed`;
- acquisition-receipt capture scope and recomputation-bound `hash_basis`;
- a new dedicated capture-context field, consumed but not designed here;
- `access_posture`, which remains free text.

The SP-6 output set is:

```text
archive_corroborated
archive_only
archive_diverged
current_capture_only
archive_post_cutoff_only
attempt_failed
not_attempted
not_applicable
```

Those values are recording values only. The visibility-sufficiency grade remains an owner residual. Finalization authority remains an owner residual. Material divergence remains downstream Judgment-owned unless the owner explicitly authorizes a non-Judgment comparison fact that this rule may consume.

## Option A - JSG-01 Interim Reader Rule

Shape: JSG-01 carries a narrow interim reader rule that derives SP-6 from already-produced capture/acquisition facts. It may live as a companion note referenced by the SP-6 section of `docs/product/jsg01_source_side_receipt_translator_v0.md`, or later be folded into that artifact after owner approval and review.

Core responsibilities:

- read the capture-owned structured posture facts and acquisition receipt;
- preserve `access_posture` as residual free text, not an enum source;
- map every structured combination to one SP-6 value or named residual;
- keep SP-2 hash-basis verification separate from SP-6 visibility posture;
- name the future ECR migration boundary.

Must not own:

- source capture or archive fetching;
- current/archive diff execution;
- materiality judgment;
- SP-6 sufficiency grade;
- finalization authority;
- canonical ECR field naming or schema;
- JSG-01 unfreeze.

Pros:

- smallest current move that answers AR-01 without entering ECR;
- keeps JSG-01 frozen while making the current-live-vs-archive limitation visible;
- avoids pretending the future ECR receipt exists;
- can be retired cleanly when ECR consolidation is authorized.

Cons:

- interim reader logic can drift if left alive after ECR consolidation;
- still depends on a capture-context field whose exact shape is capture-lane-owned;
- can duplicate Source Capture Armory semantics unless it reads upstream facts instead of coining parallel ones;
- cannot honestly emit all closed values without residuals.

## Option B - Future ECR-Owned Rule

Shape: SP-6 becomes part of the future ECR-owned receipt. ECR would own the receipt slice that names structured source-visibility inputs, residuals, comparison basis, and the derived visibility posture.

Core responsibilities if later authorized:

- define the ECR receipt's source-visibility slot or successor concept;
- bind source-slice identity and acquisition-scope references;
- define how capture facts become receipt fields without making Data Capture an ECR schema;
- bind residual grammar for access posture, conflicts, and comparison materiality;
- make SP-2 / SP-6 recomputation coverage a coherent receipt substrate.

Pros:

- cleaner eventual home for the receipt contract;
- reduces duplicate JSG-01-specific adapter logic;
- fits the boundary source that ECR owns pre-cleaning captured-signal receipt shape;
- can make SP-2 and SP-6 provenance coupling explicit.

Cons:

- selecting it now crosses the owner-reserved ECR consolidation boundary;
- higher blast radius because it starts canonical receipt design;
- risks schema-by-stealth and JSG-01 unfreeze-by-stealth;
- still cannot turn `archive_diverged` into a mechanical value without materiality authority.

Authorization required before Option B:

- owner explicitly selects Option B or authorizes ECR consolidation entry;
- owner permits canonical field/slot naming or successor naming;
- owner decides whether comparison/materiality facts may be ECR-owned, Judgment-owned, or left residual;
- owner decides whether JSG-01 waits for ECR or uses an interim reader.

## Adversarial Findings

1. `archive_diverged` is dangerous as currently named. It implies material divergence, and materiality is downstream Judgment-owned. The rule must emit a residual unless a separately authorized comparison/materiality fact is present.
2. `archive_corroborated` is only mechanical when the comparison basis is recomputable and exact enough to avoid a semantic materiality call. If the match is semantic or "material", the same residual problem applies.
3. `access_posture` must not be keyword-parsed. It may carry residual text or expose conflicts, but it cannot produce closed SP-6 values.
4. `current_capture_only` and `not_attempted` overlap unless precedence is explicit. This plan makes `current_capture_only` the output when current/live capture exists and no archive success/attempt result establishes pre-cutoff archival visibility; `not_attempted` is reserved for no archive attempt and no current captured scope sufficient to identify current-only posture.
5. Option B is architecturally appealing but not authorized. Selecting it here would bypass the owner-reserved ECR consolidation.
6. SP-2 and SP-6 must stay separate. A current-live hash with a valid basis proves bytes-held verifiability, not pre-cutoff visibility.
7. The current workspace state blocks strict claims. This routing object is advisory because the prompt, translator, review report, and posture proposal are untracked and the boundary note is modified.

## SP-6 Derivation Rule Shape

This is a precedence-ordered decision table. It is exhaustive because every input combination either matches one value row or falls to a named residual. Rows above value rows are protective residual rows; they prevent hidden Judgment, ECR, or free-text parsing.

Normalized input facets:

| Facet | Source basis | Allowed design-altitude states |
| --- | --- | --- |
| Archive/history posture | Ob.10 / frozen contract | `archived`, `attempt_failed`, `not_attempted`, `not_applicable`, `missing_or_conflict` |
| Archive cutoff scope | acquisition receipt + capture context | `pre_cutoff_archive`, `post_cutoff_archive_only`, `archive_cutoff_unknown`, `not_applicable`, `none` |
| Current capture scope | acquisition receipt | `current_capture_present`, `no_current_capture`, `current_scope_unknown` |
| Re-capture relationship | Ob.15 / frozen contract | `supersede`, `supplement`, `conflict`, `mixed`, `not_applicable_or_first_capture`, `missing_or_conflict` |
| Capture-context signal | new capture-context field | consumed abstractly only: `cutoff_sensitive`, `cutoff_insensitive_or_archive_not_applicable`, `former_overload_context`, `missing_or_delta` |
| Access posture | Ob.11 | free-text residual only; not a closed table key |
| Comparison basis | acquisition/hash basis + authorized comparison fact | `exact_recomputable_same`, `owner_or_judgment_authorized_material_divergence`, `comparison_needed_but_missing`, `comparison_not_recomputable`, `not_needed` |

Protective residual rows:

| Precedence | Condition | Output |
| --- | --- | --- |
| R0 | Capture-context field shape has been re-couriered or is missing in a way that changes archive applicability or cutoff sensitivity. | `capture_context_delta_residual` |
| R1 | Structured inputs contradict each other, or `access_posture` materially contradicts structured fields. | `source_visibility_fact_conflict_residual` |
| R2 | The only decisive visibility/archive fact appears in `access_posture` free text. | `structured_visibility_fact_missing_residual` |
| R3 | `re_capture_relationship` is `conflict` or `mixed` but source-slice/acquisition scope does not isolate original, archive, current, fallback, or failed-access states. | `recapture_scope_residual` |
| R4 | Pre-cutoff archive and current capture both exist, but the rule would need a materiality or comparison judgment that is not owner/Judgment-authorized. | `archive_current_comparison_residual` |
| R5 | A corroborated/diverged comparison is claimed, but `hash_basis` or owner-bound acquisition receipt does not cover the relevant archive/current bytes. | `comparison_not_recomputable_residual` |

Value rows:

| Precedence | Structured condition after residual rows | SP-6 output |
| --- | --- | --- |
| V1 | Archive/history posture is `not_applicable`, or capture-context signal justifies cutoff-insensitive/archive-not-applicable treatment. | `not_applicable` |
| V2 | `archived` + `pre_cutoff_archive` + `current_capture_present` + `exact_recomputable_same`. | `archive_corroborated` |
| V3 | `archived` + `pre_cutoff_archive` + `current_capture_present` + `owner_or_judgment_authorized_material_divergence`. | `archive_diverged` |
| V4 | `archived` + `pre_cutoff_archive` + `no_current_capture`. | `archive_only` |
| V5 | `archived` + `post_cutoff_archive_only`, with no pre-cutoff archive. | `archive_post_cutoff_only` |
| V6 | `archived` + `archive_cutoff_unknown`. | `archive_cutoff_unresolved_residual` |
| V7 | `attempt_failed`, with no pre-cutoff archive establishing visibility. | `attempt_failed` |
| V8 | `not_attempted` + `current_capture_present`, with no pre-cutoff archive establishing visibility. | `current_capture_only` |
| V9 | `missing_or_conflict` archive/history posture + `current_capture_present`, where the missing posture is not recoverable from structured fields. | `archive_history_posture_missing_residual` |
| V10 | `not_attempted` + `no_current_capture`. | `not_attempted` |
| V11 | Any combination not matched above. | `source_visibility_unresolved_residual` |

Interpretation constraints:

- `archive_diverged` is not emitted from `re_capture_relationship: conflict` alone.
- `archive_corroborated` is not emitted from a human assertion of "looks same" unless the owner has authorized that comparison fact for this layer.
- `current_capture_only` does not clear archival pre-cutoff visibility. It records a visible limitation.
- `attempt_failed` wins over `current_capture_only` when an archive attempt failed and no pre-cutoff archive exists, because the failed attempt is the more specific archive-history posture.
- `not_attempted` is not an escape hatch. It records absence of archive attempt when no more specific current-only or failed-attempt posture applies.
- `access_posture` travels with the result as residual context and may trigger conflict residuals, but it is not parsed into the closed SP-6 values.

## SP-2 Verifiability Check Shape

SP-2 asks whether Orca can re-check the exact bytes held. SP-6 asks whether the visibility posture supports pre-cutoff visibility. They interact but do not substitute for each other.

SP-2 check:

| Check | Pass condition | Failure result |
| --- | --- | --- |
| Hash presence | non-placeholder sha256 or owner-bound equivalent exists for the preserved object | SP-2 cannot be `inspectable_verifiable` |
| Coverage basis | `hash_basis` names the recomputation coverage, such as `relative_packet_path` plus slice/encoding, or an owner-bound acquisition receipt states what bytes the hash covers | hash-shaped string is insufficient |
| Scope alignment | basis covers the same bytes used by the SP-6 claim: archive bytes, current bytes, or both when comparing | comparison cannot support `archive_corroborated` / `archive_diverged` |
| Archive/current distinction | current-live captured bytes and pre-cutoff archive bytes are separately identified when both exist | current hash cannot prove archive visibility |
| Residual propagation | failed SP-2 does not erase SP-6 posture; SP-6 value remains a visibility record while SP-2 remains not-cleared | no fake rescue in either direction |

For `archive_corroborated`, the comparison must be recomputable over the relevant archive/current bytes or explicitly owner-bound. For `archive_only`, SP-6 may record pre-cutoff archive visibility even if SP-2 still fails; the non-clear stays in SP-2. For `current_capture_only`, a current-live hash basis can support SP-2 over current bytes but cannot establish pre-cutoff archival visibility.

## Recommendation

Recommend `TARGET_RECOMMENDED_FOR_OWNER_DECISION`: **Option A interim reader now; Option B deferred as the future canonical home after explicit owner authorization.**

Decisive criteria:

- Smallest complete intervention: Option A answers the immediate AR-01 derivation gap without entering ECR.
- Authority fit: Option B is cleaner long-term but owner-reserved; this lane cannot select it.
- Failure visibility: Option A can surface current-live-only, attempt-failed, not-attempted, and comparison residual states without pretending sufficiency.
- Reversibility: Option A can be retired when ECR consolidation lands.
- Boundary integrity: Option A must be phrased as a reader over capture/acquisition facts, not an authored ECR field.

What would change the recommendation:

- The owner explicitly authorizes ECR consolidation entry and canonical receipt field design.
- The capture-build lane re-couriers a stable capture-context field and acquisition-scope contract that materially changes the table.
- The owner authorizes a non-Judgment comparison fact sufficient for `archive_corroborated` / `archive_diverged`.
- The full ECR/EvidenceUnit consolidation supersedes this interim routing object.

## Deferred Implications

- A later owner decision should record whether Option A is accepted, amended, or rejected.
- If Option A is accepted, the follow-on artifact should patch or companion-reference the SP-6 section without changing JSG-01 gate state.
- If Option B is selected, create an ECR consolidation prompt or decision route first; do not treat this artifact as that authorization.
- Capture-build must re-courier changes to the dedicated capture-context field, acquisition receipt scope, and `hash_basis`.
- The future ECR consolidation should decide whether `source_visibility_posture` remains the name or is replaced by a receipt-owned successor.
- The future ECR consolidation should explicitly retire any JSG-01 interim rule it supersedes.

## Smallest Complete Next Routing Object

Next object: an owner-facing decision record under `docs/decisions/`, not an implementation handoff.

Minimum owner questions:

1. Approve Option A as the bounded interim JSG-01 reader rule, or explicitly authorize Option B / ECR consolidation entry.
2. Decide whether `archive_corroborated` and `archive_diverged` may be emitted from exact recomputable comparison, owner-bound comparison facts, downstream Judgment facts, or must remain residual.
3. Confirm `access_posture` remains raw residual/conflict evidence, not a closed table key.
4. Require capture-build to re-courier any capture-context, acquisition-scope, or hash_basis delta before downstream binding.

## Quality Gate Status

| Gate | Status | Evidence / boundary |
| --- | --- | --- |
| Both options developed | met_advisory | Option A and Option B developed above with owner boundaries |
| Mechanical derivation | met_advisory_with_residuals | Precedence table maps all combinations to one value or named residual |
| JSG-01 remains frozen | met_advisory | No conductor, source, schema, or gate edit; non-claims explicit |
| ECR consolidation not entered | met_advisory | Option B is deferred and owner-reserved |
| access_posture free text preserved | met_advisory | It is residual/conflict evidence only |
| SP-2 hash_basis check named | met_advisory | Separate recomputation-basis table included |
| Delta robustness | met_advisory | stale_if and residual rows cover capture-context/hash_basis re-courier deltas |
| Strict readiness / validation | not proven | Dirty/untracked controlling sources block strict claims |
| Tests | not run | Non-executing docs-only artifact; no runtime/code change |

## Non-Claims

This artifact is not:

- implementation;
- validation;
- owner ratification;
- JSG-01 unfreeze;
- ECR/EvidenceUnit consolidation;
- source schema or code change;
- source capture authorization;
- archive fetch or diff authorization;
- SP-6 sufficiency threshold;
- SP-5 finalization authority;
- Judgment materiality authority;
- fixture admission;
- judgment-quality proof;
- readiness, acceptance, commit, push, or PR.
