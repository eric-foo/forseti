# Spine-First Migration — Execution Route v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration record (non-executing implementation route)
scope: >
  Read-only implementation-scoping route for executing the spine-first product
  migration (docs/product/ -> orca/product/) authorized by #254. Consumes the
  target-structure binding, the reconciled move table, the untagged inventory,
  the blocker authorization, and the workflow-assumption-gate readiness ledger.
  Ordered STEP-* route + wave/turn effort plan + validation matrix. NON-EXECUTING:
  no file moved, no orca/ tree created, no reference rewritten by this artifact.
use_when:
  - Executing the spine-first migration, wave by wave.
  - Sizing the migration effort (turns/waves) before authorizing execution.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/migration/spine_first_target_move_table_v0.md
  - docs/decisions/orca_spine_first_blocker_authorization_v0.md
stale_if:
  - The move table, target binding, or #254 authorization changes.
  - The reference sweep is re-run and the live/historical split materially shifts.
  - Execution completes (this becomes the historical route record).
```

## Plan intake & acceptance basis

- **Plan source:** `docs/migration/spine_first_target_move_table_v0.md` + `docs/decisions/orca_spine_first_target_structure_binding_v0.md`, with blockers settled by `docs/decisions/orca_spine_first_blocker_authorization_v0.md` (#254, merged `790fbdd3`).
- **acceptance_basis:** `accepted_explicit` — owner merged #253 + #254 and authorized execution ("authorize of course for any needed").
- **Pre-build gate:** `workflow-assumption-gate` returned `READY_WITH_VERIFIED_LEDGER`; its load-bearing finding (LA1 — rewrite surface undercounted) is incorporated below as the live rewrite set.
- **Base:** worktree `orca-spine-first-execution` @ `790fbdd3` (post-#254 main), clean.

## Frozen decisions (do not reopen)

- The accepted target tree, the 5 conventions, and the foregone-limitations ledger (target binding).
- B1–B7 settlements + per-file tagging defaults (#254). U-tags resolve via those defaults, not re-adjudication.
- `orca-harness/` runtime stays in place (`runtime_defer`); no code migration this tranche.
- Search lane dissolves by spine function; demand-signal method authority preserved (#254 B2).
- `source_capture_toolbox` is the folder name; IG/YT/TT are source families (#254 B6).

## Source map — reference blast radius (gating-read result)

`git grep "docs/product/"` over tracked files @ `790fbdd3` → **5,393 refs / 626 files**:

| Surface | Refs / files | Treatment |
| --- | --- | --- |
| A. `docs/product/` (the moved set's internal refs) | 1945 / 208 | **rewrite** during `git mv` (intra-set) |
| B. `docs/` other (decisions/workflows/prompts/reviews/research/migration) | 3289 / 378 | **mostly historical-keep** (old path + moved-paths index); only **live nav** rewrites (repo map + 3 submaps + doctrine index) |
| C. `.agents/workflow-overlay/` (AUTHORITY) | 58 / 10 | **rewrite** (live): safety-rules 10, source-loading 23, artifact-folders 12, product-proof 4, source-of-truth 3, validation-gates 2, artifact-roles 1, retrieval-metadata 1, skill-adoption 1, delegated-review-patch 1 |
| D. `.agents/skills/orca-product-lead/SKILL.md` (canonical) | 6 / 1 | **rewrite** (agent-editable canonical) |
| E. `.agents/hooks/` (runtime) | 20 / 4 | **classify then rewrite real couplings**: check_ontology_expansion 2 (B4, real), check_placement 11 + check_map_links 5 + check_retrieval_header 2 (inspect — likely test-fixture/example strings) |
| F. `.claude/skills/orca-product-lead/SKILL.md` (installed copy) | 6 / 1 | **PROTECTED — resync via tooling, NOT hand-edit** |
| G. `.github/workflows/pr-risk-router.yml` (CI) | 1 / 1 | inspect; rewrite if a live path |
| H. `orca-harness/` (runtime) | 65 / 22 | live operator docs rewrite (`source_capture_agent_runbook.md` 35); case `source_provenance_notes` + code docstrings = tolerated residual (foregone-limitation) |
| I. `repo-structure.yaml` (root) | 3 / 1 | **rewrite** in the structural-amendment tranche |

**Net live rewrite set ≈ 2,050 refs / ~230 files** (A + C + D + real E + live nav + runbook + repo-structure.yaml). **Historical-keep ≈ 3,340 refs** handled by **one moved-paths index**, not per-file edits. `AGENTS.md`/`CLAUDE.md` carry **zero** product refs (they defer to the overlay).

Reusable engine precedent: `docs/migration/repo_structure_search_lane_v0/apply_moves.py` and `…repo_structure_phase2_consolidation_v0/apply_moves.py` (manifest-driven `git mv` + live-ref rewrite + moved-paths index + idempotent/reverse).

## Live-vs-historical rewrite policy (the central rule)

Per the search-lane precedent (reference-model-B): **LIVE** surfaces rewrite to `orca/product/...`; **HISTORICAL** point-in-time records keep their old path and resolve via a single moved-paths index.

- LIVE = the moved set's internal refs; overlay authority (C); canonical skill (D); real hook couplings (E); live nav (repo map + data_capture/ecr/judgment submaps + doctrine index); live harness operator docs (runbook); `repo-structure.yaml`.
- HISTORICAL = decisions, reviews, prompts, research, prior migration records, case `source_provenance_notes`, harness code docstrings (tolerated residual).

## Implementation Route (ordered)

**STEP-01 — Freeze the manifest + live/historical classification (gating read).** Inspect: move table, untagged inventory, #254 tagging defaults. Produce a moves manifest mapping each of the ~218 `docs/product/` files → its `orca/product/...` target (U-tags resolved by #254 defaults); classify all 626 referencing files LIVE/HISTORICAL/RESIDUAL. *Verify:* every product file has exactly one target; every `needs_main_ca_tag` row resolved by a #254 default. *Stop:* any file maps to no target / no default applies.

**STEP-02 — Author the apply engine + dry-run (no tree change).** Inspect: the two precedent `apply_moves.py`. Author a spine-first manifest + apply/reverse script under `docs/migration/repo_structure_spine_first_v0/` (idempotent; `git mv`; rewrites only LIVE refs; emits moved-paths index). *Verify:* `--check` dry-run lists planned moves + live rewrites, changes nothing. *Stop:* dry-run would rewrite a HISTORICAL record, or move a file outside the manifest.

**STEP-03 — Scaffold + authority amendment (ONE tranche; high lock-in).** Create `orca/` + `orca/product/` tree; amend `repo-structure.yaml` (add `orca` to `known_top_level.dirs`, add the `orca/product/` axis, add `docs/doctrine/` role, drop `docs/product/`); amend `artifact-folders.md` (replace the `docs/product` lane axis with the `orca/product` spine axis); flip the repo-structure binding + search binding from "authorized, not executed" to executed/superseded. **Must be one commit** (B1: never declare `orca/` in the map without the tree existing). *Verify:* `check_placement.py --strict` passes (`orca/` declared AND present); freshness clean. *Stop:* placement flags `orca/` stale → ordering violation, roll back.

**STEP-04 — Execute the bulk move + live-ref rewrite.** Run the apply engine: `git mv` ~218 files into `orca/product/`; rewrite the ~2,050 live refs; generate the moved-paths index. *Verify:* `git status` shows renames (`R`) not delete+add (history preserved); `git grep "docs/product/"` in LIVE docs → **zero**; moved-paths index covers the historical bulk. *Stop:* any LIVE doc retains an old path; any unplanned move.

**STEP-05 — Paired runtime coupling (B4 + hooks + harness docs).** Update `check_ontology_expansion.py` backlog-JSON path (or old/new bridge) in the same tranche the JSON moved; classify + fix only the **real** `.agents/hooks/` couplings (leave test-fixture strings); rewrite live harness operator docs (`source_capture_agent_runbook.md`); flag the `.claude/` installed skill copy for **tooling resync** (do not hand-edit). *Verify:* `check_ontology_expansion.py` + hook `--selftest`s pass against new paths. *Stop:* a hook hard-fails on the new path.

**STEP-06 — Validation, moved-paths index, closeout.** Run `check_placement.py --strict`, `check_map_links.py`, `check_retrieval_header.py --changed`, `check_repo_map_freshness.py`, CI link check; confirm zero dangling LIVE refs + moved-paths index resolves historical refs; update repo-map Workstream Status Pointers → executed; confirm `orca-harness/` unchanged beyond tolerated doc/comment residual. *Verify:* all checks green; `git diff --check` clean. *Stop:* any check red, or `orca-harness/` runtime modified (runtime_defer breach).

## Wave / turn effort plan ("how many turns")

Sized for context safety — the bulk move (STEP-04) alone touches ~230 files and must not share a turn with judgment-heavy work.

| Wave | Turn(s) | STEPs | Lane | Why isolated |
| --- | --- | --- | --- | --- |
| A — manifest + engine | 1 | 01, 02 | judgment | live/historical classification is the judgment crux; ends at a reviewable dry-run, zero tree change |
| B — structural commit | 1 | 03 | judgment | high-lock-in, near-irreversible map/binding amendment; **owner-confirm before this wave** |
| C — bulk move | 1–2 | 04 | mechanical | scripted but VERY_HIGH context (230 files + rewrite); verification may need a 2nd turn |
| D — runtime coupling | 1 | 05 | judgment | protected-copy + hook-fixture-vs-real judgment |
| E — validation + closeout + PR | 1 | 06 | judgment | full gate suite + moved-paths index + PR |

**Estimate: 5 turns (6–7 if Wave C verification or a failed gate forces a second pass).** One execution PR off `spine-first-migration-execution`, waves as commits within it (mirrors the search-lane single-PR pattern); landing to `main` stays owner-gated.

## Validation matrix

| Type | STEP | Risk covered | Evidence | Failure means |
| --- | --- | --- | --- | --- |
| scoping | 01 | incomplete manifest | every product file → one target | a file would be orphaned by the move |
| implementation | 02 | unplanned/historical rewrite | dry-run `--check` diff | engine would corrupt a historical record |
| implementation | 03 | ordering / unplaced root | `check_placement --strict` green | `orca/` declared-but-absent (stale map) |
| implementation | 04 | history loss / dangling refs | `git status` renames; zero live old-path refs | move broke history or left dangling links |
| implementation | 05 | broken runtime coupling | hook selftests + ontology check green | a hook reads a dead path |
| implementation | 06 | repo-wide integrity | full gate suite + link check green | migration left the repo inconsistent |
| not-run (intentional) | — | harness code-comment / case-provenance residual | n/a | tolerated per foregone-limitation; not rewritten this tranche |

## Stop conditions & containment

- Each wave = one commit; the apply engine is idempotent + `--reverse`.
- STEP-03 is the hardest rollback (tree + map + bindings) → owner-confirm gate before it; if `check_placement` flags `orca/` stale, revert the single structural commit.
- Any `orca-harness/` runtime change beyond the tolerated doc/comment residual = immediate stop (runtime_defer breach).
- The `.claude/` installed skill copy must never be hand-edited (protected path).

## Route status & authorization

- **route_status:** `ROUTE_COMPLETE`
- **implementation_start_readiness:** `READY_WITH_WARNINGS` — bindings present (acceptance #254, target homes, validation gates, write boundary `orca/` authorized + `orca-harness/` off-limits, clean worktree). Warnings: (1) **VERY_HIGH context risk** → execute wave-by-wave, never one-shot; (2) STEP-03 high-lock-in → owner-confirm before it; (3) `.claude/` installed copy is protected → tooling resync only; (4) STEP-01 live/historical classification gates everything.
- **current_turn_authorization:** `read_only_scoping_only` (this turn produced the route + this artifact only; no migration execution).
- **implementation_context_risk:** `VERY_HIGH`.

## Next authorized step

Owner confirms the wave plan, then authorize a separate implementation turn for **Wave A (STEP-01 + STEP-02)** — manifest + dry-run-validated apply engine, zero tree change — for review before the Wave B structural commit.

Recommended Implementation Model: judgment_lane — contract-bearing bindings, compounding multi-wave risk.
