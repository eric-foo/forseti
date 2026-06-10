# Judgment Spine Lane — Handoff Prompt (GPT-5.5 reasoning lane)

> Paste everything below the line into a fresh GPT-5.5 chat. It is fully self-contained;
> the lane has no access to the Orca repo, so all state it needs is inlined.
> Author: Orca judgment-lane orchestrator (Claude). Date: 2026-05-29. Status: v0 handoff.

---

## Your role

You are an independent **strategy + judgment-quality** reasoning lane for Orca's "Judgment Spine." You own thinking, not execution. You have **no access to the codebase and you will not write or run code.** Any step that requires writing/running code is **flagged and routed back** to a separate Claude Code session that runs only under the owner's explicit per-step authorization.

Treat this as a serious analytical commission. Be skeptical, show your reasoning, and flag where you are uncertain or where you'd need a source you don't have.

## What Orca is (context, 1 paragraph)

Orca is building a "Judgment Spine": a system whose wedge competency is **signal-integrity judgment** — specifically, distinguishing *independent corroboration* (multiple genuinely independent sources agreeing → keep/weight) from *artificial amplification* (echo, syndication, copied language, one source quoted everywhere, botting → downgrade/exclude). The product is validated by **competitor-substitution backtests**: take a real past business decision with a known outcome, freeze the evidence available *before* the decision cutoff, and test whether a disciplined judgment process reaches a defensible call. A deterministic "harness" acts as referee: it scores a contestant LLM's structured judgment against a hand-built **facilitator-ledger answer key**.

## The judgment harness in brief (v0.14)

- The harness maps a decision onto **14 frozen enum "band inputs"** and derives an **action band** on a 0–8 ladder (0=hold … 8=commit). It is a pure function (deterministic).
- **Ceiling** starts from evidence strength (`none→0, weak→3, moderate→5, strong→7`), adjusts for evidence independence (`correlated −1, partially_independent 0, independent +1`), then is **capped down** by constraint inputs (low reversibility feasibility, high build cost, weak authority/capability, bad loss shape all *cap the ceiling lower*).
- **Floor** is pushed *up* by pressure inputs (high option value, fast information decay, asymmetric upside, urgency, opportunity cost).
- If **floor > ceiling**, the case is a **conflict** → forced status `conflict_escalate` (rendered 6/6), meaning "the situation pressures you toward a bigger move than the evidence/constraints can justify — escalate / don't fake-reach."
- A "ceiling_trap" is the adjacent case where floor ≤ ceiling but the ceiling is held low by constraints.
- (You do **not** have the exact numeric cap/floor tables — they live in the repo spec and the Claude Code step will read them directly. You have enough above to sanity-check band logic qualitatively.)

## Current state — what has already been done (do not redo)

1. **Case #1 (judgment lane) chosen = Thomson Reuters / Casetext (MV-09).** Decision under test: *at 2023-06-25, how far should Thomson Reuters commit toward Casetext / its CoCounsel AI product — watch / partner / license / build / **acquire**?* The real (hidden, post-cutoff) outcome was a **$650M acquisition** (definitive agreement 2023-06-26, closed 2023-08-17 — both post-cutoff, excluded from evidence). This case was chosen because its pre-cutoff evidence is press/court/official-heavy and reachable (not blocked behind archive.org/Reddit, which a separate "capture" lane is handling).
2. **The facilitator-ledger band inputs were authored and independently adjudicated** via the calibration-grade workflow: primary labels (Claude) → second labels (GPT-5.5, separate lane) → independent adjudication (third lane). Result: **9 of 14 inputs agreed; 5 resolved to the second labeler on the merits.**
3. **Disposition = QUARANTINED → plumbing-grade.** The quarantine rule fires at >3 disagreements (5 here). Per the rubric, *quarantined cases may still be used as plumbing fixtures, but cannot support judgment-quality claims.* This was judged **substantively correct, not a volume artifact**, because the case sits on a knife-edge (below).
4. **No harness code currently exists.** An earlier skeleton was built and then deliberately reverted; it will be rebuilt later, properly, only under explicit per-step authorization.

### The adjudicated TR/Casetext ledger (frozen-candidate — do NOT re-label)

**Final 14 band inputs (post-adjudication):**

| input | value |
|---|---|
| evidence_strength | moderate |
| evidence_independence | partially_independent |
| reversibility_feasibility | low |
| reversibility_cost | high |
| authority | partial |
| authority_acquisition_cost | medium |
| capability | partial |
| capability_build_cost | high |
| loss_shape | asymmetric_down |
| opportunity_cost | moderate |
| information_decay | fast |
| option_value | high |
| upside_shape | asymmetric_up |
| urgency | medium |

**Hand-derived band (illustrative, not scorer-run):** ceiling = 3 (capped by `reversibility_feasibility: low` + `capability_build_cost: high`), floor = 4 (driven by `option_value: high`) → floor > ceiling → **`conflict_escalate` 6/6.**
**KNIFE-EDGE:** `option_value` moderate↔high flips the answer between `conflict_escalate` and `ceiling_trap` (floor 3 vs 4 against ceiling 3). This instability is *why* the quarantine is substantively right.

**Pre-cutoff evidence set (≤ 2023-06-25):**
- **E1** — LawSites (lawnext.com), 2023-03-01: CoCounsel launch, 7 skills, named beta firms, hands-on review. *Semi-independent.*
- **E2** — Casetext press release (PRNewswire), 2023-03-14: origin of the "GPT-4 passed the bar exam" claim. *Vendor source.*
- **E3** — SSRN paper, Katz/Bommarito/Gao/**Arredondo**, 2023-03-15: ~90th percentile / 297 UBE. *Arredondo is a Casetext co-founder → vendor-affiliated.*
- **E4** — Stanford Law "Legal Aggregate" blog, 2023-04-19. *Echo of the bar-exam claim.*
- **E5** — TaxProf Blog, 2023-03. *Echo.*
- **E6** — Thomson Reuters official "content-driven AI" comms, 2023-05: build/buy/partner posture + >$100M/yr AI investment signal.
- **E7** — TR + Microsoft 365 Copilot plugin, 2023-05.

**Must-address signal-integrity items (the discriminations a good judgment must make):**
- **MA-01** — the "passed-the-bar / category leader" signal is **amplification of one vendor-affiliated source** (E2/E3 + echoes E4/E5), not independent corroboration.
- **MA-02** — moderate, partly-amplified evidence supports *scoped, reversible* moves, **not** a low-reversibility $650M acquisition.
- **MA-03** — competitive FOMO is real but **unquantified** (no evidence of an imminent rival bid) → don't over-commit on fear.
- **MA-04** — separate the genuine GenAI-in-legal opportunity from the unverified "Casetext is THE leader" framing.
- **MA-05** — distinguish independent signal (E1 hands-on; named adopters) from echo (press reprinting the PR).

## Hard constraints (do not violate)

1. **You write no code and cannot access the repo.** Produce reasoning artifacts and specs only. Flag code steps for the Claude Code session; that session acts only under the owner's explicit per-step authorization.
2. **Plumbing vs judgment-quality boundary.** Any harness run on TR/Casetext proves only that the *plumbing works* and exercises the `conflict_escalate` path. It is **never** evidence of judgment quality — the case is quarantined and contaminated (well-known outcome; likely memorized by any modern LLM).
3. **Calibration-grade rigor** for any *fresh* judgment-quality ledger you plan: every band input must be justified from pre-cutoff sources, the derived band must be skeptic-defensible, nothing may be reverse-engineered from the known outcome.
4. **Contamination ceiling.** A backtest validates plumbing + evidence-discipline + scorer-calibration — **not** forward judgment under genuine uncertainty. Don't claim more.
5. **Quarantine discipline.** Do **not** re-label the TR/Casetext ledger to escape quarantine, and do **not** propose weakening the quarantine rule. Motivated reclassification is forbidden. Respecting the quarantine *is* the discipline.
6. **Lane decoupling.** Source-access tooling (archive.org/Reddit/etc. being unreachable) is a *separate capture lane's* problem. For judgment-quality case selection, prefer cases whose pre-cutoff evidence is reachable via ordinary web fetch.
7. Do not import conventions from any other project ("jb") as Orca authority.

## The recommended path forward — your first job is to pressure-test it

The orchestrator's current recommendation is a **sequence, not a single choice**:

- **Step A (now, code, gated on owner auth):** rebuild the engine from the v0.14 specs + build the TR/Casetext fixture + run it → first real-case `ScoringResult`. Expected: `conflict_escalate` 6/6. Claimed as **plumbing only.** Rationale: the engine is case-independent, the evidence is already in hand, and this adds `conflict_escalate` branch coverage + the first real capture→ledger→scorer integration test.
- **Step B (next, reasoning, your track):** select a **fresh, low-fame, uncontaminated** case and author a calibration-grade ledger for it — this is the only path to an actual *judgment-quality* result.

The claimed insight is that "build plumbing on TR/Casetext" and "get judgment quality" are **orthogonal** (engine correctness vs answer-key trustworthiness), so they should be sequenced, not traded off.

## Your deliverables

1. **Independent second opinion on the A→B sequence.** Is the orthogonality argument sound? Is there a reason to *not* build plumbing on a quarantined case first, or to pick the fresh case before building? Argue both sides, then give a clear recommendation. Name what would change your answer.
2. **Fresh-case track for judgment quality.** Propose **2–3 candidate cases** that are (a) low-fame / low-memorization, (b) have a clean *amplification-vs-corroboration* discrimination at their core, (c) reachable pre-cutoff evidence, (d) a known outcome. For each: the decision under test, the cutoff, why the wedge is present, and the contamination/memorization risk. Then recommend one and sketch its calibration-grade ledger plan (which band inputs will be hardest to justify; where dual-labeling is most likely to disagree).
3. **Acceptance criteria + test plan for Step A** (the part you uniquely add — do *not* re-spec the engine; the Claude session reads the v0.14 spec directly). Specify: the expected `ScoringResult` for TR/Casetext (`conflict_escalate` 6/6); a **knife-edge regression check** (flipping `option_value` high→moderate should flip the band to `ceiling_trap`); and the explicit claim-discipline string that must accompany any green run ("plumbing works only; not judgment quality").
4. **Code-routing flags.** List exactly which of your recommendations require a code step, so the owner can authorize them one at a time.

## Non-goals / boundaries

- Do not claim TR/Casetext demonstrates judgment quality.
- Do not write or pretend to run code; do not invent the engine's exact numeric tables.
- Do not re-open the TR/Casetext labels or the quarantine rule.
- Do not work on capture-lane source-access tooling.

## Output format

Use four clearly headed sections matching the four deliverables. Lead each with a one-line bottom-line, then the reasoning. Flag uncertainty explicitly. End with a short "what I'd need to go further" list (sources, decisions, or authorizations).
