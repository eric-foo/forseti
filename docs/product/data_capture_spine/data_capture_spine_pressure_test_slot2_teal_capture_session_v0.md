# Data Capture Spine Pressure-Test Slot 2 Teal Capture Session v0

```yaml
retrieval_header_version: 1
artifact_role: Data Capture pressure-test capture-session artifact
scope: Records the formalized Slot 2 Teal capture session for AI-generic resume-tool pricing, features, and archive-history posture under a full host/content access failure.
use_when:
  - Checking Slot 2 Data Capture evidence before all-slot pressure-test synthesis.
  - Reviewing Teal source-access failure, URL inventory, archive availability, and non-verbatim search-summary limitations.
  - Preserving Slot 2 pressure-test findings without hardening the obligation contract or designing source-access tooling.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_execution_authorization_v0.md
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - A later owner decision rejects or supersedes the Slot 2 source boundary.
  - A later Teal verbatim, raw HTML, screenshot, browser, archive-content, or authenticated/entitled recapture supersedes this access-failed capture.
  - The accepted intake-surface target, commissioning plan, or obligation contract is materially amended before all-slot synthesis.
  - Teal pricing, feature posture, archive availability, source-access posture, or product surfaces change materially before downstream use.
```

## Status

Status: `CAPTURE_SESSION_SLOT2_TEAL_FORMALIZED_FROM_OPERATOR_WORKFILE_V0`.

This artifact formalizes the root operator workfile
`slot2_teal_CAPTURE_operator_workfile.md` into a durable Data Capture
pressure-test capture-session artifact. It does not re-capture Teal, does not
promote WebSearch summaries into source language, does not fetch archive
content, and does not authorize anti-block, browser, scraper, proxy, API, or
source-access tooling.

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Slot 2 Teal pressure-test formalization pack
  edit_permission: docs-write for one Slot 2 capture-session Markdown artifact
  target_scope: docs/product/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - slot2_teal_CAPTURE_operator_workfile.md
    - docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot2_teal_subagent_output.md
```

## Source Basis

| Source | SHA256 | Role |
| --- | --- | --- |
| `slot2_teal_CAPTURE_operator_workfile.md` | `FE742C4A4410CC49136C10D1CA3258589E9335FDF4F8C2F3B3EFD588485BE5FB` | Operator-filled Slot 2 capture workfile. |
| `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot2_teal_subagent_output.md` | `39B3E7CEBC908FE43060671702771DC4242982E51E5FD8EE7BA34F02A511A038` | Agent-assisted enumerate/fetch/archive raw material used by the operator. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5` | Current amended Data Capture obligation contract used for vocabulary normalization. |
| `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` | `3D9AC208A8AF68160A43F3EB3512082BF0F9B10D3840331FE82F544E307820EB` | Slot 2 commissioning shape. |
| `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md` | `BCA50C80A7EAA889DC0B01377FFB80635BAC6DDC30F3A4FA654B42CC319CACA3` | First-batch execution authorization. |

## Formalization Note

The root workfile predates the amended obligation-contract vocabulary. This
formalization updates surface vocabulary without replaying the source capture:

- The older #6 label is normalized to `Raw Observable Fidelity`.
- The older #16 label is normalized to `Categorical Handoff Readiness`.
- Tool, host, origin, and archive-content failures are not rewritten as
  boundary `blocked`.
- The old workfile's explicit missing-state pressure is preserved as
  pressure-test evidence, but the formal obligation table uses the current
  contract states `access_failed`, `cannot_assess`, and `assessed_not_met`
  where they now apply.
- The old #16 handoff pressure is treated under the current contract as
  Capture-owned handoff readiness, not actual ECR receipt.

No new source claim is introduced here beyond vocabulary normalization and
durable capture-session packaging.

## Decision Frame

- Decision question: What does Teal (`tealhq.com`) offer and charge through
  its free and paid Teal+ tier structure, AI resume tools, job-tracking,
  Chrome-extension feature posture, and approximately 12-month change history,
  so jb can position against the AI-generic resume-tool flank and reference
  broader-market AI resume pricing?
- Owner or owner-context: jb owner; pre-launch positioning and pricing-reference
  decision.
- Consequence: Informs jb's competitive positioning and pricing reference on
  the AI-generic flank, complementing Slot 1's finance-specialized substitute
  flank.
- Allowed decision verbs: `categorical_handoff_to_ECR`, `visible_stop`,
  `visible_blocker`, `rerun`, `re-capture_posture`, or later owner-authorized
  pressure-test patch planning.
- Cutoff posture: Live-state cutoff is 2026-05-28; approximately 12-month
  prior-window comparison was desired but archive content was not captured.
- Downstream-use intent: Data Capture evidence for jb positioning and pricing
  reference only. This artifact is not buyer-facing and does not perform
  Judgment, Cleaning, ECR schema design, or product synthesis.

## Source Boundary

- Primary source surface: `tealhq.com` public web pages, including home,
  `/pricing`, `/tools`, `/tool/<name>`, `/post/<slug>`, and
  `/career-paths/*` surfaces.
- Extended source surface: `help.tealhq.com` product-documentation pages and
  `app.tealhq.com` app-surface pointers, as confirmed in the operator workfile.
- Enumerated adjacent surface: `/job/<slug>` listings hosted on Teal are kept
  as a separate carrier group, not collapsed into Teal product claims.
- Archive surface: `web.archive.org` snapshots for the change-history
  sub-question; `archive.org/wayback/available` returned snapshot availability
  and dates.
- Boundary compliance: The session used public/discoverable marketing,
  product, docs, app-pointer, and archive surfaces only. No private area,
  unauthorized account access, paid/coworker entitlement, deceptive access,
  obvious spillover, or undisclosable method was used.
- Source-boundary note: The 403 responses are host/origin access failures
  against in-bound public surfaces, not boundary hard stops.

## Capture Mode

- Initial mode: human-led operator capture with agent-assisted URL enumeration,
  WebFetch page retrieval attempts, WebSearch enumeration, and archive
  availability checks.
- Material mode change: intended verbatim/structured fetch degraded to URL
  enumeration, archive-availability posture, and flagged non-verbatim
  WebSearch summary excerpts after live Teal pages returned HTTP 403 and
  `web.archive.org` snapshot content access failed.
- Material mode limitation: no verbatim live Teal page content, archive
  snapshot body, raw HTML, screenshot, layout capture, or Mechanical Source
  Projection packet was preserved. Product-surface facts in this artifact are
  pointers or non-verbatim search-summary fragments only.

## Per-Obligation Discharge States

| # | Obligation | State | Reason (required for non-`met`) |
| --- | --- | --- | --- |
| 1 | Commissioning Gate | met | |
| 2 | Boundary Compliance | met | |
| 3 | Capture-Event Provenance | met | |
| 4 | Capture Mode Disclosure | met | |
| 5 | Mode-Change Rule | met | |
| 6 | Raw Observable Fidelity | access_failed | Source material appears in-bound and capture attempted access, but live Teal pages returned HTTP 403 and `web.archive.org` snapshot content failed to return bodies. No verbatim source language, raw HTML, screenshot, visible structure, or archive content was preserved; only URL inventory, archive availability, and flagged non-verbatim search-summary fragments remain. |
| 7 | Source Identity And Actor Context | partial | Teal source identity, registered-domain family, same-org subdomains, app pointer, and job-listing carrier distinction are visible. Actor/audience specificity from page content cannot be confirmed because page bodies were not retrieved. |
| 8 | Decomposed Timing | met | |
| 9 | Cutoff Posture | partial | Capture date, re-confirmation date, cutoff posture, and archive snapshot dates are visible, but the captured signal is empty enough that substantive pre/post/mixed positioning cannot be inspected. |
| 10 | Archive / Historical Posture | partial | Archive snapshot existence and dates were captured through `archive.org/wayback/available`, but `web.archive.org` snapshot content access failed and full snapshot enumeration through blocked endpoints was not performed. |
| 11 | Source Visibility And Access Limits | met | |
| 12 | Related Context Preservation | access_failed | Related page, tool, pricing, help, app, job-listing, and archive context were sought, but live and archive content retrieval failed. The artifact preserves URL/context pointers and limitations, not source-language related context. |
| 13 | Bundled-Offer Structure Observables | partial | Search-summary fragments point to a free tier and paid Teal+ weekly/monthly/quarterly pricing, but those fragments are non-verbatim, internally conflicting, and not fetched source content. Source-visible bundle structure, packaging cues, dependencies, and framing were not preserved. |
| 14 | Capture Failure And Blocker Visibility | met | |
| 15 | Re-Capture Semantics | not_applicable | First capture of Teal; no prior same-slice capture was supplied. |
| 16 | Categorical Handoff Readiness | assessed_not_met | Handoff readiness is assessable and not satisfied for the decision frame: Teal pricing, features, and change-history content were not captured as inspectable source material. Only failure posture, URL inventory, archive availability, and non-verbatim pointers are available for downstream inspection. |

Allowed states used: `met`, `partial`, `access_failed`, `assessed_not_met`,
`not_applicable`.

## Per-Slice Posture

| Slice | Archive/history posture | Source visibility/access posture | Related context posture | Re-capture relationship |
| --- | --- | --- | --- | --- |
| Teal live pages (`tealhq.com`, `www.tealhq.com`, root and subpaths) | Snapshot dates exist for selected homepage, pricing, tools, resume-builder, and post URLs. | HTTP 403 from live pages; no body content retrieved. | URL inventory exists; source page content does not. | Re-capture requires an authorized path that can retrieve Teal live page bodies. |
| `help.tealhq.com` docs | Not separately archived in this session. | Enumerated through WebSearch; not fetched as source content. | Product-doc pointers are visible, but docs content is not preserved. | Re-capture should fetch docs directly if feature/tier detail matters. |
| `app.tealhq.com` app pointer | Not separately archived in this session. | Enumerated as `https://app.tealhq.com/job-tracker`; not fetched. | App-surface pointer is visible, but app state/content is not preserved. | Re-capture may require allowed account-created or entitled access if the decision frame later needs app-surface observables. |
| `/job/<slug>` listings | Not separately archived in this session. | Enumerated through WebSearch; kept as carrier content, not Teal product claims. | Carrier distinction is visible; employer/job content is not used as product evidence. | Re-capture only if later source-boundary decision makes job listings material. |
| Archive snapshots | `archive.org/wayback/available` returned closest snapshot URLs and dates for selected targets. | Direct `web.archive.org/web/<timestamp>/<url>` content fetches failed at the tool layer. | Historical pricing/product bodies are not inspectable. | Re-capture requires a separately authorized archive-capable path. |
| WebSearch snippets | Not historical capture. | Search returned URL lists and model-generated summary text. | Non-verbatim fragments are pointers only; specific claims require source recapture. | Re-capture should verify any price, feature, or claim against source pages before downstream use. |

## Raw Observable Pointers

### Preserved Source Pointers

- Root and primary pages:
  - `https://www.tealhq.com/`
  - `https://www.tealhq.com/pricing`
  - `https://www.tealhq.com/tools`
  - `https://www.tealhq.com/privacy-policy`
  - `https://www.tealhq.com/partner/affiliate`
- Tool and product pages:
  - `https://www.tealhq.com/tools/resume-builder`
  - `https://www.tealhq.com/tool/resume-rewriter`
  - `https://www.tealhq.com/tool/resume-summary-generator`
  - `https://www.tealhq.com/tool/resume-job-description-match`
  - `https://www.tealhq.com/tool/job-search-chrome-extension`
  - `https://www.tealhq.com/tool/job-search-crm`
  - `https://www.tealhq.com/tool/career-goal-tracker`
  - `https://www.tealhq.com/tools/linkedin-review`
  - `https://www.tealhq.com/tools/autofill-job-applications`
  - `https://www.tealhq.com/tools/job-tracker`
  - `https://www.tealhq.com/tools/contacts-tracker`
- Blog and update pages:
  - `https://www.tealhq.com/post/best-ai-resume-builders`
  - `https://www.tealhq.com/post/whats-ahead-a-look-at-teal`
  - `https://www.tealhq.com/post/updates-to-the-teal-chrome-extension-navigation-bar`
  - `https://www.tealhq.com/post/is-linkedin-premium-worth-it`
  - `https://www.tealhq.com/post/linkedin-features`
  - `https://www.tealhq.com/post/lazyapply-reviews`
  - `https://www.tealhq.com/post/preparing-for-your-job-search`
  - `https://www.tealhq.com/post/future-workplace-trends`
  - `https://tealhq.com/post/job-search-checklist`
- Help/docs and app pointers:
  - `https://help.tealhq.com/en/`
  - `https://help.tealhq.com/en/articles/9530153-teal-vs-teal`
  - `https://help.tealhq.com/en/articles/9535168-is-there-a-teal-free-trial`
  - `https://help.tealhq.com/en/articles/9508933-getting-started-resume-builder`
  - `https://help.tealhq.com/en/articles/9457685-downloading-the-teal-job-search-companion-chrome-extension`
  - `https://help.tealhq.com/en/articles/12060992-using-the-job-matcher`
  - `https://help.tealhq.com/en/collections/9568976-resume-builder`
  - `https://help.tealhq.com/en/collections/9568978-chrome-extension`
  - `https://app.tealhq.com/job-tracker`

### Archive Snapshot Availability

Archive availability was partly captured, but snapshot content was not.

- Homepage snapshots returned around 2025-05-04, 2025-11-02, and
  2026-02-28.
- Pricing snapshots returned around 2025-04-26, 2025-11-24, and 2026-05-08.
- `/tools` snapshot returned around 2025-11-04.
- `/tools/resume-builder` snapshot returned around 2025-11-03.
- `/post/updates-to-the-teal-chrome-extension-navigation-bar` snapshot returned
  around 2025-07-11.
- Several probes returned empty `archived_snapshots`, including tested
  homepage, pricing, `/features`, and `/post/whats-ahead-a-look-at-teal`
  variants. The capture cannot distinguish genuine absence from endpoint
  limitation without a fuller archive path.

### Non-Verbatim Search-Summary Pointers

These fragments are preserved only as flagged search-summary pointers. They are
not source-language preservation and should not be used as verified Teal claims
without recapture.

- Search summaries pointed to Teal+ weekly, monthly, and quarterly pricing of
  `$13`, `$29`, and `$79`, with no annual plan.
- A separate search-summary fragment pointed to Teal+ at `$9/week`, conflicting
  with the `$13/week` pointer.
- A search-summary fragment pointed to a free tier with resume editing/exporting
  and job-tracker bookmarking.
- A search-summary fragment pointed to the Chrome extension as a featured
  Chrome Web Store extension rated `4.9` out of `5`.
- A search-summary fragment pointed to a 2025-02-26 Chrome Extension and
  Navigation Bar update post.

## Failures / Blockers / Limitations

- All attempted live `tealhq.com` root and subpath WebFetch calls returned
  HTTP 403.
- `https://www.tealhq.com/sitemap.xml`, `https://www.tealhq.com/pricing`, and
  `https://www.tealhq.com/features` also returned HTTP 403 or were not
  confirmed as canonical page bodies.
- Direct `web.archive.org/web/<timestamp>/<url>` snapshot content fetches
  failed at the tool layer.
- `web.archive.org/__wb/sparkline` and CDX-style full snapshot enumeration were
  not attempted because the relevant host path was already hard-blocked in this
  tool environment.
- `archive.org/wayback/available` worked but returns only a closest snapshot
  for a queried timestamp, not full historical enumeration.
- WebSearch summaries are non-verbatim and internally conflict on weekly Teal+
  price.
- No live HTML, archive HTML, screenshot, source language, visible layout,
  source table, source modal, app-state view, or Mechanical Source Projection
  packet was preserved.

## Categorical Handoff Or Visible Stop

- Handoff state: `visible_blocker` with `re-capture_posture`.
- Reason: The capture should not proceed as clean `categorical_handoff_to_ECR`
  because the decision-frame content was not captured as inspectable source
  material. The artifact can hand off the failure posture, URL inventory,
  archive availability, access limits, and non-verbatim pointers, but not Teal's
  pricing, feature posture, or change history as source-backed evidence.
- Re-capture posture: re-capture Teal with an authorized path that can retrieve
  live Teal page bodies, source language, visible structure, and archive
  snapshot content before using this slice as a fully inspectable AI-generic
  resume-tool source.

## Pressure-Test Findings

- S2-1 - Under a full host block, source/company identity can be visible while
  actor/audience specificity remains only partial because page content is not
  inspectable.
- S2-2 - The original workfile independently pressured the missing-state area
  that was later absorbed by the amended contract. In this formal artifact,
  current vocabulary handles the pattern as `access_failed`, `cannot_assess`,
  and `assessed_not_met` rather than hidden proposal language.
- S2-3 - The full-block case is more severe than Slot 1's paraphrase case:
  Slot 1 preserved some pricing facts, while Slot 2 preserved no source-backed
  decision content.
- S2-4 - The operator's instinct to ask whether rumored search-summary pricing
  could be used was correctly held out of Capture. Whether non-verbatim pointers
  are usable is downstream Judgment/Signal-Use work, not a Capture conclusion.
- S2-5 - Categorical handoff readiness is assessable even when source content
  is not captured. Here it is `assessed_not_met`: the limitation is visible and
  the artifact is useful as failure evidence, but it is not enough for clean
  handoff on the Teal pricing/features/history decision frame.
- S2-6 - Both checker passes were useful pressure-test evidence in the original
  workfile. Pass 1 returned `capture_closure_blocker`; Pass 2 returned
  `vocabulary_consistent` for the then-labeled proposal language. Under the
  current contract, the same surface should be read as formalized current
  vocabulary plus visible limitations, not as unresolved checker-token drift.

## Fetcher Requirements Surfaced

These are requirements surfaced by the capture, not build authorization.

1. Anti-block / 403-handling source access for in-bound public Teal pages.
2. Archive snapshot content retrieval for `web.archive.org` snapshot bodies.
3. Verbatim and source-structure preservation for retrieved Teal pages.
4. Multimodal or screenshot capture if pricing, feature packaging, app state,
   or page layout becomes material.

## LLM Capture-Visibility Checker Output

- Output: `capture_closure_blocker` - pass 1, GPT-5.5, 2026-05-29.
- Original specifics: Obligations #6, #12, and #16 were flagged in the root
  workfile because it used then-proposal states for a full-block condition, and
  the handoff was `visible_blocker`.
- Current disposition: this formal artifact normalizes the surface to current
  contract vocabulary. The blocker still stands as a capture limitation:
  decision-frame content was not captured and re-capture is needed before clean
  handoff.
- Remediation: no source re-capture was performed in this formalization.

## Vocabulary-Consistency Check Output

- Output: `vocabulary_consistent` - pass 2, GPT-5.5, 2026-05-29.
- Original specifics: the checker treated out-of-set root-workfile values as
  labeled proposal language rather than hidden vocabulary divergence.
- Current disposition: the formal artifact no longer uses the old proposal
  language as operative obligation states. It uses current contract vocabulary
  and preserves the historical pressure as a finding.

## Non-Claims

- Not validation, readiness, pressure-test discharge, buyer proof, or commercial
  readiness.
- Not a contract amendment or doctrine change.
- Not a raw HTML packet, screenshot packet, archive packet, browser recording,
  or Mechanical Source Projection packet.
- Not ECR design, Cleaning implementation, Judgment design, runtime
  authorization, source-access method authorization, tooling authorization,
  scraper authorization, browser automation authorization, API authorization, or
  schema authorization.
- Not a claim that WebSearch snippets are source language or verified Teal
  claims.

## Recommended Next Step

Use this artifact as the formal Slot 2 capture-session surface for later
all-slot pressure-test synthesis. Treat it as failure-visible
`visible_blocker` evidence, not as a usable Teal pricing/features/history source
until an authorized re-capture preserves inspectable source content.
