# Orca Audience Tier-2-A Base-Rate Prior Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Prompt artifact (deep-thinking / external data-sourcing reasoning). Paste-ready,
  NO-REPO prompt for a ChatGPT Pro pass that produces the SOURCED, VERSIONED Tier-2-A
  priors: a per-category base-rate table seeding the category->gender (and age-band)
  DEFEASIBLE prior, PLUS a slang/register->age-cohort lexicon for the audience-age
  signal. External sourcing only; the table schema, ledger-schema home, and the
  defeasible-prior deciding module are built in-repo afterward.
scope: >
  Unblocks the one build/data gate the owner cannot default: a cited base-rate
  distribution P(gender | fragrance/beauty category) (+ age-band where available),
  aggregate + text/market-derived + versioned, that creator-specific evidence later
  updates and overrides. NOT a hard category->gender map; never Tier-1; never persisted
  per-individual.
use_when:
  - Sourcing the Tier-2-A category->gender (+ age-band) base-rate prior table.
  - Defining the table shape so the consuming deciding module + ledger home can be built.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/decisions/orca_audience_ballot_taxonomy_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
stale_if:
  - The Tier-2-A binding posture (aggregate / text-only / legitimate-interests / transient / no special-category) is amended.
  - The defeasible-prior treatment (CE2) changes.
  - A base-rate table is adopted (this prompt's question is then settled; versioned refreshes supersede).
```

```yaml
orca_prompt_preflight:
  output_mode: file-write + paste-ready-chat copy
  template_kind: deep-thinking
  edit_permission: docs-write
  target_files:
    - docs/prompts/deep-thinking/orca_audience_tier2a_base_rate_prior_prompt_v0.md
  branch: claude/audience-tier2a-base-rate-prompt
  dirty_state: clean before prompt authoring
  reviews: none bound; prompt artifact for external data sourcing
  doctrine_change: none; produces DATA (a sourced prior table) that a gated slice consumes
  destinations:
    prompt_artifact_path: docs/prompts/deep-thinking/orca_audience_tier2a_base_rate_prior_prompt_v0.md
    downstream_output: chat-only response from ChatGPT Pro (no repo access)
```

## Paste-Ready Prompt

You are ChatGPT Pro. This is a NO-REPO data-sourcing reasoning pass. Produce a **sourced, versioned base-rate table** and a **table shape spec** — not code, not a readiness claim. Use only public/published knowledge; cite every number.

### Objective

An audience-inference system infers "who is a creator's content for?" from the creator's OWN public text. Most fields are content-positioning. One **gated** slice estimates the creator's **aggregate audience gender-skew** (and age-band). For the category→gender component it uses a **defeasible documented base-rate prior**: a Bayesian distribution `P(gender | category)` that a specific creator's own evidence then updates and can **override**. The prior must be a **cited statistic, never a stereotype guess.** Your job is to produce that prior table for the **fragrance / beauty** space — and, for the **age-band** signal, a **slang/register → age-cohort lexicon** (a creator's language register — kid/meme slang vs casual vs professional jargon — is a strong text signal for who the content is *for*).

### Hard constraints (the prior must respect these)

- **Aggregate only** — population-level distributions per category, never per-person.
- **Public/published sources** — market research, consumer surveys, retail/category sales data, census-style demographics. **Never** faces, biometrics, or private data.
- **Defeasible** — this is a *starting* prior that creator-specific evidence overrides; downstream output must distinguish *prior-dominated* vs *evidence-dominated*. So each row also needs a **prior-strength** signal.
- **Sourced + versioned** — every number cites a source + year; the table carries a version stamp.
- **No special-category data** — gender and age-band only, aggregate. No health, politics, religion, sexuality, ethnicity.
- **Coverage over false precision** — "a general base rate to start, refined over time." A cited range or an explicit data-gap beats an invented decimal.
- **US-first** (note region explicitly where a figure is non-US or global).

### What to produce

1. A **category taxonomy** keyed to gender/age-differentiated demand, at the granularity that actually has published data — e.g. fragrance family (fresh/aquatic, woody, oriental/amber, gourmand, floral, citrus, oud), product class (designer vs niche, cologne vs perfume/EDP, body mist), and adjacent beauty (skincare, color cosmetics, haircare) if relevant. Justify the granularity.
2. A **category → gender table**: `P(women)`, `P(men)`, `P(neutral/unknown)` per category, each with a source + year + rough sample/confidence basis.
3. A **category → age-band table** where data exists (e.g. 18–24 / 25–34 / 35–44 / 45+), same sourcing discipline.
4. A **prior-strength** marker per row (how concentrated/reliable the prior is) so the consuming system knows how readily creator evidence should override it.
5. A **table shape / schema spec** — the exact columns + types + a `version` field — so the distribution loads as a versioned data file.
6. A **slang / register → age-cohort lexicon.** A strong *text* signal for audience **age** is the creator's **language register**: kid/meme slang (e.g. "six seven"), casual, or professional/technical jargon. Produce a lexicon mapping a **marker** (a slang term or a register feature) → a likely **age cohort**, each with a source/era, a **prior-strength**, and a **volatility/decay** note (slang turns over fast → this table needs periodic refresh). Same discipline as the base rate: the marker is what an extractor *detects*; the **lexicon** (never a model's gut) maps marker→cohort; and it is **defeasible** (irony, nostalgia, the creator's own age ≠ their target).
7. **Sources** (full citations) and **limitations / risks** — data gaps, region/recency bias, slang volatility, where any prior is weak or should not be trusted.

### Required output format

1. Recommendation + the category granularity you chose and why.
2. Category → gender table (`category · P(women) · P(men) · P(neutral/unknown) · prior_strength · source · year`).
3. Category → age-band table (where available).
4. Table shape / schema spec (`column · type · meaning`, plus the `version` field).
5. Slang / register → age-cohort lexicon (`marker · age_cohort · register_class · era/source · prior_strength · volatility`).
6. Sources (full citations).
7. Limitations / risks / coverage gaps.

Use `sourced`, `estimated-from`, `low-confidence`, `data-gap` labels where useful. Do not invent precise numbers without a source — prefer a cited range or an explicit `data-gap`. Do not write code, and do not claim the table is validated, calibrated, or production-ready.
