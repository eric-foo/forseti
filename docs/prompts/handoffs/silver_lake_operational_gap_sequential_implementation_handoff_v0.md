# Silver Lake Operational Gaps — Sequential Implementation Handoff (v0)

```yaml
retrieval_header_version: 1
artifact_role: Cold-agent sequential implementation commission
scope: >
  Commission the observed Silver-lake operational gaps one work unit at a
  time, beginning with cadence systemic-I/O failure amplification. Each
  receiver implements, validates, dogfoods, lands, and stops after exactly one
  dispatched queue item. This packet records the 2026-07-19 scheduled-run
  evidence and the boundaries that must survive every fix.
use_when:
  - Dispatching one numbered queue item below to a fresh implementation lane.
  - Diagnosing the 2026-07-19 Forseti Daily Lake Cadence failure.
stale_if:
  - The dispatched item is already closed on main.
  - The named cadence, availability, map, census, or staging seams materially
    change; re-read current main and narrow the work against the new state.
authority_boundary: retrieval_only
```

## Commission and prompt preflight

```yaml
forseti_start_preflight:
  agents_read: required_by_receiver
  overlay_read: required_by_receiver
  source_pack: repo-overlay-bound
  edit_permission: implementation-authorized
  target_scope: exactly_one_explicitly_dispatched_queue_item
  dirty_state_checked: receiver_must_verify_clean
  blocked_if_missing: >
    A numbered queue item, a fresh isolated worktree off current origin/main,
    or the runtime/live-lake access needed by that item's acceptance checks.

prompt_preflight:
  output_mode: file-write
  write_destination: receiver implementation lane and its per-lane PR
  template_kind: handoff
  template_status: explicit_owner_authorized_sequential_implementation
  input_prompt_source: docs/prompts/handoffs/silver_lake_operational_gap_sequential_implementation_handoff_v0.md
  edit_permission: implementation-authorized
  targets: only the files and live operations required by the dispatched item
  branch: fresh codex/ branch in an isolated worktree based on current origin/main
  dirty_state_allowance: clean receiver only; stop on unexpected modified or untracked files
  reviews: normal project CI and risk routing; findings-first only when review is commissioned
  doctrine_change: >
    item-local classification required; do not alter durable lake or workflow
    doctrine unless the dispatched outcome makes it necessary, and then follow
    direction-change propagation in the same work unit
  report_destination: receiver chat and PR body/checks; no standalone completion report by default
  external_source_boundary: the F: lake and Windows Scheduled Task are observed runtime state, not repository authority
  repo_map_decision: not_needed
  repo_map_reason: exact owning seams and candidate files are named per item
```

There is no installed `success implement` skill in the authoring environment.
This commission therefore binds the intended behavior explicitly: smallest
complete implementation, focused validation, one bounded live dogfood where
safe, fresh-read verification, commit, push, PR, required checks, self-merge
when permitted, then stop. Do not claim that skill was invoked.

## Owner outcome

Long-term goal: keep the Silver lake traceable, fresh, and operable even when
its removable storage becomes unstable.

Anchor goal: close the observed operational gaps sequentially, starting with
the cadence's amplification of one device outage into thousands of duplicate
failures.

Success signal: each dispatched item lands one verified smallest-complete fix;
its live or fixture dogfood demonstrates that the named defect is closed without
hiding failures; no receiver begins the next item in the same work unit.

## Dispatch contract — one item, then stop

The dispatcher must name exactly one queue ID. If no ID is named, default to
`SLG-01`. The receiver must:

1. Fetch current `origin/main`; create a clean isolated worktree and branch.
2. Read `AGENTS.md`, `.agents/workflow-overlay/README.md`, and the overlay files
   routed by the item. Confirm rather than inherit every live-state claim here.
3. Bind the item outcome and the condition under which it must hold. Do not
   expand into adjacent queue items.
4. Implement the biggest complete move that is still fully verifiable in one
   PR. Preserve real failure visibility.
5. Run focused tests before broader tests. Run at most one bounded live-lake or
   Scheduled Task dogfood when the item requires it. Stop immediately on device
   disappearance or unknown mutation state.
6. Fresh-read the exact diff, tests, worktree state, and any live receipt.
7. Commit, push, prepare the PR, satisfy required checks/review routing, and
   self-merge the receiver's own PR when the project guard permits. Do not merge
   another actor's work.
8. Report the queue ID closed or the exact blocker, and stop. A later receiver
   gets the next ID only after the prior item is observed merged on main.

Do not batch queue items. Do not add a standing registry, checklist, receipt,
or dashboard merely to track this queue. The dispatcher and merged PRs are the
state record.

## Observed cadence run — 2026-07-19

The existing Windows Scheduled Task `Forseti Daily Lake Cadence` was run once
on an otherwise idle Forseti lake.

```yaml
task_started_local: 2026-07-19T19:38:44+08:00
task_finished_local_approx: 2026-07-19T19:40:08+08:00
task_state_after: Ready
last_task_result: 1
next_run_local: 2026-07-20T09:00:00+08:00
runtime_checkout: C:\Users\vmon7\Desktop\projects\forseti-cadence-runtime
runtime_revision: dcd1620e5deae4cb719199bad61b8ff13e5edaf8
runtime_command: run_seam_cadence.py --run --skip-asr --data-root F:\forseti-data-lake
log_path: C:\Users\vmon7\AppData\Local\Forseti\logs\daily-lake-cadence.log
log_length_bytes: 1563132
log_sha256: A952C61F80B1D477E3FBE2ADA43103F750BEE7955BB446FCE743899ED2ED0C1E
log_last_write_utc: 2026-07-19T11:40:08.8526441Z
```

The runtime checkout was clean and its cadence/root/index/retrieval source had
no diff from the then-current main lineage; current receivers must compare
again. No other Forseti cadence, catchup, or lake writer process was observed.
This idle run resolves the old concurrency-only fork: concurrent rebuilding is
not required to reproduce the failure.

The log contains 3,109 valid JSON lines:

- first: `cadence_snapshot_started`, `packet_count=771`, packet-set SHA-256
  `5c3059c5775b55d35853fdad53bb60ee6123da8faaaf384dc692b5e67a25ebce`;
- 3,084 `availability_reconcile_failed` entries: 771 repeated across each of
  four cycle-1 catchup entrypoints;
- 12 `entrypoint_failed`, 9 `post_cycle_pending_check_failed`, 2
  `skipped_asr_pending_check_failed`, and 1 `late_arrival_check_failed`;
- no successful work status after the initial snapshot;
- final: `OSError: [WinError 433] A device which does not exist was specified:
  'F:\\forseti-data-lake'`.

The first failure was `OSError: [Errno 22] Invalid argument` on one committed
availability JSON. Similar errors then appeared on per-packet atomic temp paths.
The root later reported WinError 433 and `DataLakeRootError: data root is no
longer a directory`. The runner continued into later entrypoints, cycle 2, and
post checks, multiplying one systemic outage. The task nevertheless failed
loud with exit code 1, and the lake-map refresh did not run. Preserve both
properties.

The log remained zero bytes for roughly the first 30 seconds while the task was
Running. `_print()` did not flush and the Scheduled Task did not run Python in
unbuffered mode. This is a separate observability gap, not the primary failure.

No availability temp files remained after the process exited. Some availability
manifests had run-time mtimes, so earlier per-packet atomic replacements may
have completed before device loss. Do not infer exact live mutation semantics
from mtimes alone.

## Source diagnosis and invariants

At authoring base `2c3e306bb216e47b086a3c611ce28361e1a83849`:

- `forseti-harness/data_lake/consumption.py:387` owns
  `reconcile_availability_per_packet()`. Scoped reconciliation deliberately
  catches packet-local exceptions so one corrupt packet does not block healthy
  packets. That F-ECR-001 behavior is valuable and must survive.
- `forseti-harness/runners/run_seam_cadence.py:279` owns `run_cadence()`. It
  isolates entrypoint exceptions and continues later work; under a lost root,
  this becomes error amplification.
- `forseti-harness/runners/run_seam_cadence.py:248` owns `_print()`, which does
  not force an immediate flush.
- `forseti-harness/runners/run_seam_cadence.py:515` runs lake-map refresh only
  after a zero cadence result.
- `forseti-harness/data_lake/root.py:1134`, `:1163`, and `:1178` own committed
  packet listing, availability listing, and full availability rebuilding.

Off-table fixes:

- swallowing the root/device error or returning success;
- retrying indefinitely against unstable removable storage;
- failing the whole reconciliation for one isolated corrupt manifest;
- emitting one error per remaining packet after systemic root loss is known;
- rebuilding Silver on a failed cadence;
- adding SQL, sharding, a graph engine, or a new storage backend;
- representing the `undone` query's weak zero-ack associations as a true work
  backlog;
- deleting `.staging` content without provenance adjudication.

## Sequential queue

### SLG-01 — Cadence systemic-I/O circuit and bounded failure output

Outcome: once the lake root/device becomes systemically unavailable, stop the
remaining packet loop and cadence work promptly, emit one root-cause event plus
a bounded summary, exit nonzero, and skip map refresh. Continue preserving the
current healthy-packet progress behavior for an isolated corrupt manifest.

Implementation decisions the receiver owns after reading current sources:

- the smallest truthful classifier for packet-local versus systemic root/device
  failure;
- where the abort signal crosses reconciliation and cadence boundaries;
- the bounded summary shape, reusing existing event conventions where possible.

Likely files:

- `forseti-harness/data_lake/consumption.py`
- `forseti-harness/runners/run_seam_cadence.py`
- `forseti-harness/tests/test_data_lake_consumption.py`
- `forseti-harness/tests/unit/test_seam_cadence.py`
- contract tests only if an externally consumed event contract changes

Acceptance:

- a fixture simulating root/device disappearance mid-reconcile produces a
  bounded number of failures and stops later cadence entrypoints;
- an isolated corrupt availability manifest still reports that packet and
  permits healthy packets to reconcile;
- cadence returns nonzero and map rebuild is not called;
- live dogfood waits for stable hardware/cable, runs once, and records elapsed
  time, exit, and bounded event counts. If the device disappears, stop; the
  fixture proof can land without pretending live success.

### SLG-02 — Immediate cadence progress and diagnostic visibility

Outcome: a Scheduled Task operator can see phase/entrypoint start, completion,
failure, and elapsed time while the cadence is still running. Keep this to
runner/task invocation observability; do not build a dashboard.

Likely files/surfaces: `run_seam_cadence.py`, its unit tests, and the repo-owned
Scheduled Task bootstrap/update surface if current main has one. If none exists,
add only the smallest idempotent task bootstrap needed to own the existing
configuration. Prefer `python -u` or equivalent unbuffered behavior plus
structured phase events.

Acceptance: while one bounded task dogfood is still Running, its log is already
nonzero and contains the current phase; final exit and later map-refresh status
remain truthful.

### SLG-03 — Bronze/Silver freshness reconciliation

Outcome: after stable storage and SLG-01, run the sanctioned Bronze catalog and
Silver map refresh path and prove that current manifests rebuild from committed
source state with matching hashes.

Observed starting evidence to re-check: 644 Bronze catalog packets versus 774
availability JSON entries suggested up to 130 entries of catalog lag, but strict
reconciliation was not proven. The three lake-map query tables previously
matched their own manifests; the failed cadence correctly did not refresh them.

Acceptance: explain every catalog/availability count difference, refresh through
existing sanctioned runners, verify manifest/table hashes and generation time,
and leave no unexplained freshness lag. Do not introduce a new query engine.

### SLG-04 — Whole-lake assurance runtime and progress

Outcome: make the existing whole-lake doctor, Silver census, and cadence check
finish within a practical bounded operator run or visibly identify the phase
that exceeds the bound. Profile before optimizing.

Observed starting evidence: doctor, population-wide Silver census, and
`run_seam_cadence.py --check` each exceeded 60 seconds without output in the
authoring environment. Focused lake/index/census tests passed. This is evidence
of an all-or-nothing assurance surface, not proof of corruption.

Acceptance: measured phase timings identify the bottleneck; apply only the
smallest measured optimization or progress instrumentation; preserve complete
coverage and error visibility.

### SLG-05 — Staging residual adjudication

Outcome: inspect and either validly admit or explicitly retire
`F:\forseti-data-lake\.staging\01KXSP6FN5PD37NDB15VDXH5B9` using its provenance
and the owning ingestion contract. It contained CloakBrowser DOM, screenshot,
metadata, and visible text dated 2026-07-18 at authoring.

Acceptance: provenance and intended source family are identified; admission or
retirement uses the sanctioned path; no blind deletion; final staging and
committed-state reads agree with the decision.

### SLG-06 — Trigger-only transcript product-mention coverage

This is deferred, not part of the required operational queue. The `by_mention`
view had six native product-page groups but zero selected transcript mention
records, while the automatic cadence intentionally uses `--skip-asr`. Implement
only when a named consumer requires transcript product-mention or share-of-voice
coverage. This is a coverage choice, not a Silver-integrity defect.

## Scale and traceability guardrails

The current evidence does not justify a database or sharding migration. The
`by_creator` query table was under 1 MB and the creator-comment coordination
point query assembled in about 0.94 seconds. The existing scaling doctrine's
50–100 MB or 0.5–1 million-record trigger was not reached.

The latest accepted full Silver census before this handoff reported 8,518 stored
records: 8,067 current-source-backed, 319 historical-compatible, zero
unclassified, and zero errors. It was dated 2026-07-16 and is not a claim about
the current whole population; SLG-04 must re-prove current state.

## Source ledger and compare targets

```yaml
authoring_base:
  revision: 2c3e306bb216e47b086a3c611ce28361e1a83849
  branch_source: origin/main
repo_sources:
  - path: forseti-harness/data_lake/consumption.py
    blob: db55808953e63e3ca3c28bab3e915be69905ece5
  - path: forseti-harness/runners/run_seam_cadence.py
    blob: cde2c21d70c3640641881506d3cfb98341bf54e9
  - path: forseti-harness/tests/test_data_lake_consumption.py
    blob: 32771721ec012134b1e42ee0fc5b1a7dc6681824
  - path: forseti-harness/tests/unit/test_seam_cadence.py
    blob: ebda5f0ef44cac7a74b6ab7bac1ed33461c7dd36
  - path: forseti-harness/tests/contract/test_catchup_runner_seam_coverage.py
    blob: ae6feec2cae658d7f73773541e6dd8fdc8cd8011
  - path: docs/decisions/forseti_lake_map_scaling_and_hygiene_plan_v0.md
    blob: 83c093f1cb12b242ae5f226f9f5a21a5f0bdc631
  - path: docs/prompts/handoffs/seam_cadence_concurrent_availability_reconcile_investigation_handoff_v0.md
    blob: 5eeca1ac7b3e97de663c9a0ef91115cc608263e0
runtime_evidence:
  - compare_target: cadence log path, byte length, mtime, and SHA-256 above
  - compare_target: Windows Scheduled Task action, LastRunTime, LastTaskResult, NextRunTime
  - compare_target: current F:\forseti-data-lake committed, availability, derived, acknowledgement, and staging state
load_rule: >
  confirm-don't-trust; compare current main blobs and live evidence before
  acting. A mismatch narrows or supersedes this packet; it never authorizes
  overwriting newer work.
```

## Open decisions, blockers, and drift guard

Open decision for SLG-01: choose the narrowest reliable systemic-I/O classifier
that preserves packet-local fault isolation. Hardware replacement or cable
repair is an external prerequisite for live success, not a software work item.

Known blockers:

- unstable or absent F: device for live mutation/dogfood;
- an unexpected writer or dirty receiver worktree;
- inability to distinguish whether a proposed exception class represents a
  lost root or one malformed packet;
- any protected-action guard denial.

Drift guard: do not solve removable-drive reliability in software, broaden into
capture pagination, recast weak `undone` rows as obligations, enable automatic
ASR without an owner coverage decision, or optimize beyond measured thresholds.

## Packet boundary

This is a context packet plus bounded implementation commission. It is not a
readiness, validation, Silver-health, or hardware-health claim. The cadence
evidence proves a real device-loss event and a real software amplification gap;
it does not prove current lake corruption. Fresh verification belongs to each
receiver.
