# Repo-Mode Delegated Adversarial Code Review + Patch Commission — ECR Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the ECR seam catch-up unit
  (g-ECR of the bronze-consumer shapes lane): the new catch-up runner that
  gives the ECR lane its own work discovery via the consumption seam, its
  S-signal test suite, the new ECR_DERIVER_VERSION policy token, plus the
  small IG OSError-half test follow-up riding the same lane. Same
  delegated_code_review_and_patch sibling-mode pattern as the IG/YT
  commissions; the special stake is a NOVEL OBLIGATION SHAPE — ECR's
  envelope has no per-packet input enumeration at all (constant per policy
  version), so a wrong analysis of ECR's true input surface would let a
  growable input class silently never re-trigger work.
use_when:
  - Dispatching the commissioned ECR catch-up code review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/ecr-seam-catchup` (lane head), pinned commit
  `d8fc756ce502cb4767f1fce1f6d1f2faab18c64c`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[ecr-runner]` `orca-harness/runners/run_ecr_catchup.py` — SHA256 `173d4bfabe52deb1391ad0fce54d83777125d7cf002b7df940b0b6ccc73915f9`
  - `[ecr-tests]` `orca-harness/tests/unit/test_ecr_catchup.py` — SHA256 `aea25ea8b95e4cde5afe0881e280f81916e2008e28ec2c88433062bde7f8e3e8`
  - `[ecr-policy-token]` `orca-harness/ecr/deriver.py` — SHA256 `b94920e25627537b1cca0503cad52130982de3f5d9a53122e14978912b27b273`
    (patch scope within this file: the ECR_DERIVER_VERSION constant and its
    comment ONLY; the four deriver functions are read-only — flag, never patch)
  - `[ig-osr-test]` `orca-harness/tests/unit/test_ig_reels_product_extract.py` — SHA256 `e229ec1ffe08b49a581c88f0c00b1e386850772d0a57c9f0f377fa5795917174`
    (patch scope within this file: the new
    test_runner_surfaces_unreadable_packet_asr_record_without_ack ONLY)
- Read-only / flag-only everywhere else — notably `orca-harness/ecr/lake.py`,
  `orca-harness/data_lake/consumption.py`, `orca-harness/data_lake/lane_registry.py`,
  the YT/IG extraction runners and their tests, the seam-coverage contract test,
  and `orca-harness/data_lake/lake_touchpoint_inventory_v0.json` (regenerated
  byte-identical in this change — if you believe it should have changed, SAY SO).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_ecr_catchup.py
  orca-harness/tests/test_ecr_lake_pilot.py
  orca-harness/tests/unit/test_ig_reels_product_extract.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/ecr_seam_catchup_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/ecr_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/ecr-seam-catchup; implementation committed at d8fc756c)
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
- branch: claude/ecr-seam-catchup, pinned commit d8fc756ce502cb4767f1fce1f6d1f2faab18c64c
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [ecr-runner] orca-harness/runners/run_ecr_catchup.py
     (SHA256 173d4bfabe52deb1391ad0fce54d83777125d7cf002b7df940b0b6ccc73915f9)
  2. [ecr-tests] orca-harness/tests/unit/test_ecr_catchup.py
     (SHA256 aea25ea8b95e4cde5afe0881e280f81916e2008e28ec2c88433062bde7f8e3e8)
  3. [ecr-policy-token] orca-harness/ecr/deriver.py — patchable ONLY at the
     ECR_DERIVER_VERSION constant + its comment; the deriver functions are
     read-only (flag, never patch)
     (SHA256 b94920e25627537b1cca0503cad52130982de3f5d9a53122e14978912b27b273)
  4. [ig-osr-test] orca-harness/tests/unit/test_ig_reels_product_extract.py —
     patchable ONLY at test_runner_surfaces_unreadable_packet_asr_record_without_ack
     (SHA256 e229ec1ffe08b49a581c88f0c00b1e386850772d0a57c9f0f377fa5795917174)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: (a) the NEW seam catch-up entrypoint for the ECR lane —
until this change, ECR record sets (four pure source-side postures + an
ecr_set completion marker, written all-or-nothing by ecr/lake.py) were
derived only when an operator pointed a command at ONE packet; the lane had
no discovery, so unpointed packets never got ECR records. The runner scans
committed availability via the consumption seam (ack namespace ecr_set,
consumer "ecr_catchup") and derives the sibling set for every packet whose
current obligation is unacknowledged. (b) A NOVEL OBLIGATION SHAPE: the
envelope is {obligation_schema, consumer, deriver_version} with NO per-packet
input enumeration — the design claim is that the raw packet is immutable and
the derivers are pure over its manifest with no derived-record inputs, so the
new ECR_DERIVER_VERSION policy token is the lane's ONLY re-trigger input.
(c) Skip-if-done keys on the ACK, never on existing ecr_set markers: a
pre-seam set carries no policy attribution, so an unacknowledged fingerprint
always derives a FRESH sibling set (stated consequence: the first live run
re-derives packets holding pre-seam sets once). (d) A small rider: the IG
OSError-half regression test mirroring the CA-adjudicated F-YT-001 test.

The failure modes that matter most: a WRONG INPUT-SURFACE CLAIM (is there any
growable input the constant obligation misses — a derived record the derivers
read, a manifest mutation path, a packet-content dependency outside the
manifest? if yes, obligation growth never re-surfaces the anchor and stale
derivations read as done forever); ACK HONESTY (can any path ack a packet
whose sibling set did not complete? does derive_failed reliably block the
ack? can an ack land under a non-committed anchor?); IDEMPOTENCE (is the
second run provably write-free? does the availability-index rebuild stay
byte-deterministic?); and TEST ADEQUACY (could a regressed runner pass these
tests — e.g. an ack written on derive failure, a policy bump that does not
re-derive, a partial sibling set acked as complete?).

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (minimum obligation envelope incl. the "every input class whose growth must
  re-surface the anchor MUST appear in the snapshot" rule; ack/evidence shape)
- orca-harness/data_lake/consumption.py (the seam helper; obligation_fn is
  called inline in pickup with NO per-item isolation)
- orca-harness/ecr/lake.py + orca-harness/ecr/deriver.py + orca-harness/tests/test_ecr_lake_pilot.py
  (the persistence adapter, the four pure derivers, and the record-set
  semantics the runner builds on — verify the purity/immutability claims the
  obligation design rests on)
- orca-harness/runners/run_ig_reels_product_extract.py and
  orca-harness/runners/run_transcript_product_extract.py (the two adjudicated
  seam-consumer patterns — divergences from them need a reason; NOT patchable)
- docs/review-outputs/adversarial-artifact-reviews/ig_reels_seam_migration_delegated_adversarial_code_review_v0.md
  and the F-YT-001 record on the claude/yt-runner-f1f2-mirror lane if
  reachable (the adjudication history this lane executes; NOT patchable)
- orca-harness/data_lake/lane_registry.py (ecr_set registration; NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate ECR's true input surface from
   the derivers' source (what do they actually read?), then the ways a
   constant-per-policy obligation, an ack-keyed skip, or the catch-up loop
   could fake done-ness, lose failure visibility, or violate the seam contract.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding: input-surface completeness ([ecr-runner]/[ecr-policy-token]: is
   deriver_version genuinely the only re-trigger input? is the version-bump
   discipline — a comment-only contract — adequate, and if not, what is the
   smallest hardening?); ack honesty and evidence sufficiency ([ecr-runner]:
   record_set_complete evidence citing the just-written set — can a crash
   between append_record_set and append_ack strand states the next run
   handles wrongly?); idempotence and byte-unchanged reruns ([ecr-tests]: is
   the tree-hash assertion sound given the availability rebuild?); per-packet
   isolation and typed failures; namespace/boundary discipline (ecr_set as
   ack namespace — any confusion risk with the record-set completion lane of
   the same name?); CLI exit semantics; the [ig-osr-test] rider's fidelity to
   the adjudicated YT shape; scope discipline. Severity labels are
   finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY (within
   the per-file bounds above) closing your accepted-quality findings; unified
   diff in chat, each hunk prefixed with its label; run the named tests if
   your runtime can and report real results. Design-level problem →
   `NEEDS_ARCHITECTURE_PASS`, findings only, NO diff.

RETURN, in order: (1) review_summary YAML + findings (label / severity /
file:line / issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks labeled and annotated with findings + per-change
citations, neutral tone, decision-sufficient substance; (3) verdict +
residual-risk note — state explicitly whether any finding means acks this
runner would write are untrustworthy, and whether the first-live-run
re-derivation consequence is correctly bounded; (4) real test results or an
explicit not-run statement; (5) one-line read-budget audit; (6) adjudicator
tail: your diff, citations, verdict, and test claims are claims to
adjudicate — accept/modify/reject per change; the CA may veto any change;
nothing is kept until that adjudication, which closes per the commissioning
overlay's Review Adjudication Next Step.

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
