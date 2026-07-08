# Org-Motion + Demand Signal — Strategy Discovery Note (v0)

- **Status:** DISCOVERY / PRE-DECISION INPUT. Not a ratified decision, not a spec, not validation, not source-of-truth.
- **Feeds:** ICP/wedge decision (`docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md`), judgment spine, capture spine.
- **Captured:** 2026-06-11. **Branch:** `ecr-sp3-timing-deriver-slice1` (shared/volatile). **Uncommitted.**
- **Non-claims:** no ratified ICP, no validation/acceptance, no implementation authorization. The empirical findings in §2 are from owner-attended, read-only archive.org probes on 2026-06-11 through the existing `source_capture/adapters/archive_org.py` adapter — they are scouting evidence, NOT a formal method-validation run.

---

## 1. The pivot (agreed)

- **Away from** the company dossier (name / HQ / industry / size band) — Google-able, ~zero differentiated value. Competitive-intelligence-of-record is likely a separate, lower-value spine.
- **Toward org-motion**: hiring composition (ATS) + headcount trend (LinkedIn) as a **corroboration / leading-indicator** signal — explicitly **not** a standalone product.
- Personnel = **moves/composition** (durable, costly to fake), **not** posts/engagement (the fake layer).

## 2. Empirical findings (probe evidence — perishable, recorded)

- **LinkedIn company pages are densely archived** (not hollow, correcting an earlier wrong read): Microsoft **1,722** Wayback snapshots, Sephora **625**. Logged-out SSR shell, ~400–500KB bodies.
- **Extractable + structured** from the logged-out archived bytes: exact follower count (Microsoft `28,330,532`), JSON-LD `numberOfEmployees` (`232,349`), company-size band (`10,001+`). Real values, not boilerplate.
- **Senior-moves roster is behind auth** — logged-out bytes carry only ~23 sampled `/in/` profiles + a "See all employees" link. Dated senior-move tracking is therefore a **forward/live** signal, **not** archive-backtestable.
- **ATS (Greenhouse) archives the full job list**: Figma board = **141** snapshots, **198** job postings + **99** department tags + **17** locations in the bytes. Openings/hiring-composition **is** archive-backtestable.
- **No-look-ahead primitive already exists**: `select_snapshot` uses `timestamp <= cutoff`. The armory `archive_org` adapter + the judgment-spine memo-at-cutoff / outcome-calibration pattern are already present — backtest harness is mostly assembled, not greenfield.
- **Caveats / lessons (confirm-don't-trust):**
  - CDX latency scales with how much is archived under a URL (5–60s+); heavy URLs time out. Fix: date-bound the CDX query (`&from=&to=`) or use the availability "closest" API.
  - Target choice matters: `boards.greenhouse.io/airbnb` (~2 rows) and `/gitlab` (0 rows) were near-empty — bad test targets, not evidence ATS is unarchived.
  - URL-form artifact: `/company/sephora/` (trailing slash) = 0 snapshots; `/company/sephora` = 625. A lone prior-fitting data point is not a finding.

## 3. Signal sufficiency (agreed)

- **Org-motion alone:** not enough for an investment **thesis**; **is** enough for a **screen** (rank-and-shortlist feeding a human analyst — a filter has a low bar).
- **Decision-worthy unit = FUSION:** demand (social/reviews/search) + org-motion corroboration.
- **Highest-value reads = DIVERGENCES:** demand↑ + staffing↑ (durable) / demand↑ + staffing flat (flash or capital-constrained) / staffing↑ + demand flat (betting ahead, or they see something not yet in consumer data).
- It is a **probability-shifter feeding a human**, not an oracle. The backtest calibrates how much weight it earns.

## 4. The three spines (agreed architecture intuition)

- **Entity-resolution spine = the Palantir-shaped JOIN asset.** Maps surface forms (LinkedIn slug, Workday/Greenhouse slug, Reddit spelling, brand vs parent) → one canonical entity. The **brand→parent hierarchy is load-bearing in beauty** (e.g. *The Ordinary → DECIEM → Estée Lauder*); signals must roll up/down the tree. Build **narrow** (the wedge's entities), designed to widen.
- **Clean data = necessary, not sufficient.** It removes garbage-in; it does not supply the judgment. Clean *for the entities this decision touches*, not globally.
- **Chain:** entity spine → fused signals → backtestable cases → **judgment spine** (the calibrated read). Org-motion archive-backtest = the **cheapest first case-generator** (provable from public archives, no waiting).
- **Smallest-complete breadth** for the first judgment ≈ **2–3 entity-joined sources** (demand + org-motion corroboration + one outcome anchor like sales rank/funding) — not "everything." Breadth is scoped by the decision.

## 5. Buyer / GTM (agreed direction — ICP NOT decided)

- **Both buyers want demand as the primary signal.** Buy-side (PE / family office) and operators (brands) differ in the *decision* (invest vs operate), not the *lead signal*. (Corrects an earlier "PE = org-motion" framing.)
- **Lead with the demand signal**; org-motion = corroboration + the cheap backtestable proof layer.
- **First buyer chosen by REACHABILITY, not signal-fit.**
- **PE / family office = worst FIRST door** (gatekept + org-motion-insufficient-for-them + demand-is-the-better-input). Destination, not first door.
- **Owner has no warm leads** (stated 2026-06-11) → relationship doors unavailable → **backtest-as-public-proof becomes the primary door-opener** (content + cold-outreach ammo). Likely first design partner = an indie/DTC brand insights lead or a consumer seed/VC fund (reachable cold + proof).

## 6. Open / not decided / load-bearing assumptions

- **The ICP itself** — route to the ICP/wedge lane. NOT decided here.
- **Load-bearing assumption:** the social/demand spines will actually produce a reliable demand signal. The entire "lead with demand" recommendation rests on this — if those spines are further from working than the LinkedIn/ATS layer, the sequencing changes.
- **Beauty-brand ATS coverage** unverified: do the target beauty brands use Greenhouse/Lever/Ashby, and are their boards archived? Per-brand check.
- **Next-build choice** unresolved: build org-motion as the judgment-spine case-generator, or settle the ICP first.

## Next authorized step

Carry §3–§5 into the ICP/wedge lane. No build/implementation is authorized by this note.
