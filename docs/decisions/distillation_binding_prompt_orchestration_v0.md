# Distillation Binding — Prompt-Orchestration Harness (prepare-only draft)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: per-spine distillation binding for the Orca prompt-orchestration harness (prompts, wrappers, handoffs, reviews, reruns, patches)
use_when:
  - Distilling a prompt-orchestration lesson into a carried rule.
  - Reasoning about output-mode/chat topology, review-report write failure, or source-heavy compaction.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
```

**Status: PREPARE-ONLY DRAFT** (see the index). Distills recorded prompt-orchestration outcomes,
several of which are already written as validation gates whose wording names the concrete failure
they prevent (a recorded-outcome source per the doctrine). Reads recorded outcomes; edits no overlay
or prompt file.

**Currentness note (2026-07-17):** This retrieval-only draft preserves the
recorded incidents, but the source-heavy unit-seal blocker and
thread-operating-target continuity node were retired as standing Forseti
behavior by the SCI behavioral-authority pass. Current source-heavy evidence
preservation is owned by `.agents/workflow-overlay/prompt-orchestration.md`;
goal continuity uses the visible active goal or accepted next objective. Do
not execute those historical cells below as live gates.

## Harness bound

The agent authoring Orca prompt artifacts (full prompts, thin wrappers, handoffs, review prompts,
reruns, patch prompts) under `prompt-orchestration.md` + `communication-style.md`. Decision nodes are
the output-mode choice, the chat-topology choice, and the source-heavy unit seal.

## Pole / key finding

**Actor-carried, with a checkable shell.** Most cells are judgment (which output mode, is the chat
topology contradictory, did the unit seal before compaction); a schema can check the *shape* of a
receipt but never its *truth* (EP-08…EP-11 PARTIAL in the EP classification). Two cells turn on a
typed `BLOCKED_*` boundary, which is the partial substrate.

## A1 — outcome → cell pairs (real, cited)

### GUARD review-report-failed-write  (actor-carried; PARTIAL shell)
- decision_node: `node:review-report-output`
- `GUARD review-report-failed-write: WHEN a review-report durable write fails → emit status: failed, recommendation: blocked, review_location: chat_only_current_thread, and NO report_path → UNLESS the durable write succeeded.`
- outcome_class: a failed durable write is reported as a successful review (a false-success path) or emits a `report_path` to a file that does not exist
- causal_miss: missing case — the write-failure branch of the review-report contract
- verification: under-case (write fails) → `status: failed` + no `report_path`; over-edge (write succeeds) → normal receipt with a valid `report_path`
- substrate: actor-carried; PARTIAL — a schema can check `report_path` exists ⇔ file present
- PROV: `validation-gates.md` → Review-report topology gate: "failed durable writes use `status: failed`, `recommendation: blocked`, `review_location: chat_only_current_thread`, and no `report_path`". tier: accepted-orca-gate.

### GUARD chat-topology-no-collision  (actor-carried)
- decision_node: `node:chat-output-topology`
- `GUARD chat-topology-no-collision: WHEN patching chat-output shape → check for contradiction between the general human-summary-first rule (communication-style) and the output-mode exceptions (prompt-orchestration) → UNLESS no chat-shape change is made.`
- outcome_class: an agent flags valid YAML-only `review-report` chat as a violation (or strips required prose) because the general rule and the exception disagree with no cross-pointer
- causal_miss: missing trigger — the general rule and its exceptions are owned in two files with no bidirectional reference
- verification: under-case (a chat-shape patch) → collision check run; over-edge (no chat-shape change) → not required
- substrate: actor-carried (a collision gate, not a key checklist)
- PROV: `validation-gates.md` → Chat-output topology gate; recorded review `docs/review-outputs/adversarial-artifact-reviews/orca_chat_output_contract_phase_plan_adversarial_review_v0.md`. tier: accepted-orca-gate.

### GUARD compaction-before-seal  (actor-carried; typed-token PARTIAL)
- decision_node: `node:source-heavy-unit-seal`
- `GUARD compaction-before-seal: WHEN context compacts before the current source-heavy unit artifact is written and hashed → stop as BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL and treat partial outputs as contaminated scratch → UNLESS the unit was already sealed (written + hashed).`
- outcome_class: a source-heavy unit's partial outputs survive a compaction and are silently trusted as if sealed
- causal_miss: missing boundary — "written and hashed" is the seal; pre-seal partials are contaminated
- verification: under-case (compaction mid-unit) → `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL`; over-edge (unit sealed first) → proceed
- substrate: actor-carried; PARTIAL — the typed `BLOCKED_*` token rejects the class once raised (the canonical home of this token)
- PROV: `validation-gates.md` → Compaction-before-seal gate: "the run must stop as `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL`; any partial outputs from that unit are contaminated scratch until archived or cleanly rerun". tier: accepted-orca-gate.

## A2 — core size / budget

Actor-carried; cells compete for budget. `review-report-failed-write` and `compaction-before-seal`
are `silent-wrong-output`-class (false success / silently-trusted contaminated unit) → prune-exempt
from frequency-only retirement. Budget model-dependent; not fixed here.

## A3 — spine / decision nodes

`node:output-mode-selection` · `node:role-binding` · `node:start-preflight` · `node:review-report-output`
· `node:chat-output-topology` · `node:source-heavy-unit-seal` · `node:thread-operating-target-continuity`.
Cells index by `decision_node`.

## A4 — slots filled

- **intervention-type set** (closed; owner-extensible): `GUARD`, `SCHEMA-GATE` (receipt shape), `SOURCE-RULE`, `TOKEN` (typed `BLOCKED_*`).
- **verification substrate**: proposed receipt-shape schemas (EP-08…EP-11, owner-gated, not built); the typed `BLOCKED_*` token; otherwise prompt-validation review.
- **fire-log capability**: MODERATE — prompt-validation verdicts and review findings record gate hits, but there is no automated firing log yet; a write-time prompt-shape checker would be the substrate.
- **tier enum**: {accepted-orca-gate, probed, asserted}.
- **review window**: owner sets (per prompt-policy patch / template change).
- **owner map**: the prompt-orchestration owner.

## Secondary finding

Several of this spine's strongest lessons are *already* gates whose wording names the failure — the
distillation here is to read each as a `LESSON` cell at its decision node and (for the checkable
shell) classify it substrate-first, leaving the truth resident.

## Scaffold (no cell invented)

The thread-operating-target continuity gate names a "prompt-quality defect" but no commit records a
concrete instance; it is a slot (codified rule), not distilled as a recorded-outcome cell here.
EP-08/09/10/11 receipt-shape schemas are proposed-not-built (owner-gated).

## Non-claims

Prepare-only; edits no overlay or prompt file; not validation, readiness, approval, or
source-of-truth promotion; placement is not authority.
```
