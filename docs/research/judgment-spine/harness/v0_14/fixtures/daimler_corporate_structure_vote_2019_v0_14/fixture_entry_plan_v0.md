# Daimler Corporate Structure Vote v0.14 Fixture Entry Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Docs-only fixture-entry plan for moving the Daimler corporate-structure vote case from parent case artifacts into a v0.14 draft fixture pack.
use_when:
  - Preparing the Daimler v0.14 draft fixture pack.
  - Checking ordered prerequisites before source acquisition, packet conversion, evidence registry, probe request prep, or facilitator ledger planning.
  - Verifying blocked gates before any contestant exposure, probe, model run, scoring, ledger freeze, schema implementation, validation, product proof, or judgment-quality claim.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_daimler_pressure_test_v0.md
input_hashes:
  docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md: E60B496101E154401EA9D6E0E5C2EC58701A7EF1E1FBEC4C01A9C5E392D0347F
  docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_daimler_pressure_test_v0.md: 4CC5C50502D8AB2E71D07FEFA514757A3645A6F455161420D7D47DCA9659D020
  docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
  docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md: ED80A0C0D7EC2252E5FC07EC175CFAD3FEE5F3D1F4527812A7813E2C5EE85EE4
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 96B2EF245E6E92A11024D1BAD3B26C2C18B45283831B5D5C1ED209B30A55AF8A
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md: 4DCFEF6800A0AF85F5FA26534C4E863174007737B9FB02B1B3B3D78C96F31BFE
branch_or_commit: main @ a2aebdd8e04c627c5102e79eb324b24b3de35226
stale_if:
  - decision cutoff, role frame, case ID, target model families, source-manifest split, or v0.14 fixture-entry protocol changes.
  - any participant-facing Daimler material is exposed to GPT-5.5, Claude Opus, or another target contestant before a model-family scoped memorization probe passes.
  - S1-S7 source retrieval finds a source cannot be captured pre-cutoff without leaking outcome, source identity, title, URL, or post-cutoff facts into participant-facing material.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: true
  overlay_read: true
  source_pack: custom_daimler_fixture_entry_minimal
  artifact_roles_checked: true
  retrieval_metadata_checked: true
  edit_permission: docs_only_fixture_entry_plan
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
  dirty_state_checked: true
  blocked_if_missing: false
```

## Spec Status

`SPEC_NOT_NEEDED_READY_FOR_SCOPING`.

The operating contract is already narrow enough to execute as documentation: create a draft-only fixture-entry plan, not a fixture admission artifact, not a participant packet, not a source registry, not a probe request, not a run ledger, and not a validation claim.

## Post-Review Patch Note

This version incorporates the review-use findings from `docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md`. The review remains decision input only; this note is not approval, validation, fixture admission, blind-use readiness, mandatory remediation, or judgment-quality proof.

## Owner-Accepted Routing

```yaml
case_id: daimler_corporate_structure_vote_2019_v0_14
fixture_folder: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/
parent_case_folder: docs/research/judgment-spine/cases/daimler-carve-out/
owner_status: accepted_for_draft_fixture_entry_only
target_contestant_families_later:
  primary: GPT-5.5
  backup: Claude Opus
probe_public_identifiers_later:
  - Daimler AG
  - corporate-structure / hive-down shareholder vote
  - May 22, 2019 annual meeting
fixture_status: not_admitted
blind_use_status: blocked
judgment_quality_status: not_claimed
```

## Current State

Daimler has a parent case seed, participant-facing packet seed, and safety receipt:

- `case_02_preflight_v0.md` frames Daimler as a public-company corporate-structure and divisional carve-out decision with a pre-decision participant frame.
- `participant_packet_v0.md` gives a zero-spoiler shareholder or board-level decision packet for the May 22, 2019 annual meeting vote.
- `safety_receipt_v0.md` records the packet as clean as drafted and identifies S1-S7 source classes.

The case is plausible as a fresh blind-run candidate because the decision is public, bounded, pre-decision, source-retrievable, and lower fame-risk than many post-outcome strategic cases. That is only a routing judgment. It does not mean the fixture is accepted, probe-passed, score-ready, validated, or judgment-quality-proven.

## Exact Fixture-Entry Goal

The v0.14 fixture-entry goal is a draft fixture pack that can be reviewed before any contestant exposure:

- `participant_packet_draft_v0.md` converted from the existing packet into v0.14 packet shape.
- `evidence_registry_draft_v0.md` containing facilitator-only source provenance, source-byte hashes, retrieval timestamps, pre-decision status, and summaries.
- `facilitator_ledger_work_queue_v0.md` or equivalent draft ledger planning artifact, explicitly unfrozen.
- `memorization_probe_request_prep_v0.md` defining model-family scoped probe inputs without running the probe.
- `fixture_authoring_receipt_v0.md` or equivalent admission checklist only after source retrieval and packet conversion are complete.

This plan is not any of those artifacts. It is the ordered route to produce them.

## Ordered Route

### STEP-1 Source Acquisition

Retrieve S1-S7 from owner-approved public or owner-supplied sources. For each source, capture:

- stable source identifier;
- source type;
- canonical retrieval location in facilitator-only notes;
- retrieval timestamp;
- raw source bytes or explicit owner/source retrieval blocker;
- `sha256(source_bytes)` when bytes are available;
- pre-decision status and basis;
- participant-safe source-class label.

Stop if a required source cannot be captured as pre-cutoff facilitator-only evidence without relying on post-cutoff facts, consulting-firm narrative, or final outcome leakage. Titles, URLs, filenames, and source identity may exist in the facilitator-only registry; the stop trigger is leakage of those identifiers, post-cutoff facts, or outcome cues into participant-facing material.

### STEP-2 Evidence Registry Draft

Convert the source captures into v0.14-style evidence units. The evidence registry is facilitator-only and may contain source titles, URLs, retrieval timestamps, and source-byte hashes. It must keep participant-safe summaries separate from full provenance.

Required draft fields per unit:

- `evidence_id`;
- `source_id`;
- `source`;
- `source_type`;
- `timestamp`;
- `retrieval_timestamp`;
- `hash`;
- `pre_decision_status`;
- `pre_decision_basis`;
- `summary`;
- participant-safe source-class label.

### STEP-3 Participant Packet Conversion

Convert `participant_packet_v0.md` into v0.14 packet form while preserving the current zero-spoiler body. Add or normalize:

- `case_id`;
- role frame;
- decision question;
- decision date and cutoff;
- `authority_constraints`;
- `capability_constraints`;
- `permitted_assumptions`;
- `forbidden_information_notice`;
- known uncertainties;
- packet-safe evidence-source manifest using source-class labels only.

Participant view must not include final vote, later implementation, later outcomes, consultant narrative, source titles, URLs, source-byte hashes, or retrieval timestamps.

### STEP-4 Leakage Adapter

Apply the Daimler pressure-test split:

- participant packet gets packet-safe source classes;
- evidence registry gets full facilitator-only provenance;
- safety receipt seeds leakage-audit and spoiler-inventory planning only through an explicit adapter note in the later `facilitator_ledger_work_queue_v0.md`, under `leakage_audit_notes` and `spoiler_inventory`, with no participant-facing copy.

Stop if the packet cannot explain evidence basis without exposing source identity or post-cutoff facts.

### STEP-5 Facilitator Ledger Planning

Create an unfrozen ledger work queue. It should name fields and owners, not fill final judgment labels. Required later fields include:

- `case_id`;
- `batch_id`;
- `labeling_rubric_version`;
- `mapping_table_version_pin`;
- `ledger_authors`;
- `second_label_diffs`;
- `frozen_band_inputs`;
- `must_address_items`;
- `underreach_observability`;
- `leakage_audit_notes`;
- `spoiler_inventory`;
- `committed_at`;
- `ledger_freeze_hash`.

Protocol-only information such as decision family, fame risk, and memorization-probe requirement should be carried in leakage-audit notes or spoiler inventory until a dedicated schema slot exists.

Probe result recording must also be reserved before any probe is run. Until a dedicated schema slot exists, the ledger work queue should carry the eventual probe pass/fail/quarantine state as a named `leakage_audit_notes.probe_result_status` entry, not as an unstructured side note.

### STEP-6 Blind-Use and Probe Request Prep

Prepare, but do not run, model-family scoped memorization probe inputs:

- `case_id`;
- decision question;
- public identifiers;
- decision cutoff;
- target family: GPT-5.5 primary;
- backup family: Claude Opus;
- probe prompt template version;
- rejection/quarantine rule for failed or ambiguous probe results.

GPT-5.5 and Claude Opus must not see participant packet material before their scoped memorization probes pass.

### STEP-7 Draft Fixture Pack Review

After STEP-1 through STEP-6 are complete, review the draft fixture pack for:

- source registry completeness;
- packet/source-manifest separation;
- evidence-unit completeness;
- leakage and spoiler controls;
- unfrozen ledger status;
- probe-request readiness;
- absence of readiness, validation, product-proof, score, or judgment-quality claims.

Only then should an owner decide whether to authorize probe execution or any fixture admission path.

## S1-S7 Source Acquisition Needs

| Source class | Needed retrieval work | Participant-safe handling |
| --- | --- | --- |
| S1 Official issuer disclosure from October 2017 | Retrieve source bytes, timestamp, hash, and pre-decision basis for initial rationale, feasibility state, employee context, and pension context. | Use source-class label only. |
| S2 Official investor presentation from May 2018 | Retrieve source bytes, timestamp, hash, and basis for approval threshold and due-diligence scope. | Use source-class label only. |
| S3 Official corporate-structure release from July 2018 | Retrieve source bytes, timestamp, hash, and basis for proposal mechanics, entity model, cost burden, employee commitments, and timing. | Use source-class label only. |
| S4 Official 2018 annual reporting and pre-vote annual-meeting materials | Retrieve source bytes, timestamp, hash, and basis for group financials, vote mechanics, agenda framing, and pre-cutoff AGM invitation, agenda, proxy, or voting materials where available before the May 22, 2019 meeting. | Use source-class label only. |
| S5 Official hive-down legal materials before vote | Retrieve source bytes, timestamp, hash, and basis for execution burden, asset-liability transfer, cost allocation, and validity conditions. | Use source-class label only. |
| S6 Official divisional business updates before cutoff | Retrieve source bytes, timestamp, hash, and basis for truck division economics and employee scale. | Use source-class label only. |
| S7 Independent business press before cutoff | Retrieve source bytes, timestamp, hash, and basis for capital-market and valuation-pressure framing. | Use only if title, URL, outlet cue, and outcome-adjacent phrasing can be withheld from participant view. |

## Owner or Source-Retrieval Dependencies

Required owner/source retrieval work:

- approve exact retrieval sources for S1-S7 or supply captures;
- approve formal S7 acquisition and evidence-registry registration, because the current participant packet seed already uses S7-class capital-market and valuation-pressure framing; any decision to remove S7 would require an explicit packet rewrite rather than a silent source-acquisition omission;
- decide where raw source bytes live if the repository should not store them directly;
- approve participant-safe source-class labels before packet conversion;
- confirm whether source retrieval should use public web retrieval, owner-supplied files, or both;
- confirm no target contestant has received Daimler packet text before probe authorization.

Decisions already accepted for this plan:

- Daimler proceeds as draft fixture-entry candidate;
- fixture folder is `docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/`;
- case ID is `daimler_corporate_structure_vote_2019_v0_14`;
- later target contestant families are GPT-5.5 primary and Claude Opus backup.

## Blocked and Non-Authorized Work

Blocked before probe execution:

- source acquisition and registry completion;
- packet conversion;
- participant-safe source-manifest review;
- evidence registry draft;
- facilitator ledger work queue;
- memorization probe request prep;
- owner authorization for probe execution.

Blocked before model runs:

- passing scoped memorization probe for each target contestant family;
- blind-use entry contract alignment;
- finalized participant packet hash;
- finalized prompt wrapper and prompt hash;
- unfrozen ledger checks showing no leakage issue.

Blocked before scoring:

- completed blind run;
- blind judgment output;
- facilitator ledger freeze;
- mapping table version pin;
- score protocol selection;
- leakage audit pass.

Not authorized in this pass:

- source retrieval;
- packet exposure to GPT-5.5, Claude Opus, or any other target contestant model;
- memorization probe execution;
- contestant model run;
- scoring;
- ledger freeze;
- schema, runtime, or code implementation;
- validation claim;
- product proof claim;
- fixture admission claim;
- judgment-quality claim;
- broad case discovery;
- importing Canoo/Walmart, Unity, Milwaukee, TR/Casetext, or jb rules as authority.

## Current Next Artifact

`source_acquisition_and_manifest_plan_v0.md` now exists in this fixture folder. Before source acquisition is authorized, resolve the S7 framing: current packet conversion assumes S7-class framing remains in scope, while source acquisition still needs formal S7 capture and evidence-registry registration.

The next planning artifact should be `participant_packet_conversion_plan_v0.md` or a direct `participant_packet_draft_v0.md`, depending on whether the owner wants one more review before packet conversion. Neither path authorizes source retrieval, probe execution, model runs, scoring, ledger freeze, schema/runtime implementation, validation, product proof, fixture admission, or judgment-quality claims.

## Closeout

plumbing works only; not judgment quality.
