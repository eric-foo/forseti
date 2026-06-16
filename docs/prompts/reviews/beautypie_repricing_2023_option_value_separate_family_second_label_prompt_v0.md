# Beauty Pie Repricing 2023 — `option_value` Separate-Family Second-Label — Courier Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (independent separate-family second-label of one band input)
scope: Commission an outcome-blind, separate-vendor second-label of the `option_value` band input for case beautypie_repricing_2023_v0, to resolve a contested label before ledger freeze.
use_when:
  - Couriering the option_value second-label to a separate-model-family labeler.
authority_boundary: retrieval_only
branch_or_commit: aec13c3
input_hashes:
  participant_packet_baseline.md: 912cc2843fa643cbffcdd0e77b258354c05ea0c6
stale_if:
  - The baseline packet blob above changes (re-pin and re-issue).
  - The v0_14 band_input_labeling_rubric option_value definition changes.
```

## Orca Start Preflight (prompt author)

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (S0 overlay + Judgment-Spine evidence-ladder subset + baseline packet + v0_14 band_input_labeling_rubric option_value section + facilitator_ledger band-input context)
  edit_permission: docs-write (this prompt artifact only; the labeler is read-only and never edits the ledger)
  target_scope: docs/prompts/reviews/ (courier prompt); label target = the option_value band input for beautypie_repricing_2023_v0
  dirty_state_checked: yes (branch ecr-sp3-timing-deriver-slice1, HEAD aec13c3; baseline packet + ledger tracked/clean at HEAD; this prompt file is new/untracked)
  blocked_if_missing: none (decision brief + rubric definition inlined below; self-contained for a repo-blind labeler)
  doctrine_change: none (courier prompt; no doctrine change)
```

---

## Commission

You are commissioned to produce **one independent, outcome-blind second-label** of a single decision-quality band input — **`option_value`** — for the Beauty Pie membership-repricing case. The primary label was set by the Claude home lane; the value is contested. Your independent assessment resolves the contest as **decision input** for the owner, who makes the final freeze call. **You do not edit any file.**

- **Author of the primary label:** Claude (Anthropic).
- **De-correlation who-constraint:** **separate vendor / model lineage from Anthropic/Claude** (cross-vendor discovery bar). This is a commission who-constraint for de-correlation, **not** a runtime-model recommendation. If you are an Anthropic/Claude-lineage model, **stop and return `BLOCKED_DE_CORRELATION`** — a same-vendor label does not de-correlate the contest.
- **Independence is the whole point.** You are deliberately **not** shown the primary label, any contested alternative, any rationale already on file, or any facilitator-only case analysis. Do not ask for them, and do not try to guess what they were. Label from the decision brief and the rubric alone.

## Outcome-blind constraint (load-bearing)

This is a real backtest case about a real company at a **2023-02-28 cutoff**. You must label as if you were deciding **before** any market response was observable.

- **Do NOT** look up, recall, or use any knowledge of Beauty Pie's actual post-cutoff outcome (what they actually did, member reaction, later pricing, results, headcount, funding, anything after the cutoff).
- **Do NOT** access the web or any repo file beyond this prompt.
- If you happen to already know the real outcome, **set it aside** and label strictly on the brief below. If you cannot do that honestly, return `BLOCKED_NOT_OUTCOME_BLIND`.

A second-label contaminated by outcome knowledge is worse than none — it silently re-introduces hindsight into a fixture whose entire value is that it was built outcome-blind.

## The task

Assign exactly one value of the `option_value` band input — **`none` | `low` | `moderate` | `high`** — for this decision, grounded only in the decision brief and the rubric's `include_if` criteria.

### The band input you are labeling — `option_value` (v0_14 rubric, verbatim)

```yaml
option_value:
  values:
    none:
      include_if: action does not preserve or create meaningful future option value
    low:
      include_if: action creates minor optionality
    moderate:
      include_if: action creates a useful future choice or learning path
    high:
      include_if: action creates major option value with bounded downside
```

Rubric context (factual, do not let it steer the label): `option_value` is one of several "action-floor" inputs in the v0_14 mapping table — a higher band raises the minimum-caution action floor. Label on the `include_if` criteria and the evidence, **not** to target any floor. Note the `high` bar has two parts: **major option value AND bounded downside** — weigh both.

### What "the action" is here

The decision is **how aggressively to restructure Beauty Pie's membership pricing** — specifically whether to eliminate the £5/mo entry tier (doubling those members to £10/mo) and scrap the monthly spending limits, across the option span: watch / hold / soften / phase-or-grandfather / commit to the full elimination-and-doubling. Assess the `option_value` of *acting* (the repricing move) on the rubric scale: does the move preserve/create meaningful future optionality, and with what downside boundedness?

## Method

Frame before you label. **If you are a skill-equipped Orca reviewer:** apply `workflow-deep-thinking` discipline first (frame what option value means for this specific decision, the failure modes of over- and under-labeling it, and where the band boundary sits), then assign. **If you are a separate-vendor / repo-blind labeler:** do the same reasoning self-contained — no Orca skills needed. Either way:

1. Read the decision brief (Appendix, the baseline packet — the core decision evidence; the experimental org-motion arm is intentionally excluded because the band input is a property of the core decision, not the experiment).
2. Reason explicitly about each rubric band's `include_if` against the evidence, especially the boundary between `moderate` ("useful future choice or learning path") and `high` ("major option value **with bounded downside**").
3. Pick the single best-fitting band. State the key uncertainty that could move it.

Be adversarial about your own first instinct: if you lean `high`, test whether the downside is genuinely *bounded* (the rubric requires it); if you lean `moderate`, test whether you are underweighting foreclosed future choices. Do not soften the call to hedge.

## Output / return contract

Output mode: **paste-ready return** (you write nothing to the repo). Return this block, then prose reasoning. The home CA records your assessment into the facilitator ledger's `second_label_diffs` and provenance; the **owner** makes the final freeze decision.

```yaml
option_value_second_label:
  band_input: option_value
  assessment:                # none | low | moderate | high  (your independent call)
  rubric_version: v0_14
  labeled_from: participant_packet_baseline.md @ aec13c3 (blob 912cc28)
  outcome_blind: yes
  blind_to_primary_label: yes
  reviewed_by:               # your model+version, e.g. gpt-5.5 — the CA records this; never fabricate
  authored_by: claude        # the primary-label lane
  de_correlation_bar: cross_vendor_discovery
  rationale: >-              # grounded ONLY in the packet evidence + the rubric include_if criteria
  key_uncertainty: >-        # the single thing most likely to move the band
```

Then give your reasoning in prose: how the evidence maps to the chosen band's `include_if`, why the adjacent bands fit worse, and the downside-boundedness judgment for the `high` test.

## Hard constraints / non-claims

- You label; you do not edit the ledger, the packets, or any file. Recording and freezing are owner/CA actions.
- Outcome-blind and independence constraints above are mandatory; violate either → return the matching blocker (`BLOCKED_NOT_OUTCOME_BLIND`, `BLOCKED_DE_CORRELATION`) instead of a label.
- Your assessment is **decision input only** — not approval, validation, fixture admission, or freeze authority. The case is product-learning tier, N=1.
- Do not request the sealed outcome, the primary/contested labels, or the facilitator analysis; reason from the brief and rubric alone.

---

## Appendix — Decision brief (baseline packet, verbatim)

> Exact file at blob `912cc2843fa643cbffcdd0e77b258354c05ea0c6` @ `aec13c3`. This is the core decision evidence. (The augmented arm adds an experimental hiring-intent signal that is not a band input and is intentionally not shown here.)

````markdown
---
case_id: beautypie_repricing_2023_v0
decision_question: At the cutoff, how aggressively should Beauty Pie restructure its membership pricing — specifically whether to eliminate the £5/mo entry tier (moving those members to £10/mo, a doubling for them) and scrap the monthly spending limits — watch, hold, soften, phase/grandfather, or commit to the full elimination-and-doubling?
decision_date_or_cutoff: 2023-02-28
role_frame: Founder/CEO and commercial leadership of Beauty Pie, a UK factory-direct membership beauty brand, deciding how aggressively to restructure membership pricing on pre-cutoff public evidence only.
authority_constraints: Full founder-led pricing and membership-structure authority; the binding constraint is reversibility and member trust, not authority.
capability_constraints: Can ship any membership/pricing structure immediately; decides on pre-cutoff evidence, before any market response to the decision is observable.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2023-02-28).
  - Distinguish a pre-existing base rate from a reaction to this specific move.
  - Treat the prices, tiers, and monthly spending limits in the evidence as real.
  - Judge only on this packet; produce a single blind judgement from it alone.
information_boundary: Decide using only the evidence in this packet. Do not use, recall, or look up any outside or later knowledge about this company or this decision; base the judgement solely on the packet.
source_manifest:
  - source_id: E1
    source: 'Beauty Pie membership model — factory-direct; members pay a membership fee to buy products at cost (public brand/product description, pre-cutoff)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E2
    source: 'Beauty Pie membership structure at cutoff — £5/mo and £10/mo monthly tiers plus a £59/yr "Beauty Pie Plus" annual (2021 relaunch), each with monthly spending limits (public pricing, pre-cutoff)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E3
    source: 'UK cost-of-living / elevated-inflation context, early 2023 (neutral macro context bearing on discretionary spend)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E4
    source: 'General base rate — eliminating an entry tier / raising the floor price is a recognized retention-risk repricing lever (general base rate)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
  - source_id: E5
    source: 'Generic comparable consumer-subscription repricings exist across the market (general base rate)'
    retrieval_timestamp: <<pending-phase4-capture>>
    hash: <<pending-phase4-capture>>
---

# Participant Packet

## Decision Context

Beauty Pie is weighing a membership repricing. The live question, before any decision is announced, is **how aggressively to restructure its membership pricing** — specifically whether to **eliminate the £5/mo entry tier** (moving those members to £10/mo, a doubling for them) and **scrap the monthly spending limits**. The £5/mo tier is the lowest-commitment way into the membership, and the spending limits are part of the current structure. The packet is intentionally narrow: it presents only what was knowable on or before the cutoff (28 February 2023); decide using only the information in this brief. The options span watch / hold / soften / phase-or-grandfather / commit-to-the-full-elimination-and-doubling.

## Evidence Units

- `E1`: Beauty Pie's **membership business model** — factory-direct; members pay a membership fee to buy beauty products at cost. The membership fee is the revenue gate, and the cheapest tier is the low-commitment on-ramp into the model.
- `E2`: Beauty Pie's **membership structure at the cutoff** — two monthly tiers, £5/mo and £10/mo, plus a £59/yr annual "Beauty Pie Plus" (introduced in a 2021 relaunch), each carrying monthly spending limits. The £5/mo tier is the lowest-commitment entry point.
- `E3`: **UK cost-of-living pressure in early 2023** — elevated inflation and squeezed discretionary household spend — a neutral macro context bearing on price sensitivity for discretionary beauty.
- `E4`: Eliminating an entry tier or raising the floor price is a **recognized retention-risk repricing lever** in subscription/membership businesses — a documented general base rate.
- `E5`: **Comparable consumer-subscription repricings** exist across the market — a generic base rate.

## Known Uncertainties

- The evidence shows entry-tier removal and floor-price increases are a normal repricing lever **and** that raising the floor on the most price-sensitive members during a cost-of-living squeeze carries retention risk; it does not settle how far is too far.
- There is no pre-cutoff measurement of *Beauty Pie's own* members' tolerance for the doubling, or for scrapping the monthly spending limits specifically.
- Whether the second-order base rate (E3, E4, E5) is enough to *decide* the calibration in advance — versus only being legible in hindsight — is the crux of this decision.
````
