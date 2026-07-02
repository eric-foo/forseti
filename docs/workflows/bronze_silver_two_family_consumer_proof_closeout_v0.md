# Bronze/Silver Two-Family Consumer Proof Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow closeout record
scope: >
  Records the post-PR #537 and post-PR #540 Bronze/Silver consumer-proof state:
  two source-family Silver producers consume public Bronze source-surface catalog
  and Attachment Record rows without claiming Bronze full GT.
use_when:
  - Checking whether the Bronze/Silver lane needs more default source-family proofs.
  - Re-establishing post-PR #537/#540 Silver consumption proof status.
  - Naming residuals before promoting work into the Bronze full-GT upgrade path.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py
branch_or_commit: origin/main@d7d2b62e0f528a8bba2bfe03bcb408bab2cd1358
stale_if:
  - PR #537 or PR #540 is reverted or materially rewritten after merge.
  - The Bronze MGT declaration, Silver Vault contract, or Attachment Record contract is superseded.
  - Either named Silver producer stops consuming public Bronze helper surfaces for AR-backed raw_refs.
  - A later accepted authority declares Bronze full GT or changes the source-family proof requirement.
```

## Success Signals First

This closeout treats the current material sequence as successful when all of the
following are true:

- Current `main` contains the PR #537 and PR #540 proof paths.
- At least two different Bronze source-family payloads have a Silver producer that can
  consume public Bronze `source_surface_catalog_rows` / Attachment Record rows
  for source-backed `raw_refs`.
- The AR-backed `raw_refs` carry re-resolution material, missing AR stays
  visible instead of being inferred as source absence, and the YouTube path also
  distinguishes ambiguous AR candidates.
- The conclusion stops at consumer proof. It does not claim Bronze full GT,
  Silver readiness, production lake validation, Manifest v2, body-store/backend
  selection, or all-source-family coverage.

Material conclusion:

The Bronze/Silver lane has crossed from a one-family example to a two-family
consumer-proof signal. That is enough to stop adding default source-family proofs
as the next bottleneck. Add a third proof only if the candidate source family has
a materially different raw-body or AR join shape that could invalidate the
generic model.

## Source-Loading Receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0/S1 plus PR #537/#540 metadata, Data Lake authority docs, and target producer/test surfaces
  edit_permission: docs-write
  target_scope: post-PR540 Bronze/Silver consumer-proof closeout and next material move sequencing
  dirty_state_checked: yes
  blocked_if_missing: overlay README, source-loading rule, handoff packet, PR merge facts, current-main producer behavior
```

Confirm-don't-trust load result: `REUSE` for the handoff's active objective,
with current-source updates. PR #537 and PR #540 are merged into current `main`;
the next material move is no longer another default first consumer slice.

## Observed Merge And Main-State Facts

These are observed facts, not inherited packet claims:

- PR #537, `[codex] Add Bronze AR raw refs to IG Silver metrics`, was observed
  with `gh pr view` as `state=MERGED`, `mergedAt=2026-06-30T17:56:30Z`, merge
  commit `2f769af8ea20f69b62b0b659e2792317afd4f95f`, head
  `a72a88555e7ff7d36a2c44b2bb42c98d7e57af4e`.
- PR #540, `[codex] Add YouTube Bronze AR raw-ref proof`, was observed with
  `gh pr view` as `state=MERGED`, `mergedAt=2026-06-30T18:58:01Z`, merge commit
  `d7d2b62e0f528a8bba2bfe03bcb408bab2cd1358`, head
  `ff6c0816088da2112beadbc6f57267115a1f7ca8`.
- Current closeout worktree `HEAD` is
  `d7d2b62e0f528a8bba2bfe03bcb408bab2cd1358`.
- `git merge-base --is-ancestor` observed PR #537's merge commit as an ancestor
  of current `HEAD`, and PR #540's merge commit as current `HEAD` or ancestor.

## Controlling Contracts Read

- Bronze MGT baseline declaration: raw packet manifests and preserved bytes stay
  authoritative; the generated Bronze catalog is rebuildable read state, not
  authority; downstream lanes have public query surfaces for source-surface
  packet rows and Attachment Record rows; Silver should now consume those public
  surfaces rather than wait for full GT.
- Silver Vault contract: source-backed `raw_refs` must resolve packet/slice/file
  material and carry hash material; source-family payload refs must enter raw
  truth through Bronze-owned surfaces, not private raw-path inference. Missing AR
  is visible residual, not evidence of source absence.
- Attachment Record contract: a Silver producer can resolve an Attachment Record
  through public Bronze surfaces, verify the body hash, and carry AR-backed
  source refs into Silver `raw_refs` without private packet-member paths. The
  contract does not authorize runtime AR implementation, Manifest v2, migration,
  or a new storage layout by itself.

## Proof Matrix

| Proof family | Landed PR | Public Bronze surface consumed | Silver proof signal | Residual kept visible |
| --- | --- | --- | --- | --- |
| Instagram creator reels grid | PR #537 | `source_surface_catalog_rows(data_root, source_family="instagram_creator", source_surface="ig_reels_grid_dom_passive_json")` in `silver_metric_producer.py` | Optional `use_bronze_attachment_records=True` upgrades observation `raw_refs` to `raw_ref_kind="bronze_attachment_record"` with AR id, schema version, physicalization, body ref/hash, source family/surface, payload kind/schema, and replay pins. | Missing AR falls back to `raw_packet_fallback_missing_attachment_record` with `typed_attachment_record_status="missing"` and `attachment_record_residual="typed_attachment_record_missing_for_raw_ref"`. |
| YouTube watch metadata/comments | PR #540 | `source_surface_catalog_rows(data_root, source_family="youtube", source_surface="youtube_watch_metadata_comments")` in `youtube_silver_metric_producer.py` | Optional `use_bronze_attachment_records=True` joins by packet/body hash and upgrades observation `raw_refs` to `raw_ref_kind="bronze_attachment_record"` with AR id, schema version, physicalization, file/path, body ref/hash, hash basis, source family/surface, payload kind/schema, and replay pins. | Missing AR falls back to `typed_attachment_record_status="missing"`; code also distinguishes ambiguous AR candidates with `typed_attachment_record_status="ambiguous"`. The merged tests pin the hit and missing paths. |

## What Is Proven

- Silver can consume public Bronze helper surfaces for two distinct
  source-family payloads instead of reading generated catalog files as authority
  or reimplementing private safe-name/folder semantics.
- AR-backed source-family `raw_refs` can carry enough material for re-resolution
  and body-hash verification in the producer's record contract.
- The missing-AR case remains visible in the emitted raw ref and record posture.
- The default non-AR path remains available behind an opt-in flag, so this proof
  does not force all consumers onto the new AR mode at once.

## What Is Not Proven

- Not Bronze full GT.
- Not Silver readiness, production runtime readiness, or real-lake completeness.
- Not Manifest v2, backend, body-store, retention, lawful-erasure, migration, or
  final Attachment Record physicalization selection.
- Not all source families and not all possible AR join shapes.
- Not evidence that generated Bronze catalog files are authority over raw packet
  material.
- Not a claim that missing AR means missing payload.

## Next Material Moves

1. Land this closeout record so the lane has a durable progress boundary after
   PR #540.
2. Stop default source-family proof expansion. A third proof should be a
   deliberate exception for a materially different raw-body or AR join shape.
3. Promote the remaining Bronze full-GT work into an explicit upgrade/scoping
   lane: deterministic writer discovery, Manifest v2 or equivalent migration,
   final AR body layout/backend/retention posture, lake-doctor or CI-owned
   representative checks, and de-correlated review before any full-GT claim.
4. If runtime work continues before that full-GT scoping lane, make it a
   downstream consumer or read-side slice that uses public Bronze packet/catalog
   / AR surfaces and preserves missing-AR visibility.

## Operational Guard

Do not let this artifact become a new source of lake authority. It is a routing
and progress record over observed PR/code/contract state. If the named code,
contracts, or PR history moves, reopen the sources in the retrieval header and
re-derive the conclusion.
