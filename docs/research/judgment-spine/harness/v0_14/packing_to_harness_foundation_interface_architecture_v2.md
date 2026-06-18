# Packing Phase To v0.14 Judgment Harness Foundation Interface Architecture (Adjudicated) v2

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Adjudicated docs-only target architecture for the Packing Phase -> v0.14 Judgment Harness Foundation interface, produced by adjudicating the GPT-authored v1 candidate against loaded sources.
use_when:
  - Deciding whether a packed case can be admitted, rejected, quarantined, adapter-blocked, or held draft before v0.14 harness execution.
  - Separating Packing-owned bundle construction from operator labeling/freeze and from Harness-owned admission, deterministic scoring, reports, and failure logs.
  - Preparing later owner review or a separately authorized implementation-scoping lane without authorizing implementation, probes, scoring, validation, or product proof.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v1.md
  - docs/research/packing-phase/README.md
  - docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
input_hashes:
  candidate_v1__packing_to_harness_foundation_interface_architecture_v1.md: 88B15FF87C7746C91AAC30E467BF0E278D5311FDFB00FC53CB481848BE5604D0
  docs/research/packing-phase/README.md: 46E79573EDFFE48F084E49A746A925A71BC9D00C07E7EDAF1C0624ED4D2FA80D
  docs/research/judgment-spine/harness/v0_14/index.md: 7038B2443E9EC96723A98359899A8975E0E42A5B45E8DFFD886EE393E3445C4F
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 4AF1F45964DBB560D7C6E02827BC30A9161D4433EA754580239C122DAEF532A5
branch_or_commit: main @ b7627d3389eeaa8456c65974039ada0e519617bc (dirty pre-existing workspace state allowed and reported; controlling sources untracked)
stale_if:
  - v0.14 is superseded by a later harness version.
  - Pydantic FacilitatorLedger schema adds case_family, decision_shape, memorization_probe_required, or known_fame_risk as first-class fields.
  - Packing-phase README ownership or the Core Spine Data Capture/Cleaning boundary (Inclusion State Rule) materially changes layer ownership.
  - The band-input labeling rubric changes the labeling actor or freeze workflow.
  - A second non-Unity fixture exposes a generic interface field missing here.
  - A later owner decision authorizes a different bundle topology or admission gate.
```

- Status: TARGET_RECOMMENDED (adjudicated; candidate accepted with modifications)
- Artifact type: Architecture adjudication artifact
- Output mode used: file-write
- Candidate adjudicated: `packing_to_harness_foundation_interface_architecture_v1.md` (GPT-authored)
- Candidate disposition: MODIFIED ACCEPT
- Implementation authorized: no
- Runtime, package, test, schema-as-code, hashing routine, probe runner, leakage validator, sealed-memo/legacy-prior-judgment adapter generator, admission-gate function, automation, commit, push, PR, model run, probe execution, scoring execution, validation execution, proof-run, product proof, or lesson promotion authorized: no
- Strict acceptance, validation, readiness, source-of-truth promotion, implementation authorization, probe pass, score-readiness, baseline comparability, harness superiority, semantic evidence support, buyer proof, feature/commercial readiness, or memory-compounding claims: not proven

## Adjudication Receipt

This artifact is the adjudicated output of the Packing -> Harness Foundation interface architecture decision. It consumes a GPT-authored candidate, independently source-checks it, and renders an architecture adjudication. It is an adjudicated architecture recommendation only. It is **not** owner acceptance, validation, readiness, implementation authorization, scoring authorization, probe pass, product proof, lesson promotion, or a harness-superiority claim.

```yaml
adjudication:
  candidate_path: docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v1.md
  candidate_author_style: GPT (generic-gpt55 template posture; not a runtime model claim)
  disposition: modified_accept            # accept | modified | rejected | no_selection
  architecture_result: TARGET_RECOMMENDED
  selected_target: block_first_hybrid_harness_entry_bundle_interface
  preserved_from_candidate:
    - option selection and option comparison (AO-1..AO-5; AO-5 selected)
    - HEB minimum bundle surfaces and Packing/Harness split
    - admission_states vocabulary (draft_only/adapter_blocked/quarantine/reject/admit_for_freeze/score_blocked)
    - "structure is not admission" principle
    - deterministic scoring/checking boundary, report meaning/non-meaning
    - non-claims catalog and bloat-cut queue
    - stale_if / "what would change the recommendation" reversibility posture
  modifications_applied: [M1, M2, M3, M4, M5, M6, M7, M8]   # see "Adjudication Modifications Folded In"
  rejected_or_not_inherited:
    - none of the candidate's claims were rejected as unsupported; all changes are sharpenings, not reversals
  method: workflow-architecture-planning (standard profile), applied after SOURCE_CONTEXT_READY
```

## Candidate Consumed And Hash

- Candidate: `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v1.md`
- Candidate SHA256: `88B15FF87C7746C91AAC30E467BF0E278D5311FDFB00FC53CB481848BE5604D0`
- Candidate self-identifies as `ARCHITECTURE_PLANNING_V1_RELOCATION_COPY`, `TARGET_RECOMMENDED`, target = block-first hybrid Harness Entry Bundle.

Prompt-named candidate path note: the commissioning adjudicator prompt named the candidate at `docs/review-inputs/packing_to_harness_foundation_interface_architecture_gpt55_candidate_v0.md`. That path does not exist in the repo (only `docs/review-inputs/README.md` is present). The operator explicitly redirected the candidate to the v1 artifact above; the candidate path was therefore taken from explicit current-turn user instruction (source hierarchy #1), not from memory.

## Source Context Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus the GPT v1 candidate, the five prompt-pinned task sources, the Core Spine Data Capture/Cleaning boundary note, band-input labeling rubric, pydantic schema reference, and (via the three adjudication subagents) proof_and_memory_plan, failure_event_log_spec, memorization_probe_protocol, judgement_case_construction_protocol, blind_judgement_schema_and_harness_protocol, and phase_1_infrastructure_architecture (deferred-implication read only).
  edit_permission: docs-write
  target_scope: Create docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v2.md only (collision-bumped from v0; see Version And Collision Note).
  dirty_state_checked: yes
  blocked_if_missing: no
workspace_preflight:
  expected_branch: main
  actual_branch: main
  expected_head: b7627d3
  actual_head: b7627d3389eeaa8456c65974039ada0e519617bc
  dirty_state: allowed_and_reported  # git porcelain reported 117 entries; controlling task sources are untracked
source_context_status: SOURCE_CONTEXT_READY
method_sequence:
  workflow_architecture_planning_reference_loaded: yes
  applied_only_after_source_context_ready: yes
  profile: standard
  subagents_launched: 3
hash_drift_handling:
  pinned_hashes_matched: 3 of 5
  pinned_hashes_drifted: 2 of 5
  drifted_sources:
    - path: docs/research/packing-phase/README.md
      pinned: E108281113DA1C27DB241BBB600B19D79334CB407707C6234EE1E1264626EF06
      current: 46E79573EDFFE48F084E49A746A925A71BC9D00C07E7EDAF1C0624ED4D2FA80D
      drift_cause: navigation-pointer addition (open_next now lists the v0 interface artifact); boundary content materially unchanged
    - path: docs/research/judgment-spine/harness/v0_14/index.md
      pinned: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
      current: 7038B2443E9EC96723A98359899A8975E0E42A5B45E8DFFD886EE393E3445C4F
      drift_cause: Bridge Foundation table row added pointing at the v0 interface artifact; source-of-truth roles, reading order, and code-ready gate unchanged
  resolution: re-pinned to current recomputed hashes; both drifts confirmed immaterial to the architecture decision by reading current content; all strict claims remain not proven per the overlay control-plane source-state gate.
```

Repository-state and authority caveat. The workspace was dirty before this artifact was written, and the controlling task sources are untracked. Per `.agents/workflow-overlay/validation-gates.md` (control-plane source-state gate), modified or untracked controlling sources may support advisory architecture work but do **not** establish strict `PASS`, acceptance, source-of-truth, validation, readiness, or proof status unless owner acceptance or controlling authority is explicit. This adjudication is advisory architecture planning; it makes no strict claim. The two drifted pins were resolved by re-pinning to current recomputed hashes after confirming the drift was a navigation-pointer addition that does not change the boundary the candidate relies on.

## Subagent Evidence Disclosure

```text
Subagents launched: 3
Evidence mode: delegated lane adjudication subagents (source-fidelity, boundary-leakage, architecture-quality)
Delegation runtime: inherited/default agent type and model (general-purpose)
Reason: the adjudicator prompt required exactly three advisory adjudication subagents; the host supports delegation.
```

Each subagent received the candidate path plus a bounded source list, performed its own source-readiness gate, read repo source directly, and returned advisory findings only. No subagent output is a verdict, validation, readiness evidence, implementation authority, or proof. The adjudicator owns synthesis below and does not treat subagent agreement as proof.

### Source-Fidelity Subagent (summary)

No critical or major source-fidelity defects. The candidate's HEB surfaces map cleanly to the bridge foundation's "Minimum Harness-Entry Shape"; the deterministic-scoring list matches `pydantic_schema_reference.md` (`ScoringResult`, `EvidenceIdCheckResult`) and `proof_and_memory_plan.md`; probe handling matches `memorization_probe_protocol.md` (`fail` -> reject/quarantine for that model family; `ambiguous` -> quarantine until operator review); failure-log non-promotion matches `failure_event_log_spec.md`; quarantine triggers match `band_input_labeling_rubric.md`. No invented Pydantic fields; the admission-state vocabulary is disclosed as interface vocabulary, not schema. The `case_family`/`decision_shape`/`memorization_probe_required`/`known_fame_risk` deferral is accurate (present in the case-construction protocol, absent from the Pydantic `FacilitatorLedger`).

### Boundary-Leakage Subagent (summary)

No hard ownership misassignment leak. Two MAJOR under-specifications: (1) the candidate places `pre_decision_status`/`pre_decision_basis` in the Packing-owned registry without stating that **final** integrity-exclusion / decision-use-downgrade is Judgment-owned per the Core Spine "Inclusion State Rule" and the thesis operating contract — readable as Packing creep into Judgment authority; (2) the candidate marks the band-label freeze owner "undecided" when `band_input_labeling_rubric.md` already specifies operator-resolves-and-freezes. Correctly bounded: Packing does-not-own list, Harness block-don't-repair, failure-log/lesson-promotion separation.

### Architecture-Quality Subagent (summary)

Two CRITICAL: (1) two conflicting admission-state vocabularies — the bundle's `admission_request` enum (`draft_only/admit_candidate/quarantine_request/reject_request`) does not map 1:1 to the Harness `admission_states` enum (`draft_only/adapter_blocked/quarantine/reject/admit_for_freeze/score_blocked`); (2) a fake-success seam — "source-byte hashes where source bytes are available" plus "evidence registry candidate ... or explicit missingness" lets an all-missing / all-"bytes-unavailable" registry pass structure with zero real hashes (the Unity EU-08 pattern), so "structure is not admission" is asserted but not fully enforced. Two MAJOR: admission/block states are narrative end states (not mechanically enforced in a docs artifact, so "turns missing X into inadmissibility states" overclaims present enforcement); residual Unity overfitting in the leakage/spoiler surface (sealed-memo/calibration/reveal/fame-risk hardcoded). Version coupling and implementation gravity are mostly handled.

## Architecture Question

### Stated

What target architecture should govern the boundary between Packing Phase outputs and Judgment Harness Foundation inputs so that Packing can transform cleaned evidence into judgment-ready case artifacts; the Harness can freeze inputs and run deterministic checks without absorbing Packing / Cleaning / Data Capture / lesson-promotion responsibilities; future implementation scoping has a stable interface; and missing provenance, leakage, unresolved evidence adapters, or missing labels block admission instead of being silently repaired by the harness?

### Inferred

Whether label freezing is a Packing output, a Harness Foundation behavior, or a distinct operator labeling step in between. The `band_input_labeling_rubric.md` workflow (primary labeler = `operator_or_case_constructor`; second labeler; operator resolves diffs and freezes) and the Core Spine "Inclusion State Rule" (integrity-exclusion / decision-use-downgrade are Judgment-owned) force the inference that an **operator labeling step** sits between Packing draft outputs and Harness admission, owning ledger freeze and final evidence inclusion status — even though it is neither Packing-as-truth nor Harness-Foundation-owned.

## Options Compared

The candidate's option comparison was sound and is preserved. Summarized:

| Option | Shape | Result |
| --- | --- | --- |
| AO-1 Cleaning feeds Harness directly | Cleaning outputs normalized evidence straight into harness fixtures. | Rejected — violates `packing-phase/README.md` cleaned-vs-judgment-ready distinction; Harness would receive evidence before participant/facilitator separation and labels exist. |
| AO-2 Packing emits a formal Harness Entry Bundle | Packing emits packet/registry/provenance/leakage/gap surfaces; Harness consumes. | Retained only inside the hybrid — insufficient alone unless Harness owns freeze/admission/scoring and adapters are hard-stop block states. |
| AO-3 Harness owns packing/admission internally | Harness constructs or repairs packets, registry, labels, admission. | Rejected — collapses Harness into Packing/Cleaning/Data Capture; hidden implementation gravity; lets deterministic scoring inherit repaired gaps. Contradicts the README handoff boundary. |
| AO-4 Manual case-specific fixtures, no general interface | Each fixture authored ad hoc. | Rejected as target (retained as exemplar-only practice) — no stable prepare-or-reject surface; Unity-specific drift; admission becomes operator memory. |
| AO-5 Hybrid: Packing owns bundle construction; operator labeling step freezes; Harness owns admission/scoring; small block-first adapter layer | Formal Packing-owned HEB + operator-owned label freeze + Harness-owned non-repairing admission/freeze/scoring/report/failure-log; explicit, small, block-first adapters. | **Selected.** |

## Adjudicated Target Architecture

```yaml
architecture_result: TARGET_RECOMMENDED
selected_target: block_first_hybrid_harness_entry_bundle_interface
candidate_disposition: modified_accept
```

A block-first hybrid interface with three operating zones plus a small adapter set:

1. **Packing** owns construction of a draft/clean **Harness Entry Bundle (HEB)** — a named admission object, not an implementation package and not a scoreable fixture by itself.
2. An **operator labeling step** (per `band_input_labeling_rubric.md`: primary labeler `operator_or_case_constructor`, second labeler, operator resolves diffs and freezes) owns the **frozen facilitator ledger**, final band-input labels, and — under Judgment authority per the Core Spine "Inclusion State Rule" — the **final** evidence `pre_decision_status`. The labeling operator may be the same human as the Packing operator in small operations, but the frozen ledger is not a Packing-as-truth output.
3. The **v0.14 Harness Foundation** owns admission decision, hash recomputation, schema validation, deterministic action-band derivation, deterministic scoring, case reports, and append-only failure logging. It blocks rather than repairs.
4. A small **adapter layer** records case-specific gaps (source-visibility gap, legacy-prior-judgment / sealed-memo treatment, protocol-to-Pydantic field carry). Adapters surface and block; they never infer or repair missing provenance, labels, hashes, or comparability.

Selection threshold met: a stable invariant is clear (the Harness can freeze and score only already-authored, provenance-backed, leakage-controlled, label-frozen inputs, and must block rather than repair upstream work); the core/satellite split is clear enough to prevent boundary leakage; non-goals are enumerated; no unresolved upstream product/feature/authority blocker would change the target.

This is a planning recommendation. It is not implementation authority, validation, approval, readiness, deployment safety, resolver proof, or plugin readiness.

## Why The Target Wins

- It gives future CAs/operators a stable prepare-or-reject surface while preserving the source-backed phase split (`packing-phase/README.md`, Core Spine boundary, `judgment_spine_thesis_operating_contract_v0.md`).
- It converts missing provenance, leakage, unresolved adapters, missing labels, missing probe state, and missing hashes into **inadmissibility states** a future admission gate must enforce, instead of harness repair work.
- It isolates the operator labeling step and Judgment-owned exclusion authority instead of letting Packing finalize labels or exclusion, and instead of letting the Harness author them.
- It is reversible: phrased as "v0.14 currently requires," carries a `stale_if` clause, and asks for a second non-Unity pressure test before broad stability claims.

## Adjudication Modifications Folded In

These eight modifications are the adjudication's substantive output. Each is source-grounded and sharpens the candidate without reversing it.

- **M1 — Evidence inclusion status is Judgment-owned at finalization (boundary).** Packing records a **proposed/candidate** `pre_decision_status` plus `pre_decision_basis` (provenance facts: `evidence_id`, `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, `summary`). The **final** `pre_decision_status` — specifically integrity-exclusion (`excluded`) and decision-use-downgrade — is assigned by the operator labeling step under Judgment authority, per `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` "Inclusion State Rule" and `judgment_spine_thesis_operating_contract_v0.md`. Admission blocks if the final status is missing or still tagged proposed. (Source: Core Spine Inclusion State Rule; thesis contract.)
- **M2 — Band-label freeze owner is the operator labeling step, not "undecided."** The freeze owner is specified by `band_input_labeling_rubric.md` (operator resolves diffs and freezes; emits `ledger_freeze_hash`, `committed_at`, `labeling_rubric_version`). The interface binds this. What remains genuinely undecided is narrower: whether the labeling operator is a separate human/role from the Packing operator (owner/per-case policy), not *who freezes*. (Source: labeling rubric workflow.)
- **M3 — One admission-state model with a request -> decision crosswalk.** The candidate's two vocabularies are reconciled: Packing emits a **request**; the Harness emits a **decision**. See "Admission State Model." (Resolves architecture-quality CRITICAL #1.)
- **M4 — Close the hash fake-success seam.** Each evidence unit must declare `bytes_available: true|false`. When true, a source-byte `hash` is mandatory. When false, an explicit justification is required and the unit routes to the source-visibility-gap adapter (`adapter_blocked`), never a silent pass. An all-missing / all-"bytes-unavailable" registry without per-unit justification is inadmissible. "Structure is not admission" is backed by these explicit block conditions. (Source: `pydantic_schema_reference.md` `hash` rule; Unity EU-08 in the extraction plan. Resolves architecture-quality CRITICAL #2.)
- **M5 — Block states are required end states, not present enforcement.** This docs artifact defines the inadmissibility states a future admission gate must enforce; it does not itself mechanically enforce them. The candidate's "turns missing X into inadmissibility states" is restated accordingly. (Resolves architecture-quality MAJOR.)
- **M6 — Generalize Unity-specific leakage surfaces.** The leakage/spoiler surface is generalized to `outcome_leakage_classes` (actual outcome, post-cutoff facts, reveal/readout, outcome calibration, owner blind-read) plus an **optional** `legacy_prior_judgment` adapter slot (a pre-existing sealed memo is one instance). `known_fame_risk` and `memorization_probe_required` are case-conditional, not always-present fields. (Source: bridge foundation; Unity extraction plan. Resolves architecture-quality MAJOR overfitting.)
- **M7 — Version-coupling hygiene.** The v0.14-specific freeze-input names (`BandInputs`, `BlindJudgement`, mapping-version pin) are tagged as the **v0.14 binding** of an abstract "frozen-scoring-inputs" slot, so a later harness version can rebind without rewriting the interface. (Source: stale_if posture.)
- **M8 — Name the protocol-to-Pydantic interim carry.** `decision_shape` rides on `BlindJudgement.decision_shape`. `case_family`, `memorization_probe_required`, and `known_fame_risk` have no first-class `FacilitatorLedger` field in v0.14, so they travel inside `leakage_audit_notes` / `spoiler_inventory` text via a named protocol-to-Pydantic adapter slot (so they are not silently dropped). Whether they become first-class schema fields stays an owner decision. (Source: `pydantic_schema_reference.md` `FacilitatorLedger`; bridge foundation leakage-field mapping.)

Convergence note (advisory, not authority): the off-spec prior `_v0.md` artifact independently reached M1 (its "S1") and a heavier version of M2 (a named "Facilitator" role). This corroborates M1/M2 but is not used as source authority. This adjudication keeps M2 lighter — the rubric already names the actor as "operator," so no new role needs inventing.

## Core / Satellite Boundary

Core (interface-invariant in v0.14):

- HEB interface; admission-state model (request -> decision crosswalk).
- Packing/operator-labeling/Harness three-zone split and Judgment-owned final inclusion status.
- Contestant-visible boundary; facilitator/parent-only boundary.
- Harness freeze inputs; deterministic checking/scoring boundary.
- Report meaning and non-meaning; inadmissibility/block states; non-claims.

Satellite (bounded, per-case):

- Unity-specific fixture details; Daimler fallback specifics.
- `legacy_prior_judgment` (sealed-memo) adapter content; source-visibility-gap adapter content; case-family-specific evidence-adapter choices.
- Future file layout, runtime code, tests, packaging, CI, dashboards.
- Parent Judgment Spine lesson promotion and product-proof interpretation.

## Packing-Owned Outputs

Packing produces the draft HEB and self-checks admissibility. Packing owns:

- participant-packet candidate (Pydantic-shaped frontmatter + packet body: decision frame, cutoff, role frame, pre-cutoff facts, known uncertainties, permitted assumptions, forbidden-information notice; excludes outcome, frozen labels, derived floor/ceiling, must-address items, hidden/decoy labels, post-decision interpretation);
- source manifest;
- evidence-registry candidate: one `EvidenceUnit`-shaped entry per source unit with provenance facts, `bytes_available` declaration, and a **proposed** `pre_decision_status` + `pre_decision_basis` (final status is Judgment-owned, M1);
- provenance/cleaning receipt: source hashes or justified hash gaps, retrieval timestamps, cleaning-trace status, cutoff basis, transformation caveats;
- visibility boundary: contestant-visible vs facilitator-only vs parent-only vs excluded;
- leakage/spoiler receipt: `outcome_leakage_classes` exclusions, anti-leakage notes, and case-conditional `memorization_probe_required` / `known_fame_risk` seeds (M6);
- adapter/gap ledger: unresolved source-visibility gaps, protocol-vs-schema carries, `legacy_prior_judgment` treatment, with a per-gap "blocks admission?" flag;
- facilitator-ledger **work queue** (drafts only, explicitly not frozen scoring truth): candidate band-input rationales, candidate must-address items, candidate underreach-observability rationale;
- draft admission **request** and inadmissibility self-check.

Packing does **not** own (per `packing-phase/README.md`): source acquisition/preservation; ECR receipt mechanics; cleaning/normalization/dedupe/translation mechanics; frozen facilitator-ledger labels; final band-input truth; **final** `pre_decision_status` (M1); action-band derivation; scoring; probe execution; model runs; failure logging; lesson promotion; product-proof claims.

## Harness-Owned Freeze / Admission / Scoring Surfaces

The Harness Foundation freezes and admits only after required inputs exist, and **blocks rather than repairs**. v0.14 binding of the abstract frozen-scoring-inputs slot (M7):

- canonical `case_id`; `participant_packet_hash`; evidence-registry freeze/hash state;
- frozen `FacilitatorLedger` (operator output): `labeling_rubric_version: v0_14`, `mapping_table_version_pin: v0_14_mvp`, `ledger_authors`, `second_label_diffs` (present even if empty), `frozen_band_inputs` (all 14 enum fields valid), `must_address_items`, `underreach_observability`, `leakage_audit_notes` (carrying the protocol-to-Pydantic interim content, M8), advisory `spoiler_inventory`, `committed_at` (ISO-8601 UTC, `Z`), `ledger_freeze_hash`;
- memorization-probe result for the target contestant/model family **before** packet exposure;
- schema-valid `BlindJudgement` + run metadata (`prompt_hash`, `participant_packet_hash`, `facilitator_ledger_hash`, `harness_version`, mapping-version pin) when scoring is requested.

The Harness recomputes hashes, validates Pydantic schemas, applies the `judgement_class_ladder_mapping` validator, runs deterministic action-band derivation and scoring, and writes append-only failure events with `not_a_rule: true`, `promotion_allowed: false` (raising on any `promotion_allowed=True`). It must **not** author labels, run second-label workflows, author must-address items, finalize `pre_decision_status` (M1), run probes, repair missing hashes, silently accept draft bundles, promote failures to rules, compare across cases for product proof, or claim baseline superiority.

## Admission State Model

One state model. Packing emits a **request**; the Harness emits a **decision** after checking. (M3, resolving the candidate's two-vocabulary incoherence.)

| Packing request | Meaning | Possible Harness decision(s) | Decision owner |
| --- | --- | --- | --- |
| `draft_only` | Not ready; docs inspection/patch only. | `draft_only` (hold) | Packing self-declares; Harness confirms |
| `admit_candidate` | Packing believes inputs complete; requests consideration. | `admit_for_freeze`, `adapter_blocked`, `quarantine`, `score_blocked`, `reject`, or `draft_only` | Harness |
| `quarantine_request` | Packing flags a material risk for review. | `quarantine` | Harness/operator; Judgment authority when the risk is integrity/decision-use |
| `reject_request` | Packing believes the case should not proceed. | `reject` | Harness/operator |

Harness decision states:

```yaml
admit_for_freeze: inputs complete enough for a later authorized freeze step; NOT validation or score-readiness by itself.
adapter_blocked:  a case-specific adapter gap (source-visibility, legacy_prior_judgment, protocol-to-Pydantic) is unresolved.
quarantine:       material risk; material retained but cannot proceed until owner/operator review resolves it.
reject:           case/bundle should not be used for the requested harness path under current facts.
score_blocked:    upstream surfaces frozen, but a valid BlindJudgement, run metadata, probe state, version match, or scoring authorization is missing.
draft_only:       confirmed not admissible; stays in Packing/labeling.
```

A bundle may be well-structured and still receive a non-admit decision. **Structure is not admission.**

## Contestant-Visible Boundary

Contestants see, via the single contestant runner (`one_runner_for_all_contestants`), the rendered prompt built from the frozen participant packet only: packet-safe case identity, decision question, cutoff, role frame, authority/capability constraints, known uncertainties, permitted assumptions, forbidden-information notice, source manifest, and packet-safe evidence summaries.

Contestants do **not** see: any `outcome_leakage_class` (actual outcome/decision, post-cutoff facts, reveal readout, outcome calibration, owner blind-read); frozen band inputs; derived action floor/ceiling; the facilitator ledger; must-address items; hidden/decoy labels; memorization-probe result or `known_fame_risk`; any `legacy_prior_judgment` content (e.g., a sealed memo); scoring hints, failure-event classifications, or parent-only lessons; other contestants' outputs.

Semantic leakage remains partly operator/review work. Harness admission checks declared boundaries and hard markers; it must not pretend it can prove all semantic non-leakage mechanically. The v0.14 schema-repair policy (one repair attempt by a separate `schema_repair_assistant`; no contestant prompt rerun; save `raw_model_output.txt` and record `schema_validity: false` on failure) is owned by the v0.14 spec and preserved unchanged.

## Deterministic Checking Boundary

Deterministic at scoring time (all backed by `pydantic_schema_reference.md` / `scorer_formula_spec.md` / `proof_and_memory_plan.md`): schema validation; hash/version consistency; pure enum-to-action-band mapping from frozen `BandInputs`; inclusive band scoring (`action_floor <= recommended_level <= action_ceiling`); overreach/underreach distances; underreach-primary gate from `underreach_observability.present`; evidence-ID presence; excluded/post-decision evidence citation checks; load-bearing-claim citation presence; must-address ID coverage; mapping-version mismatch refusal; `memorization_probe_result` carried into `ScoringResult`; append-only failure-event logging.

Subjective at labeling time (operator, not scoring): each `BandInputs` enum value; must-address selection; underreach-observability presence/basis; leakage-audit content; `decision_shape` selection; `legacy_prior_judgment` treatment; final `pre_decision_status` (Judgment authority, M1).

Phase 1 scoring does **not** check: semantic relevance of evidence to the load-bearing claim; direct vs inferential support; contradiction across evidence; judgment-quality improvement across runs; memory compounding; baseline superiority (`proof_and_memory_plan.md` evidence-to-claim policy).

## Report Meaning And Non-Meaning

A v0.14 `ScoringResult`/`CaseReport` under this interface means: fixed inputs and fixed contestant output were mechanically processed under the stated v0.14 mapping/scoring/version/hash contract; in-band/over-band/under-band, distances, shallow evidence-ID and must-address checks, and probe-result fields were reported per the v0.14 specs; failure events, if any, were appended with `not_a_rule: true` and `promotion_allowed: false`.

It does **not** mean: the case is product-ready, buyer-validated, or commercially ready; the harness beats any baseline; contestant judgment quality is proven; semantic evidence support is proven; any lesson is promoted; memory compounded; a `legacy_prior_judgment` is comparable to a fresh contestant run; the probe pass proves there is no memorization; the Packing layer or operator labeling is validated beyond rubric/second-label discipline; the HEB is correct beyond the deterministic checks named above.

## Inadmissibility / Block States

The following are the **required end states** a future admission gate must enforce (M5). This artifact defines them; it does not mechanically enforce them and does not authorize the validators.

Packing-side blockers (HEB cannot be assembled; case stays in Packing): missing participant-packet frontmatter field; any forbidden item present in the participant packet; any `EvidenceUnit` missing `evidence_id`/`source_id`/`source`/`timestamp`/`retrieval_timestamp`/proposed `pre_decision_basis`; **`bytes_available: true` with no source-byte `hash`, or `bytes_available: false` with no justification (M4)**; missing proposed `pre_decision_status`; source-visibility gap with no adapter decision recorded; missing leakage/spoiler receipt; missing visibility boundary or parent-only exclusion list; `legacy_prior_judgment` present without adapter inputs; draft-vs-frozen marker absent or set to draft at admission; any facilitator-ledger work-queue item presented as frozen truth rather than candidate.

Operator-labeling-step blockers (HEB cannot be admitted; case stays in labeling): any `BandInputs` field not enum-valid; `second_label_diffs` absent; quarantine triggers met (>3 band-input disagreements; `evidence_strength` disagreement >1 level; `loss_shape` disagreement involving `ruinous_tail`; `information_decay` disagreement involving `expiring`); must-address items promoted verbatim from Packing candidates without re-authoring; `underreach_observability.basis` set to a non-enum value; `mapping_table_version_pin` not `v0_14_mvp`; `labeling_rubric_version` not `v0_14`; `ledger_freeze_hash` missing/mismatched; `committed_at` missing or not ISO-8601 UTC `Z`; **final `pre_decision_status` still tagged proposed (M1)**; protocol-to-Pydantic content for `case_family`/`memorization_probe_required`/`known_fame_risk` absent from `leakage_audit_notes` (M8).

Probe blockers: no probe artifact for the target model family; `probe_result: fail` -> reject/quarantine for that model family; `probe_result: ambiguous` without operator review -> quarantine.

Run-binding / scoring blockers (`score_blocked`): `decision_shape` not frozen; `participant_packet_hash`/`facilitator_ledger_hash` missing or mismatched; `prompt_hash`/`harness_version` missing; `BlindJudgement` violates `judgement_class_ladder_mapping`; `legacy_prior_judgment` asserted as a `BlindJudgement` without required fields and author-context-contamination caveat.

Cross-cutting blockers: any participant-facing content includes an `outcome_leakage_class`; any attempt to set `promotion_allowed=True`; any attempt to write to forbidden Phase-1 memory directories; any baseline-/harness-superiority computation. **Block-don't-repair is the invariant; silent repair by the Harness is itself a block-class failure.**

## Deferred Implementation Implications

Non-executable. This artifact does not authorize implementation. A later owner-authorized implementation-scoping lane would inherit (not execute): model the HEB as an admission surface, not a runtime package; keep adapter decisions explicit and block-first; close the hash seam with a per-source `bytes_available` field; preserve protocol-vs-Pydantic differences rather than normalizing them silently; require version/hash fields before scoring; keep scoring pure/deterministic over frozen enum inputs; keep semantic evidence checking out of Phase 1; keep failure logs append-only and non-promotional; prevent scorer/report layers from importing model calls; preserve one contestant runner. The likely smallest first slice is one Unity case-admission-and-scoring path. Before any code scope, the lane must reopen `phase_1_infrastructure_architecture.md`, recheck source hashes, bind exact target files, and obtain explicit bounded implementation authorization.

## What Is Intentionally Undecided

- Exact serialized bundle format (one file, folder receipt, or linked artifacts).
- Whether `case_family`/`decision_shape`/`memorization_probe_required`/`known_fame_risk` become first-class Pydantic fields or remain protocol metadata via the adapter slot (M8).
- Whether the labeling operator is a separate human/role from the Packing operator (M2 binds the freeze workflow, not the staffing).
- Whether a `legacy_prior_judgment` outputs an explicit advisory-baseline record type or rides in `advisory_phase_1_fields`.
- Whether Unity, Daimler, or another case is exercised end-to-end first.
- Any runtime repo layout, validation commands, tests, CI, package names, runners, or report files.
- Any product-proof, buyer-proof, or lesson-promotion standard.

## What Would Change The Recommendation

An owner decision authorizing Packing to own label freezing, or the Harness to own packet construction; a v0.15+ harness with materially different packet/ledger/scoring/probe/failure-log contracts; a `FacilitatorLedger` revision adding the four protocol fields as first-class; a Core Spine boundary patch reassigning Cleaning/ECR/Judgment ownership; a second non-Unity case exposing a generic bundle field missing here; evidence that the adapter layer cannot stay block-first in practice; or formal-bundle overhead exceeding its boundary-safety value.

## Bloat-Cut Queue

Do not invent from this artifact: a Cleaning->Harness direct handoff; Harness-owned packing; Harness repair of provenance/cleaning-trace/labels/source-gaps/leakage; case-specific manual fixtures as the general interface; Unity-specific fields as interface fields; a new leakage schema (leakage lives in `leakage_audit_notes`/`spoiler_inventory`); a Packing-side validator/scorer/rule engine; a new evidence schema; new ladder/judgement-class vocabulary; a Packing-side hashing routine separate from `ledger_freeze_hash`/`EvidenceUnit.hash`; a Packing-side contestant runner; a new bundle file shape beyond the per-case folder layout; a `legacy_prior_judgment` conversion engine; a back-channel from Packing to Cleaning for re-cleaning; runtime/package/test/CI/dashboard work; semantic-evidence checker; memory/rules/retrieval directories; lesson-promotion mechanics; product-/buyer-proof claims; broad repo-map or manifest rewrites from this artifact alone.

## Non-Claims

This artifact does not claim: Judgment Spine validation; v0.14 harness validation, readiness, or superiority over any baseline; Packing-layer or operator-labeling validation/completeness; memorization-probe pass for any case/model family; score-readiness or case admission for any case; `legacy_prior_judgment` comparability to fresh runs; semantic evidence support beyond v0.14 shallow checks; source-of-truth promotion of any source, the candidate, or this artifact; acceptance or approval by any reviewer/operator/lifecycle authority; implementation/runtime authorization; buyer validation, willingness-to-pay, product/feature/commercial readiness, or proof-run readiness; model-training readiness, memory compounding, or rule-promotion authority; that Unity is probe-safe or the best first scoreable candidate; that Daimler is accepted into manifest inventory; that dirty/untracked sources are accepted authority; that any subagent output is a verdict or proof; that subagent agreement constitutes proof.

## Version And Collision Note

The adjudicator prompt named the output path `..._architecture_v0.md`. That path exists (an off-spec prior architecture-planning artifact), and `..._v1.md` exists (the GPT candidate adjudicated here). Per the prompt's collision rule and the overlay default-path rule, this adjudicated artifact is written to the next free suffix, `..._v2.md`. This artifact does not claim to supersede or replace `_v0.md` or `_v1.md` as accepted authority — superseding is an owner/lifecycle action not granted here. `_v1.md` remains the consumed candidate; `_v0.md` remains a prior off-spec attempt. A future owner decision may promote, retire, or supersede any of these.

## Source-Read Ledger

| Source | Why read | State |
| --- | --- | --- |
| Current user instruction (adjudicator prompt + candidate-path redirect) | Controlling task, candidate path, output path, subagent contract, hard boundaries, closeout | user-stated (hierarchy #1) |
| `AGENTS.md` | Workspace operating constraints | clean (read) |
| `.agents/workflow-overlay/README.md` + source-of-truth, source-loading, prompt-orchestration, artifact-folders, artifact-roles, retrieval-metadata, validation-gates, review-lanes, safety-rules | Overlay authority, source-state gate, output mode, artifact role/folder, retrieval header, safety | modified/clean (read); modified overlay supports advisory work, blocks strict claims |
| `workflow-architecture-planning` skill | REFERENCE-LOAD method mechanics; applied after readiness | read-only method reference |
| `..._architecture_v1.md` (candidate) | The adjudicated candidate; hashed | untracked; hash recorded |
| `docs/research/packing-phase/README.md` | Packing owns/does-not-own + handoff boundary | untracked; **re-pinned** (drift = nav-pointer addition; immaterial) |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 source-of-truth roles, reading order | untracked; **re-pinned** (drift = nav-pointer addition; immaterial) |
| `case_to_v0_14_bridge_foundation_v0.md` | Minimum harness-entry shape; candidate suitability | untracked; hash matches pin |
| `unity_v0_14_fixture_extraction_plan_v0.md` | Concrete bundle/adapter gaps (EU-08, sealed memo, fame risk) | untracked; hash matches pin |
| `judgment_spine_thesis_operating_contract_v0.md` | Non-claims, layer boundaries, drift list | untracked; hash matches pin |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer-ownership table + Inclusion State Rule (M1) | untracked (read) |
| `band_input_labeling_rubric.md` | Labeling workflow + freeze owner (M2); quarantine triggers | untracked (read) |
| `pydantic_schema_reference.md` | Authoritative schema surface; protocol-vs-Pydantic gap (M8); hash rule (M4) | untracked (read) |
| `proof_and_memory_plan.md`, `failure_event_log_spec.md`, `memorization_probe_protocol.md`, `judgement_case_construction_protocol.md`, `blind_judgement_schema_and_harness_protocol.md`, `phase_1_infrastructure_architecture.md` | Read by the three adjudication subagents for fidelity/boundary/quality checks (probe/failure/scoring/case-folder/runner/implementation-gravity) | untracked; read by subagents (advisory) |

Not loaded (would not change the result): concrete Unity fixture drafts beyond what the extraction plan summarizes; method-validation replays; proof-run packets; review outputs; `docs/_inbox/`; full product directory; implementation code/tests/packages.

## Next Authorized Step

Docs-only. Open this adjudicated artifact (and the v0.14 index) to bind a future case-admission CA prompt for Unity or Daimler without re-deriving the boundary; or open it as the frozen interface input to a separately authorized implementation-scoping prompt that reopens `phase_1_infrastructure_architecture.md`, rechecks source state, binds one fixture scope, and obtains explicit bounded implementation authorization. Recommended near-term docs step: a second non-Unity pressure test (likely Daimler) to confirm the bundle fields are generic.

Do not route directly to implementation, probe execution, model runs, scoring, proof-run, product proof, lesson promotion, baseline-comparability claims, or harness-superiority claims.
