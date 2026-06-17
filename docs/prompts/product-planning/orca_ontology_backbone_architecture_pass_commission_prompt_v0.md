# Orca Ontology Backbone — Architecture-Pass Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (architecture-pass lane commission — product planning family)
scope: >
  Commission one bounded architecture-planning lane to design Orca's shared
  semantic backbone (a Foundry-Ontology-style domain ontology) in two layers:
  a domain object/link/action layer to BUILD, and a workflow-ontology layer to
  MAP onto existing overlay authority (never rebuild). The lane runs
  goal-framing first, then architecture planning, and returns a PROPOSED
  architecture object — NOT an implementation, not the object cards
  themselves, not the folder/router enactment. The commissioning ICP /
  product-direction lane adjudicates; the owner signs adoption.
use_when:
  - Dispatching the ontology backbone architecture-pass commission (owner word 2026-06-13, "prompt out for this ontology with your structure, make them do goal framing").
authority_boundary: retrieval_only
status: AUTHORED_2026-06-13; REFRESHED_2026-06-14; PIN_TIDIED_AND_DISPATCHED_2026-06-15
adjudication_route: ICP / product-direction lane (commissioning thread) adjudicates the returned goal frame + architecture object; owner signs adoption and any folder/router binding.
lock_in_notice: >
  HIGH downstream lock-in by design — this is meant as the repo backbone. A
  wrong early object carve propagates everywhere. That is why this runs as an
  architecture pass with goal-framing first and owner-signed adoption, and why
  v0 is naming-normative / schema-light (see Kernel Discipline). Surfacing this
  tradeoff for an owner decision is part of the commission, not a side note.
```

## Applied-Contract Record (prompt-orchestration)

This 2026-06-14 refresh was authored under owner instruction ("/workflow-deep-thinking
propose ontology prompt, /workflow-delegated-review-patch the prompt after"), which
under the source hierarchy (explicit current-turn instruction > AGENTS.md > overlay)
sets the method. Per `.agents/workflow-overlay/prompt-orchestration.md` (validation
gate 1: "apply this file's contract in full and record that"), the contract was
applied: source-loading per `source-loading.md` (current product docs swept; the
SOURCE-LOAD below refreshed to landed `main`, #78/#88); the source-gated method
contract (REFERENCE-LOAD → SOURCE-LOAD → `SOURCE_CONTEXT_READY` → APPLY) preserved;
required preflight, `file-write` output mode, artifact roles, validation gates, and
non-claims preserved from v0 with the Base freshness gate updated for the live
grammar docs. This refresh updates the commission's inputs and candidate roster to
the landed grammar; it does not change prompt doctrine, so it carries no
`direction_change_propagation` of its own — the dispatched lane's deliverable still
carries one, as required below. A `workflow-delegated-review-patch` hardening pass
follows (owner instruction); its `reviewed_by` / `authored_by` provenance is recorded
on the review output.

## Pin Tidy + Applied-Contract Record (2026-06-15 — dispatch-time sha re-sync)

At dispatch the 8 sha-pinned sources were re-verified against the frozen base
`origin/main @ 953af7ea`. Six had drifted forward since the 2026-06-14 refresh and
were re-pinned to current values; all six drifts are non-material to the object
carve:

- `orca_icp_wedge_consumer_demand_first_v0.md` `42787638E6185D4A → B4EC557D024C6397`
  (wind-caller calibration carve-out, already reflected in the live grammar);
- `.agents/workflow-overlay/artifact-roles.md` `F8365D39800F7604 → A9BEC91DB82E81D1`,
  `artifact-folders.md` `BA0F05C4E9A8EC81 → 14B136BBD117425F`,
  `source-of-truth.md` `F7D5CAE3FE42C8E5 → 94E3C63F551E3C71` (Layer-2 MAP targets —
  appended DCP receipts / role rows; read live as map targets regardless of exact sha);
- `orca_repo_structure_binding_v0.md` `97903E7827AB181D → 44D1AB274FD7946A`
  (receipt sweep) and `repo-structure.yaml` `E84EB865442C40A8 → 776EE1324C356BC8`
  (a home-row addition) — mirrored as a pattern, not copied.

`beauty_venue_card_set_v0.md` (`65E22CDAE5EDE781`) and
`consumer_demand_candidate_pool_handoff_v0.md` (`19009D43A7C29858`) were unchanged.
The LIVE (verify-don't-pin) demand-grammar sources were all present at the frozen base.

Applied-contract record: this is a mechanical freshness re-sync under
`.agents/workflow-overlay/prompt-orchestration.md` (consistency-judged, fitness-gate
exempt per its "vocabulary-enforcement / provenance-correction" class). The full
prompt-orchestration contract was applied directly (the same "apply this file's
contract in full and record that" route as the 2026-06-14 refresh): preflight,
`file-write` output mode, artifact roles, validation gates, retrieval header, and
non-claims are preserved; no input, candidate roster, instruction, or doctrine
changed, so it carries no `direction_change_propagation` of its own. Owner
instruction basis: "tidy 3 pins, then dispatch" (2026-06-15); the count was
corrected to 6 drifted of 8 pinned on re-verification.

## Refresh Note (2026-06-14 — design against the current grammar, not the 2026-06-13 snapshot)

Since this commission was authored (2026-06-13), the demand-read grammar was
overhauled and owner-adjudicated; the changes are now on `main` (PRs #78, #88).
The dispatched lane MUST design against the current grammar:

- **Demand-state model (replaces "durable vs hollow").** Two independent axes —
  **durable vs transient** (persistence) × **real vs manufactured** (integrity) —
  → three actionable states: durable (commit), transient (move, time-boxed),
  manufactured (discount/avoid). "Hollow" is RETIRED. `Read` (and `Call`/`Outcome`)
  carry this two-axis classification, with a derived action state only where
  useful; do not collapse the integrity axis into the persistence axis.
- **Calling sequence = a `Read` lifecycle (governed Actions).** A read opens
  **transient** (act in-window), is **monitored**, then **earns** the upgrade to
  durable or **decays** — model it as the Read state machine
  (`open_transient → monitor → earn_durable / decay`), each with its gate.
- **Action ceiling + horizon are typed** (long-horizon *commit* vs short-horizon
  *move*, capped by signal integrity); the **never-a-feed invariant** (every output
  is a calibrated decision with an action ceiling, never a feed) is a constraint to
  encode.
- **Q0–Q3 are DECIDED** (not "PROPOSED-strength"): demand-state model (Q0); pricing
  refinement (Q1); wind-caller primacy **"at the trigger" / calibration-gated** (Q2);
  channel-vs-person boundary **refined** (Q3 — named public-figure calibration,
  **non-permanent**, the ≤5/attended capture cap **platform-scoped**, external/product
  boundary unchanged). Encode the WindCaller boundary into its object definition.
- **Gate actions** are now defined (demand-gate closures): **G1** independence by
  de-correlated origination, **G2** costly-behavior floor, **G4** org-motion
  corroboration (separate from G1) — encode as Gate actions/preconditions, routed to
  their owners, not rebuilt.

The SOURCE-LOAD and candidate roster below are updated accordingly.

## Commission

Design the Orca ontology backbone: the one shared, governed semantic layer
that every lane, scan, backtest, capture, judgment, and proof artifact
references instead of each re-inventing its own schema over raw material. The
intended decision (owner's, after this lane adjudicates): adopt the proposed
ontology as the repo's semantic backbone, and authorize its physical binding.

Owner authorization basis (2026-06-13, in-thread): "i feel that we should
heavily adopt palantir's ontology to make our workflows flow extremely
smoothly especially for this entire project... this would serve as the
backbone for the whole repo probably" + "prompt out for this ontology with
your structure, make them do goal framing."

This is an architecture pass (it touches architecture doctrine, workflow
authority, and output authority). Run the Orca Cynefin routing layer before
planning. The deliverable carries a `direction_change_propagation` receipt
(or a `direction_change_propagation_blocker`) per
`.agents/workflow-overlay/source-of-truth.md` because adoption would change
durable doctrine.

## What "ontology" means here (the four commitments to steal)

Strip the platform; keep the discipline. A Foundry-style ontology is four
commitments, and the lane must design all four:

1. **Object types** — semantic entities with stable identity and a definition
   (Vertical, Brand, Venue, WindCaller, Observation, Case, Outcome, Memo, …).
2. **Links** — typed relationships between object types (WindCaller —made→
   Call —graded-by→ Outcome; Observation —from→ Venue —supports→ Read).
   Two links the demand-gate independence work requires (added 2026-06-13):
   **`Observation —derived_from→ Observation`** (the provenance/laundering edge
   — two observations on one `derived_from` chain are NOT independent; this is
   the de-correlation mechanism behind the Demand-Substrate Hard Gate's
   independent-venue requirement) and
   **`Observation —diverges_from→ Observation`** (cross-layer disagreement — the
   integrity / astroturf-tell signal, preserved as signal, never averaged away).
   These two links are now **load-bearing** (owner-decided in the demand-gate
   closures, 2026-06-13/14), and the judgment-spine read-machinery
   (`docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md`)
   is a **forward consumer** that depends on them — design them precisely enough for
   that consumer's de-correlation + divergence weighting. The lane finalizes the
   roster; these enter as candidate links, not frozen.
3. **Actions** — the governed state transitions that are the ONLY sanctioned
   ways an object changes state, each with its precondition/gate (Case.seal
   requires a pre-declared ledger row; Slot.fill requires a dated scan doc;
   Call.grade requires an outcome receipt). Most of these gates ALREADY exist
   in prose across the repo; the ontology makes them addressable, it does not
   invent new ones.
4. **Backing mapping** — every object type names the artifact(s) that
   instantiate it (Venue ← the venue card set; Case ← the batch-1 ledger),
   the Foundry "backing dataset" analog.

## Two Layers (the required structure)

**Layer 1 — Domain ontology (BUILD).** The demand world. Author the object-type
roster, links, actions, and backing map. Candidate object types to evaluate
(roster is the lane's to finalize, under the cap): Vertical, SubNiche, Venue,
Brand (with parent resolution), Product/SKU, WindCaller, Call, Observation,
CapturePacket, EvidenceUnit, TrendVector, Read, DecisionEvent, Case, Outcome,
Memo, Slot. Assign stable IDs (`brand:beautypie`, `case:bt-beautypie-repricing-2023`)
so cross-artifact references stop being path-and-prose.

Demand-state machinery to evaluate (added 2026-06-14, under the same cap — these
may be dimensions/actions on existing types rather than new types; the lane
decides): the two-axis demand-state classification on Read/Call/Outcome
(`persistence_state: durable|transient`, `integrity_state: real|manufactured`),
plus a derived action state (`durable`, `transient`, `manufactured`) only where
that helps downstream consumers; the **Read lifecycle Actions**
(`open_transient → monitor → earn_durable / decay`); an `ActionCeiling` enum
(commit/move + the frozen ladder) as a governed transition; the **Gate** actions
`G1`/`G2`/`G4` (demand-gate closures); the **never-a-feed** invariant as an
action constraint on recurring reads; and a `claim_tier` dimension (evidence
ladder) on Memo/Case/Outcome/Read. The `WindCaller` object encodes the carve-out
boundary (non-permanent, platform-scoped capture cap, internal-use,
external/product boundary unchanged) and calibration-gated trigger primacy (Q2).
Respect the cap — fold these into existing types where they are dimensions, not
new objects.

**Layer 2 — Workflow ontology (MAP, do NOT rebuild).** Lanes, artifact roles,
claim tiers, gates, receipts, folders ALREADY have owners in the overlay.
Layer 2 POINTS at them (one card each: `backed_by: artifact-roles.md`, etc.).
Rebuilding or restating this layer would fork authority — the single worst
outcome for this repo's governance. Route, don't restate. If a workflow
concept has no clean owner, name the gap; do not mint a competing authority.

## Kernel Discipline (steal the venue card set's survival terms)

The venue card set is the proven antidote to ontology rot; adopt its kernel:

- **Hard cap** on v0 domain object types (propose ~15; the cap is a survival
  term, "16th in = one out"), with an owner and per-card review dates.
- **Dated amendments only**, never silent rewrites; fail-soft cards (dated
  hints, not current-state claims).
- **Naming-normative, schema-light (load-bearing).** v0 OWNS names,
  definitions, links, and action gates. It does NOT freeze property lists —
  those keep evolving in their owning lanes and are tracked only via the
  backing mapping. This is what keeps a backbone from becoming a straitjacket;
  state it as an explicit authority boundary of the ontology.

## Start Preflight (required; `orca_start_preflight` fields)

- Read `AGENTS.md` and `.agents/workflow-overlay/README.md` fresh before any
  work (not supplied by this prompt).
- Source pack: bounded custom pack — the SOURCE-LOAD list below.
- `repo_map_decision: loaded` — `repo_map_reason:` an ontology survey needs the
  repo map's product-anchor + lane rows to locate the proto-schemas; load
  `docs/workflows/orca_repo_map_v0.md`.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`. Spin up per the AGENTS.md
  isolation rule: fresh worktree or branch off `origin/main` (runs alongside
  many active lanes).
- Base freshness gate: the sha-pinned stable sources must exist at the pinned
  sha256 prefixes (first 16 hex). The LIVE demand-grammar / gate sources
  (thesis, taxonomy, adjudication companion, buyer-proof, demand-gate closures,
  and discovery brief where surveyed) are NOT sha-pinned — instead verify the
  2026-06-14 demand-state model + Q0–Q3 adjudication and the applied gate-closure
  model are present in the current `main` text (durable/transient/manufactured +
  calling sequence, not the retired durable-vs-hollow framing; G1 origination
  independence, G2 costly-behavior floor, G4 org-motion corroboration). Either
  check failing → `BLOCKED_STALE_BASE`, report back.
- Dirty-state allowance: fresh worktree, clean; only the lane's own new files
  may be dirty/untracked. Never touch other lanes' files.
- Edit permission: `docs-write`, limited to the deliverable path(s) below and
  optionally a `docs/hygiene/queue.md` row. READ-ONLY on every surveyed
  source — especially the overlay (Layer 2 maps it, never edits it).
- Output mode: `file-write`.
- Doctrine boundary: the deliverable is PROPOSED architecture, not enacted
  doctrine. Do NOT enact the folder binding, edit `repo-structure.yaml`,
  edit `artifact-folders.md`, or write any object card as live authority; those
  are owner-signed adoption steps. Propose them in the design.
- External source boundary: no public web research. `jb` is not Orca authority.

## Method And Source Contract (source-gated)

REFERENCE-LOAD, in this order, and do not APPLY any until
`SOURCE_CONTEXT_READY`:

1. `workflow-goal-framing` — run FIRST. Produce the goal frame (the user-owned
   long-term goal this backbone serves, the anchor goal, the success signal)
   before any architecture option work. The ontology is a means; name the end
   it serves and the signal that it is working.
2. `workflow-architecture-planning` — run SECOND, against the goal frame:
   compare cross-cutting options (e.g., thin naming-layer vs full typed schema;
   one ontology vs domain/workflow split; IDs-now vs IDs-later), define the
   core/satellite boundary, preserve deferred implementation implications, and
   name the smallest complete next routing object.

SOURCE-LOAD (pins = sha256 first-16-hex at authoring, current base):

Domain-defining and gate-defining (Layer 1 inputs). The demand-grammar docs
(thesis, taxonomy, adjudication companion, buyer-proof) and the gate-closure /
discovery sources named LIVE below were amended or applied 2026-06-14 (#78,
#88): do NOT pin them to an old sha — read current `main` and verify the
demand-state model + Q0–Q3 adjudication and applied gate-closure model are
present (NOT the retired durable-vs-hollow framing or stale raw venue-count gate
wording); if absent → `BLOCKED_STALE_BASE`. Stable docs keep their sha pins.
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md` — LIVE (verify, don't pin) — the demand world's primitives (costly behavior, action ceilings, org motion, outcome-memory moat) + the 2026-06-14 demand-state amendment (durable/transient/manufactured, calling sequence, never-a-feed, differentiation floor).
- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` — `B4EC557D024C6397` — the wedge (which entities matter first).
- `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — LIVE (verify, don't pin) — the read grammar (Read, TrendVector, WindCaller, signal layers, read types, calling sequence); Q0–Q3 DECIDED, treat its types as DECIDED inputs (the artifact status line may still read PROPOSED).
- `docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md` — LIVE (verify, don't pin) — the operative definitions (what-counts / anti-trigger / boundary per layer + read type) and the Q0–Q3 owner-decision outcomes; the firmest source for Read / WindCaller / Call definitions.
- `docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md` — LIVE (verify, don't pin) — the APPLIED G1 (independence by de-correlated origination) / G2 (costly-behavior floor) / G4 (org-motion corroboration, separate from G1) gate definitions to encode as Gate actions/preconditions. Encode as live gate semantics and flag any consuming surface that still carries stale raw-venue-count wording.
- `docs/product/foundation/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781` — the best-engineered existing object type (Venue) + the kernel survival terms to steal.
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — LIVE (verify, don't pin) — the Demand-Substrate Hard Gate (independence rests on `derived_from`, divergence/astroturf on `diverges_from`) + the never-a-feed invariant (Orca Promise) + Memo/Case semantics. (Carries some pre-2026-06-14 durable-vs-hollow wording flagged for realignment — read the current Hard Gate + Orca Promise, not the stale framing.)
- `docs/product/foundation/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858` — an existing Case/Candidate schema.

Workflow-layer (Layer 2 MAP targets — READ-ONLY, never edit):
- `.agents/workflow-overlay/artifact-roles.md` — `A9BEC91DB82E81D1`.
- `.agents/workflow-overlay/artifact-folders.md` — `14B136BBD117425F`.
- `.agents/workflow-overlay/source-of-truth.md` — `94E3C63F551E3C71` (the DCP contract this deliverable must satisfy).
- `docs/decisions/orca_repo_structure_binding_v0.md` — `44D1AB274FD7946A` — the existing router pattern (`repo-structure.yaml`) to mirror, NOT fork.
- `repo-structure.yaml` — `776EE1324C356BC8` — the machine router precedent for any proposed `ontology.yaml`.

Survey (DISCOVER and read; do not pin — confirm exact paths via the repo map):
the remaining proto-schemas the ontology must reconcile — the capture packet
schema (`docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md`),
the judgment-spine EvidenceUnit / evidence-ladder binding
(`docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
and any `evidence_binding` artifact), the discovery brief's slot columns, and
the batch-1 ledger's case rows. The scan-core spec
(`orca_demand_scan_core_spec_v0.md`) is IN-FLIGHT (PROPOSED, in a separate
worktree, not yet on `main`): treat its observation/candidate schema as a
forward consumer to design FOR, not a landed source to pin; if it is on `main`
by dispatch, read it.

Also survey (do not pin; confirm paths via the repo map): the judgment-spine
gate-ownership map (`docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md`)
— so Gate actions MAP to their owning gates rather than rebuild them; the
evidence-ladder architecture (`docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`)
— the `claim_tier` dimension on every object; the discovery brief
(`docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`)
— the `Slot` object's columns and state machine; and the read-machinery handoff
(`docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md`)
— a forward consumer that depends on `derived_from` / `diverges_from`.

Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` (with the gap
list) before applying goal-framing or architecture planning.

## Deliverable

Write to `docs/product/ontology/orca_ontology_backbone_architecture_v0.md`
(PROPOSED). Proposing this new `docs/product/ontology/` lane subfolder is part
of the design; do NOT enact it in `artifact-folders.md` / `repo-structure.yaml`
— if the folder cannot be written under current placement rules, write the
deliverable to `docs/product/foundation/orca_ontology_backbone_architecture_v0.md`
instead and flag the folder proposal in the design. The deliverable contains:

1. **Goal frame** (from step 1): the end this backbone serves + success signal.
2. **Layer 1 — domain ontology design**: the capped object-type roster (each:
   one-line definition, stable-ID scheme, key states, governed actions + their
   existing gate, links, backing artifact[s]); the link map; the action/gate
   map (citing where each gate already lives).
3. **Layer 2 — workflow ontology MAP**: one pointer card per workflow concept
   to its existing overlay owner; named gaps where no owner exists (no new
   authority minted).
4. **Kernel discipline**: cap, owner, review dates, dated-amendments,
   naming-normative/schema-light boundary — stated as the ontology's own
   survival terms.
5. **Physical binding plan (PROPOSED, not enacted)**: the `docs/product/ontology/`
   folder, an `ontology.yaml` router (router-only, mirroring repo-structure.yaml;
   never states rules), and the `artifact-folders.md` + `repo-structure.yaml`
   amendments adoption would require — with the DCP receipt.
6. **Smallest complete next routing object**: what builds first after adoption
   (e.g., the first N object cards, or the scan-spec schema re-expressed in
   ontology terms), and what is deliberately deferred.
7. **Option record + lock-in**: the cross-cutting options compared, the
   recommendation, and the named lock-in cost the owner is accepting.

## Hard Constraints

- Architecture/design only: no implementation, code, runtime, `ontology.yaml`
  enactment, object-card authoring as live authority, or folder-binding edits.
- MAP, do not rebuild Layer 2: zero edits to overlay authority; no competing
  authority surface.
- Respect the cap; naming-normative / schema-light v0 (do not freeze property
  lists).
- Smallest complete intervention; dated amendments, never silent rewrites.
- No new implementation folders (`src`, etc.); no resolver/skill changes.

## Output Contract

`file-write`. On completion: write the deliverable, then return to the
commissioning thread a headed human summary (the goal frame in one line, the
object-type roster, the recommended option + lock-in cost, the binding plan,
the smallest next object) plus path + sha256 receipt, and the DCP receipt. The
commissioning ICP / product-direction lane adjudicates; the owner signs
adoption and the folder/router binding. If blocked (Cynefin routes it out,
goal frame cannot be established, or base is stale), return the precise
blocker instead of a partial design.

## Non-Claims

Commission only — no validation, readiness, proof, adoption, folder-binding
enactment, or implementation authorization. The deliverable is PROPOSED until
owner word. The ontology is naming/relationship/gate authority by design, not
a new validation or lifecycle authority. `model_lane: unbound` (dispatch is
the owner's choice).
```
