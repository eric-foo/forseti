# Capture Spine Handoff — Typed Archive Snapshot Time (Two-Date Timing Contract) v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt (docs/prompts/handoffs/)
scope: >
  Owner-couriered cross-lane handoff commissioning the Source Capture (capture spine) lane to
  add a typed archive snapshot-time field to the archive packet timing contract (two-date
  model: access time + snapshot time), bless a legacy-packet derivation rule, and publish the
  semantics consumers bind to. Fixes the demand-projection critical finding H1 and unblocks
  ECR SP-3 timing binding quality for archive packets.
use_when:
  - The capture-spine lane receives this via owner courier and designs/implements the field.
  - The demand-projection or ECR lane needs the seam contract this handoff defines.
authority_boundary: retrieval_only
authored_by: claude-fable-5 (demand-projection home-CA lane), 2026-06-11
```

## 0. Commission and authorization

Owner ruling (2026-06-11, demand-projection review-return adjudication): the archive packet
"needs 2 dates — archive date and snap date," and **capture spine owns the typed field**. This
prompt is couriered by the owner; treat it as the accepted handoff granting **bounded
design + implementation scope in your lane only**: the archive-packet timing-contract change
described below, executed under your lane's own validation gates, schema-versioning rules, and
doctrine-propagation contract. Nothing here authorizes edits outside your lane, and this
prompt grants no validation, readiness, or acceptance claims.

Run your own `orca_start_preflight` before acting. Re-verify every citation in §4 against YOUR
worktree HEAD before implementing — they were read in another lane against a dirty tree.

## 1. Problem frame

The demand-projection layer projects preserved archive packets (Wayback snapshots of retailer
product pages) into dated observations — "this product showed this cumulative review count
**as of the snapshot date**" — and 4–6 snapshots spanning years are differenced into a
quarterly review-count curve (the durable-vs-hollow demand persistence signal).

Verified failure (H1, rated CRITICAL on the proven path): every extracted observation is dated
to the **HTTP-fetch wall-clock time**, not the snapshot's own time. The chain:

1. The adapter dates every draft from `packet.timing.capture_time`.
2. The archive runner fills `capture_time` from the HTTP result's `capture_timestamp`.
3. That metadata value is `utc_now_z()` — the moment the fetch ran.
4. The snapshot's real timestamp survives only as **prose** in `source_edit_or_version`
   ("Archive.org snapshot timestamp {ts}") and **structured but side-channel** in
   `archive_availability_metadata.json` (`selected_snapshot.timestamp`) — a metadata file the
   projector deliberately excludes from extraction candidates.

Net effect: 4–6 snapshots from 2023–2025 all emit high-confidence observations stamped
~fetch-day; the years-long curve collapses into a single quarter; the artifact looks
internally consistent. Wrong by construction, silently — a fake-success artifact under the
fail-loud doctrine.

The root cause is a **contract gap, not a data gap**: the date exists in every packet, but
only in derivable (prose / adapter-specific side-JSON) form. The trap fired precisely because
the packet's only TYPED time is the fetch time — any consumer reading the typed surface gets
the wrong date.

## 2. Why this is a cross-lane blocker

1. **Demand projection cannot self-fix.** Its dating-integrity invariant (I3: archive-mode
   observations must carry the snapshot's own declared time from a TYPED field, or a typed
   dating-gap/refusal — never fetch time) needs a typed producer field to bind to. The packet
   schema (`PacketTiming`, slices) is producer-owned; consumers coining timing fields would
   violate the ratified ECR frame rule (D4: bind real fields, coin nothing) and create a
   parallel timing vocabulary.
2. **It gates the build.** The demand-projection revised design failed its de-correlated
   cross-vendor review partly on exactly this (finding F2, accepted): a NOW+gating fix with no
   bound owner is not executable. The architecture amendment and the build gate behind it stay
   blocked until this field's owner (you) lands or schedules the contract.
3. **ECR SP-3 is a second consumer harmed today.** SP-3 timing/cutoff binds M1
   carried-by-reference to the producer's real timestamps (`source_publication_or_event` /
   `source_edit_or_version`), and its clear-condition forces `unknown` on a
   placeholder/unparseable timestamp. For archive packets the snapshot time currently lives in
   `source_edit_or_version` as PROSE — so SP-3 lands on forced-`unknown` even though the data
   exists. The typed field fixes two lanes with one producer change.

## 3. Goal frame and success signals

**GOAL:** every archive-mode Source Capture packet declares, as typed producer-owned facts,
BOTH dates — (a) **access time**: when the bytes were obtained from the archive (the existing
`capture_time`, semantics unchanged), and (b) **snapshot time**: when the archived surface was
captured by the archive (NEW typed field) — such that no consumer ever parses prose or
adapter-specific metadata JSON to date an archive observation.

**Success signals (observable):**

1. New archive packets carry a typed snapshot-time field, populated from the archive's own
   declared snapshot timestamp (Wayback 14-digit form normalized per your conventions).
   Name and placement are YOUR design decisions (candidates: `PacketTiming` packet-level,
   the `archive_snapshot_body` slice timing, or both) — publish the chosen name + semantics
   in your decision record; consumers bind to that publication.
2. Absent / unparseable / undeclared snapshot timestamp → the field is typed-unknown with
   reason (your existing `unknown_with_reason` pattern) — never fabricated, never silently
   filled with fetch time.
3. `capture_time` keeps its current meaning (fetch/access provenance) — no rename, no
   repurpose. `cutoff_posture` untouched (ECR SP-3 carries it as-is).
4. Additive and forward-only: schema version bumped per your lane's rules; existing preserved
   packets are NOT modified (packet read-only doctrine holds — no in-place upgrades).
5. A producer-blessed **legacy rule** is published for archive packets predating the field —
   e.g. "consumers MAY derive snapshot time from the preserved
   `archive_availability_metadata.json` → `selected_snapshot.timestamp`, and must flag the
   observation as derived-from-preserved-metadata" — or your documented alternative. Without
   this blessing every consumer invents its own derivation against your adapter's metadata
   layout.
6. Your lane's tests cover: snapshot ts present / absent / unparseable; sample manifest
   excerpt shows the new field.
7. Downstream effect (not your scope, recorded as the seam): demand projection implements its
   mode-aware dating policy against the typed field (prefer typed → else blessed legacy
   derivation + flag → else typed dating-gap/refusal), and ECR SP-3 can bind a real timestamp
   instead of prose.

## 4. Evidence chain (verified 2026-06-11 by the demand-projection home CA)

Read in `orca-demand-projection-wt`, branch `capture-demand-projection`, HEAD
`3e42ebc6d0792ee4b0c7f175a2d0418db4186e1b`, **dirty working tree** — line numbers are
evidentiary for that read session; RE-VERIFY against your HEAD:

- `orca-harness/source_capture/demand_projection/adapters/jsonld_demand.py:240-244` — drafts
  dated from `packet.timing.capture_time` only.
- `orca-harness/runners/run_source_capture_archive_packet.py:119` — packet `capture_time` =
  `availability_result.metadata["capture_timestamp"]`; `:310-314` — body-slice timing same.
- `orca-harness/source_capture/adapters/direct_http.py:164`, `anti_blocking_http.py:216` —
  `capture_timestamp` = `utc_now_z()` (fetch wall-clock).
- `orca-harness/runners/run_source_capture_archive_packet.py:258-261` — snapshot ts as prose in
  `source_edit_or_version`; `:245-255` — structured `selected_snapshot.timestamp` preserved in
  `archive_availability_metadata.json`.
- `orca-harness/source_capture/demand_projection/projector.py:474-476` — metadata files
  excluded from extraction candidates (why the side-JSON never reaches the projection layer).

Context artifacts (home repo, for orientation — not your edit scope):
- `docs/review-outputs/adversarial-artifact-reviews/demand_projection_f6_r6_revised_design_adversarial_artifact_review_v0.md` (finding F2 + adjudication)
- `docs/review-inputs/demand_projection_f6_r6_norepo_adversarial_artifact_review_bundle_v0/demand_projection_f6_r6_revised_design_v0.md` (design §6 H1, §I3)
- `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` (SP-3 M1 carried-by-reference binding + forced-`unknown` clear-condition)

## 5. Constraints

- Additive only. Do not rename, repurpose, or change semantics of `capture_time`,
  `cutoff_posture`, or existing timing fields.
- No fabrication path: unknown snapshot time stays typed-unknown; never default to fetch time.
- Scope: archive/history capture mode only; live-capture packets untouched (their fetch time
  IS the observation time).
- Do not modify existing preserved packets or their manifests.
- Field name, placement, and normalization are your lane's design authority; the SEMANTICS in
  §3 are the seam contract consumers will bind to.
- Doctrine propagation for the schema change runs under your lane's own gates.

## 6. Where the demand-projection architecture stands (context)

Capture side proven (live + archive packets work). Projection layer v0 exists (3 adapters,
tests green at its decision record). Its honesty-contract hardening is mid-flight: a focused
three-lens architecture pass produced revised design v0 (dispatch guard + conflict-loud dedup
+ closure audit H1–H12 + invariants I1–I7); a de-correlated cross-vendor review (GPT-5.5)
returned NEEDS_ARCHITECTURE_PASS with 6 findings, all accepted; the owner has now ruled on the
two blocking ones (result-algebra recast; THIS dating contract → capture spine). Sequence:
this field lands or is scheduled → demand-projection amendment v1 → fresh cross-vendor review
→ only then build. Your field is the critical-path unlock; the demand lane consumes it in its
amendment, and ECR SP-3 binds to it when ratified.

## 7. Return contract

Report back to the owner/CA: your decision-record path; the typed field's name, placement,
semantics, and schema version; the blessed legacy-packet rule; a sample new-packet manifest
excerpt; validation evidence (tests run); and anything you decided differently than §3
proposed, with reasons. The demand-projection lane takes the seam from your publication —
nothing in its amendment proceeds against assumed field names.

## Non-claims

A prompt, not an edit; grants no authority outside the receiving lane's own; not validation,
readiness, acceptance, or ECR ratification; does not redesign cutoff posture, ECR fields, or
the archive adapter's capture mechanics; the demand-projection consumption policy and ECR
binding remain their own lanes' work.
```

```text
orca_start_preflight (authoring lane, 2026-06-11):
  agents_read: yes
  overlay_read: yes
  source_pack: custom (prompt-orchestration, artifact-folders, artifact-roles, source-loading;
    ECR SP1-3 slice plan §SP-3; verified capture/projection sources listed in §4)
  edit_permission: docs-write (this handoff artifact only)
  target_scope: docs/prompts/handoffs/capture_spine_archive_snapshot_typed_timing_handoff_prompt_v0.md
  dirty_state_checked: yes (home controlling sources clean; evidence worktree dirty — disclosed in §4)
  blocked_if_missing: none
repo_map_decision: not_needed (destination bound directly by artifact-folders)
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
```
