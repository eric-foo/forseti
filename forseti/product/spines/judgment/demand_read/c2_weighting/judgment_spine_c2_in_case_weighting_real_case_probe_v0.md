# Judgment-Spine C2 In-Case Weighting Real-Case Probe v0 (PROPOSED — first real-evidence paired read, Medicube Age-R Booster Pro / Ulta rollout)

```yaml
retrieval_header_version: 1
artifact_role: Feasibility probe (design/docs experiment — the series' first REAL-evidence paired read; a retrospective, frozen-cutoff, real-world beauty-device demand case run under the hardened Instruction Core and the owner-adopted agreement standard, then revealed and graded on decision quality; binds no case fixture, populates no ledger, runs no conductor gate)
scope: >
  Round three of the paired-read probe series, first with real evidence:
  the late-April 2025 decision moment around committing to a full nationwide
  US retail rollout of the Medicube Age-R Booster Pro (APR Corp) — a
  TikTok-driven K-beauty device wave whose durability was genuinely uncertain
  at the cutoff. Two blind Sonnet readers, opportunity/caution framings, a
  provenance-tagged evidence packet frozen at 2025-04-30, contamination
  tell-audit, agreement audit under the owner-adopted standard, then outcome
  reveal and qualitative decision-quality grading. Owner-authorized
  ("could we do a real one?"), beauty niche per owner direction.
use_when:
  - Checking what real-evidence support exists for the in-case weighting doctrine, and at what claim tier.
  - Designing the next real-case read or a Level 1 backtest case (method deltas from synthetic to real live here).
  - Auditing how the contamination tell-audit and decision-quality grading were applied on a real case.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md   # the doctrine under test (hardened + owner-adopted agreement standard)
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_weighting_paired_read_probe_v1.md   # round two (synthetic, hardened core)
stale_if:
  - The owner adjudicates the doctrine (adopt / amend / reject).
  - A Level 1 backtest case or later real-case read supersedes these observations.
  - INV-1 (no-scoring boundary) is amended by the owner.
```

## Status

`PROPOSED` — design/docs experiment, `product_learning` tier, authored
2026-07-10 in the judgment evidence-weighting lane on explicit owner
authorization for a real case in the beauty/fragrance niche. **This is a
probe, not a Level 1 case:** it admits no casebook fixture, clears no JSG
gate, runs no conductor, populates no ledger row, and burns no reserved
casebook candidate (exclusion verified below). Real-world facts appear here
as probe inputs with provenance; nothing in this artifact is a market claim
or product recommendation.

**Two-stage pre-registration.** Stage 1 (this commit): case selection,
cutoff, decision frame, method, agreement standard, contamination rule, and
the decision-quality grading rubric — committed before the author consumes
any captured evidence. Stage 2 (a later commit, before any reader output is
consumed): the frozen packet and per-item expectations. Reader outputs are
consumed only after stage 2 is committed; the lane's commit history is the
ordering evidence.

## Case Selection (stage 1)

A delegated scout surveyed beauty/fragrance-niche candidates (2024–2026
decision moments with observable outcomes), after first extracting and
excluding every product named by the Level 1 casebook screens
(`fragrance_level1_named_case_candidate_screen_v0.md`,
`fragrance_level1_casebook_admission_frame_v0.md`) so no reserved casebook
candidate is burned by this probe.

**Selected: Medicube Age-R Booster Pro (APR Corp) — the nationwide US
rollout commitment, cutoff 2025-04-30.** Why over the alternatives:

- The decision is demand-read shaped: "is this TikTok-driven device wave
  durable demand or a fad?" — the durable/transient question the C2/C3 core
  exists for.
- Lowest memorization risk among gradeable candidates (K-beauty / TikTok
  Shop circles rather than mainstream news), and the decisive outcome
  signals land mid/late 2025 — at or past the plausible knowledge edge of
  the reader models. Residual risk is handled by the tell-audit, not
  assumed away.
- Rich pre-cutoff evidence across venue types, on both the hype side and
  the skepticism side.
- The outcome is **mixed** (see Sealed Outcome), which grades right-sizing
  rather than rewarding a lucky binary call.

**Reserve (deliberately not used, kept unburned): Youthforia** — a cleaner
resolved divergence (retailer split, later shutdown) but with its whole arc
plausibly inside current reader models' training data; suitable later for
older-cutoff models or a recall-controlled design. **Considered and set
aside:** Solawave and Dossier (outcomes not yet gradeable; Dossier noted as
the only pure-fragrance option — revisit when its pivot resolves), Bubble
(fame/meme memorization risk), Rhode/e.l.f. (too famous, no tension;
usable someday as a positive control, not a probe).

## Decision Frame (what the readers are given; time-shifted)

Readers are told: *today is 2025-04-30.* They advise a large US beauty
retailer deciding within two weeks whether to commit to a **full nationwide
rollout** (1,300+ stores, launch window August 2025) of the Medicube Age-R
Booster Pro — versus a staged/limited rollout, or passing. A wrong
overcommit means shelf-space opportunity cost and markdown exposure on a
$100+ device; a wrong undercommit risks losing category leadership in the
K-beauty device wave to a competing retailer. Horizon: through the 2025
holiday season.

## Sealed Outcome (recorded for the auditor; readers are prompt-only and never see this artifact)

As captured by the scout with citations (to be re-verified at reveal): the
nationwide rollout proceeded (August 2025 launch; 610 Ulta-at-Target doors
plus ~1,400-store chain presence per trade coverage); the brand publicly
reported crossing $100M+ revenue and 1M+ units for the franchise; and by
Black Friday (November 2025) the flagship device was discounted up to ~44%
— a signal consistent with overstock and/or wave-cooling, sitting alongside
the success narrative. The outcome is therefore **mixed**: the demand was
real and large in-window; its durability at full price past the holiday
peak is in genuine doubt. Grading uses this shape, not a win/lose label.

## Method

- **Packet:** 12–16 real evidence items captured by two delegated research
  workers (community/social and trade/hard-signal lanes), every item from a
  source verifiably published on or before 2025-04-30, each carrying venue
  type, URL, publication date, and a summary written from the cutoff
  vantage. The author assembles the packet and runs a leakage audit (no
  post-cutoff facts or hints) before any reader sees it. Deliberate
  diversity: hype, skepticism, hard costly-behavior data (sales/financials),
  expert efficacy commentary, and category base-rate context.
- **Readers:** two isolated Sonnet-tier `worker` subagents, fresh contexts,
  tools forbidden, blind to each other, to the probe series, and to the
  outcome. One opportunity framing, one caution framing; identical item
  text, different order. The hardened Instruction Core embedded verbatim.
- **Contamination tell-audit (real-case addition):** any trace that asserts
  post-cutoff facts (the launch happened, revenue milestones, discounting),
  cites knowledge not derivable from the packet, or reasons from the outcome
  backwards carries a confirmed tell → that read is quarantined as
  contaminated data and the probe says so; tells are checked before any
  agreement or quality grading. This consumes the spine's outcome-USE
  contamination posture; the Instruction Core's own step-4 clause (background
  beliefs are not evidence) is the producer-side guard.
- **Agreement audit:** the owner-adopted standard (2026-07-10): per-item
  direction + load-bearing facts + the ceiling-binding weakest item; declared
  single role wobble and attributable one-band level drift tolerated.
- **Named limitations:** the author holds the sealed outcome while
  assembling the packet (NOT a zero-spoiler constructor — a real deviation
  from the Level 1 ideal, mitigated by the two-stage pre-registration and
  the leakage audit, and disclosed here); capture workers unavoidably saw
  post-cutoff material while searching (their packet items are date-bounded;
  the leakage audit is the control); same model family throughout; one case;
  publication dates verified from page metadata (residual misdating risk).

## Decision-Quality Grading Rubric (pre-registered; qualitative, INV-1-safe)

Graded at reveal, per reader, against the packet-available evidence — not
against the outcome's luck (an evidence-right call that the world punishes
carries zero regret; spine doctrine):

1. **Direction fit:** did the verdict direction follow what the packet's
   load-bearing evidence supported? (Given the sealed outcome's shape, a
   packet-faithful read plausibly supports real-and-large current demand
   with genuinely uncertain durability — but this expectation is the
   auditor's prior, stated here so it can be wrong in public.)
2. **Right-sizing:** was the recommended action staged/hedged in proportion
   to what the weakest load-bearing item could carry — specifically, did the
   read distinguish committing to the *wave now* from betting on *full-price
   durability past the holiday peak*?
3. **Anticipation:** did the missing-evidence / counterfactual lines
   anticipate the class of signal that actually resolved the uncertainty
   (sell-through vs discount-depth after launch; wave-cooling indicators)?
4. **No outcome laundering:** grading cites packet items and the sealed
   outcome's shape only; no credit or blame for facts neither reader could
   see. The grade is stated qualitatively (e.g., "right-sized with the
   durability hedge named" / "over-committed relative to the weakest
   load-bearing item"), never as a score.

## Stage-2 Pre-Registration (packet + per-item expectations)

Committed after capture and leakage audit, before any reader is dispatched
or any reader output consumed. Leakage audit result: all 15 items date to
2025-04-30 or earlier (E7's date rests on secondary corroboration — flagged,
kept, pre-cutoff by ~6 weeks); no summary references the Ulta announcement
(May 12, 2025), the August 2025 launch, later revenue milestones, or
holiday discounting. The reader-facing decision frame names "a large US
specialty beauty retailer," not Ulta — a deliberate de-memorization step.
Known packet limitation: no verifiable pre-cutoff Reddit thread was
capturable (venue tooling blocked; secondary aggregators excluded for date
integrity), so community skepticism arrives via TikTok/press instead.

**The frozen packet (verbatim as given to readers; venue + date shown):**

- **E1** [TikTok, 2024-02-23] A creator demo captioned "2024 me: using
  Medicube AGE-R Booster Pro, 6-in-1 home aesthetic device," walking through
  Air Shot mode ("gentle exfoliation with electric needles") and microcurrent
  mode ("stimulates collagen production"), tagging the brand. The caption is
  explicitly marked "ad."
- **E2** [TikTok, 2024-08-12] A creator unboxes the Booster Pro, noting
  Medicube "so nicely gifted it to me without me even knowing," calling it
  "overall a pleasant experience, 100% would use in my daily routine" — an
  enthusiastic first impression, not a longer test.
- **E3** [Consumer press (Glamour, syndicated), 2024-09-05] A reviewer
  reports visible lifting/brightening after two minutes of microcurrent use,
  praises battery life, and notes the $399 device claims to boost product
  absorption by 490% in five minutes. The piece ties the device's popularity
  to Hailey Bieber, whose TikTok of the earlier Booster-H model "helped
  launch widespread virality." Concrete criticism: control buttons sit where
  fingers grip, so users accidentally change settings mid-treatment.
- **E4** [TikTok, dermatologist, 2025-01-18] A dermatologist responds to a
  viral claim that the Booster Pro caused Bell's palsy after two days of
  lowest-setting use: she states there isn't sufficient research to confirm
  causation, while demonstrating on herself that a comparable device can
  visibly trigger facial muscle twitching.
- **E5** [Consumer press (NewBeauty), 2025-01-21] Coverage of the viral
  TikTok (nearly 12 million views) alleging the device caused a user's
  Bell's palsy. Medicube's statement calls the claim "false information,"
  asserting the device's electrical stimulation is "scientifically
  impossible" to cause nerve damage and noting such stimulation is used
  therapeutically for Bell's palsy.
- **E6** [Consumer press (Daily Dot), 2025-01-25] An investigation names the
  TikToker behind the 11.5M-view paralysis claim, notes the device combines
  electroporation, microcurrent, electric needling, EMS, LED, and sonic
  vibration — all delivering electrical current to the face — and reports
  the public split: some commenters abandoned purchase plans; others doubted
  the condition was device-caused.
- **E7** [YouTube, dermatologist, 2025-03-15] A dermatologist's follow-up on
  the safety debate around the "$480 Medicube Booster Pro," explaining what
  the viral narrative got wrong about the device's electrical output and
  nerve-damage risk.
- **E8** [Financial press (Forbes), 2024-02-27] APR Corp (Medicube's maker)
  debuted on the Korea Exchange above its guided range, raising ~$71M;
  shares jumped 27% on debut to a ~$1.8B valuation. Its prospectus recorded
  1.6 million Age-R devices sold as of November 2023; beauty devices were
  82% of revenue over the prior three quarters, with net income nearly
  doubling year over year.
- **E9** [Trade press (Korea Herald), 2025-01-20] At CES 2025, Medicube's
  booth traffic roughly doubled to 1,200+ visitors. APR disclosed overseas
  sales exceeded 100 billion won in Q3 2024, up 78.6% year over year, and
  signaled expanded retail, logistics, and marketing abroad.
- **E10** [Financial disclosure coverage, 2025-02-10] APR's FY2024 results:
  consolidated revenue 722.8bn won (+38.0% YoY), operating profit 122.7bn
  won (+17.7%), an 11th consecutive growth year. The Age-R device division
  alone posted 312.6bn won, up 44.6% YoY; overseas annual revenue passed
  400bn won for the first time.
- **E11** [Trade press (Korea Herald), 2024-08-28] APR signed a supply
  agreement with TJX (TJ Maxx, Marshalls — ~5,000 stores across 9 countries)
  for four bestselling Medicube skincare items plus the earlier Age-R
  Booster Healer device, with the next-gen "Booster Pro" teased; timed for
  the Q4 holiday season. The article notes Medicube's Zero Pore Pad has
  consistently ranked bestseller in its Amazon category.
- **E12** [Trade analytics (WWD), 2024-10-22] TikTok Shop data for August
  2024 puts Medicube among the top beauty brands on the platform, with
  K-beauty dominating discourse and sales; Medicube's top-selling kit priced
  ~$240, far above category average — bundle-driven high order values.
- **E13** [Trade analysis (Glossy), 2023-04-18] Why at-home beauty devices
  historically fail: high price without habit formation, over-complicated
  tech, no visible immediate results. Clarisonic exceeded $100M in sales by
  2010, then its parent recorded a $263M impairment by 2016 as it declined;
  P&G's Opte had a 20,000-person waitlist at launch, then faded. NuFace is
  the counter-example (30% share of premium devices, 5M+ units, diversified
  into skincare). A device co-founder is quoted: winners must be "simple"
  and "addictive."
- **E14** [Trade press (Business of Fashion), 2024-09-25] An analysis of
  beauty-tech as "a high-stakes game": Dyson, Foreo, and NuFace case studies
  frame high-tech devices as capital-intensive, hit-driven bets where
  sustained category leadership is hard to hold.
- **E15** [Peer-reviewed systematic review, 2021-05-03] A review of 37 RCTs
  (1,871 patients) on home-based dermatologic devices found Grade-A evidence
  only for IPL hair removal and laser diodes for hair loss; Grade-B with
  reservations for RF and LED uses — and it does not cover
  microcurrent/EMS/electroporation (this device's core modalities) at all.
  The authors flag a persistent lack of double-blinded RCTs and long-term
  efficacy data for home devices generally.

**Framings:** A (opportunity): "should the retailer commit to the full
nationwide rollout?", items ordered E1→E15. B (caution): "the buying team
fears committing 1,300+ stores to a possibly-peaking social-media device
wave — how much rollout commitment is justified?", items ordered E13, E14,
E15, E5, E6, E4, E7, E2, E1, E3, E12, E11, E9, E8, E10.

**Per-item audit expectations (auditor's priors — written to be wrong in
public):**

| Item | Expected handling |
| --- | --- |
| E1 | Promotion, disclosed ad; incentive cap; not_relied_on. |
| E2 | PR-seeded testimony (gift); enthusiasm = cheap talk; not_relied_on / weak. |
| E3 | First-hand short-term testimony via consumer press; mixed (usability complaint = good-faith marker); the 490% figure recognized as a relayed brand claim, not a measurement; supporting at most. Bieber tie = attention-mechanism context. |
| E4 | Expert opinion tempering the scare — but noting the twitch demonstration cuts both ways; competence high; bears on the safety-risk claim; hedges. |
| E5 | The scare's scale is a real demand-side risk signal (12M views, purchase-abandonment potential); the brand rebuttal weighted low (maximal incentive). Expected classification: a declared cap/discount/neutral call on demand durability — NOT a step-10 integrity routing (nothing suggests the demand evidence is fake; the risk is to the product/wave, not to evidence authenticity). A reader that routes it to integrity anyway should declare why. |
| E6 | Corroborates scare scale + genuine split reaction; supporting for the demand-risk claim; NOT independent of E5 on the underlying event (same viral video — count once). |
| E7 | Expert opinion further tempering the scare; supporting; date-confidence flag may be noted. |
| E8 | Costly behavior (market pricing; 1.6M units by Nov 2023); load-bearing candidate for real-demand; temporal note (14 months old). |
| E9 | Costly behavior (disclosed quarterly revenue, +78.6% overseas); fresh; load-bearing candidate. |
| E10 | The anchor: audited-adjacent FY2024 results, device division +44.6%; expected load_bearing in both reads. |
| E11 | Costly behavior by a sophisticated counterparty (TJX, 5,000 stores) — but off-price channel is a genuinely ambiguous consideration (expansion signal vs. clearing-channel signal): expect a declared classification either way. |
| E12 | Platform sales ranking = consumer costly behavior; brand-level not Booster-Pro-specific (role-fit note expected); supporting. |
| E13 | Category base-rate opposing durability (Clarisonic template) with the NuFace counter-example inside it; supporting opposition; must not be averaged away. |
| E14 | Category base-rate; hedges. |
| E15 | The fitness-target gap: independent clinical evidence does not cover this device's core modalities — expected to feed the durability discount and the missing-evidence line; weak-context for current demand. |

**Expected verdict shape (auditor prior):** real, large, accelerating
current demand (E8/E9/E10/E12) with genuinely unresolved durability risks —
the safety-scare demand shock (E5/E6, tempered by E4/E7), the device-fad
base rate (E13/E14), no independent efficacy evidence for the modality
(E15), and no retailer sell-through or Q1-2025 financials in the packet. A
right-sized call ≈ staged or hedged commitment with named kill/scale
triggers; an unhedged full commit or a pass would each need to defeat
evidence they cannot. Expected load-bearing: E10 certainly, plus some of
E8/E9/E12; the ceiling-binding item is left open here — the adopted
standard compares whatever both readers name.

**Pass criteria:** the v1 criteria under the owner-adopted agreement
standard, plus: tell-audit clean (no assertion of the Ulta partnership, the
August 2025 launch, revenue milestones after the cutoff, or holiday
discounting; no outcome-backward reasoning), and grading per the stage-1
rubric.

## Observed Reads

`PENDING`.

## Tell-Audit, Agreement Audit, Reveal, And Grading

`PENDING`.

## Findings And Disposition

`PENDING`.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: in-case weighting doctrine on a real frozen-cutoff case (instruction-following + agreement + decision-quality grading, one case, Sonnet-tier readers)
  source_quality_state: real public evidence captured with URL/date provenance at probe tier; scout + capture by delegated workers; author-assembled packet with leakage audit; author holds the sealed outcome (named deviation)
  execution_quality_state: stage-1 pre-registration only at this commit; capture in flight; no packet frozen, no read run, no reveal
  closeout_state: no_durable_evidence
  claim_cap: product_learning only
  weakest_missing_or_failed_gate: single case; same-family readers; auditor = packet assembler = outcome holder; no conductor, no zero-spoiler constructor, no cross-family grading
  receipt_artifact_or_gap: this artifact is the probe record; a Level 1 conductor-run backtest case with a zero-spoiler constructor is the next-stronger evidence class
  non_claims:
    - not validation, readiness, or buyer proof
    - not judgment-quality evidence
    - not casebook admission, fixture creation, ledger population, or conductor involvement
    - not a market claim, product review, or retail recommendation about Medicube, APR, Ulta, or any competitor
```

## Non-Claims

- A probe over public information for internal product learning; the case
  facts are inputs with provenance, and the readers' verdicts are exercises,
  not commercial advice or claims about any named company.
- Tests within-Claude-family behavior at Sonnet reader tier on one real
  case; not model-independence, not multi-case reliability.
- `product_learning`; the doctrine remains PROPOSED pending owner
  adjudication; this probe adjusts confidence, never claim tier.

```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
