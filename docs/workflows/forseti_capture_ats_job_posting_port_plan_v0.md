# ATS Job-Posting Capture Port — Phase 0 Plan (return for owner adjudication)

```yaml
retrieval_header_version: 1
artifact_role: Phase 0 implementation plan returned for owner adjudication (non-authoritative until adjudicated)
scope: >
  Plan-first design for porting ATS job-posting capture mechanics (jb
  curated-jobs-v2, reference only) into forseti-harness/source_capture as a new
  commission-bounded source family (`ats_job_posting`) for capture-only,
  point-in-time snapshots of public ATS boards. Covers adapter designs for
  Greenhouse, Lever, Workday, Ashby; the jb mechanics port/no-port review; the
  registry seeding decision framed for one owner ruling; storage/projection,
  run, and validation contracts; and effort order. Capture only — no ranking,
  classification, relevance filtering, or pain inference.
use_when:
  - Adjudicating this plan before Phase 1 implementation is authorized.
  - Implementing Phase 1 after adjudication (implement exactly the adjudicated plan).
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_capture_ats_job_posting_port_handoff_v0.md
  - forseti-harness/docs/adapter_author_contract.md
  - forseti-harness/source_capture/adapters/direct_http.py
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
stale_if:
  - The owner adjudicates this plan (accept / amend / reject); the plan is then consumed or revised.
  - A ruling in the source handoff is reversed.
```

## What this is

This is the Phase 0 deliverable commissioned by
[`forseti_capture_ats_job_posting_port_handoff_v0.md`](forseti_capture_ats_job_posting_port_handoff_v0.md).
It is a **plan for owner adjudication**. No adapter, registry, or projection
code is written. Phase 1 (implementation) is authorized only after the owner
adjudicates this plan; any discovered deviation returns as a plan amendment, not
a silent change.

**Provenance (not authority).** jb (`C:\Users\vmon7\Desktop\projects\jb`) is
read-only reference. Every jb-derived claim below was re-verified by direct read
of the jb sources (confirm-don't-trust); corrections to the handoff's stated
claims are called out explicitly. jb is never Forseti authority; mechanics port
as new Python in forseti-harness. The one live action taken in Phase 0 is the
authorized Ashby access-posture scan (ruling 3), reported below.

**Scope guard (ruling 2).** The capture layer preserves postings verbatim and
projects them mechanically. It never ranks, filters by relevance, classifies
roles, gates by a curated relevance judgment, or infers pains. The
residue-to-pain reading is a later downstream lens over `derived/` rows and is
out of scope here entirely.

**No new spine (drift guard).** This is a source family *inside* the existing
Capture spine, not a new spine.

> Note on a stale handoff pointer: the handoff's `open_next` names
> `forseti_gtm_silent_pain_taxonomy_v0.md`, which does not exist (the GTM tree
> now holds `forseti_beauty_us_problem_discovery_to_wedge_contract_v0.md` and
> `forseti_demand_signal_gtm_design_v0.md`). It is not load-bearing for this
> capture-only plan (it is the downstream pain lens, out of scope per ruling 2),
> so it was not chased. Flagged for the owner.

---

## 0. Decisions — adjudicated (owner, 2026-07-18)

| # | Decision | Ruling |
| - | -------- | ------ |
| D1 | **Registry seeding** (ruling 5): manual per-company entries vs agent-assisted careers-page sniffing. | **Manual (Option A) for v1.** Agent-assisted sniffing deferred. See §4. |
| D2 | Description depth in `derived/`: full text vs truncation. | **Full text.** See §5. |
| D3 | Geographic scoping: full-board fetch + verbatim location/country extraction vs vendor-side country facet at fetch. | **Full-board fetch + verbatim extraction**; country facet only as an explicit commission-declared bound. See §3 (Workday) and §6. |
| D4 | Snapshot granularity: one packet per board snapshot (slices = postings) vs one packet per posting. | **One packet per board snapshot.** See §5. |
| D5 | **Storage sink**: the Forseti lake (`raw/` + `derived/` under `FORSETI_DATA_ROOT`) vs a Google Sheet (jb's CW2 sink). | **The Forseti lake.** Google Sheets rejected — it is a jb runtime choice (reference-only, not Forseti authority), it breaks the lake's raw-immutable / derived-append-only invariants, and it adds an external SaaS + credential dependency against the public-surfaces-only posture. Any future human-browsable view is a downstream rebuildable export from `derived/`, never the authoritative store, and is out of scope for v1. See §5. |

All four adapter, port, storage, projection, run, and validation contracts below
are accepted as written; Phase 1 implements exactly this adjudicated plan.

---

## 1. Ashby access-posture scan (ruling 3 — performed in Phase 0)

Single polite read-only GET, honest UA
(`ForsetiSourceCaptureAshbyScan/0.1 …`), against a real public Ashby board
(`ramp` — a non-beauty board used only to characterize the endpoint; the Phase 1
smoke capture uses real beauty boards):

- **Endpoint:** `GET https://api.ashbyhq.com/posting-api/job-board/{jobBoardName}?includeCompensation=true`
- **Auth posture:** none. Public, unauthenticated; returned `200 OK` to an honest
  UA with no key, cookie, or token.
- **Response:** `application/json; charset=utf-8`, ~2.23 MB for 126 jobs.
  Top-level keys `jobs`, `apiVersion`. **Single GET returns the full board — no
  pagination.**
- **Per-job fields:** `id, title, department, team, employmentType, location,
  shouldDisplayCompensationOnJobPostings, secondaryLocations, publishedAt,
  isListed, isRemote, workplaceType, address, jobUrl, applyUrl, descriptionHtml,
  descriptionPlain, compensation`.
- **JD is inline** (`descriptionHtml` + `descriptionPlain`, ~4.5 K chars observed)
  — **no per-job detail fetch needed.**
- **Structured location present:** `address.postalAddress.addressCountry` (e.g.
  `"USA"`), plus verbatim `location` string, `secondaryLocations`, `isRemote`,
  `workplaceType`. This gives Ashby a **genuine structured country field** for
  mechanical geography (verbatim extraction, no classification).
- **`publishedAt`** = posted date; `jobUrl`/`applyUrl` = source URLs; `isListed`
  = whether the posting is live.
- **Polite-access verdict: VIABLE / GREEN.** One unauthenticated GET per board,
  no pagination, inline JD. Size is the only caution: 2 MB+ boards approach the
  harness `direct_http` 5 MB default cap; the adapter must set an explicit,
  generous `max_bytes` and surface `size_cap_exceeded` honestly rather than
  truncate.

The Ashby **adapter** itself remains Phase 1 (scan-only in Phase 0, per ruling 3).

---

## 2. Where this lands in forseti-harness

- **One new source family:** `source_family = "ats_job_posting"`, with
  `ats_vendor ∈ {greenhouse, lever, workday, ashby}` carried as a projected
  **field**, not four separate families. Rationale: the lake's duplicate front
  door and availability listing scope by `source_family`; one family keeps
  dedup/discovery coherent while per-vendor differences live in per-vendor
  adapter modules and in the `ats_vendor` field.
- **Four adapter modules** under `forseti-harness/source_capture/adapters/`:
  `greenhouse_ats.py`, `lever_ats.py`, `workday_ats.py`, `ashby_ats.py`.
- **One runner** that maps adapter results → `write_local_source_capture_packet`
  kwargs (adapters never import the writer, never build packets — per
  `docs/adapter_author_contract.md` and the `reddit_api` exemplar).
- **One projection** `ats_job_posting_projection.py` producing one `derived/`
  row per posting.
- **One registry** reference file (see §4).

No `bronze/`/`silver/`/`gold/` lake directories are introduced (lake contract);
raw lands in `raw/`, the projection in `derived/`. (Module *names* like the
existing `retail_pdp_silver.py` are unaffected — the contract forbids medallion
*lake directories*, not module names; ATS modules use neutral names anyway.)

---

## 3. Adapter designs

All four follow the established contract (`docs/adapter_author_contract.md`;
exemplars `direct_http.py`, `reddit_api.py`): a free function
`fetch_{vendor}_ats_capture(...) -> Success | Failure` over native inputs,
**frozen** result dataclasses carrying honest `warning_notes` /
`limitation_notes`, a closed `FailureKind` `StrEnum`, a `Protocol` transport
seam so tests inject a fake (no live network in tests), no writer import, no
packet construction, no secrets in any result field. Honest UA per vendor; 403 /
429 map to typed failure kinds (`access_failed` / `rate_limited`), never a
workaround (drift guard).

Common failure kinds (per vendor, as applicable): `network_error`, `timeout`,
`access_failed`, `rate_limited`, `empty_result`, `malformed_response`,
`size_cap_exceeded`.

### 3.1 Greenhouse — CONFIRMED against jb

- **Endpoint:** `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true`
  (verified exact against jb's live workflow node string).
- **Request:** GET, no auth, no pagination — one call returns the full board.
- **Response → captured:** `job.title`, `job.location.name` (free-text location),
  `job.content` (full JD, inline), `job.absolute_url` (source URL), `job.id`
  (ats_job_id). Structured country is **not** reliably present (only
  `offices[].location` free-text). JD **inline**, no detail fetch.
- **Notes:** jb truncated JD to 5000 chars in its Normalize step — a jb display
  choice, **not ported** (D2: Forseti preserves verbatim in `raw/`, full text in
  `derived/`).

### 3.2 Lever — CONFIRMED against jb (jb built no adapter; research only)

- **Endpoint:** `GET https://api.lever.co/v0/postings/{company}?mode=json`
  (verified exact).
- **Request:** GET, no auth. Pagination via `skip`/`limit`; jb observed a full
  77-posting board in one response. The documented Lever rate limit applies only
  to POST application submissions, not read fetches.
- **Response → captured:** `text`/`title`, `descriptionPlain`/`description` (full
  JD, inline), `hostedUrl`/`applyUrl` (source URL), `id`, and a **structured
  top-level `country`** field (ISO 3166-1 alpha-2, e.g. `"US"`).
- **Geography (verified correction):** jb's scan explicitly concluded **do not use
  the `location` query param as a US filter** (string-match trap: returned 23/50
  actual US postings on one board). Forseti extracts verbatim `location` **and**
  verbatim structured `country`; it does not use `location` as a gate.

### 3.3 Workday — CONFIRMED endpoint; one handoff claim CORRECTED

- **Endpoint:** `POST https://{tenant}.{wd_server}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs`
  (list) **plus** a per-job detail `GET …/wday/cxs/{tenant}/{site}/job/{path}`
  for the JD (verified: JD is **not** inline in the list response).
- **Request:** headers `Accept: application/json`, `Content-Type:
  application/json`, optional `X-Calypso-Csrf-Token` (obtained from the careers
  HTML page, retried on 403). Body `{ appliedFacets, limit: 20, offset,
  searchText: "" }`. **Offset pagination**, page size 20.
- **Response → captured:** list gives title, external path/URL, id, structured
  location; detail GET gives
  `jobPostingInfo.jobDescription ?? jobDescription ?? description` (full JD).
- **Geography:** Workday exposes a **structured country facet** (`appliedFacets`
  country GUID) and, for tenants lacking one, jb used an `office_fallback`
  allowlist of US site codes. See §6 for the port posture (facet used only as a
  commission-declared bound, D3).
- **CORRECTION to the handoff:** the handoff states "jb used 1.5–2s for Workday."
  **jb's shipped code implements no per-request delay** — it runs
  `CONCURRENCY = 5` parallel tenant fetches with only a 5 s *retry-wait* on
  failure. The 1.5–2s figure is an **unimplemented research recommendation** in
  jb's q1b doc, not live behavior. Forseti should **implement** the polite
  posture jb only recommended: sequential per-board requests with a real
  1.5–2s inter-request delay (see §6). This is a deliberate improvement over the
  reference, recorded here rather than silently inherited.

### 3.4 Ashby — designed from the Phase 0 scan (§1)

- **Endpoint:** `GET https://api.ashbyhq.com/posting-api/job-board/{jobBoardName}?includeCompensation=true`.
- **Request:** GET, no auth, no pagination. Explicit generous `max_bytes`
  (boards exceed 2 MB); `size_cap_exceeded` on overflow, never truncate.
- **Response → captured:** `title`, `location` (free-text) +
  `address.postalAddress.addressCountry` (**structured country**), `descriptionPlain`
  / `descriptionHtml` (full JD, inline), `jobUrl` (source URL), `id`,
  `publishedAt` (posted date), `isListed`. Contradicting the handoff's
  "no research exists," the scan supplies a complete field contract.
- **Confirms handoff suspicion:** jb performed **no** Ashby research and built no
  adapter (only a Tier-3 future mention). The Phase 0 scan closes that gap.

---

## 4. Registry — shape and seeding (ruling 5, decision D1)

### Shape (recommended, not the ruling)

A **versioned reference file in the Git repo** (config/definition, not lake
data), one row per public board:

```
company, ats_vendor, board_token | (workday tenant + site), careers_url,
resolved_at, confidence
```

- **Home:** a source-map / reference artifact under the Capture spine
  (candidate: `forseti/product/spines/capture/satellites/ats_job_posting/ats_board_registry_v0.*`).
  Exact placement confirmed at Phase 1 against `repo-structure.yaml` /
  `check_placement.py`. It stays in Git (like `DecisionEvidenceAssemblyProfile`);
  **captured data never goes here, config never goes in the lake** (lake
  contract).
- The runner reads the registry to know which boards a commission targets.

### The ruling: how to seed it (D1)

| | **Option A — manual per-company entries** *(recommended)* | **Option B — agent-assisted careers-page sniffing** |
| --- | --- | --- |
| **What** | Operator/owner hand-adds each verified board row (company, vendor, token, careers_url). | A sniffer module probes a *given* company's careers URL, detects vendor + token by URL/DOM pattern (greenhouse token, lever slug, `jobs.ashbyhq.com/{org}`, workday tenant/site), emits candidate rows for human confirmation. |
| **Build effort** | Near-zero: a data file + a one-line schema note. | A per-vendor detection module + a human-confirmation review step. |
| **Per-run toll** | Zero standing; each new company is a one-time manual add. | Each sniff run carries a recurring human-confirmation step; detection heuristics rot as vendors change URL shapes (maintenance toll). |
| **Confidence** | High — every row human-verified once. | Lower — every detected row needs confirmation before use. |
| **Risk posture** | Fully mechanical; no crawler, no discovery automation; aligns with ruling 2 + drift guard. | Edges toward discovery automation; must be bounded to *given companies* (detect vendor, never crawl the web to find companies) or it becomes a standing crawler (forbidden). |

**Recommendation: Option A for v1** (smallest complete, mechanical, no crawler
risk, high confidence). Option B is a deferred upgrade if the board count grows
enough that manual onboarding is the bottleneck — at which point it is a
bounded, human-confirmed sniffer over an explicit company list, never a web
crawler. **Owner picks D1 at adjudication.**

---

## 5. Storage and projection contract

**Raw (verbatim, immutable — `raw/`).** Each capture run of a board produces one
`SourceCapturePacket` via `write_local_source_capture_packet`, staged then
atomically published to `raw/<packet_shard>/<packet_id>/`. The **verbatim ATS JSON
response is the preserved raw file** (the byte-faithful board response;
Workday's per-job detail responses preserved alongside). The lake's byte-identical
duplicate front door (`DuplicateCapturePacketError`, keyed on `source_locator` +
sha256 multiset) already rejects an unchanged re-capture — so an unchanged board
snapshot is caught at write time (this is what replaces jb's CW2 dedup; see §7).

**Snapshot granularity (D4, recommended):** **one packet per (board, as-of)
snapshot.** `source_locator` = the board API URL; each **posting is a
`SourceCaptureSlice`** (slice `locator` = the posting's `jobUrl`). This matches
the packet model (≥1 slice, ≥1 preserved file), the `reddit_api` "listing → one
slice per unit" shape, and the drift guard's "dated point-in-time snapshots."
Alternative (one packet per posting) is workable but multiplies writes and
loses the board-level snapshot identity; not recommended.

**Derived (mechanical projection — `derived/`, append-only, keyed to raw).** One
projection module emits one row per posting:

```
company, title, description, posted_date, source_url, ats_vendor,
ats_job_id, captured_at
```

Plus two mechanical geography fields (verbatim only, no classification — §6):

```
location_raw        # the verbatim vendor location string
location_country    # verbatim structured country where the vendor exposes one
                    # (Lever `country`, Ashby address…addressCountry, Workday
                    # facet/site); empty with a reason where the vendor has none
```

- **Description depth (D2, recommended): full text.** Raw preserves the verbatim
  JSON regardless; the derived row carries the **full** `descriptionPlain` /
  `content` / detail JD. jb's 5000-char truncation is **not ported** — truncation
  would drop evidence, which the capture operating model forbids. (If a real
  size problem ever appears, truncation returns as a scoped amendment, not a
  default.)
- The projection follows the `projection_shared.py` mechanics (HTML→text
  normalization, forbidden-field guards, packet-contained file reads) and is
  registered with the shared-helper duplication gate if it reuses guarded
  helpers. It performs **no** ranking, dedupe-by-similarity, scoring, or
  relevance filtering — purely mechanical field extraction.

---

## 6. Geography and job-filter mechanics — jb review and port verdicts (ruling 6)

jb's discovery spine (CW1/CW2) and the Workflow-B recheck were reviewed by direct
read (git sources) and the n8n-DB boundary was accounted for. Per ruling 6, any
ported scoping must stay **mechanical and commission-declared**; anything that
smells like relevance filtering or classification stays downstream (ruling 2).

| jb mechanism | What it actually is | In git? | Port verdict |
| --- | --- | --- | --- |
| **CW1 `isUsMarket()` US gate** | Deterministic **lexical classifier** of a free-text `location` string against a curated `US_CITIES`/state allowlist + ambiguity carve-outs + a foreign-country blocklist; **fails open on blank location**. "Deterministic gate; no LLM." | Yes (byte-verified live==git) | **DO NOT PORT into capture.** It classifies a posting as in/out-of-market — a relevance judgment, downstream per ruling 2. Capture instead extracts the **verbatim** `location_raw` + **verbatim structured** `location_country`. A curated-allowlist classifier, even deterministic, is a downstream lens, not capture. |
| **Workday country facet** (`appliedFacets` country GUID) + `office_fallback` | A fetch-time **structured** country scope on the request. | Yes | **PORT ONLY as a commission-declared bound (D3).** A country facet applied because *the commission declared "US-market boards"* is mechanical and commission-declared (ruling 6's allowed shape). Applied as a capture-side default it would silently drop non-US postings (a capture relevance decision). **v1 default: full-board fetch, no facet**; use the facet only when a commission explicitly declares the bound *and* the board is too large to fetch politely — recorded in the commission and the packet receipt as a declared bound, not a capture judgment. |
| **CW1 finance-family classifier** | Deterministic title→family keyword classifier. | Yes | **DO NOT PORT.** Pure classification — downstream (ruling 2). |
| **CW2 "final recheck + upsert"** | A **dedup** recheck against jb's Google Sheet immediately before upsert (not a geography recheck). | Yes | **NO PORT.** Forseti's raw-immutability + byte-identical duplicate front door already provide dedup-before-write; jb's sheet-upsert dedup is jb-runtime-specific. |
| **Workflow-B "target freshness recheck"** | A **scheduled** passive job re-visiting accepted rows to mark LIVE/STALE/CLOSED. | Yes | **NO PORT as a scheduler.** Drift guard forbids a standing crawler/scheduler; re-observation is a **new dated commission**. The concept (a later snapshot vs an earlier one) maps to the packet model's `re_capture_relationship` (supersede/supplement/conflict), set on a fresh commissioned capture — no standing job. |
| **Spine-A / Spine-B routing wrappers** | Pre/post-CW1 wrappers: field validation, dedup-key compute, `_lane` routing. | **No — live only in n8n DB** | **NO PORT (and not portable from git).** Only their *design* is in git; the artifacts never were. Forseti's writer + lake (packet assembly, duplicate front door, availability index) already provide the equivalent mechanical guarantees. |
| **JD 5000-char truncation** (CW1 Normalize) | A display truncation. | Yes | **NO PORT** (D2). |

**Net:** the only thing that ports from jb's geography/filter layer is **mechanical
verbatim extraction** of location + structured country. Every relevance/classification
mechanism (isUsMarket allowlist, finance-family, LLM triage in jb's separate
Workflow-C prep lane) stays downstream. Geographic *scoping* is expressed as a
**commission-declared bound** (which boards the registry names, or an explicit
country facet the commission declares), never a capture-side judgment.

---

## 7. Run mechanics

- **Commission-bounded.** A run takes a target board list (from the registry,
  §4) + an as-of date. No standing crawler, no scheduler (drift guard).
- **Per-board typed discharge state**, aligned to the capture obligation
  vocabulary: `met` / `partial` / `blocked` / `unavailable_by_source` (a
  bot-blocked or unreachable board is a typed gap, never a silent skip or a
  workaround).
- **Polite access.** Sequential per-board requests with a real **1.5–2s
  inter-request delay** (implementing the posture jb only recommended — §3.3),
  honest per-vendor UA (`direct_http` convention), explicit generous `max_bytes`.
  403/429 → typed `access_failed` / `rate_limited`; honor each surface's access
  posture; **public unauthenticated surfaces only**.
- **No auth, no credentials.** All four endpoints are public and unauthenticated
  (Workday's CSRF token is a public per-session token fetched from the careers
  page, not a secret) — no secret ever appears in any result field or metadata.

---

## 8. Validation approach (Phase 1)

- **Per-adapter unit/contract tests** using the `Protocol` transport seam: inject
  fixtures captured from real board responses; **no live network in tests**
  (`reddit_api` pattern). Cover happy path + each failure kind (403, 429, empty,
  malformed, size cap).
- **Adapter self-test** per the harness convention (focused, fails visibly).
- **One bounded live smoke capture** against **2–3 real public beauty-brand
  boards spanning ≥2 ATS vendors**, demonstrating dated point-in-time snapshots
  end-to-end (fetch → raw packet → derived rows). Candidate beauty boards to
  **confirm at smoke time** (existence/vendor verified live in Phase 1, not
  asserted here): an Ashby board and a Greenhouse or Lever board of US beauty
  brands named from the seeded registry. The smoke capture is the success signal
  for Phase 1 (§ handoff success signal).

---

## 9. Effort order and v1 exclusions

**Effort order:**

1. Registry file + schema (after D1 ruling) — smallest, unblocks the runner.
2. **Greenhouse** adapter (simplest: GET, no auth, inline JD, no pagination).
3. **Ashby** adapter (GET, no auth, inline JD, structured country; scan done).
4. Runner + `write_local_source_capture_packet` wiring; the projection.
5. **Lever** adapter (GET, no auth, structured country; light pagination).
6. **Workday** adapter (POST + CSRF + offset pagination + per-job detail — the
   heaviest; last).
7. Per-adapter tests alongside each; smoke capture last.

**v1 excludes:** any classification/ranking/relevance filtering/pain inference;
any scheduler or standing crawler; any re-observation automation (re-capture is a
new commission); agent-assisted registry sniffing (D1 Option B) unless the owner
selects it; non-public or authenticated ATS surfaces; ATS vendors beyond the four
(Taleo, SmartRecruiters, iCIMS, Avature, etc. — jb Tier 3/4, out of scope);
description truncation; the Workday country facet as a default (D3).

---

## 10. Success signal for this plan

The owner can adjudicate in one pass: **rule D1 (registry seeding)**, confirm or
adjust **D2–D4**, and accept / amend / reject the adapter, port, storage,
projection, run, and validation contracts above. Every jb-derived claim was
re-verified and corrections are called out (Workday pacing not implemented in jb;
Lever `location` param unreliable; Ashby had no jb research — now scanned; jb US
gate is a downstream classifier, not ported). On acceptance, Phase 1 implements
exactly the adjudicated plan; jb remains untouched.
```
