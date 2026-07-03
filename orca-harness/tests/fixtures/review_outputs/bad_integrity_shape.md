<!-- fixture_expected: fail -->
<!-- fixture_purpose: malformed review-output integrity shapes fail -->

# Fixture Review Output

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Fixture review output for provenance checker.
use_when:
  - Testing review-output provenance shape.
authority_boundary: retrieval_only
reviewed_by: gpt-5-codex
authored_by: claude-opus-4.8
review_use_boundary: >
  Findings are decision input only. They are not approval, validation,
  mandatory remediation, or executor-ready patch authority until separately
  accepted or authorized.
```

## Validation Evidence

- Report provenance: must be checked after this report is written.

## Diff

```diff# generated comment
diff --git a/x b/x index 111..222 100644 --- a/x +++ b/x @@ -1 +1 @@
```