# Handoff Packet — IG Capture-Rate / At-Scale Operating Envelope

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (durable continuation artifact; NOT validation/readiness/authorization)
scope: >
  Transfers the Internet-Data / R-Measurement (IG capture-rate) lane to a fresh lane/agent. The
  original commission (measure per-IP R; decide proxies) is DONE. Carries the measured findings +
  the owner's NEW scope: proxy COST for scrolling/at-scale, a human-like-behavior model beyond
  bounded_jitter, and the ideal operating-account count for the beauty vertical — plus the one
  still-open measurement (at-pace volume ceiling).
use_when:
  - Picking up the IG capture-rate lane cold; sizing the at-scale operating envelope; finishing the ceiling.
authority_boundary: retrieval_only
stale_if:
  - The in-flight endurance retry lands (sets/abandons the at-pace ceiling).
  - The carve-out is amended (capture posture authority).
  - origin/main advances past the compare targets below (it moves fast — fetch fresh).
```

## Applied-Contract Record (`prompt-orchestration.md`)
```yaml
applied_contract_record:
  contract: .agents/workflow-overlay/prompt-orchestration.md
  authoring_route: >
    workflow-handoff (explicitly owner-invoked; owns the cold-handoff STATE PACKET). The
    prompt-orchestrator was not separately invoked; per "Author Through The Prompt Orchestrator"
    / Prompt Validation Gates, this file's contract is applied in full and recorded here. The
    courier prompt (orchestrator's lane) is the fenced handoff block delivered in chat.
  family: Implementation handoff (docs/prompts/handoffs/); output_mode file-write
  preflight:
    agents_md_and_overlay_readme: read in current task context (worktree off origin/main)
    source_pack: IG capture-rate lane pack — see Authority And Source Ledger (carve-out, ig_r_probe_results/design/report, monitoring policy, IG findings, runner)
    repo_map_decision: not_needed
    repo_map_reason: continuation of an active lane with a bound, enumerated source ledger
    workspace: C:\Users\vmon7\Desktop\projects\orca
    expected_branch_head: origin/main @ fb56b7ff (#185) at write; fast-moving (see Load Contract)
    dirty_state_allowance: gitignored scratch in worktrees; this handoff newly untracked until committed
    controlling_source_state: overlay read clean in worktree; reread-required for strict claims
    doctrine_change: none — continuation artifact; alters no product/architecture/workflow/validation/review/output/lifecycle doctrine
    target: docs/prompts/handoffs/ig_capture_rate_at_scale_operating_envelope_handoff_v0.md
    edit_permission: docs-write
    output_mode: file-write
    validation_gates: retrieval-header check + placement check; this packet is a continuation artifact, NOT validation/readiness/acceptance evidence
    external_source_boundary: jb / external workflow source is read-only and not Orca authority; none imported
  fitness_reference: see Goal Handoff (anchor_goal + success_signal) — executor target / review axis-to-attack, not a pass bar
  non_claims: [not validation, not readiness, not authorization, not doctrine change]
```

## Load Contract
- packet_version: v0 · mode: max · created_at: 2026-06-16 · created_by_lane: internet-data / R-measurement (IG capture-rate)
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/prompts/handoffs/ig_capture_rate_at_scale_operating_envelope_handoff_v0.md`
- expected_branch: receiver uses a **NEW worktree off `main`** (this lane churned several merged+deleted branches — do NOT reuse `internet-data-r-probe-*`).
- expected_head: `origin/main` @ `fb56b7ff` (#185) at write time — **moves fast; fetch fresh and rebase compare targets.**
- expected_dirty_state: probe scratch (`_scratch/*.py`, `_test_runs/`) is gitignored and lives ONLY in the `.claude/worktrees/r-probe-design` worktree (NOT on main). This handoff file is newly created → untracked until committed.
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact against its compare target before acting; this packet is a weak source class (orientation), not authority.

## Goal Handoff
- long_term_goal: Build the Orca creator-momentum product (capture → projection → judgment on the creator / wind-caller signal).
- anchor_goal: Define the **at-scale IG capture operating envelope** for the beauty vertical — proxy cost/benefit, **data-payload/bandwidth efficiency (media/asset blocking) + make-vs-buy vs a managed scraper API**, a human-like-behavior model beyond the runner's `bounded_jitter`, and the **ideal operating-account count** — grounded on the measured **per-IP, pace-bound R**; and finish the **at-pace volume ceiling**.
- success_signal: A costed, carve-out-conformant operating recommendation (proxy spend yes/no + trigger; human-like cadence/scroll spec; ideal number of (account, IP) pairs for the vertical roster) + the measured at-pace ceiling, that the monitoring-policy and projection-store lanes can size against.

## Open Decision / Fork
- **decision:** how to operate IG capture at full-vertical scale, given R is per-IP and pace-bound.
  - options / sub-questions (owner-supplied, all coupled):
    1. **Proxy / bandwidth cost for scrolling/at-scale** — TWO cost axes, not one: **(a) proxy egress $ = bandwidth** — continuous scrolling pulls images/video/CSS/fonts; ~10 accounts × 8h is hundreds of GB → ~$200+/mo of proxy data UNLESS the runner **aborts media/asset requests** (`.jpg/.png/.mp4/woff/css`), which cuts **~90%** of bandwidth (the calls signal lives in the initial-document `og:description`; assets are pure waste for it). **(b)** proxy/IP-rotation as a **perma-block fallback** / if volume grows. Plus **make-vs-buy:** a managed scraper API (~$2.50/1k profiles; ~$180 for 72k) vs custom logged-out + proxy infra (cheaper per-unit, but account/proxy/detection maintenance). *(Illustrative $ — re-cost for the actual vertical roster.)*
    2. **Human-like behavior** — beyond `bounded_jitter` (8–45s gaps): scroll patterns, variable session length, time-of-day shaping, idle gaps, and **periodic long sleeps (~15 min every ~50 reads = "phone put down")**. NB: this is the **operational fix for the measured sticky throttle** — the endurance probe tripped *and sustained* the IP-wide login-wall precisely because it lacked long quiet windows. Extends account/IP lifespan; stay "faster-than-human-not-takedown-risking."
    3. **Ideal operating-account count for the beauty vertical** — carve-out caps at **≤10 (start ≤5)**. KEY COUPLING: R is **per-egress-IP, not per-account** (logged-out → no session to spread load), so extra logged-out accounts on ONE IP add **zero** throughput. Accounts only multiply throughput paired with distinct IPs (→ proxy question) or via sessions (carve-out amendment). So "ideal #accounts" = "ideal # (account, IP) pairs" for the all-in-vertical roster.
    4. **Data-payload efficiency vs fingerprint realism — the load-bearing TRADEOFF:** asset-blocking cuts ~90% bandwidth $, BUT a browser that fetches only HTML and aborts every image/css/font is a strong **bot fingerprint** → *worsens* the detection/throttle that is already the binding constraint. Bandwidth-optimization and detection-avoidance **pull in opposite directions**; tune the balance (e.g. block heavy media/video, keep enough asset traffic to look plausible), don't max one.
  - already constrained / off the table: proxies/sessions are NOT warranted for realistic monitoring cadences (decided — see Frozen). Logged-out only. Sessions need a carve-out amendment.
  - trade-offs: proxy $ vs near-zero current benefit (pace-bound, not volume-bound); **bandwidth-saving (asset-blocking) vs fingerprint-realism (detection) — opposite directions**; human-likeness effort vs takedown-risk reduction; account count bounded by the ≤10 cap AND per-IP economics; make-vs-buy (managed API) vs custom-infra maintenance.
  - owner of the call: owner (this is design/analysis; any live run is owner-gated).
  - recommendation: frame all three around the **per-IP pace-bound** finding — treat proxies/accounts as a *contingency/scaling* analysis (not a current need), and the human-like model as the live operational deliverable. Start doc/spec (default-allowed); live runs owner-gated.

## Drift Guard
- **Carve-out (`docs/decisions/wind_caller_calibration_carveout_v0.md`, amended 2026-06-15) — load-bearing:** logged-out only (never wire cookies/sessions into a committed runner); **≤10 our-own operating accounts (start ≤5)** — counts OUR capture accounts, NOT subjects (subject roster uncapped / all-in-vertical); no standing/scheduled crawler (passive = human-initiated, time-bounded, self-terminating); pace faster-than-human-but-not-takedown-risking; US-first (EU/UK need a legitimate-interest assessment first); 10-yr retention + takedown-on-request; commercial scale → licensed/bought data. **The live RUN is owner-initiated.**
- **R is PACE-bound, not volume-bound** — do not re-frame the scaling question as a volume/storage problem; the binding constraint is inter-read spacing.
- **Do not trip the throttle** — sub-2s reads trip an IP-wide soft login-wall that is **sticky ≥12 min** (sustained by probing); recovery needs a long fully-quiet window.
- **(B) virality-sprint clarification is NOT on main** — lane-only (`ig-creator-momentum-lane` @ `6ff2f559`); the carve-out on `main` has no (B) language. Burst is fine as *attended* passive reads regardless; do not assume (B) is durable doctrine.
- **Probe MEASURES READS only** — never write typed `metric_observations` (PR #158 IG typed-capture); that wiring belongs to the IG-producer slice.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)
- overlay source-loading policy: `.agents/workflow-overlay/README.md` → `source-of-truth.md` + `source-loading.md` (repo-overlay-bound; NOT zero-config). Read `.agents/workflow-overlay/README.md` before project work.
- targets to enter the ladder: the source-ledger docs below + the IG calls runner.
- already loaded (weak orientation, freshness-marked; not authority): this packet's summary of the findings (as of 2026-06-16).
- must load first (before strict/actionable steps): the carve-out; `ig_r_probe_results_v0.md` (the measured findings); `orca_creator_monitoring_policy_architecture_v0.md` (where R plugs in).
- load rule: re-run progressive source loading per the overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts (inline gist + verify pointer)
- **Per-IP, pace-bound R** — the limit is egress-IP-keyed and tripped by *pace* (sub-2s), not volume. Decided in: `docs/product/source_capture_toolbox/ig_r_probe_results_v0.md` (on main). Compare: reread-required on current `origin/main`. Verify before any scaling claim.
- **~2.5–4s operating pace (owner-adopted)** — sweet spot above the ~2s trip point. In: same results doc, "Owner closeout (2026-06-16)". reread-required.
- **Neither proxies nor sessions (for realistic cadences)** — mitigation is pace discipline. In: results doc decision section. reread-required.
- **Logged-out posture + the shipped runner is the instrument** — `run_source_capture_ig_calls_packet.py` (1 profile + ≤12 items per invocation; built-in `_detect_ig_block`). In: `ig_sustained_cadence_r_probe_design_v0.md` (on main). reread-required.

## Active Objective
Characterize the at-scale IG capture operating envelope for the beauty vertical (proxy cost, human-like behavior model, ideal (account,IP) count), grounded on per-IP pace-bound R, and land the still-open at-pace volume ceiling.

## Exact Next Authorized Action
1. **Harvest the in-flight endurance retry** (background task `bw9blnjhn`): read `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\r-probe-design\orca-harness\_test_runs\r_probe\endurance2\endurance_log.jsonl` + `endurance_summary.json`. It is recovery-gated (10-min quiet windows); it either measures the at-pace ceiling or aborts `ip_not_recovered` again. Record the result into `ig_r_probe_results_v0.md` (new follow-up PR off current main).
2. **Scope the 3 new questions** (doc/spec — default-allowed): proxy cost/benefit (as a fallback/scaling analysis), human-like-behavior model (beyond `bounded_jitter`), ideal #(account,IP) pairs (anchored on per-IP economics + the ≤10 cap + the all-in-vertical roster).
3. **Stop conditions:** any live IG capture is owner-gated, logged-out, bounded, self-terminating; never sub-2s (trips the sticky throttle); honor the carve-out.

## Authority And Source Ledger
- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (overlay is project authority).
- Source-read ledger (all paths on `origin/main` unless noted; `origin/main` moves fast → `reread-required`):
  - `docs/decisions/wind_caller_calibration_carveout_v0.md` — Role: capture posture authority. Load-bearing: yes. Compare: reread-required (note: (B) NOT present on main). Reuse: re-read before any live run.
  - `docs/product/source_capture_toolbox/ig_r_probe_results_v0.md` — Role: measured R findings + owner closeout + endurance-attempt log. Load-bearing: yes. Compare: reread-required. Reuse: the evidence record.
  - `docs/product/source_capture_toolbox/ig_capture_rate_findings_report_v0.md` — Role: downstream-facing synthesis (pace-bound guidance). Load-bearing: yes. Compare: reread-required.
  - `docs/product/source_capture_toolbox/ig_sustained_cadence_r_probe_design_v0.md` — Role: probe method/design (instrument, ramp, burst, two-consumer report, purity boundary). Load-bearing: yes. Compare: reread-required.
  - `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md` — Role: Consumer A (R sizes Tier-A breadth; pace-safe cadences). Load-bearing: yes. Compare: reread-required.
  - `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md` — Role: H5 residual + logged-out method map + discovery edge. Load-bearing: context. Compare: reread-required.
  - `orca-harness/runners/run_source_capture_ig_calls_packet.py` — Role: the instrument (logged-out; no metric_observations in this base). Load-bearing: yes. Compare: reread-required.
  - **Scratch probes (NOT on main; gitignored; in `.claude/worktrees/r-probe-design/orca-harness/_scratch/`):** `r_probe_endurance.py`, `r_probe_ramp.py`, `r_probe_discovery_snowball.py`, `r_probe_harvest.py`. Load-bearing: for re-running only. Compare: reread-required IN that worktree. Reuse rule: **disposable** — recreate from the design doc's method if the worktree is gone; do not treat as committed.
- Source gaps: the probe orchestration scripts are not committed (disposable scratch). Raw probe runs (`_test_runs/r_probe/{ramp,ramp2,endurance,endurance2,discovery,disambig}/`) are gitignored.
- Not-proven boundaries: at-pace volume ceiling (unmeasured); exact pace threshold (1s? burst-shape?); throttle decay time (>12 min). All n=1-ish; directional.

## Current Task State
- **Completed:** per-IP R measured (pace-bound); proxies-vs-sessions decided (neither, for realistic cadences); design + results + report landed on `main` (PR #162 + #170 both MERGED); "decays in minutes" corrected to sticky-≥12-min; roster of 8 (5 owner-confirmed-US + 3 search-surfaced).
- **Partially completed:** at-pace volume ceiling — endurance retry **in-flight** (`bw9blnjhn`); recovery-gated, may abort again if the IP hasn't cooled.
- **Broken / uncertain:** throttle decay time and exact pace threshold unmeasured; the 3 search-surfaced creators (`iz_alwaysglowing`, `nicolebreaksitdown`, `kbelllbeauty`) are unverified-nationality probe targets (no calibration retention).

## Workspace State
- Branch: `main` @ `fb56b7ff` (#185) at write time (fast-moving — fetch fresh).
- Lane work done via worktrees under `.claude/worktrees/`.
- Related worktrees: `r-probe-design` (runs the probes; has the gitignored `_scratch` + `_test_runs`; on the stale, merged-then-recreated `internet-data-r-probe-design-v0` branch — DANGEROUS to reuse as a branch); `r-probe-report` (merged #170, stale base); `r-probe-handoff` (this handoff, off current main).
- Target files: the source-ledger docs above; the endurance2 log.
- Dirty/untracked after writing this file: this handoff is newly created/untracked in the `r-probe-handoff` worktree until committed.

## Frozen Decisions
- R is per-IP, pace-bound (not volume-bound). Evidence: results doc; run1 176 reqs @≥2s clean vs run2 wall @sub-2s. Consequence: scaling = pace discipline, not proxies.
- Operating pace ~2.5–4s; never sub-2s. Evidence: owner closeout. Consequence: monitoring cadences just space batched reads ≥2.5s.
- Neither proxies nor sessions for realistic cadences. Evidence: results decision. Consequence: the new proxy/account analysis is contingency/scaling, not a current need.
- Burst (6h/12h) safe (hours-spaced ≪ trip pace). Evidence: report. Consequence: virality sprints are not rate-limited.
- Logged-out only; probe writes no `metric_observations`. Evidence: design purity boundary + carve-out.

## Mutable Questions
- At-pace daily-volume ceiling? — resolves when the endurance retry (`bw9blnjhn`) lands clean.
- Proxy cost vs marginal benefit for scrolling/at-scale? — new lane analysis.
- Human-like-behavior model beyond `bounded_jitter`? — new lane spec.
- Ideal #(account, IP) pairs for the beauty vertical roster (within ≤10)? — coupled to per-IP economics.

## Superseded / Dangerous-To-Reuse Context
- **"throttle decays in minutes"** — WRONG. Replacement: sticky ≥12 min, sustained by probing; needs a long fully-quiet cooldown. (Corrected in results + report.)
- **Original handoff framing "(B) not relevant to a one-shot probe"** — burst is now in scope; AND (B) is still NOT on main (lane-only `6ff2f559`). Treat burst as attended passive reads under the main posture.
- **Branch `internet-data-r-probe-design-v0`** — merged (#162) then accidentally recreated by a post-merge push; now far behind main. Do NOT branch/PR from it. (Pending owner-approved deletion.)
- **`r-probe-report` worktree / `internet-data-r-probe-report-v0`** — merged (#170), stale base #165. Do not reuse.

## Commands And Verification Evidence
- Drive the shipped runner (logged-out, from `orca-harness/`), the instrument the probes wrap:
  ```bash
  python runners/run_source_capture_ig_calls_packet.py --profile-url "https://www.instagram.com/<handle>/" \
    --decision-question "..." --output "_test_runs/<unique>/" --max-items 12 \
    --cadence-min-gap-seconds 2.5 --cadence-max-gap-seconds 4 --profile-scroll-passes 3
  ```
  Re-run target: any safe-pace (≥2.5s) read should return exit 0 with a packet; sub-2s risks the sticky login-wall. Live runs are owner-gated.
- Harvest the endurance retry: read `…/r-probe-design/orca-harness/_test_runs/r_probe/endurance2/endurance_log.jsonl`.

## Blockers And Risks
- **IP may still be throttled** — the endurance retry could abort `ip_not_recovered` again; if so, let the IP sit fully quiet (≥45–60 min, zero reads) before the next try. Evidence: prior abort after 12.7 min of probing.
- **Scratch probes not on main** — if the `r-probe-design` worktree is cleaned, recreate the orchestration from the design doc's method (the runner CLI + a loop + `_detect_ig_block`).
- **origin/main moves fast** — compare targets are path-bound + `reread-required`; do not trust this packet's HEAD.

## Confirm-Don't-Trust Load Checklist
- Re-verify before acting: per-IP pace-bound R + ~2.5–4s + neither-proxies-nor-sessions (re-read `ig_r_probe_results_v0.md` on current main); carve-out posture (re-read carve-out; confirm (B) state); the endurance retry result (harvest `endurance2` log — do not trust "in-flight").
- Compare targets: all source-ledger docs are `reread-required` on current `origin/main`.
- Load outcomes: `REUSE` only after re-verifying the above; `STALE_REREAD_REQUIRED` if main advanced (expected); `BLOCKED_*` if the carve-out changed or the endurance worktree is gone.

## Do Not Forget
- The endurance retry (`bw9blnjhn`) is IN-FLIGHT — harvest it; record the ceiling (or another abort) into the results doc via a fresh PR off current main.
- Pending cleanup (owner-gated): delete the stray `internet-data-r-probe-design-v0` remote branch; remove the idle `r-probe-report` and (later) `r-probe-design` / `r-probe-handoff` worktrees.
- The three new questions are COUPLED through per-IP economics — answer them together, not as a volume problem.
