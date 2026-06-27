# YouTube-First Behavioral Completion Spec Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review output
scope: >
  Read-only adversarial artifact review of the YouTube-first behavioral
  completion spec (docs/workflows/youtube_first_behavioral_completion_spec_v0.md)
  at SHA256 77F0446C..09A14, before any YouTube implementation uses it as
  authority. Findings, non-findings, residual risk, and not-proven boundaries
  for whether the spec is a safe, smallest-complete behavioral contract that
  preserves the owner boundary "behavioral parity, not machinery parity".
use_when:
  - Deciding whether the YouTube-first behavioral completion spec is safe to route into implementation scoping.
  - Checking the spec's persistence/correlation contract, acceptance bar, IG-as-prompt boundary, and YouTube-strength preservation.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/youtube_first_behavioral_completion_spec_adversarial_artifact_review_prompt_v0.md
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
review_target: docs/workflows/youtube_first_behavioral_completion_spec_v0.md
review_target_sha256: 77F0446CE0E2197CD6BE9155CA591AB6D25FF9A5257EFFF6A4A4C3BE23609A14
branch_or_commit: codex/unify-capture-core-planning
stale_if:
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md changes from the hash above.
  - A named YouTube capture/transcript/persistence/extraction source in the source pack changes materially.
  - A later review supersedes this one, or the owner accepts/revises the spec's behavioral boundary or residuals.
```

## review_summary

```yaml
review_summary:
  status: completed
  commission: >
    Read-only adversarial artifact review of the YouTube-first behavioral
    completion spec before any YouTube implementation uses it as authority.
  review_target: docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  review_target_sha256_expected: 77F0446CE0E2197CD6BE9155CA591AB6D25FF9A5257EFFF6A4A4C3BE23609A14
  review_target_sha256_observed: 77f0446ce0e2197cd6be9155ca591ab6d25ff9a5257efff6a4a4c3be23609a14
  hash_match: true
  reviewed_by: anthropic/claude-opus-4-8 (Claude Code)
  authored_by: unrecorded
  authored_by_note: >
    Not operator-supplied for this review. The codex/ branch lineage and the
    parent planning note (authored in the codex worktree) suggest a non-Claude
    (GPT/Codex-family) author, but that is an inference from repo-visible
    convention, not a supplied identity; recorded as unrecorded, never
    fabricated. Same-vendor-vs-cross-vendor is therefore a visible measurement
    gap, not a captured measurement.
  de_correlation_bar: not_applicable
  de_correlation_note: >
    This is a standalone commissioned adversarial artifact review, not a
    workflow-delegated-review-patch commission; the two-bar de-correlation
    record is owned by that convention and is not bound here.
  recommendation: findings_are_decision_input_only
  findings_count: 6
  severity_set: [critical, major, minor]
  critical_findings: []
  major_findings: [AR-01, AR-02]
  minor_findings: [AR-03, AR-04, AR-05, AR-06]
  summary: >
    The spec is largely sound and well-grounded: it preserves all four named
    YouTube strengths (served-HTML metadata, caption-first transcript, youtubei
    comments, ASR fallback), uses IG as a behavioral prompt rather than a
    machinery template (the borrow / don't-borrow lists are accurate against the
    real IG code), normalizes output/persistence CONTRACTS rather than
    reintroducing shared ACQUISITION machinery, closes the current ambiguous
    comments-posture gap, and disclaims implementation/production/live-scale/
    legal/TikTok claims. Two MAJOR correctness gaps concentrate on the spec's
    central new deliverable -- durable persistence correlation: (AR-01) the
    per-video record unit collides with a one-video -> many-capture-packets
    persistence reality, and the spec never names the join key it already carries
    (platform_video_id) nor a which-transcript/aggregation rule; (AR-02) the
    acceptance set tests field PRESENCE, not correlation SOUNDNESS, and
    acceptance #5's disjunctive "safe lookup path" can be satisfied by the very
    human convention the PersistenceCorrelation section forbids -- a fake-pass
    seam on the deliverable the spec exists to protect. Four minors cover
    posture-enum semantics, an over-stated "four open links" framing, a
    cross-doc IG filename divergence, and slightly loose "fused ... may scope"
    wording. None is critical: the raw materials to close every gap are present
    in the spec, so these are completeness/precision defects in a
    pre-implementation contract, caught at exactly the review checkpoint the spec
    itself names. Findings are decision input only.
```

## Method And Readiness

- Method skills REFERENCE-LOADED then APPLIED in order, per the prompt and
  `.agents/workflow-overlay/review-lanes.md` / `prompt-orchestration.md`:
  `workflow-deep-thinking` (boundary framing, failure-mode and anti-anchoring
  discipline) and `workflow-adversarial-artifact-review` (two-phase
  correctness-then-friction flow, source-read-only boundary, finding schema).
- Deep-thinking discipline status: applied. The verification pass actively tried
  to defeat the "clean spec" reading by hunting for a *critical* (a guaranteed
  machinery-parity reintroduction or a guaranteed-wrong contract) and instead
  confirmed those failure modes are ruled out by source (see Non-Findings),
  relocating the real risk to persistence-correlation completeness and the
  acceptance bar. It also re-tested whether AR-01 is avoidable by an
  implementation choosing a per-capture-run unit -- it is not, because the spec
  itself fixes the unit at *per video/Short* (BehavioralCandidateRow; Acceptance
  #1), so the cardinality tension is spec-induced, not invented.
- `SOURCE_CONTEXT_READY`: declared after the review target and the full source
  pack were read. Not `SOURCE_CONTEXT_INCOMPLETE`.
- Trigger gate: explicit `workflow-adversarial-artifact-review` lane requested by
  the filed prompt. Pass.
- Lane-collision: the review target is a non-code workflow plan/spec. The named
  Python files are read as *comparison evidence* for the spec's behavioral
  claims, not reviewed for implementation correctness in this lane. No undeclared
  collision; no retarget.
- Output binding: `filesystem-output` with bound `required_output_path` (this
  file, the prompt's intended report path). Read-only on all reviewed source;
  this report is the only write. No `patch_queue_entry` emitted (read-only
  adversarial artifact review lane; the overlay forbids patch queues here).

## Source-Read Ledger

| Source | Why read | Decision it supports | State |
| --- | --- | --- | --- |
| `docs/workflows/youtube_first_behavioral_completion_spec_v0.md` | The review target | All findings | clean; hash recomputed = expected (`77f0446c..09a14`) |
| `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md` | Parent planning note (AO-A thin core); fitness/goal reference | AR-01, AR-04, NF-1, NF-2, NF-3 | clean (committed) |
| `orca-harness/youtube_capture/capture_youtube_v0.py` | Metadata + youtubei comment lane; persistence + posture reality | AR-01, AR-02, NF-3, NF-6 | clean |
| `orca-harness/youtube_capture/shorts_scroll_capture_v0.py` | Shorts volume lane; wall marker; posture reality | AR-01, NF-6 | clean |
| `orca-harness/source_capture/transcript/youtube_captions.py` | Caption-first acquisition; caption success/failure states | AR-03, NF-3 | clean |
| `orca-harness/source_capture/transcript/caption_packet.py` | Caption SourceCapturePacket; caption->ASR fallback contract | AR-01, AR-03, NF-3 | clean |
| `orca-harness/source_capture/transcript/asr_packet.py` | Audio packet + transcript_asr record set; per-run new packet | AR-01 (cardinality), AR-03 | clean |
| `orca-harness/runners/run_transcript_product_extract.py` | Caption+ASR normalization; extraction anchored on packet_id | AR-01, AR-04, NF-3 | clean |
| `orca-harness/source_capture/ig_reels_grid.py` | IG engagement/ranking-quality signal (ranking-basis-to-borrow) | AR-05, NF-2 | clean |
| `orca-harness/source_capture/ig_reels_deep_capture.py` | IG one-render-both-voices; partial-success preservation | NF-2 | clean |
| `orca-harness/source_capture/ig_reels_deep_capture_lake.py` | IG shortcode-anchored completion; transient-media redaction | NF-2 | clean |
| `.gitignore` (lines 41-42) | Confirm metadata/comment store is gitignored local output | AR-01, AR-02 | clean |
| `git check-ignore` / `grep` over `orca-harness` | Confirm no existing bridge correlates the metadata/comment store into the lake | AR-01, AR-02 | observed: no bridge |
| Overlay authority: `AGENTS.md`, `.agents/workflow-overlay/{README, source-loading, review-lanes, prompt-orchestration, artifact-roles, retrieval-metadata}.md` | Lane permission, severity set, finding schema, provenance fields, output binding | Whole-review authority | clean |

Authority handling: this is **advisory adversarial critique** from repo-visible
evidence. No strict artifact-role verdict, approval, validation, readiness,
acceptance, or mandatory-remediation claim is made. Severity labels
`critical | major | minor` are used as **finding-priority only**, per
`review-lanes.md`; they create no approval/rejection/readiness authority.

## Fitness Reference Used (alignment axis, not a pass bar)

Per `review-lanes.md`, this intent-bearing target is judged against a bound
fitness reference, which the reviewer also attacks:

- **Goal (pointer):** the prompt Objective + the parent planning note's
  Lane-First Exploration Strategy -- "make YouTube the first complete behavioral
  lane ... borrowing the useful IG behavioral wins ... [while YouTube] still
  use[s] served HTML, youtubei, captions-first transcript, and ASR fallback"
  (`shared_capture_core_ig_youtube_tiktok_planning_v0.md`, "Lane-First
  Exploration Strategy"), under the owner boundary *behavioral parity, not
  machinery parity*.
- **Observable success signal (pointer):** the spec's own Acceptance Criteria
  (#1-#8).
- **Attacking the reference itself:** the goal is sound and the success signal
  mostly operationalizes it. The signal's weak spot is that it tests presence of
  fields rather than soundness of the correlation it most needs to guarantee
  (AR-02). The fitness reference is *present but only informally bound* -- the
  spec does not cite a `work_unit_fitness_reference_v0` object -- which is
  adequate here (a checkable success bar exists), so this is **not** a
  `no checkable success bar bound` gap; it is noted for hygiene only.

---

## Phase 1 -- Correctness Findings

### AR-01 -- major -- Per-video record unit collides with one-to-many capture persistence; correlation key and aggregation rule unspecified

- phase: correctness
- target / role: YouTube-first behavioral completion spec (Workflow plan), sections **Interfaces / Contracts -> PersistenceCorrelation**, **BehavioralCandidateRow**, **Acceptance Criteria #1**.
- source authority: the spec; `asr_packet.py`; `caption_packet.py`; `run_transcript_product_extract.py`.
- artifact evidence: the spec fixes the record unit at the *video*: "For each captured YouTube video or Short, the lane must be able to express ..." and Acceptance #1 "A YouTube video or Short has **one behavioral record** tying candidate identity, metadata, comments posture, transcript source, persistence anchors, and extraction status together." PersistenceCorrelation requires correlating "metadata/comment capture output; caption packet or audio packet; transcript derived record; product-extraction record set" and "must not leave these surfaces discoverable only by human convention," but names no join key and no cardinality rule.
- code reality: persistence is **per capture packet, one video -> many packets**. `asr_packet.py:175-179` (and its inline note) mints a **new** audio packet per run ("each run mints a NEW audio packet (fresh packet_id), so a normal rerun is a new observation"); `caption_packet.py` stages a fresh caption packet per call; a single video can carry **both** a caption transcript and an ASR transcript (`run_transcript_product_extract.py:108-122` normalizes both `youtube_captions` and `youtube_audio` surfaces for the same video). Extraction is anchored per packet (`transcript_anchor` = packet_id, `:151-167`), not per video.
- strongest defense, and why it fails: *"A spec should leave the mechanism open; the implementation can pick the anchor."* It fails because the spec does not leave a free mechanism choice -- it has already fixed the **unit** (per video) and the **constraint** (no human convention) while omitting the one fact that makes a per-video record well-defined over a one-to-many store: which key joins the surfaces (`platform_video_id`, which the spec already carries in both `BehavioralCandidateRow` and `TranscriptSource`) and how a video with multiple/again-captured transcripts collapses into "one behavioral record." That is a contract-completeness fact, not acquisition machinery, so naming it does not violate the spec's own machinery-parity boundary.
- requirement strained: "smallest *complete*" contract; PersistenceCorrelation's own "not discoverable only by human convention" guarantee.
- impact: implementation scoping must either re-derive the join key and the
  per-video aggregation rule (re-opening intent the Downstream Handoff says it
  may rely on without reopening), or guess -- risking a per-run record that
  silently fails Acceptance #1's "one behavioral record per video," or a
  video-keyed record that mis-joins when caption and ASR packets disagree. This
  is exactly the "bad contract shapes persistence/tests" risk the spec's own
  Review Checkpoint names.
- minimum_closure_condition: the spec names the correlation anchor
  (`platform_video_id`) as the required join key for the per-video behavioral
  record, and states the cardinality/selection rule for the one-video ->
  many-packets case (e.g., how multiple transcript packets, and caption-vs-ASR
  for the same video, resolve into the single behavioral record), so a scoper
  can build the record unit without re-deciding intent.
- next_authorized_action: owner/author decision to amend the spec's
  PersistenceCorrelation + Acceptance #1 wording; or owner acceptance of the gap
  as a named, scoping-time decision. No patch authority is created by this
  finding.
- patch_queue_entry authorized: no (read-only adversarial artifact review lane).
- verification / red-green: not_applicable (non-executable contract finding; no
  same-check test exists or is required).
- not proven: that any specific anchor or aggregation rule is "correct" -- this
  finding asserts the *gap*, not a chosen resolution.

### AR-02 -- major -- Acceptance criteria test field presence, not correlation soundness; #5's "safe lookup path" can be satisfied by the human convention the spec forbids

- phase: correctness
- target / role: spec sections **Acceptance Criteria #1 and #5** vs **Interfaces / Contracts -> PersistenceCorrelation**.
- source authority: the spec (internal consistency); `capture_youtube_v0.py:206-211`; `.gitignore:41-42`; `grep`/`check-ignore` over `orca-harness`.
- artifact evidence: PersistenceCorrelation states the surfaces "must not leave these surfaces discoverable only by human convention." Acceptance #5 accepts as complete: "Metadata/comment legacy packets are **either** bridged into the correlation contract **or** explicitly kept as a named residual **with a safe lookup path**." Acceptance #1 requires the surfaces be "tied together" but defines no integrity/verifiability check on the tie.
- code reality: the metadata/comment store is a separate world -- `capture_youtube_v0.py:206-211` writes plain `packet.json` to `./packets/<video_id>/` (no `SourceCapturePacket`/`DataLakeRoot`; confirmed: neither metadata/comment file imports those rails), the path is gitignored (`.gitignore:41-42`), and **no code bridges it into the packet-anchored transcript/extraction lake** (grep over `orca-harness` finds only `shorts_scroll_capture_v0.py` referencing its own output dir). So "discoverable only by human convention" is precisely the *current* state the spec must move off of.
- strongest defense, and why it fails: *"#5's escape hatch is the intended MGT residual -- bridge-not-migrate is explicitly accepted."* It fails on the **wording**, not the residual: a "safe lookup path" that is a documented *manual* procedure ("operator looks in `packets/<video_id>/`") is human convention, which PersistenceCorrelation forbids -- so #5 as written can be read to *accept* what the section *forbids*. An implementation could pass Acceptance #5 (and, because #1 tests only that fields are present, pass #1 too) while leaving the correlation unsound. The deliverable the spec exists to protect is the one place its acceptance bar is weakest.
- requirement strained: real-failure-visibility / no fake-success path; internal consistency between the contract section and its acceptance bar.
- impact: a fake-pass seam on the central deliverable -- "complete" can be claimed at scoping/closeout with a human-convention lookup, defeating the spec's purpose and re-importing the discoverability problem the spec was written to end.
- minimum_closure_condition: #5's "safe lookup path" is constrained to a
  *programmatic/deterministic* lookup (an index, bridge record, or
  packet/lake normalization -- not a manual procedure), reconciling it with
  PersistenceCorrelation; and the acceptance set gains a check that the
  correlation **resolves** (the persistence anchor for a video deterministically
  reaches that video's transcript + extraction), not merely that the fields are
  present.
- next_authorized_action: owner/author decision to tighten Acceptance #5 and add
  a correlation-soundness criterion; or owner acceptance of the residual with
  the human-convention reading explicitly disallowed.
- patch_queue_entry authorized: no.
- verification / red-green: not_applicable (non-executable acceptance-bar
  wording finding).
- not proven: that any implementation has yet exploited the seam -- this is a
  contract defect, not an observed failure.

### AR-03 -- minor -- TranscriptSource posture enum has no caption-specific success state; "transcribed" is ASR-flavored

- phase: correctness
- target / role: spec **Interfaces / Contracts -> TranscriptSource** (`posture`).
- source authority: the spec; `youtube_captions.py:136-184`; `asr_packet.py:154-165`.
- artifact evidence: TranscriptSource `posture: transcribed | no_caption_track | invalid_caption | download_failed | no_speech | failed` is one union over caption and ASR, with `source_kind: caption | asr` carried separately. The only *success* value is `transcribed`.
- code reality: ASR success is literally `transcribed` (`asr_packet.py:164`), but caption success is `found=True` / `note="ok"` (`youtube_captions.py:182-184`) -- a manual/auto caption is *provided by YouTube*, not transcribed. The failure states split cleanly by source (caption: `no_caption_track`/`invalid_caption`/`download_failed`; ASR: `no_speech`), but the success state does not.
- strongest defense, and why it fails: *"the spec says 'or a narrower compatible enum,' so implementers can adapt."* Partly holds -- which is why this is minor, not major -- but the normalization of caption-vs-ASR posture is exactly what `TranscriptSource` is responsible for; leaving "what posture does a found manual caption carry?" unstated invites two implementers to diverge (one writes `transcribed` for captions, another invents `caption_ok`), defeating the single-shape goal of Acceptance #2.
- requirement strained: Acceptance #2 ("both normalize into the **same** TranscriptSource contract").
- impact: cross-source posture drift; a minor but real normalization ambiguity in the contract's success path.
- minimum_closure_condition: the spec states the caption success posture
  explicitly -- either a caption-success value, or an explicit statement that
  `transcribed` means "usable cues available regardless of source_kind."
- next_authorized_action: owner/author wording amendment; or accept as a
  scoping-time micro-decision.
- patch_queue_entry authorized: no.
- verification / red-green: not_applicable.
- not proven: nothing strict claimed.

### AR-04 -- minor -- PersistenceCorrelation framing overstates the open work: three of the four links already exist via packet anchoring

- phase: correctness
- target / role: spec **PersistenceCorrelation** (the four-surface list).
- source authority: `run_transcript_product_extract.py:108-122, 151-167`; `asr_packet.py:185-191`; `caption_packet.py:97-141`; planning note "YouTube" + "Shared Versus Platform-Owned" sections.
- artifact evidence: PersistenceCorrelation lists four surfaces to correlate as if all four ties are open work.
- code reality: caption packet -> transcript (the json3 is a PreservedFile *inside* the caption packet) and audio packet -> transcript derived record (`derived/<audio_packet_id>/transcript_asr/`, `asr_packet.py:185-191`) and transcript -> extraction (`transcript_anchor` = packet_id drives the mentions record set, `run_transcript_product_extract.py:151-167`) **already exist** via packet-id anchoring. The genuinely-missing link is **metadata/comment store <-> transcript/lake**, because only that store is non-packet-shaped and gitignored (AR-01/AR-02 evidence). The planning note already says as much ("YouTube comments ... not yet normalized into the same SourceCapturePacket/DataLake shape"; "YouTube metadata/comment capture is not yet SourceCapturePacket/DataLakeRoot shaped").
- strongest defense, and why it fails: *"listing all four is harmless completeness."* It is *mostly* harmless -- hence minor -- but it obscures where the real effort is, and a scoper could over-estimate the persistence work (re-anchoring links that already hold) or under-focus the single outlier. Precision here directly de-risks AR-01.
- requirement strained: "smallest" (avoid implying re-work of already-correlated surfaces); accuracy of the current-state claim.
- impact: mild scoping mis-estimation; reduced focus on the one outlier link.
- minimum_closure_condition: PersistenceCorrelation distinguishes the
  already-existing packet-anchored links from the one genuinely-missing
  metadata/comment bridge.
- next_authorized_action: owner/author wording amendment; or accept as-is given
  Acceptance #5 + MGT residual #3 already single out the metadata/comment bridge.
- patch_queue_entry authorized: no.
- verification / red-green: not_applicable.
- not proven: nothing strict claimed.

### AR-06 -- minor -- "fused ... may scope" wording is loose against the spec's own implementation-authority disclaimer

- phase: correctness (boundary control)
- target / role: spec **Status** ("fused-safe one-shot slice") and **Downstream Handoff** ("one fused implementation pass may scope YouTube behavioral completion only").
- source authority: the spec (internal consistency); `AGENTS.md` (implementation requires explicit bounded authorization); `.agents/workflow-overlay/source-loading.md` Current Operating Boundary.
- artifact evidence: Status says the spec "does not cover, authorize, or imply implementation," Non-Goals and Acceptance #8 disclaim readiness/validation, yet Downstream Handoff phrases the next step as "one **fused implementation pass** may scope ... only."
- strongest defense, and why it fails: *"'may scope ... only' clearly bounds it to scoping."* Largely holds -- which keeps this minor -- but "fused implementation pass" names a lane (`fused`) that runs scoping -> spec -> lock -> *implementation* in one turn; a reader skimming Downstream Handoff in isolation could treat the fused implementation as pre-blessed, against the Status disclaimer and AGENTS.md's explicit-authorization rule.
- requirement strained: real boundary visibility; consistency with the spec's own non-authorization stance.
- impact: small authority-clarity risk at the handoff seam; low because three other sections disclaim it.
- minimum_closure_condition: the handoff wording separates "scope (read-only)"
  from "implement (separately authorized)" so the fused lane's scoping entry is
  not read as implementation pre-authorization.
- next_authorized_action: owner/author wording amendment; or accept given the
  surrounding disclaimers.
- patch_queue_entry authorized: no.
- verification / red-green: not_applicable.
- not proven: no claim that the spec *does* authorize implementation -- it does
  not; this is wording-hardening only.

---

## Phase 2 -- Friction Findings

### AR-05 -- minor -- Cross-document IG source divergence: spec cites `ig_reels_grid.py`, parent note cites `ig_reels_grid_capture.py`; both exist as distinct surfaces

- phase: friction
- target / role: spec **open_next** / source pack (`ig_reels_grid.py`) vs parent planning note **open_next** / Current Pipeline Map (`ig_reels_grid_capture.py`).
- source authority: `ls orca-harness/source_capture/` (both files present); `ig_reels_grid.py` engagement enums; planning note Current Pipeline Map.
- artifact evidence: the spec's open_next and the review source pack name `orca-harness/source_capture/ig_reels_grid.py`; the parent planning note (reachable from the spec's open_next) names `ig_reels_grid_capture.py` for the same "IG grid" role. Both files exist and are distinct: `ig_reels_grid.py` is the engagement/ranking-quality **parser** (`DOM_GRID_ENGAGEMENT`, `hidden_engagement_candidates`, view-count precedence, ranking-quality enums) and `ig_reels_grid_capture.py` is the render/enumeration **capture** path (planning note: "renders a creator /reels/ grid ... extracts DOM rows plus passive JSON candidates").
- strongest defense, and why it fails: *"the spec picked the more relevant file -- the ranking-signal parser grounds the 'borrow explicit ranking basis' win better than the render path."* That defense actually *holds* on the choice (the spec's citation is the better one for ranking-basis), so the finding is not "wrong file" -- it is that a scoper following open_next across both the spec and its parent note meets two different "IG grid" files with no disambiguation and may conflate them or assume one is a typo.
- requirement strained: retrieval hygiene / cross-artifact navigability.
- impact: minor reader confusion at scoping; risk of opening the wrong IG surface.
- minimum_closure_condition: the spec (or its parent note) adds a one-line
  disambiguation of which IG grid surface it cites and why (ranking-signal parser
  vs render/enumeration).
- next_authorized_action: owner/author one-line hygiene amendment; non-blocking.
- patch_queue_entry authorized: no.
- verification / red-green: not_applicable.
- not proven: nothing strict claimed.

---

## Non-Findings (ruling out plausible material failures from the prompt's review axes)

These are recorded because each is a *plausible* material failure the prompt
asked to attack, and each was checked against source and **did not** hold.

- **NF-1 -- Axis 1 (machinery parity reintroduced under behavioral-parity
  language): ruled out.** The spec's Interfaces are output/persistence/transcript
  **contracts** (shapes to express), which the planning note already lists as
  "Already shared or directly reusable" rails (writer/lake, transcript cue input,
  ASR machinery, extraction). Non-Goals explicitly forbid the *acquisition*
  machinery that would be parity: "Do not introduce a shared scheduler,
  producer/consumer framework, or unified acquisition engine." No
  machinery-parity reintroduction found.
- **NF-2 -- Axis 3 (copies IG mechanics instead of using IG as a prompt): ruled
  out.** The "Borrow ... / Do not borrow" lists are accurate against real IG
  code: partial-success preservation (`ig_reels_deep_capture.py:213-223` returns
  comments even when the audio/transcript leg fails), transient-media labeling
  (`ig_reels_deep_capture_lake.py:45-51, 53-98` redacts the signed handle, keeps
  host + used-flag), shortcode-anchored completion (`:31-42`, the don't-borrow
  default), and the engagement ranking-quality signal to borrow as a *prompt*
  (`ig_reels_grid.py` enums). The spec borrows behavior, not mechanics.
- **NF-3 -- Axis 8 (YouTube-specific strengths preserved): ruled out as a
  failure.** All four are named in Required Behavior and confirmed in code:
  served-HTML metadata (`capture_youtube_v0.py:147-183`,
  `ytInitialPlayerResponse`/`ytInitialData`), caption-first transcript
  (`youtube_captions.py:136-151`, manual>auto>original-language), youtubei comment
  route (`capture_youtube_v0.py:97-101, 184-205`), ASR fallback
  (`caption_packet.py:49-50` -> `asr_packet.py`).
- **NF-4 -- Axis 7 (leaks implementation/production/live-scale/legal/TikTok
  authorization): ruled out (one minor wording soft-spot = AR-06).** Status,
  Non-Goals, Acceptance #8, and the MGT residuals disclaim all of these. The only
  soft spot is the "fused ... may scope" phrasing (AR-06), which does not itself
  authorize implementation.
- **NF-5 -- Axis 6 (MGT residuals silently drop a material slice / lack upgrade
  triggers / hide risk): ruled out as written.** All five residuals carry
  explicit upgrade triggers (weak ranking, bounded comment sample, bridge-not-
  migrate, no shared scheduler, deferred IG/TikTok). Caveat, not a separate
  finding: none of the residuals names the *correlation-cardinality* risk -- that
  gap lives in the contract body and is captured by AR-01, not by the residual
  list.
- **NF-6 -- Axis 4 partial (comments behavior left vague / fake-pass-prone):
  ruled out for posture.** The spec's `comments_posture`
  (`captured | disabled | empty | blocked | failed | not_attempted`) and the
  CommentSet states *add* `blocked | failed | not_attempted`, which closes the
  current reachable ambiguity in code where `comments_posture` stays `None` when a
  comment token is present but the innertube key/version is missing
  (`capture_youtube_v0.py:169, 185-205`) or when a wall is hit
  (`shorts_scroll_capture_v0.py:42-52`). This is the spec doing its job, not a
  defect. (The broader Axis-4 acceptance-bar weakness is AR-02.)

## Residual Risk

- The two MAJOR findings (AR-01, AR-02) both concentrate on persistence
  correlation -- the spec's central new deliverable. If they are not closed
  before scoping, the most likely failure is a persistence/record shape that
  passes the current acceptance bar yet does not durably or verifiably correlate
  metadata/comments to the transcript/extraction for a given video. They are
  *completeness* defects, not contradictions that make the contract unusable: a
  scoper who reads the code (as this review did) can close them, but the spec's
  Downstream Handoff invites reliance "without reopening intent," so leaving them
  open shifts that intent decision into scoping unannounced.
- This review is **advisory critique from repo-visible evidence**. It is **not**
  approval, validation, readiness, acceptance, alignment-completion, or mandatory
  remediation. It does **not** authorize implementation, patching, or any source
  edit. `authored_by` is `unrecorded`, so the same-vendor-vs-cross-vendor
  coverage measurement is a visible gap, not a captured measurement.
- Not proven: that the spec is "complete" or "ready" in any strict sense (the
  spec's own `SPEC_COMPLETE_READY_FOR_SCOPING` is the author's claim; this review
  finds it *substantially* sound with two major and four minor gaps, and takes no
  strict verdict authority over that status).

## Review-Use Boundary

These findings are **decision input** for the spec's owner/author, not mandatory
instructions and not executor-ready work. Severity labels are finding-priority
only and create no approval, rejection, readiness, validation, or
mandatory-remediation authority. Only a separately authorized patch, acceptance,
validation, or implementation lane can make any remediation here mandatory or
executor-ready. Next authorized step: return these findings to the spec
owner/author for an accept / amend / reject decision on AR-01..AR-06.
