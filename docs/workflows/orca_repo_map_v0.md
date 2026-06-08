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

- Status: ACTIVE_RETRIEVAL_MAP (retrieval-only; source authority remains in `.agents/workflow-overlay/source-of-truth.md`)
- Artifact type: Workflow navigation artifact
- Scope: Repo navigation and source-pack selection
- Refreshed: 2026-06-06 (added the header-complete anti-blocking HTTP rung-1 adapter `anti_blocking_http` + the `block_shell` honest-success guard to the harness rows; anti-block ladder usage guide indexed via the Data Capture submap). Prior: 2026-06-05 repo-map/submap hygiene.
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
| `AGENTS.md` | Canonical root instructions, global behavior, and triggers to Orca owner docs. |
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
| `.agents/workflow-overlay/delegated-review-patch.md` | Provisional, opt-in Delegated Review-and-Patch convention for high-stakes authored artifacts; not a bound review lane. |
| `.agents/workflow-overlay/safety-rules.md` | Safety and forbidden drift. |
| `.agents/workflow-overlay/skill-adoption.md` | Skill source and adoption status. |

## Workflow Navigation Files

| Path | Use for |
| --- | --- |
| `docs/workflows/artifact_retrievability_guide.md` | Operational guidance for durable artifact headers, body-opening source surfaces, stale/recheck patterns, repo-map/index treatment, report-only retrieval checks, and hygiene anti-rot. |
| `docs/workflows/orca_repo_map_v0.md` | Compact navigation map for bounded source-pack selection and prompt setup. |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Data Capture Spine / Source Capture Armory submap. Open before enumerating capture owner docs. |
| `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | Judgment Spine submap. Open before enumerating Judgment owners across `docs/research/judgment-spine/` and `docs/product/judgment_spine_*`. |

## Orca Harness

`orca-harness/` is bounded, authorized implementation backing Data Capture
source acquisition and the v0.14 Judgment Harness. It is navigation context
here, not a runtime, acceptance, or readiness claim. Build scope is controlled
by the authorization decisions named below; surfaces outside them (production
runtime, commercial fetch, broad crawling, ECR, Cleaning, Judgment
design) remain gated.

| Path | Use for |
| --- | --- |
| `orca-harness/source_capture/` | Source-capture packet core: models, writer, CLI support, plaintext receipts, and the `block_shell` honest-success classifier (block-shell / empty / content-unverified; no positive content class). |
| `orca-harness/source_capture/adapters/` | Bounded capture adapters (direct HTTP, media/asset, Archive.org, browser snapshot, authenticated browser, Reddit API where present, and a header-complete anti-blocking HTTP rung-1 adapter `anti_blocking_http`); the heavier anti-blocking/CloakBrowser backend is selected and authorized by decision but should be verified in implementation before use. Verify any adapter's presence in code before use. Not scraper frameworks, commercial fetch, broad crawling, storage, dashboards, deployment, or production runtime. |
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
(source-capture armory) and
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
| `docs/decisions/orca_icp_wedge_pricing_first_v0.md` | **Current** first-proof wedge authority: pricing-first / AI-monetization beachhead on an outside-in competitive-intelligence engine. Owner-locked; supersedes the v0 ICP wedge below. Chosen, not validated (decide-vs-confirm test pending). |
| `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` | First ICP wedge decision and decision-family focus. **SUPERSEDED** by `orca_icp_wedge_pricing_first_v0.md` (above); historical only. |
| `docs/product/orca_product_proof_lead_charter_v0.md` | Product proof lead role and proof execution boundary. |

## Judgment Spine

The Judgment Spine spans **both** trees — `docs/research/judgment-spine/` (thesis, manifest, cases, harness) and `docs/product/judgment_spine_*` plus the conductor. **Open the consolidation map first**: it is the single `retrieval_only` entry that orients across both trees and routes one hop to every owner. Do not pre-load the owners from here.

| Path | Use for |
| --- | --- |
| `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | **Judgment Spine entry map — open first.** Per-area summary, owner-native status, and one pointer for thesis, cases/manifest, conductor, gate ownership, evidence ladder, JSG-08, and the harness; routes to the owners rather than restating them. The path toward judgment-quality evidence, not proof; by-hand runs cap at product-learning. |

## Data Capture Spine

The Data Capture Spine spans product authority, source-access decisions, Source
Capture Armory docs, source-quality support, and `orca-harness/` implementation.
**Open the consolidation map first** for capture/armory work: it is the
`retrieval_only` entry that orients across these surfaces and routes one hop to
the owner sources. Do not pre-load all capture artifacts from this map.

| Path | Use for |
| --- | --- |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | **Data Capture Spine entry map — open first.** Routes to Capture obligations, source-access boundary, build authorization, method plan, Source Capture Armory README, packet lifecycle, harness runners, source-quality support, and current Reddit pre-commercial routing. Map only; not validation, readiness, source-access permission, or implementation authority. |

## Core Spine Files

| Path | Use for |
| --- | --- |
| `docs/product/core_spine_v0_product_contract.md` | Core Spine product contract and eight primitives. |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | Manual information-production foundation and Evidence Unit standard. |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Data Capture/Cleaning/Judgment boundary and Evidence Candidate Record setup context. |
| `docs/product/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | Proposed Core Spine design note on placing independent-corroboration vs artificial-amplification discipline across the Cleaning/Judgment boundary; proposed, not validated. |
| `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` | Daimler advisory claim-tier classification decision recording the current no-durable-evidence state, required product-learning receipt before any evidence claim, and blocked buyer-proof/judgment-quality claims. |
| `docs/product/engagement_logic_registry_v0.md` | Signal-use and engagement interpretation registry. |
| `docs/product/core_spine_v0_proof_protocol_v0.md` | Core proof protocol. |
| `docs/product/core_spine_v0_proof_input_selection_v0.md` | Proof input-selection rules. |
| `docs/product/core_spine_v0_proof_packet_preflight_v0.md` | Proof packet preflight. |
| `docs/product/core_spine_v0_proof_case_selection_brief_v0.md` | Early proof case-selection brief; status BLOCKED_OWNER_CANDIDATES_NEEDED. For current case/backtest selection see the heavyweight discovery pass (`docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` and `..._results_part_2_v0.md`), which produced the candidates the brief was blocked on. |

For Data Capture / Source Capture Armory detail, open
`docs/workflows/data_capture_spine_consolidation_map_v0.md`; this repo map
intentionally does not duplicate the owner-doc inventory.

## Data Capture Harness Operating Model

Route Data Capture operating-model and commissioning-plan questions through
`docs/workflows/data_capture_spine_consolidation_map_v0.md` first. That submap
owns the one-hop pointers to v2 operating-model architecture, owner acceptance,
obligation baseline, lane thesis, and commissioning plan. This repo map does
not duplicate that inventory.

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
| `docs/research/judgment-spine/` | Judgment Spine corpus (parent contract, manifest, case tracks, harness, case-learning). **Open the consolidation map first** — see the Judgment Spine section above; it routes to every owner across both trees instead of enumerating them here. |
| `docs/research/daimler_advisory_001_source_registry_v0.md` | Manual Daimler source-unit registry separating participant-safe candidates, date ambiguity, missing evidence, and reveal-only material before any packet rebuild or judgment-quality claim. |
| `docs/research/packing-phase/` | Boundary note for decision-packet construction between cleaned evidence and Judgment Harness inputs. |
| `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md` | Decision record on pre-sale Judgment Spine model-execution evidence tiers (subscription/manual/chat default; raw API/harness as optional gate-bearing plumbing) and how to read no-case smoke-test / raw-API runner artifacts relative to buyer proof. |
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

- `docs/workflows/data_capture_spine_consolidation_map_v0.md` for orientation.
- `.agents/workflow-overlay/source-loading.md#data-capture-intake-surface--msp-pressure-test-target-pack` for the canonical pressure-test read-pack rule.

Then open only the controlling owner doc named by the submap or source-loading
pack for the current claim. Do not bulk-load all capture sessions, historical
fixture files, review outputs, or Source Capture Armory docs from this repo map.

For strict source-pinning claims, compute fresh hashes from the current target
files. Do not rely on historical hashes recorded in older prompts, reviews, or
map versions unless the task is explicitly reviewing that older state.

### Offer Or Buyer Proof Work

Start with:

- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/decisions/orca_icp_wedge_pricing_first_v0.md` — current first-proof wedge (pricing-first); supersedes the v0 wedge below
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` — superseded; historical only
- `.agents/workflow-overlay/product-proof.md`

### Core Spine Evidence Standard Work

Start with:

- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- **Open `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` first** for any Judgment Spine work; it routes to the ladder, gate ownership map, conductor, and JSG-08 owner contract below.
- `docs/product/judgment_spine_evidence_ladder_architecture_v0.md` when the work classifies Judgment Spine claim tier, proof tier, buyer-proof boundary, or judgment-quality boundary.
- `docs/product/judgment_spine_gate_ownership_map_v0.md` when the work needs to route or block Judgment Spine gate ownership before claim promotion.
- `docs/product/judgment_quality_promotion_operating_model_v0.md` — **the Judgment Spine conductor; open this FIRST for the judgment run lane** (running or planning any case through gates JSG-01 to JSG-10). It sequences the gates and routes to the evidence ladder, gate ownership map, and JSG-08 owner contract rather than restating them; use it to decide a run lifecycle state or check what a partial or by-hand run can claim. It is the path toward judgment-quality evidence, not proof — by-hand runs cap at product-learning.
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
