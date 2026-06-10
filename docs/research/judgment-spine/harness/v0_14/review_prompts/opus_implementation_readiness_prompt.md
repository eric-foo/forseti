# Opus Implementation Readiness Review — Orca Judgement Harness v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness review prompt
scope: Imported Opus implementation-readiness prompt for the v0.14 code-ready docset.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


You are reviewing Orca v0.14 for **implementation readiness only**.

Do not relitigate strategy.

Assume these are frozen for Phase 1:

```yaml
frozen:
  - Orca is a judgement harness, not a trained model
  - action-band-first is the spine
  - mapping_table.py is the first code artifact
  - band input labels require a rubric and disagreement log
  - Phase 1 memory is failure-event logging only
  - no rule promotion in first 90 days
  - Phase 1 does not claim harness beats structured pipeline
```

Review whether the v0.14 docs are ready to code.

Focus on:

```yaml
review_focus:
  - mapping_table.py interface
  - band input labeling rubric completeness
  - facilitator ledger freeze fields
  - failure_event_log schema
  - repo structure
  - runner contracts
  - evidence checker scope
  - five plumbing cases
  - tests before coding further
```

End with:

```yaml
is_ready_to_code: yes | no | mixed
biggest_blocker:
single_patch_before_coding:
decision:
  - proceed_to_build
  - proceed_with_minor_patches
  - pause_and_patch_docs
```
