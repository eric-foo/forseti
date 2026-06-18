# Orca Second-Pass Consolidation Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration/consolidation plan record (controller worksheet)
scope: >
  Controller worksheet for the Orca "second pass": records the verified closure
  of the spine-first migration residual reconciliation (Phase 0) and carries the
  corrected two-track consolidation plan (enforcement restoration + residual-debt
  seed) plus the governance artifacts and locked decisions a Phase-1 foundation
  build and Phase-2 deletion pass consume. Plan + closure record only: not an
  execution runbook, not validation, readiness, or proof.
use_when:
  - Resuming or auditing the Orca second-pass consolidation as controller.
  - Checking whether the spine-first migration residuals are closed.
  - Looking up the Phase-1 foundation scope, governance specs, or locked decisions.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/decisions/orca_spine_first_blocker_authorization_v0.md
  - docs/migration/spine_first_target_move_table_v0.md
  - docs/decisions/orca_data_lake_spine_promotion_binding_v0.md
branch_or_commit: read against origin/main @ 6cf19a76 (#262)
supersedes: []
stale_if:
  - The Phase-1 foundation lands and the report-mode gate predicate is frozen (update the DAG status).
  - A later accepted consolidation decision changes a track, the deletion-adjudication model, or a locked decision.
  - The owner reopens a Phase-0 disposition recorded as closed below.
```

## Status

Controller worksheet, v0. Phase 0 (spine-first migration residual reconciliation)
is **verified closed** against primary source; Phases 1–4 are **planned, not
started**. This record persists per the second-pass controller handoff, which
gated persistence on Phase-0 resolution.

This is a **plan + closure record**, not an execution runbook. If a Phase later
needs step-level execution mechanics, split that into a narrower artifact rather
than growing this one.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (overlay S0 + source-loading + repo map + 4 spine-first companion docs + 3 checkers + data-lake binding)
  edit_permission: docs-write (controller worksheet); Phase-1 checker build is bounded implementation under the current-turn controller authorization
  target_scope: second-pass consolidation plan; doctrine dimension = validation_philosophy (gate-extension over orca/) — DCP receipt owed at the Phase-1 enforcement-landing closeout, not at this plan-persist
  dirty_state_checked: yes (worktree clean @ 6cf19a76; lane branch claude/sweet-noether-e4b49e)
  blocked_if_missing: none for this plan-persist
```

## Base & provenance

- Read against `origin/main @ 6cf19a76` (#262), worktree `sweet-noether-e4b49e`, clean.
- The spine-first companion docs (target binding, blocker authorization, move
  table, untagged inventory) were authored against `origin/main @ 8f19b460`
  (pre-migration). They are now **historical**: the migration executed in #255.
  Where this worksheet and those docs disagree on current state, this worksheet's
  primary-source reads govern; the companion docs remain the authority for the
  *target design* and *blocker settlements*.

## Phase 0 — CLOSED (verified against primary source)

### Migration is complete and clean

The spine-first migration **executed** in `1a9a29eb` (#255, "Complete spine-first
migration Wave D/E"); subsequent corrections landed in #256–#262. Verified:

- `docs/product/` = **0 files** on origin/main (fully dissolved).
- `orca/product/` = **230 files** across all 9 spines.
- Rename-aware diff `790fbdd3..origin/main` (pre-migration base = parent of #255):
  **216 of 218** `docs/product/` files moved into `orca/product/`, **0** to any
  unexpected destination. Per-spine landing tally: capture 105, judgment 25,
  case_families 24, foundation 20, product_lead 14, scanning 11, ecr 5,
  satellites 5, cleaning 3, shared 2, data_lake 1, commission_signal_board 1.
- The **2 non-renamed deletes** are intentional README retirements the untagged
  inventory anticipated, not losses: `docs/product/README.md` (lane-axis index,
  replaced by the spine-structure `orca/product/README.md` in #257) and
  `docs/product/search/README.md` (U-S1; retired at search dissolution per B2).
  Recovery trigger: if a lane needs the retired search README content, recover
  from git at `790fbdd3:docs/product/search/README.md`.
- Net-new delta (230 − 216 = 14) traces to post-migration PRs (#257 README,
  #258 data-lake converge, #261 CSB pilot spine, #262 ontology) — accounted for
  by the commit log, not stragglers.

### Structural blockers B1–B7 — as-built dispositions

| ID | Disposition (verified) |
| --- | --- |
| B1 `orca/` root | **CLOSED.** `repo-structure.yaml:30` declares `orca` in `known_top_level.dirs`; line 51 notes `docs/product/` "retired by Wave E." |
| B2 search dissolution | **CLOSED.** `docs/product/search/` gone; `scanning/` spine built; demand-read taxonomy at `foundation/demand_read_taxonomy/`. |
| B3 `docs/doctrine/` | **Unmaterialized — accepted.** Slot never created; nothing currently needs it (the doctrine index remains at `docs/decisions/orca_doctrine_index_v0.md`). Owner-confirmed default this turn: leave unmaterialized. Reopen by request only. |
| B4 ontology hook coupling | **CLOSED (#262).** `check_ontology_expansion.py:49` → `orca/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json`; the JSON's `cards_dir` = `orca/product/spines/foundation/ontology/ontology_cards`. |
| B5 CSB first home | **CLOSED.** `commission_signal_board/` spine built (#261); gate-run commission criteria landed at `commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md` (exact B5 settlement). |
| B6 Toolbox name + IG | **CLOSED.** `capture/source_capture_toolbox/`; IG docs at `capture/source_families/instagram/`. |
| B7 sibling inventories | **CLOSED (as-built consistent).** All ambiguous rows landed at blocker-auth-default-consistent homes (below). |

### Formerly `needs_main_ca_tag` rows — all landed at blocker-auth-default homes

The #255 executor applied the blocker-authorization tagging defaults faithfully;
each ambiguous row landed at a defensible home matching as-built:

- U-F1 proof-method trio (`proof_input_selection`, `proof_packet_preflight`,
  `method_validation_rubric`) → `foundation/product_contract/`.
- U-F2 ontology beauty instance cards → `foundation/ontology/ontology_cards/`.
- U-F3 `first_proof_run_charter` → `case_families/product_learning/other_verticals/`.
- U-CF2 `first_proof_run_jb_client0_slice` → `…/other_verticals/` (not `retail_pdp/`).
- U-CF3 `consumer_demand_candidate_pool_handoff` → `case_families/product_learning/fragrance/`.
- U-J2 `judgment_current_state_and_decomposition` → `judgment/` (root slot).
- U-J3 `reveal_calibration_owner_contract`, U-J4 addendum proposal → `judgment/conductor/` (co-located; no archive subfolder, per blocker-auth).
- U-PL1 `claim_defense_doctrine` → `product_lead/proof_charter/`.
- U-PL2/U-PL3 ratification/discovery/superseded docs → `product_lead/icp_wedge/` (catch-all; superseded co-located, no archive).
- Capture `operating_model/` superseded v0/v1 co-located with v2 (no archive subfolder).

Low-priority owner-revisitable note (not blocking): U-F1/U-F3 sit on the
method-vs-corpus axis; the executor placed the proof-method *definitions* in
`foundation/product_contract/` and the run *charter/slice* corpora in
`case_families/`. Defensible and consistent with the blocker-auth default; left
as-built unless the owner wants to revisit.

### Owner decisions recorded this turn (2026-06-18)

- **U-J1 — ratified as-built.** The fragrance product-learning reconciliation doc
  stays at `satellites/fragrance/judgment_level1/reconciliation/` (the slot is in
  the accepted target tree; blocker-auth default sends domain-subject Level-1
  artifacts to `satellites/<domain>/`). The move table (line 195) and untagged
  inventory (U-J1) still label it `needs_main_ca_tag`/open — those are stale and
  superseded by this ratification.
- **Phase-0 path — residual diff + persist worksheet**, then proceed to Phase-1
  foundation.

### Data Lake promotion — amends the move table

The move table's Section 10 routed `core_spine_v0_data_lake_mechanics_map_v0.md`
to `shared/data_lake_mechanics/`. That entry is **superseded** by
`docs/decisions/orca_data_lake_spine_promotion_binding_v0.md` (#256/#258): Data
Lake is now its own shared-foundation spine. Verified as-built: `shared/` holds
only `engagement_registry/` + `projection_doctrine/`; the mechanics map is at
`data_lake/workflows/`, lake contracts at `data_lake/authority/`.

### Open Phase-0-adjacent residuals carried into Phase 1 (not blockers)

1. **Stale `docs/product/` references in live surfaces.** ~3881 lines mention
   `docs/product/` repo-wide; most are legitimate historical citations
   (reference-model-B), but some sit in **live** overlay/checker surfaces
   (`.agents/workflow-overlay/{artifact-folders,artifact-roles,retrieval-metadata,skill-adoption}.md`,
   `check_map_links.py`, `check_placement.py`, `check_retrieval_header.py`).
   These need triage in the Phase-1 shared-surface reconcile (W4) — a *stale
   live-surface* reference is a drift defect; a *historical citation* is not.
   Tripwire: a stale `docs/product/...` reference surfacing as live routing in a
   Phase-2 lane stops that lane.
2. **B3 `docs/doctrine/`** left unmaterialized (above).

## The two tracks (corrected for as-built reality)

- **Track 1 — Enforcement Restored (structural; core, this pass).** The
  `orca/product/` corpus (230 files) is currently **ungoverned** by the
  doc-checkers: `check_map_links.py` C2/C3/C4 walk only `[docs/, .agents/]`
  (`check_map_links.py:422,471,513`) and its known-prefix set
  (`check_map_links.py:80`) is `docs/ .agents/ .github/ orca-harness/` — **no
  `orca/`**. Goal: extend header / link / folder-coverage / ontology-term
  enforcement over `orca/product/**`; rebuild the map from the tree and gate
  completeness; make the ontology a single source with an exact drift-check; cut
  bloat with deletion proof; land `--strict` green over `orca/` on a **frozen
  predicate**.
- **Track 2 — Semantic Consolidation (SEED ONLY this pass).** Stand up + seed a
  residual-debt inventory and run a *targeted* high-risk semantic pass (ontology
  terms, deletion candidates, moved/cross-linked docs, schema-facing concepts).
  **Do NOT claim semantic-clean completion** — full contradiction review is a
  follow-on pass.

## Phase DAG (status)

```
Phase 0  residual reconciliation + worksheet persist .............. DONE (this record)
   ▼
Phase 1  (parallel "thick neck" — nothing fans out until ALL done)
   W1a  report-mode gate-extension over orca/ (FROZEN predicate = strict-minus-exit-0); re-measure exact current debt
   W1c  cross-spine dependency graph
   W2   ontology SSOT (promote backbone + cards → ontology.yaml) + EXACT drift-check contract + doc-term/new-term lint
   W-map rebuild-from-tree + map↔tree completeness gate
   + governance specs: waiver registry · deletion-evidence register · lane-charter template
   ▼ [STOP — owner approval before any Phase-2 fan-out]
Phase 2  W3a propose (read-only, per spine, inbound-ref evidence) → CENTRAL delete adjudication → W3b execute (worktree-isolated, 1 PR/spine)
   ▼
Phase 3  W4 shared-surface reconcile (incl. stale docs/product live-surface triage) → W5 flip orca/ checks to --strict (frozen predicate) green
   ▼
Phase 4  W7 seed residual-debt inventory + targeted high-risk semantic pass (NO full review, NO semantic-clean claim)

W6  SCI-only reminder hook — independent, anytime.
```

W2's ontology work is SSOT + drift-check + lints **only**. The 4 demand-detection
cards (Observation/TrendVector/Call/Reading) are **deferred (#262)** — closed; do
not re-open.

## W1a report-mode build — status (in progress, uncommitted)

Pre-build gates cleared twice (`workflow-assumption-gate` → READY each time;
`micro-decision-locking` → locked). **W1a report unit COMPLETE.** Additive
`--report-orca` modes in `check_map_links.py` and `header_index.py`, plus a
scope-independent predicate helper (`header_problems_for_lines`) extracted in
`check_retrieval_header.py` and shared by the live gate and the report (one
definition → no report/strict drift). All report-only, exit 0. **Non-regression
proven** for every live gate (`check_map_links --strict`/`--selftest`,
`header_index --selftest`/`--health` 67/0 /`--strict`) — byte-identical to baseline.

W1a measured debt (actual, via the shared predicates):
- **Header presence:** 14 durable `.md` under `orca/product/spines/**` lack a valid
  header — 6 in `foundation/product_contract/` (product contract, IPF, proof
  protocol, etc. — canonical docs predating the header contract), 7 in
  `source_capture_toolbox/`, 1 capture pressure-test session. Mechanical backfill.
- **Links:** 0 broken `open_next` (after the F1 fix), 0 broken inline links, 3
  annotated-nonresolving (acknowledged debt).
- **Coverage:** UNMEASURED — coverage primitive is vacuous (F2); deferred to the
  W-map / coverage-gate piece. Not emitted as a misleading 0.

Two real defects surfaced on the report's first run (both feed later phases, neither
fixed in this increment per the locked scope boundary):

- **F1 — stale inbound `open_next` (actionable, known successor).**
  `orca/product/spines/capture/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md`
  points `open_next` at `orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md`,
  retired by the data-lake promotion (#258). Successor exists:
  `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`.
  **FIXED (this turn):** repointed the live `open_next`; `--report-orca` C2 now 0.
  The 3 body occurrences (an embedded preflight `target_scope` + a DCP receipt's
  `controlling_sources_updated`/`downstream_surfaces_checked`) are historical
  records that resolve via the moved-paths index (reference-model-B) and were
  intentionally left. A possible stale *live-surface* ref in
  `.agents/workflow-overlay/artifact-folders.md` is unverified — a W4 item.

- **F2 — the existing C3 folder-coverage gate is VACUOUS (latent substrate defect).**
  `check_map_links.dir_is_covered` returns `True` for *every* folder because its
  `if "not retrieval-indexed" in line.lower(): return True` clause is not tied to
  `rel_dir`, and the map carries one such line (repo map line ~365, describing
  `docs/hygiene/`). Empirically confirmed: a fabricated uncovered folder returns
  `True`; with that line removed it returns `False`. So C3 has enforced nothing
  since ~2026-06-13, and the new COV check inherits the same vacuity (COV reported
  0, which is meaningless, not real coverage). **The real coverage enforcement is
  the W-map / coverage-gate piece**, which must: (a) re-scope the
  `not retrieval-indexed` exemption to the specific annotated folder (or move it to
  `dir_is_exempt_coverage`); (b) rebuild the map with per-spine-folder entries so
  coverage is meaningful; (c) only then does C3/COV enforce. That fix changes the
  **live `--strict` behavior** (it would begin firing on the real docs/ coverage
  backlog), so it is its own staged unit — measure the docs/+orca/ coverage backlog
  in report mode first, then fix + clean + flip. NOT folded into this report increment.

Header-debt (W1a, actual — supersedes the earlier ~8–10 proxy): **14** durable
`.md` under `orca/product/spines/**` lack a valid header, measured by the precise
`header_problems_for_lines` predicate. The ~20 `case_families/.../other_verticals/`
corpus/replay instances are outside the locked W0 spines/** scope (and the
retrieval-metadata contract likely exempts corpus instances).

## Governance artifacts the controller owns (build in Phase 1, use in Phase 2)

1. **Waiver registry** — versioned (path / check / reason / owner / recheck-trigger); the only waiver mechanism.
2. **Cross-spine dependency graph** (W1c) — inbound-reference map for delete adjudication.
3. **Deletion-evidence register** — every approved delete needs an entry (reverse-reference evidence + successor path + semantic delta + rollback pointer).
4. **Lane-charter template** — bounds each Phase-2 execute lane.
5. **Drift-check contract** — exact conformity for ontology↔runtime: required/extra types, fields, relationships, deprecations, aliases, version-compat.

## Locked decisions — DO NOT relitigate

- **W0 per-check rule (adapt, don't apply blindly):** Header — scope to
  `orca/product/spines/**`, same retrieval-header shape. Folder-coverage —
  HARDER than current C3: every non-exempt durable product folder containing
  `.md` must be map-covered. open_next / inline-links — apply the invariant,
  adapt roots, keep explicit `nonresolving` waiver support. Term-lint — no naive
  prose grep; gate only SSOT-known terms / aliases / deprecated terms / explicit
  new-term candidates. Waivers — only via the versioned registry.
- **Deletion = central-adjudicated two-phase.** NO standing per-lane delete.
  Lanes propose; the controller approves only with reverse-reference evidence +
  successor path + semantic delta + rollback pointer (register entry).
- **Ontology demand-detection cards deferred (#262)** — closed; do not re-open.
- **Track 2 this pass = seed + targeted high-risk pass only.** Do NOT claim
  semantic-clean.
- **Report-mode predicate must equal the future strict predicate** (strict-minus-exit-0) so the eventual ratchet flips cleanly.

## Non-claims

- Phase-0 closure is an **observed state** (migration complete, blockers closed),
  not validation, readiness, or proof of the product corpus.
- This plan does not govern `orca/product/`; the corpus stays ungoverned until
  the Phase-1 gates land and Phase-3 flips `--strict` green.
- No file is moved, deleted, or created by this record beyond itself.
- Not a runtime, deployment, or `orca-harness/` change.
- The historical companion docs (target binding, move table, untagged inventory)
  are not re-ratified as current state; they are the target-design / blocker
  authority, superseded for *current placement* by the as-built tree + the
  data-lake promotion binding.
```
