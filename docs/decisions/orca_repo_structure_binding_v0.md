# Orca Repo Structure Binding v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Orca-owned binding of the agent-first repo-structure invariant core
  (restated, not referenced) plus the Orca parameter layer: per-subtree axes,
  role grammar, scratch rule, machine map, surface tiering, and the EP-04
  placement-enforcement substrate authorization.
use_when:
  - Deciding where a new Orca artifact or folder belongs, beyond the
    folder-level bindings in .agents/workflow-overlay/artifact-folders.md.
  - Authoring or revising repo-structure.yaml or check_placement.py.
  - Planning or executing the Phase-2 docs/product consolidation.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - repo-structure.yaml
  - docs/decisions/orca_spine_first_blocker_authorization_v0.md
  - docs/migration/repo_structure_phase2_consolidation_v0/runbook.md
stale_if:
  - repo-structure.yaml and this binding disagree on a home or parameter.
  - A later accepted Orca decision supersedes a parameter bound here.
  # (retired 2026-06-11: "The Phase-2 consolidation applies" fired - see the
  # dated note in Status)
```

## Status

Owner-authorized adoption, v0. Authorized by explicit current-turn owner
instruction ("do all phases", 2026-06-11) through the fused implementation
pipeline. This binds the structure discipline below as Orca project doctrine
and authorizes the EP-04 placement substrate build recorded here. It is not
validation, not readiness, not ratification of any external doctrine, and not
acceptance of the jb draft doctrine as Orca authority.

Dated note — Phase-2 applied (2026-06-11): the prepared consolidation ran
(commit `1b0f3fc`, 99-file by-lane move); the harness pytest/uv scratch config
followed (`8516cdc`); EP-04 hook wiring landed in `.claude/settings.json`
(`27bade9`) and the hooks have been observed firing in-session. The `stale_if`
trigger "Phase-2 consolidation applies" fired and is retired; lane statuses in
`repo-structure.yaml` read `current` and match the migration state.

Dated note — spine-first target authorized, not executed (2026-06-18):
`docs/decisions/orca_spine_first_target_structure_binding_v0.md` binds the
target `orca/product/` spine-first tree, and
`docs/decisions/orca_spine_first_blocker_authorization_v0.md` authorizes the
execution tranche to add the `orca/` root and supersede this binding's
`docs/product/` by-lane axis. Until that execution updates `repo-structure.yaml`
and `.agents/workflow-overlay/artifact-folders.md`, the current placement rule
below remains true for the live tree.

## Provenance (origin, not authority)

The invariant core below is restated from an assessment of a cross-repo draft
structure doctrine (resident in the jb workspace, DRAFT/candidate status) plus
this repo's own observed evidence. Per `AGENTS.md` and the overlay binding
rule, jb-resident sources are not Orca authority: this binding restates the
content as Orca-owned doctrine rather than referencing the jb path as a rule
source. If the jb draft later changes, nothing in Orca changes unless a later
accepted Orca decision adopts the change.

Orca-local evidence motivating adoption: subtrees with a bound grammar stayed
clean (docs/ top level, docs/prompts/, docs/review-outputs/, docs/research/);
subtrees without one sprawled (docs/product/ reached ~100 flat files with the
axis carried by filename prefixes; docs/decisions/ ~50 flat); boundaries with
no write enforcement leaked (3 stray files at repo root, ~20 generated scratch
dirs interleaved at orca-harness/ top level, months-old material in
docs/_inbox/).

## Invariant core (restated as Orca doctrine)

1. One legible primary axis per subtree; demote other axes to nested or
   tagged secondary structure and indexes.
2. A small closed role grammar applied consistently within a subtree, so
   paths are synthesizable. The role set is a parameter; having a small closed
   set, extended only by recorded decision, is the invariant.
3. Structure-as-index: put the navigation signal in the paths and names an
   agent traverses anyway, not only in a separate index it must choose to read.
4. Current/archive separation, elevated because an agent reads and acts on a
   stale file a human would skip.
5. Discriminable, grep-able names; co-changing artifacts live near each other.
6. Single physical home per artifact; alternate routes via one terse
   machine-readable structure map that enforcement and agents both consume.
   Human narrative maps are additive (altitude-split), never copies.
7. `_inbox/` quarantine for unplaced artifacts with a promotion rule;
   structural changes are recorded as tiered decisions (new lane, role-grammar,
   or root-layout changes - not routine file placement).
8. Enforce placement at the write, not index-reading: an advisory write-time
   warning for salient placement plus a strict commit/CI-mode check as the
   backstop for incidental placement.

## Orca parameter layer (bound)

- Top-level axis (repo root): function class - governance (`.agents/`,
  `.claude/`, `AGENTS.md`, `CLAUDE.md`), artifacts (`docs/`), code
  (`orca-harness/`), navigation (`README.md`, `repo-structure.yaml`).
  The exhaustive allowed root set lives in `repo-structure.yaml`
  `known_top_level`.
- `docs/` axis: role grammar exactly as bound in
  `.agents/workflow-overlay/artifact-folders.md` (unchanged by this binding).
- `docs/product/` second-level axis: by lane. Bound lanes: `core_spine/`,
  `data_capture_spine/`, `judgment_spine/`, `signal_content/`, `ecr/`,
  `product_lead/`, plus the `search/` topic lane added by
  `docs/decisions/orca_search_product_lane_binding_v0.md` (a deliberate topic
  vertical beside the function lanes; see that record for the inclusion test and
  the invariant-#1 note). Existing bound subfolders (e.g.
  `source_capture_toolbox/`) are unchanged. Files matching no lane may remain at `docs/product/` root
  (bounded residual). Product lanes are bound here. Their `repo-structure.yaml`
  status must match the actual migration state: `planned` before the Phase-2
  apply, `current` only after the apply has run (the apply ran 2026-06-11).
  New product artifacts should use the lane folders immediately (forward-only).
- `docs/decisions/`: stays flat in v0; its naming grammar plus this binding's
  map entry are the navigation aid. Revisit only by a later decision.
- Archive mechanism: supersede banners and `superseded_by` header fields
  (current practice) remain the v0 mechanism; `_archive/` folders are
  explicitly deferred, not adopted.
- Scratch rule: `_`-prefixed directories are runtime/scratch and are excluded
  from placement evaluation; named generated patterns (pycache, pytest caches,
  egg-info) are likewise excluded. Bound in `repo-structure.yaml`
  `scratch_rules`. The orca-harness scratch *consolidation* (pytest/uv config)
  ships in the Phase-2 package because `orca-harness/pyproject.toml` carries
  another lane's uncommitted work tonight.
- Machine map: `repo-structure.yaml` at repo root, schema frozen to the keys
  `version, status, authority, entry_points, known_top_level, docs_roles,
  product_lanes, scratch_rules, legacy_tolerated, inbox, excluded`.
- `_inbox` hygiene: `inbox.max_age_days` in the map (advisory signal only,
  never a hard failure).

## Surface tiering (reconciliation of existing structure surfaces)

- `.agents/workflow-overlay/artifact-folders.md` - the placement *authority*
  (rules, accepted folders). Unchanged role.
- `repo-structure.yaml` - the machine *router*: the single machine-readable
  source that `check_placement.py` and agents consume. It must not state
  rules; it declares homes. On conflict, artifact-folders.md wins and the map
  is the stale party.
- `docs/STRUCTURE.md` and `docs/workflows/orca_repo_map_v0.md` - human
  narrative at different altitudes (docs usage guide; repo route card).
  Additive only; neither is placement authority.

## EP-04 substrate authorization (recorded)

Under the owner authorization above, the EP-04 placement substrate
(classified PARTIAL in
`docs/decisions/overlay_enforcement_placement_classification_v0.md`) is built
this turn following the EP-32 house pattern: checker
`.agents/hooks/check_placement.py` (advisory `--hook`, `--strict` commit/CI
mode, `--check`, `--selftest`, fail-open on internal error, references
authority, reads `repo-structure.yaml` as its only rule source) plus a third
`PostToolUse` entry in `.claude/settings.json`. The judgment edge stays
resident: new folders may be allowed by a later decision, and the checker
enforces placement shape, never the truth, value, or authority of any
artifact (placement is not authority). Hooks load at session start, so the
hook wiring goes live only after a Claude Code restart. The `--strict` mode
exists as a gate-on-demand commit/CI check and is intentionally not installed
as a blocking gate by this binding.

## Forward-only adoption and Phase 2

No historical tree is reorganized by this binding. The bounded exception is
the prepared Phase-2 consolidation: `docs/product/` flat files into the bound
lanes plus the orca-harness scratch config, packaged (manifest, apply/reverse
script, reference inventory, runbook) under
`docs/migration/repo_structure_phase2_consolidation_v0/`. Applying it is
gated by the runbook's precondition (clean commit checkpoint or explicit
owner waiver) and rewrites live references only; historical records keep
their original path text and are covered by the package's moved-paths index.

## Direction change propagation

The `direction_change_propagation` receipt for this change set lives inline in
`.agents/workflow-overlay/artifact-folders.md` (the controlling overlay source
updated), per the Doctrine Change Propagation Contract in
`.agents/workflow-overlay/source-of-truth.md`.

## Non-claims

- Not validation, readiness, approval, or proof of navigation improvement.
- Not ratification or import of the jb draft doctrine as Orca authority.
- Not a commit, push, or branch action; nothing is staged by this binding.
- The checker's existence or a passing run is not validation, readiness, or
  authority; placement is not authority.
- Hook wiring is not live until a session restart and is reported as such.
- The Phase-2 move is packaged and dry-run validated only; it is not executed
  by this binding.
