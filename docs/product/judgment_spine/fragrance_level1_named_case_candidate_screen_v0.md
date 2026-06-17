# Fragrance Level 1 Named-Case Candidate Screen v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine product artifact (fragrance Level 1 named-case candidate screen)
scope: >
  Screens the first named fragrance Level 1 case candidates against Orca's
  case-selection doctrine without admitting cases, authorizing source capture,
  authorizing runs, or creating proof.
use_when:
  - Choosing which fragrance Level 1 named case to try admitting first.
  - Checking why a fragrance candidate is priority, held, or rejected before source capture.
  - Preventing public fragrance examples from being mistaken for admitted casebook rows.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md
  - docs/product/core_spine/beauty_venue_card_set_v0.md
stale_if:
  - A later artifact admits, rejects, or supersedes any named fragrance case.
  - The fragrance casebook admission frame changes its named-case admission fields, slot allocation, or selection rules.
  - The case-finder doctrine, memorization-resistant finder frame, or discovery authorization boundary changes.
  - A source/evidence plan authorizes packet-grade fragrance capture.
```

## Status

This is a docs-only candidate screen.

It does not admit a case. It narrows the first search output to candidates worth
trying to admit later under the fragrance casebook admission gate.

```yaml
screen_status: bounded_candidate_screen
casebook_shape_status: admitted_slot_frame_by_pointer
named_case_status: none_admitted_by_this_artifact
default_case_status: candidate_pending_selection_or_held
claim_cap: product-learning context only
closeout_state: unreceipted_product_learning_context
source_capture_authority: none
run_authority: none
```

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 judgment/fragrance/case-selection screen
  edit_permission: docs-write
  target_scope: create a docs-only fragrance named-case candidate screen and map pointers; no case admission, source capture, prompt, run, scoring, or proof
  dirty_state_checked: yes
  blocked_if_missing: case-selection doctrine, fragrance casebook admission frame, delegated search receipts, and clean worktree state
```

## Selection Doctrine Applied

This screen uses the stricter case-selection rule, not popularity.

- Select for learnability, not brand prestige.
- Prefer a reconstructable decision with a clean cutoff, visible tradeoff,
  revealed action or outcome, and enough source depth to expose judgment misses.
- Avoid famous/headline cases for product-learning tier unless they are
  intentionally used as benchmarks or negative controls.
- Do not choose a case because the known evidence looks favorable, the outcome
  flatters Orca, or the story is convenient for marketing.
- Discovery may identify names, rough timelines, public inspectability,
  possible cutoffs, and eligibility blockers. It must not interpret signal
  strength, buyer behavior, backtest judgment, or proof.
- For fragrance Level 1, a named case still needs cutoff, post-cutoff exclusion
  rule, allowed source families, outcome-label plan, measurement window, and a
  benchmark policy that could plausibly disagree.
- The first named case should be a disagreement case, not an obvious winner.

## Search Method

Fanout ran in read-only mode across four lanes:

- doctrine scout: located the controlling case-selection doctrine;
- creator/campaign lane: screened one-origin creator and campaign-heavy cases;
- retail/review lane: screened independent fragrance, retail, review, and
  discovery-format candidates;
- crossover/repositioning lane: screened body mist, format crossover,
  discounting, and repositioning candidates.

Main-lane reconciliation added a small web spot-check for the strongest named
candidates and checked existing Orca fragrance-adjacent case assets. This is
not source capture. Source URLs below are candidate pointers only, not evidence
units, source inventories, or admissible packets.

## Recommended First Admission Attempt

Try Boy Smells 2.0 first if the next step is one named fragrance case admission.

Reason: it is the cleanest disagreement case found in this pass. A
community/brand-equity benchmark can plausibly say the rebrand damaged the
thing that made the brand valuable; a retailer-growth benchmark can plausibly
say the Sephora reset worked. That is a better first learning case than an
obvious winner like PHLUR Missing Person.

## Priority Candidates

### 1. Boy Smells 2.0 / Sephora rebrand

```yaml
case_id: boy_smells_2_0_rebrand_sephora_2025
slot_status: candidate_pending_selection
candidate_priority: 1
tentative_bucket:
  - retail strong / creator-community weak
  - repositioning case where demand exists but offer language is wrong
possible_cutoff_datetime_utc: 2025-04-11T06:59:00Z
cutoff_basis: >
  Tentative pre-rebrand cutoff: before the public April 11, 2025 rebrand.
  Needs archive pin before admission.
benchmark_policy_that_may_disagree:
  - community/brand-equity benchmark: preserve original queer-coded identity and legacy scent language
  - retailer-growth benchmark: accept mainstream Gen Z Sephora reset if new customers and sell-through appear
outcome_label_plan_candidates:
  - complaint_cluster_grows_60d
  - review_velocity_sustains_60d
  - retail_expansion_or_sku_followthrough_180d
```

Why it fits: high disagreement, clean before/after event, visible consumer
complaint surface, retailer outcome surface, and a decision object narrow enough
to test product language and channel reset.

Source pointers to inspect later:

- `https://www.them.us/story/boy-smells-fragrance-line-interview`
- `https://www.allure.com/story/boy-smells-personal-fragrances`
- `https://www.thecut.com/article/boy-smells-rebrand-perfume-review.html`
- `https://nymag.com/strategist/article/new-boy-smells-candle-review.html`

Blockers before admission:

- Need archived pre-rebrand PDPs, brand language, and SKU list.
- Need Sephora/PDP review and availability capture; brand-stated sales cannot be
  the only outcome leg.
- Keep identity discussion product-language and positioning focused. Do not turn
  the case into a cultural-position adjudication.

### 2. DedCool Mochi Milk / Milk franchise extension

```yaml
case_id: dedcool_mochi_milk_franchise_extension_2025
slot_status: candidate_pending_selection
candidate_priority: 2
tentative_bucket:
  - independent creator cluster + review velocity + restock
  - scent-family launch with community disagreement
possible_cutoff_datetime_utc: 2025-03-01T08:00:00Z
cutoff_basis: >
  Tentative pre-Mochi Milk launch cutoff. Needs archive pin and exact launch
  chronology before admission.
benchmark_policy_that_may_disagree:
  - skin-scent/layering benchmark: keep Milk as understated layering platform
  - gourmand-trend benchmark: make the Milk franchise louder and more trend-aligned
outcome_label_plan_candidates:
  - restock_or_sellout_repeats_60d
  - creator_momentum_persists_30d
  - retail_expansion_or_sku_followthrough_180d
```

Why it fits: the case tests whether a brand should stay in an understated
skin-scent lane or amplify a milk/gourmand franchise. It also has a plausible
pre/post public trail through product pages, Sephora surfaces, creator coverage,
and later franchise follow-through.

Source pointers to inspect later:

- `https://www.glossy.co/beauty/milk-remains-hot-in-fragrance-dedcool-aims-to-own-the-trend/`
- `https://www.instyle.com/dedcool-milk-layering-perfume-review-8413714`
- `https://www.byrdie.com/dedcool-mineral-milk-launch-11924733`

Blockers before admission:

- Key sell-through metrics are brand-reported through trade press.
- Need independent retailer review velocity, stock/restock, and creator/community
  confirmation around the correct SKU.
- Need exact cutoff and post-cutoff exclusion rule.

### 3. Snif Crumb Couture / Secret Menu to Ulta

```yaml
case_id: snif_crumb_couture_secret_menu_to_ulta_2025
slot_status: candidate_pending_selection
candidate_priority: 3
tentative_bucket:
  - discovery/trial format + review velocity/restock
  - retail expansion with discounting warning
possible_cutoff_datetime_utc: 2025-06-01T07:00:00Z
cutoff_basis: >
  Tentative pre-summer all-door/omnichannel move for a Secret Menu scent. Needs
  primary Ulta/Retail Dive or equivalent receipt before admission.
benchmark_policy_that_may_disagree:
  - DTC-scarcity benchmark: keep weird limited scents scarce and online-led
  - retail-productivity benchmark: scale a proven odd scent through Ulta
outcome_label_plan_candidates:
  - retail_expansion_or_sku_followthrough_180d
  - review_velocity_sustains_60d
  - discounting_or_overstock_appears_90d
```

Why it fits: it tests whether playful limited-menu fragrance can become a
repeatable retail SKU, while TikTok Shop/flash-deal behavior gives a downside
quality question.

Source pointers to inspect later:

- `https://www.beautyindependent.com/snif-talks-new-subbrand-notewrks-fragrances-toys-category-future/`
- `https://www.the-sun.com/money/11221911/ulta-beauty-major-fragrance-change-snif/`
- `https://www.ulta.com/brand/snif`

Blockers before admission:

- Main operating details come from founder/trade interview coverage.
- Need primary Ulta/PDP review count and SKU availability capture.
- Need exact date for the Crumb Couture Ulta transition.

## Candidate But Held

### Fine'ry Target fragrance line

```yaml
case_id: finery_target_fragrance_line_2023
slot_status: held
tentative_bucket:
  - retail strong / creator weak
possible_cutoff_datetime_utc: unknown
hold_reason: decision owner and cutoff are not yet clean enough
```

Useful for testing retail-led demand without a founder/creator center. Hold
until the decision owner, launch date, Target review/availability trail, and
Amazon expansion timeline can be pinned from primary or archiveable sources.

Candidate source pointers:

- `https://www.glamour.com/story/target-finery-perfume-dupes`
- `https://www.businessinsider.com/le-labo-santal-33-perfume-target-finery-dupe-2024-11`
- `https://www.realsimple.com/finery-perfume-candles-amazon-launch-january-2026-11884001`

### Touchland Power Essence Mist

```yaml
case_id: touchland_power_essence_mist_2025
slot_status: held
tentative_bucket:
  - body mist / hair-body mist / bodycare crossover
possible_cutoff_datetime_utc: 2025-02-03T07:59:00Z
hold_reason: outcome is not isolated to the mist decision
```

Useful for testing whether sanitizer scent equity can transfer into fragrance.
Hold because post-cutoff brand outcomes may be sanitizer-led rather than
mist-led.

Candidate source pointers:

- `https://www.allure.com/story/touchland-power-essence-mist-review`
- `https://www.allure.com/review/touchland-power-mist-moisturizing-hand-sanitizer`

### NOYZ Mylk de Parfum

```yaml
case_id: noyz_mylk_de_parfum_2026
slot_status: held
tentative_bucket:
  - body mist / hair-body mist / bodycare crossover
  - discovery set / travel-size / mini format
possible_cutoff_datetime_utc: 2026-02-06T07:59:00Z
hold_reason: format innovation is visible, but outcome trail is still mostly editorial and recent
```

Useful for testing fragrance-as-skincare format innovation. Hold until retailer
review velocity, repeat availability, or follow-through exists beyond launch
coverage.

Candidate source pointers:

- `https://www.glamour.com/story/noyz-mylk-de-parfum-review`
- `https://www.vogue.com/article/best-perfume-launches-2026`

## Existing Orca Assets: Do Not Remint As New Cases

These already exist in Orca discovery or harness context. They may later be
admitted through the fragrance gate if the owner wants, but this search should
not pretend they are newly discovered.

| Case | Current handling |
| --- | --- |
| `imaginaryauthors_sku_kills_2024_v0` | Existing product-learning case directory and capture-side provenance notes. Strong subtle fragrance case; not a new slot from this search. |
| Puredistance M / V2Q | Existing beauty subtle-decision screen output. Strong but non-US; use as benchmark or later owner-routed case. |
| Xerjoff Irisss | Existing subtle-class candidate under corroborated material-change A-leg. Strong but non-US and A-leg complex. |
| `nueco_fragrance_pivot_v0` | Existing product-learning case directory. Useful fragrance-adjacent pivot case, but not a pure fragrance Level 1 first-slot search result. |

## Not Recommended For First Admission

| Candidate | Why held or rejected for first named case |
| --- | --- |
| PHLUR Missing Person / Chriselle Lim relaunch | Strong source trail, but too prominent and too close to an obvious winner. Better as benchmark or later recognition-gated case. |
| Sol de Janeiro body mists | Too scaled and too consensus for the first learnability case. Better as category benchmark. |
| Addison Rae AF Collection | Potential one-origin creator case, but current DTC availability and weak clean outcome make it a lower-priority negative-control candidate. |
| Charli D'Amelio Born Dreamer | Creator fame and Ulta launch confound are high; not cleanly "no retail confirmation." |
| Beyonce Ce Noir | Fame/campaign confound is too severe for the operative product-learning finder frame. |
| Boring Company Burnt Hair | Paid preorder behavior is interesting, but novelty/non-beauty and memorization risk make it poor for fragrance Level 1. |

## Next Move

For the next docs-only step, do not broaden the casebook yet. Pick one of:

1. Admit-attempt packet for `boy_smells_2_0_rebrand_sephora_2025` with full
   admission-minimum fields, still no capture authority.
2. Source/evidence plan for fragrance Level 1 that binds candidate source
   families by pointer and routes packet-grade capture to source-capture owners.
3. A separate benchmark/negative-control note for PHLUR, Sol de Janeiro, and
   celebrity creator cases so they do not contaminate the first admissions.

## Source-Read Ledger

Local doctrine and map sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/research/judgment-spine/README.md`
- `docs/research/judgment-spine/manifest_v0.md`
- `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md`
- `docs/product/core_spine/core_spine_v0_proof_case_selection_brief_v0.md`
- `docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md`
- `docs/product/judgment_spine/fragrance_level1_casebook_admission_frame_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
- `docs/product/core_spine/beauty_venue_card_set_v0.md`
- `docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md`
- `docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md`
- `orca-harness/cases/product_learning/imaginaryauthors_sku_kills_2024_v0/source_provenance_notes_v0.md`
- `orca-harness/cases/product_learning/nueco_fragrance_pivot_v0/source_provenance_notes_v0.md`

Delegated search receipts:

- `019ed5c5-9ab2-7ac2-b946-0aca212db3ff` doctrine scout.
- `019ed5c5-e5bc-72c2-9bba-506cfea20719` creator/campaign screen.
- `019ed5c6-0f7d-7be3-af41-1ec9444d999a` retail/review screen.
- `019ed5c6-36b2-79b1-8e5a-4c0c4da8dd75` crossover/repositioning screen.

Public source pointers were used only for screening. No source capture,
archive packet, source map, source inventory, scraper, monitor, run, score, or
proof was created.

## Non-Claims

Not validation, readiness, buyer proof, product proof, judgment-quality
evidence, source-capture authority, prompt approval, run authorization, scoring
authorization, fixture admission, accepted benchmark, completed
product-learning evidence, owner adoption, or proof that any fragrance case
works.
