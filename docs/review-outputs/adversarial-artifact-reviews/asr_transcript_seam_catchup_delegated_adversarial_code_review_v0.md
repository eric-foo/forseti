# Delegated Adversarial Code Review + Adjudication — ASR Transcript Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review of the ASR transcript seam catch-up unit and the home-CA
  adjudication that closed it: one accepted major finding (F-ASR-001 — the
  record-id pre-check used the enveloped policy model while the written
  record's id used the transcriber's self-reported model, so a miswired
  transcriber could ack under the wrong policy), the kept patch, the CA's
  own in-landing fix for the touchpoint-inventory declarations the
  reviewer's expanded validation exposed, and the residuals carried forward.
use_when:
  - Checking what the ASR catch-up review found and how the F-ASR-001 keep decision was verified.
  - Citing the discharge of the independent-review gate for the commissioned six-file set.
  - Inheriting the F-ASR-001 convention (an injected engine's self-reported identity must be guarded against the enveloped policy before any durable write) and the validation lesson (tracked-scan gates must re-run after staging/committing new files).
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit aad28134746723c3e8b582c5784a13554e1aebbc; all six
    commissioned SHA256 pins matched by reviewer; patch applied in the
    worktree to five of the six patchable targets, verified by the CA)
  dispatch: docs/prompts/reviews/asr_transcript_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: one major finding, bounded patch, one off-scope validation failure surfaced, no NEEDS_ARCHITECTURE_PASS
  findings: 1
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. No live-lake or real-ASR run was performed by either party;
  behavior is proven on temp lakes with injected fake transcribers.
```

## Adjudication (claim → verification → decision)

**F-ASR-001 `[runner][yt-writer][ig-writer]` (major).** Claim: the runner's
record-id pre-check keyed on `transcriber_policy["model"]` while the
committed-packet writers derived record ids from the transcriber's
self-reported `model_info["model"]` — a miswired injected transcriber could
write a `large` transcript and have it acked under the `small` policy (the
obligation would claim a policy the engine did not run). This was the
commission's named IDENTITY-VS-POLICY COHERENCE stake. CA verification (not
inherited): confirmed against the pinned sources; traced the kept patch —
both writers now take `expected_model` and refuse on a record-ID mismatch
(comparing ids, not raw strings, so equivalent tokenizations cannot
false-positive) **before any write** (block-don't-burn preserved: no record,
no burned id, loud `derive_failed`); the runner passes the policy model and
additionally refuses to ack any derived record id differing from the
policy-expected id; YT+IG regressions pin both layers; the two writer pins
updated. The capture fusion passes no `expected_model`, so its behavior is
byte-unchanged. **Decision: ACCEPTED unmodified**, landed as commit
`648d085d`.

**CA verification of the return (fresh, not inherited):** `git status`
showed exactly five modified files, all inside the six-file patchable set
(+93/−3 matching the couriered summary); no commits or pushes were made by
the reviewer; and the CA's own fresh full-suite run over the patched
worktree (including the in-landing fix below): **2753 tests, 0 failures,
0 errors, 7 skipped**, JUnit-verified (`ORCA_DATA_ROOT` cleared).

**Reviewer-surfaced off-scope failure, fixed by the CA in this landing
(commit `cf66d35c`):** the expanded validation (producer seam +
A1 inventory gates) failed on the new runner's undeclared
`record_path`/`is_record_set_complete` lake touchpoints. Root cause is a
validation-sequencing gap on the CA side: the touchpoint scanners read
TRACKED source only, so the unit's pre-commit full-suite run could not see
the new runner; the gates first fired once it was committed. Both
touchpoints are now declared (seam-consumer read/completion checks — no new
write surface) and `lake_touchpoint_inventory_v0.json` regenerated via
`data_lake.inventory`. **Lesson carried forward:** any unit adding files
under tracked-scan-gated roots must re-run the tracked-scan gates AFTER
staging/committing, not only before.

**Class sweep:** the F-ASR-001 class (engine self-identity vs enveloped
policy) has no other current members — the ASR catch-up is the only seam
consumer whose obligation claims an injected engine's policy; the LLM
extract runners envelope `model` but also stamp it into their own record ids
from the same variable. Convention carried forward for any future
engine-injected lane: guard the engine's self-reported identity against the
enveloped policy before any durable write.

**Commissioned stakes with zero findings:** refactor byte-fidelity of both
capture paths (writer suites pin them); block-don't-burn completeness
elsewhere (the YT partial-set collision stays loud); downstream extract
re-surfacing; surface-gate completeness; reconcile fidelity; CLI/no-ASR-
import discipline; scope discipline. No NEEDS_ARCHITECTURE_PASS.

## Residual disposition

- Reviewer-stated residual (accepted): a crash inside ``append_record_set``
  after the member write but before the completion marker still requires
  operator cleanup (the packet then collides loudly as ``derive_failed``
  until cleaned). True crash-atomic record sets are lake write-boundary work
  outside this unit; carried to the census record with the existing
  ``partial_needs_cleanup`` class.
- The transcript record shapes still ride no schema version token
  (weak-envelope residual; pinned modules make changes deliberate).
- No live-lake or real faster-whisper execution evidence exists for this
  runner (standing; live runs are owner-operated cadence).

## Reviewer read-budget audit (as returned)

Full commission; pinned targets; seam contract, consumption/root helpers,
audio_asr engine, downstream extract runners, writer suites, prior
adjudication records; commissioned validation set run (in-scope: pass;
expanded: fails on the off-scope inventory declarations surfaced above);
`git diff --check` clean.
