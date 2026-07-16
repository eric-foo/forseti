# Preflight Smallest-Complete Reduction — Delegated Review & Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Lane review commission (delegated review-and-patch)
scope: >
  Cross-vendor adversarial review-and-patch commission for the prompt-preflight
  ceremony reduction on lane claude/preflight-ceremony-eval-d01edb.
use_when:
  - Couriering the delegated review of the preflight-reduction diff.
authority_boundary: retrieval_only
```

output_mode: paste-ready-chat — the body below is the couriered deliverable; findings return in chat on this lane.

---

You are a delegated adversarial reviewer-and-patcher for Forseti. This
commission is preparation-only until an operator couriers it to you; do not
claim dispatch readiness on its behalf.

preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated inline. The `environment_baseline`, `lifecycle_hard_stop`, and `decorrelation_commission` constants there bind you.

edit_permission: patch-only
target_kind: delegated_code_review_and_patch
author_vendor: Anthropic
delegate_vendor: operator_to_fill
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
access: repo
delivery: operator_courier_only
receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind

**Goal:** confirm the preflight-ceremony reduction cut only restated ceremony
and kept every load-bearing guard, and patch any defect you find within scope.
**Done looks like:** each finding carries evidence from the actual diff and
sources; any patch is bounded to the named files; validation evidence is real
(pass/fail/not-run stated); a verdict plus residual risk closes the return.

Target state (fresh read at authoring):
- worktree: `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\preflight-ceremony-eval-d01edb`
- branch: `claude/preflight-ceremony-eval-d01edb`
- reviewed diff: `1d141a9c..81b3ced2` (base = merge-base with origin/main; target = the implementation commit). Commits above 81b3ced2 on this branch carry only this commission artifact and are out of patch scope.
- dirty-state: clean tree required before you begin; stop on drift.

Patchable file scope (exactly these five):
- `.agents/workflow-overlay/prompt-orchestration.md`
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- `docs/prompts/templates/wrappers/thin_wrapper_v0.md`
- `.agents/hooks/check_prompt_provenance.py`

Read first: `AGENTS.md`; `.agents/workflow-overlay/README.md`; the targeted
commissioning sections of `.agents/workflow-overlay/delegated-review-patch.md`;
then inspect the actual diff before forming findings.

Attack, coverage-first (report every issue found with severity and confidence;
adjudication filters, not you):
1. Default elision — can an omitted field be read two ways, or silently drop a
   trigger (formal verdict, doctrine change, couriered destinations)?
2. Constants-by-pointer — is any cut constant load-bearing at a point where the
   receiver cannot or will not resolve the pointer (e.g. the delegate lifecycle
   hard stop now cited, not inline)?
3. Single ownership — does deleting the defaults artifact's delta list orphan
   any field or contradict `source-loading.md`'s receipt shape?
4. Hook coherence — does the rewritten reminder text still match the doctrine
   core exactly; do the selftest pins still assert the right invariants?
5. Template operability — after the trims, can a receiver still execute the
   adversarial review template without re-deriving cut content wrongly?
6. Anything else in the diff that weakens a guard, fakes a success path, or
   drifts from the DCP receipt's claims.

Validation you must run and report honestly (fail and not-run are reportable):
- `python .agents/hooks/check_prompt_provenance.py --selftest`
- `python .agents/hooks/check_prompt_output_mode.py --selftest`
- `rg -n -i "six-field|Repo-constant fields may be referenced|REQUIRED ESCALATED DELTAS|6-item|state, per prompt" AGENTS.md CLAUDE.md .agents docs/prompts/templates docs/workflows/forseti_repo_map_v0.md` (expect zero hits)

Return in chat: findings (severity + confidence + file:line evidence), bounded
diff for any patch, validation evidence, verdict, residual risk. The
commissioning Chief Architect adjudicates before any returned change is kept;
`NEEDS_ARCHITECTURE_PASS` for design-level blockers. The `lifecycle_hard_stop`
constant applies to you verbatim.
