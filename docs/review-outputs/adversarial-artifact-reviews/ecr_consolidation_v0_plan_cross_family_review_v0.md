# ECR Consolidation v0 Plan Cross-Family Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Cross-family review of the ECR Consolidation v0 plan.
use_when:
  - Inspecting review findings and accepted friction for the consolidation plan.
  - Tracing later ECR consolidation work to this review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

```yaml
review_summary:
  recommendation: accept_with_friction
  target: docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
  patched_plan_sha256: 11D8EF33AEA7BD4734E690181265C27ED69BB48D3A9484A89DC37C864B7716A6
  patched_findings:
    - AR-01
    - AR-02
    - AR-03
  unpatched_owner_reserved:
    - OR-01
    - OR-02
    - OR-03
  source_context: SOURCE_CONTEXT_READY
  cross_family_independence: "yes - this review was run by GPT-5 against a plan attributed to Claude-family authoring"
  review_use_boundary: "decision input only; not approval, validation, ratification, readiness, JSG-01 unfreeze, or implementation authorization"
```

## Source Readiness

SOURCE_CONTEXT_READY.

- Target hash confirmed before patching: `609768AEAB398A8FDDFC2D7B5EBBC1053682E3FD366A1481B54A3E137D8EF5CF`.
- Producer state independently verified: working-tree `orca-harness/source_capture/models.py` has closed posture vocabularies, `PreservedFile.hash_basis`, and the validator (`models.py:53-66,97-114,129-143,185-199`); `git show HEAD:orca-harness/source_capture/models.py` lacks those R2 fields and validators.
- Archive dating verified: `source_quality.py` uses `_selected_snapshot_field(..., "timestamp")` at `source_quality.py:169,405-412` or `_source_time` at `source_quality.py:434-446`; `_source_time` explicitly does not derive time from `cutoff_posture`.
- Downstream recomputation surface verified: `case_models.py` has `EvidenceUnit.hash_basis` at `case_models.py:61`, while packing v3 requires source bytes or an inspectable reference so hashes can be recomputed rather than trusted (`packing_to_harness_foundation_interface_architecture_v3.md:123,135,137,178`).
- Required pinned source hashes matched for the three pinned docs: SP-6 plan `03310806...02AB`, translator `E8944D13...92B2`, posture proposal `F873C0EA...0B27`.

## Findings

### AR-01

Severity: major

Seam: three-mode binding rule / SP-6 mode assignment

Citations: `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md:52,69,107-113,160-178`; `orca-harness/source_capture/models.py:122,176`; `orca-harness/source_capture/source_quality.py:169,405-412,434-446`; `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md:173-176`.

Finding: The plan repeatedly described SP-6 as "mode-3-today" even though its own derivation table emits values where producer inputs exist and only residualizes rows where the producer lacks the comparison/date basis. Under the plan's binding rule, those derivable reads are M2; the missing comparison/date rows are M3 stops.

Minimum closure condition: The plan must describe SP-6 as an M2 derived-read with M3 residual stops, not as a wholly M3 field.

Next authorized action: patched in the plan artifact only.

Patched: yes.

### AR-02

Severity: major

Seam: D4 / no coined names / producer binding

Citations: `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md:52,151,203-205`; `docs/product/jsg01_source_side_receipt_translator_v0.md:207,252-264,443-453`; `orca-harness/source_capture/models.py:117-180`.

Finding: The plan implied the `source_visibility_posture` name was absorbed from producer vocabulary, but the producer does not store that field. The correct D4 claim is narrower: retain the existing SP-6/ECR label while binding the derivation to real Armory inputs instead of coining parallel producer vocabulary.

Minimum closure condition: The plan must distinguish the retained SP-6/ECR label from producer-owned input fields.

Next authorized action: patched in the plan artifact only.

Patched: yes.

### AR-03

Severity: minor

Seam: citation/source-grounding

Citations: `orca-harness/source_capture/models.py:122,124,176,178`; `orca-harness/source_capture/source_quality.py:169,405-412,434-446`; `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md:123,135,137,178`; `orca-harness/schemas/case_models.py:61`.

Finding: Several source references were stale or under-grounded: the A input cited line 124 for `archive_history_posture` even though that line is `re_capture_relationship`; the R input omitted packet-level `re_capture_relationship`; the M2 citation did not include the selected-snapshot lookup body; the downstream recomputation claim named packing v3 AR-03 without line-grounding what AR-03 actually requires.

Minimum closure condition: The plan must cite the exact producer lines and bridge lines supporting each claim.

Next authorized action: patched in the plan artifact only.

Patched: yes.

## Patches Applied

### Patch for AR-01

Before:

```diff
- **The slice in one line.** SP-6 is **mode-3-today**: the adopted residual-first decision table ... reduces the producer's closed ... facts to one closed value *or* a named residual ...
- | Design SP-6 as the first ECR field (source-visibility slice)? | `TARGET_RECOMMENDED` (advisory) | Instantiates the frame as a mode-3 derived value-or-residual over the producer's closed facts; ...
- | **M3 — named-residual** ... | The verified absence of any stored `source_visibility_posture` / comparison field -> SP-6 is M3 today. |
- The rule is **concrete enough** that SP-6 instantiates it (M3 today, with an M1/M2 upgrade path ...
- **What would change this:** an owner decision ... moves SP-6 from M3 toward M1/M2 ...
```

After:

```diff
+ **The slice in one line.** SP-6 is **M2-with-M3-stops today**: the adopted residual-first decision table ... reads the producer's closed ... facts, archive-date metadata/timing convention, and `PreservedFile` references to emit one closed value *or* a named residual.
+ | Design SP-6 as the first ECR field (source-visibility slice)? | `TARGET_RECOMMENDED` (advisory) | Instantiates the frame as an M2 derived-read over producer facts where inputs exist, with M3 named-residual stops where the producer lacks a recorded comparison; ...
+ | **M3 — named-residual** ... | The verified absence of any stored `source_visibility_posture` / comparison field -> SP-6's comparison-dependent rows are M3 today. |
+ The rule is **concrete enough** that SP-6 instantiates it (M2 where archive/timing/current-presence inputs exist; M3 where the producer lacks the recorded comparison or date basis) ...
+ **What would change this:** an owner decision ... moves the currently residual SP-6 rows toward M1/M2 ...
```

Grounding citations: `source_quality.py:169,405-412,434-446`; `models.py:122,176`; boundary `:173-176`; derivation table rows `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md:160-178`.

### Patch for AR-02

Before:

```diff
- ... the name is **absorbed** from the producer vocabulary (not coined) ...
- - **Field name (D4 — absorb, do not coin):** `source_visibility_posture` ...
- - **Cutoff/timing (SP-3 sibling)** ... (SP-6 reads `cutoff_posture` as an input only).
- - **How the three errors resolve.** ... `cutoff_posture` by-name collision -> resolved into one lineage (read the implemented `VisibleFact` as the `D` input; mint no same-named enum).
```

After:

```diff
+ ... The `source_visibility_posture` label is retained from the existing SP-6/ECR language, while the inputs are bound to real producer fields rather than coined in parallel ...
+ - **Field name (D4 — retain label, bind real inputs):** `source_visibility_posture` ... D4 is satisfied by binding the derivation to the real Armory fields (`archive_history_posture`, `re_capture_relationship`, timing/archive metadata, `PreservedFile`) rather than inventing parallel producer vocabulary.
+ - **Cutoff/timing (SP-3 sibling)** ... (SP-6 reads archive-date/timing convention inputs only and does not mint a same-named `cutoff_posture` enum).
+ - **How the three errors resolve.** ... `cutoff_posture` by-name collision -> resolved by keeping the producer's implemented `PacketTiming.cutoff_posture` as a real `VisibleFact` and not minting a same-named ECR enum; SP-6's `D` input uses archive-date metadata/timing convention and never treats `cutoff_posture` as a timestamp.
```

Grounding citations: translator field and adapter rows `jsg01_source_side_receipt_translator_v0.md:207,252-264`; translator DCP sweep `:443-453`; producer fields `models.py:117-180`; archive-date behavior `source_quality.py:169,405-412,434-446`.

### Patch for AR-03

Before:

```diff
- | **M1 ... | `PreservedFile.hash_basis` (`models.py:57-66,102`) carried to `EvidenceUnit.hash_basis` (`case_models.py:61`), recomputed (packing v3 AR-03). |
- | **M2 ... | An archive-date class read from `PacketTiming` / `selected_snapshot.timestamp` (`source_quality.py:169,434-446`). |
- | **A** ... | `models.py:124,176`; closed set `:54`; validators `:132-136,189-192` |
- | **R** ... | `models.py:124`; closed set `:55` |
```

After:

```diff
+ | **M1 ... | Upstream `PreservedFile.hash_basis` (`models.py:57-66,102`) plus downstream transport/recompute surfaces (`case_models.py:61`; `packing_to_harness_foundation_interface_architecture_v3.md:123,135,137,178`). |
+ | **M2 ... | An archive-date class read from `selected_snapshot.timestamp` / `PacketTiming` slice timing (`source_quality.py:169,405-412,434-446`). |
+ | **A** ... | `models.py:122,176`; closed set `:54`; validators `:132-136,188-192` |
+ | **R** ... | `models.py:124,178`; closed set `:55`; validators `:138-142,193-198` |
```

Grounding citations: `models.py:53-66,97-114,122,124,176,178,188-198`; `source_quality.py:169,405-412,434-446`; `case_models.py:61`; packing v3 `:123,135,137,178`.

## Not Patched Owner-Reserved Findings

### OR-01

Finding: AF-7 A/B choice remains owner-reserved: declare the ECR field now vs ratify only the derivation contract as a seed.

Why not patched: The prompt explicitly forbids patching owner-reserved decisions.

Minimum closure condition: Owner chooses A or B during ratification.

### OR-02

Finding: R2 / `hash_basis` remains working-tree-only and `not_proven` for strict ratification, even though the working tree has the implementation and HEAD lacks it.

Why not patched: The plan already fences this correctly after independent verification. Committing or ratifying R2 is outside this lane.

Minimum closure condition: R2 is committed, re-confirmed, and the ECR slice is rechecked against that landed state.

### OR-03

Finding: SP-6 sufficiency grade, SP-5 finalization, materiality, D2 missing-facts placement, JSG-01 unfreeze, and boundary-doc edit remain owner-reserved/downstream.

Why not patched: The prompt forbids resolving these decisions.

Minimum closure condition: Owner/downstream lanes resolve each reserved decision under their own authority.

## Non-Findings

- Scope held after patch: frame + source-visibility slice only; siblings remain named-but-deferred.
- D1 residual routing held: rows 7-8 do not fire to values today because no producer comparison field exists; row 9 remains the live path.
- D3 fence held: upstream `PreservedFile.hash_basis` is treated as advisory working-tree state, not landed or settled.
- D4 improved: real Armory inputs are bound without minting a same-named producer field.
- Supersession boundary held: the plan describes translator supersession; it does not edit the translator, boundary doc, obligation contract, code, or JSG-01 consumer.

## Updated Artifact

- Patched plan path: `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
- New SHA256 from fresh read: `11D8EF33AEA7BD4734E690181265C27ED69BB48D3A9484A89DC37C864B7716A6`
- Source patch scope: only the target plan artifact was patched. This report was written under the required review output path. The wider worktree was dirty before this review, so no clean-worktree claim is made.

Review-use boundary: findings and patches are decision input only. They do not approve, validate, ratify, unfreeze JSG-01, land R2, edit the boundary doc, or authorize implementation.
