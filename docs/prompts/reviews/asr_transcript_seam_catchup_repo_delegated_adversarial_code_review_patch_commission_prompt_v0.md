# Repo-Mode Delegated Adversarial Code Review + Patch Commission — ASR Transcript Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the ASR transcript seam
  catch-up unit: the two ASR writer refactors (capture-path behavior must be
  byte-identical) plus new committed-packet transcription paths, the
  two-family catch-up runner using the injected non-API local transcriber,
  its test suite, and two gate-membership updates. The special stakes are
  REFACTOR FIDELITY of the fused capture+transcribe writers and the
  BLOCK-DON'T-BURN divergence (the committed-packet path writes NO record on
  a failed transcription so the append-only model+audio record id is never
  burned — is that rule complete, and can any path still burn an id or ack a
  failure?).
use_when:
  - Dispatching the commissioned ASR catch-up review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/asr-transcript-seam-catchup` (lane head), pinned commit
  `aad28134746723c3e8b582c5784a13554e1aebbc`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[yt-writer]` `orca-harness/source_capture/transcript/asr_packet.py` — SHA256 `edcdc3c0ef80d5fa65f328014e108282e6faa9faeacc3a79f5880ea1bb46afac`
  - `[ig-writer]` `orca-harness/source_capture/transcript/ig_reels_audio_packet.py` — SHA256 `278de7a857b5e13afc703013c72c13c618469039798605f26ae9a93c14a8b509`
  - `[runner]` `orca-harness/runners/run_asr_transcript_catchup.py` — SHA256 `68e9be3f18c9e16cb2b41cdadeabb4d4df7a9361cae6c5b779a10016d5376ff9`
  - `[tests]` `orca-harness/tests/unit/test_asr_transcript_catchup.py` — SHA256 `4ec90e106ce525b4877bb45b733c471ea9342e03d096c5dea3b29c3e971397aa`
  - `[gate-consumer]` `orca-harness/tests/contract/test_catchup_runner_seam_coverage.py` — SHA256 `87d904b0ada19d333e69895ec891dff6a8613970f02eadcd787ffdf5dda6cb8c`
  - `[gate-pins]` `orca-harness/tests/contract/test_policy_module_version_pins.py` — SHA256 `b15312a6ef11baff112813aca420334f1ea0c3af7cae79412c7306a2c0a82fe4`
- Read-only / flag-only everywhere else — notably
  `orca-harness/source_capture/transcript/audio_asr.py` (the local
  faster-whisper engine + the defaults the CLI envelopes),
  `orca-harness/runners/run_{transcript,ig_reels}_product_extract.py` (the
  DOWNSTREAM consumers whose obligations enumerate per-packet transcript_asr
  record shas — a catch-up-written transcript must re-surface their work,
  never break it), `orca-harness/data_lake/consumption.py`,
  `orca-harness/data_lake/root.py` (append_record / append_record_set /
  is_record_set_complete semantics), the writer suites
  (`tests/unit/test_youtube_asr_packet.py`,
  `tests/unit/test_ig_reels_audio_packet.py` — the byte-identity pins for the
  refactor), the prior catch-up adjudications (F-ECR-001 / F-FRAG-001/002 /
  F-SH-001 / F-IGRC-001/002 conventions), and
  `orca-harness/data_lake/lane_registry.py`.
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_asr_transcript_catchup.py
  orca-harness/tests/unit/test_youtube_asr_packet.py
  orca-harness/tests/unit/test_ig_reels_audio_packet.py
  orca-harness/tests/unit/test_transcript_product_extractor.py
  orca-harness/tests/unit/test_ig_reels_product_extract.py
  orca-harness/tests/unit/test_extract_runner_reconcile_surfacing.py
  orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
  orca-harness/tests/contract/test_policy_module_version_pins.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the producer seam-coverage and inventory gate suites. Run them if your
  runtime can; report real results either way — never assert a pass that was
  not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/asr_transcript_seam_catchup_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch →
  home-CA adjudication (accept/modify/reject per change, class sweep +
  byte/scope checks) → keep decision. Repo-mode discovery discharges the
  independent-review gate for the patched set.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/asr_transcript_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/asr-transcript-seam-catchup; implementation committed at aad28134)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by artifact-folders overlay file and the in-repo commission pattern.
```

## Paste-ready commission body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT — gate yourself first: the review target was authored by an
Anthropic (Claude-family) model. This commission requires a DIFFERENT vendor /
model lineage (vendor = upstream model developer, not host/reseller/wrapper).
If you are Anthropic/Claude-lineage, or your lineage is unknown or
undisclosable, reply ONLY `BLOCKED_DECORRELATION` (plus your vendor if
permitted) and stop. Who-constraint only, never a model recommendation. State
your model identity and version in your output if known and permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/asr-transcript-seam-catchup, pinned commit aad28134746723c3e8b582c5784a13554e1aebbc
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [yt-writer] orca-harness/source_capture/transcript/asr_packet.py
     (SHA256 edcdc3c0ef80d5fa65f328014e108282e6faa9faeacc3a79f5880ea1bb46afac)
  2. [ig-writer] orca-harness/source_capture/transcript/ig_reels_audio_packet.py
     (SHA256 278de7a857b5e13afc703013c72c13c618469039798605f26ae9a93c14a8b509)
  3. [runner] orca-harness/runners/run_asr_transcript_catchup.py
     (SHA256 68e9be3f18c9e16cb2b41cdadeabb4d4df7a9361cae6c5b779a10016d5376ff9)
  4. [tests] orca-harness/tests/unit/test_asr_transcript_catchup.py
     (SHA256 4ec90e106ce525b4877bb45b733c471ea9342e03d096c5dea3b29c3e971397aa)
  5. [gate-consumer] orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
     (SHA256 87d904b0ada19d333e69895ec891dff6a8613970f02eadcd787ffdf5dda6cb8c)
  6. [gate-pins] orca-harness/tests/contract/test_policy_module_version_pins.py
     (SHA256 b15312a6ef11baff112813aca420334f1ea0c3af7cae79412c7306a2c0a82fe4)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the transcript_asr lane's seam catch-up. The ASR writers
fuse capture+transcription, so committed audio packets could exist without
transcripts (crash between packet and record; any non-fused commit path). The
unit (a) extracts each writer's inline transcribe+normalize+record block into
shared per-module halves — the capture path must be BYTE-IDENTICAL (record
key order, provenance merge order, record-set vs plain record, temp-file
prefixes all deliberately preserved per module) — and adds
transcribe_committed_*_audio_packet functions for existing anchors; (b) adds
one seam runner over BOTH audio families (youtube/youtube_audio,
instagram_creator/ig_reels_audio; ack namespace transcript_asr) with the
CLI-injected non-API faster-whisper policy enumerated in the obligation.
Done-ness keys on the ACK; record ids embed the model
(asr_<model_token>__<audio_sha16>), so a policy bump re-derives under a NEW
id; a pre-existing CURRENT-policy transcript is acked by citation
(same-policy crash/capture recovery, not old-policy satisfaction).
BLOCK-DON'T-BURN: the committed-packet path writes NO record on a failed
transcription (an environment failure must not permanently occupy the
append-only id); the capture fusion keeps recording failed postures because
each capture run mints a fresh packet.

The failure modes that matter most:
- REFACTOR FIDELITY: diff the extracted halves against the pre-refactor
  inline blocks (git history at the pinned commit's parent) — is ANY byte of
  the capture-path record different (key order, provenance merge order,
  ts/posture normalization, record-set membership, return strings)? Could
  the YT/IG writer suites pass while a subtle byte change slipped through?
- BLOCK-DON'T-BURN COMPLETENESS: can any path still burn a record id on
  failure (e.g. a raise AFTER _append_* starts; a partial record-set member
  without its marker) or ack a failed outcome? Is the YT partial-set case
  (member exists, marker missing) handled honestly (the existence pre-check
  returns None → the derivation attempt collides → loud derive_failed — is
  that collision guaranteed loud, and can it deadlock forever with no
  operator signal about WHY)?
- IDENTITY-VS-POLICY COHERENCE: the record-id pre-check uses
  transcriber_policy["model"], while the written record's id uses the
  transcriber's self-reported model_info["model"]. The CLI wires both from
  one argument — but an injected transcriber that reports a DIFFERENT model
  than the policy claims would desynchronize the pre-check from the written
  record. Real risk or acceptable coupling? (The obligation would also be
  claiming a policy the transcriber didn't run.)
- DOWNSTREAM RE-SURFACING: the YT/IG extract runners' obligations enumerate
  per-packet transcript_asr record shas — verify a catch-up-written
  transcript re-fingerprints their obligations (their acked packets
  re-surface to extract the new cues) and never breaks their record parsing.
- SURFACE-GATE COMPLETENESS: are the two families' known out-of-scope sets
  complete against the actual writers (youtube_captions / watch / rss; grid
  / deep-capture-audio / calls)? Deep-capture audio must stay off-seam
  (frozen decision) — is acking it out-of-scope in the transcript_asr
  namespace consistent with its own deep-capture transcript mechanism?
- ACK HONESTY (citation-based acks read back the real record), IDEMPOTENCE,
  PER-PACKET ISOLATION, RECONCILE FIDELITY, CLI/no-ASR-import discipline
  (--check must never load audio or the ASR library), TEST ADEQUACY, SCOPE
  DISCIPLINE.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
- orca-harness/data_lake/consumption.py + orca-harness/data_lake/root.py
  (append_record / append_record_set / is_record_set_complete; NOT patchable)
- orca-harness/source_capture/transcript/audio_asr.py (the engine + the
  defaults the CLI envelopes; NOT patchable)
- orca-harness/runners/run_transcript_product_extract.py +
  orca-harness/runners/run_ig_reels_product_extract.py (downstream consumers;
  NOT patchable)
- tests/unit/test_youtube_asr_packet.py + tests/unit/test_ig_reels_audio_packet.py
  (the refactor's byte-identity pins; NOT patchable)
- docs/review-outputs/adversarial-artifact-reviews/ (the F-ECR-001,
  F-FRAG-001/002, F-SH-001, F-IGRC-001/002 conventions; NOT patchable)
- orca-harness/data_lake/lane_registry.py (NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate both writers' pre/post-refactor
   record byte layout; the full failure lattice of the committed-packet path
   (transcriber raise, failed posture, append collision, partial set, ack
   failure); and the downstream extract runners' obligation response to a
   catch-up-written transcript.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding, along the failure modes above. Severity labels are
   finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY closing
   your accepted-quality findings; unified diff in chat, each hunk prefixed
   with its label; run the named tests if your runtime can and report real
   results. Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only,
   NO diff.

RETURN, in order: (1) review_summary YAML + findings (label / severity /
file:line / issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks labeled and annotated with findings + per-change
citations, neutral tone, decision-sufficient substance; (3) verdict +
residual-risk note — state explicitly whether any finding means acks this
runner would write are untrustworthy OR a capture-path byte changed OR a
record id can be burned by a transient failure; (4) real test results or an
explicit not-run statement; (5) one-line read-budget audit; (6) adjudicator
tail: your diff, citations, verdict, and test claims are claims to adjudicate
— accept/modify/reject per change; the CA may veto any change; nothing is
kept until that adjudication, which closes per the commissioning overlay's
Review Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable.
- On return, courier the full output back for review-return adjudication; the
  CA adjudicates per labeled change and lands kept hunks in the same
  adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
