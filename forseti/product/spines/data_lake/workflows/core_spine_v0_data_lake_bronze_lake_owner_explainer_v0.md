# Core Spine v0 Data Lake Bronze Lake Owner Explainer v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/orientation record
scope: >
  Owner-facing plain-language explainer for the Bronze lake: what it is, why it
  exists, the rules it lives by, how Silver relates, what Mini God Tier versus
  full God Tier means, and what the two physicalization gates protect. Stable
  concepts only; live lane state is reached through the pointer at the end.
use_when:
  - The owner asks "explain the Bronze lake" or "where does captured data actually live".
  - Re-orienting a non-specialist reader before a Data Lake decision or ratification.
  - Checking what MGT versus full GT means without reading the contracts.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/README.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
stale_if:
  - A lake authority contract materially changes an invariant restated here.
  - Gate 1 or Gate 2 is ratified with a posture that contradicts the gates section.
  - The "Where things stand" pointer no longer names the active continuation anchor.
```

This document explains; it decides nothing. Where it disagrees with a contract
in `forseti/product/spines/data_lake/authority/`, the contract wins.

## What the Bronze lake is

The Bronze lake is Forseti's permanent raw-evidence vault. Every time Forseti
captures something from the outside world - a page, a post, a video's
transcript, a review - the capture lands here first as a **packet**: a sealed,
write-once bundle of exactly what was collected, with a manifest and
cryptographic hashes so anyone can later prove the bytes are unaltered. Nothing
in Bronze is ever edited, cleaned, deduplicated, scored, or judged. It only
grows.

## Why it exists

Every product claim Forseti ever makes downstream - a signal, a judgment, a memo -
must be traceable to raw truth. If the raw layer could be silently edited,
lossy, or unverifiable, nothing built on top of it would be provable. Bronze is
the layer that makes "show me the original evidence" always answerable.

## The rules Bronze lives by

- **Write-once raw.** A published packet is never mutated. Corrections arrive
  as new records, never as edits to old ones.
- **Append-only derived records.** Anything computed about a packet is attached
  alongside it, create-only.
- **Find-by-key.** Every packet and body is reachable by a stable key; that key
  discipline, not a queue or event system, is how things are found.
- **Hash-checkable.** Reading raw re-verifies content hashes against the
  manifest; tampering or rot is detectable, not silent.
- **Indexes are conveniences, never truth.** Catalogs and indexes are generated
  read surfaces, rebuildable from the packets at any time. If an index burned
  down, nothing would be lost.
- **The lake is not smart.** It does not clean, dedupe, score, judge, schedule,
  retry, or call other systems. Those belong to downstream spines.
- **Real data lives outside the repo.** Operational packets sit under an
  operator-configured external data root, not in Git.

## Attachment Records in one breath

An Attachment Record is the index card for a large piece of evidence: a compact
keyed entry that points at an immutable body (the sealed box) together with the
fingerprint (hash) that proves the body is intact. Consumers resolve the card
through public helper surfaces and re-check the fingerprint; they never infer
private folder layouts.

## How Silver relates

Silver is the first derived layer: validated records that *cite* Bronze rather
than copy it - every Silver observation carries source-backed references back
to raw packets. Two independent source families (Instagram and YouTube) already
produce Silver records by consuming Bronze's public catalog and Attachment
Record surfaces, which is the proof that the read path works. Layer semantics
(bronze / silver / pre-gold / gold-ready / gold) are owned by the medallion
contract in `authority/`.

## Mini God Tier versus full God Tier

> **Status update (2026-07-03):** the owner ratified the Bronze full-GT
> declaration
> (`authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md`), so
> Bronze is now full God Tier for the bounded slice that record names —
> fixture-proof tier, Gate 2 claim ceiling, backend still deliberately
> unselected. The two paragraphs below explain what the ladder *meant*; the
> declaration owns the current claim.

**Mini God Tier (where Bronze was until 2026-07-03):** the *behavior* is
proven. Typed raw truth goes in write-once, comes back by key, verifies by
hash, and two Silver consumers read it through public surfaces. For everyday
capture-and-consume work, Bronze is dependable today.

**Full God Tier (now ratified, within its named exclusions):** the *physical
architecture* is also deliberately decided, implemented, and proven - how
Attachment Record bodies are physically bound and laid out (Gate 1), what
retention and lawful erasure mean (Gate 2's ratified deferral and claim
ceiling), how the canonical entry is serialized and derived (A2), each chosen
on purpose and demonstrated against the lake's invariants by CI-owned,
fail-capable proofs. The storage backend remains deliberately unselected — a
future backend must prove this architecture, never choose it.

## The two gates, and why they exist

The lake's rule is: **the storage backend must prove the architecture, never
choose it.** Two decisions would otherwise get made silently by whatever
backend is easiest to build on, and both are nearly irreversible once real data
piles up:

- **Gate 1 - body layout.** What is the physical bond between the index card
  and the sealed box - is the body a packet member, a hash-pinned sidecar, or
  something else; exactly which bytes does a verifier re-hash; and through what
  public surface do readers resolve it? Decide this before any backend, or the
  backend's convenient shape becomes the answer by accident.
- **Gate 2 - retention and lawful erasure.** What may "delete" ever mean in an
  immutable lake - tombstones, key-shredding, backend lifecycle rules, or an
  explicitly accepted "not yet"? Decide this before a backend makes the choice
  for you, because a backend picked first quietly becomes your legal posture.

Each gate is answered by an ADR (architecture decision record): a short
document the owner ratifies, comparing options and locking one - or explicitly
deferring with named residuals and revisit triggers. ADRs are cheap and
reversible until ratified; storage migrations are neither. That asymmetry is
the entire value: a page of deliberate decision now versus re-keying or
re-ingesting the whole lake later.

## Where things stand (pointer, not state)

Live lane state is never carried in this explainer. Read the active
continuation anchor:
`forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_plan_v0.md`,
and its `open_next` chain, for the current gate status and next step.

## What this document is not

Not authority, not validation, not readiness, not a full-GT claim, and not a
substitute for the contracts. It is the owner's plain-language map of the
territory the contracts govern.
