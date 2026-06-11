# Orca Venue Registry Rejection — Owner Decision Record v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Durable home of the 2026-06-11 owner decision on venue knowledge: standing
  venue registry/atlas REJECTED; memory-free pure procedure REJECTED; thin
  exploration procedure + append-only provenance memory ADOPTED; the
  promote-on-reuse trigger (including its same-day counting widening) is the
  only revisit path. Lifted out of the procedure doc's Status block so the
  decision survives product-doc folds and re-homes.
use_when:
  - Checking whether a venue registry, atlas, source map, or card-set may be built.
  - Reading the promote-on-reuse trigger's binding terms and thresholds.
  - Auditing why no venue atlas exists despite the research pass.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/orca_venue_exploration_procedure_v0.md   # the operative method
  - docs/research/source_registry_practices_deep_research_report_v0.md   # evidence base
  - docs/decisions/pre_capture_discovery_spine_charter_recommendation_v0.md   # DO_NOT_BUILD spine outcome
stale_if:
  - A later recorded owner decision reverses or supersedes the rejection.
  - A promote-on-reuse trigger fires and a card-set decision record takes over that vertical's scope.
```

## Decision (owner, 2026-06-11, in-thread)

1. **REJECTED — standing venue registry / atlas / source map.** Basis: the
   adversarially-verified source-registry research (see `open_next`) —
   staleness is the evidenced top abandonment driver; honor-system maintenance
   rots even when automated tooling exists (checking was unscheduled); bloat is
   the default content trajectory; usage is episodic and awareness-bound.
2. **REJECTED — memory-free pure procedure.** It forfeits the compounding the
   owner explicitly wants from discovery.
3. **ADOPTED — shape C:** a thin exploration procedure plus append-only
   per-batch provenance memory (dated records of past walks; no maintained
   present-state asset). Operative method:
   `docs/product/core_spine/orca_venue_exploration_procedure_v0.md`.
4. **No new structure:** the pre-capture discovery spine charter question
   returned `DO_NOT_BUILD` (2026-06-11, commissioned CA lane; see its
   recommendation record in `open_next`).

## Promote-On-Reuse Trigger (the only revisit path)

Route a venue-registry decision back to the owner ONLY when one of these fires:

- the same vertical is screened a THIRD time — the candidate promotion is THAT
  vertical's provenance trail into a small owned card-set, never a general
  atlas;
- screens become multi-operator;
- sustained screen cadence exceeds about one per week;
- (widening, owner-accepted 2026-06-11) venue exploration performed outside
  batch case screens counts toward the same-vertical reuse count, recorded as
  dated `Venue Provenance` blocks in the exploring lane's durable artifact.

Thresholds are design values set in-thread 2026-06-11; amend by dated note. If
promotion ever happens, the card-set must carry the research's survival
ingredients: one named owner, a fixed per-entry review date, a hard size cap,
and delivery into the screen step itself.

## Why This Record Exists

The rejection and trigger previously lived only in the venue procedure's
Status block. Product docs fold or re-home at finder-frame sign-off (the
procedure's own `stale_if` says so); owner decisions must survive that. This
record is the durable home of the decision; the procedure remains the
operative method and this record does not duplicate its mechanics.

## Non-Claims

Not validation, readiness, or proof of the adopted shape's effectiveness. Not
finder-frame sign-off. Authorizes no build, registry, crawler, monitor, or
capture. The rejection binds until a later recorded owner decision supersedes
it; a fired trigger routes the question to the owner — it does not itself
authorize anything.
