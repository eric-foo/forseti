# Source Of Truth

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Source hierarchy, conflict rules, doctrine-change propagation, and known source documents.
use_when:
  - Resolving Forseti source precedence.
  - Checking whether a document is a known Forseti source.
  - Changing product, architecture, workflow, validation, review, output, or lifecycle doctrine.
authority_boundary: retrieval_only
```

## Current Source Hierarchy

1. Explicit user instruction for the current turn.
2. Forseti `AGENTS.md`.
3. This overlay under `.agents/workflow-overlay/`.
4. Forseti docs under `docs/`, when they do not conflict with the overlay.
5. Explicitly invoked or resolver-loaded skills may provide task-local mechanics only; they are not Forseti project authority.

## Conflict Rules

- Forseti overlay wins for Forseti project facts.
- External workflow sources do not own Forseti project authority. Skills may provide task-local mechanics only when explicitly invoked or resolver-loaded.
- Installed global/user/plugin skills are runtime copies or external tools, not Forseti project authority.
- If a required source is missing, report a visible failure and name the missing file or decision.
- Source hierarchy is not a read-all list. Use `.agents/workflow-overlay/source-loading.md` and `docs/workflows/forseti_repo_map_v0.md` to choose bounded source packs.

## Checkpoint Artifacts

Checkpoint artifacts capture transient lane state for recovery or transfer:
precompact working packets (`workflow-precompact`, under `docs/hygiene/`), cold
cross-lane handoff packets (`workflow-handoff`), and any equivalent lane-state
resume/snapshot note. They are convenience copies, never a Forseti source of truth.

- Non-authoritative. A checkpoint's volatile claims — what is built, what is
  authorized, current doctrine, or "where we are" — are orientation only.
  Re-confirm any such claim against the canonical source (the owning
  decision/contract/overlay), or against disk for build state, before relying on
  it. The source hierarchy above governs; a checkpoint never overrides it, even
  when more recent.
- Single-consumption, one live instance per lane. A checkpoint exists to be consumed once; the consuming lane deletes it after recovery checks run and live state is re-established. Refresh by overwriting in place under a stable name — do not accumulate `_v2`/`_v3` copies. A checkpoint whose work has landed (committed/settled) is retired by deletion.
- Point, do not copy. When a checkpoint must carry a volatile fact, record a
  pointer plus a re-confirm instruction (for example "authorization -> <decision>;
  build state -> glob disk"), not a copied snapshot that silently goes stale.

This binds how Forseti uses the `workflow-precompact` and `workflow-handoff` skills:
the skills supply mechanics, this overlay owns the lifecycle. It does not apply to
Forseti source-of-truth artifacts (decisions, contracts, architecture records) or to
pointer-indexes (the repo map, this overlay) — those are the canonical sources a
checkpoint points to and must never be deleted as "consumed." It also does not
apply to authored handoff *prompts* under `docs/prompts/handoffs/` (the
Planning/Implementation handoff prompt role): those are docs-only prompt
artifacts, not lane-state checkpoints, and keep their own role lifecycle.

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
  `docs/workflows/forseti_repo_map_v0.md`;
- executor, prompt, validation, review, and closeout surfaces when the doctrine
  affects them.

Keep propagated restatements faithful to the controlling source's strength. A
restatement in a downstream surface must not soften or narrow the controlling
rule — for example a `required`/`must` weakened to "add when known" — nor
silently fork it. Where the same wording would otherwise be copied across
surfaces, prefer pointing them at the single controlling source over duplicating
it, so the copies cannot desynchronize.

Store the propagation evidence inline in the changed artifact, prompt, handoff,
or final closeout. A controlling file keeps at most the two most recent receipts
inline; older receipts move verbatim to `docs/decisions/dcp_receipts_archive_v0.md`,
the single authorized standalone receipt archive. The inline receipts section must
end with one pointer line to the archive. No standalone receipt files other than
the authorized archive.

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
  stale_language_search: "<query, or not_run + why — not_run only for a purely additive change>"
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

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orientation/research subagent dispatch now binds a third dimension — the
    return shape. prompt-orchestration.md (the subagent-contract owner) now
    requires, for a subagent whose output an agent will consume (act on,
    summarize, or route — even if later shown to a human), a terse schema-bound
    verdict (named fields, one line each, a file:line cite per load-bearing
    claim, `unknown` for an absent field) instead of a prose dump, validated by
    the spawning CA on receipt. The load side stays owned by the source-readiness
    rule and source-loading.md; the new rule defers to them and binds only the
    return shape. The behavior contract gains a CA-facing pointer rather than a
    separate local return rule. Additive and orthogonal to the two existing
    subagent rules: source-readiness (prompt-orchestration.md, above it) and
    forked-context runtime-payload safety (decision-routing.md).
  trigger: workflow_authority
  related_triggers:
    - output_authority
  reviewed_by: >
    Cross-vendor delegated review (GPT-family, provisional convention) run and
    CA-adjudicated 2026-06-12; findings AR-01 (human/agent boundary loophole),
    AR-02 (behavior-contract pointer not a soft local rule), AR-03 (defer
    load-side ownership), AR-04 (receipt honesty) accepted and applied. Decision
    input only; not a bound-lane verdict.
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/communication-style.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Carries no subagent return-shape instruction (grep: no "subagent" hit)
        and already routes detail to the owning overlay file; the rule lives in
        prompt-orchestration.md, so no AGENTS.md restatement is added.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        Owns the distinct forked-context runtime-payload rule; the return-shape
        dimension is orthogonal and cross-referenced from prompt-orchestration.md,
        so nothing here changes or conflicts.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        The load-side owner (budgets, pack tiers, source-capsule and repo-access
        rules); the new rule defers to it for the load side and changes nothing
        in it.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        Its prose guidance governs human-facing chat output; the new rule governs
        agent-facing subagent returns — complementary, no conflict, no edit.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        No subagent enumeration to update (grep: no hit); these are additive
        in-file doc edits, not a structural or navigation change. repo-map-ack.
  stale_language_search: run
  stale_language_search_result: >
    Ran 2026-06-12 (AR-04): rg -i "prose|verbose|narrative|return.*(report|prose)"
    across .agents/workflow-overlay, plus a "subagent|return|prose" sweep of
    source-loading.md. No conflicting language — every prose/verbose hit governs
    human-facing CHAT output (communication-style.md, decision-routing.md,
    validation-gates.md), complementary to this agent-facing return rule. No
    prior rule permitted prose subagent returns.
  non_claims:
    - not validation
    - not readiness
    - not approval or acceptance
    - not source-of-truth promotion
    - delegated review findings are decision input only, not a bound-lane verdict
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The subagent return-shape contract (prompt-orchestration.md, the
    subagent-contract owner) now also covers execution / source-changing
    subagents — ones that edit, install, commit, push, or open a PR. Their
    schema-bound return must additionally carry lifecycle-verification fields
    (branch, base and commit SHA, push/PR state, `merged` state) plus a
    per-surface change list with one file:line cite each, so the dispatching CA
    verifies the durable target on a fresh read per AGENTS.md rather than trust a
    `done`. A raw diff dump is not a substitute (it is a prose dump in another
    form), and `merged` must reflect observed state, never an assumption.
    Additive extension of the orientation/research return rule directly above; it
    binds only the return shape and leaves load-side ownership unchanged.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-of-truth.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/communication-style.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Routes subagent detail to the owning overlay file; the rule lives in
        prompt-orchestration.md, so no root restatement is added.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The index already names prompt-orchestration.md as the subagent-contract
        owner; no new overlay section was added.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Prompt gates already defer to prompt-orchestration.md as the
        prompt-mechanics owner; single-source preserved.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        Governs human-facing chat output; the execution-return fields are
        agent-facing verification data — complementary, no conflict.
  stale_language_search: run
  stale_language_search_result: >
    rg -iE "diff dump|raw diff|merged|prose dump|execution.*subagent" across
    .agents/workflow-overlay on 2026-06-14: the only return-rule hits are the
    orientation/research rule directly above (extended here, not contradicted);
    `merged` appears nowhere else, so no surface sanctioned an unverified
    `merged` claim or a raw diff dump.
  non_claims:
    - not validation
    - not readiness
    - not approval or acceptance
    - not source-of-truth promotion
    - not implementation authorization
```

Older receipts (#1–#13) archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.

## Known Source Documents

- `README.md`: workspace entrypoint.
- `AGENTS.md`: agent operating instructions.
- `CLAUDE.md`: Claude Code instruction shim that imports `AGENTS.md`; no Forseti project authority of its own.
- `.agents/workflow-overlay/README.md`: overlay entrypoint.
- `.agents/workflow-overlay/artifact-roles.md`: Forseti artifact role bindings, permissions, freshness markers, and paired artifacts.
- `.agents/workflow-overlay/source-loading.md`: Forseti source-loading budgets, read packs, and context-bloat controls.
- `.agents/workflow-overlay/decision-routing.md`: Forseti Cynefin Routing Layer for non-trivial, ambiguous, cross-thread, delegated, doctrine-bearing, or messy-worktree work.
- `.agents/workflow-overlay/retrieval-metadata.md`: Forseti retrieval-header contract for durable human-authored workflow artifacts.
- `.agents/workflow-overlay/prompt-orchestration.md`: Forseti prompt artifact, wrapper, preflight, output mode, validation, and rerun bindings.
- `.agents/workflow-overlay/template-registry.md`: Forseti-owned prompt template registry for project-local templates.
- `.agents/workflow-overlay/product-proof.md`: Forseti buyer-proof semantics, trust-objection handling, pull signals, and product-proof non-claims.
- `.agents/workflow-overlay/communication-style.md`: Forseti response style for Chief Architect sequencing, review closeouts, and prompt handoffs.
- `.agents/workflow-overlay/delegated-review-patch.md`: provisional opt-in Delegated Review-and-Patch convention; not a bound review lane, no strict claims.
- `docs/STRUCTURE.md`: docs-folder usage guide for future agents; subordinate to this overlay if conflicts appear.
- `docs/workflows/orca_bootstrap_record.md`: Turn 6 bootstrap record.
- `docs/workflows/forseti_repo_map_v0.md`: compact repo map for source-pack selection and prompt setup.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`: retrieval-only entry map for Data Capture Spine and Source Capture Armory navigation; routes to owner sources, no source-access/validation/readiness/implementation authority.
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`: retrieval-only entry map for Judgment Spine navigation; routes to owner sources, no validation/readiness/buyer-proof/scoring/model-execution/judgment-quality authority.
- `docs/migration/import_queue.md`: read-only import queue state.
- `docs/decisions/dcp_receipts_archive_v0.md`: verbatim archive of direction_change_propagation receipts cycled out of inline storage; retrieval-only, no source authority.
- `docs/decisions/forseti_rename_migration_policy_v0.md`: rename policy binding Forseti as the canonical project/product name and Orca as the legacy alias; controls live-vs-historical rename classes and compatibility migration sequencing.
- `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`: current Forseti product thesis and value proposition (owner-ratified 2026-06-12; supersedes the earlier turn-08 thesis, retained as history).
- `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`: Judgment Spine claim-tier architecture for Product-Learning, Buyer-Proof, and Judgment-Quality evidence boundaries.
- `forseti/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md`: Judgment Spine gate ownership map for source identity, packet freeze, no-tools isolation, memorization probe, sealed output, scoring, reveal/calibration, classification, and closeout blockers.
- `forseti/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md`: JSG-08 owner contract for outcome reveal/calibration receipt shape, satisfaction states, scoring relationship, and claim caps.
- `docs/workflows/turn_08_workflow_bedrock_maximization.md`: docs-first maximization plan for `workflow-deep-thinking`, future `workflow-product-ultraplan`, and future `workflow-feature-ultraplan`.
