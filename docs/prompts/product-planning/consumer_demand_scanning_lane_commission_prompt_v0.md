# Consumer-Demand Scanning Lane Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (lane commission — product planning family)
scope: >
  Commission one bounded lane to author the scan-core spec: pipeline step 2
  (scanning / candidate finding) of the owner's 2026-06-12 six-step
  structure. The spec ingests the vertical/venue discovery layer (venue card
  set + screen ledgers + exploration guide), hunts the demand-read taxonomy's
  read types, and feeds capture (step 3) and candidate recording (step 4) in
  two modes (backward/backtest, forward/discovery). Docs-first method spec
  only; no implementation, no scan execution, no capture.
use_when:
  - Dispatching the scanning-lane commission (owner word 2026-06-12, "all the other lanes, prompt out").
authority_boundary: retrieval_only
status: AUTHORED_2026-06-12_AWAITING_DISPATCH
adjudication_route: ICP / product-direction lane (commissioning thread) adjudicates the returned spec; owner signs adoption.
```

## Commission

Author `docs/product/foundation/orca_demand_scan_core_spec_v0.md` (PROPOSED):
the method spec for Orca's scanning function — how an authorized scan walks a
vertical's venues, recognizes decision-shaped demand situations, and emits
structured candidate observations with provenance. The intended decision:
the commissioning lane and owner adjudicate whether this spec becomes the
operating method for both backtest case-finding (backward mode) and
discovery slot-filling (forward mode).

Owner authorization basis (2026-06-12, in-thread): "okay let's prompt this
out to handle - the scanning lane itself... prompt out for scanning so it
feeds into capture perhaps and ingests from vertical venue / discovery."

## Start Preflight (required; `orca_start_preflight` fields)

- Read `AGENTS.md` and `.agents/workflow-overlay/README.md` fresh in your
  session before any work (not supplied by this prompt).
- Source pack: bounded custom pack — the SOURCE-LOAD list below.
- `repo_map_decision: loaded` — `repo_map_reason:` the product-anchor rows
  route thesis/wedge/packet authority; load `docs/workflows/orca_repo_map_v0.md`
  product-anchor section only.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`. Spin up per the
  AGENTS.md isolation rule: fresh worktree or branch off `origin/main`
  (this commission runs alongside active lanes).
- Base freshness gate: the pinned sources below must exist at the pinned
  sha256 prefixes (first 16 hex; verify by recomputing and comparing the
  prefix). If any pinned source is missing or drifted, return
  `BLOCKED_STALE_BASE` to the commissioning lane instead of proceeding —
  the commissioning lane's batch may not have landed on `main` yet.
- Dirty-state allowance: fresh worktree, clean; only your own new files may
  be dirty/untracked. Never touch other lanes' files.
- Edit permission: `docs-write`, limited to the single deliverable path and
  (if needed) a `docs/hygiene/queue.md` row. Read-only on everything else.
- Output mode: `file-write`.
- Doctrine boundary: the deliverable is PROPOSED method spec — not doctrine.
  If your work would require changing thesis, wedge, packet, overlay, or any
  owner-locked record, stop and route the conflict back; do not edit.
- External source boundary: no public web research in this commission (the
  spec is built from in-repo material). `jb` is not Orca authority; external
  workflow source is read-only.

## Method And Source Contract (source-gated)

REFERENCE-LOAD `workflow-deep-thinking` (option discipline for spec choices).
Do not APPLY it before `SOURCE_CONTEXT_READY`.

SOURCE-LOAD (pins = sha256 first-16-hex at authoring):

- `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — `BC478D890419B2B6` — the hunting grammar (PROPOSED; owner adjudication may amend it — check its Status block for a dated owner word before treating any part as fixed).
- `docs/product/foundation/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781` — the venue layer: 12 cards, NEWSY/SUBTLE chain, access shapes, wind-caller exemplar (card 11).
- `docs/product/foundation/orca_vertical_exploration_guide_v0.md` — `EF9F5C6E716E9857` — the existing screen procedure (the scanning function's working prototype; three screens already ran under it).
- `docs/product/foundation/orca_memorization_resistant_case_finder_frame_v0.md` — `C672C1678F98878F` — the backward-mode predecessor frame; reconcile, do not duplicate.
- `docs/product/foundation/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858` — backward-mode output shape (candidate observations as practiced).
- `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md` — `48B5534E056FD42A` — forward-mode consumer: slot columns + record homes + the pool-is-never-a-slot-source bar.
- `docs/decisions/orca_product_thesis_consumer_demand_v0.md` — `B119E24691066E47` — costly-behavior primitive, integrity labels, US-first geography, capture risk posture (ask-1 amendment).
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — `732C65BEBFC31DA1` — Demand-Substrate Hard Gate (the columns scanning must make checkable).

Declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the gap
list) before applying any method or drafting the spec.

## Scope And Deliverable

One artifact: `docs/product/foundation/orca_demand_scan_core_spec_v0.md`
(PROPOSED), containing at minimum:

1. **Hunting grammar**: how a scan recognizes each read type (convergence,
   divergence, brand-decision event) from the taxonomy, per venue class
   (NEWSY vs SUBTLE). Explicit anti-triggers (complaint volume is never a
   trigger — note its PROPOSED status and the price-rerouting exception).
2. **Walk order**: how a scan consumes the card set (Step-0 read, chain
   order, fail-soft card handling, dead/thin list respected).
3. **Candidate observation schema**: brand, product/SKU, signal type (read
   type + layer), venue family, dates, provenance (link + retrieval date),
   decision relevance, mode flag — reconciled with the pool handoff shape
   (backward) and the brief's slot columns (forward).
4. **Two modes, one core**: backward (backtest case-finding; outcome-bearing,
   facilitator-side; contamination posture stated) and forward (discovery;
   outcome-free; freshness/decay rule — a live 30-90-day decision read goes
   stale in weeks; state the maximum scan-to-use age).
5. **Handoff contracts**: what the scan emits to capture (step 3 — what to
   capture, under capture-lane route bindings it never overrides) and to
   candidate recording (step 4 — pool shape or brief slots).
6. **Wind-caller sub-procedure**: per sub-niche, how candidate wind callers
   are identified and recorded (channel-level only; person-level dossiers
   forbidden), and what a calibration-ready call record looks like.
7. **Reconciliation note**: what this spec absorbs from the exploration guide
   and the case-finder frame, and what it leaves to them.

## Hard Constraints

- Docs-first: no implementation, code, automation, dashboards, or runners.
- No scan execution, no capture, no web research, no outreach in this lane.
- US-market default; non-US handling mirrors the pool/brief obligations.
- Capture route bindings are capture-lane-owned; the spec may cite, never set.
- The backtest candidate pool is never a forward-mode slot source.
- Smallest complete intervention; dated amendments, never silent rewrites.

## Output Contract

`file-write`. On completion: write the deliverable, then return to the
commissioning thread a headed human summary (what the spec binds, what it
deliberately leaves open, conflicts found) plus path + sha256 receipt. The
commissioning ICP / product-direction lane adjudicates; owner signs adoption.
If blocked, return the precise blocker instead of a partial spec.

## Non-Claims

Commission only — no validation, readiness, proof, scan authorization,
capture authorization, or implementation authorization. The deliverable is
PROPOSED until owner word. `model_lane: unbound` (dispatch is the owner's
choice).
