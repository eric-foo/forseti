# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Silver Sibling-Selection Helper + IG Metric Seed Migration (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of silver/vault unit (c): the new
  fail-closed sibling-selection rule in data_lake/sibling_selection.py, the
  migration of instagram_metric_seed off its F-IGRC-001 lexical tie-break onto
  that rule, the projection lane's declared record-id derivation rank (the
  formalized catch-up-supersedes relationship), the catch-up runner's
  prefix single-sourcing, and the test + pin-gate updates. The special stakes
  are FAIL-CLOSED CORRECTNESS (can the rule silently pick a stale or wrong
  sibling in any input shape?) and OPERATIONAL BLAST RADIUS (the seed now
  RAISES where it previously picked silently — is every new failure loud AND
  correct?).
use_when:
  - Dispatching the commissioned unit (c) review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/silver-selection-helper` (lane head), pinned commit
  `6713adb7696e745c00a6e0f8c24e4f0caa9ee05c`.
- Review target (the explicitly named multi-file set; the ONLY patchable
  surface; LF git blob bytes at the pinned commit):
  - `[rule]` `orca-harness/data_lake/sibling_selection.py` — SHA256 `2f3d18af906121f1de956e7c54dc192b4949623bd42457ccd69334886d19c259`
  - `[seed]` `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` — SHA256 `bbac0f448d9ca9f45fd2ac38abdcefd5aa23f0d59582dfc85bc8d5a78e371a7a`
  - `[lane-decl]` `orca-harness/source_capture/ig_reels_grid_projection.py` — SHA256 `6ad096feefc6e992c56135f87f6f343da9b3d05d895fd30c0435b3862ade1729` (patchable ONLY in the added declaration: `CATCHUP_IG_REELS_GRID_RECORD_ID_PREFIX` + `projection_record_id_derivation_rank`; the deriver, catalog path, and policy constants stay flag-only)
  - `[catchup-runner]` `orca-harness/runners/run_ig_reels_grid_projection_catchup.py` — SHA256 `b517bc4ab60ac7c125f3c88d67ab92e44baa873b6c71952d203279ffaab699db` (patchable ONLY in the prefix import/alias + comment; seam logic stays flag-only)
  - `[rule-tests]` `orca-harness/tests/unit/test_sibling_selection.py` — SHA256 `b73720faf6f313231e6a3df553f0ed426ee3d63b26cd05c4c042f9d895ffdf60`
  - `[seed-tests]` `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py` — SHA256 `9a7f743d11539aa01520a03a15dee060d814f27456ac937bdba1f0f209887ac2`
  - `[catchup-tests]` `orca-harness/tests/unit/test_ig_reels_grid_projection_catchup.py` — SHA256 `2459c4850406591e10a8d1e91f2c98743a92d979e11916da88a5fa09daaba294`
  - `[gate-pins]` `orca-harness/tests/contract/test_policy_module_version_pins.py` — SHA256 `c029e115fa6d32cf3a50aa517f7fa41e3260fa9f30ad3e86c9066d7c8d6382bf`
- Read-only / flag-only everywhere else — notably
  `orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py`
  (the AR-04 fail-closed rollup selection this rule generalizes; NOT patchable),
  `silver_metric_snapshot.py`, `orca-harness/data_lake/{sov_readout,
  derived_retrieval_views,lane_registry,root}.py`, the seam contract
  (`forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`),
  and the two adjudication records named below.
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_sibling_selection.py
  orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
  orca-harness/tests/unit/test_ig_reels_grid_projection_catchup.py
  orca-harness/tests/unit/test_creator_metric_silver_reader.py
  orca-harness/tests/contract/test_policy_module_version_pins.py
  orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  plus the full suite when feasible (home-lane baseline at the pinned commit:
  2853 tests, 0 failures, 0 errors, 7 skipped, junitxml-verified with
  `ORCA_DATA_ROOT` cleared). Run what your runtime can; report real results
  either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/silver_sibling_selection_helper_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch →
  home-CA adjudication (accept/modify/reject per change, class sweep +
  byte/scope checks) → keep decision. Repo-mode discovery discharges the
  independent-review gate for the patched set.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/silver_sibling_selection_helper_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/silver-selection-helper; implementation committed at 6713adb7)
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
- branch: claude/silver-selection-helper, pinned commit 6713adb7696e745c00a6e0f8c24e4f0caa9ee05c
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [rule] orca-harness/data_lake/sibling_selection.py
     (SHA256 2f3d18af906121f1de956e7c54dc192b4949623bd42457ccd69334886d19c259)
  2. [seed] orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py
     (SHA256 bbac0f448d9ca9f45fd2ac38abdcefd5aa23f0d59582dfc85bc8d5a78e371a7a)
  3. [lane-decl] orca-harness/source_capture/ig_reels_grid_projection.py
     (SHA256 6ad096feefc6e992c56135f87f6f343da9b3d05d895fd30c0435b3862ade1729)
     — patchable ONLY in the added CATCHUP_IG_REELS_GRID_RECORD_ID_PREFIX +
     projection_record_id_derivation_rank declaration; everything else in the
     file is read-only / flag-only.
  4. [catchup-runner] orca-harness/runners/run_ig_reels_grid_projection_catchup.py
     (SHA256 b517bc4ab60ac7c125f3c88d67ab92e44baa873b6c71952d203279ffaab699db)
     — patchable ONLY in the prefix import/alias + comment; seam logic is
     read-only / flag-only.
  5. [rule-tests] orca-harness/tests/unit/test_sibling_selection.py
     (SHA256 b73720faf6f313231e6a3df553f0ed426ee3d63b26cd05c4c042f9d895ffdf60)
  6. [seed-tests] orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py
     (SHA256 9a7f743d11539aa01520a03a15dee060d814f27456ac937bdba1f0f209887ac2)
  7. [catchup-tests] orca-harness/tests/unit/test_ig_reels_grid_projection_catchup.py
     (SHA256 2459c4850406591e10a8d1e91f2c98743a92d979e11916da88a5fa09daaba294)
  8. [gate-pins] orca-harness/tests/contract/test_policy_module_version_pins.py
     (SHA256 c029e115fa6d32cf3a50aa517f7fa41e3260fa9f30ad3e86c9066d7c8d6382bf)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: silver/vault unit (c), the first probe of the lake's
read-layer selection rule. The write-once lake multiplies derived siblings by
design (every policy bump / catch-up re-derivation appends a fresh record next
to its predecessor), and F-IGRC-001 was a consumer selecting a STALE sibling
via a lexical accident: instagram_metric_seed picked per-username projections
by max(observed_count, capture_time-string, lexical path). [rule] is the new
shared fail-closed selection: identical-content collapse -> caller-declared
derivation rank within one raw anchor -> parsed capture-instant recency across
anchors; SiblingSelectionError (reasons ambiguous_sibling_derivation /
unorderable_capture_recency) instead of silently picking. [seed] migrates the
per-username selection onto it and surfaces bypassed fuller-but-staler
siblings as named selection_residuals entries in the seed document.
[lane-decl] formalizes the previously-lexical catch-up-supersedes relationship
as a declared rank (catchup prefix -> 1, all other id classes -> 0); the
prefix VALUE is frozen (fingerprinted into obligation envelopes).
[catchup-runner] single-sources that prefix. [gate-pins] updates the
ig_reels_grid_projection.py pin WITHOUT bumping IG_REELS_PROJECTION_VERSION,
on the claim the change is declaration-only (no derived byte, no record-id
minting, no ack fingerprint changes for the same committed raw).

The failure modes that matter most:
- FAIL-CLOSED CORRECTNESS of [rule]: enumerate input shapes (rank ties,
  missing/equal capture instants, identical-content collapse ACROSS anchors
  with differing instants, single-candidate subjects, empty groups, rank vs
  recency interplay) and hunt for any shape where the rule silently returns a
  stale or arbitrary record instead of the newest-or-raise contract. Compare
  against the AR-04 semantics in silver_metric_reader.select_latest_rollup_per_account
  (read-only) — does the generalization weaken any of its guarantees?
- SELECTION-CHANGE BLAST RADIUS: the seed previously ALWAYS picked something;
  it now raises on ambiguity. Walk realistic lake states (operator-pointed
  fresh-ULID siblings for one packet, catalog + catch-up + operator records
  coexisting, policy re-bumps creating two zz_ catch-up siblings for one
  anchor) — which now raise? Is every new raise honest (true ambiguity) and
  none of them a routine state the lane MUST tolerate? Two same-rank
  catch-up siblings for one anchor now fail closed: verify that is the
  correct contract given the catch-up's ack-keyed skip logic (could a
  policy bump legitimately produce that state?).
- DECLARED-RANK FAITHFULNESS: rank {catchup: 1, everything else: 0} claims to
  formalize the adjudicated zz_-beats-all intent (F-IGRC-001 patch). Read the
  prior adjudication record and the catalog path: does baseline-rank parity
  between bronze_catalog ids and direct ULID ids ever produce a same-anchor
  distinct-content tie that the OLD lexical rule resolved (zz_ absent) and the
  NEW rule refuses — and is refusing right there?
- CONSUMER-GUARD FIDELITY: [catchup-tests]'s
  test_catchup_record_wins_consumer_tie_break_against_stale_catalog_sibling
  passes under the new rule via rank. Could a regressed rank declaration (e.g.
  prefix drift, classifier returning 0 for catch-up ids) pass the remaining
  suite while silently reintroducing the stale-pick class?
- PIN-GATE DECISION: verify the declaration-only claim for [lane-decl] — any
  path where the added code changes derived bytes, record ids, envelope
  fingerprints, or ack semantics for the same committed raw? If yes, the
  version-bump decision was wrong and that is a finding.
- SEED-DOCUMENT HONESTY: selection_residuals emission (only
  newer-capture-fewer-observed-rows; is that the right residual set?), the
  updated projection_dedupe_rule text vs actual behavior, determinism of the
  materialized output (the --check runner must be stable across runs given
  identical inputs), casefolded username subject keys.
- TEST ADEQUACY: could a regressed [rule] (e.g. lexical fallback reintroduced,
  instants compared as strings, rank ignored) pass [rule-tests] +
  [seed-tests]? Missing property: anything the spec claims that no test pins?
- SCOPE DISCIPLINE: any change outside the named set or the two bounded
  sub-scopes.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py
  (AR-04 fail-closed selection precedent; NOT patchable)
- orca-harness/capture_spine/creator_profile_current/silver_metric_snapshot.py
  (how discovery + selection compose upstream; NOT patchable)
- docs/review-outputs/adversarial-artifact-reviews/ig_reels_grid_projection_seam_catchup_delegated_adversarial_code_review_v0.md
  (the F-IGRC-001/002 adjudication this unit builds on; NOT patchable)
- forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (sibling multiplication is by design; NOT patchable)
- orca-harness/data_lake/lane_registry.py + orca-harness/data_lake/root.py
  (write-once append, content-free availability; NOT patchable)
- docs/decisions/silver_vault_goal_frame_ratification_v0.md (the ratified V2
  target the rule serves; NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the selection rule's full input
   space and the seed's realistic candidate states from the sources; map the
   old rule's behavior vs the new rule's behavior over that space; then the
   ways the migration could silently pick wrong, over-raise on routine states,
   or fake-pass its tests.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding, along the failure modes above. Severity labels are
   finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY (respect
   the two sub-scopes on [lane-decl] and [catchup-runner]) closing your
   accepted-quality findings; unified diff in chat, each hunk prefixed with
   its label; run the named tests if your runtime can and report real
   results. Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only,
   NO diff.

RETURN, in order: (1) review_summary YAML + findings (label / severity /
file:line / issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks labeled and annotated with findings + per-change
citations, neutral tone, decision-sufficient substance; (3) verdict +
residual-risk note — state explicitly whether any finding means the seed could
compute wrong creator-metric values from committed records, OR that routine
lake states would now fail the materializer; (4) real test results or an
explicit not-run statement; (5) one-line read-budget audit; (6) adjudicator
tail: your diff, citations, verdict, and test claims are claims to adjudicate
— accept/modify/reject per change; the CA may veto any change; nothing is kept
until that adjudication, which closes per the commissioning overlay's Review
Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable
  (ChatGPT Pro per the owner's courier offer). The branch must be pushed
  before dispatch.
- On return, courier the full output back for review-return adjudication; the
  CA adjudicates per labeled change and lands kept hunks in the same
  adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
