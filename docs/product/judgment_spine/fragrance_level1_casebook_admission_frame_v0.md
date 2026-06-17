# Fragrance Level 1 Casebook Admission Frame v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine product artifact (fragrance Level 1 casebook admission frame)
scope: >
  Admits the first 25-slot fragrance Level 1 product-learning casebook shape,
  selection rules, slot allocation, and outcome-label families without admitting
  named cases, authorizing source capture, authorizing runs, or creating proof.
use_when:
  - Filling the first real fragrance Level 1 case slots.
  - Checking whether a proposed fragrance case has enough cutoff, source, and outcome structure to become admitted.
  - Preventing the 25-case backtest plan from being mistaken for run authorization, fixture admission, scoring, or proof.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md
  - docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md
  - docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md
  - docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/product/core_spine/beauty_venue_card_set_v0.md
stale_if:
  - The current-state/decomposition map changes its default mode, SCV loop, 25-case success condition, outcome labels, source registry, commission gate, forecast/action/log/evaluation contract, or live/client readiness gates.
  - The fragrance satellite skeleton changes its casebook, source, forecast, reveal, or receipt slots.
  - The evidence ladder changes product-learning receipt minima, claim caps, or closeout states.
  - The beauty venue card set changes fragrance venue hints or review status.
  - An owner accepts, rejects, or materially changes the 25-slot allocation below.
  - A later artifact admits named fragrance cases into these slots.
```

## Status

This is a docs-only casebook admission frame.

It admits the **casebook shape**: 25 slots, bucket allocation, minimum admission
fields, and outcome-label families. It does **not** admit any named product,
brand, SKU, launch, discontinuation, or retail decision as a case yet.
Completing 25 public fragrance backtests through the Level 1 loop is the
first success condition for product learning, not a readiness, calibration, or
buyer-proof screen.

Current case state:

```yaml
casebook_id: fragrance_level1_casebook_v0
decision_family: fragrance_level1
casebook_shape_status: admitted_slot_frame
named_case_status: none_admitted
case_status_default: candidate_pending_selection
default_mode: backtest
claim_cap: product-learning context only
closeout_state: unreceipted_product_learning_context
```

## Operating Rule

This artifact is the casebook organizer below the fragrance satellite skeleton.
It consumes the current backtesting-first route: the default
named-case mode is `backtest`, with a frozen evidence cutoff and exclusion of
all post-cutoff information before reveal.

Future work may fill slots only by adding a separate named-case admission
artifact, row, or receipt that records the required fields below. A slot ID in
this artifact is not enough to treat a case as admitted.

## Admission Gate For A Named Case

A proposed named case may move from `candidate_pending_selection` to `admitted`
only when a later artifact records all of these fields:

```yaml
fragrance_case_admission_minimum:
  slot_id:
  case_id:
  brand_or_product:
  decision_family: fragrance_level1
  case_bucket:
  canonical_case_type:
  mode: backtest
  cutoff_datetime_utc:
  evidence_cutoff_at:
  post_cutoff_exclusion_rule:
  future_information_policy: exclude_all_information_after_cutoff
  commission_gate_brief_ref:
  source_registry_or_governance_ref:
  allowed_pre_cutoff_source_families:
  prohibited_or_held_sources:
  outcome_label_plan:
  forecast_targets:
  measurement_window:
  exclusion_criteria:
  benchmark_policy_that_may_disagree:
  non_claims:
    - not run authorization
    - not scoring authorization
    - not source-capture authority
    - not fixture admission
    - not buyer proof
    - not judgment-quality evidence
    - not live_internal readiness
    - not client_facing readiness
```

If any field is unknown, keep the named case at `candidate_pending_selection`
or `held`, not `admitted`.

## Slot Allocation

These slots come from the user-supplied fragrance working pack and are reconciled
through the current Judgment product-learning cap. Exact case names remain open.

| Slot IDs | Bucket | Count | Why included | Default status |
| --- | --- | ---: | --- | --- |
| FL1-001 to FL1-004 | One-origin creator spike, no retail confirmation | 4 | Tests overhype detection | candidate_pending_selection |
| FL1-005 to FL1-008 | Independent creator cluster + review velocity + restock | 4 | Tests real-demand detection | candidate_pending_selection |
| FL1-009 to FL1-012 | Creator strong / retail weak | 4 | Tests bounded-test discipline | candidate_pending_selection |
| FL1-013 to FL1-015 | Retail strong / creator weak | 3 | Tests under-the-radar opportunity detection | candidate_pending_selection |
| FL1-016 to FL1-018 | Discovery set / travel-size / mini format | 3 | Tests wedge-specific format decisions | candidate_pending_selection |
| FL1-019 to FL1-021 | Body mist / hair-body mist / bodycare crossover | 3 | Tests adjacent expansion and discount risk | candidate_pending_selection |
| FL1-022 to FL1-023 | Campaign-heavy launch, weak costly behavior | 2 | Tests campaign-dependence discounting | candidate_pending_selection |
| FL1-024 to FL1-025 | Discounting / overstock warning case | 2 | Tests downside avoidance | candidate_pending_selection |

## First Canonical Case Types

Use these as slot-filling prompts, not as admitted cases:

1. One-origin creator spike with no retail confirmation.
2. Independent creator cluster plus review velocity plus restock.
3. Strong retail reviews with weak creator attention.
4. Paid campaign cluster with weak costly behavior.
5. Body mist expansion with shopper-account lift and discount risk.
6. Scent-family launch with community disagreement.
7. Discovery set / travel-size demand without full-size confidence.
8. Retail expansion case with complaints and discounting.
9. Repositioning case where demand exists but offer language is wrong.
10. Search/AEO spike without purchase-proxy confirmation.

The first named case should be a disagreement case, not an obvious winner.

## Selection Rules

Each named case needs:

- a clear cutoff date/time;
- a publicly visible source trail before cutoff;
- a publicly visible outcome window after cutoff;
- at least one benchmark policy that could plausibly disagree with Orca;
- source families that are public, reviewable, dateable, and resolvable to the
  correct SKU, format, or decision object when SKU/format matters.

Avoid obvious consensus cases at the start. Use `unclear` instead of forcing an
outcome label when public evidence is too thin.

## Outcome-Label Families

These labels are candidate outcome families for named-case admission. A later
case artifact should bind only the labels relevant to that case.

| Outcome label family | Default window | Admission note |
| --- | --- | --- |
| `review_velocity_sustained_60d` | 60 days | New relevant reviews exceed the working threshold and are not obvious launch-dump, duplicate, old-SKU, or wrong-SKU reviews. |
| `creator_momentum_persisted_30d` | 30 days | Post-cutoff mentions continue with non-duplicated creators or cross-segment spread. |
| `creator_decay_after_launch_30d` | 30 days | Days 31-60 show material decay from days 0-30 with no new non-creator confirmation. |
| `community_confirmation_30d` | 30 days | At least three independent community/review items include usage or purchase-proxy language. |
| `restock_or_sellout_repeats_60d` | 60 days | At least one public restock, sellout, or out-of-stock event is tied to the correct SKU or format. |
| `discounting_or_overstock_appears_90d` | 90 days | Target SKU/product receives a 20%+ SKU-specific discount or repeated SKU-specific promotion not explained by ordinary sitewide sale. |
| `complaint_cluster_grows_60d` | 60 days | At least three independent post-cutoff complaints share the same issue across more than one source family or review cluster. |
| `retail_expansion_or_sku_followthrough_180d` | 180 days | A new retailer, format, SKU, restock expansion, discovery set, travel size, or adjacent product follow-through appears. |
| `search_interest_persisted_60d` | 60 days | Autocomplete, trend tool, search result ranking, marketplace search, or AEO visibility persists across at least two checks. |

These labels are evaluation inputs only. They do not create calibration, scoring,
buyer-proof, or judgment-quality claims.

Older shorthand labels using `sustains` or `persists` are migration aliases only;
new records should use the canonical `sustained` / `persisted` names above.

## Source-Family Boundary

Source-family hints should start from the beauty venue card set for fragrance
and from any later source/evidence plan that explicitly adopts source families.

At this frame stage:

- Basenotes, Fragrantica, specialist fragrance blogs, retailer reviews, trade
  press, brand pages, marketplace surfaces, creator surfaces, search/AEO, and
  community forums are candidate source families only.
- A venue hint is not source-capture authority.
- Direct access notes are dated hints, not current-state proof.
- Any source used for a named case must preserve provenance enough to enforce
  the cutoff rule.
- Creator evidence is early radar, not proof. A creator-led case needs
  non-creator confirmation before any stronger action posture is recorded.

## Casebook Fill Template

Use this row shape when a later artifact proposes a named case:

```yaml
casebook_slot:
  slot_id:
  slot_bucket:
  slot_status: candidate_pending_selection | admitted | held | excluded
  case_id:
  brand_or_product:
  canonical_case_type:
  mode: backtest
  cutoff_datetime_utc:
  evidence_cutoff_at:
  post_cutoff_exclusion_rule:
  future_information_policy: exclude_all_information_after_cutoff
  commission_gate_brief_ref:
  source_registry_or_governance_ref:
  allowed_pre_cutoff_source_families: []
  prohibited_or_held_sources: []
  outcome_label_plan: []
  forecast_targets: []
  measurement_window:
  benchmark_policy_that_may_disagree:
  admission_artifact_ref:
  exclusion_reason_if_any:
  non_claims:
    - not run authorization
    - not scoring authorization
    - not source-capture authority
    - not fixture admission
    - not buyer proof
    - not judgment-quality evidence
    - not live_internal readiness
    - not client_facing readiness
```

## Next Docs-Only Moves

1. Create or point to the Level 1 source registry, outcome-label, commission
   gate, forecast-record, decision-log, benchmark, and evaluation artifacts
   before treating any slot as run-ready.
2. Use the named-case candidate screen to choose the first admission attempt,
   then fill that candidate into an admission-minimum artifact or row while
   keeping incomplete cases at `candidate_pending_selection`.
3. Author the fragrance source/evidence plan that binds source-family governance
   by pointer and does not claim source-capture authority.
4. After at least one named case and source/evidence plan are bounded, author a
   per-case product-learning receipt template.

## Non-Claims

This artifact is not validation, readiness, buyer proof, product proof,
judgment-quality evidence, source-capture authority, prompt approval, run
authorization, scoring authorization, fixture admission, accepted benchmark,
completed product-learning evidence, `live_internal` readiness,
`client_facing` readiness, owner adoption of any named fragrance case, wholesale
temp-pack adoption, or proof that the fragrance plan works.

It admits the casebook organizer only. Named cases still require later
admission records before any backtest, prompt, evidence capture, or receipt can
claim to be case-specific.

## Source-Read Ledger

Repo and overlay sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/source-loading.md`

Judgment and fragrance sources:

- `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
- `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md`
- `docs/product/judgment_spine/fragrance_level1_named_case_candidate_screen_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md`
- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`
- `docs/product/core_spine/beauty_venue_card_set_v0.md`

User-supplied temp-pack sources:

- `C:/Users/vmon7/AppData/Local/Temp/orca_open_questions_working_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_build_action_doc.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_mgt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_mgt_goal_v1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_commission_gate_prompt.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_judgement_prompt_level1.md`
- `C:/Users/vmon7/AppData/Local/Temp/orca_docs_split_manifest.md`
