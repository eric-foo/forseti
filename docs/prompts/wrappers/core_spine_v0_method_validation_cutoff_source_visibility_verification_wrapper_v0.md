# Core Spine v0 Method Validation Cutoff Source-Visibility Verification Wrapper

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Thin launch wrapper for the Core Spine v0 method-validation cutoff/source-visibility verification prompt.
use_when:
  - Launching the cutoff/source-visibility verification pass in a new thread.
  - Checking the exact prompt path, hash, workspace, and non-replay boundary for that pass.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/core_spine_v0_method_validation_cutoff_source_visibility_verification_prompt_v0.md
input_hashes:
  docs/prompts/product-planning/core_spine_v0_method_validation_cutoff_source_visibility_verification_prompt_v0.md: A51534E692BB2E3C9543241212B5E194F83EB9DB568180F68AE40A0E50C69A6D
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
stale_if: Full prompt hash changes, case-frame locks change, or evidence replay is authorized before verification runs.
```

Use the full prompt at:

`docs/prompts/product-planning/core_spine_v0_method_validation_cutoff_source_visibility_verification_prompt_v0.md`

Full prompt SHA256:

`A51534E692BB2E3C9543241212B5E194F83EB9DB568180F68AE40A0E50C69A6D`

Workspace:

`C:\Users\vmon7\Desktop\projects\orca`

Expected branch and HEAD at wrapper preparation:

`main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c`

Dirty state:

Allowed. Modified and untracked Orca docs, prompts, review outputs, and product artifacts may exist. Do not clean, revert, stage, commit, push, switch branches, or treat untracked replay artifacts as authorization.

Output mode:

`file-write`

Edit permission:

Docs-write only for the verification report named by the full prompt. No source-changing work is authorized outside that prompt contract.

Launch instruction:

Run the full prompt exactly as written. The task is cutoff/source-family visibility verification only. Do not run evidence replay, create evidence units, produce at-cutoff recommendations, create source maps or inventories, write case studies, plan features, plan implementation, stage, commit, push, or create a PR.

If the full prompt hash differs, the target workspace is unavailable, or the verifier cannot distinguish cutoff/source-family visibility verification from evidence replay, return a blocked result instead of substituting a different task.
