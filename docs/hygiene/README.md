# Forseti Hygiene

```yaml
retrieval_header_version: 1
artifact_role: Hygiene queue
scope: Local rule surface for Forseti hygiene queues, cleanup notes, and temporary retained material.
use_when:
  - Deciding whether temporary or parked material belongs in docs/hygiene/.
  - Checking required metadata before retaining, promoting, archiving, or deleting parked material.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - docs/workflows/artifact_retrievability_guide.md
  - docs/hygiene/queue.md
```

Use this folder for docs-first triage queues and cleanup notes.

The main queue is `queue.md`. Track temporary or parked material there when it needs promotion, review, archiving, or deletion.

## Boundary

Material tracked here is non-canonical unless a higher Forseti authority promotes
the exact claim or artifact into an accepted docs folder or overlay file.

Do not cite hygiene material for validation, approval, readiness, product proof,
lifecycle completion, source-of-truth status, or edit permission.

## Retained Item Metadata

Every retained hygiene item should record:

- created date or explicit `Unknown`;
- source or owner/source lane when inferable;
- current location;
- reason retained;
- non-canonical boundary;
- promotion destination when known;
- review or removal condition;
- `review_by` or `expires_on`;
- status.

If ownership, supersession, review date, expiry date, or removal condition is
unclear, do not blindly retain, promote, or delete the item. Keep or add a queue
entry that names the uncertainty and the smallest next decision.
