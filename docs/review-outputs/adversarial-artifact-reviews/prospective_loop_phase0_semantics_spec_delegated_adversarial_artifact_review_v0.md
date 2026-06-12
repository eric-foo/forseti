# Delegated Adversarial Artifact Review + Bounded Patch -- Phase-0 Semantics Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial artifact review report (advisory decision input; bounded patch applied in working tree)
scope: >
  Review report for the commissioned repo-mode delegated review-and-patch pass
  on docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 / Codex (snapshot unrecorded)
authored_by: claude-fable-5[1m]
de_correlation_bar: cross_vendor_discovery
target: docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md
bounded_patch_scope:
  - target file only
  - this report file
non_claims:
  - advisory decision input only
  - provisional delegated-review-and-patch convention
  - not validation
  - not readiness
  - not acceptance
  - not pilot authorization
  - not a formal review-lane PASS
```

## Review Summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/prospective_loop_phase0_semantics_spec_delegated_adversarial_artifact_review_v0.md
  target: docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md
  authority: delegated review-and-patch commission under .agents/workflow-overlay/delegated-review-patch.md
  decision_criteria:
    - by-hand operator can run intake -> seal -> disclose/observe -> resolve without invented semantics
    - vocabulary trace matches orca-harness/schemas/judgement_models.py field-for-field where it claims harness ownership
    - firewall invariants from the target architecture remain intact
  findings:
    - AR-01
    - AR-02
  patch_status: bounded_patch_applied_uncommitted
  recommendation: home_model_adjudicate_diff_hunk_by_hunk
```

Advisory-only bound: this report is decision input for the commissioning Chief Architect. It creates no formal approval, validation, readiness, mandatory remediation, pilot authorization, evidence-tier promotion, or source-of-truth claim. The durable patch remains unkept until home-model adjudication.

## Preflight And Source Ledger

Actor/model-family receipt:

- author_home_model_family: Anthropic / Claude, from the commission.
- controller_model_family: OpenAI / GPT, current receiving actor role `controller`.
- de_correlation_status: satisfied for the commission's cross-vendor discovery bar; not a runtime model recommendation.

Worktree preflight:

- workspace: `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-prospective-loop-wt`.
- branch: `phase0-semantics-spec-v0`.
- start dirty-state: clean.
- `git log --oneline -5` showed `4c61374` then `a3ddd6d`; the commissioned target commit is in history.
- target SHA256 over git blob bytes: `a3ddd6d` and `HEAD` both produced `0eb599c15a99182f2d2c8870bbd786bfcd8592837e513d50d0ab116ea30f7e10`.

`orca_start_preflight`:

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_phase0_semantics_review
  edit_permission: patch-only (single named target) + report file-write
  target_scope:
    - docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/prospective_loop_phase0_semantics_spec_delegated_adversarial_artifact_review_v0.md
  dirty_state_checked: yes
  repo_map_decision: not_needed
  external_source_boundary: jb is not Orca authority
```

Sources read:

| Source | Why read | Status at read |
| --- | --- | --- |
| `AGENTS.md` | Project operating kernel, source-changing and delegated review rules | clean |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | clean |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | clean |
| `.agents/workflow-overlay/source-loading.md` | Start preflight and source-gated method contract | clean |
| `.agents/workflow-overlay/review-lanes.md` | Review lane, provenance, severity, and model-neutrality rules | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | Review-report output mode and source-gated sequencing | clean |
| `.agents/workflow-overlay/validation-gates.md` | Validation and non-self-certification boundaries | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Provisional repo-mode review-and-patch operating contract | clean |
| `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | Reference-loaded review method | clean |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | Reference-loaded shared behavior contract | clean |
| `workflow-adversarial-artifact-review` skill source | Task-local review mechanics | installed skill source, not Orca authority |
| `workflow-deep-thinking` skill source | Task-local reasoning discipline | installed skill source, not Orca authority |
| target spec | Review target and only patched artifact | clean before patch, modified by this pass |
| target architecture | Firewall invariants and decision-object source | clean |
| `orca-harness/schemas/judgement_models.py` | Vocabulary trace check | clean |
| batch-1 ledger Screen Provenance section | Worked-example cited source | clean |

Source exclusions honored: research corpus, other harness code, prior review outputs, other prompts beyond the commissioned prompt/method templates, and `_inbox`.

## Reasoning-Before-Findings Pass

The material failure modes were:

- The spec claims "zero unmapped names" and harness vocabulary reuse, so a silent field rename is worse than prose roughness: it gives Phase-1 operators a field shape that cannot later trace to the schema it cites.
- The fitness bar is hand-runnability. A field can have a fill-rule and still fail the bar if the book's file/chain mechanics do not tell an operator where and how to record it.
- The firewall is carried by ordering proof, not timestamps. Any entry mechanic that fails to embed the correct prior hash, or fails to identify which scoreable seal is being resolved, opens a post-hoc ambiguity channel.
- The patch must not redesign the architecture or create the near-half ledger; fixes must be local to vocabulary alignment and book mechanics.

## Findings

### AR-01 -- Major -- Harness vocabulary drift in assumption/evidence fields

Location: target spec "Vocabulary Trace Table" and `sealed_call` fill-rules, especially the pre-patch `assumptions` shape and worked example.

Issue: The spec claimed harness vocabulary reuse but used `evidence_refs` for assumptions and omitted harness-owned evidence field names from the live signal shape. `orca-harness/schemas/judgement_models.py` defines `LoadBearingAssumption` with `statement`, `evidence_unit_ids`, and `would_flip_if_false`; it defines `EvidenceUsed` with `claim_id`, `claim_text`, `claim_role`, and `evidence_unit_ids`. The target's pre-patch shape used `evidence_refs` and `description`, creating a silent rename at the exact vocabulary-trace surface the commission called load-bearing.

Evidence:

- Target pre-patch semantics: `assumptions` used `[{statement, evidence_refs, would_flip_if_false}]`; worked example used `evidence_refs: [batch-1 Screen Provenance]`.
- Harness source: `LoadBearingAssumption` has `evidence_unit_ids`, not `evidence_refs`; `EvidenceUsed` has `claim_text`, `claim_role`, and `evidence_unit_ids`.
- Target architecture allows a loop-specific `signal_id`; preserving `signal_id` is correct, but the evidence-text and evidence-reference fields needed explicit harness alignment.

Strongest defense: the target architecture itself names `signals_used` and `signal_id`, so the spec is not required to copy the full `EvidenceUsed` class. That defense holds for `signal_id` only. It does not justify renaming the cited harness fields where the spec explicitly claims field-for-field traceability.

Impact: A Phase-1 operator could produce assumption and signal records that are hand-readable but fail later schema or ledger translation, undermining the "zero invented semantics" bar.

Patch applied:

- Trace table now maps `evidence_unit_ids`, `claim_text`, and `claim_role` to the harness sources and `signal_id` to the target architecture / pending near-half interface.
- `signals_used` now uses `[{signal_id, claim_text, claim_role, evidence_unit_ids}]`.
- `assumptions` and the worked example now use `evidence_unit_ids`.

minimum_closure_condition: no target occurrence of `evidence_refs` remains, and the target's harness-owned field names match `judgement_models.py` where the spec claims harness ownership.

next_authorized_action: home-model adjudication of the vocabulary hunk against the target architecture and harness schema.

Verification: source-support finding; red-green proof is not applicable as an executable test. String check and diff review are the appropriate evidence.

### AR-02 -- Major -- Entry mechanics did not record actual_path or resolve update seals without operator invention

Location: target spec "The Book: Entry Mechanics" folder shape and chain rule.

Issue: The pre-patch folder shape had `01_intake.md`, `02_sealed_call.md`, assisted-only `03_disclosure.md`, optional updates, and one `0M_resolution.md` that embedded `02_sealed_call.md`. It omitted a concrete `actual_path` entry even though the field rule says `actual_path` is filled when the org decides. It also did not state how a resolution identifies and chains to a later update seal, even though both the architecture and target spec say each update is a complete scoreable sealed call and every prior seal still resolves.

Evidence:

- Target architecture: `actual_path` is a first-class group; updates are "each its own sealed call scored against its own information_set_ref; never an edit or replacement of an earlier scoreable call."
- Target pre-patch semantics: `actual_path` was filled when the org decides, but the file book had no actual-path file. Resolution embedded only the original sealed-call hash, not the specific update seal being resolved.
- Target architecture governance: replay requires recomputation from `information_set_ref`, `sealed_call`, and `outcome_record`; that implies each scoreable seal/update must be identifiable at resolution.

Strongest defense: the operator might place `actual_path` inside the resolution file and resolve only the original seal in Phase 1. That defense fails the spec's own hand-runnability standard because it requires the operator to invent file placement and update-resolution semantics, and it contradicts the "every prior seal still resolves" rule.

Impact: The chain could remain append-only while still failing to prove when the org decision was recorded or which scoreable seal/update a resolution applies to. That is a firewall and replayability defect, not just formatting friction.

Patch applied:

- Folder shape now includes `04_actual_path.md` as the passive observation entry.
- Update seals now embed both the prior scoreable seal hash and the latest prior entry hash.
- Resolution files are now `0M_resolution_<seal-entry>.md`, one per scoreable seal/update, embedding both the resolved seal/update hash and the latest prior entry hash.
- Chain rule now states the dual proof: latest prior ledger entry for ordering, and specific scoreable seal/update hash for resolution target identity.

minimum_closure_condition: the book tells a by-hand operator where to record actual path, how to keep ordering proof, and how to identify the seal/update being resolved without inventing a convention.

next_authorized_action: home-model adjudication of the entry-mechanics hunk; if accepted, any future pilot-ledger declaration should mirror this chain shape rather than re-derive it.

Verification: source-support finding; red-green proof is not applicable as an executable test. Diff review against the architecture's update/actual_path/resolution invariants is the appropriate evidence.

## Friction Findings

No separate friction-only finding was kept. The two material issues above were correctness and executability defects; other possible edits would be style or future hardening and were left untouched.

## Unified Diff

```diff
diff --git a/docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md b/docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md
index c985972..367f364 100644
--- a/docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md
+++ b/docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md
@@ -64,8 +64,9 @@ Every field name below traces to one owning source. No new vocabulary is minted.
 | --- | --- |
 | decision_object_v0 groups (identity, mode, frame, sealed_call, disclosure, actual_path, updates, resolution, learning_extraction, integrity) | Target architecture §1 (adjudicated) |
 | claimed_floor, claimed_ceiling, reasoning | `ContestantBandClaim`, orca-harness/schemas/judgement_models.py |
-| statement, would_flip_if_false | `LoadBearingAssumption`, judgement_models.py |
-| claim_role: load_bearing / supporting / contextual | `EvidenceUsed`, judgement_models.py |
+| statement, evidence_unit_ids, would_flip_if_false | `LoadBearingAssumption`, judgement_models.py |
+| claim_text, claim_role: load_bearing / supporting / contextual, evidence_unit_ids | `EvidenceUsed`, judgement_models.py |
+| signal_id | Target architecture §1 `signals_used` / pending near-half signal-reliability interface |
 | 0-8 action-intensity ladder | `RecommendedAction.ladder_level`, judgement_models.py |
 | seal-before-disclose, mechanical resolution, append-only, quarantine-as-data | Target architecture (firewall translation, adjudicated) |
 | unscoreable_by_design | Target architecture §1 intake gate |
@@ -111,8 +112,8 @@ Format per field: **filled by / when / from what / filled means**.
 - `resolution_criteria` -- sealing actor / at seal / mechanical instructions a third party could apply: where the metric is read, how the band is compared, what counts as in/over/under / filled means resolution requires zero judgment. Resolution may **apply** these; it may never author or amend them.
 - `leading_indicators` -- sealing actor / at seal / `[{signal, expected_direction, check_window}]` / observable early signals; empty allowed with the line "none identified".
 - `kill_or_adjust_triggers` -- sealing actor / at seal / `[{condition, pre_committed_response}]` / conditions concrete enough that firing is observable.
-- `signals_used` -- sealing actor / at seal / `[{signal_id, description, claim_role}]` with `claim_role` in load_bearing/supporting/contextual / every load-bearing input named (this is the live signal pre-commitment; rows flow to the near-half reliability ledger at resolution).
-- `assumptions` -- sealing actor / at seal / `[{statement, evidence_refs, would_flip_if_false}]` / every assumption whose falsity would change the call carries `would_flip_if_false: true`.
+- `signals_used` -- sealing actor / at seal / `[{signal_id, claim_text, claim_role, evidence_unit_ids}]` with `claim_role` in load_bearing/supporting/contextual / every load-bearing input named; `signal_id` is the live-loop signal key, while `claim_text`, `claim_role`, and `evidence_unit_ids` reuse the harness evidence vocabulary (this is the live signal pre-commitment; rows flow to the near-half reliability ledger at resolution).
+- `assumptions` -- sealing actor / at seal / `[{statement, evidence_unit_ids, would_flip_if_false}]` / every assumption whose falsity would change the call carries `would_flip_if_false: true`.
 - `lessons_consulted` -- sealing actor / at seal / retrieval handles of validated lessons used; `pending_interface` until the near-half ledger exists (N7); never invented.
 - `reasoning_trace` -- sealing actor / at seal / REQUIRED full trace from frame to recommendation / filled means a reader can derive the call from the brief (the derivability standard; doubles as the lesson-extraction and audit surface).
 - `seal.content_hash` -- operator / immediately after committing the sealed-call file / the hash convention below.
@@ -153,15 +154,19 @@ Format per field: **filled by / when / from what / filled means**.
   01_intake.md          # identity + mode + frame
   02_sealed_call.md     # sealed_call (embeds the SHA256 of 01_intake.md)
   03_disclosure.md      # assisted only (embeds the SHA256 of 02_sealed_call.md)
-  0N_update_seal.md     # optional re-seals (each embeds the prior seal's SHA256)
-  0M_resolution.md      # resolution + learning_extraction (embeds the SHA256 of 02_sealed_call.md)
+  04_actual_path.md     # passive observation when the org decides (embeds the latest prior entry SHA256)
+  0N_update_seal.md     # optional re-seals before org-decision/outcome/resolution signal is known (each embeds the prior scoreable seal's SHA256 and the latest prior entry SHA256)
+  0M_resolution_<seal-entry>.md # resolution + learning_extraction for one scoreable seal/update (embeds that seal/update SHA256 and the latest prior entry SHA256)
 <ledger_home>/index.md  # one line per entry: decision_id -> file -> hash -> status
 ```
 
 **The chain rule (the ordering proof):** every entry after the first embeds the
-hash of the entry it follows. A disclosure containing the seal's hash can only
-have been written after the seal existed -- ordering is proven by content, not
-by timestamps or git history, so it survives squash-merges and branch deletion.
+hash of the latest prior ledger entry it follows. A disclosure containing the
+seal's hash can only have been written after the seal existed; an update seal
+also embeds the prior scoreable seal hash it supersedes-by-reference; a
+resolution embeds the specific seal/update hash it resolves. Ordering is proven
+by content, not by timestamps or git history, so it survives squash-merges and
+branch deletion.
 
 **Hash convention (binding):** SHA256 over **git blob bytes** (LF as stored),
 never CRLF working-tree bytes. Verified recipe (cross-platform):
@@ -224,11 +229,12 @@ sign-off, not by this spec.
   Reddit equivalents, check_window: first screening day}]`.
   kill_or_adjust_triggers: `[{condition: first pass yields 0 qualifying blog
   candidates, pre_committed_response: reprioritize Reddit immediately}]`.
-  signals_used: `[{signal_id: batch1-screen-venue-yield, description: "blogs
+  signals_used: `[{signal_id: batch1-screen-venue-yield, claim_text: "blogs
   (mysubscriptionaddiction, hellosubscription) produced multiple Tier-A
-  candidates in batch-1", claim_role: load_bearing}]`. assumptions:
+  candidates in batch-1", claim_role: load_bearing, evidence_unit_ids:
+  [batch-1 Screen Provenance]}]`. assumptions:
   `[{statement: "decision-shaped events (repricing, channel entry) surface in
-  dedicated review blogs before general communities", evidence_refs: [batch-1
+  dedicated review blogs before general communities", evidence_unit_ids: [batch-1
   Screen Provenance], would_flip_if_false: true}]`. lessons_consulted:
   `pending_interface (near-half ledger not yet durable)`. reasoning_trace:
   "batch-1's only proven candidate venues are blogs; the family constraint
```

Note: the diff block above is informational. The working tree diff is the source of truth for adjudication.

## Per-Change Neutral Citations

Vocabulary hunk citations:

- `orca-harness/schemas/judgement_models.py` defines `LoadBearingAssumption.statement`, `LoadBearingAssumption.evidence_unit_ids`, and `LoadBearingAssumption.would_flip_if_false`.
- `orca-harness/schemas/judgement_models.py` defines `EvidenceUsed.claim_text`, `EvidenceUsed.claim_role`, and `EvidenceUsed.evidence_unit_ids`; `claim_role` is limited to `load_bearing`, `supporting`, or `contextual`.
- Target architecture §1 names `signals_used` as a live signal pre-commitment, while the pending near-half interface requires stable signal identity; the patch preserves `signal_id` for that loop-specific role.

Entry-mechanics hunk citations:

- Target architecture §1 makes `actual_path` a first-class field group and states updates are their own sealed calls scored against their own information set.
- Target architecture "Minimal governance" requires an append-only seal registry, replay, and quarantine-as-data breach handling.
- Target spec's own fitness test requires zero invented semantics for by-hand operation.

## Verdict As Decision Input

Recommendation: keep the bounded patch subject to home-model hunk-by-hunk adjudication. The defects were patch-level, source-supported, and did not require `NEEDS_ARCHITECTURE_PASS`.

No separate validation was run because this is a documentation semantics artifact and the defects are not executable test failures. Verification performed: hash preflight, source-read comparison, scoped diff review, and string checks for the renamed vocabulary.

## Residual Risk

- The target still depends on a future owner-signed Phase-1 pilot ledger and a future near-half signal-reliability interface. This patch does not create either.
- The exact filename ordering for multiple update seals may need pilot-ledger operational tightening, but the current patch supplies the missing semantic hooks: actual-path entry, resolved-seal identity, latest-prior-entry chain, and per-scoreable-seal resolution.
- The worked example remains illustrative only and was not turned into a sealed decision, fixture, or evidence record.

## Review-Use Boundary

This report and diff are advisory decision input. They are not approval, validation, mandatory remediation, pilot authorization, readiness, or evidence-tier promotion. The commissioning/home model decides what, if anything, is kept.

## Delegated Return Courier

DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target: `docs/prompts/reviews/prospective_loop_phase0_semantics_spec_delegated_adversarial_artifact_review_patch_prompt_v0.md`
- reviewed artifact and bounded patch scope: `docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md`; only this target plus this report were written
- findings and source evidence: AR-01 vocabulary trace drift; AR-02 entry mechanics gap for actual_path/update-seal resolution
- proposed artifact patch or exact suggested edits: uncommitted working-tree diff included above and available from `git diff`
- citations: harness `judgement_models.py`, target architecture §1 and minimal governance, batch-1 Screen Provenance for the example source reference
- reviewer verdict: keep subject to CA adjudication; no `NEEDS_ARCHITECTURE_PASS`
- residual risk: future pilot ledger and near-half interface still pending; no validation/readiness claim
- blockers, off-scope flags, and not-proven boundaries: no blockers; no off-scope files patched; validation/readiness/acceptance/pilot authorization remain not proven

## Home-Model Adjudication (2026-06-13, appended by the commissioning lane)

```yaml
home_model_adjudication:
  adjudicator: claude-fable-5[1m] (author/home model; correlation disclosed — every hunk re-checked against judgement_models.py and the landed architecture directly, not against the controller's verdict)
  diff_verified: working-tree diff matched the report's Unified Diff (4 hunks, index c985972..367f364) before adjudication
  per_hunk:
    - hunk: vocabulary trace table (AR-01)
      decision: accepted
      basis: LoadBearingAssumption.evidence_unit_ids and EvidenceUsed.claim_text/claim_role/evidence_unit_ids verified field-for-field in judgement_models.py; the original evidence_refs/description names were silent renames contradicting the spec's own zero-unmapped-names claim
    - hunk: sealed_call fill-rules (AR-01)
      decision: accepted_with_modification
      basis: harness alignment correct; modification appended by adjudicator — one clause stating evidence_unit_ids values at this tier are retrieval handles and no EvidenceUnit is bound (JSG-01 stays frozen), closing an implied-binding ambiguity the rename fix alone left open
    - hunk: entry mechanics + chain rule (AR-02)
      decision: accepted
      basis: actual_path had a fill-rule but no entry file (operator invention required — fails the spec's own fitness bar); single-resolution shape contradicted the architecture's every-prior-seal-still-resolves rule once update-seals exist; dual-hash chain strengthens ordering proof without weakening any invariant
    - hunk: worked example (AR-01)
      decision: accepted
      basis: consistency with the vocabulary hunks; controller string-check confirms no stale names remain
  vetoes: none
  modifications:
    - one clause added to the signals_used fill-rule (JSG-01/retrieval-handle boundary), recorded above
  kept_state: all 4 hunks + 1 adjudicator clause committed on phase0-semantics-spec-v0 (PR #46)
  residuals_carried:
    - update-seal filename ordering tightening deferred to the pilot-ledger declaration (controller residual, accepted)
  non_claims:
    - adjudication is a keep-decision only; not validation, readiness, ratification, acceptance, or pilot authorization
    - the spec remains PROPOSED at product-learning tier
```
