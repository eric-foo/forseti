# Orca Mini God Tier Doctrine v0

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
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md   # operative example (Shape C + influence widening)
  - docs/decisions/orca_venue_registry_rejection_decision_v0.md      # the rejected maximal shape
stale_if:
  - A later recorded owner decision supersedes or amends this lens.
  - The AGENTS.md trigger binding is removed or re-pointed.
```

## Status

Owner-adopted 2026-06-11, in-thread ("we can do that" + "write these down",
pre-capture discovery CA lane). Doctrine vocabulary and decision lens only —
not validation, not readiness, not a claim tier.

## The Lens

Mini god tier = most of the maximal ("god tier") capability's value at a
fraction of its cost and speed -- in the owner's words, "god tier but small
version so we can do most of what god tier does at lesser / faster." The target
is pushed slightly past cheap or obvious gains toward the edge of diminishing
returns, then stopped before maximal infrastructure or maintenance burden
swallows the speed/cost advantage.

Mandatory ingredient -- **accepted residuals**: the remaining foregone slice of
god tier is NAMED, bounded, and consciously accepted at decision time, never
quietly dropped. Each residual states what is left undone, why that is
acceptable now, what risk remains, and what would trigger an upgrade. Without
an accepted-residuals list the label is hype, not design.

Do not call these "small limitations" unless smallness has been shown. A
residual can be material and still accepted when the value captured, speed
gained, and reversibility of a later upgrade justify leaving it unresolved for
now.

It is a Pareto bet: the accepted residuals are the price; the cost/speed
advantage is the prize. If most of the value is achievable without standing
infrastructure, then standing infrastructure is not mini god tier -- it is the
rejected maximal shape (evidence pattern: the venue registry rejection vs
Shape C's dated provenance memory).

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
    - orca/product/spines/capture/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
    - orca/product/spines/capture/source_capture_toolbox/README.md
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
    - path: orca/product/spines/capture/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
      reason: >
        The source-quality profile owns operating result tokens and the
        visible_limitations report field. Those are lower-level source/capture
        reporting vocabulary and remain valid; changing them would rewrite
        historical tokens and exceed this owner vocabulary patch.
    - path: orca/product/spines/capture/source_capture_toolbox/README.md
      reason: >
        The README indexes the source-quality operating profile and closeouts,
        whose visible-limitations terminology remains intentionally unchanged.
  stale_language_search: >
    rg -n "mini god tier|Mini God Tier|Mini God-Tier|visible limitations|accepted residual|source_quality_mini_god_tier"
    AGENTS.md CLAUDE.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
    docs/decisions/orca_mini_god_tier_doctrine_v0.md
    orca/product/spines/capture/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
    orca/product/spines/capture/source_capture_toolbox/README.md
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
