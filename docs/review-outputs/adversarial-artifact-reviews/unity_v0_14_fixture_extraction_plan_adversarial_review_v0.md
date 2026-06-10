# Unity v0.14 Fixture Extraction Plan Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the Unity Runtime Fee v0.14 fixture extraction plan and bounded discovery pointers.
use_when:
  - Consuming this review before a Unity fixture-authoring lane, implementation-scoping prompt, or probe execution.
  - Checking whether prior bridge-review findings (AR-01 through AR-06) were addressed.
  - Deciding whether the extraction plan is ready to hand to a fixture-authoring lane.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/prompts/reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_prompt_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: F0DA91385F918F855F7DB6BA84AAA3C020AA4F711BD75450D681F829EC016D0F
  docs/research/judgment-spine/harness/v0_14/index.md: 4DB97DB3D561368CF5E780E4CF3F8A6E9053F591C23BDA918302CD2A996C6351
  docs/research/judgment-spine/manifest_v0.md: 4228C88FC32A33F2E1C5123997DB3A301E4A7000D82043CAB1BB3ADBB796766E
  docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md: 05140F3FDBF89BD97377610CA8C9A6CDD15D602BFAB41B2CA19C40181D8C37F9
```

- Status: REVIEW_COMPLETE
- Artifact type: Adversarial artifact review report
- Commissioned by prompt: `docs/prompts/reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_prompt_v0.md`
- Output mode used: review-report (file-write)
- Reviewer edit permission: read-only; this report written to `docs/review-outputs/adversarial-artifact-reviews/`
- Patch queue authorized: no
- Implementation, validation, probe execution, scoring, commit, push, or product-proof authorized: no

---

## 1. Review Target and Purpose

Primary target:

- `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`

Bounded discovery-pointer targets:

- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/manifest_v0.md`

Commissioning prompt source:

- `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md`

Prior adversarial review consulted:

- `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md`

Review purpose: Adversarially review whether the Unity extraction plan satisfies the commissioning prompt's goal, remains a docs-only plan without becoming a fixture artifact, correctly classifies Unity material across participant/facilitator/parent/excluded surfaces, correctly maps v0.14 schema fields in the EvidenceUnit conversion plan and FacilitatorLedger work queue, makes the memorization-probe gate hard enough, handles sealed-memo contamination, defines adequate Daimler fallback criteria, avoids strict-claim leakage, remediates prior AR-01 through AR-06 bridge-review findings, and keeps the discovery pointers narrow and non-authorizing.

---

## 2. Source Context Status

```yaml
source_context_status: SOURCE_CONTEXT_READY
source_gap_caveat: judgement_case_construction_protocol.md was not read by this reviewer.
  Findings EUP-01 and EUP-02 concern schema fields that may be defined or extended there.
  Those findings are advisory-confidence level, not definitive. A fixture-authoring lane
  must read both pydantic_schema_reference.md AND judgement_case_construction_protocol.md
  before authoring ledger fields.
```

**Hash verification:** All four prompt-author observed SHA256 hashes match current files exactly (case-insensitive).

| File | Observed hash | Verified |
| --- | --- | --- |
| `unity_v0_14_fixture_extraction_plan_v0.md` | F0DA91...016D0F | MATCH |
| `index.md` | 4DB97D...C6351 | MATCH |
| `manifest_v0.md` | 4228C8...6766E | MATCH |
| commissioning CA prompt | 05140F...C37F9 | MATCH |

**Git state:** HEAD b7627d3. Overlay control files modified; reviewed targets untracked. Dirty-state allowance applied per prompt. All reviewed files are working artifacts. Strict acceptance, validation, readiness, source-of-truth promotion, and proof claims remain not proven.

**Goal fit pre-check:** The extraction plan fits the anchor goal (define a case-to-v0.14 bridge CA lane mapping existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation), the success signal (minimum Unity harness-entry shape defined, controlling v0.14 spec files named, missing/unsafe/contaminated inputs exposed, smallest later implementation scope named non-executably), and the selected-next-move output-fit-check (participant-packet extraction boundaries, EvidenceUnit conversion, facilitator-ledger work queue, leakage-audit fields, required `decision_shape`, sealed-memo contamination handling, parent-only exclusions, hard memorization-probe gate, and Daimler fallback trigger without authorizing code). No `BLOCKED_GOAL_CONFLICT`.

---

## 3. Deep-Thinking and Adversarial-Review Invocation Status

- `workflow-deep-thinking`: REFERENCE-LOAD completed before source analysis; APPLIED after SOURCE_CONTEXT_READY. Used to frame the plan-versus-fixture boundary problem, failure modes (over-specification, field invention, probe bypass, strict-claim leakage, schema attribution errors, sealed-memo contamination implicit endorsement, and Daimler scope creep) and decision criteria before producing findings.
- `workflow-adversarial-artifact-review`: REFERENCE-LOAD completed before source analysis; APPLIED after SOURCE_CONTEXT_READY. Findings produced under adversarial artifact review flow.

Both skills available and applied. No blocked or advisory-only fallback required.

---

## 4. Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` | Workspace operating constraints and Orca authority boundary | Untracked |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | Modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | Modified |
| `.agents/workflow-overlay/source-loading.md` | Source-loading budgets, dirty-state caveats, source-heavy economy | Modified |
| `.agents/workflow-overlay/artifact-roles.md` | Artifact roles, permissions, review report destination | Modified |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules, reviewer write permission, adversarial artifact review doctrine | Modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | Output mode, source-gated method sequencing, review-report rules | Modified |
| `.agents/workflow-overlay/communication-style.md` | Review closeout shape, adversarial review summary YAML shape | Modified |
| `.agents/workflow-overlay/validation-gates.md` | Completion and strict-claim gates | Modified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract | Modified (read from disk pre-modification state) |
| `.agents/workflow-overlay/template-registry.md` | Template registry confirmation, adversarial-artifact-review template binding | Untracked |
| `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_extraction_plan_ca_prompt_v0.md` | **Commissioning prompt**: consumed goal, authority, extraction questions, required output shape | Untracked |
| `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md` | **Primary review target** | Untracked |
| `docs/research/judgment-spine/harness/v0_14/index.md` | Discovery-pointer target: navigation index for v0.14 spec | Untracked |
| `docs/research/judgment-spine/manifest_v0.md` | Discovery-pointer target: Judgment Spine case and harness inventory | Untracked |
| `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md` | Controlling bridge recommendation; prior finding baseline | Untracked |
| `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md` | Prior review findings AR-01 through AR-06 to check remediation | Untracked |
| `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md` | Unity artifact status, spoiler state, missing residue | Untracked |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` | v0.14 schema contracts: EvidenceUnit, FacilitatorLedger, BlindJudgement, BandInputs, ScoringResult, FailureEvent — authoritative for schema field verification | Untracked |
| `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md` | Band-input labeling workflow, required ledger fields, disagreement quarantine rules | Untracked |
| `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md` | Contestant output contract, run metadata, decision_shape enum, repeatability policy | Untracked |
| `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md` | Probe inputs, evaluation rule, pass/fail/ambiguous case handling, blocking severity | Untracked |

**Sources available, not read by reviewer:** Unity source packet, sealed memo, outcome calibration, reveal readout, judgement_case_construction_protocol.md, judgement_spine_thesis.md, judgement_harness_strategy.md, action_band_mapping_table_numbers.md, action_band_mapping_executable_spec.md, scorer_formula_spec.md, failure_event_log_spec.md, proof_and_memory_plan.md, Daimler fallback files, orca_repo_map_v0.md. None of these would change the primary findings except judgement_case_construction_protocol.md, which could affect EUP-01 and EUP-02 schema field attribution findings.

**Dirty-source confidence impact:** All reviewed targets are untracked; overlay control files are modified. Advisory findings use repo-visible evidence. Strict acceptance, readiness, validation, source-of-truth promotion, and proof claims remain not proven.

---

## 5. Findings-First Review Output

### CORRECTNESS FINDINGS

---

**EUP-01**

- **Finding ID:** EUP-01
- **Priority:** major
- **Phase:** correctness
- **Location:** Extraction plan, "Facilitator-Ledger Work Queue," sub-section "Required Identity And Version Fields"; sub-section "Required Decision Shape"
- **Issue:** Two fields — `case_family` and `decision_shape` — are listed as required identity and version fields for the facilitator ledger. Neither appears in the `FacilitatorLedger` schema in `pydantic_schema_reference.md`. Specifically: `decision_shape` is a required field in `BlindJudgement`, not in `FacilitatorLedger`. `case_family` does not appear in any v0.14 schema file read by this reviewer.
- **Evidence:** `pydantic_schema_reference.md` §FacilitatorLedger: fields are `case_id`, `batch_id`, `labeling_rubric_version`, `mapping_table_version_pin`, `ledger_authors`, `second_label_diffs`, `frozen_band_inputs`, `must_address_items`, `underreach_observability`, `leakage_audit_notes`, `spoiler_inventory`, `committed_at`, `ledger_freeze_hash` — `case_family` and `decision_shape` are absent. `pydantic_schema_reference.md` §BlindJudgement: `decision_shape: str` is a required field in the contestant output, not the facilitator ledger. `band_input_labeling_rubric.md` §Required Ledger Fields: `case_family` and `decision_shape` are absent.
- **Source gap caveat:** `judgement_case_construction_protocol.md` was not read. That spec might define additional ledger fields or a structured `decision_shape` expectation at the case level. This finding is advisory-confidence. However, `decision_shape` being in BlindJudgement and not FacilitatorLedger is visible across two spec files.
- **Requirement strained:** Commissioning prompt extraction question #4 asks for "facilitator-ledger fields that must be operator-authored later." The answer should map to v0.14 schema fields. CA commissioning prompt and bridge foundation both identify `pydantic_schema_reference.md` as the controlling schema source.
- **Impact:** A future fixture-authoring lane reading "Required Identity And Version Fields" for the facilitator ledger may write `case_family` and `decision_shape` as named YAML fields inside `FacilitatorLedger`, which would create extra-schema fields not in the pydantic model. It may also not realize that `decision_shape` must be in the BlindJudgement (contestant output), not the ledger — causing a schema-invalid BlindJudgement or an incorrect mental model about who owns `decision_shape`. The "Required Decision Shape" sub-section correctly discusses `decision_shape` in terms of the v0.14 allowed enum values, but placing this sub-section inside the facilitator-ledger work queue reinforces the incorrect attribution.
- **Minimum closure condition:** The "Required Identity And Version Fields" list is reconciled against `pydantic_schema_reference.md` §FacilitatorLedger. `decision_shape` is either removed from the ledger identity fields with a note that it belongs in BlindJudgement, or it is explicitly labeled "BlindJudgement field — the operator must freeze this value before adapting the sealed memo, but it goes in the BlindJudgement output, not the FacilitatorLedger." `case_family` is either confirmed against `judgement_case_construction_protocol.md` as a valid ledger field, or removed/labeled as "case-index metadata, not a FacilitatorLedger schema field."
- **Next authorized action:** Owner decision on whether to patch this section before the extraction plan is handed to a fixture-authoring lane, or to accept a reader warning in the fixture-authoring prompt.
- **Patch queue authorized:** No.
- **Verification gate for future executor:** The fixture-authoring lane can confirm this by reading `judgement_case_construction_protocol.md` §Facilitator Ledger Required Fields side-by-side with `pydantic_schema_reference.md` §FacilitatorLedger before writing any ledger artifact.

---

**EUP-02**

- **Finding ID:** EUP-02
- **Priority:** minor
- **Phase:** correctness
- **Location:** Extraction plan, "Leakage-Audit Field Mapping" section, fields `memorization_probe_required` and `known_fame_risk`; "Facilitator-Ledger Work Queue," sub-section "Leakage Audit, Freeze, And Commit"
- **Issue:** The extraction plan maps `memorization_probe_required` and `known_fame_risk` as discrete named fields in the facilitator ledger leakage-audit block. The `pydantic_schema_reference.md` §FacilitatorLedger shows only two leakage-related fields: `leakage_audit_notes: Optional[str]` (free-text) and `spoiler_inventory: Optional[str]` (advisory free-text). Neither `memorization_probe_required` nor `known_fame_risk` appears as a named field in the pydantic schema. The bridge foundation review (AR-02) cited `judgement_case_construction_protocol.md`'s `leakage_audit` block as containing these as sub-fields. That spec file was not read by this reviewer, so this is advisory-confidence.
- **Evidence:** `pydantic_schema_reference.md` §FacilitatorLedger: `leakage_audit_notes: Optional[str]` and `spoiler_inventory: Optional[str]` only. `band_input_labeling_rubric.md` §Required Ledger Fields: same two fields only. Bridge foundation review AR-02: "In v0.14 this maps into the facilitator ledger's leakage audit fields, including `leakage_audit_notes`, `spoiler_inventory`, `memorization_probe_required`, and `known_fame_risk`" — but without specifying whether these are free-text sub-keys or structured sub-fields.
- **Requirement strained:** A fixture-authoring lane using the pydantic schema as the implementation contract cannot write `memorization_probe_required: true` as a named YAML field in FacilitatorLedger. It would need to embed these as text inside `leakage_audit_notes`, or the case construction protocol defines them as structured sub-fields.
- **Impact:** Schema divergence between the pydantic implementation schema and the case-construction-protocol conceptual schema. A fixture-authoring lane may produce a FacilitatorLedger that contains extra-schema fields, causing pydantic validation errors. Or it may embed the information in free-text `leakage_audit_notes`, losing the discrete field distinction. The extraction plan inherits this ambiguity from the bridge foundation; it does not introduce a new error.
- **Minimum closure condition:** The extraction plan's leakage-audit field mapping note explicitly states how `memorization_probe_required` and `known_fame_risk` should be represented in the pydantic-ready FacilitatorLedger — as free-text within `leakage_audit_notes`, as structured sub-fields if the case construction protocol defines them, or as advisory text only. The fixture-authoring lane prompt must reference both `pydantic_schema_reference.md` and `judgement_case_construction_protocol.md` before resolving this.
- **Next authorized action:** Owner decision on whether to read `judgement_case_construction_protocol.md` and patch the leakage-audit field guidance, or add a note to the fixture-authoring prompt flagging this as a schema resolution requirement.
- **Patch queue authorized:** No.

---

**EUP-03**

- **Finding ID:** EUP-03
- **Priority:** minor
- **Phase:** correctness
- **Location:** Extraction plan, "Sealed Unity Memo Treatment" section, conversion gap table
- **Issue:** The sealed memo gap analysis lists eight required-area gaps (decision_shape, contestant/run metadata, prompt_hash, packet and ledger hashes, recommended action, evidence_used, must-address coverage, advisory fields, author-context contamination) but omits `judgement_class`. The `BlindJudgement` schema requires `judgement_class` as a required field with five allowed values: `recommend`, `abstain`, `wait`, `escalate`, `irreducible_uncertainty`. The sealed at-cutoff Unity memo has an action recommendation but it is not expressed using this enum. Mapping the memo action ceiling to one of these five classes is a non-trivial adapter step — "recommend" is the most likely, but "wait" or "escalate" are plausible for certain readings.
- **Evidence:** `pydantic_schema_reference.md` §BlindJudgement: `judgement_class: Literal["recommend", "abstain", "wait", "escalate", "irreducible_uncertainty"]` — required field. `blind_judgement_schema_and_harness_protocol.md` §Blind Judgement Output: `judgement_class` listed as required with the same five values. Extraction plan §Sealed Unity Memo Treatment gap table: `judgement_class` not mentioned.
- **Impact:** A fixture-authoring lane following the memo treatment plan will produce a memo adapter without flagging that `judgement_class` must be explicitly chosen. The `judgement_class`-to-ladder mapping is schema-validated (invalid combinations create a `schema_invalid` failure event), so this omission is recoverable at schema-validation time — but it is better to flag it in the plan than leave it as a surprise during adapter authoring.
- **Minimum closure condition:** The sealed memo gap table adds a row for `judgement_class` with a note that the memo action ceiling must be mapped to one of the five allowed enum values, and that the choice is load-bearing (it determines valid `ladder_level` ranges via the `judgement_class`-to-ladder mapping in the pydantic schema).
- **Next authorized action:** Owner decision at time of patching or memo-adapter authoring. No urgency that blocks handing the plan to a fixture-authoring lane, but should be noted there.
- **Patch queue authorized:** No.

---

**EUP-04**

- **Finding ID:** EUP-04
- **Priority:** minor
- **Phase:** correctness
- **Location:** Extraction plan, "Facilitator-Ledger Work Queue," sub-section "Underreach Observability"
- **Issue:** The extraction plan says: "A later operator may mark underreach observability true only if the frozen packet and ledger identify observable opportunity cost, window closure, information decay, option-value loss, or another source-backed basis." The phrase "option-value loss" is not an enum value in `UnderreachObservability.basis`. The allowed values are: `opportunity_cost`, `window_closure`, `information_decay`, `other`. "Option-value loss" is a conceptual description that would fall under `other`, not a discrete enum value. A fixture-authoring lane might attempt to write `basis: option-value loss` in the ledger YAML, creating a pydantic validation error.
- **Evidence:** `pydantic_schema_reference.md` §UnderreachObservability: `basis: Optional[Literal["opportunity_cost", "window_closure", "information_decay", "other"]] = None`. Extraction plan §Underreach Observability: "option-value loss" listed as a discrete basis category alongside the actual enum values.
- **Impact:** Low probability of causing a hard failure because the fixture-authoring lane will encounter the enum constraint at schema validation time. But using non-spec language in a planning document creates unnecessary friction. "Option-value loss" is real, but it should be labeled as `other` with notes, not as a separate basis enum.
- **Minimum closure condition:** The underreach observability section replaces "option-value loss" with `other` (consistent with the pydantic enum) and notes that option-value loss falls under `other` with a brief rationale in the `notes` field.
- **Next authorized action:** Owner review. Addressable inline in any extraction plan patch.
- **Patch queue authorized:** No.

---

### FRICTION FINDINGS

---

**EUP-05**

- **Finding ID:** EUP-05
- **Priority:** minor
- **Phase:** friction
- **Location:** Extraction plan, "Participant Packet Extraction Plan," sub-section "Required v0.14 Frontmatter," `case_id` field
- **Issue:** The frontmatter template shows `case_id: unity_runtime_fee_v0_14_candidate`. The plan states: "`case_id` is a planning placeholder. A later fixture lane must freeze the canonical case ID before writing any packet, ledger, probe, run, or score artifact." However, the plan does not specify what format or convention the canonical case ID should follow (e.g., slug convention, batch-scoped ULID, namespace prefix). A fixture-authoring lane working from this template might inadvertently copy the placeholder value or choose an incompatible format, causing an ID mismatch across packet, ledger, probe, and scoring artifacts.
- **Evidence:** Extraction plan §Required v0.14 Frontmatter: `case_id: unity_runtime_fee_v0_14_candidate` with a note that it is a placeholder. `pydantic_schema_reference.md` §FacilitatorLedger, §BlindJudgement, §ScoringResult, §CaseReport, §FailureEvent: all use `case_id: str` without a format constraint. Probe artifact path uses `<case_id>` as a path component, so the format choice has filesystem implications.
- **Impact:** Low-probability hard failure. The canonical ID would likely be frozen at fixture-authoring time regardless. But the placeholder value "unity_runtime_fee_v0_14_candidate" looks like a reasonable value and a fixture lane might freeze it without noticing it was a placeholder. Once frozen, the ID propagates across every downstream artifact. A wrong ID would require touching packet, ledger, probe, run, score, and report artifacts.
- **Minimum closure condition:** The frontmatter template either shows `case_id: <TBD — to be frozen by fixture-authoring lane; see ID convention note>`, or the plan adds a one-sentence note on the expected ID convention (e.g., "slug-style, batch-prefixed, all-lowercase, no spaces").
- **Next authorized action:** Owner review. Low urgency.
- **Patch queue authorized:** No.

---

**EUP-06**

- **Finding ID:** EUP-06
- **Priority:** minor
- **Phase:** friction
- **Location:** Extraction plan, "Consumed Goal Fit Check" section
- **Issue:** The consumed goal fit check states fit across anchor goal, success signal, and output-fit-check in prose, but does not map each success-signal criterion to a specific extraction-plan section. This was identified as AR-04 in the prior bridge foundation review. The extraction plan's fit check is more specific than the bridge foundation's (it names the exact content domains covered), but it still requires a reader to cross-reference the full artifact to verify each criterion.
- **Evidence:** Commissioning CA prompt §Goal To Consume, success_signal: "A CA can determine (a) minimum harness-entry shape, (b) which v0.14 spec files control it, (c) missing or unsafe inputs, (d) smallest later implementation scope without authorizing code." Extraction plan §Consumed Goal Fit Check: three paragraphs asserting fit across (a)-(d) collectively, without pointing to sections.
- **Impact:** Low. Fit is demonstrably satisfied by reading the full artifact. This is a navigability and auditability concern for future CAs consuming the plan. The improvement over the bridge foundation is meaningful (criteria (a)-(d) are all addressed by named sections), but the section-mapping format would eliminate the need to re-read the whole artifact.
- **Minimum closure condition:** The fit-check section cites the specific sections satisfying each success-signal criterion (e.g., "(a) minimum harness-entry shape: see Blocked-Before-Scoring Checklist and Evidence Registry Conversion Plan; (b) controlling v0.14 spec files: see Source-Read Ledger; (c) missing/unsafe inputs: see Missing fields in each section; (d) deferred implementation: see Deferred Implementation Implications").
- **Next authorized action:** Owner review. Lower priority than EUP-01.
- **Patch queue authorized:** No.

---

## 6. Non-Findings and Residual Risks

The following were checked and found satisfactory or adequately bounded. They are not findings.

**Plan-only boundary maintained:** The extraction plan does not create a participant packet, evidence registry, facilitator ledger, blind judgment, memorization probe artifact, scoring result, failure log, or case report. Each major section explicitly labels itself as a planning queue, not the artifact itself. The participant packet section says "This section is not the packet." The evidence registry section says "the source packet... is not yet a v0.14 evidence registry." No actual hashes, evidence IDs, timestamps, band labels, or scores are invented. ✓

**Prior finding AR-01 (probe risk differential) remediated:** The extraction plan explicitly characterizes Unity Runtime Fee as having "elevated known-event and memorization-probe risk for modern frontier models." The memorization-probe gate is a dedicated section with concrete pass/fail/ambiguous routing and a model-family quarantine rule. The Daimler fallback gate explicitly triggers on probe failure for intended model families. This substantially addresses the false equivalence identified in AR-01. ✓

**Prior finding AR-02 (spoiler receipt schema mapping) remediated:** The extraction plan explicitly says "Unity does not need a standalone v0.14 leakage artifact. Leakage and spoiler controls map into the facilitator ledger." The leakage-audit field mapping section maps controls to named facilitator-ledger fields. No standalone v0.14 spoiler/leakage artifact is created or implied. ✓

**Prior finding AR-03 (sealed memo author-context contamination) remediated:** The sealed memo treatment section names "author-context contamination" explicitly: "The memo may reflect author expertise, prompt context, source-selection context, and internal assumptions beyond what a clean participant packet would expose." The plan recommends the adapted memo be labeled as "a legacy sealed memo or baseline-like input in the case report. It should not be compared to fresh model contestants as if all saw the same packet under the same runner contract unless a later lane proves comparability." ✓

**Prior finding AR-05 (decision_shape missing from blind judgment minimum entry) remediated in context:** The extraction plan names `decision_shape` as a gap in the sealed memo treatment section with the allowed candidates (`ceiling_trap`, `action_band`) and the requirement to freeze exactly one value from the v0.14 allowed set. Because the extraction plan is a different artifact type than the bridge foundation (not a "minimum harness-entry shape" table), this treatment is contextually appropriate, even though it introduces the EUP-01 schema attribution question. ✓

**Prior finding AR-06 (source-read ledger positioned at end):** Residual — the extraction plan positions the source-read ledger at the end, same as the bridge foundation. The Source Context Receipt YAML near the top partially compensates. This is not re-raised as a new finding but is noted as a carry-forward residual.

**Participant-facing / facilitator-only / parent-only / excluded classification:** The four-tier material classification is internally consistent and grounded in the v0.14 case construction protocol and bridge foundation. Reveal readout, outcome calibration, owner blind-read, calibration verdict, and reveal lessons are all correctly placed in parent-only or excluded categories. No evidence of leakage of these surfaces into participant-facing candidates. ✓

**EvidenceUnit conversion plan correctness (EUP-01/02 scope only):** The conversion table for EU-01 through EU-08 correctly names the v0.14 EvidenceUnit required fields (`evidence_id`, `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, `pre_decision_status`, `pre_decision_basis`, `summary`) and correctly identifies the missing or adapter-required fields for each source EU. The PreDecisionStatus enum values (`verified_pre_decision`, `uncertain_timestamp`, `excluded`) are accurately referenced. ✓

**Memorization probe gate adequacy:** The probe gate requires the six probe input fields named in the memorization_probe_protocol.md spec (`case_id`, `decision_question`, `public_identifiers_if_any`, `decision_date_or_cutoff`, `probe_model_family`, `probe_model_id`), plus prompt-template version, prompt hash, and raw response hash. The pass/fail/ambiguous routing matches the spec exactly. The model-family quarantine rule is present and correctly scoped (failure invalidates the contestant-case pair for that family, not all families). The plan correctly notes "Passing does not prove no memorization," consistent with the spec's limits. ✓

**Second-label audit quarantine conditions:** The extraction plan includes the four spec-defined quarantine conditions from the band_input_labeling_rubric plus a fifth condition specific to Unity: "disagreement cannot be resolved without importing revealed outcome material." The fifth condition is a conservative addition appropriate for a revealed case. ✓

**Daimler fallback criteria adequacy:** The six fallback-trigger conditions are source-backed and non-circular. The plan correctly notes that Daimler is not in the manifest's current case inventory and lists the Daimler prerequisites that remain unresolved (sealed blind judgment, reveal readout, outcome calibration, evidence-unit registry, facilitator ledger, band inputs, second-label diffs, memorization probe, scoring result, failure events). Daimler fallback is defined as a routing decision, not as an implicit authorization of Daimler case work. ✓

**Strict-claim hygiene:** No validation, readiness, acceptance, source-of-truth promotion, buyer proof, implementation authorization, memorization-probe pass, score-readiness, harness superiority, or product-proof claims found in the extraction plan body. The status line says "FIXTURE_EXTRACTION_PLAN_V0" — a custom status label, not a readiness claim. The non-claims section is comprehensive. ✓

**Retrieval header hygiene:** Artifact_role "Research artifact" matches `docs/research/judgment-spine/harness/v0_14/` folder binding per `artifact-roles.md`. `input_hashes` triggered field is present with bridge-foundation provenance hashes. `stale_if` triggered field is present with appropriate conditions. ✓

**Discovery pointer narrowness:**
- `index.md` Unity extraction plan row: status "Working extraction plan; does not authorize implementation, probe execution, validation, scoring, or proof claims." Narrow and non-authorizing. ✓
- `manifest_v0.md` Judgment Harness Spec Inventory row: status "Working docs-only extraction plan; maps Unity into fixture-admission surfaces and preserves probe, leakage, scoring, implementation, and proof non-claims." Narrow and non-authorizing. ✓
- `manifest_v0.md` Unity Runtime Fee Case Inventory row: correctly shows participant packet and safety receipt as still missing. ✓

**Commissioning prompt required output shape:** All 17 required sections are present: retrieval header, source context receipt, consumed goal fit check, purpose/non-use/non-claims, source-material classification, participant packet extraction plan, evidence registry conversion plan, facilitator-ledger work queue, leakage-audit field mapping, memorization-probe gate, sealed memo treatment, parent-only/facilitator-only exclusion list, Daimler fallback gate, blocked-before-scoring checklist, deferred implementation implications, source-read ledger, next authorized step. ✓

**Failure-log vs. lesson-promotion boundary:** The blocked-before-scoring checklist item 13 requires "Failure-event logging policy remains `not_a_rule: true` and `promotion_allowed: false`." The parent-only material exclusion section correctly places lessons in parent Judgment Spine scope. No lesson-promotion or memory claim detected. ✓

---

## 7. Strict-Only Blockers and Not-Proven Boundaries

These items are not proven by this review or by the extraction plan, and cannot become proven without separate controlling authority:

- **Not proven:** `judgement_case_construction_protocol.md` defines `case_family`, `decision_shape`, `memorization_probe_required`, and `known_fame_risk` as named FacilitatorLedger schema fields. This would affect EUP-01 and EUP-02. Resolution requires reading that spec before fixture-authoring begins.
- **Not proven:** The value `v0_14_mvp` for `mapping_table_version_pin` is the correct string per `action_band_mapping_table_numbers.md`. The extraction plan asserts this value; the reviewer did not read that spec file.
- **Not proven:** The sealed at-cutoff Unity memo contains all fields required to produce a schema-valid v0.14 BlindJudgement (including `judgement_class`, `decision_shape`, `evidence_used` with claim IDs and evidence-unit ID lists, `must_address_items_covered`, `contestant_id`, `run_id`, `model_id`, `model_family`, `temperature`, `seed_if_supported`, `harness_version`, `prompt_hash`). The sealed memo has not been read by this reviewer.
- **Not proven:** Unity memorization probe result for any frontier model family. The extraction plan correctly notes probe risk is elevated for modern frontier models; probe pass is not claimed.
- **Not proven:** Daimler is accepted into the manifest's current case inventory. This requires separate owner decision.
- **Not proven:** Daimler's probe is safe for target model families. Lower fame risk is plausible, not a probe pass.
- **Not proven:** Judgment Spine validation, v0.14 harness validation, case readiness for scoring, source-of-truth promotion, acceptance, implementation authorization, buyer validation, product readiness, feature readiness, commercial readiness, model-training readiness, harness superiority, memory compounding, or lesson promotion for any candidate.
- **Not proven:** Any strict claims that depend on dirty or untracked sources as controlling authority.

---

## 8. Review-Use Boundary

This is a read-only adversarial review. Findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, source-of-truth promotion, fixture admission, probe pass, score-readiness, implementation authorization, lesson promotion, or executor-ready instructions unless a separate authorized Orca decision, patch, validation, or implementation lane accepts them.

`critical`, `major`, and `minor` labels are finding-priority labels per the commissioning prompt and Orca review-lanes overlay. They do not constitute formal approval, rejection, readiness, validation, or mandatory remediation authority by themselves.

EUP-01 is major because a schema misattribution in a planning document propagates into fixture artifacts. EUP-02 through EUP-06 are minor. None of the findings compromise the plan's validity as a docs-only extraction plan and advisory fixture-admission work queue. The plan is usable in its current state for owner review and qualified hand-off to a fixture-authoring lane.

---

## 9. Next Authorized Step

**Recommendation:** `accept_with_friction`

**Summary:** The Unity v0.14 fixture extraction plan satisfies its anchor goal and success signal, correctly maintains the plan-only boundary, remediates AR-01 through AR-05 from the prior bridge review (AR-06 residual), correctly classifies Unity source material across four tiers, produces a complete EvidenceUnit conversion plan and facilitator-ledger work queue, implements an adequate memorization-probe gate with model-family quarantine, explicitly names sealed-memo author-context contamination, defines defensible Daimler fallback criteria, and preserves comprehensive non-claims throughout. One major finding (EUP-01: `decision_shape` and `case_family` misattributed as FacilitatorLedger fields) and three minor correctness findings (EUP-02 through EUP-04) should be resolved before a fixture-authoring lane uses this plan as an implementation reference. Two minor friction findings (EUP-05, EUP-06) may be addressed at owner discretion.

**Next authorized step:** Owner decides whether to patch EUP-01 through EUP-04 before commissioning a fixture-authoring lane, or to carry them forward explicitly as named open questions in the fixture-authoring prompt. The fixture-authoring prompt must read `judgement_case_construction_protocol.md` to resolve EUP-01 and EUP-02.

Do not route directly to probe execution, model runs, scoring, implementation, proof-run, product-proof, or lesson promotion.

No patch queue, commit, push, implementation, or validation work is authorized by this review report.

---

*Review closed. Report written to `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md`.*
