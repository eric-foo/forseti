# Data Capture Spine Pressure-Test Slot 3 Reddit Capture Session v0

```yaml
retrieval_header_version: 1
artifact_role: Data Capture pressure-test capture-session artifact
scope: Records the Reddit-only first-pass Data Capture session for Slot 3 non-target US-domestic resume-driven interview-getting pain.
use_when:
  - Checking the first-pass Slot 3 Reddit capture posture before ECR receipt.
  - Reviewing Data Capture obligation discharge against the accepted intake surface and commissioning plan.
  - Preserving visible limitations before any later WSO pass, ECR design, Cleaning work, or Judgment synthesis.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_execution_authorization_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_intake_surface_consolidation_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - A later owner decision rejects or supersedes the Reddit-only first-pass scope.
  - The Slot 3 WSO pass is completed and a combined Slot 3 capture-session artifact supersedes this one.
  - The accepted intake-surface target, commissioning plan, or obligation contract is materially amended before this capture is receipted.
```

## Status

Status: `CAPTURE_SESSION_REDDIT_ONLY_FIRST_PASS_RECORDED_V0`.

This artifact records a Reddit-only first-pass capture session for the authorized
Slot 3 pressure-test frame. It does not complete Slot 3 across all named venues:
Wall Street Oasis is explicitly deferred and remains a visible limitation.

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Slot 3 Reddit pressure-test execution pack
  edit_permission: docs-write
  target_scope: docs/product/data_capture_spine_pressure_test_slot3_reddit_capture_session_v0.md
  dirty_state_checked: no destructive git operation attempted
  blocked_if_missing: none for Reddit-only first pass
```

## Decision Frame

- Decision question: Can Data Capture preserve the Reddit portion of Slot 3
  non-target resume-driven interview-getting pain as raw source plus optional
  Mechanical Source Projection, with enough categorical context for ECR receipt,
  without drifting into Cleaning, ECR schema, Judgment, or runtime/tooling design?
- Owner or owner-context: Orca owner / Chief Architect pressure-testing the Data
  Capture Spine and Mechanical Source Projection intake boundary.
- Consequence: The result informs whether the accepted intake surface and
  obligation contract are sufficient for a threaded forum corpus, and which
  limitations must travel into later WSO capture, ECR receipt, Cleaning, or
  Judgment work.
- Allowed decision verbs: `categorical_handoff_to_ECR`, `visible_stop`,
  `visible_blocker`, `rerun`, `re-capture_posture`, or later owner-authorized
  pressure-test patch planning.
- Cutoff posture: Authorized Slot 3 cutoff is Q2 2026. The local Reddit thread
  set includes selected posts created between 2023-11-26 and 2026-05-25, with no
  selected thread after Q2 2026. No live Reddit recapture was performed in this
  session.
- Downstream-use intent: Data Capture handoff only. This artifact does not rank
  pains, judge source value, classify credibility, define ECR fields, perform
  Cleaning, or synthesize customer meaning.

## Source Boundary

- Source surfaces in scope:
  - Local operator-supplied Reddit JSON files under
    `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/raw/thread_json/`.
  - Local source-projected thread outputs under the legacy path
    `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/cleansed/threads/`.
    The folder name `cleansed` is legacy batch naming only; these are Mechanical
    Source Projection outputs, not Cleaning Spine outputs.
  - Local screenshots under
    `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/raw/screenshots/`.
  - Local search-support files under
    `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/raw/search_json/`.
  - Selection manifest at
    `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/thread_selection_manifest.csv`.
- Boundary compliance (public / market-level / non-deceptive / non-intrusive):
  Local files are operator-supplied Reddit public-source captures and local
  projections. This session used local file inspection only; it did not use
  private access, authenticated access, paywall bypass, deception, scraping,
  API calls, automated extraction builds, or runtime/source-system tooling.
- Out-of-bounds material observed and excluded:
  - Wall Street Oasis was not attempted in this pass.
  - One malformed duplicate raw JSON delivery was held under
    `raw/thread_json/invalid_hold/` and was not source-projected.
  - Search-support files contain broad/noisy Reddit search listings and are
    preserved as source-discovery context, not treated as selected evidence rows.

## Capture Mode

- Initial mode: mixed human-led / agent-assisted / Mechanical Source Projection.
- Material mode changes during the session: none. The session used existing
  operator-supplied files and existing projection outputs; no live source access
  or recapture was added.

## Per-Obligation Discharge States

| # | Obligation | State | Reason (required for non-`met`) |
| --- | --- | --- | --- |
| 1 | Commissioning Gate | met | |
| 2 | Boundary Compliance | met | |
| 3 | Capture-Event Provenance | partial | Local corpus paths, source hashes, and artifact date are visible, but exact original operator acquisition timestamps are not recorded per thread beyond the folder date and source timestamps. |
| 4 | Capture Mode Disclosure | met | |
| 5 | Mode-Change Rule | met | |
| 6 | Raw Observable Preservation | partial | Ten valid thread JSON files, 12 screenshots, 2 search-support files, and 563 projected rows are preserved locally. Visual/media evidence is preserved at pointer and screenshot level, but linked Reddit gallery/image assets were not independently archived as original media files in this pass. |
| 7 | Source Identity And Actor Context | met | |
| 8 | Decomposed Timing | partial | Reddit `created_utc` and available `edited` timestamps are preserved in raw/projection files; exact operator acquisition time and archive time are not separately recorded. |
| 9 | Cutoff Posture | met | |
| 10 | Archive / Historical Posture | partial | Raw JSON and screenshots are locally preserved, but no public archive lookup or external archival confirmation was attempted. |
| 11 | Source Visibility And Access Limits | met | |
| 12 | Related Context Preservation | partial | Reddit thread/reply hierarchy is preserved in raw JSON and projected `path` fields. One selected thread projects a `more_placeholder`, and WSO related venue coverage is not attempted in this first pass. |
| 13 | Bundled-Offer Structure Observables | not_applicable | Slot 3 Reddit first pass is a forum-thread corpus, not a bundled offer, settlement, pricing package, or multi-term counterpart package. |
| 14 | Capture Failure And Blocker Visibility | met | |
| 15 | Re-Capture Semantics | met | |
| 16 | Categorical Handoff Sufficiency | partial | The Reddit-only corpus can hand off categorically with visible limitations, but this artifact does not complete Slot 3 across WSO and does not certify visual-media completeness, Cleaning readiness, or Judgment use. |

Allowed states used: `met`, `partial`, `not_applicable`.

## Per-Slice Posture

| Slice | Archive/history posture | Source visibility/access posture | Related context posture | Re-capture relationship |
| --- | --- | --- | --- | --- |
| Reddit selected thread JSON | Ten valid `.json` captures preserved locally; no external archive lookup attempted. | Public Reddit thread JSON supplied by operator; local-only inspection in this session. | Full available post/comment tree from each saved JSON is preserved; projected JSONL retains row type, parent, depth, path, author, submitter flag, body, timestamps, score, lock/collapse/sticky fields where available. | First recorded capture-session pass from the local Slot 3 batch; no live recapture performed. |
| Mechanical Source Projection outputs | Ten projection directories preserved locally with `thread.json`, `content.jsonl`, and `readable.md`. | Projection is a working view over local raw JSON and does not replace raw. | Corpus-level projection contains 563 rows: 10 post rows, 546 comment rows, 6 moderator notice rows, and 1 `more_placeholder` row. | Projection can be rerun against preserved raw files if later pressure-test review requires it. |
| Screenshots | Twelve `.png` screenshots preserved locally. | Local image files only; original Reddit media URLs were not fetched in this session. | Thread-level screenshots exist for selected posts; image/resume-specific screenshots exist for at least the resume-feedback and speedrunning-rejections slices. | Future media recapture can compare against these local screenshots and raw URL fields. |
| Search-support files | Two raw search-support files preserved locally. | Operator-supplied local search listings; not projected by the Reddit thread worker. | Broad search listings are source-discovery context only and contain off-frame/noisy results. | Not treated as selected thread evidence; future search recapture should be separately commissioned if needed. |
| WSO venue | Not attempted. | Not attempted. | Not attempted. | Deferred to second pass; this artifact must not be read as full Slot 3 venue completion. |
| Invalid duplicate raw file | One malformed duplicate file preserved under `raw/thread_json/invalid_hold/`. | Local malformed duplicate delivery, not a selected evidence source. | Excluded from projection because valid selected raw files already exist for the relevant threads. | If needed, compare against selected valid files before deletion or archival disposition; no deletion authorized here. |

## Raw Observable Pointers

Preserved root:

```text
docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/
```

Selected thread corpus:

| Capture ID | Thread ID | Tier | Title | Raw materialized comments | Projected rows | Projection notes |
| --- | --- | --- | --- | ---: | ---: | --- |
| R01 | `1tmu6ft` | P0 | 200+ applications no job | 120 | 122 | Includes 1 post row, 120 comment rows, and 1 `more_placeholder`; linked gallery URL preserved in manifest/raw URL fields. |
| R02 | `1r38dch` | P2 | I wish I could kick the shit out of my 15 year-old self. | 118 | 119 | Includes 1 post row and 118 projected comment/moderator rows. |
| R03 | `1tj8f96` | P2 | Is it worth giving up a target school to go to a non target with a full ride? | 42 | 43 | Manifest marks this as the only `counter_signal=true` row. |
| R04 | `1qw3ufa` | P0 | Junior Year at Non-Target and No Internships/Work Experience - What Should I Do? | 13 | 14 | Includes 1 post row and 13 projected comment/moderator rows. |
| R05 | `1p6hhbb` | P1 | Non-target, working in a BB in Risk...Dreaming the FO | 26 | 27 | Valid raw file projected; malformed duplicate preserved separately in invalid hold. |
| R06 | `1t9dp7z` | P1 | Non-target freshman trying to break into IB needing advice | 13 | 14 | Includes 1 post row and 13 projected comment/moderator rows. |
| R07 | `1sbky91` | P0 | Non-target junior getting mass rejected from everything. It's over. | 86 | 87 | Highest-priority anchor thread in manifest notes; no Judgment conclusion made here. |
| R08 | `1ow472d` | P0 | Non-Target Junior, Resume Feedback | 45 | 46 | Linked image URL preserved in manifest/raw URL fields; screenshot files also present. |
| R09 | `184odt8` | P1 | Rejected due to my educational background | 67 | 68 | Credential-background rejection adjacent to the frame; no relevance decision made here. |
| R10 | `1qaxpq4` | P0 | Speedrunning rejections (0 interviews) - Off-cycle IB/PE UK & DACH - CV review | 22 | 23 | Linked image URL preserved in manifest/raw URL fields; screenshot files also present. |

Projection-row preservation check:

```text
valid_raw_thread_files: 10
projection_thread_dirs: 10
projection_total_rows: 563
projection_row_shape: 10 post rows + 546 comment rows + 6 moderator_notice rows + 1 more_placeholder row
invalid_hold_files: 1 malformed duplicate, not projected
```

Projection metadata pointer:

```text
Each projection directory contains thread.json with source_file and source_sha256.
Each content.jsonl row preserves row_type plus thread/comment fields needed for source-row reachability.
Each readable.md file provides a human-readable working view over the same projection rows.
```

Source-envelope/noise posture:

```text
Projection may remove Reddit/API envelope noise from the working view.
Projection does not remove evidence rows for looking low-value, repetitive, deleted,
bot-like, low-score, embarrassing, or unhelpful.
Raw JSON remains preserved as the authority behind the working projection.
```

## Failures, Blockers, and Limitations

- Capture-owned failures observed:
  - One malformed duplicate raw JSON delivery is preserved under
    `raw/thread_json/invalid_hold/` and is excluded from projection.
  - One projected thread contains a `more_placeholder`, making the continuation
    state visible rather than silently treating the projection as exhaustive.
- Visible limitations to travel downstream:
  - WSO was not attempted; this is a Reddit-only first pass.
  - Exact operator acquisition timestamps for the original raw JSON saves are not
    separately recorded per thread.
  - No external archive lookup or archival confirmation was attempted.
  - Visual/media evidence is present as local screenshots and raw URL pointers,
    but original linked Reddit image/gallery assets were not independently
    archived as source media files in this pass.
  - Search-support files are preserved but noisy and are not mechanically
    source-projected by the Reddit thread worker.
- Out-of-bounds material treated as out of bounds:
  - No private/authenticated/paywalled/deceptive source access was attempted.
  - No runtime/source-system/tooling plan was created.
  - No ECR schema, Cleaning implementation, or Judgment synthesis is included.

## Agent-Assistance Context

- Allowed agent verbs used:
  - Read Orca overlay and controlling product docs.
  - Inspect local file paths and existence.
  - Parse local CSV/JSON/JSONL files with PowerShell for corpus counts and
    projection row-shape checks.
  - Draft this capture-session Markdown artifact.
- Discarded candidates and discard reason categories:
  - `raw/thread_json/invalid_hold/nontarget_working_in_a_bb_in_riskdreaming_the_fo.200_applications_no_job__invalid_json.json`
    was not projected because it is a malformed duplicate delivery and selected
    valid raw JSON files are present.
  - Broad search-support listings were not promoted into selected evidence rows
    because the manifest-selected thread corpus already identifies the ten
    Reddit threads for this first pass.
- Any cross of the allow/forbid line: none observed. No live access, scraping,
  runtime build, source-system planning, ECR schema, Cleaning transformation, or
  Judgment conclusion was performed.

## Categorical Handoff Or Visible Stop

- Handoff state: `categorical_handoff_to_ECR`.
- Reason if not `categorical_handoff_to_ECR`: not applicable.
- Visible limitations attached to handoff:
  - Reddit-only first pass; WSO venue deferred.
  - Archive posture, exact acquisition timestamp posture, visual-media
    preservation posture, and `more_placeholder` continuation posture must travel
    downstream.
  - ECR may receipt categorical source/projection context, but this artifact does
    not define ECR fields, IDs, storage, schema, table shape, or runtime receipt
    mechanism.

## LLM Capture-Visibility Checker Output

- Output: `visible_capture_limitation`.
- Specifics:
  - Obligations 3 and 8: exact original operator acquisition timestamps are not
    recorded per thread beyond local corpus path/date and source timestamps.
  - Obligations 6 and 10: linked Reddit image/gallery media were not independently
    archived, and no external archive lookup was attempted.
  - Obligation 12: one `more_placeholder` continuation is visible, and WSO venue
    coverage is explicitly deferred.
  - Obligation 16: categorical handoff is only for the Reddit-only first pass;
    full Slot 3 venue coverage is incomplete.
  - Artifact-internal scope only: source corpus fidelity and completeness were
    not inspected.
- Remediation taken by capture operator:
  - Limitations were made explicit in the obligation table, per-slice posture,
    raw observable pointers, failures/limitations, and categorical handoff
    sections.
  - No attempted remediation required live source access, media download,
    runtime tooling, ECR design, Cleaning, or Judgment work.
- Post-remediation re-invocation output: not invoked.

## Non-Claims

This artifact does not:

- complete Slot 3 across Reddit and WSO;
- validate, certify, approve, accept, or harden the Data Capture Spine;
- discharge the full pressure-test batch;
- claim source quality, credibility, integrity, relevance, representativeness,
  or downstream admissibility;
- define ECR fields, IDs, schemas, storage, file formats, or runtime receipt
  mechanisms;
- perform Cleaning, normalization certification, semantic dedupe, clustering,
  summarization, or translation;
- perform Judgment, Signal Use Classification, Decision Strength, Action Ceiling,
  discounting, exclusion, buyer proof, customer synthesis, or commercial-readiness
  assessment;
- authorize source-system planning, scrapers, APIs, dashboards, storage,
  packages, tests, deployment, commits, pushes, or PRs.
