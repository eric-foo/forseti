# Beauty Retailer Surface Probe — Capture Spine Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Commissions the Capture spine to (1) propose a bounded, subject-agnostic
  target list of beauty retail surfaces beyond Sephora US and return it for
  owner binding, then (2) after binding, run a bounded presence/page-state
  probe per bound retailer for commissioned subjects. Exists because CI-report
  concentration synthesis currently rests on a single deep retailer read.
use_when:
  - Dispatching the Capture spine lane for the retailer-surface probe.
  - Adjudicating the returned bound-target proposal.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_ci_report_external_review_adjudication_ledger_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md
stale_if:
  - The bound target list is ratified and the probe executed (packet consumed).
  - The owner changes the retailer-agnostic posture or the US-first default.
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-17 Asia/Singapore
- `created_by_lane`: Tower 28 CI corrections lane (branch `claude/tower28-c1-corrections-c5-validator`); provenance only, not authority
- `source_baseline`: `origin/main` at `badd1189` plus PR #1054 (corrections + adjudication ledger)
- `load_rule`: confirm-don't-trust; re-verify load-bearing facts against their sources; sender claims are hypotheses, not authority

## Commission (two steps, hard-ordered)

### Step 1 — Target binding (do this first; no capture work before it)

Propose a bounded list of beauty retail surfaces that carry brands in the
Forseti beauty pool, **beyond** the already-known candidates (Sephora at
Kohl's, Credo, Mecca, Revolve) and beyond the already-read Sephora US. The
list is **subject-agnostic**: it must serve any pool company, not adhere to
Tower 28. For each proposed retailer, state:

- why its page state matters for concentration/assortment synthesis;
- the access route and expected observables (assortment breadth, price state,
  rating/review dispersion, PDP claims language);
- known access risk (e.g., Ulta's direct site read was bot-blocked in the
  Tower 28 scan — a typed negative, not proof of non-carriage).

Return the proposal for owner binding. The owner binds the list (and may
override the geographic default below) before any probe executes.

### Step 2 — Bounded probe (only after binding)

For each bound retailer and each commissioned subject: one bounded page-state
read producing SOBS-style observation rows (URL, retrieval date, quote/summary,
independence hypothesis, limits). Preservation follows the accepted trigger
rule: capture (single-file HTML preferred; full-page screenshot only when
layout itself is the evidence) only observations that are conclusion-bearing,
disputable, or likely to disappear; negatives need route + date + query only.
Bot-blocked surfaces return typed gaps, never workarounds; lawful public reads
only, no login-wall circumvention.

## Geographic posture (default, owner-overridable at binding)

US-first as the comparison spine: US retail surfaces are the deepest public
read and keep cross-company comparability inside the pool. Add one bounded
home-market read when a subject's home market differs from the US (e.g., Mecca
for an Australian subject), because concentration claims must include the
retailer set where the subject actually concentrates.

## Context pointers (re-observe in-lane before treating as evidence)

Owner-supplied screenshot (2026-07-17) of `tower28beauty.com/pages/stores`
("Stores + Sellers"): authorized retailers listed as Tower28Beauty.com, Sephora
(US, Canada, UK, Middle East + Sephora at Kohl's), CredoBeauty.com + select
Credo US stores, Mecca (Australia & New Zealand), TikTok Shop (brand official +
Revolve's official shop), Revolve.com — with anti-diversion language
("purchases made outside of these channels are not guaranteed to be
authentic"). Amazon and Ulta are absent from the authorized list, which
sharpens the open Amazon attribution-vs-listing contradiction (CSC-004 in the
Tower 28 report). This screenshot is owner-provided context, not a lane
observation: the page must be re-read in-lane (and is itself a preservation-
trigger candidate) before anything cites it.

## Subject-bound add-on tasks (owner-authorized 2026-07-18; subject: Tower 28)

Three bounded checks from the silent-pain taxonomy
(`forseti/product/spines/product_lead/gtm/forseti_gtm_silent_pain_taxonomy_v0.md`),
run with Step 2 (or standalone if binding stalls). Each produces observation
rows with the class's hard limit attached; none authorizes cart interaction.

1. **Price-ladder read (taxonomy class 2, observation half).** For 2-3 hero
   SKUs: per-unit effective price across DTC single / DTC bundle / any DTC
   subscription state vs Sephora US shelf price, read on an ordinary
   (non-event) date, same size and market, arithmetic shown. Divergence or
   its absence is the finding; no margin, redemption, or agreement claims.
2. **Certification-directory read (taxonomy class 9).** The claims Tower 28's
   own surfaces make (cruelty-free / vegan wording and any logos) vs the
   certifiers' OWN directories (Leaping Bunny; PETA Beauty Without Bunnies),
   under which entity name. Third-party tracker sites are scouting context
   only, never citable evidence. Absence in a directory is a typed
   observation, never a misconduct claim.
3. **Diversion read (taxonomy class 10).** Re-observe
   `tower28beauty.com/pages/stores` in-lane (preservation-trigger candidate,
   including its anti-diversion language), then the Amazon listing state for
   2-3 hero SKUs: distinct "sold by" sellers, first-party vs third-party,
   price vs the DTC/Sephora price. The strong form is authorized-list absence
   plus multiple independent sellers; quiet distributor authorization stays a
   named falsifier and the leak's origin/volume stays out of claim reach.

## Drift Guard

- Subject-agnostic: the target list serves the pool, not one company.
- No standing monitoring, crawler, or recurring schedule — one bounded probe.
- Assortment and page state are never demand, velocity, or sell-through.
- No new retailer-specific schema; reuse the scan receipt's observation shape.
- Capture requests stay typed; route exhaustion returns typed failure.

## Success signal

Step 1: a bound-target proposal the owner can ratify in one pass. Step 2
(post-binding): per-retailer page-state observation rows plus typed capture
receipts for preservation-triggered items, with all limits and negatives
explicit.
