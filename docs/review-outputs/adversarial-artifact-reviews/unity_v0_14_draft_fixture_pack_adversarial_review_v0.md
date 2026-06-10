# Unity v0.14 Draft Fixture Pack Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Read-only adversarial artifact review of the Unity Runtime Fee v0.14 draft fixture pack and bounded discovery pointers.
use_when:
  - Reading the adversarial findings on the Unity v0.14 draft fixture pack.
  - Deciding whether owner-authorized patching of fixture-authoring defects is warranted before the draft pack feeds later implementation scoping or fixture-admission work.
  - Checking what remains not proven about score-readiness, probe-safety, packet cleanliness, sealed-memo comparability, or implementation authorization.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/prompts/reviews/unity_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/prompts/reviews/unity_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md: prompt_author_provided_above
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md: 580290C23AA8B3AF9DB12173BC1E5E5B939D55814CE039B1959AE8842CF842B2
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md: D48825BEA5F619DB8A16CC04064D19ABE3ABF17E55B7E05E1A3F97157D1D215F
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md: 35A92BCA9134CEE22AD5FA2CD37122BA8AC5C6E5BF91D1BA956F4C8C95FE6E15
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md: 8A92156CF312E8E254378E213F98C4B2D72C6EDB40258E8FDFB70C79A493C3C1
  docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md: C97272BF6BCAED5DBE3731F40BF3D49F71EC8C1AA20C23E4F69BB67C085D7FD6
  docs/research/judgment-spine/harness/v0_14/index.md: 59194297235C65E099C356D5141C6B2D64C4E21AECD5A1F13CD364BAD37F7163
  docs/research/judgment-spine/manifest_v0.md: E79CC2FDF22F58059A71BC12116F51DB411689304AE4228C9DB21F92CACEC644
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
```

- Status: REVIEW_COMPLETE_FINDINGS_FIRST
- Artifact type: Adversarial artifact review report
- Review lane: adversarial artifact review (Orca review-lanes.md)
- Reviewer write permission: read-only, except writing this report
- Output mode: review-report
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, PR, model run, probe execution, scoring, validation execution, fixture admission, case report creation, lesson promotion, source-of-truth promotion, deployment, install, resolver behavior, product proof, or harness-superiority authorized: no

## 1. Review Target And Purpose

Target: the Unity Runtime Fee v0.14 draft fixture pack and bounded discovery pointers.

Primary draft pack:

- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md`
- `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md`

Bounded discovery pointers:

- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Purpose: adversarially check whether the draft pack and its discovery pointers (1) satisfy the fixture-authoring commission, (2) preserve the docs-only blocked-before-scoring boundary, (3) keep the participant packet free of facilitator-only, post-cutoff, or outcome material, (4) map EU-01 through EU-08 toward v0.14 `EvidenceUnit` fields without fabrication, (5) handle EU-08 as an adapter/source-visibility gap, (6) separate direct Pydantic `FacilitatorLedger` fields from protocol fixture metadata, (7) use valid v0.14 enums, (8) avoid implying second-label audit/freeze/probe-pass/scoring/failure-event/case-report, (9) keep the sealed memo as advisory/baseline-like non-comparable material, (10) avoid strict-claim leakage, and (11) keep `index.md` and `manifest_v0.md` discovery pointers narrow.

## 2. Source Context Status

```yaml
source_context_status: SOURCE_CONTEXT_READY
```

Loaded Orca authority (overlay): `AGENTS.md`, `.agents/workflow-overlay/README.md`, `source-of-truth.md`, `source-loading.md`, `artifact-roles.md`, `review-lanes.md`, `prompt-orchestration.md`, `communication-style.md`, `validation-gates.md`, `retrieval-metadata.md`, `template-registry.md`.

Loaded commission and controlling plan: `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md`, `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`.

Loaded reviewed target: the five fixture-pack drafts and the two discovery pointers.

Loaded v0.14 schema and protocol context: `pydantic_schema_reference.md`, `judgement_case_construction_protocol.md`, `band_input_labeling_rubric.md`, `blind_judgement_schema_and_harness_protocol.md`, `memorization_probe_protocol.md`.

Loaded Unity case material for leakage checks: `cases/unity-runtime-fee/case_index.md`, `cases/unity-runtime-fee/reveal_readout_v0.md`, `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`, `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`, `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`.

Optional/targeted reads available but not consumed because they would not have changed a finding: `proof_and_memory_plan.md`, `phase_1_infrastructure_architecture.md`, Daimler fallback files, `action_band_mapping_table_numbers.md`, `action_band_mapping_executable_spec.md`, `scorer_formula_spec.md`, `failure_event_log_spec.md`, `core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`. The draft pack makes no mapping, scoring, or failure-event claims, so deeper spec verification was not load-bearing for this review.

Hash mismatches: none observed. Prompt-author input_hashes for fixture-pack drafts and discovery pointers were used directly; sources were not modified during review.

## 3. Deep-Thinking And Adversarial-Review Invocation Status

```yaml
workflow_deep_thinking:
  reference_loaded: yes
  applied: yes
  status: applied_inline_against_loaded_source_context
  scope_used: hidden-assumption check, leakage bypass paths, EvidenceUnit field correctness, schema/protocol separation, decision-question framing inheritance, retrieval-metadata hygiene
workflow_adversarial_artifact_review:
  reference_loaded: yes
  applied: yes
  status: applied_after_source_context_ready
  source_root: C:\Users\vmon7\.claude\skills\workflow-adversarial-artifact-review\SKILL.md
  collision_check: single-lane; no adjacent implementation-review or postmortem scope claimed
  output_binding: filesystem-output with required_output_path bound by prompt
```

The skill's correctness-before-friction sequence is honored. Findings carry stable anchors, source evidence, impact, `minimum_closure_condition`, and `next_authorized_action`. `patch_queue_entry` is intentionally omitted per the prompt's explicit instruction "Do not include patch_queue_entry. Patch queues are not authorized."

## 4. Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md`, `.agents/workflow-overlay/README.md` | Orca authority and overlay entrypoint | modified (overlay tree is modified per prompt-author preflight) |
| `.agents/workflow-overlay/source-of-truth.md`, `source-loading.md`, `artifact-roles.md`, `review-lanes.md`, `prompt-orchestration.md`, `communication-style.md`, `validation-gates.md`, `retrieval-metadata.md`, `template-registry.md` | Source hierarchy, source budget, artifact role bindings, adversarial-review lane rules, prompt-orchestration contracts, courier YAML shape, validation gates, retrieval-header contract, template registry | overlay tree modified; used as authority per Orca dirty-state allowance |
| `docs/prompts/reviews/unity_v0_14_draft_fixture_pack_adversarial_review_prompt_v0.md` | Review commission and target binding | untracked per prompt-author preflight |
| `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md` | Commissioning prompt for the fixture-authoring lane | untracked |
| `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md` | Controlling plan that constrained the fixture-authoring lane | untracked |
| Five fixture-pack draft files | Primary review target | untracked |
| `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/judgment-spine/manifest_v0.md` | Discovery pointers (review target) | untracked |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`, `judgement_case_construction_protocol.md`, `band_input_labeling_rubric.md`, `blind_judgement_schema_and_harness_protocol.md`, `memorization_probe_protocol.md` | v0.14 schema/protocol surfaces that the draft maps toward; field-correctness and leakage discipline | imported v0.14 specs; not modified by this review |
| `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md` | Case-folder residue status, spoiler state, missing-artifact list | tracked or untracked depending on prior commit state; treated as orientation only |
| `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`, `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`, `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | Facilitator-only and parent-only material used to check participant-packet leakage | not part of reviewed target; reviewer accessed for leakage discipline only |
| `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | Packet-safe pre-cutoff source ledger and Phase 0 case frame; verifies participant-packet field provenance and source-manifest completeness | used to confirm pre-decision basis claims |

Dirty/untracked caveats:

- Reviewed targets are untracked. Per Orca prompt-orchestration `Control-plane source-state gate` and the prompt's stated dirty-state allowance, untracked review targets may support advisory findings; they do not support strict acceptance, validation, readiness, source-of-truth promotion, or implementation authorization. This review emits findings only.
- Orca overlay sources are modified. The overlay is treated as authority because the prompt explicitly carries the dirty-state allowance. No strict overlay-policy claim is asserted that depends on a frozen overlay revision.

## 5. Findings

Use `critical`, `major`, and `minor` as finding-priority labels per Orca review-lanes.md. They do not by themselves create approval, rejection, readiness, validation, or mandatory-remediation authority. No `patch_queue_entry` is emitted in any finding; patch queues are not authorized for this lane.

### AR-01 (major, correctness): Participant-packet "Permitted Assumptions" #1 echoes a facilitator must-address conclusion

- location: `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md`, "Permitted Assumptions" section, bullet 1 ("Financial pressure can justify exploring monetization changes, but it does not by itself establish broad launch authority.").
- source authority: `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md` (`participant_packet_must_not_include: must_address_items`); `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md` MA-01 ("Commercial pressure supports monetization exploration but does not by itself authorize broad runtime/install-based launch.").
- artifact evidence: the permitted-assumption sentence and MA-01 carry the same shape — financial/commercial pressure does not by itself authorize broad launch. The framing crosses from "what evidence is permitted" to "what conclusion the contestant is steered toward".
- issue: the participant packet's permitted-assumption text leaks the substance of MA-01 into participant-facing material. Even though derivable from source-packet EU-02 limits, the packet is asserting the would-not-authorize conclusion rather than letting the contestant arrive at it.
- impact: a contestant reading the packet is partially pre-framed against a broad action ceiling before independently weighing the evidence. For a fixture intended to expose contestant judgment quality, soft-leaking the facilitator's must-address shape weakens the test. This concern is amplified because the case shape is candidate `ceiling_trap`, where the test is whether the contestant correctly caps action level despite visible pressure — a packet that pre-cues the ceiling reduces the discrimination value.
- minimum_closure_condition: the participant packet's permitted-assumptions either (a) state neutral reasoning permissions (e.g., "financial pressure may be considered when assessing monetization options") without the would-not-authorize conclusion, or (b) the receipt explicitly records the trade-off and flags it as an inherited soft-leakage concern that future clean-packet authoring must resolve.
- next_authorized_action: owner-authorized patching of the participant packet draft's "Permitted Assumptions" section, or owner-authored receipt addendum acknowledging the soft leakage and routing it to a later clean-packet authoring lane.
- recommended advisory remediation direction: replace conclusion-shape statements in permitted_assumptions with permission-shape statements; keep evidence interpretation limits in the per-evidence-unit "Limits" lines (where they already appear) rather than in the global permitted-assumptions list.
- not proven: this finding does not assert the packet is uncontested, score-ready, or unfit for use; it identifies a soft must-address leak that a later authoring lane should resolve.
- patch_queue_entry: not authorized for this lane.

### AR-02 (major, correctness): EU-08 adapter status is UNRESOLVED in the registry but the participant packet has implicitly committed to one branch

- location: `evidence_registry_draft_v0.md` EU-08 (`pre_decision_status: excluded`, `adapter_decision_status: UNRESOLVED`, `draft_registry_treatment: Provisional excluded EvidenceUnit candidate or facilitator-only source-gap note. Operator must decide before registry freeze.`); `participant_packet_draft_v0.md` "Evidence Summaries" section "EU-08 - Unity Pricing And Terms Visibility Gap" (presented as a labeled evidence summary visible to the contestant).
- source authority: extraction plan section "Evidence Registry Conversion Plan", EU-08 row ("Adapter decision required: either EvidenceUnit documenting bounded source-visibility failure or facilitator-only evidence-gap note"); commissioning prompt requirement #6 ("Handle EU-08 as an adapter/source-visibility gap rather than turning a negative lookup into proof").
- artifact evidence: the registry explicitly defers between two adapter routes (EvidenceUnit with `excluded` status vs facilitator-only source-gap note); the participant packet has chosen the former route by presenting EU-08 as a numbered evidence summary, but the receipt's Hard Blockers still lists "EU-08 adapter decision: unresolved".
- issue: the docs-only draft has implicitly selected one adapter outcome (excluded EvidenceUnit shown to participant) while the registry still describes the choice as unresolved. If the operator later selects the facilitator-only source-gap note route, EU-08 would need to be removed from participant view entirely — yet the packet is already presenting it. The pack therefore quietly prejudges an operator decision that the receipt advertises as a hard blocker.
- impact: downstream readers (later implementation scoping, patch lane, or clean-packet authoring lane) cannot tell whether the participant packet's EU-08 framing is provisional pending adapter decision or is the intended steady state. The two adapter outcomes have materially different consequences for what the contestant sees and how `evidence_id_check_result` would interact with EU-08 in any future scoring step.
- minimum_closure_condition: either (a) the receipt explicitly records that the draft participant packet provisionally selects the excluded-EvidenceUnit-shown-as-visibility-gap route pending operator confirmation, and the registry's `adapter_decision_status` carries the same provisional-choice note; or (b) EU-08 is moved from the participant packet's numbered Evidence Summaries into "Known Uncertainties And Source Gaps" until the adapter decision is made, removing the implicit commitment.
- next_authorized_action: owner-authorized patch to either the receipt (option a) or the participant packet plus registry (option b).
- recommended advisory remediation direction: option (a) is cheaper and preserves the current packet shape; option (b) is cleaner because it doesn't prejudge the adapter decision. Either resolves the inconsistency.
- not proven: this finding does not assert the participant packet's current EU-08 treatment is wrong — only that the implicit selection has not been declared.
- patch_queue_entry: not authorized for this lane.

### AR-03 (minor, correctness): Participant-packet source manifest omits S-01 (the SEC filing-locator establishing pre-decision visibility for EU-01 through EU-06)

- location: `participant_packet_draft_v0.md` YAML frontmatter `source_manifest` (lists S-03, S-04, S-05, S-06, S-07).
- source authority: `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` Source Ledger, S-01 ("SEC accession page for 2022 Form 10-K filed before cutoff", role "first-order filing locator", "Index proves filing visibility, not substantive facts by itself"); `evidence_registry_draft_v0.md` EU-01 through EU-06 use `pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet`.
- artifact evidence: six of the eight evidence units rely on the claim that S-03 was visible before cutoff. The source packet establishes that visibility through S-01 (the SEC accession index) and the S-03 filing-body row's basis line. The participant packet asserts pre-decision visibility but its `source_manifest` lacks the locator that proves it independently of facilitator narrative.
- issue: the pre-decision-visibility claim for EU-01 through EU-06 is missing one of the two source-packet sources that supports it. A contestant inspecting the source manifest can verify S-03 itself, but the manifest does not carry the filing-index locator that the source packet used to anchor pre-decision visibility.
- impact: minor — the EvidenceUnit registry still carries `pre_decision_basis` text. But for fixture-admission discipline (per v0.14 `EvidenceUnit` field contract where `hash` should be `sha256(source_bytes)` when bytes are available and the pre-decision basis should be normalized), the participant manifest is a layer thinner than the source packet's own provenance.
- minimum_closure_condition: either (a) S-01 (the SEC accession page) is added to the participant `source_manifest` as the filing-locator establishing pre-decision visibility, or (b) the pre-decision basis is reworked to anchor visibility on S-03's filing body alone with explicit acknowledgement that S-01 was the cross-check source in the source packet but is not separately included.
- next_authorized_action: owner-authorized patch to source manifest or evidence registry basis text.
- recommended advisory remediation direction: (a) is the smaller intervention and keeps the manifest auditable end-to-end; (b) is acceptable if the operator wants to minimize manifest line count.
- not proven: this finding does not contest the pre-decision visibility of S-03 itself; it only flags the missing locator in the participant manifest.
- patch_queue_entry: not authorized for this lane.

### AR-04 (minor, friction): Inherited Phase 0 decision question pre-suggests case-specific option families

- location: `participant_packet_draft_v0.md` frontmatter `decision_question` ("Should Unity proceed with a broad runtime/install-based fee model, narrow or phase the change, grandfather existing users, change messaging, or hold pending further evidence?") and "Decision Frame" body.
- source authority: `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` Phase 0 case frame (same decision question, authored at Phase 0); `judgement_case_construction_protocol.md` participant_packet contract (decision_question is a required field but no enum or shape constraint forbids option-laden phrasing).
- artifact evidence: the decision question lists five concrete case-specific option families (broad model, narrow/phase, grandfather, messaging, hold). These overlap directly with the sealed memo's options table (hold, narrow segment, phase, grandfather, exempt, messaging, hold pending) and with v0.14 candidate decision_shape `ceiling_trap`.
- issue: the inherited Phase 0 question pre-cues the case-specific option vocabulary. The fixture-authoring lane correctly used the controlling question verbatim, so this is not a fixture-authoring defect — it is an inherited Phase 0 framing concern that propagates into the v0.14 packet shape. A clean v0.14 participant packet would typically state the decision question in domain-neutral terms and let the contestant propose action paths from the generic ladder.
- impact: contestant reasoning is partially anchored to Phase 0 option vocabulary, weakening the blind-judgment discrimination of a `ceiling_trap`-shaped case. Friction, not correctness — the existing artifacts honestly inherit the Phase 0 framing.
- minimum_closure_condition: the receipt or a later clean-packet authoring lane explicitly records the inherited Phase 0 framing as a v0.14 packet-shape consideration (rather than silently propagating it). Either keep the question and flag the framing, or generate a v0.14-clean decision question in a later authoring lane.
- next_authorized_action: owner decision on whether v0.14 packets should keep the Phase 0 option-laden question or restate it more domain-neutrally for blind contestant use. This is outside the fixture-authoring lane's authority; it is a Phase 0 / case-construction call.
- recommended advisory remediation direction: add a brief receipt note acknowledging the inherited Phase 0 framing; do not edit the participant packet draft to depart from the controlling Phase 0 question.
- not proven: this finding does not assert the Phase 0 question is wrong — only that its option-laden shape is worth surfacing.
- patch_queue_entry: not authorized for this lane.

### AR-05 (minor, friction): Fixture-side participant packet artifact is not distinguished from the case-folder participant packet residue

- location: `fixture_authoring_receipt_v0.md` Draft Fixture Pack Inventory and Source-Read Ledger; `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md` "Missing Residue" (lists `cases/unity-runtime-fee/participant_packet_v0.md`, `safety_receipt_v0.md`, `blind_judgments_v0.md` as missing).
- source authority: `manifest_v0.md` Unity Runtime Fee Artifact Status table (separates the case-folder Participant Packet "Missing" entry from the new draft v0.14 fixture pack entry); `case_index.md` (Unity case-folder residue listing).
- artifact evidence: the fixture pack creates a draft participant packet under `harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/` (correctly per the commissioning prompt), but the case-folder participant packet under `cases/unity-runtime-fee/` remains missing. The receipt does not call out this distinction.
- issue: a future agent reading the case index could conflate the v0.14 fixture-side draft participant packet with the case-folder participant packet missing residue and assume the latter is partly addressed. Two different participant-packet semantics exist (one for Judgment Spine blind reuse at the case-folder level, one for v0.14 contestant runs at the harness fixture level), and the receipt does not separate them.
- impact: future-routing confusion; advisory hygiene only. No factual claim leakage.
- minimum_closure_condition: receipt-level note explaining that the fixture-side draft participant packet does not satisfy the case-folder participant packet residue named in `case_index.md`.
- next_authorized_action: owner-authorized receipt addendum.
- recommended advisory remediation direction: a one-line note in the receipt's "Draft Fixture Pack Inventory" or "Source-Read Ledger" that the fixture-side artifact is distinct from the case-folder artifact and does not retire case-folder missing residue.
- not proven: this finding does not assert that the case-folder artifacts must be authored now.
- patch_queue_entry: not authorized for this lane.

### AR-06 (minor, friction): Fixture-pack artifacts lack `input_hashes` for upstream controlling sources

- location: retrieval headers of `fixture_authoring_receipt_v0.md`, `participant_packet_draft_v0.md`, `evidence_registry_draft_v0.md`, `facilitator_ledger_draft_v0.md`, `sealed_memo_adapter_note_v0.md`.
- source authority: `.agents/workflow-overlay/retrieval-metadata.md` "Triggered Fields" section ("input_hashes: use when exact provenance is safety-critical, especially for review reports, rerun prompts, patch prompts, proof/replay artifacts, cutoff-sensitive artifacts, cross-repo inputs, or dirty-state-dependent claims"); commissioning prompt input_hashes block (which records hashes for the extraction plan, source packet, sealed memo, and v0.14 specs).
- artifact evidence: none of the five draft-pack files include `input_hashes` in their retrieval header. The commissioning prompt does carry input_hashes, and the receipt's Source Context Receipt records that overlay/source state was dirty/untracked, but the draft-pack artifacts themselves do not bind upstream provenance via hash.
- issue: the draft pack is cutoff-sensitive (Unity decision cutoff 2023-09-11) and dirty-state-dependent (overlay and Judgment Spine sources untracked per the receipt). Retrieval-metadata.md flags these conditions as exactly the case where `input_hashes` should be used. Without input_hashes on at least the extraction plan and source packet, a later agent re-reading the draft pack cannot quickly confirm whether the upstream sources have shifted.
- impact: minor — the receipt's source-read ledger lists the upstream artifacts and the prompt's input_hashes block covers the prompt-author observation point. But future provenance tracing is weaker than retrieval-metadata.md targets for cutoff-sensitive, dirty-state-dependent artifacts.
- minimum_closure_condition: at minimum, the receipt carries `input_hashes` for the extraction plan and source packet (the two most decision-bearing upstream controlling sources). Optional: the participant packet and evidence registry add input_hashes for the source packet, since their content depends most heavily on it.
- next_authorized_action: owner-authorized receipt header update.
- recommended advisory remediation direction: add input_hashes for the extraction plan and source packet to the fixture authoring receipt's retrieval header; treat the other draft files' input_hashes as optional.
- not proven: this finding does not claim that input_hashes are required for non-cutoff-sensitive drafts in general.
- patch_queue_entry: not authorized for this lane.

## 6. Non-Findings And Residual Risks

The following items were checked and produced no finding. They are recorded so future readers can confirm the review covered them:

- Band-input candidate values in `facilitator_ledger_draft_v0.md` "Frozen Band Inputs - Candidate Review Table" use valid v0.14 Pydantic `BandInputs` enum values across all 14 fields (`evidence_strength=moderate`, `evidence_independence=partially_independent`, `reversibility_feasibility=low`, `reversibility_cost=high`, `authority=partial`, `authority_acquisition_cost=medium`, `capability=partial`, `capability_build_cost=high`, `loss_shape=asymmetric_down`, `opportunity_cost=moderate`, `information_decay=slow`, `option_value=moderate`, `upside_shape=symmetric`, `urgency=low`). Verified against `pydantic_schema_reference.md` `class BandInputs` and the per-field include_if/exclude_if rules in `band_input_labeling_rubric.md`. All values are explicitly labeled `CANDIDATE_UNFROZEN`.
- `UnderreachObservability` Pydantic `basis` enum constraint (`opportunity_cost | window_closure | information_decay | other`) is correctly named in the facilitator ledger draft notes; the draft acknowledges the `judgement_case_construction_protocol.md` mention of `option_value_loss` and correctly routes it through `notes` or maps to `other`. Underreach default is `present: false`, with explicit note that the source-backed basis for primary underreach is missing.
- Direct Pydantic `FacilitatorLedger` fields are correctly separated from protocol fixture metadata. `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk` are recorded under a separate "Protocol Fixture Metadata" section with explicit status labels (`CANDIDATE_PROTOCOL_METADATA`, `CANDIDATE_PROTOCOL_OR_BLIND_JUDGEMENT_METADATA_NOT_FROZEN`, `PROTOCOL_LEAKAGE_INPUT_NOT_DIRECT_PYDANTIC_FIELD`). Matches the patch receipt EUP-01 / EUP-02 / EUP-04 distinctions from the controlling extraction plan.
- The sealed memo adapter note's "Required Adapter Gaps" table covers all the v0.14 areas named in the extraction plan: `decision_shape`, `judgement_class`, run metadata fields (`contestant_id`, `run_id`, `model_id`, `model_family`, `model_snapshot_if_available`, `temperature`, `seed_if_supported`, `harness_version`, `created_at`), prompt hash, participant packet hash, facilitator ledger hash, evidence IDs, must-address coverage, recommended action ladder mapping, and author-context contamination. The non-comparability warning is explicit and the `current_handling: retain_as_parent_judgment_spine_calibration_material` plus `exclude_from_v0_14_scoring_now: yes` posture matches the extraction plan recommendation.
- Participant-packet leakage cross-check against `outcome_calibration_v0.md` and `reveal_readout_v0.md`: the participant packet contains no September 12, 2023 announcement language, no backlash/clarification/apology/revision/cancellation facts, no owner blind-read decision, no sealed-memo action ceiling, no outcome calibration verdict, no reveal readout tactical reads (mechanism psychology, switching-cost segmentation, alternative monetization framings), no derived floor/ceiling, no must-address item labels, no probe status, no fame-risk classification. The framing in the "Decision Frame" section uses neutral language about visible business pressure, customer/ecosystem risk, missing segment economics, and operational uncertainty — all derivable from the source packet's Evidence Gaps section.
- Source packet hash separation: `evidence_registry_draft_v0.md` Registry-Level Missing Fields explicitly states "Source packet hash `FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24` is packet provenance only, not a substitute for per-source source-byte hashes." Matches the extraction plan's evidence-registry conversion rule.
- The receipt avoids implying participant packet hash, ledger freeze hash, prompt hash, packet hash, blind judgement instance, action band derivation, scoring result, failure event, or case report exists. `ledger_freeze_hash: NOT_COMPUTED`, `participant-packet hash: not computed`, `second-label audit: NOT_PERFORMED`, `action band derivation: not performed`, `BlindJudgement schema instance: not created`. All consistent.
- Strict-claim avoidance: the receipt's "Not-Proven Boundaries" section enumerates 17 not-proven claims covering Judgment Spine validation, v0.14 harness validation, case admission, participant-packet cleanliness for blind use, memorization-probe pass, scoring readiness, implementation readiness, source-of-truth promotion, acceptance/approval, buyer validation, product readiness, feature readiness, commercial readiness, model-training readiness, harness superiority, memory compounding, and lesson transfer/promotion. Comprehensive.
- Discovery pointer narrowness: `index.md` adds one row to the "Bridge Foundation" table for the receipt path with non-authorizing status text. `manifest_v0.md` adds one row to "Judgment Harness Spec Inventory" and updates the Unity Runtime Fee Artifact Status table's draft fixture pack row, both with non-authorizing text. Neither pointer changes existing roles, freshness markers, or authority bindings.
- No probes/, runs/, scores/, src/, app/, packages/, tests/, runners/, configs/, automation, or runtime files were created. The fixture-pack root contains only the five required docs-only artifacts.
- Retrieval headers on all five fixture-pack artifacts and both discovery pointers use `retrieval_header_version: 1`, set `authority_boundary: retrieval_only`, and avoid forbidden header fields (no approval, validation, readiness, lifecycle, deployment, install, resolver, edit-permission, executor-authorization, review-verdict, or source-of-truth-promotion language in the headers themselves).
- The participant packet's YAML frontmatter precedes the body's retrieval header per the commissioning prompt's rule ("If exact schema frontmatter conflicts with Orca retrieval metadata, preserve the v0.14 frontmatter first and put any Orca retrieval note below it"). Correct ordering.
- The frozen `case_id: unity_runtime_fee_2023_v0_14` matches the extraction plan's fallback convention (lowercase, filesystem-safe, digits/underscores only, no status words). The receipt's `case_id_status: frozen_for_this_docs_only_draft_pack` non-claim correctly bounds the freeze.

Residual risks:

- The facilitator ledger draft is intentionally not Pydantic-loadable (`frozen_band_inputs: NOT_FROZEN`, `committed_at: NOT_COMMITTED`, etc.). A reader who attempts to YAML-load it into the `FacilitatorLedger` model would receive type errors before reaching the documentary not-frozen markers. This is consistent with the draft's stated docs-only-not-frozen status; no change required unless future use cases assume partial loadability.
- EU-04 source packet basis says "high-value customers as contributing a substantial majority of revenue." The participant packet retains this phrasing. The Unity 2022 Form 10-K filing language uses "substantial majority" terminology, so this is consistent with the source-packet description, but the precise phrasing is a paraphrase. Future operator review may want to confirm the filing-body excerpt versus the paraphrase before binding the EvidenceUnit hash.
- The fixture pack does not author probe artifacts, run-config templates, or blind-judgment instances. All are correctly out of scope per the commissioning prompt. A later implementation-scoping lane will need to bind these surfaces.

## 7. Strict-Only Blockers And Not-Proven Boundaries

Strict-only blockers (carried by the reviewed pack, not introduced by this review):

- Per-source source-byte hashes for S-03 through S-07 are not computed.
- Per-source retrieval timestamps are not normalized.
- EU-08 adapter decision is unresolved (compounded by AR-02).
- Facilitator ledger freeze hash is `NOT_COMPUTED`; ledger is not frozen.
- Frozen band inputs are `NOT_FROZEN`; all values remain candidate.
- Second-label audit is `NOT_PERFORMED`.
- Must-address items are `CANDIDATE_ONLY`.
- `decision_shape` is candidate (`ceiling_trap`) and not frozen for a `BlindJudgement` run.
- Memorization probe is not run for any model family; Unity probe-safety is not proven.
- Sealed memo adapter is unresolved; legacy memo is not directly comparable to fresh contestant outputs.
- No `BlindJudgement` instance, `ActionBandResult`, `ScoringResult`, `FailureEvent`, or `CaseReport` exists.

Not-proven boundaries (this review does not assert any of these):

- The reviewed pack is not authorized for fixture admission, probe pass, score-readiness, implementation authorization, source-of-truth promotion, deployment, install, resolver behavior, plugin readiness, validation pass, acceptance, approval, mandatory remediation, lifecycle completion, product proof, buyer validation, harness superiority, lesson transfer, lesson promotion, or memory compounding.
- This review does not validate the Judgment Spine, the v0.14 harness, the v0.14 schemas, the v0.14 mapping table, the scoring formulas, the memorization-probe protocol, the failure-event-log protocol, the proof and memory plan, the Unity case admission, or the controlling extraction plan.
- This review does not promote the participant packet draft as packet-safe-for-blind-use; it only checks that the draft's participant-facing content does not currently expose forbidden material from the sealed memo, outcome calibration, or reveal readout (subject to AR-01 soft leakage).
- This review does not recommend, prescribe, rank, or imply a model for any review lane, contestant run, scoring lane, probe lane, or implementation lane.

## 8. Review-Use Boundary

Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, fixture admission, probe pass, score-readiness, implementation authorization, lesson promotion, deployment, install, resolver behavior, plugin readiness, harness superiority, executor-ready instructions, or patch authority. A separate authorized Orca decision, patch lane, validation lane, or implementation lane must accept any finding before remediation is mandatory or before any downstream action is taken on the basis of these findings. Severity labels `critical`, `major`, and `minor` are finding-priority labels per Orca review-lanes.md; they do not create approval, rejection, readiness, validation, or mandatory-remediation authority by themselves.

## 9. Next Authorized Step

Owner-authorized next step is one of:

- accept the draft pack as is, treating AR-01 through AR-06 as residual considerations to track but not patch, and proceed to a later owner-authorized implementation-scoping or clean-packet authoring lane that resolves them in context;
- owner-authorized patching of one or more findings (AR-01 permitted-assumptions rephrasing, AR-02 EU-08 adapter disclosure, AR-03 source-manifest S-01 addition, AR-05 receipt addendum on fixture-side vs case-folder distinction, AR-06 input_hashes for upstream controlling sources). Patching requires a separate patch-execution lane and is not authorized by this review;
- defer Unity v0.14 fixture work and switch to the Daimler fallback route per the extraction plan's Daimler Fallback Decision Gate, if probe-safety, leakage handling, or sealed-memo non-comparability concerns drive that choice.

This review does not select among these. The owner decides which path to take. None of the three paths authorize implementation, runtime, probe execution, model runs, scoring, validation, proof, product-proof, or lesson-promotion work.
