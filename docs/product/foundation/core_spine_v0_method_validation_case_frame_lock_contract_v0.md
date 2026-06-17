# Foundation Layer v0 Method Validation Case-Frame Lock Contract

- Status: FRAME_LOCK_CONTRACT_READY
- Artifact type: Product-method validation lock contract
- Scope: Safe pre-validation case detail for the five locked method-validation cases
- Date context: 2026-05-21, Asia/Singapore
- Source basis: current owner instruction, `docs/product/core_spine_v0_method_validation_case_locks_v0.md`, `docs/product/core_spine_v0_method_validation_rubric_v0.md`, `docs/product/core_spine_v0_first_proof_run_packet_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- Evidence replay authorized by this artifact: no
- Source maps, source systems, data spine, automation, dashboards, scoring engines, and generated artifacts authorized: no

## 1. Decision

The next compounding move is case-frame locking, not case-study drafting and
not evidence replay.

Case-frame locks should add enough detail to make later validation disciplined,
but not enough narrative detail to bias the at-cutoff replay.

## 2. Current Compounding Frontier

The current compounding frontier is cutoff and decision-frame discipline
because the value proposition cannot become more proven until each locked case
has a fair at-cutoff decision question, source boundary, second-order evidence
boundary, and post-window exclusion rule.

Without that layer, a future validation run can accidentally become hindsight
case writing.

## 3. Safe Detail Before Validation

Safe pre-validation detail includes:

- decision question;
- decision owner or context;
- cutoff date or cutoff window;
- fair-cutoff rationale;
- why the later outcome was not obvious at cutoff;
- allowed action verbs;
- first-order source-family boundary;
- second-order source-family boundary;
- post-window exclusion rule;
- expected outcome-comparison window;
- reliable-bet or costly-behavior standard for the case;
- positive-action or reverse-case role;
- upgrade, downgrade, reframe, blocked, useful, wrong, early, late,
  overconfident, and underconfident semantics.

This detail improves validation quality because it controls timing, source
use, and action-ceiling interpretation before evidence is interpreted.

## 4. Dangerous Detail Before Validation

Avoid pre-validation detail that would turn the lock into a case study:

- rich narrative arcs;
- post-window outcome explanations;
- likely Orca recommendation;
- detailed source lists that privilege one answer;
- causal claims about what really happened;
- moralized framing such as "obviously bad move" or "obviously right move";
- marketing lessons;
- buyer-value claims;
- feature implications;
- implementation implications.

Those details should wait until after the replay. Before the replay, they risk
turning method validation into hindsight laundering.

## 5. Three-Layer Artifact Sequence

Use this sequence:

1. Case identity lock: already recorded in
   `docs/product/core_spine_v0_method_validation_case_locks_v0.md`.
2. Case-frame locks: next artifact. It should lock cutoff, decision frame,
   source-family boundaries, exclusion rules, and result semantics for all five
   cases.
3. Case studies: only after replay. Case-study prose may become internal
   learning or marketing material only after pre-cutoff discipline protects the
   method result.

## 6. What Not To Do Yet

Do not:

- run evidence replay;
- collect full source pools;
- browse broadly for persuasive case narratives;
- write marketing case studies;
- create a source map, data spine, dashboard, scoring system, scraper, API, or
  automation;
- plan features or implementation;
- claim that any case will pass, fail, upgrade, downgrade, or validate Orca.

## 7. Replacement Rule

If case-frame locking shows that one of the five locked cases is blocked, the
replacement must preserve the blocked case's validation role.

Examples:

- a blocked reverse case should be replaced by another reverse case;
- a blocked positive-action case should be replaced by another positive-action
  case;
- a blocked SH-01-like narrative case should be replaced by another
  competitor narrative pressure case.

Do not replace a hard case with an easy case merely to complete the set.

## 8. Current Verdict

Current verdict: `READY_FOR_CASE_FRAME_LOCK_PROMPT`.

The next authorized artifact is a prompt for producing
`docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`. That
future artifact may lock cutoff and source-family boundaries, but it must not
perform evidence replay.
