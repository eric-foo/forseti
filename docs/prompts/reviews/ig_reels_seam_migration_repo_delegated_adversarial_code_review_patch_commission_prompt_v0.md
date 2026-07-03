# Repo-Mode Delegated Adversarial Code Review + Patch Commission — IG Reels Seam Migration (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the IG-reels seam migration
  (the IG product-extraction runner's packet route moved onto the consumption
  seam + its tests), dispatched to an external GPT-family controller WITH
  repository read access. Same delegated_code_review_and_patch sibling-mode
  pattern as the SoV view-build and eval commissions; the special stake here
  is completion-fact honesty — a consumer that acks without real completion
  evidence, or whose obligation snapshot misses a growable input, silently
  fakes done-ness for every future run.
use_when:
  - Dispatching the commissioned IG seam-migration code review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/ig-reels-seam-migration` (PR head), pinned commit
  `7c216b18abf83900c926634fbbf688de658ca439`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface):
  - `orca-harness/runners/run_ig_reels_product_extract.py` — SHA256 `B5C0DE1BEF75CB501BE704ABBB0334293E1627D0231B86A063E5554A0AD16009`
  - `orca-harness/tests/unit/test_ig_reels_product_extract.py` — SHA256 `8AB90F643CD1673FACDB733112AC97897E1E048FAB3B502C60C823C5878C4099`
  (LF git blob bytes at the pinned commit.)
- Read-only / flag-only in the same change (flag, never patch):
  `docs/workflows/ig_reels_deep_capture_anchoring_decision_input_v0.md` (the
  owner decision this unit prepares — if the code contradicts what it states,
  SAY SO), `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`,
  `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`.
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_ig_reels_product_extract.py
  orca-harness/tests/unit/test_ig_reels_operator_product_extract.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/ig_reels_seam_migration_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/ig_reels_seam_migration_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/ig-reels-seam-migration; implementation committed at 7c216b18)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by artifact-folders overlay file.
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
- branch: claude/ig-reels-seam-migration, pinned commit 7c216b18abf83900c926634fbbf688de658ca439
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing else):
  1. orca-harness/runners/run_ig_reels_product_extract.py
     (SHA256 B5C0DE1BEF75CB501BE704ABBB0334293E1627D0231B86A063E5554A0AD16009)
  2. orca-harness/tests/unit/test_ig_reels_product_extract.py
     (SHA256 8AB90F643CD1673FACDB733112AC97897E1E048FAB3B502C60C823C5878C4099)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the IG-reels product-extraction runner freshly migrated
onto the data lake's consumption seam. Its packet-backed route now discovers
work via obligation-fingerprint pickup over committed instagram_creator
availability and writes append-only completion acks (namespace
silver__cleaning__product_mentions, consumer "ig_reels_product_extract");
its deep-capture route is DELIBERATELY out of the seam (shortcode anchors
with no committed bronze packet — an owner decision is prepared, not
executed). The failure mode that matters most is a FAKE COMPLETION FACT:
an ack written while a transcript failed or is partial, an obligation
snapshot that omits a growable input (so a late-arriving input never
re-surfaces the packet), a fingerprint that a DIFFERENT consumer (the
YouTube runner shares the ack namespace) could satisfy or clobber, a
swallowed per-item failure, or an ack sneaking under a non-committed
deep-capture anchor. A wrong ack is silent forever — every future run
skips the packet.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (pickup/ack/evidence/conformance rules the runner must obey)
- orca-harness/data_lake/consumption.py (the seam helper the runner consumes)
- orca-harness/runners/run_transcript_product_extract.py (the YouTube
  migration PATTERN this mirrors — divergences need a reason; NOT patchable)
- orca-harness/source_capture/ig_reels_deep_capture_lake.py (why the
  deep-capture route is out-of-seam; NOT patchable)
- orca-harness/runners/run_ig_reels_operator_product_extract.py (imports
  discover_transcript_candidates/_mentions_set_state/_result_identity from
  the target — its couplings must survive; NOT patchable)
- orca-harness/cleaning/transcript_product_lake.py (mentions_record_id,
  record-set write shape the evidence refers to)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the seam consumer's load-bearing
   behaviors and the ways this migration could fake done-ness, lose failure
   visibility, or violate the seam contract.
2. MAXIMALLY ADVERSARIAL code review of the named set: ack honesty (can any
   path ack a packet whose transcripts did not all complete? is the
   no_extractable_transcripts evidence ever used to paper over a real
   failure?); obligation completeness (does the snapshot include EVERY
   growable input class of the packet route — what about a late ASR record,
   a model change, a new surface?); cross-consumer safety (YT and IG share
   the ack namespace — can either satisfy, block, or clobber the other's
   obligations?); reconcile discipline (the visible reconcile opt-out — is
   the self-reconcile equivalent to the contract's requirement?); the
   deep-capture boundary (still failure-isolated, still never acked, no
   silent behavior change to the marker-based route or the counts/CLI);
   status-entry visibility (nothing swallowed that used to surface); test
   adequacy (can the implementation regress without a test failing — e.g.
   ack-without-evidence, obligation missing asr_records, deep-capture acks?);
   scope discipline. Severity labels are finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY closing
   your accepted-quality findings; unified diff in chat; run the named tests if
   your runtime can and report real results. Everything else — including the
   decision-input doc — is READ-ONLY: flag, never patch. Design-level
   problem → `NEEDS_ARCHITECTURE_PASS`, findings only, NO diff.

RETURN, in order: (1) review_summary YAML + findings (severity / file:line /
issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks annotated with findings + per-change citations,
neutral tone, decision-sufficient substance; (3) verdict + residual-risk note
— state explicitly whether any finding means acks already written by this
code would be untrustworthy; (4) real test results or an explicit not-run
statement; (5) one-line read-budget audit; (6) adjudicator tail: your diff,
citations, verdict, and test claims are claims to adjudicate — accept/modify/
reject per change; the CA may veto any change; nothing is kept until that
adjudication.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable.
- On return, courier the full output back for review-return adjudication; if a
  kept finding invalidates the ack semantics, the CA states whether any acks
  written on real data must be retracted (append-only retraction facts), and
  lands the patch in the same adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
