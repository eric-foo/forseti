# Silver Census Gating Read — Unit (b) Handoff (v0)

```yaml
retrieval_header_version: 1
artifact_role: Lane handoff prompt (docs/prompts/handoffs/; cold-start packet for silver/vault unit (b))
scope: >
  Cold cross-lane handoff for the silver/vault lane's first post-bronze unit:
  the READ-ONLY silver census gating read. Enumerate every silver writer and
  silver/derived reader from the live gates and code (never from a handoff's
  carried copy), classify each reader's CURRENT sibling-selection behavior,
  and bring the build-vs-classify ledger to the owner BEFORE any code is
  written. Gated on the owner ratifying the silver/vault goal frame at
  kickoff. Carries the bronze end-state, the ratification gate, drift
  guards, and the confirm-don't-trust load contract.
use_when:
  - Kicking off silver/vault unit (b) in a fresh thread, after (or while obtaining) the owner's goal-frame ratification.
  - Checking what the silver census read must produce before units (c)/(d) may be scoped.
stale_if:
  - The build-vs-classify ledger has been delivered and owner-steered (then unit (b) is done history).
  - The owner re-frames the silver mission away from the proposal in the parent handoff.
authority_boundary: retrieval_only
```

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (bronze closure end-state + silver touchpoint gate rows +
    parent silver/vault handoff; compare targets pinned in-repo)
  edit_permission: docs-write (this handoff artifact only)
  target_scope: docs/prompts/handoffs/data_lake_silver_census_gating_read_handoff_v0.md
  dirty_state_checked: yes (authored on claude/silver-census-read-handoff off origin/main @ 045db196)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound by the artifact-folders overlay file and the in-repo handoff pattern.
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-07-04
- created_by_lane: bronze census closure lane (provenance only, not authority)
- workspace: the receiving lane's own fresh checkout/worktree off `origin/main`
- handoff_path: docs/prompts/handoffs/data_lake_silver_census_gating_read_handoff_v0.md
- expected_branch: read-only unit — work from `origin/main`; the ledger deliverable, if durable, lands on a fresh docs branch per the standing workflow
- expected_head: `origin/main` at or after this packet's merge (run `git fetch origin` FIRST — two prior receiving lanes failed on stale local `origin/main` refs)
- expected_dirty_state_including_handoff_file: clean tree; this packet is committed, not dirty
- load_rule: confirm-don't-trust — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## RATIFICATION GATE (do this first)

The parent handoff's goal frame is a PROPOSAL. Before any census work,
obtain the owner's ratification (or re-frame) of:

1. **Mission**: make Silver the trustworthy READ layer — every silver record
   lineage-anchored and policy-fingerprinted, sibling supersession EXPLICIT,
   every silver consumer enumerated and reading through a defined selection
   rule, vault record shapes schema-versioned; optimizing for behavioral
   signals, not artifact existence.
2. **V-signals (drafts)**: V1 lineage-closed; V2 selection-defined (one
   tested rule names the current sibling — kills the F-IGRC-001 class
   generally); V3 consumer-enumerated (silver census + reader contract
   gate); V4 vault-versioned (schema tokens close the weak-envelope class);
   V5 second-cycle-zero for silver derivation cadence.
3. **Unit order after (b)**: (c) supersession/selection design (owner-steered
   high-lock-in fork), then (d) vault schema tokens — or as re-ordered by
   the owner.

Source: `docs/prompts/handoffs/data_lake_silver_vault_lane_handoff_prompt_v0.md` (resolve on PR #662, branch `claude/silver-vault-lane-handoff`; if #662 has merged, read it on `origin/main`).
Without ratification: stop after presenting the frame; do not start the census.

## Goal Handoff

Pending ratification (fields from the proposal above; not authority until
the owner ratifies):

- long_term_goal: a trustworthy data lake whose layer-completion and read-correctness claims are executable.
- anchor_goal: deliver the silver build-vs-classify ledger — every silver writer/reader enumerated from live source with its selection behavior classified — so the owner can steer unit (c) with evidence.
- success_signal: the ledger names zero unverified rows (each row cites the gate line or code path it was read from), classifies every reader's sibling-selection behavior, and the owner can decide build-vs-classify per row without opening the code.

## Open Decision / Fork

- decision: none inside unit (b) itself — the unit EXISTS to produce the
  decision input for the owner's unit-(c) fork (selection helper vs
  supersession facts vs latest-policy-fingerprint convention). Drift risk,
  not choice: do not pre-decide that fork in the ledger; present observed
  behavior and let the owner steer.
  - owner of the call: owner (unit (c) is flagged high-lock-in — a read-layer contract).
  - precedent to respect: the projection-sweep precedent — consumer tracing
    killed 5 of 6 planned builds; expect the ledger to shrink the build list.

## Drift Guard

- READ-ONLY unit: no code edits, no lake writes, no gate-membership changes,
  no supersession design (unit c), no schema tokens (unit d).
- Enumerate from the LIVE gates and code — never trust any handoff's carried
  writer/reader list (including this packet's own inherited-context list; it
  seeds navigation only).
- Live-lake reads (if the reader-behavior census needs real record shapes)
  require a fresh per-turn owner grant; never write to the lake; the
  in-repo code and gates are the default and usually sufficient evidence.
- F-IGRC-001 is the motivating defect class (a consumer selected a STALE
  sibling via a lexical accident) — classify selection behavior with that
  lens, but do not patch anything found; record it.
- Standing workflow applies to any DURABLE deliverable (fresh docs branch,
  preflight, retrieval header, PR; owner merges). Later implementation
  units inherit the full pattern (assumption-gate → /fused; full-suite
  junitxml validation; tracked-scan gates re-run post-commit; per-unit
  cross-vendor review commission).

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
  (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first, always).
- NOTE a repo-wide rename landed 2026-07-04: the product root moved
  `orca/product/` → `forseti/product/` (PR #666). Older artifacts cite
  `orca/product/...` paths; resolve them under `forseti/product/`.
- targets to enter the ladder: the ledger below.
- must load first: `AGENTS.md`, overlay README, the parent silver/vault
  handoff (ratification gate), then the producer gate's touchpoint counter.

### Earlier-decided concepts (inline gist + verify pointer)

- **Bronze is closed by executable claim**: `run_seam_cadence.py --run`
  observed exit 0 with zero output on the live lake (2026-07-04). Decided in
  `docs/decisions/bronze_consumer_census_closure_record_v0.md` ("Closure
  observed" section; lands via PR #679 if not yet on your `origin/main`).
  Verify before relying.
- **The S3-style sibling multiplication is by design**: every policy bump
  re-derives fresh audit/silver/projection records; readers must select
  among siblings. Decided in the seam contract
  `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`. Verify before classifying selection behavior.
- **F-IGRC-001**: `projection_ig_reels_grid` record-id policy is coupled to
  `instagram_metric_seed`'s lexical tie-break; a consumer once selected a
  stale sibling lexically. Decided in
  `docs/review-outputs/adversarial-artifact-reviews/` (F-IGRC-001 record).
  Verify before citing.

## Active Objective

Produce the silver build-vs-classify ledger: every silver writer and every
silver/derived reader on current `origin/main`, enumerated from the
machine-checked gate and the code, each reader classified by how it selects
among sibling records today (lexical walk, latest-mtime, lane_dir free-walk,
pinned id, view-mediated, etc.), with a per-row build-vs-classify
recommendation for the owner to steer unit (c).

## Exact Next Authorized Action

1. `git fetch origin`; read `AGENTS.md` + overlay README; state isolation.
2. Present the ratification gate to the owner; stop if not ratified.
3. Regenerate the writer/reader enumeration from
   `EXPECTED_NON_RAW_LAKE_TOUCHPOINTS` in
   `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
   plus greps for `append_silver_record` / `lane_dir` / `derived` walks;
   diff your enumeration against this packet's seed list and note every
   difference.
4. For each reader, read its selection code path and classify its current
   sibling-selection behavior with the F-IGRC-001 lens.
5. Deliver the ledger to the owner (chat-first; durable copy per overlay if
   asked) with per-row build-vs-classify recommendations. STOP — unit (c)
   is a separate owner-steered lane.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (root), `.agents/workflow-overlay/`.
- User constraints: owner ratifies the frame; owner steers unit (c); owner
  merges PRs; live-lake reads owner-granted per turn.
- Source-read ledger (seed list — REGENERATE, never trust):
  - `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
    - Role: `EXPECTED_NON_RAW_LAKE_TOUCHPOINTS` is the machine-checked
      writer/reader touchpoint census (the counter test keeps it exact).
    - Load-bearing: yes
    - Compare target: the counter includes rows for
      `capture_spine/creator_profile_current/{silver,youtube_silver,tiktok_silver}_metric_producer.py`
      (`append_silver_record`), `silver_metric_reader.py` (`lane_dir`: 3),
      `cleaning/{fragrantica,basenotes,parfumo}_lake.py`
      (`append_silver_record`), `data_lake/silver_record.py`
      (`append_record`), `data_lake/sov_readout.py` (`lane_dir`),
      `runners/run_sov_extraction_quality_eval.py` (`lane_dir`),
      `data_lake/derived_retrieval_views.py` (`lane_dir`) — as of
      `origin/main` @ `045db196`; reread-required.
    - Last checked: 2026-07-04
    - Reuse rule: regenerate the full row set at lane start; the seed above
      is navigation, not the census.
  - `orca-harness/data_lake/silver_record.py`
    - Role: the silver record helper (writer-side shape).
    - Load-bearing: yes; Compare target: reread-required.
    - Last checked: 2026-07-04; Reuse rule: reread at lane start.
  - `orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py`
    - Role: the known lane_dir ×3 silver reader — a primary selection-behavior subject.
    - Load-bearing: yes; Compare target: reread-required.
    - Last checked: 2026-07-04; Reuse rule: reread at lane start.
  - `orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py` + `instagram_metric_seed` module
    - Role: the F-IGRC-001 motivated reader (derived walk, lexical tie-break).
    - Load-bearing: yes; Compare target: reread-required (locate the module by grep — the sender did not pin its path).
    - Last checked: never fully read by sender; Reuse rule: gating read for its ledger row.
  - `docs/prompts/handoffs/data_lake_silver_vault_lane_handoff_prompt_v0.md` (resolve on PR #662, branch `claude/silver-vault-lane-handoff`)
    - Role: the parent lane handoff — mission proposal, V-signals, unit queue.
    - Load-bearing: yes (for the ratification gate only)
    - Compare target: its "Proposed goal frame" + "Unit queue" sections; reread-required.
    - Last checked: 2026-07-04; Reuse rule: the frame is a proposal until the owner ratifies.
  - `docs/decisions/bronze_consumer_census_closure_record_v0.md`
    - Role: bronze end-state + residual ledger (the weak-envelope class unit (d) closes).
    - Load-bearing: yes; Compare target: "Closure observed — 2026-07-04" section (via PR #679 if unmerged); reread-required.
    - Last checked: 2026-07-04; Reuse rule: reread on current origin/main.
- Source gaps: the exact current reader set is unverified by the sender
  beyond the gate rows above (deliberate — enumeration IS the unit).
- Strict-only blockers: goal-frame ratification (owner); any live-lake read
  (per-turn grant).
- Not-proven boundaries: nothing here proves any reader is correct or
  broken; the ledger classifies behavior, it does not adjudicate it.

## Current Task State

- Completed upstream: bronze closed by executable claim (census record +
  PR #679); cadence runner + gates live; reconcile purge race hardened
  (PR #681, review pending).
- Not started: everything silver-side. This unit is the first.

## Superseded / Dangerous-To-Reuse Context

- Any `orca/product/...` path in older artifacts — resolve under
  `forseti/product/...` (PR #666 rename).
- The parent handoff's "Starting census facts" writer/reader list — seed
  only; the packet's own instruction ("verify by regenerating, never trust
  this copy") governs.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: this packet's gate-row seed against the live
  counter; the parent handoff's frame text (PR #662 pin); the bronze closure
  section (PR #679 pin); the rename note (forseti/ exists, orca/ does not).
- Load outcomes: `REUSE` only after those verify; missing sections →
  `STALE_REREAD_REQUIRED` (fetch current main); unratified frame → stop at
  step 2 of the next actions.

## Do Not Forget

The unit's whole value is evidence-before-build: the projection-sweep
precedent killed 5 of 6 planned builds. Deliver the ledger and stop; do not
let census momentum turn into unit (c) design.
