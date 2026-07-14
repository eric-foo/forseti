# Behavioral SCI Code Audit Ledger v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Aggregate findings-first evidence ledger for the commissioned audit of current live Forseti execution behavior.
use_when:
  - Selecting later behavioral-SCI controls from current code evidence.
  - Rechecking an audited behavioral seam or its explicit coverage boundary.
authority_boundary: retrieval_only
branch_or_commit: codex/behavioral-sci-code-audit at 3e4a157fb19de0355eaa9873373c804a28973fc2
stale_if:
  - The cited implementation, wiring, tests, or activation configuration changes.
  - A later accepted audit ledger supersedes this record.
```

## Audit Boundary

- Audited repository revision: `3e4a157fb19de0355eaa9873373c804a28973fc2` on `codex/behavioral-sci-code-audit`.
- Evidence time: `2026-07-14T19:45:36.6730009+08:00`.
- Review-use boundary: findings-first behavioral evidence only. This ledger is not a readiness, validation, approval, acceptance, deployment, or code-quality verdict.
- Coverage method: inventory tracked runner and activation surfaces, follow each selected public entrypoint to its actual owner, durable effects, recovery behavior, and matching tests, then seal one bounded source-loading unit before opening the next.
- Graph-inventory commands: `git ls-files 'forseti-harness/runners/*.py'`; family-scoped `git ls-files`; `rg` import/symbol searches; tracked activation inventory across `.codex/`, `.agents/hooks/`, `.githooks/`, and `.github/workflows/`.
- Initial inventory: 116 tracked runner files including `runners/__init__.py`; 219 Python files across the eleven packet-named owner families; 268 tracked Python test files.
- Inspected so far: generic local-file Source Capture Packet creation; the same packet writer's Data Lake raw-publication and availability-index seam; YouTube watch capture subject binding; Instagram Reels grid capture subject binding; the Bronze-runner lake/identity declaration contract; the bounded Capture→ECR→Cleaning smoke seam; Codex hook activation; local Git hook installation and pre-push mirror; CI hook-command activation; matching targeted tests/self-tests.
- Explicitly uninspected so far: all other source-family capture bodies; YouTube routes other than watch capture; Cleaning and ECR owners outside the smoke seam; Evidence Binding; shared schemas outside selected models; scoring; reports; source observability; case execution; projections; creator/retail/social consumers; Claude hook activation; GitHub branch-protection state; non-hook CI build/dependency behavior. These remain `uninspected`, not negative findings.
- Excluded: historical migration, generated output, ignored or scratch corpus, external parent-checkout material, and owner-deferred routes.
- Unknown or dynamic surfaces: environment-selected data roots, live authentication/network paths, registry/config/reflection activation, filesystem failure modes, optional dependencies, concurrency, and operator runtime state unless a later unit inspects them.
- Not-proven boundaries: passing tests do not prove behavioral completeness; imports and static search do not prove live reachability or absence; selected fixture runs do not prove production environment, authentication, cancellation, concurrency, backpressure, or recovery behavior.

## Behavioral Evidence Rows

| ID | Behavior / consumer | Entrypoint / owner | Inputs / outputs / side effects | Wiring cite | Test cite + public-seam depth | Failure / exit semantics | State / provenance / idempotency | Duplicate / superseded / orphan observations | Status | Severity | Confidence | Minimum closure condition | Candidate control | False-positive / lock-in risk | Not-proven boundaries |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `BSI-001` | Operator packages already-local files to an explicit packet directory with `--output`. | `runners/run_source_capture_packet.py::main` delegates to `source_capture.writer.write_local_source_capture_packet`. | Reads one or more local files; creates the final output directory; copies bodies under `raw/`; writes `manifest.json` and `receipt.md`; prints the output path only on success. | `forseti-harness/runners/run_source_capture_packet.py:60`, `forseti-harness/runners/run_source_capture_packet.py:86`, `forseti-harness/runners/run_source_capture_packet.py:167`, `forseti-harness/runners/run_source_capture_packet.py:255`, `forseti-harness/source_capture/writer.py:44`, `forseti-harness/source_capture/writer.py:109`, `forseti-harness/source_capture/writer.py:199`, `forseti-harness/source_capture/writer.py:316` | `forseti-harness/tests/unit/test_source_capture_packet.py:292`, `forseti-harness/tests/unit/test_source_capture_packet.py:355`, `forseti-harness/tests/unit/test_source_capture_packet.py:462`, `forseti-harness/tests/unit/test_source_capture_packet.py:481`, `forseti-harness/tests/unit/test_source_capture_packet.py:672`; `public_seam` for ordinary success and pre-write rejection, but no injected mid-copy or mid-manifest failure | Preflight input errors return CLI exit 2 and tested cases leave no output. After `_prepare_output_directory`, copies and final files are written directly into the consumer-visible destination with no staging, rollback, or cleanup wrapper; a later copy/write failure returns exit 2 but can leave a partial packet directory. | Packet IDs and hashes are recorded on success. Explicit output mode has no atomic publish or retry identity; a failed partial directory blocks a same-path retry because non-empty output is rejected. | The same final-path multi-file publication defect recurs in `BSI-006`; lake mode is a separate target mode, not duplicate ownership. | `partial` | `major` | `high` for the direct-final-path sequence; `medium` for unexercised filesystem-fault consequences | An explicit-output attempt either publishes a complete, model-valid packet atomically or fails loudly without leaving a consumer-visible partial packet; retry behavior and cleanup ownership are explicit and exercised at the public seam. | `mechanical` | A targeted public-seam fault test or shared atomic directory publisher can enforce all-or-nothing output for this writer. A universal static write-pattern gate would overreach legitimate single-file/rebuildable writes. | No fault-injection test establishes the exact residue for every OS/filesystem failure; concurrent writers and process termination are untested. |
| `BSI-002` | Operator commits a generic packet into the Data Lake and expects it to be discoverable by availability index. | `runners/run_source_capture_packet.py::main` resolves `DataLakeRoot`; `source_capture.writer.write_local_source_capture_packet` stages and publishes raw, then calls `DataLakeRoot.record_availability`. | Stages packet off the authoritative tree; atomically renames it into sharded `raw/`; then atomically replaces a rebuildable availability record; prints committed path only after both steps return. | `forseti-harness/runners/run_source_capture_packet.py:167`, `forseti-harness/runners/run_source_capture_packet.py:189`, `forseti-harness/runners/run_source_capture_packet.py:255`, `forseti-harness/source_capture/writer.py:98`, `forseti-harness/source_capture/writer.py:207`, `forseti-harness/data_lake/root.py:544`, `forseti-harness/data_lake/root.py:560`, `forseti-harness/data_lake/root.py:791` | `forseti-harness/tests/unit/test_run_source_capture_packet_lake.py:49`, `forseti-harness/tests/unit/test_run_source_capture_packet_lake.py:62`, `forseti-harness/tests/test_data_lake_availability.py:28`, `forseti-harness/tests/test_data_lake_availability.py:53`, `forseti-harness/tests/test_data_lake_doctor.py:45`; `module_seam` with a real fixture-backed lake, but no injected post-publish index failure | Raw publication is atomic and write-once. Availability is recorded afterward. If availability writing fails, the CLI returns exit 2 without printing the already-committed packet identity; raw remains durable and repairable, while the failed call presents as total failure. | Raw is authoritative and availability is rebuildable. Doctor reports missing availability and can rebuild it. A blind retry generates a new packet ID, so partial success can create duplicate source captures unless the operator discovers the first raw packet. | No second live owner observed for generic raw publication. Rebuild ownership exists in Data Lake doctor and is recovery, not duplicate primary ownership. | `partial` | `major` | `high` for commit-before-index ordering and repairability; `medium` for the unexercised producer failure path | Post-publication index failure preserves and reports the committed packet identity and explicit partial-success/recovery state, so operators can repair or resume without blindly duplicating the capture; the public seam exercises this outcome. | `resident_judgment` | A mechanical transaction rule spanning authoritative raw and rebuildable indexes would conflate different durability classes. Review should require explicit partial-success semantics at this seam; consider a deterministic test only after closure design is chosen. | No injected `record_availability` failure test; crash timing, concurrent captures, and live removable-media behavior are not proven. |
| `BSI-003` | Operator captures a requested YouTube video's served watch metadata/comments for downstream creator-metric consumers. | `runners/run_source_capture_youtube_watch_packet.py::run_source_capture_youtube_watch_packet` calls `youtube_capture.capture_youtube_v0.fetch_youtube_watch`, then `source_capture.youtube_watch_packet.write_youtube_watch_packet`. | Fetches by requested video ID; preserves served HTML, capture JSON, comments pages, metric receipts, canonical/watch/channel data nested in the fetched packet; writes a Source Capture Packet attributed to the requested ID. | `forseti-harness/runners/run_source_capture_youtube_watch_packet.py:28`, `forseti-harness/runners/run_source_capture_youtube_watch_packet.py:40`, `forseti-harness/runners/run_source_capture_youtube_watch_packet.py:45`, `forseti-harness/source_capture/youtube_watch_packet.py:63`, `forseti-harness/source_capture/youtube_watch_packet.py:79`, `forseti-harness/source_capture/youtube_watch_packet.py:84`, `forseti-harness/source_capture/youtube_watch_packet.py:102`, `forseti-harness/source_capture/youtube_watch_packet.py:178` | `forseti-harness/tests/unit/test_source_capture_youtube_watch_packet.py:34`, `forseti-harness/tests/unit/test_source_capture_youtube_watch_packet.py:91`, `forseti-harness/tests/unit/test_source_capture_youtube_watch_packet.py:293`; `module_seam` with a fake fetcher and real packet/lake writes; no requested-versus-served mismatch case | Invalid requested ID shape and empty HTML fail with code 5. The writer copies `fetch.video_id` into `platform_video_id` and attributes the packet to a watch URL, but does not compare it with the fetched packet's `video_id` or `canonical_url`; a syntactically valid wrong/redirected served video can be durably attributed to the request. | Packet provenance preserves the fetched packet and bytes, so later forensic comparison is possible. Admission itself has no subject-binding state; downstream selection by requested ID can consume misattributed metrics. | Fleet inventory declares this runner `unbound`; no duplicate live owner was inspected. Other YouTube capture routes remain uninspected. | `partial` | `major` | `high` | Before durable packet admission, the served video identity is compared with the requested ID using a source-visible stable identifier; mismatch and unavailable identity are distinct fail-loud states covered at the public/module seam. | `mechanical` | Exact video-ID equality at this producer boundary is objective and low-lock-in when the served canonical/video ID is present. Missing/redirect formats need an explicit unavailable path; a universal cross-platform identity rule would be brittle. | Live redirect behavior, fetcher guarantees, aliases, removed videos, and downstream consumer exposure were not executed; only this watch route was inspected. |
| `BSI-004` | Operator captures a requested Instagram creator's Reels grid and profile metrics for monitoring/projection consumers. | `runners/run_source_capture_ig_reels_grid_packet.py::run_source_capture_ig_reels_grid_packet` owns browser capture, profile parsing, slice construction, and packet handoff. | Requests normalized `/<handle>/reels/`; preserves DOM rows and passive JSON; extracts profile ID and metrics; writes a Source Capture Packet whose locator and summary use the requested handle. | `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:104`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:117`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:119`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:137`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:151`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:297`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:337`, `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py:407` | `forseti-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py:22`, `forseti-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py:124`, `forseti-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py:259`, `forseti-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py:415`; `module_seam` with real packet/lake writes; the main passive-profile fixture omits `username` | Capture failure returns 3; login/rate/block/challenge detection returns 5 with no packet. A clean final URL is not compared to the requested handle, and passive `web_profile_info` user data contributes metrics without preserving or comparing its username; a wrong but clean served profile can be committed under the requested creator. | Numeric profile ID and other profile facts are preserved when present, but no requested-handle-to-served-identity binding state is stored. Repeated capture can therefore build a consistent series under a stale or wrong requested identity. | Fleet inventory declares this runner `unbound`; the older IG calls route is an explicit fallback/legacy route but was not inspected for duplicate ownership. | `partial` | `major` | `high` | Before creator-attributed packet admission, source-visible served username/profile identity is preserved and compared with the normalized request; mismatch and identity-unavailable states fail loudly or remain explicitly unadmitted, with a mismatch test at the module seam. | `mechanical` | Per-family normalized username equality is objective when `web_profile_info` exposes it. Username changes, missing profile JSON, and canonicalization need explicit handling; a universal identity detector would create false confidence. | Live IG redirects, handle renames, private profiles, response variation, fallback routes, and downstream projection behavior were not executed. |
| `BSI-005` | This linked worktree runs tracked local Git commit/push adapters before repository lifecycle actions. | Git resolves `core.hooksPath`; `.githooks/pre-push` delegates to `pre_push_guard.py`; `.githooks/commit-msg` delegates repo-map/review-routing checks; `install-local-hooks.ps1 -VerifyOnly` owns installation verification. | Reads Git hook configuration and executes thin tracked adapters. Current worktree config resolves to `C:\Users\vmon7\Desktop\projects\orca\.githooks`, outside this receiver root; those adapter bytes currently equal this worktree's copies. | `.github/scripts/install-local-hooks.ps1:33`, `.github/scripts/install-local-hooks.ps1:38`, `.github/scripts/install-local-hooks.ps1:41`, `.github/scripts/install-local-hooks.ps1:69`, `.github/scripts/install-local-hooks.ps1:77`, `.githooks/pre-push:1`, `.githooks/pre-push:5`, `.githooks/commit-msg:1`, `.githooks/commit-msg:7`, `.githooks/commit-msg:12`, `.agents/hooks/pre_push_guard.py:35`, `.agents/hooks/pre_push_guard.py:130`, `.agents/hooks/pre_push_guard.py:209` | `.agents/hooks/pre_push_guard.py:154`, `.codex/hooks/forseti_guard_codex_adapter.py:185`; `module_seam` self-tests. Installation verifier is the public operator seam and fails in this worktree. | `-VerifyOnly` exits 1 and names the absolute parent path mismatch. Ordinary hooks can still fire today because the parent adapters exist and are byte-identical, but a current-branch adapter change would not be the executable adapter selected by this worktree until configuration is corrected. | Hook activation is coupled to a separate checkout's path and bytes. Policies invoked by the thin adapters are relative and were not executed through an actual commit/push in this audit. Server CI remains authoritative and local hooks remain bypassable. | No duplicate policy owner: adapters are thin and policy lives under `.agents/hooks/`. The configured adapter copy is a second physical checkout surface whose current byte equality is observed, not guaranteed. | `partial` | `minor` | `high` | `core.hooksPath` resolves to this worktree's tracked `.githooks`; `install-local-hooks.ps1 -VerifyOnly` passes; required adapters exist and their delegated policy paths resolve from the active worktree. | `no_standing_control` | The existing verifier already detects the defect deterministically. Adding another standing gate would duplicate ownership; correct the installation and retain the existing verify route. | Actual Git commit/push hook invocation, shell working-directory behavior, `--no-verify`, remote CI, and server branch protection were not exercised. |
| `BSI-006` | Operator stitches existing Capture artifacts through ECR source-side receipts into one Cleaning smoke output set. | `runners/run_capture_ecr_cleaning_smoke.py::run_capture_ecr_cleaning_smoke` owns source-family dispatch, validation, ECR receipt/cleaning handle construction, and final output publication. | Reads a manifest plus packet/projection/consolidation/lake records; verifies selected packet paths and hashes; builds three outputs: ECR receipts, Cleaning packet, and smoke summary; writes them into one requested directory. | `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:117`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:132`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:152`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:160`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:166`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:182`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:243`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:274`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:1467`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:1476`, `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py:1590` | `forseti-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py:40`, `forseti-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py:909`, `forseti-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py:1000`, `forseti-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py:1052`, `forseti-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py:1096`; `module_seam` with real fixture artifacts and output files; no injected second/third-output write failure | Named unsupported/lake-missing sources and validation errors fail before final writes. The three consumer-visible outputs are then written sequentially without staging or rollback. An `OSError` is outside the CLI's caught `ValueError`/`ValidationError` set, and a second/third write failure can leave a partial output set; any existing output then blocks same-path retry. | Successful artifacts preserve ECR/cleaning lineage and findings. The output set has no atomic commit marker, run receipt on write failure, rollback, or resumable/idempotent publication state. | Repeats the direct-final multi-file publication shape in `BSI-001`; no duplicate cross-stage owner was inspected. | `partial` | `major` | `high` | The three-file smoke result becomes consumer-visible as one complete set or not at all; mid-publication failure leaves an explicit recoverable state and same-path retry semantics, exercised by deterministic fault injection. | `mechanical` | A targeted all-or-nothing output-set test at this runner is objective and low false-positive. A generic ban on sequential writes would incorrectly cover disposable/rebuildable outputs with different contracts. | Process kill, disk-full, concurrent writers, directory durability/fsync, and real lake/removable-media failures were not exercised. |

## Unit 1 — Generic Source Capture Packet and Lake Commit

### Findings-first summary

1. `BSI-001`: explicit local output is consumer-visible before packet completion. Existing tests cover success, invalid inputs, and occupied destinations, but not failure after the destination is created.
2. `BSI-002`: lake raw truth is committed before the rebuildable availability fact. Recovery exists and is tested independently, but the producer's post-commit failure contract does not expose partial success or the committed identity.

### Blind-spot observations

- Entrypoint-to-owner reachability: observed for the generic packet CLI.
- Runner thinness: observed; argument construction and exit translation remain in the runner, while durable writing is owned by `source_capture.writer`.
- Cross-stage seam: observed through raw publication, availability, retrieval, and doctor recovery.
- Schema/version/producer/consumer alignment: packet model validation and by-key loader are inspected only at the cited seam; broader consumers remain uninspected.
- Failure taxonomy: ordinary success and pre-write terminal failure are visible; durable partial success is not separately represented.
- Retry/idempotency: no stable retry identity on either selected mode; exact repeated-run consequences beyond occupied explicit output and new lake packet IDs are not proven.
- Atomicity/cleanup: lake raw publish is atomic; local explicit output is not; staging cleanup after pre-publish failure remains uninspected.
- Provenance: successful manifests record raw stored-byte hashes and limitation facts; failure receipts do not exist for the identified partial outcomes.
- Dynamic activation, compatibility callers, concurrency, cancellation, timeouts, secrets/authentication, and CI/local parity: uninspected for this unit.
- Test realism: fixture-backed public/module seams exercise real filesystem output and Data Lake logic, but fault injection and live environment state are absent.

### Source-read receipt

- Sources: `forseti-harness/runners/run_source_capture_packet.py`; `forseti-harness/source_capture/writer.py`; relevant `DataLakeRoot` construction/write/read/index methods in `forseti-harness/data_lake/root.py`; four matching test files.
- Search boundary for missing fault coverage: tracked `forseti-harness/tests/`, `source_capture/`, and `data_lake/` searches for injected `copy2`, raw-publish, availability-write, staging-cleanup, and partial-output failures returned no matches.
- Targeted test command: `python -m pytest -p no:cacheprovider --basetemp C:\tmp\pytest_behavioral_sci_unit1 -q tests\unit\test_source_capture_packet.py tests\unit\test_run_source_capture_packet_lake.py tests\test_data_lake_availability.py tests\test_data_lake_doctor.py` from `forseti-harness/` with `PYTHONDONTWRITEBYTECODE=1`.
- Test result: exit `0`; 40 tests passed. This supports the cited success/recovery behaviors only.
- Unit-seal ledger SHA256 before the next source-loading unit: `fc6f9b469cb262fb036324511b20e9ac776e179552a52bc07f6ff9d22e2086fe`.

## Unit 2 — Social Capture Subject Identity Binding

### Findings-first summary

1. `BSI-003`: YouTube watch capture validates requested ID shape but never compares served packet/canonical identity to that request before durable attribution.
2. `BSI-004`: Instagram Reels capture rejects known access-block routes but does not preserve or compare passive profile username with the requested handle before durable creator attribution.
3. The fleet contract currently detects 27 Bronze-writing runners, no `KNOWN_UNSYNCED` lake exceptions, and shape-valid identity declarations. The declarations count is 5 `bound`, 12 `unbound`, and 10 `not_applicable`; only the two rows above were reverified against implementation bodies, so the other ten `unbound` declarations remain orientation, not audit findings.

### Blind-spot observations

- Entrypoint-to-owner reachability: observed for both selected public runners and their packet writers.
- Runner thinness: YouTube runner delegates durable construction; Instagram runner owns capture orchestration, parsing, attribution, and packet assembly in one large module. No duplicate-business-logic conclusion is made without inspecting sibling routes.
- Schema/producer/consumer alignment: requested identifiers and fetched payload identities coexist, but admission does not bind them. Downstream creator-metric and projection consumers were not inspected in this unit.
- Failure taxonomy: syntactic invalidity, capture failure, and known access blocks are distinct; wrong-subject clean success is not represented.
- Durable provenance: raw served artifacts are retained, enabling later forensic discovery, but the admission-time binding fact is absent.
- Dynamic activation: direct CLI wiring is observed; schedules, registries, operator wrappers, authentication state, and environment-dependent redirects are uninspected.
- Compatibility/supersession: the IG runner states that it supersedes the older calls route as default, but current live caller selection was not proven.
- Test realism: tests exercise real packet/lake writes with fake fetch/capture results; no adversarial mismatch fixture exists for either selected route.
- Timeout, cancellation, retry, idempotency, concurrency, backpressure, secrets, and CI/local parity: uninspected for this unit.

### Source-read receipt

- Sources: fleet detector and declarations in `forseti-harness/data_lake/inventory.py`; `tests/contract/test_capture_runner_lake_seam_coverage.py`; selected YouTube runner/writer/tests; selected Instagram runner/tests.
- Search boundary: exact selected runner/owner/test files plus tracked fleet declaration code. No claim is made that the remaining declared-unbound runners share the same implementation defect.
- Targeted test command: `python -m pytest -p no:cacheprovider --basetemp C:\tmp\pytest_behavioral_sci_unit2 -q tests\unit\test_source_capture_youtube_watch_packet.py tests\unit\test_source_capture_ig_reels_grid_packet.py tests\contract\test_capture_runner_lake_seam_coverage.py` from `forseti-harness/` with `PYTHONDONTWRITEBYTECODE=1`.
- Test result: exit `0`; 39 tests passed. This supports ordinary capture, lake wiring, and declaration shape only; identity completeness remains disproven by current producer code.
- Unit-seal ledger SHA256 before the next source-loading unit: `9990258fc0de1d35e4fbe68f1a697f9103936815b713d5c6d26980a7060e361d`.

## Unit 3 — Codex, Local Git, and CI Activation

### Findings-first summary

1. `BSI-005`: local Git hooks are installed to an absolute `.githooks` path in the separate parent checkout, so this worktree fails the repository's own installation verifier. Current thin adapter bytes match, which bounds the present impact to activation drift and delayed divergence risk.
2. Codex tracked activation points PreToolUse at the Forseti guard adapter and PostToolUse at repo-map and Google search-surface checks (`.codex/hooks.json:3`, `.codex/hooks.json:17`). The adapter self-test passed; harness trust/loading state outside the tracked config is not proven.
3. Local pre-push mirrors nine selected strict checks (`.agents/hooks/pre_push_guard.py:35`); CI derives twenty hook commands and then runs the harness test suite (`.github/workflows/ci.yml:54`, `.github/workflows/ci.yml:119`). This is documented defense-in-depth, not full local/CI parity.

### Blind-spot observations

- Dynamic activation: tracked Codex, local Git, and CI wiring inspected; actual GitHub execution, Codex trust UI state, Claude activation, and server branch protection uninspected.
- CI/local parity: objective gate-count difference observed. Local pre-push is earlier feedback only; CI-only failure latency remains visible.
- Failure visibility: hook-install verification fails loudly; guard self-tests fail closed for their named cases; actual hook subprocess launch from Git was not exercised.
- Compatibility/current callers: `.codex/hooks/orca_guard_codex_adapter.py` remains a legacy shim but active tracked config points to the Forseti adapter. The shim body was not inspected because it is not the current activation target.
- Environment/path handling: absolute parent hook path is the observed defect. Cross-shell executable bits, Python availability, and hook working directory remain not proven.
- Concurrency, cancellation, retries, backpressure, authentication, and secrets are not applicable or uninspected at this activation unit.

### Source-read receipt

- Sources: `.codex/hooks.json`; current and configured `.githooks` adapter hashes; `.github/scripts/install-local-hooks.ps1`; `.agents/hooks/pre_push_guard.py`; `.codex/hooks/forseti_guard_codex_adapter.py`; `.github/workflows/ci.yml`.
- Commands: `git config --show-origin --get core.hooksPath`; adapter SHA256 comparisons; `pwsh .github/scripts/install-local-hooks.ps1 -VerifyOnly`; both named self-tests; `pwsh .github/scripts/run-doc-gates.ps1 -List`.
- Results: install verification exit `1` with exact path mismatch; both self-tests exit `0`; CI gate list exit `0` with 20 derived hook commands. Passing self-tests establish only their coded cases.
- Unit-seal ledger SHA256 before the next source-loading unit: `e713a63210bcada9b1923b60e42327dddc18dde333f88cb6dffbd23b14d1ef28`.

## Unit 4 — Capture to ECR to Cleaning Smoke Publication

### Findings-first summary

1. `BSI-006`: the runner performs substantial validation before writing, then publishes three final JSON files sequentially. Mid-publication failure leaves an incomplete, retry-blocking output set.
2. The seam fails closed when a named ASR source lacks Data Lake access and validates selected packet path/hash lineage before output. Those positive behaviors do not close output-set atomicity.

### Blind-spot observations

- Cross-stage completeness: inspected across existing Capture inputs, ECR receipt construction, Cleaning handles, and output summary for the smoke route only.
- Schema/version/producer/consumer alignment: Pydantic models and explicit hash/path checks are used at selected boundaries; downstream non-smoke Cleaning consumers remain uninspected.
- Failure taxonomy: input/validation failures are visible; mid-publication partial success has no distinct state or receipt.
- Atomicity/resume/cleanup: final output set is not atomic, resumable, or automatically cleaned; this repeats `BSI-001`.
- Provenance/limitations: successful ECR and Cleaning artifacts carry lineage/findings; failed writes have no durable limitation record.
- Test realism: 49 fixture-backed tests exercise multiple families, hash/path drift, and periodic audit behavior; filesystem write faults and process termination are absent.
- Dynamic activation, compatibility callers, concurrency, backpressure, locking, live authentication/secrets, and CI/local parity: uninspected for this unit.

### Source-read receipt

- Sources: `forseti-harness/runners/run_capture_ecr_cleaning_smoke.py`; matching comprehensive unit test file; imported model/deriver behavior only to the depth reached by the runner and tests.
- Search boundary for fault coverage: the matching test file searched for monkeypatched/raised `_write_json`, partial-output cleanup, and mid-write failure; no matching test was found.
- Targeted test command: `python -m pytest -p no:cacheprovider --basetemp C:\tmp\pytest_behavioral_sci_unit4 -q tests\unit\test_capture_ecr_cleaning_smoke_runner.py` from `forseti-harness/` with `PYTHONDONTWRITEBYTECODE=1`.
- Test result: exit `0`; 49 tests passed. This supports the cited semantic/input validation behaviors, not atomic publication.
- Unit-seal ledger SHA256 before final validation: `b684233bfbe1827b86ebe1b0abe566151e2fc9cbe21baf7d88e247f227f12250`.

## Cross-Family Synthesis

### Repeated versus isolated

- Repeated: missing requested-versus-served subject binding at durable social-capture admission (`BSI-003`, `BSI-004`). The defect shape recurs across YouTube video and Instagram creator attribution, while platform-specific evidence fields differ.
- Repeated: consumer-visible multi-file output before full publication (`BSI-001`, `BSI-006`). Both writers preflight destination state, then write directly into the final location and make same-path retries fail after partial residue.
- Isolated so far: post-publish availability partial success (`BSI-002`) and worktree hook-path activation drift (`BSI-005`).

### Evidence-supported principles

When durable evidence is indexed or summarized under a requested subject, preserving served bytes is not the same as binding those bytes to the request. The admission seam needs a source-visible identity comparison or an explicit unbound state; this is supported by `BSI-003` and `BSI-004`.

When several files collectively represent one consumer-visible result, validating inputs before the first write is insufficient: the result needs one publication boundary or an explicit partial-success/recovery contract. This is supported by `BSI-001` and `BSI-006`.

### Exact enforcement boundaries

- `BSI-003`: immediately before `stage_and_write_packet` in the YouTube watch writer, compare the requested video ID with a preserved source-visible served/canonical ID. A mismatch fixture must fail before packet publication.
- `BSI-004`: after passive `web_profile_info` user parsing and before slice/packet publication, preserve and compare normalized served username/profile identity with the request. Missing and mismatched identities must be distinguishable.
- `BSI-001` and `BSI-006`: at each public output publisher, deterministic fault injection on the second or later file write must prove that no consumer-visible partial final set remains and that retry/recovery is explicit. This can be implemented through a behavior-specific atomic directory/set publisher; no universal source scanner is recommended.

### Semantic resident checks

- `BSI-002`: decide the intended operator contract when authoritative raw commits but a rebuildable index write fails. Evidence needed: durability class, discoverability route, safe retry identity, and whether returning partial success is acceptable. Deterministic enforcement before that decision would risk rolling back authoritative truth or pretending a rebuildable index is transactional authority.
- Missing served identity policy for renamed/private/unavailable profiles remains a resident product/source judgment. Once the allowed states are chosen per source family, exact equality/mismatch behavior can be mechanical.

### Rejected tempting proxies

- Literal retrieval headers on code: code is excluded by retrieval-metadata authority and headers would not prove behavioral wiring.
- Per-file repo-map rows: T1 is an area router, not a runner inventory.
- Universal orphan-code detector: dynamic/config/compatibility activation makes universal absence mechanically unreliable.
- Import reachability as completeness: imports do not prove consumer, state, failure, or runtime behavior.
- Passing tests as completeness: all targeted suites passed while `BSI-001`, `BSI-003`, `BSI-004`, and `BSI-006` remain visible in implementation.
- Shape-valid identity declarations as subject binding: the fleet contract preserves `unbound` states; declaration shape is not runtime proof.
- Current equality of parent/current Git hook adapter hashes as correct activation: the repository verifier still fails because the configured path is the wrong worktree surface.

### Prioritized later implementation candidates

1. `BSI-003` + `BSI-004` subject binding. Defect caught: durable wrong-subject attribution. Proof target: adversarial mismatch fixtures fail before packet publication while matched and explicitly unavailable allowed states behave distinctly. Maintenance cost: per-family identity extractor/comparator. Smallest complete closure: bind the two inspected routes only; do not claim the other ten declared-unbound routes are fixed.
2. `BSI-001` + `BSI-006` atomic result publication. Defect caught: partial consumer-visible output and retry blockage. Proof target: same public seam with deterministic second-write failure leaves no partial final result and exposes retry/recovery state. Maintenance cost: a small shared atomic-set helper only if both closures truly share the same durability contract; otherwise two local closures.
3. `BSI-002` partial durable success contract. Defect caught: blind retry after raw commit/index failure. Proof target: injected availability failure returns the committed identity and a repairable state without duplicating raw. Maintenance cost: producer result/CLI contract plus recovery test.
4. `BSI-005` hook-path correction. Defect caught: current worktree selecting another checkout's adapter. Proof target: existing `-VerifyOnly` passes. Maintenance cost: none beyond correcting local config; no new control recommended.

### Residuals and upgrade triggers

- Ten other fleet declarations are `unbound`, but their bodies were not verified. Upgrade trigger: owner selects broader subject-binding audit or a downstream incident names one route.
- Dynamic registries, schedules, environment-specific activation, live network/authentication, concurrency, cancellation, backpressure, and process-crash durability remain uninspected. Upgrade trigger: production evidence, a failing public seam, or a control decision that depends on them.
- Cleaning, ECR, Evidence Binding, schemas, scoring, reports, observability, projections, and case execution remain largely uninspected beyond the one smoke seam. Upgrade trigger: owner needs coverage for a particular consumer or a row's closure depends on that family.
- Local pre-push covers nine selected gates while CI derives twenty. Upgrade trigger: repeated CI-only failures whose earlier local detection would materially reduce iteration cost.
- The audit sampled current tracked code and fixture-backed tests; it did not run live source capture or the full suite. Upgrade trigger: a strict runtime/production claim, release decision, or remediation verification.

### Control-selection summary

| Recommendation class | Rows | Recurrence/evidence | False-positive / lock-in posture | Owner decision |
| --- | --- | --- | --- | --- |
| `mechanical` | `BSI-003`, `BSI-004` | Requested-versus-served binding gap confirmed in two source families. | Low false positive for exact stable IDs when present; missing/rename policy must be bound first; no universal cross-platform detector. | Open. |
| `mechanical` | `BSI-001`, `BSI-006` | Partial final publication recurs in two multi-file result writers. | Use public-seam fault tests/atomic publishers only for outputs that form one durability unit; avoid generic sequential-write bans. | Open. |
| `resident_judgment` | `BSI-002` | One authoritative-raw/rebuildable-index partial-success seam. | Transactional enforcement could conflate durability classes; decide operator contract first. | Open. |
| `no_standing_control` | `BSI-005` | One installation mismatch caught by the existing verifier. | New automation would duplicate the current deterministic check. | Open. |

## Commissioned Blind-Spot Coverage Matrix

| Blind spot | Audit state | Evidence / boundary |
| --- | --- | --- |
| Entrypoint-to-owner reachability | `observed` | Selected generic, YouTube, Instagram, smoke, and hook paths traced; other runners uninspected. |
| Runner thinness vs duplicated lifecycle logic | `observed` / `not_proven` | Generic/YouTube are thin; Instagram and smoke own orchestration; sibling-owner duplication not broadly inspected. |
| Cross-stage seam completeness | `observed` / `partial` | Data Lake raw→availability and Capture→ECR→Cleaning smoke inspected; other stage seams uninspected. |
| Schema/version/producer/consumer alignment | `observed` / `not_proven` | Selected Pydantic/hash/path seams inspected; broad downstream alignment not proven. |
| Failure taxonomy | `observed` / `partial` | Several exits/blocks distinct; partial durable success and partial result publication lack explicit states. |
| Timeout, cancellation, retry, idempotency | `uninspected` / `not_proven` | Retry consequences noted for rows; live timeout/cancellation behavior not audited. |
| Side effects, atomicity, resume, rollback, cleanup | `observed` / `partial` | Two repeated atomic-publication gaps and one post-publish index seam; crash/concurrency residuals remain. |
| Durable provenance and limitation reporting | `observed` / `partial` | Success paths preserve hashes/limitations; identified failure paths lack durable partial-state receipts. |
| Dynamic activation | `observed` / `partial` | Tracked Codex/Git/CI routes inspected; schedules, registries, trust state, and GitHub runtime uninspected. |
| Compatibility, supersession, live callers | `partial` | IG supersession note and Codex legacy shim observed; actual caller selection not proven. |
| Test realism / mocked seams | `observed` | 128 targeted tests plus self-tests passed; fake capture inputs and absent fault injection explicitly bounded. |
| Environment, path, dependency, auth, secrets | `observed` / `partial` | Hook-path drift found; live source auth/dependency/secret behavior uninspected. |
| Concurrency, backpressure, locking, repeated runs | `uninspected` / `not_proven` | Static retry/residue consequences only; no concurrent execution. |
| Operator diagnostics and recovery locality | `observed` / `partial` | Doctor recovery and hook verifier are visible; raw/index partial success and multi-file partial output are not locally actionable. |
| CI/local boundary parity | `observed` / `partial` | Nine selected pre-push gates vs twenty CI hook commands; server execution not run. |
| Implemented but unwired | `observed` / `not_proven` | Detector finds no unsynced Bronze writer; other implementation families and dynamic wiring uninspected. |
| Reachable code without distinct consumer/owner | `uninspected` | Universal absence claim intentionally not attempted. |
| Behavior depending on authoring-chat knowledge | `not_proven` | Selected behavior uses durable args/config/artifacts; broad repository dependence on chat was not mechanically inferred. |

## Rerunnable Command and Evidence Appendix

| Unit | Command / evidence | CWD | Revision | Exit | Short result |
| --- | --- | --- | --- | --- | --- |
| Inventory | `git ls-files 'forseti-harness/runners/*.py'` plus family/test/activation inventories | repository root | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | 116 runner files including package initializer; 219 named-family owner Python files; 268 Python tests. |
| Unit 1 | Targeted pytest command recorded above | `forseti-harness/` | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | 40 passed. |
| Unit 2 | Targeted pytest command recorded above | `forseti-harness/` | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | 39 passed. |
| Unit 3 | `pwsh .github/scripts/install-local-hooks.ps1 -VerifyOnly` | repository root | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `1` | Correctly reported configured parent-checkout hook path instead of current `.githooks`. |
| Unit 3 | `python .agents/hooks/pre_push_guard.py --selftest` | repository root | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | Nine mirrored gate cases and protected-push cases passed. |
| Unit 3 | `python .codex/hooks/forseti_guard_codex_adapter.py --selftest` | repository root | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | Guard and adapter cases passed. |
| Unit 3 | `pwsh .github/scripts/run-doc-gates.ps1 -List` | repository root | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | Derived 20 CI hook commands. |
| Unit 4 | Targeted pytest command recorded above | `forseti-harness/` | `3e4a157fb19de0355eaa9873373c804a28973fc2` | `0` | 49 passed. |

## Validation and Lifecycle State

- Ledger validation: pending final citation-path, retrieval-header, placement, repo-map, handoff-pointer, DCP-shape, diff, and fresh-read gates.
- Publication: pending final commit, push, and focused ready PR. Merge is not authorized.
