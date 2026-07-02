# Handoff Packet — creator registry lane continuation (foundation-first)

```yaml
retrieval_header_version: 1
artifact_role: cross_lane_handoff_packet
scope: >
  Cold cross-lane handoff to continue the creator registry lane foundation-first:
  harden the registry into a scalable, live-fed, formula-validated data engine and
  start sustained niche capture. A continuation artifact only — not validation,
  readiness, acceptance, or buyer proof.
use_when:
  - A fresh lane/thread picks up the creator registry work with no prior context.
  - Checking the ratified direction (foundation-first), open decisions, and drift guard.
open_next:
  - orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md
  - orca/product/spines/creator_signal/creator_signal_market_sizing_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
stale_if:
  - The receiver completes the confirm-don't-trust load and continues (packet becomes historical).
  - origin/main moves such that the source-ledger blob SHAs below no longer match (reread required).
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-01 (after PR #550 merged; architecture direction ratified + evolved)
- created_by_lane: Orca thread that ran the YT fold-in + the product-architecture/sizing/competitor strategy (provenance only, not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca` (Orca repo). External data lake is SEPARATE at `F:\orca-data-lake` (operator box, resolved via `ORCA_DATA_ROOT`); durable lake writes are owner-gated + operator-box-only.
- handoff_path: `docs/workflows/creator_registry_lane_continuation_handoff_v0.md`
- expected_branch: start a FRESH worktree/branch off `origin/main` (do NOT reuse the origin checkout, which sits on the unrelated stale branch `codex/ig-reels-capture-spine`).
- expected_head: `origin/main @ 5720b5bd` at write time. MOVES FAST — many active lanes merge; run `git fetch && git rev-parse --short origin/main` and re-verify before acting.
- expected_dirty_state_including_handoff_file: this packet + two edited product docs land via one PR (branch `claude/creator-signal-emv-fix-handoff`); once merged, the repo is clean on a fresh branch.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority. Glossary: IG=Instagram, YT=YouTube, WTP=willingness-to-pay, EMV=Earned Media Value (Tribe/CreatorIQ's metric), MIV=Media Impact Value (Launchmetrics' separate metric), ICP=ideal customer profile, "lake"=external data lake at `F:\orca-data-lake`.

## Goal Handoff

- long_term_goal: Turn the creator registry + Creator Signal surface into a proprietary, longitudinal, provenance-backed **vertical creator-intelligence data asset** (fragrance → beauty/skincare). The moat is the **evidence graph** (creator × brand × product × content × time × proof), NOT influencer software — incumbents copy screens faster than capture history.
- anchor_goal: **Foundation-first.** Harden the creator registry into a **scalable, live-fed, formula-validated data engine** ("our runs") and **start sustained niche capture** so the longitudinal time-series begins accruing. The customer-facing product + buyer/model choices are DEFERRED (how-to-sell questions; the registry is buyer-agnostic).
- success_signal: capture → registry runs **repeatably on LIVE captured data** (not just the committed review-input capture files); rollup formulas validated at scale; coverage/depth growing (esp. YT engagement + more creators); longitudinal snapshots accruing over time; lake-free unit suite green. **NOT success:** building a customer/Vetting UI, freezing a customer claim-contract schema, or editing the identity ledger.

## Open Decision / Fork

- decision: These are OWNER-owned and DEFERRED — do not silently resolve; they do not block the foundation work.
  - **Buyer**: niche/indie fragrance brands vs fragrance/beauty agencies. Options: (a) lead brands, (b) lead agencies, (c) test both. Off the table for now: committing before evidence. NEW fork to test: the primary buyer may be a **non-marketer evidence buyer** (investor / retail / procurement / legal), who values provenance more than a marketer. Trade-off: buyer choice shapes product/pricing/sales but NOT the data foundation. Owner: Eric. Recommendation: test both + the non-marketer angle in a later proof step; keep building buyer-agnostic now.
  - **Delivery model**: SaaS vs consulting/decision-driven. Recommendation: likely consulting-led early (monetize + learn while data matures) → productize to SaaS. Deferred.
  - **Customer claim-contract schema**: do NOT freeze a durable versioned external schema pre-evidence (a thin, disposable sanitizing projection is fine/needed). Owner: Eric.

## Drift Guard

- **Do NOT build the customer-facing product / Vetting UI now.** Data is too thin (33 shallow profiles); foundation-first. Why it matters: a customer probe on hollow data yields a confounded signal.
- **Do NOT freeze a durable external "claim-object" contract pre-evidence.** The `F:\` sanitization forces a thin disposable projection (fine); the versioned schema is a product bet to defer. Why: premature lock-in on an unvalidated interface.
- **Do NOT attempt head-on displacement of CreatorIQ/Tribe.** Win the flank they ignore (indie/DTC + specialist agencies + non-marketer buyers); coexist / possibly be-acquired. Why: they are a well-capitalized enterprise incumbent, not fragile.
- **Identity ledger stays FENCED** (`creator_public_handle_linkage_ledger_v0.json` — handles/channel ids); do not derive identity from metrics.
- **CI stays lake-free** (`env -u ORCA_DATA_ROOT python -m pytest tests/unit/ -q` from `orca-harness/`); no CI path resolves the real lake.
- **Durable `F:\orca-data-lake` writes are owner-gated + operator-box-only.**
- **No-drift bridge is VALUE-equal, not byte-equal**; **no scheduler at v0** (freshness on-demand via the gate).
- **Do NOT conflate EMV (Tribe/CreatorIQ) with MIV (Launchmetrics).**

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `repo-overlay-bound` — read `AGENTS.md` + `.agents/workflow-overlay/README.md` first; PR/branch-protection flow is `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.
- targets to enter the ladder: the source-read ledger below (2 creator_signal product docs + registry specs/code/runners).
- already loaded (weak orientation, freshness-marked; not authority): the sender authored/read all of these while running the lane; treat as orientation only.
- must load first (before strict/actionable steps): `creator_signal_product_architecture_v0.md` — specifically its **"## Direction Update v0.1"** section, which is the AUTHORITATIVE current direction and **wins over the doc's earlier sections on conflict**.
- load rule: re-run progressive source loading per the overlay; this loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- **Ratified product direction + Direction Update v0.1**: foundation-first; moat = longitudinal evidence graph; wedge = fragrance → beauty; compete on the flank vs CreatorIQ/Tribe; adversarial-review corrections accepted (don't-freeze-claim-contract, WTP-is-hypothesis, provenance-UX-undesigned, verdict-must-reflect-all-gaps).
  - decided in: `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md`
  - compare target: reread at current `origin/main` HEAD (this handoff's PR updates it; `origin/main` pre-edit blob was `7bfe79ce`).
  - verify before: any strict/actionable direction claim.
- **Market sizing + competitor landscape + EMV/MIV correction**: fragrance ≈ small business alone; beauty makes it Series-A-plausible (~$5M ARR base Yr3); reachable ICP SAM ≈ $100M (not the $2B headline); competitor to design against = CreatorIQ/Tribe (Tribe = EMV; MIV = Launchmetrics).
  - decided in: `orca/product/spines/creator_signal/creator_signal_market_sizing_v0.md`
  - compare target: reread at current HEAD (this PR updates it; pre-edit blob `63dd10ad`).
- **YT fold-in cut-over architecture** (§1–§8, AR-01..AR-07): the migration that made the registry lake-fed; now complete.
  - decided in: `.../creator_registry/creator_profile_current_lake_cutover_architecture_v0.md` (blob `6cab351a` @ origin/main).

## Active Objective

Scope and execute the **"registry as a scalable, live-fed, formula-validated data engine"** step: make capture → registry repeatable on LIVE data (beyond the committed review-input captures), validate the rollup formulas at scale, grow coverage/depth (esp. YT engagement + more creators), and start the longitudinal capture clock. This is **data-engineering, not product**.

## Exact Next Authorized Action

1. `git fetch`; re-verify `origin/main` HEAD; read `creator_signal_product_architecture_v0.md` (esp. **Direction Update v0.1**) + `creator_signal_market_sizing_v0.md` at current HEAD.
2. Re-read the registry pipeline (materialize.py, silver_metric_reader.py, silver_metric_snapshot.py, the producer + snapshot + freshness runners) to map what "live-fed, repeatable, scalable" requires vs today's genesis-from-committed-captures path.
3. Produce a scoping plan (read-only) for the data-engine hardening: live capture ingestion, formula-at-scale validation, coverage/depth growth, longitudinal accrual. Then implement via per-lane PR off `origin/main`; lake-free CI green; owner-gated real-lake writes.
4. Stop condition / validation: `env -u ORCA_DATA_ROOT python -m pytest tests/unit/ -q` (from `orca-harness/`) green; open PR; STOP (owner review is the gate; no customer-product build).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/README.md`. PR flow: `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.
- Overlay or equivalent authority: Orca repo overlay (`repo-overlay-bound`).
- User constraints: see Drift Guard.
- Source-read ledger (blob SHAs @ `origin/main 5720b5bd`; MOVES — reread at current HEAD):
  - `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md` — Role: ratified direction + Direction Update v0.1 (authoritative). Load-bearing: yes. Compare target: reread at current HEAD (updated in this PR; pre-edit `7bfe79ce`). Reuse rule: Direction Update v0.1 wins on conflict.
  - `orca/product/spines/creator_signal/creator_signal_market_sizing_v0.md` — Role: sizing + competitor landscape + EMV/MIV. Load-bearing: yes. Compare target: reread at current HEAD (updated in this PR; pre-edit `63dd10ad`).
  - `.../creator_registry/creator_profile_current_view_spec_v0.md` — Role: view contract. Load-bearing: yes. Compare target: `72368b85`.
  - `.../creator_registry/creator_public_handle_linkage_ledger_spec_v0.md` — Role: identity ledger (FENCED). Load-bearing: yes. Compare target: `94100a66`.
  - `.../creator_registry/README.md` — Role: registry folder front door. Load-bearing: no. Compare target: `8db0ecc2`.
  - `.../creator_registry/creator_profile_current_lake_cutover_architecture_v0.md` — Role: the (complete) lake cut-over architecture. Load-bearing: yes. Compare target: `6cab351a`.
  - `orca-harness/capture_spine/creator_profile_current/materialize.py` — Role: builds the view from rollups. Load-bearing: yes. Compare target: `4eb0f91e`.
  - `orca-harness/capture_spine/creator_profile_current/validation.py` — Role: view validator (posture coupling, promoted-link gating, `surface_handling`). Load-bearing: yes. Compare target: `70a1caa6`.
  - `orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py` — Role: rollup discovery + latest-per-account selection. Load-bearing: yes. Compare target: `18f041f4`.
  - `orca-harness/capture_spine/creator_profile_current/silver_metric_snapshot.py` — Role: snapshot generator. Load-bearing: yes. Compare target: `683a98f4`.
  - `orca-harness/runners/run_creator_profile_current_materialize.py` — Role: view build runner (`--write`/`--check`). Load-bearing: yes. Compare target: `c3fb58d3`.
  - `orca-harness/runners/run_creator_metric_rollup_snapshot.py` — Role: snapshot mint runner. Load-bearing: yes. Compare target: `23d8eb04`.
  - `orca-harness/runners/run_live_lake_freshness_gate.py` — Role: on-demand freshness gate. Load-bearing: yes. Compare target: `8e6cc0c4`.
  - `orca-harness/runners/run_youtube_creator_metric_rollup_producer.py` — Role: capture-fed YT producer. Load-bearing: yes. Compare target: `8c90b457`.
- Source gaps: none known.
- Strict-only blockers: durable lake writes need `ORCA_DATA_ROOT=F:\orca-data-lake` + owner authorization (not on CI / a fresh box).
- Not-proven boundaries: registry is a static lake-verifiable read model, not a runtime service; demand/WTP is UNVALIDATED (zero buyer proof); the moat is a destination, not the current thin state.

## Current Task State

- Completed (merged to main): the whole YouTube fold-in (§8, PRs #539/#541/#543/#544); IG cut-over (§4–§6); product-architecture direction ratified (#550) + evolved by Direction Update v0.1; adversarial review + sizing + competitor teardown incorporated.
- Partially completed: the registry is lake-fed but **genesis-from-committed-captures**, manual single-operator refresh — NOT yet a live-fed, repeatable, scalable data engine. Data is thin (33 profiles, 30 YT view-only, 3 IG engagement, 0 creator_records).
- Broken or uncertain: none known.

## Workspace State

- Branch: this packet is authored on `claude/creator-signal-emv-fix-handoff` (off `origin/main 5720b5bd`); the receiver should start its OWN fresh worktree/branch off `origin/main`.
- Head: `origin/main @ 5720b5bd` at write time (re-fetch; moves fast).
- Dirty before handoff: 2 modified product docs (arch + sizing memo — the EMV fix + Direction Update v0.1).
- Dirty after writing the handoff file: + this new file. All three land via one PR.
- Target files or artifacts: (this lane) the two edited docs + this handoff; (next lane) the registry pipeline code + runners above.
- Related worktrees or branches: the origin checkout is on unrelated stale `codex/ig-reels-capture-spine` (do NOT reuse). Many other active lanes exist (main moves fast).

## Changed / Inspected / Tested Files

- `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md` — Status: MODIFIED (this PR). Role: added "Direction Update v0.1" (foundation-first + moat + competitor + accepted review findings); Status → RATIFIED + evolved.
- `orca/product/spines/creator_signal/creator_signal_market_sizing_v0.md` — Status: MODIFIED (this PR). Role: EMV/MIV correction; competitor table expanded (Traackr, Launchmetrics, Sprout/Tagger, Meltwater/Klear); competitive-posture section added.
- `docs/workflows/creator_registry_lane_continuation_handoff_v0.md` — Status: NEW (this file).

## Frozen Decisions

- Foundation-first (build the data engine before the customer product). Evidence: Direction Update v0.1 §1. Consequence: near-term is data-engineering, not product.
- Moat = proprietary longitudinal vertical evidence graph. Evidence: competitor teardown + Direction Update v0.1 §2. Consequence: start the capture clock now; compete on the flank.
- Fragrance = wedge, beauty/skincare = destination. Evidence: sizing memo. Consequence: plan around the beauty market, not fragrance alone.
- Do NOT freeze the customer claim-contract now. Evidence: adversarial-review AR-02. Consequence: thin disposable projection only.
- No-drift = value-equal not byte-equal; identity fenced; no scheduler v0. Evidence: lake cut-over architecture + view spec.

## Mutable Questions

- Which buyer (brands / agencies / non-marketer evidence buyer)? Resolves on: a later proof step with real prospects.
- SaaS vs consulting-led delivery? Resolves on: early monetization/learning evidence.

## Superseded / Dangerous-To-Reuse Context

- The architecture doc's original "**Vetting v0 is the first build**" thrust (Vetting v0 + Staged path sections) — SUPERSEDED by Direction Update v0.1 (foundation-first). Replacement: build the data engine first.
- "High-lock-in decision #1: freeze the customer claim contract now" — SUPERSEDED (AR-02). Replacement: thin disposable projection; defer the durable schema.
- "Tribe Dynamics MIV" (in the pre-fix sizing memo) — WRONG. Tribe = **EMV**; **MIV = Launchmetrics** (separate competitor). Corrected in this PR.

## Commands And Verification Evidence

- Lake-free unit suite (matches CI), from `orca-harness/`:
  ```bash
  env -u ORCA_DATA_ROOT python -m pytest tests/unit/ -q
  ```
  Result: green at last run (pre-handoff). Re-run target: after any code change.
- Freshness gate (operator box only): `python -m runners.run_live_lake_freshness_gate --platform youtube` → FRESH.
- View staleness check: `python -m runners.run_creator_profile_current_materialize --check`.

## Blockers And Risks

- Thin data caps everything downstream; the near-term job is precisely to fix that (live capture + coverage/depth). Likely next action: scope the data-engine hardening.
- Live capture → registry is not yet wired (genesis-from-committed-captures only). Likely next action: design the live ingestion path.
- Demand/WTP unvalidated (zero buyer proof) — but that is a LATER (proof) concern, not a foundation blocker.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify before acting:
  - `origin/main` HEAD → `git fetch && git rev-parse --short origin/main` (was 5720b5bd; moves).
  - The two creator_signal docs at current HEAD → read Direction Update v0.1 (authoritative) + the sizing memo.
  - The registry code/runner blob SHAs above → compare; reread on mismatch.
  - Lake-free suite green → re-run the pytest command.
- Load outcomes: `REUSE` (all verified → proceed from Exact Next Authorized Action); `STALE_REREAD_REQUIRED` (main moved / a blob changed → reread, esp. the architecture doc + Direction Update v0.1); `BLOCKED_DRIFT` (a frozen decision reversed, or the foundation-first direction changed → reorient with the owner).
- Sources to reread if drift detected: `creator_signal_product_architecture_v0.md` (Direction Update v0.1), `materialize.py`, `silver_metric_reader.py`.

## Do Not Forget

- Foundation-first: build the live-fed registry data engine; do NOT build the customer product yet.
- Do NOT freeze the customer claim contract; do NOT edit the fenced identity ledger; durable lake writes are owner-gated.
- EMV (Tribe/CreatorIQ) ≠ MIV (Launchmetrics).
- The moat is capture history — **start the longitudinal clock now**; it can't be recreated later.
