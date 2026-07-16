# Creator Ideal Audience Calibration Examples v0

```yaml
retrieval_header_version: 1
artifact_role: Product calibration appendix (named creator examples)
scope: >
  Preserves owner-accepted named examples that calibrate commercial force and
  specificity. It is a reviewer/calibration aid, not part of routine Judgment
  context and never evidence for another creator.
use_when:
  - Human-reviewing commercial force after a creator Judgment is compiled.
  - Running an explicit leave-one-example-out calibration exercise.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md
  - forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
stale_if:
  - The controlling method or accepted example language changes.
```

## Status And Authority

`OWNER_ACCEPTED_CALIBRATION_APPENDIX_V0` — optional examples companion. Routine
Judgment prompts must not load this file. A named example is contaminated for a
cold test unless a leave-one-example-out source is recorded.
## Calibration Patterns, Not Creator Buckets

The four patterns below show the required specificity and commercial force.
They are deliberately different. Derive another role when the evidence demands
one; never force a creator into these patterns or paste their wording.

The named first-screen examples below are owner-accepted phrasing calibrations
from creator-isolated dogfood. This deck does not make them live creator claims
or replace their evidence bindings, counterevidence, and capture limitations.

Each pattern's hiring calibration shows the panel's product-meaning headline
(what the creator makes the product mean) in context. The panel's first line is
still the controlling contract's hire verdict — `Hire <creator> when <campaign
job>` — assembled from the pattern's **Campaign jobs**. Calibrate force and
specificity from these lines; take the panel grammar from the controlling
contract.

### 1. Make The Product Earn Its Recommendation

- **Evidence pattern:** the creator repeatedly tests, compares, challenges, or
  withholds easy approval; participants ask for verdicts, trade-offs, or
  reassurance.
- **Buyer tension:** category claims are cheap and the buyer fears paying for a
  recommendation that feels bought.
- **Commercial role:** reduce decision risk by making endorsement feel earned.
- **Product meaning:** a recommendation that survived scrutiny.
- **Mechanism:** visible standards, proof, comparison, and a verdict the audience
  can use as purchase reassurance.
- **Accepted first-screen calibration:** “Hire Noel when your fragrance range
  must win the buyer's last three objections: Is it real? Is it worth it? Will
  it work for me? He buys suspicious bottles, exposes failures beside the real
  thing, and wears alternatives past the paper test—until the safest choice
  feels like the obvious next bottle.”
- **Campaign jobs:** proof-led launches, comparisons, reformulations, premium
  justification, or products that win under examination.
- **Wrong hire:** a tightly controlled script that cannot tolerate scrutiny or a
  product that needs unqualified praise.
- **Overclaim trap:** purchase reassurance is not attributed conversion unless
  the evidence explicitly shows the creator caused the purchase.

### 2. Make The Product Impossible To Ignore

- **Evidence pattern:** a distinctive recurring presentation ritual or spectacle
  becomes the thing participants quote, joke about, request, or recognize.
- **Buyer tension:** competent category content blends together and the product
  needs attention, recall, and a recognizable moment.
- **Commercial role:** turn the product into the signature object inside a
  repeatable entertainment format.
- **Product meaning:** the bottle, launch, or reveal people remember and talk
  about after the post.
- **Mechanism:** creator-owned visual or verbal theatre that attracts
  participation and makes the product central to the ritual.
- **Accepted first-screen calibration:** “Hire Cologne Crown when your
  high-projection masculine scent must become impossible to ignore and easy to
  recall. He makes the atomizer the spectacle, gives the scent a blunt occasion
  and Beast Mode verdict, then gets commenters demanding the next bottle at 50,
  100—even 1,000 sprays.”
- **Campaign jobs:** reveals, visually distinctive packaging, hero-product
  launches, memorable demonstrations, and spectacle-led awareness.
- **Wrong hire:** utility-only copy, invisible packaging, or briefs that remove
  the creator's recognizable theatre.
- **Overclaim trap:** observable attention and memorability do not automatically
  prove shopping intent.

### 3. Make The Product Win The Value Argument

- **Evidence pattern:** the creator and participants repeatedly compare price,
  alternatives, clones, performance, authenticity, or whether the premium is
  justified.
- **Buyer tension:** the product is entering a skeptical market where value must
  survive side-by-side argument rather than broad aspiration.
- **Commercial role:** make the product the defensible answer in a live category
  debate.
- **Product meaning:** the option whose trade-offs can be explained and defended.
- **Mechanism:** rankings, comparisons, category fluency, and comment-level
  challenge turn value into the content rather than a closing claim.
- **Good hiring line:** “FB makes the product win the value argument.”
- **Campaign jobs:** value challengers, credible alternatives, dupe/clone
  positioning, ranked comparisons, and premium-versus-performance briefs.
- **Wrong hire:** prestige campaigns that forbid comparison or products whose
  economics collapse under direct scrutiny.
- **Overclaim trap:** value debate does not prove the cheapest option wins or
  that the whole audience shares one price posture.

### 4. Make The Product Get Used, Not Saved

- **Evidence pattern:** the creator repeatedly demonstrates a distinctive use
  style, while captured participants report trying, extending, or copying it.
- **Buyer tension:** a product may be admired yet remain too precious, passive,
  or forgettable to become part of how people actually use the category.
- **Commercial role:** make generous, visible use the product's most desirable
  role instead of careful preservation.
- **Product meaning:** the bottle people reach for and spray through, not save.
- **Mechanism:** a named, creator-specific application format makes product use
  visible and gives participants something concrete to try or adapt.
- **Accepted first-screen calibration:** “Hire Funmi when your fruit-forward
  fragrance is built to be worn generously—and needs to become the bottle
  people spray through, not save. Her rule of 20 carries it head to ankle—and
  viewers try it, push it further, and copy it.”
- **Campaign jobs:** fruit-forward or other truthfully aligned launches whose
  formulation, size, price posture, instructions, and brand voice support
  generous application.
- **Wrong hire:** scarce, precious, safety-sensitive, or high-cost-to-deplete
  products; briefs that remove the creator's recognizable use style.
- **Overclaim trap:** reported adoption in captured comments does not prove that
  most viewers copy the behavior or that increased use causes purchase.

## Non-Claims

- Not routine model context, creator evidence, a role taxonomy, or a claim source.
- Not permission to copy a named creator's role or wording onto another creator.
- Not buyer validation, performance proof, conversion evidence, or a guarantee.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: Named creator examples are isolated from the transferable routine Judgment method.
  trigger: product_doctrine
  related_triggers: []
  controlling_sources_updated:
    - forseti/product/spines/creator_signal/creator_ideal_audience_calibration_examples_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md
    - forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
  intentionally_not_updated: []
  stale_language_search: >
    rg -n "Accepted first-screen calibration|Good hiring line" forseti/product/spines/creator_signal
  stale_language_search_result: "Executed 2026-07-16; accepted named-example phrases are confined to this appendix."
  non_claims: [not validation, not readiness, not buyer proof]
```