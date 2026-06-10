# Packing To Harness Foundation Interface Architecture v1

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Docs-only architecture decision for the Packing Phase -> Judgment Harness Foundation interface under v0.14.
use_when:
  - Deciding whether a packed case can be admitted, rejected, quarantined, or held as draft before v0.14 harness execution.
  - Separating Packing-owned bundle construction from Harness-owned freeze, admission, deterministic scoring, reports, and failure logs.
  - Preparing later owner review or implementation scoping without authorizing implementation, probes, scoring, validation, or product proof.
authority_boundary: retrieval_only
open_next:
  - docs/research/packing-phase/README.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
input_hashes:
  docs/research/packing-phase/README.md: E108281113DA1C27DB241BBB600B19D79334CB407707C6234EE1E1264626EF06
  docs/research/judgment-spine/harness/v0_14/index.md: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 4AF1F45964DBB560D7C6E02827BC30A9161D4433EA754580239C122DAEF532A5
branch_or_commit: main@b7627d3389eeaa8456c65974039ada0e519617bc with dirty pre-existing workspace state
stale_if:
  - Packing Phase ownership or output obligations are materially changed.
  - v0.14 is superseded by a later harness version.
  - Orca accepts a different Data Capture, Cleaning, Packing, Judgment, or Harness phase boundary.
  - A second non-Unity fixture exposes a generic interface field missing from this decision.
```

- Status: ARCHITECTURE_PLANNING_V1_RELOCATION_COPY
- Architecture result: TARGET_RECOMMENDED
- Target: Block-first hybrid Harness Entry Bundle interface
- Output mode used: file-write
- Relocation note: written to a new versioned path after the operator reported the original path may have been overwritten; content is the v0 architecture artifact with this self-identification updated.
- Implementation authorized: no
- Runtime, package, test, automation, model run, memorization-probe execution, scoring execution, validation execution, proof-run, product-proof, lesson-promotion, commit, push, or PR authorized: no
- Strict readiness, validation, acceptance, source-of-truth promotion, probe-safety, score-readiness, implementation authorization, harness superiority, product-proof, buyer-proof, memory compounding, or lesson-promotion claims: not proven

## Source Context Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus pinned Packing and v0.14 interface sources, v0.14 protocol/scoring/probe/failure-log/proof files, infrastructure file for deferred implications only, and narrow Unity exemplar/review context
  edit_permission: docs-write
  target_scope: Create docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v0.md only unless a narrow discovery pointer is needed.
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
```

Dirty-state caveat: the worktree was dirty before this artifact was written, with modified overlay/docs files and many untracked research/review artifacts. Those sources may support this bounded architecture planning artifact, but they do not prove acceptance, validation, readiness, source-of-truth promotion, implementation authorization, score-readiness, product proof, or lesson promotion.

Hash receipt: the five required task-source hashes named in the prompt were verified and matched before the sources were used for strict source-pinning claims.

## Architecture Frame

The architecture question is how to govern the boundary where Packing turns cleaned evidence into judgment-ready case artifacts and the Judgment Harness Foundation freezes, admits, scores, reports, and logs failures without absorbing upstream responsibilities.

The controlling tension is that the harness needs strict, frozen inputs, but many case-preparation failures are not harness failures. Missing provenance, unresolved evidence adapters, participant/facilitator leakage, incomplete labels, or missing probe state should block admission instead of being repaired by the harness.

The target actor is a future Chief Architect, operator, or implementation-scoping lane deciding whether one case may enter harness execution. The target system surface is not a runtime API yet. It is a stable docs-level interface contract that later implementation scoping can consume if, and only if, a later turn explicitly authorizes bounded implementation.

Non-goals:

- Do not implement schemas, runners, probes, scoring, reports, packages, tests, or automation.
- Do not run a model, probe, scorer, validator, or product-proof lane.
- Do not claim any case is admitted, score-ready, validated, accepted, probe-safe, or product-proven.
- Do not turn Unity Runtime Fee into the interface owner.
- Do not let v0.14 harness work absorb Data Capture, ECR, Cleaning, Packing, parent Judgment Spine lesson promotion, or product proof.

## Questions This Architecture Must Answer

1. What must Packing produce before the harness can even consider admission?
2. Which fields and artifacts are contestant-visible, facilitator-only, or harness-only?
3. What does Harness freeze, hash, version-pin, admit, reject, quarantine, or mark draft-only?
4. Which checks are deterministic, and which checks remain subjective, advisory, or outside Phase 1?
5. What does a harness report mean, and what must it not be used to claim?
6. Which missing or unsafe states block admission instead of being silently repaired?
7. How should case-specific gaps be represented without creating a broad adapter that hides upstream work?
8. What should future implementation scoping inherit, and what must stay deferred?

## Subagent Evidence Disclosure

```yaml
subagents_launched: 3
evidence_mode: delegated lane subagents plus main-agent synthesis
delegation_runtime: inherited/default agent type and model
subagent_authority: advisory_only
subagent_non_claims:
  - not verdicts
  - not implementation authority
  - not validation
  - not readiness
  - not proof
```

The three advisory architecture subagents used the loaded source context. They did not edit files, run probes, run models, score cases, install packages, claim validation, or route runtime model choice.

### Directional Subagent Summary

The directional lane recommended the hybrid architecture: Packing constructs a formal Harness Entry Bundle, Harness owns freeze/admission/scoring, and a small adapter layer handles case-specific gaps without letting Harness repair upstream defects.

Its strongest source-backed reasons were:

- Packing is explicitly the layer that turns cleaned evidence into judgment-ready artifacts and the harness should consume frozen or draft-labeled artifacts.
- v0.14's four-lane structure separates participant packet, facilitator ledger, blind judgment, and scoring result.
- Deterministic scoring only works after ledger labels and enum inputs are frozen.
- Admission blockers are already explicit in the bridge and fixture sources.
- The thesis operating contract prevents Judgment/Harness work from absorbing Data Capture, ECR, or Cleaning mechanics.

The directional lane warned that the adapter layer could become a dumping ground for upstream repair and that Unity fixture work could overfit the interface.

### Adversarial Subagent Summary

The adversarial lane attacked the same hybrid target and found it survivable only as a block-first interface.

Its strongest objections were:

- A formal bundle can become a polished missingness wrapper if TODO provenance and hash gaps look structured enough to proceed.
- v0.14 has protocol-versus-Pydantic tension; an adapter can quietly normalize unresolved decisions.
- Deterministic scoring can hide subjective label weakness if frozen labels were poorly authored.
- Contestant-visible leakage is partly semantic and cannot be fully machine-checked without turning Harness into Packing/review.
- Unity's sealed memo, EU-08 gap, fame risk, and calibration chain could accidentally shape a Unity-specific interface.
- Phase 1 infrastructure files create implementation gravity.

The adversarial lane required explicit states such as `admit`, `reject`, `quarantine`, `draft_only`, and `adapter_blocked`, and required Harness to avoid authoring labels, cleaning evidence, resolving gaps, inferring provenance, repairing leakage, or adapting sealed memos into comparable contestant runs.

### Grounding Subagent Summary

The grounding lane agreed with the hybrid target but narrowed it: the Harness Entry Bundle should be a narrow admission object, not a new broad Packing Spine and not a Unity-specific fixture format.

Its grounded boundary was:

- Packing owns participant-packet candidate, evidence registry, source manifest/provenance receipt, contestant-visible boundary map, facilitator-only exclusions, adapter/gap ledger, and declared inadmissibility states.
- Harness owns canonical case ID handling, packet and ledger hashes, frozen facilitator ledger inputs, second-label diffs, probe result, BlindJudgement/run metadata, deterministic action-band mapping, scoring formulas, evidence-ID checks, must-address coverage, case report, and failure events.
- Reports mean mechanical scoring under fixed v0.14 inputs and fixed contestant output; they do not mean validation, readiness, semantic correctness, lesson promotion, or memory compounding.

It identified the smallest complete next routing object as this architecture artifact, not implementation scoping.

## Option Comparison

| Option | Architecture shape | Why it may win | Why it loses | Result |
| --- | --- | --- | --- | --- |
| AO-1 Cleaning feeds Harness directly | Cleaning outputs normalized evidence directly into Harness fixtures. | Shortest path; avoids another named interface. | Violates Packing README distinction between cleaned evidence and judgment-ready packets. Gives Cleaning contestant-packet, uncertainty, leakage, facilitator-separation, and judgment-preparation responsibilities it does not own. Harness would receive evidence before participant/facilitator boundaries and labels exist. | Rejected |
| AO-2 Packing produces formal Harness Entry Bundle consumed by Harness | Packing emits a bundle of packet, registry, provenance, leakage, and gap surfaces; Harness consumes it. | Matches Packing purpose and v0.14 need for separable surfaces. Creates a future stable interface. | Insufficient if it does not say Harness owns freeze/admission/scoring and if adapters/gaps are not hard-stop states. Can become a polished wrapper around missingness. | Retained only as part of hybrid |
| AO-3 Harness owns packing/admission internally | Harness constructs or repairs participant packets, evidence registry, labels, adapters, and admission state. | Centralizes execution and may reduce handoff friction. | Collapses Harness into Packing/Cleaning/Data Capture/review. Hidden implementation gravity. Lets deterministic scoring inherit repaired subjective or provenance gaps. | Rejected |
| AO-4 Manual case-specific fixture authoring only | Each fixture is authored manually with no general interface. | Minimal abstraction; useful for draft Unity work. | Does not give future CAs/operators a stable prepare-or-reject checklist. Encourages Unity-specific drift and repeated boundary arguments. | Rejected as target; retained as exemplar-only practice |
| AO-5 Hybrid: Packing owns bundle construction; Harness owns freeze/admission/scoring contract; small adapter layer for gaps | Formal Packing-owned Harness Entry Bundle plus Harness-owned non-repairing admission/freeze/scoring/report/failure-log contract. Case-specific adapters are explicit, small, and block-first. | Best preserves phase ownership, deterministic scoring discipline, leakage boundaries, inadmissibility states, future implementation stability, and non-claims. | Requires strict anti-bloat rules and explicit adapter-block states to avoid becoming hidden repair. Needs a second non-Unity pressure test before broad stability claims. | Selected |

## Target Architecture Result

```yaml
architecture_result: TARGET_RECOMMENDED
selected_target: block_first_hybrid_harness_entry_bundle_interface
target_recommended: yes
```

The selected target is a block-first hybrid interface:

1. Packing owns construction of a formal Harness Entry Bundle.
2. Harness owns freeze, admission decision, deterministic checks, scoring, reports, and failure logs.
3. A small adapter layer records case-specific gaps, protocol/schema mapping issues, source-visibility problems, and legacy-material treatment, but it does not repair upstream defects or infer missing fields.

This target wins because it gives future operators a stable prepare-or-reject surface while preserving the source-backed phase split. It also turns missing provenance, leakage, unresolved adapters, missing labels, missing probe state, and missing hashes into inadmissibility states instead of harness repair work.

## Selected Or Deferred Target Architecture

Selected: `block_first_hybrid_harness_entry_bundle_interface`.

Deferred:

- Exact file layout or runtime serialization for a future bundle.
- Any schema-as-code, package, runner, CLI, Makefile, tests, validation, CI, or report implementation.
- Any broad Packing Spine expansion beyond the narrow admission interface.
- Any claim that Unity, Daimler, or another fixture is admitted or score-ready.

Selection threshold is met for architecture planning because the invariant is clear: Harness can only freeze and score already-authored, provenance-backed, leakage-controlled, label-frozen inputs, and must block rather than repair missing upstream work. The core/satellite split is clear enough for owner review and later planning. The target remains planning-only.

## Core And Satellite Boundaries

Core:

- Harness Entry Bundle interface.
- Admission status vocabulary.
- Contestant-visible boundary.
- Facilitator-only boundary.
- Harness freeze inputs.
- Deterministic checking and scoring boundary.
- Report meaning and non-meaning.
- Inadmissibility and quarantine states.
- Non-claims.

Satellite:

- Unity-specific fixture details.
- Daimler fallback specifics.
- Legacy sealed-memo adapter notes.
- Case-family-specific evidence adapter choices.
- Future file layout, runtime code, tests, package setup, CI, and dashboards.
- Parent Judgment Spine lesson promotion and product-proof interpretation.

## Harness Entry Bundle

The Harness Entry Bundle is a Packing-owned admission object, not an implementation package and not a scoreable fixture by itself.

Minimum bundle surfaces:

- `case_identity`: case ID candidate, decision question, cutoff, role frame, authority constraints, capability constraints, permitted assumptions, forbidden-information notice.
- `participant_packet_candidate`: packet-safe Markdown surface and source manifest, with draft/frozen status.
- `evidence_registry_candidate`: evidence IDs, source IDs, source, timestamp, retrieval timestamp, hash, pre-decision status, pre-decision basis, and summary, or explicit missingness.
- `provenance_and_cleaning_receipt`: source hashes or hash gaps, retrieval timestamps or timestamp gaps, cleaning/normalization trace status, cutoff basis, and transformation caveats.
- `visibility_boundary`: contestant-visible material, facilitator-only material, parent-only material, and excluded material.
- `leakage_and_spoiler_receipt`: actual outcome exclusions, post-cutoff exclusions, sealed memo/calibration/reveal exclusions, known fame risk, memorization-probe requirement, and contamination notes.
- `adapter_gap_ledger`: unresolved source-visibility gaps, protocol-versus-schema mapping gaps, legacy sealed-memo treatment, case-specific conversion decisions, and whether each gap blocks admission.
- `facilitator_ledger_work_queue`: candidate label work, must-address candidates, underreach observability candidates, and second-label needs, explicitly not frozen scoring truth.
- `admission_request`: requested state: `draft_only`, `admit_candidate`, `quarantine_request`, or `reject_request`, with reasons.

The bundle may be well-structured and still inadmissible. Structure is not admission.

## Packing-Owned Outputs

Packing owns:

- Draft or clean participant packet candidate.
- Source manifest shape.
- Evidence registry candidate.
- Provenance receipt, including hashes, retrieval timestamps, pre-decision basis, and known gaps.
- Cleaning-trace receipt or explicit missing cleaning-trace blocker.
- Cutoff and spoiler boundary.
- Participant-facing versus facilitator-only separation.
- Parent-only exclusions.
- Leakage notes that later map into facilitator ledger fields or protocol metadata.
- Source-gap and adapter-decision ledger.
- Candidate must-address items and label-work queue.
- Draft admission request and inadmissibility self-check.

Packing does not own:

- Source acquisition or raw-signal preservation.
- ECR receipt mechanics.
- Cleaning, normalization, dedupe, translation, or transformation mechanics.
- Final band-input truth.
- Final second-label resolution as scoring truth unless a later owner lane explicitly assigns that to Packing.
- Deterministic action-band derivation.
- Scoring, probe execution, model runs, reports, failure logging, or lesson promotion.

## Harness-Owned Freeze Inputs

Harness owns the decision to freeze and admit only after required inputs exist.

Harness freeze/admission inputs:

- Canonical case ID.
- Participant packet hash.
- Evidence registry state and source-byte hash state.
- Facilitator ledger with mapping table version pin.
- Frozen band inputs.
- Second-label diffs, even if empty.
- Must-address items.
- Underreach observability.
- Leakage audit notes and spoiler inventory.
- Ledger committed timestamp.
- Ledger freeze hash.
- Memorization probe result for the target contestant/model family before packet exposure.
- BlindJudgement schema instance, if scoring is requested.
- Run metadata, prompt hash, participant packet hash, facilitator ledger hash, and mapping version pin.

Harness must not author these missing inputs to proceed. It may mark the case `draft_only`, `adapter_blocked`, `quarantined`, or `rejected`, and it may produce mechanical failure records only when the relevant harness step is actually authorized and run in a later lane.

## Contestant-Visible Boundary

Contestants may see:

- Clean participant packet.
- Packet-safe case identity, decision question, cutoff, role frame, authority constraints, capability constraints, known uncertainties, permitted assumptions, forbidden-information notice, and source manifest.
- Packet-safe evidence summaries.

Contestants must not see:

- Actual outcome.
- Actual decision if avoidable.
- Post-cutoff facts or post-decision interpretation.
- Frozen band inputs.
- Derived action floor or action ceiling.
- Facilitator ledger.
- Must-address items.
- Hidden severe-error labels or decoy labels.
- Memorization-probe result or fame-risk classification.
- Sealed memo recommendation.
- Owner blind-read input.
- Outcome calibration.
- Reveal readout.
- Product-proof implications.
- Scoring hints, failure-event classifications, or parent-only lessons.

Semantic leakage remains partly review/operator work. Harness admission should check declared boundaries and hard markers, but it must not pretend it can prove all semantic non-leakage mechanically.

## Deterministic Scoring And Checking Boundary

Harness deterministic checks may include only:

- Schema validation.
- Version/hash consistency checks.
- Pure enum-to-action-band mapping from frozen `BandInputs`.
- Inclusive band scoring.
- Overreach and underreach distance formulas.
- Underreach-primary gate from frozen `underreach_observability.present`.
- Evidence ID presence checks.
- Excluded/post-decision evidence citation checks.
- Load-bearing claim citation presence.
- Must-address ID coverage.
- Mapping-version mismatch refusal.
- Case report dump from existing scoring results.
- Append-only failure event logging after authorized execution.

Harness deterministic checks do not prove:

- Semantic evidence support.
- Direct versus inferential support.
- Contradiction handling.
- Full leakage absence.
- Model output repeatability.
- Memorization absence after a probe pass.
- Judgment quality.
- Harness superiority.
- Product proof.
- Lesson transfer.

## Report Meaning And Non-Meaning

A v0.14 harness report means:

- Fixed inputs and fixed contestant output were mechanically processed under the stated v0.14 mapping/scoring/version/hash contract.
- In-band, over-band, under-band, distance, shallow evidence-ID, must-address, probe-result, and failure-event fields were reported according to the loaded v0.14 specs.
- Failures may have been logged as events if the corresponding run was actually authorized and executed.

A v0.14 harness report does not mean:

- The case was a valid product proof.
- The harness improves judgment.
- The harness beats a baseline or structured pipeline.
- Semantic support was validated.
- Model memory was absent.
- The packet was free of all leakage.
- Lessons are promoted.
- Failure logs are reusable rules.
- Memory compounded.
- The implementation is ready or authorized.
- The source artifacts are accepted or promoted as source of truth.

## Inadmissibility And Block States

Use block states before execution. Do not silently repair.

```yaml
admission_states:
  draft_only:
    meaning: artifact can be inspected or patched as docs, but cannot be used for contestant exposure, probe-dependent admission, scoring, or case reports
  adapter_blocked:
    meaning: case-specific source, schema, protocol, sealed-memo, or visibility mapping is unresolved
  quarantine:
    meaning: material may be retained but cannot proceed until owner/operator review resolves a material risk
  reject:
    meaning: case or bundle should not be used for the requested harness path under current facts
  admit_for_freeze:
    meaning: inputs are complete enough for a later authorized harness freeze step; not validation or score-readiness by itself
  score_blocked:
    meaning: fixture may have frozen upstream surfaces but lacks a valid blind judgment, run metadata, probe state, version match, or scoring authorization
```

Block or quarantine when any of these are missing or unresolved:

- Provenance receipt.
- Source-byte hashes where source bytes are available.
- Retrieval timestamps.
- Pre-decision status.
- Pre-decision basis.
- Cleaning trace or explicit upstream trace status.
- Cutoff safety.
- Participant/facilitator separation.
- Source-gap adapter decision.
- Leakage or spoiler receipt.
- Participant packet hash.
- Evidence registry freeze/hash state.
- Facilitator ledger.
- Frozen band inputs.
- Second-label diffs and disagreement resolution.
- Must-address items.
- Underreach observability.
- Mapping table version pin.
- Ledger freeze hash.
- Decision shape.
- Memorization probe result for target contestant/model family.
- Schema-valid BlindJudgement.
- Run metadata and prompt hash.
- Sealed-memo comparability caveat, if a legacy memo is involved.

Specific hard stops:

- Memorization probe `fail`: reject or quarantine the contestant-case pair for that model family.
- Memorization probe `ambiguous`: quarantine until operator review.
- More than three band-input disagreements before resolution: quarantine under the labeling rubric.
- Disagreement involving `ruinous_tail` or `expiring` that cannot be resolved: quarantine.
- Mapping version mismatch: refuse to score unless a separately authorized rescore path exists.
- Participant-facing leakage from outcome, reveal, sealed memo, calibration, hidden labels, or post-cutoff material: rebuild or reject the participant-facing packet.
- Adapter layer infers missing labels, provenance, source hashes, timestamps, or sealed-memo comparability: reject the adapter output.

## Deferred Implementation Implications

These implications are preserved for later scoping only. They do not authorize code.

If a later owner-authorized implementation-scoping lane accepts this architecture, it should inherit these non-executable implications:

- Model the Harness Entry Bundle as an admission surface, not as a runtime package with implied execution.
- Keep adapter decisions explicit and block-first.
- Preserve protocol-versus-Pydantic differences instead of silently normalizing them.
- Require version and hash fields before scoring.
- Keep scoring functions pure and deterministic over frozen enum inputs.
- Keep semantic evidence checking out of Phase 1 scoring unless a later harness version explicitly adds it.
- Keep failure logs append-only and non-promotional.
- Prevent scorer/report layers from importing LLM calls.
- Preserve one contestant runner shape if implementation later follows v0.14 infrastructure architecture.

Before any implementation scope exists, a later lane would need to reopen `phase_1_infrastructure_architecture.md`, recheck current source hashes, bind exact target files, and obtain explicit bounded implementation authorization.

## What Is Intentionally Undecided

- Exact serialized bundle format.
- Whether the bundle is one file, a folder receipt, or a set of linked artifacts.
- Exact adapter schema.
- Whether protocol fields such as `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk` become direct schema fields or remain protocol metadata.
- Whether Packing or a separate operator lane freezes final band labels.
- Whether Unity, Daimler, or another case should be the first non-Unity pressure test.
- Any runtime repo layout.
- Any validation commands, tests, CI gates, package names, runners, or report files.
- Any product-proof, buyer-proof, or lesson-promotion standard.

## What Would Change The Recommendation

Reopen this recommendation if:

- Orca accepts a different Data Capture, Cleaning, Packing, Judgment, or Harness phase boundary.
- A later harness version supersedes v0.14 and changes the participant packet, evidence registry, ledger, scoring, probe, or failure-log contract.
- Owner direction says Harness should own case construction or Packing should own final frozen scoring labels.
- A second non-Unity case exposes a generic bundle field not represented here.
- The adapter layer cannot remain block-first in practice.
- Formal bundle overhead adds more bloat than boundary safety.
- A future accepted Packing Spine makes the current initial Packing README materially obsolete.

## Bloat-Cut Queue

Cut from this architecture:

- Cleaning -> Harness direct handoff.
- Harness-owned packing.
- Harness repair of provenance, cleaning trace, labels, source gaps, or leakage.
- Case-specific manual fixture authoring as the general interface.
- Unity-specific fields as interface fields.
- Runtime layout, package/test/build work, runners, probes, model calls, scoring runs, and validation.
- Semantic evidence checker.
- Dashboards or reports beyond v0.14 YAML-style mechanical report meaning.
- Memory/rules/retrieval directories.
- Lesson-promotion mechanics.
- Product-proof or buyer-proof claims.
- Runtime model recommendations.
- Broad repo-map or manifest updates from this artifact alone.

## Non-Claims

This artifact does not claim:

- Judgment Spine validation.
- v0.14 harness validation.
- case admission.
- participant-packet cleanliness for blind use.
- memorization-probe pass.
- scoring readiness.
- implementation readiness.
- source-of-truth promotion.
- acceptance or approval.
- buyer validation.
- product readiness.
- feature readiness.
- commercial readiness.
- model-training readiness.
- harness superiority.
- memory compounding.
- lesson transfer.
- lesson promotion.
- that Unity should own the interface.
- that Daimler is accepted as a fixture.
- that dirty or untracked sources are accepted authority.

## Smallest Complete Next Routing Object

The smallest complete next routing object is owner review of this architecture artifact.

If the owner accepts the target architecture, the next docs-only step should be one of:

- a narrow Harness Entry Bundle contract note that defines the bundle fields and admission states without implementation;
- a non-executing implementation-scoping prompt, but only after explicit owner acceptance and explicit bounded implementation-scope authorization;
- a second non-Unity pressure-test of the interface, likely against Daimler or another lower-fame-risk case, to check whether the bundle fields are generic.

Do not route directly to implementation, probe execution, model runs, scoring, validation, proof-run, product proof, lesson promotion, or harness-superiority claims from this artifact.

## Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| Current user prompt | Controlling architecture question, source pack, output path, subagent requirement, hard boundaries, closeout contract | user-stated |
| `AGENTS.md` | Orca workspace operating constraints and docs-write/implementation boundary | read |
| `.agents/workflow-overlay/README.md` | Overlay binding rule | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/source-loading.md` | Source-loading budget, preflight receipt, dirty-state caveats, source-heavy economy | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-gated method sequencing, output modes, repo-aware prompt/write boundaries | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted `docs/research/` artifact location | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/artifact-roles.md` | Research artifact role and permissions | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | read |
| `.agents/workflow-overlay/validation-gates.md` | Completion, strict-claim, and dirty-state validation boundaries | read; modified in worktree before this artifact |
| `.agents/workflow-overlay/review-lanes.md` | Review/subagent advisory and non-claim boundaries | read; modified in worktree before this artifact |
| `docs/workflows/orca_repo_map_v0.md` | Navigation map for Judgment Spine and research areas | read; modified in worktree before this artifact |
| `workflow-architecture-planning` skill | Reference-loaded for method mechanics only | read-only method reference |
| `docs/research/packing-phase/README.md` | Packing purpose, owns/does-not-own, harness handoff boundary | hash verified; read |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 source-of-truth roles and reading order | hash verified; read |
| `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md` | Minimum harness-entry shape, bridge blockers, non-claims | hash verified; read |
| `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md` | Unity exemplar extraction/admission gates and draft fixture blockers | hash verified; read |
| `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md` | Parent Judgment Spine and v0.14 boundary, drift guard, implementation non-authorization | hash verified; read |
| `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md` | Harness thesis and Phase 1 claim discipline | read |
| `docs/research/judgment-spine/harness/v0_14/judgement_harness_strategy.md` | Harness identity, Phase 1 contestants, label and memory boundaries | read |
| `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md` | Four-lane case structure, packet/ledger/evidence requirements, acceptance/quarantine criteria | read |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` | Pydantic-ready contracts for packet frontmatter, EvidenceUnit, FacilitatorLedger, BlindJudgement, ScoringResult, CaseReport, FailureEvent | read |
| `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md` | Contestant output, runner metadata, repair policy, artifact policy | read |
| `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md` | Labeling workflow, second-label requirements, quarantine rules | read |
| `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md` | Frozen v0.14 mapping constants | read |
| `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md` | Pure deterministic mapping function and version-pin behavior | read |
| `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md` | Scoring formulas, shallow evidence checks, non-scores | read |
| `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md` | Probe handling, fail/ambiguous/pass limits | read |
| `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md` | Failure log schema and non-promotion policy | read |
| `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md` | Phase 1 proof and memory non-claims | read |
| `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md` | Deferred implementation implications only | read; not used as implementation authorization |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md` | Unity draft fixture inventory and blocked-before-scoring status | optional exemplar read |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md` | Concrete contestant-visible draft and draft-only blockers | optional exemplar read |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md` | Concrete registry gaps and per-source hash/timestamp blockers | optional exemplar read |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md` | Concrete ledger freeze, label, second-label, and probe blockers | optional exemplar read |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md` | Legacy sealed-memo non-comparability and adapter blockers | optional exemplar read |
| `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_draft_fixture_pack_pp_01_recheck_adversarial_review_v0.md` | PP-01 closure and participant leakage/review-use boundary | optional exemplar read |

Sources deliberately not loaded in full: all case folders, all prompts, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, and runtime files. They were not needed to decide this bounded interface architecture and would have widened beyond the prompt.
