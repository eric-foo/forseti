# Demand-Substrate Hard Gate Paper Check Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (lane commission — product planning family)
scope: >
  Commission one bounded OUTCOME-AWARE lane to dress-rehearse the
  Demand-Substrate Hard Gate and the discovery brief's slot columns on paper
  against the four batch-1 beauty cases and candidate-pool rows — no
  capture, no web research, no buyers, no edits to the instruments. Output:
  a calibration report with per-case gate walks and PROPOSED clarifications,
  adjudicated by the commissioning lane. Closes gaps BP-2 and DB-2.
use_when:
  - Dispatching the gate paper-check commission (owner word 2026-06-12, "okay lets do that... let's prompt out for this").
authority_boundary: retrieval_only
status: AUTHORED_2026-06-12_AWAITING_DISPATCH
adjudication_route: ICP / product-direction lane (commissioning thread) adjudicates the report and any proposed instrument patches; owner signs.
contamination_notice: >
  This lane becomes OUTCOME-EXPOSED on the batch-1 beauty cases and the pool
  rows it reads. It can never later serve as a blind contestant on those
  subjects. Record this exposure in the report.
```

## Commission

Walk every batch-1 beauty case (ledger cases 3-6) and every candidate-pool
row through (a) the buyer-proof packet's Demand-Substrate Hard Gate and
(b) the discovery brief's slot-table columns, exactly as written, using only
in-repo material. The intended decision: does the gate work as an
instrument — are its checks answerable, discriminating, and unambiguous —
or which specific clause is vague, and what dated clarification would fix
it? The gate has never been run, even on paper; the first user must not be
defining it by improvisation mid-scan or mid-conversation.

Owner authorization basis (2026-06-12, in-thread): "okay lets do that.
expand though - whose lane it is first" — lane assignment resolved: a
commissioned outcome-aware lane, adjudicated by the ICP / product-direction
lane ("this lane will be held here just for adjudicating their input").

## Start Preflight (required; `orca_start_preflight` fields)

- Read `AGENTS.md` and `.agents/workflow-overlay/README.md` fresh before any
  work (not supplied by this prompt).
- Source pack: bounded custom pack — the SOURCE-LOAD list below.
- `repo_map_decision: not_needed` — `repo_map_reason:` all targets are
  pinned by exact path below; no routing required.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`. Spin up per the
  AGENTS.md isolation rule: fresh worktree or branch off `origin/main`.
- Base freshness gate: pinned sources must exist at the pinned sha256
  prefixes (first 16 hex). Missing/drifted → `BLOCKED_STALE_BASE`, report
  back (the commissioning lane's batch may not have landed on `main` yet).
- Dirty-state allowance: fresh worktree, clean; only the report file new.
- Edit permission: `docs-write`, limited to the single report path. The
  packet, brief, ledger, and pool are READ-ONLY — proposed patches go in the
  report as PROPOSED text, never applied.
- Output mode: `file-write`.
- Doctrine boundary: no doctrine changes; gate/brief amendments are
  adjudicated upstream.
- External source boundary: NO public web research, NO capture. If a gate
  column cannot be assessed from in-repo material, the recorded answer is
  `needs scan-time evidence` — that is itself a calibration finding, not a
  license to browse.

## Method And Source Contract (source-gated)

REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY before
`SOURCE_CONTEXT_READY`.

SOURCE-LOAD (pins = sha256 first-16-hex at authoring):

- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — `732C65BEBFC31DA1` — the gate text under test (the "Demand-Substrate Hard Gate" section) plus disqualifiers.
- `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md` — `48B5534E056FD42A` — the slot-table columns under test + stop rules.
- `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` — `FCC8361C2C9A1D42` — READ-ONLY; the four beauty cases (3-6). Do not edit, do not re-declare, do not touch cases 1-2.
- `docs/product/foundation/consumer_demand_candidate_pool_handoff_v0.md` — `19009D43A7C29858` — READ-ONLY; the 14+2 pool rows.
- `docs/product/foundation/beauty_venue_card_set_v0.md` — `65E22CDAE5EDE781` — venue families and access shapes (for the "≥2 independent venue families" walks).
- `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` — `BC478D890419B2B6` — PROPOSED read grammar; cite as context only, flag (don't resolve) any gate-vs-taxonomy tension.

Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` before applying
any method or judging any case.

## Scope And Deliverable

One artifact: `docs/product/product_lead/orca_demand_substrate_gate_paper_check_v0.md`,
containing:

1. **Per-case gate walk** (each batch-1 beauty case, each pool row): every
   gate clause and every brief column answered `pass` / `fail` /
   `ambiguous` / `needs scan-time evidence`, with the in-repo evidence cited.
2. **Ambiguity findings**: each clause that forced a judgment call the text
   does not settle (e.g., what counts as "independent" venue families; how
   much costly-behavior evidence is enough), with `minimum_closure_condition`
   (the required end state) and `next_authorized_action` per finding.
3. **PROPOSED clarifications**: dated amendment text for the packet and/or
   brief — proposed in the report only, never applied.
4. **Discrimination check**: does the gate actually separate cases, or does
   everything pass/fail together? If it doesn't discriminate, say so plainly.
5. **Contamination record**: the outcome-exposure notice with the list of
   subjects this lane is now exposed on.

## Hard Constraints

- Findings-first; no formal verdicts, no readiness claims, no patch queue.
- No edits outside the report path; no capture; no web; no outreach.
- All claims product_learning-tier or below; `no_durable_evidence` for
  anything above.
- Do not stretch the gate to make a case pass; a failing walk is a valid
  result.

## Output Contract

`file-write`. On completion: write the report, then return a headed human
summary (gate verdict-in-plain-terms, top ambiguities, whether it
discriminates) plus path + sha256 receipt to the commissioning thread for
adjudication. If blocked, return the precise blocker.

## Non-Claims

Paper calibration only — not validation, not gate clearance, not case
execution (the batch-1 anti-leak execution gate stands untouched; this
commission must not run, score, or judge any case), not readiness.
`model_lane: unbound`.
