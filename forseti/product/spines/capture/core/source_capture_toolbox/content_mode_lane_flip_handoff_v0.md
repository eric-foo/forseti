# Content-Mode Lane Flip Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold handoff packet for the all-lanes content-packet flip
scope: >
  Hands ownership of the repo-wide capture-artifact-mode flip (content packets
  as standard posture) to the next lane owner: per-lane survey of every
  projection lane, flip order, retirement semantics for post-hoc projection,
  validation route, and stop conditions.
use_when:
  - Starting or resuming the Phase B content-mode flip for any source family.
  - Deciding whether a post-hoc projection runner or module can retire.
  - Checking which capture runner a family uses before wiring ContentCaptureSpec.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
stale_if:
  - ContentCaptureSpec seam shape changes (forseti-harness/source_capture/content_capture.py).
  - Any lane listed below flips, retires its post-hoc path, or changes capture mechanism.
  - The cloakbrowser packet runner gains or rejects a content-capture seam.
```

## Objective

Make capture-time content packets the standard capture posture for every
projection lane and future incoming source (owner direction, 2026-07-17:
"we want this way for all lanes and future incoming sources too"), retiring
each family's post-hoc projection lane as it flips. Efficiency-first: flips
happen as lanes are next touched, never waiting for volume pressure.

## Authority and Currentness

- The content-mode standard is owned by
  `source_capture_playbook_v0.md` ("Capture artifact mode — content-mode
  standard"); the reference implementation and semantics (content/sample/raw
  modes, provenance floor, raw-fallback, parser-version discipline, parser-fit
  drift check) are the Reddit lane: design doc
  `reddit_radar_grid_capture_maintenance_design_v0.md`, seam
  `forseti-harness/source_capture/content_capture.py`, runner
  `forseti-harness/runners/run_source_capture_http_packet.py`.
- "Projection spine" was never an accepted spine. The operating-model v2
  Bloat-Cut Queue explicitly excludes a "Standalone Projection Spine …
  or any projection practice that drops evidence rows before ECR/Cleaning"
  (`data_capture_harness_operating_model_architecture_v2.md`). There is
  nothing to take down as a spine; retirement is per-family retirement of
  post-hoc projection runners/invocations. Content mode is compatible with
  the bloat-cut clause: it discards raw bytes with hash provenance, never
  evidence rows.
- Retirement semantics (from the Reddit flip): the projector codebase is
  shared between capture-time and post-hoc invocation. What retires per
  family is the post-hoc lane as the standard path. The post-hoc invocation
  survives for sample-mode packets (parser-fit drift checks) and legacy raw
  packets. Bump the family's parser version on any projector behavior change.

## Seam Hardening Provenance

PR #1057 (Reddit Phase A) merged at head `fd93b6c3` before its adjudicated
delegated-review patch could land (a harness outage blocked the apply). The
patch (3 accepted findings: projector-output type guard before raw discard;
honest parse-in-flight reporting on non-2xx fallback; parser-fit checker
trust hardening) lands in the same work unit that carries this packet. If
this packet is readable on main, the hardening is in; further lane flips
build on the hardened seam.

## Lane Survey (verified in-repo, 2026-07-17)

| Lane | Capture mechanism | Post-hoc projection | Flip feasibility |
| --- | --- | --- | --- |
| Reddit grid + threads | HTTP packet seam | `source_capture/reddit_projection.py` (legacy), consolidation | DONE (content mode default; PR #1057) |
| Parfumo MGT | HTTP packet seam (`run_parfumo_mgt_capture.py` calls `http_runner`) | `parfumo_projection.py`, cleaning catchup | NEAREST DROP-IN: seam already available; wire a ContentCaptureSpec projector |
| Fragrantica MGT | 3 slices: direct HTTP + 2 CloakBrowser (initial viewport, deep scroll) (`run_fragrantica_mgt_capture.py`) | `fragrantica_projection.py`, cleaning catchup | HTTP slice flippable now; CloakBrowser slices need the seam extended to `run_source_capture_cloakbrowser_packet.py` |
| Basenotes MGT | Browser snapshot adapter (`source_capture/adapters/browser_snapshot`) | `basenotes_projection.py`, cleaning catchup | Needs cloakbrowser/browser-snapshot seam |
| Retail PDP / retail grid | CloakBrowser packets over retailer PDPs | `retail_pdp_projection.py`, `retail_grid_projection.py` (deterministic per-packet, excerpt-carrying anchors) | Flippable once cloakbrowser seam exists; largest raw pages after Reddit |
| IG reels grid / calls / momentum | Live browser session, passive JSON responses; runner already extracts observations at capture time | `ig_reels_grid_projection.py` (+ catchup with record-id derivation ranks re-reading raw payloads) | DESIGN PASS REQUIRED: catchup semantics depend on raw; do not flip until catchup is re-specified against content records |
| TikTok batch | Video packets (media + metadata) | `tiktok/batch_projection.py` aggregates coverage ACROSS packets | NOT A FLIP TARGET: cross-packet aggregation, media raw is the evidence |
| YouTube behavioral | Metadata packets + captions + ASR across lake | `youtube_capture/behavioral_projection.py` aggregates | NOT A FLIP TARGET as a whole; only per-page watch-metadata parse is candidate |
| LinkedIn live adapter | Live-session runtime extraction | `linkedin_live_adapter/projection.py` per-observation | Already effectively capture-time; audit raw retention posture only |

## Flip Order (recommended)

1. Discharge the open blocker (delegated patch follow-up PR), if not already landed.
2. Parfumo: first Phase B flip (HTTP seam drop-in). Dogfood with a live
   capture + parser-fit check + size compare, mirroring the Reddit dogfood.
3. Extend ContentCaptureSpec to the CloakBrowser packet runner (one bounded
   seam change; same provenance floor and raw-fallback semantics).
4. Fragrantica, basenotes, retail PDP/grid on the extended seam, one family
   per work unit, each with its own parser version constant and drift check.
5. Re-point each family's cleaning catchup consumers at content records, then
   retire that family's post-hoc lane in the same work unit (reconcile the
   family design doc and any playbook mention).
6. IG family: separate design pass for catchup/derivation-rank semantics
   before any flip. TikTok/YouTube aggregation lanes stay as they are — they
   are not raw-to-derived projections.

## Edit Authority, Validation Route, Stop Conditions

- Each flip is one bounded work unit per family requiring explicit owner
  authorization per AGENTS.md (this packet is survey + order, not standing
  implementation authority).
- Validation per flip: family unit tests + full
  `python -X utf8 -m pytest forseti-harness/tests/unit -p no:warnings -q`
  + one live dogfood capture with parser-fit `match` before the default flips.
- Stop and surface to the owner if: a projector needs inputs unavailable at
  capture time; a downstream consumer reads raw bytes directly; the
  cloakbrowser seam extension would change packet manifest semantics for
  existing packets; or a family's raw is itself the evidence (media).

## Non-Claims

Not validation, readiness, owner acceptance of the flip order, ECR/Cleaning
authority, or authorization to implement any flip without a bounded owner
instruction.
