# Daimler Source Acquisition and Manifest Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Pre-retrieval source acquisition and source-manifest plan for the Daimler corporate-structure vote v0.14 draft fixture pack.
use_when:
  - Planning S1-S7 source retrieval before any Daimler v0.14 evidence registry or participant packet conversion.
  - Checking which source-byte hash, retrieval timestamp, and pre-decision metadata fields must be captured.
  - Preserving the split between participant-safe source labels and facilitator-only provenance.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md: E60B496101E154401EA9D6E0E5C2EC58701A7EF1E1FBEC4C01A9C5E392D0347F
  docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md: 4DCFEF6800A0AF85F5FA26534C4E863174007737B9FB02B1B3B3D78C96F31BFE
stale_if:
  - owner changes the S1-S7 source class set, decision cutoff, case ID, or fixture folder.
  - source acquisition is authorized and actual source captures produce different source classes or leakage constraints.
  - participant-facing source manifest policy changes to allow source titles, URLs, hashes, or retrieval timestamps.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: true
  overlay_read: true
  source_pack: custom_daimler_fixture_entry_plan_plus_case_seed
  artifact_role: Research artifact
  edit_permission: docs-write
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md
  dirty_state_checked: true
  blocked_if_missing: false
```

## Spec Fast Exit

```yaml
spec_status: SPEC_NOT_NEEDED_READY_FOR_SCOPING
implicit_contract: Write one pre-retrieval source acquisition and manifest plan for S1-S7; do not retrieve sources, expose participant packet text to target models, run probes, run models, score, freeze ledgers, implement schema or runtime, or claim readiness.
```

## Current State

```yaml
case_id: daimler_corporate_structure_vote_2019_v0_14
fixture_folder: docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/
source_plan_status: pre_retrieval
fixture_status: not_admitted
blind_use_status: blocked
no_probe_run: true
no_model_run: true
no_scoring_run: true
ledger_freeze_status: not_frozen
schema_or_runtime_status: not_implemented
judgment_quality_status: not_claimed
```

Daimler has a participant packet seed and safety receipt, but S1-S7 are still source classes rather than captured source records. This plan defines what must be acquired later and how the participant-safe manifest must remain separated from facilitator-only provenance.

## Acquisition Contract

Each source capture later needs:

- `source_id`: stable fixture-local identifier.
- `source_class`: one of S1-S7.
- `retrieval_owner`: owner, operator, or source-retrieval lane assigned later.
- `retrieval_method`: public retrieval, owner-supplied capture, or other owner-approved method.
- `retrieval_timestamp`: ISO 8601 timestamp with timezone.
- `source_timestamp`: publication or document timestamp when available.
- `source_type`: official issuer disclosure, official investor material, official legal/governance material, official business update, or independent business press.
- `raw_bytes_location`: storage pointer or explicit no-store decision.
- `source_byte_hash`: `sha256(source_bytes)` when bytes are available.
- `bytes_available`: true only after raw bytes are captured or owner supplies a verifiable byte artifact.
- `pre_decision_status`: pre-cutoff, rejected_post_cutoff, or unresolved.
- `pre_decision_basis`: short facilitator-only reason the source is before the cutoff.
- `participant_safe_label`: source-class label allowed in participant-facing packet material.
- `facilitator_only_provenance`: source title, URL, file name, capture path, or other identifying metadata.
- `leakage_notes`: title, URL, snippet, outlet cue, post-cutoff, consulting-narrative, or outcome-risk notes.

No field above is complete in this plan. All capture rows remain pending until source acquisition is separately authorized and performed.

## Post-Review Patch Note

This version incorporates the review-use findings from `docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_fixture_entry_source_manifest_adversarial_artifact_review_v0.md`. The review remains decision input only; this note is not approval, validation, fixture admission, blind-use readiness, mandatory remediation, or judgment-quality proof.

S7 framing is now explicit: the current participant packet seed already uses S7-class capital-market and valuation-pressure framing. The remaining owner/source-retrieval decision is whether and how to formally acquire and register S7 sources in the facilitator-only evidence registry. Removing S7 from the fixture path would require an explicit participant-packet rewrite, not a silent omission during source acquisition.

## S1-S7 Work Queue

| Source ID | Source class | Required capture | Participant-safe label | Current status | Stop condition |
| --- | --- | --- | --- | --- | --- |
| DCSV-S1 | Official issuer disclosure from October 2017 | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for initial rationale, feasibility state, employee context, and pension context. | S1 official issuer disclosure | pending_retrieval | Stop if only post-cutoff or outcome-revealing copies are available. |
| DCSV-S2 | Official investor presentation from May 2018 | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for approval threshold and due-diligence scope. | S2 official investor presentation | pending_retrieval | Stop if the capture leaks final approval, later implementation, or post-cutoff framing. |
| DCSV-S3 | Official corporate-structure release from July 2018 | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for proposal mechanics, entity model, cost burden, employee commitments, and timing. | S3 official corporate-structure release | pending_retrieval | Stop if the source identity cannot be withheld safely from participant view. |
| DCSV-S4 | Official 2018 annual reporting and pre-vote annual-meeting materials | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for group financials, vote mechanics, agenda framing, and pre-cutoff AGM invitation, agenda, proxy, or voting materials where available before the May 22, 2019 meeting. | S4 official annual and meeting materials | pending_retrieval | Stop if meeting material includes final vote result or later meeting outcome in the same participant-facing capture. |
| DCSV-S5 | Official hive-down legal materials before vote | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for execution burden, asset and liability transfer, cost allocation, and validity conditions. | S5 official hive-down legal materials | pending_retrieval | Stop if the legal material is only available in a later amended or outcome-revealing version. |
| DCSV-S6 | Official divisional business updates before cutoff | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for truck division economics and employee scale. | S6 official divisional business updates | pending_retrieval | Stop if the update is post-cutoff or tied to later performance/outcome interpretation. |
| DCSV-S7 | Independent business press before cutoff | Capture bytes, retrieval timestamp, source timestamp, hash, and pre-decision basis for capital-market and valuation-pressure framing. | S7 independent pre-cutoff business press | pending_retrieval | Stop if source title, URL, outlet cue, snippet, or article framing leaks the final decision, outcome, or later implementation. |

## Manifest Split

Participant-facing source manifest:

- may use only `S1` through `S7` and short source-class labels;
- may describe why each class matters at a high level;
- must not include source titles, URLs, filenames, hashes, retrieval timestamps, outlet names, consulting-firm narrative, final vote results, later implementation, later company actions, or outcome metrics.

Facilitator-only evidence registry:

- must contain full source provenance once acquisition is authorized;
- must contain `retrieval_timestamp` and `source_byte_hash` for each captured byte artifact;
- may contain titles, URLs, storage paths, and source notes when needed for audit;
- must keep leakage notes visible to facilitators and absent from participant-facing material.

## Source-Byte Storage Policy

```yaml
source_byte_storage_status: owner_decision_required
allowed_policy_options:
  repo_tracked_capture:
    use_only_if: owner explicitly approves storing raw source bytes in the repository.
  repo_pointer_external_bytes:
    use_only_if: owner prefers external storage while preserving stable hash and retrieval timestamp in the evidence registry.
  owner_supplied_capture:
    use_only_if: owner supplies byte artifacts and capture timestamps.
blocked_policy:
  - Do not store raw source bytes in this fixture folder by default.
  - Do not create source-byte captures during this plan.
  - Do not substitute search-result snippets for source bytes.
```

Recommended default: use facilitator-only evidence registry rows with source-byte hashes and retrieval timestamps, while deferring raw-byte storage location to owner/source-retrieval authorization.

## Evidence Registry Row Template

```yaml
evidence_unit_template:
  evidence_id: DCSV-EU-<S1-S7>-<nn>
  source_id: DCSV-S<1-7>
  source_class: S<1-7>
  source_type: pending_retrieval
  source: facilitator_only_pending
  source_timestamp: pending_retrieval
  retrieval_timestamp: pending_retrieval
  hash: pending_source_bytes
  bytes_available: false
  pre_decision_status: unresolved_until_retrieval
  pre_decision_basis: pending_retrieval
  leakage_check_status: pending_review
  summary: pending_retrieval
  participant_safe_label: pending_from_source_class
  leakage_notes: pending_facilitator_review
```

Do not fill this template from memory, search snippets, titles, URLs, or post-cutoff summaries. Use it only after authorized source acquisition produces a source capture.

## Retrieval Authorization Gates

Before retrieval starts, the owner/source-retrieval lane must decide:

- exact retrieval method for each S1-S7 source class;
- whether and how to formally acquire and register S7 in the facilitator-only evidence registry, because the current packet seed already uses S7-class framing; if S7 is not acquired, the packet seed must be explicitly rewritten before conversion;
- where raw source bytes live;
- whether source-byte hashes can be recorded in a facilitator-only evidence registry without storing bytes in this repository;
- who may see facilitator-only provenance before participant packet conversion;
- whether any target contestant has already seen Daimler participant packet text.

## Blocked and Non-Authorized Work

This plan does not authorize:

- source retrieval;
- web search or source download;
- raw source-byte capture;
- participant packet conversion;
- evidence registry completion;
- packet exposure to GPT-5.5, Claude Opus, or any other target contestant model;
- memorization probe execution;
- contestant model run;
- scoring;
- facilitator ledger freeze;
- schema, runtime, or code implementation;
- validation claim;
- product proof claim;
- fixture admission claim;
- blind-use readiness claim;
- judgment-quality claim;
- broad case discovery;
- importing Canoo/Walmart, Unity, Milwaukee, TR/Casetext, or jb rules as authority.

## Next Artifact After This Plan

After source acquisition is separately authorized and completed, create `evidence_registry_draft_v0.md` in this fixture folder. It should fill source provenance and evidence-unit fields from captured sources, not from this planning document.

If the owner wants one more zero-spoiler check before retrieval, create a short retrieval prompt or checklist that names S1-S7 classes and the forbidden participant-facing leakage fields, without naming titles or URLs.

## Closeout

plumbing works only; not judgment quality.
