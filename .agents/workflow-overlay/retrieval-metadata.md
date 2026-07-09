# Retrieval Metadata

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Retrieval-header contract for durable human-authored workflow artifacts.
use_when:
  - Defining or reviewing retrieval metadata for Orca artifacts.
  - Deciding whether a durable artifact needs a retrieval header.
authority_boundary: retrieval_only
```

This file defines Orca's lightweight retrieval-header contract for durable
human-authored workflow artifacts. It exists to help future agents find and
interpret the right artifact faster. It does not create authority.

For operational examples, artifact body-opening shape, fresh-agent checks, and
report-only retrievability audit guidance, use
`docs/workflows/artifact_retrievability_guide.md`. That guide is subordinate to
this overlay and must not add header fields, authority boundaries, validation
claims, artifact roles, or folder rules.

## Applicability

Use a retrieval header for new or materially touched durable human-authored
workflow artifacts when the artifact is expected to survive the current turn
and may affect future routing, planning, review, proof, validation, prompt, or
overlay work.

This includes durable artifacts in accepted Orca locations such as:

- `.agents/workflow-overlay/` files that define project authority;
- `docs/decisions/`;
- `docs/product/`;
- `docs/prompts/` and typed prompt child folders;
- `docs/review-inputs/` when the artifact is canonical review input rather
  than a temporary copy;
- `docs/review-outputs/`;
- `docs/workflows/`;
- `docs/migration/`;
- `docs/hygiene/` when the queue or note is intended to route future work.

Do not backfill every existing file by default. Add the header when an artifact
is new, materially touched, or part of a separately authorized proof slice.

## Exclusions

Do not require retrieval headers for:

- `docs/_inbox/` scratch unless promoted into an accepted folder;
- temporary notes, parking files, or disposable drafts with no durable role;
- simple folder README files that only describe a directory;
- generated outputs, if future Orca work authorizes generated artifacts;
- implementation code, tests, packages, runtimes, or build artifacts, if later
  authorized;
- installed global, user-level, plugin, or project-local skill copies;
- external reference material outside Orca;
- copied review-input material when the canonical artifact remains elsewhere;
- raw evidence units embedded inside a larger artifact.

If an excluded file is later promoted into a durable Orca artifact role, apply
the retrieval-header contract at promotion time.

## Core Header

Use this compact YAML shape near the top of the artifact, normally immediately
after the H1 title and before the main body:

```yaml
retrieval_header_version: 1
artifact_role:
scope:
use_when:
  -
authority_boundary: retrieval_only
```

Core field rules:

- `retrieval_header_version`: always `1`.
- `artifact_role`: the Orca artifact role or a concise repo-native role. If
  the role is required for authority and is not bound, fail visibly instead of
  inventing authority.
- `scope`: one concise statement of what the artifact covers.
- `use_when`: one to three bullets naming when a future agent should open this
  artifact.
- `authority_boundary`: always the controlled value `retrieval_only`.

## Controlled Authority Boundary

`retrieval_only` means the header helps agents find and interpret the artifact.
It does not create, upgrade, or imply:

- Forseti authority beyond the artifact's existing authority;
- validation proof;
- approval;
- readiness;
- lifecycle completion;
- deployment status;
- install status;
- resolver status;
- edit permission;
- source-of-truth status.

If the retrieval header conflicts with the artifact body, the overlay, an
accepted Orca source, or the current user instruction, the header loses. Treat
the artifact as stale or conflicting and open the controlling source.

## Triggered Fields

Add these fields only when they reduce future source loading or prevent a
material stale-source mistake:

```yaml
open_next:
supersedes:
superseded_by:
input_hashes:
branch_or_commit:
downstream_consumers:
stale_if:
```

Triggered field rules:

- `open_next`: preferred first triggered field; use it when one or more
  controlling sources should be opened after this artifact.
- `supersedes` and `superseded_by`: use when artifacts replace or are replaced
  by another durable artifact.
- `input_hashes`: use when exact provenance is safety-critical, especially for
  review reports, rerun prompts, patch prompts, proof/replay artifacts,
  cutoff-sensitive artifacts, cross-repo inputs, or dirty-state-dependent
  claims.
- `branch_or_commit`: use when the artifact depends on a specific repository
  revision or branch state.
- `downstream_consumers`: use when future prompts, reviews, workflows, or proof
  steps depend on this artifact and would otherwise be hard to discover.
- `stale_if`: use when a clear condition should force rereading or retirement
  of the artifact.

Omit a triggered field unless it changes what a future agent should open,
verify, or avoid trusting.

## Forbidden Header Fields

Do not put these concepts in the retrieval header:

- approval status;
- validation status or proof result;
- readiness status;
- lifecycle state;
- deployment, install, resolver, or publication state;
- edit permission;
- executor authorization;
- review verdict;
- source-of-truth promotion.

Artifact bodies may still contain Orca-approved status, verdict, validation,
or authorization language where the artifact role requires it. The retrieval
header itself stays retrieval-only.

## Bloat Controls

- Keep the core header to five fields unless a triggered field passes the
  retrieval-value test.
- Prefer `open_next` over long source lists when the next controlling source is
  enough.
- Do not duplicate full source-read ledgers in the header.
- Do not add universal hashes.
- Do not backfill old artifacts just to normalize formatting.
- Remove a triggered field when it stops changing source-loading behavior.

## Review Checks

When reviewing a new or materially touched durable artifact, check that:

- the header is present when the artifact is in scope;
- excluded artifacts are not promoted by metadata;
- `authority_boundary` is exactly `retrieval_only`;
- triggered fields are justified by retrieval value or provenance risk;
- no forbidden header field creates authority, validation proof, approval,
  readiness, lifecycle completion, deployment/install/resolver status, or edit
  permission.

Use `docs/workflows/artifact_retrievability_guide.md` for report-only checks
of body-opening shape, stale/recheck clarity, repo-map/index treatment, and
temporary-artifact anti-rot. Those checks identify retrieval or hygiene defects;
they do not prove or disprove validation, readiness, approval, lifecycle
completion, or edit permission.
