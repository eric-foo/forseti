# Capture Source-Family Lane Catalog

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane catalog
scope: >
  Cold-start catalog for known Capture source families. Routes from the
  source-agnostic Source Capture Playbook / Armory into the owning source-family
  lane index, then onward to runner, projection, Data Lake, ECR, and Cleaning
  surfaces without moving those downstream contracts here.
use_when:
  - A task names an already-landed source family or platform and asks to capture, route, replay, project, or find lake/cleaning seams.
  - Continuing from the Source Capture Playbook after the access-method read has identified a known source family.
  - Deciding whether a source is already homed or should be treated as a new-source probe under the playbook.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - forseti/product/spines/data_lake/README.md
stale_if:
  - A new source-family capture-to-lake lane lands without a row here.
  - A source-family README, runner, projection helper, or cleaning/lake writer changes materially.
  - Data Lake raw/derived/Silver contracts change the named lake seam files.
```

## Cold-Start Rule

Use this catalog after the Source Capture Playbook has answered the
source-access/method question.

Authority split:

- `source_capture_toolbox/source_capture_playbook_v0.md` owns the source-access
  gate, route-catalog method, and probe/receipt discipline.
- This folder owns the Capture source-family routing home: where to open for a
  known family, which runner/projection/cleaning surfaces exist, and which
  residuals travel forward.
- `forseti/product/spines/data_lake/authority/` owns raw admission, path grammar,
  derived layout, write boundary, Silver, and medallion semantics.
- Projection, ECR, and Cleaning keep their own layer semantics. A source-family
  index can point to them; it must not restate or fork them.

If a source has no row here, treat it as a new-source probe under the playbook.
If a row exists, open the family index first and confirm the named code/docs
before making strict or actionable claims.

## Lane Index

| Source family / route | Open first | Primary access/method home | Capture / packet seam | Projection / lake / cleaning seam | Current posture |
| --- | --- | --- | --- | --- | --- |
| Fragrance native database: Fragrantica, Parfumo, Basenotes | `forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md` | `docs/research/orca_fragrance_native_database_live_probe_v0.md`; `docs/workflows/parfumo_targeted_capture_contract_v0.md`; Source Capture Playbook | `run_fragrantica_mgt_capture.py`, `run_parfumo_mgt_capture.py`, `run_basenotes_mgt_capture.py` | `fragrantica_projection.py`, `parfumo_projection.py`, `basenotes_projection.py`; cleaning lake adapters; Data Lake authority docs | Current-window / targeted source-native capture lanes; no full-corpus or demand claim. |
| Retail/PDP, including fragrance purchase-review retailers | `forseti/product/spines/capture/core/source_families/retail_pdp/README.md` | Retail/PDP contracts and sidecar playbooks in this family; Source Capture Playbook | CloakBrowser packet runner sidecar; fragrance review rendered/widget companion and lake-packet runners | `retail_pdp_projection.py`, `fragrance_review_lake.py`; Data Lake authority docs | Retail/PDP projection and preserved-body seams; no ECR/Cleaning/Judgment claim from the family index. |
| Vendor pricing page | `forseti/product/spines/capture/core/source_families/vendor_pricing_page/README.md` | Source Capture Playbook; rung-1.5 embedded-payload extraction doc | `run_source_capture_price_payload_packet.py` | `price_payload_extraction.py`; Data Lake authority docs | Narrow SPA/JS-payload pricing route under `source_family="vendor_pricing_page"`; not rendered retail price, standing scheduler, ECR/Cleaning/Judgment, or price truth. |
| Instagram public creator/reels capture | `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md` | Instagram capture findings, route docs, and Source Capture Playbook | IG grid/audio/deep-capture runners; audience post-text packet seam | IG projection helpers, deep-capture lake adapter, audience-post Cleaning adapter, IG product-extraction lane; Data Lake authority docs | Multiple public-web routes landed; durable media/video and scale residuals remain source-family local. |
| TikTok public/sessioned creator capture | `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md` | TikTok capture lane spec, blocker playbook, Source Capture Playbook | Live one-creator staging, grid-only daily heartbeat, and batch-admission runners | Shared social heartbeat control; TikTok batch coverage/projection helpers; Data Lake authority docs | Daily multi-creator mechanics exist; live scale, account safety, numeric-account served binding, and durable media remain residuals. |
| YouTube public watch/Shorts/transcript capture | `forseti/product/spines/capture/core/source_families/social_media/youtube/README.md` | YouTube agent playbook and recon | Watch, caption, ASR, RSS monitor packet runners; audience post-text packet seam | YouTube metric rollup producers, transcript product Cleaning/Silver lane, audience-post Cleaning adapter; Data Lake authority docs | Public YouTube route is source-family specific; comments/transcripts/products carry their own residuals. |
| Reddit bounded candidate/intake/capture | `forseti/product/spines/capture/core/source_families/social_media/reddit/README.md` | Reddit operator playbook, candidate intake/Graph Frontier contracts, Source Capture Playbook | Old Reddit direct HTTP batch, consolidation, archive fallback, one-URL CloakBrowser when needed | Reddit consolidation/projection/ECR consumption findings; Data Lake authority docs | Pre-commercial bounded route only; no broad crawl, monitoring, or commercial Reddit authority. |
| Creator registry / public-handle linkage | `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md` | Creator registry specs | Static ledgers/materializers, not a live capture runner | Creator profile current view / Creator Signal surfaces | Cross-platform known-account preflight and profile-current view, not a source-access lane. |
| Cross-archive historical capture (not a source family) | Source Capture Playbook, section "Cross-archive historical capture"; `orca-harness/source_capture/historical_capture.py` | Source Capture Playbook | `run_source_capture_historical_packet.py` | Data Lake authority docs if raw packets are written | Cross-source route for historical/pre-cutoff state; do not create a fake source-family identity. |

## Enforcement Candidate (Evaluated, Not Built)

A future advisory hook could compare changed files under `orca-harness/source_capture/`,
`orca-harness/runners/`, and `orca-harness/cleaning/` against this catalog when a
patch introduces or changes source-family/source-surface-specific capture-to-lake
behavior.

Do not build that hook in this lane. The current smallest complete fix is the
route layer itself. A hook needs a careful extractor so it does not false-positive
on shared runners, generic packet writers, generic Data Lake helpers, or Cleaning
base classes. Build it only under separate bounded authorization, or after another
missed family-index row proves the route layer alone is not enough.

## Non-Claims

This catalog is not source-access permission, live network authorization,
validation, readiness, fixture admission, lake contract authority, ECR or
Cleaning authority, Judgment, buyer proof, source completeness, or commercial
readiness. It is a routing layer so a cold reader can find the correct owning
lane without searching the whole repo.
