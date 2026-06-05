# Source Capture Packet Fixture Retention Sensitivity Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product decision
scope: Decision record for Source Capture Packet lifecycle, durable citation, retention, and sensitivity handling before fixture admission.
use_when:
  - Deciding whether a generated Source Capture Packet is scratch-only, candidate evidence, recommended for fixture admission, or separately admitted.
  - Citing Source Capture Packet outputs from durable closeouts without promoting raw packet directories into fixtures.
  - Checking what sensitivity and retention notes must travel with raw source files, screenshots, media, account-visible, entitled, or client-provided packet artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/README.md
  - docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - orca-harness/docs/source_capture_packet.md
stale_if:
  - A later owner decision supersedes Source Capture Packet lifecycle, retention, sensitivity, or fixture-admission handling.
  - The Mini God-Tier profile materially changes packet lifecycle vocabulary.
  - Orca authorizes persistent packet storage, production runtime, broad crawler output retention, or fixture admission by a stronger governing source.
```

## Status And Decision

Status: `ACCEPTED_SOURCE_CAPTURE_PACKET_FIXTURE_RETENTION_SENSITIVITY_DECISION_V0`.

Owner-accepted decision: generated Source Capture Packets remain scratch by
default. A packet may be cited, retained, recommended for fixture admission, or
treated as separately admitted only under the lifecycle rules below.

This decision closes the current Source Capture Armory gap for generated packet
fixture, retention, and sensitivity handling. It does not admit any existing
packet as a fixture.

## Source Basis

- Current owner direction: define the narrow fixture/retention/sensitivity
  bridge before more source-quality work depends on scratch packet outputs.
- `docs/product/source_capture_toolbox/README.md`.
- `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`.
- `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`.
- `docs/review-outputs/adversarial-artifact-reviews/source_quality_slot3_post_recapture_closeout_adversarial_artifact_review_v0.md`.
- `orca-harness/docs/source_capture_packet.md`.
- `orca-harness/docs/source_capture_agent_runbook.md`.
- `.agents/workflow-overlay/source-of-truth.md`.

## Lifecycle Contract

The Mini God-Tier profile remains the vocabulary owner for source-quality packet
lifecycle states:

| Lifecycle state | Retention and citation meaning under this decision |
| --- | --- |
| `scratch` | Default state. Local or ignored packet output used for inspection only. It may be summarized by a durable closeout, but the raw packet directory itself is not fixture evidence and may be cleaned up. |
| `candidate_evidence` | A packet may be useful enough to retain or revisit, but fixture admission, rights, retention, sensitivity, and downstream use remain undecided. A candidate packet still cannot clear validation, source completeness, Judgment, buyer proof, or participant-packet gates. |
| `recommended_fixture_admission` | A report or closeout recommends that a separate admission decision be written. This is a recommendation only and must not be treated as `separately_admitted`. |
| `separately_admitted` | A separate fixture-admission or equivalent lifecycle decision exists and is cited in the report or queue row. If the cited decision cannot be found, do not use this state. |

`durable_operational_closeout` is not a packet lifecycle state. It is the role
of a human-authored closeout artifact that records packet paths, hashes, result
tokens, limitations, and non-claims from scratch or candidate packet work.

Expected cleanup or unavailability of ignored `_test_runs/` packet directories
does not by itself stale a durable closeout summary. It only prevents
reinspection beyond the recorded paths, hashes, body pointers, result tokens,
and limitations. A later durable contradiction, superseding closeout, or
admission decision can stale or replace the closeout.

## Retention Rule

Generated packet directories are not retained or committed by default.

Before a generated packet directory or raw packet content is durably retained
outside scratch, the retaining artifact or decision must state:

- packet path and packet or manifest hash when available;
- lifecycle state;
- reason for retention;
- source-access basis and capture mode;
- whether raw HTML, text, screenshots, images, media, archive bodies,
  account-visible material, entitled material, client-provided material,
  consenting-coworker/session-visible material, or machine-specific provenance
  paths are included;
- sensitivity and sharing note;
- allowed downstream use;
- forbidden claims and non-claims;
- whether a later fixture-admission decision is still required.

For `candidate_evidence`, the retention note preserves inspectability only. It
does not grant fixture admission or downstream evidentiary use.

For `recommended_fixture_admission`, the recommendation must name the packet and
why admission might be worth deciding, but it must not say admission is already
granted.

For `separately_admitted`, the report or queue row must cite the separate
admission decision. That decision, not this policy, owns the admitted use.

## Sensitivity Rule

Every durable citation or retention note for a generated packet must carry a
visible sensitivity note when the packet may contain any of:

- raw third-party source bodies;
- screenshots or page-render artifacts;
- source-linked media or gallery assets;
- account-created, paid, entitled, client-provided, or consenting-coworker
  visible material;
- archive snapshot bodies;
- personal names, handles, resumes, forum posts, reviews, or other user-authored
  material;
- machine-specific absolute paths, session labels, or local provenance pointers.

The sensitivity note is an operational handling record. It is not legal
sufficiency, rights clearance, privacy review, publication permission, or
commercial-use permission.

The packet must not preserve stolen credentials, cookies, raw browser profile
material, Playwright storage-state JSON, session sidecars, authorization
headers, secrets, or private/confidential spillover. If such material appears,
stop and treat the packet as contaminated scratch until a separate owner
decision says how to dispose, redact, or isolate it.

## Citation Rule

A future artifact may cite a Source Capture Packet only at the strength allowed
by its lifecycle state:

- `scratch`: cite only through a durable closeout summary or current local
  inspection; do not rely on raw packet permanence.
- `candidate_evidence`: cite as retained candidate context with limitations;
  do not use as admitted evidence.
- `recommended_fixture_admission`: cite as a recommendation to make a later
  admission decision; do not use as admission.
- `separately_admitted`: cite according to the separate admission decision and
  its stated allowed use.

Packet success, exit code `0`, a preserved body, a screenshot, or
`mini_god_tier_met` does not itself clear fixture admission, validation, source
completeness, participant-packet readiness, Judgment quality, buyer proof, or
legal sufficiency.

## What This Decision Closes

This decision closes the Source Capture Armory gap named as:

- no accepted fixture policy for generated packets;
- no rights, retention, or sensitivity rule for durably preserved raw source
  files, screenshots, media, entitled content, or paid-access artifacts.

It closes that gap only at the operating-policy level. It does not decide any
specific packet's admission, retention duration, legal rights, or publication
status.

## What Remains Separately Gated

The following still require separate owner authorization or a stronger
governing artifact:

- admission of any named packet as a fixture;
- production storage, database, dashboard, queue, scheduler, or crawler output
  retention;
- legal review, rights clearance, privacy review, or publication permission;
- participant-packet use;
- Judgment Spine evidence-tier promotion;
- buyer-proof or commercial-readiness use;
- API, commercial fetch, anti-detect, proxy, CAPTCHA, SERP, or production
  runtime expansion beyond already accepted boundaries.

## Non-Claims

This decision is not validation, readiness, source completeness proof, fixture
admission for any existing packet, legal sufficiency, rights clearance,
retention-duration policy, privacy review, source-access boundary amendment,
new adapter authorization, production storage authorization, ECR design,
Cleaning implementation, Judgment scoring, buyer proof, commercial-readiness
evidence, or source-of-truth promotion beyond this decision record.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Source Capture Packet lifecycle now has a bounded retention and sensitivity decision: generated packets remain scratch by default; durable closeouts may cite recorded packet facts without admitting fixtures; candidate, recommended-admission, and separately-admitted states require visible retention and sensitivity handling."
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - output_authority
  controlling_sources_updated:
    - "docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md"
    - "orca-harness/docs/source_capture_packet.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - "CLAUDE.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - ".agents/workflow-overlay/artifact-roles.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - ".agents/workflow-overlay/validation-gates.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md"
    - "orca-harness/docs/source_capture_packet.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
  intentionally_not_updated:
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "First-tranche source-access tooling build scope did not change; this decision governs output lifecycle handling only."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access permission, hard stops, disclosability, and entitlement rules did not change."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Candidate source-access methods and sequencing did not change."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden Capture outputs did not change; this decision governs generated packet lifecycle after capture tooling writes outputs."
    - path: "CLAUDE.md"
      reason: "Claude shim already delegates Orca project rules and doctrine-change propagation to AGENTS.md and the Orca overlay; no update was needed."
  stale_language_search: "rg -n \"fixture policy|retention policy|sensitivity rule|separately_admitted|recommended_fixture_admission|candidate_evidence|scratch packet|canonical fixtures|rights clearance|legal sufficiency|validated|ready|source completeness proof|Judgment scoring|buyer proof\" docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md docs/product/source_capture_toolbox/README.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md orca-harness/docs/source_capture_packet.md orca-harness/docs/source_capture_agent_runbook.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md CLAUDE.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not fixture admission for any existing packet"
    - "not legal sufficiency"
    - "not rights clearance"
    - "not production storage authorization"
    - "not ECR, Cleaning, or Judgment authority"
```
