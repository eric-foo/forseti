# Validation Gates

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Validation gates required before Orca completion claims.
use_when:
  - Checking whether an Orca completion, prompt, or artifact claim has required evidence.
  - Defining validation expectations for non-implementation architecture, proof, prompt, and artifact work.
authority_boundary: retrieval_only
```

Validation must be able to fail. Missing evidence is not a pass.

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
- Source-resolution gate: `agent-workflow` may provide generic mechanics only; installed skills are deployment copies; `jb` project policy must not be imported.
- Worktree preflight gate: repository-aware prompts must state workspace, revision or hash when needed, dirty-state allowance, target scope, and edit permission.
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
- Source-heavy economy gate: prompts that require public web/source research,
  several external page opens, source ledgers, post-window comparisons, or
  several large artifact reads must define a source-loading unit and require the
  unit artifact to be written and hashed before the next unit starts.
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

## Future Gates

- Orca independence dry run: UNKNOWN - requires owner input.
- Product/domain validation: UNKNOWN - requires owner input.
- Runtime or integration validation: UNKNOWN - requires owner input.
