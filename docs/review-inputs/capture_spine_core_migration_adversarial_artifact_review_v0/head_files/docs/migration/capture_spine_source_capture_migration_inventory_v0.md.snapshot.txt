# Capture Spine + Source Capture Toolbox — Spine-First Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration inventory record (inventory-only marking artifact)
scope: >
  Inventory-only marking artifact for the Capture Spine (Data Capture Spine +
  Source Capture Toolbox / Armory) ahead of the spine-first repo migration. Marks
  every Capture document, workflow, decision, prompt, review, runtime/code surface,
  case artifact, source-family surface, and adjacent-lane boundary; classifies each
  as Capture-owned / subsystem / runtime / source-family / cross-lane-overlap /
  case-family / downstream / shared / unclear; proposes future homes; and records
  the Search and IG cross-lane double-confirm. No moves, renames, code, or tests.
use_when:
  - Planning or sequencing the Capture-Spine slice of the spine-first migration.
  - Deciding whether a capture/source-access/packet/source-family surface is Capture-owned.
  - Orienting a fresh agent on Capture vs Search / IG / ECR / Cleaning / Judgment / case-family boundaries.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/README.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
stale_if:
  - The Data Capture consolidation map or the Source Capture Armory README changes component/owner set.
  - data_capture_spine/ or source_capture_toolbox/ membership changes (a doc is added, removed, or re-homed).
  - A later accepted Orca decision creates an IG lane, renames the Toolbox to Armory, or re-draws the Capture / Search / Cleaning / Judgment boundary.
  - The global runtime-mapping decision binds a home for orca-harness/ capture code.
```

## Status & provenance

- Status: `INVENTORY_ONLY_V0` — a marking/discovery artifact. Allocations are **proposed**; `move_now: no` for every artifact.
- Base: read against `origin/main @ c417622d`. Pending PRs on other branches are **not** assumed merged.
- Authoritative live index for Capture is `docs/workflows/data_capture_spine_consolidation_map_v0.md` (the front door, routed by area). This inventory **reads** it; on any conflict the map's pointed-to owner doc wins.
- Companion wave: this is the Capture slice of a coordinated set of spine-first inventories in flight on sibling branches (search, cleaning, ecr, foundation-layer, product-lead/buyer-proof, ontology, global-prompt-review). Cross-lane calls below must reconcile with those (see §12).
- **Subagents used:** 4 bounded read-only `Explore` agents (citation-first, strict return schema): (1) data_capture_spine docs, (2) source_capture_toolbox docs, (3) harness/runtime, (4) cross-lane boundary + Search/IG double-confirm. The main agent wrote this artifact; subagents edited nothing.

## Core allocation rule (applied)

- **Capture Spine** owns the capture lifecycle, capture obligations, source-access boundaries, intake/candidate routing (Candidate URL Intake, Corpus/standing capture), packet contracts, source-family capture/projection surfaces, source-quality support, and the Capture-owned runtime mapping.
- **Source Capture Toolbox / Armory** is adopted under Capture as a **named subsystem**, not dissolved into vague "capture docs."
- **Search** owns demand-signal discovery / search-led candidate surfacing unless a doc is clearly Capture-owned.
- **IG lane** owns IG-specific projection/source-family markings *where already marked* — Capture double-confirms, does not silently absorb (see §6).
- **Case families** own reusable evidence/run corpora; **vertical satellites** own reusable domain context; **ECR/SCR, Cleaning, Judgment** are downstream consumers, not homes for raw capture or projection truth.

---

## 1. Current Capture surfaces found

Counts are authoritative from `git ls-tree HEAD` at `c417622d`.

| Area | Where | Count | Note |
| --- | --- | --- | --- |
| Data Capture Spine docs | `docs/product/data_capture_spine/` | **64** | obligations, operating-model (v0/v1/v2), source-access, intake/corpus, Reddit/LinkedIn lanes, pressure-test slots, demand-durability venues, creator, payload/schema |
| Source Capture Toolbox / Armory docs | `docs/product/source_capture_toolbox/` | **45** | the named Armory subsystem (§2) |
| Capture front door | `docs/workflows/data_capture_spine_consolidation_map_v0.md` | 1 | the live authoritative index |
| Reddit search-surface handling workflow | `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`, `reddit_candidate_intake_to_projection_lane_handoff_v0.md`, `reddit_capture_to_ecr_consumption_probe_finding_v0.md`, `reddit_graph_frontier_b2b_marketing_traversal_record_v0.md` | ~4 | capture workflow records |
| Capture-relevant decisions | `docs/decisions/` | ~25 | source-access build auth, source-observability (×6), reddit candidate-intake default policy + ×2 adjudications, packet fixture retention, archive-snapshot typed-timing, deleted-comment-signal doctrine, post-batch/post-slot3 patch decisions, company-aggregate-forward (×2), pre-capture discovery spine charter, distillation_binding_data_capture |
| Capture runtime/code/tests | `orca-harness/source_capture/`, `orca-harness/capture_spine/`, `orca-harness/runners/`, `orca-harness/tests/`, `orca-harness/source_observability/` | many | §4; 22/31 runners are capture-family |
| Capture pressure-test evidence | `docs/product/data_capture_spine/...pressure_test_slot*` | ~12 | slot1 (MI/BIWS), slot2 (Teal), slot3 (Reddit batches/WSO) capture sessions + synthesis |

Sub-themes inside `data_capture_spine/` (the 64): obligation/architecture core (`core_spine_v0_data_capture_spine_*`, incl. blueprint, obligation contract, fixture synthesis/plan, 6 pressure-test fixtures); operating model (`data_capture_harness_operating_model_architecture_v0/v1/v2` + acceptance + product-goal + obligation-baseline + lane-thesis); source access (`data_capture_source_access_boundary_decision`, `..._method_plan`); intake (`...candidate_url_intake_contract`, `...corpus_intake_obligation_contract_proposal`, `...intake_surface_consolidation`); Reddit lane (`...reddit_candidate_url_intake_crawler_architecture`, `...reddit_graph_frontier_lane_architecture`); LinkedIn lane (`...linkedin_discovery_planning_lane_architecture`, `...linkedin_lane_index`, `...linkedin_influence_trajectory_watch_spec`, `...linkedin_live_layer_architecture`); pressure-test (slots + `...pressure_test_commissioning_plan`, `...execution_authorization`, `...closeout_synthesis`, `...all_slot_synthesis`); demand-durability venues (8, see §5/§7); creator (`orca_creator_momentum_pipeline_architecture`, `orca_creator_monitoring_policy_architecture`); payload/schema (`source_capture_tenant_payload_attachment_boundary`, `source_capture_core_payload_split_explainer`, `source_capture_packet_schema_evolution_architecture`, `data_capture_spine_posture_vocabulary_enforcement_proposal`); storage/projection (`orca_capture_projection_storage_spine_architecture`); `retail_pdp_typed_envelope_probe`; `data_capture_spine_future_exploration_lanes`.

**Classification of the bulk** (per-category; `move_now: no` throughout; `recommended_future_home` = `orca/product/spines/capture/` proposal unless noted):
- Obligation/architecture/operating-model/source-access/intake/payload/schema/pressure-test → `classification: capture_spine`; consuming/adjacent: ECR, Cleaning, Judgment (downstream), Search (consumes demand reads). Why Capture owns: these define the capture lifecycle, obligations, and access boundary — the spine's reason to exist.
- Reddit + LinkedIn lanes → `classification: source_family_capture_projection` (Capture-owned, careful boundaries — §8).
- Creator (momentum/monitoring) → `classification: source_family_capture_projection` with an `ig_owned_overlap` flag (§6).
- demand-durability venue profiles → `classification: source_family_capture_projection` (Capture), with the **search-interest** one excluded to Search (§5/§7).

## 2. Source Capture Toolbox / Armory adoption map

`docs/product/source_capture_toolbox/` (45 docs) is the **named Capture subsystem**. `classification: source_capture_toolbox_subsystem`; `current_owner: Source Capture Armory (Capture)`; `recommended_future_home: orca/product/spines/capture/source_capture_toolbox/` OR `.../armory/` (proposal — §11 naming question); `move_now: no`. Adopt as a *unit*, do not dissolve. Sub-families (from the toolbox explorer):

- **Armory core (≈11):** `README.md` (the index/authority), `source_capture_playbook_v0.md`, `capture_recon_index_v0.md`, `source_capture_anti_block_ladder_usage_guide_v0.md`, `weapon_anti_block_http_ladder_v0.md`, `pipe_block_wall_escalation_v0.md`, `weapon_rung15_embedded_payload_extraction_v0.md`, `armory_weapon_and_pipe_readme_templates_v0.md`, `source_quality_mini_god_tier_profile_v0.md`, `source_quality_source_unit_queue_template_v0.md`, `source_quality_state_assembler_v0.md`.
- **Source-quality closeouts/trials (≈7):** `source_quality_mixed_source_trial_closeout`, `..._cw_p1/p4/p6_end_to_end_pass_closeout`, `..._slot3_post_recapture_closeout`, `source_capture_toolbox_agent_usability_dry_run_closeout`, `source_capture_packet_fixture_admission_criteria_v0.md` (proposal; fixture-admission authority deferred to owner).
- **CloakBrowser (3):** `cloakbrowser_local_setup_probe_receipt`, `cloakbrowser_packet_runner_architecture` (+ `_independent_pass`).
- **Reddit (4):** `reddit_capture_operator_playbook`, `reddit_precommercial_capture_consolidation_planning_thread`, `..._success_signal_architecture`, `reddit_packet_consolidation_runner_structural_spec`.
- **Retail/PDP (3):** `retail_pdp_projection_contract`, `..._playbook`, `..._sidecar_operator_playbook` (§7).
- **Archive (3):** `archive_org_capture_runner_resilience_learnings`, `archive_org_refinement_and_source_family_gap_spec`, `source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout`.
- **LinkedIn/Reddit concurrent structure (1):** `linkedin_reddit_source_capture_armory_concurrent_structure_architecture`.
- **IG family (≈13):** `ig_*` — flagged `ig_owned_overlap` (§6).

## 3. Capture-owned source-family surfaces

Source-family capture/projection lives under Capture (Toolbox docs + data_capture_spine venue profiles + harness projection code). `classification: source_family_capture_projection`; `move_now: no`; proposed home `orca/product/spines/capture/source_families/<family>/` (proposal only).

| Family | Docs (home) | Runtime (harness) | Owner call |
| --- | --- | --- | --- |
| Reddit | toolbox reddit ×4 + data_capture_spine reddit lane ×2 + decisions ×3 | `source_capture/reddit_consolidation/`, `reddit_projection.py`, `reddit_agent_view*.py`, `screening_reddit_read.py`, `capture_spine/reddit_candidate_intake/`, `capture_spine/reddit_graph_frontier/`, `adapters/reddit_api.py` | Capture-owned (careful boundaries, §8) |
| LinkedIn | data_capture_spine linkedin ×4 | `capture_spine/linkedin_lane/`, `linkedin_live_adapter/`, `linkedin_live_runtime/`, `linkedin_graph_frontier/` | Capture-owned, no-live/upstream (§8) |
| Retail/PDP | toolbox retail ×3 + data_capture_spine ×6 (durability + typed-envelope probe) | `source_capture/retail_pdp_projection.py`, `price_payload_extraction.py`, `adapters/amazon_delivery_location.py`, `runners/run_retail_pdp_projection.py` | Capture-owned (§7) |
| IG | toolbox ig_* ×13 + data_capture_spine creator ×2 | `source_capture/ig_projection.py`, `ig_momentum_harvest.py`, `ig_calls_parse.py`, `runners/run_ig_creator_momentum_projection.py` | Capture-owned **pending IG double-confirm** (§6) |
| Archive / anti-block | toolbox archive ×3 | `adapters/archive_org.py`, `archive_today.py`, `publisher_history.py`, `anti_blocking_http.py`, `historical_capture.py`, `block_shell.py` | Capture-owned |
| demand-durability venues | data_capture_spine ×8 (minus search-interest) | `runners/run_source_capture_durability_series.py` | Capture-owned (search-interest excluded → Search, §5) |

## 4. Runtime / code / test surfaces

From the harness explorer. **Recommended_future_home for ALL runtime = leave in `orca-harness/` until the global runtime-mapping decision is bound.** This inventory MAPS lane ownership; it does not move code.

- **`orca-harness/source_capture/` → `capture_runtime`:** packet model/writer/assembly (`models.py`, `writer.py`, `packet_assembly.py`, `packet_inspection.py`), the adapter suite (`adapters/`: direct_http, anti_blocking_http, archive_org, archive_today, browser_snapshot, cloakbrowser_snapshot, media_asset, reddit_api, publisher_history, amazon_delivery_location), `historical_capture.py`, `cli_support.py`, credentials/auth/proxy (`auth_state`, `proxy_profiles`, `reddit_credentials`), `cadence`, `block_shell`, `source_quality`, `reddit_consolidation/`.
- **Source-family projection (`source_family_capture_projection`):** `ig_projection.py`, `ig_momentum_harvest.py`, `ig_calls_parse.py`, `reddit_projection.py`, `reddit_agent_view*.py`, `retail_pdp_projection.py`, `price_payload_extraction.py`, `screening_reddit_read.py`.
- **`orca-harness/capture_spine/` → `capture_spine` (intake):** `reddit_candidate_intake/`, `reddit_graph_frontier/`, `linkedin_lane/`, `linkedin_live_adapter/`, `linkedin_live_runtime/`, `linkedin_graph_frontier/`.
- **`orca-harness/source_observability/` → `capture_runtime`** (observability helpers).
- **Runners:** **22 of 31 are capture-family** (16 capture_runtime packet runners + 4 source-family projection + 2 capture_spine intake). The other 9 are Judgment/observability (`run_case`, `run_memorization_probe*`, `run_finalization_receipt`, `score_external_run`, `run_source_observability_report`, `run_source_quality_*`).
- **Tests (`capture_runtime` infra):** ~17 contract tests (adapter contracts + `test_source_capture_packet_no_runtime_imports`, `test_no_llm_imports`), ~25 capture unit tests, 2 integration (`test_reddit_screening_read_live`, `test_run_case_tr_casetext`).
- **NOT Capture (downstream, leave in harness, owned by their spine):** `ecr/` (ECR SP-1/2/3/6 derivers), `signal_content/` (SCR), `cleaning/`, `scoring/`, `evidence_binding/` (JSG-01 boundary), `reports/`. `schemas/` and `tests/conftest.py` = `shared_global`.
- **KEY FINDING:** **No demand-scan / demand-read / demand-gate / AEO / search-engine code exists in the harness.** The Search/Demand-Signal method is spec-only; the only demand-named harness surface is Capture's `run_source_capture_durability_series.py` and the case fixture text `first_demand_read_findings_v0.md`.

## 5. Search overlap and double-confirm result

`SEARCH_DOUBLE_CONFIRM:` **FOUND on main** — `docs/migration/repo_structure_search_lane_v0/` (the search lane's migration package: `reference_inventory.md`, `runbook.md`, `moved_paths_index.md`, manifest, apply script) **plus** the binding `docs/decisions/orca_search_product_lane_binding_v0.md`. **Additionally** a dedicated Search/Demand-Signal migration *inventory* (`docs/migration/search_demand_signal_migration_inventory_v0.md`) exists as **in-flight PR #247, authored this session, NOT yet on `main`/this branch** (consistent with "pending PRs not merged"). Reconcile against #247 when it lands.

**Overlap — the `demand_durability_indicator_*` split (the load-bearing seam):**
- `search_owned_overlap`: `docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md` — the **search-interest** durability profile moved to Search (#236). Capture must NOT reclaim it.
- `capture_spine` (stays): `data_capture_spine/demand_durability_indicator_{price_timeseries,availability_restock,review_velocity_corpus}_capture_profile_v0.md` + `demand_durability_multi_retailer_rendered_capture_spec`, `demand_durability_us_storefront_pin_recon_verdict`, `demand_durability_capture_pilot`, `demand_durability_indicator_standing_capture_obligation_home_decision_framing`, and the seam doc `demand_durability_indicator_capture_deconfliction_note_v0.md`.
- The search-lane binding **explicitly excludes** the retail durability profiles from Search (binding §"Explicitly EXCLUDED"), and the deconfliction note documents the split. Boundary is **mitigated, documented**.
- Other Search-owned method docs (scan-core, read-taxonomy, gate-definitions) live in `docs/product/search/` and are **consumed by** Capture's reads but Capture does NOT own them. Search-discovered candidate sources stay Search-owned until Capture accepts a source/capture obligation.

## 6. IG overlap and double-confirm result

`IG_DOUBLE_CONFIRM:` **`ig_marking_not_found_on_this_branch`** — there is **no formal IG lane binding** (nothing analogous to the search lane binding) and **no IG migration/marking doc**. IG currently exists as a **feasibility-proven capture satellite**:
- 13 `ig_*` docs under `source_capture_toolbox/` (discovery, wind-caller capture feasibility/build, reel/calls capture, R-probe, at-scale envelope, capture-shape contract, consolidated findings).
- `data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md` (**PROPOSED**, and it explicitly *defers a `creator_momentum/` lane decision*) + `orca_creator_monitoring_policy_architecture_v0.md`.
- `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` (a cold-start handoff that marks IG a **satellite, not an adopted lane**).
- Runtime: `ig_projection.py`, `ig_momentum_harvest.py`, `ig_calls_parse.py`, `run_ig_creator_momentum_projection.py`, `run_source_capture_ig_calls_packet.py` + tests.

**Classification:** `ig_owned_overlap` — held under Capture's Toolbox today, but Capture should **NOT silently absorb** these as plain Capture docs. If a later owner decision creates an IG lane (as Search got one), these need formal re-homing + a binding. **→ `double_confirm_needed` (§ below).**

## 7. Retail/PDP classification

`classification: source_family_capture_projection` → **Capture-owned, NOT a vertical satellite.** Docs: `source_capture_toolbox/retail_pdp_projection_{contract,playbook}`, `retail_pdp_sidecar_operator_playbook`; `data_capture_spine/retail_pdp_typed_envelope_probe`, `demand_durability_multi_retailer_rendered_capture_spec`, `demand_durability_us_storefront_pin_recon_verdict`, and the 3 retail durability profiles. Runtime: `source_capture/retail_pdp_projection.py`, `price_payload_extraction.py`, `adapters/amazon_delivery_location.py`, `runners/run_retail_pdp_projection.py` + the CloakBrowser sidecar (`run_source_capture_cloakbrowser_packet.py --source-family retail_pdp`). Boundary risk: **none** — Retail is cleanly Capture/Armory-bound; the projection contract states the no-ECR/Cleaning/Judgment boundary. `recommended_future_home: orca/product/spines/capture/source_families/retail_pdp/` (proposal).

## 8. Reddit / LinkedIn / other source-family boundary notes

- **Reddit Candidate URL Intake** (`data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`): Capture-adjacent intake — emits candidate subreddit/thread/outbound rows + provenance **only**; **not** Source Capture Packet output, **not** broad crawler, **not** automatic Data Capture handoff. Capture-owned, distinct from Armory capture.
- **Reddit Graph Frontier Lane** (`...reddit_graph_frontier_lane_architecture_v0.md`): accepted bounded planning lane; **not** same-run traversal, **not** Graph-Frontier-owned live fetch, **not** automatic capture. Capture-owned.
- **LinkedIn Discovery Planning** (`...linkedin_discovery_planning_lane_architecture`, `...linkedin_lane_index`): **no-live, planning-only, upstream of Source Capture Armory**; hard rails (no contact harvesting, no profile/body capture, no packet output, no handoff until promotion; `optional_poc_risk_mode` is supervised-personal only). Capture-owned upstream discovery; **not** Armory capture, **not** an Outreach lane.
- **Archive / anti-block ladder**: Capture-owned source-access mechanics (cost-ordered rungs; one Daimler/Akamai data point, not a settled capability).
- General rule applied: a **Search-discovered candidate source remains Search-owned until Capture accepts a source/capture obligation** for it.

## 9. Downstream ECR/SCR, Cleaning, Judgment interfaces

These are `downstream_consumer` — they read Capture output and must NOT become homes for raw capture/projection truth. `move_now: no`; they migrate with their own spines, not Capture.
- **ECR (source-side):** `orca-harness/ecr/` + `docs/workflows/ecr_spine_submap_v0.md` + `docs/product/signal_content/...signal_content_record_architecture` (SCR). Reads `SourceCapturePacket`; JSG-01 frozen; `evidence_binding/` is the JSG-01 boundary.
- **Cleaning:** `orca-harness/cleaning/`; boundary doc `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (the canonical Capture↔Cleaning↔Judgment split) and `core_spine_v0_data_lake_mechanics_map_v0.md` (capture→projection→ECR/SCR→Cleaning→Judgment flow by key).
- **Judgment / scoring:** `orca-harness/scoring/`, `schemas/` + the judgment spine docs — consume cleaned/derived records, not raw capture.
- **Product Lead:** `product_lead/orca_buyer_proof_packet_v0.md` etc. consume the demand reads (Search-owned) and capture outputs; they own buyer-proof, not capture.
- Interface to preserve in migration: the `SourceCapturePacket` contract (`source_capture/models.py`) is the **load-bearing seam** every downstream consumer keys off — do not fork it.

## 10. Case-family and satellite exclusions

- **`orca-harness/cases/product_learning/` (≈14 case families)** and **`cases/plumbing/` (TR/Casetext)** → `classification: case_family`. They contain `source_captures/` packets, ledgers, participant packets, runs — **reusable evidence/run corpora owned by the case-family inventory, NOT Capture.** Capture may *read* a case's source-capture packet; it does not own the case lifecycle. `recommended_future_home: leave to the case-family inventory` (do not pull into Capture).
- **Vertical satellites** (beauty venue card set, vertical exploration guide, fragrance Level-1) → owned by Core Spine / vertical-satellite inventories; Capture consumes venue context, does not own it.
- A product-learning case's embedded capture artifact moves with the **case**, unless it is *only* a Capture packet/source-capture artifact with no case binding.

## 11. Stale naming and stale placement risks

1. **`data_capture_spine/` prefix sprawl (64 docs, one flat folder).** Multiple coexisting concerns (operating-model v0/v1/v2, ~12 pressure-test slot sessions, 8 demand-durability docs, 4 LinkedIn, 2 Reddit, creator, payload/schema). A migrator must sub-partition (operating-model / intake / source-family / pressure-test-evidence) rather than move 64 files as one blob.
2. **"Source Capture Toolbox" vs "Armory" naming.** Docs say both ("Source Capture Toolbox" folder, "Source Capture Armory" README/title). The proposed home offers `source_capture_toolbox/` OR `armory/`. Pick one canonical name at migration (§12).
3. **Operating-model versions coexist** (`...architecture_v0.md`, `v1`, `v2`, `v2_acceptance_decision`). v2 is the accepted one; v0/v1 are historical. Risk of moving a superseded version as if current.
4. **IG is not formally marked** (no lane binding) yet has 13 docs + runtime + a "lane handoff" — placement is satellite-by-default, ambiguous for migration (§6).
5. **`demand_durability_indicator_*` split across `search/` and `data_capture_spine/`** — same prefix, two lanes (mitigated by the deconfliction note, but a discoverability trap).
6. **Pressure-test slot capture sessions** (`...pressure_test_slot1_mi_biws`, `slot2_teal`, `slot3_reddit_*`, `wso`) are operational capture *evidence* — are they Capture-spine docs or capture-case evidence? Borderline between `capture_spine` and `case_family`; flagged for owner.
7. **Harness runtime has no bound home.** `orca-harness/` capture code is authoritative but the global runtime-mapping decision is unbound — leave in place; do not move with the docs.
8. **The consolidation map is the de-facto index, not a placement authority** — migration must keep it (and its area pointers) in sync, or it silently rots.

## 12. Open owner questions

1. **IG lane?** Promote IG from a Toolbox satellite to a bound lane (binding + re-home of the 13 `ig_*` docs + creator-momentum spec), or keep it under Capture/Toolbox? (`double_confirm_needed`.)
2. **Toolbox vs Armory canonical name** for the subsystem folder at migration?
3. **Source-family module structure** — adopt `orca/product/spines/capture/source_families/<family>/` (reddit, linkedin, retail_pdp, ig, archive), or keep Toolbox flat?
4. **Pressure-test slot sessions** — Capture-spine operational docs, or split to a capture-evidence/case-family home?
5. **Operating-model v0/v1 disposition** — archive the superseded versions during migration?
6. **Cross-inventory reconciliation** — which inventory is authoritative where two claim a shared surface (e.g., creator-momentum spec lives in `data_capture_spine/` but is IG; ECR/Cleaning consume the packet contract)?
7. **Search reconciliation** — align this inventory's `demand_durability_*` split with the in-flight Search inventory (PR #247) before either lands.

## double_confirm_needed

- **IG marking absent** (`ig_marking_not_found_on_this_branch`). Capture is holding the IG satellite today; an IG-lane owner decision is needed before treating the 13 `ig_*` docs + creator-momentum spec as permanently Capture-owned vs IG-owned. Do not absorb silently.
- **Search inventory in flight** (PR #247 not on main). The Capture↔Search seam (the `demand_durability_*` split, Search-discovered candidates) should be cross-checked against #247 when it merges.
- These do **not** block this Capture inventory (per the task); they are recorded for owner adjudication.

## 13. Suggested migration order

Lowest-risk first; physical moves are NOT part of this artifact.
1. **Pick canonical names** (Toolbox vs Armory; whether an IG lane exists) — naming/owner decisions gate everything else.
2. **Sub-partition `data_capture_spine/`** logically (operating-model / source-access / intake / source-family / pressure-test-evidence / payload-schema) before any physical move.
3. **Adopt the Toolbox/Armory as a subsystem unit** under Capture (`orca/product/spines/capture/source_capture_toolbox|armory/`).
4. **Reconcile cross-lane seams** (Search `demand_durability_*` split vs PR #247; IG double-confirm; ECR/Cleaning/Judgment downstream) before moving shared-boundary docs.
5. **Leave harness runtime in place** until the global runtime-mapping decision binds a home.
6. **Leave case-family corpora** to the case-family inventory.
7. Keep the consolidation map (front door) and the search moved-paths index in sync throughout.

## 14. Explicit non-claims

- **Inventory only.** No file moved/renamed/deleted; no code changed; no tests run; no live capture. Allocations are **proposals** (`move_now: no` for every artifact).
- **Not** validation, readiness, source-access permission, commercial-scraping authorization, fixture promotion/admission, or buyer proof. A green checker is placement shape, not authority.
- Does **not** re-decide ownership: the consolidation map + the owner docs it points to govern; on conflict they win over this inventory.
- `likely_owner`/`classification` labels are **placement proposals**, not authority transfers; a sibling-lane inventory (search/ig/ecr/cleaning/judgment/case-family) may claim a shared surface differently — reconcile per §12.
- Read against `origin/main @ c417622d`; **pending PRs are not assumed merged** (the Search inventory PR #247 and the sibling spine-first inventories are in flight).
- Boundary calls (Capture vs Search, Capture vs IG, Capture vs Cleaning/Judgment, capture-evidence vs case-family) are the inventory's reading of current docs and are surfaced for owner adjudication, not asserted as final.
- Subagent `likely_owner` signals were adjudicated by the main agent; any residual `unclear` is flagged as an open question, not forced into a label.
```
