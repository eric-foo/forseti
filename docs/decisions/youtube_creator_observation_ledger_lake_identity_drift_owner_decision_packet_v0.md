# YouTube Creator Observation Ledger - Lake Identity Drift Owner Decision Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Owner decision record (Option B2 accepted, owner direction 2026-07-02)
scope: Evidence and options for the disposition of the YouTube Shorts fragrance creator observation ledger's live-lake reconciliation after the 2026-06-28 lake epoch change orphaned its bound data-lake root.
use_when:
  - Deciding whether the ledger re-binds to the v4.1 lake, freezes as a historical fixture on the retired root, or both via a new ledger version.
  - Investigating why the ledger's opt-in live-lake reconciliation test fails with live_lake_root_uuid_mismatch.
  - Deciding standing doctrine for packet-ref-bearing product-spine artifacts across clean-forward lake epochs.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
  - orca-harness/capture_spine/youtube_creator_observation/validation.py
stale_if:
  - A later owner decision supersedes Option B2 or re-binds the ledger to a different lake root.
  - Either lake root at F:\orca-data-lake or F:\orca-data-lake-legacy-v0-20260628T174129Z is moved, deleted, or re-initialized.
```

## Status

`ACCEPTED_OPTION_B2` (owner direction 2026-07-02, in-session, after reviewing
this packet). Superseded framing: sections below were authored while the
decision was pending and are retained as the decision basis. Owner inputs
answered at acceptance:

1. Disposition: **Option B2** - ledger v0 stays a static historical fixture
   bound to the retired root; the opt-in reconciliation is kept, re-aimed at
   the preserved archived root.
2. Legacy-root preservation: **keep as-is** at
   `F:\orca-data-lake-legacy-v0-20260628T174129Z` (owner declined deletion
   2026-07-02; ~10 MB, 1,648 files at that decision).
3. Shared test variable: **split** - this ledger's check moved to a dedicated
   `ORCA_ARCHIVED_LAKE_TEST_ROOT` opt-in (agent default under the accepted
   B2 residual, stated at application).
4. The standing epoch-vs-ledger doctrine question remains **open** - not
   decided by this record.

## Application Record (2026-07-02)

Applied surfaces (see the DCP receipt at the end of this file):

- `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py`: the
  opt-in test renamed to `..._archived_lake_refs_when_available` and re-keyed
  from `ORCA_LIVE_LAKE_TEST_ROOT` to `ORCA_ARCHIVED_LAKE_TEST_ROOT`, so
  live-lake suite runs no longer false-alarm on this fixture and this check
  no longer targets the live lake.
- `orca-harness/tests/conftest.py`: hermeticity comment extended to name the
  new archived-lake opt-in variable.
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`:
  root-binding paragraph now records the retired/archived root status and the
  archived-evidence-check semantics.
- `docs/workflows/orca_repo_map_v0.md` and
  `docs/workflows/data_capture_spine_consolidation_map_v0.md`: live routing
  rows repointed from "live-lake verifier" to the archived-lake evidence
  check.
- The ledger JSON and `validation.py` are intentionally unchanged (B2 core:
  the ledger's recorded provenance was already truthful; the validator is
  root-agnostic and its `live_lake_*` error-code vocabulary is
  fixture-asserted).

## Problem

The ledger
`orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json`
binds its data-lake provenance (`source_inputs`) to root_uuid
`01KW1E6N133JT0XCN2KCN0V5A4` (label `orca-canonical`, contract `v0`). The live
lake at `F:\orca-data-lake` now carries root_uuid
`01KW7N6ERSVVANCEZ8SD6YW3EQ` (label `orca-canonical-v4-1`, contract `v4.1`,
created 2026-06-28T17:42:20Z). The opt-in reconciliation
(`validate_youtube_creator_observation_ledger_against_live_lake`, exercised via
`ORCA_LIVE_LAKE_TEST_ROOT` per PR #592) therefore fails closed at
`live_lake_root_uuid_mismatch` before comparing any of the 200 packet refs.

## Verified Evidence (all observed 2026-07-02, read-only)

1. **The 2026-06-28 event was a clean forward epoch, not an in-place
   migration.** `F:\orca-data-lake\.orca-lake-epoch.json` records
   `"epoch_policy": "clean_forward_epoch"`, `"compatibility_migration": false`,
   and names `"legacy_roots": ["F:\\orca-data-lake-legacy-v0-20260628T174129Z"]`.
2. **The v4.1 lake contains none of the ledger's 200 packets.** A read-only
   probe mirroring the validator's per-ref checks found 200/200 refs
   `manifest_missing` against `F:\orca-data-lake` (the referenced shard
   directories do not exist). The premise "the migration preserved raw content
   and only the root identity changed" is **false** for the live root.
3. **The retired root survives intact on disk with the exact bound identity.**
   `F:\orca-data-lake-legacy-v0-20260628T174129Z\.orca-data-root` reads
   root_uuid `01KW1E6N133JT0XCN2KCN0V5A4`, label `orca-canonical`, contract
   `v0`, created 2026-06-26T07:44:40Z.
4. **All 200 refs verify against the legacy root.** The same probe returned
   200/200 `ok`: manifest and metadata files exist and `packet_id`,
   `source_family`, `source_surface`, `platform_video_id`, and `channel_id`
   all match the ledger refs. Zero failures.
5. **The actual harness test confirms both results.** Run from
   `orca-harness/`:
   - `ORCA_LIVE_LAKE_TEST_ROOT=F:\orca-data-lake` -> FAILED,
     `live_lake_root_uuid_mismatch` (reproduces the reported breakage);
   - `ORCA_LIVE_LAKE_TEST_ROOT=F:\orca-data-lake-legacy-v0-20260628T174129Z`
     -> PASSED (1 passed), with no code or ledger change.
6. **The v4.1 lake only incidentally overlaps this pool.** It holds 326
   packets (267 youtube). Its youtube packet metadata carries 31 distinct
   `platform_video_id` values; all 31 are ledger videos, but they are scattered
   across only 12 of the 31 creator observations (0-4 videos each) under
   re-minted packet ids. 169 of the 200 ledger videos have no v4.1 packet at
   all. This is incidental overlap from newer capture work, not a systematic
   re-capture of the pool.
7. **Blast radius beyond this ledger.** 15 repo files reference the retired
   root_uuid, including the ledger spec
   (`youtube_creator_observation_ledger_spec_v0.md`, which states the seed
   artifact reconciles to that root), seven
   `docs/review-inputs/youtube_shorts_fragrance_*` capture artifacts,
   `orca-harness/runners/poll_and_extract.ps1`, and
   `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`.
   This packet scopes only the ledger's reconciliation path; the wider set
   shares the same drift and may need the same doctrine applied later.

## Options

### Option A - re-verify refs and re-bind provenance to the v4.1 root

**Not available as stated.** A re-bind presumes the packets survived under the
new identity; evidence items 2 and 6 show they did not. What Option A actually
requires is a rebuild: re-capture ~169 videos into the v4.1 lake, re-match all
200 video ids to new packet ids/relpaths, recompute the ledger's ref-derived
fields and counts, and update the spec's root binding. Residual risks: YouTube
availability drift since the 2026-06 captures (deleted/private videos cannot be
re-captured, changing the evidence base), and the result is materially a new
observation snapshot - honestly a v1 ledger against the v4.1 epoch, not an
edit of v0. If the owner wants a live-lake-bound creator ledger, commission
this as a **new ledger version in its own lane** rather than mutating v0's
provenance.

### Option B - declare v0 a static historical fixture bound to the retired root

The ledger already declares `ledger_mode: source_backed_static_fixture` and its
recorded provenance is truthful: the evidence it cites exists, verified
200/200, in the preserved legacy root. Two sub-flavors:

- **B1 - retire the live reconciliation path for this ledger.** Remove or
  permanently skip the opt-in live-lake test for v0. Cost: loses the only
  check that the archived evidence remains intact.
- **B2 - keep the opt-in reconciliation, re-aimed at the archived root
  (recommended).** The check passes today against the legacy root with zero
  code or ledger changes (evidence item 5). The change is documentation and
  operator practice: record that v0's reconciliation target is
  `F:\orca-data-lake-legacy-v0-20260628T174129Z`, and stop pointing it at the
  live lake. Semantics shift from "live lake reconciliation" to
  "archived-evidence integrity check", which matches what the ledger actually
  is. Known residuals to accept or fix: (i) the legacy root is an unmanaged
  filesystem folder outside git - its durability needs an owner call
  (retention/backup); (ii) `ORCA_LIVE_LAKE_TEST_ROOT` is shared with the
  creator-metric silver-snapshot live-lake tests, which want the *live* root,
  so a full-suite run cannot serve both targets with one value - either run
  this test separately or split the variable when the decision is applied.

## Recommendation

**Option B2**, per the Decision Priority order (least compounded risk first):
it is reversible, contained, requires no edit to the ledger or validator
today, preserves real failure visibility (the integrity check stays alive and
passed a fresh run), and locks nothing in. Option A's rebuild remains
available later as a separate v1-ledger lane without any undo. The choice is
still the owner's because it fixes what "provenance" means for a product-spine
fixture: evidence frozen at its capture epoch (B) versus evidence tracking the
canonical live lake (A-as-v1).

## Standing Doctrine Question (surfaced, not decided)

`clean_forward_epoch` as lake policy means **every** future re-initialization
orphans every packet-ref-bearing artifact bound to the prior epoch - this
ledger is just the first to trip. The owner may want a standing rule: packet
provenance in product-spine artifacts binds to a named root epoch and freezes
(with a preservation obligation on retired roots), and live-lake binding is
reserved for artifacts that are rebuilt per epoch. Whichever option is chosen
here, applying it must route through the Doctrine Change Propagation Contract
in `.agents/workflow-overlay/source-of-truth.md`; this packet intentionally
carries no `direction_change_propagation` receipt because no doctrine has
changed yet.

## Owner Inputs Needed

1. Pick A-as-v1, B1, or B2 (or direct another route).
2. If B: state the preservation guarantee for
   `F:\orca-data-lake-legacy-v0-20260628T174129Z` (keep as-is / back up /
   promote to a managed read-only archive).
3. If B2: approve splitting or documenting the shared
   `ORCA_LIVE_LAKE_TEST_ROOT` usage so this test and the silver-snapshot tests
   can target different roots.
4. Whether the standing epoch-vs-ledger doctrine question gets its own
   decision record.

## Non-Claims

Not validation or readiness; not proof of payload-byte integrity in the
archived root (the probe verified existence and the validator's metadata
fields, not content hashes); not a retention guarantee for either lake root
beyond the owner's keep-as-is direction; not authority over the other
artifacts referencing the retired root; not a decision on the standing
epoch-vs-ledger doctrine question; the ledger JSON and `validation.py` remain
unchanged.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The YouTube Shorts fragrance creator observation ledger v0 is owner-accepted
    (Option B2) as a static historical fixture bound to the retired
    orca-canonical v0 lake root preserved at
    F:\orca-data-lake-legacy-v0-20260628T174129Z; its packet-ref reconciliation
    is re-aimed from the live lake to that archived root via a dedicated opt-in
    (ORCA_ARCHIVED_LAKE_TEST_ROOT), shifting the check's semantics from
    live-lake reconciliation to archived-evidence integrity.
  trigger: lifecycle_boundary
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/youtube_creator_observation_ledger_lake_identity_drift_owner_decision_packet_v0.md
    - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
    - orca-harness/tests/unit/test_youtube_creator_observation_ledger.py
    - orca-harness/tests/conftest.py
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md                                     # no ledger/lake-root reference; routes via overlay; no change
    - .agents/workflow-overlay/README.md            # no reference; no change
    - .agents/workflow-overlay/validation-gates.md  # gate semantics unchanged; the check stays opt-in
    - orca-harness/capture_spine/youtube_creator_observation/validation.py  # root-agnostic; unchanged by design
    - orca-harness/tests/unit/test_creator_metric_silver_snapshot.py        # keeps ORCA_LIVE_LAKE_TEST_ROOT for live-lake checks; unaffected
    - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json  # provenance already truthful; unchanged (B2 core)
  intentionally_not_updated:
    - path: orca-harness/capture_spine/youtube_creator_observation/validation.py
      reason: >
        Root-agnostic by construction; renaming
        validate_youtube_creator_observation_ledger_against_live_lake or its
        live_lake_* error codes would churn fixture-asserted vocabulary for no
        behavior change.
    - path: docs/prompts/reviews/silver_lineage_kit_enforcement_codex_cross_vendor_adversarial_code_review_prompt_v0.md
      reason: >
        Historical review prompt; its environment caveat names the old test
        name as a point-in-time record.
    - path: >
        docs/review-inputs/youtube_shorts_fragrance_* (7 artifacts),
        orca-harness/runners/poll_and_extract.ps1,
        docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
      reason: >
        They cite the retired root as their own point-in-time provenance; this
        record scopes the observation ledger only. Any wider sweep belongs to
        the open standing epoch-vs-ledger doctrine question.
  stale_language_search: >
    rg -n "ORCA_LIVE_LAKE_TEST_ROOT|live_lake_refs_when_available|live-lake
    verifier" across the repo after edits (run 2026-07-02, results recorded in
    the applying PR).
  non_claims:
    - not validation
    - not readiness
    - not payload-byte integrity proof for the archived root
    - not a retention guarantee beyond the owner's keep-as-is direction
    - not a decision on the standing epoch-vs-ledger doctrine question
```
