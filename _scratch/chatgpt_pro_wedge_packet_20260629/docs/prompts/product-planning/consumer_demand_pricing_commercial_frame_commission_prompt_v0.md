# Consumer-Demand Pricing / Commercial-Frame Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (lane commission — product planning family)
scope: >
  Commission one bounded lane to ground the commercial frame: comparable
  landscape (who sells demand/insights work to beauty operators, at what
  price shapes), a recommended price band + fixed-scope sprint definition,
  and the stall rule (N paid asks before the result is treated as
  evidence). Owner-authorized public web research. Paid-first is FROZEN by
  owner word; free-first is rejected. Output: a recommendation packet,
  adjudicated by the commissioning lane, decided by the owner. Closes gaps
  OH-2 (frame variables), OH-4 (economics), OH-5 (competitive scan), DB-3.
use_when:
  - Dispatching the pricing-lane commission (owner word 2026-06-12, "we will... need to prompt out another lane too for this. pricing. put 3 into that too").
authority_boundary: retrieval_only
status: AUTHORED_2026-06-12_AWAITING_DISPATCH
adjudication_route: ICP / product-direction lane (commissioning thread) adjudicates; owner decides the frame variables.
```

## Commission

Produce a pricing / commercial-frame recommendation packet for the first
beauty consumer-demand proof offer. The intended decision (owner's, after
adjudication): the price band and scope of the fixed-scope paid decision
sprint, and the stall rule. The frame itself is NOT open: paid-first stands.

Owner authorization basis (2026-06-12, in-thread): free-first rejected ("i
honestly dont agree with free first too, especially this kind of product");
pricing lane commissioned with sub-decision 3 folded in ("pricing. put 3
into that too"); public web research for this lane is owner-authorized by
that commissioning word.

## Frozen Versus Open

FROZEN (owner word, do not reopen):

- Paid-first fixed-scope sprint is the frame. No free-first design. At most
  one explicitly-labeled free lighthouse memo exists as an owner-only
  exception, recorded as weak-pull evidence — design nothing around it.
- The offer shape: one qualified live decision, one memo + evidence
  appendix (executive deck only per the packet's gates). Defined by the
  offer hypothesis and buyer-proof packet; not this lane's to change.

OPEN (this commission's deliverables):

1. **Comparable landscape**: who sells demand-intelligence, trend, insights,
   or decision-support work to beauty/CPG operators (agencies, trend houses
   like the social-listening and trend-forecasting vendors, boutique
   consultancies, data products), at what price shapes (project, sprint,
   subscription, retainer) and what claimed deliverables. Source every row.
2. **Recommended price band + sprint scope**: a band that clears the
   "is this real money" pull threshold (payment as true evidence) while
   staying founder-signable without procurement, for a US indie/DTC beauty
   decision owner; sprint scope in days and deliverable bounds consistent
   with the charter's bounded-manual-session rule.
3. **Stall rule N**: how many consecutive paid asks bouncing converts to
   evidence (commissioning lane's starting bid: 4-6, one full batch), and
   what the recorded interpretation is (kill-criteria-adjacent evidence,
   never a pivot-to-free).

## Start Preflight (required; `orca_start_preflight` fields)

- Read `AGENTS.md` and `.agents/workflow-overlay/README.md` fresh before any
  work (not supplied by this prompt).
- Source pack: bounded custom pack — the SOURCE-LOAD list below.
- `repo_map_decision: not_needed` — `repo_map_reason:` targets pinned below.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`; fresh worktree or
  branch off `origin/main` per the AGENTS.md isolation rule.
- Base freshness gate: pinned sources at pinned sha256 prefixes (first 16
  hex) or `BLOCKED_STALE_BASE`.
- Dirty-state allowance: fresh worktree, clean; only the deliverable new.
- Edit permission: `docs-write`, limited to the single deliverable path.
- Output mode: `file-write`.
- External source boundary: public web research IS authorized for this
  commission (owner word above) — read-only desk research under the
  measured-ToS posture (no absurd-level methods, no scraping
  infrastructure, no logins, no contacting vendors, no demos, no outreach
  of any kind). `jb` is not Orca authority.
- Source-heavy economy: this is source-heavy work. Define the source-loading
  unit as ONE comparable vendor/offering; record each unit into the
  deliverable (row + citations) before opening the next. If context
  compacts before a unit is sealed, stop per
  `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL` rules.

## Method And Source Contract (source-gated)

REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY before
`SOURCE_CONTEXT_READY`.

SOURCE-LOAD (pins = sha256 first-16-hex at authoring):

- `docs/product/product_lead/orca_offer_hypothesis_v0.md` — `E0E203488E4163C4` — the offer being priced (promise, mechanism, non-claims).
- `docs/product/product_lead/orca_product_proof_lead_charter_v0.md` — `4E861CD16CD50CA9` — Commercial Path Boundary, pull standard, bounded-manual-session rule, consulting-risk rule.
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — `732C65BEBFC31DA1` — paid-decision-sprint-level pull definition, rubric, suggested proof batch (6-8 / up to 3).
- `docs/product/product_lead/orca_claim_defense_doctrine_v0.md` — `E5CFDC40D4931411` — Row-1 claim cap: ALL externally-shaped pricing/offer language in the deliverable must be Row-1-safe ("built to", never "proven"); price the discipline and decision-risk reduction, not a proven oracle.
- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` — `42787638E6185D4A` — the buyer (US indie/DTC beauty operator door).

Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` before applying
any method, opening any web source, or recommending anything.

## Deliverable

One artifact: `docs/product/product_lead/orca_pricing_commercial_frame_recommendation_v0.md`
(PROPOSED), containing: the sourced comparable table; the recommended band +
sprint scope with reasoning anchored to the pull threshold and
founder-signability; the stall rule N + interpretation; explicit
uncertainty (what the comparables do NOT prove about willingness to pay —
nothing here is WTP evidence); and the open items only the owner can set.

## Hard Constraints

- No outreach, no vendor contact, no demos, no sign-ups, no logins.
- Row-1 claim cap on every externally-shaped sentence drafted.
- No WTP, validation, readiness, or buyer-proof claims — comparables are
  context, not evidence.
- Findings-first; the owner decides; nothing in the packet self-activates.

## Output Contract

`file-write`. On completion: write the deliverable, then return a headed
human summary (band, scope, N, top uncertainties) plus path + sha256
receipt to the commissioning thread for adjudication. If blocked, return
the precise blocker.

## Non-Claims

Not WTP proof, not validation, not commercial readiness, not pricing
authority (owner owns the decision), not outreach authorization.
`model_lane: unbound`.
