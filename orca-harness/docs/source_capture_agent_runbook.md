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
- use unbuilt or separately gated methods from this runbook, including
  password-driven login automation, direct browser profile/cookie import, APIs,
  SDKs, scraper frameworks, proxy behavior, anti-detect behavior, CAPTCHA
  solving, or commercial fetch services;
- use no-entitlement login bypass, credential misuse, undisclosed session/cookie
  use, or any method Orca would refuse to disclose internally;
- claim validation, readiness, ECR receipt, Cleaning output, Judgment output,
  buyer proof, or commercial readiness.

If the requested capture needs anonymous browser-rendered content, JavaScript
rendering, or screenshot preservation for one supplied URL, use the Honest
Browser Snapshot runner. If it requires login-visible or entitled content, use
Authenticated Browser Snapshot only when the operator has supplied an allowed
session mode and a previously bootstrapped local storage-state label. If the
operator asks for password automation, direct profile/cookie import, credentials
in flags or environment variables, no-entitlement bypass, anti-detect behavior,
proxy behavior, or CAPTCHA solving, stop with `visible_capture_limitation`.

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

Direct HTTP, Media / Asset, Archive.org, Browser Snapshot, and Authenticated
Browser Snapshot runners have default source-family labels and URL-derived
locators; do not ask for local-file-only fields when those runners are used.

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

The storage-state label resolves only under `orca-harness/_auth_state/`. Do not
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

If a supplied URL points directly to a source-meaningful asset, prefer Media /
Asset. If it points to a page or file whose whole response body is the capture
target, prefer Direct HTTP. If unclear, stop and ask for the operator's intended
runner rather than guessing from URL shape.

Do not chain runners unless the operator explicitly asks for multiple packets.
For example, do not run Archive.org automatically after Direct HTTP fails unless
that fallback was requested.

## Restricted Network Permission Discipline

In Codex or another restricted sandbox, launch live network-backed runners with
per-operation network permission before the first attempt. This applies to:

- Direct HTTP;
- Media / Asset capture for remote URLs;
- Archive.org availability/body capture;
- Browser Snapshot or Authenticated Browser Snapshot against a remote URL.

The local-file packet runner does not need network permission.

On Windows, `WinError 10061` before any HTTP response is usually sandbox network
refusal, not a source-access result. Do not record that as a source limitation
or spend a doomed first attempt when the runner is known to require network
access. Run the same bounded command with per-operation network permission, or
report an operational blocker if permission is unavailable.

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

The Browser Snapshot runner uses an anonymous/headless browser path. It
preserves rendered DOM, visible text, a viewport screenshot, and browser
metadata. It does not use stored sessions, browser profiles, cookies,
credentials, storage-state files, anti-detect behavior, proxy behavior, CAPTCHA
solving, crawling, OCR, or source-meaningfulness classification.

On Windows, a failure containing `WinError 5` or `Access is denied` during
Playwright startup usually means the environment blocked Playwright's browser
driver subprocess launch. Treat this as visible capture failure: exit `3`, no
normal packet, and rerun only in an environment with subprocess-launch
permission. Do not switch methods or claim the adapter is broken from this error
alone.

Authenticated Browser Snapshot:

First bootstrap storage state through a visible manual login. This writes no
packet and stores only local ignored Playwright storage-state JSON under
`orca-harness/_auth_state/`, plus a small local ignored metadata sidecar binding
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
| Browser Snapshot | `0`, `2`, `3` | Missing Playwright package, missing Chromium binary, navigation failure, or artifact failure is exit `3`; no packet. Exit `0` preserves browser artifacts only, not content sufficiency. |
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
  runner: <local_file|direct_http|media_asset|archive_org|browser_snapshot|authenticated_browser_snapshot>
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

## Direction Change Propagation - Archive Timestamp And Posture Reporting

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Agent Runbook now requires agents to preflight Archive.org cutoff timestamps as exact 14-digit YYYYMMDDhhmmss values and to report manifest postures even when limitations are empty."
  trigger: lifecycle_boundary
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "orca-harness/README.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "Toolbox component status, adapter boundaries, and deferred gaps did not change."
    - path: "orca-harness/README.md"
      reason: "It already points agents to this runbook; no new entrypoint or component status changed."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading routes were not changed; this is runner-use guidance inside the existing runbook."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the toolbox/runbook path through the harness and product docs; no new durable source family was added."
  stale_language_search: "rg -n \"cutoff-timestamp|YYYYMMDDhhmmss|empty limitations|clean capture|postures\" orca-harness/docs/source_capture_agent_runbook.md docs/product/source_capture_toolbox/README.md orca-harness/README.md"
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
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "orca-harness/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The toolbox component set, adapter boundaries, hard stops, and deferred gaps did not change; it already points to the runbook for agent-facing runner use."
    - path: "orca-harness/README.md"
      reason: "The harness README already points to the runbook for agent-facing runner selection and report format; detailed sandbox permission sequencing belongs in the runbook."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading routes were not changed; this is runner-use guidance inside the existing runbook."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the toolbox implementation and runbook surfaces; no new durable source family or component path was added."
  stale_language_search: "rg -n \"WinError 10061|network permission|restricted sandbox|standing Python|source limitation\" orca-harness/docs/source_capture_agent_runbook.md docs/product/source_capture_toolbox/README.md orca-harness/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
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
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "orca-harness/README.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "The profile already owns mini god-tier criteria, result tokens, and report-block fields; this runbook patch references that vocabulary without changing it."
    - path: "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "The queue template already owns row-status vocabulary; this runbook patch references that vocabulary without changing it."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The README already indexes the profile, queue template, and runbook; no new component or entrypoint was added."
    - path: "orca-harness/README.md"
      reason: "The harness README already points agents to this runbook for report format; detailed source-quality report fields belong in the runbook."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading routes were not changed; this is report-format guidance inside the existing runbook."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the toolbox/runbook path through the harness and product docs; no new durable source family was added."
  stale_language_search: "rg -n \"mini_god_tier_source_quality_report|source_quality_mini_god_tier_profile_v0|source_quality_source_unit_queue_template_v0|operator-commissioned source-quality pass|source-quality scoring|validated|ready|fixture admission|Judgment scoring|Commissioning Gate|Decision Frame|recommended_fixture_admission|separately_admitted\" orca-harness/docs/source_capture_agent_runbook.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md docs/product/source_capture_toolbox/README.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
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
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/README.md"
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
    - "orca-harness/README.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
      reason: "Profile tokens, lifecycle vocabulary, required criteria, and report-block fields did not change."
    - path: "docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
      reason: "Queue fields and row-status vocabulary did not change; the helper does not mutate queues."
    - path: "docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md"
      reason: "The closeout already supplies the helper requirements and remains trial evidence rather than helper API documentation."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes Data Capture source-access tooling through the toolbox README and runbook; no new read-pack entry is needed."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the toolbox and runbook entrypoints; detailed helper command routing belongs in the README/runbook."
  stale_language_search: "rg -n \"run_source_quality_report_skeleton|report-skeleton|mini_god_tier_met|source-quality scoring|validated|ready|fixture admission|Judgment scoring|source discovery|source selection\" orca-harness/docs/source_capture_agent_runbook.md orca-harness/README.md docs/product/source_capture_toolbox/README.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
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
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/README.md"
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
    - "orca-harness/README.md"
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
      reason: "Repo map already indexes the State Assembler architecture and toolbox entrypoint; detailed helper invocation belongs in the runbook and harness README."
  stale_language_search: "rg -n \"run_source_quality_state_assembler|Source Quality State Assembler|mini_god_tier_met|source-quality scoring|validated|ready|fixture admission|Judgment scoring|source discovery|source selection|runner dispatch|all rows passed|ladder complete\" orca-harness/docs/source_capture_agent_runbook.md orca-harness/README.md docs/product/source_capture_toolbox/README.md docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
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
