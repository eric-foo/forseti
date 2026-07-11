# Repository scripts

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
