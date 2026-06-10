# Milwaukee Fiscal Crossroads Case Index

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Case index for the Milwaukee fiscal-crossroads Judgment Spine case.
use_when:
  - Locating Milwaukee case artifacts before extracting or comparing judgment lessons.
  - Checking which Milwaukee artifacts exist and which remain missing.
  - Avoiding accidental reuse of revealed material as blind input.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md
  - docs/research/judgment-spine/manifest_v0.md
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S1 plus target Judgment Spine artifacts
  edit_permission: docs-write
  target_scope: Create a Milwaukee case index that preserves navigation, spoiler state, and missing residue.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Case Snapshot

- case_name: Milwaukee fiscal crossroads
- decision_family: public-sector fiscal stabilization under deadline pressure
- cutoff: `2023-07-10 23:59 CT`
- spoiler_state: revealed
- learning_status: useful single-case lesson; transfer not proven
- learnability_tier: Tier 0 candidate, because the case has a real decision owner, material fiscal tradeoff, deadline pressure, revealed action, and a concrete judgment miss around fallback triggers

## Existing Artifacts

| Artifact | Path | Use |
| --- | --- | --- |
| Reveal readout | `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md` | Post-reveal learning capsule and reusable lesson surface |
| Initial blind judgment | `docs/decisions/consultant_loop/milwaukee_initial_judgement.md` | Sealed initial judgment, stored outside this case folder |
| Owner judgment | `docs/decisions/consultant_loop/milwaukee_owner_judgement.md` | Owner judgment and critique, stored outside this case folder |

## Missing Residue

These files are not present in the case folder and should not be implied:

- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/participant_packet_v0.md`
- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/safety_receipt_v0.md`
- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/blind_judgments_v0.md`

Do not reconstruct these from memory. If later authorized, create them only from source-visible inputs and label any unavailable source gaps.

## First Reusable Lesson

A counteroffer becomes executive advice only when it has a fallback trigger, a walkaway line, and implementation guardrails.

For Milwaukee, the sharper consulting posture was not pure accept or pure reject. It was: make the cleaner counteroffer immediately, then accept the ugly but bankable package if no same-scale recurring substitute or cleaner state deal is legally available by the hard budget deadline.

## Use Boundary

Use this case to sharpen judgment about ugly-but-bankable options, deadline pressure, counteroffer discipline, and separating a good mechanism from a bad package.

Do not use this case as proof that the pattern transfers broadly, that Orca has a validated product, or that consulting-firm public cases are generally sufficient for blind backtests.

## Non-Claims

- No buyer validation.
- No willingness-to-pay proof.
- No repeatability proof.
- No product readiness.
- No feature readiness.
- No implementation readiness.
- No commercial readiness.
- No model-training readiness.
- No complete backtest packet in this folder.
- No proof that the Milwaukee lesson transfers across cases.
