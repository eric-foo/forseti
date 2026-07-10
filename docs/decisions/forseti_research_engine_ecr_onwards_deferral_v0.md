# Research Engine Focus — ECR-Onwards Deferral v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner sequencing decision; scope focus, not a taxonomy change)
scope: >
  Records the owner decision (2026-07-10) to focus active work on the research
  engine's three extraction spines (CSB, Scanning, Capture) and to defer active
  ECR / Cleaning / Judgment / buyer-proof work for now. States what stays in
  scope (both research-engine-internal seams and the Capture->ECR handoff as a
  boundary obligation), what is deferred, the rationale, and the upgrade
  trigger. A prioritization/sequencing decision only; it does not retire,
  rename, or re-authority any downstream spine.
use_when:
  - Deciding whether a proposed unit of work is in-scope research-engine work or deferred downstream work.
  - Checking why the god-tier target and P0 stop at the Capture->ECR handoff line.
  - Confirming that ECR/Cleaning/Judgment code and docs are deferred, not deleted or superseded.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_research_engine_god_tier_target_v0.md
  - docs/research/forseti_research_engine_god_tier_strategy_v0.md
  - docs/workflows/forseti_research_engine_map_v0.md
  - docs/workflows/ecr_spine_submap_v0.md   # the deferred downstream front door (kept, not retired)
stale_if:
  - The owner directs active ECR/Cleaning/Judgment work to resume.
  - The research-engine -> ECR boundary (the group's end) moves.
  - A later owner decision supersedes this sequencing.
```

## Status

`OWNER_SEQUENCING_DECISION_V0` — owner-directed 2026-07-10 on the research-engine
strategy lane ("we're talking about the research engine only for now (CSB,
Scanning, Capture); ECR onwards, let's defer"). Sequencing/prioritization only.
Not validation, not readiness, not a taxonomy change, not a retirement of any
downstream spine.

## The Decision

Active work focuses on the three extraction spines — **CSB, Scanning, Capture**
— as grouped by `docs/workflows/forseti_research_engine_map_v0.md`. **ECR,
Cleaning, Judgment, the shared Data Lake's downstream consumption, and buyer
proof are deferred**: not invested in, extended, or gated on right now.

This is a decision about *where effort goes next*, not about what the pipeline
*is*. The research-engine map already fixes the taxonomy (the group ends at the
Capture->ECR handoff); this record adds only the owner's sequencing choice on
top of that taxonomy.

## In Scope (stays active)

- **CSB, Scanning, Capture** capability, per the god-tier target
  (`docs/decisions/forseti_research_engine_god_tier_target_v0.md`).
- **Both research-engine-internal seams**: CSB->Scanning (commission consumed by
  a scan) and **Scanning->Capture** (the `capture_request` lifecycle — emitted
  to fulfilled/declined). The open Scanning->Capture seam is the in-scope half
  of strategy weakness W1 and is explicitly NOT deferred.
- **The Capture->ECR handoff as a boundary obligation**: a captured packet must
  be made provably handoff-ready (schema-valid, hash-provenanced, obligation-16
  discharged). Making a packet *ready to hand over* is Capture's job and stays
  in scope. What is deferred is ECR actually *consuming* it and everything after.

## Deferred (paused, not retired)

- ECR derivation (SP-1/2/3/6, SP-5 finalization, EvidenceUnit binding) and its
  code under `forseti-harness/ecr/`, `forseti-harness/evidence_binding/`,
  `forseti-harness/signal_content/`.
- Cleaning (all per-source adapters under `forseti-harness/cleaning/`) and the
  catch-up runners feeding it.
- Judgment (claim ladder, JSG-01 conductor, demand-read) beyond its current cap.
- Buyer proof and any commercial-readiness gate.

Deferred means **kept and unchanged**: their front doors, code, tests, and
decision records remain valid and are not deleted, superseded, or edited by this
decision. A cold reader should treat them as paused, resumable, and still
authoritative for their own domains. The two stacked commercial gates
(ECR-to-JSG-01; judgment anti-leak) are unaffected — they simply are not being
worked toward in this window.

## Rationale

1. The engine's binding constraint is upstream: capture supply already exceeds
   downstream consumption (a real captured packet sits unconsumed), and the
   Scanning->Capture seam has never closed. Investing downstream before the
   upstream loop closes builds on an unproven foundation.
2. Downstream (ECR/Cleaning) code is exercised only by synthetic fixtures; it
   will fail on first contact with real packets. That is best discovered *after*
   the engine can reliably produce real, handoff-ready packets — which is the
   in-scope work — not before.
3. Focus reduces WIP across lanes and keeps the god-tier target bounded and
   verifiable.

## Upgrade Trigger

Resume active ECR-onwards work when the research engine can reliably produce
fresh, multi-venue-family, handoff-ready packets on commission (i.e. the P0
golden thread closes and the god-tier done-conditions trend green) — or on an
explicit owner direction to resume sooner. At that point the deferred
downstream punch-list (ECR on real vertical packets, Cleaning invocation) is
the natural next lane.

## Non-Claims

A sequencing decision only. Not validation, not readiness, not a taxonomy or
authority change, not a retirement, deletion, or supersession of any downstream
spine, and not implementation authorization. It does not weaken any downstream
gate; it defers work toward them.
