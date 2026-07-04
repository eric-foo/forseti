# Aphrodite Depth Rehearsal — Honest Grade + Build Shopping List v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (rehearsal grade + gap sizing — evidence lane; advisory input to charter D-1, owner-routed)
scope: >
  The honest grading of the single-creator depth rehearsal (jeremyfragrance,
  IG) against the charter Section 4 decision-grade panel definitions, and the
  shortfall shopping list that sizes the real depth-layer build. This is the
  handoff's success-signal artifact: the ways the rehearsal falls short ARE
  the deliverable. Advisory only; the foundation exit gate (D-1) remains an
  owner decision.
use_when:
  - Sizing the depth-layer build from rehearsal evidence.
  - Preparing the owner decision on charter D-1 (foundation exit gate).
  - Deciding the next bounded depth-layer slice.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_fit_panel_v0.md
  - docs/research/aphrodite_depth_rehearsal_ad_reception_panel_v0.md
  - orca/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
stale_if:
  - A later rehearsal or the real depth-layer build supersedes this grading.
  - The charter's panel definitions (Section 4) are amended.
```

## What the rehearsal proved (worked end-to-end)

1. **The pipeline shape is real.** Registry → attributed capture → entity
   slice → recipe → provenance-stamped derived claims → panel rendering ran
   end-to-end on committed lake data with no new capture.
2. **The provenance contract is satisfiable in practice.** All 19 claims carry
   the seven required fields; 24/24 record hashes verified against packet set
   records; 18/18 receipt quotes + 6/6 caption receipts re-grepped verbatim in
   source records; corpus-level hashes are re-derivable from the corpus doc
   alone. The contract's cost is real but small at this scale.
3. **Withhold-not-zero-fill works as a product behavior.** 2 of 5 fit
   components withheld and the ad-reception core downgraded — the panels stay
   readable and honest instead of fabricating coverage.
4. **The attribution chain held under adversarial checking.** A delegated
   survey wrongly reported the IG content "orphaned"; the bronze-catalog facet
   rows + raw manifests + in-content self-identification settled it. The chain
   (derived record → catalog row → raw manifest sha256 → session identity) is
   the right spine for `source_refs`.
5. **The cheap layer earns its keep.** Grid metadata (captions, platform
   paid-partnership flags, engagement counts) powered most of the sponsorship
   detection at zero extra capture cost — as the charter's stratified policy
   predicted.

## Panel grades (against charter Section 4 decision-grade definitions)

**Fit panel: D+ (not decision-grade).** Segment share: real but one-week-thin.
Price-tier distribution: real but concentrated in 2 reels; note-family
distribution unpopulatable; price tiers had to be operator-assigned because no
ontology with tier/note data exists. Audience taste: the strongest read (the
persona-vs-product finding is genuinely decision-relevant for a brand
considering this creator) but n=64 with severe page-1 skew. Adjacency and
trajectory: withheld outright.

**Ad-reception panel: C- (not decision-grade, but structurally further along).**
Detection worked on every reel and the load read (self-brand density, informal
gifting disclosure, zero labeled partnerships) is decision-relevant as-is. The
core sponsored-vs-organic comparison is impossible on this corpus — zero
third-party sponsored items — which is a *capture-substrate* shortfall, not an
extraction shortfall.

## Shopping list (sized by observed failure, ordered by what unblocked first)

1. **YouTube long-form transcripts at roster scale** — the single biggest gap.
   The runner capability landed (PR #640) but zero YouTube transcript lanes
   exist in the lake; 12/30 registry channels have only thin caption rawfiles
   (~5.9K words total) feeding the old mentions lane, 18/30 have nothing.
   Reels ASR (593 usable words across 9 reels here) cannot carry fit-panel
   product discourse; long-form is where it lives.
2. **Sponsored-content capture stratum (charter Section 6d)** — pull-on-decision
   capture of sponsored videos + matched organic pairs. Without it the
   ad-reception panel's core comparison is structurally impossible for any
   creator. Detection-first triage (platform labels + caption markers, both
   already captured) can build the sponsored-item worklist cheaply.
3. **Ontology with tier/note reference data** — the hand slice resolved 10
   houses/10 products from one creator-week, but price tiers and note families
   required operator market knowledge; canonical reference data (sourcing and
   licensing posture: owner decision) is what makes the fit panel's
   distributions derivable instead of asserted.
4. **ASR-aware entity resolution** — observed manglings ("Jim Fraganz",
   "Savage", "Jean Procté", "Parfumse de male", 2 unresolvable niche entities)
   mean exact-match resolution will silently drop the tail; the extractor
   needs fuzzy/phonetic matching against the ontology plus an explicit
   unresolved queue (rehearsed here in the ontology slice's abstention table).
5. **Comment depth beyond page 1** — the 15-of-215 case shows page-1-only can
   surface ~7% of a hot reel's comments; fine for texture, hostile to
   intent-mining. Keep page-1 as the default stratum; add pull-on-decision
   deep comment capture for sprint creators (same shape as stratum d).
6. **Time axis** — adjacency, trajectory, and momentum all withheld on a
   single cycle. No new build needed: the existing grid cadence just has to
   keep running; every additional cycle unlocks these claim types.
7. **Empty-comment rendering** — 21/85 captured comments have empty text
   (unrendered stickers/GIFs?); a capture-lane fix or an explicit
   `unrenderable` posture would remove a silent texture undercount.
8. **Recipe → runner formalization** — the hand-run recipe
   (`aphrodite-rehearsal-extraction-v0`) plus the per-claim verification
   script pattern (hash recompute + verbatim receipt grep) is the spec seed
   for the real extractor; the mentions lane (`codex-extraction-v0`) already
   models the runner shape but lacks the panel claim types and full 7-field
   provenance.

## D-1 advisory (owner-routed, not decided here)

The rehearsal corroborates the charter's recorded recommendation: a
practice-run gate discriminates better than numeric capture targets. This
rehearsal — the depth-layer "practice dinner" — produced a concrete,
evidence-backed build list that numeric thresholds would not have surfaced
(e.g., the sponsored-stratum gap and the ASR-resolution tail). Suggested gate
shape for D-1: "a single-creator panel set reaches decision-grade on fit +
ad-reception using roster-scale substrate," with items 1–3 above as the
predicted blockers to clear. Owner decision; nothing here fires the gate.

## Non-claims

- Not validation, readiness, buyer proof, or willingness-to-pay evidence;
  `product_learning`-capped.
- Grades are the authoring model's honest self-assessment and the natural
  target for a delegated adversarial review (recommended at closeout).
- Does not authorize any shopping-list item; each is its own gated lane
  (capture strata and runners are capture-lane; ontology sourcing and D-1 are
  owner decisions; FLAG 1 commercial-use/data-rights remains open).
