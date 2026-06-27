# IG Creator Grid Capture To Projection ECR Cleaning Handoff

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet
scope: >
  Cold-reader handoff from the Instagram public creator-grid capture lane to downstream
  Projection, Evidence Candidate Record, and Cleaning only. Reels are the high-cadence traction route;
  static/profile-grid capture is a lower-cadence companion surface. TikTok/YouTube method
  transfer was split into docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md.
use_when:
  - Continuing IG creator-grid downstream Projection, ECR, or Cleaning work.
  - Checking which IG reels and static/profile-grid capture facts may be carried mechanically downstream.
  - Preventing ad, sponsorship, demand, bot, credibility, or action-use conclusions from entering non-Judgment lanes.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - IG creator-grid runner, parser, row identity, source surfaces, static-row handling, or candidate preservation changes.
  - Projection doctrine changes mechanical-only, no-salience, loss-ledger, or carry-or-residualize rules.
  - ECR/SCR carry-or-residualize, reference-never-merge, or per-kind grain discipline changes.
  - Cleaning gains owner-authorized semantic classification authority.
```

## Load Contract

- packet_version: workflow-handoff-v1
- mode: split-downstream-lanes
- created_at: 2026-06-22T20:48:29.4850791+08:00
- created_by_lane: Codex IG public creator-grid capture closeout lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`
- split_peer_packet: `docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md`
- expected_branch: `codex/ig-reels-capture-spine`
- expected_head_before_split_edit: `088b8d39`
- expected_dirty_state_before_split_edit: dirty working tree with unrelated pre-existing modified/untracked files; this split must touch only the two docs/workflows handoff packets unless the current user redirects.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Refresh 2026-06-25 (read first; supersedes the drifted facts below)

This packet was authored 2026-06-22 and is structurally current -- the lane boundaries,
drift guards, and Projection -> ECR -> Cleaning routing still hold. Several facts have
drifted; trust this block over the stale originals below, and run the confirm-don't-trust
pass over both.

- **Capture output (bio_links + JSON-sourced pinned) is now MERGED in `main` (PR #378).**
  - `creator_profile_snapshot.bio_links`: list of public link-in-bio `{title, url}` destinations
    (web_profile_info `bio_links`, `lynx_url` fallback), not just `bio_links_count`.
  - per-candidate `pinned_on_clips_tab` / `pinned_on_timeline` on `IgReelsJsonCandidate`:
    reels-tab pin = `/clips/user` `clips_tab_pinned_user_ids`; main-grid/timeline pin =
    `timeline_pinned_user_ids` / web_profile_info `pinned_for_users`; non-empty list = pinned,
    empty = not, absent = null. The pin is NOT in the rendered DOM (no accessible marker), only
    in passive JSON. Projection carries these mechanically -- pinned is a source-visible flag,
    NOT a credibility/quality/demand judgment.
- **A second capture-lane change is in PR #383 (reader + pinned identification).**
  - Reader: `DEFAULT_IG_REELS_SETTLE_SECONDS` widened 2.5 -> 4.0s so the passive `/clips/user`
    XHR more reliably lands before the DOM snapshot (a 2026-06-25 esthertakumi probe joined
    12/12 rows; an earlier 2/12 miss was a transient race). A row that still misses is the
    honest `no_passive_json_join_for_shortcode` gap, never faked.
  - Pinned identification: a packet-level `pinned_inference` summary cross-checks the explicit
    `pinned_on_clips_tab` flag against a grid-order recency-inversion heuristic
    (`infer_pinned_shortcodes_by_recency`), scoped to the reels tab. Live finding: `/clips/user`
    is purely recency-ordered and never hoists pins (inversion keys on GRID order, not feed
    order); main-grid/`timeline` pins are held out of the reels summary. The reels-tab pin
    POSITIVE remains inferred, not yet observed on a reels-pinned profile. Projection carries
    `pinned_inference` mechanically; it is a source-visible cross-check, not a verdict.
- **Momentum/traction is PRE-GOLD -- not gold, not Capture.** Per the Data Lake medallion
  contract (`core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`): the mechanical
  delta over repeated captures is SILVER; a threshold crossing ("Spike Alert / Movement Alert /
  usual-range threshold crossed") is a PRE-GOLD mechanical candidate record -- source-object
  movement is the named first precomputed candidate class -- written append-only and keyed to
  raw. Judgment alone owns the GOLD interpretation (real demand / credible / artificial). The
  momentum/Spike-Alert lane therefore lives DOWNSTREAM of Projection, not in Capture, and its
  records MUST use usual-range vocabulary, never viral/suspicious/bot/paid. Capture's only job
  is to emit clean, durably-keyed timepoints (numeric_id + shortcode + capture_timestamp +
  typed posture), which it now does.
- **SCR is deprecated/dormant (`#375`).** The Signal Content Record (`orca-harness/signal_content/`)
  is retained but dormant as a default pre-Judgment layer; the default route is evidence pack
  -> Judgment-authored signal interpretation. Read every "ECR/SCR" pairing below as
  "ECR (SCR dormant -- do not build an SCR consumer unless explicitly revived; see
  `docs/workflows/ecr_spine_submap_v0.md`)".
- **Durability/cadence is the next ops lane (NOT Capture, NOT lake).** A scaled-monitoring
  rate/cadence + graceful-degradation envelope is required before a real creator panel runs;
  it is owned by a new ops/scheduler lane (the lake contract excludes scheduling/retry, and the
  runner is per-invocation and already fails closed on blocks). See
  `docs/decisions/ig_reels_capture_cadence_durability_doctrine_v0.md`.
- **State / ledger.** The capture lane is merged in `main` (well past this packet's
  `expected_head 088b8d39`); the source-ledger SHA256s below (IG runner/parser/capture/tests/spec
  and the ECR submap, which `#375` changed) are SUPERSEDED -> treat as `reread-required` against
  current `main` + PR #383 before any strict claim.

## Authoring Preflight

- output_mode: `file-write`; destination `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`.
- template_kind: `handoff`.
- edit_permission: `docs-write`; target scope is this handoff packet only.
- reviews: no formal review verdict is created by this packet.
- doctrine_change: none intended; this is a handoff split, not a rule change.
- downstream_destination: receiving lanes write their own scoped plan, code patch, review report, or blocked result under their lane's current authorization.

## Goal Handoff

- long_term_goal: Build Orca social-source capture and downstream evidence plumbing that can monitor public creator/content traction without confusing raw capture, Projection, ECR, Cleaning, or Judgment responsibilities.
- anchor_goal: Route IG creator-grid learnings into the correct downstream lanes: Projection gets mechanical source-view enforcement, ECR gets by-key receipt/integrity/content boundaries, and Cleaning gets non-destructive normalization mechanics.
- success_signal: A cold downstream lane can re-open the named sources and continue only its lane's bounded work without re-learning the IG DOM/JSON findings or smuggling ad/sponsorship/demand/integrity judgment into Capture, Projection, ECR, or Cleaning.

## Open Decision / Fork

- decision: Whether to implement items 1-3 as one Projection-first slice or as parallel Projection, ECR, and Cleaning slices.
  - options: Projection-first adapter and tests; or parallel lane plans before code.
  - already constrained / off the table: no ad, sponsorship, bot, paid-comment, demand, credibility, integrity, Decision Strength, or Action Ceiling conclusions in Projection, ECR, Cleaning, or Capture.
  - trade-offs: Projection-first protects the row contract fastest; parallel planning reduces lane-mismatch risk but adds coordination latency.
  - owner of the call: current Orca owner / current receiving lane user instruction.
  - recommendation and why: Projection-first, then ECR/Cleaning consumption checks. Items 1-3 are most directly enforced at the projection row boundary.

## Drift Guard

- Static/reels separation remains Capture-owned. Projection/Cleaning consume declared `source_surface`; they do not decide capture cadence or mix static rows into reels traction.
- Projection is mechanical and source-visible only. It may carry captions, timestamps, counts, source surfaces, row identity, and mechanical mention counts; it must not decide meaning.
- ECR/SCR references by key and carries/residualizes; it does not author meaning from capture prose or merge projection fields into posture fields.
- Cleaning may normalize and cluster mechanically, but sponsorship, credibility, artificial-amplification, exclusion, demand, and action-support effects stay Judgment-owned.
- TikTok/YouTube work is out of scope for this packet. Use the split peer packet instead.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`.
- targets to enter the ladder:
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md`
  - `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
  - `docs/workflows/ecr_spine_submap_v0.md`
  - `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`
  - `orca-harness/source_capture/ig_reels_grid.py`
  - `orca-harness/source_capture/ig_reels_grid_capture.py`
- already loaded, weak orientation only: AGENTS, overlay README, source-loading, artifact-folders, decision-routing, prompt-orchestration, workflow-prompt-orchestrator skill, the current combined packet, IG spec, projection doctrine, ECR submap, Data/Cleaning boundary, capture playbook/recon index headings, YouTube recon/playbook, and relevant IG runner/parser/test hashes were read on 2026-06-22.
- must load first before strict/actionable steps: AGENTS.md, overlay README, source-loading, this packet, IG spec, and the owner source for the receiving lane.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors

- IG high-cadence public monitoring default is one `/reels/` page load with no hover, click, OCR, item-page fan-out, comment-text capture, or media-byte preservation.
  - verify pointer: IG spec, SHA256 `09E3149A332625F3FDF9A4AFABD560CED07AFFFF1DA95F35EE3CF93C951CCCD9`.
- Static/profile-grid capture is a lower-cadence companion surface for onboarding, refresh, and escalation. Static `/p/` rows are not part of the reels traction series; static `view_count` is `not_applicable`, not missing.
  - verify pointer: IG spec Static Comparison Policy and current runner/parser files.
- Projection may carry raw counts, captions, timestamps, labels, and baselines, but must not emit interpretation such as anomaly, independence, demand, credibility, or action labels.
  - verify pointer: Projection doctrine, SHA256 `BE22FD65CB9D6D31682D74847631C51E766D01BD0A86063B65585CC994F6CDC0`.
- ECR/SCR records are siblings over raw, reference by key, and follow carry-supplied-or-residualize; they never author interpretive values from packet prose.
  - verify pointer: ECR submap, SHA256 `B1F2BD6D10B05D53F22052349784B3C0802E47A8A155AC81E43CE9CCDD2494A1`.
- Cleaning owns non-destructive transformation mechanics only; Judgment owns credibility, exclusion, demand, integrity effect, Decision Strength, and Action Ceiling.
  - verify pointer: Data/Cleaning boundary, SHA256 `3D50EEA84071490B563A36ABE37F974654A820274EFD767FFB37FFAB05F2509D`.

## Active Objective

Transfer IG creator-grid capture closeout into downstream Projection, ECR, and Cleaning work without lane blur. TikTok/YouTube method transfer is intentionally removed from this packet and lives in the split peer packet.

## Exact Next Authorized Action

1. Projection lane: source-load this packet, the IG spec, and the projection doctrine; scope or implement a bounded IG creator-grid projection adapter that emits only mechanical source-visible rows: raw refs, row identity, source surfaces, selected fields, join status, selection limitations, candidate disagreements, caption anchors, timestamps, and mechanical mention frequencies.
2. ECR lane: source-load this packet and `docs/workflows/ecr_spine_submap_v0.md`; decide whether existing ECR/SCR consumers need references to the projection row handle or whether packet/slice keys are sufficient. Do not merge projection fields into ECR posture fields.
3. Cleaning lane: source-load this packet and the Data/Cleaning boundary; define how caption/product/brand strings and repeated mention groups may be normalized or clustered without losing originals or deciding paid/sponsored/campaign meaning.
4. Capture-owner note: static/profile-grid comparison is a lower-cadence companion source surface; this downstream packet does not implement that companion runner or authorize mixing static rows into the reels traction series.

## Code-Enforceable Items For This Downstream Packet

- Projection adapter, when built, must preserve row identity, `source_surface`, candidate counts, chosen-source policy, join status, and selection limitations.
- Projection field names must stay mechanical: examples such as `caption_surface_mention_frequency` are allowed; names such as `sponsored_ad_detected`, `botter`, `fake_engagement`, `demand_signal`, or `credibility_score` are not allowed outside Judgment-owned work.
- ECR/SCR consumers must reference packet/projection keys rather than copying projection rows into integrity posture fields.
- Cleaning transforms must preserve originals and emit non-destructive ledgers for normalized strings, clusters, and duplicates.
- Static `view_count = not_applicable` must remain enforced before the lower-cadence static comparison surface is allowed to feed downstream analysis.

## Behavioral Items To Refresh Outside Code Claims

- IG DOM hidden numeric ordering and class names.
- Passive JSON endpoint/key availability and field names.
- Whether page-load JSON carries more media rows than visible DOM under a given viewport, zoom, browser bucket, or route state.
- Whether source-visible paid-partnership, affiliate, or sponsor fields are present, absent, false, or moved. Absence or false values are not proof of not-ad.
- Whether repeated brand/product mentions are paid sponsorship, organic product discussion, campaign behavior, or content-farm cadence. Projection may count mentions; Cleaning may normalize entities; Judgment decides meaning.

## Authority And Source Ledger

- Repository instructions current hash: `4296E7617D8B2675881780CD7BE0704A00DCB17ADF7758243008DE956070940B`.
- Overlay authority:
  - `.agents/workflow-overlay/README.md`, SHA256 `7A30709D6011BD3F6458E926570B7164B91C7F3BF8BAE7DBD5A612A08DE81FDA`.
  - `.agents/workflow-overlay/source-loading.md`, SHA256 `58994CA788F1754DEA49277750B64C592DE0A4B7B19DBF495CE675DDB9C08181`.
  - `.agents/workflow-overlay/artifact-folders.md`, SHA256 `42D4F554DAF4BE6F0A4A9BCBE3C67FD74EEFCC063FC72B03E53E11242EDC7AE9`.
  - `.agents/workflow-overlay/decision-routing.md`, SHA256 `8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E`.
- Target source ledger:
  - IG spec: SHA256 `09E3149A332625F3FDF9A4AFABD560CED07AFFFF1DA95F35EE3CF93C951CCCD9`, load-bearing yes, reread before capture/projection claims.
  - Projection doctrine: SHA256 `BE22FD65CB9D6D31682D74847631C51E766D01BD0A86063B65585CC994F6CDC0`, load-bearing yes, reread before projection implementation or review.
  - ECR submap: SHA256 `B1F2BD6D10B05D53F22052349784B3C0802E47A8A155AC81E43CE9CCDD2494A1`, load-bearing yes, reread before ECR/SCR changes.
  - Data/Cleaning boundary: SHA256 `3D50EEA84071490B563A36ABE37F974654A820274EFD767FFB37FFAB05F2509D`, load-bearing yes, reread before Cleaning or cross-layer claims.
  - IG runner: SHA256 `05AAB060C464DE6A78B3A2BFFF9D1DE62DFF10BDEA8A33B14377E0BCC3060EEA`, load-bearing yes for current implementation state.
  - IG parser: SHA256 `E56326B75616E78790A8EB85A51680C2801C7420604BF0D1FE4158093C7CEB1F`, load-bearing yes for row/candidate shape.
  - IG browser capture: SHA256 `E585BB71F2BF1E8083F1EC663F9FFE08FF886609FA23B3A6BDB1A8CB2E5DE54F`, load-bearing yes for capture privacy and passive JSON mechanics.
  - Focused parser tests: SHA256 `AE99183CC88124A20175F2A2BE69D7ECE9E0C03FFA9851ADE87818A3EAED977B`.
  - Focused runner tests: SHA256 `4848F8538421C4CB57683C3580B6FD1812171A2BB0E5C371AC244E60814B3B1B`.
- Source gaps: no downstream IG creator-grid projection adapter was implemented in this split; ECR/Cleaning consumption of IG projection rows was not implemented or reviewed in this split.
- Not-proven boundaries: no scaled monitoring durability/rate envelope; no platform-stability claim; no ad/sponsorship/bot/demand/credibility classification.

## Current Task State

- Completed before this split:
  - IG public `/reels/` capture runner and parser exist on the PR branch.
  - IG spec records runner binding, static comparison policy, and lane wrap-up boundary.
  - Focused parser/runner/source-capture tests passed before the docs-only split.
  - One proxy-backed live capture for `jeremyfragrance` was admitted to a temp data-lake root; treat it as a probe artifact, not production proof.
- Partially completed:
  - Projection requirements are identified but not implemented for creator-grid rows.
  - ECR/Cleaning consumption boundary is identified but not patched.
- Broken or uncertain:
  - IG DOM hidden numeric ordering remains behavioral and must be refreshed.
  - Passive JSON surfaces and fields remain behavioral; endpoint/key stability is not a correctness claim.
  - Separate static/profile-grid companion runner is deferred; policy and row separation are recorded.

## Commands And Verification Evidence

- Previous code validation before this docs-only split:
  - `python -m py_compile source_capture\ig_reels_grid.py runners\run_source_capture_ig_reels_grid_packet.py tests\unit\test_ig_reels_grid.py tests\unit\test_source_capture_ig_reels_grid_packet.py` passed in `orca-harness`.
  - `python -m pytest tests\unit\test_ig_reels_grid.py tests\unit\test_source_capture_ig_reels_grid_packet.py tests\unit\test_source_capture_ig_calls_packet.py tests\unit\test_run_source_capture_packet_lake.py -q` reported `35 passed`.
- Re-run target: rerun the focused tests before relying on code behavior after any code edit. For a docs-only split, `git diff --check` over the touched packet files is the relevant local check.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - branch/head and dirty state;
  - IG spec lane boundary and static policy;
  - Projection doctrine mechanical-only/no-salience rules;
  - ECR submap carry-or-residualize/reference-never-merge rules;
  - Data/Cleaning boundary and Cleaning vs Judgment split;
  - runner/parser/test file contents if implementation continues;
  - test results if code changes are made.
- Compare target for each:
  - hashes in Authority And Source Ledger;
  - fresh `git status --short --branch`;
  - fresh `git rev-parse --short HEAD`;
  - rerun tests when code changes are relevant.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts match; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional or non-load-bearing facts drifted; reuse verified lane boundaries and refresh the rest.
  - `STALE_REREAD_REQUIRED`: material source drifted but can be reread and re-derived.
  - `BLOCKED_DRIFT`: drift conflicts with scope, ownership, or dirty-state safety.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim lacks a compare target and cannot be re-derived.
- Sources that must be reread if drift is detected:
  - IG spec, Projection doctrine, ECR submap, Data/Cleaning boundary, and affected runner/parser/test files.

## Do Not Forget

Projection can count and carry; Cleaning can normalize and cluster mechanically; ECR can reference and residualize; Judgment decides what it means. Static comparison cadence and capture remain Capture-owned. TikTok/YouTube inherit generic method through the split peer packet, not through this downstream IG packet.
