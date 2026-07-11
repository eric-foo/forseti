# Research Engine P0 — Golden Thread Commission v0

```yaml
retrieval_header_version: 1
artifact_role: Research execution commission (scoped P0 work-unit; not live-capture authorization)
scope: >
  Commissions the P0 "golden thread": drive one commissioned decision from CSB
  board through Scanning to fulfilled Capture packets that are ECR-handoff-ready,
  closing the Scanning->Capture seam once, for real, and instrumenting cost.
  Rescoped per the ECR-onwards deferral: P0 STOPS at the Capture->ECR handoff
  line and does not run ECR/Cleaning/Judgment. Defines the work-unit, steps,
  acceptance, and stop conditions. Execution of live captures is a separate
  authorized turn.
use_when:
  - Executing or reviewing the P0 golden thread.
  - Checking the acceptance conditions and stop conditions for the Scanning->Capture seam-closure run.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_research_engine_god_tier_target_v0.md
  - docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md
  - docs/research/forseti_research_engine_god_tier_strategy_v0.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/capture/core/source_families/README.md
stale_if:
  - The ECR-onwards deferral is lifted (P0 then extends through ECR).
  - The capture_request lifecycle-ledger shape is owner-adjudicated differently.
  - A later commission supersedes this P0 definition.
```

## Status

`COMMISSIONED_NOT_EXECUTED` — owner-commissioned 2026-07-10 ("commission P0 ...
yes"). This record scopes the work-unit and makes it ready to run. It is **not**
live-capture, source-access, or scraping authorization; the execution turn that
performs live captures carries its own per-operation approval under the source-
access boundary and the protected-action guard.

## Objective

Prove the research engine can close its own internal loop once: a single
commissioned decision goes CSB -> Scanning -> `capture_request` -> **fulfilled,
schema-valid, hash-provenanced, ECR-handoff-ready packet**, across **>=2
independent demand-origin venue families**, with every step's cost recorded.
Success is measured on the research engine alone; ECR consumption is out of
scope (deferral record).

The expected primary output is not just packets — it is the first honest
**baseline** for the god-tier done-conditions (seam-closure rate, families-per-
case, commission->handoff-ready latency, cost per evidence-unit) and a named
punch-list of what broke.

## Work-Unit Steps

- **STEP-1 — Commission.** Use or lineage-extend an existing CSB board for a
  consumer-demand beauty/fragrance candidate under the ratified ICP. Reuse the
  Imaginary Authors board or the specialist-fragrance board rather than minting
  a new candidate unless the owner names one. Board rows must carry gate role +
  demand-origin family.
- **STEP-2 — capture_request lifecycle ledger.** Introduce the smallest durable
  ledger that gives every `capture_request` a terminal state:
  `requested -> route_bound -> captured -> handoff_ready` or
  `declined(reason)`. One append-only artifact (per-run or per-commission);
  shape to be locked via micro-decision-locking at execution time. This ledger
  is the seam-closure mechanism and the core new piece P0 builds. (Its schema is
  the one lock-in choice in P0 — surface it for owner confirmation before
  hardening; see strategy fork 2.)
- **STEP-3 — Scan.** Run a bounded MGT scan against the board across >=2
  independent demand-origin families. Candidate set (proven routes):
  fragrance-native DB (Fragrantica proven; Parfumo session route) + Reddit
  fragrance/beauty subreddits (proven API / screening-read route — the strategy
  found this proven route was never used by a scan) + retail review rows. Emit
  `capture_request`s into the STEP-2 ledger.
- **STEP-4 — Fulfil captures.** Execute each request via its proven family
  runner (separate authorized live turn). Each produced packet must pass the
  `source_capture_packet_manifest_v1` schema and carry hash provenance; the
  ledger row advances to `captured` then `handoff_ready` only when Obligation-16
  categorical-handoff-readiness is discharged. A request with no viable route
  advances to `declined(reason)` — never left `unknown`.
- **STEP-5 — Instrument.** From run one, record tokens, wall-clock, venues
  touched, requests emitted/fulfilled/declined, and packets produced. These are
  the cost baseline (strategy weakness W5).
- **STEP-6 — Stop at the boundary.** Report the packets as ECR-handoff-ready.
  Do **not** run ECR/Cleaning/Judgment (deferral record). Produce the P0
  receipt: ledger end-state, families covered, latency, cost, and the punch-list.

## Acceptance

- Every emitted `capture_request` reaches a terminal ledger state (0 left
  `unknown`).
- >=1 packet per >=2 independent demand-origin families is `handoff_ready`
  (schema-valid + hash-provenanced + Obligation-16 discharged), **or** each
  miss is a recorded `declined(reason)` with a mode-ladder receipt (not a reflex
  "blocked").
- A cost/yield row exists for the scan and each capture.
- A P0 receipt records the four baseline metrics + punch-list.

"Acceptance" here means the seam was exercised and every outcome is visible —
not that the vertical is proven or any candidate cleared. A run where most
requests end `declined(reason)` with honest receipts still *passes* P0: it
closed the loop and produced the baseline.

## Stop / Pivot Conditions

- If the ledger schema balloons past a small append-only shape, lock the minimal
  version and defer richness — do not build a registry.
- If a live capture repeatedly blocks, record the mode-ladder receipt and
  `declined(reason)`; do not spend the run defeating one venue (that is P1
  access work, not P0).
- If more than a bounded scan budget is consumed without a second independent
  family, stop and report — a single-family result is itself a finding
  (matches the strategy's convergence weakness).

## Non-Claims

Scopes a work-unit only. Not live-capture / source-access / scraping
authorization, not validation, not readiness, not buyer proof, not ECR-onwards
work, and not implementation authorization for any code root. The execution turn
carries its own approvals.
