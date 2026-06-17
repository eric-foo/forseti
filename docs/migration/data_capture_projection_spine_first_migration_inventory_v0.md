# Data Capture Projection Spine-First Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Migration inventory (spine-first marking; docs-only)
scope: >
  Marks raw-packet projection, projection-view doctrine, and projection-adjacent
  files for a future spine-first migration, without moving files or changing
  current repo-structure binding. The inventory deliberately classifies
  Mechanical Source Projection under the future Capture spine, not as a new
  Projection spine.
use_when:
  - Planning a spine-first migration for Data Capture / Source Capture projection artifacts.
  - Deciding whether projection deserves its own spine or belongs under Capture.
  - Preparing a later migration manifest or moved-path index for projection-related files.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/product/core_spine_v0_projection_doctrine_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - Mechanical Source Projection ownership changes from Data Capture-owned helper.
  - Projection cache, storage plane, envelope serialization, or data-lake materialization is accepted by a later decision.
  - New IG, Retail/PDP, Reddit, LinkedIn, Cleaning, or ECR projection surfaces are added.
  - A later migration manifest supersedes this class-level inventory.
```

- Status: MIGRATION_MARKING_ONLY.
- Branch basis: `codex/commission-spine-structure` at
  `07a42b04c4343c4e3b964eea11b01fc9ebefe705` when this inventory was drafted.
- Current binding remains `docs/` plus `orca-harness/`; this file does not make
  `orca/product/spines/capture/` or any `orca/` root live.
- No file moves, rewrites, archive decisions, code moves, test moves, runtime
  changes, projection-cache choices, storage choices, or reference rewrites are
  authorized by this inventory.

## Verdict

Projection is not its own future spine under the current sources.

Mechanical Source Projection is a Data Capture-owned helper and Data Capture
Projection Packet row view. The future spine-first home should be under the
Capture spine, with Core, Cleaning, ECR/SCR, and Judgment references kept as
adjacent/shared consumers rather than pulled into a fake Projection spine.

Do not create:

```text
orca/product/spines/projection/
```

Use this as the default future allocation instead, after a later accepted root
migration makes the `orca/product/spines/` tree live:

```text
orca/product/spines/capture/
  authority/projection/
  workflows/projection/
  research/source_families/ig/
  research/source_families/retail_pdp/
  research/source_families/reddit/
  reviews/projection/
  harness/projection/          # pointers/design notes only while code stays in orca-harness/
  tests/projection/            # pointers/test plans only while executable tests stay in orca-harness/
```

Core boundary and data-lake maps should not be swallowed by Capture unless the
later migration explicitly chooses that. They are cross-spine boundary material
and are marked below as shared/core-adjacent.

## Inventory Method

Searches run from the worktree root:

```powershell
rg -n "projection|Projection|materializ|raw-to|raw packet|raw-packet|retail_pdp|ig_projection|creator-momentum" docs orca-harness -g "*.md" -g "*.py" -g "*.yaml"
rg --files docs orca-harness | rg -i "projection|retail_pdp|creator_momentum|ig_creator|ig_capture|ig_|reddit_candidate_intake_to_projection|source_capture_tenant_payload|source_capture_core_payload_split|data_lake_mechanics|capture_projection_storage|data_and_cleaning_spine_boundary|cleaning_spine_foundation|source_capture_agent_runbook|source_capture_cloakbrowser_snapshot|cleaning_projection|linkedin_live_projection"
rg -n "Mechanical Source Projection|Data Capture Projection Packet|retail_pdp_projection|ig_projection|reddit_projection|CleaningProjectionRef|projection sidecar|run_retail_pdp_projection|run_ig_creator_momentum_projection" docs\decisions docs\prompts docs\review-outputs docs\review-inputs orca-harness -g "*.md" -g "*.py" -g "*.yaml"
```

A requested 5.3 sidecar was attempted but could not start because the available
quota for `gpt-5.3-codex-spark` was exhausted. This inventory is therefore a
main-agent source-read inventory, not a reconciled multi-agent census.

## Primary Ownership Mark

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/core_spine_v0_projection_doctrine_v0.md` | `capture/authority/projection/` with a Core-boundary backlink | migrate_later_as_capture_projection_authority_candidate |
| `docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md` | `capture/authority/` | migrate_later |
| `docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md` | `capture/decisions/` or future global decisions | migrate_later_classify |
| `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md` | `capture/decisions/` or future global decisions | migrate_later_classify |
| `docs/product/data_capture_spine/data_capture_spine_pressure_test_execution_authorization_v0.md` | `capture/authority/` or `capture/decisions/` | migrate_later_classify |
| `docs/prompts/data_capture_pressure_test_reddit_mechanical_source_projection_worker_prompt_v0.md` | `capture/prompts/` | migrate_later |

Rationale: these files directly state or exercise Mechanical Source Projection
as a Data Capture-owned helper. They are the strongest Capture-spine candidates.

## Shared Core Boundary - Do Not Auto-Migrate To Capture

These are projection-load-bearing but cross-spine. A later migration should
probably place them in a Core spine or future global product docs, with links
from Capture.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | `core/authority/` or future global boundary docs | shared_core_boundary_do_not_auto_move_to_capture |
| `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | `core/authority/` or `core/workflows/` | shared_core_map_do_not_auto_move_to_capture |
| `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md` | `cleaning/authority/` or shared Core/Cleaning boundary | adjacent_cleaning_do_not_auto_move |
| `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md` | `cleaning/README.md` or shared Core/Cleaning boundary | adjacent_cleaning_do_not_auto_move |
| `docs/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md` | `cleaning/prompts/handoffs/` or shared handoff archive | adjacent_cleaning_prompt_classify |
| `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md` | `cleaning/prompts/handoffs/` | adjacent_cleaning_prompt_classify |
| `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v1.md` | `cleaning/prompts/handoffs/` | adjacent_cleaning_prompt_classify |

## Data-Lake, Payload, And Storage-Plane Candidates

These belong with Capture/data-lake architecture unless a later accepted storage
spine decision creates a different home. The current mark is still Capture, not
Projection.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md` | `capture/authority/payloads/` | migrate_later |
| `docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md` | `capture/guides/` or `capture/authority/payloads/` | migrate_later_classify |
| `docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md` | `capture/research/source_families/retail_pdp/` or `capture/authority/payloads/` | migrate_later_classify |
| `docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md` | `capture/authority/storage/` or `capture/research/storage/` | migrate_later_classify_no_projection_spine |
| `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md` | `capture/authority/source_families/ig/` | migrate_later_classify |
| `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md` | `capture/authority/source_families/ig/` | migrate_later_classify |

The word `storage spine` in `orca_capture_projection_storage_spine_architecture_v0.md`
is not enough to mint a new product spine. That artifact is PROPOSED and explicitly
non-authorizing; it should be reconciled under Capture/data-lake architecture unless
a later owner decision changes the root grammar.

## Retail/PDP Source-Family Projection

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/source_capture_toolbox/retail_pdp_projection_contract_v0.md` | `capture/authority/source_families/retail_pdp/` | migrate_later |
| `docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md` | `capture/workflows/projection/retail_pdp/` | migrate_later |
| `docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md` | `capture/workflows/projection/retail_pdp/` | migrate_later |
| `docs/product/source_capture_toolbox/README.md` | `capture/README.md` or `capture/workflows/source_capture_toolbox/README.md` | migrate_later_classify_with_armory |
| `orca-harness/source_capture/retail_pdp_projection.py` | stay in `orca-harness/`; future `capture/harness/projection/` pointer only | code_stays_until_code_root_migration |
| `orca-harness/runners/run_retail_pdp_projection.py` | stay in `orca-harness/`; future `capture/harness/projection/` pointer only | code_stays_until_code_root_migration |
| `orca-harness/runners/run_source_capture_cloakbrowser_packet.py` | stay in `orca-harness/`; sidecar option documented from Capture | code_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_retail_pdp_projection.py` | stay in `orca-harness/`; future `capture/tests/projection/` pointer only | test_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py` | stay in `orca-harness/`; Retail/PDP sidecar tests are capture-adjacent | test_stays_until_code_root_migration |

## IG / Creator-Momentum Projection And Capture Shape

IG files are source-family Capture candidates. Do not split IG projection into a
separate Projection spine. Also do not blindly move every IG capture feasibility
note into projection; most belong under IG source-family research/authority.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md` | `capture/research/source_families/ig/` | migrate_later |
| `docs/product/source_capture_toolbox/ig_capture_shape_contract_spec_v0.md` | `capture/authority/source_families/ig/` | migrate_later |
| `docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md` | `capture/authority/source_families/ig/` | migrate_later_classify |
| `docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md` | `capture/reports/source_families/ig/` | migrate_later |
| `docs/product/source_capture_toolbox/ig_*` | `capture/research/source_families/ig/` or `capture/authority/source_families/ig/` | migrate_later_classify_by_role |
| `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` | `capture/migrations/` or hygiene archive | migrate_later_classify |
| `docs/prompts/handoffs/ig_capture_rate_at_scale_operating_envelope_handoff_v0.md` | `capture/prompts/handoffs/` | migrate_later |
| `docs/research/creator_momentum_data_landscape_v0.md` | `capture/research/source_families/ig/` or shared market research | migrate_later_classify |
| `orca-harness/source_capture/ig_projection.py` | stay in `orca-harness/`; future `capture/harness/projection/` pointer only | code_stays_until_code_root_migration |
| `orca-harness/source_capture/ig_momentum_harvest.py` | stay in `orca-harness/`; source-family capture support | code_stays_until_code_root_migration |
| `orca-harness/source_capture/ig_calls_parse.py` | stay in `orca-harness/`; source-family capture support | code_stays_until_code_root_migration |
| `orca-harness/runners/run_ig_creator_momentum_projection.py` | stay in `orca-harness/`; future `capture/harness/projection/` pointer only | code_stays_until_code_root_migration |
| `orca-harness/runners/run_source_capture_ig_calls_packet.py` | stay in `orca-harness/`; source-family capture support | code_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_source_capture_ig_projection.py` | stay in `orca-harness/`; future `capture/tests/projection/` pointer only | test_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_ig_momentum_harvest.py` | stay in `orca-harness/`; source-family capture support | test_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_ig_calls_parse.py` | stay in `orca-harness/`; source-family capture support | test_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_source_capture_ig_calls_packet.py` | stay in `orca-harness/`; source-family capture support | test_stays_until_code_root_migration |

Observed IG source-capture toolbox file class at inventory time:

```text
docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md
docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md
docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md
docs/product/source_capture_toolbox/ig_capture_shape_contract_spec_v0.md
docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md
docs/product/source_capture_toolbox/ig_creator_discovery_suggested_accounts_recon_v0.md
docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md
docs/product/source_capture_toolbox/ig_logged_out_sustainability_probe_plan_v0.md
docs/product/source_capture_toolbox/ig_r_probe_results_v0.md
docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md
docs/product/source_capture_toolbox/ig_sustained_cadence_r_probe_design_v0.md
docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md
docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md
```

## Reddit And Candidate-Projection Surfaces

Reddit projection appears in two meanings: Mechanical Source Projection over
captured Reddit packets, and Candidate URL Intake projection into candidate rows.
Both stay under Capture-family work, but they should not be merged without a
source-family classification pass.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `orca-harness/source_capture/reddit_projection.py` | stay in `orca-harness/`; future `capture/harness/projection/reddit/` pointer only | code_stays_until_code_root_migration |
| `orca-harness/tests/unit/test_reddit_projection.py` | stay in `orca-harness/`; future `capture/tests/projection/reddit/` pointer only | test_stays_until_code_root_migration |
| `docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md` | `capture/workflows/source_families/reddit/` | migrate_later_classify_candidate_projection |
| `docs/workflows/reddit_candidate_intake_subreddit_projection_b2b_001_closeout_v0.md` | `capture/reports/source_families/reddit/` | migrate_later_classify_candidate_projection |
| `docs/workflows/reddit_candidate_intake_subreddit_projection_seo_002_closeout_v0.md` | `capture/reports/source_families/reddit/` | migrate_later_classify_candidate_projection |
| `docs/decisions/reddit_candidate_intake_old_reddit_html_projection_delegated_review_adjudication_decision_v0.md` | `capture/decisions/` or future global decisions | migrate_later_classify_candidate_projection |
| `docs/prompts/reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_prompt_v0.md` | `capture/prompts/reviews/` | migrate_later_classify_candidate_projection |
| `docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_v0.md` | `capture/reviews/outputs/` | migrate_later_classify_candidate_projection |
| `orca-harness/capture_spine/reddit_candidate_intake/projection.py` | stay in `orca-harness/capture_spine/` until code-root migration | code_stays_capture_spine |
| `orca-harness/tests/unit/test_reddit_candidate_intake.py` projection tests | stay in `orca-harness/` until code-root migration | test_stays_capture_spine |

## LinkedIn Candidate-Projection Surfaces

These are Capture Spine candidate-row projection helpers, not raw-packet
Mechanical Source Projection. Mark them as Capture-adjacent and do not merge them
into Retail/PDP or IG projection without a source-family pass.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `orca-harness/capture_spine/linkedin_live_adapter/projection.py` | stay in `orca-harness/capture_spine/` until code-root migration | code_stays_capture_spine |
| `docs/review-outputs/adversarial-artifact-reviews/linkedin_live_projection_slice3b2_code_review_v0.md` | `capture/reviews/outputs/source_families/linkedin/` | migrate_later_classify_candidate_projection |
| `docs/review-outputs/adversarial-artifact-reviews/linkedin_live_projection_slice3b2_code_review_v1.md` | `capture/reviews/outputs/source_families/linkedin/` | migrate_later_classify_candidate_projection |
| `docs/review-outputs/linkedin_live_projection_slice3b2_v0_no_repo_review_bundle.zip` | `capture/reviews/bundles/source_families/linkedin/` or global review archive | migrate_later_classify_bundle_policy |
| `docs/review-outputs/linkedin_live_projection_slice3b2_v1_no_repo_review_bundle.zip` | `capture/reviews/bundles/source_families/linkedin/` or global review archive | migrate_later_classify_bundle_policy |

## Cleaning And Downstream Consumers - Do Not Auto-Migrate To Capture

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `orca-harness/cleaning/projection.py` | stay in `orca-harness/`; future Cleaning spine pointer only | code_stays_cleaning_consumer |
| `orca-harness/cleaning/models.py` (`CleaningProjectionRef`) | stay in `orca-harness/`; future Cleaning spine pointer only | code_stays_cleaning_consumer |
| `orca-harness/tests/unit/test_cleaning_projection_integration.py` | stay in `orca-harness/`; future Cleaning tests pointer only | test_stays_cleaning_consumer |
| `orca-harness/tests/unit/test_cleaning_core.py` projection-ref assertions | stay in `orca-harness/`; future Cleaning tests pointer only | test_stays_cleaning_consumer |

Cleaning consumes projection references; it does not own projection.

## Review And Review-Input Candidates

| Current path class | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md` | `capture/reviews/outputs/projection/` or shared Core/Capture review | migrate_later_classify |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_*projection*` | `capture/reviews/outputs/` | migrate_later_classify |
| `docs/review-inputs/judgment_conductor_*/*core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | stay with Judgment review bundle or future global review archive | do_not_auto_move_duplicate_source_copy |

Review bundles should be migrated only after a review-specific moved-path index
or archive policy exists. Do not hand-move copied source files inside review
input bundles as if they were owner sources.

## False Positives And Do-Not-Auto-Migrate Classes

| Path class | Reason |
| --- | --- |
| `docs/prompts/wrappers/demand_projection_*` | Demand projection is product/demand analysis, not raw-packet Mechanical Source Projection. |
| `docs/review-inputs/demand_projection_*` | Demand projection review inputs are not Capture projection authority. |
| `docs/review-outputs/adversarial-artifact-reviews/demand_projection_*` | Demand projection review outputs are not Capture projection authority. |
| `docs/product/core_spine/*first_proof*` references to BLS projections | Ordinary forecast/projection word use, not this lane. |
| `orca-harness/signal_content/deriver.py` materialized wording | Signal Content Record derived-record language, not projection ownership. |
| `docs/migration/repo_structure_phase2_consolidation_v0/harness_scratch_config_snippet.toml` | Migration support file; projection hit is incidental. |

## Proposed Migration Sequence

1. Do not create a Projection spine.
2. If the spine-first root is accepted, migrate Capture first-class projection
   authority into `orca/product/spines/capture/authority/projection/` only after
   Capture's broader spine inventory exists.
3. Keep Core boundary/data-lake docs in Core/shared homes with Capture backlinks.
4. Move Retail/PDP, IG, Reddit, and LinkedIn projection artifacts by source-family
   subfolders, not as one platform-blind bucket.
5. Leave `orca-harness/` code and executable tests in place until a separate
   code-root migration decision exists; add pointers under the future Capture
   spine rather than moving runtime files.
6. Migrate review outputs only after a review-bundle policy and moved-path index
   are prepared.

## Non-Claims

This inventory is not a move manifest, validation, readiness, acceptance,
source-of-truth promotion, proof of completeness, runtime authorization,
implementation authorization, storage selection, projection-cache selection, or
code-root migration authorization. It marks projection-related documents and
classes for later migration planning only.
