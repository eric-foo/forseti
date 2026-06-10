# Packing Phase To v0.14 Judgment Harness Foundation Interface Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Docs-only target architecture for the interface between the Packing Phase and the v0.14 Judgment Harness Foundation.
use_when:
  - Deciding what Packing must produce before a case can be admitted to the v0.14 Judgment Harness.
  - Checking which fields, hashes, gates, and labels the Harness Foundation freezes versus which Packing constructs.
  - Separating Packing responsibilities from Cleaning, Data Capture, Facilitator labeling, scoring, probe execution, and lesson promotion.
  - Preparing or rejecting one case before harness execution without re-deriving the boundary.
authority_boundary: retrieval_only
open_next:
  - docs/research/packing-phase/README.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
  - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
  - docs/prompts/deep-thinking/packing_to_harness_foundation_interface_architecture_ca_prompt_v0.md
input_hashes:
  docs/research/packing-phase/README.md: E108281113DA1C27DB241BBB600B19D79334CB407707C6234EE1E1264626EF06
  docs/research/judgment-spine/harness/v0_14/index.md: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 4AF1F45964DBB560D7C6E02827BC30A9161D4433EA754580239C122DAEF532A5
branch_or_commit: main @ b7627d3 (dirty pre-existing workspace state allowed and reported)
supersedes: prior untracked v0 at this path (hash 4DF970A81C3711957470BE7B306050FF0E7FD09FC96EA0159DC0DA038BC1EC7C, never committed); replaced under explicit current-turn owner authorization
stale_if:
  - v0.14 Judgment Harness spec is superseded by v0.15 or later.
  - Pydantic FacilitatorLedger schema expands to include case_family, decision_shape, memorization_probe_required, or known_fame_risk as first-class fields.
  - Packing-phase README scope changes to absorb facilitator labeling or to release evidence-registry shape.
  - Core Spine Data Capture / Cleaning boundary note materially reassigns layer ownership.
  - A second non-Unity fixture exposes a generic interface field missing from this decision.
  - A later owner decision authorizes a different bundle topology or a different admission gate.
```

- Status: TARGET_RECOMMENDED
- Artifact type: Architecture planning artifact
- Output mode used: file-write
- Implementation authorized: no
- Runtime, package, test, schema-as-code, hashing routine, probe runner, leakage validator, sealed-memo adapter generator, automation, commit, push, PR, model run, probe execution, scoring execution, validation execution, proof run, product proof, or lesson promotion authorized: no
- Strict acceptance, validation, readiness, source-of-truth promotion, implementation authorization, probe pass, score-readiness, harness superiority, baseline comparability, semantic evidence support, buyer proof, feature readiness, commercial readiness, or memory-compounding claims: not proven

## Source Context Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Packing README, v0.14 harness index, bridge foundation, Unity extraction plan, judgment-spine thesis operating contract, judgement_case_construction_protocol, pydantic_schema_reference, blind_judgement_schema_and_harness_protocol, band_input_labeling_rubric, memorization_probe_protocol, failure_event_log_spec, proof_and_memory_plan, judgment-spine manifest, and the Core Spine Data Capture / Cleaning boundary note
  edit_permission: docs-write
  target_scope: Replace docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v0.md under explicit current-turn owner authorization, and save the commissioning prompt at docs/prompts/deep-thinking/packing_to_harness_foundation_interface_architecture_ca_prompt_v0.md.
  dirty_state_checked: yes
  blocked_if_missing: no
workspace_preflight:
  expected_branch: main
  actual_branch: main
  expected_head: b7627d3
  actual_head: b7627d3389eeaa8456c65974039ada0e519617bc
  dirty_state: allowed_and_reported
source_context_status: SOURCE_CONTEXT_READY
method_sequence:
  workflow_architecture_planning_reference_loaded: yes
  applied_only_after_source_context_ready: yes
  profile: standard
  subagents_launched: 3
collision_resolution:
  prior_v0_hash: 4DF970A81C3711957470BE7B306050FF0E7FD09FC96EA0159DC0DA038BC1EC7C
  prior_v0_mtime: 2026-05-28 04:45:27 local
  prior_v0_git_state: untracked, never committed
  collision_action: replace_v0_under_explicit_current_turn_owner_authorization
  rationale: prior v0 was content-equivalent on the architecture decision (TARGET_RECOMMENDED, block-first hybrid Harness Entry Bundle); fresh adversarial subagent pass surfaced four sharpenings folded into this replacement instead of bumping to v1
```

Repository state caveat: `git status` reported `main` at `b7627d3`, ahead of `origin/main` by 17 commits, with modified overlay control files, modified `docs/workflows/orca_repo_map_v0.md`, and many untracked Judgment Spine, Packing, prompt, review, product, and Unity fixture files. The prior v0 at the target path was untracked and never committed. Dirty and untracked state supports this bounded working architecture artifact, but does not prove acceptance, validation, readiness, source-of-truth promotion, implementation authorization, probe pass, score-readiness, or proof claims.

All five prompt-pinned task-source hashes matched. The five hashes above were verified by `sha256sum` against the prompt before APPLY. Sub-files under v0.14 were read targeted from the v0.14 index. `phase_1_infrastructure_architecture.md`, `changelog.md`, `action_band_mapping_table_numbers.md`, `action_band_mapping_executable_spec.md`, and `scorer_formula_spec.md` were not loaded because the bridge foundation and Unity extraction plan already extract the relevant interface and deferred-implementation implications; opening them would not change this architecture result and would widen the source-loading budget without benefit. Concrete exemplar fixture artifacts under `fixtures/unity_runtime_fee_2023_v0_14/` and the participant-packet draft, evidence-registry draft, facilitator-ledger draft, and sealed-memo adapter note named as optional in the prompt were not opened; the Unity extraction plan already exercises the interface against Unity, and reading the drafts would not change the option ranking.

## Consumed Goal Fit Check

The supplied `goal_handoff` maps to the loaded source pack as follows:

- `long_term_goal` ("Build Orca's Judgment Spine into a trustworthy harness for improving frontier-LLM judgment through clean case inputs, bounded blind judgments, deterministic scoring, and failure logs without fake validation or product-proof claims") is preserved as horizon context. It is not permission to broaden into product proof, runtime implementation, source-of-truth promotion, or harness superiority.
- `anchor_goal` ("Define the Packing -> Harness Foundation interface so future CAs/operators know what Packing must produce, what the harness freezes and scores, what remains blocked, and how phase ownership is preserved") is the bounding architecture question. It is satisfied below by the `Target Architecture`, `Packing-Owned Outputs`, `Harness-Owned Freeze Inputs`, and `Inadmissibility / Block States` sections.
- `success_signal` ("A future CA or operator can prepare or reject one case before harness execution by checking explicit Packing outputs, Harness freeze inputs, contestant visibility, deterministic checks, report meaning, inadmissibility states, and non-claims") is satisfied by `Packing-Owned Outputs`, `Harness-Owned Freeze Inputs`, `Contestant-Visible Boundary`, `Deterministic Scoring And Checking Boundary`, `Report Meaning And Non-Meaning`, `Inadmissibility / Block States`, and `Non-Claims`.
- `thread_operating_target` continuity: this is the same workstream as the bridge foundation and the Unity extraction plan; the anchor goal is carried forward verbatim. No conflict with the supplied handoff was found. No `BLOCKED_GOAL_CONFLICT`.

Drift guard observed: this artifact does not substitute Unity fixture polish, broad harness implementation, or template/overlay hygiene for the interface decision.

## Subagent Evidence Disclosure

```text
Subagents launched: 3
Evidence mode: delegated lane subagents (directional, adversarial, grounding)
Delegation runtime: inherited/default agent type and model (general-purpose)
Reason: prompt explicitly required exactly three advisory architecture subagents under standard profile; host supports subagents.
```

Each subagent received the same bounded source pack used here and was instructed to return advisory input only. None of the subagent outputs is a verdict, implementation authority, validation evidence, readiness evidence, or proof. The main planner owns synthesis below.

### Directional Subagent Summary

Recommended Option 5 (Hybrid: Packing owns bundle construction; Harness owns freeze/admission/scoring contract; small adapter layer for case-specific gaps). Anchored the recommendation in the explicit Packing README handoff boundary ("the harness should consume frozen or explicitly draft-labeled packet artifacts from the Packing Phase" and "should block or mark the input draft-only" rather than "silently repair upstream preparation by acting as Data Capture, Cleaning, or Packing"), in the Core Spine layer table that already assigns Cleaning/ECR/Judgment ownership, and in the v0.14 Pydantic schema surface (`ParticipantPacket` frontmatter, `EvidenceUnit`, `FacilitatorLedger`, `BlindJudgement` run-config inputs, `MemorizationProbe`, `FailureEvent`). Named core (Harness-owned: schemas, ledger freeze hash, mapping, scorer, probe gate, append-only failure logger), satellite (Packing-owned: packet body, source manifest, evidence-unit population, leakage seed content, draft work queues), and a small adapter layer for sealed memos and protocol-only fixture metadata (`case_family`, `decision_shape`, `memorization_probe_required`, `known_fame_risk`).

### Adversarial Subagent Summary

Returned nine attacks against the likely target:

- A1 Version-coupling: bundle interface is silently v0.14-shaped; v0.15/v1 would invalidate it.
- A2 Boundary leakage: assigning `pre_decision_status: excluded` and `pre_decision_basis` inside Packing is a decision-use exclusion call, which the Core Spine boundary note locates in Judgment, not Packing.
- A3 Fake-success: an admissible bundle can satisfy structural shape while leakage, hashes, or probes are stub-valued; blocking labels currently live in receipt prose, not schema.
- A4 Hidden implementation gravity: at least five executable components (freeze-hash routine, probe runner, sealed-memo adapter, evidence-unit converter, leakage validator) are implied without authorization.
- A5 Unity overfitting: the bundle has sealed-memo and fame-risk slots tuned for Unity; Daimler has none of them; non-Tier-0 cases have less.
- A6 Pydantic-vs-protocol drift: `case_family`, `decision_shape`, `memorization_probe_required`, `known_fame_risk` are in the protocol but absent from current Pydantic `FacilitatorLedger`; routing them via `leakage_audit_notes` papers over the gap.
- A7 Sealed-memo back door: "advisory baseline" labels weaken under run-time pressure and could let author-context contamination enter Phase 1 comparisons.
- A8 Inadmissibility is narrative, not enforcing: acceptance criteria live in prose bullets, not in raisers.
- A9 Lesson-promotion drift via Packing must-address candidates that become scoring truth at freeze.

Each attack named a minimum safe condition; A1 was flagged as possibly unfixable inside any v0.14-shaped architecture without deferring most interesting decisions to the adapter layer.

### Grounding Subagent Summary

Named six irreducible interface items: participant packet handoff with frozen frontmatter, participant packet hash, evidence registry as `EvidenceUnit` list with provenance fields, leakage seed inputs (`memorization_probe_required`, `known_fame_risk` plus anti-leakage/exclusion notes), explicit negative-content notice for what participants must not see, and a draft-vs-frozen marker. Cut from the interface contract: facilitator ledger contents (operator-authored later), memorization probe execution, sealed-memo adapter as general obligation, contestant run metadata, scoring and failure-event shapes, cleaning trace. Deferred to per-case adapters: EU-08-style source-visibility-gap handling, `decision_shape` selection, `case_family` choice, author-context contamination handling for any preexisting memo, parent-only material exclusions, Daimler-fallback routing. Bloat-avoidance reminders: do not invent a new leakage artifact, packing validator, packing scorer, evidence schema, ladder/judgement-class vocab, packing-side hashing, packing-side contestant runner. Recommended pointer updates limited to Packing README `open_next` and the v0.14 index Bridge Foundation table; explicitly skip manifest update and repo-map rewrite. Smallest complete next routing object: this architecture artifact. Reversibility notes: keep the artifact phrased in "v0.14 currently requires" terms with a `stale_if` clause; treating `EvidenceUnit`, `BandInputs`, or `judgement_class_ladder_mapping` as universal Packing outputs would lock Orca into a v0.14-shaped bundle.

## Architecture Frame

### Stated Architecture Question

What target architecture should govern the boundary between Packing Phase outputs and Judgment Harness Foundation inputs so that Packing can transform cleaned evidence into judgment-ready case artifacts, Harness can freeze inputs and run deterministic checks without absorbing Packing / Cleaning / Data Capture / lesson-promotion responsibilities, future implementation scoping has a stable interface, and missing provenance, leakage, unresolved evidence adapters, or missing labels block admission instead of being silently repaired by the harness.

### Inferred Architecture Question

Whether the interface is a single bundle handoff (Packing -> Harness), a two-stage handoff with an explicit operator-driven Facilitator labeling step in between, or a multi-layer cascade. The adversarial A2 finding and the band-input labeling rubric force the inference that a Facilitator labeling step exists between Packing draft outputs and Harness admission, even though it is not Packing-owned and not Harness-Foundation-owned.

### Target Actor And Downstream Consumer

- Packing operator: produces draft bundle outputs from cleaned evidence and case-frame source material.
- Facilitator / labeling operator (may be the same human, or a separate role; uses `band_input_labeling_rubric.md` and second-labeler workflow): converts Packing drafts into a frozen facilitator ledger and freezes hashes.
- Memorization-probe operator: runs probes per target contestant/model family before any contestant sees the packet.
- Harness Foundation: validates schemas, recomputes hashes, applies admission gate, executes deterministic action-band derivation and scoring, logs failures.
- Future implementation-scoping lane: consumes this artifact to bind a single bounded scope.
- Future CA or operator preparing one case: consumes this artifact to check that the case is harness-eligible or to reject it.

### Current Workaround And Current Architecture

Currently:

- The Packing README names the layer boundary in prose but does not freeze the interface object.
- The bridge foundation names the minimum harness-entry shape per surface and selects Unity as the first bridge-from-existing-material candidate.
- The Unity extraction plan exercises the interface against Unity and exposes specific surfaces and adapter gaps.
- The v0.14 spec freezes Pydantic schemas, mapping, scoring, probe, and failure-log behavior, but does not name a single interface artifact between Packing and Harness Foundation.
- No fully-frozen Harness Entry Bundle exists for any case; the Unity draft fixture pack is explicitly blocked before scoring.

Without this artifact, future CAs and operators must re-derive the boundary from three prose sources plus seven v0.14 spec files. The Unity extraction plan compresses the derivation but is case-specific.

### Decision Pressure And Why Now

The bridge foundation and Unity extraction plan have done case-level exercise of the boundary. Without a case-neutral interface artifact, every future bridge (Daimler, future cases, non-Tier-0 cases) repeats the derivation, with case-specific drift risk. A bounded interface artifact now lowers retrieval cost for future operators and clarifies which parts of the Unity-derived shape are general versus Unity-specific.

### Constraints, Non-Goals, Rejected Scope, Forbidden Paths

Constraints:

- Docs-only. No source edits beyond this artifact, the saved commissioning prompt, and at most narrow discovery pointers.
- No implementation, no schemas-as-code, no freeze-hash routine, no probe runner, no leakage validator, no sealed-memo adapter generator, no model runs, no scoring runs, no validation claims.
- No source-of-truth promotion, no acceptance, no readiness, no product proof, no buyer proof, no lesson promotion, no harness superiority claim, no memory compounding claim.
- No widening of layer ownership: Cleaning, Data Capture, Evidence Candidate Record, and lesson promotion stay where Core Spine and the thesis operating contract already place them.

Non-goals:

- Not a complete Harness Entry Bundle schema-as-code.
- Not an admission-gate Python contract.
- Not a Packing-side runtime.
- Not a case-selection policy.
- Not a Daimler decision.
- Not a probe runner specification beyond what `memorization_probe_protocol.md` already freezes.
- Not a re-litigation of v0.14 Pydantic schemas.

Rejected scope:

- Forcing Packing to own facilitator labeling under the labeling rubric.
- Forcing Harness Foundation to own draft packet construction, sealed-memo adaptation, or leakage seed authoring.
- Inventing a parallel evidence schema or parallel ledger schema.
- Promoting `case_family`, `decision_shape`, `memorization_probe_required`, or `known_fame_risk` into the Pydantic `FacilitatorLedger` in this artifact (owner decision required, see `What Is Intentionally Undecided`).
- Inventing a Packing-side superiority, comparability, or proof surface.

### Source Gaps

- Pydantic `FacilitatorLedger` does not currently carry `case_family`, `decision_shape`, `memorization_probe_required`, or `known_fame_risk`; the case construction protocol and the Unity extraction plan name these as required protocol metadata. This artifact treats them as protocol-only metadata routed through a named adapter slot pending an owner decision.
- The judgement_case_construction_protocol describes the facilitator ledger as "visible to scorer/operator only" but does not assign the labeling-workflow actor to either Packing or Harness Foundation. The band-input labeling rubric assigns it to operator-with-second-labeler. This artifact names that step as a Facilitator role between Packing draft outputs and Harness admission.
- No v0.14 spec file defines a single Harness Entry Bundle object. This artifact defines it as a named handoff surface, not as a new file shape.
- No v0.14 source defines machine-enforced admission gates; current acceptance criteria are prose bullets. This artifact names the required end state without authorizing the validators.

## Questions This Architecture Decision Must Answer

1. What does Packing produce, and what does it deliberately not produce?
2. What does the Harness Foundation freeze and check, and what does it deliberately not do?
3. Which fields are visible to contestants and which are facilitator-only?
4. What is deterministic at scoring time, and what remains subjective at labeling time?
5. What does a passing scoring report mean, and what does it not mean?
6. Under what conditions does the Harness block admission rather than score?
7. How is the protocol-vs-Pydantic field gap handled without papering over it?
8. How is a pre-existing memo (e.g., Unity sealed memo) admitted, and under what non-comparability label?
9. What is core, what is satellite, what is per-case adapter, and what is intentionally undecided?
10. What would change the recommendation?

## Architecture Option Comparison

Compared against the supplied prompt option set.

### AO-1: Cleaning Feeds Harness Directly

- Shape: Cleaning outputs a normalized evidence corpus; the Harness consumes it directly and performs participant/facilitator separation, leakage audit, band labeling, freeze, probe, scoring, and failure logging internally.
- Core responsibilities (Harness): all of the above.
- Satellite: none.
- Contracts and invariants: collapse into the Harness.
- Implications: Harness absorbs Packing-owned shapes from `docs/research/packing-phase/README.md`. Cleaning trace becomes a Harness input. Labeling-rubric work and second-label audit become Harness behaviors.
- Failure modes: collapses three layers. Violates Core Spine boundary table that gives Judgment effects to Judgment and forbids Cleaning from owning Decision Strength or Action Ceiling. Violates the Packing README handoff boundary that requires the Harness to block or mark draft-only rather than silently repair upstream preparation.
- Bloat: large; the Harness becomes a multi-role processor.
- Why it could win: simplest from a tool-count perspective.
- Why it loses: explicit source contradiction; collapses layer ownership; converts admission gates into silent repair.

### AO-2: Packing Produces A Formal Harness Entry Bundle Consumed By Harness

- Shape: a Packing layer produces a frozen Harness Entry Bundle (HEB) including frozen ParticipantPacket, EvidenceUnits, FacilitatorLedger, memorization-probe artifacts, and any sealed-memo adapter outputs. The Harness consumes the HEB through an admission gate and runs deterministic checks.
- Core responsibilities (Packing): bundle construction and freeze. Core responsibilities (Harness): admission and scoring.
- Satellite: per-case bundle content.
- Contracts and invariants: HEB is the single handoff object; admission gates block when any HEB field fails schema, hash, probe, or freeze checks.
- Implications: appears clean but conflates two operators. The frozen facilitator ledger requires the labeling-rubric workflow, second-labeler audit, and `ledger_freeze_hash`; the band-input labeling rubric assigns these to operator-with-second-labeler, not to a Packing draft author. Treating the frozen ledger as a Packing output absorbs the Facilitator labeling step into Packing without naming it.
- Failure modes: Packing silently becomes a labeling authority; second-label discipline can decay; `must_address_items` authored as Packing drafts could become scoring truth at freeze without a separate audit pass.
- Bloat: moderate; the HEB is one object, but Packing absorbs a role it does not own.
- Why it could win: appears to give the Harness one clean handoff.
- Why it loses: collapses the Facilitator labeling step into Packing; risks the adversarial A2, A8, and A9 failure modes; does not isolate `case_family`, `decision_shape`, `memorization_probe_required`, or `known_fame_risk` from the Pydantic schema surface.

### AO-3: Harness Owns Packing And Admission Internally

- Shape: a single Harness layer ingests cleaned evidence and case-frame source material and performs all packing, labeling, probe, freeze, admission, scoring, and failure logging.
- Core responsibilities (Harness): everything.
- Satellite: none.
- Contracts and invariants: collapse into the Harness.
- Implications: same Cleaning/Judgment boundary violation as AO-1, plus the Packing README boundary inversion; the Harness silently repairs missing Packing inputs.
- Failure modes: violates `docs/research/packing-phase/README.md` Judgment Harness Handoff Boundary explicitly; converts admission into silent repair; collapses the Facilitator labeling step into the Harness.
- Bloat: very large.
- Why it could win: minimizes tool count and operator interfaces.
- Why it loses: explicit source contradiction.

### AO-4: Case-Specific Manual Fixture Authoring With No General Interface

- Shape: every case re-derives the boundary; no general interface artifact exists.
- Core responsibilities: undefined; per-case.
- Satellite: everything.
- Contracts and invariants: per-case freeze of fields, hashes, probes, leakage notes.
- Implications: continues current state; future operators rederive the boundary from three prose sources plus seven v0.14 spec files for every case.
- Failure modes: case-specific drift; Unity-specific shape leaks into Daimler or future cases; admission gates become operator memory rather than retrievable contract.
- Bloat: low at first; grows quadratically as cases multiply.
- Why it could win: avoids premature generalization.
- Why it loses: the Unity extraction plan already shows the boundary is general enough to name; the cost of leaving it implicit is paid every case.

### AO-5: Hybrid (Selected): Packing Owns Draft Bundle Construction; Facilitator Owns Labeling And Freeze; Harness Owns Admission And Scoring; Named Adapter Slots Carry Case-Specific Gaps

- Shape: three named operating zones plus an adapter slot set. Packing produces draft bundle outputs and adapter inputs. A Facilitator labeling step (operator with second-labeler, under `band_input_labeling_rubric.md`) freezes the facilitator ledger from those draft inputs. The Harness Foundation admits the frozen Harness Entry Bundle and runs deterministic checks.
- Core responsibilities (Packing): participant packet body, source manifest, evidence registry with provenance facts, leakage seed inputs, facilitator-ledger work queue (drafts only), sealed-memo adapter inputs, protocol-only fixture metadata seeds. Core responsibilities (Facilitator): apply labeling rubric, run second-label workflow, resolve disagreements, freeze ledger, produce `ledger_freeze_hash` and `committed_at`. Core responsibilities (Harness): schema validation, hash recomputation, probe-result admission, schema-valid ladder mapping, deterministic action-band derivation, deterministic scoring math, append-only failure logging.
- Satellite: per-case decision_shape choice, per-case must-address authoring after second-label discipline, per-case sealed-memo treatment, per-case Daimler-fallback decision.
- Contracts and invariants: block-don't-repair admission; participant/facilitator separation; hash-bound freeze; Phase-1 failure-log-only memory; no rule promotion; sealed memos enter only as facilitator-only baseline unless a separately bound adapter handles non-comparability.
- Adapter slots (named, not generalized): sealed-memo adapter, source-visibility-gap adapter (e.g., Unity EU-08), protocol-to-Pydantic adapter for `case_family`, `decision_shape`, `memorization_probe_required`, `known_fame_risk`.
- Implications: preserves Cleaning, Data Capture, Packing, Facilitator, and Harness Foundation ownership; routes around the adversarial A2, A6, A7, A8, A9 risks; honors the grounding cuts and defers.
- Failure modes (residual): version-coupling risk if the interface is phrased as v0.14-permanent rather than v0.14-current-requires (mitigated by `stale_if` clause); narrative-not-enforcing risk persists until admission gates become machine-enforced in a later implementation-scoping lane.
- Bloat: low. One artifact. One HEB handoff name. No new schema, validator, or runtime.
- Why it wins: matches every source-stated layer rule; isolates the Facilitator labeling step instead of swallowing it; names adapter slots explicitly so future operators do not paper over the protocol-vs-Pydantic gap; preserves block-don't-repair; preserves Phase-1 non-claims.
- Why it could lose: if a later owner decision authorizes a different bundle topology (single-step Packing-as-Facilitator), AO-2 returns. This artifact's `stale_if` clause covers that case.

## Architecture Result

`TARGET_RECOMMENDED`.

## Target Architecture

Hybrid (AO-5): Packing owns draft bundle construction; a named Facilitator labeling step owns the labeling rubric workflow, second-label audit, and ledger freeze; the v0.14 Harness Foundation owns admission, deterministic action-band derivation, scoring, and append-only failure logging. A small adapter-slot set carries case-specific gaps without inviting general schema expansion.

Selection threshold:

- Stable invariant: block-don't-repair admission, participant/facilitator separation, hash-bound freeze, Phase-1 failure-log-only memory, and protocol-vs-schema adapter as a named slot rather than free-text leak-through.
- Core/satellite split: clear enough to prevent boundary leakage (see `Core / Satellite Boundary` below).
- Non-goals: enumerated above.
- No unresolved upstream blocker: the Packing README, the Core Spine boundary note, the v0.14 spec, and the bridge foundation jointly support the recommendation.

This is a planning recommendation. It is not implementation authority, validation, approval, readiness, lifecycle completion, deployment safety, resolver proof, or plugin readiness.

## Core / Satellite Boundary

### Core (Harness-Owned, Invariant Across Cases In v0.14)

- Pydantic `ParticipantPacket` frontmatter schema (`pydantic_schema_reference.md`).
- Pydantic `EvidenceUnit` schema with `evidence_id`, `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, `pre_decision_status`, `pre_decision_basis`, `summary`.
- Pydantic `FacilitatorLedger` schema fields exactly as `pydantic_schema_reference.md` defines them.
- Pydantic `BandInputs` enum set (14 fields, fixed enum values).
- Pydantic `BlindJudgement` schema and `judgement_class_ladder_mapping` validator.
- Pydantic `ActionBandResult` and deterministic action-band derivation.
- Pydantic `ScoringResult` and the deterministic scoring formulas in `scorer_formula_spec.md` and `proof_and_memory_plan.md` Code-Readiness Patch.
- `ledger_freeze_hash` canonical-YAML rule.
- Memorization probe admission gate per model family (`memorization_probe_protocol.md`).
- Append-only failure logger with `not_a_rule: true`, `promotion_allowed: false`, raise-on-`promotion_allowed=True`.
- `participant_packet_hash`, `facilitator_ledger_hash`, `prompt_hash`, `harness_version`, `mapping_table_version_pin: v0_14_mvp`, `labeling_rubric_version: v0_14`.

### Satellite (Packing-Owned, Bundle-Specific)

- Participant packet body text (decision frame, role frame, pre-cutoff facts, known uncertainties, permitted assumptions, forbidden-information notice).
- Source manifest assembly.
- Evidence-unit population per source (provenance facts only; final `pre_decision_status` and `pre_decision_basis` are Facilitator/Judgment-authority assignments, not Packing assignments — see Sharpening S1 below and Adapter Slots).
- Leakage seed content for `leakage_audit_notes` and advisory `spoiler_inventory`.
- Facilitator-ledger work queue: candidate band-input rationales (clearly tagged `packing_draft_candidate`), candidate must-address items (clearly tagged `packing_draft_candidate`), candidate underreach observability rationale (clearly tagged `packing_draft_candidate`).
- Sealed-memo adapter inputs (when a pre-existing memo or contestant-like artifact exists for the case).
- Parent-only and facilitator-only exclusion list per case.

### Named Roles At The Boundary

To honor the band-input labeling rubric's actor assignment, this architecture names three operating zones, not two:

| Role | Owns | Does not own |
| --- | --- | --- |
| Packing operator | Draft bundle construction; provenance facts on evidence units; leakage and spoiler seed content; participant/facilitator separation drafting; sealed-memo adapter input preparation; explicit `packing_draft_candidate` tagging on every advisory label, must-address candidate, and underreach rationale. | Final pre-decision status and basis assignment; frozen band-input labels; second-label audit; ledger freeze hash; probe execution; admission decisions; deterministic scoring; failure event logging. |
| Facilitator / labeling operator | Apply `band_input_labeling_rubric.md` workflow (primary labeler + second labeler + diff + resolution); re-author or re-second-label every Packing draft item before freeze (no verbatim promotion of `packing_draft_candidate` content into the frozen ledger); freeze ledger; emit `ledger_freeze_hash` and `committed_at`; assign final `pre_decision_status` and `pre_decision_basis` under Judgment-Spine authority per `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` §"Inclusion State Rule"; quarantine on disagreement triggers per the labeling rubric. | Draft bundle construction; participant packet body authoring; probe execution; deterministic scoring math; failure event logging. |
| Harness Foundation | Schema validation; hash recomputation; admission gate (block-don't-repair); probe-result admission per model family; `judgement_class_ladder_mapping` validation; deterministic action-band derivation; deterministic scoring; append-only failure-event logging with raise-on-`promotion_allowed=True`. | Drafting; labeling; ledger freeze; probe execution; sealed-memo adaptation; promotion of any failure event to a rule; baseline-superiority claims. |

### Adapter Slots (Per-Case, Named, Not Generalized)

- **Sealed-memo adapter:** maps a pre-existing memo into either a facilitator-only baseline-like input or, only under a separately bound adapter, a `BlindJudgement` instance with non-comparability flags. Default treatment is facilitator-only baseline; conversion to `BlindJudgement` requires explicit fields per `unity_v0_14_fixture_extraction_plan_v0.md` §"Sealed Unity Memo Treatment" and explicit `author_context_contamination_caveats` recorded in `advisory_phase_1_fields` until or unless a later schema revision adds first-class fields.
- **Source-visibility-gap adapter:** handles EU-08-style bounded-source-visibility-failure inputs. Adapter must produce either an `EvidenceUnit` documenting the bounded source-visibility failure (with timestamp and hash attached to the lookup result, not to a fact) or a facilitator-only evidence-gap note. Operator decision required per case.
- **Protocol-to-Pydantic adapter:** carries `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk` from the case construction protocol into the Pydantic surfaces. `decision_shape` rides on `BlindJudgement.decision_shape` for run binding. The remaining three travel inside `FacilitatorLedger.leakage_audit_notes` as structured key-value content (not free prose) until or unless the Pydantic `FacilitatorLedger` schema expands. The adapter slot is named explicitly so an operator step verifies these protocol fields are not silently lost; downstream scoring should refuse to admit cases where the structured key-value content for these four fields is absent.

## Adversarial Sharpenings Folded In

Four sharpenings from the adversarial subagent pass are folded into this v0 explicitly. They refine, not contradict, the directional recommendation.

- **S1 — `pre_decision_status` and `pre_decision_basis` finalization is a Judgment-authority decision, not a Packing decision.** Per `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` §"Inclusion State Rule", "decision-use downgrade" and "integrity exclusion" belong to Judgment Spine. Packing supplies provenance facts (`evidence_id`, `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, `summary`) and a *proposed* `pre_decision_status` with proposed basis text; the Facilitator labeling step finalizes both under Judgment authority. Harness admission blocks if final `pre_decision_status` or `pre_decision_basis` is missing or still tagged as proposed.
- **S2 — `packing_draft_candidate` provenance tag is required on every Packing-authored ledger candidate.** Candidate must-address items, candidate band-input rationales, and candidate underreach observability rationales emitted by Packing must carry an explicit `packing_draft_candidate` tag. The Facilitator must re-author or re-second-label these items under `band_input_labeling_rubric.md` before they enter the frozen ledger. Verbatim promotion of `packing_draft_candidate` content into the frozen ledger is a block-class failure of this interface.
- **S3 — Protocol-to-Pydantic adapter slot is named explicitly, not papered over via free prose.** `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk` are the four protocol-only fixture-metadata fields named in `judgement_case_construction_protocol.md` and `unity_v0_14_fixture_extraction_plan_v0.md` but absent from the current Pydantic `FacilitatorLedger`. The protocol-to-Pydantic adapter slot routes them as structured key-value content inside `leakage_audit_notes` (for the three ledger-shaped fields) and on `BlindJudgement.decision_shape` (for the run-shape field). The adapter slot is named here so a future schema revision can promote the three ledger-shaped fields to first-class without rewriting the interface.
- **S4 — Facilitator labeling is a named role distinct from Packing and from Harness Foundation.** The band-input labeling rubric assigns labeling to operator-with-second-labeler; the case construction protocol describes the facilitator ledger as "visible to scorer/operator only" but does not assign the labeling actor to either Packing or Harness. This artifact resolves the ambiguity by naming the Facilitator as a third role (see `Named Roles At The Boundary`). The Facilitator role may be filled by the same human as the Packing operator in small operations, but the responsibilities are role-separated; verbatim collapse of Packing draft candidates into a frozen ledger without applying the labeling rubric is a block-class failure of S2.

## Packing-Owned Outputs

Packing must produce the following before a case can be admitted to the v0.14 Harness Foundation. The list is bounded; nothing else is required from Packing for this interface.

| Output | Required content | Required end state | Source |
| --- | --- | --- | --- |
| Participant packet draft | Pydantic-shaped frontmatter (case_id, decision_question, decision_date_or_cutoff, role_frame, authority_constraints, capability_constraints, permitted_assumptions, forbidden_information_notice, source_manifest) plus packet body covering decision frame, cutoff, role frame, pre-cutoff facts from evidence, known uncertainties, permitted assumptions, forbidden-information notice. Excludes actual_outcome, frozen band inputs, derived floor/ceiling, must-address items, hidden labels, decoy labels, post-decision interpretation. | Frozen draft with a Packing-produced hash, ready for Facilitator and Harness consumption. | `judgement_case_construction_protocol.md`, `pydantic_schema_reference.md`, `unity_v0_14_fixture_extraction_plan_v0.md` §"Participant Packet Extraction Plan". |
| Evidence registry | One Pydantic-shaped `EvidenceUnit` per source-backed unit, with provenance facts (source_id, source, timestamp, retrieval_timestamp, source-byte hash when bytes are available) and *proposed* `pre_decision_status` plus proposed `pre_decision_basis` text. Final status assignment is a Facilitator/Judgment-authority decision per S1; Packing surfaces the proposal and the basis, not the binding exclusion. | Pydantic-shaped `EvidenceUnit` list with full provenance and proposed status. Missing hash, missing retrieval timestamp, or missing proposed basis is a Packing-side blocker, not a Harness silent-repair input. | `pydantic_schema_reference.md` §"EvidenceUnit", `unity_v0_14_fixture_extraction_plan_v0.md` §"Evidence Registry Conversion Plan", `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` §"Inclusion State Rule". |
| Leakage seed inputs | Anti-leakage notes (query cap, page-open cap, snippet-noise present but not preserved, no post-cutoff/outcome pages opened, no prior replay or contaminated archive bodies read, list of excluded source classes), proposed `memorization_probe_required: true` flag, proposed `known_fame_risk` classification with rationale. | Operator-reviewable seed content suitable for Facilitator to install into `leakage_audit_notes` and advisory `spoiler_inventory`. Probe requirement and fame risk travel through the protocol-to-Pydantic adapter slot (S3), not as free prose. | `unity_v0_14_fixture_extraction_plan_v0.md` §"Leakage-Audit Field Mapping", `memorization_probe_protocol.md` §"Inputs". |
| Facilitator-ledger work queue (drafts only) | Candidate band-input rationales (each tagged `packing_draft_candidate` per S2), candidate must-address items (each tagged `packing_draft_candidate` per S2), candidate underreach observability rationale (tagged `packing_draft_candidate` per S2). All draft items must be re-authored or re-second-labeled by Facilitator before freeze; Packing draft items are never promoted verbatim. | Visible, tagged candidate set that supports Facilitator labeling without becoming scoring truth. | `band_input_labeling_rubric.md`, `unity_v0_14_fixture_extraction_plan_v0.md` §"Facilitator-Ledger Work Queue", §"Must-Address Items"; sharpening S2. |
| Sealed-memo adapter inputs (when applicable) | Pre-existing memo content, missing-field inventory (decision_shape, judgement_class, run metadata, prompt_hash, packet/ledger hashes, evidence IDs, must-address coverage), and author-context contamination caveats explicitly recorded. Default treatment is facilitator-only baseline. | Adapter input package that prevents the memo from silently becoming a `BlindJudgement` instance. | `unity_v0_14_fixture_extraction_plan_v0.md` §"Sealed Unity Memo Treatment", `case_to_v0_14_bridge_foundation_v0.md` §"Unity Runtime Fee" blind-judgment seed. |
| Source-visibility-gap adapter inputs (when applicable) | Bounded source-visibility-failure context (lookup attempted, retrieval timestamp, lookup hash, scope) plus operator decision proposal (EvidenceUnit-with-bounded-summary, or facilitator-only evidence-gap note). | Adapter input that surfaces the gap rather than silently treating negative lookup as proof of absence. | `unity_v0_14_fixture_extraction_plan_v0.md` §"Conversion Table" EU-08 row. |
| Parent-only and facilitator-only exclusion list | Per-case enumeration of material that must not appear in the participant view (reveal readout, outcome facts, sealed memo conclusions, owner blind-read input, outcome calibration, post-cutoff source URLs/titles/snippets/bodies, known fame-risk classification, probe results, facilitator ledger contents, derived floor/ceiling). | Visible exclusion list bound to the participant packet draft. | `unity_v0_14_fixture_extraction_plan_v0.md` §"Parent-Only And Facilitator-Only Exclusion List", `judgement_case_construction_protocol.md` §"Participant Packet Must Not Include". |
| Memorization-probe artifact request | Probe input fields per `memorization_probe_protocol.md` §"Inputs" packaged for a separate probe operator: case_id, decision_question, public_identifiers_if_any, decision_date_or_cutoff, target probe_model_family and probe_model_id (per model family), probe_prompt_template_version. Packing does not run the probe; Packing prepares the inputs. | Probe-request artifact ready to be run by a probe operator before contestants see the packet. | `memorization_probe_protocol.md`. |
| Draft-vs-frozen marker | Status flag declaring the bundle as draft or frozen. Draft bundles may circulate for Facilitator labeling and probe scheduling; they must never enter Harness admission. | Explicit marker that prevents accidental admission of unsealed inputs. | `docs/research/packing-phase/README.md` §"Judgment Harness Handoff Boundary". |

Packing does not produce: final `pre_decision_status` assignments, frozen band inputs, second-label diffs, `ledger_freeze_hash`, `committed_at`, mapping-table results, action-band derivations, scoring math results, failure events, probe results, contestant runs, baseline comparisons, lesson-promotion claims, product-proof claims.

## Harness-Owned Freeze Inputs

The Harness Foundation receives a `Harness Entry Bundle (HEB)` — a named conceptual handoff object, not a new file schema — assembled from Packing-owned outputs plus the Facilitator labeling step's frozen ledger and the memorization-probe operator's probe artifacts. The HEB consists of:

| HEB component | Source | Required end state at admission |
| --- | --- | --- |
| Frozen participant packet | Packing draft, frozen by Facilitator after participant-packet review. | Pydantic-valid frontmatter; `participant_packet_hash` computed and matches recomputation. |
| Evidence registry | Packing output plus Facilitator finalization of `pre_decision_status` and `pre_decision_basis` per S1. | Pydantic-valid `EvidenceUnit` list; per-source `hash` and `retrieval_timestamp` present; final `pre_decision_status` assigned (Facilitator), not proposed; final `pre_decision_basis` text present. |
| Frozen facilitator ledger | Facilitator output (not Packing output). | Pydantic-valid `FacilitatorLedger` with `frozen_band_inputs` (all 14 enum fields valid, no `packing_draft_candidate` content carried verbatim per S2), `second_label_diffs` (present even if empty), `must_address_items` (re-authored or re-second-labeled per S2), `underreach_observability` (Pydantic `basis` enum only), `leakage_audit_notes` (containing leakage seed content and structured protocol-to-Pydantic adapter content per S3), advisory `spoiler_inventory`, `mapping_table_version_pin: v0_14_mvp`, `labeling_rubric_version: v0_14`, `ledger_freeze_hash`, `committed_at` in ISO-8601 UTC with `Z` suffix. |
| Protocol-to-Pydantic adapter content | Facilitator output that consumes Packing's leakage seeds per S3. | `memorization_probe_required`, `known_fame_risk`, and `case_family` carried inside `leakage_audit_notes` as structured key-value content (not free prose). `decision_shape` carried on `BlindJudgement.decision_shape`. Admission blocks if structured content for these four fields is absent. |
| Memorization-probe artifacts | Probe operator output (not Packing output). | At least one probe artifact per target contestant/model family per `memorization_probe_protocol.md` §"Artifact Schema"; `probe_result: pass` for that model family; `prompt_hash` and `raw_response_hash` present. `fail` or `ambiguous_until_operator_review` is a block, not a soft warning. |
| Sealed-memo adapter output (when applicable) | Adapter output from Packing's adapter inputs. | Default: facilitator-only baseline labeled non-comparable. If converted to `BlindJudgement`, must include `decision_shape`, `judgement_class` per ladder mapping, prompt/packet/ledger hashes, evidence IDs, must-address coverage, and `author_context_contamination_caveats` in `advisory_phase_1_fields`. Missing any of these blocks admission of the sealed memo as a `BlindJudgement` instance; the memo may still circulate as facilitator-only baseline. |
| Source-visibility-gap adapter output (when applicable) | Adapter output from Packing's adapter inputs, finalized by Facilitator/Judgment-authority decision. | Either Pydantic-valid `EvidenceUnit` documenting the bounded source-visibility failure or a facilitator-only evidence-gap note bound to the case. |
| Run binding inputs | Operator output prior to contestant run. | `case_id`, `decision_shape` (frozen per case from the v0.14 enum set), `mapping_table_version_pin: v0_14_mvp`, `harness_version: v0_14`, `participant_packet_hash`, `facilitator_ledger_hash`. |

The HEB is a named handoff surface. It is not a new file schema, not an authorized object model, and not a runtime contract. It maps onto the existing v0.14 per-case folder layout (`cases/<batch>/<case_id>/`) named in `judgement_case_construction_protocol.md` §"Case Folder Contract".

The Harness Foundation:

- recomputes hashes and compares to declared hashes;
- validates Pydantic schemas;
- applies the `judgement_class_ladder_mapping` validator to any `BlindJudgement` admitted (including sealed-memo-adapter output if converted);
- runs the deterministic action-band derivation from frozen `BandInputs` via the v0.14 mapping table;
- runs the deterministic scoring formulas;
- writes append-only failure events with `not_a_rule: true`, `promotion_allowed: false`;
- raises if any logger or aggregator attempts `promotion_allowed=True`.

The Harness Foundation does not:

- author labels;
- run second-label workflows;
- author must-address items;
- compute final `pre_decision_status` assignments (per S1);
- run probes;
- repair missing hashes;
- silently accept draft bundles;
- promote failure events to rules;
- compare across cases for product proof;
- claim baseline superiority.

## Contestant-Visible Boundary

Contestants see, via the contestant runner (`runners/run_contestant.py`, single runner for all contestants per `blind_judgement_schema_and_harness_protocol.md` §"Contestant Runner Policy"):

- Rendered prompt built from the frozen participant packet only.
- Nothing else.

Contestants do not see:

- The facilitator ledger or any of its fields.
- Frozen band inputs.
- Derived action floor or ceiling.
- Must-address items.
- Underreach observability.
- Leakage audit content.
- Memorization-probe results.
- Sealed-memo adapter outputs.
- Parent-only or facilitator-only material.
- Outcome facts, reveal readout, outcome calibration, owner blind-read.
- Other contestants' outputs.

The schema repair policy from `blind_judgement_schema_and_harness_protocol.md` allows one schema-repair attempt by a separate `schema_repair_assistant` role; no prompt rerun is allowed for the contestant; if repair fails, `raw_model_output.txt` is saved and `schema_validity: false` is recorded. Repair does not retry the contestant prompt. This boundary is owned by the v0.14 spec and is preserved here without modification.

Semantic leakage remains partly operator/review work. Harness admission checks declared boundaries and hard markers; it does not pretend it can prove all semantic non-leakage mechanically.

## Deterministic Scoring And Checking Boundary

Deterministic at scoring time:

- `in_band`, `over_band`, `under_band` from `recommended_level` and `action_floor`/`action_ceiling`.
- `overreach_distance` and `underreach_distance` per the frozen formulas.
- `underreach_primary` only when `underreach_observability.present == true`.
- `evidence_id_check_result`: presence of cited evidence IDs, exclusion of post-decision evidence, load-bearing claim citation coverage.
- `must_address_coverage_result` against the frozen `must_address_items`.
- `memorization_probe_result` carried into `ScoringResult` per `pydantic_schema_reference.md` §"ScoringResult".
- Schema validity of `BlindJudgement`, including `judgement_class_ladder_mapping`.
- Append-only failure-event logging when any of the named failure conditions occur per `failure_event_log_spec.md` §"Logging Rules".

Subjective at labeling time (not at scoring time):

- The choice of each `BandInputs` enum value (made by the Facilitator under `band_input_labeling_rubric.md`).
- The selection of `must_address_items` (Facilitator; not promoted verbatim from `packing_draft_candidate` content per S2).
- The presence and basis of `underreach_observability` (Facilitator).
- The leakage audit content (Facilitator, from Packing seed content, with protocol-to-Pydantic adapter content structured per S3).
- The `decision_shape` selection per case (Facilitator).
- The treatment of any sealed memo (Facilitator, using Packing adapter inputs).
- The final `pre_decision_status` assignment per evidence unit (Facilitator under Judgment authority, from Packing proposal per S1).

Phase 1 scoring does not check:

- Semantic relevance of cited evidence to the load-bearing claim.
- Direct versus inferential support.
- Contradiction across evidence units.
- Improvement of judgment quality across runs.
- Memory compounding.
- Baseline superiority.

Per `proof_and_memory_plan.md` §"Evidence-to-Claim Policy".

## Report Meaning And Non-Meaning

A v0.14 `ScoringResult` for one case with one contestant, under this interface, means:

- The HEB passed schema validation and hash recomputation.
- The memorization probe for the contestant's model family passed.
- The contestant produced a schema-valid `BlindJudgement` (or a schema-repair attempt was logged).
- The mapping table version matched.
- The deterministic action band derivation, in-band/over-band/under-band status, and shallow evidence-ID and must-address checks ran.
- Failure events, if any, were appended to `memory/logs/failure_events.yaml` with `not_a_rule: true` and `promotion_allowed: false`.

It does not mean:

- The case is product-ready, buyer-validated, model-training-ready, or commercially ready.
- The harness beats any baseline.
- The judgment quality of the contestant is proven.
- Semantic evidence support is proven.
- Any lesson is promoted.
- Memory has compounded.
- The sealed-memo adapter output, if any, is comparable to fresh contestant runs.
- The probe pass proves there is no memorization.
- The HEB is correct beyond the deterministic checks named above.
- The Packing layer has been validated.
- The Facilitator labeling is correct beyond rubric-pass and second-label discipline.

Per `proof_and_memory_plan.md` §"Phase 1 Claim Discipline", `failure_event_log_spec.md` §"Allowed Claims", `judgment_spine_thesis_operating_contract_v0.md` §"Must Not Be Used To Claim", and `memorization_probe_protocol.md` §"Limits".

## Inadmissibility / Block States

The Harness Foundation BLOCKS admission (does not silently repair) when any of the following holds. The list is the required end state for any future implementation-scoping lane; it does not authorize the validators here.

Packing-side blockers (the HEB cannot be assembled; case stays in Packing):

- Participant packet draft missing required frontmatter field.
- Participant packet draft contains any forbidden item from `judgement_case_construction_protocol.md` §"Participant Packet Must Not Include".
- Any `EvidenceUnit` missing `evidence_id`, `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, or proposed `pre_decision_basis`.
- Any `EvidenceUnit` missing a proposed `pre_decision_status` from Packing.
- Source-visibility-gap adapter required for an evidence unit (e.g., Unity EU-08 pattern) and no operator decision recorded.
- Leakage seed inputs missing (`memorization_probe_required`, `known_fame_risk`, anti-leakage notes).
- Sealed-memo adapter inputs missing for a case where a pre-existing memo is intended as facilitator-only baseline or as `BlindJudgement` input.
- Parent-only and facilitator-only exclusion list absent.
- Draft-vs-frozen marker absent or set to draft at admission time.
- Any candidate must-address, band-input rationale, or underreach rationale emitted without the `packing_draft_candidate` tag (per S2).

Facilitator-step blockers (HEB cannot be admitted; case stays in labeling):

- Any `BandInputs` field not Pydantic-enum-valid.
- `second_label_diffs` absent (must be present even if empty).
- More than three band-input disagreements before resolution, or disagreement on `evidence_strength` exceeding one level, or disagreement on `loss_shape` including `ruinous_tail`, or disagreement on `information_decay` including `expiring` that cannot be resolved.
- `must_address_items` promoted verbatim from `packing_draft_candidate` content without re-authoring or re-second-labeling (per S2).
- `underreach_observability.basis` set to a non-Pydantic value such as `option_value_loss`; option-value loss content must live in `notes` or under `other`.
- `mapping_table_version_pin` missing or not `v0_14_mvp`.
- `labeling_rubric_version` missing or not `v0_14`.
- `ledger_freeze_hash` missing or not matching `sha256(canonical_yaml_dump(ledger_minus_hash_field))` with sorted keys, LF line endings, UTF-8.
- `committed_at` missing or not ISO-8601 UTC with `Z` suffix.
- Final `pre_decision_status` on any evidence unit still tagged as proposed rather than Facilitator-finalized (per S1).
- Protocol-to-Pydantic adapter content for `case_family`, `memorization_probe_required`, or `known_fame_risk` absent or unstructured inside `leakage_audit_notes` (per S3).

Probe blockers:

- No memorization-probe artifact for the target contestant/model family.
- `probe_result: fail` for that model family.
- `probe_result: ambiguous` with `reviewed_by_operator: false`.

Run-binding blockers (HEB present but contestant run cannot be admitted to scoring):

- `decision_shape` not frozen per case.
- `participant_packet_hash` or `facilitator_ledger_hash` missing or not matching recomputed hash.
- `prompt_hash` or `harness_version` missing.
- `BlindJudgement` violates `judgement_class_ladder_mapping`.
- Sealed-memo adapter output asserted as `BlindJudgement` instance without required fields (`decision_shape`, `judgement_class`, prompt/packet/ledger hashes, evidence IDs, must-address coverage, author-context-contamination caveats in `advisory_phase_1_fields`).

Cross-cutting blockers:

- Any participant-facing content includes excluded items (reveal readout, outcome facts, sealed memo conclusions, owner blind-read, outcome calibration, post-cutoff source URLs/titles/snippets/bodies, known fame-risk classification, probe results, facilitator ledger content, derived floor/ceiling, must-address items, hidden labels, decoy labels, post-decision interpretation).
- Any logger or aggregator attempts `promotion_allowed=True`.
- Any attempt to write to forbidden Phase-1 memory directories (`memory/rules/`, `memory/promoted/`, `memory/retrieval/`, `memory/judgement_memory/`).
- Any attempt to compute baseline-superiority or harness-superiority claims.

Block-don't-repair is the invariant. Silent repair by the Harness is itself a block-class failure of this interface.

## Deferred Implementation Implications

Non-executable. This artifact does not authorize implementation.

A later owner-authorized implementation-scoping lane would need to bind a single bounded slice, likely:

- Pydantic schemas as code for `ParticipantPacket` frontmatter, `EvidenceUnit`, `FacilitatorLedger`, `BlindJudgement`, `ActionBandResult`, `ScoringResult`, `FailureEvent`.
- A `ledger_freeze_hash` routine over canonical YAML (sorted keys, LF, UTF-8).
- A source-byte hash routine for `EvidenceUnit.hash`.
- A Packing-side adapter for source-packet content into `ParticipantPacket` and `EvidenceUnit` (per case).
- A protocol-to-Pydantic adapter for `case_family`, `decision_shape`, `memorization_probe_required`, `known_fame_risk` (per S3).
- A sealed-memo adapter that preserves non-comparability rather than erases it.
- A memorization-probe runner per `memorization_probe_protocol.md`.
- An admission-gate function that raises on every blocker listed above rather than silently repairing.
- An append-only failure logger that raises on `promotion_allowed=True`.
- Per-case folder layout matching `judgement_case_construction_protocol.md` §"Case Folder Contract".

None of these is authorized here. A later implementation-scoping lane must reopen `phase_1_infrastructure_architecture.md`, recheck source state, bind one fixture scope, obtain explicit bounded implementation authorization, and preserve the no-proof and no-memory-promotion boundaries.

## What Is Intentionally Undecided

Owner decisions required before any of these are bound:

- Whether the protocol-only fields `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk` should be promoted to first-class Pydantic `FacilitatorLedger` fields (schema revision), or remain protocol-only metadata routed via structured `leakage_audit_notes` content (S3) and `BlindJudgement.decision_shape`.
- Whether the HEB requires a single bundle manifest file or remains a named handoff over the existing `cases/<batch>/<case_id>/` folder layout.
- Whether the Facilitator labeling step is recorded as its own role/section in the artifact tree (separate from Packing artifacts and Harness artifacts) or remains an operator-implicit step (S4 names the role but does not bind the artifact-tree layout).
- Whether the sealed-memo adapter outputs an explicit `AdvisoryBaselineRecord` artifact type or rides in `advisory_phase_1_fields` of an adapted `BlindJudgement`.
- Whether Daimler, Unity, or another case is the first case the interface is exercised end-to-end against (per `unity_v0_14_fixture_extraction_plan_v0.md` §"Daimler Fallback Decision Gate").
- Whether `decision_shape` should appear in the Pydantic `FacilitatorLedger` even though `judgement_case_construction_protocol.md` lists it under the ledger and `pydantic_schema_reference.md` lists it only under `BlindJudgement` (resolves adversarial A6 at the schema level).
- Whether a Packing-side receipt artifact (analogous to the existing Unity fixture authoring receipt) becomes required for every case or remains case-discretion.
- Whether the second-labeler may be a separate model-family advisory in addition to a separate human (the labeling rubric allows both; per-case policy is owner-set).
- Whether the bundle's draft-vs-frozen marker is a single status field or a per-component status set.
- Whether the same human may fill both the Packing-operator role and the Facilitator role in small operations, given that S4 separates the responsibilities but does not require separate humans.

## What Would Change The Recommendation

- An owner decision that authorizes Packing to own facilitator labeling under the labeling rubric (would collapse into AO-2 but is not currently supported by `band_input_labeling_rubric.md`).
- An owner decision that authorizes Harness Foundation to own draft packet construction (would collapse into AO-3 but is not currently supported by the Packing README boundary).
- A v0.15 spec that supersedes v0.14 with materially different schema or labeling shape.
- A Pydantic `FacilitatorLedger` revision that adds `case_family`, `decision_shape`, `memorization_probe_required`, or `known_fame_risk` as first-class fields (would simplify the protocol-to-Pydantic adapter slot).
- An owner decision that authorizes a separate `AdvisoryBaselineRecord` artifact type (would adjust the sealed-memo adapter target).
- A Core Spine boundary patch that reassigns Cleaning/ECR/Judgment ownership (would change the layer split).
- A future case (e.g., Daimler) producing a clean v0.14 admission end-to-end with materially different shape than Unity (would refine the satellite list and the adapter slots).
- An accepted product or feature plan that explicitly requires harness comparability across contestants with pre-existing memos (would force a separately authorized sealed-memo adapter beyond the current advisory-only default).
- A second non-Unity pressure test exposing a generic bundle field not represented here.

## Bloat-Cut Queue

Do not invent the following from this artifact:

- A new leakage artifact schema. Leakage lives in `FacilitatorLedger.leakage_audit_notes` (structured key-value content per S3) and advisory `spoiler_inventory`; probe/fame-risk travel through the protocol-to-Pydantic adapter slot.
- A Packing-side validator, scorer, or rule engine. Phase-1 deterministic checks are owned by the Harness scorer.
- A new evidence schema. `EvidenceUnit` is frozen in `pydantic_schema_reference.md`.
- New ladder or judgement-class vocabulary. The `judgement_class_ladder_mapping` and ladder levels 0-8 are frozen.
- New memory or rule-promotion shape. Phase 1 is failure-log only.
- A Packing-side hashing routine separate from the canonical `ledger_freeze_hash` and source-byte `EvidenceUnit.hash` already specified.
- Data Capture, ECR, or Cleaning ownership inside Packing. Core Spine boundary table already splits these.
- A Packing-side contestant runner. `one_runner_for_all_contestants: true`.
- A new bundle file shape beyond the existing v0.14 per-case folder layout. The HEB is a named handoff, not a new file type.
- A facilitator-side runtime for second-label workflow beyond what `band_input_labeling_rubric.md` already specifies.
- A new sealed-memo conversion engine. Adapter inputs and an `advisory_phase_1_fields` carry slot are sufficient.
- A back-channel from Packing to Cleaning for re-cleaning. Cleaning is upstream and not re-entered from Packing; missing-cleaning conditions block rather than re-enter.
- A separate Packing manifest for cross-case state. Per-case folder + HEB handoff is sufficient.
- A new schema for `AdvisoryBaselineRecord` (deferred to owner decision).
- A registry of case-specific adapter classes. Adapter slots are named; their content is per-case operator work.
- A broad Packing Spine expansion beyond the narrow admission interface.

## Non-Claims

This artifact does not claim:

- Judgment Spine validation.
- v0.14 harness validation, readiness, or superiority over any baseline.
- Packing layer validation, readiness, or completeness.
- Facilitator labeling validation or completeness.
- Memorization-probe pass for any case or any model family.
- Score readiness for any case.
- Sealed-memo comparability to fresh contestant runs.
- Baseline comparability.
- Semantic evidence support beyond v0.14 shallow checks.
- Source-of-truth promotion of any v0.14 spec file, the Packing README, the bridge foundation, the Unity extraction plan, the judgment-spine manifest, or this artifact.
- Acceptance or approval by any reviewer, operator, or lifecycle authority.
- Implementation authorization for schemas-as-code, freeze-hash routines, source-byte hashing, probe runners, sealed-memo adapter generators, leakage validators, or admission-gate functions.
- Runtime authorization.
- Buyer validation, willingness-to-pay, product readiness, feature readiness, commercial readiness, or proof-run readiness.
- Model-training readiness, memory compounding, or rule-promotion authority.
- Harness superiority over structured pipelines, raw frontier LLMs, single-prompt baselines, or sealed memos.
- That Unity is probe-safe, score-ready, or generally the best first scoreable candidate.
- That Daimler is accepted into manifest inventory.
- That dirty or untracked sources are accepted authority.
- Lesson promotion authority for any case-local lesson, including Milwaukee and Unity reusable lessons.
- Authorization for runtime design, scrapers, automation, tests, packages, commits, pushes, PRs, proof runs, or feature planning.
- Source-of-truth promotion of any subagent output.
- That subagent agreement constitutes proof.

## Smallest Complete Next Routing Object

This architecture artifact is itself the smallest complete next routing object. Once it is opened by a future CA or operator:

- The Unity v0.14 fixture authoring CA (named in `unity_v0_14_fixture_extraction_plan_v0.md` §"Next Authorized Step", `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md`) can be re-anchored against this interface artifact for the Unity case, with the protocol-vs-Pydantic adapter slot, sealed-memo treatment, S1 `pre_decision_status` finalization, S2 `packing_draft_candidate` tagging, and S4 Facilitator role made explicit at admission.
- A future case-admission lane for Daimler, when authorized, can use this interface artifact directly without rederiving the boundary.
- A future implementation-scoping prompt for the bounded admission slice (schemas-as-code + ledger freeze + admission gate + probe runner + failure logger) can use this artifact as its frozen interface input. That implementation-scoping lane must reopen `phase_1_infrastructure_architecture.md`, recheck source state, bind one fixture scope, and obtain explicit bounded implementation authorization.

This is not an ADR slice (v0.14 spec already binds the schemas and the action-band/scorer math; no new decision needs ratification beyond the boundary defined here). It is not a feature-planning input (no feature scope). It is not, by itself, an implementation-scoping input — implementation scoping requires a separately authorized lane that reopens the infrastructure architecture file.

## Source-Read Ledger

Required controlling sources read:

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` | Workspace operating constraints. | Clean. |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint. | Modified (in scope for overlay maintenance, not this artifact). |
| `.agents/workflow-overlay/source-of-truth.md` | Source precedence. | Modified. |
| `.agents/workflow-overlay/source-loading.md` | Source-pack and capsule budgets. | Modified. |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-gated method sequencing and output-mode rules. | Modified. |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted folder rules. | Modified. |
| `.agents/workflow-overlay/artifact-roles.md` | Artifact roles and permissions. | Modified. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract. | Clean. |
| `.agents/workflow-overlay/validation-gates.md` | Validation gate expectations. | Modified. |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules. | Modified. |
| `docs/workflows/orca_repo_map_v0.md` | Repo navigation context. | Modified. |
| `docs/research/packing-phase/README.md` | Packing-Harness handoff boundary and Packing-owns/does-not-own lists. | Untracked; hash matches prompt. |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 spec navigation, source-of-truth roles, code-ready gate. | Untracked; hash matches prompt. |
| `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md` | Minimum harness-entry shape, controlling-source map, sealed-memo treatment, deferred implementation slice. | Untracked; hash matches prompt. |
| `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md` | Concrete bundle-construction and admission-gate work queue; protocol-vs-Pydantic split. | Untracked; hash matches prompt. |
| `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md` | Drift list and non-claims discipline. | Untracked; hash matches prompt. |
| `docs/research/judgment-spine/manifest_v0.md` | Current case inventory and harness spec inventory; pointer-update fit check. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md` | Four-lane structure, case folder contract, packet must/must-not, ledger fields, acceptance/quarantine criteria. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` | Authoritative schema surface, ledger hash rule, judgement-class ladder mapping, scoring and failure-event schemas. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md` | Contestant output schema, schema-repair policy, contestant runner policy, required run metadata. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md` | Labeling workflow, enum value rules, disagreement and quarantine rules. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md` | Pre-packet probe gate, fail/ambiguous routing, artifact schema and limits. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md` | Append-only failure-log rules, forbidden directories, no-promotion invariant, raise-on-promotion. | Untracked. |
| `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md` | Phase 1 allowed/forbidden claims, evidence-to-claim policy, kill criteria. | Untracked. |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Canonical layer-ownership table; inclusion state rule; layer rules. | Untracked. |
| `workflow-architecture-planning` skill source | REFERENCE-LOAD for method mechanics only; not applied until source context ready. | Read-only method reference. |
| Prior v0 architecture artifact (hash 4DF970A81C3711957470BE7B306050FF0E7FD09FC96EA0159DC0DA038BC1EC7C) | Collision check; content compared for equivalence before replacement under owner authorization. | Untracked; never committed; superseded by this artifact. |

Sources deliberately not read:

- `phase_1_infrastructure_architecture.md`, `changelog.md`, `action_band_mapping_table_numbers.md`, `action_band_mapping_executable_spec.md`, and `scorer_formula_spec.md`: the bridge foundation and Unity extraction plan already extract the relevant interface and deferred-implementation implications; opening them would widen source loading without changing this architecture result.
- Concrete exemplar fixture artifacts under `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/`: the Unity extraction plan already exercises the interface against Unity; reading the drafts would not change the option ranking.
- Method-validation replays, proof-run packets, review outputs, prompts beyond what was named, `docs/_inbox/`, full product directory, implementation code, tests, packages, and runtime files: excluded by the prompt and by source-loading budget; would not change this architecture result.

## Next Authorized Step

The next authorized step is docs-only: open this artifact and the v0.14 index to bind any future case-admission CA prompt, or open this artifact as the frozen interface input to a separately authorized implementation-scoping prompt that reopens `phase_1_infrastructure_architecture.md`, rechecks source state, binds one fixture scope, and obtains explicit bounded implementation authorization.

Do not route directly to implementation, probe execution, model runs, scoring, proof-run, product-proof, lesson promotion, baseline comparability claims, or harness-superiority claims.
