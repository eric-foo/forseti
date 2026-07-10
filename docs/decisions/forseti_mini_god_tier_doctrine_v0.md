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
  - docs/decisions/forseti_venue_registry_rejection_decision_v0.md      # the rejected maximal shape
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

## Problem-Bound Target

Mini God Tier applies only after the owner-requested problem or capability has
been bound. Its maximal comparator is the maximal practical version of that
bounded capability, not a broader neighboring ambition, platform, architecture,
or risk universe.

MGT may push capability depth toward the edge of diminishing returns within
the bound target; it may not widen that target. Accepted residuals describe
foregone practical value within the bound target. Adjacent problems remain out
of scope and may carry a deferred-risk note plus an upgrade trigger when
material; they do not become MGT residuals or implementation scope unless the
owner explicitly expands the target.

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
    Forseti now binds the owner-requested problem before measuring SCI
    completeness or applying MGT; analysis, recommendations, plans, and
    methods may deepen but not redefine the problem; decision requests do not
    authorize downstream system design; proposed or executed standing
    maintenance surfaces require outcome-level necessity; and MGT's maximal
    comparator is limited to the bound capability.
  trigger: workflow_authority
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - AGENTS.md
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/communication-style.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: CLAUDE.md
      reason: >
        It remains a shim importing AGENTS.md and must not duplicate the rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index routes authority and does not own the always-on
        behavior kernel or the MGT target lens.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        The router already requires a smallest complete outcome and a
        disallowed next move; problem integrity belongs in the always-on
        behavior kernel.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading controls retrieval budgets and does not define task
        scope or MGT target selection.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Whether a component is necessary to the bound outcome is judgment-based
        and cannot be safely enforced by a deterministic checker.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        No response format or communication contract changes.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        No source route or artifact destination changes.
  stale_language_search: >
    rg -n -i "Problem Integrity|owner-requested outcome|bound outcome|decision
    request|recommended infrastructure|proposing or adding|Problem-Bound
    Target|maximal comparator|standing maintenance surface"
    AGENTS.md .agents docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    docs/workflows/forseti_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-11 on codex/problem-integrity-guard after the patch. New
    defining vocabulary is confined to AGENTS.md and this MGT decision record.
    The contradiction-oriented scan found only same-direction existing SCI,
    MGT, and decision-router scope guards; no checked downstream surface
    redefines the problem boundary or maximal comparator.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not automatic MGT invocation
```
```yaml
direction_change_propagation:
  doctrine_changed: >
    Problem Integrity now separates the owner-requested outcome from motivating
    context, anchors "false or materially fragile" to that outcome itself, and
    routes by the requested act rather than subject importance; a narrow
    negative recommendation may not become an unrequested alternative ownership
    model, operating posture, roadmap, fallback design, or improvement program.
  trigger: workflow_authority
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - AGENTS.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/communication-style.md
    - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: CLAUDE.md
      reason: >
        It remains a shim importing AGENTS.md and must not duplicate the rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index routes authority and does not own the always-on
        Problem Integrity rule.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        The router selects workflow shape after scope is bound; it does not own
        the distinction between motivating context and requested outcome.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source loading controls retrieval and does not authorize discovered
        evidence to become additional scope.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The outcome-versus-posture distinction requires judgment and cannot be
        enforced safely by a deterministic checker.
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        No response-format or communication contract changes.
    - path: docs/decisions/forseti_mini_god_tier_doctrine_v0.md
      reason: >
        Its Problem-Bound Target already prevents MGT from widening the target;
        only this propagation receipt changes in that record.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        No source route, artifact destination, or retrieval path changes.
  stale_language_search: >
    rg -n -i "context that motivated|second outcome|requested act|narrow
    read-only decision|negative recommendation|designing the alternative|
    ownership model|operating posture|allowed next move|improvement program"
    AGENTS.md .agents
    docs/decisions/forseti_mini_god_tier_doctrine_v0.md
    docs/workflows/forseti_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-11 on codex/problem-integrity-context-anchor after the
    patch. New defining vocabulary is confined to AGENTS.md and this receipt;
    checked downstream surfaces contain no conflicting permission to turn
    motivating context or discovered evidence into a second outcome.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not automatic MGT invocation
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.

Prior adoption surfaces updated 2026-06-11: `AGENTS.md` (trigger section);
`docs/decisions/venue_procedure_proving_screen_beauty_ledger_v0.md` (separate
owner-direction note, same turn). No other surface owned the original
vocabulary. Repo-map registration was deferred at adoption time because the
shared repo map carried another lane's uncommitted edits (hygiene routing).

## Non-Claims

Binds vocabulary and a decision lens only. Authorizes no build, no scope
expansion, no capability work. Not validation, readiness, or proof of any
artifact currently carrying the label.
