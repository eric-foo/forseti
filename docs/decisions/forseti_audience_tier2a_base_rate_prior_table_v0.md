# Forseti Tier-2-A base-rate prior table v0 (vet-corrected)

```yaml
retrieval_header_version: 1
artifact_role: sourced data artifact + verification provenance (Tier-2-A category->gender prior)
scope: >
  The honest v0 of the category->gender base-rate prior for the gated Tier-2-A
  demographic slice. Built by VERIFYING each figure against its cited source (web);
  only web-confirmed numbers carry a probability, everything else is an explicit
  data-gap. Supersedes an unvetted ChatGPT-Pro draft whose makeup/fragrance numbers
  did not survive the citation check (see Verification). Aggregate, text/market-derived,
  US-first, defeasible; never a hard map, never Tier-1, never persisted per-individual.
use_when:
  - Loading the Tier-2-A category->gender prior (once the deciding module + data class exist).
  - Reviewing what is and is not source-backed before trusting a demographic prior.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/deep-thinking/orca_audience_tier2a_base_rate_prior_prompt_v0.md   # the sourcing prompt + full schema
  - docs/prompts/deep-thinking/orca_audience_tier2a_priors_resourcing_prompt_v0.md # the stricter re-sourcing follow-up
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - A re-sourced (deeper, quote-traceable) table replaces this thin v0.
  - The Tier-2-A binding posture or the defeasible-prior treatment changes.
```

## Status

`SOURCED_THIN_V0` — **version `forseti-tier2a-beauty-prior-us-0.1.0`**, as-of `2026-06-25`.
Verified, not calibrated, not production-validated. **Deliberately thin:** it contains
ONLY figures confirmed against the cited source. It is a defeasible *starting floor* —
creator-owned public text overrides every row, and **no row may assign gender to an
individual.** Schema: see the prompt artifact in `open_next` (long-form `category_id ·
dimension · bucket · probability · measurement_frame · measure_type · prior_strength ·
basis_label · source · year · sample_basis · derivation_note · limitations · status`).

## Verified rows (the only ones with a probability)

Measurement frame: `women_men_only` (sources measure women/men; `neutral_unknown` is
`null`, never 0). Probabilities are user/wearer **composition** (share of category users),
to 2 decimals.

| category_id | bucket | probability | prior_strength | basis | source · year |
|---|---|---|---|---|---|
| `beauty.skincare_routine` | women | 0.68 | weak | composition derived from **verified prevalence 62% W / 29% M**, US-pop-weighted | CivicScience 2023 |
| `beauty.skincare_routine` | men | 0.32 | weak | " | CivicScience 2023 |
| `fragrance.body_fragrance_any` | women | 0.59 | weak | **verified daily-wearer split (41% male → 59% female)**; only the daily band is sourced, used as the any-wearer proxy | CivicScience 2018 |
| `fragrance.body_fragrance_any` | men | 0.41 | weak | " | CivicScience 2018 |

`prior_strength = weak` on both: skincare prevalence is recent (2023) but its sample
basis is undisclosed; the fragrance split is one frequency band and **stale (2018)** —
later data (Circana 2023) shows Gen-Z fragrance growth, so it should be overridden readily.

## Data-gaps (no defensible prior — creator evidence must decide)

`probability = null`, `prior_strength = none` for all of these:

- `beauty.color_cosmetics_makeup_any` — **gender split rejected.** ChatGPT cited "77% W / 25% M (at least occasionally)"; the article's gendered makeup data is about *frequent* use, **not** that split, and gives no such composition. Only "52% of US adults wear makeup at least occasionally" is real (not a gender prior). The 25%-men figure is not source-backed.
- `fragrance.body_spray_mist` — Mintel-via-secondary (2012), stale, sample undisclosed, **unverified** here.
- `fragrance.fine_fragrance`, `fragrance.market_tier.{designer,niche}`, `fragrance.concentration.{edp,edt,edc_cologne}`, `fragrance.family.{floral,gourmand,woody,fresh_aquatic,citrus,amber,oud}`, `beauty.haircare` — **no representative public US wearer-gender distribution located.** These are the cuts that would actually differentiate fragrance creators, and they do not exist in public data → the gender prior is near-uninformative for most fragrance creators.
- **All `age_band`** — the only candidate (2018 fragrance age composition) is stale and was not fully source-backed. **Age does not use a category prior in v0; it comes from the slang/register signal** (see the re-sourcing prompt).

## Verification provenance (the vet — also the review we send back)

Each active row in the ChatGPT-Pro draft was checked against its cited article on 2026-06-25:

| Draft claim | Result |
|---|---|
| Skincare 62% W / 29% M (CivicScience 2023) | ✅ **Confirmed verbatim** in the article. |
| Makeup 52% overall (CivicScience 2024) | ✅ Confirmed. |
| Makeup **77% W / 25% M** "at least occasionally" + samples 19,774/8,217 | ⚠️ **Not found.** Article reports *frequent-use* gendered trends, not that split; sample sizes not disclosed. **Rejected.** |
| Fragrance **daily 41% male → 59% female** (CivicScience 2018) | ✅ Confirmed. |
| Fragrance some-days **59%** / special-occasion **52%** female (the other inputs to the 0.57 blend) | ⚠️ **Not in the source** (qualitative only). The 0.57 derivation used unsourced numbers; replaced here with the verified daily split (0.59). |

Pattern: real outlets + a few exact figures + several interpolated numbers presented as
sourced. The verified figures were kept; the unverified ones were demoted to data-gap.

Sources checked:
- https://civicscience.com/key-skincare-trends-mens-skincare-top-products-the-connection-with-mental-well-being/
- https://civicscience.com/makeup-wearing-declining-among-women-but-increasing-among-men/
- https://civicscience.com/u-s-adults-may-seek-fragrances-to-reclaim-their-youth/

## Limitations / how this is used

- **Binary frame** — no inclusive gender distribution in the sources; `neutral_unknown` stays `null`.
- **Thin + weak** — two weak gender rows; everything fragrance-specific is a data-gap. So the prior is a soft floor, not a discriminator.
- **Therefore:** gender leans on **explicit creator text**; **age** leans on the **slang/register lexicon**; this table is only the defeasible fallback when text is silent.
- Not validation, readiness, calibration, or buyer proof. The deeper, quote-traceable table is the re-sourcing prompt's job.
