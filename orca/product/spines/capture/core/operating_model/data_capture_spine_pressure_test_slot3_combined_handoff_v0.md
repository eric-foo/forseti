# Data Capture Spine Pressure-Test Slot 3 Combined Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Data Capture pressure-test combined handoff artifact
scope: Combined Slot 3 Reddit + WSO Data Capture posture and final capture-owned handoff-state decision.
use_when:
  - Checking the source inputs, per-venue capture posture, and final Slot 3 combined handoff-state decision.
  - Preserving Reddit and WSO venue-specific limitations before ECR, Cleaning, Judgment, or pressure-test evidence synthesis.
  - Avoiding drift from Data Capture into source completion, ECR schema, Cleaning, Judgment, or runtime/source-system work.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_execution_authorization_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - A later owner decision rejects or supersedes the Slot 3 combined handoff scope.
  - Either Reddit sub-batch capture artifact is materially amended or superseded.
  - The WSO bounded source-language anchor artifact is materially amended or superseded.
  - The accepted intake-surface target, commissioning plan, or obligation contract is materially amended before this handoff is completed.
```

## Status

Status: `COMBINED_HANDOFF_STATE_DECIDED_CATEGORICAL_HANDOFF_TO_ECR_V0`.

This artifact has been rewritten against the current Reddit and WSO Slot 3
capture surfaces plus the 2026-06-01 targeted recapture packet and now sets
the combined Slot 3 capture-owned handoff state. It records an artifact-hygiene
validation pass. It does not claim Slot 3 pressure-test completion, Data
Capture validation, source completeness, or downstream readiness.

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Slot 3 combined Reddit+WSO handoff pack
  edit_permission: docs-write for combined handoff artifact through final handoff-state decision
  target_scope: docs/product/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md
    - docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md
    - docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md
    - docs/product/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md
```

## Source Surface

Primary current inputs:

| Input | Path | SHA256 | Current posture |
| --- | --- | --- | --- |
| Reddit batch 1of2 | `docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_1of2_reddit_financialcareers_threads_batch_1of2_capture_session_v0.md` | `7C284C51909F496B7715052BAF73B49DF89BE947A05F295DC303F8E05605D8FC` | `categorical_handoff_to_ECR`; checker output `visible_capture_limitation`. |
| Reddit batch 2of2 | `docs/product/data_capture_spine_pressure_test_slot_3_reddit_batch_2of2_reddit_financialcareers_threads_batch_2of2_capture_session_v0.md` | `576A6F5FE0F59CB9503C946EF64BB62688F782FEA4700C1BA5036610BF7B8C96` | `categorical_handoff_to_ECR`; checker output `visible_capture_limitation`. |
| Reddit control note | `docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md` | `1BBC784DF6A8DE049DF2F2EA66766AFBB0AB07E5AE741B8F7EF2B2102A1FED1C` | Reddit captured with visible limitations; WSO now no longer deferred. |
| WSO bounded visible-envelope pass | `docs/product/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md` | `28404EF3ACBF9F47DCCBC35E9D33300A28B47D7108725F675BC7620041F45162` | `categorical_handoff_to_ECR`; checker output `visible_capture_limitation`. |
| 2026-06-01 Slot 3 recapture packet | `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_recapture_2026_06_01/slot3_recapture_step_01_05_receipt.md` | `CB5D3A1A4AF088E4F33B0CE4D855AB65F35E671F2922B05ABA93947BA2588E01` | Supplemental packet: 10 Reddit media files preserved; 7 WSO visible envelopes captured; archive availability posture recorded. |

Controlling execution and obligation sources:

- `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`
- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`

The previous untracked combined handoff draft referenced a stale single Reddit
capture artifact and old obligation vocabulary. It is superseded by this
rewrite.

## Decision Frame

- Decision question: Can Data Capture preserve Slot 3 non-target US-domestic
  resume-driven interview-getting pain across Reddit and WSO as a combined
  source posture, with venue limitations visible, before any ECR receipt,
  Cleaning, Judgment, or synthesis?
- Owner or owner-context: Orca owner / Chief Architect pressure-testing the
  Data Capture Spine and Mechanical Source Projection intake boundary.
- Consequence: The final handoff-state decision will determine whether Slot 3
  can proceed as a captured mixed-forum venue surface, or whether limitations
  require recapture or owner review first.
- Allowed decision verbs: `categorical_handoff_to_ECR`, `visible_stop`,
  `visible_blocker`, `rerun`, `re-capture_posture`, or later owner-authorized
  pressure-test patch planning.
- Cutoff posture: Authorized Slot 3 cutoff is Q2 2026. Reddit uses the local
  JSON file state supplied on 2026-05-29. WSO uses the public-page posture
  visible during the bounded source-language anchor pass.
- Downstream-use intent: Data Capture handoff only. This artifact does not rank
  pains, classify credibility, decide downstream use, define ECR fields, perform
  Cleaning, or synthesize customer meaning.

## Source Boundary

- Reddit in scope:
  - Ten operator-supplied local `r/FinancialCareers` thread JSON slices.
  - Existing Reddit Mechanical Source Projection working views.
  - Reddit readable thread views used for bounded source-language anchors in
    batch 1.
  - Targeted 2026-06-01 Reddit media files and archive availability posture for
    `R01`, `R03`, `R08`, and `R10`.
- WSO in scope:
  - Seven public WSO URL slices with bounded source-language anchors.
  - Supplemental visible HTML, text excerpts, screenshots, and archive
    availability posture for the same seven WSO URL slices.
  - Prior WSO discovery inventory as source-candidate context.
- Boundary compliance:
  - Reddit inspection stayed inside owner-supplied local public-thread files.
  - Reddit targeted media preservation used ordinary URL fetches for public
    `preview.redd.it` and `i.redd.it` assets.
  - WSO inspection used public browser/web inspection and bounded visible-page
    envelope capture only.
  - Archive posture used Wayback availability metadata only; archive bodies were
    not retrieved.
  - No login, email unlock, social unlock, paid access, private access,
    anti-detect method, proxy, source-system build, scraper, API, ECR schema,
    Cleaning transformation, or Judgment conclusion was used.
- Observed but not used:
  - Reddit live continuation, user-profile traversal, and archive body
    retrieval.
  - WSO hidden/comment-unlocked material, full comment graph retrieval, archive
    body retrieval, and account-created access.

## Capture Mode

- Reddit batch 1 mode: agent-assisted local file inspection over
  owner-supplied raw JSON plus bounded source-language anchors from local
  readable thread views.
- Reddit batch 2 mode: mixed human-led local file inspection plus
  agent-assisted local-file inspection, using owner-supplied raw JSON and
  existing Mechanical Source Projection working views.
- WSO mode: mixed human-led plus agent-assisted public browser/web inspection,
  with bounded source-language anchors embedded directly in the artifact.
- Combined handoff mode: consolidation of current capture artifacts only. This
  artifact receipts a previously produced targeted recapture packet; it does
  not perform new live recapture, archive body retrieval, source completion,
  ECR design, Cleaning, Judgment, runtime, or tooling.

## Per-Venue Posture

| Venue unit | Captured surface | Capture posture | Principal visible limitations | Current handoff implication |
| --- | --- | --- | --- | --- |
| Reddit batch 1of2, rows R01-R05 | Five local `r/FinancialCareers` JSON slices with bounded source-language anchors and supplemental local media/archive posture for `R01`/`R03`. | `categorical_handoff_to_ECR` with visible limitations. | `R01` gallery/comment images and `R03` preview images are now locally preserved; remaining limits are local JSON cutoff, no live continuation, one visible `more` placeholder, deleted rows as placeholders, no available Wayback snapshots for targeted locators, and no archive body retrieval. | Can travel categorically as a bounded Reddit sub-batch if those snapshot and archive-body limits remain visible. |
| Reddit batch 2of2, rows R06-R10 | Five local `r/FinancialCareers` JSON slices plus existing projection working views and supplemental local media/archive posture for `R08`/`R10`. | `categorical_handoff_to_ECR` with visible limitations. | Missing separately logged per-thread acquisition receipts; `R08` and `R10` image assets are now locally preserved; targeted archive availability returned no snapshots; supplied set mixes direct-frame, adjacent, older, and UK/DACH context. | Can travel categorically as a bounded Reddit sub-batch only if mixed-slice, acquisition, and archive-body limits remain visible. |
| Reddit control note | Control summary for both Reddit sub-batches. | Reddit captured with visible limitations; neither sub-batch has active `capture_closure_blocker`. | Reddit-only state was incomplete Slot 3 coverage before WSO; targeted media recapture now supplements the two Reddit sub-batches, while live continuation and archive body retrieval remain unperformed. | Now serves as routing/control source for combined handoff; not a synthesis or validation artifact. |
| WSO bounded visible-page envelope pass | Seven public WSO URL slices with source-language anchors plus visible HTML, text excerpts, screenshots, and archive availability posture. | `categorical_handoff_to_ECR` for bounded visible-page envelope pass only. | No full WSO comment graph, hidden/comment-unlocked material, archive body retrieval, or projection rows; checker was artifact-internal Codex pass, not separate manual GPT-5.5 UI invocation. | Can travel as second-venue capture if treated as bounded visible-page envelope capture, not as a complete WSO corpus. |

## Cross-Venue Limitation Posture

- Reddit is stronger on raw/projection preservation because it has local raw JSON
  and, for batch 2, existing projection working views. Targeted image/gallery
  assets are now locally preserved for the previously image-limited slices.
- WSO is stronger as a non-Reddit venue check with source-language anchors. It
  now also has visible HTML, text excerpts, screenshots, and archive
  availability posture for the selected pages. It remains weaker on full source
  preservation because there is no complete comment graph, archive body packet,
  hidden-comment capture, or projection packet.
- Both venues carry `visible_capture_limitation` checker results rather than
  clean checker closure.
- The combined Slot 3 surface is mixed by design: direct non-target pain,
  resume/no-response pain, networking/interview access pain, advice/context,
  adjacent role/geography slices, and counter-signal context are all visible.
- No combined-source Cleaning, semantic clustering, relevance ranking,
  credibility classification, or downstream-use decision is made here.

## Final Combined Handoff-State Decision

Handoff state: `categorical_handoff_to_ECR`.

Reason:

The combined Slot 3 surface is captured enough for categorical Data
Capture-owned handoff because the active re-capture driver in the prior handoff
state has been addressed: `R01`, `R03`, `R08`, and `R10` media assets are now
locally preserved in the 2026-06-01 recapture packet, WSO has supplemental
visible-page envelope receipts, and archive availability posture is recorded
instead of silently omitted.

This is not a clean-source or completeness claim. The handoff remains bounded to
the preserved Reddit local JSON/projection/readable views, the supplemental
Reddit media packet, and the bounded WSO visible-page envelope packet. Downstream
layers must still carry the local-JSON cutoff, no live Reddit continuation, one
`R01` empty `more` placeholder, deleted-row placeholders, no archive body
retrieval, WSO hidden/comment-unlocked material not captured, no full WSO comment
graph, and same-thread/artifact-internal checker posture for WSO.

This is not a `visible_blocker` or `visible_stop`: all current venue inputs now
travel categorically as bounded inputs with visible limitations. The correct
combined classification is therefore `categorical_handoff_to_ECR`, not because
Slot 3 is complete, but because Capture has made the raw/provenance/source-limit
surface inspectable enough for downstream layers to proceed without recollecting
the source history.

Future recapture candidates, if later authorized and material downstream:

- Reddit: live continuation beyond the local JSON cutoff, especially the `R01`
  empty `more` placeholder.
- Reddit and WSO: archive body retrieval where historical/cutoff posture becomes
  load-bearing.
- WSO: full comment graph, hidden/comment-unlocked material, account-created
  access output, or row-level Mechanical Source Projection if WSO becomes
  source-load-bearing enough to need stronger source preservation.

No new recapture is performed in this artifact; it receipts the completed
2026-06-01 recapture packet.

## Artifact Hygiene Validation Record

Validation scope:

- stale obligation vocabulary and stale artifact reference search;
- current source-input hash confirmation;
- checker-token hygiene;
- downstream leakage search for Judgment, Cleaning, ECR schema, source-quality,
  runtime, approval, or readiness overclaims;
- Markdown diff hygiene.

Validation result:

- Current source-input hashes match the Source Surface table.
- The 2026-06-01 recapture packet receipts match the Source Surface table.
- Short recapture readback confirmed all 10 Reddit media files opened as
  readable images; all seven WSO text/HTML files contained the expected title
  anchors; and archive body retrieval remained explicitly `not_attempted`.
- The WSO receipt JSON preserves original temp-path file pointers, while the
  canonical packet files are the workspace-rooted files under the
  `wso_visible_envelope/` packet root; visible HTML files appear capped near
  200KB, so text excerpts and screenshots remain primary evidence for page
  content beyond that bounded HTML capture.
- No stale pre-amendment raw-observable or handoff-sufficiency obligation
  vocabulary was found in operative text.
- No stale single-Reddit-capture artifact reference was found in operative text.
- No stale checker scaffolding token was found.
- Downstream-vocabulary hits appear only in boundary, forbidden-output, or
  non-claim contexts, not as operative capture decisions.
- Pre-commit whitespace validation should be run after staging because this
  artifact is currently untracked; an unstaged `git diff --check` does not
  inspect untracked file contents.

This validation record is artifact-hygiene evidence only. It is not Data Capture
validation, source-fidelity certification, pressure-test discharge, ECR receipt,
Cleaning readiness, Judgment readiness, or approval.

## Non-Claims

This artifact does not:

- complete a full Slot 3 corpus;
- claim full Reddit or WSO source completeness;
- claim source quality, credibility, integrity, relevance,
  representativeness, or downstream admissibility;
- validate, certify, approve, accept, or harden the Data Capture Spine;
- discharge the full pressure-test batch;
- define ECR fields, IDs, schemas, storage, file formats, or runtime receipt
  mechanisms;
- perform Cleaning, normalization certification, semantic dedupe, clustering,
  summarization, or translation;
- perform Judgment, Signal Use Classification, Decision Strength, Action
  Ceiling, discounting, exclusion, buyer proof, customer synthesis, or
  commercial-readiness assessment;
- authorize source-system planning, scrapers, APIs, dashboards, storage,
  packages, tests, deployment, commits, pushes, or PRs.
