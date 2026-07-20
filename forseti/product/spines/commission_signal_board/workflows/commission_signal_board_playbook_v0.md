# Commission Signal Board And Forseti Intelligence Cycle Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow playbook
scope: >
  Operating sequence for standard signal-board and one-company competitive-
  intelligence commissions, plus the two-phase/two-turn Forseti Intelligence
  Cycle contract, without confusing CSB profiling with retrieval, capture,
  classification, or proof.
use_when:
  - Dispatching or rerunning the Commission Signal Board prompt.
  - Commissioning or executing an Understanding or Problem Framing phase.
  - Deciding whether a standard board is ready for classifier-handoff routing or a company report is mechanically complete.
  - Diagnosing validator failures on Commission Signal Board outputs.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - .agents/hooks/check_commission_signal_board_output.py
  - forseti-harness/tests/fixtures/commission_signal_board_outputs/
stale_if:
  - The Commission Signal Board prompt output contract changes.
  - The Commission Signal Board validator changes its required sections, fields, or finding codes.
  - Commission boards gain a durable artifact location or CI enforcement path.
```

- Playbook path: `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`.
- Prompt Structure path: `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md`.
- Prompt Structure Rules path: `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md`.
- Validator path: `.agents/hooks/check_commission_signal_board_output.py`.
- Validator fixture path: `forseti-harness/tests/fixtures/commission_signal_board_outputs/`.
- Current enforcement posture: manual/local checker. Not CI, not pre-commit, not a write hook.

## Purpose

This playbook keeps these objects distinct:

| Object | What it is | Validator applies? |
| --- | --- | --- |
| Intake scaffold | A request for missing commission inputs | No |
| Standard signal board | Existing standard Sections 1-10 with classifier handoff | Yes |
| Commission-stage company board | Conditional company Sections 1-10 sealed before scanning: `run_boundary: COMMISSION_SEALED_PRE_SCAN`, `not_checked` coverage rows as the commissioned scan routes, scout statuses may be `commissioned_not_yet_run` | Yes |
| Company competitive-intelligence report | Conditional company Sections 1-10 with typed ledgers, earned scout statuses, and no classifier handoff | Yes |
| Phase acquisition seal | Durable fresh-context handoff for one Intelligence Cycle phase; binds routes, receipts, provenance, failures, and acquisition-gate state | No |
| Phase deliverable | Understanding or Problem Framing synthesis produced only from a passing phase acquisition seal | Profile-dependent |
| Scanning, Capture, or classifier work | Downstream execution under its owning spine | No |

CSB owns the commission profile, source-family requirements, time posture, and
typed gaps/requests. Scanning owns the intelligent walk. Capture owns venue
access and preservation adapters. This playbook does not authorize downstream
runtime. CSB defines decision-material information jobs and candidate routes; it
does not freeze the participant packet, decide final inclusion, or declare
acquisition complete.

## Forseti Intelligence Cycle

Commission future one-company intelligence work as a **Forseti Intelligence
Cycle**. The phases are **Understanding** followed by **Problem Framing**;
`Problem` is informal shorthand only. Do not use bare `Phase 1` / `Phase 2`
language for a future commission. Historical artifacts keep their original
names and phase labels.

Each phase normally consumes two completed operator/model turns:

### Turn A — Acquire & Seal

1. Bind `cycle_id`, `commission_id`, canonical phase, phase-specific question,
   intended consumer/use, scope, and the six outcome signals below.
2. Complete prerequisite and authority checks. Generate and validate the
   phase-specific commission-stage CSB before source-heavy work.
3. Resolve the selected sources through the repo map into Scanning/Capture
   authority. Before capture starts, pin each route to the current source-family
   contract and the banked recipe card or recon-index record when one exists.
   Resolve Ulta and Quora through their existing source-specific records,
   preserving each route's scope, maturity, and typed limitations; do not
   silently substitute generic browsing or rediscovery.
4. Run authorized scanning and capture. Record every selected route, route
   result, scan/capture receipt, source/provenance locator, and real failure.
   Scanning's current MGT operating model owns continuation and closure against
   the bound phase question. Apply its lead-to-angle-to-material-seam rule:
   evidence-revealed, decision-relevant angles receive a discriminating check,
   and every material seam is supported, contradicted, meaningfully bounded, or
   honestly blocked/gapped before sealing.
5. If a material required-route or capture failure is load-bearing and a
   plausible owner action can materially unblock it, issue one consolidated
   owner-unblock escalation during the run, before sealing:

   ```yaml
   owner_unblock_escalation:
     affected_question_or_success_signal:
     route_attempted:
     observed_blocker:
     smallest_owner_action_needed:
     remains_blocked:
   ```

   This is event-triggered, not a checkpoint for every route issue. If the owner
   resolves it, resume acquisition and record the real route receipt. If it
   remains unresolved, keep acquisition blocked or record the owner's explicit
   narrowing of the commission. Never carry a fixable load-bearing capture
   failure forward merely as a final-report caveat, silently omit it, infer
   absence from it, or proceed as complete.
6. Write the phase acquisition seal below. Context compaction may discard chat,
   but not this artifact.

```yaml
phase_acquisition_seal:
  cycle_id:
  commission_id:
  phase: understanding | problem_framing
  turn: acquire_and_seal
  bound_question:
  intended_consumer:
  intended_use:
  phase_scope:
  commission_board_locator:
  outcome_signals:
    - question_fit
    - evidence_foundation
    - reasoning_quality
    - honest_uncertainty
    - implications_and_foresight
    - communication_efficiency
  resolved_routes:
    - source_or_venue:
      information_job:
      required: true | false
      route_identity:
      route_authority:
      recipe_or_recon_pointer:
      disposition: used | reused_evidence | skipped_with_rationale | blocked
  scan_receipts: []
  capture_receipts: []
  provenance_index: []
  material_gaps_and_failures: []
  seal_state: SEALED_READY_FOR_DELIVER | BLOCKED_ACQUISITION_INCOMPLETE
  acquisition_gate: pass | blocked
  deliver_allowed: true | false
  sealed_at:
```

The seal is valid for Deliver only when `seal_state:
SEALED_READY_FOR_DELIVER`, `acquisition_gate: pass`, and `deliver_allowed:
true`, and when every required route has a supported disposition and receipt or
an honestly typed blocking result. A required route that was skipped, silently
substituted, incompletely captured, or described as exhausted without the
matching route evidence forces the blocked state.

Route disposition is necessary but not sufficient. A touched lens, zero-yield
route, exhausted route list, or absence of a promotable candidate cannot
authorize Deliver. If a material seam remains unresolved because a commission
limit or source boundary stops acquisition, or if the assembled evidence cannot
support a decision-useful answer to the bound question, use
`BLOCKED_ACQUISITION_INCOMPLETE`; do not lower the answer standard to pass the
seal.

### Turn B — Deliver

Start in fresh context and load the phase acquisition seal, not the accumulated
capture chat. Verify its identity, canonical phase, bound question/use, seal
state, route receipts, provenance, and material gaps before synthesis. If the
gate is blocked or the artifact is incomplete, stop and return to Acquire &
Seal; do not issue a nominal deliverable.

Deliver compresses and communicates the acquired evidence. Its succinctness
discipline is never grounds to under-acquire during Acquire & Seal.

When the gate passes, synthesize the phase deliverable, craft the human report
or framing artifact, validate it under the owning contract, and hand off the
next phase or step. Every evidence, coverage, provenance, and route-exhaustion
claim must resolve to the seal. Preserve the final deliverable as the sealed
phase output before commissioning post-delivery review.

For Understanding, derive the prompt's optional retailer-review approval signal
only when the commissioned question gives it a named decision-material job and
the seal resolves to row-level ratings, source-visible incentive posture, and a
reproducible corpus boundary. Preserve disclosed incentivized rows in raw
capture but exclude them from the primary derived view. Report the eligible
denominator and excluded count; call unlabelled rows `not marked
incentivized`, never organic. Express both percentage fields to one decimal
using round-half-up. If the route yields only a headline aggregate or an
unreproducible slice, omit the signal and preserve the gap. This is
conditional synthesis, not a mandatory acquisition step or completion gate.

Understanding Deliver produces the decision-neutral company-intelligence
artifact. Problem Framing may acquire only decision-specific supplements to the
Understanding substrate, never a general re-scan; its eventual human output
shape remains separately review-bound and is not defined here.

Two turns are the normal operating budget, not a hard completion cap. A blocked
Acquire & Seal remains blocked and may require another acquisition attempt; it
does not count as a successful Deliver.

### Six Outcome Signals

The cycle optimizes toward these signals without turning them into a score,
required report sections, six extra gates, or repeated receipt fields:

1. **Question fit** — answer the bound question for the intended reader/use; do
   not drift toward whatever was easiest to collect.
2. **Evidence foundation** — trace load-bearing judgments to dated evidence,
   check critical independence/currentness, and record required routes and
   failures honestly.
3. **Reasoning quality** — make the evidence-to-judgment chain reconstructable;
   separate facts, assumptions, and judgments; address serious alternatives and
   disconfirming evidence when relevant.
4. **Honest uncertainty** — put confidence and material gaps where they affect
   judgments and name useful change conditions; do not force probability
   language onto descriptive facts.
5. **Implications and foresight** — explain what findings mean and which
   observable developments would change the view; do not force unsupported
   forecasts or recommendations.
6. **Communication efficiency** — make key judgments easy to find, order the
   body by importance, remove repetition/padding, and keep audit detail
   available without dominating the narrative.

Production priority:

1. **Non-negotiable foundations:** question fit, trustworthy evidence, and
   honest uncertainty. Do not trade them for prose, apparent decisiveness,
   speed, or implications. A real acquisition or evidence failure stays
   visible and may block Deliver.
2. **Primary value focus:** once the foundations hold, spend the largest
   analytical effort on sound reasoning and useful meaning/implications.
3. **Delivery discipline:** only then compress and clarify. Communication
   efficiency must not manufacture substance or dominate effort.

In one line: **optimize for decision usefulness under an integrity floor:
secure the question/evidence/uncertainty foundations; then maximize reasoning
and useful implications; then compress for clear delivery.**

Satisfy the signals through real task evidence and function, not headings,
labels, citation volume, ritual sections, forced forecasts, repeated confidence
labels, or padding. Production receives these targets and this priority order,
never numerical weights, bands, caps, or score-optimization instructions.

## Post-Delivery Adversarial Review Handoff

After a phase deliverable is sealed, commission an independent adversarial
review against the accepted post-delivery six-dimension rubric and its
applicable hard caps. The rubric authority is deferred until separately
adopted; do not reconstruct it from this production contract or create a
duplicate rubric here.

The review package must include:

- the final phase deliverable;
- the phase acquisition seal and provenance index;
- the bound question, intended consumer, and intended use;
- material gaps and failures; and
- the route receipts needed to verify evidence and exhaustion claims.

The reviewer evaluates actual function and evidence, not the presence of
headings, labels, citation volume, or ritual content, and explicitly tests for
rubric gaming. The evaluation includes the Forseti-specific rule that a report
presenting required capture routes as exhausted when the canonical route was
skipped or silently substituted is flagged as rubric gaming rather than scored
as a clean report. Any resulting numeric cap is applied only by the separately
adopted post-delivery rubric; no cap value belongs in this production contract.

Return the total number, the six-dimension profile, and all triggered flags or
caps; never return a lone number. Weights, bands, and caps remain provisional
working evaluation authority, not production instructions or a permanent
readiness gate unless separately adopted. This handoff defines only the seam
and required inputs; it does not create the numerical rubric, authorize the
reviewer to patch, or change the report layout.

## Operating Sequence

Use this sequence to create the CSB inside Acquire & Seal. The broader cycle
gate above controls whether Deliver may begin.

1. Read the prompt and this playbook.
2. Preserve `mode: backtest | forward`. Determine `commission_profile`:
   - default a one-company Brand or Org subject, including unresolved Brand/Org
     identity, to `company_competitive_intelligence`;
   - otherwise use `standard_signal_board` unless explicitly overridden.
3. Default `time_posture` to `recency_first`. Use `longitudinal` only when the
   commission explicitly asks about change, recurrence, or trajectory and
   declares both a period and rationale.
4. Check profile-specific required inputs. Return the prompt's intake scaffold
   if any are missing; intake-only output is not a validator target.
5. Include an item only when its named job can materially change the action,
   action ceiling, rival assessment, or hold condition and no equal-or-better
   included item performs that job. Use exclusion or `not_applicable` records
   for dominated routes.
6. For company commissions, route retail, customer, and claims research first,
   subject to the same named-job and substitution rules. This orders attention;
   it is not a quota, proof hierarchy, or Scanning execution instruction.
7. For a recurring or actively radarred source family, put a lake-first
   preflight in the downstream request: relevant Silver/current view, then
   packet or catalog inventory, then raw material when necessary. Treat the
   result as reuse/freshness/coverage context, not current-world proof.
8. Generate exactly the selected profile's Sections 1-10. A completed company
   report also carries the prompt-defined `## Executive Intelligence Brief`
   preamble before Section 1.
9. Save the exact output to a temporary file or bound durable artifact. For an
   Intelligence Cycle, this is the commission-board input to the phase
   acquisition seal, not the completed seal itself.
10. Run the validator. If it fails, repair the output or report its finding
   codes. Do not run downstream work from a failing report.
11. Route typed source requests to Scanning or Capture under their own
    authority. Do not execute retrieval from this playbook. Scanning decides
    marginal acquisition, dominance, and closure; Capture fulfills the bounded
    request or returns typed failure/route exhaustion.
12. For an Intelligence Cycle, assemble the phase acquisition seal only after
    the owning Scanning/Capture work returns. A typed acquisition failure
    remains visible and blocks Deliver; it is not converted into completion.

## Validator Command

From the repo root:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py <board-output-file>
```

Selftest:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
```

Focused pytest suite:

```powershell
cd forseti-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py
```

## Validator Applicability

Run the validator only against a full output with profile-specific Sections
1-10 in canonical order.

- `standard_signal_board` requires the existing `Signal Board Rows`,
  `Demand-Classifier Handoff Packet`, and `Board Status And Run Boundary`.
- `company_competitive_intelligence` requires `Company Commission And Identity
  Receipt` through `Completion Ledger And Run Boundary` and must not contain a
  classifier handoff. This includes commission-stage company boards
  (`run_boundary: COMMISSION_SEALED_PRE_SCAN`): they are full ten-section
  outputs and are validated; the validator enforces that the commission-stage
  boundary coexists with `not_checked` coverage rows and that
  `commissioned_not_yet_run` scout statuses appear only at that stage. It also
  cross-checks each Reddit/Quora scout status against the corresponding
  coverage-row status and yield so the completion ledger cannot claim a result
  the route ledger did not earn. For a completed report, the contract-required
  `## Executive Intelligence Brief` before Section 1 is compatible with the
  validator: the checker scans only numbered `###` Sections 1-10 and
  deliberately does not enforce synthesis quality.

Do not run it against `NEEDS_COMMISSION_INTAKE` or `NEEDS_CUTOFF_DATE`.

## What The Validator Checks

For `standard_signal_board`, the established structure, row vocabulary,
backtest cutoff, engagement-overclaim, and classifier-handoff checks remain
unchanged.

For `company_competitive_intelligence`, the validator checks:

- one-company identity and default profile routing;
- `mode` and orthogonal `time_posture`;
- deterministic recency tiers and age-use rules;
- declared period and rationale for `longitudinal`;
- source-family coverage, the Reddit `mandatory_bounded_scout` compatibility
  row, the initial-proving Quora compatibility row, category-aware forum
  discovery, typed gaps, and justified `not_applicable`. The Reddit/Quora rows
  are search-hygiene considerations: they may document non-selection and do not
  authorize acquisition or earn completion credit without a named
  non-dominated information job;
- observation-level URL, publisher, publication/event/access dates, evidence
  status, source class, fact domain, and syndication group;
- shared source-family vocabulary, typed `effective_time_precision` and
  `age_anchor_basis`, current-page versus dated-event separation, and no old
  evidence relabeled current;
- community evidence as external/customer evidence only;
- decision-neutral company lenses and prohibited GTM keys;
- Company Surface rows as `candidate_only` and `not_imported`;
- completion ledger, explicit gaps/requests, no arbitrary caps, typed
  `run_boundary` and `next_authorized_step`, Reddit/Quora scout-status
  consistency with their coverage rows, and no classifier handoff;
- document-wide `OBS-###` references resolve to observation-ledger rows
  (`dangling_observation_reference`);
- the shared engagement/resonance overclaim ban, which applies to both profiles.

## What A Pass Means

A standard pass means its classifier-handoff rows are mechanically eligible
under the board's own row table. A company pass means the report is mechanically
complete under the conditional company planning contract. Neither pass means:

- evidence is true;
- evidence was retrieved;
- demand exists;
- the board is exhaustive;
- graph construction is complete;
- acquisition is complete or the participant packet is frozen;
- classifier mapping is correct;
- buyer proof, validation, readiness, forecast, or client-facing claims are allowed.

## How Agents Discover This Lane

Agents should discover this playbook from:

- the Commission Signal Board prompt `open_next`;
- the repo map Product Anchor Files section;
- the repo map Active Hooks / Manual Checkers section;
- downstream wrappers or handoffs that name this playbook before board generation.

If an agent sees "Commission Signal Board", "commissioning board", or
"commission board output", it should open this playbook before running or
validating the board.

If an agent sees "Forseti Intelligence Cycle", "Understanding phase", "Problem
Framing phase", "Acquire & Seal", or "Deliver", it should open this playbook
before commissioning or executing the phase.

## Current Non-Goals

- Do not add CI or pre-commit enforcement until board artifact paths are
  standardized.
- Do not make the validator run on chat-only intake scaffolds.
- Do not turn the validator into demand classification, graph scoring, evidence
  weighting, retrieval, or proof review.
- Do not treat validator pass as approval or readiness.
- Do not implement or infer a numerical report score from the six outcome
  signals.
- Do not redesign the company-report section order while its external structure
  review remains open.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Commission Signal Board operation now routes two conditional profiles while
    preserving mode backtest|forward. Agents default one-company Brand/Org work
    to company_competitive_intelligence, default time posture to recency_first,
    use longitudinal only with period and rationale, and validate only a complete
    profile-specific output. Company reports have no classifier handoff.
  trigger: workflow_authority
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
    - forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
    - forseti-harness/tests/unit/test_commission_signal_board_output_validator.py
    - forseti-harness/tests/fixtures/commission_signal_board_outputs/
    - docs/workflows/forseti_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_commission_signal_board_output.py
    - forseti-harness/tests/fixtures/commission_signal_board_outputs/
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes Forseti project rules to the overlay and durable
        docs; adding a Commission Signal Board special case would fork the
        playbook.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The validator remains manual/local, not a CI or hook gate. The
        enforcement-placement principle already lives here; no active validation
        gate is being registered yet.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading packs are unchanged; this playbook is a run sequence for
        an existing prompt and checker.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt-orchestration mechanics are unchanged; the canonical prompt
        applies the full contract without forking prompt-policy.
  stale_language_search: >
    rg -n "Commission Signal Board|commission_signal_board|check_commission_signal_board|NEEDS_COMMISSION_INTAKE|validator target|classifier handoff"
    docs .agents forseti-harness -S
    and
    rg -n "run the validator|validator applies|manual/local|NOT hook-wired|intake-only"
    docs .agents forseti-harness -S
    (refresh during implementation validation)
  stale_language_search_result: >
    Executed 2026-07-16. The scoped profile/posture/venue/classifier search
    returned expected live-contract and non-claim hits; the exact forbidden
    posture search returned only quoted receipt literals, not live contract
    usage. Live instructions preserve the standard classifier handoff, omit it
    from company reports, and do not treat validator pass as truth, demand
    classification, proof, graph weight, recency proof, or readiness.
  non_claims:
    - not validation
    - not readiness
    - not CI enforcement
    - not pre-commit enforcement
    - not demand classification
    - not evidence retrieval
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
