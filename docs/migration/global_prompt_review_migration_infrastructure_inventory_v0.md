# Global Prompt, Review, And Migration Infrastructure Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration record
scope: Inventory-only marker for global prompt, review, workflow, validation, and migration infrastructure that should remain outside product spines during spine-first repo migration.
use_when:
  - Distinguishing product-spine content from global workflow/documentation infrastructure during repo migration.
  - Checking whether a prompt, review, migration, overlay, workflow-map, template, or validation surface should stay global even when it references a spine.
  - Planning later spine-local pointers or wrappers without moving global workflow authority into a product lane.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/artifact-roles.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - .agents/workflow-overlay/artifact-folders.md changes accepted Orca artifact folders.
  - .agents/workflow-overlay/artifact-roles.md changes prompt, review, workflow, migration, or validation role bindings.
  - docs/decisions/orca_repo_structure_binding_v0.md changes the product-lane axis or surface tiering.
  - docs/workflows/orca_repo_map_v0.md or repo-structure.yaml changes the global routing shape for prompts, reviews, migration, workflow maps, or validation hooks.
```

## Purpose

This is an inventory-only migration marking artifact. It identifies global workflow and documentation infrastructure that should remain outside `docs/product/` product spines while product content continues to organize by lane.

The classification question is not "which spine owns this?" The question is: what must stay global so spines do not absorb workflow authority, review authority, prompt mechanics, validation gates, migration history, or retrieval routing.

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 + infrastructure target reads
  edit_permission: docs-write
  target_scope: inventory-only migration marker for global prompt/review/migration infrastructure
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-loading, prompt-orchestration, artifact-folders, artifact-roles, repo map
```

Isolation decision: the original root worktree was dirty with untracked `.codex/hooks/run_orca_guard.py`, `_scratch/`, and `orca-worktrees/`, plus a permission warning under `orca-harness/.pytest_tmp/`. This artifact was written in a clean docs-write worktree on branch `codex/global-prompt-review-infra-inventory`.

Source context used:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/template-registry.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/decision-routing.md`
- `docs/workflows/orca_repo_map_v0.md` as retrieval map only
- `docs/workflows/artifact_retrievability_guide.md`
- `docs/decisions/orca_repo_structure_binding_v0.md`
- `repo-structure.yaml`
- `docs/STRUCTURE.md`
- `docs/product/README.md`
- existing migration records under `docs/migration/repo_structure_phase2_consolidation_v0/` and `docs/migration/repo_structure_search_lane_v0/`
- review/prompt folder READMEs and targeted hook documentation under `.agents/hooks/`

`workflow-deep-thinking` was applied only after that source context was ready. Its applied criterion: keep a surface global when its primary role is to route, authorize, review, validate, template, migrate, or retrieve work across lanes; spine locality applies to product content, not to the control plane.

## Classification Rule

Product-spine content belongs under the product lane axis when its primary role is product doctrine, product architecture, evidence mechanics, buyer-proof content, source/capture/Judgment/ECR product contracts, or product-lane state.

Global infrastructure remains outside product spines when its primary role is one of these:

- agent/project authority;
- source hierarchy, source-loading, prompt orchestration, review-lane, artifact-role, validation, safety, or lifecycle rules;
- prompt artifact, prompt template, wrapper, rerun, review prompt, or handoff mechanics;
- review input packaging or review output reporting;
- migration runbook, move manifest, moved-path index, import queue, or reference inventory;
- repo map, workflow record, retrieval guide, source-loading submap, or operational route card;
- decision record under the accepted `docs/decisions/` role;
- deterministic governance substrate, hook, CI workflow, or validation checker.

A filename that contains `data_capture_spine`, `judgment_spine`, `core_spine`, `ecr`, `signal_content`, `source_capture`, `search`, or another spine marker is not enough to make the artifact product-spine content. Role beats topic.

## 1. Current Global Infrastructure Surfaces

| Surface | Current location | Global role | Migration treatment |
| --- | --- | --- | --- |
| Root agent instructions | `AGENTS.md`, `CLAUDE.md` | Agent behavior kernel and Claude shim | Stay global. They route to overlay authority and must not be absorbed by a spine. |
| Overlay authority | `.agents/workflow-overlay/` | Source hierarchy, loading, prompts, artifact folders/roles, review lanes, safety, validation, templates, communication, skill adoption | Stay global. Overlay files are cross-spine project authority. |
| Machine/router map | `repo-structure.yaml` | Router-only structure map consumed by placement checking and agents | Stay global. It declares homes and product lanes; it is not product content. |
| Governance hooks | `.agents/hooks/` | Tool-boundary checks, retrieval/link checks, placement checks, guard scripts, session capsule | Stay global. Some read product files, but their role is governance/tooling. |
| Codex hook adapter | `.codex/hooks.json`, `.codex/hooks/` when present | Harness wiring for shared guard logic | Stay global project config, not product-spine content. |
| GitHub/local workflow tooling | `.github/workflows/`, `.github/scripts/`, `.githooks/` when referenced by docs | CI, auto-merge, risk routing, local hook install, branch/protection checks | Stay global. Product spines may be consumers, not owners. |
| Prompt artifacts | `docs/prompts/` and typed children | Full prompts, wrappers, handoffs, reviews, reruns, patches, advisory and architecture prompts | Stay global by role. Spine-named prompts commission or review spine work; they are not product artifacts. |
| Prompt templates | `docs/prompts/templates/` | Orca-local template registry material | Stay global and subordinate to `.agents/workflow-overlay/template-registry.md`. |
| Review inputs | `docs/review-inputs/` | Review bundles, copied source packets, manifests, hash files, review briefs | Stay global. Review-input copies are not canonical product authority unless a prompt explicitly binds that. |
| Review outputs | `docs/review-outputs/` and typed child folders | Reviewer findings reports and overlay-bound verdicts when bound | Stay global. Review findings are decision input, not product-spine source authority by location. |
| Migration records | `docs/migration/` | Runbooks, manifests, moved-path indexes, reference inventories, import queue | Stay global. They describe placement/reference changes; they are not product lane content. |
| Workflow maps and records | `docs/workflows/` | Repo map, submaps, retrievability guide, bootstrap record, operational notes | Stay global unless a later decision creates a spine-local mirror/pointer. |
| Decision records | `docs/decisions/` | Accepted/proposed Orca decisions, doctrine, authorizations, adjudications | Stay global and flat under current structure binding. Product/spine decisions may reference a spine without moving into it. |

Observed current prompt/review/migration shape, for orientation only:

- `docs/prompts/`: 174 markdown prompt/template files across `advisory`, `architecture`, `deep-thinking`, `feature-planning`, `handoffs`, `patches`, `product-planning`, `reruns`, `reviews`, `templates`, and `wrappers`, plus a few root prompt files.
- `docs/review-inputs/`: review bundles and copied source sets, including markdown, Python, YAML, text manifests, and zip bundles.
- `docs/review-outputs/`: 168 markdown review reports and 18 zip review bundles under root and typed folders.
- `docs/migration/`: existing product/search migration packages plus `import_queue.md`.

These counts are inventory signals from the current worktree, not authority or a freshness guarantee. Re-run the folder counts before using them as migration inputs.

## 2. Surfaces That Must Remain Outside Product Spines

These surfaces should not be moved into `docs/product/<lane>/` during spine-first migration:

| Must stay global | Why |
| --- | --- |
| `.agents/workflow-overlay/` | Owns Orca project authority, not a product lane. Moving it would make a spine appear to own source hierarchy, prompt rules, review rules, validation gates, or safety boundaries. |
| `.agents/hooks/`, `.codex/hooks/`, `.github/workflows/`, `.github/scripts/`, `.githooks/` | Deterministic governance/CI substrates enforce or report global rules. A product spine may be checked by them, but it must not own them by placement. |
| `repo-structure.yaml` | Router-only structure map for the whole repo. Its product-lane section points to spines but does not become one. |
| `docs/prompts/` | Prompt artifacts are orchestration records. A `data_capture_spine_*_prompt_v0.md` path still means "prompt artifact about Data Capture Spine," not "Data Capture Spine source." |
| `docs/prompts/templates/` | Template registry material has cross-lane prompt-shaping authority. Spine-local copies would fork prompt mechanics. |
| `docs/review-inputs/` | Review packages may contain copied product sources or code excerpts, but they are review inputs. Moving them into product spines would invite treating copies as canonical. |
| `docs/review-outputs/` | Review reports are findings and decision input. They must not become product-spine acceptance or validation records by placement. |
| `docs/migration/` | Migration runbooks, manifests, reference inventories, moved-path indexes, and import queues are cross-repo placement/history records. |
| `docs/workflows/orca_repo_map_v0.md` and workflow submaps | Retrieval maps route agents across spines and global folders. They are navigation/control-plane surfaces. |
| `docs/workflows/artifact_retrievability_guide.md` | Operational retrieval guide for all durable artifacts. Not a product-lane guide. |
| `docs/decisions/` | Decision records remain in the accepted global decision role. Product-lane decisions can bind product facts while still living in the decision-record surface. |

Hard rule: do not move a global infrastructure artifact just because its title, slug, or body references a product spine.

## 3. Surfaces That Merely Reference A Spine And Can Stay Global

These classes can mention a spine while remaining global:

- Spine-specific prompt artifacts, such as Data Capture, Judgment, ECR, Source Capture, or Core Spine handoffs and review prompts under `docs/prompts/`.
- Review outputs whose reviewed target is a spine artifact, code path, fixture, or migration package under `docs/review-outputs/`.
- Review-input bundles that include copied spine artifacts, harness files, or overlay excerpts under `docs/review-inputs/`.
- Migration package inventories and moved-path indexes that mention old and new product-spine paths under `docs/migration/`.
- Workflow submaps that route to a spine, such as Data Capture or ECR navigation records under `docs/workflows/`.
- Decision records with spine prefixes under `docs/decisions/`.
- Overlay source-loading packs that mention spines while owning source-loading mechanics globally.
- Validation or hook scripts that read a product-spine backlog, product-lane map, or harness path to emit a global nudge or gate.

For these surfaces, the spine reference is an object reference, not a placement claim.

## 4. Surfaces That May Need Spine-Local Copies Or Wrappers Later

No spine-local copy or wrapper is authorized by this inventory. These are future candidates only if retrieval friction appears:

| Candidate | Possible later shape | Guardrail |
| --- | --- | --- |
| Product-lane README pointers | A short pointer from `docs/product/<lane>/README.md` to relevant global prompt/review/migration trails | Pointer only. Do not duplicate prompt, review, or validation rules. |
| Spine-local "review trail" index | A lane README section listing global review prompts/outputs for that lane | Index only. Review reports stay in `docs/review-outputs/`. |
| Spine-local "prompt trail" index | A lane README section or workflow submap pointing to global prompt artifacts | Index only. Prompt artifacts stay in `docs/prompts/`. |
| Spine-specific execution runbooks currently under `docs/workflows/` | A product-facing wrapper or pointer if the runbook becomes a routine lane entrypoint | Wrapper only unless a later decision changes the artifact role. |
| Product examples embedded in global prompt templates | A spine-local example appendix if template examples become too product-specific | Do not fork the template mechanics or registry. |
| Review-input bundles containing canonical source copies | A spine-local source pointer back to canonical product docs, not the bundle | Bundles remain review packages; copied sources remain non-canonical unless explicitly bound. |
| Migration moved-path indexes | A product-lane README pointer to `docs/migration/.../moved_paths_index.md` for old-path resolution | Moved-path indexes remain global migration records. |
| Product-specific governance nudges | A product README pointer to the global hook/check that emits the nudge | Hook/check remains in `.agents/hooks/` unless a later implementation decision creates a product runtime component. |

Use these only when a fresh agent repeatedly fails to find the global trail from normal entrypoints. Do not preemptively copy global infrastructure into spines for symmetry.

## 5. Artifact-Role Risks

Key risks during spine-first migration:

1. Filename-over-role drift: moving `*_spine_*_prompt_v0.md`, `*_review_v0.md`, or `*_migration_*` because the slug names a spine would erase the prompt/review/migration role boundary.
2. Review-input copy promotion: copied source files inside `docs/review-inputs/**/sources/` can look canonical. They are review-package inputs unless the prompt explicitly says otherwise.
3. Review-output overclaim: review reports can be mistaken for approval, validation, mandatory remediation, or product readiness if placed near product sources.
4. Template fork risk: spine-local template copies would fork prompt mechanics and can silently drift from `.agents/workflow-overlay/template-registry.md`.
5. Overlay authority leakage: a spine-local copy of overlay policy would look easier to read but weaker as a source of truth. Point to the overlay instead.
6. Migration-history loss: moving runbooks or moved-path indexes into spines would hide cross-lane reference history and make old-path resolution harder.
7. Decision-record fragmentation: moving spine-specific decisions into product folders would conflict with the current global `docs/decisions/` role and make DCP/archive checks harder.
8. Validation-shape confusion: hooks and checks enforce or nudge shape only. Their existence, placement, or green output is not validation, readiness, approval, or authority.
9. Root prompt drift: root-level `docs/prompts/*.md` files are prompt-family drift, not product-spine candidates. Triage them as prompt organization, not product migration.

## 6. Retrieval/Repo-Map Risks

- The repo map is retrieval-only. It helps choose source packs but does not make a listed artifact authoritative or fresh.
- Folder-level reachability can be enough for retrieval-header CI. A new `docs/migration/*.md` artifact may be map-covered by the `docs/migration/` folder route even when its exact file path is not named.
- Existing migration packages intentionally leave historical prompt, review, research, and decision references unchanged and resolve old paths through moved-path indexes. Do not rewrite historical prompts/reviews just to make paths look current.
- A workflow submap that routes to a spine does not become product content. Its role is still retrieval/navigation unless a later accepted source changes it.
- The current repo map notes some prompt-family drift and review-output root retention. Treat those as hygiene/navigation facts, not migration orders.
- If a later migration creates new global folders, new prompt child folders, new review-output typed folders, or new workflow submaps, check repo-map freshness and retrieval-index coverage at the same time.
- If a later migration moves product files but leaves historical references, it should preserve or create a moved-path index rather than retro-editing point-in-time records.
- If a later lane needs strict claims about acceptance, validation, source-of-truth promotion, or readiness, load the controlling source. This inventory is not that source.

## 7. Open Owner Questions

1. Should `docs/prompts/` root prompt drift be cleaned into typed prompt-family folders before or after the next product-spine migration window?
2. Should each product spine README eventually include a compact "global prompt/review trail" pointer section, or should the repo map remain the only cross-lane index?
3. Should `docs/review-outputs/` gain additional typed child folders such as `prompts/`, `workflow/`, or `misc/` for new work, while retaining existing root reports in place?
4. Should `docs/review-inputs/` review bundles get explicit expiry/hygiene handling after their review is closed, or remain as durable provenance packages by default?
5. Should `docs/workflows/data_capture_spine_consolidation_map_v0.md` and similar submaps remain global workflow maps permanently, or should product spines get read-only pointer mirrors?
6. Should product-specific governance nudges, such as ontology expansion checks, be documented from the product spine README while the script remains in `.agents/hooks/`?
7. Should `docs/decisions/` stay flat indefinitely, or is a later decision-record substructure needed once decision count creates real retrieval friction?
8. Should new migration inventories like this one receive explicit repo-map rows, or is folder-level `docs/migration/` coverage sufficient until recurring use proves a route gap?

## 8. Suggested Migration Order

1. Keep the control plane fixed first: `AGENTS.md`, `.agents/workflow-overlay/`, `repo-structure.yaml`, `.agents/hooks/`, prompt templates, review lanes, and validation gates do not move as part of product-spine migration.
2. Move only product artifacts whose primary role is product content and whose destination is already bound by `docs/decisions/orca_repo_structure_binding_v0.md`, `repo-structure.yaml`, or a later accepted lane decision.
3. For each product move package, prepare or reuse a migration package with manifest, dry-run/apply mechanics if applicable, reference inventory, moved-path index, and runbook under `docs/migration/`.
4. Rewrite live navigation/authority references only when the migration package says they are live references. Leave historical prompts, review reports, decisions, and research records alone unless a later task explicitly authorizes a provenance-preserving update.
5. After product moves land, add spine-local pointers only where a fresh-agent retrieval test shows a recurring gap. Prefer README pointers or submap entries over copying prompt/review/migration content.
6. Run the relevant shape checks: retrieval header, map/link checks, placement check when product paths move, and any package-specific dry-run or strict command. Treat green checks as shape/placement evidence only.
7. Review artifact-role boundaries before closeout: copied review inputs are not canonical, review outputs are not approval, migration runbooks are not product truth, and prompt templates are not spine-owned.

## 9. Explicit Non-Claims

- This artifact moves no files.
- This artifact edits no templates.
- This artifact edits no overlay files.
- This artifact changes no validation doctrine.
- This artifact does not authorize implementation, runtime work, capture work, model execution, CI changes, hook wiring, branch protection, commit, push, PR, or merge.
- This artifact does not prove that any prompt, review, migration package, workflow map, decision, hook, or product artifact is fresh, accepted, validated, complete, or ready.
- This artifact does not supersede `.agents/workflow-overlay/artifact-folders.md`, `.agents/workflow-overlay/artifact-roles.md`, `repo-structure.yaml`, `docs/decisions/orca_repo_structure_binding_v0.md`, or `docs/workflows/orca_repo_map_v0.md`.
- This artifact does not decide future spine-local wrappers or indexes; it names candidates and owner questions only.
- This artifact does not claim every existing historical reference is current. Historical records may intentionally preserve old paths and resolve through moved-path indexes.
- This artifact does not make review outputs mandatory remediation or product authority. Reviews remain decision input until separately accepted or authorized.
- This artifact does not make a global hook or checker a product-spine artifact merely because it reads a product-spine file.
