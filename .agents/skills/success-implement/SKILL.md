---
name: success-implement
description: "Bind falsifiable success signals for an already-authorized implementation, make the smallest complete change, validate the owner-visible outcome, and ask the operator to commission delegated review-and-patch only when the remaining defect surface warrants it. Trigger only when the user explicitly invokes /success-implement or explicitly asks to use the success-implement workflow. Do not trigger for planning-only work, review-only work, or requests without implementation authority."
---

# success-implement (experimental source)

## Status and authority

This is an experimental, Forseti-local source candidate. It has controlled
paired-dogfood evidence, but is not accepted, frozen, installed, deployed, or
activated.

The skill supplies reusable implementation mechanics only. It does not supply
product facts, project authority, implementation permission, protected-action
permission, validation commands, review lanes, or lifecycle claims. Defer those
to the active repository instructions and owning sources. If the requested
outcome or implementation authority is missing, stop and name the gap.

Invocation authorizes no work beyond the user's bound request. Do not widen the
change merely to improve confidence or make review easier.

## Failure prevented

Prevent an implementation from being called successful because its code ran,
its tests passed, or its expected files exist when the owner's outcome was not
actually demonstrated. Also prevent delegated review from becoming a mandatory
ritual when the bound signals already give strong, direct evidence.

## Entry gate

Proceed only when all are true:

- the owner-requested outcome and the condition under which it must hold are
  clear;
- implementation is authorized;
- the controlling behavior sources and protected boundaries are known;
- the edit can be bounded; and
- the outcome can be observed or a missing observation can be reported
  honestly.

If a material product or design choice remains open, return that choice instead
of inventing it.

## Bind the success contract

Before editing, write a compact `SUCCESS_CONTRACT` containing:

- **Goal:** the owner-visible outcome, not the proposed implementation.
- **Authority:** the sources and instructions that control behavior.
- **Invariants:** what must remain true.
- **Non-goals:** adjacent work that is outside this unit.
- **Signals:** the observations that will distinguish success from a plausible
  near-miss.
- **Review checkpoint:** the condition for recommending delegated
  review-and-patch after validation.

Define each signal with:

```yaml
- name:
  given:
  when:
  then:
  forbidden:
  evidence:
  wrong_cause_check:
  repeat:  # only when retries, recovery, or idempotency matter
```

For a small bounded task, an equivalent compact table or paragraph is enough;
do not expand every signal into YAML when the same fields remain explicit.

Use the smallest set that covers the real outcome. A robust set normally has:

1. a positive observation at the boundary the owner cares about;
2. a negative or forbidden-path observation;
3. a perturbation that would expose a plausible false positive; and
4. a repeat, recovery, or idempotency observation when state persists or work
   may be retried.

Reject signals that only say "tests pass," "no exception," "file exists," or
"the command reported success." Those may be evidence carriers, but they are
not the owner outcome.

Turn every load-bearing outcome qualifier into a direct observation. In
particular, assert required cardinality, envelope/type, identity, ordering, and
persistence boundaries; repeating words such as "one", "exact", or "set" in
the goal does not make them observed.

## Pressure-test the signals

Before implementation:

1. Name the most plausible implementation that would pass while still failing
   the goal.
2. Ensure at least one signal rejects that near-miss.
3. Seed or simulate the target violation when practical and confirm the signal
   fails.
4. Make the wrong-cause check prove the intended boundary fails first. Avoid a
   test that passes because an earlier, unrelated guard rejected the input.
5. Capture a pre-change baseline. Prefer showing that a new signal fails before
   the fix. When the requested surface does not exist yet, record that absence
   and require a controlled post-build mutation to prove fail capability; do
   not fabricate a pre-change red result.

For an inventory, detector, matcher, or source census, also:

- name the semantic unit being counted or classified;
- seed a violation inside an already-admitted file or unit, not only as a new
  file;
- challenge at least one plausible behavior family outside the initial token
  or API vocabulary; and
- when tracked-source membership is claimed, prove ignored or untracked scratch
  cannot change the result.

If no affordable signal distinguishes the outcome from the near-miss, do not
pretend the implementation is strongly validated. Narrow the claim or stop for
the missing observability.

Once the contract and implementation-controlling seams are bound, stop source
loading and implement. Continue reading only for a concrete unresolved
authority, invariant, or validation dependency.

## Implement

Make the smallest complete intervention that satisfies the success contract.
Keep every changed line traceable to the goal, an invariant, or required
validation. Preserve real failure visibility; do not add fallback behavior that
turns an unknown or failed state into apparent success.

Follow the repository's isolation, editing, generated-file, and protected-action
rules. Do not add a registry, framework, required checklist, or standing review
step unless the bound outcome would otherwise remain false or materially
fragile.

## Validate

Run validation in this order:

1. the bound success signals;
2. focused tests for the changed behavior;
3. affected integration or contract checks; and
4. the repository's broader required gate.

Preserve each command's exit status and actual output. For long-running checks,
set the timeout from observed or historical duration, add in-command timestamps
or elapsed-time measurement, and prefer progress-visible output. Silence from a
tool wrapper is not evidence of a deadlock; distinguish command-body runtime
from tool or orchestration latency.

Re-run the near-miss or seeded violation after implementation. Record signals
that were not run and why. Structural validation does not prove deployment,
resolver activation, production readiness, or owner acceptance.

## Decide whether to request delegated review-and-patch

Recommend a de-correlated delegated review-and-patch pass when one or more of
these materially remains:

- a parser, detector, matcher, or serializer has a broad input space that the
  authored signals sample rather than exhaust;
- security, authority, privacy, destructive action, or durable-data behavior
  depends on the change;
- migration, retry, recovery, concurrency, or idempotency paths can corrupt or
  strand state;
- generated fixtures, snapshots, baselines, or proof tests are vulnerable to
  wrong-cause success;
- a material exception, authority, or identity boundary is handled but not
  directly exercised;
- cross-module invariants or a high-lock-in public contract changed; or
- validation exposed a meaningful residual that a different implementation
  family could independently attack and patch.

Do not recommend delegation merely because the change is important, non-trivial,
or eligible for review. Skip it when direct signals cover the bounded behavior,
the change is local and reversible, and no material residual above remains.

Do not dispatch a reviewer automatically. Ask the operator to commission the
pass and provide:

```yaml
DELEGATE_PATCH_RECOMMENDED:
  why:
  target_revision:
  target_scope:
  attack_surfaces:
  patch_authority:
  validation_observed:
  residuals:
  operator_request: "Please commission delegated review-and-patch against this target."
```

If not warranted, report `DELEGATED_PATCH: NOT_RECOMMENDED` with one sentence of
decisive rationale. If the operator commissions review, use the active
repository's review and prompt-orchestration rules; do not substitute
self-review.

## Closeout

Report only observed facts:

```yaml
SUCCESS_CONTRACT:
IMPLEMENTATION:
VALIDATION:
WRONG_CAUSE_CHECKS:
RESIDUALS:
DELEGATED_PATCH:
NEXT_OPERATOR_ACTION:
```

## Candidate record

- Source boundary: Forseti-local `.agents` source only; generic mechanics, not
  Forseti authority.
- Positive triggers: `/success-implement`; "use the success-implement workflow
  for this authorized fix."
- Negative triggers: planning without implementation authority; diagnosis or
  review without a requested patch; ordinary implementation that does not
  explicitly invoke this experimental candidate.
- Collision status (checked 2026-07-17): no same-name repo-local, user Codex,
  user Agents, user Claude, installed-plugin directory, or current
  resolver-visible skill was observed.
- Rollback: delete `.agents/skills/success-implement/` and remove its
  experimental candidate entry from
  `.agents/workflow-overlay/skill-adoption.md`. Do not modify user, installed,
  plugin, or external skill sources.
- Validation notes: source authoring is owner-authorized. Controlled paired
  dogfood across four historical implementation scenarios was completed on
  2026-07-18 and informed the pressure-test and review-checkpoint text.
  Structural and contradiction validation must be recorded after each change.
  Resolver activation, acceptance, and deployment are not claimed.
