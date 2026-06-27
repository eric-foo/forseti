# Delegated Adversarial Artifact Review + Bounded Patch - YouTube Shorts Transcript Tone Rubric v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission under the provisional convention)
scope: >
  Controller prompt for a de-correlated adversarial artifact review with bounded
  patch authority on the YouTube Shorts transcript-only tone rubric. The hard-30
  fixture and first label run are supporting evidence, not patch targets.
use_when:
  - Executing this commissioned controller pass in a non-OpenAI-vendor lane with repo access.
  - Running the no-repo fallback source pack as advisory-only review when the reviewer cannot access the repo.
  - Adjudicating the returned diff, findings, or proposed edits before scaling the tone lane.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md
input_hashes:
  docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md: 20b273a36e3454c1e58e160357ae972d59cd9b4aa564f782364aa133465090c6
  docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.md: 510b1e166f40cba43c9ea70b8ea6d5698f5da129752b60aec638ae7399bbc3b3
  docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json: 8cdcea5ababf017c5431e7eab8a3c5f98dac4384f625ffbd81d9d1338373cce3
  docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md: b1c745ba77040342603c45cfc7f112663ffe58c7568741c7629160eb8fdc5c56
  docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json: 9bdfc7faeb699966926544b81b3102822700cca04cf720ff109152ee0bd81ee1
branch_or_commit: codex/youtube-shorts-tone-viability-prompt @ bfb87e24a8b871f653a7f628dbdab6a132889eee
no_repo_source_pack: docs/review-inputs/youtube_shorts_tone_rubric_delegated_review_source_pack_v0.zip
no_repo_source_pack_manifest: docs/review-inputs/youtube_shorts_tone_rubric_delegated_review_source_pack_manifest_v0.md
stale_if:
  - The target rubric hash changes before the run starts.
  - The hard-30 fixture or first label run changes before the run starts.
  - Home-model adjudication for this commission completes.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated here.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom delegated-review source pack for YouTube Shorts transcript tone rubric
  edit_permission: patch-only single target + review-report file-write
  target_scope: docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md only
  dirty_state_checked: required at run start
  blocked_if_missing: AGENTS.md, overlay README, delegated-review-patch convention, prompt-orchestration rules, review-lanes rules, target rubric, hard-30 fixture, label run
output_mode: review-report plus working-tree patch in repo mode; advisory paste-ready findings only in no-repo mode
template_kind: review
template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md plus delegated-review-patch convention
authorization_basis: current owner turn explicitly invoked workflow-delegated-review-patch for the YouTube Shorts tone lane
isolation_decision: existing isolated worktree C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-shorts-tone-viability-prompt
doctrine_change_decision: none intended; flag any necessary doctrine or architecture change instead of patching it here
```

## Commission

Explicit commission under the provisional Delegated Review-and-Patch convention.
Operating contract: `.agents/workflow-overlay/delegated-review-patch.md`. Access
mode defaults to `repo`. Mode: base-subagent.

Target, and the only file that may be patched in repo mode:

`docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md`

Why read-only review is insufficient: the rubric is the instrument that would be
used to scale from the hard-30 pilot into larger YouTube Shorts batches. The home
model authored the rubric and the first labels, so a self-consistent but brittle
taxonomy, false confidence rule, or transcript-only energy/prosody overclaim is a
correlated blind spot. A de-correlated combined review-and-patch pass can harden
the rubric before larger capture or labeling work relies on it.

Supporting evidence, read-only:

- `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json`

## Actor / Model-Family Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT (Codex based on GPT-5 authored the current rubric and label-run artifacts)
  controller_model_family: operator_to_fill; must be non-OpenAI vendor lineage for cross-vendor discovery
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: verify_at_run_start
```

This is a who-constraint, not a model recommendation. Vendor means upstream model
developer/provider, not hosting platform. If your lineage is OpenAI or is
unknown/undisclosed, stop before review and return
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. No tester/testee shortcut: you are the
controller; do not dispatch subagents or a replacement controller.

## Access Modes

Repo mode is the true delegated review-and-patch path. You inspect the pinned
worktree, patch only the target rubric, write the review report, and return an
uncommitted diff for home-model adjudication.

No-repo mode is explicitly weaker. If you receive only the source pack zip, you
must not claim patch authorship or return a repo diff. Run advisory-only review
over the included files, return findings plus exact proposed edits for the
target rubric, and state that the CA must apply accepted changes and run a
bounded post-patch re-review before anything is kept.

## Worktree Preflight For Repo Mode

- Workspace:
  `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-shorts-tone-viability-prompt`
- Branch: `codex/youtube-shorts-tone-viability-prompt`
- Expected baseline commit: `bfb87e24a8b871f653a7f628dbdab6a132889eee`
- Target file and hash: `docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md`
  at SHA256 `20b273a36e3454c1e58e160357ae972d59cd9b4aa564f782364aa133465090c6`
  over git blob bytes at the baseline commit.
- Dirty-state: clean at run start, except a later dispatcher may add this prompt
  artifact and expansion artifacts without changing the target/supporting hashes.
- Permitted writes: the target rubric and the report path below. No commit, no
  push, no staging, no branch operations.
- Any precondition failure returns a blocked result naming the failed check.

Report path:

`docs/review-outputs/adversarial-artifact-reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_v0.md`

## Source-Gated Method Contract

1. Authority reads: `AGENTS.md`; `.agents/workflow-overlay/README.md`;
   `.agents/workflow-overlay/source-of-truth.md`;
   `.agents/workflow-overlay/source-loading.md`;
   `.agents/workflow-overlay/review-lanes.md`;
   `.agents/workflow-overlay/prompt-orchestration.md`;
   `.agents/workflow-overlay/validation-gates.md`;
   `.agents/workflow-overlay/delegated-review-patch.md`.
2. REFERENCE-LOAD the review method before applying it:
   `docs/prompts/templates/review/adversarial_artifact_review_v0.md` and
   `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`.
   If `workflow-deep-thinking` and `workflow-adversarial-artifact-review` are
   available, invoke them in that order after source readiness. If unavailable,
   state advisory-only status and use a reasoning-before-findings pass instead;
   do not emit formal verdict, validation, readiness, or mandatory-remediation
   claims.
3. SOURCE-LOAD the bounded source set:
   - full target rubric;
   - hard-30 fixture MD and JSON;
   - first label-run MD and JSON;
   - this prompt, only to verify commission bounds.
   Default exclusions: raw data-lake transcript bodies, YouTube pages, audio,
   comments, engagement data, all unrelated review outputs, other prompts, and
   broader product history.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with named gaps.
5. Only after that declaration, APPLY the reasoning-before-findings pass,
   adversarial review checks, findings, and bounded patch.

## Fitness Reference

Goal: decide whether a transcript-only tone rubric is stable enough to use for
larger YouTube Shorts fragrance batches without laundering audio, visual, or
engagement signals into text labels.

Done looks like: the rubric forces repeatable coarse labels; carries abstention
and confidence rules; separates transcript-observable rhetorical posture from
audio energy/prosody, visuals, and comments; exposes caption/ASR source bias;
and prevents benchmark, buyer-proof, validation, or energy-score claims.

Attack the bar itself. If this goal or success signal is wrong, too weak, or too
easy to game, name that as a finding.

## Review Purpose

Be maximally adversarial within the commissioned target and purpose:

- Taxonomy repeatability: can two reviewers apply the mode labels without each
  inventing creator-specific micro-categories?
- Admission pressure: does the rubric define when short/noisy transcripts are
  labelable versus when they must abstain or stay low confidence?
- Transcript-only boundary: does any wording let the system infer energy,
  excitement, pace, volume, affect, visual tone, product authenticity, or
  engagement quality from words alone? Push hard here. Energy/prosody belongs to
  audio features captured alongside ASR, not to transcript-derived tone scores.
- Source-bias visibility: do manual captions, auto captions, ASR, no-speech
  videos, short transcripts, and creator catchphrases remain visible as
  uncertainty drivers?
- Scaling risk: would this rubric survive the next larger capture batch, or is it
  tuned too tightly to these 30 fragrance Shorts?
- Output discipline: does the rubric prevent claims of validation,
  inter-rater reliability, benchmark readiness, buyer proof, or commercial
  decision support?

## Bounded Patch Scope

Patch only `docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md`.
Apply the smallest complete patch for accepted findings. Do not patch fixture
JSON, label-run JSON, hard-30 summaries, source-capture code, overlay files,
data-lake files, prompts other than this target, or any protected path. If the
correct fix belongs outside the target, flag it with a closure condition.

Design-level problem -> return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert
any partial diff, and return findings only.

## Output Contract

Repo mode:

1. Write the durable report to
   `docs/review-outputs/adversarial-artifact-reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_v0.md`
   before chat summary. If the report cannot be written, return
   `FAILED_REVIEW_OUTPUT_WRITE` and do not claim a report path.
2. Report contents: compact `review_summary`; actor/model-family receipt;
   access mode; source readiness status; reasoning-before-findings pass;
   findings ordered critical, major, minor; each finding with location, issue,
   evidence, impact, `minimum_closure_condition`, `next_authorized_action`, and
   advisory remediation; unified diff or `no patch`; per-change neutral
   citations; verdict-as-decision-input; residual-risk note; provenance fields
   `authored_by` and `reviewed_by`; and non-claims.
3. Leave only the target rubric and report changed in the working tree. The
   home model adjudicates hunk by hunk before anything is kept.

No-repo mode:

1. Return findings plus exact proposed edits for the target rubric, not a repo
   diff and not a patch-authorship claim.
2. State the limitation: no-repo review preserves de-correlated review only, not
   de-correlated patch authorship. Accepted CA-applied edits require a bounded
   post-patch re-review before keep.

## Non-Claims

This commission is decision input only. It is not validation, readiness,
acceptance, benchmark proof, product proof, model routing, runtime-model
recommendation, or authorization to expand labels blindly. The delegate's diff,
findings, and verdict are claims to adjudicate, not premises to inherit.
