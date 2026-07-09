# Source Capture Anti-Blocking HTTP Ladder — Daimler Live Rung-Resolution Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Orca source-capture toolbox closeout (anti-block HTTP ladder live rung-resolution)
scope: >
  Live capture-ladder test of the committed rung-1 anti_blocking_http arm against the
  Daimler DSU-001..003 Annual-Meeting 2019 PDF set after the DSU-001 direct
  control returned HTTP 403, to determine the lowest demonstrated anti-block rung
  for that blocked control and the container-level retrieval rung used for the set.
  Honest representation over
  "make the 403 disappear."
use_when:
  - Choosing an anti-block rung against a header/UA-keyed 403 wall like the observed Daimler/Akamai DSU-001 case (a full browser-like header profile sufficed there).
  - Checking whether the rung-1 anti_blocking_http arm has been live-tested, and against what.
  - Before claiming rung-1 anti-block capability "settled" (this is one data point; see Non-Claims).
authority_boundary: retrieval_only
branch_or_commit: feat/anti-block-http-ladder @ 3ca8090 (the arm under test)
open_next:
  - docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
downstream_consumers:
  - Daimler DSU-001..003 source-body preservation + receipt/registry reconciliation pass (candidate next pass; separate authorization).
  - Any future "rung-1 anti-block capability settled" claim (requires cross-family review).
stale_if:
  - The Mercedes-Benz/Akamai edge reconfigures to TLS/JA3 or behavioral bot checks (rung-1 may no longer suffice).
  - The rung-1 arm changes from 3ca8090.
```

## What this is

A live test of the **committed** rung-1 anti-block arm — not arm construction. The arm
(`anti_blocking_http` adapter + runner + `block_shell` honesty guard) was built,
delegate-reviewed, CA-adjudicated accept-in-full, and committed at `3ca8090`. This run
answers the one empirical question the build left open: **which ladder rung honestly
resolved the observed DSU-001 Daimler HTTP 403** — captured as honest packets and this durable
rung-resolution lesson. Capture date: 2026-06-06.

## Result — sufficient rung, with DSU-001 lowest-rung control

**rung-1 (`anti_blocking_http`, profile `header_complete_stdlib`) is the lowest
demonstrated sufficient rung for the blocked DSU-001 control, and the rung that
retrieved PDF-container candidates for all three DSUs.** Each rung-1 response returned
a PDF-typed body beginning with `%PDF-` that passed the container-level discriminator
(below).

| DSU | URL | rung-0 `direct_http` (control) | rung-1 `anti_blocking_http` | verdict |
|---|---|---|---|---|
| 001 | …/daimler-ir-am-agenda-2019.pdf | 403 Forbidden, `text/html`, 481 B — Akamai "Access Denied" page | 200, `application/pdf`, 2,689,478 B, `%PDF-1.4`, identity, `content_unverified` | **rung-1 container-level retrieval sufficient for this run** |
| 002 | …/daimler-ir-am-hivedownagreement-2019.pdf?r=dai | not independently run; DSU-001 same-origin control only | 200, `application/pdf`, 1,330,478 B, `%PDF-1.6`, identity, `content_unverified` | **rung-1 container-level retrieval sufficient for this run** |
| 003 | …/daimler-ir-am-hivedownreport-2019.pdf | not independently run; DSU-001 same-origin control only | 200, `application/pdf`, 4,121,124 B, `%PDF-1.6`, identity, `content_unverified` | **rung-1 container-level retrieval sufficient for this run** |

Durable evidence — SHA256 of each retrieved body (the scratch bytes are ephemeral; these
hashes are the durable record):

- DSU-001 rung-1 body: `ad2dd0669ebe1dbb5bfd7ba725ff811206f11f8e7ee49b87f623d27fd4c5a843` (2,689,478 B; `Last-Modified` 2022-11-30; `ETag "2909c6-5eea523c85b88"`)
- DSU-002 rung-1 body: `88adb707844353d2064adbe98c28288199ff3109c85645b5e8f008eb80e3b379` (1,330,478 B)
- DSU-003 rung-1 body: `e8d1c83d829a6926af75d0c1ef122110f56631795770244f3e4b10f63fe52a55` (4,121,124 B)
- DSU-001 rung-0 control body (Akamai block page): `bf5f796e1ae58b5927be2a0ddcd74676f8a1239edb5fd5673aa66be80a4ace06` (481 B)

## The wall

**Akamai.** The rung-0 control body is a textbook Akamai edge block: title "Access Denied",
`Reference #18.ed174b17.1780749963.234882d1`, and `https://errors.edgesuite.net/...`
(edgesuite.net is Akamai's domain).

**The observed flip is consistent with request-profile/header sensitivity; TLS/JA3
impersonation was not needed for this run.** rung-1 shares rung-0's stdlib
(Python `urllib`) TLS fingerprint while sending the full desktop-Chrome header
profile (`User-Agent`, `Accept*`, `Sec-CH-UA*`, `Sec-Fetch-*`). That full profile,
not an isolated User-Agent-only change, was the tested difference that flipped the
DSU-001 control from 403→200. Therefore the higher rungs were unnecessary for this
run:

- **rung-2 `curl_cffi` (TLS/JA3 impersonation)** — not needed to retrieve these containers in this run. (Remains gated behind an explicit owner dependency go.)
- **rung-3 `browser_snapshot`** — not run, and independently shape-mismatched for PDF byte capture: the runner preserves rendered DOM + visible text + screenshot with no raw-response-body path, so it cannot return `%PDF-` bytes. Demoted before the run.
- **rung-4 Patchright / rung-5 residential proxy / rung-6 cloakbrowser** — not reached. (cloakbrowser is another lane and off-limits.)

## How "sufficient" was decided — the PDF discriminator

`block_shell` classifies bodies as `BLOCK_SHELL` / `EMPTY` / `CONTENT_UNVERIFIED` with **no
positive CONTENT class**, so a binary PDF returns `content_unverified` (signal `null`) — that
is honest, not a miss. Sufficiency for a PDF target was decided by an **interpretation-layer
discriminator over already-recorded provenance — not by weakening `block_shell`**:

1. HTTP 2xx, **and**
2. no block-shell signature (`content_unverified`, signal `null`), **and**
3. `Content-Type: application/pdf`, **and**
4. body begins with `%PDF-`, **and**
5. `byte_count == Content-Length`, **and**
6. `Content-Encoding: identity` (recorded body bytes are hash-honest as delivered).

All three DSUs passed all six. This establishes **container-level retrieval evidence**:
a PDF-typed body beginning with `%PDF-` and plausible size was recorded as delivered.
It does **not** establish PDF structural validity beyond those discriminator checks,
and it does **not** certify content authenticity. A decoy or challenge PDF could still
satisfy this discriminator; the claim stops at container-level retrieval plus
byte-preservation evidence, not semantic source verification.

## Non-claims / honest limits

- `content_unverified` stands. The PDFs were not parsed or validated for semantic content;
  no claim that these are the authentic agenda / hive-down agreement / hive-down report
  beyond the container-level discriminator above.
- **Version identity:** `Last-Modified` is 2022-11-30 (DSU-001). These are the **current**
  bodies, **post-cutoff** (case cutoff 2019-05-21). Capture does **not** prove pre-cutoff
  version identity; the receipt's `pre_cutoff_identity_not_proven` stands.
- **One data point.** One Akamai configuration, one origin, one date. This is **not** a general
  "rung-1 beats Akamai" claim — Akamai can be configured for JA3/behavioral checks that
  rung-1 would not beat. Elevating this to "rung-1 anti-block capability settled" requires
  cross-family review plus more targets/wall-classes.
- **Same-origin shortcut:** only DSU-001 had an explicit rung-0 `direct_http` 403 control.
  DSU-002 and DSU-003 were retrieved at rung-1 after the DSU-001 control established the
  same-origin block pattern; this closeout does not prove they independently 403 under
  rung-0.
- Not validation, readiness, acceptance, or a registry update. Not the Daimler source-body
  preservation pass.

## Receipt linkage

The receipt `daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md` records a
`stale_if` condition: "Official Mercedes-Benz Group PDF URLs become accessible and bodies are
captured." The observed rung-1 fetch is evidence that this condition needs a separate
reconciliation decision. Reconciling the receipt + source registry and actually preserving the
bodies durably (with SHA256) is a **separate pass** (see `downstream_consumers`), requiring
its own authorization. This closeout does not perform it.

## Reproduce

From the worktree `forseti-harness/`, per URL (public-content-only; live fetch needs
per-operation network approval, never standing):

```
python runners/run_source_capture_antiblock_http_packet.py \
  --url <pdf-url> \
  --decision-question "<question>" \
  --output <scratch-dir> \
  --source-family regulatory_filing \
  --max-bytes 50000000
```

Then apply the six-point discriminator to the preserved `*_response_body.bin` and
`*_response_metadata.json`. rung-0 (`run_source_capture_http_packet.py`) is the honest
control that reproduces the block.
