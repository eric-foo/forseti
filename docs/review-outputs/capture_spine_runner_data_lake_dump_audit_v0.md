# Capture Spine Runner Data Lake Dump Audit v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Read-only audit of Capture Spine runner compliance with Orca data-lake raw
  packet commit behavior, including runner matrix, live-root comparison, test
  coverage gaps, and bounded patch recommendation.
use_when:
  - Checking which Source Capture runners can commit packets through --data-root or ORCA_DATA_ROOT.
  - Planning the smallest complete patch to wire missing packet runners into DataLakeRoot.
  - Reconciling current runner/code tests with live data-lake raw path evidence.
open_next:
  - docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
  - forseti-harness/runners/
  - forseti-harness/source_capture/writer.py
  - forseti-harness/source_capture/packet_assembly.py
  - forseti-harness/data_lake/root.py
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
branch_or_commit: codex/ig-reels-capture-spine @ 20e0f42855579ab499c8793e49dfadb61e363eea
stale_if:
  - Any runner in orca-harness/runners/ gains or loses --data-root / ORCA_DATA_ROOT support.
  - DataLakeRoot raw pathing, availability entry shape, or sharding behavior changes.
  - The live data-lake root is migrated, cleaned, rebuilt, or re-sharded.
  - test_capture_runner_lake_seam_coverage.py changes producer detection or known-unsynced entries.
authority_boundary: retrieval_only
```

## Body Opening

Purpose: audits current runner-to-lake behavior for Source Capture packet writers. It is an evidence report and patch recommendation, not an implementation patch.

Do not use for: Silver Vault schema decisions, data-lake physical-path doctrine, live capture authorization, live-root cleanup authorization, or proof that a packet source is valid.

Authority boundary: current user instruction, `AGENTS.md`, and `.agents/workflow-overlay/` win over this report. Code and live-root reads win over the handoff packet when they disagree.

Recheck recipe: rerun branch/head/status; rerun the runner feature scan; reread `root.py`, `writer.py`, `packet_assembly.py`, and `test_capture_runner_lake_seam_coverage.py`; read live root counts and a representative availability entry without writing to `F:\orca-data-lake`.

Non-claims: not validation, not readiness, not implementation authorization, not a Silver Vault finding, not acceptance of sharded or unsharded raw pathing, not authorization to delete the accidental test packet named below.

## Source Loading Receipt

- `AGENTS.md`: read. It requires smallest complete intervention, visible failure reporting, overlay loading, and no implementation/runtime work without explicit bounded authorization.
- `.agents/workflow-overlay/README.md`: read. It binds Orca overlay as project authority.
- `.agents/workflow-overlay/source-loading.md`: read. It requires bounded source loading and the capture-method playbook for capture-spine activity.
- `.agents/workflow-overlay/decision-routing.md`: read. Cynefin route was complicated with one complex live-root/code conflict; allowed next move was read-only source and filesystem probes.
- `.agents/workflow-overlay/artifact-folders.md`: read. `docs/review-outputs/` is an accepted review-output folder.
- `.agents/workflow-overlay/retrieval-metadata.md` and `docs/workflows/artifact_retrievability_guide.md`: read before creating this durable report.
- `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`: read as non-authoritative handoff packet.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`: read for Capture Spine navigation and implementation-reality warning.
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` and `capture_recon_index_v0.md`: read as capture-method context; no live capture was authorized or run.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`: read for the lake responsibility boundary.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`: read for index rebuild and derived/index non-authority.
- `orca-harness/data_lake/root.py`, `orca-harness/source_capture/writer.py`, `orca-harness/source_capture/packet_assembly.py`: read for current implementation.
- `orca-harness/runners/` and `orca-harness/tests/`: scanned and targeted files opened.

## Workspace And Live Root State

- Branch/head observed before audit: `codex/ig-reels-capture-spine`, `20e0f42855579ab499c8793e49dfadb61e363eea`.
- Dirty state observed before report: many unrelated untracked files already existed, including the handoff packet and neighboring Silver Vault draft.
- Live root marker read-only: `F:\orca-data-lake\.orca-data-root` has `root_uuid` `01KW1E6N133JT0XCN2KCN0V5A4`, `contract_version` `v0`, label `orca-canonical`.
- Pre-verification live counts observed: `241` raw manifests, `343` derived files, `241` availability files, `0` derived_retrieval files.
- Representative pre-existing availability entry observed: `F:\orca-data-lake\indexes\availability\01KW4FKEA9ETHA7MRXWVS2MQ6C.json` pointed to `raw/67c/01KW4FKEA9ETHA7MRXWVS2MQ6C`.

## Verification Incident

One test command was run before clearing inherited `ORCA_DATA_ROOT`. That violated the lane's no-live-root-write drift guard and wrote one packet to the live root:

- Packet: `01KW51Q00W7HQ06VM38H814K8Z`
- Raw path: `F:\orca-data-lake\raw\01KW51Q00W7HQ06VM38H814K8Z\manifest.json`
- Availability path: `F:\orca-data-lake\indexes\availability\01KW51Q00W7HQ06VM38H814K8Z.json`
- Availability entry: `raw_path` is `raw/01KW51Q00W7HQ06VM38H814K8Z`, `source_family` is `reddit`, `source_surface` is `local_file_artifact`.
- Post-incident counts observed: `242` raw manifests and `242` availability files.
- No deletion or cleanup was performed, because removing live-root material was not authorized.

This incident is itself an audit finding: the test suite can write to a real operator root when `ORCA_DATA_ROOT` leaks into the test environment.

## Findings

### F1 - High - Live root and current DataLakeRoot disagree on raw path shape

The live root's established entries are sharded, but current code and tests still assert unsharded packet paths.

Evidence:

- Live availability entry before the test incident: `raw_path` was `raw/67c/01KW4FKEA9ETHA7MRXWVS2MQ6C`.
- Live raw manifest exists at `F:\orca-data-lake\raw\67c\01KW4FKEA9ETHA7MRXWVS2MQ6C\manifest.json`.
- `orca-harness/data_lake/root.py:202-203` emits `raw/{packet_id}` and `raw/{packet_id}/manifest.json`.
- `orca-harness/tests/test_data_lake_availability.py:35-46` asserts `root.path / "raw" / pid` and `entry["raw_path"] == f"raw/{pid}"`.
- The accidental test packet was also written unsharded, proving current branch code can add new unsharded material to a mostly sharded live root.

Impact: patching runner support before settling path physicality risks increasing mixed live-root layout. A runner patch can be mechanically correct while still committing into the wrong physical shape for the canonical root.

### F2 - High - Nine direct Source Capture packet runners are local-output only

Current code has twelve direct packet-producing `run_source_capture_*` runners by static producer-token scan. Only three expose the lake seam (`data_root`, `--data-root`, `ORCA_DATA_ROOT`, `DataLakeRoot.resolve`):

- `run_source_capture_packet.py`
- `run_source_capture_http_packet.py`
- `run_source_capture_ig_reels_grid_packet.py`

Nine packet writers are acknowledged as missing the seam in the contract test allowlist:

- `run_source_capture_browser_packet.py`
- `run_source_capture_authenticated_browser_packet.py`
- `run_source_capture_cloakbrowser_packet.py`
- `run_source_capture_antiblock_http_packet.py`
- `run_source_capture_archive_packet.py`
- `run_source_capture_historical_packet.py`
- `run_source_capture_media_packet.py`
- `run_source_capture_price_payload_packet.py`
- `run_source_capture_ig_calls_packet.py`

Evidence:

- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:23-36` lists the known unsynced packet-producing runners.
- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:39-60` detects producers by `write_local_source_capture_packet` or `stage_and_write_packet` and treats absence of `data_root` as missing the seam.
- Representative local-only examples:
  - `run_source_capture_archive_packet.py:56-76` takes `output_directory: Path`, and its CLI has required `--output` at `run_source_capture_archive_packet.py:455`.
  - `run_source_capture_antiblock_http_packet.py:48-58` takes `output_directory: Path`, and its CLI has required `--output` at `run_source_capture_antiblock_http_packet.py:233`.

Impact: the shared writer can commit to the lake, but most packet runners do not let an operator choose that route.

### F3 - Medium - Two packet-producing orchestrators escape the seam contract

Two runners produce Source Capture packet directories indirectly but are not covered by the current producer-token contract:

- `run_source_capture_durability_series.py` invokes child writer mains per slot and always constructs child writer argv with `--output` (`run_source_capture_durability_series.py:15-18`, `run_source_capture_durability_series.py:241-270`). Its passthrough guard says the runner owns `--output` and rejects override-style knobs (`run_source_capture_durability_series.py:336-341`). It can choose `direct_http` or `cloakbrowser`, but its child packets remain local series observations.
- `run_reddit_old_http_batch.py` imports and calls `run_source_capture_http_packet` (`run_reddit_old_http_batch.py:16`, `run_reddit_old_http_batch.py:73-89`) and writes per-slot packet dirs plus local derived dirs. It has required `--output-root` (`run_reddit_old_http_batch.py:278`).

Impact: a static test can pass while packet-producing orchestration paths still never commit raw packets into the lake. These paths need a separate design call because they also own local summaries/series state; only raw packet material clearly belongs in the lake.

### F4 - Medium - Test safety and coverage are too weak for live-root work

Targeted verification only passed after removing inherited `ORCA_DATA_ROOT`:

```powershell
Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q tests/contract/test_capture_runner_lake_seam_coverage.py tests/unit/test_run_source_capture_packet_lake.py tests/unit/test_source_capture_ig_reels_grid_packet.py tests/test_data_lake_availability.py
```

Observed result after clearing env: `................ [100%]` (`16` tests passed).

The failed pre-clear run wrote to live root because `run_source_capture_packet.py:170-179` treats `ORCA_DATA_ROOT` as a valid target when `--output` is absent. That behavior may be intended for production, but tests that expect "no target" must isolate the environment.

Coverage gaps:

- `run_source_capture_packet.py` has an explicit lake test (`tests/unit/test_run_source_capture_packet_lake.py:41-51`).
- `run_source_capture_ig_reels_grid_packet.py` has a direct data-root test and env/output mutual-exclusion test (`tests/unit/test_source_capture_ig_reels_grid_packet.py:192-206`, `291-311`).
- No direct `run_source_capture_http_packet` data-root execution test was found by grep; current assurance is static seam detection plus the shared `stage_and_write_packet`/writer tests.
- The nine unsynced direct writers and two orchestration writers need per-runner tests when patched.

## Runner Matrix

| Runner | Classification | Lake seam | Test posture |
| --- | --- | --- | --- |
| `run_source_capture_packet.py` | direct packet writer | Yes: `--data-root` / `ORCA_DATA_ROOT`, shared writer | Direct lake test exists |
| `run_source_capture_http_packet.py` | direct packet writer | Yes: `--data-root` / `ORCA_DATA_ROOT`, `stage_and_write_packet` | Static seam coverage; no direct data-root execution test found |
| `run_source_capture_ig_reels_grid_packet.py` | direct packet writer | Yes: mutually exclusive `--output` / `--data-root`, env support | Direct lake and env conflict tests exist |
| `run_source_capture_antiblock_http_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_archive_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_authenticated_browser_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_browser_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_cloakbrowser_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_historical_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_media_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_price_payload_packet.py` | direct packet writer | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_ig_calls_packet.py` | direct packet writer, legacy IG fallback | No; required `--output` | Allowlisted unsynced |
| `run_source_capture_durability_series.py` | packet-producing orchestrator | No; child writer argv owns `--output` | Not covered by seam contract |
| `run_reddit_old_http_batch.py` | packet-producing batch orchestrator | No; child direct-HTTP writes local packet dirs under `--output-root` | Not covered by seam contract |
| Bootstrap/config runners | bootstrap/config | Not required unless they start emitting Source Capture Packets | Excluded |
| Projection/read-only/reporting runners | projection/read-only/reporting | Not required | Excluded |
| Candidate-intake/frontier/screening runners | candidate rows/registers/screening, not Source Capture Packets by current code evidence | Not required | Excluded |

## Patch Recommendation

Smallest complete patch should not start by wiring every runner. Do this sequence:

1. Test-safety patch first.
   - Add an autouse test guard or targeted monkeypatching that clears/refuses real `ORCA_DATA_ROOT` for unit/contract tests unless a test explicitly creates a `DataLakeRoot.for_test` root.
   - Add a regression for `test_cli_requires_exactly_one_target` with `ORCA_DATA_ROOT` cleared, and optionally a separate test that env-targeting works only against a temp test root.

2. Resolve the raw physical-path conflict before broad runner wiring.
   - Decide whether canonical physical raw path is sharded (`raw/<shard>/<packet_id>`) or unsharded (`raw/<packet_id>`).
   - Patch `DataLakeRoot`, availability rebuild/read tests, and any migration/read compatibility together. Do not add more live writers into the current mixed state without this decision.

3. After path settlement, wire the lowest-churn direct packet writers.
   - `stage_and_write_packet` users are the easiest: `antiblock_http`, `media`, and `price_payload` can follow the `run_source_capture_http_packet.py` pattern if their staging is already bytes-first.
   - Direct `write_local_source_capture_packet` runners that stage temp files beside `output_directory` need a safer adapter pattern for `data_root` mode. Prefer converting their staged bytes through `stage_and_write_packet` or a shared helper, instead of inventing one-off temp locations.

4. Treat orchestrators separately.
   - For `run_source_capture_durability_series.py`, decide whether child raw packets should commit to the lake while `series_index.json` remains local, or whether a later derived/ack contract should own the series state.
   - For `run_reddit_old_http_batch.py`, decide whether packet dirs move to the lake while batch summary and derived consolidation remain local/rebuildable.

5. Strengthen seam coverage.
   - Replace or supplement the substring allowlist test with a matrix that includes direct producers and packet-producing orchestrators.
   - For every patched runner, add a data-root execution test that asserts raw packet availability by key, mutual exclusion with local output, and no live-root dependency.

## Validation

- Static runner feature scan completed with `rg` and targeted file reads.
- Live root read-only checks completed, except the explicitly recorded accidental test write.
- Targeted tests passed after clearing `ORCA_DATA_ROOT`: `16` passed.
- No implementation patch, Silver Vault edit, runner edit, data-lake code edit, test edit, or live-root cleanup was performed.
