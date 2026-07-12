# Handoff Packet — Demand-Signal Reconstructability + Retrospective Backtest Probe (research-engine lane)

```yaml
retrieval_header_version: 1
artifact_role: Cross-lane handoff packet (probe commission; owner-directed 2026-07-10)
scope: >
  Commissions the research-engine lane (Commission Signal Board -> Scanning ->
  Capture) to run a two-part validation probe: (1) a demand-signal
  reconstructability inventory (which public demand signals can have their
  point-in-time history rebuilt from archives and cutoff-dated items, at what
  fidelity), and (2) a retrospective backtest feasibility test (do
  zero-lookahead reconstructed demand-signal series correspond to SEC-filed
  outcomes for a small public consumer-brand ticker set). Probe/validation
  tier only; authorizes no build, no standing pipeline, no commercial capture.
use_when:
  - Booting the fresh research-engine lane that executes this probe.
  - Checking what the probe may and may not do (probe-tier boundaries).
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_research_engine_map_v0.md
  - docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md
stale_if:
  - The probe completes and its findings are captured in a durable research artifact (point here to it).
  - The un-backfillable-signal moat capture is superseded or falsified.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-07-10 (provenance, not freshness proof)
- created_by_lane: `claude/sleipnir-ci-product-shape-ab29bd` (Sleipnir product-shape exploration lane; provenance only, not authority)
- workspace: the Forseti repo. A fresh receiver lane cuts its OWN worktree/branch off `origin/main` per `AGENTS.md`.
- handoff_path: `docs/workflows/forseti_demand_signal_backtest_probe_handoff_v0.md` (committed; readable from `origin/main` after the authoring lane's PR merges, else from `origin/claude/sleipnir-ci-product-shape-ab29bd`)
- expected_branch (authoring): `claude/sleipnir-ci-product-shape-ab29bd`
- expected_head: the commit introducing this packet — verify with `git log -1 --oneline -- docs/workflows/forseti_demand_signal_backtest_probe_handoff_v0.md`
- expected_dirty_state_including_handoff_file: clean after that commit; this packet and its sibling moat capture are the only files it adds
- load_rule: confirm-don't-trust. Every load-bearing fact below carries a compare target or `reread-required`. Re-verify against primary source before any strict/actionable claim; sender claims are hypotheses, not authority.
- prompt preflight (inline core): output mode `file-write` (this durable packet; probe outputs are the receiver's, see Exact Next Authorized Action step 5) · template kind `none` (workflow-handoff packet shape) · edit permission of the authoring lane `docs-write` on its own branch · reviews `findings-first` (no formal verdict bound) · doctrine change `none enacted` (probe commission only; the sibling moat capture is decision-prep pending sign-off, no receipt) · run-authoritative input for the receiver = this packet at the path above.

## Goal Handoff

- long_term_goal: Monetize Forseti's research engine by selling calibrated, outcome-scored reads (decisions/research as a service) whose moat is two un-backfillable clocks: live-captured Class-A signal history and a live out-of-sample prediction track record. (Sender-derived from owner's in-thread words 2026-07-08/10; no `workflow-goal-framing` frame exists; receiver may re-frame.)
- anchor_goal: Establish, with evidence, (a) which public demand signals can have zero-lookahead point-in-time history RECONSTRUCTED today (Class B) vs. only captured live (Class A), and (b) whether reconstructed demand-signal series correspond to SEC-filed outcomes well enough to justify designing a real backtest — so the owner can decide the backtest/product investment with facts.
- success_signal: A durable research artifact containing (1) a reconstructability matrix (signal class × venue × method × fidelity/bias notes) and (2) a scored feasibility read on signal→outcome correspondence for the pilot ticker set, everything `product_learning`-capped, with capture routed per armory discipline and no build performed.

## Open Decision / Fork (receiver weighs, owner decides)

- decision: Pilot scope — which tickers and venues the probe reconstructs.
  - options: (a) beauty candidates surfaced in the sender thread — e.l.f. (ELF), Estée Lauder (EL), Coty (COTY), Inter Parfums (IPAR), Ulta (ULTA) — chosen because public demand signal is dense and Forseti capture lanes for adjacent venues already exist; (b) a different consumer set the receiver derives (e.g., via EDGAR 13F crowding as a fund-attention proxy); (c) a mixed set.
  - already constrained / off the table: private-company subjects for the OUTCOME side (no filed ground truth); person-level signal (see Drift Guard); any venue requiring capture outside armory discipline.
  - trade-offs: (a) is fastest and matches existing capture familiarity but bakes in a beauty assumption the owner explicitly did NOT lock ("we might wanna do beauty though but of course, we might not either"); (b) is slower but tests the indicator-not-industry framing honestly.
  - owner of the call: the owner (a 2–6 ticker pilot set is cheap to steer; surface the choice, default to (a) if unanswered since it is reversible).
  - recommendation and why: start with 2–3 of (a) plus 1–2 non-beauty consumer names, so the probe tests reconstruction fidelity AND whether the method generalizes past beauty in the same pass.

## Drift Guard (read before skimming the rest)

- PROBE TIER ONLY: this packet authorizes a bounded validation probe. It does NOT authorize building a standing pipeline, a panel, dashboards, scoring engines, nowcast models as products, commercial capture scale-up, outreach, or publishing. Findings land as research artifacts, `product_learning`-capped.
- ZERO-LOOKAHEAD RULE (the owner's core instruction): every reconstructed series item must carry a creation timestamp `≤ cutoff`. Comments especially — they accrue AFTER events, so an undated or post-cutoff comment silently leaks the outcome into the "prediction." Owner verbatim: "try to find all the demand signals using archive OR cut off (comments especially should be cut off) dated posts etc."
- CAPTURE DISCIPLINE: any capture entered as evidence routes through the Source Capture Armory Runner Ladder per `.agents/workflow-overlay/safety-rules.md`; uncaptured scouting/diagnostic reads are exempt. Per-venue route bindings and ToS posture are capture-lane-owned; this probe must not stretch them per-task.
- CSB BOUNDARY: the Commission Signal Board is an evidence/signals-only board — it emits no admit/hold/fail verdicts and authorizes no scraping (its README). The probe flows CSB (what to look for) → Scanning (where/how reconstructable) → Capture (bounded probe captures under armory rules).
- ORG-LEVEL ONLY: signals about companies, brands, SKUs, categories — no person-level dossiers, no outreach surfaces. (Parent-thesis boundary; the receiver does not need to widen it for this probe.)
- DO NOT INHERIT AS SETTLED: "beauty/fragrance is the niche" (owner-open); "momentum is not priced in" (hypothesis this probe informs, not a premise); Class-B reconstruction fidelity (the thing under test).
- Reconstructed (Class-B) history is BACKTEST FUEL, NOT MOAT — do not let probe outputs get framed as a defensible data asset (`docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md`).

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first per AGENTS.md).
- targets to enter the ladder: `docs/workflows/forseti_research_engine_map_v0.md` (the group's front doors), then the spine front doors it names (CSB README; Scanning README; Data Capture consolidation map), plus the ledger below.
- already loaded by sender (weak orientation, NOT authority): research engine map; CSB README; safety-rules; the moat capture it authored. For the receiver these are must-load, not done.
- must load first (before any strict/actionable step): the research engine map; `docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md` (defines Class A/B/C and the zero-lookahead framing this probe tests); safety-rules (armory routing).
- load rule: receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts (inline gist + verify pointer)

- Research engine = CSB → Scanning → Capture; group ends at the Capture→ECR handoff — gist: extraction front half; downstream provenance/cleaning/judgment is out of scope for this probe. Decided in: `docs/workflows/forseti_research_engine_map_v0.md`. Compare target: that file on `origin/main`. reread-required.
- Class A/B/C reconstructability taxonomy + two-clocks moat — gist: un-backfillable point-in-time state = moat; dated-item reconstruction = backtest fuel; filed outcomes = free ground truth. Decided in (pending sign-off): `docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md`. Compare target: same branch/PR as this packet. reread-required.
- Sell OUTPUT, never the engine/registry/raw feed (golden goose) — gist: probes and products expose derived reads, not the data asset. Decided in: `docs/decisions/forseti_product_thesis_consumer_demand_v0.md` (Strategic Center) + Aphrodite growth map §E. Compare target: `origin/main:` those paths. reread-required.
- Owner indicator lean (2026-07-10, in-thread, NOT locked): primary indicator = demand intensity/momentum-acceleration; authenticity co-primary; durability = monitored follow-on. Compare target: quoted in the moat capture's Status/Two-Clocks sections. reread-required.

## Active Objective

Run the two-part probe: (1) inventory public demand-signal classes for the pilot subjects across candidate venues, classifying each as Class A (live-only), B (reconstructable from archives/dated items — record method + fidelity + bias), or C (vendor/filed history); (2) for the pilot tickers, reconstruct 2–4 zero-lookahead pre-earnings signal series at past quarter cutoffs and check directional correspondence against the EDGAR-filed outcomes those quarters printed. Report feasibility, not product claims.

## Exact Next Authorized Action

1. Cut a fresh lane off `origin/main` (worktree per `AGENTS.md`). Read `AGENTS.md` + overlay README; run the source-loading ladder above; declare `SOURCE_CONTEXT_READY`/`INCOMPLETE`.
2. Surface the pilot-scope fork (Open Decision) to the owner; default to recommendation if unanswered.
3. Part 1 — reconstructability inventory: per signal class (reviews w/ dates, comments w/ dates, posts/videos w/ dates, archive snapshots of listing/rank/price pages, search-interest vendor history, engagement counters) × venue: can a `date ≤ cutoff` series be rebuilt today? Method, coverage, survivorship/deletion bias, cost. Scouting reads are exempt from armory routing; anything entered as evidence routes through the Runner Ladder.
4. Part 2 — backtest feasibility: for each pilot ticker, pick 2–4 past quarters; reconstruct the pre-cutoff series; pull the filed outcome from EDGAR (10-Q/10-K/8-K); score directional correspondence honestly (including "signal too thin to say"). No model building beyond what scoring requires.
5. Write findings to a durable research artifact under `docs/research/` (per `.agents/workflow-overlay/artifact-folders.md`: research = discovery/evidence gathering; promotion into decisions/product comes later, separately), retrieval-headered, `product_learning`-capped. Update this packet's `stale_if` pointer.
6. Stop condition: both parts reported (or blocked with precise blockers). Do NOT proceed to standing capture, pipeline build, model productization, or capture-scope expansion — each is a separate owner/capture-lane decision.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `CLAUDE.md` shim). Compare target: `origin/main:AGENTS.md`. reread-required. Load-bearing: yes.
- Overlay authority: `.agents/workflow-overlay/` (README, source-loading, safety-rules, artifact-folders, decision-routing). Compare target: `origin/main`. reread-required. Load-bearing: yes.
- User constraints: owner's probe instruction quoted in Drift Guard (zero-lookahead; comments cut off at cutoff); owner's niche-not-locked statement quoted in Open Decision. Load-bearing: yes. Compare target: quoted verbatim in this packet.
- Source-read ledger (receiver rebinds fresh; all reread-required):
  - `docs/workflows/forseti_research_engine_map_v0.md` — Role: group front door (CSB/Scanning/Capture + the ECR seam). Load-bearing: yes.
  - `forseti/product/spines/commission_signal_board/README.md` — Role: CSB entry; evidence/signals-only boundary. Load-bearing: yes.
  - `forseti/product/spines/scanning/README.md` — Role: Scanning entry (venue discovery, `capture_request`s). Load-bearing: yes. (Not read by sender; front door named by the map.)
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md` — Role: Capture front door; armory + route bindings. Load-bearing: yes. (Not read by sender.)
  - `.agents/workflow-overlay/safety-rules.md` — Role: armory routing rule for evidence capture; scouting exemption. Load-bearing: yes.
  - `docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md` — Role: taxonomy + zero-lookahead frame under test. Load-bearing: yes.
- Source gaps: Scanning README and Capture consolidation map not read by sender (named via the map only); per-venue route/ToS state unknown to sender — capture-lane-owned; EDGAR retrieval mechanics assumed standard (owner: "sec filings - we already can scrape those") — receiver verifies against the capture lane's actual EDGAR/SEC tooling before relying on it.
- Strict-only blockers: no build/pipeline/productization authority; no capture-scope or ToS expansion; no outreach/publishing.
- Not-proven boundaries: everything `product_learning`-capped; signal→outcome correspondence is the thing under test, not a premise.

## Current Task State

- Completed (sender thread): product-direction exploration (3-architect synthesis; chat-only), competitor verification (Spate/WGSN/Mintel; YipitData/M Science; illustrative tier anchors), the moat capture doc (committed alongside this packet).
- Partially completed: indicator selection (owner lean recorded, not locked); niche selection (open).
- Broken or uncertain: Class-B reconstruction fidelity (unknown — Part 1); signal→outcome correspondence (unknown — Part 2); whether beauty is the right pilot frame (owner-open).

## Workspace State

- Branch (authoring): `claude/sleipnir-ci-product-shape-ab29bd`; receiver cuts its own lane off `origin/main`.
- Head: see Load Contract compare recipe.
- Dirty/untracked before handoff: clean (this packet + the moat capture are the only additions, committed together).
- Target files/artifacts: this packet; `docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md`; receiver output under `docs/research/`.
- Related branches: sender lane PR (this branch → `main`); prior Sleipnir exploration PR #805 (context only, poison-flagged for product shape — see its own handoff history; not needed for this probe).

## Frozen Decisions (verify before strict use; do not re-litigate)

- Sell output, never the engine/registry/data/feed. Evidence: thesis Strategic Center + growth map §E. Consequence: probe outputs are reads/matrices, never a sellable data dump.
- Probe-tier scope with armory-routed evidence capture. Evidence: this packet + safety-rules. Consequence: no standing monitors or pipelines from this commission.
- Zero-lookahead reconstruction rule. Evidence: owner verbatim in Drift Guard. Consequence: any series item without a verifiable `≤ cutoff` timestamp is excluded from the backtest side (may still appear in the inventory with that caveat).

## Mutable Questions

- Pilot ticker/venue set — resolves by owner answer to Open Decision.
- Fidelity threshold for "reconstructable enough" — receiver proposes from Part-1 evidence.
- Cutoff design (how many days pre-print; which quarters) — receiver proposes; must be pre-registered per series before scoring.
- Whether Part-2 correspondence justifies a real (pre-registered, forward) backtest program — owner decision after the report.

## Superseded / Dangerous-To-Reuse Context

- "Sleipnir sells bounded one-decision memos / never a report factory" as settled product shape — Why dangerous: superseded by the owner's new-company reframe (2026-07-09/10); product shape is being re-derived elsewhere. Replacement: this probe is shape-agnostic; it tests data feasibility only.
- "The engine's existing longitudinal history is a usable head start" — Why dangerous: unverified; two sender-thread architects flagged it as a claim to check, not assume. Replacement: Part 1 inventories what actually exists/reconstructs.
- "Archive-reconstructable history = moat" — Why dangerous: inverts the moat capture's core rule. Replacement: Class B = backtest fuel only.

## Commands And Verification Evidence

- Sender ran no probe commands; there is no verification evidence to inherit. First receiver evidence targets: `git log -1 --oneline -- <this packet path>` (load contract), the source-loading ladder declarations, and per-venue scouting notes with dates. All probe scoring must be re-runnable from the receiver's recorded cutoffs and item lists.

## Blockers And Risks

- Venue reconstruction may be thinner than hoped (deletions, truncation, anti-bot on historical pages) — Evidence: unknown; the probe exists to measure it. Likely next action: record per-venue fidelity honestly, including failures.
- Lookahead leakage via undated/edited items — Evidence: known Class-B bias. Likely next action: exclusion rule per Frozen Decisions.
- Scope creep toward pipeline building — Evidence: standing temptation named in sender thread. Likely next action: stop condition in Exact Next Authorized Action step 6.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: this packet's commit (compare recipe in Load Contract); the moat capture doc (same branch/PR); the research engine map + CSB README boundaries on `origin/main`; safety-rules armory routing; the two owner quotes (this packet).
- Load outcomes: `REUSE` only after re-verifying the load-bearing sources; `STALE_REREAD_REQUIRED` if any drifted; `BLOCKED_MISSING_SOURCE`/`BLOCKED_UNVERIFIABLE` if a required read is unreachable (then request a pasted source capsule).
- Sources that MUST be reread on drift: research engine map; moat capture; safety-rules.

## Do Not Forget

- The probe's honest failure modes are findings, not failures: "cannot reconstruct at usable fidelity" and "signal does not correspond to outcomes" are both decision-grade answers the owner needs.
- This packet commissions evidence, not a product: resist framing Part-2 results as a track record — retrospective correspondence is in-sample fuel; the sellable record only accrues live and forward.
