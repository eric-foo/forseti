# Data Capture Spine — Posture Vocabulary Enforcement Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Candidate proposal (authored from the JSG-01 source-side lane) to enforce the
  Data Capture Spine's EXISTING closed posture vocabularies at the source — after
  first untangling the currently-overloaded cutoff_posture field — plus add a
  recomputation-bound hash basis. Routes execution/ratification to the Data
  Capture lane.
use_when:
  - Deciding whether (and how) to close the Data Capture posture vocabularies at write-time.
  - Preparing the Data Capture lane change that JSG-01 source-side will consume.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca-harness/source_capture/models.py
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md
  - docs/product/jsg01_source_side_receipt_translator_v0.md
branch_or_commit: main @ f9b05e6 (worktree dirty; controlling sources untracked)
stale_if:
  - The Data Capture lane accepts, amends, or rejects this proposal.
  - core_spine_v0_data_capture_spine_obligation_contract_v0.md changes Ob.9/Ob.10/Ob.11/Ob.15 vocabularies.
  - orca-harness/source_capture/models.py or source_quality.py changes the posture fields, VisibleFact model, or _source_time fallback.
```

- Status: `PROPOSED_CANDIDATE_INPUT_PATCHED_POST_REVIEW`
- Lane: authored from the JSG-01 source-side lane; **execution + ratification + DCP belong to the Data Capture / capture-build lane**, not here.
- Authorizes: nothing. Not implementation, not a schema change, not a contract amendment, not validation.

## Patch history

- **v0 (initial):** proposed closing cutoff/archive/re-capture postures to the
  contract's vocabularies + adding `hash_basis: str`; treated migration as a
  generic later code concern; claimed JSG-01 could then read directly.
- **v0 patch (this revision), from independent adversarial review**
  (`docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md`,
  reviewed-target SHA256 `2E5D05B8F8366711F4A749B68664E0034BED7C8460B629EF1BA881AED04D5FA5`,
  `recommendation: patch_before_acceptance`, broadened read-pack incl. implemented
  code/tests/packets). Incorporated: AR-01 (JSG-01 overclaim downgraded), AR-02
  (off-vocabulary existing data named; migration bound pre-ratification), AR-03
  (`source_quality.py` time-fallback collision named in the impact surface), AR-04
  (`hash_basis` semantic contract specified), AR-05 (Ob.10 status/value
  representation pinned). The review confirmed the core design held
  (value-vs-sufficiency boundary, no materiality enum in Capture, `access_posture`
  left open, lane discipline).

## Headline finding (resizes this proposal)

The implemented `cutoff_posture` field is **overloaded today** — it is not
currently a cutoff posture at all:

- existing tests/packets store capture-context strings in it — e.g.
  `known_fact("local cutoff posture")` (`orca-harness/tests/unit/test_source_capture_packet.py:324-330`)
  and `"local JSON/file state supplied…"` /
  `"local markdown artifact state supplied…"`
  (`orca-harness/reports/source_capture/slot3_reddit_batch1_packet_dry_run_2/manifest.json:153-156`,
  `…_post_patch_dry_run/manifest.json:151-154`);
- `source_quality.py` reads it as a **time fallback**
  (`_source_time` → `cutoff_posture`, `orca-harness/source_capture/source_quality.py:434-442`).

So this is not "tighten a free-text field to its contract enum." It is
**"untangle a field doing three jobs, then close it."** That untangling +
migration is the bulk of the work and must precede closure. This strengthens the
case for the change — the foundation field is unreliable today — but it is bigger
than the initial sketch.

## Problem (one paragraph)

The Data Capture Spine records source postures (cutoff, archive, re-capture) as
free-text `VisibleFact.value` strings. The obligation contract already defines
closed vocabularies for most (Ob.9 cutoff; Ob.10 archive; Ob.15 re-capture), but
the schema does not enforce them, and `cutoff_posture` is additionally overloaded
(above). In a multi-agent system every reader re-interprets the same free text and
can diverge. The fix is to enforce the contract's existing vocabularies once, at
write-time — after untangling current misuse — so every reader gets a clean value.
This proposal invents no vocabulary; it enforces what the contract owns and flags
what the contract does not yet close.

## Proposed changes (concrete)

| Target | Now | Proposed | Vocabulary source | Note |
| --- | --- | --- | --- | --- |
| `PacketTiming.cutoff_posture` | `VisibleFact` free-text, **overloaded** (capture-context + time fallback) | **(1) untangle** non-cutoff usage; **(2)** then when `status==known`, `value ∈ {pre_cutoff, post_cutoff, mixed, unknown}` | **Ob.9** | requires migration + `source_quality.py` fix first (see below) |
| `archive_history_posture` | `VisibleFact` free-text | when `status==known`, `value ∈ {archived, attempt_failed}`; `not_attempted`/`not_applicable` carried by **status** | **Ob.10** | exact representation pinned below (AR-05) |
| `re_capture_relationship` | `VisibleFact` free-text | when `status==known`, `value ∈ {supersede, supplement, conflict, mixed}` | **Ob.15** | |
| `PreservedFile` | `sha256` only | ADD `hash_basis` with a **recomputation-bound** contract (below, AR-04) | AR-03/AR-04; aligns w/ `case_models.py` `EvidenceUnit.hash_basis` | not an arbitrary string |
| obligation contract Ob.9/Ob.10/Ob.15 | vocabularies illustrative | state as **closed/enforced** so contract and schema agree | — | doctrine edit (DC lane) |

### Ob.10 status/value representation (pinned — AR-05)

Ob.10's four-value posture is represented as a union of `VisibleFact.status` and
`value`: `known/archived`, `known/attempt_failed`, `not_attempted/<reason>`,
`not_applicable/<reason>`. If the DC lane rejects this representation it must bind
a different one before ratification.

### `hash_basis` contract (AR-04)

`hash_basis` must identify the recomputation basis **in relation to the preserved
bytes** (e.g., names `relative_packet_path` and what slice/encoding the `sha256`
covers) **or an owner-bound acquisition receipt** — not arbitrary prose. Minimum
end state: a source-visible basis that lets a reviewer know what bytes/receipt
coverage the hash represents. An unconstrained string recreates the
"hash-shaped string" problem under a new field name and does not close AR-03.

## Implementation impact surface (AR-03)

Closing the value vocabulary touches more than `models.py`:

- `orca-harness/source_capture/models.py` — schema enforcement.
- `orca-harness/source_capture/source_quality.py` — **`_source_time` must not
  populate `source_or_snapshot_time` from the closed `cutoff_posture` enum**
  (a posture is not a time). Re-source it from timing fields or explicit unknown.
- `orca-harness/source_capture/packet_assembly.py` — posture-honesty validator
  uses statuses; confirm the status/value split holds.
- existing tests + packets — see migration.

## Pre-ratification conditions (AR-01 / AR-02)

The DC lane must bind these before treating the proposal as acceptance-ready
(this proposal names them; it does not implement them):

1. **Migration decision (AR-02).** The observed off-vocabulary `known`
   `cutoff_posture` values above encode local-packetization limitations, not bad
   data. Bind how they map — likely `unknown` value + `unknown_with_reason`/limitation,
   or a **separate capture-context field** — and a compatibility stance for the
   named tests/manifests. Migration is a pre-ratification decision, not a generic
   later code concern.
2. **`source_quality.py` collision (AR-03)** resolved or explicitly scoped.
3. **`hash_basis` contract (AR-04)** bound, not just a `str` field added.

## Boundary that keeps this clean (value vs. sufficiency) — held

- **Close the value vocabulary at Capture** — *what posture it is* is capture-owned
  (Ob.9/Ob.10/Ob.15). Not pushing Judgment into Capture.
- **Leave sufficiency downstream** — *good-enough-to-clear, and at what claim grade*
  stays with JSG-01 / owner (the SP-6 visibility-sufficiency threshold residual).
- **No comparison/materiality verdicts in the capture enum** — archive
  corroborated/diverged depends on *material* divergence, a downstream Judgment.
  Record raw comparison facts only.

## What NOT to close (flagged, not guessed) — held

- `access_posture` (Ob.11) is **prose, not a closed set** — do not force a closed
  vocabulary; it needs a separate capture-lane vocabulary decision. Flag, don't invent.
- `source_locator`, `actor_audience_context` are inherently open identity facts.

## Relationship to JSG-01 (downgraded — AR-01)

These closures are **upstream inputs** to JSG-01 source-side, **not** a direct
read. After this lands, JSG-01 still needs a bounded derivation rule (or a named
residual) for `source_visibility_posture` (SP-6), because SP-6 is **composite** —
mapped from archive-attempt record, acquisition-receipt capture scope, and
re-capture relationship — and `access_posture` remains free-text. So this reduces
per-reader interpretation for cutoff/archive/re-capture, but does **not** by itself
produce SP-6 or fully unblock JSG-01. JSG-01 stays frozen; the residual SP-6
derivation is a Data-Capture/ECR decision, not closed by this proposal.

## Non-claims

Candidate input only. Not a schema change, not a contract amendment, not
ratification, not validation, not implementation authorization. Execution,
ratification, the `direction_change_propagation` receipt, the migration, and the
code/migration review belong to the Data Capture / capture-build lane. Does not
unfreeze JSG-01. Does not authorize runtime, tests, commits, or PRs. The patched
proposal post-dates the review above; a light re-check that these closure
conditions are met (not a full new adversarial round) is the proportionate next
step before DC-lane acceptance.
