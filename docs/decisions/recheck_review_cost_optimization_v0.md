# Recheck Review Cost Optimization v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Operator latitude to route low-stakes post-patch / blast-radius rechecks to a cheaper model tier,
  on the finding that such rechecks rarely surface a NEW major. Model-neutral: it records a finding +
  operator latitude and does NOT prescribe a runtime model in any review lane. Also records a related,
  separate, optional latitude (see end): running an ordinary review pass before a delegated de-correlated
  commission, to focus the expensive pass.
use_when:
  - Choosing the model tier for a post-patch or blast-radius recheck.
  - Checking whether a recheck may run on a cheaper model.
  - Deciding whether to run a cheap objective review pass before a delegated de-correlated commission.
authority_boundary: retrieval_only
status: adopted_decision   # records a finding + operator latitude already permitted by review-lane model-neutrality; NOT a new lane, NOT a doctrine change, no DCP receipt required
evidence_base:
  - 2-week review-corpus mining (this session): post-patch + blast-radius rechecks surfaced a NEW blocker/major in ~6 of 46 recheck files; the rest confirmed closure with no new major.
input_hashes:
  .agents/workflow-overlay/review-lanes.md: c3f37fb2e02b9ca6dee55e685c9913035a9cca050acff7954294e5e2a417df72
branch_or_commit: ecr-sp3-timing-deriver-slice1 (extends the no_repo delegated-review doctrine committed in 285fa57)
stale_if:
  - A larger corpus pass materially changes the recheck new-major rate.
  - Owner changes review-lane model-neutrality.
  - Owner mandates or forbids a pre-delegation objective review pass, or reviewed_by data measures its net effect.
```

## Decision (adopted)

- **Finding.** In the 2-week corpus, post-patch / blast-radius **rechecks** (the "did the patch land + any new major?" passes) surfaced a new blocker/major in only **~6 of 46** files; the rest confirmed closure with nothing new. Rechecks are near-zero-yield for *new* majors.
- **Decision.** The **operator/tooling may route a low-stakes recheck to a cheaper model tier.** This is a runtime model choice (operator-owned), **not** a review-lane prescription — `review-lanes.md` model-neutrality is preserved and unchanged. The recheck still happens; only its model tier is cheaper.
- **Safety carve-outs — do NOT downgrade the recheck when:**
  - the underlying patch touched a **high-lock-in / irreversible** artifact (doctrine, operating contracts, security/credential handling, irreversible side-effects) — that recheck keeps the stronger reviewer;
  - a **compounding-minor** is in play — fix minor-but-compounding findings regardless of the cheaper tier.
- **Scope.** This is the single cost optimization deliberately separated from the declined routing policy (`adversarial_review_routing_policy_v0.md`, tiers declined by owner). It stands alone; it binds nothing beyond recording this latitude + finding.

## Validity / limits

- Evidence is **one 2-week mining pass** (~6/46), not a controlled measurement. The latitude is **informed, not proven** — widen the carve-outs if a cheap-tier recheck is ever caught missing a real major. (`reviewed_by` attribution, if adopted, is what would let this be measured rather than assumed.)
- This record grants the latitude + the evidence; the actual saving is realized only when the operator/tooling actually routes rechecks to the cheaper tier.

## Related optional latitude (separate from the recheck-downgrade)

This is a distinct, optional cost move — not part of the recheck-downgrade above, not a new review lane, and not mandated.

- **Latitude.** An operator MAY run an ordinary read-only review pass (the standard `workflow-adversarial-artifact-review` / `workflow-code-review` lane) *before* commissioning a delegated de-correlated review-and-patch pass, to clear cheap objective defects (conformance, internal consistency, overclaims, scope) so the expensive delegated pass focuses on the goal-fitness judgment.
- **Already available; model-neutral.** Nothing forbids this today; it routes by *lane*, not model family (the ordinary lane carries no family constraint; the delegated lane carries the de-correlation who-constraint). It selects no runtime model — that stays an operator/tooling choice. Recording it binds no doctrine, lane, or skill change.
- **Why it is unproven and not mandated.** The delegated controller already runs the *full* review lane (objective + goal-fitness), so a precursor does not raise recall over the delegated pass — it only shifts cheap objective coverage earlier and cheaper. Net cost is unmeasured and could be negative (it adds a pass; the controller re-covers the objective layer regardless). Informed-not-proven; measure via `reviewed_by` before considering any mandate.
