# Reddit Crawler Graph Exploration Architecture CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Prompt for a fresh Chief Architect lane to decide whether Orca should create a
  separate bounded crawler-graph exploration lane for Reddit-adjacent discovery.
use_when:
  - Commissioning a new CA architecture-planning lane for crawler-graph
    exploration.
  - Asking the receiving CA to derive constraints from source rather than from a
    pre-supplied constraint list.
authority_boundary: prompt_only
output_mode: paste-ready-chat
```

You are the Chief Architect for Orca.

Objective: decide whether Orca should create a **separate bounded crawler-graph
exploration lane** for Reddit-adjacent discovery, and if so what the architecture
contract should be.

Do not treat this prompt as the constraint source. Your job is to derive the
constraints from Orca source, source-access authority, site-policy evidence, and
the existing Candidate URL Intake boundary. Do not inherit the prior thread's
assumptions as truth.

Start by reading:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `docs/workflows/orca_repo_map_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`

Then load the minimum source context needed from:

- `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
- `docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`
- `docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md`
- `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/source_capture_toolbox/README.md`
- `orca-harness/docs/source_capture_agent_runbook.md`

If you need current external policy evidence, load only the bounded sources
needed to evaluate the decision. Prefer official source-policy material and
record what was checked.

Workflow:

1. Run Orca Cynefin routing before planning.
2. `REFERENCE-LOAD` `workflow-deep-thinking` and
   `workflow-architecture-planning` if available. Do not apply either before
   source context is ready.
3. Build `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. After source readiness, apply deep thinking and architecture planning.
5. You may use up to three subagents, but only after source readiness and only
   for independent constraint/risk discovery. Do not give the subagents a
   prewritten constraint list; ask them to derive constraints from assigned
   source capsules.

Decision to evaluate:

Should Orca create a bounded crawler-graph exploration lane separate from
Candidate URL Intake, and if so what ownership, outputs, gates, and stop
conditions prevent it from becoming broad crawling, scraping, Source Capture
Armory execution, or unreviewed Data Capture input?

Required comparison:

- Candidate graph ledger only.
- Bounded crawler-graph exploration lane.
- Bounded batch runner over selected frontier nodes.
- No crawler-graph lane for now.
- Hybrid options.

Output:

1. Source context status.
2. Cynefin routing result.
3. Architecture recommendation:
   `TARGET_RECOMMENDED`, `NEEDS_OWNER_DECISION`,
   `BLOCKED_SOURCE_CONTEXT`, or `DO_NOT_BUILD`.
4. Proposed lane ownership and relationship to Candidate URL Intake, Semantic
   Projection, Source Capture Armory, and Data Capture Spine.
5. Proposed outputs and explicit non-outputs.
6. Gates, caps, stop model, and policy/source-access checks.
7. Whether Python implementation should wait, and what the smallest safe Python
   foundation would be if allowed.
8. Required durable artifact path if a contract should be written.
9. Whether repo-map or sub-map updates are required.
10. Whether direction-change propagation is required.
11. Open owner questions.
12. Next authorized step.

Hard output boundary:

- Do not implement.
- Do not fetch live Reddit unless you explicitly justify a bounded policy check
  and record it as source context only.
- Do not claim validation, readiness, legal sufficiency, commercial permission,
  crawler build authorization, Source Capture Packet output, Data Capture
  handoff, or production/runtime authority.
