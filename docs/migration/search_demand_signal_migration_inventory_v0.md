# Search / Demand-Signal — Spine-First Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration inventory record (inventory-only marking artifact)
scope: >
  Inventory-only marking artifact for the Search / Demand-Signal lane during the
  spine-first repo migration. Identifies every Search / Demand-Signal document,
  prompt, workflow, decision, review, fixture, and runtime/code surface that
  should be considered during the migration; classifies each as owned / used-by /
  feeds-global; proposes future allocation; and marks the Search-vs-Capture
  boundary. No moves, renames, code changes, or doctrine changes.
use_when:
  - Planning or sequencing the Search / Demand-Signal slice of the spine-first migration.
  - Deciding whether a demand-signal / search / answer-engine surface belongs to the lane.
  - Orienting a fresh agent on what the Search lane owns vs consumes vs feeds.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_search_product_lane_binding_v0.md
  - docs/product/search/README.md # nonresolving: retired without successor; resolve via docs/migration/repo_structure_spine_first_v0/moved_paths_index.md
  - docs/migration/repo_structure_search_lane_v0/moved_paths_index.md
stale_if:
  - The search-lane binding inclusion test / precedence rule is amended or superseded.
  - docs/product/search/ membership changes (a doc is added, removed, or re-homed).
  - A later accepted Orca decision re-draws the Search / Capture / Judgment boundary.
  - repo-structure.yaml product_lanes changes the search lane or its status.
```

## Status & provenance

- Status: `INVENTORY_ONLY_V0` — a marking/discovery artifact, not a migration plan,
  not an authorization, not doctrine. Allocations below are **proposed**.
- Base: read against `origin/main @ c417622d` (the merge of the search-lane
  provenance/hygiene PR #241, on top of the lane-creation PR #236). Pending PRs on
  other branches are **not** assumed merged.
- Authority for what the lane owns is `docs/decisions/orca_search_product_lane_binding_v0.md`
  (the inclusion test + precedence rule). This inventory **reads** that record; it
  does not re-decide it.
- Companion wave: this is the Search slice of a coordinated set of spine-first
  migration inventories in flight on sibling branches (cleaning-spine, ecr,
  foundation-layer, product-lead/buyer-proof, ontology-structure,
  global-prompt-review). Boundary calls here should be reconciled against those
  inventories before any cross-lane move (see §8).

## Lane identity (from the binding, verbatim-anchored)

The lane is Orca's **demand-signal intelligence (search-led)** vertical. Its
**inclusion test** admits a doc whose reason-to-exist is either:
- (a) the **search / answer-engine surface** itself (how Orca captures it, what it
  exposes, or its source-class — web search / SERP, Google AI Overviews & other
  answer engines, zero-click, AEO/GEO, search-interest / "trends"); OR
- (b) the **demand-signal discovery method** those surfaces feed — the scan method,
  the demand-read grammar/taxonomy, and the demand gates that adjudicate signal.

**Precedence:** when a doc is both in-scope here and spine-functional, topic-primacy
wins (it lives in `search/`); every artifact keeps exactly one physical home.

**Important boundary — Search ≠ Capture.** Search *discovers, qualifies, and routes*
candidate demand signal (the read/scan/gate **method** + the search-interest
**surface**). Capture (Data Capture Spine / Source Capture Toolbox) owns *source
acquisition and packet production* (durability capture of retail price / availability
/ review venues, Reddit intake, IG creator capture, the harness adapters/runners).
The two meet at the `demand_durability_indicator_*` family, which is **split** by
venue (see §5 and §7).

---

## 1. Current repo surfaces found

Grouped by area. `[OWN]` owned by Search, `[USE]` used-by/owned-elsewhere,
`[FEED]` feeds-Search/global, `[HIST]` Search-subject historical record in a
by-type folder, `[CAP]` Capture-owned boundary surface, `[EXCL]` explicitly
excluded by the binding.

### docs/product/search/ — the bound lane home (11 files) `[OWN]`
- `README.md` — lane front-door index.
- `aeo_capture_feasibility_probe_phase0_v0.md` + `..._evidence.json` — AEO answer-engine capture feasibility probe (ChatGPT + Google AIO), GO verdict + evidence.
- `demand_search_interest_sourcing_and_gate_delta_spec_v0.md` — search-interest / AEO source-classes + gate-read placement (the "#228" spec).
- `demand_durability_indicator_search_interest_capture_profile_v0.md` — capture obligations for the **search-interest** durability indicator.
- `orca_demand_scan_core_spec_v0.md` — the scan-function method spec.
- `orca_demand_read_taxonomy_v0.md` — the demand-read grammar (signal layers, read types, wind-caller machinery, durable/transient/manufactured model).
- `orca_demand_read_taxonomy_adjudication_v0.md` — adjudication-prep companion.
- `orca_demand_scan_gate_adjudication_packet_v0.md` — owner decision packet for the first live scan.
- `orca_demand_gate_definition_closures_proposal_v0.md` — ratified Demand-Substrate Hard Gate definitions (G1/G2/G4).
- `orca_demand_gate_run_commission_criteria_v0.md` — criteria for commissioning one candidate through the gate.

### docs/decisions/ — lane authority + dependencies
- `orca_search_product_lane_binding_v0.md` `[OWN]` — the lane's controlling decision (inclusion test, precedence, scope).
- `wind_caller_calibration_carveout_v0.md` `[USE]` — owner-signed naming boundary the read-taxonomy's wind-caller machinery binds (lives in decisions/; §6 of scan-core consumes it).
- `orca_product_thesis_consumer_demand_v0.md` `[FEED]` — origin of the durable/transient/manufactured demand-state model the taxonomy uses; global anchor (OWNER_LOCKED).
- `orca_icp_wedge_consumer_demand_first_v0.md` `[FEED]` — the wedge scoping the demand work; product-lead/global.
- `orca_consumer_demand_ratification_decision_memo_v0.md` `[FEED]` — ratifies the consumer-demand thesis/wedge the lane serves.

### docs/migration/ — the lane's own migration package `[OWN]` (meta)
- `repo_structure_search_lane_v0/` — `moves_manifest.csv`, `apply_moves.py`, `runbook.md`, `reference_inventory.md`, `moved_paths_index.md` (the 10-doc physical co-location that created the lane).

### docs/prompts/ — commissioning + review prompts (by-type folder) `[HIST]`
- `product-planning/consumer_demand_scanning_lane_commission_prompt_v0.md` — commissioned the scan-core/read-taxonomy work.
- `product-planning/demand_substrate_gate_paper_check_commission_prompt_v0.md` — demand-substrate gate paper-check (feeds the gate-definition docs).
- `product-planning/consumer_demand_probe_stage1_feasibility_commission_prompt_v0.md` — consumer-demand probe stage-1 feasibility.
- `product-planning/icp_product_direction_lane_commission_prompt_v0.md` — ICP/product-direction lane (commissions adjudication of the scan/gate work).
- `product-planning/chatgptpro_beauty_subniche_research_prompt_v0.md` — ChatGPT-Pro answer-engine discovery research prompt (answer-engine surface, but research).
- `reviews/orca_demand_scan_core_spec_delegated_adversarial_review_patch_prompt_v0.md` — review prompt for the owned scan-core spec.
- `handoffs/demand_durability_series_writer_step2_handoff_v0.md`, `handoffs/demand_durability_cadence_runner_step3_handoff_v0.md` `[CAP]` — demand-durability **capture** handoffs (data-capture side).

### docs/research/ — discovery research `[FEED]`/`[EXCL]`
- `orgmotion_demand_signal_wedge_discovery_v0.md` — org-motion demand-signal wedge discovery (research).
- `orgmotion_signal_interpretation_intent_vs_realization_v0.md` — signal interpretation research feeding the read-grammar.
- `orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md` `[EXCL]` — answer-engine discovery artifact, **explicitly excluded** by the binding.
- `orca_discovery_candidate_scan_beauty_subniche_chatgptpro_v0.md` `[FEED]` — sibling answer-engine discovery artifact (same class as the excluded one).

### docs/review-outputs/ — review history of owned docs `[HIST]`
- `adversarial-artifact-reviews/orca_demand_scan_core_spec_delegated_adversarial_review_patch_review_v0.md` — review output for scan-core.
- `adversarial-artifact-reviews/demand_gate_definition_closures_cross_vendor_adversarial_artifact_review_v0.md` — review output for the demand-gate-definition closures.

### docs/product/judgment_spine/ — consumers of the read-taxonomy `[USE]`
- `judgment_spine_demand_read_machinery_architecture_v0.md`, `judgment_spine_demand_read_grading_rubric_v0.md`, `judgment_spine_c3_verdict_action_ceiling_contract_v0.md`, `judgment_spine_c2_ledger_read_contract_v0.md` (includes folded Rule 3), `judgment_spine_first_demand_read_scope_v0.md`, `demand_read_core_adoption_and_ledger_first_direction_v0.md` — Judgment Spine machinery that **consumes** the search-owned demand-read taxonomy; Judgment-owned.

### docs/product/data_capture_spine/ — Capture boundary `[CAP]`/`[EXCL]`/`[FEED]`
- `demand_durability_indicator_price_timeseries_capture_profile_v0.md`, `..._availability_restock_capture_profile_v0.md`, `..._review_velocity_corpus_capture_profile_v0.md` `[EXCL]` — the **non-search** durability indicators (retail venues); **explicitly excluded** by the binding; capture-owned; they **feed** the demand-state read.
- `demand_durability_indicator_capture_deconfliction_note_v0.md` `[CAP]` — the note that **deconflicts** the split between the search-interest profile (→ search/) and the retail durability profiles (stay in capture). The seam doc.
- `demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md`, `demand_durability_multi_retailer_rendered_capture_spec_v0.md`, `demand_durability_us_storefront_pin_recon_verdict_v0.md`, `demand_durability_capture_pilot_v0.md`, `capture_envelope_durability_delta_spec_v0.md` `[CAP]` — demand-durability capture mechanics; capture-owned.
- `core_spine_v0_data_capture_spine_obligation_contract_v0.md`, `data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` `[FEED]` — capture obligation contracts the search-interest capture profile defers to (envelope-of-record).

### docs/product/core_spine/ — shared WHERE/ontology substrate `[USE]`/`[FEED]`
- `orca_vertical_exploration_guide_v0.md`, `beauty_venue_card_set_v0.md` `[USE]` — the WHERE/venue layer the scan-core spec layers on (scan-core `open_next` cites both).
- `orca_ontology_backbone_architecture_v0.md`, `ontology_expansion_backlog_v0.json`, `ontology_cards/` `[FEED]` — the ontology backbone the read-grammar references; multi-lane shared foundation.

### docs/product/product_lead/ — the Hard Gate + proof consumers `[USE]`/`[FEED]`
- `orca_buyer_proof_packet_v0.md` `[USE]` — carries the live Demand-Substrate Hard Gate the gate-definition-closures doc defines/aligns with (bidirectional dependency).
- `orca_offer_hypothesis_v0.md`, `orca_product_proof_lead_charter_v0.md`, `orca_discovery_consumer_demand_target_selection_brief_v0.md`, `orca_discovery_batch_0_target_selection_brief_v0.md` `[FEED]` — product-lead docs that consume demand reads / set discovery targets; product-lead-owned.

### orca-harness/ — runtime/code & test surfaces (see §6)
- **No Search/Demand-Signal-owned runtime** exists. The demand-scan/read/gate method is **spec-only** (docs).
- `runners/run_source_capture_durability_series.py`, `tests/unit/test_source_capture_durability_series.py` `[CAP]` — demand-**durability capture** series runner/test; capture-owned, not search.
- `cases/product_learning/topicals_retail_expansion_2021_v0/first_demand_read_findings_v0.md` `[USE]` — a product-learning **case fixture** that *applied* the demand-read; judgment/harness-owned consumer.

### External to the repo (named, not a repo surface) `[note]`
- `C:\Users\vmon7\aeo_tools\gemini_query_graph_mapper.py` (+ `analyze_graph.py`) — the AEO query-graph probe tooling used by the feasibility probe. **Outside the repo by design** (scratch dir). No in-repo AEO/query-graph code exists. Flagged so a migrator does not assume the probe is backed by repo code.

---

## 2. Proposed future allocation

The spine-first migration's apparent target is a single physical home per lane.
For Search / Demand-Signal that home is **`docs/product/search/`** (already bound &
populated). Proposed allocation, by class:

| Class | Proposed home | Move now? |
| --- | --- | --- |
| The 11 lane docs | `docs/product/search/` (current) | already there — no move |
| Lane binding | `docs/decisions/` (current) | stay — decisions are by-type, not by-lane |
| Migration package | `docs/migration/repo_structure_search_lane_v0/` | stay |
| Review/prompt history of owned docs `[HIST]` | `docs/prompts/…`, `docs/review-outputs/…` (current) | **owner decision (§8)** — stay (point-in-time, type-filed) vs. lane-index |
| Judgment consumers `[USE]` | `docs/product/judgment_spine/` | stay — Judgment-owned |
| Capture durability profiles `[CAP]`/`[EXCL]` | `docs/product/data_capture_spine/` | stay — Capture-owned |
| Core-spine substrate `[USE]`/`[FEED]` | `docs/product/core_spine/` | stay — shared foundation |
| Product-lead consumers `[FEED]` | `docs/product/product_lead/` | stay — product-lead-owned |

Net: **the physical lane move is essentially complete** (done by #236/#241). The
remaining migration work for this lane is **nav/seam hygiene**, not file moves
(see §7, §9).

## 3. Owned by Search / Demand-Signal

Reason-to-exist IS a search/answer-engine surface OR the demand-signal discovery method:

- **Core (in `docs/product/search/`):** the 11 files listed in §1 — 4 search/answer-engine surfaces (AEO probe + evidence, search-interest sourcing/gate-delta spec, search-interest capture profile) and 6 demand-signal method docs (scan-core, read-taxonomy + adjudication, scan-gate adjudication packet, gate-definition closures, gate-run commission criteria), plus the lane `README.md`.
- **Lane authority & meta:** `docs/decisions/orca_search_product_lane_binding_v0.md` and the `docs/migration/repo_structure_search_lane_v0/` package.
- **Owned-subject historical records (type-filed, `[HIST]`):** the scan-core review prompt + output, the demand-gate-definition-closures review, and the demand-scan/gate commission prompts. Their *subject* is owned by Search; their *home* is the by-type prompt/review folders. Recommendation: **leave in place** (consistent with the lane migration's reference-model-B: historical records keep their location and resolve via the moved-paths index), and surface them from the lane README rather than move them. Owner decision in §8.

**Consumed-by (Search owns, others read):** the demand-read taxonomy and gate
definitions are consumed across the Judgment, Data-Capture, and Core spines (see
the README "Consumed by" section). Ownership stays with Search; the consumers stay
where they are. This is the lane's defining "venue-spanning method" property.

## 4. Used by Search but owned elsewhere

Search's method depends on these; each is owned by one identifiable sibling lane and
**moves with that lane, not Search**:

- `core_spine/orca_vertical_exploration_guide_v0.md` — the WHERE/walk mechanics scan-core layers on. (Core Spine)
- `core_spine/beauty_venue_card_set_v0.md` — the venue layer scan-core reads at Step 0. (Core Spine)
- `product_lead/orca_buyer_proof_packet_v0.md` — the live Demand-Substrate Hard Gate the gate-definition doc defines/aligns with (bidirectional). (Product Lead)
- `decisions/wind_caller_calibration_carveout_v0.md` — the wind-caller naming boundary the read-taxonomy binds. (Decisions)
- `decisions/orca_product_thesis_consumer_demand_v0.md` — the demand-state model origin. (Decisions / global)
- `orca-harness/cases/.../first_demand_read_findings_v0.md` — a case fixture that applied the demand-read. (Judgment / harness)
- The Judgment Spine read-machinery / grading / verdict / ledger contracts (§1) — these are *consumers* of the taxonomy, owned by Judgment; listed here because a migrator tracing "demand-read" references will land on them.

## 5. Feeds Search but should remain global / shared

Upstream signal producers and shared foundations that feed demand reads but are
multi-consumer or another spine's responsibility — **do not pull into Search**:

- **Data-Capture durability profiles** (`demand_durability_indicator_price_timeseries…`, `…availability_restock…`, `…review_velocity_corpus…`) — produce the retail durability signals the demand-state read consumes; Capture-owned; **the binding explicitly excludes them** (different venues).
- `data_capture_spine/demand_durability_indicator_capture_deconfliction_note_v0.md` — the seam that documents the search-interest-vs-retail split; capture-owned but load-bearing for the boundary.
- The data-capture obligation contracts (`core_spine_v0_data_capture_spine_obligation_contract_v0.md`, corpus-intake contract) — the envelope-of-record the search-interest capture profile defers to.
- `core_spine/orca_ontology_backbone_architecture_v0.md` (+ cards/backlog) — shared ontology feeding the read-grammar and many other lanes.
- The consumer-demand thesis / wedge / ratification memo — global product anchors.
- The ChatGPT-Pro / org-motion discovery research artifacts (`docs/research/…`) — discovery inputs; research, not method (one is the binding's explicit exclusion).

## 6. Runtime / code surfaces and test surfaces

- **No Search/Demand-Signal-owned runtime or code exists in the repo.** The
  demand-scan, demand-read, and demand-gate work is **method specification only**
  (docs in `docs/product/search/`). A fresh agent must not assume a scan/read/gate
  engine is built.
- The only demand-adjacent harness code is **Capture-owned**: `orca-harness/runners/run_source_capture_durability_series.py` and `orca-harness/tests/unit/test_source_capture_durability_series.py` implement demand-**durability capture series** (data-capture), plus retail/PDP and source-capture surfaces. These migrate with **Data Capture**, not Search.
- **Test/fixture surface that *applies* the method:** `orca-harness/cases/product_learning/topicals_retail_expansion_2021_v0/first_demand_read_findings_v0.md` is a product-learning case fixture that used the demand-read; it belongs to the Judgment/harness case corpus.
- **External tooling (not in repo):** the AEO query-graph probe (`gemini_query_graph_mapper.py`, `analyze_graph.py`) lives in `C:\Users\vmon7\aeo_tools\` outside the repo. If a future decision brings answer-engine probing in-repo, a `search/` runtime home would need to be created — it does not exist today.

## 7. Stale naming / stale placement risks

1. **Repo map has no Search lane section.** `docs/workflows/orca_repo_map_v0.md`
   gives every other spine (Data Capture, ECR, Judgment, Core) a dedicated
   navigable section, but Search appears **only** as one row in "Workstream Status
   Pointers" (line ~807). The lane's 11 docs are not enumerated in any navigable
   map section. *Highest-value nav gap.*
2. **`demand_durability_indicator_*` prefix is split across two homes.** The
   search-interest profile lives in `search/`; the price/availability/review
   profiles live in `data_capture_spine/`. A reader seeing the shared prefix may
   assume one lane. The deconfliction note mitigates but the naming collision is a
   discoverability risk.
3. **Folder name vs concept name.** The folder is `search/` but the bound identity
   is "demand-signal intelligence (search-led)"; a migrator may hunt for a
   `demand_signal/` home that does not exist. (This task itself names it "Search /
   Demand Signal.")
4. **Old-home provenance inside moved docs.** The 6 method docs were authored under
   `core_spine/` / `product_lead/` and moved to `search/`. Internal `branch_or_commit`
   lines, status notes, and some prose still reference the authoring homes; the
   `input_hashes` provenance pins were largely reconciled by #241 but a documented
   **25-pin / 19-ledger residual** of point-in-time pins to old paths remains
   (accepted, not blocking).
5. **Historical references resolve only via the moved-paths index.** Decisions /
   reviews / prompts that cite the pre-move paths depend on
   `docs/migration/repo_structure_search_lane_v0/moved_paths_index.md`; a migrator
   consolidating folders must preserve that index.

## 8. Open questions for the owner

1. **Historical artifact co-location.** Do the type-filed review/prompt records of
   owned docs (scan-core review prompt+output, demand-gate review, demand-scan
   commission prompts) stay in `docs/prompts/` & `docs/review-outputs/`
   (reference-model-B default), or get surfaced/indexed under the lane? Inventory
   recommendation: **stay + index from the README**; confirm.
2. **`demand_durability_indicator_*` naming split.** Accept the shared prefix across
   `search/` and `data_capture_spine/` (documented by the deconfliction note), or
   rename to disambiguate (e.g., `search_interest_*` vs `retail_durability_*`)?
3. **Repo-map Search section.** Add a dedicated Search-lane section to the repo map
   for parity with the other spines? (Inventory recommends yes; §9.)
4. **wind-caller boundary.** The read-taxonomy owns "wind-caller" demand-signal
   machinery (Search), while `source_capture_toolbox/ig_wind_caller_*` owns IG
   wind-caller **capture** (Capture). Confirm the concept-vs-capture split so the
   shared term is not mistaken for one lane.
5. **Search-vs-Judgment seam.** The read-taxonomy is owned by Search but consumed
   heavily by Judgment (read-machinery, grading, verdict). Confirm Search keeps
   ownership of the *grammar* while Judgment owns the *grading/verdict* application.
6. **Cross-inventory reconciliation.** This lane's `[USE]`/`[FEED]`/`[CAP]` calls
   must agree with the sibling inventories (capture / judgment / core / product-lead).
   Which inventory is authoritative where two claim the same doc?

## 9. Suggested migration order

The physical lane move is already done (#236/#241). Remaining, lowest-risk first:

1. **Close the nav gap** — add a dedicated Search-lane section to
   `docs/workflows/orca_repo_map_v0.md` enumerating the 11 docs and pointing at the
   binding + README (mechanical; high discoverability payoff).
2. **Resolve the historical-artifact question (§8.1)** — decide stay-vs-index, then
   either index from the README or (if chosen) move with a reference rewrite.
3. **Settle the naming split (§8.2)** — accept-and-document or rename the
   `demand_durability_indicator_*` family; if rename, coordinate with Data Capture.
4. **Reconcile boundaries with sibling inventories (§8.6)** before any cross-lane
   move — especially the Capture durability profiles and the Judgment consumers.
5. **(Optional) settle the provenance residual** — the 25-pin / 19-ledger old-path
   residual and any old-home prose inside the moved method docs.
6. **Defer any `search/` runtime home** until/unless a decision authorizes bringing
   answer-engine probing in-repo (none today).

## 10. Explicit non-claims

- **Inventory only.** No file was moved, renamed, deleted, or re-homed; no code
  changed; no doctrine changed. Allocations are **proposals** for owner adjudication.
- This artifact is **not** validation, readiness, acceptance, or product proof.
- It does **not** re-decide the lane binding; `orca_search_product_lane_binding_v0.md`
  remains the inclusion-test authority. Where this inventory and the binding differ,
  the binding wins.
- Ownership/`[USE]`/`[FEED]`/`[CAP]` labels are **placement proposals**, not
  authority transfers; a sibling-lane inventory may claim a shared doc differently
  (reconcile per §8.6).
- Read against `origin/main @ c417622d`; **pending PRs on other branches are not
  assumed merged**, and the sibling spine-first inventories are in flight, not
  landed.
- The Search-vs-Capture boundary statements are the inventory's reading of current
  docs; the deconfliction note and the binding govern on conflict.
- No ToS/legal/sourcing posture is asserted or changed; the AEO probe's own
  non-claims are unchanged.
```
