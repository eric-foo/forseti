# Handoff Packet — C2 Risk-State Weighting: re-ground onto main's two-axis demand-state model

```yaml
retrieval_header_version: 1
artifact_role: >
  Handoff packet (cold cross-lane state transfer; workflow-handoff output) —
  re-ground C2 Rule 3 (risk-state weighting) onto main's two-axis demand-state model.
scope: >
  Transfers the C2 risk-state weighting work to a fresh lane off origin/main:
  Phase A determines net-new/patch/duplicate against the live C2 read-contract
  lane; Phase B re-grounds the salvageable reasoning onto main's two-axis model
  (durable/transient persistence + real/manufactured integrity). Cold-reader
  self-contained; confirm-don't-trust load contract.
use_when:
  - Picking up the C2 risk-state weighting re-grounding in a fresh lane off main.
authority_boundary: retrieval_only
applied_contract: authored via workflow-handoff (packet owner); courier prompt deferred to workflow-prompt-orchestrator.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: Orca C2 rule-3 in-thread lane (Claude Opus-class) on stale `ecr-sp3-timing-deriver-slice1`; provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/c2_risk_state_weighting_reground_two_axis_handoff_v0.md
- expected_branch (sender): ecr-sp3-timing-deriver-slice1 — STALE; the receiver spins its OWN worktree off `origin/main`, NOT this branch
- expected_head (sender): 0fc58cfe
- expected_dirty_state_including_handoff_file: 19 untracked / 0 modified at refresh; this handoff file is newly untracked; the two C2 artifacts below are untracked on this branch
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: Orca's **durable-vs-transient** demand calls become trustworthy enough that a decision owner allocates (and eventually pays) against them, on an inherently manipulable public substrate — trust earned by method, not asserted.
- anchor_goal: Re-ground the **C2 risk-state weighting rule** ("Rule 3") onto `main`'s settled **two-axis demand-state model**, AFTER first determining whether such a rule already exists in the live C2 read-contract lane (net-new / patch / duplicate). Design + docs only.
- success_signal: (Phase A) a written net-new/patch/duplicate finding, evidenced from the `ledger-c2-read-contract-v0` lane + `main`; then (Phase B, if warranted) a re-grounded Rule 3 that (a) puts the cap/discount/neutral risk-state machinery on the **MANUFACTURED (integrity) axis**, (b) treats **TRANSIENT as a persistence verdict with monitoring, NOT a cap**, (c) preserves the salvageable reasoning + re-mapped findings AR-01..06, (d) is authored in a fresh worktree off `main`, (e) asserts no scoring engine, no numbers, no G1/G2 reopening, no live-fold.

## Open Decision / Fork

- decision: **Is Rule 3 net-new, a patch to existing C2 doctrine, or a duplicate?** — resolve in Phase A before building.
  - options: (i) net-new → author it; (ii) patch → fold the salvaged reasoning into the existing C2 read-contract rule; (iii) duplicate → discard our doc, carry only any genuinely-new findings.
  - already constrained / off the table: the two-axis demand-state model is **settled on `main` (PR #78)** — do not re-litigate it; consume it.
  - trade-offs: building net-new risks duplicating live doctrine; patching requires reading the existing lane first.
  - owner of the call: the receiver proposes the classification from evidence; the **owner signs off** before any live fold.
- decision: **How the old "dispositive mechanism classes" split across the two axes.** Sender's proposed mapping (verify, don't trust): MANUFACTURED axis = astroturfing/coordination, bots/fake accounts, review-stuffing, gifted-creator waves; PERSISTENCE/TRANSIENT axis (NOT a cap) = resale/flip, event-driven/one-time, panic/scarcity buying; **channel sell-in≠sell-through = judgment call** (integrity-artifact vs transient). Owner signs off.

## Drift Guard

- **Work off `origin/main`, not `ecr-sp3-timing-deriver-slice1`.** The sender branch is stale (does NOT contain PR #78); its working-tree product docs still say the retired "hollow." Acting on it reproduces the original error.
- **The two-axis model is settled doctrine — consume, don't reopen.** `main`: **DURABLE vs TRANSIENT** (persistence) and **REAL vs MANUFACTURED** (integrity). "Hollow" is RETIRED (it conflated "decays" with "fake"). Action ceiling is matched to the demand's lifespan; transient = open + act in-window, then observe persistence.
- **TRANSIENT is not dispositive.** A just-emerged real trend can't be called durable (no track record) → it is **transient** + monitored, not capped. The sender's stale Rule 3 wrongly treated transient patterns (resale/event/panic) as dispositive caps. The cap belongs to the **MANUFACTURED axis only**.
- **The two stale artifacts encode the OLD frame — input reasoning, NOT authority.** Do not copy their "durable-vs-hollow" vocabulary; re-map, don't transcribe.
- Do **not** reopen the ratified **G1/G2 demand gate** (admissibility). INV-1: **no scoring engine, no numbers, no formula.** Design/docs only, **product_learning**; anything live/fold is **owner-gated**.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first).
- targets to enter the ladder (on `main`): `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` (the two-axis model); `docs/decisions/orca_product_thesis_consumer_demand_v0.md`; `docs/product/beauty_vertical_satellite_v0.md`; the `ledger-c2-read-contract-v0` lane's docs; the `judgment-spine-read-machinery-architecture-v0` lane's docs; the ratified demand-gate (G1/G2) doc on `main`.
- already loaded (weak orientation; NOT authority): the sender read `main`'s taxonomy via `git show` and confirmed the two-axis text; re-read fresh on `main`.
- must load first (before any strict/actionable step): `AGENTS.md` + overlay README; then `main`'s taxonomy + the `ledger-c2-read-contract-v0` lane (Phase A depends on it).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Two-axis demand-state model (durable/transient + real/manufactured); "hollow" retired.** Decided on `main` via PR **#78** (squash commit `c36e09c2`), lane `demand-read-taxonomy-adjudication-v0`; iterated further on `main` (#88, #91, #100). Verify: `git show origin/main:docs/product/product_lead/orca_demand_read_taxonomy_v0.md` (reread-required). Verify before any actionable use.
- **The C2 read step + "one core, two shells" read-machinery, checkpoint #3 = weighting.** Lane `judgment-spine-read-machinery-architecture-v0` (worktree `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-judgment-read-machinery-wt` @ `57339ea5`). Verify: read that lane fresh; reread-required.
- **The live C2 read-contract home.** Lane `ledger-c2-read-contract-v0` (worktree `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-ledger-c2-read-contract-wt` @ `6a04612e`). Phase A must read this. Verify: reread-required.
- **Ratified demand gate (G1/G2) = admissibility (genuine vs manufactured filter).** Consumed, not reopened. Verify on `main`; reread-required.

### Salvageable reasoning to carry (re-map onto the two axes; do NOT transcribe the old vocab)

The sender's Rule 3 reasoning, worth re-homing (re-mapped so the cap lives on the MANUFACTURED axis and transient is a persistence verdict):
- **Three evidentiary states → ceiling:** confirmed-present → **cap** (defeater); unconfirmed → **discount**; confirmed-absent → **neutral / floor-cleared, never positive**. Monotone: cap ≤ discount ≤ neutral.
- **Unconfirmed discount has two bands, boundary = reversibility of the *committed portion* of the action** (NOT the verb), across **economic, reputational, operational, evidence-contamination** lock-in; **least-recoverable dimension binds** (anti-slicing). Recoverable → mild (proceed); not recoverable → near-cap (advise the recoverable path until checked).
- **Discriminator set (required) per governed risk:** a present-fingerprint + an absent-clearing-check, each with a **stated sufficiency bar**; core owns the requirement + the per-class families; the vertical deck owns the specific tells. **Unlock rule:** a material/irreversible action earns a durable-grade green-light only by *running* the discriminator.
- **Discriminator status triple:** missing-but-buildable (withhold material, advise recoverable) / inconclusive (near-cap, owner bets) / impossible (→ falsifiability filter). Separator: "can you name a runnable clearing-check with more data/work?"
- **Falsifiability filter + inherent-limit caps:** a risk with no possible clearing-check does not block; it is a standing inherent-limit cap (e.g., small-N) or discarded.
- **FP/FN bounded asymmetry:** a false "durable" is irreversible + trust-damaging, worse than a reversible false "not-yet"; but bounded (a judge that never certifies is inert), so the discount hardens toward a cap only as the bet becomes irreversible.
- **Advisory, not control:** the judge withholds/grants a verdict + recommended ceiling; it never prohibits the owner's action.
- **Mini god tier:** qualitative now (no probabilities); numeric v2 only with a calibration spine + the owner lifting INV-1 — an *intended migration hypothesis*, not a guaranteed structure-preserving upgrade.

### Cross-vendor review findings to carry (AR-01..06; adjudicated ACCEPTED, re-map don't discard)

- **AR-01:** each discriminator set must state a **sufficiency bar** (what = "established present").
- **AR-02:** **broaden by property** — risks defined by "defeats durable end-use demand," mechanism-classes, not fabrication-only. *(On the two-axis model this re-maps: MANUFACTURED-axis mechanisms cap; persistence-axis ones are transient, not caps.)*
- **AR-03:** distinguish **missing / inconclusive / impossible** discriminator states (triple above).
- **AR-04:** reversibility is **multi-dimensional, least-recoverable binds** (above).
- **AR-05:** 3(c) baseline = "risk-absent baseline"; verified-clean = baseline, no positive bonus (anti-gaming) — preserved.
- **AR-06:** v2 numeric = migration **hypothesis**, may need to decompose bands into separate variables.

## Active Objective

Determine whether a C2 risk-state/weighting rule already exists in the live C2 read-contract lane on `main`, then (if warranted) re-ground the sender's Rule 3 onto `main`'s two-axis demand-state model — cap/discount/neutral on the MANUFACTURED axis, transient as a monitored persistence verdict. Design/docs only; nothing built, validated, or folded live.

## Exact Next Authorized Action

1. Spin a **fresh worktree/branch off `origin/main`** (AGENTS isolation; do NOT use `ecr-sp3-timing-deriver-slice1`). Run the Orca start preflight.
2. Read `AGENTS.md` + `.agents/workflow-overlay/README.md`, then `main`'s `orca_demand_read_taxonomy_v0.md` (two-axis model) + the **`ledger-c2-read-contract-v0`** lane + the **`judgment-spine-read-machinery-architecture-v0`** lane.
3. **Phase A:** classify Rule 3 as **net-new / patch / duplicate**; write the finding with evidence. Report to owner before building.
4. **Phase B (if warranted):** re-ground/author Rule 3 on the two-axis model, re-mapping the salvageable reasoning + AR-01..06; place the cap on the MANUFACTURED axis; treat transient as monitored persistence.
5. Stop condition: a Phase-A finding (+ optionally a re-grounded PROPOSED Rule 3); no scoring engine, no numbers, no G1/G2 reopen, no live fold (owner-gated).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim) — reread-required.
- Overlay authority: `.agents/workflow-overlay/` (README, source-loading, source-of-truth, decision-routing, prompt-orchestration) — reread-required.
- User constraints: work off `main`; two-axis model is settled (consume); transient ≠ cap; cap = manufactured axis; no scoring; don't reopen G1/G2; owner-gated for live.
- Source-read ledger:
  - `origin/main:docs/product/product_lead/orca_demand_read_taxonomy_v0.md`
    - Role: the settled two-axis demand-state model (durable/transient + real/manufactured).
    - Load-bearing: yes
    - Compare target: contains "two independent axes — durable vs transient (persistence) and real vs manufactured (integrity)"; landed via `c36e09c2` (#78). Verify `git merge-base --is-ancestor c36e09c2 origin/main` exits 0. reread-required on `main`.
    - Last checked: 2026-06-15 (via `git show origin/main:`)
    - Reuse rule: read fresh on `main`; this is the doctrine to re-ground onto.
  - `ledger-c2-read-contract-v0` lane (worktree `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-ledger-c2-read-contract-wt`)
    - Role: candidate live home of the C2 read-contract; Phase A must read it.
    - Load-bearing: yes
    - Compare target: HEAD `6a04612e` (2026-06-15); reread-required.
    - Reuse rule: read fresh; determines net-new/patch/duplicate.
  - `judgment-spine-read-machinery-architecture-v0` lane (worktree `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-judgment-read-machinery-wt`)
    - Role: "one core, two shells" read-machinery; where C2/Rule 3 conceptually sits.
    - Load-bearing: yes
    - Compare target: HEAD `57339ea5` (2026-06-15); reread-required.
    - Reuse rule: read fresh; orientation for C2's place.
  - `docs/decisions/orca_c2_risk_state_weighting_v0.md` (sender artifact)
    - Role: the stale-frame Rule 3 — INPUT reasoning to salvage, NOT authority.
    - Load-bearing: no (orientation)
    - Compare target: sha256 `D506CDC2B1BED609D9F261977D52663C5A3E16920284B8C6F965DEC21B5D221E`; **UNTRACKED on `ecr-sp3` @ 0fc58cfe** — will NOT appear in a worktree off `main`. Read by absolute path `C:\Users\vmon7\Desktop\projects\orca\docs\decisions\orca_c2_risk_state_weighting_v0.md` while it exists, or rely on the salvage summary above.
    - Last checked: 2026-06-15
    - Reuse rule: re-map, never transcribe the old vocabulary.
  - `docs/review-outputs/adversarial-artifact-reviews/orca_c2_risk_state_weighting_adversarial_artifact_review_v0.md` (sender artifact)
    - Role: the cross-vendor review + CA adjudication (AR-01..06).
    - Load-bearing: no (orientation)
    - Compare target: sha256 `76C5D20303A1A0983885DF93834A4A493E0A76A9A491F7746E698B546D279350`; UNTRACKED on `ecr-sp3` — won't travel. Findings summarized above.
    - Last checked: 2026-06-15
    - Reuse rule: carry the findings (above), re-mapped to two axes.
- Source gaps: the two sender artifacts + this handoff are UNTRACKED on `ecr-sp3` — a worktree off `main` cannot git-access them; this packet carries their substance inline.
- Strict-only blockers: any live fold into the C2 contract is a doctrine change (owner-gated + DCP receipt); out of scope for this lane.
- Not-proven boundaries: nothing here is validated, ready, or implementation-authorized; Rule 3 is PROPOSED on a stale frame.

## Current Task State

- Completed (sender): a PROPOSED Rule 3 + a cross-vendor adversarial review (AR-01..06 adjudicated/patched) — but on the STALE "durable-vs-hollow" frame.
- Partially completed: nothing re-grounded onto the two-axis model.
- Broken or uncertain: the sender's Rule 3 conflates the persistence and integrity axes; its treatment of transient as a cap is wrong on `main`'s model.

## Workspace State

- Branch (sender): ecr-sp3-timing-deriver-slice1 @ 0fc58cfe — STALE; receiver must NOT continue here.
- Dirty/untracked (sender): 19 untracked / 0 modified; includes the two C2 artifacts + this handoff file (all untracked).
- Target files/artifacts: none yet for the receiver (off `main`).
- Related worktrees/branches: `ledger-c2-read-contract-v0` @ `6a04612e`; `judgment-spine-read-machinery-architecture-v0` @ `57339ea5`; `demand-read-taxonomy-adjudication-v0` (vocab owner, squash-merged to main as `c36e09c2`/#78).

## Changed / Inspected / Tested Files

- `docs/decisions/orca_c2_risk_state_weighting_v0.md` — created by sender; stale frame; INPUT only; untracked on ecr-sp3.
- `docs/review-outputs/adversarial-artifact-reviews/orca_c2_risk_state_weighting_adversarial_artifact_review_v0.md` — created by sender; the AR review; untracked on ecr-sp3.
- `docs/prompts/handoffs/c2_risk_state_weighting_reground_two_axis_handoff_v0.md` — this packet; untracked on ecr-sp3.

## Frozen Decisions

- The two-axis demand-state model (durable/transient + real/manufactured; hollow retired) is settled on `main` (#78). Do not reopen.
- The cross-vendor AR-01..06 adjudications (ACCEPTED) stand as reasoning; re-map onto two axes, don't re-litigate.
- INV-1 (no scoring engine); advisory-not-control; G1/G2 not reopened.

## Mutable Questions

- Net-new vs patch vs duplicate (Phase A resolves).
- The exact mechanism-class → axis mapping (sender's proposal above; owner signs off).
- Whether the live C2 read-contract already encodes a risk-state rule (read `ledger-c2-read-contract-v0`).

## Superseded / Dangerous-To-Reuse Context

- **"durable vs hollow" framing** — SUPERSEDED by the two-axis model on `main`. Reusing it reproduces the conflation. Replacement: durable/transient (persistence) + real/manufactured (integrity).
- **Treating transient patterns (resale/event/panic) as dispositive caps** — WRONG on `main`'s model. Replacement: those are transient (persistence axis), not caps; only manufactured-axis mechanisms cap.
- **The sender branch `ecr-sp3-timing-deriver-slice1`** — stale (no #78); additive-untracked scratch only. Replacement: a fresh worktree off `main`.
- **The sender's Rule 3 doc as authority** — it is stale-frame INPUT only. Replacement: the salvage summary + `main`'s model.

## Commands And Verification Evidence

- Vocab merge provenance (run 2026-06-15, sender):
  ```bash
  git merge-base --is-ancestor c36e09c2 origin/main   # exit 0 → two-axis model IS on main (#78)
  git merge-base --is-ancestor c36e09c2 HEAD          # exit 1 → ecr-sp3 does NOT have it (stale)
  git branch -a --contains 95fe809f                   # only demand-read-taxonomy-adjudication-v0 (the owning lane)
  ```
  Result: two-axis model merged to `main`; sender branch stale. Re-run target: the same three commands.
- Sender artifact hashes (re-verify if read by absolute path): `D506CDC2…` (rule), `76C5D203…` (review).

## Blockers And Risks

- Sender artifacts untracked on a stale branch → not git-accessible off `main`.
  - Evidence: `git status` `??`; `is-ancestor c36e09c2 HEAD` exit 1.
  - Likely next action: rely on this packet's inline salvage; read the stale doc by absolute path only as optional cross-check while it exists.
- Possible duplication with the live C2 read-contract lane.
  - Evidence: `ledger-c2-read-contract-v0` lane exists (@ `6a04612e`).
  - Likely next action: Phase A read it first; classify before building.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) `main` has the two-axis model (`is-ancestor c36e09c2 origin/main` = 0; reread the taxonomy on `main`); (2) the receiver is on a FRESH worktree off `main`, not ecr-sp3; (3) the `ledger-c2-read-contract-v0` + read-machinery lanes' current state (reread-required); (4) the G1/G2 gate on `main`.
- Compare targets: `c36e09c2` ancestry of `origin/main`; worktree HEADs `6a04612e` / `57339ea5`; artifact sha256s if read.
- Load outcomes: `REUSE` only if `main` has the two-axis model and the receiver is off `main`; `STALE_REREAD_REQUIRED` if the lanes moved; `BLOCKED_UNVERIFIABLE` if the C2 lane state can't be read and Phase A depends on it.
- Sources to reread if drift: `main`'s taxonomy + the `ledger-c2-read-contract-v0` lane (they bound the whole decision).

## Do Not Forget

- **Work off `main`, never `ecr-sp3`.** The stale base is the entire reason this handoff exists.
- **Transient is NOT a cap** — it's a monitored persistence verdict. The cap lives on the **manufactured** axis.
- **Phase A before Phase B** — find out if Rule 3 already exists before re-authoring it.
- The two sender artifacts are **stale-frame INPUT, not authority** — re-map, don't transcribe.
