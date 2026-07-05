# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Silver V3 Reader Gate + Vault Schema Tokens + Rank-Preservation Fixes (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the silver V3/V4 batch lane:
  the reader-selection contract gate (consumer-enumerated), the record-shape
  schema tokens closing the weak-envelope class (added WITHOUT bumping
  derivation-policy tokens), and the F-SSS-002 rank-preservation fixes found
  by the first live-lake probe (identical-content collapse and seed discovery
  dedupe both silently dropped a byte-identical catch-up record's supersession
  rank). Special stakes: GATE SOUNDNESS (could an undeclared reader or a
  regressed detector pass?), the NO-BUMP pin decision (is the additive-token
  claim true — no derived byte / ack fingerprint change for the same committed
  raw on the EXISTING derivation path?), and RANK-PRESERVATION completeness
  (any other layer that dedupes content before selection?).
use_when:
  - Dispatching the commissioned silver V3/V4 batch review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/silver-v3-gate-vault-tokens` (lane head), pinned commit
  `688f3771b7e25efbf977048f0985bbec2eeb578b`.
- Review target (the explicitly named multi-file set; the ONLY patchable
  surface; LF git blob bytes at the pinned commit):
  - `[gate]` `orca-harness/tests/contract/test_silver_reader_selection_gate.py` — SHA256 `cd029b0f0922a77f332e118c5730ea5bc27433348ce0d3bf39e899d02d514398`
  - `[inventory]` `orca-harness/data_lake/inventory.py` — SHA256 `042aafd16cd53138da78102ae8ef6b763eaf3ba6e4712e62ab7661f6c4bf2029` (patchable ONLY in the SILVER_READER_* additions; discovery internals flag-only)
  - `[rule]` `orca-harness/data_lake/sibling_selection.py` — SHA256 `deea256681992ddfeb6cc7f9fb54705ab03d2d5fa3a973264a01fd058e6f401d`
  - `[seed]` `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` — SHA256 `7921a74e7d7d2db7d6e642dba607dfc0fc3f4b5a72d2ce6a20f2e68fc27f00bd`
  - `[rule-tests]` `orca-harness/tests/unit/test_sibling_selection.py` — SHA256 `24581e4519ea919db8207383d4bb30539b972e8c8a1ce62de6545be69f92570e`
  - `[seed-tests]` `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py` — SHA256 `244c5e23d05076a33256014000a011e0d5e34b867d25b29828af2732366e5077`
  - `[asr-yt]` `orca-harness/source_capture/transcript/asr_packet.py` — SHA256 `4d99991d5b27c82b8c22981dcddaa2ebd516249cab706e1016ea9379c44bb21e` (patchable ONLY in the token constant + record field)
  - `[asr-ig]` `orca-harness/source_capture/transcript/ig_reels_audio_packet.py` — SHA256 `e28bafa6c049d42fb115c52518c6a11d2d666bed386f518964b402589585502a` (patchable ONLY in the token import + record field)
  - `[mentions]` `orca-harness/cleaning/transcript_product_lake.py` — SHA256 `5e26f61b50082dd214ae6f2fe756308607a06009c09c84b33f9c95be1f2fddf4` (patchable ONLY in the token constant + payload field)
  - `[frag-cov]` `orca-harness/source_capture/fragrance_review_coverage.py` — SHA256 `b98de11e2a67abe4fd75c048926ba2b3e95b3dddfc9446a20cdef93adb6a1bad` (patchable ONLY in the token constant + receipt model field)
  - `[gate-pins]` `orca-harness/tests/contract/test_policy_module_version_pins.py` — SHA256 `7042d893f543831a3e33a31e9642b70c8f099d1e9913ed96fb5b3b8501ac3c45`
- Read-only / flag-only everywhere else — notably the catch-up runners, the
  seam contract, `silver_metric_reader.py`, `lane_registry.py`, `root.py`, and
  the two prior adjudication records
  (`.../ig_reels_grid_projection_seam_catchup_...` and
  `.../silver_sibling_selection_helper_delegated_adversarial_code_review_v0.md`).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/contract/test_silver_reader_selection_gate.py
  orca-harness/tests/contract/test_policy_module_version_pins.py
  orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  orca-harness/tests/unit/test_sibling_selection.py
  orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
  orca-harness/tests/unit/test_asr_transcript_catchup.py
  orca-harness/tests/unit/test_fragrance_review_projection_catchup.py`
  plus the full suite when feasible (home-lane baseline at the pinned commit:
  2879 tests, 0 failures, 0 errors, 7 skipped, junitxml-verified with
  `ORCA_DATA_ROOT` cleared). Run what your runtime can; report real results
  either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/silver_v3_gate_vault_tokens_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch →
  home-CA adjudication (accept/modify/reject per change, class sweep +
  byte/scope checks) → keep decision.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/silver_v3_gate_vault_tokens_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/silver-v3-gate-vault-tokens; implementation committed at 688f3771)
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
undisclosable, reply ONLY `BLOCKED_DECORRELATION` and stop. Who-constraint
only, never a model recommendation. State your model identity and version in
your output if known and permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/silver-v3-gate-vault-tokens, pinned commit 688f3771b7e25efbf977048f0985bbec2eeb578b
- REVIEW TARGET: the eleven labeled files listed under "Pinned fields" in this
  prompt's artifact (docs/prompts/reviews/silver_v3_gate_vault_tokens_repo_
  delegated_adversarial_code_review_patch_commission_prompt_v0.md at the same
  commit), with the per-label patchable sub-scopes stated there. Every
  finding, diff hunk, and citation must carry the target's label. Confirm the
  LF blob hashes if you can, else confirm you read the files at the pinned
  commit and say so.
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: three moves of the silver read-layer hardening lane.
(1) [gate]/[inventory]: the V3 reader-selection contract gate — every
production file that walks derived lanes must declare its sibling-selection
posture in SILVER_READER_SELECTION_POSTURES; lane_dir readers detected
mechanically from tracked-source discovery, path-based/indirect walkers
hand-declared (a NAMED residual). (2) [asr-yt]/[asr-ig]/[mentions]/[frag-cov]/
[gate-pins]: record-shape schema tokens (record_schema_version) closing the
pinned weak-envelope class, added ADDITIVELY without bumping any
derivation-policy token (deliberate: a bump would re-derive whole lanes on the
next cadence and trigger the flagged sov_readout all-siblings over-count).
(3) [rule]/[seed]/[rule-tests]/[seed-tests]: F-SSS-002 — the first live-lake
probe found one packet with three distinct ULID derivations plus a rank-1
catch-up byte-identical to the newest; BOTH the rule's identical-content
collapse and the seed discovery's sha-dedupe kept the lexically smallest
ref/path and silently dropped the catch-up's supersession rank, resurrecting
the ambiguity the catch-up existed to resolve. Fixed at both layers; the
collapse representative now carries the group's max rank and newest instant,
and discovery dedupe prefers the highest-rank record-id class.

The failure modes that matter most:
- GATE SOUNDNESS (F-SH-001 lens): could a regressed lane_dir detector make
  lane_dir_reader_files() return a subset and still pass (verify the
  exact-match symmetry actually fails on both undeclared AND stale)? Could a
  new reader use record_path/is_record_set_complete WITHOUT lane_dir and walk
  siblings invisibly? Is the declared_free_walk hand-registry honest and
  complete against the unit (b) census? Are the 11 declared postures accurate
  against each file's actual selection code?
- NO-BUMP PIN DECISION: for each token addition, is the "additive, not
  output-shaping for the existing derivation path" claim true — does any
  catch-up obligation envelope, ack fingerprint, or record id change for the
  same committed raw? If any does, the pin decision is a finding.
- RANK-PRESERVATION COMPLETENESS: after F-SSS-002, is there ANY remaining
  layer that collapses/dedupes identical content before selection and keeps a
  representative WITHOUT max-rank/newest-instant carry? Check the collapse's
  instant carry too: identical content with differing parsed instants — can
  that state exist, and is max() right?
- MIXED-VINTAGE READS: tokens are absent on earlier committed records by
  design. Could any reader or test treat token absence as an error, or any
  new record be written WITHOUT the token through a path the edits missed
  (sweep the writers of the four lanes)?
- TEST ADEQUACY: could a regressed gate, collapse, or dedupe pass the suite?
- SCOPE DISCIPLINE: any change outside the named set or the per-label
  sub-scopes.

CONTRACTS AND SOURCES to judge against — read in the pinned repo (one-line
read disposition per source: full / targeted <section> / grep <token> /
skip: <reason>): data_lake/inventory.py discovery internals,
tests/contract/test_capture_runner_lake_seam_coverage.py,
runners/run_ig_reels_grid_projection_catchup.py and
runners/run_asr_transcript_catchup.py (envelope fingerprints the no-bump
claim must not move), docs/review-outputs/adversarial-artifact-reviews/
silver_sibling_selection_helper_delegated_adversarial_code_review_v0.md
(the prior adjudication incl. the same-rank fail-closed residual),
docs/decisions/silver_vault_goal_frame_ratification_v0.md (V3/V4 targets),
AGENTS.md (Smallest Complete Intervention + failure visibility).

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate every layer between committed
   records and each consumer where content dedupe, collapse, or
   representative-choice occurs; enumerate every writer of the four tokened
   lanes; map what the gate's detector can and cannot see.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding, along the failure modes above.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY
   (respect per-label sub-scopes); unified diff in chat, hunks labeled; run
   the named tests if your runtime can and report real results.
   Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only, NO diff.

RETURN, in order: (1) review_summary YAML + findings (label / severity /
file:line / issue / evidence with conflicting source path / impact /
minimum_closure_condition / next_authorized_action); (2) unified diff, hunks
labeled with per-change citations, neutral tone, decision-sufficient
substance; (3) verdict + residual-risk note — state explicitly whether any
finding means the gate could silently admit an undeclared reader, a token
addition re-surfaces committed packets, or a rank can still be silently
dropped; (4) real test results or an explicit not-run statement; (5) one-line
read-budget audit; (6) adjudicator tail: your diff, citations, verdict, and
test claims are claims to adjudicate — accept/modify/reject per change; the
CA may veto any change; nothing is kept until that adjudication, which closes
per the commissioning overlay's Review Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable
  (ChatGPT Pro per the owner's standing courier arrangement). The branch is
  pushed before dispatch.
- On return, courier the full output back for review-return adjudication.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
