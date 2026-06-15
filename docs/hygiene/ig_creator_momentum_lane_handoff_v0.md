---
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (durable continuation artifact; NOT validation/readiness/governance)
scope: Transfer the IG creator-momentum lane (discover → deep-capture → per-call curves) to a fresh thread after the 2026-06-15 wind-caller capture-cap doctrine propagation landed; remaining work is the storage/scale re-eval and the capture-shape contract.
use_when:
  - Continuing the IG creator-momentum lane cold (storage/scale decision A, then the capture-shape contract).
authority_boundary: retrieval_only
stale_if:
  - HEAD moves past the recorded compare-target blobs on the named targets (re-verify per the Load Contract before acting).
  - The storage/scale decision (A) or the capture-shape contract lands (update the open decisions and next actions).
---

# Handoff Packet — IG Creator-Momentum Lane

> **REFRESH 2026-06-15 (post-`c4cb7505`).** This packet was first drafted at HEAD `c365dca2`,
> when the owner's cap rulings were still **unrecorded**. They are now **recorded and propagated**:
> commit `c4cb7505` added the dated 2026-06-15 amendment + finalized `direction_change_propagation`
> receipt to the carve-out and propagated the new framing across 10 downstream surfaces.
> **Exact Next Authorized Action #1 (record the amendment) is therefore DONE** — the receiving lane
> starts at the storage/scale re-eval and the capture-shape contract. HEAD, compare-target blobs,
> the action list, the ledger, and the verify scaffold below are updated accordingly. The one
> remaining modified-uncommitted file on this branch is the ontology commission prompt (owner's
> parallel lane — intentionally not committed here).

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: `ig-cadence-rails` worktree (provenance only; not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\ig-cadence-rails`
- handoff_path: `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md`
- expected_branch: `ig-cadence-rails`
- expected_head: `c4cb7505` (cap-redefinition propagation; was `c365dca2` at first draft)
- expected_dirty_state_including_handoff_file: after this refresh is committed, the tracked tree carries **one** modified-uncommitted file — `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md` (owner's parallel ontology lane; intentionally not committed on this branch). This handoff is committed (tracked). Gitignored `orca-harness/_scratch/` (probes) + `orca-harness/_test_runs/` (raw capture) present, not committed.
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Build the Orca **creator-momentum** product — read creator momentum (follower trajectory, reel/video view-count curves, tier band-jumps) across a consumer vertical (beauty first; Instagram first, TikTok/YouTube later) as a demand / wind-caller signal.
- anchor_goal: Carry the IG capture satellite + the creator-momentum architecture from **feasibility-proven** to a **built, owner-adopted** pipeline. The immediate concrete object is the **capture-shape contract** (what each capture packet must preserve), but it is gated (see Open Decision).
- success_signal: A capture-shape contract spec'd with the AR-01 typed availability posture, the carve-out amendment recorded, and the architecture's scale/storage re-evaluated against the corrected roster size — so deep-capture can be built without baking a wrong, un-re-capturable lock-in.

## Open Decision / Fork

- **decision A — re-evaluate the architecture's storage/scale doctrine against the owner's cap correction (now recorded, `c4cb7505`).**
  - options: keep the flat-file/no-engine choice (if the per-vertical roster stays small) OR graduate to a real columnar/time-series store (if "all creators in a vertical" is large).
  - already constrained / off the table: packets remain the SOLE source of truth; the series stays a *rebuildable* derived index (no second source of truth, no stored tier/promotion state) regardless of which store.
  - trade-offs: flat-file is lowest-lock-in but caps scale; an engine is more infra (the architecture deliberately avoided it at the old `≤10`-tracked premise — now possibly wrong).
  - owner of the call: receiving lane proposes; owner adopts (it changes durable architecture doctrine).
  - recommendation: re-derive the real roster size for one beauty sub-niche first (how many creators is "all in the vertical"?), THEN pick the store — do not assume flat-file still holds.
- **decision B — reconcile the `≤10 capture/operating accounts` cap with logged-out capture.**
  - options: the cap binds only when sessions/accounts are actually used (e.g. for rate-spread or session-bypass), and logged-out capture (which uses no account) is uncapped on that axis; OR the cap is a hard footprint ceiling regardless.
  - owner of the call: owner (it's a posture/risk decision).
  - recommendation: confirm with owner; current capture is logged-out (no account), so the cap is presently non-binding — clarify when it would bind.

## Drift Guard

- **The `≤5`→`≤10` cap is OUR CAPTURE/OPERATING-ACCOUNT footprint, NOT a tracked-creator cap** (owner, 2026-06-15). Roster/tracking target = **ALL creators within the vertical**. Any doc or plan that reads `≤10` as "track only 10 creators" is **wrong** and must be corrected.
  - why it matters: it inverts the discovery goal (comprehensive roster, not 10) and breaks the architecture's scale premise.
  - what violating it would break: a discovery build capped at 10 creators; a storage sizing based on a false small-roster premise.
- **Logged-out capture only.** Never wire cookies/session into a *committed* runner without explicit owner go (session lane is retired for the proven signals).
- **Do NOT build A1** (recent-12-only capture) — superseded by deep-capture (full window over time).
- **Sub-niche coherence filter is GATING for discovery**, not polish — a single off-niche bridge node (e.g. `@Bible`, a real `jeremyfragrance` relation) poisoned the roster at depth-2. Interim keyword/cluster + bridge-prune; forward-named to ontology `SubNiche`.
- **Capture-shape contract must carry a typed availability posture per metric** (AR-01): absence/null/blocked must never be storable as an observed `0` (fake momentum; irreversible — history can't be re-captured).
- **DEFERRED by owner — do nothing:** the prompt-orchestration "receiver self-containment" gate (#14) overlay fix. Owner said observe whether the wasted-turn-on-prompt-out recurs before codifying. Do not draft or apply it unasked.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first, per `AGENTS.md`).
- targets to enter the ladder: the architecture doc, the discovery spec + recon, the consolidated IG findings, the carve-out, `models.py`, the ontology commission (paths in the ledger below).
- already loaded (weak orientation, freshness-marked 2026-06-15; not authority): all ledger files were read this session by the sender.
- must load first (before strict/actionable steps): the architecture doc + the carve-out + `models.py` (the capture-shape contract depends on all three).
- load rule: receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **The 3-capability pipeline** (discover → deep-capture → per-call curves), IG = first satellite, platform-agnostic derivation core deferred. Decided in: the architecture doc (ledger). Verify before strict use.
- **Storage/derivation doctrine**: packets = sole source of truth; projection = rebuildable index; tier/promotion = pure derivations (never stored state); typed fields canonical + parser=provenance; ontology coupling = adapter, not hard-bind. Decided in: the architecture doc. Verify before strict use.
- **Discovery is logged-out on the `web_profile_info` tolerant 200-cookieless surface** (same surface as calls/stats/reel-views). Decided in: the discovery recon + consolidated findings. Verify before strict use.
- **Tiers**: nano <10k / micro 10–100k / mid 100–500k / macro 500k–1M / mega 1M+; promotion = band-jump OR within-band velocity; rising = micro ~10k–100k. Decided in: the discovery spec.

## Active Objective

Advance the IG creator-momentum lane: the owner's carve-out corrections are **recorded + propagated** (`c4cb7505`); next, **re-evaluate the architecture's storage/scale premise against the corrected ("all in vertical") roster, then spec the capture-shape contract** — without building deep-capture until those gates clear.

## Exact Next Authorized Action

0. **DONE (`c4cb7505`, 2026-06-15) — do not redo.** The dated amendment to
   `docs/decisions/wind_caller_calibration_carveout_v0.md` is recorded (`≤10` = OUR
   capture/operating-account footprint, NOT a tracked-creator cap; roster = all creators in the
   vertical; active = attended / passive = bounded self-terminating; faster-than-human, not
   takedown-risking; ToS owner-accepted), with a finalized `direction_change_propagation` receipt,
   and propagated across 10 downstream surfaces. **Verify the carve-out blob = `6374cbbc…` before
   assuming it; do not re-amend.**
1. **Re-open the architecture's storage doctrine + scale math** (`orca_creator_momentum_pipeline_architecture_v0.md`, the "Storage doctrine" + AR-03 provisional note): re-derive the real roster size for one beauty sub-niche; decide flat-file vs engine; surface the proposed change for owner adoption (doctrine change → DCP receipt). *(Per the sender's precompact note this storage/scale re-eval may be one of the owner's own lanes — confirm ownership with the owner before opening it here.)*
2. **Then** spec the capture-shape contract (the smallest next build object), embedding the AR-01 typed availability posture. Stop condition: do NOT build deep-capture/runner until (1) lands and the capture-shape contract is owner-accepted.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read `README.md` first).
- Overlay authority: `.agents/workflow-overlay/{source-loading,prompt-orchestration,delegated-review-patch,artifact-folders,review-lanes,safety-rules}.md`.
- User constraints: see Drift Guard (the carve-out correction is the load-bearing one).
- Source-read ledger:
  - `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md`
    - Role: the target architecture (PROPOSED, cross-vendor-review-folded). Load-bearing: **yes**.
    - Compare target: git blob `ff24252e1b4b34e3e9c4ae3e9f7c1fb550e5d457` (committed at HEAD `c365dca2`).
    - Last checked: 2026-06-15. Reuse rule: reread before any capture-shape or storage decision.
  - `docs/decisions/wind_caller_calibration_carveout_v0.md`
    - Role: capture posture/cap authority. Load-bearing: **yes** — now carries the dated 2026-06-15 amendment (`≤10` = our operating/capture accounts; roster all-in-vertical; active/passive method) + finalized DCP receipt.
    - Compare target: git blob `6374cbbccb9b557edc9d1883c6df230208c3e0ce` (committed at `c4cb7505`).
    - Last checked: 2026-06-15. Reuse rule: reread; the `≤10`/all-in-vertical/method posture is now recorded — rely on the amendment, do NOT re-amend.
  - `docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md`
    - Role: discovery capability spec (mechanisms, sub-niche filter, tiers). Load-bearing: yes.
    - Compare target: git blob `8b93c5b77042a867bc14dd20d74af995529270a5` (committed at `c4cb7505`; propagation re-framed Posture + stale_if). Last checked: 2026-06-15. Reuse rule: reread for discovery work.
  - `docs/product/source_capture_toolbox/ig_creator_discovery_suggested_accounts_recon_v0.md`
    - Role: Phase-1+2 discovery recon (GO, evidence, caveats). Load-bearing: yes.
    - Compare target: git blob `d688e79f3e9472008697954a9e3abed135133d74`. Last checked: 2026-06-15. Reuse rule: reread for discovery work.
  - `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md`
    - Role: consolidated IG capture findings (the hub). Load-bearing: yes. Compare target: git blob `3d19093e190865616ffe3151b51c27075009680a` (committed at `c4cb7505`; propagation re-framed Residuals + Posture). Last checked: 2026-06-15.
  - `docs/product/source_capture_toolbox/capture_recon_index_v0.md`
    - Role: recon index (rows for calls/reel/discovery). Load-bearing: no (orientation). Compare target: `reread-required` (HEAD). Last checked: 2026-06-15.
  - `orca-harness/source_capture/models.py`
    - Role: `SourceCaptureSlice`/`PreservedFile` packet model — NO typed metric field today (the capture-shape gap). Load-bearing: **yes**. Compare target: git blob `303450e81e25b5f0ceaeff529862f2a8041091f3` (unchanged by `c4cb7505`; re-read to confirm no typed metric field still — not re-read this refresh). Last checked: 2026-06-15.
  - `docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`
    - Role: ontology commission (Observation/TrendVector/SubNiche candidate types; AWAITING_DISPATCH). Load-bearing: no (forward reference). Compare target: `reread-required`. Last checked: 2026-06-15.
- Source gaps: the real per-vertical roster size is un-measured (gates decision A).
- Strict-only blockers: the `≤10` cap + "all in vertical" + active/passive method posture are now **recorded** in the carve-out (2026-06-15 amendment, `c4cb7505`) — rely on the amendment; do not re-record. The remaining strict gate is the storage/scale re-eval (decision A) and the un-measured roster size.
- Not-proven boundaries: everything is **feasibility-proven**, not at-scale-validated; the architecture is PROPOSED, not owner-adopted; the cross-vendor review was **advisory**, not a formal verdict.

## Current Task State

- Completed: discovery capabilities 1 feasibility (Phase-1 reachability + Phase-2 snowball) PROVEN; the discovery spec, recons, and architecture doc written + committed; architecture hardened by a cross-vendor review (AR-01..05 adjudicated + folded).
- Partially completed: the architecture is PROPOSED, not adopted. (Owner rulings on the carve-out are now made AND recorded + propagated, `c4cb7505`.)
- Broken or uncertain: the architecture's storage/scale premise (assumed `≤10` *tracked* — now corrected to `≤10` *our accounts* + all-in-vertical); the capture-shape contract is un-spec'd.

## Workspace State

- Branch: `ig-cadence-rails`. Head: `c4cb7505` (was `c365dca2` at first draft).
- Dirty before this refresh: the propagation was committed (`c4cb7505`); the ontology commission prompt is modified-uncommitted (owner's parallel lane); this handoff was untracked.
- Dirty after this refresh is committed: the ontology commission prompt remains modified-uncommitted; this handoff is committed (tracked). Gitignored `_scratch/` + `_test_runs/` present.
- Target files: the architecture doc (for action 1) + the carve-out (now amended — read-only reference).
- Related: base `origin/main` @ `02e91e20` (the #101 reel-recon merge); branch is **ahead 5, behind 32** of `origin/main`. No PR yet. Local `origin/main` ref is stale (fetch + rebase onto current main before any PR — behind 32, expect to reconcile concurrent doc-lane edits).

## Changed / Inspected / Tested Files

- `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md` — Status: committed (c365dca2). Role: target architecture. Observations: storage/scale section needs re-eval (decision A). Sections: "Storage doctrine", "The capture-shape contract", "Cross-vendor review disposition".
- `docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md` + `_suggested_accounts_recon_v0.md` — Status: committed. Role: discovery capability + evidence.
- `orca-harness/source_capture/models.py` — Status: unchanged (read-only). Role: packet model; the missing typed metric field IS the capture-shape gap.

## Frozen Decisions

- Capture/derivation invariants (packets=truth; rebuildable projection; pure derivations; typed canonical; adapter-not-bind). Evidence: architecture doc + cross-vendor review. Consequence: any build must preserve these.
- Discovery is logged-out, single `web_profile_info` surface; sub-niche filter gating. Evidence: recon. Consequence: no session in committed runner; filter required.
- Owner cap-correction (≤10 = our accounts; all-in-vertical; faster-than-human; ToS-accepted). Evidence: owner, 2026-06-15. Consequence: actions 1–2.

## Mutable Questions

- How large is "all creators in one beauty sub-niche"? (Resolves decision A / store choice.) What would resolve it: a bounded discovery roster-size measurement.
- When does the `≤10 capture-account` cap bind given logged-out capture? (Resolves decision B.) What would resolve it: owner clarification.

## Superseded / Dangerous-To-Reuse Context

- **"`≤10` = tracked-creator cap"** (the architecture's + carve-out's prior reading). Why dangerous: inverts the roster goal and the scale premise. Replacement: `≤10` = OUR capture/operating accounts; roster = all-in-vertical (owner, 2026-06-15).
- **"human-paced" capture cadence** (carve-out doc). Why stale: amended. Replacement: attended, faster-than-human, tuned to not risk takedowns.
- **A1 (recent-12 capture)**. Why dangerous: superseded by deep-capture. Replacement: full-window deep-capture per the architecture.
- The architecture's **flat-file/no-engine storage choice** is **provisional** (AR-03) and rests on the now-corrected scale premise — re-evaluate, don't reuse as settled.

## Commands And Verification Evidence

- Lane state:
  ```bash
  git -C <workspace> rev-parse HEAD          # expect c4cb7505...
  git -C <workspace> log --oneline -5         # expect c4cb7505, c365dca2, fde8c3cf, 4a61ae65, c743999d
  git -C <workspace> status -s                # expect ` M docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md` (owner's lane) + clean otherwise
  git -C <workspace> hash-object docs/decisions/wind_caller_calibration_carveout_v0.md  # expect 6374cbbccb9b557edc9d1883c6df230208c3e0ce (amended)
  git -C <workspace> hash-object docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md  # expect ff24252e1b4b34e3e9c4ae3e9f7c1fb550e5d457 (unchanged)
  ```
  Result: re-computed at refresh time (2026-06-15, post-`c4cb7505`); re-run target so the receiver confirms rather than trusts.

## Blockers And Risks

- The carve-out corrections are now recorded + propagated (`c4cb7505`) — that blocker is cleared. Residual: the storage/scale premise may be wrong at the corrected roster size → don't build storage/deep-capture before decision A. Likely next action: measure roster size, re-eval.
- The storage/scale premise may be wrong at the corrected roster size → don't build storage/deep-capture before decision A. Likely next action: measure roster size, re-eval.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: HEAD = `c4cb7505`; only the ontology prompt is modified-uncommitted; the architecture doc blob = `ff24252e…` (unchanged); the carve-out blob = `6374cbbc…` AND that it now carries the 2026-06-15 amendment (the correction IS recorded — do not re-amend); `models.py` still has no typed metric field.
- Compare targets: the git blob hashes above (recompute with `git hash-object`); HEAD/ref for any `reread-required` entries.
- Load outcomes: `REUSE` only if all the above re-verify; `STALE_REREAD_REQUIRED` if HEAD/blobs drifted further (e.g. the lane advanced past `c4cb7505`, or a rebase onto current main rewrote blobs — then reread the carve-out + architecture doc); `BLOCKED_DRIFT` if the lane branch/commits differ from expected.
- Reread if drift: the architecture doc + the carve-out (the two the next actions mutate).

## Do Not Forget

- The `≤10` correction (our accounts, not tracked creators; all-in-vertical) is the single most load-bearing owner ruling — it reshapes discovery scope AND the storage doctrine.
- Capture-shape contract must carry the AR-01 typed availability posture; history cannot be re-captured.
