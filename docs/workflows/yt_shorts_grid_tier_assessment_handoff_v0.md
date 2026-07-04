# Handoff Packet — YT Shorts grid-tier capture assessment (two-tier daily cadence direction)

```yaml
retrieval_header_version: 1
artifact_role: cross_lane_handoff_packet
scope: >
  Cold cross-lane handoff commissioning an ASSESSMENT (not an implementation) of
  the YouTube Shorts channel grid as the cheap daily capture tier for the
  creator registry, compared against what the IG /reels/ grid and TikTok profile
  grid expose. A continuation artifact only — not validation, readiness, or
  acceptance.
use_when:
  - A fresh lane picks up the grid-tier assessment with no prior context.
  - Checking the owner's 2026-07-02 two-tier daily-cadence direction verbatim.
stale_if:
  - The receiver completes the confirm-don't-trust load and lands the assessment
    (packet becomes consumed history).
  - origin/main moves such that the source-ledger blob SHAs below no longer match.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-02 (after PRs #595, #581, #602 merged)
- created_by_lane: creator-registry cycle-1 lane (provenance only, not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca` (Orca repo). External data lake SEPARATE at `F:\orca-data-lake` (operator box, `ORCA_DATA_ROOT`); durable lake writes owner-gated + operator-box-only.
- handoff_path: `docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md`
- expected_branch: start a FRESH worktree/branch off `origin/main`.
- expected_head: `origin/main @ cf43db5f` at write time. MOVES FAST — `git fetch && git rev-parse --short origin/main` and re-verify before acting.
- expected_dirty_state_including_handoff_file: this packet lands via its own lane PR; once merged, a fresh receiver branch is clean.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority. Glossary: IG=Instagram, TT=TikTok, "grid"=a channel/profile listing surface showing many content tiles at once (cheap, one page ≈ whole roster item), "deep capture"=per-content page fetch (expensive, full metrics), "lake"=`F:\orca-data-lake`.

## Goal Handoff

- long_term_goal: >
    Proprietary, longitudinal, provenance-backed vertical creator-intelligence
    data asset (fragrance -> beauty); moat = the evidence graph accrued as
    capture history.
- anchor_goal: >
    The creator registry running as a scalable, live-fed, formula-validated
    data engine with sustained capture accruing longitudinal history on the
    real lake.
- success_signal (core, verbatim from the active goal frame): owner-observable =
  real-lake recapture cycles repeating (run-ids advancing, freshness receipts
  refreshing, revalidation green over growing history); output_fit = every next
  output makes capture->registry more repeatable, verifiable, or broader/deeper
  on live data; boundary = test-lake proofs or more code alone do not count, no
  customer-facing work counts; drift_cue = product/UI/claim-contract/scheduler
  work appearing before sustained capture.

## Open Decision / Fork

- decision: what shape the daily grid tier should take per platform — the
  assessment's RECOMMENDATION feeds it; the receiver does not resolve it.
  - options: (a) YT grid tier is views-only (grid exposes view counts only) and
    spike-triggers deep watch-packet capture; (b) YT grid is engagement-bearing
    like IG/TT grids may be (likes/comments on the surface) and the tier carries
    more; (c) YT grid route is unusable logged-out and daily YT stays
    watch-packet-based (costlier).
  - already constrained / off the table: spike thresholds are an OWNER product
    parameter (do not decide); scheduler build is out of scope (no-scheduler v0
    doctrine stands until the owner revisits it); no registry pipeline changes
    in this lane.
  - trade-offs: views-only grid is cheap and probably sufficient for YT spike
    detection (owner direction names view spike as the YT trigger);
    engagement-bearing grids would let IG/TT spike rules fire on likes/comments
    per the owner direction.
  - owner of the call: Eric (after the assessment receipt).
  - recommendation: none yet — that is the deliverable.

## Drift Guard

- **Assessment, not implementation.** No grid-tier producer, no registry
  pipeline changes, no new Silver lanes, no scheduler. Why: build-before-
  assessment is the exact failure this commission exists to avoid.
- **No ledger edits.** The linkage ledger (identity) and the YT observation
  ledger (admitted pool) are read-only inputs. Why: identity stays fenced;
  admission is owner governance.
- **No spike-threshold decision.** Owner product parameter. Why: premature
  lock-in on an owner-owned knob.
- **Bounded, paced live probes only.** A few roster channels, polite pacing
  (~10-15s), stop on block signals. Probe captures may commit to the lake
  (owner direction 2026-07-02 authorizes assessment probes); a full-roster
  sweep is NOT this lane's job. Why: ToS-restricted surface; blocking risk.
- **No TikTok roster additions.** TT comparison is a code/artifact read (its
  capture spine exists); the registry has zero TT accounts and this lane adds
  none.
- **CI stays lake-free** (`env -u ORCA_DATA_ROOT python -m pytest tests/unit/ -q`
  from `orca-harness/`) — relevant only if the receiver touches code, which it
  should not.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `repo-overlay-bound` — read `AGENTS.md` +
  `.agents/workflow-overlay/README.md` first; artifact placement rules in
  `.agents/workflow-overlay/artifact-folders.md`; PR flow in
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.
- targets to enter the ladder: the source-read ledger below (grid capture
  modules for all three platforms + the roster ledger).
- already loaded (weak orientation, freshness-marked; not authority): the
  sender verified the named files exist at `origin/main cf43db5f` on
  2026-07-02; the sender has NOT read the grid modules' internals — field-level
  claims about what each grid exposes are deliberately absent here.
- must load first (before strict/actionable steps): the three grid capture
  modules named in the ledger, then the owner direction quote below.
- load rule: re-run progressive source loading per the overlay; this loaded-set
  only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- **Owner two-tier daily-cadence direction (2026-07-02), verbatim:** "daily is
  better, but thats acutally daily grid capture , only go to reel if theres a
  view / like / comment spike (for ig and tt) and view spike for yt shorts".
  - decided in: owner chat direction to the creator-registry lane, 2026-07-02
    (this quote is the primary record; no doctrine file carries it yet).
  - compare target: quoted verbatim above (`reread-required` only if the owner
    restates it).
  - verify before: framing the assessment questions.
- **Foundation-first direction (ratified):** registry = data engine first; no
  customer product; Direction Update v0.1 wins over earlier sections.
  - decided in: `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md`
  - compare target: blob `be66df59` @ `origin/main cf43db5f`.
- **No scheduler at v0; the scheduled drift check is a NAMED upgrade trigger** in
  the same architecture doc — daily cadence pressure makes this an owner fork,
  not a receiver decision.
- **Cycle-1 landed state:** the registry is live-fed from watch packets
  (deep tier); snapshot run_id 2; PRs #595 (cycle-1 refresh + exclusions),
  #581 (batch sweep wrapper), #602 (capture classifier fix) all MERGED
  2026-07-02.
  - compare target: `git log origin/main --oneline` shows the three merges;
    receipt `selection_run_id: 2` in
    `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_freshness_receipt_v0.json`.
- **IG is already grid-fed:** the registry's IG metrics derive from `/reels/`
  grid captures (grid → projection → producer). YT is watch-packet-fed (deep
  only). This asymmetry is exactly what the assessment maps.

## Active Objective

Assess whether the YouTube Shorts channel grid (`youtube.com/@handle/shorts`)
can serve as the cheap DAILY capture tier the owner directed: determine
empirically what per-video fields it exposes logged-out (views expected;
like/comment presence must be verified, not assumed), compare against what the
IG `/reels/` grid and TikTok profile grid expose in our existing capture paths,
and prove per-video VIEW capture from the YT grid on a bounded roster probe.
Deliverable: an assessment receipt document + a grid-tier recommendation. No
implementation.

## Exact Next Authorized Action

1. `git fetch`; re-verify `origin/main`; fresh branch. Read the three grid
   modules in the ledger below (YT shorts scroll, IG reels grid, TT video/batch
   capture) and record what fields each SURFACE exposes per tile according to
   the code and any committed capture artifacts.
2. Bounded live probe (owner-authorized): run or adapt
   `orca-harness/youtube_capture/shorts_scroll_capture_v0.py` against 2-3
   admitted roster channels (channel ids in the linkage ledger below), polite
   pacing, stop on block signals. Record per-tile fields actually observed
   (views? likes? comments? publish recency?) and whether the route still works
   logged-out.
3. Write the assessment receipt:
   `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_grid_tier_assessment_v0.md`
   (co-located with YT capture docs; confirm placement against
   `.agents/workflow-overlay/artifact-folders.md` and adjust there if the
   overlay says otherwise). Contents: observed per-platform grid fields
   (YT probed; IG/TT from code+artifacts), route viability, per-video view
   capture proof for YT, gaps, and a recommendation on grid-tier producer shape
   (views-only vs engagement-bearing vs unusable).
4. Land via lane branch + PR off `origin/main` (`git push -u origin <lane>` is
   the allowed explicit push). Stop condition: PR open = owner review gate.
   If code was touched (it should not be): lake-free suite must be green first.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/README.md`.
- Overlay or equivalent authority: Orca repo overlay (`repo-overlay-bound`).
- User constraints: see Drift Guard.
- Source-read ledger (blob SHAs @ `origin/main cf43db5f`; MOVES — reread at current HEAD):
  - `orca-harness/youtube_capture/shorts_scroll_capture_v0.py` — Role: the
    existing YT Shorts grid-scroll capture route (the probe vehicle).
    Load-bearing: yes. Compare target: `a80bf567`. Last checked: 2026-07-02.
    Reuse rule: read before probing; sender has not verified it still works.
  - `orca-harness/source_capture/ig_reels_grid_capture.py` — Role: IG grid
    capture (the comparison baseline; what IG tiles expose). Load-bearing: yes.
    Compare target: `51f18fab`. Last checked: 2026-07-02.
  - `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py` — Role:
    IG grid capture runner (default IG route). Load-bearing: yes. Compare
    target: `339f18d8`. Last checked: 2026-07-02.
  - `orca-harness/runners/run_source_capture_tiktok_video_packet.py` — Role: TT
    capture entry point (TT comparison is code-read only). Load-bearing: yes.
    Compare target: `e0c10ad7`. Last checked: 2026-07-02.
  - `orca-harness/runners/run_source_capture_youtube_watch_batch.py` — Role:
    the deep-tier sweep runner (pacing/circuit-break pattern to mirror for any
    probe loop). Load-bearing: no. Compare target: `c64de36f`.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`
    — Role: roster (YT channel ids for the probe). READ-ONLY (identity fenced).
    Load-bearing: yes. Compare target: `e8d35b5c`. Last checked: 2026-07-02.
  - `orca/product/spines/creator_signal/creator_signal_product_architecture_v0.md`
    — Role: foundation-first direction + no-scheduler upgrade trigger.
    Load-bearing: yes. Compare target: `be66df59`.
- Source gaps: the sender has NOT read any grid module's internals; nothing in
  this packet asserts what any grid exposes — that is the assessment.
- Strict-only blockers: live probe needs `ORCA_DATA_ROOT` + operator box; a
  fresh box without the lake can still do the code-read half.
- Not-proven boundaries: no claim that the YT grid route works today, that
  grids expose engagement anywhere, or that daily cadence is operationally
  settled (scheduler fork is owner-owned).

## Current Task State

- Completed (merged to main): deep-tier live loop end-to-end (capture sweep →
  producer → snapshot run 2 → view → revalidation), operator exclusions,
  classifier fix (#595/#581/#602).
- Partially completed: cadence direction accepted (owner, 2026-07-02) but the
  daily grid tier is unassessed — this lane.
- Broken or uncertain: none known in scope.

## Workspace State

- Branch: packet authored on `claude/yt-grid-tier-assessment-handoff` off
  `origin/main cf43db5f`; receiver starts its OWN fresh worktree/branch.
- Dirty before handoff: clean; after writing: this file only (lands via its PR).
- Target files or artifacts: (this lane) this packet; (receiver) the assessment
  receipt doc + possibly probe capture packets in the lake.
- Related worktrees or branches: many active lanes; main moves fast.

## Changed / Inspected / Tested Files

- `docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md` — Status: NEW (this file).

## Frozen Decisions

- Two-tier capture direction (daily grid + spike-triggered deep). Evidence:
  owner quote above. Consequence: the assessment frames everything as
  tier-1-cheap vs tier-2-deep.
- Foundation-first / no customer product. Evidence: Direction Update v0.1.
- Deep tier stays watch-packet-based and already works; this lane does not
  touch it.

## Mutable Questions

- Does the YT Shorts grid expose anything beyond views per tile? Resolves on:
  the probe.
- Do IG/TT grids expose likes/comments (enabling their richer spike rule)?
  Resolves on: code/artifact read (+ existing IG captures).
- Scheduler doctrine for daily cadence? Resolves on: owner fork AFTER the
  assessment (do not resolve).

## Superseded / Dangerous-To-Reuse Context

- "Weekly watch-packet sweep as the standing cadence" (sender's earlier
  recommendation) — SUPERSEDED by the owner's 2026-07-02 daily two-tier
  direction. Replacement: daily grid tier assessed here; deep tier becomes
  spike-triggered.

## Commands And Verification Evidence

- Lake-free unit suite (only if code is touched, which is out of scope):
  ```bash
  env -u ORCA_DATA_ROOT python -m pytest tests/unit/ -q
  ```
  Result: green at sender's last run (2026-07-02, post-#595). Re-run target:
  after any code change.
- Probe pacing reference: the deep-tier sweep ran 196 videos at ~15s pacing on
  2026-07-02 without blocking (evidence: lake watch packets 09:12-10:01Z).

## Blockers And Risks

- YT grid may render via JS/continuation such that logged-out HTML carries few
  tiles — probe must record how many tiles per fetch and whether scrolling
  (continuation requests) is needed. Likely next action if severe: note it and
  recommend accordingly; do not build workarounds.
- Grid view counts are typically ROUNDED display text ("1.2M views") — record
  exactness per platform; approximate-count posture is an owner decision to
  surface, not resolve.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts to re-verify: `origin/main` HEAD; the 7 ledger blob SHAs;
  the three merged PRs (#595/#581/#602) visible in `git log origin/main`;
  receipt `selection_run_id: 2`.
- Load outcomes: `REUSE` (all verified → proceed from Exact Next Authorized
  Action); `STALE_REREAD_REQUIRED` (main moved / blob changed → reread the
  changed source); `BLOCKED_DRIFT` (two-tier direction reversed or deep-tier
  pipeline changed under this packet → reorient with the owner).
- Sources to reread on drift: the architecture doc; the grid modules.

## Do Not Forget

- This lane ASSESSES; it does not build the grid tier, the spike rule, or the
  scheduler.
- Grid view counts may be rounded — record exactness honestly; never zero-fill
  or precision-inflate.
- The probe is bounded and paced; a block signal ends it, loudly.
