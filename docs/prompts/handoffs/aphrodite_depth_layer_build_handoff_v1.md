# Aphrodite Depth-Layer Build — Cold Handoff v1 (D-1 Dress Rehearsal)

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff packet (cold cross-lane; owner dispatch of this packet IS the bounded build authorization for the rehearsal slice only)
scope: >
  Cold handoff for the Aphrodite depth-layer build lane, superseding
  aphrodite_depth_layer_build_handoff_v0.md (stale per its own stale_if: the
  charter D-1 gate is now ratified, the single-creator rehearsal slice v0
  recommended has since run twice and been graded, and the fragrance ontology
  it listed as a build task now exists). The work unit is the D-1 full dress
  rehearsal: one real creator, all five Vetting Sprint evidence panels,
  operator-runner transport, fit fully DERIVED against
  fragrance_reference_v0.yaml, graded against the ratified six-criteria gate.
  Durable claim-store architecture is explicitly OUT of this lane (gated on
  the capture<->lake sync lane; see Open Decisions).
use_when:
  - The owner dispatches the depth-layer build lane ("read & execute" on this packet).
  - Checking what the D-1 dress rehearsal must produce, what is authorized, and what stays gated.
authority_boundary: retrieval_only
stale_if:
  - Charter section 7 gate 3 (D-1 criteria) is amended.
  - The panel design record or the derived-claim provenance contract is superseded.
  - The capture<->lake sync lane lands its authority split (re-check the claim-store deferral).
  - The rehearsal completes (this packet's work unit is then done; grade record supersedes).
```

## Load Contract

- packet_version: v1 (supersedes `aphrodite_depth_layer_build_handoff_v0.md`)
- mode: max
- created_at: 2026-07-05
- created_by_lane: aphrodite foundation lane (worktree infallible-lederberg-80043c) — provenance only, not authority
- workspace: the Forseti repo (this repository)
- handoff_path: docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md
- expected_branch: receiver works a fresh lane branch/worktree off `main` at or after `8be03976`
- load_rule: confirm-don't-trust — re-verify every load-bearing fact below against its named source before acting; sender claims are hypotheses, not authority.

## Authorization (read this first)

This packet is a planning artifact until the owner dispatches it. **Owner
dispatch ("read & execute" or equivalent) constitutes bounded build
authorization for the rehearsal slice only**, covering: capture refresh of the
one rehearsal creator within existing bounded-session rules if the corpus is
stale; operator-run extraction (model-in-session, versioned recipe, NO API
key/daemon); entity resolution against the ontology; rehearsal-grade claim
records and panel projections; research/product doc writes; and the per-lane
PR flow. It does NOT authorize: roster-scale capture, any standing crawler,
new data-lake lanes or schema, dupe-graph capture (gated on the sync lane),
FLAG-1 resolution, or any buyer contact.

## Goal Handoff

```yaml
goal_handoff:
  long_term_goal: >
    The two-layer Aphrodite moat (charter section 3): a compounding,
    receipt-stamped evidence asset over the niche fragrance-creator roster —
    depth now (ontology + entity-resolved derived claims), time later
    (longitudinal axis) — that makes paid Vetting Sprint reports
    decision-grade and is economically irrational for horizontal incumbents
    to replicate.
  anchor_goal: >
    Fire the ratified D-1 foundation exit gate: run the full dress rehearsal —
    one real captured creator, all five evidence panels (fit, ad-reception,
    purchase-intent, brand adjacency, momentum) rendered via the
    operator-runner transport, fit fully DERIVED against
    fragrance_reference_v0.yaml — and produce the rehearsal sprint report plus
    the bounded-effort receipt that sizes the durable build.
  success_signal: >
    All six ratified D-1 criteria OBSERVED, not asserted (charter section 7
    gate 3): (1) five panels rendered via operator-runner against a real
    captured creator; (2) zero operator-asserted fit facts — every fit element
    resolves to fragrance_reference_v0.yaml coordinates, provable by
    mechanical scan of the claim records; (3) provenance behavior end-to-end
    with at least one honest withhold actually displayed; (4) candidate-set
    assembly exercised with concrete buyer-side product coordinates (register
    row R-3), not stubbed; (5) cross-vendor adversarial review of the
    rehearsal output returns blocker/major-free; (6) a bounded-effort receipt
    (reads/steps/time) recorded. Secondary signal: the rehearsal's failure
    modes and effort receipt are written up as the sizing input for the
    speed-2 durable-store architecture pass. A failed-but-honest rehearsal
    (criteria missed, misses named and sized) is a VALID outcome; a padded
    pass is not.
```

## Open Decision / Fork (receiver routes to owner at dispatch)

- decision: which creator anchors the rehearsal.
  - options: (a) GentsScents — corpus already captured 2026-07-04 (15 videos,
    53,749 transcript words, 591 sampled comments, 85 affiliate links), graded
    A-/A- on fit/ad-reception substrate; refresh only if the owner wants
    recency. (b) A fresh registry creator, if the owner wants to prove the
    method is not GentsScents-shaped.
  - recommendation: (a). The gate tests the pipeline, not creator variety;
    reusing the graded corpus isolates what is actually new (extraction at
    panel grain, resolution, projection, review).
  - owner of the call: owner, at dispatch.
- decision: buyer coordinates for candidate-set assembly (criterion 4).
  - options: (a) a real waitlist-inbound buyer's coordinates if the D-1
    accelerator has fired; (b) a synthetic-but-concrete buyer profile from the
    charter's lead lane (dupe-first/clone house, creator-owned DTC, or
    pre-designer indie), stated as synthetic in the report.
  - recommendation: (b) unless a waitlist signal exists at dispatch; the
    charter's accelerator converts the rehearsal into real Sprint prep if one
    arrives mid-lane.
  - owner of the call: owner, at dispatch.

## Drift Guard

- Panels, never scores: no composite/vanity score anywhere (charter forbidden
  set; panel design section 7 names "should I buy now" synthesis an explicit
  non-goal). Violating this voids the rehearsal as gate evidence.
- No person-level identity or demographic inference; comment author usernames
  are dropped before extraction (rehearsal recipe precedent).
- Missing ≠ zero: absent evidence resolves to an explicit withhold claim
  object, never a zero, never a silent drop. Momentum WILL mostly withhold on
  a single capture cycle — that is correct behavior and satisfies criterion 3;
  do not fake a momentum read to look complete.
- No standing crawler; bounded, self-terminating, pre-authorized capture
  sessions only; account caps per the carve-out.
- Do NOT build durable lake lanes, new silver schemas, or migrate claim
  storage in this lane — that is the speed-2 architecture pass, gated on the
  capture<->lake sync lane (running concurrently in the owner's other lane;
  do not duplicate its work).
- Do NOT resolve or assume FLAG-1 (commercial use / data rights) — it is a
  Phase-1 owner+legal gate and must appear in the first Sprint's scope
  conversation per the ratified rider.
- All grades and reports are `product_learning`-capped: not validation, not
  readiness, not buyer proof.
- The ratified D-1 criteria are frozen (charter section 7 gate 3, register row
  D-1, 2026-07-05). The receiver grades against them; it does not renegotiate
  them.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/README.md` →
  `source-loading.md` (read the overlay README before project work, per
  AGENTS.md). Repo entry: `docs/workflows/forseti_repo_map_v0.md`
  (Decisive-File Quick Index).
- targets to enter the ladder (read in this order):
  1. `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`
     — sections 3, 4, 7 (the ratified gate definition), 8, 9.
  2. `forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md`
     — the display target: fit matrix rules, dupe-space roll-up, buyer-segment
     lead variants, gameability countermeasures, residuals R1–R7.
  3. `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`
     — the seven required fields every derived claim carries; show/downgrade/withhold.
  4. `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
     — the resolution target: houses, products, notes, accords→family mapping,
     tier rubric (in-file), dupe_relationships (EMPTY by honest absence —
     display the panel design's empty-graph text, do not populate it).
  5. `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v0.md` — the
     hand-run recipe this lane promotes to v1 (claim types, hashing rule,
     receipt rule, abstention rules).
  5b. `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md` —
     the adjudicated cross-vendor second opinion on the v1 design (2026-07-05):
     the five-panel claim-type baseline, YouTube adaptations, label sets,
     candidate-set intake schema + synthetic buyer example, failure forecast,
     and rulings M1–M4 that override the raw return where they conflict.
     Recipe v1 is authored FROM this record; do not re-derive from the raw
     v0 recipe alone.
  6. `docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md`
     — the graded substrate this lane most likely builds on.
  7. `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` — the
     Capture ↔ Creator Signal ownership boundary.
- already loaded by sender (weak orientation, 2026-07-05; NOT authority): all
  of the above, plus the v0 handoff and the capture↔lake sync handoff (#712).
- must load first before any strict/actionable step: items 1–4 above, fresh.

### Earlier-decided concepts (essentials inline + verify pointer)

- **D-1 gate ratified 2026-07-05** — six-criteria practice-run + waitlist
  accelerator + FLAG-1 rider; numeric roster thresholds excluded. Verify:
  charter section 7 gate 3 / register row D-1 (merged PR #726).
- **Transport = operator-runner, NO API key** (owner decision 2026-07-05):
  extraction is run by the model in-session under a versioned recipe;
  `run_transcript_product_extract.py` (daemon, key-dependent) is NOT this
  lane's tool. Verify: round-2 grade "not yet run" section names the
  key-blocker this decision routes around.
- **Ontology exists and is the fit substrate** — fragrance_reference_v0.yaml
  merged (#695/#705/#707): Fragrantica-sourced provenance, operator tier
  rubric in-file, accord→family mapping in-file. Chypre vocabulary addition is
  owner-parked; unmapped accords stay accords-only. Verify: the file's own
  header blocks.
- **Panel design adjudicated Mini God Tier** (#717): per-row
  show/downgrade/withhold, no composite; dupe roll-up rule with empty-graph
  honest-absence text; buyer-segment lead variants (dupe-first house reads
  dupe-space first; DTC founder reads audience-taste first; niche house reads
  adjacency first). Verify: the design record itself.
- **Two-speed structure** (sender recommendation the owner commissioned this
  handoff against, 2026-07-05): speed 1 = this rehearsal on rehearsal-grade
  storage (per-creator claim records in the established rehearsal pattern —
  one creator's volume makes later migration near-free); speed 2 = durable
  claim-store home decided in a bounded architecture pass AFTER the
  capture↔lake sync lane lands. Treat as standing unless the owner reopens it
  at dispatch.
- **Rehearsal precedent**: round 1 (jeremyfragrance, D+/C-, substrate-bound)
  and round 2 (GentsScents, A-/A- time-excluded) already ran; the remaining
  gap to A was extraction + ontology — the ontology half is now closed.
  Verify: the two grade records.

## The Work Unit (speed 1 only)

Produce the D-1 dress rehearsal end-to-end on ONE creator:

1. **Corpus** — reuse or refresh the creator's captured substrate (owner
   choice above); freeze it in a corpus record (rehearsal round-1 precedent:
   ordered shortcode/hash list so every corpus-level hash is re-derivable).
2. **Extraction (operator-run, recipe v1)** — promote the v0 recipe per the
   adjudicated second-opinion record (read-first item 5b): the claim-type
   baseline for all five panels, YouTube hashing/receipt/segmentation rules,
   stance + purchase-intent label sets, with rulings M1–M4 applied. Every
   claim: seven provenance fields + provenance_state.
3. **Entity resolution** — mentions → dotted IDs against
   fragrance_reference_v0.yaml; unresolved mentions in an explicit table;
   note-family/tier coordinates come FROM the reference file, never asserted.
4. **Claim records** — per-creator, rehearsal-grade storage (see two-speed);
   mechanically scannable so criterion 2 (zero operator-asserted fit facts)
   is provable by grep/script, not by claim.
5. **Panel projection** — five static, source-backed panels per the panel
   design's display rules (fit matrix rows with per-row provenance state;
   dupe-space section showing the honest-absence text for the empty graph;
   buyer-variant lead ordering for the chosen buyer profile).
6. **Candidate-set assembly** — exercise the buyer-side intake (R-3) with the
   chosen coordinates; record what the intake needed that did not exist.
7. **Cross-vendor adversarial review** — commission per
   `.agents/workflow-overlay/delegated-review-patch.md` (different-family
   reviewer; home-lane adjudication record).
8. **Grade + receipts** — grade against the six criteria; bounded-effort
   receipt (reads/steps/time); failure modes sized as the speed-2 shopping
   list.

## Substrate that already exists (reuse, do not rebuild)

- GentsScents corpus on disk (30 runner invocations, 2026-07-04; note 12 of
  15 videos carry duplicate packets — reads must dedupe newest-per-video).
- Capture runners: `run_source_capture_youtube_caption_packet.py`,
  `run_source_capture_youtube_watch_packet.py`.
- Extraction recipe v0 + derived-claims JSON + ontology-slice pattern
  (docs/research/aphrodite_depth_rehearsal_*).
- fragrance_reference_v0.yaml (the resolution target).
- Creator registry current-view + capture preflight (GentsScents =
  `acct_yt_fragrance_010`, existing_match/allowed).
- Static-projection precedent:
  `creator_signal_multi_creator_library_static_projection_v0.md` pattern.

## Blockers And Risks

- The capture↔lake sync lane is live in the owner's other lane; if it
  restructures capture record locations mid-rehearsal, re-pin the corpus by
  hash before extraction (the corpus record makes this checkable).
- Adversarial review (criterion 5) requires a different-family reviewer lane
  to be available; if unavailable, the rehearsal parks at criterion 5 with
  criteria 1–4 + 6 evidenced — do not substitute a same-family self-review.
- No API key is NOT a blocker (operator-runner decided); do not reintroduce a
  key dependency.

## Recovery / Load Outcomes

- Required checks before work: charter section 7 gate 3 unchanged since
  `8be03976`; panel design + provenance contract present on main; the
  rehearsal-substrate records readable; this packet's Authorization section
  matched against the owner's actual dispatch words.
- REUSE: all match → start at Work Unit step 1.
- STALE_REREAD_REQUIRED: main advanced over any read-first source → re-read
  fresh before acting.
- BLOCKED_DRIFT: D-1 criteria amended, panel design superseded, or dispatch
  words conflict with the Authorization section → stop, route to owner.

## Preflight / boundary receipt

```yaml
output_mode: file-write (this planning packet only)
template_kind: handoff
edit_permission: none granted by this packet alone; owner dispatch grants the bounded rehearsal-slice authorization named in the Authorization section
receiving_lane_first_move: run the Recovery checks, confirm the two owner calls (creator choice, buyer coordinates), then Work Unit step 1
workflow_sequence_policy: overlay_owned
workflow_sequence_source: accepted_project_artifact (charter section 7 gate 3 + this packet)
doctrine_change: none (planning handoff; the rehearsal's own records and any DCP fire in the receiving lane)
non_claims: [not validation, not readiness, not buyer proof, not willingness-to-pay evidence, not commercial-use/data-rights clearance, not roster-scale or lake-schema authorization]
```
