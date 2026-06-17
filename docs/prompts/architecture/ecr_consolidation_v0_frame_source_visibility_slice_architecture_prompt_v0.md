# ECR Consolidation v0 — Frame + Source-Visibility Slice — Architecture Planning Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: >
  Architecture-planning prompt to OPEN the owner-reserved ECR/EvidenceUnit
  consolidation, BOUNDED to the smallest-complete increment: a thin ECR frame
  plus the source-visibility slice (SP-6). Non-executing; 3-subagent fan-out;
  designs only the frame + slice, leaving sibling ECR fields named-but-deferred.
use_when:
  - Running or dispatching the bounded ECR-consolidation-v0 architecture decision.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md
input_hashes:
  docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md: 03310806D8B4475CC281FF65F2247B59702D3B4036DF6C38A9A1383EDB7102AB
  docs/product/jsg01_source_side_receipt_translator_v0.md: E8944D13FF8B3FAF62AC24209EC50FDA7C03CC9D4F906687246B2E15C01592B2
  docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md: F873C0EA9B61135971058B517DF0C220569FAFDA032D9407B2073216D8920B27
branch_or_commit: main @ e4e854e (authored). Re-verified at d69aeee (+2 capture-lane commits; worktree dirty). R2 (posture-vocabulary closure + PreservedFile.hash_basis) is PRESENT-BUT-UNCOMMITTED in the working tree as of 2026-06-05 (absent from HEAD) — VERIFY source_capture/* against the live working tree; do not trust producer facts restated in this prompt.
```

## Commission

Design **ECR consolidation v0**, bounded to two parts and nothing more:

1. **A thin ECR frame** — the minimal skeleton that lets one field be designed without pre-committing the rest: a canonical (at least provisional) ECR object name; the layering invariants (capture *produces facts* → ECR *receipts/derives* → packing → harness *consumes carried references*); the **binding rule** (how a capture fact becomes an ECR field); and the sibling ECR field areas enumerated **named-but-deferred**.
2. **The source-visibility slice** — SP-6 `source_visibility_posture` as the first authored ECR field, whose derivation spec is the residual-first decision table from the adopted SP-6 plan, deriving from upstream `SourceCapturePacket` facts, with the recomputation basis upstream-owned and carried.

Output is a **non-executing architecture routing object**: the frame, the slice, adversarial findings, a recommendation, deferred implications, and the smallest complete next step (independent review → owner ratification + boundary-doc update + DCP).

## Locked decisions (build against these; do not relitigate)

- **The ECR consolidation is OPENED by the owner, scoped to the source-visibility slice.** Smallest-complete = frame + slice. The **full field-architecture consolidation is OUT of scope** (overbuild) — design siblings only as named-deferred placeholders.
  - **Open provenance (a re-run must verify, not assume):** the open is a **current-turn owner instruction**, not yet recorded in a controlling source. The boundary doc (`core_spine_v0_data_and_cleaning_spine_boundary_v0.md:281-309`) and the SP-6 plan still record the consolidation as **owner-reserved / not entered**. A fresh re-run may treat the open as authorized only by an owner present in-thread, or by a cited decision artifact once one exists; recording it (decision artifact + boundary-doc edit + `direction_change_propagation`) is part of the later owner-gated **ratification**, not this lane.
  - **Field-vs-contract sub-choice (surface, do not freeze):** authoring SP-6 "as an ECR field" provisionally assumes the owner-reserved question *"is ECR the canonical object that hosts fields?"* (`...boundary_v0.md:283-284,298`). Keep the object name **provisional**; the strictly-smaller increment — authoring only the **derivation contract** (the residual-first table as the seed) and deferring the field declaration — is a legitimate owner sub-choice to surface at ratification.
- **D3 (locked):** the verifiability basis is **upstream-owned** (`SourceCapturePacket` preserved bytes + acquisition receipt) and **carried downstream as a reference** — never re-authored at the harness `EvidenceUnit` layer.
- **Facts stay capture-side.** R2 (posture-vocabulary closure + `PreservedFile.hash_basis`) is **present-but-uncommitted in the working tree** (verify; treat as advisory / `not_proven`, not landed); the comparison/archive-dating facts are produced by the Armory (upstream-owned). The ECR slice **references/derives** from them; it does **not** author new capture facts.
- **D1 (accepted):** SP-6 is only partially mechanically derivable today — `archive_corroborated`/`archive_diverged` need a recorded comparison the producer does not store, and materiality is downstream Judgment. The slice emits **named residuals** there; it does not invent the comparison.
- **D4 (accepted):** bind the real Armory fields (`access_posture`, `archive_history_posture`, `re_capture_relationship`, `PreservedFile`), never coin parallel names.

## Authorization / boundary (read first)

- **Design-only, NON-EXECUTING.** No code, schema, obligation-contract, or boundary-doc edits. The lane produces the design; the boundary-doc update + DCP receipt + ratification are a **later owner-gated step**.
- **BOUNDED — overbuild guard.** Design only the frame + source-visibility slice. Sibling ECR fields are **named-but-deferred**, never designed. If the slice cannot be designed without designing a sibling, **STOP and flag** — do not expand scope to the full consolidation.
- **Premature-freeze guard.** The frame must be holistic enough that the slice does not pre-commit sibling field shapes; the slice must be consistent with the eventual full consolidation.
- **JSG-01 stays FROZEN.** This does not unfreeze, bind, or ratify it.
- **Owner-reserved (not for the lane):** the full ECR field architecture (siblings); JSG-01 unfreeze; SP-5 finalization authority; the SP-6 sufficiency grade; the actual boundary-doc edit/ratification.
- No `jb` import; `agent-workflow` is reusable mechanics only.

## Thread operating target continuity

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: >
    Foundation step for the frozen JSG-01 source-side gate: the owner opened the
    reserved ECR consolidation, scoped to source-visibility, so SP-6 gets a
    proper (non-throwaway) home with the correct upstream binding. Orientation
    only; not authority, readiness, or JSG-01 unfreeze.
```

## Preflight (orca_start_preflight)

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: docs-write   # the architecture PLAN only; read-only for all source/code/contract
  target_scope: [docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md]
  dirty_state_checked: required_yes
  blocked_if_missing: yes
controlling_source_state: worktree dirty; controlling sources untracked/modified → advisory planning only; no strict readiness/acceptance/ratification claim.
doctrine_note: opening the consolidation flips the boundary doc's reserved-consolidation status; that edit + a direction_change_propagation receipt are a LATER owner-gated ratification step, not done by this design lane.
external_source_boundary: agent-workflow reusable mechanics only; jb is NOT Orca authority.
```

## Source pack / required reads (broadened — include the implemented producer)

- **Slice spec:** `docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` (SHA `03310806…02AB`) — the residual-first SP-6 decision table + the SP-2/hash_basis finding.
- **Reserved-consolidation source:** `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` — the deferred ECR questions (:281-309), the Inclusion State Rule, canonical-vs-working name.
- **What SP-6 supersedes:** `docs/product/jsg01_source_side_receipt_translator_v0.md` (SHA `E8944D13…92B2`) — SP-6 def + the duplication/collision the slice resolves.
- **Capture-side facts (referenced, not authored):** `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` (SHA `F873C0EA…0B27`); obligation contract Ob.7-16.
- **Implemented producer (READ — the blind-spot fix; VERIFY against the live working tree, do not trust facts restated here):** `orca-harness/source_capture/models.py` (`SourceCapturePacket`, `VisibleFact`, `PreservedFile`, `SourceCaptureSlice`, `PacketTiming`), `source_quality.py` (archive dating via `archive_availability.selected_snapshot.timestamp` then `_source_time`, which is decoupled from `cutoff_posture` — "a posture is not a time"), `packet_assembly.py` (posture-honesty validator). **Producer state at re-verification (d69aeee + dirty; UNCOMMITTED → advisory, re-confirm):** R2 has landed in the working tree — `PreservedFile.hash_basis` EXISTS (closed to `{raw_stored_bytes}`, AR-04-bound) and Ob.9/Ob.10/Ob.15 posture vocabularies are enforced at write-time. STILL ABSENT: any stored `source_visibility_posture` and any recorded archive-vs-current comparison field (so D1 holds). The producer is dirty/concurrently-changing and is intentionally **not SHA-pinned** (the three docs above are pinned because they are stable; the producer is not) — re-read it before relying on any producer fact.
- **Downstream carried-reference target:** `orca-harness/schemas/case_models.py` (`EvidenceUnit.hash_basis`).
- **The three representations to account for in the frame (not all design):** IPF Evidence Unit standard (`core_spine_v0_information_production_foundation_v0.md`), the harness pydantic (`pydantic_schema_reference.md`), and `SourceCapturePacket`.
- **Capture→harness path:** `packing_to_harness_foundation_interface_architecture_v3.md` (finalization owner-reserved; the missing capture→EvidenceUnit bridge).

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, prompt-orchestration, source-of-truth).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-architecture-planning`. Do not APPLY yet.
3. `SOURCE-LOAD` the pack.
4. Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE`.
5. APPLY deep-thinking to frame failure modes, then architecture-planning to design the frame + slice and name the routing object.

## Subagents — 3 standard (general-purpose), explicitly authorized

Each receives the source pack (or runs its own source-readiness gate), does source-backed work, applies no method before `SOURCE_CONTEXT_READY`, and discloses its approach. Advisory only; the lane synthesizes and owns the routing object.

- **SA-1 — ECR frame architect:** the thin skeleton — canonical object name (provisional), layering invariants, the upstream-owned/carried binding rule (D3), sibling field areas named-but-deferred, and how the frame coherently *accounts for* (without designing) the IPF / pydantic / SourceCapturePacket representations.
- **SA-2 — source-visibility slice architect:** SP-6 as the first ECR field — the residual-first derivation (from the adopted plan), the upstream references to Armory facts, the recomputation basis (upstream-owned/carried), and how the interim translator SP-6 is superseded by this.
- **SA-3 — adversary / integrator:** attack both — premature-freeze (does the slice pre-commit siblings?), scope creep (does it drift toward the full consolidation?), layer violation (any downstream re-authoring, any new capture fact designed here, any break of upstream-owned), JSG-01-frozen integrity, residual leakage (finalization/sufficiency staying owner-reserved), and whether the slice is consistent with the eventual full consolidation. Propose the smallest-complete synthesis + the next routing object.

The lane synthesizes SA-1..SA-3. It must keep the result within the locked scope.

## Output (non-executing architecture routing object)

- The **ECR frame**: object name (provisional), layering invariants, the binding rule, sibling areas named-but-deferred, representation accounting.
- The **source-visibility slice**: SP-6 as an ECR field, its derivation spec (residual-first), upstream references, basis (upstream-owned/carried), supersession of the interim translator SP-6.
- Adversarial findings; recommendation with decisive criteria.
- **Deferred implications:** the capture→ECR→harness bridge; the sibling ECR fields; the capture-side comparison/archive-dating facts; the boundary-doc update + DCP at ratification.
- The **smallest complete next routing object** (→ independent cross-family review → owner ratification).

Output mode: `file-write` (exactly one mode) the plan to `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`. **No** source/code/schema/contract/boundary-doc change. Do not execute implementation.

## Quality gates (must be able to fail)

- Frame is holistic enough to host the slice **without** pre-committing sibling field shapes.
- Slice designs **only** source-visibility; siblings named-deferred, not designed.
- **No scope creep** into the full consolidation (overbuild guard held).
- Upstream-owned/carried binding (D3) preserved; no downstream re-authoring; no new capture fact authored here (facts referenced as capture-owned).
- The three representations (IPF / pydantic / SourceCapturePacket) are coherently *accounted for* in the frame without designing all their fields.
- JSG-01 not unfrozen; finalization + sufficiency grade left owner-reserved; SP-6 partial-mechanicalness (D1) preserved as residuals.

## Non-claims

Architecture-planning / design only. Not implementation, validation, ratification, JSG-01 unfreeze, the full ECR field architecture, the boundary-doc edit, the sufficiency threshold, or finalization authority. Opening the consolidation is owner-authorized **scoped to source-visibility**; this lane designs that scoped increment and nothing wider.

## Patch history

- **v0 patch (2026-06-05), from the adversarial artifact review** (`docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_adversarial_review_v0.md`, `recommendation: patch_before_acceptance`), adjudicated and applied under owner-delegated final authority. Closed: **PR-01** — corrected the false "`PreservedFile` — no `hash_basis`" producer fact, characterized R2 as present-but-uncommitted, flagged the dirty producer as not-SHA-pinned / verify-against-tree; **PR-02** — added open-provenance (current-turn owner instruction; controlling sources still reserve it; recording deferred to ratification); **PR-03** — flagged the ECR-object presupposition + the field-vs-derivation-contract owner sub-choice; **PR-04** — bound exactly one output mode + the exact plan path. Deferred: **OH-1** (optional; inline SP-6-plan restatement left as-is, mitigated by the hash-pin). This patch corrects prompt accuracy only; it changes no product / architecture / workflow / validation / review / output / lifecycle doctrine, so no `direction_change_propagation` receipt is required. JSG-01 stays frozen; the consolidation open + boundary-doc edit + DCP remain the later owner-gated ratification step. The existing synthesized plan (`docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`, prior session, untracked) already reflects these corrections and needs no rework from this patch.
```
