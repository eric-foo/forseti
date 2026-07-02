# YouTube Leading-Dash Residual Fix PR 511

```yaml
retrieval_header_version: 1
artifact_role: Repo-map recent-change note
scope: Low-conflict context for the YouTube leading-dash id residual fix and the shared argv helper in PR #511.
use_when:
  - Reconstructing why YouTube capture runners share `_youtube_cli.py` argv normalization.
  - Checking PR #511 repo-map context without appending chronology to the main repo-map header.
open_next:
  - docs/workflows/orca_repo_map_v0.md
  - docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md
  - orca-harness/runners/_youtube_cli.py
authority_boundary: retrieval_only
```

PR #511 fixes the leading-dash YouTube id residual: a valid 11-character id
beginning with `-` now passes as `--video-id -...` through the shared argv
normalization helper `orca-harness/runners/_youtube_cli.py` (used by the
watch, caption, and ASR packet runners) while ordinary argparse errors for
registered option strings such as `--data-root` are preserved. With the
leading-dash retry, `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`
records 31 caption-route videos with watch+caption packets and complete
source-lineage-bearing product-extraction/projection; 2 watch-only videos
remain `no_extraction_eligible_sources`, ASR/no-caption remains unmeasured,
and platform-wide behavioral completeness is still not claimed.
