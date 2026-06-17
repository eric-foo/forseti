# Orca Spine-First Workspace Structure Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record (proposed repo-structure target)
scope: >
  Proposed mini-god-tier repo structure target for moving Orca from
  artifact-role-first product docs into spine-first product workspaces, with
  separate Orca docs, and Commission Signal Board as the lowest-risk pilot.
use_when:
  - Deciding whether spine work should remain split across docs/product, docs/prompts, docs/workflows, docs/research, and orca-harness.
  - Planning a Commission Signal Board pilot migration into a whole-spine workspace.
  - Allocating subsidiary documents inside a spine-first workspace without losing artifact-role clarity.
  - Separating Orca product workspace material from global Orca docs.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_repo_structure_binding_v0.md
  - .agents/workflow-overlay/artifact-folders.md
  - repo-structure.yaml
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
stale_if:
  - A later accepted repo-structure decision supersedes or amends the CSB pilot scope.
  - repo-structure.yaml adds or removes a top-level product workspace root.
  - Another product spine moves before its lane migration inventory and binding update are accepted.
```

- Status: PARTIALLY_ACCEPTED_FOR_CSB_PILOT.
- Current binding: `docs/` plus `orca-harness/` remain current for non-migrated
  work; `orca/product/spines/commission_signal_board/` is now the live
  docs-only Commission Signal Board pilot spine per
  `docs/decisions/orca_repo_structure_binding_v0.md`.
- This proposal plus current-turn owner authorization authorizes only the CSB
  docs-only pilot spine. It does not authorize a bulk migration,
  implementation work, validation claim, readiness claim, global `orca/docs/`
  move, or automatic supersession of the current placement checker.

## Decision Question

Should Orca move from an artifact-role-first layout to an `orca/product` plus
`orca/docs` layout, so each spine has one physical product home that contains
its authority, prompts, workflows, research, cases, reviews, reports, and
harness-facing pointers?

## Recommendation

Adopt a spine-first target layout, but only through a staged migration.

Use Commission Signal Board as the pilot because it is nascent and already has a
small bounded file set:

- one product/adjudication packet;
- one prompt artifact;
- one workflow playbook;
- one manual validator;
- one unit test and fixture set;
- one repo-map registration.

Do not begin with Judgment, Capture, ECR, or Source Capture. Those lanes already
have larger histories, cross-references, review bundles, and runtime surfaces.

## Target Shape

The mini-god-tier target is a whole-spine workspace under `orca/product`, with
global, non-spine documents under `orca/docs`.

```text
orca/
  product/
    README.md
    spines/
      commission_signal_board/
        README.md
        spine.yaml
        authority/
        decisions/
        prompts/
        workflows/
        research/
        cases/
        reviews/
        reports/
        harness/
        tests/
        migrations/
        archive/

      judgment/
      capture/
      ecr/
      signal_content/
      forecasting/
      weighting/
      decision/

    shared/
      product_lead/
      buyer_proof/
      claim_defense/
      repo_structure/

  docs/
    README.md
    decisions/
    workflows/
    prompts/
      templates/
      shared/
    review-inputs/
    review-outputs/
    migration/
    hygiene/
    guides/
```

`orca/product/spines/<spine>/` is the spine's physical home. The spine is not a
folder under `docs/product/`; it is the product workspace.

`orca/docs/` is the future home for global documents that are not owned by one
spine: repo-wide decisions, global workflow maps, prompt templates, review-lane
archives, hygiene, migration records, and human repo guides.

The current root `docs/` tree remains the transition/current binding until a
later accepted migration moves or aliases it. After a spine is migrated, new
spine-owned subsidiary documents should be created inside that spine unless a
global artifact role is more correct.

## Spine Internal Grammar

| Folder | Use | Not for |
| --- | --- | --- |
| `authority/` | Product doctrine, operating contracts, architecture, invariants, ownership maps. | Generated outputs, tests, scratch notes. |
| `decisions/` | Spine-local decisions and accepted/adjudicated direction records. | Repo-wide structure decisions or overlay authority. |
| `prompts/` | Spine-local full prompts, wrappers, reruns, review prompts, and handoff prompts. | Cross-spine prompt templates. |
| `workflows/` | Playbooks, route cards, submaps, runbooks, operator sequences. | Product doctrine that belongs in `authority/`. |
| `research/` | Evidence discovery, source screens, synthesis, rejected-source maps, feasibility probes. | Accepted product doctrine. |
| `cases/` | Case manifests, case packets, case-specific notes, captured case artifacts when human-readable. | Shared harness fixtures or generated run cache. |
| `reviews/` | Review inputs, reviewer outputs, adjudications, patch-review packets scoped to the spine. | Repo-wide review-lane doctrine. |
| `reports/` | Human-readable run summaries, dry-run receipts, closeouts, and result ledgers. | Machine-only generated scratch. |
| `harness/` | Spine-local harness design notes, schemas, validators, runners, and code pointers. | Shared executable packages that remain in `orca-harness/` until a separate code-root migration. |
| `tests/` | Spine-local fixture descriptions, expected-output docs, test plans, test pointers. | The canonical executable tests if they still live under `orca-harness/tests/`. |
| `migrations/` | Per-spine move plans, moved-path indexes, reverse plans, and stale-reference audits. | Global repo-structure migrations. |
| `archive/` | Superseded spine-local artifacts after a migration decision adopts archive mechanics. | Current artifacts. |

The grammar is role-typed, but the first axis is the spine. That is the point:
humans and agents enter by product subsystem first, then choose the artifact
role.

## Shared And Global Artifacts

Not every file should move into a spine.

Keep these global or shared:

- `AGENTS.md`, `.agents/workflow-overlay/`, and `.agents/hooks/` as agent
  governance and hook substrates.
- `repo-structure.yaml` as the machine structure map.
- repo-wide decisions in `docs/decisions/` until a later decision creates
  `orca/docs/decisions/`.
- repo-wide maps in `docs/workflows/` until their replacement exists under
  `orca/docs/workflows/`.
- reusable prompt templates in the global prompt-template home.
- shared executable packages in `orca-harness/` until a separate code-root
  migration is accepted.
- historical migration packages and moved-path indexes in `docs/migration/`
  until `orca/docs/migration/` is accepted.

Spine-local review reports can move into the spine. Cross-spine review doctrine
and reusable review conventions stay global.

## Commission Signal Board Pilot

Proposed pilot home:

```text
orca/product/spines/commission_signal_board/
  README.md
  spine.yaml
  authority/
    orca_commission_signal_board_prompt_adjudication_packet_v0.md
  prompts/
    orca_commission_signal_board_prompt_v0.md
  workflows/
    commission_signal_board_playbook_v0.md
  harness/
    validator.md
  tests/
    fixtures/
      commission_signal_board_outputs/
    unit/
      test_commission_signal_board_output_validator.md
  migrations/
    moved_paths_index.md
```

The executable validator may stay at
`.agents/hooks/check_commission_signal_board_output.py` during the pilot if it is
still a manual/local hook substrate. If it becomes product runtime, move or wrap
it under `orca-harness/commission_signal_board/` through a separate
implementation authorization.

The pilot should use stubs or moved-path indexes for old locations rather than
silently breaking references.

## Options Considered

| Option | Judgment |
| --- | --- |
| Keep current artifact-role-first layout | Lowest churn, but poor spine onboarding and too much cross-folder hunting. |
| Add only `docs/product/spines/` | Smallest structural move, but fails the product-workspace goal because the spine still lives under docs. |
| Add top-level `product/spines/` | Cleaner than `docs/product`, but lacks the Orca namespace and creates a second root-level product concept beside `orca-harness`. |
| Add `orca/product/spines/` plus future `orca/docs/` | Preferred target. It gives the product system a real workspace while keeping global documents separate; harness/code absorption remains separately decided. |
| Move all spines now | Rejected. Too much reference churn and too much risk while Judgment/Capture are active. |

## Required Binding Changes Before Additional Moves

For the Commission Signal Board pilot, these surfaces were updated in the
binding patch that created the live spine. Before creating any additional
product spine or global `orca/docs/` home, update:

- `docs/decisions/orca_repo_structure_binding_v0.md`;
- `.agents/workflow-overlay/artifact-folders.md`;
- `repo-structure.yaml`;
- `docs/STRUCTURE.md`;
- `docs/workflows/orca_repo_map_v0.md`;
- placement-checker tests or expectations if they assert the closed root set or
  deeper path grammar.

The accepted decision should say whether `docs/product/<lane>/` becomes
legacy-current, migration-source, or still allowed for non-migrated spines.

## Phased Migration

1. Accept or amend this target decision. **CSB pilot: done. Broader direction:
   accepted in principle, staged.**
2. Add the root binding for `orca/product/spines/`. **Done only for
   `orca/product/spines/commission_signal_board/`.**
3. Pilot Commission Signal Board only. **Current live pilot.**
4. Run stale-reference searches and record a moved-path index.
5. Update the Commission Signal Board playbook and repo map to point at the new
   spine home.
6. Leave Judgment, Capture, ECR, Signal Content, and Source Capture untouched
   until the pilot proves the pattern.
7. Decide the next spine by current churn and reference surface, not by desire
   for tidiness.

## Visible Limitations

This is the mini-god-tier version, not the maximal one.

- It does not create a full monorepo package architecture.
- It does not move implementation code out of `orca-harness/`.
- It does not migrate all existing spines.
- It does not rewrite historical references by default.
- It does not prove the new layout improves outcome quality.
- It does not authorize runtime work, CI changes, or hook wiring.
- It preserves global governance and shared maps instead of forcing everything
  into one spine folder.

## Non-Claims

This proposal is not validation, readiness, approval, implementation
authorization, migration completion, hook deployment, CI enforcement, or proof
that any spine is complete. It is a target architecture proposal for owner
decision and staged migration planning.
