# Orca Repo Map v0

```yaml
retrieval_header_version: 1
artifact_role: Repository map
scope: Compact navigation map for Orca source loading and prompt setup.
use_when:
  - Choosing a bounded source pack before a CA prompt, review prompt, or product artifact.
  - Orienting a new thread without bulk-loading the repository.
  - Deciding which product, prompt, review, research, or workflow files are adjacent to a task.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
stale_if:
  - New top-level docs folders are added.
  - Core Spine, Data Capture Spine, Cleaning Spine, Judgment Spine, offer, proof, or prompt families are materially reorganized.
  - .agents/workflow-overlay/source-of-truth.md changes source hierarchy or the doctrine-change propagation contract.
  - A later repo-map artifact supersedes this file.
```

- Status: PROPOSED_MAP
- Artifact type: Workflow navigation artifact
- Scope: Repo navigation and source-pack selection
- Refreshed: 2026-05-25
- Implementation authorized: no

## How To Use This Map

Use this map to choose files. Do not treat it as product authority.

For source precedence, open `.agents/workflow-overlay/source-of-truth.md`.
For source-loading budgets, open `.agents/workflow-overlay/source-loading.md`.
For artifact retrievability, body-opening shape, stale/recheck patterns, and
temporary-artifact anti-rot guidance, open
`docs/workflows/artifact_retrievability_guide.md`.

Start-route cue: when a task may change product doctrine, architecture
doctrine, workflow authority, validation philosophy, review authority, output
authority, or a lifecycle boundary, open the Doctrine Change Propagation
Contract in `.agents/workflow-overlay/source-of-truth.md` before selecting
downstream surfaces. Use this map to identify likely downstream surfaces; do not
treat the map itself as propagation evidence.

## Top-Level Structure

| Path | Role |
| --- | --- |
| `AGENTS.md` | Workspace instructions and Orca project operating constraints. |
| `.agents/workflow-overlay/` | Orca overlay authority for project facts, folders, source rules, prompt rules, validation, safety, and review lanes. |
| `docs/decisions/` | Decision records. |
| `docs/product/` | Product contracts, Core Spine artifacts, proof plans, source/evidence standards, offer, buyer-proof, and decision artifacts. |
| `docs/prompts/` | Prompt artifacts, wrappers, reruns, reviews, and local templates. |
| `docs/research/` | Research artifacts and consulting-judgment corpus material. |
| `docs/review-inputs/` | Prepared review inputs. |
| `docs/review-outputs/` | Review reports and adversarial artifact reviews. |
| `docs/workflows/` | Workflow records, operational notes, and repo maps. |
| `docs/migration/` | Import and migration records. |
| `docs/hygiene/` | Triage and cleanup queues. |
| `docs/_inbox/` | Non-authoritative scratch and parked material. |

## Overlay Files

| Path | Use for |
| --- | --- |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule. |
| `.agents/workflow-overlay/project-authority.md` | Project identity, stage, and forbidden drift. |
| `.agents/workflow-overlay/source-of-truth.md` | Source precedence, conflict rules, and doctrine-change propagation contract. |
| `.agents/workflow-overlay/source-loading.md` | Read packs, context budgets, and prompt source capsules. |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted artifact folders and folder rules. |
| `.agents/workflow-overlay/artifact-roles.md` | Artifact role bindings and permissions. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract. |
| `.agents/workflow-overlay/prompt-orchestration.md` | Prompt artifact, wrapper, preflight, and rerun rules. |
| `.agents/workflow-overlay/template-registry.md` | Orca-local prompt template registry. |
| `.agents/workflow-overlay/product-proof.md` | Buyer-proof semantics and non-claims. |
| `.agents/workflow-overlay/communication-style.md` | Orca response style. |
| `.agents/workflow-overlay/validation-gates.md` | Validation gate expectations. |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules. |
| `.agents/workflow-overlay/safety-rules.md` | Safety and forbidden drift. |
| `.agents/workflow-overlay/skill-adoption.md` | Skill source and adoption status. |

## Workflow Navigation Files

| Path | Use for |
| --- | --- |
| `docs/workflows/artifact_retrievability_guide.md` | Operational guidance for durable artifact headers, body-opening source surfaces, stale/recheck patterns, repo-map/index treatment, report-only retrieval checks, and hygiene anti-rot. |
| `docs/workflows/orca_repo_map_v0.md` | Compact navigation map for bounded source-pack selection and prompt setup. |

## Product Anchor Files

Use these before broad product architecture or CA setup:

| Path | Use for |
| --- | --- |
| `docs/decisions/turn_08_product_thesis_v0.md` | Orca thesis, value proposition, strategic center, broad product boundary. |
| `docs/product/orca_offer_hypothesis_v0.md` | Offer hypothesis, buyer-facing language, first proof offer, ICP boundary. |
| `docs/product/orca_buyer_proof_packet_v0.md` | First buyer-proof packet, proof gates, pull signals, kill/graduation criteria. |
| `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` | Selected first ICP wedge and decision-family focus. |
| `docs/product/orca_product_proof_lead_charter_v0.md` | Product proof lead role and proof execution boundary. |

## Core Spine Files

| Path | Use for |
| --- | --- |
| `docs/product/core_spine_v0_product_contract.md` | Core Spine product contract and eight primitives. |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | Manual information-production foundation and Evidence Unit standard. |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Data Capture/Cleaning/Judgment boundary and Evidence Candidate Record setup context. |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Data Capture Spine architecture blueprint for commissioned capture, core/satellite boundary, and rejected patterns. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Draft Data Capture Spine v0 obligation contract for setup and pressure testing. |
| `docs/product/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md` | Planning-only fixture architecture for remaining Data Capture pressure tests and stop condition. |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md` | Navigation and status-use note for the Data Capture pressure-test synthesis after optional adversarial clarifications. |
| `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md` | Full Data Capture pressure-test synthesis across planned fixtures; advisory baseline candidate, not acceptance or completion. |
| `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md` | Context-preservation note for threaded, review, docs/changelog, domain-language, human-assisted, and archive/history capture. |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` | Data Capture pressure fixture for threaded forum and package/segmentation capture using Reddit API/data pricing. |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md` | Data Capture pressure fixture for public-sector package/bundle capture using Milwaukee fiscal-crossroads material. |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` | Data Capture pressure fixture for review-surface capture using ClickUp Trustpilot/G2 material. |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` | Data Capture pressure fixture for docs/changelog/versioned-page capture using Kubernetes v1.32 docs. |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` | Data Capture pressure fixture for archive/history and recapture using Unity Runtime Fee material. |
| `docs/product/engagement_logic_registry_v0.md` | Signal-use and engagement interpretation registry. |
| `docs/product/core_spine_v0_proof_protocol_v0.md` | Core proof protocol. |
| `docs/product/core_spine_v0_proof_input_selection_v0.md` | Proof input-selection rules. |
| `docs/product/core_spine_v0_proof_packet_preflight_v0.md` | Proof packet preflight. |
| `docs/product/core_spine_v0_proof_case_selection_brief_v0.md` | Proof case-selection brief. |

## Method Validation And Replay Files

Use only when method-validation history, replay evidence, or case-frame locks
are directly relevant. Do not include by default in Data Capture Spine CA prompts.

Key files:

- `docs/product/core_spine_v0_method_validation_replay_packet_v0.md`
- `docs/product/core_spine_v0_method_validation_rubric_v0.md`
- `docs/product/core_spine_v0_method_validation_case_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md`

## First Proof And Discovery Files

Use for customer discovery, target selection, first proof packet prep, or live
proof readiness questions.

Key files:

- `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`
- `docs/product/core_spine_v0_first_proof_run_charter_v0.md`
- `docs/product/core_spine_v0_first_proof_run_locks_v0.md`
- `docs/product/core_spine_v0_first_proof_run_packet_v0.md`
- `docs/product/core_spine_v0_first_proof_run_jb_client0_slice_v0.md`
- `docs/product/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md`
- `docs/product/core_spine_v0_first_proof_run_sh01_shadow_slice_v0.md`
- `docs/product/orca_discovery_batch_0_target_selection_brief_v0.md`
- `docs/product/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md`
- `docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md`

## Backtest Specimens

Use when the task is specifically about historical cutoff discipline or the
Unity runtime-fee specimen:

- `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`

## Prompt Families

| Path | Use for |
| --- | --- |
| `docs/prompts/product-planning/` | Product planning prompt drafts. |
| `docs/prompts/feature-planning/` | Feature planning prompt drafts. |
| `docs/prompts/deep-thinking/` | Deep reasoning prompt drafts. |
| `docs/prompts/handoffs/` | Handoff prompt drafts. |
| `docs/prompts/reviews/` | Review prompts. |
| `docs/prompts/reruns/` | Rerun prompts. |
| `docs/prompts/patches/` | Patch prompts. |
| `docs/prompts/wrappers/` | Thin wrapper prompts. |
| `docs/prompts/templates/` | Local prompt templates. |
| `docs/prompts/hygiene-queue/` | Current drift/parking area; not listed as an accepted prompt-family folder in the overlay. |

## Research And Review Areas

| Path | Use for |
| --- | --- |
| `docs/research/consulting-judgment-corpus/` | Consulting-judgment corpus, prompts, lane outputs, synthesis, candidate screens, backtestability, and reject patterns. |
| `docs/research/judgment-spine/` | Judgment Spine parent contract, manifest, case indexes, and case-learning artifacts for consultant-grade decision judgment. |
| `docs/review-outputs/adversarial-artifact-reviews/` | Adversarial artifact review reports. |
| `docs/review-outputs/method-validation/` | Method-validation review outputs. |
| `docs/review-outputs/proof/` | Proof review outputs. |

## Inbox Warning

`docs/_inbox/` is non-authoritative. It currently contains contaminated
method-validation replay outputs and compacted-run material. Do not read or
promote those files unless the task explicitly concerns contamination,
recovery, hygiene, or comparison against canonical promoted files.

## Recommended Read Packs

### Data Capture Spine Setup CA

Use the canonical read-pack rule in
`.agents/workflow-overlay/source-loading.md#data-capture-spine-ca-read-pack`.
This map is only a navigation aid and must not fork the Data Capture Spine
source-loading rule.

Navigation pointers for that pack live in the Product Anchor Files and Core
Spine Files sections above. Do not read the target files in full by default.
Use the targeted sections named by `source-loading.md`, then expand only when a
concrete source gap could change the Data Capture Spine CA prompt.

Exclude by default:

- method-validation replays;
- first proof run packets;
- review outputs;
- research corpus;
- `docs/_inbox/`.

### Data Capture Setup / Pressure-Test Packet

Use this packet when continuing Data Capture Spine setup, obligation-contract
pressure testing, or source-family fixture checks. This is a navigation pointer
only; it does not claim that Data Capture Spine is closed, source-of-truth
promoted, accepted, formally validated, ready for ECR/Cleaning handoff,
implementation-ready, runtime-ready, or Cleaning-complete.

Start with:

- `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md`

Current pressure-test or setup handoffs should pin a freshly computed hash of
the obligation contract. The last reported working hash for the contract was
`A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF`, but
receiving lanes should recompute it before strict source-pinning claims.

Current post-clarification synthesis hash was last reported as
`46103142927A7EA7A4B61F10E0EF029614814F36438F4359C4B69B838E6C6126`. The
pressure-test synthesis usage note hash was last reported as
`7A5C5B26AA6F95C99428D7C7EB5014FD172E47DF57BFC2D92C68A1994DECAE29`. Recompute
before strict claims.

Note: older fixture headers and the adversarial review may reference earlier
synthesis or contract hashes. Treat those as historical provenance unless the
receiving lane is explicitly reviewing that older state. The adversarial review
is useful for rationale and optional clarification findings, but it reviewed
the pre-clarification synthesis hash recorded inside that report.

### Offer Or Buyer Proof Work

Start with:

- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`
- `.agents/workflow-overlay/product-proof.md`

### Core Spine Evidence Standard Work

Start with:

- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/engagement_logic_registry_v0.md`
- nearest boundary or proof artifact named by the request.

### Prompt Or Review Prompt Work

Start with:

- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/template-registry.md`
- relevant prompt template under `docs/prompts/templates/`
- the target source artifact being prompted or reviewed.

## New Thread Guidance

Use a new thread or compact handoff when the next task needs more than one
recommended read pack, more than six full artifacts, or both repo-map refresh
and CA prompt drafting. The handoff should cite this map, the source-loading
overlay, the target read pack, and the files excluded by default.

## Not-Proven Boundaries

This map does not prove acceptance, validation, readiness, buyer pull,
implementation authorization, source correctness, or freshness of every listed
artifact. Check the target artifact, retrieval header, and current `git status`
before strict claims.
