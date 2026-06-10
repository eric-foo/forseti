# No-repo cross-vendor adversarial review bundle — Orca overlay: de-correlation family = vendor + two-bar

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: >
  No-repo cross-vendor adversarial-review bundle manifest for the uncommitted
  Orca overlay edit defining de-correlation "family" = vendor + the two-bar
  review-tier rule. Names the source files + hashes, what changed, and the review
  focus. A courier for an external review; not a verdict and not a kept change.
use_when:
  - Running or couriering the cross-vendor adversarial review of the family=vendor overlay edit.
  - Confirming the bundle's source files + hashes before or after the review.
authority_boundary: retrieval_only
input_hashes:
  .agents/workflow-overlay/delegated-review-patch.md: 26802AD9CE0BFA30630361CD9FA59AF27115D63E089F214657291048A05F8CC8
  .agents/workflow-overlay/review-lanes.md: FBB2AA513329B88F01B6D9049536738FED8CA07D6BF90233FBECFD22721F7A56
branch_or_commit: ecr-sp3-timing-deriver-slice1 (working tree; the edit is held uncommitted)
stale_if:
  - Either overlay file changes (re-hash + rebundle).
  - The overlay edit is committed or abandoned (the review target moves).
```

Review-input courier for a **cross-vendor (non-Anthropic)** adversarial artifact
review of an **uncommitted** Orca overlay doctrine edit. Findings-only; the author
(Orca CA, Claude/Opus) adjudicates, applies accepted fixes, and commits. Keep or
discard after the review at the operator's discretion.

## Files (review the WHOLE file — a "new seam" can be a contradiction anywhere, not just the changed lines)

- `delegated-review-patch.md` — sha256 `26802AD9CE0BFA30630361CD9FA59AF27115D63E089F214657291048A05F8CC8`
- `review-lanes.md` — sha256 `FBB2AA513329B88F01B6D9049536738FED8CA07D6BF90233FBECFD22721F7A56`

(Both are `.agents/workflow-overlay/` files in the working tree, with the held edit applied.)

## What changed (the edit under review)

De-correlation **"family" is pinned to VENDOR / model lineage (not tier)**, with a
**two-bar** rule — **cross-vendor = the discovery bar** (required to claim the
no-new-seam standard for a full or doctrine-surface pass); **same-vendor
lower/mechanical-tier = the bounded sanity / verification tier** (advisory) — plus
a requirement to **record why the cross-vendor bar was not needed** when the
same-vendor bar is chosen.

- `delegated-review-patch.md`: the "De-correlation — observable criterion and
  fallback" paragraph; the `de_correlation_criterion` in `model_ladder`; and the
  `no_repo` clause wording (same-family→same-vendor, cross-family→cross-vendor).
- `review-lanes.md`: a new "Two-bar de-correlation (review tier; family = vendor)"
  bullet in the Review Doctrine list; an appended `direction_change_propagation` block.

## Review focus

- (a) Does family = vendor REMOVE the prior internal contradiction — `de_correlation_criterion` had said "Opus author requires a non-Opus delegate" (tier-flavored) while the `no_repo` clause treats same-vendor lower tier (Opus→Sonnet) as "same-family … NOT cross-family"? Consistent now across both files?
- (b) Is "vendor / model lineage" unambiguous (same-lab variants, fine-tunes, white-labels, an Anthropic model served via a third party)?
- (c) Any NEW contradiction with the unchanged adjacent rules — the `reviewed_by`/`authored_by` provenance fields (which make same-vs-cross-family coverage measurable) and review-lane **model-neutrality** (never recommend/rank/imply a runtime model)?
- (d) Are the two-bar rule + the same-vendor justification requirement coherent and *checkable* (could an operator mechanically tell which bar applies + whether the justification is present; any loophole letting a same-vendor pass claim the no-new-seam standard)?

## How to run

Paste the full adversarial-artifact-review prompt (provided in chat) and attach
these files. The reviewer **must be non-Anthropic** (cross-vendor = the discovery
bar for this doctrine surface). Output: findings-only (no diff), severity-labeled,
neutral decision-sufficient citations, verdict + residual. Findings are decision
input only — not approval, validation, or a keep decision.
