# TikTok Sessioned Capture + Warm-Probe Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Capture probe plan
scope: Runbook for sessioned/cookied TikTok capture via a dedicated account, plus a warm-session detection-ceiling probe that measures how far the paced per-page capture pattern survives before a real challenge.
use_when:
  - Setting up or running authenticated TikTok capture after the owner pivot to sessioned.
  - Measuring the per-account detection ceiling before any scale run.
authority_boundary: retrieval_only
status: plan + expanded partial sessioned DOM/hydration receipts; full packet-response contract and per-account ceiling still UNMEASURED. Execution remains gated (human login + per-operation network approval).
derived_from:
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md   # C1–C8' invariants
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md   # what's reachable + detection addendum
authorization:
  direction: owner decision 2026-06-22 — pivot to sessioned/cookied
  execution_gates:
    - human-performed login of a DEDICATED account (agent never enters credentials)
    - per-operation network approval at runtime
    - owner acceptance of account-ban risk for the dedicated account
non_claims: one-account/one-session measurement; ban risk accepted; public content only; not validation/readiness; not legal advice
```

## Objective

Two outputs from one runbook:
1. **Capture:** per-video creator-momentum metadata + top/relevant comments (with exact `create_time`/`cid`/`uid`), under an authenticated session, at the spec's paced per-page pattern.
2. **Measurement:** the **per-account detection ceiling** — how many videos the paced pattern captures from one warmed account before TikTok issues a real challenge — which sets the scale math (`throughput ≈ accounts × per-account-ceiling × paced-rate`).

## Latest partial execution receipt

`docs/workflows/tiktok_sessioned_warm_probe_receipt_v0.md` records a 2026-06-30
N=1 headed sessioned probe on the pinned first-slice fixture. The sessioned route
loaded without visible login/challenge signals, parsed the embedded video-detail
blob, and rendered visible comment DOM after a comments-control click.

`docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md`
extends that DOM/hydration evidence in the same lane: one Chrome TikTok tab,
public content only, no session-secret reads, 94 `@tiktok` profile-grid anchors
after bounded scroll, exact video-detail hydration for the pinned fixture, and
20 visible top-level comment DOM rows.

Neither receipt captured `/api/comment/list` response bodies, so the exact
comment packet contract (`cid`, `uid`, exact `create_time`, cursor, `has_more`)
and the per-account ceiling remain unmeasured.

A later existing-Chrome diagnostic confirmed that the already-running user
Chrome session can render the pinned video comments without a visible login gate
or challenge, but the current Chrome-extension surface exposes only DOM and
`pageAssets`, not XHR/fetch response bodies. Do not spend more probe budget on
Chrome-extension DOM reads for packet proof; the remaining bottleneck is a
response-body capture surface for the page-owned comment request.

## Pre-conditions (all required before any capture)

1. **Dedicated, non-personal account.** Never a personal/primary account. Treat it as **burnable**; a ban costs only this account.
2. **Human-performed login.** A human logs the dedicated account in headed; the agent **never** enters credentials. (`run_source_capture_browser_session_bootstrap.py` saves the session; nothing about the credentials is captured.)
3. **One session per context, no concurrent/duplicate TikTok tabs** in that browser (the recon captcha was likely a duplicate-session trigger — do not reproduce it).
4. **Warm the session first:** before capture, some ordinary human-like browsing on the account (watch a few videos, normal pace). Session trust/warmth is the lever we identified; a cold session is the worst case.
5. **Per-operation network approval** granted at runtime; logged-in but **public content only** (no DMs/private/access-controlled surfaces).

## Capture pattern (per video — from the spec, ≤3 requests)

1. Load the video page in the **real authenticated browser context** (non-headless). Read metadata from `#__UNIVERSAL_DATA_FOR_REHYDRATION__` → `webapp.video-detail` (raw stats + `createTime` + author + `authorStats`). **0 extra requests.**
2. Trigger the comment panel (one programmatic click — there is no native default-to-Comments; confirmed). **Intercept** the page's own `GET /api/comment/list` response (hook `fetch`/`XHR`); never forge `msToken`/`X-Bogus`.
3. Capture the **first comment page + at most ONE pagination** (top/relevant; no chronological census). Extract `cid`, `text`, `create_time`, `digg_count`, `reply_comment_total`, `user{uid, unique_id, nickname}`.
4. **Human-rate cadence with jitter** between videos (`cadence.build_cadence_plan(bounded_jitter)`); start ~2.5–4 s, never sub-2 s; re-measure.

## Warm-probe / ceiling measurement

Run the capture pattern across an **escalating batch** from the single warmed account, watching for the first real challenge, and record where it appears:

- Batch ladder (one account, sequential, paced): **1 → 5 → 20 → 50 → 100 videos** (stop early on any challenge).
- After each video record: requests used, captured-ok vs blocked, and any challenge signal.
- The result is the **per-account ceiling** = videos captured cleanly before the first challenge, at the paced rate. Repeat on a fresh warmed account only if the owner wants a second data point.

## Stop conditions (any one → stop that account immediately)

Slider/"verify" captcha; account challenge or logout-forced; ban/40x on the authenticated session; `msToken`/signature rejection; empty/stripped page; operator concern. On any: **stop that account, record the ceiling point, cool down; never solve a challenge; do not rotate to a new account within the same run without owner say-so.** Distinguish a real TikTok signal from transport/infra glitches (e.g., an extension `[BLOCKED: JWT token]` `chrome-error` is infra, not TikTok — retry once).

If a cold lane is confounded by whether a blocker should use UI movement, open
`docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md`. It names
the allowed bounded pointer-action substrate for benign overlays, comment routing,
DOM close diagnosis, and visual-X close diagnosis, and it forbids treating any
challenge-close click as capture success.

## Receipts / measurement ledger (no secrets — C7/G-2)

Per run record: account label (not credentials), session mode (`entitled_session`), warm-up performed, batch ladder reached, per-video request count, **first-challenge point (video N + observed rate)**, verdict, and limitations. **Never** record credentials, cookies, storage-state, `msToken`, proxy endpoints, or exit IPs.

## Outputs / verdict

- A **measured per-account ceiling** at the paced pattern → feeds the scale math and the self-capture-vs-vendor decision (recon/scaling analysis).
- Confirmation that the sessioned capture pattern returns the spec's data contract (metadata + top comments + exact timestamps) under an authenticated session.
- An honest statement of whether sessioning materially raised the ceiling vs logged-out.

## Harness fit

Reuse: `browser_snapshot.py::fetch_browser_page_observation_capture` (page response observer plus post-load comment-panel action), `cadence.py` (C4), `auth_state.py` + `run_source_capture_browser_session_bootstrap.py` + `run_source_capture_authenticated_browser_packet.py` (sessioned context, human login), `packet_assembly`/`writer` (receipts), `block_shell`/`rendered_access` (challenge detection). New TikTok-specific: `tiktok_parse.py` (blob + comment-list parsers) and the sessioned capture runner that enforces the ≤3-request cap + stop-on-challenge. The change vs the failed headless runs is **non-headless + warmed authenticated session plus page-owned response observation**, not forged request logic.

## Non-claims

One account, one session, one measurement run. A measured ceiling is for that account/IP/fingerprint at that time; it does not generalize to a guaranteed scale rate. Sessioning trades a recoverable captcha for an account ban — accepted for a dedicated burnable account, not a personal one. Public content only via an entitled session; commenter handles/uids are public comment metadata for aggregate integrity analysis, not individual dossiers. No build/deploy authority; not legal advice.
```
