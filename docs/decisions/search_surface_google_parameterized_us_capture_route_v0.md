# Search-Surface Google Parameterized-US Capture Route v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Google Search-surface capture route binding for US-parameterized logged-out research.
use_when:
  - Commissioning or reviewing Google Search / SERP / search-surface capture for Orca search-surface intelligence.
  - Deciding whether a search-surface artifact can claim US-parameterized versus physically US-local locality.
  - Checking the default route for Search-Surface MGT and capture-efficacy pilots.
authority_boundary: retrieval_only
open_next:
  - .agents/hooks/check_search_surface_google_route.py
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - Orca adds a dedicated Google search-surface runner or source-capture adapter.
  - A future accepted source binds a physically US-local Google Search capture route.
  - Google Search route parameters or personalization controls materially change.
  - The search-surface pilot graduates from capture-efficacy to Judgment, Product Lead, or durable-demand proof.
```

## Decision

Default Google Search-surface capture for the current Orca pilot uses the
US-parameterized, logged-out-visible route:

- Google Search URL parameters: `hl=en`, `gl=us`, and `pws=0`.
- Use no stored Google session where practical.
- Label the route as **US-parameterized**.
- State the non-claim on every durable US-parameterized Google search-surface
  artifact: **US-parameterized is not physically US-local**.

The current proxy/VPN path is not the default route. In the live side-by-side
operator check, the parameterized route produced a visible result surface while
the proxy route produced a Google unusual-traffic block with a visible exit-IP
string. That observation is enough to avoid making proxy/VPN the default for
this capture-efficacy pilot. It is not durable proof that parameterized Google
Search is physically representative of US-local search.

## Required Boundary

Parameterized-US capture supports this claim only:

> A logged-out-visible Google Search surface was requested with US-oriented
> parameters.

It does not support these claims:

- The browser, network, or operator was physically in the United States.
- Google returned the same SERP a US-located user would see.
- The result set is market-representative, complete, stable, or sufficient.
- The result set proves durable demand, buyer pull, product readiness, Judgment
  evidence, Product Lead action, or commercial viability.

Physical locality may be claimed only when a capture packet carries separate,
observed US egress evidence and says exactly what was observed. Until then,
physical locality is not asserted.

## Proxy And VPN Escalation

Proxy, VPN, or cloud-US browser use is an explicit escalation, not a default.
Use it only when the owner or accepted commission says the decision requires
physical locality. If the route returns a Google block page with visible exit-IP
or account-sensitive material, do not preserve that page in durable Orca docs;
quarantine, redact, or leave it as scratch according to the capture lane's
source-handling rules.

This decision does not authorize a crawler, monitor, search dashboard, ranking
score, durable demand proof route, AEO/GEO product lane, or Google-specific
infrastructure.

## Code-Enforced Shell

The checkable shell is enforced by
`.agents/hooks/check_search_surface_google_route.py`, wired as:

- advisory PostToolUse hook in `.claude/settings.json`;
- advisory PostToolUse hook in `.codex/hooks.json`;
- strict diff-scoped CI gate in `.github/workflows/ci.yml`.

The checker enforces only shape:

- Google Search URLs in durable Orca docs carry `hl=en`, `gl=us`, and `pws=0`;
- US-parameterized Google search-surface artifacts include the physical-locality
  non-claim;
- Google unusual-traffic block pages with visible exit-IP content are not
  preserved in durable docs.

A passing checker is not validation, readiness, source sufficiency, demand
proof, Judgment evidence, Product Lead evidence, or physical-locality proof.

## What Code Cannot Enforce

The hook cannot prove:

- what Google actually returned to the operator;
- whether the operator was logged out;
- whether Google personalized or localized the result despite parameters;
- whether an egress path was physically US-local;
- whether the capture is sufficient for the target market or decision;
- whether the evidence should be promoted beyond capture-efficacy evaluation.

Those remain judgment and source-quality questions for Scanning, Capture,
Judgment, Product Lead, or an explicitly commissioned review lane.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now binds the default Google Search-surface capture route for the
    current search-surface pilot to US-parameterized logged-out-visible capture
    (`hl=en`, `gl=us`, `pws=0`) while forbidding silent physically-US-local,
    validation, readiness, demand-proof, Judgment, or Product Lead claims.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
    - output_authority
  controlling_sources_updated:
    - docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md
    - .agents/hooks/check_search_surface_google_route.py
    - .claude/settings.json
    - .codex/hooks.json
    - .github/workflows/ci.yml
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/README.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes project work to the overlay and permits explicit
        bounded implementation authorization. Duplicating this route rule there
        would make the agent kernel too domain-specific.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay start surface already routes enforcement placement,
        validation gates, prompt orchestration, and source hierarchy. The new
        route is discoverable through the decision record, validation-gates
        active instance, repo map, CI, and hook README.
    - path: orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
      reason: >
        This patch binds the Google search-surface pilot route only. The capture
        playbook remains the broader source-capture operating guide and should
        be updated only if the route graduates from pilot doctrine into a
        reusable Capture family procedure.
  stale_language_search: >
    rg -n "US-parameterized|physically US|Google search-surface|hl=en|gl=us|pws=0|VPN|proxy"
    docs .agents orca
  non_claims:
    - not validation
    - not readiness
    - not demand proof
    - not Judgment evidence
    - not Product Lead evidence
    - not physical-US locality proof
    - not a crawler, monitor, dashboard, score, or durable search infrastructure
```
