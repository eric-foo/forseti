# Forseti Mini God Tier Doctrine v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner-adopted capability-target lens)
scope: >
  Durable home of the "mini god tier" lens: what the phrase binds when the
  owner says it, the mandatory accepted-residuals requirement, the composition
  rule with Smallest Complete Intervention, invocation authority, and claim
  guards. The AGENTS.md kernel carries the trigger phrase and points here; this
  record is the only full statement.
use_when:
  - The owner sets a "mini god tier" bar for a capability, method, or product shape.
  - Choosing between capability shapes (maximal vs bounded) for an owner-set ambition.
  - Auditing whether an artifact labeled mini god tier named its accepted residuals.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md   # kernel trigger binding ("Mini God Tier" section)
  - .agents/workflow-overlay/retrieval-metadata.md   # doctrine family: the retrievability/header-schema doctrine all durable artifacts follow
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md   # doctrine family: distillation doctrine + spine-binding index
  - forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md   # operative example (Shape C + influence widening)
  - docs/decisions/orca_venue_registry_rejection_decision_v0.md      # the rejected maximal shape
stale_if:
  - A later recorded owner decision supersedes or amends this lens.
  - The AGENTS.md trigger binding is removed or re-pointed.
```

## Status

Owner-adopted 2026-06-11, in-thread ("we can do that" + "write these down",
pre-capture discovery CA lane). Doctrine vocabulary and decision lens only —
not validation, not readiness, not a claim tier.

Owner-amended 2026-06-30 in-thread: Mini God Tier is not an 80/20 shortcut.
When the owner invokes the lens without a lower numeric bar, aim for roughly
90-95% of the practical capability value of the maximal version, while still
stopping before full-GT infrastructure, backend, migration, or maintenance
commitments consume the speed/cost advantage.

## The Lens

Mini god tier = roughly 90-95% of the maximal ("god tier") capability's
practical value at a meaningfully lower cost, speed, lock-in, and maintenance
burden -- in the owner's words, "god tier but small version so we can do most
of what god tier does at lesser / faster." It is not an 80/20 shortcut. The
target is pushed to the edge of diminishing returns, then stopped before
maximal infrastructure or maintenance burden swallows the speed/cost advantage.
The percentage is a capability-target calibration, not validation evidence or a
measured readiness claim.

Mandatory ingredient -- **accepted residuals**: the remaining foregone slice of
god tier, normally the final 5-10% of practical value or the high-lock-in
physicalization/operations work needed to reach it, is NAMED, bounded, and
consciously accepted at decision time, never quietly dropped. Each residual
states what is left undone, why that is acceptable now, what risk remains, and
what would trigger an upgrade. Without an accepted-residuals list the label is
hype, not design.

Do not call these "small limitations" unless smallness has been shown. A
residual can be material and still accepted when the value captured, speed
gained, and reversibility of a later upgrade justify leaving it unresolved for
now.

It is a high-coverage Pareto bet, not a cheap-first 80/20 bet: the accepted
residuals are the price; the cost/speed advantage is the prize. If 90-95% of
the practical value is achievable without standing infrastructure, then
standing infrastructure is not mini god tier -- it is the rejected maximal
shape (evidence pattern: the venue registry rejection vs Shape C's dated
provenance memory). If 90-95% is not achievable without full-GT infrastructure,
the correct move is to surface that tradeoff and name the residuals, not to
quietly lower the bar or quietly build the maximal substrate.

Terminology boundary: "visible limitations" remains valid operational
vocabulary where a capture, source-quality, or report row must surface missing
facts or source limits. For the Mini God Tier doctrine itself, visibility is the
reporting behavior; accepted residuals are the design requirement.

## Invocation Authority

Owner-invoked only. Agents apply the lens when the owner sets the bar — by
saying the phrase in a turn, or via a recorded owner direction for a
workstream. Agents never self-invoke it to raise targets or expand scope.

## Composition With Smallest Complete Intervention

The two rules operate on different objects and compose:

- Mini god tier chooses the TARGET (what capability bar the work aims at) —
  and only when the owner sets it.
- Smallest Complete Intervention governs every INTERVENTION toward that
  target: completeness is measured against the owner-set bar; each step stays
  minimal; lock-in tie-breaks still apply.
- Mini god tier never overrides SCI's prohibition on speculative
  infrastructure, and is never agent-grounds for exceeding a request.

## Guards

- Not a claim tier: labeling something mini god tier asserts no validation,
  readiness, or proof.
- Not an 80/20 shortcut: unless the owner sets a lower bar, the target is
  roughly 90-95% of practical capability value with accepted residuals.
- Percent language is target calibration only; do not report a numeric
  achievement percentage without independent evidence.
- The accepted-residuals list is mandatory at adoption time; silent capability
  drops void the label.
- Drift cue: "while we're at it" additions creeping toward god tier — route
  back to the owner instead of building.

## Discoverability Binding

The trigger phrase is bound in `AGENTS.md` ("Mini God Tier" kernel section),
added the same turn as this record. AGENTS.md loads in every agent session, so
the phrase cannot be missed; the kernel line points here and never duplicates
this record.

## Direction Change Propagation

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
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
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
    docs/decisions/orca_mini_god_tier_doctrine_v0.md
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
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
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
    docs/decisions/orca_mini_god_tier_doctrine_v0.md
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

Prior adoption surfaces updated 2026-06-11: `AGENTS.md` (trigger section);
`docs/decisions/venue_procedure_proving_screen_beauty_ledger_v0.md` (separate
owner-direction note, same turn). No other surface owned the original
vocabulary. Repo-map registration was deferred at adoption time because the
shared repo map carried another lane's uncommitted edits (hygiene routing).

## Non-Claims

Binds vocabulary and a decision lens only. Authorizes no build, no scope
expansion, no capability work. Not validation, readiness, or proof of any
artifact currently carrying the label.
