# Unity Runtime Fee v0.14 Fixture Extraction Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Docs-only extraction plan for mapping the Unity Runtime Fee case into v0.14 Judgment Harness fixture-admission surfaces.
use_when:
  - Planning a Unity v0.14 fixture-admission work queue before any harness implementation or scoring.
  - Checking Unity participant-packet, evidence-registry, facilitator-ledger, leakage, probe, and sealed-memo boundaries.
  - Deciding when Daimler should replace Unity as the lower-fame-risk next candidate.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md
  - docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md
  - docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md
  - docs/research/judgment-spine/harness/v0_14/index.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md: CEE971DF9313D6DF50439F63058F4A2DF92B0FBD5FE4CE2D4F4226E05616C369
  docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md: 730A707674756E9EB9B7CE9678EBB1C02A3A1D9A2CD5EF3F1B5BB0746DCC569E
  docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md: 2DB46EEF3D6ED6F54451693DC33B5B789066EB1BF26946370B702601650A3C30
stale_if:
  - Any Unity source packet, sealed memo, outcome calibration, reveal readout, or v0.14 harness spec named here changes materially.
  - A memorization probe result is produced for Unity and a target model family.
  - A later owner decision chooses Daimler or another case as the first fixture-admission candidate.
```

- Status: FIXTURE_EXTRACTION_PLAN_V0
- Artifact type: Judgment Spine / v0.14 harness fixture extraction plan
- Output mode used: file-write
- Implementation authorized: no
- Runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, validation execution, or lesson-promotion authorized: no
- Strict acceptance, validation, readiness, source-of-truth promotion, implementation authorization, memorization-probe pass, score-readiness, harness superiority, or product-proof claims: not proven

## Source Context Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus prompt-orchestration overlay, patched bridge foundation, bridge adversarial review, Unity case artifacts, v0.14 harness specs, and Daimler fallback artifacts
  edit_permission: docs-write
  target_scope: Create a docs-only Unity v0.14 fixture extraction plan and narrow discovery pointers only.
  dirty_state_checked: yes
  blocked_if_missing: no
source_context_status: SOURCE_CONTEXT_READY
method_sequence:
  workflow_deep_thinking_reference_loaded: yes
  applied_only_after_source_context_ready: yes
```

Repository state caveat: `git status --short --branch` showed `main...origin/main [ahead 17]`, modified overlay and docs files, modified `docs/workflows/orca_repo_map_v0.md`, and many untracked Judgment Spine, prompt, review, and Unity specimen files before this artifact was written. The target extraction-plan path did not exist. These sources are sufficient for this bounded working plan, but dirty or untracked state does not prove acceptance, validation, readiness, source-of-truth promotion, implementation authorization, or score-readiness.

Required Daimler fallback files were present and read:

- `docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md`
- `docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md`
- `docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md`

## Post-Review Patch Receipt

```yaml
patch_basis:
  review_report: docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md
  review_report_hash: 730A707674756E9EB9B7CE9678EBB1C02A3A1D9A2CD5EF3F1B5BB0746DCC569E
  scope: EUP-01 through EUP-04 only
  patched:
    - EUP-01: distinguish protocol fixture metadata from direct Pydantic FacilitatorLedger fields.
    - EUP-02: map memorization_probe_required and known_fame_risk as protocol leakage inputs, not direct Pydantic ledger fields.
    - EUP-03: add judgement_class to sealed-memo BlindJudgement adaptation gaps.
    - EUP-04: constrain UnderreachObservability.basis to the Pydantic enum and place option-value loss in notes or other.
    - EUP-05: replace copyable case_id placeholder with a freeze-before-authoring convention note.
    - EUP-06: map success-signal criteria to specific plan sections.
  not_patched_here: []
```

This patch receipt is provenance only. It does not prove acceptance, validation, readiness, source-of-truth promotion, implementation authorization, probe pass, score-readiness, product proof, or harness superiority.

## Consumed Goal Fit Check

The source-loaded task still fits the anchor goal: define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.

The source-loaded task still fits the success signal: this plan names the minimum Unity harness-entry shape, identifies the v0.14 files that control it, exposes missing, unsafe, contaminated, and not-proven inputs, and names only non-executable later implementation implications.

Success-signal section map:

| Success-signal criterion | Plan sections that carry it |
| --- | --- |
| Minimum Unity harness-entry shape | `Participant Packet Extraction Plan`, `Evidence Registry Conversion Plan`, `Facilitator-Ledger Work Queue`, `Memorization-Probe Admission Gate`, `Sealed Unity Memo Treatment`, and `Blocked-Before-Scoring Checklist` |
| Controlling v0.14 spec files | `Source-Read Ledger`, plus the v0.14 schema/protocol references embedded in `Evidence Registry Conversion Plan`, `Facilitator-Ledger Work Queue`, `Leakage-Audit Field Mapping`, and `Sealed Unity Memo Treatment` |
| Missing or unsafe inputs | `Registry-Level Missing Fields`, `Leakage-Audit Field Mapping`, `Sealed Unity Memo Treatment`, `Parent-Only And Facilitator-Only Exclusion List`, and `Daimler Fallback Decision Gate` |
| Smallest later implementation scope without authorizing code | `Deferred Implementation Implications` and `Next Authorized Step` |

The source-loaded task still fits the selected next move output-fit check: it maps Unity source material into participant-packet extraction boundaries, EvidenceUnit conversion, facilitator-ledger work queue, leakage-audit fields, required `decision_shape`, sealed-memo contamination handling, parent-only exclusions, hard memorization-probe gate, and Daimler fallback trigger without authorizing code, scoring, probe execution, proof, or validation.

No `BLOCKED_GOAL_CONFLICT` was found.

## Purpose, Non-Use Boundary, And Strict Non-Claims

This plan converts the Unity bridge recommendation into a fixture-admission work queue. It is not the participant packet, evidence registry, facilitator ledger, memorization probe, blind judgment, scoring result, failure log, or case report.

Use it to decide what a later bounded lane must extract, author, adapt, exclude, or block before Unity can enter v0.14 harness scoring for a specific contestant/model family.

Do not use it to:

- expose revealed or outcome material to a participant-facing packet;
- treat Unity as probe-safe or score-ready;
- treat the sealed memo as a fresh contestant run;
- run a model, probe, scorer, validator, or proof workflow;
- create implementation files, tests, packages, configs, runners, schemas-as-code, or automation;
- promote Unity lessons into reusable doctrine;
- claim Judgment Spine, v0.14, product, buyer, or harness superiority proof.

Strict claims that remain not proven: acceptance, validation, readiness, source-of-truth promotion, implementation authorization, model-family probe pass, score-readiness, baseline comparability, semantic evidence support, product proof, lesson transfer, and harness superiority.

## Unity Source-Material Classification

### Participant-Facing Candidates

These can seed a later participant packet only after a clean packet-authoring lane strips commentary, normalizes source references, and preserves the cutoff.

| Material | Candidate use | Conditions |
| --- | --- | --- |
| Unity case identity from the case index | `case_id`, decision family, cutoff, role frame, decision question | Must not include reveal status, lesson language, or outcome facts in participant view. |
| Source packet Phase 0 case frame | decision question, assumed decision-owner role, cutoff, allowed and forbidden source families | Must be rewritten as v0.14 frontmatter and packet body, not copied with process notes. |
| Source packet EU-01 through EU-08 | evidence-unit body seed and source-manifest seed | Must be converted to v0.14 `EvidenceUnit` fields and audited for missing hashes, retrieval timestamps, and pre-decision bases. |
| Source packet Evidence Gaps | known uncertainties section | Must remain framed as unknowns, not as conclusions imported from later calibration. |
| Source packet pre-cutoff source ledger | `source_manifest` seed | Must exclude search snippets, noisy result text, and any source title or body that leaks post-cutoff outcome. |
| Source packet anti-leakage notes | participant warning and facilitator leakage-audit seed | Participant-facing warning can mention forbidden information categories only; detailed leakage audit belongs in the facilitator ledger. |

Participant packet must not include actual outcome, post-cutoff Unity announcements, policy revision or cancellation facts, owner blind-read input, sealed memo recommendations, outcome calibration, reveal readout, frozen band inputs, derived floor or ceiling, must-address items, hidden error labels, decoy labels, or post-decision interpretation.

### Facilitator-Only Candidates

| Material | Facilitator use | Boundary |
| --- | --- | --- |
| Source packet anti-leakage ledger | Populate Pydantic ledger fields `leakage_audit_notes` and advisory `spoiler_inventory`; carry protocol leakage-audit inputs `memorization_probe_required` and `known_fame_risk` through notes or an explicit protocol-to-schema adapter | Not a standalone v0.14 leakage artifact, and not four direct Pydantic `FacilitatorLedger` fields. |
| Source packet source-family caps and missing source classes | Explain packet limits and evidence gaps | Do not turn missing fields into negative evidence unless the v0.14 evidence registry labels the basis. |
| Sealed at-cutoff memo | Advisory or baseline-like existing judgment candidate after adapter review | Not a fresh contestant run; not scoreable until schema/run metadata, evidence IDs, must-address coverage, prompt hash, participant-packet hash, ledger hash, and author-context contamination are handled. |
| Outcome calibration and reveal readout | Post-run calibration and qualitative miss analysis | Must not enter participant packet or frozen scoring truth. |
| Owner blind-read decision inside outcome calibration | Parent Judgment Spine comparison context | User-stated calibration input, not independent contestant output or scoring truth. |
| Bridge foundation and adversarial review | Fixture-extraction constraints and failure modes | Review is historical; patched bridge foundation controls if conflict appears. |

### Parent-Only Material

Parent Judgment Spine material may guide later learning after blind use, but should not be forced into v0.14 fixture fields now.

- Unity reveal readout reusable lessons and tactical reads.
- Outcome calibration verdict and product-proof implications.
- Owner blind-read improvement over the sealed memo.
- Mechanism-psychology, alternative-monetization, and consulting-takeaway prose when stated as post-reveal learning.
- Claims about transfer to future cases.
- Adjacent MV-04 method-validation replay.

### Excluded Material

- Any post-cutoff or outcome source opened during calibration.
- Current Unity pricing pages or later official policy pages when preparing a blind participant packet.
- Retrospective explainers, Wikipedia or summary pages, and snippets/titles revealing backlash, apology, revision, cancellation, leadership changes, or outcome.
- Prior replay artifacts or contaminated archive bodies.
- Search result pages as participant evidence.
- Any source material whose pre-cutoff visibility cannot be established and whose content would change the decision packet.

## Participant Packet Extraction Plan

This section is not the packet. It defines the later packet-authoring queue.

### Required v0.14 Frontmatter

Later packet frontmatter must include:

```yaml
case_id: <freeze_before_authoring>
decision_question: Should Unity proceed with a broad runtime/install-based fee model, narrow or phase the change, grandfather existing users, change messaging, or hold pending further evidence?
decision_date_or_cutoff: 2023-09-11 23:59 Pacific Time
role_frame: executive or senior monetization/package decision owner accountable for product packaging, developer trust, revenue, customer retention, and launch risk
authority_constraints: to be authored from packet-safe role assumptions only
capability_constraints: to be authored from packet-safe source gaps only
permitted_assumptions: to be authored from clean pre-cutoff source packet limits
information_boundary: whitelist-only ("decide using only the information in this brief; not outside or later knowledge about this case"); no enumerated forbidden-category list on the contestant surface
source_manifest: to be converted from source packet source ledger after hash and timestamp audit
```

`case_id` is intentionally not frozen in this plan. A later fixture-authoring lane must freeze one canonical ID before writing any packet, ledger, evidence unit, probe plan, run-adapter, or score-adjacent artifact. Use a filesystem-safe lowercase slug with digits and underscores only, no spaces, no punctuation other than underscores, and no status words such as `candidate`, `draft`, `ready`, `accepted`, `passed`, or `scoreable`. If no narrower convention is accepted before authoring, use `unity_runtime_fee_2023_v0_14` consistently across all fixture artifacts.

### Packet Body Sections

The later participant packet should contain:

- decision frame and cutoff;
- role frame and decision-owner responsibilities;
- pre-cutoff facts from EU-01 through EU-08;
- known uncertainties and source gaps from the source packet;
- permitted assumptions;
- forbidden-information notice;
- clean source manifest.

The packet should not ask the participant to evaluate whether the actual Unity policy was good or bad. It should ask for a bounded at-cutoff decision: hold, watch, narrow, test, option, phase, escalate, move, or commit, expressed through the required blind-judgment schema in a later run.

### Participant-Facing Facts That Must Remain Absent

- actual September 12, 2023 announcement outcome;
- backlash, clarification, apology, revision, cancellation, or later terms-update facts;
- owner blind-read result;
- sealed memo action ceiling;
- outcome calibration assessment;
- reveal readout transfer lessons;
- known v0.14 band labels;
- derived action floor or ceiling;
- must-address item list;
- leakage-audit assessment;
- probe results or fame-risk classification.

## Evidence Registry Conversion Plan

The source packet contains EU-01 through EU-08 in an evidence-unit style, but it is not yet a v0.14 evidence registry.

v0.14 `EvidenceUnit` requires:

```yaml
evidence_id:
source_id:
source:
timestamp:
retrieval_timestamp:
hash:
pre_decision_status:
pre_decision_basis:
summary:
```

### Conversion Table

| Source EU | v0.14 conversion target | Missing or adapter-required fields |
| --- | --- | --- |
| EU-01: Unity platform has distinct Create and Grow monetization surfaces | EvidenceUnit from S-03 with summary about Create/Grow surfaces and runtime/install fee boundary | Need canonical `source_id`, exact filing timestamp or publication date, original retrieval timestamp, source-byte hash, normalized pre-decision basis. |
| EU-02: Unity had visible financial pressure before cutoff | EvidenceUnit from S-03 with summary about 2022 revenue growth, net loss, and operating expenses | Same S-03 field gaps; must avoid inferring private urgency, board pressure, target revenue, timing, or acceptable mechanism. |
| EU-03: Unity revenue depended on both Create and Grow businesses | EvidenceUnit from S-03 with summary about Create/Grow revenue dependence | Same S-03 field gaps; must preserve limit that cohort, game-size, install-count, platform, plan, and developer economics are not proven. |
| EU-04: High-value customer base was material, but distribution details were missing | EvidenceUnit from S-03 with summary about high-value customer materiality and missing distribution details | Same S-03 field gaps; must not imply which customers would face a fee, contract constraints, or exposed churn. |
| EU-05: Unity disclosed renewal, retention, and customer-confidence risks | EvidenceUnit from S-03 with summary about customer confidence, renewal, cancellation, reduced use, and alternatives | Same S-03 field gaps; must not quantify churn, elasticity, switching cost, or fee-specific effect. |
| EU-06: Price and customer economics were public competitive factors | EvidenceUnit from S-03 with summary about competition, price, and customer economics | Same S-03 field gaps; must not prove competitor adoption likelihood or acceptable communications package. |
| EU-07: Alternative engine licensing frame | EvidenceUnit from S-06/S-07 with summary about archived Unreal licensing context | Need exact source hash for archive snapshot, retrieval timestamp, and pre-decision basis from 2023-01-03 archive timestamp; keep contextual authority limit. |
| EU-08: Exact pre-cutoff Unity pricing/terms visibility not established | Adapter decision required: either EvidenceUnit documenting bounded source-visibility failure or facilitator-only evidence-gap note | Need operator decision on status. If kept as EvidenceUnit, timestamp and hash attach to the CDX lookup result, not a Unity pricing fact. Do not treat negative lookup as proof no pricing/terms page existed. |

### Registry-Level Missing Fields

Before a v0.14 evidence registry can be frozen:

- every EU must receive a stable `evidence_id` and `source_id`;
- every source must have a canonical `source` field suitable for participant source manifest or facilitator registry;
- every source needs `timestamp`, `retrieval_timestamp`, and `hash`, with source-byte hash when bytes are available;
- every EU needs `pre_decision_status` from `verified_pre_decision`, `uncertain_timestamp`, or `excluded`;
- every EU needs a normalized `pre_decision_basis`;
- EU-08 needs an explicit adapter decision because it is a source-visibility gap, not ordinary affirmative evidence;
- source packet hash alone is not enough to replace per-source hashes for v0.14 scoring support.

## Facilitator-Ledger Work Queue

This section defines fields that must be operator-authored later. It does not freeze labels.

### Required Identity, Version, And Protocol Metadata

Direct Pydantic `FacilitatorLedger` fields to author later:

- canonical `case_id`;
- `batch_id`;
- `mapping_table_version_pin: v0_14_mvp`;
- `labeling_rubric_version: v0_14`;
- `ledger_authors`, including primary labeler and second labeler;
- `committed_at` in ISO-8601 UTC with `Z` suffix;
- `ledger_freeze_hash` computed over canonical YAML minus the hash field.

Protocol fixture metadata to track in the fixture-admission work queue:

- `case_family` appears in `judgement_case_construction_protocol.md`, but is absent from the current Pydantic `FacilitatorLedger`; a later lane must keep it as case-construction metadata or define an explicit adapter before claiming schema-valid ledger serialization.
- `decision_shape` appears in `judgement_case_construction_protocol.md` and is required by Pydantic `BlindJudgement`; it is absent from the current Pydantic `FacilitatorLedger`, so it must be frozen for the run/BlindJudgement contract and not treated as a direct ledger field unless the schema expands.

### Required Decision Shape

The likely candidate protocol/run `decision_shape` is `ceiling_trap`, because the case tests whether visible revenue pressure and strategic plausibility should still cap a broad runtime/install-fee commitment.

`action_band` is a possible fallback if the operator wants a more general right-sized action fixture. Do not score either shape until the operator freezes exactly one value from the v0.14 allowed set. Under the current Pydantic schema, this is a required `BlindJudgement` field and protocol metadata, not a direct `FacilitatorLedger` field.

### Frozen Band Inputs To Author Later

All of these are required v0.14 enum fields. They must be labeled from packet evidence, second-labeled, diffed, resolved, and frozen before any contestant run.

| Field | Work item |
| --- | --- |
| `evidence_strength` | Decide how much the pre-cutoff evidence supports action beyond exploration. |
| `evidence_independence` | Decide whether S-03-heavy evidence plus Unreal context is correlated, partially independent, or independent. |
| `reversibility_feasibility` | Assess reversibility of broad runtime/install fee, narrow wedge, phase, grandfathering, or hold options. |
| `reversibility_cost` | Assess trust, legal, operational, and ecosystem reversal cost. |
| `authority` | State whether the assumed decision owner has authority for launch, phase, grandfathering, exemptions, or hold. |
| `authority_acquisition_cost` | State what approvals or governance friction are required if authority is partial. |
| `capability` | Assess ability to meter, bill, dispute, support, communicate, and enforce the model from packet-safe evidence. |
| `capability_build_cost` | Assess capability gaps without importing post-reveal implementation evidence. |
| `loss_shape` | Decide whether broad launch has asymmetric-down, ruinous-tail, unknown, or symmetric loss shape from pre-cutoff evidence. |
| `opportunity_cost` | Assess cost of holding or delaying broad runtime monetization from financial-pressure evidence. |
| `information_decay` | Assess whether waiting improves information or loses an expiring window. |
| `option_value` | Assess whether a small wedge, customer test, or grandfathered phase preserves option value. |
| `upside_shape` | Assess whether runtime monetization has asymmetric or convex upside only after evidence gates. |
| `urgency` | Assess timing pressure from public evidence only, not later events. |

### Second-Label Audit

The later ledger must include `second_label_diffs`, even if empty. Quarantine or review is required if:

- more than three band inputs disagree before resolution;
- evidence-strength disagreement exceeds one level;
- loss-shape disagreement includes `ruinous_tail`;
- information-decay disagreement includes `expiring`;
- disagreement cannot be resolved without importing revealed outcome material.

### Must-Address Items

Later operator-authored must-address items should cover at least:

| Candidate item | Evidence basis |
| --- | --- |
| Commercial pressure supports exploration but not broad launch authority by itself | EU-01, EU-02, EU-03 |
| Customer confidence, renewal, cancellation, reduced-use, and substitution risks are decision-critical | EU-05, EU-06 |
| High-value segmentation is plausible but exposure, contract rights, and churn are not proven | EU-04, EU-08 |
| Exact pricing, terms, elasticity, legal enforceability, metering, support, dispute handling, and communications readiness remain unknown | EU-08 and source packet Evidence Gaps |
| Competitor/customer economics context matters but does not prove switching behavior | EU-06, EU-07 |

These are candidate ledger items, not a frozen ledger. They must not be shown to contestants through the participant packet.

### Underreach Observability

Do not default `underreach_observability.present` to true. The source packet shows financial pressure and possible monetization opportunity, but lacks private revenue targets, urgency, customer-level economics, and timing evidence.

A later operator may mark underreach observability true only if the frozen packet and ledger identify an observable source-backed basis. For direct Pydantic `UnderreachObservability.basis`, the valid values are `opportunity_cost`, `window_closure`, `information_decay`, or `other`; option-value loss can be described in `notes` and, if no schema value fits, mapped to `other`. Otherwise, underreach can be logged as advisory, not a primary failure.

### Leakage Audit, Freeze, And Commit

The later facilitator ledger work queue must preserve both the Pydantic schema surface and the case-construction protocol leakage controls.

Direct Pydantic `FacilitatorLedger` fields:

- `leakage_audit_notes` from the source packet anti-leakage ledger and this plan's exclusion list;
- `spoiler_inventory` naming withheld artifact categories, advisory in the Pydantic reference;
- `ledger_freeze_hash`;
- `committed_at`;
- `mapping_table_version_pin`;
- `labeling_rubric_version`.

Protocol leakage-audit inputs to carry in `leakage_audit_notes` or a later explicit protocol-to-schema adapter:

- `memorization_probe_required: true`;
- `known_fame_risk: elevated` or another operator-frozen value with rationale.

No scoring may occur before the ledger is frozen.

## Leakage-Audit Field Mapping

Unity does not need a standalone v0.14 leakage artifact. Leakage and spoiler controls map into the facilitator ledger, but the current v0.14 sources split this across two layers: `pydantic_schema_reference.md` exposes `leakage_audit_notes` and advisory `spoiler_inventory`, while `judgement_case_construction_protocol.md` names protocol leakage-audit inputs including `memorization_probe_required` and `known_fame_risk`.

| v0.14 surface | Unity source input | Planned value or rule |
| --- | --- | --- |
| Pydantic `leakage_audit_notes` | Source packet Anti-Leakage Ledger; case index missing-residue note; bridge foundation caveats | Carry: query cap used, page-open cap used, snippet-noise was present but not preserved, no post-cutoff/outcome pages opened in the source packet, no prior replay artifacts read, no contaminated archive bodies read, Unity is revealed outside participant view, protocol probe requirement, and known fame-risk rationale. |
| Pydantic advisory `spoiler_inventory` | Unity case index, sealed memo, outcome calibration, reveal readout | Withhold: sealed memo recommendation, owner blind-read decision, actual outcome, backlash/revision/cancellation facts, outcome source ledger, calibration verdict, reveal lessons, product-proof implications. |
| Protocol leakage input `memorization_probe_required` | v0.14 memorization probe protocol and bridge foundation | `true` for every target contestant/model family before packet exposure; not a discrete current Pydantic `FacilitatorLedger` field unless a later adapter or schema revision adds it. |
| Protocol leakage input `known_fame_risk` | Bridge foundation and review AR-01 | `elevated` or `high`; Unity Runtime Fee was a widely public 2023 event and may be known to frontier models. Not a discrete current Pydantic `FacilitatorLedger` field unless a later adapter or schema revision adds it. |

The leakage audit must also record that source packet snippet-noise existed but leaked facts were not quoted or preserved. If any later packet-authoring lane opens a snippet, URL, title, or page that reveals post-cutoff outcome, the participant-facing packet is contaminated and must be rebuilt.

## Memorization-Probe Admission Gate

The memorization probe must run before a contestant/model family sees the Unity participant packet. This plan does not run it.

Required probe input fields:

- `case_id`;
- decision question;
- minimal public identifiers;
- decision date or cutoff;
- probe model family;
- probe model ID;
- probe prompt template version;
- prompt hash and raw response hash in the artifact.

Routing:

| Probe result | Case handling |
| --- | --- |
| `pass` | Unity is usable for that model family only. Passing does not prove no memorization. |
| `fail` | Reject or quarantine Unity for that model family. Log or plan `memorization_probe_failed` as blocking if a failure log later exists. |
| `ambiguous` | Quarantine until operator review. Treat as material blockage, not a routine missing field. |

Model-family quarantine rule: a failure invalidates the contestant-case pair for that model family. It does not automatically invalidate Unity for all families, but if all intended frontier families fail or remain ambiguous, Unity should not be the first scoreable fixture. Use Unity only as parent Judgment Spine material or extraction-planning material, and switch to the Daimler fallback route if the workstream needs a live blind-run or scoreable candidate.

## Sealed Unity Memo Treatment

The sealed at-cutoff memo is useful, but it is not automatically a v0.14 `BlindJudgement`.

Default treatment: advisory or baseline-like existing judgment candidate, not a fresh contestant run and not scoring truth.

It may be adapted only if a later lane can represent these fields without fabrication:

| Required area | Current gap |
| --- | --- |
| `decision_shape` | Must be frozen, likely `ceiling_trap` or `action_band`; current memo predates the v0.14 enum. |
| `judgement_class` | Must map to exactly one of `recommend`, `abstain`, `wait`, `escalate`, or `irreducible_uncertainty`; current memo predates this schema and must not receive a hindsight class assignment. |
| contestant/run metadata | Missing v0.14 `contestant_id`, `run_id`, `model_id`, `model_family`, `model_snapshot_if_available`, `temperature`, `seed_if_supported`, and `harness_version` in the required run sense. |
| `prompt_hash` | Memo header has source packet hash, but not a v0.14 rendered-prompt hash. |
| packet and ledger hashes | No v0.14 participant packet or facilitator ledger existed when the memo was written. |
| recommended action | Memo states an action ceiling and recommendations, but needs ladder-level mapping without hindsight or invented scoring. |
| `evidence_used` | Memo cites EU-01 through EU-08 in prose; needs claim IDs, claim roles, and evidence-unit ID lists. |
| must-address coverage | No v0.14 must-address list existed; coverage must be reconstructed after ledger authoring. |
| advisory fields | Any severe-error assessment, reversal triggers, or probabilities are advisory only in Phase 1. |
| author-context contamination | The memo may reflect author expertise, prompt context, source-selection context, and internal assumptions beyond what a clean participant packet would expose. |

If adapted, the memo should be labeled as a legacy sealed memo or baseline-like input in the case report. It should not be compared to fresh model contestants as if all saw the same packet under the same runner contract unless a later lane proves comparability.

If the adapter cannot preserve these caveats, exclude the sealed memo from v0.14 scoring and keep it as parent Judgment Spine calibration material.

## Parent-Only And Facilitator-Only Exclusion List

### Exclude From Participant View

- sealed memo recommendations and action ceiling;
- owner blind-read decision;
- actual outcome and post-cutoff Unity policy path;
- outcome calibration assessment;
- reveal readout capsule, lessons, and tactical reads;
- product-proof implications;
- post-cutoff source URLs, source titles, snippets, or source body text;
- known fame-risk classification and probe results;
- facilitator ledger, band labels, action floor/ceiling, must-address items, underreach assessment, leakage audit, and failure events.

### Exclude From v0.14 Scoring Truth

- reveal readout lessons;
- outcome calibration verdict;
- owner blind-read judgment unless separately represented as a schema-valid contestant under a comparable packet/run contract, which is not proven;
- product-proof implications;
- semantic claim support beyond v0.14 shallow evidence checks;
- any lesson-promotion or transfer claim.

### Keep As Parent Judgment Spine Material

- mechanism-psychology lesson;
- alternative monetization lesson;
- implementation-cost as strategy lesson;
- switching-cost segmentation lesson;
- calibrated action ceiling after reveal;
- consulting takeaway.

These can inform future case-learning or lesson-promotion lanes only under the Judgment Spine thesis operating contract, not this fixture plan.

## Daimler Fallback Decision Gate

Daimler becomes the better next candidate or fallback route when the objective shifts from "bridge existing Unity material into v0.14 shape" to "run a lower-fame-risk blind case or first scoreable fixture."

Switch or defer to Daimler if any of these occur:

- Unity fails or remains ambiguous on memorization probes for the target model families.
- The owner wants the next lane to collect a fresh blind judgment rather than adapt an existing sealed memo.
- Unity participant-packet extraction cannot avoid leakage from revealed or outcome material.
- Unity evidence registry cannot reconstruct required hashes, timestamps, or pre-decision bases without opening contaminating sources.
- The sealed memo is needed for scoring but cannot be adapted without hiding author-context contamination.
- The first scoreable candidate is more important than exercising the richest bridge-from-existing-material chain.

Daimler fallback prerequisites remain unresolved:

- Daimler is not listed in the manifest's current case inventory.
- Daimler has a participant packet and safety receipt, but lacks sealed blind judgment, owner critique, reveal readout, outcome calibration, v0.14 evidence registry, facilitator ledger, frozen band inputs, second-label diffs, memorization probe, scoring result, and failure events.
- Daimler's lower fame risk is plausible, not a probe pass.

## Blocked-Before-Scoring Checklist

Unity must remain blocked before any v0.14 scoring, failure logging, baseline comparison, proof-run, or implementation scoping until all applicable items below are resolved:

- Clean participant packet written from pre-cutoff inputs only.
- Participant packet hash produced.
- Evidence registry converted for EU-01 through EU-08 with required fields, hashes, retrieval timestamps, and statuses.
- EU-08 adapter decision resolved.
- Facilitator ledger authored with required identity, version, authors, band inputs, must-address items, underreach observability, leakage fields, committed timestamp, and freeze hash.
- Second-label audit completed and disagreements resolved or case quarantined.
- `decision_shape` frozen.
- Memorization probe run and passed for the target contestant/model family.
- Sealed memo treatment decided: excluded, advisory/baseline-like, or adapted with explicit contamination caveats.
- Any adapted blind judgment has required run metadata, prompt hash, evidence IDs, must-address coverage, and schema-valid ladder mapping.
- Mapping-table version pin matches v0.14.
- No participant-facing leakage from reveal, outcome calibration, owner blind read, sealed memo conclusions, or post-cutoff sources.
- Failure-event logging policy remains `not_a_rule: true` and `promotion_allowed: false`.

Until then, Unity is not score-ready and probe-safety is not proven.

## Deferred Implementation Implications

These are non-executable implications only. They do not authorize code or implementation scoping.

A later owner-authorized implementation-scoping prompt would need to bind a single fixture-admission slice, likely:

- schema surfaces for `ParticipantPacket` frontmatter, `EvidenceUnit`, `FacilitatorLedger`, `BlindJudgement`, `ActionBandResult`, `ScoringResult`, and `FailureEvent`;
- deterministic action-band mapping and scorer formulas from v0.14;
- a source-packet-to-ParticipantPacket and EvidenceUnit adapter for Unity;
- a facilitator-ledger authoring and freeze workflow;
- a memorization-probe artifact shape and quarantine routing;
- a sealed-memo adapter that can preserve non-comparability rather than erase it.

Do not implement any of that from this plan. A later implementation-scoping lane must reopen `phase_1_infrastructure_architecture.md`, recheck source state, bind target files, and obtain explicit bounded implementation authorization.

## Source-Read Ledger

| Source | Why read |
| --- | --- |
| `AGENTS.md` and `.agents/workflow-overlay/README.md` | Workspace and overlay authority. |
| `.agents/workflow-overlay/source-of-truth.md`, `source-loading.md`, `prompt-orchestration.md`, `artifact-roles.md`, `artifact-folders.md`, `validation-gates.md`, `retrieval-metadata.md` | Source hierarchy, read budget, method sequencing, artifact permissions, accepted folder, validation, and retrieval-header rules. |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` and `judgment_spine_thesis_operating_contract_v0.md` | Parent Judgment Spine goal, layer boundary, drift guard, and non-claims. |
| `docs/research/judgment-spine/README.md`, `manifest_v0.md`, `docs/workflows/orca_repo_map_v0.md` | Case-unit shape, current case inventory, harness inventory, and navigation context. |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 spec index and source-of-truth roles. |
| `case_to_v0_14_bridge_foundation_v0.md` | Controlling bridge recommendation and minimum harness-entry shape. |
| `case_to_v0_14_bridge_foundation_adversarial_review_v0.md` | Historical review findings, especially Unity probe-risk differential, leakage-field mapping, sealed-memo contamination, and `decision_shape` gap. |
| Unity case index, source packet, sealed memo, outcome calibration, and reveal readout | Unity artifact status, clean pre-cutoff evidence, existing sealed judgment-like material, reveal/calibration exclusions, and parent-only lessons. |
| v0.14 thesis, strategy, case protocol, schemas, labeling rubric, mapping table, executable spec, scorer formula, blind-judgment protocol, memorization probe, failure log, proof and memory plan | Required schema, ledger, mapping, scoring, probe, failure-log, and claim-discipline controls. |
| Daimler preflight, participant packet, and safety receipt | Fallback candidate status, lower-fame-risk route, existing zero-spoiler packet, safety boundary, and missing artifacts. |

Sources deliberately not read: all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, and runtime files. They were not needed for this extraction plan and would have widened beyond the prompt.

## Next Authorized Step

The next authorized step is docs-only: use `docs/prompts/deep-thinking/judgment_spine_unity_v0_14_fixture_authoring_ca_prompt_v0.md` to author a blocked-before-scoring Unity v0.14 draft fixture pack, or run a read-only adversarial artifact review of that draft pack after it exists.

Do not route directly to implementation, probe execution, model runs, scoring, proof-run, product-proof, lesson promotion, or harness-superiority claims.
