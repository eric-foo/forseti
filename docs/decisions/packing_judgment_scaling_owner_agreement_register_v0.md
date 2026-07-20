# Packing And Judgment Scaling Owner Agreement Register v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (owner agreement register)
scope: >
  Records owner-stated agreements, locked decisions, uncontested proposals, and
  open forks from the 2026-07-21 Packing Spine / judgment-scaling deliberation,
  so future lanes neither re-derive nor overclaim them.
use_when:
  - Continuing Packing Spine adjudication or implementation work.
  - Commissioning the judgment-scaling (pull-to-assemble / hierarchy) architecture design.
  - Checking whether a Packing or judgment-scaling direction was owner-agreed, merely proposed, or still open.
authority_boundary: retrieval_only
open_next:
  - docs/research/packing-phase/README.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
  - docs/research/judgment-spine/evidence_condensation_hierarchy_deferred_direction_v0.md
  - forseti-harness/judgment/creator_audience.py
branch_or_commit: claude/packing-spine-columnar-compiler-8b37a9 @ 5134bc65 (session base 12c3fde4)
stale_if:
  - The Packing fork (A/B/C) is decided and its implementation lands.
  - A judgment-scaling architecture artifact supersedes the directional entries.
  - The owner reverses any recorded entry in a later turn or artifact.
```

## Provenance And Claim Tier

- Source: owner statements in the 2026-07-21 working session continuing
  `packing_spine_columnar_compiler_continuation_handoff_v0` (session base HEAD
  `12c3fde4`).
- Evidence tier: chat-first owner direction. This register is a faithful record,
  not proof; if an entry is disputed, reconfirm with the owner instead of
  treating this file as settlement.
- Tiers below are ordered by strength: Locked > Owner-agreed > Uncontested >
  Directional > Proposed-unreviewed > Open.

## Locked (explicit owner selection)

- **Alias policy: one alias per exact-normalized-duplicate group.** Current
  `_grouped_rows` behavior stands; the response compiler already expands each
  alias to every member durable evidence ID, so compiled claim support stays
  cue-precise. (Owner selected "Keep group alias".)
- **Fork decided: Option B (thin Packing compiler + creator-audience
  adapter).** Owner, 2026-07-21: "okay proceed B, success implement."
- **Implementation granted for the B slice (2026-07-21, superseding the
  earlier "Adjudicate only" hold).** Same owner statement as above. The grant
  is bounded to the columnar packing slice: the `forseti-harness/packing/`
  module, the `build_creator_audience_prompt` wiring, and its focused tests.
  No other runtime work is authorized by it.

## Owner-Agreed (stated in session)

- **Whole-transcript aliases stay forbidden.** One alias covering a transcript
  would falsely imply every line supports every claim. ("i agree that one tag
  cant be for one transcript.")
- **Judgment is pull, not push — with the split: pull to assemble, freeze to
  judge.** A Judgment-side agent (subagent-like, holding a lake query
  capability) owns evidence demand; the final judgment call still consumes a
  frozen, packed bundle so citations compile exactly. ("i agree", with
  smallest-complete emphasis.)
- **Blind determinism is scoped to backtesting.** Forward-looking/nowcasting
  judgment does not need blindness; it needs "recorded, not blind": a frozen
  judged evidence set plus a retrieval trail. Packer determinism (same input →
  same bytes) is retained regardless.
- **Audit provenance is not sent to the model; it stays one lookup away.**
  Aliases + text + salience go to the model; durable IDs/paths stay in the
  facilitator manifest; the compiler re-expands. Support topology (an alias
  spanning multiple source items) stays model-visible because it changes what
  the model may claim.
- **Prompt caching is deferred to the API migration.** Judgment currently runs
  on subscription where caching is harness-managed and uncontrollable; the
  lever (cached method-deck prefix, Batch API discount) activates when bulk
  judgment moves to API calls. Keep the existing static-first / evidence-last
  prompt shape, which is already cache-optimal. ("well its API so thats for
  future.")
- **Condensation is required at scale.** Raw-dump prompts fail on cost and on
  mid-context accuracy loss ("lost in the middle"); condensation via
  mini-judgment rounds is the owner's chosen direction. ("thats my exact
  take.")
- **The level shape makes sense: mini-rounds → topic rounds → final judgment,
  plus audit descent as the fourth surface.** ("the 3 level thing makes sense
  (well 4 with audit).")
- **Columnar packing is the might-as-well bottom layer.** Lossless, cheap,
  serves every future level (including packing `judged_claim` tables); not the
  scaling strategy itself. ("true its mechanical so its a might as well";
  "i agree with your 4.")
- **The existing lake addressing/map is the initial query surface.** Owner
  notes the lake map (non-SQL, address-based) already exists; no new warehouse
  implied. ("technically we do have a query surface (not sql yet though) the
  lake map.")
- **A SQL index over the lake is being set up as a parallel effort** (owner
  fact, 2026-07-21: "we're also setting up a sql index as well"). Pull-loop
  design may assume address-based enumeration now and SQL-queryable lookup
  soon; ranked/semantic retrieval remains deferred behind the
  enumeration-stops-scaling trigger.
- **Confirmation-seeking retrieval is a risk to avoid, not a mechanism to
  build.** Mitigations when pull lands: retrieval log recorded as provenance
  plus coverage obligations in the pull method. (Owner: "that means we dont do
  a confirmation seeking retrieval. that makes sense.")
- **Smallest-complete pull starts on lake enumeration** (agent enumerates
  lanes for a subject and reads records; the agent is the relevance judge);
  content-based/ranked retrieval is a trigger-gated upgrade. (Owner: "no
  worries then.")
- **Freezing split ratified.** The freeze event (fixing the working set,
  bundle id + hash) belongs to the assembly side (evidence binding today, the
  pull loop later); the frozen form and its verification (canonical bytes,
  deterministic serialization, rehydration checks) belong to the Packing lane.
  (Owner: "that makes sense.")
- **Hierarchy machinery is explicitly deferred, with the design preserved.**
  Owner: "i dont think we need that machinery now, but in future for sure
  write it down somewhere that when we want to improve / go to GT etc it would
  be there present." The design record lives at
  `docs/research/judgment-spine/evidence_condensation_hierarchy_deferred_direction_v0.md`.

## Uncontested (presented earlier, not disputed; owner asked these be recorded as presumed agreement)

- Citation capability must survive any compression exactly (handoff Drift
  Guard; relied on throughout without objection).
- Packing serializes an already-selected evidence set; it never selects,
  labels, scores, or repairs (layer boundary).
- Packing-slice technical locks as proposed: encoding-only change (the
  `creator_audience_compact_judgment_view_v3` field set is unchanged); dense
  tables per evidence kind × multiplicity class; a `packing_columnar_view_v0`
  envelope with a deterministic deep-equal rehydration contract that fails
  loud on version/column/shape drift; packer core payload-agnostic with a thin
  creator-audience adapter; package placement `forseti-harness/packing/`.
- First fixtures: synthetic TikTok + Instagram bundles in unit tests, no live
  capture; byte measurement comes from a generated fixture; no size-savings
  claim (including the earlier ~54% figure) until reproduced that way.
  Measured 2026-07-21 in
  `forseti-harness/tests/unit/test_packing_columnar_v0.py`: -34.0% (scaled
  TikTok fixture, 15 evidence rows), -9.5% (Instagram fixture), and +8.3%
  (larger) on a tiny one-row-per-table fixture where the column headers
  dominate. The ~54% figure was not reproduced and must not be cited.
- Mini-round outputs reuse the existing claim shape (statement + representative
  and full support aliases, compiled and validated) — no second citation
  system; the condensation act is a descriptive Judgment round, owned by
  Judgment, never by Packing.
- Derived claims are labeled as their own evidence kind (e.g. `judged_claim`)
  when consumed by a higher level; second-hand evidence is never disguised as
  observed evidence.
- Hierarchies need a cross-partition contradiction surface; per-partition
  rounds cannot see contradictions that span partitions.
- Lineage expansion is transitive: a final claim unwinds through intermediate
  claims to raw lines.
- Option B (thin Packing compiler + creator-audience adapter) was the standing
  recommendation for the fork; the owner locked it on 2026-07-21 (see Locked).

## Directional (shape agreed; deliberation required before design lock)

- **Hierarchical mini-judgment architecture.** Owner: "the hierachy thing im
  guessing (But need more deliberation / explanation on that, surface looks
  nice though)." Direction is accepted for further design work; partition
  scheme, `judged_claim` contract, contradiction-pass mechanics, round
  orchestration, and validation design are all undecided and owed a dedicated
  architecture artifact before any lock.

## Open Decisions

- Commissioning of the judgment-scaling architecture artifact (pull loop +
  hierarchy design).
- Retrieval-surface upgrade beyond lake-map enumeration (future, trigger-based).
- Caching implementation at the API migration (future; no action now).

## Non-Claims

- No runtime implementation, validation, readiness, performance, or size claim
  is made or implied by this register.
- No architecture named here is owner-*accepted* beyond the tier stated;
  Directional and Proposed entries are explicitly not agreements.
- This register records owner statements; it does not itself authorize edits,
  implementation, or supersession of any owning source.
