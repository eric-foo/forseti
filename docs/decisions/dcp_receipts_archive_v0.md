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
