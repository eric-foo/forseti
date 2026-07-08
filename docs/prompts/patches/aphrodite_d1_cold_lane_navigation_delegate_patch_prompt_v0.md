# Aphrodite D-1 Cold-Lane Navigation Delegate Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact - bounded delegate patch prompt for Aphrodite D-1 research navigation and auditability.
scope: >
  Source-backed prompt for a repo-capable delegate to inspect and, only if needed,
  patch the live Aphrodite D-1 depth rehearsal bundle so a cold lane can find and
  audit the recipe, corpus, claims, adjudication record, and live fragrance
  reference without inventing missing outputs or promoting validation claims.
use_when:
  - Commissioning a bounded docs patch on the live Aphrodite D-1 cold-lane route.
  - Rechecking whether the recipe/corpus/claims route stayed navigable after artifact restoration.
  - Verifying that unplaced provenance/panel artifacts remain explicit blockers rather than fake live dependencies.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
stale_if:
  - The Aphrodite D-1 recipe, corpus, claims JSON, adjudication record, or fragrance reference is renamed or superseded.
  - Orca binds an accepted live destination for creator-signal product spines.
  - The delegated-review-patch or prompt-orchestration overlay changes the output-mode or patch-authority contract.
```

## Orca Prompt Preflight

- Output mode: `file-write` for this Orca prompt artifact at `docs/prompts/patches/aphrodite_d1_cold_lane_navigation_delegate_patch_prompt_v0.md`; a paste-ready copy may be couriered to the receiving delegate.
- Template kind: `patch`; no dedicated registered Orca patch template exists, so this uses the Orca prompt-orchestration contract plus existing project-local patch prompt shape. This is an ordinary multi-file prompt-orchestrated docs patch, not the provisional single-target delegated-review-and-patch convention.
- Edit permission / targets / branch: this prompt authoring lane is docs-write only. The receiving delegate may patch only the named live Aphrodite target files below, in the workspace it is explicitly given. Current observed authoring workspace was `C:/Users/vmon7/Desktop/projects/orca`, detached HEAD `63694997142f63b60b4e50c1bc687192df0a80fa`, dirty with unrelated pre-existing untracked files; the delegate must fresh-read its own `git status --short --branch` and must not revert unrelated work.
- Reviews: findings first if any issue is found. No formal verdict, readiness, validation, buyer-proof, or D-1 passage claim is bound by this prompt.
- Doctrine change: no doctrine change is requested. If the delegate concludes the fix requires creating or binding a new `orca/product/spines/creator_signal` destination, it must stop and return `OWNER_DECISION_REQUIRED`; do not mint that path in this patch.
- Destinations: this prompt is the input artifact. Delegate output is a chat/report-back patch summary plus observed validation output. If the delegate writes a durable report, the operator must fill an exact report path first.

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: prior_goal_completed
  changed_from_input: no
  lifecycle_status: complete_before_this_prompt
  if_changed_reason:
```

## Operator Fields

```yaml
delegate_identity: operator_to_fill
delegate_access: repo_preferred
report_destination: chat_return_unless_operator_fills_durable_path
de_correlation_claim: not_claimed
```

This is a bounded delegate patch prompt, not a claim that the provisional
delegated-review-and-patch convention has been fully commissioned. Do not claim
cross-vendor discovery or no-new-seam status from this run.

If the operator instead wants to use the provisional delegated-review-and-patch
convention strictly, stop and route out a new commission with a single named
target file, normally `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md`,
and treat README, corpus, claims, adjudication, and fragrance reference as
read-only sources unless separately bound.

## Objective

Inspect the live Aphrodite D-1 bundle and make the smallest complete docs patch,
only if the current files still fail cold-lane navigation or auditability.
At authoring time, no live navigation blocker was observed; this prompt is for
optional delegated hardening over a recent uncommitted multi-file repair, not a
claim that a patch is required.

Done means:

- A cold lane can reach recipe, corpus, and claims from `docs/research/README.md`
  without broad search.
- Every live Aphrodite `open_next` target outside `.codex/worktrees/` resolves
  with `Test-Path` from the workspace root.
- The claims JSON still binds to the corpus hash and recipe version.
- The recipe does not present unplaced provenance contract or panel design files
  as restored live dependencies.
- The live bundle stays explicitly evidence-lane / pre-output / incomplete where
  dependencies are unplaced.

If all checks already pass, do not churn wording. Return `no_patch_needed` with
the observed validation outputs.

## Required Source Loading

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `docs/research/README.md`
- `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`
- `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
- `orca/product/spines/foundation/ontology/fragrance_reference_v0.yaml`

If an expected live artifact is missing, inspect these worktrees only for missing
artifact recovery evidence, and treat them as candidate sources, not authority:

- `.codex/worktrees/aphrodite-d1-depth-rehearsal`
- `.codex/worktrees/aphrodite-creator-capture-strategy`
- `.codex/worktrees/aphrodite-human-supervised-browser-route`

For any worktree candidate you use, record branch, HEAD, dirty status, tracked
path evidence, and why it matches or does not match the live D-1 bundle.

## Source-Gated Method Contract

1. REFERENCE-LOAD the prompt and patch constraints above. Do not apply a patch yet.
2. SOURCE-LOAD the required live sources and any needed worktree candidates.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, assess the route defects and patch if needed.
5. Every load-bearing finding must cite `file:line` or the closest available path
   plus heading if line numbers are unavailable.

## Bounded Patch Scope

Editable only if needed:

- `docs/research/README.md`
- `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md`
- `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`
- `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md`
- `orca/product/spines/foundation/ontology/fragrance_reference_v0.yaml`

Allowed edits:

- Fix dead or stale `open_next` paths.
- Fix body text that falsely says a non-live artifact was restored.
- Repoint stale fragrance-reference paths from old `forseti/product/...` form to
  the accepted live `orca/product/spines/foundation/ontology/fragrance_reference_v0.yaml`
  path, if any remain.
- Add or tighten compact runbook/checklist text only when needed to preserve the
  cold-lane route or audit boundary.
- Restore a missing claims/adjudication/fragrance artifact only if exact matching
  evidence is verified from a named Aphrodite worktree and the live destination
  is accepted by Orca source hierarchy.

Forbidden edits:

- Do not invent or regenerate claim outputs.
- Do not change claim values, counts, receipts, model, timestamps, or hash fields
  except for path-reference repair that does not alter the claim substance.
- Do not claim validation, readiness, buyer proof, D-1 passage, commercial use,
  or truth proof.
- Do not create `orca/product/spines/creator_signal` unless an accepted Orca
  authority source already binds that destination in your fresh read.
- Do not bulk-edit unrelated research docs.
- Do not edit worktree files as the fix.
- Do not revert unrelated dirty work.

## Known Live State To Verify, Not Trust

At prompt authoring time, the live route had these source-backed signals:

- `docs/research/README.md` named the Aphrodite D-1 bundle route to recipe,
  corpus, and claims, and explicitly said evidence lane only, not
  validation/readiness/buyer proof.
- `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md` marked the
  bundle `RECIPE_V1_AUTHORED_FOR_D1_REHEARSAL_PRE_OUTPUT_LIVE_BUNDLE`.
- The recipe said the D-1 claims JSON, adjudication record, and fragrance
  reference were restored live.
- The recipe said the derived-claim provenance contract and vetting sprint panel
  design were verified in `.codex/worktrees/aphrodite-d1-depth-rehearsal/...`
  but not restored because live Orca had no accepted `orca/product/spines/creator_signal`
  destination.
- The corpus retained `F:/orca-data-lake/raw` only as an external local source
  boundary note, not as a repo-relative `open_next`.
- The fragrance reference used `orca/product/spines/foundation/ontology/...` for
  `naming_authority` and `ssot`.

Fresh-read those facts before relying on them.

## Required Validation

Run from the workspace root after any patch, or before returning `no_patch_needed`:

```powershell
$files = @(
  'docs\research\aphrodite_depth_rehearsal_extraction_recipe_v1.md',
  'docs\research\aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md',
  'docs\research\aphrodite_recipe_v1_second_opinion_adjudication_v0.md'
)
foreach ($file in $files) {
  $lines=Get-Content -LiteralPath $file
  $inBlock=$false
  foreach ($line in $lines) {
    if ($line -match '^open_next:\s*$') { $inBlock=$true; continue }
    if ($inBlock -and $line -match '^\S') { $inBlock=$false }
    if ($inBlock -and $line -match '^\s*-\s+(.+?)\s*$') {
      $target=$Matches[1]
      '{0} -> {1} :: {2}' -f $file,$target,(Test-Path -LiteralPath $target)
    }
  }
}
```

```powershell
Select-String -Path 'docs\research\README.md' -Pattern 'Aphrodite D-1 depth rehearsal bundle'
$targets=@(
  'docs\research\aphrodite_depth_rehearsal_extraction_recipe_v1.md',
  'docs\research\aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md',
  'docs\research\aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json'
)
foreach ($target in $targets) {
  '{0} :: {1}' -f $target,(Test-Path -LiteralPath $target)
}
```

```powershell
$corpus='docs\research\aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md'
$claimsPath='docs\research\aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json'
$corpusText=Get-Content -Raw -LiteralPath $corpus
$claims=Get-Content -Raw -LiteralPath $claimsPath | ConvertFrom-Json
$corpusHash=[regex]::Match($corpusText,'corpus_input_hash`: `([0-9a-f]+)`').Groups[1].Value
$recipeVersion='aphrodite-rehearsal-extraction-v1'
$pass=$claims.extraction_pass
$items=@($claims.claims)
$badHash=@($items | Where-Object { $_.input_content_hash -ne $corpusHash })
$badRecipe=@($items | Where-Object { $_.extraction_recipe_version -ne $recipeVersion })
'corpus_hash={0}' -f $corpusHash
'recipe_version={0}' -f $recipeVersion
'claims_top_input_content_hash={0}' -f $pass.input_content_hash
'claims_top_recipe_version={0}' -f $pass.extraction_recipe_version
'claim_count={0}' -f $items.Count
'claims_with_nonmatching_input_content_hash={0}' -f $badHash.Count
'claims_with_nonmatching_recipe_version={0}' -f $badRecipe.Count
'binding_ok={0}' -f (($pass.input_content_hash -eq $corpusHash) -and ($pass.extraction_recipe_version -eq $recipeVersion) -and ($badHash.Count -eq 0) -and ($badRecipe.Count -eq 0))
```

```powershell
rg -n "Restored at `forseti|retrieval `open_next` repointed|forseti/product/spines/foundation/ontology" docs\research\aphrodite_depth_rehearsal_extraction_recipe_v1.md docs\research\aphrodite_recipe_v1_second_opinion_adjudication_v0.md docs\research\aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md docs\research\aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
```

The last `rg` command should return no matches. An exit code of 1 from `rg`
with no output is acceptable and means no matches.

```powershell
git diff --check -- docs\research\README.md docs\research\aphrodite_depth_rehearsal_extraction_recipe_v1.md docs\research\aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md docs\research\aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json docs\research\aphrodite_recipe_v1_second_opinion_adjudication_v0.md orca\product\spines\foundation\ontology\fragrance_reference_v0.yaml
```

## Return Contract

Return findings first, then patch status:

```text
SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE:
- sources read:
- worktrees inspected:
- missing/unavailable sources:

Findings:
- [blocker|major|minor] <issue or no findings> - <file:line evidence> - minimum closure condition:

Patch:
- applied | no_patch_needed | proposed_only | blocked:
- files changed:
- diff summary:

Artifact status:
- claims JSON:
- adjudication record:
- provenance contract:
- panel design:
- fragrance reference:

Validation:
- open_next Test-Path output:
- cold route output:
- claims binding output:
- stale route scan output:

Remaining blockers:
- owner decisions needed:
- accepted residuals:

Non-claims:
- no validation/readiness/buyer-proof/D-1-passage claim
- no source promotion claim
- no runtime/model-routing claim
```

If blocked, stop with the nearest precise blocker:

- `SOURCE_CONTEXT_INCOMPLETE`
- `OWNER_DECISION_REQUIRED`
- `LIVE_DESTINATION_UNBOUND`
- `WORKTREE_CANDIDATE_NOT_VERIFIED`
- `PATCH_AUTHORITY_UNBOUND`
- `VALIDATION_FAILED`

## Dispatcher Notes

This prompt is intentionally conservative. The expected useful outcomes are
either a tiny docs-path/status repair or a `no_patch_needed` validation readout.
Do not turn this into a product-spine architecture decision, a claim extraction
rerun, or a broad Aphrodite research cleanup.

