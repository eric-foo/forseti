# Data Capture Spine Consolidation Map v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow navigation artifact (Data Capture Spine consolidation map / orientation submap)
scope: Single entry point that orients a reader across Data Capture Spine, Source Capture Armory, source-access authority, source-quality support, and harness implementation surfaces. Map only; not source-of-truth.
use_when:
  - Orienting to Data Capture Spine or Source Capture Armory before source-access, packet, runner, source-quality, or capture-lane work.
  - Finding which owner doc owns a capture area, source-access method, armory component, packet lifecycle, or implementation surface.
  - Checking current Reddit pre-commercial capture routing without bulk-loading every capture artifact.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/README.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
stale_if:
  - The source-access tooling authorization changes build tranches, selected backend, or Reddit ordering.
  - The Source Capture Armory README changes component status, runner set, or gap list.
  - The Data Capture obligation contract changes capture obligations or forbidden outputs.
  - Source Capture Packet lifecycle, retention, or fixture-admission rules move to a new owner.
  - Data Capture operating-model, obligation-baseline, lane-thesis, or commissioning-plan ownership moves.
```

> **What this is.** A retrieval map. It tells a cold reader which owner source
> to open for a Data Capture / Source Capture Armory question. It is the map, not
> the authority: on any conflict, the pointed-to owner source wins.
>
> **Do not use** this map as validation, readiness, source-access permission,
> implementation authorization, fixture admission, source-quality proof, ECR,
> Cleaning, Judgment, or buyer proof.

## Fast Route

| I need to... | Open |
| --- | --- |
| Understand current Source Capture Armory components and gaps | `docs/product/source_capture_toolbox/README.md` |
| Check whether a source-access build or backend is authorized | `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` |
| Check source-access boundary / hard stops | `docs/product/data_capture_source_access_boundary_decision_v0.md` |
| Compare source-access methods and Reddit ordering | `docs/product/data_capture_source_access_method_plan_v0.md` |
| Check operating-model / commissioning-plan authority | `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`, then `docs/product/data_capture_harness_operating_model_architecture_v2.md` or `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` as needed |
| Plan bounded pre-commercial Reddit capture/consolidation | `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md` |
| Check Capture obligations / forbidden outputs | `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` |
| Check packet lifecycle, retention, sensitivity, or fixture movement | `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md` |
| Run existing capture tools safely | `orca-harness/docs/source_capture_agent_runbook.md` |
| Author a new adapter against existing conventions | `orca-harness/docs/adapter_author_contract.md` |
| Inspect actual implemented adapters/runners | `orca-harness/source_capture/` and `orca-harness/runners/` |
| Choose or escalate an anti-block rung against a 403 bot-block (honestly) | `docs/product/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md` |
| Check source-quality pass/report conventions | `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` and `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` |
| Assemble existing source-quality rows and packet state | `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` |

## Current Reality Snapshot

- **Armory is the entrypoint.** `docs/product/source_capture_toolbox/README.md`
  indexes components, build order, current gaps, and non-claims.
- **Anti-block HTTP ladder has a rung-1 arm + usage guide.** A header-complete
  stdlib anti-blocking HTTP fetch (`anti_blocking_http`, rung-1) plus a
  `block_shell` honest-success guard were built and live-proven against one
  Akamai 403 wall (Daimler IR PDFs) — container-level retrieval, one data point,
  not a settled capability. Introduced on the `feat/anti-block-http-ladder`
  branch (confirm merge state in git before assuming it is on main). See the
  anti-block ladder usage guide and the rung-resolution closeout in Areas.
- **Build authority is bounded.** The source-access tooling authorization owns
  first/second/third-tranche build scope. It now selects CloakBrowser as the
  primary anti-blocking backend.
- **Reddit pre-commercial route is source-specific.** Use CloakBrowser
  anti-blocking first once implemented, prefer old Reddit HTML where available,
  keep capture low-volume and subreddit/thematic/thread-family bounded, then use
  archive capture where live capture is unnecessary or fails visibly.
- **Reddit consolidation now has a planning thread.**
  `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`
  is the durable architectural planning artifact for packet-before-parser
  handoff, BeautifulSoup parser role, provenance-first consolidation shape, and
  implementation stop lines.
- **Reddit `.json` is not the spine.** Treat anonymous `.json` endpoints as
  opportunistic fallback only; current official guidance and developer reports
  indicate OAuth/login credentials are expected and anonymous `.json` access can
  fail with 403/network-security blocks.
- **BeautifulSoup is parser-only.** It can parse retrieved old Reddit HTML or
  archived HTML after preservation; it does not fetch, bypass blocking, solve JS,
  or replace packet provenance.
- **No broad crawling.** Subreddit/thematic/thread-family bounding is allowed for
  Reddit pre-commercial capture, but site-wide walking, generic harvesting,
  production monitoring, storage, dashboards, deployment, and production runtime
  remain outside this map.

## Areas

### Capture obligations

- summary: What a Data Capture packet must preserve and what it must not decide.
- owner: `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`

### Source-access boundary

- summary: Discoverable-or-entitled + disclosable standard, owner-accepted
  anti-blocking risk posture, and hard stops.
- owner: `docs/product/data_capture_source_access_boundary_decision_v0.md`

### Source-access build authority

- summary: Bounded first/second/third-tranche build authority, CloakBrowser
  selection, Reddit ordering, deferred commercial/runtime surfaces, non-claims.
- owner: `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`

### Method planning

- summary: Candidate methods, source-family recommendations, Reddit `.json`
  posture, old Reddit HTML preference, BeautifulSoup parser position.
- owner: `docs/product/data_capture_source_access_method_plan_v0.md`

### Operating model / commissioning

- summary: Owner-accepted v2 Data Capture operating-model architecture,
  obligation baseline, lane thesis, and bounded pressure-test commissioning
  plan. These are pressure-test planning authorities, not validation,
  hardening, product readiness, runtime, ECR, Cleaning, or Judgment design.
- owners: `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`,
  `docs/product/data_capture_harness_operating_model_architecture_v2.md`,
  `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`,
  `docs/product/data_capture_obligation_baseline_decision_v0.md`,
  `docs/product/data_capture_spine_lane_product_thesis_v0.md`,
  `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`

### Reddit pre-commercial planning thread

- summary: Architectural planning route for bounded Reddit capture and
  consolidation: CloakBrowser-first old Reddit HTML, packet-before-parser
  handoff, provenance-first consolidation fields, archive fallback, `.json`
  fallback posture, and implementation stop lines.
- owner: `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`

### Source Capture Armory

- summary: Product-facing component index, build order, current gaps, non-claims,
  and source-quality entrypoints.
- owner: `docs/product/source_capture_toolbox/README.md`

### Anti-block capture ladder

- summary: How to choose and honestly escalate anti-block rungs (0 `direct_http`
  control → 1 header-complete `anti_blocking_http` → 2 `curl_cffi` TLS/JA3
  (gated) → 3 `browser_snapshot` → heavier rungs) against 403 bot-blocks; how to
  judge success honestly (`block_shell` + a container-level discriminator); and
  the live Daimler/Akamai rung-1 result. Cost-ordered, not capability-ordered;
  browser rungs do not capture file bytes; one data point, not a settled
  capability.
- owners: `docs/product/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md`,
  `docs/product/source_capture_toolbox/source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md`

### Packet lifecycle / retention

- summary: Scratch packet lifecycle, durable citation, retention/sensitivity
  handling, and separate fixture admission boundaries.
- owner: `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`

### Harness implementation

- summary: Current runnable packet writers, adapters, runner docs, and tests.
  Implementation reality must be checked in code; docs may be ahead of runners.
- owners: `orca-harness/docs/source_capture_agent_runbook.md`,
  `orca-harness/docs/adapter_author_contract.md`, `orca-harness/source_capture/`,
  `orca-harness/runners/`

### Source-quality support

- summary: Mini God-Tier source-quality posture, queue/report template,
  state assembler, and operational closeouts. These do not validate sources or
  admit fixtures.
- owners: `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`,
  `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md`,
  `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md`

## Non-Claims

This map is not validation, readiness, source-access boundary amendment, legal
sufficiency, implementation execution, source completeness proof, fixture
admission, source-quality scoring, ECR design, Cleaning implementation, Judgment
design, buyer proof, commercial fetch authorization, broad crawler authorization,
storage/dashboard/deployment authorization, or production-runtime authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Data Capture Spine and Source Capture Armory now have a thin workflow consolidation map, and Reddit capture routing records old Reddit HTML as the preferred pre-commercial browser-visible surface while treating anonymous `.json` as opportunistic fallback and BeautifulSoup as parser-only."
  trigger: workflow_authority
  related_triggers:
    - product_doctrine
    - architecture_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/docs/adapter_author_contract.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Top-level project instructions do not enumerate per-spine repo maps or Reddit source-access method ordering."
    - path: ".agents/workflow-overlay/artifact-folders.md"
      reason: "docs/workflows already owns repo maps and workflow navigation artifacts; no new folder convention was introduced."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary permission and hard stops already permit disclosable anti-blocking; this patch changes route/order and navigation, not the boundary."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden outputs did not change."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "The runbook already states CloakBrowser anti-blocking is authorized but not implemented in current runners; this map adds navigation, not runnable commands."
    - path: "orca-harness/docs/adapter_author_contract.md"
      reason: "Adapter author conventions already mention the selected CloakBrowser route; this map does not change adapter implementation conventions."
  stale_language_search: "rg -n \"Judgment Spine entry map|Data Capture Spine entry map|data_capture_spine_consolidation_map|Reddit official API.*cleanest|human-led/browser-visible capture by default pre-sale|anonymous `.json`.*primary|BeautifulSoup.*access method|old Reddit\" docs/workflows/orca_repo_map_v0.md .agents/workflow-overlay/source-loading.md .agents/workflow-overlay/source-of-truth.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/data_capture_source_access_method_plan_v0.md docs/product/source_capture_toolbox/README.md"
  stale_language_search_result: "Executed 2026-06-05 after this patch. Remaining hits are this map, the main repo-map pointer, source-loading pointer, source-of-truth known-document entry, current old Reddit / `.json` / BeautifulSoup posture text, and historical receipt text. No live route makes anonymous `.json` primary or BeautifulSoup an access method."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not legal sufficiency"
    - "not implementation execution"
    - "not CloakBrowser installed"
    - "not Reddit live-run authorization"
    - "not commercial fetch, broad crawling, storage, dashboard, deployment, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Anti-Block Capture Ladder Navigation

```yaml
direction_change_propagation:
  doctrine_changed: "The Data Capture submap and repo map now route to the anti-block capture ladder: a header-complete anti_blocking_http rung-1 adapter plus a block_shell honest-success guard (introduced on feat/anti-block-http-ladder, live-proven against one Akamai 403 wall — one data point, container-level retrieval, not settled), with a usage guide and a rung-resolution closeout."
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The README reflects committed-main armory state; the rung-1 arm is on feat/anti-block-http-ladder and not yet merged. Index it from the README in a separate pass when the arm lands on main."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Build authority is unchanged; the header-complete stdlib rung is within the authorized bounded anti-blocking scope and adds no new gated surface."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not a settled anti-block capability"
    - "not merged to main"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment design"
```
