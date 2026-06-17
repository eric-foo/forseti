# Unity Runtime Fee Case Index

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Case index for the Unity Runtime Fee Judgment Spine case.
use_when:
  - Locating Unity Runtime Fee case artifacts before extracting or comparing judgment lessons.
  - Checking which Unity artifacts exist and which remain missing for blind reuse.
  - Avoiding accidental reuse of revealed material as blind input.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md
  - docs/research/judgment-spine/manifest_v0.md
  - docs/product/foundation/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md
  - docs/product/foundation/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md
  - docs/product/foundation/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S1 plus target Judgment Spine and Unity specimen artifacts
  edit_permission: docs-write
  target_scope: Package the existing Unity Runtime Fee specimen into the Judgment Spine case index shape used by Milwaukee.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Case Snapshot

- case_name: Unity Runtime Fee monetization crossroads
- decision_family: platform pricing, packaging, monetization, ecosystem trust, and implementation risk
- cutoff: `2023-09-11 23:59 Pacific Time`
- spoiler_state: revealed
- learning_status: useful avoided-false-commit lesson; transfer not proven
- learnability_tier: Tier 0 candidate, because the case has a clear decision owner context, cutoff, pre-cutoff source packet, sealed at-cutoff memo, owner blind-read input, revealed outcome, and calibration lesson

## Existing Artifacts

| Artifact | Path | Use |
| --- | --- | --- |
| Reveal readout | `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md` | Post-reveal learning capsule and reusable lesson surface |
| Pre-cutoff source packet | `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md` | Phase 0 case frame and Phase 1 pre-cutoff public source packet |
| Sealed at-cutoff memo | `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md` | Internal sealed decision memo written before outcome calibration |
| Outcome calibration | `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md` | Post-seal comparison against revealed outcome and owner blind-read judgment |
| Adjacent MV-04 method replay | `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` | Secondary method-validation evidence; do not treat as the canonical specimen source |

## Missing Residue

These files are not present in the case folder and should not be implied:

- `docs/research/judgment-spine/cases/unity-runtime-fee/participant_packet_v0.md`
- `docs/research/judgment-spine/cases/unity-runtime-fee/safety_receipt_v0.md`
- `docs/research/judgment-spine/cases/unity-runtime-fee/blind_judgments_v0.md`

The owner blind-read judgment exists inside
`docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`,
not as a separate consolidated blind-judgments file.

Do not reconstruct missing residue from memory. If later authorized, create a
participant packet only from clean pre-cutoff inputs and keep the sealed memo,
owner blind read, outcome facts, and revealed calibration out of participant
view.

## First Reusable Lesson

Commercial pressure is not launch authority when the pricing mechanism itself
changes the customer bargain.

For Unity, the sharper consulting posture was not merely "narrow and phase."
It was: hold any broad runtime/install-based fee; introduce a runtime-fee
category only if a tiny, customer-accepted, future-version-only or opt-in wedge
proves it can exist without ecosystem shock; otherwise prefer less
trust-damaging monetization such as subscription thresholds, enterprise
packaging, and cost control.

## Use Boundary

Use this case to sharpen judgment about platform pricing, monetization pressure,
mechanism psychology, implementation cost, grandfathering, segment exemptions,
and action-ceiling discipline.

Do not use this case as proof that runtime fees are always wrong, that public
developer backlash was fully predictable at cutoff, that Orca has a validated
product, or that a source system, miner, fine-tuning dataset, or implementation
program should be built.

## Non-Claims

- No buyer validation.
- No willingness-to-pay proof.
- No repeatability proof.
- No product readiness.
- No feature readiness.
- No implementation readiness.
- No commercial readiness.
- No model-training readiness.
- No fine-tuning readiness.
- No complete blind participant packet in this case folder.
- No proof that the Unity lesson transfers across cases.
