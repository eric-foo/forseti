# Fragrantica Capture To Data Lake Projection ECR Cleaning Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet
scope: Cold-reader handoff from Fragrantica capture diagnosis to Data Lake, Mechanical Source Projection, ECR, and Cleaning lanes.
use_when:
  - Classifying the Fragrantica packet under Data Lake without misrouting it as retail PDP.
  - Scoping Fragrantica mechanical projection, ECR receipt, or Cleaning input.
  - Checking Fragrantica current-window completeness limits before downstream work.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_fragrance_native_database_live_probe_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - Fragrantica route, review DOM, login wall, packet manifest, or Data Lake raw/derived contracts change.
  - A later packet captures the full Fragrantica review archive or supersedes this current-window packet.
```

## Load Contract

- packet_version: workflow-handoff-v1
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-06-29T03:35:43+08:00
- created_by_lane: Codex fragrance-native live-probe lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrance-native-live-probe`
- handoff_path: `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
- expected_branch: `codex/fragrance-native-live-probe`
- expected_head: `b4641d65`
- expected_dirty_state_before_handoff_file: clean worktree at `b4641d65`.
- expected_dirty_state_after_this_turn: modified `docs/research/orca_fragrance_native_database_live_probe_v0.md`; untracked `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Authoring Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 handoff plus Data Lake / Projection / ECR / Cleaning targets
  edit_permission: docs-write
  target_scope:
    - docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
    - docs/research/orca_fragrance_native_database_live_probe_v0.md
  dirty_state_checked: yes
prompt_contract:
  output_mode: file-write
  template_kind: handoff packet, not courier prompt
  edit_permission_targets_branch: docs-write; docs/workflows and docs/research only; branch codex/fragrance-native-live-probe
  doctrine_change: none intended
cynefin_routing:
  smallest_complete_outcome: durable Fragrantica-to-Data-Lake handoff plus separate Parfumo diagnosis addendum
  regime: mixed; handoff is complicated source-bound work, Parfumo diagnosis is complex probe work
  allowed_next_move: Data Lake classification/projection scoping from named packet refs
  disallowed_next_move: runtime crawler, full archive crawl, ECR/Cleaning implementation, or Judgment/demand claims from this packet
```

## Current Route Addendum — Rendered Content Mode (2026-07-18)

The historical direct packet facts below remain evidence, but they no longer
describe the standard artifact posture for the two rendered slices:

- `run_fragrantica_mgt_capture.py` still creates three packets. Direct HTTP
  (`fragrantica_product_page_direct_http`) remains raw and unchanged as the
  canary. The initial-viewport and deep-scroll CloakBrowser surfaces default to
  `content`; `sample` and `raw` remain explicit modes.
- Rendered content records use
  `fragrantica_rendered_current_window_content`,
  `fragrantica_rendered_current_window_content_v1`, and
  `fragrantica_rendered_current_window_parser_v1`. The existing projection
  method/version remain unchanged because raw/content row and Cleaning
  semantics are equivalent.
- Successful content projection retains `content_record.json`,
  `content_capture_metadata.json`, the CloakBrowser snapshot metadata, and the
  active-capture screenshot. Rendered DOM and visible text are hashed then
  discarded. Projection failure preserves every captured artifact and returns
  exit code `4`.
- `fragrantica_projection.py` prefers a valid content record and binds rows and
  bindings to the actual packet with JSON-pointer anchors. Raw and historical
  packets retain the raw parser. Fragrantica Cleaning catch-up admits all three
  Fragrantica surfaces and consumes content records without rereading discarded
  DOM/text.
- Live BR540 acceptance on 2026-07-18 produced parser-fit `match` for both
  rendered sample packets; raw/content Projection and Cleaning were equivalent.
  Initial rendered packet bytes fell from 1,081,579 to 538,469, and deep-scroll
  bytes fell from 5,430,341 to 1,024,476. Content packets retained screenshots,
  contained no rendered DOM/text, and retained both input hashes. The live
  screenshots showed the requested product page and footer respectively, with
  no cookie or access overlay.

This flips only the two rendered Fragrantica surfaces. It does not retire the
direct-HTTP canary, the shared projection runner for raw/sample/legacy packets,
or the login boundary on the full review archive.

## Goal Handoff

- long_term_goal: Build Orca fragrance-native source capture and downstream evidence plumbing that can monitor specialist fragrance precursor demand without blurring raw capture, Data Lake, Projection, ECR, Cleaning, or Judgment responsibilities.
- anchor_goal: Transfer Fragrantica current-window capture facts to Data Lake, Projection, ECR, and Cleaning lanes with the right source-family classification and explicit completeness limits.
- success_signal: A cold downstream lane can classify the Fragrantica packet under `fragrance_native_database`, preserve the raw-key relationship, scope projection/ECR/Cleaning work, and avoid treating the current-window 210/310 review-card evidence as a complete Fragrantica review archive or as retail PDP.

## Open Decision / Fork

- decision: Whether the existing Fragrantica packet under `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV` should be accepted as the raw packet to sync, held/quarantined as an environment-root accident, or replayed as a fresh packet.
  - options: validate/admit existing packet; hold/quarantine and replay later; replay immediately under a deliberate Data Lake run.
  - already constrained / off the table: mutating raw in place; encoding source/date/product/completeness in the raw path; classifying Fragrantica as `retail_pdp`; treating current-window reviews as full archive.
  - recommendation and why: validate the existing packet first. If manifest/hash/admission checks pass, keep it as the observed raw packet fact and classify by manifest metadata. If routine provenance must be cleaner, replay to a new packet and mark this one as probe evidence.

## Drift Guard

- Fragrantica belongs to `fragrance_native_database`, not `retail_pdp`; otherwise merchant/verified-purchase/offer semantics leak into an enthusiast database.
- Raw physical path is opaque by-packet fanout only; no source family, date, URL, product, identity, content hash, or dedupe meaning belongs in the path.
- Current-window Fragrantica reviews are partial: direct HTTP has 210 review cards; CloakBrowser scroll diagnosis saw 310 unique review IDs; visible text still showed `Reviews (3.9K)` and the full-archive login prompt.
- No auth-gate bypass: full archive access in observed route requires login; use only own-entitled/manual route if owner later authorizes it.
- No ECR, Cleaning, Judgment, buyer-proof, demand, credibility, or commercial-readiness claim is created by this handoff.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`.
- targets to enter the ladder: this packet; `docs/research/orca_fragrance_native_database_live_probe_v0.md`; the Fragrantica direct receipt/manifest under `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV`; the CloakBrowser diagnostic receipt/manifest under `orca-harness/_test_runs/fragrance_native_20260629/fragrantica_cloakbrowser_scroll_diag_packet`; Data Lake raw/storage contracts; projection doctrine; ECR submap; Data/Cleaning boundary.
- already loaded, weak orientation only: AGENTS context supplied by user; overlay README/source-loading/decision-routing/prompt-orchestration/retrieval-metadata/artifact-folders; targeted Data Lake, projection, ECR, Cleaning sources; packet receipts/manifests; Fragrantica raw parse; Parfumo live endpoint probes.
- must load first before strict/actionable steps: AGENTS.md/current user instruction, overlay README/source-loading, this packet, Fragrantica packet receipts/manifests, Data Lake raw admission and storage contracts, and the receiving lane owner doc.
- load rule: receiver re-runs progressive source loading per overlay; this packet only seeds the ladder.

### Earlier-decided concepts and behaviors

- Data Lake is raw-truth shared foundation and does not own source capture execution, projection semantics, ECR, Cleaning, or Judgment. Verify in `orca/product/spines/data_lake/README.md` before strict lake ownership claims.
- Raw packet paths are `raw/<packet_shard>/<packet_id>/`, with shard from `sha256(packet_id)[:3]`, and carry no semantic meaning. Verify against raw-admission contract SHA256 `582D7612CC1C89CE8D92E71189AEDEEB749ADDE5DB13F9265DF77A79620282D7`.
- New source-family payloads target Attachment Records or derived/projection metadata, not new direct lake-core fields. Verify against storage contract SHA256 `0248FA723972AEFFD04220876229F1E116F6BB9855391855ABFBC05C2F98B262`.
- Projection is a mechanical re-derivable view over raw; carry or residualize, never author from prose. Verify against projection doctrine SHA256 `81AE300C0AC7A26641771C2A11C9E0CF690A7C8C2429228D73F036586583F01D`.
- ECR and Cleaning are sibling downstream lanes over raw/projection refs; they do not repair missing archive coverage or decide meaning. Verify against ECR submap SHA256 `C945C079D06F4D15A487BB99D9CB3431E1A8CF5AFDA1679424D1842E6C596F60` and Data/Cleaning boundary SHA256 `3D50EEA84071490B563A36ABE37F974654A820274EFD767FFB37FFAB05F2509D`.

## Active Objective

Transfer Fragrantica current-window capture diagnosis into the right Data Lake, Projection, ECR, and Cleaning continuation lane without turning a fragrance-native enthusiast database into retail PDP and without overstating review completeness.

## Exact Next Authorized Action

1. Data Lake lane: re-open the Fragrantica direct packet receipt/manifest, verify hashes and raw-admission criteria, then decide accept vs quarantine/replay. Keep physical path by packet shard; classify semantically by manifest metadata: `source_family=fragrance_native_database`, `source_surface=fragrantica_product_page_direct_http`, platform `fragrantica` in projection/attachment metadata, object type `fragrance_product`, product id `33519`, and source locator URL.
2. Projection lane: scope a `fragrance_native_database` mechanical projection over the raw packet. Minimum row groups: product snapshot, review-card current-window rows, review-tab/source-order facts, aggregate rating/performance facts, and residuals/loss ledger for archive incompleteness, no linked-media preservation, no review-attached-photo proof, and no full archive.
3. ECR lane: consume only raw/projection refs and source-visible/residualized facts. Do not merge projection fields into ECR posture fields and do not author scent meaning, quality, demand, credibility, or completeness from prose.
4. Cleaning lane: define non-destructive normalization only: review text cleanup, source-language/string normalization, mechanical length bins, author/display-name normalization with raw refs, and source-visible rating/performance enum carry. Do not decide sentiment, credibility, duplicate effect, independence, demand, exclusion, or action support.
5. Stop if the direct packet is missing, hashes fail, manifest source family/surface differs, or lake authority changed.
## Where To Classify It Under Data Lake

- Raw physical home: `raw/<packet_shard>/<packet_id>/`, currently observed as `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV`. The `930` shard is physical fanout only and must not be read as source, date, product, or classification.
- Lake key: `packet_id=01KW7SGXRZHFTS372X391Z8GHV`. Re-captures get new packet IDs; do not dedupe by URL into the same raw path.
- Manifest metadata classification:
  - `source_family: fragrance_native_database`
  - `source_surface: fragrantica_product_page_direct_http`
  - source locator: `https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html`
- Recommended projection/Attachment Record metadata, not lake-core path grammar:
  - `source_platform: fragrantica`
  - `source_object_type: fragrance_product`
  - `source_object_site_id: 33519`
  - `source_object_name: Baccarat Rouge 540`
  - `brand_or_house: Maison Francis Kurkdjian`
  - `evidence_surface_class: fragrance_native_product_review_current_window`
- Explicit negative classification: not `retail_pdp`, not `retail_review_substrate`, not retailer verified-purchase reviews, not merchant offer/price/availability substrate.
- Downstream derived home, if built later: `derived/<anchor_shard>/<raw-anchor>/<lane-namespace>/<record-id>`, with lane namespaces owned by projection/ECR/Cleaning. Do not freeze source taxonomy into the lake path.

## Fragrantica Data Integrity And Quality Facts

- Direct HTTP packet:
  - packet_id: `01KW7SGXRZHFTS372X391Z8GHV`
  - path observed: `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV`
  - capture_time: `2026-06-28T18:57:58Z`
  - body file: `raw/01_http_response_body.bin`, SHA256 `62ede0326b08124bc9a8e54c991fa7bcf531a06177a69c04cab2d33c5c531273`, 1,806,640 bytes
  - receipt SHA256: `7294350957F35BBCA04C529EC776611A0B52D043E262E86F2DB2329A0BE17111`
  - manifest SHA256: `15800A4CB1A8D67EAC68C2D15C0831967E1661F0BB071AFEEDDE0601E4F86D2E`
- Direct current-window review substrate parsed from preserved bytes:
  - total review cards: 210
  - all-reviews tab cards: 200; first dates `2026-06-25`, `2026-06-22`, `2026-06-21`; last all-tab dates `2026-01-13`, `2026-01-13`, `2026-01-13`
  - positive tab cards: 5; negative tab cards: 5; search tab cards: 0
  - each card carried author metadata, `datePublished`, avatar image, vote button, share permalink, review text, and `user-perfume-votes-new` JSON in the parse run.
  - review permalinks are source-visible via `?ccid=<comment_id>#focus-zone` share paths.
  - review text lengths: count 210, min 10, p50 326.5, p90 1054, max 3763; 68 reviews over 500 chars; 26 reviews over 1000 chars.
  - per-card rating distribution: `{5: 54, 0: 54, 1: 30, 3: 28, 2: 27, 4: 17}` where `0` is no/zero source vote as carried.
  - longevity distribution: `{0: 131, 4: 38, 5: 24, 3: 11, 2: 3, 1: 3}`.
  - sillage distribution: `{0: 127, 3: 38, 2: 24, 4: 14, 1: 7}`.
  - relation distribution: `{None: 116, have: 77, had: 13, want: 4}`.
  - gender distribution: `{None: 124, unisex: 41, female_unisex: 28, female: 10, male_unisex: 6, male: 1}`.
  - season counts: `{winter: 71, autumn: 67, spring: 39, summer: 17}`.
  - day/night counts: `{night: 63, day: 37}`.
- CloakBrowser scroll diagnostic packet:
  - packet_id: `01KW7TH4J2ZK8HSA2H2DFNS5V7`
  - scratch path: `orca-harness/_test_runs/fragrance_native_20260629/fragrantica_cloakbrowser_scroll_diag_packet`
  - capture_time: `2026-06-28T19:15:33Z`
  - rendered DOM SHA256 `9e37eda80975b077183dbf615673531c9c8894016b0f08901436d19f5bf107a7`, 4,274,647 bytes
  - visible text SHA256 `aa072abea821f7350469775bdadb9b6d60696752681714192472a34a2c5c4b2e`, 172,288 bytes
  - screenshot SHA256 `619658ca8112e5aa29b9e114b8510e749fa6c3f0fc1bd9b238c3ce2187b5cbd4`, 261,812 bytes
  - visible text showed `Reviews (3.9K)` and `Sign in to access the full review archive`.
  - rendered DOM carried 310 unique `review_` IDs after scroll, still partial versus 3.9K.
- Quality boundary:
  - Long-form reviews are present and mechanically measurable.
  - Reviewer avatar/profile images are present in review cards.
  - Review-attached photos are not proven in current card evidence; linked media assets were not independently preserved.
  - The packet preserves source-visible rating/performance votes per current-window card, but not a full all-time review archive or page-level star histogram beyond source-visible aggregate/count fields.

## Authority And Source Ledger

| Source | Role | Load-bearing | Compare target | Last checked | Reuse rule |
| --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | Project behavior and overlay binding | yes | user-supplied current task context; reread repo copy if strict conflict appears | 2026-06-29 | Orientation until repo reread for strict policy claims |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | yes | SHA256 `A136775DA51F7B1B7563292660B705673B26E1A6436A08F7566C221D3B4BCF6A` | 2026-06-29 | Reread if overlay ownership changes |
| `.agents/workflow-overlay/source-loading.md` | Source-loading and handoff read-pack rule | yes | SHA256 `8FADC263B98F08B73B68E44DE71709D4AAF7FEA5D2E0390602B93E7863E11AB3` | 2026-06-29 | Reread before strict source-loading claims |
| `.agents/workflow-overlay/artifact-folders.md` | Durable destination | yes | SHA256 `A90D856804A80DFA836BB615A5EECF78C4FD871C35F575513433810CAC4CF305` | 2026-06-29 | Reread before placement claims |
| `.agents/workflow-overlay/decision-routing.md` | Cynefin routing | yes | SHA256 `8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E` | 2026-06-29 | Reread before routing/delegation claims |
| `.agents/workflow-overlay/prompt-orchestration.md` | Durable handoff contract | yes | SHA256 `64740C756AEC4A19F5218BCF275E05328B15B82AB62F08D9D977BB89CF849EE5` | 2026-06-29 | Reread before prompt/handoff contract claims |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | yes | SHA256 `7CE0444850C988A1E4C74FAA07EBC696561C3874F978F7C6C6E498092F9C83D7` | 2026-06-29 | Reread before header claims |
| `docs/research/orca_fragrance_native_database_live_probe_v0.md` | Probe record and packet addendum | yes | pre-edit SHA256 `B231277AC42EA75A2E16A2153109A2379FD1C00E1010D838076DA81EB73B9BE2`; modified this turn, reread current file | 2026-06-29 | Reread current file |
| `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV/receipt.md` | Fragrantica direct packet receipt | yes | SHA256 `7294350957F35BBCA04C529EC776611A0B52D043E262E86F2DB2329A0BE17111`; 2631 bytes | 2026-06-29 | Reread/hash before accepting packet facts |
| `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV/manifest.json` | Fragrantica manifest | yes | SHA256 `15800A4CB1A8D67EAC68C2D15C0831967E1661F0BB071AFEEDDE0601E4F86D2E`; 6680 bytes | 2026-06-29 | Reread/validate before sync |
| CloakBrowser diagnostic receipt | Scroll diagnostic | yes for 310-ID facts | SHA256 `9F5EB291774D5C8920616C37585B557F61752826AFFD9559180B29F8B408B027`; 3423 bytes | 2026-06-29 | Reread if using browser-scroll facts |
| Data Lake raw admission contract | Raw key/path/admission authority | yes | SHA256 `582D7612CC1C89CE8D92E71189AEDEEB749ADDE5DB13F9265DF77A79620282D7` | 2026-06-29 | Reread before lake path/admission claims |
| Data Lake storage contract | Raw/Attachment/derived slot authority | yes | SHA256 `0248FA723972AEFFD04220876229F1E116F6BB9855391855ABFBC05C2F98B262` | 2026-06-29 | Reread before storage/Attachment claims |
| Projection doctrine | Projection boundary | yes | SHA256 `81AE300C0AC7A26641771C2A11C9E0CF690A7C8C2429228D73F036586583F01D` | 2026-06-29 | Reread before projection work |
| ECR submap | ECR invariants | yes | SHA256 `C945C079D06F4D15A487BB99D9CB3431E1A8CF5AFDA1679424D1842E6C596F60` | 2026-06-29 | Reread before ECR work |
| Data/Cleaning boundary | Layer split | yes | SHA256 `3D50EEA84071490B563A36ABE37F974654A820274EFD767FFB37FFAB05F2509D` | 2026-06-29 | Reread before Cleaning/cross-layer claims |

## Source Gaps / Not-Proven Boundaries

- Fragrantica full review archive is login-gated in the observed route and not captured.
- Fragrantica endpoint route for full archive is not pinned in this packet; re-derive under capture playbook if needed.
- Review-attached photos are not proven; only reviewer/avatar images are proven in review cards.
- No fixture admission or routine Data Lake sync was run by this handoff.
- No full database coverage, full archive, demand proof, buyer proof, ECR readiness, Cleaning readiness, or Judgment quality is proven.
## Current Task State

- Completed:
  - Fragrantica direct HTTP packet exists in the configured external data root with source_family `fragrance_native_database` and source_surface `fragrantica_product_page_direct_http`.
  - Fragrantica current-window card integrity/quality fields were mechanically parsed from preserved bytes.
  - CloakBrowser scroll diagnostic exists in ignored scratch and shows more review IDs but still a login-gated archive boundary.
  - Parfumo diagnosis addendum was added to the research artifact; Parfumo is not the target of this handoff packet.
- Partially completed:
  - Data Lake sync/classification is specified for the receiver but not executed.
  - Mechanical projection row shape is recommended but not authored as code or schema.
  - ECR and Cleaning continuation boundaries are specified but not implemented.
- Broken or uncertain:
  - The existing Fragrantica direct packet landed in `F:/orca-data-lake` because `ORCA_DATA_ROOT` overrode the requested scratch output. Treat as generated packet fact until Data Lake receiving lane validates or replays it.
  - Full Fragrantica review archive capture remains unresolved behind the login/archive boundary.

## Workspace State

- Branch: `codex/fragrance-native-live-probe`
- Head before this docs turn: `b4641d65`
- Dirty or untracked state before handoff: clean worktree at `b4641d65`.
- Dirty or untracked state after writing the handoff file: expected modified `docs/research/orca_fragrance_native_database_live_probe_v0.md` and untracked `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`; receiver must run fresh `git status --short --branch`.
- Target files/artifacts: this handoff file; `docs/research/orca_fragrance_native_database_live_probe_v0.md`; Fragrantica direct packet under `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV`; CloakBrowser diagnostic under `orca-harness/_test_runs/fragrance_native_20260629/fragrantica_cloakbrowser_scroll_diag_packet`.
- Related worktrees or branches: main workspace is on unrelated dirty lane `codex/ig-reels-capture-spine`; do not edit or claim state from it for this lane.

## Changed / Inspected / Tested Files

- `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`
  - Status: created in this turn.
  - Role: cold handoff packet for Fragrantica Data Lake / Projection / ECR / Cleaning continuation.
- `docs/research/orca_fragrance_native_database_live_probe_v0.md`
  - Status: modified in this turn.
  - Role: research/probe receipt.
  - Important observations: Parfumo pagination addendum added and closeout updated.
- `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV/receipt.md`
  - Status: inspected, external data root.
  - Role: Fragrantica direct packet receipt.
  - Important observations: source_family `fragrance_native_database`, source_surface `fragrantica_product_page_direct_http`, direct HTTP 200, body SHA/size.
- `orca-harness/_test_runs/fragrance_native_20260629/fragrantica_cloakbrowser_scroll_diag_packet/receipt.md`
  - Status: inspected, ignored scratch.
  - Role: Fragrantica browser-scroll diagnostic receipt.

## Frozen Decisions

- Decision: classify Fragrantica as `fragrance_native_database`, not `retail_pdp`.
  - Evidence: packet manifest/receipt source_family and source_surface; source character is fragrance-native enthusiast database, not merchant PDP.
  - Consequence: Projection/ECR/Cleaning must not import retailer PDP field assumptions.
- Decision: use raw packet metadata/Attachment Record/projection metadata for semantic classification; do not encode classification in raw path.
  - Evidence: Data Lake raw admission and physicality contracts.
  - Consequence: physical path remains `raw/<packet_shard>/<packet_id>/`.
- Decision: Fragrantica current-window capture is useful but incomplete.
  - Evidence: 210 direct cards, 310 CloakBrowser DOM IDs, visible `Reviews (3.9K)` and login archive prompt.
  - Consequence: projection must carry completeness residuals and raw-pull triggers.
- Decision: ECR/Cleaning do not get to repair missing review archive coverage.
  - Evidence: projection and ECR carry-or-residualize doctrine; Data/Cleaning boundary.
  - Consequence: absent full archive is a residual, not a cleaned value or observed zero.

## Mutable Questions

- Should Data Lake accept the existing external-root packet or require a deliberate replay?
  - Why still mutable: packet exists and hashes are visible, but it landed via environment override during a probe.
  - What would resolve it: receiving lane runs raw-admission checks and records accept/hold/replay decision.
- Should Fragrantica full archive be pursued later?
  - Why still mutable: public current-window data is useful; full archive is login-gated in observed route.
  - What would resolve it: owner authorizes own-entitled login/manual route, or a public non-auth route is re-derived under capture playbook.
- What exact projection schema should Fragrantica use?
  - Why still mutable: this packet names row groups and residuals, not a ratified schema.
  - What would resolve it: projection lane authors a bounded schema/adapter plan with tests.
- Should CloakBrowser scroll diagnostic be promoted, replayed, or kept scratch?
  - Why still mutable: it preserved more review IDs but is diagnostic and partial.
  - What would resolve it: Data Lake or Capture owner decides whether browser-rendered current-window DOM adds enough value beyond direct HTTP.

## Superseded / Dangerous-To-Reuse Context

- Treating Fragrantica as retail/PDP because it has product pages and reviews is dangerous. Current replacement: `fragrance_native_database` source family with Fragrantica-specific projection rows/residuals.
- Treating direct HTTP 200 plus 210 inline cards as complete Fragrantica capture is dangerous. Current replacement: current-window partial capture only.
- Treating Data Lake sync as moving the packet into a source-named folder is dangerous. Current replacement: opaque raw shard path plus manifest/projection/attachment metadata.

## Commands And Verification Evidence

- `git status --short --branch; git rev-parse --short HEAD; git branch --show-current`
  - Passed: yes.
  - Important output: live-probe worktree was clean at `b4641d65` on `codex/fragrance-native-live-probe` before docs edits.
  - Re-run target: run from `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrance-native-live-probe`.
- `Get-FileHash -Algorithm SHA256 <target files>`
  - Passed: yes.
  - Important output: source hashes are recorded in Authority And Source Ledger.
  - Re-run target: recompute hashes for every load-bearing file before acting.
- Python parse over Fragrantica direct packet and CloakBrowser DOM
  - Passed after one quoting rerun.
  - Important output: direct packet had 210 review cards with field counts/distributions above; CloakBrowser DOM had 310 unique review IDs; visible text carried `Reviews (3.9K)` and login archive prompt.
  - Re-run target: parse `F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV/raw/01_http_response_body.bin` and the CloakBrowser DOM file.
- Parfumo live POST probes
  - Passed with network approval.
  - Important output: Parfumo addendum was updated in the research artifact; not load-bearing for Fragrantica handoff.
  - Re-run target: see `docs/research/orca_fragrance_native_database_live_probe_v0.md` addendum.
- Validation not run:
  - No code tests were run because this was a docs-only handoff/research update.
  - Recommended verification before commit or downstream use: `git diff --check -- docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md docs/research/orca_fragrance_native_database_live_probe_v0.md` and fresh `git status --short --branch`.

## Blockers And Risks

- Existing Fragrantica packet may be treated as formal Data Lake admission without raw-admission verification.
  - Evidence: research closeout says the packet landed in configured ORCA data root during completeness check and is a generated packet fact only.
  - Likely next action: Data Lake receiving lane runs admission/availability validation and records accept/hold/replay.
- Full archive login prompt could tempt unauthorized access or unbounded route escalation.
  - Evidence: direct/CloakBrowser artifacts contain the login archive prompt.
  - Likely next action: stop at current-window capture unless owner supplies own-entitled route or a new public route fact.
- Projection could silently drop positive/negative tabs, long reviews, or no-vote cards.
  - Evidence: tab counts and rating distribution include positive/negative cards and rating `0`/missing posture.
  - Likely next action: projection must carry tab/source-order and residuals/loss ledger.
- Cleaning could interpret review text sentiment or scent meaning.
  - Evidence: Cleaning boundary forbids credibility/exclusion/strength effects; Judgment owns interpretation.
  - Likely next action: Cleaning only normalizes non-destructively and records raw-to-cleaned trace.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting: branch/head/dirty state; handoff path; Fragrantica direct receipt/manifest/body hashes; direct current-window parse counts if used; CloakBrowser receipt/manifest/DOM hash if browser-scroll facts are used; Data Lake raw admission/path and storage contract; projection/ECR/Cleaning boundary rules.
- Compare targets: hashes and paths in Authority And Source Ledger; fresh `git status --short --branch`; fresh parse over preserved raw bytes; current overlay/Data Lake/projection/ECR/Cleaning source docs.
- Load outcomes:
  - `REUSE`: all load-bearing facts re-verified; continue exact next authorized action.
  - `PARTIAL_REUSE`: optional Parfumo or non-load-bearing context drifted; reuse verified Fragrantica/Data Lake facts.
  - `STALE_REREAD_REQUIRED`: handoff source docs, packet receipts, head, or dirty state drifted but can be re-derived.
  - `BLOCKED_DRIFT`: Fragrantica packet missing/hash mismatch, source_family/surface conflict, or workspace drift conflicts with expected lane.
  - `BLOCKED_MISSING_PACKET`: this handoff path or named Fragrantica packet is absent/unreadable.
  - `BLOCKED_UNVERIFIABLE`: any load-bearing claim lacks a compare target and cannot be re-derived.

## Do Not Forget

The right lake classification is `fragrance_native_database` plus Fragrantica-specific source-surface metadata. The raw path stays opaque; the current-window reviews stay partial; and ECR/Cleaning must carry residuals rather than repair or interpret missing archive coverage.
