# Quora B2B Answering-Meta Design — Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Commission / handoff prompt (routes the Quora B2B answering-methodology design to a fresh docs lane; prepares and scopes the work, does not execute it)
scope: >
  Commissions a fresh lane to design the Quora B2B "answering meta": the
  owner-required answering methodology (channel-goal options, context
  requirements per answer, non-generic depth-of-value bar, per-question-type
  approach, tone contract, claim boundaries) that must exist before any real
  Quora answer content is drafted. Methodology-first: publishable answers stay
  out of scope.
use_when:
  - Spinning up the lane that designs the Quora B2B answering methodology.
  - Checking what the answering-meta work must read, decide, produce, and not claim.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/quora_b2b_answer_strategy_pilot_handoff_v0.md
  - docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/quora_b2b_postmerge_capture_calibration_delegated_adversarial_review_patch_v0.md
stale_if:
  - The owner decides the Quora content channel is dropped rather than deferred.
  - The calibration record's candidate table is superseded or re-run with a different candidate set.
  - The answering-meta artifact this prompt commissions exists and is owner-adjudicated (the prompt is then historical).
```

## Forseti Start Preflight (the receiving lane must establish before work)

```yaml
forseti_start_preflight:
  agents_read: required   # AGENTS.md + .agents/workflow-overlay/README.md in the current task context
  overlay_read: required
  source_pack: bounded custom pack = this commission's Required Reads (below)
  repo_map_decision: receiver records loaded | not_needed | unavailable, plus reason
  workspace: fresh worktree or branch off origin/main (docs lane; state isolation before editing per AGENTS.md)
  branch_or_revision: >
    All controlling inputs are on origin/main at or after commit 94bd3695
    (PR #829). SHA256 compare targets at commission authoring (re-read the
    files regardless; hashes are compare targets, not substitutes, and
    line-ending normalization can shift bytes):
    calibration record 80399574C4FED31B3D0732509FC580605171CE5C314787BA318DFBA393CD5B6F;
    delegated review C28566AA33EDE06B1DFDBA684D9EBF7EB25E4E5BEC3B9020FF4130A920A9A13E;
    handoff packet (post-Disposition) A60B8270BC668220C15CE123CA2343ACAE749694BFD4AA085F9EBA1DD46F794E.
  dirty_state_allowance: clean start; untracked-in-scope only for the new methodology artifact
  edit_permission: docs-write (one new methodology artifact; no code, no overlay edits, no capture runs)
  target_scope:
    - forseti/product/spines/scanning/source_families/answer_engine/quora_b2b_answering_meta_v0.md  # the deliverable (default path; see Output Contract)
  output_mode: file-write (the methodology artifact), plus a headed human summary in chat closeout
  validation_gates: git diff --check; .agents/hooks/check_retrieval_header.py --strict on the new artifact; .agents/hooks/check_placement.py --check; fresh read of touched sections before completion claims
  external_source_boundary: external workflow source is read-only; jb is not Forseti authority; no live Quora access in this lane
  doctrine_change: >
    none expected. The deliverable is DECISION INPUT (proposal status) pending
    owner adjudication, not controlling doctrine. If the receiver instead
    claims it as controlling method doctrine for future answer content, that is
    doctrine-changing and requires a direction_change_propagation receipt or
    blocker per .agents/workflow-overlay/source-of-truth.md — default is: do
    not claim it; leave adoption to the owner.
  blocked_if_missing: yes — if the calibration record or the handoff packet's Disposition section is unreachable on origin/main, STOP and report rather than reconstructing from memory.
```

## Objective And Intended Decision (what this is for / done looks like)

**Goal (fresh prose — no controlling upstream methodology exists yet; the
re-entry condition lives in the handoff packet's Disposition section, 2026-07-10):**
give the owner a decidable answering methodology for Quora B2B content — so
that when answer drafting resumes, every answer has a defined purpose, a
context bar, a non-generic value bar, and a tone contract, instead of being
generic LLM-flavored filler.

**Done looks like:** one methodology artifact that (a) proposes 2–4 channel-goal
options with a recommended default and named tradeoffs, (b) defines the
answering meta well enough that a competent writer could take one admissible
candidate row and know exactly what to establish before drafting, what depth
bar the draft must clear, what tone to use, and which claims are forbidden,
and (c) stops for owner adjudication without drafting publishable answers.

> This goal is the executor's **target + review axis-to-attack**, not a
> pass-bar graded against this prompt's wording
> (`docs/decisions/work_unit_fitness_reference_v0.md`).

## Goal Handoff

```yaml
goal_handoff:
  long_term_goal: >
    Use source-captured B2B question surfaces to produce answer-strategy
    content that is useful for Orca's B2B wedge without pretending a Quora
    capture is buyer proof.   # carried verbatim from the handoff packet's Goal Handoff
  anchor_goal: >
    Design the Quora B2B answering meta: channel-goal options + recommended
    default, context requirements per answer, non-generic depth-of-value bar,
    per-question-archetype approach, tone contract, and claim boundaries —
    as owner decision input.
  success_signal: >
    The owner can adjudicate the channel goal and the methodology in one pass:
    options are comparable, the meta is concrete enough to govern a real
    draft, sensitivity of the meta to the channel-goal choice is labeled, and
    no buyer-proof, publishable-content, or capture-reliability claim is made.
continuity_disclosure:
  prior_anchor_goal: >
    "draft a small answer-strategy pilot" (handoff packet, 2026-07-10) — executed
    once and DEFERRED by owner decision the same day; see the packet's
    Disposition section. This commission replaces it by explicit owner
    instruction ("for the answering meta - let's prompt for it"), not silently.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: none
```

## Routing

```yaml
workflow_sequence_policy: overlay_owned
workflow_sequence_source: explicit_user_instruction (owner, 2026-07-10) + accepted_project_artifact (handoff packet Disposition re-entry condition)
workflow_sequence_status: bound
receiver: fresh docs lane (model-neutral; no runtime model routing is made or implied)
```

Decision routing: run the Forseti Cynefin Routing Layer
(`.agents/workflow-overlay/decision-routing.md`) at lane start as AGENTS.md
requires for delegated work. Expected classification: complicated
(sense-analyze-respond) — source-grounded design with owner adjudication, no
live-risk probes; if the receiver instead finds genuine complexity (e.g. the
channel-goal options cannot be compared without new evidence), stop and
surface that rather than probing live surfaces.

## Required Reads (source-gated)

`REFERENCE-LOAD` (procedural guidance only — do not APPLY before source
readiness):

- `forseti-product-lead` skill (`.agents/skills/`, per
  `.agents/workflow-overlay/skill-adoption.md`) — for the channel-goal
  framing, which is a product decision (buyer, job, positioning) prepared for
  owner sign-off. If the skill is not resolver-available in the receiving
  session, proceed under `.agents/workflow-overlay/product-proof.md` alone and
  name the gap; do not hand-reconstruct the skill.

`SOURCE-LOAD` (the task sources):

- **Controlling for admissible inputs:**
  `docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md` — the
  19-row candidate table (paraphrases tied to packet line numbers), evidence
  boundary, and residuals.
- `docs/workflows/quora_b2b_answer_strategy_pilot_handoff_v0.md` — the Goal
  Handoff, Drift Guard, and the Disposition section (2026-07-10) this
  commission re-enters from.
- `docs/review-outputs/adversarial-artifact-reviews/quora_b2b_postmerge_capture_calibration_delegated_adversarial_review_patch_v0.md`
  — corrected evidence interpretation (esp. rows 210/215 and the
  bot-detection-pressure footnote).
- `.agents/workflow-overlay/product-proof.md` — buyer-proof semantics and
  non-claims; the methodology's claim rules must not redefine trust-objection
  or buyer-proof vocabulary locally.
- `forseti/product/spines/scanning/README.md` and
  `forseti/product/spines/scanning/source_families/answer_engine/` (existing
  family spec) — placement home and any existing answer-engine method
  constraints the meta must not contradict.
- Targeted excerpt only:
  `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  route-maturity note — the bounded-evidence framing for Quora capture
  reliability the methodology must carry, not re-litigate.

Then declare **`SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` with
missing/gap/conflict). Do **not** produce channel-goal options, archetype
clusters, or methodology sections before that declaration.

## The Work

**STEP 1 — Channel-goal options (owner decision input; APPLY
`forseti-product-lead` framing here).** Propose 2–4 options for what Quora B2B
answer content is *for*, each with: the buyer/reader it serves, the job the
content does (e.g. answer-engine/search visibility, credibility/authority,
lead generation), what observable signal would say it is working, what would
kill it, and tradeoffs. Recommend one default and say why. Do not decide —
prepare for owner sign-off.

**STEP 2 — Question-archetype clustering.** Cluster the calibration record's
19 candidate rows into a small set of question archetypes (e.g. discovery
practice, hiring, pricing, validation, marketing craft — derive from the
actual rows, do not force this example set). Name which archetypes serve the
recommended channel goal and which do not.

**STEP 3 — The answering meta itself.** For the recommended default (with
sensitivity labels where another channel-goal option would change the rule),
define:

- **Context requirements per answer** — what must be established before
  drafting (searcher intent read, what the asker already tried, what a
  generic answer would say, what we know that it would not).
- **Non-generic depth-of-value bar** — a checkable test a draft must pass
  (e.g. "contains at least one thing a generic LLM answer would not:
  a named tradeoff, a concrete number range with provenance, a
  counter-intuitive stop rule"). Make the bar falsifiable, not vibes.
- **Per-archetype approach/structure** — how an answer for each archetype
  opens, what it must cover, how it closes; when to include an Orca pointer
  and when not.
- **Tone contract** — voice, person, hedging policy, jargon policy, length
  envelope.
- **Claim boundaries** — carried from the grounding records: candidate rows
  are demand signal, not buyer proof; no invented exact Quora wording
  (paraphrase table is not quotation; exact wording requires the local packet
  named by the calibration record); no Quora-reliability or session-durability
  claims; no Orca-internal disclosures (e.g. pricing) without owner say-so.

**STEP 4 — Optional worked exemplars (bounded).** At most 1–2 worked
calibration exemplars applying the meta to an admissible candidate row, each
clearly labeled **NON-PUBLISHABLE — calibration only**. Skip if they would
front-run the owner's channel-goal decision.

**STEP 5 — Open decisions and stop.** End the artifact with the owner
decision list (channel goal, meta adoption, whether/when drafting resumes,
placement confirmation) and stop. No publishable answers, no posting plan,
no capture, no code.

## Hard Boundaries (drift guard)

- No live Quora capture, scrape, probe, or session use — this is a docs lane.
- No publishable answer content; exemplars only as bounded in STEP 4.
- No buyer-proof, market-proof, source-quality-proof, or Quora-policy claims.
- No invented exact Quora wording anywhere in the artifact.
- No code edits, no overlay edits, no skill edits, no capture-playbook edits.
- No runtime model recommendation, ranking, or routing for any future lane.
- The deliverable is proposal-status decision input; adoption is owner-owned.
- Do not widen into a general multi-channel content strategy; Quora B2B only,
  swap-ready for other surfaces later only if the owner asks.

## Output Contract And Validation

- **Input prompt source (run-authoritative for the receiver):** this canonical
  prompt artifact at
  `docs/prompts/handoffs/quora_b2b_answering_meta_design_commission_prompt_v0.md`
  on origin/main after its lane PR merges.
- **Output artifact (exact path, file-write):**
  `forseti/product/spines/scanning/source_families/answer_engine/quora_b2b_answering_meta_v0.md`
  with a retrieval header per `.agents/workflow-overlay/retrieval-metadata.md`
  and proposal/decision-input status stated in the body. If reading the
  scanning front door shows this home is wrong (e.g. the owner's channel-goal
  choice reframes ownership), surface the placement question in chat instead
  of silently relocating.
- **Validation before completion claims:** `git diff --check`;
  `python .agents/hooks/check_retrieval_header.py --strict <artifact>`;
  `python .agents/hooks/check_placement.py --check`; fresh read of the
  written artifact. Report observed results only; a green check is shape, not
  validation of the methodology's quality.
- **Lane flow:** worktree/branch off `origin/main`, commit, push, PR per
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`; landing
  to main stays human-gated.
- **Chat closeout:** headed human summary first (recommendation, why it
  matters, material boundaries, owner decision list), then the artifact
  receipt (path, hash, validation results).

## Assumptions, Unknowns, Blocked Conditions

- Assumption (labeled): the owner still wants the Quora content leg pursued at
  methodology depth; if the owner has since dropped the channel, this
  commission is stale (see `stale_if`).
- Unknown: the channel goal — deliberately open; STEP 1 exists to make it
  decidable, not to decide it.
- Unknown: whether `forseti-product-lead` resolves in the receiving session;
  fallback bound in Required Reads.
- Blocked if: controlling sources unreachable on origin/main
  (`blocked_if_missing` above); or the receiver finds the calibration record
  superseded (then stop and surface, per `stale_if`).

## Non-Claims

- Not capture authorization, not implementation authorization, not validation,
  not readiness, not buyer proof, not Quora reliability proof, not adopted
  method doctrine, not a posting/publication decision.
