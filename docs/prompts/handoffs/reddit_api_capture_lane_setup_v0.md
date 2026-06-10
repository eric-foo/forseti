# Reddit API Capture — Lane Setup (fresh-agent handoff)

```yaml
retrieval_header_version: 1
artifact_role: Lane-setup handoff prompt
scope: Spins the Reddit API source-capture path off as its own CA lane for a fresh agent. Covers the adapter/runner build AND the API-access/approval gate.
use_when:
  - Starting the Reddit API source-capture lane from cold.
  - Building or reviewing adapters/reddit_api.py and its runner.
authority_boundary: retrieval_only
load_rule: confirm-don't-trust — re-read every named source before any strict or actionable claim. This prompt is orientation, not authority.
workspace: C:\Users\vmon7\Desktop\projects\orca
expected_branch: main
commit_policy: nothing committed or pushed without explicit owner go.
review_discipline: cross-family adversarial review (different model family) is required before the adapter/runner are treated as settled; same-family self-review is NOT trusted on this lane.
```

## Anchor goal (front-loaded)

Stand up Orca's **Reddit API source-capture path** — build it and get it
**cross-family adversarially reviewed OFFLINE now** (no Reddit approval needed),
while the owner resolves the access-classification gate **in parallel**. The
offline build is the *real* code; the Protocol seam makes offline == live.
**Path-not-proof: nothing runs live without an explicit owner go.**

## Open decision (front-loaded — OWNER-RESERVED; you do NOT make this call)

Reddit's free API tier is **non-commercial** (open-source / academic / personal).
Orca's *eventual product* (competitor intelligence / analytics / SaaS) is
**commercial** by Reddit's own definition (enterprise-gated, reported ~$12k+/yr).
The *current* phase is a pre-revenue solo viability prototype — legitimately
personal/research. The owner submits an **honest** access application (disclose
truthfully, let Reddit classify — no self-labeling to dodge fees, consistent with
Orca's no-undisclosed-access hard stop) and **owns the response**:

- **personal-ok / free granted** → owner authorizes a low-volume live dry-run; data stays scratch.
- **commercial / gated** → owner picks defer / enterprise / substitute source. You present the banked-asset state + options; you do **not** pick.
- **denied / ambiguous** → owner decides reapply / clarify / defer.

You build **Track A regardless** and **surface** this when it resolves. Zero
engineering is wasted in any outcome (the seam + the general credential store are reusable).

## Success signals

1. `adapters/reddit_api.py` + its runner are built to `adapter_author_contract.md`, fully **offline-testable** (fake client; no live network, no `praw`/`requests`/SDK in unit/contract tests).
2. A **mandatory no-secret-in-packet test passes** — no bearer token / `client_secret` / `Authorization` in any packet manifest, `raw/`, or receipt (the AR-02 gate).
3. The adapter/runner pass a **cross-family adversarial review** (different model family) tasked at **secret-leakage**, before being treated as settled; the STEP-06 DCP receipt is **held** until it clears.
4. Provenance guardrail is baked into artifacts: packets stay **scratch**; the live dry-run is owner-gated; a durable **non-claim** that Reddit data may not enter a sold/material Orca product without commercial re-acquisition.
5. No live Reddit call has occurred without an owner go.

## Inherited / settled (verify via confirm-don't-trust; do NOT relitigate)

**STEP-03 credential store — DONE and cross-family-cleared:**
- `orca-harness/source_capture/local_secret_store.py` — shared credential-store security core (directory confinement incl. symlinked-root rejection, label→filename sanitization with a reserved `.meta.json`-suffix guard, size-capped JSON read, sidecar mechanics).
- `orca-harness/source_capture/reddit_credentials.py` — `RedditCredentialMode = owner_registered_script_app`; app-only `client_id` + `client_secret` (NO `refresh_token`); exact-key shape (extra keys rejected); secret-redacting `RedditCredentials.__repr__` (both fields); `load_reddit_credentials(label, *, credential_mode, credential_root=None)` enforces shape + sidecar binding + mode mismatch.
- `orca-harness/runners/run_source_capture_reddit_credential_bootstrap.py` — owner registers an already-placed creds file (no secret flags, no packet). `.gitignore` ignores `orca-harness/_reddit_credentials/`.
- The completion receipt is inline in `orca-harness/docs/adapter_author_contract.md` (frozen-list item names the shared core + the two specializations).

**OAuth — verified against live docs this turn (RE-VERIFY at build time against Reddit's current docs before writing the real client):**
- Token: `POST https://www.reddit.com/api/v1/access_token`, **HTTP Basic** auth (`client_id`:`client_secret`), body `grant_type=client_credentials` (application-only, confidential client, public read-only).
- Authed requests: base `https://oauth.reddit.com`, header `Authorization: bearer <token>`, plus a **descriptive unique `User-Agent`** (generic UAs get blocked/429'd — precedent: `direct_http.DEFAULT_USER_AGENT`).
- Token lives **1 hour, no refresh** → the real client obtains and caches it, re-fetching on expiry.
- Free tier ~60–100 req/min. Endpoints: `/r/{subreddit}/{listing}` (`hot`/`new`/`top`/`rising`), `/comments/{post_id}`.
- If `client_credentials` app-only is gone → **escalate to owner** (the client + STEP-03 schema would need a user-context mode); do NOT improvise.

**Adapter design — specced; do NOT re-derive (build it):**
- `adapters/reddit_api.py`: free function `fetch_reddit_api_capture(*, client, subreddit=None, listing=None, post_id=None, limit=..., ...) -> RedditApiCaptureSuccess | RedditApiCaptureFailure`. Validate native inputs: exactly one of `post_id` XOR `subreddit` (+ `listing`).
- **Thin Protocol seam:** `RedditApiClient` with one method `get(*, path, params) -> <response>` where the response carries `status: int` and `body: bytes` (raw JSON). The adapter owns Reddit endpoint knowledge (`/r/{sub}/{listing}`, `/comments/{id}`); the client owns "authenticated GET → raw bytes + status," hiding all OAuth.
- **Creds-agnostic adapter:** `client` is a **required** param (no default — unlike `browser_snapshot`'s Playwright default, because a real client needs creds). Tests inject a **fake** client; the **runner** builds the real one. The bearer token lives ONLY inside the real client's `get` and is never returned.
- **Real client:** a private `_RedditOAuthClient` (stdlib `urllib`, caches the 1-hr token) + a public factory `build_reddit_oauth_client(*, credentials, user_agent=...)` the runner calls. Lives in `reddit_api.py` (precedent: `_PlaywrightBrowserSnapshotEngine` in `browser_snapshot.py`).
- **Result types mirror `direct_http`:** `RedditApiCaptureSuccess` / `RedditApiCaptureFailure` / `RedditApiCaptureFailureKind` (network/timeout/auth_failed/access_failed/rate_limited/empty/malformed/size_cap), frozen dataclasses, with `warning_notes` / `limitation_notes`, and `metadata` carrying **NO secrets**.
- **post = SourceCaptureSlice, comments per post (batch-over-posts, like `media_asset`):** `post_id` mode = batch of one; `listing` mode = fetch the listing → N post IDs → one `/comments/{id}` per post. Each successful post → a slice with its **verbatim default `/comments` response** (post + comment tree incl. Reddit `"more children"` stubs — **NOT** recursive expansion; note the boundary honestly). Each failed post (deleted/private/429) → a slice with a limitation, **without** aborting the whole capture (the media failed-asset pattern; the honesty validator already handles it). Conservative default `limit` + a cap to respect the 60–100/min budget.

## Lane sequencing (operating rules)

- **TWO PARALLEL TRACKS.**
  - **Track A (you / the CA):** build STEP-04 → STEP-05 → STEP-06 → STEP-07, all **offline against a FAKE client**. No approval needed.
  - **Track B (owner, not you):** submit the honest Reddit access application.
  - The build does **NOT** gate on approval. Only the **live dry-run (tail of STEP-07)** gates on a real `personal-ok` classification **AND** an explicit owner go.
- **Access classification is OWNER-RESERVED** (see Open decision). You surface outcomes + options; you never decide or run live on a self-asserted classification.
- **Provenance guardrail (bake into artifacts; do not decide):** packets stay scratch (no fixture admission — existing armory invariant); the live dry-run is owner-gated + low-volume + only after a real `personal-ok`; a durable non-claim that Reddit-captured data may not enter a sold/material Orca product without commercial re-acquisition (in the runner's `NON_CLAIMS` + the STEP-06 DCP/runbook).

## Build steps (Track A) + review checkpoints

- **STEP-04 — `adapters/reddit_api.py`:** result types + `RedditApiClient` Protocol + `fetch_reddit_api_capture` (batch-over-posts, per-post slice data with raw JSON, partial-failure slices, NO secrets) + the private `_RedditOAuthClient` + public `build_reddit_oauth_client` factory. Export via `adapters/__init__.py`. Unit tests with a **fake client** + a **contract test** (no forbidden imports — explicitly **no `praw`**, mirror `tests/contract/test_source_capture_*_contract.py`).
- **STEP-05 — `runners/run_source_capture_reddit_packet.py`:** `load_reddit_credentials(label, mode)` → `build_reddit_oauth_client(...)` → `fetch_reddit_api_capture(client=..., ...)` → route the result through the shared `packet_assembly.stage_and_write_packet` helper (post = slice; each slice's raw JSON preserved) with a module-level `REDDIT_API_NON_CLAIMS`. Exit codes **0 / 2 / 3** (match the other runners). No secret flags on the CLI (`--credential-label` + `--credential-mode` only).
- **STEP-06 — docs:** add the Reddit runner's Runner-Selection row + the credential-registration command + exit-code row to `orca-harness/docs/source_capture_agent_runbook.md`; flip any README gap note; author the **DCP receipt** (trigger `architecture_doctrine`, likely `related_triggers: [output_authority]`) — **held as a blocker** until the cross-family review clears.
- **STEP-07 — gates + dry-run:** the **MANDATORY no-secret-in-packet test** (seed a recognizable secret into the store, run the runner with a fake client returning canned listing/comments JSON, assert the secret + `Authorization` + token are absent from manifest + `raw/` + receipt — mirror `tests/unit/test_source_capture_authenticated_browser_snapshot.py::test_authenticated_browser_runner_writes_packet_without_state_leakage`); a no-clean-rollup-over-failed-post test; then the **owner-gated** manual live dry-run (only after `personal-ok` + owner go).

**Review checkpoints (this lane's standing discipline):**
- Front-load the **no-secret-in-packet provability** — design the adapter/runner so the AR-02 test is provable from the start, not bolted on.
- After STEP-04 + STEP-05 land (the OAuth client + secret-handling core): **cross-family adversarial review** (different model family) specifically tasked to attack secret-leakage (bearer/`client_secret`/`Authorization` reaching a packet/metadata/log). Layer a cheap same-family mechanical/source-grounded pass under it. **Same-family self-review is not trusted.**
- Patch findings → re-review if needed → only then lift the STEP-06 DCP blocker.
- **Firewall:** if the no-secret test cannot be made to pass → **STOP**; the credentialed adapter is not safe to use live.

## Mandatory discipline / drift-guard

- Follow `orca-harness/docs/adapter_author_contract.md`: `fetch_*` → `Success|Failure`; adapters **never import the writer**; honest `warning_notes`/`limitation_notes`; **no second credential subsystem** (reuse `local_secret_store.py` + the STEP-03 store); **no `praw`/`requests`/SDKs** (stdlib `urllib` only).
- **NO secrets** (bearer token / `client_secret` / `Authorization`) in any packet / metadata / log / result field. Packets record only label / mode / loaded-boolean.
- Re-verify the OAuth flow against Reddit's **current** live docs before writing the real client.
- Nothing committed/pushed without owner. No live Reddit call without owner go.

## Scope / non-claims

Not validation / readiness / buyer-proof / fixture-admission. Not Cleaning or
Judgment. Packets stay scratch. This handoff is orientation + lane setup — **not**
authorization to commit, and **not** authorization to run live. The access
classification and any commercial decision are owner-reserved.

## Owner-reserved decisions

- The access classification + response (free/personal vs commercial; defer / enterprise / substitute source).
- The live dry-run go.
- Any commit / push.

## Source anchors (confirm-don't-trust — read before strict claims)

- `orca-harness/docs/adapter_author_contract.md` — the adapter/runner contract + invariants + the STEP-03 completion receipt.
- `orca-harness/source_capture/adapters/direct_http.py` — transport + result-type precedent (stdlib `urllib`, `Success/Failure/FailureKind`, `metadata`, descriptive UA).
- `orca-harness/source_capture/adapters/browser_snapshot.py` — Protocol-seam precedent (injected engine/client, private real impl, typed failures).
- `orca-harness/source_capture/adapters/media_asset.py` — batch / multi-slice / partial-failure precedent (post-per-slice analog).
- `orca-harness/source_capture/reddit_credentials.py` + `local_secret_store.py` — the STEP-03 store you load creds from.
- `orca-harness/source_capture/packet_assembly.py` — the `stage_and_write_packet` helper the runner uses.
- `orca-harness/runners/run_source_capture_http_packet.py` + `run_source_capture_media_packet.py` — runner precedents that already use the helper.
- `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py` — the no-secret-leakage test pattern (your AR-02 template) + no-secret-flags discipline.
- `orca-harness/docs/source_capture_agent_runbook.md` — the runbook you update at STEP-06.
- Reddit OAuth2 (re-verify): `https://github.com/reddit-archive/reddit/wiki/OAuth2`.
```
