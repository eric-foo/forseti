# Engagement Resonance Enforcement Goal Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff / enforcement planning note
scope: >
  Durable MGT/SCI lens, per-checker goal frames, and cold-lane handoff for the
  first six code-enforcement candidates around public engagement as qualitative
  resonance weight.
use_when:
  - Continuing the engagement-resonance enforcement work one checker at a time.
  - Deciding which deterministic checks should remove repetitive burden from LLM agents.
  - Preventing code enforcement from becoming resonance scoring, proof, runtime infrastructure, or broad doctrine redesign.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/artifact-folders.md
  - orca/product/shared/engagement_registry/engagement_logic_registry_v0.md
  - .agents/hooks/check_commission_signal_board_output.py
  - .agents/hooks/check_csb_scanning_artifact.py
```

## Executive Frame

This artifact frames six enforcement candidates for the engagement-resonance
doctrine. The priority is not "most important doctrine." The priority is
"which deterministic checks remove the most repetitive, error-prone burden from
LLM agents without pretending to make qualitative Judgment calls."

The core enforcement boundary:

- Code may enforce artifact shape, required fields, vocabulary sync, stale
  phrase bans, receipt hygiene, and forbidden overclaim language.
- Code must not decide final resonance weight, demand, credibility,
  independence, buyer proof, Commit/Scale support, Action Ceiling, or proof.
- Passing a checker is not validation, readiness, proof, or acceptance.

## Program Goal Frame

Goal establishing:

- Long-term goal: Make Orca's public-engagement handling reliable enough that
  future agents preserve resonance evidence and avoid proof/scoring drift
  without needing repeated manual policing.
- Anchor goal: Build the first six deterministic enforcement surfaces one by
  one, starting with the highest LLM-burden reducers.
- Success signal:
  - Core success:
    - Owner-observable: Each completed unit removes one class of repetitive LLM
      review burden and has a local checker/selftest or explicit not-yet-built
      reason.
    - Output fit: Future agents can run or rely on a narrow check instead of
      rereading broad doctrine to catch the same mechanical mistake.
    - Boundary: A checker passing does not count as proof, resonance judgment,
      buyer proof, validation, readiness, or acceptance.
    - Drift cue: The work starts creating scoring engines, schema/runtime
      infrastructure, broad CI gates, or new doctrine instead of small
      deterministic checks.
  - Secondary success signals:
    - Checkers cite their owning doctrine rather than restating it.
    - False positives stay bounded to mechanical, source-visible failures.
    - Existing advisory/strict hook patterns are reused where possible.

```yaml
goal_handoff:
  long_term_goal: "Make Orca's public-engagement handling reliable enough that future agents preserve resonance evidence and avoid proof/scoring drift without repeated manual policing."
  anchor_goal: "Build the first six deterministic enforcement surfaces one by one, starting with the highest LLM-burden reducers."
  success_signal:
    core_success:
      owner_observable: "Each completed unit removes one class of repetitive LLM review burden and has a local checker/selftest or explicit not-yet-built reason."
      output_fit: "Future agents can run or rely on a narrow check instead of rereading broad doctrine to catch the same mechanical mistake."
      boundary: "A checker passing does not count as proof, resonance judgment, buyer proof, validation, readiness, or acceptance."
      drift_cue: "The work starts creating scoring engines, schema/runtime infrastructure, broad CI gates, or new doctrine instead of small deterministic checks."
    secondary_success_signals:
      - "Checkers cite their owning doctrine rather than restating it."
      - "False positives stay bounded to mechanical, source-visible failures."
      - "Existing advisory/strict hook patterns are reused where possible."
  status: user_stated
```

## Priority 1 - DCP Receipt Hygiene Checker

Why this is high value:

- LLMs repeatedly maintain `direction_change_propagation` receipts by hand.
- The rule is structural: max two inline receipts, required archive pointer,
  and no unauthorized standalone receipt files.
- It directly caught AR-02 in the engagement registry and is cheap to verify.

MGT lens:

- Target: catch nearly all receipt-shape failures at a fraction of a manual
  review pass.
- Accepted residuals:
  - It will not decide whether a DCP receipt is semantically honest.
  - It will not verify every downstream surface was truly checked.
  - It will not judge whether a doctrine change needed a receipt.
- Upgrade trigger: If agents keep passing structurally valid but dishonest
  receipts, add a separate receipt-honesty review checklist, not a fake
  semantic validator.

SCI lens:

- Smallest complete intervention: add one checker for changed durable docs that
  mechanically inspects DCP block count, archive pointer presence, and
  unauthorized standalone receipt files.
- Avoid: broad whole-repo blocking by default, receipt semantic scoring, or
  rewriting historical receipts.

Goal frame:

```yaml
goal_handoff:
  long_term_goal: "Reduce recurring LLM burden around doctrine-change receipt maintenance."
  anchor_goal: "Add a deterministic DCP receipt hygiene check for changed durable docs."
  success_signal:
    core_success:
      owner_observable: "A changed doc with malformed DCP receipt storage is reported by a checker instead of discovered in review."
      output_fit: "The checker names the exact structural defect and owning source-of-truth rule."
      boundary: "The checker does not validate receipt truth, readiness, acceptance, or doctrine correctness."
      drift_cue: "The implementation tries to judge whether downstream surfaces were actually checked."
  status: user_stated
```

## Priority 2 - Registry/List Sync Checker

Why this is high value:

- LLMs are weak at keeping duplicated vocabulary lists synchronized across
  several docs.
- The recent review found `resonance-direction evidence` in Foundation before
  it existed in the registry.
- This class is deterministic and generalizes beyond engagement.

MGT lens:

- Target: make canonical vocabulary drift obvious without forcing a large
  ontology system.
- Accepted residuals:
  - It only covers explicitly registered canonical/list pairs.
  - It does not decide whether a new vocabulary item is product-correct.
  - It does not auto-edit downstream docs.
- Upgrade trigger: If many vocab pairs emerge, move from hardcoded pairs to a
  small registry of list-sync bindings.

SCI lens:

- Smallest complete intervention: start with one binding: engagement registry
  Signal Use Classification list must contain any Signal Use category added to
  Information Production Foundation.
- Avoid: full ontology, YAML schema migration, or broad product-vocabulary
  normalization.

Goal frame:

```yaml
goal_handoff:
  long_term_goal: "Prevent LLM-authored doctrine surfaces from silently forking canonical vocabularies."
  anchor_goal: "Add the first narrow registry/list sync check for engagement Signal Use categories."
  success_signal:
    core_success:
      owner_observable: "A new Signal Use category in Foundation fails or reports if absent from the engagement registry."
      output_fit: "The next agent can fix vocabulary drift from a specific checker message instead of manually comparing lists."
      boundary: "The checker does not decide whether the category should exist."
      drift_cue: "The work becomes a full ontology rewrite or starts auto-promoting categories."
  status: user_stated
```

## Priority 3 - Stale Doctrine Phrase Sweep

Why this is high value:

- LLMs miss old phrasing in large doctrine surfaces.
- The stale sweep already helped verify the engagement-resonance patch.
- The target is language leakage, not correctness of the whole doctrine.

MGT lens:

- Target: catch most stale mental-model leaks with a small curated phrase set.
- Accepted residuals:
  - It will miss novel stale phrasing.
  - It may need allowlists for historical prompts, review outputs, and receipt
    query self-references.
  - It does not prove doctrine is coherent.
- Upgrade trigger: If stale leakage keeps appearing under new wording, add
  pattern families or per-lane phrase packs.

SCI lens:

- Smallest complete intervention: create or extend a report/strict-capable
  checker over live doctrine paths only, excluding historical prompts/reviews
  unless explicitly asked.
- Avoid: broad grep noise that trains agents to ignore findings.

Goal frame:

```yaml
goal_handoff:
  long_term_goal: "Keep superseded engagement doctrine from reappearing in live product surfaces."
  anchor_goal: "Add a targeted stale-phrase sweep for engagement/resonance doctrine drift."
  success_signal:
    core_success:
      owner_observable: "Old attention-only, score-boost, and engagement-proof phrases are surfaced mechanically when they re-enter live doctrine."
      output_fit: "The checker separates live doctrine findings from historical/self-reference noise."
      boundary: "The sweep is leakage detection, not validation or proof of current doctrine."
      drift_cue: "The phrase list becomes broad, noisy, or blocks historical records by default."
  status: user_stated
```

## Priority 4 - CSB Output Checker Extension

Why this is high value:

- Commission Signal Board rows are LLM-authored handoff objects that downstream
  lanes consume.
- Existing checker already validates row shape and graph/recency mechanics.
- Engagement/resonance overclaims in CSB can poison later capture, scanning, or
  judgment work.

MGT lens:

- Target: block the dangerous, mechanical CSB overclaims without judging the
  signal itself.
- Accepted residuals:
  - It will not decide whether a row is actually good evidence.
  - It will not require every engagement qualifier in every row.
  - It will not parse arbitrary prose perfectly.
- Upgrade trigger: If board artifacts adopt structured engagement columns,
  validate those fields directly.

SCI lens:

- Smallest complete intervention: extend
  `.agents/hooks/check_commission_signal_board_output.py` with forbidden
  engagement/resonance-as-proof patterns and selftests.
- Avoid: new CSB schema columns unless a later owner decision authorizes them.

Goal frame:

```yaml
goal_handoff:
  long_term_goal: "Protect downstream lanes from CSB rows that upgrade engagement into proof or decision authority."
  anchor_goal: "Extend the CSB checker to catch engagement/resonance overclaim language."
  success_signal:
    core_success:
      owner_observable: "A CSB output that treats engagement as proof, graph weight, Commit/Scale support, credibility, Action Ceiling, or final resonance weight is flagged."
      output_fit: "The checker preserves existing CSB row validation while adding only the new overclaim class."
      boundary: "The checker does not judge evidence quality or demand."
      drift_cue: "The implementation adds new required board columns or turns CSB into Judgment."
  status: user_stated
```

## Priority 5 - Scanning Artifact Checker Extension

Why this is high value:

- Scanning artifacts are LLM-authored and can easily turn routing context into
  proof language.
- Existing checker already has a recency-as-proof forbidden-pattern substrate.
- Engagement/resonance needs the same guard at the scanning boundary.

MGT lens:

- Target: catch the highest-risk scanning overclaim with a small extension to
  an existing checker.
- Accepted residuals:
  - It will not decide which venue deserves priority.
  - It will not prove a scan found enough evidence.
  - It will not force all engagement qualifier fields unless artifacts become
    structured enough to support that.
- Upgrade trigger: If scanning outputs standardize engagement observation
  records, require qualifier fields when engagement metrics are present.

SCI lens:

- Smallest complete intervention: add engagement/resonance-as-proof forbidden
  text patterns and selftests to `.agents/hooks/check_csb_scanning_artifact.py`.
- Avoid: new scan schema, capture-route binding, or scoring/ranking logic.

Goal frame:

```yaml
goal_handoff:
  long_term_goal: "Keep Scanning from converting public engagement into proof while preserving it as routing context."
  anchor_goal: "Extend the scanning artifact checker to catch engagement/resonance-as-proof and final-weight language."
  success_signal:
    core_success:
      owner_observable: "A scan artifact that treats engagement/resonance as proof, gate clearance, route binding, or final resonance weight is flagged."
      output_fit: "The checker gives a narrow finding without requiring a broad scan redesign."
      boundary: "The checker does not judge venue priority, candidate quality, or Capture route choice."
      drift_cue: "The implementation starts binding Capture routes or requiring a new scan schema."
  status: user_stated
```

## Priority 6 - Review Output Provenance Checker

Why this is high value:

- Review outputs are often LLM-authored closeout records, and provenance fields
  are easy to omit.
- Missing `reviewed_by`, `authored_by`, or review-use boundaries weakens later
  adjudication and de-correlation claims.
- This is lower than product-path checks because it protects process memory, not
  the demand-signal handoff itself.

MGT lens:

- Target: make review-output provenance omissions mechanically visible without
  deciding review quality.
- Accepted residuals:
  - It will not verify the reviewer identity beyond recorded text.
  - It will not decide whether de-correlation was truly satisfied unless a
    separate provenance-bound field exists.
  - It will not grade findings.
- Upgrade trigger: If provenance becomes machine-produced, bind stronger
  receipt-field provenance checks.

SCI lens:

- Smallest complete intervention: add a checker for new/materially changed
  `docs/review-outputs/**` markdown files requiring retrieval header,
  `reviewed_by`, `authored_by`, and review-use boundary / non-approval wording.
- Avoid: review scoring, model ranking, or formal PASS/readiness language.

Goal frame:

```yaml
goal_handoff:
  long_term_goal: "Make review records easier for future agents to adjudicate without trusting vague provenance."
  anchor_goal: "Add a narrow review-output provenance shape checker."
  success_signal:
    core_success:
      owner_observable: "A new review output missing provenance or review-use boundary fields is flagged."
      output_fit: "Future adjudication can see who reviewed, who authored, and what the review does not claim."
      boundary: "The checker does not validate review quality, de-correlation truth, approval, or readiness."
      drift_cue: "The implementation starts ranking models or treating provenance text as self-certifying proof."
  status: user_stated
```

## Recommended One-By-One Order

1. DCP receipt hygiene checker.
2. Registry/list sync checker.
3. Stale doctrine phrase sweep.
4. CSB output checker extension.
5. Scanning artifact checker extension.
6. Review output provenance checker.

Why this order:

- Items 1-3 remove the most repeated cross-document LLM burden immediately.
- Items 4-5 enforce at artifact-production boundaries where bad handoffs enter
  downstream work.
- Item 6 improves adjudication memory, but it is less directly in the product
  signal path.

## Handoff

### Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-26
- created_by_lane: Codex, branch `codex/search-surface-mgt-p0-captures-ws`
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\search-surface-mgt-p0-captures`
- handoff_path: `docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md`
- expected_branch: `codex/search-surface-mgt-p0-captures-ws`
- expected_head_before_handoff_file: `6d749e9f61b4b81164ef0a432ed7cf86d20993d4`
- expected_dirty_state_after_handoff_file:
  - `?? docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md`
  - `?? docs/prompts/hygiene-queue/` (pre-existing, unrelated; do not stage unless explicitly routed)
- load_rule: confirm-don't-trust; re-read the named sources before strict or
  actionable claims.

### Active Objective

Implement the six engagement-resonance enforcement candidates one at a time,
starting with Priority 1 unless the owner redirects. The next implementation
unit should produce a narrow checker or an explicit not-yet-buildable blocker;
it must not implement all six at once.

### Open Decision / Fork

- decision: Which enforcement unit to implement first.
- options:
  - Start with Priority 1, DCP receipt hygiene checker.
  - Override order if the owner wants a product-path checker first.
- already constrained:
  - Work 1-6 one by one.
  - Do not build scoring, schema/runtime infrastructure, crawlers, dashboards,
    or broad validation systems.
- recommendation: Start with Priority 1. It is deterministic, high leverage,
  and directly removes recurring hand-maintained DCP burden.

### Drift Guard

- Do not convert qualitative engagement resonance into a numeric score or code
  judgment.
- Do not turn checker passing into validation, readiness, proof, buyer proof, or
  acceptance.
- Do not widen the first implementation into all six checks at once.
- Do not add new runtime/schema infrastructure without a separate explicit
  implementation authorization.

### Exact Next Authorized Action

1. Implement Priority 1 only: DCP receipt hygiene checker.
2. Use existing `.agents/hooks/` checker patterns with report/advisory and
   strict modes where appropriate.
3. Add selftests and run the narrow validation set before committing.
4. After Priority 1 lands, return to this artifact to choose Priority 2.

### Source Ledger

- `AGENTS.md`
  - Role: project instruction kernel, MGT/SCI trigger source
  - Load-bearing: yes
  - Compare target: reread-required
  - Reuse rule: verify before implementation
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`
  - Role: MGT doctrine
  - Load-bearing: yes
  - Compare target: reread-required
  - Reuse rule: verify accepted residuals before claiming MGT fit
- `.agents/workflow-overlay/validation-gates.md`
  - Role: enforcement placement and checker boundary authority
  - Load-bearing: yes
  - Compare target: reread-required
  - Reuse rule: verify before adding or promoting any checker
- `.agents/workflow-overlay/source-of-truth.md`
  - Role: DCP receipt mechanics and archive rule
  - Load-bearing: yes
  - Compare target: reread-required
  - Reuse rule: verify before Priority 1
- `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`
  - Role: canonical engagement/resonance doctrine and Signal Use vocabulary
  - Load-bearing: yes
  - Compare target: reread-required
  - Reuse rule: verify before Priorities 2-5
- `.agents/hooks/check_commission_signal_board_output.py`
  - Role: existing CSB checker substrate
  - Load-bearing: yes for Priority 4
  - Compare target: reread-required
  - Reuse rule: inspect current parser and selftest shape before editing
- `.agents/hooks/check_csb_scanning_artifact.py`
  - Role: existing scanning checker substrate
  - Load-bearing: yes for Priority 5
  - Compare target: reread-required
  - Reuse rule: inspect current forbidden-pattern and selftest shape before editing

### Not-Proven Boundaries

- This artifact does not validate any checker.
- This artifact does not authorize implementation beyond the next one-by-one
  checker work the owner selects.
- This artifact does not claim code can judge resonance quality.
- This artifact does not change doctrine; it plans enforcement candidates.

## Courier Block

```text
Get back context from:
docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md

Follow the packet's confirm-don't-trust load contract. If you have repo/filesystem access, open the packet and re-read its named load-bearing sources before making strict or actionable claims. If you do not have repo/filesystem access, stop and request a pasted source capsule or no-repo handoff.

Continue only the lane named in the packet's Goal Handoff / Active Objective. Do not perform work excluded by the packet's Drift Guard unless explicitly redirected by the current user.
```
