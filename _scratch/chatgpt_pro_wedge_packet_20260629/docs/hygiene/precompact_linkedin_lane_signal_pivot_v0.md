# Precompact Working Packet — LinkedIn Lane signal-target pivot (personnel + openings)

```yaml
retrieval_header_version: 1
artifact_role: Precompact recovery checkpoint (disposable working packet) for the LinkedIn / competitive-intelligence discovery lane thread
scope: >
  Recovery anchor after manual compaction. Slice 3c-2b (live company-page BrowserFetcher) is
  DONE + committed + live-validated. This turn pivoted the SIGNAL TARGET (owner + deep-think):
  away from a generic company dossier, toward KEY PERSONNEL (public-actor signals) + COMPANY
  OPENINGS (hiring signals). Captures that pivot + the validated state + the next move.
authority_boundary: retrieval_only
supersedes: docs/hygiene/precompact_linkedin_lane_slice3c2b_v0.md
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ my commits 132a34b (slice) + 2b0f927 (hydration fix); HEAD 342f70a (volatile, structure lane on top) — verify by SHA, not position
```

## Restore Contract
- packet_version: 1
- mode: max
- workspace: C:\Users\vmon7\Desktop\projects\orca
- checkpoint_path: docs/hygiene/precompact_linkedin_lane_signal_pivot_v0.md
- expected_branch: ecr-sp3-timing-deriver-slice1 (SHARED + VOLATILE — a coordinator sweeps in-flight work into checkpoint commits)
- expected_head: 342f70a at checkpoint, but HEAD is NOT the anchor. Anchor = commits 132a34b + 2b0f927 + the 161-test pass.
- recovery_rule: confirm-don't-trust. Verify 132a34b + 2b0f927 exist; run the LinkedIn tests (expect 161); do NOT sweep the dirty tree (other lanes).

## Active Objective
Build the LinkedIn / outside-in competitive-intelligence discovery lane. Slice 3c-2b (the live attended company-page BrowserFetcher) is COMPLETE: built, cross-vendor reviewed (F1-F4 applied), 161 tests pass, LIVE-VALIDATED on real logged-in pages (Blackstone, Sephora), committed. **This turn the owner rejected the "generic company dossier" direction and set a new SIGNAL TARGET: key personnel (public-actor signals) + company openings (hiring signals).**

## Exact Next Authorized Action
1. **Do NOT build yet.** The direction is set but unscoped.
2. Next move = **`workflow-deep-thinking` + `workflow-assumption-gate` on the OPENINGS slice** (the recommended next slice — highest value, lowest risk). Decide: (a) SOURCE — public ATS boards (Greenhouse / Lever / Ashby) or company careers page (defensible, uniform) vs LinkedIn Jobs (ToS-gray); lean ATS/careers; (b) the job-posting MODEL shape (new candidate_class e.g. hiring_signal/job_opening, or a new observation/signal type — an architecture decision); (c) the defensibility tradeoff (openings pull toward defensible non-LinkedIn sources → advances the long-term legally-defensible goal).
3. Bind to a concrete intelligence DECISION/THEME first (owner-owned) — the genericized POC showed the value is theme-bound, not per-row facts.
4. **Personnel = parallel track**, reuses the EXISTING person-candidate model (senior_role_or_public_actor_basis); public actors only, no rosters, intelligence-not-contacts.
5. Then `/fused` to build, once scoped + gated.

## Authority And Source Ledger
- Repo instructions: CLAUDE.md -> AGENTS.md -> `.agents/workflow-overlay/`. Default-allowed = docs/decisions/prompts/reviews/overlay; implementation needs explicit bounded authorization (`/fused` or accepted owner instruction).
- Source-read ledger (reread before scoping the openings slice):
  - `docs/product/data_capture_spine/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md` — the Candidate Row Schema + DEFINED signals (~L203-234): classification (entity_type, candidate_class incl. creator_or_influencer), business_relevance_note/theme, visible_influence_numbers (follower/connection-band/subscriber/engagement) + influence trajectory, person `senior_role_or_public_actor_basis`. **NO company facts by design; even location is dropped at projection.** Reread for the openings model shape.
  - `docs/workflows/linkedin_lane_operator_pilot_plan_v0.md` — capture phases (Discovery / Bounded-Watch / Graph-Frontier / Semantic-Projection / Promotion) + guardrails; "jobs" + "company page/post" are named capture units; business/org rows = low-sensitivity, person rows require a public-actor basis.
  - `orca-harness/source_capture/adapters/{direct_http*,browser_snapshot}.py` + `docs/adapter_author_contract.md` — the armory HTTP/browser adapters = the DEFENSIBLE path for ATS/careers openings (reuse, don't reinvent).
  - `orca-harness/capture_spine/linkedin_live_runtime/{fetcher,runtime,minimizer}.py` + `linkedin_live_adapter/{models,validation,projection}.py` — the validated SPINE; downstream (minimize→validate→project) is source-agnostic, reuse for openings.
  - `docs/product/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md` — influence-over-time (if personnel/influence-trajectory pursued).
- Not-proven boundaries: harness claim = "module + its tests pass" ONLY. Live LinkedIn capture = owner-accepted POC-risk, ToS-gray, NOT legally-defensible. Live driver path owner-validated, not unit-tested.

## Current Task State
- COMPLETE + COMMITTED (verify by SHA): slice 3c-2b = `132a34b` (extractor.py, browser_driver.py, fetcher.py[+BrowserFetcher], __init__.py, test_linkedin_live_runtime_browser_fetcher.py, adjudication record, no-repo bundle — swept by coordinator) + `2b0f927` (the SPA content-hydration `content_ready_selector` fix). 161 LinkedIn tests pass.
- LIVE-VALIDATED: Blackstone (display_name='Blackstone', follower band '2M') + Sephora ('SEPHORA','3M') — clean minimized bags, no person/HTML leakage; fail-closed correct on un-hydrated pages + on a wrong slug (L'Oréal, dropped). Cross-vendor GPT-5.5 review F1-F4 adjudicated+applied (F2 mechanism corrected by home model).
- THIS TURN (analysis only, no build): deep-think -> signal-target pivot to personnel + openings; openings-first via defensible ATS/careers source.
- Broken/uncertain: none of mine.

## Workspace State
- Branch: ecr-sp3-timing-deriver-slice1 (shared, volatile). HEAD 342f70a (structure lane). My commits 132a34b + 2b0f927 present.
- Dirty/untracked: OTHER lanes only (judgment-spine: judgment_spine_consolidation_map_v0.md, manifest_v0.md; demand_projection_f6_r6 review bundle/wrapper/outputs; capture_spine handoff prompt). NONE mine — do NOT sweep. This checkpoint file is a new untracked file.
- Off-repo POC tools (Desktop, throwaway operator tools — NOT committed): `validate_linkedin_live.py` (one-page eyeball), `linkedin_capture_run.py` (full pipeline + JSONL courier), `linkedin_capture_linkedin_lane_live_scouting_001.jsonl` (2 captured rows: Blackstone, Sephora), `chrome-poc-profile\` (a logged-in Chrome profile). The raw `linkedin_live_dump.html` was deleted (raw DOM hygiene).

## Frozen Decisions
- **SIGNAL TARGET PIVOT (owner, this turn):** NOT a company dossier — generic industry/size/HQ/founded = static commodity, freely available, low decision-value; owner-rejected. YES = **key personnel + company openings** (dynamic, intent-revealing, leading indicators of competitor strategy).
- **Openings-first:** highest value + lowest risk (job posts = business content, not person data). Best source = **public ATS boards (Greenhouse/Lever/Ashby) or company careers page** (public, uniform, DEFENSIBLE) over LinkedIn Jobs (ToS-gray) — advances the legally-defensible goal; reuses armory `direct_http`, not the CDP driver.
- **Personnel = narrow, high-constraint:** public actors ONLY (named exec/founder/spokesperson/public appearance + concrete basis), no employee rosters, no contacts (contacts = the DEFERRED Outreach Lane, out of bounds). Reuses the existing person-candidate model.
- **The 3c-2b plumbing is the reusable SPINE:** CDP driver + fetch→minimize→validate→project. Downstream is source-agnostic; only the extractor (+ for openings, a small model addition) is new per surface.
- **Standing default:** consumer-found upstream-validator gaps fold into the owning validator (no re-ask).

## Mutable Questions
- Openings source: ATS (Greenhouse/Lever/Ashby) vs company careers page vs LinkedIn Jobs (lean ATS/careers for defensibility + uniformity).
- Openings model shape: new candidate_class (hiring_signal / job_opening) vs new observation/signal type — architecture decision (scope via assumption-gate).
- The concrete intelligence decision/theme to bind to (owner-owned).
- run_live_capture per-capture error handling: committed runtime stays fail-closed; resilient-skip is done at the operator-script level (linkedin_capture_run.py loops per-target). Revisit if a batch runtime is built.

## Superseded / Dangerous-To-Reuse Context
- `docs/hygiene/precompact_linkedin_lane_slice3c2b_v0.md` — STALE; slice 3c-2b now DONE + committed + live-validated. This packet supersedes it.
- "Company dossier / generic company facts (industry, size, HQ, founded)" enrichment idea — **REJECTED** by owner this turn (not valuable). Do not build it.
- L'Oréal third-company validation — dropped (wrong slug; the lane correctly fail-closed). Generalization already shown by Blackstone + Sephora.
- Method pins (current, freshness-gate before any no-repo bundle): adversarial_artifact_review_v0.md@5fc263a1, review-lanes.md@43b1793d.

## Commands And Validation Evidence
- Tests: `C:\Users\vmon7\AppData\Local\Programs\Python\Python312\python.exe -m pytest <repo>\orca-harness\tests -k linkedin` with `$env:PYTHONPATH = "C:\Users\vmon7\Desktop\projects\orca\orca-harness"`. Last run: **161 passed**.
- Live validation (owner-run, attended): start Chrome `--remote-debugging-port=9222 --user-data-dir=...chrome-poc-profile` (fully quit Chrome first; use 127.0.0.1 not localhost — IPv6), logged into LinkedIn; then `python validate_linkedin_live.py "<company-url>"` or `linkedin_capture_run.py "<url>" ...`.
- Commit (only when asked, branch-guarded): verify branch==ecr-sp3; `git add -- <explicit paths>` then `git commit -m ... -- <paths>`; never `git add -A`; `git show --stat HEAD` after. NOTE the volatile branch: a prior "commit" was swept into the coordinator's 132a34b — confirm by SHA, and re-commit only a genuine diff.

## Blockers And Risks
- **No blocker to scoping** the openings slice (analysis/scoping is default-allowed). Building needs `/fused` after deep-think + assumption-gate.
- **Volatile shared branch:** the coordinator periodically commits all in-flight work into checkpoint commits (132a34b). My `git commit` once reported "nothing to commit" because my files were already swept. Always re-verify branch + exact file state + by-SHA before trusting/committing.
- Openings-via-LinkedIn-Jobs would stay ToS-gray; ATS/careers sources are the defensible alternative (the recommended direction).
- Don't commit live-captured data to the repo without a retention/decision-frame decision (the JSONL is local scouting output, candidate/scouting tier, NOT a Data Capture handoff).

## Recovery Instructions
- Required checks: (1) `git log --oneline -1 132a34b` and `... 2b0f927` — confirm present; (2) run the LinkedIn tests — expect 161; (3) confirm the dirty tree is still other-lane work (do not sweep).
- Recovery outcomes: REUSE if both SHAs exist + 161 pass — continue at Exact Next Authorized Action (deep-think + assumption-gate on the openings slice). STALE_REREAD if a SHA is missing (coordinator squash/rebase) — re-locate by commit message. BLOCKED_DRIFT if my committed files were altered by another lane — stop + report.
- Reread before scoping: the discovery-lane architecture (Candidate Row Schema), the pilot plan (capture units + guardrails), the armory direct_http/browser adapters.

## Do Not Forget
- Commit ONLY when asked; branch-guard (ecr-sp3); `git add -- <paths>` then `git commit -- <paths>`; never `git add -A`; the branch is volatile (coordinator sweeps — verify by SHA).
- Signal target = **personnel + openings**, NOT a company dossier (owner-rejected). Openings-first, via DEFENSIBLE ATS/careers sources (not LinkedIn Jobs).
- Personnel = public actors only, no rosters, intelligence-not-contacts (contacts = deferred Outreach Lane).
- Minimization holds: no profile bodies / contact / follower-connection lists / content / org-chart. POC-risk, ToS-gray, owner-present, not legally-defensible (long-term goal legally-defensible → favors ATS/careers).
- The validated 3c-2b spine (driver + minimize→project) is reusable; only the per-surface extractor (+ openings model addition) is new.
- Desktop POC tools are off-repo throwaway; the JSONL is local scouting output (not committed, not a handoff).
