# Adversarial Artifact Review: Data Capture Spine Source Observability Requirements Boundary Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review report
scope: Source-backed adversarial review of the source-observability requirements boundary decision after Slot 3 recapture, covering RQ classification correctness, boundary control, direction-change propagation receipt adequacy, and Validation Readback scope.
use_when:
  - Deciding whether the requirements boundary decision is safe for use as current requirements context.
  - Checking whether any blocking or major finding requires remediation before the artifact is used to route implementation scoping or further requirements narrowing.
authority_boundary: retrieval_only
```

## Review Metadata

```text
review_date: 2026-06-02
review_lane: adversarial-artifact-review (Orca overlay § review-lanes.md)
output_mode: filesystem-output
required_output_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_source_observability_requirements_boundary_decision_adversarial_artifact_review_v0.md
edit_permission: read-only (reviewer writes this report only; no edits to reviewed artifacts)
commission: Source-backed adversarial review of Data Capture Spine Source Observability Requirements Boundary Decision v0 after Slot 3 recapture
```

---

## Workspace Preflight

```text
orca_start_preflight:
  agents_read: yes — AGENTS.md read (hash verified)
  overlay_read: yes — .agents/workflow-overlay/README.md read (hash verified)
  skills_loaded:
    - workflow-deep-thinking: loaded and applied; discipline applied before finding enumeration
    - workflow-adversarial-artifact-review: loaded and applied as the operating review method
  source_pack: custom requirements-boundary decision review pack (11 files read)
  edit_permission: read-only; report write to docs/review-outputs/adversarial-artifact-reviews/ only
  target_scope: docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md
  dirty_state_checked: yes — working tree dirty; allowed dirty state declared in review prompt; see dirty-source ledger below
  blocked_if_missing: none of the required source files were missing
```

---

## Hash Verification Ledger

All hashes computed with `Get-FileHash -Algorithm SHA256` immediately before this review.

### Primary Review Target

| File | Expected | Computed | Status |
| --- | --- | --- | --- |
| `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md` | `C8DABF051B03EEEB4B9AD30A459DD38D9AA16FACDA2621E5BEFEDA5EF76D059A` | `C8DABF051B03EEEB4B9AD30A459DD38D9AA16FACDA2621E5BEFEDA5EF76D059A` | ✅ MATCH |

### Propagation Surfaces

| File | Expected | Computed | Status |
| --- | --- | --- | --- |
| `AGENTS.md` | `5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1` | `5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1` | ✅ MATCH |
| `.agents/workflow-overlay/README.md` | `40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F` | `40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F` | ✅ MATCH |
| `.agents/workflow-overlay/source-of-truth.md` | `57C9A6A457A80E0BB66771B3F1B67BD7994CEB9763F0D5D08076061A9921327A` | `57C9A6A457A80E0BB66771B3F1B67BD7994CEB9763F0D5D08076061A9921327A` | ✅ MATCH |
| `.agents/workflow-overlay/source-loading.md` | `D584146C7D9E3DBB5E6C65DC1699C1376A22CF87C70136A8F048D9F7969C3E0B` | `D584146C7D9E3DBB5E6C65DC1699C1376A22CF87C70136A8F048D9F7969C3E0B` | ✅ MATCH |
| `.agents/workflow-overlay/retrieval-metadata.md` | `8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F` | `8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F` | ✅ MATCH |
| `docs/workflows/orca_repo_map_v0.md` | `735C87F70B443945E07138743610C2A166E865A235086585892BDEB05D174040` | `735C87F70B443945E07138743610C2A166E865A235086585892BDEB05D174040` | ✅ MATCH |

### Source-Basis Files

| File | Expected | Computed | Status |
| --- | --- | --- | --- |
| `docs/decisions/data_capture_spine_post_slot3_recapture_delta_lane_local_acceptance_decision_v0.md` | `B4CC4B916CBC35CCDF853650A6F7C4220AF622123D8BD773CF01CED096134E2A` | `B4CC4B916CBC35CCDF853650A6F7C4220AF622123D8BD773CF01CED096134E2A` | ✅ MATCH |
| `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md` | `43B7903ED3A173A17CC8C9C71780F43158744932A3BF5A72B9C3178F4F4DB302` | `43B7903ED3A173A17CC8C9C71780F43158744932A3BF5A72B9C3178F4F4DB302` | ✅ MATCH |
| `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md` | `B242238DA1F456949F858115E7E7B7ACF31BD01BEA38D3CC3FEE98BCD4B55625` | `B242238DA1F456949F858115E7E7B7ACF31BD01BEA38D3CC3FEE98BCD4B55625` | ✅ MATCH |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_slot3_recapture_delta_adversarial_artifact_review_v0.md` | `C2E894C91ED787D7879579EAA35DF03006F97739F20DE43AC348274D9BB7D544` | `C2E894C91ED787D7879579EAA35DF03006F97739F20DE43AC348274D9BB7D544` | ✅ MATCH |

**Hash mismatch ledger**: None. All eleven files verified at expected hashes.

---

## Dirty-Source Ledger

Per `git status --short` at review start, the following controlling or source-basis files have modified or untracked status.

| Source | Git status | Role in this review | Impact on advisory findings |
| --- | --- | --- | --- |
| `AGENTS.md` | `M` modified | Agent operating boundary | Advisory only; hash verified; no finding depends solely on this |
| `.agents/workflow-overlay/README.md` | `M` modified | Overlay entrypoint | Advisory only; hash verified |
| `.agents/workflow-overlay/source-of-truth.md` | `M` modified | Source hierarchy and propagation contract | Advisory only; hash verified; substantive content relied on is present |
| `.agents/workflow-overlay/source-loading.md` | `M` modified | Source-loading budgets and read packs | Advisory only; hash verified; propagation target content confirmed present |
| `docs/workflows/orca_repo_map_v0.md` | `M` modified | Navigation map | Advisory only; hash verified; propagation target entry confirmed present |
| Primary review target | `??` untracked | Review subject | Allowed per dirty-state allowance; hash verified at expected value |
| All source-basis files | `??` untracked | Decision inputs | Allowed per dirty-state allowance; all hashes verified |
| `.agents/workflow-overlay/retrieval-metadata.md` | clean (not in git status) | Retrieval header contract | Clean; hash verified |

Dirty-state allowance declared in review prompt covers all M and ?? files above. All hashes match expected values.

Strict-authority finding note: dirty sources may support advisory work; strict claims about source-of-truth status, validation, readiness, or proof remain `not proven` unless controlling authority accepts them. No strict-required claims are attempted in this review.

---

## Method Application Notes

### `workflow-deep-thinking` — Applied

Using `workflow-deep-thinking`.

**Real question framed before finding enumeration**: Does the requirements boundary decision correctly classify RQ-01 through RQ-05 after Slot 3 recapture, hold appropriate non-implementation and boundary limits, correctly complete the direction-change propagation receipt, and do so without internal contradictions — specifically, does any surface create a hidden bypass path toward source-access expansion or implementation authorization?

**Failure modes checked adversarially before listing findings**:

**FM-A: Target treats delta as governing doctrine rather than decision input.** Check: The "Current Input Versus Stale Candidate Context" section says: "The accepted post-Slot-3-recapture delta is the current input for this decision." It does not elevate the delta to doctrine. The source-of-truth hierarchy is unchanged. The lane-local acceptance decision established this exact input-only relationship; the target faithfully adopts it. Not a finding.

**FM-B: Older scoping artifact is misrepresented — either falsely retired or falsely elevated.** Check: The target says the old scoping artifact "is stale as a standalone current basis" but "remains valid candidate context for RQ-01 through RQ-05." The "Current Use Of Prior Scoping Artifact" section provides explicit permitted and prohibited uses. This treatment is accurate and well-bounded. Not a finding.

**FM-C: RQ-01 carry-forward is overbroad or changes the source-basis requirement.** Check: The original scoping artifact's RQ-01 says preserve "enough source language and visible source structure for a later reader to inspect what the source actually said and how the source presented it, when language or structure carries decision-relevant meaning." The target's formulation says "capture must preserve enough source language and visible source structure, or visibly record the limitation, when the source surface or Decision Frame makes language/structure part of the observable source state." Two changes: (1) adds "or visibly record the limitation" — a refinement, not an expansion; (2) introduces "Decision Frame" as a capitalized, undefined qualifying term. The first change is appropriate. The second change introduces ambiguity because "Decision Frame" is capitalized but not defined in the artifact or traced to any source-basis file. This is a finding — AR-SB-02 below.

**FM-D: RQ-02 split is incorrect or one side is unsupported.** Check: The delta's Support Threshold Checkpoint classified archive requirements as `support_now_for_visibility_requirement` (near-term) / `support_later_for_body-retrieval_default` (deferred pending source-family scoping). The target's `modify_split` classification is: "Carry forward archive availability, archive-body retrieval state, and non-retrieval reason visibility now. Defer any default requirement that archived body content must be retrieved before categorical handoff; that default needs source-family scoping or a later owner decision." This faithfully implements the split from the delta's Support Threshold. Not a finding.

**FM-E: RQ-03 carry-forward smuggles a media pipeline or universal screenshot mandate.** Check: The target says "media, screenshots, layout, gallery assets, charts, images, or app-page presentation must be preserved or limitation-visible when they carry source meaning. This is not a universal screenshot or media mandate." The scoping artifact's RQ-03 non-goals explicitly excluded: "no universal full-page screenshot rule; no image OCR/transcription pipeline; no computer-vision or media-processing method." The target's formulation adds "or limitation-visible" as the alternative to full preservation, narrowing rather than expanding scope. The explicit "This is not a universal screenshot or media mandate" sentence in the RQ table closes the bypass. Not a finding.

**FM-F: RQ-04 deferral is undercut by the Requirements Boundary section.** Check: The RQ table classifies RQ-04 as `defer_with_visible_candidate_status`. The Boundary Guards section reinforces: "This decision does not authorize source-access expansion. RQ-04 remains deferred because source-access handling could otherwise collapse into method selection." However, the Requirements Boundary section lists "explicit access-failure posture where encountered, without changing the source-access boundary" as part of the current bounded requirements context. This creates a tension: a future reader consulting only the Requirements Boundary section could treat access-failure posture documentation as a current bounded obligation equal to the RQ-01/RQ-03/RQ-05 items — contrary to RQ-04's deferral. This is a finding — AR-SB-01 below.

**FM-G: Over-authorization is present anywhere in the artifact.** Check: Non-Claims, Boundary Guards, and "Next Allowed Decision" sections reviewed. Non-Claims section is comprehensive and excludes the full list of forbidden authorizations. Boundary Guards explicitly prohibit source-access expansion, tooling, ECR schema, Cleaning, Judgment, contract hardening, and method-plan amendment. Next Allowed Decision routes only to non-implementation scoping, narrowing, prioritization, or more pressure tests, with explicit separate-authorization requirement for implementation or source-action. The Spec-Writing Gate section does not claim spec was run — it records a scoped route was used and why a separate spec was not needed. No operative over-authorization found.

**FM-H: Direction-change propagation trigger is wrong.** Check: The trigger `product_doctrine` is used. The change propagated is: "The current Data Capture Source Observability requirements boundary is now post-Slot-3-recapture: RQ-01, RQ-03, and RQ-05 carry forward; RQ-02 is split; RQ-04 is deferred candidate context." This is a product requirements boundary update, which maps to `product_doctrine`. The other triggers (`architecture_doctrine`, `lifecycle_boundary`, `workflow_authority`, `validation_philosophy`, `review_authority`, `output_authority`) are not the right category for a requirements classification decision. The split of RQ-02 has a deferral dimension but this does not rise to `lifecycle_boundary`. `product_doctrine` is the correct trigger.

**FM-I: Downstream updates (source-loading.md and repo-map) are insufficient or misaligned.** Check: Source-loading.md (hash verified) includes: "The post-Slot-3-recapture requirements-boundary decision is the current source for RQ status after recapture: RQ-01, RQ-03, and RQ-05 carry forward; RQ-02 is split into visibility-now/body-retrieval-default-deferred; RQ-04 remains deferred candidate context." The decision artifact path and the RQ classifications are correctly recorded. The repo-map (hash verified) entry for this decision reads: "Current post-Slot-3-recapture Source Observability requirements boundary decision: RQ-01/RQ-03/RQ-05 carry forward, RQ-02 is split, RQ-04 remains deferred candidate context; not implementation or source-access method authority." Both updates are aligned with the artifact's claims. Not a finding.

**FM-J: Intentionally-not-updated surfaces are unjustified.** Check:
- AGENTS.md: reason given is "No agent-wide behavior rule changed." Correct — AGENTS.md governs agent operating behavior, not Data Capture requirements boundaries.
- README.md: reason given is "Overlay entrypoint and binding rule unchanged." Correct.
- source-of-truth.md: reason given is "Doctrine-change propagation mechanics unchanged." Correct — only the product requirements classification changed, not the propagation contract itself.
- Old scoping artifact: reason given is "Left intact as historical candidate context; this decision records its stale-alone status instead of rewriting its source basis." Correct and appropriate — rewriting the old artifact would remove its value as historical candidate context.
All justifications are sound. Not a finding.

**FM-K: Validation Readback overclaims.** Check: The Validation Readback records five observed checks (fresh readback, SHA256 computation, over-authorization scan, stale Slot 3 scan, git diff --check) and four observed result sets. The closing line is: "This validation readback is not validation, readiness, acceptance, source promotion, or implementation authorization." The checks described are consistent with the results reported. The artifact's self-reported hash during validation (`34A39FA79FFB6B384CAACC5B45BBBF0E84CB6D20223E68C3B86C78841D449131`) is explicitly identified as the pre-validation-section state; the current hash differs because the Validation Readback section was added afterward, which is expected and disclosed. The source-loading.md and repo-map hashes in the readback match the independently computed values in this review. No overclaim. Not a finding.

**FM-L: `open_next` in the retrieval header routes future agents to the stale scoping artifact without warning.** Check: The header's `open_next` includes `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md` without a stale qualifier. The body's "Current Use Of Prior Scoping Artifact" section provides full permitted/prohibited use guidance, and both source-loading.md and repo-map refer to this decision as the current source for RQ status. A future agent doing only header-level routing could follow `open_next` to the scoping artifact without the stale-alone warning. This is advisory friction — the protocol says `open_next` is conditional, and body guidance is clear, but the risk of header-first agents is real. Finding AR-SB-03 below.

**High-risk verification pass applied**: FM-F and FM-C were the most load-bearing failure modes for boundary control. FM-F confirmed a real but minor internal tension. FM-C confirmed the "Decision Frame" term is a genuine ambiguity that could narrow RQ-01's scope in future use. No failure mode elevated to blocking.

---

### `workflow-adversarial-artifact-review` — Applied

Lane: adversarial-artifact-review.
Claim level: advisory findings from repo-visible evidence and source-basis files. Strict-required claims are not needed; target carries `authority_boundary: retrieval_only`.
Output mode: filesystem-output at the required output path above.
Patch queues: not authorized. No patch queue entries emitted.
Review scope: correctness and friction findings ordered by severity.
Lane collision: no collision — this is a non-code product decision artifact, not implementation code, installed-copy behavior, or a postmortem subject.
Trigger gate: satisfied by explicit adversarial artifact review commission in the review prompt.

---

## Source-Read Ledger

| Source | Why read | What claim or decision it supports | Status |
| --- | --- | --- | --- |
| `AGENTS.md` | Required method sequence | Agent operating boundary, read-only discipline | M (dirty, advisory only); hash verified |
| `.agents/workflow-overlay/README.md` | Required method sequence | Overlay entrypoint and binding rule | M (dirty, advisory only); hash verified |
| `.agents/workflow-overlay/source-of-truth.md` | Required method sequence; propagation contract | Direction-change propagation receipt check; trigger vocabulary | M (dirty, advisory only); hash verified |
| `.agents/workflow-overlay/source-loading.md` | Propagation surface; read pack check | Confirms propagation target entry and RQ classification language | M (dirty, advisory only); hash verified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | Check for triggered fields, forbidden fields | Clean; hash verified |
| `docs/workflows/orca_repo_map_v0.md` | Propagation surface; navigation | Confirms repo-map entry for decision artifact | M (dirty, advisory only); hash verified |
| Review target: `...requirements_boundary_decision_v0.md` | Primary review target | All findings in this review | Hash verified: MATCH |
| `...post_slot3_recapture_delta_lane_local_acceptance_decision_v0.md` | Source basis; input authorization | Verifies delta is correctly treated as input, not basis; confirms accepted scope | Hash verified: MATCH |
| `...all_slot_synthesis_post_slot3_recapture_delta_v0.md` | Source basis; RQ-01 through RQ-05 classification support | Delta's support threshold classifications vs. target RQ table | Hash verified: MATCH |
| `...source_observability_requirements_scoping_v0.md` | Source basis; candidate RQ wording | RQ-01 through RQ-05 original formulations; stale-alone status check | Hash verified: MATCH |
| `...data_capture_spine_post_slot3_recapture_delta_adversarial_artifact_review_v0.md` | Source basis; upstream review | Delta review recommendation and findings; baseline for input confidence | Hash verified: MATCH |

---

## Review Question Responses (Matrix)

Summary answers before full findings. Supporting evidence in the findings sections below.

| Question | Short answer | Finding IDs |
| --- | --- | --- |
| 1. Target correctly treats delta as current lane-local input, not governing doctrine? | Yes — faithfully implemented | No finding |
| 2. Older scoping artifact correctly classified as stale-alone while preserved as candidate context? | Yes — accurate and well-bounded | No finding |
| 3. RQ-01, RQ-03, RQ-05 correctly carried forward? | Yes, with minor ambiguity in RQ-01 formulation | AR-SB-02 |
| 4. RQ-02 correctly split into visibility-now and archive-body-default-deferred? | Yes — faithful to delta's split classification | No finding |
| 5. RQ-04 correctly deferred without changing source-access boundary? | Yes at the RQ table level; internal tension in Requirements Boundary section | AR-SB-01 |
| 6. Artifact avoids implementation, tooling, API, scraper, method-plan, contract, ECR, Cleaning, Judgment, validation, readiness, buyer-proof, and commercial-readiness authorization? | Yes — no operative over-authorization found | No finding |
| 7a. `product_doctrine` the right trigger? | Yes | No finding |
| 7b. source-loading.md and repo-map sufficient downstream updates? | Yes — both entries verified and aligned | No finding |
| 7c. Intentionally-not-updated surfaces justified? | Yes — all four justifications are sound | No finding |
| 8. Source-loading and repo-map edits help agents without making old scoping artifact governing doctrine? | Yes; slight friction from open_next without stale qualifier | AR-SB-03 |
| 9. Validation Readback overclaims? | No — non-claim is correctly stated; observed facts are accurate | No finding |
| 10. Hidden contradiction between "requirements boundary" and "not implementation/source-action authorization"? | Partial tension in Requirements Boundary section for RQ-04 | AR-SB-01 |

---

## Phase 1 — Correctness Findings

### Finding AR-SB-01 — Minor: RQ-04 deferral and Requirements Boundary section are in tension

**Finding ID:** AR-SB-01
**Phase:** correctness
**Severity:** minor
**Artifact location:** Review target — "RQ Classification" table (RQ-04 row) and "Requirements Boundary" section (fifth bullet); also "Boundary Guards" section

**Source evidence:**
- Target RQ table, RQ-04 row: `defer_with_visible_candidate_status` — "Current evidence keeps access failure handling visible, especially from Slot 2 and bounded WSO limits, but does not change source-access boundary or authorize source-access method-plan amendment."
- Target Boundary Guards: "This decision does not authorize source-access expansion. `RQ-04` remains deferred because source-access handling could otherwise collapse into method selection. The current hard line remains outside this artifact."
- Target Requirements Boundary section lists as current bounded context: "explicit access-failure posture where encountered, without changing the source-access boundary."
- Source basis — delta's Support Threshold Checkpoint, RQ-04 row: `support_later_after_more_evidence_or_owner_priority` — "No bypass, proxy, anti-detect, no-entitlement gate bypass, API default, entitlement-policy change, or source-access boundary change."
- Source basis — scoping artifact RQ-04: Evidence-weight note warns this "is retained from a single-slot severity signal, not a cross-slot count threshold."

**Issue:** The RQ Classification table classifies RQ-04 as deferred, and the Boundary Guards section reinforces the deferral with explicit rationale. However, the Requirements Boundary section — which purports to describe the current bounded Source Observability requirements context — includes "explicit access-failure posture where encountered, without changing the source-access boundary" as one of its five bullets. The other four bullets map directly to the carried-forward requirements (RQ-01, RQ-05, RQ-03, and the visibility half of RQ-02). This fifth bullet reads as a current bounded requirement alongside those, despite RQ-04 being deferred.

The artifact does not explain why a deferred RQ contributes a current bounded requirement bullet. The most likely intent is that the bullet represents only the "visible candidate status" portion of the deferral — i.e., access-failure posture should remain observable in captures as a matter of existing practice, but no new formal requirement is established. However, this distinction is absent from the Requirements Boundary section itself.

**Impact:** A future agent preparing implementation scoping, further requirements narrowing, or a requirements readback using the Requirements Boundary section as its operative surface might treat "explicit access-failure posture where encountered" as a current bounded obligation on equal footing with RQ-01, RQ-03, and RQ-05 carried-forward requirements. This could create premature scope expansion toward source-access handling, which is exactly the boundary failure the RQ-04 deferral and boundary guards are designed to prevent. The Boundary Guards partially mitigate this, but the section structure creates an ambiguous reading.

**Minimum closure condition:** Owner should decide one of:
(a) Remove the fifth bullet from the Requirements Boundary section (since RQ-04 is deferred, no new bounded requirement exists);
(b) Qualify the bullet to read: "explicit access-failure posture where already practiced, reflecting the deferred candidate status of RQ-04 rather than a current bounded requirement"; or
(c) Add a parenthetical note in the Requirements Boundary section pointing to the RQ-04 row's deferral classification.

Resolving this removes the most likely misreading path for future implementation scoping agents.

**Patch queue:** Not overlay-authorized. Advisory only.
**Strict claims not proven:** This is an internal consistency issue, not a factual error. The Boundary Guards clearly state the deferral; the Requirements Boundary section does not.
**Next authorized action:** Owner decision on wording clarification before the artifact is used as input to implementation scoping authorization.

---

### Finding AR-SB-02 — Minor: RQ-01 carried-forward formulation introduces undefined "Decision Frame" term

**Finding ID:** AR-SB-02
**Phase:** correctness
**Severity:** minor
**Artifact location:** Review target — "RQ Classification" table, RQ-01 row: "capture must preserve enough source language and visible source structure, or visibly record the limitation, when the source surface or **Decision Frame** makes language/structure part of the observable source state."

**Source evidence:**
- Target RQ-01 carried-forward formulation: includes "or Decision Frame" as a qualifying condition.
- Source basis — scoping artifact RQ-01 candidate requirement: "when language or structure carries decision-relevant meaning." No capitalization; no "Decision Frame" term.
- Source basis — delta Support Threshold Checkpoint, source-language/structure row: "Support means deciding the requirements boundary, not building a recorder, schema, ranking rule, or Judgment selection policy." No "Decision Frame" term.
- Source basis — delta Cross-Slot Pattern table, source-language row: "Slot 1 preserved pricing and bundle facts through paraphrase/reorganized renderings but not exact source wording, layout, table placement, nesting, or packaging cues." No "Decision Frame" term.
- None of the eleven files in the source-read ledger define "Decision Frame" in the Data Capture or source-observability context.
- "Decision Frame" as a capitalized term appears in the Orca consulting-judgment corpus and Judgment Spine, where it refers to a specific artifact type representing the framing context for a judgment case. That usage is from the Judgment Spine, not the Data Capture Spine.

**Issue:** "Decision Frame" is capitalized, suggesting a specific Orca artifact type. If the intent is to refer to the Judgment Spine's Decision Frame artifact type, then the RQ-01 requirement applies only when a source surface or a Decision Frame artifact makes language/structure observable — a narrow scope that would exclude many Data Capture contexts that do not produce Decision Frame artifacts. This would be significantly more restrictive than the scoping artifact's "when language or structure carries decision-relevant meaning."

If "Decision Frame" is used generically to mean "the framing of a decision context," then the capitalization is misleading and may cause a future reader to import the Judgment Spine meaning.

Either reading creates a scope inconsistency: the scoping artifact's RQ-01 applied to any capture surface where language/structure carries meaning; the target's formulation adds a qualifier that depends on interpretation of an undefined term.

**Impact:** Future agents using RQ-01 as requirements context for implementation scoping, further narrowing, or prompt setup may apply a narrower or different scope than the owner intended, depending on how they interpret "Decision Frame." Specifically, a reader familiar with the Judgment Spine might restrict RQ-01 to Decision Frame-producing workflows, inadvertently narrowing the source-observability requirement for Data Capture fixtures that do not produce Decision Frames.

**Minimum closure condition:** Either (a) replace "Decision Frame" with the non-capitalized original scope formulation ("when language or structure carries decision-relevant meaning"), or (b) add a footnote or inline clarification defining what "Decision Frame" means in this RQ-01 context to prevent cross-spine terminology contamination.

**Patch queue:** Not overlay-authorized. Advisory only.
**Strict claims not proven:** Whether "Decision Frame" is intentionally narrowing is not proven; it may be a non-technical use of the phrase. The issue is the ambiguity, not a proven intent.
**Next authorized action:** Owner decision on wording before the RQ-01 formulation is used as input to implementation scoping.

---

### RQ-01, RQ-03, RQ-05 carry-forward — No additional correctness findings

The carried-forward classifications for RQ-03 and RQ-05 are accurate:

- **RQ-03 `carry_forward_modified`**: The target formulation adds "or limitation-visible" as an alternative to full preservation, which is a narrowing refinement consistent with the scoping artifact's approach and the delta's support threshold. The "not a universal screenshot or media mandate" sentence closes the expansion bypass. The modality-trigger scope matches the delta's classification rationale. No additional finding.

- **RQ-05 `carry_forward`**: The formulation retains the forum/review/text-heavy discourse scope and the source-language-anchor requirements from the scoping artifact. No new terminology introduced. Consistent with the delta's `support_now_for_non-implementation_requirements_decision` classification. No additional finding.

---

### RQ-02 split — No correctness finding

The `modify_split` classification faithfully implements the delta's `support_now_for_visibility_requirement` / `support_later_for_body-retrieval_default` split. The near-term side (archive availability, retrieval state, non-retrieval reason visibility) and the deferred side (default requirement for archived body retrieval before categorical handoff, pending source-family scoping or later owner decision) are clearly separated. The deferral rationale ("needs source-family scoping or a later owner decision") is appropriate given the delta's evidence. No finding.

---

### Direction-change propagation receipt — No correctness finding

The receipt uses `product_doctrine` as trigger. This is the correct trigger for a Data Capture product requirements classification decision that establishes which candidate requirements survive as bounded context after recapture. The alternative triggers (`architecture_doctrine`, `lifecycle_boundary`, `workflow_authority`, `validation_philosophy`, `review_authority`, `output_authority`) are not applicable: no architecture changed, no lifecycle boundary was moved, and no workflow, validation, review, or output authority rule changed.

`controlling_sources_updated` lists three entries (the decision artifact, source-loading.md, and repo-map), which matches the actual changes made. Both downstream update targets were independently verified at expected hashes with correct content. No additional propagation surface omissions identified: AGENTS.md, overlay README, source-of-truth.md, and the old scoping artifact are appropriately in the `intentionally_not_updated` list with sound justifications for each.

No correctness finding on the propagation receipt.

---

### Validation Readback — No correctness finding

The Validation Readback reports five checks (fresh readback, SHA256 computation, over-authorization scan, stale Slot 3 scan, git diff --check) and their observed results. The source-loading.md and repo-map hashes reported in the readback match the hashes independently computed in this review. The artifact's pre-validation-section hash (`34A39FA79FFB6B384CAACC5B45BBBF0E84CB6D20223E68C3B86C78841D449131`) is the expected intermediate state before the Validation Readback section was added; the current hash (`C8DABF051B03EEEB4B9AD30A459DD38D9AA16FACDA2621E5BEFEDA5EF76D059A`) reflects the full published artifact. The readback's closing non-claim is correct: "This validation readback is not validation, readiness, acceptance, source promotion, or implementation authorization." No overclaim present.

---

## Phase 2 — Friction Findings

### Finding AR-SB-03 — Advisory: `open_next` lists the stale scoping artifact without a stale qualifier

**Finding ID:** AR-SB-03
**Phase:** friction
**Severity:** advisory
**Artifact location:** Review target — retrieval header, `open_next` field: `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md`

**Source evidence:**
- Target retrieval header: `open_next` includes `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md` and `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md` and `.agents/workflow-overlay/source-loading.md`.
- Target body, "Current Input Versus Stale Candidate Context": the old scoping artifact "is stale as a standalone current basis" and "future agents should not use it without this decision or a later superseding decision."
- Target body, "Current Use Of Prior Scoping Artifact": provides explicit permitted and prohibited uses.
- Source-loading.md (verified): names the decision artifact as the current source for RQ status; does not explicitly warn that the scoping artifact is stale-alone without this decision.
- Retrieval-metadata.md rule: "`open_next`: use it when one or more controlling sources should be opened after this artifact."

**Issue:** The `open_next` field is the primary header-level discovery surface for future agents. Listing the old scoping artifact in `open_next` without any qualifier means a header-first agent following `open_next` will find the scoping artifact as a recommended next read — with no indication at the header level that it is stale-alone without the present decision. The body provides full, clear guidance, but the header does not.

The retrieval-metadata.md contract says `open_next` should be used "when one or more controlling sources should be opened after this artifact." The scoping artifact is candidate context, not a controlling source — listing it in `open_next` slightly overstates its role at the header level.

**Impact:** Minimal, given the protocol that `open_next` is conditional ("open it only when it can change the current task") and the body's "Current Use Of Prior Scoping Artifact" section is clear. The risk materializes only if a future agent follows header-only discovery and reaches the scoping artifact before reading the decision body. The source-loading.md and repo-map updates mitigate this further by pointing to the decision artifact as the current RQ-status source.

**Minimum closure condition:** None required. Advisory friction observation. If the owner finds this notable, consider relabeling `open_next` entries to separate controlling sources from candidate context, or add an inline note that the scoping artifact is candidate context only and stale-alone.

**Patch queue:** Not overlay-authorized. Advisory prose only.
**Next authorized action:** No action required. Record only.

---

## Summary of All Findings

| ID | Phase | Severity | Short description |
| --- | --- | --- | --- |
| AR-SB-01 | Correctness | Minor | Tension between RQ-04 `defer_with_visible_candidate_status` classification and access-failure posture bullet in Requirements Boundary section; may read as a current bounded obligation |
| AR-SB-02 | Correctness | Minor | RQ-01 carry-forward introduces capitalized "Decision Frame" as an undefined qualifier; may unintentionally narrow scope to Judgment Spine artifact contexts |
| AR-SB-03 | Friction | Advisory | `open_next` in retrieval header lists the stale scoping artifact without a stale qualifier; header-only agents may miss the stale-alone status |

**Blocking or major findings that prevent owner use**: 0.

**Minor findings (should patch before broader reuse or implementation scoping)**: 2 — AR-SB-01, AR-SB-02.

**Advisory findings**: 1 — AR-SB-03.

---

## Recommendation

`safe_for_owner_use_as_requirements_boundary_basis_with_minor_patches_recommended`

The artifact correctly classifies RQ-01 through RQ-05 after Slot 3 recapture, faithfully implements the delta's support threshold guidance, maintains non-implementation and source-access boundaries, completes a well-formed direction-change propagation receipt, and does not overclaim in the Validation Readback. No blocking or major finding prevents the owner from using this artifact as the current requirements boundary basis.

**Minor patches recommended before use in downstream implementation scoping or requirements-narrowing work:**

1. **AR-SB-01** — Clarify the Requirements Boundary section's access-failure posture bullet to make its deferred status explicit (i.e., it is not a new bounded obligation, only the visible-candidate-status aspect of the deferred RQ-04). This prevents premature scope expansion toward source-access handling during implementation scoping.

2. **AR-SB-02** — Replace "Decision Frame" in the RQ-01 classification with the original scope formulation ("when language or structure carries decision-relevant meaning") or add an explicit definition. This prevents cross-spine terminology confusion during future requirements refinement.

**Advisory (no action required for current owner use):**

- AR-SB-03: Consider qualifying the scoping artifact's `open_next` entry to indicate candidate-context status.

**After minor patches**, the artifact is well-positioned as the current requirements boundary basis for the next bounded content decision.

---

## `next_action`

1. Owner reviews AR-SB-01 and decides whether the Requirements Boundary section's access-failure posture bullet should be qualified or removed to prevent misreading as a current bounded requirement.
2. Owner reviews AR-SB-02 and decides whether "Decision Frame" in the RQ-01 classification should be replaced with the original scope language or given an explicit definition.
3. Owner proceeds with the next bounded content decision per the artifact's "Next Allowed Decision" section: implementation-scoping authorization, requirements narrowing, RQ-04 prioritization decision, or another pressure-test batch.
4. Any route toward implementation or source-action requires separate owner authorization naming that scope.

---

## Non-Claims

This review does not:

- validate, accept, or harden the Data Capture Spine or the requirements boundary decision;
- promote any artifact to source-of-truth status;
- authorize implementation, runtime, scrapers, APIs, dashboards, storage, tests, deployment, commits, or pushes;
- authorize source-access method-plan amendment or obligation-contract amendment;
- authorize ECR design, Cleaning implementation, or Judgment design;
- certify that RQ-01 through RQ-05 are complete, correct, or sufficient for implementation;
- claim the deferred RQ-04 candidate is resolved;
- produce a patch queue;
- constitute buyer proof or commercial-readiness evidence.

---

## Review-Use Boundary

These findings are decision input only. They are not mandatory remediation, approval, validation, or executor-ready patch authority. The minor patches (AR-SB-01, AR-SB-02) are recommendations for owner consideration before the artifact is used as input to implementation scoping or requirements-narrowing work; they are not mandatory before owner use of this artifact as the current requirements boundary basis. Advisory finding AR-SB-03 requires no action.

---

## Compact Courier Summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_source_observability_requirements_boundary_decision_adversarial_artifact_review_v0.md
  recommendation: safe_for_owner_use_as_requirements_boundary_basis_with_minor_patches_recommended
  findings_count: 3
  blocking_or_major_findings: []
  minor_findings:
    - "AR-SB-01 (minor, correctness): Requirements Boundary section includes access-failure posture as current bounded context despite RQ-04 being deferred — may read as current bounded obligation; recommend clarifying or removing the bullet before implementation scoping use."
    - "AR-SB-02 (minor, correctness): RQ-01 carry-forward introduces capitalized 'Decision Frame' as an undefined qualifier; may unintentionally narrow scope to Judgment Spine artifact contexts; recommend replacing with original scope language."
  advisory_findings:
    - "AR-SB-03 (advisory, friction): open_next lists the stale scoping artifact without a stale qualifier; header-only agents may miss the stale-alone status; no action required."
  next_action: >
    Owner reviews AR-SB-01 and AR-SB-02 before routing to implementation scoping.
    No blocking finding. Artifact is the current requirements boundary basis for
    RQ-01 through RQ-05 after Slot 3 recapture. Separate authorization required
    for any implementation, source-action, method-plan amendment, or contract amendment.
```
