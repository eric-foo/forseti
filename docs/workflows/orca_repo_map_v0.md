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
  - New top-level folders (under the repo root or docs/) are added.
  - orca-harness/ packages, adapters, runners, fixtures, or its build authorizations are added or reorganized.
  - Core Spine, Data Capture Spine, Cleaning Spine, Judgment Spine, offer, proof, or prompt families are materially reorganized.
  - .agents/workflow-overlay/source-of-truth.md changes source hierarchy or the doctrine-change propagation contract.
  - A later repo-map artifact supersedes this file.
```

- Status: PROPOSED_MAP
- Artifact type: Workflow navigation artifact
- Scope: Repo navigation and source-pack selection
- Refreshed: 2026-06-03
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
downstream surfaces. That contract owns primary `trigger` plus
`related_triggers` grammar for multi-dimensional doctrine changes. Use this map
to identify likely downstream surfaces; do not treat the map itself as
propagation evidence.

## Top-Level Structure

| Path | Role |
| --- | --- |
| `AGENTS.md` | Workspace instructions and Orca project operating constraints. |
| `.agents/workflow-overlay/` | Orca overlay authority for project facts, folders, source rules, prompt rules, validation, safety, and review lanes. |
| `orca-harness/` | Bounded authorized implementation backing Data Capture source acquisition and the v0.14 Judgment Harness (capture adapters, source-observability, schemas, scoring, runners, fixtures, tests). Navigation context only; not runtime, acceptance, or readiness. See the Orca Harness section. |
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
| `slot1_*` / `slot2_*` `_CAPTURE_operator_workfile.md` (repo root) | Loose Data Capture pressure-test operator workfiles parked at the repo root; un-triaged drift, not authoritative. Route through `docs/hygiene/queue.md`. |

## Overlay Files

| Path | Use for |
| --- | --- |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule. |
| `.agents/workflow-overlay/project-authority.md` | Project identity, stage, and forbidden drift. |
| `.agents/workflow-overlay/source-of-truth.md` | Source precedence, conflict rules, and doctrine-change propagation contract, including primary and related trigger grammar. |
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

## Orca Harness

`orca-harness/` is bounded, authorized implementation backing Data Capture
source acquisition and the v0.14 Judgment Harness. It is navigation context
here, not a runtime, acceptance, or readiness claim. Build scope is controlled
by the authorization decisions named below; surfaces outside them (production
runtime, API/commercial fetch, anti-detect, proxy, ECR, Cleaning, Judgment
design) remain gated.

| Path | Use for |
| --- | --- |
| `orca-harness/source_capture/` | Source-capture packet core: models, writer, CLI support, and plaintext receipts. |
| `orca-harness/source_capture/adapters/` | Bounded capture adapters (direct HTTP, media/asset, Archive.org, browser snapshot, authenticated browser); not scraper frameworks, API SDKs, proxies, or anti-detect. |
| `orca-harness/source_observability/` | Local operator-record posture checker and limitation reporter. |
| `orca-harness/schemas/` | Pydantic v2 models for cases, judgments, scoring, and probes (v0.14). |
| `orca-harness/scoring/` | Deterministic band scorer and mapping table (v0.14 Step A); not judgment-quality proof. |
| `orca-harness/reports/` | Report-rendering code (case and source-observability reports); generated dry-run outputs under it are gitignored. |
| `orca-harness/runners/` | CLI entrypoints for case runs, memorization probe, source-capture packets, and source-observability reports. |
| `orca-harness/cases/` | Tracked deterministic fixture case(s) (e.g. TR/Casetext v0.14) with evidence, packet, and ledger; generated `scores/` and run outputs are gitignored. |
| `orca-harness/config/` | Static YAML config (contestants, models, prompts) consumed by runners. |
| `orca-harness/docs/` | Harness operating docs: source-capture packet and agent runbook, source-observability record guide, and scalability note. |
| `orca-harness/tests/` | `unit/`, `contract/`, and `integration/` tests, including no-LLM-import and no-tools contract guards. |
| `orca-harness/harness_utils.py`, `Makefile`, `pyproject.toml` | Shared utilities, dev shortcuts, and package metadata (optional `[browser]` Playwright extra). |

Controlling build authority:
`docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
(source-capture toolbox) and
`docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md`
(local source-observability support).

Generated/gitignored scratch — do not enumerate or treat as authoritative:
`orca-harness/_test_runs/`, `_auth_state/`, `pytest_*` temp dirs,
`reports/source_observability/*_dry_run.*`, `cases/*/*/scores/`, and
`memory/logs/`.

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
| `docs/product/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | Proposed Core Spine design note on placing independent-corroboration vs artificial-amplification discipline across the Cleaning/Judgment boundary; proposed, not validated. |
| `docs/product/judgment_spine_evidence_ladder_architecture_v0.md` | Judgment Spine claim-tier architecture separating Product-Learning, Buyer-Proof, and Judgment-Quality evidence and promotion gates. |
| `docs/product/judgment_spine_gate_ownership_map_v0.md` | Case-agnostic Judgment Spine gate ownership map for source identity, packet freeze, no-tools isolation, memorization probe, sealed output, scoring, reveal/calibration, claim classification, and closeout blockers before stronger claims. |
| `docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md` | Case-agnostic JSG-08 owner contract for reveal-only, qualitative calibration, score-linked calibration, contaminated, or absent outcome reveal/calibration receipts. |
| `docs/product/judgment_quality_promotion_operating_model_v0.md` | Case-agnostic conductor that sequences Judgment Spine gates JSG-01 to JSG-10 with mechanical receipt predicates, total fail/blocked transitions, a by-hand isolation cap, and named run lifecycle states; routes and verifies receipts, does not compute judgment quality. |
| `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` | Daimler advisory claim-tier classification decision recording the current no-durable-evidence state, required product-learning receipt before any evidence claim, and blocked buyer-proof/judgment-quality claims. |
| `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md` | Commissioner classification for the first N=3 Data Capture pressure-test batch: patchable, not architecture-threatening; docs-only patch planning authorized, not contract hardening or runtime/source-system work. |
| `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md` | Owner decision accepting the minor-patched post-batch Data Capture patch plan for downstream docs-only obligation-contract and source-access method patch drafts; not contract hardening or implementation authority. |
| `docs/product/data_capture_spine_post_batch_patch_plan_v0.md` | Docs-only post-batch Data Capture patch plan sequencing contract candidates, source-access refinements, MSP next gate, checker refinements, and owner gate; accepted by owner decision for downstream docs-only patch drafts, not direct contract hardening authority. |
| `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md` | Docs-only obligation-contract patch proposal for discharge vocabulary, Obligation #6, Obligation #16, and checker-adjacent wording after the N=3 pressure-test batch; patched after adversarial review for owner-decision input, not contract amendment. |
| `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md` | Owner decision that accepted PCP-01 through PCP-08 for bounded Data Capture obligation-contract amendment drafting; now consumed by the amended controlling obligation contract; not runtime/source-system authorization. |
| `docs/product/data_capture_spine_intake_surface_consolidation_v0.md` | Accepted bounded pressure-test target for Raw Capture, optional Mechanical Source Projection, categorical ECR receipt, and Cleaning handoff. |
| `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md` | Owner authorization for the bounded first three-slot Data Capture pressure-test execution batch; not runtime, tooling, or downstream design authorization. |
| `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md` | All-slot synthesis of the first Data Capture pressure-test batch; classifies recurring source-observability pressure as patchable on this record and routes the next bounded owner decision, not validation or implementation authority. |
| `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md` | Closeout synthesis for the first Data Capture pressure-test foundation after Slot 3 recapture and Source Observability support closeout; records the foundation as good enough for bounded next planning, not validation, readiness, contract hardening, or implementation authority. |
| `docs/product/source_capture_toolbox/README.md` | Product-facing entrypoint and folder convention for the Source Capture Toolbox; indexes controlling authority, component responsibilities, build order, and current gaps without authorizing deferred adapters or downstream-spine design. |
| `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` | Architecture boundary for a read-only Source Quality State Assembler over already-bounded source-quality rows and existing Source Capture Packets; state census only, not source discovery, runner dispatch, source-quality scoring, fixture admission, or Judgment authority. |
| `docs/product/source_capture_toolbox/source_capture_toolbox_agent_usability_dry_run_closeout_v0.md` | Closeout note for the Canoo/Walmart fresh-agent Source Capture Toolbox dry run; records agent-usability signal, runbook lessons, and the distinction between toolbox usability and source-quality improvement. |
| `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` | Owner authorization for bounded first-tranche Data Capture source-access tooling builds: Source Capture Packet core/CLI, direct HTTP, media/asset preservation, Archive.org availability/body retrieval, and honest browser snapshot support; not API, commercial fetch, anti-detect, proxy, production runtime, ECR, Cleaning, or Judgment authorization. |
| `docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md` | Owner authorization for one bounded docs-only source-observability requirements scoping lane after the all-slot pressure-test synthesis; not source-access implementation, runtime/tooling, contract hardening, or downstream ECR/Cleaning/Judgment design. |
| `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md` | Candidate source-observability requirements and owner-decision queue from the all-slot pressure-test batch; decision input only, not implementation authority or governing doctrine. |
| `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md` | Current post-Slot-3-recapture Source Observability requirements boundary decision: RQ-01/RQ-03/RQ-05 carry forward, RQ-02 is split, RQ-04 remains deferred candidate context; not implementation or source-access method authority. |
| `docs/decisions/data_capture_spine_source_observability_requirements_support_implementation_scoping_authorization_v0.md` | Owner authorization for one bounded implementation-scoping lane for post-Slot-3-recapture Source Observability requirements support: RQ-01/RQ-03/RQ-05 plus RQ-02 visibility-only; not implementation execution, RQ-04/source-access handling, method-plan amendment, or contract hardening. |
| `docs/decisions/data_capture_spine_source_observability_local_support_implementation_scoping_authorization_v0.md` | Owner authorization for one bounded implementation-scoping lane for local source-observability support; not implementation execution, source-access method work, archive/media retrieval, contract hardening, or downstream ECR/Cleaning/Judgment design. |
| `docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md` | Owner authorization and durable trace for bounded local source-observability support implementation execution; limited to operator-record model/checker/report runner/docs/tests, not source acquisition, archive/media retrieval, browser automation, contract hardening, or downstream ECR/Cleaning/Judgment design. |
| `docs/decisions/data_capture_spine_source_observability_support_closeout_decision_v0.md` | Closeout decision that the updated local source-observability helper was sufficient for the current post-recapture Slot 3 support use case without schema or code expansion; leaves only a later candidate helper-semantics vocabulary patch if repeated friction recurs. |
| `docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md` | Slot 3 Reddit sub-batch control note recording Reddit batch checker outcomes, source-language-anchor capture lesson, visible media/cutoff limitations, and the open WSO-run versus WSO-defer decision before cross-venue synthesis. |
| `docs/product/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md` | Combined first-pass Slot 3 Reddit + WSO Data Capture handoff posture; categorical ECR handoff with visible venue-specific limitations, not pressure-test discharge. |
| `docs/product/data_capture_source_access_boundary_decision_v0.md` | Current Data Capture source-access boundary: discoverable-or-entitled, free/account-created access allowed, paid/client/coworker entitlement allowed, obvious spillover excluded once noticed, and hard-stop exclusions. |
| `docs/product/data_capture_source_access_method_plan_v0.md` | Source-access method plan under the current boundary; first-tranche build authority is separate and bounded by `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`. |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Data Capture Spine architecture blueprint for commissioned capture, core/satellite boundary, and rejected patterns. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Amended draft Data Capture Spine v0 obligation contract for setup and pressure testing, now operationalizing PCP-01 through PCP-08. |
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
| `docs/product/core_spine_v0_proof_case_selection_brief_v0.md` | Early proof case-selection brief; status BLOCKED_OWNER_CANDIDATES_NEEDED. For current case/backtest selection see the heavyweight discovery pass (`docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` and `..._results_part_2_v0.md`), which produced the candidates the brief was blocked on. |

## Data Capture Harness Operating Model

Accepted design direction for how commissioned Data Capture should operate.
Retrieval/navigation context only; "accepted" here means owner-accepted for
bounded pressure-test commissioning planning, not validated, hardened, or
product-ready. v0 and v1 of the operating-model architecture are superseded by
v2 — do not load them as current.

| Path | Use for |
| --- | --- |
| `docs/product/data_capture_harness_operating_model_architecture_v2.md` | Proposed v2 hybrid operating-model architecture (roles, session lifecycle, obligation-discharge visibility, handoff boundaries); resolves the v0/v1 review findings. Not ECR/Cleaning/Judgment/runtime design. |
| `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md` | Owner acceptance of v2 as the controlling operating-model architecture for pressure-test commissioning planning only; explicitly not validation, hardening, or product readiness. |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Accepted decision demoting the current manual harness + BT2-04 dry run to a direction signal and stating the goal for a buyer-trustworthy, obligation-discharging, inspectable harness. |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted Data Capture obligation baseline underpinning the v2 operating-model architecture; not validation, hardening, or product readiness. |
| `docs/product/data_capture_spine_lane_product_thesis_v0.md` | Data Capture Spine lane product thesis built on the v2 operating model; states lane purpose and boundaries without designing ECR/Cleaning/Judgment or authorizing runtime. |
| `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` | Bounded commissioning plan for three real Data Capture pressure tests against the accepted intake surface, v2 architecture, and current obligation contract; states what the tests expose and exclude. |

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
- `docs/product/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md` (discovery-scope charter), `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` (READY_FOR_OWNER_CASE_SELECTION), and `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md` (backtest candidates; proposes BT2-01 Chegg/ChatGPT) — the heavyweight proof-case discovery pass that produced the candidates the older case-selection brief was blocked on.

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
| `docs/prompts/patches/` | Patch prompts (accepted family; no drafts created yet). |
| `docs/prompts/wrappers/` | Thin wrapper prompts. |
| `docs/prompts/templates/` | Local prompt templates. |
| `docs/prompts/hygiene-queue/` | Current drift/parking area; not listed as an accepted prompt-family folder in the overlay. |

A few Data Capture pressure-test prompts currently sit unfiled at the
`docs/prompts/` root rather than in a typed family folder; treat them as drift
pending hygiene triage.

## Research And Review Areas

| Path | Use for |
| --- | --- |
| `docs/research/consulting-judgment-corpus/` | Consulting-judgment corpus, prompts, lane outputs, synthesis, candidate screens, backtestability, and reject patterns. |
| `docs/research/judgment-spine/` | Judgment Spine parent contract, manifest, three case tracks (Milwaukee, Unity, Canoo/Walmart), harness specs, and case-learning artifacts for consultant-grade decision judgment. |
| `docs/research/judgment-spine/manifest_v0.md` | Authoritative Judgment Spine case inventory and per-artifact status; open first for case selection. Indexes cases as Tier 0 — not validated, scored, or buyer-proof. |
| `docs/research/judgment-spine/cases/` | The three Tier 0 case tracks (Milwaukee, Unity Runtime Fee, Canoo/Walmart) at qualitative case-learning capture; see the manifest for per-case artifact status. Not scoreable fixtures, repeatability, or judgment-quality proof. |
| `docs/research/daimler_advisory_001_source_registry_v0.md` | Manual Daimler source-unit registry separating participant-safe candidates, date ambiguity, missing evidence, and reveal-only material before any packet rebuild or judgment-quality claim. |
| `docs/research/packing-phase/` | Boundary note for decision-packet construction between cleaned evidence and Judgment Harness inputs. |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` | Long-term Judgment Spine optimization thesis; open before CA setup, harness changes, or lesson-promotion decisions. |
| `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md` | Operating contract for consuming, protecting, and applying the Judgment Spine thesis; open after the thesis before future Judgment Spine prompts, harness changes, case additions, or lesson-promotion decisions. |
| `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md` | Decision record on pre-sale Judgment Spine model-execution evidence tiers (subscription/manual/chat default; raw API/harness as optional gate-bearing plumbing) and how to read no-case smoke-test / raw-API runner artifacts relative to buyer proof. |
| `docs/research/judgment-spine/harness/v0_14/` | Working v0.14 Judgment Harness spec: schemas, scoring, runner contracts, case construction, memorization probe, and failure logging. |
| `docs/research/judgment-spine/harness/v0_14/fixtures/` | Draft docs-only v0.14 fixture packs (Unity, Canoo/Walmart); blocked before scoring — not probe-safe, score-ready, validation, or proof. |
| `docs/research/judgment-spine/harness/adjacent-context/` | Side-context index for related Orca judgment/evidence/layer-boundary material; not controlling v0.14 spec authority. |
| `docs/review-outputs/` (root) | Flat collection of harness implementation/code-review outputs (source-capture adapters, source-observability helper, no-tools probe and execution-foundation); advisory findings only, co-located at the folder root rather than a typed subfolder. |
| `docs/review-outputs/adversarial-artifact-reviews/` | Adversarial artifact review reports, including the Daimler advisory and Canoo/Walmart Judgment Spine fixture-review families. |
| `docs/review-outputs/method-validation/` | Method-validation review outputs. |
| `docs/review-outputs/proof/` | Proof review outputs (currently a README placeholder). |

## Daimler Advisory & Probe Lane

Daimler is the selected internal advisory proof slice and first Judgment Spine
v0.14 fixture candidate. The whole lane is facilitator-only and carries no
durable evidence and no judgment-quality, buyer-proof, blind-use, or
fixture-admission claim. See also the mapped Daimler claim-tier classification
(Core Spine Files) and source registry (Research And Review Areas).

| Path | Use for |
| --- | --- |
| `docs/decisions/advisory_proof_slice_definition_v0.md` and `docs/decisions/advisory_runbook_scope_daimler_v0.md` | Define Daimler as the non-gate-clearing advisory proof slice and scope a future operator-facing advisory runbook; docs-only, no model execution or participant-packet exposure authorized. |
| `docs/decisions/daimler_advisory_run_authorization_decision_v0.md` and `docs/decisions/daimler_advisory_run_001_authorization_record_v0.md` | Advisory-run authorization state (gates currently closed) and the specific DAIMLER_ADVISORY_001 authorization for participant-safe prompt preparation only; not model-run authorization. |
| `docs/decisions/daimler_v0_14_probe_execution_authorization_decision_v0.md` and `docs/decisions/daimler_v0_14_backup_probe_authorization_decision_v0.md` | Bounded public-identifiers-only memorization-probe authorizations for the primary (GPT-5.5) and backup (Claude Opus) families; no scoring, blind-use, or fixture admission. |
| `docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md` | Facilitator-only gate outcome: no selected target family cleared the memorization-probe gate (GPT-5.5 access-blocked; Claude Opus failed with a tool-isolation caveat); blind-use/fixture-admission not authorized. |
| `docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | Toolkit capability specs inferred from the Daimler source fanout (cutoff provenance, evidence registry, packet compiler, isolation checker); planning only, not build/runtime authorization or a judgment-quality claim. |

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

- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`
- `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`
- `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md` and `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md` when routing from the completed all-slot pressure-test batch to the next source-observability decision.
- `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md` when checking the current closeout checkpoint for the first Data Capture pressure-test foundation after Slot 3 recapture and Source Observability support closeout.
- `docs/product/source_capture_toolbox/README.md` when orienting the first-tranche Source Capture Toolbox, checking component responsibilities, or finding current toolbox gaps.
- `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` when checking the architecture boundary for assembling multiple already-bounded source-quality rows and existing Source Capture Packets into a state census.
- `docs/product/source_capture_toolbox/source_capture_toolbox_agent_usability_dry_run_closeout_v0.md` when checking whether the current toolbox is agent-usable from a fresh-agent dry run, what runbook lessons were patched, or how to distinguish the dry run from a source-quality win.
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` when checking whether bounded first-tranche source-access tooling builds are authorized and where API/commercial/anti-detect/proxy/runtime surfaces remain gated.
- `orca-harness/source_capture/` (see the Orca Harness section) when the task needs the actual bounded capture implementation, adapters, or CLI runners rather than the toolbox contract.
- `docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md` when checking whether bounded docs-only source-observability requirements scoping is authorized.
- `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md` when reviewing candidate source-observability requirements or routing their next owner decision.
- `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md` when checking current RQ status after Slot 3 recapture or deciding whether the older scoping artifact is stale-alone.
- `docs/decisions/data_capture_spine_source_observability_requirements_support_implementation_scoping_authorization_v0.md` when checking whether bounded implementation scoping is authorized from the post-recapture requirements boundary.
- `docs/decisions/data_capture_spine_source_observability_local_support_implementation_scoping_authorization_v0.md` when checking whether bounded local source-observability support implementation scoping is authorized.
- `docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md` when checking whether bounded local source-observability support implementation execution was authorized and how far it extends.
- `docs/decisions/data_capture_spine_source_observability_support_closeout_decision_v0.md` when checking whether the updated local helper was sufficient for current post-recapture Slot 3 support or whether any helper patch remains open.
- `docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md` when continuing Slot 3 WSO/non-Reddit capture or cross-venue Slot 3 synthesis.
- `docs/product/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md` and `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md` (with `docs/decisions/data_capture_spine_post_slot3_recapture_delta_lane_local_acceptance_decision_v0.md`) when checking Slot 3 interim synthesis or the reviewed post-recapture delta against the all-slot synthesis.
- Per-slot capture-session records (`docs/product/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md`, `..._slot2_teal_...`, `..._slot3_reddit_...`, `..._slot3_wso_...`, and the Reddit batch 1of2/2of2 sessions) are execution detail — open a specific one only to inspect what that slot captured; they do not harden the obligation contract.
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
`B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5`, but
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
- `docs/product/judgment_spine_evidence_ladder_architecture_v0.md` when the work classifies Judgment Spine claim tier, proof tier, buyer-proof boundary, or judgment-quality boundary.
- `docs/product/judgment_spine_gate_ownership_map_v0.md` when the work needs to route or block Judgment Spine gate ownership before claim promotion.
- `docs/product/judgment_quality_promotion_operating_model_v0.md` when the work needs to run or plan a case through gates JSG-01 to JSG-10, decide a run lifecycle state, or check what a partial or by-hand run can claim.
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
artifact. Listing `orca-harness/` reflects authorized, bounded implementation
only; it does not assert runtime readiness, that its build scope is validated,
or that any gated surface (production runtime, API/commercial fetch, ECR,
Cleaning, Judgment) is authorized. Check the target artifact, retrieval header,
and current `git status` before strict claims.
