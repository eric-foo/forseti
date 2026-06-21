# Capture Spine Core Migration Adversarial Artifact Review Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Review input packet
scope: >
  Greppable source packet for read-only adversarial artifact review of the
  Capture spine core migration at commit a75c337b3497d530f9b7fbfb25acb0fd230d3616.
use_when:
  - Reviewing PR #316's Capture spine core migration as a multi-file artifact change.
  - Checking moved-path correctness, stale references, DCP honesty, and scope containment.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/capture_spine_core_migration_adversarial_artifact_review_prompt_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/capture_spine_core_migration_adversarial_artifact_review_v0.md # nonresolving: expected reviewer output path created by running this prompt
```

## Packet Contents

This packet is generated from the migration commit, not from the later review-package commit.

Normalization note: the greppable snapshot and diff text is whitespace-normalized to satisfy repository whitespace gates. For byte-exact source, use the pinned `merge_base` and `target_ref` Git objects named below.

```text
diff_range_ref: origin/main
merge_base: 35066b1528c7b8a75476ded14461674e76fe8b51
base_snapshot_ref: 35066b1528c7b8a75476ded14461674e76fe8b51
target_ref: a75c337b3497d530f9b7fbfb25acb0fd230d3616
name_status_rows: 226
head_file_count: 226
base_file_count: 225
head_snapshot_count: 226
base_snapshot_count: 225
status_counts: A=1, M=122, R=103
```

Files:

- `diff_u80.patch` - full migration diff with 80 lines of context.
- `manifest/name_status.tsv` - Git name-status manifest with rename detection.
- `manifest/diff_stat.txt`, `manifest/numstat.tsv`, `manifest/summary.txt` - review navigation aids.
- `manifest/head_files.txt` - all target-side snapshot paths included under `head_files/`.
- `manifest/base_files.txt` - all base-side snapshot paths included under `base_files/`.
- `head_files/` - target-side snapshot text files for all added, modified, copied, or renamed-to files; original source paths are preserved with a `.snapshot.txt` suffix.
- `base_files/` - merge-base snapshot text files for all modified, deleted, copied-from, or renamed-from files; original source paths are preserved with a `.snapshot.txt` suffix.

Hash pins:

```text
diff_u80.patch sha256: 4F2DDD6E5D2AD3C9124BD9E380AD6BBDDB566C2ECAFD1D6173A4B70FB31E3EFB
manifest/name_status.tsv sha256: 087D8B18BD2AF27378188E95A2B1F8429C6E94EDE1761583A00FCE88107DF939
manifest/refs.txt sha256: 711105F253DAF841D71112086F060048D1BF6FDCB456137241732DD04F7A090B
manifest/head_snapshot_files.txt sha256: 7829ED278143AE0FA85B685C0B72C5F3966C3732D610792926B193A120FBF47E
manifest/base_snapshot_files.txt sha256: A43A6D684FDB0526C2485D8EF8D0834D72FFEE7E473C43B01A6F756128AC0E8A
```

## Reviewer Use

Review the filed prompt first:

```text
docs/prompts/reviews/capture_spine_core_migration_adversarial_artifact_review_prompt_v0.md
```

Use `rg` and normal filesystem inspection inside this packet. Useful starting points:

```powershell
rg -n "social_video|capture/source_families/instagram|capture/contracts|capture/operating_model" docs/review-inputs/capture_spine_core_migration_adversarial_artifact_review_v0
rg -n "source_quality|cadence|missingness|satellite|web_search_capture|youtube|tiktok" docs/review-inputs/capture_spine_core_migration_adversarial_artifact_review_v0
rg -n "orca/product/spines/capture/" docs/review-inputs/capture_spine_core_migration_adversarial_artifact_review_v0/head_files
```

The packet is review input only. It is not validation, approval, source-of-truth promotion, readiness, or patch authority.
