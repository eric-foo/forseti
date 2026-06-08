# Adversarial Code Review - Source Capture `packet_assembly` STEP-02

```yaml
retrieval_header_version: 1
artifact_role: Review report
review_prompt: docs/prompts/reviews/source_capture_packet_assembly_step02_adversarial_code_review_prompt_v0.md
review_lane: adversarial code review
reviewed_targets:
  - orca-harness/source_capture/packet_assembly.py
  - orca-harness/runners/run_source_capture_http_packet.py
  - orca-harness/docs/adapter_author_contract.md
  - orca-harness/source_capture/writer.py
  - orca-harness/source_capture/models.py
  - orca-harness/runners/run_source_capture_media_packet.py
authority_boundary: advisory_findings_only
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_assembly_step02_adversarial_code_review_v0.md
  recommendation: patch_before_acceptance
  summary: "The HTTP port appears source-preserving, but the helper should not propagate until posture-honesty and credentialed-adapter secrecy boundaries are tightened."
  findings_count: 3
  blocking_findings:
    - AR-01: Posture-honesty validation is weaker than the documented propagation invariant
    - AR-02: Credentialed adapter secrecy remains convention-only at the shared last mile
  advisory_findings:
    - AR-03: Generic staging-collision text loses adapter-specific routing detail
  prior_findings_remediated: []
  next_action: "Authorize a narrow patch to align the helper/contract/tests before porting media or Reddit."
```

## Source Context

SOURCE_CONTEXT_READY for repo-visible advisory review.

Source-read ledger:

- `AGENTS.md` supplied in prompt context: Orca overlay is required; review reports require durable-write verification before reporting.
- `.agents/workflow-overlay/README.md`: Orca overlay entrypoint and binding rule.
- `.agents/workflow-overlay/review-lanes.md`: read-only review boundary; findings are decision input, not patch authority.
- `.agents/workflow-overlay/prompt-orchestration.md`: `review-report` output mode writes under `docs/review-outputs/` and returns compact summary after durable write.
- `.agents/workflow-overlay/communication-style.md`: `review_summary` YAML shape.
- `.agents/workflow-overlay/artifact-roles.md` and `artifact-folders.md`: review prompt/report roles and destination are bound.
- `.agents/workflow-overlay/validation-gates.md` and `source-of-truth.md`: strict validation/readiness claims remain blocked by dirty controlling sources unless explicitly accepted.
- `docs/prompts/reviews/source_capture_packet_assembly_step02_adversarial_code_review_prompt_v0.md`: commission, target files, criteria, and report destination.
- `orca-harness/source_capture/packet_assembly.py`: new shared helper under review.
- `orca-harness/runners/run_source_capture_http_packet.py`: HTTP runner port under review.
- `orca-harness/docs/adapter_author_contract.md`: contract and generalization authority named by the prompt.
- `orca-harness/source_capture/writer.py`: packet writer and preserved-file ID assignment.
- `orca-harness/source_capture/models.py`: `VisibleFact`, slice, packet, and preserved-file-reference validation.
- `orca-harness/runners/run_source_capture_media_packet.py`: unported generalization target.
- `orca-harness/source_capture/adapters/direct_http.py`, `media_asset.py`, `auth_state.py`: metadata, media composition, and credential-indirection references.
- `orca-harness/tests/unit/test_source_capture_direct_http.py` and `test_source_capture_media_asset.py`: source-visible behavior assertions for HTTP and media runners.
- `orca-harness/docs/source_capture_agent_runbook.md`: downstream reporting boundary for empty limitations plus visible postures.
- `git status --short --branch`: worktree is dirty; reviewed helper, contract doc, and prompt are untracked or modified. Findings are advisory, not validation, readiness, or acceptance.

Deep-thinking discipline was applied through `workflow-deep-thinking` before findings: the decisive question is not whether STEP-02 removes duplicated staging code, but whether the extracted "last mile" can be propagated without weakening per-slice honesty, file-reference integrity, or credential secrecy.

No tests were run for this review. The prompt supplied prior test evidence, but this report does not validate it or claim the test suite passes.

## Scope And Boundaries

Review scope:

- Helper shape in `packet_assembly.py`.
- HTTP runner behavior preservation from source diff and current code.
- Media generalization fit.
- Credentialed Reddit generalization risk.
- Contract/doc alignment where it directly controls implementation expectations.

Excluded scope:

- No source patches.
- No patch queue entries.
- No fixture admission, product proof, runtime readiness, or validation pass/fail claim.
- No live network, credential, or Reddit implementation review.

Patch-queue routing is not authorized. Each finding includes a closure condition and next authorized action only.

## Phase 1 - Correctness Findings

### AR-01 - Posture-honesty validation is weaker than the documented propagation invariant

Reviewed target: `orca-harness/source_capture/packet_assembly.py`

Location anchor: `validate_capture_posture_honesty`, lines 26-45; helper call site lines 80-83.

Evidence:

- `adapter_author_contract.md` states the invariant as: if a slice carries a limitation "or a non-`known` posture", capture-level `limitations` must surface it (lines 86-89).
- `models.py` confirms postures are `VisibleFact` with statuses `known`, `unknown_with_reason`, `not_attempted`, and `not_applicable` (lines 25-44), and `SourceCaptureSlice` carries access/archive/media/re-capture postures plus `limitations` (lines 64-74).
- The helper only computes `slice_limited = any(source_slice.limitations for source_slice in source_slices)` and rejects only when that is true and capture-level limitations are empty (lines 40-45).
- `writer.py` simply copies `limitations` into the packet (lines 87-88, 152-155). The final packet validator checks preserved-file references only (models lines 116-128); it does not enforce posture honesty.

Requirement strained:

The prompt asks whether the helper is a sound, behavior-preserving contract that will generalize without hiding per-slice honesty. As written, it does not enforce the contract's own non-`known` posture branch.

Impact:

A future runner can emit a slice with `unknown_with_reason` or `not_attempted` on a material axis, leave `source_slice.limitations=[]`, pass `limitations=[]`, and still get a packet that looks clean at the capture-level limitations list. That is exactly the "clean rollup hides a failed/limited slice" failure the helper was supposed to prevent before propagation.

Important nuance:

A naive rule of "any non-`known` slice posture requires packet limitations" is too strong for existing direct HTTP behavior. The HTTP runner intentionally has `archive_posture = not_attempted(...)`, `media_posture = not_attempted(...)`, and `recapture_posture = not_applicable(...)` (HTTP lines 104-110), and passes those same postures at capture level (HTTP lines 147-150). The runbook also says an exit-code-0 packet with empty limitations must not be collapsed into clean capture because visible postures may still carry caveats (runbook lines 531-533). The fix should not blindly turn every ordinary not-attempted axis into a packet limitation.

Minimum closure condition:

The helper and contract must agree on one enforceable rule. Either narrow the contract to "slice limitation must surface in packet limitations" and rely on packet-level postures for known non-limitation axes, or extend validation to compare slice postures against the supplied capture-level rollup and require packet limitations only for non-`known` slice postures that are not visibly represented by the capture-level posture/limitations. Add a red-green test where a slice non-`known` posture is hidden by an empty capture-level rollup and the helper rejects it, plus a test showing the direct HTTP same-posture case remains valid.

Red-green proof status:

Needed. A testable remediation claim exists, but this review did not run or author tests.

Next authorized action:

Owner/CA patch authorization for a narrow helper + contract + unit-test patch. This review does not authorize the patch.

### AR-02 - Credentialed adapter secrecy remains convention-only at the shared last mile

Reviewed target: `orca-harness/source_capture/packet_assembly.py` and `orca-harness/docs/adapter_author_contract.md`

Location anchor: helper forwarding/staging lines 56-93; contract no-secrets invariant lines 79-81; writer packet/raw persistence lines 132-163 and 254-268.

Evidence:

- The contract requires: credentials/tokens/cookies/storage-state live in ignored local config, and packets record only label/mode/loaded-boolean (contract lines 79-81).
- The helper says `writer_kwargs` are forwarded verbatim to `write_local_source_capture_packet` (lines 56-62) and then writes every staged artifact byte before calling the writer (lines 85-93).
- The writer persists supplied metadata fields into `SourceCapturePacket` (lines 132-155) and copies every input file to `raw/` (lines 254-268).
- The existing direct HTTP adapter metadata is intentionally limited to response metadata such as URL, status, content type, date, ETag, timestamp, timeout, and byte count (direct_http lines 154-160 and following), and tests assert `Set-Cookie` is absent for direct HTTP and media metadata (direct HTTP test lines 230-234; media test lines 154-158).
- `auth_state.py` provides a label/path/mode-validation pattern for browser credentials (for example lines 26-31 and 50-75), but `stage_and_write_packet` does not require or verify that pattern for future credentialed runners.

Requirement strained:

The commission specifically asks whether the helper/contract is safe for a coming credentialed Reddit adapter "without hiding per-slice honesty or leaking secrets." The current helper is a staging/writer convenience, not a secrecy boundary.

Impact:

For HTTP and media today, source-visible metadata tests reduce the immediate risk. For Reddit, a runner could accidentally stage request headers, Authorization values, cookies, OAuth refresh/access tokens, or credentialed raw API metadata into `staged_artifacts`, or pass secret-bearing values through `writer_kwargs`. The shared helper would faithfully persist them to `raw/`, manifest fields, or receipt text. Once the helper is treated as the common last mile, this becomes a propagation risk because future adapter authors may infer that using the helper is enough to satisfy the no-secrets invariant.

Minimum closure condition:

Before credentialed Reddit uses this helper, bind a concrete secrecy boundary at the runner/helper contract. Acceptable closure could be an allowlisted public metadata schema for staged metadata plus tests that secret-like request/auth fields are excluded, or a required credential-indirection shape that passes only labels/modes/loaded booleans into packet fields. If the project deliberately keeps this as convention-only, the contract must say the helper does not structurally enforce no-secrets and must name the adapter-level tests required before credentialed use.

Red-green proof status:

Needed for credentialed adapter propagation. A non-executable policy sentence is insufficient; at least one test should prove a credential-like field is not persisted by the runner path that will use the helper.

Next authorized action:

Owner/CA decision on whether no-secrets enforcement belongs in the helper boundary, the credentialed runner boundary, or both. Do not port Reddit through this helper until that decision is made.

## Non-Findings Checked

File-id coupling:

No concrete helper defect found when a runner uses `staged_file_id_map` from the exact `staged_artifacts` passed to `stage_and_write_packet`. The helper builds `staged_paths` from the same ordered sequence (packet_assembly lines 71, 86-92), and the writer assigns `file_01`, `file_02`, etc. in `input_files` order (writer lines 254-262). The duplicate filename guard is sufficient for the current filename-keyed map (packet_assembly lines 18-22).

Media generalization:

The media runner's final `packet_slices.sort(key=lambda item: item.slice_id)` is not by itself a file-ID failure. The writer validates that each preserved file is referenced by some slice, not that slice order matches raw-file order (models lines 116-128), and current media tests assert multi-asset file references remain correct (`file_03`, `file_04` for asset 02; test lines 176-182). The helper can fit media if the runner creates `staged_artifacts` in raw-file order and uses the map for each success before sorting slices. Failure slices with `preserved_file_ids=[]` also remain compatible because the writer only requires preserved files to be referenced, not every slice to reference a file.

HTTP behavior preservation:

From source diff and current code, the port preserves the important manifest shape modulo expected dynamic IDs/timestamps. The old hard-coded `["file_01", "file_02"]` became map lookups for the same two artifacts (HTTP lines 84-91, 126-129). The shared `archive_posture`, `media_posture`, and `recapture_posture` objects serialize the same values as separate-but-equal constructor calls because `VisibleFact` stores status/value/reason fields (models lines 32-44). This is source review only, not byte-level validation.

## Phase 2 - Friction Findings

### AR-03 - Generic staging-collision text loses adapter-specific routing detail

Reviewed target: `orca-harness/source_capture/packet_assembly.py` and `orca-harness/runners/run_source_capture_http_packet.py`

Location anchor: helper collision guard lines 73-78; HTTP diff replacing the direct-HTTP-specific message.

Evidence:

- The previous HTTP runner message named "direct HTTP staging files"; the port now emits the helper's generic "source capture staging files already exist in the output parent; clear them before rerunning" (packet_assembly lines 73-78).
- Exit-code mapping remains preserved: `ValueError` still maps to status 2 in the HTTP runner (HTTP lines 252-253).

Impact:

This is not a behavior-preservation blocker unless downstream tests or operator docs match the exact stderr text. It does reduce operator routing detail in multi-runner scratch directories, especially once media and Reddit also use the helper and collide in the same parent.

Minimum closure condition:

Either accept the generic wording as the shared helper contract, or add a non-secret `staging_context`/runner label to the helper error so the message stays adapter-specific without duplicating cleanup code.

Red-green proof status:

Optional. Only needed if exact error text is part of the runner contract.

Next authorized action:

Treat as advisory friction during the same narrow patch if the owner wants operator-specific diagnostics preserved.

## Strict-Only Blockers And Not-Proven Boundaries

- Strict validation/test pass is not proven. No tests were run in this review.
- Formal acceptance/readiness is not proven. The worktree is dirty and key reviewed files are untracked or modified.
- Patch queue is not authorized. Remediation directions above are closure conditions, not executor-ready instructions.
- Secret safety for a future Reddit adapter is not proven by HTTP/media tests.
- Byte-identical manifest preservation is not proven by this review; only source-level preservation was inspected.

## Recommendation

Patch before acceptance for propagation. The HTTP port itself looks like a reasonable first use of the helper, and the file-ID map is compatible with the media runner's real shape if used carefully. But the helper should not become the common last mile for media + credentialed Reddit until AR-01 and AR-02 are resolved or explicitly downgraded by the owner with the risk accepted.

Review-use boundary: these findings are decision input only. They are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized.
