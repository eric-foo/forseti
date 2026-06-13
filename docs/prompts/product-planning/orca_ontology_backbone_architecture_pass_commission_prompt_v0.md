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
status: AUTHORED_2026-06-13_AWAITING_DISPATCH
adjudication_route: ICP / product-direction lane (commissioning thread) adjudicates the returned goal frame + architecture object; owner signs adoption and any folder/router binding.
lock_in_notice: >
  HIGH downstream lock-in by design — this is meant as the repo backbone. A
  wrong early object carve propagates everywhere. That is why this runs as an
  architecture pass with goal-framing first and owner-signed adoption, and why
  v0 is naming-normative / schema-light (see Kernel Discipline). Surfacing this
  tradeoff for an owner decision is part of the commission, not a side note.
```

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
- Base freshness gate: the pinned sources must exist at the pinned sha256
  prefixes (first 16 hex). Missing/drifted → `BLOCKED_STALE_BASE`, report back
  (the commissioning lane's batch may not have landed on `main`).
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

Domain-defining (Layer 1 inputs):
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md` — `B119E24691066E47` — the demand world's primitives (costly behavior, action ceilings, org motion, outcome-memory moat).
- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` — `42787638E6185D4A` — the wedge (which entities matter first).
- `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — `BC478D890419B2B6` — the read grammar (Read, TrendVector, WindCaller, layers); PROPOSED, so treat its types as PROPOSED-strength inputs.
- `docs/product/core_spine/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781` — the best-engineered existing object type (Venue) + the kernel survival terms to steal.
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — `732C65BEBFC31DA1` — Demand-Substrate Hard Gate (an action gate to encode), Memo/Case semantics.
- `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858` — an existing Case/Candidate schema.

Workflow-layer (Layer 2 MAP targets — READ-ONLY, never edit):
- `.agents/workflow-overlay/artifact-roles.md` — `F8365D39800F7604`.
- `.agents/workflow-overlay/artifact-folders.md` — `BA0F05C4E9A8EC81`.
- `.agents/workflow-overlay/source-of-truth.md` — `F7D5CAE3FE42C8E5` (the DCP contract this deliverable must satisfy).
- `docs/decisions/orca_repo_structure_binding_v0.md` — `97903E7827AB181D` — the existing router pattern (`repo-structure.yaml`) to mirror, NOT fork.
- `repo-structure.yaml` — `E84EB865442C40A8` — the machine router precedent for any proposed `ontology.yaml`.

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

Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` (with the gap
list) before applying goal-framing or architecture planning.

## Deliverable

Write to `docs/product/ontology/orca_ontology_backbone_architecture_v0.md`
(PROPOSED). Proposing this new `docs/product/ontology/` lane subfolder is part
of the design; do NOT enact it in `artifact-folders.md` / `repo-structure.yaml`
— if the folder cannot be written under current placement rules, write the
deliverable to `docs/product/core_spine/orca_ontology_backbone_architecture_v0.md`
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
