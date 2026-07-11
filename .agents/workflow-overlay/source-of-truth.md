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
- Single-consumption, one live instance per lane. A checkpoint exists to be consumed once; the consuming lane deletes it after recovery checks run and live state is re-established. Refresh by overwriting in place under a stable name — do not accumulate `_v2`/`_v3` copies. A checkpoint whose work has landed (committed/settled) is retired by deletion. A transport-only commit that stabilizes packet bytes for a receiver does not mean the underlying work has landed.
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
inline. When adding a third, delete the oldest inline receipt; Git and PR history
preserve it. Do not append new receipts to
`docs/decisions/dcp_receipts_archive_v0.md`: that file is frozen legacy history.
Existing archive-pointer lines may remain as historical notes, but new or changed
DCP sections do not require one. Do not create another standalone receipt file.

Cold-agent fast path: decide whether a durable rule changed; name its controlling
source; consider the baseline surfaces above; record what was updated, checked,
and intentionally unchanged; keep the receipt compact; run the diff-scoped shape
check; and report semantic evidence separately. Do not read the legacy archive
for ordinary doctrine work. Whole-repository audit is reserved for changes to
the DCP contract/checker or explicit legacy-corpus repair.

Use this receipt shape:

```yaml
direction_change_propagation:
  doctrine_changed: "<one sentence>"
  trigger: product_doctrine | architecture_doctrine | workflow_authority | validation_philosophy | review_authority | output_authority | lifecycle_boundary
  related_triggers: [] # optional discovery/routing metadata; does not reduce required checks
  controlling_sources_updated: ["<path>"]
  downstream_surfaces_checked: ["<path>"]
  intentionally_not_updated:
    - {path: "<path>", reason: "<why unchanged>"}
  stale_language_search: "<query, or not_run + why — not_run only for a purely additive change>"
  non_claims: ["not validation", "not readiness"]
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
    DCP keeps its existing receipt schema and baseline-surface accountability
    while retiring archive rotation: controlling files keep at most two inline
    receipts, delete the oldest when adding a third, and never append the frozen
    legacy archive; routine work uses diff-scoped shape/hygiene checks, while
    whole-corpus audit is maintenance-only and reports receipt-relevant counts.
  trigger: workflow_authority
  related_triggers: [validation_philosophy, lifecycle_boundary]
  controlling_sources_updated: [.agents/workflow-overlay/source-of-truth.md, .agents/workflow-overlay/validation-gates.md, .agents/hooks/check_dcp_receipt.py, .agents/hooks/check_dcp_receipt_hygiene.py, .agents/hooks/README.md, docs/decisions/dcp_receipts_archive_v0.md, docs/workflows/forseti_repo_map_v0.md]
  downstream_surfaces_checked: [AGENTS.md, CLAUDE.md, .agents/workflow-overlay/README.md, .agents/workflow-overlay/source-loading.md, .agents/workflow-overlay/decision-routing.md, .agents/workflow-overlay/artifact-folders.md, .agents/workflow-overlay/communication-style.md, .agents/workflow-overlay/template-registry.md, .github/workflows/ci.yml]
  intentionally_not_updated:
    - {path: AGENTS.md, reason: "The kernel already routes doctrine-changing work to source-of-truth.md; receipt storage mechanics stay overlay-owned."}
    - {path: .github/workflows/ci.yml, reason: "CI continues to run the same diff-scoped strict shape command; only checker output and audit scope change."}
    - {path: existing archive-pointer lines, reason: "Forward-only transition: existing pointers remain historical notes and do not authorize new archive writes."}
    - {path: legacy receipt corpus, reason: "No bulk migration or rewrite; existing receipts remain historical evidence under the unchanged schema."}
  stale_language_search: 'rg -n -i "older receipts.*archiv|receipts.*cycled out|move.*dcp_receipts_archive|append.*dcp_receipts_archive|archive pointer|missing_dcp_archive_pointer|receipt-archiving rule" AGENTS.md CLAUDE.md .agents docs/workflows/forseti_repo_map_v0.md docs/decisions/forseti_mini_god_tier_doctrine_v0.md'
  stale_language_search_result: >
    Executed 2026-07-11 after the patch. Remaining archive-pointer hits are
    historical notes in untouched DCP sections or compatibility selftest
    fixtures; the controlling contract, archive header, repo map, communication
    owner, validation owner, and checker docs now state the frozen lifecycle.
  non_claims: [not validation, not readiness, not receipt truth, not implementation authorization]
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

Legacy receipts #1–#13 remain frozen in `docs/decisions/dcp_receipts_archive_v0.md`; do not append or load them for ordinary work.

## Known Source Documents

- `README.md`: workspace entrypoint.
- `AGENTS.md`: agent operating instructions.
- `CLAUDE.md`: Claude Code instruction shim that imports `AGENTS.md`; no Forseti project authority of its own.
- `.agents/workflow-overlay/README.md`: overlay entrypoint.
- `.agents/workflow-overlay/artifact-roles.md`: Forseti artifact role bindings, permissions, freshness markers, and paired artifacts.
- `.agents/workflow-overlay/source-loading.md`: Forseti source-loading budgets, read packs, and context-bloat controls.
- `.agents/workflow-overlay/decision-routing.md`: Forseti Cynefin Routing Layer for work where uncertainty about decomposition, authority, source truth, or sequencing could materially change the next move.
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
- `docs/decisions/dcp_receipts_archive_v0.md`: frozen legacy receipt history; retrieval-only, no source authority, no new writes, and not part of ordinary doctrine work.
- `docs/decisions/forseti_rename_migration_policy_v0.md`: rename policy binding Forseti as the canonical project/product name and Orca as the legacy alias; controls live-vs-historical rename classes and compatibility migration sequencing.
- `docs/decisions/forseti_product_thesis_evidence_adjudication_v0.md`: current Forseti product thesis (owner-ratified direction 2026-07-12): evidence adjudication and decision learning, decision-relative evidence weighting as the epistemic heart, human judgment allowed before autonomous Judgment maturity, and candidate universe reset.
- `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`: superseded consumer-demand / beauty-first thesis, retained as historical product input rather than current direction.
- `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`: Judgment Spine claim-tier architecture for Product-Learning, Buyer-Proof, and Judgment-Quality evidence boundaries.
- `forseti/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md`: Judgment Spine gate ownership map for source identity, packet freeze, no-tools isolation, memorization probe, sealed output, scoring, reveal/calibration, classification, and closeout blockers.
- `forseti/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md`: JSG-08 owner contract for outcome reveal/calibration receipt shape, satisfaction states, scoring relationship, and claim caps.
- `docs/workflows/turn_08_workflow_bedrock_maximization.md`: docs-first maximization plan for `workflow-deep-thinking`, future `workflow-product-ultraplan`, and future `workflow-feature-ultraplan`.
