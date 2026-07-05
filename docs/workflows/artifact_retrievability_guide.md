# Forseti Artifact Retrievability Guide

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Operational guide for making Forseti artifacts findable, classifiable, stale-checkable, and source-loadable without making retrieval metadata authoritative.
use_when:
  - Creating or materially touching a durable human-authored Forseti workflow artifact.
  - Deciding whether temporary material should remain transient, enter hygiene triage, or be promoted.
  - Reviewing artifact retrievability, stale-source handling, or body-opening shape.
open_next:
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/retrieval-metadata.md
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/hygiene/README.md
downstream_consumers:
  - prompt authors
  - review authors
  - docs-write executors
  - hygiene maintainers
  - repo-map maintainers
stale_if:
  - .agents/workflow-overlay/source-of-truth.md changes Forseti source hierarchy or conflict rules.
  - .agents/workflow-overlay/source-loading.md changes retrieval-header expansion, source-pack, or body-shape guidance.
  - .agents/workflow-overlay/retrieval-metadata.md changes header applicability, fields, exclusions, or authority boundary.
  - .agents/workflow-overlay/artifact-folders.md changes accepted artifact folders, _inbox, or hygiene routing.
  - docs/hygiene/README.md changes temporary-retention metadata rules.
authority_boundary: retrieval_only
```

This guide is an operational playbook. It helps future agents apply Forseti's
overlay rules consistently, but it does not replace the overlay and does not
create authority, validation proof, approval, readiness, lifecycle completion,
deployment/install/resolver status, source-of-truth status, or edit permission.

If this guide conflicts with `AGENTS.md`, the overlay, an accepted Forseti source,
or a current user instruction, use the controlling source and treat this guide
or the affected artifact route as stale.

## Ownership Map

| Concern | Owner |
| --- | --- |
| Source hierarchy and conflict order | `.agents/workflow-overlay/source-of-truth.md` |
| Source packs, expansion rules, context budgets, source capsules | `.agents/workflow-overlay/source-loading.md` |
| Retrieval header fields, applicability, exclusions, bloat controls | `.agents/workflow-overlay/retrieval-metadata.md` |
| Accepted folders, `_inbox`, hygiene routing, no-implementation folders | `.agents/workflow-overlay/artifact-folders.md` |
| Artifact role bindings, permissions, freshness markers | `.agents/workflow-overlay/artifact-roles.md` |
| Completion and prompt validation gates | `.agents/workflow-overlay/validation-gates.md` |
| Repo navigation and recurring read packs | `docs/workflows/forseti_repo_map_v0.md` |
| Temporary retained material and cleanup triage | `docs/hygiene/README.md` and `docs/hygiene/queue.md` |

This guide owns examples, decision tests, body-opening shape, fresh-agent
checks, and report-only retrievability audit criteria. It does not own new
artifact roles, new header fields, source precedence, validation semantics, or
folder authority.

## Operating Rule

Make important durable artifacts self-locating. Do not make every file look
durable.

Use durable retrieval treatment when at least one condition is true:

- A future prompt, review, executor, handoff, product/proof step, or hygiene
  pass is expected to open the file.
- The artifact routes a future agent to source packs, controlling files,
  output paths, review lanes, stale conditions, or next workflow moves.
- The artifact records a durable decision, product/proof context, workflow
  record, review report, prompt, patch/rerun context, migration note,
  validation evidence locator, or supersession relationship.
- The artifact is temporary but intentionally retained because a named review,
  promotion, expiry, or removal condition exists.

Do not use durable retrieval treatment for "maybe useful someday." If the next
use cannot be named, keep the material chat-local, `_inbox` scratch, or ordinary
temporary notes.

## Material Touch Test

A material touch is a change that affects routing, artifact identity, scope,
claims, output destination, downstream use, evidence/provenance, stale
conditions, supersession, or authority boundaries.

Formatting-only changes, typo fixes, line-ending normalization, or mechanical
path churn do not by themselves require adding new retrieval metadata unless
the artifact is already being edited for decision-bearing content.

## Decision Table

Use this table after checking the controlling overlay files. It is
report-checkable guidance, not a source-of-truth replacement.

| Artifact class | Header treatment | Body opening should expose | Stale or recheck pattern | Do not use for |
| --- | --- | --- | --- | --- |
| Overlay authority file | Required when new or materially touched | Rule scope, conflict owner, downstream files affected, non-claims | Recheck the changed overlay section and any linked source-loading or validation rule | Product proof or external workflow authority |
| Full prompt artifact | Required when durable | Objective, source hierarchy, required reads, output mode, destination, hard constraints, validation gates | Recheck source hierarchy, template registry, output mode, and named target sources | Runtime authorization or implied model/skill readiness |
| Thin wrapper prompt | Required only when durable and expected to route future work | Full prompt path, hash or revision when material, target workspace, delta, output mode | Recheck referenced full prompt and target revision | Forking policy or restating project rules |
| Review prompt or review input | Required when saved for review | Review target, review lane, source hashes/revisions when material, allowed report path, read/write boundary | Recheck target identity, prompt revision, and review-lane authority | Patch authorization unless explicitly assigned elsewhere |
| Review report | Required when durable | Reviewed artifact, source inspected, findings/verdict under review lane, residual risks, non-claims | Recheck reviewed target hash/revision and controlling review prompt before reuse | Proof that target passed, approval, or mandatory remediation |
| Rerun or patch prompt | Required when durable | Prior artifact, frozen decisions, mutable field, unresolved finding, target files, output mode | Recheck prior artifact hash/revision and whether the finding is already resolved | Scope reset or broad re-review |
| Patch queue | Required when durable | Stable units, target files, accepted/non-accepted fixes, validation expectations, files not to touch | Recheck reviewed targets and accepted findings before execution | Source-changing authority by itself |
| Workflow record, architecture note, or implementation scope | Required when durable | Decision/result, source basis, next allowed step, blockers, non-claims | Recheck controlling overlay files and named target artifacts | Lifecycle completion or implementation readiness unless separately proven |
| Repo map, route card, or navigation surface | Required when it routes source loading | What to open first, when not to open it, controlling sources, stale triggers | Recheck folder structure, accepted folders, and named route targets | Evidence, product truth, validation, acceptance, or freshness proof |
| Product artifact | Required when downstream workflow stages are expected to retrieve it | Product question, decision status if any, source basis, proof boundary, excluded claims | Recheck product-proof overlay and controlling product decisions | Buyer pull, proof success, or product readiness unless separately evidenced |
| Research artifact | Required when it supports future product/proof work | Research question, evidence boundary, query/source list when material, synthesis/non-claims | Recheck source date boundary, query scope, and superseding synthesis | Product authority by default |
| Migration/import note | Required when durable | Source path, import boundary, current disposition, promotion or rejection rule | Recheck source file identity and accepted destination | Canonical promotion unless separately accepted |
| Hygiene queue or cleanup note | Required when it routes future cleanup | Queue item, retained reason, non-canonical boundary, promotion/removal condition, review/expiry | Recheck `review_by` or `expires_on`, owner/source lane, and whether removal condition is met | Authority, validation, readiness, product proof, or lifecycle completion |
| `_inbox` scratch | Excluded unless promoted | Creation note or queue item only when retained | Promote, queue, archive, or delete before citing | Forseti authority |
| Code, tests, generated outputs, installed copies, raw hits | Excluded unless future authority binds them as workflow evidence | Ordinary local conventions only | Use future code/test/generated controls if implementation is authorized | Workflow authority through metadata |

## Header Discipline

Use the header shape and field rules in
`.agents/workflow-overlay/retrieval-metadata.md`.

The header answers:

- what this artifact is;
- when a future agent should open it;
- what controlling source might be opened next;
- when it might be stale.

The header does not answer:

- whether the artifact is approved;
- whether validation passed;
- whether implementation may begin;
- whether a review finding is accepted;
- whether lifecycle, deployment, install, resolver, or publication work is
  complete.

Prefer `open_next` when it reduces future source loading. Do not use `open_next`
as an instruction to read every linked file. `source-loading.md` controls
whether a linked file should be opened for the current task.

## Body Opening Shape

For long or decision-bearing artifacts, place a source-loading surface near the
top. Use a compact section, paragraph, or table that answers the questions that
let a future agent stop reading early.

Recommended body-opening fields:

- Purpose: the decision, workflow move, or source-loading problem the artifact
  supports.
- Use when: concrete triggers for opening it.
- Do not use for: adjacent tasks or strict claims this artifact must not
  support.
- Authority boundary: which source wins if there is a conflict.
- Open next: the smallest next files or sections to inspect when material.
- Stale conditions: what upstream change would make routing unsafe.
- Recheck recipe: for high-provenance artifacts, the path, section, hash check,
  command, or owner decision needed to verify freshness.
- Non-claims: approval, validation, readiness, lifecycle, implementation, or
  proof claims that remain unproven.

Do not paste full source ledgers, full evidence bodies, or long readbacks into
the opening. Put detail later in the artifact and keep the opening useful for
routing.

## Conflict Order

When retrieval metadata, artifact body text, route maps, indexes, hygiene notes,
or workflow records disagree, use this order:

1. Current user instruction.
2. `AGENTS.md`.
3. `.agents/workflow-overlay/` for Forseti project facts, constraints, artifact
   folders, review lanes, validation gates, safety rules, and source hierarchy.
4. Accepted Forseti docs under `docs/` when they do not conflict with the overlay.
5. The target artifact body for its own evidence, reasoning, decision, review,
   or contract when it is fresh and has normal authority.
6. Retrieval header fields for orientation only.
7. Repo maps, indexes, source capsules, hygiene queues, prior prompts, and
   chat summaries as derived navigation unless a higher source promotes the
   exact claim.

If the body and header disagree, treat the header as stale and fix it when the
task authorizes edits. If the body and controlling source disagree, follow the
controlling source and classify the artifact as stale, superseded, or blocked
before routing from it.

## Stale And Recheck Pattern

Use `stale_if` for checkable upstream conditions, not vague age signals.

Prefer:

```yaml
stale_if:
  - .agents/workflow-overlay/retrieval-metadata.md changes header field rules.
  - reviewed target file is re-patched after input_hashes were recorded.
  - docs/workflows/forseti_repo_map_v0.md is superseded by a later repo map.
```

Avoid:

```yaml
stale_if:
  - if this seems old
  - if future work changes
```

For high-provenance artifacts, put the recheck method in the body opening or a
short `Recheck` section. Name the source path, heading, hash check, command, or
owner decision needed. Do not add a new header field for recheck recipes unless
the overlay later expands the header contract.

When a stale condition is met, do not silently route from the artifact. Open the
controlling source, mark the artifact stale or superseded if edits are
authorized, or return a blocker when the task needs a strict claim.

## Repo Maps And Indexes

Repo maps and indexes are retrieval aids. They help agents choose source packs,
but they do not replace artifact bodies, retrieval headers, or overlay
authority.

Add or update a repo-map entry only when it prevents recurring broad reads,
stabilizes a source-loading route, or warns agents away from high-risk scratch
or historical material. Do not add entries simply to mirror every file on disk.

Being listed in a repo map does not mean:

- the listed artifact is fresh;
- the artifact has passed validation;
- the artifact is accepted or approved;
- the artifact is product authority;
- the artifact can be edited.

The repo map should point to controlling sources for strict claims, especially
source hierarchy, source loading, artifact folders, product proof, review lanes,
and validation gates.

## Temporary Artifact Anti-Rot

Temporary retained material is allowed only when it has a future disposition.
It must not become a semi-permanent junk drawer.

Use this disposition order:

1. Keep chat-local or transient when no future source-loading value is expected.
2. Put raw, untriaged material in `docs/_inbox/` only as scratch and do not cite
   it as authority.
3. Add an item to `docs/hygiene/queue.md` when material needs review,
   promotion, archiving, or deletion.
4. Promote to an accepted docs folder only when the artifact role and
   destination are clear.

Every retained hygiene item should carry:

- created date;
- source or owner/source lane when inferable;
- current location;
- reason retained;
- non-canonical boundary;
- promotion destination when known;
- review or removal condition;
- `review_by` or `expires_on`;
- status.

Do not blindly retain, promote, or delete when ownership, supersession,
review/expiry date, or removal condition is unclear. Create or update a hygiene
queue item instead.

## Report-Only Audit Checks

These checks may be used in review, closeout, or docs-health passes. A finding
is a retrieval or hygiene defect. It is not proof that the artifact body is
false, that validation failed, or that broad edits are authorized.

Flag:

- in-scope durable workflow artifacts without `retrieval_header_version: 1`;
- `authority_boundary` values other than `retrieval_only`;
- header fields outside the overlay contract;
- artifact roles that are unbound or used as state claims;
- header or opening text that implies validation success, approval, readiness,
  lifecycle completion, deployment/install/resolver status, source promotion,
  publication, or edit permission;
- `open_next`, `supersedes`, or `superseded_by` paths that are broken or too
  broad to guide source loading;
- high-provenance artifacts without `input_hashes`, `branch_or_commit`, or a
  body-level omission reason;
- route maps or navigation surfaces missing known `open_next` or `stale_if`
  values;
- long artifacts whose first screen does not expose purpose, use/non-use,
  authority boundary, next source, stale conditions, or recheck recipe when
  material;
- hygiene items missing created date, retained reason, non-canonical boundary,
  promotion/removal condition, `review_by` or `expires_on`, or owner/source
  lane when inferable;
- broad backfill or metadata-normalization work not explicitly authorized;
- JB-specific paths, lifecycle rules, handoffs, validation habits, or policy
  treated as Forseti authority.

## Examples

Good durable workflow header:

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Architecture discussion for Forseti artifact retrievability hardening.
use_when:
  - Deciding whether the retrieval-spine architecture has been accepted.
open_next:
  - .agents/workflow-overlay/retrieval-metadata.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - .agents/workflow-overlay/retrieval-metadata.md changes header field rules.
authority_boundary: retrieval_only
```

Bad overclaiming header:

```yaml
retrieval_header_version: 1
artifact_role: validation_summary
scope: Validation passed and implementation ready.
status: PASS
authority_boundary: approved
```

Problems: `status` is not part of the retrieval header contract, `scope`
overclaims, and `authority_boundary` is not `retrieval_only`.

Temporary material worth retaining:

```text
created: 2026-05-24
source_or_owner_lane: current Codex thread
current_location: docs/_inbox/example.md
reason_retained: preserves unresolved review input for a named follow-up
non_canonical_boundary: scratch only; not Forseti authority
promote_to: docs/review-inputs/ if review is authorized
review_or_removal_condition: remove after follow-up review input is written
review_by: 2026-06-07
status: Open
```

Temporary material not worth retaining:

```text
One-off search notes that were not cited, not handed off, and not needed after
the current answer.
```

Keep it chat-local or delete the scratch. Do not add a durable header.

## Fresh-Agent Check

Before relying on a durable artifact as retrievable, ask:

1. Starting from `AGENTS.md`, the overlay README, source-loading, the repo map,
   or the relevant accepted folder, could a new agent find the artifact without
   broad repository search?
2. Could the agent classify the artifact role without inventing a new role?
3. Could the agent tell whether the artifact is stale, superseded, or bound to
   a specific input identity?
4. Could the agent identify the next source to open when one is necessary?
5. Could the agent distinguish retrieval metadata from authority, validation,
   approval, readiness, lifecycle completion, product proof, or edit permission?
6. Could the agent see whether temporary retained material should be promoted,
   reviewed, archived, or removed?

If any answer is no, fix the destination, header, body opening, stale condition,
repo-map route, or hygiene queue item when edits are authorized. Otherwise
record the defect as report-only routing risk.

## Adoption And Migration

Adoption is forward-only by default. Apply this guide to new or materially
touched durable artifacts and to explicitly authorized cleanup slices.

Do not broad-backfill historical artifacts merely to normalize formatting. Do
not create audit tooling, generated reports, tests, packages, automation, or
runtime validators without a later explicit implementation authorization.

When a strict claim depends on acceptance, validation, readiness, buyer pull,
deployment, resolver behavior, source-of-truth promotion, or edit permission,
open the controlling source or mark the claim `not proven`.
