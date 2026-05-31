# Data Capture Spine Pressure-Test Slot 3 WSO Capture Session v0

```yaml
retrieval_header_version: 1
artifact_role: Data Capture pressure-test capture-session artifact
scope: Records the current WSO bounded Data Capture session for Slot 3 non-target US-domestic resume-driven interview-getting pain.
use_when:
  - Checking the WSO venue capture posture before ECR receipt.
  - Reviewing WSO source-visible language and source-access limits after the Reddit first pass.
  - Preserving WSO limitations before any Reddit+WSO Slot 3 handoff, Cleaning work, or Judgment synthesis.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md
  - docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md
  - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
  - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - docs/product/data_capture_spine_intake_surface_consolidation_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - A later owner decision rejects or supersedes the WSO venue scope.
  - A later WSO raw/source-projection packet supersedes this bounded source-language anchor pass.
  - The accepted intake-surface target, commissioning plan, or obligation contract is materially amended before this capture is receipted.
  - WSO source visibility changes materially or source-language anchors become unavailable at the cited URLs.
```

## Status

Status: `CAPTURE_SESSION_WSO_BOUNDED_SOURCE_LANGUAGE_ANCHORS_V0`.

This artifact records the WSO/non-Reddit venue for the authorized Slot 3
pressure-test frame. It is a bounded public-page capture with source-language
anchors embedded from the start. It does not create a Reddit-style raw JSON
corpus, preserved raw HTML packet, screenshot set, or Mechanical Source
Projection packet.

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Slot 3 WSO pressure-test execution pack
  edit_permission: docs-write for one WSO capture-session Markdown artifact
  target_scope: docs/product/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md
```

## Decision Frame

- Decision question: Can Data Capture preserve the WSO portion of Slot 3
  non-target resume-driven interview-getting pain as an internally inspectable
  bounded venue artifact, with source-language anchors and visible limitations,
  without drifting into source-system bypass, ECR schema, Cleaning, Judgment, or
  runtime/tooling design?
- Owner or owner-context: Orca owner / Chief Architect pressure-testing the
  Data Capture Spine and Mechanical Source Projection intake boundary.
- Consequence: The result determines whether WSO can travel into a later
  Reddit+WSO Slot 3 handoff as a bounded second venue, and which limitations
  must remain visible before any synthesis.
- Allowed decision verbs: `categorical_handoff_to_ECR`, `visible_stop`,
  `visible_blocker`, `rerun`, `re-capture_posture`, or later owner-authorized
  pressure-test patch planning.
- Cutoff posture: Authorized Slot 3 cutoff is Q2 2026. The selected WSO pages
  are older durable pages or 2025 pages; no selected WSO page observed in this
  pass is after Q2 2026.
- Downstream-use intent: Data Capture handoff only. This artifact does not rank
  pains, judge source value, classify credibility, define ECR fields, perform
  Cleaning, or synthesize customer meaning.

## Source Boundary

- Source surfaces in scope:
  - Public WSO forum URLs from the prior Slot 3 discovery note:
    `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot3_nontarget_forum_subagent_output.md`.
  - Public WSO forum pages reachable through current browser/web inspection.
  - The Reddit Slot 3 control note as required routing context:
    `docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md`.
- Boundary compliance: this session used discoverable public page access and
  browser/web inspection only. It did not use login, email unlock, social
  unlock, paid access, private access, deceptive collection, anti-detect
  methods, proxies, automated extraction builds, or runtime/source-system
  tooling.
- Out-of-bounds material observed and excluded:
  - WSO comment-unlock prompts were visible on some pages and were not used.
  - Full hidden or gated comment material is not claimed.
  - Prior source-access planning options for stronger WSO access were not used.

## Capture Mode

- Initial mode: mixed human-led plus agent-assisted public web inspection.
- Material mode changes during the session:
  - The session began by checking the repository state and classifying the
    existing untracked WSO/combined artifacts as stale scratch.
  - The session then reopened the Reddit control note and the prior WSO
    discovery inventory.
  - The session used public browser/web inspection for selected WSO pages.
  - No Mechanical Source Projection was performed because no preserved WSO raw
    source packet was created.

## Per-Obligation Discharge States

| # | Obligation | State | Reason (required for non-`met`) |
| --- | --- | --- | --- |
| 1 | Commissioning Gate | met | |
| 2 | Boundary Compliance | met | |
| 3 | Capture-Event Provenance | partial | Source URLs, selected page titles, visible page dates or relative ages where available, prior discovery note path, current capture date, and operator category are visible, but no local raw HTML/screenshot hash or exact browser acquisition timestamp was recorded per WSO page. |
| 4 | Capture Mode Disclosure | met | |
| 5 | Mode-Change Rule | met | |
| 6 | Raw Observable Fidelity | partial | This artifact embeds bounded source-language anchors and page posture, but no raw WSO HTML, screenshot set, complete comment graph, or row-level projection packet was preserved locally. |
| 7 | Source Identity And Actor Context | partial | WSO surface identity, URLs, titles, handles where visible, role badges where visible, regions where visible, and comment counts where visible are recorded; full actor history and hidden comment context are not claimed. |
| 8 | Decomposed Timing | partial | Public pages expose page dates or relative ages in visible text where available; exact capture timestamps, edit history, and complete comment timestamps are not separately preserved. |
| 9 | Cutoff Posture | met | |
| 10 | Archive / Historical Posture | not_attempted | No Wayback/archive lookup or external archival confirmation was attempted for WSO in this pass. |
| 11 | Source Visibility And Access Limits | met | |
| 12 | Related Context Preservation | partial | The selected pages preserve OP posture and selected visible reply/comment anchors, but this pass does not preserve full thread hierarchy, all comments, or hidden/comment-unlocked material. |
| 13 | Bundled-Offer Structure Observables | not_applicable | Slot 3 WSO is a forum-thread venue, not a bundled offer, settlement, pricing package, or multi-term counterparty package. |
| 14 | Capture Failure And Blocker Visibility | met | |
| 15 | Re-Capture Semantics | not_applicable | No prior accepted WSO capture for this same bounded venue slice was supplied; the old untracked WSO artifact is treated as stale scratch, not as a prior accepted capture. |
| 16 | Categorical Handoff Readiness | partial | The artifact is handoff-ready only as a bounded WSO venue capture with embedded source-language anchors and visible limitations. It is not a complete WSO raw corpus, full comment graph, archive packet, screenshot packet, or Mechanical Source Projection packet. |

Allowed states used: `met`, `partial`, `not_attempted`, `not_applicable`.

## Per-Slice Posture

| Slice | Archive/history posture | Source visibility/access posture | Related context posture | Re-capture relationship |
| --- | --- | --- | --- | --- |
| Prior WSO discovery inventory | Prior local discovery note preserved; no WSO raw page bodies preserved there. | Earlier direct WebFetch attempts were recorded as HTTP 403, while URL inventory and search snippets were captured. | URL inventory includes WSO non-target, resume, no-response, interview-access, advice, and success/counter-signal candidates. | Used as candidate inventory for this current bounded public-page inspection pass. |
| Current WSO public-page inspection | No external archive lookup attempted. | Selected WSO pages were publicly inspectable enough to capture source-language anchors. Pages include heavy navigation/promo envelope and some comment-unlock prompts. | OP/title posture and selected visible comment/reply anchors are preserved below. Full comment graph completeness is not claimed. | Future pass can recapture with screenshots, raw HTML, archive lookup, or account-created access only if separately authorized. |
| WSO hidden/full comments | Not attempted. | Email/social unlock prompts were visible and not used. | Hidden or gated comments are not captured. | Requires a separate owner decision or human-led access path if needed. |
| Mechanical Source Projection | Not applicable in this pass. | No WSO raw source packet exists to project. | No row-level WSO projection exists. | Can be commissioned later only after raw WSO source is preserved. |

## Raw Observable Pointers

Prior discovery source:

```text
docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot3_nontarget_forum_subagent_output.md
```

The prior discovery note records WSO search/query attempts, direct WSO WebFetch
403 blockers, and a URL inventory of candidate WSO threads. Current browser/web
inspection found selected WSO pages publicly inspectable enough to embed bounded
source-language anchors in this artifact.

### Bounded Source-Language Anchors

The excerpts below are short source-language anchors, not a full transcript and
not a cleaned corpus. They preserve enough wording for a fresh checker to see
what was captured without re-fetching the pages.

| Capture ID | URL | Source-visible posture | Source-language anchors |
| --- | --- | --- | --- |
| WSO-01 | `https://www.wallstreetoasis.com/forum/investment-banking/are-non-target-students-doomed-in-ib` | Public WSO forum thread; visible page context includes 46 comments and United States region labels. | Title anchor: "Are non-target students doomed in IB?" OP asks whether firms will look at a non-target applicant and whether it is too late. Visible reply anchors include "significantly harder", "networking is the most important thing", and advice to try a boutique then lateral. |
| WSO-02 | `https://www.wallstreetoasis.com/forum/investment-banking/how-to-recruit-from-a-non-target` | Public WSO forum thread dated Jul 13, 2025; visible region All United States; 19 comments visible at page level. | Title anchor: "How to recruit from a non-target?" OP is a transfer student planning for summer 2027. Visible reply anchors include "network and know ur technicals" and "Find 10-20 places to apply a week." |
| WSO-03 | `https://www.wallstreetoasis.com/forum/investment-banking/how-hard-is-it-really-to-go-past-the-first-round-resume-round-without` | Public WSO forum thread; visible region United States - Midwest; 45 comments visible at page level. | Title anchor asks about getting past the resume round without networking. OP repeats "networking networking networking" and asks whether non-target candidates are doomed. Visible reply anchors include "resume black holes" and "you are going to have to network." |
| WSO-04 | `https://www.wallstreetoasis.com/forum/investment-banking/a-non-targets-failure` | Public WSO forum thread dated Jun 13, 2020; visible region United States - Northeast; 17 comments visible at page level. | Title anchor: "A non-target's failure." OP says they were "gunning for a sophomore SA role" from a non-target and asks "What did I do wrong?" Visible replies include "landed 0 offers" and "direct applications don't do much." |
| WSO-05 | `https://www.wallstreetoasis.com/forum/investment-banking/networking-zero-response-rate` | Public WSO forum thread; visible region All United States; 14 comments visible at page level. | Title anchor: "Networking: zero response rate." OP says they sent "150+ emails" and received "zero responses." Visible replies ask for an example email, cite a "tough hiring market", and suggest more direct outreach language. |
| WSO-06 | `https://www.wallstreetoasis.com/forum/investment-banking/non-target-recruiting-guide-part-i-resume-and-networking` | Public WSO forum thread dated Apr 24, 2018; advice/context slice with comment-unlock prompt visible later on page. | Title anchor: "Non-Target Recruiting Guide Part I: Resume and Networking." Visible guide language frames the non-target issue as "getting into the door" and says candidates must "crush it from there." |
| WSO-07 | `https://www.wallstreetoasis.com/forum/investment-banking/i-finally-did-it-extreme-non-target-to-my-dream-role-investment-banking` | Public WSO forum thread; visible OP context is UK non-target, so this is related counter-signal context, not US-domestic core. | Title anchor: "Extreme Non-Target to my dream role." OP says "worst 10 universities UK", used "cold LinkedIn messaging", expected IB to be easy after internship, and then "I was wrong." |

### Venue Envelope Notes

- WSO pages expose substantial navigation, promotional, related-link, profile,
  and unlock scaffolding.
- This pass records source-language anchors and page posture only. It does not
  mechanically separate source-envelope noise into projection rows.
- The current artifact should be treated as a bounded WSO venue capture, not as
  a complete WSO corpus or source-system extraction.

## Failures, Blockers, and Limitations

- Capture-owned failures observed:
  - No local WSO raw corpus existed before this pass.
  - No WSO raw HTML, screenshots, archive captures, or projection rows were
    saved during this pass.
  - Prior subagent WebFetch attempts against WSO recorded HTTP 403, while
    current browser/web inspection could view selected public pages. This mixed
    access posture must remain visible.
- Visible limitations to travel downstream:
  - Full comment graph completeness is not claimed.
  - Hidden or comment-unlocked material is not captured.
  - No external archive lookup was attempted.
  - WSO-07 is outside the US-domestic core frame and should travel only as
    related/counter-signal context.
  - No Mechanical Source Projection packet exists for WSO.
  - WSO pages contain substantial source-envelope noise that was not
    mechanically projected away in this pass.
- Out-of-bounds material treated as out of bounds:
  - No login, email unlock, social unlock, paid access, private access,
    anti-detect method, proxy, source-system build, scraper, or API was used.
  - No ECR schema, Cleaning implementation, or Judgment synthesis is included.

## Agent-Assistance Context

- Allowed agent verbs used:
  - Read Orca overlay and controlling product docs.
  - Inspect repository state for existing WSO and combined Slot 3 artifacts.
  - Inspect prior local WSO discovery note and Reddit control note.
  - Open selected public WSO URLs through browser/web inspection.
  - Draft this capture-session Markdown artifact.
- Discarded candidates and discard reason categories:
  - Prior WSO search-result snippets were not treated as full source bodies.
  - Stronger access-method planning options were not used because they were
    outside this bounded WSO pass.
  - WSO-07 was not treated as US-domestic core evidence because the visible OP
    context is UK non-target.
  - The existing untracked WSO and combined handoff artifacts were treated as
    stale scratch because they used stale obligation vocabulary and lacked
    bounded source-language anchors.
- Any cross of the allow/forbid line: none observed. No login, unlock,
  scraping, runtime build, source-system planning, ECR schema, Cleaning
  transformation, or Judgment conclusion was performed.

## Categorical Handoff Or Visible Stop

- Handoff state: `categorical_handoff_to_ECR`.
- Reason if not `categorical_handoff_to_ECR`: not applicable.
- Visible limitations attached to handoff:
  - Handoff is only for the bounded WSO source-language anchor pass.
  - This is not a full WSO raw corpus, not a full WSO comment graph, not a WSO
    archive packet, not a WSO screenshot packet, and not a WSO Mechanical Source
    Projection packet.
  - ECR may receipt categorical source/provenance/visibility context, but this
    artifact does not define ECR fields, IDs, storage, schema, table shape, or
    runtime receipt mechanism.
  - If WSO becomes materially load-bearing downstream, a later owner decision
    may still choose recapture with raw HTML, screenshots, archive lookup, or
    account-created access.

## LLM Capture-Visibility Checker Output

- Output: `visible_capture_limitation`.
- Invocation boundary:
  - This was an artifact-internal checker pass using the pinned checker
    questions in the same Codex execution thread. The stricter separate manual
    GPT-5.5 UI invocation specified by the commissioning plan was not performed
    for this WSO artifact. That model-separation limitation travels downstream.
- Specifics:
  - Obligation 3: exact browser acquisition timestamp and local raw file hash
    were not recorded per WSO page.
  - Obligation 6: source-language anchors are visible, but raw WSO HTML,
    screenshots, full comment graph, and projection rows are not preserved.
  - Obligation 8: complete item-level timing, edit history, and comment timing
    are not separately preserved.
  - Obligation 10: archive/history lookup was not attempted.
  - Obligation 12: full thread hierarchy and hidden/comment-unlocked material
    are not preserved.
  - Obligation 16: handoff is categorical only for the bounded WSO anchor pass,
    not for a complete WSO corpus or projection packet.
  - Checker scope: source fidelity, source completeness, and full WSO comment
    graph completeness were not independently verified.
- Remediation taken by capture operator:
  - Source-language anchors were embedded in the artifact.
  - Limitations were made explicit in the obligation table, per-slice posture,
    raw observable pointers, failures/limitations, and categorical handoff
    sections.
  - No remediation attempted live WSO recapture, login/unlock, archive lookup,
    raw HTML preservation, runtime tooling, ECR design, Cleaning, or Judgment.
- Post-remediation re-invocation:
  - None performed; no second checker-token output is asserted.

## Combined Handoff Decision

The current WSO artifact is suitable to carry into a later Reddit+WSO Slot 3
combined handoff as a bounded second-venue capture with visible limitations.

The existing untracked combined handoff artifact should remain scratch until it
is rewritten against:

- the two current Reddit batch artifacts;
- `docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md`;
- this WSO bounded source-language anchor artifact; and
- the current amended obligation contract vocabulary.

No Reddit+WSO synthesis is performed in this artifact.

## Non-Claims

This artifact does not:

- complete a full WSO raw corpus capture;
- create a WSO Mechanical Source Projection packet;
- validate, certify, approve, accept, or harden the Data Capture Spine;
- discharge the full pressure-test batch;
- claim source quality, credibility, integrity, relevance, representativeness,
  or downstream admissibility;
- define ECR fields, IDs, schemas, storage, file formats, or runtime receipt
  mechanisms;
- perform Cleaning, normalization certification, semantic dedupe, clustering,
  summarization, or translation;
- perform Judgment, Signal Use Classification, Decision Strength, Action
  Ceiling, discounting, exclusion, buyer proof, customer synthesis, or
  commercial-readiness assessment;
- authorize source-system planning, scrapers, APIs, dashboards, storage,
  packages, tests, deployment, commits, pushes, or PRs.
