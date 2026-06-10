# Orca Judgment Spine Case Learning Preservation Prompt

```yaml
retrieval_header_version: 1
artifact_role: full prompt artifact
scope: Prompt for preserving compact, cross-case judgment lessons after a blind case reveal without creating a skill.
use_when:
  - A blind Judgment Spine case has a sealed judgment and a reveal.
  - A future agent needs to preserve what the case teaches for other cases.
  - A case capsule must stay structured enough to skim across many cases.
authority_boundary: retrieval_only
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S0 plus prompt-orchestration, artifact folder, product-proof, and retrieval metadata rules
  edit_permission: docs-write
  target_scope: Save a reusable prompt for future agents to preserve Judgment Spine case learning without a skill.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Prompt

You are preserving learning from an Orca Judgment Spine blind case.

This is not a skill. Do not create, install, rewrite, shadow, or promote any
skill. Use this prompt as the local operating checklist for this case only.

## Required Reads

Read the smallest source pack that can support the task:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md`
4. `.agents/workflow-overlay/product-proof.md`
5. `.agents/workflow-overlay/artifact-folders.md`
6. `.agents/workflow-overlay/retrieval-metadata.md`
7. The current case's participant packet, safety receipt, blind judgment files,
   reveal sources or reveal readout, and any adversarial review of the case
   capsule.

Do not bulk-read all cases, all review outputs, all prompts, or all research
folders. Expand only when a missing source could change the preserved lesson,
the artifact boundary, the reveal claim, or a non-claim.

## Stop Conditions

Stop and report a blocker if:

- the owner or participant blind judgment has not been sealed;
- reveal material is being introduced before a blind judgment is sealed;
- the task asks for outcome calibration but no reveal source is available;
- a participant-facing artifact would include the actual action, outcome,
  consulting recommendation, implementation status, or post-cutoff facts;
- the task requires product readiness, repeatability proof, buyer validation,
  or full backtest claims that are not supported by Orca authority and evidence.

## Output Target

Prefer writing or updating:

```text
docs/research/judgment-spine/cases/<case-slug>/reveal_readout_vN.md
```

If the case folder lacks a `case_index.md`, `blind_judgments_vN.md`, or a
Judgment Spine manifest, do not silently pretend the structure exists. Name the
missing artifact as structural residue and preserve the lesson in the reveal
readout only if the current turn authorizes docs-write.

## Required Artifact Shape

The reveal readout must be compact. It should help a future agent make a better
judgment on a different case without rereading the full case thread.

Use these sections:

```text
# <Case Title> Reveal Readout

retrieval header

## Preflight
orca_start_preflight

## Capsule
- cutoff:
- decision_question:
- actual_action:
- highest_leverage_judgment_for_this_case:
- key_transfer_lesson:
- transfer_pattern: `preferred_move | fallback_trigger | walkaway_line |
  implementation_guardrails | evidence_that_would_change_decision`
- pattern_instantiation:
  - preferred_move:
  - fallback_trigger:
  - walkaway_line:
  - implementation_guardrails:
  - evidence_that_would_change_decision:
- tactical_read: only if the case contains a counterparty offer, package,
  settlement, regulatory bargain, or similar bundle.
- tactical_read_boundary: packaging is information to preserve and test; do not
  assert counterparty intent as fact unless the source directly states it.

## What Happened
Actual revealed action, date, and source-family boundary only.

## Blind Judgments Compared
Short comparison of the sealed assistant/agent judgment and owner/participant
judgment. Do not paste long judgments if links exist.

## Material Assessment
Which judgment was materially better for this case under the visible reveal,
and why. Scope the claim to this case.

## Transferable Judgment Pattern
Generic primitive list plus a case-specific instantiation:
- preferred_move:
- fallback_trigger:
- walkaway_line:
- implementation_guardrails:
- evidence_that_would_change_decision:

## Tactical Reads
Include only when the case has source-visible negotiation, bundle, or
counterparty-offer material. Preserve what the source shows before interpreting
what it means:

### Counterparty Concession Read
What the counterparty frames as a concession, requirement, restriction,
safeguard, sweetener, or condition.

### Packaging As Signal
How bundle structure changes the read: which terms travel together, what is
framed as the trade, and what should be preserved as source-visible packaging
rather than inferred motive.

### Signal Discipline
How the decision owner should avoid confirming the full value of a quiet win
before pricing concessions, negotiating poison terms, or setting fallback
pressure.

Boundary: packaging is information to preserve and test; do not assert
counterparty intent as fact unless the source directly states it.

## Reusable Lessons
3-7 bullets. No duplicate capsule lines. Each lesson must help future cases.

## Consulting Takeaway
What a client-facing recommendation should do differently next time.

## Artifact Links
Links to participant packet, safety receipt, blind judgments, reveal sources,
and review outputs when those artifacts exist.

## Non-Claims
Preserve the required non-claims.
```

## Judgment Transfer Standard

The first quality test is:

> Can a future agent use this capsule to make a materially better judgment on a
> different case without rereading the full thread?

Optimize for that test before optimizing for completeness or elegance.

Every case learning capsule should preserve:

- the decision pattern, not just the outcome;
- the failed or incomplete reasoning move;
- the fallback trigger that would turn posture into advice;
- the walkaway line that prevents overconcession;
- the implementation guardrails that reduce downside if the ugly option wins;
- the evidence that would have changed the decision.
- the tactical read and boundary when source-visible packaging, concession
  framing, or counterparty bundle structure changes the judgment.

If a lesson does not help a future case, cut it.

The Capsule may use a two-tier shape: first the skim header fields, then the
slotted transfer block. Favor slotted depth over arbitrary line-count brevity
when the transfer test requires the slots.

## Non-Claims To Preserve

Unless later Orca authority and evidence explicitly prove otherwise, include:

- no buyer validation;
- no willingness-to-pay proof;
- no repeatability proof;
- no product readiness;
- no feature readiness;
- no implementation readiness;
- no commercial readiness;
- no Core Spine validation;
- no full backtest completed by the capsule;
- no proof that a single-case pattern transfers across cases.

## Closeout

Return a concise closeout with:

- artifact path;
- SHA256;
- whether the capsule is complete or interim;
- missing sibling artifacts or structural residue;
- checks not run;
- next authorized step.

Do not claim validation, acceptance, product readiness, implementation
readiness, or repeatability proof from this prompt.
