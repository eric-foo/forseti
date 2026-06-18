# Orca Major Move Folder Integrity CA Discussion v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Chief Architect discussion of whether Orca should use major-move folders, broader workstream folders, indexes, or a hybrid folder-integrity pattern.
use_when:
  - Deciding how to route future ICP, commercial-frame, product-proof, review, and prompt artifacts without losing retrieval cohesion.
  - Preparing a later patch to artifact-folder or structure guidance.
  - Checking why Orca should not immediately create dedicated major-move folders.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/retrieval-metadata.md
  - docs/STRUCTURE.md
input_hashes:
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: A6510BFF8951C7A2A01087133076C7933D1EF922735A6790237B05BBED503E74
  - path: .agents/workflow-overlay/artifact-folders.md
    sha256: 53CD58EEE4F22A778A7235F969CE73334EBAAB7D0DC9BF9408B0F7D4FEFB3589
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 9E159E3A7CC933083F56C95EBDDED4E19B2F51D55EE8EF774F3BEC62D566834F
  - path: .agents/workflow-overlay/retrieval-metadata.md
    sha256: ECE14148E415EF5C9E3E89FD5ACC47DEADDC84B9A4F653FBF1F455AD3C0B90DE
stale_if:
  - Accepted artifact folders change.
  - Prompt path-assignment behavior changes.
  - Owner accepts a dedicated major-move folder class.
  - Docs structure guidance changes how workstream indexes or typed child folders are treated.
```

## Status And Recommendation

Status: `INDEX_MANIFEST_HYBRID_RECOMMENDED`.

Recommendation: keep artifact-type folders as canonical destinations, but add lightweight per-major-move manifest or index artifacts under an accepted folder, starting with `docs/workflows/<major_move_slug>_artifact_manifest_vN.md`, rather than creating dedicated ICP or major-move folders now.

Source basis: `AGENTS.md`; `.agents/workflow-overlay/README.md`; `.agents/workflow-overlay/source-of-truth.md`; `.agents/workflow-overlay/artifact-folders.md`; `.agents/workflow-overlay/artifact-roles.md`; `.agents/workflow-overlay/prompt-orchestration.md`; `.agents/workflow-overlay/retrieval-metadata.md`; `docs/STRUCTURE.md`; `docs/README.md`; `orca/product/README.md`; `docs/prompts/README.md`; `docs/review-outputs/README.md`; `docs/hygiene/queue.md`; `docs/decisions/turn_08_product_thesis_v0.md`; `docs/product/orca_offer_hypothesis_v0.md`; `docs/product/orca_buyer_proof_packet_v0.md`; `docs/product/orca_product_proof_lead_charter_v0.md`; `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`; targeted `rg` searches over `docs/` and `.agents/workflow-overlay/` for ICP, first wedge, commercial frame, proof, major move, folder, artifact, workflow, decision, review, prompt, workstream, manifest, index, and router language.

## Problem Frame

Trigger:

The owner asked whether every major Orca move should get its own folder, for example an `ICP` folder, or whether the folder should be broader.

Observed risk:

Orca now has clusters of related artifacts that cross artifact roles: ICP / first-wedge decisions, product proof, commercial-frame preparation, prompts, reviews, patch routes, workflow records, and future proof or customer-discovery materials. The current folder model can make one workstream hard to see end to end because relevant artifacts are spread across `docs/product/`, `docs/prompts/`, `docs/review-outputs/`, `docs/workflows/`, `docs/research/`, and possibly `docs/decisions/`.

Why it matters:

Folder topology is not just navigation. In Orca, folders bind artifact role, write permission, output mode, review routing, retrieval metadata expectations, and source-of-truth boundaries. A folder pattern that makes one move easier to browse can still damage prompt determinism or duplicate authority if artifacts are moved away from their role-owned destinations.

Desired folder-integrity outcome:

Future agents should be able to load all artifacts for one major move quickly while preserving canonical artifact roles, avoiding duplicated source-of-truth paths, and keeping prompt and review output routing deterministic.

## Current Folder Model

Current accepted folders:

- `.agents/workflow-overlay/`: overlay authority for Orca-specific project facts, artifact folders, artifact roles, prompt rules, validation gates, review lanes, safety rules, and source hierarchy.
- `docs/decisions/`: decision records.
- `docs/product/`: product contracts, proof plans, core-spine notes, satellite notes, evidence standards, source maps, decision artifacts, memo substrates, evidence appendices, and executive-deck shape drafts.
- `docs/research/`: source-backed research artifacts and evidence lane outputs that do not become product authority by default.
- `docs/prompts/` plus typed prompt-family children: product planning, feature planning, deep-thinking, handoffs, reviews, reruns, patches, wrappers, and templates.
- `docs/review-inputs/`: prepared review inputs.
- `docs/review-outputs/` and `docs/review-outputs/adversarial-artifact-reviews/`: reviewer reports and verdicts.
- `docs/workflows/`: workflow records, validation notes, and operational records.
- `docs/migration/`: migration and import records.
- `docs/hygiene/`: triage queues and cleanup notes.
- `docs/_inbox/`: non-authoritative scratch.

What works:

- Artifact role remains legible from the path. A product artifact goes under `docs/product/`; a review report goes under `docs/review-outputs/`; a prompt goes under `docs/prompts/`.
- Prompt and review path assignment stays deterministic because prompt orchestration can choose the narrowest accepted role folder.
- Write permissions remain bounded. A reviewer writes reports; a Product Lead writes product artifacts; a workflow pass writes workflow records.
- Retrieval headers can carry `open_next`, `input_hashes`, `downstream_consumers`, and `stale_if` without requiring folder moves.
- The model resists implementation drift because docs-first locations are explicit and implementation folders remain forbidden until later authorization.

What is starting to strain:

- A major move can now span several role folders. The ICP / first-wedge move already touches a product prompt, product decision artifact, offer hypothesis, buyer-proof packet, proof lead charter, adversarial reviews, and future patch implications.
- Existing product and method-validation work uses naming prefixes to create cohesion inside flat folders. That works for source-aware agents, but it forces future agents to search and reconstruct the cluster manually.
- `docs/STRUCTURE.md` and `docs/review-outputs/README.md` already describe typed child folders as navigation aids for durable workstreams, while the overlay has only accepted some child folders explicitly. This is a sign that navigation pressure exists and should be resolved deliberately.
- `docs/hygiene/queue.md` already records one folder-drift item: `docs/prompts/hygiene-queue/` exists but is not accepted by the overlay. That is a warning against ad hoc folder creation.

## Options Compared

| Option | Retrieval clarity | Artifact-role integrity | Prompt/review determinism | Sprawl and migration risk | Assessment |
| --- | --- | --- | --- | --- | --- |
| Keep current artifact-type model unchanged | Medium. Agents can search by slug, but must reconstruct cross-folder workstreams. | Strong. Role and write permission stay path-obvious. | Strong. Existing prompt orchestration remains clean. | Low near-term, but search cost rises with each major move. | Too conservative. It preserves integrity but does not address the observed cross-folder retrieval strain. |
| Create dedicated major-move folders such as `docs/moves/icp/` or `docs/product/icp/` | High for browsing one move. | Weak-to-medium. A move folder can contain prompts, reviews, product docs, and workflows, blurring role-owned destinations unless it only stores duplicates or links. | Weak. Prompt and review outputs would either break current path rules or need exception logic for each move. | High. Creates migration pressure and encourages every attractive initiative to request a folder. | Not recommended now. It solves browsing by making source-of-truth and write-boundary questions worse. |
| Create broader workstream folders such as `docs/product/first-proof/`, `docs/product/market-selection/`, or `docs/workflows/major-moves/` | Medium-to-high if scoped well. | Medium. Broader folders are less brittle than `ICP`, but still risk mixing roles if used as canonical destinations. | Medium. Safe only if each workstream folder is clearly limited to one artifact role or to index records. | Medium-to-high. Better than one folder per move, but still needs acceptance criteria, migration rules, and overlay ownership. | Potential later pattern, not first move. Use only after manifests prove repeated retrieval burden and the folder's artifact role is narrow. |
| Use lightweight index/router artifacts instead of new folders | High enough for source-aware agents if each index lists canonical artifacts, statuses, hashes when useful, owners, stale conditions, and next steps. | Strong. Canonical artifacts stay in role-owned folders. | Strong. Prompt and review destinations remain unchanged. | Low. No migration is required, and index files can be retired or superseded. | Strong baseline. It directly addresses retrieval without moving authority. |
| Hybrid: keep artifact-type folders canonical, add per-major-move indexes or manifests | High. Browsing starts at a manifest, then follows canonical links. | Strong, if the manifest is retrieval-only and does not duplicate product truth or review verdicts. | Strong. Existing path assignment still works. | Low-to-medium. Needs a small overlay/structure rule to avoid inconsistent manifest formats. | Recommended. It gives major moves a durable retrieval surface without creating premature folder classes. |

Other observed pattern:

Typed child folders already exist or are described for some review and research workstreams. They can be legitimate when the folder still belongs to one artifact role, such as a review-output child folder or research corpus subtree. That precedent does not justify a cross-role `ICP` folder. It supports the narrower rule: child folders are safe when they refine an artifact role, not when they replace role ownership with initiative ownership.

## Recommended Pattern

Naming pattern:

Use `docs/workflows/<major_move_slug>_artifact_manifest_vN.md` for cross-role major-move manifests. Examples:

- `docs/workflows/orca_first_icp_wedge_artifact_manifest_v0.md`
- `docs/workflows/orca_commercial_frame_artifact_manifest_v0.md`
- `docs/workflows/orca_product_proof_artifact_manifest_v0.md`

Each manifest should be a workflow record with retrieval metadata. It should include:

- move scope and status;
- controlling sources;
- canonical artifact map grouped by role, not by file convenience;
- current accepted, proposed, blocked, and deferred items;
- prompts and wrappers;
- review reports and unresolved findings;
- patch implications;
- stale conditions;
- exact next authorized step.

Which artifacts remain in artifact-type folders:

- Product truth, proof packets, ICP decisions, offer hypotheses, commercial-frame product artifacts, source maps, memo substrates, and executive-deck shape drafts remain in `docs/product/` unless a later accepted decision creates a narrower product-only child folder.
- Prompt artifacts remain in `docs/prompts/` and its accepted typed children.
- Review reports remain in `docs/review-outputs/` or a typed review-output child folder.
- Workflow records and cross-role manifests remain in `docs/workflows/`.
- Accepted decision records remain in `docs/decisions/`.
- Research evidence remains in `docs/research/` and does not become product authority by manifest inclusion.
- Scratch remains in `docs/_inbox/` and cannot be cited as authority unless promoted through accepted folders or hygiene routing.

Whether indexes/manifests are needed:

Yes. Major moves now need a retrieval object, but not a canonical destination folder. The manifest is the right first object because it can point across roles, carry stale conditions, and preserve the distinction between source loading and authority.

Whether any new folder class is justified:

No new cross-role folder class is justified now. A future folder class could be justified only if repeated manifests show that a role-specific subtree is needed, such as a product-only proof workstream folder or a review-output workstream folder, and only after the overlay binds the folder's artifact role, permissions, freshness markers, and migration rule.

What should happen for the ICP / first-wedge work specifically:

Do not create `docs/moves/icp/`, `docs/product/icp/`, or an `ICP` folder. Create or queue a manifest such as `docs/workflows/orca_first_icp_wedge_artifact_manifest_v0.md` only after the owner accepts this pattern or authorizes the next docs-write step. That manifest should point to the existing canonical artifacts, especially `docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md`, `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`, `docs/product/orca_offer_hypothesis_v0.md`, `docs/product/orca_buyer_proof_packet_v0.md`, `docs/product/orca_product_proof_lead_charter_v0.md`, and the relevant adversarial review reports.

## Patch Implications

`.agents/workflow-overlay/artifact-folders.md`:

A later patch should add a rule that cross-role major-move cohesion is handled by workflow manifests under `docs/workflows/` unless a later accepted decision creates a narrower role-specific child folder. It should also say that major-move folders are not canonical destinations by default.

`.agents/workflow-overlay/artifact-roles.md`:

A later patch may clarify that `Workflow record` includes cross-role artifact manifests or indexes when they are retrieval-only and do not promote the artifacts they list.

`.agents/workflow-overlay/retrieval-metadata.md`:

No mandatory patch is required. The existing `open_next`, `downstream_consumers`, and `stale_if` fields already support the manifest pattern. A later patch could add a short example only if future agents misapply the header.

`.agents/workflow-overlay/prompt-orchestration.md`:

A later patch may mention that prompt artifacts should point to downstream manifests when a major-move manifest exists, but canonical prompt destinations remain unchanged.

`docs/STRUCTURE.md`:

A later patch should explain the distinction between role-specific typed child folders and cross-role major-move manifests. It should also warn that `docs/moves/` and ad hoc initiative folders are not accepted destinations unless the overlay is patched first.

Workflow index:

If accepted, create the first manifest for the ICP / first-wedge move as a separate docs-write step. Do not combine that with folder creation, overlay patching, or migration.

Conceptual patch units:

- `STEP-01`: Patch artifact-folder rules to prefer workflow manifests over cross-role major-move folders.
- `STEP-02`: Patch artifact-role language for workflow manifests if needed.
- `STEP-03`: Patch `docs/STRUCTURE.md` with a short navigation rule.
- `STEP-04`: Create the first ICP / first-wedge manifest under `docs/workflows/`.
- `STEP-05`: Review unresolved drift such as `docs/prompts/hygiene-queue/` through the hygiene queue, not as part of major-move folder adoption.

## Risks And Non-Claims

Folder sprawl risk:

Dedicated major-move folders invite one folder per initiative and force the project to decide whether every workstream is a folder-worthy workstream. The manifest pattern reduces that risk because a new manifest is cheaper to create, easier to supersede, and does not alter accepted destinations.

Duplicate authority risk:

A manifest must not restate product truth, review verdicts, proof claims, or patch acceptance as independent authority. It should link canonical artifacts and record routing state. If the manifest conflicts with a product artifact, review report, decision record, overlay file, or current user instruction, the controlling source wins.

Migration risk:

Moving existing artifacts into initiative folders would create stale hashes, stale prompts, broken downstream paths, and possible review-output confusion. The recommended pattern requires no migration now.

Over-generic bucket risk:

A broad folder like `docs/workflows/major-moves/` could become a dumping ground if it stores full artifacts instead of indexes. If a child folder is ever created, it must be narrowly defined and subordinate to a bound artifact role.

No folder acceptance claim:

This artifact recommends a pattern. It does not accept a new folder class, create one, or update the overlay.

No migration completion claim:

No artifacts were moved, renamed, or migrated.

No validation/readiness claim:

This discussion does not validate Orca product proof, ICP correctness, commercial readiness, folder readiness, prompt readiness, or implementation readiness.

## Exact Next Authorized Step

Owner or Chief Architect should accept, reject, or modify the `INDEX_MANIFEST_HYBRID_RECOMMENDED` pattern. If accepted, the next docs-write step is a narrow patch route for `.agents/workflow-overlay/artifact-folders.md` and `docs/STRUCTURE.md` that binds cross-role major-move manifests under `docs/workflows/` before any ICP manifest is created.
