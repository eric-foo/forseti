# Contestant No-Tools Execution Contract Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review output - adversarial artifact review
scope: >
  Read-only adversarial review of the v0.14 contestant no-tools execution
  contract patch: new contract, memorization-probe protocol addendum, and v0.14
  index discoverability.
use_when:
  - Checking whether the no-tools contract can govern future contestant probe or blind-judgment gate semantics.
  - Deciding whether the docs-only patch preserves the Daimler probe-gate lesson without rescuing Daimler.
  - Auditing whether prompt-only no-search language is no longer enough for clean pass semantics.
authority_boundary: retrieval_only
output_mode: filesystem-output
required_output_path: docs/review-outputs/adversarial-artifact-reviews/contestant_no_tools_execution_contract_adversarial_artifact_review_v0.md
review_date: "2026-06-01"
branch_or_commit: main @ fb7f1a1cac09
reviewer: Codex GPT-5 coding agent
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_v0_14_no_tools_execution_contract_review
  edit_permission: review-report-write-only
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/research/judgment-spine/harness/v0_14/index.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

The workspace has pre-existing modified overlay files and an untracked
`docs/research/judgment-spine/harness/v0_14/` tree. This review relies on the
current repo-visible target files and reports that untracked state rather than
treating it as clean source authority.

Non-contestant exposure boundary: this review did not load the Daimler
participant packet, facilitator ledger, evidence registry body, source
manifests, or outcome/reveal material. The review target is the cross-cutting
execution-isolation contract and protocol patch, not a contestant packet.

## Sources Reviewed

| Source | Observed SHA256 | Use |
| --- | --- | --- |
| `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md` | `FBFC15CF97E648DB45A2F39B71EE8C0E7803CE49A136BA8C370645CCF0F3202C` | Primary contract target |
| `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md` | `2EE9CA52838D30A0C8424A3B02F9CBCDBE55A2F6FE87238D382A49ED4B65A20B` | Protocol addendum and artifact schema |
| `docs/research/judgment-spine/harness/v0_14/index.md` | `FAFEFA6224D538CD963553434A234A36A4D02F1679228153657D6C6451F6FEA8` | Discoverability and code-ready gate pointer |
| `docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md` | `2D4E2F304417759FA1EC143486327DF94F8E8FF06F6ABCEA4FC9734138632C93` | Source of tool-isolation failure mode |
| `docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md` | `4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693` | Confirmed Daimler remains closed and caveated |

## Review Method

`workflow-deep-thinking` discipline was applied before findings. The decisive
failure modes were:

- prompt-only "do not search" language still clearing a future pass;
- raw `probe_result: pass` bypassing execution isolation through an older case
  handling block;
- a fail with unproven isolation being cited as proof of training-data
  memorization;
- a tool-using run being treated as merely ambiguous instead of invalid;
- the imported-protocol header hiding a local Orca addendum;
- the contract becoming undiscoverable from the v0.14 index;
- the patch implying runtime hooks, probe authorization, validation, fixture
  admission, or judgment-quality proof.

`workflow-adversarial-artifact-review` mechanics were then applied to the
patched artifacts as a read-only review lane. No reviewed artifact was edited
during this review report write.

## Findings

No critical, major, or minor findings.

### Correctness Assessment

The patch closes the tool-isolation gap at the docs-contract level:

- `pass_valid` requires both `probe_result == pass` and
  `isolation_result == proven`.
- `fail_gate_closing_with_caveat` preserves the conservative gate-closing
  consequence for a fail when isolation is not proven, while explicitly
  blocking proof-of-memorization language.
- `execution_invalid_tool_violation` makes actual tool use invalid for clean
  contestant gate purposes.
- The protocol artifact schema now has a dedicated
  `contestant_execution_isolation` block with tool policy, tool configuration
  evidence, tool-call trace status, disabled-tool fields, hidden-context
  boundary, and normalized isolation result.
- The protocol's `Case Handling` block now states that raw `probe_result: pass`
  is not sufficient to make the contestant-case pair usable.

### Boundary Assessment

The patch preserves the current Daimler outcome. It does not rescue Daimler,
rerun Opus, reopen the selected-family gate, authorize a new target family,
authorize participant packet exposure, or convert the Opus Agent-harness result
into verified training-data memorization proof.

The protocol header now truthfully states that the file is an imported v0.14
spec with an Orca local execution-isolation addendum. This avoids the false
appearance that the patched protocol remains an untouched imported source.

The v0.14 index names the new contract in the Bridge Foundation table, reading
order, source-of-truth roles, and code-ready gate. The broader repo map already
routes Judgment Harness work to the v0.14 folder; not updating it for one
additional local harness file is acceptable because the v0.14 index is the
narrower navigation surface.

### Propagation Assessment

The new contract carries an inline `direction_change_propagation` receipt with
the correct trigger: `validation_philosophy`. It names the controlling harness
sources updated, the downstream surfaces checked, and the surfaces intentionally
not updated. The receipt does not claim validation, readiness, implementation
authorization, or fixture admission.

## Recommendation

```yaml
review_summary:
  status: completed
  recommendation: accept
  reviewed_targets:
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/research/judgment-spine/harness/v0_14/index.md
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_authorized_action: >
    Use the no-tools execution contract as docs-only gate doctrine for future
    contestant probe or blind-judgment execution planning. Runtime hook design,
    probe execution, model runs, scoring, validation, fixture admission, and
    judgment-quality claims still require separate authorization.
  non_claims:
    - no runtime hook implemented
    - no probe run
    - no probe pass
    - no blind-use authorization
    - no participant packet exposure
    - no model judgment run
    - no scoring
    - no ledger freeze
    - no schema/runtime implementation
    - no validation
    - no fixture admission
    - no judgment-quality claim
```

## Review-Use Boundary

These findings are decision input only. This review is not approval,
validation, mandatory remediation, runtime hook authority, probe execution
authority, fixture admission, or judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
