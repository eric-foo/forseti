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

`PENDING` — committed after packet assembly and leakage audit, before any
reader output is consumed.

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
