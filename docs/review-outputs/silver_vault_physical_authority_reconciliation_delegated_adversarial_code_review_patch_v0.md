# Silver Vault Physical-Authority Reconciliation Delegated Adversarial Code Review-And-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review output (review-report)
scope: >
  Independent cross-vendor review of the completed Silver Vault physical-authority
  reconciliation diff on codex/silver-vault-mgt-reconciliation, with bounded patch
  authority over the commissioned file set. Findings are decision input for Chief
  Architect adjudication; no patch was kept.
use_when:
  - Adjudicating the codex/silver-vault-mgt-reconciliation implementation diff before fused closeout.
  - Checking what the repository does and does not prove about the new Silver physical source gate.
stale_if:
  - The branch head advances past the reviewed dispatch HEAD.
  - A later commission supersedes this review route.
authority_boundary: retrieval_only
```

## Review Identity And Provenance

```yaml
review_identity:
  reviewed_by: claude-opus-4-8 (Anthropic)
  authored_by: OpenAI GPT-5 Codex
  de_correlation_status: satisfied
  de_correlation_bar: cross_vendor_discovery
  de_correlation_basis: >
    Author vendor OpenAI; controller vendor Anthropic. Vendors differ, so the
    cross-vendor discovery bar is met. Who-constraint only; not a model
    recommendation or ranking.
  commission: docs/prompts/reviews/silver_vault_physical_authority_reconciliation_delegated_adversarial_code_review_patch_prompt_v0.md
  target_kind: delegated_code_review_and_patch
  review_lane: workflow-code-review
  access: repo
  dispatch_mode: external-controller-courier
  current_receiving_actor_role: controller
  review_routing_status: routed

target_state:
  workspace_or_repo: C:\Users\vmon7\Desktop\projects\forseti-worktrees\1b40\orca
  launch_checkout: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\silver-vault-authority-reconciliation-8fab68
  effective_target_worktree: C:\Users\vmon7\Desktop\projects\forseti-worktrees\1b40\orca
  target_resolution_method: >
    launch_checkout != commissioned target, so registered worktrees were
    enumerated via `git worktree list --porcelain`; exactly one worktree holds
    branch codex/silver-vault-mgt-reconciliation.
  branch: codex/silver-vault-mgt-reconciliation
  review_base_exact: d790ac11a192144f684e3c3300d4e9c82901f083
  dispatch_head_exact: 21317aa9b1b005925eb75503652ae79d20144242
  ancestry_verified: yes (`git merge-base --is-ancestor` exit 0)
  initial_dirty_state: clean (`git status --porcelain` empty)
  final_dirty_state: clean (`git status --porcelain` empty)
  direct_write_capability_proof: >
    Target-rooted file write + read-back, then `git add -N` exit 0 showing
    `A controller_write_probe_check`, then reset and removal; tree returned to
    clean. (A first probe using a .tmp suffix was gitignored and did not prove
    index write; it was rerun with a non-ignored path.)
  no_concurrent_writer_status: >
    confirmed at preflight (no *.lock under the worktree git dir; no
    MERGE_HEAD / REBASE_HEAD / CHERRY_PICK_HEAD / BISECT_LOG) and rechecked
    immediately before the first edit (branch, HEAD, and clean tree unchanged).
  target_drift_during_review: none
  scope_verification: >
    47 changed paths base..HEAD == the 46 commissioned targets + the commission
    prompt itself (read-only, excluded from patch scope).
  controller_created_scratch: none remaining
```

## Verdict

```yaml
overall_verdict: findings_returned_no_patch_kept
patch_count: 0
findings: 8   # 0 critical, 2 major, 6 minor
considered_and_defended_count: 7
validation: all bound gates pass at the as-authored dispatch HEAD
non_claims:
  - not a production-readiness claim
  - not a Mini God Tier claim
  - not validation acceptance; the CA adjudicates these findings as claims
  - not a claim that any real (private-lake) Silver record resolves under the new gate
```

The commissioned behavior is, in the main, implemented as specified and the
repository proves it at the level the repository can. Both Silver write front
doors verify sources before persistence; record-set validation is genuinely
all-before-any; the census, the exact-policy mention selector, and the
behavioral reader all route through the same root-aware physical verifier; the
three source-less capture lanes are retired with the old writer failing visibly;
and only `by_mention` and `undone` move to the Silver Vault-owned home with
`by_creator` still deferred.

The two material findings are both about the **gap between what the gate claims
to check and what it actually checks**, not about a bypass. No finding
demonstrates a route by which a malformed envelope or an unresolved/tampered
source obtains Silver authority. Sub-verdicts differ materially by label and are
given below.

### Per-label sub-verdicts

| Label | Sub-verdict |
|---|---|
| `[authority-gate]` | Sound against the named attacks; `hash_basis` is carried but never interpreted (FIND-01), and validation/verification disagree on a derived ref's `sha256` (FIND-03). |
| `[producer-refs]` | Correct; residue only — three ref-kind constants are now dead (FIND-04). |
| `[legacy-retirement]` | Meets the commissioned behavior. Whole writer body is unreachable by design (FIND-05). |
| `[retrieval-home]` | Correct and DCP-compliant. One blind `rmtree` of a no-longer-owned tree (FIND-06). |
| `[proof-tests]` | Pass, but the YouTube 196-record proof runs against fabricated sources (FIND-02). This is the weakest label. |

## Findings

Coverage-first: every issue found is listed, including low-confidence and minor
ones. Severity and confidence are priority labels, not reporting thresholds.

### FIND-01 `[authority-gate]` — `hash_basis` is required to be present but is never interpreted

- **severity**: major · **confidence**: medium
- **location**: `forseti-harness/data_lake/silver_record.py:167-179` (validation),
  `:237-274` (`_verify_raw_packet_ref`), `:277-318` (`_verify_attachment_record_ref`)
- **evidence**: `_validate_lineage_refs` enforces only that `sha256` and
  `hash_basis` travel together; it never constrains the basis *value*.
  `_verify_raw_packet_ref` then always interprets the digest as a preserved
  file's **raw stored bytes** hash — matching `preserved_files[].sha256` when
  `file_id` is absent, or hashing `loaded.bodies[file_id]` when present —
  regardless of the declared basis. `hash_basis` is read nowhere in the verifier.
  The same field carries values from two incompatible vocabularies: the Bronze
  Attachment-Record path copies the AR's basis (`"raw_stored_bytes"`, asserted at
  `tests/unit/test_youtube_creator_metric_silver_producer.py:353`), while the
  raw-packet fallback path restricts the basis to
  `source_captured_watch_html_sha256` / `source_captured_selective_payload_sha256`
  (`youtube_silver_metric_producer.py:520-527`) — neither of which names raw
  stored bytes. The new fixtures demonstrate the field is already incoherent:
  `tests/unit/_creator_metric_silver_fixtures.py:91-94` and
  `tests/unit/test_youtube_creator_metric_silver_producer.py:264-268` declare
  `source_captured_selective_payload_sha256` on a digest that is in fact the raw
  stored bytes hash of a synthetic body, and the gate accepts the pair.
- **impact**: the contract's hash-basis coupling cannot detect a producer that
  mislabels or silently changes its hash basis. The gate's real invariant is
  "digest == raw stored bytes", which is narrower than what the field claims to
  express. Fail-closed, not a bypass: a digest genuinely computed on a different
  basis is rejected rather than misaccepted — but it is rejected for the wrong
  stated reason, and the label carries no enforcement weight.
- **minimum_closure_condition**: the raw-ref `hash_basis` vocabulary and the
  verifier's interpretation are reconciled — either the verifier resolves each
  declared basis, or the field is constrained to the bases the verifier actually
  checks — and no fixture declares a basis that contradicts the digest it carries.
- **next_authorized_action**: `NEEDS_ARCHITECTURE_PASS`. Closing this requires
  deciding the basis vocabulary and per-basis resolution semantics across the
  Bronze-AR and raw-packet paths; that is design-level and outside a bounded patch.

### FIND-02 `[proof-tests]` — the 196-observation YouTube proof runs against fabricated sources, not the branch the real seed takes

- **severity**: major · **confidence**: high
- **location**: `forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py:226-272`
  (`_materialize_seed_sources`), `:44` (`EXPECTED_OBSERVATIONS = 196`);
  `forseti-harness/tests/unit/_creator_metric_silver_fixtures.py:68-98`
- **evidence**: `_materialize_seed_sources` fabricates one raw packet per
  `source_packet_id_or_none` whose entire preserved body is
  `{"packet_id": "<id>"}`, rebinds each observation's `source_evidence_sha256` to
  that stub's hash, and sets `source_watch_html_sha256_or_none = None`. The
  committed seed
  (`forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`)
  carries **empty** `source_evidence_sha256` and `source_evidence_hash_basis` for
  all 196 observations and a **populated** `source_watch_html_sha256_or_none`
  (verified by direct inspection: 196/196 have a blank basis). The real path
  therefore takes the watch-html fallback branch
  (`youtube_silver_metric_producer.py:517-519`) — the exact branch the test
  disables by nulling that field. No test exercises the watch-html basis branch
  through `verify_silver_vault_record_sources`.
- **impact**: the suite establishes that the producer emits 196 gate-passing
  records **when the sources are synthesized to match the digests**, not that any
  real YouTube observation resolves under the new physical gate. The stub bodies
  contain none of the actual evidence. The private lake is unavailable in-repo,
  so this cannot be closed here.
- **not a false claim**: the fixture docstrings are explicit that only provenance
  is rebound, and `docs/decisions/silver_vault_legacy_record_convergence_v0.md`
  correctly records `not recovery of unavailable records`. This is a coverage
  boundary to name, not a misrepresentation to correct.
- **minimum_closure_condition**: the not-proven boundary is explicit on the
  durable record, and/or a test exercises the watch-html basis branch end-to-end
  through the physical verifier.
- **next_authorized_action**: owner decision. A watch-html-branch test is
  reachable in scope (`_commit_youtube_watch_packet` already exists) but a
  faithful fixture depends on resolving FIND-01 first.

### FIND-03 `[authority-gate]` — validation and verification disagree on what a derived ref's `sha256` means

- **severity**: minor · **confidence**: high
- **location**: `forseti-harness/data_lake/silver_record.py:195-196` vs `:332-339`
- **evidence**: `_validate_lineage_refs` treats `sha256` as an *alias for
  `content_hash`* (`digest = ref.get("content_hash", ref.get("sha256"))`, and
  likewise `hash_basis` for `content_hash_basis`). `_verify_derived_ref` treats
  `sha256` as the derived record's **raw file bytes** hash and `content_hash` as
  the **canonical content** hash — two different values for the same record.
- **impact**: a derived ref carrying `sha256` with the meaning validation
  explicitly permits (content hash) would be rejected as tampered. Latent only:
  every current producer emits `content_hash`
  (`cleaning/*_lake.py`, both metric producers), so no live path hits it.
- **minimum_closure_condition**: validation and verification agree on what a
  derived ref's `sha256` denotes, or the alias is removed.
- **next_authorized_action**: flag; closure requires deciding the alias semantics.

### FIND-04 `[producer-refs]` — dead ref-kind constants left by the `raw_ref_kind` → `ref_type` migration

- **severity**: minor · **confidence**: high
- **location**: `silver_metric_producer.py:95`,
  `youtube_silver_metric_producer.py:138-139`
- **evidence**: `_RAW_PACKET_FALLBACK_REF_KIND`,
  `_RAW_PACKET_FALLBACK_MISSING_AR_REF_KIND`, and
  `_RAW_PACKET_FALLBACK_AMBIGUOUS_AR_REF_KIND` are defined but unreferenced
  repo-wide (grep returns definitions only). The missing-vs-ambiguous
  Attachment-Record distinction they encoded now survives only via
  `typed_attachment_record_status`, which the verifier does not read.
- **impact**: dead code; no behavior change. The `raw_ref_kind` field name itself
  survives only in historical docs/review outputs, which correctly remain lane records.
- **minimum_closure_condition**: the three constants are removed or referenced.
- **next_authorized_action**: optional hardening, non-required.

### FIND-05 `[legacy-retirement]` — the retired writer's entire body is unreachable

- **severity**: minor · **confidence**: high
- **location**: `forseti-harness/source_capture/ig_reels_deep_capture_lake.py:106-115`
- **evidence**: `write_reel_deep_capture_into_lake` raises
  `ValueError("eligible_bronze_required: ...")` before roughly 100 lines of
  retained construction logic, declared intentional by an inline comment
  ("Historical construction logic is intentionally retained below for audit
  readability"). The module helpers `_media_provenance`,
  `_transient_media_redactions`, and `_redact_transient_media` are now reachable
  only from that dead body, and their tests were removed (7 → 3 test functions in
  `tests/unit/test_ig_reels_deep_capture_lake.py`).
- **impact**: none at runtime — the fail-closed gate is correct and visible. Git
  history already preserves the logic, so "retained for audit readability" buys
  little against the cost of unreachable code that static analysis flags and that
  no test now covers.
- **minimum_closure_condition**: owner decides whether the unreachable body stays.
- **next_authorized_action**: optional; owner decision.

### FIND-06 `[retrieval-home]` — rebuild blindly `rmtree`s a tree it no longer owns

- **severity**: minor · **confidence**: medium
- **location**: `forseti-harness/data_lake/derived_retrieval_views.py:249-251`
- **evidence**: `rebuild_derived_retrieval` unconditionally
  `shutil.rmtree`s `indexes/derived_retrieval/object_level` — a path this module
  no longer owns or writes — with no ownership or manifest check, and the removal
  is not disclosed in the returned dict (`status`, `views`, `deferred_views`,
  `generation_id`, `file_count`). Under the previous code that tree *was* this
  module's own output, so the blast radius has widened in meaning even though the
  call is textually similar.
- **impact**: anything else ever written under `object_level` is destroyed by a
  routine, repeatable rebuild. Contained: the tree is rebuildable-tier by
  contract, so this is recoverable rather than authority loss. Note the owned-view
  replacement below it is correctly surgical (per-view `unlink`, not a wipe),
  which is what preserves a deferred `by_creator` — so the wide `rmtree` is
  inconsistent with the care taken two lines later.
- **minimum_closure_condition**: the legacy-home removal is either scoped to the
  files this module previously emitted, or disclosed in the rebuild result.
- **next_authorized_action**: flag.

### FIND-07 `[authority-gate]` — every record's envelope is validated twice

- **severity**: minor · **confidence**: high
- **location**: `forseti-harness/data_lake/silver_record.py:217`
- **evidence**: `verify_silver_vault_record_sources` re-runs
  `validate_silver_vault_record(record)` although all four call sites validate
  immediately before calling it: `append_silver_record:602-604`,
  `append_silver_record_set:627-630`, `silver_census.py:646-654`, and
  `product_mention_selection.py:160-178`.
- **impact**: correctness-neutral and defensively reasonable for a public
  function, but it doubles envelope validation — including a full canonical-JSON
  re-serialization and SHA-256 re-hash — on every record on every path.
- **minimum_closure_condition**: the redundancy is removed or accepted as a
  deliberate public-entry-point guard.
- **next_authorized_action**: optional; non-required.

### FIND-08 `[authority-gate]` — census physical verification is O(records × packet bytes) with no caching

- **severity**: minor · **confidence**: medium · **runtime cost: not proven**
- **location**: `forseti-harness/data_lake/silver_census.py:653-664`;
  `forseti-harness/data_lake/root.py:813-899` (`load_raw_packet`)
- **evidence**: the census now calls `verify_silver_vault_record_sources` for
  every valid Silver record. Each raw-packet ref calls `load_raw_packet`, which
  re-reads and re-hashes **every** preserved file in that packet (not only the
  referenced one), and nothing caches loaded packets across records. Records
  sharing a packet each pay the full packet re-hash — e.g. 196 metric
  observations over a shared watch packet re-hash it 196 times.
- **impact**: the census was previously an envelope-only read-side build; it is
  now hash-bound on total packet bytes. On a large lake with heavy HTML packets
  this may be a substantial regression. **Not proven**: no live-lake measurement
  was taken (the commission forbids inspecting the live lake), and the temp-lake
  test packets are too small to reveal it.
- **minimum_closure_condition**: census verification cost is measured on a
  representative lake, or a per-packet cache is introduced, or the cost is
  accepted and recorded.
- **next_authorized_action**: flag as risk; owner decision on measurement.

## considered_and_defended

Candidates the evidence defeated. These are not findings and carry no severity
or closure fields; they are listed so the adjudicator sees the discard pile
rather than inheriting my self-filter.

- **"Two historical DCP receipts were deleted from the consumption seam
  contract, destroying the cross-vendor review adjudication provenance
  (`reviewed_by: OpenAI GPT-5.5 Pro`, `de_correlation_bar`, report path)."** —
  Defeated. `.agents/workflow-overlay/source-of-truth.md:107-110` requires a
  controlling file to keep **at most the two most recent receipts inline** and to
  **delete the oldest when adding a third**, with Git/PR history as the
  preservation mechanism and the archive explicitly frozen. The base carried 3
  receipts (already over the cap, and with a malformed unclosed fence — 10 fences,
  a `​```yaml` opened inside an unclosed block); the change lands at exactly 2 and
  repairs the fence. `check_dcp_receipt_hygiene.py` confirms both directions: it
  flags 4 receipts as `too_many_inline_dcp_receipts` and passes the as-authored 2.
  I authored a restoration patch, the gate flagged it, and I reverted it —
  reported here in full rather than quietly dropped, because it was my strongest
  candidate and it was wrong.
- **"`append_silver_record_set` interleaves verification with member-byte
  building, so it is not all-before-any."** — Defeated. `members` is a local dict
  and `data_root.append_record_set` is called only after the loop completes
  (`silver_record.py:625-638`), so a failure on member *k* persists nothing for
  members *0..k-1*. Envelope + write-binding validation is a separate prior full
  pass over all members.
- **"`_verify_derived_ref` applies `silver_content_hash` to non-Silver derived
  records (cleaning audit packs), so every legitimate cleaning Silver write would
  fail."** — Defeated. The audit pack's `_content_hash`
  (`cleaning/basenotes_lake.py:373-376`) uses the identical canonicalization
  (pop `content_hash`; sorted-keys, compact-separator, non-ASCII-preserving JSON)
  as `silver_content_hash`, so the recomputation is coherent. The full cleaning
  pipeline suite passes.
- **"A derived ref's address is record-controlled, so it could resolve an
  arbitrary path (path substitution)."** — Defeated. `DataLakeRoot.record_path`
  (`root.py:765-776`) validates `subtree` against `_APPENDABLE_SUBTREES`, runs
  `_validate_segment` on `raw_anchor`/`lane`/`record_id`, and confines resolution
  to `_within`, so traversal outside the lake is rejected before any read.
- **"The census now walks only active lanes, so retired-lane bytes silently
  vanish from the observation record."** — Defeated. The walk is over
  `sorted(SILVER_LANES)` (`silver_census.py:608`), which still includes retired
  lanes. Their records count into `silver_records` and route to
  `unclassified_silver_records` because their `schema_version` is not
  `silver_vault_record_v0` (`:642-644`) — visible, named, and non-authoritative,
  which is the commissioned behavior. `_ACTIVE_SILVER_LANES` gates only the
  applicability table.
- **"Removing four tests from `test_ig_reels_deep_capture_lake.py` weakens
  coverage of transient-URL redaction and write-once semantics."** — Defeated.
  Every removed test asserted persistence behavior of a writer that now raises
  before persisting; three new tests cover the retirement (fail-before-bytes,
  stable historical audit record id, runner surfacing `eligible_bronze_required`).
  Coverage tracks the behavior that still exists. (The now-uncovered helpers are
  recorded separately as FIND-05.)
- **"`DataLakeRootError` is not a `ValueError`, so the census `except (TypeError,
  ValueError)` would let a lake error escape and crash the census."** — Defeated.
  `verify_silver_vault_record_sources` catches `DataLakeRootError` internally
  (`silver_record.py:224,231`) and re-raises `SilverRecordError`, a `ValueError`
  subclass, so the census handler is reached.

## Controller Patch

**None.** No unified diff is returned; the working tree is clean at
`21317aa9b1b005925eb75503652ae79d20144242`.

One patch was authored and then reverted: a restoration of the two pruned DCP
receipts in
`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`
(86 insertions, 0 deletions). Running the owning gate showed the patch itself
violated the two-receipt cap in `.agents/workflow-overlay/source-of-truth.md` —
the as-authored state was correct and my patch was the defect. It was reverted with `git checkout --`, the file is
byte-identical to HEAD, and `git status --porcelain` is empty. Full reasoning is
recorded in `considered_and_defended` above.

Every remaining finding is either design-level (FIND-01, FIND-03: they require
deciding hash-basis vocabulary and alias semantics), owner-decision
(FIND-02, FIND-05, FIND-08), or explicitly optional (FIND-04, FIND-07). Under the
commission's escalation contract, none is a defect I may safely close by
patch inside the named scope.

## Validation Evidence

All commands run in `C:\Users\vmon7\Desktop\projects\forseti-worktrees\1b40\orca`
at HEAD `21317aa9`, against the as-authored tree (post-revert).

| Command | Result |
|---|---|
| `python -m pytest -p no:cacheprovider -q <44 bound test files>` (the commission's combined suite, from `forseti-harness`, `PYTHONDONTWRITEBYTECODE=1`) | **pass** — exit 0; 452 passed, 2 skipped, 0 failed. Only `datetime.utcnow()` DeprecationWarnings, all from untouched capture modules. |
| `git diff --check` (working tree) | **pass** — exit 0 |
| `git diff --check d790ac11..HEAD` | **pass** — exit 0 |
| `python .agents/hooks/check_retrieval_header.py <consumption seam contract>` | **pass** — exit 0 |
| `python .agents/hooks/check_dcp_receipt.py --strict --base d790ac11...` | **pass** — exit 0; "3 changed Markdown files; 3 real receipts/blockers shape-valid across 2 files" |
| `python .agents/hooks/check_dcp_receipt_hygiene.py <consumption seam contract>` | **pass** — exit 0, no findings on the as-authored file (it flagged `too_many_inline_dcp_receipts` only against my reverted patch) |
| `python .agents/hooks/check_silver_lane_registry.py` | **pass** — exit 0; "no silver-lane write violations". Notes 2 statically unresolved lane args, incl. `ig_reels_deep_capture_lake.py:145` — inside the now-unreachable body (FIND-05). |
| Live `F:\forseti-data-lake` read or write | **not_run** — forbidden by the commission. FIND-08's runtime cost is unmeasured for this reason. |

No command was skipped silently; nothing failed. Passing tests are evidence the
bound gates hold at this revision — they are not a readiness or Mini God Tier
claim, and per FIND-02 they do not establish real-source behavior.

## Residual Risk And Not-Proven Boundaries

- **Real-source admission is unproven.** No repository evidence shows that any
  record whose sources live in the unavailable private lake passes the new gate.
  Every passing physical-verification test resolves against temp-lake packets
  created by the test to match the digests asserted (FIND-02).
- **`hash_basis` semantics are unresolved** (FIND-01). Until reconciled, the
  field is a label the gate does not enforce, and the fixtures already carry one
  basis value that contradicts the digest beside it.
- **Census runtime cost on a real lake is unmeasured** (FIND-08).
- **Concurrency/robustness of the verifier under a mutating lake was not
  examined** — the gate reads packets and derived records non-transactionally;
  no finding is made, but no assurance is offered either.
- **The Bronze Attachment-Record path was reviewed by reading only.** No test in
  the bound suite drives `_verify_attachment_record_ref` against a catalog whose
  row disagrees with a ref field; the field-mismatch loop
  (`silver_record.py:300-314`) checks only fields the ref actually carries, so a
  ref that simply omits a field skips that comparison. Not raised as a finding —
  the commission's owner-bound behavior permits optional fields — but the
  omit-to-skip shape is worth the adjudicator's eye.
- **I did not attempt to prove the negative** that no other authority-making
  reader bypasses the gate. I checked the readers named in the commission
  (`silver_census`, `product_mention_selection`, `ig_reels_behavioral_lake`) and
  found all three routed through `verify_silver_vault_record_sources`. A
  repo-wide sweep for unrouted Silver readers was not performed.
- This review is **decision input only**. It is not approval, validation,
  mandatory remediation, readiness, or executor-ready patch authority.

## Adjudicator Next Moves

Chief Architect: close this adjudication under
`.agents/workflow-overlay/communication-style.md` → **Review Adjudication Next
Step**. Adjudicate the findings, verdict, and residuals as claims — not as
premises to inherit; close any self-closable material issue in the same turn;
route a smallest-complete closure step only where another review round, another
lane, an architecture pass, or an owner decision is genuinely needed; then batch
admin/lifecycle follow-ups into exactly one land step with no deep-thinking;
then, if a visible active goal or `thread_operating_target` exists, deep-think
the 1-5 material moves that best advance it — otherwise record
`no_visible_active_goal`.

Specifically worth a decision: FIND-01 and FIND-02 travel together — both trace
to the same unresolved question of what a raw-ref digest is a hash *of*.
Resolving the basis vocabulary would likely make a faithful watch-html-branch
test writable, closing both.

## Review-Use Boundary

These review findings are decision input only. They are not approval, not
validation, not mandatory remediation, and not executor-ready patch authority
until separately accepted or authorized by the commissioning Chief Architect.
