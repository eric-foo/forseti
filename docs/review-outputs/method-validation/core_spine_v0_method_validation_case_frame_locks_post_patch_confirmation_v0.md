# Core Spine v0 Method Validation Case-Frame Locks Post-Patch Confirmation

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Narrow post-patch confirmation of Core Spine v0 method-validation case-frame locks; checks AR-01 through AR-05 remediation, no new contamination, NEEDS_VERIFICATION propagation, replay authorization boundary, and replay artifact status.
use_when:
  - Deciding whether to accept the patched frame locks as input for replay authorization.
  - Checking whether the AR-01 through AR-05 patches hold without new drift.
  - Understanding the replay artifact boundary observation before downstream decisions.
authority_boundary: retrieval_only
open_next:
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md
input_hashes:
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: 4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785
prior_artifact_hash: B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md
stale_if: Target artifact hash changes, or the replay authorization boundary is separately resolved by owner decision.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_post_patch_confirmation_v0.md
  recommendation: accept
  summary: "All five AR patches confirmed applied and holding; no new contamination; NEEDS_VERIFICATION propagation correct; frame-lock artifact correctly denies replay authorization. Three replay artifacts exist in the workspace — they do not contaminate the frame-lock record, but replay authorization is not documented in any artifact; the Chief Architect should confirm whether a separate launch authorization was given or is still pending."
  findings_count: 1
  blocking_findings: []
  advisory_findings:
    - "OB-01: Three replay artifacts exist but no documented replay launch authorization is visible in the artifact record"
  prior_findings_remediated:
    - "AR-01: MV-09 why-not-obvious field now balanced; action-side plausibility stated alongside caution factors"
    - "AR-02: MV-05 outcome-comparison window now marked NEEDS_VERIFICATION with dependency note"
    - "AR-03: MV-03 and MV-05 reframe conditions generalized to move categories"
    - "AR-04: Section 10 now has explicit non-authorization sentence; verdict now CASE_FRAMES_ACCEPTED_REPLAY_AUTHORIZATION_NOT_GRANTED"
    - "AR-05: MV-01 exclusion rule now uses category language; Resolution Platform product name removed"
  next_action: "Accept patched frame locks; confirm or record replay launch authorization separately; replay artifacts are not to be treated as upstream inputs to the frame-lock record."
```

## Review Provenance

- Review type: narrow post-patch confirmation.
- Reviewed artifact: `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`.
- Prior review: `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md` — five advisory findings (AR-01 through AR-05) from the full rerun.
- Artifact hash at prior review: `B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537`.
- Artifact hash at this confirmation: `4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785`.
- Hash difference confirms patches were applied.
- Edit permission: read-only.
- Output mode: review-report.

## Source-Read Ledger

| Source | Status | Role in confirmation |
| --- | --- | --- |
| `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md` | untracked | Target artifact — confirmed against prior findings |
| `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md` | untracked | Replay artifact read to assess authorization boundary |
| `docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md` | untracked | Replay artifact read to assess authorization boundary |
| `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` | untracked | Replay artifact read to assess authorization boundary |

All sources are untracked. Used under dirty-state allowance per prior review-prompt terms.

## Scope

- Confirm AR-01 through AR-05 are remediated.
- Check no new outcome-shaped language was introduced by the patches.
- Check NEEDS_VERIFICATION propagation holds.
- Check evidence replay remains unauthorized in the frame-lock artifact.
- Check the untracked replay artifacts are not being treated as authorized inputs to the frame-lock record.

Excluded: full adversarial re-review, new finding development, patch execution, external source verification, pass/fail prediction, judgment of company decisions.

## AR Remediation Checks

### AR-01 — MV-09 positive-action frame bias

Finding: The "why later outcome was not obvious" field listed only caution factors, and the upgrade conditions required five concurrent criteria, creating structural bias toward caution in the portfolio's sole positive-action case.

Current text — why not obvious:
> "Legal AI had strong promise and plausible action-side pressure from incumbent content assets, practitioner workflow pain, visible AI capability, strategic timing, and legal-workflow distribution. It also carried unresolved accuracy, confidentiality, professional-duty, hallucination, workflow-fit, adoption, procurement, and integration risks. An incumbent could plausibly build, partner, acquire, wait, or limit exposure."

Current text — reliable-bet standard:
> "Upgrade to decisive capability capture or bounded `Move`..." (was "acquisition or bounded Move").

Current text — reframe conditions:
> "The move shifts from a single outcome path toward partner, license, build, acquire, test inside existing legal-workflow products, or target narrower legal workflows." (was "acquiring Casetext specifically to...").

Status: **REMEDIATED.** The why-not-obvious field now names action-side plausibility (incumbent content assets, practitioner workflow pain, visible AI capability, strategic timing, legal-workflow distribution) before listing caution factors. The reliable-bet standard no longer singles out acquisition. The reframe conditions are now expressed in terms of a neutral move category.

### AR-02 — MV-05 provisional cutoff dependency cascade

Finding: The outcome-comparison window (2023-06-01 through 2023-08-31) depended on the NEEDS_VERIFICATION provisional cutoff (2023-05-30) but was stated as fixed.

Current text — outcome-comparison window:
> "`NEEDS_VERIFICATION`; provisional window is 2023-06-01 through 2023-08-31 for immediate ecosystem response, with later corporate and data-licensing context allowed only as separate long-window calibration if the cutoff is verified before broad third-party-app fallout."

Current text — Section 10 MV-05 verification note:
> "Confirm the cleanest cutoff around 2023-05-30 and separate pre-cutoff API-dependence evidence from June 2023 protest evidence. If the cutoff cannot be pinned before broad third-party-app or moderator fallout, mark the case blocked or reframe the cutoff before replay."

Status: **REMEDIATED.** The outcome window now carries NEEDS_VERIFICATION and explicitly states the dependency. The Section 10 note names the block condition.

### AR-03 — MV-03 and MV-05 reframe conditions outcome-shaped

Finding: MV-03 named three specific Stack Overflow strategic paths; MV-05 listed five specific remediation paths. Both mirrored actual outcome trajectories.

Current MV-03 reframe:
> "The frame shifts from direct AI competition response toward knowledge quality, data-value capture, community governance, or workflow-positioning strategy."

Current MV-05 reframe:
> "The response shifts from broad API pricing toward segmented monetization, ecosystem protection, governance design, or staged rollout."

Status: **REMEDIATED.** Both fields are now move-category neutral. The MV-03 reframe no longer names "protect verified developer knowledge, license trusted data, and improve workflow retrieval." The MV-05 reframe no longer lists the five specific paths.

### AR-04 — Section 10 authorization drift

Finding: "Verification needs before evidence replay" framing could be read as a checklist where completion authorizes replay. Verdict used "awaiting" language creating sequencing pull.

Current Section 10 closing sentence:
> "Completing these verification steps does not itself authorize evidence replay; replay requires a separate later owner launch authorization."

Current Section 12 verdict:
> `CASE_FRAMES_ACCEPTED_REPLAY_AUTHORIZATION_NOT_GRANTED`

Status: **REMEDIATED.** The explicit non-authorization sentence is present. The verdict no longer uses pull language.

### AR-05 — MV-01 exclusion rule names a concrete post-window product

Finding: "Resolution Platform material" named a specific Zendesk product, embedding outcome knowledge in the exclusion rule.

Current MV-01 post-window exclusion:
> "Exclude post-cutoff Zendesk AI-agent, resolution-product, platform-restructuring, acquisition, packaging, comparison, or response-positioning material; post-cutoff Intercom/Fin repositioning, pricing, or integration changes; refreshed comparison pages; and forum/review material published or materially changed after cutoff from the at-cutoff recommendation."

Status: **REMEDIATED.** The specific product name is replaced with a category list. The same pattern applied to MV-05's post-window exclusion: "Apollo shutdown announcements" is now "third-party app shutdown announcements"; "IPO/data-licensing developments" is now "later corporate or data-licensing developments."

## New Contamination Check

No outcome-shaped language was introduced by the patches.

Items checked:

- MV-09 patched text introduces action-side plausibility language that is pre-cutoff plausible ("incumbent content assets, practitioner workflow pain, visible AI capability, strategic timing") and does not name the acquisition outcome.
- MV-05 outcome window now carries NEEDS_VERIFICATION without narrowing or specifying the window start in a way that biases replay.
- MV-03 and MV-05 reframe conditions are now more generic than before; no new specificity was introduced.
- MV-04 reframe conditions unchanged from prior patched version; no new contamination.
- MV-01 exclusion rule expansion (adding "packaging" and "response-positioning" to the category list) is appropriately generic.

## NEEDS_VERIFICATION Propagation Check

All five cases checked:

- MV-01: cutoff `NEEDS_VERIFICATION`; outcome window "exact source timing remains `NEEDS_VERIFICATION`." Dependency is flagged.
- MV-03: cutoff is exact (2023-07-26); "source-level visibility for second-order materials remains `NEEDS_VERIFICATION`." Appropriate.
- MV-04: "exact source visibility remains `NEEDS_VERIFICATION`." Appropriate.
- MV-05: cutoff `NEEDS_VERIFICATION`; outcome window now `NEEDS_VERIFICATION` with explicit dependency note. **AR-02 remediation confirmed.**
- MV-09: "exact source visibility remains `NEEDS_VERIFICATION`." Appropriate.

NEEDS_VERIFICATION propagation: **PASS.** No NEEDS_VERIFICATION field is treated as resolved elsewhere in the artifact. No downstream field inherits a NEEDS_VERIFICATION value while being stated as certain.

## Replay Authorization Boundary Check

Frame-lock artifact Section 1: "Evidence replay authorized: no."

Frame-lock artifact Section 12 verdict: `CASE_FRAMES_ACCEPTED_REPLAY_AUTHORIZATION_NOT_GRANTED`.

Frame-lock artifact Section 10: "Completing these verification steps does not itself authorize evidence replay; replay requires a separate later owner launch authorization."

Frame-lock artifact self-check: **PASS.** The frame-lock correctly states that replay is not authorized.

## OB-01 — Replay Artifacts Exist; Authorization Not Documented in Artifact Record

This is an observation, not a correctness finding against the frame-lock artifact.

Three replay artifacts are present in the workspace as untracked files:

- `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md` — status `REPLAY_COMPLETE`.
- `docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md` — status `REPLAY_COMPLETE`.
- `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md` — status `REPLAY_COMPLETE`.

Each replay artifact cites "accepted case-frame locks" as part of its source basis. The frame-lock artifact's Section 1 acceptance state says "Chief Architect accepted this frame-lock record in chat on 2026-05-21 after the FF-01 source-boundary patch; evidence replay still requires a separate launch authorization."

The frame-lock record does not contain a separate replay launch authorization. Whether that authorization was given in a subsequent chat turn is not visible in the artifact record.

Two things confirmed:

- The replay artifacts are not referenced by the frame-lock artifact. They do not contaminate the frame-lock record. The frame-lock's integrity is not compromised by their existence.
- The replay artifacts are outputs, not upstream inputs to the frame-lock. There is no circular reference or contamination path.

Documentation inconsistency noted:

The MV-01 replay artifact (Section 3, post-window exclusion rule) contains the pre-patch exclusion text naming "Resolution Platform material" rather than the patched category language. This indicates the MV-01 replay was executed against the pre-patch version of the frame-lock or captured the old exclusion text. It does not affect the patched frame-lock artifact but means the replay executor saw "Resolution Platform" named explicitly during that run.

What the Chief Architect should confirm or record:

- Whether a separate replay launch authorization was given in chat or elsewhere, and if so, whether it should be recorded in an artifact.
- If replay authorization was not separately given, the replay artifacts exist as unauthorized outputs and should be treated accordingly — as useful but not yet formally accepted method-validation products.

This does not block acceptance of the patched frame-lock record. It is a documentation and authorization-hygiene observation.

## Not-Proven Boundaries

- Public pre-cutoff source availability for any of the five cases is not proven; NEEDS_VERIFICATION items are unresolved.
- Whether replay authorization was separately granted is not proven from the artifact record.
- Whether the replay artifacts will be accepted as method-validation products is a Chief Architect decision.
- This confirmation does not accept, approve, or validate any replay artifact.

## Blockers

No blocking finding.

The five AR patches are applied correctly. No new contamination was introduced. NEEDS_VERIFICATION propagation is correct. The frame-lock artifact correctly states replay is not authorized.

## Next Authorized Step

Accept the patched frame-lock record at Chief Architect discretion.

If a replay launch authorization was separately given in chat, record it in an artifact or note it in the frame-lock acceptance state, so the replay artifacts have a traceable authorization chain.

If replay authorization has not yet been separately given, note the three replay artifacts as existing outside their authorized sequence; decide whether to accept them retroactively or treat them as pre-authorization drafts.

## Review-Use Boundary

This confirmation is decision input for the Chief Architect. It does not approve, accept, validate, or run the method-validation replay. It does not authorize source collection, source maps, data spine work, feature planning, implementation, staging, commit, push, or PR work.
