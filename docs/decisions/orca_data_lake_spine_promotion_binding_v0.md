# Orca Data Lake Spine Promotion Binding v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Binds orca/product/spines/data_lake/ as an accepted shared_foundation spine.
  This is a spine PROMOTION binding, not a move pass: it pins the spine identity,
  the bound subfolder grammar, and the producer/consumer/ownership boundary,
  extending the spine-first target structure. No file moves; the content
  relocation (lake contracts + mechanics map) is a separate later R2 move pass.
use_when:
  - Deciding whether an artifact is data_lake-owned versus capture / ECR / projection / judgment.
  - Planning or gating the R2 Data Lake content move.
  - Authoring the data_lake spine README, future spine.yaml, or move manifest.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/README.md
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - .agents/workflow-overlay/artifact-folders.md
supersedes: []
stale_if:
  - The owner amends the data_lake spine shape or its shared_foundation kind.
  - The R2 move pass executes and relocates the lake content + amends the surfaces.
  - A later accepted Orca decision supersedes the spine identity or ownership boundary bound here.
```

## Status

Owner-accepted **spine-promotion binding**, v0 (2026-06-18). The owner accepted
`orca/product/spines/data_lake/` as a shared-foundation spine in the current turn
and bounded this pass to "accept the binding only." This binds the spine **shape
and identity** as live structure; it does **not** move, rename, or create any
content file, does not re-create `docs/product/`, does not re-organize
capture/projection/engagement, and leaves runtime code and tests in
`orca-harness/`.

Provenance (origin, not authority): at binding time, the data-lake structure
analysis lived in the in-flight `codex/commission-spine-structure` lane at
`docs/migration/data_lake_spine_first_migration_plan_v0.md` (+ its inventory),
and the lake contract files lived in the in-flight `codex/data-lake-core-contract`
lane. Post-R2, the #239 plan/inventory records intentionally stay in
`docs/migration/` as repo-structure migration records, and the lake contracts
live under `orca/product/spines/data_lake/authority/`. These records are
provenance/input, not current binding by themselves.

## Decision

`orca/product/spines/data_lake/` is an accepted **shared-foundation spine** — the
ninth spine under `orca/product/spines/`. It earns its own home (rather than a
folder under `orca/product/shared/`) because it **owns hard, cross-layer storage
contracts** that other spines depend on; folding it into `shared/data_lake_mechanics/`
would hide the actual owner.

### Spine identity (bound)

```yaml
name: data_lake
spine_kind: shared_foundation
root: orca/product/spines/data_lake/
producers:
  - capture
consumers:
  - projection
  - ecr
  - signal_statement
  - cleaning
  - judgment
owns:
  - raw packet preservation contract
  - keyed retrievability contract
  - Attachment Record contract
  - passive Availability Index contract
  - append-only derived-result and acknowledgement attachment contract
does_not_own:
  - physical backend or storage engine
  - source capture execution
  - Mechanical Source Projection semantics
  - ECR derivation semantics
  - Signal Statement interpretation
  - Cleaning transforms
  - Judgment interpretation
  - queue, retry, scheduling, or lane orchestration
```

### Bound subfolder grammar

The accepted shape is the **small** five-folder form (orientation files at the
root, not buried in subfolders). Other folders (`decisions/`, `prompts/`,
`reviews/`, `research/`, `cases/`, `reports/`, `archive/`) are **not** added under
the spine — process history stays in `docs/`; runtime stays in `orca-harness/`.

```
orca/product/spines/data_lake/
  README.md       # spine front-door + this identity
  authority/      # lake contracts / invariants / source-truth rules
  workflows/      # operational / read-flow docs (mechanics maps, route cards)
  migrations/     # lake-specific schema/data migration plans (NOT repo migration logs)
  harness/        # docs / pointers / specs for harness integration (NOT runtime code)
  tests/          # test strategy / fixtures / spec docs (actual test code stays in orca-harness for now)
```

`spine.yaml` is deferred (optional; authored only if a consumer spine needs a
machine-readable contract). Empty subfolders are documented here, not scaffolded
on disk; they materialize when content lands in R2.

## Boundary — what this binds vs what R2 defers

Bound now (this pass):

- the spine path, `spine_kind: shared_foundation`, ownership boundary, and the
  five-folder grammar above, recognized in the live placement authority
  (`.agents/workflow-overlay/artifact-folders.md` spine enumeration) and the repo
  map.

Post-R2 note (2026-06-18): R2 executed — the 3 contracts landed in `authority/`,
the canonical mechanics map in `workflows/`, and
`orca/product/shared/data_lake_mechanics/` is retired. Placement closeout
(2026-06-20): the 2 #239 repo-structure planning docs stay in `docs/migration/`
as repo-structure migration records, not in `data_lake/migrations/`. The
original binding-time deferral text is retained below for the record.

Deferred at binding time to the R2 move pass:

- moving the three lake contracts
  (`core_spine_v0_data_lake_core_contract_v0.md`,
  `…_storage_contract_v0.md`, `…_attachment_record_implementation_contract_v0.md`)
  into `data_lake/authority/`. **These are not on `main`** — they live in the
  `codex/data-lake-core-contract` lane at old `docs/product/core_spine/…` paths;
  that lane must land/re-base **onto the spine tree** first (merging it as-is
  would re-create the retired `docs/product/` wing).
- relocating the mechanics map from its current transitional home
  `orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md`
  into `data_lake/workflows/` (the spine-first migration's move table placed it in
  `shared/` before this promotion; the move set must be re-based onto current
  `main`, i.e. moved **from `shared/`**, not from `docs/product/core_spine/`).
- the `projection_doctrine` re-home (Capture-owned `classify_before_move`, not a
  shared layer) and the `engagement_logic_registry` re-home (judgment/Core
  signal-use rubric, not lake data) — each its own decision, not this binding.

R2 preconditions (load-bearing; do not bury):

1. this binding accepted (done) and the live placement/map surfaces updated (this pass);
2. the `codex/data-lake-core-contract` lane landed or re-based onto `orca/product/spines/data_lake/authority/` (not merged at old `docs/product/` paths);
3. the move set re-based onto current `main` (mechanics map from `shared/`);
4. reuse the forward-only `open_next` repoint convention (move-engine rewrites retrieval metadata across all files via the moved-paths index; historical body prose excepted) so the move does not re-introduce link rot.

## Supersession

This binding supersedes the `shared/data_lake_mechanics/` entry in the **Accepted
target tree** of `docs/decisions/orca_spine_first_target_structure_binding_v0.md`
(now the historical target record): the mechanics map's bound future home is
`data_lake/workflows/`, and the lake's contracts are `data_lake/authority/`-owned,
not `shared/`. `shared/projection_doctrine/` and `shared/engagement_registry/`
are untouched by this binding and remain pending their own R2 decisions.

## Non-claims

- Not validation, readiness, approval, proof, or product proof.
- Not a move pass: no file is moved, renamed, or created except this record, the
  spine README front-door, and the binding/map surface updates; `orca-harness/` is
  untouched.
- Not ratification of the in-flight `commission-spine-structure` or
  `data-lake-core-contract` lanes as merged truth; they are R2 input.
- Not a `spine.yaml`, backend, storage-engine, queue, or runtime authorization.
- A green `check_placement.py` / `check_map_links.py` / `header_index.py` run after
  this pass is placement/link shape, not authority or readiness.

## Direction change propagation

The `direction_change_propagation` receipt for this change set lives inline in
`.agents/workflow-overlay/artifact-folders.md` (a controlling overlay source
updated by this binding — the spine enumeration), per the Doctrine Change
Propagation Contract in `.agents/workflow-overlay/source-of-truth.md`.
