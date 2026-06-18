# Source Capture — Typed Archive Snapshot-Time Decision (Two-Date Timing Contract) v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Capture-spine producer decision adding a typed, producer-owned archive
  snapshot-time field (`archive_snapshot_time`) to the Source Capture packet
  timing contract, so archive-mode observations can be dated from the archive's
  own snapshot moment instead of the HTTP fetch time. Publishes the seam name,
  placement, semantics, normalization, schema-version decision, and the blessed
  legacy-packet derivation rule that downstream consumers bind to.
use_when:
  - A consumer (demand-projection dating, ECR SP-3 timing) needs the typed
    archive snapshot-time seam this lane published.
  - Reviewing or extending the archive packet timing contract.
authority_boundary: retrieval_only
open_next:
  - orca-harness/source_capture/models.py
  - orca-harness/runners/run_source_capture_archive_packet.py
  - orca/product/spines/capture/packet_schema/source_capture_packet_schema_evolution_architecture_v0.md
branch_or_commit: capture-archive-snapshot-timing (base main @ f15de945); no merge (owner-gated)
input_hashes:
  commission_handoff_sha256: 69E370A3C39D5206030DFBA3E16F06D037C2467F5129608CBA2C9F6936C2EC04
  models_py_sha256_after: c59322785af4d2cdaf41e842e8a8cd17df95f772d2d49deb03d11eea8d370480
downstream_consumers:
  - demand-projection mode-aware archive dating (binds the typed field; separate lane)
  - ECR SP-3 timing/cutoff binding (binds a real timestamp instead of prose; separate lane)
stale_if:
  - capture_time or cutoff_posture semantics are changed (this decision assumes both unchanged).
  - a breaking manifest_version bump (v1 -> v2) lands (revisit the no-bump decision below).
  - archive_snapshot_time is renamed or its placement changes before consumers bind.
```

## Status

`DECIDED — IMPLEMENTED IN LANE, NOT MERGED (owner-gated)`. Bounded design +
implementation executed under the owner-couriered accepted handoff
(`docs/prompts/handoffs/capture_spine_archive_snapshot_typed_timing_handoff_prompt_v0.md`,
SHA256 verified `69E370A3…C2EC04`). This record is the published seam; the
demand-projection and ECR SP-3 lanes bind to it. It is not validation, readiness,
acceptance, ECR ratification, or merge authorization.

## Decision (one line)

Archive-mode Source Capture packets now declare a **typed, producer-owned
`archive_snapshot_time`** on `PacketTiming` — the archive's own snapshot moment,
normalized to ISO-8601 UTC `Z` — **distinct from `capture_time`** (our
fetch/access time, unchanged), populated-or-typed-unknown, additive and
forward-only with **no `manifest_version` bump** (the change is non-breaking).

---

## 1. The typed field (the seam consumers bind to)

| Property | Value |
| --- | --- |
| **Name** | `archive_snapshot_time` |
| **Type** | `VisibleFact | None` (optional, default `None`) on `PacketTiming` (`orca-harness/source_capture/models.py:85-95`) |
| **Placement** | Packet-level `packet.timing` **and** both archive slice timings (`archive_availability`, `archive_snapshot_body`). One value computed per packet, carried consistently. |
| **Known value** | The archive snapshot timestamp normalized to ISO-8601 UTC `Z` (e.g. Wayback `20240101000000` → `2024-01-01T00:00:00Z`) — same format as `capture_time`. |
| **Unknown** | `unknown_with_reason(...)` when no snapshot was selected, or the declared timestamp is not a parseable 14-digit Wayback form. **Never** fabricated; **never** the fetch time. |
| **`None`** | The producer did not set the field for this packet — a **legacy** packet captured before the field existed, or a **non-archive** capture mode. New archive packets always emit a `VisibleFact`, never `None`. |

**Semantics (the binding contract).** `archive_snapshot_time` answers *"when did
the archive capture this surface?"* It is **independent of `capture_time`**, which
answers *"when did we obtain the bytes from the archive?"* and keeps its current
meaning (no rename, no repurpose). A consumer dating an archive observation reads
`packet.timing.archive_snapshot_time`; it never parses prose or the
`archive_availability_metadata.json` side-file for a new packet.

**Three distinct, honest times now coexist on an archive packet** (none collapsed):
`archive_snapshot_time` = the snapshot moment; packet-level `capture_time` = the
packet **write** time (`writer.py` `utc_now_z()`); slice-level `capture_time` = the
archive **fetch** time (`metadata["capture_timestamp"]`).

**Producer code path.** `_archive_snapshot_time_fact()` +
`_normalize_wayback_timestamp()` in
`orca-harness/runners/run_source_capture_archive_packet.py`; threaded to the
packet level via a new optional `archive_snapshot_time` parameter on
`write_local_source_capture_packet` (`orca-harness/source_capture/writer.py`),
and onto the slice timings via `_availability_timing` / `_body_timing`.

## 2. Schema-version decision — NO bump (deviation from handoff §3 success-signal #4, with reasons)

Handoff success-signal #4 said "schema version bumped per your lane's rules."
**My lane's rule** — the adopted packet schema-evolution architecture
(`docs/product/source_capture_packet_schema_evolution_architecture_v0.md`, Q2 /
AR-02) — bumps `SOURCE_CAPTURE_MANIFEST_VERSION` **only on a breaking change**
(required-add / vocab-narrow / field-remove). This change is an **additive
*optional* field**, which is none of those:

- **Backward read holds:** under `StrictModel(extra="forbid")`, an existing
  manifest that omits the key still validates (the field defaults `None`).
  Verified by `test_packet_timing_archive_snapshot_time_is_optional_for_legacy_manifests`.
- **The consumer keys on field presence, not version** (handoff §3 #7: "prefer
  typed → else blessed legacy derivation → else typed dating-gap").
- Bumping would **mislabel** a non-breaking change as a version break, flip all
  existing v1 packets to `declares_current_manifest_version = False`
  (`packet_inspection.py:91`), and trip that architecture doc's own
  `stale_if` ("a second breaking bump v1 → v2").
- **Forward-skew limit acknowledged:** an older reader whose `PacketTiming`
  model predates this field and still uses `extra="forbid"` will reject a new
  manifest carrying `archive_snapshot_time` (including a serialized `null` on a
  non-archive packet). The no-bump decision is therefore a backward-read /
  current-reader compatibility decision, not a guarantee that old code can read
  new manifests. A version bump would not make that older strict reader accept
  the extra key; it would only label this additive field as a breaking v2
  contrary to the adopted bump-on-breaking-change rule.

**Owner-confirmed (this turn): no bump.** `SOURCE_CAPTURE_MANIFEST_VERSION`
stays `source_capture_packet_manifest_v1` (unchanged — verified in the diff). The
typed field's presence (`VisibleFact` vs `None`) is the consumer's signal.

## 3. Blessed legacy-packet rule (published)

For an **archive-mode** packet where `packet.timing.archive_snapshot_time` is
`None` (captured before this field existed), a consumer **MAY** derive the
snapshot time from the preserved
`archive_availability_metadata.json → selected_snapshot.timestamp` (14-digit
Wayback form), normalizing it the same way, and **MUST** flag the resulting
observation `derived_from_preserved_metadata`. A consumer **MUST NOT** fall back
to `capture_time` / fetch time for dating. Preserved packets are **not** modified
to backfill the field (packet read-once doctrine holds).

Disambiguation for `None`: only **archive-mode** packets (`capture_mode =
archive/history`) take the legacy derivation; for non-archive packets `None`
correctly means "no archive snapshot," and their existing fetch-time dating is
already correct.

## 4. Sample new-packet manifest excerpt (authentic `model_dump`)

Packet-level `timing` block of a new archive packet with a selected snapshot
(`json.dumps(..., sort_keys=True)`, as written to `manifest.json`):

```json
"timing": {
  "archive_snapshot_time": { "status": "known", "value": "2024-01-01T00:00:00Z", "reason": null },
  "capture_time":          { "status": "known", "value": "2026-06-11T13:22:04Z", "reason": null },
  "cutoff_posture":        { "status": "known", "value": "pre_cutoff", "reason": null },
  "recapture_time":        { "status": "not_applicable", "value": null, "reason": "archive packet did not model an earlier capture by default" },
  "source_edit_or_version":{ "status": "known", "value": "Archive.org snapshot timestamp 20240101000000", "reason": null },
  "source_publication_or_event": { "status": "unknown_with_reason", "value": null, "reason": "Archive.org adapter did not infer original source publication or event timing" }
}
```

Note `archive_snapshot_time` (`2024-01-01T00:00:00Z`) is **distinct** from
`capture_time` (`2026-06-11T13:22:04Z`). The same block carries onto each archive
slice timing. When the snapshot timestamp is absent or unparseable, the field is
`{ "status": "unknown_with_reason", "value": null, "reason": "...not a parseable
14-digit Wayback timestamp" }`.

## 5. §4 evidence chain — re-verified against this lane's HEAD

The mis-dating chain **holds on the producer side** (this lane's edit scope),
re-verified in this worktree:

- archive runner intermediate timing and archive slice `capture_time` use
  `known_fact(str(metadata["capture_timestamp"]))` — runner `:116-127`;
  `_body_timing` `:346-358`; `_availability_timing` `:361-370`.
- final packet-level `capture_time` is rebuilt by `writer.py` from
  `captured_at` (`writer.py:91-102`, `:134-149`), so it is packet write/access
  timing rather than archive snapshot timing.
- `capture_timestamp = utc_now_z()` (fetch wall-clock) — `direct_http.py:164`, `anti_blocking_http.py:216`.
- snapshot time as **prose** in `source_edit_or_version` (`_source_version_from_snapshot`) + structured side-channel `selected_snapshot.timestamp` in `archive_availability_metadata.json` (`_snapshot_metadata`).

**Two §4 links cited from the demand-projection lane are absent from `main`**
(observed: `orca-harness/source_capture/demand_projection/**` → no files):
`jsonld_demand.py` and `projector.py` are **consumer-side** files on the unmerged
`capture-demand-projection` branch. This **confirms this lane is producer-only**;
those consumers bind to this published field in their own lane (handoff §3 #7).

## 6. Validation evidence

Run with the project venv (CPython 3.12.7, pydantic 2.13.4), pytest 9.0.3.

- **150 passed, 0 failed** across the full source-capture blast radius (archive,
  packet, packet-assembly, packet-inspection, both HTTP adapters, media, reddit,
  source-quality, and the matching contract tests). No regression from the added
  timing key.
- New tests (all pass):
  - `test_archive_runner_emits_typed_archive_snapshot_time` — end-to-end: packet + both slices carry the normalized known snapshot time; `capture_time` distinct.
  - `test_archive_runner_types_archive_snapshot_time_unknown_when_no_snapshot` — **absent** → typed `unknown_with_reason`.
  - `test_normalize_wayback_timestamp_present_and_unparseable` — **present** → ISO-8601 Z; wrong-length / non-numeric / empty / impossible-date → `None`.
  - `test_archive_snapshot_time_fact_present_absent_unparseable` — **present / absent / unparseable** at the fact builder.
  - `test_packet_timing_archive_snapshot_time_is_optional_for_legacy_manifests` — legacy manifest (no key) still validates; field reads back `None` (additive, no bump).
  - `test_packet_timing_accepts_explicit_archive_snapshot_time` — explicit set; `capture_time` stays its own distinct fact.
- Diff: **+161 / −0** (purely additive), 5 files, all under `orca-harness/`. `SOURCE_CAPTURE_MANIFEST_VERSION` line unchanged.

## 7. Constraints honored

- Additive only; `capture_time` and `cutoff_posture` not renamed, repurposed, or re-vocabularied.
- No fabrication path: unknown snapshot time is typed-unknown; never defaults to fetch time.
- Archive/history producers populate the field as a `VisibleFact`; non-archive
  runners leave it `None`. Because the field lives on shared `PacketTiming`, new
  non-archive manifests may serialize `"archive_snapshot_time": null`; that is a
  deliberate shape footprint, not a timing-semantics change (`capture_time`
  remains intact).
- Existing preserved packets / manifests not modified. No merge.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Archive-mode Source Capture packets now declare a typed, producer-owned
    `archive_snapshot_time` field on PacketTiming (the archive's own snapshot
    moment, normalized ISO-8601 Z), distinct from capture_time; additive and
    optional with no manifest_version bump (backward-read/current-reader
    compatible under the adopted bump-on-breaking-change rule; old strict-reader
    forward skew remains a recorded limitation). It is the published seam downstream archive
    observation dating and ECR SP-3 timing bind to.
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/writer.py
    - orca-harness/runners/run_source_capture_archive_packet.py
    - docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md
  downstream_surfaces_checked:
    - path: docs/product/source_capture_packet_schema_evolution_architecture_v0.md
      note: >
        Change is consistent with its adopted recommendation (additive evolution,
        bump-on-breaking-change only, lenient read). Its models.py input_hash pin
        (3B89A19B...A7245) and `stale_if: models.py SHA256 drifts` are now tripped
        by this additive edit (new hash c5932278...0480); see intentionally_not_updated.
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      note: >
        Ob.8 "Decomposed Timing" (lines 240-255) already requires preserving timing
        as separate visible categories where available; the typed field implements
        that for the archive snapshot category. No obligation changed.
    - path: orca-harness/source_capture/packet_inspection.py
      note: lenient version-aware read still holds; legacy v1 packets stay readable and conforming.
  intentionally_not_updated:
    - path: orca-harness/source_capture/models.py (SOURCE_CAPTURE_MANIFEST_VERSION)
      reason: additive optional field is backward-read/current-reader compatible; bump-on-breaking-change rule => no bump (owner-confirmed), with old strict-reader forward skew recorded as a limitation.
    - path: docs/product/source_capture_packet_schema_evolution_architecture_v0.md (input_hashes re-pin)
      reason: >
        Re-pinning that doc's models.py hash and clearing its drift `stale_if` is
        separate freshness hygiene, not this bounded lane; the change upholds, not
        contradicts, its recommendation.
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: implements Ob.8 (separate visible timing category); adds/changes/removes no obligation. Naming the field explicitly there is optional future hygiene.
    - path: existing preserved packets / manifests
      reason: packet read-once doctrine; legacy packets handled by the published legacy rule, not backfill.
    - path: demand-projection and ECR SP-3 consumer lanes
      reason: they bind to this published seam in their own lanes (handoff §3 #7); not this producer lane's edit scope.
  stale_language_search: >
    grep -rnEi "survives only as prose|only as prose|no typed snapshot|prose in
    source_edit_or_version|single typed time" docs/ (worktree), excluding the
    commission handoff.
  stale_language_search_result: >
    No hits. No durable producer doc asserts that archive snapshot time exists
    only as prose / has no typed field, so the purely additive change desyncs no
    existing rule.
  non_claims:
    - not validation
    - not readiness
    - not acceptance or ECR ratification
    - not merge authorization
    - not a change to capture_time or cutoff_posture semantics
```

## Downstream seam (recorded — not this lane's scope)

- **Demand projection** implements its mode-aware archive dating against
  `packet.timing.archive_snapshot_time` (prefer typed → else the §3 legacy
  derivation + `derived_from_preserved_metadata` flag → else typed
  dating-gap/refusal).
- **ECR SP-3** binds the real typed timestamp instead of the prose in
  `source_edit_or_version`.

## Non-Claims

A producer contract decision + bounded in-lane implementation. Not validation,
readiness, acceptance, ECR ratification, deployment, or merge authorization. Does
not redesign cutoff posture, ECR fields, or archive capture mechanics; does not
modify existing preserved packets; does not bind the consumer lanes (they consume
this seam in their own lanes).
