# Summer Fridays Understanding Dogfood - Standalone Acquire & Seal Commission v2

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff / execution-inert producer commission
scope: Defines the standalone producer for the paired Summer Fridays Understanding Turn A dogfood; authoring grants no execution authority.
use_when:
  - Dispatching this producer after a separate visible owner launch authorization.
  - Verifying the paired producer commissions share the exact common contract.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
branch_or_commit: c06f2be9e189a02bdad300538966277a075b5bc5
```

## Prompt Preflight

`preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated inline.`

```yaml
output_mode: file-write
template_kind: none
edit_permission: docs-write
workspace: C:\tmp\forseti-sf-understanding-dogfood-20260723-p02-standalone
branch: codex/sf-understanding-dogfood-20260723-p02-standalone
required_revision: c06f2be9e189a02bdad300538966277a075b5bc5
revision_mode: exact
dirty_state_allowance: clean at release; no pre-existing in-scope output
input_prompt_source: docs/prompts/handoffs/summer_fridays_understanding_dogfood_standalone_20260723_v2.md at the couriered authoring commit
commission_board: docs/research/summer_fridays_understanding_dogfood_20260723_p02/standalone/commission_board.md
acquisition_record: docs/research/summer_fridays_understanding_dogfood_20260723_p02/standalone/turn_a_acquisition_record.md
acquisition_seal: docs/workflows/summer_fridays_understanding_dogfood_20260723_p02/standalone/acquisition_seal.md
data_root: C:\tmp\forseti-sf-understanding-dogfood-20260723-p02\standalone\data
common_block_id: sf_understanding_dogfood_20260723_p02_common_v3
common_block_sha256: fe76bfd1e29b3c243ea34a6c0087a5ab390af1429022af8f56a392573d2fdb42
common_block_sha256_rule: SHA-256 of UTF-8 bytes of the lines strictly between the COMMON_COMMISSION_BLOCK markers after CRLF/CR-to-LF normalization, LF-joined, with no trailing LF
doctrine_change: none
source_pack: custom - paired company Turn A authorities and selected retail capture interfaces
repo_map_decision: not_needed
repo_map_reason: named sources, runtime revision, outputs, and validation routes are bound
controlling_source_state: clean_at_required_revision
untracked_files_in_scope: false
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: arm commission board, Turn A acquisition record, acquisition seal, and arm data root
  dirty_state_checked: yes
  blocked_if_missing: required source, exact receiver binding, capability equality, or release field
```

## Dispatch Gate

This artifact is execution-inert when authored. It authorizes no task creation, live web access, acquisition, output write, commit, push, PR, merge, Deliver, or adjudication. Proceed only after a later visible owner instruction authorizes this exact paired run and a mechanical dispatcher supplies a valid `PAIR_RELEASE`. Otherwise return `BLOCKED_EXECUTION_AUTHORIZATION_MISSING` before source-heavy work.

The dispatcher verifies bindings and releases both arms; it cannot research, interpret evidence, choose routes/follow-ups, or contribute to a seal.

`PAIR_RELEASE` is forbidden until each producer is a distinct Codex managed-worktree task whose registered task `cwd` and `git rev-parse --show-toplevel` both equal that arm's `workspace`. Prompt text, a launch-root path, or a claimed effective target does not bind the receiver. Each receiver observes clean `HEAD == required_revision` and no concurrent writer, then creates a unique `.receiver_write_proof_<PAIR_ID>_<ARM>.tmp` at the worktree root, fresh-reads the exact nonce, deletes this expressly temporary proof, and verifies absence. The dispatcher carries only these mechanical receipts. Any mismatch or failed create/read/delete blocks both arms before source-heavy work.

Before source-heavy work, the arm seal owner recomputes the common-block digest from its couriered copy under `common_block_sha256_rule` and compares it with both the preflight value and the `PAIR_RELEASE` value. A mismatch or inability to recompute returns `BLOCKED_EXECUTION_AUTHORIZATION_MISSING`; never proceed on or report a hash merely copied from this prompt.

<!-- COMMON_COMMISSION_BLOCK_START -->
## Frozen Common Commission

### Purpose and success target

Produce a decision-neutral, evidence-accountable Summer Fridays company Understanding substrate through Turn A Acquire & Seal. A cold producer must execute without prior chat and finish with either an honestly passing phase acquisition seal or `BLOCKED_ACQUISITION_INCOMPLETE`. This target is a later review axis to attack, not a pass bar graded against this prompt.

```yaml
pair_id: sf_understanding_dogfood_20260723_p02
common_commission_id: sf_understanding_dogfood_20260723_p02_common_v3
subject: Summer Fridays
subject_type: Brand_or_Org_identity_to_verify
commission_profile: company_competitive_intelligence
mode: forward
phase: understanding
turn: acquire_and_seal
time_posture: recency_first
source_revision: c06f2be9e189a02bdad300538966277a075b5bc5
target_market: US_first
as_of_date: supplied_once_in_PAIR_RELEASE_as_the_shared_UTC_release_date
```

The mechanical dispatcher supplies `PAIR_RELEASE` with pair ID, exact source revision, common-block hash, shared UTC release time/date, the shared operator-asserted active US VPN state, two verified receiver/root identities, and equal source/tool/credential capability per evidence actor. Any mismatch blocks both arms.

### Bound question and limits

> What does current public evidence show about Summer Fridays as a company and brand system - its proposition, owned and retailer-expressed portfolio architecture, markets and channels, strategic and operating motion, material events, customer and community response, visible concentrations and dependencies, contradictions, strong and weak links, and observable tensions warranting later Problem Framing?

Observable tensions are evidence-bounded seams only. Do not assign pain severity, ICP, urgency, willingness to pay, opportunity size, commercial response, or a recommended attack.

Resolve five high-yield jobs: current offering/portfolio architecture; exact current commercial/retail expression where material; channel/distribution/geography posture; strategic/operating chronology; applicable material events. Cover nine lenses: portfolio and retail architecture; observable positioning; offerings/claims; markets/channels; recent strategic/operating moves; customer/community response; bounded competitor/substitute context; contradictions; evidence gaps.

Deep competitors, archives, supply, creators, advertising, search trends, international expansion, and legal investigation activate only for a named unresolved inference job. No ICD 203, longitudinal proof, universal deep capture, complete global SKU graph, or unsupported forecast.

Optimize toward question fit, evidence foundation, reasoning quality, honest uncertainty, implications and foresight, and communication efficiency. Here, implications/foresight means supported implications and observable change conditions, not forecasts or recommendations. These signals are not scores, quotas, sections, or completion credits.

### Required reads and contamination ban

Read targeted sections at the exact revision:

1. `AGENTS.md`; overlay README, source-loading, and decision-routing.
2. Company-intelligence architecture: common substrate, high-yield core, portfolio/retail architecture, claim ceilings.
3. CSB authority: Intelligence Cycle, six signals, company extension.
4. CSB playbook: Turn A, acquisition seal, validator boundary.
5. Tiered-retail handoff: frozen decisions, capability state, Step 6, drift guard.
6. Data Capture map, Retail/PDP README, storefront-pin registry, and selected route authorities.
7. Current interfaces/tests for grid projection, portfolio onboarding, selected supported retailer routes, review overlap, and CSB validation.

Passing tests or landed code prove interface behavior only, never live route admission or evidence sufficiency.

Do not read or reuse prior Summer Fridays packets, reports, receipts, hero selections, conclusions, gap reviews, browser history, or the evidence world at `C:\tmp\forseti-summer-fridays-understanding-handoff`. Historical identity may be checked only to prevent a path collision.

### Commission-stage validation and Turn A boundary

Generate the full commission-stage company CSB with Sections 1-10 and `run_boundary: COMMISSION_SEALED_PRE_SCAN`. Validate before source-heavy work:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py <ARM_COMMISSION_BOARD>
```

Repair findings or stop. This is the only company-output validation in Turn A. Later completed-company-output validation is future-only: this run creates no Turn B company report. The phase acquisition seal is manually adjudicated against the playbook gate.

### Acquisition route

1. Capture owned subject/ownership identity, categories, franchises, parents, material variants, bundles/sets, claims, price architecture, channels/geography, chronology, and material events. Owned evidence is canonical identity authority. Independently verify owned-census provenance because its `source_packet_id` is not dereferenced by the compositor.
2. Before probing any retailer, capture and fresh-read Summer Fridays' current official `https://summerfridays.com/pages/authorized-retailers` surface. File a retailer-admission board recording each named retailer, observed US-facing relevance, available capture capability, distinct material evidence job, and `PRIMARY|SECONDARY|EXCLUDE|BLOCKED` disposition. A retailer not named there is never mandatory; an observed unnamed route may be probed only for a named contradiction job and never proves authorization.
3. Select one officially named, US-facing, route-supported retail primary by breadth, exact identity, and non-duplicative evidence yield. Capture its complete reachable brand grid, reconcile every verified row to the owned denominator, and capture one baseline PDP per exact non-bundle primary listing. Keep other officially named, material, route-supported retailers in one unified secondary corpus, but capture them shallowly and deepen only for discriminating assortment, commercial, seller, provider, review, or access evidence. Do not force Sephora, Ulta, Target, and Amazon as a quartet.
4. Preserve `PARENT|VARIANT_URL|BUNDLE_SET` and `EXACT|AMBIGUOUS|UNMATCHED`. Separately type baseline state as `CONTENT_BASELINE_ADMITTED|RAW_BASELINE_CAPTURED_EXTRACTION_FAILED|ACCESS_FAILED|IDENTITY_FAILED`. Compact-extraction failure never converts an otherwise sufficient exact raw page into absent acquisition: preserve the raw packet and extractor failure, use only facts verified from that page, and never claim unrecovered compact fields.
5. Select review/Q&A depth only after breadth and only for named non-duplicative jobs. The five-job core cannot replace customer/community evidence.
6. Map onboarding rows to raw references and capture-job IDs. Link by provider/native ID, explicit syndication, then normalized exact fingerprint. Preserve all occurrences; ambiguous conflicts remain unmerged. Q&A stays source-local.
7. Run a bounded category-aware Reddit scout. Capture community evidence only for a named non-dominated job. Serious customer-response seams require an independent or discriminating check.
8. Use existing observation, coverage, gaps/requests, completion, provenance, and seal surfaces. Add no standing schema.

Run from `forseti-harness`, binding `<ARM_DATA_ROOT>` to the arm destination:

```powershell
python runners/run_source_capture_cloakbrowser_packet.py --url <GRID_URL> --source-family retail_pdp --decision-question "<BOUND_QUESTION>" --data-root <ARM_DATA_ROOT> --retail-capture-profile <GRID_PROFILE> <COUNTRY_OR_OPTIONAL_LOCAL_CONTEXT_ARGUMENTS>
python runners/run_retail_grid_projection.py --packet-dir <GRID_PACKET_DIR> --output <GRID_PROJECTION_JSON>
python runners/run_retail_portfolio_onboarding.py --commission <PORTFOLIO_COMMISSION_JSON> --output <PORTFOLIO_OUTPUT_JSON>
python runners/run_retail_review_overlap.py select-depth --commission <DEPTH_COMMISSION_JSON> --output <DEPTH_SELECTION_JSON>
python runners/run_retail_review_overlap.py link-reviews --commission <LINKAGE_COMMISSION_JSON> --output <REVIEW_LINKAGE_JSON>
```

Use only profiles justified by the retailer-admission board. Sephora uses `--sephora-market US`. Ulta uses `--ulta-market US` only if the official-current or contradiction-job rule admits it. Amazon `.com` and Target `.com` need no ZIP for US-facing catalog/PDP capture under the operator-asserted active US VPN; preserve observed currency and marketplace markers. A delivery/target ZIP is optional and may be supplied only for a named local fulfillment job.

Any ZIP binds only retailer-visible local delivery, shipping, pickup, or fulfillment context. A requested pin failure remains a typed local-context failure but does not discard otherwise sufficient catalog/PDP content or a completed grid projection. No ZIP, VPN, `.com` route, or `NOT_LISTED` result supports nationwide availability, stock, distribution, authorization, or absence. Amazon completeness covers only the declared query and reachable ranked-search window, never a complete or authorized-only brand catalog.

For selected depth, use an implemented onboarding runner only when its retailer was admitted for a named evidence job, with the arm data root and exact parent packet ID. Amazon onboarding is bounded native PDP top-review evidence, not equivalent Helpful/Recent, Q&A, or a complete corpus.

### Failures, stopping, and seal

Retailer outcomes are exactly `GRID_CAPTURED_COMPLETE`, `GRID_CAPTURED_INCOMPLETE`, `NOT_LISTED`, `ROUTE_BLOCKED`, `MARKET_UNPINNED`, or `SURFACE_NOT_EXPOSED`. Apply them only to retailers admitted by the official-first board or to an expressly named contradiction probe. Use `NOT_LISTED` only after an admitted sufficient surface and only for that observed US-facing surface; it never supports nationwide absence, authorization, or a distribution-gap claim. Incomplete grids receive no closure credit.

Keep identity ambiguity, unmatched rows, missing variants/baselines, provider ambiguity, insufficient customer evidence, and unresolved seams visible. Syndicated reviews never become independent corroboration.

Every material seam must be supported, contradicted, meaningfully bounded, or honestly blocked. A touched lens, source/retailer count, zero-yield route, validator pass, or typed gap cannot manufacture sufficiency. Stop only when the acquisition floor holds and no remaining lawful, safe, non-dominated route has materially positive value for an unresolved material job; otherwise block the seal.

For one owner-fixable load-bearing failure, issue the playbook's consolidated owner-unblock escalation. The mechanical dispatcher may forward it verbatim and return the arm-scoped answer but may not interpret evidence or design recovery. A common scope/question change invalidates both runs and requires new pair IDs/common block.

Write the commission board, Turn A acquisition record, and phase acquisition seal to arm destinations. The record includes route results, receipts/provenance, denominator verification, reconciliation/baselines, depth/linkage mappings, seams/follow-ups/failures, escalation, and descriptive effort.

Manual seal adjudication permits `SEALED_READY_FOR_DELIVER` only with `acquisition_gate: pass`, `deliver_allowed: true`, truthful required-route dispositions/receipts, and evidence sufficient for the bound question. Otherwise use `BLOCKED_ACQUISITION_INCOMPLETE`, `acquisition_gate: blocked`, and `deliver_allowed: false`.

No Turn B report, later company-output validation, Problem Framing, or comparative adjudication may begin.

### Fairness and isolation

Exactly five evidence actors exist: `SA0` and `CO0-CO3`. Any pair-release dispatcher is mechanical, not a sixth analytic actor. Both arms share this byte-identical block, revision/date, question/use, floor, ceilings, failures, stopping rule, capability class, and unblock mechanism.

Use separate worktrees, branches, browser profiles, caches/downloads, data/artifact roots, ledgers, and seals. Do not promote arm records into a shared current view before both seals. Producers never read the sibling arm; the dispatcher never relays sibling evidence or progress. Counts, time, tokens, and calls are descriptive costs, never quotas. A topology breach, cross-read, prior-evidence use, or shared-output reuse invalidates the affected arm.

Durable blind-adjudication prompt authoring is deferred until both actual seals exist so it can bind their real paths and hashes. No evaluator-only criteria belong in producer prompts.

### PLANNED_NOT_OBSERVED signals

- Cold launchability/topology: exact clean receiver, common hash, no inherited Summer Fridays context, exactly five evidence actors, mechanical dispatcher only.
- Comparable independence: equal evidence contract/capability, isolated outputs; a common outage or timing drift cannot be mistaken for topology quality.
- Correct-cause closure: the official-first retailer board, resolved material jobs, and verified receipts cause a passing seal, not a forced retailer quartet, counts, a wrong denominator, Amazon window completion, a typed gap, or validator pass.
- Deterministic preservation: raw refs verify, native occurrences survive, fresh-output replay is deterministic, ambiguous conflicts stay unmerged.
- Phase integrity: commission-stage CSB validated, seal manually adjudicated, no Turn B report or premature later-output validation.

Live route admission, denominator correctness, evidence sufficiency, seam yield, and comparative quality remain unobserved until the authorized runs and later blind adjudication.
<!-- COMMON_COMMISSION_BLOCK_END -->
## Standalone Topology

```yaml
cycle_id: sf_understanding_20260723_p02_sa
commission_id: sf_understanding_csb_20260723_p02_sa
evidence_actor: SA0
topology: completely_standalone
delegation: prohibited
subagents: prohibited
task_creation_by_SA0: prohibited
seal_owner: SA0
```

`SA0` performs the entire Acquire & Seal run: source resolution, commission-stage CSB and validation, owned/retailer acquisition, reconciliation/baselines, selected depth, community evidence, seam tests/follow-ups, accounting/escalation, and manual seal adjudication. Direct tools are allowed only after release; delegating, spawning helpers, creating another task, or asking the dispatcher to reason is a topology failure.

## Return

Fresh-read durable targets, then return: arm/actor, revision, the recomputed common hash, board path and validation exit, acquisition-record path, seal path/state/gate/deliver flag, material failures, unblock status, contamination/topology status, and the observed `turn_b_started` value. Every field is reported as observed, never copied from this prompt; `turn_b_started: true` is a reportable phase failure, never a silent pass.

Lifecycle actions remain governed by the `lifecycle_hard_stop` constant in `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`; this commission grants none of them.
