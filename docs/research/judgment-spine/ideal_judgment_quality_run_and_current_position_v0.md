# Ideal Judgment-Quality Run — Reference, and Orca's Current Position

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  Reference synthesis of what an IDEAL judgment-quality Judgment Spine run requires
  (case selection, the memorization probe, clean execution, cross-family identity
  provenance, scoring), how it future-proofs as model training cutoffs vanish
  (prospective seal-and-wait), where to SOURCE such cases, and — honestly — where
  Orca currently stands relative to that ideal. Captures a multi-step reasoning
  chain so it is not lost. Not doctrine, not a new claim tier, not a validation.
use_when:
  - Designing or sourcing a judgment-quality (not product-learning) run.
  - Checking why famous/resolved cases cannot be judgment-quality and what can.
  - Deciding how much to invest in judgment-quality machinery vs product-learning.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
  - forseti/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md   # claims posture while the gap stands (dated note below)
stale_if:
  - The conductor's case-selection posture, the by-hand cap, or the probe's role changes.
  - The evidence ladder changes its tier vocabulary.
  - An authorized live blind-judgment runner, a non-synthetic post-cutoff run, the SP-5 finalizer's remaining half, or the JSG-01 EvidenceUnit binding lands (the memorization-probe runner, scoring, and the SP-5 finalizer half are already built).
```

## What this is

A durable capture of the "ideal judgment-quality run" reasoning, plus an honest
read of how close Orca is. It is a **reference**, not a claim: it does not assert
Orca has judgment quality, and it invents no tier. Orca's current honest tier is
**product-learning**.

## Part 1 — What an ideal judgment-quality run requires

**The governing principle: non-recognition comes from case *selection*, not from
disguising a case the model already knows.** You do not take a case the model has
seen and make it forget; you pick a case it *could not* have seen.

1. **Post-cutoff case selection.** Choose a decision whose **outcome resolved
   after the target model's training cutoff** (ideally the decision too). A model
   cannot have memorized an outcome that had not happened when it was trained →
   genuine non-recognition **and** a real ground-truth outcome to score against.
   Famous pre-cutoff cases (e.g. a 2022 event) are poor targets; **anonymizing**
   a famous case is *not* a substitute (re-identification risk; the conductor
   distrusts it).
2. **The memorization probe is the empirical non-recognition check** — and the
   answer to "you can't know the model's real cutoff." Stated cutoffs are fuzzy
   and unreliable; the probe tests, per case per model, "does *this* model
   recognize *this* case?" It is **mandatory and never skipped**. You don't trust
   the date; you probe.
3. **Clean execution is the binding constraint** (not identity). The blind
   judgment must be produced **isolated** (no reveal/outcome leakage into
   context), **no-tools** (no looking the answer up), and **sealed before**
   reveal — with **auditable provenance** (a runner receipt). This is where
   judgment-quality is actually won or lost, and where by-hand caps at
   product-learning.
4. **Cross-family identity provenance comes from who *ran* the model, never the
   model's self-report.** A model's self-stamp of its own family is banned
   self-certification and unreliable (models misreport their identity; promptable
   with "you are Y"). The family fact must come from the **dispatcher** (operator
   who chose the endpoint → product-learning grade) or an **auditable runner**
   (→ judgment-quality grade).
5. **Scoring + score-linked calibration.** A deterministic score (JSG-07) and a
   score-linked outcome calibration (JSG-08) against the real outcome.

## Part 2 — Future-proofing: when models lose a clean cutoff

As models become continuously-updated / live-retrieval, there is no clean "after
the cutoff" window. The method does not break — it **shifts shape**:

- The probe stays valid (empirical); it simply rejects more cases.
- The robust limit is **prospective seal-and-wait**: judge a decision whose
  outcome is **genuinely unresolved in the real world**, seal the judgment, and
  wait for reality to resolve it. No model — however current — can memorize an
  outcome that has not happened *anywhere* yet.
- So `sealed_awaiting_outcome` is not an edge case — it is the **future-proof
  core**. The progression: famous pre-cutoff (worthless) → recent post-cutoff
  retrospective (probe-gated) → **prospective seal-and-wait** (survives a
  no-cutoff model).
- Residual tensions (real): prospective testing is **slow / low-throughput**
  (wait real time); **live/RAG models blur "blind, no-tools"** (testing them
  isolated measures reasoning, not as-deployed use — the test definition may have
  to fork); it gets operationally harder as models advance.

## Part 3 — Sourcing the cases (the "case-finder")

The trap: *emergent* stories are encountered as post-mortems (already resolved →
memorized). The unlock: for **scheduled-resolution events, documentation peaks
*before* the outcome** — the inverse of a post-mortem.

- **Scheduled-resolution public events:** FDA/regulatory decision dates, earnings,
  M&A awaiting antitrust clearance, court rulings with set dates, elections/votes,
  central-bank decisions, product launches. Rich pre-decision evidence + a known
  resolution date + a currently-unknown outcome.
- **Forecasting / prediction platforms** (Metaculus, Good Judgment, Polymarket,
  Kalshi): purpose-built feeds of "open, documented, resolves-on-a-date,
  objectively scorable" questions — and they supply a **human baseline** to beat.
- **Strategic decisions in flight:** a company publicly weighing a documented bet
  whose result will be observable (the prospective form of the canoo-walmart
  shape).

**Filters:** must be a genuine **decision with options/tradeoffs** (not just a
binary forecast — the spine measures decision quality); **workable outcome
horizon** (months, not years); **objectively verifiable** outcome; enough
**pre-decision public evidence**; spotlit enough to document but not so saturated
the model holds a hard outcome prior (the probe still gates this).

**Recognition:** prospective judgment-quality is **forecasting-tournament
methodology applied to decisions** (superforecasting) — a validated paradigm that
both confirms the approach and tells you where the supply and baselines live.

## Part 4 — The honest cost

Judgment-quality evidence is **perishable and per-model** (each run is tied to one
model's cutoff; today's clean case is tomorrow's memorized case), **low-throughput**
(prospective runs wait real time), and demands a **continuous curation pipeline**
(the case-finder). The durable asset may be the *pipeline that can reliably source
and run these*, not any single run.

## Part 5 — Where Orca stands today ("almost", honestly)

**Current honest tier: product-learning.** Not a deficiency to apologize for — it
is the correct tier given the by-hand reality, and product-learning data is ~fully
usable for Orca's own work (learning, iterating, internal decisions). "Usable for
our work" and "earns the judgment-quality tier (survives a hostile external
reviewer)" are different things; we have the former.

**What is already solid (the "almost"):**
- **Identity / cross-family provenance** via owner-dispatch (you know the
  endpoint; immune to "you are Y" injection) — solid for the family fact.
- The **SP-5 finalization design** (separate finalization-receipt record keyed by
  `evidence_id`, operator family-attestation; A1/A3 settled).
- The **reveal/calibration + classification/closeout machinery** works by-hand
  today (canoo-walmart carries a complete JSG-08 + JSG-09/10 set).
- The conductor is hardened (Round-18) and the gate predicates are
  mechanically checkable against real receipts (canoo-walmart exercise).

**The gap to judgment-quality (the binding constraints) — corrected 2026-06-09 against the harness code:**

A prior version of this list named the memorization-probe runner and scoring as
gaps. That was wrong: both are **built** (`orca-harness/runners/run_memorization_probe.py`;
`scoring/band_scorer.py` + the `run_case.py` "fixed Step A case scorer"). See
`judgment_spine_machinery_build_state_gap_map_v0.md` for the verified inventory.
The accurate, narrower gap:
- **Authorized live blind-judgment execution under proven isolation.**
  `test_no_llm_imports` bars the LLM **SDK import packages** (not raw HTTP), and
  `run_memorization_probe_raw_api.py` already makes opt-in guarded live calls for the
  *probe* via raw `urllib`. The missing piece is the equivalent for the **blind
  judgment**: an *authorized live-execution surface* (raw API is the accepted one)
  producing a blind judgment under proven isolation, bound to an auditable
  live-execution record. Today this is by-hand; no authorized real-case record exists.
- **SP-5 finalizer** — half built (corrected 2026-06-11): the
  `FinalizationReceipt` model + validate-only consumer exist
  (`orca-harness/schemas/finalization_models.py`, committed `a37f896`); the
  remaining gap is the case-packet/`EvidenceUnit` side. Current inventory:
  `judgment_spine_machinery_build_state_gap_map_v0.md`.
- **JSG-01 `EvidenceUnit` binding** — the ECR derivers are built but bind no
  `EvidenceUnit`; no case packet yet carries the derived fields.
- **Post-cutoff / prospective case sourcing** — the case-finder pipeline (Part 3); only a frame doc exists.

So "almost" = **product-learning now, with a clearly-named gap**: close in design
and on the identity piece, gapped on the cleanliness machinery + case sourcing
that actually define judgment-quality. It is **not** a new tier; the current claim
tier remains product-learning.

**Strategic note (flag, not a decision):** because judgment-quality is perishable,
per-model, low-throughput, and case-finder-dependent, leaning on **product-learning
as the workhorse** — and treating judgment-quality as a deliberate, curated,
occasional, *prospective* effort when external proof is specifically needed — is a
defensible posture. Whether to invest in the judgment-quality machinery vs. bank
product-learning value is a **product-strategy decision** (owner-owned), not
settled here.

## Dated Note — Claims Posture While The Gap Stands (owner-accepted 2026-06-11)

After a claims-policy pass (cross-vendor adversarially reviewed), the owner
accepted that the gap above cannot be closed by declaration or framing: Orca
does not "JQ itself." External wording is governed by
`docs/product/product_lead/orca_claim_defense_doctrine_v0.md` — the
Judgment-Quality **Standard** frame: Orca markets being **built to** the
standard now; **proven at** the judgment-quality rung becomes claimable only
when the ladder's `completed_judgment_quality_evidence` receipt exists. Per
Parts 1–2 above, that receipt arrives only through the sealed path
(probe-gated post-cutoff retrospectives at best; prospective seal-and-wait as
the future-proof core) plus the named machinery receipts — not through
rebuttal capability, staged disclosure, or branding. Until then the honest
tier stays product-learning, and the commercial route runs through buyer-proof
(paid pilots generate sealed forward calls as a side effect). Owner read,
recorded so a future thread does not re-litigate self-declared JQ: "that would
come again only when [we] have sealed."

## Non-Claims

- Not doctrine; not a controlling source; no `direction_change_propagation` receipt.
- Mints **no** new claim tier; "almost judgment quality" is a proximity
  description. Orca's current tier is **product-learning**.
- Does not validate the Judgment Spine, does not claim Orca has judgment quality,
  does not authorize model execution, scoring, fixture admission, or a build.
- Reference synthesis / docs-analysis only; not readiness, not buyer proof.
