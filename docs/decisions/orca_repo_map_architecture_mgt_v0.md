# Forseti Repo-Map Architecture (Mini God Tier) v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record (owner-invoked mini-god-tier architecture)
scope: >
  The locked Forseti repo-map retrieval architecture: curated map, dense-area
  submaps, retrieval headers, generated on-demand inventory/health, session
  health capsule, recent-change satellite, promotion-on-touch, and the
  reachability-coverage invariant. Binds what the central map owns vs what
  generated and satellite surfaces own.
use_when:
  - Building, rebuilding, or gating the repo map / submaps.
  - Defining or changing what folder "coverage" means in check_map_links.
  - Deciding whether a folder needs its own map row (it usually does not).
  - Deciding whether a recent-change note should be promoted into map/submap/header routing.
  - Checking whether a standing gardener or committed generated inventory is justified.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/orca_repo_map_v0.md
  - .agents/hooks/check_map_links.py
  - .agents/hooks/header_index.py
  - .agents/hooks/session_context_capsule.py
  - docs/workflows/repo_map_recent_changes/README.md
  - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - A later owner decision amends the tiers, coverage invariant, generated inventory role, health-surface role, or promotion-on-touch boundary.
  - The owner elects the maximal (god-tier) row-per-doc central manifest instead.
  - Evidence from retrieval probes proves a standing gardener is necessary.
```

## Status

Owner-invoked mini-god-tier (MGT) design, 2026-06-19 (this thread; owner said
"make it the MGT" for the repo-map structure). Per
`docs/decisions/forseti_mini_god_tier_doctrine_v0.md` this is a **design lens, not a
claim tier** — it asserts no validation or readiness, and its mandatory
named-limitations list is below.

## Decision

The repo map is **high-level authority + a router, not a per-doc index.** Per-doc
indexing is already solved, decentrally, by retrieval headers (they travel with
the doc, die with the doc, and `header_index --index` regenerates the full
per-doc view on demand). A central per-doc enumeration would duplicate that and
churn on every edit — the standing-infrastructure shape MGT rejects.

**God-tier vs MGT (owner-asked 2026-06-19) — split by layer.** The *artifact* is
MGT: decentralized (high-level map + submaps + headers), with the full per-doc
list regenerated on demand by `header_index --index`. The *guarantee* is
god-tier-rigorous: the completeness invariant is **gated** (every durable doc
headered + every folder reachable + zero orphan). A persisted, always-in-sync
complete central index (the god-tier *artifact*) is rejected — in Forseti's
multi-lane, about-to-bloat-cut repo it is a merge-conflict magnet and duplicates
the headers, adding nothing over (headers + `--index` + the git PR diff). Rigor
lives in the gate, not the file.

### 2026-07-02 lock amendment: full retrieval stack

The selected target architecture is now locked as a stack, not just the original
three-tier map/submap/header shape:

1. **Curated main map**: stable routing, major areas, source-pack orientation,
   active-hook discoverability, and submap registry; not a full inventory.
2. **Dense-area submaps**: localized human navigation for areas too dense for
   the main map.
3. **Retrieval headers**: durable-doc labels that travel with each artifact and
   provide role, scope, use_when, stale_if, and open_next hints.
4. **Generated on-demand inventory and health**: `header_index.py --index` is
   the complete file-level catalog when needed; `--health --oneline` is the
   advisory backlog surface.
5. **Session capsule health line**: `session_context_capsule.py` exposes the
   retrieval-health count at lane start so cold lanes see backlog without walking
   the tree.
6. **Recent-change satellite**: `docs/workflows/repo_map_recent_changes/` is
   low-conflict context for map-affecting changes, not route truth and not a
   replacement for map/submap/header updates.
7. **Promotion-on-touch**: promote a recent-change note only when it prevents a
   recurring broad read, stabilizes a route, or changes durable navigation.

Rejected shapes remain rejected unless a later probe proves a gap: manual full
main-map inventory, committed generated inventory artifacts, and a standing
periodic gardener loop. A gardener may become justified only after measured
retrieval failures or backlog behavior show that promotion-on-touch is not enough.

### The three tiers

| Tier | Owns | Churn |
| --- | --- | --- |
| **T1 — the map** (`docs/workflows/orca_repo_map_v0.md`) | top-level dirs; the spine axis + **major areas** (one or two levels deep); fast-route Q&A; governance/active-hooks notes; the **submap registry** | only on *structural* change (new spine/area) — stable across the bloat cut |
| **T2 — per-spine submaps** (`docs/workflows/*submap*.md`) | internal routing for **dense** spines only (ECR exists; capture + judgment are the next candidates) | localized to one area |
| **T3 — retrieval headers** (per durable doc) | the per-doc index: role / scope / use_when / open_next | travels with the doc; **zero map churn on delete** |

### Coverage invariant (gateable)

A folder containing durable docs is **covered** iff **it, or an ancestor *area*,
is a canonical map/submap path entry**, enforced down to a **minimum declared
depth** (the spine-area level). A spine-area entry covers its sub-folders;
declaring only a high root (e.g. `orca/product/`) does **not** cover leaves
(that would re-introduce vacuity). Leaf discovery within a covered area is via
the submap (if dense) + retrieval headers.

"Canonical path entry" = a backticked path token in the **first cell** of a map
table row (folder rows and file rows both confer coverage on their containing
area). Prose mentions, answer-cell paths in Q&A tables, and "add X later" debt
notes do **not** confer coverage.

### Named foregone limitations (mandatory — MGT)

1. **No hand-maintained central list of every doc.** Navigation is map → submap
   → header. *Kept value:* `header_index --index` regenerates the full per-doc
   list on demand, so the standing infrastructure is dropped, not the capability.
2. **Coverage guarantees reachability, not explicit per-folder naming.** A folder
   is reached via its area, not a dedicated row.
3. **Submaps add one indirection hop and need their own freshness discipline** (a
   submap registry in T1 + a "registered submaps exist/fresh" check).
4. **The coverage predicate is ancestor-path matching** (segment-aware), slightly
   more code than a substring "is it named" test — but it is the correct predicate.
5. **Index quality depends on header discipline** — already separately gated by
   `header_index`, so not a new risk.
6. **Promotion-on-touch is judgment-based.** It intentionally does not promise
   that every recent-change note is promoted on a schedule; Batch 2 retrieval
   probes must prove a real repeated failure before a standing gardener is built.

The Pareto bet: accept (1)+(2) as the price; win low-churn + stable-across-bloat
+ zero duplication as the prize.

## Consequences

- **Coverage semantics:** `check_map_links.dir_is_covered` becomes
  **ancestor-area** reachability against canonical first-cell path tokens — NOT
  the raw-substring or descendant-prefix forms. This kills the false-cover cases
  (sibling `foobar`, prose mention, answer-cell path, child-covers-parent).
- **Map-rebuild (W-map) scope shrinks:** from "add a row per uncovered leaf
  folder" to "declare the **area hierarchy** to area-depth + add the capture and
  judgment submaps." The ~34 orca/ "uncovered" leaf folders measured under loose
  matching largely collapse into a bounded set of area entries.
- **C3 folder-coverage and the `header_index` orphan check are complementary,**
  not redundant: the orphan check only fires on header-bearing docs, so C3 still
  catches a folder whose docs lack headers. Both share the one fixed
  `dir_is_covered`.
- **Exemptions** (operational corpus/fixture/source folders that should not be
  governed) route through the versioned waiver registry, exact-path, not pattern
  matching.

## Non-claims

- Design lens only (MGT): not validation, readiness, or proof; no artifact
  currently carries a readiness claim from this record.
- Not the implementation: this binds the target; the coverage-checker rewrite,
  the map rebuild, and the submaps are separate authorized builds.
- Not a claim that the map is currently complete under this invariant — it is the
  target the rebuild converges to.
- Not a claim that retrieval health is clean; the current advisory health count
  remains probe evidence, not readiness.
- Not authorization for a standing gardener, committed generated inventory, or
  broad header backfill.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Repo-map MGT architecture is locked as a full retrieval stack: curated main
    map, dense-area submaps, retrieval headers, generated on-demand
    inventory/health, session-capsule health line, recent-change satellite, and
    promotion-on-touch. Manual full inventory, committed generated inventory,
    and standing gardener loops remain rejected unless retrieval probes prove a
    repeated failure.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/orca_repo_map_architecture_mgt_v0.md
    - docs/decisions/orca_doctrine_index_v0.md
    - docs/workflows/repo_map_retrieval_probe_batch_2_v0.md
    - .agents/hooks/header_index.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/repo_map_recent_changes/README.md
    - .agents/hooks/check_map_links.py
    - .agents/hooks/session_context_capsule.py
    - docs/prompts/deep-thinking/repo_map_god_tier_architecture_3subagent_prompt_v1.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The current map already exposes the recent-change satellite and active
        hook surfaces; this lock amends the decision record rather than adding a
        high-conflict top-map chronology or full inventory.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Enforcement placement and the retrieval-header index gate already name
        `header_index.py --index`, `--health`, `--health --oneline`, and
        `--strict`; the Batch 2 hook fix changes Windows output robustness, not
        the gate contract.
    - path: .agents/hooks/check_map_links.py
      reason: >
        C3 reachability semantics already point to this decision record; the
        lock amendment does not change the predicate.
  stale_language_search: >
    rg -n "Repo-Map Architecture|promotion-on-touch|gardener|committed generated inventory|header_index --index|repo_map_recent_changes" docs/decisions docs/workflows .agents/workflow-overlay .agents/hooks docs/prompts/deep-thinking/repo_map_god_tier_architecture_3subagent_prompt_v1.md
  stale_language_search_result: >
    Executed 2026-07-02 during the lock/probe patch. Live hits are this amended
    decision, the patched 3-subagent prompt, the recent-change README/map route,
    validation-gates/header_index hook documentation, and historical or adjacent
    uses of repo-map/gardener language. No checked live surface still selects a
    manual full inventory, committed generated inventory, or standing gardener as
    the default architecture.
  non_claims:
    - not validation
    - not readiness
    - not proof that retrieval health is clean
    - not source-of-truth promotion beyond this decision record
    - not implementation authorization beyond the bounded header_index Windows-output fix
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca adopts a mini-god-tier tiered repo-map architecture: the central map is
    high-level authority + router (top-level dirs, spine axis + major areas,
    fast-route, governance, submap registry); dense spines get submaps; retrieval
    headers remain the decentralized per-doc index. "Coverage" is redefined as a
    reachability invariant — a folder is covered iff it or an ancestor area is a
    canonical first-cell map/submap path entry (depth-bounded), NOT row-per-folder.
    This supersedes the implicit row/substring coverage model and rescopes the
    coverage checker and the map rebuild.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/decisions/orca_repo_map_architecture_mgt_v0.md
  downstream_surfaces_checked:
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/check_map_links.py
    - .agents/hooks/header_index.py
    - .agents/workflow-overlay/validation-gates.md
    - docs/migration/orca_second_pass_consolidation_plan_v0.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The map rebuild to the tiered/area-declared form is a separate authorized
        build (W-map); this record binds the target, it does not rebuild the map.
    - path: .agents/hooks/check_map_links.py
      reason: >
        The dir_is_covered ancestor-area rewrite is the next authorized build
        under this binding; this record defines the invariant, it does not edit
        the checker.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The coverage gate's enforcement-placement note updates when the checker
        rewrite lands, not at design-binding time.
  stale_language_search: >
    rg -i "every .*folder.*map|row per (folder|doc)|map-covered" .agents docs
    (deferred to the checker-rewrite build, which is where stale coverage language
    in checker docstrings/comments will be reconciled)
  non_claims:
    - not validation
    - not readiness
    - not implementation of the checker or map rebuild
    - MGT is a design lens, not a claim tier
```

Older receipts, when cycled out, are archived verbatim in docs/decisions/dcp_receipts_archive_v0.md.
