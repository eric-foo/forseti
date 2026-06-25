# Orca Audience-Inference Ballot Bucket + Label Taxonomy Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Prompt artifact (deep-thinking / external architecture reasoning). Paste-ready, NO-REPO
  prompt for a ChatGPT Pro pass on Orca's creator ideal-audience inference "ballot"
  taxonomy: the output-field (bucket) set, the label vocabulary/ontology, the
  Tier-1/Tier-2-A/Tier-3 boundary, and where an aesthetic/"vibe" signal sits. External
  reasoning only; SCI + mini-god-tier framing and any implementation happen in-repo.
scope: >
  Solve two coupled problems: (1) free-text labels split the deterministic tally
  ("beginner"/"newbie"/"starter" count as three), and (2) a leaky demographic DENYLIST
  guards the Tier-1/Tier-2-A boundary. Recommend a bucket set + label ontology + tier
  mapping. Pose (do not decide) the owner's question of collapsing Tier-1/Tier-2-A.
use_when:
  - Asking a no-repo model to reason about the audience-inference field set + label ontology.
  - Deciding the Tier-1 vs Tier-2-A boundary or whether to restructure it.
  - Replacing the leaky demographic denylist with a positive allow-list / SubNiche ontology.
authority_boundary: retrieval_only
open_next:
  - orca-harness/schemas/audience_inference_models.py
  - orca-harness/cleaning/audience_extractor.py
  - orca-harness/scoring/audience_fusion.py
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
stale_if:
  - The Tier-1/Tier-2-A/Tier-3 boundary or the Tier-2-A carve-out is amended.
  - The OutputField set or the fusion modality-cap / abstention model changes.
  - A label allow-list / SubNiche ontology is adopted (this prompt's question is then settled).
```

```yaml
orca_prompt_preflight:
  output_mode: file-write + paste-ready-chat copy
  template_kind: deep-thinking
  edit_permission: docs-write
  target_files:
    - docs/prompts/deep-thinking/orca_audience_ballot_bucket_taxonomy_prompt_v0.md
  branch: claude/audience-ballot-bucket-taxonomy-prompt
  dirty_state: clean before prompt authoring
  reviews: none bound; prompt artifact for external reasoning
  doctrine_change: none; the Tier-collapse question is POSED for reasoning, decided in-repo
  destinations:
    prompt_artifact_path: docs/prompts/deep-thinking/orca_audience_ballot_bucket_taxonomy_prompt_v0.md
    downstream_output: chat-only response from ChatGPT Pro (no repo access)
```

## Paste-Ready Prompt

You are ChatGPT Pro. This is a NO-REPO source-capsule reasoning pass. Use ONLY the capsule below as repository context: do not assume code beyond it, do not invent implementation facts, and do not recommend backend, runtime, scraper, scheduler, or crawler work. Return a decision frame and a recommended taxonomy — not code, not a readiness claim.

### Objective

Orca infers, from a creator's OWN public content (post captions + profile bio — written text, not spoken transcripts), **"who is this creator's content for?"** and attaches an ideal-audience profile to each rostered fragrance/beauty creator. Two passes:

- **Pass 1 — the LLM READS and LABELS.** It reads one post and emits "evidence ballots." Each ballot = `(target_field` a.k.a. the "bucket"`, label, vote −1..+1, modality, a VERBATIM source quote, flags)`. The LLM only *proposes*; it never decides the profile. Guards reject any ballot whose bucket isn't in the allowed set, whose quote isn't literally in the post, or whose label is a forbidden/deferred demographic.
- **Pass 2 — deterministic code DECIDES.** Per bucket it tallies the surviving ballots' weighted votes, applies per-modality caps (no single signal-type can dominate), a dependence discount (a repeated creative counts less), creator-authored-text precedence, and **abstains** when the top signal is weak or the top-two margin is small. **The tally is by EXACT label string.**

You recommend the **ballot taxonomy**: the bucket set, the label vocabulary/ontology, and the tier mapping.

### Source capsule

**Current buckets (Tier-1 output fields):** `segment`, `audience_role`, `purchase_intent`, `skill_level`, `price_tier`. **Labels are currently FREE TEXT** (the LLM writes e.g. `aspirational_beauty`, `beginner`, `conversion`).

**Two weaknesses to solve:**
1. **Free-text labels split the vote.** Because Pass 2 tallies by exact string, `beginner` / `newbie` / `starter` are three different answers and never combine — diluting real signal. A constrained label vocabulary (allow-list, or a hierarchical "SubNiche ontology") is the candidate fix, balanced against not over-rigidifying a fast-moving niche.
2. **The demographic guard is a leaky DENYLIST.** Today a denylist rejects labels like `men_oriented` / `women_oriented` / age cohorts. Denylists leak (miss novel phrasings). A positive allow-list / ontology that *routes* concepts to the right tier is the durable fix.

**Tier structure (governance — load-bearing):**
- **Tier-1 (live):** *content positioning* — what the content IS, read from the creator's own words. Direct, auditable, persistable now.
- **Tier-2-A (council-approved, GATED — not yet built):** *audience demographic skew* (gender-skew / age-band). This is an INFERENCE about the **audience (people)**, often via a **DEFEASIBLE PRIOR** (e.g. "a cologne review skews male-audience") that content evidence can override. It is gated on: (a) a **SOURCED base-rate table** so a prior is a cited statistic, not bare stereotyping; (b) **aggregate-only + transient + legitimate-interests** handling; (c) a **separate ledger home** recording each inference with its provenance and defeasibility. It must NEVER be tallied into the Tier-1 content profile.
- **Tier-3 (forbidden forever):** any inference of gender/age/identity from **faces / appearance / biometrics**; special-category data (health, politics, religion, sexuality); person de-anonymization; individual-level dossiers.

**Operating constraints:** public data only; audience demographics are **aggregate + text-derived only** (never biometric, never per-follower); everything is **object-level** (a public creator handle / public post), never a person dossier; the output profile always carries `actual_audience = not_estimated` (Orca infers IDEAL fit, not measured audience); this lane is never "gold" (gold = a separate Judgment layer).

**Open owner question (reason about it; do not assume the answer):** should Tier-1 and Tier-2-A be **collapsed** into one "allowed" space, leaving only Tier-3 forbidden? The in-house view is **no** — collapsing routes demographic inference through the Tier-1 tally with no sourced base-rate, no defeasibility, and no aggregate/transient handling, which re-opens a recently-closed "demographic-label backdoor." Argue the strongest case both ways and give a clear recommendation.

### Questions to answer

1. **Bucket set:** Are the 5 Tier-1 fields the right content-positioning dimensions? What is missing or redundant? Specifically: should **aesthetic / vibe / tone** be (a) its own Tier-1 field, (b) a label-class under `segment`, or (c) excluded — and why?
2. **Label ontology:** Recommend how to constrain labels to stop synonym vote-splitting *without* over-rigidifying a fast-moving niche — closed enum per field, curated allow-list + an explicit "other" escape, or a hierarchical SubNiche ontology. How are new labels admitted over time, and by whom/what?
3. **Tier boundary:** Keep, collapse, or restructure Tier-1/Tier-2-A? Give a clear recommendation with the governance AND epistemic reasons. Map each proposed bucket/label to a tier.
4. **Aesthetic → age:** If aesthetic/vibe is captured, draw the exact line between the *content* aesthetic (Tier-1) and any *audience-age* inference it implies (Tier-2-A).
5. **Allow-list vs denylist:** Design how a positive allow-list / ontology replaces the leaky denylist so Tier-2-A concepts are *routed* (held for the gated slice), not merely rejected, while Tier-3 stays hard-forbidden.
6. **Fusion fit:** Does your taxonomy work with exact-label tallying + per-modality caps + abstention, or does it require changes to the deciding model? Name any.
7. **v0 vs deferred:** What ships first vs waits until evidence accrues?

### Required output format

1. Recommendation (one screen)
2. Bucket Set — table: field · definition · tier · example labels
3. Label Ontology Approach
4. Tier-1 / Tier-2-A / Tier-3 Mapping (and the collapse question, answered)
5. Aesthetic / Vibe Placement
6. Fusion-Compatibility Notes
7. v0 vs Deferred
8. Visible Limitations / Risks

Use `recommended`, `viable-but-risky`, `reject`, `deferred`, `source-gap` where useful. Do not write code, choose a backend, or claim validation/readiness/product proof.
