# Cleaning Spine-First Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Migration inventory (Cleaning spine-first marking; docs-only)
scope: >
  Inventory Cleaning-owned and Cleaning-adjacent artifacts for a future
  spine-first Orca workspace migration, without moving files or changing current
  repo-structure binding.
use_when:
  - Planning where Cleaning artifacts should live under a future spine-first structure.
  - Separating Cleaning ownership from Capture, ECR/SCR, Foundation, Judgment, and satellite consumers.
  - Preparing a later move manifest, moved-path index, or spine-local README for Cleaning.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md
  - docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/product/core_spine_v0_projection_doctrine_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - Cleaning Foundation changes the layer boundary, allowed transform classes, or raw-keyed handle contract.
  - Capture, ECR/SCR, Judgment, Foundation, or satellite ownership changes.
  - Code-root migration out of orca-harness is authorized.
  - A later Cleaning move manifest supersedes this inventory.
```

- Status: `MIGRATION_MARKING_ONLY`.
- Current binding remains `docs/` plus `orca-harness/`.
- Future `orca/product/spines/cleaning/` paths in this inventory are target
  candidates only. They are not live placement homes until a later accepted
  structure decision and binding patch make them live.
- No files were moved by this pass.
- No code, tests, schemas, package files, runtime files, generated artifacts, or
  review bundles are moved by this inventory.

## 1. Start-State Receipt

```yaml
worktree_path: C:/Users/vmon7/Desktop/projects/orca/orca-worktrees/cleaning-spine-first-migration-inventory
branch: codex/cleaning-spine-first-migration-inventory
base: origin/main
head_at_start: b139fa9f
dirty_state_at_start: clean
current_binding_observed:
  - docs/decisions/orca_repo_structure_binding_v0.md
  - .agents/workflow-overlay/artifact-folders.md
  - repo-structure.yaml
  - docs/STRUCTURE.md
pending_structure_branches_checked:
  - branch: codex/commission-spine-structure
    relevant_pending_records:
      - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
      - docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md
      - docs/migration/data_capture_projection_spine_first_migration_inventory_v0.md
      - docs/migration/judgment_spine_spine_first_migration_inventory_v0.md
      - docs/migration/data_lake_spine_first_migration_inventory_v0.md
    treatment: pending_provenance_not_current_main_authority
  - branch: codex/ecr-spine-first-migration-inventory
    treatment: observed as existing structure/migration branch; not switched into
  - branch: codex/ontology-structure-migration-inventory
    treatment: observed as existing structure/migration branch; not switched into
prior_cleaning_worktree:
  path: C:/Users/vmon7/.codex/worktrees/33ea/orca
  branch_at_preflight: codex/cleaning-spine-successor-main-codex
  status: clean
  upstream: gone
  handling: left untouched
required_searches_run:
  - rg --files | rg -i "clean|cleaning|projection|residual|dedupe|normalize|classification|inclusion"
  - rg -n -i "Cleaning|cleaning spine|cleaning layer|projection|residual|dedupe|normalize|classification|inclusion state|decision-use downgrade|excluded" docs .agents orca-harness --glob "!_scratch/**" --glob "!orca-worktrees/**"
files_moved: none
code_touched: no
```

Cynefin route: `complicated`, layer-based inventory. The safe move is a
docs-only marking artifact. The disallowed moves are live file moves, code
changes, schema/runtime changes, review-bundle reclassification by relocation,
or treating pending branch records as current main authority.

## 2. Cleaning Scope Definition

Cleaning is a distinct operating layer between Capture/ECR and Judgment.

Cleaning may consume:

- raw capture anchors and source slices;
- Data Capture Projection Packet row views, receipts, loss ledgers, warnings,
  residuals, and raw anchors;
- Evidence Candidate Record receipt/read references;
- source-family adaptation notes clearly labeled as adaptation or unresolved
  candidates.

Cleaning owns:

- stable Cleaning input handles keyed to raw;
- optional projection and ECR references attached to those handles;
- non-destructive transform ledgers;
- normalization, translation, summarization, exact-identity dedupe mechanics,
  ledger propagation, residuals, warnings, omissions, and raw-pull triggers;
- raw-to-cleaned traceability.

Cleaning must not own:

- source acquisition, source access, preservation, or projection ownership
  (Capture);
- ECR/SCR source-side derived-record semantics (ECR/SCR);
- credibility, independence effects, exclusion, discounting, Signal Integrity,
  Signal Use, Decision Strength, or Action Ceiling (Judgment);
- satellite/domain interpretation; or
- runtime storage/API/schema ratification beyond separately authorized bounded
  implementation.

Short contract:

```text
Capture preserves and may project.
ECR/SCR derives source-side receipts/records.
Cleaning transforms non-destructively and keeps raw-keyed traceability.
Judgment decides what the evidence means.
```

## 3. Artifact Inventory Table

Migration marks:

- `move_now`: not used in this pass.
- `move_later`: candidate to move after the spine-first root and path grammar are
  accepted.
- `pointer_only`: keep canonical artifact elsewhere; future Cleaning spine may
  point to it.
- `do_not_move`: false positive, global artifact, copied bundle, or wrong owner.
- `historical_only`: preserve as history/archive; do not use as current
  authority.

| Current path | Artifact role | Owner / consumer | Future target path | Migration mark | Reason | Dependencies | Validation needed after move |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md` | Cleaning purpose entrypoint | Owner: Cleaning; consumers: CA, implementers, reviewers | `orca/product/spines/cleaning/README.md` | `move_later` | It is the plain-language front door for Cleaning. | Cleaning Foundation; boundary note; Projection Doctrine | Retrieval header, moved-path index, repo-map update, stale-reference search |
| `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md` | Cleaning layer contract/foundation | Owner: Cleaning; consumers: Capture, ECR, Judgment, implementation scoping | `orca/product/spines/cleaning/authority/cleaning_spine_foundation_v0.md` | `move_later` | Strongest Cleaning-owned authority candidate. | Projection Doctrine; boundary note; corroboration discipline; capture-context preservation note | Retrieval header, cross-reference rewrite, moved-path index, artifact review if ratification changes |
| `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Cross-layer boundary note | Owner: Foundation/Core boundary; consumers: Capture, ECR, Cleaning, Judgment | `orca/product/spines/foundation/cleaning/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` plus Cleaning pointer | `pointer_only` | Cleaning depends on this, but it is not Cleaning-owned. | Core product contract; IPF; ECR/JSG updates in the same file | Boundary-owner move decision, multi-spine backlink audit |
| `docs/product/core_spine_v0_projection_doctrine_v0.md` | Projection doctrine / Data Capture projection view rules | Owner: Capture projection; consumer: Cleaning | `orca/product/spines/capture/authority/projection/projection_doctrine_v0.md` plus Cleaning pointer | `pointer_only` | Projection is a Capture-owned helper; Cleaning consumes refs only. | Boundary note; source-capture projection code | Capture migration manifest, Cleaning backlink, projection stale-reference audit |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md` | Capture-context preservation note | Owner: Capture; consumer: future Cleaning/ECR | `orca/product/spines/capture/authority/core_spine_v0_data_capture_context_preservation_note_v0.md` | `pointer_only` | It controls what context Cleaning receives, not Cleaning semantics. | Capture architecture; ECR handoff | Capture move validation and Cleaning pointer |
| `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Capture architecture blueprint | Owner: Capture; consumer: Cleaning boundary | `orca/product/spines/capture/authority/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | `pointer_only` | Upstream owner of capture and projection flow. | Data Capture consolidation map | Capture migration validation |
| `docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md` | Capture intake consolidation | Owner: Capture; consumer: Cleaning | `orca/product/spines/capture/authority/data_capture_spine_intake_surface_consolidation_v0.md` | `pointer_only` | Names projection and Cleaning traceability but remains Capture. | Capture intake docs | Capture migration validation |
| `docs/product/source_capture_toolbox/retail_pdp_projection_contract_v0.md` | Retail/PDP projection contract | Owner: Capture/source-family; consumer: Cleaning adapter | `orca/product/spines/capture/authority/source_families/retail_pdp/retail_pdp_projection_contract_v0.md` | `pointer_only` | Source-family projection is upstream input to Cleaning. | Retail projection playbook; source-capture code | Capture source-family migration validation |
| `docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md` | Retail/PDP projection playbook | Owner: Capture/source-family; consumer: Cleaning adapter | `orca/product/spines/capture/workflows/projection/retail_pdp/retail_pdp_projection_playbook_v0.md` | `pointer_only` | Operational projection playbook, not Cleaning. | Retail projection contract | Capture source-family migration validation |
| `docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md` | Reddit candidate-intake projection handoff | Owner: Capture/Reddit; consumer: Cleaning only indirectly | `orca/product/spines/capture/workflows/source_families/reddit/reddit_candidate_intake_to_projection_lane_handoff_v0.md` | `pointer_only` | Candidate projection is Capture-family, not Cleaning. | Reddit candidate intake architecture | Capture migration validation |
| `docs/workflows/reddit_candidate_intake_subreddit_projection_b2b_001_closeout_v0.md` | Reddit candidate projection closeout | Owner: Capture/Reddit report | `orca/product/spines/capture/reports/source_families/reddit/reddit_candidate_intake_subreddit_projection_b2b_001_closeout_v0.md` | `pointer_only` | Historical Capture report, not Cleaning. | Candidate intake lane | Report archive/moved-path validation |
| `docs/workflows/reddit_candidate_intake_subreddit_projection_seo_002_closeout_v0.md` | Reddit candidate projection closeout | Owner: Capture/Reddit report | `orca/product/spines/capture/reports/source_families/reddit/reddit_candidate_intake_subreddit_projection_seo_002_closeout_v0.md` | `pointer_only` | Historical Capture report, not Cleaning. | Candidate intake lane | Report archive/moved-path validation |
| `docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md` | Capture/projection/storage architecture | Owner: Capture/Data Lake classification needed | `orca/product/spines/capture/authority/storage/orca_capture_projection_storage_spine_architecture_v0.md` or Data Lake pointer | `pointer_only` | Storage/projection is adjacent; do not make it Cleaning-owned. | Data Lake pending inventory; Capture projection inventory | Owner classification before move |
| `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | Cross-layer by-key mechanics map | Owner: Foundation/Data Lake; consumers: Capture, ECR/SCR, Cleaning, Judgment | `orca/product/spines/foundation/authority/core_spine_v0_data_lake_mechanics_map_v0.md` or Data Lake spine pointer | `pointer_only` | Cleaning depends on the by-key flow but does not own lake mechanics. | Data Lake inventory pending branch; ECR/SCR | Foundation/Data Lake owner decision |
| `docs/workflows/ecr_spine_submap_v0.md` | ECR/SCR route map | Owner: ECR/SCR; consumer: Cleaning/Judgment | `orca/product/spines/ecr/workflows/ecr_spine_submap_v0.md` | `pointer_only` | ECR/SCR derives source-side records; Cleaning may attach ECR refs only. | ECR plans, SCR architecture | ECR migration validation |
| `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | ECR frame/source visibility plan | Owner: ECR | `orca/product/spines/ecr/authority/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | `pointer_only` | ECR source-side integrity, not Cleaning. | ECR submap; boundary note | ECR migration validation |
| `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | ECR SP-1/2/3 source-side plan | Owner: ECR | `orca/product/spines/ecr/authority/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | `pointer_only` | Source-side derived-read semantics stay ECR. | ECR frame plan | ECR migration validation |
| `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | Signal Content Record architecture | Owner: SCR/Signal Content | `orca/product/spines/signal_content/authority/core_spine_v0_signal_content_record_architecture_v0.md` | `pointer_only` | Content deriver is sibling to ECR and upstream to Judgment, not Cleaning. | ECR/SCR submap | SCR migration validation |
| `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md` | Judgment conductor | Owner: Judgment; consumer of cleaned view | `orca/product/spines/judgment/authority/judgment_quality_promotion_operating_model_v0.md` | `pointer_only` | Judgment consumes Cleaning outputs and owns effects. | Judgment migration inventory pending branch | Judgment migration validation |
| `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` | Judgment claim-tier architecture | Owner: Judgment | `orca/product/spines/judgment/authority/judgment_spine_evidence_ladder_architecture_v0.md` | `pointer_only` | Downstream claim tier; not Cleaning. | Judgment gate map | Judgment migration validation |
| `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md` | Judgment gate ownership map | Owner: Judgment | `orca/product/spines/judgment/authority/judgment_spine_gate_ownership_map_v0.md` | `pointer_only` | Owns downstream gates after Cleaning. | Judgment evidence ladder | Judgment migration validation |
| `docs/product/search/orca_demand_read_taxonomy_v0.md` | Demand/read taxonomy mentioning cleaning labels | Owner: Search/product satellite; consumer: Cleaning labels as upstream/adaptation | `orca/product/spines/search/authority/orca_demand_read_taxonomy_v0.md` or satellite home | `pointer_only` | Satellite consumer of Cleaning-labeled surfaces; not Cleaning owner. | Search lane binding | Search/satellite migration validation |
| `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v1.md` | Cleaning architecture handoff prompt | Owner: Cleaning prompt history; consumer: future implementers | `orca/product/spines/cleaning/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v1.md` | `move_later` | Current/latest Cleaning foundation planning prompt. | Foundation; README; review context | Prompt-path rewrite, retrieval header check |
| `docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md` | Prior Cleaning architecture prompt | Owner: Cleaning prompt history | `orca/product/spines/cleaning/archive/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md` | `historical_only` | Superseded by v1 for practical routing unless owner says otherwise. | v1 prompt | Archive/moved-path validation |
| `docs/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md` | Cleaning/projection doctrine handoff prompt | Owner: Cleaning/Capture boundary prompt | `orca/product/spines/cleaning/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md` with Capture backlink | `move_later` | Cleaning-specific handoff over projection boundary. | Projection Doctrine; boundary note | Prompt-path rewrite, backlink audit |
| `docs/review-inputs/judgment_conductor_delegated_review_v0/sources/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Copied source in review bundle | Owner: review bundle; canonical owner remains boundary doc | stay in place; no Cleaning target | `do_not_move` | Copied review-input source, explicitly excluded by retrieval metadata from promotion. | Canonical boundary doc | None unless review-bundle migration exists |
| `docs/review-inputs/judgment_conductor_full_decorrelated_adversarial_review_v0/sources/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Copied source in review bundle | Owner: review bundle | stay in place; no Cleaning target | `do_not_move` | Copied source, not authority. | Canonical boundary doc | None unless review-bundle migration exists |
| `docs/review-inputs/judgment_conductor_post_patch_recheck_v0/sources/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Copied source in review bundle | Owner: review bundle | stay in place; no Cleaning target | `do_not_move` | Copied source, not authority. | Canonical boundary doc | None unless review-bundle migration exists |
| `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md` | Historical/advisory projection closeout | Owner: review output/archive | `orca/product/spines/capture/reviews/outputs/projection/projection_doctrine_v0_vendor_ca_closeout_v0.md` or global review archive | `historical_only` | Review output is input/provenance, not current Cleaning authority. | Projection Doctrine | Review archive policy before any move |
| `docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_v0.md` | Historical projection code review | Owner: Capture review output | `orca/product/spines/capture/reviews/outputs/source_families/reddit/...` or global review archive | `historical_only` | Capture projection review; not Cleaning. | Reddit candidate projection decision | Review archive policy before any move |
| `docs/review-outputs/adversarial-artifact-reviews/linkedin_live_projection_slice3b2_code_review_v0.md` | Historical LinkedIn projection review | Owner: Capture review output | `orca/product/spines/capture/reviews/outputs/source_families/linkedin/...` or global review archive | `historical_only` | Capture projection review; not Cleaning. | LinkedIn projection code | Review archive policy before any move |
| `docs/review-outputs/adversarial-artifact-reviews/linkedin_live_projection_slice3b2_code_review_v1.md` | Historical LinkedIn projection review | Owner: Capture review output | `orca/product/spines/capture/reviews/outputs/source_families/linkedin/...` or global review archive | `historical_only` | Capture projection review; not Cleaning. | LinkedIn projection code | Review archive policy before any move |
| `docs/review-outputs/linkedin_live_projection_slice3b2_v0_no_repo_review_bundle.zip` | Review bundle zip | Owner: review archive | stay in place or future review archive | `do_not_move` | Binary review bundle; not Cleaning authority. | LinkedIn review output | Review-bundle policy only |
| `docs/review-outputs/linkedin_live_projection_slice3b2_v1_no_repo_review_bundle.zip` | Review bundle zip | Owner: review archive | stay in place or future review archive | `do_not_move` | Binary review bundle; not Cleaning authority. | LinkedIn review output | Review-bundle policy only |
| `orca-harness/cleaning/__init__.py` | Cleaning package export surface | Owner: implementation/runtime; consumer: tests/future runner | `orca/product/spines/cleaning/harness/pointers/cleaning_package_exports.md` | `pointer_only` | Executable code stays in `orca-harness/` until code-root migration. | Cleaning models/core/projection | Code-root decision plus tests if ever moved |
| `orca-harness/cleaning/models.py` | Cleaning Pydantic model substrate | Owner: implementation/runtime; consumer: Cleaning package | `orca/product/spines/cleaning/harness/pointers/cleaning_models.md` | `pointer_only` | Code/runtime surface; do not move in docs-only pass. | Foundation; pyproject package registration | Unit tests and import-path audit if ever moved |
| `orca-harness/cleaning/core.py` | Cleaning exact-identity mechanics | Owner: implementation/runtime | `orca/product/spines/cleaning/harness/pointers/cleaning_core.md` | `pointer_only` | Code/runtime surface; do not move in docs-only pass. | Cleaning models | Unit tests and import-path audit if ever moved |
| `orca-harness/cleaning/projection.py` | Projection-to-Cleaning adapter | Owner: implementation/runtime; consumes Capture projection packets | `orca/product/spines/cleaning/harness/pointers/projection_adapter.md` | `pointer_only` | Code/runtime surface and cross-spine adapter; keep in harness. | Capture projection modules; Cleaning models | Unit tests and import-path audit if ever moved |
| `orca-harness/tests/unit/test_cleaning_core.py` | Cleaning core unit tests | Owner: implementation/runtime tests | `orca/product/spines/cleaning/tests/pointers/test_cleaning_core.md` | `pointer_only` | Executable tests stay in `orca-harness/tests/`. | Cleaning models/core | Test suite if code-root migration occurs |
| `orca-harness/tests/unit/test_cleaning_projection_integration.py` | Projection-to-Cleaning integration tests | Owner: implementation/runtime tests | `orca/product/spines/cleaning/tests/pointers/test_cleaning_projection_integration.md` | `pointer_only` | Executable tests stay in `orca-harness/tests/`. | Reddit and Retail projection builders | Test suite if code-root migration occurs |
| `orca-harness/pyproject.toml` | Package registration includes Cleaning | Owner: harness/runtime packaging | `orca/product/spines/cleaning/harness/pointers/package_registration.md` | `pointer_only` | Runtime packaging surface; not a docs artifact. | `orca-harness/cleaning/` | Packaging/import validation if code-root migration occurs |
| `orca-harness/source_capture/reddit_projection.py` | Reddit raw-packet projection code | Owner: Capture/source_capture runtime; consumer: Cleaning adapter | `orca/product/spines/capture/harness/pointers/projection/reddit_projection.md` | `pointer_only` | Upstream projection producer; not Cleaning. | Reddit projection tests | Capture code-root decision and tests |
| `orca-harness/source_capture/retail_pdp_projection.py` | Retail/PDP raw-packet projection code | Owner: Capture/source_capture runtime; consumer: Cleaning adapter | `orca/product/spines/capture/harness/pointers/projection/retail_pdp_projection.md` | `pointer_only` | Upstream projection producer; not Cleaning. | Retail projection tests | Capture code-root decision and tests |
| `orca-harness/source_capture/ig_projection.py` | IG projection code | Owner: Capture/source_capture runtime | `orca/product/spines/capture/harness/pointers/projection/ig_projection.md` | `pointer_only` | Upstream projection producer; Cleaning-adjacent only. | IG projection tests | Capture code-root decision and tests |
| `orca-harness/runners/run_retail_pdp_projection.py` | Retail projection runner | Owner: Capture runtime | `orca/product/spines/capture/harness/pointers/runners/run_retail_pdp_projection.md` | `pointer_only` | Runtime runner; not Cleaning. | Retail projection code | Capture code-root decision and tests |
| `orca-harness/runners/run_ig_creator_momentum_projection.py` | IG projection runner | Owner: Capture runtime | `orca/product/spines/capture/harness/pointers/runners/run_ig_creator_momentum_projection.md` | `pointer_only` | Runtime runner; not Cleaning. | IG projection code | Capture code-root decision and tests |
| `orca-harness/capture_spine/reddit_candidate_intake/projection.py` | Candidate-row projection helper | Owner: Capture Spine runtime | `orca/product/spines/capture/harness/pointers/candidate_projection/reddit_candidate_intake_projection.md` | `pointer_only` | Candidate projection is Capture, not Cleaning. | Candidate intake models/tests | Capture code-root decision and tests |
| `orca-harness/capture_spine/linkedin_live_adapter/projection.py` | LinkedIn candidate-row projection helper | Owner: Capture Spine runtime | `orca/product/spines/capture/harness/pointers/candidate_projection/linkedin_live_projection.md` | `pointer_only` | Candidate projection is Capture, not Cleaning. | LinkedIn adapter tests | Capture code-root decision and tests |
| `orca-harness/tests/unit/test_reddit_projection.py` | Reddit projection tests | Owner: Capture tests; consumer: Cleaning adapter test | `orca/product/spines/capture/tests/pointers/projection/test_reddit_projection.md` | `pointer_only` | Upstream projection tests, not Cleaning. | Reddit projection code | Capture code-root decision and tests |
| `orca-harness/tests/unit/test_retail_pdp_projection.py` | Retail/PDP projection tests | Owner: Capture tests; consumer: Cleaning adapter test | `orca/product/spines/capture/tests/pointers/projection/test_retail_pdp_projection.md` | `pointer_only` | Upstream projection tests, not Cleaning. | Retail projection code | Capture code-root decision and tests |
| `orca-harness/tests/unit/test_source_capture_ig_projection.py` | IG projection tests | Owner: Capture tests | `orca/product/spines/capture/tests/pointers/projection/test_source_capture_ig_projection.md` | `pointer_only` | Upstream projection tests, not Cleaning. | IG projection code | Capture code-root decision and tests |
| `orca-harness/cases/product_learning/**/source_captures/*clean*/**` | Raw case capture paths containing product names such as clean mascara/cleanser | Owner: case/source-capture artifacts | stay in case/source-capture homes | `do_not_move` | Word "clean" is product/source text, not Cleaning Spine. | Case manifests and raw artifacts | None for Cleaning migration |
| `docs/hygiene/repo_cleanup_pass_2026_06_v0.md` | Repo cleanup/hygiene note | Owner: repo hygiene | stay in `docs/hygiene/` | `do_not_move` | "cleanup" is hygiene, not Cleaning Spine. | Hygiene queue | None for Cleaning migration |
| `docs/prompts/handoffs/repo_wide_hygiene_cleanup_lane_handoff_prompt_v0.md` | Repo cleanup handoff prompt | Owner: repo hygiene/prompt | stay in handoff archive unless hygiene migration says otherwise | `do_not_move` | False positive for Cleaning. | Hygiene lane | None for Cleaning migration |
| `docs/review-outputs/adversarial-artifact-reviews/demand_projection_*` and `docs/review-inputs/demand_projection_*` | Demand projection review artifacts | Owner: demand/search/product review | future demand/search review archive, not Cleaning | `do_not_move` | "Projection" here is demand analysis, not source projection or Cleaning. | Search/product lanes | Demand/search migration only |

## 4. Boundary Map: Capture -> ECR/SCR -> Cleaning -> Judgment

```text
Decision Frame
  -> Capture
       preserves raw, source identity, timing, visibility, context
       may create Data Capture Projection Packet row views
       owns source-family projection contracts
  -> ECR/SCR
       derives source-side receipt/integrity/content records
       carries or residualizes, never authors from prose
       remains keyed to captured packet/slice
  -> Cleaning
       consumes raw-keyed handles with optional projection/ECR refs
       writes non-destructive transform ledgers
       normalizes/translates/summarizes/exact-dedupes mechanically
       preserves raw-pull triggers and warnings
  -> Judgment
       decides credibility, independence, inclusion/exclusion effect,
       signal use, strength, action ceiling, and outcome-relevant meaning
```

Boundary rules for future placement:

- Do not merge Cleaning with Capture. Capture can project; Cleaning consumes
  projection refs and verifies traceability.
- Do not merge Cleaning with ECR/SCR. ECR/SCR derive source-side records;
  Cleaning transforms working material and records mechanics.
- Do not merge Cleaning with Judgment. Judgment evaluates; Cleaning prepares and
  qualifies evidence mechanically.
- Do not treat Projection as a standalone spine. Existing and pending sources
  classify it as a Capture-owned helper.
- Do not promote copied review-input source files into authority by moving them.

## 5. Consumer Map

| Consumer | What it needs from Cleaning | Future pointer from Cleaning spine |
| --- | --- | --- |
| Capture / Projection | Traceability checks, raw-pull triggers, evidence-row preservation feedback | `capture/authority/projection/` backlink to Cleaning README/foundation |
| ECR/SCR | Optional ECR refs on Cleaning handles and warning propagation | `ecr/workflows/ecr_spine_submap_v0.md` pointer from Cleaning `authority/` |
| Judgment | Cleaned working view, transform ledger, warnings, residuals, raw-pull triggers | Judgment conductor and gate maps point to Cleaning `authority/` |
| Search / demand satellites | Mechanically cleaned or labeled input surfaces without Judgment effects | Satellite pointer to Cleaning source-family adaptation boundary |
| Harness/runtime | Pydantic models, exact-identity mechanics, projection-to-cleaning adapter | Spine-local `harness/pointers/`, not code moves |
| Review lanes | Auditable sources for adversarial review of Cleaning artifacts | Spine-local review folder only after review-bundle policy exists |

## 6. Future-Home Recommendation

Evaluate the requested candidate homes:

| Candidate | Verdict | Reason |
| --- | --- | --- |
| `orca/product/spines/cleaning/` | Recommended future primary home | Current sources show Cleaning owns a distinct operating layer: its own allowed transforms, ledger contract, raw-keyed handle contract, source-family adaptation boundary, and Judgment consumer contract. |
| `orca/product/spines/foundation/cleaning/` | Use only for cross-spine boundary material | The data/cleaning boundary and data-lake mechanics maps are Foundation/Core-adjacent. They should be pointed to by Cleaning, not swallowed by Cleaning. |
| `orca/product/shared/cleaning/` | Not recommended as primary home | "Shared" understates that Cleaning is a pipeline stage with ownership and downstream consumers. It can host shared concepts only if a later structure decision creates shared utilities. |
| `orca/product/substrates/cleaning/` | Not recommended under current source evidence | "Substrate" fits the thin code/model core, but the product layer is broader than substrate: it includes source-family adaptation rules, ledgers, raw-pull triggers, and handoff contracts. |

Recommendation: Cleaning should be a spine, not merely a shared substrate.

Proposed future skeleton, after root binding acceptance:

```text
orca/product/spines/cleaning/
  README.md
  spine.yaml
  authority/
    cleaning_spine_foundation_v0.md
  prompts/
    handoffs/
  workflows/
  reviews/
  reports/
  harness/
    pointers/
  tests/
    pointers/
  migrations/
  archive/
```

## 7. Do-Not-Move List

Do not move in a Cleaning migration:

- `orca-harness/cleaning/**` code in this docs-only pass. Future Cleaning spine
  may add pointer docs, but executable code stays in `orca-harness/` until a
  separate code-root migration is accepted.
- `orca-harness/tests/unit/test_cleaning_*.py` tests in this docs-only pass.
- Capture projection code and tests under `orca-harness/source_capture/`,
  `orca-harness/capture_spine/`, and `orca-harness/runners/`.
- Copied review-input source files under `docs/review-inputs/**/sources/`.
- Binary review bundles under `docs/review-outputs/**/*.zip`.
- Product-learning raw capture paths where "clean" is part of the product or
  source name, such as mascara/cleanser captures.
- Repo cleanup and hygiene prompts that match `clean` only as English
  "cleanup".
- Demand-projection review artifacts that use "projection" in an analytical
  demand sense, not Capture projection or Cleaning.
- Historical review outputs as current authority. They may be archived by a
  review migration, but they do not define Cleaning's live home.

## 8. Migration Sequence

1. Do not move anything from this inventory.
2. Accept or amend the pending spine-first proposal, or create an equivalent
   current-main structure decision.
3. Update binding surfaces before any live `orca/product/spines/cleaning/`
   directory exists:
   - `docs/decisions/orca_repo_structure_binding_v0.md`
   - `.agents/workflow-overlay/artifact-folders.md`
   - `repo-structure.yaml`
   - `docs/STRUCTURE.md`
   - `docs/workflows/orca_repo_map_v0.md`
   - placement-checker expectations if the new root/path grammar is enforced.
4. Create a Cleaning spine skeleton with `README.md`, `spine.yaml`,
   `authority/`, `prompts/`, `harness/pointers/`, `tests/pointers/`, and
   `migrations/`.
5. Move Cleaning-owned docs first:
   - README to `orca/product/spines/cleaning/README.md`;
   - foundation to `authority/`;
   - Cleaning handoff prompts to `prompts/handoffs/` or `archive/` by status.
6. Add pointers, not moves, for Capture projection, ECR/SCR, Foundation
   boundary docs, Judgment consumers, and `orca-harness/` code/tests.
7. Write a moved-path index and update only live navigation surfaces.
   Historical records keep old paths unless a later migration authorizes a
   historical rewrite.
8. Run placement, retrieval-header, repo-map freshness, and diff-hygiene checks.
   Run tests only if code/test files move or code-root pointers become
   executable behavior.
9. Migrate review outputs only after a review-specific archive/bundle policy
   exists.

## 9. Open Questions

- Will the pending spine-first proposal be accepted, amended, or replaced?
- If a Foundation spine exists, should cross-layer boundary material live under
  `orca/product/spines/foundation/cleaning/` or under a generic Foundation
  `authority/` folder with Cleaning backlinks?
- Is the Cleaning Foundation still a draft (`FOUNDATION_DRAFT_FROM_PROJECTION_CANDIDATE`)
  when migration happens, or will owner ratification change the target role?
- Should source-family adaptation notes live under Cleaning or remain in
  Capture/satellite homes with Cleaning pointers?
- What is the durable rule for historical review-output migration into
  spine-local `reviews/` folders versus a global review archive?
- When, if ever, does `orca-harness/cleaning/` move to a product-spine code root?
- Should `spine.yaml` carry owner/consumer contracts for raw-keyed handles,
  projection refs, and ECR refs, or only point to authority docs?

## 10. Non-Claims

This inventory is not validation, readiness, product proof, schema
ratification, runtime authorization, implementation authorization, permission
to move files, a move manifest, code-root migration approval, review-bundle
policy, or source-of-truth promotion.

It does not authorize creating `orca/product/spines/cleaning/`. It only marks
where Cleaning-related artifacts should go if a later accepted structure
decision makes that root live.
