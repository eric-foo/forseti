# Packing Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door (Packing serialization spine)
scope: >
  Front-door for the packing spine: the model-facing serialization layer
  between evidence assembly and Judgment. Routes to the serialization
  contract (boundary, invariants, versioning, adapter contract) and the
  current capability declaration.
use_when:
  - Entering the packing spine or deciding whether a behavior is packing-owned.
  - Authoring or reviewing a packing adapter for a new judgment lane or view.
  - Checking what packing may claim (encoding, determinism, citation passthrough) and what it never does (select, label, score, store).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/packing/authority/packing_spine_v0_serialization_contract_v0.md
  - forseti/product/spines/packing/authority/packing_spine_v0_columnar_mgt_declaration_v0.md
  - docs/research/packing-phase/README.md
  - docs/decisions/packing_judgment_scaling_owner_agreement_register_v0.md
  - docs/research/judgment-spine/evidence_condensation_hierarchy_deferred_direction_v0.md
stale_if:
  - The serialization contract is amended or superseded.
  - The capability declaration (MGT) is amended or superseded (e.g. a GT upgrade).
  - The packing code home moves from forseti-harness/packing/.
```

## What this spine is

`packing` is a **shared serialization spine**: it turns an already-selected,
already-frozen evidence set into the exact bytes a model sees, and turns those
bytes back losslessly. It sits between assembly and Judgment and is consumed by
every judgment lane.

- **Produced for:** judgment lanes (creator-audience today; retail and future
  lanes when they define model-facing views; condensation-hierarchy rounds when
  commissioned).
- **Fed by:** evidence assembly (evidence binding today; the pull-to-assemble
  loop later). Assembly selects and freezes the set; packing serializes it.
- **Owns:** model-facing serialization (pack/unpack, envelope versions, the
  adapter contract), the deterministic frozen *form* of a bundle and its
  verification (declared; implementation deferred), and the packing invariants
  every adapter must satisfy.
- **Does not own:** evidence selection, inclusion, labeling, scoring, or
  repair (Judgment/assembly); the freeze *event* (assembly); storage or
  retrieval (data lake); prompt instructions, method decks, or response shapes
  (judgment lanes); condensation (a Judgment act).

The binding authority is
`authority/packing_spine_v0_serialization_contract_v0.md`. The earlier
Packing Phase boundary note (`docs/research/packing-phase/README.md`) remains
the phase-process research record; boundary authority now lives here.

## Subfolder grammar

| Folder | Holds |
| --- | --- |
| `authority/` | serialization contract, invariants, capability declarations |

Runtime code and tests stay in `forseti-harness/packing/` and
`forseti-harness/tests/`; this spine holds contracts, never code.

## Status

Spine created 2026-07-21 on owner direction ("i will 100% be using it often,
let's plan out a spine for it too"). Current capability: columnar packer v0
(payload-agnostic core + creator-audience adapter, PR #1213), declared Mini
God Tier with named accepted residuals in
`authority/packing_spine_v0_columnar_mgt_declaration_v0.md`.

Non-claims: not validation, readiness, or runtime authorization; placement and
routing shape only.
