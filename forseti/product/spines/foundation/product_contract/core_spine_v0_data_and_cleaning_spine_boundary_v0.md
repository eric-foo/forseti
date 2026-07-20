# Core Spine v0 Data and Cleaning Boundary

```yaml
retrieval_header_version: 1
artifact_role: Product architecture boundary
scope: >
  Canonical ownership from source acquisition through capture retention,
  Cleaning adaptation, ECR posture, and Silver production.
use_when:
  - Deciding whether source bytes, content records, Cleaning handles, or Silver facts own a field.
  - Designing a capture-retention change or a source-family Cleaning adapter.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
stale_if:
  - The owner changes capture retention, Cleaning ownership, ECR posture, or Silver admission.
```

Status: owner-ratified boundary, revised 2026-07-20.

## Canonical path

```text
source acquisition
  → Source Capture packet (raw or canonical content)
  → Cleaning-owned validation and source-family adaptation
  → ECR posture and Cleaning audit
  → Silver facts
  → Judgment
```

There is no standalone capture Projection layer in this path.

Capture owns acquisition, access and pin admission, deterministic family
extraction, and retention. For a content-eligible route, Capture writes the
family-owned `content_record.json` before releasing disposable DOM, visible
text, or HTTP response bytes. For a genuine raw route—or any access, pin,
sufficiency, secret, or extraction failure—Capture preserves raw evidence and
fails loud. Capture never writes a derived Projection packet.

Cleaning owns validation of the retained content record, binding its rows to
the real packet and packet-local JSON pointers, family adaptation, exact source
anchors, residual propagation, transformation ledgers, and cleaned working
views. Raw historical packets are decoded through explicit read-only legacy
adapters. That compatibility route may read old Projection-era artifacts; it
must never create a new Projection record.

ECR owns source-side epistemic posture. It may reference the same capture
packet as Cleaning, but it does not become content extraction, Cleaning, or
Judgment.

Silver producers consume a Cleaning result. They do not read a persisted
capture Projection record, and they do not bypass Cleaning by reinterpreting
discarded source envelopes.

Judgment alone owns credibility, independence effects, salience, Signal
Integrity, Signal Use, Decision Strength, and Action Ceiling.

## Retention contract

Current capture retention has two requested modes:

- `content`: retain the canonical family content record and its extraction
  metadata; hash then discard only the source envelopes declared disposable by
  that route.
- `raw`: retain the original source evidence and do not pretend extraction
  succeeded.

Metadata records `requested_retention_mode`, `retention_outcome`,
`extractor_version`, `extraction_status`, and the hashes and byte counts of
each disposable input. A failed extraction has outcome `raw_failure`, preserves
all supplied original artifacts, and returns the route's typed nonzero failure.

There is no admitted `sample` packet. Extractor qualification is ephemeral:
operator-supplied scratch inputs are compared with a canonical content record;
a match deletes only those explicit scratch inputs and leaves a qualification
report, while drift or failure preserves scratch for diagnosis. Qualification
never admits a packet and is not a standing lake lane.

Screenshots and browser metadata are retained only according to their capture
contracts. A screenshot is source-media evidence, never access proof and never
a substitute for URL, locale, currency, ZIP, challenge-free, or sufficiency
admission.

## Source-anchor contract

A Cleaning input handle contains one `CleaningSourceAnchor`, plus optional
source row identity and ECR reference. A source anchor identifies either:

- a preserved packet file or a packet-local selector/pointer within it; or
- a separately persisted derived source record, such as an ASR transcript.

Content rows bind to `/rows/<index>` or another honest pointer in the retained
content record. The handle contains no Projection reference or
`keyed_siblings_over_raw` relation. Exact-identity dedupe uses the complete
source-anchor identity; near-match and semantic clustering remain separately
authorized mechanics.

## Analytical projections

Cross-packet analytical products may still use “projection” when they are an
actual observation or aggregation layer rather than a capture-retention
adapter—for example Instagram, TikTok, or YouTube behavioral series. Their
writers, versions, and cadence are governed by their own contracts. This
exception does not reopen capture Projection packets.

## Historical compatibility

Existing raw, sample-era, content, and persisted Projection artifacts remain
immutable and readable. Compatibility code is:

- read-only;
- isolated from current writer APIs and package exports;
- forbidden from minting new Projection records;
- required to produce the same Cleaning-owned source-anchor shape as current
  content consumption.

## Non-claims

This boundary does not make content records Judgment-ready, prove source or
corpus completeness, authorize anti-blocking escalation, treat compactness as
salience, or retire analytical aggregation projections. It does not permit
discarding genuine raw evidence or failure artifacts.
