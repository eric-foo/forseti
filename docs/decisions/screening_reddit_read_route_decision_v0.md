```yaml
retrieval_header_version: 1
artifact_role: Decision record - screening Reddit read-route (capture-spine provider side)
scope: >
  Records the Main-CA decision on how screening agents obtain Reddit reads, given the 2026-06-12
  tooling discovery that the WebFetch tool blocks reddit.com for screening agents while the
  capture-harness HTTP runners reach it fine (recon receipts). Adopts a layered route - snippets
  default / bounded capture-harness screening-read service / operator-manual fallback - and records
  the service contract the implementation must preserve. The bounded service was wired on the
  `codex/screening-read-service-build` PR branch on 2026-06-21.
use_when:
  - A screen orchestrator needs to know how Reddit or browser-rung screening reads are obtained today.
  - A screen orchestrator needs to know how Reddit origination reads are obtained today.
  - The Walker Equipment Kit's Reddit wall (KNOWN WALLS, point 4) is revisited.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/screening_read_service_build_receipt_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
  - docs/decisions/ingestible_beauty_screen1_ledger_v0.md
stale_if:
  - The screening-read service API, route set, or no-packet/no-ECR boundary changes.
  - The WebFetch tool changes its reddit.com policy (re-decide the default).
  - The owner changes the capture risk posture or the screening-read boundary.
```

# Screening Reddit Read-Route Decision (v0)

## Provenance and authority

Owner-couriered Main-CA commission, 2026-06-12 ("decide the screening Reddit read route").
Recommended by the pre-capture discovery lane (ingestible-beauty screen-1 ledger). Decided by the
Main CA as capture-spine owner (the provider side). The original record was a route decision, not a
build authorization. The wiring was later commissioned and built on 2026-06-21 on
`codex/screening-read-service-build`; see
`docs/workflows/screening_read_service_build_receipt_v0.md`.

## The constraint (why this needed deciding)

Discovered 2026-06-12 (`docs/decisions/ingestible_beauty_screen1_ledger_v0.md`, "Tooling
Discovery"): the WebFetch tool itself blocks `reddit.com` ("Claude Code is unable to fetch from
old.reddit.com") for screening agents - both `old.reddit.com` and `www.reddit.com` - and
`site:reddit.com` search-operator queries return zero. This is an agent-tooling constraint, not a
Reddit-side block: the capture-harness HTTP runners reach these surfaces fine (recon receipts:
old.reddit listing HTTP 200 -> 10 thread URLs; thread body HTTP 200 ~104 KB).

Consequence: the capture lane's GO Reddit read shape (`capture_recon_index_v0.md`, Forums/threads) is
GO for the capture runner but unusable by WebFetch-based screening agents. The outstanding old.reddit
search-surface receipt was therefore closable only by the capture runner, not by a screening agent.
That residual is now closed by the screening-read service build receipt.

## Decision - a layered route

1. **DEFAULT - snippets-only.** Screening walkers may still take Reddit origination signal from search
   snippets when the orchestrator has not invoked a capture-harness screening read. This is the floor,
   not the ceiling.
2. **DURABLE REAL-READ - use the bounded screening-read service.** When a screen needs real Reddit
   reads, its orchestrator invokes the capture-harness screening-read entry under this contract:
   - logged-out public reads only (no logins, no entitled-account use for screening);
   - per-screen bounded - starts and stops with the screen; no standing service, crawler, scheduler,
     or monitor;
   - invoked by the screen's orchestrator, not by walkers directly;
   - entitlement gate first (playbook Step 0 / pattern 4): public content only, never defeat an
     auth/access-control gate; human-rate;
   - no Source Capture Packet / no manifest / no ECR - the entry returns screen-light records only:
     status, bytes, content class, `block_shell` result, and bounded extracted fields;
   - first act = the outstanding receipt, now closed - one bounded GET on
     `old.reddit.com/r/<sub>/search?q=...&restrict_sr=on&sort=new` recording status / bytes /
     `/comments/`-marker count + the `.json` rate ceiling.
   The implemented entry is `source_capture.screening_read.screening_read(...)`.
3. **FALLBACK - operator-manual.** The owner runs fetches for specific threads when the service is not
   available.
4. **BROWSER-RUNG SCREENING READ - use `screening_browser_read(...)` only through the orchestrator.**
   For public challenge-walled pages that need rendering, the wrapper uses the existing
   `cloakbrowser_snapshot` adapter and returns visible text plus `block_shell` classification on
   visible text. It never stages packets, writes manifests, captures screenshots for the caller, or
   touches ECR.

These are non-exclusive layers (graceful degradation), not a single all-in commitment.

## Build closeout (2026-06-21)

The separate authorized capture-lane build turn wired:

- `source_capture.screening_read.screening_read(...)`;
- `source_capture.screening_read.close_old_reddit_search_surface_receipt(...)`;
- `source_capture.screening_browser_read.screening_browser_read(...)`;
- `source_capture.screening_extraction.extract_screening_fields(...)`;
- tests covering entitlement/orchestrator gates, screen-light shape, no-packet/no-ECR, extraction
  range sanity, visible-text-vs-DOM `block_shell`, and first-act receipt shape.

The one structural line the implementation must keep: the service stays per-screen-bounded and
entitlement-gated. A standing screening-read service would be a standing crawler - the exact line the
owner has repeatedly held (capture risk posture; no farm). Bounded-invocation is the difference
between "the runner answers a screen's bounded question" and "a service that watches Reddit."

## Propagation

This branch updates the screening-side Walker Equipment Kit, the beauty venue-card caveat, the old
Reddit handling note, the capture recon index, the Armory README, the Data Capture submap, the repo
map, and the harness README with pointers to the wired screening-read path. Cross-lane ownership
remains the same: this record is the capture-spine provider-side route source; the Walker Kit remains
the scanning-side consumer surface.

## Non-claims

This record is not validation, readiness, merge acceptance, production runtime, source completeness
proof, broad crawling authorization, source-access boundary amendment, commercial fetch permission,
Source Capture Packet output, ECR, Cleaning, Judgment, or buyer proof. The implementation is on the
PR branch until that PR lands.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The bounded Reddit screening-read route moved from deferred build gate to
    implemented PR-branch wiring, and the same screening posture now includes a
    browser/interstitial wrapper over CloakBrowser that returns visible text
    without Source Capture Packet, manifest, ECR, Cleaning, or Judgment output.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - docs/decisions/screening_reddit_read_route_decision_v0.md
    - docs/workflows/screening_read_service_build_receipt_v0.md
    - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
    - orca/product/satellites/beauty/beauty_venue_card_set_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - orca-harness/README.md
  stale_language_search: >
    rg -n "until the cross-lane wiring|bounded screening-read service does not exist|Build gate|search-surface live receipt \\+ rate ceiling pending|screening walks use search snippets until"
    docs/decisions/screening_reddit_read_route_decision_v0.md
    orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
    orca/product/satellites/beauty/beauty_venue_card_set_v0.md
    orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    docs/workflows/orca_repo_map_v0.md
    docs/workflows/data_capture_spine_consolidation_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-21 after propagation. Remaining hits are limited to the
    DCP receipt itself (the search query and this result field). No checked
    downstream surface retained the pre-build, undecided-wiring, or pending
    old.reddit-search-receipt wording.
  non_claims:
    - not validation
    - not readiness
    - not merge acceptance
    - not production runtime
    - not Source Capture Packet generation
    - not ECR, Cleaning, or Judgment design
```
