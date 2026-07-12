# TikTok Product Extract Runner Delegated Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated implementation/code review-and-patch output
scope: >
  Cross-vendor review and bounded patch of the staged TikTok transcript-product
  extraction runner on codex/tiktok-product-extract-runner.
use_when:
  - Auditing the sibling-isolation correction applied before the runner lane was committed.
  - Reconstructing the review evidence and home-model adjudication for this implementation.
authority_boundary: retrieval_only
reviewed_by: Anthropic Claude Sonnet 5
authored_by: OpenAI GPT-5 Codex
review_use_boundary: >
  Findings and patches are decision input for home-model adjudication; this
  record is not approval, validation, mandatory remediation, patch authority,
  deployment readiness, or a live-extraction claim.
```

## Commission

- Review lane: `workflow-code-review` under the delegated code review-and-patch convention.
- Target: staged implementation diff on branch `codex/tiktok-product-extract-runner`, base
  `a6a24833d0a8fc0e82b6e77f4bc8d49a31d84e70`.
- Patch authority: runner and focused test files only; other staged files remained read-only.
- De-correlation: author vendor OpenAI; controller vendor Anthropic; cross-vendor discovery bar satisfied.
- Excluded: live provider calls, capture changes, entity normalization, comments, SoV, Gold/Judgment,
  Creator Registry, live-lake writes, commits, pushes, and PR actions.

## Finding

### F-01 — Blocker — malformed sibling aborted the entire batch

Before the delegated patch, `_transcripts_for_packet` normalized every video inside one
packet-grain function. A malformed cue, timestamp, transcript, or hash raised before the function
returned, discarding already-normalized valid sibling transcripts. The packet remained
unacknowledged, but healthy siblings were never processed.

- Impact: violated the accepted requirement that sibling transcripts fail independently.
- Minimum closure condition: isolate discovery failures per video, continue processing valid
  siblings, surface the malformed sibling, and withhold packet acknowledgement.
- Patch: extracted `_transcript_for_video`; `_transcripts_for_packet` now returns valid transcripts
  plus per-video discovery failures; `run_extraction` processes the valid siblings while keeping
  the packet incomplete; added a regression test covering the mixed valid/malformed batch.

## Considered And Defended

- Shared acknowledgement namespace does not cross-satisfy YouTube, Instagram, and TikTok because
  each obligation fingerprints a distinct consumer identity.
- JSON pointers use the original committed video-array index, not a filtered index.
- Manifest SHA-256 is a sufficient cheap immutable-packet obligation input because packet bodies
  are write-once and preserved-file hashes are carried by the manifest.
- Non-batch TikTok packets truthfully produce `no_extractable_transcripts` evidence.
- The timestamp parser consumes the canonical timestamp shape already emitted into admitted
  TikTok packets.

## Validation Evidence

Home-model fresh rerun after the delegated patch:

```text
python -m pytest -p no:cacheprovider --no-header --no-summary -q
  tests/unit/test_tiktok_product_extract.py
  tests/unit/test_transcript_product_extractor.py
  tests/unit/test_transcript_product_lake.py
  tests/contract/test_no_llm_imports.py
  tests/contract/test_catchup_runner_seam_coverage.py
  tests/contract/test_capture_runner_lake_seam_coverage.py
  tests/contract/test_data_lake_inventory_gate.py

Result: 106 passed, 0 failed.
```

Additional observed checks:

- `git diff --cached --check` — exit 0.
- `python .agents/hooks/check_retrieval_header.py --staged --strict` — exit 0.
- `python .agents/hooks/check_map_links.py --strict` — exit 0, 0 findings; 36 annotated
  nonresolving entries were reported as existing debt, not failures.
- Scratch TopFrag offline proof after adjudication — eight `extracted` statuses, eight injected
  transport calls, and an empty idempotent rerun.

## Home-Model Adjudication

- F-01: **accepted**. The finding is reproducible from the pre-patch control flow and directly
  contradicts the locked sibling-isolation behavior.
- Delegated patch: **accepted as written**. It stays within the commissioned files, preserves
  packet acknowledgement semantics, and adds a focused regression test.
- Reviewer validation count: superseded by the home-model fresh observation of 106 passing tests.
- Architecture escalation: not required.

## Residuals And Non-Claims

- Entity normalization quality remains unimplemented and unproven.
- The TopFrag proof used an injected offline transport returning empty mention arrays; it proves
  mechanics, lineage, record persistence, acknowledgement, and idempotency—not extraction recall.
- No live provider, live lake, capture, registry, SoV, Gold/Judgment, deployment, or readiness claim.
