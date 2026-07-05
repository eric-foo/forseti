# Seam Cadence Concurrent Availability-Reconcile Failure — Investigation Handoff (v0)

```yaml
retrieval_header_version: 1
artifact_role: Lane handoff prompt (docs/prompts/handoffs/; cold-start packet for a new investigation lane)
scope: >
  Cold cross-lane handoff for an unresolved defect-or-noise question surfaced
  while verifying an unrelated fix: a live run_seam_cadence.py --run invocation
  produced dozens of FileNotFoundError/PermissionError entrypoint_failed
  results on indexes/availability/*.json paths while another process was
  confirmed concurrently touching the same live data lake. Carries the exact
  failure evidence, the suspected mechanism (a delete-then-rebuild-whole-index
  pattern with no lock in reconcile_availability_per_packet), the open
  fork between benign transient noise and a real concurrency-safety gap, and
  the receiver's load contract.
use_when:
  - Investigating why a run_seam_cadence.py or any *_catchup.py run failed with
    FileNotFoundError/PermissionError on indexes/availability/*.json.
  - Deciding whether reconcile_availability_per_packet needs concurrency
    hardening (the receiving lane owns data_lake/consumption.py and the
    cadence orchestrator).
stale_if:
  - The open fork is resolved (transient noise confirmed on an idle-lake
    re-run, or a hardening fix is merged and adjudicated) -- then this is
    done history.
  - reconcile_availability_per_packet's delete-then-rebuild shape changes on
    main for unrelated reasons before this is investigated.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-07-04
- created_by_lane: parfumo-blocked-capture-fix lane (PR #676 author; provenance only, not authority)
- workspace: the receiving lane's own fresh checkout/worktree off `origin/main`
- handoff_path: docs/prompts/handoffs/seam_cadence_concurrent_availability_reconcile_investigation_handoff_v0.md
- expected_branch: receiver creates a fresh lane branch off `origin/main` (per the standing workflow below)
- expected_head: `origin/main` at or after `045db1966f24c252d45e0780f744eda8b9586294` (the merged parfumo fix, PR #676 — unrelated to this investigation but the current tip at authoring time)
- expected_dirty_state_including_handoff_file: clean tree at lane start; this packet is committed, not dirty
- load_rule: confirm-don't-trust — re-verify every load-bearing fact below against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

Derived from this session's observation while verifying an unrelated fix (not a ratified `workflow-goal-framing` output — treat as orientation):

- long_term_goal: a trustworthy data lake whose layer-completion claims are executable, never asserted — cadence runs must be safe to execute whenever an operator needs to check bronze/cleaning completion, including when another process is concurrently using the lake.
- anchor_goal: determine why `run_seam_cadence.py --run` produced dozens of `entrypoint_failed` results (mixed `FileNotFoundError`/`PermissionError` on `indexes/availability/*.json` files) while another process was confirmed to be concurrently touching `F:\orca-data-lake`, and close the gap if it is a real robustness defect rather than accepting it as expected/benign.
- success_signal: either (a) a clean re-run of `run_seam_cadence.py --run --skip-asr` against the live lake when it is confirmed idle, proving this run's failures were purely transient concurrent-access noise with no code defect, or (b) if the same failure class reproduces on an idle lake (i.e., it is NOT actually about concurrency), a scoped root-cause diagnosis plus a fix proposal — with no fake-success path (never silently swallowing or masking a real reconcile failure).

## Open Decision / Fork

- decision: is the observed failure pattern (a) benign/expected noise from two processes concurrently reconciling the same lake with no locking, requiring no code change (just "don't run cadence commands against a lake another process is using, or retry"), or (b) a real robustness gap where `reconcile_availability_per_packet` should tolerate a concurrent writer (lock, retry-once, or a safer non-destructive rebuild strategy) instead of surfacing raw `FileNotFoundError`/`PermissionError` per packet?
  - options:
    1. **Accept as expected concurrent-access noise** — document that cadence/catch-up runners must not be run concurrently against the same lake root (or must expect and tolerate transient failures when they are), and that a retry when idle is the correct operator response. No code change.
    2. **Harden `reconcile_availability_per_packet`** (`orca-harness/data_lake/consumption.py:369-421`, see Source-Read Ledger below) to be safe under a concurrent writer — e.g., a lock file, an atomic per-file write instead of delete-then-rebuild-the-whole-directory, or a bounded retry-once on `FileNotFoundError`/`PermissionError` before surfacing `availability_reconcile_failed`.
    3. **Something else the receiver's own investigation surfaces** — the sender's read of the code (below) is a plausible mechanism, not a proven root cause; the receiver may find a different explanation.
  - already constrained / off the table: touching the parfumo blocked-capture fix (merged, verified, unrelated — see Drift Guard); changing the seam cadence's core two-cycle/exit-code semantics; any change to `run_seam_cadence.py`'s gating logic to make failures pass silently (that would recreate exactly the fake-success risk the bronze census closure lane exists to prevent).
  - trade-offs: option 1 is cheap but leaves the cadence fragile under exactly the multi-operator/multi-agent conditions this repo actually runs in (the owner confirmed concurrent access is a real, current condition, not a hypothetical). Option 2 is more durable but touches a function every cleaning/ECR/projection catch-up runner shares (`reconcile_availability_per_packet` is explicitly the "single-sourced" F-ECR-001 shape per its own docstring, consumed by a seam-coverage contract test) — a change here has wide blast radius and should go through `workflow-assumption-gate` → scoping before any edit, not be improvised.
  - owner of the call: the receiving lane, after reproducing/diagnosing; if option 2, likely needs owner sign-off given the shared-function blast radius.
  - recommendation: reproduce first (confirm the lake is idle, retry, see if it's clean) — if clean, this may still be worth a hardening pass given the owner has confirmed concurrent multi-operator access is normal here, not exceptional. Investigate the code shape named below before deciding; do not assume it is definitely the mechanism.

## Drift Guard

- Do not touch the parfumo blocked-capture fix (`orca-harness/runners/run_parfumo_cleaning_catchup.py`'s `_blocked_capture_evidence_or_none`/`_is_zero_handles_validation_error` and its tests) — already merged as PR #676 (commit `045db196`), independently verified clean in isolation this session (see Commands And Verification Evidence). This investigation is not a continuation of that lane and must not reopen it.
- Do not assume the parfumo fix caused the cadence-wide failure. It was proven unrelated: the standalone `run_parfumo_cleaning_catchup.py --check`/`--run`/`--check` sequence (which exercises exactly the merged fix) completed cleanly with zero errors, both before and independent of the full `run_seam_cadence.py --run` that then failed across many *other* entrypoints.
- Never write to `F:\orca-data-lake` outside the sanctioned runners; live-lake reads/runs need a fresh owner grant each turn (per-turn; the permission classifier enforces this — do not work around it). Before any live-lake run in this investigation, confirm with the owner whether the lake is currently idle or still concurrently in use.
- Do not relax `run_seam_cadence.py`'s fail-loud exit-code semantics or the census record's classification sections to make a future run "pass" — a masked reconcile failure is a fake-success path, the exact thing the bronze cadence exists to prevent.
- Standing workflow (inherit verbatim, same as the parfumo lane): fresh branch off `origin/main`; `workflow-assumption-gate` → `/fused` for any code change; full-suite validation via the project's existing test invocations with `ORCA_DATA_ROOT` cleared; re-run tracked-scan gates AFTER committing; explicit `git push -u origin <lane>`; owner merges (or self-merge only under the protected-action guard's verified exception); per-unit repo-mode cross-vendor delegated review commission for any non-trivial patch (pin commit SHA; non-Anthropic who-constraint; owner couriers; home-CA adjudicates) — see the parfumo lane's own delegated review record for the concrete shape: `docs/review-outputs/parfumo_cleaning_blocked_capture_delegated_code_review_v0.md`.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `AGENTS.md` + `.agents/workflow-overlay/README.md` first, always).
- targets to enter the ladder: `orca-harness/data_lake/consumption.py` (`reconcile_availability_per_packet`, line 369; `pickup`, line 329), `orca-harness/runners/run_seam_cadence.py` (the cadence orchestrator that calls each lane's `run_catchup`/entrypoint in cycles), `docs/decisions/bronze_consumer_census_closure_record_v0.md` (the record whose "Live dry-run status" section will need updating once the parfumo blocker's clearance — already independently confirmed this session — and this new investigation's outcome are both known).
- already loaded by the sender (weak orientation, 2026-07-04; not authority): a partial read of `reconcile_availability_per_packet`'s body (quoted below); no read of `run_seam_cadence.py`'s cycle-orchestration logic itself.
- must load first: `AGENTS.md`, overlay README, then `run_seam_cadence.py` in full (the sender did not fully read this file), then `reconcile_availability_per_packet` and its caller `pickup` in full.

### Earlier-decided concepts (inline gist + verify pointer)

- **Bronze completion signal is executable**: `runners/run_seam_cadence.py --run` must exit 0 (second cycle zero + final pending sweep zero). Decided in `docs/decisions/bronze_consumer_census_closure_record_v0.md` (PR #664) + F-CAD-001 adjudication. Verify before actionable use.
- **`reconcile_availability_per_packet` is the single-sourced, shared reconcile shape (F-ECR-001 adjudicated)**: every cleaning/ECR/projection catch-up runner must consume this one helper rather than carrying a local copy; a seam-coverage contract test enforces that. This means a fix here (option 2 above) is NOT locally scoped to one runner — it changes shared behavior for ECR, fragrantica, basenotes, parfumo, fragrance-review, and ig-reels-grid catch-up simultaneously. Verify the exact enforcement test before editing (`reread-required` — the sender did not locate/open this contract test this session).
- **The parfumo blocked-capture fix is done and unrelated**: merged PR #676 (`045db1966f24c252d45e0780f744eda8b9586294`), live-verified this session (packet `01KWCG89CBFH90Z4ABKYWKF5VE` acked, standalone parfumo pending count went 1 → 0, confirmed twice). Do not re-verify this as part of the current investigation; it is closed history.

## Active Objective

Determine whether the mixed `FileNotFoundError`/`PermissionError` failures seen across multiple catch-up entrypoints during a `run_seam_cadence.py --run --skip-asr` live run — while another process was concurrently using the same lake — indicate a real concurrency-safety gap in `reconcile_availability_per_packet`'s delete-then-rebuild-the-whole-index pattern, or were benign transient noise from that concurrent access with no code defect; then close the gap (if real) or document the operational constraint (if not).

## Exact Next Authorized Action

1. Read `AGENTS.md` + `.agents/workflow-overlay/README.md`; state isolation (fresh branch off `origin/main`).
2. Read `orca-harness/runners/run_seam_cadence.py` in full and `orca-harness/data_lake/consumption.py`'s `pickup`/`reconcile_availability_per_packet` in full (the sender only partially read the latter — see Source-Read Ledger).
3. Request a per-turn owner grant to confirm whether `F:\orca-data-lake` is currently idle (ask the owner directly, as this session did).
4. If idle: re-run `python orca-harness/runners/run_seam_cadence.py --run --skip-asr --data-root F:\orca-data-lake` once under the grant. Clean exit 0 (or the expected two-residual truthful-red shape excluding the parfumo/ASR items, which are already known-resolved/known-deferred) supports the "transient" hypothesis (option 1). A repeat of the same `entrypoint_failed` pattern on an idle lake disproves "concurrency-only" and points at a different, still-unknown mechanism — do not assume it is still concurrency-related if the lake was confirmed idle.
5. Independently of step 4's outcome, read `reconcile_availability_per_packet`'s delete-then-rebuild pattern (quoted below) and judge whether it is safe under a concurrent second writer on general principles (not just this one observed run) — this is the sender's suspected mechanism, not a confirmed one.
6. If a real gap is found, classify it into option 2's shape (lock / atomic swap / retry-once) and run `workflow-assumption-gate` → `/fused` before any edit, given the shared blast radius named above.
7. Update `docs/decisions/bronze_consumer_census_closure_record_v0.md`'s "Live dry-run status" section with this investigation's outcome once resolved (it currently still shows the now-superseded pre-parfumo-fix state — see Superseded / Dangerous-To-Reuse Context).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (root), `.agents/workflow-overlay/` (Forseti authority).
- User constraints: live-lake reads/runs owner-granted per turn; owner confirmed concurrent lake access was occurring during this session's observed failure; owner merges PRs (self-merge only under the protected-action guard's verified exception).
- Source-read ledger:
  - `orca-harness/data_lake/consumption.py`
    - Role: shared availability-index reconcile helper (`reconcile_availability_per_packet`, line 369) consumed by every catch-up runner in the cadence.
    - Load-bearing: yes
    - Compare target: git blob hash `f0d59077f82e5df1cd8e0f4b8620f3d79798dfde` at commit `045db1966f24c252d45e0780f744eda8b9586294`. Quoted excerpt (lines 388-393, the suspected mechanism): the function first does `if avail.is_dir(): for entry_file in avail.glob("*.json"): entry_file.unlink()` (deletes every existing availability-index file), then `avail.mkdir(parents=True, exist_ok=True)`, then walks `raw/<shard>/<packet_id>/` and calls `root.record_availability(packet_id)` per committed packet to regenerate the index one file at a time (lines 395-413) — with **no lock and no per-file exception handling for the delete/rebuild itself** (only `root.record_availability` calls are wrapped in try/except, at line 405-413). The sender did not read `root.record_availability`'s own implementation.
    - Last checked: 2026-07-04 (partial read — lines 369-413 only; the full file and `pickup` at line 329 were not read).
    - Reuse rule: reread-required (full file) before any strict claim or edit.
  - `orca-harness/runners/run_seam_cadence.py`
    - Role: the cadence orchestrator; iterates entrypoints across (per this session's observed output) at least 2 cycles, calling each lane's catch-up/derive entrypoint including `run_parfumo_cleaning_catchup.py`.
    - Load-bearing: yes
    - Compare target: git blob hash `d4b5e5d1db06f9e22421ab2a092fbe365e8694e8` at commit `045db1966f24c252d45e0780f744eda8b9586294`.
    - Last checked: never opened by the sender this session (only its output was observed) — this is a gating read for the receiver.
    - Reuse rule: reread-required; the sender has NOT verified how this orchestrator sequences/isolates entrypoint calls, whether it runs them serially or with any parallelism, or how `--skip-asr` interacts with the observed failures.
  - `orca-harness/runners/run_parfumo_cleaning_catchup.py`
    - Role: control case proving the merged parfumo fix is unrelated to this investigation's failure.
    - Load-bearing: yes (for the "parfumo fix is unrelated" claim only, not for this investigation's own root cause)
    - Compare target: git blob hash `031fa1b4a8da5279e94c05ce148ab388e3ac73f3` at commit `045db1966f24c252d45e0780f744eda8b9586294` (post-merge state, includes both the fix and the delegated-review patch).
    - Last checked: 2026-07-04, exercised live (not just read) — see Commands And Verification Evidence.
    - Reuse rule: closed history; do not re-verify as part of this investigation.
  - `docs/decisions/bronze_consumer_census_closure_record_v0.md`
    - Role: the record whose "Live dry-run status" section names the parfumo blocker (now resolved) and will need to reflect this investigation's outcome once known.
    - Load-bearing: yes
    - Compare target: git blob hash `d088bb11bbd1154533840d3971bb92c8815f9b5f` at commit `045db1966f24c252d45e0780f744eda8b9586294`. This hash predates today's parfumo-clearance and cadence-failure observations — the record has NOT been updated with either yet.
    - Last checked: 2026-07-04 (read for the prior parfumo-fix lane; not re-read for this handoff).
    - Reuse rule: reread-required before any update; treat its current dry-run section as stale relative to the events in this packet.
  - Live lake `F:\orca-data-lake`
    - Role: the environment where the failure was observed; confirmed by the owner to have had concurrent external access during this session's run.
    - Load-bearing: yes
    - Compare target: reread-required (owner-gated per-turn read/run grant); no snapshot of `indexes/availability/` was taken.
    - Last checked: 2026-07-04, during the failing `run_seam_cadence.py --run --skip-asr` invocation (see Commands And Verification Evidence) — state has almost certainly changed since (the other process was actively mutating it).
    - Reuse rule: never act on this investigation's classification without re-running against the live lake under a fresh grant.
- Source gaps: `run_seam_cadence.py`'s full body (cycle/orchestration logic), `data_lake.consumption.pickup`'s full body, `root.record_availability`'s implementation, and whatever seam-coverage contract test enforces the F-ECR-001 single-sourcing rule — none of these were opened this session. This is the gating read.
- Strict-only blockers: any live-lake run needs a fresh per-turn owner grant and (per this investigation) an explicit confirmation the lake is idle first; any edit to `reconcile_availability_per_packet` needs `workflow-assumption-gate` → scoping given its shared multi-runner blast radius.
- Not-proven boundaries: nothing in this packet proves the delete-then-rebuild pattern in `reconcile_availability_per_packet` is actually the mechanism behind the observed failures — it is the sender's plausible-but-unverified read of the code, offered as the strongest lead, not a diagnosis. The sender did not observe the other process's own operations and cannot rule out an entirely different cause (e.g., a network-drive/`F:\` transient I/O issue independent of any application-level race — the census record's own prior dry-run section separately noted "5 transient F:-drive I/O failures (WinError 433 device errors / one Errno 13)" on an earlier run, which is a different error class than this session's `FileNotFoundError`/`PermissionError` pair but establishes that this drive has a history of transient I/O flakiness worth ruling out too).

## Current Task State

- Completed (by the sending lane, this session): the parfumo blocked-capture fix, merged as PR #676, live-verified (packet acked, pending count 1→0, confirmed twice) — fully closed, not part of this investigation.
- Broken or uncertain (the subject of this handoff): the cadence-wide `entrypoint_failed` pattern observed during one `run_seam_cadence.py --run --skip-asr` invocation; root cause not yet diagnosed, only a plausible mechanism identified from a partial code read.

## Workspace State

- Branch: `claude/seam-cadence-concurrent-access-handoff` (created fresh off `origin/main` for this handoff only; the receiver should create its own fresh lane branch for the actual investigation/fix work rather than reusing this one).
- Head: `045db1966f24c252d45e0780f744eda8b9586294` (= `origin/main` at authoring time).
- Dirty or untracked state before handoff: clean.
- Dirty or untracked state after writing the handoff file: this one new file, staged/committed by the sender before handoff (see courier block for exact path); otherwise clean.
- Target files or artifacts: none yet touched for the investigation itself (read-only observation only, this session).
- Related worktrees or branches: `claude/parfumo-empty-handles-fix` (the now-merged, closed parfumo lane branch — safe to ignore/delete per normal hygiene, not part of this investigation).

## Changed / Inspected / Tested Files

- `orca-harness/data_lake/consumption.py`
  - Status: unmodified; partially read (lines 369-413) this session.
  - Role: shared availability-index reconcile helper.
  - Important observations: delete-then-rebuild-the-whole-directory pattern with no lock (see Source-Read Ledger quoted excerpt).
  - Symbols or sections: `reconcile_availability_per_packet` (line 369), `pickup` (line 329, not read).

## Frozen Decisions

- The parfumo blocked-capture fix stays as merged; this investigation does not reopen it.
- Any fix to `reconcile_availability_per_packet` (if pursued) must not weaken `run_seam_cadence.py`'s fail-loud exit-code semantics or the F-ECR-001 per-packet failure-visibility shape (a corrupt/racing packet must still surface as a visible status, never silently vanish).

## Mutable Questions

- Is the delete-then-rebuild pattern in `reconcile_availability_per_packet` actually reachable by two concurrent OS-level processes in this repo's real usage pattern (i.e., does anything else besides a human/agent manually invoking these runners ever run them on a schedule, such that true concurrent invocation is expected/routine rather than an edge case)? Resolves by reading `run_seam_cadence.py` and any scheduler/cron wiring for it.
- Is the correct fix a lock, a retry-once, or a structural change to avoid delete-then-rebuild entirely (e.g., only regenerating entries for packets whose manifest changed, rather than wiping and redoing everything)? Resolves after reproducing and reading `root.record_availability`.

## Superseded / Dangerous-To-Reuse Context

- The census record's (`docs/decisions/bronze_consumer_census_closure_record_v0.md`) current "Live dry-run status" section still names the parfumo packet as an open blocker — this is now stale; the parfumo fix is merged and live-verified. Do not treat that section as current without first re-reading it, and update it as part of closing out whichever investigation (parfumo clearance, this one, or both) lands next.
- The census record's separately-noted "5 transient F:-drive I/O failures (WinError 433 device errors / one Errno 13)" from an earlier dry-run is a DIFFERENT error class (WinError 433 / Errno 13) than this session's `FileNotFoundError`/`PermissionError` pair — do not conflate them as the same known issue, but do treat the drive's prior flakiness history as relevant context when weighing "concurrency race" vs. "drive I/O flakiness" as the mechanism.

## Commands And Verification Evidence

- Command (owner-granted, 2026-07-04, confirming the parfumo fix in isolation — NOT the failing command):
  ```
  python orca-harness/runners/run_parfumo_cleaning_catchup.py --check --data-root F:\orca-data-lake
  python orca-harness/runners/run_parfumo_cleaning_catchup.py --run --data-root F:\orca-data-lake
  python orca-harness/runners/run_parfumo_cleaning_catchup.py --check --data-root F:\orca-data-lake
  python orca-harness/runners/run_parfumo_cleaning_catchup.py --run --data-root F:\orca-data-lake
  ```
  Result: `1` → `{"packet_id": "01KWCG89CBFH90Z4ABKYWKF5VE", "source_surface": "parfumo_product_page_direct_http", "status": "acked_no_cleanable_content"}` → `0` → empty output (byte-unchanged noop). Clean throughout; establishes the control case.
- Command (owner-granted, 2026-07-04, the FAILING command — this investigation's subject):
  ```
  python orca-harness/runners/run_seam_cadence.py --run --skip-asr --data-root F:\orca-data-lake
  ```
  Result: exit code 1. Dozens of `{"cycle": 1, "entrypoint": "run_ecr_catchup.py", ..., "status": "derived"}`-shaped successes, THEN a run of failures in both cycle 1 and cycle 2, verbatim examples (entrypoint name, error class, and path pattern are load-bearing; the specific packet ids are not — they vary):
  ```
  {"cycle": 1, "entrypoint": "run_fragrantica_cleaning_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWJ2G508SBQPD9HCRBWPMHZB.json'", "status": "entrypoint_failed"}
  {"cycle": 1, "entrypoint": "run_basenotes_cleaning_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPFX146F2G9NVP18NJRNXJ3.json'", "status": "entrypoint_failed"}
  {"cycle": 1, "entrypoint": "run_parfumo_cleaning_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG0TG8P9J01299Y1S60NZT.json'", "status": "entrypoint_failed"}
  {"cycle": 1, "entrypoint": "run_fragrance_review_projection_catchup.py", "error": "PermissionError: [WinError 5] Access is denied: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG1R779AV458XJQ2RD97DV.json'", "status": "entrypoint_failed"}
  {"cycle": 1, "entrypoint": "run_ig_reels_grid_projection_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG27VFANTQ3Z5TCRWFVHHZ.json'", "status": "entrypoint_failed"}
  {"cycle": 1, "entrypoint": "run_asr_transcript_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG34K9WH40RNSYQYYM4XC2.json'", "status": "skipped_asr_pending_check_failed"}
  {"cycle": 2, "entrypoint": "run_ecr_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG3J25578XT7D95QRJE17K.json'", "status": "entrypoint_failed"}
  {"cycle": 2, "entrypoint": "run_fragrantica_cleaning_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG3Y1STP6YDRNPYYK4Z2F9.json'", "status": "entrypoint_failed"}
  {"cycle": 2, "entrypoint": "run_basenotes_cleaning_catchup.py", "error": "PermissionError: [WinError 5] Access is denied: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG40ZRBFY6SEB1X6YAZ25M.json'", "status": "entrypoint_failed"}
  {"cycle": 2, "entrypoint": "run_parfumo_cleaning_catchup.py", "error": "PermissionError: [WinError 5] Access is denied: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG5B07BJE0HR3DEC8AMZ0B.json'", "status": "entrypoint_failed"}
  {"cycle": 2, "entrypoint": "run_fragrance_review_projection_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG5QV9S8REG3Z0NB2VT9YX.json'", "status": "entrypoint_failed"}
  {"cycle": 2, "entrypoint": "run_ig_reels_grid_projection_catchup.py", "error": "FileNotFoundError: [WinError 2] The system cannot find the file specified: 'F:\\\\orca-data-lake\\\\indexes\\\\availability\\\\01KWPG67A6JS5FHBHEH06TA8F9.json'", "status": "entrypoint_failed"}
  {"cycle": 2, "entrypoint": "run_asr_transcript_catchup.py", "pending": 54, "status": "skipped_asr_compute"}
  {"cycle": "post", "entrypoint": "run_asr_transcript_catchup.py", "pending": 54, "status": "post_cycle_pending"}
  ```
  Note the second cycle-1 `run_parfumo_cleaning_catchup.py` entry above shows `entrypoint_failed`, NOT `acked_no_cleanable_content` — this is expected and does NOT contradict the control-case result: it hit the same shared-index race on a *different, unrelated* packet id (`01KWPG0TG8P9J01299Y1S60NZT`, not `01KWCG89CBFH90Z4ABKYWKF5VE`) before ever reaching the fixed code path for the specific blocked packet.
  Owner confirmed live, when asked directly, that another process/person was concurrently touching `F:\orca-data-lake` during this run.
  - Re-run target so the receiver can confirm rather than trust: repeat `python orca-harness/runners/run_seam_cadence.py --run --skip-asr --data-root F:\orca-data-lake` under a fresh owner grant once the owner confirms the lake is idle.

## Blockers And Risks

- Per-turn owner read/run grant required before any live-lake command (hard gate), plus (specific to this investigation) explicit confirmation the lake is idle before treating a clean re-run as proof of "transient."
- `reconcile_availability_per_packet` is shared across every catch-up runner in the cadence (F-ECR-001 single-sourced convention) — any fix has wide blast radius and must not be improvised without `workflow-assumption-gate` → scoping.
- Risk of conflating this session's error class (`FileNotFoundError`/`PermissionError`) with the census record's previously-noted, differently-shaped `F:`-drive transient I/O failures (`WinError 433`/`Errno 13`) — keep them distinct until proven related.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: all four source-read-ledger compare targets above (blob hashes at `045db1966f24c252d45e0780f744eda8b9586294`); whether `origin/main` has moved past that commit (fetch and compare); whether the live lake is currently idle (ask the owner fresh, do not assume the state from this packet's authoring time persists).
- Load outcomes: `REUSE` only after all of the above verify AND the owner has freshly confirmed lake-idle status for this turn; a moved `origin/main` with changes touching any of the four ledger files → `STALE_REREAD_REQUIRED`; an unreadable lake or no grant → stop and request the grant, same as this packet's own sending lane did.

## Do Not Forget

The parfumo fix is done and unrelated — do not let this investigation's failures cast doubt back on PR #676; the control-case evidence above already rules it out. The actual open question is narrow: is the shared availability-index reconcile safe under concurrent multi-process access, which this repo's owner has confirmed is a real, current operating condition, not a hypothetical.
