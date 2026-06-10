# Fresh Full De-Correlated Adversarial Artifact Review — Judgment Conductor (`no_repo` / advisory)

```yaml
retrieval_header_version: 1
artifact_role: Review-input bundle brief (delegated review-and-patch commission; no_repo, advisory, fresh full pass)
scope: >
  Self-contained commission brief, fitness reference, post-Round-17 delta map, owner-source map, hash
  manifest, and findings-only output contract for a fresh FULL de-correlated adversarial review of the
  patched judgment conductor by a repo-blind, non-Opus-family reviewer. Not Orca authority; advisory only.
use_when:
  - Running the commissioned fresh full no_repo adversarial review of the patched judgment conductor.
  - Checking the fitness reference (four seams + Invariant A/B + Seam 5), the Round-17 deltas to attack,
    the owner-source map, the hash manifest, or the findings-only output contract.
authority_boundary: retrieval_only
```

> This brief travels inside the bundle so it is self-contained for a reviewer with **no repo access**.
> Governing convention: Orca `.agents/workflow-overlay/delegated-review-patch.md` (`no_repo` mode).

## What this is

A **fresh, full, de-correlated, no-repo adversarial artifact review** of ONE high-stakes Orca artifact:
the **Judgment Quality Promotion Operating Model** ("the conductor"), **as patched through Round-17**.
You have **no repo access** — everything you need is in this bundle (`sources/`). You return **FINDINGS
ONLY** — no diff, no patch. The home/CA model adjudicates every finding and applies any accepted change
itself.

This is **not** a bounded recheck of specific prior findings. It is a **full pass**: re-attack the whole
artifact against the four seams, the two invariants, and the closeout terminal route, **and** specifically
test whether the Round-17 patch (below) **opened any new seam**.

**Why this pass exists / success signal.** The conductor's standing goal is to be airtight on its four
seams and to **survive a full de-correlated review with NO new seam**. A prior cross-family pass produced
seven findings that were patched (Round-17), then cleared by a *bounded* recheck the owner accepted as
sufficient — but a *strict* full de-correlated pass on the patched bytes has not yet been run. This is that
pass. The success signal is met only if you open **no new seam** (and confirm the four hold).

## Review target

`sources/judgment_quality_promotion_operating_model_v0.md` — a case-agnostic conductor that sequences
Judgment Spine gates **JSG-01 → JSG-10** over owner-produced receipts. It is supposed to *route and verify
receipts*, never to compute judgment quality. Review the **bytes in this bundle** (confirm against the Hash
Manifest below), not any remembered version.

## Decision criteria / fitness reference (ATTACK axes — NOT pass-if-matches bars)

Attack each; treat the reference as something to break, not a checklist to confirm.

1. **Seam 1 — mechanical predicate, no LLM discretion.** Every gate clear-condition must be a mechanical
   read of an owner-produced receipt field (exact field + allowed value). No predicate may require judgment.
   Hunt for discretion smuggled in (e.g. a completeness-judgment, an "owner-enumerated field presence/
   validity" check that actually needs the conductor to decide what is complete).
2. **Seam 2 — total fail/blocked transitions.** The transition function must be total over
   `[cleared, contaminated_or_blocked, held, not_cleared_or_indeterminate]`, name the affected gate, and cap
   correctly: weakest-cleared for not-cleared; the `blocked_or_contaminated` cap for **affirmative**
   contamination (NOT weakest-cleared). Hunt for undefined/contradictory routing, or **absence mis-routed as
   contamination**.
3. **Seam 3 — by-hand isolation cap.** By-hand JSG-04/05/06 cannot bind auditable live-execution provenance
   → cannot clear at judgment-quality strength → the run **caps at product-learning**. Hunt for any path that
   lets a by-hand / self-asserted receipt clear, or over-claims above product-learning.
4. **Seam 4 — named `sealed_awaiting_outcome`.** A live post-cutoff case with no outcome is **held** (not
   failed, not closed), resolves to an existing ladder state, and mints **no new** claim vocabulary. Hunt for
   lifecycle states that invent vocabulary or mis-resolve to the ladder.
5. **Seam 5 — closeout self-dependency terminal route.** When the halting gate is JSG-09 or JSG-10, the
   conductor must not "close out via JSG-09/10" (circular); it enters `halted_no_completed_closeout` and emits
   the ladder's `judgment_spine_claim_classification` record for the closeout artifact. Hunt for circularity,
   minted vocabulary, or a self-authored closeout claim.

Plus two invariants:

- **Invariant A (no-authority):** the conductor is subject/assistant, **never the gavel**. A gate that needs
  the conductor to exercise judgment to clear is NOT cleared. Verdicts, scores, and claim tiers live in their
  owner sources.
- **Invariant B (route-don't-restate):** the conductor holds **only** routing/lifecycle. Every predicate must
  check an OWNER-produced field and cite the owner; it must never duplicate, paraphrase, or contradict owner
  semantics. **Restatement, paraphrase-clear, or contradiction of an owner source is a finding.**

## Round-17 deltas to attack (did any open a new seam?)

These seven changes are what the last review produced. Probe each for self-consistency, owner-grounding, and
whether the fix introduced a NEW seam. Do **not** merely confirm them.

1. **F1 — JSG-01 routes to the ratified SP-1/2/3/6 source-side schema but stays FROZEN.** The core-spine
   boundary now declares SP-1 `source_identity_state` ∈ {resolved, family_only}, SP-2 `inspectability_state
   == inspectable_verifiable`, SP-3 timing `== pre_cutoff` over `PacketTiming.cutoff_posture`, SP-6
   `source_visibility_posture`. The conductor routes to these but holds JSG-01 `indeterminate_until_authored`
   in practice (derivers + SP-5 finalizer + D2 deferred) and says "JSG-01 stays FROZEN and clears no case."
   Attack: is the routing faithful to the boundary's ratified schema (verify against
   `core_spine_v0_data_and_cleaning_spine_boundary_v0.md`)? Does "routes to ratified fields but FROZEN"
   create an internal contradiction, an over-claim, or a path that could clear?
2. **F2 — JSG-02/03/07 rebound to owner-enumerated field presence/validity** (not holistic "completeness").
   Attack: does "present and valid per the owner-enumerated required receipt fields" still require the
   conductor to *judge* completeness (Invariant A leak) or to *enumerate* owner fields locally (Invariant B
   leak)?
3. **F3 — JSG-07 scoring-integrity-vs-admission contamination discriminator is `indeterminate_until_authored`**
   because the scorer's `FailureEvent.failure_type` is unconstrained free text; a `FailureEvent.severity ==
   "blocking"` routes as **not-cleared**, not contamination. Attack: with the contamination trigger withdrawn,
   is any affirmative scoring-integrity breach now mis-routed or lost? Is `severity == "blocking" →
   not-cleared` consistent with Seam 2's precedence (verify against `scoring_models.py`)?
4. **F4 — ladder-reconciliation post-cutoff contamination regained `isolation_result == proven`.** Attack:
   is this consistent with the transition function and `memorization_probe_protocol.md`? Any double-definition
   or contradiction with the absence-is-not-contamination rule?
5. **F5 — `sealed_awaiting_outcome` re-grounded as a mechanical read of JSG-08 `receipt_status == absent`**
   (routes as not-cleared via the owner contract's `absent` state); demoted to a **non-binding operator
   annotation**; the conductor makes no liveness judgment. Attack: does removing the liveness judgment fully
   satisfy Invariant A? Is the `held` branch still total and non-contradictory against the not-cleared branch
   (Seam 2)? Does the annotation smuggle any clearance?
6. **F6 — Seam-5 emits the ladder `judgment_spine_claim_classification` record** (`closeout_state:
   no_durable_evidence`) for the closeout artifact instead of a prose claim. Attack: is the "subject is the
   closeout artifact, not the case judgment" non-circularity argument sound? Any minted vocabulary?
7. **F7 — `input_hashes` recomputed and `branch_or_commit` updated.** Bookkeeping; review the bundled bytes
   per the Hash Manifest regardless.

## Owner sources provided (verify route-don't-restate fidelity against these)

| Bundle file (`sources/`) | Original repo path | What it owns |
| --- | --- | --- |
| `judgment_quality_promotion_operating_model_v0.md` | docs/product/ | **THE TARGET** (conductor) |
| `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | docs/product/ | JSG-01 owner surface; declares the **ratified** SP-1/2/3/6 source-side ECR field schema (F1) |
| `core_spine_v0_data_capture_spine_obligation_contract_v0.md` | docs/product/ | JSG-01 source-identity obligation owner; defines no ECR field schema |
| `judgment_spine_evidence_ladder_architecture_v0.md` | docs/product/ | claim tiers, closeout states, weakest-cleared-gate, sub-floor |
| `judgment_spine_gate_ownership_map_v0.md` | docs/product/ | gate ownership, required receipts, gate dependencies |
| `judgment_spine_reveal_calibration_owner_contract_v0.md` | docs/product/ | JSG-08 satisfaction states + required receipt fields |
| `contestant_no_tools_execution_contract_v0.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-04/05/06 isolation + live-execution provenance boundary |
| `memorization_probe_protocol.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-05 recognition-verdict semantics |
| `phase_1_infrastructure_architecture.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-07 scorer / version / hash guardrails |
| `packing_to_harness_foundation_interface_architecture_v3.md` | docs/research/judgment-spine/harness/v0_14/ | frozen packet/ledger + deterministic-checking boundary |
| `band_input_labeling_rubric.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-03 ledger band inputs |
| `validation-gates.md` | .agents/workflow-overlay/ | the **Receipt-field provenance gate** the conductor's Seam-1 sub-rule cites |
| `product-proof.md` | .agents/workflow-overlay/ | JSG-02 zero-spoiler participant boundary |
| `band_scorer.py` | orca-harness/scoring/ | Seam-3 reality: hardcodes `memorization_probe_result="not_run"` |
| `run_case.py` | orca-harness/runners/ | Seam-3 reality: scores a pre-supplied blind judgment; executes no contestant |
| `scoring_models.py` | orca-harness/schemas/ | JSG-07 schema — `ScoringResult`/`FailureEvent` (load-bearing for F3) |

## Scoped-out surfaces (NOT predicate owners — do NOT block on these)

The following are intentionally **excluded** and must **not** trigger `SOURCE_CONTEXT_INCOMPLETE`: the
conductor cites them only as `downstream_consumers`, `input_hashes` provenance pins, `stale_language_search`
targets, or `downstream_surfaces_checked` — the dependency points the other way, and they sit outside this
commission's bounded scope (the four seams + Invariant A/B + Seam 5):
`.agents/workflow-overlay/source-loading.md`, `docs/workflows/orca_repo_map_v0.md`,
`docs/research/judgment-spine/manifest_v0.md`, `AGENTS.md`, `.agents/workflow-overlay/README.md`,
`.agents/workflow-overlay/source-of-truth.md`. The ECR source-identity field **derivers**, the **SP-5
finalizer**, and **D2** are intentionally **not built**; verify JSG-01 correctly holds those as
`indeterminate_until_authored` / FROZEN. Declare `SOURCE_CONTEXT_READY` once the `sources/` owner set is read.

## Output contract (`no_repo` / advisory)

Return **FINDINGS ONLY**. For each finding:

- `title`
- `severity`: `critical` | `major` | `minor` (priority only — you hold **no** formal verdict/validation authority)
- `location`: exact conductor section / line
- `seam_or_invariant_broken`
- `evidence`: cite the provided owner-source file + section — **neutral in tone, decision-sufficient in substance**
- `minimum_closure_condition`: the required end state (not how to implement it)
- `next_authorized_action`

Then a `residual_risk` note and an explicit **`NEW_SEAMS`** section (anything beyond the four seams + Seam 5 +
the seven Round-17 deltas). If you open no new seam and the four hold, say so explicitly — that is the success
signal.

**Do NOT emit:** a unified diff, a patch, `PASS`/ready/validated/approved claims, severity as authority, or any
runtime-model recommendation.

## Boundaries

- This is **advisory** (`no_repo`): de-correlated review only. The home/CA model adjudicates every finding,
  applies any accepted change within bounded scope, and decides what is kept.
- **De-correlation (commission who-constraint, NOT a model recommendation):** review this with a **different,
  non-Opus model family** than the author (author family = Claude Opus-class). For this *full* pass claiming
  the "no new seam" success signal, the reviewer **must be cross-family** (per the Orca overlay: cross-family
  de-correlation is reserved for discovery and for claiming the no-new-seam standard). Record `reviewed_by`
  and `authored_by` families in your return.
- Confirm the bytes you reviewed against the **Hash Manifest** below.

## Hash Manifest (SHA256 of bundled `sources/` bytes)

```text
0CE6E9584F4F1C4716559A654870AF43EBED3E5D53D3279AB658993B7DE1C2AE  band_input_labeling_rubric.md
D54DCD2CB34A8158232E1A428F70A1F3F182052529D7BC8E5293D5F21A67E1E3  band_scorer.py
3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C  contestant_no_tools_execution_contract_v0.md
28CB338F7208DA848DB70D0B59D33AFE2DC87D96D7DBFA9F2ABF654F8AB0EAC7  core_spine_v0_data_and_cleaning_spine_boundary_v0.md
ED225C5BF9B201644B6338A765A3B6B58FF69AA8E3B4BA98928E38C2DBF760E9  core_spine_v0_data_capture_spine_obligation_contract_v0.md
49739850CD2E156284D4E8B9ED29F2261FB5DFC84D469029C5F32A71B20E2F15  judgment_quality_promotion_operating_model_v0.md
79F6696DD50BE3FDCB574FD6AED4FE0761C6335029BFDBE39B51F104F4AD16CF  judgment_spine_evidence_ladder_architecture_v0.md
9A07DE8D61249D26DF1DB4E66FE918893D74FFF4970D2B9BABD1C0F97878CE9F  judgment_spine_gate_ownership_map_v0.md
ED146BEB5767EFDDA3E979AA798CA5CB044A896421872B02FBDF03615E4E6E07  judgment_spine_reveal_calibration_owner_contract_v0.md
7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61  memorization_probe_protocol.md
7291EF5E7C19A3514AE2B0E91D9FDD8917D7C4BFF039726FCD6075E55F73C1A4  packing_to_harness_foundation_interface_architecture_v3.md
0459C21E7083CD9295290170692BE47A85CBCD24B42B9B0C6E9D7ACF29AC850A  phase_1_infrastructure_architecture.md
AD1724202841D616F74494B22E3659D7987CC875BD36BF0F23B12C210E4B19C4  product-proof.md
F04BABF1EF4BAFE187E83552E3A3066DEBC47CAD92F5186011BD7B2925CE52AD  run_case.py
58A9FC2E0B605F8BB8189BF53252130A4D83B6F0FA440F3F56A0990ECB1FF896  scoring_models.py
689081A755FE88AAF140BD7C368B9F428856F160B858B5D0F5877B33FE258CEB  validation-gates.md
```

Author family: Claude Opus-class · Required reviewer family: cross-family, non-Opus · Mode: `no_repo` advisory, findings-only.
