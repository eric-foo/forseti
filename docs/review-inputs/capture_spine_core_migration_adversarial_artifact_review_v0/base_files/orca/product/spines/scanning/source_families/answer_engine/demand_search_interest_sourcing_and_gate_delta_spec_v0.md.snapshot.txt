# Demand Search-Interest + Answer-Engine (AEO) Source-Class & Gate-Read Delta Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (PROPOSED — search-interest + answer-engine (AEO) demand-signal SOURCE-CLASS selection + gate-read placement delta). Consumes the durability capture machinery; does not fork it. Not doctrine, not validation, not readiness.
scope: >
  Settles the PROPOSED source CLASSES and the demand-gate read-placement for
  search-interest and answer-engine (AEO) visibility — NOT the concrete sources
  (those stay owner-gated, AR-04). Covers: the two decision products and the
  Core/Satellite wall (with a query-set taint rule), the surface→gate mapping
  (incl. the AEO scan-schema dependency), the feasibility gate, and the
  owner-gated sourcing ask. Primary engine = Google AI Overviews; secondary =
  Gemini + ChatGPT (owner priorities, pending the open empirical question).
  First target sub-niche = US indie/DTC fragrance (owner-set in-thread, pending
  durable pin). Docs-first; no scrape execution; sourcing owner-gated.
use_when:
  - Settling search-interest / AEO source classes + gate placement before any capture is authorized.
  - Checking the Core/Satellite wall and the query-set taint rule (which seed may feed the blind gate).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/demand_durability_indicators/search_interest/demand_durability_indicator_search_interest_capture_profile_v0.md  # CONSUME — search-interest capture obligations/pins/comparability (authority for §6 pins)
  - orca/product/spines/capture/demand_durability_indicators/capture_envelope_durability_delta_spec_v0.md                       # CONSUME — temporal regimes, cold-start, comparability
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md         # CONSUME — capture envelope of record / obligations
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md                                            # the live Demand-Substrate Hard Gate (G1 cards, AR-04, floor/ceiling, defeater)
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md                                           # candidate-observation schema (venue_family/gate_family/costly_behavior enums)
  - orca/product/spines/scanning/admissibility_checkability/orca_demand_gate_definition_closures_proposal_v0.md                      # AR-04 unsourced-gap classification
  - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md                                          # search-interest read type (read-grammar basis)
  - orca/product/spines/capture/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md                 # access/ToS posture (capture-spine-owned)
  - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md                                          # wedge target (currently "US indie/DTC beauty or personal-care"; fragrance is a narrowing — see §2)
stale_if:
  - The capture envelope of record (obligation contract / models.py) or the scan-schema enums are amended in a way that covers these facts.
  - An owner decision adopts/narrows/rejects the search-interest or AEO source classes, or pins the fragrance sub-niche.
  - Phase 0 finds the AI-Overview observation infeasible/non-automatable (re-route AEO-primary).
```

- Status: `PROPOSED_PENDING_FEASIBILITY_AND_OWNER_ADJUDICATION` (revised after cross-family adversarial review — see §13 Review Adjudication)
- Implementation / runtime / contract-hardening / scan-schema-amendment authorized: **no**
- Sourcing authorized: **no** — owner-gated (AR-04)
- First target sub-niche: **US indie/DTC fragrance (Vertical)** — owner-set in-thread 2026-06-17; the wedge authority currently scopes "US indie/DTC beauty or personal-care," so fragrance is a **narrowing pending a durable owner-pinned record** (do not treat as wedge-sourced).
- Engine order: **Google AI Overviews (primary)** → Gemini, ChatGPT (secondary) → others out of scope. These are **owner priorities**, not proven exposure/coverage claims (see §10).
- Cross-spine pointer: this is the scanning-side source-class recon for
  search-interest/AEO; capture obligations stay in
  `orca/product/spines/capture/demand_durability_indicators/search_interest/demand_durability_indicator_search_interest_capture_profile_v0.md`,
  and demand-state interpretation routes through the taxonomy and judgment
  demand-read core.

## 1. Consume-not-fork & authority ledger (pins = sha256 first-16-hex, origin/main @ b139fa9f)

_Pins re-verified 2026-06-18 against origin/main @ b139fa9f. The four that changed
since the prior pin (`demand_durability_indicator_search_interest_capture_profile_v0.md`,
`orca_buyer_proof_packet_v0.md`, `orca_demand_scan_core_spec_v0.md`,
`orca_demand_gate_definition_closures_proposal_v0.md`) drifted only via the #236
search-lane path-rewrite — no substantive source change since this spec's derivation._

| Source | Pin | Relation |
| --- | --- | --- |
| `demand_durability_indicator_search_interest_capture_profile_v0.md` | `46823c1aec5ee07a` | CONSUME — **authority for search-interest pins/cadence/comparability** (§6 cites it; this spec adds no search-interest capture obligations). |
| `capture_envelope_durability_delta_spec_v0.md` | `afe3156a32dea4b8` | CONSUME — temporal regimes / cold-start / comparability. |
| `core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `82ff4d7517bcfd5b` | CONSUME — envelope of record; if conflict, it wins. |
| `orca_buyer_proof_packet_v0.md` | `869d63ad38155f5c` | the live Demand-Substrate Hard Gate. |
| `orca_demand_scan_core_spec_v0.md` | `4cacab489b2c8d79` | candidate-observation schema; `gate_family ∈ {review_surfaces, forums_community, search_interest, none}`, `costly_behavior ∈ {gradeable, attention_only, none}` — **no AEO value** (see §7). |
| `orca_demand_gate_definition_closures_proposal_v0.md` | `c84e9ad6439bbbbc` | AR-04 (search-interest = G1 unsourced demand-family gap, owner-owned). |
| `orca_demand_read_taxonomy_v0.md` | `5fe5c41e1036d1a2` | search-interest read type (read-grammar basis). |
| `data_capture_source_access_boundary_decision_v0.md` | `4f9dd359077bf9e1` | access/ToS posture (cite, never set/narrow). |
| `orca_icp_wedge_consumer_demand_first_v0.md` | `9e27cba9bf71cc83` | wedge target — scopes "beauty/personal-care"; fragrance is a narrowing pending pin (§2). |

## 2. Purpose & what this settles (and what it does NOT)

Search-interest is an **AR-04 G1 unsourced demand-family gap**. This spec settles:
- the PROPOSED **source classes** (which kinds of surface to read) and
- the **gate read-placement** (how each enters — or cannot yet enter — the demand gate).

It does **NOT** settle (these stay owner decisions, AR-04): the concrete sources
(named search-volume provider, marketplace/on-site source, AEO engine final
selection), sourcing authorization, or the fragrance sub-niche pin. "Settles
sourcing" would overstate AR-04 closure — it does not.

## 3. Two decision products, one wall

Orca sells *decisions*, not only demand-existence verdicts. Two distinct decisions
ride these signals; their **inputs** are walled, not their value:

- **Decision A — demand existence** (gate): *does independent demand exist, and how
  bold a bet does it license?* Inputs must be **blind / independent**. Fed by the **Core**.
- **Decision B — channel position** (AEO/GTM advisory): *given demand exists, am I
  winning the AI-answer channel for it, and should I invest there?* Inputs may be
  **first-party-seeded**. Fed by the **Satellite**.

Both are first-class outputs. The wall (§4) keeps B's first-party inputs out of A's
blind read; mixing them makes A circular.

## 4. The wall + query-set taint rule (load-bearing)

The wall is **not only at the evidence-row level**; the dangerous leak is upstream in
**query-set construction** (first-party query → LLM expansion → seed set → Core
observation (Observation) → gate-facing read). "Not demand evidence" on the final row does not stop
a tainted query from shaping the blind observation corpus. Therefore:

- **Core seed sets** are generated **only from independent public/category sources**
  (public top-search lists, the demand-read taxonomy's category grammar), **produced
  and frozen/versioned BEFORE any first-party data is read.**
- **Taint propagation:** any query, expansion, synonym, cluster, prompt, or seed
  **derived from first-party data** (brand conversion logs, CRM, first-party-seeded
  LLM expansion) is **permanently Satellite-tainted** and may **never** feed Core —
  not after aggregation, sanitization, or LLM expansion.
- **LLM-issued query discovery** may expand Core seeds **only from already-Core
  (independent) inputs**; seeded from first-party data, its output is Satellite. LLM
  queries are a discovery aid, **never demand evidence**, either way.
- **Collision disclosure:** if a Satellite query coincides with a Core query, **disclose
  the collision**; never silently promote the tainted query into Core.

The Satellite's negative case ("demand proven by conversions, but the AI doesn't
surface you") is a **visibility/risk** signal for Decision B, never a demand signal
for Decision A.

## 5. Signal model — attention-class; floor guard

Both reads are **attention/visibility-class**. The gate rule: a mention/interest
signal **caps the CEILING**; only **gradeable costly behavior clears the FLOOR**.

**Floor guard (mechanical):** every search-interest and AEO observation carries
`costly_behavior: attention_only` by default. It can clear the floor **only** if a
separate, **independently captured gate-eligible costly-behavior receipt** exists
under the existing gate — never inferred from the mention/interest itself.
First-party conversion/query data never enters Core and never clears Core's floor.

## 6. Source-class selection & read-placement (NOT a capture profile)

This section selects source classes and places their read. It is **not** a capture
profile: for search-interest, capture obligations (entity/topic pin, pull-date pin,
locale pin, normalization limits, cadence, no-magnitude-comparison rule) are owned by
the consumed `demand_durability_indicator_search_interest_capture_profile_v0.md` —
**cite it verbatim, do not restate looser versions here.**

**Search-interest classes** (read-placement; pins/comparability per the consumed profile):
- **Google Trends** — relative interest (0–100), **not absolute volume**; comparability is **constrained** (normalized values depend on the exact topic/query ID and pull date — per the consumed profile; do not claim "good comparability across terms"). Assumption: low-cost, lower-ToS-risk (not yet sourced/verified).
- **A named search-volume provider** (owner decision slot) — absolute-ish term volume; provider/method pinned at capture.
- **Marketplace / on-site search** (owner decision slot, where obtainable) — closest to purchase-intent search; access/ToS-dependent, may be unavailable.

**AEO classes** (multi-engine):
- **Google AI Overviews — PRIMARY** (owner priority). **Temporal posture: snapshot / forward-only** unless a source exposes reliable history; **`not_shown` is an observation state, not absence-of-demand**; any stale-after rule is proposed, adjudicate.
- **Gemini, ChatGPT — SECONDARY** (owner priority).
- **LLM-issued queries** — discovery aid only (§4), never demand evidence.

## 7. Surface → gate mapping (mechanical executability)

Cross-checked against the scan-core observation schema. Search-interest maps cleanly;
**AEO has no schema home and is not gate-recordable until an owner-approved scan-schema
amendment adds an answer-engine value.**

| Surface | `venue_family` | `gate_family` | `signal_layer` | `costly_behavior` | Floor | Ceiling | Temporal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Search-interest | `search_interest` | `search_interest` | `buy_side` | `attention_only` | never clears | contributes to ceiling (one origin) | short-decay |
| AEO visibility | **none today — needs owner-approved amendment (e.g. `answer_engine_surface`)** | `none` | **none today (no fitting value)** | `attention_only` | never clears | **non-origin visibility corroboration** only | snapshot/forward-only |

- **AEO placement reasoning (corrected):** AEO is **non-origin visibility corroboration**
  with `gate_family: none` — **not** "G4." The reason it is excluded from the G1
  independent-origin count is that **AEO is a distribution/surfacing layer, not a
  demand-origin venue (Venue)** (not merely "origination is un-verifiable," which must not be
  used to demote real demand families like reviews/search-interest). G4 is specifically
  **org-motion** corroboration (retail presence); AEO is not org-motion, so it is not G4.
  Calling AEO G4 — or adding any AEO scan value — requires an explicit **owner-approved
  gate + scan-schema amendment**.
- **Dependency:** until that amendment lands, AEO is recorded only as an
  out-of-schema **visibility annotation** (not a gate observation). The AEO gate-read
  delta is therefore **contingent on an owner-gated scan-schema amendment**.
- De-correlation applies to both: a branded-campaign search spike or coordinated AEO
  surfacing = **one origin**; `origination_ref`/`derived_from` carry the laundering trace.

## 8. AEO capture-observable minimum (routed to the capture lane — not owned here)

If AEO is sourced, the minimum observables an AEO capture must record are below —
framed as a **capture-lane delta routed to the capture spine** (the capture lane owns
hardening it into the envelope; this spec does not fork a profile): engine · query ·
date/time · locale · session/logged-out + personalization state · Overview fired /
`not_shown` · surfaced brands (Brand)/products (Product) · cited sources · raw preserved observable
(HTML/screenshot equivalent) · visible limitations. Route to the capture lane under
the obligation contract; do not duplicate envelope obligations here.

## 9. Phase 0 — AI-Overview feasibility/automatability gate (FIRST; itself owner-authorized)

Phase 0 requires **source observation**, so — even scoped — it needs its **own bounded
owner authorization before any live observation**; it is not covered by this docs-only
spec. With that authorization, categorical **GO** criteria:

- frozen fragrance **query set** (Core-provenance, §4);
- **pins:** US, logged-out, fixed session/method;
- **repeated captures** across sessions and dates (volatility check);
- **raw observable preserved** (HTML/screenshot equivalent);
- **Overview shown / `not_shown`** state recorded;
- **cited-source extraction**;
- **failure taxonomy** logged (bot detection, DOM change, not-shown rate);
- **source-access classified under** `data_capture_source_access_boundary_decision_v0.md`
  (its disclosable/measured-risk posture — which does **not** claim ToS/legal
  sufficiency; do not narrow it to "ToS-respecting").

Output: **GO / RE-ROUTE.** If AI-Overview capture is infeasible or non-automatable,
AEO-primary re-routes (Gemini/ChatGPT primary, or AEO drops to manual spot-check)
before the rest is committed. §§6–8 are contingent on Phase-0 GO.

## 10. Open empirical / ROI gate (deep-research → owner sourcing-authorization)

OPEN, and gates the owner's **sourcing authorization (AR-04)**, not this spec: (a) do
AI-answer mentions actually **convert** vs. classic search? (b) is **GEO/AEO efficacy**
a proven revenue driver or vendor-claimed? The engine-order and "exposure" priorities in
§6 are **owner priorities pending these answers** — not proven facts. Run deep-research
as the go/no-go input.

## 11. Owner-gated sourcing authorization ask + decision slots

After Phase-0 GO, the lane returns a recommendation for the owner to authorize
(AR-04). Owner **decision slots**:
- search-interest: Google Trends (assumed in) · **named search-volume provider** (choose) · **marketplace/on-site source** (if obtainable);
- AEO: **primary engine confirm / re-route** (post Phase-0) · secondary engines;
- **scan-schema amendment** for AEO (`answer_engine_surface`-type value) — yes/no;
- **access posture** per the boundary decision.

The lane does **not** authorize sourcing, run capture, or amend the schema itself.

## 12. (reserved)

## 13. Review Adjudication (traceability)

Revised after a **cross-family adversarial artifact review** (external, no-repo
reviewer, run against the v0 zip), home-model adjudicated 2026-06-17: **all 10 findings
accepted** (2 critical, 6 major, 2 minor) plus the smallest-complete reshape and the
mini-god-tier limitations list (§14). Key folds: query-set **taint rule** (C1); the
**AEO-not-gate-recordable** dependency, verified against the scan schema's
`gate_family` enum at `orca_demand_scan_core_spec_v0.md:340-343` (C2); **non-origin
visibility corroboration** relabel (M1); §6 demoted from capture-profile to
source-selection (M2); Phase-0 self-authorization + GO criteria (M3); "source classes,
not sourcing" honesty (M4); floor guard (M5); ledger + fragrance-pending-pin (M6);
overclaims → assumptions (m1); AEO temporal posture (m2). M2↔capture-delta reconciled in
§8 (routed delta, not a forked profile). Advisory review; no formal verdict adopted.

## 14. Visible Limitations (mini-god-tier — mandatory named foregone slice)

Accepted ceilings (named, not silently dropped):

1. **No AEO query-volume truth** — engine query volumes unobserved; search-interest is only a coverage heuristic, not volume-equivalence.
2. **No AEO independence proof** — surfacing-layer; cannot count as an independent demand origin (and is not gate-recordable until amended).
3. **No floor clearance from search/AEO** — mentions/interest/Overview surfacing are attention-class only.
4. **No first-party data in the blind gate** — converting queries, CRM, analytics, conversion attribution are Satellite-only.
5. **No conversion/ROI validation** — whether AI-answer mentions convert / drive revenue is OPEN.
6. **No causal channel measurement** — does not measure whether an AI answer caused a purchase/switch.
7. **No full engine coverage** — AI Overviews primary; Gemini/ChatGPT secondary; other engines out of scope.
8. **No exhaustive personalization matrix** — narrow posture (US, logged-out, fixed method); device/account/location variance unmapped.
9. **No historical AEO corpus** — snapshot/forward-only unless reliable history appears.
10. **No durable-demand call from a snapshot** — durability needs over-time observation; these only affect the ceiling.
11. **No numeric scoring engine** — weighting stays qualitative/in-session.
12. **No full query-universe coverage** — Core seed set is a bounded category proxy.
13. **No marketplace/on-site guarantee** — access-dependent, may be unavailable.
14. **No source authorization** — no vendors/APIs/scraping/automation/capture-runs authorized.
15. **No legal/data-rights sufficiency claim** — access stays under the boundary decision.
16. **No schema hardening by itself** — new fields / the AEO scan value require separate owner-controlled amendment.
17. **No dashboard/feed/monitor/source-system** — decision-artifact input only.
18. **No broad-market claim** — first target is narrow (US fragrance); proves nothing across all beauty/non-US/non-fragrance.
19. **No buyer-proof/readiness claim.**
20. **No maximal GEO advisory product** — the Satellite audits channel position for known converting queries; it is not a full GEO optimization/attribution suite.

## Non-claims

Method/decision-prep only — no validation, readiness, proof, buyer-proof, sourcing
authorization, capture authorization, scan-schema-amendment authorization, or
implementation authorization. PROPOSED until owner word + Phase-0 GO. Mentions ≠ demand;
first-party seed never enters the blind gate; deep-research efficacy is OPEN.
`model_lane: unbound`.
