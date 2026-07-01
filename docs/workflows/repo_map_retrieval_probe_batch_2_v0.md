# Repo Map Retrieval Probe Batch 2 v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow retrieval probe record
scope: Batch 2 probe for the repo-map MGT retrieval stack: cold-lane orientation, generated index behavior, health visibility, recent-change routing, and map-link coverage evidence.
use_when:
  - Checking what Batch 2 proved or did not prove before header-backlog or gardener work.
  - Planning repo-map retrieval improvements after the 2026-07-02 lock amendment.
  - Reviewing why `header_index.py` gained Windows-safe stdout/stderr configuration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_repo_map_architecture_mgt_v0.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/workflows/repo_map_recent_changes/README.md
  - .agents/hooks/header_index.py
  - .agents/hooks/session_context_capsule.py
  - .agents/hooks/check_map_links.py
stale_if:
  - `.agents/hooks/header_index.py` changes index, health, strict, or output behavior.
  - `.agents/hooks/session_context_capsule.py` changes retrieval-health capsule behavior.
  - `.agents/hooks/check_map_links.py` changes map/submap coverage semantics.
  - A later retrieval probe supersedes these observations.
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 + repo-map retrieval hooks
  edit_permission: implementation-authorized
  target_scope: Batch 1 architecture lock plus Batch 2 retrieval probe and bounded generated-index hook fix
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-of-truth doctrine-change contract, source-loading budget, repo map, architecture decision, header_index, session capsule, check_map_links, recent-change README
```

## Probe Goal

Measure whether the locked repo-map retrieval stack can get a cold lane to the
right sources without a full manual inventory or standing gardener. The success
bar is the source-loading budget: no more than four full-file reads, eight
targeted reads, and ten decisive excerpts for routine source discovery.

## Observed Probe Runs

| Probe | Question | Entry / command | Observed result | Assessment |
| --- | --- | --- | --- | --- |
| P1 | What state does a cold lane see immediately? | `python -B .agents/hooks/session_context_capsule.py --check` | Capsule reported branch `codex/repo-map-god-tier-architecture-prompt`, clean tree, source-loading entry points, and `retrieval health: 66 missing headers, 0 orphans`. | Pass for visibility; not readiness because backlog remains. |
| P2 | Can the health layer be queried directly? | `python -B .agents/hooks/header_index.py --health --oneline` | `retrieval health: 66 missing headers, 0 orphans`. | Pass for direct health; backlog becomes Batch 3 input. |
| P3 | Can generated inventory find the repo-map architecture decision? | `python -B .agents/hooks/header_index.py --index | Select-String ...` | Initially failed open on Windows console encoding (`'charmap' codec can't encode character '\u2192'`). After the bounded hook fix, the query returned the architecture decision and adjacent prompt hits. | Probe found and fixed a core generated-index defect. |
| P4 | Is the recent-change satellite discoverable and correctly bounded? | `rg -n "recent-change|repo_map_recent_changes|not substitute" docs/workflows/orca_repo_map_v0.md docs/workflows/repo_map_recent_changes/README.md` | Repo map points to `docs/workflows/repo_map_recent_changes/`; README says it is low-conflict context and not a substitute for real route updates. | Pass. |
| P5 | Is coverage check ownership discoverable? | `rg -n "C1|C2|C3|C4|dir_is_covered|Reachability semantics" .agents/hooks/check_map_links.py` | `check_map_links.py` exposes C1-C4, C3 folder coverage, strict mode, and `dir_is_covered` pointing to the MGT decision. | Pass. |
| P6 | Is the cold-lane budget itself visible? | `rg -n "four full-file reads|eight targeted|ten decisive|cold-lane retrievability bar" .agents/workflow-overlay/source-loading.md` | Source-loading lines 245-257 bind the 4/8/10 budget and call budget excess a retrievability defect signal. | Pass. |

## Batch 2 Adversarial Review

Advisory review only; not a formal verdict, validation, readiness, or mandatory
patch queue. The review attacked whether Batch 2 could create fake confidence by
proving only easy paths.

| Finding | Attack | Adjudication | Closure |
| --- | --- | --- | --- |
| AR-B2-01 | Generated inventory is not god-tier if `header_index.py --index` fails on ordinary repo text. | Accepted. The Windows `charmap` failure made the generated catalog unreliable in this probe. | Closed in this batch by configuring `header_index.py` stdout/stderr as UTF-8 with replacement fallback; selftest and filtered `--index` probe passed after patch. |
| AR-B2-02 | Health visibility can create false confidence if the backlog is visible but ignored. | Accepted. `66 missing headers, 0 orphans` is a visible backlog, not readiness. | Carried to Batch 3 as header-value triage; no broad backfill authorized. |
| AR-B2-03 | A small probe cannot prove a standing gardener will never be needed. | Accepted residual. This batch can reject gardener-by-default, not gardener-forever. | Keep promotion-on-touch as default; require repeated measured retrieval failure before a standing gardener is reconsidered. |
| AR-B2-04 | The new workflow probe record might itself be a repo-map event. | Downgraded. It lives under already mapped `docs/workflows/` and does not create a new route family. | `check_repo_map_freshness.py --changed --strict` was run with an explicit repo-map ack. |

## Batch 2 Patch Result

The probe found one implementation defect in the generated inventory layer:
`header_index.py --index` could fail open on Windows when indexed text contained
non-ASCII characters such as `→`. The hook now configures stdout/stderr as UTF-8
with replacement fallback before printing report-mode output. This preserves the
read-only/fail-open boundary while making the human catalog printable on Windows.

## Findings

- The locked architecture is viable as a layered retrieval stack: capsule health,
  repo map, recent-change satellite, generated index, and coverage checker are
  all discoverable from current sources.
- Current retrieval health is not clean: `66 missing headers, 0 orphans`.
- The generated index is now usable in the observed Windows probe after the
  stdout/stderr fix.
- No evidence from this probe justifies a standing gardener or committed
  generated inventory.

## Next Batch Input

Batch 3 should triage the 66 missing headers by retrieval value. Do not bulk
backfill every missing header. Start with durable authority, workflow, decision,
prompt, and review artifacts that affect future routing; leave scratch or
historical material alone unless it demonstrably prevents retrieval.

## Non-Claims

- Not validation.
- Not readiness.
- Not proof that the whole repo is retrievable.
- Not a claim that the 66 missing headers are all worth fixing.
- Not authorization for a standing gardener, committed generated inventory, or broad backfill.