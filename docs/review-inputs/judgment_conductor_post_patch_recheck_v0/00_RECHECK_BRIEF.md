# Post-Patch Re-Review (Recheck) — Judgment Conductor (no_repo · advisory · findings-only · BOUNDED)

```yaml
retrieval_header_version: 1
artifact_role: Review-input bundle brief (delegated post-patch re-review; no_repo, advisory, bounded)
scope: >
  Bounded closure + blast-radius recheck of the Round-17 patch to the judgment conductor, for a
  repo-blind reviewer. Not Orca authority; advisory only.
use_when:
  - Running the commissioned no_repo post-patch re-review of the judgment conductor from this bundle.
authority_boundary: retrieval_only
```

## What this is
A REQUIRED de-correlated, no-repo POST-PATCH re-review. A first de-correlated pass (GPT-5.5 Thinking)
found 7 findings on the judgment conductor; the home model (Claude Opus-class) applied a bounded patch
(Round-17). This pass checks the PATCH only — it is BOUNDED, not a fresh full review. No repo access;
everything is in this bundle. Return FINDINGS ONLY (no diff/patch). You hold no verdict/validation authority.

## Inputs
- `sources/judgment_quality_promotion_operating_model_v0.md` — the PATCHED conductor (post-Round-17).
- `02_PATCH_DIFF.txt` — the exact Round-17 patch (the touched scope; commit cc41cfb).
- `01_FINDINGS_AND_ADJUDICATION.md` — the 7 findings, CA adjudication, and each `minimum_closure_condition`.
- `sources/` — the conductor owner sources (verify the patched predicates route correctly).
- `00_HASH_MANIFEST.txt` — confirm bundle bytes.

## Bounded task (do ONLY this)
1. Closure: for EACH of F1-F7, decide CLOSED / NOT_CLOSED / PARTIALLY against that finding's
   `minimum_closure_condition` in `01_...`, by reading the patched conductor + `02_PATCH_DIFF.txt`.
   Cite the owner source where closure depends on route-don't-restate fidelity.
2. Blast radius: in the touched scope ONLY (`02_PATCH_DIFF.txt`), find any NEW blocker/major the patch
   caused or made newly visible (new internal contradiction, new Invariant A/B breach, broken predicate).
EXCLUDE: fresh full-artifact review, unrelated critique, minor/nits, pre-existing issues outside the touched scope.

## Fitness reference (standard for closure)
The patch must keep the conductor airtight on the 4 seams + Invariant A (no-authority) + Invariant B
(route-don't-restate); JSG-01 must stay FROZEN (clears no case). Full detail in `01_...`.

## Output (return in your reply; the CA persists it)
Per finding F1-F7: status CLOSED|NOT_CLOSED|PARTIALLY + 1-line basis + owner-source cite.
Then `NEW_BLOCKER_OR_MAJOR` (touched scope only; or "none found"), `residual_risk` (1-2 lines), and
`provenance` (reviewed_by: your model+version; authored_by: Claude Opus-class).
Do NOT return a diff/patch or any PASS/validated/ready claim. A clean pass = all 7 CLOSED and no new blocker/major.

## Boundaries
- Advisory (no_repo): the CA adjudicates; anything short of a clean pass routes to another patch+re-review cycle.
- De-correlation (operator): post to a non-Opus model family different from the author (Claude Opus-class).
  The round-1 reviewer (GPT-5.5 Thinking) is fine; a different non-Opus family adds independence.
- Confirm bytes against `00_HASH_MANIFEST.txt`.
