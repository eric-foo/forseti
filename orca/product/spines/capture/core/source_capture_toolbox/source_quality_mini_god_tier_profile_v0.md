# Source Quality Mini God-Tier Profile v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Reusable source-quality operating profile for deciding the smallest complete source-capture posture future agents should target per source unit.
use_when:
  - Planning or running bounded source-quality improvement passes after the Source Capture Armory has a concrete source locator.
  - Distinguishing source-capture completeness from fixture admission, Judgment scoring, ECR, Cleaning, or source discovery.
  - Preparing a source-unit queue before applying Source Capture Armory runners.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/README.md
  - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - The Source Capture Armory packet shape, runner set, or output lifecycle materially changes.
  - The Data Capture obligation contract changes capture obligations, forbidden outputs, or handoff states.
  - The Source Capture Packet fixture, retention, or sensitivity decision is amended or superseded.
```

## Status

Status: `SOURCE_QUALITY_MINI_GOD_TIER_PROFILE_V0`.

This profile defines the smallest complete source-quality target for one source
unit or a bounded source set. It exists to make future source captures repeatable
without turning every source into a bespoke closeout or full fixture-admission
exercise.

Mini god-tier is stronger than "a packet was written" and weaker than full
formal evidence admission. It means the source unit has the best in-bound body
posture currently available, enough provenance to inspect identity, bounded
source-language anchors, a coverage or drift note, visible limitations, and an
explicit lifecycle state.

## Commissioning Boundary

This profile assumes a source unit is already bounded by an owner, operator,
case, slot, source packet, or other accepted source context. That bounded source
context does not by itself satisfy the Data Capture Commissioning Gate or create
a Decision Frame.

If a source-quality pass lacks the decision question, cutoff posture, operator
instruction, or other commissioned-capture inputs required by the controlling
Data Capture obligation contract, stop with `visible_stop` or carry the missing
input as a visible limitation. Do not use this profile to backfill a missing
commissioning decision.

## Required Criteria

A source unit reaches mini god-tier only when all six criteria are answered
visibly.

| Criterion | Required answer |
| --- | --- |
| Best in-bound body possession | The strongest appropriate source body or body-equivalent has been preserved within the source-access boundary, or the failure is carried visibly. |
| Identity and provenance | Original locator, final or snapshot locator, source family/surface, HTTP or access status where applicable, content type, byte count, SHA256, capture time, and source/snapshot/publication timing where available are recorded or marked unknown with reason. |
| Source-language anchors | A bounded set of operator-identified or source-visible anchors exists for the supplied decision context, or the source type makes anchors not applicable with reason. |
| Coverage or drift note | The packet state says whether it improves, replaces, supplements, conflicts with, or merely standardizes the prior source state. For historical sources, it notes whether current/live and archived body posture appears same-source or visibly divergent. |
| Visible limitations | Missing media, archive gaps, login gates, cutoff uncertainty, pointer-only states, parse issues, shell pages, body caps, access failures, and other source-observable limits are preserved instead of hidden. |
| Lifecycle state | The output says whether the packet is scratch, candidate evidence, recommended for separate fixture admission, or already admitted by a separate source. |

## Result Tokens

Use these tokens to classify a source-quality pass. They are operating tokens,
not review verdicts, validation states, or Judgment claims.

| Token | Meaning |
| --- | --- |
| `mini_god_tier_met` | All six criteria are visibly satisfied for the bounded source unit. |
| `mini_god_tier_with_visible_limitations` | The strongest available in-bound capture exists, but one or more limitations must travel forward. |
| `current_body_standardized_only` | Current/live body capture is standardized, but historical identity or cutoff posture remains weaker than needed. |
| `archive_body_not_preserved` | Archive availability may exist, but an inspectable archive body was not preserved. |
| `body_possession_not_proven` | Metadata, pointers, shells, failures, or summaries exist, but source-body possession is not proven. |
| `needs_separate_fixture_admission_decision` | The packet may be useful enough to preserve durably, but fixture admission, rights, retention, or sensitivity must be decided separately. |
| `visible_stop` | Required inputs, source-access boundary, permissions, or runner prerequisites are missing, and continuing would require guessing or an unauthorized method. |

Do not invent additional tokens casually. If a future source family needs a new
token, update this profile and carry a direction-change propagation receipt.

## Packet Lifecycle Vocabulary

Use these lifecycle states in mini god-tier reports and source-unit queues:

`docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
controls how these lifecycle states may be cited, retained, or escalated. This
profile owns the operating vocabulary; the decision owns retention and
sensitivity handling.

| State | Meaning |
| --- | --- |
| `scratch` | Local or ignored packet output used for inspection only; not durable evidence. |
| `candidate_evidence` | Packet may be useful for later source-quality work, but no fixture admission, rights, retention, or sensitivity decision is implied. |
| `recommended_fixture_admission` | Recommendation to seek a separate fixture-admission decision; this is not admission and must not be treated as `separately_admitted`. |
| `separately_admitted` | A separate fixture-admission or equivalent lifecycle decision exists and should be cited in the report or queue row. |

If the report cannot cite the separate admission decision, do not use
`separately_admitted`.

## Runner Ladder

Choose the narrowest runner that can plausibly satisfy best in-bound body
possession for the source unit. Do not chain runners unless the operator
authorized a fallback.

| Source posture | Primary runner | Fallback posture |
| --- | --- | --- |
| Already-local body or source artifact | Local file packet runner | If provenance is too weak, classify as `body_possession_not_proven` or `current_body_standardized_only`. |
| Historical identity matters and URL is available | Archive.org runner | If only metadata is preserved, classify as `archive_body_not_preserved`; Direct HTTP may standardize current body only. |
| Current public body is enough | Direct HTTP runner | If the body is an app shell, wall, or blocked page, carry visible limitation and consider browser snapshot only if authorized. |
| Source-visible media or explicit asset URLs matter | Media / Asset runner | Pointer-only or failed media must remain visible. |
| JavaScript-rendered or screenshot-needed page | Browser Snapshot runner | Browser artifacts do not prove content sufficiency; report shell or wall states visibly. |
| Login-visible or entitled browser content | Authenticated Browser Snapshot runner | Requires allowed manual-login storage-state mode; session use does not prove entitlement sufficiency or source completeness. |

## Source-Unit Queue Template

Use this template to plan source-quality passes before running tools. Populate
only fields that are known from supplied sources or operator instruction.

| Field | Meaning |
| --- | --- |
| `source_id` | Stable source identifier from the case, slot, or source packet. |
| `case_or_slot` | Bounded evidence context. |
| `locator` | Original URL, local path, or supplied provenance pointer. |
| `decision_relevance` | Short source-visible reason the unit matters to the decision frame. |
| `current_state` | Existing source posture, such as current-live body, pointer-only, local artifact, archive metadata only, or missing. |
| `target_posture` | The mini god-tier body posture sought. |
| `primary_runner` | Narrowest authorized runner for the target posture. |
| `fallback_runner` | Optional authorized fallback, or `none`. |
| `cutoff` | Relevant cutoff timestamp or reason none applies. |
| `result_token` | One token from this profile after the run. |
| `packet_lifecycle` | Scratch, candidate evidence, recommended fixture admission, or separately admitted. |

Do not use the queue to discover sources, rank source relevance, decide
credibility, or allocate Judgment weight. It is an operating planner for
already-bounded source units.

## Mini God-Tier Report Block

After a source-quality pass, future agents should report the following minimum
fields:

```yaml
mini_god_tier_source_quality_report:
  source_id: "<source id>"
  result_token: "<profile token>"
  packet_path: "<path or none>"
  best_in_bound_body:
    posture: "<preserved|not_preserved|metadata_only|current_only|not_applicable>"
    preserved_body_path: "<packet-relative path or none>"
    sha256: "<hash or none>"
    byte_count: "<bytes or none>"
    source_or_snapshot_time: "<timestamp or unknown_with_reason>"
  provenance:
    original_locator: "<locator or unknown_with_reason>"
    final_or_snapshot_locator: "<locator or unknown_with_reason>"
    access_status: "<status or unknown_with_reason>"
    content_type: "<content type or unknown_with_reason>"
    capture_time: "<timestamp or unknown_with_reason>"
  source_language_anchors:
    - "<bounded source-visible anchor or not_applicable_with_reason>"
  coverage_or_drift_note: "<improves|replaces|supplements|conflicts|standardizes|unknown_with_reason>"
  visible_limitations:
    - "<limitation or none>"
  lifecycle_state: "<scratch|candidate_evidence|recommended_fixture_admission|separately_admitted>"
  non_claims:
    - "not validation"
    - "not source completeness proof"
    - "not fixture admission unless separately decided"
    - "not Judgment scoring"
```

## Non-Claims

This profile is not validation, readiness, source completeness proof, fixture
admission, rights clearance, retention policy, sensitivity review, source-access
boundary amendment, source discovery, crawler authorization, API authorization,
commercial fetch authorization, browser fallback authorization, source-quality
scoring, credibility assessment, inclusion/exclusion advice, ECR design,
Cleaning implementation, Judgment scoring, buyer proof, or commercial-readiness
evidence.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory now has a reusable Mini God-Tier Source Quality Profile that defines the smallest complete source-quality target for future bounded source units without creating fixture admission, validation, source discovery, or Judgment authority."
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - "orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "orca/product/spines/capture/core/source_capture_toolbox/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "orca/product/spines/capture/core/source_capture_toolbox/README.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations, forbidden outputs, and handoff states did not change; this profile operationalizes source-quality targets inside the existing armory."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "No source-access permission, hard stop, entitlement, or disclosability rule changed."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "No new adapter, source method, API, crawler, browser fallback, or production runtime was authorized."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "Checkpoint 1 defines the profile standard only; the agent-facing report-block patch is a later checkpoint."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes armory work through the armory README; no new read-pack entry is required for this profile."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory folder and README as the entrypoint; the README now points to this profile."
  stale_language_search: "rg -n \"mini_god_tier|Mini God-Tier|source-quality scoring|fixture admission|validated|ready|Judgment scoring|ECR design|Cleaning implementation|source discovery|source selection|commissioning gate|Decision Frame|recommended_fixture_admission|separately_admitted\" orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md orca/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md orca-harness/docs/source_capture_agent_runbook.md orca/product/spines/capture/core/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source completeness proof"
    - "not fixture admission"
    - "not source-access boundary amendment"
    - "not adapter authorization"
    - "not ECR, Cleaning, or Judgment authority"
```

## Direction Change Propagation - Review Clarification Patch

```yaml
direction_change_propagation:
  doctrine_changed: "The Mini God-Tier source-quality structure now explicitly separates bounded-source context from the Data Capture Commissioning Gate, defines packet lifecycle states so recommended fixture admission cannot be read as admission, and clarifies that source-quality report blocks require an operator-commissioned source-quality pass."
  trigger: product_doctrine
  related_triggers:
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - "orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "orca/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "orca/product/spines/capture/core/source_capture_toolbox/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  intentionally_not_updated:
    - path: "orca/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "The README already indexes the profile, queue template, and runbook; the clarification changes operating semantics inside those artifacts, not component discoverability."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes armory work through the armory README; no new read-pack entry is required for this clarification."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory folder and runbook surfaces; no new durable source family or component path was added."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and Commissioning Gate requirements did not change; this patch says the mini god-tier structure does not satisfy them by itself."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "No source-access permission, hard stop, entitlement, or disclosability rule changed."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "No new adapter, source method, API, crawler, browser fallback, or production runtime was authorized."
  stale_language_search: "rg -n \"recommended_fixture_admission|separately_admitted|operator-commissioned source-quality pass|operator commissioned a source-quality pass|Commissioning Gate|Decision Frame|source-quality scoring|fixture admission|validated|ready|Judgment scoring|ECR design|Cleaning implementation|source discovery|source selection\" orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md orca/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md orca-harness/docs/source_capture_agent_runbook.md orca/product/spines/capture/core/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not fixture admission"
    - "not source completeness proof"
    - "not source-access boundary amendment"
    - "not adapter authorization"
    - "not ECR, Cleaning, or Judgment authority"
```
