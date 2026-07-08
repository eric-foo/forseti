# Creator Ledger Cross-Platform Identity Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Prompt for a fresh architecture-planning lane to decide the v0 creator-ledger
  account-linking architecture across Instagram, TikTok, and YouTube: table
  shape, evidence levels, confidence gates, LLM-assist boundary, and storage
  posture before any runtime or capture implementation.
use_when:
  - Commissioning a planning-only architecture pass for creator-ledger cross-platform account linking.
  - Deciding how Orca may associate public creator accounts without claiming real-world identity.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md
stale_if:
  - The creator roster/frontier ledger spec is superseded or moved.
  - Orca adopts a runtime schema or storage design for the creator ledger.
  - Wind-caller, public-name, passive-monitoring, ontology, or cross-platform identity boundaries change.
```

Paste the body below into a fresh architecture-planning lane in this workspace.

---

You are the Chief Architect for Orca.

## Objective and intended decision

Decide the smallest complete v0 architecture for Orca's creator ledger to
associate Instagram, TikTok, and YouTube public creator accounts while
preserving the current ledger privacy and ontology boundaries.

The intended output is an architecture recommendation for the owner. It is not
an implementation prompt, not a database migration, not capture authorization,
and not permission to create or populate the ledger.

The concrete decision to answer:

- Should the first creator ledger stay as a static table-shaped fixture rather
  than SQLite?
- What row types are needed for cross-platform accounts?
- What evidence is strong enough to link accounts to one ledger-local creator
  record?
- Can bundled weak evidence produce a confident account-link state, and if yes,
  what must the ledger call that state so it does not claim real-world identity?
- What should LLMs be allowed to do in the link decision?

## Plain-language frame

Cross-platform identity stitching means taking accounts from different platforms
and treating them as the same real-world person or entity. That can be risky
because it can silently create a person dossier, false identity match, outreach
surface, or privacy-sensitive profile.

For this pass, do not ask whether Orca can prove "same legal person." The safer
question is whether public accounts can be linked as the same **public creator
surface** under a ledger-local creator record, with source pointers, evidence
type, confidence, review state, and explicit non-claims.

## Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- Prompt artifact input:
  `docs/prompts/deep-thinking/creator_ledger_cross_platform_identity_architecture_prompt_v0.md`.
- Authorization basis: current owner request for a couriered architecture-planning prompt after creator-ledger placement discussion.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`.
- Branch at authoring: `codex/ig-reels-capture-spine`.
- Head at authoring: `20e0f42855579ab499c8793e49dfadb61e363eea`.
- Dirty-state allowance: untracked scratch, hygiene handoffs, and unrelated worktree artifacts may exist in the parent checkout. Treat them as out of scope unless they are named below.
- Isolation decision: existing lane branch, docs-only prompt artifact, no runtime or ledger edits.
- Source pack: custom S3 target deepening, bounded to required reads below.
- Edit permission for the receiving lane: read-only by default. Docs-write is allowed only for one architecture recommendation artifact if the owner explicitly asks for it in that lane.
- Target files or dirs: the existing creator-ledger spec and adjacent source-family product folder only. Do not create, move, rename, or populate the actual ledger.
- Output mode for the receiving lane: chat-only architecture recommendation unless the owner explicitly upgrades to a file-written recommendation.
- Doctrine change decision: this prompt itself changes no doctrine. A recommendation that changes ledger contract, ontology boundary, source-family placement, or storage/runtime posture would require a later owner-accepted artifact and direction-change propagation.
- Validation gates: source-read completeness, Cynefin routing, architecture-planning output contract, and explicit non-claims. Do not claim validation, readiness, proof, or implementation authorization.

## Required reads

Authority and routing:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`

Task sources:

- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/README.md`
- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md`

Optional, only if route context could change the recommendation:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md`

## Method sequencing

1. Run Orca Cynefin routing from `.agents/workflow-overlay/decision-routing.md`
   before planning.
2. REFERENCE-LOAD `workflow-architecture-planning` if available. Do not APPLY it yet.
3. SOURCE-LOAD the required reads above.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, with missing sources and source gaps.
5. Only after source readiness, APPLY architecture planning to the loaded source context.
6. Use the standard profile unless source gaps force a lean, advisory-only result.

## User-stated working hypothesis to test

The owner accepts the distinction between best and weaker evidence:

- Best evidence: explicit cross-links from platform bios or About pages, the
  same official site or link hub, or a public self-declared statement such as
  "my TikTok is X" or "subscribe to my YouTube Y."
- Weaker evidence: same handle, same display name, same profile photo, similar
  content style, same niche, similar voice, or posting-pattern similarities.

The owner also believes that bundled weaker evidence can probably support a
confident conclusion that the accounts are the same creator.

Test that hypothesis without turning it into a real-world identity claim.
Consider whether the correct architecture is:

- `confirmed_public_account_link` only for direct self-declared or cross-linked evidence.
- `probable_public_account_link` for bundled weak evidence that passes explicit thresholds.
- `candidate_public_account_link` for weak or partial evidence that needs review.
- Never `same_person`, `real_identity`, `legal_identity`, or equivalent.

## Architecture options to compare

Compare at least these options:

1. Keep the current Instagram-only ledger spec and defer cross-platform account linking.
2. Add table-shaped static fixture rows now:
   `creator_roster_entries`, `platform_accounts`, `account_link_evidence`,
   `creator_name_observations`, and `roster_lifecycle_events`.
3. Add the same table-shaped fixture plus a small future validator contract for
   required fields, forbidden fields, source pointers, confidence labels, and
   append-only behavior. Do not build the validator in this pass.
4. Adopt SQLite immediately.
5. Adopt an identity graph or person-profile model. This option should be
   seriously tested and likely rejected or deferred if it violates the current
   privacy and ontology boundaries.

## Required design questions

Answer these directly:

- What is the stable core object: `creator_record_id`, `platform_account_id`, or another ID?
- What does a ledger-local creator record mean if it is not a real-world identity?
- What is the exact relationship between `creator_record_id` and platform accounts?
- What evidence rows are append-only?
- What evidence is allowed to upgrade a candidate link to probable or confirmed?
- Can multiple weaker signals together reach `probable`, and what threshold or review state prevents fake certainty?
- What should an LLM be allowed to produce: candidate links, evidence summaries, confidence suggestions, or final link decisions?
- What fields are forbidden because they would create a person dossier, outreach list, or real-world identity profile?
- Does table-shaped YAML/JSONL preserve a clean path to SQLite later?
- What would make SQLite worth adopting later?

## Hard constraints

- Do not create the actual ledger file.
- Do not populate any creator rows.
- Do not build a database, runner, crawler, scheduler, capture system, validator, migration, dashboard, or production store.
- Do not authorize Instagram, TikTok, or YouTube capture.
- Do not infer legal names, contact details, demographics, locations, private data, or cross-platform real-world identity.
- Do not create a `Creator` ontology type.
- Do not claim that any roster entry is a `WindCaller`.
- Do not treat LLM judgment as authority. It may assist evidence classification only if the architecture preserves source pointers, confidence labels, review state, and non-claims.

## Output contract

Return a concise architecture recommendation with this shape:

1. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
2. Cynefin routing result.
3. Architecture result:
   `TARGET_RECOMMENDED`, `OPTIONS_COMPARED_NO_SELECTION`,
   `NEEDS_SOURCE_CONTEXT`, `NEEDS_OWNER_DECISION`, or `DEFER_OR_REJECT`.
4. Plain-English definition of the safe object Orca is linking.
5. Option comparison, including SQLite-now versus static-table-first.
6. Recommended row/table model.
7. Evidence and confidence model:
   best evidence, weaker evidence, bundled weak evidence threshold, review states, and non-claims.
8. LLM-assist boundary.
9. Core and satellite boundaries.
10. Deferred implementation implications, including how hard a future SQLite migration would be.
11. Forbidden fields and fake-success risks.
12. Smallest complete next routing object.
13. Owner decisions still needed.

## Expected direction, not a forced answer

The likely target is a static, table-shaped docs-only ledger fixture first, with
`platform_accounts` and `account_link_evidence` separated from
`creator_roster_entries`. SQLite should be treated as a future storage option
that remains cheap if the static fixture is already relational in shape.

Do not rubber-stamp that direction. Compare it against SQLite-now and against a
defer/no-link option. If the sources show that cross-platform linking violates
current boundaries even with non-claims, say so.

## Non-claims

This architecture pass is not validation, readiness, buyer proof, legal
sufficiency, implementation authorization, capture authorization, database
authorization, ontology amendment, or permission to create or populate the
ledger.
