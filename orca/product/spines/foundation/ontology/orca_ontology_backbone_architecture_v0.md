# Orca Ontology Backbone — Architecture (PROPOSED) v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (architecture-pass deliverable — PROPOSED ontology backbone)
scope: >
  PROPOSED design for Orca's shared, governed semantic backbone: a Foundry-style
  domain ontology in two layers — Layer 1 (domain object/link/action roster to
  BUILD) and Layer 2 (workflow ontology that MAPS to existing overlay owners,
  never rebuilds). Naming-normative / schema-light. Returns a design for owner
  adjudication; enacts nothing.
use_when:
  - Adjudicating whether to adopt the Orca ontology as the repo's semantic backbone.
  - Locating the proposed object roster, links, action gates, ID grammar, and binding plan.
authority_boundary: retrieval_only
status: ADOPTED_2026-06-15 (owner-signed) — core 15 of 18 names; Buyer + Org RESERVED (deferred, §6.1)
commission: docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
base: origin/main @ 953af7ea (frozen); freshness gate PASSED (8/8 sha-pins + LIVE grammar verified)
adjudication_route: ICP / product-direction lane adjudicates; owner signs adoption and any folder/router binding.
lock_in_notice: >
  HIGH downstream lock-in BY DESIGN — this is meant as the repo backbone. The
  lock-in lives in the NAMING / RELATIONSHIP / ID-GRAMMAR surface (object names,
  the two load-bearing links, the ID scheme), which is deliberately kept small
  and schema-light so the cost is bounded. See §7.
```

This is PROPOSED architecture. It is not validation, readiness, proof, adoption,
or implementation authorization. It enacts no folder, router, or object card. The
ontology is naming / relationship / gate-pointer authority by design — not a new
validation or lifecycle authority. Property lists are deliberately NOT frozen.

---

## §0. Method, Source Context, and Freshness (receipt)

- **Cynefin route:** Complicated (reason-through from existing sources) with one
  Complex edge — the object carve is HIGH lock-in and rests on a freshly-landed
  demand grammar; carved risk-first against the current grammar, not the
  2026-06-13 snapshot.
- **Method (source-gated):** `workflow-goal-framing` (§1) → `SOURCE_CONTEXT_READY`
  → `workflow-architecture-planning` (§7). Methods were REFERENCE-LOADed and only
  APPLIED after source readiness.
- **Freshness gate:** PASSED. All 8 sha-pinned sources matched frozen base
  `953af7ea`; the LIVE demand-grammar sources were verified to carry the current
  demand-state model + Q0–Q3 adjudication + applied G1/G2/G4 gate-closure model
  (NOT the retired durable-vs-hollow framing).
- **Source-read ledger** (read at the frozen base; extraction delegated read-only):
  - Layer-1 grammar: `orca_product_thesis_consumer_demand_v0.md`,
    `orca_demand_read_taxonomy_v0.md`, `orca_demand_read_taxonomy_adjudication_v0.md`.
  - Gates/proof: `orca_demand_gate_definition_closures_proposal_v0.md`,
    `orca_buyer_proof_packet_v0.md`.
  - Object exemplars/kernel: `beauty_venue_card_set_v0.md`,
    `consumer_demand_candidate_pool_handoff_v0.md`,
    `orca_discovery_consumer_demand_target_selection_brief_v0.md`.
  - Survey: `source_capture_packet_schema_evolution_architecture_v0.md`,
    `judgment_spine_evidence_ladder_architecture_v0.md`,
    `judgment_spine_gate_ownership_map_v0.md`,
    `judgment_spine_read_machinery_architecture_handoff_v0.md`,
    `judgment_spine_backtest_batch1_ledger_declaration_v0.md`.
  - Layer-2 owners + binding: `artifact-roles.md`, `artifact-folders.md`,
    `source-of-truth.md`, `orca_repo_structure_binding_v0.md`, `repo-structure.yaml`.
- **Declared source gaps (not blockers; commission anticipated):**
  1. `orca_demand_scan_core_spec_v0.md` is ABSENT (in-flight, not on `main`) —
     designed FOR as a forward consumer; its Observation/Candidate schema is not pinned.
  2. `EvidenceUnit` is not a frozen schema anywhere; the concrete artifact is the
     3-tier `claim_tier` ladder. Treated as a candidate type, schema-light.

---

## §1. Goal Frame

**Long-term goal.** Orca becomes a consumer-demand decision-intelligence product
(beauty first) whose every lane, scan, capture, backtest, judgment, and proof
artifact reasons over ONE shared, governed vocabulary of demand-world
objects/links/actions — so repo knowledge compounds (the outcome-memory moat)
instead of fragmenting into per-lane schema re-inventions.

**Anchor goal.** A PROPOSED ontology-backbone architecture that (a) names the
capped demand-world object/link/action roster (Layer 1) against the current landed
grammar, and (b) MAPS workflow concepts to their existing overlay owners (Layer 2)
— naming-normative / schema-light, adoptable in one owner pass, nothing enacted.

**Success signal.**
- *Core success.*
  - *Owner-observable:* owner reads this one doc and sees the full object roster
    (≤18), each with definition + stable-ID scheme + key states + governed
    actions/gates + links + backing artifact, plus a Layer-2 pointer table — enough
    to adopt / amend / reject in one pass.
  - *Output fit:* cross-artifact references become addressable IDs
    (`brand:beautypie`, `case:beautypie.repricing-2023`) instead of path-and-prose;
    the two load-bearing links (`derived_from`, `diverges_from`) are precise enough
    for the read-machinery forward consumer — without freezing any property list.
  - *Boundary:* NOT success = a complete-looking doc that rebuilds/restates Layer-2
    authority (forks governance), freezes property lists (straitjacket), enacts the
    folder/router, or asserts validation/readiness/adoption. Writing the file ≠ goal.
  - *Drift cue:* the design mints NEW gates/authority instead of pointing at existing
    owners; the roster inflates past the cap by promoting demand-state dimensions into
    new types; or it re-derives the demand grammar instead of encoding the landed one.
- *Secondary success.* The in-flight scan-spec and the read-machinery can be
  expressed in ontology terms with no new vocabulary; the cap + per-card review-date
  + dated-amendment kernel is stated as the ontology's OWN survival terms.

**Open question (owner decision the pass surfaces, does not answer):** accept the
HIGH repo-wide-backbone lock-in now vs a thinner naming-only layer — owner-signed
at adoption via the §7 option record.

---

## §2. Layer 1 — Domain Ontology (BUILD)

The demand world. Naming-normative / schema-light: each card OWNS the type's name,
one-line definition, stable-ID scheme, key states, governed actions (with the gate
that already governs the transition), links, and backing artifact(s). It does NOT
freeze the property list — that keeps evolving in the owning lane and is tracked
only via the backing map.

### 2.1 Stable-ID grammar (naming authority; NOT a registry)

`namespace:slug`, lowercase, dot-separated sub-parts. The ontology owns the
*grammar*; minting/resolving individual IDs (a registry) is deferred satellite (§6).

**ID-canonicalization (owner-decided 2026-06-15; forward-only convention).** This grammar is
the single naming authority: the **canonical id is the dotted form**. **Existing harness `*_v0`
ids are NOT physically renamed** — each is kept as the recorded **storage alias** under its
canonical dotted id (recorded on the Case card's `harness_case_id`, which seeds the registry);
**new cases are born dotted**. The version suffix (`_v0`) is **metadata, not part of the ID**
(owner-confirmed 2026-06-15); **an ID survives any rename** (the display name lives in a field;
the ID is an opaque, stable handle). Forward-only was chosen over a physical rename of sealed
history because the harness resolves cases by path and `case_id` is an embedded,
cross-artifact-asserted field (`run_case.py:169`) — renaming sealed / holdout / hash-pinned runs
would corrupt provenance. Both id forms always resolve (nothing is deleted), so an old reference
never dangles. (See §6.1.)

| Namespace | Example | Means |
| --- | --- | --- |
| `vertical:` | `vertical:beauty`, `vertical:beauty.fragrance` | a demand domain; sub-niche via dotted child |
| `brand:` | `brand:beautypie` | a consumer brand |
| `product:` | `product:retinol`, `product:refillable-format` | the demand target (ingredient/category/format/claim/SKU) |
| `venue:` | `venue:basenotes` | a demand-signal surface |
| `windcaller:` | `windcaller:tiktok.hyram` | a leading-indicator account/community/detector |
| `call:` | `call:tiktok.hyram.2023-04-12` | a wind-caller's early public call |
| `observation:` | `observation:basenotes.2023-04-12.3` | one captured demand signal |
| `trend:` | `trend:beautypie.2023-05-01` | a TrendVector (demand movement); `read` is an action, not an ID namespace |
| `decision:` | `decision:beautypie.repricing-2023` | a live brand-decision event |
| `memo:` | `memo:beautypie.repricing-2023.1` | a decision-risk memo |
| `reading:` | `reading:beautypie.repricing-2023.1` | a Reading (the `Read` action's calibrated decision output) |
| `case:` | `case:beautypie.repricing-2023` | a backtest/proof case |
| `outcome:` | `outcome:beautypie.repricing-2023` | a realized result |
| `packet:` | `packet:3b89a19b…` | a source-capture packet (by sha) |
| `evidence:` | `evidence:beautypie.repricing-2023.1` | a cleaned evidence unit |
| `buyer:` | `buyer:<slug>` | a qualified buyer (the ICP entity a Memo serves) |
| `org:` | `org:thg` | a company / parent org behind a Brand (org-motion anchor) |

### 2.2 Object-type roster (17 of 18 types — cap raised to 18 on 2026-06-15; "19th in = one out")

This roster is **v0 naming authority**, not a command to build all cards at once.
Build-readiness is staged in §9: weak-backing and forward-consumer types may be
reserved as names while their owning artifacts mature.

Folds applied to stay under the cap (noted): **SubNiche → Vertical** (self-parent
link). **`Read` is an ACTION on the `TrendVector` object, not an object type**
(owner-directed amendment 2026-06-15, replacing the v0 TrendVector→Read merge — see
§6.1): the object is the demand movement (`TrendVector`); reading it is the governed
verb (§2.5). Demand-state, action-ceiling, read-type, and claim-tier are
**dimensions**, not types (§2.4) — and **`claim_tier` specifically is everywhere a
receipt-gated evidence-ladder outcome, never a value a type mints; a row that lists it shows
the *currently carried* tier, set only by the gate** (owner decision 2026-06-15; closes the
AR-01 residual for `Memo` / `EvidenceUnit`). Gates are **actions**, not types (§2.5). **`Slot` →
`DecisionEvent.discovery_status`** (owner decision 2026-06-15, §6.1).

| # | Type | One-line definition | Key states / dimensions | Backing artifact(s) |
| --- | --- | --- | --- | --- |
| 1 | **Vertical** | A demand domain at a level (vertical or sub-niche); sub-niches nest via self-parent. | level: vertical \| sub_niche | thesis, wedge |
| 2 | **Brand** | A consumer brand (consumer-facing label); company/parent resolution via `Org`. A Brand can itself act as a `WindCaller` (its own moves precede the shift), but never as an independent demand-origin for its own product/decision. | — | candidate-pool handoff |
| 3 | **Product** | The demand target a TrendVector is *about*: ingredient / category / format / claim / SKU. | target_type | (gap — no single backing yet; §3) |
| 4 | **Venue** | A demand-signal surface (where observations originate). | access_shape, review_by | beauty venue card set |
| 5 | **WindCaller** | A leading-indicator referent — an account, community, detector, a Brand, *or a press/trade outlet* whose own moves precede the shift; per vertical×sub-niche; carries the carve-out boundary. Press is the venue-chain *launderer* (community originates → press launders → BoF/WWD terminate), so a press call is a *leading* indicator only when it genuinely originates; otherwise `derived_from` collapses it to the originating family (no independent-origin double-count) — same guard as Brand-as-WindCaller. | calibration_state; carve-out (non-permanent, platform-scoped cap, internal-use) | demand-read taxonomy (gap — no card-set asset yet; §3) |
| 6 | **Call** | A wind-caller's early public call that opens a (transient) TrendVector. | — | scan-spec (forward) / read outputs |
| 7 | **Observation** | One captured demand-signal instance from a Venue — the node the two provenance links connect. | integrity flags | CapturePacket / scan-spec (forward) |
| 8 | **TrendVector** | The demand movement: demand moving toward/away from a target (ingredient/category/format/claim), with direction, velocity, expected lifespan. *(Reading it — emitting a calibrated decision — is the `Read` action, §2.5.)* | persistence_state, integrity_state | demand-read taxonomy |
| 9 | **DecisionEvent** | The live brand-decision event the `Read` action serves (the monetization unit a Memo is produced for); a discovery scan evaluates *candidate* DecisionEvents (absorbs the former Slot). | trigger status, discovery_status: slot_open\|filled\|qualified | candidate pool, discovery brief |
| 10 | **Reading** | The dated calibrated output of the `Read` action — Orca's call on a `TrendVector` for a `DecisionEvent`: an action ceiling (monitor/probe/commit/hold/scale/avoid/reduce) + read_type, capped by integrity, bound by never-a-feed. The lightweight decision record; a `Memo` elaborates it for a qualified buyer decision. | read_type, action_ceiling, claim_tier | read outputs (gap — scan-spec forward consumer + memos) |
| 11 | **Memo** | The Public-Signal Demand-Allocation Decision-Risk Memo for one qualified DecisionEvent (reasoning substrate + proof gate). | claim_tier; gate pass/cap/fail | buyer-proof packet |
| 12 | **Case** | A backtest/proof case: a historical decision with known outcome. | known_outcome; receipt-backed claim-cap pointers only. `split` and `entry_basis` are batch-ledger metadata, not standing ontology dimensions. | batch-1 ledger declaration |
| 13 | **Outcome** | The realized result a Reading/Call/Case is graded against (calibration target). | — | case ledger / calibration |
| 14 | **CapturePacket** | A write-once, hash-pinned source-capture packet — the raw provenance an Observation derives from. | manifest_version, cutoff_posture | `orca-harness/source_capture/models.py` |
| 15 | **EvidenceUnit** | A cleaned evidence unit (IPF standard) bound at the Cleaning/Judgment boundary. | claim_tier | IPF foundation + evidence ladder |
| 16 | **Buyer** *(RESERVED 2026-06-15)* | *(name reserved — adoption deferred; no dedicated landed backing yet, §3)* The qualified customer a `Memo` serves — the ICP entity (e.g. a beauty operator) who owns the live `DecisionEvent`. Was implicit in the Hard Gate precondition. | qualification_status | icp/wedge + offer hypothesis (indirect) |
| 17 | **Org** *(RESERVED 2026-06-15)* | *(name reserved — adoption deferred; no dedicated landed backing yet, §3)* The company / parent behind a `Brand`; the unit org-motion (hiring, headcount, retail presence) attaches to. Distinct from `Brand` (a consumer label). | (org-motion signals) | G4 org-motion cards (corroboration data, not an Org-object definition) |

### 2.3 Link map (typed relationships)

Structural / identity:
- `Vertical —narrows_to→ Vertical` (sub-niche nesting)
- `Brand —in→ Vertical` · `Brand —owned_by→ Org` · `Org —subsidiary_of→ Org` (parent resolution) · `Brand —offers→ Product` · `Brand —can_act_as→ WindCaller`
- `WindCaller —covers→ Vertical` (per vertical×sub-niche)

Signal flow:
- `WindCaller —made→ Call` · `Call —opens→ TrendVector`
- `TrendVector —about→ Product` (or `—about→ Brand`)
- `Observation —from→ Venue` · `Observation —supports→ TrendVector` · `Observation —captured_in→ CapturePacket`
- `EvidenceUnit —cleaned_from→ Observation` (and/or `CapturePacket`)
- the **`Read` action** (§2.5) reads a `TrendVector` and `—serves→ DecisionEvent`, emitting a `Reading`: `Reading —of→ TrendVector` · `Reading —for→ DecisionEvent` · `Memo —elaborates→ Reading` (the heavyweight form for a qualified decision)

**The two load-bearing links** (owner-decided in the demand-gate closures; the
read-machinery forward consumer depends on them — design them precisely):
- **`Observation —derived_from→ Observation`** — the provenance/laundering edge.
  Two Observations on one `derived_from` chain are NOT independent: they collapse
  to a single origination family. This is the de-correlation test behind G1
  (independence by de-correlated origination) and the Demand-Substrate Hard Gate's
  independent-origin count. Directed, transitive for the collapse test (any shared
  upstream origination event = one family); pairwise "neither derives from the
  other" is explicitly insufficient. Cycles are invalid producer data; until
  repaired, every node in the cycle collapses to one origination family. Multi-parent
  derivation unions all upstream families, so any shared upstream family blocks
  independent-origin counting.
- **`Observation —diverges_from→ Observation`** — the cross-layer disagreement edge.
  The integrity / astroturf tell. Preserved as signal, never averaged away.
  Constrains the action ceiling; and where divergence indicates the costly-behavior
  instance is itself likely manufactured/coordinated, it can **defeat the floor**
  (G2), not merely cap the ceiling. Directed, non-collapsing (divergence is kept,
  not resolved). It must carry the layer or coordination basis that makes the
  disagreement meaningful: a G2 floor-defeater requires the costly-behavior instance
  to sit inside the same coordinated layer that the divergence flags; otherwise
  divergence constrains the ceiling only.

Self-origin guard:
- A `Brand —can_act_as→ WindCaller` link may support calibration or early-warning
  reads, but observations/calls self-originated by that Brand are labeled
  `self_originated` for that Brand's own Product/DecisionEvent and are excluded
  from the G1 independent-origin count. They may corroborate or explain a move;
  they cannot launder the brand's own signal into independent demand.

Proof / calibration:
- `Memo —for→ DecisionEvent` · `Memo —cites→ EvidenceUnit` (and/or `Observation`) · `Memo —serves→ Buyer` · `Buyer —owns→ DecisionEvent`
- `Case —backtests→ DecisionEvent` · `Reading —graded_by→ Outcome` · `Call —graded_by→ Outcome` · `Case —graded_by→ Outcome`
- a discovery-scan candidate is a `DecisionEvent` (with `discovery_status`) · `DecisionEvent —concerns→ Brand` (candidate = brand + live decision)

G4 distinction (must not leak into the G1 count):
- org-motion / retail-presence evidence (attached to `Org`) `corroborates` a TrendVector but is EXCLUDED
  from the independent-origin count — modeled as a distinct link `corroborates` (G4),
  never `supports`-counted toward independence (G1). The premium signal is the
  `diverges_from` read where org-motion and demand layers disagree.

### 2.4 Demand-state machinery (DIMENSIONS, not new types)

Folded onto existing types under the cap, per the commission:
- `persistence_state: durable | transient` (durable = persists past trigger;
  transient = real but decays) — on `TrendVector` (carried onto `Outcome` for
  grading). "Hollow" is RETIRED (it conflated transient with manufactured).
- `integrity_state: real | manufactured` (real = costly behavior; manufactured =
  fake/amplified) — on `TrendVector` (and `Outcome`).
- derived action state `{durable→commit/hold/scale, transient→commit (reversible)→reduce on decay,
  manufactured→avoid}` — derived only where it helps a consumer; the
  integrity axis must NOT be collapsed into the persistence axis.
- `action_ceiling` — the flat verb set `{monitor, probe, commit, hold, scale, avoid, reduce}`
  (horizon not declared — it accretes via monitoring); capped by signal
  integrity *(dated note 2026-06-20, owner-directed; read-through, not re-adoption: this
  `action_ceiling` value set was changed from the prior frozen ladder
  `act/phase/narrow/hold/defend` × horizon to this flat 7-verb set per the demand-read C3
  contract's 2026-06-20 amendment, which owns the vocabulary and carries the propagation
  receipt — a one-field value-set update; the object roster, links, and ID grammar are
  unchanged)* ("the verb may not exceed what signal integrity supports"). It is a
  **field on the `Reading`** (the `Read` action's output, §2.5), not a standing field
  on `TrendVector`.
- `read_type ∈ {durable-demand, transient-spike, manufactured-demand,
  brand-decision-event (monetization unit), wind-caller-calibration (compounding
  asset)}` — a field on the `Reading` (classifies it). *Divergence is a technique, not
  a read type.*
- `claim_tier ∈ {product_learning, buyer_proof, judgment_quality}` — on Reading, Memo,
  Case, Outcome (the evidence ladder, MAPPED, §5).

### 2.5 Action / gate map (governed transitions — the ONLY sanctioned state changes)

Each names the gate that ALREADY governs it; the ontology makes the gate
*addressable*, it does not invent new gates.

| Action | On | Precondition / gate (where it already lives) |
| --- | --- | --- |
| `TrendVector.open_transient` | TrendVector | conservative default: opens transient and acts in-window; never opens durable (demand-read taxonomy / calling sequence) |
| `TrendVector.monitor` | TrendVector | persistence is observed, not predicted (taxonomy) |
| `TrendVector.earn_durable` | TrendVector | monitored persistence holds past the trigger (taxonomy) — the earned upgrade transient→durable |
| `TrendVector.decay` | TrendVector | spike decays as called (taxonomy) |
| `Read` (emit calibrated decision) | TrendVector → Reading | reads a `TrendVector` for a `DecisionEvent`; emits a `Reading` (action ceiling + read_type), capped by signal integrity and bound by `never_a_feed` (demand-read taxonomy + Orca Promise) |
| `Gate.G1` (independence) | TrendVector / candidate | ≥2 de-correlated origination families for material commitment; `derived_from`-chain siblings collapse to one (demand-gate closures) |
| `Gate.G2` (costly-behavior floor) | TrendVector / candidate | ≥1 gradeable costly-behavior instance in ≥1 qualifying demand-venue family; absence of demand is not a pass (demand-gate closures) |
| `Gate.G4` (org-motion corroboration) | TrendVector | separate org-motion cards; corroborates but excluded from the G1 count (demand-gate closures) |
| `HardGate.evaluate` | candidate / TrendVector | fusion+integrity rule bundling G1+G2+ceiling+integrity → fail \| pass-capped(1 origin) \| pass-material(≥2) (buyer-proof packet) |
| `Memo.produce` | Memo | named qualified buyer + live decision trigger selected AND Hard Gate passes (buyer-proof packet) |
| `Call.grade` | Call | requires an Outcome receipt (wind-caller calibration; demand-side calibration is a gap — §3) |
| `Case.seal` | Case | requires a pre-declared ledger row (batch-1 ledger declaration) |
| `DecisionEvent.fill_from_scan` | DecisionEvent | a discovery slot (candidate DecisionEvent) is filled only from a dated, provenance-noted candidate scan by an authorized lane (discovery brief) |
| *constraint* `never_a_feed` | the `Read` action | every output is a calibrated decision with an action ceiling — never a feed/stream (Orca Promise; buyer-proof packet) |

Judgment-spine gates JSG-01..JSG-10 that govern Case/EvidenceUnit/Memo as they move
toward judgment-quality evidence are MAPPED, not restated (§5).

---

## §3. Backing Map and Named Gaps

Every type names the artifact(s) that instantiate it (the Foundry "backing dataset"
analog) — see the right column of §2.2. Where no clean owner/backing exists yet,
the gap is NAMED, not filled with a new authority:

- **WindCaller has no maintained card-set asset** (Venue has the venue card set;
  WindCaller does not). Future asset, parallel to the venue cards.
- **Product (demand target) has no single backing artifact** — currently implicit
  in reads/memos.
- **Observation and Call backing depends on the in-flight scan-spec**
  (`orca_demand_scan_core_spec_v0.md`, not yet on `main`) — design FOR it.
- **Demand-side Call.grade / Outcome calibration** exists only as the judgment-spine
  reveal/calibration gate (JSG-08, not cleared for any case) — a gap for demand-side
  outcome grading.
- **No global stable-ID registry/resolver exists.** v0 owns the ID *grammar*
  (§2.1); the registry is deferred satellite (§6).

---

## §4. Forward Consumers (design-for, not yet landed)

Two consumers are not yet on `main` but the carve is designed FOR them; they are
why the ID *grammar* and the two links are CORE (not deferred):

- **Read-machinery** (`docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md`).
  Its core weight step **de-correlates** signal sources via `derived_from` (so shared
  upstream is not double-counted as independent corroboration) and **maps divergence**
  via `diverges_from` (convergence-vs-divergence weighting), per-vertical, learned from
  backtested cases, LLM-in-session / qualitative (no scoring engine until the owner
  lifts the no-scoring boundary). It names this commission as the carrier of the two
  links. Requirement on the ontology: `Observation` identity + the two links specified
  precisely (§2.3).
- **Demand scan-core spec** (`orca_demand_scan_core_spec_v0.md`, IN-FLIGHT, not on
  `main`). A forward consumer whose Observation/Candidate schema should re-express in
  ontology terms (`Observation`, `TrendVector`, `DecisionEvent`, `Call`) with no new vocabulary when it
  lands. Requirement: the §2.1 ID grammar so its rows reference addressable objects, not
  path-and-prose.



---

## §5. Layer 2 — Workflow Ontology (MAP, do NOT rebuild)

Lanes, artifact roles, claim tiers, gates, receipts, and folders ALREADY have
owners in the overlay. Layer 2 is one pointer card per concept; it mints ZERO
authority. Rebuilding or restating would fork governance — the single worst outcome
for this repo. Route, don't restate.

| Workflow concept | Existing owner (points to; does not restate) |
| --- | --- |
| Lanes (product second-level axis) | `docs/decisions/orca_repo_structure_binding_v0.md` + `.agents/workflow-overlay/artifact-folders.md` |
| Artifact roles (15 bound roles) | `.agents/workflow-overlay/artifact-roles.md` |
| Claim / evidence tiers (`product_learning`→`buyer_proof`→`judgment_quality`) | `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md` (+ per-role "Validation evidence" in `artifact-roles.md`) |
| Validation gates | `.agents/workflow-overlay/validation-gates.md` |
| Judgment-run gates JSG-01..JSG-10 | `orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md` |
| Receipts (Doctrine Change Propagation) | `.agents/workflow-overlay/source-of-truth.md` (archive `docs/decisions/dcp_receipts_archive_v0.md`) |
| Folders / placement | `.agents/workflow-overlay/artifact-folders.md` |
| Review lanes | `.agents/workflow-overlay/review-lanes.md` |
| Prompt families | `.agents/workflow-overlay/prompt-orchestration.md` |
| Source hierarchy / source-of-truth | `.agents/workflow-overlay/source-of-truth.md` |
| Retrieval headers | `.agents/workflow-overlay/retrieval-metadata.md` |
| Template registry | `.agents/workflow-overlay/template-registry.md` |
| Skill adoption | `.agents/workflow-overlay/skill-adoption.md` |
| Repo router (machine map) | `repo-structure.yaml` (binding `orca_repo_structure_binding_v0.md`) |

**Layer-2 rule:** a Layer-1 action that has a workflow owner (e.g. a `claim_tier`
or a JSG gate) carries `backed_by: <owner path>` and nothing more. No Layer-2 card
states a rule; if a workflow concept has no clean owner, it is named as a gap above,
never minted here.

---

## §6. Kernel Discipline (the ontology's OWN survival terms)

Stolen from the venue card set, the proven antidote to ontology rot:

- **Hard cap: 18 domain object types** (raised from 15 on 2026-06-15 to seat `Buyer`
  and `Org` as first-class; §6.1). "19th in = one out." 17 of 18 used — one slot of
  deliberate headroom.
- **Owner: Eric.** Per-type review dates (each card carries a `review_by`); a card
  past its date is a stale hint to review or retire, not a current-state claim.
- **Dated amendments only, never silent rewrites.** Fail-soft cards: dated hints,
  not current-state claims.
- **Naming-normative / schema-light (load-bearing authority boundary).** v0 OWNS
  names, definitions, links, action gates, and the ID grammar. It does NOT freeze
  property lists — those keep evolving in their owning lanes and are tracked only
  via the backing map (§3). This is the explicit authority boundary that keeps the
  backbone from becoming a straitjacket.

### 6.1 Amendments (dated)

- **2026-06-15 (owner-directed):** `Read` reclassified from object type to **action**
  on the `TrendVector` object; `TrendVector` takes the object slot (cap unchanged at
  15). The calling-sequence lifecycle (`open_transient → monitor → earn_durable /
  decay`) moves onto `TrendVector`; `read_type` and `action_ceiling` become outputs of
  the `Read` action. Rationale: the source names "Read / Trend vector" as one concept,
  but the object (the demand movement) and the act of reading it separate cleanly — an
  action operates on an object.
- **2026-06-15 (owner-directed): `Reading` split out.** The `Read` action's output is
  now its own lightweight object — `Reading` (the calibrated call: action ceiling +
  read_type + claim_tier) — distinct from the heavyweight `Memo`, which *elaborates* a
  `Reading` for a qualified buyer decision after the Hard Gate. Most Readings never
  become Memos. This was the 16th type and tripped the 15-cap.
- **2026-06-15 (owner decision): `Slot` folded to hold the 15-cap.** To restore
  one-in-one-out for the `Reading` addition, `Slot` is folded into a `discovery_status`
  dimension on `DecisionEvent` (`slot_open | filled | qualified`); the `Slot.fill`
  action becomes `DecisionEvent.fill_from_scan`. Rationale: a `Slot` was a discovery-lane
  worksheet row whose durable content is a candidate `DecisionEvent` + gate evidence
  already captured by the gate actions. Roster back to 15.
- **2026-06-15 (owner decision): cap raised 15 → 18; `Buyer` and `Org` seated as types.**
  The 15-cap was borrowed from the venue card set's *instance* cap (12 venues); for a
  whole-domain *type* roster, 18 is the disciplined size. `Buyer` (the qualified ICP
  customer a `Memo` serves — was implicit in the Hard Gate precondition) and `Org` (the
  company/parent a `Brand` rolls up to, the org-motion / G4 anchor, distinct from the
  consumer-facing `Brand`) become first-class. Roster now 17 of 18. Also recorded: a
  `Brand` may act as a `WindCaller` (`Brand —can_act_as→ WindCaller`) — a brand's own
  moves can be the leading indicator.
- **2026-06-15 (cross-vendor delegated review applied; CA-accepted).** A de-correlated
  adversarial review-and-patch (reviewed_by `openai-gpt-5-codex`; authored_by Anthropic
  Claude Opus; commission `docs/prompts/reviews/ontology_backbone_architecture_delegated_review_prompt_v0.md`)
  returned four findings, all CA-adjudicated against cited source and accepted with no
  modification: **AR-01** `Case` row — `claim_tier` / `split` / `entry_basis` demoted from
  standing ontology dimensions to batch-ledger metadata + receipt-backed claim-cap pointers
  (batch-1 ledger "mints no ladder vocabulary"; `claim_tier` is receipt-gated, not
  type-intrinsic); **AR-02** the two load-bearing links specified at their failure edge —
  `derived_from` gains cycle-collapse + multi-parent-union, `diverges_from` gains the
  same-coordinated-layer basis a G2 floor-defeater requires; **AR-03** a self-origin guard so
  a `Brand —can_act_as→ WindCaller` cannot count its own move as an independent G1 origin for
  its own Product/DecisionEvent (`self_originated`, excluded from the independent-origin
  count); **AR-04** live cap language corrected 15 → 18 and the roster marked v0 naming
  authority with build-readiness staged in §9. No `NEEDS_ARCHITECTURE_PASS`. Report:
  `docs/review-outputs/adversarial-artifact-reviews/ontology_backbone_architecture_review_v0.md`.
  This hardening does not adopt the ontology — status stays PROPOSED.
- **2026-06-15 (owner decisions: order-0 ID rule + `claim_tier` uniformity).** (1) **Order-0
  ID-canonicalization decided.** The §2.1 grammar is the single naming authority — producer /
  harness IDs **conform to it**, not the reverse; `case:` / `outcome:` examples normalized to
  the dotted grammar (matching `decision:`); the version suffix (`_v0`) is **metadata, not
  part of the ID** (owner-confirmed 2026-06-15); **IDs are opaque and survive
  rename**. Migrating the live harness `*_v0` IDs into this grammar is a downstream job **owed
  by the harness lane**, not executed by this decision (§2.1, §9). The prior §9 note —
  `derived_from` (origination) authoritative over venue-family for independence — stands.
  (2) **`claim_tier` uniformity (AR-01 residual closed).** `claim_tier` is everywhere a
  receipt-gated evidence-ladder outcome, never type-minted (rule added at §2.2/§2.4);
  `Memo` / `EvidenceUnit` rows keep the field as the *carried* tier, not an intrinsic value —
  no per-row rewrite needed.
- **2026-06-15 (owner adjudication: ADOPT core / RESERVE Buyer + Org).** Owner adjudicated the
  PROPOSED backbone: **adopt the 15-name core** (rows 1–15) as the repo naming / relationship /
  ID authority, and **RESERVE `Buyer` (16) and `Org` (17)** — names held, adoption deferred —
  because both lack a *dedicated landed backing artifact* (their pointers are indirect: Buyer →
  icp/wedge + an *offer hypothesis*; Org → G4 org-motion *corroboration cards*, not an Org-object
  definition). Reserving (not dropping) keeps the names available under the cap (15 adopted + 2
  reserved + 1 open = 18); either is adopted later by dated amendment once a real backing artifact
  lands. Links that depend on a reserved object (`Memo —serves→ Buyer`, `Buyer —owns→
  DecisionEvent`, `Brand` parent-resolution `→ Org`) are **reserved with it** — provisional until
  the object is adopted. Status → `OWNER_ADJUDICATED … AWAITING_MERGE_TO_MAIN`; the merge to `main`
  (which makes adoption live) remains the human gate.
- **2026-06-15 (owner: Press-as-WindCaller; migration approach; reserved-name graduation).**
  (1) **Press / trade outlets are admissible `WindCaller` referents** (§2.2 row 5) — but press is
  the venue-chain *launderer*, so a press call is a *leading* indicator only when it genuinely
  originates; otherwise `derived_from` collapses it to the originating family (no independent-origin
  double-count) — the same guard as Brand-as-WindCaller. (2) **Migration approach = physical
  rename** (owner choice, long-term cleanliness), resolving the assumption-gate's alias-vs-rename
  fork. Caveat carried to scoping: harness IDs are path-structural (case dir names propagated across
  reports / ledgers / `_test_runs` / multiple worktrees) and some are frozen / hash-pinned run
  history — scoping must handle frozen / holdout run artifacts carefully (leave-and-alias or a
  one-time re-pin), not blind-rename. Execution stays gated on adoption-merge + a full inventory
  (assumption-gate P2/P3). (3) **Reserved-name graduation:** `Buyer` graduates when a landed
  buyer / offer (ICP-proof) artifact mints it; `Org` graduates when the in-flight org-motion capture
  producer (EDGAR headcount / org-movement) lands a schema to re-express it against — each via dated
  amendment; fold-fallback for `Org` is a `parent_org` dimension on `Brand` if that producer never
  lands.
- **2026-06-15 (owner: forward-only ID convention — supersedes the "migrate / rename" framing above).**
  The order-0 migration is resolved **forward-only**, NOT by physically renaming existing cases: the
  canonical id is the dotted form; each existing harness `*_v0` id is **kept as the recorded storage
  alias** under its canonical dotted id (on the Case card's `harness_case_id`, which seeds the
  registry); **new cases are born dotted**. Rationale (assumption-gate, source-verified): the harness
  resolves cases by path and `case_id` is an embedded, cross-artifact-asserted field
  (`run_case.py:169`), so renaming sealed / holdout / hash-pinned runs would corrupt provenance; both
  id forms always resolve (nothing deleted), so an old reference never dangles. This **supersedes**
  the "harness `*_v0` IDs migrate / conform by physical rename" wording in the earlier order-0 and
  migration amendments and in §9 item 0; §2.1 now states the forward-only rule.

---

## §7. Option Record + Lock-In

**Architecture result: `TARGET_RECOMMENDED`** (standard profile; directional /
adversarial / grounding perspectives run locally; extraction delegated read-only).

| Option | Shape | Why it loses / wins |
| --- | --- | --- |
| **AO-1 Thin naming + action-gate layer, schema-light** ✅ RECOMMENDED | Owns names, definitions, links, action-gate pointers, ID grammar; property lists stay in owning lanes. | WINS: venue-card-proven anti-rot; low lock-in; does not fork lane schemas; survives a still-evolving demand grammar. Loses: no machine-validated schema (deferred to satellite). |
| **AO-2 Full typed schema** ❌ | Freeze each type's property list now. | LOSES: builds the straitjacket the goal frame forbids; HIGH lock-in; forks lane-owned schemas; rots on the next grammar amendment. |
| **AO-3 One flat ontology (no domain/workflow split)** ❌ | One layer over domain + workflow. | LOSES: rebuilds/forks Layer-2 overlay authority — the worst governance outcome. |
| **AO-4 IDs-later (names now, IDs deferred)** ◑ partial | Defer the ID scheme. | LOSES: forward consumers (read-machinery, scan-spec) need addressable refs now; path-and-prose persists. ADOPT the ID *grammar* now (§2.1), defer the *registry* (§6). |

**Recommended target = AO-1 + domain/workflow split + ID-grammar-now / registry-later.**

**Core / satellite boundary.**
- *Core (v0 owns):* the §2.2 roster names + definitions; the §2.1 ID grammar; the
  §2.3 links (esp. `derived_from` / `diverges_from`); the §2.5 action-gate names +
  preconditions; the §3 backing map; the §6 kernel terms.
- *Satellite (deferred, NOT v0):* property-list schemas (stay in owning lanes); the
  ID registry/resolver/index; `ontology.yaml` enactment; object cards as live
  authority; migrating existing artifacts to stable IDs; any runtime/tooling.

**Invariants later work must preserve.**
1. Layer 2 never mints authority (MAP only).
2. Naming-normative / schema-light — never freeze property lists in the backbone.
3. `derived_from` = independence/laundering (collapse); `diverges_from` =
   divergence/integrity (preserve-as-signal, never average) — both load-bearing.
4. `never_a_feed` is an action constraint, not a new gate.
5. The hard cap (18) holds; growth is one-in-one-out by dated amendment.

**Lock-in the owner is accepting (the §0 lock_in_notice, concretely).** Adoption
makes a repo-wide shared NAMING / RELATIONSHIP / ID-GRAMMAR surface the reference
substrate. Renaming a core object, or changing the two load-bearing links,
propagates to every consumer plus the read-machinery — costly to roll back. This is
accepted deliberately because the compounding benefit (one vocabulary; addressable
cross-artifact references; the moat) requires it. It is bounded by: schema-light
(property lists stay free), the small capped surface, dated amendments, and
PROPOSED-until-owner-signs.

**What would change the recommendation.** If the demand grammar is still materially
unsettled (it is now Q0–Q3 DECIDED, so it is not); if the owner wants a thinner
naming-only layer with no action gates; or if a registry/resolver is needed in v0
(it is not — forward consumers need the grammar, not the registry).

---

## §8. Physical Binding Plan (PROPOSED — NOT enacted)

Adoption (owner-signed) would require, in order:

1. **Create the `docs/product/ontology/` lane.** It is NOT currently an accepted
   lane (the product second-level axis is a closed set; a new lane needs a recorded
   decision). This v0 deliverable is therefore written to the commission's prescribed
   fallback `orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md`.
   - *artifact-folders.md amendment:* add `ontology/` to the bound product-lane set.
   - *repo-structure.yaml amendment:* add `{ name: ontology, status: current }` to
     `product_lanes` and `{ home: docs/product/ontology, entry: docs/product/ontology/README.md }`
     to `docs_roles`.
2. **Add an `ontology.yaml` router (router-only; states no rules).** Mirror the
   `repo-structure.yaml` `{ home, entry }` field grammar and carry the same
   `authority:`/`note: router_only_not_authority_not_validation` disclaimer. It would
   index the object cards; placement/naming authority stays in this doc + the cards.
3. **Author the first object cards** (§9) under the new folder, as dated hints.

None of the above is done here. Adoption is an owner-signed step.

**Doctrine Change Propagation receipt** (adoption would change `architecture_doctrine`
and add an `output_authority` surface; this receipt travels with the PROPOSED design
and is the template the adoption edit must complete):

```yaml
direction_change_propagation:
  doctrine_changed: >
    PROPOSED: Orca adopts a two-layer, naming-normative / schema-light ontology
    backbone — a capped domain object/link/action roster + stable-ID grammar (Layer 1
    BUILD) and a workflow-ontology MAP to existing overlay owners (Layer 2, mints no
    authority) — as the repo's shared semantic reference layer.
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - docs/product/ontology/orca_ontology_backbone_architecture_v0.md   # on adoption (this doc, promoted from the core_spine fallback)
  downstream_surfaces_to_check_on_adoption:
    - .agents/workflow-overlay/artifact-folders.md      # add ontology lane
    - repo-structure.yaml                                # add product_lane + docs_role
    - docs/decisions/orca_repo_structure_binding_v0.md   # record the new lane decision
    - docs/workflows/orca_repo_map_v0.md                 # add ontology lane row
    - .agents/workflow-overlay/source-of-truth.md        # known-source entry
  intentionally_not_updated_now:
    - path: "ALL of the above"
      reason: >
        This is PROPOSED architecture; enacting any binding is an owner-signed
        adoption step. No overlay/router/folder edit is made by this pass.
  stale_language_search: "not_run — PROPOSED design; no source-changing doctrine edit made yet"
  non_claims:
    - not validation
    - not readiness
    - not adoption
    - not folder/router enactment
    - not implementation authorization
```

---

## §9. Smallest Complete Next Routing Object

**After adoption (owner-signed), the build proceeds in this order** — corrected by a
pre-build pass (`workflow-deep-thinking` + `workflow-assumption-gate`, 2026-06-15) that
refuted "build 5 cards first":

0. **The real first object is the ID-canonicalization rule** (an owner decision, not a
   card) — **DECIDED 2026-06-15 (see §2.1, §6.1).** Every card references IDs, and the
   backing artifacts use NON-slug IDs (venue cards `#1–12`, candidate pool `#1–14`, batch
   ledger `*_v0`). Resolution: the §2.1 grammar is the **single authority and producer /
   harness IDs conform to it** — the canonical `brand:` / `venue:` / `case:` are the dotted
   slugs, the live harness `*_v0` case IDs **migrate to them** (a downstream job owed by the
   harness lane), the `_v0` version suffix is **metadata, not part of the ID** (owner-confirmed),
   and **IDs survive rename**. Still encode here, citing the demand-gate closures:
   **`derived_from` (origination) is authoritative over venue-family** for independence
   counting (the card states the pointer; it mints no new rule).
1. **Then author the three cards with landed backing:** `Brand`, `Venue`, `Case`, as
   dated cards. The `Case` card MUST *map* (not restate) the dev/holdout split +
   zero-spoiler discipline to the batch-ledger + evidence-ladder owners (Layer-2 rule).
2. **Defer `Observation` + `TrendVector`** until the in-flight scan-spec lands on `main`,
   so they are designed against a real producer rather than a guessed shape; then
   re-express the scanner's Observation/Candidate schema in ontology terms (no new
   vocabulary).

**Deliberately deferred (satellite):** the remaining cards; the full ID
registry/resolver (beyond the order-0 canonicalization seed); property-list schemas;
migrating existing artifacts to stable IDs; the `WindCaller` card-set asset; demand-side
`Call.grade` / `Outcome` calibration.

**If not adopted:** no further build; the design stays PROPOSED.

---

## §10. Non-Claims

Commission deliverable only — no validation, readiness, proof, adoption,
folder-binding enactment, or implementation authorization. PROPOSED until owner
word. The ontology is naming / relationship / gate-pointer authority by design, not
a new validation or lifecycle authority. Property lists are deliberately not frozen.
`model_lane: unbound`.
