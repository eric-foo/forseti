# Core Spine v0 Cleaning Spine README

```yaml
retrieval_header_version: 1
artifact_role: Product architecture entrypoint
scope: Plain-language purpose and build boundary for Cleaning Spine v0 and its thin source-agnostic cleaning core.
use_when:
  - Onboarding to Cleaning Spine before reading the full foundation.
  - Checking whether a cleaning rule belongs in source-invariant core, source-family adaptation, or unresolved candidate space.
  - Preparing implementation scoping for a thin Cleaning core without turning it into generic ETL or Judgment.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - Cleaning Spine Foundation changes the layer boundary, allowed transform classes, ledger contract, or source-family adaptation boundary.
  - Data Capture / Evidence Candidate Record / Cleaning / Judgment ownership changes.
  - Projection Doctrine is amended, superseded, ratified differently, or rejected.
```

- Status: `PURPOSE_ENTRYPOINT`
- Source basis: current Cleaning Spine Foundation, Data Capture / Cleaning boundary note, and Projection Doctrine candidate posture.
- Supersedes: nothing.
- Implementation authorized: bounded_substrate_v0 (source-invariant Pydantic models + exact-identity deriver; `orca-harness/cleaning/`; does not authorize broader Cleaning, ECR, or Judgment implementation).
- Runtime schema authorized: bounded_substrate_v0 (in-memory Pydantic schema only; not a persisted storage, API, or final object-model schema).
- Authority note: this README is a map and purpose guide. The foundation and boundary notes carry the load-bearing rules.

## Purpose

Cleaning Spine exists because Orca needs to work with messy captured material
from many source families without losing the ability to inspect the original
evidence.

Its job is to turn raw capture, projection views, and Evidence Candidate Record
receipt material into a cleaner working view while preserving traceability. It
records what changed, why it changed mechanically, what raw or projected material
the change came from, what was preserved, and what a later reviewer still needs
to inspect.

Cleaning is not where Orca decides whether evidence is credible, independent,
important, demand-supporting, or action-supporting. Cleaning makes evidence
easier to inspect. Judgment decides what the evidence means.

## Short Mental Model

For any source family, the intended flow is:

1. Data Capture preserves raw material, source identity, timing, visibility, and
   capture context.
2. Projection, when used, turns source material into an inspectable mechanical
   row or packet view with warnings and loss records.
3. Evidence Candidate Record receipt records the pre-cleaning handoff facts.
4. Cleaning creates a stable input handle keyed to raw, then writes a transform
   ledger over that handle.
5. Judgment consumes the cleaned working view, ledger, warnings, residuals, and
   raw-pull triggers, but reopens raw whenever source meaning or decision use is
   load-bearing.

Raw remains canonical. Projection and Cleaning are working views.

## What Is Generic

The scalable Cleaning core should be generic at the contract level:

- stable cleaning input handles keyed to raw;
- optional projection and Evidence Candidate Record references attached to the
  handle;
- non-destructive transform ledger entries;
- preservation checks for source identity, timing, hierarchy, semantic binding,
  counts, and original addressability;
- residuals, warnings, omissions, and raw-pull triggers;
- allowed transform classes such as normalization, translation, summarization,
  exact-identity dedupe mechanics, and ledger propagation;
- explicit non-claims that prevent Cleaning from becoming Judgment.

That generic layer lets Reddit threads, retail PDP/review surfaces, social or
video surfaces, official/package documents, support-style review surfaces, and
browser-visible access overlays enter the same Cleaning contract without turning
each source family into a separate spine.

Public-reaction engagement context is one named working view inside this generic
contract. When Capture or Projection preserves visible reaction metrics, Cleaning
may surface `engagement_context` for navigation and traceability. It must keep
raw/projection refs, metric posture, row binding, residuals, and non-claims; it
may preserve direction, visible audience-fit basis, baseline context, and
discount reasons as resonance context; it must not decide final resonance
weight, credibility, independence, amplification, demand support, or Action
Ceiling.

## What Is Not Generic

Cleaning should not be built as a broad all-purpose data-cleaning platform.

Generic ETL often optimizes for one clean table, compactness, or downstream
analytics convenience. Orca needs evidence-grade preservation. A cleaner view is
only useful if the raw source, projection loss, timing, source identity, counts,
hierarchy, and unresolved ambiguity remain visible.

The core therefore must not:

- acquire sources, choose source access paths, or remove source envelopes;
- delete or hide evidence rows because they look repetitive, awkward, low-value,
  bot-like, confusing, or non-salient;
- convert projection or Cleaning views into canonical raw evidence;
- assign credibility, independence, salience, Signal Integrity, Signal Use,
  Decision Strength, or Action Ceiling;
- code-enforce near-match dedupe, copied-language grouping, or clustering in
  core v0 unless separately owner-authorized.

The useful genericness is the invariant preservation contract, not a universal
cleaning engine.

## Source-Family Adaptation

Different sources still need different adapters or family rules. A Reddit thread
has chains and comments. A retail PDP has product, seller, price, claims, review,
and page-state surfaces. Official documents have publication, versioning, and
package-context issues. Browser-visible overlays may have access-path and
inspectability constraints.

Those differences belong in `source_family_adaptation` or
`unresolved_candidate` space until they are proven source-invariant. A
family-specific rule should not become core merely because it is useful once. It
can move toward core only after comparison across at least two non-overlapping
source families or explicit owner acceptance of the exception.

## Scalable Build Shape

The first scalable build should model the source-invariant core before it grows
source-specific convenience logic:

1. Define the Cleaning input handle and transform ledger shape.
2. Keep raw, projection, and Evidence Candidate Record references distinct.
3. Implement non-destructive transform records and preservation checks.
4. Limit core v0 dedupe mechanics to exact-identity membership.
5. Carry warnings, residuals, omissions, and raw-pull triggers forward.
6. Put family-specific parsing and heuristics behind thin adapters.
7. Prove the same core can handle at least two non-overlapping source families
   without leaking source-specific fields into the invariant contract.

This also makes Cleaning usable as the cleaning spine of a normal data pipeline
when the pipeline needs auditability, reversibility, and provenance. It is less
suited to disposable ETL where raw traceability and later human inspection do
not matter.

## Build Boundary

This README supports implementation scoping, but it is not implementation
authorization. A build plan still needs to bind:

- the first source-family fixtures;
- the exact runtime schema names;
- validation expectations;
- how warnings and raw-pull triggers are represented;
- which transforms are implemented now versus left as ledger-only candidates.

Until then, the durable direction is: build a thin source-agnostic Cleaning core
around traceable handles and non-destructive ledgers, with source-family
adaptation at the edge and Judgment outside the Cleaning layer.
