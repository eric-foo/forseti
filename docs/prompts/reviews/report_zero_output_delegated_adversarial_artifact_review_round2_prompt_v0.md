# Delegated Adversarial Artifact Review — Report Zero, ROUND 2 (post-patch verification)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (round-2 delegated cross-vendor review of the PATCHED Report Zero output — closure verification of AR-01..AR-06 plus regression sweep; couriered externally with the round-2 zip source pack)
scope: >
  The route-out prompt commissioning the round-2 de-correlated, non-Anthropic
  review after the round-1 blocker verdict was adjudicated and patched.
  Blocker/major-free on THIS round is the D-1 criterion-5 bar; the home lane
  adjudicates the return.
use_when:
  - Couriering the patched Report Zero output for its round-2 review.
  - Adjudicating the round-2 return against the D-1 gate.
authority_boundary: retrieval_only
open_next:
  - docs/research/report_zero/aphrodite_report_zero_review_round1_adjudication_v0.md
  - docs/research/report_zero/aphrodite_report_zero_grade_v0.md
stale_if:
  - The round-2 return is adjudicated.
```

Operator instruction: paste the prompt below into a fresh NON-Anthropic model
session (e.g. the same ChatGPT Pro family that ran round 1) and attach
`report_zero_review_pack_round2.zip` (25 files: the 24 round-1 entries at
their PATCHED state + the round-1 adjudication record). Bring the return back
to the home lane for adjudication.

---

````markdown
# Adversarial Artifact Review — "Report Zero" ROUND 2: verify the round-1 patch (zip attached)

## Commission

commission_mode: delegated cross-vendor adversarial artifact review (round 2 — closure verification + regression sweep)
terminal_output_mode: paste-ready-chat (no repo access; everything you need is in the attached zip)
output_mode: paste-ready-chat
review_posture: adversarial — verify each claimed closure yourself; do not take the patch's word for anything
no_runtime_model_recommendation: true

actor_receipt:
  artifact_author_family: Anthropic / Claude (claude-fable-5 authored every reviewed artifact AND the patch)
  round1_reviewer: OpenAI GPT-5 returned verdict=blocker (findings AR-01..AR-06); the home lane accepted all six and patched
  controller_requirement: you MUST be a non-Anthropic model family; if you are Anthropic-family, return BLOCKED_CONTROLLER_NOT_DECORRELATED and stop.
  home_lane: adjudicates your return; your findings are claims, not accepted truth.

## What changed since round 1 (the patch under review)

The zip contains the PATCHED artifacts plus
`aphrodite_report_zero_review_round1_adjudication_v0.md` — the home lane's
per-finding verdicts, the diagnosed root causes, and the adopted
resolution-granularity rule. The claimed closures:

1. **AR-01:** all 30 corpus claim objects now materialize the seven provenance
   fields per claim (structured `source_refs` with actual hashes); all 15
   coded files carry a `record_provenance` block with the real 64-hex
   video/transcript/watch/comments hash chain; "same cue @ms" receipts
   expanded to verbatim quote + video_id@ms; the 7 withholds carry explicit
   `receipt: none — withheld` self-documentation.
2. **AR-02:** `adj.organic_brand_product_presence` and
   `adj.organic_attention_stance` downgraded and relabeled "self-funded
   editorial"; the report's decision read no longer claims organic coverage.
3. **AR-03:** one granularity rule adopted (most-specific reference entry;
   distinct flankers without an entry are unresolved): "Absolute Aventus"
   mentions re-coded to `product:creed.aventus-absolu` in the two source
   videos; nySgot9sqMY's Sauvage-Elixir and BdC-Exclusive forecasts withdrawn
   to an unresolved flanker-forecast entry; tier distribution corrected to
   8 designer / 2 niche / 1 luxury.
4. **AR-04:** ALL attention rows recomputed mechanically from the coded files
   (not just the two round-1 samples): Sauvage 7/283,773 (stands),
   Bleu 7/272,266, Y-EDP 6/228,259, Invictus 5/223,026, Aventus 4/138,511,
   Absolu 2/90,066, Coach 4/177,733, Ultra-Male 4/141,980, Allure 3,
   Versace 3, LV 2/65,054; bought-because-of-creator reconciled to 14 (12
   product-specific + 2 channel-level, named); ownership 157; top-3 30.8%.
5. **AR-05:** allocation methods now displayed on-panel beside every
   view-weighted surface, including the disclosure that no fractional
   tier/note view-distribution was computed.
6. **AR-06:** run log corrected to 30 claim objects with an erratum note.

## Your verification duties (all of them)

A. **Closure check, finding by finding.** For each of AR-01..AR-06: is the
   defect actually closed in the artifacts (not just claimed closed in the
   adjudication record)? Recompute AR-04's sums yourself from the coded files.
   Re-run AR-01's field audit yourself (all 30 corpus claims, all 15 coded
   records).
B. **Regression sweep.** Did the patch break anything that passed in round 1?
   Spot-check: total views 552,859; the Sauvage 51% share; the withhold texts;
   M2 two-number display; person-level boundary; synthetic-buyer disclosure;
   internal consistency between coded files, derived claims, and the report
   after the renumbering.
C. **Granularity-rule audit.** Is the adopted rule applied consistently
   everywhere (Aventus/Absolu split, Sauvage-Elixir unresolved, Le Male In
   Blue precedent, Invictus original-EDT unresolved)? Any mention resolved
   against the rule?
D. **New-defect hunt.** The patch touched 20+ files; hunt for anything it
   introduced (broken JSON semantics, contradictory numbers, receipts that no
   longer match their entries).

## Verdict + return contract

Return, in order:
- `review_summary` YAML: {round: 2, verdict: blocker|major|minor|clean,
  counts by severity, closure_check: {AR-01..AR-06: closed|not_closed},
  fabrication_check: pass|fail, confidence}
- Findings ordered by severity (file + location, exact defect, contract it
  violates, minimum fix). An unclosed round-1 finding is at least major.
- Your recomputations with numbers.
- Residual-risk note (what the zip cannot prove — e.g. lake packets).
- Adjudication note: findings are claims for the home lane to adjudicate.

Do not rewrite the artifacts. Do not review strategy. Do not re-litigate the
governing contracts or the adjudicated rule choices — but DO flag if a rule is
applied inconsistently or an adjudication claim misstates what the artifacts
contain. Findings only.
````
