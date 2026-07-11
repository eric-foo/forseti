# DCP Receipts Archive

```yaml
retrieval_header_version: 1
artifact_role: DCP receipts archive
scope: Frozen legacy archive of direction_change_propagation receipts cycled out before 2026-07-11.
use_when:
  - Auditing the full propagation history of past doctrine changes.
  - Verifying that a stale-language search term was already handled in a prior receipt.
  - Tracing which surfaces were checked or intentionally skipped for a historical doctrine change.
authority_boundary: retrieval_only
```

Frozen 2026-07-11. Do not append new receipts. Forseti controlling files keep at
most two current inline receipts and delete the oldest when adding a third; Git
and PR history preserve later history. The governing rule lives in
`.agents/workflow-overlay/source-of-truth.md`, Doctrine Change Propagation
Contract. This file carries no source authority, validation evidence, readiness,
approval, or lifecycle claims and is not loaded for ordinary doctrine work.

## From .agents/workflow-overlay/source-of-truth.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forked-context subagent spawning now treats inherited runtime defaults as
    omitted fields and forbids explicit default/null type or model overrides.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already routes delegated work to the overlay; duplicating payload
        mechanics would fork the rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        Already names decision-routing as the delegated-work owner.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Subagent source-context rules are unchanged; payload hygiene belongs in
        decision-routing.
    - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
      reason: >
        Already points delegated prompt work to decision-routing.
  stale_language_search: >
    rg -n "fork_context|full-history fork|agent_type|runtime-safe forked|default/null|inherited defaults"
    AGENTS.md .agents/workflow-overlay docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  stale_language_search_result: >
    Executed on 2026-06-08 after this patch. Hits were the intended subagent
    runtime payload rule in decision-routing.md and this DCP receipt in
    source-of-truth.md. No downstream surface retained a conflicting instruction
    to combine full-history fork with explicit default/null type or model
    overrides.
  non_claims:
    - not validation
    - not readiness
    - not model routing
    - not host API schema authority
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Doctrine Change Propagation Contract now requires propagated
    restatements to stay faithful to the controlling source's strength — no
    softening, narrowing, or silent forking, and prefer pointing at the single
    controlling source over copying — and allows stale_language_search to be
    not_run only for a purely additive change.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/source-of-truth.md
    - docs/decisions/doctrine_change_propagation_restatement_integrity_decision_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already requires that CLAUDE.md and downstream surfaces not duplicate,
        fork, or weaken Orca rules and "load the owning overlay file instead of
        duplicating the rule here." The restatement-integrity rule generalizes
        that existing principle into the propagation contract; copying its text
        into AGENTS.md would itself fork the rule it adds.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Already states convenience copies "must not fork the rule." Owner text
        stays solely in source-of-truth.md; source-loading references the
        contract rather than restating it.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Already practices reference-over-copy ("intentionally does not duplicate
        the owner-doc inventory"); routing is unchanged and points to this
        overlay as the propagation owner.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names source-of-truth.md as the
        doctrine-change-propagation owner; no new section owner was added.
  stale_language_search: >
    rg -n 'not_run only|purely additive|reference over copy|prefer reference|do
    not copy|duplicat|fork the rule|faithful to the controlling|must not soften'
    .agents/workflow-overlay AGENTS.md CLAUDE.md docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-08 after this patch (this change includes a schema edit,
    so it is not purely additive and the search is required). A separate check
    confirmed the receipt-schema placeholder stale_language_search lives in
    exactly one place (source-of-truth.md), so the additive-only tightening forks
    no copy. Every duplicate/fork hit elsewhere (AGENTS.md, CLAUDE.md,
    source-loading.md, the repo map, validation-gates.md, and prior DCP receipts)
    already asserts reference-over-copy or no-fork and is consistent with the new
    restatement-integrity rule. No surface retained an instruction to weaken,
    narrow, or freely copy a propagated restatement, and none permitted not_run
    for a non-additive change.
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
    The Cynefin Routing Layer now requires a smallest-complete outcome, allows
    Mixed/Unclear classification, and requires concrete bottleneck and
    evidence-shaped stop/pivot wording.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already triggers the Cynefin Routing Layer and points to the
        owner file. The refinement changes router output details, not the root
        trigger.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already registers the decision-routing owner. No new
        overlay section or owner path was added.
    - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
      reason: >
        The shared prompt behavior contract references the owner file and should
        not duplicate the router fields.
  stale_language_search: >
    rg -n "Smallest complete outcome|Mixed or Unclear|mixed or unclear|concrete bottleneck|evidence-shaped stop|decision_routing"
    .agents/workflow-overlay/decision-routing.md .agents/workflow-overlay/source-of-truth.md docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  stale_language_search_result: >
    Executed on 2026-06-06 after this patch. Hits were the intended owner-file
    output fields, Mixed/Unclear regime text, this DCP receipt, and no live
    YAML-style decision_routing block.
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
    - docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
    - docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/communication-style.md
  intentionally_not_updated:
    - path: docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
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
    docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
    docs/product/judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md
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

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now treats checkpoint artifacts (precompact packets, cold cross-lane
    workflow-handoff state packets, and equivalent lane-state snapshots) as
    non-authoritative, single-consumption state: their volatile claims must be
    re-confirmed against canonical source or disk, and the consuming lane burns
    (deletes) the checkpoint after consumption, keeping one live instance per
    lane. Authored handoff prompts under docs/prompts/handoffs/ are excluded.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/skill-adoption.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The agent kernel already requires confirm-don't-trust (verify the durable
        target with a fresh read before strict claims). This overlay specifies how
        that applies to checkpoint artifacts; it does not change the kernel rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        Checkpoint non-authority is a source-hierarchy/conflict clarification
        inside source-of-truth's existing scope; no new overlay section owner was
        created.
    - path: .agents/workflow-overlay/artifact-roles.md
      reason: >
        The docs/hygiene/ Hygiene-queue role already carries a promotion-or-disposal
        lifecycle that accommodates burning; the new rule adds the consumption
        trigger without contradicting the role binding. The handoff-prompt and
        inbox-scratch roles are explicitly outside the checkpoint rule.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading already treats summaries, context packets, and prior-thread
        notes as orientation, not authority; the checkpoint rule is consistent and
        adds no read-pack change.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Every handoff reference there is an authored handoff PROMPT (a prompt
        role), not a workflow-handoff state packet; the new rule excludes them.
        "Chat checkpoints" there means receipt-level chat facts, a different sense.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        Adoption status of workflow-precompact / workflow-handoff is unchanged; the
        skills still supply mechanics and the overlay binds their use, not the
        skill source. The file is also concurrently modified by another lane and
        was left untouched.
  stale_language_search: >
    rg -ni "precompact|handoff|checkpoint|disposable|burn|single-consumption|re-confirm|retain" .agents/workflow-overlay
  stale_language_search_result: >
    Run 2026-06-06 after this patch. Every "handoff" hit is an authored
    handoff-PROMPT reference (docs/prompts/handoffs/ Planning/Implementation
    handoff role), which the new rule explicitly excludes; "chat checkpoints" in
    prompt-orchestration.md is receipt-level chat facts, a different sense. The
    only state-checkpoint doctrine hits are the new Checkpoint Artifacts section
    and this receipt in source-of-truth.md. No live surface asserts a state
    checkpoint is authoritative or must be retained after consumption.
  non_claims:
    - not validation
    - not readiness
    - not skill adoption
    - not skill-source edit
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now binds the Enforcement Placement principle into the overlay and
    enforces its first instance at a tool boundary: a load-bearing,
    mechanically-checkable rule is enforced by a deterministic substrate
    (write-time hook + portable checker with a --strict CI/commit mode) rather
    than actor-carried instruction. The first instance is the retrieval-header
    check (EP-06): a PostToolUse Write|Edit hook running
    .agents/hooks/check_retrieval_header.py, which references (never restates)
    .agents/workflow-overlay/retrieval-metadata.md. This builds the EP-06
    substrate the prepare-only classification record proposed and left
    owner-gated; the current-turn authorization satisfies that gate.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md          # owns the thin Enforcement Placement principle
    - .agents/workflow-overlay/decision-routing.md          # one-line cross-ref to the owner
    - docs/workflows/orca_repo_map_v0.md                    # Active Hooks note (discoverability + reinstall)
    - .agents/hooks/check_retrieval_header.py               # the substrate (new file; advisory + --strict)
    - .claude/settings.json                                 # PostToolUse Write|Edit hook (new hooks block)
    - docs/decisions/overlay_enforcement_placement_classification_v0.md  # build-status update (EP-06 built; stale_if tripped)
    - .agents/workflow-overlay/source-of-truth.md           # this receipt
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/safety-rules.md
    - docs/workflows/artifact_retrievability_guide.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already routes doctrine and infrastructure work to the overlay and
        decision-routing; the new principle lives in overlay files AGENTS.md
        already points to. No root-instruction change.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already registers validation-gates.md and
        decision-routing.md as owners; the principle is a section within an
        existing owner, not a new overlay file, so no index entry is added.
    - path: .agents/workflow-overlay/retrieval-metadata.md
      reason: >
        It is the enforced rule and remains the single source for header scope,
        exclusions, and fields; the checker references it and must not restate
        it. Unchanged.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        It already owns the bounded-implementation owner gate that the
        current-turn authorization satisfies; the principle was homed in
        validation-gates.md per owner decision. Separately, the new checker
        surfaced that safety-rules.md itself lacks a retrieval header (a
        pre-existing gap) — left to the owner; forward-only, not backfilled here.
    - path: docs/workflows/artifact_retrievability_guide.md
      reason: >
        Report-only retrieval guidance subordinate to retrieval-metadata.md; the
        boundary checker is a separate enforcement substrate that references the
        contract, not this guide. Unchanged.
  stale_language_search: >
    rg -n "Enforcement Placement|enforcement-placement|check_retrieval_header|Active Hooks|hookSpecificOutput"
    AGENTS.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md .claude/settings.json
    docs/decisions/overlay_enforcement_placement_classification_v0.md
  stale_language_search_result: >
    Executed 2026-06-09 after this patch. Hits are confined to the intended
    surfaces: the validation-gates.md principle, the decision-routing.md
    cross-ref, the repo-map Active Hooks note, the checker script, the
    settings.json hook, the prior classification decision (EP-06/07 plus its
    new build-update note), and this receipt. No surface carries a conflicting
    instruction to enforce this rule only by actor-carried instruction, and no
    checked surface restates the retrieval-header rule's body in place of
    referencing retrieval-metadata.md.
  non_claims:
    - not validation
    - not readiness
    - not approval or acceptance
    - not source-of-truth promotion
    - not blanket implementation or runtime authorization beyond this bounded checker and hook
    - the hook and checker enforce header shape, never the truth of any field
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca adds a second Enforcement Placement substrate: a repo-map freshness
    check (.agents/hooks/check_repo_map_freshness.py) that enforces the
    mechanically-detectable subset of the repo map's own stale_if: block at the
    write boundary (a PostToolUse Write|Edit hook) and as a portable --strict
    commit/CI gate. It reads the repo map AS its spec and references the map's
    stale_if as authority, never restating it; advisory and forward-only by
    default. High-precision gate triggers are a new top-level area (stale_if #1)
    and a new orca-harness runner/adapter (#2); source-of-truth edits (#5) are an
    advisory nudge only; judgment-shaped staleness (#3 spine reorg, #4 routing
    doctrine) stays with this Doctrine Change Propagation contract, which already
    lists the repo map as a downstream surface. A legitimate non-map change is
    acknowledged by a repo-map-ack: commit-message token or by the map's
    "do not enumerate" exclusion list; updating the map or a consolidation submap
    in the same change also satisfies the gate.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - .agents/hooks/check_repo_map_freshness.py            # the substrate (new file; advisory + --strict, fails open)
    - .claude/settings.json                                # second PostToolUse Write|Edit hook
    - docs/workflows/orca_repo_map_v0.md                   # Active Hooks note (discoverability, reinstall, ack, recheck recipe)
    - .agents/workflow-overlay/source-of-truth.md          # this receipt
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/artifact_retrievability_guide.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The Enforcement Placement principle there already authorizes reusing the
        write-time-hook + portable-checker pattern for "the next such rule" and
        names the retrieval-header check (EP-06) as the active instance. This is
        that reuse and changes no principle, so no edit. A later turn may add a
        second named active instance there if desired.
    - path: docs/decisions/overlay_enforcement_placement_classification_v0.md
      reason: >
        The per-rule EP classification record governs the previously enumerated
        substrates (EP-06 header check; EP-01/03 permission floor). Recording
        repo-map freshness as a new EP item is a classification-record edit owned
        by that decision and was not in this bounded build's scope; left to the
        owner.
    - path: AGENTS.md
      reason: >
        Already routes doctrine and infrastructure work to the overlay and
        decision-routing; the checker lives in surfaces AGENTS.md points to.
    - path: .agents/workflow-overlay/retrieval-metadata.md
      reason: >
        Different rule (the retrieval-header contract). The freshness checker
        enforces the repo map's stale_if, not the header contract; unchanged.
  stale_language_search: >
    rg -n "check_repo_map_freshness|repo-map freshness|repo-map-ack|Repo-map freshness check"
    .claude/settings.json docs/workflows/orca_repo_map_v0.md
    .agents/workflow-overlay/source-of-truth.md .agents/hooks/check_repo_map_freshness.py
  stale_language_search_result: >
    Executed 2026-06-09 after this patch. Hits are confined to the intended
    surfaces: the checker script, the settings.json second PostToolUse hook, the
    repo-map Active Hooks note, and this receipt. One pre-existing unrelated hit
    remains at source-of-truth.md ("not repo-map freshness proof", a non-claim in
    the earlier repo_map_decision preflight receipt); it does not concern this
    checker. No surface instructs enforcing repo-map freshness only by
    actor-carried instruction, and no checked surface restates the map's stale_if
    body in place of referencing the map.
  non_claims:
    - not validation
    - not readiness
    - not approval or acceptance
    - not source-of-truth promotion
    - not a new EP classification-record entry (left to that owner)
    - the hook and checker enforce map shape, never the truth or completeness of any route
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Judgment Spine routing-pointer batch (ORCA-HYGIENE-008) is complete:
    every entry surface now routes Judgment Spine navigation through the
    consolidation submap — the repo map and the source-loading read pack
    (landed earlier; 2026-06-05 receipt above), and now the spine README
    (open_next trimmed to the single submap pointer, contract body kept) and
    the harness README (submap up-pointer added).
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - docs/research/judgment-spine/README.md
    - docs/research/judgment-spine/harness/README.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
    - docs/research/judgment-spine/manifest_v0.md
    - docs/hygiene/queue.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Its Judgment Spine section already says open the consolidation map
        first (2026-06-04 partial work + 2026-06-05 receipt); unchanged today.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        The Judgment Spine Evidence Ladder Read Pack already starts with the
        consolidation map; covered by the 2026-06-05 routing receipt.
    - path: docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
      reason: >
        It is the routing destination; pointing more surfaces at it changes
        nothing inside it.
    - path: docs/research/judgment-spine/manifest_v0.md
      reason: >
        Inventory owner, not an entry surface; separately brought current
        2026-06-11 (ORCA-HYGIENE-009/012) without routing-doctrine change.
  stale_language_search: >
    rg -n "open_next|manifest open first" docs/research/judgment-spine/README.md
    docs/research/judgment-spine/harness/README.md
  stale_language_search_result: >
    Executed 2026-06-11 after the two README edits. The spine README open_next
    carries exactly the consolidation-map pointer; the harness README open_next
    leads with the submap up-pointer then its local v0_14 and adjacent-context
    entries. Neither README still instructs entering through the manifest or a
    scattered per-doc enumeration.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not acceptance
```

## From .agents/workflow-overlay/delegated-review-patch.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now carries a provisional, opt-in Delegated Review-and-Patch convention:
    under an explicit Chief Architect commission, a de-correlated executor may run
    a combined review-and-patch hardening pass on a single named high-stakes
    authored artifact, with the CA adjudicating the returned diff before anything
    is kept. It is not a bound review lane and creates no strict claims.
  trigger: review_authority
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/review-lanes.md
    - AGENTS.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Model-neutrality, review-prompt findings-first defaults, strict-claim
        gates, and preflight fields are unchanged. The convention defers to them
        and adds a who-constraint, not review-lane model routing.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The convention claims no validation or readiness and creates no new
        validation gate; existing gates are unchanged.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Preflight receipt and source packs are referenced, not changed.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The protected-path list defers to safety-rules as the authority rather
        than forking a new forbidden-edit set; no safety rule changes.
    - path: CLAUDE.md
      reason: >
        CLAUDE.md is a thin shim that loads AGENTS.md and must not duplicate
        Orca rules; the AGENTS.md terse pointer ("...and delegated
        review-and-patch, load the owning overlay file") covers the convention.
        No CLAUDE.md pointer was added.
  stale_language_search: >
    rg -n "source-read-only|Reviewer threads are source-read-only|runtime model|model-neutral|reviewer still does not edit|patch authority"
    .agents/workflow-overlay/review-lanes.md
    .agents/workflow-overlay/prompt-orchestration.md
    AGENTS.md CLAUDE.md
  stale_language_search_result: >
    Run during this binding. Hits are the existing reviewer-read-only rule and
    the existing model-neutrality rule. The convention is consistent with both:
    the delegate is a commissioned executor (not a read-only reviewer), and
    de-correlation is a commission who-constraint, not review-lane model routing.
    No prior text claimed authored artifacts may never be patched or that no
    commissioned-executor path exists, so no language was made stale.
  non_claims:
    - not validation
    - not readiness
    - not formal review authority
    - not a mandatory or machine-routable review lane
    - not runtime model routing
    - not jb authority import
```

```yaml
# no_repo access mode added 2026-06-08, after a de-correlated cross-family no-repo review + bounded recheck (5/5 prior findings closed) and CA adjudication.
direction_change_propagation:
  doctrine_changed: >
    The provisional Delegated Review-and-Patch convention gains a no_repo access mode: a repo-blind
    de-correlated delegate runs advisory-only (portable method), returns findings not a diff, the CA
    applies the patch, and a required de-correlated post-patch re-review restores patch-time
    de-correlation before keep. Review-side de-correlation, CA adjudication, protected paths, and the
    strict-claim boundary are unchanged.
  trigger: review_authority
  related_triggers: [workflow_authority, output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/review-lanes.md          # UPDATED: lane line now distinguishes repo (delegate patches) vs no_repo (delegate read-only/advisory, CA patches)
    - .agents/workflow-overlay/prompt-orchestration.md  # checked, no change: no_repo review prompts use existing paste-ready-chat + the registered portable-method template; deep-thinking-first, model-neutrality, findings-first already apply
    - AGENTS.md                                         # checked, no change: the existing delegated-review-and-patch pointer (line 48) covers the new mode
  intentionally_not_updated:
    - path: docs/decisions/adversarial_review_routing_policy_v0.md
      reason: routing-policy tiers declined by owner (Pile 3); the no_repo mode stands alone
    - path: .agents/workflow-overlay/safety-rules.md
      reason: protected-path set unchanged; the no_repo delegate edits nothing
    - path: .agents/workflow-overlay/validation-gates.md
      reason: advisory findings create no validation or strict claim
  stale_language_search: >
    grep 'NOT a source-read-only review lane|unified diff|patches the target' over review-lanes.md,
    delegated-review-patch.md, AGENTS.md. Result: review-lanes line updated for the two modes; the
    'unified diff' delegate_return is repo-mode-specific and the no_repo subsection states the
    findings-return, so no other language was made stale.
  non_claims:
    - not validation
    - not readiness
    - not a bound, mandatory, or machine-routable review lane (the convention stays provisional)
    - not runtime model routing (access is an operator/commission constraint)
```

```yaml
# Bounded recheck actor refined 2026-06-09 (CA decision): same-family lower/mechanical-tier, not cross-family.
direction_change_propagation:
  doctrine_changed: >
    no_repo post-patch re-review refined: the REQUIRED post-patch re-review is now a BOUNDED closure +
    blast-radius recheck run by a SAME-FAMILY different/lower (mechanical-tier) model, not a cross-family
    de-correlated pass. A bounded recheck verifies a known patch against explicit closure conditions
    (near-mechanical) rather than discovering unknown seams, so cross-family de-correlation — whose value is
    in discovery — is reserved for the discovery (full adversarial) pass and for claiming the
    survives-an-adversarial-review-with-no-new-seam standard. Amends the 2026-06-08 no_repo entry's
    "de-correlated post-patch re-review" to this bounded same-family recheck. CA adjudication, review-side
    de-correlation, protected paths, the freshness gate, and the strict-claim boundary are unchanged.
    who-constraint only; not a runtime-model recommendation.
  trigger: review_authority
  related_triggers: [workflow_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/review-lanes.md
    - AGENTS.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        the no_repo lane line distinguishes repo vs no_repo by who-patches (delegate read-only/advisory,
        CA patches); the recheck-actor tier is owned here and needs no lane-line change.
    - path: .agents/workflow-overlay/delegated-review-patch.md (model_ladder block)
      reason: >
        the executor rung already defines a cheap same-family tier; the bounded recheck reuses that concept
        rather than adding a rung.
  non_claims:
    - not validation
    - not readiness
    - not a bound, mandatory, or machine-routable review lane (the convention stays provisional)
    - not runtime model routing (same-family/lower-tier is a who-constraint)
```

```yaml
# no_repo package shape bound 2026-06-10 (CA decision): self-contained bundle + thin-wrapper, with inline fallback.
direction_change_propagation:
  doctrine_changed: >
    The no_repo access mode now binds a default PACKAGE SHAPE: a self-contained bundle (the
    hash-confirmable verbatim target attachment(s) plus a guardrail-complete README carrying the
    method, authority excerpts, and contract) delivered with a thin-wrapper chat prompt that points
    the repo-blind reviewer at the in-bundle README. The thin wrapper still carries the cross-vendor
    who-constraint (it must not migrate silently into the bundle), and when the reviewer cannot read
    in-bundle files the method is inlined in chat instead. Review-side de-correlation, CA adjudication,
    the verbatim-hash-attachment + freshness-gate requirements, and the strict-claim boundary are unchanged.
  trigger: review_authority
  related_triggers: [output_authority, workflow_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - path: docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md
      note: >
        "How to use" softened from "paste the block" to "deliver verbatim -- pasted or as the bundle
        README; shape bound in delegated-review-patch.md". Prose only; the distilled PORTABLE METHOD
        block and its derived_from pins are unchanged, so no consumer re-pin is owed.
    - path: docs/prompts/templates/wrappers/thin_wrapper_v0.md
      note: >
        the "read & execute the README in the attached bundle" wrapper is a thin-wrapper variant,
        owned by prompt-orchestration. NOT edited here -- flagged for that lane if a registered
        no_repo wrapper variant is wanted.
    - path: .agents/workflow-overlay/review-lanes.md
      note: the repo-vs-no_repo lane line (who-patches) is unchanged; the package shape is owned here.
  intentionally_not_updated:
    - path: workflow-delegated-review-patch (the reusable kernel skill)
      reason: >
        the kernel owns invariants and the commission/adjudication contract, NOT a concrete
        packaging/delivery shape (it states the overlay owns output destinations and "hardcodes none
        of them"). Encoding a package shape there would break its boundary and portability, and it is
        an installed/user-level skill out of edit-bounds without a deployment turn. The shape is an
        overlay binding; the skill is unchanged.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        model-neutrality, findings-first defaults, and preflight fields are unchanged; the thin-wrapper
        shape composes with the existing paste-ready-chat rendering rather than forking it.
  non_claims:
    - not validation
    - not readiness
    - not a bound, mandatory, or machine-routable review lane (the convention stays provisional)
    - not runtime model routing (access mode and package shape are operator/commission constraints)
```

```yaml
# repo-mode discovery discharges a downstream independent-review gate; added 2026-06-13 (CA + owner decision).
direction_change_propagation:
  doctrine_changed: >
    The repo-mode delegated review-and-patch loop -- cross-vendor delegate runs full-artifact discovery and
    authors the bounded fix; CA adjudicates and independently verifies via class-sweep + byte/scope checks --
    SATISFIES a cross_vendor_discovery independent-review requirement for the patched artifact, so a separate
    standalone post-patch re-scan is not additionally required to clear a downstream leakage gate.
    Proportionality is owner-set by assurance tier (buyer-proof may still require a separate pass;
    product-learning / N-case batch may rely on the delegated pass); the one non-independent sliver (the
    delegate's own edited lines) must be mechanically verifiable and the limitation recorded. Contrasts
    no_repo, which still requires the bounded same-vendor post-patch recheck. Validation/who-constraint
    framing only; not runtime-model routing.
  trigger: review_authority
  related_triggers: [validation_philosophy]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - path: .agents/workflow-overlay/review-lanes.md
      note: >
        two-bar rule is consistent (it already names cross_vendor_discovery as the discovery bar); a one-line
        cross-ref that the bar can be DELIVERED via the repo-mode delegated loop is recommended and deferred to
        a low-risk follow-up, not required (no stale routing without it).
    - path: orca/product/spines/judgment/conductor/conductor_construction_integrity_probe_addendum_v1.md
      note: >
        the R6 pre-freeze leakage gate is the consuming gate; conductor v1 is PROPOSED/pending ratification, so
        not edited mid-flight -- reconcile (R6 independent leakage review is satisfiable via the delegated loop)
        at its next revision/ratification.
    - path: .agents/workflow-overlay/validation-gates.md
      note: no new validation gate; this clarifies when an existing independent-review requirement is met.
  intentionally_not_updated:
    - path: AGENTS.md
      reason: the delegated-review-patch pointer already routes here; no top-level rule change.
  receipt_section_hygiene: >
    This file's inline receipt section now exceeds the <=2-most-recent-inline limit (source-of-truth.md DCP
    contract; it already held 4 before this change). Rotation of the older receipts to
    docs/decisions/dcp_receipts_archive_v0.md plus the required archive-pointer line is owed as a separate
    low-risk hygiene pass; deferred here to keep this doctrine change focused and reviewable.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane (the convention stays provisional)
    - not runtime model routing
```

```yaml
# incomplete commission route-out fallback bound 2026-06-16 (CA decision).
direction_change_propagation:
  doctrine_changed: >
    Incomplete delegated-review-patch commissions now route through
    workflow-prompt-orchestrator as paste-ready route-out prompts when target
    and purpose are inferable, with missing operator-owned fields marked
    operator_to_fill; multi-file implementation/code diffs are routed to the
    appropriate review prompt instead of being stretched into this convention.
  trigger: review_authority
  related_triggers: [workflow_authority, output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
  receipt_storage_updated:
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/skill-adoption.md
    - AGENTS.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Already owns prompt-orchestrator authoring, paste-ready-chat output,
        repo-aware prompt preflight, and source-gated review method sequencing;
        this patch routes to that owner instead of duplicating its contract.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        Already defines delegated review-and-patch as provisional, opt-in, and
        not machine-routable; the non-eligible target boundary belongs in the
        convention file rather than in the general lane index.
    - path: workflow-delegated-review-patch skill source and plugin cache
      reason: >
        External/user/plugin skill source is protected and not Orca project
        authority. This Orca behavior is bound in the overlay; reusable upstream
        skill-source changes require a separate skill-governance/deployment turn.
    - path: AGENTS.md
      reason: >
        Already routes delegated review-and-patch to the owning overlay file; a
        root restatement would fork the rule.
  stale_language_search: >
    rg -n "incomplete commission|operator_to_fill|prompt_orchestrator_route_out|multi-file implementation|code diff|machine-routable|workflow-prompt-orchestrator"
    .agents/workflow-overlay AGENTS.md
    plus targeted checks for protected external skill-source boundaries and
    prompt-orchestrator review defaults.
  stale_language_search_result: >
    Executed 2026-06-16. Live hits are the new route-out fallback and interface
    fields in delegated-review-patch.md; existing prompt-orchestrator ownership
    in AGENTS.md and prompt-orchestration.md; existing delegated-review-patch
    non-machine-routable text in delegated-review-patch.md and review-lanes.md;
    and existing skill-adoption/source-of-truth text that protects external,
    user-level, plugin, and installed skill source from ordinary Orca work. No
    checked live surface instructed agents to hand-draft route-out prompts,
    force multi-file code diffs into delegated review-and-patch, or edit
    external reusable skill source in this Orca overlay turn.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane (the convention stays provisional)
    - not runtime model routing
    - not reusable skill-source deployment
```

## From .agents/workflow-overlay/artifact-folders.md

### Direction Change Propagation - Source Capture Armory Product Folder

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory product-doc folder convention is now bound in the overlay folder authority while existing controlling Data Capture source-access documents remain at their historical paths."
  trigger: output_authority
  controlling_sources_updated:
    - ".agents/workflow-overlay/artifact-folders.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/artifact-roles.md"
      reason: "The existing Product artifact role covers Source Capture Armory design notes and scoped specs; this patch binds folder routing, not a new artifact role."
    - path: "docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access boundary permission and hard stops did not change."
    - path: "docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Data Capture obligations did not change."
  stale_language_search: "rg -n \"source_capture_toolbox|Source Capture Armory\" .agents/workflow-overlay/artifact-folders.md docs/product/README.md docs/product/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation authorization"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment design"
```

### Direction Change Propagation - No-Case Smoke Tests Folder

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Judgment Harness v0.14 now has a narrow accepted folder for no-case
    smoke-test receipts and operator provenance records, with a permanent
    plumbing-only/non-gate-clearing boundary.
  trigger: output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/artifact-folders.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    - docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_adversarial_artifact_review_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/artifact-roles.md
      reason: >
        Existing Research artifact and Workflow record roles already cover the
        receipt/provenance distinction; this patch only binds a narrower folder.
    - path: docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
      reason: >
        The checklist already requires exact receipt/provenance paths and keeps
        smoke artifacts non-gate-clearing; no semantic update is required.
  stale_language_search: >
    rg -n "smoke_tests|no-case smoke|SMOKE_NOCASE_|gate-clearing|fixture admission|judgment-quality"
    .agents/workflow-overlay/artifact-folders.md
    docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
  non_claims:
    - not validation
    - not readiness
    - not live-call authorization
    - not fixture admission
    - not judgment-quality proof
```

## From .agents/workflow-overlay/prompt-orchestration.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca prompt authoring now has an explicit routing rule: all prompt, handoff,
    wrapper, rerun, and patch-prompt authoring must go through
    workflow-prompt-orchestrator (the prompt-orchestration owner that applies
    source-loading and the preflight/routing contract); hand-drafting any of them
    is a prompt-quality defect, and AGENTS.md now carries the up-front trigger
    pointing here.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - AGENTS.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/prompts/templates/_generic/
  intentionally_not_updated:
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names prompt-orchestration.md as the owner of
        prompt artifact, wrapper, preflight, and output-mode rules; the routing
        rule lives in that owner file and needs no index restatement.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its Prompt Orchestration Gates already defer to prompt-orchestration.md
        as the prompt-mechanics owner; single-source is preserved by adding the
        enforcement precondition in that owner file, not by duplicating it here.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        Its caution that workflow-prompt-orchestrator adoption needs a resolver
        recheck is unchanged and is explicitly preserved by the new rule's
        fallback clause; the routing default does not assert strict adoption.
    - path: .agents/workflow-overlay/template-registry.md
      reason: >
        It governs template-target retrieval, not prompt-authoring routing; the
        new rule does not change template fallback behavior.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; the only hit
        is an unrelated historical rg pattern in a prior receipt.
    - path: docs/prompts/templates/_generic/
      reason: >
        Model-target templates retired 2026-06-13 (unused; owner decision); no
        longer a live surface. Prior receipt preserved for history only.
  stale_language_search: >
    rg -i -n "prompt-orchestrator|hand-draft|hand-drafted|route through" .agents docs AGENTS.md
    (run 2026-06-09 on main @ cc93187 in the worktree)
  stale_language_search_result: >
    Executed 2026-06-09. No surface stated an opposing rule (no surface permits
    hand-drafting prompts or bypassing source-loading). Existing prompt-orchestrator
    hits are the binding, the Anti-Import adoption caution, the skill-adoption
    recheck note, template-target references, and an unrelated historical rg pattern
    in source-of-truth.md — none conflicts with or duplicates the new routing rule.
  non_claims:
    - not validation
    - not readiness
    - not a claim that workflow-prompt-orchestrator is an adopted or resolver-validated executable
    - not implementation authorization
    - not source promotion
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Model-target template retrieval retired (unused; no-runtime-model-routing
    rules retained and tightened); preflight defaults artifact
    (docs/prompts/templates/shared/orca_preflight_defaults_v0.md) blessed for
    referencing repo-constant preflight fields, with required per-prompt deltas
    still mandatory in every referencing prompt.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/review-lanes.md
    - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/artifact-roles.md
    - docs/prompts/templates/README.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        No model-target retrieval rule lives in AGENTS.md; the overlay-routing
        trigger is unchanged; no edit needed.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index names template-registry.md as the template owner;
        retirement lives there; no index restatement needed.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and propagation mechanics are unchanged; no model-target
        retrieval rule lives here.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        No model-target retrieval or _generic path referenced here; unaffected.
    - path: .agents/workflow-overlay/artifact-roles.md
      reason: >
        No model-target retrieval or _generic path referenced here; unaffected.
    - path: docs/prompts/templates/README.md
      reason: >
        Updated in 1e to remove _generic reference and note retirement; no
        further change needed.
  stale_language_search: >
    rg -i -n "generic-gpt|generic-claude|model-named template|template target" .agents docs AGENTS.md
    (run 2026-06-13 post-edit in worktree orca-template-retire-wt)
  stale_language_search_result: >
    Executed 2026-06-13. Live-overlay hits: template-registry.md and
    review-lanes.md and prompt-orchestration.md carry "template target" as
    allowed model-neutral terminology (prompt-shaping label, not routing) —
    these are the no-routing rules themselves, not stale doctrine.
    Non-live hits: docs/prompts/product-planning/ (1 hit — historical template
    basis note in a prior authored prompt, not a routing instruction);
    docs/research/judgment-spine/ (1 hit — research artifact with explicit
    "not a runtime model claim" disclaimer); docs/review-outputs/ (multiple
    hits — historical review records citing prior template IDs, archives only).
    No live-doctrine surface retains an instruction that routes agents to a
    model-target template or implies runtime model selection.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```

## From .agents/workflow-overlay/prompt-orchestration.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Prompt orchestration now surfaces the fitness_reference (goal + observable
    success signal, owned by work_unit_fitness_reference_v0) for durable and
    cross-recipient prompts in two places: the chat return for the dispatcher in
    plain language (human-glance test), and the prompt body for the receiving
    executor, pointer-preferred and labeled executor-target / review-axis-to-attack
    (not a review pass bar). This EXTENDS the surfacing of
    work_unit_fitness_reference_v0 beyond its review-only scope-lock; it reuses that
    object (no new vocabulary) and changes none of its substance — not the review
    back-pressure, the scoped fused gate, prompt_body_injection: no, or the
    alignment-axis guardrail.
  trigger: output_authority
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
  downstream_surfaces_checked:
    - docs/decisions/work_unit_fitness_reference_v0.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/validation-gates.md
    - AGENTS.md
  intentionally_not_updated:
    - path: docs/decisions/work_unit_fitness_reference_v0.md
      reason: >
        The owning decision is unchanged in substance; this overlay rule extends
        its surfacing and cites it as the concept owner. The decision's scope-lock
        (adversarial artifact review + fused gate) remains accurate for what it
        enacted; the extension lives in the overlay, not by re-opening the decision.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        Its review-side fitness_reference rule (pointer-preferred, axis-to-attack,
        name the gap when unbound) is unchanged and is explicitly preserved by the
        new rule's executor-target / not-a-pass-bar labeling.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        It owns the general chat shape; its Decision-criteria consumption item
        already accommodates a surfaced goal+signal. prompt-orchestration.md owns
        output-mode behavior and carries the new surfacing requirement, so no
        duplicate rule is added here.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its prompt gates defer to prompt-orchestration.md as the prompt-mechanics
        owner; the new surfacing rule lives there and needs no new gate.
    - path: AGENTS.md
      reason: >
        Routes prompt detail to prompt-orchestration.md; the rule lives in that
        owner file, so no root restatement is added.
  stale_language_search: >
    rg -i "fitness_reference|prompt_body_injection|success signal|fitness reference"
    .agents/workflow-overlay (run 2026-06-15 in worktree orch-goal-success @ cd681d9e)
  stale_language_search_result: >
    Executed 2026-06-15. Hits: prompt-orchestration.md (the goal-fitness gate, the
    review fitness_reference rule, review gate item g), review-lanes.md (the
    review-side fitness_reference rule), skill-adoption.md (the workflow-goal-framing
    skill entry). None states an opposing rule; all are consistent with extending
    the same object's surfacing. No surface forbids surfacing the fitness_reference
    in chat or carrying it pointer-preferred in a prompt body.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```


## From orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Storage Contract v0 now records the blocker-1 implementation-facing
    Attachment Record contract: compact manifest/index entries link to immutable,
    hash-checkable attachment bodies, while exact sidecar/member layout,
    serialization, manifest version, backend, migration, validation, readiness,
    and runtime implementation remain deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/review-lanes.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - orca/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/writer.py
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        It remains the parent logical contract and already defers exact field
        names and physical representation; the storage contract plus new
        implementation contract own the narrower blocker-1 physicalization
        direction without reopening core boundaries.
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
      reason: >
        It remains a planning-only mechanics map. Its broader physicalization
        gate stays stale-if-superseded by later storage/manifest/sidecar
        decisions, and this patch does not select those physical choices.
    - path: orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
      reason: >
        It remains the accepted logical typed-envelope boundary and explicitly
        defers physical storage. This patch records the storage-lane
        implementation contract without globally renaming historical envelope
        terminology.
  stale_language_search: >
    rg -n "table of contents|storage engine selected|sidecar selected|Manifest v2 selected|call ECR|call SCR|call Cleaning|call Projection|call Judgment|implementation readiness|runtime implementation closeout"
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-18 after edits. Hits are expected guardrails only: the
    new implementation contract rejects "table of contents" as architecture
    terminology and forbids the Availability Index from calling ECR, SCR,
    Cleaning, Projection, or Judgment; the storage contract states blocker 1 is
    not a runtime implementation closeout and contains the query in this
    receipt; the mechanics map hit is an older receipt non-claim against
    implementation readiness. No hit selects a backend, sidecar, Manifest v2,
    runtime implementation, validation, or readiness.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not Manifest v2 selection
    - not sidecar selection
    - not storage-engine selection
```

## From .agents/workflow-overlay/prompt-orchestration.md
```yaml
direction_change_propagation:
  doctrine_changed: >
    Operating Economy reform -- reduce no-value latency without losing any
    defect-catching friction. (1) AGENTS.md adds an "Operating Economy" section
    (act-default on reversible work; the "can I pick a defensible default and
    proceed?" test; the harness permission prompts / protected-action guard ARE
    the irreversibility gate, so no chat double-ask; surface a risky assumption
    [keep] != ask permission for a clear reversible action [cut]; load each skill
    once per thread; pre-build gates and precompact are triggered-only and
    precompact is a thin restore pointer) and refines the kernel "surface
    ambiguity" line accordingly. (2) The orchestrator mandate is NARROWED:
    routine prompts apply the new ~12-line "Orca Prompt Preflight" core inline
    (no skill reload); fused, delegated-review-patch, and novel/cross-lane prompts
    still author through the full workflow-prompt-orchestrator skill. The full
    Required Preflight Fields / Review Prompt Defaults / Output Modes obligations
    are unchanged -- the core is an additive fast-path, not a reduced obligation.
    (3) The existing docs/prompts/** PostToolUse hook (check_prompt_provenance.py,
    config-proposal P5) is evolved to INJECT the preflight core instead of a bare
    "use the orchestrator" pointer -- the real, agent-agnostic enforcement that
    replaces the invoke-ritual; its now-stale strong-mandate message is corrected
    to the narrowed two-depth routing.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  reviewed_by: >
    Cross-vendor delegated adversarial artifact review (non-Claude / GPT-family,
    provisional convention) run and CA-adjudicated 2026-06-19; findings AR-01
    (six-point core readable as the whole contract), AR-02 (routine/novel boundary
    self-classifying), AR-03 (irreversibility-gate wording overclaims for ungated
    hard-to-reverse actions), AR-04 (edit-permission enum inconsistent across
    surfaces) all accepted and folded in pre-merge. Decision input only, not a
    bound-lane verdict.
  controlling_sources_updated:
    - AGENTS.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/check_prompt_provenance.py
    - docs/workflows/orca_repo_map_v0.md     # Active Hooks note: faithful restatement of the evolved hook
    - docs/decisions/dcp_receipts_archive_v0.md  # receipt rotation target (older receipt moved here verbatim)
  downstream_surfaces_checked:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/skill-adoption.md
    - .claude/settings.json
    - .agents/hooks/remind_sci.py
  intentionally_not_updated:
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names prompt-orchestration.md as the prompt /
        preflight owner and AGENTS.md as the kernel; the preflight core and the
        Operating Economy section live in those owners, so no index restatement
        is needed.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; this change
        consumes that contract (receipt + rotation), it does not alter it.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its Prompt Orchestration Gates defer to prompt-orchestration.md as the
        prompt-mechanics owner and carry no "must author through the orchestrator"
        text (verified by grep); the narrowed two-depth routing lives in the owner
        file, so no gate text changes.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        Its Enforcement Placement pointer and Cynefin triggers are unchanged; the
        evolved hook is the same boundary substrate it already describes in
        principle, not a new gate.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        Its incomplete-commission route-out through workflow-prompt-orchestrator
        is exactly a "use the full skill" case under the narrowed routing --
        preserved, not stale; no edit.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        Its orchestrator references are adoption cautions, not the authoring
        mandate (verified by grep); unaffected by the narrowing.
    - path: .claude/settings.json
      reason: >
        The hook is evolved in place (same file, same PostToolUse Write|Edit
        wiring); no registration change, so settings.json is unchanged.
    - path: .agents/hooks/remind_sci.py
      reason: >
        Its _SCI_VERBATIM mirrors the AGENTS.md "Smallest Complete Intervention"
        section, which is untouched (only the kernel "surface ambiguity" line, the
        mandate line, and a new Operating Economy section change); the mirror stays
        in sync. Verified by selftest.
  stale_language_search: >
    rg -i -n "through.{0,40}workflow-prompt-orchestrator|never hand-draft|must be authored through"
    .agents docs AGENTS.md (run 2026-06-19 in worktree cranky-driscoll-c4e109)
  stale_language_search_result: >
    Executed 2026-06-19 post-edit. In scope (.agents, docs, AGENTS.md) every hit is
    reconciled: AGENTS.md and prompt-orchestration.md ("Author Through" +
    "Authoring-route precondition") now carry the narrowed two-depth routing
    (novel-case "author through the full skill"); the repo map "Active Hooks" note
    and check_prompt_provenance.py (docstring + the line recording that the prior
    strong-mandate message went stale) carry the corrected wording;
    prompt-orchestration.md's other hits are this receipt's own reason text and query
    string; and delegated-review-patch.md "Route the request through
    workflow-prompt-orchestrator" is the explicit full-skill route-out for an
    incomplete commission -- one of the "use the full skill" cases, consistent with
    the narrowing (not stale). No in-scope surface retains an unqualified "author
    every prompt through the orchestrator" mandate. A whole-repo sweep additionally
    finds restatements under orca/product/** (fragrance satellite, capture and
    commission-board artifacts) saying "author through the orchestrator"; these are
    product-lane artifacts, not doctrine-routing surfaces, and stay valid (the
    full-skill path is never wrong, only sometimes more than a routine prompt needs)
    -- reconciling them is out of scope for this kernel change.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```


```yaml
direction_change_propagation:
  doctrine_changed: >
    Durable and cross-recipient Orca prompts (review, handoff, commission,
    wrapper, rerun, patch — and any prompt handed to another model/agent/thread/
    worktree) must now be authored as a FILE-WRITE under docs/prompts/**, not
    chat-only; paste-ready-chat carries a copy of the filed body, not a substitute
    for filing. This retracts the previously-accepted limitation that the
    docs/prompts/** provenance hook (check_prompt_provenance.py) misses
    paste-ready-chat prompts that never touch disk: by requiring durable prompts
    to touch disk, the hook always fires and injects the preflight (incl. source
    pack / required reads + the Source-Gated Method Contract), so source-loading
    is enforced for every durable prompt. chat-only is reserved for trivial,
    single-target inline prompts.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/check_prompt_provenance.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .claude/settings.json
    - docs/decisions/dcp_receipts_archive_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The kernel routes prompt detail to prompt-orchestration.md; the filing
        rule lives in that owner file, so no root restatement is added.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its Authoring-route precondition already requires the prompt contract to
        have been applied at the correct depth; the filing rule is part of that
        contract in the owner file, so the gate needs no new text.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Owns the read-pack / orca_start_preflight the hook injects; this rule
        routes durable prompts through that preflight and changes nothing in the
        load-side owner.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        Owns the general chat shape; the paste-ready-chat output-mode tightening
        lives in prompt-orchestration.md (output-mode owner), so no duplicate here.
        Its chat-only hits are review/decision OUTPUT, not prompt authoring.
    - path: .agents/workflow-overlay/template-registry.md
      reason: >
        Lists paste-ready-chat as the delivery mode of FILED docs/prompts/templates/**
        templates; consistent with "filed artifact + paste copy." No mode removed.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        Its paste-ready-chat route-out is a cross-recipient prompt; under the new
        rule that is a filed artifact with paste-ready-chat as its copy — consistent.
        A one-line "filed + copy" clarification is optional, not required; flagged,
        not silently forked.
    - path: .claude/settings.json
      reason: >
        The hook wiring is unchanged (same PostToolUse Write|Edit registration);
        only the hook docstring note is updated to reflect the doctrinal closure.
    - path: docs/decisions/dcp_receipts_archive_v0.md
      reason: >
        Receipt-rotation target only — the prior 2026-06-15 fitness_reference
        receipt was moved there verbatim to keep this file at the
        two-most-recent-inline limit. Not a doctrine surface.
  stale_language_search: >
    rg -i "paste-ready-chat|never touch disk|chat-only|authored.{0,20}file-write"
    .agents/workflow-overlay AGENTS.md (run 2026-06-20)
  stale_language_search_result: >
    Executed 2026-06-20; the terms appear in 5 overlay files (not 1).
    prompt-orchestration.md carries the new filing rule + paste-ready-chat tightening
    (the change itself). communication-style.md uses chat-only for review/decision
    OUTPUT, not prompt authoring — consistent. template-registry.md lists
    paste-ready-chat as the delivery mode of FILED docs/prompts/templates/** templates
    — consistent with "filed + paste copy." validation-gates.md names the output-mode
    enum — consistent. delegated-review-patch.md specifies a paste-ready-chat route-out
    prompt: under the new rule a cross-recipient route-out is a filed artifact with
    paste-ready-chat as its copy — consistent, optional one-line clarification flagged
    (not silently forked). No live surface presents chat-only / paste-ready-without-a-file
    as an accepted authoring path for a durable or cross-recipient prompt.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```

```yaml
direction_change_propagation:
  change_id: subagent_validation_probe_timeout_2026_06_20
  trigger: workflow_authority | validation_philosophy
  changed_sources:
    - .agents/workflow-overlay/prompt-orchestration.md
  reason: >
    A delegated ontology-tagging lane repeatedly invoked a newly authored
    validation hook that hung during selftest and left background Python
    processes. The subagent contract needed an explicit smoke-timeout stop rule
    for new/custom validation surfaces before retry or completion claims.
  controlling_sources_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-of-truth.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        It already owns delegation routing and runtime-payload safety; the new
        rule is the prompt/dispatch execution contract for subagent validation
        probes, so it belongs in prompt-orchestration.md.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Known gate semantics and CI timeouts are unchanged. The new 30-second
        limit is a smoke-probe stop condition for newly introduced or materially
        changed validation commands, not a replacement gate timeout.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and propagation mechanics are unchanged; this receipt
        consumes the existing doctrine-change propagation contract.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```

```yaml
# archived from .agents/workflow-overlay/delegated-review-patch.md on 2026-06-30 by repo-access-default patch.
# delegated_code_review_and_patch sibling mode bound 2026-06-28 (CA decision).
direction_change_propagation:
  doctrine_changed: >
    The delegated review-and-patch convention now defines a delegated_code_review_and_patch
    sibling mode for bounded multi-file implementation/code diffs, replacing the prior flat
    exclusion (the 2026-06-16 "do not stretch this convention to a multi-file code diff" text,
    now rotated to the archive). The sibling mode keeps the code review lane (workflow-code-review,
    deep-thinking first, source-gated) as its review method -- NOT artifact review and not a merge
    of the two -- bounds the patch to an explicitly named multi-file set that cannot silently widen
    (everything outside it flag-only), names validation/test obligations that can fail, and keeps
    patch authority an explicit commission subordinate to the implementation-authorization boundary
    in safety-rules.md / AGENTS.md. All other convention machinery (commission, de-correlation /
    two-bar, repo/no_repo access-mode obligations, CA adjudication of the returned diff before keep,
    NEEDS_ARCHITECTURE_PASS, strict-claim boundary, no runtime-model recommendation) is inherited
    unchanged. Legitimizes the shape practice already ran as a disclosed per-commission deviation
    (e.g. docs/prompts/reviews/source_capture_lenient_read_slice_delegated_adversarial_code_review_and_patch_prompt_v0.md).
  trigger: review_authority
  related_triggers: [workflow_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/review-lanes.md          # lane-index summary line de-narrowed to name the code-diff sibling mode
    - docs/workflows/orca_repo_map_v0.md                # repo-map index line de-narrowed likewise
  receipt_storage_updated:
    - docs/decisions/dcp_receipts_archive_v0.md          # 2026-06-13 and 2026-06-16 receipts rotated here verbatim
  downstream_surfaces_checked:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      note: >
        "delegated-review-patch ... author through the full skill" routing is target-kind-agnostic;
        a delegated_code_review_and_patch prompt is still a delegated-review-patch prompt routed
        through the full skill, and Review Prompt Defaults already own the code-review method
        (deep-thinking first, source-gated) the sibling mode points to. No edit.
    - path: .agents/workflow-overlay/safety-rules.md
      note: >
        Already requires explicit bounded authorization for implementation/source-changing work;
        the sibling mode defers to that boundary (the commission IS the authorization) and grants
        no standing code-patch authority. Unchanged.
    - path: .agents/workflow-overlay/artifact-roles.md
      note: >
        "reviewers are read-only unless explicitly assigned patch execution" stays true; the
        commission is exactly that explicit assignment. Unchanged.
    - path: .agents/workflow-overlay/skill-adoption.md
      note: >
        Its workflow-delegated-review-patch row ("bounded de-correlated review-and-patch hardening
        pass") is target-kind-agnostic and stays accurate. Unchanged.
    - path: .agents/workflow-overlay/review-lanes.md
      note: >
        "implementation/code review and artifact review remain separate lanes" stays true -- the
        sibling mode USES the code review lane as its review method, it does not merge the lanes;
        two-bar de-correlation and reviewed_by/authored_by provenance already cover code review.
    - path: AGENTS.md
      note: routes delegated review-and-patch to the owning overlay file; no root restatement (a fork). Unchanged.
  stale_language_search: >
    rg -ni "multi-file|implementation/code|code diff|delegated_code_review|patch execution|source-read-only"
    .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md AGENTS.md
  stale_language_search_result: >
    Executed 2026-06-28. The prior flat exclusion in delegated-review-patch.md is replaced by the
    sibling-mode route; the interface non_eligible_target_boundary is replaced by
    code_diff_target_routing + target_kinds. review-lanes.md line ~29 and repo-map line ~497
    narrowing phrase ("high-stakes authored artifacts") now name the code-diff sibling mode. The
    2026-06-16 receipt's exclusion sentence ("multi-file ... routed to the appropriate review prompt
    instead of being stretched into this convention") was the only inline contradiction; it has been
    rotated verbatim to docs/decisions/dcp_receipts_archive_v0.md as superseded history, not left
    inline. "reviewers are read-only unless explicitly assigned patch execution" (artifact-roles.md,
    review-lanes.md) and "implementation/code review and artifact review remain separate lanes"
    (review-lanes.md) are unchanged and consistent -- the sibling mode commissions patch execution
    explicitly and uses the code review lane as its method. No live surface still presents multi-file
    code diffs as categorically ineligible for the convention.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane (the convention stays provisional)
    - not runtime model routing
    - not standing implementation/code-patch authorization (per-commission only)
```
## From orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Silver Vault v4.1 now explicitly clarifies Creator Vault generated read-model
    placement and sync semantics: account/content envelopes stay sibling read
    homes, TikTok/Youtube/Instagram path examples are read-model keys only,
    acknowledgement refs remain lane receipts/manifests rather than envelope
    authority, relationship/source-ref examples are concrete for future
    read-model scoping, and client carveout replicas/exports are generated from
    Silver records and read-model manifests rather than separate capture sources
    by default.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - orca-harness/data_lake/root.py
    - orca-harness/tests/test_data_lake_root.py
    - docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_root_epoch_mixed_artifact_code_review_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
      reason: >
        Already owns only the generic v4.1 folder grammar and states Creator
        Vault is generated/non-authoritative; platform examples and carveout sync
        belong in the Silver Vault record/read-model contract.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
      reason: >
        Owns physical slot invariants and does not enumerate Creator Vault
        platform keys or client-replica semantics.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        Owns derived/ack addressing and rebuildability; this patch uses that
        boundary without changing addressing or opening new derived_retrieval
        view classes.
    - path: orca-harness/data_lake/root.py
      reason: >
        Runtime already creates only the generic Creator Vault account/content
        homes; no platform-specific folders, builder code, runner changes, or
        live data-root mutation are authorized by this contract clarification.
    - path: orca-harness/tests/test_data_lake_root.py
      reason: >
        Existing tests verify the generic skeleton from LAKE_SUBDIRECTORIES; no
        runtime path list changed.
  stale_language_search: >
    rg -n "Creator Vault|creator_vault|carveout|replica|acknowledgement|tiktok|TikTok"
    orca/product/spines/data_lake/authority orca-harness/data_lake/root.py
    orca-harness/tests/test_data_lake_root.py
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not runner PR work
    - not client replica implementation
    - not live external data-root mutation
```

## From .agents/workflow-overlay/source-loading.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Spine read packs (Data Capture Spine CA, Data Capture Intake Surface / MSP
    Pressure-Test Target, Judgment Spine Evidence Ladder) reshaped to
    front-door pointer form matching the ECR pack model: each pack now leads
    with its retrieval_only front-door submap and routes to owner docs on
    demand. Embedded spine state (slot-by-slot pressure-test authorization-chain
    walk, CloakBrowser selection, Reddit ordering, RQ status) relocated verbatim
    to the spine-owned closeout synthesis. Source-loading.md is navigation only;
    state of the work lives in the spine-owned doc it belongs to.
  trigger: workflow_authority
  related_triggers:
    - architecture_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/source-loading.md
    - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_closeout_synthesis_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/README.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt orchestration binds source-loading as the read-pack authority and
        points here; it does not reproduce pack contents. The front-door reshape
        does not change the binding rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names source-loading.md as the read-pack owner.
        No section owner or overlay path changed.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map already points to the section anchors
        (source-loading.md#data-capture-intake-surface--msp-pressure-test-target-pack
        etc.) and does not reproduce pack contents. Section headings are
        unchanged so existing anchors remain valid.
    - path: docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
      reason: >
        The Judgment Spine consolidation map is the front door this pack now
        points to; it is not a downstream consumer of pack contents. No changes
        needed there.
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      reason: >
        The Data Capture Spine consolidation map is the front door this pack now
        points to; it is not a downstream consumer of pack contents. No changes
        needed there.
  stale_language_search: >
    rg -n "MSP|pressure-test|read pack" .agents/workflow-overlay/
  stale_language_search_result: >
    Executed 2026-06-13 after edits. Hits in .agents/workflow-overlay/:
    artifact-folders.md:197 ("read packs reference unchanged paths until
    Phase-2 apply" — DCP receipt comment, not stale); README.md:19 ("read
    packs, and context-bloat controls" — description of source-loading.md,
    accurate); source-loading.md — section title "Data Capture Intake Surface /
    MSP Pressure-Test Target Pack" (correct, kept), "pressure-test" in navigation
    text (correct nav context, not state prose), "read pack" in capsule-limit
    prose and Expansion Rules (both accurate descriptions of navigation artifacts,
    not stale); source-of-truth.md — references to source-loading.md description
    (accurate). No hit retained the inline authorization-chain state narrative
    or bulk file-list in source-loading.md; none points to a stale-language
    conflict requiring a further fix.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
    - not ECR or Judgment design
```

## From orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Capture now interprets scanning/CSB recency-currentness as preservation
    urgency and source-drift risk, not proof or route binding: same-strength
    newer/current source states may deserve earlier capture when the request is
    otherwise in scope and route-matched.
  trigger: product_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
    - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
    - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    - orca/product/spines/scanning/README.md
    - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  intentionally_not_updated:
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      reason: >
        The submap remains a pointer surface and already routes capture-method
        questions to this playbook; no route ownership changed.
    - path: orca/product/spines/capture/core/source_capture_toolbox/README.md
      reason: >
        The Source Capture Armory index already points operators to this playbook
        for method routing; duplicating recency semantics there would create a
        second wording surface.
  stale_language_search: >
    rg -n "recency|recent|current-state|currentness|preservation urgency|route binding|proof|access-control gate"
    orca/product/spines/capture orca/product/spines/scanning docs/workflows/data_capture_spine_consolidation_map_v0.md docs/workflows/orca_repo_map_v0.md
    (run 2026-06-23)
  stale_language_search_result: >
    Hits were accepted recency/currentness preservation-priority language,
    repo-map routing summaries, existing capture/scanning safeguards, harvested
    historical source text, or explicit no-proof/no-route-binding/no-access-gate
    boundaries. No controlling Capture/scanning surface was found that lets
    recency/currentness prove demand, authorize access, or bind a Capture route.
  non_claims:
    - not validation
    - not readiness
    - not capture authorization
    - not source-access authorization
    - not buyer proof
```

## From .agents/workflow-overlay/delegated-review-patch.md

```yaml
# repo-access default and clean-adjudication next-moves hardening 2026-06-30 (CA decision).
direction_change_propagation:
  doctrine_changed: >
    Delegated review-and-patch commissions now bind repo as the default access
    mode. no_repo is selected only by an explicit commission value plus a reason
    repository access is unavailable or intentionally excluded; cross-vendor,
    external, couriered, paste-ready-chat, or portable-method dispatch does not
    imply repo-blindness. Review-return adjudication is also tightened: the CA
    adjudicates findings/diff/verdict/residuals first; if a material issue
    remains, the next step is closure for that issue; only after a clean
    adjudication does admin collapse into exactly one land step and material
    next moves receive deep thinking.
  trigger: review_authority
  related_triggers: [workflow_authority, output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/template-registry.md
    - docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md
    - docs/prompts/templates/review/delegated_review_return_adjudication_v0.md
    - docs/prompts/reviews/ontology_commission_refresh_delegated_review_patch_prompt_v0.md
    - docs/prompts/reviews/ontology_backbone_architecture_delegated_review_prompt_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - path: .agents/workflow-overlay/review-lanes.md
      note: >
        Review-lane model-neutrality, findings-first defaults, provenance fields,
        and CA consumption order stay intact; the access default and adjudication
        tail are delegated-review/prompt mechanics, not lane authority changes.
    - path: AGENTS.md
      note: >
        Already routes delegated-review-patch, prompt artifacts, review lanes, and
        doctrine-changing work to the owning overlay/prompt sources; no root
        restatement added.
    - path: docs/workflows/orca_repo_map_v0.md
      note: >
        Existing index lines still route delegated-review-patch and prompt
        orchestration to the owning overlay files; no new top-level source folder
        or lifecycle boundary was introduced.
  receipt_storage_updated:
    - docs/decisions/dcp_receipts_archive_v0.md
  stale_language_search: >
    rg --hidden --glob '!worktrees/**' --glob '!.git/**' --glob '!docs/review-inputs/**' -n
    "no_repo[^\n]{0,80}(default|expected)|expected dispatch|repo-blind cross-vendor|cross-family / external / no-repo|repo-agnostic / cross-family|The reviewer needs nothing else -- no repo|The reviewer needs nothing else — no repo"
    .agents docs AGENTS.md
  stale_language_search_result: >
    Executed 2026-06-30 after patch and rechecked after the delegated review
    report was written. No live prompt, template, or overlay surface still
    defaults delegated review-and-patch to no_repo or treats cross-vendor,
    external, couriered, paste-ready, or portable delivery as repo-blind by
    default. Remaining hits are only quoted stale-search literals in this receipt
    and the delegated review-patch commission prompt, archived DCP history in
    docs/decisions/dcp_receipts_archive_v0.md, and review-output notes under
    docs/review-outputs/ including the current delegated review report.
  non_claims:
    - not validation
    - not readiness
    - not a bound/mandatory/machine-routable review lane
    - not runtime model routing
    - not standing implementation/code-patch authorization
```

## From .agents/workflow-overlay/source-loading.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Source-loading now binds the canonical capture-method playbook
    (source_capture_playbook_v0.md + its open_next recon-index) as a required start-read for
    capture-spine activity, and points scanning/screening activity at the screening-side Walker
    Equipment Kit (escalating to the playbook only for packet-grade capture). Previously the
    playbook was canonical but referenced by no overlay surface and reachable only one hop from a
    pack — not an auto-load start-read.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/source-loading.md
  downstream_surfaces_checked:
    - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
      reason: >
        It is the target being bound and is already canonical; no content change is needed to make
        it a start-read.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map already routes to the playbook / recon-index; adding a source-loading
        start-read does not change the map's pointers.
  stale_language_search: >
    rg -n "capture_investigation_playbook|source_capture_playbook" .agents/workflow-overlay/
  stale_language_search_result: >
    Executed 2026-06-14 in the worktree. No matches in .agents/workflow-overlay/ — the overlay
    referenced neither the canonical nor the retired playbook name before this edit, so this adds
    the first overlay binding and there is no stale retired-name reference to repoint.
  non_claims:
    - not validation
    - not readiness
    - not authorization to capture, build, or run (the playbook stays non-authorizing doctrine;
      per-probe network approval still required)
```

## From .agents/workflow-overlay/validation-gates.md

The first archived receipt below concerns the US-parameterized Google
search-surface route; as that route decision states, parameterized US
capture is US-parameterized only, not physically US-local.

```yaml
direction_change_propagation:
  doctrine_changed: >
    Google search-surface route-shape enforcement is now an active validation-gate
    instance: a diff-scoped CI checker plus advisory PostToolUse hooks enforce
    the mechanically checkable shell of the parameterized Google route decision
    while preserving the non-claim that passing shape is not physical-locality,
    source-sufficiency, validation, readiness, demand, Judgment, or Product Lead
    proof.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md
    - .agents/hooks/check_search_surface_google_route.py
    - .claude/settings.json
    - .codex/hooks.json
    - .github/workflows/ci.yml
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/README.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes validation and enforcement-placement changes to
        the overlay. Adding a Google-specific route rule to the behavior kernel
        would create a narrower duplicate source.
    - path: .agents/workflow-overlay/README.md
      reason: >
        README already points project work to validation-gates, prompt
        orchestration, and source-of-truth. The active instance is recorded here
        and in the repo map/hook README.
  stale_language_search: >
    rg -n "Google search-surface|US-parameterized|physical-locality|check_search_surface_google_route"
    .agents docs orca
  non_claims:
    - not validation
    - not readiness
    - not source sufficiency
    - not demand proof
    - not Judgment evidence
    - not Product Lead evidence
    - not physical-locality proof
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca validation doctrine now includes a receipt-field provenance
    (non-self-certification) gate: a check, predicate, acceptance, or completion
    claim must not clear on a self-asserted field value; clearing requires an
    owner-produced, provenance-bound, or independently verifiable value, else the
    check is indeterminate_until_authored.
  trigger: validation_philosophy
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
  intentionally_not_updated:
    - path: external workflow source and plugin skill source
      reason: >
        Deliberately Orca-only. jb already carries equivalent discipline
        (source-authority ceilings, no-fake-fallback, "user-confirmed is not
        verified"), so there is nothing to spread now. This rule is a candidate
        for external promotion later, which is a separate governed skill-source
        change, not an Orca-lane edit.
    - path: jb project sources
      reason: >
        Out of scope and already covered by jb's own evidence/claim discipline;
        Orca must not edit jb authority.
    - path: orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md and the JS gate/owner-contract docs
      reason: >
        They already encode this discipline for Judgment Spine gates (e.g., the
        no-tools contract Receipt Provenance Boundary). This overlay gate
        generalizes it without restating their semantics.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        No duplicate rule added. validation-gates.md is overlay and already read
        by every Orca agent, so the gate reaches review and authoring without a
        pointer; single-source preserved.
  stale_language_search: >
    rg -n "self-asserted|self-certif|provenance|indeterminate_until_authored|verifiable"
    .agents/workflow-overlay/validation-gates.md
  stale_language_search_result: >
    Executed on 2026-06-03 after adding the gate. The terms appear only in the
    new Current Gates bullet and this receipt; no conflicting or duplicate rule
    exists elsewhere in the file, and no prior language stated that a
    self-asserted field is sufficient to clear a gate. No hit converted the gate
    into a validation, readiness, PASS, acceptance, or judgment-quality claim.
  non_claims:
    - not validation
    - not readiness
    - the gate's existence does not prove it is enforced or that any artifact passes it
    - not a kernel or jb change
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    New forward-only CI gate: changed durable docs must carry a retrieval header
    and be map-reachable (substring-present in repo map or any submap); whole-repo
    backlog surfaced advisory-only via --health + the session capsule.
  trigger: validation_philosophy
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/header_index.py
    - .github/workflows/ci.yml
    - .agents/hooks/session_context_capsule.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/check_retrieval_header.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md triggers overlay-load for validation gates; the gate is
        registered in validation-gates.md which AGENTS.md already routes to.
        No new trigger word is needed.
    - path: .agents/workflow-overlay/README.md
      reason: >
        README routes to validation-gates.md. The new gate is registered there;
        no new overlay-level pointer needed.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading packs are unchanged; the new hook is a CI substrate, not
        a source-loading artifact or context-budget item.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map's Active Hooks section already documents the pattern;
        this DCP receipt is in validation-gates.md (the enforcement-placement
        authority). A separate map entry is deferred as a hygiene-level note,
        not a DCP-required propagation.
    - path: .agents/hooks/check_retrieval_header.py
      reason: >
        check_retrieval_header.py is unchanged; header_index.py imports from it
        without modification. Its own selftest continues to pass.
  stale_language_search: >
    rg -i -n "retrieval header|header_index|missing header" .agents
  stale_language_search_result: >
    Executed 2026-06-13 after adding header_index.py. Hits are in:
    check_map_links.py (retrieval header mention, unrelated), check_retrieval_header.py
    (canonical source, unchanged), header_index.py (new file, expected),
    session_context_capsule.py (new capsule line, expected), README.md (hook table),
    prompt-orchestration.md and retrieval-metadata.md (authority docs, unchanged),
    source-loading.md (use_when reference, unchanged). No pre-existing stale
    language; no checked surface required a new CA to block the gate or omit the
    header requirement.
  non_claims:
    - not validation
    - not readiness
    - the gate's existence does not prove any artifact passes it
    - not a kernel or jb change
    - --strict passing for a PR does not prove the whole repo is header-complete
```

## From orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Storage Contract v0 now records the blocker-2 incumbent-field
    direction: existing direct packet/slice fields remain legacy-readable and
    transitional, are not precedent for new direct source-family fields, are not
    promoted to universal lake core, and may only move through future dual-read
    or replay under separate authorization; pinned packets are not mutated.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/capture/core/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/writer.py
    - orca-harness/source_capture/ig_projection.py
    - orca-harness/source_capture/retail_pdp_projection.py
  intentionally_not_updated:
    - path: orca-harness/source_capture/models.py and writer/projection code
      reason: >
        This patch records architecture direction only. Existing fields and
        readers remain live and readable; no runtime migration, dual-read
        implementation, replay implementation, or schema mutation is authorized.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
      reason: >
        It already defers the migration/replay plan for incumbent direct fields.
        This patch settles the high-level fate in the storage/core/boundary
        sources without choosing dual-read mechanics or replay triggers.
  stale_language_search: >
    rg -n "Decide the fate of incumbent direct fields|Before physicalization, the incumbent field fate must be decided|Whether current `metric_observations` remain|Whether demand pins remain|migrate incumbent fields|legacy-readable transitional|future dual-read or replay"
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-18 after edits. No live target text still says incumbent
    direct-field fate must be decided, nor that current metric observations or
    demand pins have an open high-level fate. Hits are expected: the storage,
    core, mechanics map, attachment-boundary, and repo-map text now state the
    accepted legacy-readable / future-dual-read-or-replay direction; the storage
    contract keeps "migrate incumbent fields" only as a non-goal; this receipt
    contains the query. No hit authorizes migration, schema finalization,
    runtime implementation, validation, readiness, or storage-engine selection.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not migration authorization
    - not schema finalization
    - not storage-engine selection
```

## From docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has a developer-workflow doctrine: CI runs the orca-harness test suite on every PR and
    push to main (live), behind a per-lane PR off main with a squash default and a rebase cadence.
    The server-side hard merge gate (branch protection / rulesets) and auto-merge are the deferred
    target — blocked on this private+free repo (HTTP 403) — so interim enforcement is a
    merge-when-green discipline until a GitHub Pro/Team upgrade or public visibility unblocks the gate.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Its rule "do not commit, push, configure remotes, or create pull requests unless explicitly
        authorized" is unchanged. This doctrine defines the merge gate and flow for when a lane is
        authorized; it does not grant standing commit/push/PR authority.
    - path: AGENTS.md
      reason: >
        The behavior kernel and authorization boundaries are unchanged; this is a decision record,
        not a kernel rule, and AGENTS.md already routes durable doctrine into docs/decisions and the
        overlay.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map is clean on main but carries uncommitted edits in the concurrent ecr lane;
        adding a pointer now would create a cross-lane merge conflict. The record lives in the
        canonical docs/decisions/ folder and is discoverable there. A one-line pointer can be added
        in a later turn once the repo-map lane settles.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; this record is a downstream
        decision, not an overlay-authority or hierarchy change. The same cross-lane-dirty caution as
        the repo map applies to its Known Source Documents list.
  stale_language_search: >
    rg -i -n "branch protection|github/workflows|github actions|required status check|auto.?merge|merge gate|continuous integration|enforce_admins|ci\.yml|status check"
    .agents docs   (run against main's content in the worktree before first landing this record)
  stale_language_search_result: >
    Executed 2026-06-09. No prior CI, GitHub Actions, branch-protection, required-status-check,
    auto-merge, or merge-gate doctrine exists in .agents/ or docs/. The only two hits are unrelated:
    a "status check" cell in a fixture-receipt review table and a "status checks" mention meaning
    `git status` in orca_bootstrap_record.md. This confirms the record is additive and forks no
    existing rule. The 2026-06-09 amendment corrects only this record's own enforcement statements
    and adds no doctrine vocabulary that conflicts with another surface.
  non_claims:
    - not validation
    - not readiness
    - not product, runtime, or judgment-quality readiness
    - not deployment
    - not blanket commit/push/PR authorization
    - the interim discipline is not a server-enforced gate
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The merge-when-green interim is amended to structure B: agents prepare green PRs but do not
    self-merge to main; a human or otherwise authorized action lands to main, now enforced by the
    enforcement lane's protected-action guard (it blocks an agent's gh pr merge -> main and allows a
    benign lane-branch push). This supersedes the prior "a solo lane self-merges once CI is green"
    wording, and re-scopes .github/scripts/merge-when-green.ps1 as the human's check-then-merge tool,
    not an agent self-merge path.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/scripts/merge-when-green.ps1
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - .agents/workflow-overlay/safety-rules.md
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The guard is the enforcement lane's surface (frozen, cross-lane). That lane built the
        structure-B re-target; this doctrine records and relies on it, and does not edit it.
    - path: docs/decisions/overlay_enforcement_placement_classification_v0.md
      reason: >
        The enforcement lane owns and updates the EP classification record for the guard; this
        doctrine references the guard's behavior, it does not edit that record.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Its "do not push/merge unless authorized" rule is unchanged; structure B is the concrete
        enforcement of it for main, and the guard cites safety-rules as its authority.
    - path: AGENTS.md
      reason: >
        The lane-isolation trigger (PR #9) and behavior kernel are unchanged; the who-merges change
        lives in this decision record, not the kernel.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; this is a downstream decision
        amendment (and the file is coordination-frozen this turn regardless).
  stale_language_search: >
    rg -i -n "self-merge|self-merges|lane .*merges|merge-when-green|gh pr merge"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md .github/scripts/merge-when-green.ps1
    (run 2026-06-09 in the doctrine-structure-b worktree)
  stale_language_search_result: >
    Executed 2026-06-09. Remaining "self-merge" mentions are the now-explicitly-superseded item 2
    server-gated-target note and this receipt; item 7 and the helper are re-scoped to human-landed.
    No surface still asserts agents self-merge to main as the live interim.
  non_claims:
    - not validation
    - not readiness
    - not an edit to the enforcement lane's guard or its classification record
    - not a claim that the guard is bug-free or that every merge passed CI
    - structure B is a guard-enforced interim, not the deferred server-side gate
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds the lane-isolation integrity mechanism (Decision item 8): lane isolation is a judgment rule,
    so its integrity is maintained by early detection — a read-only detector,
    .github/scripts/lane-health-check.ps1 (PR #11), that flags uncommitted pile-up on a shared base,
    worktree sprawl, and machine-local enforcement (a .agents/hooks/*.py present locally but not
    tracked on origin/main). Detection was chosen over a hard SessionStart reminder; the detector is a
    nudge, not a gate.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .github/scripts/lane-health-check.ps1
    - AGENTS.md
    - .agents/hooks/guard_protected_actions.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The lane-isolation rule (PR #9) is unchanged; item 8 records the integrity mechanism for that
        rule, not a new or altered kernel rule.
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        Cross-lane, frozen. The detector only observes whether enforcement hooks are tracked on main;
        it does not edit the guard. The guard's own on-main durability is a separate flag already
        raised to the enforcement lane.
  stale_language_search: >
    rg -i -n "lane.?isolation|SessionStart|machine-local|early.detection|health.?check"
    docs AGENTS.md .agents   (run 2026-06-09 in the doctrine-lane-isolation worktree off main @ 583d4f0)
  stale_language_search_result: >
    Executed 2026-06-09. Additive — no surface asserts a lane-isolation integrity mechanism or a
    SessionStart reminder that item 8 would contradict. The only doctrine hit is the prior receipt's
    note that the lane-isolation trigger (PR #9) is unchanged, which item 8 is consistent with. Other
    hits are unrelated (a jb skills inventory in orca_bootstrap_record.md, and the workflow-health-check
    kernel skill in skill-adoption.md).
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the detector is a nudge, not a gate, and not a guarantee of lane hygiene
    - not an edit to the enforcement lane's guard or its on-main durability
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    States the structure-B guard's liveness boundary in Decision item 7 and the Status interim bullet:
    guard enforcement is currently machine-local — the guard and its .claude/settings.json PreToolUse
    registration are not tracked on origin/main, so a fresh clone, another machine, or CI is not yet
    protected. Durable-on-main is the target, pending the guard + its registration landing via the
    coordinator's hooks-cluster PR (a human lands it; the guard blocks an agent from merging its own
    PR). On landing, EP-03 git-lifecycle merge protection becomes durable on every clone while EP-01
    external-path protection stays per-machine. This is the enforcement lane's answer to the
    lane-health detector's machine-local flag: A (durable-on-main) is the target, B (machine-local) is
    the honest interim.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .claude/settings.json
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        Cross-lane, frozen, verified correct (selftest 32/32). Landing it on main is the coordinator's
        hooks-cluster PR, not this doctrine edit; a human lands it because the guard blocks an agent
        from merging its own PR.
    - path: .claude/settings.json
      reason: >
        Coordinator-owned and frozen; origin/main carries no PreToolUse registration. Its landing
        rides the same coordinated hooks-cluster PR.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Per the enforcement lane, its "Active Hooks" note has the same not-on-main incoherence for the
        retrieval-header hook; that is the repo-map / hook owners' fix, flagged not edited here.
  stale_language_search: >
    rg -i -n "enforc" docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-09 in the doctrine-lane-isolation worktree)
  stale_language_search_result: >
    Executed 2026-06-09. Both live "enforced" claims — the Status interim bullet and Decision item 7 —
    now carry the machine-local liveness boundary. The remaining hits are the Enforcement-status
    section, the server-enforced-gate non-claims, and the historical DCP receipts (which accurately
    record prior changes); none present structure-B guard enforcement as durable on main while the
    guard is untracked there.
  non_claims:
    - not validation, readiness, or acceptance
    - structure-B guard enforcement is machine-local until the guard lands on main; this records the
      boundary, it does not land the guard
    - not an edit to the enforcement lane's guard, the coordinator's settings.json, or the repo map
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Flips the structure-B guard liveness from machine-local interim (prior receipt) to DURABLE on main:
    the guard and its .claude/settings.json PreToolUse registration landed via PR #15 and are verified
    tracked + registered on origin/main, so a fresh clone is protected. This supersedes the "currently
    machine-local / durable-on-main is the target, pending" framing in Decision item 7, the Status
    interim bullet, and the prior boundary receipt. EP-03 git-lifecycle merge protection is durable on
    every clone; EP-01 external-path protection stays per-machine. Closes the lane-health detector's
    machine-local flag (Option A landed).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .claude/settings.json
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        On main now (via PR #15, enforcement-lane-owned); this records its durable status, it does not
        edit the guard.
    - path: .claude/settings.json
      reason: >
        On main now (via PR #15, coordinator-owned); its guard registration is verified present, not
        edited here.
  verification: >
    Observed 2026-06-09 before the flip: git ls-tree origin/main lists
    .agents/hooks/guard_protected_actions.py, and origin/main:.claude/settings.json registers
    "python .agents/hooks/guard_protected_actions.py" - so a fresh clone carries both the script and
    its registration.
  stale_language_search: >
    rg -i -n "machine-local|not yet|pending|interim|Liveness|durable"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-09 in the doctrine-flip-durable worktree)
  stale_language_search_result: >
    Executed 2026-06-09. The two live guard-liveness claims (Status bullet, Decision item 7) now read
    "durable on main." Remaining interim/machine-local hits are: the structure-B-vs-server-gate
    "interim" (still accurate - structure B remains the interim until the 403-blocked server gate), the
    detector's check-name in item 8, and the historical DCP receipts (which record prior states). No
    live surface still claims the guard is machine-local.
  non_claims:
    - not validation or readiness of any lane's content
    - EP-01 external-path protection is per-machine, not durable-on-main
    - the other two cluster hooks (retrieval-header, repo-map-freshness) landed with the guard for
      registration coherence; their correctness is their owners' concern, not asserted here
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Scopes the structure-B "durable on main" claim in Decision item 7 to its actual reach: the guard is
    a Claude-Code-specific .claude/settings.json PreToolUse hook (matcher = Claude Code tool names), so
    "a fresh clone is protected" holds for Claude Code sessions only. A non-Claude-Code harness (e.g.
    Codex) is not guard-blocked until the same scripts are wired into its own config; the
    harness-agnostic, unbypassable gate remains the deferred server-side branch protection. Corrects a
    potential overstatement (the durable flip read as harness-agnostic).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .claude/settings.json
    - .agents/hooks/guard_protected_actions.py
  intentionally_not_updated:
    - path: .claude/settings.json
      reason: >
        The Claude-Code wiring is correct and on main; this records its harness scope, it does not
        change the registration. Wiring other harnesses is per-harness work.
  verification: >
    origin/main:.claude/settings.json registers the guard under hooks.PreToolUse with matcher
    "Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit" - Claude Code tool names - confirming the
    enforcement is Claude-Code-scoped as wired.
  non_claims:
    - not validation or readiness
    - does not claim any non-Claude-Code harness is protected; states the opposite until wired
    - the harness-agnostic gate (server-side branch protection) remains deferred / 403-blocked
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Relaxes structure B to structure B' (owner-ratified 2026-06-12): an agent MAY self-merge its own
    PR via a direct `gh pr merge <N>`, but ONLY when the protected-action guard confirms the PR is
    mergeStateStatus == CLEAN, every CI check has completed green, and it carries the opt-in
    `agent-automerge` label. Every other state, the no-arg/ambiguous form, the `gh api .../merge`
    form, a foreign `--repo`, or any lookup error/timeout FAILS CLOSED to a human merge, and the guard
    prints the repo-scoped manual command. This supersedes the prior structure-B "agents do not
    self-merge; a human lands every merge" wording and acts on the 2026-06-09 owner flag in the EP
    classification record ("if you intend agent self-merge-when-green, relax the gh pr merge block").
    The bar is CLEAN + green + label (not bare CLEAN) because, with branch protection 403-blocked, no
    check is required and an empty/early check set can read CLEAN before CI starts; the rollup-green +
    label requirements close that false-green race. EP-01 protected paths and EP-03 push-to-main /
    force-push / destructive-clean are UNCHANGED. The guard stays Claude-Code-scoped; the
    harness-agnostic server-side gate remains the deferred end-state.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .agents/hooks/guard_protected_actions.py
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  downstream_surfaces_checked:
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - .claude/settings.json
    - .github/scripts/merge-when-green.ps1
    - .github/scripts/lane-health-check.ps1
  intentionally_not_updated:
    - path: .claude/settings.json
      reason: >
        The guard's PreToolUse registration and matcher are unchanged; the behavior change is wholly
        inside the guard script. The `ask` rule `Bash/PowerShell(gh pr*)` is left in place as an
        interactive-mode belt-and-suspenders (the human is still prompted in interactive mode; the
        guard is the auto-mode enforcement). The `git commit` ask->allow owner hand-edit is a separate
        classifier-bound change, not this lane's.
    - path: .github/scripts/merge-when-green.ps1
      reason: >
        Still the human's check-then-merge tool; re-scoped in item 7 prose (it wraps `gh pr merge`
        inside a script subprocess the PreToolUse guard does not see, so agents must not use it to
        self-merge), but its content is unchanged.
    - path: .github/scripts/lane-health-check.ps1
      reason: >
        The machine-local-enforcement detector is unaffected; the guard remains tracked on origin/main.
    - path: docs/decisions/overlay_enforcement_placement_classification_v0.md
      reason: >
        The enforcement lane owns the guard's EP record and records this guard change there directly
        (see its 2026-06-12 Update section); this doctrine references that record rather than the
        reverse. (Listed here as a checked downstream surface, not unchanged — it IS updated, in its
        own lane section.)
  verification: >
    Guard `--selftest` 46/46 PASS, exit 0 (CLEAN+green+label -> allow; no-label / non-CLEAN / pending /
    empty-checkset / BLOCKED / unknown-PR / lookup-raises / no-number / gh-api-form / foreign-repo ->
    block; merge-allowed + push-to-main -> block; all pre-existing EP-01 and EP-03 push/force/
    destructive/benign cases unchanged). Live payload render: `gh pr merge` (no number) and the gh-api
    form both exit 2 with the repo-scoped manual command in stderr; `git status` exits 0. CI re-runs
    the orca-harness suite on this PR.
  stale_language_search: >
    grep -rin -E "self-merge|self-merges|human-gated|human-land|do not .*self|structure b"
    AGENTS.md .agents/workflow-overlay
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    docs/decisions/overlay_enforcement_placement_classification_v0.md
    (run 2026-06-12 in the guard-clean-self-merge worktree off origin/main @ b463c3c)
  stale_language_search_result: >
    Executed 2026-06-12. All LIVE surfaces now carry the conditional CLEAN self-merge: AGENTS.md line
    60 (kernel landing clause), safety-rules.md line 25, the doctrine Status interim bullet, Decision
    item 2's server-gated-target parenthetical, and Decision item 7. The remaining "structure B" /
    "human lands every merge" / "agents do not self-merge" hits are the historical DCP receipts above
    (append-only records of prior states, correctly not edited) and the EP record's 2026-06-09 owner
    flag (now acted upon and recorded in that record's 2026-06-12 Update). No live surface still
    asserts that agents never self-merge to main.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - CLEAN + green + label is a CI-and-mergeability signal, NOT a human diff-review; main is not
      deployed and a bad merge is reversible by a follow-up PR
    - EP-01 protected paths and EP-03 push/force/destructive blocks are unchanged
    - the guard is Claude-Code-scoped; a non-Claude-Code harness is neither blocked nor granted
      self-merge until wired
    - not durable on main until this amendment's own PR is landed by a human (the pre-amendment guard
      blocks the agent from self-merging it)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 9: an unattended GitHub Actions auto-merge bot
    (.github/workflows/auto-merge.yml) that is the unattended extension of structure B' (item 7).
    Where the guard lets the in-session agent self-merge a CLEAN + green + agent-automerge-labeled PR,
    this workflow lands the SAME opt-in PRs with no agent session, triggered on CI completion plus a
    3-hour cron backstop and workflow_dispatch. It carries its own in-code guardrails: the
    agent-automerge label, mergeable == MERGEABLE, orca-harness-tests green (no failing/pending check),
    behind_by == 0 (up-to-date with main), one merge per run, and squash + delete-branch. It uses an
    immediate `gh pr merge --squash` that does NOT need the 403-blocked allow_auto_merge, so it is an
    interim unattended auto-merge, NOT the deferred server-side gate. The EP-03 guard and
    merge-when-green.ps1 are unchanged; the workflow runs in Actions, not through the PreToolUse hook.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/workflows/auto-merge.yml
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/workflows/ci.yml
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        Frozen enforcement-lane surface. The bot runs in Actions (not through the PreToolUse hook) and
        carries its guardrails independently; the in-session guard's lack of an up-to-date check is a
        documented residual and a deferred enforcement-lane follow-on, not closed here.
    - path: .github/workflows/ci.yml
      reason: >
        Referenced by the bot's workflow_run trigger (workflows: [ci]) and as the orca-harness-tests
        green gate; its content is unchanged.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The do-not-push/merge-unless-authorized rule is unchanged; the bot is an Actions actor, not an
        agent lane, and the owner lands this lane's own PR.
  verification: >
    auto-merge.yml parses (python yaml.safe_load OK): workflow name auto-merge, concurrency group
    auto-merge, env AUTOMERGE_LABEL=agent-automerge, permissions contents/pull-requests: write, triggers
    workflow_run[ci] + schedule(0 */3 * * *) + workflow_dispatch. All label references are
    agent-automerge while name/concurrency stay auto-merge; the jq eligibility filters were hand-traced
    (green -> eligible; failing/pending/no-checks -> skip). NOT live-run: jq is not installed locally and
    the workflow cannot run until on main; the first live merge is owner-triggered and fail-safe.
  stale_language_search: >
    rg -i -n "auto.?merge|allow_auto_merge|unattended|overnight"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-14 in the automerge-bot-v0 worktree off origin/main @ 8e54aad)
  stale_language_search_result: >
    Executed 2026-06-14. Item 4 (native auto-merge deferred/blocked) now carries a parenthetical pointer
    to the interim Actions-bot path (item 9); the Status section carries the unattended-auto-merge
    bullet; item 9 is the canonical home. No live surface still implies the human merge is the only
    interim or that no unattended auto-merge exists. The "deferred target" wording for the native
    allow_auto_merge + server gate stays accurate (item 9 is explicitly not that gate).
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the bot is code-backed and logic-checked, NOT a proven unattended merge; the first live run is
      owner-triggered and fail-safe (ineligible PR skipped, never mis-merged)
    - not the server-side branch-protection / native auto-merge gate (still 403-blocked); an interim
      Actions-bot mechanism
    - the in-session guard path still lacks an up-to-date check (documented residual); the guard is
      unchanged this lane
    - the owner lands this lane's own PR
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 10: a lane-start auto-prune standing rule (agent-instruction-only) that is the
    CLEANUP complement to item 9's auto-merge bot. At each new lane's start the agent runs
    `git fetch --prune origin`, then non-force `git worktree remove` of any [gone]-branch worktree with
    no open PR, then `git branch -D` of those [gone] branches (both worktree-bound and branch-only),
    bounded by load-bearing guards: non-force remove only, exclude open-PR worktrees, never the seal or
    any [ahead]-unpushed worktree, glance for closed-unmerged before -D, and re-derive live every time.
    It is NOT a destructive always-on automation, NOT a --force prune, NOT a creation throttle, and NOT
    a guard edit; wiring the item-8 lane-health-check.ps1 detector to perform/prompt the prune is an
    explicit optional follow-on, deliberately deferred (the detector stays read-only).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/scripts/lane-health-check.ps1
    - .github/workflows/auto-merge.yml
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The EP-03 guard is the frozen enforcement-lane surface; this is a behavioral/doctrine rule and
        does not edit or weaken it. Non-force worktree remove and branch -D on lane branches are not
        guard-blocked actions; push-to-main / force-push / destructive clean stay hard-blocked.
    - path: .github/scripts/lane-health-check.ps1
      reason: >
        The item-8 detector stays read-only; wiring it to perform or prompt the prune is the explicit
        optional follow-on, intentionally not taken here to avoid introducing a destructive script.
    - path: .github/workflows/auto-merge.yml
      reason: >
        Item 9's bot (the merge half) is unchanged; item 10 is its cleanup complement and composes with
        it (a bot-merged lane's branch reads [gone] and becomes prunable at the next lane start).
    - path: AGENTS.md
      reason: >
        The behavior kernel and authorization boundaries are unchanged; the owner placed this procedural
        git rule in the decision record (not the terse global kernel), co-located with items 8 and 9.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The do-not-push/merge-unless-authorized rule is unchanged; this rule prunes only merged,
        no-open-PR residue at lane start and grants no new push/merge authority.
  verification: >
    Re-verified 2026-06-15 against origin/main before drafting (origin/main advanced 7c804cb -> 5efd405
    during the session; doctrine identical across both, empty diff): items 8 and 9 present and unchanged;
    PR #97 (auto-merge bot) MERGED 2026-06-14T14:36:46Z; auto-merge.yml and lane-health-check.ps1 tracked
    on origin/main. Live state grounding the guards: the only [gone] branch was
    r6-rescan-commission-beautypie (PR #37 MERGED -> a genuine squash-merge, not closed-unmerged); the
    [ahead] set was doctrine-harness-caveat, hooks-readme, judgment-spine-read-machinery-architecture-v0,
    ledger-c2-read-contract-v0; the seal worktree orca-seal-wt [pilot-seal-outcome] present. The prune
    commands are proven by this lane's predecessor backlog sweep (worktrees 53->29, six [gone] branches
    deleted, dirty worktrees correctly refused by non-force remove). NO fresh destructive sweep was run
    as part of authoring this rule.
  stale_language_search: >
    git grep -i -nE "auto.?prune|worktree remove|lane.?start.*prune|sprawl|manual sweep|cleanup.*manual|\[gone\]"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md AGENTS.md .agents/workflow-overlay
    (run 2026-06-15 in the autoprune-rule worktree off origin/main @ 5efd405)
  stale_language_search_result: >
    Executed 2026-06-15. The only hits are item 8 and its DCP receipt naming "worktree sprawl" as drift
    the read-only detector *surfaces*. No live surface claims cleanup is manual-only, that no prune rule
    exists, or that sprawl is unaddressed, so item 10 forks no existing wording — it is purely additive
    and acts on what item 8 only detects (the two compose: detect, then prune). No surface required an
    edit.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - a behavioral/doctrine rule, NOT code; "live" only insofar as agents follow it
    - asserts no proven long-run bound on worktree/branch count (unproven until run across several lanes)
    - not an edit to the EP-03 guard, the item-8 detector, or the item-9 bot
    - not a destructive always-on automation, a --force prune, or a creation throttle
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 11: a standing self-label policy for WHEN the lane author applies the existing
    opt-in agent-automerge marker. The merge mechanism is unchanged (items 7/9: bot/guard act only on
    labeled PRs); this item sets the agent's default judgment — apply the label to its own CLEAN + green
    PR by default for routine low-risk changes (additive docs, decisions/prompts/reviews the author is
    confident in, or small scoped code with test coverage), and WITHHOLD it (leave for owner review) for
    higher-risk changes: enforcement/safety surfaces (EP-01/EP-03 guard, hooks, settings.json, CI or
    auto-merge workflows, this doctrine), contested doctrine/tradeoff decisions, high downstream lock-in
    (schema/interface/persisted data), author uncertainty, or owner-requested review — when in doubt,
    withhold. This shifts the routine-work default from "wait for the owner" to "land unattended" while
    preserving the human gate where it matters. It grants NO new merge authority and is author judgment,
    not a path Action; a deterministic path-scoped auto-label Action is an explicit deferred follow-on.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/workflows/auto-merge.yml
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The EP-03 guard is unchanged: self-merge still requires CLEAN + green + label and fails closed.
        Item 11 sets which PRs the author labels, not what the guard allows; no authority is added.
    - path: .github/workflows/auto-merge.yml
      reason: >
        The bot's guardrails (label, mergeable, green, up-to-date, one-per-run, squash+delete) are
        unchanged; item 11 changes only the agent's default policy for applying the label it already reads.
    - path: AGENTS.md
      reason: >
        The behavior kernel and the per-turn / accepted-handoff authorization to open a PR at all are
        unchanged; this is a procedural default in the decision record, co-located with items 7/9/10.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The do-not-push/merge-unless-authorized rule is unchanged; item 11 grants no new authority and
        applies only to a PR the lane was already authorized to open.
  verification: >
    Re-verified 2026-06-15 against origin/main @ f883b68 (item 10 landed via PR #104, MERGED
    2026-06-15T08:05:22Z): items 7 and 9 present; item 7's "the opt-in label is the agent's deliberate
    marker" framing (lines ~100-101) stays accurate — item 11 keeps the marker a deliberate per-PR
    judgment and does not auto-apply it, so that wording is consistent and not edited. Item 7's "a human
    lands every other case" (unlabeled / non-CLEAN / non-green) also stays accurate. All YAML blocks parse.
  stale_language_search: >
    git grep -i -nE "self.?label|opt.?in|deliberate marker|by default.*label|agent-automerge"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md AGENTS.md .agents/workflow-overlay
    (run 2026-06-15 in the selflabel-default worktree off origin/main @ f883b68)
  stale_language_search_result: >
    Executed 2026-06-15. The agent-automerge / opt-in / deliberate-marker hits are all item 7 and item 9
    MECHANISM wording, which item 11 preserves (the bot/guard still act only on labeled PRs; the marker
    stays a deliberate per-PR judgment). No live surface claims the agent never self-applies the label or
    that every PR must wait for the owner, so item 11 forks no existing rule — it is additive and only
    sets the agent's default direction for applying the existing marker. The other opt-in hits are the
    unrelated delegated-review-patch convention. No surface required an edit.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - a behavioral/doctrine rule, NOT code; "live" only insofar as agents follow it
    - grants no new merge authority; item 7's guard and the per-lane authorization are unchanged
    - does not claim auto-landed PRs are correct (CI is a test-suite signal only; main is not deployed and
      a bad merge is reversible by a follow-up PR)
    - not a path-scoped auto-label automation (that deterministic variant is a deferred optional follow-on)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Flips the auto-merge bot (Decision item 9) from "code-backed, NOT a proven unattended merge" to
    PROVEN: on 2026-06-15 the bot landed PR #121 with no agent session (merged by github-actions[bot]).
    This was unblocked by PR #118, which added actions:read to the workflow permissions — the scope the
    statusCheckRollup -> checkSuite.workflowRun eligibility query needs; before it, every bot run that
    evaluated a labeled PR failed GraphQL "Resource not accessible by integration", so no earlier run had
    actually merged. Updates the two LIVE surfaces (the Status "Unattended auto-merge" bullet and item 9's
    Liveness line); the fail-safe behavior (ineligible PR skipped, never mis-merged) and the
    not-the-server-side-gate framing are unchanged.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .github/workflows/auto-merge.yml
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .github/workflows/auto-merge.yml
      reason: >
        The actions:read fix already landed via PR #118; this record only flips the liveness claim it
        enables. The workflow logic is unchanged.
    - path: AGENTS.md
      reason: >
        The kernel routes "land via the per-lane PR flow" to this doctrine; the bot's existence (item 9)
        and how to opt a PR in (item 11) live here, so no kernel edit is needed.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Merge authority is unchanged; proving the bot works grants no new authority.
  verification: >
    Observed 2026-06-15: PR #121 state MERGED, mergedBy.login = "github-actions"; auto-merge run
    27541440896 logged "PR #121 is eligible (labeled, mergeable, green, up-to-date). Merging (squash)."
    then "Merged PR #121 at 0a87d8f8...". Earlier bot run 27534994021 had failed on PR #116 with
    "Resource not accessible by integration (...statusCheckRollup...checkSuite.workflowRun)"; actions:read
    landed via PR #118 (MERGED 2026-06-15). The two live surfaces now read "proven".
  stale_language_search: >
    git grep -inE "first live run|first live merge|not.{0,4}a proven unattended|NOT.{0,4}claim a proven"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-15 in the doctrine-automerge-bot-proven worktree off origin/main @ 9f10a8a7)
  stale_language_search_result: >
    Executed 2026-06-15. The two LIVE surfaces (Status "Unattended auto-merge" bullet, item 9 Liveness)
    now read "proven". The remaining "first live run / first live merge / not a proven" hits are the
    append-only DCP receipts that recorded the bot's addition and its actions:read fix — historical
    records of prior states, correctly NOT edited.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the proven claim is one observed unattended bot merge (#121); it is NOT the server-side
      branch-protection gate (still 403-blocked) and does not claim the bot is bug-free
    - still fail-safe: an ineligible PR is skipped, never mis-merged
    - the in-session PreToolUse guard is unchanged (and is harness/working-tree-scoped, not the bot)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 12: adopts the up-to-date-before-merge MGT after recurring red push:main CI from
    combination breaks (two independently-green PRs that break combined). Root cause: behind_by==0 is
    enforced only for the bot (item 9), not the in-session guard (item 7 residual) or human/CLI merges.
    Adopted: (1) bot-as-default merge path (routine PRs land via the bot, which enforces up-to-date;
    extends item 11); (2) forward-ref annotation discipline (a branch-only open_next/derived_from link
    must carry "# nonresolving: <reason>", which check_map_links already exempts as debt); (3) a red-main
    detector workflow (.github/workflows/main-red-alert.yml) that opens/auto-closes a single tracking
    issue on push:main red/green. Downgraded O2a (guard behind_by check) and O2b (merge-when-green
    refuse-when-behind); deferred the server-side require-up-to-date gate (O1, 403-blocked). Foregone
    limit named: a raw gh pr merge of a behind PR can still break main — detected fast, not prevented.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/workflows/main-red-alert.yml
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/scripts/merge-when-green.ps1
    - .agents/hooks/check_map_links.py
    - .github/workflows/auto-merge.yml
    - AGENTS.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        O2a (adding behind_by==0 to the guard's self-merge allowance) is downgraded, not adopted; the
        frozen EP-03 guard is unchanged. Agents route through the bot (which enforces up-to-date) by default.
    - path: .github/scripts/merge-when-green.ps1
      reason: >
        O2b (refuse-when-behind in the helper) is downgraded — a raw gh pr merge bypasses the helper, so
        the substrate gives near-zero coverage of the actual path. Unchanged.
    - path: .agents/hooks/check_map_links.py
      reason: >
        The "# nonresolving:" exemption already exists in the checker; item 12 adopts the DISCIPLINE of
        using it for deliberate forward-refs. No checker change needed.
    - path: .github/workflows/auto-merge.yml
      reason: >
        The bot already enforces behind_by==0; item 12 makes it the default path. The workflow is unchanged.
    - path: AGENTS.md
      reason: >
        The kernel routes "land via the per-lane PR flow" to this doctrine; the bot-as-default habit and
        the disciplines live here. No kernel edit.
  verification: >
    main-red-alert.yml parses (python yaml.safe_load OK): triggers workflow_run[ci] + workflow_dispatch;
    permissions issues:write + actions:read; gated to push:main outcomes; dedup-by-title issue
    open/comment/close. check_map_links --strict OK on the PR tree — item 12's path refs resolve
    (main-red-alert.yml in this PR; check_map_links.py and merge-when-green.ps1 on main; the proposal is
    referenced by PR number, not a path token). Liveness: the detector is code-backed and NOT yet proven
    on a live red main (the first real push:main failure proves it), mirroring item 9's honest non-claim.
  stale_language_search: >
    git grep -inE "up.?to.?date|behind_by|combination break|main.?red|nonresolving"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-15 in the dev-workflow-uptodate-mgt worktree; re-synced onto origin/main after #127/#129)
  stale_language_search_result: >
    Executed 2026-06-15. Item 9 (now flipped to proven by #127) notes the in-session guard "lacks an
    up-to-date check (documented residual)"; item 12 is consistent with and acts on that note (downgrades
    the guard fix O2a, adopts bot-as-default instead). No live surface claims up-to-date is enforced on
    all paths, so item 12 forks no existing rule — it is additive.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the red-main detector is code-backed, NOT yet proven on a live red main; detective, not preventive
    - up-to-date enforcement is not complete here (the raw-CLI / other-harness path is a named, accepted
      residual); the complete, unbypassable gate remains the deferred server-side option (O1)
    - O2a does not edit the EP-03 guard; O2b does not edit the helper; check_map_links is unchanged
    - mini-god-tier is a capability-target lens, not a validation or readiness claim
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Narrows the proven unattended auto-merge bot with deterministic risk routing:
    `pr-risk-router.yml` labels PRs as auto-merge eligible, manual-review
    required, or blocked; `auto-merge.yml` now requires both `agent-automerge`
    and `risk/auto-merge-eligible` and skips manual/blocked PRs. Higher-risk PRs
    get a deterministic merge packet, not automated approval. This narrows the
    earlier label-only unattended path while preserving the non-claim that this
    is not server-side branch protection.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/workflows/auto-merge.yml
    - .github/workflows/pr-risk-router.yml
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The behavior kernel and explicit authorization boundaries are unchanged;
        this is a merge-routing workflow doctrine update, not a new global agent
        rule.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The no-unauthorized commit/push/PR/merge rule is unchanged. The workflows
        define repository automation behavior after explicit PR flow, not blanket
        agent authority.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The existing enforcement-placement and non-self-certification rules
        already cover this shape: deterministic labels are routing/check signal,
        not validation or approval evidence.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The current map already indexes `.github/` as GitHub Actions workflows
        and local operational scripts; no new top-level route is introduced.
  non_claims:
    - not server-side branch protection
    - not native GitHub auto-merge
    - not validation
    - not readiness
    - not review approval
    - not blanket agent merge authority
```

## From .agents/workflow-overlay/source-loading.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    New Thread Triggers now prefers a handoff packet plus a fresh lane over
    /compact-and-continue at phase boundaries; Targeted Read Protocol now binds
    the routine read shape for prompt-orchestration.md (Orca Prompt Preflight
    plus the single family section; full-file reads reserved for fused,
    delegated-review-patch, and novel or cross-lane authoring).
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/skill-adoption.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already states the routine-vs-full prompt-authoring split this read
        shape serves; the new rule points at that split rather than restating
        it.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Precompact/handoff packet skill bindings unchanged; the new trigger
        governs when to prefer a fresh lane, not how packets are built.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        workflow-precompact adoption status unchanged; the skill remains the
        packet mechanic when compaction is chosen.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Repo-map section anchors into this file are unchanged (checked
        2026-07-02; anchors reference read-pack sections, not the edited
        sections).
  stale_language_search: >
    rg -in "compact-and-continue|/compact|precompact" AGENTS.md .agents/workflow-overlay/
  stale_language_search_result: >
    Executed 2026-07-02 after edits. Hits: the new trigger itself
    (source-loading.md), this receipt's own text, precompact packet-skill
    bindings in source-of-truth.md and skill-adoption.md, and the AGENTS.md
    precompact-is-a-thin-restore-pointer rule — all compatible: they govern
    packet mechanics when compaction or handoff happens; none instructs
    compact-and-continue at phase boundaries.
  non_claims:
    - not validation
    - not readiness
    - no token-savings efficacy claim
```
## From orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Attachment Record implementation doctrine now binds Silver consumption: AR
    entries are typed raw-payload refs over preserved Bronze bodies, Silver
    records carry AR-backed raw_refs when deriving facts from source-family
    payload bodies, and missing AR rows remain visible residual/posture rather
    than inferred absence.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - orca/product/spines/data_lake/README.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca-harness/data_lake/catalog.py
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        Storage still owns Manifest v2, sidecar/member/body-store layout,
        backend, migration, retention, and lawful-erasure choices. This patch
        binds consumer shape without selecting those physicalization decisions.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        Core already defines Attachment Records as source-payload refs and
        forbids cleaned/Judgment meaning. This patch narrows downstream Silver
        consumption mechanics without changing the parent boundary.
    - path: orca-harness/data_lake/catalog.py
      reason: >
        Existing post-PR-525 catalog helpers expose AR rows and body hash
        verification; no runtime implementation is authorized here.
  stale_language_search: >
    rg -n "Attachment Record|raw_refs|Silver|Manifest v2|body store|full God Tier"
    orca/product/spines/data_lake orca-harness/data_lake/catalog.py docs/workflows/orca_repo_map_v0.md
  non_claims:
    - not validation
    - not readiness
    - not runtime implementation authorization
    - not Manifest v2 selection
    - not body-store layout selection
    - not Silver producer implementation
```

## From orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Storage Contract v0 retires the blanket no-storage-engine posture:
    the contract still selects no engine itself, but a bounded data-lake
    physicalization or implementation lane may now choose a concrete
    filesystem/database/SQL-capable embedded engine (for example DuckDB),
    object-store, warehouse/lakehouse, or hybrid backend when it preserves raw
    immutability, append-only derived/ack records, rebuildable non-authoritative
    indexes, by-key discovery, the no-smart-lake boundary, and external
    operational-data placement or an explicit supersession of that placement
    model.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/data_lake/README.md
    - docs/workflows/orca_repo_map_v0.md
    - orca-harness/data_lake/__init__.py
    - orca-harness/data_lake/root.py
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        It governs bronze/silver/pre-gold/gold-ready/gold semantics, not storage
        engine choice. Its backend non-claims remain correct as "not selected by
        this contract" and do not block a storage-contract physicalization lane.
  stale_language_search: >
    rg -n "no storage engine|No storage engine|selects no storage engine|select a storage engine|storage-engine selection|No backend/queue/scheduler/engine|No queue/engine|non-selecting storage contract|physical engine"
    orca/product/spines/data_lake orca-harness/data_lake docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-25 after edits. Remaining hits are expected and
    non-blocking: the new storage contract rule retires the old blanket no-engine
    posture and names the deliberate engine-selection boundary; mechanics,
    derived-layout, and physicality contracts now say no engine is selected by
    that artifact or map; storage and physicality prior DCP/non-claim hits are
    historical/non-authorizing receipts; the query appears in this receipt. No
    live current surface still says the Data Lake selects no storage engine,
    uses a non-selecting storage contract, or forbids a bounded downstream
    engine/backend selection.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not a selected engine/backend
    - not Manifest v2 selection
    - not sidecar selection
    - not queue/runtime selection
```

## From orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Physicality Location Contract v0 records the location boundary:
    operational data lives under one operator-configured external data root
    (ORCA_DATA_ROOT, generalized; example F:\orca-data), separate from the Git
    repo; the v0 directory grammar is raw/ attachments/ derived/ acknowledgements/
    and a split indexes/availability (content-free) plus indexes/derived_retrieval
    (rebuildable, non-authoritative); raw is immutable, derived/ack append-only,
    indexes rebuildable; root resolution is fail-closed including not-mounted and a
    root-marker identity check; durable record names are mechanical
    (SourceObjectMovementThresholdCrossingRecord, DecisionEvidenceAssemblyView,
    DecisionEvidenceAssemblyReceipt, DecisionEvidenceAssemblyProfile) with no
    GoldReady prefix and gold only as Judgment output; storage engine, backend,
    serialization, queue, runtime, and migration remain deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - orca/product/spines/data_lake/README.md
  downstream_surfaces_checked:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .gitignore
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        The Storage Contract remains the non-selecting physicalization-blocker owner.
        This contract adds the location boundary and directory grammar without
        reopening storage-slot or blocker ownership.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        The medallion contract already defers physical home and names the data lake
        physicality lane as a downstream consumer. This contract is that downstream
        location decision and does not change medallion semantics.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Repo-map registration is a separate hygiene/routing step on the shared map;
        this lane records the contract and its local README pointer without editing
        the shared repo map. Registration is a recommended follow-up.
  stale_language_search: >
    rg -n "ORCA_DATA_ROOT|physicality location|external data root|orca-data|indexes/availability|indexes/derived_retrieval|SourceObjectMovementThresholdCrossingRecord|DecisionEvidenceAssembly"
    orca/product/spines/data_lake docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    To be executed against the data_lake spine and repo map after landing; this lane
    introduces the ORCA_DATA_ROOT and physicality-location vocabulary, so expected
    hits are this contract and the data_lake README pointer. No prior live data-lake
    source is expected to define a competing data-root location boundary.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not backend or storage-engine selection
    - not serialization, manifest, or schema finalization
    - not queue/runtime design
    - not migration authorization
```

## From .agents/workflow-overlay/validation-gates.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Incident-derived workflow hardening now separates patch correctness, GitHub
    sandbox-egress classification, and validation-result bucket semantics: Codex/manual
    patch misses stop-and-reread and require `git diff` hunk inspection before correctness
    claims; `127.0.0.1:9` GitHub API failures are sandbox egress refusal, not repo/CI
    failure; validation reports classify outputs as GATE PASS/FAIL, INFO/DEBT, or OUT
    OF SCOPE, with unknown nonzero results failing closed.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .agents/workflow-overlay/validation-gates.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .github/workflows/ci.yml
    - .agents/hooks/check_map_links.py
    - .agents/hooks/check_doc_terms.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes repo-changing lane work to the dev-workflow doctrine and
        validation claims to the overlay; duplicating these scoped rules there would bloat
        the shared instruction surface and create drift risk.
    - path: .github/workflows/ci.yml
      reason: >
        No normalized validation wrapper is introduced yet. CI continues to run existing
        individual gates directly; wrapper enforcement is deferred until there is a concrete
        consumer.
    - path: .agents/hooks/check_map_links.py
      reason: >
        Existing strict/report modes already distinguish gate output from annotated debt;
        the new bucket policy governs reporting and any future wrapper rather than changing
        this checker.
    - path: .agents/hooks/check_doc_terms.py
      reason: >
        Existing `--check` / `--report-orca` modes are report-only and exit 0; the new
        bucket policy names them INFO/DEBT unless a future gate promotes them explicitly.
  stale_language_search: >
    rg -n "git diff --check|127\.0\.0\.1:9|GATE PASS|GATE FAIL|INFO|DEBT|OUT OF SCOPE|check_doc_terms|check_map_links"
    AGENTS.md .agents docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md .github .agents/hooks
  stale_language_search_result: >
    Executed 2026-06-20 during this patch. Existing and new hits are compatible: AGENTS.md already
    routes to the owning doctrine/overlay; check_map_links and check_doc_terms document strict
    versus report-only modes; ci.yml runs individual gates directly; no normalized wrapper consumer
    exists today.
  non_claims:
    - not validation
    - not readiness
    - not a new hook or CI wrapper
    - not a Claude Code edit-tool mandate
    - the bucket policy does not prove any artifact passes a gate
```

## From forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds the Aphrodite carveout charter as the strategy register above the
    product architecture: the brand-to-spine identity stitch and naming
    boundary; the phase strategy with gates; the two-layer moat doctrine
    (depth-now content/ontology layer, time-later longitudinal layer) as the
    cashing order of the ratified evidence-graph moat; the ratified first
    sellable unit (paid design-partner Vetting Sprint) with five evidence
    panels; buyer-lane defaults; the stratified capture policy shape
    (hypothesis-tier numbers); extraction-provenance and ToS-check pre-build
    gates; and the DECIDE/DEFAULT/DEFER register with MGT accepted residuals.
    Sequencing (foundation-first) and all ownership boundaries unchanged.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
    - docs/decisions/forseti_company_brand_architecture_v0.md   # D8 amendment (waitlist role fields), same lane
    - forseti/product/spines/creator_signal/README.md               # index row for this charter
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md  # foundation-first sequencing and Vetting v0 shape consistent; this charter sits above it and pulls nothing forward
    - docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md              # owns/does_not_own split untouched; charter routes to it
    - .agents/workflow-overlay/product-proof.md                                     # proof semantics consumed, not redefined
    - forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md    # grammar reused; parent demand-substrate gate explicitly not transferred
    - docs/workflows/orca_repo_map_v0.md                                            # decision/product records not exhaustively indexed (existing precedent); the spine README row carries the route
    - AGENTS.md                                                                     # no naming/brand/product content; routes to overlay — unchanged
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Existing precedent (spine binding DCP): per-spine artifacts route via
        the spine front door, which this lane updates; no repo-map row added.
    - path: forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
      reason: >
        Its Direction Update v0.1 remains the sequencing authority; this
        charter routes to it rather than editing it. Its older Vetting v0
        detail sections already carry the v0.1 supersession note.
  stale_language_search: >
    rg -in "aphrodite" --glob "!docs/_inbox/**" --glob "!forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md" .
  stale_language_search_result: >
    Executed 2026-07-04 in the lane worktree with all three edits staged, before
    commit. Hits in exactly four files, all expected: the brand ADR (the naming
    authority plus this lane's D8 amendment), the web-foundation design-lane
    handoff (a committed point-in-time packet whose stale_if routes receivers to
    the ADR), one captured-evidence datapoint (the "Soki London Aphrodite"
    fragrance product title in docs/review-inputs/youtube_shorts_fragrance_
    tone_expansion200_capture_v0.json — evidence data, not routing), and the
    spine README (this lane's new index row). No repo surface carries stale or
    conflicting Aphrodite routing.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not willingness-to-pay evidence
    - not implementation, capture, outreach, or publishing authorization
    - charter is DRAFT pending delegated review and owner ratification
```

## From docs/decisions/forseti_external_identity_path_migration_decision_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    After the Forseti rename audit, the next migration architecture splits
    external identity from internal compatibility paths: repo slug/local checkout
    identity may be migrated first under owner gate, while forseti/product/,
    orca-harness/, repo-map path, skill IDs, start-preflight alias, and CI check
    names remain deferred migration units until moved-path indexes, validation,
    rollback, and dependency impacts are bound.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - architecture_doctrine
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/forseti_rename_migration_policy_v0.md
    - docs/decisions/forseti_compatibility_migration_boundary_v0.md
    - docs/workflows/forseti_rename_stale_reference_audit_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - repo-structure.yaml
    - .github/workflows/ci.yml
    - .github/workflows/auto-merge.yml
    - .github/scripts/merge-when-green.ps1
    - .agents/hooks/guard_protected_actions.py
    - orca-harness/pyproject.toml
  intentionally_not_updated:
    - path: docs/decisions/forseti_compatibility_migration_boundary_v0.md
      reason: >
        It remains accurate for the already-completed Step 4/5 fused lane and
        explicitly says deeper migration requires a separate accepted plan; this
        new decision is that next-phase planning record, not a replacement edit.
    - path: repo-structure.yaml
      reason: >
        Internal roots remain compatibility paths in this branch; changing the
        machine structure map belongs to a future moved-path migration.
    - path: .github/workflows/ci.yml
      reason: >
        CI check name and working directory remain compatibility identifiers
        until the harness root/package migration is accepted.
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The GitHub repo slug has not been externally renamed yet; changing the
        protected-action repo slug before the external cutover would make the
        guard disagree with the current repository.
  stale_language_search: >
    git grep -l -F -- orca-harness; git grep -l -F -- orca/product; git grep -l
    -F -- docs/workflows/orca_repo_map_v0.md; git grep -l -F -- eric-foo/orca
  stale_language_search_result: >
    Executed 2026-07-04 in codex/forseti-path-migration-plan. Counts: 971
    tracked files mention orca-harness, 1239 mention orca/product, 474 mention
    docs/workflows/orca_repo_map_v0.md, and 84 mention eric-foo/orca. These are
    migration blast-radius evidence, not defects by themselves.
  non_claims:
    - not validation
    - not readiness
    - not path/package migration
    - not GitHub repo rename execution
```

## From .agents/workflow-overlay/validation-gates.md (archived 2026-07-10)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca validation doctrine adds a review-routing disposition gate: a change
    touching code roots (forseti-harness/, .agents/hooks/) must carry its review
    disposition -- a review artifact added under docs/prompts/reviews/ or
    docs/review-outputs/ in the same change, or a shape-valid
    review_routing_status line (routed <existing path> | blocked -- <reason> |
    not_needed -- <reason>) in the change's commit messages -- enforced
    diff-scoped and forward-only by .agents/hooks/check_review_routing.py
    (EP-35) as a CI --strict gate plus a local commit-msg advisory. Born from
    the 2026-07-02 fused-lane audit: fused implementation lanes carried a
    delegated-review obligation whose disposition lived only in chat, so most
    lanes closed without filing it and nothing durable could check the miss.
  trigger: validation_philosophy
  related_triggers:
    - review_authority
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_review_routing.py
    - .github/workflows/ci.yml
    - .githooks/commit-msg
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .claude/settings.json
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already routes validation and enforcement-placement changes to this
        overlay file; a kernel restatement would fork the owner.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        The gate binds no review lane and creates no verdict or severity
        authority; a pointer would dual-home the disposition rule.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        The convention stays provisional and opt-in; the gate enforces
        disposition visibility on code lanes generally, not this convention.
    - path: .claude/settings.json
      reason: >
        No PostToolUse wiring; the disposition is a commit-message property,
        not a file-write property. The local boundary is .githooks/commit-msg.
    - path: user-level fused skill source (~/.claude/skills/fused/SKILL.md)
      reason: >
        Outside Orca authority (installed/user-level skill source is
        protected); the owner applies the companion skill edit separately.
  stale_language_search: >
    rg -n "review_routing_status" .agents docs AGENTS.md
  stale_language_search_result: >
    Executed 2026-07-02 before this change: the token appeared only in one
    workflow handoff note (flagged there as an unowned one-off field) and one
    data-lake scoping record; no live overlay surface owned it. This change
    makes validation-gates.md the owning surface; the checker references it
    and does not restate it.
  non_claims:
    - not validation
    - not readiness
    - not review quality, severity, or verdict authority
    - not a bound or mandatory review lane
    - a green run is disposition shape only, never proof a review happened or was sufficient
```

## From forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Commission Signal Board rows now carry recency/currentness as source-route
    attention metadata: same-strength newer/current URL-backed signals normally
    deserve more downstream scan attention than older context, without becoming
    proof, classifier mapping, or graph weight.
  trigger: product_doctrine
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
    - orca-harness/tests/unit/test_commission_signal_board_output_validator.py
    - orca-harness/tests/fixtures/commission_signal_board_outputs/
    - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/check_commission_signal_board_output.py
    - forseti/product/spines/scanning/README.md
    - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The CSB validator remains a manual/local checker, not a CI, pre-commit,
        or write-hook gate. The existing enforcement-placement rule already
        covers why mechanically checkable output shape lives in the checker.
  stale_language_search: >
    rg -n "recency|recent|current-state|currentness|optional board metadata|validator only requires existing core row columns|proof|graph weight|classifier mapping"
    forseti/product/spines/commission_signal_board forseti/product/spines/scanning docs/workflows/orca_repo_map_v0.md
    (run 2026-06-23)
  stale_language_search_result: >
    Hits were accepted recency/currentness attention language, repo-map routing
    summaries, existing scanning safeguards, historical CSB source-family
    references, or explicit no-proof/no-classifier/no-graph-weight boundaries.
    No controlling CSB/scanning surface was found that turns recency/currentness
    into buyer proof, demand classification, classifier mapping, or graph weight;
    the old optional-validator wording produced only receipt search-string hits,
    not live instructional hits, after the CSB validator began requiring recency
    fields and enum values.
    Capture and Judgment surfaces carry their own DCP receipts for the same
    propagation, and the follow-up adversarial review ran a cross-spine leakage
    search with no proof, scoring, route-binding, or gate-clearance leakage found.
  non_claims:
    - not validation
    - not readiness
    - not demand classification
    - not buyer proof
    - not source-access authorization
```

## From .agents/workflow-overlay/validation-gates.md (archived 2026-07-10, EP-10/11/15 gate-wave rotation)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca validation doctrine adds a handoff-pointer resolution gate: a changed
    durable .md file must not reference a handoff-packet path
    (docs/workflows/*handoff*.md, docs/prompts/handoffs/*.md) that does not
    resolve in the same tree, unless the pointer line carries an explicit
    resolution pin (branch / PR # / origin ref vocabulary) or an exemption
    marker -- enforced diff-scoped and forward-only by
    .agents/hooks/check_handoff_pointers.py (EP-36) as a CI --strict gate.
    Born from repeated cold-agent resolution failures where handoff packets
    lived only on unmerged authoring branches while filed prompts referencing
    them landed on main, so receiving agents and delegated reviewers starting
    cold from main could not resolve their required reads.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_handoff_pointers.py
    - .github/workflows/ci.yml
    - forseti-harness/tests/unit/test_hook_internal_error_gating.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-of-truth.md
    - .claude/settings.json
    - .agents/hooks/check_map_links.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already routes validation and enforcement-placement changes to this
        overlay file; a kernel restatement would fork the owner.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Per the enforcement-placement principle a substrate-enforced rule is
        not also carried as a resident instruction; prompt authors hit the CI
        gate mechanically, and the existing worktree-preflight and
        input-prompt-source rules already carry the judgment side (which
        branch, which source) that stays resident.
    - path: .claude/settings.json
      reason: >
        No PostToolUse wiring: the defect is a merge-topology property
        (packet on a different unmerged branch), invisible at the write
        boundary where the packet usually exists in the author's own tree;
        the enforcing boundary is CI on the landing PR.
    - path: .agents/hooks/check_map_links.py
      reason: >
        Its C1/C2/C4 checks gate map files, open_next headers, and inline
        markdown links whole-corpus; the new gate covers prose/backtick
        handoff pointers diff-scoped with pin/exemption vocabulary --
        different scope and exemption grammar, kept as a sibling checker.
  stale_language_search: >
    rg -in "handoff.*resolv|resolve.*handoff|unmerged.*handoff|check_handoff_pointers"
    AGENTS.md .agents docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-03 after edits: hits are this gate's own rule text,
    checker, README row, and registration surfaces, plus unrelated generic
    mentions (the AGENTS.md jb-handoffs boundary sentence and skill-adoption
    skill-name rows); no other surface carries a conflicting handoff-pointer
    resolution rule.
  non_claims:
    - not validation
    - not readiness
    - not packet content freshness, pin truth, or source-choice correctness
    - not a courier-delivery guarantee for prompts that never land in the repo
    - a green run is pointer shape only, never proof the right packet was cited
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forseti validation doctrine adds a source-input hash freshness gate:
    repo-local JSON list-style source_inputs[] records with source_pointer +
    sha256 must match current file bytes when the artifact or referenced
    source changed, enforced by .agents/hooks/check_source_input_hashes.py
    (EP-37) as a diff-scoped CI --strict gate plus a local pre-push mirror.
    Born from PR #817, where a Creator Registry ledger merge changed the
    ledger hash while the YouTube metric seed still carried the old
    source-input hash and full pytest caught it late.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_source_input_hashes.py
    - .github/workflows/ci.yml
    - .agents/hooks/pre_push_guard.py
    - forseti-harness/tests/unit/test_hook_internal_error_gating.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - forseti-harness/tests/unit/test_youtube_creator_metric_seed.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md routes validation and enforcement-placement doctrine to the
        overlay; restating this narrow gate there would fork the owner.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Its DCP storage rule governs receipt rotation; the gate changes
        validation placement, not source hierarchy or receipt mechanics.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading budgets and source packs are unchanged; this is
        post-change provenance freshness, not source-loading procedure.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        This path is a compatibility pointer whose open_next is the live
        Forseti repo map; duplicating active hook content there would fork the
        current retrieval surface.
    - path: forseti-harness/tests/unit/test_youtube_creator_metric_seed.py
      reason: >
        The existing semantic/generated-artifact test remains; the new hook
        catches the broader hash-drift class earlier without weakening that
        test.
  stale_language_search: >
    rg -in "source-input hash|source_inputs.*sha256|check_source_input_hashes|strict CI doc gates"
    .agents docs .github forseti-harness
  stale_language_search_result: >
    Executed 2026-07-10 after edits: intended hits are this gate's owner text,
    checker, CI/pre-push wiring, hook README, live Forseti repo-map note,
    enforcement-placement classification, and historical/source-input ledger
    references; the stale phrase "strict CI doc gates" appears only in this
    receipt's search query/result provenance text, and no conflicting
    source-input hash rule remains.
  non_claims:
    - not validation
    - not readiness
    - not semantic generated-artifact completeness
    - not source quality, capture freshness, or metric validity
    - a green run is provenance hash freshness only
```

## From .agents/workflow-overlay/validation-gates.md (archived 2026-07-10, EP-10/11/15 gate-wave rotation, round 2)

```yaml
direction_change_propagation:
  doctrine_changed: >
    The source-input hash freshness gate (EP-37) extends to source-capture
    packet manifests: a JSON document with a top-level manifest_version string
    must have top-level preserved_files[] records (relative_packet_path +
    sha256) that match current raw stored bytes, with the path resolved
    against the manifest's own directory, when the manifest or the preserved
    file changed -- same diff-scoped, forward-only CI --strict gate plus local
    pre-push mirror in .agents/hooks/check_source_input_hashes.py. Gap
    surfaced by the EP-15 build survey (PR #842): the packet-manifest shape
    was matched by neither the source_inputs[] JSON gate nor the markdown
    pin-grammar gate, leaving preserved raw capture bytes ungated.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_source_input_hashes.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - .github/workflows/ci.yml
    - .agents/hooks/pre_push_guard.py
    - forseti-harness/tests/unit/test_hook_internal_error_gating.py
    - .gitattributes
  intentionally_not_updated:
    - path: .github/workflows/ci.yml
      reason: >
        The extension rides the already-registered EP-37 --strict step; there
        is no new gate to register.
    - path: .agents/hooks/pre_push_guard.py
      reason: >
        The local mirror already invokes check_source_input_hashes.py
        --strict; the extended record family is picked up unchanged.
    - path: forseti-harness/tests/unit/test_hook_internal_error_gating.py
      reason: >
        The hook's CASES row already pins internal-error gating; the
        extension changes matched record shapes, not error or exit semantics.
    - path: .gitattributes
      reason: >
        Its **/source_captures/** -text rule already pins the raw-bytes
        invariant this extension verifies; the gate consumes that invariant,
        it does not amend it.
  stale_language_search: >
    rg -in "preserved_files|relative_packet_path|source-input hash|source_inputs.*sha256"
    .agents docs/workflows/forseti_repo_map_v0.md
    docs/decisions/overlay_enforcement_placement_classification_v0.md .github
  stale_language_search_result: >
    Executed 2026-07-10 after edits: hits are this gate's own rule text and
    receipt, the checker and its selftest, CI/pre-push wiring, the hook README
    rows, the enforcement-placement decision record, and the repo-map gate
    entry plus its generic .agents/hooks folder description; no other surface
    carries a conflicting source-input or preserved-file hash rule.
  non_claims:
    - not validation
    - not readiness
    - not archive completeness or source-state truth
    - not capture freshness, source quality, or packet content correctness
    - a green run is provenance hash freshness only
```

## From docs/decisions/forseti_mini_god_tier_doctrine_v0.md (archived 2026-07-11, problem-bound target rotation)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Mini God Tier doctrine renames the mandatory visible-limitations requirement
    to accepted residuals: residuals are named, bounded, justified, and carry
    remaining risk plus an upgrade trigger after pushing to the diminishing-
    returns edge; source-quality "visible limitations" vocabulary remains
    operational reporting vocabulary, not the doctrine-level name.
  trigger: product_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - AGENTS.md
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/safety-rules.md
    - docs/workflows/orca_repo_map_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
  intentionally_not_updated:
    - path: CLAUDE.md
      reason: >
        Claude shim imports AGENTS.md and must not duplicate Orca project rules.
    - path: .agents/workflow-overlay/README.md
      reason: >
        Overlay index does not own Mini God Tier vocabulary; AGENTS.md points to
        this decision record as the full statement.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading owns read-pack mechanics and does not restate the Mini God
        Tier lens.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Safety rules reference the separate Source Capture Armory Mini God-Tier
        source-quality discipline; that operating profile is intentionally not
        renamed by this doctrine-level vocabulary patch.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Repo map routes Source Capture Armory source-quality surfaces. The
        global Mini God Tier trigger remains AGENTS.md -> this decision record;
        no path or read-pack destination changed.
    - path: orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
      reason: >
        The source-quality profile owns operating result tokens and the
        visible_limitations report field. Those are lower-level source/capture
        reporting vocabulary and remain valid; changing them would rewrite
        historical tokens and exceed this owner vocabulary patch.
    - path: orca/product/spines/capture/core/source_capture_toolbox/README.md
      reason: >
        The README indexes the source-quality operating profile and closeouts,
        whose visible-limitations terminology remains intentionally unchanged.
  stale_language_search: >
    rg -n "mini god tier|Mini God Tier|Mini God-Tier|visible limitations|accepted residual|source_quality_mini_god_tier"
    AGENTS.md CLAUDE.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
    docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
    orca/product/spines/capture/core/source_capture_toolbox/README.md
  stale_language_search_result: >
    Executed 2026-06-21 in branch codex/mgt-accepted-residuals-v2 after the patch.
    Remaining "visible limitations" hits in the checked source-quality surfaces
    are operating/reporting vocabulary by design. AGENTS.md now uses accepted
    residuals for the global trigger binding, and this record now separates
    doctrine-level accepted residuals from source-quality visible-limit reporting.
  non_claims:
    - not validation
    - not readiness
    - not proof
    - not source-quality token migration
    - not source-of-truth promotion
```

## From docs/decisions/forseti_mini_god_tier_doctrine_v0.md (archived 2026-07-11, context-bound SCI follow-up rotation)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Mini God Tier doctrine now sets the default owner-invoked target at roughly
    90-95% of practical maximal capability value, explicitly rejecting an 80/20
    shortcut interpretation while preserving Smallest Complete Intervention,
    accepted residuals, lock-in guards, and the non-claim boundary.
  trigger: product_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md intentionally points to this decision record as the full Mini
        God Tier statement; duplicating the 90-95% target there would fork the
        doctrine surface.
    - path: CLAUDE.md
      reason: >
        Claude shim imports AGENTS.md and must not duplicate Orca project rules.
    - path: .agents/workflow-overlay/README.md
      reason: >
        Overlay index does not own Mini God Tier vocabulary; AGENTS.md points to
        this decision record as the full statement.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and DCP mechanics are unchanged; this patch changes the
        product-doctrine target bar inside the existing controlling decision.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading owns read-pack mechanics and does not restate the Mini God
        Tier lens.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        No path, route, source-pack, or index destination changed; the existing
        AGENTS.md -> decision-record binding remains the discovery route.
    - path: orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
      reason: >
        The source-quality profile owns a specific capture operating profile and
        its visible_limitations report field. This patch changes the global
        owner-invoked MGT doctrine lens without rewriting source-quality
        operating tokens.
    - path: orca/product/spines/capture/core/source_capture_toolbox/README.md
      reason: >
        The README indexes the source-quality operating profile and closeouts;
        no route or source-quality profile name changed.
  stale_language_search: >
    rg -n "80/20|90-95|90%|95%|fraction of its cost|cheap or obvious|Mini God Tier|mini god tier|Mini God-Tier"
    AGENTS.md CLAUDE.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
    docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    orca/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
    orca/product/spines/capture/core/source_capture_toolbox/README.md
  stale_language_search_result: >
    Executed 2026-06-30 in branch codex/mgt-90-95-doctrine after the patch.
    Hits outside this decision record are route/binding mentions or
    source-quality profile mentions that do not define the global MGT target
    percentage. No checked downstream surface states an 80/20 target or a lower
    default bar for the global Mini God Tier doctrine.
  non_claims:
    - not validation
    - not readiness
    - not proof
    - not a numeric achievement claim
    - not source-quality token migration
    - not implementation authorization
```

## Archived from .agents/workflow-overlay/prompt-orchestration.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Review-prompt economy: ordinary single-target read-only reviews may use the
    routine preflight path when no escalation trigger applies; deep-thinking is
    required by trigger rather than for every review prompt; delegated route-out
    delivery follows source-role filing classification, where paste-ready chat is
    a copy/surface rather than a substitute for required filed or lane-scoped
    prompt carriage.
  trigger: workflow_authority
  related_triggers: [review_authority, output_authority]
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-loading.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: Operating Economy already says deep-thinking is triggered-only; this patch reconciles subordinate review/prompt doctrine to that kernel.
    - path: .agents/workflow-overlay/source-loading.md
      reason: Source-Gated Method Contract and source readiness are unchanged.
  non_claims:
    - not validation
    - not readiness
    - not runtime model routing
    - not patch authorization
```


## Archived from .agents/workflow-overlay/source-of-truth.md

```yaml
direction_change_propagation:
  doctrine_changed: >
    Receipt-archiving rule adopted (at most two most-recent receipts inline per
    controlling file; older receipts move verbatim to the single authorized
    standalone archive docs/decisions/dcp_receipts_archive_v0.md; inline section
    ends with one pointer line to the archive; no other standalone receipt files)
    AND strength-preserving compression of prompt-orchestration.md and
    source-of-truth.md (duplicate prose collapsed, multi-sentence annotations
    tightened to one sentence; every must/never/only/required obligation
    preserved verbatim or in equivalent enumeration).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-loading.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md is the agent-behavior kernel; it carries no receipt mechanics
        and does not enumerate inline-vs-archive storage rules. The kernel
        already routes doctrine-changing work to the overlay.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its gate 12 defers to source-of-truth.md for receipt mechanics and its
        "standalone receipt file" prohibition refers to unauthorized expansions,
        not the one authorized archive. No gate logic changes.
  stale_language_search: >
    rg -i -n "standalone receipt|inline in the changed artifact|do not create a standalone"
    .agents docs AGENTS.md
  stale_language_search_result: >
    Executed 2026-06-13 in worktree orca-f2-trim-wt (branch f2-doctrine-trim,
    base origin/main). Hits: .agents/workflow-overlay/validation-gates.md:33
    ("standalone receipt file" in the prohibition list for unauthorized
    expansions — consistent with the new rule; the one authorized archive is
    named in source-of-truth.md and not prohibited).
    .agents/workflow-overlay/source-of-truth.md:106,109,110 — the amended
    paragraph introducing the archive rule.
    .agents/workflow-overlay/artifact-folders.md:203 — DCP contract stores
    receipts inline, consistent.
    docs/prompts/handoffs/ecr_jsg01_source_side_receipt_lane_setup_v0.md:87 —
    unrelated "no standalone receipt file" in a prompt context.
    review-input and review-output snapshots — contain historical text only.
    No live surface retains an instruction that contradicts the new archive rule
    or the removed "Do not create a standalone receipt file" sentence.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
```

## From .agents/workflow-overlay/validation-gates.md (archived 2026-07-11, pre-push/ontology gate rotation)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forseti validation doctrine adds two gates and hardens one: a
    review-summary shape gate (changed docs/review-outputs/ files carrying a
    real review_summary block must keep the communication-style.md shape --
    no forbidden process keys, a resolving report_path, the bound
    failed-write shape, non-blank recommendation; full recommendation
    vocabulary membership stays advisory-only pending an owner decision on
    the delegated-review-patch extended vocabulary), a hash-pin freshness
    gate (markdown freshness pins -- labeled path+sha256 bullet pairs and
    source_captures receipt.md preserved-file bullets -- must match current
    CRLF-normalized target bytes when the pin doc or target changed;
    provenance-style tables and ledgers deliberately unparsed), and
    substrate enforcement of the existing Output-mode gate's checkable shell
    (declaration presence plus at least one closed-set token; exactly-one
    and role-scoping stay resident). Enforced by
    .agents/hooks/check_review_summary.py, check_hash_pin_freshness.py, and
    check_prompt_output_mode.py as diff-scoped forward-only CI --strict
    gates (hash-pin also mirrored in the local pre-push guard), built under
    the EP-10/EP-11/EP-15 rows of
    docs/decisions/overlay_enforcement_placement_classification_v0.md with
    the EP-11 row corrected SUBSTRATE->PARTIAL from build-time corpus
    measurement.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_prompt_output_mode.py
    - .agents/hooks/check_review_summary.py
    - .agents/hooks/check_hash_pin_freshness.py
    - .github/workflows/ci.yml
    - .agents/hooks/pre_push_guard.py
    - forseti-harness/tests/unit/test_hook_internal_error_gating.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - .agents/hooks/README.md
    - .agents/workflow-overlay/skill-adoption.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/communication-style.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/source-of-truth.md
    - .claude/settings.json
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Routes validation and enforcement-placement doctrine to this overlay
        file; a kernel restatement would fork the owner.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        It owns the review_summary shape being enforced; the checker
        references it, and the known delegated-review-patch extended
        recommendation vocabulary is flagged for a separate owner decision
        rather than silently widening the bound enum here.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        It owns the closed output-mode set; per the enforcement-placement
        principle the substrate references the owner (and the checker
        selftest asserts against the owning section), so no restatement is
        added.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        Its lanes' extended recommendation vocabulary is the flagged owner
        gap; binding or renaming that vocabulary is a doctrine decision this
        gate deliberately does not make.
    - path: .claude/settings.json
      reason: >
        No new write-time hooks: prompt writes already receive the
        check_prompt_provenance.py reminder, review outputs are frequently
        authored by other harnesses that never fire this harness's hooks,
        and hash drift is a cross-file property best caught at push/CI.
  stale_language_search: >
    rg -in "output-mode gate|review_summary|hash-pin|check_prompt_output_mode|check_review_summary|check_hash_pin_freshness"
    AGENTS.md .agents docs/workflows/forseti_repo_map_v0.md docs/decisions/overlay_enforcement_placement_classification_v0.md
  stale_language_search_result: >
    Executed 2026-07-10 after edits over the declared scope: hits are the new
    gate bullets and Enforcement Placement registry text in this file, the
    three checkers' own docstrings/selftests, the hooks README rows, the
    pre_push_guard mirror entry, the repo-map Active Hooks notes, the
    classification-doc update and corrected EP-11 row, the skill-adoption pin
    pointer, and pre-existing reference text in communication-style.md (the
    review_summary shape source), review-lanes.md, delegated-review-patch.md
    (hash-pinned protected-path language), and one hash-pinned mention in
    check_handoff_pointers.py; AGENTS.md has zero hits. No surface carries a
    conflicting output-mode, review-summary, or hash-pin enforcement rule.
  non_claims:
    - not validation
    - not readiness
    - not review quality, finding truth, or severity authority
    - not prompt quality or mode-choice correctness
    - not semantic validity, source quality, or capture freshness
    - a green run is shape/freshness only, never approval
```

## From docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md (archived 2026-07-11, server-gate activation rotation)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds PR cadence guidance: lanes should open a focused PR after each major
    durable point, not after every subpoint; subpoints stay grouped when they
    share the same reviewable decision, controlling sources, validation, and
    non-claims. PR bodies should state the decision change, why, stance shifts,
    changed files, non-claims, and validation.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes landing through this per-lane PR flow. The
        cadence refinement belongs in the flow record, not the root kernel.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The explicit-authorization rule for commit, push, and PR creation is
        unchanged; this cadence applies only after authorization.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and propagation mechanics are unchanged; this is a
        downstream workflow decision amendment.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map already points lane PR flow to this decision record; no
        new routing surface or file owner was added.
  stale_language_search: >
    rg -n "major durable point|every major point|every subpoint|per-lane PR|one focused PR|PR cadence"
    AGENTS.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  stale_language_search_result: >
    Executed 2026-06-16 after this patch. Hits are the new item 9 cadence
    language, this receipt, and existing compatible references to per-lane /
    one-focused-PR flow. No checked surface requires a PR for every subpoint or
    grants standing PR authority.
  non_claims:
    - not validation
    - not readiness
    - not blanket commit authorization
    - not blanket push authorization
    - not blanket PR authorization
    - not a merge authorization
```

## From `.agents/workflow-overlay/prompt-orchestration.md` (archived 2026-07-12, target-worktree resolution rotation)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Prompt filing is now classified by source role: canonical, reusable, or
    doctrine-bearing prompt artifacts still file under docs/prompts/**, while
    lane-scoped execution prompts attach to the overall lane PR body/comment or
    ignored docs/_inbox scratch and must not open standalone prompt-only PRs.
  trigger: workflow_authority
  related_triggers:
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/check_prompt_provenance.py
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/dcp_receipts_archive_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/template-registry.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .github/workflows/pr-risk-router.yml
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes prompt mechanics to prompt-orchestration.md and
        still correctly requires every durable prompt, handoff, wrapper, rerun,
        or patch prompt to apply the prompt contract; no root restatement of the
        filing classification is needed.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its prompt gates defer output-mode and prompt-mechanics exceptions to
        prompt-orchestration.md; it did not encode the old file-every-cross-
        recipient-prompt rule, so no gate wording changes.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading owns read packs and source capsules. This patch changes
        where lane-scoped prompt text is carried, not the required reads or
        Source-Gated Method Contract.
    - path: .agents/workflow-overlay/artifact-folders.md
      reason: >
        Existing folder roles already distinguish docs/prompts/** canonical prompt
        artifacts from docs/_inbox scratch; the prompt owner now classifies when
        each applies.
    - path: .agents/workflow-overlay/artifact-roles.md
      reason: >
        Existing role bindings already define Full prompt artifact and Inbox
        scratch separately; this patch changes the routing rule, not the role
        table.
    - path: .agents/workflow-overlay/template-registry.md
      reason: >
        Template rows that use paste-ready-chat describe template delivery modes,
        not whether a lane-scoped execution prompt opens a standalone PR.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        Its paste-ready route-out remains governed by prompt-orchestration.md;
        route-out prompts may now be lane-scoped when they only fill the current
        commission lane, or canonical when promoted as reusable artifacts.
    - path: .github/workflows/pr-risk-router.yml
      reason: >
        It should continue treating docs/prompts/** as manual-risk for canonical
        prompt artifacts; the fix is to stop creating standalone tracked prompt
        files for lane-scoped execution prompts, not to loosen PR risk routing.
  stale_language_search: >
    rg -i -n "Durable and cross-recipient|paste-ready-chat prompt that never touches disk|not a substitute for filing|filed artifact|standalone prompt PR|prompt-only PR|prompt artifact path"
    .agents AGENTS.md docs/workflows docs/prompts/templates .github/workflows/pr-risk-router.yml docs/decisions/dcp_receipts_archive_v0.md;
    rg -i -n "authored as a FILE-WRITE under docs/prompts|requires durable.*cross-recipient.*touch disk|not an accepted authoring path|never touch disk|durable prompt.*docs/prompts|cross-recipient prompt.*docs/prompts|file-every-cross"
    .agents AGENTS.md docs/workflows docs/prompts/templates .github/workflows/pr-risk-router.yml;
    rg -i -n "lane-scoped|overall lane PR|prompt-only PR|standalone prompt PR|canonical prompt"
    .agents AGENTS.md docs/workflows docs/prompts/templates .github/workflows/pr-risk-router.yml
  stale_language_search_result: >
    Executed 2026-06-30 after edits. The broad old-language query hits only the
    new canonical/lane-scoped rule in prompt-orchestration.md plus historical
    archived receipts in docs/decisions/dcp_receipts_archive_v0.md; the stricter
    old-mandate query hits only this receipt reason text ("file-every-cross-");
    and the lane-scoped query hits the new owner rule plus the updated hook and
    repo-map notes. docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md
    says canonical prompt destinations remain unchanged, which is consistent.
    No live surface checked retains an unqualified durable/cross-recipient
    docs/prompts/** filing mandate or a standalone prompt-PR requirement.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
    - not a cleanup decision for existing prompt PRs
```
