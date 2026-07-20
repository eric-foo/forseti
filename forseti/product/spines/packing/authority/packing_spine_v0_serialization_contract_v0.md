# Packing Spine v0 Serialization Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Spine authority contract
scope: >
  Binds the Packing Spine boundary, the five serialization invariants, envelope
  versioning discipline, the adapter contract every new consumer must satisfy,
  and the declared-but-deferred frozen-form verification responsibility.
use_when:
  - Authoring a packing adapter for a new judgment lane, view, or evidence kind.
  - Changing the packing core, an envelope version, or any packed surface.
  - Adjudicating whether a proposed behavior belongs to packing or a neighbor.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/packing/README.md
  - forseti/product/spines/packing/authority/packing_spine_v0_columnar_mgt_declaration_v0.md
  - forseti-harness/packing/columnar.py
  - forseti-harness/packing/creator_audience_adapter.py
  - forseti-harness/tests/unit/test_packing_columnar_v0.py
  - docs/decisions/packing_judgment_scaling_owner_agreement_register_v0.md
stale_if:
  - An accepted later contract amends the boundary, invariants, or versioning rules.
  - The frozen-form verification responsibility is implemented or reassigned.
  - The packing code home moves from forseti-harness/packing/.
```

## Status

Owner-commissioned 2026-07-21 (in-thread: spine planning requested and the
recommended contract-first shape ratified with "proceed"). This contract binds
boundary, invariants, and adapter obligations. It is not validation, readiness,
or implementation authorization for any future adapter.

## Boundary

Packing owns:

- **Model-facing serialization**: converting an already-selected, already-frozen
  evidence view into the exact packed form a prompt embeds, and converting that
  form back losslessly (`pack`/`unpack`).
- **Envelope versions and their discipline** (below).
- **The adapter contract** every consuming lane must satisfy (below).
- **The frozen form and its verification** — canonical bytes, deterministic
  serialization, rehydration checks over a frozen bundle. Declared here as
  packing-owned per the owner-ratified freezing split; implementation is
  deferred (see the MGT declaration's residuals).

Packing never:

- selects, includes, excludes, labels, scores, or repairs evidence;
- performs the freeze *event* (fixing the working set, bundle id + hash) —
  that belongs to assembly (evidence binding today, the pull loop later);
- stores or retrieves evidence (data lake);
- owns prompt instructions, method decks, or response shapes (judgment lanes);
- condenses or summarizes (condensation is a Judgment act even when its output
  is later packed).

## Invariants (every adapter, every version)

- **PS-I1 Encoding-only.** The packed form carries exactly the input view's
  fields — nothing added, dropped, renamed, or reinterpreted. A packing change
  may never change what the model can learn from the view.
- **PS-I2 Deterministic bytes.** Same input view, same packed bytes.
- **PS-I3 Deep-equal rehydration.** `unpack(pack(view)) == view`, exactly.
- **PS-I4 Citation passthrough.** Aliases and their capability-manifest binding
  survive untouched; durable evidence IDs and audit paths never enter the
  packed surface (they cannot enter it, because the input view never carries
  them — an adapter must not add a path that could).
- **PS-I5 Fail loud on drift.** Unknown envelope version, table, column set,
  row shape, or row key-set is an error at pack or unpack time — never a
  silent coercion, default, or partial result.

## Envelope Versioning

- An envelope version string (e.g. `packing_columnar_view_v0`) is an immutable
  contract. Any change to its tables, columns, envelope keys, or semantics is a
  **new** version string; existing strings are never redefined.
- Consumers pin a (view version, packing version) pair. Rehydration of an
  unpinned or unknown pair fails loud (PS-I5).
- Version bumps are encoding-only by definition (PS-I1); a change that alters
  view content is a *view* change owned by the consuming lane, not a packing
  version bump.

## Adapter Contract

One adapter per **model-facing view schema**, never per platform (TikTok and
Instagram share the creator-audience adapter because they share the view).
A new adapter must:

1. Split the view's rows into homogeneous classes — one dense table per
   distinct row key-set — with column orders declared as constants.
2. Route all table mechanics through the payload-agnostic core
   (`forseti-harness/packing/columnar.py`); adapters stay thin and declare, they
   do not re-implement packing.
3. Ship the standard validation template in the same change:
   deep-equal round-trip on synthetic fixtures (no live capture), packer
   determinism, alias-set preservation against the lane's manifest, absence of
   durable IDs/audit paths in packed and prompt bytes, fail-loud tamper cases
   (version, column, row shape, unknown table, row key drift), and a recorded
   byte measurement.
4. Claim no size savings beyond its recorded measurement. Savings scale with
   rows per table; small fixtures can measure negative (headers dominate), and
   that result is reported, not suppressed.

## Satellites (named, not owned)

- `forseti-harness/packing/` — core + adapters (runtime code home).
- `forseti-harness/tests/unit/test_packing_columnar_v0.py` — the validation
  template's reference instance.
- `docs/decisions/packing_judgment_scaling_owner_agreement_register_v0.md` —
  historical owner-agreement record, including measured byte numbers.
- `docs/research/judgment-spine/evidence_condensation_hierarchy_deferred_direction_v0.md`
  — the deferred future consumer (`judged_claim` tables at every level).
- `docs/research/packing-phase/README.md` — the phase-process research note
  this contract's boundary section supersedes for boundary authority.

## Implemented State (informative, not a claim)

As of 2026-07-21: `packing_columnar_view_v0` core + creator-audience adapter
(PR #1213), serving `creator_audience_compact_judgment_view_v3` for TikTok and
Instagram. Measured on a live-lake 8-video bundle rebuild: flat view 98,805 B
vs packed 49,840 B (-49.6%). Capability tier is owned by the MGT declaration,
not this contract.

## Non-Claims

- Not validation, readiness, proof, or implementation authorization.
- Does not authorize new adapters, the frozen-form implementation, or any
  runtime work; those need their own grants.
- Does not select storage, retrieval, caching, or judgment behavior.
