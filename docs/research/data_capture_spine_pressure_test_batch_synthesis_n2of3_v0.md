# Data Capture Spine Pressure-Test — Batch Synthesis (Interim, N=2 of 3) v0

```yaml
retrieval_header_version: 1
artifact_role: Research synthesis report
scope: Interim (N=2 of 3) cross-slot evidence synthesis for the Data Capture Spine pressure-test batch. Organizes slot-1 (M&I) and slot-2 (Teal) capture evidence, the accumulated source-access requirement set, and the recurring discharge-vocabulary signal. Evidence-only; not a batch verdict and not product authority.
use_when:
  - Reviewing what slots 1-2 of the Data Capture pressure-test batch have surfaced before running slot 3.
  - Checking the accumulated fetcher-spec set and the discharge-vocabulary findings across captures.
  - Preparing the eventual (post-slot-3) commissioner batch verdict and patchable-vs-architecture classification.
authority_boundary: retrieval_only
open_next:
  - slot1_mi_CAPTURE_operator_workfile.md # nonresolving: operator workfile, never committed
  - slot2_teal_CAPTURE_operator_workfile.md # nonresolving: operator workfile, never committed
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - Slot 3 runs and supersedes this interim synthesis with the full N=3 picture.
  - The commissioner renders the batch verdict or the patchable-vs-architecture classification (this synthesis then becomes historical input).
  - The obligation contract or commissioning plan is materially revised or superseded.
  - Either the slot-1 or slot-2 workfile is materially revised.
```

- Status: `BATCH_SYNTHESIS_INTERIM_N2_OF_3`
- This is **evidence organization**, not a verdict and not product authority.

## What this is / is not

**Is:** a cross-slot organization of the evidence from slots 1-2 of the Data Capture Spine pressure-test batch — the state spreads, the accumulated source-access (fetcher) requirement set, the recurring discharge-vocabulary signal, the architecture's resilient parts, and what slot 3 would resolve.

**Is not:** the batch verdict; the patchable-vs-architecture-threatening classification; a contract amendment; an obligation-state/handoff call; a promotion of any candidate state, spec, or finding; a product, proof, readiness, or validation claim. Those remain owner/commissioner decisions, and the batch verdict is premature at N=2 (slot 3 pending). Per the commissioning plan's count thresholds, a single capture's finding is not a standalone invalidation.

## Batch status: N=2 of 3

| | Slot 1 (M&I) | Slot 2 (Teal) | Slot 3 (forums/reviews) |
| --- | --- | --- | --- |
| Source family | finance-specialized content + bundle/pricing + archive | AI-generic resume-tool changelog/pricing/feature + archive | forum threading + anonymous actors + deletion/edit/lock + review recency |
| Access environment | reachable; **paraphrase** capture (WebFetch not verbatim) | **full host block** (tealhq.com 403 + web.archive.org content tool-block) | *pending* — expected reachable; different stressors |
| State spread | 9 `met` / 6 `partial` / 1 `n/a` | 8 `met` / 4 `partial` / 1 `n/a` / **3 out-of-vocab gaps** | — |
| Out-of-vocab states | none (but #12 → *indeterminate*, F-C) | #6, #12 `cannot_assess`; #16 `insufficient` | — |
| Handoff | `visible_stop` (+ `re-capture_posture`) | `visible_blocker` (+ `re-capture_posture`) — harder | — |
| Pass-1 checker | `capture_closure_blocker` | `capture_closure_blocker` | — |
| Pass-2 checker | `vocabulary_divergence` (1 HARD look-alike: "rejected") | `vocabulary_consistent` (all labeled proposals) | — |

Source workfiles: [slot1_mi_CAPTURE_operator_workfile.md](../../slot1_mi_CAPTURE_operator_workfile.md), [slot2_teal_CAPTURE_operator_workfile.md](../../slot2_teal_CAPTURE_operator_workfile.md). <!-- # nonresolving: untracked root operator workfiles, never committed -->

## The accumulated source-access requirement set (a real batch output)

The fetcher specs are growing **empirically from real access failures**, not abstract design — consistent with the obligation contract's "do not harden from abstract reasoning" intent:

1. **Verbatim + structure preservation** — no paraphrase as system of record (slot 1, findings F-A/F-B).
2. **Archive snapshot content retrieval** — `web.archive.org` content reach (slot 1 #10; **re-confirmed** slot 2 #10 — two data points = load-bearing, not a one-off). Slot-2 operator note: low priority.
3. **Multimodal / screenshot capture** — for layout/packaging-dependent pages (slot 1 #13).
4. **Anti-block / 403-handling access** — a fetch path that survives an origin/edge 403 to *public* pages (slot 2 — **new**; slot 1's live site was reachable, so this mode did not exist there).

Each slot's access environment surfaced a distinct requirement. Slot 3 (forums/reviews) will plausibly surface a 5th around deletion/edit/lock-state and review-recency capture.

## Strongest cross-slot signal: the discharge vocabulary under degraded access

- **Slot 1:** #12 fairness ceiling became *indeterminate* (F-C) — the **1st reach** for a missing 7th state (`cannot_assess`), but `partial` still fit elsewhere; the vocabulary **strained but held**.
- **Slot 2:** the reach **recurred** (#10), then the vocabulary **broke** at the content obligations — #6 and #12 recorded as explicit `cannot_assess` gaps and #16 as an `insufficient` gap (a *second*, distinct missing state: judged-but-not-met, vs unjudgeable). Findings S2-2, S2-3, S2-5.

So **2 of 2 captures reached for discharge states the contract lacks, and the severity escalated with access degradation** (paraphrase → full block). Slot 2 surfaced **two** candidate missing states:
- `cannot_assess` / `indeterminate` — obligation is *unjudgeable* (zero observable to assess);
- `insufficient` / `assessed_not_met` — obligation is *judged and not satisfied* due to a capture access-failure (no clean home among the 6, since `partial` overstates, `unavailable_by_source` conflates blocked-with-not-exposed, and `blocked` is reserved for the boundary per F-D).

### The distinction that bears on the deferred classification

In slot 2 the operator reached for missing *vocabulary states*, **not** for tooling/runtime to *function*. This does **not** cleanly match any architecture-threatening criterion enumerated in the commissioning plan ("operators needing runtime to function," "hidden Judgment language," "rubber-stamp checker output"). It may be a category the plan did not anticipate — a discharge-vocabulary expressiveness gap. The commissioner's call is therefore structured as:

- **(P) Patchable** — extend the discharge-state set by 1-2 states (`cannot_assess`, `insufficient`/`assessed_not_met`); bounded vocabulary change, architecture shape unchanged (slot-1 F-C was disposed *patchable*). The evidence leans here: the operator wanted states not runtime; the checker discriminated; failure-visibility held.
- **(A) Architecture-threatening** — the discharge model itself is mis-shaped for degraded/blocked access. The pull toward this: the plan's count logic (2/3 at the same criterion = pause-and-review) *if* "reached for a missing state" is read as one criterion firing twice; and the plan's "1-of-3 patchable *unless* unambiguous and severe in itself" carve-out, which the full-block inexpressibility may or may not clear.

**This synthesis does not pick (P) or (A).** It surfaces the decision structure and the evidence.

## What held (the architecture's resilient parts)

- **Operator-led discipline held in both slots** — slot 1: the agent declined to take the #13 call (F-G); slot 2: the operator self-caught a #13 capture-time downstream-use smuggle (S2-4). The "operator makes every state/handoff/classification call" line did not slip.
- **F-D (tool-block ≠ boundary `blocked`)** was load-bearing and held in both.
- **The LLM checker discriminated in both slots** — 0/2 rubber-stamps; pass-1 returned a real `capture_closure_blocker` each time; pass-2 caught a look-alike prose collision in slot 1 and was correctly clean in slot 2. A good data point for the v2-with-LLM-checker coupled hypothesis (the checker is not decorative). **Coupling to keep in view (S2-6):** slot-2 pass-1's Q1 closure-blocker was substantially driven by the operator's choice to record explicit gaps — "the checker caught it" is partly entangled with "the operator surfaced it."
- **Failure-visibility obligations (#11, #14) strengthened under a full block** — the block is cleanly recordable; these were slot 2's clean `met`s.

## What slot 3 resolves (UPDATED 2026-05-29 — earlier "expected reachable" assumption falsified)

**Correction:** slot 3 was *designed* as the reachable forum test, but the subagent run came back **access-blocked at multiple layers** — Reddit fully empty (host-block + zero `site:reddit.com` results), WSO 403 on all bodies (but ~131 **verbatim titles** + flagged snippets captured), `web.archive.org` blocked, and Claude-in-Chrome browser-automation *also* declines both `reddit.com` and `wallstreetoasis.com` via a tool-policy "safety restrictions" denylist. So both agent transports fail, by different mechanisms. Slot 3 is therefore a **third access-degraded capture**, not the reachable counterfactual — unless the operator supplies thread bodies via their own browser (slot-3 fork B1). Slot-3 raw material: `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot3_nontarget_forum_subagent_output.md`.

What slot 3 can still resolve:
- **Shape difference:** slot 3 captured *partial* verbatim observable (~131 WSO titles), unlike slot 2's near-zero. If its content obligations (#6/#12) land as `partial` rather than `cannot_assess` gaps, that is evidence the vocabulary gap is specific to **zero-observable** captures, not access-blocks generally.
- **If run reachable (fork B1):** it finally tests the intended forum stressors — #7 anonymous actor identity, #12 thread/reply chains, #10/#11 deletion/edit/lock posture, review recency — and whether the vocabulary gap recurs on a *different* failure mode.

The (P)-vs-(A) call remains the commissioner's; slot 3 (whichever fork) is the N=3 input. Continuation handoff: `docs/prompts/handoffs/orca_data_capture_pressure_test_ca_handoff_prompt_v0.md`.

## Deferred — explicitly NOT decided here (owner/commissioner)

- The patchable-vs-architecture-threatening classification of the discharge-vocabulary gap.
- Whether to add `cannot_assess` and/or `insufficient`/`assessed_not_met` to the obligation contract (contract amendment).
- Formal adoption of the pass-2 vocabulary-consistency checker into the commissioning plan (tracked: `docs/hygiene/queue.md` ORCA-HYGIENE-003).
- The batch verdict (premature at N=2; slot 3 pending).
- Any promotion of candidate operating controls, specs, or findings to stable/inherited status.

## Cross-references

- Obligation contract (6 discharge states; agent allow/forbid line): `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.
- Commissioning plan (slot frames; invalidation criteria; count thresholds; LLM-checker scope): `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`.
- Pass-1 checker prompt: `docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md`.
- Pass-2 checker prompt (pinned this batch): `docs/prompts/data_capture_spine_pressure_test_llm_vocabulary_consistency_checker_prompt_v0.md`.
- Slot findings: slot 1 F-A..F-H; slot 2 S2-1..S2-6 (in the respective workfiles).

## Non-Claims

This synthesis does not claim or constitute: validation; hardening; readiness of any kind; buyer or willingness-to-pay proof; the batch verdict; the patchable-vs-architecture classification; a contract amendment or state promotion; obligation-state, per-slice, handoff, or classification calls; product authority; source-of-truth status; or any implementation, runtime, tooling, scraper, automation, schema, or deployment authorization. It is interim evidence organization at N=2 of 3, pending slot 3 and the commissioner's decisions.
