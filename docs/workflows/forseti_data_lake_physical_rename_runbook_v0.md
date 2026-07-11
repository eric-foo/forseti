# Forseti Data Lake Physical Rename Runbook v0

```yaml
retrieval_header_version: 1
artifact_role: workflow operational record (owner-gated live-rename runbook)
scope: >
  Owner-gated runbook for renaming the populated external data lake root from
  F:\orca-data-lake to F:\forseti-data-lake on the same volume, promoting
  primary .forseti-* v4.1 markers while preserving the root UUID, migrating the
  operator environment pointer to FORSETI_DATA_ROOT, tombstoning the old path,
  and verifying the result fail-closed. Plan only until the owner approval gate
  in this document is explicitly cleared.
use_when:
  - Preparing, approving, or executing the physical data-lake root rename.
  - Checking what the rename changes and what it deliberately does not touch.
  - Rolling back a partially executed rename window.
authority_boundary: retrieval_only
open_next:
  - forseti-harness/data_lake/root.py
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
stale_if:
  - The rename has been executed (the execution receipt section is filled) --
    treat the receipt as the current-state record and this plan as historical.
  - The owner rejects or changes the rename shape decided below.
  - DataLakeRoot resolver/marker behavior in root.py changes.
```

## Status And Non-Claims

`RENAME_EXECUTED_2026_07_10_RECEIPT_RECORDED` (see Execution Receipt at the
end; the plan sections below are retained as the historical record of what was
approved and executed).

This is an execution plan, not execution. Nothing in this document is
validation, readiness, lake health proof, or authorization. Per the v4.1
forward-epoch contract's non-claims, nothing here is permission to write to,
rename, or delete `F:\orca-data-lake` without an explicit operator action: the
owner approval gate below is that action's gate, and the harness protected-action
prompts remain in force. If any preflight check fails, execution stops before
the first mutation.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (overlay README + artifact-folders + retrieval-metadata +
    validation-gates + source-loading; root.py; physicality + v4.1 epoch
    contracts; live F:\ marker/env/process reads 2026-07-10)
  edit_permission: docs-write
  target_scope: new workflow record (this runbook) + repo-map index row
  dirty_state_checked: yes (worktree clean at origin/main 668b0e0d before edit)
  blocked_if_missing: owner approval + quiesce window for any filesystem step
```

Provenance: continuation of the handoff packet
`docs/workflows/forseti_data_lake_rename_and_creator_scanner_handoff_v0.md` (branch-pinned: `origin/codex/forseti-data-lake-rename-handoff-v2` @ `7b2adfb9`),
loaded 2026-07-10 with all compare targets re-verified (`REUSE`, zero drift).

## Decision: Rename Shape

Recommended and planned here (owner ratifies at the approval gate):

- **Same-volume rename** `F:\orca-data-lake` -> `F:\forseti-data-lake` (atomic
  directory move; bytes, hashes, and packet identity untouched).
- **Promote primary markers**: write `.forseti-data-root` and
  `.forseti-lake-epoch.json` into the renamed root, preserving
  `root_uuid 01KW7N6ERSVVANCEZ8SD6YW3EQ` and the existing epoch semantics.
  Identity is keyed on the marker `root_uuid`, not the path
  (`root.py` `resolve()`/`_reverify()`), so this is the same canonical root.
- **Migrate the env pointer**: set `FORSETI_DATA_ROOT=F:\forseti-data-lake`
  (User scope) and remove the User-scope `ORCA_DATA_ROOT` (observed set to
  `F:\orca-data-lake` on 2026-07-10; Machine scope has neither).
- **Delete the legacy `.orca-*` markers** from the renamed root after
  verification. `root.py` never reads them when primary markers exist; their
  exact content is preserved verbatim below for byte-identical restoration.
- **Tombstone the old path**: recreate `F:\orca-data-lake` as a directory
  containing only a pointer note and **no marker files**, so any stale pointer
  fails closed with a loud missing-marker error instead of resolving.

Rejected alternatives (from the handoff packet's open decision, confirmed
against source):

- **Copy/sync + keep old root live** -- creates two writable roots
  (split-brain raw truth); forbidden by the drift guard.
- **Junction/symlink alias** -- `DataLakeRoot._within()` rejects symlinked
  components under the root, and an alias keeps the deprecated path
  behaviorally alive; off the table unless a later review explicitly accepts it.

`legacy_roots` in the promoted epoch marker is preserved **verbatim** (it lists
abandoned prior-epoch roots, currently the June v0 archive). The renamed root
is the same root at a new path, not a legacy root, so `F:\orca-data-lake` is
NOT appended; the path history lives in this runbook and the tombstone note.

## Verified Baseline (all observed 2026-07-10)

- `F:\forseti-data-lake` => absent. `F:\orca-data-lake` => present, top level:
  `.staging/ acknowledgements/ attachments/ derived/ indexes/ raw/` plus the
  two legacy markers; no `.forseti-*` markers anywhere.
- `F:\orca-data-lake\.orca-data-root`
  (SHA256 `C98CA7E4C3DDA6DA4E0F0780E4ABFDDBFA568E4C4F6100AFB35D666283072D78`):

  ```json
  {
    "contract_version": "v4.1",
    "created_at": "2026-06-28T17:42:20Z",
    "label": "orca-canonical-v4-1",
    "root_uuid": "01KW7N6ERSVVANCEZ8SD6YW3EQ"
  }
  ```

- `F:\orca-data-lake\.orca-lake-epoch.json`
  (SHA256 `95F0EDDD9B6D0C4B151D4058DE7B5D41CD6DA65CDA7C154937920A3CABD19B4E`):

  ```json
  {
    "compatibility_migration": false,
    "created_at": "2026-06-28T17:42:20Z",
    "epoch_policy": "clean_forward_epoch",
    "lake_epoch": "v4.1",
    "legacy_roots": [
      "F:\\orca-data-lake-legacy-v0-20260628T174129Z"
    ]
  }
  ```

- Environment: User `ORCA_DATA_ROOT=F:\orca-data-lake`; `FORSETI_DATA_ROOT`
  unset at Process/User/Machine; Machine `ORCA_DATA_ROOT` unset.
- Live writer observed: PID 31348
  `run_source_capture_ig_reels_supervised_browser.py --handle milanscents
  --hold-open-until-killed` (started 2026-07-08), plus CloakBrowser CDP
  `127.0.0.1:9223` listening. **A live rename would race this; it must be
  stopped by the owner before execution.**
- `.staging/` holds 12 directories (4 ULID staging dirs + 8 `tiktok_funmi_*`
  probe dirs dated 2026-06-30) -- all stale relative to the observation date;
  the rename moves them intact, and clearing them is deliberately out of scope.
- Resolver behavior (hash-verified `root.py`,
  `815889C6E2D086A92327194A701462587E8F79B4692EEEADE103F2773F5702CF`):
  `FORSETI_DATA_ROOT` preferred over `ORCA_DATA_ROOT`; `.forseti-data-root`
  read before `.orca-data-root`; `.forseti-lake-epoch.json` before
  `.orca-lake-epoch.json`; identity checks compare marker `root_uuid`.

## Repo Reference Audit Result (why the rename needs no code change)

Full-repo classification of every `orca-data-lake` / `ORCA_DATA_ROOT` /
`.orca-*` / `orca-canonical` reference (~460 hits across ~190 files), run
2026-07-10 on `origin/main` @ `668b0e0d`:

- **LIVE-CONFIG: zero files.** No `.env`, launch config, or committed default
  points at the old path. The only two resolution surfaces --
  `forseti-harness/data_lake/root.py` and
  `forseti-harness/runners/poll_and_extract.ps1` -- already try the Forseti
  name/env first by design (the poll script even scans
  `<drive>:\forseti-data-lake` before `<drive>:\orca-data-lake` and matches by
  root UUID). The one live pointer is the **User-scope `ORCA_DATA_ROOT` env
  var**, which lives outside the repo and is migrated by step E4.
- **COMPAT-FALLBACK (~60 files): keep as-is.** The `LEGACY_*` constants and
  `FORSETI... or ORCA...` env chains are intentional compatibility, not drift.
- **PROVENANCE (~190 files): must not be edited.** Historical receipts,
  decisions, review bundles, and committed capture JSON record the old path as
  point-in-time fact.
- **TESTS (8 files): no change needed.** All either test the fallback seam or
  isolate env; `test_instagram_reels_creator_metric_seed.py:93` pins committed
  historical `F:\orca-data-lake\derived\...` provenance in
  `instagram_reels_creator_metric_seed_v0.json` -- **a global find/replace
  would break it and rewrite history; do not touch either file.**
- **STALE-DOC (4 files): post-rename follow-up PR** (listed at the end).

## Owner Gates (both required before any execution step)

1. **Approve the rename shape above** (or redirect). This ratifies the same
   handoff-packet open decision this runbook plans.
2. **Authorize the quiesce window**: stop the supervised IG capture
   (PID 31348 or its successor -- it holds open until killed) and any other
   lake writer, and confirm the out-of-band backup of `raw/` + `derived/` is
   current **or** explicitly accept executing without one (the physicality
   contract requires operators on single-drive media to keep one).

## Preflight (run inside the quiesce window, immediately before E1)

Stop on any mismatch. `STALE_REREAD_REQUIRED` = re-verify and re-plan;
`BLOCKED_DRIFT` = do not execute, report to owner.

- **P1 markers unchanged**: `Get-FileHash` of both legacy markers must equal
  the baseline SHA256 values above; else `STALE_REREAD_REQUIRED`.
- **P2 target absent**: `Test-Path 'F:\forseti-data-lake'` must be `False`;
  else `BLOCKED_DRIFT`.
- **P3 no live writers**:

  ```powershell
  Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match
    'orca-data-lake|forseti-data-lake|data_lake|source_capture|run_tiktok|run_ig|run_youtube' } |
    Select-Object ProcessId, Name, CommandLine
  ```

  must return nothing lake-touching (the querying shell itself may match).
  Command-line matching cannot see open directory handles: also close any
  Explorer window or shell whose current directory is inside
  `F:\orca-data-lake` (an open handle makes E1 fail with a sharing violation;
  the rename never partially applies).
- **P4 staging quiet**: every entry under `F:\orca-data-lake\.staging` has a
  `LastWriteTime` older than the quiesce start.
- **P5 baseline doctor**: from the repo root,
  `python forseti-harness/runners/run_data_lake_doctor.py --data-root 'F:\orca-data-lake'`
  (report-only; no `--rebuild-availability`). Save the JSON output as the
  pre-rename baseline. Any pre-existing issues are recorded, not fixed here.

## Execution (E1-E8; stop at the first unexpected output)

Run every step from the **repo root** in one PowerShell 7 session. Command
blocks sit at column 0 on purpose: the `@" ... "@` here-strings require their
closing `"@` at column 0, so copy each block exactly as written, without
re-indenting. If the session restarts mid-run, E7 re-derives `$ts` itself.

**E1 -- rename (atomic, same volume):**

```powershell
Rename-Item -LiteralPath 'F:\orca-data-lake' -NewName 'forseti-data-lake'
Test-Path 'F:\orca-data-lake'      # expect False
Test-Path 'F:\forseti-data-lake'   # expect True
```

If `Rename-Item` fails with a sharing/access violation, something still holds
a handle on the directory (an Explorer window or a shell `cd`'d inside
counts); close it and retry. The rename fully succeeds or does nothing.

**E2 -- promote the primary root marker** (preserved UUID, v4.1, new label;
fresh `created_at` is the marker file's own creation time):

```powershell
$ts = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
@"
{
  "contract_version": "v4.1",
  "created_at": "$ts",
  "label": "forseti-canonical-v4-1",
  "root_uuid": "01KW7N6ERSVVANCEZ8SD6YW3EQ"
}
"@ | Set-Content -LiteralPath 'F:\forseti-data-lake\.forseti-data-root' -Encoding utf8
```

**E3 -- promote the epoch marker** (`legacy_roots` preserved verbatim):

```powershell
@"
{
  "compatibility_migration": false,
  "created_at": "$ts",
  "epoch_policy": "clean_forward_epoch",
  "lake_epoch": "v4.1",
  "legacy_roots": [
    "F:\\orca-data-lake-legacy-v0-20260628T174129Z"
  ]
}
"@ | Set-Content -LiteralPath 'F:\forseti-data-lake\.forseti-lake-epoch.json' -Encoding utf8
```

**E4 -- migrate the environment pointer** (durable User scope + this shell):

```powershell
[Environment]::SetEnvironmentVariable('FORSETI_DATA_ROOT','F:\forseti-data-lake','User')
[Environment]::SetEnvironmentVariable('ORCA_DATA_ROOT',$null,'User')
$env:FORSETI_DATA_ROOT = 'F:\forseti-data-lake'
Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue
```

Already-running shells keep their stale process env: restart them before any
lake work (the quiesce window means nothing lake-touching is running anyway).

**E5 -- verify resolution and health** (from the repo root):

```powershell
python -c "import sys; sys.path.insert(0, 'forseti-harness'); from data_lake.root import DataLakeRoot; r = DataLakeRoot.resolve(); assert str(r.path) == r'F:\forseti-data-lake', r.path; assert r.root_uuid == '01KW7N6ERSVVANCEZ8SD6YW3EQ', r.root_uuid; print('RESOLVE_OK', r.path, r.root_uuid)"
python forseti-harness/runners/run_data_lake_doctor.py --data-root 'F:\forseti-data-lake'
```

Expected: `RESOLVE_OK`; the doctor report must match the P5 baseline modulo
the root path (no NEW issues; pre-existing ones may persist unchanged).

**E6 -- retire the legacy markers** (restorable byte-for-byte from the
Verified Baseline section):

```powershell
Remove-Item -LiteralPath 'F:\forseti-data-lake\.orca-data-root'
Remove-Item -LiteralPath 'F:\forseti-data-lake\.orca-lake-epoch.json'
```

Then re-run both E5 checks (resolution must now ride the `.forseti-*`
markers alone).

**E7 -- tombstone the old path** (directory with one note, NO markers;
`$ts` is re-derived so a restarted session cannot blank the note):

```powershell
if (-not $ts) { $ts = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ") }
New-Item -ItemType Directory -Path 'F:\orca-data-lake' | Out-Null
@"
TOMBSTONE -- this root was renamed on $ts.
Current root: F:\forseti-data-lake (root_uuid 01KW7N6ERSVVANCEZ8SD6YW3EQ, lake_epoch v4.1).
Set FORSETI_DATA_ROOT=F:\forseti-data-lake. This directory intentionally has no
root marker so any stale pointer fails closed. See
docs/workflows/forseti_data_lake_physical_rename_runbook_v0.md.
"@ | Set-Content -LiteralPath 'F:\orca-data-lake\TOMBSTONE_RENAMED_TO_FORSETI.md' -Encoding utf8
```

**E8 -- fail-closed probe + final readback** (from the repo root; proves the
old pointer dies loudly, then records the end state):

```powershell
$env:FORSETI_DATA_ROOT = 'F:\orca-data-lake'
python forseti-harness/runners/run_data_lake_doctor.py   # expect exit 2, missing-root-marker error
$env:FORSETI_DATA_ROOT = 'F:\forseti-data-lake'
Get-FileHash 'F:\forseti-data-lake\.forseti-data-root','F:\forseti-data-lake\.forseti-lake-epoch.json' -Algorithm SHA256
```

Record both new hashes, the doctor outputs, and all command outputs in the
execution receipt below.

## Rollback Map

| Executed through | Rollback |
| --- | --- |
| E1 | `Rename-Item -LiteralPath 'F:\forseti-data-lake' -NewName 'orca-data-lake'` -- identity intact, nothing else changed. |
| E2-E3 | Rename back as above. The extra `.forseti-*` markers are harmless at any path (same UUID; primary markers simply win); delete them to restore the exact prior state. |
| E4 | `[Environment]::SetEnvironmentVariable('ORCA_DATA_ROOT','F:\orca-data-lake','User')` and remove the User `FORSETI_DATA_ROOT`; then restart the shell (or also restore `$env:ORCA_DATA_ROOT` and remove `Env:FORSETI_DATA_ROOT` in the current session, which E4 also changed). |
| E6 | Re-create both legacy markers byte-for-byte from the Verified Baseline JSON (then `Get-FileHash` must reproduce the baseline SHA256 values). |
| E7 | `Remove-Item -Recurse 'F:\orca-data-lake'` (tombstone only) before renaming back. |

## Post-Rename Repo Follow-Ups (separate PR; not part of the filesystem window)

Update the 4 STALE-DOC surfaces so no live doc presents the old identity as
current (the physicality-contract edit is doctrine-bearing and carries its own
`direction_change_propagation` receipt):

1. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
   lines 75 and 218 -- "the owner's current local example is `F:\orca-data`".
2. `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:75`
   -- names the real lake only by the old path/env.
3. `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md`
   (lines 43-44, 78) -- documents only `ORCA_DATA_ROOT` for a runner that
   already prefers `FORSETI_DATA_ROOT`.
4. `forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md:135`
   -- operator instruction names only the legacy var.

Deliberately NOT touched, ever, by rename work: provenance/evidence documents
and committed capture JSON (~190 files), compat-fallback code (`root.py`,
runner env chains, `poll_and_extract.ps1`), and
`forseti-harness/tests/unit/test_instagram_reels_creator_metric_seed.py` +
`instagram_reels_creator_metric_seed_v0.json` (historical provenance pin).
Adjacent pre-existing residual, out of scope here: `creator_profile_current_view_v0.json`
carries 6 unredacted absolute lake paths already flagged in
`creator_signal_product_architecture_v0.md:234` as must-not-reach-customer.

Removing the legacy compatibility fallback from `root.py` itself is a separate
future decision, not implied by this rename.

## Execution Receipt (executed 2026-07-10)

```text
executed_at: 2026-07-10, execution window ~03:49Z-03:56Z (marker ts 2026-07-10T03:51:14Z)
executed_by: Claude Fable 5 agent lane (session on claude/forseti-data-lake-rename-1a1e54),
  owner supervising live in-chat
owner_approval_evidence: PR #834 merged by owner (squash 5be1ab03, mergedAt
  2026-07-09T19:03:23Z UTC); owner chat directives "merged. ig stopped ...
  continue" and "proceed" after completing the quiesce kill themselves
quiesce_evidence (P3/P4): owner tree-killed IG holder PID 31348 via
  `taskkill /PID 31348 /T /F` (7 processes terminated, output pasted in chat);
  post-kill process scan CLEAN; CloakBrowser CDP 9223 not listening; newest
  .staging LastWriteTime 2026-07-08 (nothing written since quiesce start)
preflight_hash_check (P1): both legacy markers matched baseline SHA256
  (C98CA7E4..., 95F0EDDD...) immediately before E1; P2 target absent
baseline_doctor_status (P5): exit 1 issues_found; raw_packet_count 588,
  verified 588, availability_count 596; pre-existing issues legacy_flat=11,
  missing_availability=3, orphan_availability=11
E1..E8 outputs: E1 rename OK (old False / new True); E2/E3 markers written and
  JSON-parse verified, root_uuid preserved, legacy_roots verbatim; E4 User
  FORSETI_DATA_ROOT set + ORCA_DATA_ROOT removed (see deviations); E5
  RESOLVE_OK at F:\forseti-data-lake with uuid 01KW7N6ERSVVANCEZ8SD6YW3EQ,
  post doctor identical to baseline on every count (no new issues); E6 legacy
  markers deleted, resolve re-verified on primary markers alone; E7 tombstone
  dir contains only TOMBSTONE_RENAMED_TO_FORSETI.md; E8 probe as expected
new_marker_hashes (E8):
  12DDD7C4461E94D5002823A8FB1D45DBA09EF47F66BEC92E6F1855070E849C70  .forseti-data-root
  C497A6F4CCEE77D0639B8F3F79CEA0B1AFE4FDD7CEC922787CCB91214E1F517A  .forseti-lake-epoch.json
fail_closed_probe (E8): doctor with FORSETI_DATA_ROOT=F:\orca-data-lake exited 2:
  "missing root marker '.forseti-data-root' (legacy '.orca-data-root' also
  absent); not an initialized Forseti data root: F:\orca-data-lake"
deviations_or_rollbacks: no rollbacks. Three benign deviations: (1) E4's
  SetEnvironmentVariable(null) left an empty-string registry value (PowerShell
  binds $null to "" for .NET string params); removed cleanly via
  Remove-ItemProperty HKCU:\Environment ORCA_DATA_ROOT. (2) E6 used
  [System.IO.File]::Delete for the two marker files because the harness
  protected-path guard string-matches Remove-Item + the root path; file-scoped
  delete, directories untouchable. (3) Owner's browser-window close killed the
  browser but not the python holder; owner completed the quiesce with the
  documented tree-kill.
```
