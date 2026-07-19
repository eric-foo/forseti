# Source Capture — Anti-Block Capture Ladder: Usage Guide & Distilled Lessons v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (Source Capture Armory usage guide / distilled lessons)
scope: >
  How to choose and HONESTLY use the anti-block capture rungs against bot-block
  (403-class) walls on public sources, plus the distilled lessons from the live
  Daimler/Akamai rung-1 result. Read before picking or escalating a rung.
use_when:
  - Choosing or escalating an anti-block rung against a 403/bot-block on a public source.
  - Judging whether an anti-block capture honestly succeeded (esp. for file/PDF targets).
  - Before claiming any anti-block rung is a "settled" capability.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
branch_or_commit: feat/anti-block-http-ladder @ 507c47f (rung-1 arm @ 3ca8090)
stale_if:
  - The anti_blocking_http arm changes from 3ca8090, or a new rung is built.
  - A target wall is observed to behave differently than recorded here.
  - The armory README build order or adapter set is updated (reconcile rung build-states).
```

## Read this when

You hit a `403`/bot-block on a **public** source and need the *lowest sufficient*
honest way through — not "make the 403 disappear." This guide says which rung to
try, how to judge success without fooling yourself, and what each rung cannot do.
Adapter build authority is the build-authorization decision, not this guide.

## The ladder (cheapest-first — cost-ordered, NOT capability-ordered)

| Rung | Tool / runner | Beats | Does NOT do | Build state |
|---|---|---|---|---|
| 0 | `direct_http` · `run_source_capture_http_packet.py` | nothing by design — honest bot baseline; **reproduces the block + yields wall diagnostics** | beat any real wall; impersonate | implemented (armory Direct HTTP adapter) |
| 1 | `anti_blocking_http` (`header_complete_stdlib`) · `run_source_capture_antiblock_http_packet.py` | naive UA/header sniffing — **header/UA-keyed walls** (e.g. the observed Akamai DSU-001 403) | impersonate TLS/JA3; run JS; proxy | **committed @ 3ca8090 (feat branch); not yet merged to main / indexed in README** |
| 2 | `curl_cffi` (TLS/JA3 impersonation) | passive TLS/JA3 **fingerprint** walls (no browser) | run JS; proxy | **NOT built — gated on explicit owner dependency go** |
| 3 | `browser_snapshot` (Playwright headless) · `run_source_capture_browser_packet.py` | **JS challenges** ("checking your browser"); JS-rendered HTML | capture **raw file (PDF) bytes** — no raw-response-body path; defeat anti-headless detection | implemented (armory Honest Browser Snapshot adapter); HTML-oriented; not anti-detect |
| 4 | Patchright (anti-detect browser) | headless-**detection** walls on HTML pages | capture file bytes (same browser limit) | contemplated fallback; not implemented this lane |
| 5 | residential proxy | IP-reputation / geo walls | — | deferred / gated |
| 6 | cloakbrowser | heavy anti-block browser capture | — | **OTHER lane** (third-tranche selected backend); off-limits here; not implemented in README state |
| 7 | `realchrome_cdp` · `run_source_capture_realchrome_cdp_packet.py`; unattended Kohl's wrapper `run_kohls_unattended_capture.py` | **walls that fingerprint the automation/stealth browsers of the lower rungs** — e.g. Akamai denying Direct HTTP, anti-block HTTP, and CloakBrowser (headless *and* headed) cold on any tested egress. A **genuine full Chrome** executes the wall's sensor JS and earns a valid session; a same-site warm hop seeds it even when the hop itself is blocked. Proven on Kohl's `prd-6715879`. | capture raw file bytes; defeat entitled/login gates; prove arbitrary Akamai sites | **implemented** — the generic runner attaches to a real Chrome over CDP; the Kohl's one-shot starts a temporary headful Chrome under Xvfb, captures PDP + policy through the same packet seam, and stops it. Live unattended GO packets: `01KXXV920Z8PQVHP6DN16335DF` / `01KXXVA8B5EHY86N4EJZ7Y6360`. |

Three load-bearing rules about the ladder:

1. **Cost-ordered, not capability-ordered.** A higher rung is not strictly more
   capable. Headless rung-3 can be *weaker* than rung-2 (JA3) against a TLS
   fingerprint wall while costing more. So **"still-blocked at the rungs you
   tried" ≠ unbeatable** — name the untested on-target rung (for a TLS-keyed
   wall that is rung-2, JA3).
2. **Browser rungs (3, 4, 6, 7) capture rendered DOM + visible text + screenshot —
   NOT raw file bytes.** For a **file target** (PDF, zip, xlsx…), the byte-fetch
   rungs are **0 / 1 / 2**. Pointing a browser rung at a PDF measures the wrong
   layer (you get viewer/render artifacts, not the `%PDF-` bytes).
3. **Escalate explicitly, one rung per run. No auto-escalation.** Stop at the
   lowest sufficient rung.

## Pick a rung

1. **Always run rung-0 first as the control.** It reproduces the block and its
   response body + headers **identify the wall**:
   - Akamai → `Access Denied` + `Reference #...` + `errors.edgesuite.net` (seen on Daimler);
   - Cloudflare → `Just a moment...` / `cf-mitigated` / `cf-ray`;
   - others → `Server`, `x-amzn-waf-*`, `x-iinfo` (Imperva), DataDome/PerimeterX headers.
2. **Map wall → rung:** header/UA-keyed → **rung-1**; passive TLS/JA3 → **rung-2** (gated);
   JS challenge → **rung-3**; headless-detected on an HTML page → **rung-4**; IP/geo → **rung-5**;
   automation-fingerprinted even by a stealth browser (e.g. Akamai denying CloakBrowser cold on
   any tested egress) → **rung-7** (genuine Chrome via CDP; a same-site warm hop seeds the wall's
   session). Use the unattended Kohl's wrapper where its exact two-surface admission applies;
   other sources still need their own bounded wrapper or an operator-provided Chrome.
3. **File target?** Never a browser rung for the bytes — stay on **0 / 1 / 2**.
4. **Same-origin set?** Use **probe-one-then-confirm**: run rung-0 control + the
   ladder on one URL, then confirm only the winning rung on the rest. Don't
   brute-force the full URL×rung matrix.

## Judge success HONESTLY (the anti-fake-pass crux)

- `block_shell` classifies a body as **`BLOCK_SHELL` / `EMPTY` / `CONTENT_UNVERIFIED`** —
  there is **no positive `CONTENT` class**, and a `200` is **never** recorded as
  captured content. A binary file → `content_unverified` (honest, not a miss).
- For a **file/PDF target**, decide sufficiency with an **interpretation-layer
  container discriminator** over already-recorded provenance — do **not** weaken
  `block_shell`:
  1. HTTP `2xx`, **and**
  2. no block-shell signature (`content_unverified`, signal `null`), **and**
  3. expected `Content-Type` (e.g. `application/pdf`), **and**
  4. expected magic bytes (e.g. body begins `%PDF-`), **and**
  5. `byte_count == Content-Length`, **and**
  6. `Content-Encoding: identity` (recorded bytes hash-honest as delivered).
- A pass means **"a well-formed-*container* body was retrieved"** — it does **not**
  certify structural validity beyond those checks, nor content authenticity. A
  decoy/challenge `200` could still pass; the claim stops at container-level
  retrieval + byte preservation.

## Operating rules

- **Worktree off committed HEAD** when `main` carries other lanes' uncommitted
  code — run/build there so you never execute other-lane code; keep scratch
  packets in gitignored `_test_runs/`.
- **Live fetch needs per-operation network approval** (sandbox escalation),
  never standing. This ladder is the **anonymous** path — it sends no
  credentials, so it reaches anonymously-served content. If a target needs
  entitled access (login / paywall), this ladder is not the tool: **never
  bypass an unentitled gate** (the hard line), and reach content we are
  *entitled* to (our own free / paid account) via the separate
  authenticated-capture path. A free signup nag over content already served to
  an anonymous request is not a gate.
- Record per URL × rung: HTTP status, `block_shell` verdict, discriminator
  result, and the lowest sufficient rung (or an honest still-blocked).

## Recurring honest limits (carry these forward)

- container ≠ content authenticity / structural validity;
- **current body ≠ pre-cutoff version identity** (a fetched copy is today's, not
  provably the historical original);
- one wall / config / date ≠ a "settled" capability;
- a control proven on one URL ≠ proven for the whole set.

## Evidence to date (one data point)

Daimler DSU-001..003 (Mercedes-Benz IR PDFs) behind an Akamai edge: **rung-1
retrieved all three** (`200` · `application/pdf` · `%PDF-` · size match · identity),
with the rung-0 `403` control proven on DSU-001. The flip was consistent with
header/UA sensitivity (rung-0 and rung-1 share Python TLS; only the header
profile differed) — **not** TLS/JA3 — for that config. Full evidence and honest
limits: the rung-resolution closeout (`open_next`), committed `507c47f`; arm `3ca8090`.

## Non-claims

- Not validation, readiness, acceptance, or a "settled capability" claim.
- Derived from the CA-adjudicated rung-resolution closeout (decision-input
  lineage); it is not new doctrine and does not amend the build-authorization
  decision, the source-access boundary, or the obligation contract.
- Per-rung build authority comes from
  `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`,
  not this guide. Promoting this to canonical armory usage doctrine, merging the
  rung-1 arm to `main`, or indexing it from the README are separate authorized steps.
