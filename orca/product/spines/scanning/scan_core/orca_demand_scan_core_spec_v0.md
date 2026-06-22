# Orca Demand Scan-Core Spec v0 (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: Product method spec (PROPOSED scan core — pipeline step 2; pending commissioning-lane adjudication and owner word)
scope: >
  The method spec for Orca's scanning function: how an authorized scan walks
  a vertical's venues, recognizes decision-shaped demand situations from the
  demand-read taxonomy's demand-state model (durable / transient /
  manufactured), and emits structured candidate observations with provenance —
  in two modes (backward/backtest case-finding, forward/discovery) over one
  core grammar. Ingests the vertical/venue discovery layer; feeds capture
  (step 3) and candidate recording (step 4). Method only: authorizes no scan
  run, capture, web research, or outreach.
use_when:
  - Commissioning or running an authorized demand scan (backward or forward mode).
  - Checking what a scan hunts, what it emits, to whom, and under which mode obligations.
  - Promoting precursor signals into rich candidate observations after MGT minimum evidence is met.
  - Adjudicating this spec (commissioning ICP / product-direction lane; owner signs adoption).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md          # the hunting grammar's source (PROPOSED; 3-state model)
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md      # the walk mechanics this spec layers on
  - orca/product/satellites/beauty/beauty_venue_card_set_v0.md                # the venue layer (beauty)
  - orca/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md  # forward-mode consumer
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md            # the re-derived Demand-Substrate Hard Gate
  - docs/decisions/wind_caller_calibration_carveout_v0.md              # wind-caller naming boundary (owner-signed)
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md  # access-toolkit route for packet-grade capture walls
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md      # source-class recon catalog for access-toolkit routing
  - orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md  # search-interest/AEO source-class recon
input_hashes:
  # sha256 first-16-hex over git BLOB bytes (LF as stored; `git cat-file blob <rev>:<path>`),
  # NOT over CRLF working-tree bytes. A Get-FileHash mismatch on a CRLF checkout is not staleness.
  # Re-pinned 2026-06-16 against origin/main @ fc51291c during the re-derivation (below).
  - path: orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
    sha256_16_lf: 5FE5C41E1036D1A2
    note: >
      Re-pinned 2026-06-16 (was BC478D890419B2B6). DRIFT was substantive: the
      2026-06-14/15 owner amendments retired "hollow", introduced the
      durable / transient / manufactured demand-state model, the transient-spike
      read, the calling sequence, divergence-as-technique, the ratified pricing
      refinement, and the wind-caller naming carve-out. §1/§3/§4/§6 are
      re-derived against this text (see Status).
  - path: orca/product/satellites/beauty/beauty_venue_card_set_v0.md
    sha256_16_lf: 65E22CDAE5EDE781
    note: Unchanged since the 2026-06-13 draft.
  - path: orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
    sha256_16_lf: EF9F5C6E716E9857
    note: Unchanged since the 2026-06-13 draft.
  - path: orca/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md
    sha256_16_lf: C672C1678F98878F
    note: Unchanged since the 2026-06-13 draft.
  - path: orca/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md
    sha256_16_lf: 19009D43A7C29858
    note: Unchanged since the 2026-06-13 draft.
  - path: orca/product/spines/product_lead/icp_wedge/orca_discovery_consumer_demand_target_selection_brief_v0.md
    sha256_16_lf: DBBB59522D777934
    note: >
      Re-pinned 2026-06-16 (was 48B5534E056FD42A). DRIFT: the slot table column
      "Venue families visible (≥2 required)" became "Independent demand-venue
      origins visible" (laundered / shared-origination copies = one; org-motion /
      retail excluded), with verb-tier slot guidance and a reworded
      qualification objective #3. §3/§5 forward reconciliation re-derived.
  - path: docs/decisions/orca_product_thesis_consumer_demand_v0.md
    sha256_16_lf: 63BAE324F50016F3
    note: >
      Re-pinned 2026-06-16 (was B119E24691066E47). DRIFT: the 2026-06-14 owner
      amendment carries the same durable / transient / manufactured demand-state
      model, the never-a-feed invariant, and the wind-caller carve-out pointer.
      The costly-behavior primitive and US-first geography are unchanged.
  - path: orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
    sha256_16_lf: 05291BB682CF2FAC
    note: >
      Re-pinned 2026-06-16 (was 25EBD39AE95C3A07). DRIFT was substantive: the
      Demand-Substrate Hard Gate was re-derived (2026-06-13 P2/P3/P4 apply) to
      de-correlation-by-origination + verb-tiering by commitment; retail presence
      reclassified to G4 org-motion corroboration (excluded from the demand-origin
      count); a gradeable costly-behavior floor with floor-vs-ceiling ordering and
      a divergence defeater. §3 schema re-derived against this gate (see Status).
  - path: docs/decisions/wind_caller_calibration_carveout_v0.md
    sha256_16_lf: 9D242D774B76D083
    note: >
      Newly bound (owner-signed 2026-06-13; amended through 2026-06-15). Governs
      §6's wind-caller naming boundary: named-public-figure calibration is
      permitted for INTERNAL use only; the external/sold person-level boundary is
      unchanged.
branch_or_commit: demand-scan-core-spec-v0 @ fc51291c (origin/main); re-derived 2026-06-16
stale_if:
  - The demand-read taxonomy is owner-adjudicated with further amendments (re-derive the hunting grammar against the adjudicated text).
  - The card set, exploration guide, candidate-pool handoff, or target-selection brief is amended or superseded on a surface this spec binds.
  - The thesis or the Demand-Substrate Hard Gate is amended.
  - The wind-caller calibration carve-out is amended on the naming / internal-use / external-boundary surface §6 binds.
```

## Status

`PROPOSED_PENDING_ADJUDICATION` — first authored 2026-06-13 by the commissioned
scanning lane under
`docs/prompts/product-planning/consumer_demand_scanning_lane_commission_prompt_v0.md`
(owner authorization basis 2026-06-12, in-thread: "okay let's prompt this out
to handle - the scanning lane itself"). The commissioning ICP /
product-direction lane adjudicates; the owner signs adoption. Becomes the
operating method for both scan modes only on that word.

**Re-derived 2026-06-16 (owner-directed: "re-derive, then land").** Between the
2026-06-13 draft and this landing, the base drifted substantively on three
surfaces this spec binds, firing all three of the draft's own `stale_if`
triggers — so this is a re-derivation, not a mechanical re-pin:

- **Demand-read taxonomy** (owner-adjudicated 2026-06-14/15): retired "hollow";
  adopted the two-axis demand-state model (persistence: **durable vs transient**;
  integrity: **real vs manufactured**) yielding three actionable states; added
  the **transient-spike read** (equal billing) and the **calling sequence**;
  demoted **divergence to a recognition technique, not a verdict**; ratified the
  pricing refinement; and added the wind-caller naming carve-out. §1 (hunting
  grammar), §3 (`read_type`), §4 (modes), and §6 (wind-caller) are re-derived
  against it.
- **Demand-Substrate Hard Gate** (buyer-proof packet, 2026-06-13 apply): the gate
  moved from a raw "≥2 venue families" count to **de-correlation by origination**
  plus **verb-tiering by commitment**; **retail presence** is reclassified to G4
  org-motion corroboration (excluded from the demand-origin count); and a
  **gradeable costly-behavior floor** with floor-vs-ceiling ordering and a
  divergence defeater. §3 (the schema's gate vocabulary) is re-derived against it.
- **Thesis** (2026-06-14 amendment) and **target-selection brief** slot re-column
  carry the same model; §1/§4/§5 reconciled.

The 2026-06-13 draft's delegated adversarial review (committed alongside as a
dated record: `docs/prompts/reviews/…` + `docs/review-outputs/…`) **predates this
re-derivation and covered the prior schema** — its principle (the gate must be
mechanically checkable from the schema, not re-judged from prose) is preserved
and strengthened here (origination-keyed), but its specific remedy (a four-family
`gate_family` that included `retail_presence`) is superseded by the gate
re-derivation. A fresh adversarial review of this re-derived schema is a
reasonable next step the commissioning lane may commission.

Source-state note: the demand-read taxonomy remains
`PROPOSED_PENDING_OWNER_ADJUDICATION` — every grammar element this spec takes
from it is bound at PROPOSED strength and re-derives if the taxonomy is
adjudicated with further amendments.

## What this is — and is not

Pipeline step 2 (scanning / candidate finding) of the owner's 2026-06-12
six-step structure. A scan is a **guide-governed walk with a recognition
grammar and an emission schema bound on top**: the vertical exploration guide
owns how a walk moves (steps, caps, stop rules, Walker Equipment Kit,
provenance memory); this spec owns what the walk hunts and what it emits.

The scanning README and MGT intelligent-walk operating model are the cold-start
front door. This spec is the richer promoted-observation schema and gate-prep
surface; it should not be forced onto every precursor or low-level move.

- A scan RUNS ONLY under explicit authorization (a batch plan in backward
  mode; an authorized candidate-scan lane in forward mode). No step runs
  standing. This spec authorizes no run.
- It is NOT a monitor, registry, atlas, scraper, source map, capture
  mechanism, or standing intake — the finder frame's and guide's must-not
  boundaries carry unchanged.
- Scan evidence is screening-grade (URLs + short quotes, per the Walker
  Equipment Kit). Packet-grade capture belongs to the capture lane (step 3).
- Cross-spine dependency: unresolved access or source-class questions route to
  the capture playbook/recon index and, for search-interest/AEO, to the
  answer-engine source-class delta; the scan core consumes those pointers but
  authorizes none of them.

## 1. Hunting Grammar

What a scan recognizes, per read type from the taxonomy, per venue class from
the card set's chain (NEWSY: origination launders upward into a citable
record; SUBTLE: nothing launders — the detector IS the record).

The taxonomy's demand-state model has **two independent axes** — persistence
(**durable** vs **transient**) and integrity (**real** vs **manufactured**) —
yielding three actionable read-states. A scan does not *predict* which state a
signal will become; it recognizes the state the receipts can currently support
and tags it conservatively (see the calling-sequence rule below).

### Durable-demand read (real + persists → commit)

Trigger: at least two **effectively-independent demand-venue (Venue) origins** (§3
independence rule) moving the same direction on the same trend vector (TrendVector) or brand (Brand),
with at least one **gradeable** costly-behavior signal (sellouts, waitlists,
restock pressure, review velocity/content shifts, pain-point convergence,
dupe-seeking, switching, effortful UGC), **and receipt-visible persistence past
the trigger** — optionally corroborated by org motion in the same direction.

- NEWSY recognition: origination venues (community boards) produce the move;
  trade press corroborates or launders it; org motion (ad launches, hiring
  direction, pipeline/launch signals, retail placements) points the same way.
- SUBTLE recognition: detector or tracker record plus a community wave
  agreeing — independent detection counts as an origin distinct from the
  community discussing it.
- Durable is the **earned** state: absent receipt-visible persistence, the same
  evidence is recognized as a **transient-spike** read, not a durable one (the
  scan never opens at "durable"; calling-sequence rule below).

### Transient-spike read (real + decays → probe / monitor, time-boxed)

Trigger: real, gradeable costly behavior with a **short observed lifespan or no
persistence yet visible** — a viral surge, a time-limited dupe wave, a seasonal
pop. This is **the conservative default** for any real-demand recognition: a
transient spike and durable convergence look identical in the moment, and only
observed persistence — not an upfront guess — separates them.

- NEWSY / SUBTLE recognition: identical to the durable read at the trigger; the
  difference is *only* whether the receipts already show persistence past the
  trigger. The scan records the in-window signal and its dates; the durable
  upgrade is a **downstream monitored act, not the scan's** (the scan builds no
  standing monitor).

### Manufactured-demand read (fake / amplified → discount / avoid)

Trigger: demand that is **not real** — promotion-engagement mismatch (promoted
hard, engaging below the channel's own baseline), astroturf / coordinated / bot
amplification, dupe-wave distortion, or a quality attack running where marketing
is loudest. **Divergence is the recognition technique here, not a verdict**: it
is the cross-venue disagreement used to classify a candidate as transient or
manufactured — never noise to average away (thesis integrity layer).

- NEWSY recognition: marketing-loud surfaces versus community sentiment splits
  (the taxonomy's TikTok-vs-IG, Reddit-attacks-under-promo-push examples).
- SUBTLE recognition: detector evidence contradicting brand-maintained claims
  (a silent reformulation detected by INCI diff while marketing continues
  unchanged).
- Per the gate's divergence defeater (§3): if the only costly-behavior signal
  sits inside the same coordinated layer that divergence flags, the read is
  manufactured (the floor is defeated, not merely the ceiling capped).

### Brand-decision event (DecisionEvent) read (the monetization unit)

Trigger: evidence that a specific brand's allocation decision happened or is
visibly imminent — launch / reposition; retail or channel entry or exit;
restock / sellout handling; discontinuation / moratorium; defend-versus-hype;
event-triggered pricing. The demand-state read (durable / transient /
manufactured), wind-caller state, and integrity labels are context that makes
the event decide-grade and set the action ceiling — commit or scale when origins
converge and persist; probe or monitor when they do not.

- NEWSY recognition: brand statement or trade coverage of the decision;
  founder quotes; community detection that trade press adopts as canonical.
- SUBTLE recognition: no brand statement exists — the detector record IS the
  evidence, under the guide's corroborated material-change A-leg: material
  evidence of the change from 2+ INDEPENDENT origins PLUS a community detection
  wave. A single origin never mints a candidate.

### Wind-caller (WindCaller) calibration read (the compounding asset)

Trigger: a channel (or named public-figure creator, per §6) whose dated public
call (Call) preceded a move or event the scan can date. Calibration grades the call on
**both** whether the move happened **and how long it lasted** (a caller good at
durable shifts and one good at spikes are different and both valuable). The scan
records a calibration-ready call record (§6); grading itself is downstream
outcome-memory machinery, never the scan's act.

### Calling-sequence rule for scans (PROPOSED absorption — adjudication surface)

The taxonomy's calling sequence is "first call = transient (conservative
default) → monitor → earn durable." For a point-in-time scan this absorbs as:
**the scan classifies demand-state conservatively** — transient by default for
any real-demand recognition, durable ONLY when the receipts themselves evidence
persistence past the trigger, manufactured when the integrity/divergence
technique defeats reality. The "observe persistence, earn the durable upgrade"
step is a **downstream monitored act outside the scan's authority** (the scan
builds no standing monitor; passive monitoring, where authorized, is a separate
capture-lane act under the wind-caller carve-out's Tier-1 discipline). *This
absorption is flagged for adjudication — the commissioning lane may accept it or
direct a different scan-time classification rule.*

### Anti-triggers (explicit; none of these mints a candidate)

- **Price-complaint volume — never a trigger.** Chronic, non-discriminating,
  ungradeable (taxonomy pricing refinement, **owner-ratified 2026-06-14**). The
  exception is real: **price-driven rerouting** (dupe adoption, trade-down,
  switching with stated cause) is gradeable costly behavior and IS a trigger —
  usually a transient read, durable when a price move drives permanent defection
  to a cheaper brand (the read classifies which). An event-triggered pricing
  decision (happened or visibly imminent) IS a brand-decision event. Complaint
  chatter alone triggers neither.
- **Attention/engagement volume alone** — at most a look-here cue for the
  walk; a candidate requires gradeable costly-behavior or decision-event
  evidence (thesis costly-behavior primitive). Absence of demand ("velocity
  miss," falling engagement) is never a costly-behavior pass.
- **Availability alone** — movement over availability (owner word); presence
  on a shelf is not a read.
- **Prominence** — fame is not relevance; in backward mode it is a FAME flag
  obligation (case-finder bar), never a selection criterion.
- **Person-level signals beyond the wind-caller carve-out** — org-level signals
  only, except the bounded internal wind-caller naming permitted in §6. No
  outreach or contact lists (Tier 3, absolute); no audience / follower-graph
  analysis (Tier 2, deferred-gated); LinkedIn stays org-level (unchanged).

Precursor signals may route the walk, explain a pivot, or justify a later
`capture_request`, but they do not mint a candidate unless the promotion and
candidate-entry rules below are met.

## 2. Walk Order

How a scan consumes the venue layer. For a vertical with a promoted card set
(beauty today), the guide's Step-0 rule applies: **read the card set FIRST**,
then the provenance grep (`rg -l "Screen Provenance|Venue Provenance" docs/`).

- **Chain order.** Enter NEWSY via the trade hubs (cards 1–3), brand-story
  press first; ingredient/market press only when hunting regulatory forcing
  functions (guide trade-press fork). Enter SUBTLE via origination/tracker
  cards (4–9) and detector cards (10–12).
- **Mode inflection.** Backward mode may enter NEWSY-first: resolved events
  are already laundered into the citable record, then traced back to
  origination for pre-cutoff depth. Forward mode weights origination and
  detector cards: detection precedes press by weeks-to-months (card 8), and
  freshness is the forward constraint.
- **Fail-soft cards.** Cards are dated hints, never current-state claims. A
  card that fails its access shape is an ACCESS-NOTE under the Walker
  Equipment Kit (escalate the read shape within screening posture, record
  shapes tried, move on). A scan never edits a card; card maintenance is
  owner review-date work.
- **Dead/thin list respected.** Known dead/thin venues are not re-walked
  without stated reason.
- **Discovery beyond the cards** follows the guide's Steps 1–3 (defaults
  pass, hub-finding, expand-on-signal) under its caps and stop rules; newly
  productive precursor surfaces or venues land in the scan's provenance block,
  never appended to any standing list.

## 3. Candidate Observation Schema

Precursor signals stay in the MGT/minimum-evidence layer until they are worth
carrying for downstream gate or capture evaluation. Promotion into this richer
schema requires the signal to tie to a URL, decision window or candidate, and a
possible gate role; a precursor by itself is not gate proof.

Two record shapes: the **observation (Observation)** (one venue × one signal) and the
**candidate entry** (one brand × one decision, aggregating observations).
Both are emitted into the scan's own dated artifact (homes in §5).

### Independence rule (de-correlation by origination)

The re-derived Demand-Substrate Hard Gate counts **effectively-independent
demand-venue origins**, not a raw venue-family count. An independent origin
traces to a **distinct origination event**: signals on the same `derived_from`
chain — or tracing to a common upstream origination event or a shared
coordinated origination — **collapse to one** origin. Pairwise "neither derives
from the other" is insufficient (two laundered siblings of one event satisfy it
while violating independence). The schema therefore records origination lineage
so the gate check is mechanical, not judgment-at-consumption.

### Observation record

```yaml
observation_id:           # scan-local sequence
mode: backward | forward
brand:                    # brand, plus parent where visible (entity join is downstream)
product_or_sku:           # or category-level / null
trend_vector:             # ingredient/category/format/claim in motion, or null for pure brand events
read_type: durable | transient | manufactured | brand_decision_event | wind_caller_call
                          # durable/transient/manufactured are the three demand-state reads;
                          # divergence is a recognition technique recorded below, not a read_type
demand_state: durable | transient | manufactured | not_applicable
                          # for demand-state reads: the conservatively-tagged state (§1 calling-sequence rule)
signal_layer: trend_vector | wind_caller | buy_side | org_motion | integrity
venue:                    # card number/name, or discovered venue
venue_class: newsy | subtle
venue_family: review_surfaces | forums_community | search_interest | retail_presence | trade_press | tracker_detector | org_motion_surface | creator_social
gate_family: review_surfaces | forums_community | search_interest | none
                          # the demand families that COUNT toward independence (retail_presence excluded — it is G4 corroboration);
                          # today only forums_community is sourced; review_surfaces + search_interest are unsourced gaps (owner-owned)
gate_family_basis:        # why this observation does or does not count toward the demand-origin count
origination_ref:          # the distinct origination event this observation traces to (for de-correlation)
derived_from:             # upstream origination/chain refs, where resolvable (laundering trace)
costly_behavior: gradeable | attention_only | none
                          # gradeable = (a) attributable to identifiable buyer actions; (b) statable with direction + rough magnitude; (c) corroborable/checkable
integrity_notes:          # amplification risk, incentive distortion, copied/coordinated marks, venue bias
divergence_basis:         # cross-venue disagreement observed (the technique), and whether it caps the ceiling or defeats the floor
event_dates:              # when the observed thing happened (as dateable from the receipt)
retrieval_date:           # when the scan read it
provenance:               # URL + short quote (screening-grade)
decision_relevance:       # which wedge decision family this bears on, and why
us_flag: us | non_us | border
```

`venue_family` / `gate_family` vocabulary note (gate checkability): the
re-derived Demand-Substrate Hard Gate counts independence across its demand
families — `review_surfaces`, `forums_community`, `search_interest` — and counts
**distinct origins**, not distinct family labels. **`retail_presence` is now G4
org-motion corroboration, EXCLUDED from the demand-origin count** (it is neither
a deprecated label nor a sourcing gap); the non-demand-origin families
`trade_press`, `tracker_detector`, `org_motion_surface`, and `creator_social` are
likewise evidence/corroboration venues that take `gate_family: none`. Public YouTube videos/Shorts can feed
`creator_social` when they provide a dated public call or campaign context, but
not comments, channel/person dossiers, graphs, or monitoring. If a trade-press
receipt launders a community-originated
demand signal, `venue_family` stays `trade_press`, `gate_family` records the
underlying demand family evidenced, and `origination_ref` ties it back to the
single origin (so a laundered chain never counts as multiple origins). A
`gate_family` value is recorded only on an observation whose own venue is that
demand family AND whose `origination_ref` is distinct. Today only
`forums_community` is sourced; `review_surfaces` and `search_interest` are
owner-owned unsourced gaps — a scan records them as gaps, never as satisfied.

### Candidate entry

```yaml
candidate_id:
mode: backward | forward
brand:                    # + parent where visible
vertical_subniche:
decision_context:         # one line — the resolved decision (backward) or the live/imminent decision (forward)
decision_family: tier_price | retail_channel | launch_moratorium_reposition | taste_shift_pivot | defend_hold
demand_state: durable | transient | manufactured | undetermined   # conservatively tagged (§1)
venue_class: newsy | subtle
observations: []          # observation_ids supporting this entry
gate_check:               # derived from observations; makes the re-derived Hard Gate mechanically checkable
  independent_origins_seen: []   # distinct origination events backing demand-venue observations;
                                 # each backed by observation_ids + origination_ref + independence_basis (laundered siblings collapse to one)
  costly_behavior_floor: cleared | not_cleared   # ≥1 GRADEABLE costly-behavior instance in ≥1 qualifying demand-venue family (with supporting observation_ids)
  commitment_ceiling: hold_low_commitment | material_action_eligible   # derived: 1 origin → hold/low-commitment; ≥2 converging independent origins → material action
  divergence_result: none | caps_ceiling | defeats_floor   # the divergence technique's effect on this candidate
  integrity_labels_applicable: yes | no
  org_motion_route: available_cited | unavailable_unknown | blocked_outside_current_binding | not_applicable   # cites the owning capture-lane binding when available; never sets one
  retail_corroboration: present_g4 | absent | not_applicable   # retail presence as G4 corroboration only — never counted as a demand origin
decision_owner_pointer:   # public role (named only when the name is itself the public receipt); or unknown
flags: []                 # FAME | NON_US | BORDER | WEAK | CORR (pool vocabulary, carried verbatim)
zero_spoiler_feasibility: # backward only — can a pre-cutoff packet be built without outcome leakage? (note, not proof)
outcome_note:             # backward only — what resolved and when
freshness:                # forward only — oldest load-bearing retrieval_date + stale_after (§4)
```

**Gate outcome is by tier, not a single hard count** (buyer-proof gate): a
candidate FAILS the gate only when the **floor cannot clear** — no gradeable
costly-behavior instance in any qualifying demand-venue family
(engagement/attention volume alone never clears it), or no qualifying
demand-venue origin at all. With the floor cleared on **one** independent
origin, the read is admissible but **capped at hold / low-commitment**; any material
or irreversible commitment — **commit or scale** — requires **≥2 independent converging
origins**. A single clean origin is a ceiling cap, not an automatic failure.

`decision_owner_pointer` boundary: role-level by default; a name appears only
when it is itself the public receipt (a founder quoted on the decision).
Org-level signals only — no person-level dossiers in any sold or external
surface (the contact gate is closed). The one bounded exception is internal
wind-caller naming under the carve-out (§6), which is internal-calibration-only
and never enters a sold or published surface.

### Shape reconciliation

- **Backward → pool row** (candidate-pool handoff columns): Brand ←
  `brand`; Vertical ← `vertical_subniche`; Decision (one line) ←
  `decision_context`; Class ← `venue_class`; Flags ← `flags`; Source ledger ←
  the scan's dated artifact. The pool's flag vocabulary and consuming-batch
  obligations carry unchanged.
- **Forward → brief slot columns** (target-selection brief, re-columned
  2026-06-14): Candidate context ← `brand` + `decision_context`; Decision
  family ← `decision_family`; **Independent demand-venue origins visible** ←
  `gate_check.independent_origins_seen` (laundered / shared-origination copies =
  one; org-motion / retail excluded); Costly-behavior evidence visible ←
  `gate_check.costly_behavior_floor`; Org-motion route available ←
  `gate_check.org_motion_route`; Named decision owner ←
  `decision_owner_pointer`; Status ← the discovery lane's own call. Slot-tier
  guidance carried verbatim: **1 independent origin → hold/low-commitment
  ceiling; ≥2 converging origins → material-action eligible.** The scan fills no
  slot — it produces the dated scan doc a slot may be filled from.

## 4. Two Modes, One Core

One grammar (§1), one walk discipline (§2), one schema (§3). The modes differ
in purpose, outcome posture, entry weighting, output home, and freshness.

| | Backward (backtest case-finding) | Forward (discovery / targeted) |
| --- | --- | --- |
| Purpose | Surface resolved, decision-grade cases (Case) for backtest batches | Surface live/imminent decisions (for the brief's blank slots, or for a commissioned single target) |
| Outcome posture | Outcome-bearing by design | Outcome-free (no outcome exists yet) |
| Walk entry | NEWSY-first allowed (laundered record, trace back) | Origination/detector-weighted (freshness) |
| Output home | Scan's dated ledger; pool vN consolidates | `docs/research/orca_discovery_candidate_scan_*.md` (brief record home), or a dated single-decision scan doc (targeted) |
| Freshness | Cutoff-window framed | 21-day scan-to-use maximum (below) |

**Forward mode runs in two entry shapes.** Same core grammar, schema, and gate;
they differ only in entry trigger and output home:

- **Discovery slot-filling.** The default forward shape: a vertical-scoped walk
  hunting live/imminent decisions to fill the target-selection brief's blank
  slots. Output home: the brief's bound record home.
- **Commission-driven targeted.** A single named company/decision arrives (a
  commission), and the gate-forward grammar produces the collection plan for
  that one read — what venues to walk, which origins and gate columns the read
  must clear, what would qualify or disqualify it. Output home: a dated
  single-decision scan doc (not a brief slot); the brief's slot-fill rule still
  governs if that read is later promoted to a slot. This is distinct from broad
  slot-filling and is named explicitly so a demand commission is not blind
  before discovery → capture → ECR. *(This thin targeted mode was the
  commission's open "resolve-first" question; resolved here by addition rather
  than assumed under slot-filling.)*

**Backward contamination posture.** The scanner is facilitator-side and
outcome-exposed by design — it hunts events because they resolved. Its
discipline is therefore not blindness but containment: (i) the scan direction
(vertical × decision family) is declared before walking, and every in-scope
candidate found is recorded, hits and non-hits alike (anti-cherry-pick — no
outcome-flattering selection); (ii) every candidate carries a
`zero_spoiler_feasibility` note (whether a pre-cutoff packet (CapturePacket) looks buildable
without the outcome leaking) and prominence is flagged FAME for the
case-finder bar; (iii) no candidate is minted from the scanning model's own
memory — every claim is URL-backed (Walker Equipment Kit rule 7; the frame's
self-reference trap); (iv) recognition probes, swaps, admission, dev/holdout
splits, and packet construction belong to the CONSUMING batch under the
finder frame's operative bar and the pool's consuming-batch obligations — the
scan runs none of them.

**Forward freshness/decay rule.** A live 30–90-day decision read goes stale
in weeks. Every forward observation carries `retrieval_date`; every forward
candidate entry carries `stale_after` = earliest load-bearing
`retrieval_date` + 21 days. **Maximum scan-to-use age: 21 days** from
retrieval to slot-qualification use (PROPOSED default — adjudicate or amend
by dated note). This bounds **observation freshness**, and is distinct from
predicting decay: per the taxonomy, durability is **observed, not predicted**
(the scan tags transient conservatively and never forecasts a decay curve; the
durable upgrade is earned downstream by monitored persistence). Past
`stale_after`, the entry may not feed a slot until the load-bearing
observations are re-verified (fresh retrieval of the same receipts, refreshing
`retrieval_date`); re-verification is a bounded re-read, not a new scan.
Forward entries record no predictions as outcomes; `outcome_note` stays empty
in forward mode.

**Mode wall.** The backtest candidate pool is NEVER a forward-mode slot
source (brief rule, owner word DB-4). If a forward scan independently
re-observes a live decision at a brand that also sits in the pool, the dated
forward scan doc is the slot source and must stand on its own fresh
observations; the pool row is neither imported nor cited as qualification
evidence.

## 5. Handoff Contracts

### To capture (step 3)

Per candidate entry, the scan emits a **capture_request** (the shared scanning
vocabulary term for the older "capture-needs list"): venue + URL set + which
observation and which gate column the capture would support + the window
(cutoff-bounded for backward; freshness-bounded for forward).
Boundaries, all hard:

- Per-venue route bindings are capture-lane-owned. The scan CITES the
  current binding state it relied on (e.g., a card's recorded read shape) and
  may say `route: unknown`; it never sets, stretches, or recommends a route.
  Route expansion is a capture-lane decision (thesis ask-1 posture: measured
  ToS risk accepted, absurd-level rejected — applied there, not here).
- Scan evidence stays screening-grade. Nothing the scan collected is
  packet-grade; capture re-acquires under its own provenance discipline.
- Unresolved access walls are the ORCHESTRATOR's close-out duty: every wall
  routes to the capture seam (Source Capture Playbook / Source Capture Armory
  screening-read service / recon index) before that vertical's next scan (guide
  rule, carried).

### To candidate recording (step 4)

- **Backward:** candidate entries land in the scan's own dated ledger with a
  `Screen Provenance` (or lane-appropriate `Venue Provenance`) block per the
  guide — verbatim section names; append-only; negative set included. Pool
  consolidation is a separate cut under the pool's own rules (one-shot,
  dated, never updated in place; source ledgers remain the source of truth;
  flag vocabulary verbatim).
- **Forward (discovery):** candidate entries land in a dated scan doc at
  `docs/research/orca_discovery_candidate_scan_<slug>_v0.md` (the brief's
  bound record home), provenance-noted. Slot-filling is the discovery lane's
  act under the brief's slot-fill rule; near-miss, hold, and
  disqualification records go to the proof-batch notes home.
- **Forward (targeted):** the single-decision read lands in its own dated scan
  doc; it is not a brief slot unless and until the discovery lane promotes it
  under the brief's slot-fill rule.
- Candidate companies are not buyers, leads, prospects, or clients; the
  no-buyer-contact gate is closed and this spec does not touch it.

## 6. Wind-Caller Sub-Procedure

Per sub-niche, inside any authorized scan (both modes):

1. **Identification.** When a walk move yields an influence observation (the
   guide's widening: hubs, pointing structures, byline concentration), test
   for wind-caller candidacy: a channel, including a public YouTube video or
   Short that carries a dated public call, or a named public-figure creator,
   per the carve-out below, whose dated public call preceded a move or event
   the scan can date, in this sub-niche, with a receipt. Pointing chains
   terminate at wind callers; INCIDecoder (card 11) is the worked exemplar —
   its commissioned tests became the root receipt an entire event chain cites.
2. **Call record** (calibration-ready means a later grading pass can score
   hit/miss without re-derivation):

```yaml
caller_channel:    # channel name + platform/venue
caller_public_figure:  # public handle + public name — ONLY for named public-figure creators, internal-calibration use only (carve-out); else null
subniche:
call:              # direction + object (trend vector or brand decision)
call_date:
call_receipt:      # URL + retrieval date
preceded:          # the move/event it preceded, with dates, where resolvable
latency:           # call date → event/market date
graded_on:         # whether-it-happened AND how-long-it-lasted (durable vs transient), per the taxonomy
outcome_status: resolved | open   # backward: usually resolved; forward: open
```

3. **Anti-cherry-pick.** Record the calls found in scope whether they look
   like hits or misses; calibration GRADING is outcome-memory machinery
   downstream, never the scan's act.
4. **Boundaries (hard) — reconciled to the wind-caller carve-out
   (`docs/decisions/wind_caller_calibration_carveout_v0.md`, owner-signed
   2026-06-13, amended through 2026-06-15):**
   - **Naming a public-figure creator wind-caller is permitted for INTERNAL
     calibration only** — public handle, public name, public calls, public
     stats, call-vs-outcome calibration — recorded **non-permanently**
     (time-bounded; 10-year retention ceiling + takedown-on-request).
   - **No sold or externally published person-level surface** (Tier 3,
     absolute, unchanged); no outreach or contact lists; no special-category or
     private/auth-gated data; no audience / follower-graph analysis (Tier 2,
     deferred-gated). The external/product boundary is unchanged.
   - **Public YouTube video/Shorts calls are admissible only as dated, non-login
     public-call receipts**; no comment scraping, channel enumeration,
     subscriber/follower graph, channel/person dossier, or standing channel
     observation is created by the scan.
   - **The scan does only screening-grade identification + the call record
     above.** Deeper calibration capture (platform stats, Social Blade, the
     bounded passive-monitoring runs) is a **capture-lane act under the
     carve-out's Tier-1 discipline (≤10 own operating accounts, attended-active
     / bounded-self-terminating-passive, US-first), not the scan's.** *(This
     scan-vs-capture boundary is a PROPOSED absorption — flagged for
     adjudication.)*
   - **In-scan observation only** — standing observation of any channel is a
     monitor, forbidden to the scan. No wind-caller registry, atlas, or card
     set arises from scans; consolidation of influence trails routes only
     through the guide's promote-on-reuse trigger, owner-decided. Call records
     are dated history, never current-state claims about a channel's
     reliability.
   - **LinkedIn org-motion is a separate context, completely unchanged** —
     org-level only (hiring composition, headcount), never person-level.

## 7. Reconciliation Note

- **Demand-read taxonomy** — this spec ABSORBS its demand-state model (durable /
  transient / manufactured; divergence as a recognition technique; the
  conservative transient-default classification) into the hunting grammar (§1)
  and the schema (§3). It LEAVES with the taxonomy the model's ownership and any
  ontology / decision-grade proof, which the taxonomy explicitly defers to a
  separate pass. The taxonomy is PROPOSED; this spec re-derives if it is
  adjudicated with further amendments.
- **Demand-Substrate Hard Gate (buyer-proof packet)** — this spec ABSORBS the
  re-derived gate (origination-independence, verb-tiering by commitment, retail
  excluded, the gradeable costly-behavior floor, the divergence defeater) into
  §3 so the gate is mechanically checkable from a scan's emitted schema. It
  redefines nothing in the gate; it makes the gate's columns fillable.
- **Vertical exploration guide** — this spec ABSORBS the candidate-finding
  intent of the walk: what a scan hunts (§1), how it consumes the venue layer
  (§2), what it emits (§3), and the mode semantics (§4). It LEAVES with the
  guide: all walk mechanics (Steps 0–5, move caps, dry rule, ACCESS-NOTE
  semantics, the Walker Equipment Kit, Screen/Venue Provenance memory, the
  promote-on-reuse trigger and its thresholds). A scan is a guide-governed
  walk; this spec amends nothing in the guide. If adoption requires the guide
  to point here, that is a dated note routed at adjudication, not performed
  by this lane.
- **Memorization-resistant case-finder frame** — the frame OWNS the
  backward-mode admission bar (operative obscurity bar, decision-grade +
  source-depth floor, zero-spoiler, decide-vs-confirm tension,
  anti-cherry-pick) and the recognition/probe protocol. This spec ABSORBS
  only the scan-time obligations that make that bar checkable later (FAME
  flagging, zero-spoiler feasibility notes, declared-direction
  anti-cherry-pick, URL-backed-only minting) and LEAVES admission, probes,
  swaps, and splits to the consuming batch. The scan extends the frame's
  screen; it does not replace it.
- **Candidate-pool handoff / target-selection brief** — own the destination
  shapes (backward consolidated pool; forward slots and record homes). This
  spec emits INTO those shapes (§3 reconciliation, §5 contracts) and
  redefines neither; their obligations bind their consumers unchanged.
- **Wind-caller calibration carve-out** — owns the naming / internal-use /
  retention / external-boundary policy; §6 cites it and stays inside it.

## Hard Constraints (carried)

Docs-first: no implementation, code, automation, dashboards, or runners. This
spec authorizes no scan execution, capture, web research, or outreach.
US-market default: non-US candidates are flagged and route to the owner or
defer (pool/brief obligations mirrored). Capture route bindings are
capture-lane-owned — cited, never set. The backtest candidate pool is never a
forward-mode slot source. Amendments are dated notes only; no silent
rewrites.

## Non-Claims

PROPOSED method spec only — not doctrine, not validation, readiness, buyer
proof, or judgment-quality evidence; closeout state for any such claim:
`no_durable_evidence`. Mints no evidence-ladder vocabulary; redefines no
overlay-owned semantics; does not adjudicate the taxonomy, the Hard Gate, the
thesis, or the carve-out it binds from. Authorizes no scan, capture,
monitoring, outreach, or build; every consuming lane keeps its own
authorization boundary.

**Adjudication surfaces** (named so the commissioning lane can accept or amend
them explicitly, not silently baked):

- The 21-day forward freshness default (§4).
- The conservative transient-default scan-time classification rule (§1) and the
  scan-vs-capture-lane boundary for wind-caller calibration (§6).
- The `gate_family` demand-family set now excludes `retail_presence` and treats
  `review_surfaces` / `search_interest` as today-unsourced gaps (§3), per the
  re-derived Hard Gate.
- The commission-driven targeted forward entry shape (§4).
