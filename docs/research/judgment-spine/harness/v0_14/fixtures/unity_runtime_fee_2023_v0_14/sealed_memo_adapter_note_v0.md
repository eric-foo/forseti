# Unity Runtime Fee Sealed Memo Adapter Note v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Adapter note for the legacy Unity sealed at-cutoff memo in the v0.14 draft fixture pack.
use_when:
  - Deciding whether the sealed Unity memo can be adapted into a v0.14 BlindJudgement.
  - Preserving non-comparability between the legacy memo and future fresh contestant outputs.
  - Checking memo-adapter blockers before any scoring or baseline comparison.
authority_boundary: retrieval_only
input_hashes:
  fixture_authoring_prompt: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
  extraction_plan: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  source_packet: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  legacy_sealed_memo: 2DB46EEF3D6ED6F54451693DC33B5B789066EB1BF26946370B702601650A3C30
  pydantic_schema_reference: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  case_construction_protocol: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
  post_authoring_review: BB1EAD239DF2A1EE5704B888BD5F1F261B0E2DD2D656E5FCB4330708A19C674C
open_next:
  - docs/product/core_spine/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md
  - docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
```

- Status: SEALED_MEMO_ADAPTER_NOTE_ONLY
- Case ID: `unity_runtime_fee_2023_v0_14`
- Adapter status: not adapted
- Scoring status: not score-ready
- Comparability status: not comparable to fresh contestant outputs

## Default Treatment

Treat the existing Unity at-cutoff memo as advisory or baseline-like legacy material. It is not a fresh contestant run, not a v0.14 `BlindJudgement`, not scoring truth, and not directly comparable to a future model output unless a later adapter lane proves comparability.

The memo may remain useful as parent Judgment Spine calibration material because it was written against the sealed pre-cutoff source packet and did not open post-cutoff sources. That provenance does not make it schema-valid for v0.14 scoring.

## Required Adapter Gaps

| Required area | Current gap |
| --- | --- |
| `decision_shape` | Must be frozen from the v0.14 allowed set. Leading candidate is `ceiling_trap`; `action_band` is possible. The legacy memo predates this field. |
| `judgement_class` | Must map to one of `recommend`, `abstain`, `wait`, `escalate`, or `irreducible_uncertainty`. The legacy memo recommendation should not receive a hindsight class assignment. |
| Run metadata | Missing v0.14 `contestant_id`, `run_id`, `model_id`, `model_family`, `model_snapshot_if_available`, `temperature`, `seed_if_supported`, `harness_version`, and `created_at` in the required runner sense. |
| Prompt hash | Memo has a source packet hash, but not a v0.14 rendered-prompt hash. |
| Participant packet hash | No v0.14 participant packet existed when the memo was written. |
| Facilitator ledger hash | No v0.14 facilitator ledger existed when the memo was written. |
| Evidence IDs | Memo cites EU-01 through EU-08 in prose, but v0.14 requires structured `evidence_used` claims with evidence unit IDs. |
| Must-address coverage | No frozen must-address list existed when the memo was written; coverage cannot be reconstructed as if it had existed. |
| Recommended action mapping | The memo's recommendation and action ceiling would need ladder-level mapping without hindsight. |
| Author-context contamination | The memo may reflect author expertise, source-selection context, prompt context, and assumptions not available to a future clean contestant. |

## Recommended Handling

```yaml
current_handling: retain_as_parent_judgment_spine_calibration_material
future_adapter_candidate: yes
exclude_from_v0_14_scoring_now: yes
exclude_from_fresh_contestant_comparison_now: yes
```

Retain the memo as parent Judgment Spine material and as a future adapter candidate. Exclude it from v0.14 scoring unless a later docs-only or implementation-authorized adapter lane can represent all required fields without fabrication and without hiding author-context contamination.

If the adapter cannot preserve these caveats, keep the memo outside v0.14 scoring permanently for this fixture and use it only for parent case-learning comparison.

## Non-Comparability Warning

Do not compare the legacy sealed memo to fresh contestant outputs as if all parties saw the same packet, prompt, runner contract, ledger, evidence registry, and hash-pinned fixture.

Fresh contestants would see a v0.14 participant packet and run under a v0.14 prompt and runner contract. The legacy memo saw an earlier source-packet context, no v0.14 facilitator ledger, no frozen must-address list, no v0.14 decision shape, no v0.14 prompt hash, no participant packet hash, and no ledger hash.

Any comparison before those differences are represented would overstate baseline meaning and contaminate scoring interpretation.

## What A Future Adapter Must Prove

A future adapter lane must prove or explicitly label:

- whether the memo is excluded, retained only as parent calibration material, or adapted as a legacy baseline-like contestant;
- exact `decision_shape`;
- exact `judgement_class`;
- recommended action ladder level and label;
- structured `evidence_used` claim IDs, roles, and evidence unit IDs;
- must-address coverage against a frozen must-address list;
- prompt hash or explicit absence of a rendered-prompt hash;
- participant packet hash or explicit absence because no v0.14 packet existed;
- facilitator ledger hash or explicit absence because no v0.14 ledger existed;
- full run metadata gaps;
- author-context contamination caveat;
- non-comparability caveat in any case report or review surface.

## Not Authorized Here

This note does not adapt the memo, run schema validation, run a model, run a probe, compute scores, create a case report, create failure events, or make baseline claims.
