# Delegated Adversarial Code Review + Adjudication — SoV Readout View Build (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review-and-patch of the SoV readout view build (data_lake/sov_readout.py +
  runners/run_data_lake_sov_readout.py + tests/test_data_lake_sov_readout.py)
  and the home-CA adjudication that closed it: reviewer identity, the finding,
  per-hunk accept/reject decisions, the CA closure checks (fresh test run,
  byte/scope check, class sweep), and the named residuals.
use_when:
  - Checking what the SoV view-build code review found and what the CA kept or rejected.
  - Verifying the de-correlation and gate-discharge provenance behind the view build's patch pass.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit 59225845ba8f497a95ef6865bc27367cf639327c on
    branch claude/sov-view-build, merged to main via PR #621 squash; delegate
    patched directly in the lane worktree per the base-subagent loop)
  dispatch: docs/prompts/reviews/sov_view_build_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: CA_adjudicate_diff_accept_or_modify (patch-level, no NEEDS_ARCHITECTURE_PASS)
  findings: 1 major
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, formal
  lane verdict, or acceptance. Extraction-quality validity (recall/precision/
  brand-attribution of the upstream extractor) is explicitly NOT established by
  this pass; it is the named next measurement unit.
```

## Adjudication (finding: claim → verification → decision)

1. **F1 (major) — read-side mention validation laundered malformed persisted
   mentions into counted evidence — ACCEPTED.** Claim verified against the
   persisted schema (`orca-harness/schemas/product_mention_models.py:97-141`:
   non-empty `brand`/`line`; `start_ms >= 0`; `end_ms >= start_ms`) and the
   field contract's exact-string group-key + dereferenceable-ref clauses:
   pre-patch `_well_formed_mention` coerced a blank persisted `brand` to
   `"unknown"` and a non-string `line` to `""` (inventing group keys not
   present verbatim in the committed record) and accepted any `int` span
   (including bools and inverted/negative spans). Impact: a corrupt or
   hand-tampered record could feed denominator/share instead of surfacing as a
   defect. Applied fix: reject-and-count — malformed entries go to
   `coverage.malformed_mention_entries`, never into rows; span check tightened
   to `type() is int`, `start_ms >= 0`, `end_ms >= start_ms` (mirrors the
   write-side validators exactly).

**Hunk dispositions:** all hunks ACCEPTED unmodified — module hunk (span
bounds + bool rejection; blank brand rejected; blank/non-string line
rejected) and the three test hunks (the "unknown" row fixture now sources
from the extractor's literal `"unknown"`; three malformed fixtures pin
`malformed_mention_entries == 4` and rows constrained to exactly the valid
key). Nothing modified; nothing rejected.

## CA closure checks (gate discharge)

- **Byte/scope check:** fresh `git diff --stat` on the lane worktree showed
  exactly the two commissioned files (module + tests; the runner needed no
  change), 16 insertions / 7 deletions, matching the couriered diff
  hunk-for-hunk. No file outside the named set was touched.
- **Fresh test run (delegate claims re-verified, not inherited):** 45 passed —
  `tests/test_data_lake_sov_readout.py` (14),
  `tests/contract/test_capture_runner_lake_seam_coverage.py` (16),
  `tests/contract/test_data_lake_inventory_gate.py` (15) — plus the full
  orca-harness suite on the patched tree: 2550 tests, 0 failures, 0 errors,
  7 skipped (JUnit-XML-verified, ORCA_DATA_ROOT cleared, 2026-07-03).
- **Class sweep (F1's leak class: read-side coercion of persisted fields into
  evidence):** remaining coercions in `sov_readout.py` are (a) cohort-matching
  identity keys (`source_object` fields coerced for set membership — blank
  values cannot match any declared member, so this path can only EXCLUDE,
  never admit evidence) and (b) the `"unversioned"` rubric disclosure token in
  `selection_policy_versions` (labels provenance; feeds no count and no group
  key). Neither is the leak class. One same-class occurrence exists OUTSIDE
  the commissioned set: `derived_retrieval_views.py` `build_by_mention_view`
  coerces blank brand/line into index keys — it is a retrieval index, not a
  counting readout, and is out of commissioned scope; recorded as a residual
  below rather than patched.
- Per the delegated-review-patch overlay ("Code-diff target kind" +
  repo-mode discharge), this repo-mode discovery pass plus the checks above
  **discharge the independent-review gate** for the patched set; no separate
  post-patch cross-vendor re-scan is required.

## Named residuals (open, not defects closed by this pass)

- `comparison_set_ref` source-backedness is declaration-only (reviewer
  residual, concurred): the readout requires the ref to be declared but no
  validator dereferences it yet. Upgrade trigger: first buyer-facing readout
  carrying a comparison_set.
- `by_mention` index-key coercion (CA class-sweep note above). Upgrade
  trigger: any use of by_mention keys as a counting/evidence surface.
- Extraction-quality validity (extractor recall/precision, brand-unknown
  rate, brand knowledge-leak rate) is unmeasured; the SoV readout is honest
  about its inputs but only as meaningful as they are. Owner-routed next
  unit: the extraction-quality eval.

## Reviewer read-budget audit (as returned)

Target files full; field contract full; seam contract targeted
(On-Demand-First/rebuildability); supporting sources targeted (incumbent view
pattern, lineage gate, mention record shape, root by-key/write APIs,
AGENTS/overlay authority).
