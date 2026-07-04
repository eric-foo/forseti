# Aphrodite Depth Rehearsal — D-1 GentsScents Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (cross-vendor adversarial artifact review result for the D-1 GentsScents rehearsal; findings-first, advisory; not D-1 passage)
scope: >
  The commissioned cross-vendor adversarial review of the GentsScents D-1
  rehearsal artifact set, run per
  docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md.
  Reports findings against the five target artifacts and the control sources
  named in that input, and states the criterion-5 review verdict.
use_when:
  - Adjudicating this review before marking D-1 criterion 5 observed.
  - Checking what a cross-vendor pass found in the GentsScents rehearsal.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_grade_v0.md
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
stale_if:
  - Any target artifact is patched after this review.
  - The review-lane or delegated-review-patch overlay changes the cross-vendor/decorrelation bar.
```

## Review provenance and lane binding

- `reviewed_by`: `claude-sonnet-5` (Anthropic).
- `authored_by`: `gpt-5-codex` (OpenAI), per the `extraction_model` field carried on every claim in `aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json` and the review-input's stated "Author/home family: OpenAI/GPT/Codex."
- `de_correlation_bar`: `cross_vendor_discovery` — the author vendor (OpenAI) and the delegate vendor (Anthropic) differ, satisfying the cross-vendor discovery bar in `.agents/workflow-overlay/review-lanes.md`.
- **Lane actually run: `workflow-adversarial-artifact-review`** (source-read-only, per `.agents/workflow-overlay/review-lanes.md` "Current Lanes"), invoked directly per the review-input's paste-ready prompt, with `workflow-deep-thinking` invoked first per the same prompt and per `.agents/workflow-overlay/review-lanes.md` Rules. This is **not** a `workflow-delegated-review-patch` run: no single named target file or bounded multi-file set was commissioned, no patch authority was granted, and no diff is returned. See finding AR-05 for a residual ambiguity about which convention the charter's criterion-5 language actually intends.
- Output mode: `filesystem-output`, `required_output_path` = `docs/review-outputs/adversarial-artifact-reviews/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_artifact_review_v0.md`, per the review-input's "Output path" section. This is a durable review report, not chat-only.
- Review target and purpose are commission-bound to the five target artifacts named in the review-input, read against the eight named control sources plus two additional control-adjacent sources read because a missing read could change a finding: `aphrodite_derived_claim_provenance_contract_v0.md` (the seven required derivation-provenance fields) and `aphrodite_vetting_sprint_panel_design_v0.md` (the ratified per-row display design the panel projection must match). Neither addition retargets the review; both are read-only sources used to judge the five named targets.

## Source-read ledger

| Source | Role | Freshness / state |
| --- | --- | --- |
| `docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md` | Commission | Read from `codex/aphrodite-d1-depth-rehearsal`, clean working tree |
| `.agents/workflow-overlay/review-lanes.md` | Review-lane authority | Clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Adjacent-lane authority | Clean |
| `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md` | Build authorization / D-1 work-unit definition | Clean |
| `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` | Fitness reference (D-1 gate 3 definition) | Clean |
| `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md` | Recipe-v1 binding rulings M1–M4 | Clean |
| `docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md` | Prior-round substrate grading | Clean |
| `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md` | SoV methodology + numbers reused by the claim record | Clean |
| `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml` | Resolution target | Clean |
| `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md` | Provenance-field authority (not in commission's read list; read because it is decisive for AR-01 and finding 5 of the adversarial questions) | Clean |
| `forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md` | Ratified display design (not in commission's read list; read because it is decisive for AR-02/AR-03) | Clean |
| `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md` | Target 1 | Clean |
| `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md` | Target 2 | Clean |
| `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json` | Target 3 (all 30 claim objects read in full) | Clean |
| `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_panel_projection_v0.md` | Target 4 | Clean |
| `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_grade_v0.md` | Target 5 | Clean |

All sources were read from the `codex/aphrodite-d1-depth-rehearsal` branch checkout, working tree clean, no dirty or unanchored source relied on for any finding below.

## Findings (severity-ordered)

### AR-01 — MAJOR — confidence: high

- **Files**: `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json` (all `fit.*` claims), `docs/research/aphrodite_depth_rehearsal_round2_share_of_voice_v0.md`.
- **Problem**: Every `fit.*` claim's `receipt` field cites an aggregate summary row in `aphrodite_depth_rehearsal_round2_share_of_voice_v0.md` (e.g. "Official SoV aggregate: Creed Aventus 5 videos, 183,116 attention views, 1.2%"), not a verbatim per-mention transcript receipt (`video_id`, `start_ms`/`end_ms`, quote). The round-2 SoV document itself states its extraction produced "417 raw product mentions... each with brand, product, verbatim receipt, stance, resolution confidence," but only ever publishes the aggregate top-8 table — the per-mention verbatim receipts were never committed to the repository. The result: for the fit panel specifically, there is no artifact anywhere in this repo that lets a reader drill back from a displayed number (e.g. Aventus's 183,116 attention views) to an actual transcript quote and timestamp.
- **Strongest defense and why it fails**: One could argue the "receipt" field only needs to name *what the claim rests on*, and citing a specific, dated, already-reviewed research document satisfies that. This holds for corpus-level or count-level claims (e.g. `fit.video_segment_share`), but it fails for the panel that D-1 criterion 2 and criterion 3 hinge on hardest: `aphrodite_derived_claim_provenance_contract_v0.md` defines `receipt` as "the supporting quote(s) / timestamp(s) / comment link(s) the claim rests on... the buyer can 'verify this claim' at the source, same as per-number drill-back," and the adjudicated YouTube "Receipt rule" (`aphrodite_recipe_v1_second_opinion_adjudication_v0.md`) requires transcript receipts to be "verbatim, mechanically greppable, and include `video_id`, `start_ms`, `end_ms`, and the quote." Citing an aggregate table one level removed from the transcript does not meet that bar, and no verbatim receipt for any fit-panel mention is recoverable from any committed artifact.
- **Why it matters**: This directly weakens D-1 criterion 3 ("provenance behavior end-to-end") specifically for the fit panel — the panel criterion 2 depends on most. The purchase-intent panel, by contrast, *does* carry genuine verbatim per-comment receipts (e.g. `eH93HPAWucE` comment 9), showing the recipe is capable of this granularity when the underlying data supports it; the fit panel's shortfall is a real gap, not a structural limit of the recipe.
- **Minimum closure condition**: Either (a) the underlying per-mention verbatim receipts from the round-2 SoV extraction pass are located and published (even as an appendix), and fit-panel claims cite them directly, or (b) the fit-panel claims are explicitly downgraded (not shown at their current posture) with a named limitation stating the drill-back terminates at an aggregate table, not a transcript quote.
- **Next authorized action**: Home-lane decision on which closure path to take; this review does not patch.

### AR-02 — MAJOR — confidence: high

- **File/anchor**: `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`, claim `fit.note_family_overlap.v0`; cross-checked against `forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md` §2.
- **Problem**: The ratified panel design requires note-family overlap to render as **individual chips per buyer note family**, each explicitly one of three states: `observed with receipts` / `observed only via adjacent products` / `withheld — not observed in captured corpus`. The buyer's originals carry note families `[fresh, spicy, amber, citrus, aromatic, musk, woody]` (Sauvage) and `[fruity, sweet, woody, leather, citrus]` (Aventus) — 10 distinct families across the two anchors. The claim renders only a flat `observed_overlap: [citrus, woody, fresh, spicy, aromatic]` array. The families `amber`, `musk`, `fruity`, `sweet`, and `leather` are not mentioned anywhere in the claim — they are silently omitted rather than rendered as explicit `withheld — not observed` chips.
- **Strongest defense and why it fails**: The claim is already postured `downgrade`, which signals the row is not fully reliable, and one could argue the omission is implicitly covered by that downgrade. This does not hold: the recipe's own Abstention Rules state "Missing evidence emits a claim with `value: null`, `provenance_state: withhold`... It is never zero-filled and never dropped" — a `downgrade` posture on the claim as a whole does not substitute for per-family withhold states the ratified design explicitly requires as separate chips. A buyer reading this row cannot tell whether "amber" was checked and absent, or never checked at all.
- **Why it matters**: This is exactly the "missing ≠ zero, never a silent drop" drift guard named in the build handoff, applied at sub-claim granularity. For a skeptical dupe-first buyer whose whole evaluation rests on note-family fit, a silently dropped family reads as "no evidence to the contrary" rather than the honest "not observed."
- **Minimum closure condition**: Re-render `fit.note_family_overlap` with one explicit chip state per buyer target note family (all 10, not only the 5 that overlap), per the ratified §2 design.
- **Next authorized action**: Home-lane decision; not patched by this review.

### AR-03 — MAJOR — confidence: medium-high

- **File/anchor**: `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`, claim `fit.tier_alignment.v0` (`provenance_state: show`); cross-checked against `aphrodite_vetting_sprint_panel_design_v0.md` §2.
- **Problem**: The ratified design specifies this row as "Creator's **attention-weighted and editorial coverage distribution** across the ontology tier vocabulary [designer, niche, luxury, creator-owned-dtc, clone-house, adjacent], displayed separately from note overlap." The rehearsal's claim instead compares only the two buyer-anchor products' individual tiers (`niche`, `designer`) plus a qualitative sentence ("mainly designer with a niche Aventus anchor"). No attention-weighted or editorial percentage distribution across the six-tier vocabulary is computed or shown, and the claim is postured `show` (the highest-confidence posture) rather than being marked as a narrower substitute.
- **Strongest defense and why it fails**: M1 of the accepted adjudication rules that tier facts under the adopted rubric render `show, not downgrade` — this correctly licenses showing the two anchor products' tiers at high confidence. It does not license substituting a 2-product comparison for the ratified design's full-vocabulary distribution without naming the narrower scope; M1 governs the *provenance posture* of a tier fact, not the *completeness* of the row against its own design spec.
- **Why it matters**: This is also where the recipe-v1 second-opinion's M4(b) fractional-view-allocation ruling would apply ("fractional allocation for tier/note distributions... disclosed on-panel") — but because no distribution is actually computed, that disclosure obligation never gets a chance to be violated or honored; the deeper problem is the distribution itself is missing. A reader could reasonably believe the `show`-postured "tier alignment" row is the full ratified distribution when it is a much narrower comparison.
- **Minimum closure condition**: Either render the full attention-weighted/editorial tier distribution (with fractional-allocation disclosure per M4(b) if that method is used), or relabel the row's scope explicitly (e.g. "anchor-tier comparison only, not the full-vocabulary distribution") and consider downgrading the posture to match the narrower scope actually delivered.
- **Next authorized action**: Home-lane decision; not patched by this review.

### AR-04 — MAJOR — confidence: medium

- **Files**: `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json` (`buyer_profile` object), `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md` ("Creator and Buyer Inputs"); cross-checked against `aphrodite_recipe_v1_second_opinion_adjudication_v0.md` "Candidate-Set Intake."
- **Problem**: The recipe-v1 second-opinion adjudication's Verdicts table explicitly **accepted as proposed** a structured candidate-set intake schema (`buyer_segment`, `buyer_house_tier`, `dupe_target_originals` as a list of resolved product objects, `note_family_targets`, `occasion_targets`, `target_tier_position`, and — called out by name as "a genuine improvement" — `intake_source_state` per coordinate, to make the provenance of each buyer coordinate mechanically visible). The D-1 rehearsal's actual `buyer_profile` is a flat object with only `profile_type`, `locked_by`, and a four-line prose `coordinates` array. None of the structured fields, and none of the `intake_source_state` provenance, appear anywhere in the five target artifacts.
- **Strongest defense and why it fails**: The recipe's own "Bindings for recipe v1" section (5 numbered items) does not explicitly list the intake schema as a mandatory binding — only the claim-type table, hashing rules, the two required-output claim types, the gate-6 run log, and rulings M1–M4. This is a real distinction and softens the finding from a binding violation to a fidelity gap. It does not fully defend the gap: the adjudication's Status line states everything in the appendix (which includes the intake schema and its accepted verdict) is adjudicated-accepted material "except as ruled above" — the intake schema was not ruled against, it was accepted outright — and the whole point of `intake_source_state` was to make D-1 criterion 4's "actually exercised, not stubbed" claim mechanically checkable. A flat prose list cannot be mechanically scanned the way the accepted schema was designed to be.
- **Why it matters**: The grade doc marks criterion 4 `OBSERVED_FOR_SYNTHETIC_BUYER` without naming this simplification as a residual anywhere. A reader adjudicating the grade has no way to know the fuller, adjudicated-accepted intake design was not used.
- **Minimum closure condition**: Either populate the accepted intake schema (with `intake_source_state` per coordinate) for this buyer profile, or add an explicit residual to the grade doc naming the simplification and why it was accepted for this rehearsal.
- **Next authorized action**: Home-lane decision; not patched by this review.

### AR-05 — MINOR — confidence: medium

- **Files**: `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md` §7 gate 3 criterion 5 ("...per the delegated-review lane"), `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md` Work Unit step 7 ("commission per `.agents/workflow-overlay/delegated-review-patch.md`"), vs. `docs/review-inputs/aphrodite_depth_rehearsal_d1_gentsscents_adversarial_review_input_v0.md` (which invokes only `workflow-adversarial-artifact-review`, explicitly disclaims patch authority, and names no single bounded target file or file set).
- **Problem**: The charter and handoff both point criterion 5 at "the delegated-review lane" / a `delegated-review-patch.md` commission, but the review-input that actually dispatched this pass runs the plain, source-read-only `workflow-adversarial-artifact-review` lane instead. `delegated-review-patch.md`'s default mode requires a single named target artifact with a bounded patch scope (or, in its sibling mode, a named multi-file code-diff set); neither fits a five-heterogeneous-file evidence-artifact review with no patch authority.
- **Strongest defense (this one holds, but the ambiguity is still worth naming)**: `.agents/workflow-overlay/review-lanes.md` binds its own cross-vendor "two-bar de-correlation" rule directly inside the plain adversarial-artifact-review lane, independent of `delegated-review-patch.md`; and `delegated-review-patch.md` itself gates its use "by commission, not by category," which this review-input never invoked. On the weight of the evidence, the plain lane is a defensible, self-consistent vehicle for satisfying "cross-vendor adversarial review... blocker/major-free."
- **Why it matters**: Because the interpretation is defensible rather than settled by explicit reconciliation anywhere in the artifact set, a future reader (or a stricter adjudicator) could read the charter's literal words and conclude the wrong convention was used, or conversely assume protections (bounded patch scope, protected-path list, model ladder, the delegated-review-output finalization gate) applied when they did not.
- **Minimum closure condition**: The home lane names, once, which convention governs D-1 criterion 5 satisfaction and why, closing the ambiguity for future rehearsals.
- **Next authorized action**: Home-lane note; no patch needed for this review's own conduct, since it was correctly invoked per the review-input's explicit instruction.

### AR-06 — MINOR — confidence: low-medium (compact)

`docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md` records the buyer-coordinate Open Decision as `"locked_by": "owner choice during fused run"` (also in the claims JSON), but the handoff's other Open Decision — which creator anchors the rehearsal — has no equivalent recorded owner confirmation anywhere in the five artifacts; GentsScents matches the handoff's own recommendation, so this is very likely benign, but the asymmetric documentation is a traceability gap against a handoff that named both items as owner-routed decisions.

### AR-07 — NOTE — confidence: low (compact)

`fit.tier_alignment.v0`'s `reference_coords` cite only the two buyer-anchor products' tier fields, not the ~8 top-attention products its own `creator_attention_tiers` prose summarizes ("mainly designer with a niche Aventus anchor"); independently verifiable via `fit.product_segment_presence`'s `reference_coords` and the ontology file itself, so this is a completeness nit, not a defect that blocks verification.

## Considered and defended

- **CD-1**: The 29-vs-30 claim-count discrepancy between the adjudication's prose ("29 claim types") and its own appendix table (30 rows, including `fit.unresolved_product_mentions`) is a candidate inconsistency finding. Defended: the discrepancy originates in a control source (the adjudication record), not in a target artifact, and the claim record discloses it visibly (`claim_count_audit`) rather than silently resolving or hiding it.
- **CD-2**: A candidate finding that fit-panel attention numbers use non-fractional ("reach-style") view weighting inconsistent with ruling M4(b)'s fractional-allocation requirement. Defended: M4(b)'s fractional-allocation rule applies specifically to tier/note **distributions**, and per AR-03 no such distribution is actually rendered in this rehearsal — the per-product `attention_views` figures shown are reach-style numbers under the adjudication's separate, undisputed "product reach" rule, which carries no fractional-disclosure obligation.

## Answers to the adversarial questions (summary)

1. **Fake D-1 passage / readiness / validation / buyer proof / FLAG-1 / commercial clearance?** No. All five artifacts carry explicit non-claims sections, and the grade doc states plainly "any claim that D-1 fired is false" pending criterion 5.
2. **All five panels represented, no hidden score?** Yes — five panels, per-row show/downgrade/withhold states throughout, no composite number found anywhere.
3. **Fit product-coordinate claims resolve against the ontology or explicitly withhold/downgrade?** Mostly yes at the claim-object level, but see AR-02/AR-03 for granularity gaps within otherwise-compliant claims.
4. **Dupe-space honest withhold while showing direct-original attention?** Yes — `fit.dupe_direct_original_attention` shows, `fit.dupe_clone_tail_attention` withholds with the exact required text, consistently in both the claim record and the panel projection.
5. **All required provenance fields on every claim?** Yes — all 30 claims carry the seven fields required by `aphrodite_derived_claim_provenance_contract_v0.md` plus `provenance_state`; see AR-01 for a drill-back depth gap that survives despite the fields being formally present.
6. **M2 preserved (no blended `liked_support` scalar)?** Yes — `intent.engagement_weighted_support` keeps raw counts and `sum(like_count)` separate per bucket, with `blended_scalar: null` explicit.
7. **Synthetic buyer profile stays an intake coordinate, not market proof?** Yes in framing; see AR-04 for a fidelity gap in how that intake is structured.
8. **Limitations (count mismatch, low-confidence tail, affiliate-heavy corpus, no organic comparator, single-cycle momentum) visible?** Yes, consistently and honestly disclosed throughout.
9. **Criterion table / grade too generous anywhere?** Criterion 2's residual note and criterion 4's evidence line are both thinner than warranted given AR-01 through AR-04; criteria 1, 3, 5, 6 read as accurately calibrated.
10. **Review input / grade explicit that same-family review cannot satisfy criterion 5?** Yes, unambiguously, in multiple places.

## Criterion 5 review verdict

```yaml
criterion_5_review_verdict: NOT_BLOCKER_MAJOR_FREE
can_home_lane_consider_criterion_5_observed_after_adjudication: "no — not until AR-01 through AR-04 are adjudicated (closed, downgraded-with-named-limitation, or explicitly accepted as residuals by the home lane)"
blocker_count: 0
major_count: 4
minor_count: 2
note_count: 1
```

## Residual risks (remain even if AR-01–AR-04 are closed)

- Single capture cycle; momentum intentionally thin — by design, not a defect, but still a real limit on what any buyer can conclude before a second cycle.
- Affiliate-heavy corpus with no clean organic comparator for ad-reception — already disclosed, structural to this creator's monetization style, not fixable inside this rehearsal.
- ~13% low-confidence ASR clone/niche tail excluded from rollups — already disclosed and named (panel design residual R4); correct direction (undercounts, does not fabricate) but still caps clone-tail completeness.
- Empty ontology dupe graph — already disclosed and named (panel design residual R1); clone-house demand remains unproven until citable `dupe_of` edges exist.
- Everything here is `product_learning`-capped; none of it is buyer proof, willingness-to-pay evidence, or commercial-use clearance.

## Test / validation suggestions

- Recover or re-derive the per-mention verbatim receipts behind the round-2 SoV extraction and cite them directly from fit-panel claims (closes AR-01), or explicitly downgrade and name the gap.
- Re-render `fit.note_family_overlap` as one explicit chip per buyer target note family, including withheld chips for every non-overlapping family (closes AR-02).
- Either compute the full attention-weighted/editorial tier distribution with fractional-allocation disclosure, or relabel `fit.tier_alignment`'s scope and reconsider its posture (closes AR-03).
- Populate the accepted candidate-set intake schema with `intake_source_state`, or add a named residual to the grade doc (closes AR-04).
- Have the home lane record, once, which convention (plain adversarial-artifact-review vs. delegated-review-patch) governs D-1 criterion 5, to remove the ambiguity in AR-05 for future rehearsals.

## Review-use boundary

These findings are decision input for the Chief Architect / owner adjudicating this rehearsal against D-1 criterion 5. They are not approval, validation, mandatory remediation, or executor-ready patch authority. No file outside this report was edited or patched by this review. Closing any of AR-01 through AR-07 is the home lane's authorized next action, not this review's.

## Non-claims

- Not validation, readiness, buyer proof, willingness-to-pay evidence, or D-1 passage.
- Not a `workflow-delegated-review-patch` run; no diff, no patch, no bounded-executor commission was exercised.
- Not a resolution of FLAG-1 or any commercial-use/data-rights question.
- Does not itself decide whether D-1 criterion 5 is observed — that is the home lane's adjudication, per the review-use boundary above.
