# Source Capture Agent Runbook

This runbook is for agents operating the Source Capture Toolbox from
`orca-harness/`. It tells an agent how to run the existing packet writers and
how to report what happened without deciding source meaning.

Use this when an agent is given concrete capture inputs. Do not use it for
source discovery, evidence selection, credibility judgment, Cleaning, ECR field
design, or autonomous crawling.

## Agent Boundary

The agent may:

- run the local-file packet runner against already-local source files;
- run Direct HTTP against one explicitly supplied ordinary HTTP URL;
- run Media / Asset capture against explicitly supplied asset URLs;
- run Archive.org capture against one explicitly supplied original URL;
- run Browser Snapshot capture against one explicitly supplied URL that needs
  anonymous browser rendering or screenshot preservation;
- inspect `manifest.json`, `receipt.md`, and `raw/`;
- report packet path, exit code, preserved files, warnings, and limitations.

The agent must not:

- decide whether evidence is true, important, credible, duplicative, or useful;
- infer source meaning beyond reporting preserved source-visible text or files;
- choose targets through broad search or crawling;
- discover hidden media, parse galleries, recurse through pages, or run OCR;
- use unbuilt or separately gated methods from this runbook, including
  logged-in browser session/profile/cookie/storage-state reuse, APIs, SDKs,
  scraper frameworks, proxy/session behavior, anti-detect behavior, CAPTCHA
  solving, or commercial fetch services;
- use no-entitlement login bypass, credential misuse, undisclosed session/cookie
  use, or any method Orca would refuse to disclose internally;
- claim validation, readiness, ECR receipt, Cleaning output, Judgment output,
  buyer proof, or commercial readiness.

If the requested capture needs anonymous browser-rendered content, JavaScript
rendering, or screenshot preservation for one supplied URL, use the Honest
Browser Snapshot runner. If it requires login-visible or entitled content through
stored sessions, browser profiles, cookies, credentials, or storage-state files,
stop with `visible_capture_limitation`: that browser-session extension is not
built in v0.

The agent cannot reliably know browser-rendering or login-wall posture before
running a byte-preserving adapter. A Direct HTTP, Media / Asset, or Archive.org
exit code `0` proves only that bytes were preserved into a packet. It does not
prove source-meaningful content was captured. If the decision question targets
content that is commonly JavaScript-rendered, login/entitlement-gated, or
browser-visible only, or if the preserved body appears to be an app shell,
consent wall, cookie wall, auth/login wall, bot-block page, or other
non-content shell, report `visible_capture_limitation` and consider Browser
Snapshot only when the operator authorized that next runner. Do not describe any
packet as a clean content capture merely because bytes or browser artifacts were
preserved.

If preserved or fetched content is obviously private, confidential,
cross-account, admin-only, or workspace/team spillover, stop and flag it for the
operator. Do not report it as a clean capture. The boundary call belongs to the
operator/owner, not the agent.

## Required Inputs

Before running anything, the agent must have:

- `decision_question`: the capture question supplied by the operator;
- `output_directory`: a new, empty packet directory path;
- one concrete source input:
  - local file path for local-file packets;
  - ordinary HTTP URL for Direct HTTP;
  - explicit media/asset URL list for Media / Asset;
  - original URL plus optional cutoff timestamp for Archive.org;
  - ordinary URL for Browser Snapshot;
- enough context to set `cutoff_posture` or explain why cutoff posture is
  unknown.

For the local-file packet runner only, the agent must also have:

- `source_family`: operator-supplied source-family label. If the operator did
  not supply one, do not infer it from file contents; stop or use an explicitly
  authorized neutral value such as `operator_unspecified`.
- `source_locator` or `source_locator_unknown_reason`: operator-supplied
  provenance pointer, or a visible reason no stable locator was supplied.

Direct HTTP, Media / Asset, Archive.org, and Browser Snapshot runners have
default source-family labels and URL-derived locators; do not ask for
local-file-only fields when those runners are used.

If any required input is missing, do not invent it. Stop and report the smallest
missing input.

## Runner Selection

Use the narrowest runner that matches the supplied input.

| Supplied input | Runner | Use when |
| --- | --- | --- |
| Already-local raw source files | `run_source_capture_packet.py` | The operator already preserved files and only needs a packet. |
| One ordinary URL | `run_source_capture_http_packet.py` | A single page/file may be fetched through normal Direct HTTP. |
| Explicit asset URLs | `run_source_capture_media_packet.py` | The operator supplied image/media/gallery-frame URLs directly. |
| Original URL plus archive need | `run_source_capture_archive_packet.py` | The operator needs Archive.org availability and maybe snapshot body. |
| Browser-rendered or screenshot-needed page | `run_source_capture_browser_packet.py` | One supplied URL needs anonymous browser rendering or screenshot preservation. |
| Login-visible or entitled browser session content | none yet | Stop; v0 does not use stored sessions, profiles, cookies, credentials, or storage-state. |

If a supplied URL points directly to a source-meaningful asset, prefer Media /
Asset. If it points to a page or file whose whole response body is the capture
target, prefer Direct HTTP. If unclear, stop and ask for the operator's intended
runner rather than guessing from URL shape.

Do not chain runners unless the operator explicitly asks for multiple packets.
For example, do not run Archive.org automatically after Direct HTTP fails unless
that fallback was requested.

## Output Directory Discipline

Use a fresh directory under `_test_runs/` for smoke tests or under
`reports/source_capture/` for local review evidence. Do not overwrite existing
packet directories.

`_test_runs/` is ignored local scratch. `reports/source_capture/` is not
ignored by default and may be git-tracked. Packets can contain copied raw
third-party source files, media, archive snapshot bodies, and machine-specific
provenance paths. Do not stage or commit generated packet directories or raw
packet contents without an explicit owner decision.

Generated packets are discovery-grade capture outputs. They are not rights,
retention, sensitivity, material-use, client-use, or durable-evidence clearance.
If downstream Judgment or client-facing work would make a packet material,
follow the source-access boundary decision and perform clean
reacquisition/verification through the normal disclosed path before relying on
it materially.

Recommended naming:

```text
_test_runs/source_capture_<runner>_<short_slug>
reports/source_capture/<case_or_slot>_<runner>_<short_slug>
```

Generated packet directories are not canonical fixtures unless a separate
fixture-admission decision says so.

## Commands

Run from `orca-harness/`.

Local file packet:

```powershell
python runners/run_source_capture_packet.py `
  --source-family "<source family>" `
  --source-locator "<source locator or local provenance pointer>" `
  --decision-question "<operator-supplied decision question>" `
  --input-file "<local raw file>" `
  --cutoff-posture "<operator-supplied cutoff posture>" `
  --access-posture "local_file_only" `
  --archive-history-not-attempted-reason "local packet runner does not query archives" `
  --media-modality-not-attempted-reason "local packet runner does not retrieve additional media" `
  --output "<packet directory>"
```

Use repeated `--input-file` flags when the operator supplies multiple already
local files for the same bounded source packet. If no stable source locator was
supplied, replace `--source-locator` with:

```powershell
--source-locator-unknown-reason "<operator-supplied reason no stable locator is available>"
```

Direct HTTP:

```powershell
python runners/run_source_capture_http_packet.py `
  --url "<ordinary http or https URL>" `
  --decision-question "<operator-supplied decision question>" `
  --cutoff-posture "<operator-supplied cutoff posture>" `
  --output "<packet directory>"
```

Media / Asset:

```powershell
python runners/run_source_capture_media_packet.py `
  --asset-url "<explicit asset URL>" `
  --decision-question "<operator-supplied decision question>" `
  --cutoff-posture "<operator-supplied cutoff posture>" `
  --output "<packet directory>"
```

Archive.org:

```powershell
python runners/run_source_capture_archive_packet.py `
  --url "<original URL>" `
  --cutoff-timestamp "<YYYYMMDDhhmmss or omit if latest is intended>" `
  --decision-question "<operator-supplied decision question>" `
  --output "<packet directory>"
```

The Archive.org runner derives cutoff posture from `--cutoff-timestamp` when
the operator does not pass an explicit cutoff-posture flag. If latest snapshot
selection is intended, omit `--cutoff-timestamp` and report that no cutoff bound
was supplied.

Browser Snapshot:

The Browser Snapshot runner requires the optional browser dependency and a local
Chromium browser binary before live use:

```powershell
python -m pip install -e .[browser]
python -m playwright install chromium
```

```powershell
python runners/run_source_capture_browser_packet.py `
  --url "<ordinary http or https URL>" `
  --decision-question "<operator-supplied decision question>" `
  --cutoff-posture "<operator-supplied cutoff posture>" `
  --output "<packet directory>"
```

The Browser Snapshot runner uses an anonymous/headless browser path. It
preserves rendered DOM, visible text, a viewport screenshot, and browser
metadata. It does not use stored sessions, browser profiles, cookies,
credentials, storage-state files, anti-detect behavior, proxy behavior, CAPTCHA
solving, crawling, OCR, or source-meaningfulness classification.

## Post-Run Inspection

After a runner returns exit code `0`, inspect:

```powershell
Get-Content <packet directory>\receipt.md
Get-Content <packet directory>\manifest.json
Get-ChildItem <packet directory>\raw
```

The agent report must include:

- runner used;
- command exit code;
- packet path;
- whether `manifest.json`, `receipt.md`, and `raw/` exist;
- preserved file list from `raw/`;
- source slice ids from `manifest.json`;
- access, archive/history, media/modality, cutoff, and re-capture posture from
  `manifest.json` when present;
- warnings and limitations from `manifest.json`;
- any visible access, archive, media, or cutoff limitations;
- receipt non-claims from `receipt.md` or manifest receipt metadata when
  present.

For Archive.org packets, report that `snapshot_count` reflects
`collapse=digest` unique-content snapshot rows returned by the availability
endpoint, not every historical capture timestamp that Archive.org may hold.

For Browser Snapshot packets, report that the screenshot is viewport-only and
that browser artifacts do not prove content sufficiency, login-wall absence, or
source completeness.

Do not summarize the source as true or false. Do not say the capture is ready,
validated, complete, or sufficient for Judgment.

## Exit Handling

Exit code `0` means a packet was written. It does not mean source-meaningful
content was captured, nor that capture is complete or validated.

Exit code `2` means CLI/config/user input error. Report the exact missing or
invalid input and do not retry with guessed values.

Exit code `3` means capture failed visibly and no normal packet was written for
the current network runners. Report the error, the runner used, and the fact
that no normal packet exists.

Current runner exit-code shape:

| Runner | Exit codes | Notes |
| --- | --- | --- |
| Local file packet | `0`, `2` | Missing files, overwrite refusal, and CLI/config errors are exit `2`. |
| Direct HTTP | `0`, `2`, `3` | Network/no-body/size-cap capture failure is exit `3`; no packet. |
| Media / Asset | `0`, `2`, `3` | At least one preserved asset can write a packet with visible failed-asset limitations; all assets failed is exit `3`; no packet. |
| Archive.org | `0`, `2`, `3` | Availability lookup failure is exit `3`; no packet. Metadata-only states can still be exit `0` packets with limitations. |
| Browser Snapshot | `0`, `2`, `3` | Missing Playwright package, missing Chromium binary, navigation failure, or artifact failure is exit `3`; no packet. Exit `0` preserves browser artifacts only, not content sufficiency. |

If a network runner reports a staging-collision or "clear it before rerunning"
message, clear or choose a new output parent only after operator approval. Do
not delete unrelated files.

If a runner writes a packet with limitations, preserve those limitations in the
agent report. Do not patch them away by rerunning a different method unless the
operator authorizes the next method.

## Minimal Agent Report Template

```text
source_capture_agent_report:
  runner: <local_file|direct_http|media_asset|archive_org|browser_snapshot>
  exit_code: <observed exit code>
  packet_path: <path or none>
  packet_written: <yes|no>
  inspected:
    manifest_json: <yes|no>
    receipt_md: <yes|no>
    raw_dir: <yes|no>
  preserved_files:
    - <raw file path or none>
  source_slices:
    - <slice id or none>
  postures:
    access: <manifest access posture or none>
    archive_history: <manifest archive/history posture or none>
    media_modality: <manifest media/modality posture or none>
    cutoff: <manifest cutoff posture or none>
    recapture: <manifest re-capture posture or none>
  warnings:
    - <manifest warning or none>
  limitations:
    - <manifest limitation or none>
  archive_snapshot_count_caveat: <if archive packet, collapse=digest unique-content rows; otherwise none>
  browser_snapshot_caveat: <if browser packet, viewport screenshot and no content-sufficiency proof; otherwise none>
  visible_stop_if_any: <missing input, access failure, browser-needed, no packet, or none>
  non_claims:
    - <receipt non-claim or none>
```

## Testing Before Agent Reuse

Before treating a changed runner as reusable by agents, run the relevant focused
tests and the source-capture stack:

```powershell
python -m pytest -p no:cacheprovider tests/unit/test_source_capture_packet.py tests/contract/test_source_capture_packet_no_runtime_imports.py tests/unit/test_source_capture_direct_http.py tests/contract/test_source_capture_direct_http_contract.py tests/unit/test_source_capture_media_asset.py tests/contract/test_source_capture_media_asset_contract.py tests/unit/test_source_capture_archive_org.py tests/contract/test_source_capture_archive_org_contract.py tests/unit/test_source_capture_browser_snapshot.py tests/contract/test_source_capture_browser_snapshot_contract.py
```

For a new adapter, add focused unit tests, contract tests, one manual dry-run,
and adversarial implementation review before committing it as an agent-facing
primitive.
