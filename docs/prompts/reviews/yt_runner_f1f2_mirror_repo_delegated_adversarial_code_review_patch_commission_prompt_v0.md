# Repo-Mode Delegated Adversarial Code Review + Patch Commission — YouTube Runner F1/F2 Mirror (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the YouTube-runner F1/F2
  mirror (unit (a) of the bronze-consumer shapes lane): the two defect
  classes the #637 adjudication's class sweep named in
  run_transcript_product_extract.py, mirrored from the adjudicated IG fix.
  Same delegated_code_review_and_patch sibling-mode pattern as the IG
  seam-migration commission; the special stake is MIRROR FIDELITY over a
  completion-fact surface — a divergence from the adjudicated semantics
  (raising transcript reads vs cheap non-raising obligation entries, rubric
  policy token) re-opens the exact fake-done class the mirror closes.
use_when:
  - Dispatching the commissioned YT-mirror code review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/yt-runner-f1f2-mirror` (lane head), pinned commit
  `9e2b56920b26a17112a23a2c8e4f9b0915b5e222`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface):
  - `orca-harness/runners/run_transcript_product_extract.py` — SHA256 `9d64730f68c234702453cb9e2cc6f25be594ca75bc92e0e76261457021587ad3`
  - `orca-harness/tests/unit/test_transcript_product_lake.py` — SHA256 `e8b7959c8379bd09dce32359c493d8f96f500fe29bb26c7aecd0e30df8e2ece8`
  (LF git blob bytes at the pinned commit.)
- Read-only / flag-only in the same change (flag, never patch):
  `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  (lane_dir count pin 1→2 for this runner),
  `orca-harness/data_lake/lake_touchpoint_inventory_v0.json` (regenerated,
  single count delta), and everything else — notably the IG runner/tests the
  mirror copies from and the adjudication record it executes.
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_transcript_product_lake.py
  orca-harness/tests/unit/test_youtube_caption_product_extract.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/yt_runner_f1f2_mirror_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch →
  home-CA adjudication (accept/modify/reject per change, class sweep +
  byte/scope checks) → keep decision. Repo-mode discovery discharges the
  independent-review gate for the patched set.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/yt_runner_f1f2_mirror_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/yt-runner-f1f2-mirror; implementation committed at 9e2b5692)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by artifact-folders overlay file and the in-repo commission pattern.
```

## Paste-ready commission body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT — gate yourself first: the review target was authored by an
Anthropic (Claude-family) model. This commission requires a DIFFERENT vendor /
model lineage (vendor = upstream model developer, not host/reseller/wrapper).
If you are Anthropic/Claude-lineage, or your lineage is unknown or
undisclosable, reply ONLY `BLOCKED_DECORRELATION` (plus your vendor if
permitted) and stop. Who-constraint only, never a model recommendation. State
your model identity and version in your output if known and permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/yt-runner-f1f2-mirror, pinned commit 9e2b56920b26a17112a23a2c8e4f9b0915b5e222
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing else):
  1. orca-harness/runners/run_transcript_product_extract.py
     (SHA256 9d64730f68c234702453cb9e2cc6f25be594ca75bc92e0e76261457021587ad3)
  2. orca-harness/tests/unit/test_transcript_product_lake.py
     (SHA256 e8b7959c8379bd09dce32359c493d8f96f500fe29bb26c7aecd0e30df8e2ece8)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the YouTube transcript product-extraction runner, already
on the consumption seam (ack namespace silver__cleaning__product_mentions,
consumer "transcript_product_extract"), now carrying the MIRROR of the two
defect-class fixes adjudicated for the IG runner in PR #637:
- F1: _asr_records previously caught (OSError, ValueError) with `continue`,
  so a damaged transcript_asr record was invisible to BOTH the obligation
  snapshot and the transcript scan — the packet could ack as transcript-less
  over damaged input (fake completion fact, silent forever). The mirror makes
  _asr_records raise (→ discovery_failed, no ack, re-surfaces every run) and
  adds _asr_record_obligation_entries, a CHEAP NON-RAISING snapshot feeder
  (an exception inside pickup's obligation_fn would abort the entire pickup
  loop; OSError becomes an unreadable:<type> marker entry).
- F2: _packet_obligation previously omitted the extractor rubric token; the
  mirror adds rubric_version (EXTRACTOR_RUBRIC_VERSION) so a rubric change
  re-surfaces acked packets for a re-check and re-ack under the new
  fingerprint WITHOUT re-running extraction (the deterministic mentions
  record id keys on model, not rubric — a Cleaning-owned decision this
  change must NOT smuggle in).
The failure mode that matters most is MIRROR INFIDELITY: any divergence from
the adjudicated IG semantics that re-opens the fake-done class, aborts pickup
on damaged input, silently changes the caption route, or lets the new tests
pass without pinning the behavior (a fake-pass-prone test is a finding).

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (minimum obligation envelope incl. policy tokens; pickup/ack/evidence rules)
- orca-harness/data_lake/consumption.py (the seam helper; note obligation_fn
  is called inline in pickup with NO per-item isolation)
- orca-harness/runners/run_ig_reels_product_extract.py and
  orca-harness/tests/unit/test_ig_reels_product_extract.py (the ADJUDICATED
  pattern this mirrors — divergences need a reason; NOT patchable)
- docs/review-outputs/adversarial-artifact-reviews/ig_reels_seam_migration_delegated_adversarial_code_review_v0.md
  (the adjudication record whose class sweep commissioned this mirror,
  including the F1/F2 verification notes and the accepted fingerprint-churn
  consequence; NOT patchable)
- orca-harness/cleaning/transcript_product_lake.py (mentions_record_id,
  record-set write shape the evidence refers to) and
  orca-harness/cleaning/transcript_product_extractor.py (EXTRACTOR_RUBRIC_VERSION)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the load-bearing behaviors of a
   seam consumer's obligation/read split and the ways a MIRROR of an
   adjudicated fix could diverge, under-pin, or over-reach.
2. MAXIMALLY ADVERSARIAL code review of the named set: mirror fidelity (does
   every F1/F2 semantic match the adjudicated IG shape, and is every
   divergence forced by a YT-specific reason — captions, extension-less
   record ids, consumer identity?); obligation safety (is the snapshot path
   provably non-raising for every input class — damaged JSON, OSError,
   non-file entries, missing lane dir? does it still include EVERY growable
   input?); ack honesty (can any path still ack over damaged input? does
   discovery_failed reliably block the ack? can the caption route regress?);
   fingerprint-churn consequence (is the accepted one-time re-surface of all
   previously acked YT packets correctly bounded — re-check + re-ack, never
   re-extraction? is anything conditioned on the OLD fingerprints?);
   cross-consumer safety (YT and IG share the ack namespace — does the
   consumer identity still isolate their obligations?); test adequacy (do the
   new tests actually pin the fixed behavior — could the pre-mirror code pass
   them? is the byte-unchanged rerun assertion sound given the availability
   index rebuild? is the rubric monkeypatch pinning the module binding the
   runner actually reads?); status-entry visibility (nothing swallowed that
   used to surface); scope discipline (nothing beyond the two files changed
   behaviorally; the count-pin and inventory deltas are flag-only surfaces).
   Severity labels are finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY closing
   your accepted-quality findings; unified diff in chat; run the named tests if
   your runtime can and report real results. Everything else — including the
   adjudication record and the IG pattern files — is READ-ONLY: flag, never
   patch. Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only, NO
   diff.

RETURN, in order: (1) review_summary YAML + findings (severity / file:line /
issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks annotated with findings + per-change citations,
neutral tone, decision-sufficient substance; (3) verdict + residual-risk note
— state explicitly whether any finding means acks already written by the
PRE-mirror YouTube code on a live lake would be untrustworthy (the home lane
holds that disposition as UNKNOWN pending an owner-gated live-lake read);
(4) real test results or an explicit not-run statement; (5) one-line
read-budget audit; (6) adjudicator tail: your diff, citations, verdict, and
test claims are claims to adjudicate — accept/modify/reject per change; the
CA may veto any change; nothing is kept until that adjudication, which closes
per the commissioning overlay's Review Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable.
- On return, courier the full output back for review-return adjudication; if a
  kept finding invalidates the mirror's ack semantics, the CA states whether
  any acks written on real data must be retracted (append-only retraction
  facts), and lands the patch in the same adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
