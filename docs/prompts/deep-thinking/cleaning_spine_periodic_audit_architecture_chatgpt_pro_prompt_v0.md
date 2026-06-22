# Cleaning Spine Periodic Audit Architecture ChatGPT Pro Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Deep-thinking prompt
scope: Prompt for designing the best architecture for a periodic Cleaning spine audit.
use_when:
  - Asking ChatGPT Pro or another external reasoning model to propose a periodic no-network Cleaning audit architecture.
  - Comparing audit architecture options for detecting Cleaning spine regressions.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md
branch_or_commit: codex/cleaning-spine-continuation @ 013bedeb
```

## Orca Prompt Preflight

```yaml
output_mode: paste-ready-chat
prompt_artifact_path: docs/prompts/deep-thinking/cleaning_spine_periodic_audit_architecture_chatgpt_pro_prompt_v0.md
template_kind: deep-thinking
template_source: no bound project-local deep-thinking template used; prompt follows Orca prompt-orchestration preflight directly
edit_permission: read-only
target_workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation
target_branch: codex/cleaning-spine-continuation
target_commit: 013bedeb
dirty_state_allowance: none required for repo-capable review; if no repo access, use the embedded source capsule
target_artifacts:
  - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
  - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/smoke_summary.json
  - orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/packet_manifest.json
  - docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md
doctrine_change: none; request is architecture advice only
receiver: ChatGPT Pro or another external architecture/reasoning reviewer
```

## Paste-Ready Prompt

You are helping design a periodic audit architecture for Orca's Cleaning spine.

Goal: propose the best practical architecture for a recurring, mostly no-network audit that detects when the Cleaning spine stops preserving traceability or source meaning.

Do not write code. Do not recommend live web capture as the first periodic audit. Do not infer product readiness, validation, Judgment quality, demand, credibility, salience, or actionability. This is an architecture recommendation only.

If you have filesystem/repo access, read the listed source files first. If you do not have repo access, use the source capsule below and clearly mark any claims that would require repo verification.

### Repo-Capable Source Load

If available, read:

1. `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
2. `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
3. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/stitched/smoke_summary.json`
4. `orca-harness/_test_runs/ig_cleaning_spine_stage1_20260621/raw_cleaned_review_packet/packet_manifest.json`
5. `docs/review-outputs/adversarial-artifact-reviews/ig_cleaning_raw_vs_cleaned_adversarial_artifact_review_v0.md`

Then declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.

### Source Capsule For No-Repo Review

Current Cleaning spine evidence:

- Existing no-network stitcher: `run_capture_ecr_cleaning_smoke.py`.
- It consumes existing packet/projection/consolidation artifacts.
- It writes:
  - `ecr_source_side_receipts.json`
  - `cleaning_packet.json`
  - `smoke_summary.json`
- It supports retail, Reddit, and Instagram source entries.
- It is explicitly not live capture, not crawler, not production acceptance, not proof-run readiness, not Judgment scoring, not semantic cleaning.
- Existing tests cover the stitcher plus Cleaning core/projection integration.

Recent IG real-artifact smoke:

- Input was completed Stage 1 logged-out IG Source Capture Packets, not live capture during the Cleaning run.
- Sources:
  - `instagram:curlyscents`: 37 handles
  - `instagram:funmimonet`: 23 handles
  - `instagram:jeremyfragrance`: 37 handles
  - `instagram:theperfumeguy`: 37 handles
- Total result:
  - 4 IG packets
  - 4 ECR receipts
  - 134 Cleaning handles
  - 0 stitcher findings
- Raw-vs-cleaned packet:
  - 134 raw-cleaned pairs
  - all sampled hashes matched
  - all sampled JSON Pointers resolved
  - no Judgment vocabulary found
  - ECR residuals preserved

Independent raw-vs-cleaned review result:

- Verdict: `bounded_raw_to_cleaned_trace_supported`.
- Cleaning did not overclean meaning.
- Cleaning did not underclean traceability.
- Cleaning did not lose anchors.
- Cleaning did not introduce Judgment semantics.
- Cleaning preserved ECR residuals.
- One minor projection-layer issue was found:
  - `funmimonet:ig_call_07:view_count` had `is_video=false` but projection posture `unavailable_with_reason`; reviewer said `not_applicable` would be semantically cleaner.
  - Cleaning preserved this faithfully; not a Cleaning defect.
- Two advisory observations:
  - raw profile API view counts can exist but projection may null them under a `partial_signal` quality gate;
  - cross-account IG content URLs can appear and must be handled by identity policy, not guessed from URL alone.

Cleaning's actual job at this stage:

- Create `CleaningInputHandle` records from projection rows.
- Preserve packet ID, slice ID, file ID, relative path, SHA-256, and JSON Pointer/text anchors.
- Attach projection refs that say the projection is `not_cleaned` and `not_judgment_ready`.
- Attach ECR source-side posture refs.
- Preserve warnings, residuals, and raw-pull triggers.
- Preserve `relation: keyed_siblings_over_raw`.
- Not rewrite captions, summarize source text, infer demand, score credibility, normalize engagement meaning, or create Judgment-ready facts.

### Design Question

Design a periodic audit architecture for the Cleaning spine that answers:

> "If something breaks in packet -> projection -> ECR -> Cleaning trace preservation, how will we detect it quickly, classify it correctly, and avoid confusing Cleaning regressions with Source Capture or projection regressions?"

### Required Architecture Output

Return a concise but rigorous architecture proposal with these sections:

1. **Recommended Architecture**
   - components;
   - data flow;
   - where scheduling lives;
   - what runs no-network vs what, if anything, is deferred to later live rehearsals.

2. **Detection Matrix**
   For each breakage class, name:
   - signal checked;
   - how it is detected;
   - severity;
   - likely owner: Source Capture, projection, ECR, Cleaning, audit harness, or fixture maintenance;
   - whether the periodic audit should fail, warn, or only record.

   Include at least:
   - missing packet/projection artifact;
   - projection packet_id mismatch;
   - raw file hash mismatch;
   - JSON Pointer or text anchor no longer resolves;
   - ECR ref packet-key mismatch;
   - ECR residual suppression;
   - projection certification no longer says `not_cleaned` / `not_judgment_ready`;
   - Judgment vocabulary leakage;
   - unavailable/not-applicable/observed posture confusion;
   - fake zero values for unavailable metrics;
   - count drift across fixtures;
   - review packet wrapper drift, like missing `relation`;
   - source fixture staleness;
   - absolute-path portability issues.

3. **Cadence**
   Recommend what should run:
   - on PR or pre-merge;
   - nightly or weekly;
   - monthly or manual only.

4. **Audit Manifest Design**
   Describe the manifest shape: what artifacts it names, what expectations are exact, what expectations are invariant-based, and how to avoid brittle golden-file testing.

5. **Audit Report Design**
   Describe the output report fields: counts, pass/warn/fail, new findings, owner classification, artifact links, residuals, and non-claims.

6. **Baseline And Drift Policy**
   Explain how to decide whether count changes are acceptable fixture drift, projection behavior change, or Cleaning breakage.

7. **Escalation Policy**
   What should page/block immediately, what should become a ticket, and what should stay advisory?

8. **Rollout Plan**
   Give a smallest-complete rollout sequence: v0, v1, v2. Keep v0 intentionally boring.

9. **Anti-Patterns**
   Name what we should avoid, especially coupling this first audit to live capture, product proof, or Judgment readiness.

10. **Open Questions**
   Name only the questions that materially affect architecture.

### Constraints

- First periodic audit should be deterministic and no-network.
- It should consume packet-grade artifacts, not run live web capture.
- It must preserve failure visibility; do not invent fake success if input artifacts are missing.
- It must distinguish Cleaning defects from projection/source defects.
- It must not treat ECR residuals as failure by themselves.
- It must not claim production readiness, product proof, Judgment quality, or full Orca E2E readiness.
- It should be easy to run locally, in CI/pre-merge, and from a scheduled automation.

### Preferred Answer Style

Be direct. Favor a practical architecture over a large platform design. Give clear severity/ownership rules. If you recommend a scheduler, distinguish app-level scheduling from repo-level audit code. If there are multiple viable designs, pick one and explain why.
