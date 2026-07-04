# Handoff Packet — Aphrodite Fragrance Sub-Ontology Build

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff packet (cold cross-lane handoff — planning artifact, NOT a build authorization)
scope: >
  Cold handoff for building the Aphrodite fragrance sub-ontology: fragrance
  reference data (houses, products, note families, accords, price tiers,
  dupe-relationships, occasion/season vocabulary) as DATA on the adopted Orca/
  Forseti ontology backbone, so the Creator Signal fit read becomes a structured
  match instead of a flat description. Built to be cold-agent-usable and
  provenance-backed. Surfaces the creator-entity modeling fork as an open owner
  decision. Executing it needs explicit owner build-authorization; this packet
  grants none.
use_when:
  - A fresh lane is authorized to build the Aphrodite fragrance sub-ontology and needs the full context cold.
  - Checking what the live ontology substrate is, what the build must conform to, and the open creator-entity decision.
authority_boundary: retrieval_only
stale_if:
  - The ontology backbone, its SSOT (ontology.yaml), or the expansion backlog is amended or superseded.
  - The creator-entity modeling fork is decided by the owner (replace the Open Decision block).
  - origin/main advances such that the pinned compare targets below no longer resolve.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-07-04
- created_by_lane: `claude/priceless-gagarin-19ddd2` (Aphrodite depth-rehearsal lane; SENDER — provenance only, not authority)
- workspace: the Orca/Forseti repo (github `eric-foo/orca`)
- handoff_path: `docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md`
- **start from `origin/main`, NOT the sender branch.** origin/main @ `6a998ddc` (or later). The sender branch is on the pre-migration `orca/` path scheme; main migrated `orca/ → forseti/` (PR #666). All ontology paths below are `forseti/` on main.
- expected_dirty_state: this handoff file is newly created and untracked on the sender branch until committed.
- load_rule: confirm-don't-trust. Every load-bearing fact below carries a compare target on `origin/main`; re-verify against it before acting. Sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: >
    Cash the Aphrodite "depth-now" moat: turn captured creator content into
    entity-resolved, receipt-stamped derived claims that make the Creator Signal
    Vetting Sprint report decision-grade for a niche-complete fragrance roster
    (per `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`).
- anchor_goal: >
    Build the fragrance sub-ontology — houses, products, note families, accords,
    price tiers, dupe-relationships, occasion/season vocabulary — as schema-light
    DATA on the adopted ontology backbone, so the fit panel's product-tier and
    note-family components become DERIVED (resolved against the ontology) instead
    of operator-asserted, and the fit read becomes a structured match between a
    creator's coverage footprint and a buyer's product.
- success_signal: >
    A cold agent, from main's standard entry points and within the source-loading
    budget, resolves an arbitrary fragrance to its canonical `product:` id with
    note-family / tier / dupe data AND its provenance; the four ontology hooks
    stay green on the addition; and ≥80% of the products the two depth rehearsals
    surfaced resolve to a sub-ontology entry. See Success Signals below for the
    full testable set.

## Open Decision / Fork

- decision: **How does the creator ENTITY sit in the ontology?** (Does NOT block the fragrance reference-data build; the houses/products/notes are vertical data regardless. Resolve before the creator entity is referenced by stable ontology id.)
  - options:
    - **(A) Creators = `WindCaller` card-set.** The backbone models `windcaller:` as "a leading-indicator account/community/detector" and lists WindCaller as *deferred, awaiting a card-set asset parallel to the venue cards* (`ontology_expansion_backlog_v0.json`). Fragrance creators could be that asset (`windcaller:youtube.gentsscents`). Spends no new type slot.
    - **(B) New capped `Creator` type.** Spends the ONE open slot in the 18-type cap ("19th in = one out"). Owner-signed, high lock-in. Models the vetting-subject role honestly.
    - **(C) Creators stay Capture-registry entities, ontology-referenced.** The Capture-owned creator registry keeps creator rows; the ontology references them by id but mints no ontology type. No cap pressure; respects the Capture↔Creator-Signal spine boundary.
  - already constrained / off the table: minting a new capped type WITHOUT owner sign-off (the cap is owner-signed, §6/§6.1 of the backbone). Forking the SSOT or Layer-2 authority.
  - trade-offs: (A) reuses an existing noun but bends its "demand leading-indicator" meaning to fit "vetting subject"; (B) honest modeling but permanent cap spend; (C) cleanest boundary + zero cap cost but the creator is not a first-class ontology citizen.
  - owner of the call: Eric (ontology owner per backbone §6).
  - recommendation and why: **Lean (C).** The spine promotion binding (`.../creator_signal/...` charter + `orca_creator_signal_spine_promotion_binding_v0.md`) already places creator identity in Capture, not the product ontology. The fit read needs only `product:`/`brand:`/note data plus the creator's mention footprint (already in the registry + captures). (C) spends no cap slot and defers the high-lock-in roster decision until a proven need. Surface, do not auto-decide.

## Drift Guard

- **Schema-light: fragrance specifics are DATA, never new frozen schema or a new capped type.** Backbone §6 kernel rule + charter high-lock-in decision #4 ("vertical specificity as data, not schema"). Violating it forks the backbone and spends lock-in the owner did not authorize.
- **Do not spend the one open type slot** (add a `Creator`/`Fragrance` type) without the Open Decision resolved by the owner. The cap is owner-signed.
- **Work on `forseti/` paths on current main, not `orca/`.** origin/main migrated orca/→forseti/ (PR #666). Any `orca/...` path is stale.
- **Conform to the live ontology machinery; do not build a parallel one.** The SSOT is `ontology.yaml`; new deferred-type graduation goes through `ontology_expansion_backlog_v0.json` + `ontology_cards/`; the four hooks gate it. Adding a sub-ontology outside this is a fork, not an extension.
- **Respect the Capture ↔ Creator Signal boundary.** Creator Signal owns display/claim language; Capture owns the registry, capture, and computation. The sub-ontology is reference data (a foundation-spine concern), not a Creator-Signal display artifact and not a Capture runner.
- **This is foundation-stage.** Not the sellable Vetting Sprint; authorizes no capture, no roster build, no selling. FLAG 1 (commercial-use/data-rights) is untouched and remains a Phase-1 owner+legal gate.
- **Provenance is co-#1, not optional.** A retrievable ontology of unsourced/hallucinated fragrance facts is a liability — it launders vibes into buyer-facing claims. Every fact carries a source or an explicit `operator_asserted_pending_source` marker; nothing bare ships as authoritative.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (+ `AGENTS.md`, `.agents/workflow-overlay/README.md` first). Run the Forseti start-preflight.
- targets to enter the ladder (all on `origin/main`, `forseti/` scheme):
  - `forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md` — the adopted naming/relationship/ID authority (human rationale; governs on conflict).
  - `forseti/product/spines/foundation/ontology/ontology.yaml` — the machine-readable SSOT (namespaces, type roster, dimensions). Load this to see `product:`, `brand:`, `vertical:beauty.fragrance`, `windcaller:`.
  - `forseti/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json` — deferred-type backlog; note `Product` ("card when a Product backing lands") and `WindCaller` ("no card-set asset yet") are deferred — the fragrance sub-ontology is a plausible `Product` backing.
  - `forseti/product/spines/foundation/ontology/ontology_cards/` (README + `brand_beautypie_v0.md`, `venue_basenotes_v0.md`, `vertical_beauty_v0.md`) — the card PATTERN to follow.
  - `.agents/hooks/check_ontology_ssot.py`, `check_ontology_expansion.py`, `check_ontology_tag_validity.py`, `check_ontology_drift.py` — the four gates the build must pass. Read their headers for the exact contract.
  - `docs/decisions/ontology_runtime_drift_check_contract_v0.md` — the drift-check contract (runtime_bindings scope).
  - `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` §4 (five panels, esp. panel 1 fit) — WHY this build exists.
  - `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md` — the provenance discipline derived claims must carry (the sub-ontology's facts feed these).
- already loaded (weak orientation, freshness-marked; NOT authority): the sender read the backbone doc + ontology.yaml + expansion backlog at origin/main @ 6a998ddc on 2026-07-04. Re-read; main may have advanced.
- must load first (before any strict/actionable step): the backbone doc + ontology.yaml + the four hook headers. Building without them risks a fork the hooks will reject.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **The ontology is ADOPTED and ENACTED, not just proposed.** Gist: core 15/18 types adopted 2026-06-15; SSOT + cards + backlog + 4 hooks are live on main. Decided in: `orca_ontology_backbone_architecture_v0.md` (status header + §6.1) and `ontology.yaml` (status: ADOPTED). Verify before strict use.
- **"Vertical specificity as data, not schema."** Gist: fragrance categories live in values/reference data; the schema stays vertical-neutral. Decided in: backbone §6 + charter high-lock-in decision #4 (`aphrodite_carveout_charter_v0.md`). Verify before designing any new field.
- **Creator Signal ↔ Capture boundary.** Gist: Creator Signal owns display/claim language; Capture owns registry/capture/computation. Decided in: `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` (owns/does_not_own). Verify before deciding where the sub-ontology and any creator entity live.
- **Fit is the core read; the ontology makes it a structured match.** Gist: place each mentioned product in ontology space (brand/product/tier/note/accord/occasion/dupe-of); creator footprint = attention-weighted distribution over that space; fit = similarity to the buyer's product coordinates + audience-taste match. Decided in: this lane's analysis + charter §4 panel 1. Verify against the charter.

## Active Objective

Build the Aphrodite fragrance sub-ontology as schema-light reference DATA on the adopted backbone (houses as `brand:` cards; fragrances as `product:` data; note-family / accord / tier / occasion vocabulary; a dupe-of relationship graph), registered in the SSOT and carded per the existing pattern, so the Creator Signal fit panel's tier/note components become derived and the fit read becomes a structured match — cold-agent-usable and provenance-backed.

## Exact Next Authorized Action

1. **Obtain explicit owner build-authorization** for this sub-ontology build (this packet grants none) and run the Forseti start-preflight.
2. Route through `workflow-implementation-scoping` against the live substrate (the four ontology hooks + SSOT define the conformance contract; scope how the fragrance data model attaches to `product:`/`brand:` without a new type).
3. Surface the **Open Decision (creator entity)** to the owner before any creator entity is given a stable ontology id; the reference-data build proceeds without it.
4. Validation / stop condition: the build is not done until the Success Signals below pass, including all four ontology hooks green and the cold-retrieval test.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (start-preflight, source hierarchy, artifact folders, validation gates). Load-bearing: yes. Compare target: `origin/main:AGENTS.md`. Reuse rule: overlay wins on Forseti facts.
- Ontology backbone (naming authority): `forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md`. Load-bearing: yes. Compare target: `git show origin/main:<path>` resolves; status header reads ADOPTED. Reuse rule: governs on conflict with the SSOT.
- Ontology SSOT: `forseti/product/spines/foundation/ontology/ontology.yaml`. Load-bearing: yes. Compare target: resolves on origin/main; contains `product:`, `brand:`, `vertical:beauty.fragrance`, `windcaller:` namespaces. Reuse rule: machine SSOT of the adopted backbone.
- Expansion backlog: `forseti/product/spines/foundation/ontology/ontology_expansion_backlog_v0.json`. Load-bearing: yes. Compare target: resolves; `Product` + `WindCaller` in `deferred_no_auto_trigger`. Reuse rule: the mechanism for graduating a deferred type.
- Four ontology hooks: `.agents/hooks/check_ontology_{ssot,expansion,tag_validity,drift}.py`. Load-bearing: yes. Compare target: all four resolve on origin/main. Reuse rule: the build must pass all four.
- Charter (why + panels): `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`. Load-bearing: yes (scopes the fit read). Compare target: resolves on origin/main. Reuse rule: strategy register; owner-ratified direction.
- Provenance contract: `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`. Load-bearing: yes. Compare target: resolves. Reuse rule: the discipline the sub-ontology's facts must support downstream.
- **Seed data (rehearsal-surfaced products)** — on the SENDER BRANCH `claude/priceless-gagarin-19ddd2` (PR #665), NOT yet on main, and on `orca/`-era `docs/research/` paths (docs/ not renamed, so paths hold): `docs/research/aphrodite_depth_rehearsal_ontology_slice_v0.md` (~10 houses / ~10 products, hand-resolved, receipt-backed) and `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md` (GentsScents: designer head clean, clone/niche tail flagged low-confidence). Load-bearing: yes (the v0 seed). Compare target: `git show claude/priceless-gagarin-19ddd2:docs/research/aphrodite_depth_rehearsal_ontology_slice_v0.md` (branch-pinned; resolve from the branch or after PR #665 merges). Reuse rule: seed only — the designer head is reliable; the clone/niche tail (~13% low-confidence ASR) must be re-verified against a real fragrance reference before it enters the ontology as fact.
- Source gaps: no fragrance-reference source is bound (Fragrantica/Parfumo/basenotes are candidate references, not yet an authorized capture — that is its own gated decision). The `Product` type has no prior backing (this build is a candidate first backing).
- Strict-only blockers: owner build-authorization (OPEN); the creator-entity Open Decision (OPEN, for the creator entity only).
- Not-proven boundaries: not validation, readiness, buyer proof; `product_learning`-capped. A green hook run is conformance shape, not fact-correctness.

## Current Task State

- Completed (by the sender lane, as rehearsal): the fit-read design (structured-match framing), a hand-built rehearsal ontology slice (~10 houses/products) and a 417-mention SoV extraction proving the derivation is real; discovery that the ontology substrate is live on main with a SSOT + backlog + 4 hooks; the creator-entity fork identified.
- Partially completed: the seed reference data exists only as rehearsal artifacts (hand/assisted), not as ontology cards/data; not provenance-graded against a real reference.
- Broken or uncertain: how the creator ENTITY attaches (Open Decision); whether a fragrance-reference source will be authorized (source gap).

## Workspace State

- Branch (sender): `claude/priceless-gagarin-19ddd2` @ `32c81dc0` (pre-forseti-migration `orca/` scheme; behind main).
- origin/main: `6a998ddc` (forseti/ scheme; 16 commits ahead of the sender's merge-base `f3f765c5`, incl. PR #666 orca→forseti migration).
- Dirty state before handoff: clean. After writing this file: this handoff file is untracked until committed.
- Target files/artifacts (for the receiver): new fragrance cards/data under `forseti/product/spines/foundation/ontology/` + a SSOT/backlog update — exact shape is the receiver's scoping output.
- Related: PR #665 (sender's rehearsal lane) is on stale `orca/` paths and needs rebase onto forseti main before it lands — separate concern, flagged not fixed here.

## Frozen Decisions

- The ontology backbone (types, ID grammar, links, cap) is ADOPTED and owner-signed. Evidence: backbone status header + ontology.yaml `status: ADOPTED`. Consequence: the sub-ontology attaches to it; it does not redesign it.
- Fragrance specifics are DATA, not schema/type. Evidence: backbone §6 + charter #4. Consequence: no new frozen field list, no new capped type without owner sign.
- #1 conditions: cold-agent usability + provenance (co-#1) + derivation-usefulness. Evidence: this lane's owner exchange (2026-07-04). Consequence: the Success Signals encode all three.

## Mutable Questions

- Creator-entity attachment (the Open Decision) — owner-owned.
- Whether to authorize a fragrance-reference capture (Fragrantica/Parfumo/basenotes) to source facts vs operator-assert-then-verify — resolves the provenance source gap; its own gated decision.
- Exact card granularity: one card per house with products as data, vs per-product cards — receiver scoping decision, constrained by the existing card pattern + tag-validity hook.

## Superseded / Dangerous-To-Reuse Context

- **Any `orca/product/...` path** — superseded by `forseti/product/...` on main (PR #666). Current replacement: the `forseti/` paths in this packet. Using an `orca/` path resolves nothing on main.
- The sender's earlier claim (in the round-2 grade's FIRST draft) that ad-reception needed a watch-packet SCHEMA change — false and already corrected; the description is captured. Not relevant to this ontology build, but do not carry that stale claim.

## Confirm-Don't-Trust Load Checklist

- Re-verify on `origin/main` before acting: (1) the backbone doc + ontology.yaml resolve and read ADOPTED; (2) the four ontology hooks exist; (3) the expansion backlog lists `Product` deferred; (4) the charter + provenance contract resolve on forseti/ paths.
- Re-derive the seed from the branch-pinned rehearsal artifacts (PR #665); treat the clone/niche tail as unverified.
- Load outcomes: `REUSE` only after (1)-(4) verify; `STALE_REREAD_REQUIRED` if main advanced and paths moved; `BLOCKED_MISSING_PACKET`/`BLOCKED_UNVERIFIABLE` if the ontology substrate or charter no longer resolves as described.

## Success Signals (robust, testable — the definition of done)

1. **Cold-retrieval test.** A fresh agent, given only main's standard entry points, resolves an arbitrary in-scope fragrance to its canonical `product:` id with note-family / tier / dupe data AND its provenance, within the source-loading budget (the ratified cold-lane retrievability bar in `source-loading.md`), with zero sender context. Fails if it must guess a path or exceed the budget.
2. **Hook conformance (all four green).** `check_ontology_ssot` (parses; namespaces/links resolve; deferred set == backlog), `check_ontology_expansion` (no owed-card nudge left open), `check_ontology_tag_validity`, `check_ontology_drift` all pass on the addition. A hook red = not done.
3. **Provenance coverage.** Every fragrance fact carries a source ref or an explicit `operator_asserted_pending_source` marker; **zero** bare unsourced facts ship as authoritative. A random spot-check of N facts (note family, tier, dupe-of) against a real fragrance reference passes at an agreed threshold (e.g. ≥90%).
4. **Derivation / resolution rate.** ≥80% of the products the two depth rehearsals surfaced resolve to a sub-ontology `product:` entry (measures seed coverage); the fit panel's tier/note components recompute as *derived* (resolved against the ontology) rather than operator-labeled.
5. **Backbone conformance.** Registered in `ontology.yaml`; mints no new capped type without the Open Decision resolved; property lists stay as data (schema-light); Layer-2 authority not forked; the backbone still governs on conflict.
6. **Cold extensibility.** A fresh agent can add a new house/product/note as DATA following the stated pattern, without editing schema or the backbone, and the four hooks stay green.

## Do Not Forget

- Start from `origin/main` (`forseti/` paths), never the sender branch's `orca/` paths.
- The creator-entity fork is the owner's call and gates only the creator entity, not the reference-data build.
- Provenance is co-#1: an unsourced fragrance fact is a liability, not a nice-to-have.

## Preflight / boundary receipt

```yaml
output_mode: file-write (this planning handoff packet only)
template_kind: handoff
edit_permission: none for the build — this packet grants no source-changing authority; the packet itself was a docs-write to docs/prompts/handoffs/ on branch claude/priceless-gagarin-19ddd2
receiving_lane_first_move: obtain owner build-authorization, then workflow-implementation-scoping against the live ontology substrate
reviews: none bound; downstream scoping + the four ontology hooks are the conformance gates
doctrine_change: none (planning handoff; the sub-ontology build's own direction_change_propagation receipt fires when it lands, since it touches the ADOPTED ontology substrate + expansion backlog)
destinations:
  input_prompt_artifact: docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md
  output_artifact_written: docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md
non_claims: [not build authorization, not validation, not readiness, not fact-correctness, product_learning-capped]
```
```

Get back context from:
docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md

Follow the packet's confirm-don't-trust load contract. If you have repo/filesystem access, open the packet and re-read its named load-bearing sources on `origin/main` (the `forseti/` ontology substrate) before making strict or actionable claims. If you do not have repo/filesystem access, stop and request a pasted source capsule or no-repo handoff.

Continue only the lane named in the packet's Goal Handoff / Active Objective (build the Aphrodite fragrance sub-ontology as reference data on the adopted backbone). Do not perform work excluded by the packet's Drift Guard — no new capped type without owner sign-off, no `orca/` paths, no parallel ontology machinery, no capture/selling — unless explicitly redirected by the current user.
