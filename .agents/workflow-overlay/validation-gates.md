# Validation Gates

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Validation gates required before Orca completion claims.
use_when:
  - Checking whether an Orca completion, prompt, or artifact claim has required evidence.
  - Defining validation expectations for docs/decision work, explicitly authorized implementation work, prompts, and artifacts.
authority_boundary: retrieval_only
```

**Routine read shape** (owned by `.agents/workflow-overlay/source-loading.md`,
Targeted Read Protocol): closeout checks read "Current Gates"; prompt
authoring reads "Prompt Orchestration Gates"; product-proof work reads
"Product Proof Gates"; enforcement-placement decisions read "Enforcement
Placement"; a full-file read is for editing validation doctrine.

Validation must be able to fail. Missing evidence is not a pass.

Validation reports must preserve failure visibility by bucket:

- `GATE PASS` / `GATE FAIL` are exit-code-bearing checks required for the claim.
- `INFO` / `DEBT` is explicit allowlisted non-gating output; it never changes the gate exit code.
- `OUT OF SCOPE` must name the owning lane or source surface; it cannot mean inconvenient or ignored.
- Unknown nonzero exits, unknown findings, and wrapper-internal errors default to `GATE FAIL`, never
  `INFO`. A future wrapper may encode this policy, but bucket membership is owned here; any wrapper
  script that encodes it must exit nonzero iff any `GATE FAIL` exists.

## Current Gates

- Required Orca files exist before claiming bootstrap completion.
- No software implementation directories are present unless explicitly authorized.
- `AGENTS.md` and overlay files do not encode `jb` project-specific authority as Orca rules.
- Repo-aware prompt use, review setup, handoff creation, docs-write or overlay
  maintenance, source-changing work, and completion claims include or report
  the `orca_start_preflight` receipt from
  `.agents/workflow-overlay/source-loading.md`. Missing preflight evidence is a
  blocker for the claim or handoff, not proof that the artifact body is false
  and not authority for broad cleanup.
- Doctrine-changing source work must include an inline
  `direction_change_propagation` receipt or explicit
  `direction_change_propagation_blocker` under
  `.agents/workflow-overlay/source-of-truth.md` before claiming completion.
  Missing propagation evidence blocks strict completion, readiness, validation,
  `PASS`, `ADEQUATE_NOW`, acceptance, or alignment-complete claims; it does not
  authorize a broad template sweep, automation, new skill, registry, or
  standalone receipt file.
- Review-routing disposition gate: a change that touches code roots
  (`orca-harness/`, `.agents/hooks/`) must carry its review disposition in the
  same change — either a review artifact added under `docs/prompts/reviews/`
  or `docs/review-outputs/`, or a shape-valid `review_routing_status:` line in
  one of the change's commit messages:
  `review_routing_status: routed <existing docs/prompts/reviews/... or docs/review-outputs/... path>`,
  `review_routing_status: blocked -- <reason>`, or
  `review_routing_status: not_needed -- <reason>`.
  A carried recommended or required adversarial review may close only as
  `routed` or `blocked`, never `not_needed` (the fused/review contracts own
  that vocabulary; this gate does not weaken it). The disposition is routing
  shape only: it is not review quality, review truth, severity authority,
  validation, or readiness, and the gate never decides whether review SHOULD
  have been recommended — that stays resident scoping judgment. Enforced
  diff-scoped and forward-only by `.agents/hooks/check_review_routing.py`
  (local `--commit-msg` advisory; CI `--strict`).
- Handoff-pointer resolution gate: a changed durable `.md` file must not
  reference a handoff-packet path (`docs/workflows/*handoff*.md`,
  `docs/prompts/handoffs/*.md`) that does not resolve in the same tree,
  unless the pointer line carries an explicit resolution pin (the word
  `branch`, `PR #<n>`, or an `origin/<ref>` token — a fetch handle for a cold
  reader) or an exemption marker (`does not exist yet`, `created on first`,
  `not retrieval-indexed`, `nonresolving:`, or superseded/removed/deleted
  wording for retired packets). Practical consequence: a handoff packet
  merges no later than the first main-bound artifact that points at it (the
  same PR is fine), or the pointer pins the authoring branch explicitly — a
  cold receiving lane resolves required reads from `origin/main`, not from
  unmerged authoring branches. The gate is pointer shape only: it never
  proves a packet's content is current, that a pinned branch still exists, or
  that the cited packet was the right source — that stays resident judgment.
  Couriers that never land in the repo (chat bodies, PR comments, ignored
  `docs/_inbox/` scratch) are outside its reach and stay governed by
  `.agents/workflow-overlay/prompt-orchestration.md`. Enforced diff-scoped
  and forward-only by `.agents/hooks/check_handoff_pointers.py` (CI
  `--strict`; whole-corpus backlog via `--audit`, never gated).
- Receipt-field provenance gate (non-self-certification): a gate, predicate,
  acceptance check, or completion claim must not clear on a self-asserted field
  value. A field clears only when it is owner-produced and provenance-bound or
  independently verifiable — computed, re-derivable, audited, or produced by an
  authorized process. A value a by-hand, unauthorized, dry-runner,
  local-fixture, manually normalized, or operator-authored record could simply
  assert is not self-certifying and does not clear, even when it reads `proven`,
  `pass_valid`, `valid`, or `complete`. Where no owner-produced or verifiable
  field exists yet, the check is `indeterminate_until_authored` (blocked, not
  passed); do not clear on a paraphrase and do not invent the field. Corollaries:
  (a) fix the whole class of such checks in one pass, not one instance; (b)
  verify a cited source actually defines the field before binding a check to it;
  (c) single-source any value otherwise enumerated in multiple places (enumerate
  once; reference it). This gate is a check, not validation or readiness
  evidence; its presence does not prove any artifact passes it. Lifecycle:
  Orca-local adoption of general authoring/review discipline, not Orca-owned
  doctrine; it is a candidate for future skill-source adoption and becomes
  stale here if an equivalent accepted skill-source rule is adopted.
- New or materially touched durable human-authored workflow artifacts follow
  `.agents/workflow-overlay/retrieval-metadata.md` or are clearly outside that
  contract.
- Report-only retrievability checks may use
  `docs/workflows/artifact_retrievability_guide.md` for artifact body-opening
  shape, stale/recheck clarity, repo-map/index treatment, and hygiene anti-rot.
  Findings are routing or hygiene defects only; they do not prove validation
  failure, validation success, approval, readiness, lifecycle completion,
  implementation authorization, or edit permission.
- Source hashes for migration-governance inputs are recorded in `docs/workflows/orca_bootstrap_record.md`.
- Resolver-visible skill-name snapshots are recorded before any skill adoption or promotion work.
- Git status is reported when this workspace is a Git repo.

## Prompt Orchestration Gates

- Overlay authority gate: `AGENTS.md` and `.agents/workflow-overlay/README.md`
  must be read before prompt-orchestration work, and repo-aware prompts must
  carry the start-preflight fields owned by
  `.agents/workflow-overlay/source-loading.md`.
- Artifact role gate: every prompt role must be bound in `.agents/workflow-overlay/artifact-roles.md` or another accepted Orca overlay file.
- Source-resolution gate: external workflow sources do not provide Orca authority; installed skills are deployment copies; `jb` project policy must not be imported.
- Worktree preflight gate: repository-aware prompts must state workspace, revision or hash when needed, dirty-state allowance, target scope, and edit permission.
- Control-plane source-state gate: repository-aware prompts, prompt-policy
  patches, workflow patches, and CA handoffs must classify controlling Orca
  sources as clean, modified, untracked, stale, or not checked when those
  sources affect strict claims. Modified or untracked controlling sources may
  support advisory work, but strict `PASS`, `ADEQUATE_NOW`, readiness,
  acceptance, source-of-truth, validation, or proof claims remain blocked unless
  owner acceptance or controlling authority is explicit.
- Output-mode gate: prompts must name exactly one output mode from `.agents/workflow-overlay/prompt-orchestration.md`.
- Chat-output topology gate: prompt-policy patches, workflow patches, and
  reusable prompt templates touching chat output shape must check for
  contradictions between the general human-summary / agent-detail /
  optional courier-state rule in
  `.agents/workflow-overlay/communication-style.md` and output-mode exceptions
  in `.agents/workflow-overlay/prompt-orchestration.md`.
  This is a collision gate, not a required-key checklist: decision-bearing chat
  should start with human-readable prose; agent detail should stay separate;
  courier state should stay compact and last when used; YAML should not be
  defaulted unless the user asks, an output mode requires it, an explicit
  output contract needs machine-shaped fields, or lane switching / handoff
  routing would materially benefit from compact courier YAML;
  `review-report` YAML-only chat remains tied to successful durable report
  writes; `file-write` receipts remain valid only when the durable artifact
  carries the human value and no material decision must be understood from chat;
  `paste-ready-chat` must be classified
  before template propagation; task-native structured outputs such as evidence
  tables must not be naively rewritten into verbose closeouts; already-correct
  active `review-report` prompts and stale one-offs must not be broad-synced;
  and extra courier keys or ritual non-claim fields must not be added merely to
  satisfy process metrics.
- Review-report topology gate: prompts and prompt-policy patches touching
  `review-report` must check that the saved-report exception is adjacent to the
  owning output-mode rule; the durable report remains the review artifact; chat
  YAML remains courier output; YAML-only chat is valid only after successful
  report write, explicit chat-only selection, or pre-write blockage; failed
  durable writes use `status: failed`, `recommendation: blocked`,
  `review_location: chat_only_current_thread`, and no `report_path`; the failed
  path is named in human-readable routing detail; no extra YAML keys are added
  for process metrics; retrieval metadata stays retrieval-only; active
  templates/prompts are patched or stale one-offs are queued for hygiene; and
  no validation, approval, readiness, resolver, lifecycle, install, deploy,
  merge-safety, or product-readiness claim is introduced.
- Review-doctrine gate: review prompts, review templates, review-output
  closeouts, and CA-facing review handoffs must keep review output
  findings-first by default; require adversarial artifact review prompts to
  invoke `workflow-adversarial-artifact-review` after source readiness or block
  strict claims as advisory-only; bind any formal verdict, severity contract,
  blocked/ready status, validation claim, readiness claim, mandatory
  remediation, patch queue, or executor-ready handoff; include
  `minimum_closure_condition` and `next_authorized_action` for actionable
  findings; define closure conditions as required end states rather than
  implementation instructions; label optional hardening as optional and
  non-required; exclude `patch_queue_entry` unless the lane is patch-queue
  review or patch/integration execution; preserve the Chief Architect
  consumption order from `.agents/workflow-overlay/communication-style.md`; and
  avoid creating a synthesis lane. Missing or contradictory doctrine binding
  blocks strict `PASS`, readiness, acceptance, validation, or
  alignment-complete claims.
- Thread operating target continuity gate: when a generated workflow prompt,
  wrapper, rerun, review prompt, patch prompt, or handoff continues the same
  workstream or claims to optimize for the same anchor goal, a visible active
  `thread_operating_target` must be carried forward verbatim near the top of
  the prompt with the continuity disclosure from
  `.agents/workflow-overlay/prompt-orchestration.md`, or the omission must be
  explained. Omission without explanation is a prompt-quality defect. The
  target is thread-local orientation only, not source authority, validation
  evidence, readiness, approval, lifecycle completion, workflow sequencing
  authority, durable memory, or edit permission.
- Source-heavy economy gate: prompts that require public web/source research,
  several external page opens, source ledgers, post-window comparisons, or
  several large artifact reads must define a source-loading unit and require the
  unit artifact to be written and hashed before the next unit starts.
- Source-capsule budget gate: source capsules must stay within the budgets in
  `.agents/workflow-overlay/source-loading.md`. If the budget is exceeded, the
  prompt must narrow the question, split the source-loading unit, or move to a
  new-thread handoff instead of compressing broader history into the capsule.
- Compaction-before-seal gate: if context compacts before the current
  source-heavy unit artifact is written and hashed, the run must stop as
  `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL`; any partial outputs from that unit
  are contaminated scratch until archived or cleanly rerun.
- Readback economy gate: prompt validation must use targeted existence, hash,
  marker, status, and count checks. It must not require full artifact echo, full
  ledger-row echo, pasted Evidence Units, or broad source dumps unless a
  targeted failure makes that exact excerpt necessary.
- Retrieval-metadata gate: new or materially touched durable prompt artifacts
  must follow `.agents/workflow-overlay/retrieval-metadata.md` without using
  retrieval metadata as authority, validation proof, approval, readiness,
  lifecycle completion, deployment/install/resolver status, or edit permission.
- Rerun economy gate: retry prompts must name the prior artifact, frozen decisions, mutable fields, and unresolved finding.
- Leakage gate: prompt artifacts must not copy `jb` templates, GAP/CV Engine paths, compiler paths, handoff rules, product-lead rules, or repo-local lifecycle mechanics.

## Product Proof Gates

- Judgment Spine claim-tier gate: Judgment Spine product-learning,
  buyer-proof, advisory, backtest, fixture, model-run, scoring, memo, deck,
  calibration, architecture, spec, prompt, wrapper, and runbook artifacts must
  classify the claim tier and closeout state using
  `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md` before
  making proof, readiness, validation, fixture-admission, scoring,
  blind-use-readiness, or judgment-quality claims. Product-Learning evidence
  cannot be reused as Buyer-Proof or Judgment-Quality evidence without the
  explicit promotion gate for the stronger tier. Classifications must apply the
  ladder's weakest-cleared-gate rule: source-quality and execution-quality gaps
  cap the claim at the lowest cleared gate, and missing evidence is not a pass.
  If no durable evidence exists for the evaluated run, answer, proof, scoring,
  or judgment-quality claim, the closeout state is `no_durable_evidence`.
  The classification must appear inline in the artifact being classified or
  co-reference a durable classification record with a path, hash, or equivalent
  retrieval handle.
  Architecture, spec, prompt, wrapper, and runbook artifacts are design or
  product-learning inputs by default; they are not Buyer-Proof or
  Judgment-Quality evidence unless the stronger tier's receipt is satisfied.

- Objection/refusal gate: product-proof, customer-discovery, buyer-proof, memo,
  deck, and readback artifacts must not treat initial buyer skepticism as a
  kill criterion. They must classify skepticism as `trust_objection` unless
  the buyer refuses the evidence type regardless of evidence quality, examples,
  numbers, mechanism, case logic, or proof experience.
- Trust-refusal gate: only `trust_refusal` may disqualify on public-signal
  trust grounds. `trust_objection` is proof material and must be captured,
  tested, and read back when other qualification gates pass.
- Pull-versus-praise gate: product-proof artifacts must distinguish observable
  decision or budget-adjacent behavior from approval language, praise,
  curiosity, generic research interest, or requests for source volume.
- Zero-spoiler backtest gate: case-study, consulting-case, preflight,
  participant-packet, and backtest artifacts must not expose actual decisions,
  consulting recommendations, implementation actions, post-cutoff facts,
  outcomes, result quality, or leaking source titles/snippets/URLs before the
  owner or participant blind judgment is sealed. If leakage occurs, the
  participant-facing packet is contaminated and must be rebuilt from clean
  pre-cutoff sources before blind use.

## Enforcement Placement

A load-bearing rule that is mechanically checkable at a tool boundary is
enforced there — a write-time hook plus a portable checker with a `--strict`
commit/CI mode — rather than carried only as an instruction, which fires only
when the model attends to it. The checker references the rule's authority and
never restates it; it is advisory and forward-only by default. Judgment-based
rules (claim discipline, scope, lifecycle reasoning) stay resident and still
must actually fire, not merely be present; a substrate enforces shape, never
truth (cf. the receipt-field provenance gate above). The per-rule
classification and the owner gate for building each substrate live in
`docs/decisions/overlay_enforcement_placement_classification_v0.md`.

Active instance: the retrieval-header check
(`.agents/hooks/check_retrieval_header.py`, EP-06) enforces
`.agents/workflow-overlay/retrieval-metadata.md` at the write boundary and is
registered in the repo map's "Active Hooks" note; reuse this pattern for the
next such rule. Placement decides where a rule is enforced, not whether it is
correct: a passing check is not validation, readiness, approval, or
source-of-truth promotion.

**Retrieval-header index + forward-only CI gate** (`.agents/hooks/header_index.py`).
Companion to EP-06. Adds three non-blocking surfaces and one CI gate:
- `--index`: full retrieval view of all header-bearing durable docs (human use).
- `--health [--verbose]`: whole-repo advisory counts of MISSING-HEADER and ORPHAN
  docs; exit 0 always (backlog surfaced, not gated).
- `--health --oneline`: single capsule line emitted by `session_context_capsule.py`
  at session start so every lane sees the advisory health count without walking the
  tree itself.
- `--strict`: **CI gate — diff-scoped, forward-only.** For changed durable `.md`
  files only (vs `$GITHUB_BASE_REF` or `origin/main`): fails (exit 1) if a
  changed doc is MISSING-HEADER or is an ORPHAN (not substring-found in the repo
  map or any submap).  Pre-existing backlog is never gated — only new/changed docs
  are in scope.  Fails OPEN (exit 0) if diff-scoping is unavailable; never falls
  back to whole-repo strict.
Registered in `.github/workflows/ci.yml` after the existing link-check step.

**Google search-surface route guard**
(`.agents/hooks/check_search_surface_google_route.py`). Diff-scoped CI plus
advisory PostToolUse checker for the mechanically checkable shell of
`docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md`:
Google Search capture URLs in changed durable docs carry the bound route
parameters; artifacts using the route carry the physical-locality non-claim; and
blocked Google pages with visible exit-IP content are not preserved in durable
docs. This is route-shape enforcement only. It is not physical-locality proof,
source sufficiency, validation, readiness, demand proof, Judgment evidence, or
Product Lead evidence.

**Retrieval-header forbidden-field scan** (`.agents/hooks/check_retrieval_header.py`,
EP-07 forbidden-field subset — the part previously deferred). The shared header
predicate (`header_problems_for_lines`, used by both the write-time `--hook` and
the `header_index.py --strict` CI gate) now also rejects status-leak keys in a
retrieval header — approval / validation / readiness / lifecycle / deployment /
install / resolver / publication / source-of-truth status — referencing
`retrieval-metadata.md` ("Forbidden Header Fields"), never restating it.
Born-green (no current in-scope header uses these keys). `edit_permission` /
`verdict` / `status` are intentionally NOT banned: review-output and prompt
frontmatter legitimately carry them. A `use_when` 1–3 count and a closed
allowed-key set were assessed and intentionally NOT enforced — the corpus mixes
retrieval-header fields with required review/prompt-provenance frontmatter in one
block, so neither is born-green. Placement enforces header shape, never truth.

**Doctrine-change receipt-shape gate** (`.agents/hooks/check_dcp_receipt.py`,
EP-09 shape subset). Diff-scoped, forward-only CI gate (a sibling to the
deletion-evidence gate): for changed `.md` files it validates that any real
`direction_change_propagation` receipt or `direction_change_propagation_blocker`
present is shape-valid — required keys present, `trigger` / `related_triggers`
drawn only from the seven controlled trigger values, `non_claims` a non-empty
list — referencing `source-of-truth.md` (Doctrine Change Propagation Contract),
never restating it. It validates SHAPE only: it does NOT decide whether an edit
is doctrine-changing, so it never requires a receipt to be *present* (the EP-09
over-edge stays resident judgment), and it never asserts a listed
controlling/downstream surface was truly updated or checked. Contract template
blocks and non-receipt note-markers are skipped. The inline-receipt cap, archive
pointer, and "no standalone receipt files" rules are deliberately NOT gated here
(not born-green; several controlling files already hold >2 inline receipts).
Registered in `.github/workflows/ci.yml`; whole-repo advisory backlog via
`--audit`; `--selftest` present.

**Review-routing disposition gate** (`.agents/hooks/check_review_routing.py`,
EP-35). Diff-scoped, forward-only CI gate plus a local commit-msg advisory: a
change touching code roots must carry its review disposition — a review
artifact filed in the same change, or a shape-valid `review_routing_status`
line (grammar owned by the Current Gates bullet above), with `routed` paths
verified to exist. Born from the 2026-07-02 fused-lane audit: most fused
implementation lanes closed without filing the delegated-review handoff their
contract carried, several claimed it in commit prose without filing it, and
the disposition lived only in chat where nothing durable could check it
(51 of 67 code-root landings in the trailing 120 main commits carried no
disposition at build time — advisory backlog via `--audit`, never gated).
The gate checks disposition PRESENCE and SHAPE only — never the truth of a
`not_needed` reason, the quality of a filed review, or whether review should
have been recommended (resident judgment; cf. the receipt-field provenance
gate). Registered in `.github/workflows/ci.yml` and `.githooks/commit-msg`;
`--selftest` present.

**Local pre-push doc-gate mirror** (`.agents/hooks/pre_push_guard.py`, the
policy behind the `.githooks/pre-push` adapter). For a push whose update lines
pass the guard's safety checks, the guard also runs the strict doc gates CI
runs — `check_map_links.py --strict`, `header_index.py --strict`,
`check_review_routing.py --strict` (diff-scoped checkers default to base
`origin/main`, the same base CI resolves for a PR) — so a forward-only gate
miss, e.g. a reviewer-authored `docs/review-outputs/**` report missing its
retrieval header (the PR #613 red round), fails at the push boundary instead
of costing a CI round. Same checkers, same rule owners; the mirror adds no
rule. A nonzero or unlaunchable gate blocks the push (the GATE FAIL bucket
above); the checkers' own infra-gap fail-opens are unchanged. Write-time note:
the EP-06 retrieval-header advisory already covers `docs/review-outputs/**`
writes at the Claude Code write boundary; this mirror is the harness-agnostic
catch for writes that advisory cannot see or that ignored it. Local Git hook
only: bypassable with `--no-verify`; CI remains the authoritative boundary; a
green pre-push is not validation, readiness, or approval.

**Handoff-pointer resolution gate** (`.agents/hooks/check_handoff_pointers.py`,
EP-36). Diff-scoped, forward-only CI gate for the Current Gates bullet above:
handoff-packet paths referenced in changed durable docs must resolve in the
same tree, or the pointer line must carry an explicit pin or exemption marker.
Born from repeated cold-agent resolution failures: packets authored on
unmerged lane branches — e.g. `docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md`, reachable only on its authoring branch — were
referenced by filed courier/patch prompts that landed on `main`, so receiving
agents and delegated reviewers starting cold from `main` could not find them
(both the receiving agent and a delegated reviewer failed on that packet; the
`--audit` backlog at build time showed 17 unresolved pointers across at least
six distinct packets — surfaced, never gated). Because the gate runs on the
landing PR's tree, it mechanically enforces the merge-ordering rule without
needing to see lane starts. A write-time PostToolUse advisory was
intentionally NOT built: the defect is a merge-topology property (packet on a
different unmerged branch), invisible at the write boundary where the packet
usually exists in the author's own tree. Registered in
`.github/workflows/ci.yml`; `--selftest` present. Pointer shape only — a
green run never proves packet content, freshness, or pin truth.


## Future Gates

- Orca independence dry run: UNKNOWN - requires owner input.
- Product/domain validation: UNKNOWN - requires owner input.
- Runtime or integration validation: UNKNOWN - requires owner input.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca validation doctrine adds a review-routing disposition gate: a change
    touching code roots (orca-harness/, .agents/hooks/) must carry its review
    disposition -- a review artifact added under docs/prompts/reviews/ or
    docs/review-outputs/ in the same change, or a shape-valid
    review_routing_status line (routed <existing path> | blocked -- <reason> |
    not_needed -- <reason>) in the change's commit messages -- enforced
    diff-scoped and forward-only by .agents/hooks/check_review_routing.py
    (EP-35) as a CI --strict gate plus a local commit-msg advisory. Born from
    the 2026-07-02 fused-lane audit: fused implementation lanes carried a
    delegated-review obligation whose disposition lived only in chat, so most
    lanes closed without filing it and nothing durable could check the miss.
  trigger: validation_philosophy
  related_triggers:
    - review_authority
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_review_routing.py
    - .github/workflows/ci.yml
    - .githooks/commit-msg
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .claude/settings.json
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already routes validation and enforcement-placement changes to this
        overlay file; a kernel restatement would fork the owner.
    - path: .agents/workflow-overlay/review-lanes.md
      reason: >
        The gate binds no review lane and creates no verdict or severity
        authority; a pointer would dual-home the disposition rule.
    - path: .agents/workflow-overlay/delegated-review-patch.md
      reason: >
        The convention stays provisional and opt-in; the gate enforces
        disposition visibility on code lanes generally, not this convention.
    - path: .claude/settings.json
      reason: >
        No PostToolUse wiring; the disposition is a commit-message property,
        not a file-write property. The local boundary is .githooks/commit-msg.
    - path: user-level fused skill source (~/.claude/skills/fused/SKILL.md)
      reason: >
        Outside Orca authority (installed/user-level skill source is
        protected); the owner applies the companion skill edit separately.
  stale_language_search: >
    rg -n "review_routing_status" .agents docs AGENTS.md
  stale_language_search_result: >
    Executed 2026-07-02 before this change: the token appeared only in one
    workflow handoff note (flagged there as an unowned one-off field) and one
    data-lake scoping record; no live overlay surface owned it. This change
    makes validation-gates.md the owning surface; the checker references it
    and does not restate it.
  non_claims:
    - not validation
    - not readiness
    - not review quality, severity, or verdict authority
    - not a bound or mandatory review lane
    - a green run is disposition shape only, never proof a review happened or was sufficient
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca validation doctrine adds a handoff-pointer resolution gate: a changed
    durable .md file must not reference a handoff-packet path
    (docs/workflows/*handoff*.md, docs/prompts/handoffs/*.md) that does not
    resolve in the same tree, unless the pointer line carries an explicit
    resolution pin (branch / PR # / origin ref vocabulary) or an exemption
    marker -- enforced diff-scoped and forward-only by
    .agents/hooks/check_handoff_pointers.py (EP-36) as a CI --strict gate.
    Born from repeated cold-agent resolution failures where handoff packets
    lived only on unmerged authoring branches while filed prompts referencing
    them landed on main, so receiving agents and delegated reviewers starting
    cold from main could not resolve their required reads.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/check_handoff_pointers.py
    - .github/workflows/ci.yml
    - orca-harness/tests/unit/test_hook_internal_error_gating.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/source-of-truth.md
    - .claude/settings.json
    - .agents/hooks/check_map_links.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already routes validation and enforcement-placement changes to this
        overlay file; a kernel restatement would fork the owner.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Per the enforcement-placement principle a substrate-enforced rule is
        not also carried as a resident instruction; prompt authors hit the CI
        gate mechanically, and the existing worktree-preflight and
        input-prompt-source rules already carry the judgment side (which
        branch, which source) that stays resident.
    - path: .claude/settings.json
      reason: >
        No PostToolUse wiring: the defect is a merge-topology property
        (packet on a different unmerged branch), invisible at the write
        boundary where the packet usually exists in the author's own tree;
        the enforcing boundary is CI on the landing PR.
    - path: .agents/hooks/check_map_links.py
      reason: >
        Its C1/C2/C4 checks gate map files, open_next headers, and inline
        markdown links whole-corpus; the new gate covers prose/backtick
        handoff pointers diff-scoped with pin/exemption vocabulary --
        different scope and exemption grammar, kept as a sibling checker.
  stale_language_search: >
    rg -in "handoff.*resolv|resolve.*handoff|unmerged.*handoff|check_handoff_pointers"
    AGENTS.md .agents docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-03 after edits: hits are this gate's own rule text,
    checker, README row, and registration surfaces, plus unrelated generic
    mentions (the AGENTS.md jb-handoffs boundary sentence and skill-adoption
    skill-name rows); no other surface carries a conflicting handoff-pointer
    resolution rule.
  non_claims:
    - not validation
    - not readiness
    - not packet content freshness, pin truth, or source-choice correctness
    - not a courier-delivery guarantee for prompts that never land in the repo
    - a green run is pointer shape only, never proof the right packet was cited
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
