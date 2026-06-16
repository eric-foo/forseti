# Reddit Capture Lane Migration Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Handoff prompt
scope: Cold-lane prompt for migrating Reddit capture routing out of the generic Source Capture Playbook and into a Reddit source-family lane/pointer model.
use_when:
  - Commissioning a docs-only lane to separate Reddit capture routing from the generic Source Capture Playbook.
  - Updating Source Capture Armory routing plus the Orca repo map and Data Capture submap for Reddit capture.
open_next:
  - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
authority_boundary: retrieval_only
```

## Handoff Packet

You are the fresh lane for the Orca Reddit capture routing migration. Your job
is to make Reddit capture a clearly source-specific lane under Source Capture
Armory, while keeping the generic Source Capture Playbook generic.

This is a docs-only migration unless the owner explicitly grants a narrower
implementation task in your current turn.

## Goal Handoff

Long-term goal: Orca's capture spine should route platform-specific capture
work through explicit source-family lanes so agents do not bypass the intended
capture path when a platform has special discovery, access, blocking, or
projection needs.

Anchor goal for this lane: migrate Reddit capture operating guidance out of
`docs/product/source_capture_toolbox/source_capture_playbook_v0.md` and make
that generic playbook point to the Reddit source-family lane instead. Update the
Source Capture Armory index plus the top-level repo map and Data Capture submap
so a cold agent can find the Reddit lane without relying on chat context.

Success signal: a cold agent that opens the generic Source Capture Playbook for
a Reddit task is routed to the Reddit lane before choosing any Reddit capture
method. The same cold agent can then follow repo-map and submap pointers to the
Reddit discovery, selection, exact-thread capture, consolidation, and agent-view
surfaces without treating generic browser/search capture as a substitute.

## Routing Preflight

Run Orca Cynefin routing before planning. Expected classification:

- Smallest complete outcome: docs-only routing migration for Reddit capture.
- Regime: complicated.
- Why: the work is mostly source hierarchy and routing authority, but the target
  can be reasoned from current repo sources.
- Decomposition: layer-based.
- Current bottleneck: prevent execution bypass by removing live Reddit-specific
  operating order from generic or stale routing surfaces.
- Riskiest assumption: that "migrate Reddit capture out" means pointerization,
  not a wholesale file move or capture implementation rewrite.
- Stop or pivot condition: a controlling source still requires a Reddit route
  that conflicts with the current Reddit operator playbook and cannot be
  reconciled by narrow doc edits.
- Allowed next move: patch the routing docs and maps listed in this handoff.
- Disallowed next move: change Reddit capture behavior, runner code, ECR,
  Cleaning, Judgment, commercial access, broad crawling, or platform-wide lane
  architecture.

## Required Source Pack

Load these before editing:

- Current user instruction and `AGENTS.md`.
- `.agents/workflow-overlay/README.md`.
- `.agents/workflow-overlay/decision-routing.md`.
- `.agents/workflow-overlay/source-loading.md`.
- `.agents/workflow-overlay/source-of-truth.md`.
- `.agents/workflow-overlay/artifact-folders.md`.
- `.agents/workflow-overlay/retrieval-metadata.md`.
- `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`.
- `docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`.
- `docs/product/source_capture_toolbox/README.md`.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`.
- `docs/workflows/orca_repo_map_v0.md`.
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`.
- `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`.
- `docs/product/data_capture_spine/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`.
- `docs/product/data_capture_spine/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md`.
- `orca-harness/docs/source_capture_agent_runbook.md`.
- Presence check only: `orca-harness/runners/` and `orca-harness/source_capture/`
  for Reddit runner/module names. Do not edit code unless the owner grants an
  implementation task.

Do not trust this prompt as source-of-truth. Re-read the files in your target
worktree and report any mismatch.

## Current Observations To Verify

These were observed from branch `codex/reddit-capture-migration-handoff` created
from `0fc58cfe`. Treat them as starting context, not proof for your lane:

- `main` did not contain
  `docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`
  when this handoff was authored. A main-based worktree may be stale for this
  migration.
- `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` says the
  Source Capture Playbook is a generic method and that per-source recipe cards
  are authored by probes, but it still has Reddit-specific live route notes.
- `docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`
  already presents a Reddit lane view: discovery candidate rows, Graph Frontier
  selection, exact-thread capture/consolidation, and cleaned agent view.
- `docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`
  says exact old Reddit thread URLs use old Reddit Direct HTTP first when current
  old Reddit HTML is the capture target and the bounded batch runner accepts the
  URL; CloakBrowser remains the anti-blocking/browser-visible route when Direct
  HTTP is unsuitable or blocked.
- `.agents/workflow-overlay/source-loading.md` still appeared to say, in live
  pack text, that Reddit pre-commercial capture order is CloakBrowser
  anti-blocking first once implemented. This can bypass the migrated lane if not
  reconciled.
- `docs/workflows/orca_repo_map_v0.md` and
  `docs/workflows/data_capture_spine_consolidation_map_v0.md` contain older
  Reddit CloakBrowser / proxy route language that may need narrowing or
  retargeting to the Reddit lane.
- The harness in the observed branch had Reddit runner/module names such as
  `run_reddit_old_http_batch.py`, `run_reddit_candidate_intake_live.py`,
  `run_reddit_graph_frontier_register.py`, `run_reddit_consolidation.py`,
  `run_reddit_batch_quality_summary.py`, and `run_reddit_agent_view.py`. Verify
  this in your target branch before claiming runner availability.

## Required Migration Shape

Preferred solution: pointer-only migration.

Make the generic Source Capture Playbook say, in effect:

- it remains the generic source-capture intake method;
- source-specific operational recipes live in source-family lane artifacts;
- Reddit capture is source-specific and should route to the Reddit lane before
  choosing discovery, selection, exact-thread capture, consolidation, or
  projection/agent-view reads;
- generic browser/search capture must not be used as a Reddit capture fallback
  unless the Reddit lane explicitly routes there for a bounded case.

Make the Reddit lane surface say, in effect:

- it is the Reddit source-family operating lane under Source Capture Armory;
- it owns the current Reddit operator path for bounded personal/pre-commercial
  Reddit capture;
- discovery/search/listing and graph/frontier work produce candidate rows or
  registers, not Source Capture Packets;
- exact old Reddit thread URLs are the bridge into capture;
- old Reddit Direct HTTP is the current exact-thread default when its stated
  conditions hold;
- CloakBrowser/browser-visible capture is for unsuitable/blocked Direct HTTP or
  browser-visible needs, not a reason to skip a working exact-thread Direct HTTP
  capture;
- cold anonymous `.json` is not the spine;
- capture does not authorize broad crawling, commercial use, production
  monitoring, ECR, Cleaning, Judgment, or buyer-proof claims.

If the existing `reddit_capture_operator_playbook_v0.md` can carry this role
cleanly, do not create a new Reddit lane artifact. If it cannot, create the
smallest explicit Reddit lane artifact and make the current operator playbook
point to it. Do not rename or move files just to make the folder prettier.

## Expected Touch Points

Patch only what is needed from this list:

1. `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`
   - Remove or neutralize live Reddit-specific route instructions.
   - Add a short pointer to the Reddit lane for any Reddit capture work.
   - Preserve generic route-catalog and probe/recipe-card behavior.

2. `docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`
   - Confirm or add front-door language that this is the Reddit source-family
     lane/operator surface under Source Capture Armory.
   - Keep exact-thread Direct HTTP, CloakBrowser, archive fallback, warm JSON,
     discovery, Graph Frontier, consolidation, and agent-view boundaries
     aligned with existing source-backed language.

3. `docs/product/source_capture_toolbox/README.md`
   - Ensure the Source Capture Armory index points to the Reddit lane as the
     current Reddit capture route.
   - Do not duplicate the whole Reddit playbook in the README.

4. `.agents/workflow-overlay/source-loading.md`
   - Inspect live Reddit source-loading text.
   - If it still routes Reddit pre-commercial capture to CloakBrowser first in
     conflict with the Reddit operator playbook, patch it narrowly so future
     agents load the Reddit lane and preserve the exact-thread Direct HTTP first
     condition.
   - Do not rewrite unrelated source-loading packs.

5. `docs/workflows/data_capture_spine_consolidation_map_v0.md`
   - Update the Data Capture submap fast route and current-reality sections so
     Reddit capture points to the Reddit lane/operator playbook.
   - Preserve separate Candidate URL Intake and Graph Frontier boundaries.
   - Remove any live wording that makes CloakBrowser the first step for all
     Reddit capture when exact-thread Direct HTTP is available.

6. `docs/workflows/orca_repo_map_v0.md`
   - Update only the top-level pointer/stale-if/DCP surfaces needed so cold
     agents know Reddit capture is source-specific and should go through the
     Data Capture submap or Reddit lane.
   - Keep detailed Reddit routing in the submap and Reddit lane, not the top
     map.

## Do Not Do

- Do not change capture runner code.
- Do not create new Reddit capture implementation.
- Do not run live Reddit capture as validation for this docs migration.
- Do not change projection, ECR, cleaning, or judgment doctrine.
- Do not make commercial Reddit, API, proxy, anti-detect, storage, dashboard,
  scheduler, deployment, or production-runtime claims.
- Do not treat Reddit search pages, subreddit listings, or candidate discovery
  as Source Capture Packet capture.
- Do not delete historical DCP receipts because their old terms are searchable.
  Update live routing text and add a new DCP receipt instead.

## Validation

At minimum, run and report:

- `git diff --check`
- `python .agents/hooks/check_retrieval_header.py --changed`
- `python .agents/hooks/check_repo_map_freshness.py --changed`
- `rg -n "Reddit|reddit|CloakBrowser|old Reddit Direct HTTP|\\.json|source_capture_playbook|reddit_capture_operator" .agents/workflow-overlay/source-loading.md docs/product/source_capture_toolbox/source_capture_playbook_v0.md docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md docs/product/source_capture_toolbox/README.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/workflows/orca_repo_map_v0.md`

If a hook is unavailable or fails for reasons unrelated to your patch, state the
observed failure and do not convert it into success.

## Direction Change Propagation

This is a routing/doctrine migration, so changed docs that already use Direction
Change Propagation should receive a new narrow DCP receipt. Include:

- what routing changed;
- which surfaces were checked;
- the stale-language search run;
- downstream consumers affected;
- explicit non-claims.

If you touch a durable artifact without a retrieval header and the retrieval
metadata contract applies, add the header. Do not use retrieval metadata to
claim approval, validation, readiness, or authority.

## Required Closeout

Return:

- files changed;
- branch and commit/worktree state actually observed;
- validation commands and actual results;
- remaining stale/conflicting source text, if any;
- whether the migration is complete or requires owner adjudication.

Do not open a PR unless the owner asks for one in your current turn.

## Courier Prompt

Get back context from this handoff artifact:

`docs/prompts/handoffs/reddit_capture_lane_migration_handoff_prompt_v0.md`

Your lane is docs-only unless newly authorized otherwise. Migrate Reddit capture
routing out of the generic Source Capture Playbook into the Reddit
source-family lane/pointer model, update Source Capture Armory routing plus the
repo map and Data Capture submap, and reconcile any live source-loading text
that would still make future agents bypass the Reddit lane. Re-read all source
files in your target worktree; do not trust chat context or this prompt as
proof.
