# Judgment Quality Promotion Operating Model v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Case-agnostic operating model (conductor) that sequences Judgment Spine gates JSG-01 through JSG-10 into a runnable, receipt-verified path, using mechanical gate predicates, a total fail/blocked transition function, an explicit by-hand isolation cap, and named run lifecycle states, without computing judgment quality and without restating gate semantics owned elsewhere.
use_when:
  - Running or planning a case through the Judgment Spine gates end to end.
  - Deciding which run lifecycle state a partial or held run is in.
  - Checking what a partially completed or by-hand run can and cannot claim.
  - Routing an agent from one gate to the next without inventing gate ownership.
authority_boundary: retrieval_only
no_authority_invariant: >
  This conductor sequences gates and verifies receipts. It does not authorize
  model execution, probe execution, scoring, fixture admission, or claim
  promotion, and it does not compute judgment quality, recognition verdicts, or
  scores. Those remain owned by the controlling sources, the deterministic
  scorer, the memorization-probe artifact, and human authorization gates.
open_next:
  - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  - forseti/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md
  - forseti/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - .agents/workflow-overlay/product-proof.md
  - .agents/workflow-overlay/validation-gates.md
input_hashes:
  AGENTS.md: D5F688AA91412D105A60E907F9647C56CB4A59303E955058AA313665D88D1566
  .agents/workflow-overlay/README.md: 7A30709D6011BD3F6458E926570B7164B91C7F3BF8BAE7DBD5A612A08DE81FDA
  .agents/workflow-overlay/source-of-truth.md: D985345F27389D21640E116B74FC4F145C5836C64331295E41D6D47AFBED8DF1
  .agents/workflow-overlay/source-loading.md: C22A373C786A06D91A2102858FFF58B29BBF428AEEBB7F4C5C554D3E97547347
  .agents/workflow-overlay/product-proof.md: AD1724202841D616F74494B22E3659D7987CC875BD36BF0F23B12C210E4B19C4
  .agents/workflow-overlay/validation-gates.md: 689081A755FE88AAF140BD7C368B9F428856F160B858B5D0F5877B33FE258CEB
  docs/product/judgment_spine_evidence_ladder_architecture_v0.md: 79F6696DD50BE3FDCB574FD6AED4FE0761C6335029BFDBE39B51F104F4AD16CF
  docs/product/judgment_spine_gate_ownership_map_v0.md: 9A07DE8D61249D26DF1DB4E66FE918893D74FFF4970D2B9BABD1C0F97878CE9F
  docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md: ED146BEB5767EFDDA3E979AA798CA5CB044A896421872B02FBDF03615E4E6E07
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61
  docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md: 7291EF5E7C19A3514AE2B0E91D9FDD8917D7C4BFF039726FCD6075E55F73C1A4
  docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md: 0459C21E7083CD9295290170692BE47A85CBCD24B42B9B0C6E9D7ACF29AC850A
  docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md: 0CE6E9584F4F1C4716559A654870AF43EBED3E5D53D3279AB658993B7DE1C2AE
  docs/workflows/orca_repo_map_v0.md: 7E78B27B4014A98BC95D340D3A153B1DD624EA8F7A285988CF7ECC4766DCE46A
  forseti-harness/scoring/band_scorer.py: D54DCD2CB34A8158232E1A428F70A1F3F182052529D7BC8E5293D5F21A67E1E3
  forseti-harness/runners/run_case.py: F04BABF1EF4BAFE187E83552E3A3066DEBC47CAD92F5186011BD7B2925CE52AD
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 7962ae8ad6661b637940735b49ce693f832da106 (working tree dirty — concurrent-lane changes; see baseline note)
input_hash_baseline_note: >
  Recomputed 2026-06-09 during the Round-17 delegated-review patch against the
  current working-tree bytes (the reviewed bundle's accepted source set). The
  worktree remains dirty (concurrent-lane changes), so these still pin
  working-tree bytes, not a clean committed baseline. Six overlay/navigation
  files (AGENTS.md, README.md, source-of-truth.md, source-loading.md,
  validation-gates.md, orca_repo_map_v0.md) drifted from the prior pins; the
  Judgment Spine owner sources and harness files matched. Recompute before any
  strict reliance.
downstream_consumers:
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/research/judgment-spine/manifest_v0.md
  - docs/product/judgment_spine_gate_ownership_map_v0.md
  - future Judgment Spine case runs and case run-state records
stale_if:
  - docs/product/judgment_spine_evidence_ladder_architecture_v0.md changes claim tiers, closeout states, weakest-cleared-gate rule, sub-floor rule, or receipt minima.
  - docs/product/judgment_spine_gate_ownership_map_v0.md changes gate ownership, required receipts, or gate dependencies.
  - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md changes JSG-08 satisfaction states or claim caps.
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md changes isolation or sealed-output gate semantics.
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md changes probe gate interpretation semantics.
  - A later accepted contestant-execution runner, scoring route, or operating-model artifact supersedes this conductor.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_judgment_quality_conductor
  edit_permission: docs-write
  target_scope:
    - docs/product/judgment_quality_promotion_operating_model_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/research/judgment-spine/manifest_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
  path_collision_checked:
    path: docs/product/judgment_quality_promotion_operating_model_v0.md
    existed_before_write: no
  dirty_or_untracked_notes:
    - The conductor target was absent before this write (owner-deferred until now).
    - Controlling product docs and several overlay files are untracked or modified in this worktree; input_hashes pin current worktree bytes.
```

## Purpose

This artifact is the Judgment Spine **conductor**: the connective tissue that
sequences the owned gates `JSG-01` through `JSG-10` into a path a future agent
can actually walk a case through. The gate semantics, claim vocabulary, and
receipt minima already exist in the evidence ladder, the gate ownership map, the
`JSG-08` owner contract, and the harness contracts. What did not exist was the
operating model that orders those gates, checks each gate's receipt, and routes
between them. This conductor supplies exactly that and nothing more.

It re-opens the owner-deferred operating-model spine. It holds the full Judgment
Spine discipline at minimal footprint by **routing to** the owner sources rather
than restating them. It assembles and verifies receipts; it never computes
judgment quality.

## No-Authority Invariant

The conductor, and any LLM acting as conductor, is supporting cast. It is the
subject or the assistant. It is never the gavel.

```yaml
no_authority_invariant:
  conductor_may_only:
    - evaluate a mechanical predicate over an existing receipt field
    - advance, halt, or hold per the transition function
    - record the resulting run lifecycle state and route to the next gate owner
  conductor_must_never:
    - compute judgment quality
    - decide a memorization recognition verdict
    - compute, revise, or repair a score
    - author a missing gate receipt to escape a halt
    - mint, rename, merge, or split any claim tier or closeout_state
    - authorize a model run, probe run, scoring, fixture admission, or promotion
  authority_owners:
    memorization_recognition_verdict: read from the JSG-05 probe artifact (memorization_probe_protocol)
    score: read from the deterministic scorer output (phase_1_infrastructure / band_scorer)
    gate_semantics_and_ownership: gate ownership map and each gate's owner contract
    claim_caps_and_closeout_vocabulary: evidence ladder
    run_fixture_promotion_authorization: human / owner gate
```

This is **Invariant A**. A run that requires the conductor to exercise judgment
to clear a gate has not cleared that gate.

## Route, Don't Restate

This is **Invariant B**. The conductor owns only routing and lifecycle
constructs: the gate sequence, the predicate-binding rule, the transition
function, the by-hand cap rule, and the run lifecycle states. It owns no gate
semantics and no claim vocabulary. Every predicate checks an owner-produced
receipt field; the conductor cites the owner source and never duplicates or
contradicts it. If this conductor and a controlling source disagree, the
controlling source wins and this conductor is stale for that point.

## Isolation Topology

```yaml
isolation_topology:
  orchestrator_thread:
    role: reads sources, evaluates predicates, sequences gates, records run state
    authority: none
  isolated_child_runs:
    - gate: JSG-05 memorization probe
      isolation_owner: memorization_probe_protocol + contestant_no_tools_execution_contract
    - gate: JSG-06 contestant blind judgment
      isolation_owner: contestant_no_tools_execution_contract
    rule: child runs must be isolated from orchestrator context; the orchestrator must not leak packet, ledger, or outcome material into them
  deterministic_scorer:
    gate: JSG-07
    owner: phase_1_infrastructure_architecture / band_scorer
    rule: code computes the score; the conductor reads it
  human_authorization_gates:
    - run authorization
    - fixture admission
    - claim promotion
    rule: owner decides; the conductor never self-authorizes
```

The conductor coordinates these roles. It never collapses any of them into
itself.

## Gate Sequence And Mechanical Predicate Table

**Seam 1 — predicate-binding rule.** Every gate's clear-condition is expressed
as **either** (a) an exact source-owned receipt field path and an allowed value,
**or** (b) a read of an owner-produced status field. A gate is `cleared` only
when the named field exists and equals an allowed value; this is evaluable
without judgment. A semantically loaded concept (for example "valid source
identity") is **not** clearable by the conductor unless the controlling owner
source defines the exact field that carries it. Where the owner source does not
yet name a checkable field or value, the gate predicate is
`indeterminate_until_authored`: the conductor treats the gate as **not cleared**,
halts, and names the missing owner-schema field as the blocker. The conductor
never clears on a paraphrase and never invents a field.

**Receipt-provenance sub-rule (non-self-certification).** This applies the
Orca-general **Receipt-field provenance gate**
(`.agents/workflow-overlay/validation-gates.md`), which is the single source of
the principle: a receipt field is gate-clearing only when owner-produced and
provenance-bound or independently verifiable, never on a self-asserted value;
absent that, the check is `indeterminate_until_authored`. Conductor-specific
application: for the machine- or run-produced gates (JSG-04, JSG-05, JSG-06,
JSG-07), the predicate must check the provenance the owner contract requires (for
example, `contestant_no_tools_execution_contract_v0.md` Receipt Provenance
Boundary) — an owner-produced authorized status that binds provenance, or the
explicit auditable provenance fields — not the bare `proven`/`pass_valid` field.
Where that provenance is not yet producible (for example, no
contestant-execution runner exists), the predicate is
`indeterminate_until_authored` / not cleared, which caps the run per Seam 3.

This rule is what makes Seam 1 mechanical and what keeps Invariant A and
Invariant B intact.

| Gate | Routed semantics owner | Receipt | Mechanical clear-predicate | If owner field/schema absent |
| --- | --- | --- | --- | --- |
| JSG-01 | data-capture obligation contract + core-spine boundary own the source-identity obligation and declare the **ratified** JSG-01 source-side ECR field schema (SP-1/2/3/6) plus the **ratified JSG-01-scoped `EvidenceUnit` binding contract** (2026-06-12); packing interface owns `pre_decision_status` | packing final status + ECR source-side postures + `FinalizationReceipt`, composed onto the case packet's bound evidence unit by `forseti-harness/evidence_binding/` | `pre_decision_status` present and set to an allowed *cleared* pre-decision value (not `excluded` or an uncertain/placeholder value), read through the SP-5 finalization chain. The finalization-provenance subpredicate — that the final `pre_decision_status` was finalized by the Judgment authority (AR-01, **resolved** — operator-for-now, a distinct cross-family act; see `docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md`) — evaluates via the validate-only consumer (`forseti-harness/schemas/finalization_models.py`, `a37f896`; producer acting half `forseti-harness/runners/run_finalization_receipt.py`): cleared **only** on a single current, cross-family, binding-consistent `FinalizationReceipt` whose recorded `judge_model_family` matches the run's judge family — a mismatched or placeholder-recorded judge family **blocks** until a correction receipt re-points it (append-only). The source-identity, inspectability, timing/cutoff, and source-visibility subpredicates route to the **ratified** owner fields and allowed values (core-spine boundary: SP-1 `source_identity_state` ∈ {`resolved`, `family_only`}; SP-2 `inspectability_state == inspectable_verifiable`; SP-3 timing `== pre_cutoff` carried over the producer's `PacketTiming.cutoff_posture`; SP-6 `source_visibility_posture` per the ratified decision-C grade) and **evaluate determinately** via the built derivers (`forseti-harness/ecr/deriver.py`) composed onto the bound case-packet evidence unit by the ratified binding (`forseti-harness/evidence_binding/`; SP-2/SP-3 read at the bound slice's row; no aggregate verdict is composed — this conductor combines the subpredicates). Per the unfreeze act's D2 consumption (option b): D2 stays deferred; the corroborated SP-6 tier is unreachable and archive+current packets land on named residuals — residuals do **not** clear (conservative; never a pass) | **UNFROZEN** (owner dated act 2026-06-12 — `docs/decisions/jsg01_unfreeze_decision_v0.md`; first carrying packet `forseti-harness/cases/product_learning/jsg01_binding_assembly_proof_v0`): evaluable over a bound case packet; any subpredicate whose owner field is absent or unresolvable routes to not-cleared per Seam 3 (missing evidence is not a pass). **JSG-01 clears no case until a separately authorized run evaluates one** |
| JSG-02 | evidence ladder + product-proof zero-spoiler boundary + packing interface | frozen participant packet | the participant-packet freeze receipt is present and valid per the owner-enumerated required receipt fields (the conductor checks owner-enumerated field presence/validity, not holistic completeness), including the product-proof zero-spoiler boundary for participant-facing surfaces and the packing interface's participant-visible boundary / leakage-spoiler admission checks. The conductor must not enumerate the owner-owned spoiler list locally. A bare present `participant_packet_hash`, or a hard-marker-only packing pass that leaves a product-proof-covered participant-facing leakage/spoiler issue unresolved, does **not** clear. A recorded leakage/spoiler block-class failure routes to contaminated/blocked (Leakage) | semantic-leakage subpredicate is `indeterminate_until_authored` (owner leaves it to operator/review) until its admission fields are authored |
| JSG-03 | band-input labeling rubric + packing interface | frozen FacilitatorLedger (Case) | the frozen FacilitatorLedger receipt is present and valid per the owner-enumerated required receipt fields (the conductor checks owner-enumerated field presence/validity, not holistic completeness), including the packing interface's frozen-ledger requirements and any rubric quarantine handling; the conductor must not enumerate ledger-content fields locally. A bare present `ledger_freeze_hash` does **not** clear when the owner-required frozen-ledger receipt is incomplete or invalid | `indeterminate_until_authored` for any required ledger field whose owner schema is not yet authored |
| JSG-04 | contestant no-tools execution contract | `contestant_execution_isolation` + authorized live-execution provenance | `isolation_result == "proven"` **and** the contract's auditable live-execution provenance is bound (separate owner authorization; production by the live runner; accepted endpoint; out-of-band operator record binding provider, endpoint, UTC timestamp, exit status, console output, `prompt_hash`, `raw_response_hash`). A bare computed `proven` does **not** clear (receipt-provenance sub-rule) | not cleared; with no live runner, by-hand receipts cannot bind provenance, so `indeterminate_until_authored` / capped per Seam 3 |
| JSG-05 | memorization probe protocol + no-tools contract provenance boundary | probe artifact | gate-interpretation `== pass_valid`, **read from the JSG-05 artifact, not the scorer**, **and** bound by the same auditable live-execution provenance as JSG-04. A bare computed `pass_valid` does **not** clear (receipt-provenance sub-rule) | not cleared / `indeterminate_until_authored` until authorized live provenance is bound; only the owner-defined confirmed recognition state with proven isolation routes to contaminated/blocked via Seam 2, while caveated or ambiguous probe outcomes route as not-cleared/quarantine under the owner protocol |
| JSG-06 | no-tools contract blind-judgment section (isolation) + evidence ladder / gate map sealed-output receipt | sealed blind judgment | JSG-04 cleared **and** the blind-judgment run has `isolation_result == "proven"` with inherited auditable live-execution provenance **and** the owner-required sealed blind judgment hash is present per the gate map and evidence ladder. `sealed_before_reveal` remains a **JSG-08** receipt field, not a JSG-06 clear-condition; the seal-before-reveal property is enforced at JSG-08 | not cleared / `indeterminate_until_authored` until the owner-required sealed-output receipt and inherited no-tools provenance are present |
| JSG-07 | phase-1 infrastructure + packing interface | scoring result | the scoring receipt is present and valid per the owner-enumerated required receipt fields (the conductor checks owner-enumerated field presence/validity, not holistic completeness), including the phase-1 infrastructure version/hash guardrails, the packing interface's frozen-input and deterministic-checking boundary, and the scorer-produced `ScoringResult` / `FailureEvent` outputs. Authenticity may clear only through an owner-produced or independently verifiable scoring provenance/hash check; the conductor must not define its own re-derivation discriminator or treat a hand-authored result as clearing. Because the current scorer output includes run-generated identifiers, timestamps, and failure-event IDs, a naive rerun equality check over `scoring_result_hash` is **not** an owner-supported gate predicate. An owner-produced `FailureEvent` with `severity == "blocking"` prevents clearing and routes by the transition function; absence, missing run metadata/hash/version, or a bare `score_blocked` for a missing input routes to **not-cleared** (Seam 3). The scoring-integrity-vs-admission **contamination** discriminator is `indeterminate_until_authored`: the scorer's `FailureEvent.failure_type` is an unconstrained free-text field, so no exact owner value yet distinguishes an affirmative scoring-integrity breach from an admission/absence state | not cleared until the owner-required scoring receipt, scoring provenance/hash check, and failure-event handling are present and valid per the owner sources; a `FailureEvent.severity == "blocking"` routes by the transition function; the scoring-integrity contamination discriminator stays `indeterminate_until_authored` pending an owner enum; missing/absent scoring evidence routes to not-cleared |
| JSG-08 | reveal/calibration owner contract | `jsg_08_reveal_calibration_receipt` | the owner contract's Required Receipt Fields are complete for the case-specific durable receipt, `receipt_status == score_linked_outcome_calibration`, and `sealed_blind_output.sealed_before_reveal == yes`, for judgment-quality strength. The conductor checks completeness by reference to the owner contract and must not enumerate the receipt fields locally. A bare `receipt_status` value without the owner-required supporting receipt does **not** clear (receipt-provenance sub-rule: `receipt_status` is self-asserted). `sealed_before_reveal == no` is an affirmative seal-ordering breach and routes to contaminated/blocked; `unknown`, a weaker `receipt_status`, or any owner-required field named-missing caps lower / not cleared per the contract | not cleared at judgment-quality strength |
| JSG-09 | evidence ladder `judgment_spine_claim_classification` + validation gate | classification record | classification record present and complete per the ladder's `judgment_spine_claim_classification` schema, and `claim_cap` is owner-consistent by reference to the ladder-owned cap rules for the recorded `closeout_state` plus the ladder weakest-cleared-gate rule where applicable. The conductor must not enumerate classification fields or cap values locally | terminal route (Seam 5) |
| JSG-10 | evidence ladder closeout vocabulary + validation gate | named closeout | `closeout_state` present, drawn from the ladder vocabulary, and `claim_cap` owner-consistent by reference to the ladder-owned cap rule for that recorded `closeout_state` plus the ladder weakest-cleared-gate rule where applicable. The conductor must not enumerate cap values locally and must not default every state to weakest-cleared | terminal route (Seam 5) |

Note on JSG-05 versus JSG-07: the deterministic scorer emits
`memorization_probe_result="not_run"` as a fixed field; the conductor must read
the recognition verdict from the **JSG-05 probe artifact**, never from the
scorer output. A present scoring result does not imply a cleared probe.

## Transition Function

**Seam 2 — total fail/blocked transitions.** The conductor evaluates gates in
order. The transition function is total over the full outcome alphabet: every
gate, including the closeout gates, has exactly one defined behavior for each
outcome — cleared, contaminated-or-blocked, held (JSG-08 `receipt_status == absent`, a lifecycle annotation over not-cleared),
or not-cleared/indeterminate — evaluated in that precedence order.

```yaml
transition_function:
  evaluate_in_order: [JSG-01, JSG-02, JSG-03, JSG-04, JSG-05, JSG-06, JSG-07, JSG-08, JSG-09, JSG-10]
  outcome_precedence: [cleared, contaminated_or_blocked, held, not_cleared_or_indeterminate]
  on_gate_G:  # classify the gate outcome into exactly one branch, in the precedence order above
    if_cleared: advance to the next gate
    elif_contaminated_or_blocked:
      trigger: a gate's owner receipt reports an AFFIRMATIVE invalidity or breach value — JSG-08 `receipt_status == contaminated_or_invalid` or `sealed_before_reveal == no`; `isolation_result == violated`; a JSG-02/JSG-03 packing or product-proof leakage/spoiler block-class failure; or the JSG-05 owner-defined confirmed recognition state with proven isolation (the JSG-07 scoring-integrity contamination trigger is **withheld as `indeterminate_until_authored`** — see the JSG-07 row — because `FailureEvent.failure_type` is unconstrained; a `FailureEvent.severity == "blocking"` halts as not-cleared, not contamination). It fires only on a positive owner-reported invalidity value, read from the routed owner source rather than locally re-derived
      note: this must be an affirmative owner-reported invalidity value, so the routing decision stays a mechanical field read (Invariant A). Absence, not-yet-authored provenance, unresolved status, by-hand execution with no auditable runner, `sealed_before_reveal == unknown`, JSG-05 ambiguity, or JSG-05 fail-with-unproven-isolation caveat is NOT contamination; it routes to else_not_cleared_or_indeterminate and caps via the ladder-owned closeout/cap rules. Contamination can poison gates that already mechanically cleared, so it must NOT use the ordinary weakest-cleared-gate cap
      action:
        - halt at G; do not advance
        - resolve the closeout through JSG-09/JSG-10 using the ladder-owned `blocked_or_contaminated` closeout_state and its owner cap rule
        - name the affected or contaminated gate(s)
        - record via JSG-09 then JSG-10 at that cap, or the terminal route below if G is itself JSG-09 or JSG-10
    elif_held:
      trigger: G is JSG-08 AND its owner receipt reports `receipt_status == absent` (a mechanical owner-field read). The conductor does **not** itself judge whether the real-world outcome has occurred — no owner field records live/pending versus dead-absent, so liveness is not a conductor predicate (Invariant A)
      action: route as not-cleared via the JSG-08 owner contract's `absent` state and cap per the ladder; `sealed_awaiting_outcome` is a **non-binding lifecycle annotation** an operator may attach when the case is known-live (see Run Lifecycle States), not a separate gate-clearing transition — a hold label over not-cleared, not a failure and not a closeout
    else_not_cleared_or_indeterminate:
      - halt at G; do not advance
      - record the weakest cleared gate as context, then route the final claim cap through JSG-09/JSG-10 using the ladder-owned cap rule for the selected `closeout_state` plus the ladder weakest-cleared-gate rule where applicable; missing evidence is not a pass
      - name the failed, missing, or indeterminate gate G
      - record the closeout via JSG-09 then JSG-10 at that owner-derived cap
      - EXCEPTION: if G is itself JSG-09 or JSG-10, use the closeout self-dependency terminal route below
```

**Ladder reconciliation (Route, Don't Restate).** The evidence ladder's
`blocked_or_contaminated` use_when names six defects; this conductor maps each to
an affirmative owner value, never to a mere absence: **leakage** → a JSG-02/JSG-03
packing or product-proof leakage/spoiler block-class failure; **post-cutoff contamination** →
JSG-05 `probe_result == fail` **with** `isolation_result == proven` (a bare `fail` without proven isolation is a caveated not-cleared route, not contamination, per the transition function and the probe protocol); **tool-use breach** → `isolation_result ==
violated`; **unreconciled scoring failure** → a JSG-07 owner-reported
scoring-integrity/admission failure, such as an owner-reported frozen-input
mismatch, is **`indeterminate_until_authored`** (no exact owner value yet discriminates an integrity breach from an admission/absence state, since `FailureEvent.failure_type` is unconstrained), so no current value routes to `blocked_or_contaminated`; a conductor-invented rerun hash
comparison is not a valid discriminator, and a bare `score_blocked` for a
*missing* input is absence → not-cleared; **missing isolation / missing source
identity** → read as an **affirmative defect that breaks an evaluated gate**
(`isolation_result == violated`, or an owner-set `receipt_status ==
contaminated_or_invalid`), consistent with the ladder's own "...breaks the
evaluated gate" framing. Not-yet-authored absence — `not_proven`, a by-hand gate
with no runner, an `indeterminate_until_authored` subpredicate — is an evidence
gap, not a broken gate, so it routes to not-cleared and the by-hand
product-learning cap (Seam 3), not to `blocked_or_contaminated`. This is a
reading the ladder permits, not an override; if the ladder later distinguishes
these explicitly, this conductor tracks it and is stale for that point until
updated.

**Seam 5 — closeout self-dependency terminal route.** When the halting gate is
`JSG-09` or `JSG-10` — the closeout machinery itself is the missing or invalid
receipt — the conductor must not "close out via JSG-09/10," which would be
circular. It enters the terminal run state `halted_no_completed_closeout`:

```yaml
halted_no_completed_closeout:
  trigger: JSG-09 or JSG-10 is the missing or invalid gate
  conductor_must:
    - make no completed-closeout claim
    - name the missing or invalid classification or closeout artifact as the blocker
    - record the weakest cleared gate among JSG-01 through JSG-08 for context
    - emit the ladder's `judgment_spine_claim_classification` record (owner-owned shape) with `closeout_state: no_durable_evidence` and `weakest_missing_or_failed_gate: JSG-09|JSG-10` — the ladder sub-floor rule applied to the closeout artifact's own missing evidence; do not author a bespoke prose closeout claim
  conductor_must_not:
    - author the missing classification or closeout receipt to escape the halt
    - invent a closeout_state
```

The closeout artifact's own classification, recorded in the ladder's `judgment_spine_claim_classification` shape (not a conductor-authored prose claim; its subject is the closeout artifact, not the case judgment, so it is non-circular — the conductor does not run JSG-09/JSG-10 on the case), resolves to `no_durable_evidence` because the closeout
receipt has no durable evidence of its own; this is the ladder sub-floor rule
applied to the closeout artifact.

## By-Hand Isolation Cap

**Seam 3 — by-hand cap.** A gate step is "by-hand" when it is performed manually
by a person or an agent thread without an auditable runner receipt that proves
the property. The contrast is a code runner that emits an audit-grade receipt.

```yaml
by_hand_isolation_cap:
  affected_gates: [JSG-04, JSG-05, JSG-06]
  mechanism: >
    By-hand execution cannot bind the authorized, auditable live-execution
    provenance the no-tools contract requires; a hand-typed
    isolation_result == "proven" or gate_interpretation == "pass_valid" field is
    not self-certifying and is not gate-clearing (receipt-provenance sub-rule and
    the no-tools contract Receipt Provenance Boundary). JSG-04 therefore does not
    clear, JSG-05 cannot clear on a by-hand probe receipt, and JSG-06 (which
    depends on JSG-04) does not clear, at judgment-quality strength.
  claim_cap: no stronger than product-learning
  realized_closeout_state_is_one_of:
    - no_durable_evidence
    - unreceipted_product_learning_context
    - completed_product_learning_evidence
  realized_state_rule: >
    Selected per the actual product-learning-receipt completeness under the
    evidence ladder. By-hand does NOT automatically grant
    completed_product_learning_evidence.
  current_harness_reality:
    - There is no contestant-execution runner.
    - band_scorer hardcodes memorization_probe_result="not_run".
    - run_case scores a pre-supplied blind_judgement.yaml; it does not execute a contestant.
    - Therefore the first run loop is by-hand and caps at product-learning by this rule. The runner that would lift the cap is deferred.
```

## Run Lifecycle States

**Seam 4 — named run states.** These are operating-model run-state labels, not
new ladder tiers. Each resolves to an existing ladder closeout_state or claim
cap. The conductor mints no new claim vocabulary.

| Run state | Meaning | Ladder resolution |
| --- | --- | --- |
| `not_started` | no gate evaluated | no completed closeout; any claim cap must come from the ladder once classified |
| `in_progress_at_<gate>` | gates before `<gate>` cleared; evaluating `<gate>` | provisional weakest-cleared context only; no completed-closeout claim |
| `sealed` | JSG-06 cleared per its full gate-table predicate; a by-hand run still cannot reach it, because by-hand JSG-04 does not clear and the run halts there | provisional weakest-cleared context only; final claim cap still requires JSG-09/JSG-10 classification under the ladder |
| `scored` | JSG-07 cleared | provisional weakest-cleared context only; final claim cap still requires JSG-09/JSG-10 classification under the ladder |
| `sealed_awaiting_outcome` | a **non-binding lifecycle annotation** an operator may attach to a not-cleared-via-`absent` run that is known-live (sealed, possibly scored, real-world outcome not yet in); the conductor does not itself decide liveness — it reads JSG-08 `receipt_status == absent`, and the label adds no gate clearance | JSG-08 `receipt_status == absent` → not-cleared; reveal/calibration claim follows the JSG-08 owner contract and ladder classification; no completed judgment-quality claim until JSG-08, JSG-09, and JSG-10 clear |
| `calibrated` | JSG-08 cleared at the required status | JSG-08 status is read from the owner contract; final claim cap still requires JSG-09/JSG-10 classification under the ladder |
| `closed` | JSG-09 classification and JSG-10 closeout recorded | the recorded `closeout_state` and `claim_cap` per the ladder-owned classification |
| `halted_at_<gate>` | a non-closeout gate failed or is indeterminate (ordinary not-cleared, no contamination) | closeout via JSG-09/JSG-10; final claim cap is owner-derived from the selected ladder `closeout_state` and weakest-cleared context where applicable |
| `blocked_or_contaminated` | a gate's owner receipt reports an affirmative invalidity/breach value — not mere absence, by-hand/indeterminate execution, JSG-05 ambiguity, or a JSG-05 fail-with-unproven-isolation caveat | closeout_state = `blocked_or_contaminated`; claim cap per the ladder-owned cap rule for that state; name the affected gate |
| `halted_no_completed_closeout` | JSG-09 or JSG-10 itself failed (Seam 5) | ladder `judgment_spine_claim_classification` record with `closeout_state = no_durable_evidence` (sub-floor for the closeout artifact), not a conductor-authored claim |

`sealed_awaiting_outcome` exit rule: when the real-world outcome arrives, route
to a **JSG-08 attempt**, which resolves to one of the JSG-08 owner-contract
satisfaction states (`absent`, `reveal_readout_only`,
`qualitative_outcome_calibration`, `score_linked_outcome_calibration`, or
`contaminated_or_invalid`). Only `score_linked_outcome_calibration` clears at
judgment-quality strength; weaker statuses cap lower, and `contaminated_or_invalid`
routes through the contaminated/blocked branch. It never mints a new tier.

## Case-Selection Posture

```yaml
case_selection_posture:
  prefer: post-cutoff-first
  post_cutoff_first_means: the decision AND the outcome both fall after the model's training cutoff, giving both non-recognition and a real ground-truth outcome
  probe: JSG-05 memorization probe is mandatory and is the verifier of non-recognition; it is never skipped
  anonymization: probe-verified secondary only; renaming or perturbing a famous case risks hidden re-identification and severs ground-truth anchoring, so it is never assumed
  live_case_note: liveness is NOT a conductor predicate — the conductor only reads the JSG-08 receipt_status field; an operator MAY attach the non-binding sealed_awaiting_outcome annotation to a case they independently know to be live, but the conductor routes receipt_status == absent as not-cleared regardless and never itself decides live-versus-no-outcome (Invariant A)
  superseded_first_targets: famous pre-cutoff cases (for example a 2022 event) are poor FIRST judgment-quality targets
```

## How To Run A Case

1. **Authorization (human gate).** The owner authorizes the run. The conductor
   does not self-authorize.
2. **Select the case** per the post-cutoff-first posture; record source identity
   (JSG-01 inputs).
3. **Walk gates JSG-01 through JSG-10 in order.** At each gate, read the named
   receipt and evaluate the mechanical predicate (Seam 1).
4. **On clear, advance. On not-cleared or indeterminate, apply the transition
   function** (Seam 2), or the terminal route (Seam 5) if the halting gate is
   JSG-09 or JSG-10.
5. **Mark the execution mode.** If JSG-04, JSG-05, or JSG-06 ran by-hand, apply
   the by-hand cap (Seam 3).
6. **At JSG-08, read `receipt_status` mechanically.** `receipt_status ==
   absent` routes as not-cleared via the owner contract's `absent` state (the
   Seam-2 held branch); the conductor does not decide whether a real-world
   outcome is still pending. An operator MAY attach the non-binding
   `sealed_awaiting_outcome` annotation when they independently know the case is
   live — it adds no gate clearance and is not a conductor liveness
   determination (Invariant A). Revisit JSG-08 when a new owner receipt lands.
7. **Record JSG-09 classification and JSG-10 closeout** at the achieved cap, or
   `halted_no_completed_closeout` per Seam 5.

Existing harness components and their gate roles (plumbing only, not judgment
quality): `forseti-harness/runners/run_case.py` scores a supplied blind judgment
(JSG-07 plumbing); `forseti-harness/scoring/band_scorer.py` is the deterministic
scorer (JSG-07; note `memorization_probe_result` is hardcoded `not_run`);
`run_memorization_probe` handlers serve JSG-05. No contestant-execution runner
exists, so JSG-04, JSG-05, and JSG-06 are by-hand for now.

## Scaling Rule

Because the conductor routes rather than restates, it absorbs change without
drift:

- **Gate added:** add one predicate row (binding rule applies: exact field/value
  or `indeterminate_until_authored`), one transition entry, and a citation to
  the new owner source. No semantics are duplicated.
- **Gate closed or re-owned:** its predicate becomes a read of the
  owner-produced status field; the conductor changes the citation, not the
  meaning.
- **Owner semantics change:** the predicate auto-tracks because it only checks
  owner-produced fields; update `input_hashes` and `stale_if`.
- **Contestant-execution runner introduced (deferred):** the by-hand cap lifts
  for JSG-04/05/06 once an authorized runner emits the auditable live-execution
  provenance those gates require; the cap rule itself does not change, only which
  execution mode is in force.

This is why the footprint stays minimal: the conductor never holds gate meaning,
only the sequence, the predicates, the transitions, the lifecycle states, and
the by-hand cap.

## Connective-Tissue Wiring

So that every agent is routed here rather than reinventing a path, this
conductor is registered in:

- `.agents/workflow-overlay/source-loading.md` (Judgment Spine read pack);
- `docs/workflows/orca_repo_map_v0.md` (navigation);
- `docs/research/judgment-spine/manifest_v0.md` (Judgment Spine manifest);
- `docs/product/judgment_spine_gate_ownership_map_v0.md` (`downstream_consumers`).

These registrations are applied in the same pass as this artifact; see
`controlling_sources_updated` in the propagation block.

## Non-Claims

- This conductor does not validate Judgment Spine.
- This conductor does not create judgment-quality evidence; existing and
  surviving an adversarial review does not make it a clean run or proof.
- This conductor is the **path** toward judgment-quality evidence, not proof of
  it.
- This conductor does not authorize model execution, probe execution, scoring,
  fixture admission, or claim promotion.
- This conductor does not compute judgment quality, recognition verdicts, or
  scores; it reads them from their owners.
- This conductor does not create, rename, merge, or split any claim tier or
  closeout_state.
- By-hand runs cap at product-learning and cannot reach completed
  judgment-quality evidence.
- This conductor does not authorize implementation, runtime design, tests,
  deployment, commits, pushes, or PRs.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The owner-deferred Judgment Spine operating-model spine is re-opened. A
    case-agnostic conductor now sequences JSG-01 through JSG-10 with mechanical
    receipt predicates (including a receipt-provenance non-self-certification
    rule), a total fail/blocked transition function including a
    closeout self-dependency terminal route, an explicit by-hand isolation cap,
    and named run lifecycle states including sealed_awaiting_outcome. All of
    these are routing and lifecycle constructs that resolve to existing ladder
    vocabulary; no new claim tier or closeout_state is minted. Round-3 review
    patch (2026-06-03): the transition function is made total over a four-value
    outcome alphabet — cleared, contaminated_or_blocked, held, and
    not_cleared/indeterminate — with explicit precedence; a contaminated/blocked
    outcome now routes to the existing ladder closeout_state blocked_or_contaminated
    (cap = weakest unaffected gate, often none) instead of being mis-routed to the
    weakest-cleared-gate cap; the JSG-08 pending-outcome hold is folded in as a
    precedence-ordered branch so it is no longer doubly-defined against the
    not-cleared branch; JSG-06's predicate is re-bound to its own owner field
    (isolation_result proven) with the sealed-output subpredicate marked
    indeterminate_until_authored and the JSG-08-owned sealed_before_reveal field
    removed from it; and JSG-06's inherited-provenance dependency on JSG-04 is
    stated explicitly. blocked_or_contaminated already exists in the evidence
    ladder, so still no new claim tier or closeout_state is minted. The same
    pass also made the sealed lifecycle row's predicate explicit (with a
    by-hand-cannot-reach note), enumerated the five JSG-08 satisfaction states in
    the sealed_awaiting_outcome exit rule, and added a JSG-06->JSG-04 dependency
    line to the gate ownership map to make explicit a dependency the conductor
    already encoded — a co-pass alignment, not a superseding gate-dependency
    change, so it does not by itself make this conductor stale. Round-5 review
    patch (2026-06-03): the contaminated/blocked branch is narrowed to fire only
    on an affirmative owner-reported invalidity value (JSG-08
    contaminated_or_invalid, isolation_result == violated, or sealed_before_reveal
    == no), never on absence or a by-hand/indeterminate gate — those route to
    not-cleared and cap per Seam 3, which preserves the by-hand product-learning
    cap and keeps the branch a mechanical field read (Invariant A); and the
    seal-before-reveal ordering check is relocated into the JSG-08 predicate as a
    read of its own sealed_before_reveal field (it had been removed from JSG-06
    but not yet landed at JSG-08). Round-7 review patch (2026-06-03): the
    contaminated/blocked enumeration is completed against the owner sources — a
    confirmed JSG-05 memorization recognition (`probe_result == fail`,
    gate-interpretation fail_gate_closing / fail_gate_closing_with_caveat,
    severity blocking) now routes to blocked_or_contaminated, while a JSG-05
    ambiguous quarantine and all not-yet-authored absences route to not-cleared;
    a Route-Don't-Restate reconciliation note records that the ladder's
    blocked_or_contaminated use_when phrase "missing isolation, missing source
    identity" is read as an affirmative gate-breaking defect (not a
    not-yet-authored absence, which is an evidence gap capped per Seam 3), a
    reading the ladder's "breaks the evaluated gate" framing permits; and the
    JSG-06 forward-reference and the JSG-08 sealed_before_reveal == no mapping are
    reworded to name the field-level mechanism and its owner grounding. A robust
    later option is to add sealed_before_reveal == no to the JSG-08 owner
    contract's contaminated_or_invalid use_when so the conductor reads a literal
    owner mapping. Still no new claim tier or closeout_state minted. Round-9
    review patch (2026-06-03): a systematic predicate-completeness pass binds each
    gate predicate to its owner's full required-receipt rather than a bare
    structural field — JSG-02 now also requires the zero-spoiler participant-visible
    boundary (no packing leakage/spoiler block-class failure; semantic-leakage
    portion indeterminate_until_authored), JSG-03 now also requires the
    owner-required ledger contents (authors, version pins, enum-valid band inputs,
    second_label_diffs disagreement trail), and JSG-01's indeterminate subpredicate
    is broadened to source-identity, inspectability, and timing/cutoff; and the
    contamination enumeration is completed against all six ladder
    blocked_or_contaminated use_when items by adding the JSG-02/JSG-03 packing
    leakage/spoiler block-class failure and the JSG-07 unreconciled scoring
    failure-event as affirmative owner-reported invalidity values (the JSG-07
    value is withdrawn in the Round-11 entry below). Absence still routes to
    not-cleared (Seam 3); still no new claim tier or closeout_state minted. Round-11 review patch (2026-06-03): two predicate-binding corrections
    from the final review — (1) JSG-01's bound pre_decision_status subpredicate no
    longer clears on bare presence; Judgment-authority finalization is marked
    indeterminate_until_authored (the finalizing authority is an unstaffed open
    owner decision and an operator-set status is an owner block-state) and the
    clearing value is constrained to a cleared pre-decision value (not excluded);
    (2) the JSG-07 score_blocked value added in round 9 is WITHDRAWN from the
    contamination set — score_blocked is a mixed admission state firing mostly on
    absences, so the scoring-integrity-contamination subpredicate is now
    indeterminate_until_authored and a bare score_blocked / re-derivation mismatch
    / absent result routes to not-cleared (Seam 3), pending an owner field that
    discriminates an affirmative integrity failure from an absence. Two low nits
    also tidied (the sealed lifecycle row now points to the full JSG-06 predicate;
    JSG-07 re-derivation is framed as owner-authorized verification, not a
    conductor-computed score). The contamination set is therefore five affirmative
    owner values plus the two reconciled missing-isolation/source-identity
    readings; still no new claim tier or closeout_state minted. Round-13 patch
    (2026-06-03), from an INDEPENDENT out-of-thread adversarial review (the
    in-thread rounds 3-12 shared the author's blind spot and wrongly passed these):
    (AR-01, high) JSG-08 no longer clears on a bare self-asserted `receipt_status`
    — it now requires the full owner-required receipt present and non-missing, per
    the owner's "clears only when its own durable receipt satisfies the fields";
    (AR-02, med) a JSG-07 affirmative re-derivation / frozen-input mismatch (an
    unreconciled scoring failure) now routes to blocked_or_contaminated rather than
    being lumped with absence at not-cleared — correcting a round-11 over-correction,
    the owner-authorized re-derivation being the discriminator (so the contamination
    set gains this affirmative value); (AR-03, med) JSG-10 and JSG-09 now check
    `claim_cap` consistency by reference to the ladder-owned cap rules for the
    recorded `closeout_state`, rather than restating cap values in the conductor.
    Round-14 patch (2026-06-04), from a SECOND independent out-of-thread review that
    both reviewed AND patched in one pass (rounds 3-12 were self-review and shared the
    author's blind spot; this pass was verified field-by-field against the owner sources
    before applying): five confirmed seams fixed in reference-not-restate style —
    (AR-P1, high) JSG-08 stops enumerating the receipt (it had omitted owner-required
    `case_id`, `receipt_artifact`, `failure_events`) and now references the reveal
    contract's Required Receipt Fields; (AR-P2, high) JSG-09/JSG-10, the not-cleared cap
    action, and the run-lifecycle resolutions stop restating cap values and now reference
    the ladder's per-`closeout_state` cap rule plus the weakest-cleared-gate rule;
    (AR-P3, high) JSG-03 stops enumerating frozen-FacilitatorLedger contents and references
    the packing interface's frozen-ledger requirements; (AR-P4, med) JSG-06 binds the sealed
    blind judgment hash named by the gate map and evidence ladder instead of falsely treating
    it as unowned, so `sealed` is reachable for a clean isolated run while still gated behind
    JSG-04 provenance (by-hand still cannot reach it); (AR-P5, med) the JSG-05
    fail-with-unproven-isolation caveat no longer routes to affirmative contamination — only
    the proven-isolation confirmed recognition does — resolving a contradiction with the
    conductor's own absence-is-not-contamination note and with the probe/no-tools owners. A
    parallel lossy restatement in the gate ownership map (its JSG-08 receipt list and JSG-10
    weakest-cleared cap) is logged for a separate owner-map pass and is NOT changed here.
    This is one pass and does not claim completeness. Still no new claim tier or
    closeout_state minted.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/product/judgment_quality_promotion_operating_model_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/research/judgment-spine/manifest_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/product-proof.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md
    - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
    - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
    - docs/research/judgment-spine/manifest_v0.md
    - forseti-harness/scoring/band_scorer.py
    - forseti-harness/runners/run_case.py
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The existing Judgment Spine claim-tier gate already requires claim tier
        and closeout state before stronger claims. The conductor routes through
        that gate; it does not add a new overlay validation rule.
    - path: docs/product/judgment_spine_evidence_ladder_architecture_v0.md
      reason: >
        The ladder owns claim tiers, closeout states, weakest-cleared-gate, the
        sub-floor rule, and receipt minima. The conductor consumes that
        vocabulary and adds none.
    - path: docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
      reason: >
        The JSG-08 contract owns the reveal/calibration receipt shape and
        satisfaction states. The conductor reads its status field and changes
        nothing.
    - path: forseti-harness (band_scorer.py, run_case.py, runners, schemas)
      reason: >
        No code changed. The conductor describes how existing plumbing maps to
        gates and records that the contestant-execution runner remains deferred.
    - path: Daimler-specific and Canoo/Walmart case, run, and decision artifacts
      reason: >
        This is a case-agnostic operating model. Applying it to a specific case
        requires a separate case-specific run-state and classification record.
  stale_language_search: >
    rg -n "conductor|operating model|sealed_awaiting_outcome|halted_no_completed_closeout|indeterminate_until_authored|judgment_quality_promotion_operating_model|by-hand"
    docs/product/judgment_quality_promotion_operating_model_v0.md
    .agents/workflow-overlay/source-loading.md
    docs/workflows/orca_repo_map_v0.md
    docs/research/judgment-spine/manifest_v0.md
    docs/product/judgment_spine_gate_ownership_map_v0.md
  stale_language_search_result: >
    Executed on 2026-06-03 after wiring. The new lifecycle vocabulary
    (sealed_awaiting_outcome, halted_no_completed_closeout,
    indeterminate_until_authored) appears only in this conductor, with no
    colliding or contradicting use elsewhere. The operating-model path appears
    in this conductor and the four wired surfaces (source-loading read pack,
    repo map, manifest, gate ownership map), plus historical deferred notes in
    the evidence ladder, product-proof, and the gate map's own prior DCP, one
    prior review output, and disposable hygiene-queue checkpoints. Those prior
    references are historical DCP or checkpoint records left intact by design;
    none contradicts the re-opening recorded here. No hit converted a routing or
    navigation surface into validation, readiness, scoring authorization, model
    execution, or judgment-quality evidence.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not fixture admission
    - not scoring authorization
    - not model execution
    - not judgment-quality evidence
    - not implementation authorization
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Round-16 patch (2026-06-04): JSG-02 now names product-proof as a routed
    zero-spoiler owner for participant-facing surfaces instead of relying only
    on packing hard-marker checks. JSG-07 no longer treats a conductor-defined
    rerun equality check over `scoring_result_hash` as an owner-authorized gate
    predicate — this reverses the round-13 AR-02 entry above, which wrongly
    treated that re-derivation as the scoring-integrity discriminator. The
    predicate now routes to the phase-1 infrastructure, packing
    deterministic-checking boundary, and scorer-produced ScoringResult/FailureEvent
    outputs for scoring receipt completeness, provenance/hash checking,
    failure-event handling, and affirmative scoring-integrity/admission failures.
    This prevents a participant-visible spoiler leak, scored-by-hand run, or
    under-receipted score with owner-produced blocking failure events from reaching
    the `scored` lifecycle state or a stronger claim merely because local hard
    markers or version/hash fields exist. No new claim tier or closeout_state is
    minted.
  trigger: architecture_doctrine
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/product/judgment_quality_promotion_operating_model_v0.md
  downstream_surfaces_checked:
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md
    - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
    - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
    - .agents/workflow-overlay/product-proof.md
    - forseti-harness/scoring/band_scorer.py
    - forseti-harness/schemas/scoring_models.py
  non_claims:
    - not validation
    - not readiness
    - not scoring authorization
    - not judgment-quality evidence
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Round-17 patch (2026-06-09), from an independent out-of-thread, no-repo,
    cross-family delegated adversarial review (reviewer GPT-5.5 Thinking; author
    family Claude Opus-class; commission workflow-delegated-review-patch no_repo
    mode; findings + CA adjudication recorded at
    docs/review-outputs/adversarial-artifact-reviews/judgment_conductor_no_repo_delegated_adversarial_artifact_review_v0.md).
    Seven findings, all CA-accepted after verification against the owner sources:
    (F1) JSG-01 stops asserting "no ECR field schema exists" — the source-side
    schema SP-1/2/3/6 is now ratified in the core-spine boundary, so the
    source-identity/inspectability/timing subpredicates route to the declared
    owner fields and allowed values, while the field derivers, the SP-5 finalizer,
    and D2 stay indeterminate; JSG-01 remains FROZEN and clears no case.
    (F2) the JSG-02/JSG-03/JSG-07 "complete per the routed owner sources" clear
    predicates are rebound to owner-enumerated field presence/validity (not a
    holistic completeness judgment), keeping the semantic-leakage subpredicate
    indeterminate. (F3) the JSG-07 scoring-integrity-vs-admission contamination
    discriminator is marked indeterminate_until_authored because the scorer's
    FailureEvent.failure_type is unconstrained free-text; a FailureEvent.severity
    == "blocking" routes by the transition function as not-cleared, not
    contamination — withdrawing the prior under-specified affirmative
    scoring-integrity contamination trigger from the transition function and the
    ladder reconciliation. (F4) the ladder-reconciliation shorthand for
    post-cutoff contamination regains the isolation_result == proven qualifier it
    had dropped, matching the transition function and the probe protocol. (F5)
    the sealed_awaiting_outcome held branch is re-grounded as a mechanical read of
    JSG-08 receipt_status == absent (routes as not-cleared via the owner
    contract's absent state); sealed_awaiting_outcome is demoted to a non-binding
    operator lifecycle annotation, removing the conductor's liveness judgment
    (Invariant A). Owner chose conductor-only path (a); no pending-outcome owner
    field was added. (F6) the Seam-5 closeout self-dependency terminal route now
    emits the ladder-owned judgment_spine_claim_classification record
    (closeout_state no_durable_evidence, weakest_missing_or_failed_gate
    JSG-09|JSG-10) for the closeout artifact rather than a conductor-authored
    prose closeout claim — non-circular (subject is the closeout artifact, not the
    case judgment). (F7) input_hashes recomputed against current working-tree
    bytes and branch_or_commit updated. No new claim tier or closeout_state is
    minted; JSG-01 stays FROZEN. This is one advisory-review pass; nothing here is
    kept until the mandatory de-correlated post-patch re-review clears.
  trigger: architecture_doctrine
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/product/judgment_quality_promotion_operating_model_v0.md
  downstream_surfaces_checked:
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - forseti-harness/schemas/scoring_models.py
    - .agents/workflow-overlay/validation-gates.md
  intentionally_not_updated:
    - path: docs/product/judgment_spine_gate_ownership_map_v0.md
      reason: >
        The gate map's Round-15 reference-not-restate patch already fixed the
        JSG-08/JSG-10 restatement the conductor's stale Round-14 note flagged; no
        further gate-map change is required, and the historical Round-14 note is
        left intact as a record.
    - path: docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
      reason: >
        F1 routes the conductor TO the owner's already-ratified SP-1/2/3/6 schema;
        the owner source is authority and is not edited here.
    - path: docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
      reason: >
        F5 path (a) routes via the existing absent state; the owner-source-change
        option (b), adding a pending-outcome field, was declined.
    - path: forseti-harness (scoring_models.py, band_scorer.py, run_case.py)
      reason: >
        No code changed. F3 reads the existing FailureEvent.severity and records
        that failure_type is unconstrained; the discriminating owner enum is deferred.
  non_claims:
    - not validation
    - not readiness
    - not judgment-quality evidence
    - not a clean adversarial pass (new seams were opened; a de-correlated post-patch re-review is required before keep)
    - JSG-01 stays FROZEN; this pass does not unfreeze it
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Round-18 patch (2026-06-09), from the fresh FULL de-correlated, no-repo,
    cross-family adversarial review of the patched (post-Round-17) conductor
    (reviewer GPT-5.5 Thinking; author family Claude Opus-class; commission
    workflow-delegated-review-patch no_repo mode; courier bundle archive sha256
    8E47AB4D28CE200A3DD3F49F30968776C4765FFF9C77C22BE955CE32AE17B091, all 16
    bundled sources byte-matched the embedded manifest). The pass confirmed the
    four seams, Invariant A/B, and Seam 5 hold, and opened exactly one residual
    seam (NEW-SEAM-F5-LIVE-PROCEDURE, severity major), CA-accepted: the Round-17
    F5 repair de-judged liveness in the formal transition function and lifecycle
    table, but two procedural-prose spots still told the conductor to record
    sealed_awaiting_outcome for "a live post-cutoff case with no outcome yet" — a
    conductor-side liveness determination the F5 fix had removed. This patch
    rebinds both spots: (1) the Case-Selection Posture live_case_note now states
    liveness is NOT a conductor predicate (the conductor only reads JSG-08
    receipt_status; sealed_awaiting_outcome is a non-binding operator annotation);
    (2) How-To-Run-A-Case step 6 now reads JSG-08 receipt_status mechanically
    (receipt_status == absent routes not-cleared via the owner contract's absent
    state, the Seam-2 held branch), with sealed_awaiting_outcome as an optional
    non-binding operator annotation and no conductor liveness call. This only
    aligns procedural prose with the already-patched transition function and
    lifecycle table; no predicate, transition rule, ladder vocabulary, or claim
    tier changed. No new claim tier or closeout_state minted; JSG-01 stays FROZEN.
    NOT YET KEPT: the mandatory bounded same-family post-patch recheck has not yet
    run. Tracked-but-not-changed-here: the JSG-01 row's note that the SP-1/2/3/6
    derivers are "deferred" is stale — they are built and committed in the ECR
    lane (forseti-harness/ecr/, commits d857c58/51f4193/14490ce/6329d71); this
    CA-discovered accuracy correction is deferred to the JSG-01 work item.
  trigger: architecture_doctrine
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/product/judgment_quality_promotion_operating_model_v0.md
  downstream_surfaces_checked:
    - docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md
    - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
  non_claims:
    - not validation
    - not readiness
    - not judgment-quality evidence
    - not kept until the bounded same-family post-patch recheck clears
    - JSG-01 stays FROZEN; this pass does not unfreeze it
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Round-19 patch (2026-06-10): build-state correction only (no gate/predicate/transition
    change). The SP-5 finalizer HALF is now built and committed
    (forseti-harness/schemas/finalization_models.py, a37f896 -- the FinalizationReceipt model +
    a validate-only, block-don't-repair consumer; hardened after a no_repo cross-family code
    review). The JSG-01 finalization-provenance subpredicate row is corrected from "SP-5
    finalization mechanism is unbuilt" to "mechanism built, but no case packet yet carries a
    FinalizationReceipt." JSG-01 STAYS FROZEN: the EvidenceUnit binding, a case packet
    carrying a receipt, and D2 still gate the unfreeze. No claim tier or closeout_state minted.
  trigger: lifecycle_boundary
  related_triggers:
    - validation_philosophy
  controlling_sources_updated:
    - docs/product/judgment_quality_promotion_operating_model_v0.md
    - docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  downstream_surfaces_checked:
    - docs/workflows/orca_repo_map_v0.md
    - docs/research/judgment-spine/ideal_judgment_quality_run_and_current_position_v0.md
    - docs/research/judgment-spine/sp5_finalization_receipt_spec_v0.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Thin door -- its Judgment Spine section routes to the consolidation map / gap map
        (now updated) rather than carrying build-state; no edit needed.
    - path: docs/research/judgment-spine/sp5_finalization_receipt_spec_v0.md
      reason: >
        The behavior spec stays the contract; an as-built note is a later spec pass.
  non_claims:
    - not validation
    - not readiness
    - not judgment-quality evidence
    - not a JSG-01 unfreeze (JSG-01 stays FROZEN)
    - not the EvidenceUnit binding (a separate later slice)
```
