# Source Capture Agent Runbook

This runbook is for agents operating the Source Capture Armory from
`forseti-harness/`. It tells an agent how to run the existing packet writers and
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
- run CloakBrowser Snapshot capture against one explicitly supplied URL that
  needs anonymous anti-blocking browser rendering without stored session,
  profile, proxy, or credential injection;
- bootstrap a permitted browser session manually into ignored local Playwright
  storage-state JSON;
- run Authenticated Browser Snapshot capture against one explicitly supplied URL
  using a previously bootstrapped storage-state label and an allowed session
  mode;
- inspect `manifest.json`, `receipt.md`, and `raw/`;
- report packet path, exit code, preserved files, warnings, and limitations.

The agent must not:

- decide whether evidence is true, important, credible, duplicative, or useful;
- infer source meaning beyond reporting preserved source-visible text or files;
- choose targets through broad search or crawling;
- discover hidden media, parse galleries, recurse through pages, or run OCR;
- use methods that do not have an implemented runner in this runbook, including
  password-driven login automation, direct browser profile/cookie import, broad
  crawler/spider frameworks, proxy behavior, standalone CAPTCHA-solving
  services, or commercial fetch services;
- use no-entitlement login bypass, credential misuse, undisclosed session/cookie
  use, or any method Orca would refuse to disclose internally;
- claim validation, readiness, ECR receipt, Cleaning output, Judgment output,
  buyer proof, or commercial readiness.

If the requested capture needs ordinary anonymous browser-rendered content,
JavaScript rendering, or screenshot preservation for one supplied URL, use the
Honest Browser Snapshot runner. If an ordinary browser may pass after visible
launch, a local Chromium channel, or a bounded post-navigation settle delay, use
the Browser Snapshot controls first (`--headed`, `--browser-channel`,
`--settle-seconds`). If those controls are expected to fail or have failed
because the source blocks ordinary browser capture, use the CloakBrowser
Snapshot runner for one supplied URL. If it requires
login-visible or entitled content, use Authenticated Browser Snapshot only when
the operator has supplied an allowed session mode and a previously bootstrapped
local storage-state label. If the operator asks for password automation, direct
profile/cookie import, credentials in flags or environment variables,
no-entitlement bypass, proxy behavior, or CAPTCHA solving through these existing
runners, stop with `visible_capture_limitation`.

For all browser routes, diagnose rendered access from visible text and title
before treating full-DOM challenge markers as decisive. Hidden or residual
Cloudflare/Akamai/Kasada/DataDome/PerimeterX script/template text can remain in
the DOM after source content is visible; record that as a limitation/warning,
not as `access_failed`. If the visible text/title is still an interstitial,
CAPTCHA, or access-block shell, report `access_failed` / PARTIAL even when DOM
and screenshot artifacts were preserved.

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
  - original URL plus optional 14-digit `YYYYMMDDhhmmss` cutoff timestamp for
    Archive.org;
  - ordinary URL for Browser Snapshot;
  - ordinary URL for CloakBrowser Snapshot;
  - ordinary URL, storage-state label, and allowed session mode for
    Authenticated Browser Snapshot;
- enough context to set `cutoff_posture` or explain why cutoff posture is
  unknown.

For the local-file packet runner only, the agent must also have:

- `source_family`: operator-supplied source-family label. If the operator did
  not supply one, do not infer it from file contents; stop or use an explicitly
  authorized neutral value such as `operator_unspecified`.
- `source_locator` or `source_locator_unknown_reason`: operator-supplied
  provenance pointer, or a visible reason no stable locator was supplied.

Direct HTTP, Media / Asset, Archive.org, Browser Snapshot, CloakBrowser
Snapshot, and Authenticated Browser Snapshot runners have default source-family
labels and URL-derived locators; do not ask for local-file-only fields when
those runners are used.

For Archive.org, preflight the cutoff timestamp before running. If supplied, it
must be exactly 14 digits in `YYYYMMDDhhmmss` form. If the operator supplies a
conflicting, too-short, too-long, or malformed timestamp, stop and ask for a
corrected value. Do not silently repair the timestamp by guessing the intended
date.

For Authenticated Browser Snapshot, `session_mode` must be exactly one of:

- `free_account_created_session`
- `paid_entitled_session`
- `client_provided_session`
- `consenting_coworker_session`

The storage-state label resolves only under `forseti-harness/_auth_state/`. Do not
paste, print, stage, commit, or copy storage-state JSON, cookies, credentials, or
session values into a packet or report.

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
| Login-visible or entitled browser session content | `run_source_capture_browser_session_bootstrap.py`, then `run_source_capture_authenticated_browser_packet.py` | The operator authorizes an allowed manual-login storage-state session. |
| Anti-blocking browser-rendered page | `run_source_capture_cloakbrowser_packet.py` | One supplied URL needs anonymous CloakBrowser rendering because ordinary Browser Snapshot controls (`--headed`, `--browser-channel`, `--settle-seconds`) are expected to fail or have failed. |
| Retail/PDP anti-blocking capture plus local projection | `run_source_capture_cloakbrowser_packet.py --source-family retail_pdp --retail-pdp-projection-output <path>` | One supplied retailer PDP URL needs a Source Capture Packet and a separate no-network Retail/PDP projection JSON. For the current Amazon/Sephora/Ulta smoke commands, use `docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md`. |
| Reddit pre-commercial anti-blocking capture | `run_source_capture_cloakbrowser_packet.py` for one supplied old Reddit/thread URL only | The runner can preserve one supplied browser-visible URL through CloakBrowser; it does not discover Reddit targets, monitor threads, parse/consolidate comments, use credentials, or authorize broad crawling. |

If a supplied URL points directly to a source-meaningful asset, prefer Media /
Asset. If it points to a page or file whose whole response body is the capture
target, prefer Direct HTTP. If unclear, stop and ask for the operator's intended
runner rather than guessing from URL shape.

For Reddit thread JSON, do not treat a cold `.json` URL as the default Direct
HTTP or browser-navigation target. Current bounded probes show cold `.json`
requests can return Reddit network-security blocks even when the matching old
Reddit HTML thread is capturable. The useful JSON shape is a specialized warm
same-context flow: load the exact old Reddit HTML thread first in CloakBrowser,
confirm it is not access-blocked, then fetch the same thread's `.json` inside
that same browser context and preserve both bodies. Use that only when a
specialized runner or explicitly bounded diagnostic authorizes it; do not use it
to follow links, discover targets, crawl subreddits, capture users/profiles, or
monitor threads.

For supplied exact old Reddit thread URLs where current old Reddit HTML is the
capture target, use the bounded Direct HTTP batch runner first. CloakBrowser is
the anti-blocking/browser-visible route when Direct HTTP is unsuitable, blocked,
or explicitly requested; do not skip a working Direct HTTP capture merely
because CloakBrowser exists.

For bounded old Reddit Direct HTTP batches, prefer the batch runner's
budget-window cadence over a mechanical fixed delay when running more than a
tiny smoke list:

```powershell
python runners/run_reddit_old_http_batch.py `
  --url-list "<json list of exact old.reddit.com thread URLs>" `
  --output-root "<scratch output directory>" `
  --decision-question "<bounded capture question>" `
  --max-urls 9 `
  --cadence-mode bounded_jitter `
  --cadence-window-seconds 900 `
  --cadence-min-gap-seconds 20 `
  --cadence-max-gap-seconds 180
```

This is a bounded low-load schedule, not a stealth or human-impersonation claim.
The runner records the cadence mode, random seed, planned waits, planned
offsets, and actual per-slot timestamps in `batch_summary.json`. Keep
`--max-urls` as the hard ceiling, choose a window that can fit the minimum gap,
and stop on visible blocks instead of adding retries or proxy/browser fallback
inside the same runner. Use `--delay-seconds` only when a fixed mechanical
cadence is intentionally desired.

When a downstream agent needs to read Reddit outputs, generate two local view
states from the existing JSON artifact instead of feeding the durable artifact
blindly into context:

```powershell
python runners/run_reddit_agent_view.py `
  --input "<reddit_thread_consolidation.json | reddit_candidate_url_intake.json | reddit_graph_frontier_register.json>" `
  --output-dir "<fresh scratch output directory>"
```

The runner writes:

- `reddit_agent_view_full.json`: a full copy of the input JSON for audit and
  fallback.
- `reddit_agent_view_stripped.json`: an agent-context view that removes repeated
  packet provenance, per-row receipts, direct author handles, scores,
  timestamps, generated identifiers, and repeated non-claims while preserving
  source meaning such as thread/post/comment text, graph shape, candidate
  values, postures, counts, stop reasons, and promotion-relevant fields.
- `reddit_agent_view_receipt.md`: a local receipt for the view-generation step.

The stripped view is not a replacement for the durable artifact and is not a
source-capture, validation, readiness, source-completeness, Data Capture, ECR,
Cleaning, or Judgment claim. Do not remove strings inside `body_text` merely
because they look like HTML or CSS; those may be real user content.

Before making stripped views the default read surface for agents, build a local
A/B probe pack from one or more existing view directories:

```powershell
python runners/run_reddit_agent_view_ab_probe.py `
  --view-dir "<directory containing reddit_agent_view_full.json and reddit_agent_view_stripped.json>" `
  --view-dir "<another view directory, optional>" `
  --output-dir "<fresh scratch output directory>"
```

The A/B probe runner verifies that each full/stripped pair describes the same
Reddit artifact type, then writes paired prompts and a comparison worksheet for
agent or owner review. It does not call a model, fetch Reddit, evaluate answers,
choose the default view, promote candidates, or replace the durable artifact.
Treat its `needs_agent_or_owner_outputs` status as the next human/agent
comparison step, not as a pass/fail result.

The current Reddit agent read-surface rule is:

- The agent reads the **cleaned view** we prepare upstream (emitted today as
  `reddit_agent_view_stripped.json`). Cleaning runs AFTER projection, on the
  projected artifact, and is **content-lossless**: it preserves all substantive
  content (thread/post/comment text, visible candidate values, bounds/caps/
  exclusions, stop reasons, selected frontier decisions, parser warnings that
  affect interpretation, non-claims) and removes only worthless noise (repeated
  packet provenance, hashes, paths, generated identifiers, score/timestamp
  cruft, repeated non-claims). The agent gets all the data at a fraction of the
  token/context cost. It is not an agent toggle between two surfaces; it is the
  one view we hand over.
- The verbatim copy (`reddit_agent_view_full.json`) is **provenance/audit only**
  -- open it for packet/source provenance, raw artifact lineage, exact
  reconstruction, or any decision that could be confused with promotion,
  validation, source completeness, fixture admission, commercial readiness, Data
  Capture handoff, ECR, Cleaning, or Judgment.
- Because cleaning is content-lossless, dropping any decision-relevant field is a
  **bug**, not aggressive cleaning (e.g. the caps/exclusions regression caught
  this session). Guard the retained fields with regression tests, not this rule
  alone.

This rule began as a three-case local A/B probe and is now framed as a
content-lossless cleaning step for token/context efficiency. It is a read-surface
operating rule -- not validation, readiness, source-completeness proof, canonical
evidence replacement, or a claim that byte reduction proves quality.

Do not chain runners unless the operator explicitly asks for multiple packets.
For example, do not run Archive.org automatically after Direct HTTP fails unless
that fallback was requested.

When the operator requests archive fallback for a bounded blocked URL, keep the
fallback inside the same source unit. For a single blocked URL:

1. preserve the live/current block packet when the runner wrote one;
2. run Archive.org against the exact supplied URL;
3. for Reddit thread URLs only, if the exact old/new host has no snapshot,
   optionally run Archive.org against the same-thread canonical host variant
   (`old.reddit.com` <-> `www.reddit.com`) without changing subreddit, thread
   id, slug, or query scope;
4. report `snapshot_count`, selected snapshot timestamp, whether a snapshot body
   was preserved, and any `archive_body_not_preserved` or equivalent limitation;
5. stop.

Do not use archive fallback to broaden into subreddit crawl, source discovery,
related URLs, user/profile pages, comment links, recommendations, or "more like
this" surfaces. `snapshot_count=0` is a real fallback result, not permission to
search wider.

## Restricted Network Permission Discipline

In Codex or another restricted sandbox, launch live network-backed runners with
per-operation network permission before the first attempt. This applies to:

- Direct HTTP;
- Media / Asset capture for remote URLs;
- Archive.org availability/body capture;
- Browser Snapshot or Authenticated Browser Snapshot against a remote URL;
- CloakBrowser Snapshot against a remote URL.

The local-file packet runner does not need network permission.

On Windows, `WinError 10061` before any HTTP response is usually sandbox network
refusal, not a source-access result. Do not record that as a source limitation
or spend a doomed first attempt when the runner is known to require network
access. Run the same bounded command with per-operation network permission, or
report an operational blocker if permission is unavailable.

If a packet exists and its preserved response metadata shows an HTTP status such
as `403 Blocked`, treat that as a source-access outcome rather than a sandbox
network refusal. Inspect the preserved body enough to distinguish source content
from an interstitial, but do not infer source meaning from the block page. A
visible Reddit "network security" block is a hard content-capture failure for
that method and should route only to an explicitly requested bounded fallback.

Do not request broad standing Python or network permission for source capture.
The approval request should name the exact runner class and the single bounded
source packet attempt. If a denied or timed-out attempt leaves no packet
directory, the same fresh output path may be reused; otherwise choose a new
output path or ask the operator before clearing anything.

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

For packet lifecycle, retention, durable citation, and sensitivity handling,
open
`docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`.
That decision keeps generated packets scratch by default and distinguishes
durable closeout summaries from fixture admission.

Recommended naming:

```text
_test_runs/source_capture_<runner>_<short_slug>
reports/source_capture/<case_or_slot>_<runner>_<short_slug>
```

Generated packet directories are not canonical fixtures unless a separate
fixture-admission decision says so.

## Commands

Run from `forseti-harness/`.

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
was supplied. If a cutoff timestamp is supplied, check that it is exactly 14
digits in `YYYYMMDDhhmmss` form before executing; malformed timestamps are
operator-input defects, not archive-access failures.

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

The Browser Snapshot runner defaults to an anonymous/headless browser path.
It preserves rendered DOM, visible text, a viewport screenshot, and browser
metadata. For one supplied URL, `--headed` runs visibly, `--browser-channel`
selects a local Playwright Chromium channel such as Chrome or Edge, and
`--settle-seconds` waits after navigation before artifact capture. It does not
use stored sessions, browser profiles, cookies, credentials, storage-state
files, anti-detect behavior, proxy behavior, CAPTCHA solving, crawling, OCR, or
source-meaningfulness classification. Its rendered-access posture is a guard
against fake success, not content sufficiency proof: visible text/title decide
whether the browser is still showing a block shell; residual challenge markers
in the full DOM alone are preserved as limitations.

On Windows, a failure containing `WinError 5` or `Access is denied` during
Playwright startup usually means the environment blocked Playwright's browser
driver subprocess launch. Treat this as visible capture failure: exit `3`, no
normal packet, and rerun only in an environment with subprocess-launch
permission. Do not switch methods or claim the adapter is broken from this error
alone.

Authenticated Browser Snapshot:

First bootstrap storage state through a visible manual login. This writes no
packet and stores only local ignored Playwright storage-state JSON under
`forseti-harness/_auth_state/`, plus a small local ignored metadata sidecar binding
the saved state file to the declared session mode:

```powershell
python runners/run_source_capture_browser_session_bootstrap.py `
  --login-url "<ordinary login or target URL>" `
  --state-label "<local state label>" `
  --session-mode "<allowed session mode>"
```

The runner opens a headed Chromium window. Complete only the permitted login in
that window, then press Enter in the terminal to save storage state. Do not pass
passwords, usernames, cookies, tokens, or profile paths to the runner. If the
label already exists, choose a new label or ask the operator before deleting
anything. Choose a non-sensitive state label; the label is later recorded in
packet metadata.

Then capture one explicit URL with that saved state:

```powershell
python runners/run_source_capture_authenticated_browser_packet.py `
  --url "<ordinary http or https URL>" `
  --state-label "<local state label>" `
  --session-mode "<allowed session mode>" `
  --decision-question "<operator-supplied decision question>" `
  --cutoff-posture "<operator-supplied cutoff posture>" `
  --output "<packet directory>"
```

The Authenticated Browser Snapshot runner preserves rendered DOM, visible text,
a viewport screenshot, and browser metadata. It records the session mode and
state label, and it refuses to run if the capture-time session mode does not
match the bootstrap sidecar. It does not copy, hash, print, or preserve the
storage-state file, metadata sidecar, or cookie/session values. It does not
prove login-wall absence or content sufficiency. If a login wall or auth
challenge remains visibly present, preserve that as a limitation and do not call
the packet a clean unlocked capture.

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
  `manifest.json` when present, even when `limitations` is empty;
- warnings and limitations from `manifest.json`;
- any visible access, archive, media, or cutoff limitations;
- receipt non-claims from `receipt.md` or manifest receipt metadata when
  present.

When the operator commissioned a source-quality pass, the agent report must also
include a `mini_god_tier_source_quality_report` block. Use result tokens from
`docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`
and queue row-status vocabulary from
`docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md`.
Do not redefine those vocabularies in the runbook report.

For this runbook, an operator-commissioned source-quality pass means the
operator explicitly asked for source-quality improvement or mini god-tier
classification for a bounded source unit. Ordinary packet smoke tests, adapter
checks, local packaging tests, and generic capture runs do not trigger this
block unless the operator says they are source-quality passes.

The mini god-tier block reports the observed packet state and visible limits. It
does not validate the source, admit a fixture, prove source completeness, score
source quality, or decide Judgment meaning.

For source-quality passes, agents may use the report-skeleton helper after a
packet has already been written:

```powershell
python runners/run_source_quality_report_skeleton.py `
  --packet "<packet directory or manifest.json>" `
  --source-id "<operator-supplied source id>" `
  --output "<skeleton yaml>"
```

The helper is local and deterministic. It reads existing packet manifest and
packet-side metadata only, then emits a Mini God-Tier report skeleton for
operator completion. It does not fetch sources, parse source bodies for meaning,
infer source-language anchors, discover sources, admit fixtures, score source
quality, or finalize `mini_god_tier_met`. Treat `suggested_result_token` as
conservative guidance, not the final `result_token`.

For multi-row source-quality passes, agents may use the Source Quality State
Assembler after queue rows and packet paths already exist:

```powershell
python runners/run_source_quality_state_assembler.py `
  --queue "<queue yaml with explicit rows>" `
  --output "<state census yaml>"
```

The assembler is a read-only state census helper. It reads explicit rows,
existing packet paths, and existing packet manifests, then surfaces skeleton
state, visible stops, lifecycle posture, and operator-finalization requirements
per row. It does not run Source Capture tools, discover sources, fetch data,
rank rows, score source quality, auto-advance row status, or finalize
`mini_god_tier_met`. Missing packet paths and invalid manifests must remain
visible row stops, not hidden batch failures or clean passes.

For Archive.org packets, report that `snapshot_count` reflects
`collapse=digest` unique-content snapshot rows returned by the availability
endpoint, not every historical capture timestamp that Archive.org may hold.

For Browser Snapshot packets, report that the screenshot is viewport-only and
that browser artifacts do not prove content sufficiency, login-wall absence, or
source completeness.

For Authenticated Browser Snapshot packets, report the session mode and state
label, but do not report storage-state file contents, cookie values, tokens, or
credentials. Also report that storage-state use does not prove entitlement
sufficiency, login-wall absence, or source completeness.

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
| Browser Snapshot | `0`, `2`, `3` | Missing Playwright package, missing Chromium/local channel binary, navigation failure, or artifact failure is exit `3`; no packet. Exit `0` preserves browser artifacts only, not content sufficiency; rendered access-block pages are packets with visible limitations, not successful source-content capture. |
| Browser Session Bootstrap | `0`, `2`, `3` | Exit `0` writes ignored local storage-state JSON only; no packet. Missing/invalid labels are exit `2`; Playwright/browser/manual interaction failures are exit `3`. |
| Authenticated Browser Snapshot | `0`, `2`, `3` | Missing/invalid auth state is exit `2`; missing Playwright package, missing Chromium binary, navigation failure, or artifact failure is exit `3`; no normal packet. Exit `0` preserves browser artifacts only, not content sufficiency or login-wall absence. |

If a network runner reports a staging-collision or "clear it before rerunning"
message, clear or choose a new output parent only after operator approval. Do
not delete unrelated files.

If a runner writes a packet with limitations, preserve those limitations in the
agent report. Do not patch them away by rerunning a different method unless the
operator authorizes the next method.

## Minimal Agent Report Template

```text
source_capture_agent_report:
  runner: <local_file|direct_http|media_asset|archive_org|browser_snapshot|cloakbrowser_snapshot|authenticated_browser_snapshot>
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
  authenticated_browser_caveat: <if authenticated browser packet, session mode/state label reported but no state contents or login-wall absence proof; otherwise none>
  visible_stop_if_any: <missing input, access failure, browser-needed, no packet, or none>
  non_claims:
    - <receipt non-claim or none>
  mini_god_tier_source_quality_report:
    required_when: <operator commissioned a source-quality pass; otherwise omit>
    source_id: <operator-supplied source id or unknown_with_reason>
    result_token: <token from source_quality_mini_god_tier_profile_v0.md>
    packet_path: <path or none>
    best_in_bound_body:
      posture: <preserved|not_preserved|metadata_only|current_only|not_applicable>
      preserved_body_path: <packet-relative path or none>
      sha256: <hash or none>
      byte_count: <bytes or none>
      source_or_snapshot_time: <timestamp or unknown_with_reason>
    provenance:
      original_locator: <locator or unknown_with_reason>
      final_or_snapshot_locator: <locator or unknown_with_reason>
      access_status: <status or unknown_with_reason>
      content_type: <content type or unknown_with_reason>
      capture_time: <timestamp or unknown_with_reason>
    source_language_anchors:
      - <bounded source-visible anchor or not_applicable_with_reason>
    coverage_or_drift_note: <improves|replaces|supplements|conflicts|standardizes|unknown_with_reason>
    visible_limitations:
      - <limitation or none>
    lifecycle_state: <scratch|candidate_evidence|recommended_fixture_admission|separately_admitted>
    lifecycle_decision_reference: <required if separately_admitted; otherwise none>
    non_claims:
      - not validation
      - not source completeness proof
      - not fixture admission unless separately decided
      - not Judgment scoring
```

Do not use `separately_admitted` unless `lifecycle_decision_reference` cites the
separate fixture-admission or equivalent lifecycle decision. After completing
the mini god-tier report block for a queued source-quality row, update the queue
row from `packet_written_needs_report` to `reported` when the queue is part of
the commissioned work.

Do not collapse an exit-code-0 packet with empty limitations into "clean
capture." Packet postures may still carry current-capture, cutoff, archive,
media, browser, or access caveats that matter downstream.

## Testing Before Agent Reuse

Before treating a changed runner as reusable by agents, run the relevant focused
tests and the source-capture stack:

```powershell
python -m pytest -p no:cacheprovider tests/unit/test_source_capture_packet.py tests/contract/test_source_capture_packet_no_runtime_imports.py tests/unit/test_source_capture_direct_http.py tests/contract/test_source_capture_direct_http_contract.py tests/unit/test_source_capture_media_asset.py tests/contract/test_source_capture_media_asset_contract.py tests/unit/test_source_capture_archive_org.py tests/contract/test_source_capture_archive_org_contract.py tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_source_capture_authenticated_browser_snapshot.py tests/contract/test_source_capture_browser_snapshot_contract.py
```

For a new adapter, add focused unit tests, contract tests, one manual dry-run,
and adversarial implementation review before committing it as an agent-facing
primitive.

For the source-quality report-skeleton helper, run:

```powershell
python -m pytest -p no:cacheprovider tests/unit/test_source_quality_report_skeleton.py tests/contract/test_source_quality_report_skeleton_contract.py
```

For the Source Quality State Assembler helper, run:

```powershell
python -m pytest -p no:cacheprovider tests/unit/test_source_quality_state_assembler.py tests/contract/test_source_quality_report_skeleton_contract.py
```

## Direction Change Propagation - Reddit Agent View Default Read Surface

```yaml
direction_change_propagation:
  doctrine_changed: >
    After a three-case local A/B probe, Reddit stripped agent views are now the
    default agent-read surface for semantic thread, Candidate URL Intake, and
    Graph Frontier reasoning, with full JSON required for audit, provenance,
    reconstruction, promotion, validation, source-completeness, fixture,
    commercial, Data Capture, ECR, Cleaning, or Judgment-adjacent decisions.
  trigger: output_authority
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Root behavior does not enumerate runner-specific read surfaces."
    - path: ".agents/workflow-overlay/README.md"
      reason: "Overlay routing owners are unchanged."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Source hierarchy is unchanged; the runbook owns the operator rule."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-pack budgets are unchanged; this is a Reddit runner read-surface rule."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already routes implementation status to this runbook."
    - path: "docs/workflows/data_capture_spine_consolidation_map_v0.md"
      reason: "Data Capture submap already routes safe capture-tool use to this runbook."
  stale_language_search: >
    rg -n "Before making stripped views the default|stripped_default_for_agent_context|make_stripped_default|reddit_agent_view_stripped|default agent-read surface|full JSON required"
    AGENTS.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
    docs/workflows/data_capture_spine_consolidation_map_v0.md
    forseti-harness/docs/source_capture_agent_runbook.md
  stale_language_search_result: >
    Executed on 2026-06-08 after this patch. Hits were confined to the intended
    Reddit agent-view runbook section and this DCP receipt. No checked downstream
    surface retained stale language saying stripped views are still undecided as
    the default agent-read surface.
  non_claims:
    - not validation
    - not readiness
    - not source completeness proof
    - not canonical evidence replacement
    - not Data Capture handoff
```

## Direction Change Propagation - Agent Read Surface Reframed To Content-Lossless Cleaning

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Reddit agent read-surface rule is reframed: the agent reads a single
    CLEANED view we prepare upstream (after projection, on the projected
    artifact), not a stripped-versus-full toggle. Cleaning is content-lossless --
    it preserves all substantive content and decision-relevant fields and removes
    only worthless noise (repeated provenance, hashes, paths, generated ids,
    score/timestamp cruft, repeated non-claims), giving the agent all the data at
    a fraction of the token/context cost. The verbatim copy is provenance/audit
    only. Dropping any decision-relevant field is a bug, not cleaning, and is
    guarded by regression tests rather than this rule alone.
  trigger: output_authority
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
    - "docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  intentionally_not_updated:
    - path: "forseti-harness/source_capture/reddit_agent_view.py"
      reason: >
        Code still emits the cleaned view as reddit_agent_view_stripped.json via
        the _strip_* functions. This reframe changes the read-surface doctrine and
        docs, not the artifact filenames; a stripped->cleaned code rename is an
        optional later refactor with reference lock-in, not part of this patch.
    - path: "AGENTS.md"
      reason: "Root behavior does not enumerate runner-specific read surfaces."
  non_claims:
    - not validation
    - not readiness
    - not a code rename
    - not source completeness proof
    - not canonical evidence replacement
```

## Direction Change Propagation - Archive Timestamp And Posture Reporting

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Agent Runbook now requires agents to preflight Archive.org cutoff timestamps as exact 14-digit YYYYMMDDhhmmss values and to report manifest postures even when limitations are empty."
  trigger: lifecycle_boundary
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "forseti-harness/README.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "Armory component status, adapter boundaries, and deferred gaps did not change."
    - path: "forseti-harness/README.md"
      reason: "It already points agents to this runbook; no new entrypoint or component status changed."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading routes were not changed; this is runner-use guidance inside the existing runbook."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory/runbook path through the harness and product docs; no new durable source family was added."
  stale_language_search: "rg -n \"cutoff-timestamp|YYYYMMDDhhmmss|empty limitations|clean capture|postures\" forseti-harness/docs/source_capture_agent_runbook.md docs/product/source_capture_toolbox/README.md forseti-harness/README.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source completeness"
    - "not source-access boundary amendment"
    - "not adapter implementation"
```

## Direction Change Propagation - Restricted Network Runner Permission

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Agent Runbook now tells agents to request per-operation network permission before running live network-backed source-capture runners in restricted sandboxes, and to treat pre-response WinError 10061 as an operational sandbox refusal rather than a source limitation."
  trigger: lifecycle_boundary
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "forseti-harness/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The armory component set, adapter boundaries, hard stops, and deferred gaps did not change; it already points to the runbook for agent-facing runner use."
    - path: "forseti-harness/README.md"
      reason: "The harness README already points to the runbook for agent-facing runner selection and report format; detailed sandbox permission sequencing belongs in the runbook."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading routes were not changed; this is runner-use guidance inside the existing runbook."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory implementation and runbook surfaces; no new durable source family or component path was added."
  stale_language_search: "rg -n \"WinError 10061|network permission|restricted sandbox|standing Python|source limitation\" forseti-harness/docs/source_capture_agent_runbook.md docs/product/source_capture_toolbox/README.md forseti-harness/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not broad standing permission"
    - "not adapter implementation"
    - "not source-quality proof"
```

## Direction Change Propagation - Mini God-Tier Report Block

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Agent Runbook now requires agents to include a mini_god_tier_source_quality_report block when an operator commissions a source-quality pass, while leaving result-token vocabulary in the Mini God-Tier profile and row-status vocabulary in the source-unit queue template."
  trigger: output_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "forseti-harness/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "The profile already owns mini god-tier criteria, result tokens, and report-block fields; this runbook patch references that vocabulary without changing it."
    - path: "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "The queue template already owns row-status vocabulary; this runbook patch references that vocabulary without changing it."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The README already indexes the profile, queue template, and runbook; no new component or entrypoint was added."
    - path: "forseti-harness/README.md"
      reason: "The harness README already points agents to this runbook for report format; detailed source-quality report fields belong in the runbook."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading routes were not changed; this is report-format guidance inside the existing runbook."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory/runbook path through the harness and product docs; no new durable source family was added."
  stale_language_search: "rg -n \"mini_god_tier_source_quality_report|source_quality_mini_god_tier_profile_v0|source_quality_source_unit_queue_template_v0|operator-commissioned source-quality pass|source-quality scoring|validated|ready|fixture admission|Judgment scoring|Commissioning Gate|Decision Frame|recommended_fixture_admission|separately_admitted\" forseti-harness/docs/source_capture_agent_runbook.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md docs/product/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source completeness proof"
    - "not fixture admission"
    - "not source-quality scoring"
    - "not ECR, Cleaning, or Judgment authority"
```

## Direction Change Propagation - Source Quality Report-Skeleton Helper

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Agent Runbook now exposes a local Source Quality report-skeleton helper for existing Source Capture Packets; the helper emits conservative operator-completion skeletons and does not finalize result tokens, fetch sources, parse source meaning, admit fixtures, or score source quality."
  trigger: output_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
    - "forseti-harness/README.md"
    - "docs/product/source_capture_toolbox/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "forseti-harness/README.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "Profile tokens, lifecycle vocabulary, required criteria, and report-block fields did not change."
    - path: "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "Queue fields and row-status vocabulary did not change; the helper does not mutate queues."
    - path: "docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md"
      reason: "The closeout already supplies the helper requirements and remains trial evidence rather than helper API documentation."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes Data Capture source-access tooling through the armory README and runbook; no new read-pack entry is needed."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory and runbook entrypoints; detailed helper command routing belongs in the README/runbook."
  stale_language_search: "rg -n \"run_source_quality_report_skeleton|report-skeleton|mini_god_tier_met|source-quality scoring|validated|ready|fixture admission|Judgment scoring|source discovery|source selection\" forseti-harness/docs/source_capture_agent_runbook.md forseti-harness/README.md docs/product/source_capture_toolbox/README.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source completeness proof"
    - "not fixture admission"
    - "not source-quality scoring"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment authority"
```

## Direction Change Propagation - Source Quality State Assembler Helper

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Agent Runbook now exposes a local read-only Source Quality State Assembler helper for explicit source-quality rows and existing packet manifests; the helper emits a state census and does not run capture tools, discover sources, score source quality, auto-advance queue rows, or finalize mini_god_tier_met."
  trigger: output_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - "forseti-harness/docs/source_capture_agent_runbook.md"
    - "forseti-harness/README.md"
    - "docs/product/source_capture_toolbox/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "forseti-harness/README.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md"
      reason: "The architecture boundary already authorizes only a read-only state census over explicit rows and existing packets; implementation follows that boundary without changing it."
    - path: "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "Result tokens, criteria, lifecycle states, and finalization ownership did not change."
    - path: "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "Queue row fields and row-status vocabulary did not change; the assembler echoes rows and does not mutate queues."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes multi-row state-census questions to the State Assembler architecture boundary."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the State Assembler architecture and armory entrypoint; detailed helper invocation belongs in the runbook and harness README."
  stale_language_search: "rg -n \"run_source_quality_state_assembler|Source Quality State Assembler|mini_god_tier_met|source-quality scoring|validated|ready|fixture admission|Judgment scoring|source discovery|source selection|runner dispatch|all rows passed|ladder complete\" forseti-harness/docs/source_capture_agent_runbook.md forseti-harness/README.md docs/product/source_capture_toolbox/README.md docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source completeness proof"
    - "not fixture admission"
    - "not source discovery"
    - "not runner dispatch"
    - "not source acquisition"
    - "not source-quality scoring"
    - "not ECR, Cleaning, or Judgment authority"
```
