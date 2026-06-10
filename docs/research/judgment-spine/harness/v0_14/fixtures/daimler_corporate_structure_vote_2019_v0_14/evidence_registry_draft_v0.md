# Daimler Evidence Registry Draft v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Draft facilitator-only EvidenceUnit registry for the Daimler corporate-structure vote v0.14 fixture candidate.
use_when:
  - Reviewing candidate EvidenceUnit fields before any Daimler fixture freeze.
  - Mapping Daimler S1-S7 source captures into v0.14 registry shape.
  - Checking source hash, retrieval timestamp, pre-decision basis, leakage note, and participant-safe label coverage before packet conversion.
authority_boundary: retrieval_only
input_hashes:
  source_acquisition_receipt_v0.md: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
  source_acquisition_and_manifest_plan_v0.md: D85D69F16308138AFB639DA3BD2229A43A13EE96653D9CF8B62E69122B8C5BDD
  fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  pydantic_schema_reference.md: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md: 47BBA3BE55627FDE39B347A24E20779005B633B2143ACEE51625AE21460B47B1
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_receipt_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
stale_if:
  - Owner requires canonical Mercedes-Benz Group bytes for S1 or S4A, or original Reuters/Investing bytes for S7, instead of the current source set.
  - Source IDs, source classes, case ID, cutoff, participant-safe source-manifest policy, or raw-byte storage policy change.
  - Any participant-facing artifact copies titles, URLs, filenames, outlet names, byte sizes, source hashes, retrieval timestamps, or 403 details from this facilitator-only registry.
```

- Status: EVIDENCE_REGISTRY_DRAFT_NOT_FROZEN
- Case ID: `daimler_corporate_structure_vote_2019_v0_14`
- Fixture status: not admitted
- Registry freeze hash: `NOT_COMPUTED`
- Source-byte hashes: captured for `DCSV-S1` through `DCSV-S7` from current live public web bytes and owner-supplied local PDF captures
- Retrieval timestamps: captured for current live public web bytes and normalized from owner-supplied local PDF file timestamps
- EvidenceUnit source shape: single-source draft units
- Participant visibility: facilitator internal only

## Registry Boundary

This registry maps captured Daimler source classes into draft v0.14 EvidenceUnit fields. It is not a frozen EvidenceUnit registry, not a participant packet, not a participant-facing source manifest, not a facilitator ledger, not a scoring input, not fixture admission, and not proof of judgment quality.

This file is facilitator-only. It may contain provenance, hashes, retrieval timestamps, local file paths, and leakage notes. Participant-facing material may use only source-class labels such as `S1 official issuer disclosure`; it must not copy titles, URLs, filenames, outlet names, byte sizes, source hashes, retrieval timestamps, optional-residue notes, or 403 details from this registry.

Because this registry is facilitator-only, `EvidenceUnit.source` carries the real source locator or local file path used for source-byte hashing. The participant packet conversion must not copy `EvidenceUnit.source`; participant-facing `source_manifest.source` values must be derived only from `participant_safe_label` and source-class labels.

The `bytes_available`, `leakage_check_status`, `participant_safe_label`, and `leakage_notes` fields are facilitator-only tracking fields outside the v0.14 EvidenceUnit schema. They must be stripped before any schema-validated or participant-facing use.

## Source Manifest Draft

| Source ID | Source role | Source date/status | Facilitator-only provenance | Participant-safe label | Hash status |
| --- | --- | --- | --- | --- | --- |
| DCSV-S1 | Initial rationale, feasibility state, employee context, and pension context | 2017-10 official issuer disclosure | `https://www.prnewswire.com/news-releases/daimler-board-of-management-decides-on-first-steps-to-strengthen-the-divisional-structure-300536970.html` | S1 official issuer disclosure | `3B2F49C6B4225B26B0E2F51E9ACEB19344F6D2CD5BAB400D562F0AB1910EA85A` |
| DCSV-S2 | Approval threshold and due-diligence scope | 2018-05 official investor presentation | `C:\Users\vmon7\Downloads\daimler-ir-corporatepresentation-may-2018.pdf` | S2 official investor presentation | `ECED20BD57F7162FD94E0D0D5E75E5C91574624F349F89D0A3D616A6C4FCDCCF` |
| DCSV-S3 | Proposal mechanics, entity model, cost burden, employee commitments, and timing | 2018-07 official corporate-structure release | `https://www.daimlertruck.com/en/newsroom/pressrelease/consistent-continuation-of-strategy-daimler-lines-up-for-the-future-40772994` | S3 official corporate-structure release | `7DD023357E42D5428F646E978A057A55FAA499EBBE466942ACD4A990D6AA2383` |
| DCSV-S4A | Group financials, annual reporting context, and divisional performance context | 2018 annual reporting material | `https://www.annualreports.com/HostedData/AnnualReportArchive/d/NYSE_DAI_2018.pdf` | S4 official annual and meeting materials | `A6A8A534AA6F91BAA131A96E9C674892FA61F782E1C0D99D52F197830D481D6A` |
| DCSV-S4B | Pre-vote annual-meeting agenda and governance framing | 2019 pre-vote annual-meeting material | `C:\Users\vmon7\Downloads\daimler-ir-am-agenda-2019.pdf` | S4 official annual and meeting materials | `AD2DD0669EBE1DBB5BFD7BA725FF811206F11F8E7EE49B87F623D27FD4C5A843` |
| DCSV-S5 | Hive-down legal mechanics, transfer categories, cost allocation, and validity conditions | 2019 pre-vote legal material | `C:\Users\vmon7\Downloads\daimler-ir-am-hivedownreport-2019.pdf` | S5 official hive-down legal materials | `E8D1C83D829A6926AF75D0C1EF122110F56631795770244F3E4B10F63FE52A55` |
| DCSV-S6 | Truck division economics and employee scale | 2018-06-06 official divisional business update | `C:\Users\vmon7\Downloads\daimler-ir-cmddtstrategydaum-20180606.pdf` | S6 official divisional business updates | `BFC5122922BF2755D81BE46B1B58AFDA5E1622C598D07E7544B5E02B56069895` |
| DCSV-S7 | Capital-market and valuation-pressure framing | 2018-07-30 independent pre-cutoff business press mirror | `https://autto.at/en/news/daimler-split-business-cars-trucks-mobility-units-20180730.html` | S7 independent pre-cutoff business press | `58E9A350C8B5B6AF58122812BBCF72431DEB120B85B0BB5AC9BDDADC2E3727B7` |

## Source Acquisition Status

```yaml
source_acquisition_receipt: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_receipt_v0.md
source_acquisition_receipt_hash: 9827EC9408CE97FF69DF9451829492431A9C0DDE4E0A54F6FF4107D6882EEBF8
source_hash_timestamp_gate: complete_for_current_source_set
capture_scope: current_live_public_web_bytes_and_owner_supplied_local_pdf_bytes_not_historical_archive
captured_source_ids:
  - DCSV-S1
  - DCSV-S2
  - DCSV-S3
  - DCSV-S4A
  - DCSV-S4B
  - DCSV-S5
  - DCSV-S6
  - DCSV-S7
blocked_source_ids: []
optional_canonical_residue:
  - DCSV-S1-CANONICAL
  - DCSV-S4A-CANONICAL
  - DCSV-S7-ORIGINAL
raw_bytes_retained_in_repo: false
participant_visibility: facilitator_internal_only
non_claim: Source acquisition does not freeze the registry, prove participant readiness, authorize blind use, or prove judgment quality.
```

## Draft Evidence Units

```yaml
evidence_units:
  - evidence_id: DCSV-E01
    source_id: DCSV-S1
    source_type: official_issuer_disclosure
    source: 'https://www.prnewswire.com/news-releases/daimler-board-of-management-decides-on-first-steps-to-strengthen-the-divisional-structure-300536970.html'
    timestamp: 2017-10
    retrieval_timestamp: 2026-05-30T16:20:46Z
    hash: 3B2F49C6B4225B26B0E2F51E9ACEB19344F6D2CD5BAB400D562F0AB1910EA85A
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is an October 2017 official issuer disclosure, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S1 official issuer disclosure
    leakage_notes: Facilitator provenance includes raw locator and distribution details; participant-facing material must use only the S1 label.
    summary: >
      The restructuring rationale existed before the final vote window: management framed divisional
      strengthening as a way to increase entrepreneurial responsibility, accountability, speed,
      partnership flexibility, and capital-market optionality while preserving group-level control
      and selected synergies. This supports structural-need framing, not approval by itself.

  - evidence_id: DCSV-E02
    source_id: DCSV-S2
    source_type: official_investor_material
    source: 'C:\Users\vmon7\Downloads\daimler-ir-corporatepresentation-may-2018.pdf'
    timestamp: 2018-05
    retrieval_timestamp: 2026-05-30T16:40:53.5951509Z
    hash: ECED20BD57F7162FD94E0D0D5E75E5C91574624F349F89D0A3D616A6C4FCDCCF
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is a May 2018 official investor presentation, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S2 official investor presentation
    leakage_notes: Local filename and source identity are facilitator-only; participant-facing material must use only the S2 label.
    summary: >
      The due-diligence problem was broader than brand architecture. The approval question implicated
      legal entity separation, governance, financing, transferred assets and liabilities, employee
      representation, and transaction feasibility. This supports a guardrail-oriented approval
      threshold rather than treating the vote as a simple endorsement of focus.

  - evidence_id: DCSV-E03
    source_id: DCSV-S3
    source_type: official_corporate_structure_release
    source: 'https://www.daimlertruck.com/en/newsroom/pressrelease/consistent-continuation-of-strategy-daimler-lines-up-for-the-future-40772994'
    timestamp: 2018-07
    retrieval_timestamp: 2026-05-30T16:19:30Z
    hash: 7DD023357E42D5428F646E978A057A55FAA499EBBE466942ACD4A990D6AA2383
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is a July 2018 official corporate-structure release, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S3 official corporate-structure release
    leakage_notes: Facilitator provenance includes raw locator and corporate source identity; participant-facing material must use only the S3 label.
    summary: >
      The proposed model separated Cars and Vans, Trucks and Buses, and financial-services or mobility
      activity into major legally independent operating entities under the parent company. This supports
      the participant packet's entity-model and mechanics facts, but it does not settle whether legal
      separation is superior to internal accountability changes.

  - evidence_id: DCSV-E04
    source_id: DCSV-S3
    source_type: official_corporate_structure_release
    source: 'https://www.daimlertruck.com/en/newsroom/pressrelease/consistent-continuation-of-strategy-daimler-lines-up-for-the-future-40772994'
    timestamp: 2018-07
    retrieval_timestamp: 2026-05-30T16:19:30Z
    hash: 7DD023357E42D5428F646E978A057A55FAA499EBBE466942ACD4A990D6AA2383
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is a July 2018 official corporate-structure release, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S3 official corporate-structure release
    leakage_notes: Cost, timing, and employee-commitment facts must remain pre-cutoff and must not be mixed with later implementation status.
    summary: >
      The official proposal carried meaningful cost, timing, and stakeholder commitments: one-time
      costs, later running costs, employee safeguards, pension-related measures, profit-sharing
      continuity, and German investment commitments. This supports both stabilizer and hidden-cost
      interpretations.

  - evidence_id: DCSV-E05A
    source_id: DCSV-S4A
    source_type: official_annual_reporting_material
    source: 'https://www.annualreports.com/HostedData/AnnualReportArchive/d/NYSE_DAI_2018.pdf'
    timestamp: 2018
    retrieval_timestamp: 2026-05-30T16:24:05Z
    hash: A6A8A534AA6F91BAA131A96E9C674892FA61F782E1C0D99D52F197830D481D6A
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is 2018 official annual reporting material, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S4 official annual and meeting materials
    leakage_notes: Annual-report mirror provenance is facilitator-only; participant-facing material must not expose the raw locator or hash.
    summary: >
      Daimler was a very large global automotive group entering the vote with about EUR167.4 billion
      of revenue, about EUR11.1 billion of EBIT, about EUR7.6 billion of net profit, about 298,700
      employees, and about EUR9.1 billion of research and development expenditure in 2018. This
      supports materiality and transition-burden context.

  - evidence_id: DCSV-E05B
    source_id: DCSV-S4A
    source_type: official_annual_reporting_material
    source: 'https://www.annualreports.com/HostedData/AnnualReportArchive/d/NYSE_DAI_2018.pdf'
    timestamp: 2018
    retrieval_timestamp: 2026-05-30T16:24:05Z
    hash: A6A8A534AA6F91BAA131A96E9C674892FA61F782E1C0D99D52F197830D481D6A
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is 2018 official annual reporting material, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S4 official annual and meeting materials
    leakage_notes: Divisional performance facts must remain pre-cutoff and must not be updated with later corporate actions or outcomes.
    summary: >
      The operating divisions differed materially: Cars produced the largest EBIT but declined from
      the prior year, Vans had record unit sales but sharply lower EBIT, Buses remained positive but
      slightly lower, and financial services and mobility had a large contract-volume role with lower
      EBIT. This supports the case for different divisional economics and investment cycles.

  - evidence_id: DCSV-E06
    source_id: DCSV-S4B
    source_type: official_governance_material
    source: 'C:\Users\vmon7\Downloads\daimler-ir-am-agenda-2019.pdf'
    timestamp: 2019_pre_vote
    retrieval_timestamp: 2026-05-30T16:40:59.4868089Z
    hash: AD2DD0669EBE1DBB5BFD7BA725FF811206F11F8E7EE49B87F623D27FD4C5A843
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is the 2019 official annual-meeting agenda published before the May 22, 2019 meeting, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S4 official annual and meeting materials
    leakage_notes: Local filename and meeting-material identity are facilitator-only; participant-facing material must not expose agenda titles, file names, URLs, or vote-result context.
    summary: >
      The annual-meeting material supports that the decision was a governance approval question before
      the May 22, 2019 meeting, not merely management communication. It grounds the vote mechanics and
      agenda framing without revealing the final shareholder result.

  - evidence_id: DCSV-E07
    source_id: DCSV-S5
    source_type: official_legal_governance_material
    source: 'C:\Users\vmon7\Downloads\daimler-ir-am-hivedownreport-2019.pdf'
    timestamp: 2019_pre_vote
    retrieval_timestamp: 2026-05-30T16:41:03.3973838Z
    hash: E8D1C83D829A6926AF75D0C1EF122110F56631795770244F3E4B10F63FE52A55
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Safety receipt classifies the hive-down legal materials as published before the vote and before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S5 official hive-down legal materials
    leakage_notes: Legal document title, filename, and locator are facilitator-only; participant-facing material must summarize execution burden without exposing source identity.
    summary: >
      The legal hive-down work involved asset and liability transfer mechanics, mixed-use contracts,
      treasury arrangements, customer and dealer agreements, IP and software allocation, public-law
      authorizations, employee transfers, supervisory-board composition, and withdrawal conditions.
      This supports high execution burden and the need for guardrails.

  - evidence_id: DCSV-E08
    source_id: DCSV-S6
    source_type: official_business_update
    source: 'C:\Users\vmon7\Downloads\daimler-ir-cmddtstrategydaum-20180606.pdf'
    timestamp: 2018-06-06
    retrieval_timestamp: 2026-05-30T16:41:06.8947056Z
    hash: BFC5122922BF2755D81BE46B1B58AFDA5E1622C598D07E7544B5E02B56069895
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source class is a June 6, 2018 official divisional business update, before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S6 official divisional business updates
    leakage_notes: Local filename and source identity are facilitator-only; participant-facing material must not reveal source title or locator.
    summary: >
      The truck business had distinct scale and economics, including about EUR38.3 billion of revenue,
      about EUR2.8 billion of EBIT, about 517,300 unit sales excluding the BFDA joint venture count,
      and about 83,000 employees at year-end 2018. This supports the claim that at least one major
      operating division had separable business characteristics.

  - evidence_id: DCSV-E09
    source_id: DCSV-S7
    source_type: independent_business_press
    source: 'https://autto.at/en/news/daimler-split-business-cars-trucks-mobility-units-20180730.html'
    timestamp: 2018-07-30
    retrieval_timestamp: 2026-05-30T16:21:31Z
    hash: 58E9A350C8B5B6AF58122812BBCF72431DEB120B85B0BB5AC9BDDADC2E3727B7
    bytes_available: true
    pre_decision_status: verified_pre_decision
    pre_decision_basis: Source acquisition receipt records an independent business-press mirror before the May 21, 2019 decision cutoff.
    leakage_check_status: pending_review
    participant_safe_label: S7 independent pre-cutoff business press
    leakage_notes: Outlet cue, article title, URL, and original-wire-source residue are facilitator-only; participant-facing material may use only capital-market and valuation-pressure framing.
    summary: >
      Independent pre-cutoff commentary treated clearer separation as potentially useful for valuation
      clarity and strategic optionality, especially for divisions with different economics and investment
      cycles. The same logic remains two-sided: separation could also destroy synergies, raise fixed
      cost, or create coordination drag.
```

## Excluded Or Unresolved Source Material

```yaml
excluded_or_unresolved_sources:
  - source_id: DCSV-S1-CANONICAL
    status: optional_canonical_residue
    reason: Canonical Mercedes-Benz Group endpoint returned HTTP 403 to programmatic retrieval; DCSV-S1 official PRNewswire distribution is used for the current source set unless owner requires canonical issuer-domain bytes.
  - source_id: DCSV-S3-ALT
    status: optional_alternate_distribution_not_used
    reason: Source acquisition receipt captured a PRNewswire alternate distribution for the same pre-cutoff official corporate-structure release; DCSV-S3 official Daimler Truck page remains the current registry source unless owner changes the preferred S3 distribution.
  - source_id: DCSV-S4A-CANONICAL
    status: optional_canonical_residue
    reason: AnnualReports mirror of the official 2018 annual report is used for the current source set unless owner requires issuer-domain annual-report bytes.
  - source_id: DCSV-S7-ORIGINAL
    status: optional_original_residue
    reason: Original Reuters/Investing page returned HTTP 403 to programmatic retrieval; accessible independent business-press mirror is used for the current source set unless owner requires original page bytes.
unresolved_fields:
  - registry freeze hash
  - facilitator ledger mapping and any later ledger freeze hash
  - participant packet conversion source-manifest mapping
  - memorization probe request and result status
  - blind judgement adapter linkage
  - any future scoring-result evidence ID checks
```

## Non-Claims

- No frozen EvidenceUnit registry.
- No participant-packet readiness.
- No participant-safe source manifest.
- No historical archive source-byte proof.
- No raw-byte repository archive.
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
