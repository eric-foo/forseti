```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial implementation review of Data Capture posture-vocabulary enforcement.
use_when:
  - Inspecting implementation findings before accepting or patching the enforcement change.
  - Tracing posture-vocabulary enforcement decisions to their review evidence.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_implementation_adversarial_review_v0.md
  recommendation: patch_before_acceptance
  summary: "R2 should not be treated as settled yet because current on-disk source_capture packet manifests still fail the new schema: all lack hash_basis, and two retain off-vocabulary known cutoff_posture narratives."
  findings_count: 2
  blocking_findings:
    - R2-01: Existing packet manifests lack required hash_basis and fail read-back.
    - R2-02: Existing packet manifests still carry off-vocabulary known cutoff_posture narratives.
  advisory_findings: []
  prior_findings_remediated:
    - AR-03: source_quality.py no longer derives source_or_snapshot_time from cutoff_posture.
    - AR-04-new-writes: writer records raw_stored_bytes for new preserved files.
    - AR-05-new-writes: archive runner emits archived/attempt_failed as known values and keeps detail outside the posture value.
  next_action: "Do not ratify R2 or bind JSG-01 to it until the current packet-manifest compatibility gap is closed or the owner explicitly scopes those untracked manifests out of the ratification surface."
```

# Data Capture Spine Posture Vocabulary Enforcement - Implementation Adversarial Review v0

## Source Readiness

SOURCE_CONTEXT_READY.

Authority and method sequence:

- `AGENTS.md` was supplied in the current thread; `.agents/workflow-overlay/README.md` was read.
- Orca review-lane and prompt-output authority was read from `.agents/workflow-overlay/review-lanes.md` and `.agents/workflow-overlay/prompt-orchestration.md`.
- `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were REFERENCE-LOADed before task source analysis and applied only after SOURCE_CONTEXT_READY.
- Review output mode is `review-report`; destination is this file under `docs/review-outputs/adversarial-artifact-reviews/`.
- Edit boundary: reviewed implementation and doctrine were not patched. This report is the only written artifact.

Prompt anchor hashes:

- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`: confirmed `806E7CE9DC92CFB57CDFFD62AA14091DC9EA2C29BD28D23B21AE138F69DF3ED4`.
- `orca-harness/source_capture/models.py`: confirmed `6506ACA56FA7B3768552F0F382DAEB474EA4D0EB5B238C3BA47108B159121E75`.

Dirty-state boundary:

- `git status --short --branch` showed `main...origin/main [ahead 6]` with many modified and untracked Orca sources, including the controlling doctrine file, the implementation files under review, untracked `orca-harness/reports/source_capture/`, and untracked `orca-harness/source_capture/packet_assembly.py`.
- This review is advisory only. It does not approve, validate, ratify, settle, commit, push, or unfreeze JSG-01.

Model-family precondition:

- The prompt names Claude as author. This reviewer runtime is Codex/GPT-5, so the cross-family review bar is met from visible runtime identity.

Validation/read evidence run during review:

- Targeted tests command: `python -m pytest -p no:cacheprovider -q --basetemp pytest_review_tmp orca-harness\tests\unit\test_source_capture_packet.py orca-harness\tests\unit\test_source_capture_archive_org.py orca-harness\tests\unit\test_source_capture_direct_http.py orca-harness\tests\unit\test_source_capture_media_asset.py orca-harness\tests\unit\test_source_quality_state_assembler.py orca-harness\tests\unit\test_source_quality_report_skeleton.py`
- Result: passed (`.....................................................................    [100%]`).
- Structured manifest read-back check: all three manifests under `orca-harness/reports/source_capture/**/manifest.json` were parsed, their preserved-file hashes recomputed from `relative_packet_path`, and then passed to `SourceCapturePacket.model_validate`. All three failed model validation for missing `hash_basis`; two also failed for off-vocabulary known `cutoff_posture` values. The stored file bytes matched their recorded `sha256` values.

## Findings

### R2-01 - Existing packet manifests lack required hash_basis and fail read-back

- severity: major
- seam: hash_basis recomputation-bound / migration completeness / read-back compatibility
- phase: correctness

Evidence:

- `PreservedFile.hash_basis` is now a required field with no default in the schema (`orca-harness/source_capture/models.py:97-103`).
- The schema closes `hash_basis` to `raw_stored_bytes` only (`orca-harness/source_capture/models.py:57-66`) and rejects any other value (`orca-harness/source_capture/models.py:105-114`).
- New writer output sets `hash_basis="raw_stored_bytes"` after copying each input and hashing the destination file (`orca-harness/source_capture/writer.py:253-267`).
- `hash_file` hashes the raw stored bytes by reading the file bytes directly (`orca-harness/harness_utils.py:33-34`).
- Existing manifest `slot3_reddit_batch1_packet_dry_run` has `preserved_files[0]` with `relative_packet_path`, `sha256`, and `size_bytes`, but no `hash_basis` before the object closes (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run/manifest.json:36-43`).
- Existing manifest `slot3_reddit_batch1_packet_dry_run_2` has the same missing field shape (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/manifest.json:36-43`).
- Existing manifest `slot3_reddit_batch1_packet_post_patch_dry_run` has the same missing field shape (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_post_patch_dry_run/manifest.json:35-42`).
- The proposal made migration of existing packets/tests a pre-ratification requirement, not a later generic cleanup (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:121-131`).

Why this matters:

The new writer path is honest for future packets, but the current packet corpus in the prompt's required read-pack is not migrated. Required-with-no-default is therefore not just a schema tightening; it breaks read-back of every currently present `orca-harness/reports/source_capture/**/manifest.json` packet reviewed. That directly fails the prompt's "existing packets still validate" gate and prevents treating R2 as settled.

minimum_closure_condition:

Every current packet manifest that remains in the ratification/read-back surface must carry a recomputation-bound `hash_basis` consistent with the bytes at its `relative_packet_path`, and `SourceCapturePacket.model_validate` must succeed for the packet corpus under `orca-harness/reports/source_capture/**/manifest.json`; alternatively, the owner must explicitly declare these untracked manifests outside the current ratification surface before R2 is treated as settled.

next_authorized_action:

Owner/Data Capture lane decision: authorize a bounded packet-manifest migration or replay, or explicitly scope these untracked packet manifests out of the ratification surface, then rerun the manifest validation/read-back check. This review does not authorize or execute that patch.

### R2-02 - Existing packet manifests still carry off-vocabulary known cutoff_posture narratives

- severity: major
- seam: cutoff posture closure / migration completeness / no silent survivor
- phase: correctness

Evidence:

- The doctrine now says `cutoff_posture.status == known` must use one of `pre_cutoff`, `post_cutoff`, `mixed`, or `unknown`, and says narrative belongs in `capture_context` or a non-known status reason (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:272-278`).
- The schema implements the same closed cutoff set (`orca-harness/source_capture/models.py:53`) and validates `PacketTiming.cutoff_posture` against it (`orca-harness/source_capture/models.py:82-94`).
- The previous proposal explicitly named the off-vocabulary existing packets as migration debt and bound a compatibility stance before ratification (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:124-129`).
- The prior adversarial review named the same two packet manifests as outside the proposed cutoff set (`docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md:84-90`).
- `slot3_reddit_batch1_packet_dry_run_2` still records capture-level `cutoff_posture.status` as `known` with value `local JSON/file state supplied for the Slot 3 pressure-test capture; no live Reddit continuation or archive lookup performed by packet CLI` (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/manifest.json:153-157`) and repeats the same known narrative at slice timing (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/manifest.json:120-124`).
- `slot3_reddit_batch1_packet_post_patch_dry_run` still records capture-level `cutoff_posture.status` as `known` with value `local markdown artifact state supplied for the post-patch source capture packet dry-run` (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_post_patch_dry_run/manifest.json:151-155`) and repeats the same known narrative at slice timing (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_post_patch_dry_run/manifest.json:118-122`).
- Structured validation in this review failed those two manifests on both capture-level and slice-level `PacketTiming` cutoff validation.

Why this matters:

The implementation correctly rejects new off-vocabulary known cutoff values, but two current packets still contain exactly the old narrative values that the proposal and prior review said must be migrated before ratification. This is a migration failure, not a doctrine/code exactness failure. Treating R2 as settled with those packets present would leave the Data Capture lane with a current packet corpus that contradicts the closed vocabulary it just adopted.

minimum_closure_condition:

Every current packet manifest that remains in scope must replace off-vocabulary known `cutoff_posture` narratives with a valid closed known value or an appropriate non-known status plus reason, with the displaced local-packetization narrative preserved in an allowed context field or limitation where it remains decision-relevant; `SourceCapturePacket.model_validate` must pass for both capture-level and slice-level timing.

next_authorized_action:

Owner/Data Capture lane decision: authorize a bounded migration/replay for the affected packet manifests, or explicitly mark those untracked manifests as out of scope before claiming the R2 implementation and doctrine are settled. This review does not authorize or execute that migration.

## Non-Findings

### NF-01 - Code/doctrine exactness holds for the three closed sets

Ob.9 doctrine says known cutoff values are `pre_cutoff`, `post_cutoff`, `mixed`, or `unknown` (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:272-278`), matching `CUTOFF_POSTURE_VALUES` (`orca-harness/source_capture/models.py:53`) and the `PacketTiming` validator (`orca-harness/source_capture/models.py:82-94`).

Ob.10 doctrine says known archive/history values are `archived` or `attempt_failed`, with `not_attempted` and `not_applicable` carried by status plus reason (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:290-299`), matching `ARCHIVE_HISTORY_POSTURE_VALUES` (`orca-harness/source_capture/models.py:54`) and packet/slice validators (`orca-harness/source_capture/models.py:129-143`, `orca-harness/source_capture/models.py:185-199`).

Ob.15 doctrine says known re-capture relationship values are `supersede`, `supplement`, `conflict`, or `mixed` (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:434-439`), matching `RE_CAPTURE_RELATIONSHIP_VALUES` (`orca-harness/source_capture/models.py:55`) and packet/slice validators (`orca-harness/source_capture/models.py:137-142`, `orca-harness/source_capture/models.py:193-198`).

`access_posture` remains open: the model comment says it is intentionally left open (`orca-harness/source_capture/models.py:48-52`), `SourceCaptureSlice.access_posture` and `SourceCapturePacket.access_posture` have no closed-posture validator (`orca-harness/source_capture/models.py:117-143`, `orca-harness/source_capture/models.py:160-199`), and Ob.11 remains prose rather than a closed set (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:324-338`).

### NF-02 - cutoff_posture is no longer used as source/snapshot time fallback

`_source_time` now checks only `source_edit_or_version` and `source_publication_or_event`, then returns an explicit unknown if neither is known (`orca-harness/source_capture/source_quality.py:434-446`). This closes prior AR-03 for the reviewed implementation surface.

### NF-03 - Archive Option (b) representation is coherent for new archive packets

The archive runner emits closed archive posture values: `_archive_posture` returns `archived` only when a selected snapshot body is preserved and otherwise `attempt_failed` (`orca-harness/runners/run_source_capture_archive_packet.py:273-281`); `_body_archive_posture` returns `not_applicable` when no snapshot was selected, `archived` for preserved body, and `attempt_failed` for body failure (`orca-harness/runners/run_source_capture_archive_packet.py:300-307`).

Recoverability is preserved outside the posture value. The selected snapshot metadata includes timestamp, original URL, snapshot URL, status code, MIME type, and digest (`orca-harness/runners/run_source_capture_archive_packet.py:245-254`); packet metadata records selected snapshot and body HTTP metadata (`orca-harness/runners/run_source_capture_archive_packet.py:237-244`); body failure is surfaced in packet limitations (`orca-harness/runners/run_source_capture_archive_packet.py:183-184`, `orca-harness/runners/run_source_capture_archive_packet.py:336-340`).

### NF-04 - New-write hash_basis is honest and recomputable

For new packets, the writer hashes the copied destination file and records `hash_basis="raw_stored_bytes"` (`orca-harness/source_capture/writer.py:253-267`), while `hash_file` reads raw bytes (`orca-harness/harness_utils.py:33-34`). The targeted writer test asserts both the output manifest field and recomputation against the copied file (`orca-harness/tests/unit/test_source_capture_packet.py:206-237`).

The manifest read-back script also recomputed the existing packet files from `relative_packet_path` and found the stored `sha256` values matched. Their failure is the absent `hash_basis` field and, for two manifests, off-vocabulary cutoff text.

### NF-05 - Value-vs-sufficiency boundary held

The Data Capture/Cleaning boundary says Data Capture owns acquisition, preservation, visibility, timing, cutoff/archive posture, and handoff requirements, while Judgment owns credibility, discounting, exclusion, Decision Strength, and Action Ceiling (`docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md:72-79`). Ob.9 says Capture makes cutoff posture visible but does not decide admissibility (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:280-282`), and Ob.10 says archive success is not required while sufficiency belongs downstream (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:318-319`). I found no reviewed code path that turns `archived` or `attempt_failed` into a Judgment sufficiency verdict.

### NF-06 - Targeted new-write tests are green, but not settlement proof

The six prompt-named test files that directly cover packet model/writer behavior, archive runner, direct HTTP runner, media runner, and source-quality rendering passed in this review. That is useful evidence for new writes, but it does not prove existing packet compatibility because the on-disk manifest read-back check failed.

## Not-Proven Boundaries

- Full-suite green is not proven. I ran the six review-relevant unit files named by the prompt, not the entire repository test suite.
- Current packet compatibility is not proven; it is disproven for the three manifests found under `orca-harness/reports/source_capture/**/manifest.json`.
- Browser and authenticated-browser runners were included in the runner scan because they construct packets. Their defaults are schema-safe, and bad operator-supplied closed-field values are rejected by model validation before writing, but no prompt-named test exercises those two runners.
- CLI ergonomics are not proven settled. The CLI flags for `--cutoff-posture` and `--recapture-relationship` remain open strings in multiple runners (`orca-harness/runners/run_source_capture_http_packet.py:191-196`, `orca-harness/runners/run_source_capture_media_packet.py:307-312`, `orca-harness/runners/run_source_capture_archive_packet.py:404-409`, `orca-harness/runners/run_source_capture_browser_packet.py:225-230`, `orca-harness/runners/run_source_capture_authenticated_browser_packet.py:298-303`), and `build_optional_fact` converts any supplied value into `known_fact(value)` (`orca-harness/source_capture/cli_support.py:12-35`). The schema catches invalid values before manifest write, so this is optional hardening rather than a blocking finding.
- I did not validate historical packets outside `orca-harness/reports/source_capture/**/manifest.json`, generated pytest run directories, or unrelated evidence YAML files. The prompt scoped existing packet manifests under that reports path.
- Because the worktree is dirty/untracked, this report cannot make strict readiness, acceptance, ratification, or source-of-truth settlement claims.

## Optional Hardening

- Add closed-value choices or clearer CLI help for the now-closed operator-facing fields so invalid values fail at argument parsing instead of at Pydantic model validation. This is not required to close R2 because the schema already preserves real failure visibility and prevents invalid manifests from being written.
- Add a manifest corpus read-back test or check for `orca-harness/reports/source_capture/**/manifest.json` if those reports remain in the current packet compatibility surface. This would prevent "new writer green, old packet broken" from recurring.

## Review-Use Boundary

These findings are decision input for the owner and Data Capture lane only. They are not approval, validation, ratification, mandatory remediation, patch authority, executor-ready instructions, or JSG-01 unfreeze authority. A separate owner/Data Capture decision is required before any migration, patch, acceptance, or downstream binding.
