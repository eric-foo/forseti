# No-Tools Execution Foundation F-01/F-02 Post-Patch Adversarial Recheck Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Bounded adversarial closure and blast-radius recheck for the F-01/F-02 no-tools execution foundation provenance/checklist patch.
use_when:
  - Launching the post-patch adversarial recheck for no-tools execution foundation F-01/F-02.
  - Verifying the receipt-provenance docs patch and no-case smoke-test checklist before any live smoke-test authorization.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/no_tools_execution_foundation_blind_spot_adversarial_review_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
```

## Paste-Ready Prompt

````text
You are performing a bounded adversarial closure/blast-radius recheck for the Orca no-tools execution foundation.

Repository: C:\Users\vmon7\Desktop\projects\orca
Expected branch: main
Expected HEAD: fe9444990e20774ffa2a7486f7eb5708b221d128

Required output mode: filesystem-output.
Required output path:
docs/review-outputs/no_tools_execution_foundation_f01_f02_post_patch_adversarial_recheck_v0.md

Review type: read-only adversarial recheck.
Do not patch files. Do not run live provider calls. Do not run models. Do not pass `--allow-live-provider-call`. Do not read API keys. Do not expose participant packets. Do not run a real probe, blind judgment, scoring, validation, fixture admission, ledger freeze, product proof, or judgment-quality proof.

If the output path already exists, stop with:

```yaml
review_summary:
  status: blocked
  reason: BLOCKED_OUTPUT_COLLISION
```

## Source-Gated Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read the overlay/review authorities listed below.
3. Verify all required source hashes exactly before declaring `SOURCE_CONTEXT_READY`.
4. If a file hash mismatches, stop before review and report the mismatch. If HEAD differs but all source hashes match, annotate the HEAD discrepancy and continue.
5. Apply `workflow-deep-thinking` first to frame closure and patch-caused regression risks.
6. Apply `workflow-adversarial-artifact-review` or equivalent read-only adversarial review posture to write the durable report.
7. Write the full report to `required_output_path`.
8. Fresh-read the report and compute its SHA-256 before returning chat closeout.

## Required Sources and Hashes

Authority:

```yaml
AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
.agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
.agents/workflow-overlay/source-of-truth.md: 57C9A6A457A80E0BB66771B3F1B67BD7994CEB9763F0D5D08076061A9921327A
.agents/workflow-overlay/review-lanes.md: 2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199
.agents/workflow-overlay/validation-gates.md: 2640638B8B8420B11951437A190B5578A8DACCB7B84583FC17A6808809628DE9
```

Prior review:

```yaml
docs/review-outputs/no_tools_execution_foundation_blind_spot_adversarial_review_v0.md: 9D426F7458653466CE262BC81DC0F178EC22E4F5DDCEFCEE5C523435D5BAF8E9
```

Patched targets:

```yaml
docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: F46AA6A4003E200C41796826277A6D8074ED84F26E6B6A5DD9E15584BE5EB0F5
docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 7A17255422C546858C54807161A265074FC0A5BD6739AFDE5592A51D94A8B26D
docs/research/judgment-spine/harness/v0_14/index.md: CB8499747F6BB034DC8A47DFE850298FF6D504CAFC8488E3431661A3E6172CEB
orca-harness/README.md: 9E5DA0BD36C1FB598F4EB582C098D0B2DA54C14E848E74F6AA48674D1BFBF94D
orca-harness/docs/v0_14/README.md: C32B8F544D72790FD6B5AA6A9C2C32803BF493D78865EE2C65FE6CAE79BA9CE0
```

Context source:

```yaml
docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61
```

## Review Commission

Determine whether the docs-only F-01/F-02 patch closes the two major findings from `no_tools_execution_foundation_blind_spot_adversarial_review_v0.md` without introducing any new blocker or major regression in the touched scope.

This is a smallest-complete bounded recheck. Do not reopen the full no-tools execution foundation review. Do not review unrelated dirty files. Do not create new minor/nit findings unless they directly prevent F-01/F-02 closure or create blocker/major risk in the touched patch scope.

## Frozen Prior Findings

### F-01

Prior finding: a `pass_valid` receipt recorded no execution provenance; non-live surfaces could mint a receipt indistinguishable from a genuine live raw-API one.

Minimum closure condition for this docs-only closure path:

- the controlling contract states that computed `pass_valid` / `proven` fields are not self-certifying live execution evidence;
- dry-runner, local fixture, manually normalized, and operator-authored receipts are not gate-clearing live execution evidence regardless of computed fields;
- no-case smoke-test receipts are permanently non-gate-clearing;
- gate-eligible live raw-API receipts require separate owner authorization and an out-of-band provenance record;
- the provenance record binds provider, endpoint URL, UTC timestamp, process exit status, full console output, `prompt_hash`, and `raw_response_hash` to the receipt.

### F-02

Prior finding: no operator artifact defined or governed a no-case smoke test.

Minimum closure condition:

- a single operator authorization/checklist exists under an Orca-owned harness v0.14 path;
- it states the purpose is plumbing-only, no real case, distinct from fresh-case probe and blind judgment;
- it defines a reserved synthetic `case_id` convention such as `SMOKE_NOCASE_`;
- it states smoke receipts are non-gate-clearing even if they compute `pass_valid`;
- it requires out-of-band provenance capture including provider, endpoint URL, UTC timestamp, process exit status, full console output, receipt hash, `prompt_hash`, and `raw_response_hash`;
- it states concrete authorization fields for provider/model/account or credential lane/endpoint/output path and one-shot scope;
- it carries non-claims and the required boundary `plumbing works only; not judgment quality`.

## Regression Surfaces

Check only blocker/major risk introduced or exposed by the patch in these surfaces:

- accidental live-call authorization;
- accidental real-case probe or blind judgment authorization;
- participant-packet exposure authorization;
- treating no-case smoke receipts as gate-clearing;
- contradicting the memorization probe protocol's existing gate semantics;
- stale or misleading v0.14 index/README navigation that could route an operator around the checklist;
- direction-change propagation omission for the new receipt-provenance rule;
- readiness, validation, fixture admission, scoring, ledger freeze, product proof, or judgment-quality overclaim.

## Expected Report Shape

The durable report must include:

- commission and scope;
- source context and hash verification;
- closure assessment for F-01 and F-02;
- patch-caused blocker/major regression assessment;
- recommendation: `accept`, `accept_with_friction`, `patch_before_acceptance`, or `blocked`;
- review-use boundary and non-claims.

After writing and verifying the report, return only a compact human summary plus this courier YAML:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/no_tools_execution_foundation_f01_f02_post_patch_adversarial_recheck_v0.md
  report_hash:
  recommendation:
  closed_findings:
    - F-01
    - F-02
  still_open_findings: []
  patch_caused_regressions: []
  next_action:
  non_claims:
    - no live provider call
    - no model call
    - no participant packet exposure
    - no real probe
    - no blind judgment
    - no scoring
    - no ledger freeze
    - no schema/runtime implementation
    - no validation
    - no fixture admission
    - no product proof
    - no judgment-quality claim
```

Required closeout line: plumbing works only; not judgment quality.
````
