# Reddit Packet Consolidation Runner Structural Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Structural spec
scope: Offline Reddit packet consolidation core that consumes existing Source Capture Packets and produces derived, provenance-linked Reddit thread artifacts.
use_when:
  - Scoping or implementing the Reddit packet consolidation runner.
  - Checking the boundary between Reddit capture, packet preservation, parsing, consolidation, and later monitoring or storage.
  - Reviewing whether a proposed Reddit consolidation implementation preserves packet-first provenance and visible refusal behavior.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md
  - orca-harness/source_capture/packet_inspection.py
  - orca-harness/source_capture/source_quality.py
stale_if:
  - Source Capture Packet manifest semantics change.
  - read_packet_leniently or PacketConformanceReport behavior changes.
  - Reddit consolidation is implemented with a different module boundary or output shape.
  - Bounded discovery, monitoring, archive fallback, or storage receives separate accepted architecture that changes the packet-producer relationship.
```

## Status

Status: `STRUCTURAL_SPEC_V0`.

This is a structural spec for the Reddit packet consolidation core. It locks the
implementation-facing boundary for a future runner, but it does not implement
the runner, install dependencies, authorize live Reddit access, admit fixtures,
or validate parser correctness.

CA adjudication: delegated adversarial-review hunks accepted on 2026-06-06.
The source packet directory remains read-only input; reconciliation mismatch is
not clean success; and the empty-success vs failed-extraction fixture row is
binding for the first implementation slice.

## Locked Decisions

Future implementation must preserve these decisions unless a later accepted
architecture or spec supersedes this artifact:

1. **Module boundary:** implement under
   `orca-harness/source_capture/reddit_consolidation/`, not as a top-level
   `orca-harness/source_capture/*.py` module.
2. **Packet reader reuse:** consume packets through `read_packet_leniently()`
   and `PacketConformanceReport`; do not build a second manifest reader.
3. **Packet-first boundary:** capture produces Source Capture Packets;
   consolidation consumes Source Capture Packets.
4. **Comment structure:** write a flat comment list with `parent_id` pointers,
   not recursive nested JSON.
5. **Closed comment posture:** use a closed posture vocabulary for comment node
   state: `present`, `deleted`, `removed`, `collapsed`, `missing_dom`,
   `unavailable`.
6. **Fixtures before parser code:** hand-author a small, license-safe old Reddit
   HTML fixture set before parser implementation. Fixtures are parser-test
   scaffolding, not captured packets.

## Core Boundary

The Reddit consolidation core is an offline packet consumer.

Core responsibilities:

- inspect one Source Capture Packet directory;
- decide whether that packet is eligible for Reddit consolidation;
- resolve and hash-check the preserved raw HTML artifact;
- parse preserved browser-visible old Reddit HTML;
- write a derived JSON artifact that points back to the packet;
- write a human-readable consolidation receipt;
- expose warnings, limitations, and non-claims.

Satellite responsibilities, explicitly outside the core:

- live CloakBrowser capture;
- Archive.org or other archive fallback capture;
- bounded target discovery or intake;
- low-volume monitoring;
- storage, database, queue, scheduler, dashboard, or export corpus;
- commercial Reddit API behavior;
- ECR, Cleaning, Judgment, source-quality scoring, fixture admission, or buyer
  proof.

Later live capture, archive fallback, bounded discovery/intake, and monitoring
layers may feed this core only by producing Source Capture Packets or
packet-equivalent preserved inputs accepted by a later spec. They must not add
fetching, crawling, monitoring, or storage behavior to the consolidation core.

## Input Packet Contract

Input is one packet directory or manifest path. The future runner should accept
the same user-facing convention already used by source-quality helpers:

- a directory containing `manifest.json`; or
- an explicit path to `manifest.json`.

The runner must resolve that input to a manifest path, then call
`read_packet_leniently(manifest_path)`.

The runner must not:

- parse a manifest by hand;
- rebuild the packet schema;
- dispatch to per-version packet schemas;
- proceed when `PacketConformanceReport.packet` is `None`;
- use a non-conforming manifest as if it were a packet.

For conforming packets, the runner must resolve raw files through the packet's
`preserved_files[*].file_id` and `relative_packet_path` fields. It must
recompute `sha256` over the stored raw bytes and compare the result to the
manifest's recorded hash before treating the raw file as parser input.

The parser input is the preserved raw HTML file, not the packet receipt,
metadata JSON, visible-text sidecar, or an external URL.

## Eligibility And Refusal Rules

Each refusal must be visible and typed. A refused packet must not produce a
derived JSON artifact.

Required refusal cases:

| Refusal | Required behavior |
| --- | --- |
| Manifest missing or unreadable | Refuse with a manifest-read failure. |
| Manifest is parseable but non-conforming | Refuse using the `PacketConformanceReport` conformance facts. |
| Manifest declares a non-current version | Refuse visibly; do not dispatch to a guessed historical schema. |
| No validated packet is available | Refuse; do not build partial packet state. |
| Packet is not Reddit-like or old-Reddit/browser-visible HTML-like | Refuse as ineligible source surface. |
| No preserved raw HTML file can be resolved | Refuse as missing DOM/body input. |
| Preserved file path is missing | Refuse with the missing `file_id` / path. |
| Stored bytes hash does not match manifest hash | Refuse with hash mismatch; do not parse. |
| Packet or raw artifact appears credential/session/profile contaminated | Refuse as contaminated scratch. |
| Parser cannot identify the required thread/post envelope | Refuse or emit a parse-failure result with no successful thread artifact; do not write plausible-empty success JSON. |

Exit-code convention for the future runner should match existing source-capture
runners:

- `0`: consolidation artifact and receipt written;
- `2`: bad CLI input or invalid arguments;
- `3`: eligible runner invocation failed or refused visibly.

Exit `0` is not a claim of Reddit completeness, parser correctness, source
quality, canonical source body, ECR readiness, Cleaning readiness, Judgment
readiness, or Data Capture handoff readiness.

## Derived JSON Contract

The derived artifact is a consolidation artifact. It is not the source body and
does not replace the packet.

The source packet directory is read-only input. The runner must not modify, add
to, delete from, or otherwise mutate the packet directory or its preserved
files; the derived JSON artifact and the consolidation receipt are written to a
separate output location so the canonical packet stays byte-for-byte intact and
physically distinct from the derived text.

Top-level shape:

```text
reddit_thread_consolidation:
  schema_version
  source_packet
  thread
  post
  comments
  counts
  warnings
  limitations
  non_claims
```

Required source-packet provenance:

- packet path supplied by the operator;
- manifest path;
- packet id when available;
- manifest hash or packet directory hash when implemented;
- raw HTML `file_id`;
- raw HTML `relative_packet_path`;
- raw HTML `sha256`;
- source family and surface from the packet;
- capture method/provenance fields available from packet metadata.

Required thread/post fields:

- `thread_id`, when visible or derivable from visible permalink structure;
- `subreddit`, when visible;
- `title`, when visible;
- `permalink`, when visible;
- visible author state;
- visible timestamp state;
- visible score state;
- post body text as derivative text only;
- pointer back to raw HTML provenance for the body.

Required comment fields:

- stable row id assigned by the consolidator;
- `comment_id`, when visible or safely derivable from visible markup;
- `parent_id`, when visible from markup nesting;
- `depth`, when visible from markup nesting;
- visible author state;
- visible timestamp state;
- visible score state;
- derivative body text;
- `comment_posture`, one of:
  - `present`
  - `deleted`
  - `removed`
  - `collapsed`
  - `missing_dom`
  - `unavailable`
- provenance pointer back to raw HTML file id and packet path;
- parser warnings for that node.

Comments must be a flat list. A consumer may reconstruct a tree from
`parent_id`, but the consolidation artifact itself must not rely on a recursive
tree as the primary representation.

## Canonical Provenance Rule

Raw packet provenance is canonical. Parsed text is derivative.

The derived JSON may carry post/comment text for convenience, but every
source-language field must remain subordinate to a resolvable raw packet pointer.
If the raw packet pointer cannot be resolved, the artifact must not present the
parsed text as the source body.

The consolidator must not:

- treat parsed text as the canonical source;
- silently repair missing source language;
- infer deleted or removed text;
- infer author, timestamp, score, or nesting when not visible;
- dedupe, cluster, rank, score, classify, or judge comments;
- construct ECR fields or Cleaning outputs.

Unknown, hidden, deleted, removed, collapsed, or missing DOM states must travel
as explicit states or limitations.

## Parser Contract

The parser is an offline pure parser over already-preserved HTML.

Allowed parser dependency:

- `BeautifulSoup` / `bs4`, but only inside
  `orca-harness/source_capture/reddit_consolidation/` or behind a lazy injected
  parser seam. It must not be imported from a top-level
  `orca-harness/source_capture/*.py` module.

Forbidden parser behavior:

- network access;
- live URL fetch;
- browser automation;
- archive lookup;
- Reddit API calls;
- source discovery;
- monitoring;
- storage/export side effects;
- credential/session/profile/proxy use;
- CAPTCHA solving;
- semantic inference repair;
- dedupe, clustering, scoring, ranking, or credibility judgment.

Implementation should add a sibling contract test for the
`source_capture/reddit_consolidation/` package that forbids network/fetch/browser
imports while allowing `bs4`.

Parser output should be modeled as a strict intermediate representation before
being written to the final derived JSON. That intermediate model is a parser
handoff, not a source-of-truth replacement.

## Consolidation Receipt Contract

The future runner must write a human-readable receipt next to the derived JSON.

The receipt must state:

- packet path and manifest path inspected;
- raw HTML file id/path/hash used;
- thread/post fields found;
- number of comment nodes parsed;
- number of deleted/removed/collapsed/missing/unavailable nodes;
- parser warnings;
- limitations;
- refusal or partial-visibility posture where relevant;
- non-claims.

The receipt must reconcile visible node counts when the parser can observe them.
A clean rollup must not hide failed, limited, deleted, removed, collapsed, or
missing-DOM nodes. When the parsed comment count is below the comment nodes the
parser can observe in the preserved DOM, the gap must travel as a visible parse
limitation or failure; a reconciliation mismatch is not a clean success and must
not be written as an exit-`0` plausible-empty success artifact.

Required non-claims:

- not validation;
- not readiness;
- not Reddit source completeness proof;
- not live Reddit capture;
- not Reddit monitoring;
- not source discovery;
- not broad crawling;
- not storage, database, queue, scheduler, dashboard, or export corpus;
- not commercial API behavior;
- not source-quality scoring;
- not fixture admission;
- not canonical source body;
- not ECR design;
- not Cleaning implementation;
- not Judgment scoring or judgment-quality evidence.

## Fixture Matrix

The first implementation should create hand-authored, license-safe fixtures.
Fixtures should be minimal old-Reddit-like HTML, not copied Reddit pages and not
captured packets.

Required fixtures:

| Fixture | Must prove |
| --- | --- |
| Normal thread | title, post body, at least two comments, visible nesting, visible metadata where represented. |
| Nested replies | flat comments preserve `parent_id` and depth without recursive primary output. |
| Deleted and removed comments | deleted/removed states are visible and not treated as absent or repaired. |
| Collapsed or unavailable node | collapsed/unavailable posture travels with limitations. |
| Missing DOM/body input | runner refuses or fails visibly; no plausible-empty success artifact. |
| Empty-success vs failed extraction | a genuinely empty thread (envelope present, zero comments) is recorded as a reconciled success, while an envelope-present thread whose parsed comment count is below the observable comment nodes fails visibly as a parse limitation rather than writing plausible-empty success JSON. |
| Non-Reddit packet | eligibility gate refuses visibly. |
| Malformed HTML | parser warning/failure is visible; no silent success if required envelope is missing. |
| Hash mismatch | raw-file hash mismatch refuses before parsing. |
| Score hidden / id not visible | unknown/not-visible state travels explicitly. |

Fixture tests should build or emulate Source Capture Packet directories using
the existing writer/packet model where practical, rather than bypassing the
packet contract.

## Later Plug-In Seams

These are future seams only. They are not part of this core spec's
implementation scope.

### Live CloakBrowser Capture

Live capture may produce a Source Capture Packet containing old Reddit or
browser-visible Reddit HTML. The consolidation core consumes that packet after
capture completes. It must not invoke CloakBrowser itself.

### Archive Fallback

Archive fallback may produce a packet with archived HTML. A later accepted spec
may add an archive-specific parser surface or reuse the same old-Reddit parser
when the archived body matches the expected shape. Archive lookup does not
belong inside the consolidation core.

### Bounded Discovery / Intake

Bounded discovery or intake may define approved subreddits, themes, thread
families, or monitored thread sets. It feeds capture. It does not feed the
consolidation core directly except through packets.

### Low-Volume Monitoring

Monitoring may schedule repeated capture of approved targets. It is a packet
producer. It must not parse, store, or judge source meaning inside the monitor.

### Storage / Export

Durable storage, database, queue, dashboard, corpus export, or retained dataset
behavior requires separate owner authorization and retention/sensitivity
handling. The consolidation core writes local derived artifacts only.

## Implementation Scoping Notes

Likely future touch points:

- `orca-harness/source_capture/reddit_consolidation/`
- `orca-harness/runners/run_reddit_consolidation.py`
- `orca-harness/tests/unit/test_reddit_consolidation*.py`
- `orca-harness/tests/contract/test_reddit_consolidation*.py`
- hand-authored fixtures under an implementation-appropriate test fixture path

Expected validation, when implementation is later authorized:

- offline unit tests over fixtures;
- refusal tests over non-conforming, non-Reddit, missing-DOM, malformed, and
  hash-mismatch packets;
- contract test forbidding network/fetch/browser imports in the consolidation
  package;
- no live Reddit access in tests.

This section is implementation-scoping input only. It is not an implementation
route, patch queue, validation result, dependency-install authorization, or
source-changing authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Reddit packet consolidation now has a contract-first structural spec: the core is an offline packet consumer under source_capture/reddit_consolidation that reuses read_packet_leniently, writes derivative provenance-linked thread artifacts, and keeps live capture, discovery, monitoring, archive lookup, storage, commercial API behavior, ECR, Cleaning, and Judgment outside the core."
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - workflow_authority
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/retrieval-metadata.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "orca-harness/docs/adapter_author_contract.md"
    - "orca-harness/source_capture/packet_inspection.py"
    - "orca-harness/source_capture/source_quality.py"
  intentionally_not_updated:
    - path: "docs/workflows/data_capture_spine_consolidation_map_v0.md"
      reason: "The map already routes Reddit consolidation planning through the Armory README and planning thread. This spec is new and can be added to map surfaces in a separate navigation-index pass if owner wants broader discoverability."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "This artifact is the first structural spec for the runner. The Armory README can index it after adversarial review and CA adjudication, avoiding premature promotion before spec hardening."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
      reason: "The planning thread remains the higher-level planning artifact. This spec narrows implementation-facing consolidation structure without changing the planning-thread success-signal gates."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden outputs did not change."
    - path: "orca-harness/docs/adapter_author_contract.md"
      reason: "Adapter author conventions did not change; this spec applies the existing packet-consumer precedent, not a new adapter convention."
  stale_language_search: "rg -n \"capture produces packets|consolidation consumes packets|Reddit packet consolidation|reddit_packet_consolidation_runner_structural_spec|source_capture/reddit_consolidation|read_packet_leniently\" forseti/product/spines/capture/core/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md forseti/product/spines/capture/core/source_capture_toolbox/README.md docs/workflows/data_capture_spine_consolidation_map_v0.md orca-harness/docs/source_capture_agent_runbook.md"
  stale_language_search_result: "Executed 2026-06-06 after writing this artifact. Hits were confined to this new spec: retrieval header/body references to the Reddit packet consolidation core, locked source_capture/reddit_consolidation placement, read_packet_leniently reuse, and this DCP receipt. No checked README, map, or runbook surface claimed implementation, validation, readiness, live capture, monitoring, storage, or commercial API authorization from this spec."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation"
    - "not dependency-install authorization"
    - "not live Reddit capture authorization"
    - "not monitoring, source discovery, storage, dashboard, or commercial API authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Non-Claims

This structural spec is not implementation, validation, readiness, source-access
authorization, legal sufficiency, live Reddit capture authorization, monitoring
authorization, source-discovery authorization, broad-crawling authorization,
archive-fetch authorization, storage/dashboard/deployment authorization,
commercial API authorization, BeautifulSoup install authorization, fixture
admission, source-quality scoring, ECR design, Cleaning implementation, Judgment
design, buyer proof, staging, commit, or deployment.
