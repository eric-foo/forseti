# Source Quality State Assembler v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Architecture boundary for a read-only Source Capture-owned state assembler over already-bounded Mini God-Tier source-quality rows and existing Source Capture Packets.
use_when:
  - Deciding whether a future Source Quality helper may combine multiple already-bounded source-quality rows.
  - Preventing packet success, helper suggestions, or scratch lifecycle from being upgraded into source-quality verdicts.
  - Distinguishing the Source Capture Armory state-assembler pattern from Judgment Spine conductor authority.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
  - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
stale_if:
  - The Mini God-Tier profile changes result tokens, lifecycle states, or report-block fields.
  - The source-unit queue template changes row-status vocabulary or bounded-source rules.
  - The report-skeleton helper begins finalizing source-quality results instead of requiring operator review.
  - A later accepted architecture authorizes runner dispatch, durable combined reports, fixture admission, or source-quality scoring.
```

## Status

Status: `SOURCE_QUALITY_STATE_ASSEMBLER_ARCHITECTURE_V0`.

This artifact records the architecture boundary for a possible Source Quality
State Assembler. It is an architecture note for future scoped work, not an
implementation plan and not implementation authorization.

## Purpose

Mini God-Tier is Orca's smallest complete source-quality target for a bounded
source unit. It is not maximal collection. It is best in-bound body possession
plus identity/provenance, bounded source-language anchors, coverage or drift
posture, visible limitations, and lifecycle posture sufficient for downstream
use or visible stop.

The Source Quality State Assembler exists to make that target repeatable across
multiple already-bounded source units without creating fake completeness. It
would assemble existing queue-row, packet, helper-output, lifecycle, and
limitation state into an inspectable state view.

The word "conductor" is intentionally not used for this layer. A conductor can
sound like a gate sequencer or authority surface. This layer is only a state
assembler/router: it reads existing state, preserves stops, and routes
quality-bearing conclusions back to the operator.

## Use This For

- Checking whether a future helper can safely combine existing source-quality
  row state.
- Keeping packet-write success separate from source-quality result tokens.
- Preserving metadata-only, body-missing, scratch, and limitation states across
  a multi-row source-quality pass.
- Borrowing Judgment Spine conductor discipline as a pattern without importing
  Judgment authority.

## Do Not Use This For

- Source discovery or source selection.
- Source acquisition, runner dispatch, archive retrieval, browser capture,
  media capture, API calls, scraper behavior, or fallback chaining.
- Source-quality scoring, credibility, relevance ranking, inclusion, exclusion,
  fixture admission, rights, retention, sensitivity, or lifecycle admission.
- Automated finalization of `mini_god_tier_met`.
- ECR, Cleaning, Judgment, buyer-proof, or commercial-readiness claims.

## Accepted Target Architecture

The accepted v0 target is a Source Capture-owned, read-only assembler/router
over already-bounded source-quality rows and existing Source Capture Packets (CapturePacket).

Its only allowed flow is:

```text
already-bounded queue row
  -> existing packet path
  -> packet-exists-at-cited-path check
  -> packet-inspectability check
  -> already-produced or read-only report-skeleton helper output surfaced verbatim
  -> operator-finalization requirement
  -> per-row and combined state census
```

The combined output shape is a state census, not a verdict. It may count or
list source units by posture, but it must keep each row's result token,
limitations, lifecycle state, and operator-completion requirements visible. It
must not claim that a batch passed, that a ladder completed, that a fixture is
admitted, or that source quality was scored.

## Core Responsibilities

The v0 state assembler may:

- read already-bounded source-unit queue rows;
- read existing Source Capture Packet directories or manifests;
- check whether the cited packet path exists;
- check whether the packet is inspectable enough for the existing report
  skeleton helper to read;
- surface already-produced helper output, or invoke only the existing read-only
  report-skeleton helper against an existing packet manifest;
- surface the helper's `suggested_result_token`,
  `result_token_finalization`, `operator_completion_required`,
  `visible_limitations`, and `lifecycle_state` without strengthening them;
- echo the row's existing workflow state from the queue template's row-status
  vocabulary;
- preserve input order in any combined view;
- emit a failure-preserving state census.

## Forbidden Responsibilities

The v0 state assembler must not:

- discover, select, rank, include, exclude, or search for sources;
- launch any Source Capture runner;
- launch the report-skeleton CLI as a runner-dispatch substitute unless a later
  implementation scope explicitly authorizes that read-only invocation shape;
- fetch, retrieve, archive, render, screenshot, preserve media, call APIs, or
  automate browsers;
- parse raw source bodies for meaning;
- infer source-language anchors;
- score source quality, credibility, relevance, or Judgment meaning;
- finalize `mini_god_tier_met` by automation;
- auto-advance a row to `reported`;
- assert `ready_for_tool_run` as dispatch authorization;
- mint result tokens, lifecycle states, row-status tokens, or aggregate status
  vocabulary;
- convert `_test_runs/` packet paths into durable evidence;
- emit `recommended_fixture_admission` or `separately_admitted` without the
  separate decision/reference required by the Mini God-Tier profile and helper;
- create a durable combined report unless a later owner decision authorizes the
  output form and claim boundary;
- produce ECR, Cleaning, Judgment, buyer-proof, or product-readiness outputs.

## Judgment Pattern Reference

Judgment Spine has a conductor pattern that sequences owned gates, verifies
receipts, routes to the next owner, and carries a no-authority invariant. That
pattern is useful here only as discipline:

- route, do not restate;
- preserve visible stops instead of skipping rows;
- do not compute the quality claim being routed;
- treat missing receipts or missing inputs as stops, not success.

This artifact does not import Judgment authority. It does not borrow Judgment
claim tiers, credibility analysis, Signal Use, Decision Strength, Action
Ceiling, reveal/calibration, scoring, or gate semantics. Judgment remains the
owner of inference and decision-use effects. Source Capture remains the owner
of capture and source-quality support mechanics.

## Fake-Success Guardrails

| Fake-success vector | Required guardrail |
| --- | --- |
| Packet exists, therefore source body is possessed. | Keep helper body posture and result token visible; metadata-only remains metadata-only. |
| Archive availability metadata becomes archive body preservation. | Preserve `archive_body_not_preserved` or `body_possession_not_proven` when no inspectable body is present. |
| Empty visible limitations becomes clean pass. | Preserve `result_token_finalization: operator_review_required`; empty helper limitations never finalize met-ness. |
| Scratch packet becomes durable evidence. | Preserve packet lifecycle and `_test_runs/` scratch boundary. |
| Helper suggestion becomes final result. | Keep `suggested_result_token` distinct from operator-finalized report blocks. |
| Combined batch view becomes pass/fail verdict. | Emit census/listing only; no green rollup, no "all rows passed", no ladder completion claim. |
| Bounded source row becomes Commissioning Gate or Decision Frame. | Carry missing commissioned-capture inputs as visible stop or limitation. |
| Judgment conductor pattern imports Judgment authority. | Cite Judgment only for no-authority routing discipline. |

## Output Boundary

Allowed future output, if separately authorized, is a state census over existing
rows and packets. It may say what was inspectable, missing, limited, suggested,
or waiting for operator finalization.

It must not say the source-quality batch is validated, ready, admitted,
complete, scored, Judgment-useful, buyer-proof, or commercially ready.

## Non-Claims

This artifact is not validation, readiness, source completeness proof, fixture
admission, rights clearance, retention policy, sensitivity review, source-access
boundary amendment, source discovery, runner dispatch authorization, API
authorization, crawler authorization, browser fallback authorization,
source-quality scoring, credibility assessment, inclusion/exclusion advice, ECR
design, Cleaning implementation, Judgment scoring, buyer proof, or
commercial-readiness evidence.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory now has a Source Quality State Assembler architecture boundary for read-only multi-row source-quality state census over already-bounded rows and existing packets, explicitly avoiding conductor/gate-sequencer authority."
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
    - product_doctrine
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - "CLAUDE.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - "docs/workflows/artifact_retrievability_guide.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "forseti-harness/docs/source_capture_agent_runbook.md"
    - "forseti-harness/source_capture/source_quality.py"
    - "docs/product/judgment_quality_promotion_operating_model_v0.md"
    - "docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md"
    - "docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md"
  intentionally_not_updated:
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "Mini God-Tier criteria, result tokens, lifecycle states, and report-block fields did not change."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "Queue fields and row-status vocabulary did not change; this architecture only assembles existing state."
    - path: "CLAUDE.md"
      reason: "Claude-specific instructions already defer Orca project rules to the overlay and DCP contract; no Source Capture component, output, or source-quality boundary is encoded there."
    - path: "forseti-harness/docs/source_capture_agent_runbook.md"
      reason: "No runner, helper, or agent procedure changed in this docs-only architecture boundary."
    - path: "forseti-harness/source_capture/source_quality.py"
      reason: "The report-skeleton helper behavior did not change; it remains operator-review-required and never finalizes mini_god_tier_met."
    - path: "docs/product/judgment_quality_promotion_operating_model_v0.md"
      reason: "Judgment conductor doctrine is referenced only as a pattern source; no Judgment gate, claim-tier, or scoring rule changed."
    - path: "docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md"
      reason: "Judgment/Data Capture boundary already separates Judgment inference from source acquisition and preservation mechanics."
    - path: "docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md"
      reason: "The Daimler toolkit-planning boundary already keeps Source Capture Armory responsibilities separate from later Judgment packet/reveal/execution/calibration concerns."
  stale_language_search: "rg -n \"Source Quality State Assembler|source_quality_state_assembler|conductor|gate sequencer|validated|ready|fixture admission|Judgment scoring|source discovery|source selection|runner dispatch|mini_god_tier_met|all rows passed|ladder complete\" forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md forseti/product/spines/capture/core/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  stale_language_search_result: "Executed on 2026-06-03 after the AR-01 through AR-05 review patch. Hits are expected title/navigation references, explicit forbidden-responsibility and non-claim text, Judgment-pattern caveats, the source-loading/repo-map navigation entries, existing Judgment conductor navigation text, and this DCP receipt/search string. No hit authorizes conductor/gate-sequencer behavior, validation, readiness, fixture admission, Judgment scoring, source discovery, source selection, runner dispatch, automated mini_god_tier_met finalization, all-rows-passed rollup, or ladder-complete claim."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source completeness proof"
    - "not fixture admission"
    - "not source discovery"
    - "not source acquisition"
    - "not runner dispatch authorization"
    - "not ECR, Cleaning, or Judgment authority"
```
