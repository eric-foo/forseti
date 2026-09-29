# Commission Signal Board Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine README
scope: Entry point for the live Commission Signal Board spine and the Forseti Intelligence Cycle operating contract.
use_when:
  - Starting Commission Signal Board prompt, playbook, validator, or migration work.
  - Commissioning Gathering, Consolidation or Delivery in a Forseti Intelligence Cycle.
  - Checking which CSB artifacts are canonical after the spine-first pilot authorization.
  - Distinguishing the live CSB pilot from the staged global docs migration.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/spine.yaml
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/judgment/claim_support/forseti_intelligence_claim_support_contract_v0.md
  - forseti/product/spines/judgment/claim_support/forseti_semantic_evidence_integration_contract_v0.md
  - forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
stale_if:
  - The Commission Signal Board spine is renamed, retired, or merged into another spine.
  - The executable validator moves out of .agents/hooks.
  - Global Forseti docs move into a product-root docs subtree.
```

- Status: LIVE_PILOT_SPINE.
- Owner authorization: current-turn authorization, 2026-06-18.
- Current scope: Commission Signal Board plus the docs-only Forseti Intelligence Cycle operating contract.
- Global docs migration: accepted in direction, staged, not executed here.

## Canonical Artifacts

| Role | Path |
| --- | --- |
| Spine manifest | `forseti/product/spines/commission_signal_board/spine.yaml` |
| Prompt Structure Rules | `forseti/product/spines/commission_signal_board/authority/forseti_commission_signal_board_prompt_structure_rules_v0.md` |
| Prompt Structure | `forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md` |
| Playbook / Forseti Intelligence Cycle contract | `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` |
| Deliver decision-memorandum method | `forseti/product/spines/commission_signal_board/workflows/deliver_decision_memorandum_method_v0.md` |
| Validator pointer | `forseti/product/spines/commission_signal_board/harness/validator.md` |
| Test pointer | `forseti/product/spines/commission_signal_board/tests/validator_tests.md` |
| Moved-path index | `forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md` |
| Phase-vocabulary migration note | `forseti/product/spines/commission_signal_board/migrations/intelligence_cycle_phase_vocabulary_migration_v0.md` |

Naming note: **Prompt Structure** is the runnable CSB prompt/template. **Prompt Structure Rules** is the durable authority/rules doc for that prompt structure. File paths now use role-aligned names.

## Commission Profiles And Time Postures

CSB keeps the existing `mode: backtest | forward` axis unchanged and adds two
orthogonal fields:

- `commission_profile: standard_signal_board | company_competitive_intelligence`;
- `time_posture: recency_first | longitudinal`.

`recency_first` is the universal default and uses the canonical prompt's
deterministic 0-30, 31-90, 91-180, and over-180-day ladder. `longitudinal` is an
explicit override only for change, recurrence, or trajectory across a declared
period and requires both the period and rationale. A named event is a route or
query inside one of these two postures, not another posture.

A commission for one company subject defaults to
`company_competitive_intelligence` when the subject is a Brand or Org, including
an unresolved Brand/Org identity. That profile produces the conditional
ten-section company report and no demand-classifier handoff. Other commissions
continue to use the existing standard Sections 1-10 and classifier handoff.

## Forseti Intelligence Cycle

Commission one-company intelligence work as a **Forseti Intelligence Cycle**:
**Gathering → Consolidation → Delivery**. The
[operating authority](authority/forseti_commission_signal_board_prompt_structure_rules_v0.md#forseti-intelligence-cycle-operating-contract)
owns their meanings, completion boundaries and compatibility with existing
`Understanding` / `Deliver` profiles and `Acquire & Seal` / `Synthesize`
operations. Phase names do not prescribe extra model calls or duplicate reviews.

Gathering preserves the source collection; Consolidation produces reviewed,
source-linked understanding; Delivery answers the commissioned reader's question.
For the customer-evidence report route, use the
[adopted consolidation baseline](../../../../docs/workflows/customer_evidence_consolidation_baseline_v0.md).
Its accepted report can be delivered directly when it already fits the commission.
The playbook retains the typed acquisition gates and bounded supplement rules
for profiles that require them. Completing one phase does not authorize the next.

The shared intelligence claim-support contract governs every interpretation of
evidence across all three phases; changing the phase name never strengthens
what a source supports.

Use the phase-specific owners below; the playbook remains the operating
contract. Open the source for the current job rather than loading every owner.

| Current job | Owning source |
| --- | --- |
| Commission inputs or missing-input intake | [Required inputs](prompts/forseti_commission_signal_board_prompt_structure_v0.md#required-inputs), [missing-input return](prompts/forseti_commission_signal_board_prompt_structure_v0.md#missing-input-intake-output), and [board validation](workflows/commission_signal_board_playbook_v0.md#validator-command) |
| Company acquisition roles and source routing | [Role entry reads](workflows/commission_signal_board_playbook_v0.md#role-entry-reads); the commissioner binds the applicable sections and run inputs before dispatch |
| Consumer-brand completion, depth, maturity, and final source review | [Intelligence Cycle operating rules](authority/forseti_commission_signal_board_prompt_structure_rules_v0.md#forseti-intelligence-cycle-operating-contract) |
| Company information jobs, retailer admission, and metric claim limits | [Conditional company prompt contract](prompts/forseti_commission_signal_board_prompt_structure_v0.md#conditional-company-competitive-intelligence-output-contract) |
| Evidence Consolidation, judgment jobs, or repair/resume | [Supported operating route](../../../../docs/workflows/phase_a_customer_evidence_completion_path_v0.md#supported-operating-route); forward the runner's returned worker prompt |
| Synthesis gate and Deliver boundaries | [Turn B](workflows/commission_signal_board_playbook_v0.md#turn-b--synthesize) |
| Commissioned Deliver memorandum | [Deliver decision-memorandum method](workflows/deliver_decision_memorandum_method_v0.md) |
| Post-delivery review handoff | [Current review boundary and inputs](workflows/commission_signal_board_playbook_v0.md#post-delivery-adversarial-review-handoff) |

The playbook owns the execution gates and six non-numeric outcome signals.
Historical artifact names containing `phase1` or `Phase 1` remain historically
accurate provenance and are not executable names for a future cycle.

## Legacy Non-Controlling Artifacts

| Artifact | Status | Current authority |
| --- | --- | --- |
| `forseti/product/spines/commission_signal_board/dispatch_rules/forseti_demand_gate_run_commission_criteria_v0.md` | Historical only; not a live CSB dispatch rule | Use the CSB prompt and playbook. CSB is an evidence/signals-only board and must not emit admit/hold/fail gate verdicts. |

## Boundaries

CSB owns commission profiles, source-family requirements, time posture, and
typed gaps/requests. Scanning owns the intelligent walk, exact-query and
category-aware hidden-venue discovery, negatives, access notes, and frontier
closeout. Capture owns lawful source access and preservation adapters. CSB does
not contain venue or research modules and does not fake either downstream act.
CSB defines material information jobs and candidate routes; it does not freeze a
participant packet, decide final inclusion, or declare acquisition complete.
Every included item needs a named decision-material job and no equal-or-better
included substitute.

For recurring or actively radarred source families, CSB routes a lake-first
preflight before external Scanning or Capture: relevant Silver/current view,
then packet or catalog inventory, then raw material when needed. Lake inspection
tests reuse, freshness, and coverage only. It is not proof of current external
reality; absence from Silver is not absence from the lake or the world, and a
missing read model does not block acquisition.

This spine does not authorize retrieval, scraping, capture, graph construction,
demand classification, forecasting, judgment, buyer proof, validation,
readiness, CI, hook wiring, or runtime work. Public-reaction engagement belongs
in CSB as resonance/routing context only; the authority and prompt artifacts keep
it separate from proof, Commit/Scale support, graph weight, classifier mapping,
final resonance weight, and Action Ceiling.

The executable validator remains at
`.agents/hooks/check_commission_signal_board_output.py`. The executable tests
and fixtures remain under `forseti-harness/tests/`.

Company reports remain one-company-at-a-time and decision-neutral. They may use
bounded comparator pointers to interpret the subject, but deep competitor
treatment requires a separately named follow-up commission. Their Company
Surface ledger is candidate-only: no import, identity resolution, stored
corpus, or Company Surface mutation occurs in CSB.

## Old Paths

The old CSB doc paths under `docs/` are absent on current `main`. Use the
moved-path index before following historical links or older handoff packets:

```text
forseti/product/spines/commission_signal_board/migrations/moved_paths_index.md
```
