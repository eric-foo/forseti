# Delegated Adversarial Code Review + Adjudication — Fragrantica Cleaning Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review-and-patch of the Fragrantica Cleaning seam catch-up unit
  (g-reviews/cleaning, fragrantica; runners/run_fragrantica_cleaning_catchup.py
  + tests) and the home-CA adjudication that closed it: the two findings,
  their dispositions, the CA closure checks, the class-sweep notes, and the
  design conventions the next cleaning catch-up units (basenotes, parfumo)
  must inherit.
use_when:
  - Checking what the fragrantica catch-up review found and what the CA kept or rejected.
  - Authoring the basenotes/parfumo catch-up units (inherit the fuller policy envelope + surface allowlist conventions recorded here).
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 via Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit 4134d8bdf3cfa7619f2ac56d4dd17bf92f9e972d read at the
    claude/fragrantica-cleaning-seam-catchup lane head; both commissioned
    SHA256 pins matched by reviewer; delegate applied the patch directly in
    the lane worktree — no commit/push, per commission)
  dispatch: docs/prompts/reviews/fragrantica_cleaning_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: patch-level (no NEEDS_ARCHITECTURE_PASS)
  findings: 2
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. No live-lake run was performed; this runner has never executed
  outside temp-lake tests.
```

## Adjudication (per finding: claim → verification → decision)

1. **F-FRAG-001 (major) `[frag-runner]` — the obligation snapshot omitted
   output-shaping policy tokens — ACCEPTED.** Verified against the derivation
   sources: the audit pack embeds the projection method/certification and the
   generic audit-pack schema version; the Silver records embed the vault
   record schema version and the cleaning method id; and the transform-rule
   names plus the vote-metric specs select and shape which Silver records are
   emitted — yet the commissioned envelope carried only five tokens, so a
   change to any omitted constant would leave old outputs acked as current
   (the exact F2/seam-envelope class: an input whose change must re-trigger
   work missing from the snapshot). Kept the delegate's fix: the envelope now
   carries all output-shaping constants (projection method/version/
   certification, both audit schema versions, both silver schema versions,
   cleaning method id, the two transform-rule names, and the vote-metric
   specs), with a token-presence test and a second policy-bump test
   (cleaning_method_id) pinning the re-surface behavior. Coupling note,
   accepted: the envelope imports the private `_REVIEW_VOTE_METRIC_SPECS`
   from the read-only cleaning module — publicizing that name would exceed
   the commissioned patch scope; the coupling fails visibly (ImportError) if
   the cleaning module refactors. Queued as a possible one-line rename in a
   later cleaning-owned change.
2. **F-FRAG-002 (major) `[frag-runner]` — the surface gate acknowledged EVERY
   non-Fragrantica surface, including unknown future surfaces — ACCEPTED.**
   The commission asked the reviewer to challenge the authored all-surface
   design, and the challenge lands: the envelope carries no surface
   knowledge, so a FUTURE Fragrantica-owned surface (or any newly added
   family surface) captured before the runner supports it would be acked
   out-of-scope under an unchanged fingerprint and NEVER re-surface — a
   permanent silent pre-close, strictly worse than visible churn. Kept the
   delegate's fix: known basenotes/parfumo surfaces (verified by the CA
   against their capture/projection sources) are acked with an explicit
   `basis: known_non_fragrantica_source_surface` evidence field; unknown
   surfaces get a visible `unsupported_surface` status (CLI exit nonzero),
   NO ack, and re-surface every run until deliberately classified.

**Hunk dispositions:** all hunks ACCEPTED as returned (delegate-applied in
the lane worktree; the CA verified the applied content directly against the
working tree). Nothing modified; nothing rejected.

## CA closure checks (gate discharge)

- **Byte/scope check:** `git status`/`git diff --stat` show exactly the two
  commissioned files modified (+127/-13 across runner and tests);
  `git diff --check` clean (CRLF working-copy warnings only); read-only
  surfaces untouched.
- **Fresh test run (CA's own, not the delegate's claim):** full orca-harness
  suite with the kept patch, JUnit-verified: 2656 tests, 0 failures,
  0 errors, 7 skipped (`ORCA_DATA_ROOT` cleared); the token-presence,
  method-id-bump, and unknown-surface tests confirmed present in the JUnit
  case list. Touchpoint inventory unaffected (no new counted calls).
- **Class sweep (F-FRAG-001's class — output-shaping constants missing from
  a seam envelope):** ECR is covered by design (`ECR_DERIVER_VERSION` is the
  declared cover-all; its comment-bound bump discipline is already a
  recorded residual). The YT/IG extraction envelopes carry their dominant
  policy tokens (model, rubric) but not e.g. the lineage schema constant
  their outputs embed — WEAK members, unflagged by both of their own
  cross-vendor reviews; recorded as a census-closure residual rather than a
  queued patch. **Convention for the next units:** basenotes/parfumo
  catch-ups must enumerate every output-shaping constant into their
  envelopes from the start.
- **Class sweep (F-FRAG-002's class — open-world acking over a shared
  discriminator):** ECR consumes every family by design (universal deriver;
  no discriminator, not a member); YT/IG filter by family+surface inside
  their own discovery and ack only what they processed (not members).
  **Convention for the next units:** basenotes/parfumo catch-ups inherit the
  allowlist + `unsupported_surface` shape, never an open-world else-branch.
- Per the delegated-review-patch overlay, this repo-mode pass plus the checks
  above discharge the independent-review gate for the patched set.

## Residual disposition

- Pre-patch acks for unknown/future surfaces (the reviewer's untrust class):
  EMPTY — this runner has never executed outside temp-lake tests (the lane
  PR is unmerged and the live lake carries only the fragrantica surface).
- Envelope enlargement re-surfacing old-shape acks once: moot for the same
  reason; no live acks exist for this lane.
- Private-constant import coupling: accepted, fail-visible, queued as a
  cleaning-owned rename candidate.

## Reviewer read-budget audit (as returned)

Commission full; target files full; seam contract, consumption helper,
Fragrantica derivation/projection/cleaning, basenotes/parfumo cleaners, ECR
pattern + adjudication report, lane registry, AGENTS/overlay, seam-coverage
and inventory gate sources read. Reviewer-run validation: target suite and
commissioned suite passed; `git diff --check` exit 0.
