# Judgment Spine Thesis Operating Contract Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the Judgment Spine thesis operating contract and bounded navigation/thesis patches.
use_when:
  - Checking the review result before accepting the operating contract into thesis-lane work.
  - Understanding which findings must close before the contract is used as governing guidance.
  - Checking what patches were within authorized scope.
authority_boundary: retrieval_only
input_hashes:
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 6DBFFE3ABD281193A54EA4781AF6D4E75FB0D646575C98987B7B1B6C327E7442
  docs/research/judgment-spine/judgment_spine_thesis_v0.md: 8F198443BA99B292B8F9C4F370E4CB441C9DFE4418023DBE358286DA26C31DED
  docs/research/judgment-spine/README.md: 3584FDEF4C672D78DFBF14BBDA9D06DAAD7FF3C7382F31E929E184E2960454DD
  docs/research/judgment-spine/manifest_v0.md: 15F91CB0C0FDE9E87462CE328C70E1F5C3403EFCD449C0D2DD22CFC6A1F25D17
```

- Status: REVIEW_COMPLETE_V0
- Review type: Adversarial artifact review
- Review lane: Adversarial artifact review (Orca overlay, `review-lanes.md`)
- Reviewer edit permission: read-only; this report is the only write artifact
- Patch queue authorized: no
- Implementation, runtime, package, test, automation, commit, push, or PR authorized: no

---

## 1. Review Target And Purpose

**Primary target:** `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`

**Bounded patch targets:**
- `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
- `docs/research/judgment-spine/README.md`
- `docs/research/judgment-spine/manifest_v0.md`

**Commissioning prompt:** `docs/prompts/reviews/judgment_spine_thesis_operating_contract_adversarial_review_prompt_v0.md`

**Prompt source that authorized the target work:** `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md`

**Review purpose:** Adversarially inspect whether the operating contract and bounded patches:

1. Satisfy the CA prompt's goal of turning the Judgment Spine thesis into a practical operating contract for future lanes.
2. Preserve the parent Judgment Spine thesis without becoming broad architecture planning or harness implementation.
3. Correctly distinguish parent Judgment Spine, v0.14 Judgment Harness, case-learning artifacts, failure logs, promoted lessons, Data Capture, ECR, Cleaning, and implementation authorization.
4. Preserve non-claims around validation, readiness, product proof, buyer proof, superiority, implementation, runtime, automation, tests, commits, pushes, and PRs.
5. Avoid creating new authority, source-of-truth promotion, approval, readiness, or mandatory remediation claims.
6. Keep navigation/thesis patches narrow and discoverability-oriented.
7. Stay compact enough to open before future Judgment Spine work without becoming a second architecture manual.

---

## 2. Source Context Status

```yaml
source_context_status: SOURCE_CONTEXT_READY
```

**Hash verification:** All four prompt-author-specified SHA256 hashes match the files on disk exactly. No hash mismatches.

**Dirty-state classification:**

| Source | Git status | Authority level |
| --- | --- | --- |
| `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md` | Untracked (`??`) | Working artifact; not acceptance, validation, readiness, or source-of-truth promotion |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` | Untracked (`??`) | Working thesis; not acceptance, validation, or source-of-truth |
| `docs/research/judgment-spine/README.md` | Untracked (`??`) | Working navigation artifact |
| `docs/research/judgment-spine/manifest_v0.md` | Untracked (`??`) | Working manifest |
| `.agents/workflow-overlay/*.md` | Modified (`M`) | Overlay files are dirty; advisory-grade for strict overlay claims; used as current guidance |
| `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md` | Not committed (inside tracked tree) | Commissioning context; `PROPOSED_PROMPT` status |

The review prompt's dirty-state allowance covers this: "dirty and untracked Orca docs may exist. The reviewed Judgment Spine files may be untracked. Treat dirty or untracked sources as working artifacts unless an accepted Orca source makes them controlling authority."

**Controlling sources for strict overlay claims** (read, dirty): `.agents/workflow-overlay/` files are modified but used here as advisory overlay guidance. Strict acceptance, validation, readiness, or source-of-truth claims remain `not proven`.

---

## 3. Deep-Thinking And Adversarial-Review Invocation Status

- `workflow-deep-thinking`: REFERENCE-LOADED; APPLIED before findings (framed boundary problem, failure modes, decision criteria).
- `workflow-adversarial-artifact-review`: REFERENCE-LOADED; APPLIED to produce findings after `SOURCE_CONTEXT_READY`.
- Both skills were invoked in sequence per the review prompt's method-sequencing contract.

**Working-notes goal-fit assessment (per review prompt):**

```yaml
goal_fit_check:
  anchor_goal: "Define a Thesis Operating Contract for how future lanes should consume, protect, and apply the Judgment Spine thesis."
  anchor_goal_fit: yes
  success_signal: "Future agents can use the thesis to judge fit, prevent drift, and preserve non-claims without re-litigating the long-term goal."
  success_signal_fit: yes
  basis: >
    The contract provides clear lane-type taxonomy, drift identification, non-claims,
    and owner-decision gates. All 8 CA prompt requirements are addressed. No blocking
    goal conflict found.
```

---

## 4. Source-Read Ledger

| Source | Why read | Status | Decision supported |
| --- | --- | --- | --- |
| `AGENTS.md` | Project operating boundary | Clean (tracked) | Overlay authority and implementation boundary |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | Modified (dirty) | Overlay precedence |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | Modified (dirty) | Source authority for review claims |
| `.agents/workflow-overlay/source-loading.md` | Source-loading budgets and source-gated method contract | Modified (dirty) | Source preflight and method sequencing |
| `.agents/workflow-overlay/artifact-roles.md` | Role bindings and permissions | Modified (dirty) | Artifact role binding check |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules and reviewer permissions | Modified (dirty) | Review authority and report destination |
| `.agents/workflow-overlay/prompt-orchestration.md` | Prompt artifact rules and output modes | Modified (dirty) | Output mode and review-report binding |
| `.agents/workflow-overlay/communication-style.md` | Courier YAML shape | Modified (dirty) | Report closeout shape |
| `.agents/workflow-overlay/validation-gates.md` | Validation gate definitions | Modified (dirty) | Gate-compliance check |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract | Untracked (new) | Header hygiene review |
| `.agents/workflow-overlay/template-registry.md` | Template registry | Untracked (new) | Template binding check |
| `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md` | Commissioning prompt; defines authorized scope and requirements | Not committed | Commission authority and patch scope |
| `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md` | Primary review target | Untracked | All 7 review purpose items |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` | Parent thesis (bounded patch target and reference baseline) | Untracked | CA requirement compliance; patch scope; layer boundary baseline |
| `docs/research/judgment-spine/README.md` | Bounded patch target | Untracked | Navigation patch narrowness |
| `docs/research/judgment-spine/manifest_v0.md` | Bounded patch target | Untracked | Navigation patch narrowness |
| `docs/research/judgment-spine/harness/v0_14/index.md` | v0.14 harness index; parent-vs-harness separation check | Untracked | Parent Judgment Spine vs. v0.14 harness boundary |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer-boundary canonical reference | Tracked (clean) | Data Capture / ECR / Cleaning / Judgment boundary check |

**Sources available not read:**
- `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md` — optional read; not opened because the harness index and operating contract content were sufficient to assess parent-vs-harness separation without it
- `docs/product/core_spine_v0_information_production_foundation_v0.md` — optional read; not opened because the boundary note was sufficient for layer-boundary assessment; operating contract cites it only as advisory background
- `docs/research/judgment-spine/harness/adjacent-context/README.md` — optional read; not decision-bearing for this review
- `docs/workflows/orca_repo_map_v0.md` — modified per git status; expected navigation patch target; not a required read for this review but noted as a modified file under authorized navigation patch scope

---

## 5. Findings-First Review Output

### Finding AR-01

- **Finding id:** AR-01
- **Priority:** minor
- **Phase:** correctness
- **Location:** `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`, section "Relationship To Other Judgment Spine Work > Data Capture / ECR / Cleaning Boundaries"
- **Issue:** The Judgment Spine ownership list in the "Data Capture / ECR / Cleaning Boundaries" subsection is truncated compared to the parent thesis. Specifically, the following items that the thesis includes in Judgment Spine's owned effects are absent from the operating contract's explicit ownership list: (a) "alternative explanations" (the thesis says "uncertainty and alternative explanations"; the contract says only "uncertainty"), (b) "overreach, underreach, escalation, abstention, and unsupported-claim failure modes," and (c) "reusable lessons from blind judgment versus reveal."
- **Evidence:**
  - Thesis (`judgment_spine_thesis_v0.md`, "Layer Boundary" section): "Signal Integrity effects; Signal Use Classification; uncertainty and alternative explanations; counterevidence; discounting and exclusion; Decision Strength; Action Floor, Action Ceiling, and action-band judgment; overreach, underreach, escalation, abstention, and unsupported-claim failure modes; reusable lessons from blind judgment versus reveal."
  - Operating contract ("Data Capture / ECR / Cleaning Boundaries"): "Signal Integrity effects, Signal Use Classification, uncertainty, counterevidence, discounting, exclusion, Decision Strength, Action Floor, Action Ceiling, and action-band judgment." Stops there.
  - The operating contract does mention "overreach, underreach, escalation, abstention, and unsupported-claim categories" in the "Thesis-Aligned Work" section, and lesson promotion is covered in "Case-Learning Artifacts" and "Failure Logs And Promoted Lessons." But those sections address different questions. The ownership list in the boundary section is the natural reference for a future agent doing a layer-boundary check.
- **Requirement or boundary strained:** CA prompt requirement 3 ("correctly distinguish [...] Data Capture / ECR / Cleaning / Judgment boundaries"). The operating contract's "Data Capture / ECR / Cleaning Boundaries" subsection is the dedicated cross-referencing section and is incomplete relative to the thesis baseline.
- **Impact:** A future agent consulting only the operating contract's boundary section for layer-ownership guidance could conclude that Judgment Spine's ownership does not include "alternative explanations," overreach/underreach/escalation/abstention/unsupported-claim failure modes, or reusable lessons. This creates drift risk if that agent then looks for another layer to handle these items.
- **Blocked state:** Not a blocker for the overall operating contract. The three items are implied or covered elsewhere in the document and in the thesis. But the explicit boundary section, which is the first-stop reference for boundary disputes, is weaker than it should be.
- **Minimum closure condition:** The "Data Capture / ECR / Cleaning Boundaries" subsection's Judgment Spine ownership list is updated to include (a) "alternative explanations" in the uncertainty item, (b) "overreach, underreach, escalation, abstention, and unsupported-claim failure modes," and (c) "reusable lessons from blind judgment versus reveal" — aligning it to the thesis's own layer-boundary list.
- **Next authorized action:** Owner decision on whether to accept as-is (relying on the distributed coverage elsewhere in the contract) or commission a narrow patch to the operating contract's boundary section. Patch queues are not authorized by this review lane.
- **Patch queue authorized:** no
- **Verification:** Not a testable executable check. Closure condition is met when the operating contract's boundary-section ownership list matches the thesis baseline for those three items. Red-green proof: not applicable (non-executable artifact finding).
- **Strict claims not proven:** None created by this finding.

---

### Finding AR-02

- **Finding id:** AR-02
- **Priority:** minor
- **Phase:** friction
- **Location:** `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`, retrieval header — `artifact_role: Judgment Spine thesis operating contract`
- **Issue:** The artifact role value "Judgment Spine thesis operating contract" is a repo-native role description but is not mapped in the overlay's role-binding table (`artifact-roles.md`). The standard overlay role for `docs/research/` artifacts is "Research artifact." A future agent performing a role-binding lookup via `artifact-roles.md` will not find an explicit binding for "Judgment Spine thesis operating contract" and may not know how to interpret the role.
- **Evidence:**
  - `artifact-roles.md` role table: "Research artifact" maps to `docs/research/` with specific read/write permissions, freshness markers, and paired artifacts. No entry for "Judgment Spine thesis operating contract."
  - `retrieval-metadata.md`: "artifact_role: the Orca artifact role or a concise repo-native role. If the role is required for authority and is not bound, fail visibly instead of inventing authority." — The guidance allows a "concise repo-native role," so the value is not prohibited. But "required for authority" strict cases will find no binding.
  - `authority_boundary: retrieval_only` is present, so no authority is fabricated. The impact is navigational, not authority-generating.
- **Requirement or boundary strained:** Retrieval-metadata contract (preferred repo-native roles should map to the standard table when they can). The operating contract's governance function is not a standard "research artifact" purpose, but it lives under `docs/research/`.
- **Impact:** Friction. A future agent doing role-binding lookup will not find the role. It will need to fall back to "Research artifact" for permissions, which is correct but requires interpretation. No authority confusion results because of `retrieval_only`.
- **Blocked state:** Not blocked. Advisory friction finding only.
- **Minimum closure condition:** Either (a) the overlay's `artifact-roles.md` table gains an entry for "Judgment Spine thesis operating contract" (or a general "thesis operating contract" category for governance artifacts), or (b) the role is changed to "Research artifact" with a repo-native note in the `scope` field explaining its governance function.
- **Next authorized action:** Owner awareness. No urgent action required. If the operating contract is accepted and other governance artifacts follow the same pattern, option (a) becomes worth doing.
- **Patch queue authorized:** no
- **Verification:** Red-green proof: not applicable (non-executable artifact finding).
- **Strict claims not proven:** None created by this finding.

---

### Finding AR-03

- **Finding id:** AR-03
- **Priority:** minor
- **Phase:** friction
- **Location:** `docs/research/judgment-spine/judgment_spine_thesis_v0.md`, retrieval header — `open_next` addition
- **Issue:** The `open_next` addition to the parent thesis's retrieval header (`open_next: - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`) is categorically ambiguous under the CA prompt's patch-scope rules. The CA prompt authorized two distinct patch types: (a) thesis content patches — "clarifying goal wording; sharpening non-claims; tightening parent-vs-harness separation; tightening layer boundaries; clarifying promotion or hindsight guards; clarifying how future lanes consume the thesis" — and (b) navigation patches — "only if needed to make the new operating contract discoverable, and only in `docs/research/judgment-spine/README.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`." Adding `open_next` to the thesis file is a retrieval-header navigation change to a file that was not on the navigation-patch list.
- **Evidence:**
  - CA prompt: "Navigation patch allowed: only if needed to make the new operating contract discoverable, and only in `docs/research/judgment-spine/README.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`." The thesis file (`judgment_spine_thesis_v0.md`) is not on this list.
  - CA prompt: "Valid thesis patches include: [...] clarifying how future lanes consume the thesis." This provides an alternative basis — adding `open_next` to the thesis could be classified as a thesis-content patch under "clarifying how future lanes consume the thesis."
  - The actual change is a single `open_next` retrieval-header entry. It does not change any thesis body content, goals, non-claims, or boundaries.
- **Requirement or boundary strained:** The CA prompt's distinction between thesis content patches and navigation patches; the navigation patch file list was explicit and did not include the thesis.
- **Impact:** Friction and minor ambiguity. The patch is correct in intent and minimal in scope. The ambiguity is in authorization categorization. If the CA agent classified it as a "thesis content patch under clarifying how future lanes consume the thesis," that is defensible. If classified as a "navigation patch," the file was not on the authorized list. Either way, no authority is created, no content is changed, and the change is reversible. The main risk is that future reviewers cannot tell whether the thesis file is within the navigation-patch authorized set.
- **Blocked state:** Not blocked. This is a friction finding about patch-scope categorization transparency.
- **Minimum closure condition:** The operating contract's source-context receipt (or a summary in the manifest) explicitly classifies the thesis `open_next` addition as a "thesis content patch under 'clarifying how future lanes consume the thesis'" so that a future reviewer can trace the authorization category.
- **Next authorized action:** Owner awareness. If owner accepts the classification as a thesis content patch, no further action is needed. If the owner considers it unauthorized, a decision about whether to revert or accept is required.
- **Patch queue authorized:** no
- **Verification:** Red-green proof: not applicable (non-executable artifact finding).
- **Strict claims not proven:** None created by this finding.

---

## 6. Non-Findings And Residual Risks

### Non-Findings

**CA prompt requirement satisfaction:** All 8 requirements from the CA prompt are satisfied:

1. What the thesis optimizes for — addressed in "What The Thesis Optimizes For." ✓
2. How future lanes should consume the thesis — addressed in "How Future Lanes Must Consume The Thesis" (8-item consumption checklist). ✓
3. What counts as thesis-aligned work — addressed in "Thesis-Aligned Work." ✓
4. What counts as thesis drift — addressed in "Thesis Drift" (11-item drift list). ✓
5. What changes require owner decision — addressed in "Owner Decisions Required" (8-item gate). ✓
6. How the thesis relates to parent Judgment Spine, v0.14 harness, case-learning, failure logs, promoted lessons, Data Capture / ECR / Cleaning, and implementation authorization — addressed in "Relationship To Other Judgment Spine Work" (6 subsections). ✓ (subject to AR-01 minor omission)
7. How future agents should use the thesis when preparing CA prompts, harness changes, case additions, or lesson-promotion decisions — addressed in "Applying The Thesis To Future Outputs" (5 subsections). ✓
8. What the thesis must not be used to claim — addressed in "Must Not Be Used To Claim" (non-claims list). ✓

**Non-claims completeness:** The operating contract's "Must Not Be Used To Claim" section covers all CA prompt non-claim requirements: Judgment Spine validation, v0.14 harness validation and superiority, buyer validation, willingness-to-pay, all readiness types (product, feature, commercial, proof-run, implementation, model-training), memory compounding, source-of-truth promotion, approval, acceptance, lifecycle completion, resolver/deployment/installed behavior, and authorization for runtime design, schemas, scrapers, automation, tests, packages, commits, pushes, PRs, and feature planning. ✓

**Parent-vs-harness separation:** The operating contract correctly identifies the v0.14 Judgment Harness as "one executable-spec candidate inside the parent Judgment Spine" and prohibits "forcing all Judgment Spine material into the v0.14 harness" and "letting the v0.14 harness define parent Judgment Spine strategy by default." This matches the thesis and harness index. ✓

**Data Capture / ECR / Cleaning layer boundaries (partial):** The layer-boundary assignment for what Judgment Spine must NOT own (source acquisition, ECR receipt fields, transformation ledgers, normalization, dedupe, translation, summarization, runtime storage, source APIs, source maps, capture operations) is complete and matches the canonical boundary note (`core_spine_v0_data_and_cleaning_spine_boundary_v0.md`). Only the owned-by-Judgment-Spine list has the AR-01 truncation. ✓ (with AR-01 minor gap)

**Compactness:** The operating contract is approximately 200 lines. It answers all required governance questions. It does not include harness implementation details, architecture planning, product-proof arguments, or broad spine architecture. The "Relationship" and "Applying" sections add some length but each addresses a distinct CA requirement. Acceptable for a governance artifact. ✓

**Readiness-gate language:** The sentence "If the proposed work cannot state its lane type, authority, source boundary, and non-claims, it is not ready to use the thesis" in the consumption checklist is a self-assessment gate for future lanes, not an authority-based blocking mechanism. The operating contract has `authority_boundary: retrieval_only`, so this reads as guidance rather than authority. ✓

**Navigation patches (README, manifest):** The README and manifest patches are narrow, discoverability-oriented, and within the authorized navigation patch file list. The README addition is two sentences pointing to the operating contract. The manifest addition is one table row with appropriate non-claim labeling. ✓

**Source-context receipt:** The operating contract includes a proper `orca_start_preflight` receipt with `dirty_state_checked: yes` and a `source_context_caveat` explicitly noting that the untracked state means the contract cannot prove acceptance, validation, readiness, approval, or source-of-truth promotion. ✓

**Stale-or-recheck section:** Present and covers 5 recheck conditions that are appropriate to the artifact's lifecycle. ✓

**Next-authorized-step:** "The next authorized thesis-lane step is review or refinement of this operating contract and its narrow navigation pointers. This contract does not route to harness implementation." — correctly bounded. ✓

### Residual Risks

1. All four reviewed files are untracked. No acceptance, validation, readiness, approval, or source-of-truth claims can be made from them under the current overlay.
2. The commissioning CA prompt (`judgment_spine_thesis_operating_contract_ca_prompt_v0.md`) is `PROPOSED_PROMPT` status — not accepted. The operating contract's source basis inherits this constraint.
3. The overlay files are modified (dirty). Strict overlay-binding claims remain advisory-grade until the overlay is committed or accepted.
4. `docs/workflows/orca_repo_map_v0.md` was modified (per git status) and is in the authorized navigation patch scope, but was not a required read for this review. Its changes were not assessed here.

---

## 7. Strict-Only Blockers And Not-Proven Boundaries

**Strict claims that remain `not proven`:**

- Acceptance of the operating contract as Orca source-of-truth: `not proven`
- Validation of the Judgment Spine thesis or operating contract: `not proven`
- Readiness of any kind (product, feature, implementation, proof-run, commercial): `not proven`
- Approval: `not proven`
- Source-of-truth promotion: `not proven`
- Any claim that the operating contract is accepted guidance rather than working guidance: `not proven` (the untracked/dirty state and PROPOSED_PROMPT commission source prevent this)

**Strict-only blockers for strict claims:**

- Dirty overlay sources block strict overlay-binding claims.
- Untracked review targets block acceptance or readiness claims.
- `PROPOSED_PROMPT` commission source blocks any strict claim that this review result is backed by an accepted prompt artifact.

These blockers apply only to strict claims. They do not suppress the advisory findings above or prevent the operating contract from serving as working guidance for thesis-lane work.

---

## 8. Review-Use Boundary

This is a read-only adversarial artifact review. All findings and non-findings are decision input only.

They are not approval, validation, product proof, readiness, source-of-truth promotion, implementation authorization, or mandatory remediation unless a separate authorized Orca decision, patch, validation, or implementation lane explicitly accepts them.

The findings in this report use `critical`, `major`, and `minor` as finding-priority labels only. These labels do not create approval, rejection, readiness, validation, or mandatory-remediation authority.

Patch queues are not authorized by this review lane. AR-01, AR-02, and AR-03 identify closure conditions and next authorized actions, but no executor-ready patch entries are included or authorized.

---

## 9. Next Authorized Step

The owner should decide:

1. **AR-01**: Accept the truncated layer-boundary list as-is (relying on the distributed coverage in the "Thesis-Aligned Work" and relationship subsections), or commission a narrow patch to complete the Judgment Spine ownership list in the "Data Capture / ECR / Cleaning Boundaries" subsection.
2. **AR-02**: Accept "Judgment Spine thesis operating contract" as a repo-native role (no action), or commission an overlay patch to add a role binding in `artifact-roles.md`.
3. **AR-03**: Ratify the thesis `open_next` addition as a "thesis content patch under clarifying how future lanes consume the thesis" (no action beyond owner acknowledgment), or decide whether the navigation-patch file list should be read more strictly (which would require either reversion or explicit retroactive authorization).

If all three findings are accepted or waived, the operating contract may proceed to use as working guidance for future Judgment Spine thesis-lane work.

The next authorized thesis-lane step after owner decision is working use of the operating contract as consumption and drift-prevention guidance — not harness implementation, not broad architecture planning, not product proof, and not validation claims.
