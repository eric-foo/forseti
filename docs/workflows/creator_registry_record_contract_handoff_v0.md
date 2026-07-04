# Handoff Packet — Creator Registry Per-Creator Record Contract

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet
scope: Cold-reader handoff to pin the creator registry per-creator record contract (field set + consumer contract) and rule the current-window-vs-global-stats fork; explain-first before pinning.
use_when:
  - Continuing the creator-registry record-contract design in a fresh thread.
  - Deciding what key info and computed stats the per-creator registry record stores and what a consumer is promised.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-03
- created_by_lane: creator-registry stewardship thread (provenance only; not an authority claim)
- workspace: the Orca repository (this is a git worktree of it); external data lake `F:\orca-data-lake` is NOT needed for this task
- handoff_path: docs/workflows/creator_registry_record_contract_handoff_v0.md
- expected_branch: claude/registry-record-contract-handoff (the branch this packet is committed on); receiver may work from a fresh branch off origin/main
- expected_head: origin/main was cdc542c2 when this packet was written
- expected_dirty_state_including_handoff_file: this packet is the only add on its branch; once committed the tree is clean
- load_rule: confirm-don't-trust; re-verify every load-bearing fact below against its compare target before acting; the sender's claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: A live, self-sustaining creator-metric registry a downstream consumer (creator vetting, ranking, outreach) can trust — one current record per creator holding key identity info + computed stats, honestly posture-coupled (observed⇔a numeric value; not-observed⇔null + a reason; never zero-filled), across the platforms Orca can reliably capture, refreshed each capture.
- anchor_goal: Pin the creator registry's **per-creator record contract** — the full key-info + computed-stats field set the registry stores and refreshes each capture — and confirm the record's computation and update-from-Silver semantics are solid. This is a design pass over the EXISTING committed read model; it needs no new capture.
- success_signal: A downstream reader can open one creator's record and find every key field it needs — identity, current computed stats, and whatever cross-capture "global" stats the owner rules in — each field honestly posture-coupled and traceable back to its Silver source. The contract states, per field, what a consumer is promised.

## Open Decision / Fork  (receiver must EXPLAIN this to the owner and get a ruling BEFORE pinning the contract)

- decision: Does the per-creator record contract include only **current-window stats**, or also **global cross-capture stats**?
  - Concretely: the committed view already carries two computed-stat fields that are declared `not_attempted` today — `posting_cadence` and `recent_velocity` (verify: `metric_rollups` block in `creator_profile_current_view_v0.json`). They are placeholders for cross-capture / momentum stats. The fork decides their fate.
  - options:
    - **(A) Current-window only.** The record stores the latest capture cycle's rollup per creator (average/median views, average like/comment counts, engagement rate). `posting_cadence`/`recent_velocity` stay honest `not_attempted` stubs. Smaller, ships as-is, no cross-capture computation.
    - **(B) Also global cross-capture stats.** Additionally compute per-creator aggregates ACROSS the whole Silver longitudinal history each capture (e.g. posting cadence, recent velocity / momentum, trend), filling the two stubs. Richer record; momentum/velocity is arguably the highest-signal metric for creator vetting.
    - **(C, sender's recommendation) Both, staged.** Pin the current-window fields as the v0 contract floor NOW, and *specify* the global-stats fields as named, declared-deferred extensions (each stub keeps `not_attempted` but with a concrete named recipe and the input it awaits), rather than either dropping them or building them before enough history exists.
  - already constrained / off the table: cadence and scale are NOT in scope (they belong to the Silver lake / capture spine — see Drift Guard); no new capture is run for this task; the identity ledger is fenced (read-only); TikTok data is parked.
  - trade-offs: (A) is smallest but a consumer wanting momentum/trend gets nulls. (B) is richest but cross-capture aggregation needs ≥2+ cycles of Silver history to be meaningful and leans on the Silver longitudinal read (a Silver concern) — building it before history exists is premature. (C) captures B's value as a committed intention without forcing the cross-capture build prematurely, at the cost of shipping a partially-declared-deferred contract.
  - owner of the call: the human owner, in the new thread. The receiver EXPLAINS the two steps + the fork with trade-offs, then STOPS for the ruling before writing the contract.
  - recommendation and why: (C). The registry's value is a trustworthy current picture per creator; momentum/velocity is high-signal for vetting (argues for B), but cross-capture stats depend on longitudinal history that accrues on the Silver side over cycles (argues against building now). Staging — pin current-window now, spec the global-stats fields as declared-deferred — banks the value and keeps the record honest.

## Drift Guard

- **Cadence and scale are NOT registry concerns.** They belong to the Silver data lake / capture spine (how often data is captured; how many creators; the O(history) discovery scaling cliff). The owner explicitly corrected the sender on this. Do not scope cadence or scale into the registry record contract.
  - why it matters: the sender's prior goal frame wrongly imported these; the registry is a read model (current state per creator), not a pipeline. Violating this re-muddles the layer boundary the owner just sharpened.
- **TikTok data is parked.** The TikTok metric-pipeline CODE exists (branch `claude/tiktok-silver-pipeline`, PR #622 — verify its merge state) but there is NO TikTok data, and live TikTok capture is blocked by TikTok login bot-detection + Chrome App-Bound-Encryption (detection-evasion was explicitly declined). Do not treat TikTok as a live platform in the record contract; the contract covers the platforms with real data (Instagram, YouTube).
- **The identity linkage ledger is FENCED — read-only.** File: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`. The record contract must not propose writing identity or inferring cross-platform linkage; identity additions are a separate owner-gated lane.
- **No capture, no lake writes for this task.** This is a schema/contract design pass over the committed read model. Do not run captures, producers, snapshots, or any `F:\orca-data-lake` write.
- **Posture/value coupling is invariant.** Any field the contract defines must obey: observed ⇒ a numeric value; not-observed ⇒ null value + a reason; never zero-filled. This is load-bearing doctrine, not a style preference.
- **This is not a product-claim-contract freeze.** Pinning the record's field/computation/update contract is a data-model design act, not a freeze of what Orca claims to a customer. Do not over-reach into product positioning.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: repo-overlay-bound. Read `.agents/workflow-overlay/README.md` before project work (per `AGENTS.md`), then follow the Orca overlay. Entry points also include `docs/workflows/orca_repo_map_v0.md`.
- targets to enter the ladder (the four registry sources, see Source Ledger for compare targets):
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json` (the registry read model — the artifact whose contract is being pinned)
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md` (the registry read-model spec)
  - `orca-harness/capture_spine/creator_profile_current/materialize.py` (how the view is computed/materialized from the Silver snapshots)
  - `orca-harness/runners/run_creator_profile_current_materialize.py` (the materializer runner: `--check` for staleness, `--write` to refresh)
- already loaded (weak orientation, freshness-marked 2026-07-03; NOT authority): the field-set facts quoted in this packet were read from `creator_profile_current_view_v0.json` at blob `ae065ecfe38f` on origin/main.
- must load first (before any strict or actionable step): the overlay README, then the view + view spec at their compare targets.
- load rule: the receiver re-runs progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- **Three-layer architecture:** Bronze raw lake packets → Silver derived metric records (append-only longitudinal MetricObservation + MetricRollupObservation) → committed registry read model. The **creator registry IS the committed read model** (`creator_profile_current_view_v0.json`), materialized from per-platform Silver rollup snapshots. Verify in: the view spec (compare target below) and `materialize.py`.
- **Registry vs Silver boundary (owner-sharpened, this thread):** registry = the current per-creator state (identity + computed stats), refreshed each capture; Silver/capture = the flow (capture, longitudinal accumulation, cadence, scale). Verify by reading the view spec + `materialize.py` (registry side) and noting cadence/scale live in the capture-spine runners, not here.
- **Posture/value coupling doctrine:** observed⇔value; not-observed⇔null+reason; never zero-filled. Verify: it is enforced in `capture_spine/creator_profile_current/validation.py` and asserted throughout the view.
- **Where stats are computed vs stored:** the per-video→rollup computation (including `engagement_rate = round((sum(like)+sum(comment))/sum(view), 6)` over complete-input videos) happens at the Silver **producer** stage; the registry view STORES/PRESENTS the current computed rollup per creator. So "the computed stats" the owner refers to are computed on the Silver side and surfaced in the registry record. Verify in the producer modules under `capture_spine/creator_profile_current/` and the revalidator `rollup_formula_revalidation.py`.

## Active Objective

In a fresh thread: (1) EXPLAIN to the owner the two steps to pin the creator registry's per-creator record contract and WHY each matters, plus the current-window-vs-global-stats fork; (2) get the owner's ruling on the fork; (3) THEN pin the record contract. No capture, no lake writes; design over the committed read model only.

## Exact Next Authorized Action

1. Load the overlay README and reread the four registry sources at their compare targets (Source Ledger). Confirm the `metric_rollups` field set and the two `not_attempted` stubs still match this packet's quoted facts; if origin/main moved, re-derive from the live view.
2. EXPLAIN FIRST (chat only, no edits), for the owner:
   - **Step 1 — Pin the per-creator record field set.** Enumerate what the record stores per creator today (identity: `platform_accounts`, `platform_account_id_or_none`, `identity_state`, `identity_evidence_summary`; computed stats: the `metric_rollups` block; supporting: `sample_support`/`freshness`/`limitations`/`non_claims`/`source_drill_back` lineage; stubs: `ideal_audience_profile`, `review_state_or_none`, `wind_calling_summary`, and the two `not_attempted` metric stubs). Decide what is IN the v0 contract. **Why:** the registry's job is one trustworthy current record per creator; if the field set is not pinned, every cycle and every consumer risks drift about what a creator record even contains. Pinning it makes the record a stable contract instead of an incidental shape.
   - **Step 2 — Define the consumer contract.** State, per field, what a downstream reader is promised: what `observed` / `unavailable_with_reason` / `not_attempted` mean for that field, what the lineage (`source_drill_back`) and `freshness` guarantee, and what must never be assumed (e.g. a `not_attempted` or `unavailable` value is NOT zero). **Why:** "live use" means a downstream reader trusts the record; without a stated per-field promise, consumers misread postures as zeros or trust stale data — the exact failure the posture/value coupling doctrine exists to prevent.
   - **The fork** (see Open Decision): current-window only (A) vs also global cross-capture stats (B) vs both-staged (C, sender's recommendation), with the trade-offs.
3. STOP for the owner's ruling on the fork. Do NOT write the contract, build cross-capture stats, run any capture, or touch the identity ledger before the ruling. After the ruling, pin the contract as the owner directs (a design/spec artifact; if it becomes a committed doc, land it via the per-lane PR flow).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ its import of the same); read `.agents/workflow-overlay/README.md` before project work.
- Overlay or equivalent authority: `.agents/workflow-overlay/` (Orca overlay owns lanes, source loading, validation, PR flow).
- User constraints: see Goal Handoff, Open Decision, and Drift Guard. Owner's load-bearing correction (this thread, verbatim gist): "cadence isn't a creator registry thing, neither is scale, it's for silver data lake; creator registry is more of just storing key information about each creator (updated every capture for the global stats) as well as the computed stats being computed."
- Source-read ledger:
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
    - Role: the registry read model — the artifact whose per-creator record contract is being pinned. Source of the quoted field-set + stub facts.
    - Load-bearing: yes
    - Compare target: blob `ae065ecfe38f` on origin/main (`git rev-parse origin/main:<path>`); reread if it differs.
    - Last checked: 2026-07-03
    - Reuse rule: reread if blob moved (e.g. if PR #615 cycle-2 YT refresh merged, values change but the field set should not).
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
    - Role: the registry read-model spec (what the view is and its rules).
    - Load-bearing: yes
    - Compare target: blob `72368b858630` on origin/main.
    - Last checked: 2026-07-03
    - Reuse rule: reread at current origin/main before strict claims about the record's intended contract.
  - `orca-harness/capture_spine/creator_profile_current/materialize.py`
    - Role: how the registry view is computed/materialized from the Silver rollup snapshots (the update-from-Silver semantics).
    - Load-bearing: yes
    - Compare target: blob `4eb0f91ec4ce` on origin/main.
    - Last checked: 2026-07-03
    - Reuse rule: reread before strict claims about how the record updates each capture.
  - `orca-harness/runners/run_creator_profile_current_materialize.py`
    - Role: materializer runner (`--check` staleness, `--write` refresh).
    - Load-bearing: no (context for how a refresh is triggered)
    - Compare target: blob `c3fb58d36c74` on origin/main.
    - Last checked: 2026-07-03
    - Reuse rule: reread if the update mechanism is questioned.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`
    - Role: identity ledger — FENCED, read-only (Drift Guard).
    - Load-bearing: no (boundary marker)
    - Compare target: reread-required (do not write).
    - Last checked: not this thread
    - Reuse rule: never write; identity additions are a separate owner-gated lane.
- Source gaps: whether the view spec already anticipates cross-capture/global stats (the fork) is UNKNOWN to the sender — the receiver must read the spec to see if `posting_cadence`/`recent_velocity` have a stated intended recipe.
- Strict-only blockers: none for a design pass; committing any resulting contract doc goes through the per-lane PR flow (owner-gated on push/PR).
- Not-proven boundaries: the value of global cross-capture stats is unvalidated (no consumer exists yet); do not assert readiness or consumer fit.

## Current Task State

- Completed: the registry's current-window computation was review-hardened this thread (a delegated review of the sibling TikTok pipeline caught and fixed a zero-fill leak, a mixed-subset revalidation gap, and an identity-overwrite gap — landed on the TikTok branch, not the registry read model itself).
- Partially completed: the per-creator record field set exists and is populated for Instagram + YouTube; its CONTRACT (what's promised, and the global-stats fork) is not pinned — that is this handoff's task.
- Broken or uncertain: none in the registry read model. Note engagement_rate shows `unavailable_with_reason` on origin/main for the first profile (YouTube cycle-1); PR #615 (cycle-2 YT refresh, engagement observed for 28/30) may be unmerged — verify, but it does not change the field-set contract.

## Workspace State

- Branch: claude/registry-record-contract-handoff (created off origin/main cdc542c2 to carry this packet).
- Head: cdc542c2 at branch creation.
- Dirty or untracked state before handoff: clean.
- Dirty or untracked state after writing the handoff file: this packet is newly added/untracked until committed on its branch.
- Target files or artifacts: this packet (docs/workflows/creator_registry_record_contract_handoff_v0.md); the four registry sources in the Source Ledger.
- Related worktrees or branches: `claude/tiktok-silver-pipeline` (PR #622, TikTok code — parked data); `claude/yt-cycle2-engagement-refresh` (PR #615, YT engagement cycle-2 — verify merge state); `claude/funny-hamilton-07988f` (PR #626, IG revalidation hardening follow-up).

## Changed / Inspected / Tested Files

- `docs/workflows/creator_registry_record_contract_handoff_v0.md`
  - Status: added by this handoff (the packet itself).
  - Role: the durable cold-reader continuation artifact.
  - Important observations: this is a handoff, not a contract; the contract is the receiver's output after the owner's fork ruling.

## Frozen Decisions

- Registry = the committed read model materialized from Silver; cadence/scale are Silver/capture concerns.
  - Evidence: owner correction this thread; verify in the view spec + materialize.py.
  - Consequence: the record contract covers identity + computed current stats + lineage/freshness, not pipeline concerns.
- Posture/value coupling is invariant; never zero-fill.
  - Evidence: enforced in `capture_spine/creator_profile_current/validation.py`.
  - Consequence: every contract field must declare its posture semantics.
- TikTok data parked; identity ledger fenced.
  - Evidence: this thread; the ledger file's read-only fence.
  - Consequence: contract covers IG + YT; no identity writes.

## Mutable Questions

- Which computed stats belong in the v0 record contract — current-window only, or also global cross-capture stats? (The Open Decision fork; owner-owned.)
  - Why still mutable: unresolved owner design call; depends on how much cross-capture value is worth vs. deferring until Silver history accrues.
  - What would resolve it: the owner's ruling after the receiver explains the fork.
- Does the view spec already name intended recipes for `posting_cadence`/`recent_velocity`?
  - Why still mutable: sender did not read the spec's stub intentions.
  - What would resolve it: reading `creator_profile_current_view_spec_v0.md`.

## Superseded / Dangerous-To-Reuse Context

- Sender's earlier goal frame that made "cadence" and "scale" the registry's anchor goal.
  - Why stale or dangerous: the owner corrected it — those are Silver/capture concerns, not registry. Reusing it re-muddles the layer boundary.
  - Current replacement: the Goal Handoff + Drift Guard in this packet.

## Commands And Verification Evidence

- Compare-target read (how the field-set facts were derived; receiver re-runs to confirm):
  ```bash
  git rev-parse --short origin/main
  git rev-parse origin/main:orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  git show origin/main:orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  ```
  Result:
  - Passed/failed/not run: run 2026-07-03; origin/main = cdc542c2; view blob = ae065ecfe38f.
  - Important output: `metric_rollups` keys = {average_views, median_views, average_like_count, average_comment_count, engagement_rate, posting_cadence, recent_velocity}; `posting_cadence` and `recent_velocity` postures = `not_attempted`; per-profile record keys include platform_accounts, identity_evidence_summary, source_drill_back, freshness, limitations, non_claims, ideal_audience_profile, review_state_or_none, wind_calling_summary.
  - Re-run target so the receiver can confirm rather than trust: the three commands above.

## Blockers And Risks

- Risk: receiver builds cross-capture stats before the owner rules the fork, or scopes cadence/scale into the contract.
  - Evidence: the sender made the cadence/scale mistake; it is an easy trap.
  - Likely next action: explain-first and stop for the ruling, per the Exact Next Authorized Action.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting: the `metric_rollups` field set and the two `not_attempted` stubs; the registry-vs-Silver boundary; posture/value coupling invariance.
- Compare target for each: view blob `ae065ecfe38f`; view spec blob `72368b858630`; materialize.py blob `4eb0f91ec4ce`; validation.py (posture coupling).
- Load outcomes and what each means: `REUSE` — field set + boundary re-verified, proceed to explain-first; `STALE_REREAD_REQUIRED` — origin/main moved (e.g. #615 merged), re-derive the field set from the live view before explaining; `BLOCKED_DRIFT` — a compare target conflicts with an owner constraint (e.g. the record now writes identity), stop and reorient with the owner.
- Sources that must be reread if drift is detected: the view + view spec + materialize.py at current origin/main.

## Do Not Forget

- The owner wants EXPLAIN-FIRST: explain the two steps + why + the fork, get the ruling, THEN pin the contract. Do not jump to writing the contract.
