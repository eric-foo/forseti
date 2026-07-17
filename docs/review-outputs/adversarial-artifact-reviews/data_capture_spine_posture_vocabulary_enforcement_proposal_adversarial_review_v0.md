```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the Data Capture posture-vocabulary enforcement proposal.
use_when:
  - Inspecting proposal findings before owner adjudication or revision.
  - Tracing the enforcement proposal to its adversarial review evidence.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md
  recommendation: patch_before_acceptance
  summary: "The proposal is directionally right on value-vs-sufficiency, but it overclaims JSG-01 completeness and misses implemented-code and migration collisions that must be patched before acceptance or ratification."
  findings_count: 5
  blocking_findings:
    - AR-01: JSG-01 foundation claim still requires downstream source-visibility derivation.
    - AR-02: Existing packets and tests carry off-vocabulary known cutoff values.
    - AR-03: source_quality.py treats cutoff_posture as a source/snapshot time fallback.
    - AR-04: hash_basis as an unconstrained string is not enough to close verifiability.
  advisory_findings:
    - AR-05: Ob.10 status-vs-value split is plausible but not yet exact contract/schema language.
  prior_findings_remediated: []
  next_action: "Patch the proposal before the Data Capture lane treats it as acceptance-ready; keep JSG-01 frozen and treat this report as advisory decision input only."
```

# Data Capture Spine Posture Vocabulary Enforcement Proposal - Adversarial Artifact Review v0

## Source Readiness

SOURCE_CONTEXT_READY.

Target hash was confirmed before review:

- `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
- observed SHA256: `2E5D05B8F8366711F4A749B68664E0034BED7C8460B629EF1BA881AED04D5FA5`
- prompt-pinned SHA256: `2E5D05B8F8366711F4A749B68664E0034BED7C8460B629EF1BA881AED04D5FA5`

Review mode: read-only adversarial artifact review, durable `review-report`.
`workflow-deep-thinking` and `workflow-adversarial-artifact-review` were reference-loaded before source loading and applied only after `SOURCE_CONTEXT_READY`.

Strict claims are blocked. The worktree is dirty and several controlling sources are modified or untracked, including `AGENTS.md`, overlay files, the target proposal, `docs/product/jsg01_source_side_receipt_translator_v0.md`, `orca-harness/source_capture/packet_assembly.py`, `orca-harness/tests/unit/test_packet_assembly.py`, and `orca-harness/reports/source_capture/`. This report is advisory only: no PASS, readiness, validation, ratification, patch queue, or implementation authorization.

## Findings

### AR-01 - JSG-01 foundation claim still requires downstream source-visibility derivation

- severity: major
- phase: correctness
- seam: Completeness for the consumer / value-vs-sufficiency boundary
- reviewed target: `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
- location anchor: "Relationship to JSG-01 (why this is the foundation)"
- patch_queue_routing_authorized: no

Evidence:

- The proposal says that once it lands, "JSG-01 source-side reads the closed values directly -- no per-reader interpretation" (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:94-96`).
- The same proposal leaves `access_posture` free-text because Ob.11 is prose, not a closed set (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:75-77`).
- JSG-01's own translator defines `source_visibility_posture` as a closed field with values such as `archive_corroborated`, `archive_only`, `archive_diverged`, `current_capture_only`, `archive_post_cutoff_only`, `attempt_failed`, `not_attempted`, and `not_applicable` (`docs/product/jsg01_source_side_receipt_translator_v0.md:214-232`).
- JSG-01 also says no single harness field carries that posture; it must be mapped from archive-attempt record, acquisition receipt capture scope, and re-capture relationship (`docs/product/jsg01_source_side_receipt_translator_v0.md:260-262`).
- The boundary doc assigns source visibility, timing, cutoff/archive posture, and preservation to Data Capture, while Judgment owns Signal Integrity, uncertainty, counterevidence, discounting, exclusion, Decision Strength, and Action Ceiling (`docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md:72-77`).

Requirement strained:

The proposal correctly avoids putting materiality verdicts such as `archive_corroborated` / `archive_diverged` into Capture, but it then overstates what JSG-01 can consume directly. Closing `cutoff_posture`, `archive_history_posture`, and `re_capture_relationship` reduces interpretation, but it does not by itself produce JSG-01's `source_visibility_posture` or eliminate per-reader mapping.

Impact:

If accepted as written, the Data Capture lane could believe this is sufficient for JSG-01 source-side binding, when it is only a partial upstream cleanup. JSG-01 still needs a bounded derivation rule or an explicit residual naming which free-text/source records remain outside the proposed closure.

minimum_closure_condition:

The proposal must downgrade the JSG-01 claim from "reads the closed values directly -- no per-reader interpretation" to a narrower claim: these closures are upstream inputs, while `source_visibility_posture` still needs a Data Capture / ECR-owned derivation or residual decision. It must name which source-side facts remain free-text or multi-field inputs.

next_authorized_action:

Owner or Data Capture lane may patch the proposal text and rerun or accept this finding as advisory input. This review does not authorize the patch.

verification evidence needed for future executor:

A future review should re-read the proposal's JSG-01 relationship section and verify it no longer claims direct completeness for SP-6. Red-green proof is not applicable to this non-executable artifact finding.

### AR-02 - Existing packets and tests carry off-vocabulary known cutoff values

- severity: major
- phase: correctness
- seam: Migration landmines / no invention / validation confidence
- reviewed target: `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
- location anchor: "Known seams for the review / DC lane (do not solve here)" and "Proposed changes"
- patch_queue_routing_authorized: no

Evidence:

- The proposal would allow `PacketTiming.cutoff_posture` known values only in `{pre_cutoff, post_cutoff, mixed, unknown}` (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:52`).
- The proposal acknowledges that existing packets/tests with off-vocabulary free text would fail validation, then punts migration to the implementation lane (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:87-90`).
- A unit test creates `cutoff_posture=known_fact("local cutoff posture")`, which is outside the proposed set (`orca-harness/tests/unit/test_source_capture_packet.py:324-330`).
- Existing packet `slot3_reddit_batch1_packet_dry_run_2` carries capture-level `cutoff_posture.status = known` and value `local JSON/file state supplied...`, outside the proposed set (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/manifest.json:153-156`).
- Existing packet `slot3_reddit_batch1_packet_post_patch_dry_run` carries capture-level `cutoff_posture.status = known` and value `local markdown artifact state supplied...`, outside the proposed set (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_post_patch_dry_run/manifest.json:151-154`).

Requirement violated or unsupported:

The proposal is honest that migration exists, but for an acceptance/ratification foundation this is too weak. The required read-pack asked whether existing packets/tests would break. They would, and the proposal does not bind the minimum migration decision needed before ratification.

Impact:

Closing the schema without an accepted migration stance would break current tests and existing packet manifests. Worse, the current packet values are not random bad data; they encode local-packetization limitations that would need a mapped representation, likely as `unknown` value, `unknown_with_reason` status, limitations, or a separate capture-context field.

minimum_closure_condition:

Before acceptance or ratification, the proposal must explicitly name the observed off-vocabulary current values and require a migration/compatibility decision for tests and existing manifests. It does not need to implement the migration, but it must stop treating migration as a generic later code concern.

next_authorized_action:

Data Capture lane may patch the proposal to bind migration as a pre-ratification condition. This review does not authorize code or manifest edits.

verification evidence needed for future executor:

Future executor evidence should include a source-visible migration policy and a recheck of the same tests/manifests. Same-check red-green proof may apply only if a later implementation lane changes schema/tests; it is not applicable to this report.

### AR-03 - `source_quality.py` treats `cutoff_posture` as a source/snapshot time fallback

- severity: major
- phase: correctness
- seam: Implemented-code collision / downstream executability
- reviewed target: `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
- location anchor: "Problem" and "Proposed changes"
- patch_queue_routing_authorized: no

Evidence:

- The proposal frames the issue as free-text posture values being interpreted by downstream readers (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:32-41`).
- `source_quality.py` writes `source_or_snapshot_time` using `_source_time(generic_body_slice)` (`orca-harness/source_capture/source_quality.py:183-195`).
- `_source_time` falls back from `source_edit_or_version` and `source_publication_or_event` to `source_slice.timing.cutoff_posture`, returning the first known value (`orca-harness/source_capture/source_quality.py:434-442`).
- Under the proposal, `cutoff_posture` known values would become enum-like posture values such as `pre_cutoff` or `mixed`, not timestamp or source/snapshot time text (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:52`).

Requirement violated or unsupported:

The proposal's implementation surface is incomplete. It names `models.py` and schema enforcement, but a required implemented consumer currently treats `cutoff_posture` as a time fallback. Closing that value vocabulary changes report content semantics unless `source_quality.py` is amended or the proposal explicitly scopes the collision.

Impact:

After the proposed schema change, source-quality output could report `source_or_snapshot_time: pre_cutoff`, which is a posture, not a time. That is a subtle false-clarity path: the value would be valid under the new enum, but invalid as the source-quality field it flows into.

minimum_closure_condition:

The proposal must add `source_quality.py` to the required impact surface and state that source/snapshot time must not be populated from the closed cutoff posture enum. It may leave implementation to the authorized lane, but the collision must be named before acceptance.

next_authorized_action:

Data Capture lane may patch the proposal's implementation-impact section and later authorize a bounded implementation review. This review does not authorize code edits.

verification evidence needed for future executor:

A future implementation review should verify that `source_or_snapshot_time` is sourced from timing fields or explicit unknown status, not from closed posture values. Same-check red-green proof could apply in a later code lane; not applicable here.

### AR-04 - `hash_basis: str` is necessary but not sufficient to close verifiability

- severity: major
- phase: correctness
- seam: hash_basis sufficiency / inspectability
- reviewed target: `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
- location anchor: "Proposed changes"
- patch_queue_routing_authorized: no

Evidence:

- The proposal says to add `PreservedFile.hash_basis: str` as "what the hash covers" and marks it as required when `sha256` is present (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:55`).
- Current `PreservedFile` already stores `relative_packet_path`, `sha256`, and `size_bytes`, but no basis field (`orca-harness/source_capture/models.py:56-61`).
- The writer computes `sha256` over the copied destination path and records the relative packet path (`orca-harness/source_capture/writer.py:259-265`).
- Harness `EvidenceUnit` carries both `hash` and `hash_basis` as strings (`orca-harness/schemas/case_models.py:53-62`).
- JSG-01 requires a non-placeholder source-byte hash plus a recorded recomputation-coverage basis, and explicitly says verifiability requires knowing what the hash covers, not just that a hash-shaped string exists (`docs/product/jsg01_source_side_receipt_translator_v0.md:138-149`).

Requirement strained:

Adding `hash_basis` is the right direction, but an unconstrained string alone does not close AR-03. It can still be vague, stale, inconsistent with the actual `relative_packet_path`, or disconnected from the bytes the writer hashed.

Impact:

If the Data Capture lane treats "add `hash_basis: str`" as sufficient, SP-2 can still receive a field that looks present while failing recomputability. That recreates the exact "hash-shaped string" problem under a different field name.

minimum_closure_condition:

The proposal must state the semantic contract for `hash_basis`: it must identify the recomputation basis in relation to preserved bytes or an owner-bound acquisition receipt, not merely hold arbitrary prose. The minimum acceptable end state is a source-visible basis that lets a reviewer know what bytes or receipt coverage the hash represents.

next_authorized_action:

Owner or Data Capture lane may patch the proposal to strengthen the basis contract. This review does not authorize schema edits.

verification evidence needed for future executor:

Future review should inspect the amended proposal and any schema tests for basis semantics. Same-check red-green proof may apply in a later implementation lane; not applicable to this artifact review.

### AR-05 - Ob.10 status-vs-value split is plausible but not yet exact contract/schema language

- severity: minor
- phase: friction
- seam: Status-vs-value reconciliation / exact vocabulary match
- reviewed target: `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
- location anchor: "Proposed changes" and "Known seams"
- patch_queue_routing_authorized: no

Evidence:

- Ob.10 says capture-level archive/history posture may be recorded as one of `archived`, `attempt_failed`, `not_attempted`, and `not_applicable` (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:276-285`).
- The proposal would enforce known archive values only as `{archived, attempt_failed}` and carry `not_attempted` / `not_applicable` through `VisibleFactStatus` instead of value (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:53`).
- The current model has `VisibleFactStatus.NOT_ATTEMPTED` and `VisibleFactStatus.NOT_APPLICABLE`, and non-known facts require a reason (`orca-harness/source_capture/models.py:25-45`).
- `packet_assembly.py` already treats `not_attempted` and `not_applicable` as honest scope statements, not limitations (`orca-harness/source_capture/packet_assembly.py:47-53`).
- The proposal itself flags this as a seam for Data Capture confirmation (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:83-86`).

Requirement strained:

The split is probably the cleanest representation in the current `VisibleFact` model, but the proposal simultaneously says it "does not invent vocabulary" and asks the obligation contract to state the vocabularies as closed/enforced. Without explicit contract/schema wording, a reader can reasonably think Ob.10 has a four-value closed value enum, while implementation would enforce a two-value known-value enum plus two statuses.

Impact:

This is less severe than the migration and consumer-completeness issues because the proposal flags the seam. But leaving it as an implicit reconciliation will cause future reviews to argue about exactness rather than substance.

minimum_closure_condition:

The proposal must state that Ob.10's closed posture is represented as a union of `VisibleFact.status` and `VisibleFact.value`: `known/archived`, `known/attempt_failed`, `not_attempted/<reason>`, and `not_applicable/<reason>`. If the Data Capture lane rejects that representation, it must bind a different one before ratification.

next_authorized_action:

Owner or Data Capture lane may accept this as a wording patch target. This review does not authorize the patch.

verification evidence needed for future executor:

Future review should check the proposal and any contract amendment for an explicit status/value representation. Red-green proof is not applicable to this artifact finding.

## Non-Findings

- Value-vs-sufficiency boundary mostly holds. The proposal correctly says Capture should record posture values and leave gate-clearing sufficiency to JSG-01 / owner judgment (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:58-66`), matching Ob.9's rule that Capture makes cutoff visible but does not decide admissibility (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:260-274`) and Ob.10's rule that visible archive posture is required while sufficiency belongs downstream (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:299-305`).
- No materiality enum was added to Capture. The proposal explicitly rejects `corroborated` / `diverged` as capture values (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:67-71`), which is correct because JSG-01's `archive_diverged` depends on material divergence and says that is a downstream Judgment call (`docs/product/jsg01_source_side_receipt_translator_v0.md:220-246`).
- Leaving `access_posture` open is correct for this proposal. Ob.11 gives prose obligations, not a closed vocabulary (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:310-324`), and the proposal correctly flags that a separate capture-lane vocabulary decision would be needed (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:73-79`).
- Ob.15 inclusion of `mixed` is defensible. The contract says later capture may supersede, supplement, or conflict and must preserve mixed relationships rather than forcing one global label (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:412-430`), and the proposal includes `mixed` for `re_capture_relationship` (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:54`).
- Lane discipline holds. The proposal states it authorizes nothing and routes execution, ratification, direction-change propagation, and code/migration review to the Data Capture / capture-build lane (`docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:26-28`, `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md:100-106`).

## Not-Proven Boundaries

- Cross-family dispatch is not certified by this report. The prompt states the author was Claude and this run occurred in the current Codex thread, but the report does not independently prove operator routing.
- Schema safety beyond the read-pack is not proven. I read the required implemented code, tests, and three existing manifests under `orca-harness/reports/source_capture/**/manifest.json`; I did not prove there are no other packet-like artifacts elsewhere.
- Validation was not run. The review was read-only and the target proposal is not an implementation patch.
- Acceptance, readiness, ratification, JSG-01 unfreeze, direction-change propagation, and source-of-truth status are not proven because controlling sources are dirty/untracked and this review is advisory.
- No patch queue is emitted. Review findings are not executor-ready instructions.

## Source-Read Ledger

| Source | Why read | Status observed |
| --- | --- | --- |
| `AGENTS.md` | Repository instructions and Orca boundary | modified |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | modified |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial review lane and output rules | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | `review-report`, source-gated method contract | modified |
| `.agents/workflow-overlay/source-loading.md` | Source readiness and dirty-source handling | modified |
| `.agents/workflow-overlay/communication-style.md` | `review_summary` shape | modified |
| `workflow-deep-thinking` skill | Method reference loaded before source analysis | external reusable mechanics, not Orca authority |
| `workflow-adversarial-artifact-review` skill | Method reference loaded before source analysis | external reusable mechanics, not Orca authority |
| `docs/prompts/reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_prompt_v0.md` | Commission and output contract | untracked |
| `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` | Target artifact | untracked; hash matched prompt |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Ob.9/Ob.10/Ob.11/Ob.15 vocabulary authority | not listed dirty in targeted status |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Capture/Judgment boundary | modified |
| `docs/product/jsg01_source_side_receipt_translator_v0.md` | Consumer and source-side field needs | untracked |
| `orca-harness/source_capture/models.py` | Implemented packet model | not listed dirty in targeted status |
| `orca-harness/source_capture/writer.py` | Packet writing and hash computation | not listed dirty in targeted status |
| `orca-harness/source_capture/source_quality.py` | Implemented downstream consumer | modified |
| `orca-harness/source_capture/packet_assembly.py` | Current posture honesty semantics | untracked |
| `orca-harness/tests/unit/test_source_capture_packet.py` | Existing tests and fixtures | not listed dirty in targeted status |
| `orca-harness/tests/unit/test_packet_assembly.py` | Existing posture-honesty tests | untracked |
| `orca-harness/reports/source_capture/**/manifest.json` | Existing packet migration reality | untracked directory |
| `orca-harness/schemas/case_models.py` | Harness contrast for `EvidenceUnit.hash_basis` | not listed dirty in targeted status |

## Review-Use Boundary

These findings are decision input for the owner and Data Capture lane only. They are not approval, validation, ratification, mandatory remediation, executor-ready patch authority, schema execution, or permission to unfreeze JSG-01.
