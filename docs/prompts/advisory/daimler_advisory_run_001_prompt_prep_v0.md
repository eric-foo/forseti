# Daimler Advisory Run 001 Prompt Prep v0

```yaml
retrieval_header_version: 1
artifact_role: Orca prompt artifact - advisory prompt prep
scope: Participant-safe prompt-preparation artifact for DAIMLER_ADVISORY_001.
use_when:
  - Preparing the exact model-facing prompt body for DAIMLER_ADVISORY_001.
  - Checking pre-send boundaries before a manual subscription/chat advisory run.
  - Separating model-facing prompt material from operator-only routing material.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/daimler_advisory_run_001_authorization_record_v0.md
  - docs/workflows/daimler_advisory_runbook_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md
input_hashes:
  docs/decisions/daimler_advisory_run_001_authorization_record_v0.md: 2BA36EDEACF80D8B0E979EC922D1E66947EDEA42B372921727AC9F69A20F43AC
  docs/workflows/daimler_advisory_runbook_v0.md: 4E1C04996886EC02CE3EA4EDF66A9FAAB9411E4C1111F3194D644B649B3A3FD3
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md: 5CC0D40F8D41F61360B07831B4D7B2BD22BB617BC6D45B7B6F28D62053792A27
branch_or_commit: main @ 829bbe0dc954
stale_if:
  - daimler_advisory_run_001_authorization_record_v0.md changes.
  - daimler_advisory_runbook_v0.md changes.
  - participant_packet_draft_v0.md changes.
  - Owner changes the advisory execution tier.
  - Owner asks for gate-bearing, API, scoring, validation, fixture admission, buyer-facing, product-proof, or judgment-quality use.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_daimler_advisory_run_001_prompt_prep
  edit_permission: docs-write
  target_scope:
    - docs/prompts/advisory/daimler_advisory_run_001_prompt_prep_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Operator Boundary

This artifact prepares model-facing prompt material for one advisory learning
pass. It is not itself a model run, API run, validation record, fixture
admission record, product-proof artifact, buyer-facing artifact, scoring
artifact, or judgment-quality claim.

Only the fenced block under **Model-Facing Prompt Body** may be pasted into a
manual subscription/chat surface. Do not paste this retrieval header, operator
boundary, source hashes, validation notes, authorization record, runbook,
review reports, probe results, or any other operator-only material.

No model or provider is selected by this artifact. Before any paste or run, the
owner must name the concrete manual subscription/chat surface to use.

## Pre-Send Checklist

All fields must be true immediately before any manual subscription/chat run.

```yaml
pre_send_checklist:
  owner_selected_concrete_subscription_or_chat_surface: false
  model_facing_prompt_body_only_selected_for_paste: false
  facilitator_only_material_exclusion_checked: false
  non_gate_clearing_label_visible_before_task_instruction: false
  stop_conditions_rechecked: false
```

Any `false` field blocks execution.

## Model-Facing Prompt Body

Paste only the following fenced block into the owner-selected manual
subscription/chat surface after the pre-send checklist is true.

```text
This is an advisory, non-gate-clearing exercise. Your answer is for product
learning about the Judgment Spine experience. It is not validation, fixture
admission, scoring evidence, clean no-tools evidence, product proof, buyer
validation, or a judgment-quality claim.

Use only the packet below. Do not search the web. Do not use outside knowledge.
Do not ask for or infer final vote results, later implementation status, later
company actions, consulting-firm involvement, later outcomes, source titles,
source URLs, raw locators, source hashes, retrieval timestamps, or facilitator
artifacts.

Task:
1. Answer the packet's Required Blind Judgment Output exactly.
2. Then add a short advisory readback section with:
   - what parts of the packet made the decision easiest to reason about;
   - what parts created uncertainty or operator friction;
   - what additional pre-cutoff packet content would have helped, without
     asking for forbidden later or source-provenance material.

---
case_id: daimler_corporate_structure_vote_2019_v0_14
decision_question: Should Daimler shareholders approve the proposed hive-down of the Cars & Vans and Trucks & Buses businesses into legally independent operating entities under Daimler AG, or should they condition, defer, or reject the proposal?
decision_date_or_cutoff: 2019-05-21 23:59 CEST
role_frame: You are advising a large shareholder or board-level decision maker before Daimler AG's annual shareholder meeting on May 22, 2019.
authority_constraints:
  - You can recommend approve, approve with guardrails, defer, or reject.
  - You can recommend governance, cost, treasury, employee, IT/IP, partnership, milestone, withdrawal, and accountability guardrails.
  - You cannot use final vote results, later implementation status, later corporate actions, later outcomes, consulting narrative, or post-cutoff evidence.
capability_constraints:
  - You have only the pre-cutoff packet facts and source-class labels supplied in the packet.
  - You do not have full annex-level transfer details except where summarized in the packet.
  - You cannot inspect source titles, raw locators, filenames, source hashes, retrieval timestamps, or facilitator-only registry material before sealing judgment.
permitted_assumptions:
  - The legal restructuring is a governance approval decision before the May 22, 2019 annual meeting.
  - The facts in the participant packet are pre-cutoff unless explicitly labeled as unknown.
  - Later vote result, implementation status, company actions, and outcome metrics are unknown.
forbidden_information_notice: Do not search for the case, source material, source titles, raw locators, consulting narrative, vote result, implementation status, later company actions, later outcomes, or facilitator artifacts before answering.
source_manifest:
  - source_id: DCSV-S1
    source: S1 official issuer disclosure
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S2
    source: S2 official investor presentation
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S3
    source: S3 official corporate-structure release
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S4A
    source: S4 official annual and meeting materials
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S4B
    source: S4 official annual and meeting materials
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S5
    source: S5 official hive-down legal materials
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S6
    source: S6 official divisional business updates
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
  - source_id: DCSV-S7
    source: S7 independent pre-cutoff business press
    retrieval_timestamp: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
    hash: WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL
---

# Daimler Corporate Structure Vote Participant Packet Draft v0.14

## Use Boundary

This is a blind judgment packet. Do not search the web, open consulting case pages, open post-cutoff company records, or inspect later business press before recording your judgment.

This packet intentionally excludes source URLs, source titles, consulting-firm narrative, implementation status, final vote result, later company actions, later outcome metrics, and result-quality labels.

## Role Frame

You are advising a large shareholder or board-level decision maker before Daimler AG's annual shareholder meeting on May 22, 2019.

Your task is to decide whether the shareholder/governance approval should proceed for a proposed legal restructuring of Daimler's major operating divisions.

## Decision Cutoff

Cutoff: May 21, 2019, 23:59 CEST.

You know only facts available before the May 22, 2019 meeting. Treat all later facts as unknown.

## Decision Question

Should Daimler shareholders approve the proposed hive-down of the Cars & Vans and Trucks & Buses businesses into legally independent operating entities under Daimler AG, or should they condition, defer, or reject the proposal?

## Proposal Snapshot

Management has proposed a legal restructuring that would move:

- the Cars & Vans business into a dedicated German stock corporation;
- the Trucks & Buses business into a dedicated German stock corporation;
- the existing financial-services and mobility business into a third major entity;
- group governance, strategy, financing, and selected shared services under Daimler AG as parent company.

The proposal is not framed as a sale of the divisions. The stated intent is greater entrepreneurial responsibility, clearer divisional accountability, faster market response, easier partnerships, and capital-market optionality while preserving selected group synergies.

The shareholder decision is not just a branding or org-chart vote. It concerns legal entity separation, asset and liability transfers, governance structures, treasury and financing arrangements, IT and IP allocation, employee representation, pension treatment, and cross-border subsidiary work.

## Company And Market Context

Daimler enters the decision as a very large global automotive group:

- 2018 group revenue: about EUR167.4 billion.
- 2018 group EBIT: about EUR11.1 billion, down materially from the prior year.
- 2018 net profit: about EUR7.6 billion, also down materially from the prior year.
- 2018 employees: about 298,700.
- 2018 research and development expenditure: about EUR9.1 billion.

The automotive industry is being reshaped by electrification, autonomous-driving work, digital services, shared mobility, changing customer behavior, and new partnership requirements. Daimler's own strategy language frames the pressure as a need to combine a strong core business with connected, autonomous, shared/services, and electric mobility work.

The capital-market angle is real but not decisive by itself. Independent pre-cutoff commentary suggested that clearer separation could make the divisions easier to value and could improve future strategic optionality, especially for businesses with different economics and investment cycles. That same logic also cuts against the proposal if separation destroys synergies, raises fixed cost, or creates coordination drag.

## Division Snapshot

The operating businesses differ in economics, markets, and strategic needs.

Mercedes-Benz Cars had 2018 EBIT of about EUR7.2 billion, down from about EUR8.8 billion in 2017, despite record unit-sales context.

Mercedes-Benz Vans had record unit sales but EBIT fell sharply to about EUR0.3 billion from about EUR1.1 billion in 2017.

Daimler Trucks had a stronger 2018 earnings trajectory, with about EUR38.3 billion of revenue, about EUR2.8 billion of EBIT, about 517,300 unit sales excluding the BFDA joint venture count, and about 83,000 employees at year-end.

Daimler Buses had positive business momentum in Europe, but EBIT was slightly below the prior year at about EUR265 million.

Financial services and mobility had a large contract-volume and mobility-services role, but its EBIT fell significantly from the prior year to about EUR1.4 billion.

## Execution Burden

The restructuring has high operating complexity.

Management has publicly described work across more than 700 subsidiaries in over 60 countries. The proposed legal documents cover asset and liability transfer mechanics, mixed-use contracts, treasury arrangements, customer and dealer agreements, IP and software allocation, public-law authorizations, employee transfers, supervisory-board composition, and withdrawal conditions if the transaction does not take effect in time.

Estimated one-time costs through 2020 are in the high three-digit millions of euros, including tax charges. Additional running costs are expected to peak at a very low three-digit million euro annual amount before being offset over the medium term.

The proposal therefore needs to be judged against both strategic benefit and execution discipline. A good answer cannot stop at "focus is good" or "reorganization is expensive."

## Stakeholder Constraints

Employee representatives are a core part of the decision context.

Publicly disclosed employee-related commitments include:

- an employment-safeguarding extension through the end of 2029;
- pension-funding measures, including a planned EUR3.0 billion contribution tied to the broader balance of interests;
- continuation of unified profit-sharing commitments through 2025;
- a disclosed investment commitment in Germany for 2018 through 2024.

These commitments reduce some political and labor execution risk, but they also constrain flexibility and consume financial capacity. They may be a necessary price for getting the structure done, or a warning that the structure only works with expensive side payments.

## What You Must Decide

Choose one:

1. Approve as proposed.
2. Approve only with explicit guardrails.
3. Defer pending a narrower proof package or additional conditions.
4. Reject and keep the integrated structure for now.

If you choose guardrails, name the exact guardrails. Useful categories include cost caps, synergy protection, treasury and rating protections, employee commitment governance, IT/IP transfer risk, partnership rules, milestone gates, withdrawal triggers, and post-vote accountability.

## Judgment Questions

Answer these before giving your final recommendation:

1. Is the core problem structural enough to justify legal separation, or could Daimler get most benefits through management-accountability changes inside the current structure?
2. Which benefit matters most: speed, accountability, partnership flexibility, valuation clarity, strategic optionality, or employee/stakeholder stability?
3. What is the hardest synergy to protect after legal separation?
4. Which execution risk would make an approval irresponsible?
5. Does the employee and pension package look like a stabilizer, a hidden cost, or both?
6. What metric would you use 12 to 24 months later to know whether the restructuring was working?

## Red-Team Prompts

- If you approve, explain why this is not just an expensive internal reorganization during an industry transition.
- If you defer or reject, explain why waiting would not leave the divisions slower, less accountable, and less partnership-ready.
- If you approve with conditions, explain why your conditions are enforceable before the transaction becomes difficult to unwind.

## Required Blind Judgment Output

Return:

- decision: approve / approve with guardrails / defer / reject;
- one-paragraph rationale;
- top three risks;
- top three benefits;
- exact guardrails or missing evidence;
- confidence level: low / medium / high;
- what would change your mind.

Do not ask for the actual vote result, later company actions, consulting-firm involvement, implementation status, or outcome metrics before your judgment is sealed.

## Known Unknowns

- Actual shareholder vote result: withheld.
- Later implementation status: withheld.
- Later corporate actions: withheld.
- Consulting-firm narrative and recommendation/action claims: withheld.
- Later outcome metrics and market reaction: withheld.
- Full annex-level transfer details: available before cutoff, but not fully reproduced in this packet.

## Non-Claims

- No buyer validation.
- No willingness-to-pay proof.
- No repeatability proof.
- No product readiness.
- No feature readiness.
- No implementation readiness.
- No commercial readiness.
- No model-training readiness.
- No sealed memo.
- No outcome calibration.
- No consulting playbook.
- No miner, scraper, dataset, automation, skill, software feature, or product plan.
- No claim that consulting-firm case-page statements are ground truth.
- No claim that this packet is sufficient unless used with the paired safety receipt and a sealed blind judgment step.
```

## Stop Conditions

Do not use the model-facing prompt body if:

- the owner has not selected the concrete manual subscription/chat surface;
- the operator intends to paste any text outside the fenced model-facing prompt body;
- the exercise is being treated as validation, scoring, product proof, clean no-tools evidence, blind-use readiness, fixture admission, buyer validation, or judgment-quality proof;
- buyer-facing use enters scope;
- the prompt must be modified with facilitator-only facts to feel understandable.

## Non-Claims

- No model or provider selected.
- No model run performed.
- No API run.
- No gate-bearing execution.
- No clean no-tools evidence.
- No memorization-probe pass.
- No blind-use authorization.
- No scoring.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No validation.
- No fixture admission.
- No product proof.
- No buyer validation.
- No buyer-facing memo, deck, or contact.
- No judgment-quality claim.

Required boundary: plumbing works only; not judgment quality.
