# DCP Receipts Archive

```yaml
retrieval_header_version: 1
artifact_role: DCP receipts archive
scope: Verbatim archive of direction_change_propagation receipts that have cycled out of the two-most-recent inline limit in controlling overlay files.
use_when:
  - Auditing the full propagation history of past doctrine changes.
  - Verifying that a stale-language search term was already handled in a prior receipt.
  - Tracing which surfaces were checked or intentionally skipped for a historical doctrine change.
authority_boundary: retrieval_only
```

This file is the single authorized standalone archive for Orca direction_change_propagation receipts that have been moved out of controlling overlay files under the receipt-archiving rule (at most two most-recent receipts inline per controlling file; older receipts move here verbatim). The rule that governs receipt archiving lives in `.agents/workflow-overlay/source-of-truth.md`, Doctrine Change Propagation Contract section. This file carries no source authority, validation evidence, readiness, approval, or lifecycle claims.

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
