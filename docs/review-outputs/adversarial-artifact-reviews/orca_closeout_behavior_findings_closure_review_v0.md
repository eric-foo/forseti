# Orca Closeout Behavior Findings Closure Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Closure review verifying that PG-01, PG-02, and PG-03 close FF-01, FF-02, and FF-03 from the Orca closeout behavior patch adversarial review.
use_when:
  - Checking whether all three prior advisory findings from the closeout behavior patch review are closed.
  - Deciding whether the closeout behavior patch surface is ready to accept or needs a final micro-fix.
  - Tracing the chain from the prior review report to the follow-through patches.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
input_hashes:
  - path: .agents/workflow-overlay/communication-style.md
    sha256: D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049
  - path: .agents/workflow-overlay/validation-gates.md
    sha256: 0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7
  - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    sha256: 125594470EA7123CA2C80F78687464B69FE304C6D3F67166E9A04D9FDE215B9F
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: 615FBCA5C3903BE81B1C334B7AF6E1E1250CF51484F8C3DD4B6FC85289180229
  - path: docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
    sha256: 389CE8FF8F760FEC726A3E3604FB55CD0137F5ADC297FF54EA4825123DE5311D
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md
    sha256: 967BB1A53FF0911B0539A6F83B272215B233C0325E537D3F2B67A87CEE7DD20D
downstream_consumers:
  - Owner decision on accepting the closeout behavior patch surface or authorizing one final micro-fix.
stale_if:
  - Any pinned closure input hash changes before this review is acted on.
  - Additional closeout behavior patches are applied before this review is acted on.
  - The prior adversarial review report is superseded or corrected before this review is acted on.
```

---

## 1. Review Summary

**Recommendation:** `accept_with_friction`

**Closure result:** `all_findings_closed`

All three prior advisory findings are closed by their respective follow-through patches: FF-01 is closed by PG-01 (exact overlay threshold now in the shared behavior contract), FF-02 is closed by PG-02 (corrected YAML trigger and preserved human-readable closeout in the CA prompt), and FF-03 is closed by PG-03 (historical status, `superseded_by` pointers, and an explicit body-level note about the "conditionally required" language); one new minor advisory finding (FC-01) notes that the CA discussion's Prompt Structure Guidance template also contains the weaker phrase "likely to be handed" — not covered by the body-level historical note — but this is bounded by the document's `superseded_by` field and does not keep any original finding open.

---

## 2. Scope Reviewed

### Workspace Preflight

| Field | Expected | Actual | Match |
| --- | --- | --- | --- |
| Workspace path | `C:\Users\vmon7\Desktop\projects\orca` | Confirmed | ✓ |
| Branch | `main` | `main` | ✓ |
| HEAD | `a873c9c3ed3b289a65f9c472c63e0aadf880a127` | `a873c9c3ed3b289a65f9c472c63e0aadf880a127` | ✓ |

No `BLOCKED_STALE_REVIEW_INPUT` or `BLOCKED_MISSING_SOURCE` condition.

### Hash Match Status

| File | Pinned SHA256 | Computed SHA256 | Match | Git State |
| --- | --- | --- | --- | --- |
| `.agents/workflow-overlay/communication-style.md` | D93931D9... | D93931D9... | ✓ | modified, in scope |
| `.agents/workflow-overlay/prompt-orchestration.md` | 54242C83... | 54242C83... | ✓ | modified, in scope |
| `.agents/workflow-overlay/validation-gates.md` | 0DEBE6EA... | 0DEBE6EA... | ✓ | modified, in scope |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | 125594470E... | 125594470E... | ✓ | modified, in scope |
| `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` | 615FBCA5... | 615FBCA5... | ✓ | untracked, in scope |
| `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` | 389CE8FF... | 389CE8FF... | ✓ | untracked, in scope |
| `docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md` | 967BB1A5... | 967BB1A5... | ✓ | untracked, in scope |

All seven pinned hashes match exactly. Review proceeded with full authority.

### Source-Read Ledger

| Source | Role | Git State | Decision Supported |
| --- | --- | --- | --- |
| `AGENTS.md` | Orca operating instructions | clean | Source hierarchy, authority boundary |
| `.agents/workflow-overlay/README.md` | Overlay authority | clean | Overlay entrypoint, binding rule |
| `.agents/workflow-overlay/source-of-truth.md` | Overlay authority | clean | Source hierarchy binding |
| `.agents/workflow-overlay/artifact-roles.md` | Overlay authority | clean | Role binding: review report, prompt template, handoff prompt, workflow record |
| `.agents/workflow-overlay/artifact-folders.md` | Overlay authority | clean | Folder rules |
| `.agents/workflow-overlay/review-lanes.md` | Overlay authority | clean | Adversarial artifact review lane binding |
| `.agents/workflow-overlay/prompt-orchestration.md` | Overlay authority | modified (in scope) | YAML trigger standard, output-mode rules |
| `.agents/workflow-overlay/communication-style.md` | Overlay authority | modified (in scope) | YAML trigger standard, courier YAML shape |
| `.agents/workflow-overlay/validation-gates.md` | Overlay authority | modified (in scope) | YAML trigger standard, chat-output topology gate |
| `.agents/workflow-overlay/template-registry.md` | Overlay authority | clean | Template kind binding |
| `.agents/workflow-overlay/retrieval-metadata.md` | Overlay authority | clean | Retrieval metadata contract |
| Prior review report | Review report (prior) | untracked, in scope | Prior findings FF-01, FF-02, FF-03 and PG-01, PG-02, PG-03 |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | Prompt template | modified, in scope | FF-01/PG-01 closure target |
| `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` | Planning handoff prompt | untracked, in scope | FF-02/PG-02 closure target |
| `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` | Workflow record | untracked, in scope | FF-03/PG-03 closure target |

Dirty-state handling: all three closure target files are dirty (modified or untracked) and explicitly in scope for this review per the review prompt. The overlay references are also dirty and used as the authoritative threshold standard.

### Deep Thinking

`workflow-deep-thinking` was invoked before the formal adversarial artifact review pass. It produced the closure criteria, failure modes (threshold approximation, authority creep, template subordination loss, superseded_by accuracy, YAML obligation drift), and decision criteria used throughout. The framing was active in this review.

### Source-Loading Mode

Strict formal review. Overlay authority loaded. Artifact roles, review lane, validation gates, and source hierarchy bound before findings were written.

---

## 3. Closure Matrix

### FF-01 — Shared Behavior Contract YAML Trigger

**Original finding:** `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` used "lane switching / handoff routing benefits from compact courier YAML" — missing "would materially" — making the YAML trigger weaker than the three overlay files.

**PG-01 correction:** Replace "benefits from" with "would materially benefit from."

**Closure evidence:**

- Line 31 of the current file: `lane switching / handoff routing would materially benefit from compact`
- Targeted search for "benefits from compact courier YAML" in the file: no matches
- Targeted search for "would materially benefit" in the file: confirmed match at line 31

**FF-01 status: CLOSED.** The exact overlay threshold is present. The old weaker phrase is absent.

**Regression check:** The contract at lines 27-28 reads "follow the chat-output topology in `.agents/workflow-overlay/communication-style.md`" — explicitly deferring to the overlay. Source Authority section (line 18) names the overlay as the owner of Orca project facts. The contract reads as a template include that points to the overlay, not as a second overlay authority. Regression: **not present**.

---

### FF-02 — Major-Move CA Prompt Chat Closeout YAML Trigger

**Original finding:** `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` Chat Closeout used "compact courier YAML when this result is likely to be handed to another lane, agent, thread, or prompt" — a lower threshold than the overlay's "would materially benefit."

**PG-02 correction:** Replace with "compact courier YAML when lane switching, handoff routing, or another agent or thread is expected to continue from this result and compact courier YAML would materially benefit that routing."

**Closure evidence:**

- Lines 283-284 of the current file: `compact courier YAML when lane switching, handoff routing, or another agent or thread is expected to continue from this result and compact courier YAML would materially benefit that routing.`
- Targeted search for "likely to be handed" in the file: no matches
- Targeted search for "would materially benefit" in the file: confirmed match at line 284

**FF-02 status: CLOSED.** The corrected conditional threshold is present. "Likely to be handed" is absent.

**Regression check:** Chat Closeout section (line 270) still requires "a compact headed human-readable closeout" and "Do not return a receipt-only response." Multiple bullet points requiring decision substance remain intact (recommendation, material decision facts, tradeoffs, deferred items, exact next step). Human-readable headed closeout: **preserved**. Regression: **not present**.

---

### FF-03 — CA Discussion Stale-If Not Flagged, Historical Language Unaddressed

**Original finding:** `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` had met its `stale_if` condition (patch applied) but lacked `superseded_by` pointers and a historical status marker; its "conditionally required" YAML language remained readable as current guidance.

**PG-03 correction:** Add `superseded_by` field pointing to controlling sources, update status to `HISTORICAL_PATCH_DISCUSSION`, add a body-level note that "conditionally required" is historical and the current threshold is the overlay's.

**Closure evidence:**

- Line 50: `Status: \`HISTORICAL_PATCH_DISCUSSION\`.`
- Line 17: `superseded_by:` field present, listing `.agents/workflow-overlay/communication-style.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/validation-gates.md`, and `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` — all four controlling current sources, confirmed accurate.
- Lines 51-59: Historical note explicitly states the `stale_if` condition was met and names "conditionally required" as historical: "Where this discussion says courier YAML is 'conditionally required,' treat that as historical framing superseded by the current overlay threshold: use compact courier YAML only when requested, required by output mode or output contract, or lane switching / handoff routing would materially benefit from it."
- Body text at line 157 still reads "Courier YAML should be conditionally required..." but this is in the historical Recommended Closeout Contract section, covered by the historical note above.

**FF-03 status: CLOSED.** Status updated, `superseded_by` added and accurate, "conditionally required" language explicitly named as historical in the body-level note, and current overlay threshold stated as the replacement.

**Residual-risk check (FF-03):** See FC-01 below. The Prompt Structure Guidance template at line 233 contains a second weak phrase ("likely to be handed") not covered by the historical note's specific callout. This is advisory only and does not keep FF-03 open.

---

## 4. Findings

### FC-01

**Severity:** Minor (advisory)

**Affected original finding:** FF-03

**Location:** `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`, Prompt Structure Guidance section, line 233

**Issue:** The PG-03 historical note (lines 56-59) explicitly names "conditionally required" as the historical phrase superseded by the overlay threshold. However, the CA discussion's Prompt Structure Guidance section contains a second weak phrase at line 233 — "compact courier YAML when this result is likely to be handed to another lane, agent, thread, or prompt" — which was the original FF-02 language. This phrase is not mentioned in the historical note. A future prompt author using the Prompt Structure Guidance as a template source could pick up "likely to be handed" without the specific historical callout that was applied to "conditionally required."

**Evidence:**

- Line 233: `compact courier YAML when this result is likely to be handed to another lane, agent, thread, or prompt.`
- Lines 56-59 (historical note): names "conditionally required" specifically as the historical phrase; does not name "likely to be handed."
- `superseded_by` field at line 17: applies to the whole document but is a header-level signal, not a phrase-level callout.

**Impact:** Advisory. A prompt author who ignores the `HISTORICAL_PATCH_DISCUSSION` status, ignores the `superseded_by` field, ignores the historical note, and directly uses the Prompt Structure Guidance template clause would pick up "likely to be handed" instead of the correct "would materially benefit" threshold. This path requires multiple source-discipline failures. The `superseded_by` field is the primary defense and is accurate. This finding does not keep FF-03 open.

**Recommended correction:** Extend the historical note by one phrase to also name "likely to be handed" as historical: e.g., add "Similarly, where the Prompt Structure Guidance below recommends 'likely to be handed,' treat that as the pre-patch threshold; use the current overlay threshold ('would materially benefit') instead." This is a one-sentence edit to the Status section historical note.

---

## 5. Non-Findings

**NCF-01 — FF-01 template subordination intact.** The shared behavior contract (Output Discipline section, line 27) explicitly defers to `.agents/workflow-overlay/communication-style.md` for the chat-output topology rule. The Source Authority section (line 18) places the overlay above docs. The contract does not claim to own YAML policy; it inherits it. No authority-creep regression introduced.

**NCF-02 — FF-02 human-readable headed closeout preserved.** The Chat Closeout section in the CA prompt (lines 270-287) explicitly requires a "compact headed human-readable closeout," prohibits "receipt-only response," and lists six content bullets (recommendation, material decision facts, tradeoffs, deferred items, artifact path/SHA256, next step) before the YAML condition. The human-readable closeout requirement is unambiguously preserved and the human-first ordering is correct.

**NCF-03 — FF-03 superseded_by pointers accurate.** All four `superseded_by` sources are confirmed current Orca overlay authority: `communication-style.md`, `prompt-orchestration.md`, `validation-gates.md`, and the shared behavior contract. The fourth (`orca_prompt_behavior_contract_v0.md`) was itself patched for PG-01, so the pointer correctly leads to the closed version.

**NCF-04 — No new validation, readiness, approval, or lifecycle claims.** Targeted search across all three target files for claim language found no new claims. The shared behavior contract's non-claim statement (line 41) is an existing, correct restriction clause. No new completion, readiness, resolver, install, deploy, product-readiness, or merge-safety claims were introduced.

**NCF-05 — No jb policy contamination.** All "jb" occurrences in target files are exclusion/prohibition clauses ("Do not import `jb` rules..."), not imported jb policy. No GAP, CV Engine, lifecycle mechanics, or jb handoff rules found in any closure patch.

**NCF-06 — No scope broadening.** All three patches are narrowly scoped to their respective findings. No overlay files, no review reports other than this one, no skill files, and no unrelated docs were touched. The CA discussion patch is limited to the retrieval header and Status section.

**NCF-07 — FF-03 stale_if condition correctly described in historical note.** The historical note states "the stale_if condition for owner acceptance or rejection of a file-write closeout summary patch has been met" and "the patch route recommended by this discussion has been applied in the working tree." This is accurate and matches the prior review's assessment.

**NCF-08 — Overlay YAML threshold integrity confirmed.** The three overlay files (`communication-style.md`, `prompt-orchestration.md`, `validation-gates.md`) all consistently use "lane switching / handoff routing would materially benefit from compact courier YAML." The closure patches correctly aligned to this standard. No overlay file was modified by the closure patches.

---

## 6. Residual Risks And Non-Claims

### Residual Risks

**RR-01 (FC-01):** The CA discussion Prompt Structure Guidance template still carries "likely to be handed" without an explicit historical callout. The risk is bounded by `superseded_by` and `HISTORICAL_PATCH_DISCUSSION` status but not fully eliminated by the body-level historical note. The owner may choose to add one sentence to the historical note to close this gap.

**RR-02 (CA discussion Recommendation line):** Lines 61-62 in the CA discussion Status section contain the original Recommendation ("patch the `file-write` output-mode rule and shared prompt behavior..."). The framing makes clear this is the historical recommendation that was applied, but the "Recommendation:" label could be read as forward-looking by a reader who skims without reading the preceding historical note. This is bounded by context and does not constitute a finding.

### Non-Claims

This review does not claim:

- Approval of the closeout behavior patch surface.
- Validation that the patch surface is complete or correct.
- Readiness of any Orca artifact, prompt, or overlay for deployment or production use.
- Lifecycle completion.
- Resolver behavior.
- Install or deployment status.
- Implementation readiness.
- Product readiness.
- Merge safety.
- That any finding or non-finding constitutes a mandatory remediation order.

Findings are decision input for the owner. Only a separately authorized patch, acceptance, validation, lifecycle, or implementation lane can make remediation mandatory or executor-ready.

---

## 7. Exact Next Authorized Step

Accept FF-01, FF-02, and FF-03 as closed by their respective follow-through patches. If the owner chooses to resolve FC-01, authorize a narrow one-sentence edit to the historical note in `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` to also name "likely to be handed" as historical alongside "conditionally required" — no overlay changes, no skill changes, no commit, and no PR are required to accept the three original findings as closed.
