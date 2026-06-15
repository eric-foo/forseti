# Judgment-Spine C2 Rule 3 (Risk-State Weighting) — Phase A Classification Finding (PROPOSED)

```yaml
retrieval_header_version: 1
artifact_role: >
  Phase-A classification finding (advisory; product_learning tier) — answers
  whether a C2 risk-state/weighting "Rule 3" already exists in the live C2
  read-contract lane, classifies the stale-frame sender Rule 3 as net-new /
  patch / duplicate, and recommends the fold direction under main's two-axis
  demand-state model. Decision input for owner sign-off; performs no fold.
scope: >
  Re-grounds the C2 risk-state weighting work (sender artifact authored on the
  retired durable-vs-hollow frame) onto main's settled two-axis model. Phase A
  only: classification + evidence + recommended re-mapping direction. Phase B
  (authoring the re-grounded Rule 3 into the live C2 read-contract spec) is
  owner-gated and not performed here.
use_when:
  - Deciding whether/how to fold a C2 risk-state "Rule 3" into the live C2 read-contract.
  - Re-grounding the stale-frame Rule 3 reasoning onto the durable/transient + real/manufactured axes.
authority_boundary: retrieval_only
open_next:
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md                            # main's two-axis demand-state model (the doctrine to re-ground onto)
  - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md             # the live C2 read-contract (rules 1-2 landed; rule 3 OPEN) — ledger-c2-read-contract-v0 lane @ 6a04612e
  - docs/prompts/handoffs/judgment_spine_c2_read_contract_continuation_handoff_v0.md     # the live lane's own Rule-3 Open Decision — same lane
  - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md  # C0-C4 core; C2=Weight; C3=verdict+ceiling — judgment-spine-read-machinery-architecture-v0 lane @ 57339ea5
stale_if:
  - The owner signs off (accept / amend / reject) the classification or the axis mapping — fold the decision in.
  - The ledger-c2-read-contract-v0 lane advances past 6a04612e and writes Rule 3 itself (re-reconcile).
  - Main's two-axis taxonomy is amended or owner-adjudicated (re-derive the mapping against the amended text).
```

## Status

`PROPOSED` — Phase-A classification finding, `product_learning` / design tier.
Authored 2026-06-15 in a fresh worktree off `origin/main` (739411f4), branch
`c2-risk-state-weighting-reground-v0`, picking up the cold handoff
`docs/prompts/handoffs/c2_risk_state_weighting_reground_two_axis_handoff_v0.md`
(itself untracked on the stale `ecr-sp3-timing-deriver-slice1` lane). This finding
**proposes a classification and a re-mapping direction for owner sign-off**; it
folds nothing, edits no live spec, performs no doctrine change, and asserts no
scoring engine, number, or G1/G2 reopening.

## The Phase A Question

Does a C2 risk-state / weighting rule already exist in the **live** C2
read-contract lane on `main`? And is the sender's stale-frame `Rule 3`
(`docs/decisions/orca_c2_risk_state_weighting_v0.md`, on `ecr-sp3`) **net-new**,
a **patch** to existing C2 doctrine, or a **duplicate**?

## Finding (recommendation for owner sign-off)

**Classification: PATCH.** Rule 3 is a net-new *rule* that already has a
designated home **inside the existing C2 read-contract spec** — it is not a
standalone new doc, and it is not a duplicate (not yet written). The sender's
separate decision-record at `docs/decisions/orca_c2_risk_state_weighting_v0.md`
should **not** survive as an independent artifact; its salvageable reasoning
re-maps into the live C2 read-contract spec's open "rule 3" slot, re-grounded onto
main's two-axis model.

This is corroborated from **both** sides:

- **Live-lane side (the authoritative side for the question).** The
  `ledger-c2-read-contract-v0` lane (@ `6a04612e`) has the C2 read-contract spec
  with **Required Behavior items 1–8 landed but Rule 3 explicitly OPEN.** The spec
  itself names "a prospective **rule 3**" and scopes it as "how C2 treats a known
  risk across evidentiary states (present / unconfirmed / absent)"
  (`judgment_spine_c2_ledger_read_contract_v0.md`, lines 60–65); item 8 already
  seeds the cap/discount/neutral classification as an ambiguity-handling rule
  (lines 116–119). The lane's own continuation handoff makes the home explicit:
  *"author rule 3 into the spec `judgment_spine_c2_ledger_read_contract_v0.md`
  … matching the rules 1-2 style"*
  (`judgment_spine_c2_read_contract_continuation_handoff_v0.md`, Exact Next
  Authorized Action #2; Open Decision block defines the same present→cap /
  unconfirmed→discount / absent→neutral chain and routes it "to a dedicated
  Claude thread … Owner will return with the decision").
- **Sender side.** The sender doc (sha256 `D506CDC2…`, verified) is literally
  titled *"Orca C2 Read-Contract — Rule 3: Risk-State Weighting"* and its own
  `use_when` / `ripple_surfaces` say *"Folding Rule 3 into the live C2
  read-contract … is the doctrine-change step."* So the sender artifact **is the
  output of the live lane's spawned Rule-3 thread**, always intended to be folded
  back — not an independent decision.

**Why not net-new (standalone):** Rule 3 has a named home and an open slot in the
existing contract; a fresh standalone decision-record would fork live doctrine.
**Why not duplicate:** Rule 3 is not yet written into the live spec (items 1–2 /
7–8 landed; the lane's commit log and handoff both record "rule 3 … open"), so the
salvaged reasoning is the missing piece, not redundant.

## The substantive correction (why a re-ground is warranted, not a transcribe)

The sender's Rule 3 was authored on the **retired durable-vs-hollow frame**
(`ecr-sp3` predates PR #78 / `c36e09c2`, verified: `c36e09c2` is an ancestor of
`origin/main` but **not** of `ecr-sp3`). Its §3(a) lists **five** mechanism
classes all as "confirmed present → DEFEATER (cap)":

| Sender §3(a) mechanism class | Two-axis re-mapping | Caps the read? |
| --- | --- | --- |
| Fabrication / coordination / astroturf (bots, fake accounts, review-stuffing, laundered origination, staged costly-behavior) | **MANUFACTURED (integrity) axis** — demand is not *real* | **Yes — dispositive cap** (defeater) |
| Non-use demand (resale / collectible / speculative flip) | **PERSISTENCE axis** — real demand, short/zero end-use lifespan | **No — transient verdict** |
| Transient / event-driven one-time spike | **PERSISTENCE axis** | **No — transient verdict** |
| Distress / scarcity / panic buying | **PERSISTENCE axis** | **No — transient verdict** |
| Channel demand (sell-in ≠ sell-through) | **JUDGMENT CALL** — integrity-artifact (placement w/o pull) vs transient/timing | **Owner-set** |

On `main`'s model the retired "hollow" conflation is exactly this: it merged
*manufactured* (fake/amplified → discount/avoid) with *transient* (real demand
that decays → still valuable, act in-window). The sender's §3(a) reproduces that
conflation by capping all five classes. Per the two-axis taxonomy
(`orca_demand_read_taxonomy_v0.md`) and the read-machinery architecture
(C0–C4), the correct re-mapping is:

- **Manufactured-axis risks** stay in Rule 3 as **defeaters/caps** at **C2 (Weight)** —
  when confirmed-present, there is no *real* demand to weight. Discriminator
  family: origination de-correlation (does the signal survive outside the
  coordinated cluster?). The live lane already gestures at this: its owner-raised
  refinement names "manufactured demand, which the Demand-Substrate Hard Gate
  rules out" as the **dominant disqualifier**.
- **Persistence-axis patterns** (resale, event, scarcity) are **NOT caps**. They
  **reclassify the demand-state** — real but transient — and route to **C3
  (Verdict + Action Ceiling)**, where the ceiling is matched to the demand's
  lifespan (act in-window; observe persistence; earn the upgrade to durable). The
  sender's persistence discriminator families (use-vs-flip; repeat/persistence;
  persistence-after-normalization; sell-through-vs-sell-in) are **not discarded** —
  they **re-home** from "Rule 3 caps" to C3's durable-vs-transient classification +
  the calling-sequence monitoring.
- **Channel sell-in ≠ sell-through** is the genuine boundary case — flag it as an
  owner judgment call (integrity-artifact vs transient/timing), per the sender
  handoff's second Open Decision.

The sender's **general machinery is sound and axis-agnostic** and is preserved
as-is: §3(b) unconfirmed → ceiling-discount with the reversibility two-band split
(least-recoverable dimension binds; economic/reputational/operational/
evidence-contamination); §3(c) confirmed-absent → neutral baseline, never positive
(anti-gaming, = AR-05); §3(d) discriminator set + sufficiency bar + missing/
inconclusive/impossible triple; §3(e) falsifiability filter + small-N inherent-limit
cap (orthogonal); the FP/FN bounded-asymmetry basis; advisory-not-control; the
mini-god-tier qualitative-now / numeric-v2-hypothesis posture. The cross-vendor
review findings AR-01..06 (accepted; per the sender doc's own Review Provenance and
the inbound handoff) carry forward **re-mapped**, not re-litigated.

## Net effect on Rule 3's shape (the proposed Phase B direction — owner-gated)

Re-grounding **shrinks Rule 3's scope at C2** to manufactured-axis (integrity)
dispositive risks across present/unconfirmed/absent (cap/discount/neutral), keeping
all the general machinery; and **moves the persistence-axis mechanisms out of the
cap** into C3's durable-vs-transient verdict and its horizon-matched action ceiling.
This is the smallest change that satisfies both the live lane's open Rule-3 slot and
main's two-axis model, and it directly discharges the inbound handoff's Drift Guard
("transient is not a cap; the cap belongs to the manufactured axis").

## What the owner is asked to sign off (before Phase B)

1. **Classification = PATCH** (fold into the live C2 read-contract spec; retire the
   standalone `docs/decisions/orca_c2_risk_state_weighting_v0.md` as an independent
   artifact). Alternatives on the table: net-new (rejected — forks live doctrine)
   or duplicate (rejected — Rule 3 unwritten).
2. **Mechanism-class → axis mapping** (the table above): manufactured-axis = C2 cap;
   persistence-axis = C3 transient verdict, not a cap; channel sell-in≠sell-through
   = owner judgment call.
3. **Phase B authorship locus**: Rule 3 is authored into
   `judgment_spine_c2_ledger_read_contract_v0.md` **in the
   `ledger-c2-read-contract-v0` lane** (its open slot), not in this worktree —
   because the live fold is that lane's doctrine-change step (DCP receipt owed at
   that time). This finding lane prepares the design; it does not perform the fold.

## Related-lane observation (flagged, not acted on)

The read-machinery architecture
(`judgment_spine_demand_read_machinery_architecture_v0.md`, lane @ `57339ea5`)
still says **C3 emits "the durable-vs-hollow verdict"** (line 136) — a stale
"hollow" reference post-#78. That is a *second* consumer of the two-axis
re-grounding (the C3 verdict vocabulary), owned by that lane. Noted here as a
cross-lane drift signal; **out of scope** for this lane to edit.

## Scope boundaries / non-claims

- Phase A finding only: classification + evidence + recommended direction. **No
  fold performed**, no live spec edited, no doctrine change executed.
- INV-1 holds: **no scoring engine, no number, no formula** is proposed; Rule 3
  stays a qualitative stated-classification + reason.
- The ratified **G1/G2 / Demand-Substrate Hard Gate** (admissibility) is consumed,
  **not reopened**. The two-axis taxonomy is consumed, not re-litigated.
- Not validation, readiness, buyer proof, or judgment-quality evidence; closeout
  state for any such claim: `no_durable_evidence`.
- The two-axis taxonomy artifact itself remains
  `PROPOSED_PENDING_OWNER_ADJUDICATION`; the two-axis *vocabulary* is on `main`
  (#78) and is the current read grammar this finding re-grounds onto.

## Source-Read Ledger

- `origin/main:docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — the
  two-axis demand-state model (durable/transient + real/manufactured; "hollow"
  retired). Read fresh on `origin/main` (739411f4) 2026-06-15. Status:
  PROPOSED_PENDING_OWNER_ADJUDICATION; two-axis amendment landed via #78
  (`c36e09c2`, verified ancestor of `origin/main`; NOT of `ecr-sp3`).
  Load-bearing: yes.
- `judgment_spine_c2_ledger_read_contract_v0.md` — live C2 read-contract; Required
  Behavior 1–8 landed, Rule 3 OPEN (lines 60–65, 116–119). Lane
  `ledger-c2-read-contract-v0`, worktree `orca-ledger-c2-read-contract-wt` @
  `6a04612e`; read fresh 2026-06-15. Branch-only (not on `origin/main`).
  Load-bearing: yes.
- `judgment_spine_c2_read_contract_continuation_handoff_v0.md` — the live lane's
  own Rule-3 Open Decision + "author rule 3 into the spec" directive. Same lane @
  `6a04612e`; read fresh 2026-06-15. Load-bearing: yes.
- `judgment_spine_demand_read_machinery_architecture_v0.md` — C0–C4 core (C1=gate,
  C2=Weight/checkpoint-3, C3=Verdict+Ceiling); C3 carries a stale "durable-vs-hollow"
  reference. Lane `judgment-spine-read-machinery-architecture-v0`, worktree
  `orca-judgment-read-machinery-wt` @ `57339ea5`; read fresh 2026-06-15.
  Load-bearing: yes (orientation for C2/C3 placement).
- `docs/decisions/orca_c2_risk_state_weighting_v0.md` — sender Rule 3 (stale frame;
  §3(a) conflates the axes). On `ecr-sp3-timing-deriver-slice1` @ `0fc58cfe`,
  UNTRACKED; read by absolute path 2026-06-15; sha256 `D506CDC2…` **verified**.
  Role: INPUT reasoning to salvage/re-map, NOT authority.
- `docs/review-outputs/adversarial-artifact-reviews/orca_c2_risk_state_weighting_adversarial_artifact_review_v0.md`
  — cross-vendor AR-01..06 (accepted). Sender artifact on `ecr-sp3`, UNTRACKED;
  packet sha256 `76C5D203…`. **Available, not independently re-read**; findings
  carried from the inbound handoff's inline summary + the sender doc's Review
  Provenance section. Role: salvage input.

```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
