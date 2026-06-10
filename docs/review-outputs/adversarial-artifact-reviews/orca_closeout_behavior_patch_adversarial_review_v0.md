# Orca Closeout Behavior Patch Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the Orca closeout-behavior patch that changed file-write chat closeouts toward headed human prose plus artifact receipts, with no YAML by default.
use_when:
  - Checking whether the closeout-behavior patch cleanly implements the owner's no-YAML-default direction.
  - Reviewing findings FF-01 through FF-03 before authorizing patch guidance follow-through.
  - Assessing whether the CA discussion is still useful or risks misleading future agents.
authority_boundary: retrieval_only
input_hashes:
  - path: .agents/workflow-overlay/communication-style.md
    sha256: D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049
  - path: .agents/workflow-overlay/validation-gates.md
    sha256: 0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7
  - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    sha256: CB892EB9ED69E800672C6B32A679517C459C85B17D2C2A6E238D5FBA3015A3B6
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: DFCF2865434CC4405846C0842A4789ACBB787477C64C2B6BCF6D518BB5D2626F
  - path: docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
    sha256: 37E8DFBA790595799354D52ED2875B8A501F103E14E83A2E325A28415AA9620D
downstream_consumers:
  - Closeout-behavior patch cleanup and follow-through.
  - Future Orca prompt-orchestration and shared-behavior-contract patches.
stale_if:
  - Any target file hash changes.
  - Owner changes the accepted no-YAML-default closeout rule.
  - The patch is superseded or reverted.
```

---

## 1. Review Summary

**Recommendation:** `accept_with_friction`

The closeout-behavior patch correctly implements the owner's accepted direction: headed human prose is now the default for substantial decision-bearing file-write closeouts, YAML is not required by default, path/hash/status receipts follow the human summary, and the review-report and paste-ready-chat exceptions are preserved intact. Three advisory findings require follow-through before the patch surface is internally consistent: a wording gap in the shared behavior contract lowers the YAML trigger threshold relative to the overlay; an active CA prompt's Chat Closeout clause also uses a lower threshold; and the CA discussion that drove the patches remains accessible with unremediated stale-if conditions, carrying language that could mislead future agents about YAML obligation. No correctness failures, no overclaims, and no jb imports were found.

---

## 2. Scope And Sources

### Target Files Reviewed

| File | Role | Hash at Review Start | Match |
| --- | --- | --- | --- |
| `.agents/workflow-overlay/communication-style.md` | Orca overlay authority | D93931D9... | ✓ |
| `.agents/workflow-overlay/prompt-orchestration.md` | Orca overlay authority | 54242C83... | ✓ |
| `.agents/workflow-overlay/validation-gates.md` | Orca overlay authority | 0DEBE6EA... | ✓ |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | Prompt template | CB892EB9... | ✓ |
| `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` | Planning handoff prompt | DFCF2865... | ✓ |
| `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` | Workflow record | 37E8DFBA... | ✓ |

All six target hashes match the prompt-creation pins exactly. No mismatches.

Also read: `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/artifact-roles.md`, `.agents/workflow-overlay/artifact-folders.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/template-registry.md`, `.agents/workflow-overlay/retrieval-metadata.md`, `docs/prompts/reviews/orca_closeout_behavior_patch_adversarial_review_prompt_v0.md`.

### Hash Mismatch Status

No mismatches. Review proceeded with full authority.

### Dirty-State Handling

Dirty state was allowed and treated as material per the review prompt. All target files were reviewed in place on branch `main` at HEAD `a873c9c3ed3b289a65f9c472c63e0aadf880a127`. The CA discussion's input hashes are pre-patch for all five overlapping overlay files; this is expected evidence that the patch was applied after the CA discussion was written.

### Deep Thinking

`workflow-deep-thinking` was invoked before formal findings and produced the boundary-problem frame, failure-mode enumeration (FM-1 through FM-5), and decision criteria used in this review.

### Source-Loading Mode

Strict formal review. All required overlay authority was loaded. Artifact roles, review lane, validation gates, and source hierarchy were bound before findings were written.

---

## 3. Decision Contract Under Review

### Accepted No-YAML-Default Closeout Behavior

The owner accepted the following direction:

- For short chat-native output without a durable artifact: use clear headed formatting, slightly less prose. No YAML required.
- For substantial decision-bearing `file-write` artifacts: use a concise headed human summary before the artifact path/hash/status receipt. Do not allow "do not paste the full artifact" to collapse into receipt-only chat.
- YAML is **not required by default**. Use YAML when: the user requests it; an output mode explicitly requires machine-shaped fields; or lane switching / handoff routing would materially benefit from compact courier YAML.

### Preserved Output-Mode Exceptions

These exceptions were explicitly out of scope for the no-YAML-default rule and must survive unchanged:

1. **`review-report` saved-report exception**: YAML-only chat is valid after the required durable report is successfully written. The compact `review_summary` YAML shape is a legitimate courier output for this mode.
2. **`paste-ready-chat` prompt-body exception**: the paste-ready body may be the deliverable; surrounding CA, planning, or routing decisions must still use human-readable chat shape.
3. **Artifact-native tables**: evidence tables, source ledgers, and structured comparisons that are native to the artifact format are not naively rewritten into verbose closeouts.
4. **Source-heavy economy**: compact chat receipts remain valid when the durable artifact carries the human-readable value and no material decision must be understood from chat.

---

## 4. Findings

Findings are ordered by severity and impact on the patch objective.

---

### FF-01 — Shared Behavior Contract YAML Trigger Inconsistency

**Severity:** Advisory

**Location:** `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`, Output Discipline section

**Issue:** The shared behavior contract states:

> "YAML is not required unless the user requests it, the output mode requires machine-shaped fields, or **lane switching / handoff routing benefits from compact courier YAML**."

The three overlay files (`communication-style.md`, `prompt-orchestration.md`, `validation-gates.md`) all use a stronger, consistent phrase:

> "**lane switching / handoff routing would materially benefit from** compact courier YAML"

The shared behavior contract drops "would materially" and says only "benefits from." This is a lower threshold. A future Orca prompt template that includes the shared behavior contract as its governing clause will apply YAML more liberally than a reviewer reading the overlay files intends. The difference is subtle but exploitable: "benefits from" can be satisfied by almost any handoff scenario, while "would materially benefit from" requires judgment that the YAML provides value that prose cannot.

**Evidence:**
- `orca_prompt_behavior_contract_v0.md` line: "lane switching / handoff routing benefits from compact courier YAML"
- `communication-style.md` line: "lane switching / handoff routing would materially benefit from compact courier YAML"
- `prompt-orchestration.md` line: "lane switching / handoff routing would materially benefit from compact courier YAML"
- `validation-gates.md` line: "lane switching / handoff routing would materially benefit from compact courier YAML"

**Impact:** Templates inheriting from the shared behavior contract have a softer YAML guard than the overlay files. In practice this is advisory severity because the shared behavior contract also says "YAML is not required unless..." — the overall direction remains correct. But the inconsistent threshold weakens the patch's precision for any future prompt that relies on the shared contract as its primary authority.

**Recommended Correction:** Align the shared behavior contract's YAML trigger to "would materially benefit from compact courier YAML" to match the three overlay files exactly.

---

### FF-02 — Major-Move CA Prompt Chat Closeout Uses Lower YAML Threshold

**Severity:** Advisory

**Location:** `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`, `## Chat Closeout` section

**Issue:** The Chat Closeout clause now requires a substantive human-readable closeout — this is a correct improvement over the pre-patch receipt-only behavior. However, it specifies YAML as follows:

> "compact courier YAML **when this result is likely to be handed** to another lane, agent, thread, or prompt."

The overlay's YAML threshold is "would materially benefit from compact courier YAML." The phrase "likely to be handed" is a lower bar. A CA prompt producing a folder-integrity decision will almost always produce a result that is *plausibly* going to be handed off somewhere. This clause effectively makes YAML the expected behavior for any CA pass where the next step is not entirely in-thread — which describes most non-trivial CA work.

The overlay does not say YAML when a result is "likely" to continue; it says YAML when lane switching or handoff routing *would materially benefit* from compact carrier state. The difference matters: "materially benefits" requires judgment that YAML adds routing value prose cannot provide; "likely to be handed" is nearly always true for a CA decision artifact.

**Evidence:**
- `orca_major_move_folder_integrity_ca_prompt_v0.md` Chat Closeout: "compact courier YAML when this result is likely to be handed to another lane, agent, thread, or prompt."
- `prompt-orchestration.md` file-write rule: "YAML is not required by default for `file-write` closeouts; use it when ... lane switching / handoff routing would materially benefit from compact courier YAML."

**Impact:** This is an active prompt used for substantial CA file-write work. The lower threshold means a CA agent following this prompt will default to YAML for most CA decisions — which is closer to the pre-patch behavior the owner rejected. The human summary requirement is correctly present, so this is not a receipt-only failure; it is a residual YAML-default risk in an active prompt.

**Recommended Correction:** Replace "when this result is likely to be handed to another lane, agent, thread, or prompt" with "when lane switching, handoff routing, or another agent or thread is expected to continue from this result and compact courier YAML would materially benefit that routing." This aligns the active prompt with the overlay threshold while preserving the intent.

---

### FF-03 — CA Discussion Stale-If Condition Met But Not Flagged

**Severity:** Advisory

**Location:** `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`, retrieval header `stale_if` field

**Issue:** The CA discussion's retrieval header includes this `stale_if` condition:

> "Owner accepts or rejects a file-write closeout summary patch."

That condition has been met. The patch has been applied: all five overlay files the CA discussion pinned have changed. The CA discussion's `HYBRID_PATCH_ROUTE_RECOMMENDED` status is now a historical recommendation, not a pending one.

However, the CA discussion has no update to its status field, no `superseded_by` link, and no note that its `stale_if` condition was triggered. A future agent opening the CA discussion — which is easily discoverable via its `open_next` fields pointing to the patched overlay files, or via search — will encounter:

> "Courier YAML should be **conditionally required** for substantial file-write CA artifacts when lane switching, future prompt handoff, review routing, or another thread/agent is expected to continue from the result."

The phrase "conditionally required" is materially stronger than the current overlay's "would materially benefit." An agent reading the CA discussion as current authority (rather than as historical input) could apply a higher YAML obligation than the overlay intends. The artifact's `authority_boundary: retrieval_only` is the correct defense, but `retrieval_only` does not automatically force agents to check `stale_if` conditions — it merely limits the artifact's authority. Many agents will read the CA discussion's recommendation as the reasoning the overlay was based on, and will weight it accordingly.

**Evidence:**
- CA discussion `stale_if`: "Owner accepts or rejects a file-write closeout summary patch." — this condition was met when the patch was applied.
- CA discussion input hashes for `communication-style.md`: `0D7F72...` — current hash is `D93931...` — changed.
- CA discussion input hashes for `prompt-orchestration.md`: `9E159E...` — current hash is `54242C...` — changed.
- CA discussion input hashes for `validation-gates.md`: `4711210E...` — current hash is `0DEBE6EA...` — changed.
- CA discussion recommendation: "Courier YAML should be **conditionally required**..." — current overlay says "would materially benefit from compact courier YAML" — weaker trigger.

**Impact:** Advisory. The CA discussion cannot override the overlay because `retrieval_only` limits its authority. However, agents with imperfect source-hierarchy discipline may read the CA discussion's reasoning as the operative rule, particularly if they encounter it through `open_next` chains or searches for "file-write" or "closeout." The mismatch between "conditionally required" and "would materially benefit" is real and could subtly push YAML usage back toward what the owner rejected.

**Recommended Correction:** Add a `superseded_by` triggered field in the CA discussion's retrieval header pointing to the patched overlay files, and update the `Status` field from `HYBRID_PATCH_ROUTE_RECOMMENDED` to `HISTORICAL_PATCH_DISCUSSION` or an equivalent note that the patches have been applied and the overlay is now the controlling source. Alternatively, if the CA discussion is retained purely as historical evidence, add a brief note at the top of the document body stating that the stale_if condition has been met and the current rule is in the overlay.

---

## 5. Non-Findings

These risks were checked and did not produce findings.

**NF-01 — review-report YAML-only exception intact.** All four patched files preserve the rule that `review-report` may use YAML-only chat only after the required durable report has been successfully written. `communication-style.md` owns the YAML shapes and failed-write shapes. `prompt-orchestration.md` explicitly states the durable-write precondition for YAML-only chat. `validation-gates.md` includes a comprehensive review-report topology gate covering failed writes, no extra keys, and no claims. The exception is correctly preserved and not weakened.

**NF-02 — paste-ready-chat exception intact.** `prompt-orchestration.md` correctly states that `paste-ready-chat` may prioritize the paste-ready body when that body is the deliverable, and must not hide a Chief Architect, planning, scoping, phase-gate, or completion decision inside machine-only structure. No file contradicts this.

**NF-03 — artifact-native table and source-heavy economy exceptions intact.** `validation-gates.md` explicitly preserves "task-native structured outputs such as evidence tables must not be naively rewritten into verbose closeouts." `prompt-orchestration.md` preserves source-heavy economy through the source-loading unit, compaction-before-seal, and readback-economy gates. Neither was disturbed.

**NF-04 — No overclaims in the patch.** No file in the patch surface contains validation claims, readiness claims, approval claims, lifecycle-completion claims, resolver claims, deployment/install claims, or product-readiness claims. The patched files make behavioral rules, not completion assertions.

**NF-05 — No jb policy imports.** No jb paths, handoff rules, lifecycle mechanics, GAP/CV Engine policy, product-lead rules, or repo-local lifecycle mechanics were found in the patched material.

**NF-06 — Headed human summary requirement is clear and affirmative.** `prompt-orchestration.md` is explicit: "Substantial decision-bearing file writes must close with clear headed human summary first, then path/hash/status receipt." `communication-style.md` says the human-summary-first rule applies to "substantial decision-bearing `file-write` closeouts." The shared behavior contract says "Do not let 'do not paste the full artifact' collapse into path/hash/status-only chat." The receipt-only failure mode from before the patch is blocked at three independent points.

**NF-07 — Review prompt hash pinning coherent.** The review prompt's `input_hashes` pin all six target files at their current (post-patch) hashes. These matched exactly at review start. The CA discussion's input hashes are pre-patch, which is expected — the CA discussion was written before the patch was applied and its hashes record the pre-patch state. No incoherence in pinning.

**NF-08 — Output mode topology gate present.** `validation-gates.md`'s chat-output topology gate correctly functions as a collision gate, not a required-key checklist. It explicitly prohibits adding "extra courier keys or ritual non-claim fields merely to satisfy process metrics." This prevents the gate from being misused to require YAML for compliance rather than routing value.

---

## 6. Stale Or Historical Artifact Risk

**`docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`**

Status assessment: **Stale — historical context only, not current authority.**

The CA discussion was the correct driving artifact for the patch. It correctly identified the ambiguity between receipt-only closeouts and full artifact pasteback, recommended the hybrid patch route, defined the minimum human summary requirement, and scoped YAML as conditional for lane switching. The patched overlay files implement this recommendation.

However, the CA discussion is now stale in three concrete ways:

1. All five overlay files it pinned have changed. Its input hashes are pre-patch.
2. Its `stale_if` condition "Owner accepts or rejects a file-write closeout summary patch" has been met.
3. Its recommendation "Courier YAML should be **conditionally required**" is now superseded by the overlay's "would materially benefit from compact courier YAML" — a weaker, more accurate trigger.

The CA discussion carries useful historical reasoning: the problem frame, the options compared, the recommended closeout contract, and the patch implications remain valid as context for understanding why the overlay was changed. It is not misleading about the primary direction (headed human summary before receipt, no YAML by default). However, its YAML obligation language is stronger than what was ultimately implemented, and it has no explicit marker that its patches have been applied.

**Risk:** Medium. An agent reading the CA discussion's `Recommended Closeout Contract` section for YAML guidance will find "conditionally required" and may apply that as the operative rule rather than reading the overlay's "would materially benefit from." This risk is bounded by `authority_boundary: retrieval_only`, but not eliminated by it.

**Disposition:** Treat as historical. The controlling source for closeout behavior is the current overlay. The CA discussion should be annotated as historical (stale_if triggered, patches applied) but need not be deleted — its problem framing and option comparison remain useful historical context. See Patch Guidance for the minimal correction.

---

## 7. Patch Guidance

Conceptual guidance only. No patch queues. No patch execution authority is granted here. The owner must authorize a patch route before any changes are made.

**PG-01 — Align shared behavior contract YAML trigger**

File: `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Change: In the Output Discipline section, replace "lane switching / handoff routing benefits from compact courier YAML" with "lane switching / handoff routing would materially benefit from compact courier YAML."

This is a one-phrase alignment. It does not change the behavioral direction; it eliminates the threshold gap between the shared contract and the three overlay files.

**PG-02 — Align major-move CA prompt Chat Closeout YAML trigger**

File: `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`

Change: In the `## Chat Closeout` section, replace "compact courier YAML when this result is likely to be handed to another lane, agent, thread, or prompt" with "compact courier YAML when lane switching, handoff routing, or another agent or thread is expected to continue from this result and compact courier YAML would materially benefit that routing."

This preserves the intent of conditional YAML for handoff routing while aligning with the overlay threshold.

**PG-03 — Mark CA discussion as historical**

File: `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`

Change: Add a `superseded_by` field to the retrieval header pointing to the patched overlay files, and update the status field or add a brief note at the top of the document body indicating the stale_if condition has been met and the patch was applied. Example status update: `HISTORICAL_PATCH_DISCUSSION — patches applied; controlling source is the overlay`.

This does not require changing the CA discussion's content. A retrieval header update and a one-line status note are sufficient.

---

## 8. Non-Claims

This review does not claim:

- Approval of the patch.
- Validation that the patch is complete or correct.
- Readiness of any Orca artifact, prompt, or overlay for deployment or production use.
- Lifecycle completion.
- Resolver behavior.
- Install or deployment status.
- Implementation readiness.
- Product readiness.
- Merge safety.
- That any finding constitutes a mandatory remediation order.

Findings are decision input for the owner. Only a separately authorized patch, acceptance, validation, lifecycle, or implementation lane can make remediation mandatory or executor-ready.

---

## 9. Exact Next Authorized Step

Authorize a narrow docs-write patch route targeting `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` (PG-01), `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` (PG-02), and the retrieval header plus status field of `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` (PG-03). No overlay files, no skill files, no commits, no PRs, and no implementation changes are authorized by this review.
