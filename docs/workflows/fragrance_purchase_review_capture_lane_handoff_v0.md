# Handoff Packet — Fragrance Purchase-Review Capture Lane (foundation done → interlinked next steps)

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff
scope: >
  Cold handoff for the fragrance purchase-review CAPTURE lane. The capture
  FOUNDATION (find -> grab -> durably preserve) is built and merged, but
  reliable-at-scale capture and any monitoring are NOT built. The remaining
  steps are tightly interlinked with the data-lake lane and want a joint design.
use_when:
  - Routing the fragrance purchase-review lane's next steps (Yotpo fallback,
    real-data-through-tee, recurring monitor, typed Attachment Record entry).
  - Co-designing the typed evidence record + monitoring substrate with the
    data-lake lane.
  - Checking the lane's honest capability status (what is proven vs not).
authority_boundary: retrieval_only
```

> Refresh note: this supersedes the original v0 framing ("lane done; next unit = the typed AR entry"). The accurate picture is below: the foundation is done, but **reliable capture and monitoring are not**, and the next steps are co-dependent with the data-lake lane.

## Load Contract

- packet_version: 2
- mode: max
- created_at: 2026-06-30
- created_by_lane: claude/fragrance-review-claim-ceiling-contract (sender; provenance only, not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca` (Orca repo; authored from worktree `.claude/worktrees/distracted-newton-1323ec`)
- handoff_path: `docs/workflows/fragrance_purchase_review_capture_lane_handoff_v0.md` (this file; refreshed in place)
- expected_head (of `origin/main` at handoff): `14a07922` (Merge pull request #512) — **main moves fast; re-check and reread compare targets against the current HEAD**
- expected_dirty_state_including_handoff_file: this file is modified on a docs branch off `origin/main`; the merged lane code is clean on `origin/main`
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: for fragrance purchase-review, reliably FIND review-positive product pages, GRAB their review data, durably PRESERVE an exact replayable copy, and MONITOR it over time — the source-capture discipline, so a typed, queryable evidence record can be built and kept current.
- anchor_goal: design the **typed evidence record + the durable-store + the monitoring cadence together with the DATA-LAKE lane**, because they are one substrate — then close the capture-side reliability gaps that feed it. (Owner routes; see Open Decision.)
- success_signal: real fragrance review data flows find -> grab -> durable lake -> a typed record -> recurring re-capture, with cross-vendor capture uniform (Judge.me AND Yotpo) and the typed record carrying the provenance + series/cadence that monitoring produces.

## Open Decision / Fork

- decision: how to sequence and co-own the interlinked next steps, given the capture lane and data-lake lane share the same substrate?
  - options:
    1. **Data-lake drives the typed AR entry first** (sets the durable schema); capture feeds it. Risk: the schema gets designed without the monitoring/series + multi-vendor realities the capture side knows.
    2. **Capture closes its gaps first** (Yotpo fallback + real-data-through-tee) to produce real lake data, THEN co-design the typed record on real data. Risk: defers the schema decision; real data may be small.
    3. **Joint architecture pass NOW spanning both lanes** — design the typed evidence record + monitoring/series shape together before either builds, then split implementation. Costs a coordination step up front.
  - already constrained / off the table: the typed AR entry is **data-lake-lane-owned**, not capture; capture must not build it. The claim ceiling ("not a durable AR / no closure") is now CODE-enforced (see Drift Guard) — do not regress it.
  - trade-offs: the interlink is real and tight — F6 already shows a capture-side choice (positional `file_id`) directly binds the data-lake-side schema; monitoring sits on the lake's append-on-rederive + demand-durability series fields; the typed record must carry what monitoring produces. Designing the pieces separately risks a record that can't hold the series/provenance, or a monitor with nowhere coherent to write.
  - owner of the call: human owner / Chief Architect.
  - recommendation: **option 3 (joint architecture pass first)**, because the typed record, durable store, and monitoring cadence are the same substrate and the lanes are co-dependent. Surface the cross-lane coordination cost to the owner before committing.

## Drift Guard

- Do NOT claim the lane can "reliably capture and monitor." Honest status: the FOUNDATION is built (find + grab + preserve), proven at PILOT scale / on a SYNTHETIC fixture for the lake step. Reliable-at-scale capture and ANY monitoring are NOT built (see Current Task State).
- Do NOT regress the claim ceiling. "Not a durable Attachment Record / no AR physicalization / no 7-check closure" is now enforced by `orca-harness/tests/contract/test_fragrance_review_claim_ceiling_contract.py` (PR #492, merged). A future edit that drops the non-claim turns that test red — keep it red-on-drop.
- The typed AR entry is DATA-LAKE-lane work; building it in the capture lane violates lane ownership. F6: it must reference/supersede the preserved bodies WITHOUT inheriting the positional `file_id` or staging-path semantics, and should round-trip the per-response provenance (response_origin/kind/url/index) + operator widget_route/source_id the tee leaves unattributed — its OWN contract test, not this lane's.
- Do NOT auto-start the owner-owned chip `task_816ff6af` ("Extend fragrance companion auto-fallback to Yotpo v3").
- Start any new unit on a NEW branch/worktree off updated `origin/main` (`14a07922` at handoff, but it moves — re-fetch). Prior fragrance branches are spent.
- The harness runs via `uv` and must ALWAYS use `--frozen` (a non-frozen `uv run` once mutated `uv.lock`); add `--with pytest` for tests, `--with certifi` for live TLS.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/README.md` (read before project work, per `AGENTS.md`); repo-map entry point `docs/workflows/orca_repo_map_v0.md`.
- targets to enter the ladder: the four fragrance runners + the lake module + the data-lake substrate + the AR contract doc (all in the ledger below).
- already loaded (weak orientation; not authority): this packet.
- must load first (before strict/actionable steps): the data-lake AR contract + `data_lake/root.py` + the demand-durability series machinery (for the monitoring shape), reread against current `origin/main`.

### Earlier-decided concepts (inline gist + verify pointer)

- The lake step was deliberately scoped to a "preserved-body tee pilot" that makes NO typed-AR / closure claim, after a GPT-5.5 cross-vendor review; the ceiling is now code-locked.
  - decided in: PRs #489 (tee) + #492 (claim-ceiling contract), merged.
  - compare target: `reread-required` (read `fragrance_review_lake.py` docstring + the claim-ceiling contract test on current `origin/main`).

## Active Objective

The capture lane's FOUNDATION (find review-positive PDPs, grab their review-widget bytes, durably preserve an exact copy + project a view) is built and merged. This packet routes the INTERLINKED next steps toward "reliably capture + monitor", which require co-design with the data-lake lane.

## Exact Next Authorized Action

1. Owner decides sequencing from Open Decision (recommended: a joint capture + data-lake architecture pass first).
2. If option 3: run `workflow-architecture-planning` spanning both lanes against the AR contract doc + the demand-durability series machinery; obtain a bounded build authorization before any implementation.
3. Stop condition: do not begin typed-AR-entry implementation without the architecture pass + bounded authorization (the AR contract "does not authorize runtime implementation").

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (kernel) + `.agents/workflow-overlay/`.
- Source-read ledger (all HEAD-bound to current `origin/main`; reread before strict/actionable use):
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` — Role: the typed AR entry's contract (7 checks; "does not authorize runtime implementation"). Load-bearing: yes. Compare: `reread-required`.
  - `orca-harness/data_lake/root.py` — Role: lake substrate (load_raw_packet fail-closed re-hash, append_record append-only, rebuild_availability packet-grained, for_test). Load-bearing: yes. Compare: `reread-required`.
  - `orca-harness/source_capture/writer.py` + `runners/run_source_capture_durability_series.py` — Role: the demand-durability SERIES machinery (series_id / cold_start / intended_cadence / re_capture) that MONITORING would build on. Load-bearing: yes (for the monitor step). Compare: `reread-required`.
  - `orca-harness/source_capture/fragrance_review_lake.py` + `runners/run_fragrance_review_lake_packet.py` + `tests/test_fragrance_review_lake_pilot.py` + `tests/contract/test_fragrance_review_claim_ceiling_contract.py` — Role: the shipped tee + its claim ceiling (now code-locked). Load-bearing: yes. Compare: `reread-required`.
  - `orca-harness/source_capture/fragrance_rendered_widget_companion.py` + `runners/run_fragrance_rendered_widget_companion.py` — Role: the GRAB step (capture). The Yotpo auto-fallback gap lives here (companion auto-builds Judge.me fallback, not Yotpo). Load-bearing: yes (for the Yotpo step). Compare: `reread-required`.
  - `orca-harness/source_capture/fragrance_review_discovery.py` + `runners/run_fragrance_review_discovery.py` — Role: the FIND step (discovery). Load-bearing: no (built + run). Compare: `reread-required` only if extending.
- Not-proven boundaries: the lake tee is proven on ONE synthetic fixture; capture is proven at pilot scale (4/5 retailers); monitoring is NOT built; real pilot data has NOT been run through the tee into a durable lake end-to-end.

## Current Task State

- Completed (merged): FIND (discovery, PR #481), GRAB (companion + Option A pilot, 4/5 retailers), PRESERVE (tee pilot PR #489 + claim-ceiling contract PR #492).
- Partially completed / NOT reliable: GRAB is pilot-level, not at-scale — Yotpo auto-fallback missing (ZGO captured 5/6), and burst rate-limiting dropped Indigo. Operator-run, not an automated pipeline.
- NOT built: MONITOR (no recurring re-capture / cadence / change-detection for fragrance reviews — the tee explicitly declares "does not model an earlier capture"). Real-data-through-tee-into-durable-lake end-to-end NOT run. Typed AR entry NOT built (data-lake lane).

## The Interlinked Next Steps (each names its lane + the interlink)

1. **Yotpo auto-fallback** (capture/companion; owner chip `task_816ff6af`) — makes GRAB uniform across review vendors. Interlink: the typed record can't assume coverage until multi-vendor capture is uniform.
2. **Real data through the tee into a durable lake, end-to-end** (capture produces, data-lake stores) — proves PRESERVE on real data, not synthetic.
3. **Recurring monitor** (cadence re-capture + change detection) — Interlink: sits on the lake's append-on-rederive + the demand-durability series machinery; cadence/series shape is shared with data-lake.
4. **Typed AR entry** (DATA-LAKE lane) — references/supersedes the preserved bodies; F6. Interlink: must carry the provenance + series/cadence that steps 2-3 produce.

## Superseded / Dangerous-To-Reuse Context

- Stale (this refresh corrects it): the original v0 framing "the active objective is complete; the only next unit is the typed AR entry; park the lane."
  - Why stale: it implied the lane was effectively done. The honest picture is a built FOUNDATION with reliable-capture and monitoring still UNBUILT, and the next steps co-dependent with the data-lake lane.
  - Current replacement: this packet's Current Task State + Interlinked Next Steps.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: current `origin/main` HEAD (moves fast); the claim-ceiling contract is green (`pytest tests/contract/test_fragrance_review_claim_ceiling_contract.py`); the AR contract still "does not authorize runtime implementation"; the demand-durability series machinery shape (for monitoring).
- Load outcomes: `STALE_REREAD_REQUIRED` is expected (main advances past `14a07922`); reread the ledger sources against the new HEAD before any strict step.

## Do Not Forget

- "Reliably capture + monitor" is the GOAL, not the current state. Today: foundation built; reliable-at-scale capture and monitoring are NOT built. State that honestly.
- Steps 2-4 share the data-lake substrate — design the typed record + monitoring shape JOINTLY with the data-lake lane, not blindly across a wall.
