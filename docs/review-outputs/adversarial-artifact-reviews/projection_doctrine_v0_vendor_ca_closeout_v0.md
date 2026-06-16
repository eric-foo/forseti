# Projection Doctrine v0 Vendor-CA Closeout

```yaml
retrieval_header_version: 1
artifact_role: Vendor-CA closeout for a product architecture draft
scope: >
  Bounded closure check of the folded-in Projection Doctrine v0 review findings,
  keep decision, and residual owner decisions. This is decision input, not
  validation, readiness, ratification, buyer proof, or implementation authority.
use_when:
  - Checking why Projection Doctrine v0 is marked kept by the vendor CA.
  - Verifying which review findings were closed before using the doctrine as a candidate view contract.
  - Separating projection doctrine keep from owner decisions OD-1, OD-4, and OD-7.
authority_boundary: retrieval_only
```

```yaml
ca_closeout:
  reviewed_by: openai/gpt-5-codex
  authored_by: claude-opus-4.8
  de_correlation_bar: cross_vendor_discovery
  reviewer_ca_correlation: "same vendor/model family performed discovery review and CA closeout; owner accepted this boundary"
  hash_confirmed: true
  hash_evidence:
    review_object_commit_before_ca_closeout: "ed4d3472"
    review_object_path: "docs/product/core_spine_v0_projection_doctrine_v0.md"
    expected_sha256_lf: "dda5eeb60750c66782733ae36a2ede43f151b089dfa7f7d8ffb77a21b9696d85"
    observed_sha256_lf_from_git_blob: "dda5eeb60750c66782733ae36a2ede43f151b089dfa7f7d8ffb77a21b9696d85"
    expected_git_blob_prefix: "89c91417"
    observed_review_object_git_blob: "89c91417ac09bb8f6f0b3691e3b1536436f243ae"
    current_doctrine_blob_after_status_update: "33c9c85e62c0f5e1cefa967c906906c013ef49d5"
    note: "Hash confirmation applies to the pre-closeout review object. The current doctrine file has a later status/closeout-reference amendment, so its blob is expected to differ."
  closure:
    - id: F1
      verdict: closed
      where: "§1, §2, §4, §11"
      note: "Projected Unit is framed as a non-canonical working name for the existing Data Capture Projection Packet view; object/schema questions are OD-1/OD-7-gated."
    - id: F2
      verdict: closed
      where: "§3, §5, §9"
      note: "Collapse is frame-conditional, logged, raw-anchored, and forbidden when it removes evidence rows or bindings."
    - id: F3
      verdict: closed
      where: "§3, §9"
      note: "Projection carries raw counts, labels, timestamps, captions, and baseline facts; anomaly/call-record style interpretation is kept out."
    - id: F4
      verdict: closed
      where: "§7"
      note: "Cleaning inclusion-state is narrowed to mechanical status tokens; discount/exclude/strength/action-support reasons are Judgment-authored only."
    - id: F5
      verdict: closed
      where: "§8"
      note: "Raw pull-in separates triggering claim type from minimum Action-Ceiling and uses closed IPF rungs."
    - id: F6
      verdict: closed
      where: "§4, §6"
      note: "Loss ledger anchors are modality-appropriate and may use byte range, DOM path, screenshot region, timestamp, frame hash, rendered span, or named residual."
    - id: fitness
      verdict: closed
      where: "§3 Rule 10, §9"
      note: "Salience is frame-bound, carried, or residualized; projection may not make compactness decisions by judging importance."
  new_blocker_major_in_touched_delta: "none"
  keep_decision: keep
  required_amendments: []
  kept:
    - "Projection Doctrine v0 as a candidate view contract for owner confirmation."
    - "The rule that projection is a Data-Capture-owned mechanical view over raw, not a new spine layer and not Cleaning or Judgment."
  residual_risk: >
    OD-1 pipeline ordering, OD-4 dedupe/clustering ownership, and OD-7 naming remain
    owner architecture decisions. This closeout cannot catch the discovery reviewer's
    own blind spots as well as a third independent vendor would; a third-party pass is
    optional if the owner wants more de-correlation before ratification.
```

**Status**

The vendor CA keeps Projection Doctrine v0 as a candidate doctrine for owner
confirmation. The keep means the six review findings and the fitness attack have
adequate folded-in closure in the persisted artifact; it does not mean the doctrine is
validated, ratified, buyer-proof, Judgment-quality, or implementation-ready.

**What To Do Next**

Use the doctrine to constrain source-lane projection work: raw remains canonical,
projected views stay traceable and view-only, and Judgment must pull raw for the named
trigger classes. Owner decisions OD-1, OD-4, and OD-7 still need explicit architecture
adjudication before the candidate shape becomes a general object model or durable
pipeline ordering.
