# Artifact Folders

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Accepted Orca artifact folders and folder rules.
use_when:
  - Deciding where Orca artifacts belong.
  - Checking whether a folder is authoritative, scratch, or forbidden.
authority_boundary: retrieval_only
```

## Accepted Folders

- `docs/decisions/`: Orca decision records.
- `docs/prompts/`: Orca prompt artifacts.
- `docs/prompts/product-planning/`: product planning prompt drafts.
- `docs/prompts/feature-planning/`: feature planning prompt drafts.
- `docs/prompts/deep-thinking/`: deep reasoning prompt drafts.
- `docs/prompts/handoffs/`: implementation handoff prompt drafts.
- `docs/prompts/reviews/`: review prompt drafts.
- `docs/prompts/reruns/`: rerun prompt drafts.
- `docs/prompts/patches/`: patch prompt drafts.
- `docs/prompts/wrappers/`: thin wrapper prompts that reference full prompt artifacts.
- `docs/prompts/templates/`: Orca-local prompt templates and template README files, subordinate to `.agents/workflow-overlay/template-registry.md`.
- `docs/review-inputs/`: artifacts prepared for review.
- `docs/review-outputs/`: reviewer findings reports and overlay-bound verdicts.
- `docs/review-outputs/adversarial-artifact-reviews/`: adversarial artifact review reports.
- `docs/workflows/`: workflow records, repo maps, validation notes, and operational records owned by Orca.
- `docs/migration/`: migration and import queue records.
- `docs/product/`: product contracts, product proof plans, core-spine notes, satellite notes, evidence standards, source maps, decision artifacts, memo substrates, evidence appendices, and executive-deck shape drafts.
- `docs/product/source_capture_toolbox/`: product-facing Source Capture Armory design notes, scoped specs, and gap notes. Existing controlling Data Capture source-access decisions, method plans, and obligation contracts remain at their historical paths unless a later migration decision moves them.
- `docs/product/search/`: Orca's demand-signal intelligence (search-led) lane - search / answer-engine surfaces (web search / SERP, AI Overviews and other answer engines, zero-click, AEO/GEO, search-interest) PLUS the demand-signal discovery method (scan core, read taxonomy, demand gates) they feed, bound by `docs/decisions/orca_search_product_lane_binding_v0.md`. Membership is set by that record's inclusion test; topic-primacy wins over spine placement for those docs. The method docs are search-led but venue-spanning (consumed across judgment/capture/core spines).
- `docs/product/` lane subfolders (`core_spine/`, `data_capture_spine/`, `judgment_spine/`, `signal_content/`, `ecr/`, `product_lead/`, `search/`): the bound second-level axis for product artifacts per `docs/decisions/orca_repo_structure_binding_v0.md` (and, for the `search/` topic lane, `docs/decisions/orca_search_product_lane_binding_v0.md`). New product artifacts use the matching lane; files matching no lane may stay at `docs/product/` root. Existing flat files move only via a migration package, not ad hoc. **Being superseded by `orca/product/` (spine-first migration, executing — see below); both coexist until Wave E drops `docs/product/`.**
- `orca/product/` (repo root): the **spine-first product tree** — target of the in-progress migration bound by `docs/decisions/orca_spine_first_target_structure_binding_v0.md` and authorized by `docs/decisions/orca_spine_first_blocker_authorization_v0.md` (#254). Second-level axis: `spines/` (`foundation/`, `commission_signal_board/`, `scanning/`, `capture/`, `ecr/`, `cleaning/`, `judgment/`, `product_lead/`), `satellites/`, `case_families/`, `shared/`. Per-spine structure is owned by the spine-first binding, not the machine map; `check_placement.py` treats `orca/` as a declared top-level area. Wave B created the root + this authority; Wave C moves the `docs/product/` files in (manifest + apply engine under `docs/migration/repo_structure_spine_first_v0/`); Wave E drops `docs/product/`. `docs/doctrine/` is intentionally NOT created by this migration (owner B3: index/router-only, seeded later).
- `repo-structure.yaml` (repo root): the machine structure map - router only, consumed by `.agents/hooks/check_placement.py` and agents for navigation. It declares homes and never states rules; this overlay file remains the placement authority and wins on conflict.
- `docs/research/`: public/source research artifacts, evidence-only lane outputs, synthesis reports, candidate screens, and reject-pattern maps that support Orca product or proof work without becoming product authority by default.
- `docs/research/judgment-spine/harness/v0_14/smoke_tests/`: Judgment Harness v0.14 no-case smoke-test receipts and operator provenance records. Artifacts in this folder are plumbing evidence only and do not become real-case probe, validation, fixture-admission, product-proof, or judgment-quality evidence by location.
- `docs/hygiene/`: triage queues and cleanup notes for Orca artifacts.
- `docs/_inbox/`: non-authoritative temporary holding area for scratch prompts, notes, imports, and untriaged material.
- `.agents/skills/`: Orca-local accepted/candidate workflow skill source (for example, `orca-product-lead`), governed by `.agents/workflow-overlay/skill-adoption.md`. Orca-local only; this is NOT plugin, user-level, installed, or external skill source, and living here does not deploy, activate, or make a skill resolver-visible.

## Rules

- Keep durable Orca artifacts under `docs/` unless a later Orca decision creates a narrower folder.
- Full prompt artifacts and thin wrappers must follow `.agents/workflow-overlay/prompt-orchestration.md`.
- New or materially touched durable human-authored workflow artifacts must
  follow `.agents/workflow-overlay/retrieval-metadata.md` unless that contract
  excludes the artifact class.
- Treat `docs/_inbox/` as scratch only. Nothing in `_inbox` is Orca authority until promoted into an accepted docs folder or overlay file.
- Track parked or temporary material through `docs/hygiene/queue.md` when it may need promotion, review, archiving, or deletion.
- Keep product artifacts in `docs/product/` unless they are accepted decision records, prompt artifacts, workflow records, review artifacts, or migration records.
- Keep research artifacts in `docs/research/` when the primary purpose is source discovery, corpus qualification, evidence gathering, candidate screening, or rejected-source mapping. Promote research conclusions into `docs/product/` or `docs/decisions/` only through a later accepted product or decision artifact.
- Do not create implementation folders such as `src`, `app`, `packages`, `tests`, or automation runtimes until explicitly authorized.
- Orca-local workflow skills live only under `.agents/skills/` and are governed by `.agents/workflow-overlay/skill-adoption.md`; acceptance there is a local freeze, not deployment, and must not edit plugin, user-level, installed, or external skill source.
- Do not copy or move material from external reference folders unless a later turn explicitly authorizes the import.
- Placement is checked at the write boundary by `.agents/hooks/check_placement.py` (EP-04, advisory; `--strict` commit/CI mode available), which reads `repo-structure.yaml` as its only rule source. A passing check is placement shape only - never validation, readiness, or authority. Parameters and invariants: `docs/decisions/orca_repo_structure_binding_v0.md`.

## Direction Change Propagation - Orca-Local Skill Folder

```yaml
direction_change_propagation:
  doctrine_changed: >
    `.agents/skills/` is now a bound Orca-local accepted/candidate workflow-skill
    source folder, and the first Orca-local skill (`orca-product-lead`) is
    accepted/frozen. Acceptance is a local freeze only — not deployment,
    activation, or resolver-visibility.
  trigger: output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/skills/orca-product-lead/SKILL.md
  downstream_surfaces_checked:
    - AGENTS.md                                      # grep: no skill/folder reference; skill rules already defer to overlay; no change
    - .agents/workflow-overlay/README.md             # grep: no reference; no change
    - .agents/workflow-overlay/source-of-truth.md    # grep: no reference; skill is not an authority source (it defers)
    - .agents/workflow-overlay/project-authority.md  # grep: no reference; skill is explicitly non-authority
  stale_language_search: 'rg -n "orca-product-lead|\.agents/skills|no accepted Orca-local" . (run 2026-06-08; only skill-adoption.md carried the stale "no accepted" status, now fixed)'
  intentionally_not_updated:
    - path: .agents/workflow-overlay/skill-adoption.md (Known Snapshots, 2026-05-24 line)
      reason: dated historical observation, true as of its date.
    - path: docs/workflows/orca_pricing_first_doc_cascade_proposal_v0.md
      reason: historical proposal record (row 7 deferral); current acceptance state now lives in skill-adoption.md; the proposal is not retro-edited.
    - path: orca/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md
      reason: already-superseded historical record; its supersede banner governs.
    - path: docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md
      reason: already-superseded historical record; its supersede banner governs.
    - path: docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md
      reason: historical generator prompt; records a then-open question, not current state.
    - path: docs/prompts/handoffs/jb_prompt_path_assignment_ca_settlement_prompt_v0.md
      reason: jb-scoped non-Orca lane; its "do not edit .agents/skills" guardrail is not stale.
  non_claims:
    - not deployment
    - not activation
    - not resolver-visibility
    - not validation
    - not readiness
```

## Direction Change Propagation - Repo Structure Binding v0

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca adopts the agent-first repo-structure invariant core as Orca-owned
    doctrine via docs/decisions/orca_repo_structure_binding_v0.md, binds the
    docs/product/ by-lane second axis and root machine map repo-structure.yaml
    (router-only), and authorizes the EP-04 placement substrate
    (.agents/hooks/check_placement.py, advisory write-boundary + --strict
    commit/CI mode). Forward-only; the docs/product flat-file consolidation is
    packaged under docs/migration/repo_structure_phase2_consolidation_v0/ and
    is not executed by this change.
  trigger: output_authority
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/artifact-folders.md
    - docs/decisions/orca_repo_structure_binding_v0.md
    - repo-structure.yaml
  downstream_surfaces_checked:
    - AGENTS.md                                      # no structure facts; defers to overlay; no change
    - .agents/workflow-overlay/README.md             # section ownership unchanged; no change
    - .agents/workflow-overlay/source-of-truth.md    # hierarchy/propagation mechanics unchanged; receipt inline here per contract
    - .agents/workflow-overlay/source-loading.md     # read packs reference unchanged paths until Phase-2 apply
    - .agents/workflow-overlay/validation-gates.md   # Enforcement Placement principle already present and generic
    - docs/workflows/orca_repo_map_v0.md             # updated in this change set (Active Hooks + root map entry)
    - docs/STRUCTURE.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: shared commit-once-whole file; hierarchy unchanged; DCP contract stores receipts inline in the changed artifact.
    - path: docs/STRUCTURE.md
      reason: narrative tier per the binding's surface tiering; gains lane detail when the Phase-2 move applies, not before.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: the principle is already bound there; the EP-04 instance is recorded in the EP classification decision update and the repo map Active Hooks note.
  stale_language_search: 'rg -n "repo-structure.yaml|check_placement|orca_repo_structure_binding" .agents/workflow-overlay docs/STRUCTURE.md docs/workflows/orca_repo_map_v0.md AGENTS.md (run at closeout; expected hits only in this change set)'
  non_claims:
    - not validation
    - not readiness
    - not a commit, push, or branch action
    - not execution of the Phase-2 move
    - hook wiring not live until session restart
```

## Direction Change Propagation - Search Product Lane v0

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca adds docs/product/search/ as a bound topic lane - the demand-signal
    intelligence (search-led) vertical: search / answer-engine surfaces PLUS the
    demand-signal discovery method (scan core, read taxonomy, demand gates) they
    feed - bound by docs/decisions/orca_search_product_lane_binding_v0.md
    (inclusion test + precedence rule). 10 member docs are physically co-located
    via the migration package, applied on the lane branch. The demand-signal
    method docs are search-led but venue-spanning (consumed across
    judgment/capture/core spines); placing them in search/ does not narrow their
    authority.
  trigger: output_authority
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/decisions/orca_search_product_lane_binding_v0.md   # lane binding + inclusion test + precedence rule (expanded to demand-signal method)
    - docs/decisions/orca_repo_structure_binding_v0.md        # bound-lanes bullet notes search/
    - repo-structure.yaml                                     # product_lanes += { search } (current once applied)
    - .agents/workflow-overlay/artifact-folders.md            # search accepted-folder entry + lane-subfolder list + this receipt
    - orca/product/README.md                                  # lane list includes search/
    - docs/product/search/README.md                          # lane front-door index (restructured for the expanded lane)
    - docs/workflows/orca_repo_map_v0.md                      # Workstream Status Pointers: search lane row
    - docs/migration/repo_structure_search_lane_v0/           # package: 10-row manifest + idempotent apply/reverse + runbook + reference inventory + moved-paths index
    - the 10 moved docs + ~19 live referencing files          # apply rewrites their full-path references into search/
  downstream_surfaces_checked:
    - path: docs/STRUCTURE.md
      result: no product-lane enumeration (lists only top-level docs/ roles); no change needed (narrative tier).
    - path: .agents/workflow-overlay/source-loading.md
      result: not a full-path referrer of the moved docs (worker sweep); no search read-pack yet; unchanged.
    - path: .agents/hooks/check_placement.py
      result: reads repo-structure.yaml as its only rule source; recognizes the lane via product_lanes; no code change.
    - path: AGENTS.md
      result: defers structure facts to the overlay; no change.
    - path: historical referencing records (decisions/reviews/prompts/research/hygiene)
      result: keep old paths by design (worker sweep); resolve via the package moved_paths_index.
  intentionally_not_updated:
    - path: docs/STRUCTURE.md
      reason: narrative tier per the binding's surface tiering; no product-lane list to amend (same treatment as the Phase-2 move).
    - path: the moved docs' content
      reason: not edited except intra-set full-path references (hash-safe; no inbound hash pins); search/README.md was hand-restructured separately.
    - path: orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md (bare-name "in-flight/not on main" prose)
      reason: pre-existing stale status independent of this move (the scan-core spec is already on main); out of scope for this migration.
  stale_language_search: >
    The runbook's apply sequence includes a git-grep reference-resolution check
    that must return no stale old-path hits in LIVE docs after --apply; verified
    post-apply.
  non_claims:
    - not validation
    - not readiness
    - not product proof
    - placement of the demand-signal method docs in search/ does not narrow their venue-spanning authority
    - a green check_placement run is placement shape, not authority
```

## Direction Change Propagation - Spine-First Migration Wave B (orca/ root + authority)

```yaml
direction_change_propagation:
  doctrine_changed: >
    Spine-first migration Wave B (structural commit): the `orca/` top-level root
    is created and declared in repo-structure.yaml known_top_level, and
    artifact-folders.md now declares `orca/product/` as the spine-first product
    tree (target bound by orca_spine_first_target_structure_binding_v0,
    authorized by orca_spine_first_blocker_authorization_v0 / #254). The
    `docs/product/` by-lane axis is being superseded by the `orca/product/` spine
    axis; both coexist during execution. No files are moved by Wave B (that is
    Wave C); `docs/product/` remains valid until Wave E drops it. `docs/doctrine/`
    is intentionally NOT added (owner B3: index/router-only, seeded later, not
    part of the product-tree move).
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
    - workflow_authority
  controlling_sources_updated:
    - repo-structure.yaml
    - .agents/workflow-overlay/artifact-folders.md
    - docs/decisions/orca_repo_structure_binding_v0.md
    - docs/decisions/orca_search_product_lane_binding_v0.md
  downstream_surfaces_checked:
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/check_placement.py
    - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        docs/product -> orca/product reference rewrites + the orca/ nav section are
        Wave C (apply engine, live nav) and Wave E (status pointers); Wave B does
        not touch the map. The repo-map-freshness advisory on the new orca/
        top-level is acknowledged and deferred to Wave E.
    - path: .agents/hooks/check_placement.py
      reason: >
        No code change needed: classify() treats any non-docs known_top_level dir
        as a declared area, so adding `orca` to known_top_level.dirs suffices for
        orca/product/ to be placed.
    - path: repo-structure.yaml docs_roles + product_lanes (docs/product)
      reason: >
        Left intact: docs/product/ is still populated until Wave C moves the files
        and Wave E drops the role; removing it now would flag the live files.
  stale_language_search: >
    rg -n "known_top_level|orca/product" repo-structure.yaml
    .agents/workflow-overlay/artifact-folders.md (run 2026-06-18, worktree
    orca-spine-first-execution)
  stale_language_search_result: >
    docs/product by-lane bullet + repo-structure.yaml docs_roles/product_lanes
    remain (intentional, live until Wave C/E); the new orca/product bullet +
    known_top_level orca entry are the Wave B additions; no surface claims the
    migration is complete or that files have moved.
  non_claims:
    - not validation, readiness, or proof
    - not file movement (Wave C) or docs/product removal (Wave E)
    - not creation of docs/doctrine (owner-deferred)
    - a green check_placement run is placement shape, not authority
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
