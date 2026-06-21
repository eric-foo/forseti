# Screening-Capture Hybrid MGT Strategy Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Paste-ready strategy prompt for a ChatGPT-style reasoning lane to weigh the
  mini-god-tier shape for combining screening reads with capture, including
  screen-gated, delayed-commit, direct-capture, and boundary-collapse variants,
  using the current screening-read build as context.
use_when:
  - Asking an external reasoning model to adjudicate screening-read versus capture
    hybrid architecture.
  - Weighing pros and cons of screen-gated capture, single-read delayed-commit,
    direct capture exceptions, and boundary-changing hybrids.
  - Forcing accepted residuals before adopting a hybrid source-access strategy.
authority_boundary: retrieval_only
output_mode: paste-ready-chat
open_next:
  - docs/workflows/screening_read_service_build_receipt_v0.md
  - docs/workflows/screening_read_reusable_findings_v0.md
  - docs/decisions/screening_reddit_read_route_decision_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - orca-harness/source_capture/screening_read.py
  - orca-harness/source_capture/screening_browser_read.py
stale_if:
  - The screening-read API, capture packet boundary, or no-packet/no-ECR contract changes.
  - The owner changes the source-access posture for screening or capture.
  - A later architecture decision adopts a hybrid commit-gate design.
```

Paste the body below into ChatGPT or another external reasoning model.

---

You are advising Orca on source-access architecture. Your task is to decide the
Mini God Tier strategy for combining **screening read** and **capture**.

Do not implement. Do not browse. Do not claim validation, readiness, legal
sufficiency, production safety, or source-access approval. This is a strategy
adjudication prompt.

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
v0 -- constants bound; deltas stated below.

- Prompt artifact path:
  `docs/prompts/deep-thinking/screening_capture_hybrid_mgt_strategy_prompt_v0.md`.
- Authorization basis: current owner request to produce a ChatGPT strategy
  prompt for the screening/capture hybrid MGT decision.
- Output mode: `paste-ready-chat`; the receiving model returns a chat-only
  strategy memo and writes no files.
- Template kind: `deep-thinking`; no project-local deep-thinking template was
  bound, so this prompt uses the Orca prompt contract plus the source capsule
  below.
- Edit permission: `read-only` for the receiving model; no repository edits,
  patches, captures, packets, manifests, ECR records, or runtime actions.
- Target files/dirs for context only:
  `docs/workflows/screening_read_service_build_receipt_v0.md`,
  `docs/workflows/screening_read_reusable_findings_v0.md`,
  `docs/decisions/screening_reddit_read_route_decision_v0.md`,
  `docs/decisions/orca_mini_god_tier_doctrine_v0.md`,
  `orca-harness/source_capture/screening_read.py`, and
  `orca-harness/source_capture/screening_browser_read.py`.
- Branch/reference at authoring:
  `codex/screening-read-service-build` at
  `a7d90f86b7e223a9740d6bcffdbdd45ca3331453`.
- Dirty-state allowance: receiving model should assume no repo access and use
  the source capsule below; if repo access exists, it must reread the named files
  and report source-context status.
- Source pack: bounded custom source capsule from the current screening-read PR
  plus the MGT doctrine summarized below.
- Repo map decision: not needed for the receiving model; this prompt already
  names its bounded source pack.
- Doctrine change decision: the receiving model may recommend a future
  architecture/lifecycle-boundary change, but this prompt does not authorize or
  perform that change.
- Isolation decision: authored in the existing screening-read service PR worktree
  because this prompt is a continuation of that workstream.
- Validation gates for the response: source-context status stated; five options
  compared; "capture if it feels okay" evaluated with explicit pros, cons,
  safeguards, and criteria; accepted residuals named for any MGT recommendation;
  no validation, readiness, approval, or implementation claim.
- Thread operating target continuity: no active thread operating target is
  carried; this is a strategy prompt for a downstream reasoning lane.

## Objective

Decide whether Orca should combine screening and capture into a hybrid flow, and
if so what the mini-god-tier shape should be.

The owner's tempting idea is:

> Screen, then capture if it feels okay. Maybe ignore the boundary because the
> hybrid is cleaner.

Treat that as a candidate to evaluate fairly, not as an instruction to obey or
as a flaw to dismiss upfront. Weigh its advantages -- lower latency, fewer
duplicate reads, simpler operator flow, and exact same-page preservation --
against its risks: silent over-collection, hidden ECR/packet writes, vague human
judgment, and untestable source-access boundaries. If it survives, translate it
into explicit criteria, safeguards, and accepted residuals. If it fails, explain
which risks make it worse than the alternatives.

## Mini God Tier Bar

Mini God Tier means: capture most of the maximal capability's value at much
lower cost and speed than a maximal architecture, while naming the accepted
residuals. It is not a validation claim or readiness claim.

Your output must include an **accepted residuals** list. For each residual, name:

- what is left undone;
- why that is acceptable now;
- what risk remains;
- what would trigger an upgrade.

If you cannot name accepted residuals, do not call the design MGT.

## Current Build Context

Orca now has a bounded screening-read build on PR branch
`codex/screening-read-service-build` at commit
`a7d90f86b7e223a9740d6bcffdbdd45ca3331453`.

Current screening entries:

- `source_capture.screening_read.screening_read(...)`
- `source_capture.screening_browser_read.screening_browser_read(...)`
- `source_capture.screening_extraction.extract_structured_listing_candidates(...)`

Current screening boundary:

- orchestrator-invoked, not walker-direct;
- one source, one bounded question, human-rate;
- logged-out public URLs only;
- entitlement gate before fetch;
- no standing crawler, scheduler, monitor, dashboard, or production runtime;
- no new fetch/search infrastructure;
- no Source Capture Packet, no packet manifest, no packet staging;
- no ECR, Cleaning, or Judgment touch;
- browser screening returns visible text and classifies `block_shell` on visible
  text, not full DOM.

Current reusable finding:

- For browser/interstitial pages, classify the rendered visible text. Full DOM
  can retain residual challenge scripts and false-positive as blocked.
- For same-shaped listing pages, extract by targeted row/card-local locators:
  container, title anchor, optional href filter/canonicalizer, row-local
  datetime, and range-sanity guard.
- Do not use page-wide date aggregates such as `min(all datetimes)`, because
  page chrome/sidebar dates can pollute candidate dates.

Live probes of the generic extractor succeeded on public listing pages:

- GitHub Blog: 18 candidates, all row-local datetimes known.
- Node.js Blog: 6 candidates, all row-local datetimes known.
- Astro Blog: 12 candidates, all row-local datetimes known.

Known limitation of the current build:

- It proves screen-light read/extraction behavior, not a hybrid commit-gate.
- It can add latency if the same page is later captured separately.
- It can see a page state that changes before capture.
- It deliberately does not write packets/ECR during screening.

## Options To Compare

Compare these options. You may add a hybrid only if it is materially different.

1. **Pure screening then separate capture**
   - Screening reads and extracts screen-light fields.
   - If the orchestrator decides the source is worth it, a separate capture run
     happens later.

2. **Boundary-collapse hybrid**
   - Screening captures if it "feels okay."
   - The same entry can silently produce durable capture artifacts.

3. **Screen-gated capture**
   - Screening remains pure.
   - A separate orchestrator route applies explicit gate criteria.
   - If the gate passes, it invokes the normal capture path as a separate
     posture and records that the capture was triggered by screening.

4. **Single-read delayed-commit capture**
   - Fetch/render once into ephemeral memory.
   - Run screening classification/extraction on the ephemeral result.
   - If the gate fails, discard with no durable artifact.
   - If the gate passes, explicitly commit the same result into the capture
     packet path.
   - The commit moment must be mechanically explicit and testable.

5. **Direct capture for admitted/high-confidence sources**
   - Skip screening when the source is already admitted, high-confidence,
     volatile, and the question requires durable evidence.

## Decision Criteria

Evaluate each option against:

- evidence hygiene;
- latency;
- page-state drift between screening and capture;
- auditability of the posture transition;
- implementation complexity;
- testability of "nothing durable before the gate";
- fit with human-rate / public-only / no standing crawler constraints;
- failure modes if a future agent misunderstands the design;
- how well it uses the current screening-read build.

## Hard Constraints

- Do not hide capture side effects inside `screening_read`; if a design captures
  from a screening entry, name it as a boundary-changing design and define the
  explicit commit point, safeguards, and tests.
- Do not leave "feels okay" as a gate; convert it to explicit criteria before
  recommending any hybrid.
- Do not create packet, manifest, ECR, Cleaning, or Judgment side effects before
  a capture gate has passed.
- Do not weaken public-only / entitlement-first / no-auth-bypass boundaries.
- Do not propose a standing crawler, scheduler, monitor, or production runtime.
- Do not rely on broad source discovery, generic crawling, or new fetch/search
  infrastructure.
- Do not treat MGT as proof, validation, readiness, or owner approval.

## Output Contract

Return a concise strategy memo with these sections:

1. **Direct Answer**
   - Is the ideal hybrid real?
   - What are the pros, cons, and required safeguards for "capture if it
     feels okay / ignore the boundary"? Under what conditions, if any, is it
     acceptable?

2. **Recommended MGT Shape**
   - Name the target architecture.
   - State the smallest complete version.
   - State what current build pieces it reuses.

3. **Option Comparison**
   - Short table comparing the five options against the decision criteria.

4. **Gate Contract**
   - Propose explicit gate criteria for screen-to-capture promotion.
   - Include at least: content class, login/block-shell refusal, required
     extracted fields, bounded question/source id, public entitlement state, and
     no packet/ECR before gate.

5. **State Machine**
   - Name states and transitions.
   - Include `screening_read`, `screen_decision`, `capture_invoked`,
     `ephemeral_discarded`, and `packet_committed` or better equivalents.

6. **Accepted Residuals**
   - Mandatory for the MGT claim.
   - Include the residuals, risks, and upgrade triggers.

7. **Tests Required Before Build**
   - Boundary tests.
   - Gate tests.
   - No-packet/no-ECR-before-gate tests.
   - Drift/duplicate-fetch tests if relevant.
   - Single-read delayed-commit tests if recommended.

8. **Recommendation**
   - Recommend Tier 1 now, Tier 2 later, direct capture exceptions, or no hybrid.
   - Name the next artifact that should be written if the owner accepts the
     strategy.

## Starting Hypothesis To Evaluate

A plausible answer is:

- MGT is **screen-gated capture now** plus a future **single-read delayed-commit**
  upgrade if latency becomes measured pain.
- `screening_read` itself stays pure.
- The orchestrator owns the gate and invokes capture.
- "Capture if it feels okay" may be unacceptable as phrased, but could become
  viable if translated into explicit, testable gate criteria and a clear commit
  boundary.

Do not accept or reject this hypothesis automatically. Weigh it against the
alternatives and replace it if another MGT design captures more value at lower
cost with named accepted residuals.
