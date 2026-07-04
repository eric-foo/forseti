# Data Capture Spine Pressure-Test Slot 1 M&I/BIWS Capture Session v0

```yaml
retrieval_header_version: 1
artifact_role: Data Capture pressure-test capture-session artifact
scope: Records the formalized Slot 1 Mergers & Inquisitions / Breaking Into Wall Street capture session for finance-specialized substitute pricing, bundle, resume-help, and archive-history posture.
use_when:
  - Checking Slot 1 Data Capture evidence before all-slot pressure-test synthesis.
  - Reviewing M&I/BIWS pricing, bundle, resume-help, redirect, archive, and paraphrase limitations.
  - Preserving Slot 1 pressure-test findings without hardening the obligation contract or designing source-access tooling.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_execution_authorization_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - slot2_teal_CAPTURE_operator_workfile.md # nonresolving: operator workfile, never committed
stale_if:
  - A later owner decision rejects or supersedes the Slot 1 source boundary.
  - A later M&I/BIWS verbatim, raw HTML, screenshot, or archive-content recapture supersedes this paraphrase-limited capture.
  - The accepted intake-surface target, commissioning plan, or obligation contract is materially amended before all-slot synthesis.
  - M&I/BIWS pricing, redirects, bundle structure, or resume-help posture changes materially before downstream use.
```

## Status

Status: `CAPTURE_SESSION_SLOT1_MI_BIWS_FORMALIZED_FROM_OPERATOR_WORKFILE_V0`.

This artifact formalizes the root operator workfile
`slot1_mi_CAPTURE_operator_workfile.md` into a durable Data Capture
pressure-test capture-session artifact. It does not re-capture M&I/BIWS, does
not certify verbatim source language, does not fetch archive content, and does
not authorize source-access tooling.

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Slot 1 M&I/BIWS pressure-test formalization pack
  edit_permission: docs-write for one Slot 1 capture-session Markdown artifact
  target_scope: docs/product/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - slot1_mi_CAPTURE_operator_workfile.md
    - docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot1_mi_subagent_output.md
```

## Source Basis

| Source | SHA256 | Role |
| --- | --- | --- |
| `slot1_mi_CAPTURE_operator_workfile.md` | `1FC6446EB6E1F45E8E16526F90B15870374DB215743F03E744C80E5E560A27CF` | Operator-filled Slot 1 capture workfile. |
| `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot1_mi_subagent_output.md` | `D393968A56174B2C2DF73E21B3CAF2AA8BCA755DA115C17BFDB2E41996F7FF4F` | Agent-assisted enumerate/fetch/archive raw material used by the operator. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5` | Current amended Data Capture obligation contract used for vocabulary normalization. |
| `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` | `3D9AC208A8AF68160A43F3EB3512082BF0F9B10D3840331FE82F544E307820EB` | Slot 1 commissioning shape. |
| `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md` | `BCA50C80A7EAA889DC0B01377FFB80635BAC6DDC30F3A4FA654B42CC319CACA3` | First-batch execution authorization. |

## Formalization Note

The root workfile predates the amended obligation-contract vocabulary. This
formalization updates surface labels only:

- The older #6 label in the root workfile is normalized to `Raw Observable
  Fidelity`.
- The older #16 label in the root workfile is normalized to `Categorical
  Handoff Readiness`.
- Tool/archive access failures are not rewritten as boundary `blocked`.
- The old `indeterminate` / `cannot_assess` finding is preserved as a
  pressure-test observation; the actual Slot 1 #12 state remains `partial`
  because some related context was preserved while the fairness ceiling could
  not be assessed against verbatim source.
- The old #16 "no ECR receiver exists" pressure is treated under the current
  contract as Capture-owned handoff readiness, not actual ECR receipt.

No new obligation-state judgment is introduced here beyond this vocabulary
normalization.

## Decision Frame

- Decision question: What does Mergers & Inquisitions, and its course store
  Breaking Into Wall Street, charge and how does it bundle or structure
  finance-career content and resume help as of Q2 2026, so jb can set its own
  price and bundle structure for a finance resume product?
- Owner or owner-context: jb owner; pre-launch pricing and positioning
  decision.
- Consequence: Sets jb's price range, bundle structure, and competitive
  position on the finance-specialized substitute flank.
- Allowed decision verbs: `categorical_handoff_to_ECR`, `visible_stop`,
  `visible_blocker`, `rerun`, `re-capture_posture`, or later owner-authorized
  pressure-test patch planning.
- Cutoff posture: Live-state cutoff is 2026-05-28; approximately 24-month
  prior-window comparison was desired but archive content was not captured.
- Downstream-use intent: Data Capture evidence for jb pricing/positioning
  only. This artifact is not buyer-facing and does not perform Judgment,
  Cleaning, ECR schema design, or product synthesis.

## Source Boundary

- Primary source surface: `mergersandinquisitions.com` public content, blog,
  coaching, resume, sitemap, and pricing-adjacent pages.
- Extended source surface: `breakingintowallstreet.com` pages linked by M&I
  and live-redirect targets for M&I product/resume/coaching pages.
- Archive surface: `archive.org/wayback/available` returned snapshot dates;
  `web.archive.org` snapshot content fetches failed at the tool layer.
- Boundary compliance: The session used public/discoverable marketing and
  course pages only. No login, account-created access, paid/coworker
  entitlement, private area, deceptive access, obvious spillover, or
  undisclosable method was used.
- Source-boundary note: M&I and BIWS are treated together because the M&I home
  page, navigation, course cards, and live redirects point to BIWS as the
  product/pricing surface. The operator confirmed BIWS as in boundary.

## Capture Mode

- Initial mode: human-led operator capture with agent-assisted enumeration,
  WebFetch page rendering, and archive availability checks.
- Material mode changes: none recorded.
- Material mode limitation: WebFetch returned reorganized/paraphrased page
  renderings rather than character-perfect source text. Dollar amounts, product
  names, bundle names, savings claims, and claim numbers were preserved as
  captured facts, but exact source wording, layout, emphasis, table placement,
  nesting, and other visible packaging cues were not certified.

## Per-Obligation Discharge States

| # | Obligation | State | Reason (required for non-`met`) |
| --- | --- | --- | --- |
| 1 | Commissioning Gate | met | |
| 2 | Boundary Compliance | met | |
| 3 | Capture-Event Provenance | met | |
| 4 | Capture Mode Disclosure | met | |
| 5 | Mode-Change Rule | met | |
| 6 | Raw Observable Fidelity | partial | WebFetch preserved pricing facts, product names, bundle names, savings claims, and claim numbers as paraphrased/reorganized renderings. Exact source wording, visible structure, layout, emphasis, table placement, nesting, proximity, and packaging cues were not preserved faithfully. |
| 7 | Source Identity And Actor Context | met | |
| 8 | Decomposed Timing | partial | Sitemap lastmod timestamps, archive snapshot dates, capture date 2026-05-28, and cutoff posture were visible. Original publication timing was not separated from last-edit timing, and archive content that might establish historical state access-failed. |
| 9 | Cutoff Posture | met | |
| 10 | Archive / Historical Posture | partial | Archive snapshot existence and dates were captured through `archive.org/wayback/available`, but `web.archive.org` snapshot content access failed. Historical pricing and product content were not captured. |
| 11 | Source Visibility And Access Limits | met | |
| 12 | Related Context Preservation | partial | Course descriptions, bundle framing, level groupings, savings claims, money-back terms, and resume/coaching context were captured, but the fairness ceiling cannot be assessed against verbatim source because the capture is paraphrase-limited. |
| 13 | Bundled-Offer Structure Observables | partial | Bundle membership, pricing, savings framing, and tier structure were captured. Visible packaging cues such as layout, emphasis, table placement, nesting, and proximity were not preserved by text-only WebFetch. |
| 14 | Capture Failure And Blocker Visibility | met | |
| 15 | Re-Capture Semantics | not_applicable | First capture; no prior same-slice capture was supplied. |
| 16 | Categorical Handoff Readiness | partial | Current pricing and bundle facts are usable and limitations are visible, but handoff is below `categorical_handoff_to_ECR` because source language, visible structure, packaging cues, and archive content are not faithfully preserved. |

Allowed states used: `met`, `partial`, `not_applicable`.

## Per-Slice Posture

| Slice | Archive/history posture | Source visibility/access posture | Related context posture | Re-capture relationship |
| --- | --- | --- | --- | --- |
| M&I live pages | Snapshot dates available for selected URLs; archive content not retrieved. | Public pages accessible through WebFetch, but rendered as paraphrase/reorganized text. | Home page, navigation, resume/career content, course cards, and sitemap relationships preserved at fact level. | Future recapture should preserve verbatim text and screenshots if marketing language or page structure matters. |
| BIWS course/store pages | Snapshot dates available for selected URLs; archive content not retrieved. | Public BIWS pages accessible through WebFetch, but rendered as paraphrase/reorganized text. | Course, bundle, price, guarantee, support, and savings facts preserved at fact level. | Future recapture should preserve raw HTML/screenshots and archive versions if bundle presentation or historical price drift matters. |
| M&I redirected pages | Snapshot dates available for some original M&I locators; archive content not retrieved. | `/investment-banking-coaching/`, `/investment-banking-resume-review/`, and `/services/` redirect to `https://breakingintowallstreet.com/resume-editing-pitch-perfection/`. | Original locator, current target, and pricing-context shift are visible. | Future recapture should preserve redirect chain, current target content, and archive content for old M&I pages. |
| Archive snapshots | Snapshot existence and timestamps were captured via `archive.org/wayback/available`. | Direct `web.archive.org/web/<timestamp>/<url>` content fetches access-failed at the tool layer. | Historical pricing/product content is not inspectable in this capture. | Recapture requires a browser, curl, or other separately authorized archive-capable path. |

## Raw Observable Pointers

### Preserved Source Pointers

- Root and sitemap surfaces:
  - `https://mergersandinquisitions.com/`
  - `https://mergersandinquisitions.com/sitemap.xml`
  - `https://mergersandinquisitions.com/sitemap_index.xml`
  - `https://mergersandinquisitions.com/page-sitemap.xml`
  - `https://mergersandinquisitions.com/post-sitemap.xml`
- M&I pricing/resume/coaching source locators:
  - `https://mergersandinquisitions.com/investment-banking-coaching/`
  - `https://mergersandinquisitions.com/investment-banking-resume-review/`
  - `https://mergersandinquisitions.com/services/`
  - `https://mergersandinquisitions.com/coaching-bronze/`
  - `https://mergersandinquisitions.com/coaching-silver/`
  - `https://mergersandinquisitions.com/coaching-gold/`
  - `https://mergersandinquisitions.com/breaking-into-wall-street-biws/`
- BIWS product/pricing locators:
  - `https://breakingintowallstreet.com/breaking-into-wall-street-courses/`
  - `https://breakingintowallstreet.com/platinum/`
  - `https://breakingintowallstreet.com/biws-premium/`
  - `https://breakingintowallstreet.com/excel-and-financial-modeling/`
  - `https://breakingintowallstreet.com/networking-toolkit/`
  - `https://breakingintowallstreet.com/investment-banking-interview-guide/`
  - `https://breakingintowallstreet.com/core-financial-modeling/`
  - `https://breakingintowallstreet.com/resume-editing-pitch-perfection/`

### Captured Pricing And Bundle Facts

These facts are preserved from the subagent output's WebFetch renderings. They
are useful pricing and bundle anchors, but they are not certified verbatim
source-language preservation.

- M&I/BIWS resume and coaching:
  - M&I `/investment-banking-coaching/`, `/investment-banking-resume-review/`,
    and `/services/` live-redirect to BIWS resume editing / pitch perfection.
  - BIWS resume service is described as available to course customers who have
    purchased programs valued at `$497` or more.
  - Resume Editing price captured as `$300`.
  - Resume Editing + Pitch Perfection price captured as `$500`.
  - M&I Bronze Coaching price captured as `$497`.
  - M&I Silver Coaching price captured as `$997`.
  - M&I Gold Coaching price captured as `$1,997`.
- BIWS course and bundle posture:
  - BIWS Platinum captured as `$497 / Year` or `$1,497` one-time fee.
  - BIWS Platinum captured as all 15 individual courses, `300+` hours of
    training, total individual value `$3,305`, and claimed savings `$2,808`.
  - BIWS Premium bundle captured as `$497`, saving `$194`, described as a
    `28%` discount / "Most Popular" in the subagent output.
  - Excel & Financial Modeling bundle captured as `$397`, saving `$97`.
  - Networking Toolkit captured as `$147` or four monthly payments of `$37`.
  - IB Interview Guide captured as `$197` or four monthly payments of `$49`;
    related claim captured as `578+` pages and 17 Excel-based case studies.
  - Core Financial Modeling captured as `$297`.
  - Excel & VBA captured as `$197`.
  - PowerPoint Pro captured as `$197`.
  - Advanced M&A Modeling and Biotech Valuation captured as `$97` each.
  - Several modeling courses captured in the `$197` to `$497` range.
- M&I positioning and adjacent claims:
  - M&I home page captured `307,012+` monthly readers.
  - M&I lead magnet captured Banker Blueprint as 57 pages and `115,341+`
    industry peers.
  - M&I site captured as `641` expert articles.
  - BIWS social-proof claim captured as `56,763+` students.

### Archive Snapshot Availability

Archive availability was partly captured, but snapshot content was not.

- M&I home page: 2025-11-08 snapshot returned for one query; 2024-06-01 and
  2025-06-01 queries returned no snapshot.
- M&I `investment-banking-resume-review/`: snapshots returned around
  2024-05-26 and 2025-06-20.
- M&I `investment-banking-coaching/`: snapshots returned around 2024-05-26 and
  2025-12-09.
- M&I coaching tier pages: snapshots returned for Bronze, Silver, and Gold
  pages.
- BIWS Platinum: snapshots returned around 2024-04-24 and 2025-10-14.
- BIWS Premium: snapshots returned around 2024-04-24 and 2025-12-07.
- Several BIWS course or resume-editing archive probes returned empty
  `archived_snapshots` for tested timestamps.

## Failures / Blockers / Limitations

- WebFetch returned paraphrased/reorganized page renderings rather than
  character-perfect source text.
- `web.archive.org` snapshot content fetches failed at the tool layer for all
  attempted direct snapshot content URLs.
- Archive availability queries showed some snapshots exist, but historical
  pricing/product content is not captured.
- M&I resume/coaching/service URLs redirect to a BIWS resume-editing page,
  while older M&I coaching tier pages still expose Bronze/Silver/Gold pricing.
- The relationship between BIWS `$300` / `$500` resume editing and M&I
  `$497` / `$997` / `$1,997` coaching tiers is visible but not resolved.
- Text-only capture does not preserve visible packaging cues, layout, table
  placement, proximity, emphasis, or nesting.
- The capture does not include raw HTML, screenshots, a browser recording, or
  a Mechanical Source Projection packet.

## Categorical Handoff Or Visible Stop

- Handoff state: `visible_stop` with `re-capture_posture`.
- Reason: Current pricing, bundle, redirect, and resume-help facts are visible
  enough to inspect as pressure-test evidence, but the capture should not be
  treated as clean `categorical_handoff_to_ECR`. Source-language fidelity,
  visible-structure fidelity, packaging cues, and archive content are not
  faithfully preserved.
- Re-capture posture: recapture M&I/BIWS with verbatim/source-structure
  preservation, screenshots or equivalent layout capture, and archive-content
  retrieval before using this slice as a fully inspectable pricing and
  bundle-presentation source.

## Pressure-Test Findings

- F-A - Fact preservation and source-language preservation diverged. Prices,
  product names, and bundle facts survived the paraphrase capture, but the
  source's own marketing language did not.
- F-B - Paraphrase cannot be the system of record when source wording,
  structure, and marketing posture carry signal.
- F-C - A related-context fairness ceiling can become unable to be assessed
  without faithful source capture. The later contract's `cannot_assess`
  vocabulary is relevant to this pressure.
- F-D - Tool-layer or archive access failure must not be mislabeled as
  boundary `blocked`.
- F-E - Handoff readiness is frame-weighted: historical archive loss matters,
  but in this capture the paraphrase and packaging-fidelity losses were more
  load-bearing for the decision frame.
- F-F - The older workfile wording stressed that actual ECR handoff did not
  exist in phase. Under the current contract, the relevant issue is Capture's
  categorical handoff readiness, not actual ECR receipt.
- F-G - Operator usability and role boundary were stressed: the agent assembled
  mechanics, but the operator made state calls; when the operator tried to
  delegate the #13 hard call, the agent held the operator-led line.
- F-H - The checker token `capture_closure_blocker` was easy to misread as
  boundary `blocked` or a mandatory rerun trigger. Current checker glossary
  should keep that distinction visible.

## Fetcher Requirements Surfaced

These are requirements surfaced by the capture, not build authorization.

1. Verbatim and source-structure preservation: no paraphrase as the record.
2. Archive snapshot content retrieval: reach `web.archive.org` snapshot content
   where snapshots are known to exist.
3. Multimodal or screenshot capture: preserve layout, visible packaging,
   emphasis, tables, nesting, and proximity where those carry signal.

## LLM Capture-Visibility Checker Output

- Output: `capture_closure_blocker` - pass 1, GPT-5.5, 2026-05-28.
- Specifics: Obligations #6, #12, #13, and #16; slices M&I live, BIWS, and
  redirected M&I-to-BIWS pages. Paraphrase was the preserved record while source
  language and visible packaging cues carried frame signal. Raw source
  language, visible structure, and modality were not preserved where required.
- Positive checks: all 16 obligation states were declared; non-`met` reasons
  were present; archive/history rollup was uniform; source/access posture was
  captured per slice; no ECR fields, IDs, schemas, storage, or runtime were
  defined.
- Remediation: none performed in this formalization. The blocker stands as
  pressure-test evidence. Re-capture requires verbatim, structure, multimodal,
  and archive-capable access not authorized here.

## Vocabulary-Consistency Check Output

- Output: `vocabulary_divergence` - pass 2, GPT-5.5, 2026-05-28.
- Specifics: The checker flagged old #16 prose that used the look-alike word
  "rejected" outside the controlled vocabulary. The declared values were valid:
  obligation #16 `partial`, handoff `visible_stop`.
- Disposition in this formal artifact: the look-alike term is not used as an
  operative state. The artifact uses current contract labels and preserves
  `cannot_assess` / handoff-readiness split as historical pressure-test
  findings rather than hidden vocabulary drift.

## Non-Claims

- Not validation, readiness, pressure-test discharge, buyer proof, or commercial
  readiness.
- Not a contract amendment or doctrine change.
- Not a raw HTML packet, screenshot packet, archive packet, browser recording,
  or Mechanical Source Projection packet.
- Not ECR design, Cleaning implementation, Judgment design, runtime
  authorization, source-access method authorization, tooling authorization, or
  schema authorization.
- Not a claim that captured WebFetch snippets are character-perfect source
  language.

## Recommended Next Step

Use this artifact as the formal Slot 1 capture-session surface for later
all-slot pressure-test synthesis. Before synthesis, formalize Slot 2 against
the current nine-state obligation contract so Slot 1, Slot 2, and Slot 3 are
comparable without replaying old six-state vocabulary drift.
