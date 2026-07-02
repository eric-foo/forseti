# Handoff Packet — YouTube Creator-Metric Silver Producer (build)

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (durable continuation artifact; NOT validation/readiness/authorization)
scope: >
  Commissions a fresh lane to BUILD a YouTube creator-metric Silver Vault producer that emits
  MetricObservation + MetricRollupObservation records for the 30 YouTube platform accounts, mirroring
  the merged Instagram producer's Silver-envelope discipline with zero drift from the committed YouTube
  metric seed. The reader half (re-pointing creator_profile_current onto Silver records) is a SEPARATE
  lane and is OUT OF SCOPE here.
use_when:
  - Picking up the YouTube creator-metric Silver producer build cold in a fresh lane.
  - Deciding where the YouTube producer sources its numbers (the front-loaded open decision).
authority_boundary: retrieval_only
open_next:
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/tests/unit/test_creator_metric_silver_producer.py
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json
  - orca-harness/tests/unit/test_youtube_creator_metric_seed.py
  - orca-harness/data_lake/root.py
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
stale_if:
  - origin/main advances past the compare targets below (fetch fresh first).
  - The Instagram producer (silver_metric_producer.py) or the creator_metric_silver_record_contract_v0 changes its envelope, posture, or content_hash semantics.
  - The committed youtube_shorts_fragrance_creator_metric_seed_v0.json rollup/observation shape changes.
  - A YouTube seed builder is introduced (changes the open decision below).
```

You are a fresh reader. Treat this packet as a pointer, not authority:
**confirm-don't-trust**. Re-verify every pinned commit, path, count, and claim
below against a fresh read of the live repo before acting. Work in your **own
fresh worktree off `origin/main`** — not in the sender's lane.

---

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-30 (session date stamp; verify via `git log` of this file — author clock API unavailable)
- created_by_lane: `claude/creator-profile-silver-repoint` (the READER lane — provenance only, NOT authority; this lane keeps building the reader and is NOT your lane)
- handoff_path: `docs/prompts/handoffs/youtube_creator_metric_silver_producer_build_handoff_v0.md`
- workspace: the Orca repo. Receiver works in its OWN fresh worktree/branch off `origin/main` (suggested branch `claude/youtube-creator-metric-silver-producer`).
- expected_head (origin/main at handoff time): `54167272977fe689f9c0e49adc3fd663ceb960ea` — **fetch fresh; it moves.** Contains the merged Instagram producer (PR #477).
- expected_dirty_state: this handoff file is newly created → untracked in the sender lane until committed.
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Make the creator registry source-backed & lake-aware — creator metrics derive from Silver / data-lake records so the registry stops going manually stale; the identity ledger stays identity-only.
- anchor_goal: Build a YouTube creator-metric Silver Vault producer that emits formal `MetricObservation` + `MetricRollupObservation` records for the 30 YouTube platform accounts, mirroring the merged Instagram producer's envelope discipline, with **zero drift** from the committed YouTube metric seed.
- success_signal: A producer module + unit test (using `DataLakeRoot.for_test`, no external lake) where the emitted Silver records (a) are Silver-Vault-conformant (common header, `content_hash` reproducible independently, posture/value coupling), (b) carry numbers **exactly equal** to the committed `youtube_shorts_fragrance_creator_metric_seed_v0.json` observations/rollups, (c) thread rollup→observation lineage via `derived_refs`, and (d) leave the committed view, both seeds, `materialize.py`, `validation.py`, and CI **untouched**.

## Open Decision / Fork (front-loaded — decide in scoping before building)

**Where does the YouTube producer get its numbers?** The Instagram producer reuses a real builder (`build_instagram_reels_creator_metric_seed_from_files`) that recomputes from projection files. **YouTube has no such builder** (verified: `def build_youtube…` → no matches; no `youtube_metric_seed.py`). The recompute logic exists ONLY inside `tests/unit/test_youtube_creator_metric_seed.py`. So:

- **Option 1 — extract a builder, mirror IG exactly.** Refactor the reconstruction logic in `test_youtube_creator_metric_seed.py` into a reusable `capture_spine/creator_profile_current/youtube_metric_seed.py::build_youtube_shorts_fragrance_creator_metric_seed_from_files(...)` (mirroring `instagram_metric_seed.py`), then the producer reuses it.
  - Pro: exact architectural mirror; producer derives from source review-inputs; one builder reusable by future callers.
  - Con: more work; introduces a new builder + its own no-drift test (builder output must equal the committed seed); larger blast radius.
- **Option 2 (recommended for the first reviewable slice) — wrap the committed seed JSON.** The producer reads `youtube_shorts_fragrance_creator_metric_seed_v0.json` and wraps its `metric_observations` + `metric_rollups` into Silver envelopes (no recompute).
  - Pro: smallest complete producer; no-drift is **trivially guaranteed** (the numbers ARE the committed, already-tested seed); mirrors the IG *envelope* discipline (the part that matters for Silver records).
  - Con: derives from a committed proof artifact rather than recomputing from source review-inputs — a doctrinal difference from IG. Name it as an accepted residual (upgrade trigger: if the YouTube seed needs live recompute, do Option 1).
- already off the table: **no new metric math.** Whichever option, emitted numbers MUST equal the committed YouTube seed exactly (no-drift). Do NOT compute engagement from view-only data.
- owner of the call: the receiver's implementation-scoping. Escalate to the human owner only if Option 1-vs-2 is treated as a producer-uniformity doctrine decision rather than a slice-sizing one.
- recommendation: **Option 2** for v0 (smallest complete, trivially no-drift), with a named residual + Option-1 upgrade trigger.

## Drift Guard

- **No-drift is the contract.** The producer must not introduce or recompute metric magnitudes that diverge from the committed YouTube seed. The producer test must assert equality against the committed seed's numbers (mirror `test_rollup_record_lineage_and_no_drift`).
- **Posture/value coupling (mirror IG `_assert_posture_value_coupling`).** observed ⇔ numeric value + no reason; non-observed ⇔ null value + reason. YouTube `engagement_rate` is `unavailable_with_reason` and `average_like_count`/`average_comment_count`/`posting_cadence`/`recent_velocity` are non-observed — keep them that way. **Missing ≠ zero.**
- **Fail closed (mirror IG).** Raise on a blank/absent `entity_key` native_id (`_required_subject_native_id`), on a posture/value violation, and on a missing source anchor — never emit a fake-shaped record.
- **Do NOT touch:** the committed `creator_profile_current_view_v0.json`; the YouTube or IG seed JSONs; `materialize.py`; `validation.py`; the Silver Vault record contract (data-lake-lane owned, read-only); the Instagram producer. This lane is **additive** — a new YouTube producer module + new test + YouTube coverage in a producer-owned contract.
- **Scope (mirror IG v0):** emit `MetricObservation` + `MetricRollupObservation` ONLY. NOT entity/relationship records; NOT cross-platform identity; NOT the `creator_profile_current` read-model re-point (that is the READER lane, separate).
- Identity ledger stays identity-only.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish
- overlay source-loading policy: per `AGENTS.md` → `.agents/workflow-overlay/README.md` then the overlay files it routes to (source-of-truth, source-loading, safety-rules, decision-routing). Read fresh.
- targets to enter the ladder: the seven `open_next` paths above.
- already loaded (weak orientation, not authority): the sender read all seven `open_next` files at origin/main `54167272`; re-read before any strict claim.
- must load first: the Instagram producer + its test + the IG contract (the mirror), and the YouTube seed + its test (the source).

### Earlier-decided concepts (inline gist + verify pointer)
- **Silver Vault envelope discipline** (the mirror target): common header (`record_id`, `raw_anchor`, `lane_namespace`, `producer_id`, `schema_version`, `producer_schema_version`, `content_hash`+`content_hash_basis`, `record_kind`, `payload_kind`, `producer_row_kind`, `source_family`, `source_surface`, `observed_at`, `captured_at`, `raw_refs`, `derived_refs`); `content_hash` = `sha256:` of canonical JSON excluding `content_hash` (`sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False`). Decided in: `silver_metric_producer.py` + `core_spine_v0_data_lake_silver_vault_record_contract_v0.md`. Verify before building.
- **MetricRollupObservation + `derivation` marker + posture rule**: a computed rollup may carry `observed` posture only when source-backed; every rollup carries `payload.observation.derivation` = `{kind: computed_metric_rollup, source_record_ref_kind: derived_refs, metric_posture_semantics: source_input_support_not_raw_aggregate_visibility, calculation_recipe_version: <recipe>}`. Decided in: `creator_metric_silver_record_contract_v0.md`. The YouTube producer must carry the same marker. Verify before building.
- **Producer-owned contract pattern**: the IG producer has a sibling contract doc. Sub-decision for the receiver: extend `creator_metric_silver_record_contract_v0.md` to cover YouTube, or add a YouTube sibling contract. Mirror its `artifact_role: source_capture_family_architecture_contract` + `authority_boundary: retrieval_only` header.

## Active Objective

Build and unit-test a YouTube creator-metric Silver producer (additive, new module + new test + contract coverage) that emits Silver-Vault-conformant `MetricObservation` + `MetricRollupObservation` records for the 30 YouTube accounts, numbers identical to the committed YouTube seed, mirroring the merged Instagram producer's envelope discipline. Do not re-point the read model.

## Exact Next Authorized Action

1. Fresh-read the mirror (`silver_metric_producer.py`, `test_creator_metric_silver_producer.py`, `creator_metric_silver_record_contract_v0.md`) and the source (`youtube_shorts_fragrance_creator_metric_seed_v0.json`, `test_youtube_creator_metric_seed.py`).
2. Run Orca implementation-scoping. Resolve the **Open Decision** (Option 1 vs 2) AND the **anchoring question** (see Blockers): does each YouTube observation carry a usable `source_packet_id_or_none` for the Silver `raw_anchor` path segment, and what `raw_refs` shape is honest given YouTube carries no `raw_anchor` dict?
3. Build the producer + unit test (`DataLakeRoot.for_test`) + producer-owned contract coverage; prove no-drift vs the committed YouTube seed (assert equality of observation/rollup numbers).
4. Validate: new test green; full creator suite green; `run_creator_profile_current_materialize.py --check` still up to date (committed view untouched); doc-hygiene gates pass for any new `.md` (see Commands).
5. Commit / push / PR per the Orca per-lane PR flow (`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`). Push/PR are owner-gated by `settings.json` prompts.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`, `CLAUDE.md`, `.agents/workflow-overlay/README.md` — read fresh.
- Overlay authority: `.agents/workflow-overlay/*` (source-of-truth, source-loading, safety-rules, decision-routing).
- Source-read ledger (compare targets at origin/main `54167272` unless noted; **fetch fresh**):
  - `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
    - Role: the mirror — envelope discipline, `derivation` marker, fail-closed helpers, `_content_hash`/`_canonical_json_bytes`/`_json_bytes`, `append_record` usage.
    - Load-bearing: yes. Compare target: HEAD `54167272`; reread-required.
  - `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
    - Role: the test template — `for_test` lake, independent `_content_hash` reproduction, posture coupling, derived_refs lineage, no-drift assertions, fail-closed native_id test.
    - Load-bearing: yes. Compare target: HEAD `54167272`; reread-required.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
    - Role: producer-owned contract (MetricObservation/MetricRollupObservation + derivation + posture rule) to mirror/extend for YouTube.
    - Load-bearing: yes. Compare target: HEAD `54167272`; reread-required.
  - `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`
    - Role: the YouTube source of numbers (Option 2 input / Option 1 equality target). 30 accounts, 196 observations, 30 rollups.
    - Load-bearing: yes. Compare target: counts asserted in `test_youtube_creator_metric_seed.py:142`; reread-required for field shapes.
  - `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`
    - Role: documents the YouTube seed shape + reconstruction logic (Option 1 extraction source). Provenance fields posture at lines 161-170 (note: NO `raw_anchor` in `portable_provenance_fields`, unlike IG).
    - Load-bearing: yes. Compare target: HEAD `54167272`; reread-required.
  - `orca-harness/data_lake/root.py`
    - Role: `DataLakeRoot` writer — `append_record(subtree="derived", raw_anchor, lane, record_id, data)`, `for_test`. `raw_anchor`/`lane`/`record_id` must satisfy `_SAFE_SEGMENT` (`[A-Za-z0-9][A-Za-z0-9._-]{0,127}`).
    - Load-bearing: yes. Compare target: HEAD `54167272`; reread-required.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
    - Role: Silver envelope authority (READ-ONLY; data-lake lane owns it — do not edit).
    - Load-bearing: yes. Compare target: reread-required.
- Source gaps / not-proven: whether YouTube observations carry a usable source anchor for Silver records (see Blockers) — **not proven**; must be resolved in scoping.

## Current Task State

- Completed (other lanes): Instagram producer + its contract + test merged to main (PR #477). Reader lane (`creator_profile_current` re-point) in progress separately.
- Not started: the YouTube producer (this commission).

## Workspace State

- Branch: receiver creates `claude/youtube-creator-metric-silver-producer` (or similar) off `origin/main`.
- Head: `origin/main` = `54167272` at handoff (fetch fresh).
- Target files (to CREATE): `orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py` (name receiver's choice; or a shared `silver_metric_producer.py` extension — scoping decides), `orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`, plus YouTube coverage in a producer-owned contract `.md`. Option 1 additionally creates `youtube_metric_seed.py`.
- Related lanes: `claude/creator-profile-silver-repoint` (READER — independent, parallel, not your lane).

## Frozen Decisions

- v0 emits `MetricObservation` + `MetricRollupObservation` only (no entity/relationship records); subject carried as a self-describing `entity_key` ref. Evidence: IG producer scope. Consequence: no PlatformAccountEntity/content-object/relationship records in this slice.
- No-drift vs the committed YouTube seed is mandatory. Evidence: anchor_goal + IG precedent. Consequence: the producer test must assert numeric equality with the committed seed.
- The read-model re-point is NOT in this lane. Evidence: it is the separate READER lane. Consequence: do not modify `materialize.py`/`validation.py`/the committed view.

## Mutable Questions

- Option 1 (extract builder) vs Option 2 (wrap committed seed)? — resolved in scoping; recommend Option 2 for v0.
- Extend `creator_metric_silver_record_contract_v0.md` for YouTube, or add a YouTube sibling contract? — resolved in scoping.
- Producer module: new `youtube_silver_metric_producer.py` vs generalizing the existing `silver_metric_producer.py`? — resolved in scoping; prefer a sibling module to keep the merged IG producer untouched unless a clean shared core emerges.

## Superseded / Dangerous-To-Reuse Context

- The phrase "follow the IG producer" must NOT be read as "reuse a YouTube seed builder" — **none exists.** Only the envelope discipline transfers directly; the number-source is the open decision above.
- Do NOT copy IG's `raw_refs`/`raw_anchor` field handling blindly: the IG observation carries a `raw_anchor` dict (file_id/relative_packet_path/sha256/hash_basis); the YouTube seed's `portable_provenance_fields` excludes `raw_anchor`. The YouTube `raw_refs` shape must be re-derived honestly from what the YouTube seed actually carries.

## Commands And Verification Evidence

- Scoped tests (run from `orca-harness/`):
  ```bash
  python -m pytest tests/unit/test_youtube_creator_metric_silver_producer.py tests/unit/test_youtube_creator_metric_seed.py tests/unit/test_creator_profile_current_static_view.py
  ```
  Result: not run (producer not built yet) — this is the receiver's target.
- Committed view unchanged (run from `orca-harness/`):
  ```bash
  python runners/run_creator_profile_current_materialize.py --check
  ```
  Expected: "up to date" (this lane must not change the committed view).
- Doc-hygiene gates for any new `.md` (run `--strict` from repo root; the FULL set — `check_map_links` alone is NOT enough): `check_map_links`, `header_index`, `check_csb_scanning_artifact --diff origin/main`, `check_ontology_ssot`, `check_ontology_tag_validity`, `check_ontology_drift`, `check_deletion_evidence`, `check_dcp_receipt`. New durable `.md` needs a valid header with `authority_boundary: retrieval_only`. Authority: `.github/workflows/ci.yml`.

## Blockers And Risks

- **Anchoring (load-bearing, reread-required).** The Silver record's `raw_anchor` path segment + `raw_refs` come (in IG) from `source_packet_id_or_none` and a `raw_anchor` dict. The YouTube seed's `portable_provenance_fields` **excludes `raw_anchor`**, and whether `source_packet_id_or_none` is populated per YouTube observation is **not verified here**. Action: inspect the actual `youtube_shorts_fragrance_creator_metric_seed_v0.json` observation rows. If no usable packet id exists, decide an honest YouTube anchor (e.g., a YouTube-appropriate raw anchor or a non-observed provenance posture) in scoping — do NOT fabricate one. `raw_anchor` must satisfy `_SAFE_SEGMENT`.
- **Posture surface.** YouTube observes only `view_count`; engagement/like/comment rollups are non-observed. Verify the producer carries non-observed postures with reasons and null values (missing ≠ zero), and that the `derivation` marker is still attached to the rollup.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: origin/main HEAD (moves); the seven `open_next` files at the current HEAD; the YouTube seed counts (30/196/30) and per-observation provenance fields; the IG envelope helpers; `DataLakeRoot.append_record` segment rules.
- Compare targets: HEAD `54167272` (fetch fresh); `test_youtube_creator_metric_seed.py:142` (counts), `:161-170` (provenance posture), `:259-260` (engagement non-observed).
- Load outcomes: `REUSE` only after re-verifying the mirror + source; `STALE_REREAD_REQUIRED` if main advanced; `BLOCKED_UNVERIFIABLE` if the anchoring question cannot be resolved from the seed/source.

## Do Not Forget

- The number-source is an open decision, not "reuse a builder" — there is no YouTube builder. Resolve it in scoping before building.
- This lane is additive and must leave the committed view, both seeds, `materialize.py`, `validation.py`, and CI untouched.
