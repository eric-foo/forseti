# Forseti Research Engine — God-Tier Strategy v0

```yaml
retrieval_header_version: 1
artifact_role: Research strategy record (research-engine weakness map + maximization plan; not capture authorization)
scope: >
  Evidence-grounded weakness map of the three research-engine spines (CSB,
  Scanning, Capture) and a phased maximization ("god tier") plan: close the
  extraction-to-judgment loop, win demand-origin access for the ratified
  vertical, add orchestration + cost/yield instrumentation, make route/venue
  knowledge compound, then run case-batch volume. Proposal for owner
  adjudication; authorizes nothing.
use_when:
  - Deciding the next research-engine investment (seams vs access vs automation vs memory).
  - Commissioning work on the Scanning->Capture or Capture->ECR handoffs.
  - Checking which research-engine weaknesses are evidence-backed and which fixes are already parked/unmerged.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_research_engine_map_v0.md
  - forseti/product/spines/commission_signal_board/README.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/capture/README.md
  - docs/decisions/forseti_moat_judgment_quality_proof_path_decision_chain_v0.md
  - docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md
stale_if:
  - A capture_request fulfillment loop, route-state ledger, or capture orchestrator is built (Phases P0-P3 land), changing the weakness baseline.
  - The owner adjudicates the forks below (standing cadence, route ledger, board lineage) differently than recommended.
  - The ratified product direction (consumer-demand, >=2 independent venue families, 30-90 day window) is superseded.
  - A later research-engine strategy record supersedes this one.
```

- Status: `PROPOSED_RESEARCH_STRATEGY_V0` — owner adjudication owed. Not owner ratification.
- Method: six parallel read-only inventory lanes (CSB, Scanning, Capture spine docs,
  forseti-harness built reality, failure/lesson corpus, downstream demand), run
  2026-07-10 on this worktree, plus orchestrator spot-checks of the load-bearing
  negative claims (capture_request fulfillment, CSB board count). Counts below are
  as-observed on 2026-07-10; raw capture packets live outside the repo
  (`F:\orca-data-lake`), so repo-observed negatives are stated as repo-observed.

## Verdict In One Screen

The research engine is **design-complete and execution-starved**. Each spine is
individually real — CSB has a working prompt+validator, Scanning has a proven
walk method with a CI receipt gate, Capture has 8 generic Armory adapters plus
proven routes on IG/TikTok/YouTube/Reddit and a pydantic-enforced packet schema
— but the engine **as a system has never run once end-to-end**. Every seam
between the organs is open:

- No scan-emitted `capture_request` has a repo-observed fulfillment; every one
  shows `route_binding_state: unknown`, and later scans re-triage the same
  requests as still-open.
- Exactly 2 real CSB boards exist; boards are write-once snapshots that expire
  rather than compound.
- One real vertical packet (Fragrantica, 210 review cards, 2026-06-28) reached
  the raw lake and stalled before ECR
  (`docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`).
- ECR/Cleaning code is orphaned: the only ECR derivation ever run used an
  off-vertical Wikipedia/Canoo fixture; the 6 cleaning adapters have no
  repo-observed real invocation; Judgment's 14 product-learning cases
  hand-author evidence YAML that mimics ECR field shapes instead of running the
  built deriver.

Meanwhile the ratified product direction
(`docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`) demands exactly
what the engine currently cannot supply: signal **fused across >=2 independent
venue families** inside a **live 30-90 day decision window** — and the
demand-origin venues (buyer-language forums, fragrance-native DBs) are the
least-proven access class, while scans converged on a single family (Parfumo)
and held Reddit deferred even though Capture has a proven Reddit route.

God tier is therefore not "more capability docs" and not "a bigger crawler." It
is: **close the loop, win demand-origin access, add a crankshaft
(orchestration + measurement), make knowledge compound, then run case-batch
volume through the existing evidence-grade discipline** — which is the moat and
must be kept.

## What The Engine Actually Is Today (observed 2026-07-10)

| Layer | Real state | Key evidence |
| --- | --- | --- |
| CSB | Prompt-first manual board generator; 2 real boards ever (1 brand + 1 categorical); validator manual-only, not CI; no write-back loop; name unratified | `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`, `docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md`, `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` |
| Scanning | ~11 scan-shaped artifacts in a 2-week burst (7 on one brand); receipt-shape CI gate live; hidden-venue discovery re-finds the same 2 venues; broad-scout subagent used once; zero cost/latency accounting | `docs/research/orca_discovery_candidate_scan_imaginary_authors_*_v0.md`, `.agents/hooks/check_csb_scanning_artifact.py` |
| Capture | Most-built spine: Armory adapters done; packet schema v1 write-time enforced; proven pilots per family (Reddit 563 rows, TikTok 30/30 videos + 596 comments, IG 365-media pagination + 243-account snowball, YouTube n=10, retail 25 review rows, Fragrantica 1 packet, Quora 1 packet) — but two strongest retail findings sit unmerged, Quora is uncatalogued, no packet is fixture-admitted | `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`, `forseti/product/spines/capture/core/source_capture_toolbox/README.md` |
| Harness | 93 standalone `run_*.py` runners, no orchestrator, no console_scripts, no scheduler; nothing runs unattended; ~242 test files with effectively 0% live-network coverage (the one live test permanently skipped) | `forseti-harness/runners/`, `forseti-harness/tests/integration/test_reddit_screening_read_live.py` |
| Downstream | ECR 7 commits / evidence_binding 3 commits of ~448 harness commits; catchup runners exist with no persisted run state; Judgment capped at product_learning, cases hand-author evidence | `forseti-harness/ecr/`, `forseti-harness/cases/product_learning/`, `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` |
| Demand streams | Two: (1) ratified consumer-demand commissioned cases (moat-gated batch-1), (2) Aphrodite/Creator Signal longitudinal creator graph (IG heartbeat + selective deep capture) — the second explains why social families are most-proven while commissioned-decision venues starve | `docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`, `docs/research/aphrodite_creator_capture_strategy_v0.md` |

A further calibration: a large share of "proven" capture volume (Reddit
r/financialcareers + WSO, Quora B2B, Daimler/Teal recon) predates the
consumer-demand ratification and belongs to superseded directions. The routes
transfer technically; the current vertical's demand-origin coverage is far
thinner than the recon index suggests at first read.

## Weakness Map (ranked)

**W1 — The pipeline has never closed (seams).** The single biggest weakness.
Scanning→Capture: capture_requests carry no fulfillment loop and none is
repo-observed fulfilled. Capture→ECR: "safe to hand to ECR" is a self-discharged
prose checklist (Obligation 16), exercised once off-vertical. ECR→Cleaning→
Judgment: never run on real vertical data; Judgment cases bypass the built code
with hand-authored YAML. Consequence: capture supply already exceeds downstream
consumption (an unconsumed real packet exists), and both stacked commercial
gates (ECR-to-JSG-01, judgment anti-leak) sit behind seams no one has crossed.

**W2 — Demand-origin access is weakest exactly where the product needs it.**
Basenotes Cloudflare-challenged; Fragrantica has no static-HTML route (one
CloakBrowser packet proven); Reddit cold `.json` 403 (warm-context fix known,
not a runner) — yet Capture's proven Reddit route was never used by any scan.
Scans converged on one demand-origin family (Parfumo); every candidate topped
out at `hold_low_commitment` for lack of a second independent origin. Headless
SERP is 100% bot-blocked (0/6); only a visible browser worked. LinkedIn is
policy-blocked. The >=2-independent-venue-family fusion requirement is
currently unreachable.

**W3 — No orchestration, no cadence, no unattended anything.** 93 runners with
no dispatcher; every capture is agent/operator-driven per invocation; recapture
threshold is an explicitly open design knob
(`core_spine_v0_data_capture_spine_obligation_contract_v0.md`, freshness
question); the Armory defers schedulers by doctrine. Aphrodite's heartbeat and
the demand-durability indicators both already strain against this.

**W4 — Knowledge does not compound.** CSB boards are write-once and expire; no
shared controlled route-state vocabulary exists (family READMEs use ad-hoc
prose; "blocked" was the dominant false diagnosis across Daimler/Sephora/
Teal/WSO with no mechanical re-probe gate); the two strongest retail findings
live in unmerged worktrees; no packet has ever been fixture-admitted; scans
rediscover the same hidden venues. The creator registry and recon index are the
only real compounding memory prototypes.

**W5 — Zero cost/yield instrumentation.** No scan or capture records tokens,
wall-clock, or dollar cost; the only timing data is per-query timestamps in two
SERP batch receipts. The engine cannot be optimized, priced, or throughput-
planned, and ceremony-to-output ratio is invisible (git history: ~33% of 120
recent commits were rename/migration mechanics; ~42% of recent commits were
planning docs).

**W6 — Integrity checks are shape-only and drift is live.** The CI CSB-row
check is a string-presence heuristic that never resolves the cited board; three
early scan artifacts carry a closeout state outside the current checker enum;
the most complete scan's own validation section never mentions the mandated
checker; the efficiency-audit checklist shows items open that already landed
(APH-IMPL-1/-3); two guard scripts have confirmed unfixed bugs (HOOK-1 no-ops
on every real edit; HOOK-8 loses its stderr). Lesson→guard conversion is ~50%.

**W7 — Durability and coverage residuals on proven routes.** IG/TikTok durable
media/video preservation unproven (the two highest-signal creator platforms
cannot durably keep their core modality); Quora uncatalogued one-off; AEO has
no schema home; 0% live-network test coverage means route rot is invisible
until a commissioned run hits it.

**W8 — Rename/pointer debt taxes every run.** Live spine pointers
(`spine.yaml`, `harness/validator.md`, `tests/validator_tests.md`,
`docs/workflows/ecr_spine_submap_v0.md`) and two hooks still point at
nonexistent `orca-*` paths; a cold reader following canonical pointers loads
nothing.

What is explicitly NOT weak: the anti-overclaim constitution (packet schema
enforcement, receipt gates, hash-freshness gates, non-claims discipline,
"capture is the obligation, mode is subordinate"). That discipline caught real
overclaims (Quora F1/F2/F4) and is the substance behind an evidence-grade
product. The plan builds on it, never around it.

## What God Tier Means Here

**Any commissioned decision question → fresh (30-90d), provenance-hashed,
multi-venue-family evidence, ECR-admitted, in hours-to-days, at case-batch
scale, with compounding coverage and self-measuring cost — inside the existing
evidence-grade discipline.**

Measurable definition of done (baseline → target):

1. Seam closure: % of capture_requests reaching a terminal tracked state
   (fulfilled / declined-with-reason): **0% → 100%**.
2. Demand-origin venue families captured per commissioned case: **~1 → >=2**
   (ratified floor) → 3+ at god tier.
3. Loop latency (commission → ECR-admitted packets): **never measured →
   baseline in P0 → <=2 days → hours**.
4. Cost visibility: % of scan/capture runs emitting a cost/yield row:
   **0% → 100%**.
5. Route freshness: every proven route live-smoked within 7 days before
   commissioned use: **no live coverage → standing opt-in smoke tier**.
6. Knowledge reuse: % of venues in a new scan pre-known from the route/venue
   ledger (vs rediscovered): **unmeasured → rising trend**.
7. Judgment-input integrity: % of new product-learning cases using ECR-derived
   (not hand-authored) evidence: **0% → 100%**.

## Owner Decisions Applied (2026-07-10)

The owner adjudicated this record on 2026-07-10. Applied here; the plan below
is updated to match:

- **Scope narrowed to the research engine (CSB, Scanning, Capture).** ECR,
  Cleaning, Judgment, and buyer proof are deferred — kept, not retired. P0 is
  re-scoped to STOP at the Capture→ECR handoff line. See
  `docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md`. This
  removes done-condition #7 (ECR-derived judgment evidence) from research-engine
  scope; it returns when the deferral lifts.
- **God-tier target recorded** as the durable north star:
  `docs/decisions/forseti_research_engine_god_tier_target_v0.md`.
- **P0 + hygiene rider commissioned.** Hygiene rider largely landed this turn
  (below). P0 commissioned as
  `docs/research/forseti_research_engine_p0_golden_thread_commission_v0.md`
  (scoped, not yet executed).
- **W2 (demand-origin access)** owner-owned ("Basenotes will be fixed") — P1
  coordinates with that fix rather than duplicating it.
- **W3 (93 runners)** investigated — the "mostly superseded" hypothesis is
  largely false; see the Runner Census appendix.

## The Plan

Ordering logic (Cynefin: complex → risk-first probe before infrastructure):
close the loop once manually before automating it; pull forward only the access
wins that are already discovered/parked; add standing substrate only where
volume proves the need. Scope is now research-engine-only (ECR-onwards
deferred).

### H — Hygiene rider (LANDED 2026-07-10 on this lane, except where noted)

- **[done]** Stale `orca-harness/` pointers repointed to `forseti-harness/` in
  the CSB spine's own canonical surfaces: `spine.yaml` (+ repo_map →
  `forseti_repo_map_v0.md`), `tests/validator_tests.md`, `README.md`,
  `migrations/moved_paths_index.md`; and `ecr_spine_submap_v0.md`. (These were
  fresh findings, not in the efficiency-audit wave plan.)
- **[done]** Two buggy guards fixed + selftested: HOOK-1
  (`check_search_surface_google_route.py`) now relativizes absolute hook-payload
  paths so it no longer no-ops; HOOK-8 (`check_full_gt_claims.py`) now emits
  `additionalContext` JSON on stdout (was lost on stderr) and scans only lines
  changed vs HEAD. Also HOOK-2/HOOK-7 (`header_index.py` `orca` → `forseti`) and
  REF-5 (Armory folder-convention block).
- **[done]** Efficiency-audit checklist reconciled: APH-IMPL-1/-3 marked landed
  (PR #830); HOOK-1/2/7/8 + REF-5 marked landed this turn.
- **[blocked → routed]** RE-CSB-4 (scan-core sha256 provenance pins): re-verify
  FAILED — all four renamed `forseti_*` sources hash-mismatch their pinned
  values, so they drifted in *content*, not just name. A mechanical repoint
  would launder drift; it needs a re-derivation pass, not a hygiene edit.
  Recorded in the wave plan.
- **[owner/other-lane]** Merge-or-close the two parked retail findings
  (Sephora/Bazaarvoice, Ulta Apollo-state) — in unmerged worktrees this lane
  cannot see.

Note: HOOK-1/2/7/8, REF-5, RE-CSB-4 are also tracked by the separate
efficiency-audit lane's wave plan; landing them here (with that plan
reconciled) retires them from that lane to avoid double-work.

### P0 — Golden Thread: close the Scanning→Capture loop once, for real

**Commissioned** as
`docs/research/forseti_research_engine_p0_golden_thread_commission_v0.md`
(scoped, not yet executed). Re-scoped to the research-engine boundary: it STOPS
at Capture→ECR-handoff-ready and does not run ECR/Cleaning/Judgment.

One commissioned decision (beauty/personal-care candidate per ICP; extending an
existing board is acceptable) driven through the engine:

1. CSB board (fresh or lineage-extended) → bounded scan → capture_requests
   emitted **into a new minimal lifecycle ledger** (requested → route_bound →
   captured → handoff_ready → declined-with-reason). The ledger is the smallest
   artifact that makes fulfillment visible forever after, and the core new
   piece P0 builds.
2. Execute the requests via already-proven routes across **>=2 independent
   demand-origin families**: fragrance-native DB (Fragrantica proven; Parfumo
   session route) + Reddit fragrance/beauty subreddits via the proven API/
   screening-read route + retail review rows.
3. Each packet is `source_capture_packet_manifest_v1`-valid, hash-provenanced,
   and Obligation-16 handoff-ready — the boundary line. ECR derivation,
   Cleaning invocation, and Judgment-case feeding are **deferred** (they were
   step 3 in the pre-decision draft; removed from research-engine scope per the
   ECR-onwards deferral, and will be the natural next lane when it lifts).
4. Instrument everything from the first run: tokens, wall-clock, rows, packets
   per stage — the P0 receipts are the cost baseline.

Success = the seam exercised and every outcome visible (fulfilled or
declined-with-reason), or every break named with owner-visible evidence. A run
where most requests end `declined(reason)` with honest mode-ladder receipts
still passes P0 — it closed the loop and produced the baseline. Non-claims: not
buyer proof, not readiness, not the vertical proven.

### P1 — Demand-origin access supremacy (current vertical)

- Reddit-for-fragrance: proven route, unproven vertical — run it on the
  fragrance/beauty subreddits.
- Basenotes: residential-proxy CloakBrowser probe (route named in the Armory,
  unproven), under a mechanical re-probe ladder.
- Fragrantica/Parfumo: from 1 proven packet → repeatable current-window
  capture profile.
- SERP: accept the visible-browser operator-attended route as v0 (headless is
  bot-blocked; mode is subordinate); park headless without further spend.
- Quora: promote the one-off pilot into a catalogued source-family row.
- **Mechanize "blocked is a hypothesis":** recording `blocked` in a recon/route
  artifact requires a mode-ladder receipt (N modes attempted, or explicit skip
  reason) — checker-shaped, per the enforcement-placement doctrine, converting
  the corpus's top prose-only lesson into a gate.
- LinkedIn: accepted residual (policy wall); no automation work.

### P2 — The crankshaft: orchestration + instrumentation + rot detection

- **Batch dispatcher:** one entrypoint consuming a capture_request batch and
  dispatching to family runners with per-lane session isolation (now fixed),
  budget caps, and receipts. Commissioned-batch orchestration, not a standing
  crawler — stays inside current doctrine.
- **Cost/yield ledger:** every runner emits a standard cost row (tokens /
  wall-clock / bytes / rows / outcome); one readout runner aggregates. Target:
  the owner can answer "$ and hours per evidence-unit" from a file.
- **Live-smoke tier:** tiny opt-in suite, one stable-endpoint request per
  proven family, operator-triggered (weekly cadence suggested), never in
  default CI — detects route rot before a commissioned run hits it.
- **Fixture admission:** admit one golden packet per proven family as a durable
  fixture (closes the "no packet ever fixture-admitted" gap and hardens tests).

### P3 — Compounding memory

- **Route-State Ledger (capture-owned):** one YAML, controlled maturity enum
  per family × venue × mode (e.g. proven / partial / blocked-hypothesis /
  policy-blocked / retired) with dated evidence pointers. Scans already must
  cite route state; this gives them one place to cite from. This is the *mini*
  shape of the previously **rejected** venue-registry maximal
  (`docs/decisions/forseti_venue_registry_rejection_decision_v0.md`): dated
  provenance memory owned by Capture (which owns route binding), not a scanning
  authority atlas — surfaced as a fork below, not assumed.
- **CSB board lineage:** new boards inherit prior rows + last-known
  evidence_status on regeneration (write-once auditability preserved,
  compounding added).
- **Lesson→guard pipeline:** run the distillation procedure on the top
  prose-only lessons; add a checklist↔merged-PR reconciliation check so audit
  state cannot silently drift.

### P4 — Batch scale (the payoff)

Run 5-10 commissioned cases through the closed research-engine loop with
orchestrated capture: >=2 demand-origin families each, handoff-ready packets,
measured cost, parallel lanes under per-lane isolation. This is the feedstock
that the deferred moat gates (ECR-to-JSG-01, judgment anti-leak, batch-1) will
consume *when the ECR-onwards deferral lifts* — P4 fills the pantry;
downstream consumption is out of current scope. Aphrodite composition: the
creator heartbeat continues as the longitudinal layer; commissioned cases pull
selective deep capture on demand; both streams share the dispatcher, ledgers,
and smoke tier.

## Owner Forks (decisions needed; recommendation first)

1. **Narrow standing cadence** for named recurring families (demand-durability
   indicators; Aphrodite grid heartbeat) vs strict commissioned-only.
   Recommend: narrow, budget-capped grant for named families only. Highest
   value / medium lock-in; both doctrine layers already strain toward it.
   *(Open.)*
2. **Route-State Ledger** vs the venue-registry rejection precedent —
   **ROUTED 2026-07-10**: owner redirected W4/W5 to a cross-family state model,
   alternatives-first; subsumed by
   `docs/prompts/handoffs/research_engine_cross_family_memory_cost_model_design_handoff_v0.md`.
3. **CSB board lineage** — **ROUTED 2026-07-10** into the same cross-family
   design handoff (whether lineage lives inside the state model or as a CSB
   prompt amendment is one of its mutable questions).
4. **Legacy scan-artifact closeout enum** — **RESOLVED 2026-07-10: grandfather.**
   Implemented this turn: `check_csb_scanning_artifact.py` auto-detection
   (CI `--diff` / `--changed`) skips the 3 pre-contract legacy artifacts
   (`..._mgt_v0.md`, `..._csb_first_venue_eval_v0.md`, `..._core_satellite_csb_v0.md`),
   which each fail 9-16 checks they predate; explicit-path invocation still
   validates strictly. Mirrors the packet schema v0→v1 grandfathering. Selftest
   added.
5. **Judgment-case evidence source** — **out of current scope** (ECR-onwards
   deferred); revisit when the deferral lifts.
6. **AEO schema home**: defer until the P1 visible-browser SERP route proves
   value; then decide. *(Open.)*
7. **capture_request lifecycle-ledger schema** (new; the one lock-in choice in
   P0). Recommend: smallest append-only shape, locked via micro-decision-locking
   at execution, surfaced for confirmation before hardening. *(Open — decide at
   P0 execution.)*

## Accepted Residuals / Anti-Goals

Named residuals (accepted, with upgrade triggers):

- LinkedIn stays policy-blocked; professional-context evidence gap accepted
  until a written-permission route exists.
- Headless SERP parked; SERP stays operator-attended (upgrade trigger: a
  materially different access posture, not more headless attempts).
- IG/TikTok durable media/video preservation unproven; metadata/text layers
  carry until a preservation probe is commissioned.
- Live-network checks stay opt-in/operator-triggered, never default CI —
  account safety over detection latency.

Anti-goals (god tier is NOT):

- No broad crawler, standing monitor, or venue atlas-as-authority.
- No CAPTCHA solving, login automation, cookie import, or commercial scraping
  services (Armory gated list stands).
- No dashboards/UI before the loop closes; no new doctrine layers before
  execution volume — doctrine is the over-supplied asset.

## Known Uncertainties (preserved)

- ECR/Cleaning code may fail on first contact with real packets — P0 is
  designed to expose exactly that; expect a punch list.
- Raw packets live outside the repo (`F:\orca-data-lake`); repo-observed
  negatives could undercount capture volume, though in-artifact
  `route_binding_state: unknown` + re-triage records are positive evidence of
  the open seam.
- Route confidence is partially inflated by superseded-direction captures
  (career/B2B era); vertical-specific behavior (fragrance subreddits,
  Basenotes) is unproven.
- Inventory counts (93 runners, 448 commits, artifact counts) are as-observed
  2026-07-10 by the inventory lanes; not individually re-verified.

## Appendix — Runner Census (W3, investigated 2026-07-10)

Owner question: "why do we have 93 standalone runners — I believe a lot would be
superseded." Census (in-repo, `git log` last-touch + doc-reference count +
test-name match over `forseti-harness/runners/`):

**The "mostly superseded" hypothesis is largely false.** Evidence:

- **91 of 93 runners are referenced by at least one durable doc**; only **2**
  have zero doc references: `run_reddit_agent_view_ab_probe.py` and
  `run_source_capture_proxy_profile_bootstrap.py`. A superseded-leftover set
  would show many zero-reference orphans; it doesn't.
- **Last-touch date is not a supersession signal here.** ~80 of 93 show a
  last-touch of 2026-07-05 — the orca→forseti rename campaign's mass-move date,
  not a real edit — so date cannot distinguish live from dead. (This is the same
  rename debt as W8, here obscuring the census rather than breaking a link.)

**Why 93 exist (the real answer): per-operation CLI by design.** The harness
follows a one-command-per-operation runbook pattern (`docs/source_capture_agent_runbook.md`):
a distinct `run_*` per adapter × operation. The count decomposes into families —
capture-packet-per-adapter (`run_source_capture_*_packet.py`), projection-per-
source (`run_*_projection.py`), catch-up/backfill (`run_*_catchup.py`),
metric-rollup-per-platform (`run_*_metric_rollup_producer.py`), data-lake ops
(`run_data_lake_*`), and probes. This is breadth of coverage, not redundancy;
it is also exactly why P2's single orchestrated dispatcher is worth building —
93 hand-invoked entrypoints is the operability cost of that design, not dead code.

**Genuine trim/lineage candidates (low confidence; verify before any deletion):**

| Runner | Signal | Confidence |
| --- | --- | --- |
| `run_reddit_agent_view_ab_probe.py` | 0 doc refs; `_ab_probe` sibling of `run_reddit_agent_view.py` | med — likely one-off A/B probe |
| `run_source_capture_proxy_profile_bootstrap.py` | 0 doc refs | low — may be live operational tooling used ad hoc |
| `run_case_case001.py` | specific-case sibling of generic `run_case.py` (4 refs) | low-med — likely a superseded single-case script |
| `run_memorization_probe.py` vs `_raw_api.py` | probe pair | low — both may be intentionally retained |
| IG heartbeat trio (`run_source_capture_ig_daily_heartbeat{,_control,_operator}.py`) | active lineage (recent fixes #830) | keep — active, not superseded |

Recommendation: **do not delete on this evidence.** The high-value W3 move is
P2's dispatcher (collapses 93 hand-invocations behind one orchestrated
entrypoint), not pruning — pruning saves little and risks removing a documented
fallback. A proper deletion pass needs the deletion-evidence gate per runner;
the two zero-reference runners are the only reasonable first candidates.
(Census note: the deeper per-runner subagent census was not completed — its
agent hit a spend limit — so the lineage table is from the in-repo signals
above, not an exhaustive read.)

## Non-Claims

This record is analysis and proposal only. It is not owner ratification, not
validation, not readiness, not capture/source-access authorization, not
implementation authorization for any code root, not a schedule commitment, not
buyer proof, and not a claim that any listed weakness has been fixed. The
2026-07-10 hygiene-rider fixes (hook + pointer edits) are verified by their
selftests and the focused unit suite; every other phase requires the normal
per-lane authorization and review flow.
