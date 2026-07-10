# Batch 1 Decision-Gate Economics Pilot

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Temporary binding for measuring decision-gate economics across implementation-bound decisions.
use_when:
  - Recording a closed implementation-bound decision in the Batch 1 pilot.
  - Interpreting decision-gate outcomes, comparability, or closeout thresholds.
  - Retiring or changing the temporary pilot.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/process_improvement_batch1/README.md
  - .agents/workflow-overlay/source-of-truth.md
stale_if:
  - The owner changes the Batch 1 sample, outcome vocabulary, or retirement boundary.
  - Any measured method changes its entry or claim contract.
```

## Active pilot rule

The owner activated this temporary pilot on 2026-07-11. It measures the
decision economics of `workflow-deep-thinking`, `workflow-assumption-gate`,
and the `fused` ENTRY decision in one evidence ledger across closed,
implementation-bound decisions.

The three methods are independent observations, never a mandatory execution
chain. A case may use one, several, none, or have unknown use. `fused_entry`
means only the fused implementation-scoping entry decision; it does not mean
that the whole fused pipeline ran or that implementation succeeded.

This pilot changes no trigger for any measured method. `AGENTS.md` remains the
owner of triggered-only pre-build gates.

## Case contract

Every case uses this shape:

```yaml
case_id: DG-00
decision_label: ""
implementation_bound: yes | no | unknown
original_route: ""
load_bearing_assumption: ""
gate_method_use:
  deep_thinking:
    status: used | not_used | not_applicable | unknown
    evidence_pointer: path:line | unknown
  assumption_gate:
    status: used | not_used | not_applicable | unknown
    evidence_pointer: path:line | unknown
  fused_entry:
    status: used | not_used | not_applicable | unknown
    evidence_pointer: path:line | unknown
outcome: confirmed | route_changed | build_blocked | scope_reduced | false_positive | unknown
avoided_rework_evidence:
  observation: ""
  evidence_pointers:
    - path:line
  counterfactual_amount: unknown
incremental_minutes: non_negative_integer | unknown
downstream_reversal:
  status: yes | no | unknown
  evidence_pointer: path:line | unknown
exact_evidence_pointers:
  - path:line
comparability:
  status: comparable | not_comparable | unknown
  reason: ""
```

The outcome values mean:

- `confirmed`: the load-bearing assumption was checked and the original route
  remained materially unchanged.
- `route_changed`: the check changed the implementation shape or dependency
  route.
- `build_blocked`: the check stopped the proposed build.
- `scope_reduced`: the check preserved the route but removed material scope.
- `false_positive`: later source evidence shows the gate materially changed or
  blocked a route unnecessarily. Mere lack of observed benefit is not a false
  positive.
- `unknown`: current evidence cannot support one of the other values.

## Evidence and comparability

Use exact repository `path:line` pointers or an equally exact durable source
identity for every load-bearing non-`unknown` value. Do not reconstruct minutes,
method use, or downstream non-reversal from memory or silence:

- `incremental_minutes` is an observed or contemporaneously recorded
  non-negative integer; otherwise it is `unknown`.
- `downstream_reversal.status: no` requires affirmative downstream evidence.
  Absence of a visible reversal remains `unknown`.
- `avoided_rework_evidence` records the source-visible abandoned or changed work
  shape. It does not prove causality, time saved, or the counterfactual amount.

A case is `comparable` only when:

1. `implementation_bound` is `yes`;
2. `original_route` and `load_bearing_assumption` are source-backed;
3. at least one method-use status is known and source-backed;
4. `outcome` is not `unknown` and is source-backed; and
5. the exact evidence pointers resolve.

Unknown incremental minutes or downstream reversal do not by themselves make a
case non-comparable. Retain non-comparable cases only when their gap is useful;
they never increment the closeout sample.
`comparability.status` and the workflow record's observed count are cached
routing assessments, not self-certifying completion fields. At closeout, the
Chief Architect must fresh-read every counted case, resolve its evidence
pointers, and re-derive the five criteria above. A stale or failed pointer
removes the case from the count; the recorded status or count never clears the
threshold by value alone.

## Sample, closeout, and retirement

- Closeout becomes eligible at eight comparable cases.
- The pilot hard-stops at twelve comparable cases.
- Continuing from eight toward twelve requires a recorded reason tied to
  method or outcome coverage; do not add cases merely to fill slots.
- If a closeout attempt has fewer than six comparable cases, stop the economics
  comparison and pivot to a qualitative decision-delta/conformance audit.
- Six or seven comparable cases may support only an insufficient-sample
  closeout, not a comparative economics conclusion.
- At eight to twelve comparable cases, synthesize the ledger for an owner
  keep/change/stop decision.
- After that owner decision, retire or amend this temporary rule through the
  Doctrine Change Propagation Contract. Do not leave it resident indefinitely.

There is no CI notifier, automatic owner ping, permanent automation, or runtime
model routing for this pilot.

## Seed boundary and non-claims

The initial ledger contains only the two source-backed historical cases named
by the owner: EP-34 session-HEAD and the LinkedIn live-envelope route change.
Do not add other retrospective cases without the same case contract.

This pilot is measurement only:

- not proof that a method caused a better decision;
- not a requirement to invoke any measured method;
- not validation, readiness, approval, or implementation authority;
- not a model-quality comparison or runtime-model routing rule;
- not authority for a later process batch or enforcement substrate.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    A temporary Batch 1 decision-gate economics pilot now measures
    deep-thinking, assumption-gate, and fused ENTRY use in one non-mandatory
    evidence ledger, with exact-source cases, bounded outcome vocabulary,
    honest unknowns, an eight-to-twelve comparable-case closeout, and explicit
    insufficient-sample and retirement boundaries.
  trigger: workflow_authority
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/batch1-decision-gate-economics.md
    - .agents/workflow-overlay/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/batch0-process-pilot.md
    - docs/decisions/forseti_doctrine_index_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/process_improvement_batch1/README.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already makes deep-thinking, assumption-gate, micro-decision
        locking, and precompact triggered-only; this pilot measures use and
        changes no trigger.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        The overlay index and repo map provide a bounded route to the pilot; no
        global source pack or read budget changes.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The pilot adds no deterministic gate, hook, CI check, or
        self-certifying completion field.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        Review authority and adjudication are unchanged; this pilot measures
        decision-gate use rather than adding a review lane.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        No prompt family, output mode, or method-sequencing contract changes.
    - path: .agents/workflow-overlay/batch0-process-pilot.md
      reason: >
        Batch 0 continues counting under its own receipt contract; Batch 1
        neither replaces nor changes it.
  stale_language_search: >
    rg -n -i "decision-gate economics|fused ENTRY|mandatory.*(deep-thinking|assumption-gate)|eight.*twelve comparable"
    AGENTS.md .agents/workflow-overlay docs/workflows docs/decisions/forseti_doctrine_index_v0.md
  stale_language_search_result: >
    Executed 2026-07-11 after edits. Live hits are the new pilot owner,
    its overlay/doctrine/repo-map routes, the workflow ledger, and the search
    command recorded in this receipt. No checked live source mandates the three
    methods as a chain or states a conflicting comparable-case threshold.
  non_claims:
    - not validation or readiness
    - not proof of causal process value
    - not a mandatory gate chain
    - not runtime model routing
    - not permanent automation
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
