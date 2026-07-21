# Tower 28 Phase 2 — Plan-First Commission Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Commissions a PLAN for Tower 28 Phase 2 — the decision/GTM layer over the
  Phase 1 v2 dossier. Plan only: the lane returns a plan for owner
  adjudication; nothing executes (no capture, no scanning, no outreach, no
  contract edits) until the owner rules on the returned plan.
use_when:
  - Dispatching the Tower 28 Phase 2 planning lane.
  - Adjudicating the returned Phase 2 plan.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v2.md
  - docs/decisions/forseti_ci_report_external_review_adjudication_ledger_v0.md
  - forseti/product/spines/product_lead/gtm/forseti_gtm_silent_pain_taxonomy_v0.md
  - forseti/product/spines/product_lead/gtm/forseti_gtm_indie_offensive_buyer_hypothesis_v0.md
  - forseti/product/spines/product_lead/gtm/forseti_beauty_us_problem_discovery_to_wedge_contract_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
stale_if:
  - The Phase 2 plan is returned and adjudicated (packet consumed).
  - The owner changes the Phase 2 output shape, evidence posture, or subject.
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-18 Asia/Singapore
- `created_by_lane`: Tower 28 CI/GTM lane; provenance only, not authority
- `load_rule`: confirm-don't-trust; re-verify load-bearing facts against the
  sources in `open_next`. Dispatch-critical reads first (this packet, the
  ledger's round-2 skeleton, the report's Exec Brief); read the full
  observation ledger and taxonomy classes while planning, not before.

## HARD GATE: plan first

Return a plan for owner adjudication. Do not execute any part of it —
no capture requests, no scanning, no review pulls, no outreach material, no
edits to any contract or taxonomy. Execution authorization arrives only with
the owner's ruling on the returned plan.

## What Phase 2 is (and is not)

Phase 2 consumes the decision-neutral Phase 1 v2 dossier (the live artifact,
post fix-pass) and produces the decision layer: adjudicated strategic calls
for a named reader. Phase 1 stays untouched and neutral — it is also the
Company Surface feed. Phase 2 never rewrites Phase 1 evidence; every Phase 2
claim traces to Phase 1 OBS/COV rows or to plan-approved fresh supplements.

## The plan must cover (in this order)

1. **Decision set.** Propose the concrete decisions Phase 2 will resolve,
   each named by reader, choice, and horizon. The defensive subject frame comes from
   the GTM contract; the offensive indie-buyer frame comes from the dedicated
   GTM hypothesis. Propose both Tower 28 itself and a competing/adjacent indie
   as candidate readers.
   Propose 2-4; the owner picks at adjudication. Ordering, not quota.
2. **Output shape.** Each resolved decision uses the ledger round-2 adopted
   skeleton: Decision (reader, choice, horizon) / Call / Recommended action /
   Why (which evidence combines) / Limits (what public evidence cannot
   establish) / Reversal condition (what observation would change the call).
   Comparative calls carry explicit "peer base pending" limits until pool
   Phase 1 runs land — never silently borrow strength from a missing peer
   comparison.
3. **Evidence design — decision-specific supplements only.** The contract
   rule binds: Phase 2 may request only decision-specific fresh supplements,
   never a general re-scan. Known candidates the plan should price and bind
   to named decisions (not auto-include): Reddit thread bodies (typed
   REQ-001 already exists in the v2 report); the expanded balanced review
   sampling per the ledger's coded method — sample across rating levels and
   recency; code purchase reason, outcome, switching target, claim
   confirmed/contradicted; existence never stated as rate; Quora reads.
   Every supplement names the decision it serves and what changes if it is
   skipped. All acquisition routes through the capture spine under its own
   authority.
4. **Silent-pain Tier A menu pass.** From the taxonomy (current ruling
   state), name which Tier A classes are decision-material for Tower 28
   specifically — the menu feeds runs one dish at a time, never wholesale.
   Live Tower 28 instances already flagged: class 10 diversion (the Amazon
   "RG Click Picks" second-seller thread), class 2 price-ladder, class 9
   certification directories (endpoints harvested in the capture recon
   index), class 8 SPF regulated-SKU. Each selected class states its
   first-run verification obligation (a class is verified before it is ever
   used in outreach).
5. **External-review loop.** The plan schedules the same discipline Phase 1
   used: the completed Phase 2 artifact goes to a fresh external session
   (same-vendor, fresh context) for assessment, adjudicated into the CI
   adjudication ledger before any GTM use.
6. **Consumption boundary.** GTM content (pain, buyer, wedge, outreach)
   lives in Phase 2 artifacts only — it never enters CSB reports, Company
   Surface, or the Phase 1 dossier. Claim discipline binds throughout:
   three-layer packaging, hard limits travel with findings, legality never
   characterized.

## Drift Guard

- Plan only; the hard gate above governs.
- No new standing surfaces: no monitoring, no dashboards, no registries; a
  longitudinal idea goes to the co-movement seed list as a seed, unexecuted.
- No taxonomy edits from this lane; class friction returns as typed feedback.
- Smallest complete plan: bounded supplements with named decisions beat
  exhaustive acquisition; if a decision resolves on existing Phase 1 rows,
  say so and request nothing.

## Success signal

A plan the owner can adjudicate in one pass: proposed decision set (2-4,
each reader/choice/horizon), per-decision skeleton stubs, priced
decision-bound supplement requests, the selected Tier A classes with
verification obligations, and the external-review step — with nothing
executed.
