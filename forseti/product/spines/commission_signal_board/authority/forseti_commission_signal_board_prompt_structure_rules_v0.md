# Forseti Commission Signal Board Prompt Structure Rules v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt Structure Rules
scope: >
  Durable rules for the Commission Signal Board Prompt Structure: the board is
  a signal and evidence routing structure, not a gate, demand check, proof step,
  classifier, retrieval process, or implementation authorization.
use_when:
  - Checking the durable rules behind the Commission Signal Board Prompt Structure.
  - Checking which prompt sections are adopted, modified, deferred, or rejected under the evidence/signals-only boundary.
  - Preparing owner sign-off on commission signal-board naming, source-routing, and classifier handoff.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md
  - forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
stale_if:
  - The owner chooses a different durable name for the commission signal/evidence object.
  - A later Commission Signal Board Prompt Structure supersedes this rules doc.
  - A demand-classifier handoff contract supersedes this evidence/signals-only boundary.
```

## Start Preflight

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S2 product anchor plus target prompt, adjacent classifier/proof context, and historical gate-named artifacts
  edit_permission: docs-write
  target_scope: product-lead Prompt Structure Rules artifact; no prompt artifact, no implementation, no runtime authorization
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-loading, prompt-orchestration, buyer-proof packet, adjacent demand/gate context artifacts, temporary prompt
```

## Decision Question

Should the temporary file
`C:/Users/vmon7/AppData/Local/Temp/orca_commission_gate_prompt (1).md`
become a durable Level 1 commission prompt, be rewritten through Forseti prompt
orchestration, or be deferred?

## Owner Correction

The commission object should not be a **gate**.

The commission object should be a **signal board**: a structured evidence and
signal surface that organizes what is known, where it came from, how strong or
weak the signal coverage is, what contradicts it, and what remains missing.

It should not decide whether demand exists. The demand-classification layer owns
the demand check. Commission should prepare clean evidence and signal inputs for
that layer, not pre-judge them.

This means the commission output should be a board or packet of signals, not an
`admit` / `hold` / `fail` verdict.

## Adjudication

Do **not** install the temporary prompt as-is.

Use it as a strong decision-prep draft for a future signal-board prompt, but
strip out the gate semantics. The valuable parts are source routing, mode/cutoff
discipline, provenance discipline, creator/non-creator separation, redirect
rules, and output shape. The wrong parts are any demand decision, pass/fail
gate, proof claim, or classifier-like judgment.

The recommended direction is:

- Adopt **Commission Signal Board** as the working object name unless the owner
  picks a better noun.
- Commission owns evidence and signals only: collect, route, tag, compare,
  preserve provenance, expose conflicts, and name gaps.
- The demand classifier owns demand judgment.
- Buyer-proof and client-facing claims remain downstream and separately gated.
- Durable prompt authoring still goes through prompt-orchestration.

Current prompt amendment: the durable CSB prompt now records recency/currentness
as source-route attention metadata (`recency_status` and `recency_attention`).
The manual/local CSB validator now enforces those row-shape fields and enum
values, but only as output shape: same-strength newer/current URL-backed rows
can deserve more scan attention, and that attention is not buyer proof, demand
classification, classifier mapping, evidence weighting, or graph weight.

Current prompt amendment (2026-07-17): the company competitive-intelligence
completion ledger now carries commission-stage vocabulary. A company board
sealed before its scan uses `run_boundary: COMMISSION_SEALED_PRE_SCAN` — valid
only while the coverage ledger still contains `not_checked` rows — and may set
`reddit_scout_status` / `quora_scout_status` to `commissioned_not_yet_run` at
that stage only. This exists so a truthful pre-scan commission never has to
borrow the completed-report boundary (origin: adversarial-review finding AR-07
against the Tower 28 Phase 1 commission). It changes lifecycle vocabulary only:
no scan, capture, classification, or proof semantics change, and a completed
company report must still carry earned checked/blocked scout values.
Each completion-ledger scout value must agree with its corresponding coverage
row's status and yield; the completion ledger cannot claim a checked, blocked,
pending, or not-required result that the coverage ledger does not show.

Public-reaction engagement belongs in the board as resonance context, not
judgment. CSB may ask rows to preserve source-visible upvotes, helpful votes,
likes, views, shares, comment counts, reply counts, score state, visible
sort/rank/order, pinned/hearted/official-response markers, direction, visible
audience-fit basis, baseline context, and discount reasons when supplied or
source-backed. CSB must not turn those facts into demand proof, Commit/Scale
support, credibility, independence, graph weight, classifier mapping, final
resonance weight, or Action Ceiling.

The temporary prompt is too high-lock-in to adopt wholesale because it mixes
five different objects in one artifact: commission intake, venue playbook,
source registry, forecast-target schema, and graph retrieval schema. Installing
that bundle as authority would silently decide product, Judgment, Data Capture,
and prompt-packaging questions that are not all settled.

## Company Competitive-Intelligence Extension

The canonical representation is:

```yaml
mode: backtest | forward
commission_profile: standard_signal_board | company_competitive_intelligence
time_posture: recency_first | longitudinal
```

These axes are orthogonal. A one-company subject whose identity is a Brand or
Org defaults to `company_competitive_intelligence`, including when the
Brand/Org identity remains unresolved. Preserve one-company-at-a-time:
comparators may interpret the subject, but deep competitor treatment requires a
separately named follow-up commission.

`recency_first` is the universal default. It uses the deterministic `0-30`,
`31-90`, `91-180`, and `>180` day ladder. `longitudinal` is an explicit
override only for change, recurrence, or trajectory across a declared period,
and it requires both the period and rationale. A named event is a route or
query inside the selected posture. Historical observations may be primary only
inside the declared longitudinal period and must never be relabeled current.

The one-company report is decision-neutral. Its required lenses are observable
positioning; offerings and claims; markets and channels; recent strategic and
operating moves; customer and community response; bounded competitor or
substitute context; contradictions; and evidence gaps. It must not infer pain,
buyer, ICP, priority, urgency, willingness to pay, outreach, offer, or wedge.

Every included CSB item must perform a named, decision-material information job:
it must have a credible route to changing the action, action ceiling, rival
assessment, or hold condition. Do not include a source, row, observation, venue,
or capture target when an equal-or-better included item performs the same job.
Structural rows that document a rejected, dominated, unavailable, or
`not_applicable` route are exclusion/accountability records, not evidence
inclusion and not completion credit.

Every material observation preserves source URL, publisher, publication date,
event date, access date, evidence status, source class, fact domain, and
syndication group. A current page is not evidence that every claim on it is a
current event. Community observations remain external/customer evidence and
cannot establish representative demand or internal company fact. Syndicated
copies are not independent corroboration.

Reddit and Quora remain explicit search-hygiene considerations in the company
coverage ledger so their selection or rejection is visible. External scouting
is commissioned only when the venue performs a named decision-material job and
is not dominated by an equal-or-better included route. Zero yield is a route
result, never completion. Generic and specialist forums use category-aware
hidden-venue discovery rather than a universal platform list. Blocked, missing,
dominated, or non-material coverage becomes a typed gap, exclusion, or
`not_applicable` record with rationale.

CSB owns profiles, source-family requirements, time posture, and typed
gaps/requests. Scanning owns intelligent-walk selection. Capture owns venue
access and preservation adapters. CSB does not contain either runtime.
Company Surface references are `candidate_only` and `not_imported`. The report
has no arbitrary length, page, source-count, or observation cap. No numeric
source, row, observation, venue, or capture target establishes completion.
CSB completion means the material information jobs and candidate routes are
defined, not that acquisition is complete or a participant packet is frozen.

For a recurring or actively radarred source family, CSB should route Scanning
or Capture to inspect the existing Data Lake before external acquisition:
relevant Silver/current view first, then packet or catalog inventory, then raw
material when necessary. This is a reuse, freshness, and coverage preflight,
not proof of current external reality. Absence from Silver is not absence from
the lake or the external world, and a missing read model does not block
external acquisition.

## Current Source State

The controlling product thesis says Forseti is outside-in consumer-demand decision
intelligence for distinguishing durable demand from transient or manufactured
demand; beauty/personal-care is the first vertical (Vertical) and the engine remains
vertical-portable (`docs/decisions/forseti_product_thesis_consumer_demand_v0.md`).

The offer hypothesis narrows the first proof offer to US-market indie/DTC beauty
or personal-care operators facing live 30-90 day consumer-demand allocation
decisions (DecisionEvent), while preserving Forseti's broader offer boundary
(`forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md`).

The buyer-proof packet binds proof requirements, not commission-board behavior.
For this commission layer, those requirements are downstream context: they say
why clean signal provenance matters, but they do not turn commission into a
proof or demand-decision surface
(`forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md`).

The current gate-run criteria and demand-scan adjudication packet are adjacent
historical/context artifacts. Under this correction, their gate language should
not be copied into the commission object. Any future durable prompt should
separate signal-board generation from demand classification
(`forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md`,
`forseti/product/spines/scanning/admissibility_checkability/forseti_demand_scan_gate_adjudication_packet_v0.md`).

Data Capture doctrine already treats source-family adaptation as satellite
work: source-family feasibility, blind spots, capture-fidelity heuristics,
threaded-community conventions, review-platform conventions, and
human-assisted-capture requirements stay source-family-specific until they
survive comparison across non-overlapping families or the owner accepts an
exception (`forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`).

Adjacent source-family records support subfamily separation. Reddit Graph
Frontier separates Reddit-native discovery surfaces from external web/SERP
discovery and keeps web-discovered subreddit candidates distinct rather than
laundering them into Reddit-source intake
(`docs/workflows/reddit_graph_frontier_b2b_marketing_traversal_record_v0.md`).
Quora has one bounded post-merge capture proof: a profile-backed CloakBrowser
Quora search-packet capture with caller-bound detail sufficiency
(`docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md`); the capture
playbook's route-maturity note treats that as bounded Quora evidence, not broad
Quora reliability, session durability, or proxy/geo proof
(`forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`).
AEO is currently non-origin visibility corroboration only, not a gate-recordable
or independent demand-origin surface
(`forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`).
Creator monitoring is designed as core machinery plus per-platform profiles:
IG fills first, while TikTok, YouTube, and Reddit creator profiles are
named-deferred seams
(`forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md`).
LinkedIn is no-live, planning-only under strict privacy rails; it is not news,
not consumer signal capture, and not live graph capture by default
(`forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md`).

Prompt policy requires any durable Forseti prompt to be authored through
prompt-orchestration or to apply that contract in full. The temporary prompt is
not yet a durable prompt artifact.

Fresh exact-term search in this worktree found no durable hits for the temporary
prompt's schema names: `commission_gate_brief`, `future_information_policy`,
`graph_family_plan`, `forecast_targets_for_downstream`, `backtesting-first`, or
`evidence_cutoff_at`. Existing code provides lower-level capture/provenance,
cutoff posture, projections, graph-frontier patterns, and action-band Judgment
scoring, but not a commission signal-board schema, runner, or output contract.

## Mini God Tier Target

Owner direction sets a **mini god tier** bar for the future commission signal
board. Under Forseti's mini-god-tier doctrine, that is a capability-target lens
with mandatory visible limitations, not a validation, readiness, proof, or scope
expansion claim (`docs/decisions/forseti_mini_god_tier_doctrine_v0.md`).

For this board, mini god tier means: most of the value of a heavier signal
intelligence and graph-prep system, at prompt-first/manual-first speed and cost.
The board should create a materially better handoff to retrieval, graph,
demand-classifier, forecasting, and judgment lanes than an unstructured scan.

Required MGT output shape (a structural contract, not a collection minimum):

- hierarchical source-family and subfamily map;
- source posture per subfamily: available now, planned lane, deferred,
  manual-only, not authorized, or noisy/deferred;
- graph retrieval brief;
- graph-ready signal rows;
- mandatory counterevidence paths;
- campaign-overlap and duplication risks;
- cutoff-safe chronology for backtests;
- visible limitations.

Visible limitations:

- not exhaustive web monitoring;
- not a standing source registry;
- not automated crawling or platform scraping authorization;
- not Discord scraping by default;
- not LinkedIn live access or relationship-graph analytics;
- not a graph database;
- not graph scoring;
- not a demand classifier;
- not buyer proof;
- not validation or readiness;
- not client-facing output.

## Source-Family Map

The source map should be hierarchical:

```text
source_family -> subfamily -> surface -> observable -> signal_role -> graph_role
```

The board should preserve subfamily identity rather than collapsing everything
into broad buckets. This avoids mixing source families with different access,
noise, provenance, independence, and graph behavior.

| Source family | Subfamilies / surfaces | Signal role / content | Capture posture |
| --- | --- | --- | --- |
| Forums / community | Reddit; Quora; category-relevant generic or specialist forums discovered for the subject | external/customer language, comparisons, objections, corrections, and response context | Keep Reddit/Quora as explicit search-hygiene considerations, but commission external scouting only for a named decision-material job with no equal-or-better included substitute. Record dominated, non-material, blocked, and zero-yield routes without treating them as completion. Other forums use category-aware hidden-venue discovery, not a fixed universal platform list. Community evidence is never representative demand or internal company fact. Execution stays with Scanning/Capture. |
| Reviews | retailer reviews, marketplace reviews, brand-site reviews, specialist fragrance reviews | experience claims, recency, complaints, repeat-use hints, contradiction checks | Do not collapse to aggregate stars; preserve recency and source conventions. |
| Creator / social video | Instagram, TikTok, YouTube, shorts/reels, affiliate/creator posts, later Reddit creator/community personalities | attention spread, creator clusters, campaign risk, audience language, propagation timing | IG has current adjacent capture/discovery work; TikTok/YouTube/Reddit creator profiles are planned/deferred seams. |
| Retail / PDP | Sephora, Ulta, Amazon, Nordstrom, brand PDPs, retailer search/category pages | availability, assortment, stock/discounting posture, review context, retailer corroboration | Retail/PDP is corroborative and operationally useful; it is not consumer-origin by itself. |
| Search / discovery | Google Trends, search-volume provider, SERP, preserved SERP packets, marketplace search, on-site search | interest traces, query language, discovery routes, hidden-venue pointers, counterevidence queries | Search-interest can carry attention/interest signal. Search-Surface MGT is a source-route scout only; methodology and pins stay with the answer-engine/search-interest source-family spec, while execution routes to Scanning frontier/exact-query work or Capture direct-source requests. |
| AEO / answer engines | Google AI Overviews, Gemini, ChatGPT, other answer-engine surfaces | answer visibility, cited-source ecosystem, entity association, visibility gaps | Visibility annotation only unless a later owner-approved schema amendment changes this; never an independent demand-origin surface today. |
| News / editorial / trade | trade publications, editorial, newsletters, specialist blogs, press | launch chronology, industry framing, awareness, third-party narrative | News is a distinct family; LinkedIn reposts of news point back to the actual source. |
| Professional / org-motion | ATS/careers pages, hiring pages, founder/executive public posts, partnership announcements, LinkedIn when explicitly routed | hiring/movement, organizational intent, operator-side propagation | ATS/careers pages are better movement sources than LinkedIn. LinkedIn remains no-live/planning-only unless separately authorized. |
| Owned channels | brand site, brand socials, email archive, product pages, press releases | official chronology, brand claims, launch framing | High chronology value, low independence. |

Answer-engine/search-interest/AEO route note: for source-class or routing questions,
open `forseti/product/spines/scanning/README.md`, then
`forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`,
then `docs/research/answer_engine/` as research/probe evidence only. Do not route
through legacy search-lane history, and do not treat AEO as product authority,
gate-recordable, validation/readiness/proof, capture authorization, scraping,
scaling, or implementation authorization.

### Search-Surface MGT Standing Route Card

Standing behavior: when a commission has an open question about market language,
comparison/confusion, hidden venues, or counterevidence queries, the board should
consider a Search-Surface MGT route row rather than leaving search discovery as
background prose.

Use this row pattern:

```yaml
source_family: search_discovery
source_subfamily: search_surface_mgt
signal_role: search_interest
row_purpose: source_route
evidence_status: provided | source_backed | to_retrieve | gap
```

CSB may point to preserved SERP packets as routing evidence, but it does not run
Google capture, score search demand, or treat query count, rank, repeated SERP
presence, PAA/PAS, product modules, or autocomplete as proof.

Preferred handoff:

```text
CSB source-route row
-> Scanning exact-query / frontier selection
-> Capture P1 direct-source acquisition when concrete URLs or surfaces exist
```

## Graph-Light Contract

Graphing belongs in the commission ecosystem, but the signal board should carry
only the lightest complete graph responsibility.

The board owns:

- seed entities;
- adjacent brands (Brand)/products (Product)/formats;
- source families and subfamilies to check;
- creator slices and planned/deferred creator platforms;
- counterevidence paths;
- node types to retrieve;
- edge types to retrieve;
- campaign-overlap and duplication checks;
- cutoff-date rule for backtesting;
- graph-ready signal rows.

The board does **not** own:

- graph construction;
- graph database or persistent graph infrastructure;
- graph scoring;
- centrality or clustering algorithms;
- evidence weighting;
- demand classification;
- forecast probabilities;
- judgment or recommendation.

Most important: **graph weight is not signal weight**.

`graph_weight` means a source or row is useful for relationships, propagation,
duplication, chronology, campaign clustering, or counterevidence routing. It
does not mean the source is strong evidence of demand. AEO can be graph-useful
while remaining non-origin visibility. LinkedIn can be graph-useful for
professional/org-motion relationships while remaining weak as consumer demand
evidence. Creator surfaces can be graph-rich while still requiring
non-creator confirmation downstream.

The future prompt should therefore separate:

```yaml
source_family: <family>
source_subfamily: <subfamily>
surface: <specific venue or route>
observable: <what can be seen>
capture_posture: available_now | planned_lane | deferred | manual_only | not_authorized | noisy_deferred
row_purpose: chronology | source_route | signal_unit | contradiction | gap | classifier_handoff | recency_priority
graph_role: seed | node_candidate | edge_candidate | propagation_path | campaign_overlap_check | counterevidence_path | none
graph_weight_hint: high | medium | low | none   # relation utility only, never signal strength
signal_role: consumer_language | review_experience | creator_attention | retail_corroboration | search_interest | aeo_visibility | org_motion | owned_claim | none
```

Two board-local clarifications keep this taxonomy from leaking into the lanes it
feeds:

- **Board labels are board-local; they are not demand-classifier families.** The
  source families and `signal_role` values above organize evidence for handoff;
  they do not map one-to-one onto the demand classifier's existing families. In
  particular, `org_motion` here means professional / hiring / partnership
  movement, with retail presence filed separately under Retail / PDP — it is
  **not** the existing G4 demand-classifier label, where "org-motion
  corroboration" refers to retail presence
  (`forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`).
  The demand classifier owns the board-`signal_role` -> classifier-family mapping; the
  board only labels and routes, consistent with the owner correction that the
  classifier owns the demand check.
- **`row_purpose` and `signal_role` are distinct fields.** In the source-family
  map, `signal_role` records the *signal content* a family yields. The schema's
  separate `row_purpose` field records the job of the row inside the board
  (`chronology | source_route | signal_unit | contradiction | gap |
  classifier_handoff | recency_priority`). A future prompt and the Owner
  Decision 2 field set should
  not conflate the two.

## Section Adjudication Matrix

| Prompt section | Decision | Rationale | Owner / next handling |
| --- | --- | --- | --- |
| 3. Required mode contract | Adopt with modification | The `backtest` cutoff and future-information exclusion are directionally right and align with zero-spoiler backtest doctrine. For a board, the mode controls evidence admissibility and chronology, not verdict authority. | Carry into future prompt as required evidence preflight; client-facing mode stays deferred. |
| 4. Intake schema | Modify | The schema is useful, but it should become a signal-board brief: candidate, decision context, time window, source families/subfamilies, known unknowns, and evidence constraints. It should not decide buyer proof or demand. | Rewrite through prompt-orchestration if owner accepts the direction. |
| 5. Gate decision / allocation | Reject gate decision; keep allocation as collection guidance | Effort allocation is search hygiene only. No ratio, count, or coverage target establishes inclusion, acquisition closure, or a demand outcome. | Rename this section in any future prompt to signal-collection allocation. |
| 6. Decision-type playbooks | Adopt as signal-route cards | The playbooks are useful venue-routing cards for fragrance/beauty cases, but they are not proof doctrine or demand-classifier logic. | Keep as route cards that identify likely signal families. |
| 7. Source registry | Adopt with guardrails | The public/repeatable/provenance admission rule fits Forseti's public-first posture and Data Capture source-family discipline. The registry should preserve family/subfamily/surface distinctions and capture posture. | Bind each source family and subfamily to capture/provenance fields before any implementation. |
| 8. Creator routing | Adopt with guardrails | Manual creator routing is acceptable for v1 and the non-creator confirmation guardrail is important. Creator evidence should be tagged by platform, origin, graph role, and relation to non-creator signals, not treated as demand proof. | Use as source routing; IG can be first, TikTok/YouTube/Reddit creator profiles stay planned/deferred until their profiles are accepted. |
| 9. Outcome labels | Defer as downstream vocabulary | The labels are valuable for forecast/evaluation design, but the signal board should prepare evidence for downstream evaluation, not score outcomes. | Owner decides whether these labels become a downstream forecast-target registry. |
| 10. Graph-family retrieval plan | Adopt as lightweight graph retrieval brief; defer graph construction/scoring | The graph vocabulary is useful and should carry graphing weight: source relationships, duplication, propagation, counterevidence, chronology, and campaign-overlap risks. Graph weight must remain separate from signal weight. | Future prompt should require graph-ready rows and a graph retrieval brief; runtime schema and graph artifact construction require separate authorization. |
| 11. Redirect and stop rules | Adopt with modification | The rules correctly prevent tunnel vision, weak provenance, campaign-cluster false positives, and unavailable private-data chases. For a board, they control evidence collection quality, not demand outcome. | Carry into future prompt as signal-collection control policy. |
| 12. Required gate output | Replace | The output should be a signal board: source-family/subfamily coverage, signal units, provenance, chronology/cutoff posture, origin/de-duplication notes, graph retrieval brief, graph-ready rows, conflicts, gaps, and classifier handoff notes. It should not output `admit`, `hold`, or `fail`. | Future prompt output contract after owner approval. |
| 13. Standalone sufficiency | Accept only as evidence/signal collection sufficiency | The prompt may be standalone enough to generate a first-pass signal board, but not enough for demand classification, buyer proof, runtime implementation, or client-facing use. | Keep the boundary explicit. |

## Owner Decisions Needed

1. Ratify or replace the working name **Commission Signal Board**.
2. Decide the required structural board fields for handoff to the demand classifier and
   graph/retrieval lanes: source-family/subfamily coverage, signal units,
   provenance, chronology, graph retrieval brief, graph-ready rows, conflicts,
   gaps, and handoff notes are the recommended schema.
3. Ratify the initial source-family/subfamily map, including ATS/careers pages
   as the preferred movement source, Reddit as a forums/community subfamily,
   AEO as visibility annotation, and Discord as noisy/deferred unless a public
   repeatable bounded slice exists.
4. Decide whether the temporary prompt's fragrance-specific playbooks are the
   first signal-board satellite or only an example deck for a broader beauty
   signal board.
5. Authorize a durable signal-board prompt artifact through
   prompt-orchestration, or explicitly defer prompt authoring.

## Recommended Owner Sign-Off Option

Recommended: **adopt-as-modified direction under the name Commission Signal
Board, do not adopt-as-is**.

This preserves the valuable parts of the prompt while avoiding four failure
modes:

- calling commission a gate;
- turning signal collection into demand judgment;
- collapsing graph weight into signal weight;
- turning search quotas or playbooks into proof rules;
- creating a graph/forecast/runtime contract before the owning lanes accept it.

If the owner accepts this option, the next authorized step is a
prompt-orchestrated durable signal-board prompt that references this packet and
the current classifier/proof boundaries. If the owner does not accept it, no
prompt artifact or implementation should be created from the temp file.

## Non-Claims

- Not owner ratification.
- Not a prompt artifact.
- Not a gate.
- Not a demand classifier.
- Not graph construction or graph scoring.
- Not buyer proof.
- Not validation or readiness.
- Not a scoring engine.
- Not implementation authorization.
- Not authorization to run a scan, capture sources, contact buyers, or produce a client-facing artifact.
- Not acquisition closure, final packet inclusion, or a frozen participant packet.
