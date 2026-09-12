# Repository scripts

## Agent CI observation

From `forseti-harness`, use
`python -m runners.run_ci_watch --repo OWNER/REPO --pr NUMBER --head SHA --output-dir _scratch/ci-watch`.
Supply the full expected commit SHA. GitHub CLI owns polling; normal tool waits
preserve the runtime's responsiveness requirement. Watch output remains on disk
and one JSON result identifies the final counts, issues and full record. Failure,
missing checks, timeout and revision changes remain nonzero. The watch timeout
defaults to 900 seconds; identity/check snapshots each have a 30-second timeout.
This read-only command never merges and does not replace the fresh merge guard.
`merge-when-green.ps1` remains a human-only merge helper.

## Review-report mechanics

`review-report-mechanics.py` assembles or verifies a reviewer-authored report
without making review decisions. It accepts an explicit worktree, base ref,
report path, and patch paths; `assemble` additionally accepts a draft containing
exactly one `{{REVIEW_MECHANICS_UNIFIED_DIFF}}` token.

```powershell
python .github/scripts/review-report-mechanics.py assemble `
  --worktree . `
  --base HEAD `
  --draft docs/_inbox/review-draft.md `
  --report docs/review-outputs/example-review.md `
  --patch path/to/changed-file.py

python .github/scripts/review-report-mechanics.py verify `
  --worktree . `
  --base HEAD `
  --report docs/review-outputs/example-review.md `
  --patch path/to/changed-file.py
```

The runner emits one compact JSON receipt containing only observed paths,
hashes, exit codes, and gate buckets. It invokes Git plus the existing review
provenance and summary-shape checkers. Failures remain nonzero and visible; an
existing report is replaced only when `assemble --replace` is explicit. The
report path may not be named `README.md`: that basename is excluded from both
downstream checkers' scope, so the runner rejects it rather than silently
skipping provenance/summary verification.
