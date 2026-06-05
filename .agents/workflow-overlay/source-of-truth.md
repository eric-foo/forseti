# Source Of Truth

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Source hierarchy, conflict rules, doctrine-change propagation, and known source documents.
use_when:
  - Resolving Orca source precedence.
  - Checking whether a document is a known Orca source.
  - Changing product, architecture, workflow, validation, review, output, or lifecycle doctrine.
authority_boundary: retrieval_only
```

## Current Source Hierarchy

1. Explicit user instruction for the current turn.
2. Orca `AGENTS.md`.
3. This overlay under `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Explicitly invoked or resolver-loaded skills may provide task-local mechanics only; they are not Orca project authority.

## Conflict Rules

- Orca overlay wins for Orca project facts.
- External workflow sources do not own Orca project authority. Skills may provide task-local mechanics only when explicitly invoked or resolver-loaded.
- Installed global/user/plugin skills are runtime copies or external tools, not Orca project authority.
- If a required source is missing, report a visible failure and name the missing file or decision.
- Source hierarchy is not a read-all list. Use `.agents/workflow-overlay/source-loading.md` and `docs/workflows/orca_repo_map_v0.md` to choose bounded source packs.

## Doctrine Change Propagation Contract

Doctrine-changing work is any source-changing edit that changes a durable rule
future agents may follow for product doctrine, architecture doctrine, workflow
authority, validation philosophy, review authority, output authority, or a
lifecycle boundary.

Use these trigger values:

- `product_doctrine`
- `architecture_doctrine`
- `workflow_authority`
- `validation_philosophy`
- `review_authority`
- `output_authority`
- `lifecycle_boundary`

Each `direction_change_propagation` receipt keeps `trigger` as one primary
trigger for backward compatibility and route clarity. If a source-changing edit
materially touches additional doctrine dimensions, add `related_triggers` as a
list using the same trigger vocabulary. `related_triggers` is discovery and
routing metadata only: it does not replace the primary trigger, reduce the
required controlling-source update, or reduce downstream surface checks.
An additional doctrine dimension is material when it changes which downstream
surface must be checked, changes which future agent route can rely on the
receipt, or is explicitly identified by a source, review, or receipt as a
secondary propagation risk. Do not add `related_triggers` for incidental topic
overlap, examples, quoted vocabulary, or context that does not affect routing
or downstream checks.

Before claiming completion for doctrine-changing work, update the controlling
source and check the downstream source-loaded surfaces that could continue to
route agents by stale doctrine. At minimum, consider:

- top-level agent instructions such as `AGENTS.md` and `CLAUDE.md`;
- the controlling overlay file under `.agents/workflow-overlay/`;
- start-route and source-loading surfaces such as
  `.agents/workflow-overlay/source-loading.md` and
  `docs/workflows/orca_repo_map_v0.md`;
- executor, prompt, validation, review, and closeout surfaces when the doctrine
  affects them.

Store the propagation evidence inline in the changed artifact, prompt, handoff,
or final closeout. Do not create a standalone receipt file, new skill,
registry, broad template sweep, or automation for this loop unless a later turn
explicitly authorizes that expansion.

Use this receipt shape:

```yaml
direction_change_propagation:
  doctrine_changed: "<one sentence>"
  trigger: product_doctrine | architecture_doctrine | workflow_authority | validation_philosophy | review_authority | output_authority | lifecycle_boundary
  related_triggers: [] # optional discovery/routing metadata; does not reduce required checks
  controlling_sources_updated:
    - "<path>"
  downstream_surfaces_checked:
    - "<path>"
  intentionally_not_updated:
    - path: "<path>"
      reason: "<why unchanged>"
  stale_language_search: "<query or not_run + why>"
  non_claims:
    - "not validation"
    - "not readiness"
```

If propagation cannot be completed, return an explicit blocker instead of a
completion claim:

```yaml
direction_change_propagation_blocker:
  doctrine_changed: "<one sentence>"
  trigger: product_doctrine | architecture_doctrine | workflow_authority | validation_philosophy | review_authority | output_authority | lifecycle_boundary
  related_triggers: [] # optional discovery/routing metadata; does not reduce required checks
  blocking_surface: "<missing, conflicting, or unchecked path/source>"
  attempted_check: "<what was attempted>"
  allowed_next_step: "<narrow action that would unblock propagation>"
  non_claims:
    - "not validation"
    - "not readiness"
```

The receipt or blocker is propagation evidence only. It is not validation,
readiness, approval, acceptance, proof, implementation authorization, or source
promotion.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has an ordinary-start quick path for tiny, non-doctrine work and
    marks the repo map as the active retrieval-only map instead of a proposed
    map, without changing source authority, validation, readiness, or
    implementation authorization.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Root instructions already require the overlay and decision-routing
        preflight for substantial or doctrine-bearing work. The quick path is a
        source-loading detail for tiny, non-doctrine work.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay entrypoint already lists source-loading, source-of-truth,
        and decision-routing owners. No new overlay section was added.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        The quick path points to existing bypass conditions and does not change
        the router's trigger, bypass, or output rules.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt preflight and repo_map_decision behavior are unchanged. The
        quick path does not apply to repo-aware prompt authoring.
    - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
      reason: >
        Prompt behavior remains bound to prompt-orchestration and source-loading
        for repo-aware prompts; duplicating the quick path into templates would
        create drift.
  stale_language_search: >
    rg -n "PROPOSED_MAP|ACTIVE_RETRIEVAL_MAP|Ordinary-Start Quick Path|tiny, non-doctrine|mandatory repo-map read|mandatory Cynefin"
    AGENTS.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  stale_language_search_result: >
    Executed on 2026-06-06 after this patch. Hits were the intended active
    retrieval-map status in docs/workflows/orca_repo_map_v0.md, the
    Ordinary-Start Quick Path in source-loading.md, and this DCP receipt. No hit
    retained PROPOSED_MAP or introduced a mandatory repo-map read or mandatory
    Cynefin route for tiny, non-doctrine work.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
    - not repo-map authority expansion
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Repo-aware Orca prompts now record a repo_map_decision and repo_map_reason
    in required preflight so repo-map routing is explicit without making the
    repo map a mandatory read.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/source-loading.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading already owns source-pack and repo-map read mechanics.
        This patch records a prompt-preflight decision; it does not change the
        read-pack rule or make repo-map loading mandatory.
    - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
      reason: >
        The shared behavior contract already requires repo-aware prompts to
        follow prompt-orchestration for source-gated method use and output mode
        rules. Manually duplicating the new preflight field into templates would
        create drift.
  stale_language_search: >
    rg -n "repo_map_decision|repo_map_reason|repo-map routing|mandatory read for every prompt"
    .agents/workflow-overlay docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  stale_language_search_result: >
    Executed on 2026-06-05 after this patch. Hits were the intended
    prompt-orchestration preflight field and this source-of-truth receipt. No
    hit required template-by-template duplication or converted the repo map into
    a mandatory read.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not repo-map freshness proof
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has a lightweight Cynefin Routing Layer that classifies non-trivial
    work before planning, delegation, review, patching, or infrastructure
    expansion.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt orchestration already owns prompt families and source-gated
        method sequencing. This patch adds router propagation to the shared
        behavior contract, without changing output modes, preflight fields, or
        prompt validation verdicts.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The overlay README and source-of-truth known-source list are sufficient
        for this new overlay section. The repo map is already dirty from another
        lane and does not need a routing-map change for the router to be found.
  stale_language_search: >
    rg -n "Cynefin Routing Layer|decision-routing|decision_routing|before planning or delegation"
    AGENTS.md .agents/workflow-overlay docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  stale_language_search_result: >
    Executed on 2026-06-05 after this patch. Hits were the intended AGENTS
    trigger, overlay README section, decision-routing owner file, source-of-truth
    receipt and known-source entry, and shared prompt behavior contract. No hit
    placed the full router in AGENTS.md, converted it into validation/readiness,
    or treated prompt behavior as live-chat authority.
  non_claims:
    - not validation
    - not readiness
    - not review authority
    - not implementation authorization
    - not source promotion
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca doctrine-change propagation receipts now keep one primary trigger and
    may add related_triggers for secondary doctrine dimensions that need
    machine-detectable routing.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/communication-style.md
  intentionally_not_updated:
    - path: docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
      reason: >
        The owner-contract DCP receipt remains a primary architecture-doctrine
        change. The concrete lifecycle-audit failure mode was exposed in the
        gate-map DCP receipt, which now carries related_triggers.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Validation-gate doctrine still requires a DCP receipt or blocker. This
        patch changes DCP trigger grammar, not validation-gate pass/fail rules.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt closeout still delegates doctrine-change propagation to this
        source-of-truth contract. No prompt output mode or wrapper rule changes.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        Response-style guidance still points to DCP receipts or blockers without
        owning receipt grammar.
  stale_language_search: >
    rg -n "related_triggers|additional_trigger|multi-trigger DCP|one trigger|trigger: architecture_doctrine|lifecycle-boundary implications"
    .agents/workflow-overlay/source-of-truth.md
    .agents/workflow-overlay/source-loading.md
    docs/workflows/orca_repo_map_v0.md
    docs/product/judgment_spine_gate_ownership_map_v0.md
    docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
  stale_language_search_result: >
    Executed on 2026-06-03 after the AR-01 through AR-03 minor review patch for
    the DCP primary/related trigger grammar. Hits in source-of-truth are
    expected trigger vocabulary, related_triggers grammar, field-level comments,
    threshold guidance, this DCP receipt, and non-claims. Hits in source-loading
    and repo-map are expected navigation references. Hits in the gate map are
    expected primary trigger and related_triggers receipt fields. Hits in the
    owner contract are expected architecture-doctrine primary trigger fields.
    No hit converted related_triggers into validation, readiness, acceptance,
    source-of-truth promotion, buyer proof, fixture admission, scoring
    authorization, model-execution authorization, or judgment-quality evidence.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - not implementation authorization
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca no longer imports or recognizes external workflow-core / agent-workflow
    source documents as reusable workflow authority; only explicitly invoked or
    resolver-loaded skills may provide task-local mechanics.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - AGENTS.md
    - CLAUDE.md
    - README.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/skill-adoption.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - README.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/skill-adoption.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        Skill provenance paths that contain agent-workflow remain because the
        user explicitly preserved skills. These paths record resolver-visible
        skill evidence only, not workflow-core authority.
  stale_language_search: >
    rg -n "workflow-core|@\\.\\./agent-workflow|supersede any conflicting local|Future accepted `agent-workflow`|Future `agent-workflow` source|reusable `agent-workflow`|agent-workflow.*mechanics|agent-workflow material|agent-workflow.*source guidance|agent-workflow.*prompt-orchestrator|candidate for promotion to the `agent-workflow`|workflow-kernel|future kernel skill|AGENTS.md.*operating constraints"
    AGENTS.md CLAUDE.md README.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-05 after this patch. Matches were confined to this
    DCP receipt's doctrine_changed, intentionally_not_updated, and
    stale_language_search text; no live authority or route-card surface outside
    this receipt matched.
    A broader `rg -n "agent-workflow" AGENTS.md CLAUDE.md README.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md`
    returned only skill-adoption provenance paths for the preserved skill
    exception plus this DCP receipt.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not resolver proof
    - not skill adoption
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca repo-map routing now keeps the main repo map thin and routes Data
    Capture and Judgment owner inventories through their consolidation submaps.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Root instructions already route project facts and workflow authority
        through the Orca overlay and do not enumerate repo-map/submap details.
    - path: CLAUDE.md
      reason: >
        Claude shim imports AGENTS.md and carries no independent Orca map
        routing.
    - path: docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
      reason: >
        Judgment submap already functions as the entry map; this patch changes
        source-loading to enter through it, not the submap's owner inventory.
  stale_language_search: >
    rg -n "Data Capture Setup / Pressure-Test Packet|data_capture_spine_consolidation_map_v0|Judgment Spine Evidence Ladder Read Pack|judgment_spine_consolidation_map_v0|last reported working hash|B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5|Current post-clarification synthesis hash"
    .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-05 after this patch. Remaining hits were the intended
    Data Capture submap pointers, Judgment submap pointers, source-loading
    read-pack heading, source-of-truth known-source entries, this DCP receipt,
    and historical Data Capture submap DCP text. No live main repo-map route
    retained the removed historical hash pins or the long Data Capture owner-doc
    inventory.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not acceptance
    - not implementation authorization
```

## Known Source Documents

- `README.md`: workspace entrypoint.
- `AGENTS.md`: agent operating instructions.
- `CLAUDE.md`: Claude Code instruction shim that imports `AGENTS.md`; no Orca project authority of its own.
- `.agents/workflow-overlay/README.md`: overlay entrypoint.
- `.agents/workflow-overlay/artifact-roles.md`: Orca artifact role bindings, permissions, freshness markers, and paired artifacts.
- `.agents/workflow-overlay/source-loading.md`: Orca source-loading budgets, read packs, and context-bloat controls.
- `.agents/workflow-overlay/decision-routing.md`: Orca Cynefin Routing Layer for non-trivial, ambiguous, cross-thread, delegated, doctrine-bearing, or messy-worktree work.
- `.agents/workflow-overlay/retrieval-metadata.md`: Orca retrieval-header contract for durable human-authored workflow artifacts.
- `.agents/workflow-overlay/prompt-orchestration.md`: Orca prompt artifact, wrapper, preflight, output mode, validation, and rerun bindings.
- `.agents/workflow-overlay/template-registry.md`: Orca-owned prompt template registry for project-local templates.
- `.agents/workflow-overlay/product-proof.md`: Orca buyer-proof semantics, trust-objection handling, pull signals, and product-proof non-claims.
- `.agents/workflow-overlay/communication-style.md`: Orca response style for Chief Architect sequencing, review closeouts, and prompt handoffs.
- `.agents/workflow-overlay/delegated-review-patch.md`: provisional, opt-in Delegated Review-and-Patch convention for high-stakes authored artifacts, plus overlay-interface fields a future skill implementation may read; not a bound review lane and creates no strict claims.
- `docs/STRUCTURE.md`: docs-folder usage guide for future agents; subordinate to this overlay if conflicts appear.
- `docs/workflows/orca_bootstrap_record.md`: Turn 6 bootstrap record.
- `docs/workflows/orca_repo_map_v0.md`: compact repo map for source-pack selection and prompt setup.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`: retrieval-only entry map for Data Capture Spine and Source Capture Armory navigation; routes to owner sources and carries no source-access, validation, readiness, implementation, ECR, Cleaning, or Judgment authority.
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`: retrieval-only entry map for Judgment Spine navigation across product docs, research docs, cases, manifest, conductor, gate ownership, evidence ladder, JSG-08, and harness surfaces; routes to owner sources and carries no validation, readiness, buyer-proof, fixture-admission, scoring, model-execution, or judgment-quality authority.
- `docs/migration/import_queue.md`: read-only import queue state.
- `docs/decisions/turn_08_product_thesis_v0.md`: current Orca product thesis and value proposition.
- `docs/product/judgment_spine_evidence_ladder_architecture_v0.md`: Judgment Spine claim-tier architecture for Product-Learning, Buyer-Proof, and Judgment-Quality evidence boundaries.
- `docs/product/judgment_spine_gate_ownership_map_v0.md`: Judgment Spine gate ownership map for source identity, packet freeze, no-tools isolation, memorization probe, sealed output, scoring, reveal/calibration, classification, and closeout blockers.
- `docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md`: JSG-08 owner contract for outcome reveal/calibration receipt shape, satisfaction states, scoring relationship, and claim caps.
- `docs/workflows/turn_08_workflow_bedrock_maximization.md`: docs-first maximization plan for `workflow-deep-thinking`, future `workflow-product-ultraplan`, and future `workflow-feature-ultraplan`.
