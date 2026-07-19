# Marc Jacobs Beauty Relaunch Understanding Scan Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: CSB-first scan and capture-route receipt for the Marc Jacobs Beauty relaunch Understanding Acquire & Seal turn.
use_when:
  - Auditing the bounded R0-R5 acquisition walk.
  - Checking source, route, negative, access, and closure accounting before Deliver.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_commission_board_v0.md
  - docs/workflows/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_acquisition_seal_v0.md
stale_if:
  - The acquisition is reopened or a cited current surface materially changes.
```

## Scan Intake Receipt

```yaml
scan_receipt_version: 1
commission_id: marc_jacobs_beauty_relaunch_understanding_csb_20260719
scan_date: 2026-07-19
mode: forward
subject: Marc Jacobs Beauty
market_or_geography: US retail translation; global owned relaunch context
source_context_status: SOURCE_CONTEXT_READY
run_caps:
  max_screening_moves_total: 12
  max_exact_queries_total: 20
screening_moves_used: 9
exact_queries_used: 16
hidden_venue_pointers: 3
capture_requests: 0
closeout_state: no_candidate_after_discovery
```

## Broad Scout Return

The broad scout covered the current owned, retail, review, Reddit-native, and
independent-editorial frontiers required by the commission. Exact queries
`EQ-001` through `EQ-016` first resolved the named routes, then checked
contradictions, negatives, access notes, current-state recency, and hidden
venues. Venue evaluation kept company-syndicated launch language separate from
independent hands-on observation.

Three hidden venue pointers survived the bounded scout: a multi-tester Allure
review, a disclosed product-sample review in The Looker/Daily Beast, and a
self-purchased long-wear review at LiftBakeLove. The recommended main deepening
was the already-commissioned selected-PDP and selected-thread preservation; it
was completed. TikTok did not receive a unique non-dominated information job,
and Quora remained unnecessary. No further deepening had expected decision
value above its time and access cost after R4.

## CSB Board Intake

Board source:
`docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_commission_board_v0.md`.

Rows consumed as route map: `SBR-001` through `SBR-009`, mapped one-to-one to
board rows `COV-001` through `COV-009`.

## Exact Query Discovery Ledger

| Query ID | Query text or exact route | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQ-001 | Coty Marc Jacobs Beauty relaunch 2026 | Resolve the official launch frame. | positive | Preserve the Coty origin. |
| EQ-002 | site:marcjacobs.com Marc Jacobs Beauty face eyes lips | Resolve current owned assortment. | positive | Read current category and product surfaces. |
| EQ-003 | site:marcjacobs.com "Joystick Blush" | Resolve the owned blush PDP and claims. | positive_partial | Preserve indexed official content; record direct-page access denial. |
| EQ-004 | site:marcjacobs.com "Born Star" "Heart On" "Drawn This Way" | Resolve current eye and lip claims. | positive | Carry official product URLs and current claims. |
| EQ-005 | site:sephora.com/brand "Marc Jacobs Beauty" | Resolve Sephora's current brand translation. | positive | Use the canonical Sephora route. |
| EQ-006 | Sephora Joystick Buildable Cream Blush Stick | Resolve the exact PDP. | positive | Preserve canonical PDP and review substrate. |
| EQ-007 | Sephora Born Star Cream-to-Powder Long-Wear Eyeshadow | Resolve the exact PDP. | positive | Preserve canonical PDP and review substrate. |
| EQ-008 | Sephora Heart On Long-Lasting Soft Shine Lipstick | Resolve the exact PDP. | positive | Preserve canonical PDP and review substrate. |
| EQ-009 | old Reddit r/Sephora search: Marc Jacobs Beauty, new | Current retailer-community scout. | positive | Select only non-dominated experience threads. |
| EQ-010 | old Reddit r/MakeupAddiction search: Marc Jacobs Beauty, new | Current makeup-community scout. | positive | Select distinct comparison and removal threads. |
| EQ-011 | old Reddit r/BeautyGuruChatter search: Marc Jacobs Beauty, new | Creator-watch scout. | zero_current_yield | Do not deepen; current relevant rows were absent. |
| EQ-012 | old Reddit r/beauty search: Marc Jacobs Beauty, new | Broad beauty-community miss check. | low_yield | No selected thread added. |
| EQ-013 | Marc Jacobs Beauty relaunch 2026 review eyeliner blush highlighter | Find independent corroboration and conflicts. | positive | Evaluate independent hands-on reviews. |
| EQ-014 | Marc Jacobs Beauty 2026 relaunch hands-on review | Hidden-venue and negative discovery. | positive | Retain distinct independent origins. |
| EQ-015 | site:allure.com Marc Jacobs Beauty 2026 relaunch review | Resolve a multi-tester editorial origin. | positive | Carry shade- and tester-specific counterevidence. |
| EQ-016 | site:wwd.com Marc Jacobs Beauty relaunch 2026 | Check trade coverage and syndication. | no_unique_hands_on_yield | Do not substitute launch coverage for independent wear evidence. |

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | COV-001 | Coty exact announcement | venue_value | Direct HTTP preserved the official relaunch origin, proposition, seven-product assortment, pricing, and launch channels. | R0 complete. |
| M02 | COV-002 | Marc Jacobs current category and product pages | candidate_support | Current owned URLs established assortment, shade breadth, packaging language, textures, and performance claims; the exact Joystick page denied both direct HTTP and browser packet capture. | R1 sufficient with a typed access residual. |
| M03 | COV-003 | Sephora brand page and three selected PDPs | candidate_support | Canonical US-market CloakBrowser captures admitted USD offers for Joystick, Born Star, and Heart On. Delivery location remained unpinned. | Retail translation sufficient. |
| M04 | COV-004 | Dated Sephora review rows | contradiction | Current rows preserved incentive markers and both favorable and unfavorable product experience. | Review substrate sufficient; no prevalence inference. |
| M05 | COV-005 | Four bounded old-Reddit search surfaces | venue_value | Canonical screening reads returned current candidates from Sephora and MakeupAddiction; the other two surfaces added no non-dominated current thread. | Mandatory scout complete. |
| M06 | COV-005 | Seven exact selected old-Reddit threads | contradiction | Content-mode packets preserved attributable posts and comments spanning mascara, blush, eyeshadow, highlighter, eyeliner, packaging, and value comparisons. | Selected-thread preservation complete. |
| M07 | COV-008 | Allure, The Looker/Daily Beast, LiftBakeLove | contradiction | Independent hands-on sources corroborated several textures and performance claims while exposing shade-, tester-, and product-specific conflicts. | Independent-origin requirement complete. |
| M08 | COV-009 | Broad hidden-venue, better-origin, syndication, and negative scout | negative | Better origins were retained; repeated launch-copy coverage was not counted as independent product-performance corroboration. | Hidden-venue and syndication check complete. |
| M09 | COV-006, COV-007, COV-009 | Closure/value test | access_note | Quora was dominated and TikTok had no unique job. Remaining uncertainty is typed and additional retrieval was not expected to change the decision-neutral evidence shape. | R5 closure fired. |

## Hidden Venue Pointers

```yaml
hidden_venue_pointer_id: HVP-001
venue: Allure
url: https://www.allure.com/story/marc-jacobs-beauty-relaunch-2026-review
why_non_dominated: Multiple named testers supplied product- and shade-specific wear observations, including counterevidence within the same product family.
```

```yaml
hidden_venue_pointer_id: HVP-002
venue: The Looker / Daily Beast
url: https://thelooker.thedailybeast.com/marc-jacobs-beauty-relaunched-review/
why_non_dominated: The author disclosed pre-launch samples and supplied a distinct mascara, blush, bronzer, and eyeshadow wear test.
```

```yaml
hidden_venue_pointer_id: HVP-003
venue: LiftBakeLove
url: https://liftbakelove.com/2026/06/12/i-bought-too-much-from-the-marc-jacobs-beauty-relaunch-so-you-dont-have-to/
why_non_dominated: The author disclosed self-purchase and longer real-life use, adding product-specific wear, taste, storage, and shade-representation evidence.
```

## Observations

```yaml
observation_id: OBS-001
source_move_id: M01
url: https://www.coty.com/news/coty-launches-marc-jacobs-beauty-one-of-the-most-requested-luxury-comebacks
retrieval_date: 2026-07-19
short_quote_or_summary: Coty framed the relaunch around Joyride Sensoriality, bold self-expression, seven opening products, 26-to-42-dollar pricing, tactile packaging, and staged Marc Jacobs, Sephora, and Selfridges distribution.
signal_stage: venue_value
claim_it_might_support: official current relaunch proposition, assortment, price, partnership, and named channel plan
gate_role: none
independence_hypothesis: official first-party origin; syndicated restatements are not independent
uncertainty_or_limits: Cannot establish product performance, customer experience, prevalence, or local availability.
```

```yaml
observation_id: OBS-002
source_move_id: M02
url: https://www.marcjacobs.com/us-en/the-marc-jacobs/beauty-fragrance/view-all/
retrieval_date: 2026-07-19
short_quote_or_summary: Current owned surfaces showed the seven-product assortment and product-specific packaging, texture, shade, and long-wear claims; indexed official PDP content remained readable although one exact-page packet route returned Akamai denial.
signal_stage: candidate_support
claim_it_might_support: current owned expression of assortment and product claims
gate_role: none
independence_hypothesis: official first-party product surfaces
uncertainty_or_limits: Exact Joystick PDP packet capture is partial; indexed official content is screen-light and not an independent performance test.
```

```yaml
observation_id: OBS-003
source_move_id: M03
url: https://www.sephora.com/brand/marc-jacobs-beauty
retrieval_date: 2026-07-19
short_quote_or_summary: Sephora translated the relaunch as maximalist, playful, upgraded, multi-use, and long-wearing; selected PDPs carried 29-to-35-dollar USD offers and current product claims.
signal_stage: candidate_support
claim_it_might_support: retailer translation of the proposition and selected assortment
gate_role: none
independence_hypothesis: retailer surface; product copy may be brand-supplied
uncertainty_or_limits: US/USD was source-confirmed, but delivery location and local stock were not pinned.
```

```yaml
observation_id: OBS-004
source_move_id: M04
url: https://www.sephora.com/product/heart-on-long-lasting-soft-shine-lipstick-P524918?country_switch=us&skuId=2994481
retrieval_date: 2026-07-19
short_quote_or_summary: Dated Heart On rows praised smooth, moisturizing, buildable wear but also reported shade-photo mismatches, a loose cap, returns, and one 2-to-3-hour wear result; incentive disclosures were preserved row by row.
signal_stage: contradiction
claim_it_might_support: early external experience and conflict with absolute all-day or non-fading language
gate_role: none
independence_hypothesis: customer review substrate; reviewer independence varies and incentive markers matter
uncertainty_or_limits: Attributable rows are not representative prevalence and cannot establish population-level satisfaction.
```

```yaml
observation_id: OBS-005
source_move_id: M04
url: https://www.sephora.com/product/born-star-cream-to-powder-long-wear-eyeshadow-P524930?country_switch=us&skuId=2994705
retrieval_date: 2026-07-19
short_quote_or_summary: Dated Born Star rows included smooth, easy, crease-resistant experiences alongside breakage or shrinkage in the pan, creasing, low pigment, warm-shade mismatch, and bulky-price concerns.
signal_stage: contradiction
claim_it_might_support: early shade-, packaging-, and wear-specific counterevidence
gate_role: none
independence_hypothesis: customer review substrate with preserved incentive markers
uncertainty_or_limits: The rows establish attributable examples, not defect rate or prevalence.
```

```yaml
observation_id: OBS-006
source_move_id: M06
url: https://old.reddit.com/r/Sephora/comments/1txln4q/marc_jacobs_review/
retrieval_date: 2026-07-19
short_quote_or_summary: A first-hand review found creamy eyeshadow and blendable blush, then updated that blush lasted only a couple of hours while eyeshadow lasted all night; comments repeatedly split on cute design versus light, cheap, bulky, or flimsy hand-feel.
signal_stage: contradiction
claim_it_might_support: early product texture, wear, and packaging experience
gate_role: none
independence_hypothesis: attributable community source; external customer evidence only
uncertainty_or_limits: Self-selected discussion is not representative demand, quality rate, or internal company fact.
```

```yaml
observation_id: OBS-007
source_move_id: M06
url: https://old.reddit.com/r/Sephora/comments/1u35l10/the_marc_jacobs_liner_kinda_sucks/
retrieval_date: 2026-07-19
short_quote_or_summary: >
  Eyeliner experience was strongly shade-dependent: some black and brown
  shades were smooth and extremely durable, while Delulu and bright blue
  reports described softness, breakage, patchiness, weak payoff, smudging, or
  short waterline wear.
signal_stage: contradiction
claim_it_might_support: bounded counterevidence to a uniform 24-hour waterproof performance reading
gate_role: none
independence_hypothesis: attributable community source with counterexamples in the same thread set
uncertainty_or_limits: Shade, application, skin, and technique differences prevent a line-wide causal or prevalence conclusion.
```

```yaml
observation_id: OBS-008
source_move_id: M06
url: https://old.reddit.com/r/Sephora/comments/1tx2d4i/marc_jacobs_money_shot_highlighter_issue/
retrieval_date: 2026-07-19
short_quote_or_summary: Multiple attributable users described Money Shot arriving dried or shrunken, tiny, patchy, or goopy and reported replacements or returns; related comments also carried liner breakage and shade mismatch.
signal_stage: negative
claim_it_might_support: early material quality-control and value concerns
gate_role: none
independence_hypothesis: attributable community source; repeated reports remain nonrepresentative
uncertainty_or_limits: Material negative evidence, not a severe safety signal and not a defect-rate estimate.
```

```yaml
observation_id: OBS-009
source_move_id: M07
url: https://www.allure.com/story/marc-jacobs-beauty-relaunch-2026-review
retrieval_date: 2026-07-19
short_quote_or_summary: Allure testers corroborated creamy liner, blendability, and durable wear, but another tester found one Born Star shade messy with weak payoff and migration after five hours; Heart On did not survive eating, drinking, or kissing.
signal_stage: contradiction
claim_it_might_support: independent product- and tester-specific corroboration and counterevidence
gate_role: none
independence_hypothesis: independent editorial origin with brand-supplied imagery or products disclosed in context
uncertainty_or_limits: Small named tester set; findings remain shade-, method-, and person-specific.
```

## Negatives And Access Notes

- `NEG-001`: the local derived lake lookup for “Marc Jacobs Beauty” returned
  `not_found`; this is not proof of zero prior data or catalog exhaustion.
- `ACCESS-001`: exact owned Joystick capture returned HTTP 403 and then a
  preserved `akamai_access_denied` browser artifact. Current indexed official
  product content remained partial screen-light evidence.
- `ACCESS-002`: the in-app browser backend was unavailable; no unrelated browser
  route was silently substituted.
- `ACCESS-003`: Sephora capture succeeded only after replacing a locally
  hard-coded Laneige fixture profile with the same registry-authorized
  Sephora/US CloakBrowser route and target-specific sufficiency checks.
- `ACCESS-004`: the first Reddit content batch summary reported zero secondary
  consolidations because it searched for raw HTML after content-mode discard.
  All seven manifests and `raw/01_content_record.json` files fresh-read as
  present; this is a summary residual, not source loss.
- `NEG-002`: no severe safety or harm evidence was found. Attributable quality,
  packaging, shade-representation, taste, and wear complaints were preserved as
  material negatives without converting them into prevalence.
- `GAP-001`: exact owned PDP packet preservation is partial.
- `GAP-002`: delivery location and local store availability remain unpinned.
- `GAP-003`: early customer and community evidence is nonrepresentative.
- `GAP-004`: a Reddit user's same-formula/manufacturer inference from ingredient
  lists remains unverified and is not adopted as company fact.

## Capture Triage

No downstream capture request remains. R0, the selected R2 PDPs, and seven
selected R3 threads were preserved during this Acquire & Seal turn under their
route-owned contracts. Scanning does not commit packets, bind new routes, or
perform ECR, Cleaning, or Judgment work.

## Candidate Decision

```yaml
candidate_decision:
  closeout_state: no_candidate_after_discovery
  independent_origins_seen:
    - official_first_party
    - retailer
    - customer_community
    - independent_editorial
  reason: >
    The commissioned company-understanding evidence foundation is necessary
    complete with typed residuals. This scan did not commission or produce a
    company-surface candidate for another lane.
```

## Closeout

`no_candidate_after_discovery`.

R5 closure fired after required R0-R4 jobs completed and the remaining gaps were
typed. The next authorized act is the separately commissioned Deliver turn,
not more acquisition by default.
