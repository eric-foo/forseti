# Handoff Packet — Capture Playbook ↔ Capture-To-Lake Lane Synchronization

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet (cold cross-lane handoff — structural sync work unit; NOT a capture or lake-write authorization)
scope: >
  Cold handoff for synchronizing the capture playbook (Source Capture Toolbox)
  with every per-source capture-to-lake lane (bronze runners, lake tees,
  projections, cleaning adapters), so that any agent entering from the playbook
  reaches each source's full capture→lake→cleaning route without archaeology.
  Owner-directed 2026-07-05 after a measured discovery failure (fragrance-DB
  family). Proposes a three-way authority model for owner ratification; grants
  no capture-run, lake-write, or doctrine-edit authority by itself.
use_when:
  - A fresh lane is authorized to execute the capture-playbook/lake sync work unit.
  - Checking the proposed access/routing/lake authority split before ratifying it.
authority_boundary: retrieval_only
stale_if:
  - The Source Capture Toolbox README, source_families/ tree, or Data Capture submap is restructured.
  - The proposed authority model is ratified or amended by the owner (replace the Open Decision block).
  - origin/main advances such that the pinned compare targets no longer resolve.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-07-05
- created_by_lane: `claude/infallible-lederberg-80043c` session (Aphrodite sub-ontology + Fragrantica sourcing lane; SENDER — provenance only, not authority)
- workspace: the Orca/Forseti repo (github `eric-foo/orca`)
- handoff_path: `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md`
- expected_branch: start a fresh lane from `origin/main` @ `24c08287` or later
- expected_head: `24c08287` at authoring (re-verify; main moves fast)
- expected_dirty_state_including_handoff_file: this handoff file is untracked on the sender branch until committed; receiver starts clean
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: >
    Every capture source in Forseti runs one seamless, synchronized path from
    access (playbook) through capture packets into the bronze/silver lake and
    cleaning, discoverable cold from the standard entry points.
    (Owner-stated this session 2026-07-05: "they are to make the captures /
    dump to data lake stuff seamless and synchronized" — not a formal
    workflow-goal-framing output.)
- anchor_goal: >
    Home every per-source capture-to-lake lane in the capture spine's
    source_families/ tree as a lane index, wire the playbook/submap/repo-map
    pointers to it, and get the proposed authority model ratified — so the
    fragrance-DB discovery failure class cannot recur silently.
- success_signal: >
    A cold agent given only "capture <source X> and land it in the lake"
    reaches, from the toolbox/playbook, source X's lane index naming the access
    route, the harness runners, the lake admission/storage contracts, and the
    cleaning seam — within the source-loading cold-lane budget — for EVERY
    source family with landed capture-to-lake code, not only fragrance-DB.

## Open Decision / Fork — the authority model (ratify BEFORE wiring pointers)

- decision: adopt the three-way authority split for capture knowledge.
  - options:
    1. **Proposed (owner-proposed, sender-refined):**
       (a) the capture playbook / Source Capture Toolbox is the AUTHORITY FOR
       ACCESS — rungs, anti-blocking ladder, ToS/access posture — and POINTS to
       each source's lane index; (b) a per-source lane index in
       `forseti/product/spines/capture/core/source_families/<family>/` is the
       ROUTING HOME tying access route + harness runners + lake contracts +
       cleaning seams together (the LinkedIn lane-index pattern); (c) the
       data_lake spine authority docs REMAIN the authority for
       admission/storage/bronze-silver contracts — the playbook never forks or
       restates lake doctrine. Pointers run both ways (playbook ↔ lane index ↔
       lake contracts).
    2. Playbook as single authority for the whole capture→lake path (owner's
       first phrasing, before the sender's pushback).
    3. Status quo (lanes documented wherever they were built).
  - already constrained / off the table: moving lake admission/storage
    authority out of the data_lake spine; rewriting doctrine inside the
    playbook; a new top-level folder scheme (source_families/ is the
    established home).
  - trade-offs: option 1 keeps each authority where its gates already live and
    adds only routing; option 2 would duplicate lake doctrine into the playbook
    (fork risk — the exact failure the overlay's single-owner rule exists to
    prevent); option 3 is the measured failure state.
  - owner of the call: Eric. (Owner asked "does it make sense? pushback if
    not" — the sender's pushback IS the option-1 refinement; the refinement is
    not yet owner-ratified.)
  - recommendation and why: option 1 — it matches existing ownership
    (toolbox=access weapons, data_lake spine=storage contracts) and fixes the
    failure with pure routing, no doctrine movement.

## Drift Guard

- **No capture runs, no lake writes, no runner edits from this packet.** This is documentation/index work; runtime work needs its own bounded authorization.
- **Do not fork lake doctrine into the playbook.** The data_lake spine authority docs stay the single owner of admission/storage/bronze contracts; the playbook and lane indexes point, never restate.
- **source_families/ is the home; do not invent a new scheme.** Follow the LinkedIn lane-index precedent (`data_capture_spine_linkedin_lane_index_v0.md`, whose own repo-map row says "open first").
- **Do not rewrite the two wall-of-text repo-map harness rows as part of this unit.** They are a separate hygiene concern; this unit only ADDS lane-index pointers (Quick Index rows / family rows). Repo-map edits are commit-once-whole (hook-enforced).
- **The existing docs/workflows handoff packets stay where they are** — they are historical lane records; the lane index POINTS to them rather than moving them (link, don't migrate).
- Land via per-lane PR flow; repo-map edits trigger the immediate explicit-path commit hook.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (+ `AGENTS.md`, `.agents/workflow-overlay/README.md` first; run the Forseti start-preflight).
- targets to enter the ladder (all on `origin/main`):
  - `forseti/product/spines/capture/core/source_capture_toolbox/README.md` — the playbook/armory index (the surface being synced).
  - `forseti/product/spines/capture/core/source_families/` — the routing home; note which families exist (retail_pdp, social_media/{instagram,tiktok,youtube}) and which are missing.
  - `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md` — the lane-index PATTERN to copy (note: it lives under the scanning spine; the capture-spine analog goes under capture's source_families/).
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md` — the Data Capture submap to wire.
  - `docs/workflows/forseti_repo_map_v0.md` — "Decisive-File Quick Index" section (add rows) + the two harness rows (lines ~688/~702 at authoring) that currently bury the runner inventory.
  - `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`, `docs/workflows/fragrantica_cleaning_audit_pack_handoff_v0.md`, `docs/workflows/parfumo_targeted_capture_contract_v0.md` — the confirmed-unhomed fragrance-DB lane records.
  - `forseti/product/spines/data_lake/authority/` — the lake contracts the lane indexes point at (do not restate).
- already loaded (weak orientation, freshness-marked; NOT authority): the sender swept these surfaces on 2026-07-05 at `origin/main` @ `24c08287`; the disconnect evidence below is from that sweep. Re-verify; main may have advanced.
- must load first (before any strict/actionable step): toolbox README + source_families/ listing + the LinkedIn lane index (pattern) + the repo-map freshness hook contract (`.agents/hooks/check_repo_map_freshness.py` header) since this unit edits map-described folders.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Owner access posture:** publicly accessible content is capturable; no credential use, no paywall/access-control bypass. Decided: owner statement 2026-07-04 in the sender session; corroborated by `forseti/product/spines/creator_signal/aphrodite_depth_capture_tos_risk_sanity_check_v0.md` ("discoverable/public material, visible through free/account-created access"). Verify before any access-posture claim.
- **Enforcement placement principle:** load-bearing mechanically-checkable rules live at tool boundaries (hooks), not instruction prose. Decided in: `.agents/workflow-overlay/validation-gates.md` → "Enforcement Placement" + `docs/decisions/overlay_enforcement_placement_classification_v0.md`. Verify before designing the candidate hook.
- **Repo-map hygiene conventions:** commit-once-whole map edits (hook-forced); one-note-per-change context in `docs/workflows/repo_map_recent_changes/`. Decided in: the map header + that folder's README. Verify before map edits.

## Active Objective

Inventory every per-source capture-to-lake surface in the repo (harness capture modules, bronze/lake tee runners, projections, cleaning adapters, and their docs/workflows lane records); home each unhomed family as a `source_families/<family>/` lane index on the LinkedIn pattern; wire toolbox README, Data Capture submap, and repo-map Quick Index pointers both ways; get the three-way authority model ratified and recorded; evaluate (not necessarily build) an enforcement hook so future lanes cannot land capture-to-lake code without a lane-index row.

## Exact Next Authorized Action

1. **Ratify the authority model with the owner (Open Decision above).** One question; do not wire pointers under an unratified split.
2. Run the inventory: enumerate per-source surfaces from `git ls-files orca-harness/source_capture orca-harness/runners orca-harness/cleaning` + `rg -il "<source name>"` over `docs/workflows` and `forseti/product/spines/{capture,data_lake,scanning}` — produce a family → {access route, runners, lake seams, cleaning adapters, lane records, homed?} table. Confirmed-unhomed seed: fragrance-DB (Fragrantica/Parfumo/basenotes). Candidate to check: the fragrance purchase-review family (`fragrance_review_*.py` — may or may not shelter under retail_pdp), Reddit surfaces, historical/Wayback capture.
3. For each unhomed family: author the lane index in `forseti/product/spines/capture/core/source_families/<family>/`, then wire the three pointer surfaces (toolbox README row, Data Capture submap row, repo-map Quick Index row). Repo-map edit commits immediately, explicit-path, per hook.
4. Record the ratified authority model as a dated note where the owner directs (likely the toolbox README head or a docs/decisions record) with its `direction_change_propagation` receipt (workflow_authority trigger).
5. Evaluate the enforcement candidate: an advisory session-start or commit-time check — new module under `orca-harness/{source_capture,runners,cleaning}` whose source family has no lane index → nudge. Propose to owner; build only if authorized.
6. Validation / stop: cold-retrieval spot test per Success Signal (one agent, one source family, playbook entry, within budget); all repo-map/doc hooks green; stop if the inventory reveals a family whose lake seam contradicts data_lake authority docs (that is a finding for the owner, not a silent fix).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (start-preflight, source hierarchy, artifact folders, validation gates). Load-bearing: yes. Compare target: `origin/main:AGENTS.md` resolves. Reuse rule: overlay wins on Forseti facts.
- Toolbox/playbook: `forseti/product/spines/capture/core/source_capture_toolbox/README.md`. Load-bearing: yes. Compare target: resolves on origin/main; at authoring it contains ZERO references to fragrantica/parfumo/basenotes or bronze/lake (quoted sweep evidence below). Last checked: 2026-07-05 @ 24c08287. Reuse rule: the access-authority surface being synced.
- source_families tree: `forseti/product/spines/capture/core/source_families/`. Load-bearing: yes. Compare target: `git ls-tree origin/main` shows retail_pdp + social_media only (no fragrance-DB family). Last checked: 2026-07-05. Reuse rule: the routing home.
- Lane-index pattern: `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md`. Load-bearing: yes. Compare target: resolves; its repo-map row reads "open first for any LinkedIn task". Reuse rule: copy the pattern, not the content.
- Unhomed fragrance-DB lane records: `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`, `docs/workflows/fragrantica_cleaning_audit_pack_handoff_v0.md`, `docs/workflows/parfumo_targeted_capture_contract_v0.md`. Load-bearing: yes (the confirmed instance). Compare target: all three resolve on origin/main. Reuse rule: link targets for the fragrance_db lane index; do not move.
- Harness surfaces: `orca-harness/source_capture/` (incl. `fragrantica_projection.py`, `fragrance_review_lake.py`), `orca-harness/runners/` (incl. `run_fragrantica_mgt_capture.py`, `run_fragrantica_projection.py`, `run_parfumo_mgt_capture.py`), `orca-harness/cleaning/` (incl. `parfumo.py`, `parfumo_lake.py`). Load-bearing: yes. Compare target: `git ls-files` the three dirs. Reuse rule: inventory input; enumerate fresh, the repo-map rows are illustrative-not-exhaustive by their own admission.
- Lake authority: `forseti/product/spines/data_lake/authority/` contracts. Load-bearing: yes. Compare target: folder resolves on origin/main. Reuse rule: pointed-to authority; NEVER restated into playbook or lane indexes.
- Evidence of the failure (measured): a commissioned sourcing agent on 2026-07-04, starting from the ToS doc + toolbox per doctrine, never reached the fragrantica lane; sweep on 2026-07-05 found zero capture-spine references (see Current Task State). Load-bearing: yes (motivates the unit). Compare target: re-run `rg -il "fragrantica|parfumo|basenotes" forseti/product/spines/capture` — expect empty until fixed.
- Source gaps: no inventory exists yet of WHICH families are unhomed beyond fragrance-DB (step 2 produces it).
- Strict-only blockers: owner ratification of the authority model (Open Decision); enforcement-hook build authorization (step 5).
- Not-proven boundaries: not validation or readiness; the packet asserts the disconnect for fragrance-DB only — other families' status is hypothesis until inventoried.

## Current Task State

- Completed (by the sender, as diagnosis): the measured discovery failure (Fragrantica commission missed the existing lane); the four-surface sweep at `24c08287` — capture spine: 0 hits; toolbox README: 0 hits; Data Capture submap: 0 hits; repo map: hits only inside two ~300-word `orca-harness/` rows; the fragrance-DB lane records located in docs/workflows; the authority-model proposal + sender refinement.
- Partially completed: nothing wired; no lane index authored; no inventory beyond fragrance-DB.
- Broken or uncertain: whether other families (fragrance purchase-review, Reddit, historical capture) share the disconnect — inventory decides.

## Workspace State

- Branch (sender): `claude/capture-lake-sync-handoff` @ `24c08287` (== origin/main at authoring).
- Dirty state before handoff: clean. After writing this file: this handoff file untracked until committed.
- Target files/artifacts (for the receiver): new `source_families/<family>/` lane indexes; edits to toolbox README, Data Capture submap, repo map (Quick Index + family rows); a dated authority-model record; optional hook.
- Related: PRs #695/#698/#701/#705/#707 (the Aphrodite sub-ontology lane whose sourcing run exposed this) — context only.

## Frozen Decisions

- Owner access posture (public-content capture OK; no credentials/bypass). Evidence: owner statement 2026-07-04 + ToS sanity check doc. Consequence: lane indexes record access routes under this posture.
- The sync itself is owner-directed, non-optional. Evidence: owner statement 2026-07-05 ("they are to make the captures / dump to data lake stuff seamless and synchronized"). Consequence: option 3 (status quo) is not an acceptable end state.

## Mutable Questions

- The authority model refinement (option 1) — proposed, owner-owned, ratify first.
- Whether the enforcement hook is worth building now or deferred — owner call after the inventory sizes the recurrence risk.
- Whether fragrance purchase-review shelters under retail_pdp or needs its own family — inventory decides.

## Superseded / Dangerous-To-Reuse Context

- The sender's earlier narrow fix proposal ("create fragrance_db lane index only") — superseded by this owner-widened unit covering ALL families. Do not fix only fragrance-DB and declare done.
- Any assumption that the repo map's two harness rows are a complete runner inventory — the rows say "illustrative, not exhaustive; enumerate with `git ls-files`".

## Commands And Verification Evidence

- Disconnect sweep (re-run target):
  ```bash
  rg -il "fragrantica|parfumo|basenotes" forseti/product/spines/capture forseti/product/spines/data_lake
  rg -in "fragrantica|parfumo|basenotes" docs/workflows/data_capture_spine_consolidation_map_v0.md
  ```
  Result 2026-07-05 @ 24c08287: capture spine 0 relevant hits (one unrelated IG recon file); submap 0 hits; data_lake spine 3 authority/workflow docs reference parfumo/fragrantica (lake side knows; capture side doesn't).
- Inventory seed: `git ls-files orca-harness/source_capture orca-harness/runners orca-harness/cleaning` — not run in full by the sender; receiver runs it.

## Blockers And Risks

- Owner ratification pending (Open Decision) — blocks pointer wiring.
- Repo-map contention: map edits are commit-once-whole with an immediate-commit hook; batch map rows into one edit per the hook's rhythm.
- Risk: lane indexes rot like the map rows did — that is exactly what the step-5 enforcement candidate addresses; do not skip evaluating it.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) toolbox README still lacks per-source lake routing; (2) source_families/ still lacks the fragrance-DB family; (3) the three fragrance-DB lane records resolve; (4) the LinkedIn lane index resolves as pattern; (5) main tip and this packet's pins.
- Load outcomes: `REUSE` after (1)-(5) verify; `STALE_REREAD_REQUIRED` if surfaces moved; `BLOCKED_DRIFT` if someone already started homing families (coordinate, don't duplicate); `BLOCKED_MISSING_PACKET`/`BLOCKED_UNVERIFIABLE` per contract.

## Do Not Forget

- Ratify the authority split BEFORE wiring pointers.
- Link, don't migrate: existing docs/workflows lane records stay put.
- The playbook points at lake doctrine; it never restates it.
- This packet authorizes documentation/index work only — no capture runs, no lake writes, no runner edits.

## Preflight / boundary receipt

```yaml
output_mode: file-write (this handoff packet only)
template_kind: handoff (workflow-handoff max packet; authored through the loaded prompt-orchestrator contract; no registry template bound for handoffs)
edit_permission: docs-write for this packet only, on branch claude/capture-lake-sync-handoff; the sync work itself is the receiver's, under its own authorization
reviews: none bound; findings-first applies to the receiver's inventory output; no runtime-model recommendation anywhere in this packet
doctrine_change: none by this packet (it PROPOSES the authority model; the ratification + recording step in the receiver lane carries the direction_change_propagation receipt, trigger workflow_authority)
destinations:
  input_prompt_artifact: docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md
  output_artifact_written: docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md
non_claims: [not capture or lake-write authorization, not validation, not readiness, not a ratified authority model]
```
