# Thin Wrapper — no_repo Adversarial Artifact Review Courier: Data Lake Consumption Seam Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: >
  Courier wrapper delivering the no_repo adversarial-artifact-review bundle for
  core_spine_v0_data_lake_consumption_seam_contract_v0.md to an external, repo-blind,
  cross-vendor de-correlated reviewer. Carries the who-constraint, hash pins, and return
  routing; all method/authority/commission content lives in the bundle README.
use_when:
  - Dispatching the commissioned de-correlated review of the consumption seam contract.
  - Re-dispatching the same bundle unchanged (verify hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Wrapped source (bundle README):
  `docs/review-inputs/data_lake_consumption_seam_contract_norepo_adversarial_artifact_review_bundle_v0/README.md`
  — SHA256 `369943214969C822BAC27AF2FB3171E5A6B5AAEDDA854E440FD6F117B85FE4F6`
- Review target attachment:
  `docs/review-inputs/data_lake_consumption_seam_contract_norepo_adversarial_artifact_review_bundle_v0/core_spine_v0_data_lake_consumption_seam_contract_v0.md`
  — SHA256 `C3D5A74B74273982C7E0192BB52504B0754E4F92DBF641DD39332B2B18D6C159`
  (byte-identical to the in-repo target at commit `a7812c4d`)
- Operator workspace (dispatch side):
  `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\elated-cannon-a6e2cf`, branch
  `claude/elated-cannon-a6e2cf` (PR #580). Receiver side: NOT APPLICABLE — the reviewer is
  repo-blind by commission (`no_repo` access mode); content identity is carried by the
  SHA256 pins, not by branch state.
- Dirty-state allowance: bundle files may be dispatched from the working tree; the hash pins
  above are the integrity contract. If either file changes, re-pin before dispatch.
- Output mode: `paste-ready-chat` (this wrapper's body below). Receiver review output: chat
  transcript findings (the receiver cannot write files). Durable report: written by the home
  CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/data_lake_consumption_seam_contract_adversarial_artifact_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery` recorded.
- Edit permission: receiver none (advisory-only, returns findings, never a diff).
- Preflight failure behavior (receiver-side, carried in the body): Anthropic/Claude lineage
  or undisclosed lineage → `BLOCKED_DECORRELATION`; unreadable attachments →
  `BLOCKED_BUNDLE_UNREADABLE`; hash unconfirmable → proceed advisory-only and say so.
- Workflow sequence (overlay-owned): `workflow_sequence_policy: overlay_owned`,
  `workflow_sequence_source: active_overlay`, `workflow_sequence_status: bound` — per
  `.agents/workflow-overlay/delegated-review-patch.md` (no_repo loop): de-correlated
  discovery review (this dispatch) → home-CA review-return adjudication → CA applies
  accepted amendments to the single target → bounded SAME-vendor mechanical-tier post-patch
  recheck → keep decision. Cross-vendor de-correlation is reserved for this discovery pass.

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
thread_operating_target: >
  Land consumption seam v0 as the one tested way every derived lane picks up committed
  Bronze work: contract + shared helper + rebuild runner + one proving consumer, with
  metrics on-demand-first and views never authoritative; nothing is ratified or accepted
  until this de-correlated discovery review returns and the home CA adjudicates it.
```

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch, prompt-orchestration Orca Prompt Preflight +
    review family, review-lanes routine shape, template-registry, source-loading routine
    shape; templates: portable-adversarial-artifact-review-method, thin-wrapper; precedent
    bundle demand_projection_f6_r6)
  edit_permission: docs-write (bundle + wrapper + template re-derivation artifacts only)
  target_scope: docs/review-inputs/data_lake_consumption_seam_contract_norepo_adversarial_artifact_review_bundle_v0/,
    docs/prompts/wrappers/data_lake_consumption_seam_contract_norepo_adversarial_artifact_review_wrapper_v0.md,
    docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md (re-derivation)
  dirty_state_checked: yes (lane branch claude/elated-cannon-a6e2cf; implementation commits
    a7812c4d/d6c77c99 pushed; prompt artifacts authored on top)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destinations bound directly by artifact-folders overlay file.
freshness_gate: PASS 2026-07-02 after re-derivation — portable-method derived_from pins
  re-derived/re-pinned this date (template read-budget audit folded into method §6;
  review-lanes changes pin-only) and now match live sources (c5c4e7d3…33e9c4; ddc3e03b…50d).
```

## Paste-ready courier body (attach both bundle files to the same message)

````markdown
You are the de-correlated external reviewer ("controller") for a no-repo-access ADVERSARIAL
ARTIFACT REVIEW commissioned by another lane.

WHO-CONSTRAINT — gate yourself before anything else: the review target was authored by an
Anthropic (Claude-family) model. This commission requires the reviewer to be a DIFFERENT
vendor / model lineage (vendor = the upstream model developer, not the hosting platform,
reseller, or wrapper). If you are an Anthropic/Claude-lineage model, or your lineage is
unknown or undisclosable, reply ONLY `BLOCKED_DECORRELATION` (plus your vendor if permitted)
and stop. This is a who-constraint of the commission — never a model recommendation or
ranking. State your model identity and version in your output if known and permitted.

ATTACHED BUNDLE (2 files):
1. README.md — your complete method, authority excerpts, commission, and output contract.
   SHA256 369943214969C822BAC27AF2FB3171E5A6B5AAEDDA854E440FD6F117B85FE4F6
2. core_spine_v0_data_lake_consumption_seam_contract_v0.md — the review target: the Data
   Lake consumption seam contract (how every derived lane picks up committed work and
   acknowledges completion, the index rebuild-command binding, and the on-demand-first
   metrics policy).
   SHA256 C3D5A74B74273982C7E0192BB52504B0754E4F92DBF641DD39332B2B18D6C159

If you cannot read the attached files, reply ONLY `BLOCKED_BUNDLE_UNREADABLE`. If you can
compute SHA256, confirm the target matches its pin and say so; if you cannot compute hashes,
proceed advisory-only and say so.

TASK: Read README.md fully, then execute exactly what it specifies — a read-only,
advisory-only, MAXIMALLY ADVERSARIAL artifact review of the review target,
reasoning-pass-first, findings-first, per the PORTABLE METHOD in README §4 and the
commission in README §2. You have NO repository access: treat the target's file/symbol
citations as authored evidence claims; attack the reasoning, internal consistency,
authority conformance (README §3 excerpts), completeness, and scope discipline — including
whether the obligation-fingerprint pickup model, the ack-namespace rule, the six-point
conformance contract, the weaker undone-view semantics, and the metrics policy can actually
deliver "every derived lane picks up committed work the same tested way" without a queue
becoming truth, a view becoming load-bearing, or missing evidence becoming zero. Label
anything settleable only by reading the repository as `unverifiable from provided sources`.
Do not patch, do not emit executor-ready steps, do not claim validation, readiness, or
approval.

RETURN: your full review in this chat, in the README §4.6 output shape — compact
review_summary YAML first, then findings ordered critical → major → minor, each with
severity / location / issue / evidence / impact / minimum_closure_condition /
next_authorized_action / advisory remediation direction, closing with the one-line
read-budget audit over the provided files. Your findings are decision input only for the
commissioning Chief Architect; they create no approval, validation, or readiness.
````

## Dispatch notes (operator)

- Attach BOTH bundle files to the same external-chat message as the pasted body. If the
  reviewer UI cannot attach files, fall back per the overlay binding: paste the README body
  inline FIRST (it is self-contained), then the target — never point a repo-blind reviewer
  at files it cannot open.
- Your stated paste target (a ChatGPT-family / OpenAI model) satisfies the cross-vendor
  who-constraint against the Anthropic author; pasting into any Anthropic/Claude-family
  model would defeat de-correlation.
- On return, courier the reviewer's full output back into the home lane and invoke
  review-return adjudication (`workflow-delegated-review-patch`, review-return mode). Record
  `reviewed_by` (the actual reviewer model+version, or `unrecorded`) on the durable report.
- The landed implementation diff (PR #580) is NOT part of this artifact commission; a
  code-lane pass over the diff is a separate owner option (e.g. `/code-review ultra 580` or
  a `delegated_code_review_and_patch` commission).
- Non-claims: provisional convention; advisory findings only; no validation, readiness,
  formal verdict, or build authorization; token-saving figures of the underlying convention
  remain UNMEASURED hypotheses.
