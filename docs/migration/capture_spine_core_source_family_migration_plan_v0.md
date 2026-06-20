# Capture Spine Core / Source-Family Migration Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration plan (Capture spine internal structure; docs-only)
scope: >
  Plans a future current-capture-spine-only re-home from
  orca/product/spines/capture/{contracts,operating_model,packet_schema,
  demand_durability_indicators,source_capture_toolbox,source_families}/ into a
  proposed capture/core/ reusable layer, including a social_media grouping under
  capture/core/source_families/. No file moves, no runtime work, no satellite
  migration, and no validation/readiness claim.
use_when:
  - Planning an internal Capture spine structure migration before any file moves.
  - Checking whether capture/core/ or source_families/social_media/ is a proposed amendment or already accepted placement.
  - Sequencing a future capture-only move table and downstream map/reference updates.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/migration/capture_spine_source_capture_migration_inventory_v0.md
branch_or_commit: codex/capture-spine-core-migration-plan @ 35066b15
stale_if:
  - Any file under orca/product/spines/capture/ is moved, renamed, deleted, or added.
  - A later accepted Orca decision amends the Capture spine target tree, the source-family phase convention, or the Source Capture Toolbox home.
  - A future execution pass creates capture/core/ or source_families/social_media/ and updates the owning maps.
```

- Status: `MIGRATION_PLAN_ONLY`.
- Scope: current files under `orca/product/spines/capture/**` only.
- Execution note (2026-06-21): the accepted follow-on execution moved the
  current Capture files under `capture/core/` in commit
  `a75c337b3497d530f9b7fbfb25acb0fd230d3616`; current structure authority lives
  in `docs/decisions/orca_spine_first_target_structure_binding_v0.md` and the
  git rename diff. The plan text below remains historical planning evidence.
- Current inventory basis: 103 current Capture spine files in this worktree:
  `contracts` 8, `demand_durability_indicators` 8, `operating_model` 35,
  `packet_schema` 3, `source_capture_toolbox` 28, `source_families` 21.
- This plan does not move, rename, delete, validate, or authorize
  runtime/source-access work by itself.
- The target paths below are proposed future paths. They are not current
  accepted placement until a later accepted execution pass updates the owning
  structure sources and physically moves the files.

## Source-Authority Check

Loaded sources and planning result:

| Source | Relevant finding |
| --- | --- |
| `.agents/workflow-overlay/artifact-folders.md` | `docs/migration/` is an accepted migration-record folder. `orca/product/` is the spine-first product tree; per-spine structure is owned by the spine-first binding, not the machine map. |
| `docs/decisions/orca_spine_first_target_structure_binding_v0.md` | Current accepted Capture target is flat under `capture/`: `contracts`, `operating_model`, `packet_schema`, `source_capture_toolbox`, `demand_durability_indicators`, and `source_families/{retail_pdp,reddit,instagram,youtube,tiktok,answer_engine}`. It also binds source-family phase separation and says IG/YT/TT are source families, not peer spines. |
| `repo-structure.yaml` | Declares `orca` as a top-level area and explicitly says per-spine structure is owned by the spine-first binding. It does not currently enumerate Capture subdirectories. |
| `docs/workflows/orca_repo_map_v0.md` | Routes `orca/product/spines/capture/` as the acquisition-side spine and names current subdirs flat under `capture/`; calls Capture dense and routes detail through the Capture submap. |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Current Capture submap routes to flat Capture homes and current source families: `retail_pdp` and `instagram`. It is a map, not source authority, but must be updated after a future move. |
| `docs/migration/capture_spine_source_capture_migration_inventory_v0.md` | Prior inventory classified Capture, Toolbox, source-family, runtime, search, IG, and downstream boundaries. It flagged IG as absent formal lane binding at the time; later spine-first execution placed IG under Capture source families. |
| `docs/migration/phase2_proposals/*capture*_w3a_proposal_v0.md` | Advisory deletion/ontology scans only. They do not authorize deletion in this migration plan; they do identify files that a future execution pass must not treat as unexplored. |

Advisory answer to the source-authority prompt:

1. `capture/core/` does not fit the currently accepted flat Capture target tree;
   therefore it must be framed as a proposed amendment, not as already accepted
   current placement. It does not conflict with `repo-structure.yaml` because the
   machine map does not own per-spine internals.
2. Grouping `instagram`, future `tiktok`, and future `youtube` under
   `source_families/social_media/` does not violate the source-family phase
   convention as long as the grouping remains under Capture's acquisition-side
   `source_families/`. It does amend the accepted flat member paths and therefore
   needs a future structure update.
3. Future execution must update route maps and old-path references, at minimum:
   `docs/decisions/orca_spine_first_target_structure_binding_v0.md`,
   `docs/workflows/orca_repo_map_v0.md`,
   `docs/workflows/data_capture_spine_consolidation_map_v0.md`,
   `.agents/workflow-overlay/source-loading.md` if any read packs name moved
   paths, `docs/migration/spine_first_target_move_table_v0.md` or a successor
   move table, `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md`
   or a successor moved-path index, and the three Phase-2 capture proposals whose
   `stale_if` conditions would fire after movement.
4. Guardrails: call this a plan, target, or proposed amendment; do not call it
   execution, validation, readiness, approval, source promotion, or proof. Do not
   imply satellites, harness code, Search/scanning docs, or runtime work moved.

## Target Shape

Recommended future shape for the current Capture spine only:

```text
orca/product/spines/capture/
  README.md                         # optional future index, not created by this plan
  core/
    contracts/
      candidate_intake/
      corpus_intake/
      obligation_contracts/
      source_access_boundary/
    demand_durability_indicators/
      availability_restock/
      price_timeseries/
      review_velocity/
      search_interest/
    cadence_and_missingness/         # future reserved core category; no current folder
    operating_model/
    packet_schema/
    source_quality/                  # extraction candidate, not first-wave default
    source_capture_toolbox/
    source_families/
      retail_pdp/
      web_search_capture/            # future reserved family; no current files
      social_media/
        instagram/
        tiktok/                     # future reserved family; no current files
        youtube/                    # future reserved family; no current files
```

`capture/core/` means the reusable acquisition layer inside the Capture spine.
It is not a peer to `orca/product/spines/`, not a product satellite, and not a
runtime root.

`social_media/` is a source-family grouping, not a new spine or satellite. It
groups social-media source mechanics under the Capture acquisition phase. It
does not authorize TikTok or YouTube capture behavior and does not inherit IG
rules into those families.

`source_quality/` belongs in the target core vocabulary because source quality is
not the same concern as route/tool selection. Current source-quality files are
still indexed as Source Capture Toolbox components, so extraction should be a
second wave unless the owner accepts a larger reference rewrite.

`cadence_and_missingness/` belongs in the target core vocabulary, but no current
Capture Spine folder maps cleanly to it. Do not invent it by moving pressure-test
or demand-durability docs merely because those docs discuss cadence.

## Classification Rules

| Class | Rule | Future treatment |
| --- | --- | --- |
| `core_contract` | Capture obligations, source-access boundary, candidate/corpus intake, packet contract, or posture vocabulary. | Move under `capture/core/contracts/` or `capture/core/packet_schema/`. |
| `core_operating_model` | Capture operating model, commissioning, pressure-test operating docs, accepted operating-model versions, and current Capture backlog. | Move under `capture/core/operating_model/`; do not archive/delete in this plan. |
| `core_indicator_profile` | Capture-owned demand-durability indicator profiles and capture envelope deltas. | Move under `capture/core/demand_durability_indicators/`. |
| `core_toolbox` | Source Capture Toolbox/Armory route catalog, playbook, anti-block ladder, browser/archive/reddit/source-quality support, and subsystem README. | Move as a unit under `capture/core/source_capture_toolbox/` first. Internal extraction is deferred. |
| `core_source_quality` | Reusable source-quality posture, queues, assemblers, and closeouts currently housed inside the Toolbox. | Target `capture/core/source_quality/`, but defer extraction until references and the Toolbox README are rewritten. |
| `core_source_family` | Source-family-specific capture/projection mechanics. | Move under `capture/core/source_families/<family>/`; social platforms use `social_media/<platform>/`. |
| `future_empty_family` | Target home for a family with no current capture-spine files. | Name in the plan only; create no empty directory unless a later execution pass accepts placeholder indexes. |
| `non_move_current_scope` | Satellite, case-family, scanning/search, harness runtime, review output, decision record, or workflow map outside `orca/product/spines/capture/**`. | Do not move in this plan. Update references only in a future execution pass. |
| `possible_deletion_elsewhere` | File named by Phase-2 deletion proposals. | Retain/move as-is unless a separate deletion pass is accepted and executed first. |

## Proposed Move Table

This is a planning table, not an execution manifest. Counts are current files in
this worktree.

| Current path pattern | Proposed future path pattern | Count | Treatment | Notes |
| --- | --- | ---: | --- | --- |
| `orca/product/spines/capture/contracts/**` | `orca/product/spines/capture/core/contracts/**` | 8 | direct grouped move | Includes current obligation, candidate intake, corpus intake, and source-access boundary files. Retain the posture vocabulary proposal unless a separate deletion pass removes it first. |
| `orca/product/spines/capture/packet_schema/**` | `orca/product/spines/capture/core/packet_schema/**` | 3 | direct grouped move | Keeps packet schema and typed-payload boundary under reusable core. |
| `orca/product/spines/capture/operating_model/**` | `orca/product/spines/capture/core/operating_model/**` | 35 | direct grouped move with archive/deletion deferred | Includes v0/v1/v2 operating-model history and pressure-test/session docs. Phase-2 deletion candidates v0/v1 are not deleted by this plan. |
| `orca/product/spines/capture/demand_durability_indicators/**` | `orca/product/spines/capture/core/demand_durability_indicators/**` | 8 | direct grouped move | Keeps `search_interest` as a Capture-owned durability indicator profile, not a Search lane. |
| `orca/product/spines/capture/source_capture_toolbox/**` | `orca/product/spines/capture/core/source_capture_toolbox/**` | 28 | direct grouped move as subsystem unit | Preserve Toolbox as the named Capture subsystem for the first wave. |
| `orca/product/spines/capture/source_capture_toolbox/source_quality_*` | `orca/product/spines/capture/core/source_quality/` | 8 | deferred extraction candidate | Better target category, but extraction requires reference/index rewrite and should not ride the wrapper wave silently. |
| `orca/product/spines/capture/source_families/retail_pdp/**` | `orca/product/spines/capture/core/source_families/retail_pdp/**` | 6 | direct grouped move | Retail/PDP stays a Capture source family, not a fragrance/beauty satellite. |
| `orca/product/spines/capture/source_families/instagram/**` | `orca/product/spines/capture/core/source_families/social_media/instagram/**` | 15 | direct grouped move after structure acceptance | IG becomes the first populated social-media capture family. Do not infer TikTok/YouTube behavior from IG. |
| none currently under Capture | `orca/product/spines/capture/core/source_families/web_search_capture/` | 0 | future reserved home only | Name is user-preferred, but current binding uses `answer_engine`; resolve naming before creation. |
| none currently under Capture | `orca/product/spines/capture/core/source_families/social_media/tiktok/` | 0 | future reserved home only | Create only with a future TikTok recipe/recon/index artifact or accepted placeholder convention. |
| none currently under Capture | `orca/product/spines/capture/core/source_families/social_media/youtube/` | 0 | future reserved home only | Create only with a future YouTube recipe/recon/index artifact or accepted placeholder convention. |
| none currently under Capture | `orca/product/spines/capture/core/cadence_and_missingness/` | 0 | future reserved core category only | Do not create or populate until a file actually owns reusable cadence/missingness doctrine. |

## Ambiguous / Deferred Queue

These items should not block writing this plan, but they should shape a future
execution pass:

| Item | Why deferred | Recommended handling |
| --- | --- | --- |
| `source_quality_*` files under `source_capture_toolbox/` | User's target model includes `source_quality/` as a core category, but current maps index these as Toolbox components. | First wrapper execution may keep them under `core/source_capture_toolbox/`; extraction to `core/source_quality/` should be a deliberate second wave. |
| Operating-model v0/v1 history | Phase-2 W3a proposed deletion candidates, but deletion would sever historical prompt/review hash anchors unless adjudicated. | Retain/move in structure pass unless a separate deletion-evidence pass executes first. |
| `data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` | Phase-2 W3a marked it as absorbed by parent contract, but it still exists in current capture spine. | Retain/move in structure pass unless a separate deletion-evidence pass executes first. |
| IG lane vs source-family wording | Current placement has IG under Capture source families, while older inventory flagged no formal IG lane binding. | Treat IG as `social_media/instagram` source family, not a peer lane or satellite, unless a later owner decision creates an IG lane. |
| TikTok and YouTube | Accepted target structure previously named them as capture source families, but no current capture-spine files exist. | Reserve target convention in prose only; no empty directory creation in first move. |
| Web search / answer-engine capture | User wants "one for Search itself," but this plan is current Capture spine only and current capture files do not include a web-search source-family directory. | Defer to a later cross-spine Search/scanning/capture plan. Keep current `search_interest` indicator under `core/demand_durability_indicators/search_interest/`. |
| `cadence_and_missingness/` | Useful target category, but current files do not cleanly map to it without semantic splitting. | Reserve in target vocabulary only; do not create in first wave. |

## Non-Moves

This plan intentionally excludes:

- `orca/product/spines/scanning/**`, including scanning-side source families.
- `orca/product/satellites/**`, including future fragrance venue/source-profile
  homes.
- `orca/product/case_families/**`.
- `orca/product/shared/**`.
- `orca/product/spines/data_lake/**`.
- `orca-harness/**` runtime, tests, runners, adapters, or fixtures.
- `docs/decisions/**`, `docs/workflows/**`, `docs/prompts/**`,
  `docs/review-*`, `docs/research/**`, and `docs/hygiene/**` as moved content.

Future execution may update references in these excluded areas, but it must not
move their files as part of this capture-only migration.

## Execution Waves For A Future Pass

No execution is authorized here. If the owner accepts this plan, the safest
future sequence is:

1. Accept or amend the proposed internal Capture target shape:
   `capture/core/` and `source_families/social_media/`.
2. Decide whether a deletion pass runs before movement. If not, retain all 103
   current Capture files.
3. Create a move manifest and moved-path index for only the accepted current
   Capture paths.
4. Move the grouped directories into `capture/core/`, with IG moving to
   `core/source_families/social_media/instagram/`.
5. Rewrite live references in Capture docs, repo maps, source-loading packs,
   prompts that are not historical point-in-time records, and open_next
   retrieval metadata.
6. Update the Capture submap and top-level repo map to route through
   `capture/core/`.
7. Run placement/link/header/reference checks and report only observed results.
8. Leave TikTok, YouTube, web-search capture, satellites, and harness movement
   for separately accepted lanes.

## Future Validation Checklist

For a later execution pass only:

```powershell
git diff --check
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\header_index.py --strict
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_placement.py --check
rg -n "orca/product/spines/capture/(contracts|operating_model|packet_schema|demand_durability_indicators|source_capture_toolbox|source_families/(instagram|retail_pdp))" docs orca .agents
```

Expected future result: live references to moved current Capture paths should be
rewritten or explicitly historical/migration-index references. A green checker
is placement/link/header hygiene only, not validation or readiness.

## Non-Claims

- Not execution, validation, readiness, acceptance, source promotion, proof, or
  runtime authorization.
- Not a move manifest; path patterns above need a generated manifest before
  execution.
- Not deletion authorization; Phase-2 deletion candidates remain separate.
- Not a satellite migration and not a Search/scanning migration.
- Not authorization for IG, TikTok, YouTube, browser calibration, scraping,
  source access, live runs, harness code, tests, storage, scheduling, or
  production runtime.
- Not proof that `capture/core/` or `source_families/social_media/` is accepted
  current placement; those are proposed target amendments.
