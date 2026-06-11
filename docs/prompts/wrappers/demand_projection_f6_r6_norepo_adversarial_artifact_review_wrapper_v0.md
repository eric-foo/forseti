# Thin Wrapper — no_repo Adversarial Artifact Review Courier: Demand-Projection F6+R6 Revised Design (v0)

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: >
  Courier wrapper delivering the no_repo adversarial-artifact-review bundle for
  demand_projection_f6_r6_revised_design_v0.md to an external, repo-blind, cross-vendor
  de-correlated reviewer. Carries the who-constraint, hash pins, and return routing; all
  method/authority/commission content lives in the bundle README.
use_when:
  - Dispatching the commissioned de-correlated review of the F6+R6 revised design.
  - Re-dispatching the same bundle unchanged (verify hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Wrapped source (bundle README):
  `docs/review-inputs/demand_projection_f6_r6_norepo_adversarial_artifact_review_bundle_v0/README.md`
  — SHA256 `89C2EF81D9E8F14A6DCCC9B094D368B075C6603BB587E8E4D7579A490A3CE894`
- Review target attachment:
  `docs/review-inputs/demand_projection_f6_r6_norepo_adversarial_artifact_review_bundle_v0/demand_projection_f6_r6_revised_design_v0.md`
  — SHA256 `91ACE1B76852006A29A6AB4DF44D3DC108EDA3DF8B33F4C2373DF46D492B0C2F`
- Operator workspace (dispatch side): `C:\Users\vmon7\Desktop\projects\orca`, branch
  `ecr-sp3-timing-deriver-slice1`. Receiver side: NOT APPLICABLE — the reviewer is repo-blind
  by commission (`no_repo` access mode); content identity is carried by the SHA256 pins, not
  by branch state.
- Dirty-state allowance: bundle files may be dispatched from the working tree; the hash pins
  above are the integrity contract. If either file changes, re-pin before dispatch.
- Output mode: `paste-ready-chat` (this wrapper's body below). Receiver review output:
  chat transcript findings (the receiver cannot write files). Durable report: written by the
  home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/demand_projection_f6_r6_revised_design_adversarial_artifact_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery` recorded.
- Edit permission: receiver none (advisory-only, returns findings, never a diff).
- Preflight failure behavior (receiver-side, carried in the body): Anthropic/Claude lineage or
  undisclosed lineage → `BLOCKED_DECORRELATION`; unreadable attachments →
  `BLOCKED_BUNDLE_UNREADABLE`; hash unconfirmable → proceed advisory-only and say so.
- Workflow sequence (overlay-owned): `workflow_sequence_policy: overlay_owned`,
  `workflow_sequence_source: active_overlay`, `workflow_sequence_status: bound` — per
  `.agents/workflow-overlay/delegated-review-patch.md` (no_repo loop): de-correlated discovery
  review (this dispatch) → home-CA review-return adjudication → CA applies accepted amendments
  to the single target → bounded SAME-vendor mechanical-tier post-patch recheck → keep
  decision. Cross-vendor de-correlation is reserved for this discovery pass.

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
thread_operating_target: >
  Make the demand-projection three-valued honesty contract hold on the proven path at
  smallest-complete scope: every (entity, signal_type, period) coordinate resolves to exactly
  one of OBSERVATION / typed GAP / REFUSAL, with no silent fourth outcome and no false GAP;
  nothing is built, ratified, or merged until the revised design clears one de-correlated
  cross-vendor check.
```

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch, prompt-orchestration, review-lanes,
    template-registry, artifact-folders, artifact-roles, skill-adoption, source-loading,
    decision-routing; templates: portable-adversarial-artifact-review-method, thin-wrapper)
  edit_permission: docs-write (bundle + wrapper artifacts only)
  target_scope: docs/review-inputs/demand_projection_f6_r6_norepo_adversarial_artifact_review_bundle_v0/,
    docs/prompts/wrappers/demand_projection_f6_r6_norepo_adversarial_artifact_review_wrapper_v0.md
  dirty_state_checked: yes (controlling overlay sources clean; unrelated lane files dirty and
    untouched; doctrine change: none — this commission uses the provisional convention,
    changes no overlay)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destinations bound directly by artifact-folders/artifact-roles overlay files.
freshness_gate: PASS 2026-06-11 — portable-method derived_from pins matched live sources
  (0CB80057…B60C3FC; 7FD702F5…F3C22).
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
   SHA256 89C2EF81D9E8F14A6DCCC9B094D368B075C6603BB587E8E4D7579A490A3CE894
2. demand_projection_f6_r6_revised_design_v0.md — the review target.
   SHA256 91ACE1B76852006A29A6AB4DF44D3DC108EDA3DF8B33F4C2373DF46D492B0C2F

If you cannot read the attached files, reply ONLY `BLOCKED_BUNDLE_UNREADABLE`. If you can
compute SHA256, confirm the target matches its pin and say so; if you cannot compute hashes,
proceed advisory-only and say so.

TASK: Read README.md fully, then execute exactly what it specifies — a read-only,
advisory-only, MAXIMALLY ADVERSARIAL artifact review of the review target,
reasoning-pass-first, findings-first, per the PORTABLE METHOD in README §4 and the commission
in README §2. You have NO repository access: treat the target's file:line citations as
authored evidence claims; attack the reasoning, internal consistency, completeness,
contract-closure logic, and scope discipline; label anything settleable only by reading the
repository as `unverifiable from provided sources`. Do not patch, do not emit executor-ready
steps, do not claim validation, readiness, or approval.

RETURN: your full review in this chat, in the README §4.6 output shape — compact
review_summary YAML first, then findings ordered critical → major → minor, each with
severity / location / issue / evidence / impact / minimum_closure_condition /
next_authorized_action / advisory remediation direction. Your findings are decision input
only for the commissioning Chief Architect; they create no approval, validation, or
readiness.
````

## Dispatch notes (operator)

- Attach BOTH bundle files to the same external-chat message as the pasted body. If the
  reviewer UI cannot attach files, fall back per the overlay binding: paste the README body
  inline FIRST (it is self-contained), then the target — never point a repo-blind reviewer at
  files it cannot open.
- On return, courier the reviewer's full output back into the home lane and invoke
  review-return adjudication (`workflow-delegated-review-patch`, review-return mode). Record
  `reviewed_by` (the actual reviewer model+version, or `unrecorded`) on the durable report.
- Non-claims: provisional convention; advisory findings only; no validation, readiness,
  formal verdict, or build authorization; token-saving figures of the underlying convention
  remain UNMEASURED hypotheses.
