# Orca C2 Read-Contract — Rule 3: Risk-State Weighting (PROPOSED v0)

```yaml
retrieval_header_version: 1
artifact_role: >
  Decision record (PROPOSED) — C2 read-contract Rule 3: how the demand-read
  judge's weighting step treats a known dispositive failure-mode across its
  evidentiary states. product_learning tier; qualitative; INV-1-safe; advisory
  ceiling only. Cross-vendor adversarially reviewed + patched; not yet folded
  into the live C2 contract.
scope: >
  The qualitative convention for how C2 (the core's weighting step) weights a
  known dispositive risk across present / unconfirmed / absent, plus the
  inherent-limit (small-N) case. Mini-god-tier shape: qualitative now, numeric
  v2 gated on a calibration spine + lifting INV-1.
use_when:
  - Defining or reviewing how C2 weights a known risk by its evidence state.
  - Folding Rule 3 into the live C2 read-contract (read-machinery lane; owner-gated).
authority_boundary: retrieval_only
status: PROPOSED_OWNER_ACCEPTED_IN_THREAD_2026-06-15_CROSS_VENDOR_REVIEWED_PATCHED_NOT_LIVE
authored_by: claude-opus-4.8
reviewed_by: unrecorded  # operator-run cross_vendor (non-Claude family per commission); exact model+version not supplied — never fabricated
de_correlation_bar: cross_vendor
derived_from:
  - cross-model blind weighting probe (Claude / GPT / Qwen / Grok) — residual-disagreement localization
  - in-thread deliberation with owner, 2026-06-15
review_report: docs/review-outputs/adversarial-artifact-reviews/orca_c2_risk_state_weighting_adversarial_artifact_review_v0.md
consumes_does_not_reopen:
  - docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md  # G1/G2 ratified gate (admissibility front-door)
ripple_surfaces:
  - docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md  # the C2 read-contract home; folding-in is the doctrine-change step (DCP owed at that time)
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md                                # the MGT lens this rule adopts
open_next:
  - docs/prompts/handoffs/judgment_spine_read_machinery_architecture_handoff_v0.md
```

## Purpose

Settle how C2 — the demand-read judge's weighting step — treats a known
**dispositive** failure-mode (one that, *if active, defeats the "durable demand"
reading*) across the three states in which evidence can leave it, plus the
inherent-limit case. This is the hype-resistance core of the judge: the rule that
decides whether hollow demand can ever be read as durable, and how strongly the
judge advises against acting on an unproven risk.

## Framing principles (inherited by every clause)

- **Trust ceiling, not a score.** C2 outputs a qualitative ceiling on how durable
  a signal may be read, never a number. INV-1: no scoring engine, no formula.
- **Advisory, not control.** The judge **withholds or grants a verdict and a
  recommended action-ceiling; it never prohibits the owner's action.** "Cap,"
  "near-cap," and "withhold" describe what the judge will *certify*, not what the
  owner may *do*. The owner may always override with eyes open; the rule's job is
  to make an override a conscious, named bet rather than a silent default.
- **Scope = dispositive risks only, defined by property.** Rule 3 governs risks
  that, if active, **defeat durable end-use demand** — *whether by fabrication or
  by a non-fabrication mechanism* (mechanism classes in 3(a)). Magnitude-only
  factors (a still-durable signal that is merely smaller or softer) are ordinary
  markdowns elsewhere in C2 — not Rule-3 risk-states.
- **Monotone chain.** On the trust ceiling, **cap ≤ discount ≤ neutral**
  (present ≤ unconfirmed ≤ absent). Inherent-limit caps sit orthogonal; the
  binding ceiling is the lowest that applies.

## The rule

### 3(a) — Confirmed present → DEFEATER (cap)

Evidence the risk is active **caps the read**: the judge withholds the "durable"
verdict on this dimension and strongly advises against relying on it as durable,
regardless of positive evidence elsewhere. (Mirrors the G1 defeater — a
manufactured costly-behavior instance defeats the floor, it does not merely lower
the ceiling.)

*Why it fully caps:* for a dispositive risk, confirmed-active means the apparent
demand **is not durable end-use demand**, so there is no honest "durable" left to
grant. A dispositive risk belongs to one of several **mechanism classes**, each
with its own discriminator family (3(d)) — fabrication is one class, not the only
one:

- **Fabrication / coordination (astroturfing)** — the signal is manufactured:
  coordinated buzz, bot / fake-account inflation, creators running the **same
  talking points**, one origination laundered to look like many independent
  sources, or a costly-behavior instance staged inside that coordinated layer.
  Family: **origination de-correlation** (does the signal — including any
  costly-behavior instance — survive *outside* the coordinated cluster, or only
  inside it?). Fabricated costly-behavior is caught here by de-correlation, not by
  transaction forensics (rarely OSINT-visible).
- **Non-use demand (resale / collectible / speculative flip)** — real money, but
  buyers are not end-users; demand evaporates when the flip trade does. Family:
  **use-vs-flip** (resale-premium / hold-to-flip signatures vs replenishment /
  consumption).
- **Channel demand, not consumer demand (sell-in ≠ sell-through)** — retailers
  stocked it; consumers have not pulled it through. Family:
  **sell-through-vs-sell-in** (is there consumer-side pull, or only wholesale
  placement?).
- **Transient / event-driven** — a one-time spike (trend, event, scandal
  attention) with no repeat. Family: **repeat / persistence** (does demand survive
  past the triggering window?).
- **Distress / scarcity buying** — stockpiling driven by shortage fear, not durable
  preference. Family: **persistence-after-normalization** (does demand hold once
  supply / scarcity normalizes?).

"Confirmed present" means the discriminator set's **sufficiency bar** (3(d)) is
met — the named pattern that constitutes *established* present, not mere suspicion
and not a confession. Where a risk has no discriminator set with a stated
sufficiency bar, the cap is not reachable; the case sits in 3(b) unconfirmed.

**Not a confirmed-present archetype — "sells only at a discount."** Demand that
currently appears only at a non-durable price is **not** a default cap: exposure
via discount can genuinely shift taste and build real full-price willingness-to-pay
(sampling → preference). This is the **promo-WTP risk**, handled as an *unconfirmed*
case (3(b)) whose clearing-check is a **full-price window** (family: full-price
costly-behavior durability); it becomes a 3(a) cap **only** once demand is observed
to *collapse* at full price. Treating "currently discount-only" as dispositive up
front would wrongly penalize a legitimate acquisition funnel.

### 3(b) — Unconfirmed-but-possible → CEILING DISCOUNT, two bands on reversibility

A known failure-mode with no evidence either way takes a markdown strictly
between (a) and (c). **Two bands, and the boundary is whether the committed
portion of the action is recoverable before its cost sinks — not the action's
verb name:**

- *Recoverable* (watchlist, small test, returnable / consignment order, a pilot
  you can still halt) → **mild** discount; proceed.
- *Not recoverable* (non-cancellable inventory, a public thesis, capital you
  cannot claw back) → **near-cap**: the judge withholds a durable-grade license
  for the irreversible move and **strongly advises the recoverable path until the
  risk is checked.** It does not forbid; the owner may override knowingly.
- A staged action (phase / narrow) is in the recoverable band **only while the
  stage is genuinely abortable before lock-in.**

**Recoverability is multi-dimensional, and the least-recoverable dimension binds.**
"Recoverable" means recoverable across **economic, reputational, operational, and
evidence-contamination** lock-in. An action is in the *recoverable* band only if it
is recoverable on **all** of these; if **any** dimension is sunk, it is in the
material band. This blocks gaming by slicing the action so that only the
economically-recoverable part is named. *Evidence-contamination* is explicit: a
"small test" that *manufactures* the very signal you are trying to read (e.g., your
own promotion creates the demand you would then measure) is **material**, not
reversible — it corrupts the evidence.

*Why:* collapsing this into neutral equates "didn't check" with "checked and
clear" and kills the verify incentive; a flat cap makes the ceiling un-clearable
and the judge can never certify. Keying the band to reversibility puts the
residual judgment on the action's economics — which the owner knows — not on the
risk's probability, which was the entire locus of cross-model disagreement.

### 3(c) — Confirmed absent → FLOOR-CLEARED / NEUTRAL, never positive

Evidence the risk is not active removes the markdown and returns the signal to the
**risk-absent baseline** — the level a signal sits at when this risk does not
apply. A *verified-clean* signal (checked, absent) and a *risk-not-applicable*
signal both sit at this baseline; both rank **above** an *unverified* signal, which
bears the 3(b) discount. Verified-clean earns **no positive credit over
risk-not-applicable** — clearing a risk is a gate passed, not credit banked.

*Why:* the no-bonus-over-baseline is deliberate, not an oversight. Positive credit
would let audit-clearing substitute for demand strength, would incoherently rank
"had-it-and-cleared-it" above "never-had-it," and would invite manufacture-then-clear
gaming. The "verified beats unverified" intuition is already delivered — by
verified-clean *not bearing* the discount that unverified carries.

### 3(d) — Discriminator companion (required) + sufficiency bar + unlock rule

Every dispositive risk this rule governs must have a **discriminator set**: a
*present-fingerprint* (the pattern that classifies it present → cap) and an
*absent-clearing-check* (the cheap test that classifies it absent → neutral). Each
set must state its **sufficiency bar** — the named conjunction that constitutes
*established* present (e.g. *synchronized timing AND shared talking points AND no
survival outside the coordinated cluster*) — so that "confirmed present" (3(a)) is
a stated standard, not a reader's hunch.

- **Core owns** the *requirement*, the *shape*, the per-class discriminator
  *families* (origination de-correlation; use-vs-flip; sell-through-vs-sell-in;
  repeat / persistence; persistence-after-normalization; full-price durability),
  and the rule that each set must carry a sufficiency bar.
- **The vertical satellite / deck owns** the vertical-specific tells and the
  specific conjunction that fills each sufficiency bar, grown from backtested cases
  under the survival kernel — not promoted into core.

**Discriminator status — three distinct states with distinct ceiling consequences:**

- **Set exists and was run:** fingerprint met → present (cap); clearing-check met →
  absent (neutral); **neither conclusively → inconclusive →** near-cap holds, the
  owner decides whether to make the irreversible bet (this happens often, and is
  fine).
- **Missing-but-buildable** (the risk is checkable in principle, but no set exists
  yet): the judge withholds a durable-grade green-light for a material move and
  advises the recoverable path; the owner may override knowingly; the resolution is
  to **build the set** (a deck task). This is the thin-deck conservatism, made
  explicit — not a permanent block.
- **Impossible** (no clearing-check could ever exist, even with more data / work):
  routed to 3(e) — it is **not** allowed to block as "unconfirmed."

*The separator that keeps "missing" from laundering an unfalsifiable risk:* **"Can
you name a clearing-check that more data or work would make runnable?"** Yes →
missing-but-buildable. No → impossible (3(e)).

**Unlock rule:** a material / irreversible action on an unconfirmed risk earns the
judge's durable-grade green-light only by **running** the discriminator — clearing
it (→ neutral, proceed) or, if it fires, capping (→ advise against). A default
discount never earns a material green-light; absent a run (or absent a set), the
judge withholds it and advises the recoverable path (the owner may still override).

*Why:* this is what stops "unconfirmed" becoming a blanket fallback — a material
green-light is earned by checking, not by sitting in a default markdown.

### 3(e) — Falsifiability filter + inherent-limit caps

A purported dispositive risk **only counts** if it can have a clearing-check (the
nameability test in 3(d)). **No possible clearing-check → it does not block** via
the present / unconfirmed / absent machinery. It is either:

- a **standing inherent-limit cap** — orthogonal to (a)–(c), *not* clearable by
  verification, binding whenever it is the lower ceiling (archetype: small-N / a
  thin or non-replicable evidence base); or
- discarded as noise.

*Why:* without this, an unfalsifiable "what if it's fake in some unprovable way"
permanently caps everything and weaponizes the unlock gate into paralysis. The
discriminator requirement (3(d)) doubles as the anti-over-restraint filter.

## False-positive / false-negative basis (buyer-facing)

C2 advises more strongly against a suspected-but-unproven dispositive risk the
more *irreversible* the action it would authorize, because the two errors are not
symmetric. A false "durable" is acted on irreversibly (sunk cost) **and** damages
a valued, slow-to-rebuild trust attribute; a false "not-yet" is conservative and
reversible by later evidence. The asymmetry is **bounded** — a judge that never
certifies is inert — so at low, reversible stakes the discount is mild and signals
clear cheaply; it hardens toward a cap only as the bet becomes un-undoable, where a
false "durable" cannot be retracted. Verification is the unlock.

## Status, limits, and v2 path (mini god tier)

This is the **mini-god-tier** shape for hype resistance: most of the
durable-vs-hollow discriminating value, with no scoring-engine infrastructure.
Consciously-accepted limitations (named, per the MGT doctrine — not quietly
dropped):

- qualitative bands, **no probabilities** ("durable" is a band, never "73%");
- **LLM-in-session** execution — reproducibility rests on this frame's tightness,
  not a deterministic engine; some residual variance remains;
- **thin-deck early conservatism** — before the discriminator sets are built, the
  judge withholds durable-grade green-lights on many material moves. The post-review
  patches (more mechanism classes, a sufficiency bar per set, an honest
  missing-discriminator state) **compound** this: a more correct rule holds the
  owner back *more* early, until the deck is built. Accepted, and named.
- **manual, case-by-case** lesson install (diagnose → prove → generalize →
  install); no automated retraining;
- coverage bounded to **dispositive, checkable** risks;
- forward-capture **cold-start** — some durability dimensions are unreadable until
  a tracking window passes.

**v2 path (intended migration hypothesis, not a guaranteed structure-preserving
upgrade):** numeric calibration of these bands and tells graduates **only when** a
data-science / calibration spine exists **and** the owner explicitly lifts INV-1.
The *aim* is to calibrate the same structure, but a numeric v2 may need to
**decompose** the currently-bundled bands into separate variables (likelihood,
evidence-quality, severity, action-lock-in). Forward-compatibility is the design
target, not a proven property.

## Honest residuals

- The discriminator check can come back **inconclusive** (fairly often). When it
  does, the near-cap stands and the **owner** decides whether to make the
  irreversible bet anyway. The rule does not pretend this away.
- A third intermediate reversibility band was considered and rejected: deciding
  "which case is in the middle band" reintroduces the exact severity judgment the
  cross-model probe isolated as the whole residual disagreement.

## Review provenance

Cross-vendor adversarial artifact review (reviewer non-Claude family per the
`cross_vendor` commission; author `claude-opus-4.8`). 6 findings — all accepted
(AR-05 in part: wording fixed, the no-bonus decision preserved); AR-01..04 were
fold-blockers, now patched above. Full findings + CA adjudication:
`docs/review-outputs/adversarial-artifact-reviews/orca_c2_risk_state_weighting_adversarial_artifact_review_v0.md`.

## Non-claims

PROPOSED only; owner-accepted in-thread (2026-06-15) **as a proposal**, then
cross-vendor reviewed and patched. Not validated, not ready, not live. Does **not**
reopen the ratified demand gate (G1/G2) — the origination-de-correlation family
*references* the gate's independence logic and must not re-implement it at fold-in.
Asserts no scoring engine and no numeric weighting. Folding Rule 3 into the live C2
read-contract (read-machinery lane) is the doctrine-change step and carries its own
Direction Change Propagation receipt at that time; this record does not perform that
change.
```
