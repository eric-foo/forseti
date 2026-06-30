# Fragrance-Native Capture Pipeline (Parfumo + Basenotes) Build Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet (cold-reader build handoff)
scope: >
  Cold handoff to a fresh lane to build the same Fragrantica "capture reviews"
  capability -- raw source-capture packet -> mechanical projection -> Cleaning
  audit pack + post-cleaned Silver -- for two more fragrance-native databases,
  Parfumo and Basenotes, by adapting the Fragrantica reference modules and riding
  the merged no-blur infrastructure (silver front-door, lane registry, non-silver
  mirror). Parfumo is capture-ready on the anonymous rendered default; Basenotes via the residential-proxy CloakBrowser route (verified live).
use_when:
  - Building the Parfumo capture -> projection -> Cleaning -> Silver pipeline.
  - Deciding the generalize-shared vs clone-per-source architecture fork.
  - Building the Basenotes pipeline via the residential-proxy CloakBrowser route (verified; see the research probe's Proxy Route Verification Addendum).
authority_boundary: retrieval_only
open_next:
  - docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
  - docs/research/orca_fragrance_native_database_live_probe_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca-harness/data_lake/lane_registry.py
stale_if:
  - The no-blur infrastructure (append_silver_record front-door, non_silver_record
    mirror, lane_registry roles) is reshaped or moved.
  - The Fragrantica reference modules (fragrantica_projection.py, fragrantica_lake.py,
    test_fragrantica_capture_to_silver_e2e.py) are moved or materially changed.
  - The residential-proxy CloakBrowser route stops reaching Basenotes (Cloudflare tightens), or a cleaner Basenotes route appears.
  - The Parfumo product route or pagination route changes.
  - This build is started/landed (then refresh or retire this packet).
```

## Load Contract

- packet_version: workflow-handoff-v1
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-06-30 (session local)
- created_by_lane: Claude no-blur-enforcement lane (session `zealous-jang-522dbf`); provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca` (main repo) + per-lane worktrees under `...\orca\worktrees\`
- handoff_path: `docs/workflows/fragrance_native_capture_pipeline_parfumo_basenotes_build_handoff_v0.md`
- authored_on_worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrance-native-capture-handoff`, branch `claude/fragrance-native-capture-handoff`, base `origin/main`
- expected_base_head: `7d0dcfdd` (Merge #515) at authoring time -- **main MOVES FAST** (many parallel lanes); treat the merged-PR set named under "No-Blur Infrastructure", not the SHA, as the anchor.
- expected_dirty_state_including_handoff_file: this handoff file newly UNTRACKED on the authoring worktree; otherwise clean.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority. The Fragrantica reference files are `reread-required` against current `origin/main` because they are code that other lanes may move.

## Goal Handoff

- long_term_goal: Build Orca fragrance-native source capture and downstream evidence plumbing that can monitor specialist fragrance precursor demand WITHOUT blurring raw capture, Data Lake, Projection, ECR, Cleaning, or Judgment responsibilities (the no-blur invariant).
- anchor_goal: Stand up the Fragrantica-equivalent capture->projection->Cleaning-audit->Silver pipeline for Parfumo and Basenotes -- both capture-reachable (Parfumo on the anonymous rendered default; Basenotes via the residential-proxy CloakBrowser route, verified live this turn) -- reusing the merged no-blur infrastructure rather than rebuilding it.
- success_signal: A cold lane can (a) run a Parfumo capture packet through a projection + Cleaning-audit + Silver path that mirrors Fragrantica, with all four layers persisting as DISTINCT roles threaded by one raw anchor; (b) the new Silver records go through `append_silver_record` and the new lanes are declared in `lane_registry.py`, so the CI guard + non-silver conformance test pass; (c) Basenotes is captured via the residential-proxy CloakBrowser route (anonymous CloakBrowser is Cloudflare-blocked; the proxy renders real product content -- verified this turn), not faked and not wrongly declared blocked.

## Open Decision / Fork

- **Decision A -- generalize a shared `fragrance_native` pipeline vs clone-per-source.** The Fragrantica modules (`fragrantica_projection.py`, `fragrantica_lake.py`) are bespoke. All three sources share `source_family=fragrance_native_database`; only the DOM/field extraction differs per source. The research probe's own route answer says to build the **shared** projection/Cleaning shape once Fragrantica + Parfumo are both in hand.
  - options: (1) clone `fragrantica_*` -> `parfumo_*` and adapt; (2) factor the genuinely shared shape (audit-pack payload, Silver record shape, front-door routing, lineage threading) into a `fragrance_native` helper and keep only DOM parse + field extraction per-source; (3) hybrid -- clone Parfumo first for a working second instance, then factor the shared seam from the two concrete instances.
  - already constrained / off the table: rebuilding the no-blur infra; reshaping `silver_lineage`; encoding source taxonomy into the raw lake path; classifying these as `retail_pdp`.
  - trade-offs: option 1 is fastest and lowest-lock-in but duplicates; option 2 is the product-intended end state but is **high-lock-in** abstraction from possibly-too-few instances; option 3 follows "harvest before cook" -- avoid abstracting from one instance.
  - owner of the call: receiving lane, surfaced to owner because option 2 is a high-lock-in shared-shape commitment (Decision-Priority lock-in tiebreaker applies).
  - recommendation: **option 3.** Build Parfumo by adapting the Fragrantica template to get a real second instance, then factor only the seam the two instances actually share. Do not abstract a shared pipeline from Fragrantica alone.
- **Decision B -- Basenotes capture route: RESOLVED to proxied CloakBrowser (owner-authorized, verified).** Anonymous CloakBrowser on Basenotes returns the Cloudflare "Just a moment" interstitial (`ACCESS_BLOCKED`/`residual_challenge_marker`), but CloakBrowser through the residential proxy profile `reddit-res-01` renders the real product page (`no_block_marker`; title "Mojave Ghost by Byredo · Basenotes"; ~3.8 KB visible text with notes/house/reviews) -- verified live this turn. So Basenotes is captured the SAME way as Parfumo, just with the proxy profile attached.
  - already constrained / off the table: building anti-bot / Cloudflare detection-evasion tooling (out of scope and a safety boundary) -- the residential proxy is an existing, owner-authorized capture route, not evasion tooling; treating a challenge page as captured content; reference the proxy by LABEL only (never serialize endpoint/credentials).
  - remaining open (build-level, not access blockers): run-to-run robustness (Cloudflare is probabilistic; a residential exit may occasionally still be challenged -- handle as a retry/limitation, never as silent zero); and whether the FULL review corpus loads via deep-scroll vs just the product page.
  - owner of the call: owner already authorized the proxy route; the receiver builds it.

## Drift Guard

- **No-blur invariant is the whole point.** Every new Silver record MUST be written through `data_lake.silver_record.append_silver_record` (the validating front-door), never the raw `append_record`. The CI guard `.agents/hooks/check_silver_lane_registry.py` fails a silver-named lane that is undeclared or bypasses the front-door. `FRONT_DOOR_PENDING` is empty -- do not add a new bypass.
- **Same source_family, new source_surface.** Parfumo/Basenotes are `source_family=fragrance_native_database`, NOT a new bespoke family and NOT `retail_pdp`. source_surface = `parfumo_product_page_direct_http` / `basenotes_*`. Do not import retailer/verified-purchase/offer semantics.
- **Four distinct representations, one raw anchor.** raw capture / projection / Cleaning audit pack / post-cleaned Silver each stay a DISTINCT persisted record with its own declared role; none impersonates another; Judgment stays out of scope. This is what `test_fragrantica_capture_to_silver_e2e.py` asserts -- the new sources must get the equivalent e2e proof.
- **Projection is mechanical, carry-or-residualize.** A projection certification must include the exact tokens `not_cleaned` and `not_judgment_ready` (the non-silver mirror checks this). Never author cleaned/judged values from prose; residualize missing coverage.
- **The default capture route IS CloakBrowser rendered deep-scroll.** For fragrance-native sources the default route is the anti-blocking rendered browser (`source_capture/adapters/cloakbrowser_snapshot.py`), deep-scrolled to load the on-page reviews widget to completion (it handles IntersectionObserver-gated lazy review sections + "load more"); the per-source pagination route (e.g. Parfumo's first-party AJAX) extends depth. The direct-HTTP fetch is a SUPPLEMENTARY structured-HTML slot, NOT the default route. Mirror the slot orchestration in `runners/run_fragrantica_mgt_capture.py`, but the rendered browser is the route that matters.
- **Cloudflare-walled sources use the residential-proxy CloakBrowser route.** Verified live this turn: anonymous CloakBrowser on Basenotes hits the Cloudflare interstitial; CloakBrowser through the residential proxy profile (`reddit-res-01`, owner-authorized) renders the real page. So a walled source's route is proxied CloakBrowser, not "blocked". Pass the `ProxyProfile` to the same adapter; reference it by LABEL only, never serialize the endpoint/credentials.
- **Do not conflate with the retail purchase-review widget lane.** `fragrance_rendered_widget_companion.py` / `fragrance_review_lake.py` / `runners/run_fragrance_review_lake_packet.py` are the SEPARATE fragrance *purchase-review* lane (retailer PDPs + review-widget bytes, e.g. Yotpo fallback; PRs #481/#489/#492) -- a different source family. It is NOT the capture mechanism for the fragrance-native databases here; their reviews are on-page, captured by CloakBrowser deep-scroll + per-source pagination.
- **Live capture is owner-authorized but per-turn.** The owner authorized the rendered-browser + residential-proxy route for these sources; the proxy profile `reddit-res-01` is the sanctioned route. Each live HTTP/rendered fetch against external roots still needs the per-turn owner network approval (a prior approval does not roll forward). No login/auth-gate bypass; capture only public content; residualize partial coverage.
- **Capture completeness is partial and must be residualized.** Parfumo full corpus (369 reviews / 1390 statements) was NOT captured; only a current product-page probe exists. Carry completeness residuals exactly as Fragrantica does for its 210/310-of-3.9K window.
- **Scratch packets are not fixture-admitted.** The Parfumo scratch packet `01KW7SJ8F4M6ZTGVWMBB9ZVXCR` is local ignored scratch (a generated fact), not a Data Lake admission or test fixture.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `.agents/workflow-overlay/README.md` first per `AGENTS.md`).
- targets to enter the ladder: this packet; the Fragrantica reference handoff `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`; the research probe `docs/research/orca_fragrance_native_database_live_probe_v0.md`; the Fragrantica code modules listed in the Source Ledger; the no-blur infra modules; the Silver Vault + projection + data/cleaning contracts.
- already loaded (weak orientation only, freshness-marked, not authority): this sender's session read the no-blur infra (silver_record.py, non_silver_record.py, lane_registry.py) and the Fragrantica module signatures while authoring; the receiver must reread current `origin/main` copies.
- must load first before strict/actionable steps: `AGENTS.md` + overlay README/source-loading; this packet; the Fragrantica reference handoff + the research probe; the Silver Vault contract; the lane_registry; the projection doctrine and data/cleaning boundary.
- load rule: receiver re-runs progressive source loading per overlay; this packet only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- **No-blur enforced by code (Batches 1-3, all merged).** Silver is write-time enforced via the front-door; a non-silver negative mirror exists and is CI-conformance-tested on real Fragrantica producer output; a static guard blocks silver-lane bypass; `FRONT_DOOR_PENDING` is empty. Verify in `orca-harness/data_lake/silver_record.py`, `non_silver_record.py`, `lane_registry.py`, `.agents/hooks/check_silver_lane_registry.py` before strict enforcement claims. (Merged PRs #495, #501, #506, #507, #512.)
- **Fragrantica = `fragrance_native_database`, not retail PDP.** Decided in the Fragrantica reference handoff. Verify against `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md`.
- **Data Lake is raw-truth shared foundation;** projection/ECR/Cleaning are sibling lanes over raw/projection refs; ECR/Cleaning do not repair missing archive coverage or author meaning. Verify against the projection doctrine and the data/cleaning boundary contract before strict layer-ownership claims.
- **Raw packet paths are opaque (`raw/<packet_shard>/<packet_id>/`); semantic classification lives in manifest/projection metadata,** never the path. Verify against the Data Lake raw admission + storage contracts.

## Active Objective

Build the Parfumo capture->projection->Cleaning-audit->Silver pipeline as a faithful Fragrantica-equivalent that rides the merged no-blur infrastructure, producing the same four-distinct-layers end-to-end proof; and build Basenotes the same way via the residential-proxy CloakBrowser route (verified reachable this turn). Decide the shared-vs-clone architecture fork (Decision A) before writing the second projection module.

## Exact Next Authorized Action

1. **Re-verify the no-blur infra and Fragrantica template** on current `origin/main` (Source Ledger entries; all `reread-required`). Confirm `append_silver_record`, `validate_non_silver_record`, the `LANE_ROLES` map, and the four Fragrantica modules still have the shapes this packet describes. If they moved, update the plan before coding.
2. **Decision A (fork).** Choose clone vs shared-factor vs hybrid (recommendation: hybrid -- clone Parfumo first). State the decision; if choosing the high-lock-in shared-factor now, surface to owner first.
3. **Parfumo capture (CloakBrowser rendered is the route).** Under explicit owner network authorization, capture via CloakBrowser deep-scroll (`source_surface=parfumo_product_page_cloakbrowser_deep_scroll_current_window`) to load the on-page reviews to completion, then the first-party AJAX pagination route for fuller review/statement depth; mirror the slot orchestration in `runners/run_fragrantica_mgt_capture.py`. The direct-HTTP fetch (`parfumo_product_page_direct_http`) is a supplementary structured-HTML slot, not the route. `source_family=fragrance_native_database`. Product URL `https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum` (resolve via `s_perfumes_x.php` search when needed). Parfumo returned 200 on anonymous direct HTTP, so anonymous CloakBrowser should suffice (no proxy expected); the existing scratch probe packet (`01KW7SJ8F4M6ZTGVWMBB9ZVXCR`) is the direct-HTTP slot only.
4. **Parfumo projection.** Author `source_capture/parfumo_projection.py` mirroring `fragrantica_projection.py`: a mechanical projection over preserved bytes into lane `projection_parfumo`, with a certification carrying the exact tokens `not_cleaned` and `not_judgment_ready`. Parse the Parfumo review/statement DOM (per-source extraction is the only genuinely new code). Add `project_parfumo_into_lake(data_root, packet_id)`.
5. **Parfumo Cleaning + Silver.** Author `cleaning/parfumo_lake.py` mirroring `fragrantica_lake.py`: emit a `cleaning_audit_pack_v0` audit pack to lane `cleaning_parfumo_audit` (raw writer; it is intentionally NOT a Silver record) and one post-cleaned Silver record per review handle to lane `cleaning_parfumo_silver` **through `append_silver_record`**, threaded to the audit by `derived_refs` (edge `derived_from_record`, audit `content_hash`).
6. **Declare the new lanes** in `orca-harness/data_lake/lane_registry.py`: `projection_parfumo` -> `PROJECTION`, `cleaning_parfumo_audit` -> `CLEANING_AUDIT`, `cleaning_parfumo_silver` -> `SILVER_ENVELOPE`. Add the Basenotes triplet (`projection_basenotes` / `cleaning_basenotes_audit` / `cleaning_basenotes_silver`) the same way -- Basenotes capture uses the residential-proxy CloakBrowser route.
7. **Tests (acceptance).** Add `tests/test_parfumo_capture_to_silver_e2e.py` mirroring `test_fragrantica_capture_to_silver_e2e.py` (four distinct layers, one raw anchor), plus projection/cleaning pilots; and extend `tests/unit/test_non_silver_record_roles.py` so the REAL Parfumo audit + projection producer output is run through `validate_non_silver_record` (the no-blur conformance net).
8. **Validate:** `python -m pytest` from `orca-harness/` (set `$env:ORCA_DATA_ROOT=$null` first) and the 9 `.agents/hooks/check_*.py --strict` hooks, especially `check_silver_lane_registry.py --selftest --strict`. Land via the per-lane PR flow.
9. **Basenotes (same build as Parfumo, with the proxy).** Capture via CloakBrowser deep-scroll through the residential proxy profile `reddit-res-01` (anonymous CloakBrowser is Cloudflare-blocked; the proxy renders real content -- verified this turn). `source_surface=basenotes_product_page_cloakbrowser_deep_scroll_current_window`. Then build `basenotes_projection.py` + `basenotes_lake.py` + lanes + tests exactly like Parfumo. Treat an occasional Cloudflare challenge on a proxied run as a retry/limitation, never a silent empty result. Reference the proxy by LABEL only; do not build detection-evasion.
10. **Stop conditions:** stop if the no-blur infra shape drifted from this packet; if the Parfumo route returns a block shell / changed product URL; if any live fetch lacks owner network authorization; or if a Silver write is about to use the raw writer.

## Authority And Source Ledger

| Source | Role | Load-bearing | Compare target | Reuse rule |
| --- | --- | --- | --- | --- |
| `AGENTS.md` + `.agents/workflow-overlay/README.md` | Project behavior + overlay binding | yes | reread-required | Reread before strict project-rule claims |
| `.agents/workflow-overlay/source-loading.md` | Source-loading doctrine | yes | reread-required | Reread before strict source-loading claims |
| `.agents/workflow-overlay/artifact-folders.md` | Durable destination (docs/workflows/) | yes | reread-required | Reread before placement claims |
| `orca-harness/data_lake/silver_record.py` | Silver front-door `append_silver_record` + envelope validator | yes | reread-required @ origin/main | The ONLY sanctioned Silver writer; reread before routing Silver |
| `orca-harness/data_lake/non_silver_record.py` | Non-silver negative mirror `validate_non_silver_record` | yes | reread-required @ origin/main | Run new projection + audit output through it (conformance) |
| `orca-harness/data_lake/lane_registry.py` | `LANE_ROLES` map + guard source of truth | yes | reread-required @ origin/main | Declare new lanes here or the guard fails CI |
| `.agents/hooks/check_silver_lane_registry.py` | Write-path guard (G1 declared / G2 front-door) | yes | reread-required @ origin/main | Must pass `--selftest --strict` |
| `orca-harness/source_capture/fragrantica_projection.py` | Projection template: `build_fragrantica_projection`, `project_fragrantica_into_lake`, `PROJECTION_FRAGRANTICA_LANE`, `FRAGRANTICA_PROJECTION_CERTIFICATION` | yes | reread-required @ origin/main | Mirror for `parfumo_projection.py` |
| `orca-harness/cleaning/fragrantica_lake.py` | Cleaning+Silver template: `derive_fragrantica_cleaning_into_lake`, `FRAGRANTICA_CLEANING_AUDIT_LANE`, `FRAGRANTICA_CLEANING_SILVER_LANE`, audit-pack payload, post-cleaned Silver via front-door | yes | reread-required @ origin/main | Mirror for `parfumo_lake.py` |
| `orca-harness/cleaning/fragrantica.py` | Non-lake cleaning transform logic | no | reread-required | Reference for transform shape |
| `orca-harness/tests/test_fragrantica_capture_to_silver_e2e.py` | Acceptance template (4 distinct layers, one anchor) | yes | reread-required @ origin/main | Mirror as `test_parfumo_capture_to_silver_e2e.py` |
| `orca-harness/tests/unit/test_non_silver_record_roles.py` | Real-producer non-silver conformance test | yes | reread-required @ origin/main | Extend for Parfumo real producer output |
| `orca-harness/source_capture/models.py` | `SourceCapturePacket`, `source_family: str`, posture helpers (`known_fact`/`not_applicable`/`not_attempted`/`unknown_with_reason`), `SourceCaptureSlice`, `PacketTiming` | yes | reread-required @ origin/main | Capture model is source-generic; new source = new source_surface |
| `orca-harness/source_capture/writer.py` | `write_local_source_capture_packet` | yes | reread-required @ origin/main | Capture writer |
| `orca-harness/runners/run_fragrantica_mgt_capture.py` + `run_fragrantica_projection.py` | Capture + projection runners | yes | reread-required @ origin/main | Mirror for Parfumo runners |
| `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md` | Fragrantica pipeline + classification reference | yes | reread-required | The canonical pipeline description to mirror |
| `docs/research/orca_fragrance_native_database_live_probe_v0.md` | Parfumo/Basenotes access facts + Parfumo pagination addendum | yes | reread-required | The DURABLE record of capture-route facts (scratch packets are ephemeral) |
| `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` | Silver Vault contract | yes | reread-required | Reread before Silver envelope claims |
| `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` | Projection boundary | yes | reread-required | Reread before projection work |

- Source gaps: exact Parfumo and Basenotes review-card / statement DOM field names are not enumerated here (per-source extraction is discovery work over the preserved bytes). Basenotes' capture ROUTE is resolved (residential-proxy CloakBrowser, verified); only its DOM field map is open.
- Not-proven boundaries: no Parfumo full-corpus capture; no Basenotes capture; no ECR/Cleaning/Judgment readiness; no demand/buyer proof. This handoff authorizes pipeline build scoping, not live crawling.

## Current Task State

- Completed (this sender, separate workstream): the no-blur infrastructure (Batches 1-3) is merged and is what the new pipelines ride.
- Available to reuse: the Fragrantica capture->projection->Cleaning->Silver pipeline + its e2e proof; the Parfumo route pin + scratch probe packet; the research probe doc.
- Not started: any Parfumo/Basenotes projection, cleaning, silver, runner, or test code; the architecture fork decision.
- Verified this turn: Basenotes renders real content via the residential-proxy CloakBrowser route (anonymous CloakBrowser is Cloudflare-blocked). No remaining hard access blocker; proxy-run robustness + full-review depth are the open build questions.

## Workspace State

- Authoring worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrance-native-capture-handoff`, branch `claude/fragrance-native-capture-handoff`, base `origin/main` @ `7d0dcfdd` (Merge #515).
- Dirty state before this file: clean.
- Dirty state after writing this file: this handoff file UNTRACKED on the authoring worktree.
- The build should happen on its OWN fresh worktree off `origin/main` (not this doc worktree, not the stale session worktree). Live capture needs owner network authorization.
- Related: the Fragrantica lane modules + the `fragrance-native-live-probe` research lane are the upstream context; the Fragrantica handoff doc cites the live-probe receipts.

## Frozen Decisions

- Decision: new Silver records ride `append_silver_record`; new lanes are declared in `lane_registry.py`.
  - Evidence: the merged no-blur front-door + guard; `fragrantica_lake.py` already routes its Silver through `append_silver_record`.
  - Consequence: a raw-writer Silver write fails CI; this is non-negotiable.
- Decision: Parfumo/Basenotes are `source_family=fragrance_native_database`, new `source_surface`.
  - Evidence: the research probe pinned Parfumo as `parfumo_product_page_direct_http` under `fragrance_native_database`; Fragrantica uses the same family.
  - Consequence: no retail-PDP semantics; classification in manifest/projection metadata, not the raw path.
- Decision: both sources are capturable; they differ only by route. Parfumo on the anonymous rendered default (direct HTTP returned 200); Basenotes via the residential-proxy CloakBrowser route.
  - Evidence: research probe (Parfumo direct HTTP 200 + pinned route + AJAX pagination); live probe this turn -- anonymous CloakBrowser on Basenotes = Cloudflare interstitial, proxied CloakBrowser (`reddit-res-01`) = real product page rendered.
  - Consequence: build both; Basenotes attaches the proxy profile; never declare Basenotes "blocked" (that was the anonymous-only result) and never store a challenge page as content.

## Mutable Questions

- Decision A: clone vs shared-factor vs hybrid pipeline shape? (Resolved by the receiver; recommendation = hybrid/clone-first.)
- What exact projection row groups + field extraction does Parfumo need? (Resolved by reading the preserved Parfumo bytes; mirror Fragrantica's row groups, then add Parfumo-specific fields.)
- Should the Parfumo full 369-review / 1390-statement corpus be pursued (AJAX pagination route), or is the current product-page window enough for v0? (Owner/product call; v0 can be current-window with residuals, like Fragrantica.)
- Basenotes: route is verified (residential-proxy CloakBrowser); open are run-to-run robustness (Cloudflare is probabilistic) and whether the full review corpus loads via deep-scroll. (Build questions, not access blockers.)

## Superseded / Dangerous-To-Reuse Context

- Treating Basenotes as permanently access-blocked is WRONG -- that was an anonymous-only result. Current replacement: anonymous CloakBrowser is Cloudflare-blocked, but the residential-proxy CloakBrowser route (`reddit-res-01`) renders real Basenotes content (verified this turn); both sources are buildable, Basenotes via the proxy profile. The earlier `direct_http`-as-default framing is also superseded: CloakBrowser rendered deep-scroll is the default route.
- Building a shared `fragrance_native` pipeline abstraction from Fragrantica ALONE is premature (one instance). Current replacement: get Parfumo as a real second instance first, then factor the shared seam.
- Building anti-bot / Cloudflare evasion to reach Basenotes is out of scope and a safety boundary. Current replacement: owner-authorized public access probe or owner-entitled bytes.
- The Parfumo scratch packet `01KW7SJ8F4M6ZTGVWMBB9ZVXCR` is ignored local scratch, not a fixture or Data Lake admission; do not treat it as durable. The durable record of Parfumo facts is the research doc.

## Commands And Verification Evidence

- Reference acceptance test (mirror it):
  ```bash
  # from orca-harness/ ; $env:ORCA_DATA_ROOT=$null
  python -m pytest tests/test_fragrantica_capture_to_silver_e2e.py
  ```
  - Re-run target: author `tests/test_parfumo_capture_to_silver_e2e.py` and make it green.
- No-blur guard (must stay green after declaring new lanes):
  ```bash
  python .agents/hooks/check_silver_lane_registry.py --selftest --strict
  ```
- Full suite + strict hooks before landing:
  ```bash
  python -m pytest            # use --junitxml=<file> for authoritative counts in PowerShell
  # + the 9 .agents/hooks/check_*.py --strict hooks
  ```
- Not run by this handoff: no code was written or tests run; this is a docs-only build handoff.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting: the no-blur infra shapes (front-door, mirror, lane_registry, guard); the four Fragrantica template module signatures; the Parfumo + Basenotes capture routes (Basenotes = residential-proxy CloakBrowser, verified this turn; re-confirm the proxy still renders content, since Cloudflare is probabilistic); `append_silver_record` is the only sanctioned Silver writer.
- Compare targets: reread the named code modules on current `origin/main`; reread the research probe doc for the route facts; re-run the CloakBrowser probe for the Basenotes proxy route; reread the Silver Vault + projection contracts.
- Load outcomes:
  - `REUSE`: infra + template shapes match -> proceed from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: only secondary references drifted -> reuse verified plan, re-derive the rest.
  - `STALE_REREAD_REQUIRED`: a template module or contract moved/changed -> re-map before coding.
  - `BLOCKED_DRIFT`: the no-blur front-door/guard/mirror was reshaped, contradicting a Frozen Decision -> stop and reconcile.
  - `BLOCKED_UNVERIFIABLE`: a Parfumo/Basenotes access fact cannot be re-derived from the research doc and the scratch packet is gone -> re-probe under owner network authorization rather than trusting this packet.

## Do Not Forget

- Build both Parfumo and Basenotes; Basenotes attaches the residential proxy profile `reddit-res-01`. Never store a Cloudflare challenge page as content, and never silently emit an empty result on a challenged run -- that would violate real-failure-visibility.
- Every new Silver record goes through `append_silver_record`; declare the new lanes in `lane_registry.py`; extend the non-silver conformance test with real Parfumo producer output. That is what keeps no-blur enforced by CODE for the new sources.
- No live capture without explicit owner network authorization; capture only public content; residualize partial coverage.
