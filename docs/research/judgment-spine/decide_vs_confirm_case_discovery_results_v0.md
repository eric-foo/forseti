# Decide-vs-Confirm Case Discovery Results + Frame-Locks v0

```yaml
retrieval_header_version: 1
artifact_role: Facilitator-side case discovery results + proposed frame-locks (PROPOSED, spoiler-bearing)
scope: >
  Candidate universe + adjudication + a case-selection PROPOSAL + proposed
  frame-locks for the decide-vs-confirm crux tests, from a bounded web-search
  discovery pass applying the memorization-resistant case-finder screen. NOT
  owner selection, NOT validation, NOT captured evidence. Carries sealed outcome
  notes below a divider — facilitator-side.
use_when:
  - Owner selecting / confirming decide-vs-confirm test subjects.
  - Resuming the proof lane to capture and seal a selected case.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/decide_vs_confirm_backtest_case_frame_template_v0.md
  - forseti/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md
  - forseti/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md
  - docs/decisions/orca_moat_judgment_quality_proof_path_decision_chain_v0.md
stale_if:
  - Owner selects / rejects candidates, or the universe is superseded by a later pass.
  - The B2B-vertical deeper pass (in progress) lands and is folded in.
```

## Status

`DISCOVERY_RESULTS_PENDING_OWNER_SELECTION`. A candidate universe + a selection
*proposal* + *proposed* frame-locks. No candidate is selected merely by appearing
here (per the discovery charter). Not validation, not buyer proof, not
judgment-quality, not captured evidence. Cutoffs are `NEEDS_VERIFICATION`; evidence
and outcomes are `NEEDS_CAPTURE`. Freezes nothing.

**Zero-spoiler notice:** everything above the SEALED divider is outcome-free and
blind-judgeable. The SEALED section (and the frame-locks' post-window exclusions
within it) carries outcomes — **do not read it if you intend to be a blind judge.**

Dirty-state: written on the current ECR branch (`ecr-sp3-timing-deriver-slice1`),
untracked; durable-home reconciliation is a separate step.

## Method + honest limits

Two bounded web-search discovery agents (one per family) surfaced candidates from
*outside* model recall, screened against the finder's gate, eligibility-only,
anti-leakage. **A B2B-vertical deeper pass has now completed — folded in under "Deeper B2B-vertical pass" below.**

The two limits that matter:

1. **Obscure ≠ memorization-certified.** The obscurity signal is search-prevalence
   + "the agent didn't already know it" — *not* certified below a frontier
   contestant model's training recall. These are far less famous than Unity/Reddit
   but the memorization gap is *narrowed, not closed*. Real certification needs the
   deferred mechanism (probe the contestant, or training-prevalence).
2. **Narrow-band tension confirmed empirically.** Obscure cases have thin, tangled
   sourcing where outcome and pre-cutoff signal share the same few first-party
   posts. Source-depth is marginal for several; **zero-spoiler packet construction
   (fencing the outcome out) is the hard part** — both agents flagged it.

Diversity gap: no pure B2B-vertical case in the obscure band within the first
bounded budget (candidates cluster in creator/dev/prosumer tools) — hence the
deeper pass.

## Candidate universe (eligibility-only; outcome-free)

### Family A — repricing
- **A1 · Inoreader (RSS reader), 2019 Pro repricing/repackaging.** Bootstrapped
  ~7-person co (Innologica). Decision: how aggressively to gate power-user features
  (Rules limits) into paid tiers under funding pressure. Cutoff ~Jan 2019
  (`NEEDS_VERIFICATION`). Pre-cutoff sources archivable. Obscurity: narrow-band good.
  Outcome known. **Strongest A.**
- **A2 · Supernotes (note app), lifetime-plan introduce→kill→4-yr-license.** Obscure,
  clean, but multi-year arc (blurry single cutoff) and same prosumer-notes shape as
  A1 (diversity weakness). Outcome heavily first-party.

### Family B — clean-substrate competitor-displacement
- **B1 · Craft CMS (Pixel & Tonic) vs. ExpressionEngine.** Ecosystem insider (EE's
  top add-on maker) deciding whether to build the rival the community is leaving
  toward. Substrate: community/forum discontent + agency migration posts (non-review).
  Cutoff ~2012-2013 (`NEEDS_VERIFICATION`). Obscurity: good. **Strongest B (decision sharpness).**
- **B2 · Buttondown vs. TinyLetter (Mailchimp wind-down).** Solo-founder rival deciding
  whether to court the departing cohort. First-party migration substrate. Cutoff
  ~mid/late 2023 (`NEEDS_VERIFICATION`). Risk: famous destination (Substack) could
  swallow the frame; large leakage surface. **Strong alternate.**
- **B3 · Vanilla Forums vs. Discourse/NodeBB.** Clean community-departure substrate,
  but weakest discrete decision-moment + murky outcome. Marginal.

## Adjudicated drops (surfaced flagged; concur)
- **LastPass 2019 (A)** — too famous + later breach/free-tier news everywhere → zero-spoiler infeasible.
- **mastodon.technology shutdown (B)** — weak frame-fit (admin exit, not competitor-response).
- Both agents also explicitly rejected AI-synthesized *fictional* "case studies" and the famous-headline band (Netflix, Unity/Godot, Reddit/Lemmy, Freenode, Photobucket, OSS-license wars).

## Deeper B2B-vertical pass (folded in)

**Structural finding (the binding constraint):** obscure + outcome-resolved +
un-memorized is a *narrow intersection* for B2B-vertical. The cleanest, most-datable
obscure B2B decisions surfaced cluster in 2024-2025 — recent enough to be
un-memorized, but their outcomes have NOT resolved yet (e.g. a 2-yr price freeze
announced Oct 2025 resolves ~2027). The older, outcome-resolved obscure cases tend
to be either famous or thin/tangled-sourced. So for a *backtest* (which needs a
resolved outcome), the obscure-B2B band is genuinely thin — ~17 searches yielded
only 2 soft-eligible repricing candidates and **zero** clean Family-B case.

**Forward-test implication (recorded as an option, not a decision):** the temporal
bind suggests a forward-test variant — pick a recent obscure decision, seal a blind
judgment NOW (definitionally un-memorized post-cutoff; zero-spoiler is trivial
because the outcome does not exist yet), and score it WHEN the outcome resolves.
That dissolves both the memorization and zero-spoiler problems at the cost of
latency (you wait for the outcome). Candidate seed: C3 Ekos.

### B2B-vertical repricing candidates (Family A; eligibility-only)
- **C1 · Genesis Chiropractic Software / ClinicMind (Jan 2024).** Chiropractic
  EHR+RCM vertical; post-acquisition pricing/repackaging of the bundled offering.
  Cutoff ~late 2023 (`NEEDS_VERIFICATION`). Strong obscurity-band fit; the
  **B2B-vertical swap option for Family A**. Risks: "outcome publicly known" is soft
  (slow drift, not a crisp event); cleanest later signal sits partly on REVIEW sites
  (anti-leakage hazard); may be "integration" more than a sharp repricing — verify a
  real price/packaging change with at-cutoff uncertainty occurred.
- **C2 · ClinicSense / Fullscript (2022).** Massage/wellness-clinic
  practice-management; post-acquisition repricing of a low-cost base under a larger
  health-commerce parent. Cutoff ~2022 (`NEEDS_VERIFICATION`). Strong obscurity.
  Risks: outcome diffuse + review-sourced; at-cutoff uncertainty unverified; pre/post
  pricing not pinned.

### Flagged / dropped (deeper pass)
- **C3 · Ekos / Next Glass (Oct 2025), craft-beverage SaaS** — strong obscurity +
  clean non-review press, but the 2-yr freeze outcome has NOT resolved and is
  post-cutoff → fails "outcome publicly known" *as a backtest*. Retained only as the
  forward-test seed above.
- **C4 · Breeze ChMS / Tithely (2021→2025), church management** — CONFLICTING public
  outcome claims → serious anti-leakage / zero-spoiler hazard. Recall-adjacent.
- **C5 · Ham Radio Deluxe** — too-famous-within-niche (recalled pre-search =
  memorization hazard) + borderline out-of-domain. Excluded.

### Family-B B2B-vertical gap (explicit)
No clean, fully-eligible B2B-vertical competitor-displacement case surfaced (obscure
+ clean non-review departure signal + discrete response decision + at-cutoff
uncertainty + resolved outcome). The "clean non-review signal" bar tends to pull
toward famous (Unity, GitHub) or consumer cases. Real gap, not lack of effort — a
dedicated Family-B dig into niche-vendor changelogs / integration-marketplace
"import from &lt;competitor&gt;" launches would be the next attempt.

## Selection PROPOSAL (owner-confirmable; not a selection)

Per the crux test (one repricing + one clean-substrate displacement):
- **Repricing → A1 Inoreader** (clear strongest).
- **Displacement → B1 Craft/ExpressionEngine** (sharpest decision); **B2 Buttondown** as the swap-in if you prefer cleaner dating / a more recent case.

Frame-locks for the proposed two are below; swap by saying so.

---
## ═══════ SEALED — FACILITATOR ONLY (outcomes; do not read if blind-judging) ═══════

**Sealed outcome notes (existence + rough direction; not interpreted):**
- A1 Inoreader: founder publicly walked back a power-user limit; company remained operational (2019→ongoing).
- A2 Supernotes: lifetime plan discontinued, replaced by a 4-year license (~2021; successor announced Dec 2023).
- B1 Craft/EE: P&T built the rival (Craft CMS launched 2013) and later divested its EE plugins.
- B2 Buttondown: a "Dear TinyLetter Users" migration post exists (~2023-2024); Buttondown continued operating.
- C1 Genesis/ClinicMind: continued G2 "Leader/Momentum" awards through 2025; scattered review mentions of cost; no crisp resolution event. Direction not assessed.
- C2 ClinicSense/Fullscript: review aggregators note "recent price increases" as a drawback. Direction not assessed.
- C4 Breeze/Tithely: third-party sources claim later all-access ~$119/mo vs prior ~$60-80; vendor disputes any increase — conflicting, not adjudicated.

**Proposed frame-locks (facilitator-side; cutoffs `NEEDS_VERIFICATION`, evidence/outcome `NEEDS_CAPTURE`):**

### FL-A1 · Inoreader repricing
- decision_family: pricing / repricing / packaging
- decision_owner_context: Founder/CEO, Innologica (bootstrapped RSS-reader co)
- decision_question: at cutoff, how aggressively to gate power-user functionality (Rules limits) into paid tiers when repackaging — watch / hold / narrow / phase / commit
- cutoff_window: ~Jan 2019 (`NEEDS_VERIFICATION`)
- decide_vs_confirm_hypothesis: does clean public signal at cutoff (competitor RSS-reader pricing/packaging + public power-user sentiment) DECIDE the gating calibration, or only CONFIRM it after the reaction? AR-S2: decision-grade for a first-time aggressive gating, or needs an observable iteration?
- anti_cherry_pick: drawn from a pre-declared obscure-repricing discovery lane
- post_window_exclusion: exclude the founder's public walk-back and all post-cutoff pricing evolutions / user reaction from at-cutoff reasoning
- risks: outcome partly self-reported (founder blog); thin/tangled sourcing → zero-spoiler fencing required; obscurity heuristic, not contestant-recall-certified

### FL-B1 · Craft CMS / Pixel & Tonic vs. ExpressionEngine
- decision_family: competitor-displacement (clean non-review substrate)
- decision_owner_context: Founder Brandon Kelly, Pixel & Tonic (EE's leading add-on maker — ecosystem insider)
- decision_question: at cutoff, should P&T respond to EE community discontent + beginning departures by building/backing a competing CMS, or stay loyal to EE — watch / probe / test / hold / build / move
- cutoff_window: ~2012-2013 (`NEEDS_VERIFICATION`)
- decide_vs_confirm_hypothesis: can clean non-review public signal at cutoff (EE community/forum discontent + agency sentiment) DECIDE the build-the-rival move, or only CONFIRM it after the rival's adoption was known?
- anti_cherry_pick: drawn from a pre-declared obscure-displacement discovery lane
- post_window_exclusion: exclude the rival's launch (2013), its adoption, and the EE-plugin divestiture from at-cutoff reasoning
- risks: hindsight-inevitability gloss (must reconstruct genuine 2012-13 uncertainty); some primary-source dating needs Wayback verification; ecosystem-insider not pure outside rival (confirm frame fit); obscurity heuristic, not certified
## ═══════════════════════════ END SEALED ═══════════════════════════

## Non-Claims

Not owner selection, not validation, not buyer proof, not judgment-quality, not
captured evidence, not memorization-certified. Obscurity reads are heuristic. No
case is proven decision-grade until capture verifies cutoff, source depth, and
zero-spoiler feasibility. Authorizes no capture or build. Freezes nothing without
owner sign-off.

## Dependencies / next steps

- **Owner confirms / swaps** the selection proposal (selection is owner-owned).
- On confirm: **capture** (cutoff-disciplined source lane, gated) builds the clean
  pre-cutoff packet and seals the outcome → fills the case-frame template's
  `NEEDS_CAPTURE` slots.
- **B2B-vertical deeper pass** (in progress) folds into the universe on completion.
- Register selected real cases in `manifest_v0.md` when authored.
