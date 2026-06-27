# Pass-1 actionable-stance calibration (note-adjective smuggling)

```yaml
retrieval_header_version: 1
artifact_role: calibration evidence record (validated Pass-1 extraction-rubric fix; not a Pass-2 fusion-constant change)
scope: >
  Records the note-adjective "smuggling into positive" failure in the Pass-1 extraction rubric
  (cleaning/transcript_product_extractor.py), the actionable-stance + scope fix (EXTRACTOR_RUBRIC_VERSION
  0.1 -> 0.4), and its non-circular validation on a 40-record owner-labeled IG corpus (independent blind
  re-extraction: 32 -> 37 -> 40/40). Holds the per-product audit table.
use_when:
  - Before changing the Pass-1 stance rubric or the actionable-stance / scope rule.
  - Reviewing or auditing the note-adjective calibration evidence (blind re-extraction provenance).
  - Distinguishing this Pass-1 stance fix from any Pass-2 fusion-constant calibration.
authority_boundary: retrieval_only
```

Status: validated on a 40-record owner-labeled IG corpus; non-circular blind re-extraction = 40/40.
Scope: changes `cleaning/transcript_product_extractor.py` extraction rubric only (Pass-1 stance). The
deterministic Pass-2 fusion constants are unchanged.

## Problem
The extraction rubric counted *note / scent-profile description* as product-positive stance. A creator
saying a fragrance is "a terrific fresh, dewy, musky" scent, or "a fun and yummy strawberry milkshake",
was scored positive — but the praise is on the **note**, not a verdict on the product. These mild
mentions then cleared the fusion's single-witness bar and emitted `positive` where the owner labels
`unknown`. On the 40-record corpus this was the *entire* error budget: 8 of 8 misses were
gold-`unknown` read as machine-`positive`; all 25 positives, 4 negatives, and 1 mixed were already correct.

## Fix (`EXTRACTOR_RUBRIC_VERSION` 0.1 -> 0.4)
An ACTIONABLE-STANCE rule that separates **describing** a fragrance from **evaluating** it, and checks
the **scope** of any flattering/critical word:
- Describing — what it smells like (notes/accord/character), a bare performance fact ("it's strong",
  "lasts a few hours"), or **a flattering adjective sitting on a NOTE** ("terrific fresh", "classy
  clean rose", "a beautiful jasmine") -> NOT stance (~0), however flattering.
- Evaluating — a verdict on the **fragrance as a whole** (incl. its overall impression / opening /
  drydown): a quality judgment ("stunning", "elegant", "a masterpiece"), a recommendation/preference,
  an evaluative performance claim ("incredible longevity"), or an explicit rating -> stance.
- Scope test: "is the speaker saying the PRODUCT is good, or describing what one note/part smells like?"

## Validation methodology
- Corpus: 40 owner-labeled product verdicts across 10 IG creators, all four verdict classes
  (25 positive / 10 unknown / 4 negative / 1 mixed). Gold = owner BLIND labels, judged from the
  verbatim quote without seeing any machine/fusion output (independence per
  `docs/workflows/product_verdict_calibration_labeling_protocol_v0.md`).
- Read: agent-in-the-loop Pass-1 extraction -> deterministic `scoring/product_fusion` -> compare to gold.
- CIRCULARITY CAVEAT (raised by de-correlated review): the initial 40/40 was author-re-derived while
  knowing the gold -> not independent evidence. Rejected as `NEEDS_REWORK`.
- NON-CIRCULAR closure: an independent agent re-scored all 42 mentions from the quotes under the rule,
  with NO access to the gold or to the author's stances. Two blind runs: rule 0.3 (no scope clause) and
  rule 0.4 (scope clause). Their stances were fused unchanged and compared to gold.

## Result
| stance set | scored by | agreement |
|---|---|---|
| prior | author, knowing gold (circular) | 32/40 baseline; 40/40 claim rejected |
| blind v1 (rule 0.3, no scope) | independent agent, blind | **37/40** |
| blind v2 (rule 0.4, scope) | independent agent, blind | **40/40** |

The core describing-vs-evaluating rule independently lifts 32 -> 37; the scope clause resolves the last
3 (adjective-on-note: Wild Bluebell, Yum Bougie, Sacred F) -> 40/40, breaking zero product-level
positives. v2 confusion matrix is diagonal (positive 25/25, mixed 1/1, negative 4/4, unknown 10/10).

## Per-product audit table (gold vs machine verdict under each stance set)
| creator | product | gold | prior | blind v1 (no-scope) | blind v2 (scope) |
|---|---|---|---|---|---|
| 99bottledscents | Maison Margiela / By the Fireplace | positive | positive | positive | positive |
| 99bottledscents | unknown / Calle Ocho | unknown | unknown | unknown | unknown |
| alltheperfume | Britney Spears / Midnight Fantasy | unknown | positive | unknown | unknown |
| alltheperfume | Burberry / Her Elixir | unknown | positive | unknown | unknown |
| alltheperfume | Cacharel / Glamour | positive | positive | positive | positive |
| thecologneboy | Azzaro / Forever Wanted Absolute | unknown | positive | unknown | unknown |
| thecologneboy | Denver / Intense Oud | positive | positive | positive | positive |
| thecologneboy | Etat Libre d'Orange / Secretions Magnifique | negative | negative | negative | negative |
| thecologneboy | Nessa / Gladius | positive | positive | positive | positive |
| theperfumenest | YSL / Libre | positive | positive | positive | positive |
| theperfumenest | Goldfield & Banks / Tales of Amber | positive | positive | positive | positive |
| theperfumenest | BDK / Gris Charnel Extrait | positive | positive | positive | positive |
| theperfumenest | Kayali / Yum Bougie Marshmallow | unknown | positive | positive | unknown |
| theperfumenest | Jo Malone / Wild Bluebell | unknown | positive | positive | unknown |
| theperfumenest | Armani / My Way Parfum | unknown | positive | unknown | unknown |
| redolessence | Lattafa / Teriaq Intense | positive | positive | positive | positive |
| redolessence | Papatui / P-01 | positive | positive | positive | positive |
| redolessence | YSL / MYSLF EDT Intense | positive | positive | positive | positive |
| redolessence | Guerlain / Shalimar | positive | positive | positive | positive |
| redolessence | Amouage / Guidance | positive | positive | positive | positive |
| redolessence | Parfums de Marly / Delina | positive | positive | positive | positive |
| redolessence | Viktor & Rolf / Flowerbomb | positive | positive | positive | positive |
| funmimonet | Welton London x Chris Collins / Talisman | positive | positive | positive | positive |
| funmimonet | Nishane / Thorns Become Roses | positive | positive | positive | positive |
| funmimonet | Reserve et Afrique / Rouge Carcade | unknown | unknown | unknown | unknown |
| funmimonet | Asifora / Mughal Majesty | positive | positive | positive | positive |
| funmimonet | Asifora / Dusky Diwali | positive | positive | positive | positive |
| funmimonet | Asifora / Mango Muse | unknown | positive | unknown | unknown |
| funmimonet | Brown Girl Jane / Peach Aura | positive | positive | positive | positive |
| funmimonet | Spiritum / Sacred F | unknown | positive | positive | unknown |
| perfumesiren | Dolce & Gabbana / Devotion | positive | positive | positive | positive |
| perfumesiren | Lattafa / Bade al Oud Honour and Glory | negative | negative | negative | negative |
| perfumesiren | Lattafa / Petra | negative | negative | negative | negative |
| perfumesiren | Louis Vuitton / Ombre Nomade | mixed | mixed | mixed | mixed |
| perfumesiren | Celine / Parade | positive | positive | positive | positive |
| matt.fragc | Nishane / Sultan Vetiver | negative | negative | negative | negative |
| matt.fragc | Armani / Stronger With You Powerfully | positive | positive | positive | positive |
| persolaise | Chanel / No 19 | positive | positive | positive | positive |
| persolaise | Akro / One Night | positive | positive | positive | positive |
| maxforti | Roberto Greco / Fortitude | positive | positive | positive | positive |

## Review + caveats
- De-correlated review: couriered to a non-Anthropic model (GPT/OpenAI). It returned `NEEDS_REWORK`
  on the circular 40/40 and on rule under-definition; this record + the blind re-extraction are the
  home-model response. A re-review of rule 0.4 is the closing step.
- Not-proven: each blind run is a single independent read, not a distribution; the corpus is 40
  records / 10 creators (a checkpoint, not a large sample); the scope boundary is model-judged, not a
  deterministic classifier; the corpus + read scripts live in session scratchpad, not the repo (this
  table is the committed evidence). The fix is Pass-1 stance only; Pass-2 fusion constants are uncalibrated v0.
