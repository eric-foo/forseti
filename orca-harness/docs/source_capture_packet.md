# Source Capture Packet

The Source Capture Packet is the first bounded Source Capture Toolbox checkpoint
implemented in `orca-harness`. It packages already-local source artifacts into a
local packet directory without fetching anything from a network, browser, API,
archive service, or scraper runtime.

For agent-facing runner selection, stop conditions, and report format, see
`source_capture_agent_runbook.md`.

The same packet shape now also accepts one bounded Direct HTTP capture path. The
Direct HTTP runner may fetch one ordinary `http://` or `https://` URL with
stdlib `urllib`, preserve the raw response body plus selected provenance-safe
response metadata, and then hand those files to the packet writer. It must not
invent a normal packet when the HTTP path returns no body, times out, hits DNS
or TLS failure, or breaches the configured byte cap.

## Local Packet Directory Shape

The runner writes:

```text
<packet directory>/
  manifest.json
  receipt.md
  raw/
    01_<original filename>
    02_<original filename>
```

The Direct HTTP runner stages `http_response_body.bin` and
`http_response_metadata.json` in the output directory's parent while building
the packet, then removes those staging files after the packet writer copies them
into `raw/`.

The Media / Asset runner stages explicit asset files as
`asset_01_body.bin`, `asset_01_metadata.json`, `asset_02_body.bin`, and so on in
the output directory's parent while building the packet, then removes those
staging files after the packet writer copies preserved assets into `raw/`.

The Archive.org runner stages `archive_availability_metadata.json`, and when a
selected snapshot body is preserved, `archive_snapshot_body.bin` and
`archive_snapshot_body_metadata.json` in the output directory's parent while
building the packet. It removes those staging files after the packet writer
copies preserved archive artifacts into `raw/`.

The Browser Snapshot runner stages `browser_rendered_dom.html`,
`browser_visible_text.txt`, `browser_viewport_screenshot.png`, and
`browser_snapshot_metadata.json` in the output directory's parent while building
the packet. It removes those staging files after the packet writer copies the
browser artifacts into `raw/`.

The Authenticated Browser Snapshot runner stages
`authenticated_browser_rendered_dom.html`,
`authenticated_browser_visible_text.txt`,
`authenticated_browser_viewport_screenshot.png`, and
`authenticated_browser_snapshot_metadata.json` in the output directory's parent
while building the packet. It removes those staging files after the packet
writer copies the browser artifacts into `raw/`. The Playwright storage-state
JSON and the small session-mode metadata sidecar used to open the browser
context stay under ignored `_auth_state/` and are not copied, hashed, printed,
or preserved in the packet.

`manifest.json` is the machine-readable packet record. It carries the packet id,
manifest version, obligation-contract version, requested decision context,
source locator/provenance pointer, decomposed timing fields, access posture,
archive/history posture, media/modality posture, re-capture posture, preserved
file metadata, warnings, limitations, and receipt metadata.

`source_locator` is operator-supplied provenance. It may be a URL, absolute
path, relative path, source-system pointer, or unknown-with-reason value. It is
not normalized into a universal locator by this local CLI.

`preserved_files[*].original_path` records the absolute path that the local
operator supplied at packetization time. It is provenance, not a portable live
locator. Use `relative_packet_path` and the copied file under `raw/` for packet
inspection.

`source_slices[*].slice_id` uses ordinal IDs (`slice_01`, `slice_02`, ...).
The default local CLI writes one slice because it packages one bounded local
source set. The writer API also accepts explicit slices for future adapters or
tests that need to preserve per-slice locator, timing, access, archive, media,
or re-capture divergence.

`receipt.md` is the human-readable packet receipt. It restates the requested
context, decomposed timing, preserved files, warnings, limitations, and the
explicit non-claims for this local-file checkpoint.

## Local CLI Boundary

Run from `orca-harness/`:

```powershell
python runners/run_source_capture_packet.py `
  --source-family "docs_page" `
  --source-locator "C:\capture\vendor_pricing_page.html" `
  --decision-question "What did the pricing page show before the decision cutoff?" `
  --input-file "C:\capture\vendor_pricing_page.html" `
  --source-publication-or-event "pricing page date visible in local artifact" `
  --cutoff-posture "pre-decision local capture artifact" `
  --access-posture "local_file_only" `
  --archive-history-not-attempted-reason "local CLI does not query archives" `
  --media-modality-not-attempted-reason "local CLI does not retrieve additional media" `
  --output ".\_test_runs\example_source_capture_packet"
```

If no live or local locator is available, pass:

```powershell
--source-locator-unknown-reason "operator did not supply a stable locator"
```

This CLI packages already-local files only. It fails on missing input files and
refuses to overwrite a non-empty output directory.

Optional metadata flags let an operator preserve known timing, access, archive,
media, actor, mode-change, cutoff, and re-capture posture when that context is
already available. If the operator does not supply a field, the packet records a
visible default such as `unknown_with_reason`, `not_attempted`, or
`not_applicable` rather than silently omitting the field.

Examples:

```powershell
--actor-audience-context "forum posters and commenters"
--source-publication-or-event "thread comments visible in supplied JSON"
--source-edit-or-version-unknown-reason "edit state not exposed in local artifact"
--cutoff-posture "local JSON file state supplied for pressure-test capture"
--recapture-time-not-applicable-reason "first local packetization"
--access-posture "local_file_only"
--access-posture-unknown-reason "operator did not classify access posture"
--access-posture-not-attempted-reason "access posture was not assessed"
--archive-history-not-attempted-reason "dry-run did not query archives"
--media-modality-posture "markdown artifact only; linked media not fetched"
--recapture-relationship-not-applicable-reason "no prior packet supplied"
--visible-mode-change "none observed during local packetization"
```

Only pass one value or reason flag per field. For example, do not combine
`--access-posture` with `--access-posture-unknown-reason`.

## Direct HTTP Boundary

Run from `orca-harness/`:

```powershell
python runners/run_source_capture_http_packet.py `
  --url "https://example.com/page" `
  --decision-question "What did the page return before the decision cutoff?" `
  --cutoff-posture "pre-cutoff direct HTTP capture requested by operator" `
  --output ".\_test_runs\example_source_capture_http_packet"
```

The Direct HTTP runner uses ordinary stdlib HTTP only. It preserves a non-empty
response body plus provenance-safe metadata. HTTP error responses with bodies
can still produce a packet, but the access limitation is visible. Timeout,
DNS/TLS failure, empty-body response, or byte-cap breach fails visibly and writes
no normal packet.

## Media / Asset Boundary

Run from `orca-harness/`:

```powershell
python runners/run_source_capture_media_packet.py `
  --asset-url "https://example.com/source-image.png" `
  --asset-url "https://example.com/source-gallery-frame.jpg" `
  --decision-question "Which source-meaningful media assets were visible before cutoff?" `
  --cutoff-posture "pre-cutoff explicit asset capture requested by operator" `
  --output ".\_test_runs\example_source_capture_media_packet"
```

The Media / Asset runner preserves only operator-supplied explicit asset URLs.
It does not discover assets, parse galleries, parse HTML, inspect CSS, recurse
through linked assets, run OCR, analyze images, query archives, or automate a
browser. It reuses the Direct HTTP helper for ordinary HTTP access.

If at least one asset body is preserved, the runner writes a packet and records
failed or unavailable assets as visible per-slice limitations. If no asset body
is preserved, it fails visibly and writes no normal packet. Non-2xx responses
with bodies can be preserved, but the corresponding slice carries an
`access_failed` limitation.

## Archive.org Boundary

Run from `orca-harness/`:

```powershell
python runners/run_source_capture_archive_packet.py `
  --url "https://example.com/page" `
  --cutoff-timestamp "20240501000000" `
  --decision-question "What archived source state was visible before cutoff?" `
  --output ".\_test_runs\example_source_capture_archive_packet"
```

The Archive.org runner queries a CDX/Wayback-style availability endpoint and
preserves the raw availability metadata whenever that lookup returns a body. It
then selects a snapshot at or before `--cutoff-timestamp` when supplied, or the
latest available snapshot when no cutoff is supplied.

The default CDX query uses `collapse=digest`, so `snapshot_count` reflects
unique-content snapshot rows returned by the availability endpoint, not every
historical capture timestamp that Archive.org may hold for the URL.

Archive availability and archive-body preservation are separate states:

- availability metadata preserved and no eligible snapshot found: packet
  written with metadata only;
- availability metadata preserved and snapshot body preserved: packet written
  with metadata plus body;
- availability metadata preserved but snapshot body retrieval failed: packet
  written with metadata and visible body limitation;
- availability lookup failed before metadata was preserved: no normal packet
  written.

Snapshot body retrieval reuses the Direct HTTP helper. Non-2xx snapshot
responses with a body can be preserved, but the packet carries an
`access_failed` limitation.

The runner does not use browser automation, Archive.org packages, API SDKs,
scraper frameworks, proxy/session injection, anti-detect behavior, CAPTCHA
handling, archived-HTML meaning extraction, OCR, image analysis, ECR, Cleaning,
Judgment, buyer proof, or commercial-readiness logic.

## Browser Snapshot Boundary

Run from `orca-harness/`:

The Browser Snapshot runner requires the optional browser dependency and a local
Chromium browser binary before live use:

```powershell
python -m pip install -e .[browser]
python -m playwright install chromium
```

```powershell
python runners/run_source_capture_browser_packet.py `
  --url "https://example.com/page" `
  --decision-question "What browser-rendered source was visible before cutoff?" `
  --cutoff-posture "pre-cutoff browser snapshot requested by operator" `
  --output ".\_test_runs\example_source_capture_browser_packet"
```

The Browser Snapshot runner uses an anonymous/headless browser path for one
explicitly supplied URL. It preserves rendered DOM, visible text, a viewport
screenshot, and metadata. It uses a fresh browser context and does not accept or
load stored sessions, browser profiles, cookies, credentials, or storage-state
files.

Exit codes:

- `0`: packet written.
- `2`: CLI or user/config error.
- `3`: missing Playwright package, missing Chromium binary, browser
  navigation, or artifact failure; no normal packet written.

The runner writes four deterministic packet inputs before packet writing:

```text
browser_rendered_dom.html
browser_visible_text.txt
browser_viewport_screenshot.png
browser_snapshot_metadata.json
```

The packet writer then copies them into the packet `raw/` directory as numbered
preserved files.

The metadata records requested URL, final URL, page title, capture timestamp,
timeout, wait policy, viewport, screenshot mode, and artifact byte counts. It
does not preserve request cookies, authorization material, browser profiles, or
storage-state files.

The runner does not use anti-detect behavior, proxies, CAPTCHA solving, API
SDKs, scraper frameworks, crawling, OCR, image analysis, ECR, Cleaning,
Judgment, buyer proof, or commercial-readiness logic. A packet proves browser
artifacts were preserved; it does not prove source-meaningful content
sufficiency, login-wall absence, or source completeness.

## Authenticated Browser Snapshot Boundary

Authenticated Browser Snapshot is the manual-login storage-state extension of
Browser Snapshot. It is for one explicitly supplied URL where the operator has
already bootstrapped a permitted browser session under one of the allowed
session modes.

First create local ignored storage state:

```powershell
python runners/run_source_capture_browser_session_bootstrap.py `
  --login-url "https://example.com/login" `
  --state-label "example-client-session" `
  --session-mode "client_provided_session"
```

Allowed session modes are:

- `free_account_created_session`
- `paid_entitled_session`
- `client_provided_session`
- `consenting_coworker_session`

The bootstrap runner opens a headed browser for manual login and writes only a
Playwright storage-state JSON file plus a session-mode metadata sidecar under
`orca-harness/_auth_state/`. It writes no packet. It does not accept username,
password, token, cookie, or profile path arguments.

Then write a packet:

```powershell
python runners/run_source_capture_authenticated_browser_packet.py `
  --url "https://example.com/entitled-page" `
  --state-label "example-client-session" `
  --session-mode "client_provided_session" `
  --decision-question "What authenticated source was visible before cutoff?" `
  --cutoff-posture "pre-cutoff authenticated browser snapshot requested by operator" `
  --output ".\_test_runs\example_authenticated_browser_packet"
```

The authenticated packet preserves rendered DOM, visible text, a viewport
screenshot, and metadata. It records `source_surface` as
`authenticated_browser_snapshot`, records the session mode and state label in
visible packet metadata, verifies the capture-time session mode against the
bootstrap sidecar, and records that storage state was loaded. It does not copy,
hash, print, or preserve the storage-state JSON, metadata sidecar, or
cookie/session values. Operators should choose non-sensitive state labels
because labels are packet-visible.

The runner must not be used for password-driven login automation, direct
profile/cookie import, no-entitlement bypass, anti-detect behavior, proxy
behavior, CAPTCHA solving, crawling, OCR, image analysis, ECR, Cleaning,
Judgment, buyer proof, or commercial-readiness logic. A packet proves
authenticated browser artifacts were preserved; it does not prove entitlement
sufficiency, login-wall absence, source completeness, source truth, or content
sufficiency.

## Direct HTTP Runner

Run from `orca-harness/`:

```powershell
python runners/run_source_capture_http_packet.py `
  --url "https://example.com/page" `
  --decision-question "What did the page return before the decision cutoff?" `
  --cutoff-posture "pre-cutoff direct HTTP capture requested by operator" `
  --output ".\_test_runs\example_source_capture_http_packet"
```

Exit codes:

- `0`: packet written.
- `2`: CLI or user/config error.
- `3`: HTTP/network/no-body/size-cap capture failure; no normal packet written.

The Direct HTTP runner writes two deterministic packet inputs before packet
writing:

```text
http_response_body.bin
http_response_metadata.json
```

The packet writer then copies them into the packet `raw/` directory as numbered
preserved files such as:

```text
raw/01_http_response_body.bin
raw/02_http_response_metadata.json
```

`http_response_metadata.json` preserves only provenance-safe response metadata:

- requested URL
- final URL
- status
- reason
- content-type
- content-length if known
- date
- last-modified
- etag
- capture timestamp
- timeout seconds
- byte count

It does not preserve `set-cookie`, request cookies, authorization material, or
other secret-bearing headers by default.

Non-2xx responses with a non-empty body still produce a packet. The packet
receipt and manifest carry a visible `access_failed` limitation so downstream
layers can inspect the preserved response without mistaking it for a clean HTTP
success.

Network error, timeout, DNS/TLS failure, empty-body response, or byte-cap breach
returns exit code `3` and writes no normal packet.

## Dry-Run Output Lifecycle

Dry-run packet directories under `reports/source_capture/` are local review
evidence unless a separate fixture-admission decision says otherwise. They may
contain machine-specific provenance paths and raw copied source artifacts. Do
not treat them as canonical fixtures, buyer proof, validation evidence, or a
required capture gate merely because they exist in the reports tree.

## Non-Claims

This packet core and local CLI are not source acquisition, direct HTTP fetch,
archive retrieval, media preservation, browser automation, ECR design, Cleaning
implementation, Judgment scoring, buyer proof, or commercial-readiness logic.
The Direct HTTP, Media / Asset, Archive.org, Browser Snapshot, and Authenticated
Browser Snapshot runners are bounded source-acquisition adapters, but they are
still not archive completeness proof, source-state truth proof, password-driven
login automation, credential storage, API SDK use, scraper framework use,
proxy behavior, anti-detect behavior, OCR or image analysis, ECR design,
Cleaning implementation, Judgment scoring, buyer proof, or commercial-readiness
logic.
