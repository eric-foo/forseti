# Coordinator return serialization sample — 2026-09-12

```yaml
retrieval_header_version: 1
artifact_role: Bounded implementation and dogfood record
scope: Lossless advance return serialization; structural sample and unmeasured subscription impact.
use_when:
  - Deciding whether to land the coordinator return serialization candidate.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/coordinator-efficiency-20260912/measurement.json
```

The candidate preserves the complete `advance` return and removes JSON
indentation. Seven genuine CLI boundaries shrink from **85,886 to 81,211 UTF-8
bytes** (LF-normalized): **4,675 bytes / 5.44%**. Every parsed value and the final
native consumer view match. **Subscription quota savings are unproven. I would
not land this change solely as a quota-efficiency fix on this evidence.** The
small, reversible serialization candidate is retained for the source owner's
landing decision; this record does not promote its economic value.

The initial baseline was already compact in substance: ready returns were mostly
complete generated worker instructions. Removing transitions would lose earlier
reconciliation-level bindings that the current artifact map does not retain.
There was no justified bulk-removal formatter or new artifact store to build.
The only runtime change is serialization in the public CLI; the two actual
consumer guidance sources say to parse once, forward full worker prompts
unchanged, and load complete relevant evidence for source-dependent judgment.
Worker intake, schema, raw-write/submit instructions, immutable publication,
selection, grouping, default authoring and the 60-second wait ceiling are unchanged.

| Native boundary | Before bytes | Candidate bytes |
| --- | ---: | ---: |
| Ready extraction | 15,021 | 14,445 |
| Unchanged pending extraction | 15,020 | 14,444 |
| Invalid response, exit 2 | 8,933 | 8,404 |
| Verification ready | 16,292 | 15,597 |
| Reconciliation level 1 | 11,355 | 10,667 |
| Reconciliation level 2 | 12,365 | 11,566 |
| Completed view | 6,900 | 6,088 |

The sample reused the existing four-leaf alternate `_advance_replay_fixture`
with method v13, `input_order`, authoring v4, 30,000 prompt bytes and two
evidence items per work unit. These are deterministic native-valid fixture
answers, **not fresh generation or saved model-authored judgments**. Each arm
submitted six unchanged answers through native intake and immutable submission,
then read back the same accepted view and response hashes. One deliberately
invalid response was preserved outside the response directory before replaying
the valid answer in each arm. That equal preparation intervention does not
establish autonomous operator-rescue performance. The invalid return retained
its exact filename/batch-identity error, nonzero exit, and another ready request.

The implementation coordinator read the complete materialized source and view:
all four fixture leaves say “I did not find the balm drying during winter use.”
The view preserves that negation, winter condition, `descriptive_only` ceiling,
`not_checked` conflict and unavailable capture completeness. Completion therefore
does not support the opposite drying claim or global absence of opposition.
This is a bounded fixture assessment, not independent semantic qualification;
the historical neutral/approval/price campaign was not rerun because serialization
does not alter any of its evidence or judgment inputs.

One Astra/high baseline coordinator replay launch failed on local Codex
configuration loading before generation. Authentication was not determined;
no model usage or provider response exists. The candidate arm was not launched
after the owner clarified the economic target and prohibited further attempts
merely for price comparison. There is no measured token, Codex-credit, API-cost
or quota delta. The owner-supplied Codex credit rates are preserved only as an
unused proxy in [measurement.json](measurement.json); they do not establish a
mapping to this Pro account's usage percentage. Account-wide percentage changes
would also be confounded by another active task.

Focused advance/job/worker tests and the 18 harness coupling contract tests
exited zero. The real candidate replay passed exact parsed-state comparison at
all seven boundaries, native receipt readback and final view byte equality.
Preparation, development and this report are outside the recurring sample
denominator; their cost was not measured. No extra model worker, judge, helper,
repair or compaction was launched. No independent review, publication or landing
was performed. Full CI remains a publication concern for the source task.

The managed worktree is `C:/Users/vmon7/.codex/worktrees/f8e7/forseti`, branch
`codex/coordinator-efficiency-20260912`, initially clean at required baseline
`307e149ae80075e115abfd543e7ec4a43964166e`, with no other writer observed. The
advisory diagnosis and corrected measurement hashes matched and those files
were not edited. Exact inputs, source pins, errors, counts and raw artifact
pointers are in the measurement. Raw sample files remain under the worktree's
ignored `forseti-harness/_scratch/coordinator-efficiency-20260912/`; preserve
that directory for raw replay inspection. The record is stale for changed
serialization, worker transport, fixture bytes or quota-meter semantics.

Completion remains owned by source task `01a0955a-643a-7dc1-b747-da71e35b40f7`.
The unresolved outcome is lower subscription drain for the same completed unit;
the verified outcome here is only lossless, smaller coordinator delivery.
