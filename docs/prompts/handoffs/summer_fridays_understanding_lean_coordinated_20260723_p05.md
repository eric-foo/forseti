# Summer Fridays Understanding — Lean Coordinated Acquire & Seal Commission p05

```yaml
retrieval_header_version: 1
artifact_role: Execution-ready cold handoff
scope: >
  Runs one Summer Fridays Understanding Turn A treatment using the default
  four-actor lean execution protocol. It does not run a standalone sibling,
  Deliver, or the later control-versus-treatment adjudication.
use_when:
  - The owner explicitly authorizes the p05 Summer Fridays treatment run.
  - A clean dedicated worktree can be bound at the exact required revision.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
stale_if:
  - The Intelligence Cycle acquisition contract or default four-actor route changes.
  - A named capture/profile interface moves or is retired.
  - The required revision no longer represents the intended treatment runtime.
```

## Prompt Preflight

```yaml
output_mode: file-write
edit_permission: docs-write
task_kind: company_understanding_acquire_and_seal
target_scope: p05 commission board, specialist terminal returns, Turn A acquisition record, acquisition seal, and arm data root
required_revision: fd20aa4e7b0c29117d097d652ea6dbeaabcbef01
revision_mode: exact
branch: codex/sf-understanding-dogfood-20260723-p05-lean-coordinated
workspace: C:\tmp\forseti-sf-understanding-dogfood-20260723-p05-lean-coordinated
data_root: C:\tmp\forseti-sf-understanding-dogfood-20260723-p05\coordinated\data
commission_board: docs/research/summer_fridays_understanding_dogfood_20260723_p05/coordinated/commission_board.md
acquisition_record: docs/research/summer_fridays_understanding_dogfood_20260723_p05/coordinated/turn_a_acquisition_record.md
acquisition_seal: docs/workflows/summer_fridays_understanding_dogfood_20260723_p05/coordinated/acquisition_seal.md
later_company_output_validation: future_only
turn_b: forbidden
lifecycle_actions: prohibited
```

This prompt is execution-ready but inert until the owner explicitly couriers it
as the authorized p05 run. Once authorized, execute directly: do not return
`PREP_ONLY`, wait for a second release message, create a sibling task, perform a
write-capability probe, or add a dispatcher/controller actor.

At launch, fresh-read the target worktree, exact revision, dirty state, and
writer state. Bind the named worktree when it is clean and at the required
revision. A launch-root mismatch alone is not a blocker. Stop on a real revision
mismatch, concurrent writer, inaccessible target, or material dirty-state
collision.

## Goal And Bound Question

Produce a decision-neutral, evidence-accountable Summer Fridays Understanding
substrate through Turn A Acquire & Seal:

> What does current public evidence show about Summer Fridays as a company and
> brand system — its proposition, owned and retailer-expressed portfolio
> architecture, markets and channels, strategic and operating motion, material
> events, customer and community response, visible concentrations and
> dependencies, contradictions, strong and weak links, and observable tensions
> warranting later Problem Framing?

```yaml
cycle_id: sf_understanding_20260723_p05_co
commission_id: sf_understanding_csb_20260723_p05_co
subject: Summer Fridays
subject_type: Brand_or_Org_identity_to_verify
phase: understanding
turn: acquire_and_seal
commission_profile: company_competitive_intelligence
time_posture: recency_first
intended_consumer: fresh-context Forseti Deliver producer and later Problem Framing
intended_use: decision-neutral company Understanding substrate
```

Maximize decision-useful completeness under the integrity floor. Compactness,
actor count, token use, elapsed time, source count, and a passing validator are
not acquisition success criteria. Every material job must be supported,
contradicted, meaningfully bounded, or honestly blocked/gapped.

## Isolation And Comparison Boundary

This is one coordinated treatment run, not another pair. The completed p04
coordinated run is the later control; do not rerun its standalone arm.

Before the p05 seal is final, no actor may read or reuse any prior Summer
Fridays prompt output, packet, report, receipt, actor return, browser history,
conclusion, hero/depth selection, gap review, acquisition record, or seal.
Historical path identity may be checked only to prevent collision. Do not expose
control paths, hashes, evidence, conclusions, or token totals to `CO0`-`CO3`.

The later comparison is observational, not a clean causal experiment: public
source state and repository capability can change between runs. The evaluator
must distinguish orchestration effects from route, runtime, and evidence-world
drift. Author its durable prompt only after the p05 record and seal exist, using
fresh hashes of both control and treatment artifacts.

## Commission-Stage Gate

Before source-heavy work:

1. Load the prompt's owning sources through the repo map.
2. Generate the company-profile commission-stage CSB at `commission_board`.
3. Set `run_boundary: COMMISSION_SEALED_PRE_SCAN`; coverage routes remain
   `not_checked` or `commissioned_not_yet_run`.
4. Run:

   ```powershell
   python -B .agents\hooks\check_commission_signal_board_output.py --profile company_competitive_intelligence --input docs\research\summer_fridays_understanding_dogfood_20260723_p05\coordinated\commission_board.md
   ```

5. Repair any finding or stop. This is the only company-output validation in
   Turn A. No company report exists yet. Manually adjudicate the acquisition
   seal after acquisition.

## Four-Actor Lean Execution

Exactly four evidence actors exist:

- `CO0`: Chief Architect, integration, durable-record owner, and seal owner.
- `CO1`: owned company/high-yield core — identity, ownership, leadership,
  proposition, claims, portfolio denominator, price/channel/geography posture,
  chronology, material events, and the official-retailer authorization outcome.
- `CO2`: unified Sephora/Ulta/Target/Amazon portfolio/retail corpus — route
  planning, grids, deterministic union/reconciliation, exact PDP baselines,
  retailer-native facts/failures, provider identity, overlap, and breadth/depth
  selection pointers. Never split retailers by actor.
- `CO3`: mandatory customer/community and selected depth — retailer reviews and
  Q&A, bounded Reddit and qualified community routes, customer language, pain
  points, objections, complaints, usage contexts, workarounds, response
  patterns, syndication ceilings, and discriminating depth checks.

`CO0` dispatches `CO1`-`CO3` together as same-root collaboration subagents.
Use thin role-specific source capsules with no full controller-history fork.
Each capsule supplies only the bound question, role jobs/ceilings, relevant
owning-source pointers, upstream terminal path, data root, output path, and
terminal return contract. Specialists create no actors/tasks and do not perform
Git lifecycle actions.

Bind these terminal paths:

```yaml
co1_terminal: docs/research/summer_fridays_understanding_dogfood_20260723_p05/coordinated/specialists/co1_company_core.md
co2_terminal: docs/research/summer_fridays_understanding_dogfood_20260723_p05/coordinated/specialists/co2_retail_corpus.md
co3_terminal: docs/research/summer_fridays_understanding_dogfood_20260723_p05/coordinated/specialists/co3_customer_community_depth.md
```

- `CO1` publishes the official-retailer authorization outcome first. A positive
  statement, typed absence, contradiction, or blocked result is a valid outcome.
- `CO2` may plan its locked retailer job set concurrently but waits for that
  published outcome before probing. The outcome informs interpretation; it does
  not cancel the required typed test of Sephora, Ulta, Target, and Amazon.
- `CO3` starts its bounded customer/community scout immediately. Its
  evidence-selected retailer depth waits only for `CO2`'s reconciled breadth and
  selection pointers.

Each specialist plans once, locks the currently deterministic jobs, and runs
compatible capture/projection work as a batch or bounded local loop without a
model turn between ordinary items. Persist per-item raw packets, provenance,
typed outcomes, and failures. Evidence-revealed material seams may add named
jobs; batching is not an evidence cap.

Each specialist writes one terminal return indexing durable artifacts,
completed/unresolved jobs, failures, seams, follow-ups, and descriptive effort.
Do not paste raw corpora into chat or send routine progress, readiness, release,
or hash handshakes. Notify `CO0` early only for an observed blocker requiring a
controller or owner decision that changes the locked work.

`CO0` waits on terminal-completion or decision-requiring-blocker events. It
fresh-reads every load-bearing cited artifact before integration, resolves an
actor-local correction in that same actor task, and alone writes the acquisition
record and seal. Only `CO0` sends user-facing run progress.

## Source And Capture Route

Use current live authority and current implemented profiles at the required
revision. Do not rediscover a route already named in the source-family README,
pin registry, recon index, or banked recipe.

1. Resolve the owned high-yield core and current publicly exposed denominator.
2. Capture and fresh-read Summer Fridays' current official authorized-retailers
   surface before retailer probing. Preserve its exact outcome and limitations.
3. Test Sephora, Ulta, Target, and Amazon as one CO2 corpus. Emit exactly one
   typed outcome per retailer:
   `GRID_CAPTURED_COMPLETE`, `GRID_CAPTURED_INCOMPLETE`, `NOT_LISTED`,
   `ROUTE_BLOCKED`, `MARKET_UNPINNED`, or `SURFACE_NOT_EXPOSED`.
4. Use the current v4.1-compatible retail capture/projection route and its live
   source-specific profiles. Try the admitted direct/no-VPN route first.
   If the observed result is non-US or blocked and current route authority
   permits the owner-authorized US VPN fallback, use it once and preserve both
   the pre-VPN result and post-VPN result. VPN state is transport posture, never
   evidence.
5. Capture each available grid, deterministically union and reconcile exact rows
   with owned candidates, return to owned evidence to close the publicly exposed
   denominator and typed gaps, and capture one full-raw baseline PDP for every
   reconciled exact non-bundle listing.
6. Use retail portfolio onboarding, depth selection, review linkage, and an
   implemented retailer onboarding runner through their current live
   interfaces. Preserve duplicate placements, variants, bundles/sets,
   ambiguity, unmatched rows, missing variants, and route failures distinctly.
7. `CO3` always runs the bounded community scout, even after prior zero yield.
   Expand depth only for a named, non-duplicative job with positive expected
   decision value.

ZIP `10001`, when a live profile requires or optionally accepts it, binds only
retailer-visible local delivery, shipping, pickup, or fulfillment context. It
does not bind the US-facing catalog and cannot support nationwide stock,
availability, distribution, authorization, or absence. `.com`, USD, VPN, and
`NOT_LISTED` also cannot support those nationwide claims. Amazon completeness is
limited to the declared query and reachable ranked-search window.

## Stopping, Escalation, And Seal

Continue while another lawful, safe, non-dominated route has materially positive
expected value for an unresolved material job. Stop only when every material
seam is supported, contradicted, meaningfully bounded, or honestly blocked.

Issue one consolidated owner-unblock escalation only when a load-bearing failure
has a plausible owner action that could materially change the result:

```yaml
owner_unblock_escalation:
  affected_question_or_success_signal:
  route_attempted:
  observed_blocker:
  smallest_owner_action_needed:
  remains_blocked:
```

Write the commission board, specialist terminal returns, acquisition record,
and acquisition seal to the bound paths. The record must include actor/job
attribution, route results, receipts/provenance, denominator verification,
reconciliation/baselines, depth/linkage mappings, material seams/failures,
escalation, and descriptive effort. Specialist returns are pointers, never seal
evidence; `CO0` verifies the durable artifacts directly.

The seal may pass only when the current playbook's acquisition gate passes.
Otherwise write `BLOCKED_ACQUISITION_INCOMPLETE`, preserve the useful evidence,
and name the smallest genuine unblock. Do not author Turn B or a company report.

## Return

After fresh-reading the durable targets, `CO0` returns:

- exact revision and observed actor roster/jobs;
- commission board path and validator exit;
- three terminal return paths;
- acquisition record and seal paths;
- seal state, acquisition gate, and `deliver_allowed`;
- material failures and owner-unblock status;
- direct/no-VPN and any route-authorized VPN fallback disposition;
- observed retailer-split and contamination status;
- task/session identifiers needed for later token and inference-event accounting;
- descriptive runner/job effort; and
- observed `turn_b_started` (`true` is a phase failure).

No commit, push, PR, merge, stash, reset, clean, repository hygiene, Deliver,
control comparison, or post-run adjudication is authorized.
