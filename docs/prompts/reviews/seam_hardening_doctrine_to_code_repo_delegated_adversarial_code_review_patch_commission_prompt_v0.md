# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Seam Hardening Doctrine-to-Code (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the seam hardening unit: the
  shared per-packet availability reconcile (single-sourced in
  data_lake/consumption.py, adopted by seven runners — including the YT/IG
  extract runners whose reconciles previously swallowed errors) and three new
  contract gates (consumer seam coverage; cleaning-family surface partition;
  policy-module version pins). The special stakes are REFACTOR FIDELITY
  (seven deletions of a thrice-reviewed pattern must be behavior-identical
  where tested and deliberately behavior-CHANGING only at the two YT/IG
  swallow sites) and GATE SOUNDNESS (a contract gate that can be trivially
  satisfied, or that mis-scans, converts doctrine into false confidence).
use_when:
  - Dispatching the commissioned seam-hardening review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/seam-hardening-doctrine-to-code` (stacked on
  `claude/fragrance-review-projection-seam-catchup`, PR #648), pinned commit
  `5c70537406984e854bc3620e1f7e9790c670d38f`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[helper]` `orca-harness/data_lake/consumption.py` — SHA256 `0af3c5b53fde350aba6e5eed2fbbce6d52cb16936c1f8d40c2b043abea44a5a4`
  - `[ecr]` `orca-harness/runners/run_ecr_catchup.py` — SHA256 `f843f428a3e15a1cedacabb6ad85f6a5533ba535a289e967101822158dca8b54`
  - `[frag]` `orca-harness/runners/run_fragrantica_cleaning_catchup.py` — SHA256 `9689d273b861cfe60b0268cbe083ac3b816fcddbf21142ab5bd0156ca90d49d8`
  - `[bn]` `orca-harness/runners/run_basenotes_cleaning_catchup.py` — SHA256 `3a03bb9544591b16762aae0e1774219e085cfb383673e399bcba3ac7a45d24c1`
  - `[pf]` `orca-harness/runners/run_parfumo_cleaning_catchup.py` — SHA256 `70f919071b3ae4ce1fad8cd8d5a7643dd58362436cc80b050a6bc666109d84cd`
  - `[frp]` `orca-harness/runners/run_fragrance_review_projection_catchup.py` — SHA256 `8053b6814a5de47bd8f40dd4e98fe7a98df27c61f146349d1eb8008ada9caaeb`
  - `[yt]` `orca-harness/runners/run_transcript_product_extract.py` — SHA256 `648dd204aeafb4d6021473c5243957c798a54daeb532ff08482f6b4feca43b79`
  - `[ig]` `orca-harness/runners/run_ig_reels_product_extract.py` — SHA256 `ace0c9e57a1de82d50b87c0e2e8936e0bf8d36ba6c39f11d419d4ba3f87994ef`
  - `[gate-consumer]` `orca-harness/tests/contract/test_catchup_runner_seam_coverage.py` — SHA256 `4a3204717b4a5f1b63d68b2bb4b1d3de2ad5e82b93472b17c1a4e74a62cf9c54`
  - `[gate-partition]` `orca-harness/tests/contract/test_cleaning_family_surface_partition.py` — SHA256 `fc023700a868dfdacf5a555dae16409f099ecdc99f0c689ceaade748fc939734`
  - `[gate-pins]` `orca-harness/tests/contract/test_policy_module_version_pins.py` — SHA256 `e1c54a507a74d4caddb8d3f2dace9f9621d66ee28328cc4d3ca33128fe784aa0`
- Read-only / flag-only everywhere else — notably `orca-harness/data_lake/root.py`
  (rebuild_availability / record_availability semantics the helper mirrors),
  `orca-harness/data_lake/inventory.py` (AST discovery utilities +
  NON_RAW_LAKE_TOUCHPOINT_CALLS: record_availability is untracked, so the
  touchpoint counter is unchanged by this move — if you believe that is wrong,
  SAY SO), `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  (the producer-side sibling gate), the affected test suites
  (`tests/unit/test_*_catchup.py`, `tests/unit/test_ig_reels_product_extract.py`,
  `tests/unit/test_transcript_product_extractor.py`), the 15 pinned policy
  modules named inside `[gate-pins]`, and
  `docs/review-outputs/adversarial-artifact-reviews/*_seam_catchup_*.md`
  (F-ECR-001 / F-FRAG-001 / F-FRAG-002 adjudications this unit mechanizes).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
  orca-harness/tests/contract/test_cleaning_family_surface_partition.py
  orca-harness/tests/contract/test_policy_module_version_pins.py
  orca-harness/tests/unit/test_ecr_catchup.py
  orca-harness/tests/unit/test_fragrantica_cleaning_catchup.py
  orca-harness/tests/unit/test_basenotes_cleaning_catchup.py
  orca-harness/tests/unit/test_parfumo_cleaning_catchup.py
  orca-harness/tests/unit/test_fragrance_review_projection_catchup.py
  orca-harness/tests/unit/test_ig_reels_product_extract.py
  orca-harness/tests/unit/test_transcript_product_extractor.py`
  plus the producer seam-coverage and inventory gate suites. Run them if your
  runtime can; report real results either way — never assert a pass that was
  not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/seam_hardening_doctrine_to_code_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/seam_hardening_doctrine_to_code_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/seam-hardening-doctrine-to-code; implementation committed at 5c705374)
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
- branch: claude/seam-hardening-doctrine-to-code (stacked on
  claude/fragrance-review-projection-seam-catchup), pinned commit
  5c70537406984e854bc3620e1f7e9790c670d38f
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [helper] orca-harness/data_lake/consumption.py
     (SHA256 0af3c5b53fde350aba6e5eed2fbbce6d52cb16936c1f8d40c2b043abea44a5a4)
  2. [ecr] orca-harness/runners/run_ecr_catchup.py
     (SHA256 f843f428a3e15a1cedacabb6ad85f6a5533ba535a289e967101822158dca8b54)
  3. [frag] orca-harness/runners/run_fragrantica_cleaning_catchup.py
     (SHA256 9689d273b861cfe60b0268cbe083ac3b816fcddbf21142ab5bd0156ca90d49d8)
  4. [bn] orca-harness/runners/run_basenotes_cleaning_catchup.py
     (SHA256 3a03bb9544591b16762aae0e1774219e085cfb383673e399bcba3ac7a45d24c1)
  5. [pf] orca-harness/runners/run_parfumo_cleaning_catchup.py
     (SHA256 70f919071b3ae4ce1fad8cd8d5a7643dd58362436cc80b050a6bc666109d84cd)
  6. [frp] orca-harness/runners/run_fragrance_review_projection_catchup.py
     (SHA256 8053b6814a5de47bd8f40dd4e98fe7a98df27c61f146349d1eb8008ada9caaeb)
  7. [yt] orca-harness/runners/run_transcript_product_extract.py
     (SHA256 648dd204aeafb4d6021473c5243957c798a54daeb532ff08482f6b4feca43b79)
  8. [ig] orca-harness/runners/run_ig_reels_product_extract.py
     (SHA256 ace0c9e57a1de82d50b87c0e2e8936e0bf8d36ba6c39f11d419d4ba3f87994ef)
  9. [gate-consumer] orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
     (SHA256 4a3204717b4a5f1b63d68b2bb4b1d3de2ad5e82b93472b17c1a4e74a62cf9c54)
  10. [gate-partition] orca-harness/tests/contract/test_cleaning_family_surface_partition.py
     (SHA256 fc023700a868dfdacf5a555dae16409f099ecdc99f0c689ceaade748fc939734)
  11. [gate-pins] orca-harness/tests/contract/test_policy_module_version_pins.py
     (SHA256 e1c54a507a74d4caddb8d3f2dace9f9621d66ee28328cc4d3ca33128fe784aa0)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the doctrine-to-code hardening of the consumption seam.
Until now, four conventions lived only in adjudication records a cold agent
had to read: the F-ECR-001 per-packet fail-visible availability reconcile
(previously seven runner-local copies, two of which — [yt] and [ig] — still
SWALLOWED reconcile failures with except-pass, hiding healthy packets because
the rebuild deletes index entries first); the consumer seam shape (by-key
pickup + append_ack, explicit reconcile choice, view-independence); the
F-FRAG-002 cleaning-family surface partition (previously verified by hand in
review); and the version-bump discipline for derivation-policy modules
(previously comment-bound). This unit single-sources the reconcile in
[helper], adopts it in all seven runners (behavior-identical where tested;
deliberately behavior-CHANGING at the [yt]/[ig] swallow sites: run loops now
emit availability_reconcile_failed statuses, IG's candidates channel carries
reconcile failures as (None, failure) entries, and IG's pending-count
scheduler gate raises loud), and adds three contract gates so the conventions
fail CI instead of needing an agent to remember them.

The failure modes that matter most:
- REFACTOR FIDELITY: is the shared helper byte-behavior-identical to the five
  deleted fail-visible copies (ordering, shard checks, error truncation,
  delete-then-rebuild)? Do the two YT/IG behavior CHANGES land exactly at the
  swallow sites and nowhere else — could any existing caller of the changed
  IG functions (_candidate_packet_ids signature change; pending count raising)
  break, double-count, or silently drop failures? Sweep ALL call sites.
- GATE SOUNDNESS (the deep stake — a gate that can be gamed is worse than
  doctrine): can [gate-consumer]'s AST scan be satisfied trivially (importing
  the helper without calling it; calling it but discarding failures; aliased
  imports it fails to see; a consumer that avoids importing
  data_lake.consumption entirely and hand-rolls acks)? Does [gate-partition]
  actually pin the partition, or could a lane change families and slip out of
  scope? Can [gate-pins] be satisfied by updating the pin without the version
  decision (yes by design — is the directed message strong enough, and are
  the 15 pinned modules the RIGHT set: anything missing whose internals shape
  derived output, anything pinned that is pure noise)?
- FAILURE-CHANNEL HONESTY: does every reconcile failure now reach a visible
  channel in all seven runners (statuses, candidates, loud raise), and does
  any path still exist where a reconcile failure yields a clean empty pickup?
- SCOPE DISCIPLINE: the helper lives in data_lake/consumption.py whose module
  contract says lane-side infrastructure over public surfaces — is the
  index-file deletion inside the helper a boundary violation that belongs on
  DataLakeRoot instead? (Flag with reasoning; a design-level answer is
  NEEDS_ARCHITECTURE_PASS, not a patch.)
- TEST ADEQUACY: no test exercises the shared helper's failure path through
  the YT/IG runners — the existing suites only cover the five catch-ups'
  behavior. Is a test-only patch warranted for the [yt]/[ig] reconcile
  failure surfacing?

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
- orca-harness/data_lake/root.py (rebuild_availability, record_availability,
  the write boundary; NOT patchable)
- orca-harness/data_lake/inventory.py (AST utilities + touchpoint tracking;
  NOT patchable)
- orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py (the
  producer-side sibling whose mechanics [gate-consumer] mirrors; NOT patchable)
- docs/review-outputs/adversarial-artifact-reviews/ecr_seam_catchup_delegated_adversarial_code_review_v0.md
  and the fragrantica / basenotes_parfumo / fragrance_review adjudications
  (the F-ECR-001 / F-FRAG-001 / F-FRAG-002 conventions this unit mechanizes)
- the affected unit suites: tests/unit/test_*_catchup.py,
  tests/unit/test_ig_reels_product_extract.py,
  tests/unit/test_transcript_product_extractor.py
- the 15 policy modules pinned in [gate-pins] (spot-check that pins match)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate every runner's reconcile call
   site and failure channel before and after this change; enumerate the ways
   each of the three gates could be gamed, mis-scan, or false-positive.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding, along the failure modes above. Severity labels are
   finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY closing
   your accepted-quality findings; unified diff in chat, each hunk prefixed
   with its label; run the named tests if your runtime can and report real
   results. Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only,
   NO diff.

RETURN, in order: (1) review_summary YAML + findings (label / severity /
file:line / issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks labeled and annotated with findings + per-change
citations, neutral tone, decision-sufficient substance; (3) verdict +
residual-risk note — state explicitly whether any finding means the new gates
give FALSE CONFIDENCE or the consolidated reconcile is less safe than the
copies it replaced; (4) real test results or an explicit not-run statement;
(5) one-line read-budget audit; (6) adjudicator tail: your diff, citations,
verdict, and test claims are claims to adjudicate — accept/modify/reject per
change; the CA may veto any change; nothing is kept until that adjudication,
which closes per the commissioning overlay's Review Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable.
- On return, courier the full output back for review-return adjudication; the
  CA adjudicates per labeled change and lands kept hunks in the same
  adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
