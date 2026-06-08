# Adversarial Artifact Review: Data Capture Spine Manual Harness and BT2-04 Dry Run

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Adversarial artifact review of the reusable manual Data Capture dry-run harness
  and the first BT2-04 commissioned manual dry-run output, as a pair.
use_when:
  - Deciding whether the harness and dry run are usable for the next Data Capture move.
  - Preparing a harness patch prompt after first dry-run pressure.
  - Checking whether BT2-04 dry-run output can serve as first harness-use evidence.
authority_boundary: retrieval_only
input_hashes:
  harness: untracked in worktree at review time; worktree b7627d3
  dry_run: untracked in worktree at review time; worktree b7627d3
  obligation_contract: untracked in worktree at review time
  charter: untracked in worktree at review time
branch_or_commit: codex/data-capture-sourcing-architecture@b7627d3
stale_if:
  - The harness or dry-run artifact is patched.
  - The obligation contract is materially revised.
  - A superseding adversarial review is produced.
```

---

## 1. Retrieval Header and Review Status

- **Review type**: Adversarial artifact review — pair review.
- **Review date**: 2026-05-26.
- **Review branch / HEAD**: `codex/data-capture-sourcing-architecture` @ `b7627d3` (confirmed via git log).
- **Review lane**: Artifact review; read-only; report written to `docs/review-outputs/` only.
- **Dirty state**: Multiple Data Capture artifacts were untracked at review time. Treated as repo-visible worktree sources, not source-of-truth promoted.

### Opening Non-Claims

This review does not claim:

- Data Capture is complete.
- The obligation contract is validated or hardened.
- The harness is formally validated.
- BT2-04 proves product readiness or buyer proof.
- ECR, Cleaning, Judgment, runtime, or tooling is ready.
- Any source map, scraper, API, storage, dashboard, automation, test, deployment, or implementation should be built.
- Source-of-truth promotion.
- Data Capture closure.

---

## 2. Source / Preflight Ledger

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Data Capture dry-run review pack (S4 equivalent)
  edit_permission: review-report-write only
  target_scope: adversarial pair review of harness and BT2-04 dry run; write durable report; no source edits, no harness patches, no dry-run edits
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README; source-loading; artifact-folders; artifact-roles; retrieval-metadata; review-lanes; validation-gates; repo-map; obligation contract; source-family/capture-mode architecture; satellite boundary note; harness; charter; dry-run output
```

| Source | Why read | Worktree status |
| --- | --- | --- |
| `AGENTS.md` | Orca project boundary and docs-write limits | Clean read |
| `.agents/workflow-overlay/README.md` | Overlay binding rule | Clean read |
| `.agents/workflow-overlay/source-loading.md` | Start preflight, source-pack, and body-shape rules | Clean read |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted destination paths | Clean read |
| `.agents/workflow-overlay/artifact-roles.md` | Review report role and permission | Clean read |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract | Clean read |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules and report destination | Clean read |
| `.agents/workflow-overlay/validation-gates.md` | Gate expectations for durable artifacts | Clean read |
| `docs/workflows/orca_repo_map_v0.md` | Navigation; noted as modified in worktree | Modified |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation surface | Untracked in worktree |
| `docs/product/core_spine_v0_data_capture_spine_source_family_capture_mode_architecture_v0.md` | Source-family routing architecture | Untracked in worktree |
| `docs/product/core_spine_v0_data_capture_spine_source_family_satellite_boundary_note_v0.md` | Satellite ceiling and governance | Untracked in worktree |
| `docs/product/core_spine_v0_data_capture_spine_manual_dry_run_harness_v0.md` | **Primary review target — harness** | Untracked in worktree |
| `docs/product/core_spine_v0_data_capture_spine_bt204_manual_dry_run_v0.md` | **Primary review target — dry run** | Untracked in worktree |
| `docs/product/core_spine_v0_data_capture_spine_first_commissioned_dry_run_charter_v0.md` | Commission and cutoff authority | Untracked in worktree |

**Dirty-state note**: All primary review targets and their supporting architecture artifacts were untracked at review time. Findings are advisory claims based on repo-visible worktree evidence. Strict claims about acceptance, source-of-truth status, validation, or readiness require controlling committed authority and remain `not proven` on this basis alone.

---

## 3. Review Target Summary

**Pair under review**:

1. `docs/product/core_spine_v0_data_capture_spine_manual_dry_run_harness_v0.md` (`MANUAL_HARNESS_DRAFT_V0`) — the reusable manual operating envelope for Capture-only commissioned dry runs.
2. `docs/product/core_spine_v0_data_capture_spine_bt204_manual_dry_run_v0.md` (`MANUAL_DRY_RUN_OUTPUT_V0`) — the first commissioned BT2-04 dry-run instance, using the harness.

**Core review question**: Did the manual harness and the BT2-04 dry-run output, together, actually keep Data Capture disciplined?

---

## 4. Verdict

```yaml
verdict: PATCH_BEFORE_NEXT_DRY_RUN
max_severity: P2
usable_as_first_harness_evidence: yes
```

**Rationale**: No P0 or P1 defects found. The pair prevents fake capture success, silent candidate omission, ECR/Cleaning/Judgment leakage, tooling drift, and downstream proof/backtest calibration leakage. Three P2 defects require patching before the system is used for another commissioned dry run: (1) discard reason vocabulary drift between harness template and dry-run execution; (2) CS-08 raw observable is a summary rather than preserved source language; (3) H-09 obligation discharge ledger uses run-level rollups that do not expose per-slice archive/historical and timing states where the obligation contract requires them.

The BT2-04 dry run is usable as first harness-use evidence — it demonstrates obligation-first structure, genuine negative-space recording, archive-failure visibility, and layer-boundary discipline — but its P2 defects should be visible to downstream readers and the harness should be patched before the next run.

---

## 5. Findings — Ordered by Severity

### 5.1 P2 Findings

---

**[H-P2-01] Harness discard-reason vocabulary differs from dry-run vocabulary**

- **Severity**: P2
- **Artifact**: Harness, `H-04 Candidate Trace`, allowed discard reason categories list
- **Issue**: The harness template defines `post_window_for_current_commission` as the discard reason for post-window candidates. The BT2-04 dry run uses `post_cutoff_for_at_cutoff_use` instead, describes it as the "commissioned fixed vocabulary," and applies it throughout H-04. These are not the same term. No harness update row in H-00 reconciles this substitution.
- **Why it matters for Capture discipline**: Vocabulary drift between the harness template and a dry-run's actual usage creates incompatibility when comparing obligation discharge states across multiple dry runs. Future runs may use the harness template term (`post_window_for_current_commission`) while this run used `post_cutoff_for_at_cutoff_use`. A reviewer checking cross-run consistency would see two terms that appear different but refer to the same state — or may not realize they differ. The dry run's term is arguably more precise for cutoff-date cases, which makes the harness template's broader phrasing a defect.
- **Recommended patch direction**: Update the harness H-04 discard vocabulary to `post_cutoff_for_at_cutoff_use` (adopt the dry run's more commission-specific term). Add a brief annotation that this category applies to post-cutoff candidates in backtest or cutoff-date-specific runs. If the broader `post_window_for_current_commission` term covers a materially different case (e.g., pre-cutoff-date commission windows), retain it as a sibling category with distinct definitions. Add an H-00 change-log row when this change is made.

---

**[H-P2-02] H-09 rollup design does not require per-slice obligation states when source states differ**

- **Severity**: P2
- **Artifact**: Harness, `H-09 Obligation Discharge Ledger`, design and instructions
- **Issue**: The harness template presents H-09 as a single-row-per-obligation ledger with no guidance on when rollup is permitted vs. when per-slice rows are required. The obligation contract states: "A rollup archive posture is allowed only when it does not hide a failed, degraded, unavailable, not-attempted, fallback, migrated, or conflicting source state." The harness doesn't encode this rollup condition or instruct operators to split the ledger when source states differ.
- **Why it matters for Capture discipline**: An operator following the harness template can legitimately write one `partial` row per obligation and cross-reference H-07 — and still technically comply with the harness as written — even when per-slice states would expose materially different archive, timing, or access failures. The gap between the harness template's one-row-per-obligation design and the obligation contract's rollup prohibition is a harness defect that can silently permit obligation collapse.
- **Recommended patch direction**: Add a rollup condition note to H-09 template instructions: when archive/historical posture, decomposed timing, or source visibility states differ materially across source slices, either (a) add sub-rows by source slice for those obligations or (b) explicitly cross-reference H-07 per-slice content with a stated rationale for the rollup. Align the condition with the obligation contract's language.

---

**[D-P2-01] CS-08 raw observable is a summary, not a preserved source-visible statement**

- **Severity**: P2
- **Artifact**: Dry run, `H-05 Source-Slice Capture Notes`, CS-08 Axios entry, `Raw observable` field
- **Issue**: The H-05 raw observable for CS-08 reads: "Axios described text-prompt image programs as moving quickly into cultural disruption, identified rights, falsehoods, ownership, creativity, jobs, training-data, and compensation questions, and contrasted DALL-E 2 with Stable Diffusion's open-source/downloading posture." This is Orca's characterization of the Axios article's themes — not a preserved source-visible claim. No direct quotation or source-language excerpt is provided. The obligation contract requires: "preserve what the source showed or said, not only Orca's summary" and warns: "Source-read ledgers, summaries, and title/date/claim rows are provenance aids. They do not by themselves preserve the raw observable when source meaning depends on thread context, modality, layout, edits, related replies, or visible source structure."
- **Why it matters for Capture discipline**: The downstream ECR reconstruction floor requires reconstructing what the Axios source was claiming without re-fetching. With only a thematic summary, it is not possible to determine whether specific Axios phrasings, named actors, specific issue framings, or exact contrasts between DALL-E 2 and Stable Diffusion were present in the source or introduced by Orca. This sets a precedent that paraphrase-as-capture is acceptable for media/analysis sources, which the obligation contract specifically prohibits.
- **Recommended patch direction**: Flag CS-08 as requiring a raw observable supplement. Add a recapture note stating that the current entry is a high-level paraphrase of the Axios article's themes and that at least two to three direct source-language excerpts should be added in a follow-on recapture before CS-08 is used for downstream ECR or Judgment inspection. The existing entry may stand as a partial capture state marker, but should not represent the raw observable standard.

---

**[D-P2-02] H-09 uses run-level rollups that do not expose per-slice archive/historical and decomposed timing states**

- **Severity**: P2
- **Artifact**: Dry run, `H-09 Obligation Discharge Ledger`, rows `Archive / historical posture` and `Decomposed timing`
- **Issue**: H-09's `Archive / historical posture` row records one `partial` state with a cross-reference to H-07. H-09's `Decomposed timing` row records one `partial` state with a generic limitation note. However, across the 8 source slices: CS-01 used a fallback mirror with no Wayback attempt; CS-02 had no archive attempt at all; CS-03 through CS-07 had failed Wayback attempts; CS-08 was not attempted. These are materially different obligation states — `not_attempted`, `partial` (fallback used), `partial` (failed archive), and `blocked` (for those where failure was the only state). The obligation contract prohibits rollups that "hide a failed, degraded, unavailable, not-attempted, fallback, migrated, or conflicting source state." The cross-reference to H-07 partially mitigates this, but H-09 as the obligation discharge ledger does not itself expose these states.
- **Why it matters for Capture discipline**: A downstream reviewer inspecting H-09 as the obligation ledger would see only `partial` for archive obligations across the entire run. That single state collapses CS-01's successful fallback, CS-02's no-attempt, CS-03..07's failed Wayback attempts, and CS-08's no-attempt into one undifferentiated row. The H-07 cross-reference requires separate section reading that may not happen in a rapid downstream review.
- **Recommended patch direction**: Add per-slice sub-rows to H-09 for the `Archive / historical posture` and `Decomposed timing` obligations. At minimum: for each source slice, state the obligation state (`met`, `partial`, `blocked`, `unavailable_by_source`, `not_attempted`) and a one-line evidence note. The H-07 cross-reference may remain as supplementary detail.

---

### 5.2 P3 Findings

---

**[D-P3-01] Dry run treats its own extended vocabulary as "commissioned fixed vocabulary" without harness cross-reference**

- **Severity**: P3
- **Artifact**: Dry run, `H-04 Candidate Trace`, opening note
- **Issue**: H-04 opens with "Discard reasons use the commissioned fixed vocabulary: `out_of_scope_commission`, `duplicate_locator`, `inaccessible`, `non_public`, `boundary_violating`, `source_family_misclassified`, `post_cutoff_for_at_cutoff_use`, and `not_needed_after_bounded_capture`." The harness template defines `post_window_for_current_commission`, not `post_cutoff_for_at_cutoff_use`. The dry run presents its own term as if it is the harness vocabulary without noting the substitution.
- **Why it matters**: Future operators reading the dry run as usage guidance would see a different vocabulary than the harness template, without knowing a deliberate substitution occurred. This compounds H-P2-01.
- **Recommended patch direction**: Add a parenthetical in the H-04 opening note noting that `post_cutoff_for_at_cutoff_use` is the BT2-04-specific refinement of the harness template's `post_window_for_current_commission`. Cross-reference H-12/H-13/H-14 where this vocabulary pressure should have been logged as a run-local addition and field candidate.

---

**[D-P3-02] `boundary_violating` used for uncertain-boundary rather than confirmed-boundary cases**

- **Severity**: P3
- **Artifact**: Dry run, `H-04 Candidate Trace`, row for public social/contributor statements
- **Issue**: The dry run uses `boundary_violating` as the discard reason for Reddit/social/professional posts where the operator stopped because boundary safety was uncertain, not because a confirmed boundary violation would occur. The harness's discard category implies a confirmed boundary crossing.
- **Why it matters**: Conflating "uncertain boundary safety" with "confirmed boundary violation" could either over-restrict future runs (refusing candidates that could be captured safely) or under-document the decision (not showing whether the uncertainty itself was the stop reason or an anticipated confirmed violation).
- **Recommended patch direction**: Add a note to the H-04 table row clarifying that `boundary_violating` is used here as a precautionary stop due to high uncertainty about maintaining the public/market-level/non-dossier boundary without further source expansion — not a confirmed violation. Consider adding a future H-12 friction entry for "boundary_uncertain_stop" as a candidate for harness vocabulary extension.

---

**[H-P3-01] Harness section numbering is discontinuous (H-15 → section 21)**

- **Severity**: P3
- **Artifact**: Harness, section numbering
- **Issue**: The harness uses `H-00` through `H-15` for operator sections, then jumps to `## 21. Stop Gates`, `## 22. Update Protocol`, and `## 23. Non-Claims`. Sections 16–20 do not exist. The dry run references these section numbers (e.g., "Section 21" in the stop-gate assessment) without confusion, but the gap in numbering is a navigational clarity issue.
- **Why it matters**: Minor navigational confusion when referencing by number in cross-artifact citations.
- **Recommended patch direction**: Normalize numbering: either renumber outer sections to follow H-15 (e.g., `## 16. Stop Gates`) or keep the H- prefix through all operator sections and add non-H numbered outer sections starting at 1. Update the dry run's references to match.

---

**[D-P3-03] No `input_hashes` in dry-run retrieval header for a cutoff-sensitive artifact with untracked inputs**

- **Severity**: P3
- **Artifact**: Dry run, retrieval header
- **Issue**: The dry-run retrieval header does not include `input_hashes` for its controlling sources (obligation contract, harness, charter), several of which were untracked in the worktree during execution. The retrieval-metadata overlay lists cutoff-sensitive artifacts as candidates for `input_hashes`.
- **Why it matters**: Future reviewers cannot verify that the harness, obligation contract, and charter versions used match current repo state without explicit hashes. The source loading table records file status (`Untracked in worktree before this run`) but not content hashes, making strict provenance claims fragile.
- **Recommended patch direction**: Add `input_hashes` for at least the harness, obligation contract, and charter. For untracked files, note explicitly that hashes could not be computed and capture a note that the hashes were assigned at first-commit time.

---

**[D-P3-04] Capture timing uses "same session" without UTC equivalent or relative order**

- **Severity**: P3
- **Artifact**: Dry run, `H-06 Timing And Window Posture`, capture timing column; `H-09`, limitation note
- **Issue**: All eight source slices record capture timing as "same session" or reference the session timestamp `2026-05-26T00:47:34+08:00 local shell timestamp." The H-09 limitation note flags the absence of a UTC timestamp. No within-session relative order is provided.
- **Why it matters**: For multi-session or multi-timezone audit, a UTC timestamp equivalent is cleaner. For cross-slice provenance tracing (e.g., did CS-08 influence CS-04's framing?), relative order within the session is unverifiable.
- **Recommended patch direction**: Add UTC equivalent in H-02 (`2026-05-25T16:47:34Z`). For within-session relative order, a note in H-02 explaining the session was linear or that relative order was not separately recorded is sufficient.

---

## 6. Harness-Specific Assessment

**What the harness gets right**:

- Operating rules 1–10 encode obligation-first, Capture-only, commission-gated behavior. The stop-gate wording in section 21 is concrete enough to prevent fake success (Rule 8, Section 21 fourth bullet).
- The H-00 through H-15 section structure follows the full obligation contract surface: commission → session/mode → source routing → candidate trace → source slice → timing → archive → context/bundle/modality → obligation discharge → failure → captured-but-unusable → friction → run-local additions → field candidates → promotion/deferral.
- The field candidate promotion pathway (H-13 → H-14 → H-15) is appropriately conservative. Promotion requires "repeated pressure across at least two non-overlapping source families" or explicit owner sign-off — language taken directly from the obligation contract.
- The update protocol (section 22) is intentionally conservative. It prevents dry-run convenience from accumulating as permanent core law.

**Harness defects**:

- H-P2-01 (vocabulary): `post_window_for_current_commission` vs. `post_cutoff_for_at_cutoff_use` is the most actionable defect.
- H-P2-02 (H-09 rollup design): the template needs a per-slice split condition aligned with the obligation contract's rollup rule.
- H-P3-01 (section numbering): navigational clarity.
- The harness does not yet address how to handle cases where the `current page leakage` risk is high enough to block pre-cutoff use but low enough to preserve partial observables. This gap was exposed by the dry run and partially handled by run-local additions, but no core harness field or stop-gate language covers it. This is not a defect in the current harness — it's a correctly deferred item — but it is worth noting as harness-development pressure for later dry runs.

**Harness boundary discipline**: Clean. The harness does not authorize implementation, tooling, source maps, ECR design, Cleaning transformations, or Judgment scoring anywhere in its sections. Section 2 and Section 23 non-claims are comprehensive and redundant (redundancy is appropriate for a boundary document).

---

## 7. BT2-04 Dry-Run-Specific Assessment

**What the dry run gets right**:

- H-01 commission capsule is properly filled and tied to the BT2-04 Decision Frame with explicit cutoff, decision verbs, consequence, and boundary statement.
- H-04 candidate trace is the strongest section. It shows eight distinct search/session contexts with batch summaries before filtering, fetched vs. not-captured candidates, discard reasons, and explicit boundary posture. The negative-space note at the end of H-04 explicitly names its purpose. This is genuine Capture discipline.
- H-07 archive/history posture per-slice is detailed and disciplined. Failed Wayback attempts are preserved and not papered over. The note "Archive success did not erase failed exact archive access" is explicitly stated — a genuine non-collapse commitment.
- H-10 failure log covers git-setup issues, SEC body access failures, archive failures, current-page mixed state, Stability AI date ambiguity, LAION update link, professional/social boundary risk, post-cutoff candidate leakage, and Midjourney source state. This is comprehensive failure visibility.
- H-11 captured-but-unusable log correctly marks CS-01, CS-04, CS-05, CS-06, and CS-08 as partial with visible downstream failure reasons. No downstream exclusion decisions are made.
- H-15 promotes no field to core. All candidates are correctly deferred to `run_local_only`, `satellite_guidance`, or `deferred_runtime`.
- The decision to explicitly not read `docs/product/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md` during source loading is a genuine safeguard against treating the proof-run candidate pool as a reusable source map. This is the zero-spoiler principle applied correctly.

**Dry-run defects**:

- D-P2-01 (CS-08 raw observable): media/analysis source has only a thematic summary, not preserved source language.
- D-P2-02 (H-09 rollup): archive/history and decomposed timing obligation states are rolled up without per-slice discharge evidence.
- D-P3-01, D-P3-02, D-P3-03, D-P3-04: minor clarity and provenance gaps.

**Dry-run layer boundary**: Clean. No ECR field, Cleaning transformation, Judgment scoring, credibility label, inclusion/exclusion decision, or proof conclusion appears anywhere in the 8 source slices, H-09, H-11, H-14, or H-15. The "Downstream decision avoided? Yes" column in H-11 is consistently correct. The non-claims section is comprehensive.

---

## 8. Harness / Dry-Run Interaction Assessment

The pair works as an operating unit. The dry run follows the harness structure faithfully — H-00 through H-15 are all present and filled, stop-gate assessment uses harness framing, and the update protocol is respected (no harness patches were made during the run).

**Interaction friction that the pair revealed**:

1. **Vocabulary gap (H-P2-01 / D-P3-01)**: The harness's template vocabulary didn't match what the run needed for cutoff-date-specific backtest cases. The dry run created its own term, described it as the fixed vocabulary, and did not log the substitution in H-13 or H-14. This is a minor harness-learns-from-run scenario that the update protocol should have handled: the vocabulary gap should have appeared as a run-local addition in H-13 and a field candidate in H-14, then routed to the harness as a patch candidate. It wasn't. The pair's update protocol would have caught this if followed strictly.

2. **H-09 rollup gap (H-P2-02 / D-P2-02)**: The harness template didn't require per-slice rows in H-09, so the dry run didn't produce them. The obligation contract requires them when states differ. The harness template needs to encode this condition so future runs surface the difference automatically.

3. **Raw observable standard for media/analysis sources (D-P2-01)**: The harness H-05 template requires "raw observable" but doesn't specify the minimum preservation standard for media/analysis sources where full-text reproduction is impractical. CS-08 shows what happens without that specification: a high-level summary stands in for the source-visible claim. The harness could add a note to H-05 that for media/analysis sources, at least two to three source-language excerpts are needed when a direct quote is unavailable.

**Interactions that worked correctly**:

- The stop-gate for source-map drift was effective. Specific locators appear as run-local output but not as a reusable inventory.
- The archive/history interaction between H-07 and H-10 was handled correctly. H-07 preserves per-slice states; H-10 generalizes them as failures. H-09 is the weak link, not H-07/H-10.
- The field candidate log (H-14) correctly absorbed run-local pressure without promoting it to core. The harness learned from the run without changing.

---

## 9. Field Candidate and Run-Local Addition Assessment

The dry run produced 5 run-local additions in H-13 and 6 field candidates in H-14. All 6 candidates were classified in H-15.

| Candidate | H-15 classification | Reviewer assessment |
| --- | --- | --- |
| Current-page leakage marker | `run_local_only` | Correct. The harness already has H-06 cutoff/window posture. This run shows two-family use pressure but the harness slot exists. Should not be promoted until another dry run surfaces a gap in H-06 specifically. |
| Search-result date support marker | `run_local_only` | Correct. One-family pressure; session-limitation origin; not a harness core gap. |
| Official locator plus fallback body carrier | `run_local_only` | Correct. One public-company access issue; H-07 already handles this. |
| Public/social boundary guard | `satellite_guidance` | Correct. Family-specific boundary pressure; no captured slice used it; correct satellite routing. |
| Post-cutoff negative-space guard | `run_local_only` | Reasonable but borderline. This pattern is relevant to any BT2-04-style cutoff-date backtest frame, and the obligation contract's Cutoff Posture obligation (§9) requires it for all commissioned captures with a cutoff date. A future dry run on a different case with a clear cutoff date would encounter the same need. The run correctly defers it given single-run evidence, but the satellite routing (not core) should be reconsidered if a second backtest-frame dry run surfaces the same need. |
| Repeatable archive/history access check | `deferred_runtime` | Correct. Archive access friction is real but tooling design is explicitly outside authorization. |

**Summary**: No field was improperly promoted to core. The promotion pathway was followed. The most interesting deferral decision is `post_cutoff_negative_space_guard` — it is correctly `run_local_only` for now but may warrant satellite guidance after a second cutoff-date frame.

---

## 10. Source-Map / Runtime / ECR / Cleaning / Judgment Leakage Assessment

| Leakage type | Harness | Dry run | Assessment |
| --- | --- | --- | --- |
| Source-map drift | H-04 forbids favored-source markers; H-03 routing results are not a named inventory | H-10 includes explicit source-map drift stop row; locators appear as run-local candidate output, not a reusable map | Clean |
| Platform inventory drift | Section 2 and Section 21 stop gates forbid | No platform inventory in H-03 or H-04 | Clean |
| ECR field leakage | Section 2, H-09, Section 21, Section 23 non-claims forbid | H-09 uses obligation discharge states, not ECR field values; opening non-claims confirm no ECR records | Clean |
| Cleaning transformation leakage | Section 2 and Section 23 forbid | No normalization, dedupe, clustering, or summarization appears in the captured slices | Clean |
| Judgment leakage | Section 2 and Section 23 forbid | No credibility labels, relevance scores, inclusion/exclusion decisions, or Decision Strength appear anywhere | Clean |
| Scoring / admissibility leakage | H-04 forbids; H-11 requires downstream decision avoidance | H-11 "Downstream decision avoided?" is consistently "Yes" | Clean |
| Tooling design leakage | Section 21 stop gate; Section 22 update rule 7 | H-12 routes all friction to candidates, not designs; H-15 classifies archive friction as `deferred_runtime` without designing it; H-12 closing note is explicit | Clean |
| Proof/backtest calibration leakage | Harness non-claims §23 | Dry run explicitly did NOT read the BT2-04 backtest proof slice; this is the key safeguard | Clean |

**Assessment**: This is one of the strongest areas of both artifacts. The layer boundary discipline is consistent, enforced by multiple non-claim layers, and demonstrated by the active decision to avoid reading the proof slice.

---

## 11. Retrieval / Repo-Map Assessment

**Repo map status**: The repo map (`docs/workflows/orca_repo_map_v0.md`) was modified in the worktree at the time all three primary artifacts were authored. The dry run and harness note this in their source-loading tables. The map's PROPOSED_MAP status means it is not committed at HEAD. Future agents retrieving the repo map from the committed HEAD would see a different map than what was used during authoring.

**Impact on source loading**: The worktree's modified repo map was used for navigation. Any changes made to the map (adding Data Capture packet entries) are visible in the worktree but not committed. This is a retrieval drift risk for agents that open the committed repo map and expect it to point to the new Data Capture artifacts.

**Recommendation**: When the Data Capture artifacts are committed (if separately authorized), update the repo map entry and commit it with the artifacts so navigation pointers remain accurate.

**Untracked artifact risk**: All six primary Data Capture artifacts (obligation contract, source-family architecture, satellite boundary note, harness, charter, dry run) were untracked at the time this review was conducted. This means they are not part of the committed history at b7627d3. A future agent starting from the committed HEAD would not find these artifacts without the worktree or an explicit dirty-state allowance. This is a disclosure, not a blocker (the review task allows dirty state), but it means the review itself is based on worktree-visible artifacts that may not persist.

---

## 12. Required Patches

### Patches Required Before Next Dry Run

| ID | Target artifact | Summary | Severity |
| --- | --- | --- | --- |
| H-P2-01 | Harness, H-04 template | Update discard vocabulary from `post_window_for_current_commission` to `post_cutoff_for_at_cutoff_use`; reconcile with dry-run vocabulary; add H-00 change-log row | P2 |
| H-P2-02 | Harness, H-09 template | Add rollup condition note aligned with obligation contract; require per-slice sub-rows or explicit cross-reference to H-07 when archive/timing states differ | P2 |
| D-P2-01 | Dry run, H-05 CS-08 | Flag CS-08 raw observable as paraphrase-only; add recapture note for direct source-language excerpt supplement | P2 |
| D-P2-02 | Dry run, H-09 | Add per-slice sub-rows for archive/historical posture and decomposed timing obligation states | P2 |

### Optional Clarifications

| ID | Target artifact | Summary | Severity |
| --- | --- | --- | --- |
| D-P3-01 | Dry run, H-04 opening note | Add note that `post_cutoff_for_at_cutoff_use` replaces harness template's `post_window_for_current_commission`; log in H-13 as vocabulary extension candidate | P3 |
| D-P3-02 | Dry run, H-04 social/threaded row | Clarify `boundary_violating` is used as precautionary uncertain-boundary stop, not confirmed-violation label | P3 |
| H-P3-01 | Harness, section numbering | Normalize section numbers so H-15 flows into stop gates; update dry run cross-references | P3 |
| D-P3-03 | Dry run, retrieval header | Add `input_hashes` for harness, obligation contract, and charter (with untracked file note) | P3 |
| D-P3-04 | Dry run, H-02 and H-06 | Add UTC equivalent for session timestamp; note within-session relative order is unrecorded | P3 |

---

## 13. Deferred Issues

| Issue | Why deferred | When to reconsider |
| --- | --- | --- |
| Minimum raw observable standard for media/analysis sources in H-05 harness template | Single dry run; CS-08 is the only media slice; not enough pressure for core law | After second dry run with a media/analysis source slice |
| `boundary_uncertain_stop` as a new harness discard category | Single-run boundary pressure; not enough for core | After second dry run with professional/social/threaded candidates |
| `post_cutoff_negative_space_guard` promotion to satellite guidance | Single-run pressure; may be backtest-specific | After second dry run on a cutoff-date commissioned frame |
| Archive/history access check for deferred-runtime friction (H-15) | Correctly deferred; tooling not authorized | When a later owner instruction authorizes bounded runtime scope |
| Snapshot Integrity Class / archive attempt threshold | Open design knob in obligation contract; untouched by this dry run | After obligation contract pressure-test revision |

---

## 14. Things Explicitly Not Found

The following were assessed and not found to be defects:

- Fake capture success: the obligation ledger uses genuine `partial` states with visible limitations; no optimistic `met` without evidence.
- ECR-by-stealth in captured source slices: no ECR field values, record IDs, schema keys, or storage references appear.
- Cleaning-by-stealth: no normalization, dedupe, clustering, or summarization appears.
- Judgment-by-stealth: no credibility labels, relevance scores, or inclusion/exclusion decisions appear.
- Tooling design: H-12 friction entries are correctly routed to candidates, not tool specifications.
- Proof/backtest contamination: the dry run actively avoided reading the proof slice.
- Source-map drift: locators appear as run-local output under obligation discharge, not as a reusable inventory.
- Overpromotion to core: H-15 correctly classifies all candidates as run-local, satellite, or deferred-runtime.
- Public/social dossier risk: threaded/social candidates were not captured; the boundary stop is visible and correctly logged.
- Hidden post-cutoff leakage: CS-04 and CS-05 are marked `mixed` with explicit post-cutoff isolation notes; post-cutoff candidates are logged as negative space.

---

## 15. Final Non-Claims

This review does not claim:

- Data Capture is complete.
- The obligation contract is validated or hardened.
- The harness is formally validated by this run.
- BT2-04 proves product readiness, buyer proof, or commercial readiness.
- ECR, Cleaning, Judgment, or any downstream layer is ready.
- Any source captured in BT2-04 is valid, credible, admissible, or decision-useful.
- Any source map, scraper, API, storage, dashboard, automation, test, deployment, package, or runtime should be built.
- Source-of-truth promotion for any artifact reviewed here.
- Data Capture closure.
- Another dry run is authorized.
- The harness patches identified above may be applied without separate patch execution authority.
