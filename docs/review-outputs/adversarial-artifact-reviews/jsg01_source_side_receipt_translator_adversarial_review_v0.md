```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md
  recommendation: patch_before_acceptance
  summary: "The translator is directionally sound and preserves the no-fork/finalization boundary, but the Canoo/Walmart replay overclaims source-side clearance on current/live captured bytes that do not prove pre-cutoff visibility."
  findings_count: 3
  blocking_findings:
    - AR-01: Canoo/Walmart replay clears despite unproven historical/pre-cutoff source-byte visibility
  advisory_findings:
    - AR-02: SP-1 resolved value is under-evidenced for actor/audience category and manifest resolution
    - AR-03: Hash-basis drift is treated as non-load-bearing even though SP-2 depends on what the hash covers
  prior_findings_remediated: []
  next_action: "Owner should authorize a narrow patch or decide that current/live source-byte capture is sufficient for this first slice before ratifying the translator."
```

# JSG-01 Source-Side Receipt Translator Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Read-only adversarial artifact review of the proposed JSG-01 source-side
  receipt translator, bounded to owner ratification input before JSG-01 unfreezes.
use_when:
  - Consuming the independent review of the proposed source-side translator.
  - Deciding whether to ratify, patch, or reject the JSG-01 first slice.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/source_side_receipts/jsg01_source_side_receipt_translator_v0.md
  - docs/prompts/reviews/jsg01_source_side_receipt_translator_adversarial_review_prompt_v0.md
  - .agents/workflow-overlay/review-lanes.md
```

- Status: REVIEW_COMPLETE_ADVISORY
- Artifact type: Adversarial artifact review report
- Commissioning prompt: `docs/prompts/reviews/jsg01_source_side_receipt_translator_adversarial_review_prompt_v0.md`
- Review target: `docs/product/jsg01_source_side_receipt_translator_v0.md`
- Output mode used: `review-report`
- Reviewer edit permission: read-only; this report written under `docs/review-outputs/adversarial-artifact-reviews/`
- Patch queue authorized: no
- Implementation, validation, ratification, gate clearance, commit, push, runtime work, or product-proof authorized: no

---

## 1. Source Context Status

```yaml
source_context_status: SOURCE_CONTEXT_READY
target_hash_status:
  path: docs/product/jsg01_source_side_receipt_translator_v0.md
  expected_sha256: 2F6F3C4760AE554FF12D7A500882B43682E08B28D5F41718018B869A5EDFFA1B
  observed_sha256: 2F6F3C4760AE554FF12D7A500882B43682E08B28D5F41718018B869A5EDFFA1B
  result: match
workspace_state:
  branch: main
  observed_head: f9b05e6
  dirty_state: dirty
strict_claim_boundary: >
  Dirty and untracked controlling sources support advisory review only.
  Strict PASS, readiness, acceptance, ratification, validation, source-of-truth,
  gate-clearance, fixture-admission, or judgment-quality claims remain not proven.
```

All required read-pack sources were available. One narrow extra source was read:
`docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_acquisition_receipt_v0.md`,
because the translator's Canoo/Walmart SP-2 replay depends on source-byte hash
provenance.

Method status:

- `workflow-deep-thinking`: REFERENCE-LOAD completed before source loading; APPLIED after `SOURCE_CONTEXT_READY` to frame the boundary problem and failure modes.
- `workflow-adversarial-artifact-review`: REFERENCE-LOAD completed before source loading; APPLIED after `SOURCE_CONTEXT_READY` to produce findings.

Source-state ledger:

| Source | Why read | Source state observed |
| --- | --- | --- |
| `AGENTS.md` | Workspace rules and durable-claim verification boundary | modified |
| `.agents/workflow-overlay/README.md` | Orca overlay entrypoint and precedence | modified |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial artifact review lane and output boundary | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | `review-report` output contract and prompt gates | modified |
| `.agents/workflow-overlay/validation-gates.md` | Receipt-field provenance gate | not listed dirty in targeted status |
| `.agents/workflow-overlay/communication-style.md` | `review_summary` YAML shape | modified |
| `.agents/workflow-overlay/source-loading.md` | Start preflight and source-read ledger rules | modified |
| `docs/product/jsg01_source_side_receipt_translator_v0.md` | Reviewed target | untracked; hash matched prompt |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | IPF Evidence Unit Standard | not listed dirty in targeted status |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Ob.7/8/9/12/16 source and cutoff obligations | not listed dirty in targeted status |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Inclusion State Rule and ECR/Evidence Unit consolidation boundary | modified |
| `docs/product/judgment_quality_promotion_operating_model_v0.md` | JSG-01 row and receipt-provenance sub-rule | not listed dirty in targeted status |
| `docs/product/judgment_spine_gate_ownership_map_v0.md` | JSG-01 ownership surface | not listed dirty in targeted status |
| `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md` | AR-01/03/04/05 and finalization boundary | untracked |
| `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` | Harness EvidenceUnit reference fields | untracked |
| `orca-harness/schemas/case_models.py` | Current code EvidenceUnit field set | not listed dirty in targeted status |
| `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md` | Canoo/Walmart replay fixture | not listed dirty in targeted status |
| `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_acquisition_receipt_v0.md` | Canoo/Walmart source-byte hash provenance | not listed dirty in targeted status |
| `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md` | Unity replay fixture | untracked |

---

## 2. Findings

### AR-01 - Canoo/Walmart replay clears despite unproven historical/pre-cutoff source-byte visibility

- Severity: critical
- Phase: correctness
- Seam attacked: determinacy is real; provenance soundness; scope honesty
- Target anchor: `Worked validation replay (Canoo/Walmart + Unity)`, especially lines 240-251
- Source authority used: IPF Evidence Unit Standard, Data-Capture Ob.8/9/11/12, Canoo/Walmart evidence registry, Canoo/Walmart source-acquisition receipt
- Patch queue authorized: no

Artifact evidence:

- The target says Canoo/Walmart SP-2 clears because units have "real sha256 per unit + source_acquisition_receipt bytes" and SP-3 clears because 2022-01 through 2022-06 timestamps precede the cutoff (`docs/product/jsg01_source_side_receipt_translator_v0.md:242`, `:245`, `:246`).
- It then concludes: "DETERMINATE - source-side clears; the single residual is finalization authority" (`docs/product/jsg01_source_side_receipt_translator_v0.md:250`).

Contrary source evidence:

- IPF makes pre-cutoff visibility required for cutoff-sensitive claims (`docs/product/core_spine_v0_information_production_foundation_v0.md:95`) and treats unavailable source visibility as blocked (`docs/product/core_spine_v0_information_production_foundation_v0.md:142`-`:147`).
- Data Capture says live or mutable sources must distinguish edit/capture/cutoff timing and mark mixed or unknown when item-level timing does not make the boundary clear (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:252`-`:255`), and that cutoff posture must be visible enough for downstream Judgment rules (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:260`-`:274`).
- The Canoo/Walmart source-acquisition receipt says the bytes are current live public web bytes captured on 2026-05-30 for CW-P1 through CW-P5 plus owner-supplied local SEC bytes for CW-P6, and explicitly says it "does not prove that the pages are unchanged from their original publication dates" (`docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_acquisition_receipt_v0.md:39`-`:44`).
- The same receipt records SHA-256 over captured local file bytes, not historical/archive source bytes (`docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_acquisition_receipt_v0.md:52`-`:61`).

Why this matters:

The translator's central proof signal is that one real case clears the
source-side subpredicates and leaves only SP-5 finalization. That claim is too
strong under the source-side rules as loaded. Current/live captured bytes can
make source bytes inspectable now, but they do not by themselves prove that the
source bytes were pre-cutoff visible, unchanged, or free of post-window edits.
For a cutoff-sensitive backtest, that is exactly the risk SP-3 is supposed to
surface rather than hide.

This does not prove Canoo/Walmart cannot clear. It proves the current replay
cannot claim Canoo/Walmart clears source-side without either a historical/archive
visibility basis or an owner-accepted rule that current/live captures of these
source families are sufficient for this first slice.

Minimum closure condition:

The Canoo/Walmart replay must no longer clear SP-2/SP-3 solely from current/live
2026 captured bytes plus pre-cutoff publication dates. Either the replay must
bind source-byte visibility to historical/archive/cutoff-window provenance, or
it must explicitly mark the affected source-side posture as `unknown`, `mixed`,
or otherwise not-cleared pending owner acceptance of current/live capture
sufficiency.

Next authorized action:

Owner decision or patch-authorization request. A read-only reviewer cannot patch
the translator or create the sufficiency rule.

Verification evidence needed for future closure:

Line-cited source-acquisition evidence showing historical/archive or owner-
accepted current/live sufficiency for each Canoo/Walmart source, then a rerun of
the SP-2/SP-3 replay against the same closed values. Red-green proof is
not_applicable for this non-executable artifact finding.

### AR-02 - SP-1 `resolved` value is under-evidenced for actor/audience category and manifest resolution

- Severity: major
- Phase: correctness
- Seam attacked: closed values are sourced, not invented; determinacy is real
- Target anchor: `SP-1 source-identity` and adapter row for `source_identity_state`
- Source authority used: IPF, Data-Capture Ob.7, Pydantic schema reference, current `case_models.py`, Canoo/Walmart registry, Unity registry
- Patch queue authorized: no

Artifact evidence:

- The target defines `resolved` as requiring a specific locator/citation/archive
  reference or a resolving owner/facilitator source id, plus an actor/audience
  category present and non-placeholder (`docs/product/jsg01_source_side_receipt_translator_v0.md:105`-`:108`).
- The adapter rule maps `source_id` + `source` to `resolved` if both are non-placeholder and the `source_id` resolves in the source manifest (`docs/product/jsg01_source_side_receipt_translator_v0.md:211`-`:214`).
- The worked replay calls Canoo/Walmart `resolved` and Unity EU-01..07 `resolved` (`docs/product/jsg01_source_side_receipt_translator_v0.md:244`, `:260`).

Contrary or under-specified source evidence:

- IPF separates "Source locator or source family" from "Source actor or audience type" (`docs/product/core_spine_v0_information_production_foundation_v0.md:91`-`:92`).
- Ob.7 requires source surface/family, actor or audience category where knowable, and visible marking when actor specificity is unavailable (`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md:226`-`:235`).
- The Pydantic `EvidenceUnit` reference includes `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, and `pre_decision_status`, but no actor/audience category field (`docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md:64`-`:72`).
- Current `case_models.py` likewise has no actor/audience category field on `EvidenceUnit` (`orca-harness/schemas/case_models.py:53`-`:63`).
- Canoo/Walmart has a source-manifest draft with source roles that could support actor/source-family categories (`docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/evidence_registry_draft_v0.md:41`-`:49`), but Unity's loaded registry evidence is just per-unit URLs/source IDs and does not show a resolved manifest or explicit actor/audience field for EU-01..07 (`docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md:52`-`:59`, `:160`-`:167`).

Why this matters:

The issue is not that SP-1 must fail. The issue is that the target's exact
`resolved` value is not replayed from all fields its own definition requires.
The likely defensible value for some units may be `family_only` or a `resolved`
value whose actor/category is sourced from a separate manifest or source packet.
But the report as written lets `source_id` + `source` silently stand in for a
full actor/audience category check.

Because `family_only` also clears under the proposed rule, this may not change
the final SP-1 clear/non-clear outcome. It does change the determinacy claim and
the closed-value replay. A receipt translator should be strict about exact
values, not just final clear status.

Minimum closure condition:

The SP-1 replay must either cite the actor/audience or source-family category
evidence used for each `resolved` value, or downgrade units to `family_only` /
`unresolved` as the loaded fixture evidence permits. If actor/audience category
is intentionally optional when a specific locator exists, the `resolved`
definition must say that explicitly rather than requiring it and then skipping it.

Next authorized action:

Patch-authorization request for the target, or owner decision that the
source-side first slice should relax the `resolved` definition.

Verification evidence needed for future closure:

Line-cited replay table showing each unit's `source_identity_state`, the exact
locator/manifest/category evidence behind it, and the resulting clear/non-clear
status. Red-green proof is not_applicable for this non-executable artifact
finding.

### AR-03 - Hash-basis drift is treated as non-load-bearing even though SP-2 depends on what the hash covers

- Severity: major
- Phase: correctness
- Seam attacked: provenance soundness; adapter stability / three-representation drift
- Target anchor: `SP-2 inspectability` and `Three-representation drift`
- Source authority used: packing interface AR-03, Pydantic schema reference, current `case_models.py`, Canoo/Walmart source-acquisition receipt, Unity registry
- Patch queue authorized: no

Artifact evidence:

- SP-2 clears only on `inspectable_verifiable`, defined as an inspectable observation plus a verifiable integrity anchor (`docs/product/jsg01_source_side_receipt_translator_v0.md:133`-`:148`).
- The target acknowledges that `case_models.py` carries `source_type` and `hash_basis` while the Pydantic reference and fixture drafts lack them, then says `hash_basis` only further supports SP-2 and is not required for clearing (`docs/product/jsg01_source_side_receipt_translator_v0.md:223`-`:233`).

Contrary or under-specified source evidence:

- AR-03 requires source bytes or an inspectable reference to reach the Harness so a hash can be recomputed and verified (`docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md:123`-`:135`), and treats `bytes_available: true` without a verifiable hash or recomputation basis as a packing-side block condition (`docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md:176`-`:179`).
- The Pydantic reference says `hash` is `sha256(source_bytes)` when source bytes are available (`docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md:76`).
- Current `case_models.py` requires `hash_basis` on `EvidenceUnit` (`orca-harness/schemas/case_models.py:53`-`:63`).
- Canoo/Walmart can supply a hash-basis equivalent through its acquisition receipt: all hashes are SHA-256 over captured local file bytes (`docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_acquisition_receipt_v0.md:52`).
- Unity cannot: every EU-01..EU-07 hash is `TBD_SOURCE_BYTE_HASH`, and EU-07 still needs archive CDX digest or source-byte hash recovery (`docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md:55`-`:58`, `:163`-`:170`).

Why this matters:

The translator is right that the current fixtures can sometimes provide a
hash-basis equivalent outside the `EvidenceUnit` object. Canoo/Walmart does so
through the source-acquisition receipt. But the target's stronger statement that
`hash_basis` is not required for clearing is too broad. SP-2 does not merely ask
whether a hash-shaped string exists; it asks whether the integrity anchor is
independently verifiable. That requires knowing what bytes or reference the hash
covers, whether through `hash_basis`, a source-acquisition receipt, or another
owner-bound equivalent.

Minimum closure condition:

The SP-2 rule must require a hash-basis equivalent for any clearing
`inspectable_verifiable` value, even if that equivalent is not literally the
`hash_basis` field. The three-representation drift section must stop implying
that hash coverage is only optional support.

Next authorized action:

Patch-authorization request. This is a wording and replay-boundary correction,
not permission to change code or fixtures.

Verification evidence needed for future closure:

Line-cited SP-2 language requiring recomputation basis, plus per-fixture evidence
showing where that basis is recorded. Red-green proof is not_applicable for this
non-executable artifact finding.

---

## 3. Non-Findings

NF-01 - Canonical home / no-fork mostly holds.

The target authors source-side fields in IPF/Data-Capture terms and keeps the
harness as adapter target, not field home (`docs/product/jsg01_source_side_receipt_translator_v0.md:50`-`:59`,
`:81`-`:89`). The boundary source supports citing the IPF Evidence Unit standard
until later ECR/Evidence Unit consolidation (`docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md:131`-`:134`), and the target does not apply a conductor predicate edit.

NF-02 - SP-2 byte-verifiability is defensible, including the Unity EU-07 result.

The stricter choice to not clear `inspectable_reference_only` is supported by
AR-03's recomputation requirement and the receipt-field provenance gate. Unity
EU-07 has a real archive URL and pre-cutoff timestamp, but still has
`TBD_SOURCE_BYTE_HASH` and explicitly needs CDX digest or source-byte hash
recovery (`docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md:160`-`:170`).
That is a visible limitation, not a false failure.

NF-03 - Finalization firewall holds.

The target keeps SP-5 owner-reserved, defines no finalization field or authority,
and treats SP-4 as value-determinate but necessary-not-sufficient
(`docs/product/jsg01_source_side_receipt_translator_v0.md:176`-`:203`). This is
consistent with the packing interface's open owner decision about who finalizes
evidence `pre_decision_status` (`docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md:190`-`:192`).

NF-04 - Conductor reference is staged as a pointer, not a predicate edit.

The target explicitly says the conductor reference is proposed, not applied, and
that JSG-01 stays frozen until ratification (`docs/product/jsg01_source_side_receipt_translator_v0.md:274`-`:290`).
This avoids a stealth gate flip.

NF-05 - Scope honesty mostly holds.

The target repeatedly says it is proposed, not ratified, not validation, not
readiness, not fixture admission, and not gate clearance (`docs/product/jsg01_source_side_receipt_translator_v0.md:34`-`:38`,
`:340`-`:346`). The exception is AR-01: the internal Canoo/Walmart replay
overstates what the current source acquisition actually proves.

---

## 4. Not-Proven Boundaries

- Cross-family independence is not proven by this report. The prompt says the owner should dispatch the review to a different model family, but runtime model routing is outside Orca review-lane authority.
- Ratification is not proven. The owner has not ratified the source-side field slice in the reviewed target or in this review.
- JSG-01 remains frozen / indeterminate. This review does not unfreeze the gate.
- Validation, readiness, fixture admission, judgment-quality evidence, buyer-proof, implementation authorization, runtime behavior, tests, commits, pushes, and PRs are not proven and not authorized.
- The review did not establish that the translator works for cases beyond Canoo/Walmart and Unity.
- Dirty and untracked controlling sources support advisory findings only. They do not support strict PASS, acceptance, source-of-truth, validation, readiness, or proof claims.

---

## 5. Recommendation

Recommendation: `patch_before_acceptance`.

The translator should not be ratified as-is because its main positive replay
signal overclaims Canoo/Walmart source-side clearance. The architecture is still
salvageable and mostly well-bounded: no-fork posture, SP-2 strictness, SP-5
finalization firewall, and staged conductor reference all hold. The narrow
repair is to make the replay and SP-2/SP-3 provenance boundary as strict as the
translator's own doctrine requires.

Review-use boundary: findings are decision input for the owner only. They are
not approval, validation, ratification, mandatory remediation, gate-clearance,
or patch authority until separately accepted or authorized.
