# Orca Tier-2-A Priors Re-Sourcing Prompt v0 (quote-traceable)

```yaml
retrieval_header_version: 1
artifact_role: >
  Prompt artifact (deep-thinking / external data-sourcing reasoning). Paste-ready,
  NO-REPO, MODEL-AGNOSTIC prompt (ChatGPT Pro or Claude/Opus with live web) for a
  STRICTER re-sourcing pass on Orca's Tier-2-A priors after a first pass laundered
  interpolated numbers as sourced. Adds a hard quote-traceability rule and feeds the
  prior vet back so the failure cannot repeat.
scope: >
  Re-source two Tier-2-A priors for fragrance/beauty: (1) category->gender base-rate
  table (+ age-band where genuinely sourced), (2) slang/register->age-cohort lexicon.
  Every numeric cell must be backed by a verbatim quote + URL or marked data-gap.
  Aggregate, text/market-derived, US-first, defeasible; never a hard map, never Tier-1,
  never per-individual.
use_when:
  - Re-running the Tier-2-A prior sourcing with citation discipline a model can't fake.
  - Sourcing the slang->age lexicon for the audience-age signal.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_audience_tier2a_base_rate_prior_table_v0.md   # the vet-corrected v0 table + verification
  - docs/prompts/deep-thinking/orca_audience_tier2a_base_rate_prior_prompt_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - A quote-traceable table + lexicon are adopted (this prompt's question is then settled).
  - The Tier-2-A binding posture or the defeasible-prior treatment changes.
```

```yaml
orca_prompt_preflight:
  output_mode: file-write + paste-ready-chat copy
  template_kind: deep-thinking
  edit_permission: docs-write
  target_files:
    - docs/prompts/deep-thinking/orca_audience_tier2a_priors_resourcing_prompt_v0.md
  branch: claude/audience-tier2a-base-rate-prompt
  dirty_state: clean before prompt authoring
  reviews: embeds the in-repo vet of the first pass (findings-first; no formal verdict bound)
  doctrine_change: none; produces DATA (priors) a gated slice consumes
  destinations:
    prompt_artifact_path: docs/prompts/deep-thinking/orca_audience_tier2a_priors_resourcing_prompt_v0.md
    downstream_output: chat-only response from ChatGPT Pro or Claude/Opus (web-enabled, no repo access)
```

## Paste-Ready Prompt

You are a careful research assistant **with live web access**. This is a NO-REPO, **quote-traceable** data-sourcing pass. A previous pass produced a table that *looked* sourced but had invented figures dressed in real citations — your job is to do it **strictly**. Return tables + per-number quotes + a shape spec. No code, no readiness claim.

### Objective

Orca infers "who is a creator's content for?" from the creator's OWN public text. A gated slice estimates the creator's **aggregate audience gender-skew and age-band**, using **defeasible documented priors** that the creator's own evidence overrides. Source two priors for the **fragrance / beauty** space:

1. a **category → gender base-rate table** (+ age-band where genuinely sourced);
2. a **slang / register → age-cohort lexicon** (a creator's language register — kid/meme slang vs casual vs professional jargon — is a strong text signal for audience age).

### The hard rule (this is the point of this pass)

**Every numeric cell must be backed by a VERBATIM quote from the cited page, with the URL.** Put the quote in the row. If you cannot quote a number from a real, currently-loadable source, the cell is **`data-gap`** — do **not** estimate, interpolate, or round a guess into a number. If a value is *derived* (e.g. composition from prevalence rates), **every input to the derivation must itself be quote-backed**, and you must show the arithmetic. A plausible-but-unquotable number is a failure, not a contribution.

### What the previous pass got wrong (do not repeat)

An independent vet checked the first pass against its own citations and found:

- **Skincare "62% of women / 29% of men have a routine" (CivicScience 2023): VERIFIED** — keep, with the quote.
- **Fragrance "41% of daily wearers are male" → 59% female (CivicScience 2018): VERIFIED** for the *daily* band only — keep that; the "some-days 59% / special-occasion 52%" figures it also used were **NOT in the article** (qualitative only) — do not reuse them.
- **Makeup "77% of women / 25% of men wear makeup at least occasionally" + sample sizes: NOT FOUND** in the cited article (which reports *frequent-use* gendered trends, not that split). **Treat as data-gap unless you can quote a real source.**
- Fragrance **family / designer-vs-niche / concentration** gender splits: the first pass correctly found **no representative US data** — re-confirm or fill only with quote-backed sources.

### Constraints (the priors must respect these)

- **Aggregate only**, population-level — never per-person.
- **Public/published**, text/market-derived — **never** faces, biometrics, or private data.
- **Defeasible** — a starting prior the creator's evidence overrides; each row carries a **prior-strength** (`medium`/`weak`/`none`) and, for slang, a **volatility/decay** marker (slang turns over fast → periodic refresh).
- **Versioned**, US-first (flag non-US/global), **no special-category** data (gender + age-band only).
- **Coverage over false precision** — a cited range or an explicit `data-gap` beats an invented decimal. `neutral/unknown` = `null` (not 0) when the source uses a binary frame.

### Required output format

1. Recommendation + the category granularity you can actually support with quotes.
2. **Category → gender table** (`category · P(women) · P(men) · P(neutral/unknown) · prior_strength · quote · url · year`).
3. **Category → age-band table** where genuinely sourced (same columns + quote/url).
4. **Slang/register → age-cohort lexicon** (`marker · age_cohort · register_class · prior_strength · volatility · quote/era · url`).
5. Table shape / schema spec (columns + types + a `version` field) for each.
6. Sources (full citations, each with the quote used).
7. Limitations / risks / coverage gaps.

Use `sourced` / `low-confidence` / `data-gap` labels. Do not write code, and do not claim the tables are validated, calibrated, or production-ready. If most cells end up `data-gap`, that is the correct, honest answer — say so.
