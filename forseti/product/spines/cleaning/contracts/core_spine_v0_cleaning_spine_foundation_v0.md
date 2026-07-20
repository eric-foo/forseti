# Core Spine v0 Cleaning Spine Foundation

```yaml
retrieval_header_version: 1
artifact_role: Product-method foundation artifact
scope: >
  Cleaning-owned validation, source adaptation, transformation, traceability,
  and Silver handoff for canonical content and historical raw evidence.
use_when:
  - Implementing or checking Cleaning input handles and source-family adapters.
  - Deciding whether a transformation, residual, anchor, or cleaned fact belongs in Cleaning.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
stale_if:
  - Cleaning input ownership, transform classes, Silver admission, or Judgment ownership changes.
```

Status: owner-ratified foundation, revised 2026-07-20.

## Purpose and boundary

Cleaning turns retained source evidence into smaller, inspectable working
material without deciding what the evidence means. It is the only current
boundary that:

- validates `content_record.json`;
- rebinds content rows to actual packet identity and packet-local JSON pointers;
- adapts family rows into `CleaningInputHandle` values;
- propagates omissions, residuals, warnings, and raw-pull triggers;
- records non-destructive transformations; and
- supplies cleaned facts to Silver producers.

Capture owns acquisition and retention. ECR owns source-side epistemic posture.
Judgment owns credibility, independence, salience, Signal Integrity, Signal
Use, Decision Strength, and Action Ceiling.

## Inputs

Cleaning may receive:

- a current canonical content record and its packet manifest;
- an immutable historical raw packet decoded by a family-owned legacy adapter;
- a read-only historical Projection-era artifact through the legacy decoder;
- ECR source-side receipt material; and
- separately persisted derived source records such as ASR transcripts.

A historical Projection artifact is compatibility input, not a current layer.
No Cleaning path may write or require a new capture Projection record.

## Input handle

The minimum current handle is:

```yaml
cleaning_input_handle:
  handle_id: "<stable within the Cleaning packet>"
  source_family: "<family>"
  source_surface: "<surface>"
  source_anchor:
    packet_id: "<capture packet>"
    slice_id: "<optional slice>"
    file_id: "<optional preserved file>"
    relative_packet_path: "<optional packet-local path>"
    sha256: "<source commitment>"
    hash_basis: "<declared basis>"
    anchor_kind: "<file | json_pointer | html_selector | script_index | text_pattern | derived_record>"
    json_pointer: "<when anchor_kind=json_pointer>"
    anchor_value: "<when another specific anchor kind requires it>"
    derived_record_ref: "<when anchor_kind=derived_record>"
  source_row_id: "<optional family row identity>"
  source_row_kind: "<optional family row kind>"
  ecr_ref: "<optional packet-keyed ECR source-side receipt>"
  residuals: []
  warnings: []
  raw_pull_triggers: []
```

Current content rows use honest pointers into the retained content record.
`source_row_id` and `source_row_kind` preserve family row identity without
creating a second authority object. There is no `CleaningProjectionRef`,
`projection_ref`, `CleaningRawAnchor`, or `KEYED_SIBLINGS_OVER_RAW`.

## Validation and adaptation

Before emitting handles, the current-content adapter must verify:

- one unambiguous `content_record.json`;
- manifest hash and path binding;
- family, source surface, source URL, content schema, and extractor version;
- successful content retention metadata;
- packet slice/file consistency; and
- family-specific pin and sufficiency conditions.

The adapter then binds each row to the real packet and its JSON pointer. It may
normalize source-family shapes, but it may not fabricate packet/file identity,
facts, counts, source visibility, or missing rows.

The legacy decoder is read-only and visibly named as compatibility. It produces
the same source-anchor handle shape and never persists a new intermediary.

## Allowed transformations

Cleaning may perform only ledgered, traceable, non-destructive:

- formatting and whitespace normalization;
- unit or source-native representation normalization that preserves the
  original value;
- translation paired with source-language text and method;
- navigation summaries whose originals remain addressable;
- exact-identity duplicate grouping using complete source-anchor identity; and
- propagation of capture, ECR, and Cleaning residuals or warnings.

Near-match dedupe, copied-language grouping, semantic clustering, and
cross-source reconciliation remain separately authorized mechanics.

Every transform ledger entry identifies its input handle, rule, input grain,
original and transformed values where applicable, preservation checks,
omissions, residuals, warnings, and raw-pull triggers.

## Engagement context

When separately authorized, Cleaning may preserve source-visible engagement
context—helpful votes, likes, views, reply counts, visible sort/order, and
row-bound hierarchy—as navigation facts. It must retain metric posture,
row/source binding, timing, omissions, and residuals.

Engagement is not proof. Cleaning may not label material credible, independent,
strong, weak, demand-supporting, amplified, discounted, excluded, or
action-supporting.

## Silver handoff

Silver producers consume the validated Cleaning result and use
`CleaningSourceAnchor` values for lineage. A Cleaning audit pack may persist the
full transform ledger as processing evidence; it is not a Silver fact. Silver
facts carry a one-way reference to the audit pack when one is written.

No Silver producer may require a persisted capture Projection record or reread
discarded DOM/text to recover facts already present in canonical content.

## Failure and raw pull

Malformed content, schema or hash drift, source mismatch, missing required
rows, or dishonest anchors fail loud before cleaned or Silver output. Raw-pull
triggers explain which original source evidence requires inspection; they do
not silently replace canonical content or confer Judgment status.

## Non-claims

Cleaning is not source acquisition, source truth, corpus completeness,
credibility assessment, sentiment judgment, demand proof, Evidence Unit
binding, or product readiness. Compactness never authorizes evidence deletion
or salience ranking.
