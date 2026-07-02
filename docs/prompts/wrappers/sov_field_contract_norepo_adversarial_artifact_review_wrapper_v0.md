# Thin Wrapper — no_repo Adversarial Artifact Review Courier: Share-of-Voice Field Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: >
  Courier wrapper delivering the no_repo adversarial-artifact-review bundle for
  core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md to
  an external, repo-blind, cross-vendor de-correlated reviewer. Carries the
  who-constraint, hash pins, and return routing; method/authority/commission
  live in the bundle README.
use_when:
  - Dispatching the commissioned de-correlated review of the SoV field contract.
  - Re-dispatching the same bundle unchanged (verify hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Wrapped source (bundle README):
  `docs/review-inputs/sov_field_contract_norepo_adversarial_artifact_review_bundle_v0/README.md`
  — SHA256 `548A15D3374ACC791FF16C3DC97EDE46BB1731E4A91A7E1DDBAFFF7EBF66C12C`
- Review target attachment:
  `docs/review-inputs/sov_field_contract_norepo_adversarial_artifact_review_bundle_v0/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md`
  — SHA256 `33C7F793AB049A9EE3655A7194FF39B8E3B83307D8B1C63E1A3D97FB24792F4B`
  (byte-identical to the in-repo target at commit `b0a31c88`)
- Operator workspace (dispatch side):
  `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\elated-cannon-a6e2cf`, branch
  `claude/sov-field-contract`. Receiver side: NOT APPLICABLE — repo-blind by
  commission (`no_repo`); content identity travels by the SHA256 pins.
- Output mode: `paste-ready-chat` (body below). Receiver output: chat findings.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/sov_field_contract_adversarial_artifact_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`.
- Edit permission: receiver none (advisory-only findings, never a diff).
- Preflight failure behavior (receiver-side, carried in the body):
  Anthropic/Claude or undisclosed lineage → `BLOCKED_DECORRELATION`; unreadable
  attachments → `BLOCKED_BUNDLE_UNREADABLE`; hash unconfirmable → proceed
  advisory-only and say so.
- Workflow sequence (overlay-owned): `workflow_sequence_policy: overlay_owned`,
  `workflow_sequence_source: active_overlay`, `workflow_sequence_status: bound`
  — per `.agents/workflow-overlay/delegated-review-patch.md` (no_repo loop):
  de-correlated discovery review (this dispatch) → home-CA review-return
  adjudication → CA applies accepted amendments → bounded SAME-vendor
  mechanical-tier post-patch recheck → keep decision.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch overlay binding + portable method
    template, both already loaded/re-derived this thread; SoV field contract +
    seam contract + Silver Vault posture rules as authority sources)
  edit_permission: docs-write (bundle + wrapper artifacts only)
  target_scope: docs/review-inputs/sov_field_contract_norepo_adversarial_artifact_review_bundle_v0/,
    docs/prompts/wrappers/sov_field_contract_norepo_adversarial_artifact_review_wrapper_v0.md
  dirty_state_checked: yes (lane claude/sov-field-contract; contract committed b0a31c88)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destinations bound directly by artifact-folders overlay file.
freshness_gate: PASS 2026-07-02 — portable method re-derived earlier this same
  day; derived_from pins match live sources; no source change since.
```

## Paste-ready courier body (attach both bundle files to the same message)

````markdown
You are the de-correlated external reviewer ("controller") for a no-repo-access
ADVERSARIAL ARTIFACT REVIEW commissioned by another lane.

WHO-CONSTRAINT — gate yourself before anything else: the review target was
authored by an Anthropic (Claude-family) model. This commission requires the
reviewer to be a DIFFERENT vendor / model lineage (vendor = the upstream model
developer, not the hosting platform, reseller, or wrapper). If you are an
Anthropic/Claude-lineage model, or your lineage is unknown or undisclosable,
reply ONLY `BLOCKED_DECORRELATION` (plus your vendor if permitted) and stop.
This is a who-constraint of the commission — never a model recommendation or
ranking. State your model identity and version in your output if known and
permitted.

ATTACHED BUNDLE (2 files):
1. README.md — your complete method, authority excerpts, commission, and
   output contract.
   SHA256 548A15D3374ACC791FF16C3DC97EDE46BB1731E4A91A7E1DDBAFFF7EBF66C12C
2. core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md —
   the review target: the field-level contract every share-of-voice
   computation/view over a source-backed social-evidence data lake must
   conform to (readout identity, grouping, numerator/denominator/coverage,
   window basis, posture semantics, forbidden fields).
   SHA256 33C7F793AB049A9EE3655A7194FF39B8E3B83307D8B1C63E1A3D97FB24792F4B

If you cannot read the attached files, reply ONLY `BLOCKED_BUNDLE_UNREADABLE`.
If you can compute SHA256, confirm the target matches its pin and say so; if
you cannot compute hashes, proceed advisory-only and say so.

TASK: Read README.md fully, then execute exactly what it specifies — a
read-only, advisory-only, MAXIMALLY ADVERSARIAL artifact review of the target,
reasoning-pass-first, findings-first, per the PORTABLE METHOD in README §4 and
the commission in README §2. You have NO repository access: attack the field
semantics — can a conforming readout still mislead a buyer (silent denominator
shrinkage, fragmentation gaming, cohort cherry-picking, window-basis abuse,
zero/posture leaks, coverage fields present but decision-useless)? Are the
forbidden-fields and upgrade-trigger boundaries actually closed? Is anything
under- or over-specified for the next actor (a view builder)? Label
repo-settleable claims `unverifiable from provided sources`. Do not patch, do
not emit executor-ready steps, do not claim validation, readiness, or approval.

RETURN: your full review in this chat, in the README §4.6 output shape —
compact review_summary YAML first, then findings ordered critical → major →
minor with severity / location / issue / evidence / impact /
minimum_closure_condition / next_authorized_action / advisory remediation
direction, closing with the one-line read-budget audit. Your findings are
decision input only for the commissioning Chief Architect.
````

## Dispatch notes (operator)

- Attach BOTH bundle files to the same external-chat message as the pasted
  body; if the reviewer UI cannot attach files, paste the README inline FIRST,
  then the target.
- Your usual paste target (ChatGPT-family / OpenAI) satisfies the cross-vendor
  who-constraint against the Anthropic author.
- On return, courier the reviewer's full output back into the home lane for
  review-return adjudication (same loop as the seam-contract review).
- Non-claims: provisional convention; advisory findings only; no validation,
  readiness, formal verdict, or build authorization.
