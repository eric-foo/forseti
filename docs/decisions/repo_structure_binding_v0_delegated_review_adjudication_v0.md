# Repo Structure Binding v0 - Delegated Review Adjudication

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Home-model (CA) adjudication of the cross-vendor delegated review of the
  repo-structure binding v0 bundle: finding dispositions, applied patches,
  bounded recheck result, and the kept state.
use_when:
  - Checking what the delegated review found and what was kept or rejected.
  - Auditing the binding/checker/runbook patch set of 2026-06-11.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_repo_structure_binding_v0.md
  - docs/review-inputs/repo_structure_binding_v0_delegated_review_v0/MANIFEST.md
```

## Commission and actors

- Convention: provisional opt-in Delegated Review-and-Patch
  (`.agents/workflow-overlay/delegated-review-patch.md`), `no_repo` mode.
- Bundle: `docs/review-inputs/repo_structure_binding_v0_delegated_review_v0/`
  (hash-pinned attachments; the as-reviewed snapshot).
- Discovery reviewer (cross-vendor who-constraint): OpenAI / GPT-5.5 Thinking
  (self-declared; satisfies author-vendor != delegate-vendor; Anthropic author).
- CA / home model (adjudication + patch application): Claude (Fable 5).
- Bounded post-patch recheck (same-vendor lower/mechanical tier per the
  overlay): Claude Haiku subagent, scope = closure of findings + new
  blocker/major in the touched delta only.

## Findings and dispositions

- **DRB-001 (major) - binding/map lane-status mismatch: ACCEPTED.** The
  binding's "lanes are `planned`" sentence went stale when the Phase-2 apply
  flipped the map to `current` (a transition the binding's own `stale_if`
  declared). Patched the binding's product-lane paragraph to the reviewer's
  state-agnostic rule (status must match actual migration state) plus the
  apply date.
- **DRB-002 (major) - checker did not enforce lane membership: ACCEPTED via
  the stronger arm of the reviewer's sufficiency clause.** Rather than adding
  a disclaiming sentence to the binding, `check_placement.py` was extended:
  unknown subfolders under `docs/product/` now classify as violations
  (`'docs/product/<x>/' is not a bound product lane`), with selftest cases
  for an unknown lane (rejected) and depth below a bound lane (ok). CA also
  fixed an adjacent regression the reviewer's finding exposed: the flat-product
  lane nudge had been keyed to the retired legacy tolerance; it now fires for
  OK-status flat writes too (post-apply residuals).
- **DRB-003 (minor) - "Validated by dry-run" claim inflation: ACCEPTED.**
  Runbook now reads "Dry-run checked 2026-06-11: exit 0, zero collisions" and
  carries an APPLIED status note per its own `stale_if`.

Nothing was rejected; no `NEEDS_ARCHITECTURE_PASS` was raised; the reviewer's
verdict was sound-with-patches.

## Recheck result (bounded, same-vendor lower tier)

3/3 findings verified CLOSED against current file text/code; no new
blocker/major found in the touched delta; checker selftest 18 cases + 6
guards pass; live-tree `--strict` exit 0. The recheck is verification of
known closure conditions, not a discovery pass, and creates no
no-new-seam claim beyond the cross-vendor discovery review.

## Kept state

Touched delta kept in full: `docs/decisions/forseti_repo_structure_binding_v0.md`
(DRB-001 wording), `.agents/hooks/check_placement.py` (DRB-002 lane
enforcement + nudge restoration + selftest cases), the Phase-2 runbook
(DRB-003 wording + applied-status note). The review bundle remains the
as-reviewed snapshot and is intentionally not refreshed; its MANIFEST hashes
pin what the reviewer saw.

## Non-claims

- Not validation, readiness, acceptance of the binding beyond its own
  owner-authorized v0 status; reviewer findings and the recheck create no
  strict claims.
- The cross-vendor reviewer's lineage is self-declared in its output; the
  commission records it as such.
- Placement checking remains shape-only; placement is not authority.
