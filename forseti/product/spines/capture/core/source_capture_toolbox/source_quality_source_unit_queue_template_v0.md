# Source Quality Source-Unit Queue Template v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Reusable blank queue template for planning mini god-tier source-quality passes over bounded source units.
use_when:
  - Preparing a batch of already-bounded source units for Source Capture Armory runner use.
  - Tracking pre-run, blocked, packet-written, and reported states without selecting or ranking sources.
  - Keeping mini god-tier result tokens and packet lifecycle state consistent across source-quality passes.
authority_boundary: bounded_planning_template
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - forseti-harness/docs/source_capture_agent_runbook.md
stale_if:
  - The Mini God-Tier Source Quality Profile changes result tokens or required criteria.
  - The Source Capture Armory runner set or packet lifecycle changes.
  - A separate fixture-admission, rights, retention, or sensitivity policy becomes controlling for generated packets.
```

## Status

Status: `SOURCE_QUALITY_SOURCE_UNIT_QUEUE_TEMPLATE_V0`.

This template helps agents plan source-quality passes for source units that are
already bounded by a case, slot, source packet, or operator instruction. It is
a planning surface for applying the Mini God-Tier Source Quality Profile; it is
not a source-discovery, source-selection, fixture-admission, or Judgment
surface.

Already bounded does not mean Commissioning Gate satisfied. If the row lacks a
decision question, cutoff posture, operator instruction, or other required
commissioned-capture input, keep the row at `blocked_missing_input` instead of
using the queue to backfill missing commissioning context.

## Queue Row Fields

Each queue row should carry only operator-supplied or source-visible planning
facts. Unknowns must remain visible.

| Field | Required? | Meaning |
| --- | --- | --- |
| `source_id` | yes | Stable source identifier from the case, slot, source packet, or operator instruction. |
| `case_or_slot` | yes | Bounded evidence context. |
| `locator` | yes, unless unknown with reason | Original URL, local path, or supplied provenance pointer. |
| `decision_relevance` | yes, bounded | Short operator-supplied or source-visible reason the unit matters to the decision frame; not a relevance ranking and not a substitute for a Decision Frame. |
| `current_state` | yes | Existing source posture, such as current-live body, pointer-only, local artifact, archive metadata only, missing body, or unknown with reason. |
| `target_posture` | yes | The mini god-tier body posture sought for this unit. |
| `primary_runner` | yes | Narrowest authorized Source Capture Armory runner for the target posture. |
| `fallback_runner` | optional | Explicitly authorized fallback runner, or `none`. |
| `cutoff` | yes, when applicable | Relevant cutoff timestamp or reason no cutoff applies. |
| `row_status` | yes | Queue workflow state from the row-status vocabulary below. |
| `result_token` | no before run; yes after report | Result token from the Mini God-Tier profile. |
| `packet_lifecycle` | yes after packet exists | Lifecycle state from the Mini God-Tier profile; `recommended_fixture_admission` is only a recommendation to seek a separate admission decision. |
| `visible_limitations` | optional before run; yes after report if any | Source-visible, access, archive, media, cutoff, shell, or lifecycle limits. |
| `notes` | optional | Bounded operator notes that do not select sources, score quality, or interpret Judgment meaning. |

## Row-Status Vocabulary

These row-status tokens describe queue workflow position only. They do not
classify source quality.

| Token | Meaning |
| --- | --- |
| `planned` | Row has enough context to be considered, but runner inputs are not yet confirmed. |
| `ready_for_tool_run` | Required runner inputs are present and no visible stop is known. |
| `blocked_missing_input` | The row cannot be run without a concrete missing input, permission, cutoff, locator, or runner prerequisite. |
| `packet_written_needs_report` | A packet was written, but the mini god-tier report block has not yet been completed. |
| `reported` | The mini god-tier report block has been completed and the row has a result token. |

Use result tokens only from
`source_quality_mini_god_tier_profile_v0.md`. Do not create row-local result
tokens.

## Blank Queue Table

| source_id | case_or_slot | locator | decision_relevance | current_state | target_posture | primary_runner | fallback_runner | cutoff | row_status | result_token | packet_lifecycle | visible_limitations | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  | `planned` |  |  |  |  |

## Fill Rules

- Do not add a row unless the source unit is already bounded by owner,
  operator, case, slot, or source-packet context.
- Do not treat a bounded source row as satisfying the Data Capture
  Commissioning Gate by itself.
- Do not use this queue to search for, discover, rank, include, exclude, or
  score sources.
- Do not mark a row `ready_for_tool_run` unless the exact runner input is
  present and the runner is authorized by current Source Capture Armory
  boundaries.
- Do not fill `result_token` until a packet result or visible stop has been
  inspected against the Mini God-Tier Source Quality Profile.
- Do not convert `_test_runs/` packet paths into durable evidence by placing
  them in the queue. Use `packet_lifecycle` to keep scratch, candidate, and
  admitted states separate. Use `separately_admitted` only when the row can cite
  a separate fixture-admission or equivalent lifecycle decision.
- If the row needs a method outside the first-tranche armory, mark the missing
  method as a visible limitation or blocker instead of inventing a runner.

## Non-Claims

This template is not source discovery, source selection, source ranking,
source-quality scoring, source completeness proof, validation, readiness,
fixture admission, rights clearance, retention policy, sensitivity review,
source-access boundary amendment, adapter authorization, browser fallback
authorization, API authorization, crawler authorization, ECR design, Cleaning
implementation, Judgment scoring, buyer proof, or commercial-readiness evidence.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory now has a reusable blank source-unit queue template for planning mini god-tier source-quality passes without selecting sources, redefining result tokens, or converting packet outputs into fixture admission."
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti-harness/docs/source_capture_agent_runbook.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "The profile already owns result tokens, required criteria, and a source-unit queue field summary; this template references that authority without changing it."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations, forbidden outputs, and handoff states did not change."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "No source-access permission, hard stop, entitlement, or disclosability rule changed."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "No new adapter, source method, API, crawler, browser fallback, or production runtime was authorized."
    - path: "forseti-harness/docs/source_capture_agent_runbook.md"
      reason: "Checkpoint 2 defines the product queue template only; agent-facing report-block integration remains a later checkpoint."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes armory work through the armory README; no new read-pack entry is required for this template."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory folder and README as the entrypoint; the README now points to this template."
  stale_language_search: "rg -n \"ready_for_tool_run|fixture admission|source-quality scoring|validated|ready|Judgment scoring|ECR design|Cleaning implementation|source discovery|source selection|Commissioning Gate|Decision Frame|recommended_fixture_admission|separately_admitted\" forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md forseti-harness/docs/source_capture_agent_runbook.md forseti/product/spines/capture/core/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source discovery"
    - "not source selection"
    - "not source completeness proof"
    - "not fixture admission"
    - "not source-access boundary amendment"
    - "not adapter authorization"
    - "not ECR, Cleaning, or Judgment authority"
```
