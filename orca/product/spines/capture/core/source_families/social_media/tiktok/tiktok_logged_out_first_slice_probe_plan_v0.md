# TikTok Logged-Out First-Slice Probe Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Capture probe plan
scope: Operational runbook for a single bounded, owner-authorized, logged-out TikTok first-slice probe (one public profile + one public video + that video's first comment page) to discover whether a public-web capture route exists.
use_when:
  - About to run (or authorize the network gate for) the first live TikTok route-existence probe.
authority_boundary: retrieval_only
authorization_status: owner-authorized for the bounded first slice (chat instruction, 2026-06-21); NOT parked pending owner intent. Remaining execution gate is the harness per-operation network permission only (see "Execution gate").
derived_from:
  - docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md  # §4 ROUTE_OPTIONS, §6 LIVE_PROBE_GATE
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_logged_out_sustainability_probe_plan_v0.md  # shape precedent only
authority_boundary_note: planning runbook; running it is a separate runtime act gated below. Grants no build authority; asserts no validation/readiness; not legal advice.
```

## Objective

Resolve the lane's single gating unknown: **does a public, logged-out web route exist that yields source-native TikTok creator/video/comment data?** Output is a route receipt + a verdict, not "all fields captured." A clean `NO-GO`/`CATALOG_GAP` is as valuable as a `GO`.

## Locked subject (chosen before run; no discovery/snowball mid-run)

- Profile: `https://www.tiktok.com/@tiktok` — TikTok's own official, maximally-public, **non-personal** account (market/creator-level public signal, not an individual dossier).
- Video: the first public video surfaced on that profile at run time (record its exact URL in the receipt).
- Comments: the first comment page of that one video.

One subject only. If `@tiktok` itself is walled logged-out, that is itself a strong route signal.

## Execution gate (the ONE remaining unblock)

Owner has authorized the bounded first slice. The remaining gate is **harness-level, not owner-intent**: a live external fetch is denied by the auto-mode classifier until a per-operation network permission is granted (a Bash permission rule for the runner command, or an explicit per-call approval). This plan does not bypass that gate. Confirmed environment readiness: Python 3.11.15, `source_capture` imports OK, Playwright present.

## Route order (cheapest-first; stop at the first wall)

1. **Rung-0 direct HTTP control** — identify the wall from body/headers before any browser. `run_source_capture_http_packet.py`.
2. **Embedded hydration blob (Route 2)** — inspect the rung-0 body (or a logged-out rendered DOM) for a universal/rehydration JSON blob; extract field+value anchors. Loud miss if absent.
3. **Browser-context XHR (Route 4)** — only same-origin, page-emitted requests that run logged-out without invented auth headers/tokens. `run_source_capture_browser_packet.py` (+ context-response capture). **NO-GO** if the data only comes from a signed/authed endpoint.
4. **Cursor-followed scroll (Route 5)** — for comment depth, follow the source's own cursor, not `mouse.wheel`.

Pace: human-rate **~2.5–4 s between reads, never sub-2 s** (IG-derived starting hypothesis, re-measure for TikTok). Ceilings: ≤ ~10 reads total this slice; one subject; one session window.

## Exact runner commands (output to gitignored scratch only)

```bash
# Scratch output (gitignored): orca-harness/_test_runs/tiktok_first_slice_probe/
# Run from orca-harness/. Rung-0 control first:
python runners/run_source_capture_http_packet.py \
  --url "https://www.tiktok.com/@tiktok" \
  --source-family tiktok_creator --source-surface tiktok_profile_http \
  --decision-question "Does a public logged-out route yield source-native TikTok profile data?" \
  --output-directory _test_runs/tiktok_first_slice_probe/profile_http \
  --operator-category probe --capture-mode logged_out_public
# (confirm exact flags via: python runners/run_source_capture_http_packet.py --help)
# Then, only if rung-0 shows a public shell with embedded data or a non-terminal wall,
# escalate ONE rung to the browser packet against the same URL, same scratch dir.
```

Confirm each runner's real flags with `--help` before the first call; the call above is the intended shape, not a verified flag list.

## Receipt (mandatory — the Measurement Ledger / Source Capture Packet)

Every read records: access classification (Step-0), route tried, routes skipped-with-reason, raw body + sha256, source URL, retrieval timestamp, status code, selector/JSON-path anchors (field+value), request rate/volume, block-shell classification, why-stopped, and the verdict. No receipt → no strict interpretation.

## Stop conditions (any one halts immediately)

Login redirect / signup modal / any auth wall; captcha / "verify you are human" / interstitial in visible text; 401/403/429 / rate interstitial / network-security block; any sign content is access-controlled not public; any route reaching a private/signed API behind the auth gate; operator concern; mobile-app-only substrate (→ `CATALOG_GAP`). After any wall: **stop, fully-quiet cooldown ≥ 60 min, do not keep periodically probing.**

## Verdict set

`GO_PUBLIC_LOGGED_OUT_ROUTE_OBSERVED` · `PARTIAL_PUBLIC_ROUTE_OBSERVED` · `NO_GO_AUTH_OR_ACCESS_CONTROL_WALL` · `CATALOG_GAP_MOBILE_OR_VENDOR_ONLY` · `NO_ROUTE_OBSERVED`. Verdict requires checkable source-native evidence (raw bytes/hash + a field+value anchor with URL+timestamp); paraphrase-only → `PARTIAL`.

## Hard boundaries

Public/logged-out only. No login, no own-account, no cookies/storage-state, no proxy/exit-IP, no auth/access-control defeat, no invented auth headers, no signed/private-API replay. Output to gitignored scratch only; nothing durable without a separate request. No recipe card authored as if a route exists — the card is the *output* of this probe (`GO`/`PARTIAL`/`NO-GO`/`CATALOG_GAP`), not a precondition.

## On completion

Record the verdict + receipt; then the owed capture-lane alignment (recon index / probe-lane dated update) can be discharged against an actual observed result rather than a hypothesis.
```
