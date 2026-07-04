# Delegated Adversarial Code Review + Adjudication — Silver V3 Reader Gate + Vault Schema Tokens + Rank-Preservation Fixes (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review of the silver V3/V4 batch lane (reader-selection gate, record-shape
  schema tokens, F-SSS-002 rank-preservation fixes) and the home-CA
  adjudication that closed it: two accepted findings (F-SVG-001 — the reader
  gate exact-matched only direct lane_dir callers, so a new path-based
  derived-lane reader could bypass the posture registry; F-SVG-002 — schema-
  token closure rode module hash pins with no direct guard that the token is
  stamped into each writer), both delegate patches kept unmodified, and the
  reviewer's negative results on the no-bump and rank-preservation stakes.
use_when:
  - Checking what the V3/V4 batch review found and how the keep decisions were verified.
  - Citing the discharge of the per-unit independent-review gate for the commissioned eleven-file set at commit 688f3771.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5/Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (local branch claude/silver-v3-gate-vault-tokens; reviewer
    read HEAD c95c0f0f with pinned commit 688f3771 present locally and stated
    that all eleven commissioned blob SHA256s matched; the branch advance
    beyond the pin was the doc-only commission prompt commit)
  dispatch: docs/prompts/reviews/silver_v3_gate_vault_tokens_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: two findings (one major, one medium), bounded 2-file patch, no NEEDS_ARCHITECTURE_PASS
  findings: 2
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. The reviewer performed no live-lake run.
```

## Adjudication (claim → verification → decision)

**F-SVG-001 `[gate]` (major).** Claim: the reader-selection gate mechanically
exact-matched only direct `lane_dir` callers; the hand-declared free-walk
registry was not bound to the unit (b) `record_path` /
`is_record_set_complete` census, so a NEW path-based derived-lane reader
could avoid `lane_dir_reader_files()` and pass the gate undetected. CA
verification (not inherited): confirmed against the gate source at the pinned
commit — the free-walk registry had no mechanical backing (this was the
gate's own NAMED residual, which the patch converts from named-but-manual to
mechanically bound). Kept patch: a path-based census test requiring every
`record_path`/`is_record_set_complete` touchpoint outside the lane_dir set to
be either `declared_free_walk` or reason-excluded, with stale symmetry on
declarations AND exclusions. CA spot-checked the five exclusion reasons
against the unit (b) census observations of those writer-side files
(catch-up current-policy id checks, audit anchor resolution, orchestrator /
deep-capture completion-marker checks, projection proof-path checks) — all
consistent. **Decision: ACCEPTED unmodified.**

**F-SVG-002 `[gate-pins]` (medium).** Claim: record-schema-token closure
depended only on module hash pins; a future pin update could drop the stamped
payload field while appearing ritually handled. CA verification: correct —
the pin gate forces a conscious decision but never inspects the token sites.
Kept patch: `RECORD_SCHEMA_TOKEN_FIELD_SITES` direct source guard over the
four token constants and their stamped-field usages. Known accepted
limitation: literal-string matching (consistent with the gate family's
style); a rename refactor fails loudly rather than silently.
**Decision: ACCEPTED unmodified.**

**Reviewer negative results (recorded, not inherited as proof):** no
committed-packet re-surface path found for the no-bump token decision
(obligation/ack/record-id sweep), and no remaining content-dedupe layer that
silently drops catch-up rank after the F-SSS-002 fixes.

**Validation (CA's own run, kept state):** full suite via `--junitxml` with
`ORCA_DATA_ROOT` cleared: **2881 tests, 0 failures, 0 errors, 7 skipped** —
consistent with the delegate-reported `2874 passed, 7 skipped` (its first
full-suite attempt failed on Windows temp permissions and was rerun with a
workspace basetemp; treated as claims, verified by the CA's own run).

## Residual disposition

- Mechanical detection still keys on `DataLakeRoot` call names; a reader
  using raw `Path` traversal with none of the census calls remains detectable
  only by review (the seed is hand-declared via
  `_DECLARED_FREE_WALK_WITHOUT_TOUCHPOINT`). Narrower after this patch;
  still named.
- Seed re-materialization remains blocked pending the owner-directed removal
  of the `vanzzcoser` test packets (two anchors enumerated read-only:
  `01KW9T70AM3SZE4VXKWG17ANZG`, `01KW9WD600VE4NXCKF364N8ZH9`); the automated
  deletion was denied by the harness permission classifier — operator-run
  removal required.

## Adjudication landing

Kept patch landed as commit `4efc8ec1` on `claude/silver-v3-gate-vault-tokens`
(2 files, +105). No hunks rejected or modified.
