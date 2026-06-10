# Cross-Family Adversarial Check — JSG-01 ECR Receipt: Bind vs Fork

```yaml
artifact_role: Cross-family review prompt
review_lane: independent adversarial check (different model family; read-only; reviewer does not patch)
decisive_criterion: long-term structural integrity
load_rule: confirm-don't-trust — read the named sources before any firm claim; name anything you could not verify.
authority_boundary: independent signal for owner adjudication only — not a verdict, authorization, or block.
scope: bind-vs-fork for the JSG-01 source-side receipt ONLY (not finalization authority, not judgment quality, not fixture admission).
```

## Your job

You are an **independent reviewer from a different model family** than the one that made this decision. Your value is catching the *conceptual* blind spots a same-family reviewer would share — shared assumptions, over-readings, framing errors. Be **adversarial**: actively try to **refute** the recommended option. Default to skeptical. If you cannot access a named source, say so and mark which claims you could not verify.

The owner's decisive criterion is **long-term structural integrity** (maintainability as the system grows and a later consolidation lands), not speed.

## Background (enough to rule; verify against the anchors)

Orca's "Judgment Spine" has a first gate, **JSG-01**, that mechanically checks four source-side things about each piece of evidence before judgment runs: (1) source-identity, (2) inspectability / raw-observable, (3) timing/cutoff, (4) pre-decision status. It currently **halts** (`indeterminate_until_authored`) because no schema names the exact fields + allowed-values it should check — which freezes the entire judgment pipeline. (The 4th subpredicate also needs a Judgment-side "who finalized it" authority; that is **out of scope for this check** and handled separately.)

## The decision under review

**Recommended: BIND, don't FORK.** Rather than author a *new* ECR field schema, write a minimal "JSG-01 source-side receipt **binding**" that **references the existing `EvidenceUnit` schema** (and its `PreDecisionStatus` enum), naming which existing fields satisfy each subpredicate + the cleared-conditions. The conductor *references* the binding (no copy, no predicate edit).

## Evidence the decision rests on (attack these)

1. An `EvidenceUnit` schema **already exists** (`pydantic_schema_reference.md`, v0.14 harness spec):
   ```python
   class PreDecisionStatus(StrEnum):
       VERIFIED_PRE_DECISION = "verified_pre_decision"
       UNCERTAIN_TIMESTAMP   = "uncertain_timestamp"
       EXCLUDED              = "excluded"
   class EvidenceUnit(BaseModel):
       evidence_id: str; source_id: str; source: str; timestamp: str
       retrieval_timestamp: str; hash: str
       pre_decision_status: PreDecisionStatus; pre_decision_basis: str; summary: str
   ```
2. The capture/cleaning **boundary doc** says ECR owns the "pre-cleaning captured-signal receipt"; that *"the current IPF Evidence Unit standard remains the source to cite until the later ECR/EvidenceUnit consolidation"*; that Data Capture must **not** own *"final ECR field architecture"*; and that the **final ECR/EvidenceUnit field architecture is a deferred owner decision**.
3. The **obligation contract** states source-side obligations (identity, raw-observable, timing, cutoff) as *prose* but explicitly *"does not define ECR fields/keys/schema."*
4. Two real fixtures (Canoo/Walmart, Unity) already populate the `EvidenceUnit` fields.

## What to attack (bind-vs-fork specifically)

- Does binding to the existing schema create **hidden coupling the deferred consolidation will later have to tear out** — i.e., is "bind" actually *more* long-term rework than a clean minimal fork?
- Is a **v0.14 harness pydantic spec the right thing for a GATE to depend on**, or is it a research-snapshot that shouldn't be load-bearing? (Possible divergence: a separate IPF semantic home, `core_spine_v0_information_production_foundation_v0.md`, may differ from the harness pydantic — which is canonical? Does the divergence break the bind?)
- Does binding force JSG-01 to **inherit `EvidenceUnit` quirks** — e.g., `PreDecisionStatus` has only 3 values; is that enum complete/correct for what JSG-01 must distinguish, or does binding lock in a too-narrow vocabulary?
- Is there a **third option** that beats both (a thin view/adapter; a versioned interface; binding to the IPF semantic standard instead of the pydantic; extending a different contract)? Name it concretely.
- Is *"the boundary doc says cite the existing standard"* genuine support for binding, or **over-read** (cite-for-semantics ≠ bind-a-gate-predicate-to-it)?
- Under **long-term structural integrity**, rank {bind, fork, third option} and justify the winner as the system grows and the consolidation lands.

## Output

- **Verdict:** `bind` | `fork` | `third-option` | `insufficient-evidence`.
- **Single most decisive reason.**
- **Strongest argument against your own verdict** (steelman the other side).
- **Unverifiable claims:** anything above you could not confirm against source.
- **Citations:** the specific sources/lines you relied on.

## Source anchors (read before ruling)

- `docs/product/judgment_quality_promotion_operating_model_v0.md` — JSG-01 clear-predicate row (~L205)
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` — ECR layer, "cite existing standard," deferred consolidation, capture-must-not-own-final-schema
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` — Ob. 6/7/8/9/16 (16 explicitly does NOT define ECR fields)
- `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md` — `EvidenceUnit` + `PreDecisionStatus`
- `docs/product/core_spine_v0_information_production_foundation_v0.md` — IPF EvidenceUnit semantic home (canonical-home cross-check)
- `docs/research/judgment-spine/harness/v0_14/fixtures/{canoo_walmart_2022,unity_runtime_fee_2023}_v0_14/evidence_registry_draft_v0.md` — real populated cases
```
