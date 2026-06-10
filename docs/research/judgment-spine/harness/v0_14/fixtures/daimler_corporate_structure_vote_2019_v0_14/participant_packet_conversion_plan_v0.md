# Daimler Participant Packet Conversion Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Docs-only conversion contract for turning the Daimler parent participant packet into a v0.14 participant packet draft without exposing facilitator-only source provenance.
use_when:
  - Preparing Daimler participant_packet_draft_v0.md after source/evidence plumbing recheck.
  - Checking the participant-safe source_manifest mapping before packet conversion execution.
  - Verifying that participant packet conversion remains blocked from blind use, probe execution, scoring, fixture admission, and judgment-quality claims.
authority_boundary: retrieval_only
input_hashes:
  fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  source_acquisition_and_manifest_plan_v0.md: D85D69F16308138AFB639DA3BD2229A43A13EE96653D9CF8B62E69122B8C5BDD
  source_acquisition_receipt_v0.md: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
  evidence_registry_draft_v0.md: 2E9FC02E7D19AA21DC9C66E9DF740D53A6798365D70EB76A2D3F213F2DD2FBA5
  post_patch_adversarial_recheck_v0.md: 5E43E7E26BD37AA7270A019A60BD5F600ED53C75367611EA7F44B886AE605F34
  docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  pydantic_schema_reference.md: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_manifest_participant_safe_adapter_decision_v0.md: 39E92DB6C9D86C1BB18857069CF0507065C4460A15B3293359611875B3DB2E32
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md: 059EE78287C0F667DD75568F3179EE8424D2FFCD42CCC2882C177F5A7C9C2FD6
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_participant_packet_conversion_plan_adversarial_artifact_review_v0.md: 22A4360B444E9C65CF141C3D55BACAF09FD90581069AB3B1736DB58CE17A3A35
open_next:
  - docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/evidence_registry_draft_v0.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
downstream_consumers:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md
stale_if:
  - Any input hash changes.
  - The participant-safe source-manifest policy changes.
  - The v0.14 participant packet frontmatter schema changes.
  - Owner requires canonical source bytes instead of the current S1-S7 source set.
  - A participant-facing artifact copies facilitator-only locators, filenames, hashes, retrieval timestamps, byte sizes, outlet names, optional residue, 403 details, source titles, post-cutoff facts, final vote result, implementation status, or later outcomes.
```

- Status: PARTICIPANT_PACKET_CONVERSION_PLAN_NOT_PACKET_DRAFT
- Case ID: `daimler_corporate_structure_vote_2019_v0_14`
- Conversion target: `participant_packet_draft_v0.md`
- Participant packet draft status: not created by this plan
- Source-manifest mapping status: specified for conversion planning
- Blind-use status: blocked
- Fixture status: not admitted
- Judgment-quality status: not claimed

## Spec Status

```yaml
spec_status: SPEC_COMPLETE_READY_FOR_SCOPING
authorization_status: conversion_execution_requires_owner_acceptance_after_this_plan
input_basis: owner accepted post-patch evidence-registry recheck and authorized next docs-only step
required_behavior: >
  Convert the existing Daimler participant packet into v0.14 frontmatter shape
  while preserving its zero-spoiler body and using only participant-safe
  source-class labels in the source_manifest.
non_goals:
  - Do not author participant_packet_draft_v0.md in this artifact.
  - Do not expose facilitator-only source provenance to participant view.
  - Do not run a memorization probe, contestant model, scoring, validation, or ledger freeze.
  - Do not claim fixture admission, blind-use readiness, participant-packet readiness, product proof, or judgment quality.
interfaces_contracts:
  - v0.14 participant packet frontmatter fields from pydantic_schema_reference.md.
  - Daimler source_manifest rows defined in this plan.
  - Existing parent participant packet body, with only shape/heading normalization allowed during draft conversion.
acceptance_criteria:
  - Every S1-S7 participant-safe source label is mapped exactly once.
  - Participant-facing retrieval_timestamp and hash values are withheld placeholders before seal.
  - No raw source locator, title, filename, outlet cue, byte size, source-byte hash, retrieval timestamp, optional-residue note, or 403 detail appears in participant-facing packet material.
  - The resulting draft remains pre-cutoff and excludes final vote result, later implementation, later corporate actions, later outcomes, consulting narrative, and result-quality labels.
deferred_open_questions: []
scoping_may_rely_on: >
  Packet conversion may be scoped from this plan without inventing the participant-safe
  source_manifest mapping or v0.14 frontmatter intent.
```

## Conversion Boundary

This plan defines what a later packet-conversion pass must create. It is not the converted packet, not a participant-facing artifact, not a review report, not a facilitator ledger, not a probe request, not a scoring input, and not fixture admission.

The packet converter must use the parent participant packet as the body source and the evidence registry only for participant-safe labels. The converter must not copy `EvidenceUnit.source`, facilitator-only provenance, source hashes, retrieval timestamps, byte sizes, local file names, raw source locators, optional canonical residue, or 403 retrieval details into the participant-facing packet.

## Required v0.14 Frontmatter Values

The later `participant_packet_draft_v0.md` must start with YAML frontmatter using this intent:

```yaml
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
```

## Source Manifest Mapping Contract

| Evidence registry source ID | Participant `source_id` | Participant `source` | Participant retrieval timestamp | Participant hash | Rule |
| --- | --- | --- | --- | --- | --- |
| DCSV-S1 | DCSV-S1 | S1 official issuer disclosure | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use label only. |
| DCSV-S2 | DCSV-S2 | S2 official investor presentation | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use label only. |
| DCSV-S3 | DCSV-S3 | S3 official corporate-structure release | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use current DCSV-S3 label; do not expose DCSV-S3-ALT. |
| DCSV-S4A | DCSV-S4A | S4 official annual and meeting materials | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use same S4 participant-safe label as DCSV-S4B. |
| DCSV-S4B | DCSV-S4B | S4 official annual and meeting materials | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use same S4 participant-safe label as DCSV-S4A. |
| DCSV-S5 | DCSV-S5 | S5 official hive-down legal materials | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use label only. |
| DCSV-S6 | DCSV-S6 | S6 official divisional business updates | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Use label only. |
| DCSV-S7 | DCSV-S7 | S7 independent pre-cutoff business press | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL` | Include for the current parent packet. The safety receipt classifies S7 clean when source titles and URLs remain excluded. |

The repeated S4 label is intentional. The participant may know that annual and meeting materials support the packet, but must not see the separate facilitator provenance for the annual report versus annual-meeting agenda.

The manifest table maps source IDs, not EvidenceUnit count. Multiple EvidenceUnits may share one `source_id`; for example, DCSV-E03 and DCSV-E04 both map to the single DCSV-S3 manifest row, and DCSV-E05A and DCSV-E05B both map to the single DCSV-S4A manifest row. The table above is the authoritative participant-facing source-manifest mapping.

S7 inclusion is mandatory for the current parent packet because the packet already uses S7-class capital-market and valuation-pressure framing. Removing S7 requires an explicit packet rewrite that removes that framing; it must not happen silently during conversion. "Original-wire residue" means facilitator-only source-origin cues such as original Reuters/Investing lineage, mirror provenance, outlet cues, titles, raw locators, or source-origin notes. It is not packet body content in the current parent packet, and the safety receipt already treats S7 as clean when titles and URLs remain excluded.

## Packet Body Conversion Rules

The later draft must preserve the parent packet's zero-spoiler body and may normalize only to fit v0.14 packet shape:

- keep the role frame, decision cutoff, decision question, proposal snapshot, company and market context, division snapshot, execution burden, stakeholder constraints, judgment questions, red-team prompts, required blind judgment output, known unknowns, and non-claims;
- keep the instruction not to search for the case or later developments before answering;
- do not add source titles, source URLs, source filenames, outlet names, source hashes, retrieval timestamps, source-byte sizes, 403 notes, canonical-source residue, final vote result, implementation status, later actions, later outcomes, consulting narrative, or result-quality labels;
- do not derive new participant-facing facts from facilitator-only summaries unless they already appear in the parent participant packet or are needed only as non-substantive v0.14 frontmatter normalization;
- do not add evidence IDs to the participant-facing body except through the safe `source_manifest` rows above.

## Draft Acceptance Checks

Before any later `participant_packet_draft_v0.md` is treated as conversion-complete, run these checks and record the evidence in that artifact or a paired receipt:

1. Confirm the draft starts with v0.14 YAML frontmatter containing every required field from the Pydantic schema reference.
2. Confirm the `source_manifest` rows match this plan exactly.
3. Confirm every `retrieval_timestamp` and `hash` shown to the participant is `WITHHELD_OR_PLACEHOLDER_BEFORE_SEAL`.
4. Confirm the draft contains no raw source locators, local filenames, source titles, outlet names, source-byte hashes, true retrieval timestamps, byte sizes, optional-residue notes, or 403 details.
5. Confirm the draft contains no final vote result, later implementation status, later corporate actions, later outcome metrics, consulting narrative, or result-quality labels.
6. Confirm the draft does not claim participant-packet readiness, blind-use readiness, probe pass, score readiness, validation, fixture admission, product proof, or judgment quality.

Passing these checks would support only "participant packet draft converted according to the plan." It would not prove blind-use readiness, fixture admission, validation, product proof, or judgment quality.

## Open Questions

None for packet conversion planning. Owner may still later choose to require canonical S1, S4A, or S7 source bytes, but that would stale the source receipt and evidence registry rather than change the participant-safe mapping contract.

## Next Gate

After owner acceptance of this plan, the next docs-only artifact may be `participant_packet_draft_v0.md`. That later artifact should not proceed to blind use until a separate review checks the converted packet, source-manifest boundary, and no-spoiler surface.

## Non-Claims

- No participant packet draft was created by this plan.
- No participant-packet readiness.
- No blind-use readiness.
- No memorization-probe pass.
- No model run.
- No scoring readiness.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No fixture validation.
- No fixture admission.
- No product proof.
- No judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
