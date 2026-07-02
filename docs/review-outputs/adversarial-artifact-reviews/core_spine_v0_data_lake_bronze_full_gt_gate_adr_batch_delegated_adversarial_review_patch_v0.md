# Core Spine v0 Data Lake Bronze Full-GT Gate ADR Batch Delegated Adversarial Review-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: adversarial artifact review output
scope: >
  Delegated adversarial review-and-patch pass over the Bronze full-GT Gate ADR
  batch: Gate 1 Attachment Record body-layout ADR, Gate 2 retention/lawful-erasure
  posture ADR, and bounded recheck of the patched physicalization decision brief.
use_when:
  - Adjudicating the delegated review return before owner ratification of Gate 1 or Gate 2.
  - Checking the bounded patch applied to the Gate 1 ADR.
  - Checking why this execution does not discharge the brief's cross-vendor discovery bar.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_prompt_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
input_hashes:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md: "pre-patch git blob 8448df4acb9147649cfa31b668fe6156aaeff123"
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md: "git blob 5fd4aeef3f48da97f403923a49f077c1abaacc3c"
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md: "git blob 4b5e5abf7e5215caad003a2de6713e3f5d8567a3"
branch_or_commit: >
  Reviewed in supplied worktree branch claude/bronze-gate-adr-batch at
  42d24338795ae7500a68954aad5653df30ea3c0c. Target blobs matched the prompt pins
  before patch; branch HEAD differed from the prompt's expected authoring commit
  68627923f439e717076badf228d418f32477db89.
stale_if:
  - The commissioning CA rejects or modifies this patch during adjudication.
  - The owner ratifies, modifies, or rejects either Gate ADR.
  - A later accepted authority changes raw admission path grammar, backend selection, retention, lawful erasure, or Attachment Record body layout.
  - A true non-OpenAI, non-Anthropic controller reruns and supersedes this pass.
```

## Review Summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md
  recommendation: patch_before_acceptance
  reviewed_by: OpenAI / Codex / GPT-5
  authored_by: "[gate1-adr]/[gate2-adr] Anthropic/Claude; [brief-recheck] OpenAI/GPT (operator-recorded)"
  de_correlation_bar_per_label:
    gate1_adr: cross_vendor_discovery
    gate2_adr: cross_vendor_discovery
    brief_recheck: same_vendor_sanity
  same_vendor_rationale: >
    The current controller is OpenAI/GPT-family. That differs from the ADR author
    family and satisfies cross-vendor discovery for the two ADRs, but it is the
    same family as the Codex-authored physicalization brief and cannot discharge
    the brief's outstanding cross-vendor discovery bar.
  summary: "Found and patched two Gate 1 ADR issues: stale raw-path grammar and an under-gated G1-D external-body unlock path."
  findings_count: 2
  blocking_findings: []
  advisory_findings:
    - AR-01: Gate 1 stale raw-path grammar over-selected the physical path
    - AR-02: Gate 1 G1-D lockout could be read as Gate-2-only
  prior_findings_remediated: []
  next_action: "Commissioning CA adjudicates the Gate 1 patch as decision input; owner ratification remains separate, and brief cross-vendor discovery remains unsatisfied."
```

## Source Context

`SOURCE_CONTEXT_READY`.

Pre-review gates observed:

- `git status --short --branch`: `## claude/bronze-gate-adr-batch...origin/claude/bronze-gate-adr-batch`; no dirty files before patch.
- `git branch --show-current`: `claude/bronze-gate-adr-batch`.
- `git rev-parse HEAD`: `42d24338795ae7500a68954aad5653df30ea3c0c`.
- `git rev-parse HEAD:orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`: `8448df4acb9147649cfa31b668fe6156aaeff123`.
- `git rev-parse HEAD:orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md`: `5fd4aeef3f48da97f403923a49f077c1abaacc3c`.
- `git rev-parse HEAD:orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`: `4b5e5abf7e5215caad003a2de6713e3f5d8567a3`.
- Limitation: branch HEAD had advanced from the prompt's expected authoring commit, but the three pinned target blobs matched exactly, so the prompt's blob-mismatch stop condition did not fire.

Sources read: `AGENTS.md`; `.agents/workflow-overlay/README.md`; `.agents/workflow-overlay/source-loading.md`; `.agents/workflow-overlay/decision-routing.md`; `.agents/workflow-overlay/delegated-review-patch.md`; `.agents/workflow-overlay/review-lanes.md`; `.agents/workflow-overlay/prompt-orchestration.md`; `.agents/workflow-overlay/validation-gates.md`; `.agents/workflow-overlay/retrieval-metadata.md`; `.agents/workflow-overlay/communication-style.md`; `workflow-deep-thinking`; `workflow-adversarial-artifact-review`; `docs/prompts/templates/review/adversarial_artifact_review_v0.md`; `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`; the three labeled targets; the Gate ADR batch plan; the Attachment Record implementation contract; the Storage contract; the Physicality Location contract; the Raw Admission + Key Grammar contract; the Bronze MGT baseline declaration; and the prior physicalization brief delegated review output.

## Findings

No critical findings.

### AR-01 - Major - [gate1-adr] Stale Raw-Path Grammar Over-Selected The Physical Path

Phase: correctness.

Location: `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`, Decision In One Screen and Required Gate 1 output 3.

Issue: The pre-patch ADR selected packet-member as a body relationship but described the body as landing under `raw/<packet_id>/`. That was stale against the raw-admission contract, which now locks the packet-depth raw container behind a shard prefix. The wording let the ADR look like it selected a raw path schema rather than only the body relationship.

Evidence:

- The raw-admission contract locks the raw path grammar as `raw/<packet_shard>/<packet_id>/` and requires by-key lookup to recompute the shard, not scan or infer a locator (`core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md:95`).
- The Physicality Location contract says raw-path names are logical slot homes and that `raw/<packet_id>/...` was not locked there (`core_spine_v0_data_lake_physicality_location_contract_v0.md:148`).
- The patched ADR now says the body lands inside the packet's raw container under the current raw-admission grammar, and explicitly says this selects the body relationship, not a new raw path schema (`core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md:53`).
- The patched Required Gate 1 output now names the current sharded grammar and says the body reference remains packet-relative, not a second raw path contract (`core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md:98`).

Strongest defense considered: The ADR was probably using `raw/<packet_id>/` as shorthand for packet membership, not intending to override raw admission. That defense fails because this is an ADR prepared for owner ratification; shorthand in a ratification candidate can become the frozen contract downstream.

Impact: A future implementation-scoping lane could implement or test against the stale unsharded path, or treat Gate 1 as the authority for raw path grammar. That would contradict the raw-admission key grammar and blur a body-relationship ADR into path-schema selection.

Minimum closure condition: The Gate 1 ADR must state packet-member as a body relationship under the current raw-admission grammar, without creating a separate raw path contract or relying on stale `raw/<packet_id>/` wording.

Next authorized action: Patch within `[gate1-adr]`; CA adjudication required before keeping it.

Recommended correction: Applied in the target file.

### AR-02 - Major - [gate1-adr] G1-D Lockout Could Be Read As Gate-2-Only

Phase: correctness.

Location: `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`, Decision In One Screen, option ledger, Required Gate 1 output 3, and Named Residuals.

Issue: The pre-patch ADR said external blob/database bodies were rejected until Gate 2. That was too weak: Gate 2 can ratify an explicit deferral, and a deferral alone must not unlock an external body backend. G1-D needs Gate 2 plus a separate backend/physicalization ADR that proves storage invariants.

Evidence:

- The brief says G1-D is unacceptable before Gate 2 proves erasure/retention posture and directs that external bodies not be selected unless Gate 2 first proves the backend can preserve lake immutability, append-only history, rebuildability, and lawful-erasure posture (`core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md:136`).
- The Storage contract says any backend selection must prove raw immutability, append-only derived/ack records, rebuildable indexes, by-key discovery, external-data-root preservation or explicit supersession, and deterministic checks (`core_spine_v0_data_lake_storage_contract_v0.md:158`).
- The Gate 2 ADR records deferral with forbidden backend operations while deferred and says a backend ADR reopens or reratifies the deferral against the backend semantics (`core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md:90`, `:107`).
- The patched Gate 1 ADR now says G1-D stays locked behind Gate 2 plus a backend/physicalization ADR, and that Gate 2 ratification or deferral alone does not unlock external bodies (`core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md:59`, `:134`).

Strongest defense considered: Gate 2's backend trigger and forbidden-backend list would probably catch this later. That defense fails because the Gate 1 ADR itself is the artifact a future body-layout implementation lane will open; it must not be readable as permission to move from Gate 2 deferral directly to an external body store.

Impact: Ratifying both ADRs could leave a quiet path where external blob/database bodies are treated as eligible as soon as Gate 2 is ratified or explicitly deferred, without a backend decision proving storage invariants. That would shorten the route to backend lock-in and claim more than either ADR should claim.

Minimum closure condition: The Gate 1 ADR must keep G1-D rejected until both Gate 2 and a separate backend/physicalization ADR close the storage-invariant question; Gate 2 deferral alone cannot unlock external bodies.

Next authorized action: Patch within `[gate1-adr]`; CA adjudication required before keeping it.

Recommended correction: Applied in the target file.

## No-Patch Results

[gate2-adr]: No patch applied. The ADR names residual scope, claim ceiling, tombstone-only unavailability, forbidden backend operations while deferred, and revisit triggers. It does not claim erasure capability, backend selection, validation, readiness, or Bronze full GT.

[brief-recheck]: No patch applied. The brief's two gates remain satisfied as decided or explicitly deferred by the authored ADRs after the Gate 1 patch. This execution is same-vendor sanity for the brief, so it does not discharge the brief's outstanding cross-vendor discovery bar.

## Patch Applied

Changed only:

- `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`

Unified diff, with label tags:

[gate1-adr]

```diff
diff --git a/orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md b/orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
index 8448df4a..01e03a87 100644
--- a/orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
+++ b/orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
@@ -51,11 +51,13 @@ orca_start_preflight:

 ```text
 Selected (pending ratification): PACKET-MEMBER is the default physical body
-home. An Attachment Record body lands as immutable packet material under
-raw/<packet_id>/ at capture/publish time, exactly as preserved files land
-today. The attachments/ sidecar slot stays RESERVED, usable only through a
-future ADR when a body genuinely cannot land inside its packet. External
-blob/database bodies (G1-D) stay locked behind Gate 2. Durable entry
+home. An Attachment Record body lands as immutable packet material inside the
+packet's raw container under the current raw-admission grammar, exactly as
+preserved files land today; this selects the body relationship, not a new raw
+path schema. The attachments/ sidecar slot stays RESERVED, usable only through
+a future ADR when a body genuinely cannot land inside its packet. External
+blob/database bodies (G1-D) stay locked behind Gate 2 plus a separate
+backend/physicalization ADR that proves the storage invariants. Durable entry
 serialization (Manifest v2 vs packet-index) stays deferred to the A2 fork,
 which stays gated on the A1 deterministic inventory.
 ```
@@ -72,7 +74,7 @@ serialization or backend before the A1 inventory and Gate 2 exist.
 | G1-A incumbent generated-AR posture | Keep generated AR entries over preserved bodies; layout formally undecided. | Subsumed | Its physical substance IS packet-member; this ADR ratifies that substance instead of leaving it incidental. |
 | G1-B packet-member / bundle body | Body is immutable packet material with a compact keyed entry. | **Selected as default** | Matches current proven reality; strongest raw-authority fit; hash basis and packet identity stay local; no second body home. |
 | G1-C hash-pinned sidecar under `attachments/` | Body lives beside packets, keyed and hash-pinned. | Deferred (slot reserved) | No current body needs it; a second home doubles resolution/verification paths. Reopen trigger below. |
-| G1-D external blob/database row | Body in backend material with hash-checked ref. | Rejected until Gate 2 | Highest lock-in; the storage contract's engine boundary and Gate 2 must be satisfied first. |
+| G1-D external blob/database row | Body in backend material with hash-checked ref. | Rejected until Gate 2 plus a backend/physicalization ADR | Highest lock-in; the storage contract's engine boundary and Gate 2 must be satisfied before an external body store is even eligible. |

 Sidecar reopen trigger: a concrete body that cannot land inside its packet at
 publish time - late-arriving material for a pinned packet, or media whose size
@@ -94,8 +96,12 @@ rejected per the AR contract).
    the rule. A verifier re-reads the packet-relative file and re-hashes those
    bytes; nothing else (no manifest text, no metadata) is inside the basis.
 3. **Physical relationship.** Packet-member: the body is immutable material
-   inside `raw/<packet_id>/`, written once at staging/publish. `attachments/`
-   reserved (deferred), external bodies rejected until Gate 2.
+   inside the packet's raw container under the raw-admission key grammar
+   (currently `raw/<packet_shard>/<packet_id>/`, with by-key lookup recomputing
+   the shard), written once at staging/publish. The body reference remains
+   packet-relative; this ADR does not create a second raw path contract.
+   `attachments/` reserved (deferred), external bodies rejected until Gate 2
+   plus a backend/physicalization ADR.
 4. **Public read surface.** `source_surface_catalog_rows`,
    `load_attachment_record_body`, and their successors remain the only public
    resolution path; Silver resolves and hash-verifies through them and never
@@ -106,10 +112,12 @@ rejected per the AR contract).
 6. **Rebuild rule.** All indexes/catalog state rebuild from committed packet
    material and keys; nothing about this selection makes any index
    load-bearing.
-7. **Replay/migration implication.** Zero migration: existing packets already
-   satisfy the selected shape. Incumbent direct fields stay legacy-readable
-   (storage contract blocker-2 direction); corrections/replays append new
-   packet material; pinned packets are never mutated in place.
+7. **Replay/migration implication.** Zero body-home migration for the currently
+   exercised preserved-body shape: existing packets already satisfy the selected
+   relationship. Raw path grammar, Manifest/index serialization, dual-read, and
+   replay mechanics remain separate decisions. Incumbent direct fields stay
+   legacy-readable (storage contract blocker-2 direction); corrections/replays
+   append new packet material; pinned packets are never mutated in place.
 8. **Rejected shapes.** Everything the AR contract rejects, affirmed;
    plus, from this ADR: no second body home without a ratified ADR; no body
    bytes promoted into lake-core fields; no consumer resolution that bypasses
@@ -125,7 +133,8 @@ rejected per the AR contract).
   bodies; a media-heavy source family may hit the sidecar reopen trigger.
 - **Backend remains unselected.** Packet-member is a layout relationship, not
   a filesystem commitment; a future backend must reproduce this relationship
-  and prove the storage-contract invariants.
+  and prove the storage-contract invariants. Gate 2 ratification or deferral
+  alone does not unlock G1-D external bodies.

 ## Owner Ratification
```

## Validation

- `git diff --check -- orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`: passed, exit 0. Output was only Git's line-ending warning: `warning: in the working copy of 'orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md', LF will be replaced by CRLF the next time Git touches it`.
- `python .agents/hooks/check_retrieval_header.py --strict orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`: passed, exit 0, no output.
- `python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md`: passed, exit 0, no output.

## Residual Risk

This pass is cross-vendor discovery for `[gate1-adr]` and `[gate2-adr]`, but same-vendor sanity for `[brief-recheck]`. It cannot satisfy the brief's outstanding cross-vendor discovery bar or any no-new-seam standard for the brief.

The patch is decision input only. It is not approval, validation, readiness, mandatory remediation, gate ratification, backend selection, retention/lawful-erasure selection, erasure capability, or Bronze full-GT proof.

## Delegated Review Return

```yaml
delegated_review_return:
  source_context: SOURCE_CONTEXT_READY
  de_correlation_bar_per_label:
    gate1_adr: cross_vendor_discovery
    gate2_adr: cross_vendor_discovery
    brief_recheck: same_vendor_sanity
  controller_family: "OpenAI / Codex / GPT-5"
  verdict_overall: PATCHED_FOR_CA_ADJUDICATION
  verdict_per_label:
    gate1_adr: "patched for CA adjudication"
    gate2_adr: "no patch findings-only; no material defect found in bounded pass"
    brief_recheck: "no patch findings-only; same-vendor sanity only"
  patch_scope: "the three labeled targets only; actual patch touched [gate1-adr] only"
  report_path: "docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md"
  validation:
    - command: "git status --short --branch"
      result: passed
      evidence: "pre-review output: ## claude/bronze-gate-adr-batch...origin/claude/bronze-gate-adr-batch; no dirty files"
    - command: "git rev-parse HEAD"
      result: passed
      evidence: "42d24338795ae7500a68954aad5653df30ea3c0c"
    - command: "git rev-parse HEAD:<each labeled target path>"
      result: passed
      evidence: "all three target blobs matched the prompt pins"
    - command: "git diff --check -- orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md"
      result: passed
      evidence: "exit 0; only line-ending warning output"
    - command: "python .agents/hooks/check_retrieval_header.py --strict orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md"
      result: passed
      evidence: "exit 0, no output"
    - command: "python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md"
      result: passed
      evidence: "exit 0, no output"
  residual_risk: "Brief recheck is same-vendor sanity only; CA adjudication required before keeping the patch; owner ratification remains separate."
  ca_adjudication_required: true
```

Review-use boundary: these findings and the patch are decision input only. They are not approval, validation, readiness, mandatory remediation, gate ratification, backend or retention selection, erasure capability, full-GT proof, or evidence that the ADR batch may skip owner ratification.
