# Data Capture Spine Posture Vocabulary Enforcement Proposal — Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial artifact review of the proposed Data Capture Spine
  posture-vocabulary enforcement (R2), to make the foundation solid before the
  Data Capture lane executes/ratifies it and before JSG-01 binds to it.
use_when:
  - Dispatching the independent 2nd-opinion review of the R2 proposal.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md: 2E5D05B8F8366711F4A749B68664E0034BED7C8460B629EF1BA881AED04D5FA5
branch_or_commit: main @ f9b05e6 (worktree dirty; controlling sources untracked)
```

## Commission

Adversarially review **one artifact**: the Data Capture Spine posture-vocabulary
enforcement proposal (R2). Decide whether it is sound enough for the Data Capture
lane to take into execution + ratification — and surface every material failure
mode first. Read-only, findings-first, advisory. It does not approve, execute,
ratify, or unfreeze any gate.

## Target (commission-bound; do not retarget)

- `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`
  (SHA256 `2E5D05B8F8366711F4A749B68664E0034BED7C8460B629EF1BA881AED04D5FA5`).
  Confirm the hash; if it differs, stop and report drift.

## Operator precondition (owner-set, NOT prompt-routed)

To satisfy the independent-review bar, dispatch to a reviewer in a **different
model family** from the author (Claude). This prompt is model-neutral and does
not select or recommend a runtime model.

## Reviewer start state

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: read-only
  target_scope: [docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md]
  dirty_state_checked: required_yes
  blocked_if_missing: yes
controlling_source_state: untracked/dirty; advisory review only; no strict PASS/readiness/ratification claims.
edit_permission: read-only
output_mode: review-report
external_source_boundary: agent-workflow is read-only reusable mechanics; jb is NOT Orca authority.
```

## Required read-pack — INCLUDES the implemented code (blind-spot fix)

The prior review of the JSG-01 translator **missed a real collision because its
read-pack excluded the implemented capture code.** Do not repeat that. This review
MUST read the code, its tests, and existing packets — not just doctrine docs:

- **Target:** the proposal (above).
- **Contract (vocabulary source of truth):** `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` — Ob.9 (cutoff), Ob.10 (archive), Ob.11 (visibility), Ob.15 (re-capture). Verify the proposed closed values match these *exactly*.
- **Implemented code:** `orca-harness/source_capture/models.py` (SourceCapturePacket, PacketTiming, VisibleFact, PreservedFile), `writer.py`, `source_quality.py`, `packet_assembly.py`.
- **Tests + existing packets (migration reality):** `orca-harness/tests/unit/test_source_capture_packet.py`, `test_packet_assembly.py`, and existing packet manifests under `orca-harness/reports/source_capture/**/manifest.json`. Check what posture values existing packets actually carry.
- **Harness contrast:** `orca-harness/schemas/case_models.py` (`EvidenceUnit.hash_basis`).
- **Layer boundary:** `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (Capture records / Judgment decides).
- **Consumer:** `docs/product/jsg01_source_side_receipt_translator_v0.md` (what JSG-01 needs from these fields).

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, review-lanes, prompt-orchestration).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-adversarial-artifact-review`. Do **not** APPLY yet.
3. `SOURCE-LOAD` the read-pack.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only then APPLY deep-thinking to frame failure modes, then adversarial-artifact-review to produce findings, each cited to file:line.

If `workflow-adversarial-artifact-review` is unavailable/not applied, return blocked or advisory-only; emit no formal verdict/readiness/validation claim.

## Decision criteria — attack these seams

1. **Value-vs-sufficiency boundary.** Does closing the vocabulary stay *value-only* (what posture it is) and leave *sufficiency* (good-enough-to-clear, claim grade) downstream? Is any posture being closed actually a downstream Judgment — especially the archive "corroborated/diverged" materiality call the proposal says to keep out?
2. **No invention.** Do the proposed closed values (`cutoff`, `archive`, `re_capture`) match Ob.9/Ob.10/Ob.15 **exactly** (file:line)? Any added, dropped, or renamed value?
3. **access_posture left open — correctly?** Is the proposal right that Ob.11 has no closed set, or does a closed vocabulary exist there that the proposal should have used? Conversely, is leaving it free-text a hole?
4. **Status-vs-value reconciliation (archive).** Routing `not_attempted`/`not_applicable` to `VisibleFactStatus` and `{archived, attempt_failed}` to the value — clean, or does it double-encode / lose information / conflict with how `packet_assembly.py` already uses statuses?
5. **Migration landmines.** Do existing packets/tests/runners actually carry posture values *outside* the proposed closed sets? (Read the packets + tests.) Would closing the schema break them, and is the proposal's "migration is a code concern" punt acceptable or does it hide a blocker?
6. **Completeness for the consumer.** Does closing these give JSG-01 (and the eventual ECR) what a source-side gate needs, or are there source-side facts still left as unenforced free text that the gate would have to interpret anyway?
7. **hash_basis sufficiency.** Does adding `hash_basis: str` actually close AR-03 (verifiable "what the hash covers"), or does verifiability need more (constrained basis, linkage to preserved bytes)?
8. **Lane discipline.** Does the proposal stay a *proposal* (routes execution/ratification/DCP to the DC lane), or does it over-reach toward executing/ratifying?

## Output contract

- `review-report` mode. Write to `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md`.
- Start with the compact `review_summary` YAML (`recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked`), then findings.
- Findings-first: ID, `severity` (`critical|major|minor`, priority only), seam, file:line evidence, `minimum_closure_condition` (end state), `next_authorized_action`.
- Include non-findings (seams that held) and not-proven boundaries (e.g., that the schema change is safe for cases beyond those read; that this review is cross-family if the reviewer is same-family).
- **Advisory only.** No `patch_queue_entry`, no executor-ready how-to. Optional hardening labeled optional.

## Validation gates (must be able to fail)

- Source readiness declared before findings; the implemented code + existing packets actually read (or `SOURCE_CONTEXT_INCOMPLETE`).
- Target hash confirmed; drift → BLOCKED.
- Untracked/dirty sources → advisory only; no strict PASS/readiness/ratification claim.
- Durable report written before any YAML-only chat summary; on write failure use `status: failed`, `review_location: chat_only_current_thread`, `recommendation: blocked`.

## Review-use boundary

Findings are decision input for the owner / Data Capture lane only — not approval,
validation, ratification, mandatory remediation, or patch authority. This review
does not execute the schema/contract change and does not unfreeze JSG-01.
`agent-workflow` is read-only reusable mechanics; `jb` is not Orca authority.
