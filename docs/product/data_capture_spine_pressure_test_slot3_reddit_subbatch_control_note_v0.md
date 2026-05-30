# Data Capture Spine Pressure-Test Slot 3 Reddit Sub-Batch Control Note v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Control note for the completed Slot 3 Reddit sub-batch captures before WSO/cross-venue Slot 3 synthesis.
use_when:
  - Checking whether the Reddit half of Slot 3 has capture-session artifacts and checker outputs.
  - Routing the next Slot 3 decision between WSO execution and explicit WSO deferral.
  - Preserving Reddit-specific capture lessons without promoting them to doctrine.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md
  - docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md
  - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
  - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - Either Reddit sub-batch capture artifact is materially amended or superseded.
  - WSO or another non-Reddit Slot 3 venue is captured and accepted into the Slot 3 evidence surface.
  - A later owner decision classifies Slot 3 as Reddit-only or changes the authorized Slot 3 venue coverage.
```

## Status

Status: `SLOT3_REDDIT_SUBBATCH_CAPTURED_WITH_VISIBLE_LIMITATIONS_V0`.

This note records the control state after completing two Reddit sub-batch
capture artifacts and checker invocations for Slot 3. It is not a full Slot 3
synthesis because Wall Street Oasis and cross-venue coverage remain unresolved.

## Source Surface

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 Slot 3 Reddit control-note pack
  edit_permission: docs-write
  target_scope:
    - docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/artifact-folders.md
    - docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md
    - docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md
```

Sources read for this note:

- `docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md`
- `docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/artifact-folders.md`

## Captured Artifacts

| Unit | Artifact | SHA256 | Capture handoff state | Checker output |
| --- | --- | --- | --- | --- |
| Reddit batch 1of2, manifest rows R01-R05 | `docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md` | `7833038440C81B6BEE30AC4AAEE7F8CBF4AFF383E0AD5269ED671F141293E770` | `re-capture_posture` | `visible_capture_limitation` |
| Reddit batch 2of2, manifest rows R06-R10 | `docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md` | `BA950FCF72AC7EB1B3C85BBEA3BEE8F398CB08D35D292EF82182102C04A2E8F5` | `categorical_handoff_to_ECR` | `visible_capture_limitation` |

Both Reddit sub-batch artifacts now carry checker outputs. Neither artifact has
an active `capture_closure_blocker`.

## Checker And Remediation Record

Batch 1 initially received `capture_closure_blocker` because the artifact
preserved paths, hashes, counts, IDs, scores, and paraphrased pointers, but did
not include enough source-language post/comment text for artifact-internal
inspection. The remediation added a bounded source-language raw observable
anchor subsection under `Raw Observable Pointers`, using only the supplied local
`readable.md` thread views for R01-R05.

After remediation, Batch 1 received `visible_capture_limitation`. The remaining
limitations are media/gallery and preview-image preservation limits, local JSON
cutoff, no live/archive continuation, pointer-only deleted rows, and limited
Reddit-visible actor context.

Batch 2 received `visible_capture_limitation` without a closure blocker. Its
visible limitations are missing per-thread original operator acquisition
receipts, pointer-only resume images for R08/R10, and mixed direct-frame /
adjacent / older / UK-DACH slice fit.

The checker prompt itself was patched during this run to avoid treating
pre-checker placeholder scaffolding inside the artifact's own checker section as
checker-token divergence. This is recorded as prompt-surface hygiene, not as
capture validation or doctrine hardening.

## Reddit-Specific Capture Lessons

- Artifact-internal checking requires bounded source-language anchors for text
  or forum sources. Provenance paths and raw-file hashes are necessary but not
  sufficient when the checker cannot open source files.
- Source-language anchors should be bounded, not full-thread restatements:
  OP title/body language plus a small number of source-visible comment or reply
  excerpts by ID and score were enough to clear the Batch 1 closure blocker.
- Media-dependent slices remain visibly limited when the local packet preserves
  metadata, preview URLs, or `i.redd.it` pointers but not local binary assets.
- Thread-level cutoff should stay local-file based unless live recapture,
  archive lookup, continuation fetch, or media retrieval is separately
  authorized.
- Checker scaffolding must not become part of the vocabulary surface being
  audited. Pre-invocation placeholders are operational scaffolding; final
  artifacts must replace them with one of the four checker tokens.

These are pressure-test observations from the Reddit sub-batch only. They are
not promoted to obligation-contract doctrine, source-family core rule, or
future tooling requirement by this note.

## Open Limitations

- Wall Street Oasis was not captured.
- Cross-venue Slot 3 synthesis has not been performed.
- Reddit media binaries were not fetched or locally preserved for image/gallery
  dependent slices.
- Live Reddit continuation, archive/cache lookup, and user-profile traversal
  were not attempted.
- The ten-thread Reddit set mixes direct target-frame evidence with adjacent
  educational-background, role-specific, UK/DACH, and counterfactual target vs.
  non-target context. That mixed-slice posture must remain visible downstream.
- This note does not classify whether Reddit-only evidence is sufficient for
  Slot 3; that is an owner/control decision still open.

## Next Decision

The next control decision is one of:

1. Run the WSO/non-Reddit Slot 3 venue capture before Slot 3 synthesis.
2. Explicitly defer WSO and classify the current Slot 3 evidence as Reddit-only
   pressure-test evidence.

Default recommendation for control integrity: run or explicitly defer WSO before
writing a full Slot 3 synthesis. Do not silently treat the completed Reddit
sub-batch as complete Slot 3 venue coverage.

## Non-Claims

This note is not validation, readiness, pressure-test discharge, full Slot 3
synthesis, WSO coverage, cross-venue synthesis, ECR design, Cleaning design,
Judgment design, runtime authorization, source-family promotion, obligation
contract hardening, buyer proof, or commercial-readiness evidence.

No direction-change propagation receipt is included because this note records
captured evidence and routing state without changing product doctrine,
architecture doctrine, workflow authority, validation philosophy, review
authority, output authority, or lifecycle boundaries.
