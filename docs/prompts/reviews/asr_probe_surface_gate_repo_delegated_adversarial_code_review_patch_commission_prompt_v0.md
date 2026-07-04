# Repo-Mode Delegated Adversarial Code Review + Patch Commission — ASR Probe Surface Gate (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of a two-file micro-unit: the two
  YT probe surfaces (yt_shorts_channel_grid_probe_v0,
  yt_channel_rss_feed_probe_v0) join the ASR lane's YT
  known_out_of_scope_surfaces, plus the regression test. The special stake is
  SURFACE-GATE CORRECTNESS (F-FRAG-002/F-IGRC-002 class): a wrong
  out-of-scope classification silently acks packets that should be
  transcribed — attack the claim that these probe surfaces can never carry
  transcribable audio.
use_when:
  - Dispatching the commissioned probe-surface-gate review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/asr-surface-gate-probes` (lane head), pinned commit
  `af38e46c6f483ef9db0c82b1d60c7eb760274829`.
- Review target (the explicitly named multi-file set; the ONLY patchable
  surface; LF git blob bytes at the pinned commit):
  - `[asr-runner]` `orca-harness/runners/run_asr_transcript_catchup.py` — SHA256 `5adf8cae310623faf87a4709aa6145095bccb2bb92441624765f2af632e6a8cd`
  - `[asr-tests]` `orca-harness/tests/unit/test_asr_transcript_catchup.py` — SHA256 `b66682d0ef7260eb0afd262894fd12341ea10a56911710a3a2ddc9d2b9fcb614`
- Read-only / flag-only everywhere else — notably the capture writers for
  these surfaces (grep `yt_shorts_channel_grid_probe_v0` /
  `yt_channel_rss_feed_probe_v0` across `orca-harness/` to find their
  producers and confirm the surfaces never preserve audio bytes),
  `source_capture/transcript/{asr_packet,ig_reels_audio_packet}.py`,
  `data_lake/consumption.py`, and the prior adjudications (F-ASR-001,
  F-CAD-001, F-FRAG-002, F-IGRC-002 under
  `docs/review-outputs/adversarial-artifact-reviews/`).
- Access mode: `repo` — inspect the pinned source in place.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_asr_transcript_catchup.py
  orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
  orca-harness/tests/contract/test_policy_module_version_pins.py`
  (with `ORCA_DATA_ROOT` unset). Run if your runtime can; report real results
  either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Durable report written by the
  home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/asr_probe_surface_gate_delegated_adversarial_code_review_v0.md`.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"); home-CA adjudicates before anything is kept.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; targets pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/asr_probe_surface_gate_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/asr-surface-gate-probes; implementation committed at af38e46c)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by the artifact-folders overlay file and the in-repo commission pattern.
```

## Paste-ready commission body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT — gate yourself first: the review target was authored by an
Anthropic (Claude-family) model. This commission requires a DIFFERENT vendor /
model lineage (vendor = upstream model developer, not host/reseller/wrapper).
If you are Anthropic/Claude-lineage, or your lineage is unknown or
undisclosable, reply ONLY `BLOCKED_DECORRELATION` and stop. Who-constraint
only, never a model recommendation. State your model identity if permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/asr-surface-gate-probes, pinned commit af38e46c6f483ef9db0c82b1d60c7eb760274829
- REVIEW TARGET (review AND may patch — nothing else; label every finding):
  1. [asr-runner] orca-harness/runners/run_asr_transcript_catchup.py
     (SHA256 5adf8cae310623faf87a4709aa6145095bccb2bb92441624765f2af632e6a8cd)
  2. [asr-tests] orca-harness/tests/unit/test_asr_transcript_catchup.py
     (SHA256 b66682d0ef7260eb0afd262894fd12341ea10a56911710a3a2ddc9d2b9fcb614)
If you cannot open the repository, reply ONLY `BLOCKED_REPO_UNREADABLE`. If
you cannot see the pinned commit, review the branch head and state the commit
you actually read.

WHAT THE CHANGE IS: two surface tokens added to the YT family's
known_out_of_scope_surfaces in the ASR transcript catch-up (plus a
regression). Basis claimed by the author: the 2026-07-04 live drain left
exactly two packets pending as unsupported_surface
(01KWHV1Q2E48SS4A9QXGRR90B5 grid probe, 01KWHWAB07R3PG1WP0VHM1HP7A RSS
probe); both manifests declare media_modality_posture "media bytes out of
scope" (grid HTML/JSON; feed XML). Because the surface gate is fingerprinted
policy (F-IGRC-002), the change re-surfaces existing family acks once for a
compute-free re-ack.

The failure modes that matter most:
- SURFACE-GATE CORRECTNESS (the stake): from the capture writers in the
  pinned repo (find the producers of these two surfaces), can either surface
  EVER preserve transcribable audio bytes? If the surface definition is
  probe-versioned (…_probe_v0), what stops a future v1 with audio riding the
  SAME token? Is classifying by token alone honest here, per the
  F-FRAG-002/F-IGRC-002 conventions?
- ENVELOPE EFFECT: confirm the re-fingerprint consequence is stated truthfully
  and the re-ack path cannot double-ack or collide (ack_<fp> ids).
- TEST ADEQUACY: does the regression actually pin the new tokens (would a
  typo'd token fail it?); is the second-run-silent assertion meaningful?
- SCOPE DISCIPLINE: exactly two files; flag anything that should have
  required a different home (e.g. a shared surface registry) instead of
  patching it.

TASK: (1) structured reasoning pass over the two surfaces' producers and the
gate's failure lattice; (2) maximally adversarial review of the named set;
(3) bounded patch (unified diff in chat, labeled hunks) for accepted-quality
findings; run the named tests if you can and report real results.
Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only, NO diff.

RETURN, in order: review_summary YAML + labeled findings (severity /
file:line / issue / evidence / impact / minimum_closure_condition /
next_authorized_action); labeled unified diff with per-change citations;
verdict + residual-risk note (state explicitly whether an out-of-scope ack
this gate writes could cover transcribable audio); real test results or an
explicit not-run statement; one-line read-budget audit; adjudicator tail:
your output is claims to adjudicate — the CA may veto any change; nothing is
kept until home-CA adjudication.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a non-Anthropic lane with the GitHub repo readable (repo mode;
  cross-vendor discovery bar).
- On return, courier the full output back for review-return adjudication.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
