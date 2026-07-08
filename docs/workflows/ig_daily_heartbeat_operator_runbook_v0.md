# IG Daily Heartbeat Operator Runbook v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Operator command shape for supervised IG daily heartbeat run-control sessions.
use_when:
  - Preparing a supervised IG daily heartbeat session from Creator Registry and an active-monitoring sidecar.
  - Building a disabled Windows Task Scheduler entry by hand without registering it from Codex.
  - Checking the run-control data layout before a live IG heartbeat run.
authority_boundary: retrieval_only
open_next:
  - forseti-harness/runners/run_source_capture_ig_daily_heartbeat_operator.py
  - forseti-harness/runners/run_source_capture_ig_daily_heartbeat_control.py
  - forseti-harness/runners/run_source_capture_ig_daily_heartbeat.py
```

This runbook is an operator aid only. It is not live IG authorization, account-safety proof, Windows Scheduled Task registration, egress routing, Silver/Gold monitoring, or creator-intelligence output.

## Current Attachment

Use the operator wrapper, not a new scraper:

```powershell
python forseti-harness\runners\run_source_capture_ig_daily_heartbeat_operator.py run-session `
  --registry-index "<path-to-creator-registry-index.json>" `
  --monitoring-sidecar "<path-to-ig-daily-monitoring-sidecar.json>" `
  --run-control-root "<path-to-run-control-root>" `
  --plan-date "<YYYY-MM-DD>" `
  --bucket 1 `
  --lane-id lane_1 `
  --lane-count 2 `
  --output-root "<path-to-local-packet-output-root>"
```

What that does, in order:

1. Creates `daily_plan.json` if the date has no plan yet.
2. Runs exactly one planned bucket/lane through the existing heartbeat runner.
3. Refreshes `daily_summary.json` after the session.

If the plan already exists, it is reused. The wrapper does not overwrite the plan or erase `attempts.jsonl`.

## Runtime Layout

All run-control records stay under the run-control root:

```text
run_control/ig_daily_heartbeat/<YYYY-MM-DD>/
  daily_plan.json
  attempts.jsonl
  session_<bucket>_roster.json
  heartbeat_receipts_session_<bucket>.jsonl
  session_<bucket>_summary.json
  daily_summary.json
```

Packet output is separate. Use `--output-root` for local packet bundles. Use `--data-root` only when the owner has explicitly authorized lake writes for that run.

## Windows Task Scheduler Template

Do not register this from Codex. If the owner later wants a Windows task, create it manually with these fields and leave it disabled until the first supervised dry run is accepted.

```text
Program/script:
powershell.exe

Start in:
<repo-or-worktree-root>

Add arguments:
-NoProfile -ExecutionPolicy Bypass -Command "$PlanDate=(Get-Date -Format 'yyyy-MM-dd'); python 'forseti-harness\runners\run_source_capture_ig_daily_heartbeat_operator.py' run-session --registry-index '<registry>' --monitoring-sidecar '<sidecar>' --run-control-root '<run-control-root>' --plan-date $PlanDate --bucket <1-4> --lane-id lane_1 --lane-count 2 --output-root '<packet-output-root>'"
```

Create one task/action per bucket window, or run the same action manually with a different `--bucket`. Do not use per-request egress rotation here; egress/lane binding is a separate lane.

## Failure Handling

- A missing plan is created by default. Add `--no-plan-if-missing` when a session must fail unless planning already happened.
- A terminal attempt in `attempts.jsonl` prevents an accidental duplicate session for that creator unless `--retry-status` is explicitly supplied.
- Access gaps, failures, and successes come from heartbeat receipts. Missing metrics or missing receipts are not converted to zero or success.
- CAPTCHA, login, challenge, and access blocks remain owner-attention events. This wrapper does not solve or route around them.

## Non-Claims

- Not a scheduled task registration.
- Not a live-run receipt.
- Not a 2.5k/day throughput proof.
- Not an account-safety claim.
- Not Silver, Gold, EMA, breakout tagging, deep capture selection, or Creator Registry mutation.
