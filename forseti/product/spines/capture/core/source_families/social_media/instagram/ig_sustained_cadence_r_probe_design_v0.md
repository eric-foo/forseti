# IG Sustained-Cadence R-Probe — Design (v0)

```yaml
retrieval_header_version: 1
artifact_role: probe design / measurement-method spec (non-authorizing; the RUN is owner-gated)
scope: >
  Design for a bounded, logged-out, self-terminating probe that measures R (safe
  reads/day) and rate-limit-onset behavior for the IG creator-momentum capture path
  across TWO read profiles (steady-state age-bucket cadence + burst 6h/12h on one hot
  post) — closing the H5 sustained-cadence-at-scale residual, reporting R/volume for
  TWO consumers (monitoring-policy cadence sizing + projection-store engine pick), and
  deciding the scaling mitigation if R is insufficient (IP-rotation/proxies vs
  re-opening the retired sessioned lane). Design only; the live RUN is owner-gated.
  The probe MEASURES READS only — it writes no typed metric_observations (no coupling
  to the unbuilt IG producer; PR #158).
use_when:
  - Scoping or authorizing the H5 / R / rate-limit probe (steady-state + burst) for the IG capture path.
  - Deciding the scaling mitigation if logged-out R is insufficient (proxies/IP-rotation vs re-opening the sessioned lane).
  - Sizing the monitoring-policy cadences AND the projection-store engine pick from measured R + volume.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_r_probe_results_v0.md   # landed first measured reading
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md   # the H5 residual + logged-out method map
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md   # where R plugs in (read-budget equation)
  - docs/decisions/wind_caller_calibration_carveout_v0.md   # capture posture authority (amended 2026-06-15)
stale_if:
  - A fuller R follow-up run changes the measured pace-bound result, at-pace ceiling, or decay-time posture.
  - The shipped calls runner changes its read model (max-items cap, scroll-pass enumeration, or onset detector).
  - The carve-out is amended in a way that changes the probe's posture bounds.
branch_or_commit: designed against origin/main @ f266f83b (PR #154); instrument = orca-harness/runners/run_source_capture_ig_calls_packet.py at that revision.
```

## Status

`DESIGN — RUN LANDED; HISTORICAL METHOD SPEC.` This is doc/spec work (default-allowed).
The first measured reading has landed in `ig_r_probe_results_v0.md`; use that results doc for current
R claims. Any further probe **RUN** remains live network / ToS-risk activity and is
**owner-initiated** per the wind-caller carve-out. Nothing here authorizes another run, a proxy build,
or any push/PR. Not validation, readiness, or a build-go.

**2026-06-16 addendum (delta, not a reset):** this design now covers **two read
profiles** (steady-state + burst), structures its report for **two consumers**
(monitoring-policy + projection-store), and adds a **purity boundary** (measures reads
only; writes no typed `metric_observations`). Confirm-don't-trust note: the addendum
historically cited carve-out posture **(B)** (pre-authorized, self-terminating sprints) as "now
durably recorded," but as of this writing **(B) is still NOT on `main`** — lane-only
(`ig-creator-momentum-lane` @ `6ff2f559`); the carve-out on `main` has no (B) language.
The burst profile does **not depend on (B) being merged**: an *attended* burst test is
human-initiated passive reads, already permitted by the **main** posture. The (B)
propagation gap is flagged for the carve-out lane owner, not resolved here.

**2026-06-16 outcome note:** the first R-probe measured a pace-bound result, not a complete at-pace
daily ceiling. Current `origin/main`'s packet-mode IG runner has since grown metric-observation
surfaces, but this probe design's purity boundary still applies to the R claim: R-probe evidence is
read-measurement evidence, not producer/projection acceptance.

## The question (what R is, precisely)

**R = safe reads/day**: how many logged-out IG page reads Orca can sustain per day
before **rate-limit onset** — the point at which IG returns a `429`
"please wait a few minutes" interstitial, redirects to `/accounts/login`, or shows
a network-security block.

At design time, R was **the one empirically-unmeasured number** in the creator-momentum lane. The
monitoring policy (`forseti_creator_monitoring_policy_architecture_v0.md`) is built around it: its
read-budget bound is `reads/cycle ≤ R × cycle_days`, and R sizes **Tier-A breadth** (how many
creators get full age-bucket density). The first measured reading now says R is per-IP pace-bound,
with the at-pace daily ceiling still open.

### The H5 residual this closes
Per `ig_capture_findings_consolidated_v0.md`: single deep walks of one creator are
clean (no `429`; the reel path went 25 pages / 365 media with no wall). What is
**UNTESTED** is *repeated harvesting across many subject creators, over time*. The
probes to date are `n=1–2` feasibility GOs, not at-scale validations. This probe
measures that residual directly.

### The load-bearing insight: in the logged-out posture, R is per-egress-IP
The shipped runner is logged-out by construction, and the snapshot adapter opens a
**fresh browser context per capture** (`new_context()` → `goto()` → `browser.close()`),
so **no cookie/session state accumulates** between reads. There is no account to
ban — and none to spread load across. Therefore IG's logged-out rate limit is keyed
to the **egress IP / network fingerprint**, not to any session identity. Two
consequences that shape the whole probe:

- **Baseline R is a per-IP quantity.** "≤10 operating accounts" does **not**
  multiply throughput on one IP: logged-out contexts on one egress all share that
  IP's budget. (This is exactly why the carve-out's account cap counts *our
  operating accounts*, not subjects — and why on the logged-out path the binding
  resource is the IP, not the account.)
- **The mitigation question is therefore a division.** Once per-IP R and roster demand
  are known, IPs-needed ≈ `ceil(roster_demand / per_IP_R)`. A scaling mitigation —
  proxies/IP-rotation, *or* re-opening the sessioned lane (a different regime; see the
  decision rule) — is warranted **iff** one egress IP cannot carry the roster. Measure the
  numerator and denominator first; do not build mitigation before measuring the problem.

### What counts as a "read" (two levels — state both)
- **Invocation level** (what the operator drives): one runner invocation = `1`
  profile capture + `N` item captures, `N ≤ 12` (hard cap in the runner).
- **IG-request level** (what the rate limit actually sees): the adapter exposes
  **no network log**, so requests are *modeled*, not counted: a **profile** capture
  ≈ `1` document request + up to `scroll_passes` grid XHRs (default 3 ⇒ ≈ 4 IG
  requests); an **item** capture ≈ `1` document request (the `og:description` is in
  the initial document; item captures use `scroll_passes=0`). So one default
  invocation ≈ `(1+3) + 12 ≈ 16` IG requests, worst case. **R must be reported in
  IG-request units** (the rate-limit unit), with the invocation count alongside.
  *(True per-request counting would require adding a network log to the adapter — a
  separate owner-gated code change; not required for a first R reading, noted as an
  optional accuracy upgrade below.)*

## Instruments (use what is shipped; do not build new capture code to measure)

| Instrument | State | Role in the probe |
|---|---|---|
| `run_source_capture_ig_calls_packet.py` (shipped, logged-out, 832 tests, live `@hyram` 6/6) | **BUILT, merged** | The primary read generator. Drive it repeatedly across the subject set. |
| `_detect_ig_block()` inside that runner | **BUILT** | The **onset detector** — already classifies `redirected_to_login`, `rate_limited_429_interstitial`, `network_security_block`. Profile-level block ⇒ exit code `3` (NO-GO, no packet); item-level block ⇒ recorded per-item as `access_blocked` / `block_reason`. The probe reads these; it adds no new detection logic. |
| Reel/view-count cursor path (`web_profile_info` + grid `graphql/query`, `doc_id=7950326061742207`) | **FEASIBILITY-PROVEN, NOT built** | There is **no runner to drive**. So baseline R is measured with the **calls runner**. Reel-depth reads are an *additional* read class; characterizing their R is a deferred follow-up after that build (or an optional in-session manual cursor-walk — see Open decisions). Do not claim to "drive a reel runner"; none exists. |

**Tunable knobs the probe uses (existing CLI, no code change):** `--max-items`
(≤12), `--cadence-min-gap-seconds` / `--cadence-max-gap-seconds` /
`--cadence-window-seconds` (within-invocation pacing), `--cadence-random-seed`,
`--profile-scroll-passes`, `--output`. **There is no proxy/session knob** — by
construction (conforms to the carve-out's logged-out-only rule).

**Throughput envelope (so the time ceiling is realistic):** each capture launches a
fresh headless Chromium (~1–2 s) plus page-load plus the cadence gap. At the
runner's default gaps (8–45 s) a ~13-capture creator-invocation takes ≈ 5–6 min; a
5–8 creator pass ≈ 30–50 min. The ramp shortens gaps to raise reads/hour.

## Probe design

### Subjects (passive monitoring of already-flagged creators — not discovery)
A **small set of 5–8 public-figure beauty creators**, **US-first**, that are
**already flagged** (chosen before the run). Because the set is pre-chosen, the run
is **PASSIVE** monitoring (no discovery during it), which the carve-out permits as a
human-initiated, time-bounded, self-terminating session. The subject roster is
uncapped in doctrine; a small set is sufficient to generate sustained multi-creator
load without overreach.

### Operating context (carve-out account cap)
**Baseline phase: one egress IP / one operating context** (well within ≤10, start
≤5). Because R is per-IP, one egress is the correct unit to measure first. An
optional second phase may add a **second egress IP** to test whether R is additive
across IPs (the proxies-warranted follow-up) — deferred unless the owner opts in.

### Steady-state read-profile — the ramp (dimension = aggregate IG-requests/hour, raised in bounded rounds)
Start conservative, raise the aggregate read rate each round until onset or a hard
ceiling. The ramp deliberately pushes **faster than human-mimicking pace** — which
the 2026-06-15 passive posture authorizes ("faster than human, but not
takedown-risking") and which is the *only* way to find the wall.

| Round | Within-invocation gaps | Between-creator pause | Aggregate intent |
|---|---|---|---|
| R1 (baseline) | default 8–45 s | ~2–5 min | One clean full pass over the set at human-mimicking pace. Onset here would be a strong NO-GO signal. |
| R2 | 2–8 s | ~30–60 s | ~3–5× R1 rate; repeat passes, accumulate reads. |
| R3 | 0.5–2 s | none (back-to-back) | Push toward the wall; keep accumulating until a stop condition fires. |

Re-running the same creator with a fresh `--output` each round is itself part of
"sustained cadence" (passive re-monitoring) and is the cheapest way to accumulate
reads without expanding the subject set.

### Stop conditions (bounded + self-terminating; first to fire wins)
1. **Onset (the measurement endpoint):** the first `_detect_ig_block()` hit of any
   class. Record cumulative reads-to-onset, wall-clock, round, and which class.
   **Do not push past onset** — this is the "not takedown-risking" guarantee:
   approach the wall once, detect it, retreat.
2. **Read ceiling `N_max`** (no-onset endpoint): default **≈ 800 IG-request-equiv
   reads** (owner-tunable). Reaching it without onset ⇒ R is reported as a **lower
   bound** (`R ≥ N_max / session_fraction_of_day`), not a point estimate.
3. **Time ceiling `T_max`:** a single attended sitting, default **≤ 3–4 hours**. No
   overnight / standing run.
4. **Manual abort:** the operator stops at any time.

### Optional: onset-recovery characterization (transient vs hard)
If onset fires before `N_max`, optionally: wait a bounded cooldown (e.g. 10 / 30 /
60 min), attempt **one** read, record whether access recovered. This distinguishes a
*soft rate limit* (recovers after cooldown ⇒ R is a rate, manage with pacing) from a
*hard block* (does not recover ⇒ R is a hard daily cap, proxies more likely). Keep
total added reads ≤ ~5; still self-terminating.

### Burst read-profile — single hot post at 6h/12h (Delta 1; de-risks carve-out (B))
The most aggressive pattern the system will ever run is the **(B) virality sprint**: one
hot post sampled at a **6h / 12h** cadence while it spikes — the highest rate-limit /
takedown risk, and the most valuable thing to measure **before** the sprint mechanism is
built. It is measurable **now, attended**; the sprint **auto-launch mechanism does not need
to exist** to test whether the *cadence itself* is sustainable.

- **Question:** can a SINGLE already-flagged hot post (one reel/post permalink) be read
  **logged-out** at ~6h/12h for **~1–2 days** without a wall?
- **Method:** a thin **one-permalink read** (browser snapshot + `_detect_ig_block` +
  `parse_ig_og_description`) against the one post on a 6h/12h schedule of
  **operator-initiated** reads (NOT a daemon) for 1–2 days; record each read's block
  result + latency. ~4–8 reads total.
- **Conformance:** bounded, self-terminating, attended, no-discovery passive monitoring —
  permitted by the **main** carve-out posture **without** needing (B) merged; the operator
  initiates each read (no auto-launch).
- **Output:** burst-cadence feasibility (GO / wall-at-read-k), which **directly de-risks
  (B)** before the sprint auto-launcher is ever built.
- **Sequencing:** run **after** the steady-state ramp and **after the IP recovers** from any
  ramp-induced rate-limit — never concurrently (same IP would confound both).

### What to record (per read, append-only)
Wall-clock; round; subject handle; capture kind (profile/item); cumulative
invocation count; **modeled IG-request count** (profile = 1 + scroll_passes; item =
1); runner exit code; per-item `status` (`captured` / `access_blocked` /
`no_signal` / `capture_failed`) and any `block_reason`; page-load latency if
available. The first row whose `block_reason` is set is the onset point.

## From measurement to R
- **Onset observed at cumulative `C` reads in elapsed `t`:** report **R ≈ C** as the
  per-IP safe daily budget if onset did not recover in cooldown (hard cap); if it
  recovered after cooldown `c`, report R as a *rate* ≈ `C / (t + c)` reads per
  recovery window, extrapolated conservatively to a daily figure with the recovery
  behavior noted. Always per-IP.
- **No onset by `N_max` in `T_max`:** report **R ≥ N_max** (lower bound) and note the
  probe did not reach the wall — a *good* outcome (one IP carries at least `N_max`/day).
  Do **not** invent a point estimate the data does not support.

R is reported in **IG-request units**, with the invocation count and the modeling
assumption (profile = 1 + scroll_passes XHRs) stated, so the monitoring policy can
consume it directly.

## Report structure — two consumers (Delta 2)
R/volume feeds **two** downstream lanes, so the report is structured to serve both:

- **Consumer A — monitoring policy** (`forseti_creator_monitoring_policy_architecture_v0.md`):
  needs **steady-state R** to turn its illustrative R-tunable cadences into sized defaults
  (R sizes Tier-A breadth = how many creators get full density).
- **Consumer B — data-pipeline / projection-store lane**
  (`forseti_capture_projection_storage_spine_architecture_v0.md`): its **engine pick is gated
  on R + volume** (total rows over the working horizon).

Report these four, in a shape both consume:
1. **Steady-state R** — per-IP safe reads/day (onset point or `≥` lower bound), in IG-request units.
2. **Burst-cadence feasibility** — can one hot post sustain 6h/12h for ~1–2 days (GO / wall-at-read-k).
3. **Roster size** — all-in-vertical estimate `M` (the uncapped subject roster) × tier mix.
4. **Per-platform read cost** — reads/creator/day by tier (IG filled; TikTok/YouTube/Reddit are deferred profile seams).

## Extrapolation to roster demand (the proxies math)
Using the monitoring policy's read-budget equation and its own illustrative IG
figures (Tier-A daily poster fully tracked ≈ ~10 reads/day; per-creator cap K≈30;
Tier-C heartbeat ≈ weekly):

```
roster_demand (reads/day) ≈ M × [ f_A · d_A + f_B · d_B + f_C · d_C ]
  where M = roster size; f_* = tier fractions; d_* = per-creator reads/day per tier
  illustrative: d_A ≈ 10,  d_B ≈ 1.5,  d_C ≈ 0.15
  illustrative mix f_A=0.10, f_B=0.30, f_C=0.60  ⇒  per-creator ≈ 1.54 reads/day
```

| Roster M | Illustrative roster_demand | per-IP R needed to avoid proxies |
|---|---|---|
| 200 | ≈ 308 reads/day | 1 IP suffices if measured R ≳ 308/day |
| 1,000 | ≈ 1,540 reads/day | 1 IP if R ≳ 1,540/day; else `ceil(1540 / R)` IPs |

**(All figures illustrative — R was unmeasured at design time; M and the tier mix are owner inputs.
Use `ig_at_scale_operating_envelope_v0.md` for the current first-measured operating envelope.)**

## The scaling-mitigation decision rule (the conditional fork)
The probe's outcome maps to one of three actions — **not** a proxies yes/no:

1. **per-IP R ≥ roster_demand ⇒ no scaling mitigation needed.** One egress carries the
   working roster; record the headroom; revisit only if the roster or cadence grows.
2. **per-IP R < roster_demand ⇒ add IPs (proxies / IP-rotation).** Stays logged-out and
   carve-out-compliant. Estimate IPs ≈ `ceil(roster_demand / per_IP_R)`, subject to a
   follow-up **additivity check** (the optional 2nd-IP phase, or a later probe) because
   subnet/fingerprint correlation may mean N IPs deliver < N×R. The proxy BUILD remains
   separately authorized.
3. **per-IP R < roster_demand ⇒ re-open the retired sessioned lane (alternative regime).**
   The IG findings retired the session/auth lane with an explicit reopen condition —
   *"re-open only if the H5-scale probe shows logged-out is rate-walled where a session
   sustains more — a scale question, not a reachability one"* — and **this probe is that
   H5-scale probe.** A sessioned runtime is keyed to the **account** (not the IP), so it
   can raise per-account limits and spread load across accounts, **but**: accounts are
   bannable (logged-out has none to lose), need creation + warming, and login automation
   raises ToS / detection risk. It also **requires an owner carve-out amendment** — the
   current drift guard forbids wiring cookies/sessions into a committed runner. Branch 3
   is a doctrine decision, not a build the probe authorizes.

Branches 2 and 3 are **alternatives for the same trigger** (low logged-out R). Choosing
between them — IP-rotation cost/fragility vs account ban-risk + ToS + carve-out amendment
— is an owner decision the probe's R measurement *informs* but does not make.

## Carve-out conformance checklist (load-bearing)
Governed by `wind_caller_calibration_carveout_v0.md` as amended 2026-06-15:

- [x] **Logged-out only** — runner has no cookie/session path; never wire one in.
- [x] **Operating-account cap** — 1 egress for baseline (≤10 / start ≤5); the cap
      counts our operating contexts, not subjects.
- [x] **Subjects** — small set of already-flagged, US-first public-figure creators;
      **passive** (no discovery during the run).
- [x] **No standing/scheduled crawler** — human-initiated, time-bounded, self-
      terminating single session; hard `N_max` / `T_max` ceilings; no daemon.
- [x] **Pace** — ramps *faster than human* (authorized) but **stops at first onset**
      (approach-and-retreat = "not takedown-risking"); never sustains past the wall.
- [x] **RUN is owner-initiated** — live ToS-risk activity; not launched here.
- [x] **Retention** — probe records are operational measurements (read tallies /
      onset), not person dossiers; subject material stays within the 10-year /
      takedown posture.

## Owner-gated RUN procedure (ready to authorize; do not run until owner go)
Run from `orca-harness/`. One invocation per (creator, round); unique `--output`
each time (the runner refuses to overwrite an existing staging parent). Example
single invocation:

```
python runners/run_source_capture_ig_calls_packet.py \
  --profile-url "https://www.instagram.com/<handle>/" \
  --decision-question "R-probe: logged-out IG safe-reads/day onset (H5)" \
  --output "_test_runs/r_probe/<round>/<handle>/" \
  --max-items 12 \
  --cadence-min-gap-seconds <round_min> --cadence-max-gap-seconds <round_max> \
  --cadence-window-seconds 900 --cadence-random-seed <round>
```

The orchestration across (creators × rounds) is a **thin shell/PowerShell loop over
this existing CLI** plus an append-only log of the per-read fields above — **no new
committed runner code** for a first reading. On the first `_detect_ig_block` hit
(exit `3` at profile, or an `access_blocked` item), the loop **stops**. Outputs go
to the gitignored `_test_runs/` scratch.

## Open decisions for the owner (before the RUN)
1. **Subject set** — which 5–8 already-flagged US-first creators (or accept an
   operator-chosen set at run time).
2. **Ceilings** — confirm/adjust `N_max` (~800 reads) and `T_max` (~3–4 h).
3. **Reel read class** — include an optional in-session manual cursor-walk to
   characterize reel-depth R (uses the proven-but-unbuilt mechanism), or defer it
   until the reel runner is built? Default: **defer**.
4. **2nd-IP additivity** — include the optional second-egress mini-phase to test R
   additivity now, or defer until baseline R says proxies are warranted? Default:
   **defer**.
5. **Per-request accuracy** — accept modeled IG-request counts for a first reading,
   or first add a network log to the adapter (separate code change)? Default:
   **accept the model**.
6. **Burst post + window** — which already-flagged hot post to burst-sample, and the
   window (~1–2 days at 6h/12h). Runs **after** the steady-state ramp + IP recovery.

## Non-claims
Design / measurement-method only — not authorization for the run, a proxy build, or
any push/PR; not validation, readiness, buyer-proof, or commercial authorization.
"Shipped" / "feasibility-proven" refer to the instruments' states recorded in
`ig_capture_findings_consolidated_v0.md`; the reel path is not built. All
extrapolation figures in this method spec were illustrative until the RUN landed; use
`ig_r_probe_results_v0.md` for current R evidence.

**Purity boundary (Delta 3):** the probe **MEASURES READS only**. It must **never write
typed `metric_observations`** (the IG typed-capture core, PR #158) during its runs — that
would couple the read-measurement to the **unbuilt IG producer**. Capture-wiring belongs to
the IG-producer slice, not here. (This design's base predates #158; keep it so — do not
rebase the probe onto the typed-capture producer.)
```
