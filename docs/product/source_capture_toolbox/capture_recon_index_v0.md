```yaml
retrieval_header_version: 1
artifact_role: Capture recon consolidation index (non-authorizing)
scope: >
  Consolidates the scattered per-source capture RECON / INVESTIGATION findings across
  the toolbox, data-capture-spine pressure tests, research receipts, and worktree-resident
  lane findings into one index. Records, per source probed, what was found capturable, at
  which runner rung, where the signal actually lives, and any corrected false-diagnosis.
  This index is the evidence base the capture-investigation doctrine + runbook distil from.
use_when:
  - Drafting the source-agnostic capture-investigation doctrine and per-archetype recipe cards.
  - Checking whether a source archetype already has a worked recon before re-probing it.
  - Locating the highest-signal real probe receipts (captured bytes / live-verified verdicts).
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2.md
stale_if:
  - A new source recon lands (this index is append-only until the doctrine supersedes it as the home).
  - The worktree-resident findings (Sephora/Bazaarvoice reviews; Ulta Apollo embedded-JSON) merge to main.
  - The capture-investigation doctrine is authored and adopts the cross-cutting patterns below as its spine.
```

# Capture Recon Consolidation Index (v0)

## What this is — and is not

This is a **non-authorizing index** of the capture RECON / INVESTIGATION findings already
in the repo — the docs that probed a real source to learn **whether and how it can be
captured**. It exists so the capture-investigation doctrine and its per-archetype recipe
cards are **distilled from real probe evidence, not invented**.

It is **not** a build spec, not validation, not an acceptance claim, and not legal advice.
Verdicts below are **as reported by each source doc**, not re-observed here. It governs
nothing; it feeds the doctrine.

## Cross-cutting patterns — the doctrine seed (highest-value section)

These six patterns recur across independent probes. They are the spine the investigation
doctrine should encode.

1. **"Blocked" is a hypothesis, not a verdict — and it is the dominant false-diagnosis.**
   A 403 / empty body / "anti-bot gated" read was *wrong or imprecise* in multiple
   independent cases: Daimler PDFs (direct-HTTP 403 **and** headless 403, yet **visible
   Chrome + the PDF-viewer download button succeeded**); Sephora reviews (worktree:
   "anti-bot gated" → actually a **scroll-overshoot** that never fired the lazy-load
   observer); Teal/WSO (403 first recorded as "content unavailable," later re-diagnosed as
   an anti-bot gate). **Escalate the interaction (real browser context → user-initiated
   action → progressive scroll → proxy/geo) and re-probe before recording NO-GO.** A false
   "blocked" abandons a capturable source.
2. **Locate the signal substrate first; pick the tool second.** Reddit = raw JSON;
   reviews = a first-party-rendered vendor API (Bazaarvoice); SPA state =
   `__APOLLO_STATE__` / `__NEXT_DATA__` (Ulta, worktree); PDF body = a download button.
   The cheapest working rung is a function of **where the signal lives**, so step 1 of
   diagnosis is finding the substrate, not choosing a runner.
3. **Verbatim-vs-paraphrase is a separate axis from reachable-vs-blocked.** WebFetch
   *reaches* M&I/BIWS but returns **paraphrase**, losing layout/packaging fidelity. A
   recipe must record whether a rung preserves source **bytes**, independent of whether it
   gets through.
4. **The entitlement/legal gate is orthogonal to the technical gate and comes first.**
   LinkedIn policy forbids automated capture **regardless** of technical reachability;
   Reddit's API has a commercial-use gate. A NO-GO can be *legal*, not technical. Never
   bypass an unentitled gate even when it is technically trivial.
5. **NO-GO and PARTIAL are first-class, honest outcomes.** Daimler pre-cutoff archive
   returned **no memento exists** → an honest NO-GO; archive *availability* ≠ body
   *retrieval* → PARTIAL. Concluding "not cleanly capturable within boundary" is a
   *successful* diagnosis, not a failure.
6. **The runner ladder is empirically real and cheapest-first.** archive.org →
   direct-HTTP → **(visible) browser** → cloakbrowser+proxy. "Visible browser + a
   user-initiated action" is a genuine escalation rung that defeats headless-detection
   where both direct-HTTP and headless fail (Daimler).

## Index — by archetype (verdicts as reported by each source)

### Reviews
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Sephora PDP reviews **(worktree, pending-merge)** | `orca-cloak-scroll-wt/orca-harness/docs/source_capture_review_rendering_findings_v0.md` | Bazaarvoice API, first-party-rendered into DOM, lazy-load on **progressive scroll**; bot wall **passed** legitimately | **GO via incremental scroll** (corrects a prior false "anti-bot-gated" claim) | HIGH ⭐ |
| ClickUp on Trustpilot / G2 | `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` | Live public review text; rating+text+date coupling, reviewer-status labels | Captured; review-surface satellite guidance formalized | MODERATE |

### Forums / threads
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Reddit r/financialcareers (10 threads, 563 rows) | `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_reddit_capture_session_v0.md` | Raw JSON → Mechanical Source Projection; row/parent_id/depth; `more_placeholder` visibility | `categorical_handoff_to_ECR` (limited) | HIGH |
| Reddit ECR-consumption probe (old.reddit r/b2bmarketing) | `docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md` | `run_source_capture_http_packet`, HTTP 200 ~104 KB, 14 comments; `cutoff_posture` param | GO / residual by-design (missing Decision Frame, not a capture defect) | HIGH |
| Wall Street Oasis (7 pages) | `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot3_wso_capture_session_v0.md` | Browser visible-page + Wayback availability; email-unlock prompts visible, **not used** | `categorical_handoff_to_ECR` (partial; no full comment graph) | HIGH |
| Reddit API-pricing threads (r/reddit, r/Devvit, r/apolloapp) | `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` | Public pages (live fetch blocked → recorded as source-access failure, not boundary); related-chain + package segmentation | Related-chain/bundle preserved; discharge specificity needs tightening | HIGH |
| Reddit offline packet consolidation (parser spec) | `docs/product/source_capture_toolbox/reddit_packet_consolidation_runner_structural_spec_v0.md` | Packet reader; flat comment list + parent_id; closed comment-posture vocab | Packet-first boundary locked; raw packet > parsed text | HIGH (spec) |
| Slot-3 source-quality closeout (Reddit b1/b2 + WSO) | `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md` | Raw JSON + visible HTML (~200 KB cap) | `mini_god_tier_with_visible_limitations` (bounded GO) | MODERATE |

### Pricing
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| OpenAI price payload **(worktree/lane, rung-1.5)** | `orca-rung15-wt` (branch `capture-rung15-openai-payload`, unmerged) | Embedded price payload + token-list certification | Committed-not-merged; narrowed "internally-consistent as-served" claim | HIGH ⭐ (lane) |
| M&I / BIWS | `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md` | WebFetch → **paraphrase, not verbatim**; archive metadata known, bodies failed | `visible_stop` + re-capture posture (fidelity loss) | HIGH |
| Teal (tealhq.com) | `docs/product/data_capture_spine/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md` | **HTTP 403 full-host block** → WebSearch fallback (non-verbatim) | `visible_blocker` + re-capture posture (anti-block/auth needed) | HIGH |

### Docs / changelog
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Kubernetes v1.32 deprecation guide / release blog | `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` | Live docs + GitHub raw + static snapshot; version-page + last-modified coupling | Passed; docs-changelog satellite guidance | MODERATE |

### Archive / history
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Daimler DSU PDFs (pre-cutoff identity) | `docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md` | Direct-HTTP **403**; archive.org CDX = **no pre-cutoff memento** | **NO-GO** on pre-cutoff version identity (honest) | HIGH ⭐ |
| Unity Runtime Fee (announce + recapture) | `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` | Live + archive.org availability (bodies not fetched); recapture-delta | Archive availability ≠ body; recapture timing posture | MODERATE |

### Docs / PDF body (anti-bot escalation)
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Daimler DSU-001/002/003 PDFs (body capture) | `docs/research/daimler_advisory_001_browser_source_body_capture_dsu_001_003_receipt_v0.md` | direct-HTTP 403 + headless 403 → **visible Chrome + download button = captured bytes** (2.6/1.3/4.1 MB, `%PDF`, SHA256) | **GO via visible browser + user action** (corrected anti-bot diagnosis) | HIGH ⭐ |
| Daimler S1–S7 source acquisition | `docs/research/judgment-spine/harness/v0_14/fixtures/.../source_acquisition_receipt_v0.md` | Canonical issuer 403 → public-mirror + owner-supplied PDF fallback (SHA256 verified) | MIXED GO/NO-GO (canonical-domain bytes residual) | HIGH |

### SPA embedded-state
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| Ulta product / Apollo cache **(worktree/lane, DP-002)** | demand-projection lane (`orca-demand-projection-wt`, unmerged) | `__APOLLO_STATE__` cache node; needle from field+value `"productId":"<id>"` | Provenance fix (a) applied in-lane; keep-gate pending | HIGH ⭐ (lane) |

### Browser-automation runner
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| CloakBrowser local setup | `docs/product/source_capture_toolbox/cloakbrowser_local_setup_probe_receipt_v0.md` | Local binary (Chromium 146) + API introspection; smoke test | `READY_FOR_ADAPTER_CONTRACT_SCOPING` | HIGH |
| CloakBrowser packet-runner architecture | `docs/product/source_capture_toolbox/cloakbrowser_packet_runner_architecture_v0.md` | API shape from public docs + introspection; no-secret/anonymous seam | `TARGET_RECOMMENDED` (adapter-contract-first) | HIGH (arch) |

### Social networks (policy boundary; technical probe largely absent)
| Source probed | Path | Rung / where signal lives | Reported verdict | Signal |
| --- | --- | --- | --- | --- |
| LinkedIn official policy | `docs/product/source_capture_toolbox/linkedin_reddit_source_capture_armory_concurrent_structure_architecture_v0.md` | Policy docs (2026-06-05): scraping/automation forbidden absent authorization | **Boundary-only** — official/API/manual/entitled routes only; no scraping | MODERATE-HIGH |

## Coverage map

- **Well-covered:** forums/threads (Reddit ×4, WSO), pricing (M&I, Teal, OpenAI-lane), archive/history (Daimler, Unity), docs-PDF body (Daimler — the strongest anti-bot escalation case), browser runner (CloakBrowser), reviews (ClickUp + Sephora-pending).
- **Thin / single-fixture:** docs-changelog (Kubernetes only), reviews (one merged fixture; the strong one is worktree-pending), SPA embedded-state (Ulta worktree-pending only).
- **ABSENT — and directly relevant to the stated multi-source product direction:**
  **TikTok and Instagram have no technical recon at all.** The only social probe is the
  LinkedIn *policy* boundary. Any TikTok/IG recipe card is **speculative** until probed,
  and both carry the heaviest ToS/auth-wall/anti-bot posture (entitlement gate, Pattern 4,
  applies before any technical attempt). No media/video capture recipe exists either.

## Pending-merge / external (not on main; include before the doctrine finalizes)

- **Sephora/Bazaarvoice reviews finding** — worktree `orca-cloak-scroll-wt`, in squash `0faf262`, force-push pending. The single best **reviews** diagnosis (and the canonical "blocked was wrong" lesson).
- **Ulta Apollo embedded-JSON (DP-002)** — demand-projection lane worktree, unmerged. The single best **SPA-embedded-state** diagnosis.
- **OpenAI price payload (rung-1.5)** — `orca-rung15-wt`, unmerged. Best **pricing-embedded** diagnosis.
- **Operator-supplied / gitignored scratch** (evidence, not tracked): `docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/...`; `orca-harness/_test_runs/{cloakbrowser_api_probe,source_quality_slot3_*}/`.

## Non-claims

Not an authorization, not a build spec, not validation/readiness/acceptance, not legal
advice. Verdicts are as reported by each source doc. The absence of a TikTok/IG probe is a
**sweep result** (no such recon surfaced across the main-tree docs), not a proof that none
could exist. Worktree-resident findings are **claimed by their lanes** and unverified here
until merged.
