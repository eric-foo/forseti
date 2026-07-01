# Repo Map God-Tier Architecture 3-Subagent Prompt v1

```yaml
retrieval_header_version: 1
artifact_role: Architecture planning courier prompt
scope: Paste-ready prompt for collecting three independent advisory architecture perspectives on a god-tier Orca repo-map/retrieval architecture before owner-thread adjudication.
use_when:
  - Couriering a read-only architecture evidence pack to another capable repo-aware thread.
  - Comparing repo-map, generated inventory, submap, recent-change, and promotion-on-touch architecture options.
  - Preparing inputs for owner-thread adjudication before any implementation or durable doctrine change.
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/workflows/repo_map_recent_changes/README.md
  - .agents/hooks/check_repo_map_freshness.py
  - .agents/hooks/header_index.py
  - .agents/hooks/check_map_links.py
  - .agents/hooks/session_context_capsule.py
stale_if:
  - docs/workflows/orca_repo_map_v0.md changes repo-map freshness policy.
  - docs/workflows/repo_map_recent_changes/README.md changes recent-change note policy.
  - .agents/hooks/check_repo_map_freshness.py changes structural trigger behavior.
  - .agents/hooks/header_index.py changes generated index or health behavior.
  - .agents/hooks/check_map_links.py changes map/submap coverage behavior.
  - .agents/hooks/session_context_capsule.py changes session-start retrieval-health behavior.
  - .agents/workflow-overlay/prompt-orchestration.md changes cross-recipient prompt or subagent return-shape rules.
authority_boundary: retrieval_only
```

This prompt is a courier artifact. It collects advisory evidence only; it is not
implementation authorization, validation, approval, readiness, or a final
architecture decision.

````markdown
# Repo Map God-Tier Retrieval Architecture: 3-Subagent Evidence Pack

You are operating in the Orca repository. Produce a read-only architecture
evidence pack for the owner thread to adjudicate later. Do not implement, edit
files, stage, commit, push, open PRs, or claim readiness.

## Orca Prompt Preflight

```yaml
output_mode: paste-ready-chat
template_kind: deep-thinking / architecture-planning evidence pack
edit_permission: read-only
targets:
  - repo-map and retrieval architecture
  - generated inventory architecture
  - area submap architecture
  - repo-map recent-change inbox and promotion-on-touch routing
workspace: C:\Users\vmon7\Desktop\projects\orca
branch: current checked-out branch; verify and report
dirty_state_allowance: read-only inspection only; report dirty state, do not modify it
reviews: none; advisory architecture evidence only
doctrine_change: candidate architecture/workflow-authority implications only; do not write a direction_change_propagation receipt
destination: return one chat evidence pack to the couriering user/thread
```

## Required Method And Source Sequence

REFERENCE-LOAD these method/authority sources first. Do not APPLY architecture
planning until after SOURCE_CONTEXT_READY is declared.

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `workflow-architecture-planning` skill instructions if available in your runtime

Then SOURCE-LOAD the smallest complete task source pack:

- `docs/workflows/orca_repo_map_v0.md`
- `docs/workflows/repo_map_recent_changes/README.md`
- `.agents/hooks/check_repo_map_freshness.py`
- `.agents/hooks/header_index.py`
- `.agents/hooks/check_map_links.py`
- `.agents/hooks/session_context_capsule.py`
- `docs/workflows/artifact_retrievability_guide.md`
- `docs/decisions/orca_repo_map_architecture_mgt_v0.md` if present in the checkout
- Any repo-structure or map-link/checker source you can identify as directly decision-bearing; otherwise list it under `sources_available_not_read`.

Declare:

```text
SOURCE_CONTEXT_READY
```

or:

```text
SOURCE_CONTEXT_INCOMPLETE:
- missing source:
- why it matters:
- what claims are not proven:
```

Only after source readiness, APPLY standard architecture planning.

## Task

We are considering a god-tier repo-map/retrieval architecture for Orca.

Current candidate architecture to test, not assume:

- Keep the main repo map as a stable curated router, not a full manual inventory.
- Keep recent-change notes low-conflict under `docs/workflows/repo_map_recent_changes/`.
- Use generated on-demand inventory for complete file-level retrievability.
- Use area submaps for meaningful human navigation detail.
- Treat retrieval-health capsule wiring as already expected if `session_context_capsule.py`
  calls `header_index.py --health --oneline`; if this is not true in the checkout,
  report that as a source-backed gap.
- Prefer triggered promotion-on-touch over a periodic gardener loop unless the
  sources show a real backlog, cold-lane retrieval failure, or repeat broad-read
  cost that justifies more machinery.

The owner-thread question:

> What is the strongest target architecture for making Orca repo navigation and retrieval god-tier while avoiding repo-map PR conflicts and main-map bloat?

## Mandatory 3-Subagent Requirement

Spawn exactly three independent read-only advisory subagents if your runtime
supports subagents. Use inherited/default runtime settings unless your host
explicitly supports safe overrides. Do not edit files in subagents.

If you cannot spawn exactly three independent subagents, stop and return:

```text
BLOCKED_3SUBAGENT_UNAVAILABLE
```

Do not replace the requested three-subagent evidence pack with a single local
simulation unless the couriering user explicitly authorizes fallback.

## Subagent 1: Directional Architecture Case

Ask for the strongest source-backed case for the low-churn layered architecture:

- main map as curated router;
- generated on-demand inventory as complete file-level findability;
- area submaps as durable detail;
- retrieval-health line in the session capsule as cold-lane warning surface;
- recent-change inbox as low-conflict satellite;
- triggered promotion-on-touch instead of standing batch work.

Return concise claims with `file:line` citations.

## Subagent 2: Adversarial Architecture Case

Ask for the strongest case against the layered architecture and for omitted
better options. It must test:

- whether full manual inventory in the main map is actually better;
- whether a committed generated inventory is needed despite on-demand `header_index`;
- whether generated inventory or health lines create false confidence;
- whether periodic gardener batching reintroduces conflict hotspots;
- whether triggered promotion-on-touch misses durable navigation drift;
- whether submaps increase fragmentation;
- hidden maintenance and validation burden;
- fake-success paths.

Return concise claims with `file:line` citations.

## Subagent 3: Grounding / Anti-Bloat Case

Ask for the smallest repo-native architecture that preserves retrievability
while cutting bloat. It must identify:

- core versus satellite surfaces;
- what should remain manual versus generated;
- what should be checked by deterministic hooks/gates;
- what should remain judgment-based promotion-on-touch work;
- whether the smallest next routing object is a read-only retrieval probe,
  a decision-record amendment, or no new artifact.

Return concise claims with `file:line` citations.

## Main Return Shape

Do not make the final owner-thread architecture decision. Return an advisory
evidence pack for adjudication with exactly these sections:

```text
ADVISORY_EVIDENCE_PACK_ONLY

Workspace Readback:
- branch:
- HEAD:
- dirty state:
- source context: READY | INCOMPLETE
- subagents launched: 3 | BLOCKED_3SUBAGENT_UNAVAILABLE

Directional Lane:
- result:
- strongest claims:
- cited evidence:
- risks it accepts:

Adversarial Lane:
- result:
- strongest objections:
- cited evidence:
- architecture changes it would demand:

Grounding Lane:
- result:
- core:
- satellite:
- bloat cuts:
- cited evidence:
- smallest next routing object:

Option Comparison For Adjudicator:
- AO-1 Manual full main-map inventory:
- AO-2 Generated inventory only:
- AO-3 Current fix only:
- AO-4 Layered map + on-demand generated inventory + triggered promotion-on-touch:
- AO-5 Standing gardener or committed generated inventory if genuinely justified:

Not Proven / Source Gaps:
-

Decision Pressure:
- what the owner-thread must decide before implementation:
- what would change the recommendation:

Non-Claims:
- not implementation authorization
- not validation
- not approval
- not readiness
- not source-of-truth promotion
- not a final architecture decision
```

Keep the whole response compact enough to paste back into an adjudication
thread. Prefer cited bullets over prose.
````
