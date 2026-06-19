# Judgment Spine — Backtest Batch 1 Ledger Declaration v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Pre-declared ledger for product-learning backtest batch 1 (beauty /
  personal-care consumer-demand decisions (DecisionEvent): case (Case) list with dev/holdout
  marking, pinned scoring-key version, swap policy and alternates, execution
  rules, all-results reporting commitment, and screen provenance. Caps at
  product-learning; covers by-hand runs only.
use_when:
  - Running, swapping, scoring, or reporting any batch-1 backtest case.
  - Checking what batch 1 may claim and what its results bind.
  - Auditing batch-1 case selection against the anti-cherry-pick rule.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md
  - docs/research/judgment-spine/decide_vs_confirm_backtest_case_frame_template_v0.md
  - orca-harness/cases/product_learning/inoreader_repricing_2019_v0/cross_vendor_blind_run_findings_v0.md
input_hashes:
  orca-harness/scoring/band_scorer.py: D54DCD2CB34A8158232E1A428F70A1F3F182052529D7BC8E5293D5F21A67E1E3
  orca-harness/scoring/mapping_table.py: 8BFD4830A2E3C8FEFEE631B4CE69AF6241BDBDDE585AFAAB09A7791A356AC9E9
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 342f70a (working tree dirty — concurrent lanes; hashes pin worktree bytes)
stale_if:
  - The owner amends the case list, split, panel, or swap pool (amend by dated note, not silent rewrite).
  - An owner-accepted scoring-key change lands (the batch stops; see Key Pin).
  - The batch closes with its distillation record (this ledger becomes historical).
```

## Status

`BATCH1_ACTIVE_OWNER_SIGNED` — a batch-local label, not an evidence-ladder
closeout_state or claim tier. The owner authorized batch 1 and selected the Tier A
case set in-thread (2026-06-11).

Amendment 2026-06-11 (owner sign-off, in-thread): the proposed dev/holdout split
and the proposed default contestant panel were both CONFIRMED unchanged; status
advanced from `BATCH1_DECLARED_PENDING_OWNER_SIGNOFF`. Later changes remain
dated-amendment-only.

## Authorization Basis And Cap

- Owner, in-thread, 2026-06-11: "batch 1 authorized"; Tier A selected ("we'll do
  tier A"); case-family constraint relaxed to any beauty-vertical consumer-demand
  decision (not repricing-only).
- Covers: by-hand contestant runs (fresh chat-surface or sub-agent sessions) plus
  deterministic scoring via `orca-harness/runners/run_case.py`, at
  product-learning tier.
- Does NOT cover: live raw-API provider calls (each needs its own authorization
  record), scoring-key changes, JQ-lane builds (D5 propagation, tooled runner,
  sealed pool), fixture admission, or buyer contact.
- Claim cap: product-learning per
  `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`; the
  chat/manual execution surface is permanently non-gate-clearing per
  `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`.

## Ledger (pre-declared; every result will be reported)

| # | Case | Sector / decision family (DecisionEvent) | Split | Entry basis |
| --- | --- | --- | --- | --- |
| 1 | `inoreader_repricing_2019_v0` | SaaS subscription repricing | dev | RETRO — run 2026-06-10 before this ledger existed; results known; fixture `QUARANTINED` |
| 2 | `feedhaven_repricing_2019_anon_v0` | anonymized variant of #1 | dev | RETRO — same basis |
| 3 | Beauty Pie — £5/month entry-tier elimination, minimum doubled (2023) | beauty subscription repricing | dev | Tier A (screen 2026-06-11) |
| 4 | Topicals — DTC to nationwide Sephora at month 9 (2020–21) | beauty launch/expand (family-transfer probe) | dev | Tier A (screen 2026-06-11) |
| 5 | Lime Crime — prestige price cut + Target/Walmart entry (2022) | beauty repricing / repositioning | holdout (owner-confirmed 2026-06-11) | Tier A (screen 2026-06-11) |
| 6 | REFY — 320-door Sephora rollout at month 7 (2020–21) | beauty launch/expand (family-transfer probe) | holdout (owner-confirmed 2026-06-11) | Tier A (screen 2026-06-11) |

Dev/holdout meaning (batch-local vocabulary): dev cases may inform key/harness
critique and proposed changes; holdout cases are run once under the pinned key
and only reported — no key or harness iteration may condition on them. Cases 1–2
are dev by necessity (their results are already known). The split for cases 3–6
was **owner-confirmed 2026-06-11** (see Status amendment). Harness case IDs for
cases 3–6 are assigned at packet construction.

## Swap Pool (Tier B alternates, preference order within family)

- Repricing family: Ipsy Glam Bag +$1 / Plus +$3 (2021); Birchbox $10 to $13–15
  (2019).
- Launch/demand family: KraveBeauty two-year launch moratorium (2020–22); The
  Ordinary salicylic-acid restock-vs-reformulate (2019–21; brand-fame risk — the
  recognition check decides).

Swap rule: a recognition fail at check time swaps the case for the next same-family
alternate; the swap event is itself recorded as a batch finding; this ledger is
amended by dated note, never silently rewritten.

## Key Pin

The scoring key is frozen for the entire batch as implemented at the
`input_hashes` above (notably `option_value: high` forcing action floor 4 stands
AS-IS — batch 1 measures that rule, it does not change it). An owner-accepted key
change stops the batch; unrun cases roll into a new ledger under the new pin.
Proposed key changes belong only in the closing distillation record.

## Execution Rules

- Contestant runs happen only in fresh isolated sessions (chat surface or
  sub-agent), web search OFF (structural where the surface allows; recorded),
  against zero-spoiler packets.
- The planning thread that authored this ledger is outcome-aware for every ledger
  and swap-pool case; no contestant run may be primed from it.
- A recognition check per case-and-model pair precedes any judgment (isolated
  session; self-report recorded; a fail is a swap signal, not a verdict).
- Default panel (owner-confirmed 2026-06-11): Claude Sonnet-class,
  GPT-5.5, Grok 4, plus Gemini subject to recognition. Per-case recognition
  decides clean vs contaminated arms; contaminated arms are recorded as data, not
  discarded.
- Scoring: `orca-harness/runners/run_case.py` against the pinned key; one
  findings record per case (the Inoreader cross-vendor findings record is the
  exemplar shape).
- All results reported: in-band / over / under, failures, exclusions, swaps,
  quarantines. Selective reporting voids the batch's anti-cherry-pick property.

## Closing Artifact

The batch closes with one distillation record: floor-4 replication verdict within
the repricing family at N>1; recognition-to-call map update; decide-vs-confirm
reads; proposed-not-applied key changes (owner-gated); venues-used provenance.

## Screen Provenance (batch record — NOT a standing source map)

- Screen run 2026-06-11 by two web-research agents (external-signal sourcing per
  the finder frame's self-reference-trap rule); every candidate backed by found
  URLs.
- Venues that produced candidates or evidence: mysubscriptionaddiction.com,
  hellosubscription.com, Mumsnet (style & beauty), Glossy, Beauty Independent,
  Retail Dive, BeautyMatter, Fragrantica, Reddit (r/SkincareAddiction,
  r/MakeupAddiction, r/Glossier), Deciem Chatroom, assorted trade press.
- Rejected negative set (recognition-saturated or screen-failing): Fenty launch;
  Dollar Shave Club; The Ordinary 2020 pricing stunt; Glossier-to-Sephora;
  Glossier 2022 price rise (brand fame); Shea Moisture 2017; Olaplex channel
  saga; Paula's Choice post-PE drift (no clean cutoff); Mielle/P&G (family
  mismatch + community sensitivity); Phlur Missing Person (viral saturation);
  Byredo Baudelaire (thin sources, weak outcome); The Ordinary foundation return
  (outcome too young).
- Boundary: this section is batch provenance only. It does not create a standing
  source map, source inventory, monitor, or crawler (the case-finder frame's
  must-not boundary holds). A durable venue-atlas decision is deferred to the
  next-batch case-quality rubric pass and is owner-owned.

## Owner Direction Recorded (2026-06-11, in-thread)

- Case-family constraint relaxed: any beauty-vertical consumer-demand decision
  (e.g., taste/preference shifts forcing pivot decisions), not repricing-only.
- Tier A approved as the batch-1 new-case set.
- A "preferential qualities for a case" rubric is deferred to the next batch.

## Amendment - Org-Motion Admission, Case #3 (2026-06-11, owner sign-off, in-thread)

The owner authorized, in-thread 2026-06-11, admitting **org-motion evidence**
into **case #3 (Beauty Pie) only**, after a read-only gate-0 feasibility probe.
This is a dated scope amendment; it does not rewrite the case-#3 row, the Status
label, the Key Pin, or `input_hashes`.

- **Scope: ATS-led.** Org-motion for case #3 = **hiring composition** from the
  public Greenhouse board (`boards.eu.greenhouse.io/beautypie`) - NOT the
  hiring+headcount-trend fusion. The LinkedIn headcount-trend leg is not
  archive-backtestable at this cutoff; an optional single Nov-2022 LinkedIn point
  may corroborate, nothing more.
- **Feasibility basis:**
  `docs/research/orgmotion_beautypie_capture_feasibility_v0.md` (gate-0 PASS: 13
  status-200 Greenhouse snapshots, 8 pre-cutoff months 2022-01..2023-01; LinkedIn
  company page first archived 2025-04, no usable pre-cutoff trend). Cutoff
  <= 2023-02, before the ~2 March 2023 announcement.
- **Capture path (Phase-4):** via the Capture Investigation Playbook +
  `orca-harness/source_capture/adapters/archive_org.py` (`select_snapshot`
  <= cutoff, anti-leakage) -> `SourceCapturePacket` -> ECR derivation. The gate-0
  by-hand CDX reads are feasibility evidence only and do **not** bind.
- **Paired design:** the org-motion units are the **only** difference between the
  baseline (without) and augmented (with) arms, presented as raw job-list facts
  (counts, departments, trajectory), never an editorialized "they were expanding"
  (anti-steering).

Non-claims (this amendment changes none of them): product-learning cap holds,
N=1; the pinned scoring key is **unchanged** (not a key change; the
`option_value: high` -> action-floor-4 rule stands as-is); **JSG-01 stays
frozen** (ECR derives integrity context and binds no `EvidenceUnit`); not
live-API authorization; mints no new ladder, closeout-state, or claim-tier
vocabulary. Org-motion is **not** promoted to a standing source-family, and the
holdouts (#5 Lime Crime, #6 REFY) are untouched.

## Amendment - Org-Motion Batch Pre-Commitment (2026-06-11, owner sign-off, in-thread)

To remove the selection bias that case-by-case org-motion admission would otherwise
carry (the case-#3 admission happened *after* its gate-0 revealed org-motion aligned
with the outcome), the owner pre-commits, in-thread 2026-06-11:

- **Org-motion is attempted on ALL remaining batch cases** (#4 Topicals, #5 Lime
  Crime, #6 REFY), not only #3. This set + the run-on-all rule are fixed **now**,
  before each case's gate-0 reveals whether org-motion aligns, so inclusion cannot
  correlate with favorability.
- **Per case:** run gate-0 feasibility; where org-motion is archive-backtestable
  <=cutoff, run the paired with/without; **record a blind org-motion prediction** (the
  signal's predicted direction) *before* the reveal. Report **all** results -
  including feasibility failures and cases where org-motion did not move the call.
  Selective reporting voids the anti-cherry-pick property.
- **Outcome-blind construction:** packets are built by an actor not holding the
  sealed outcome (see the proposed conductor construction-integrity addendum,
  `docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_proposal_v0.md`).
- **Dev/holdout respected:** dev cases (#3, #4) may inform method; holdouts (#5, #6)
  are run once under the pinned key and only reported - no key or harness iteration
  may condition on them.

Honest claim this enables: "org-motion moved the call in K of N pre-committed cases,"
not "here is a case where it worked." Caps unchanged: product-learning, small-N;
pinned scoring key unchanged; JSG-01 frozen; not live-API authorization; org-motion
not promoted to a standing source-family. Per-case org-motion scope (ATS-led vs
broader) is set at each case's gate-0, as for #3.

## Non-Claims

- Not validation, readiness, buyer proof, or judgment-quality evidence; the
  product-learning cap holds for every batch-1 result.
- Not live-API authorization; not a scoring-key change; not fixture admission;
  not a JSG-01 unfreeze; not case-finder-frame sign-off; not D5 propagation.
- Mints no ladder vocabulary: dev/holdout and the Status label are batch-local.
- This ledger's existence proves selection discipline only — it proves nothing
  about result quality.

## Amendment - Active Recall Dropped: Recognition Check -> Isolation Screen + Trace Tell-Audit (2026-06-12)

Per the ratified owner architecture decision (drop active recall entirely,
2026-06-12) and the conductor construction-integrity addendum v1
(`docs/product/judgment_spine/conductor_construction_integrity_probe_addendum_v1.md`,
R3/R5; v1 pending ratification, applies as by-hand discipline), propagated by
`docs/decisions/r5_whitelist_decision_framing_propagation_v0.md`, the Execution
Rules recognition-check bullet ("a recognition check per case-and-model pair
precedes any judgment ... a fail is a swap signal") is **superseded** as follows
(dated note; the original bullet is left in place per the dated-amendment-only rule):

- A **non-inducing pre-judgment isolation screen** (structural web-off /
  `isolation_result == proven`, recorded) precedes any judgment. Active "name the
  case" recall is **dropped** — forcing recall manufactures recognition (a
  survivorship trap).
- **Recognition capacity alone is not contamination and not a swap signal.**
  Contamination is **outcome-USE**, caught after the fact by tell-auditing the
  required reasoning trace at JSG-08; a confirmed outcome-use tell routes the arm to
  contaminated / **quarantine = recorded-as-data, not discarded**.
- A fame/obscurity screen may still inform swap selection, but it is not a
  recognition gate.

This is a dated method amendment only. It changes none of the caps: pinned scoring
key unchanged; product-learning cap and N held; JSG-01 frozen; not live-API
authorization; **not a new owner sign-off**. The case list, split, panel, and swap
pool are untouched.
