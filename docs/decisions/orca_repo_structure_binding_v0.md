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
  - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
  - orca/product/spines/commission_signal_board/README.md
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

Dated note - Commission Signal Board pilot spine live (2026-06-18): current-turn
owner authorization accepts the spine-first direction in principle and
authorizes a docs-only CSB pilot under
`orca/product/spines/commission_signal_board/`. This makes `orca/` a live
top-level root only for the documented CSB pilot scope. The global `orca/docs/`
move and other product-spine moves remain staged and require their own bounded
migration steps.

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
  `.claude/`, `AGENTS.md`, `CLAUDE.md`), artifacts (`docs/`), pilot product
  workspace (`orca/`, currently only
  `orca/product/spines/commission_signal_board/`), code (`orca-harness/`),
  navigation (`README.md`, `repo-structure.yaml`).
  The exhaustive allowed root set lives in `repo-structure.yaml`
  `known_top_level`.
- `docs/` axis: role grammar exactly as bound in
  `.agents/workflow-overlay/artifact-folders.md` (unchanged by this binding).
- `docs/product/` second-level axis: by lane. Bound lanes: `core_spine/`,
  `data_capture_spine/`, `judgment_spine/`, `signal_content/`, `ecr/`,
  `product_lead/`. Existing bound subfolders (e.g. `source_capture_toolbox/`)
  are unchanged. Files matching no lane may remain at `docs/product/` root
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
  product_lanes, orca_product_spines, scratch_rules, legacy_tolerated, inbox,
  excluded`.
- `orca/product/spines/commission_signal_board/`: live docs-only CSB pilot
  spine. Its spine-local docs are canonical there; old CSB paths under `docs/`
  are resolver stubs backed by
  `orca/product/spines/commission_signal_board/migrations/moved_paths_index.md`.
  Validator code, tests, fixtures, repo-wide decisions, repo maps, and overlay
  files remain in their existing global homes.
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

No historical tree is reorganized by this binding except for explicitly
accepted migration packages or pilots. The bounded exceptions are:

- the prepared Phase-2 consolidation: `docs/product/` flat files into the bound
lanes plus the orca-harness scratch config, packaged (manifest, apply/reverse
script, reference inventory, runbook) under
`docs/migration/repo_structure_phase2_consolidation_v0/`. Applying it is
gated by the runbook's precondition (clean commit checkpoint or explicit
owner waiver) and rewrites live references only; historical records keep
their original path text and are covered by the package's moved-paths index.
- the Commission Signal Board docs-only pilot spine under
  `orca/product/spines/commission_signal_board/`, with old-path stubs and a
  moved-path index. This pilot does not execute the global docs move.

## Direction change propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now accepts `orca/` as a live top-level root only for the docs-only
    Commission Signal Board pilot spine under
    `orca/product/spines/commission_signal_board/`; global `orca/docs/` and all
    other spine moves remain staged.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/orca_repo_structure_binding_v0.md
    - .agents/workflow-overlay/artifact-folders.md
    - repo-structure.yaml
    - docs/STRUCTURE.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
    - docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md
    - orca/product/spines/commission_signal_board/migrations/moved_paths_index.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/hooks/check_placement.py
    - orca/product/spines/commission_signal_board/README.md
    - orca/product/spines/commission_signal_board/spine.yaml
    - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
    - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
    - orca/product/spines/commission_signal_board/harness/validator.md
    - orca/product/spines/commission_signal_board/tests/validator_tests.md
  intentionally_not_updated:
    - path: .agents/hooks/check_commission_signal_board_output.py
      reason: >
        The validator remains a manual/local shared hook substrate; this pass
        does not move executable validator code or change validator behavior.
    - path: orca-harness/tests/unit/test_commission_signal_board_output_validator.py
      reason: >
        Executable tests remain in orca-harness until separate code-root
        migration authority exists; the spine has a pointer doc only.
    - path: orca-harness/tests/fixtures/commission_signal_board_outputs/
      reason: >
        Fixtures remain bound to the executable harness test suite.
    - path: docs/prompts/handoffs/commission_signal_board_spine_pilot_reconciliation_handoff_prompt_v0.md
      reason: >
        Historical handoff prompt remains in the global handoff prompt archive;
        stubs and moved-path index cover current CSB docs.
  stale_language_search: >
    rg -n "docs/workflows/commission_signal_board_playbook_v0|docs/prompts/product-planning/orca_commission_signal_board_prompt_v0|docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0|orca/product/spines/commission_signal_board|orca/docs" docs .agents repo-structure.yaml orca/product/spines/commission_signal_board
  non_claims:
    - not validation
    - not readiness
    - not runtime authorization
    - not global docs migration
    - not movement of validator code, tests, or fixtures
```

Older receipts remain archived or stored in their original controlling surfaces
per `.agents/workflow-overlay/source-of-truth.md`.

## Non-claims

- Not validation, readiness, approval, or proof of navigation improvement.
- Not ratification or import of the jb draft doctrine as Orca authority.
- Not a commit, push, or branch action; nothing is staged by this binding.
- Not the global `orca/docs/` migration or any non-CSB product-spine migration.
- The checker's existence or a passing run is not validation, readiness, or
  authority; placement is not authority.
- Hook wiring is not live until a session restart and is reported as such.
- The Phase-2 move is packaged and dry-run validated only; it is not executed
  by this binding.
