```yaml
retrieval_header_version: 1
artifact_role: build architecture decision/plan (non-authorizing; planning-only)
scope: >
  Target build architecture for operationalizing IG wind-caller CALLS self-capture
  (per-item post + reel caption + engagement) on attended, logged-in, ≤5 public-figure
  accounts. Decides how to COMPOSE the already-built authenticated-browser capability
  plus the small IG-specific delta, names the few genuinely-architectural choices, maps
  authorization, and gates the build on the H5 cadence probe. Downstream of the IG
  capture-feasibility recon.
use_when:
  - Scoping or authorizing the IG calls-capture build.
  - Checking what already exists vs what is net-new for IG capture.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - The authenticated-browser adapter / auth_state / cadence primitives change shape.
  - The H5 cadence probe result flips the A2 fork (plain-headless vs session+anti-detect).
  - The owner sets the retention/purge horizon (currently an open prerequisite).
status: PLANNING_DRAFT — pre-scoping; not a build authorization
```

# IG Wind-Caller Calls-Capture — Build Architecture (v0, planning)

## Headline: this is mostly COMPOSE + a small delta, not a net-new build

A 3-lens architecture pass (read-only subagents) + home-model verification against primary
source found the **authenticated-browser capability already exists, is tested, reviewed, and
authorized.** The IG work composes it; it does **not** build an auth capability from scratch. This
**corrects** the recon's earlier build-lane finding (which inspected only the anonymous
`cloakbrowser_snapshot.py` and overstated the gap — see the recon doc's dated correction).

## What already exists (verified, with paths)

| Piece | Path | What it gives |
|---|---|---|
| Authenticated adapter | `orca-harness/source_capture/adapters/browser_snapshot.py` | Loads a saved session (`storage_state_path`) into a Playwright context; returns rendered DOM + visible text + viewport screenshot + metadata (`storage_state_loaded`); single URL; `headless=True`; no proxy/scroll/sniff. |
| Session store | `orca-harness/source_capture/auth_state.py` + `local_secret_store.py` | `AuthenticatedSessionMode`, storage-state JSON validation, metadata-sidecar mode binding, path confinement, size cap. Secret lives in gitignored `_auth_state/`. |
| Interactive login | `runners/run_source_capture_browser_session_bootstrap.py` | `headless=False` + human `input()` — the **owner** enters credentials; the agent never does. |
| Capture→packet | `runners/run_source_capture_authenticated_browser_packet.py` | Loads session → captures one URL → Source Capture Packet; generic login-wall limitation detector; non-claims forbid credential/cookie/storage-state capture; records `access_posture` with `session_mode` (not the secret). |
| Cadence governor | `orca-harness/source_capture/cadence.py` | `build_cadence_plan(mode="bounded_jitter", window/min_gap/max_gap/seed)` → per-item variable waits; deterministic-per-seed for auditability. Already driven item-by-item in the Reddit batch runner. |
| Tests + review + authorization | `tests/unit/test_source_capture_authenticated_browser_snapshot.py`; `docs/review-outputs/source_capture_authenticated_browser_snapshot_adversarial_code_review_v0.md` (+ post-patch recheck); `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` (1st-tranche #5 honest/authenticated browser; 2nd-tranche #7 owner-named source adapters). |

## The IG delta (what is net-new)

- **D1 — Multi-item capture loop (NEW runner).** Grid scroll-enumerate (`/p/` + `/reel/` permalinks; reuse the scroll mechanics) → per-item visit → packet, with `cadence.py` `bounded_jitter` between items. The existing runner is single-URL; this is a bounded multi-item runner that *composes* it.
- **D2 — IG extraction (parser).** Caption from the rendered DOM node (the meta truncates ~59–86%); engagement (likes/comments/date/`#ad` sponsorship) from `og:description`/DOM. Parser-over-retrieved-HTML is explicitly allowed by the authorization; cross-check the DOM caption against the meta prefix, flag mismatch, never silently truncate.
- **D3 — Reel view/play count via WARM SAME-CONTEXT JSON.** Not in the page DOM; in the media GraphQL JSON. This is **not a new method** — it is the **authorized Reddit "load page in-context, then read its own JSON" enrichment pattern** (build-authorization, Anti-Blocking/Reddit-ordering amendment) applied to IG. Needs a response-read hook the current adapter lacks.
- **D4 — IG block signature.** Extend the generic login-wall detector with IG markers (login-modal / `challenge` / 429-interstitial).

## Genuinely-architectural choices (small)

- **A1 — Loop home.** RECOMMEND a **new runner** composing the existing single-URL adapter N times (lowest lock-in; the adapter stays single-purpose) over a new multi-item adapter. Low stakes; reversible.
- **A2 — The one real fork (H5-gated).** The anti-detect path (`cloakbrowser_snapshot`, no session) and the session path (`browser_snapshot`, no anti-detect) are **separate**; neither does **session + anti-detect together**. If plain authenticated-headless survives the H5 cadence probe → no merge (small). If IG flags it → we need a combined session+cloak capability (**bigger lift, higher lock-in**). **Do not pre-decide; the H5 probe decides it.**
- **A3 — Reel-JSON method scope.** Covered by the existing warm-same-context-JSON authorization (above); confirm with owner only because it reads the page's own API responses.

## Doctrine: NOT doctrine-touching

The "no-secret/anonymous" property was a per-adapter property of `cloakbrowser_snapshot`/`direct_http`, never repo-wide doctrine. The authenticated session store is an **already-authorized, already-reviewed** exception with explicit secret confinement (authorization 2nd-tranche invariant: "credentials, tokens, cookies, and storage-state never enter the packet … live in local ignored config only"; runner non-claims say the same). No new owner doctrine decision is needed for secret-handling.

## Authorization map (what's covered vs to confirm)

- **Covered:** authenticated browser snapshot on an owner-named source (1st-tranche #5 + 2nd-tranche #7) + the wind-caller carve-out (the person-level permission, ≤5 public-figure accounts, attended, human-mimicking, internal-only).
- **To confirm with owner before build:** (i) the **multi-item loop framed as a bounded capture unit** — one named account = the bound, NOT broad/site-wide walking (mirrors the authorized Reddit "bounded unit = subreddit/thread-family" language); (ii) the **reel media boundary** — we capture caption text + engagement counts, NOT video bytes; (iii) the carve-out's required **retention/purge horizon** must be owner-set **before the first durable session** (currently open — a prerequisite, not a code task).

## H5 gate (the build's premise — run before scaling)

Bounded ~20–30-item slice on ONE already-authorized account at full `bounded_jitter` cadence, BEFORE any full-account walk. Abort signal = login-wall modal / IG `challenge` / HTTP 429 / `access_blocked`. Pass = sample completes clean, captions non-empty, engagement parsed. This **also resolves A2** (plain-headless suffices vs need session+anti-detect). Goal: do not build the full walk then discover cadence fails.

## Cadence governor (reuse `cadence.py`)

`bounded_jitter`: inter-item ~8–45 s jitter; inject a long 90–180 s pause every ~5–9 items; randomize visit order; **per-session ≤40 items; ≤2 sessions / ≤60 items per day; ≤5 accounts total**; deterministic-per-seed for auditability; **no scheduler entrypoint** (operator launches each attended run).

## Record boundary

Per-item → **Source Capture Packets** via the existing `write_local_source_capture_packet` (one packet per item, or one packet with N `SourceCaptureSlice`s). The calibration ledger is a **downstream consumer** of packets. **ECR / Cleaning / Judgment schema design is OUT** (confirmed by the runner non-claims + the recon).

## Next steps (each gated)

1. `workflow-implementation-scoping` over D1–D4 + A1 (read-only route; STEP-*).
2. Owner confirms the three authorization deltas + sets the retention horizon.
3. **H5 gate probe** (bounded) → resolves A2.
4. Bounded build authorization → build the delta → full offline contract suite green before any green claim.

## Non-claims

Planning draft. Not a build authorization, not validation/readiness, not a doctrine change, not an authorization-scope ruling (the owner adjudicates the three deltas), not ECR/Cleaning/Judgment design. The existing-capability claims are verified against primary source at the paths cited; the authorization mapping is an advisory reading of the cited decision, not an owner ruling.
```
