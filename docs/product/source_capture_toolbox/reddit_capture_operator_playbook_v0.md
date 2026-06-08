# Reddit Capture Operator Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Current operator procedure for bounded Reddit capture and consolidation using implemented Source Capture Armory tools.
use_when:
  - Running or planning exact-thread Reddit capture with current Orca runners.
  - Choosing between old Reddit Direct HTTP, CloakBrowser, archive fallback, and Reddit consolidation.
  - Checking Reddit capture stops, non-claims, and operator report expectations.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - docs/product/source_capture_toolbox/README.md
stale_if:
  - Old Reddit HTML becomes unavailable or materially unsuitable.
  - A warm same-context Reddit JSON runner is implemented.
  - Reddit capture ordering or CloakBrowser/proxy posture is amended.
  - Candidate URL intake receives a production-grade handoff contract.
  - A Reddit lane stage (discover/select/capture/read) or its runner changes.
```

## Status

Status: `REDDIT_CAPTURE_OPERATOR_PLAYBOOK_V0`.

This playbook is current-procedure guidance for bounded personal-project Reddit
capture. It consolidates existing Armory and runbook rules. It does not create a
new source-access method, authorize broad crawling, authorize commercial Reddit
use, or prove capture quality.

## Reddit Lane At A Glance

This playbook owns the **capture** stage. A new agent operating Reddit end to end
moves through four stages, in order, staying inside each stage's owner contract:

| Stage | What it does | Runner | Owner contract |
| --- | --- | --- | --- |
| 1. Discover | Find candidate subreddits/threads (rows + provenance only; no bodies) | `orca-harness/runners/run_reddit_candidate_intake_live.py` | `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md` |
| 2. Select | Build a Graph Frontier Register over candidates and queue a non-executing next-run envelope | `orca-harness/runners/run_reddit_graph_frontier_register.py` | `docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` |
| 3. Capture | Capture exact thread URLs into packets + consolidation (this playbook) | `run_reddit_old_http_batch.py` / `run_reddit_consolidation.py` / `run_reddit_batch_quality_summary.py` | this playbook |
| 4. Read | Read capture/intake/frontier outputs as an agent (stripped view is the default surface; full JSON for provenance) | `orca-harness/runners/run_reddit_agent_view.py` | `orca-harness/docs/source_capture_agent_runbook.md` (stripped-default rule) |

Stages 1–2 are planning/provenance only: they never capture bodies and never
authorize the next run automatically — each hop needs a fresh bounded run
envelope, and promotion of a discovered URL into a capture unit is a separate gate
before stage 3. The navigation hub for every owner doc in this lane is
`docs/workflows/data_capture_spine_consolidation_map_v0.md`.

## Current Operator Default

For exact old Reddit thread URLs, use old Reddit Direct HTTP first.

That is the current cheapest complete path because the implemented batch runner
accepts only exact `old.reddit.com` thread URLs, preserves each response into a
Source Capture Packet, runs Reddit consolidation, records cadence, and emits a
batch summary. CloakBrowser remains available for one supplied anti-blocking
browser-visible URL, but current Reddit use should not route there first while
old Reddit Direct HTTP works for exact thread capture.

Do not use cold `.json` as the default target. Current bounded probes showed
cold Reddit `.json` can block even when the matching old Reddit HTML works. The
useful JSON path is future/specialized: load the exact old Reddit HTML first in
one browser context, then fetch that same thread's `.json` inside the same
context and preserve both bodies with provenance.

## Required Inputs

Before running a Reddit capture unit, bind:

- `unit_type`: normally `candidate_or_scouting` unless an approved Decision
  Frame or capture unit is supplied.
- `purpose`: why these exact thread URLs are being captured.
- `decision_question`: the operator-supplied question for packet metadata.
- `urls`: exact `https://old.reddit.com/.../comments/...` thread URLs.
- `exclusions`: no link following, no user/profile capture, no subreddit crawl,
  no recommendations, no comment-link expansion.
- `volume_ceiling`: hard maximum URL count.
- `monitoring`: none unless a separate monitoring lane with stop date exists.
- `commercial_use`: no.

If those fields are missing, stop and ask for the smallest missing input. Do not
infer a broad topic crawl from a few example URLs.

## URL List Shape

Use a JSON array. Prefer explicit `slot_id` values so outputs stay readable:

```json
[
  {
    "slot_id": "b2b_001",
    "url": "https://old.reddit.com/r/SaaS/comments/1es61lz/why_is_b2b_so_much_better/"
  },
  {
    "slot_id": "seo_001",
    "url": "https://old.reddit.com/r/SEO/comments/1txm4fv/brand_name_change_impact_on_seo/"
  }
]
```

Slot ids may contain only letters, numbers, underscores, and hyphens. The batch
runner rejects non-`old.reddit.com` hosts and URLs without `/comments/`.

## Primary Path: Old Reddit Direct HTTP Batch

Default working directory for this playbook is the repo root:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca
```

Run a bounded batch with budget-window cadence:

```powershell
python orca-harness\runners\run_reddit_old_http_batch.py `
  --url-list "orca-harness\_test_runs\reddit_urls.json" `
  --output-root "orca-harness\_test_runs\reddit_batch_001" `
  --decision-question "Can bounded old Reddit Direct HTTP capture feed Reddit consolidation?" `
  --max-urls 9 `
  --timeout-seconds 20 `
  --max-bytes 5000000 `
  --cadence-mode bounded_jitter `
  --cadence-window-seconds 900 `
  --cadence-min-gap-seconds 20 `
  --cadence-max-gap-seconds 180
```

Use a smaller window for tiny smoke tests only when the minimum gap still fits
the URL count. The cadence is a bounded low-load schedule, not a stealth claim or
human-impersonation claim.

The batch runner creates:

- one packet directory per slot: `<slot_id>_packet`;
- one derived consolidation directory per slot: `<slot_id>_derived`;
- `batch_summary.json` at the output root.

The runner does not use proxy, browser automation, retries, source discovery,
link following, broad Reddit crawl, monitoring, commercial API behavior, ECR,
Cleaning, or Judgment behavior.

## Quality Summary

After the batch completes, summarize downstream usability:

```powershell
python orca-harness\runners\run_reddit_batch_quality_summary.py `
  --batch-summary "orca-harness\_test_runs\reddit_batch_001\batch_summary.json" `
  --output-dir "orca-harness\_test_runs\reddit_batch_001_quality"
```

Read both outputs:

- `reddit_batch_quality_summary.json`;
- `reddit_batch_quality_summary_receipt.md`.

Interpret `usable_for_downstream` conservatively:

- `yes`: capture and consolidation succeeded without current quality flags.
- `needs_review`: source was captured, but thread/parser/posture warnings need
  operator inspection before use.
- `no`: capture, consolidation, HTTP status, metadata, or comment reconciliation
  failed materially.

`needs_review` is not failure and not success. Inspect the slot's consolidation
JSON and receipt before using it. Typical causes include parser warnings, missing
title, no present comments, thread warnings, or source-visible limitations such
as collapsed, removed, deleted, or media-only comment states.

## Single Packet Or Reconsolidation

For one existing packet:

```powershell
python orca-harness\runners\run_reddit_consolidation.py `
  --packet "orca-harness\_test_runs\reddit_batch_001\seo_001_packet" `
  --output-dir "orca-harness\_test_runs\reddit_batch_001\seo_001_derived_rerun"
```

Use this when parser code changes and existing packets need local-only
reconsolidation. This does not fetch Reddit again.

## Archive Fallback

Use archive fallback only when the operator asks for it or the current source
state is blocked/unavailable enough that historical posture is part of the same
bounded source unit.

For one exact URL:

```powershell
python orca-harness\runners\run_source_capture_archive_packet.py `
  --url "https://old.reddit.com/r/SaaS/comments/1es61lz/why_is_b2b_so_much_better/" `
  --decision-question "Can archive capture preserve this old Reddit thread for consolidation?" `
  --output "orca-harness\_test_runs\reddit_archive_001" `
  --source-family reddit_thread `
  --source-surface archive_org_old_reddit_thread `
  --timeout-seconds 20 `
  --max-bytes 5000000
```

If the exact old/new host has no snapshot, the only allowed expansion is the
same-thread canonical host variant: `old.reddit.com` to `www.reddit.com`, or the
reverse, without changing subreddit, thread id, slug, or query scope.

Do not use archive fallback to discover related URLs, crawl a subreddit, inspect
user/profile pages, follow recommendations, or chase comment links.
`snapshot_count=0` is a real result.

## CloakBrowser And Proxy Use

Use CloakBrowser only for one supplied URL when browser-visible anti-blocking
capture is explicitly needed or Direct HTTP is unsuitable. Do not ask agents to
free-browse Reddit through CloakBrowser.

The current CloakBrowser runner preserves a packet for one supplied URL and
records method provenance. It must not carry stored sessions, browser profiles,
cookies, credentials, raw proxy secrets, CAPTCHA solving, crawling, user/profile
capture, ECR, Cleaning, Judgment, or commercial readiness.

Proxy configuration is not the default Reddit path. A proxy may be tested only
through an explicit local profile and explicit operator authorization. Record
the proxy category in provenance when used, but never preserve proxy endpoints,
passwords, exit IPs, cookies, tokens, or credentials in packets, logs, reports,
or prompts.

If CloakBrowser reaches a Reddit network-security or access-block page, treat it
as a hard content-capture failure for that method. Do not relabel the block page
as source content.

## Warm Same-Context JSON

Warm same-context JSON is not the current default and is not a generic fallback.
Use it only after a specialized runner or diagnostic explicitly authorizes the
flow:

1. load the exact old Reddit HTML thread first;
2. confirm the page is not access-blocked;
3. fetch the same thread's `.json` inside the same browser context;
4. preserve both HTML and JSON bodies with method provenance;
5. stop.

Do not use JSON enrichment to follow links, expand comments beyond the supplied
thread, discover subreddits, capture users/profiles, monitor threads, or claim
commercial API compliance.

## Deleted, Removed, Collapsed, And Media-Only Comments

Treat these as source-visible postures, not automatic parser failures:

- `removed`: currently visible source state says removed or equivalent.
- `deleted`: currently visible source state says deleted or equivalent.
- `collapsed`: the current old Reddit DOM presents a collapsed placeholder.
- `media_only`: a comment body node exists but has no extractable text, often
  because the visible body is non-text media.

Do not infer why a comment was removed or deleted. Moderator action, automod,
spam removal, user deletion, account deletion, or other source-state changes
can look similar from current public HTML.

Active deleted-comment recovery was evaluated and **dropped** (see
`docs/decisions/data_capture_spine_deleted_comment_signal_retrieval_scoped_doctrine_decision_v0.md`):
third-party archives are stale and recovery is unverified, against the
no-body/comment hard stop and the privacy/consent cost. Do not attempt it. The
only safe path remains exact-thread archive fallback with timestamped provenance,
not broad recovery from unofficial caches.

## Stop Lines

Stop instead of widening when any of these occur:

- requested URL is not an exact old Reddit thread URL;
- URL count exceeds the bound;
- operator asks for subreddit crawl, broad source discovery, user/profile
  capture, recommendation expansion, or link following;
- packet output would contain secrets, cookies, tokens, proxy credentials,
  storage state, or private/entitled content not explicitly authorized;
- Direct HTTP, CloakBrowser, or Archive.org returns a visible block or no
  snapshot and no explicit fallback remains;
- the operator asks for commercial Reddit use without a sanctioned commercial,
  enterprise API, or data-licensing path.

## Minimal Closeout

Report:

- command run and working directory;
- exact URL count and hard ceiling;
- cadence mode and window;
- packet path or no packet;
- batch summary path;
- quality summary path, if run;
- counts: capture success, consolidation success, usable yes, needs review, no;
- any visible block, archive fallback result, parser warning, or limitation;
- non-claims.

Do not claim validation, readiness, source completeness, fixture admission, ECR
handoff, Cleaning handoff, Judgment scoring, buyer proof, or commercial
readiness from this playbook.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Reddit current-operator procedure now uses exact old Reddit Direct HTTP first for supplied thread URLs when current old Reddit HTML is the capture target and the bounded batch runner accepts the URL, while retaining CloakBrowser as the primary anti-blocking/browser-visible route when Direct HTTP is unsuitable or blocked."
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - output_authority
  controlling_sources_updated:
    - "docs/product/source_capture_toolbox/reddit_capture_operator_playbook_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-loading.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md"
      reason: "Historical architecture artifact; current operator method order is now carried by the playbook, planning thread, method plan, authorization decision, runbook, and Armory README."
    - path: "docs/product/source_capture_toolbox/cloakbrowser_packet_runner_architecture_independent_pass_v0.md"
      reason: "Historical independent architecture artifact; updating it would rewrite review context rather than current operator doctrine."
    - path: "docs/product/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md"
      reason: "Historical concurrent-structure architecture artifact; current Reddit operator procedure is not governed there."
  stale_language_search: "rg -n \"CloakBrowser-first|CloakBrowser anti-blocking first|anti-blocking browser capture first|recommended_for_reddit_pre_commercial|method_order_observed|current order is CloakBrowser\" docs/product/source_capture_toolbox docs/product/data_capture_source_access_method_plan_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md orca-harness/docs/source_capture_agent_runbook.md"
  stale_language_search_result: "Executed 2026-06-08 after this patch. Remaining hits are historical architecture artifacts, historical patch-reason/DCP text, this receipt's own search string, and updated current fields whose values now say exact old Reddit Direct HTTP first for supplied thread URLs; no live operator-order surface still tells agents to skip a working Direct HTTP capture merely because CloakBrowser exists."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not source completeness proof"
    - "not source discovery authorization"
    - "not broad crawling"
    - "not monitoring"
    - "not commercial Reddit authority"
    - "not ECR, Cleaning, Judgment, or buyer proof"
```
